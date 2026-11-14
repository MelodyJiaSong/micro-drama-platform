# -*- coding: utf-8 -*-
"""提交出片前的分镜机检（chuanyue_yiri follow-up 059）：剧级登记表把检查登记为闸门才跑；只报要出的镜头。"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import shot_take  # noqa: E402

SHOT = {"id": "st1", "duration": 5, "cast": ["c1"], "action": "他拍。Riley 走过街。第 0 秒：她站在路缘。", "blocking": "x",
        "beats": "0–5秒 她走过街", "camera": "他拍，固定机位。", "lighting": "清晨", "dialogue": ""}


def make(tmp: Path, registry: str, point: bool) -> Path:
    d = tmp / "ai_videos" / "demo"
    (d / "2_世界观人设" / "characters").mkdir(parents=True)
    (d / "workflow.json").write_text(json.dumps({"workflow": "three-module-v1"}), encoding="utf-8")
    if registry:
        (d / "qc_checks.toml").write_text(registry, encoding="utf-8")
    ep = d / "episodes" / "ep01"; ep.mkdir(parents=True)
    shots = [dict(SHOT, point="看懂街就是排水沟")] if point else [dict(SHOT)]
    shots.append(dict(SHOT, id="st2", point="另一镜"))
    (ep / "filming.json").write_text(json.dumps({"content": {"scenes": [{"id": "s1", "shots": shots}]}}, ensure_ascii=False), encoding="utf-8")
    return ep


REG = '[[check]]\nid = "filming.point_written"\nstage = "keyframe"\nkind = "machine"\ngate = true\nauto = true\ndesc = "x"\nbasis = "x"\nsources = []\n'


def test_missing_point_blocks_only_that_shot(tmp_path):
    ep = make(tmp_path, REG, point=False)
    assert any("没写看点" in p for p in shot_take.filming_checks(ep, ["ep1_s1_st1"]))
    assert shot_take.filming_checks(ep, ["ep1_s1_st2"]) == []


def test_drama_without_registry_is_not_checked(tmp_path):
    ep = make(tmp_path, "", point=False)
    assert shot_take.filming_checks(ep, ["ep1_s1_st1"]) == []
