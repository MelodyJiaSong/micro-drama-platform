from __future__ import annotations

from starlette.types import ASGIApp, Message, Receive, Scope, Send

CSP_HEADER: str = (
    "default-src 'self'; "
    "img-src 'self' data: blob:; "
    "style-src 'self' 'unsafe-inline'; "
    "script-src 'self'; "
    "connect-src 'self'; "
    "object-src 'none'; "
    "base-uri 'self'; "
    "frame-ancestors 'none'"
)

_HEADERS: tuple[tuple[bytes, bytes], ...] = (
    (b"content-security-policy", CSP_HEADER.encode()),
    (b"x-content-type-options", b"nosniff"),
    (b"referrer-policy", b"no-referrer"),
    (b"x-frame-options", b"DENY"),
)


class SecurityHeadersMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return

        async def send_with_headers(message: Message) -> None:
            if message["type"] == "http.response.start":
                present = {key.lower() for key, _ in message.get("headers", [])}
                message["headers"] = list(message.get("headers", [])) + [
                    (key, value) for key, value in _HEADERS if key not in present
                ]
            await send(message)

        await self._app(scope, receive, send_with_headers)
