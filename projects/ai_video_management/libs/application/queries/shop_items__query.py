"""商店货单（follow-up 316）：出售方 → 货单，物品 → 哪些出售方卖它。只读。"""
from __future__ import annotations

from libs.application.dtos.shop_items__dto import ShopItemQdto, ShopItemsQdto, ShopSellerQdto
from libs.infrastructure.daos.shop_items__dao import ShopItemDao
from libs.infrastructure.readers.shop_items__reader import ShopItemsReader


def _item(dao: ShopItemDao, sold_by: list[str]) -> ShopItemQdto:
    return ShopItemQdto(dao.prop_key, dao.name_zh, dao.name_en, dao.category, dao.price, dao.recipe,
                        dao.card, dao.image, list(sold_by))


class ShopItemsQuery:
    def __init__(self, reader: ShopItemsReader) -> None:
        self.reader = reader

    def read(self, drama: str) -> ShopItemsQdto:
        norm, dao = self.reader.read(drama)
        sold_by: dict[str, list[str]] = {}
        first: dict[str, ShopItemDao] = {}
        for seller in dao.sellers:
            for item in seller.items:
                first.setdefault(item.prop_key, item)
                keys = sold_by.setdefault(item.prop_key, [])
                if seller.key not in keys:
                    keys.append(seller.key)
        sellers = [ShopSellerQdto(s.key, s.name_zh, s.name_en, s.kind, s.where, s.folder, s.card, s.image, s.count,
                                  [_item(i, sold_by[i.prop_key]) for i in s.items]) for s in dao.sellers]
        items = [_item(i, sold_by[key]) for key, i in first.items()]
        return ShopItemsQdto(norm, dao.source, dao.doc, dao.version, dao.note, sellers, items, dao.error)
