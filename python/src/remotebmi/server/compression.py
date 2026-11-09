import zstandard
from starlette.datastructures import CommaSeparatedStrings, Headers, MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class GetValueCompressionMiddleware:
    """Compress get_value JSON responses when explicitly accepting zstd."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        routing = scope.get("extensions", {}).get("connexion_routing", {})
        if (
            scope["type"] != "http"
            or scope["method"] != "GET"
            or routing.get("operation_id") != "remotebmi.server.api.get_value"
        ):
            await self.app(scope, receive, send)
            return

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
                    == "application/json"
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
