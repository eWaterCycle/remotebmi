//! HTTP/1.1 framing shared by server and client.

use std::io::{self, IoSlice, Read, Write};

/// Maximum size of request or response head.
pub const MAX_HEAD: usize = 64 * 1024;
const READ_CHUNK: usize = 64 * 1024;

pub fn invalid_data(msg: impl Into<String>) -> io::Error {
    io::Error::new(io::ErrorKind::InvalidData, msg.into())
}

/// Buffered reader over a stream, keeps bytes read beyond current message.
pub struct BufConn<S> {
    pub stream: S,
    /// Storage, bytes start..end are read but not consumed yet
    buf: Vec<u8>,
    start: usize,
    end: usize,
}

impl<S: Read + Write> BufConn<S> {
    pub fn new(stream: S) -> Self {
        BufConn {
            stream,
            buf: vec![0; READ_CHUNK],
            start: 0,
            end: 0,
        }
    }

    pub fn buffered(&self) -> &[u8] {
        &self.buf[self.start..self.end]
    }

    pub fn consume(&mut self, n: usize) {
        self.start += n;
        if self.start == self.end {
            self.start = 0;
            self.end = 0;
        }
    }

    /// Read more bytes into buffer, returns number of bytes read (0 at end of stream).
    pub fn fill(&mut self) -> io::Result<usize> {
        if self.start > 0 {
            self.buf.copy_within(self.start..self.end, 0);
            self.end -= self.start;
            self.start = 0;
        }
        if self.end == self.buf.len() {
            self.buf.resize(self.buf.len() * 2, 0);
        }
        let n = self.stream.read(&mut self.buf[self.end..])?;
        self.end += n;
        Ok(n)
    }

    /// Read exactly n bytes of body.
    pub fn read_exact_vec(&mut self, n: usize) -> io::Result<Vec<u8>> {
        let buffered = self.buffered();
        if buffered.len() >= n {
            let body = buffered[..n].to_vec();
            self.consume(n);
            return Ok(body);
        }
        let mut body = Vec::with_capacity(n);
        body.extend_from_slice(buffered);
        let have = buffered.len();
        self.consume(have);
        let read = (&mut self.stream)
            .take((n - have) as u64)
            .read_to_end(&mut body)?;
        if have + read != n {
            return Err(io::Error::new(
                io::ErrorKind::UnexpectedEof,
                "connection closed before end of body",
            ));
        }
        Ok(body)
    }

    /// Read a CRLF terminated line, without the CRLF.
    fn read_line(&mut self) -> io::Result<Vec<u8>> {
        loop {
            if let Some(i) = self.buffered().windows(2).position(|w| w == b"\r\n") {
                let line = self.buffered()[..i].to_vec();
                self.consume(i + 2);
                return Ok(line);
            }
            if self.buffered().len() > MAX_HEAD {
                return Err(invalid_data("line too long"));
            }
            if self.fill()? == 0 {
                return Err(io::Error::new(
                    io::ErrorKind::UnexpectedEof,
                    "connection closed in chunked body",
                ));
            }
        }
    }

    /// Read body with chunked transfer encoding.
    pub fn read_chunked(&mut self, max: usize) -> io::Result<Vec<u8>> {
        let mut body = Vec::new();
        loop {
            let line = self.read_line()?;
            let size_text = std::str::from_utf8(&line)
                .ok()
                .and_then(|l| l.split(';').next())
                .map(str::trim)
                .ok_or_else(|| invalid_data("invalid chunk size"))?;
            let size = usize::from_str_radix(size_text, 16)
                .map_err(|_| invalid_data("invalid chunk size"))?;
            if size == 0 {
                // Skip trailers
                while !self.read_line()?.is_empty() {}
                return Ok(body);
            }
            if body.len() + size > max {
                return Err(invalid_data("body too large"));
            }
            body.extend(self.read_exact_vec(size)?);
            if !self.read_line()?.is_empty() {
                return Err(invalid_data("missing CRLF after chunk"));
            }
        }
    }

    /// Read until end of stream.
    pub fn read_to_close(&mut self) -> io::Result<Vec<u8>> {
        let mut body = self.buffered().to_vec();
        let have = body.len();
        self.consume(have);
        self.stream.read_to_end(&mut body)?;
        Ok(body)
    }

    /// Write head and body, in one system call when possible.
    pub fn write_message(&mut self, head: &[u8], body: &[u8]) -> io::Result<()> {
        write_all_vectored(&mut self.stream, head, body)
    }
}

pub fn write_all_vectored<W: Write>(w: &mut W, head: &[u8], body: &[u8]) -> io::Result<()> {
    let (mut head, mut body) = (head, body);
    while !head.is_empty() {
        let n = w.write_vectored(&[IoSlice::new(head), IoSlice::new(body)])?;
        if n == 0 {
            return Err(io::ErrorKind::WriteZero.into());
        }
        if n >= head.len() {
            body = &body[n - head.len()..];
            head = &[];
        } else {
            head = &head[n..];
        }
    }
    w.write_all(body)
}

/// Find header value, case-insensitive name.
pub fn header<'a>(headers: &[httparse::Header<'a>], name: &str) -> Option<&'a str> {
    headers
        .iter()
        .find(|h| h.name.eq_ignore_ascii_case(name))
        .and_then(|h| std::str::from_utf8(h.value).ok())
}

/// Whether a comma separated header value contains a token, case-insensitive.
pub fn has_token(value: &str, token: &str) -> bool {
    value
        .split(',')
        .any(|t| t.trim().eq_ignore_ascii_case(token))
}

/// Whether Accept-Encoding header value accepts zstd.
pub fn accepts_zstd(accept_encoding: &str) -> bool {
    for coding in accept_encoding.split(',') {
        let mut parts = coding.split(';');
        let name = parts.next().unwrap_or("").trim();
        if !(name.eq_ignore_ascii_case("zstd") || name == "*") {
            continue;
        }
        for param in parts {
            if let Some((key, value)) = param.split_once('=') {
                if key.trim() == "q" {
                    return value
                        .trim()
                        .parse::<f64>()
                        .map(|q| q > 0.0)
                        .unwrap_or(false);
                }
            }
        }
        return true;
    }
    false
}

/// Percent-decode path like uvicorn does, invalid UTF-8 is replaced.
pub fn percent_decode(path: &str) -> String {
    let bytes = path.as_bytes();
    if !bytes.contains(&b'%') {
        return path.to_owned();
    }
    let mut out = Vec::with_capacity(bytes.len());
    let mut i = 0;
    while i < bytes.len() {
        if bytes[i] == b'%' && i + 2 < bytes.len() {
            let hex = std::str::from_utf8(&bytes[i + 1..i + 3]).ok();
            if let Some(v) = hex.and_then(|h| u8::from_str_radix(h, 16).ok()) {
                out.push(v);
                i += 3;
                continue;
            }
        }
        out.push(bytes[i]);
        i += 1;
    }
    String::from_utf8_lossy(&out).into_owned()
}

/// Escape string for use in JSON.
pub fn json_string(s: &str) -> String {
    let mut out = String::with_capacity(s.len() + 2);
    out.push('"');
    for c in s.chars() {
        match c {
            '"' => out.push_str("\\\""),
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            c if (c as u32) < 0x20 => out.push_str(&format!("\\u{:04x}", c as u32)),
            c => out.push(c),
        }
    }
    out.push('"');
    out
}

pub fn reason(status: u16) -> &'static str {
    match status {
        100 => "Continue",
        200 => "OK",
        201 => "Created",
        204 => "No Content",
        400 => "Bad Request",
        404 => "Not Found",
        405 => "Method Not Allowed",
        411 => "Length Required",
        413 => "Content Too Large",
        415 => "Unsupported Media Type",
        431 => "Request Header Fields Too Large",
        500 => "Internal Server Error",
        _ => "",
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn decodes_percent() {
        assert_eq!(percent_decode("/a%20b"), "/a b");
        assert_eq!(percent_decode("/a%2Fb"), "/a/b");
        assert_eq!(percent_decode("/a%2"), "/a%2");
        assert_eq!(percent_decode("/a%zz"), "/a%zz");
    }

    #[test]
    fn zstd_negotiation() {
        assert!(accepts_zstd("gzip, zstd"));
        assert!(accepts_zstd("zstd;q=0.5"));
        assert!(!accepts_zstd("zstd;q=0"));
        assert!(!accepts_zstd("gzip"));
        assert!(accepts_zstd("*"));
    }

    #[test]
    fn chunked() {
        let data: &[u8] = b"5\r\nhello\r\n6;ext=1\r\n world\r\n0\r\n\r\nrest";
        let mut conn = BufConn::new(std::io::Cursor::new(data.to_vec()));
        assert_eq!(conn.read_chunked(1 << 20).unwrap(), b"hello world");
        assert_eq!(conn.buffered(), b"rest");
    }
}
