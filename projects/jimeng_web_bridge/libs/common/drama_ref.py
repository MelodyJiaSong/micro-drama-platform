"""Drama roots under `ai_videos/` (spec v2 FR-10, §8 divergence 2).

Re-implements `ai_video_management`'s rule because projects may not import each
other: a directory directly under `ai_videos/` is a series iff it holds
`series.json`, and `_`-prefixed directories are never dramas at either level.
The FR-10 "listable" filter is layered on top so folders like `notes/` stay out
of the UI without changing what counts as a drama root.

Drama-facing inputs are accepted only in the canonical `/`-joined form. A `\\`
inside a segment would otherwise let `ai_videos/hs\\hy3\\renders` pass as a
two-segment drama root that the sandbox later splits into five (U2-SEC-01).
"""
from __future__ import annotations

import os
import re
from collections.abc import Sequence
from pathlib import Path

from libs.common.paths import AI_VIDEOS_DIR_NAME, is_reparse_point, lexical_violation, segment_violation

SERIES_MARKER_NAME: str = "series.json"
SERIES_SHARED_DIR_NAME: str = "_series"
DRAMA_CONFIG_NAME: str = "jimeng_config.toml"
ASSET_KIND_DIR_NAMES: tuple[str, ...] = ("characters", "props", "scenes")
# Config may extend `references.search_exclude` but never re-admit these (security SEC-F10).
HARD_EXCLUDED_DIR_NAMES: tuple[str, ...] = ("_deleted", "_candidates", "renders")
_HARD_EXCLUDED_FOLDED: frozenset[str] = frozenset(name.casefold() for name in HARD_EXCLUDED_DIR_NAMES)
_SHOT_MD_RE = re.compile(r"^shot.*\.md$")


def canonical_rel_violation(rel: str) -> str | None:
    if "\\" in rel:
        return "backslash_separator"
    return lexical_violation(rel)


def is_hard_excluded_name(name: str) -> bool:
    # NTFS names are case-insensitive, so `Renders/` is the same exclusion as `renders/` (U2-SEC-06).
    return name.casefold() in _HARD_EXCLUDED_FOLDED


def inside_hard_excluded(rel: str) -> bool:
    return any(is_hard_excluded_name(part) for part in rel.split("/"))


def is_series_dir(path: Path) -> bool:
    return (path / SERIES_MARKER_NAME).is_file()


def visible_subdirs(parent: Path) -> list[Path]:
    if not parent.is_dir():
        return []
    return sorted(
        child
        for child in parent.iterdir()
        if not child.name.startswith("_") and not is_reparse_point(child) and child.is_dir()
    )


def searchable_subdirs(parent: Path) -> list[Path]:
    return [child for child in visible_subdirs(parent) if not is_hard_excluded_name(child.name)]


def drama_candidate_dirs(parent: Path) -> list[Path]:
    return [child for child in visible_subdirs(parent) if not _never_a_drama(child.name)]


def series_dirs(root: Path) -> list[Path]:
    return [entry for entry in drama_candidate_dirs(root / AI_VIDEOS_DIR_NAME) if is_series_dir(entry)]


def drama_dirs(root: Path) -> list[Path]:
    out: list[Path] = []
    for entry in drama_candidate_dirs(root / AI_VIDEOS_DIR_NAME):
        if is_series_dir(entry):
            out.extend(drama_candidate_dirs(entry))
        else:
            out.append(entry)
    return out


def drama_depth(root: Path, parts: Sequence[str]) -> int | None:
    if len(parts) < 2 or parts[0] != AI_VIDEOS_DIR_NAME or _never_a_drama(parts[1]):
        return None
    if not is_series_dir(root / AI_VIDEOS_DIR_NAME / parts[1]):
        return 2
    if len(parts) < 3 or _never_a_drama(parts[2]):
        return None
    return 3


def drama_root_rel(root: Path, parts: Sequence[str]) -> str | None:
    depth = drama_depth(root, parts)
    if depth is None:
        return None
    return "/".join(parts[:depth])


def split_drama_rel(root: Path, rel: str) -> tuple[str, list[str]] | None:
    stripped = rel.strip("/")
    if canonical_rel_violation(stripped) is not None:
        return None
    parts = stripped.split("/")
    depth = drama_depth(root, parts)
    if depth is None:
        return None
    return "/".join(parts[:depth]), list(parts[depth:])


def series_shared_rel(drama_rel: str) -> str | None:
    parts = drama_rel.split("/")
    if len(parts) != 3:
        return None
    return "/".join((parts[0], parts[1], SERIES_SHARED_DIR_NAME))


def asset_kind_dirs(drama_path: Path, kind: str) -> list[Path]:
    """`{kind}/` directly under the drama root or one level down (`2_世界观人设/{kind}`)."""
    return [
        base / kind
        for base in (drama_path, *searchable_subdirs(drama_path))
        if (base / kind).is_dir() and not is_reparse_point(base / kind)
    ]


def is_listable_drama(path: Path) -> bool:
    if (path / DRAMA_CONFIG_NAME).is_file():
        return True
    if any(asset_kind_dirs(path, kind) for kind in ASSET_KIND_DIR_NAMES):
        return True
    return _has_shot_md(path)


def _never_a_drama(segment: str) -> bool:
    return (
        segment.startswith("_")
        or is_hard_excluded_name(segment)
        or segment_violation(segment) is not None
    )


def _has_shot_md(path: Path) -> bool:
    for current, dirnames, filenames in os.walk(path):
        if any(_SHOT_MD_RE.match(name) for name in filenames):
            return True
        dirnames[:] = [
            name
            for name in dirnames
            if not name.startswith("_")
            and not is_hard_excluded_name(name)
            and not is_reparse_point(Path(current) / name)
        ]
    return False
