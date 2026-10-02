"""Route a download by the equipment routing key it carries.

Every piece of equipment lives once, as an `e{N}_{品质}_{名}/` folder at any depth
under `equipment/` (`equipment/板甲/胸/e79_…`, `equipment/主手/e12_…`); the item
is found by its name (`series_shared.equipment_item_dirs`), never by depth.

| leftmost key in the name | lands in                | as                                          |
|--------------------------|-------------------------|---------------------------------------------|
| `e{N}-{M}` (image)        | the `e{N}_…` item folder | the card's ```text first line `e{N}-{M}_…`, |
|                          |                         | else `e{N}-{M}_{正面|侧面|背面}`              |

Equipment is imported by view key only — a bare `e{N}`, a video or a model file
routes nowhere (a GLB only ever lands in `props/p{N}_*/mesh/`), and a number
owned by two item folders routes nowhere.
"""
from __future__ import annotations

from pathlib import Path

from libs.common import equipment_key, series_shared
from libs.common.equipment_key import EquipmentKey
from libs.infrastructure.daos.equipment_route__dao import KIND_EQUIPMENT_VIEW, EquipmentRouteDao
from libs.infrastructure.readers.card_view__reader import VIEW_IMAGE_EXTS, view_stem


class EquipmentKeyRouter:
    def route(self, filename: str, drama_dir: Path) -> EquipmentRouteDao | None:
        src = Path(filename)
        ext = src.suffix.lower()
        key = equipment_key.first_key(src.stem)
        if key is None or key.view is None or ext not in VIEW_IMAGE_EXTS:
            return None
        found = self.item(key.number, drama_dir)
        if found is None:
            return None
        folder, own = found
        return EquipmentRouteDao(folder, KIND_EQUIPMENT_VIEW, f"{view_stem(folder, own.base, key.view)}{ext}")

    @staticmethod
    def item(number: int, drama_dir: Path) -> tuple[Path, EquipmentKey] | None:
        """The one `e{number}_…` item folder across the drama's equipment roots,
        with its key as written on disk; None when there is none or several."""
        hits = [
            (d, k) for d in series_shared.equipment_item_dirs(drama_dir)
            if (k := equipment_key.parse_name(d.name)) is not None and k.number == number
        ]
        return hits[0] if len({d.resolve() for d, _ in hits}) == 1 else None


__all__ = ["EquipmentKeyRouter"]
