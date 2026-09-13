"""Research routes: read-only browsing of the ai_videos/_research/ datasets.

Datasets are produced offline (tools/yt_research.py + a research run) — there is
deliberately no write or re-run endpoint here, so the webapp can never fabricate
metrics it did not measure.
"""
from __future__ import annotations

from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from apps.api.container import Container
from libs.application.commands.research__command import ResearchCommand
from libs.application.queries.research__query import ResearchQuery
from libs.infrastructure.errors.research__error import ResearchError

router = APIRouter()


class SeriesMarkBody(BaseModel):
    status: str | None = None
    rating: int | None = None
    note: str | None = None


class VideoMarkBody(BaseModel):
    bookmarked: bool | None = None
    note: str | None = None


def _error(exc: ResearchError) -> Response:
    status = 404 if exc.kind == "not_found" else 400
    return JSONResponse(
        status_code=status, content={"detail": {"kind": exc.kind, "message": str(exc)}}
    )


@router.get("/api/research/datasets")
@inject
def research_datasets(
    query: ResearchQuery = Depends(Provide[Container.research_query]),
) -> Any:
    return query.datasets()


@router.get("/api/research/dataset/{dataset}")
@inject
def research_dataset(
    dataset: str, query: ResearchQuery = Depends(Provide[Container.research_query])
) -> Any:
    try:
        return query.dataset(dataset)
    except ResearchError as exc:
        return _error(exc)


@router.get("/api/research/dataset/{dataset}/series/{slug}")
@inject
def research_series(
    dataset: str, slug: str, query: ResearchQuery = Depends(Provide[Container.research_query])
) -> Any:
    try:
        return query.series(dataset, slug)
    except ResearchError as exc:
        return _error(exc)


@router.get("/api/research/dataset/{dataset}/workspace")
@inject
def research_workspace(
    dataset: str, query: ResearchQuery = Depends(Provide[Container.research_query])
) -> Any:
    try:
        return query.workspace(dataset)
    except ResearchError as exc:
        return _error(exc)


@router.put("/api/research/dataset/{dataset}/series/{slug}/mark")
@inject
def research_mark_series(
    dataset: str,
    slug: str,
    body: SeriesMarkBody,
    command: ResearchCommand = Depends(Provide[Container.research_command]),
) -> Any:
    try:
        return command.mark_series(dataset, slug, body.status, body.rating, body.note)
    except ResearchError as exc:
        return _error(exc)


@router.put("/api/research/dataset/{dataset}/video/{video_id}/mark")
@inject
def research_mark_video(
    dataset: str,
    video_id: str,
    body: VideoMarkBody,
    command: ResearchCommand = Depends(Provide[Container.research_command]),
) -> Any:
    try:
        return command.mark_video(dataset, video_id, body.bookmarked, body.note)
    except ResearchError as exc:
        return _error(exc)
