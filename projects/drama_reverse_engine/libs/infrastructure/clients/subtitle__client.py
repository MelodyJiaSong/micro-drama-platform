from __future__ import annotations

from typing import Protocol

from libs.infrastructure.daos.subtitleline__dao import SubtitleLineDao


class SubtitleExtractor(Protocol):
    """NFR-O1 seam for burned-in subtitle OCR (PaddleOCR/VideoSubFinder backends)."""

    @property
    def available(self) -> bool: ...

    def extract(self, video_path: str) -> list[SubtitleLineDao]: ...


class NullSubtitleExtractor:
    """Degradation stand-in when no OCR backend is installed (FR-2.3 ASR-only path)."""

    available = False

    def extract(self, video_path: str) -> list[SubtitleLineDao]:
        return []
