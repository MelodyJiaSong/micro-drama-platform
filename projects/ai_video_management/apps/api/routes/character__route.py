"""Character-aggregate read routes: GET /api/character-videos — newest
turntable mp4 per character, powering the gallery tile preview; GET
/api/character-reel — one card's 样片与正片 (follow-up 286)."""
from __future__ import annotations

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse, Response

from apps.api.container import Container
from libs.application.dtos.character_reel__dto import CharacterReelQdto
from libs.application.queries.character__query import CharacterQuery
from libs.application.queries.character_reel__query import CharacterReelQuery

router = APIRouter()


@router.get("/api/character-videos")
@inject
def character_videos(
    path: str = Query(...),
    query: CharacterQuery = Depends(Provide[Container.character_query]),
) -> Response:
    return JSONResponse(
        status_code=200, content=query.list_latest_videos(path).to_payload()
    )


@router.get("/api/character-reel")
@inject
def character_reel(path: str = Query(...),
                   query: CharacterReelQuery = Depends(Provide[Container.character_reel_query])) -> CharacterReelQdto:
    return query.read(path)
