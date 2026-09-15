from typing import Annotated, Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from apps.api.container import Container
from apps.api.routes._helpers import to_json
from libs.application.commands.drama_config__command import DramaConfigCommand
from libs.application.queries.drama_config__query import DramaConfigQuery

router = APIRouter()


class SaveConfigBody(BaseModel):
    data: dict[str, Any] | None = None
    text: str | None = None
    expected_sha256: str | None = None


@router.get("/api/dramas")
@inject
def list_dramas(query: Annotated[DramaConfigQuery, Depends(Provide[Container.drama_config_query])]) -> object:
    return to_json(query.list_dramas())


@router.get("/api/dramas/{drama:path}/config")
@inject
def get_config(drama: str, query: Annotated[DramaConfigQuery, Depends(Provide[Container.drama_config_query])]) -> object:
    return to_json(query.get(drama))


@router.post("/api/dramas/{drama:path}/config/propose")
@inject
def propose_config(
    drama: str, command: Annotated[DramaConfigCommand, Depends(Provide[Container.drama_config_command])]
) -> object:
    return to_json(command.propose(drama))


@router.put("/api/dramas/{drama:path}/config")
@inject
def save_config(
    drama: str,
    body: SaveConfigBody,
    command: Annotated[DramaConfigCommand, Depends(Provide[Container.drama_config_command])],
) -> object:
    return to_json(command.save(drama, body.data, body.text, body.expected_sha256))
