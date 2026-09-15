from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceItemDao:
    name: str
    label: str
    raw_token: str


@dataclass(frozen=True)
class LegacyReferenceDao:
    """`kinds` lists every legacy trait of the token, primary first: `no_at` > `slot_number` > `no_paren`."""

    kinds: tuple[str, ...]
    token: str

    @property
    def kind(self) -> str:
        return self.kinds[0]


@dataclass(frozen=True)
class ReferenceLineDao:
    line_count: int
    items: tuple[ReferenceItemDao, ...]
    legacy: tuple[LegacyReferenceDao, ...]
    unrecognized: tuple[str, ...]
    marker_count: int
    declares_none: bool

    @property
    def integrity_ok(self) -> bool:
        return self.marker_count == len(self.items)


@dataclass(frozen=True)
class ShotPromptDao:
    source_rel: str
    prompt: str
    negative_prompt: str | None
    ratio: str | None
    ratio_raw: str | None
    duration_s: int | None
    duration_raw: str | None
    references: ReferenceLineDao
