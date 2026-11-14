from libs.application.dtos.source__dto import CueHitQdto, SearchHitQdto, SourceQdto
from libs.application.mappers.source__mapper import SourceMapper
from libs.common.options import DURATIONS, ORDERS
from libs.common.types import Auth
from libs.infrastructure.readers.source__reader import SourceReader
from libs.infrastructure.readers.subtitle__reader import SubtitleReader
from libs.infrastructure.readers.youtube__reader import YoutubeReader


class SourceQuery:
    def __init__(self, youtube: YoutubeReader, sources: SourceReader, subtitles: SubtitleReader,
                 mapper: SourceMapper) -> None:
        self._youtube = youtube
        self._sources = sources
        self._subtitles = subtitles
        self._mapper = mapper

    def search(self, query: str, limit: int, duration: str, order: str, cc_only: bool,
               auth: Auth) -> list[SearchHitQdto]:
        hits = self._youtube.search(query, limit, DURATIONS[duration], ORDERS[order], cc_only, auth)
        return [self._mapper.hit(hit) for hit in hits]

    def library(self) -> list[SourceQdto]:
        rows = []
        for source in self._sources.all():
            languages = tuple(self._subtitles.language(self._sources.path(source.video_id, name))
                              for name in source.subtitle_files)
            rows.append(self._mapper.summary(source, self._sources.folder(source.video_id), languages))
        return rows

    def find(self, keyword: str, source_id: str, limit: int) -> list[CueHitQdto]:
        needle = keyword.casefold()
        sources = [self._sources.load(source_id)] if source_id else self._sources.all()
        hits: list[CueHitQdto] = []
        for source in sources:
            seen: set[tuple] = set()
            for name in source.subtitle_files:
                path = self._sources.path(source.video_id, name)
                language = self._subtitles.language(path)
                cues = self._subtitles.read(path)
                if cues in seen:
                    continue
                seen.add(cues)
                for cue in cues:
                    if needle in cue.text.casefold():
                        hits.append(self._mapper.cue_hit(source, language, cue))
                        if len(hits) >= limit:
                            return hits
        return hits
