from libs.application.dtos.clip__dto import ClipCdto
from libs.application.mappers.clip__mapper import ClipMapper
from libs.application.mappers.source__mapper import SourceMapper
from libs.domain.value_objects.time_range__valueobject import TimeRange
from libs.infrastructure.readers.source__reader import SourceReader
from libs.infrastructure.readers.subtitle__reader import SubtitleReader
from libs.infrastructure.writers.clip__writer import ClipWriter


class ClipCommand:
    def __init__(self, sources: SourceReader, subtitles: SubtitleReader, writer: ClipWriter,
                 source_mapper: SourceMapper, mapper: ClipMapper) -> None:
        self._sources = sources
        self._subtitles = subtitles
        self._writer = writer
        self._source_mapper = source_mapper
        self._mapper = mapper

    def cut(self, source_id: str, start: str, end: str, vertical: bool) -> ClipCdto:
        source = self._sources.load(source_id)
        clip = self._source_mapper.entity(source).plan_clip(TimeRange.parse(start, end), vertical)
        cues = {}
        for name in source.subtitle_files:
            path = self._sources.path(source_id, name)
            read = self._subtitles.read(path)
            if read not in cues.values():
                cues[self._subtitles.language(path)] = read
        video = self._sources.path(source_id, source.video_file)
        file, subtitles = self._writer.write(self._mapper.dao(clip, source, video, cues))
        return self._mapper.result(clip, file, subtitles)
