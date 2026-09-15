"""The cross-episode asset folders a series member routes downloads into.

A series keeps the characters / scenes / props its episodes share in
`ai_videos/{series}/_series/` (`drama_ref.SERIES_SHARED_DIR_NAME`). `_series` is
never a drama, so anything that walks one drama's asset folders has to be told
to walk the shared ones too — otherwise a shared card's download has nowhere to
land, and an episode-local duplicate silently swallows it instead.

When an episode folder and a shared folder own the same routing prefix
(`asset_key.folder_key`) or carry the same name, there is no way to tell which
of the two a download belongs to. That is reported, never guessed.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from libs.common import asset_key, drama_layout
from libs.common.drama_ref import AI_VIDEOS_DIR_NAME, SERIES_SHARED_DIR_NAME, is_series_dir

CONFLICT_PREFIX: str = "series_key_conflict"

LayoutDir = Callable[[Path], Path]
_ASSET_LAYOUTS: tuple[LayoutDir, ...] = (
    drama_layout.characters_dir,
    drama_layout.scenes_dir,
    drama_layout.props_dir,
)


def shared_dir(drama_dir: Path) -> Path | None:
    """`ai_videos/{series}/_series/` for a series member, else None."""
    series = drama_dir.parent
    if drama_dir.name.startswith("_") or series.parent.name != AI_VIDEOS_DIR_NAME:
        return None
    if not is_series_dir(series):
        return None
    shared = series / SERIES_SHARED_DIR_NAME
    return shared if shared.is_dir() and not shared.is_symlink() else None


def asset_roots(drama_dir: Path) -> list[Path]:
    """The drama itself, then its series' shared dir when there is one."""
    shared = shared_dir(drama_dir)
    return [drama_dir] if shared is None else [drama_dir, shared]


def child_dirs(parent: Path) -> list[Path]:
    try:
        return sorted(p for p in parent.iterdir() if p.is_dir() and not p.is_symlink())
    except OSError:
        return []


def asset_dirs(drama_dir: Path, layout_dir: LayoutDir) -> list[Path]:
    """Every `{characters|scenes|props}/*` folder across the drama's asset roots."""
    return [child for root in asset_roots(drama_dir) for child in child_dirs(layout_dir(root))]


@dataclass(frozen=True)
class SeriesKeyConflict:
    episode_folder: Path
    series_folder: Path

    def message(self, rel: Callable[[Path], str]) -> str:
        return f"{CONFLICT_PREFIX}: {rel(self.episode_folder)} <-> {rel(self.series_folder)}"


@dataclass(frozen=True)
class SeriesConflicts:
    by_folder: dict[Path, SeriesKeyConflict]
    by_key: dict[str, SeriesKeyConflict]

    def owning(self, folder: Path) -> SeriesKeyConflict | None:
        """The conflict covering `folder` or any folder above it."""
        for candidate in (folder, *folder.parents):
            hit = self.by_folder.get(candidate)
            if hit is not None:
                return hit
        return None

    def for_key(self, key: str) -> SeriesKeyConflict | None:
        return self.by_key.get(key.lower())


def _owned_folders(root: Path) -> list[Path]:
    """Asset folders plus the keyed `bg{N}_{主体}` subjects nested inside scenes."""
    folders = [child for layout in _ASSET_LAYOUTS for child in child_dirs(layout(root))]
    subjects = [
        sub
        for scene in child_dirs(drama_layout.scenes_dir(root))
        for sub in child_dirs(scene)
        if asset_key.folder_key(sub.name) is not None
    ]
    return folders + subjects


def find_conflicts(drama_dir: Path) -> SeriesConflicts:
    shared = shared_dir(drama_dir)
    if shared is None:
        return SeriesConflicts(by_folder={}, by_key={})
    shared_by_key: dict[str, Path] = {}
    shared_by_name: dict[str, Path] = {}
    for folder in _owned_folders(shared):
        key = asset_key.folder_key(folder.name)
        if key is not None:
            shared_by_key.setdefault(key.lower(), folder)
        shared_by_name.setdefault(folder.name.casefold(), folder)
    by_folder: dict[Path, SeriesKeyConflict] = {}
    by_key: dict[str, SeriesKeyConflict] = {}
    for folder in _owned_folders(drama_dir):
        key = asset_key.folder_key(folder.name)
        twin = (shared_by_key.get(key.lower()) if key is not None else None) or shared_by_name.get(
            folder.name.casefold()
        )
        if twin is None:
            continue
        conflict = SeriesKeyConflict(episode_folder=folder, series_folder=twin)
        by_folder.setdefault(folder, conflict)
        by_folder.setdefault(twin, conflict)
        twin_key = asset_key.folder_key(twin.name)
        for owned in (key, twin_key):
            if owned is not None:
                by_key.setdefault(owned.lower(), conflict)
    return SeriesConflicts(by_folder=by_folder, by_key=by_key)


__all__ = [
    "CONFLICT_PREFIX",
    "SeriesConflicts",
    "SeriesKeyConflict",
    "asset_dirs",
    "asset_roots",
    "child_dirs",
    "find_conflicts",
    "shared_dir",
]
