from __future__ import annotations

import json
from pathlib import Path

from libs.infrastructure.clients.claude_subtitle__client import ClaudeSubtitleExtractor, merge_frame_texts
from libs.infrastructure.daos.media__dao import MediaInfoDao


class _FakeCli:
    available = True

    def __init__(self, replies: list[str]) -> None:
        self.replies = replies
        self.calls: list[str] = []

    def run_text(self, prompt: str, read_dirs: tuple[str, ...] = (), max_turns: int = 8) -> str:
        self.calls.append(prompt)
        return self.replies[len(self.calls) - 1]


class _FakeFfmpeg:
    def __init__(self, duration_s: float) -> None:
        self.duration_s = duration_s
        self.extracted: list[float] = []

    def probe(self, path: str) -> MediaInfoDao:
        return MediaInfoDao(duration_s=self.duration_s, width=1080, height=1920, decodable=True)

    def extract_frame(self, path: str, at_s: float, out_path: str) -> None:
        Path(out_path).write_bytes(b"jpg")
        self.extracted.append(at_s)


def test_merge_consecutive_identical_texts_into_lines() -> None:
    lines = merge_frame_texts(
        [(0.5, "你还敢回来？"), (1.5, "你还敢回来？"), (2.5, ""), (3.5, "客官息怒")], half_step_s=0.5
    )
    assert [(l.text, l.start_s, l.end_s) for l in lines] == [
        ("你还敢回来？", 0.0, 2.0), ("客官息怒", 3.0, 4.0),
    ]
    assert all(l.source == "ocr" for l in lines)


def test_extract_samples_one_fps_and_merges(tmp_path: Path) -> None:
    video = tmp_path / "source.mp4"
    video.write_bytes(b"v")
    reply = json.dumps({"frames": [
        {"i": 0, "text": "你还敢回来？"}, {"i": 1, "text": "你还敢回来？"},
        {"i": 2, "text": None}, {"i": 3, "text": "客官息怒"},
        {"i": 4, "text": None}, {"i": 5, "text": None},
        {"i": 6, "text": None}, {"i": 7, "text": None},
        {"i": 8, "text": None}, {"i": 9, "text": None},
    ]}, ensure_ascii=False)
    cli = _FakeCli([reply])
    ffmpeg = _FakeFfmpeg(duration_s=10.0)
    lines = ClaudeSubtitleExtractor(cli, ffmpeg).extract(str(video))  # type: ignore[arg-type]
    assert len(ffmpeg.extracted) == 10 and len(cli.calls) == 1
    assert [l.text for l in lines] == ["你还敢回来？", "客官息怒"]
    assert not (tmp_path / ".claude_subs_source").exists()  # frames cleaned up


def test_extract_chunks_long_videos(tmp_path: Path) -> None:
    video = tmp_path / "long.mp4"
    video.write_bytes(b"v")
    empty = json.dumps({"frames": []})
    cli = _FakeCli([empty, empty, empty])
    lines = ClaudeSubtitleExtractor(cli, _FakeFfmpeg(duration_s=70.0)).extract(str(video))  # type: ignore[arg-type]
    assert len(cli.calls) == 3  # 70 frames in chunks of 30
    assert lines == []


def test_availability_mirrors_cli(tmp_path: Path) -> None:
    cli = _FakeCli([])
    cli.available = False
    assert ClaudeSubtitleExtractor(cli, _FakeFfmpeg(1.0)).available is False  # type: ignore[arg-type]


def test_malformed_row_salvaged_without_retry(tmp_path: Path) -> None:
    """2026-07-18 real run: one row came back as {"i":129,null} (no "text" key) and the
    whole chunk failed json.loads — well-formed rows must be salvaged."""
    from libs.infrastructure.clients.claude_subtitle__client import salvage_frame_rows

    reply = ('{"frames":[{"i":0,"text":"我倒要去看个明白"},{"i":1,"text":"北边那片天"},'
             '{"i":2,null},{"i":3,"text":null}]}')
    rows = salvage_frame_rows(reply)
    assert rows == [{"i": 0, "text": "我倒要去看个明白"}, {"i": 1, "text": "北边那片天"}, {"i": 3, "text": None}]

    video = tmp_path / "v.mp4"
    video.write_bytes(b"v")
    cli = _FakeCli([reply])
    lines = ClaudeSubtitleExtractor(cli, _FakeFfmpeg(duration_s=4.0)).extract(str(video))  # type: ignore[arg-type]
    assert len(cli.calls) == 1  # salvage succeeded, no retry needed
    assert [l.text for l in lines] == ["我倒要去看个明白", "北边那片天"]


def test_unsalvageable_chunk_retries_once(tmp_path: Path) -> None:
    video = tmp_path / "v.mp4"
    video.write_bytes(b"v")
    good = json.dumps({"frames": [{"i": 0, "text": "台词行"}, {"i": 1, "text": None},
                                  {"i": 2, "text": None}, {"i": 3, "text": None}]}, ensure_ascii=False)
    cli = _FakeCli(["完全不是JSON的回复", good])
    lines = ClaudeSubtitleExtractor(cli, _FakeFfmpeg(duration_s=4.0)).extract(str(video))  # type: ignore[arg-type]
    assert len(cli.calls) == 2 and "务必只输出" in cli.calls[1]
    assert [l.text for l in lines] == ["台词行"]
