from __future__ import annotations

from typing import Protocol

from libs.infrastructure.clients.ffmpeg__client import FfmpegClient
from libs.infrastructure.daos.shotspan__dao import ShotSpanDao


class ShotDetector(Protocol):
    """NFR-O1 seam — default is the ffmpeg scene filter; TransNetV2/AutoShot
    backends plug in behind the same protocol."""

    def detect(self, video_path: str, duration_s: float) -> list[ShotSpanDao]: ...


class FfmpegSceneShotDetector:
    def __init__(self, ffmpeg: FfmpegClient, threshold: float = 0.4) -> None:
        self._ffmpeg = ffmpeg
        self._threshold = threshold

    def detect(self, video_path: str, duration_s: float) -> list[ShotSpanDao]:
        cuts = [t for t in self._ffmpeg.scene_change_times(video_path, self._threshold) if 0.0 < t < duration_s]
        bounds = [0.0, *sorted(set(cuts)), duration_s]
        return [ShotSpanDao(start_s=a, end_s=b) for a, b in zip(bounds, bounds[1:]) if b - a > 1e-3]
