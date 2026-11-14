"""人物卡样片与正片的原始读数（follow-up 286）：路径都是仓库相对路径，文件不在就是空串。"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SkillCardDao:
    key: str                          # k651
    number: int
    path: str                         # 技能目录
    title: str                        # 技能卡 md 首个 `# ` 行
    card: str
    icon: str
    peak: str
    drafts: list[dict[str, Any]]      # ShotRendersReader 的生成记录，新的在前
    finals: list[dict[str, Any]]


@dataclass(frozen=True)
class CharacterReelDao:
    name: str
    path: str
    drama: str
    turntable: str
    skills: list[SkillCardDao]
    cuts: dict[str, list[dict[str, Any]]]   # {阶段: [剪辑决定，带 _path / _dir / _file_version / _episode；人物目录 demo/ 的带 _own]}
