//! HTTP/1.1 server that calls a Python handler for each request.
//!
//! One thread per connection with blocking IO, which has the lowest latency
//! for the few connections a BMI server has.
//! The GIL is only held while calling the handler.

use std::collections::{HashMap, HashSet};
use std::io::{self, Write};
use std::net::{Shutdown, SocketAddr, TcpListener, TcpStream, ToSocketAddrs};
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::{Arc, Condvar, Mutex};
use std::thread::JoinHandle;

use pyo3::buffer::PyBuffer;
use pyo3::prelude::*;
use pyo3::types::PyBytes;

use crate::body::Body;
use crate::http::{
    accepts_zstd, has_token, header, invalid_data, json_string, percent_decode, reason, BufConn,
    MAX_HEAD,
};

/// Maximum size of a decompressed or chunked request body.
const MAX_BODY: usize = 4 << 30;
const CORS_METHODS: [&str; 3] = ["DELETE", "GET", "POST"];
const CORS_MAX_AGE: u32 = 600;
const PREFLIGHT_VARY: &str = "Origin, Access-Control-Request-Method, \
    Access-Control-Request-Headers, Access-Control-Request-Private-Network";

/// Same behavior as CorsPolicy in remotebmi/_http.py.
struct Cors {
    allow_all: bool,
    origins: HashSet<String>,
}

impl Cors {
    fn allowed<'a>(&self, origin: &'a str) -> Option<&'a str> {
        if self.allow_all {
            Some("*")
        } else if self.origins.contains(origin) {
            Some(origin)
        } else {
            None
        }
    }

    fn headers(&self, origin: Option<&str>, out: &mut Vec<u8>) {
        if let Some(allowed) = origin.and_then(|o| self.allowed(o)) {
            push_header(out, "access-control-allow-origin", allowed);
        }
        push_header(out, "vary", "Origin");
    }

    fn preflight(&self, req: &Request, origin: &str, method: &str) -> Response {
        let mut headers = Vec::new();
        push_header(&mut headers, "vary", PREFLIGHT_VARY);
        let mut failures = Vec::new();
        match self.allowed(origin) {
            Some(allowed) => push_header(&mut headers, "access-control-allow-origin", allowed),
            None => failures.push("origin"),
        }
        if !CORS_METHODS.contains(&method) {
            failures.push("method");
        }
        push_header(
            &mut headers,
            "access-control-allow-methods",
            &CORS_METHODS.join(", "),
        );
        push_header(
            &mut headers,
            "access-control-max-age",
            &CORS_MAX_AGE.to_string(),
        );
        if let Some(requested) = &req.preflight_headers {
            push_header(&mut headers, "access-control-allow-headers", requested);
        }
        push_header(&mut headers, "content-type", "text/plain; charset=utf-8");
        let (status, text) = if failures.is_empty() {
            (200, "OK".to_owned())
        } else {
            (400, format!("Disallowed CORS {}", failures.join(", ")))
        };
        Response {
            status,
            content_type: String::new(),
            body: ResponseBody::Owned(text.into_bytes()),
            allow: String::new(),
            extra_headers: headers,
            compress: false,
            preflight: true,
        }
    }
}

fn push_header(out: &mut Vec<u8>, name: &str, value: &str) {
    out.extend_from_slice(name.as_bytes());
    out.extend_from_slice(b": ");
    out.extend_from_slice(value.as_bytes());
    out.extend_from_slice(b"\r\n");
}

struct Shared {
    handler: Py<PyAny>,
    cors: Option<Cors>,
    compression_level: i32,
    min_compress_size: usize,
    /// Model methods are called one at a time
    model_lock: ModelLock,
    stop: AtomicBool,
    /// Open connections by id, to close them on stop
    connections: Mutex<HashMap<u64, TcpStream>>,
    next_connection_id: AtomicU64,
}

struct Request {
    method: String,
    path: String,
    accept: String,
    content_type: String,
    content_encoding: String,
    accept_encoding: String,
    origin: Option<String>,
    preflight_method: Option<String>,
    preflight_headers: Option<String>,
    keep_alive: bool,
    body: Vec<u8>,
}

enum ResponseBody {
    Owned(Vec<u8>),
    Python(PyBuffer<u8>),
}

impl ResponseBody {
    fn as_slice(&self) -> &[u8] {
        match self {
            ResponseBody::Owned(v) => v,
            // Buffer stays valid while PyBuffer is held, reading does not need the GIL.
            ResponseBody::Python(b) => unsafe {
                std::slice::from_raw_parts(b.buf_ptr() as *const u8, b.len_bytes())
            },
        }
    }
}

struct Response {
    status: u16,
    content_type: String,
    body: ResponseBody,
    allow: String,
    extra_headers: Vec<u8>,
    compress: bool,
    /// Response to CORS preflight request, gets no other headers
    preflight: bool,
}

fn problem(status: u16, title: &str, detail: &str) -> Response {
    let body = format!(
        "{{\"type\": \"about:blank\", \"title\": {}, \"detail\": {}, \"status\": {}}}",
        json_string(title),
        json_string(detail),
        status
    );
    Response {
        status,
        content_type: "application/problem+json".to_owned(),
        body: ResponseBody::Owned(body.into_bytes()),
        allow: String::new(),
        extra_headers: Vec::new(),
        compress: false,
        preflight: false,
    }
}

/// Read request head and body, None when connection was closed between requests.
fn read_request(conn: &mut BufConn<TcpStream>) -> io::Result<Option<Request>> {
    loop {
        if !conn.buffered().is_empty() {
            let mut headers = [httparse::EMPTY_HEADER; 64];
            let mut parsed = httparse::Request::new(&mut headers);
            match parsed.parse(conn.buffered()) {
                Ok(httparse::Status::Complete(head_len)) => {
                    let h = &*parsed.headers;
                    let get = |name| header(h, name).unwrap_or("").to_owned();
                    let raw_path = parsed.path.unwrap_or("/");
                    let path = percent_decode(raw_path.split('?').next().unwrap_or(""));
                    let http10 = parsed.version == Some(0);
                    let connection = header(h, "connection").unwrap_or("");
                    let keep_alive = if http10 {
                        has_token(connection, "keep-alive")
                    } else {
                        !has_token(connection, "close")
                    };
                    let chunked = header(h, "transfer-encoding")
                        .map(|te| has_token(te, "chunked"))
                        .unwrap_or(false);
                    let content_length = match header(h, "content-length") {
                        Some(v) => Some(
                            v.trim()
                                .parse::<usize>()
                                .map_err(|_| invalid_data("invalid content-length"))?,
                        ),
                        None => None,
                    };
                    let expect_continue = header(h, "expect")
                        .map(|e| e.trim().eq_ignore_ascii_case("100-continue"))
                        .unwrap_or(false);
                    let mut request = Request {
                        method: parsed.method.unwrap_or("").to_owned(),
                        path,
                        accept: get("accept"),
                        content_type: get("content-type"),
                        content_encoding: get("content-encoding").trim().to_ascii_lowercase(),
                        accept_encoding: get("accept-encoding"),
                        origin: header(h, "origin").map(str::to_owned),
                        preflight_method: header(h, "access-control-request-method")
                            .map(str::to_owned),
                        preflight_headers: header(h, "access-control-request-headers")
                            .map(str::to_owned),
                        keep_alive,
                        body: Vec::new(),
                    };
                    conn.consume(head_len);
                    if expect_continue && (chunked || content_length.unwrap_or(0) > 0) {
                        conn.stream.write_all(b"HTTP/1.1 100 Continue\r\n\r\n")?;
                    }
                    if chunked {
                        request.body = conn.read_chunked(MAX_BODY)?;
                    } else if let Some(n) = content_length {
                        request.body = conn.read_exact_vec(n)?;
                    }
                    return Ok(Some(request));
                }
                Ok(httparse::Status::Partial) => {
                    if conn.buffered().len() > MAX_HEAD {
                        return Err(invalid_data("request head too large"));
                    }
                }
                Err(e) => return Err(invalid_data(e.to_string())),
            }
        }
        if conn.fill()? == 0 {
            if conn.buffered().is_empty() {
                return Ok(None);
            }
            return Err(io::Error::new(
                io::ErrorKind::UnexpectedEof,
                "connection closed in request head",
            ));
        }
    }
}

/// Lets one connection at a time call the model.
struct ModelLock {
    busy: Mutex<bool>,
    released: Condvar,
}

struct ModelGuard<'a>(&'a ModelLock);

impl ModelLock {
    fn new() -> Self {
        ModelLock {
            busy: Mutex::new(false),
            released: Condvar::new(),
        }
    }

    fn try_acquire(&self) -> bool {
        let mut busy = lock(&self.busy);
        !std::mem::replace(&mut *busy, true)
    }

    fn acquire(&self) {
        let mut busy = lock(&self.busy);
        while *busy {
            busy = self.released.wait(busy).unwrap_or_else(|e| e.into_inner());
        }
        *busy = true;
    }

    /// Lock, waiting without holding the GIL so the holder can finish.
    fn lock(&self, py: Python<'_>) -> ModelGuard<'_> {
        if !self.try_acquire() {
            py.detach(|| self.acquire());
        }
        ModelGuard(self)
    }
}

impl Drop for ModelGuard<'_> {
    fn drop(&mut self) {
        *lock(&self.0.busy) = false;
        self.0.released.notify_one();
    }
}

fn call_handler(py: Python<'_>, shared: &Shared, request: &Request, body: Vec<u8>) -> Response {
    let _guard = shared.model_lock.lock(py);
    let result = (|| -> PyResult<Response> {
        let body = if body.is_empty() {
            PyBytes::new(py, b"").into_any()
        } else {
            Bound::new(py, Body::new(body))?.into_any()
        };
        let result = shared.handler.bind(py).call1((
            request.method.as_str(),
            request.path.as_str(),
            request.accept.as_str(),
            request.content_type.as_str(),
            body,
        ))?;
        let (status, content_type, body, allow): (u16, String, Bound<'_, PyAny>, String) =
            result.extract()?;
        let buffer = PyBuffer::<u8>::get(&body)?;
        if !buffer.is_c_contiguous() {
            return Err(pyo3::exceptions::PyBufferError::new_err(
                "Response body must be C contiguous",
            ));
        }
        Ok(Response {
            status,
            content_type,
            body: ResponseBody::Python(buffer),
            allow,
            extra_headers: Vec::new(),
            compress: true,
            preflight: false,
        })
    })();
    result.unwrap_or_else(|e| problem(500, "Internal Server Error", &e.value(py).to_string()))
}

fn handle(py: Python<'_>, shared: &Shared, request: &mut Request) -> Response {
    if let (Some(cors), "OPTIONS", Some(origin), Some(method)) = (
        &shared.cors,
        request.method.as_str(),
        &request.origin,
        &request.preflight_method,
    ) {
        return cors.preflight(request, origin, method);
    }
    let body = std::mem::take(&mut request.body);
    let body = match request.content_encoding.as_str() {
        "" | "identity" => body,
        "zstd" => match py.detach(|| zstd::stream::decode_all(&body[..])) {
            Ok(decoded) if decoded.len() <= MAX_BODY => decoded,
            Ok(_) => return problem(400, "Bad Request", "Decompressed body too large"),
            Err(e) => return problem(400, "Bad Request", &e.to_string()),
        },
        other => {
            let detail = format!("Unsupported Content-Encoding ({other})");
            return problem(415, "Unsupported Media Type", &detail);
        }
    };
    call_handler(py, shared, request, body)
}

/// Compress and write response, does not need the GIL.
fn write_response(
    shared: &Shared,
    conn: &mut BufConn<TcpStream>,
    request: &Request,
    response: &Response,
    head: &mut Vec<u8>,
) -> io::Result<()> {
    let compressed;
    let mut body = response.body.as_slice();
    head.clear();
    write!(
        head,
        "HTTP/1.1 {} {}\r\n",
        response.status,
        reason(response.status)
    )?;
    if !response.preflight {
        push_header(head, "accept-encoding", "zstd");
    }
    if !response.content_type.is_empty() {
        push_header(head, "content-type", &response.content_type);
    }
    if !response.allow.is_empty() {
        push_header(head, "allow", &response.allow);
    }
    if response.compress
        && body.len() >= shared.min_compress_size
        && accepts_zstd(&request.accept_encoding)
    {
        compressed = zstd::bulk::compress(body, shared.compression_level)?;
        body = &compressed;
        push_header(head, "content-encoding", "zstd");
        push_header(head, "vary", "Accept-Encoding");
    }
    head.extend_from_slice(&response.extra_headers);
    if let (Some(cors), false) = (&shared.cors, response.preflight) {
        cors.headers(request.origin.as_deref(), head);
    }
    if response.status != 204 {
        push_header(head, "content-length", &body.len().to_string());
    }
    if !request.keep_alive {
        push_header(head, "connection", "close");
    }
    head.extend_from_slice(b"\r\n");
    if request.method == "HEAD" || response.status == 204 {
        body = &[];
    }
    conn.write_message(head, body)
}

fn serve_connection(shared: &Shared, stream: TcpStream) {
    // Stay attached to the interpreter and only release the GIL around IO,
    // as attaching a new thread state for each request is slow.
    Python::attach(|py| {
        let mut conn = BufConn::new(stream);
        let mut head = Vec::with_capacity(512);
        loop {
            let mut request = match py.detach(|| read_request(&mut conn)) {
                Ok(Some(request)) => request,
                Ok(None) => return,
                Err(e) => {
                    if e.kind() == io::ErrorKind::InvalidData {
                        let body = e.to_string();
                        let _ = write!(
                            conn.stream,
                            "HTTP/1.1 400 Bad Request\r\ncontent-type: text/plain\r\n\
                             content-length: {}\r\nconnection: close\r\n\r\n{}",
                            body.len(),
                            body
                        );
                    }
                    return;
                }
            };
            let response = handle(py, shared, &mut request);
            let written =
                py.detach(|| write_response(shared, &mut conn, &request, &response, &mut head));
            // Release Python buffer while attached
            drop(response);
            if written.is_err() || !request.keep_alive {
                return;
            }
        }
    });
}

/// Lock mutex, also when another thread panicked while holding it.
fn lock<T>(mutex: &Mutex<T>) -> std::sync::MutexGuard<'_, T> {
    mutex.lock().unwrap_or_else(|e| e.into_inner())
}

fn accept_loop(shared: Arc<Shared>, listener: TcpListener) {
    for stream in listener.incoming() {
        if shared.stop.load(Ordering::SeqCst) {
            return;
        }
        let Ok(stream) = stream else { continue };
        let _ = stream.set_nodelay(true);
        let id = shared.next_connection_id.fetch_add(1, Ordering::SeqCst);
        if let Ok(clone) = stream.try_clone() {
            lock(&shared.connections).insert(id, clone);
        }
        let shared = shared.clone();
        std::thread::spawn(move || {
            serve_connection(&shared, stream);
            lock(&shared.connections).remove(&id);
        });
    }
}

/// HTTP server calling `handler(method, path, accept, content_type, body)` for each request.
///
/// The handler returns a tuple of status code, content type, body (bytes-like) and
/// value of Allow header, like `remotebmi.server.lean.Dispatcher`.
/// The server handles CORS and zstd content encoding itself.
/// Serving starts on construction, in background threads.
#[pyclass(frozen, module = "remotebmi_rs")]
pub struct RustServer {
    shared: Arc<Shared>,
    addr: SocketAddr,
    thread: Mutex<Option<JoinHandle<()>>>,
}

#[pymethods]
impl RustServer {
    #[new]
    #[pyo3(signature = (handler, host="127.0.0.1", port=0, cors_origins=None, compression_level=1, min_compress_size=1024))]
    fn new(
        handler: Py<PyAny>,
        host: &str,
        port: u16,
        cors_origins: Option<Vec<String>>,
        compression_level: i32,
        min_compress_size: usize,
    ) -> PyResult<Self> {
        let listener = TcpListener::bind((host, port))?;
        let addr = listener.local_addr()?;
        let cors = cors_origins.filter(|o| !o.is_empty()).map(|origins| Cors {
            allow_all: origins.iter().any(|o| o == "*"),
            origins: origins.into_iter().collect(),
        });
        let shared = Arc::new(Shared {
            handler,
            cors,
            compression_level,
            min_compress_size,
            model_lock: ModelLock::new(),
            stop: AtomicBool::new(false),
            connections: Mutex::new(HashMap::new()),
            next_connection_id: AtomicU64::new(0),
        });
        let thread_shared = shared.clone();
        let thread = std::thread::spawn(move || accept_loop(thread_shared, listener));
        Ok(RustServer {
            shared,
            addr,
            thread: Mutex::new(Some(thread)),
        })
    }

    /// Port the server listens on.
    #[getter]
    fn port(&self) -> u16 {
        self.addr.port()
    }

    /// Stop accepting connections and close open connections.
    fn stop(&self, py: Python<'_>) {
        py.detach(|| {
            if self.shared.stop.swap(true, Ordering::SeqCst) {
                return;
            }
            // Wake up accept loop
            let wake = if self.addr.ip().is_unspecified() {
                let localhost = if self.addr.is_ipv4() {
                    "127.0.0.1"
                } else {
                    "::1"
                };
                (localhost, self.addr.port())
                    .to_socket_addrs()
                    .ok()
                    .and_then(|mut a| a.next())
            } else {
                Some(self.addr)
            };
            if let Some(wake) = wake {
                let _ = TcpStream::connect(wake);
            }
            for (_, connection) in lock(&self.shared.connections).drain() {
                let _ = connection.shutdown(Shutdown::Both);
            }
            if let Some(thread) = lock(&self.thread).take() {
                let _ = thread.join();
            }
        });
    }

    fn __enter__(slf: Py<Self>) -> Py<Self> {
        slf
    }

    fn __exit__(
        &self,
        py: Python<'_>,
        _exc_type: Option<Bound<'_, PyAny>>,
        _exc: Option<Bound<'_, PyAny>>,
        _tb: Option<Bound<'_, PyAny>>,
    ) {
        self.stop(py);
    }
}
