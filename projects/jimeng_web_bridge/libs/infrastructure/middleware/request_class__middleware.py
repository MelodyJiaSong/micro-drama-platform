from __future__ import annotations

import hmac
import json
import logging
from dataclasses import dataclass
from http.cookies import CookieError, SimpleCookie

from starlette.types import ASGIApp, Receive, Scope, Send

logger = logging.getLogger("jimeng_web_bridge.security")

UI_SESSION_COOKIE: str = "jwb_ui"
REQUEST_CLASS_KEY: str = "request_class"
PUBLIC: str = "public"
BEARER: str = "bearer"
UI: str = "ui"

_SAFE_METHODS: frozenset[str] = frozenset({"GET", "HEAD"})


@dataclass(frozen=True)
class RequestGatePolicy:
    host_allow: frozenset[str]
    origin_allow: frozenset[str]
    bearer_token: str
    ui_session: str
    public_get_paths: frozenset[str] = frozenset({"/", "/index.html", "/api/health", "/favicon.ico"})
    public_get_prefixes: tuple[str, ...] = ("/assets/",)

    @classmethod
    def for_local(cls, port: int, bearer_token: str, ui_session: str) -> RequestGatePolicy:
        hosts = frozenset({f"127.0.0.1:{port}", f"localhost:{port}"})
        return cls(
            host_allow=hosts,
            origin_allow=frozenset(f"http://{host}" for host in hosts),
            bearer_token=bearer_token,
            ui_session=ui_session,
        )


class RequestClassMiddleware:
    """Decides who is calling before any route runs (spec v2 NFR 安全 identity table).

    A bearer caller (MCP / scripts) is never allowed onto `/ui-api/*`, which is where
    confirmation and every other human-only action lives; `/mcp` never accepts the
    browser identity.
    """

    def __init__(self, app: ASGIApp, policy: RequestGatePolicy) -> None:
        self._app = app
        self._policy = policy

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "lifespan":
            await self._app(scope, receive, send)
            return
        verdict = self._classify(scope) if scope["type"] == "http" else None
        if verdict is None:
            await self._deny(scope, send)
            return
        scope.setdefault("state", {})[REQUEST_CLASS_KEY] = verdict
        await self._app(scope, receive, send)

    def _classify(self, scope: Scope) -> str | None:
        headers = _headers(scope)
        if headers.get("host") not in self._policy.host_allow:
            return None
        path: str = scope.get("path", "")
        method: str = str(scope.get("method", "GET")).upper()
        authorization = headers.get("authorization")
        if authorization is not None:
            if not self._bearer_ok(authorization) or path.startswith("/ui-api/"):
                return None
            return BEARER
        if path == "/mcp" or path.startswith("/mcp/"):
            return None
        if method in _SAFE_METHODS and self._is_public(path):
            return PUBLIC
        if headers.get("sec-fetch-site") != "same-origin":
            return None
        cookie = _cookie_value(headers.get("cookie"), UI_SESSION_COOKIE)
        if cookie is None or not hmac.compare_digest(cookie.encode(), self._policy.ui_session.encode()):
            return None
        if method not in _SAFE_METHODS and headers.get("origin") not in self._policy.origin_allow:
            return None
        return UI

    def _bearer_ok(self, authorization: str) -> bool:
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer" or not token:
            return False
        return hmac.compare_digest(token.strip().encode(), self._policy.bearer_token.encode())

    def _is_public(self, path: str) -> bool:
        if path in self._policy.public_get_paths or path.startswith(self._policy.public_get_prefixes):
            return True
        # SPA deep links (/queue, /batches/b1) only ever return the HTML shell, which is also what
        # hands the browser its session cookie; data stays behind /api, /ui-api and /mcp.
        return not path.startswith(("/api/", "/ui-api/", "/mcp"))

    async def _deny(self, scope: Scope, send: Send) -> None:
        logger.warning(
            "request_denied",
            extra={"kind": "request_denied", "path": scope.get("path"), "method": scope.get("method")},
        )
        if scope["type"] != "http":
            await send({"type": "websocket.close", "code": 1008})
            return
        body = json.dumps(
            {"error_code": "forbidden", "message": "request not allowed from this client", "hint": None}
        ).encode()
        await send(
            {
                "type": "http.response.start",
                "status": 403,
                "headers": [(b"content-type", b"application/json"), (b"content-length", str(len(body)).encode())],
            }
        )
        await send({"type": "http.response.body", "body": body})


def _headers(scope: Scope) -> dict[str, str]:
    return {key.decode("latin-1").lower(): value.decode("latin-1") for key, value in scope.get("headers", [])}


def _cookie_value(raw: str | None, name: str) -> str | None:
    if raw is None:
        return None
    jar = SimpleCookie()
    try:
        jar.load(raw)
    except CookieError:
        return None
    morsel = jar.get(name)
    return morsel.value if morsel is not None else None
