# Connexion has no type stubs.
# mypy: disable-error-code="no-untyped-def,no-any-unimported"

import sys
from importlib.metadata import version

import numpy as np
import pytest
import simplejson
import zstandard
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
    Float32Model,
    NonFiniteFloat32Model,
    Rect3DGridModel,
)


@pytest.fixture
def fake_app():
    return make_app(Rect3DGridModel())


def test_remotebmi_capabilities(fake_app: AsyncApp):
    with fake_app.test_client() as httpclient:
        response = httpclient.get("/remotebmi_capabilities")

    assert response.status_code == 200
    expected = {
        "bmi_version": "2.0",
        "remotebmi_version": version("remotebmi"),
        "supports_binary": False,
        "index_type": f"int{np.dtype(int).itemsize * 8}",
        "byte_order": sys.byteorder,
        "supports_zstd": True,
    }
    assert response.json() == expected


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
        "value, encoded",
        [(42.0, 42.0), (np.nan, "NaN"), (np.inf, "Infinity"), (-np.inf, "-Infinity")],
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
        "value, encoded",
        [(42.0, 42.0), (np.nan, "NaN"), (np.inf, "Infinity"), (-np.inf, "-Infinity")],
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
        "value, encoded",
        [(42.0, 42.0), (np.nan, "NaN"), (np.inf, "Infinity"), (-np.inf, "-Infinity")],
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
        "value, encoded",
        [(42.0, 42.0), (np.nan, "NaN"), (np.inf, "Infinity"), (-np.inf, "-Infinity")],
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
        "value, encoded",
        [(42.0, 42.0), (np.nan, "NaN"), (np.inf, "Infinity"), (-np.inf, "-Infinity")],
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
        assert_array_equal(model.time, value)


class TestCompression:
    @pytest.fixture
    def model(self):
        model = Float32Model()
        model.value[:] = [1.0, 2.0, 3.0]
        return model

    @pytest.fixture
    def fake_app(self, model: Float32Model):
        return make_app(model)

    def get_raw_value_response(
        self,
        fake_app: AsyncApp,
        model: Float32Model,
        headers: dict[str, str],
    ):
        model.value = np.tile(model.value, 256)
        with fake_app.test_client() as httpclient:
            httpclient.headers.pop("Accept-Encoding", None)
            with httpclient.stream(
                "GET",
                "/get_value/some_var",
                headers=headers,
            ) as response:
                body = b"".join(response.iter_raw())

        expected_response = {
            "status_code": 200,
            "content-type": "application/json",
            "vary": "Accept-Encoding",
            "content-length": str(len(body)),
        }
        actual_response = {
            "status_code": response.status_code,
            "content-type": response.headers.get("content-type"),
            "vary": response.headers.get("vary"),
            "content-length": response.headers.get("content-length"),
        }
        assert actual_response == expected_response
        return response, body

    def assert_value_body(self, body: bytes):
        assert simplejson.loads(body, allow_nan=False) == [1.0, 2.0, 3.0] * 256

    @pytest.mark.parametrize("accept_encoding", ["zstd", "gzip, zstd", "ZSTD"])
    def test_get_value_compression(
        self,
        fake_app: AsyncApp,
        model: Float32Model,
        accept_encoding: str,
    ):
        response, body = self.get_raw_value_response(
            fake_app, model, {"Accept-Encoding": accept_encoding}
        )

        assert response.headers["content-encoding"] == "zstd"
        decoded = zstandard.ZstdDecompressor().decompress(body, max_output_size=100_000)
        self.assert_value_body(decoded)

    @pytest.mark.parametrize(
        "headers",
        [
            {"Accept-Encoding": "*"},  # Only explicit zstd enables compression.
            {"Accept-Encoding": "zstd;q=0"},  # Weighted tokens do not match bare zstd.
            {"Accept-Encoding": "zstd;q=0.5"},  # Quality weights are not parsed.
            {"Accept-Encoding": "gzip"},
            {"Accept-Encoding": "identity"},
            {"Accept-Encoding": ""},
            {},
        ],
    )
    def test_get_value_uncompressed(
        self,
        fake_app: AsyncApp,
        model: Float32Model,
        headers: dict[str, str],
    ):
        response, body = self.get_raw_value_response(fake_app, model, headers)

        assert "content-encoding" not in response.headers
        self.assert_value_body(body)

    def test_get_value_small_response(self, fake_app: AsyncApp):
        with fake_app.test_client() as httpclient:
            response = httpclient.get(
                "/get_value/some_var", headers={"Accept-Encoding": "zstd"}
            )

        expected_response = {"content-encoding": "zstd", "values": [1.0, 2.0, 3.0]}
        assert {
            "content-encoding": response.headers.get("content-encoding"),
            "values": response.json(),
        } == expected_response

    def test_get_value_client_decompression(
        self, fake_client: RemoteBmiClient, model: Float32Model
    ):
        model.value = np.tile(model.value, 256)
        result = fake_client.get_value("some_var", np.empty_like(model.value))
        assert_array_equal(result, model.value)

    def test_indexed_getter_compression(self, fake_app: AsyncApp):
        with fake_app.test_client() as httpclient:
            response = httpclient.post(
                "/get_value_at_indices/some_var",
                json=[0] * 256,
                headers={"Accept-Encoding": "zstd"},
            )

        expected_response = {"content-encoding": "zstd", "values": [1.0] * 256}
        assert {
            "content-encoding": response.headers.get("content-encoding"),
            "values": response.json(),
        } == expected_response

    def post_compressed(self, fake_app: AsyncApp, path: str, body: object):
        content = zstandard.ZstdCompressor().compress(simplejson.dumps(body).encode())
        with fake_app.test_client() as httpclient:
            return httpclient.post(
                path,
                content=content,
                headers={
                    "Content-Type": "application/json",
                    "Content-Encoding": "zstd",
                    "Accept-Encoding": "zstd",
                },
            )

    def test_compressed_indices(self, fake_app: AsyncApp):
        response = self.post_compressed(
            fake_app, "/get_value_at_indices/some_var", [2, 0]
        )
        assert {
            "status": response.status_code,
            "encoding": response.headers.get("content-encoding"),
            "values": response.json(),
        } == {"status": 200, "encoding": "zstd", "values": [3.0, 1.0]}

    @pytest.mark.parametrize(
        "path, body, expected",
        [
            ("/set_value/some_var", [4.0, 5.0, 6.0], [4.0, 5.0, 6.0]),
            (
                "/set_value_at_indices/some_var",
                {"indices": [2, 0], "values": [4.0, 5.0]},
                [5.0, 2.0, 4.0],
            ),
        ],
    )
    def test_compressed_setter(
        self,
        fake_app: AsyncApp,
        model: Float32Model,
        path: str,
        body: object,
        expected: list[float],
    ):
        response = self.post_compressed(fake_app, path, body)
        assert {
            "status": response.status_code,
            "encoding": response.headers.get("content-encoding"),
            "body": response.content,
            "values": model.value.tolist(),
        } == {"status": 204, "encoding": None, "body": b"", "values": expected}

    @pytest.mark.parametrize(
        "encoding, content, status",
        [
            ("zstd", b"invalid", 400),
            ("zstd", b"\x28\xb5", 400),
            ("zstd", zstandard.ZstdCompressor().compress(b"[]")[:-1], 400),
            ("zstd", zstandard.ZstdCompressor().compress(b"[]") + b"extra", 400),
            ("gzip", b"[]", 415),
        ],
    )
    def test_invalid_request_encoding(
        self,
        fake_app: AsyncApp,
        model: Float32Model,
        encoding: str,
        content: bytes,
        status: int,
    ):
        with fake_app.test_client() as httpclient:
            response = httpclient.post(
                "/set_value/some_var",
                content=content,
                headers={
                    "Content-Type": "application/json",
                    "Content-Encoding": encoding,
                },
            )
        assert {"status": response.status_code, "values": model.value.tolist()} == {
            "status": status,
            "values": [1.0, 2.0, 3.0],
        }

    def test_compressed_body_is_validated(
        self, fake_app: AsyncApp, model: Float32Model
    ):
        response = self.post_compressed(
            fake_app, "/set_value/some_var", {"unexpected": []}
        )
        assert {"status": response.status_code, "values": model.value.tolist()} == {
            "status": 400,
            "values": [1.0, 2.0, 3.0],
        }

    @pytest.mark.parametrize(
        "compression, accept_encoding, content_encoding",
        [
            (True, "zstd", "zstd"),
            (False, "identity", None),
        ],
    )
    def test_value_transfers(
        self,
        fake_app: AsyncApp,
        model: Float32Model,
        compression: bool,
        accept_encoding: str,
        content_encoding: str | None,
    ):
        request_headers: list[tuple[str | None, str | None]] = []

        def record_headers(request):
            request_headers.append(
                (
                    request.headers.get("accept-encoding"),
                    request.headers.get("content-encoding"),
                )
            )

        with fake_app.test_client() as httpclient:
            httpclient.event_hooks["request"].append(record_headers)
            client = RemoteBmiClient(
                "http://testserver", client=httpclient, compression=compression
            )
            client.set_value("some_var", np.array([4.0, 5.0, 6.0]))
            full_result = client.get_value("some_var", np.empty(3))
            client.set_value_at_indices(
                "some_var", np.array([0, 2]), np.array([7.0, 8.0])
            )
            indexed_result = client.get_value_at_indices(
                "some_var", np.empty(2), np.array([2, 0])
            )

        expected = {
            "full_result": [4.0, 5.0, 6.0],
            "indexed_result": [8.0, 7.0],
            "model_values": [7.0, 5.0, 8.0],
            "request_headers": [
                (accept_encoding, content_encoding),
                (accept_encoding, None),
                (accept_encoding, content_encoding),
                (accept_encoding, content_encoding),
            ],
        }
        actual = {
            "full_result": full_result.tolist(),
            "indexed_result": indexed_result.tolist(),
            "model_values": model.value.tolist(),
            "request_headers": request_headers[-4:],
        }
        assert actual == expected
