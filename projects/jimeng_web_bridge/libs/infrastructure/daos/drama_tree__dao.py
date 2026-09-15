from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DramaNodeDao:
    name: str
    path: str
    node_type: str
    children: tuple[DramaNodeDao, ...]


@dataclass(frozen=True)
class FileEntryDao:
    rel: str
    parent_name: str
    stem: str
    ext: str
    is_link: bool


@dataclass(frozen=True)
class LinkTargetDao:
    link_rel: str
    target_rel: str
    note: str | None


@dataclass(frozen=True)
class CharacterCardDao:
    dir_rel: str
    dir_name: str
    character_name: str
    c_prefix: str | None
    linked_source_drama: str | None


@dataclass(frozen=True)
class ResolveResultDao:
    """`status`: found | not_found | ambiguous | link_invalid. `path` is the link target when `link_path` is set."""

    status: str
    name: str
    path: str | None = None
    link_path: str | None = None
    candidates: tuple[str, ...] = ()
    step: str | None = None
    reason: str | None = None
    looked_for: str | None = None
