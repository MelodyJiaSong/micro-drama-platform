from __future__ import annotations

from dataclasses import dataclass

from libs.infrastructure.daos.shot_prompt__dao import ReferenceLineDao


@dataclass(frozen=True)
class AssetBlockDao:
    """A ```text block whose first line starts with a routing key; image/video is decided in domain."""

    key: str
    first_line: str
    body: str
    heading: str | None
    fields: tuple[str, ...]
    ratio: str | None
    duration_s: int | None
    references: ReferenceLineDao


@dataclass(frozen=True)
class AssetCardDao:
    source_rel: str
    card_dir_name: str
    subject_kind: str | None
    folder_key: str | None
    blocks: tuple[AssetBlockDao, ...]
