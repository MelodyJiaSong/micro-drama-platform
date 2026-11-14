"""商店货单的原始读数（follow-up 316）：路径都已换成仓库相对路径，文件不在为空串。"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ShopItemDao:
    prop_key: str                     # p157
    name_zh: str
    name_en: str
    category: str                     # 消耗品 / 基础件 / 合成成品 …
    price: str                        # 原文（`250 / 875`、`— / 525`）
    recipe: str                       # 合成路线原文，基础件为空串
    card: str                         # 道具卡 .md
    image: str                        # 道具图


@dataclass(frozen=True)
class ShopSellerDao:
    key: str                          # bg22 / m300 / m7
    name_zh: str
    name_en: str
    kind: str                         # 建筑（消耗品商店）/ 人形商人（合成）/ 野怪掉落 …
    where: str
    folder: str                       # 出售方资产目录
    card: str                         # `{目录}/{目录名}.md`
    image: str                        # `{目录}/{目录名}.png|jpg|jpeg|webp`
    count: int
    items: list[ShopItemDao] = field(default_factory=list)


@dataclass(frozen=True)
class ShopItemsDao:
    source: str                       # shop_items.json；剧没有货单为空串
    doc: str                          # 同目录的人读版 shop_items.md，不在为空串
    version: str
    note: str
    sellers: list[ShopSellerDao] = field(default_factory=list)
    error: str = ""                   # 文件在但读不了 / 结构不对
