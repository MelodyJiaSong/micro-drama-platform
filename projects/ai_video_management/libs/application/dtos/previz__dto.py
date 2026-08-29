"""Previz-aggregate DTOs: one status Qdto, shared by the start and poll endpoints.

Start and poll return the same shape on purpose — the UI holds a single piece
of state and overwrites it with whatever came back, whether that was the POST
that launched the job or the GET that polled it.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PrevizStatusQdto:
    blend: str
    state: str
    rendered_frames: int
    total_frames: int
    percent: int
    message: str
    mp4: str | None
    elapsed_seconds: int

    def to_payload(self) -> dict[str, Any]:
        return {
            "blend": self.blend,
            "state": self.state,
            "rendered_frames": self.rendered_frames,
            "total_frames": self.total_frames,
            "percent": self.percent,
            "message": self.message,
            "mp4": self.mp4,
            "elapsed_seconds": self.elapsed_seconds,
        }
