from libs.domain.value_objects.download__valueobject import Download
from libs.infrastructure.daos.download__dao import DownloadDao


class DownloadMapper:
    def to_dao(self, request: Download) -> DownloadDao:
        return DownloadDao(request.url, request.directory, request.mode, request.height, request.browser)
