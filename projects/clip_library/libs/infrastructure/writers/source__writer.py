from dataclasses import asdict
import json
from pathlib import Path
from typing import Callable

from libs.common.options import BATCH_SLEEP, INFO_FILE, MAX_HEIGHT, SOURCE_RECORD, SOURCES_DIR, VIDEO_STEM
from libs.common.types import Auth
from libs.infrastructure.clients.ytdlp__client import YtdlpClient
from libs.infrastructure.daos.source__dao import SourceDao, SourceInfoDao
from libs.infrastructure.errors.library__error import VideoFileMissingError

_VIDEO_SUFFIXES = (".mp4", ".mkv", ".webm")


class SourceWriter:
    def __init__(self, library: Path, ytdlp: YtdlpClient) -> None:
        self._root = library / SOURCES_DIR
        self._ytdlp = ytdlp

    def download(self, info: SourceInfoDao, sub_langs: str, auth: Auth,
                 notify: Callable[[str], None]) -> tuple[str, tuple[str, ...]]:
        folder = self._root / info.video_id
        folder.mkdir(parents=True, exist_ok=True)
        info_path = folder / INFO_FILE
        info_path.write_text(info.raw_json, encoding="utf-8")
        self._ytdlp.stream([
            "--load-info-json", str(info_path), "-P", str(folder), "-o", f"{VIDEO_STEM}.%(ext)s",
            "-f", f"bv*[height<={MAX_HEIGHT}]+ba/b[height<={MAX_HEIGHT}]", "-S", "ext:mp4:m4a",
            "--merge-output-format", "mp4", "--write-subs", "--write-auto-subs", "--sub-langs", sub_langs,
            "--sub-format", "vtt", "--ignore-errors", "--sleep-interval", str(BATCH_SLEEP[0]),
            "--max-sleep-interval", str(BATCH_SLEEP[1]), "--sleep-subtitles", "3",
        ], auth, notify)
        videos = [path for path in folder.glob(f"{VIDEO_STEM}.*") if path.suffix in _VIDEO_SUFFIXES]
        if not videos:
            raise VideoFileMissingError(str(folder))
        subtitles = tuple(sorted(path.name for path in folder.glob(f"{VIDEO_STEM}.*.vtt")))
        return videos[0].name, subtitles

    def save(self, source: SourceDao) -> Path:
        record = self._root / source.video_id / SOURCE_RECORD
        record.write_text(json.dumps(asdict(source), ensure_ascii=False, indent=2), encoding="utf-8")
        return record
