from dataclasses import dataclass

from libs.domain.value_objects.license__valueobject import License
from libs.domain.value_objects.time_range__valueobject import TimeRange


@dataclass
class ClipEntity:
    source_id: str
    time_range: TimeRange
    license: License
    vertical: bool

    @property
    def clip_id(self) -> str:
        start = int(self.time_range.start * 1000)
        end = int(self.time_range.end * 1000)
        return f"{self.source_id}_{start}-{end}{'_v' if self.vertical else ''}"
