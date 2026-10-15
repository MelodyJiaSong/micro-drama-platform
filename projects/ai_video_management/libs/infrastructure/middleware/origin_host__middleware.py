"""Origin/Host gate for every write, plus security headers on every response.

The rule itself (which methods are checked, the CSP value, the bound origin's
allow lists) lives in `libs.common.origin`; this module only applies it.
"""
from __future__ import annotations

import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp

from libs.common.origin import CSP_HEADER, BoundOrigin, is_guarded

logger = logging.getLogger("ai_video_management.api_security")


class OriginHostMiddleware(BaseHTTPMiddleware):
    """Refuse a write unless it demonstrably comes from this app (follow-up 239).

    Applies to every method except GET/HEAD/OPTIONS (`is_guarded`):

    * `Host` must name the bound loopback address. A DNS-rebinding page reaches
      127.0.0.1 under its own hostname and sends that hostname here.
    * `Origin` must be present and be the app's own origin (validation/security.md
      SEC-ORIGIN-HOST-01/02). Browsers attach it to every non-GET/HEAD request,
      cross-site ones included; a sandboxed frame or a file:// page sends `null`,
      refused like any other foreign value. A local script that writes through
      the API sets the app's own Origin explicitly; a request without one is
      refused rather than guessed to be local.

    The Vite dev server's origin is deliberately not on the list: its proxy
    rewrites the Origin of the dev page's own requests to the backend's
    (`apps/ui/devProxyOrigin.ts`), so both runtime modes arrive in the same
    shape, and anything else it relays keeps its foreign Origin.
    """

    def __init__(self, app: ASGIApp, bound: BoundOrigin) -> None:
        super().__init__(app)
        self._origin_allow: frozenset[str] = bound.origin_allow_list()
        self._host_allow: frozenset[str] = bound.host_allow_list()

    async def dispatch(self, request: Request, call_next):  # type: ignore[no-untyped-def]
        method = request.method.upper()
        if is_guarded(method):
            origin = request.headers.get("origin")
            host = request.headers.get("host")
            if host not in self._host_allow:
                return self._blocked("host", method, request, origin, host)
            if origin is None or origin not in self._origin_allow:
                return self._blocked("origin", method, request, origin, host)
        return await call_next(request)

    @staticmethod
    def _blocked(reason: str, method: str, request: Request, origin: str | None, host: str | None) -> JSONResponse:
        logger.warning(
            "origin_host_403",
            extra={
                "kind": "origin_host_403",
                "reason": reason,
                "method": method,
                "path": request.scope.get("path", ""),
                "origin": origin,
                "host": host,
            },
        )
        return JSONResponse(status_code=403, content={"detail": {"kind": "origin_blocked"}})


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Attach CSP + X-Content-Type-Options + Referrer-Policy on every response."""

    async def dispatch(self, request: Request, call_next):  # type: ignore[no-untyped-def]
        response = await call_next(request)
        response.headers.setdefault("Content-Security-Policy", CSP_HEADER)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        return response
