# mypy: disable-error-code="no-untyped-def"

from collections.abc import Callable, Generator
from contextlib import contextmanager

import httpx
import numpy as np
import pytest
from numpy.testing import assert_array_equal

from remotebmi import RemoteBmiClient


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
        yield RemoteBmiClient(base_url="http://testserver", client=httpclient)


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


class TestNonFiniteNoneModel:
    def test_get_value(self):
        def handle_request(request: httpx.Request) -> httpx.Response:
            assert request.method == "GET"
            assert request.url.path == "/get_value/some_var"
            return httpx.Response(200, json=[42.0, None])

        out = np.empty(2, dtype=object)

        with make_fake_client(handle_request) as client:
            result = client.get_value("some_var", out)

        expected = np.array([42.0, None], dtype=object)
        assert_array_equal(result, expected)
        assert_array_equal(out, expected)
