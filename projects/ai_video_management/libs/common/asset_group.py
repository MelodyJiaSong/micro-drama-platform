"""Asset folders may sit one group folder down (follow-up 284).

`characters/` and `props/` hold one folder per asset (`c65_Axe/`, `p1_极速神符/`),
either directly or inside one unkeyed group folder that splits a drama's assets
by side (`characters/近卫_sentinel/c65_Axe/`). Only one level: a group's keyed
children are the assets, its other children are ignored. An unkeyed folder with
no keyed child is not a group — it is returned as is, so older flat dramas and
their unkeyed folders behave exactly as before. `background/` nests freely
(`series_shared.scene_subject_dirs`).

The production tools import this module too (`tools/*.py`), so it imports only
relatively and never through `libs.`.
"""
from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
import re

from .character_dir import CHARACTER_DIR_RE

IsKeyed = Callable[[str], bool]


def _dirs(parent: Path) -> list[Path]:
    try:
        return sorted(p for p in parent.iterdir() if p.is_dir() and not p.is_symlink())
    except OSError:
        return []


def grouped_dirs(root: Path, is_keyed: IsKeyed) -> list[Path]:
    """`root`'s asset folders: keyed children, plus the keyed children of every
    unkeyed child that has any; an unkeyed child without keyed children stays."""
    out: list[Path] = []
    for child in _dirs(root):
        if is_keyed(child.name):
            out.append(child)
            continue
        inner = [g for g in _dirs(child) if is_keyed(g.name)]
        out.extend(inner or [child])
    return out


def group_dirs(root: Path, is_keyed: IsKeyed) -> list[Path]:
    """The group folders under `root` (unkeyed children holding keyed assets)."""
    return [c for c in _dirs(root) if not is_keyed(c.name) and any(is_keyed(g.name) for g in _dirs(c))]


def is_character_name(name: str) -> bool:
    return CHARACTER_DIR_RE.match(name) is not None


def character_dirs(characters_root: Path) -> list[Path]:
    """Every character card folder (`cN_…` / `mN_…`) under `characters/`, flat or grouped."""
    return [d for d in grouped_dirs(characters_root, is_character_name) if is_character_name(d.name)]


def find_character_dir(characters_root: Path, name: str) -> Path | None:
    """A card folder by its exact folder name (`c65_Axe`), wherever its group."""
    return next((d for d in character_dirs(characters_root) if d.name == name), None)


def character_weapon_keys(text: str) -> list[str]:
    match = re.search(r"^武器参考[:：]\s*(.+)$", text, re.M)
    if not match:
        return []
    keys = [s.strip() for s in match.group(1).split(",")]
    if not all(re.fullmatch(r"p[1-9]\d*", s) for s in keys) or len(keys) != len(set(keys)):
        raise ValueError("武器参考必须是不重复的 p 编号，以英文逗号分隔")
    return keys


__all__ = [
    "IsKeyed",
    "character_dirs",
    "character_weapon_keys",
    "find_character_dir",
    "group_dirs",
    "grouped_dirs",
    "is_character_name",
]
