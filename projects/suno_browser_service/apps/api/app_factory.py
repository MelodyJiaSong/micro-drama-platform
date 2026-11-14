from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
import asyncio
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware

from projects.suno_browser_service.apps.api.container import Container
from projects.suno_browser_service.apps.api.routes import job__route, router
from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.infrastructure.clients.manual_browser__client import window_open


def create_app(container: Container | None = None, *, worker: bool = True) -> FastAPI:
    dependencies = container or Container()
    dependencies.wire(modules=[job__route])

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        dependencies.auth()
        # Initialize database-backed providers before concurrent HTTP requests arrive.
        dependencies.query()
        dependencies.command()
        if worker:
            dependencies.runtime().start()
        try:
            yield
        finally:
            if worker:
                runtime = dependencies.runtime()
                await asyncio.to_thread(runtime.stop)
                while runtime.thread and runtime.thread.is_alive():
                    await asyncio.sleep(0.25)

    app = FastAPI(title="Suno 浏览器服务", version="0.3.0", lifespan=lifespan,
                  description="本机单账号浏览器自动化服务，提供 UI、HTTP、MCP、CLI 共用任务队列。\n\n调用顺序：capabilities → 上传参考（可选）→ plan → jobs → 查询 → 文件下载。所有 /v1 请求需 Bearer token。生成与官方下载可能消耗 Suno 额度；查询、预检和读取本机文件不访问 Suno。\n\n遇 needs_login/needs_attention/uncertain 处理原任务，不换键重提。验证码会暂停整个队列。真实 Suno 新控件及官方下载仍待验收；本机测试不代表付费账号链路已通过。")
    app.state.container = dependencies
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost", "testserver"])

    @app.exception_handler(ServiceError)
    async def error(request: Request, exc: ServiceError) -> JSONResponse:
        return JSONResponse(status_code=exc.status, content={"error": {"code": exc.code, "message": str(exc)}})

    @app.get("/health", tags=["运行状态"], summary="检查本机 worker 与队列暂停状态")
    def health() -> JSONResponse:
        """不需 token。status=ok 只证明本机 worker 存活，不证明 Suno 登录或可生成；automation_paused=true 时可查询但不执行浏览器任务。browser_window=closed 时任务保持排队，运行 open-window.ps1 后继续。"""
        runtime = dependencies.runtime() if worker else None
        healthy = not worker or bool(runtime and runtime.thread and runtime.thread.is_alive() and not runtime.failure)
        settings = dependencies.settings()
        # browser_window: "open"/"closed" for the always-open window (jobs wait queued while closed); "not_used" otherwise.
        window = ("open" if window_open(settings) else "closed") if settings.attached else "not_used"
        return JSONResponse({"status": "ok" if healthy else "worker_stopped", "worker": worker,
                             "automation_paused": bool(runtime and runtime.automation_paused()), "browser_window": window},
                            status_code=200 if healthy else 503)

    app.include_router(router)

    @app.get("/", include_in_schema=False)
    def home() -> RedirectResponse:
        return RedirectResponse("/ui/")

    static = Path(__file__).parent / "static"
    if static.is_dir():
        app.mount("/ui", StaticFiles(directory=static, html=True), name="ui")
    else:
        @app.get("/ui/", include_in_schema=False)
        def ui_unbuilt() -> JSONResponse:
            return JSONResponse({"error": "UI 尚未构建；在 apps/ui 运行 npm ci 和 npm run build，或运行 setup.ps1。"}, status_code=503)

    @app.middleware("http")
    async def ui_headers(request: Request, call_next):
        response = await call_next(request)
        if request.url.path.startswith("/ui"):
            response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; media-src 'self' blob:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["Referrer-Policy"] = "no-referrer"
        return response
    return app
