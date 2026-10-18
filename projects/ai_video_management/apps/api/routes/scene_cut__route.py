"""剪辑模块（follow-up 269）：GET 一集各场的草稿剪辑与正片剪辑。视频本身经 /api/media 按 Range 播放。"""
from __future__ import annotations

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from apps.api.container import Container
from libs.application.dtos.scene_cut__dto import EpisodeCutsQdto
from libs.application.queries.scene_cut__query import SceneCutQuery

router = APIRouter()


@router.get("/api/scene-cuts")
@inject
def read_cuts(episode_path: str = Query(...),
              query: SceneCutQuery = Depends(Provide[Container.scene_cut_query])) -> EpisodeCutsQdto:
    return query.read(episode_path)
