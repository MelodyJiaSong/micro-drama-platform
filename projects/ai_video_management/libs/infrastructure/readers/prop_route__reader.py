"""Route a download by the prop routing key it carries (follow-up 174).

Every object lives once, under `props/p{N}_{名}/` (`libs.common.prop_key`);
a scene only links to it (`assets/*.link.json`).

| leftmost key in the name | prop                          | lands as                                   |
|--------------------------|-------------------------------|--------------------------------------------|
| `p{N}-{i}` (image)        | scene object (has `asset.toml`) | the card's ```text first line `p{N}-{i}_…`, |
|                          |                               | else `p{N}-{i}_{正面|侧面|背面}`             |
| `p{N}…` (`.glb`)          | any prop                      | `mesh/p{N}.glb`                            |

A story prop carries no `asset.toml`; its `p{N}-{M}` anchors are not routed
here and keep the importer's `p{N}-{M}.{ext}` naming (rule 4b-A), which shot
`参考:` lines point at. A GLB holds exactly one object (2026-09-25), so a model
file routes by prop key only. A number owned by two folders routes nowhere.
"""
from __future__ import annotations

from pathlib import Path

from libs.common import drama_layout, prop_key, series_shared
from libs.common.prop_key import PropKey
from libs.infrastructure.daos.prop_route__dao import KIND_PROP_MESH, KIND_PROP_VIEW, PropRouteDao
from libs.infrastructure.readers.card_view__reader import VIEW_IMAGE_EXTS, view_stem

MESH_DIR_NAME: str = "mesh"
# The asset generator's spec (`tools/gen_bg_assets.py`): the one thing that
# makes a prop a scene object rather than a story prop.
OBJECT_SPEC_NAME: str = "asset.toml"
MODEL_EXTS: frozenset[str] = frozenset({".glb", ".gltf"})
_MESH_EXT: str = ".glb"


class PropKeyRouter:
    def route(self, filename: str, drama_dir: Path) -> PropRouteDao | None:
        src = Path(filename)
        ext = src.suffix.lower()
        key = prop_key.first_key(src.stem)
        if key is None:
            return None
        found = self._prop(key.number, drama_dir)
        if found is None:
            return None
        folder, own = found
        if ext in MODEL_EXTS:
            if ext != _MESH_EXT:
                return None
            return PropRouteDao(folder / MESH_DIR_NAME, KIND_PROP_MESH, f"{own.base}{_MESH_EXT}")
        if key.view is None or ext not in VIEW_IMAGE_EXTS or not (folder / OBJECT_SPEC_NAME).is_file():
            return None
        return PropRouteDao(folder, KIND_PROP_VIEW, f"{view_stem(folder, own.base, key.view)}{ext}")

    @staticmethod
    def _prop(number: int, drama_dir: Path) -> tuple[Path, PropKey] | None:
        """The one `p{number}_…` folder across the drama's prop roots, with its
        key as written on disk; None when there is none or several."""
        hits = [
            (d, k) for d in series_shared.asset_dirs(drama_dir, drama_layout.props_dir)
            if (k := prop_key.parse_name(d.name)) is not None and k.view is None and k.number == number
        ]
        return hits[0] if len({d.resolve() for d, _ in hits}) == 1 else None


__all__ = ["MESH_DIR_NAME", "MODEL_EXTS", "OBJECT_SPEC_NAME", "PropKeyRouter"]
