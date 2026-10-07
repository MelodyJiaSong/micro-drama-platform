from __future__ import annotations

from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from apps.api.container import Container
from libs.application.dtos.global_workflow__dto import GlobalWorkflowQdto
from libs.application.queries.global_workflow__query import GlobalWorkflowQuery

router = APIRouter()


@router.get("/api/global-workflow")
@inject
def read_global_workflow(query: GlobalWorkflowQuery = Depends(Provide[Container.global_workflow_query])) -> GlobalWorkflowQdto:
    return query.read()


@router.get("/api/global-workflow/source")
@inject
def read_global_source(source_id: str = Query(...), query: GlobalWorkflowQuery = Depends(Provide[Container.global_workflow_query])) -> dict[str, Any]:
    return query.source(source_id)


@router.get("/api/global-workflow/coverage")
@inject
def read_global_coverage(query: GlobalWorkflowQuery = Depends(Provide[Container.global_workflow_query])) -> dict[str, Any]:
    return query.coverage()
