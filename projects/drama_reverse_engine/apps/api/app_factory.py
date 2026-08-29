from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.staticfiles import StaticFiles

from apps.api.container import Container
from apps.api.routes import router
from libs.infrastructure.middleware.auth__middleware import token_auth_middleware

_UI_DIST = Path(__file__).resolve().parent.parent / "ui" / "dist"


def create_app(serve_static: bool = False, container: Container | None = None) -> FastAPI:
    container = container or Container()
    app = FastAPI(title="drama_reverse_engine", docs_url="/api/docs", openapi_url="/api/openapi.json")
    app.state.container = container
    app.add_middleware(BaseHTTPMiddleware, dispatch=token_auth_middleware)
    app.include_router(router)
    if serve_static and _UI_DIST.is_dir():
        app.mount("/", StaticFiles(directory=str(_UI_DIST), html=True), name="ui")
    return app
