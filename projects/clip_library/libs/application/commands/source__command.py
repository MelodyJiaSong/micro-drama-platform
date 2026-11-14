from typing import Callable

from libs.application.dtos.source__dto import DownloadBatchCdto, DownloadItemCdto
from libs.application.mappers.source__mapper import SourceMapper
from libs.common.options import DURATIONS, ORDERS, LicenseKind
from libs.common.types import Auth
from libs.domain.entities.source__entity import SourceEntity
from libs.domain.errors.license__error import LicenseError
from libs.domain.value_objects.license__valueobject import License
from libs.infrastructure.errors.library__error import LibraryError
from libs.infrastructure.readers.source__reader import SourceReader
from libs.infrastructure.readers.youtube__reader import YoutubeReader
from libs.infrastructure.writers.source__writer import SourceWriter


class SourceCommand:
    def __init__(self, youtube: YoutubeReader, sources: SourceReader, writer: SourceWriter,
                 mapper: SourceMapper) -> None:
        self._youtube = youtube
        self._sources = sources
        self._writer = writer
        self._mapper = mapper

    def download(self, urls: list[str], claimed: LicenseKind | None, note: str, sub_langs: str,
                 auth: Auth, notify: Callable[[str], None]) -> DownloadBatchCdto:
        items = []
        for index, url in enumerate(urls, 1):
            notify(f"[{index}/{len(urls)}] {url}")
            items.append(self._one(url, claimed, note, sub_langs, auth, notify))
            notify(f"  → {items[-1].status} {items[-1].message}")
        return DownloadBatchCdto(tuple(items))

    def download_search(self, query: str, limit: int, duration: str, order: str, cc_only: bool,
                        claimed: LicenseKind | None, note: str, sub_langs: str, auth: Auth,
                        notify: Callable[[str], None]) -> DownloadBatchCdto:
        hits = self._youtube.search(query, limit, DURATIONS[duration], ORDERS[order], cc_only, auth)
        notify(f"搜索到 {len(hits)} 条")
        return self.download([hit.url for hit in hits], claimed, note, sub_langs, auth, notify)

    def _one(self, url: str, claimed: LicenseKind | None, note: str, sub_langs: str, auth: Auth,
             notify: Callable[[str], None]) -> DownloadItemCdto:
        try:
            info = self._youtube.info(url, auth)
            if self._sources.exists(info.video_id):
                return DownloadItemCdto(url, info.video_id, "已存在", info.title)
            entity = SourceEntity(info.video_id, info.duration,
                                  License.resolve(claimed, info.platform_license, note))
            video, subtitles = self._writer.download(info, sub_langs, auth, notify)
            self._writer.save(self._mapper.record(info, entity, video, subtitles))
            return DownloadItemCdto(url, info.video_id, "完成", f"{entity.license.label} · {info.title}")
        except (LicenseError, LibraryError) as error:
            return DownloadItemCdto(url, "", "失败", str(error))
