"""Lean BMI client with low overhead per call.

Uses http.client from the standard library (or the Rust transport from the
`remotebmi_rs` package) instead of httpx, transfers values of
get_value and set_value as raw bytes and caches variable types.
"""

import json
import select
from collections.abc import Mapping
from http.client import HTTPConnection, HTTPException, HTTPSConnection
from typing import Any, Protocol
from urllib.parse import quote, urlsplit

import numpy as np
from bmipy import Bmi
from numpy import ndarray

from remotebmi._http import JSON, OCTET_STREAM, wire_dtype, zstd

from .utils import validate_url

TransportResponse = tuple[int, str, str, str, Any]
"""Status code, Content-Type, Content-Encoding and Accept-Encoding headers
(empty string when absent) and the body as bytes-like object."""


class Transport(Protocol):
    """Sends a HTTP request and returns the response."""

    def request(
        self,
        method: str,
        path: str,
        body: Any,
        headers: Mapping[str, str],
    ) -> TransportResponse:
        """Send request.

        Args:
            method: HTTP method.
            path: Path including leading slash, already percent-encoded.
            body: Bytes-like object or None.
            headers: Extra request headers.
        """
        ...

    def close(self) -> None: ...


class HttpClientTransport:
    """Transport using http.client from the standard library.

    Args:
        base_url: Where the remote BMI server is running.
        timeout: How long a response can take in seconds.
        keep_alive: Reuse connection between requests.
    """

    def __init__(self, base_url: str, timeout: float | None, keep_alive: bool = True):
        url = urlsplit(base_url)
        connection_class = HTTPSConnection if url.scheme == "https" else HTTPConnection
        self.connection = connection_class(
            url.hostname or "", url.port, timeout=timeout
        )
        self.prefix = url.path.rstrip("/")
        self.keep_alive = keep_alive

    def request(
        self, method: str, path: str, body: Any, headers: Mapping[str, str]
    ) -> TransportResponse:
        connection = self.connection
        sock = connection.sock
        if sock is not None and select.select((sock,), (), (), 0)[0]:
            # An idle connection is only readable if the server closed it,
            # so reconnect instead of sending a request that will fail.
            connection.close()
        if not self.keep_alive:
            headers = {**headers, "Connection": "close"}
        try:
            connection.request(method, self.prefix + path, body, dict(headers))
            response = connection.getresponse()
            data = response.read()
        except (OSError, HTTPException):
            connection.close()
            raise
        if not self.keep_alive or response.will_close:
            connection.close()
        get = response.headers.get
        return (
            response.status,
            get("content-type", ""),
            get("content-encoding", ""),
            get("accept-encoding", ""),
            data,
        )

    def close(self) -> None:
        self.connection.close()


def rust_transport(
    base_url: str, timeout: float | None, keep_alive: bool = True
) -> Transport:
    """Transport implemented in Rust, from the optional remotebmi_rs package."""
    from remotebmi_rs import RustTransport  # noqa: PLC0415

    url = urlsplit(base_url)
    if url.scheme != "http":
        msg = "Rust transport only supports http"
        raise ValueError(msg)
    transport: Transport = RustTransport(
        url.hostname or "", url.port or 80, url.path.rstrip("/"), timeout, keep_alive
    )
    return transport


class RemoteBmiError(Exception):
    """Server responded with an error.

    Attributes:
        status: HTTP status code.
        problem: Problem details from response body.
        remote_traceback: Traceback of exception raised by the model on the server.
    """

    def __init__(self, status: int, problem: dict[str, Any]):
        self.status = status
        self.problem = problem
        self.remote_traceback = "".join(problem.get("traceback", []))
        title = problem.get("title", "")
        detail = problem.get("detail", "")
        super().__init__(
            f"{status} {title}: {detail}" if detail else f"{status} {title}"
        )

    @classmethod
    def from_response(cls, status: int, body: Any) -> "RemoteBmiError":
        try:
            problem = json.loads(bytes(body))
        except ValueError:
            problem = None
        if not isinstance(problem, dict):
            problem = {"title": bytes(body).decode("utf-8", "replace")}
        return cls(status, problem)


_NO_HEADERS: dict[str, str] = {}
_JSON_BODY = {"Content-Type": JSON}
_OCTET_BODY = {"Content-Type": OCTET_STREAM}
_ACCEPT_OCTET = f"{OCTET_STREAM}, {JSON};q=0.5"


class LeanBmiClient(Bmi):
    """BMI client with low overhead per call.

    Drop-in replacement for :class:`remotebmi.RemoteBmiClient`,
    except that :meth:`get_var_type` returns numpy type names and
    errors raise :class:`RemoteBmiError` instead of httpx.HTTPStatusError.

    Args:
        base_url: Where the remote BMI server is running.
        timeout: How long a response can take in seconds.
            Defaults to 1 day. Set to None to disable timeout.
        keep_alive: Reuse the connection between calls.
            Disable for the R server implementation.
        binary_values: Transfer values of get_value and set_value as raw bytes
            (application/octet-stream) instead of JSON.
            Falls back to JSON for servers that do not support raw bytes.
        compress: Ask server to compress responses with zstd and compress
            set_value request bodies when the server accepts zstd.
            Only pays off on slow networks or compressible data.
        min_compress_size: Request bodies with fewer bytes are not compressed.
        compression_level: zstd level used to compress request bodies.
        transport: How to send requests. `"python"` uses http.client,
            `"rust"` uses the remotebmi_rs package. Or a :class:`Transport` object.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float | None = 60 * 60 * 24,
        keep_alive: bool = True,
        binary_values: bool = True,
        compress: bool = False,
        min_compress_size: int = 1024,
        compression_level: int = 1,
        transport: str | Transport = "python",
    ):
        validate_url(base_url)
        if compress and zstd is None:
            msg = "compress=True requires Python >= 3.14 or backports.zstd package"
            raise ImportError(msg)
        if transport == "python":
            self.transport: Transport = HttpClientTransport(
                base_url, timeout, keep_alive
            )
        elif transport == "rust":
            self.transport = rust_transport(base_url, timeout, keep_alive)
        elif isinstance(transport, str):
            msg = f"Unknown transport {transport!r}, expected 'python' or 'rust'"
            raise ValueError(msg)
        else:
            self.transport = transport
        self.binary_values = binary_values
        self._binary_set_value = binary_values
        self.compress = compress
        self.min_compress_size = min_compress_size
        self.compression_level = compression_level
        self._server_accepts_zstd = False
        self._paths: dict[tuple[str, str], str] = {}
        self._dtypes: dict[str, np.dtype] = {}
        self._get_value_headers = {"Accept": _ACCEPT_OCTET} if binary_values else {}
        if compress:
            self._get_value_headers["Accept-Encoding"] = "zstd"

    def __del__(self) -> None:
        if hasattr(self, "transport"):
            self.transport.close()

    def _path(self, operation: str, arg: str) -> str:
        key = (operation, arg)
        path = self._paths.get(key)
        if path is None:
            path = self._paths[key] = f"/{operation}/{quote(arg, safe='')}"
        return path

    def _request(
        self,
        method: str,
        path: str,
        body: Any = None,
        headers: Mapping[str, str] = _NO_HEADERS,
    ) -> tuple[str, Any]:
        """Send request, return content type and decoded body of successful response."""
        status, content_type, content_encoding, accept_encoding, data = (
            self.transport.request(method, path, body, headers)
        )
        if accept_encoding:
            self._server_accepts_zstd = "zstd" in accept_encoding.lower()
        if content_encoding and content_encoding.lower() != "identity":
            if content_encoding.lower() != "zstd" or zstd is None:
                msg = (
                    f"Can not decode response with Content-Encoding {content_encoding}"
                )
                raise ValueError(msg)
            data = zstd.decompress(data)
        if status >= 400:
            raise RemoteBmiError.from_response(status, data)
        return content_type, data

    def _get(self, path: str) -> Any:
        return json.loads(self._request("GET", path)[1])

    def _post_json(self, path: str, value: object) -> Any:
        return self._request("POST", path, json.dumps(value).encode(), _JSON_BODY)[1]

    def initialize(self, config_file: str) -> None:
        self._post_json("/initialize", {"config_file": config_file})

    def update(self) -> None:
        self._request("POST", "/update")

    def update_until(self, time: float) -> None:
        self._post_json("/update_until", float(time))

    def finalize(self) -> None:
        self._request("DELETE", "/finalize")

    def get_component_name(self) -> str:
        return str(self._get("/get_component_name")["name"])

    def get_input_item_count(self) -> int:
        return int(self._get("/get_input_item_count"))

    def get_output_item_count(self) -> int:
        return int(self._get("/get_output_item_count"))

    def get_input_var_names(self) -> tuple[str, ...]:  # type: ignore[override]
        return tuple(self._get("/get_input_var_names"))

    def get_output_var_names(self) -> tuple[str, ...]:  # type: ignore[override]
        return tuple(self._get("/get_output_var_names"))

    def get_var_grid(self, name: str) -> int:
        return int(self._get(self._path("get_var_grid", name)))

    def get_var_type(self, name: str) -> str:
        """Type of variable as numpy name, for example `float32` or `int64`."""
        return str(self._wire_dtype(name).newbyteorder("="))

    def _wire_dtype(self, name: str) -> np.dtype:
        dtype = self._dtypes.get(name)
        if dtype is None:
            var_type = self._get(self._path("get_var_type", name))["type"]
            # A variable does not change type, so cache it.
            dtype = self._dtypes[name] = wire_dtype(var_type)
        return dtype

    def get_var_units(self, name: str) -> str:
        return str(self._get(self._path("get_var_units", name))["units"])

    def get_var_itemsize(self, name: str) -> int:
        return int(self._get(self._path("get_var_itemsize", name)))

    def get_var_nbytes(self, name: str) -> int:
        return int(self._get(self._path("get_var_nbytes", name)))

    def get_var_location(self, name: str) -> str:
        return str(self._get(self._path("get_var_location", name))["location"])

    def get_current_time(self) -> float:
        return float(self._get("/get_current_time"))

    def get_start_time(self) -> float:
        return float(self._get("/get_start_time"))

    def get_end_time(self) -> float:
        return float(self._get("/get_end_time"))

    def get_time_units(self) -> str:
        return str(self._get("/get_time_units")["units"])

    def get_time_step(self) -> float:
        return float(self._get("/get_time_step"))

    def get_value(self, name: str, dest: ndarray) -> ndarray:
        path = self._path("get_value", name)
        content_type, data = self._request("GET", path, None, self._get_value_headers)
        if content_type.startswith(OCTET_STREAM):
            items = np.frombuffer(data, dtype=self._wire_dtype(name))
        else:
            items = np.array(json.loads(data))
        np.copyto(dest, items.reshape(dest.shape))
        return dest

    def get_value_ptr(self, name: str) -> ndarray:
        raise NotImplementedError

    def get_value_at_indices(self, name: str, dest: ndarray, inds: ndarray) -> ndarray:
        path = self._path("get_value_at_indices", name)
        items = np.array(json.loads(self._post_json(path, inds.tolist())))
        np.copyto(dest, items.reshape(dest.shape))
        return dest

    def set_value(self, name: str, src: ndarray) -> None:
        path = self._path("set_value", name)
        if self._binary_set_value:
            try:
                self._set_value_binary(path, name, src)
            except RemoteBmiError as e:
                if e.status not in (400, 415):
                    raise
                # Server, like R and Julia ones, does not accept raw bytes
                self._binary_set_value = False
            except TypeError:
                # Variable type has no numpy equivalent
                pass
            else:
                return
        self._post_json(path, np.asarray(src).ravel().tolist())

    def _set_value_binary(self, path: str, name: str, src: ndarray) -> None:
        items = np.ascontiguousarray(src, dtype=self._wire_dtype(name))
        body: Any = memoryview(items).cast("B")
        headers = _OCTET_BODY
        if (
            self.compress
            and self._server_accepts_zstd
            and len(body) >= self.min_compress_size
            and zstd is not None
        ):
            body = zstd.compress(body, self.compression_level)
            headers = {**_OCTET_BODY, "Content-Encoding": "zstd"}
        self._request("POST", path, body, headers)

    def set_value_at_indices(self, name: str, inds: ndarray, src: ndarray) -> None:
        path = self._path("set_value_at_indices", name)
        self._post_json(path, {"indices": inds.tolist(), "values": src.tolist()})

    def get_grid_rank(self, grid: int) -> int:
        return int(self._get(f"/get_grid_rank/{int(grid)}"))

    def get_grid_size(self, grid: int) -> int:
        return int(self._get(f"/get_grid_size/{int(grid)}"))

    def get_grid_type(self, grid: int) -> str:
        return str(self._get(f"/get_grid_type/{int(grid)}")["type"])

    def _get_array(self, operation: str, grid: int, dest: ndarray) -> ndarray:
        items = np.array(self._get(f"/{operation}/{int(grid)}"))
        np.copyto(dest, items.reshape(dest.shape))
        return dest

    def get_grid_shape(self, grid: int, shape: ndarray) -> ndarray:
        return self._get_array("get_grid_shape", grid, shape)

    def get_grid_spacing(self, grid: int, spacing: ndarray) -> ndarray:
        return self._get_array("get_grid_spacing", grid, spacing)

    def get_grid_origin(self, grid: int, origin: ndarray) -> ndarray:
        return self._get_array("get_grid_origin", grid, origin)

    def get_grid_x(self, grid: int, x: ndarray) -> ndarray:
        return self._get_array("get_grid_x", grid, x)

    def get_grid_y(self, grid: int, y: ndarray) -> ndarray:
        return self._get_array("get_grid_y", grid, y)

    def get_grid_z(self, grid: int, z: ndarray) -> ndarray:
        return self._get_array("get_grid_z", grid, z)

    def get_grid_node_count(self, grid: int) -> int:
        return int(self._get(f"/get_grid_node_count/{int(grid)}"))

    def get_grid_edge_count(self, grid: int) -> int:
        return int(self._get(f"/get_grid_edge_count/{int(grid)}"))

    def get_grid_face_count(self, grid: int) -> int:
        return int(self._get(f"/get_grid_face_count/{int(grid)}"))

    def get_grid_edge_nodes(self, grid: int, edge_nodes: ndarray) -> ndarray:
        return self._get_array("get_grid_edge_nodes", grid, edge_nodes)

    def get_grid_face_edges(self, grid: int, face_edges: ndarray) -> ndarray:
        return self._get_array("get_grid_face_edges", grid, face_edges)

    def get_grid_face_nodes(self, grid: int, face_nodes: ndarray) -> ndarray:
        return self._get_array("get_grid_face_nodes", grid, face_nodes)

    def get_grid_nodes_per_face(self, grid: int, nodes_per_face: ndarray) -> ndarray:
        return self._get_array("get_grid_nodes_per_face", grid, nodes_per_face)
