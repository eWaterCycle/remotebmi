# mypy: disable-error-code="no-untyped-def"

import json
from contextlib import closing, contextmanager
from types import SimpleNamespace

import httpx
import numpy as np
import pytest
import zstandard

from remotebmi import RemoteBmiClient
from remotebmi.client.apptainer import BmiClientApptainer
from remotebmi.client.docker import BmiClientDocker


class FakeContainer:
    status = "running"

    def reload(self):
        pass

    def stop(self):
        pass


class FakeProcess:
    def poll(self):
        return None

    def terminate(self):
        pass

    def wait(self):
        return 0


class TestCompression:
    @contextmanager
    def make_client(
        self,
        responses: list[httpx.Response],
        compression: bool = False,
        client_headers: dict[str, str] | None = None,
    ):
        requests: list[httpx.Request] = []
        response_iter = iter(responses)

        def handle_request(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return next(response_iter)

        headers = {"Accept-Encoding": "gzip, zstd"}
        headers.update(client_headers or {})
        with httpx.Client(
            base_url="http://testserver",
            transport=httpx.MockTransport(handle_request),
            headers=headers,
        ) as httpclient:
            client = RemoteBmiClient(
                "http://testserver", client=httpclient, compression=compression
            )
            yield client, requests, httpclient

    def compressed_response(self, values: list[float]) -> httpx.Response:
        return httpx.Response(
            200,
            content=zstandard.ZstdCompressor().compress(json.dumps(values).encode()),
            headers={"Content-Encoding": "zstd", "Content-Type": "application/json"},
        )

    def request_details(self, request: httpx.Request) -> dict:
        return {
            "method": request.method,
            "path": request.url.path,
            "accept_encoding": request.headers["accept-encoding"],
            "content_encoding": request.headers.get("content-encoding"),
        }

    def test_client_context_manager(self):
        response = httpx.Response(200, json=[1.0, 2.0])
        with self.make_client([response]) as (client, _, _):
            with client._compression_client() as httpclient:
                result = httpclient.get("/get_value/temperature")
                values = result.json()
            assert (values, response.is_closed) == ([1.0, 2.0], True)

    def test_client_context_closes_http_error(self):
        response = httpx.Response(500, stream=httpx.ByteStream(b"error"))
        with self.make_client([response]) as (client, _, _):
            with (
                pytest.raises(httpx.HTTPStatusError),
                client._compression_client() as httpclient,
            ):
                httpclient.get("/get_value/temperature").raise_for_status()
            assert response.is_closed

    @pytest.mark.parametrize("mode", [True, False])
    @pytest.mark.parametrize(
        "response, expected",
        [
            (
                httpx.Response(200, json={"supports_zstd": False}),
                {"supports_zstd": False},
            ),
            (httpx.Response(404), None),
        ],
    )
    def test_capabilities_property_fetches_once(self, mode, response, expected):
        with self.make_client([response], compression=mode) as (client, requests, _):
            first = client.capabilities
            second = client.capabilities
            assert {
                "capabilities": [first, second],
                "requests": [self.request_details(request) for request in requests],
            } == {
                "capabilities": [expected, expected],
                "requests": [
                    {
                        "method": "GET",
                        "path": "/remotebmi_capabilities",
                        "accept_encoding": "identity",
                        "content_encoding": None,
                    }
                ],
            }

    def test_compressed_get_and_cached_capabilities(self):
        capabilities = {
            "bmi_version": "2.0",
            "remotebmi_version": "0.1.1",
            "supports_binary": False,
            "index_type": "int64",
            "byte_order": "little",
            "supports_zstd": True,
        }
        responses = [
            httpx.Response(200, json=capabilities),
            self.compressed_response([1.0, 2.0]),
            self.compressed_response([3.0, 4.0]),
        ]
        with self.make_client(responses, compression=True) as (
            client,
            requests,
            httpclient,
        ):
            first = client.get_value("temperature", np.empty(2)).tolist()
            second = client.get_value("temperature", np.empty(2)).tolist()
            expected_get = {
                "method": "GET",
                "path": "/get_value/temperature",
                "accept_encoding": "zstd",
                "content_encoding": None,
            }
            assert {
                "values": [first, second],
                "requests": [self.request_details(request) for request in requests],
                "client_accept_encoding": httpclient.headers["accept-encoding"],
                "capabilities": client.capabilities,
            } == {
                "values": [[1.0, 2.0], [3.0, 4.0]],
                "requests": [
                    {
                        "method": "GET",
                        "path": "/remotebmi_capabilities",
                        "accept_encoding": "identity",
                        "content_encoding": None,
                    },
                    expected_get,
                    expected_get,
                ],
                "client_accept_encoding": "gzip, zstd",
                "capabilities": capabilities,
            }

    @pytest.mark.parametrize(
        "capabilities",
        [
            httpx.Response(200, json={"supports_zstd": False}),
            httpx.Response(200, json={}),
            httpx.Response(404),
        ],
    )
    def test_enabled_falls_back_to_identity(self, capabilities):
        responses = [
            capabilities,
            httpx.Response(200, json=[1.0]),
            httpx.Response(200, json=[2.0]),
        ]
        with self.make_client(responses, compression=True) as (
            client,
            requests,
            _,
        ):
            values = client.get_value("temperature", np.empty(1)).tolist()
            second = client.get_value("temperature", np.empty(1)).tolist()
            assert {
                "values": [values, second],
                "paths": [request.url.path for request in requests],
                "encodings": [
                    request.headers["accept-encoding"] for request in requests
                ],
            } == {
                "values": [[1.0], [2.0]],
                "paths": [
                    "/remotebmi_capabilities",
                    "/get_value/temperature",
                    "/get_value/temperature",
                ],
                "encodings": ["identity"] * 3,
            }

    def test_compression_defaults_to_false(self):
        client = RemoteBmiClient("http://testserver")
        with closing(client.client):
            assert client.compression is False

    def test_disabled_skips_capabilities(self):
        with self.make_client([httpx.Response(200, json=[1.0])]) as (
            client,
            requests,
            _,
        ):
            values = client.get_value("temperature", np.empty(1)).tolist()
            assert (
                values,
                [self.request_details(request) for request in requests],
            ) == (
                [1.0],
                [
                    {
                        "method": "GET",
                        "path": "/get_value/temperature",
                        "accept_encoding": "identity",
                        "content_encoding": None,
                    }
                ],
            )

    @pytest.mark.parametrize("mode", [True, False])
    def test_metadata_requests_use_httpx_defaults(self, mode):
        with self.make_client(
            [httpx.Response(200, json={"name": "model"})], compression=mode
        ) as (
            client,
            requests,
            _,
        ):
            name = client.get_component_name()
            assert (name, requests[0].headers["accept-encoding"]) == (
                "model",
                "gzip, zstd",
            )

    def test_compressed_indexed_get(self):
        responses = [
            httpx.Response(200, json={"supports_zstd": True}),
            self.compressed_response([2.0]),
        ]
        with self.make_client(responses, compression=True) as (client, requests, _):
            values = client.get_value_at_indices(
                "temperature", np.empty(1), np.array([1])
            ).tolist()
            request = requests[-1]
            assert {
                "request": self.request_details(request),
                "content_type": request.headers["content-type"],
                "indices": json.loads(
                    zstandard.ZstdDecompressor().decompress(request.content)
                ),
                "values": values,
            } == {
                "request": {
                    "method": "POST",
                    "path": "/get_value_at_indices/temperature",
                    "accept_encoding": "zstd",
                    "content_encoding": "zstd",
                },
                "content_type": "application/json",
                "indices": [1],
                "values": [2.0],
            }

    def test_compressed_setters_accept_no_content_response(self):
        responses = [
            httpx.Response(200, json={"supports_zstd": True}),
            httpx.Response(204),
            httpx.Response(204),
        ]
        with self.make_client(responses, compression=True) as (client, requests, _):
            client.set_value("temperature", np.array([1.0, 2.0]))
            client.set_value_at_indices("temperature", np.array([1]), np.array([3.0]))
            assert [
                (
                    request.url.path,
                    request.headers["content-encoding"],
                    json.loads(
                        zstandard.ZstdDecompressor().decompress(request.content)
                    ),
                )
                for request in requests[1:]
            ] == [
                ("/set_value/temperature", "zstd", [1.0, 2.0]),
                (
                    "/set_value_at_indices/temperature",
                    "zstd",
                    {"indices": [1], "values": [3.0]},
                ),
            ]

    def test_disabled_sends_uncompressed_setter(self):
        with self.make_client([httpx.Response(204)], compression=False) as (
            client,
            requests,
            _,
        ):
            client.set_value("temperature", np.array([1.0, 2.0]))
            request = requests[0]
            assert (self.request_details(request), json.loads(request.content)) == (
                {
                    "method": "POST",
                    "path": "/set_value/temperature",
                    "accept_encoding": "identity",
                    "content_encoding": None,
                },
                [1.0, 2.0],
            )

    def test_capabilities_error_propagates(self):
        with self.make_client([httpx.Response(500)], compression=True) as (
            client,
            requests,
            _,
        ):
            with pytest.raises(httpx.HTTPStatusError):
                client.set_value("temperature", np.array([1.0]))
            assert len(requests) == 1

    def test_enabled_accepts_uncompressed_value_response(self):
        responses = [
            httpx.Response(200, json={"supports_zstd": True}),
            httpx.Response(200, json=[1.0]),
        ]
        with self.make_client(responses, compression=True) as (client, _, _):
            assert client.get_value("temperature", np.empty(1)).tolist() == [1.0]

    def test_enabled_propagates_value_error_without_retry(self):
        responses = [
            httpx.Response(200, json={"supports_zstd": True}),
            httpx.Response(500),
        ]
        with self.make_client(responses, compression=True) as (client, requests, _):
            with pytest.raises(httpx.HTTPStatusError):
                client.get_value("temperature", np.empty(1))
            assert len(requests) == 2

    @pytest.mark.parametrize("mode", ["auto", "never", "always", "invalid"])
    def test_invalid_compression_mode(self, mode):
        with pytest.raises(TypeError, match="compression"):
            RemoteBmiClient("http://testserver", compression=mode)

    @pytest.mark.parametrize(
        "mode, capabilities",
        [
            (False, []),
            (True, [httpx.Response(200, json={"supports_zstd": False})]),
            (True, [httpx.Response(404)]),
        ],
    )
    def test_uncompressed_requests_remove_inherited_encoding(self, mode, capabilities):
        with self.make_client(
            [*capabilities, httpx.Response(204)],
            compression=mode,
            client_headers={"Content-Encoding": "zstd"},
        ) as (client, requests, httpclient):
            client.set_value("temperature", np.array([1.0]))
            assert {
                "request_encodings": [
                    request.headers.get("content-encoding") for request in requests
                ],
                "values": json.loads(requests[-1].content),
                "client_encoding": httpclient.headers["content-encoding"],
            } == {
                "request_encodings": [None] * len(requests),
                "values": [1.0],
                "client_encoding": "zstd",
            }

    def test_metadata_preserves_inherited_encoding(self):
        with self.make_client(
            [httpx.Response(200, json={"name": "model"})],
            client_headers={"Content-Encoding": "zstd"},
        ) as (client, requests, _):
            name = client.get_component_name()
            assert (name, requests[0].headers.get("content-encoding")) == (
                "model",
                "zstd",
            )

    def test_setter_error_is_not_retried(self):
        responses = [
            httpx.Response(200, json={"supports_zstd": True}),
            httpx.Response(500),
        ]
        with self.make_client(responses, compression=True) as (client, requests, _):
            with pytest.raises(httpx.HTTPStatusError):
                client.set_value("temperature", np.array([1.0]))
            assert [request.url.path for request in requests] == [
                "/remotebmi_capabilities",
                "/set_value/temperature",
            ]

    @pytest.mark.parametrize("mode", [None, True, False])
    def test_docker_forwards_compression(self, mode, tmp_path, monkeypatch):
        def run_container(*args, **kwargs):
            return FakeContainer()

        docker_client = SimpleNamespace(containers=SimpleNamespace(run=run_container))
        monkeypatch.setattr(
            "remotebmi.client.docker.docker.from_env", lambda: docker_client
        )
        kwargs = {} if mode is None else {"compression": mode}
        client = BmiClientDocker(
            "model", str(tmp_path), host="localhost", delay=0, **kwargs
        )
        with closing(client.client):
            assert client.compression is (mode or False)

    @pytest.mark.parametrize("mode", [None, True, False])
    def test_apptainer_forwards_compression(self, mode, tmp_path, monkeypatch):
        def start_process(*args, **kwargs):
            return FakeProcess()

        monkeypatch.setattr(
            "remotebmi.client.apptainer.subprocess.Popen", start_process
        )
        kwargs = {} if mode is None else {"compression": mode}
        client = BmiClientApptainer(
            "model", str(tmp_path), capture_logs=False, **kwargs
        )
        with closing(client.client):
            assert client.compression is (mode or False)
