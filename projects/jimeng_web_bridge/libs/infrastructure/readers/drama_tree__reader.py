from __future__ import annotations

import hashlib
import os
import re
from collections.abc import Sequence
from pathlib import Path

from libs.common import drama_ref
from libs.common.paths import RepoSandbox, is_reparse_point
from libs.infrastructure.daos.drama_tree__dao import (
    CharacterCardDao,
    DramaNodeDao,
    FileEntryDao,
    LinkTargetDao,
    ResolveResultDao,
)
from libs.infrastructure.errors.sandbox__error import LinkRejectedError, SandboxError
from libs.infrastructure.readers.file_index__reader import FileIndexReader
from libs.infrastructure.readers.link_json__reader import LINK_SUFFIX, LinkJsonReader
from libs.infrastructure.readers.reference_resolver__reader import IMAGE_EXTS, ReferenceResolverReader

_C_PREFIX_RE = re.compile(r"^(c\d+)_")
_HASH_CHUNK_BYTES: int = 1 << 20


class DramaTreeReader:
    def __init__(self, sandbox: RepoSandbox) -> None:
        self._sandbox: RepoSandbox = sandbox
        self._files: FileIndexReader = FileIndexReader(sandbox)
        self._links: LinkJsonReader = LinkJsonReader(sandbox)
        self._resolver: ReferenceResolverReader = ReferenceResolverReader(sandbox, self._files, self._links)

    def list_dramas(self) -> tuple[DramaNodeDao, ...]:
        nodes: list[DramaNodeDao] = []
        for entry in drama_ref.drama_candidate_dirs(self._sandbox.read_root):
            if drama_ref.is_series_dir(entry):
                children = tuple(
                    DramaNodeDao(child.name, self._rel(child), "drama", ())
                    for child in drama_ref.drama_candidate_dirs(entry)
                    if drama_ref.is_listable_drama(child)
                )
                if children:
                    nodes.append(DramaNodeDao(entry.name, self._rel(entry), "series", children))
            elif drama_ref.is_listable_drama(entry):
                nodes.append(DramaNodeDao(entry.name, self._rel(entry), "drama", ()))
        return tuple(nodes)

    def drama_root_of(self, rel: str) -> str | None:
        split = drama_ref.split_drama_rel(self._sandbox.repo_root, rel)
        return None if split is None else split[0]

    def search_bases(self, drama_rel: str) -> tuple[str, ...]:
        return self._resolver.search_bases(drama_rel)

    def list_files(self, drama_rel: str, search_exclude: Sequence[str]) -> tuple[FileEntryDao, ...]:
        return tuple(
            entry for base in self.search_bases(drama_rel) for entry in self._files.list_files(base, search_exclude)
        )

    def character_cards(self, drama_rel: str) -> tuple[CharacterCardDao, ...]:
        cards: list[CharacterCardDao] = []
        for base in self._existing_bases(drama_rel):
            for kind_dir in drama_ref.asset_kind_dirs(base, "characters"):
                cards.extend(self._card(card, drama_rel) for card in drama_ref.searchable_subdirs(kind_dir))
        return tuple(cards)

    def find_character_card(self, drama_rel: str, name: str) -> ResolveResultDao:
        hits = [card for card in self.character_cards(drama_rel) if name in (card.dir_name, card.character_name)]
        if not hits:
            return ResolveResultDao(status="not_found", name=name, reason="no_card")
        if len(hits) > 1:
            return ResolveResultDao(status="ambiguous", name=name, candidates=tuple(c.dir_rel for c in hits))
        step = "dir_name" if hits[0].dir_name == name else "character_name"
        return ResolveResultDao(status="found", name=name, path=hits[0].dir_rel, step=step)

    def asset_card_paths(self, drama_rel: str) -> tuple[str, ...]:
        found: list[str] = []
        for base in self._existing_bases(drama_rel):
            for kind in drama_ref.ASSET_KIND_DIR_NAMES:
                for kind_dir in drama_ref.asset_kind_dirs(base, kind):
                    for current, dirnames, filenames in os.walk(kind_dir):
                        dirnames[:] = sorted(
                            n
                            for n in dirnames
                            if not n.startswith("_")
                            and not drama_ref.is_hard_excluded_name(n)
                            and not is_reparse_point(Path(current) / n)
                        )
                        card_md = f"{Path(current).name}.md"
                        if Path(current) != kind_dir and card_md in filenames:
                            found.append(self._rel(Path(current) / card_md))
        return tuple(found)

    def resolve_asset_file(self, drama_rel: str, name: str, search_exclude: Sequence[str]) -> ResolveResultDao:
        return self._resolver.asset_file(drama_rel, name, search_exclude)

    def resolve_shot_video(self, shot_dir_rel: str, name: str, search_exclude: Sequence[str]) -> ResolveResultDao:
        return self._resolver.shot_video(shot_dir_rel, name, search_exclude)

    def resolve_prev_shot_lastframe(self, shot_dir_rel: str, name: str) -> ResolveResultDao:
        return self._resolver.prev_shot_lastframe(shot_dir_rel, name)

    def read_link(self, link_rel: str) -> LinkTargetDao:
        return self._links.read(link_rel)

    def sha256(self, rel: str) -> str:
        verdict = self._sandbox.check_read(rel)
        if verdict.path is None:
            raise SandboxError(verdict.violation or "rejected", verdict.rel)
        digest = hashlib.sha256()
        try:
            if not verdict.path.is_file():
                raise SandboxError("not_a_file", verdict.rel)
            with verdict.path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(_HASH_CHUNK_BYTES), b""):
                    digest.update(chunk)
        except OSError as error:
            raise SandboxError("unreadable", verdict.rel) from error
        return digest.hexdigest()

    def _existing_bases(self, drama_rel: str) -> list[Path]:
        paths = (self._sandbox.check_read(base).path for base in self.search_bases(drama_rel))
        return [path for path in paths if path is not None and path.is_dir()]

    def _card(self, card: Path, drama_rel: str) -> CharacterCardDao:
        match = _C_PREFIX_RE.match(card.name)
        return CharacterCardDao(
            dir_rel=self._rel(card),
            dir_name=card.name,
            character_name=card.name[match.end():] if match else card.name,
            c_prefix=match.group(1) if match else None,
            linked_source_drama=self._linked_source(card, drama_rel),
        )

    def _linked_source(self, card: Path, drama_rel: str) -> str | None:
        for child in sorted(card.iterdir()):
            inner = child.name[: -len(LINK_SUFFIX)]
            if not child.name.endswith(LINK_SUFFIX) or os.path.splitext(inner)[1].lower() not in IMAGE_EXTS:
                continue
            try:
                link = self._links.read(self._rel(child))
            except LinkRejectedError:
                continue
            source = self.drama_root_of(link.target_rel)
            if source is not None and source != drama_rel:
                return source
        return None

    def _rel(self, path: Path) -> str:
        return self._sandbox.rel(path) or path.as_posix()
