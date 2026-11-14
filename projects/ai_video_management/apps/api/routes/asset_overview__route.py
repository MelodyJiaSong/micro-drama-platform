"""资产总览 read route（follow-up 293）：GET /api/asset-overview — 一部剧的人物、背景、道具，每个资产一格。"""
from __future__ import annotations

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from apps.api.container import Container
from libs.application.dtos.asset_overview__dto import AssetOverviewQdto
from libs.application.queries.asset_overview__query import AssetOverviewQuery

router = APIRouter()


@router.get("/api/asset-overview")
@inject
def asset_overview(drama: str = Query(...),
                   query: AssetOverviewQuery = Depends(Provide[Container.asset_overview_query])) -> AssetOverviewQdto:
    return query.read(drama)
