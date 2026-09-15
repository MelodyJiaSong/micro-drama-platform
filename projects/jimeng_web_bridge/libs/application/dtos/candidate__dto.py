from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ArchivedFileCdto:
    from_rel: str
    to_rel: str


@dataclass(frozen=True)
class PromoteCdto:
    candidate_rel: str
    target_rel: str
    sidecar_rel: str
    sha256: str
    size: int
    archived: tuple[ArchivedFileCdto, ...]
