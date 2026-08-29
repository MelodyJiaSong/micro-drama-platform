from __future__ import annotations

from dataclasses import dataclass

from libs.common.constants import FPS
from libs.domain.errors.shot__error import InvalidTimeRangeError


@dataclass(frozen=True)
class TimeRange:
    start_s: float
    end_s: float

    def __post_init__(self) -> None:
        if self.start_s < 0 or self.end_s <= self.start_s:
            raise InvalidTimeRangeError(f"invalid range [{self.start_s}, {self.end_s}]")

    @property
    def duration_s(self) -> float:
        return self.end_s - self.start_s

    @property
    def start_frame(self) -> int:
        return round(self.start_s * FPS)

    @property
    def end_frame(self) -> int:
        return round(self.end_s * FPS)

    @property
    def frame_count(self) -> int:
        return self.end_frame - self.start_frame

    def frames_apart(self, other: TimeRange) -> int:
        return abs(self.frame_count - other.frame_count)
