from dataclasses import dataclass


@dataclass(frozen=True)
class DownloadCdto:
    paths: tuple[str, ...]
