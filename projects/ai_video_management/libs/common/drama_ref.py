"""Where a drama root sits under `ai_videos/` — flat, or nested inside a series.

Until 2026-09-09 a drama was always exactly `ai_videos/{drama}`: two segments,
hard-coded in ~20 places. `荒野生活` introduced a **series**: one top-level folder
holding many dramas (`ai_videos/huangye_shenghuo/{hy1,hy2}/`), so a drama root is
now **two OR three** segments and every path parser has to ask the filesystem
which one it is looking at.

A directory directly under `ai_videos/` is a **series** iff it contains
`series.json`. That marker is the single, explicit rule — no name conventions, no
manifest of episodes (episode membership stays derived from the filesystem per
CLAUDE.md § State surfaces). Everything else directly under `ai_videos/` is either
a flat drama or an `_`-prefixed system library (`_actors`, `_bgm`, `_deleted`, …).

Depth is therefore:

    ai_videos/{drama}                 -> 2
    ai_videos/{series}/{drama}        -> 3

`_`-prefixed segments are never dramas at either level, so a series may keep its
own shared assets in `ai_videos/{series}/_series/` without that folder being
mistaken for an episode.
"""
from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

AI_VIDEOS_DIR_NAME: str = "ai_videos"
SERIES_MARKER_NAME: str = "series.json"
SERIES_SHARED_DIR_NAME: str = "_series"


def is_series_dir(path: Path) -> bool:
    return (path / SERIES_MARKER_NAME).is_file()


def series_dirs(root: Path) -> list[Path]:
    """Series folders directly under `ai_videos/`, sorted by name."""
    ai_videos = root / AI_VIDEOS_DIR_NAME
    if not ai_videos.is_dir():
        return []
    return sorted(
        p for p in ai_videos.iterdir()
        if p.is_dir() and not p.is_symlink() and not p.name.startswith("_") and is_series_dir(p)
    )


def drama_dirs(root: Path) -> list[Path]:
    """Every drama root under `ai_videos/`, flat ones and series members alike.

    Series members are emitted in place of their series folder, so callers that
    iterate dramas (casting scans, bgm reference scans, …) see leaf dramas only.
    """
    ai_videos = root / AI_VIDEOS_DIR_NAME
    if not ai_videos.is_dir():
        return []
    out: list[Path] = []
    for entry in sorted(p for p in ai_videos.iterdir() if p.is_dir()):
        if entry.is_symlink() or entry.name.startswith("_"):
            continue
        if is_series_dir(entry):
            out.extend(
                sorted(
                    p for p in entry.iterdir()
                    if p.is_dir() and not p.is_symlink() and not p.name.startswith("_")
                )
            )
            continue
        out.append(entry)
    return out


def drama_depth(root: Path, parts: Sequence[str]) -> int | None:
    """How many leading segments of `parts` name the drama root, or None.

    Returns 2 for a flat drama, 3 for a series member. None when `parts` is not
    under a drama at all — wrong first segment, a system library (`_actors`), a
    series folder with nothing after it, or a series' own `_series/` shared dir.
    """
    if len(parts) < 2 or parts[0] != AI_VIDEOS_DIR_NAME:
        return None
    if not parts[1] or parts[1].startswith("_"):
        return None
    if not is_series_dir(root / AI_VIDEOS_DIR_NAME / parts[1]):
        return 2
    if len(parts) < 3 or not parts[2] or parts[2].startswith("_"):
        return None
    return 3


def drama_root_rel(root: Path, parts: Sequence[str]) -> str | None:
    """`ai_videos/{drama}` or `ai_videos/{series}/{drama}` for `parts`, else None."""
    depth = drama_depth(root, parts)
    if depth is None:
        return None
    return "/".join(parts[:depth])


def split_drama_rel(root: Path, rel: str) -> tuple[str, list[str]] | None:
    """Split `rel` into (drama root rel, remaining segments), or None."""
    parts = rel.strip("/").split("/")
    depth = drama_depth(root, parts)
    if depth is None:
        return None
    return "/".join(parts[:depth]), list(parts[depth:])
