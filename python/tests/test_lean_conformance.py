"""Lean and Rust servers should respond like the connexion server, which follows openapi.yaml."""

# mypy: disable-error-code="no-untyped-def"

import contextlib
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import httpx
import numpy as np
import pytest
import yaml
from bmipy import Bmi
from starlette.testclient import TestClient

from remotebmi._http import zstd
from remotebmi.server import make_app
from remotebmi.server.lean import ROUTES, make_lean_app

from .fake_models import (
    FailingModel,
    FullModel,
    Int32Model,
    Rect3DGridModel,
    SomeError,
    UniRectGridModel,
    UnstructuredGridBmiModel,
)
from .servers import requires_rust, rust_server

SPEC = Path(__file__).parents[1] / "src" / "remotebmi" / "server" / "openapi.yaml"


def failing_model():
    return FailingModel(SomeError("boom"))


def octet(body):
    return {"content": body, "headers": {"content-type": "application/octet-stream"}}


GET_OCTET = {"headers": {"accept": "application/octet-stream"}}

# Each case is a model factory and a sequence of requests,
# responses are compared after each request.
Request = tuple[str, str, dict[str, Any]]
CASES: dict[str, tuple[Callable[[], Bmi], list[Request]]] = {
    "initialize": (
        FullModel,
        [("POST", "/initialize", {"json": {"config_file": "a"}})],
    ),
    "initialize extra prop": (
        FullModel,
        [("POST", "/initialize", {"json": {"config_file": "a", "x": 1}})],
    ),
    "initialize wrong type": (
        FullModel,
        [("POST", "/initialize", {"json": {"config_file": 1}})],
    ),
    "initialize invalid json": (
        FullModel,
        [
            (
                "POST",
                "/initialize",
                {"content": b"{bad", "headers": {"content-type": "application/json"}},
            )
        ],
    ),
    "initialize text": (
        FullModel,
        [
            (
                "POST",
                "/initialize",
                {"content": b"{}", "headers": {"content-type": "text/plain"}},
            )
        ],
    ),
    "initialize no body": (FullModel, [("POST", "/initialize", {})]),
    "update": (FullModel, [("POST", "/update", {}), ("GET", "/get_current_time", {})]),
    "update_until": (
        FullModel,
        [("POST", "/update_until", {"json": 5.5}), ("GET", "/get_current_time", {})],
    ),
    "update_until int": (FullModel, [("POST", "/update_until", {"json": 5})]),
    "update_until object": (
        FullModel,
        [("POST", "/update_until", {"json": {"until": 5}})],
    ),
    "update_until string": (FullModel, [("POST", "/update_until", {"json": "5"})]),
    "update_until no body": (FullModel, [("POST", "/update_until", {})]),
    "finalize": (FullModel, [("DELETE", "/finalize", {})]),
    "exchange items": (
        FullModel,
        [
            ("GET", "/get_component_name", {}),
            ("GET", "/get_input_item_count", {}),
            ("GET", "/get_input_var_names", {}),
            ("GET", "/get_output_item_count", {}),
            ("GET", "/get_output_var_names", {}),
        ],
    ),
    "time": (
        FullModel,
        [
            ("GET", "/get_current_time", {}),
            ("GET", "/get_end_time", {}),
            ("GET", "/get_start_time", {}),
            ("GET", "/get_time_step", {}),
            ("GET", "/get_time_units", {}),
        ],
    ),
    "var info": (
        FullModel,
        [
            ("GET", "/get_var_grid/somevar", {}),
            ("GET", "/get_var_itemsize/somevar", {}),
            ("GET", "/get_var_location/somevar", {}),
            ("GET", "/get_var_nbytes/somevar", {}),
            ("GET", "/get_var_type/somevar", {}),
            ("GET", "/get_var_units/somevar", {}),
        ],
    ),
    "var name with space": (FullModel, [("GET", "/get_var_units/some%20var", {})]),
    "var name with slash": (FullModel, [("GET", "/get_var_units/some%2Fvar", {})]),
    "var name empty": (FullModel, [("GET", "/get_var_units/", {})]),
    "get_value json": (FullModel, [("GET", "/get_value/somevar", {})]),
    "get_value octet": (FullModel, [("GET", "/get_value/somevar", GET_OCTET)]),
    "get_value octet int32": (Int32Model, [("GET", "/get_value/somevar", GET_OCTET)]),
    "get_value prefer json": (
        FullModel,
        [
            (
                "GET",
                "/get_value/somevar",
                {
                    "headers": {
                        "accept": "application/json, application/octet-stream;q=0.5"
                    }
                },
            )
        ],
    ),
    "get_value_at_indices": (
        FullModel,
        [("POST", "/get_value_at_indices/somevar", {"json": [2, 0]})],
    ),
    "get_value_at_indices empty": (
        FullModel,
        [("POST", "/get_value_at_indices/somevar", {"json": []})],
    ),
    "get_value_at_indices negative": (
        FullModel,
        [("POST", "/get_value_at_indices/somevar", {"json": [-1]})],
    ),
    "get_value_at_indices float": (
        FullModel,
        [("POST", "/get_value_at_indices/somevar", {"json": [1.5]})],
    ),
    "set_value json": (
        FullModel,
        [
            ("POST", "/set_value/somevar", {"json": [7, 8.5, 9]}),
            ("GET", "/get_value/somevar", {}),
        ],
    ),
    "set_value json empty": (FullModel, [("POST", "/set_value/somevar", {"json": []})]),
    "set_value json strings": (
        FullModel,
        [("POST", "/set_value/somevar", {"json": ["a"]})],
    ),
    "set_value json object": (
        FullModel,
        [("POST", "/set_value/somevar", {"json": {"a": 1}})],
    ),
    "set_value octet": (
        FullModel,
        [
            ("POST", "/set_value/somevar", octet(np.array([7, 8, 9], "<f4").tobytes())),
            ("GET", "/get_value/somevar", GET_OCTET),
        ],
    ),
    "set_value octet int32": (
        Int32Model,
        [
            ("POST", "/set_value/somevar", octet(np.array([7, 8, 9], "<i4").tobytes())),
            ("GET", "/get_value/somevar", {}),
        ],
    ),
    "set_value octet empty": (FullModel, [("POST", "/set_value/somevar", octet(b""))]),
    "set_value octet partial item": (
        FullModel,
        [("POST", "/set_value/somevar", octet(b"123"))],
    ),
    "set_value text": (
        FullModel,
        [
            (
                "POST",
                "/set_value/somevar",
                {"content": b"1", "headers": {"content-type": "text/plain"}},
            )
        ],
    ),
    "set_value_at_indices": (
        FullModel,
        [
            (
                "POST",
                "/set_value_at_indices/somevar",
                {"json": {"indices": [2], "values": [9]}},
            ),
            ("GET", "/get_value/somevar", {}),
        ],
    ),
    "set_value_at_indices missing values": (
        FullModel,
        [("POST", "/set_value_at_indices/somevar", {"json": {"indices": [2]}})],
    ),
    "set_value_at_indices negative": (
        FullModel,
        [
            (
                "POST",
                "/set_value_at_indices/somevar",
                {"json": {"indices": [-2], "values": [9]}},
            )
        ],
    ),
    "rectilinear grid": (
        Rect3DGridModel,
        [
            ("GET", "/get_grid_rank/0", {}),
            ("GET", "/get_grid_size/0", {}),
            ("GET", "/get_grid_type/0", {}),
            ("GET", "/get_grid_shape/0", {}),
            ("GET", "/get_grid_x/0", {}),
            ("GET", "/get_grid_y/0", {}),
            ("GET", "/get_grid_z/0", {}),
        ],
    ),
    "uniform rectilinear grid": (
        UniRectGridModel,
        [("GET", "/get_grid_origin/0", {}), ("GET", "/get_grid_spacing/0", {})],
    ),
    "unstructured grid": (
        UnstructuredGridBmiModel,
        [
            ("GET", "/get_grid_node_count/0", {}),
            ("GET", "/get_grid_edge_count/0", {}),
            ("GET", "/get_grid_face_count/0", {}),
            ("GET", "/get_grid_edge_nodes/0", {}),
            ("GET", "/get_grid_face_edges/0", {}),
            ("GET", "/get_grid_face_nodes/0", {}),
            ("GET", "/get_grid_nodes_per_face/0", {}),
        ],
    ),
    "grid not an integer": (Rect3DGridModel, [("GET", "/get_grid_rank/abc", {})]),
    "grid a float": (Rect3DGridModel, [("GET", "/get_grid_rank/1.5", {})]),
    "grid negative": (failing_model, [("GET", "/get_grid_rank/-1", {})]),
    "model error": (
        failing_model,
        [
            ("POST", "/update", {}),
            ("GET", "/get_current_time", {}),
            ("GET", "/get_value/somevar", {}),
            ("GET", "/get_grid_x/0", {}),
        ],
    ),
    "not found": (FullModel, [("GET", "/nonexisting", {}), ("GET", "/", {})]),
    "trailing slash": (FullModel, [("GET", "/get_current_time/", {})]),
    "method not allowed": (
        FullModel,
        [
            ("GET", "/update", {}),
            ("PUT", "/get_var_grid/somevar", {}),
            ("OPTIONS", "/get_var_grid/somevar", {}),
        ],
    ),
    "head": (FullModel, [("HEAD", "/get_current_time", {})]),
}


@contextlib.contextmanager
def http_client(implementation, model, **kwargs):
    if implementation == "connexion":
        with TestClient(make_app(model, **kwargs)) as client:
            yield client
    elif implementation == "lean":
        with TestClient(make_lean_app(model, **kwargs)) as client:
            yield client
    else:
        with rust_server(model, **kwargs) as url, httpx.Client(base_url=url) as client:
            yield client


def normalize(response):
    """Parts of response that should be same for all implementations."""
    content_type = response.headers.get("content-type", "") if response.content else ""
    body = response.content
    if content_type.endswith("json") and body:
        body = json.loads(body)
        if isinstance(body, dict):
            body.pop("traceback", None)
            if body.get("status") in (400, 415):
                # Validation messages of connexion are not replicated
                body.pop("detail", None)
    allow = response.headers.get("allow")
    allow = None if allow is None else {m.strip() for m in allow.split(",")}
    return response.status_code, content_type.partition(";")[0], body, allow


IMPLEMENTATIONS = ["lean", pytest.param("rust", marks=requires_rust)]


@pytest.mark.parametrize("implementation", IMPLEMENTATIONS)
@pytest.mark.parametrize("case", CASES.keys())
def test_same_response_as_connexion(implementation, case):
    model_factory, requests = CASES[case]
    with (
        http_client("connexion", model_factory()) as expected_client,
        http_client(implementation, model_factory()) as actual_client,
    ):
        for method, path, kwargs in requests:
            expected = normalize(expected_client.request(method, path, **kwargs))
            actual = normalize(actual_client.request(method, path, **kwargs))
            assert actual == expected, f"{method} {path}"


def test_cases_cover_all_operations():
    covered = {
        path.split("/")[1] for _, requests in CASES.values() for _, path, _ in requests
    }
    assert set(ROUTES) <= covered


def test_routes_match_openapi_spec():
    spec = yaml.safe_load(SPEC.read_text())
    expected = {}
    for path, operations in spec["paths"].items():
        for method, operation in operations.items():
            params = [p["name"] for p in operation.get("parameters", [])]
            expected[operation["operationId"]] = (
                method.upper(),
                params[0] if params else None,
            )
            assert path == "/" + operation["operationId"] + (
                f"/{{{params[0]}}}" if params else ""
            )
    assert expected == ROUTES


def test_openapi_spec_copies_are_same():
    assert SPEC.read_text() == (Path(__file__).parents[2] / "openapi.yaml").read_text()


CORS_CASES: dict[str, tuple[list[str], str, dict[str, str]]] = {
    "simple, any origin": (["*"], "GET", {"origin": "http://a.org"}),
    "simple, allowed origin": (["http://a.org"], "GET", {"origin": "http://a.org"}),
    "simple, other origin": (["http://a.org"], "GET", {"origin": "http://b.org"}),
    "simple, no origin": (["http://a.org"], "GET", {}),
    "preflight, any origin": (
        ["*"],
        "OPTIONS",
        {
            "origin": "http://a.org",
            "access-control-request-method": "POST",
            "access-control-request-headers": "content-type, content-encoding",
        },
    ),
    "preflight, allowed origin": (
        ["http://a.org", "http://b.org"],
        "OPTIONS",
        {"origin": "http://b.org", "access-control-request-method": "GET"},
    ),
    "preflight, other origin": (
        ["http://a.org"],
        "OPTIONS",
        {"origin": "http://b.org", "access-control-request-method": "GET"},
    ),
    "preflight, other method": (
        ["*"],
        "OPTIONS",
        {"origin": "http://a.org", "access-control-request-method": "PUT"},
    ),
    "options without preflight headers": (["*"], "OPTIONS", {"origin": "http://a.org"}),
    "error response": (["*"], "PUT", {"origin": "http://a.org"}),
}


def cors_headers(response):
    headers = {
        k: v
        for k, v in response.headers.items()
        if k.startswith("access-control-") or k == "vary"
    }
    if "vary" in headers:
        # multiple vary headers are joined
        headers["vary"] = {
            v.strip() for v in ",".join(response.headers.get_list("vary")).split(",")
        } - {"Accept-Encoding"}
    return response.status_code, headers


@pytest.mark.parametrize("implementation", IMPLEMENTATIONS)
@pytest.mark.parametrize("case", CORS_CASES.keys())
def test_cors_same_as_connexion(implementation, case):
    origins, method, headers = CORS_CASES[case]
    path = "/get_var_grid/somevar"
    with (
        http_client("connexion", FullModel(), cors_origins=origins) as expected_client,
        http_client(implementation, FullModel(), cors_origins=origins) as actual_client,
    ):
        expected = cors_headers(expected_client.request(method, path, headers=headers))
        actual = cors_headers(actual_client.request(method, path, headers=headers))

    assert actual == expected


@pytest.mark.parametrize("implementation", ["connexion", *IMPLEMENTATIONS])
def test_no_cors_by_default(implementation):
    with http_client(implementation, FullModel()) as client:
        response = client.get(
            "/get_var_grid/somevar", headers={"origin": "http://a.org"}
        )

    assert "access-control-allow-origin" not in response.headers


requires_zstd = pytest.mark.skipif(zstd is None, reason="zstd not available")


class BigModel(FullModel):
    def __init__(self):
        super().__init__()
        self.value = np.linspace(0, 1, 10_000, dtype=np.float32)


@requires_zstd
@pytest.mark.parametrize("implementation", IMPLEMENTATIONS)
def test_compressed_response(implementation):
    with http_client(implementation, BigModel()) as client:
        request = client.build_request(
            "GET",
            "/get_value/somevar",
            headers={"accept": "application/octet-stream", "accept-encoding": "zstd"},
        )
        response = client.send(request, stream=True)
        raw = b"".join(response.iter_raw())
        response.close()

    assert response.headers["content-encoding"] == "zstd"
    assert zstd.decompress(raw) == BigModel().value.tobytes()  # type: ignore[union-attr]
    assert len(raw) < len(BigModel().value.tobytes())


@requires_zstd
@pytest.mark.parametrize("implementation", IMPLEMENTATIONS)
def test_small_response_not_compressed(implementation):
    with http_client(implementation, FullModel()) as client:
        response = client.get(
            "/get_var_grid/somevar", headers={"accept-encoding": "zstd"}
        )

    assert "content-encoding" not in response.headers
    assert response.headers["accept-encoding"] == "zstd"


@requires_zstd
@pytest.mark.parametrize("implementation", IMPLEMENTATIONS)
def test_compressed_request(implementation):
    model = BigModel()
    values = np.arange(10_000, dtype=np.float32)
    with http_client(implementation, model) as client:
        response = client.post(
            "/set_value/somevar",
            content=zstd.compress(values.tobytes()),  # type: ignore[union-attr]
            headers={
                "content-type": "application/octet-stream",
                "content-encoding": "zstd",
            },
        )

    assert response.status_code == 204
    np.testing.assert_array_equal(model.value, values)


@pytest.mark.parametrize("implementation", IMPLEMENTATIONS)
@pytest.mark.parametrize(
    ("encoding", "status"),
    [("gzip", 415), pytest.param("zstd", 400, marks=requires_zstd)],
)
def test_bad_content_encoding(implementation, encoding, status):
    with http_client(implementation, FullModel()) as client:
        response = client.post(
            "/set_value/somevar",
            content=b"not compressed",
            headers={
                "content-type": "application/octet-stream",
                "content-encoding": encoding,
            },
        )

    assert response.status_code == status
    assert response.headers["content-type"] == "application/problem+json"
