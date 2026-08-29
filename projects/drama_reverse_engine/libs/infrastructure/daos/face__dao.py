from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FaceDao:
    frame_rel_path: str
    at_s: float
    bbox: tuple[int, int, int, int]
    embedding: tuple[float, ...]
    quality: float
