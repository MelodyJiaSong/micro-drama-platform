from __future__ import annotations

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from apps.api.container import Container
from libs.application.dtos.process_qc__dto import ProcessQcDramaQdto, ProcessQcRepoQdto
from libs.application.queries.process_qc__query import ProcessQcQuery

router = APIRouter()


@router.get("/api/process-qc")
@inject
def read_process_qc(query: ProcessQcQuery = Depends(Provide[Container.process_qc_query])) -> ProcessQcRepoQdto:
    return query.repo()


@router.get("/api/process-qc/drama")
@inject
def read_process_qc_drama(drama: str = Query(...),
                          query: ProcessQcQuery = Depends(Provide[Container.process_qc_query])) -> ProcessQcDramaQdto:
    return query.drama(drama)
