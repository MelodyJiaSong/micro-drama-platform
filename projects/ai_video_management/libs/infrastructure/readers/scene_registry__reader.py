"""`scenes/registry.toml` — a drama's single source of bg numbers (follow-up 173).

A continent / zone folder (`scenes/{大陆}/{区}/`) carries no bg key of its own;
the zone's key is that of its zone-level subject, the registry row with
`kind = "zone_whole"` for that zone (`bg172_艾尔文森林全境` → `bg172`). This is
the only place in the webapp that parses the registry.
"""
from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

REGISTRY_FILE_NAME: str = "registry.toml"
ZONE_WHOLE_KIND: str = "zone_whole"


@dataclass(frozen=True)
class _ZoneRow:
    continent: str
    key: str


class SceneRegistryReader:
    """Parses each registry once per mtime — the tree asks for every zone."""

    def __init__(self) -> None:
        self._cache: dict[Path, tuple[int, dict[str, _ZoneRow]]] = {}

    def zone_key(self, scenes_root: Path, zone_dir: Path) -> str | None:
        """`bg172` for `scenes/eastern_kingdoms/elwynn_forest`, else None."""
        row = self._zones(scenes_root / REGISTRY_FILE_NAME).get(zone_dir.name)
        if row is None:
            return None
        if row.continent and row.continent != zone_dir.parent.name:
            return None
        return row.key

    def _zones(self, registry: Path) -> dict[str, _ZoneRow]:
        try:
            mtime = registry.stat().st_mtime_ns
        except OSError:
            return {}
        hit = self._cache.get(registry)
        if hit is not None and hit[0] == mtime:
            return hit[1]
        zones = self._parse(registry)
        self._cache[registry] = (mtime, zones)
        return zones

    @staticmethod
    def _parse(registry: Path) -> dict[str, _ZoneRow]:
        try:
            with registry.open("rb") as fh:
                data = tomllib.load(fh)
        except (OSError, tomllib.TOMLDecodeError):
            return {}
        zones: dict[str, _ZoneRow] = {}
        for row in data.get("bg", []):
            if not isinstance(row, dict) or row.get("kind") != ZONE_WHOLE_KIND:
                continue
            zone, n = row.get("zone"), row.get("n")
            if isinstance(zone, str) and zone and isinstance(n, int):
                continent = row.get("continent")
                zones.setdefault(zone, _ZoneRow(
                    continent=continent if isinstance(continent, str) else "",
                    key=f"bg{n}",
                ))
        return zones


__all__ = ["REGISTRY_FILE_NAME", "SceneRegistryReader", "ZONE_WHOLE_KIND"]
