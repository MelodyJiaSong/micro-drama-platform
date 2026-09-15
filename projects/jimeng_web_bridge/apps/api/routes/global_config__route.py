from typing import Annotated, Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from apps.api.container import Container
from apps.api.routes._helpers import require_ui, to_json
from libs.application.commands.global_config__command import GlobalConfigCommand
from libs.application.queries.global_config__query import GlobalConfigQuery

router = APIRouter()


class SaveGlobalConfigBody(BaseModel):
    data: dict[str, Any] | None = None
    text: str | None = None
    expected_sha256: str | None = None


@router.get("/api/config/global")
@inject
def get_global_config(query: Annotated[GlobalConfigQuery, Depends(Provide[Container.global_config_query])]) -> object:
    return to_json(query.get())


@router.put("/ui-api/config/global")
@inject
def save_global_config(
    request: Request,
    body: SaveGlobalConfigBody,
    command: Annotated[GlobalConfigCommand, Depends(Provide[Container.global_config_command])],
) -> object:
    require_ui(request)
    return to_json(command.save(body.data, body.text, body.expected_sha256))
