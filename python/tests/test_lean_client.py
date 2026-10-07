"""LeanBmiClient against every server implementation should behave like calling the model."""

# mypy: disable-error-code="no-untyped-def"

import contextlib
import time
from pathlib import Path

import numpy as np
import pytest
from starlette.testclient import TestClient

from remotebmi._http import zstd
from remotebmi.client.lean import LeanBmiClient, RemoteBmiError
from remotebmi.reserve import (
    reserve_grid_edge_nodes,
    reserve_grid_face_,
    reserve_grid_nodes,
    reserve_grid_nodes_per_face,
    reserve_grid_padding,
    reserve_grid_shape,
)
from remotebmi.server import make_app
from remotebmi.server.lean import make_lean_app

from .fake_models import (
    FailingModel,
    Float32Model,
    FullModel,
    Int32Model,
    Rect3DGridModel,
    SomeError,
    Structured3DQuadrilateralsGridModel,
    UniRectGridModel,
    UnstructuredGridBmiModel,
)
from .servers import (
    AsgiTransport,
    has_rust,
    requires_rust,
    rust_server,
    serve,
    uvicorn_server,
)

# Server implementation and client transport
COMBINATIONS = [
    ("connexion", "asgi"),
    ("lean", "asgi"),
    ("connexion", "python"),
    ("lean", "python"),
    pytest.param("lean", "rust", marks=requires_rust),
    pytest.param("rust", "python", marks=requires_rust),
    pytest.param("rust", "rust", marks=requires_rust),
]


@contextlib.contextmanager
def lean_client(server, transport, model, **kwargs):
    if transport == "asgi":
        app = make_app(model) if server == "connexion" else make_lean_app(model)
        with TestClient(app) as test_client:
            yield LeanBmiClient(
                "http://testserver", transport=AsgiTransport(test_client), **kwargs
            )
    else:
        with serve(server, model) as url:
            client = LeanBmiClient(url, transport=transport, **kwargs)
            try:
                yield client
            finally:
                client.transport.close()


def failing_model():
    return FailingModel(SomeError("boom"))


def safe(reserve, model, *args):
    """Destination array, or a dummy one when model can not tell its size."""
    try:
        return reserve(model, *args)
    except SomeError:
        return np.empty(3)


def bmi_calls(model):
    """Name and arguments of every BMI method (except get_value_ptr)."""
    yield "initialize", ("config.yml",)
    yield "update", ()
    yield "update_until", (5.0,)
    for name in (
        "get_component_name",
        "get_input_item_count",
        "get_output_item_count",
        "get_input_var_names",
        "get_output_var_names",
        "get_current_time",
        "get_start_time",
        "get_end_time",
        "get_time_step",
        "get_time_units",
    ):
        yield name, ()
    for name in (
        "get_var_grid",
        "get_var_type",
        "get_var_units",
        "get_var_itemsize",
        "get_var_nbytes",
        "get_var_location",
    ):
        yield name, ("somevar",)
    if isinstance(model, Float32Model):
        dtype = model.dtype
        yield "get_value", ("somevar", np.empty(3, dtype))
        yield "get_value_at_indices", ("somevar", np.empty(2, dtype), np.array([2, 0]))
        yield "set_value", ("somevar", np.array([7, 8, 9], dtype))
        yield "get_value", ("somevar", np.empty(3, dtype))
        yield "set_value_at_indices", ("somevar", np.array([1]), np.array([5], dtype))
        yield "get_value", ("somevar", np.empty(3, dtype))
    else:
        yield "get_value", ("somevar", np.empty(3))
        yield "set_value", ("somevar", np.ones(3))
    grid = 0
    for name in ("get_grid_rank", "get_grid_size", "get_grid_type"):
        yield name, (grid,)
    yield "get_grid_shape", (grid, safe(reserve_grid_shape, model, grid))
    yield "get_grid_spacing", (grid, safe(reserve_grid_padding, model, grid))
    yield "get_grid_origin", (grid, safe(reserve_grid_padding, model, grid))
    for dim, name in enumerate(("get_grid_x", "get_grid_y", "get_grid_z")):
        yield name, (grid, safe(reserve_grid_nodes, model, grid, dim))
    for name in ("get_grid_node_count", "get_grid_edge_count", "get_grid_face_count"):
        yield name, (grid,)
    yield "get_grid_edge_nodes", (grid, safe(reserve_grid_edge_nodes, model, grid))
    yield "get_grid_face_edges", (grid, safe(reserve_grid_face_, model, grid))
    yield "get_grid_face_nodes", (grid, safe(reserve_grid_face_, model, grid))
    yield (
        "get_grid_nodes_per_face",
        (grid, safe(reserve_grid_nodes_per_face, model, grid)),
    )
    yield "finalize", ()


def outcome(bmi, name, args):
    """Result of calling BMI method, comparable between direct and remote calls."""
    args = [a.copy() if isinstance(a, np.ndarray) else a for a in args]
    try:
        result = getattr(bmi, name)(*args)
    except RemoteBmiError as e:
        return "raised", e.problem["type"]
    except Exception as e:  # noqa: BLE001
        return "raised", type(e).__name__
    if name == "get_var_type":
        result = np.dtype(result)
    if isinstance(result, np.ndarray):
        result = (result.tolist(), result.dtype)
    if isinstance(result, tuple):
        result = list(result)
    dests = [(a.tolist(), a.dtype) for a in args if isinstance(a, np.ndarray)]
    return "returned", result, dests


MODELS = [
    FullModel,
    Int32Model,
    failing_model,
    Rect3DGridModel,
    UniRectGridModel,
    Structured3DQuadrilateralsGridModel,
    UnstructuredGridBmiModel,
]


@pytest.mark.parametrize(
    "options",
    [
        {},
        {"binary_values": False},
        pytest.param(
            {"compress": True, "min_compress_size": 0},
            marks=pytest.mark.skipif(zstd is None, reason="zstd not available"),
        ),
        {"keep_alive": False},
    ],
    ids=["binary", "json", "compressed", "no keep-alive"],
)
@pytest.mark.parametrize("model_factory", MODELS, ids=lambda m: m.__name__)
@pytest.mark.parametrize(("server", "transport"), COMBINATIONS)
def test_same_as_direct_call(server, transport, model_factory, options):
    direct_model = model_factory()
    served_model = model_factory()
    mismatches = []
    with lean_client(server, transport, served_model, **options) as client:
        for name, args in bmi_calls(direct_model):
            expected = outcome(direct_model, name, args)
            actual = outcome(client, name, args)
            if actual != expected:
                mismatches.append(f"{name}: {actual} != {expected}")

    assert mismatches == []
    if isinstance(direct_model, Float32Model):
        np.testing.assert_array_equal(served_model.value, direct_model.value)


@pytest.mark.parametrize(("server", "transport"), COMBINATIONS)
def test_remote_error(server, transport):
    with (
        lean_client(server, transport, failing_model()) as client,
        pytest.raises(
            RemoteBmiError, match="500 Model raised SomeError: boom"
        ) as excinfo,
    ):
        client.update()

    assert excinfo.value.status == 500
    assert "SomeError: boom" in excinfo.value.remote_traceback


@pytest.mark.skipif(zstd is None, reason="zstd not available")
@pytest.mark.parametrize(("server", "transport"), COMBINATIONS)
def test_large_compressed_values(server, transport):
    model = Float32Model()
    model.value = np.linspace(0, 1, 100_000, dtype=np.float32)
    values = np.linspace(1, 2, 100_000, dtype=np.float32)
    with lean_client(server, transport, model, compress=True) as client:
        client.set_value("somevar", values)
        dest = np.empty_like(values)
        client.get_value("somevar", dest)

    np.testing.assert_array_equal(dest, values)
    np.testing.assert_array_equal(model.value, values)


@pytest.mark.parametrize(
    "transport", ["python", pytest.param("rust", marks=requires_rust)]
)
def test_reconnect_after_server_closed_idle_connection(transport):
    model = FullModel()
    with uvicorn_server(make_lean_app(model), timeout_keep_alive=1) as url:
        client = LeanBmiClient(url, transport=transport)
        assert client.get_component_name() == "full"
        time.sleep(1.5)

        assert client.get_component_name() == "full"


@requires_rust
@pytest.mark.parametrize("transport", ["python", "rust"])
def test_reconnect_after_server_restart(transport):
    with rust_server(FullModel()) as url:
        client = LeanBmiClient(url, transport=transport)
        assert client.get_component_name() == "full"
    port = int(url.rpartition(":")[2])
    with rust_server(FullModel(), port=port):
        assert client.get_component_name() == "full"


def test_unknown_transport():
    with pytest.raises(ValueError, match="Unknown transport"):
        LeanBmiClient("http://localhost:50051", transport="carrier pigeon")


@pytest.mark.skipif(has_rust, reason="remotebmi_rs is installed")
def test_rust_transport_not_installed():
    with pytest.raises(ImportError):
        LeanBmiClient("http://localhost:50051", transport="rust")


def json_only(app):
    """ASGI app like servers that do not support raw bytes, such as R and Julia."""

    async def wrapper(scope, receive, send):
        if scope["type"] == "http":
            headers = dict(scope["headers"])
            if headers.get(b"content-type") == b"application/octet-stream":
                await send(
                    {"type": "http.response.start", "status": 415, "headers": []}
                )
                await send({"type": "http.response.body", "body": b""})
                return
            scope = {
                **scope,
                "headers": [(k, v) for k, v in scope["headers"] if k != b"accept"],
            }
        await app(scope, receive, send)

    return wrapper


def test_binary_values_fall_back_to_json():
    model = FullModel()
    with TestClient(json_only(make_lean_app(model))) as test_client:
        client = LeanBmiClient(
            "http://testserver", transport=AsgiTransport(test_client)
        )
        client.set_value("somevar", np.array([4, 5, 6], np.float32))
        dest = np.empty(3, np.float32)
        client.get_value("somevar", dest)

    np.testing.assert_array_equal(model.value, [4, 5, 6])
    np.testing.assert_array_equal(dest, [4, 5, 6])
    assert not client._binary_set_value


class UnknownTypeModel(FullModel):
    def get_var_type(self, name):
        return "real"


def test_set_value_of_unknown_type_falls_back_to_json():
    model = UnknownTypeModel()
    with TestClient(make_lean_app(model)) as test_client:
        client = LeanBmiClient(
            "http://testserver", transport=AsgiTransport(test_client)
        )
        client.set_value("somevar", np.array([4, 5, 6]))

    np.testing.assert_array_equal(model.value, [4, 5, 6])


@requires_rust
@pytest.mark.skipif(not Path("/proc/self/fd").exists(), reason="needs /proc")
def test_rust_server_closes_connections():
    def open_files():
        return len(list(Path("/proc/self/fd").iterdir()))

    with rust_server(FullModel()) as url:
        client = LeanBmiClient(url, keep_alive=False)
        client.get_component_name()
        before = open_files()
        for _ in range(100):
            client.get_component_name()
        time.sleep(0.1)  # let connection threads finish

        assert open_files() - before < 10
