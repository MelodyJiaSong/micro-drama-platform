# -*- coding: utf-8 -*-
"""分镜机检 [动机] [过演] [跨语言]（chuanyue_yiri follow-up 062）：EP1 s3 面包房那段原写法必须报，改好的写法不报。"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from filming_lint import lint  # noqa: E402

BAD = {"id": "st4", "duration": 10, "cast": ["c1", "c2"], "point": "她听不懂指路，只抓到一个词",
       "action": "Riley 问他鱼露；Felix 两手端着托板，头一直低着，眼睛只看托板上的面包，飞快地说了一句。",
       "beats": "0–2秒 Riley 问 Garum；2–5秒 Felix 头一直低着说那句拉丁语；5–6秒 Felix 鼓起腮帮憋住笑", "blocking": "x",
       "camera": "他拍", "lighting": "x",
       "dialogue": "Riley（问，美式英语）：Garum? / Felix（拉丁语，飞快）：Hac recta platea… ito ad dextram!"}
GOOD = dict(BAD,
            action="Riley 举起掰下的面包、指指街上问他哪里有鱼露；Felix 两手端着满托板，抬眼看她，用下巴朝街上一努，飞快地说了一句。",
            beats="0–2秒 Riley 举着面包、指指街上问；2–5秒 Felix 抬眼看她，用下巴朝街上一努说那句拉丁语；5–6秒 Felix 嘴角微微一动",
            dialogue="Riley（问，美式英语）：Garum? Where can I get garum? / Felix（拉丁语，飞快）：Hac recta platea… ito ad dextram!")


def run(tmp: Path, shot: dict) -> list[str]:
    d = tmp / "ai_videos" / "demo"
    (d / "2_世界观人设" / "characters" / "c2_Felix").mkdir(parents=True, exist_ok=True)
    ep = d / "episodes" / "ep01"; ep.mkdir(parents=True, exist_ok=True)
    (ep / "filming.json").write_text(json.dumps({"content": {"scenes": [{"id": "s3", "shots": [shot]}]}}, ensure_ascii=False), encoding="utf-8")
    return lint(ep, None)


def test_bakery_original_is_flagged(tmp_path):
    out = "\n".join(run(tmp_path, BAD))
    assert "[动机]" in out and "[过演]" in out and "[跨语言]" in out


def test_bakery_rewrite_passes(tmp_path):
    out = run(tmp_path, GOOD)
    assert not [p for p in out if any(t in p for t in ("[动机]", "[过演]", "[跨语言]"))], out
