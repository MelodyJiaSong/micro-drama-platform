from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from apps.api.container import Container
from apps.api.routes._helpers import to_json
from libs.application.queries.entity__query import EntityQuery

router = APIRouter()


@router.get("/api/entities/reconcile")
@inject
def reconcile(
    query: Annotated[EntityQuery, Depends(Provide[Container.entity_query])], drama: str | None = None
) -> object:
    return to_json(query.reconcile(drama))
