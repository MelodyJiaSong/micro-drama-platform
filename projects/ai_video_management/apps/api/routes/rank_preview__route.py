"""排行榜预览 read route（follow-up 320）：GET /api/rank-preview?path= — `ai_videos/paihangbang` 系列总览或其下一期的审片数据。"""
from __future__ import annotations

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from apps.api.container import Container
from libs.application.dtos.rank_preview__dto import RankPreviewQdto
from libs.application.queries.rank_preview__query import RankPreviewQuery

router = APIRouter()


@router.get("/api/rank-preview")
@inject
def rank_preview(path: str = Query(...),
                 query: RankPreviewQuery = Depends(Provide[Container.rank_preview_query])) -> RankPreviewQdto:
    return query.read(path)
