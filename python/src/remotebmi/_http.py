"""HTTP details of the BMI wire format shared by servers and clients."""

import contextlib
import importlib
import importlib.util
from collections.abc import Sequence
from functools import lru_cache
from types import ModuleType

import numpy as np

JSON = "application/json"
OCTET_STREAM = "application/octet-stream"
PROBLEM_JSON = "application/problem+json"


def _import_zstd() -> ModuleType | None:
    # compression.zstd is in standard library since Python 3.14,
    # for older Pythons the backports.zstd package provides the same API.
    for name in ("compression.zstd", "backports.zstd"):
        if importlib.util.find_spec(name.partition(".")[0]) is None:
            continue
        with contextlib.suppress(ImportError):
            return importlib.import_module(name)
    return None


zstd = _import_zstd()


def accept_quality(accept: str, media_type: str) -> float:
    """Quality the Accept header gives to media_type, the most specific range wins."""
    main_type = media_type.partition("/")[0]
    specificities = {media_type: 2, f"{main_type}/*": 1, "*/*": 0}
    best_specificity, best_quality = -1, 0.0
    for media_range in accept.split(","):
        range_type, *params = (p.strip() for p in media_range.split(";"))
        specificity = specificities.get(range_type.lower(), -1)
        if specificity < 0 or specificity < best_specificity:
            continue
        quality = 1.0
        for param in params:
            key, _, value = param.partition("=")
            if key.strip() == "q":
                try:
                    quality = float(value)
                except ValueError:
                    quality = 0.0
        best_specificity, best_quality = specificity, quality
    return best_quality


@lru_cache(maxsize=64)
def prefers_octet_stream(accept: str) -> bool:
    """Whether Accept header prefers raw bytes over JSON."""
    if not accept:
        return False
    octet_quality = accept_quality(accept, OCTET_STREAM)
    return octet_quality > 0 and octet_quality > accept_quality(accept, JSON)


@lru_cache(maxsize=64)
def accepts_zstd(accept_encoding: str) -> bool:
    """Whether Accept-Encoding header accepts zstd content coding."""
    for coding in accept_encoding.split(","):
        name, *params = (p.strip() for p in coding.split(";"))
        if name.lower() not in ("zstd", "*"):
            continue
        for param in params:
            key, _, value = param.partition("=")
            if key.strip() == "q":
                try:
                    return float(value) > 0
                except ValueError:
                    return False
        return True
    return False


def wire_dtype(var_type: str) -> np.dtype:
    """Little-endian dtype of items of a variable in an application/octet-stream body.

    Args:
        var_type: Type as returned by get_var_type.
            float and double as named in openapi spec, other names as numpy names them.
    """
    dtype = np.dtype(
        {"float": np.float32, "double": np.float64}.get(var_type, var_type)
    )
    little_endian: np.dtype = dtype.newbyteorder("<")
    return little_endian


CORS_METHODS = ("DELETE", "GET", "POST")
CORS_MAX_AGE = 600
_PREFLIGHT_VARY = (
    "Origin, Access-Control-Request-Method, Access-Control-Request-Headers, "
    "Access-Control-Request-Private-Network"
)


class CorsPolicy:
    """Which origins may call the server from a browser.

    Mirrors starlette.middleware.cors.CORSMiddleware as configured in
    remotebmi.server.make_app (all headers allowed, no credentials),
    so all servers answer the same.
    """

    def __init__(self, origins: Sequence[str]):
        self.allow_all = "*" in origins
        self.origins = frozenset(origins)

    def is_allowed(self, origin: str) -> bool:
        return self.allow_all or origin in self.origins

    def headers(self, origin: str | None) -> list[tuple[bytes, bytes]]:
        """Headers to add to a response of a non-preflight request."""
        if origin is not None and self.is_allowed(origin):
            allowed = "*" if self.allow_all else origin
            return [
                (b"access-control-allow-origin", allowed.encode("latin-1")),
                (b"vary", b"Origin"),
            ]
        return [(b"vary", b"Origin")]

    def preflight(
        self, origin: str, method: str, request_headers: str | None
    ) -> tuple[int, list[tuple[bytes, bytes]], bytes]:
        """Status, headers and body for a response to a preflight request."""
        headers = [(b"vary", _PREFLIGHT_VARY.encode())]
        failures = []
        if self.is_allowed(origin):
            allowed = "*" if self.allow_all else origin
            headers.append((b"access-control-allow-origin", allowed.encode("latin-1")))
        else:
            failures.append("origin")
        if method not in CORS_METHODS:
            failures.append("method")
        headers.append(
            (b"access-control-allow-methods", ", ".join(CORS_METHODS).encode())
        )
        headers.append((b"access-control-max-age", str(CORS_MAX_AGE).encode()))
        if request_headers is not None:
            headers.append(
                (b"access-control-allow-headers", request_headers.encode("latin-1"))
            )
        if failures:
            return 400, headers, ("Disallowed CORS " + ", ".join(failures)).encode()
        return 200, headers, b"OK"
