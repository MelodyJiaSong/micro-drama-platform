"""Mux routes: the /tools page's BGM-mux utility.

`POST /api/mux/bgm` takes a video upload + an audio upload, writes the muxed MP4
to the importer's watch folder, and streams it back. Uploads never enter the repo
tree (see `mux__writer`), so this route sits outside the EXPOSED_TREE path sandbox
by construction rather than by carving a hole in it.

The saved file's absolute path rides back in the `X-Output-Path` header,
percent-encoded: HTTP header values are latin-1, and these paths are routinely
Chinese. The client decodes it with `decodeURIComponent`.
"""
from __future__ import annotations

from urllib.parse import quote

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import FileResponse, JSONResponse, Response

from apps.api.container import Container
from libs.application.commands.mux__command import MuxCommand
from libs.application.dtos.mux__dto import MuxOptions
from libs.infrastructure.errors.mux__error import MuxError

router = APIRouter()


def _error(exc: MuxError) -> Response:
    status = 400 if exc.kind == "unsupported_media" else 500
    return JSONResponse(
        status_code=status, content={"detail": {"kind": exc.kind, "message": str(exc)}}
    )


@router.post("/api/mux/bgm")
@inject
def mux_bgm(
    video: UploadFile = File(...),
    audio: UploadFile = File(...),
    bgm_volume: float = Form(0.6),
    no_loop: bool = Form(False),
    keep_source_audio: bool = Form(False),
    source_volume: float = Form(1.0),
    duck_source: bool = Form(False),
    bgm_start: float = Form(0.0),
    fade_in: float = Form(0.0),
    fade_out: float = Form(0.0),
    command: MuxCommand = Depends(Provide[Container.mux_command]),
) -> Response:
    # `def`, not `async def`: the mux is a blocking ffmpeg run, so FastAPI hands
    # it to the threadpool instead of stalling the event loop.
    options = MuxOptions(
        bgm_volume=bgm_volume,
        no_loop=no_loop,
        keep_source_audio=keep_source_audio,
        source_volume=source_volume,
        duck_source=duck_source,
        bgm_start=bgm_start,
        fade_in=fade_in,
        fade_out=fade_out,
    )
    try:
        result = command.add_bgm(
            video.filename or "", video.file, audio.filename or "", audio.file, options
        )
    except MuxError as exc:
        return _error(exc)
    return FileResponse(
        result.output,
        media_type="video/mp4",
        filename=result.download_name,
        headers={"X-Output-Path": quote(str(result.output))},
    )
