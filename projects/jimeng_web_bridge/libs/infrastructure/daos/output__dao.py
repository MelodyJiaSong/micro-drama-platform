from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MediaProbeDao:
    duration_s: float | None
    width: int
    height: int


@dataclass(frozen=True)
class OutputExpectationDao:
    size: int
    sha256: str
    duration_s: float | None
    ratio: str | None
    duration_tolerance_s: float
    ratio_tolerance: float = 0.01


@dataclass(frozen=True)
class FinalizedOutputDao:
    path_rel: str
    sidecar_rel: str | None
    sha256: str
    size: int
    duration_s: float | None
    width: int
    height: int


@dataclass(frozen=True)
class ArchivedFileDao:
    from_rel: str
    to_rel: str


@dataclass(frozen=True)
class PromotedFileDao:
    candidate_rel: str
    target_rel: str
    sidecar_rel: str
    sha256: str
    size: int
    archived: tuple[ArchivedFileDao, ...]
