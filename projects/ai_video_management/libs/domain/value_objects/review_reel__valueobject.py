"""审片串联的计划（follow-up 260）：按分镜顺序选好的每镜一条，和没有可用条的镜头；章节起止由各条实际时长累加。"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from libs.common.review_reel import REEL_FORMAT


@dataclass(frozen=True)
class ReelClip:
    scene: str
    key: str
    take: str          # take 目录（仓库相对路径）
    video: str         # 该条的视频（仓库相对路径）
    size: int
    mtime_ns: int
    review_status: str
    note: str = ""


@dataclass(frozen=True)
class ReviewReelPlan:
    name: str
    scene: str | None
    clips: list[ReelClip]
    skipped: list[dict[str, str]] = field(default_factory=list)

    @property
    def fingerprint(self) -> str:
        """只看选中的文件本身（路径、大小、修改时间）与编码规格；审核文字改了不必重拼。"""
        body = [self.name, self.scene, REEL_FORMAT, [[c.key, c.video, c.size, c.mtime_ns] for c in self.clips]]
        return hashlib.sha256(json.dumps(body, ensure_ascii=False).encode("utf-8")).hexdigest()

    def chapters(self, durations: list[float]) -> list[dict[str, Any]]:
        if len(durations) != len(self.clips):
            raise ValueError("每条都要有时长")
        out, start = [], 0.0
        for clip, seconds in zip(self.clips, durations):
            end = round(start + seconds, 3)
            out.append({"scene": clip.scene, "key": clip.key, "take": clip.take, "video": clip.video,
                        "start": round(start, 3), "end": end, "duration": round(seconds, 3),
                        "review_status": clip.review_status, "note": clip.note})
            start = end
        return out
