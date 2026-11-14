from dataclasses import dataclass


@dataclass(frozen=True)
class ClipCdto:
    clip_id: str
    file: str
    subtitles: tuple[str, ...]
    license_label: str
    seconds: float
