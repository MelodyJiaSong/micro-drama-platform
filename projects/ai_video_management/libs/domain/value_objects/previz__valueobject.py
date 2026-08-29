"""Previz render job state — the value objects the renderer reports progress with.

A previz render is minutes long (480 frames of EEVEE ≈ 15–30 min), so the API
cannot answer it in one request. The job runs detached and the UI polls this
snapshot.

Phases are ordered: `building` (rebuild the .blend from the scene master +
previz_config.toml, so a config edit takes effect without any manual step) →
`probing` (read frame_end out of the .blend) → `rendering`
(Blender writes the PNG sequence) → `muxing` (ffmpeg assembles the MP4) →
`done` / `failed` / `cancelled`.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Final

STATE_IDLE: Final[str] = "idle"
STATE_BUILDING: Final[str] = "building"
STATE_PROBING: Final[str] = "probing"
STATE_RENDERING: Final[str] = "rendering"
STATE_MUXING: Final[str] = "muxing"
STATE_DONE: Final[str] = "done"
STATE_FAILED: Final[str] = "failed"
STATE_CANCELLED: Final[str] = "cancelled"

TERMINAL_STATES: Final[frozenset[str]] = frozenset(
    {STATE_DONE, STATE_FAILED, STATE_CANCELLED}
)


@dataclass(frozen=True)
class PrevizJobSnapshot:
    """Immutable view of a render job, safe to hand across threads."""

    blend_rel: str
    state: str
    rendered_frames: int
    total_frames: int
    started_at: float
    finished_at: float | None
    message: str
    mp4_rel: str | None

    @property
    def is_terminal(self) -> bool:
        return self.state in TERMINAL_STATES

    @property
    def percent(self) -> int:
        """Whole-percent progress. Muxing is the last 3% — it is quick but not
        instant, and a bar frozen at 100% while ffmpeg runs reads as a hang."""
        if self.state == STATE_DONE:
            return 100
        if self.state == STATE_MUXING:
            return 97
        if self.state == STATE_BUILDING:
            return 1
        if self.total_frames <= 0:
            return 0
        ratio = self.rendered_frames / self.total_frames
        return max(0, min(96, int(ratio * 96)))
