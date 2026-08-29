from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ShotSpanDao:
    start_s: float
    end_s: float
