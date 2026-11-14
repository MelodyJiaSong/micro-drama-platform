from dataclasses import dataclass


@dataclass(frozen=True)
class SearchHitDao:
    video_id: str
    url: str
    title: str
    channel: str
    duration: float
    view_count: int


@dataclass(frozen=True)
class SourceInfoDao:
    video_id: str
    url: str
    title: str
    channel: str
    channel_url: str
    duration: float
    upload_date: str
    view_count: int
    platform_license: str
    raw_json: str


@dataclass(frozen=True)
class SourceDao:
    video_id: str
    url: str
    title: str
    channel: str
    channel_url: str
    duration: float
    upload_date: str
    view_count: int
    platform_license: str
    license_kind: str
    license_note: str
    video_file: str
    subtitle_files: tuple[str, ...]
    downloaded_at: str
