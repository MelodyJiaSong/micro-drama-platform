import html
from pathlib import Path
import re

from libs.infrastructure.daos.clip__dao import CueDao

_TIMING = re.compile(r"((?:\d+:)?\d{2}:\d{2}\.\d{3})\s+-->\s+((?:\d+:)?\d{2}:\d{2}\.\d{3})")
_TAG = re.compile(r"<[^>]+>")


def _seconds(stamp: str) -> float:
    total = 0.0
    for part in stamp.split(":"):
        total = total * 60 + float(part)
    return total


class SubtitleReader:
    def read(self, path: Path) -> tuple[CueDao, ...]:
        cues: list[CueDao] = []
        last_line = ""
        for block in re.split(r"\r?\n\r?\n", path.read_text(encoding="utf-8", errors="replace")):
            lines = block.strip().splitlines()
            timing_index = next((i for i, line in enumerate(lines) if _TIMING.search(line)), None)
            if timing_index is None:
                continue
            match = _TIMING.search(lines[timing_index])
            assert match is not None
            fresh = []
            for raw in lines[timing_index + 1:]:
                line = html.unescape(_TAG.sub("", raw)).strip()
                if line and line != last_line:
                    fresh.append(line)
                    last_line = line
            if fresh:
                cues.append(CueDao(_seconds(match.group(1)), _seconds(match.group(2)), " ".join(fresh)))
        return tuple(CueDao(cue.start, min(cue.end, after.start) if after.start > cue.start else cue.end, cue.text)
                     for cue, after in zip(cues, cues[1:] + [CueDao(float("inf"), 0.0, "")]))

    def language(self, path: Path) -> str:
        parts = path.name.split(".")
        return parts[-2] if len(parts) >= 3 else "unknown"
