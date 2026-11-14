from dataclasses import dataclass

from libs.domain.entities.clip__entity import ClipEntity
from libs.domain.errors.clip__error import ClipOutOfRangeError, ClipTooLongError
from libs.domain.value_objects.license__valueobject import License
from libs.domain.value_objects.time_range__valueobject import TimeRange

_END_TOLERANCE = 0.5


@dataclass
class SourceEntity:
    source_id: str
    duration: float
    license: License

    def plan_clip(self, time_range: TimeRange, vertical: bool) -> ClipEntity:
        if self.duration and time_range.end > self.duration + _END_TOLERANCE:
            raise ClipOutOfRangeError(time_range.end, self.duration)
        limit = self.license.max_clip_seconds
        if limit is not None and time_range.seconds > limit:
            raise ClipTooLongError(time_range.seconds, limit)
        return ClipEntity(self.source_id, time_range, self.license, vertical)
