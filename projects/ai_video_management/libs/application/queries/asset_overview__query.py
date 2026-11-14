"""资产总览（follow-up 293）：人物、背景、道具各一节，节内按分组、组内按键号排，每个资产一格。只读。"""
from __future__ import annotations

import re

from libs.application.dtos.asset_overview__dto import AssetGroupQdto, AssetOverviewQdto, AssetSectionQdto, AssetTileQdto
from libs.infrastructure.daos.asset_overview__dao import AssetFolderDao
from libs.infrastructure.readers.asset_overview__reader import AssetOverviewReader

SECTIONS = (("characters", "人物"), ("background", "背景"), ("props", "道具"))
KEY_RE = re.compile(r"^([a-z]+)(\d+)(?=_|$)", re.I)
# 英雄 c 在召唤物 / 野怪 m 前；其余前缀按字母
PREFIX_ORDER = {"c": 0, "m": 1}
DIGITS_RE = re.compile(r"(\d+)")


def _natural(text: str) -> list[object]:
    return [int(part) if part.isdigit() else part.lower() for part in DIGITS_RE.split(text)]


def _order(folder: str) -> tuple[int, str, int, list[object]]:
    match = KEY_RE.match(folder)
    if not match:
        return (9, "", 0, _natural(folder))
    prefix = match.group(1).lower()
    return (PREFIX_ORDER.get(prefix, 2), prefix, int(match.group(2)), _natural(folder))


def _stem(path: str) -> str:
    name = path.rsplit("/", 1)[-1]
    return name.rsplit(".", 1)[0]


def _portrait(folder: str, images: list[str]) -> str:
    exact = [p for p in images if _stem(p) == folder]
    if exact:
        return exact[0]
    named = sorted((p for p in images if _stem(p).startswith(folder)), key=lambda p: _natural(_stem(p)))
    return named[0] if named else (images[0] if images else "")


def tile(dao: AssetFolderDao) -> AssetTileQdto:
    match = KEY_RE.match(dao.folder)
    portrait = _portrait(dao.folder, dao.images)
    images = ([portrait] if portrait else []) + sorted((p for p in dao.images if p != portrait), key=lambda p: _natural(_stem(p)))
    videos = [path for path, _ in sorted(dao.videos, key=lambda v: v[1], reverse=True)]
    name = dao.title.split(" · ", 1)[0].strip() if dao.title else dao.folder
    return AssetTileQdto(match.group(0).lower() if match else "", dao.folder, dao.path, dao.card, name, dao.title, portrait,
                         images, videos, dao.meta)


def groups(daos: list[AssetFolderDao]) -> list[AssetGroupQdto]:
    """分组按组里最小的键号排（近卫 c1 在天灾 c60 前、中立野怪 m7 后），组内按键号。"""
    by_group: dict[str, list[AssetFolderDao]] = {}
    for dao in daos:
        by_group.setdefault(dao.group, []).append(dao)
    ordered = sorted(by_group.items(), key=lambda item: (min(_order(d.folder) for d in item[1]), _natural(item[0])))
    return [AssetGroupQdto(name, [tile(d) for d in sorted(members, key=lambda d: _order(d.folder))]) for name, members in ordered]


class AssetOverviewQuery:
    def __init__(self, reader: AssetOverviewReader) -> None:
        self.reader = reader

    def read(self, drama: str) -> AssetOverviewQdto:
        norm, kinds, watch = self.reader.read(drama)
        sections = [AssetSectionQdto(kind, label, len(kinds.get(kind, [])), groups(kinds.get(kind, []))) for kind, label in SECTIONS]
        return AssetOverviewQdto(norm, sections, watch)
