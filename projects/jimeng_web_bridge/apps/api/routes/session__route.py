from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from apps.api.container import Container
from apps.api.routes._helpers import to_json
from libs.application.commands.session__command import SessionCommand
from libs.application.dtos.session__dto import HealthQdto
from libs.application.queries.session__query import SessionQuery

router = APIRouter()


@router.get("/api/health")
@inject
def health(query: Annotated[SessionQuery, Depends(Provide[Container.session_query])]) -> HealthQdto:
    return query.health()


@router.get("/api/session")
@inject
def session_status(query: Annotated[SessionQuery, Depends(Provide[Container.session_query])]) -> object:
    return to_json(query.status())


@router.post("/api/session/browser/open")
@inject
def open_browser(command: Annotated[SessionCommand, Depends(Provide[Container.session_command])]) -> object:
    return to_json(command.open_browser())
