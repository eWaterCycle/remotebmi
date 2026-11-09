//! Bytes owned by Rust, exposed to Python with the buffer protocol without copying.

use std::os::raw::{c_int, c_void};

use pyo3::exceptions::PyBufferError;
use pyo3::ffi;
use pyo3::prelude::*;

/// Read-only bytes-like object, for example `numpy.frombuffer(body)` does not copy.
#[pyclass(frozen, module = "remotebmi_rs")]
pub struct Body {
    data: Vec<u8>,
}

impl Body {
    pub fn new(data: Vec<u8>) -> Self {
        Body { data }
    }
}

#[pymethods]
impl Body {
    unsafe fn __getbuffer__(
        slf: Bound<'_, Self>,
        view: *mut ffi::Py_buffer,
        flags: c_int,
    ) -> PyResult<()> {
        if view.is_null() {
            return Err(PyBufferError::new_err("View is null"));
        }
        let data = &slf.get().data;
        // Fills view for read-only bytes and keeps a reference to slf in view.obj
        let result = unsafe {
            ffi::PyBuffer_FillInfo(
                view,
                slf.as_ptr(),
                data.as_ptr() as *mut c_void,
                data.len() as ffi::Py_ssize_t,
                1,
                flags,
            )
        };
        if result == -1 {
            return Err(PyErr::fetch(slf.py()));
        }
        Ok(())
    }

    unsafe fn __releasebuffer__(&self, _view: *mut ffi::Py_buffer) {}

    fn __len__(&self) -> usize {
        self.data.len()
    }

    fn __repr__(&self) -> String {
        format!("<remotebmi_rs.Body of {} bytes>", self.data.len())
    }
}
