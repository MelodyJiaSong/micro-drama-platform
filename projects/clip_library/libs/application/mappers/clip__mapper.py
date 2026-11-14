from pathlib import Path

from libs.application.dtos.clip__dto import ClipCdto
from libs.domain.entities.clip__entity import ClipEntity
from libs.infrastructure.daos.clip__dao import ClipDao, CueDao
from libs.infrastructure.daos.source__dao import SourceDao

_TITLE_CHARS = 24


def attribution(source: SourceDao, label: str) -> str:
    title = source.title if len(source.title) <= _TITLE_CHARS else source.title[:_TITLE_CHARS] + "…"
    return f"来源：{source.channel} · {label}\n《{title}》"


class ClipMapper:
    def dao(self, clip: ClipEntity, source: SourceDao, video: Path,
            subtitles: dict[str, tuple[CueDao, ...]]) -> ClipDao:
        return ClipDao(clip.clip_id, source.video_id, source.url, source.title, source.channel,
                       clip.license.kind.value, clip.license.label, clip.license.note,
                       clip.time_range.start, clip.time_range.end, clip.vertical, str(video),
                       attribution(source, clip.license.label), subtitles)

    def result(self, clip: ClipEntity, file: Path, subtitles: tuple[Path, ...]) -> ClipCdto:
        return ClipCdto(clip.clip_id, str(file), tuple(str(path) for path in subtitles),
                        clip.license.label, clip.time_range.seconds)
