"""商店货单 read route（follow-up 316）：GET /api/shop-items — 一部剧 `2_世界观人设/props/shop_items.json` 的出售方与货单。"""
from __future__ import annotations

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from apps.api.container import Container
from libs.application.dtos.shop_items__dto import ShopItemsQdto
from libs.application.queries.shop_items__query import ShopItemsQuery

router = APIRouter()


@router.get("/api/shop-items")
@inject
def shop_items(drama: str = Query(...),
               query: ShopItemsQuery = Depends(Provide[Container.shop_items_query])) -> ShopItemsQdto:
    return query.read(drama)
