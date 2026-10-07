# mypy: disable-error-code="no-untyped-def"

import numpy as np
import pytest
from numpy.testing import assert_array_equal
from starlette.testclient import TestClient

from remotebmi import RemoteBmiClient
from remotebmi.reserve import (
    reserve_grid_nodes,
    reserve_grid_shape,
)
from remotebmi.server import make_app
from remotebmi.server.lean import make_lean_app

from .fake_models import Float32Model, Int32Model, Rect3DGridModel


@pytest.fixture(params=[make_app, make_lean_app], ids=["connexion", "lean"])
def app_factory(request):
    return request.param


@pytest.fixture
def fake_app(app_factory):
    return app_factory(Rect3DGridModel())


@pytest.fixture
def fake_client(fake_app):
    with TestClient(fake_app) as httpclient:
        yield RemoteBmiClient(base_url="http://testserver", client=httpclient)


def test_initialize(fake_client):
    fake_client.initialize("test.cfg")
    # TODO model func is a noop, use smarter model to test this better


def test_get_output_var_names(fake_client):
    names = fake_client.get_output_var_names()
    assert names == ("plate_surface__temperature",)


def test_get_output_item_count(fake_client):
    count = fake_client.get_output_item_count()
    assert count == 1


def test_var_grid(fake_client):
    grid = fake_client.get_var_grid("plate_surface__temperature")
    assert grid == 0


def test_get_grid_type(fake_client):
    gtype = fake_client.get_grid_type(1)
    assert gtype == "rectilinear"


def test_grid_size(fake_client):
    size = fake_client.get_grid_size(1)
    assert size == 24


def test_grid_rank(fake_client):
    rank = fake_client.get_grid_rank(1)
    assert rank == 3


def test_grid_shape(fake_client):
    out = reserve_grid_shape(fake_client, 1)

    result = fake_client.get_grid_shape(1, out)

    expected = np.array([2, 3, 4], dtype=np.int64)
    assert_array_equal(result, expected)
    assert_array_equal(out, expected)


def test_get_grid_x(fake_client):
    out = reserve_grid_nodes(fake_client, 1)

    result = fake_client.get_grid_x(1, out)

    expected = np.array([0.1, 0.2, 0.3, 0.4])
    assert_array_equal(result, expected)
    assert_array_equal(out, expected)


def test_get_grid_y(fake_client):
    out = reserve_grid_nodes(fake_client, 1, 1)

    result = fake_client.get_grid_y(1, out)

    expected = np.array([1.1, 1.2, 1.3])
    assert_array_equal(result, expected)
    assert_array_equal(out, expected)


def test_get_grid_z(fake_client):
    out = reserve_grid_nodes(fake_client, 1, 2)

    result = fake_client.get_grid_z(1, out)

    expected = np.array([2.1, 2.2])
    assert_array_equal(result, expected)
    assert_array_equal(out, expected)


@pytest.fixture(params=[Float32Model, Int32Model])
def dtype_model(request):
    return request.param()


@pytest.fixture
def dtype_httpclient(dtype_model, app_factory):
    with TestClient(app_factory(dtype_model)) as httpclient:
        yield httpclient


@pytest.mark.parametrize("binary_values", [False, True], ids=["json", "binary"])
def test_get_value(dtype_model, dtype_httpclient, binary_values):
    client = RemoteBmiClient(
        base_url="http://testserver",
        client=dtype_httpclient,
        binary_values=binary_values,
    )
    dest = np.empty(3, dtype=dtype_model.dtype)

    client.get_value("somevar", dest)

    assert_array_equal(dest, dtype_model.value)


@pytest.mark.parametrize("binary_values", [False, True], ids=["json", "binary"])
def test_set_value(dtype_model, dtype_httpclient, binary_values):
    client = RemoteBmiClient(
        base_url="http://testserver",
        client=dtype_httpclient,
        binary_values=binary_values,
    )
    src = np.array([4, 5, 6], dtype=np.float64)

    client.set_value("somevar", src)

    assert_array_equal(dtype_model.value, src)
    assert dtype_model.value.dtype == dtype_model.dtype


@pytest.mark.parametrize(
    ("accept", "expected"),
    [
        (None, "application/json"),
        ("*/*", "application/json"),
        ("application/json", "application/json"),
        ("application/octet-stream", "application/octet-stream"),
        (
            "application/octet-stream, application/json;q=0.5",
            "application/octet-stream",
        ),
        ("application/json, application/octet-stream;q=0.5", "application/json"),
        ("application/octet-stream;q=0", "application/json"),
    ],
)
def test_get_value_content_negotiation(accept, expected, app_factory):
    model = Float32Model()
    headers = {} if accept is None else {"Accept": accept}
    with TestClient(app_factory(model)) as httpclient:
        response = httpclient.get("/get_value/somevar", headers=headers)

    assert response.status_code == 200
    assert response.headers["content-type"] == expected
    if expected == "application/octet-stream":
        assert response.content == model.value.astype("<f4").tobytes()


@pytest.mark.parametrize("body", [b"", b"12345"], ids=["empty", "partial item"])
def test_set_value_octet_stream_invalid_length(body, app_factory):
    with TestClient(app_factory(Float32Model())) as httpclient:
        response = httpclient.post(
            "/set_value/somevar",
            content=body,
            headers={"Content-Type": "application/octet-stream"},
        )

    assert response.status_code == 400


class UpdateUntilModel(Float32Model):
    def update_until(self, time):
        self.until = time


def test_update_until(app_factory):
    model = UpdateUntilModel()
    with TestClient(app_factory(model)) as httpclient:
        client = RemoteBmiClient(base_url="http://testserver", client=httpclient)

        client.update_until(42.5)

    assert model.until == 42.5


def test_get_value_at_indices(dtype_model, dtype_httpclient):
    client = RemoteBmiClient(base_url="http://testserver", client=dtype_httpclient)
    dest = np.empty(2, dtype=dtype_model.dtype)

    client.get_value_at_indices("somevar", dest, np.array([0, 2]))

    assert_array_equal(dest, dtype_model.value[[0, 2]])


def test_set_value_at_indices(dtype_model, dtype_httpclient):
    client = RemoteBmiClient(base_url="http://testserver", client=dtype_httpclient)
    expected = dtype_model.value.copy()
    expected[[0, 2]] = [7, 8]

    client.set_value_at_indices("somevar", np.array([0, 2]), np.array([7.0, 8.0]))

    assert_array_equal(dtype_model.value, expected)


def test_initialize_status(app_factory):
    with TestClient(app_factory(Float32Model())) as httpclient:
        response = httpclient.post("/initialize", json={"config_file": "test.cfg"})

    assert response.status_code == 201


# TODO test all BMI functions
