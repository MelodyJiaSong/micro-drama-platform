from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MediaInfoDao:
    duration_s: float
    width: int
    height: int
    decodable: bool
    detail: str = ""
