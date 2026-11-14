# -*- coding: utf-8 -*-
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
import skill_run  # noqa: E402

BODY = """k9_X_clip
时长：13秒
0–0.5秒 停顿：开场图那一帧。
0.5–2.0秒 起势：站定，不出特效。
2.0–10.5秒 技能主体。
10.5–11.0秒 吹一下指尖。
11.0–13.0秒 收势：站定不动。
要求：一个连续固定镜头。"""


def test_action_window_from_beats(monkeypatch):
    monkeypatch.setattr(skill_run.skill_pack, "shot", lambda sd: {"text": BODY, "refs": []})
    assert skill_run.action_window(Path("k9_X")) == "2.0-11.0"


def test_whens_ignore_negative_words(tmp_path):
    sd = tmp_path / "k9_X"
    sd.mkdir()
    (sd / "k9_X.md").write_text("# x\n## 技能视频 prompt\n```text\n头顶旋涡，被晕住；一镜到底\n负面词：减速, 眩晕光环\n```\n",
                                encoding="utf-8")
    assert skill_run.whens(sd) == ["一镜到底"]          # 眩晕、减速只在负面词里，不算


def test_whens_detects_stun(tmp_path):
    sd = tmp_path / "k9_X"
    sd.mkdir()
    (sd / "k9_X.md").write_text("## 技能视频 prompt\n```text\n落地后被眩晕约2秒\n```\n", encoding="utf-8")
    assert skill_run.whens(sd) == ["眩晕"]


def _skill(tmp_path, policy: bool):
    drama = tmp_path / "ai_videos" / "d"
    sd = drama / "2_世界观人设" / "characters" / "c1_X" / "skills" / "k1_X"
    take = sd / "renders" / "20261030-100000_abcd1234"
    take.mkdir(parents=True)
    (take / "k1_X_clip.mp4").write_bytes(b"x")
    (drama / "qc_checks.toml").write_text("[policy]\nwait_user_feedback_after_render = %s\n" % str(policy).lower(),
                                          encoding="utf-8")
    return sd, take


def test_feedback_gate_blocks_until_user_feedback(tmp_path, monkeypatch):
    import qc
    from tools import skill_pack
    monkeypatch.setattr(qc, "drama_dir_of", lambda p: tmp_path / "ai_videos" / "d")
    monkeypatch.setattr(skill_pack, "REPO", tmp_path)
    sd, take = _skill(tmp_path, True)
    assert skill_pack.feedback_gate(sd)                      # 出过片、没反馈 → 拒绝
    skill_pack.feedback(sd, "用户：重出，要一镜到底")
    assert skill_pack.feedback_gate(sd) is None              # 记了反馈 → 放行
    assert "一镜到底" in (take / skill_pack.FEEDBACK).read_text(encoding="utf-8")


def test_feedback_gate_off_without_policy(tmp_path, monkeypatch):
    import qc
    from tools import skill_pack
    monkeypatch.setattr(qc, "drama_dir_of", lambda p: tmp_path / "ai_videos" / "d")
    sd, _ = _skill(tmp_path, False)
    assert skill_pack.feedback_gate(sd) is None


def test_edge_overlap_separates_cut_from_flash():
    import numpy as np
    import motion_check as mc
    rng = np.random.default_rng(0)
    base = rng.random((mc.H, mc.W)).astype(np.float32) * 255
    flash = np.clip(base * 0.6 + 120, 0, 255)                # 闪光：亮度整体变、边缘不动
    cut = np.roll(base, (17, 40), axis=(0, 1))               # 切镜：边缘整体移位
    assert mc.edge_overlap(base, flash) >= mc.CUT_OVERLAP
    assert mc.edge_overlap(base, cut) < mc.CUT_OVERLAP


def test_forced_onetake_only_for_skill_videos(tmp_path, monkeypatch):
    import qc
    drama = tmp_path / "ai_videos" / "d"
    drama.mkdir(parents=True)
    (drama / "qc_checks.toml").write_text("[policy]\nskill_video_onetake = true\n", encoding="utf-8")
    monkeypatch.setattr(qc, "drama_dir_of", lambda p: drama)
    assert qc.forced_when(drama / "2_世界观人设" / "characters" / "c1" / "skills" / "k1" / "renders" / "r") == {"一镜到底"}
    assert qc.forced_when(drama / "2_世界观人设" / "characters" / "c1" / "c1_turntable") == set()
