"""Health-aggregate route: GET /api/health.

Reports which source tree the running process actually loaded. This machine has
two clones of this repo, and a server started from the wrong CWD silently serves
stale writers while still writing into the other clone's data — a failure mode
that cost a full session to identify. One curl now answers it.
"""
from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response

from libs.infrastructure.writers import downloads__writer, media__writer

router = APIRouter()


@router.get("/api/health")
def health() -> Response:
    return JSONResponse(
        status_code=200,
        content={
            "downloads_writer": downloads__writer.__file__,
            "media_writer": media__writer.__file__,
            "has_subject_routing": hasattr(downloads__writer, "_SUBJECT_KEY"),
            "has_multi_view_rename": hasattr(media__writer, "_SINGLE_IMAGE_FOLDER"),
        },
    )
