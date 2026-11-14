from dataclasses import dataclass


@dataclass(frozen=True)
class SearchHitQdto:
    video_id: str
    url: str
    title: str
    channel: str
    duration: float
    view_count: int


@dataclass(frozen=True)
class SourceQdto:
    video_id: str
    title: str
    channel: str
    license_label: str
    duration: float
    subtitle_languages: tuple[str, ...]
    folder: str


@dataclass(frozen=True)
class CueHitQdto:
    source_id: str
    title: str
    language: str
    start: float
    end: float
    text: str


@dataclass(frozen=True)
class DownloadItemCdto:
    url: str
    video_id: str
    status: str
    message: str


@dataclass(frozen=True)
class DownloadBatchCdto:
    items: tuple[DownloadItemCdto, ...]
