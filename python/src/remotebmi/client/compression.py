"""Zstd-aware HTTPX adapter for BMI value transfers."""

from contextlib import ExitStack
from dataclasses import dataclass
from json import dumps
from typing import Literal, get_args

import zstandard
from httpx import Client, Response

Compression = Literal["auto", "never", "always"]


def validate_compression(compression: Compression) -> None:
    """Reject unknown compression modes."""
    if compression not in get_args(Compression):
        msg = f"compression must be one of: {', '.join(get_args(Compression))}"
        raise ValueError(msg)


@dataclass
class _CompressionClient:
    """Apply compression per request and register responses for context cleanup."""

    client: Client
    compress: bool
    require_compressed_response: bool
    responses: ExitStack

    def _request(self, method: str, path: str, json: object = None) -> Response:
        """Send a value request and enforce required response compression."""
        headers = {"Accept-Encoding": "zstd" if self.compress else "identity"}
        content = None
        if json is not None:
            content = dumps(
                json, ensure_ascii=False, allow_nan=False, separators=(",", ":")
            ).encode()
            headers["Content-Type"] = "application/json"
        if self.compress and content is not None:
            content = zstandard.ZstdCompressor().compress(content)
            headers["Content-Encoding"] = "zstd"
        request = self.client.build_request(
            method, path, content=content, headers=headers
        )
        if "Content-Encoding" not in headers:
            request.headers.pop("Content-Encoding", None)
        response = self.client.send(request, stream=True)
        self.responses.callback(response.close)
        response.read()
        if (
            self.require_compressed_response
            and response.status_code == 200
            and response.headers.get("Content-Encoding", "").lower() != "zstd"
        ):
            msg = "Server returned an uncompressed value response despite compression='always'"
            raise RuntimeError(msg)
        return response

    def get(self, path: str) -> Response:
        """Get values using the negotiated response encoding."""
        return self._request("GET", path)

    def post(self, path: str, *, json: object) -> Response:
        """Post JSON, compressing its bytes when enabled."""
        return self._request("POST", path, json=json)
