"""Previz routes: POST /api/previz/render, POST /api/previz/cancel, GET /api/previz/status.

Render is a 15–30 minute job, so POST only *starts* it and returns the opening
snapshot; the UI polls GET /api/previz/status until the state is terminal.
"""
from __future__ import annotations

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from apps.api.container import Container
from libs.application.commands.previz__command import PrevizCommand
from libs.application.queries.previz__query import PrevizQuery

router = APIRouter()


class PrevizBody(BaseModel):
    path: str


@router.post("/api/previz/render")
@inject
def render_previz(
    body: PrevizBody,
    command: PrevizCommand = Depends(Provide[Container.previz_command]),
) -> Response:
    return JSONResponse(status_code=202, content=command.render(body.path).to_payload())


@router.post("/api/previz/cancel")
@inject
def cancel_previz(
    body: PrevizBody,
    command: PrevizCommand = Depends(Provide[Container.previz_command]),
) -> Response:
    return JSONResponse(status_code=200, content=command.cancel(body.path).to_payload())


@router.get("/api/previz/status")
@inject
def previz_status(
    path: str = Query(...),
    query: PrevizQuery = Depends(Provide[Container.previz_query]),
) -> Response:
    return JSONResponse(status_code=200, content=query.status(path).to_payload())
