"""商店货单的读模型（follow-up 316）。路径都是仓库相对路径，经 /api/media 显示；文件不在为空串。"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ShopItemQdto:
    prop_key: str
    name_zh: str
    name_en: str
    category: str
    price: str
    recipe: str
    card: str
    image: str
    sold_by: list[str] = field(default_factory=list)   # 出售方键，按货单顺序


@dataclass(frozen=True)
class ShopSellerQdto:
    key: str
    name_zh: str
    name_en: str
    kind: str
    where: str
    folder: str
    card: str
    image: str
    count: int
    items: list[ShopItemQdto] = field(default_factory=list)


@dataclass(frozen=True)
class ShopItemsQdto:
    drama: str
    source: str                       # 剧没有货单为空串
    doc: str
    version: str
    note: str
    sellers: list[ShopSellerQdto] = field(default_factory=list)
    items: list[ShopItemQdto] = field(default_factory=list)   # 去重，按第一次出现的顺序
    error: str = ""
