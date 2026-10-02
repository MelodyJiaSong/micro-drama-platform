"""Where an equipment-keyed download lands."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

KIND_EQUIPMENT_VIEW: str = "equipment_view"   # `equipment/…/e{N}_{品质}_{名}/e{N}-{M}_{视图}`


@dataclass(frozen=True)
class EquipmentRouteDao:
    folder: Path
    kind: str
    name: str   # destination file name, extension included
