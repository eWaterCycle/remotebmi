# mypy: disable-error-code="no-untyped-def"

import json
from collections.abc import Callable, Generator
from contextlib import contextmanager

import httpx
import numpy as np
import pytest
from numpy.testing import assert_array_equal

from remotebmi import RemoteBmiClient
from remotebmi.nonfinite import IEEENumber


@pytest.mark.parametrize(
    "url",
    [
        "invalid_url",
        "http://",
        "ws://somehost",
        "ftp://invalid",
        "12345",
        "",
        None,
    ],
)
def test_remote_bmi_client_init_invalid_url(url: str):
    with pytest.raises(ValueError):
        RemoteBmiClient(url)


@pytest.mark.parametrize(
    "url",
    [
        "http://somehost",
        "https://somehost",
    ],
)
def test_remote_bmi_client_init_valid_url(url: str):
    client = RemoteBmiClient(url)
    assert client.client.base_url == url


@contextmanager
def make_fake_client(
    handler: Callable[[httpx.Request], httpx.Response],
) -> Generator[RemoteBmiClient]:
    """Create a client with a test-specific HTTP request handler."""
    with httpx.Client(
        base_url="http://testserver", transport=httpx.MockTransport(handler)
    ) as httpclient:
        yield RemoteBmiClient(
            base_url="http://testserver", client=httpclient, compression="never"
        )


class TestNonFiniteFloat32Model:
    def test_get_value(self):
        def handle_request(request: httpx.Request) -> httpx.Response:
            assert request.method == "GET"
            assert request.url.path == "/get_value/some_var"
            return httpx.Response(200, json=["NaN", "Infinity", "-Infinity", 42.0])

        out = np.empty(4, dtype=np.float32)

        with make_fake_client(handle_request) as client:
            result = client.get_value("some_var", out)

        expected = np.array([np.nan, np.inf, -np.inf, 42.0], dtype=np.float32)
        assert_array_equal(result, expected)
        assert_array_equal(out, expected)

    def test_get_value_at_indices(self):
        def handle_request(request: httpx.Request) -> httpx.Response:
            assert request.method == "POST"
            assert request.url.path == "/get_value_at_indices/some_var"
            assert json.loads(request.content) == [2, 3, 1, 0]
            return httpx.Response(200, json=["-Infinity", 42.0, "Infinity", "NaN"])

        out = np.empty(4, dtype=np.float32)
        indices = np.array([2, 3, 1, 0])

        with make_fake_client(handle_request) as client:
            result = client.get_value_at_indices("some_var", out, indices)

        expected = np.array([-np.inf, 42.0, np.inf, np.nan], dtype=np.float32)
        assert result.dtype == np.float32
        assert_array_equal(result, expected)
        assert_array_equal(out, expected)

    def test_set_value(self):
        def handle_request(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/set_value/some_var"
            assert json.loads(request.content) == ["NaN", "Infinity", "-Infinity", 42.0]
            return httpx.Response(204)

        src = np.array([np.nan, np.inf, -np.inf, 42.0], dtype=np.float32)
        original = src.copy()

        with make_fake_client(handle_request) as client:
            client.set_value("some_var", src)

        assert_array_equal(src, original)

    def test_set_value_at_indices(self):
        def handle_request(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/set_value_at_indices/some_var"
            assert json.loads(request.content) == {
                "indices": [2, 0, 1, 3],
                "values": ["NaN", "Infinity", "-Infinity", 42.0],
            }
            return httpx.Response(204)

        src = np.array([np.nan, np.inf, -np.inf, 42.0], dtype=np.float32)
        original = src.copy()
        indices = np.array([2, 0, 1, 3])

        with make_fake_client(handle_request) as client:
            client.set_value_at_indices("some_var", indices, src)

        assert_array_equal(src, original)

    def assert_grid_response(
        self,
        method: Callable[[RemoteBmiClient, int, np.ndarray], np.ndarray],
        path: str,
    ):
        def handle_request(request: httpx.Request):
            assert request.url.path == path
            return httpx.Response(200, json=["NaN", "Infinity", "-Infinity", 42.0])

        out = np.empty(4, dtype=np.float64)
        with make_fake_client(handle_request) as client:
            result = method(client, 1, out)

        assert result is out
        assert_array_equal(out, [np.nan, np.inf, -np.inf, 42.0])

    def assert_time_response(
        self,
        method: Callable[[RemoteBmiClient], float],
        path: str,
        value: float,
        encoded: IEEENumber,
    ):
        def handle_request(request: httpx.Request):
            assert request.url.path == path
            return httpx.Response(200, json=encoded)

        with make_fake_client(handle_request) as client:
            assert_array_equal(method(client), value)

    def test_get_grid_spacing(self):
        self.assert_grid_response(
            RemoteBmiClient.get_grid_spacing, "/get_grid_spacing/1"
        )

    def test_get_grid_origin(self):
        self.assert_grid_response(RemoteBmiClient.get_grid_origin, "/get_grid_origin/1")

    def test_get_grid_x(self):
        self.assert_grid_response(RemoteBmiClient.get_grid_x, "/get_grid_x/1")

    def test_get_grid_y(self):
        self.assert_grid_response(RemoteBmiClient.get_grid_y, "/get_grid_y/1")

    def test_get_grid_z(self):
        self.assert_grid_response(RemoteBmiClient.get_grid_z, "/get_grid_z/1")

    @pytest.mark.parametrize(
        "value, encoded",
        [(42.0, 42.0), (np.nan, "NaN"), (np.inf, "Infinity"), (-np.inf, "-Infinity")],
    )
    def test_get_start_time(self, value: float, encoded: IEEENumber):
        self.assert_time_response(
            RemoteBmiClient.get_start_time, "/get_start_time", value, encoded
        )

    @pytest.mark.parametrize(
        "value, encoded",
        [(42.0, 42.0), (np.nan, "NaN"), (np.inf, "Infinity"), (-np.inf, "-Infinity")],
    )
    def test_get_end_time(self, value: float, encoded: IEEENumber):
        self.assert_time_response(
            RemoteBmiClient.get_end_time, "/get_end_time", value, encoded
        )

    @pytest.mark.parametrize(
        "value, encoded",
        [(42.0, 42.0), (np.nan, "NaN"), (np.inf, "Infinity"), (-np.inf, "-Infinity")],
    )
    def test_get_current_time(self, value: float, encoded: IEEENumber):
        self.assert_time_response(
            RemoteBmiClient.get_current_time, "/get_current_time", value, encoded
        )

    @pytest.mark.parametrize(
        "value, encoded",
        [(42.0, 42.0), (np.nan, "NaN"), (np.inf, "Infinity"), (-np.inf, "-Infinity")],
    )
    def test_get_time_step(self, value: float, encoded: IEEENumber):
        self.assert_time_response(
            RemoteBmiClient.get_time_step, "/get_time_step", value, encoded
        )

    @pytest.mark.parametrize(
        "value, encoded",
        [(42.0, 42.0), (np.nan, "NaN"), (np.inf, "Infinity"), (-np.inf, "-Infinity")],
    )
    def test_update_until_ieee_double(self, value: float, encoded: IEEENumber):
        def handle_request(request: httpx.Request):
            assert request.url.path == "/update_until"
            assert json.loads(request.content) == encoded
            return httpx.Response(204)

        with make_fake_client(handle_request) as client:
            client.update_until(value)
