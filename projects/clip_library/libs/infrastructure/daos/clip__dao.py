from dataclasses import dataclass


@dataclass(frozen=True)
class CueDao:
    start: float
    end: float
    text: str


@dataclass(frozen=True)
class ClipDao:
    clip_id: str
    source_id: str
    url: str
    title: str
    channel: str
    license_kind: str
    license_label: str
    license_note: str
    start: float
    end: float
    vertical: bool
    video_file: str
    attribution: str
    subtitles: dict[str, tuple[CueDao, ...]]
