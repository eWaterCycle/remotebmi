# remotebmi-rs

Experimental Rust HTTP server and client transport for the Python [remotebmi](../python) package,
built with [PyO3](https://pyo3.rs) and [maturin](https://www.maturin.rs).

It cuts the per call overhead of remotebmi to close to a bare TCP round trip,
see [benchmarks](../python/benchmarks/README.md).

## What it does

- `RustServer` parses HTTP/1.1, handles CORS and zstd content encoding,
  and calls `remotebmi.server.lean.Dispatcher` (Python) to call the BMI model.
  So it serves exactly the same API as the Python servers,
  which is tested in `python/tests/test_lean_conformance.py` against the connexion server.
- `RustTransport` sends requests for `remotebmi.client.lean.LeanBmiClient(..., transport="rust")`.

Design choices for low latency:

- One thread per connection with blocking IO, a BMI server has very few connections.
- Connection threads stay attached to the Python interpreter and only release the GIL
  around IO, compression and waiting for another connection to finish its model call.
- Request and response bodies are not copied between Rust and Python:
  request bodies are exposed with the buffer protocol (`Body`),
  response bodies are read from the Python buffer.
- Model methods are called one at a time.

## Install

Requires a [Rust toolchain](https://rustup.rs).

```shell
pip install ./rust
# or, for development, in an environment with remotebmi installed
pip install maturin
cd rust && maturin develop --release
```

## Usage

```shell
BMI_MODULE=mypackage BMI_CLASS=MyModel BMI_SERVER_BACKEND=rust run-lean-bmi-server
```

```python
from remotebmi.client.lean import LeanBmiClient
from remotebmi.server.rust import start_rust_server

with start_rust_server(MyModel(), port=50051, cors_origins=["*"]) as server:
    model = LeanBmiClient(f"http://localhost:{server.port}", transport="rust")
    model.initialize("config.yml")
```

The Rust transport only supports plain `http` URLs.

## Development

```shell
cargo fmt --check
cargo clippy --release
cargo test --release
maturin develop --release && pytest ../python/tests
```
