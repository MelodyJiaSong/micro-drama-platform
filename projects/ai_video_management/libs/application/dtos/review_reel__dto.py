from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ReviewReelQdto:
    """一份审片串联（整集或一场）的状态与结果（follow-up 260）。"""
    episode_path: str
    scene: str | None
    name: str
    state: str                     # none / running / done / failed / interrupted
    done: int = 0                  # 进度：已处理镜头数
    total: int = 0
    error: str = ""
    video_path: str = ""
    stale: bool = False            # 有了新的生成条，或已有的文件变了：结果需要重新生成
    manifest: dict[str, Any] | None = None
    scenes: list[dict[str, Any]] = field(default_factory=list)   # 场次选择：id、地点·时间、镜头数
