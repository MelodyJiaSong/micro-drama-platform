"""英雄 demo 定版标记的读模型（dota_yingxiong follow-up 315）。路径都是仓库相对路径。"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DemoStatusQdto:
    hero: str                         # 人物目录（`…/characters/[{分组}/]{卡}`）
    folder: str                       # c65_Axe
    version: int                      # 定版剪辑的版本号
    cut: str                          # demo/edit/final/cut_v{N}.json
    video: str                        # 定版成片；文件不在为空串
    status: str                       # cut 的 status 原文
    newer: list[int] = field(default_factory=list)   # 定版之后又剪、还没定的版本
    publish: str = ""                 # demo/publish.md；不在为空串
    publish_video: str = ""           # publish.md 开头写的成片文件名
    publish_state: str = "missing"    # ok / stale（写的不是定版成片）/ missing


@dataclass(frozen=True)
class DemoStatusListQdto:
    heroes: list[DemoStatusQdto] = field(default_factory=list)
