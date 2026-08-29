from __future__ import annotations

import json
from pathlib import Path

import pytest

from libs.application.commands.understand__command import UnderstandCommand
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace
from libs.infrastructure.clients.composer__client import NullLlmComposer
from libs.infrastructure.clients.understanding__client import NullVideoUnderstanding
from libs.infrastructure.errors.understanding__error import UnderstandingBackendUnavailableError
from libs.infrastructure.daos.shotanalysis__dao import (
    EpisodeUnderstandingDao,
    ShotAnalysisDao,
    SpeakerAssignmentDao,
)
from libs.infrastructure.readers.artifact__reader import ArtifactReader
from libs.infrastructure.writers.artifact__writer import ArtifactWriter


class _FakeFfmpeg:
    def cut_clip(self, path: str, start_s: float, end_s: float, out_path: str) -> None:
        Path(out_path).write_bytes(b"clip")


class _FakeVlm:
    available = True

    def episode_pass(self, video_abs_path: str, dialogue_lines: list[dict]) -> EpisodeUnderstandingDao:
        return EpisodeUnderstandingDao(
            narrative="废婿归来，酒馆立威。",
            beats=("入场", "冲突", "反转"),
            emotion_curve="压抑—爆发",
            character_continuity={"裴远": "玄色劲装全集一致"},
            speaker_assignments=(
                SpeakerAssignmentDao(0, "裴远", "对白", 0.95),
                SpeakerAssignmentDao(1, "掌柜", "对白", 0.4),
            ),
        )

    def shot_pass(self, clip_abs_path: str, prev_shot_summary: str,
                  character_descriptors: dict[str, str], shot_index: int) -> ShotAnalysisDao:
        return ShotAnalysisDao(
            index=shot_index, shot_size="中景", camera_angle="平视", camera_move="固定",
            blocking="右侧入画", action=f"第{shot_index}镜动作", performance="眼神冷峻",
            scene_desc="酒馆内堂", lighting="暖黄烛光", mood="紧张",
            continuous_with_prev=shot_index == 2, characters=("裴远",),
            confidences={"camera_move": 0.5 if shot_index == 1 else 0.9, "shot_size": 0.95},
        )


class _FakeComposer:
    available = True

    def author_descriptor(self, character_name: str, ref_notes: str) -> str:
        return f"{character_name}：三十岁上下，玄色劲装（依据：{ref_notes[:12]}）"

    def compose_novel(self, script_markdown: str, narrative: str) -> str:
        return narrative


def _setup(tmp_path: Path, descriptor: str = "锁定描述") -> tuple[UnderstandCommand, Path]:
    ws = SafeWorkspace(root=str(tmp_path))
    writer = ArtifactWriter(ws)
    writer.write_text("d1/ep01/source.mp4", "fake")
    writer.write_json("d1/ep01/shots.json", [
        {"index": 1, "start_s": 0.0, "end_s": 2.8, "duration_s": 2.8},
        {"index": 2, "start_s": 2.8, "end_s": 6.0, "duration_s": 3.2},
    ])
    writer.write_json("d1/ep01/dialogue_raw.json", {"lines": [
        {"text": "你还敢回来？", "start_s": 0.5, "end_s": 2.0, "status": "match"},
        {"text": "客官息怒", "start_s": 3.0, "end_s": 4.0, "status": "match"},
    ], "flagged_count": 0, "degradations": []})
    writer.write_json("d1/characters/library.json", {"characters": [
        {"character_id": "c1", "name": "裴远", "descriptor": descriptor, "centroid": [1.0], "refs": [], "face_count": 9},
    ], "face_count": 9, "degradations": []})
    cmd = UnderstandCommand(ffmpeg=_FakeFfmpeg(), vlm=_FakeVlm(), composer=_FakeComposer(),  # type: ignore[arg-type]
                            reader=ArtifactReader(ws), writer=writer)
    return cmd, tmp_path


def test_two_pass_outputs_written_with_review_queue(tmp_path: Path) -> None:
    cmd, root = _setup(tmp_path)
    result = cmd.run("d1", "d1/ep01")
    assert result.shot_count == 2
    assert result.low_confidence_count == 1  # shot1 camera_move 0.5
    data = json.loads((root / "d1/ep01/understanding.json").read_text(encoding="utf-8"))
    assert data["review_queue"][0]["field"] == "camera_move"
    assert data["shots"][1]["continuous_with_prev"] is True


def test_speaker_attribution_fills_dialogue_json(tmp_path: Path) -> None:
    cmd, root = _setup(tmp_path)
    result = cmd.run("d1", "d1/ep01")
    lines = json.loads((root / "d1/ep01/dialogue.json").read_text(encoding="utf-8"))["lines"]
    assert lines[0]["speaker"] == "裴远" and lines[0]["attribution"] == "episode_pass"
    assert result.speaker_low_confidence_count == 1  # 掌柜 0.4


def test_idempotent_skip_on_second_run(tmp_path: Path) -> None:
    cmd, _ = _setup(tmp_path)
    assert not cmd.run("d1", "d1/ep01").skipped
    assert cmd.run("d1", "d1/ep01").skipped


def test_unavailable_backend_halts_loudly(tmp_path: Path) -> None:
    cmd, _ = _setup(tmp_path)
    cmd._vlm = NullVideoUnderstanding()  # type: ignore[attr-defined]
    with pytest.raises(UnderstandingBackendUnavailableError):
        cmd.run("d1", "d1/ep01", force=True)


def test_empty_descriptor_authored_and_persisted(tmp_path: Path) -> None:
    cmd, root = _setup(tmp_path, descriptor="")
    cmd.run("d1", "d1/ep01")
    library = json.loads((root / "d1/characters/library.json").read_text(encoding="utf-8"))
    assert library["characters"][0]["descriptor"].startswith("裴远：三十岁上下")


def test_vlm_discovered_character_gets_card_and_descriptor(tmp_path: Path) -> None:
    """Default install (Null face backend) leaves the library EMPTY — VLM-named
    characters must still end understand with a card + descriptor, else compose
    dead-ends on DescriptorDriftError (2026-07-18 real-run regression)."""
    cmd, root = _setup(tmp_path)
    (root / "d1/characters/library.json").write_text(json.dumps(
        {"characters": [], "face_count": 0, "degradations": ["face_backend_unavailable"]},
        ensure_ascii=False), encoding="utf-8")
    cmd.run("d1", "d1/ep01")
    library = json.loads((root / "d1/characters/library.json").read_text(encoding="utf-8"))
    cards = {c["name"]: c for c in library["characters"]}
    assert "裴远" in cards and cards["裴远"]["origin"] == "vlm_discovered"
    assert cards["裴远"]["descriptor"].startswith("裴远：三十岁上下")


def test_shot_only_character_card_created_after_loop(tmp_path: Path) -> None:
    class _NoContinuityVlm(_FakeVlm):
        def episode_pass(self, video_abs_path: str, dialogue_lines: list[dict]) -> EpisodeUnderstandingDao:
            base = super().episode_pass(video_abs_path, dialogue_lines)
            return EpisodeUnderstandingDao(base.narrative, base.beats, base.emotion_curve, {},
                                           base.speaker_assignments)

    cmd, root = _setup(tmp_path)
    cmd._vlm = _NoContinuityVlm()  # type: ignore[attr-defined]
    (root / "d1/characters/library.json").write_text(json.dumps(
        {"characters": [], "face_count": 0, "degradations": []}, ensure_ascii=False), encoding="utf-8")
    cmd.run("d1", "d1/ep01")
    library = json.loads((root / "d1/characters/library.json").read_text(encoding="utf-8"))
    cards = {c["name"]: c for c in library["characters"]}
    assert "裴远" in cards and cards["裴远"]["descriptor"]


def test_empty_descriptor_left_empty_when_composer_unavailable(tmp_path: Path) -> None:
    cmd, root = _setup(tmp_path, descriptor="")
    cmd._composer = NullLlmComposer()  # type: ignore[attr-defined]
    cmd.run("d1", "d1/ep01")
    library = json.loads((root / "d1/characters/library.json").read_text(encoding="utf-8"))
    assert library["characters"][0]["descriptor"] == ""  # compose stage will raise DescriptorDriftError
