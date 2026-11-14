"""英雄 demo 定版标记 read route（follow-up 315）：GET /api/demo-status — demo 已定版的人物、定版成片与发布文案状态。"""
from __future__ import annotations

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from apps.api.container import Container
from libs.application.dtos.demo_status__dto import DemoStatusListQdto
from libs.application.queries.demo_status__query import DemoStatusQuery

router = APIRouter()


@router.get("/api/demo-status")
@inject
def demo_status(query: DemoStatusQuery = Depends(Provide[Container.demo_status_query])) -> DemoStatusListQdto:
    return query.read()
