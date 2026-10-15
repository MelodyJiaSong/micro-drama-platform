"""FastAPI app construction.

Per follow-up 114: every aggregate's domain errors are translated to JSON
responses by global `app.exception_handler` registrations here, replacing
the per-endpoint try/except blocks that used to live in each route file.
The shape — `{"detail": {"kind": <slug>, ...}}` — is byte-identical to the
prior behavior; only the place that produces it has moved.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.types import Scope

from apps.api.container import Container
from apps.api.routes import router
from libs.common.global_workflow import GlobalWorkflowError
from libs.domain.errors.episode_workflow__error import EpisodeWorkflowError
from libs.domain.errors.drama__error import (
    DramaNotFoundError,
    InvalidDramaPathError,
)
from libs.domain.errors.character_video__error import (
    AudioExtractFailedError,
    CharacterVideoNotFoundError,
    FfmpegMissingForCharacterVideoError,
    InvalidCharacterVideoPathError,
    InvalidCharactersDirError,
    NotCharacterVideoError,
    ViewExtractFailedError,
)
from libs.domain.errors.downloads__error import DownloadsDirMissingError
from libs.domain.errors.file__error import (
    FileNotInSandboxError,
    FileTooLargeError,
    InvalidBodyEncodingError,
    MissingIfUnmodifiedSinceError,
    StaleWriteError,
    UnsupportedFileExtensionError,
)
from libs.domain.errors.media__error import (
    AlreadyArchivedError,
    AlreadyDeletedError,
    InvalidMediaPathError,
    MediaMoveFailedError,
    MediaNotFoundError,
    MediaTargetExistsError,
    NotInArchiveError,
    NotMediaError,
    NotUnderAiVideosError,
    NotUnderDeletedError,
)
from libs.infrastructure.middleware.origin_host__middleware import (
    OriginHostMiddleware,
    SecurityHeadersMiddleware,
)


def _err(status: int, kind: str, **extras: Any) -> JSONResponse:
    body: dict[str, Any] = {"kind": kind}
    body.update(extras)
    return JSONResponse(status_code=status, content={"detail": body})


# (ErrorClass, status_code, kind, include_message)
_PLAIN: tuple[tuple[type[Exception], int, str, bool], ...] = (
    # drama path (Downloads import / media rename)
    (InvalidDramaPathError, 400, "invalid_drama_path", False),
    (DramaNotFoundError, 404, "not_found", False),
    # character_video
    (InvalidCharacterVideoPathError, 400, "invalid_path", False),
    (InvalidCharactersDirError, 400, "invalid_characters_dir", False),
    (NotCharacterVideoError, 400, "not_a_character_video", False),
    (CharacterVideoNotFoundError, 404, "not_found", False),
    (FfmpegMissingForCharacterVideoError, 500, "ffmpeg_missing", True),
    (ViewExtractFailedError, 500, "view_extract_failed", True),
    (AudioExtractFailedError, 500, "audio_extract_failed", True),
    # downloads
    # (DownloadsDirMissingError handled specially — payload key is `path`, not `message`.)
    # file
    (UnsupportedFileExtensionError, 400, "extension_not_allowed", False),
    (FileTooLargeError, 413, "too_large", False),
    (FileNotInSandboxError, 404, "not_found", False),
    (MissingIfUnmodifiedSinceError, 400, "missing_if_unmodified_since", False),
    (InvalidBodyEncodingError, 400, "invalid_body_encoding", False),
    # media
    (InvalidMediaPathError, 400, "invalid_path", False),
    (NotMediaError, 400, "extension_not_allowed", False),
    (NotUnderAiVideosError, 400, "not_in_ai_videos", False),
    (AlreadyDeletedError, 400, "already_deleted", False),
    (AlreadyArchivedError, 400, "already_archived", False),
    (NotInArchiveError, 400, "not_in_archive", False),
    (NotUnderDeletedError, 400, "not_in_deleted", False),
    (MediaNotFoundError, 404, "not_found", False),
    (MediaMoveFailedError, 500, "move_failed", True),
)


def _make_plain_handler(status: int, kind: str, include_message: bool):
    if include_message:
        def handler(_req: Request, exc: Exception) -> Response:
            return _err(status, kind, message=str(exc))
    else:
        def handler(_req: Request, _exc: Exception) -> Response:
            return _err(status, kind)
    return handler


def _register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(GlobalWorkflowError)
    def _global_workflow_error(_req: Request, exc: GlobalWorkflowError) -> Response:
        return _err(exc.status_code, "global_workflow", message=str(exc))


    @app.exception_handler(EpisodeWorkflowError)
    def _workflow_error(_req: Request, exc: EpisodeWorkflowError) -> Response:
        return _err(exc.status_code, "episode_workflow", message=str(exc))

    for exc_cls, status, kind, include_message in _PLAIN:
        app.add_exception_handler(exc_cls, _make_plain_handler(status, kind, include_message))

    @app.exception_handler(StaleWriteError)
    def _stale_write(_req: Request, exc: StaleWriteError) -> Response:  # type: ignore[unused-function]
        return _err(409, "stale_write", current_mtime=exc.current_mtime)

    @app.exception_handler(MediaTargetExistsError)
    def _media_target_exists(_req: Request, exc: MediaTargetExistsError) -> Response:  # type: ignore[unused-function]
        return _err(409, "target_exists", target=str(exc))

    @app.exception_handler(DownloadsDirMissingError)
    def _downloads_dir_missing(_req: Request, exc: DownloadsDirMissingError) -> Response:  # type: ignore[unused-function]
        return _err(500, "downloads_dir_missing", path=str(exc))

    @app.exception_handler(StarletteHTTPException)
    def _http_exception(_req: Request, exc: StarletteHTTPException) -> Response:  # type: ignore[unused-function]
        if exc.status_code == 405:
            headers = dict(exc.headers or {})
            return JSONResponse(
                status_code=405,
                content={"detail": {"kind": "method_not_allowed"}},
                headers=headers,
            )
        # Fall through to FastAPI's default shape for other HTTPExceptions.
        if isinstance(exc, FastAPIHTTPException):
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
        return JSONResponse(status_code=exc.status_code, content={"detail": str(exc.detail)})


class SpaStaticFiles(StaticFiles):
    """Serve the built bundle, falling back to index.html for client-side routes.

    `StaticFiles(html=True)` only falls back for *directory* paths, so every SPA
    route (`/research`, `/drama`, `/workflow`, …) 404s when opened directly or
    refreshed. The research workspace keeps its tab and open series in the query
    string, so deep links have to resolve for the feature to work at all.

    `/api/*` is deliberately excluded: an unknown API path must stay a JSON 404,
    not silently return the HTML shell — that failure mode is very hard to debug
    from the client side.
    """

    async def get_response(self, path: str, scope: Scope) -> Response:
        try:
            return await super().get_response(path, scope)
        except StarletteHTTPException as exc:
            request_path = str(scope.get("path", ""))
            if exc.status_code != 404 or request_path.startswith("/api/"):
                raise
            return await super().get_response("index.html", scope)


def create_app(container: Container, serve_static: bool = True) -> FastAPI:
    app = FastAPI(title="ai_video_management", openapi_url=None, docs_url=None, redoc_url=None)

    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(OriginHostMiddleware, bound=container.bound_origin())
    _register_exception_handlers(app)
    app.include_router(router)

    if serve_static:
        static_dir = Path(__file__).resolve().parent / "static"
        if static_dir.is_dir():
            app.mount("/", SpaStaticFiles(directory=str(static_dir), html=True), name="static")

    return app
