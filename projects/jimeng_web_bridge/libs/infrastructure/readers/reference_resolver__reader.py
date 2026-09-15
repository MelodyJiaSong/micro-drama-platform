from __future__ import annotations

import re
from collections.abc import Callable, Sequence

from libs.common import drama_ref
from libs.common.paths import RepoSandbox
from libs.infrastructure.daos.drama_tree__dao import FileEntryDao, ResolveResultDao
from libs.infrastructure.errors.sandbox__error import LinkRejectedError
from libs.infrastructure.readers.file_index__reader import FileIndexReader
from libs.infrastructure.readers.link_json__reader import IMAGE_EXTS, VIDEO_EXTS, LinkJsonReader

__all__ = ["IMAGE_EXTS", "VIDEO_EXTS", "ReferenceResolverReader"]

_ROUTING_KEY_RE = re.compile(r"^(?:bg|c|p)\d+-\d+$")
_SUBJECT_DIR_RE = re.compile(r"^(?:bg|c|p)\d+_")
_SHOT_DIR_RE = re.compile(r"^shot(\d+)$")
_PREVIZ_PREFIX_RE = re.compile(r"^previz_(shot\d+)$")
_PREVIZ_SUFFIX_RE = re.compile(r"^(shot\d+)_previz$")

Matcher = Callable[[FileEntryDao], bool]


class ReferenceResolverReader:
    """File-backed resolvers of spec v2 FR-8: `asset_file`, `shot_video`, `prev_shot_lastframe`."""

    def __init__(self, sandbox: RepoSandbox, files: FileIndexReader, links: LinkJsonReader) -> None:
        self._sandbox: RepoSandbox = sandbox
        self._files: FileIndexReader = files
        self._links: LinkJsonReader = links

    def search_bases(self, drama_rel: str) -> tuple[str, ...]:
        if drama_ref.canonical_rel_violation(drama_rel) is not None:
            return ()
        if drama_ref.drama_root_rel(self._sandbox.repo_root, drama_rel.split("/")) != drama_rel:
            return ()
        if self._sandbox.check_read(drama_rel).rel != drama_rel:
            return ()
        shared = drama_ref.series_shared_rel(drama_rel)
        return (drama_rel,) if shared is None else (drama_rel, shared)

    def asset_file(self, drama_rel: str, name: str, search_exclude: Sequence[str]) -> ResolveResultDao:
        bases = self.search_bases(drama_rel)
        if not bases:
            return ResolveResultDao(status="not_found", name=name, reason="not_a_drama")
        images = [
            entry
            for base in bases
            for entry in self._files.list_files(base, search_exclude)
            if entry.ext in IMAGE_EXTS
        ]
        for step, matches in _asset_steps(name):
            hits = [entry for entry in images if matches(entry)]
            if hits:
                return self._decide(name, step, hits)
        return ResolveResultDao(status="not_found", name=name, reason="no_match")

    def shot_video(self, shot_dir_rel: str, name: str, search_exclude: Sequence[str]) -> ResolveResultDao:
        if not _usable_shot_dir(shot_dir_rel):
            return ResolveResultDao(status="not_found", name=name, reason="invalid_path")
        videos = [
            entry
            for entry in self._files.list_files(shot_dir_rel, search_exclude)
            if entry.ext in VIDEO_EXTS and not entry.is_link
        ]
        for step, wanted in (("exact_stem", name), ("swapped_alias", _swapped_alias(name))):
            hits = [entry for entry in videos if wanted is not None and entry.stem == wanted]
            if hits:
                return self._decide(name, step, hits)
        return ResolveResultDao(status="not_found", name=name, reason="no_match")

    def prev_shot_lastframe(self, shot_dir_rel: str, name: str) -> ResolveResultDao:
        if not _usable_shot_dir(shot_dir_rel):
            return ResolveResultDao(status="not_found", name=name, reason="invalid_path")
        parts = shot_dir_rel.split("/")
        match = _SHOT_DIR_RE.match(parts[-1])
        if match is None:
            return ResolveResultDao(status="not_found", name=name, reason="not_a_shot_dir")
        number = int(match.group(1))
        if number <= 1:
            return ResolveResultDao(status="not_found", name=name, reason="first_shot")
        previous = f"shot{number - 1:0{len(match.group(1))}d}"
        rel = "/".join((*parts[:-1], previous, f"{previous}_lastframe.png"))
        verdict = self._sandbox.check_read(rel)
        if verdict.path is not None and verdict.path.is_file():
            return ResolveResultDao(status="found", name=name, path=verdict.rel, step="previous_shot_lastframe")
        return ResolveResultDao(status="not_found", name=name, reason="missing", looked_for=rel)

    def _decide(self, name: str, step: str, hits: list[FileEntryDao]) -> ResolveResultDao:
        if len(hits) > 1:
            return ResolveResultDao(
                status="ambiguous", name=name, step=step, candidates=tuple(hit.rel for hit in hits)
            )
        hit = hits[0]
        if not hit.is_link:
            return ResolveResultDao(status="found", name=name, path=hit.rel, step=step)
        try:
            link = self._links.read(hit.rel)
        except LinkRejectedError as error:
            return ResolveResultDao(
                status="link_invalid", name=name, link_path=hit.rel, step=step, reason=error.reason
            )
        return ResolveResultDao(status="found", name=name, path=link.target_rel, link_path=hit.rel, step=step)


def _usable_shot_dir(shot_dir_rel: str) -> bool:
    return drama_ref.canonical_rel_violation(shot_dir_rel) is None and not drama_ref.inside_hard_excluded(shot_dir_rel)


def _asset_steps(name: str) -> list[tuple[str, Matcher]]:
    steps: list[tuple[str, Matcher]] = [("exact_stem", lambda entry: entry.stem == name)]
    if _ROUTING_KEY_RE.match(name):
        prefix = f"{name}_"
        steps.append(("routing_key_prefix", lambda entry: entry.stem.startswith(prefix)))
    if _SUBJECT_DIR_RE.match(name):
        steps.append(("subject_dir_main", lambda entry: entry.parent_name == name and entry.stem == name))
    return steps


def _swapped_alias(name: str) -> str | None:
    prefixed = _PREVIZ_PREFIX_RE.match(name)
    if prefixed is not None:
        return f"{prefixed.group(1)}_previz"
    suffixed = _PREVIZ_SUFFIX_RE.match(name)
    if suffixed is not None:
        return f"previz_{suffixed.group(1)}"
    return None
