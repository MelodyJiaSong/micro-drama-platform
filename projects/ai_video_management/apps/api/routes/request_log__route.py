from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query

from apps.api.container import Container
from libs.application.queries.request_log__query import RequestLogQuery

router = APIRouter()


@router.get("/api/request-logs")
@inject
def list_logs(query: RequestLogQuery = Depends(Provide[Container.request_log_query])) -> dict:
    return query.list().to_payload()


@router.get("/api/request-log")
@inject
def read_log(path: str, offset: int = Query(0, ge=0, le=100000), limit: int = Query(50, ge=1, le=100),
             query: RequestLogQuery = Depends(Provide[Container.request_log_query])) -> dict:
    try:
        return query.read(path, offset, limit).to_payload()
    except FileNotFoundError:
        raise HTTPException(404, "请求日志不存在") from None
