"""Helpers to run the different server implementations in tests."""

import contextlib
import importlib.util
import socket
import threading
import time
from collections.abc import Iterator, Mapping
from typing import Any

import pytest
import uvicorn
from bmipy import Bmi
from starlette.testclient import TestClient

from remotebmi.client.lean import TransportResponse
from remotebmi.server import make_app
from remotebmi.server.lean import make_lean_app

has_rust = importlib.util.find_spec("remotebmi_rs") is not None
requires_rust = pytest.mark.skipif(
    not has_rust, reason="remotebmi_rs not installed, see rust/README.md"
)


@contextlib.contextmanager
def uvicorn_server(app: Any, **config: Any) -> Iterator[str]:
    """Run ASGI app with uvicorn in a thread, yields base url."""
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, log_level="warning", **config))
    thread = threading.Thread(target=server.run, kwargs={"sockets": [sock]})
    thread.start()
    try:
        while not server.started:
            if not thread.is_alive():
                msg = "uvicorn server did not start"
                raise RuntimeError(msg)
            time.sleep(0.01)
        yield f"http://127.0.0.1:{port}"
    finally:
        server.should_exit = True
        thread.join()
        sock.close()


@contextlib.contextmanager
def rust_server(model: Bmi, **kwargs: Any) -> Iterator[str]:
    """Run model with Rust server, yields base url."""
    from remotebmi.server.rust import start_rust_server  # noqa: PLC0415

    with start_rust_server(model, **kwargs) as server:
        yield f"http://127.0.0.1:{server.port}"


@contextlib.contextmanager
def serve(implementation: str, model: Bmi, **kwargs: Any) -> Iterator[str]:
    """Serve model over a socket with one of the server implementations."""
    if implementation == "connexion":
        with uvicorn_server(make_app(model, **kwargs)) as url:
            yield url
    elif implementation == "lean":
        with uvicorn_server(make_lean_app(model, **kwargs)) as url:
            yield url
    elif implementation == "rust":
        with rust_server(model, **kwargs) as url:
            yield url
    else:
        msg = f"Unknown implementation {implementation}"
        raise ValueError(msg)


class AsgiTransport:
    """Transport for LeanBmiClient that calls an ASGI app in-process."""

    def __init__(self, client: TestClient):
        self.client = client

    def request(
        self, method: str, path: str, body: Any, headers: Mapping[str, str]
    ) -> TransportResponse:
        content = None if body is None else bytes(body)
        request = self.client.build_request(
            method, path, content=content, headers=dict(headers)
        )
        response = self.client.send(request, stream=True)
        try:
            # Raw to leave decoding of Content-Encoding to client under test
            data = b"".join(response.iter_raw())
        finally:
            response.close()
        get = response.headers.get
        return (
            response.status_code,
            get("content-type", ""),
            get("content-encoding", ""),
            get("accept-encoding", ""),
            data,
        )

    def close(self) -> None:
        pass
