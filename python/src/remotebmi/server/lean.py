"""Lean BMI server, a plain ASGI app without web framework or schema validation.

Serves the same API as the connexion based server in :mod:`remotebmi.server`,
which is described by openapi.yaml and used as reference in the tests,
but with much less overhead per request.

The :class:`Dispatcher` maps a request to a model call and is also used by the
Rust server in the `remotebmi_rs` package.
"""

import json
from collections.abc import Awaitable, Callable, MutableMapping, Sequence
from os import environ
from traceback import format_exception
from typing import Any

import numpy as np
from bmipy import Bmi

from remotebmi._http import (
    JSON,
    OCTET_STREAM,
    PROBLEM_JSON,
    CorsPolicy,
    accepts_zstd,
    prefers_octet_stream,
    wire_dtype,
    zstd,
)
from remotebmi.reserve import (
    reserve_grid_edge_nodes,
    reserve_grid_face_,
    reserve_grid_nodes,
    reserve_grid_nodes_per_face,
    reserve_grid_padding,
    reserve_grid_shape,
    reserve_values,
    reserve_values_at_indices,
)

Body = bytes | bytearray | memoryview
Response = tuple[int, str, Body, str]
"""Status code, content type, body and allowed methods (only set for 405)."""

ROUTES: dict[str, tuple[str, str | None]] = {
    "initialize": ("POST", None),
    "update": ("POST", None),
    "update_until": ("POST", None),
    "finalize": ("DELETE", None),
    "get_component_name": ("GET", None),
    "get_input_item_count": ("GET", None),
    "get_input_var_names": ("GET", None),
    "get_output_item_count": ("GET", None),
    "get_output_var_names": ("GET", None),
    "get_var_grid": ("GET", "name"),
    "get_var_itemsize": ("GET", "name"),
    "get_var_location": ("GET", "name"),
    "get_var_nbytes": ("GET", "name"),
    "get_var_type": ("GET", "name"),
    "get_var_units": ("GET", "name"),
    "get_current_time": ("GET", None),
    "get_end_time": ("GET", None),
    "get_start_time": ("GET", None),
    "get_time_step": ("GET", None),
    "get_time_units": ("GET", None),
    "get_value": ("GET", "name"),
    "get_value_at_indices": ("POST", "name"),
    "set_value": ("POST", "name"),
    "set_value_at_indices": ("POST", "name"),
    "get_grid_rank": ("GET", "grid"),
    "get_grid_type": ("GET", "grid"),
    "get_grid_size": ("GET", "grid"),
    "get_grid_origin": ("GET", "grid"),
    "get_grid_shape": ("GET", "grid"),
    "get_grid_spacing": ("GET", "grid"),
    "get_grid_x": ("GET", "grid"),
    "get_grid_y": ("GET", "grid"),
    "get_grid_z": ("GET", "grid"),
    "get_grid_edge_count": ("GET", "grid"),
    "get_grid_edge_nodes": ("GET", "grid"),
    "get_grid_face_count": ("GET", "grid"),
    "get_grid_face_edges": ("GET", "grid"),
    "get_grid_face_nodes": ("GET", "grid"),
    "get_grid_node_count": ("GET", "grid"),
    "get_grid_nodes_per_face": ("GET", "grid"),
}
"""Operation (first path segment) to HTTP method and name of path parameter."""

_NO_CONTENT: Response = (204, "", b"", "")
_CREATED: Response = (201, "", b"", "")


def _problem(status: int, title: str, detail: str, **ext: Any) -> Response:
    body = {"type": "about:blank", "title": title, "detail": detail, "status": status}
    body.update(ext)
    return status, PROBLEM_JSON, json.dumps(body).encode(), ""


_NOT_FOUND = _problem(404, "Not Found", "Not Found")
_ALLOWED = {"GET": "GET, HEAD", "POST": "POST", "DELETE": "DELETE"}
_NOT_ALLOWED = {
    method: (*_problem(405, "Method Not Allowed", "Method Not Allowed")[:3], allow)
    for method, allow in _ALLOWED.items()
}


class BadRequestError(Exception):
    """Request does not conform to openapi.yaml."""

    def __init__(self, detail: str, status: int = 400, title: str = "Bad Request"):
        super().__init__(detail)
        self.status = status
        self.title = title


def _json(value: object) -> Response:
    return 200, JSON, json.dumps(value).encode(), ""


def _media_type(content_type: str) -> str:
    return content_type.partition(";")[0].strip().lower()


def _json_body(body: Body, content_type: str, expected: tuple[str, ...]) -> Any:
    if not body:
        msg = "RequestBody is required"
        raise BadRequestError(msg)
    media_type = _media_type(content_type)
    if media_type != JSON:
        msg = f"Invalid Content-type ({media_type}), expected {list(expected)}"
        raise BadRequestError(msg, 415, "Unsupported Media Type")
    try:
        return json.loads(body if isinstance(body, bytes | bytearray) else bytes(body))
    except ValueError as e:
        raise BadRequestError(str(e)) from e


def _numbers(value: object, what: str) -> np.ndarray:
    if not isinstance(value, list) or not value:
        msg = f"{what} should be a non-empty array of numbers"
        raise BadRequestError(msg)
    items = np.array(value)
    if items.ndim != 1 or items.dtype.kind not in "iuf":
        msg = f"{what} should be a non-empty array of numbers"
        raise BadRequestError(msg)
    return items


def _indices(value: object, what: str) -> np.ndarray:
    if not isinstance(value, list) or not value:
        msg = f"{what} should be a non-empty array of integers"
        raise BadRequestError(msg)
    items = np.array(value)
    if items.ndim != 1 or items.dtype.kind not in "iu" or (items < 0).any():
        msg = f"{what} should be a non-empty array of non-negative integers"
        raise BadRequestError(msg)
    return items.astype(np.int64, copy=False)


def _is_int(text: str) -> bool:
    digits = text[1:] if text[:1] == "-" else text
    return digits.isascii() and digits.isdecimal()


def model_error(exc: Exception) -> Response:
    """Response for an exception raised by the model, same as connexion server."""
    exc_class = exc.__class__.__name__
    return _problem(
        500,
        f"Model raised {exc_class}",
        str(exc),
        type=exc_class,
        traceback=format_exception(exc),
    )


class Dispatcher:
    """Calls the model method for a request and makes the response.

    Args:
        model: The model to call.
    """

    def __init__(self, model: Bmi):
        self.model = model
        self._routes = {
            operation: (method, param, getattr(self, operation))
            for operation, (method, param) in ROUTES.items()
        }

    def __call__(
        self, method: str, path: str, accept: str, content_type: str, body: Body
    ) -> Response:
        """Handle request.

        Args:
            method: HTTP method.
            path: Percent-decoded path of the request without query string.
            accept: Value of Accept header or empty string.
            content_type: Value of Content-Type header or empty string.
            body: Request body, already decoded if it had a Content-Encoding.
        """
        operation, _, arg = path[1:].partition("/")
        route = self._routes.get(operation)
        if route is None:
            return _NOT_FOUND
        route_method, param, handler = route
        if param is None:
            # connexion redirects to path without trailing slash
            if arg:
                return _NOT_FOUND
        elif not arg or "/" in arg or (param == "grid" and not _is_int(arg)):
            return _NOT_FOUND
        if method != route_method and (method != "HEAD" or route_method != "GET"):
            return _NOT_ALLOWED[route_method]
        try:
            if param is None:
                return handler(accept, content_type, body)  # type: ignore[no-any-return]
            if param == "grid":
                return handler(int(arg), accept, content_type, body)  # type: ignore[no-any-return]
            return handler(arg, accept, content_type, body)  # type: ignore[no-any-return]
        except BadRequestError as e:
            return _problem(e.status, e.title, str(e))
        except Exception as e:  # noqa: BLE001 any model error should be reported to client
            return model_error(e)

    # Handlers below have the same name as the BMI method and operationId in openapi.yaml,
    # arguments are the path parameter (if any), Accept, Content-Type and body.

    def initialize(self, _accept: str, content_type: str, body: Body) -> Response:
        request = _json_body(body, content_type, (JSON,))
        if (
            not isinstance(request, dict)
            or request.keys() != {"config_file"}
            or not isinstance(request["config_file"], str)
        ):
            msg = "Request body should be object with only config_file string property"
            raise BadRequestError(msg)
        self.model.initialize(request["config_file"])
        return _CREATED

    def update(self, *_: object) -> Response:
        self.model.update()
        return _NO_CONTENT

    def update_until(self, _accept: str, content_type: str, body: Body) -> Response:
        until = _json_body(body, content_type, (JSON,))
        if not isinstance(until, int | float) or isinstance(until, bool):
            msg = f"{until!r} is not of type 'number'"
            raise BadRequestError(msg)
        self.model.update_until(until)
        return _NO_CONTENT

    def finalize(self, *_: object) -> Response:
        self.model.finalize()
        return _NO_CONTENT

    def get_component_name(self, *_: object) -> Response:
        return _json({"name": str(self.model.get_component_name())})

    def get_input_item_count(self, *_: object) -> Response:
        return _json(int(self.model.get_input_item_count()))

    def get_input_var_names(self, *_: object) -> Response:
        return _json([str(n) for n in self.model.get_input_var_names()])

    def get_output_item_count(self, *_: object) -> Response:
        return _json(int(self.model.get_output_item_count()))

    def get_output_var_names(self, *_: object) -> Response:
        return _json([str(n) for n in self.model.get_output_var_names()])

    def get_var_grid(self, name: str, *_: object) -> Response:
        return _json(int(self.model.get_var_grid(name)))

    def get_var_itemsize(self, name: str, *_: object) -> Response:
        return _json(int(self.model.get_var_itemsize(name)))

    def get_var_location(self, name: str, *_: object) -> Response:
        return _json({"location": str(self.model.get_var_location(name))})

    def get_var_nbytes(self, name: str, *_: object) -> Response:
        return _json(int(self.model.get_var_nbytes(name)))

    def get_var_type(self, name: str, *_: object) -> Response:
        return _json({"type": str(self.model.get_var_type(name))})

    def get_var_units(self, name: str, *_: object) -> Response:
        return _json({"units": str(self.model.get_var_units(name))})

    def get_current_time(self, *_: object) -> Response:
        return _json(float(self.model.get_current_time()))

    def get_end_time(self, *_: object) -> Response:
        return _json(float(self.model.get_end_time()))

    def get_start_time(self, *_: object) -> Response:
        return _json(float(self.model.get_start_time()))

    def get_time_step(self, *_: object) -> Response:
        return _json(float(self.model.get_time_step()))

    def get_time_units(self, *_: object) -> Response:
        return _json({"units": str(self.model.get_time_units())})

    def get_value(self, name: str, accept: str, *_: object) -> Response:
        dest = reserve_values(self.model, name)
        values = self.model.get_value(name, dest)
        if not prefers_octet_stream(accept):
            return _json(values.tolist())
        if values is not dest:
            # Model could return its own array, which it could change before
            # the response is sent.
            np.copyto(dest, values, casting="unsafe")
        if dest.dtype.byteorder == ">":
            dest = dest.astype(dest.dtype.newbyteorder("<"))
        return 200, OCTET_STREAM, memoryview(dest).cast("B"), ""

    def get_value_at_indices(
        self, name: str, _accept: str, content_type: str, body: Body
    ) -> Response:
        indices = _indices(_json_body(body, content_type, (JSON,)), "Request body")
        dest = reserve_values_at_indices(self.model, name, indices)
        return _json(self.model.get_value_at_indices(name, dest, indices).tolist())

    def set_value(
        self, name: str, _accept: str, content_type: str, body: Body
    ) -> Response:
        if _media_type(content_type) == OCTET_STREAM:
            if not body:
                msg = "Request body must not be empty"
                raise BadRequestError(msg)
            dtype = wire_dtype(self.model.get_var_type(name))
            if len(body) % dtype.itemsize:
                msg = f"Body length {len(body)} is not a multiple of item size {dtype.itemsize} of {dtype}"
                raise BadRequestError(msg)
            # Copy so model gets writable array in native byte order
            items = np.frombuffer(body, dtype=dtype).astype(dtype.newbyteorder("="))
        else:
            expected = (JSON, OCTET_STREAM)
            items = _numbers(_json_body(body, content_type, expected), "Request body")
        self.model.set_value(name, items)
        return _NO_CONTENT

    def set_value_at_indices(
        self, name: str, _accept: str, content_type: str, body: Body
    ) -> Response:
        request = _json_body(body, content_type, (JSON,))
        if not isinstance(request, dict) or request.keys() != {"indices", "values"}:
            msg = (
                "Request body should be object with only indices and values properties"
            )
            raise BadRequestError(msg)
        indices = _indices(request["indices"], "indices")
        values = _numbers(request["values"], "values")
        self.model.set_value_at_indices(name, indices, values)
        return _NO_CONTENT

    def get_grid_rank(self, grid: int, *_: object) -> Response:
        return _json(int(self.model.get_grid_rank(grid)))

    def get_grid_type(self, grid: int, *_: object) -> Response:
        return _json({"type": str(self.model.get_grid_type(grid))})

    def get_grid_size(self, grid: int, *_: object) -> Response:
        return _json(int(self.model.get_grid_size(grid)))

    def get_grid_origin(self, grid: int, *_: object) -> Response:
        origin = reserve_grid_padding(self.model, grid)
        return _json(self.model.get_grid_origin(grid, origin).tolist())

    def get_grid_shape(self, grid: int, *_: object) -> Response:
        shape = reserve_grid_shape(self.model, grid)
        return _json(self.model.get_grid_shape(grid, shape).tolist())

    def get_grid_spacing(self, grid: int, *_: object) -> Response:
        spacing = reserve_grid_padding(self.model, grid)
        return _json(self.model.get_grid_spacing(grid, spacing).tolist())

    def get_grid_x(self, grid: int, *_: object) -> Response:
        x = reserve_grid_nodes(self.model, grid, 0)
        return _json(self.model.get_grid_x(grid, x).tolist())

    def get_grid_y(self, grid: int, *_: object) -> Response:
        y = reserve_grid_nodes(self.model, grid, 1)
        return _json(self.model.get_grid_y(grid, y).tolist())

    def get_grid_z(self, grid: int, *_: object) -> Response:
        z = reserve_grid_nodes(self.model, grid, 2)
        return _json(self.model.get_grid_z(grid, z).tolist())

    def get_grid_edge_count(self, grid: int, *_: object) -> Response:
        return _json(int(self.model.get_grid_edge_count(grid)))

    def get_grid_edge_nodes(self, grid: int, *_: object) -> Response:
        edge_nodes = reserve_grid_edge_nodes(self.model, grid)
        return _json(self.model.get_grid_edge_nodes(grid, edge_nodes).tolist())

    def get_grid_face_count(self, grid: int, *_: object) -> Response:
        return _json(int(self.model.get_grid_face_count(grid)))

    def get_grid_face_edges(self, grid: int, *_: object) -> Response:
        face_edges = reserve_grid_face_(self.model, grid)
        return _json(self.model.get_grid_face_edges(grid, face_edges).tolist())

    def get_grid_face_nodes(self, grid: int, *_: object) -> Response:
        face_nodes = reserve_grid_face_(self.model, grid)
        return _json(self.model.get_grid_face_nodes(grid, face_nodes).tolist())

    def get_grid_node_count(self, grid: int, *_: object) -> Response:
        return _json(int(self.model.get_grid_node_count(grid)))

    def get_grid_nodes_per_face(self, grid: int, *_: object) -> Response:
        nodes_per_face = reserve_grid_nodes_per_face(self.model, grid)
        return _json(self.model.get_grid_nodes_per_face(grid, nodes_per_face).tolist())


Scope = MutableMapping[str, Any]
Message = MutableMapping[str, Any]
Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]

_ADVERTISE_ZSTD = [(b"accept-encoding", b"zstd")] if zstd is not None else []


class LeanApp:
    """ASGI app serving a BMI model.

    Model methods are called in the event loop, so one at a time.

    Args:
        model: The model to serve.
        cors_origins: Origins allowed to call the server from a browser,
            `["*"]` for any origin. Default is no CORS headers.
        compression_level: zstd level used to compress responses
            when client accepts it and zstd is available.
        min_compress_size: Responses with fewer bytes are not compressed.
    """

    def __init__(
        self,
        model: Bmi,
        cors_origins: Sequence[str] | None = None,
        compression_level: int = 1,
        min_compress_size: int = 1024,
    ):
        self.dispatch = Dispatcher(model)
        self.cors = CorsPolicy(cors_origins) if cors_origins else None
        self.compression_level = compression_level
        self.min_compress_size = min_compress_size

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            await self._http(scope, receive, send)
        elif scope["type"] == "lifespan":
            while True:
                message = await receive()
                if message["type"] == "lifespan.startup":
                    await send({"type": "lifespan.startup.complete"})
                elif message["type"] == "lifespan.shutdown":
                    await send({"type": "lifespan.shutdown.complete"})
                    return

    async def _http(self, scope: Scope, receive: Receive, send: Send) -> None:
        headers = dict(scope["headers"])
        method = scope["method"]
        origin = _header(headers, b"origin")
        preflight_method = _header(headers, b"access-control-request-method")
        if (
            self.cors is not None
            and method == "OPTIONS"
            and origin is not None
            and preflight_method is not None
        ):
            status, cors_headers, text = self.cors.preflight(
                origin,
                preflight_method,
                _header(headers, b"access-control-request-headers"),
            )
            cors_headers.append((b"content-type", b"text/plain; charset=utf-8"))
            await _send_response(send, status, cors_headers, text)
            return

        try:
            body = _decode_body(
                await _read_body(receive), _header(headers, b"content-encoding") or ""
            )
        except BadRequestError as e:
            status, ctype, error, _ = _problem(e.status, e.title, str(e))
            await self._respond(send, method, status, ctype, error, "", origin, "")
            return
        status, ctype, response, allow = self.dispatch(
            method,
            scope["path"],
            _header(headers, b"accept") or "",
            _header(headers, b"content-type") or "",
            body,
        )
        accept_encoding = _header(headers, b"accept-encoding") or ""
        await self._respond(
            send, method, status, ctype, response, allow, origin, accept_encoding
        )

    async def _respond(
        self,
        send: Send,
        method: str,
        status: int,
        content_type: str,
        body: Body,
        allow: str,
        origin: str | None,
        accept_encoding: str,
    ) -> None:
        headers = list(_ADVERTISE_ZSTD)
        if content_type:
            headers.append((b"content-type", content_type.encode()))
        if allow:
            headers.append((b"allow", allow.encode()))
        if (
            zstd is not None
            and len(body) >= self.min_compress_size
            and accept_encoding
            and accepts_zstd(accept_encoding)
        ):
            body = zstd.compress(body, self.compression_level)
            headers.append((b"content-encoding", b"zstd"))
            headers.append((b"vary", b"Accept-Encoding"))
        if self.cors is not None:
            headers.extend(self.cors.headers(origin))
        await _send_response(send, status, headers, body, head=method == "HEAD")


def _header(headers: dict[bytes, bytes], name: bytes) -> str | None:
    value = headers.get(name)
    return None if value is None else value.decode("latin-1")


async def _read_body(receive: Receive) -> bytes:
    message = await receive()
    body: bytes = message.get("body", b"")
    if not message.get("more_body", False):
        return body
    chunks = [body]
    while message.get("more_body", False):
        message = await receive()
        chunks.append(message.get("body", b""))
    return b"".join(chunks)


def _decode_body(body: bytes, content_encoding: str) -> Body:
    content_encoding = content_encoding.strip().lower()
    if not content_encoding or content_encoding == "identity":
        return body
    if content_encoding == "zstd" and zstd is not None:
        try:
            return zstd.decompress(body)  # type: ignore[no-any-return]
        except zstd.ZstdError as e:
            raise BadRequestError(str(e)) from e
    detail = f"Unsupported Content-Encoding ({content_encoding})"
    raise BadRequestError(detail, 415, "Unsupported Media Type")


async def _send_response(
    send: Send,
    status: int,
    headers: list[tuple[bytes, bytes]],
    body: Body,
    head: bool = False,
) -> None:
    if status != 204:
        headers.append((b"content-length", str(len(body)).encode()))
    await send({"type": "http.response.start", "status": status, "headers": headers})
    await send({"type": "http.response.body", "body": b"" if head else bytes(body)})


def make_lean_app(
    model: Bmi,
    cors_origins: Sequence[str] | None = None,
    compression_level: int = 1,
    min_compress_size: int = 1024,
) -> LeanApp:
    """Make ASGI app that serves the model with low overhead.

    Args:
        model: The model to serve.
        cors_origins: Origins allowed to call the server from a browser,
            `["*"]` for any origin. Default is no CORS headers.
        compression_level: zstd level used to compress responses
            when client accepts it and zstd is available.
        min_compress_size: Responses with fewer bytes are not compressed.
    """
    return LeanApp(model, cors_origins, compression_level, min_compress_size)


def main(**kwargs):  # type: ignore[no-untyped-def]
    """Serve model from environment variables with lean server.

    Uses same environment variables as `run-bmi-server`.
    If BMI_SERVER_BACKEND environment variable is `rust` then the Rust server from
    the remotebmi_rs package is used instead of uvicorn.
    """
    from remotebmi.server import cors_origins_from_env  # noqa: PLC0415
    from remotebmi.server.build import from_env  # noqa: PLC0415

    model = from_env()
    port = int(environ.get("BMI_PORT", "50051"))
    host = kwargs.pop("host", "127.0.0.1")
    cors_origins = cors_origins_from_env()
    if environ.get("BMI_SERVER_BACKEND", "uvicorn") == "rust":
        from remotebmi.server.rust import serve_rust  # noqa: PLC0415

        serve_rust(model, host=host, port=port, cors_origins=cors_origins)
        return

    import uvicorn  # noqa: PLC0415

    app = make_lean_app(model, cors_origins=cors_origins)
    uvicorn.run(app, host=host, port=port, **kwargs)


if __name__ == "__main__":
    main()
