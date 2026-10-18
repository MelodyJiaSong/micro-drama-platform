"""Two-step generation (follow-up 265): a cheap 480p draft first; once the user marks it 通过, a 720p final is
submitted with the approved draft as an extra reference video."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from tools import shot_take

PROMPT = ("ep1_s9_st1\n时长：5秒\n比例：16:9\n"
          "参考：`ep1_s9_st1_overhead=>@图片1`、`c1-14_便服=>@图片2`、`c1_Aaron_audio=>@音频1`\n"
          "参考用法：`ep1_s9_st1_overhead`是本镜的俯视站位示意图。\n人物：\n  亚伦：……\n")


def take(renders: Path, name: str, stage: str | None, status: str, resolution: str = "480p") -> Path:
    folder = renders / name
    folder.mkdir(parents=True)
    record = {"key": "ep1_s9_st1", "take": name, "resolution": resolution}
    if stage:
        record["stage"] = stage
    (folder / "generation.json").write_text(json.dumps(record), encoding="utf-8")
    (folder / "review.md").write_text(shot_take.REVIEW_TEMPLATE.replace("状态：待审核", "状态：" + status), encoding="utf-8")
    (folder / "ep1_s9_st1_x.mp4").write_bytes(b"v")
    return folder


def test_each_stage_reads_its_resolution_from_the_drama_settings() -> None:
    assert shot_take.stage_resolution({"draft_resolution": "480p", "resolution": "720p"}, "draft") == "480p"
    assert shot_take.stage_resolution({"resolution": "720p"}, "final") == "720p"
    assert shot_take.stage_resolution({}, "draft") == "480p"   # the cheapest Seedance 2.5 tier
    assert shot_take.stage_resolution({}, "final") == "720p"


def test_final_prompt_adds_the_draft_as_the_last_reference_and_says_how_to_use_it() -> None:
    out = shot_take.final_prompt(PROMPT, "ep1_s9_st1", ["@视频1"])
    ref = next(line for line in out.splitlines() if line.startswith("参考："))
    assert ref.endswith("、`ep1_s9_st1_draft=>@视频1`")
    usage = next(line for line in out.splitlines() if line.startswith("参考用法："))
    assert usage.startswith("参考用法：`ep1_s9_st1_overhead`是本镜的俯视站位示意图。")
    assert "`ep1_s9_st1_draft`是本镜用户已审过的草稿" in usage and "三视图" in usage
    assert out.replace(ref, "").replace(usage, "") == PROMPT.replace(PROMPT.splitlines()[3], "").replace(PROMPT.splitlines()[4], "")


def test_a_long_draft_is_named_part_by_part() -> None:
    out = shot_take.final_prompt(PROMPT, "ep1_s9_st1", ["@视频1", "@视频2"])
    assert "`ep1_s9_st1_draft_p1=>@视频1`、`ep1_s9_st1_draft_p2=>@视频2`" in out
    assert "`ep1_s9_st1_draft_p1`、`ep1_s9_st1_draft_p2`是本镜用户已审过的草稿" in out


def test_only_a_draft_the_user_marked_通过_can_seed_a_final(tmp_path: Path) -> None:
    drafts = tmp_path / "drafts"
    take(drafts, "20261016-100000_aaaa1111", "draft", "通过（用户 2026-10-16 10:30）")
    take(drafts, "20261016-110000_bbbb2222", "draft", "待审核")
    take(drafts, "20261016-120000_cccc3333", "final", "通过", "720p")
    assert shot_take.approved_draft(tmp_path).name == "20261016-100000_aaaa1111"
    with pytest.raises(SystemExit, match="不是用户标了通过的草稿"):
        shot_take.approved_draft(tmp_path, "20261016-110000_bbbb2222")
    with pytest.raises(SystemExit, match="不是用户标了通过的草稿"):
        shot_take.approved_draft(tmp_path, "20261016-120000_cccc3333")
    with pytest.raises(SystemExit, match="没有用户标了通过的草稿"):
        shot_take.approved_draft(tmp_path / "elsewhere")


def test_takes_from_before_the_two_steps_count_by_resolution(tmp_path: Path) -> None:
    old = take(tmp_path / "renders", "20261011-090000_dddd4444", None, "通过", "720p")
    assert shot_take.take_stage(old, {"draft_resolution": "480p"}) == "final"


@pytest.fixture
def pack(tmp_path: Path, monkeypatch) -> Path:
    shot_dir = tmp_path / "shot"
    pack = shot_dir / "资料包"
    (pack / "upload").mkdir(parents=True)
    (pack / "upload" / "01_image1.jpg").write_bytes(b"i")
    (pack / "prompt.txt").write_text(PROMPT, encoding="utf-8")
    man = {"refs": [{"tag": "@图片1", "key": "ep1_s9_st1_overhead", "kind": "image", "upload": "upload/01_image1.jpg"}]}
    (pack / "manifest.json").write_text(json.dumps(man), encoding="utf-8")
    monkeypatch.setattr(shot_take, "shot_info", lambda ep, key: ({"id": key, "scene": "s9", "text": PROMPT}, shot_dir))
    monkeypatch.setattr(shot_take.shot_pack, "state", lambda p, s: "ok")
    monkeypatch.setattr(shot_take.shot_pack.es, "settings", lambda d: {"prompt": {"model": "seedance2.5", "resolution": "720p",
                                                                                  "draft_resolution": "480p"}})
    monkeypatch.setattr(shot_take.shot_pack.es, "drama_root", lambda p: tmp_path)
    monkeypatch.setattr(shot_take, "REPO", tmp_path)
    return shot_dir


def fake_submit(sent: list[list[str]]):
    def run(cmd, **kwargs):
        sent.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, json.dumps({"submit_id": "abcdef123456", "gen_status": "querying",
                                                                "credit_count": 40}), "")
    return run


def test_a_draft_goes_in_at_480p_with_the_pack_as_it_is(pack: Path, tmp_path: Path, monkeypatch) -> None:
    sent: list[list[str]] = []
    monkeypatch.setattr(shot_take.subprocess, "run", fake_submit(sent))
    sid, credits, (text, _), meta = shot_take.submit(tmp_path, "ep1_s9_st1", "draft")
    assert "--video_resolution=480p" in sent[0] and "--video" not in sent[0]
    assert text == PROMPT and meta == {"stage": "draft", "resolution": "480p"}
    pending = json.loads((pack / "drafts" / ".pending" / "abcdef123456.json").read_text(encoding="utf-8"))
    assert pending["meta"]["stage"] == "draft"


def test_a_final_goes_in_at_720p_with_the_approved_draft_appended(pack: Path, tmp_path: Path, monkeypatch) -> None:
    draft = take(pack / "drafts", "20261016-100000_aaaa1111", "draft", "通过（用户）")
    part = draft / "upload" / "draft_ref.mp4"
    monkeypatch.setattr(shot_take, "draft_reference", lambda folder: [part])
    sent: list[list[str]] = []
    monkeypatch.setattr(shot_take.subprocess, "run", fake_submit(sent))
    _, _, (text, man), meta = shot_take.submit(tmp_path, "ep1_s9_st1", "final")
    cmd = sent[0]
    assert "--video_resolution=720p" in cmd
    assert cmd[cmd.index("--video") + 1] == str(part)
    assert "`ep1_s9_st1_draft=>@视频1`" in text and cmd[cmd.index("--video") - 2] == "--image"
    assert meta["stage"] == "final" and meta["resolution"] == "720p" and meta["from_take"] == "20261016-100000_aaaa1111"
    assert man["refs"][-1]["key"] == "ep1_s9_st1_draft" and man["refs"][-1]["tag"] == "@视频1"


def test_a_final_without_a_draft_only_when_the_user_says_so(pack: Path, tmp_path: Path, monkeypatch) -> None:
    sent: list[list[str]] = []
    monkeypatch.setattr(shot_take.subprocess, "run", fake_submit(sent))
    _, _, (text, man), meta = shot_take.submit(tmp_path, "ep1_s9_st1", "final", no_draft="用户要求直接出 720p")
    assert "--video_resolution=720p" in sent[0] and "--video" not in sent[0]
    assert text == PROMPT and meta == {"stage": "final", "resolution": "720p", "no_draft": "用户要求直接出 720p"}
    video = tmp_path / "out.mp4"
    video.write_bytes(b"v")
    folder = shot_take.make_take(tmp_path, "ep1_s9_st1", "abcdef123456", video, 160, None, (text, man), meta=meta)
    assert json.loads((folder / "generation.json").read_text(encoding="utf-8"))["no_draft"] == "用户要求直接出 720p"


def test_the_take_records_its_stage_and_where_a_final_came_from(pack: Path, tmp_path: Path) -> None:
    video = tmp_path / "out.mp4"
    video.write_bytes(b"v")
    meta = {"stage": "final", "resolution": "720p", "from_take": "20261016-100000_aaaa1111"}
    folder = shot_take.make_take(tmp_path, "ep1_s9_st1", "abcdef123456", video, 160, None, (PROMPT, {"refs": []}), meta=meta)
    record = json.loads((folder / "generation.json").read_text(encoding="utf-8"))
    assert folder.parent.name == "renders"
    draft = shot_take.make_take(tmp_path, "ep1_s9_st1", "fedcba654321", video, 40, None, (PROMPT, {"refs": []}),
                                meta={"stage": "draft", "resolution": "480p"})
    assert draft.parent.name == "drafts"      # 草稿单独一个目录（follow-up 266）
    assert record["stage"] == "final" and record["resolution"] == "720p" and record["from_take"] == "20261016-100000_aaaa1111"


@pytest.mark.skipif(shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None, reason="needs ffmpeg")
def test_the_draft_reference_is_lifted_to_720p_without_sound_and_cut_to_15_s_parts(tmp_path: Path) -> None:
    folder = tmp_path / "renders" / "20261016-100000_aaaa1111"
    folder.mkdir(parents=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc=size=848x480:rate=24:duration=18",
                    "-f", "lavfi", "-i", "sine=duration=18", "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    str(folder / "ep1_s9_st1_x.mp4")], check=True)
    parts = shot_take.draft_reference(folder)
    assert len(parts) == 2
    for part in parts:
        probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height", "-of", "json", str(part)],
                               capture_output=True, text=True).stdout
        streams = json.loads(probe)["streams"]
        assert [s["codec_type"] for s in streams] == ["video"] and (streams[0]["width"], streams[0]["height"]) == (1280, 720)
