from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query

from apps.api.container import Container
from libs.application.queries.review_run__query import ReviewRunQuery

router = APIRouter()


@router.get("/api/review-runs")
@inject
def list_runs(query: ReviewRunQuery = Depends(Provide[Container.review_run_query])) -> dict:
    return query.list().to_payload()


@router.get("/api/review-runs/checklist")
@inject
def read_checklist(path: str = Query(...), query: ReviewRunQuery = Depends(Provide[Container.review_run_query])) -> dict:
    """一张审查单的 checklist.json（可超过 /api/file 的 1 MiB 上限）；读不到一律 404。"""
    run = query.checklist(path)
    if run is None:
        raise HTTPException(status_code=404, detail="审查单不存在或读不了")
    return run
