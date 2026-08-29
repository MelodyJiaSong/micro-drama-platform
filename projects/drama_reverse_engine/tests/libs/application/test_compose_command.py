from __future__ import annotations

from pathlib import Path

from libs.application.commands.compose__command import ComposeCommand
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace
from libs.infrastructure.clients.composer__client import NullLlmComposer
from libs.infrastructure.readers.artifact__reader import ArtifactReader
from libs.infrastructure.writers.artifact__writer import ArtifactWriter

_DESCRIPTOR = "三十岁男子，剑眉星目，玄色劲装"


class _FakeComposer:
    available = True

    def compose_novel(self, script_markdown: str, narrative: str) -> str:
        return f"# 第一章\n\n{narrative}（文学化改写）"

    def author_descriptor(self, character_name: str, ref_notes: str) -> str:
        return _DESCRIPTOR


def _analysis(index: int, continuous: bool) -> dict:
    return {
        "index": index, "shot_size": "中景", "camera_angle": "平视", "camera_move": "固定",
        "blocking": "右侧入画", "action": f"第{index}镜动作", "performance": "眼神冷峻",
        "scene_desc": "酒馆内堂", "lighting": "暖黄烛光", "mood": "紧张",
        "continuous_with_prev": continuous, "characters": ["裴远"],
        "confidences": {"camera_move": 0.9},
    }


def _setup(tmp_path: Path, composer: object) -> tuple[ComposeCommand, Path]:
    ws = SafeWorkspace(root=str(tmp_path))
    writer = ArtifactWriter(ws)
    writer.write_json("d1/ep01/shots.json", [
        {"index": 1, "start_s": 0.0, "end_s": 2.8, "duration_s": 2.8},
        {"index": 2, "start_s": 2.8, "end_s": 6.0, "duration_s": 3.2},
        {"index": 3, "start_s": 6.0, "end_s": 10.0, "duration_s": 4.0},
    ])
    writer.write_json("d1/ep01/dialogue.json", {"lines": [
        {"text": "你还敢回来？", "start_s": 0.5, "end_s": 2.0, "speaker": "裴远", "dialogue_type": "对白"},
        {"text": "此地不宜久留。", "start_s": 6.5, "end_s": 8.0, "speaker": "裴远", "dialogue_type": "内心独白"},
    ], "speaker_low_confidence_count": 0})
    writer.write_json("d1/ep01/understanding.json", {
        "narrative": "废婿归来。", "beats": ["入场"], "emotion_curve": "平-爆",
        "character_continuity": {}, "review_queue": [],
        "speaker_low_confidence_count": 0,
        "shots": [_analysis(1, False), _analysis(2, True), _analysis(3, False)],
    })
    writer.write_json("d1/characters/library.json", {"characters": [
        {"character_id": "c1", "name": "裴远", "descriptor": _DESCRIPTOR, "centroid": [1.0], "refs": [], "face_count": 9},
    ], "face_count": 9, "degradations": []})
    return ComposeCommand(composer=composer, reader=ArtifactReader(ws), writer=writer), tmp_path  # type: ignore[arg-type]


def test_subtitle_token_in_vlm_description_scrubbed_not_fatal(tmp_path: Path) -> None:
    """2026-07-18 real run: VLM scene_desc mentioned the on-screen 角色名牌…字幕 overlay
    and compose died on SubtitleContaminationError — the token must be scrubbed with a
    degradation tag instead."""
    cmd, root = _setup(tmp_path, _FakeComposer())
    reader = ArtifactReader(SafeWorkspace(root=str(tmp_path)))
    understanding = reader.read_json("d1/ep01/understanding.json")
    understanding["shots"][0]["scene_desc"] = "王府大堂，画面右上角有角色名牌'裴知秋'字幕"
    ArtifactWriter(SafeWorkspace(root=str(tmp_path))).write_json("d1/ep01/understanding.json", understanding)
    result = cmd.run("d1", "d1/ep01")
    assert "shot01_subtitle_token_scrubbed" in result.degradations
    shot1 = (root / "d1/ep01/shots/shot01/shot01.md").read_text(encoding="utf-8")
    body = shot1.split("## 视频 prompt")[1]
    assert "字幕" not in body


def test_short_source_shots_merge_into_one_prompt_unit(tmp_path: Path) -> None:
    """Follow-up 005: 2.8s + 3.2s original shots are below the Seedance 4s floor —
    they merge into one 6s prompt unit; the 4s shot stands alone."""
    cmd, root = _setup(tmp_path, _FakeComposer())
    result = cmd.run("d1", "d1/ep01")
    assert len(result.shot_files) == 2
    shot1 = (root / "d1/ep01/shots/shot01/shot01.md").read_text(encoding="utf-8")
    shot2 = (root / "d1/ep01/shots/shot02/shot02.md").read_text(encoding="utf-8")
    assert "duration_s: 6\n" in shot1 and "（镜内跳切）" in shot1
    assert "原镜01+原镜02（镜内跳切合并）" in shot1
    assert "硬切（独立首帧）" in shot1 and "硬切（独立首帧）" in shot2


def test_long_source_shot_split_into_linked_segments(tmp_path: Path) -> None:
    """Follow-up 005: a 20s original shot exceeds the Seedance 15s cap — split into
    two 10s segments chained 首帧=上一镜末帧, with the handoff source tail-locked."""
    cmd, root = _setup(tmp_path, _FakeComposer())
    writer = ArtifactWriter(SafeWorkspace(root=str(tmp_path)))
    writer.write_json("d1/ep01/shots.json", [{"index": 1, "start_s": 0.0, "end_s": 20.0, "duration_s": 20.0}])
    writer.write_json("d1/ep01/understanding.json", {
        "narrative": "长镜独白。", "beats": [], "emotion_curve": "平",
        "character_continuity": {}, "review_queue": [], "speaker_low_confidence_count": 0,
        "shots": [_analysis(1, False)],
    })
    result = cmd.run("d1", "d1/ep01")
    assert len(result.shot_files) == 2
    shot1 = (root / "d1/ep01/shots/shot01/shot01.md").read_text(encoding="utf-8")
    shot2 = (root / "d1/ep01/shots/shot02/shot02.md").read_text(encoding="utf-8")
    assert "duration_s: 10\n" in shot1 and "tail_locked: true" in shot1
    assert "原镜01 第1/2段" in shot1
    assert "承接 shot01 末帧" in shot2 and "本镜首帧(上一镜末帧)" in shot2
    assert "原镜01 第2/2段" in shot2 and "原长镜第2/2段" in shot2


def test_descriptor_pasted_byte_identical_in_every_shot_naming_character(tmp_path: Path) -> None:
    cmd, root = _setup(tmp_path, _FakeComposer())
    result = cmd.run("d1", "d1/ep01")
    for rel in result.shot_files:
        content = (root / rel).read_text(encoding="utf-8")
        assert _DESCRIPTOR in content


def test_script_keeps_dialogue_verbatim_and_marks_os(tmp_path: Path) -> None:
    cmd, root = _setup(tmp_path, _FakeComposer())
    cmd.run("d1", "d1/ep01")
    script = (root / "d1/ep01/script.md").read_text(encoding="utf-8")
    assert script.startswith("第1集：")  # sample_juben.docx 影视剧本体 (follow-up 006)
    assert "分集大纲：" in script and "正文：" in script
    assert "1-1 日 内 酒馆内堂" in script and "人物：裴远" in script
    assert "裴远（紧张）：你还敢回来？" in script  # follow-up 008: 首句对白带 mood 括注
    assert "裴远（内心独白）：此地不宜久留。" in script
    assert "△" in script
    shot2 = (root / "d1/ep01/shots/shot02/shot02.md").read_text(encoding="utf-8")
    assert "口型不动" in shot2
    assert "台词配音 prompt" in shot2 and "voice_裴远(锁定" in shot2


def test_shot_md_follows_wushen_five_layer_structure(tmp_path: Path) -> None:
    """Follow-up 008: shotNN.md = YAML → ## 原片对应段 → H1 → ## Shot context bullets
    → ## 视频 prompt (武神觉醒 field order) → ## 台词配音 prompt (```text block)."""
    cmd, root = _setup(tmp_path, _FakeComposer())
    cmd.run("d1", "d1/ep01")
    shot1 = (root / "d1/ep01/shots/shot01/shot01.md").read_text(encoding="utf-8")
    assert "# ep01 / shot01 · " in shot1
    assert "## Shot context" in shot1
    assert "- **Summary**：" in shot1 and "- **Duration**：6s。" in shot1
    assert "- **衔接**：硬切（独立首帧）。" in shot1
    assert "- **Reference uploads**：裴远 参考图。" in shot1
    assert "## Kling prompt" not in shot1
    body = shot1.split("## 视频 prompt")[1].split("## 台词配音 prompt")[0]
    for field in ("参考分配:", "角色识别 / 参考图:", "情节: `", "镜头: `", "走位: `",
                  "台词:（画面不显示文字、仅供口型与配音参考；逐条↓）", "光线 / 色调: `", "负面词:"):
        assert field in body
    assert "时长: 6秒" in body
    voice = shot1.split("## 台词配音 prompt")[1]
    assert "```text" in voice and "音色: voice_裴远(锁定" in voice and "时长目标: 6秒内" in voice


def test_null_composer_degrades_to_skeleton_novel(tmp_path: Path) -> None:
    cmd, root = _setup(tmp_path, NullLlmComposer())
    result = cmd.run("d1", "d1/ep01")
    assert "novel_llm_unavailable_skeleton_only" in result.degradations
    assert "骨架版" in (root / "d1/ep01/novel.md").read_text(encoding="utf-8")


def test_all_shot_prompts_aggregated_and_idempotent_skip(tmp_path: Path) -> None:
    cmd, root = _setup(tmp_path, _FakeComposer())
    first = cmd.run("d1", "d1/ep01")
    assert (root / "d1/ep01/all_shot_prompts.md").exists()
    second = cmd.run("d1", "d1/ep01")
    assert not first.skipped and second.skipped


def test_out_of_range_line_clamped_not_dropped(tmp_path: Path) -> None:
    cmd, root = _setup(tmp_path, _FakeComposer())
    import json as _json

    dlg_path = root / "d1/ep01/dialogue.json"
    data = _json.loads(dlg_path.read_text(encoding="utf-8"))
    data["lines"].append({"text": "谁都别拦我！", "start_s": 13.0, "end_s": 15.5,
                          "speaker": "裴远", "dialogue_type": "对白"})
    dlg_path.write_text(_json.dumps(data, ensure_ascii=False), encoding="utf-8")
    result = cmd.run("d1", "d1/ep01")
    assert any(d.startswith("lines_clamped_to_nearest_shot:1") for d in result.degradations)
    script = (root / "d1/ep01/script.md").read_text(encoding="utf-8")
    assert "谁都别拦我！" in script
    shot2 = (root / "d1/ep01/shots/shot02/shot02.md").read_text(encoding="utf-8")
    assert "谁都别拦我" in shot2


def test_empty_descriptor_raises_descriptor_drift(tmp_path: Path) -> None:
    import json as _json

    import pytest

    from libs.domain.errors.shot__error import DescriptorDriftError

    cmd, root = _setup(tmp_path, _FakeComposer())
    lib_path = root / "d1/characters/library.json"
    lib = _json.loads(lib_path.read_text(encoding="utf-8"))
    lib["characters"][0]["descriptor"] = ""
    lib_path.write_text(_json.dumps(lib, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(DescriptorDriftError):
        cmd.run("d1", "d1/ep01")


def test_shot_md_carries_source_segment_block(tmp_path: Path) -> None:
    cmd, root = _setup(tmp_path, _FakeComposer())
    cmd.run("d1", "d1/ep01")
    shot1 = (root / "d1/ep01/shots/shot01/shot01.md").read_text(encoding="utf-8")
    assert "## 原片对应段" in shot1
    assert "时间码 0.00s–6.00s" in shot1
