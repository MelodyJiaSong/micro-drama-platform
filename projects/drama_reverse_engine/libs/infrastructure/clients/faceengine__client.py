from __future__ import annotations

from typing import Protocol

from libs.infrastructure.daos.face__dao import FaceDao


class FaceEngine(Protocol):
    """NFR-O1 seam for face detection + ArcFace embedding + quality scoring
    (InsightFace backend plugs in here)."""

    @property
    def available(self) -> bool: ...

    def detect(self, image_abs_path: str, frame_rel_path: str, at_s: float) -> list[FaceDao]: ...


class NullFaceEngine:
    available = False

    def detect(self, image_abs_path: str, frame_rel_path: str, at_s: float) -> list[FaceDao]:
        return []
