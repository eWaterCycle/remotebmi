# Connexion has no type stubs.
# mypy: disable-error-code="no-untyped-def,no-any-unimported"

import numpy as np
import pytest
import simplejson
from connexion import AsyncApp
from numpy.testing import assert_array_equal

from remotebmi import RemoteBmiClient
from remotebmi.nonfinite import IEEENumber
from remotebmi.reserve import (
    reserve_grid_nodes,
    reserve_grid_shape,
)
from remotebmi.server import make_app

from .fake_models import (
    NonFiniteFloat32Model,
    Rect3DGridModel,
)


@pytest.fixture
def fake_app():
    return make_app(Rect3DGridModel())


@pytest.fixture
def fake_client(fake_app: AsyncApp):
    with fake_app.test_client() as httpclient:
        yield RemoteBmiClient(base_url="http://testserver", client=httpclient)


def test_initialize(fake_client: RemoteBmiClient):
    fake_client.initialize("test.cfg")
    # TODO model func is a noop, use smarter model to test this better


def test_get_output_var_names(fake_client: RemoteBmiClient):
    names = fake_client.get_output_var_names()
    assert names == ("plate_surface__temperature",)


def test_get_output_item_count(fake_client: RemoteBmiClient):
    count = fake_client.get_output_item_count()
    assert count == 1


def test_var_grid(fake_client: RemoteBmiClient):
    grid = fake_client.get_var_grid("plate_surface__temperature")
    assert grid == 0


def test_get_grid_type(fake_client: RemoteBmiClient):
    gtype = fake_client.get_grid_type(1)
    assert gtype == "rectilinear"


def test_grid_size(fake_client: RemoteBmiClient):
    size = fake_client.get_grid_size(1)
    assert size == 24


def test_grid_rank(fake_client: RemoteBmiClient):
    rank = fake_client.get_grid_rank(1)
    assert rank == 3


def test_grid_shape(fake_client: RemoteBmiClient):
    out = reserve_grid_shape(fake_client, 1)

    result = fake_client.get_grid_shape(1, out)

    expected = np.array([2, 3, 4], dtype=np.int64)
    assert_array_equal(result, expected)
    assert_array_equal(out, expected)


def test_get_grid_x(fake_client: RemoteBmiClient):
    out = reserve_grid_nodes(fake_client, 1)

    result = fake_client.get_grid_x(1, out)

    expected = np.array([0.1, 0.2, 0.3, 0.4])
    assert_array_equal(result, expected)
    assert_array_equal(out, expected)


def test_get_grid_y(fake_client: RemoteBmiClient):
    out = reserve_grid_nodes(fake_client, 1, 1)

    result = fake_client.get_grid_y(1, out)

    expected = np.array([1.1, 1.2, 1.3])
    assert_array_equal(result, expected)
    assert_array_equal(out, expected)


def test_get_grid_z(fake_client: RemoteBmiClient):
    out = reserve_grid_nodes(fake_client, 1, 2)

    result = fake_client.get_grid_z(1, out)

    expected = np.array([2.1, 2.2])
    assert_array_equal(result, expected)
    assert_array_equal(out, expected)


class TestNonFiniteFloat32Model:
    @pytest.fixture
    def model(self):
        return NonFiniteFloat32Model()

    @pytest.fixture
    def fake_app(self, model: NonFiniteFloat32Model):
        return make_app(model)

    def test_get_value(self, fake_app: AsyncApp):
        with fake_app.test_client() as httpclient:
            response = httpclient.get("/get_value/some_var")

        values = simplejson.loads(response.content, allow_nan=False)

        assert values == ["NaN", "Infinity", "-Infinity", 42.0]

    def test_get_value_at_indices(self, fake_app: AsyncApp):
        with fake_app.test_client() as httpclient:
            response = httpclient.post(
                "/get_value_at_indices/some_var", json=[2, 3, 1, 0]
            )

        values = simplejson.loads(response.content, allow_nan=False)

        assert values == ["-Infinity", 42.0, "Infinity", "NaN"]

    def test_set_value(self, fake_app: AsyncApp, model: NonFiniteFloat32Model):
        model.value[:] = 0.0

        with fake_app.test_client() as httpclient:
            response = httpclient.post(
                "/set_value/some_var", json=["NaN", "Infinity", "-Infinity", 42.0]
            )

        assert response.status_code == 204
        assert_array_equal(model.value, [np.nan, np.inf, -np.inf, 42.0])

    def test_set_value_at_indices(
        self, fake_app: AsyncApp, model: NonFiniteFloat32Model
    ):
        with fake_app.test_client() as httpclient:
            response = httpclient.post(
                "/set_value_at_indices/some_var",
                json={
                    "indices": [2, 0, 1, 3],
                    "values": ["NaN", "Infinity", "-Infinity", 42.0],
                },
            )

        assert response.status_code == 204
        assert_array_equal(model.value, [np.inf, -np.inf, np.nan, 42.0])

    def assert_get_response(
        self, fake_app: AsyncApp, path: str, expected: IEEENumber | list[IEEENumber]
    ):
        with fake_app.test_client() as httpclient:
            response = httpclient.get(path)

        assert response.status_code == 200
        assert simplejson.loads(response.content, allow_nan=False) == expected

    def test_get_grid_spacing(self, fake_app: AsyncApp):
        self.assert_get_response(
            fake_app, "/get_grid_spacing/1", ["NaN", "Infinity", "-Infinity"]
        )

    def test_get_grid_origin(self, fake_app: AsyncApp):
        self.assert_get_response(
            fake_app, "/get_grid_origin/1", ["NaN", "Infinity", "-Infinity"]
        )

    def test_get_grid_x(self, fake_app: AsyncApp):
        self.assert_get_response(
            fake_app, "/get_grid_x/1", ["NaN", "Infinity", "-Infinity", 42.0]
        )

    def test_get_grid_y(self, fake_app: AsyncApp):
        self.assert_get_response(
            fake_app, "/get_grid_y/1", ["NaN", "Infinity", "-Infinity"]
        )

    def test_get_grid_z(self, fake_app: AsyncApp):
        self.assert_get_response(fake_app, "/get_grid_z/1", ["NaN", "Infinity"])

    @pytest.mark.parametrize(
        "value, encoded", [(42.0, 42.0), (np.inf, "Infinity"), (-np.inf, "-Infinity")]
    )
    def test_get_start_time(
        self,
        value: float,
        encoded: IEEENumber,
        fake_app: AsyncApp,
        model: NonFiniteFloat32Model,
    ):
        model.time = value
        self.assert_get_response(fake_app, "/get_start_time", encoded)

    @pytest.mark.parametrize(
        "value, encoded", [(42.0, 42.0), (np.inf, "Infinity"), (-np.inf, "-Infinity")]
    )
    def test_get_end_time(
        self,
        value: float,
        encoded: IEEENumber,
        fake_app: AsyncApp,
        model: NonFiniteFloat32Model,
    ):
        model.time = value
        self.assert_get_response(fake_app, "/get_end_time", encoded)

    @pytest.mark.parametrize(
        "value, encoded", [(42.0, 42.0), (np.inf, "Infinity"), (-np.inf, "-Infinity")]
    )
    def test_get_current_time(
        self,
        value: float,
        encoded: IEEENumber,
        fake_app: AsyncApp,
        model: NonFiniteFloat32Model,
    ):
        model.time = value
        self.assert_get_response(fake_app, "/get_current_time", encoded)

    @pytest.mark.parametrize(
        "value, encoded", [(42.0, 42.0), (np.inf, "Infinity"), (-np.inf, "-Infinity")]
    )
    def test_get_time_step(
        self,
        value: float,
        encoded: IEEENumber,
        fake_app: AsyncApp,
        model: NonFiniteFloat32Model,
    ):
        model.time = value
        self.assert_get_response(fake_app, "/get_time_step", encoded)

    @pytest.mark.parametrize(
        "value, encoded", [(42.0, 42.0), (np.inf, "Infinity"), (-np.inf, "-Infinity")]
    )
    def test_update_until_ieee_double(
        self,
        value: float,
        encoded: IEEENumber,
        fake_app: AsyncApp,
        model: NonFiniteFloat32Model,
    ):
        with fake_app.test_client() as httpclient:
            response = httpclient.post("/update_until", json=encoded)

        assert response.status_code == 204
        assert model.time == value

    def test_update_until_rejects_nan(
        self, fake_app: AsyncApp, model: NonFiniteFloat32Model
    ):
        with fake_app.test_client() as httpclient:
            response = httpclient.post("/update_until", json="NaN")

        assert response.status_code == 400
        assert model.time == 42.0
