from dataclasses import dataclass


@dataclass(frozen=True)
class DownloadDao:
    url: str
    directory: str
    mode: str
    height: int
    browser: str
