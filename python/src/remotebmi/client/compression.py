"""Zstd-aware HTTPX adapter for BMI value transfers."""

from contextlib import ExitStack
from dataclasses import dataclass
from json import dumps

import zstandard
from httpx import Client, Response


@dataclass
class CompressionClient:
    """Apply compression per request and register responses for context cleanup."""

    client: Client
    compress: bool
    responses: ExitStack

    def _request(self, method: str, path: str, json: object = None) -> Response:
        """Send a value request using the negotiated compression."""
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
        return response

    def get(self, path: str) -> Response:
        """Get values using the negotiated response encoding."""
        return self._request("GET", path)

    def post(self, path: str, *, json: object) -> Response:
        """Post JSON, compressing its bytes when enabled."""
        return self._request("POST", path, json=json)
