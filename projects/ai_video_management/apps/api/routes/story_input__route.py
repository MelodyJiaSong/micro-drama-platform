from __future__ import annotations

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from apps.api.container import Container
from libs.application.dtos.story_input__dto import StoryInputQdto
from libs.application.queries.story_input__query import StoryInputQuery

router = APIRouter()


@router.get("/api/story-input")
@inject
def read_input(episode_path: str = Query(...), profile_id: str | None = Query(None),
               query: StoryInputQuery = Depends(Provide[Container.story_input_query])) -> StoryInputQdto:
    return query.read(episode_path, profile_id)
