"""技能视频出片前的时间轴审阅关卡（用户 2026-10-24 定为必要流程）。"""
from pathlib import Path

import pytest

from tools import skill_pack

TEXT = "k901_Test_clip\n时长：8秒\n位置：甲在左，乙在右。\n0–1秒 乙冲来。\n1.0秒 光柱落下。\n负面词：白天"


def card(tmp_path: Path) -> Path:
    sd = tmp_path / "k901_Test"
    sd.mkdir()
    (sd / "k901_Test.md").write_text("# 卡\n\n## 技能视频 prompt\n\n视频参考: a=x.png\n\n```text\n" + TEXT + "\n```\n", encoding="utf-8")
    return sd


@pytest.fixture
def shot(monkeypatch: pytest.MonkeyPatch):
    state = {"text": TEXT}
    monkeypatch.setattr(skill_pack, "shot", lambda sd: {"id": sd.name + "_clip", "text": state["text"], "refs": []})
    return state


def test_timeline_rows_and_fingerprint_ignore_negatives(shot):
    rows, fp = skill_pack.timeline(shot)
    assert rows == [("0–1秒", "乙冲来。"), ("1.0秒", "光柱落下。")]
    shot["text"] = TEXT.replace("负面词：白天", "负面词：白天，阳光")
    assert skill_pack.timeline(shot)[1] == fp
    shot["text"] = TEXT.replace("时长：8秒", "时长：10秒")
    assert skill_pack.timeline(shot)[1] != fp


def test_submit_blocked_until_current_timeline_approved(tmp_path: Path, shot):
    sd = card(tmp_path)
    with pytest.raises(SystemExit, match="还没经用户审阅"):
        skill_pack.check_approved(sd)
    fp = skill_pack.approve(sd)
    skill_pack.check_approved(sd)
    text = (sd / "k901_Test.md").read_text(encoding="utf-8")
    assert text.count("时间轴审阅:") == 1 and fp in text and text.index("时间轴审阅:") < text.index("视频参考:")
    shot["text"] = TEXT.replace("1.0秒 光柱落下。", "1.5秒 光柱落下。")
    with pytest.raises(SystemExit):
        skill_pack.check_approved(sd)
    skill_pack.approve(sd)
    assert (sd / "k901_Test.md").read_text(encoding="utf-8").count("时间轴审阅:") == 1
