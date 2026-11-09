"""Rust HTTP server and client transport for remotebmi."""

from collections.abc import Callable, Mapping
from types import TracebackType
from typing import Any, Self

Response = tuple[int, str, Any, str]

class Body:
    """Read-only bytes-like object owned by Rust, supports the buffer protocol."""

    def __len__(self) -> int: ...

class RustTransport:
    """Sends HTTP requests over one reused TCP connection."""

    def __init__(
        self,
        host: str,
        port: int,
        prefix: str = "",
        timeout: float | None = None,
        keep_alive: bool = True,
    ) -> None: ...
    def request(
        self,
        method: str,
        path: str,
        body: Any = None,
        headers: Mapping[str, str] | None = None,
    ) -> tuple[int, str, str, str, bytes | Body]: ...
    def close(self) -> None: ...

class RustServer:
    """HTTP server calling handler(method, path, accept, content_type, body)."""

    def __init__(
        self,
        handler: Callable[..., Response],
        host: str = "127.0.0.1",
        port: int = 0,
        cors_origins: list[str] | None = None,
        compression_level: int = 1,
        min_compress_size: int = 1024,
    ) -> None: ...
    @property
    def port(self) -> int: ...
    def stop(self) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None: ...
