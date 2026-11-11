# mypy: disable-error-code="no-untyped-def"

import json
from contextlib import ExitStack

import httpx
import pytest
import zstandard

from remotebmi.client.compression import CompressionClient


def assert_request_matches(actual: httpx.Request, expected: httpx.Request):
    header_names = ("Accept-Encoding", "Content-Encoding", "Content-Type")

    assert (
        actual.method,
        actual.url,
        [actual.headers.get(name) for name in header_names],
        actual.content,
    ) == (
        expected.method,
        expected.url,
        [expected.headers.get(name) for name in header_names],
        expected.content,
    )


def assert_response_matches(actual: httpx.Response, expected: httpx.Response):
    assert (actual.status_code, actual.headers, actual.content) == (
        expected.status_code,
        expected.headers,
        expected.content,
    )


def test_get_compressed():
    def handle_request(request):
        expected_request = httpx.Request(
            "GET",
            "http://testserver/get_value/temperature",
            headers={"Accept-Encoding": "zstd"},
        )

        assert_request_matches(request, expected_request)

        body = json.dumps([1.0, 2.0]).encode()
        return httpx.Response(
            200,
            content=zstandard.ZstdCompressor().compress(body),
            headers={"Content-Type": "application/json", "Content-Encoding": "zstd"},
        )

    with httpx.Client(
        base_url="http://testserver",
        transport=httpx.MockTransport(handle_request),
        headers={"Content-Encoding": "zstd"},
    ) as httpclient:
        with ExitStack() as responses:
            client = CompressionClient(
                client=httpclient, compress=True, responses=responses
            )

            result = client.get("/get_value/temperature")

        body = json.dumps([1.0, 2.0]).encode()
        expected_response = httpx.Response(
            200,
            content=zstandard.ZstdCompressor().compress(body),
            headers={"Content-Type": "application/json", "Content-Encoding": "zstd"},
        )
        assert_response_matches(result, expected_response)
        assert httpclient.headers["Content-Encoding"] == "zstd"


def test_get_uncompressed():
    def handle_request(request):
        expected_request = httpx.Request(
            "GET",
            "http://testserver/get_value/temperature",
            headers={"Accept-Encoding": "identity"},
        )

        assert_request_matches(request, expected_request)

        body = json.dumps([1.0, 2.0]).encode()
        return httpx.Response(
            200, content=body, headers={"Content-Type": "application/json"}
        )

    with httpx.Client(
        base_url="http://testserver",
        transport=httpx.MockTransport(handle_request),
        headers={"Content-Encoding": "zstd"},
    ) as httpclient:
        with ExitStack() as responses:
            client = CompressionClient(
                client=httpclient, compress=False, responses=responses
            )

            result = client.get("/get_value/temperature")

        body = json.dumps([1.0, 2.0]).encode()
        expected_response = httpx.Response(
            200, content=body, headers={"Content-Type": "application/json"}
        )
        assert_response_matches(result, expected_response)
        assert httpclient.headers["Content-Encoding"] == "zstd"


def test_post_compressed():
    def handle_request(request):
        body = b'{"indices":[1],"values":[2.0]}'
        body = zstandard.ZstdCompressor().compress(body)
        expected_request = httpx.Request(
            "POST",
            "http://testserver/set_value_at_indices/temperature",
            headers={
                "Accept-Encoding": "zstd",
                "Content-Type": "application/json",
                "Content-Encoding": "zstd",
            },
            content=body,
        )

        assert_request_matches(request, expected_request)

        return httpx.Response(204)

    with httpx.Client(
        base_url="http://testserver",
        transport=httpx.MockTransport(handle_request),
        headers={"Content-Encoding": "zstd"},
    ) as httpclient:
        with ExitStack() as responses:
            client = CompressionClient(
                client=httpclient, compress=True, responses=responses
            )

            values = {"indices": [1], "values": [2.0]}
            result = client.post("/set_value_at_indices/temperature", json=values)

        expected_response = httpx.Response(204)
        assert_response_matches(result, expected_response)
        assert httpclient.headers["Content-Encoding"] == "zstd"


def test_post_uncompressed():
    def handle_request(request):
        body = b'{"indices":[1],"values":[2.0]}'
        expected_request = httpx.Request(
            "POST",
            "http://testserver/set_value_at_indices/temperature",
            headers={"Accept-Encoding": "identity", "Content-Type": "application/json"},
            content=body,
        )

        assert_request_matches(request, expected_request)

        return httpx.Response(204)

    with httpx.Client(
        base_url="http://testserver",
        transport=httpx.MockTransport(handle_request),
        headers={"Content-Encoding": "zstd"},
    ) as httpclient:
        with ExitStack() as responses:
            client = CompressionClient(
                client=httpclient, compress=False, responses=responses
            )

            values = {"indices": [1], "values": [2.0]}
            result = client.post("/set_value_at_indices/temperature", json=values)

        expected_response = httpx.Response(204)
        assert_response_matches(result, expected_response)
        assert httpclient.headers["Content-Encoding"] == "zstd"


def test_response_closed_on_decoding_error():
    response = httpx.Response(
        200,
        stream=httpx.ByteStream(b"invalid zstd"),
        headers={"Content-Encoding": "zstd"},
    )

    with httpx.Client(
        base_url="http://testserver",
        transport=httpx.MockTransport(lambda _: response),
    ) as httpclient:
        with pytest.raises(httpx.DecodingError), ExitStack() as responses:
            client = CompressionClient(
                client=httpclient, compress=True, responses=responses
            )

            client.get("/get_value/temperature")

        assert response.is_closed
