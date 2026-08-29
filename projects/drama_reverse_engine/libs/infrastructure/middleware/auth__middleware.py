from __future__ import annotations

import hmac
import os

from starlette.requests import Request
from starlette.responses import JSONResponse

_PUBLIC_PATHS = ("/api/health",)


async def token_auth_middleware(request: Request, call_next):
    """SEC-06/07: token required on every /api path except health when DRE_API_TOKEN is
    set; constant-time compare; the token value itself is never logged or echoed."""
    token = os.environ.get("DRE_API_TOKEN", "")
    path = request.url.path
    if token and path.startswith("/api") and path not in _PUBLIC_PATHS:
        supplied = request.headers.get("x-api-token", "")
        if not hmac.compare_digest(supplied.encode(), token.encode()):
            return JSONResponse({"detail": "unauthorized"}, status_code=401)
    return await call_next(request)
