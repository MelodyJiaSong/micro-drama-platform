from datetime import datetime
import json
from pathlib import Path

from libs.common.options import CLIP_LEDGER, CLIPS_DIR, FONT_FILES, VERTICAL_SIZE
from libs.infrastructure.clients.ffmpeg__client import FfmpegClient
from libs.infrastructure.daos.clip__dao import ClipDao, CueDao
from libs.infrastructure.errors.library__error import FontMissingError

_ATTRIBUTION = "attribution.txt"
_CLIP = "clip.mp4"


def _stamp(seconds: float) -> str:
    millis = round(seconds * 1000)
    return f"{millis // 3600000:02}:{millis // 60000 % 60:02}:{millis // 1000 % 60:02},{millis % 1000:03}"


def _srt(cues: tuple[CueDao, ...], start: float, end: float) -> str:
    rows = [cue for cue in cues if cue.start < end and cue.end > start]
    return "\n".join(f"{i}\n{_stamp(max(0.0, c.start - start))} --> {_stamp(min(end, c.end) - start)}\n{c.text}\n"
                     for i, c in enumerate(rows, 1))


class ClipWriter:
    def __init__(self, library: Path, ffmpeg: FfmpegClient) -> None:
        self._library = library
        self._ffmpeg = ffmpeg

    def write(self, clip: ClipDao) -> tuple[Path, tuple[Path, ...]]:
        folder = self._library / CLIPS_DIR / clip.clip_id
        folder.mkdir(parents=True, exist_ok=True)
        (folder / _ATTRIBUTION).write_text(clip.attribution, encoding="utf-8")
        output = folder / _CLIP
        self._ffmpeg.run(["-ss", f"{clip.start:.3f}", "-i", clip.video_file, "-t", f"{clip.end - clip.start:.3f}",
                          "-filter_complex", self._graph(clip.vertical), "-map", "[v]", "-map", "0:a?",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "160k",
                          "-movflags", "+faststart"], output)
        subtitles = []
        for language, cues in clip.subtitles.items():
            path = folder / f"clip.{language}.srt"
            path.write_text(_srt(cues, clip.start, clip.end), encoding="utf-8")
            subtitles.append(path)
        self._ledger(clip, output)
        return output, tuple(subtitles)

    def _graph(self, vertical: bool) -> str:
        font = next((path for path in FONT_FILES if path.is_file()), None)
        if font is None:
            raise FontMissingError()
        escaped = font.as_posix().replace(":", "\\:")
        draw = (f"drawtext=fontfile='{escaped}':textfile={_ATTRIBUTION}:fontcolor=white:"
                f"fontsize=w/{30 if vertical else 40}:"
                "line_spacing=8:box=1:boxcolor=black@0.55:boxborderw=14:x=(w-text_w)/2:y=h-text_h-h/14")
        if not vertical:
            return f"[0:v]{draw}[v]"
        width, height = VERTICAL_SIZE
        return (f"[0:v]split[a][b];[a]scale={width}:{height}:force_original_aspect_ratio=increase,"
                f"crop={width}:{height},boxblur=20:2[bg];[b]scale={width}:-2[fg];"
                f"[bg][fg]overlay=(W-w)/2:(H-h)/2,{draw}[v]")

    def _ledger(self, clip: ClipDao, output: Path) -> None:
        entry = {"created_at": datetime.now().isoformat(timespec="seconds"), "clip_id": clip.clip_id,
                 "source_id": clip.source_id, "url": clip.url, "title": clip.title, "channel": clip.channel,
                 "license": clip.license_kind, "license_note": clip.license_note,
                 "start": clip.start, "end": clip.end, "file": str(output)}
        with (self._library / CLIP_LEDGER).open("a", encoding="utf-8") as ledger:
            ledger.write(json.dumps(entry, ensure_ascii=False) + "\n")
