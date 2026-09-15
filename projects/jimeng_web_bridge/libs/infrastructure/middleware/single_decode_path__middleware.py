from __future__ import annotations

from urllib.parse import unquote

from starlette.types import ASGIApp, Receive, Scope, Send


class SingleDecodePathMiddleware:
    """Rebuilds `scope["path"]` as exactly one percent-decode of `raw_path`.

    The request gate and every `{…:path}` parameter are judged on this value, so a transport that
    decodes twice (Starlette's TestClient turns `%252F` into `/`) cannot smuggle a second decode
    past the path sandbox. Under uvicorn this is a no-op: it already decodes `raw_path` once.
    """

    def __init__(self, app: ASGIApp) -> None:
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        raw_path = scope.get("raw_path") if scope["type"] in ("http", "websocket") else None
        if isinstance(raw_path, bytes) and raw_path:
            scope = {**scope, "path": unquote(raw_path.split(b"?", 1)[0].decode("latin-1"), encoding="utf-8")}
        await self._app(scope, receive, send)
