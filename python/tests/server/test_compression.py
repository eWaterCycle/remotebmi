import asyncio
from copy import deepcopy

import pytest
import zstandard
from starlette.datastructures import Headers
from starlette.types import Message, Receive, Scope, Send

from remotebmi.server.compression import ValueCompressionMiddleware


@pytest.mark.parametrize(
    "status, headers, body_messages",
    [
        pytest.param(
            500,
            [(b"content-type", b"application/json"), (b"vary", b"Origin")],
            [{"type": "http.response.body", "body": b"error"}],
            id="error",
        ),
        pytest.param(
            200,
            [(b"content-type", b"text/plain"), (b"vary", b"Origin")],
            [{"type": "http.response.body", "body": b"text"}],
            id="non-json",
        ),
        pytest.param(
            200,
            [
                (b"content-type", b"application/json"),
                (b"vary", b"Origin"),
                (b"content-encoding", b"gzip"),
            ],
            [{"type": "http.response.body", "body": b"encoded"}],
            id="already-encoded",
        ),
        pytest.param(
            200,
            [(b"content-type", b"application/json"), (b"vary", b"Origin")],
            [
                {"type": "http.response.body", "body": b"first", "more_body": True},
                {"type": "http.response.body", "body": b"last"},
            ],
            id="streaming",
        ),
    ],
)
def test_response_passthrough(
    status: int, headers: list[tuple[bytes, bytes]], body_messages: list[Message]
) -> None:
    messages: list[Message] = [
        {"type": "http.response.start", "status": status, "headers": headers},
        *body_messages,
    ]
    expected = deepcopy(messages)
    sent: list[Message] = []

    async def app(scope: Scope, receive: Receive, send: Send) -> None:
        for message in messages:
            await send(message)

    async def receive() -> Message:
        return {"type": "http.request"}

    async def send(message: Message) -> None:
        sent.append(message)

    scope: Scope = {
        "type": "http",
        "method": "GET",
        "headers": [(b"accept-encoding", b"zstd")],
        "extensions": {
            "connexion_routing": {"operation_id": "remotebmi.server.api.get_value"}
        },
    }
    asyncio.run(ValueCompressionMiddleware(app)(scope, receive, send))

    assert sent == expected


class TestRequestDecompression:
    @pytest.mark.parametrize(
        "operation", ["get_value_at_indices", "set_value", "set_value_at_indices"]
    )
    def test_chunked_binary_body(self, operation: str) -> None:
        body = b"\x00\x01\x80\xff"
        compressed = zstandard.ZstdCompressor().compress(body)
        incoming = iter(
            [
                {"type": "http.request", "body": compressed[:4], "more_body": True},
                {"type": "http.request", "body": compressed[4:], "more_body": False},
            ]
        )
        actual: dict[str, object] = {}

        async def app(scope: Scope, receive: Receive, send: Send) -> None:
            message = await receive()
            actual.update(headers=dict(Headers(scope=scope)), body=message)

        async def receive() -> Message:
            return next(incoming)

        async def send(message: Message) -> None:
            pass

        scope: Scope = {
            "type": "http",
            "method": "POST",
            "headers": [
                (b"content-type", b"application/octet-stream"),
                (b"content-encoding", b"zstd"),
                (b"content-length", str(len(compressed)).encode()),
            ],
            "extensions": {
                "connexion_routing": {
                    "operation_id": f"remotebmi.server.api.{operation}"
                }
            },
        }
        asyncio.run(ValueCompressionMiddleware(app)(scope, receive, send))
        assert actual == {
            "headers": {
                "content-type": "application/octet-stream",
                "content-length": "4",
            },
            "body": {"type": "http.request", "body": body, "more_body": False},
        }


class TestResponseCompression:
    def test_binary_response_preserves_headers(self) -> None:
        body = b"\x00\x01\x80\xff"
        messages: list[Message] = [
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [
                    (b"content-type", b"application/octet-stream"),
                    (b"content-length", str(len(body)).encode()),
                    (b"vary", b"Origin"),
                ],
            },
            {"type": "http.response.body", "body": body},
        ]
        sent: list[Message] = []

        async def app(scope: Scope, receive: Receive, send: Send) -> None:
            for message in messages:
                await send(message)

        async def receive() -> Message:
            return {"type": "http.request"}

        async def send(message: Message) -> None:
            sent.append(message)

        scope: Scope = {
            "type": "http",
            "method": "GET",
            "headers": [(b"accept-encoding", b"zstd")],
            "extensions": {
                "connexion_routing": {"operation_id": "remotebmi.server.api.get_value"}
            },
        }
        asyncio.run(ValueCompressionMiddleware(app)(scope, receive, send))
        assert {
            "status": sent[0]["status"],
            "headers": dict(Headers(raw=sent[0]["headers"])),
            "body": zstandard.ZstdDecompressor().decompress(sent[1]["body"]),
        } == {
            "status": 200,
            "headers": {
                "content-type": "application/octet-stream",
                "content-length": str(len(sent[1]["body"])),
                "content-encoding": "zstd",
                "vary": "Origin, Accept-Encoding",
            },
            "body": body,
        }
