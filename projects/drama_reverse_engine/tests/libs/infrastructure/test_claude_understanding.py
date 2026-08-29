from __future__ import annotations

import json
from pathlib import Path

from libs.infrastructure.clients.claude_understanding__client import ClaudeVideoUnderstanding
from libs.infrastructure.daos.media__dao import MediaInfoDao

_EPISODE_JSON = {
    "narrative": "废婿归来，酒馆立威。",
    "beats": ["入场", "冲突"],
    "emotion_curve": "压抑—爆发",
    "character_continuity": {"裴远": "玄色劲装"},
    "speaker_assignments": [
        {"line_index": 0, "speaker": "裴远", "dialogue_type": "对白", "confidence": 0.9},
    ],
}

_SHOT_JSON = {
    "shot_size": "不在词表里", "camera_angle": "平视", "camera_move": "推",
    "blocking": "右侧入画", "action": "推门而入", "performance": "眼神冷峻",
    "scene_desc": "酒馆内堂", "lighting": "暖黄", "mood": "紧张",
    "continuous_with_prev": True, "characters": ["裴远"], "confidences": {"shot_size": 0.4},
}


class _FakeCli:
    available = True

    def __init__(self, reply: str, first_reply: str | None = None) -> None:
        self.reply = reply
        self.first_reply = first_reply
        self.calls: list[dict] = []

    def run_text(self, prompt: str, read_dirs: tuple[str, ...] = (), max_turns: int = 8) -> str:
        self.calls.append({"prompt": prompt, "read_dirs": read_dirs, "max_turns": max_turns})
        if self.first_reply is not None and len(self.calls) == 1:
            return self.first_reply
        return self.reply


class _FakeFfmpeg:
    def __init__(self, duration_s: float) -> None:
        self.duration_s = duration_s
        self.extracted: list[tuple[float, str]] = []

    def probe(self, path: str) -> MediaInfoDao:
        return MediaInfoDao(duration_s=self.duration_s, width=1080, height=1920, decodable=True)

    def extract_frame(self, path: str, at_s: float, out_path: str) -> None:
        Path(out_path).write_bytes(b"jpg")
        self.extracted.append((at_s, out_path))


def test_episode_pass_samples_frames_and_parses(tmp_path: Path) -> None:
    video = tmp_path / "source.mp4"
    video.write_bytes(b"v")
    cli = _FakeCli(f"```json\n{json.dumps(_EPISODE_JSON, ensure_ascii=False)}\n```")
    ffmpeg = _FakeFfmpeg(duration_s=30.0)
    dao = ClaudeVideoUnderstanding(cli, ffmpeg).episode_pass(str(video), [  # type: ignore[arg-type]
        {"text": "你还敢回来？", "start_s": 0.5, "end_s": 2.0},
    ])
    assert dao.narrative == "废婿归来，酒馆立威。"
    assert dao.speaker_assignments[0].speaker == "裴远"
    assert len(ffmpeg.extracted) == 7  # 30s // 5 + 1
    assert "你还敢回来？" in cli.calls[0]["prompt"]
    assert cli.calls[0]["read_dirs"] and ".claude_frames_episode_source" in cli.calls[0]["read_dirs"][0]
    assert not Path(cli.calls[0]["read_dirs"][0]).exists()  # cleaned up after the call


def test_episode_pass_caps_frames_on_long_video(tmp_path: Path) -> None:
    video = tmp_path / "long.mp4"
    video.write_bytes(b"v")
    ffmpeg = _FakeFfmpeg(duration_s=600.0)
    ClaudeVideoUnderstanding(_FakeCli(json.dumps(_EPISODE_JSON)), ffmpeg).episode_pass(str(video), [])  # type: ignore[arg-type]
    assert len(ffmpeg.extracted) == 24


def test_shot_pass_three_frames_and_vocab_snap(tmp_path: Path) -> None:
    clip = tmp_path / "shot01.mp4"
    clip.write_bytes(b"v")
    cli = _FakeCli(json.dumps(_SHOT_JSON, ensure_ascii=False))
    ffmpeg = _FakeFfmpeg(duration_s=8.0)
    dao = ClaudeVideoUnderstanding(cli, ffmpeg).shot_pass(str(clip), "上一镜：入场", {"裴远": "玄色劲装"}, 3)  # type: ignore[arg-type]
    assert dao.index == 3
    assert dao.shot_size == "中景"  # snapped to vocab default
    assert dao.camera_move == "推"
    assert [round(t, 2) for t, _ in ffmpeg.extracted] == [1.2, 4.0, 6.8]
    assert "玄色劲装" in cli.calls[0]["prompt"]


def test_availability_mirrors_cli(tmp_path: Path) -> None:
    cli = _FakeCli("{}")
    cli.available = False
    assert ClaudeVideoUnderstanding(cli, _FakeFfmpeg(1.0)).available is False  # type: ignore[arg-type]


def test_non_json_reply_retried_once(tmp_path: Path) -> None:
    video = tmp_path / "source.mp4"
    video.write_bytes(b"v")
    cli = _FakeCli(json.dumps(_EPISODE_JSON, ensure_ascii=False), first_reply="这不是JSON，我拒绝分析")
    dao = ClaudeVideoUnderstanding(cli, _FakeFfmpeg(duration_s=10.0)).episode_pass(str(video), [])  # type: ignore[arg-type]
    assert dao.narrative == "废婿归来，酒馆立威。"
    assert len(cli.calls) == 2 and "务必只输出" in cli.calls[1]["prompt"]


def test_parse_shot_characters_object_entries_reduce_to_names() -> None:
    """Models sometimes ignore the string-array contract and return character objects
    (2026-07-18 real run: {'name': '裴知秋', 'desc': ...} str()-ed into the descriptor
    lookup key)."""
    from libs.infrastructure.clients.gemini_understanding__client import parse_shot_json

    data = {**_SHOT_JSON, "characters": [{"name": "裴知秋", "desc": "黑袍"}, "掌柜", ""]}
    assert parse_shot_json(data, 1).characters == ("裴知秋", "掌柜")
