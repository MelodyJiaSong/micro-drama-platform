
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from pydantic import BaseModel

from libs.application.commands.drama__command import DramaCommand
from libs.application.queries.drama__query import DramaQuery
from libs.domain.errors.workspace__error import WorkspaceError
from libs.infrastructure.errors.ffmpeg__error import FfmpegError

router = APIRouter()

_UPLOAD_CHUNK = 1024 * 1024


class CreateDramaBody(BaseModel):
    drama_id: str
    title: str
    declaration_accepted: bool
    declared_by: str
    declaration_version: str = "v1"
    gate_a_enabled: bool = False
    gate_b_enabled: bool = False


@router.post("/api/dramas")
@inject
def create_drama(body: CreateDramaBody, command: DramaCommand = Depends(Provide["drama_command"])):
    if "/" in body.drama_id or "\\" in body.drama_id or not body.drama_id.isascii():
        raise HTTPException(status_code=400, detail="drama_id must be a plain ASCII slug")
    try:
        result = command.create(body.drama_id, body.title, body.declaration_accepted,
                                body.declared_by, body.declaration_version,
                                body.gate_a_enabled, body.gate_b_enabled)
    except WorkspaceError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"drama_id": result.drama_id, "title": result.title}


@router.get("/api/dramas")
@inject
def list_dramas(query: DramaQuery = Depends(Provide["drama_query"])):
    return {"dramas": [
        {"drama_id": d.drama_id, "title": d.title,
         "gate_a_enabled": d.gate_a_enabled, "gate_b_enabled": d.gate_b_enabled,
         "children": [
             {"episode_rel_dir": e.episode_rel_dir, "stage": e.stage, "failed_reason": e.failed_reason,
              "gate_hold": e.gate_hold, "busy": e.busy, "shot_count": e.shot_count,
              "degradations": e.degradations, "artifacts": e.artifacts}
             for e in d.children
         ]}
        for d in query.tree()
    ]}


@router.post("/api/uploads")
@inject
async def upload_new_drama(
    file: UploadFile,
    declaration_accepted: bool = Form(False),
    declared_by: str = Form("operator"),
    title: str = Form(""),
    command: DramaCommand = Depends(Provide["drama_command"]),
):
    """Follow-up 003: upload-first — one upload creates one new entry (drama)."""
    if not (file.filename or "").lower().endswith((".mp4", ".mov")):
        raise HTTPException(status_code=400, detail="only mp4/mov accepted")

    async def _stream():
        while chunk := await file.read(_UPLOAD_CHUNK):
            yield chunk

    try:
        drama_id, final_title, episodes = await command.create_and_upload(
            file.filename or "upload.mp4", title, declaration_accepted, declared_by, _stream())
    except WorkspaceError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except FfmpegError as exc:
        raise HTTPException(status_code=400, detail=f"upload rejected: {exc}")
    return {"drama_id": drama_id, "title": final_title, "episodes": episodes}


@router.post("/api/dramas/{drama_id}/upload")
@inject
async def upload_source(
    drama_id: str,
    file: UploadFile,
    command: DramaCommand = Depends(Provide["drama_command"]),
):
    if not (file.filename or "").lower().endswith((".mp4", ".mov")):
        raise HTTPException(status_code=400, detail="only mp4/mov accepted")

    async def _stream():
        while chunk := await file.read(_UPLOAD_CHUNK):
            yield chunk

    try:
        episodes = await command.stream_upload(drama_id, file.filename or "upload.mp4", _stream())
    except WorkspaceError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except FfmpegError as exc:
        raise HTTPException(status_code=400, detail=f"upload rejected: {exc}")
    return {"episodes": episodes}
