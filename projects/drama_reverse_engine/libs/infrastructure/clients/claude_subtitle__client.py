from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from libs.infrastructure.clients.claudecli__client import ClaudeCliClient, extract_json_object
from libs.infrastructure.clients.ffmpeg__client import FfmpegClient
from libs.infrastructure.daos.subtitleline__dao import SubtitleLineDao
from libs.infrastructure.errors.claudecli__error import ClaudeCliError

_MAX_FRAMES = 240
_CHUNK = 30
_RETRY_SUFFIX = "\n（上次输出不是合法 JSON，这次务必只输出一个合法的 JSON 对象，逐行都带 \"text\" 键。）"

_ROW_RE = re.compile(r'\{\s*"i"\s*:\s*(\d+)\s*,\s*"text"\s*:\s*("(?:[^"\\]|\\.)*"|null)\s*\}')


def salvage_frame_rows(reply: str) -> list[dict]:
    """One malformed row (real run 2026-07-18: {"i":129,null}) must not sink the whole
    chunk — regex out every well-formed {"i":N,"text":...} row and drop the broken ones."""
    return [{"i": int(m.group(1)), "text": json.loads(m.group(2))} for m in _ROW_RE.finditer(reply)]


def merge_frame_texts(entries: list[tuple[float, str]], half_step_s: float) -> list[SubtitleLineDao]:
    """Consecutive frames showing the same subtitle text collapse into one timed line;
    a frame with no subtitle breaks the run."""
    lines: list[SubtitleLineDao] = []
    current: str = ""
    start = end = 0.0
    for at_s, text in entries:
        text = (text or "").strip()
        if text and text == current:
            end = at_s
            continue
        if current:
            lines.append(SubtitleLineDao(current, max(0.0, start - half_step_s), end + half_step_s,
                                         source="ocr", confidence=0.7))
        current = text
        start = end = at_s
    if current:
        lines.append(SubtitleLineDao(current, max(0.0, start - half_step_s), end + half_step_s,
                                     source="ocr", confidence=0.7))
    return lines


class ClaudeSubtitleExtractor:
    """SubtitleExtractor backend on the local Claude Code CLI (zero key, follow-up 002):
    sample ~1 fps frames, batch them through headless sessions that transcribe the
    burned-in dialogue subtitle per frame, then merge consecutive identical texts into
    timed lines. Confidence is capped at 0.7 — frame sampling can clip line boundaries,
    so ASR reconciliation (when installed) still adds value."""

    def __init__(self, cli: ClaudeCliClient, ffmpeg: FfmpegClient,
                 max_frames: int = _MAX_FRAMES, chunk_size: int = _CHUNK, max_turns: int = 40) -> None:
        self._cli = cli
        self._ffmpeg = ffmpeg
        self._max_frames = max_frames
        self._chunk_size = chunk_size
        self._max_turns = max_turns

    @property
    def available(self) -> bool:
        return self._cli.available

    def extract(self, video_path: str) -> list[SubtitleLineDao]:
        duration = self._ffmpeg.probe(video_path).duration_s
        if duration <= 0:
            return []
        count = min(self._max_frames, max(1, int(duration)))
        step = duration / count
        times = [(i + 0.5) * step for i in range(count)]

        source = Path(video_path)
        frames_dir = source.parent / f".claude_subs_{source.stem}"
        shutil.rmtree(frames_dir, ignore_errors=True)
        frames_dir.mkdir(parents=True, exist_ok=True)
        entries: list[tuple[float, str]] = []
        try:
            paths = []
            for i, at_s in enumerate(times):
                out = frames_dir / f"f{i:04d}.jpg"
                self._ffmpeg.extract_frame(str(source), at_s, str(out))
                paths.append(out)
            for chunk_start in range(0, len(paths), self._chunk_size):
                chunk = list(range(chunk_start, min(chunk_start + self._chunk_size, len(paths))))
                listing = "\n".join(f"- 帧{i} @ {times[i]:.1f}s: {paths[i]}" for i in chunk)
                prompt = (
                    "逐张用 Read 工具查看以下视频抽帧，转写每帧画面下方烧录的对白硬字幕行"
                    "（只要主对白字幕原文；忽略台标/水印/角色名片/片头片尾字幕；该帧无对白字幕则为 null）。"
                    '只输出一个 JSON 对象，不要输出其他文字：{"frames":[{"i":帧号,"text":"字幕原文或null"}]}。'
                    "无论帧里有没有字幕（哪怕是测试图/纯色）都只输出该 JSON——没有字幕就全为 null，"
                    "绝不输出 JSON 以外的解释或拒绝。\n"
                    + listing
                )
                rows = self._chunk_rows(prompt, frames_dir)
                by_index = {int(row.get("i", -1)): row.get("text") for row in rows}
                for i in chunk:
                    text = by_index.get(i)
                    entries.append((times[i], text if isinstance(text, str) else ""))
        finally:
            shutil.rmtree(frames_dir, ignore_errors=True)
        return merge_frame_texts(entries, half_step_s=step / 2)

    def _chunk_rows(self, prompt: str, frames_dir: Path) -> list[dict]:
        reply = self._cli.run_text(prompt, read_dirs=(str(frames_dir),), max_turns=self._max_turns)
        rows = self._parse_rows(reply)
        if rows is None:
            reply = self._cli.run_text(prompt + _RETRY_SUFFIX, read_dirs=(str(frames_dir),),
                                       max_turns=self._max_turns)
            rows = self._parse_rows(reply)
            if rows is None:
                raise ClaudeCliError(f"subtitle chunk reply unparseable after retry: {reply[-300:]!r}")
        return rows

    @staticmethod
    def _parse_rows(reply: str) -> list[dict] | None:
        try:
            return list(extract_json_object(reply).get("frames", []))
        except ClaudeCliError:
            salvaged = salvage_frame_rows(reply)
            return salvaged or None
