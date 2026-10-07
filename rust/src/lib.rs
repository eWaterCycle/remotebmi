//! Rust HTTP server and client transport for remotebmi.
//!
//! The server parses HTTP, handles CORS and zstd compression and calls
//! `remotebmi.server.lean.Dispatcher` for the BMI part,
//! so it serves the same API as the Python servers.

mod body;
mod client;
mod http;
mod server;

use pyo3::prelude::*;

#[pymodule]
fn remotebmi_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<body::Body>()?;
    m.add_class::<client::RustTransport>()?;
    m.add_class::<server::RustServer>()?;
    Ok(())
}
