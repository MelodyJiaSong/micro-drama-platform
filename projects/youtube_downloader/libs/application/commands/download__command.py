from threading import Event
from typing import Callable

from libs.application.dtos.download__dto import DownloadCdto
from libs.application.mappers.download__mapper import DownloadMapper
from libs.domain.value_objects.download__valueobject import Download
from libs.infrastructure.errors.download__error import DownloadCancelledError, DownloadFailedError
from libs.infrastructure.writers.download__writer import DownloadWriter


class DownloadCommand:
    def __init__(self, writer: DownloadWriter, mapper: DownloadMapper) -> None:
        self.writer = writer
        self.mapper = mapper

    def download(self, url: str, directory: str, mode: str, height: int, browser: str,
                 cancel: Event, notify: Callable[[str], None]) -> DownloadCdto:
        request = Download(url, directory, mode, height, browser)
        try:
            paths = self.writer.download(self.mapper.to_dao(request), cancel, notify)
        except DownloadCancelledError as error:
            raise InterruptedError("已取消；保留的分片可在同目录重试续传。") from error
        except DownloadFailedError as error:
            raise RuntimeError(str(error)) from error
        return DownloadCdto(paths)
