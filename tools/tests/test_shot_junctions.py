# -*- coding: utf-8 -*-
"""镜间接点机检（chuanyue_yiri follow-up 056）：EP1 s1 st1→st2 的原写法必须报，改后的写法和场间接点不报。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shot_junctions import table  # noqa: E402

ST1 = {"id": "st1", "action": "他拍。Riley 背对镜头仰头看城。第 0 秒：她背对镜头、仰头看城。",
       "beats": "0–5秒 背对镜头看城；5.5–15.5秒 小声说那段话；15.5–18秒 说完她越过右肩回头望一眼城门，安静",
       "camera": "他拍，固定机位，镜头静止。全景。",
       "dialogue": "Riley（小声、半笑半喘、不敢相信）：Oh my god. Okay… it worked. That's — that's Pompeii up there. Like, real Pompeii."}
ST2 = {"id": "st2", "action": "自拍：Riley 面对镜头。第 0 秒：她面对镜头，右臂伸出去持镜，嘴还闭着，在笑。",
       "beats": "0–1.5秒 她举着右臂对镜头笑，还没开口；1.5–9秒 说 Good morning from Pompeii!",
       "camera": "自拍：她伸直右臂持镜。近景。",
       "dialogue": "Riley（兴奋、欢快）：Good morning from Pompeii! It's May, 75 AD."}


def flags(rows):
    return [r for r in rows if r.startswith("- ⚠")]


def test_original_ep1_s1_junction_is_flagged():
    rows, bad = table([{"id": "s1", "shots": [ST1, ST2]}])
    text = "\n".join(flags(rows))
    assert bad == 1
    assert "重新打招呼" in text and "Pompeii" in text and "视角来源" in text


def test_bridge_with_handoff_and_restart_passes():
    fixed = dict(ST1, beats=ST1["beats"].replace("说完她越过右肩回头望一眼城门，安静",
                                                 "她边说 Wait, wait — I gotta do this right. 边走向镜头；21–22秒 伸出右手抓向镜头，手掌挡满画面"),
                 dialogue=ST1["dialogue"] + "（笑出来，边走边说：）Wait, wait — I gotta do this right.")
    rows, bad = table([{"id": "s1", "shots": [fixed, ST2]}])
    assert bad == 0 and not any(r.startswith("- ℹ") for r in rows)


def test_cross_scene_junction_listed_not_flagged():
    rows, bad = table([{"id": "s1", "shots": [ST1]}, {"id": "s2", "shots": [ST2]}])
    assert bad == 0 and any("场间接点" in r for r in rows)
