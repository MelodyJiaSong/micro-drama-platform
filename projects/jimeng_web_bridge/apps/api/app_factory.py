"""FastAPI construction: request gate → (MCP | routes | HTML shell).

Order matters: SecurityHeaders wraps everything (headers on 403s too), RequestClass runs before
any route so a bearer client can never reach `/ui-api/*` and `/mcp` never sees the browser identity.
MCP is dispatched by path next to FastAPI rather than mounted inside it, so `/mcp` needs no trailing
slash redirect; its session manager runs inside FastAPI's lifespan.
"""
from __future__ import annotations

import contextlib
from collections.abc import AsyncIterator
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from mcp.server.transport_security import TransportSecuritySettings
from starlette.types import ASGIApp, Receive, Scope, Send

from apps.api.container import Container
from apps.api.error_handlers import register_error_handlers
from apps.api.mcp_tools import build_mcp_server
from apps.api.routes import router
from libs.common.app_settings import AppSettings
from libs.infrastructure.middleware.request_class__middleware import (
    UI_SESSION_COOKIE,
    RequestClassMiddleware,
    RequestGatePolicy,
)
from libs.infrastructure.middleware.security_headers__middleware import SecurityHeadersMiddleware
from libs.infrastructure.middleware.single_decode_path__middleware import SingleDecodePathMiddleware

MCP_PATH: str = "/mcp"


def create_app(settings: AppSettings, container: Container) -> ASGIApp:
    mcp_server = build_mcp_server(container)
    hosts = [f"127.0.0.1:{settings.port}", f"localhost:{settings.port}"]
    mcp_app = mcp_server.streamable_http_app(
        streamable_http_path=MCP_PATH,
        stateless_http=True,
        json_response=False,
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=True,
            allowed_hosts=hosts,
            allowed_origins=[f"http://{host}" for host in hosts],
        ),
    )

    @contextlib.asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        async with mcp_server.session_manager.run():
            yield

    app = FastAPI(title="jimeng_web_bridge", docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan)
    app.state.container = container
    register_error_handlers(app)
    app.include_router(router)
    app.mount("/assets", StaticFiles(directory=settings.static_dir / "assets", check_dir=False), name="assets")
    index = settings.static_dir / "index.html"

    @app.get("/{spa_path:path}", include_in_schema=False)
    def html_shell(spa_path: str) -> Response:
        if spa_path.startswith(("api/", "ui-api/", "mcp", "assets/")):
            return JSONResponse({"error_code": "not_found", "message": "no such endpoint", "hint": None}, status_code=404)
        return _shell_response(index, settings.ui_session)

    dispatched = _PathDispatch(app, mcp_app)
    gated = RequestClassMiddleware(dispatched, RequestGatePolicy.for_local(settings.port, settings.bearer_token, settings.ui_session))
    return SecurityHeadersMiddleware(SingleDecodePathMiddleware(gated))


class _PathDispatch:
    def __init__(self, app: ASGIApp, mcp_app: ASGIApp) -> None:
        self._app = app
        self._mcp_app = mcp_app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        path: str = scope.get("path", "")
        if scope["type"] == "http" and (path == MCP_PATH or path.startswith(MCP_PATH + "/")):
            await self._mcp_app(scope, receive, send)
            return
        await self._app(scope, receive, send)


def _shell_response(index: Path, ui_session: str) -> Response:
    if not index.is_file():
        response: Response = JSONResponse(
            {"error_code": "ui_not_built", "message": "管理网页尚未构建", "hint": "运行 make ui-build"}, status_code=503
        )
    else:
        response = FileResponse(index, media_type="text/html; charset=utf-8", headers={"Cache-Control": "no-store"})
    response.set_cookie(UI_SESSION_COOKIE, ui_session, httponly=True, samesite="strict", path="/")
    return response
