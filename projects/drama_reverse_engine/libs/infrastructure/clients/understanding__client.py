from __future__ import annotations

from typing import Protocol

from libs.infrastructure.daos.shotanalysis__dao import EpisodeUnderstandingDao, ShotAnalysisDao


class VideoUnderstanding(Protocol):
    """NFR-O1 seam for the two-pass VLM reverse-engineering layer.
    Real backends: Gemini 2.5 Pro (primary), Qwen3-VL-plus (fallback)."""

    @property
    def available(self) -> bool: ...

    def episode_pass(self, video_abs_path: str, dialogue_lines: list[dict]) -> EpisodeUnderstandingDao: ...

    def shot_pass(
        self,
        clip_abs_path: str,
        prev_shot_summary: str,
        character_descriptors: dict[str, str],
        shot_index: int,
    ) -> ShotAnalysisDao: ...


class FallbackVideoUnderstanding:
    """FR-4.4: primary backend (Gemini) with per-call retry, degrading to the fallback
    (Qwen) after consecutive failures; degradation is surfaced via `last_backend`."""

    def __init__(self, primary: VideoUnderstanding, fallback: VideoUnderstanding, retries: int = 2) -> None:
        self._primary = primary
        self._fallback = fallback
        self._retries = retries
        self.last_backend = "primary"

    @property
    def available(self) -> bool:
        return self._primary.available or self._fallback.available

    def episode_pass(self, video_abs_path: str, dialogue_lines: list[dict]) -> EpisodeUnderstandingDao:
        return self._call("episode_pass", video_abs_path, dialogue_lines)

    def shot_pass(self, clip_abs_path: str, prev_shot_summary: str,
                  character_descriptors: dict[str, str], shot_index: int) -> ShotAnalysisDao:
        return self._call("shot_pass", clip_abs_path, prev_shot_summary, character_descriptors, shot_index)

    def _call(self, method: str, *args: object):
        last_exc: Exception | None = None
        if self._primary.available:
            for _ in range(self._retries):
                try:
                    result = getattr(self._primary, method)(*args)
                    self.last_backend = "primary"
                    return result
                except Exception as exc:
                    last_exc = exc
        if self._fallback.available:
            self.last_backend = "fallback"
            return getattr(self._fallback, method)(*args)
        raise last_exc or NotImplementedError("no video-understanding backend configured")


class NullVideoUnderstanding:
    available = False

    def episode_pass(self, video_abs_path: str, dialogue_lines: list[dict]) -> EpisodeUnderstandingDao:
        raise NotImplementedError("no video-understanding backend configured")

    def shot_pass(
        self, clip_abs_path: str, prev_shot_summary: str,
        character_descriptors: dict[str, str], shot_index: int,
    ) -> ShotAnalysisDao:
        raise NotImplementedError("no video-understanding backend configured")
