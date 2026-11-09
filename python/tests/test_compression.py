import asyncio
from copy import deepcopy

import pytest
from starlette.types import Message, Receive, Scope, Send

from remotebmi.server.compression import GetValueCompressionMiddleware


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
    asyncio.run(GetValueCompressionMiddleware(app)(scope, receive, send))

    assert sent == expected
