from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceLibraryCdto:
    character_count: int
    face_count: int
    degradations: list[str]
    skipped: bool = False
