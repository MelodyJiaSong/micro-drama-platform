from dataclasses import dataclass
import re

from libs.domain.errors.clip__error import EmptyRangeError, InvalidTimeError

_TIME = re.compile(r"^(?:(\d+):)?(?:(\d+):)?(\d+(?:\.\d+)?)$")


def parse_seconds(text: str) -> float:
    match = _TIME.match(text.strip())
    if match is None:
        raise InvalidTimeError(text)
    parts = [part for part in match.groups() if part is not None]
    seconds = 0.0
    for part in parts:
        seconds = seconds * 60 + float(part)
    return seconds


@dataclass(frozen=True)
class TimeRange:
    start: float
    end: float

    def __post_init__(self) -> None:
        if self.end <= self.start or self.start < 0:
            raise EmptyRangeError()

    @classmethod
    def parse(cls, start: str, end: str) -> "TimeRange":
        return cls(parse_seconds(start), parse_seconds(end))

    @property
    def seconds(self) -> float:
        return self.end - self.start

    def overlaps(self, start: float, end: float) -> bool:
        return start < self.end and end > self.start
