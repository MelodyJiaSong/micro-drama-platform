"""资产总览的读模型（follow-up 293）。路径都是仓库相对路径，经 /api/media 显示。"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class AssetTileQdto:
    key: str                          # c24 / bg4 / p10；目录名不带键为空串
    folder: str
    path: str
    card: str
    name: str                         # 卡标题 ` · ` 前的第一段（敌法师）；没有卡用目录名
    title: str                        # 卡标题全文（敌法师 · Anti-Mage · Magina）
    portrait: str                     # 封面图：`{目录}.{png|jpg|…}`，否则以目录名开头的图，否则第一张；没有为空串
    images: list[str] = field(default_factory=list)   # 封面在前，其余按名字（v2 在 v10 前）
    videos: list[str] = field(default_factory=list)   # 新的在前
    meta: list[str] = field(default_factory=list)     # 卡开头的 `> ` 行


@dataclass(frozen=True)
class AssetGroupQdto:
    name: str                         # 分组目录，没有分组为空串
    tiles: list[AssetTileQdto] = field(default_factory=list)


@dataclass(frozen=True)
class AssetSectionQdto:
    kind: str                         # characters / background / props
    label: str
    count: int
    groups: list[AssetGroupQdto] = field(default_factory=list)


@dataclass(frozen=True)
class AssetOverviewQdto:
    drama: str
    sections: list[AssetSectionQdto] = field(default_factory=list)
    watch: list[str] = field(default_factory=list)    # 这些目录变了就重取
