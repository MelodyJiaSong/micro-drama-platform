from __future__ import annotations

import os
import stat
from collections.abc import Iterator, Sequence
from pathlib import Path

from libs.common import drama_ref
from libs.common.paths import RepoSandbox
from libs.infrastructure.daos.drama_tree__dao import FileEntryDao
from libs.infrastructure.readers.link_json__reader import LINK_SUFFIX

HARD_EXCLUDES: tuple[str, ...] = drama_ref.HARD_EXCLUDED_DIR_NAMES


class FileIndexReader:
    def __init__(self, sandbox: RepoSandbox) -> None:
        self._sandbox: RepoSandbox = sandbox

    def list_files(self, base_rel: str, search_exclude: Sequence[str]) -> tuple[FileEntryDao, ...]:
        if drama_ref.canonical_rel_violation(base_rel) is not None:
            return ()
        verdict = self._sandbox.check_read(base_rel)
        if verdict.path is None or verdict.rel is None or not verdict.path.is_dir():
            return ()
        # The floor only matches below the base, so a base that is itself inside an excluded dir is refused.
        if drama_ref.inside_hard_excluded(verdict.rel):
            return ()
        patterns = _patterns(search_exclude)
        entries = self._walk(verdict.path, verdict.rel, (), patterns)
        return tuple(sorted(entries, key=lambda entry: entry.rel))

    def _walk(
        self,
        directory: Path,
        directory_rel: str,
        below: tuple[str, ...],
        patterns: tuple[tuple[str, ...], ...],
    ) -> Iterator[FileEntryDao]:
        with os.scandir(directory) as scanned:
            children = sorted(scanned, key=lambda child: child.name)
        for child in children:
            if _is_reparse(child):
                continue
            child_rel = f"{directory_rel}/{child.name}"
            if child.is_dir(follow_symlinks=False):
                parts = (*below, child.name.casefold())
                if not any(parts[-len(pattern):] == pattern for pattern in patterns if len(parts) >= len(pattern)):
                    yield from self._walk(Path(child.path), child_rel, parts, patterns)
            elif child.is_file(follow_symlinks=False):
                yield _entry(child_rel, directory.name, child.name)


def _patterns(search_exclude: Sequence[str]) -> tuple[tuple[str, ...], ...]:
    raw = (*HARD_EXCLUDES, *search_exclude)
    # Case-folded on both sides: on NTFS `Renders/` and `renders/` are the same folder (U2-SEC-06).
    return tuple(
        tuple(part.casefold() for part in item.replace("\\", "/").strip("/").split("/"))
        for item in raw
        if item.replace("\\", "/").strip("/")
    )


def _entry(rel: str, parent_name: str, name: str) -> FileEntryDao:
    is_link = name.endswith(LINK_SUFFIX)
    inner = name[: -len(LINK_SUFFIX)] if is_link else name
    stem, ext = os.path.splitext(inner)
    return FileEntryDao(rel=rel, parent_name=parent_name, stem=stem, ext=ext.lower(), is_link=is_link)


def _is_reparse(entry: os.DirEntry[str]) -> bool:
    if entry.is_symlink():
        return True
    try:
        attributes = getattr(entry.stat(follow_symlinks=False), "st_file_attributes", 0)
    except OSError:
        return True
    return bool(attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
