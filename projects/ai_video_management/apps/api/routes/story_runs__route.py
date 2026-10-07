from __future__ import annotations

from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from apps.api.container import Container
from libs.application.dtos.story_runs__dto import StoryRunsQdto
from libs.application.queries.story_runs__query import StoryRunsQuery

router = APIRouter()


@router.get("/api/story-runs")
@inject
def read_runs(episode_path: str = Query(...),
              query: StoryRunsQuery = Depends(Provide[Container.story_runs_query])) -> StoryRunsQdto:
    return query.read(episode_path)


@router.get("/api/story-runs/detail")
@inject
def read_run(episode_path: str = Query(...), run_id: str = Query(...),
             query: StoryRunsQuery = Depends(Provide[Container.story_runs_query])) -> dict[str, Any]:
    return query.detail(episode_path, run_id)
