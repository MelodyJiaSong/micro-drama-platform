"""Character-video aggregate routes: extract a turntable's views + audio + trim."""
from __future__ import annotations

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from apps.api.container import Container
from libs.application.commands.character_video__command import CharacterVideoCommand

router = APIRouter()


class ExtractCharacterViewsBody(BaseModel):
    path: str


class ExtractAllCharacterViewsBody(BaseModel):
    path: str


@router.post("/api/extract-character-views")
@inject
def extract_character_views(
    body: ExtractCharacterViewsBody,
    command: CharacterVideoCommand = Depends(Provide[Container.character_video_command]),
) -> Response:
    return JSONResponse(status_code=200, content=command.extract_views(body.path).to_payload())


@router.post("/api/extract-all-character-views")
@inject
def extract_all_character_views(
    body: ExtractAllCharacterViewsBody,
    command: CharacterVideoCommand = Depends(Provide[Container.character_video_command]),
) -> Response:
    return JSONResponse(
        status_code=200, content=command.extract_all_views(body.path).to_payload()
    )
