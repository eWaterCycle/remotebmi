import zstandard
from starlette.datastructures import CommaSeparatedStrings, Headers, MutableHeaders
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send


def decompress_body(body: bytes) -> bytes:
    decompressor = zstandard.ZstdDecompressor().decompressobj()
    result = decompressor.decompress(body)
    if not decompressor.eof or decompressor.unused_data:
        msg = "Incomplete zstd frame or trailing data."
        raise zstandard.ZstdError(msg)
    return result


class ValueCompressionMiddleware:
    """Decompress value requests and compress responses around validation."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def _decompress_request(
        self, scope: Scope, receive: Receive, send: Send
    ) -> tuple[Scope, Receive] | None:
        encoding = (
            ",".join(Headers(scope=scope).getlist("content-encoding")).strip().lower()
        )
        if encoding not in {"", "identity", "zstd"}:
            response = JSONResponse(
                {
                    "status": 415,
                    "detail": "Unsupported Content-Encoding; use zstd or identity.",
                },
                status_code=415,
            )
            await response(scope, receive, send)
            return None
        if encoding:
            scope = {**scope, "headers": list(scope["headers"])}
            headers = MutableHeaders(scope=scope)
            del headers["content-encoding"]
        if encoding == "zstd":
            body = await Request(scope, receive).body()
            try:
                body = decompress_body(body)
            except zstandard.ZstdError:
                response = JSONResponse(
                    {"status": 400, "detail": "Invalid zstd request body."},
                    status_code=400,
                )
                await response(scope, receive, send)
                return None
            headers["content-length"] = str(len(body))
            original_receive = receive
            delivered = False

            async def receive_body() -> Message:
                nonlocal delivered
                if delivered:
                    return await original_receive()
                delivered = True
                return {"type": "http.request", "body": body, "more_body": False}

            receive = receive_body
        return scope, receive

    async def _compress_response(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        compress = any(
            encoding.lower() == "zstd"
            for value in Headers(scope=scope).getlist("accept-encoding")
            for encoding in CommaSeparatedStrings(value)
        )
        start: Message | None = None

        async def send_response(message: Message) -> None:
            nonlocal start
            if message["type"] == "http.response.start":
                headers = Headers(raw=message["headers"])
                if (
                    message["status"] == 200
                    and headers.get("content-type", "").split(";")[0]
                    in {"application/json", "application/octet-stream"}
                    and "content-encoding" not in headers
                ):
                    start = message
                    return
            elif start is not None:
                # get_value returns one JSON body; pass streaming responses through.
                if message["type"] == "http.response.body" and not message.get(
                    "more_body", False
                ):
                    headers = MutableHeaders(scope=start)
                    headers.add_vary_header("Accept-Encoding")
                    body = message.get("body", b"")
                    if compress:
                        body = zstandard.ZstdCompressor().compress(body)
                        message = {**message, "body": body}
                        headers["Content-Encoding"] = "zstd"
                        headers["Content-Length"] = str(len(body))
                await send(start)
                start = None
            await send(message)

        await self.app(scope, receive, send_response)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        routing = scope.get("extensions", {}).get("connexion_routing", {})
        operation = routing.get("operation_id")
        if scope["type"] != "http" or operation not in {
            "remotebmi.server.api.get_value",
            "remotebmi.server.api.get_value_at_indices",
            "remotebmi.server.api.set_value",
            "remotebmi.server.api.set_value_at_indices",
        }:
            await self.app(scope, receive, send)
            return

        if scope["method"] == "POST" and operation != "remotebmi.server.api.get_value":
            request = await self._decompress_request(scope, receive, send)
            if request is None:
                return
            scope, receive = request

        if operation not in {
            "remotebmi.server.api.get_value",
            "remotebmi.server.api.get_value_at_indices",
        }:
            await self.app(scope, receive, send)
            return

        await self._compress_response(scope, receive, send)
