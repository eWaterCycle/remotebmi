//! HTTP/1.1 client transport for remotebmi.client.lean.LeanBmiClient.

use std::io::{self, Write};
use std::net::TcpStream;
use std::sync::Mutex;
use std::time::Duration;

use pyo3::buffer::PyBuffer;
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyDict};

use crate::body::Body;
use crate::http::{has_token, header, invalid_data, BufConn, MAX_HEAD};

const MAX_BODY: usize = 4 << 30;

struct ResponseParts {
    status: u16,
    content_type: String,
    content_encoding: String,
    accept_encoding: String,
    body: Vec<u8>,
}

/// Whether the server closed an idle connection (or sent something unexpected).
#[cfg(unix)]
fn is_closed(stream: &TcpStream) -> bool {
    use std::os::fd::AsRawFd;
    let mut byte = [0u8; 1];
    let n = unsafe {
        libc::recv(
            stream.as_raw_fd(),
            byte.as_mut_ptr() as *mut libc::c_void,
            1,
            libc::MSG_PEEK | libc::MSG_DONTWAIT,
        )
    };
    if n < 0 {
        let err = io::Error::last_os_error();
        return err.kind() != io::ErrorKind::WouldBlock;
    }
    true
}

#[cfg(not(unix))]
fn is_closed(stream: &TcpStream) -> bool {
    let mut byte = [0u8; 1];
    if stream.set_nonblocking(true).is_err() {
        return true;
    }
    let result = stream.peek(&mut byte);
    let _ = stream.set_nonblocking(false);
    !matches!(result, Err(ref e) if e.kind() == io::ErrorKind::WouldBlock)
}

fn read_response(
    conn: &mut BufConn<TcpStream>,
    head_request: bool,
) -> io::Result<(ResponseParts, bool)> {
    loop {
        if !conn.buffered().is_empty() {
            let mut headers = [httparse::EMPTY_HEADER; 64];
            let mut parsed = httparse::Response::new(&mut headers);
            match parsed.parse(conn.buffered()) {
                Ok(httparse::Status::Complete(head_len)) => {
                    let status = parsed.code.unwrap_or(0);
                    let h = &*parsed.headers;
                    let get = |name| header(h, name).unwrap_or("").to_owned();
                    let content_type = get("content-type");
                    let content_encoding = get("content-encoding");
                    let accept_encoding = get("accept-encoding");
                    let http10 = parsed.version == Some(0);
                    let connection = header(h, "connection").unwrap_or("");
                    let mut keep_alive = if http10 {
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
                    conn.consume(head_len);
                    if (100..200).contains(&status) {
                        // Interim response, real response follows
                        continue;
                    }
                    let body = if head_request || status == 204 || status == 304 {
                        Vec::new()
                    } else if chunked {
                        conn.read_chunked(MAX_BODY)?
                    } else if let Some(n) = content_length {
                        conn.read_exact_vec(n)?
                    } else {
                        keep_alive = false;
                        conn.read_to_close()?
                    };
                    let parts = ResponseParts {
                        status,
                        content_type,
                        content_encoding,
                        accept_encoding,
                        body,
                    };
                    return Ok((parts, keep_alive));
                }
                Ok(httparse::Status::Partial) => {
                    if conn.buffered().len() > MAX_HEAD {
                        return Err(invalid_data("response head too large"));
                    }
                }
                Err(e) => return Err(invalid_data(e.to_string())),
            }
        }
        if conn.fill()? == 0 {
            return Err(io::Error::new(
                io::ErrorKind::ConnectionAborted,
                "server closed connection without response",
            ));
        }
    }
}

/// Sends HTTP requests over one reused TCP connection.
///
/// Implements the Transport protocol of remotebmi.client.lean.
#[pyclass(frozen, module = "remotebmi_rs")]
pub struct RustTransport {
    host: String,
    port: u16,
    prefix: String,
    timeout: Option<Duration>,
    keep_alive: bool,
    connection: Mutex<Option<BufConn<TcpStream>>>,
}

impl RustTransport {
    fn connect(&self) -> io::Result<BufConn<TcpStream>> {
        let stream = TcpStream::connect((self.host.as_str(), self.port))?;
        stream.set_nodelay(true)?;
        stream.set_read_timeout(self.timeout)?;
        stream.set_write_timeout(self.timeout)?;
        Ok(BufConn::new(stream))
    }

    fn send(&self, head: &[u8], body: &[u8], head_request: bool) -> io::Result<ResponseParts> {
        let mut guard = self.connection.lock().unwrap_or_else(|e| e.into_inner());
        if let Some(conn) = guard.as_ref() {
            if is_closed(&conn.stream) {
                *guard = None;
            }
        }
        let conn = match guard.as_mut() {
            Some(conn) => conn,
            None => guard.insert(self.connect()?),
        };
        let result = conn
            .write_message(head, body)
            .and_then(|_| read_response(conn, head_request));
        match result {
            Ok((parts, keep_alive)) => {
                if !keep_alive || !self.keep_alive {
                    *guard = None;
                }
                Ok(parts)
            }
            Err(e) => {
                *guard = None;
                Err(e)
            }
        }
    }
}

#[pymethods]
impl RustTransport {
    #[new]
    #[pyo3(signature = (host, port, prefix="", timeout=None, keep_alive=true))]
    fn new(host: String, port: u16, prefix: &str, timeout: Option<f64>, keep_alive: bool) -> Self {
        RustTransport {
            host,
            port,
            prefix: prefix.to_owned(),
            timeout: timeout.filter(|t| *t > 0.0).map(Duration::from_secs_f64),
            keep_alive,
            connection: Mutex::new(None),
        }
    }

    /// Send request, returns status, content type, content encoding,
    /// accept encoding and body.
    ///
    /// Body of an application/octet-stream response is a Body object
    /// to avoid copying, other bodies are bytes.
    #[pyo3(signature = (method, path, body=None, headers=None))]
    fn request<'py>(
        &self,
        py: Python<'py>,
        method: &str,
        path: &str,
        body: Option<Bound<'py, PyAny>>,
        headers: Option<Bound<'py, PyDict>>,
    ) -> PyResult<(u16, String, String, String, Bound<'py, PyAny>)> {
        let body = match &body {
            Some(b) if !b.is_none() => {
                let buffer = PyBuffer::<u8>::get(b)?;
                if !buffer.is_c_contiguous() {
                    return Err(pyo3::exceptions::PyBufferError::new_err(
                        "Request body must be C contiguous",
                    ));
                }
                Some(buffer)
            }
            _ => None,
        };
        let mut head = Vec::with_capacity(256);
        write!(
            head,
            "{} {}{} HTTP/1.1\r\nhost: {}:{}\r\n",
            method, self.prefix, path, self.host, self.port
        )?;
        if let Some(headers) = &headers {
            for (key, value) in headers.iter() {
                write!(head, "{}: {}\r\n", key.str()?, value.str()?)?;
            }
        }
        let body_len = body.as_ref().map(|b| b.len_bytes()).unwrap_or(0);
        if body.is_some() || method == "POST" {
            write!(head, "content-length: {}\r\n", body_len)?;
        }
        if !self.keep_alive {
            head.extend_from_slice(b"connection: close\r\n");
        }
        head.extend_from_slice(b"\r\n");
        let head_request = method == "HEAD";
        let parts = py.detach(|| {
            // Buffer stays valid while PyBuffer is held, reading does not need the GIL.
            let body_slice = match &body {
                Some(b) => unsafe {
                    std::slice::from_raw_parts(b.buf_ptr() as *const u8, b.len_bytes())
                },
                None => &[][..],
            };
            self.send(&head, body_slice, head_request)
        });
        drop(body);
        let parts = parts?;
        let body = if parts.content_type.starts_with("application/octet-stream")
            && !parts.body.is_empty()
        {
            Bound::new(py, Body::new(parts.body))?.into_any()
        } else {
            PyBytes::new(py, &parts.body).into_any()
        };
        Ok((
            parts.status,
            parts.content_type,
            parts.content_encoding,
            parts.accept_encoding,
            body,
        ))
    }

    /// Close the connection, next request opens a new one.
    fn close(&self, py: Python<'_>) {
        py.detach(|| {
            *self.connection.lock().unwrap_or_else(|e| e.into_inner()) = None;
        });
    }
}
