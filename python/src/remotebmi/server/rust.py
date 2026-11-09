"""Serve a BMI model with the Rust HTTP server from the remotebmi_rs package.

The Rust server parses HTTP and handles CORS and compression,
:class:`remotebmi.server.lean.Dispatcher` calls the model.
"""

import time
from collections.abc import Sequence
from typing import Any

from bmipy import Bmi

from remotebmi.server.lean import Dispatcher


def start_rust_server(
    model: Bmi,
    host: str = "127.0.0.1",
    port: int = 0,
    cors_origins: Sequence[str] | None = None,
    compression_level: int = 1,
    min_compress_size: int = 1024,
) -> Any:
    """Start serving model in background threads.

    Args:
        model: The model to serve.
        host: Address to listen on.
        port: Port to listen on, 0 picks a free port.
        cors_origins: Origins allowed to call the server from a browser,
            `["*"]` for any origin. Default is no CORS headers.
        compression_level: zstd level used to compress responses
            when client accepts it.
        min_compress_size: Responses with fewer bytes are not compressed.

    Returns:
        A remotebmi_rs.RustServer, with port attribute and stop method.
    """
    from remotebmi_rs import RustServer  # noqa: PLC0415

    return RustServer(
        Dispatcher(model),
        host,
        port,
        list(cors_origins) if cors_origins else None,
        compression_level,
        min_compress_size,
    )


def serve_rust(
    model: Bmi,
    host: str = "127.0.0.1",
    port: int = 50051,
    cors_origins: Sequence[str] | None = None,
) -> None:
    """Serve model until interrupted."""
    server = start_rust_server(model, host, port, cors_origins)
    try:
        while True:
            time.sleep(3600)
    finally:
        server.stop()
