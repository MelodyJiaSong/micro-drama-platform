"""整集审片串联（follow-up 260）：GET 查状态与结果，POST 开始拼（后台线程）。视频本身经 /api/media 按 Range 播放。"""
from __future__ import annotations

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from apps.api.container import Container
from libs.application.commands.review_reel__command import ReviewReelCommand
from libs.application.dtos.review_reel__dto import ReviewReelQdto
from libs.application.queries.review_reel__query import ReviewReelQuery

router = APIRouter()


class StartBody(BaseModel):
    episode_path: str
    scene: str | None = None


@router.get("/api/review-reel")
@inject
def read_reel(episode_path: str = Query(...), scene: str | None = Query(None),
              query: ReviewReelQuery = Depends(Provide[Container.review_reel_query])) -> ReviewReelQdto:
    return query.read(episode_path, scene or None)


@router.post("/api/review-reel")
@inject
def start_reel(body: StartBody, command: ReviewReelCommand = Depends(Provide[Container.review_reel_command])) -> ReviewReelQdto:
    return command.start(body.episode_path, body.scene or None)
