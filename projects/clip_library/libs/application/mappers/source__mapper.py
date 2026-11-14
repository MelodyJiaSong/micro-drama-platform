from datetime import datetime
from pathlib import Path

from libs.application.dtos.source__dto import CueHitQdto, SearchHitQdto, SourceQdto
from libs.common.options import LicenseKind
from libs.domain.entities.source__entity import SourceEntity
from libs.domain.value_objects.license__valueobject import License
from libs.infrastructure.daos.clip__dao import CueDao
from libs.infrastructure.daos.source__dao import SearchHitDao, SourceDao, SourceInfoDao


class SourceMapper:
    def hit(self, hit: SearchHitDao) -> SearchHitQdto:
        return SearchHitQdto(hit.video_id, hit.url, hit.title, hit.channel, hit.duration, hit.view_count)

    def entity(self, source: SourceDao) -> SourceEntity:
        return SourceEntity(source.video_id, source.duration,
                            License(LicenseKind(source.license_kind), source.license_note))

    def record(self, info: SourceInfoDao, entity: SourceEntity, video_file: str,
               subtitles: tuple[str, ...]) -> SourceDao:
        return SourceDao(info.video_id, info.url, info.title, info.channel, info.channel_url, info.duration,
                         info.upload_date, info.view_count, info.platform_license, entity.license.kind.value,
                         entity.license.note, video_file, subtitles,
                         datetime.now().isoformat(timespec="seconds"))

    def summary(self, source: SourceDao, folder: Path, languages: tuple[str, ...]) -> SourceQdto:
        return SourceQdto(source.video_id, source.title, source.channel, self.entity(source).license.label,
                          source.duration, languages, str(folder))

    def cue_hit(self, source: SourceDao, language: str, cue: CueDao) -> CueHitQdto:
        return CueHitQdto(source.video_id, source.title, language, cue.start, cue.end, cue.text)
