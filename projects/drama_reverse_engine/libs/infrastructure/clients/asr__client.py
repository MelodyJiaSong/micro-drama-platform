from __future__ import annotations

from typing import Protocol

from libs.infrastructure.daos.subtitleline__dao import SubtitleLineDao


class AsrTranscriber(Protocol):
    """NFR-O1 seam for speech transcription (FunASR/Paraformer backend)."""

    @property
    def available(self) -> bool: ...

    def transcribe(self, video_path: str) -> list[SubtitleLineDao]: ...


class NullAsrTranscriber:
    available = False

    def transcribe(self, video_path: str) -> list[SubtitleLineDao]:
        return []
