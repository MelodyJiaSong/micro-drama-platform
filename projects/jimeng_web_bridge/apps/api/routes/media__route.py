from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from apps.api.container import Container
from libs.application.queries.artifact__query import ArtifactQuery
from libs.application.queries.thumbnail__query import ThumbnailQuery

router = APIRouter()


@router.get("/api/thumbs")
@inject
def thumbnail(
    path: str,
    query: Annotated[ThumbnailQuery, Depends(Provide[Container.thumbnail_query])],
    max_edge: int | None = None,
) -> FileResponse:
    thumb = query.get(path, max_edge)
    return FileResponse(thumb.file_path, media_type=thumb.content_type, headers={"Cache-Control": "private, max-age=300"})


@router.get("/api/artifacts/{job_id}/{name}")
@inject
def screenshot(
    job_id: str, name: str, query: Annotated[ArtifactQuery, Depends(Provide[Container.artifact_query])]
) -> FileResponse:
    artifact = query.get_screenshot(job_id, name)
    return FileResponse(artifact.file_path, media_type=artifact.content_type, headers={"Cache-Control": "no-store"})
