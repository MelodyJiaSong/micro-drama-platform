"""follow-up 262：overhead [[carry]] 写清谁什么时候带着什么（在手里 / 背在身后），机检把关，previz 人偶据此带上这件东西。"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import overhead_previz
import shot_overhead
from previz import planschema


def aaron(**kw) -> dict:
    return {"key": "c1_Aaron", "label": "亚伦", "path": [[0, 0.0, 0.0, 0.0, -1.0], [8, 0.0, 0.0, 0.0, -1.0]], **kw}


def wolf() -> dict:
    return {"key": "m7_Wolf", "label": "狼甲", "path": [[0, 0.0, -1.2], [8, 0.0, -1.2]]}


def errs(cfg: dict) -> list[str]:
    return shot_overhead.carry_errors(cfg, 8.0)


def test_valid_back_then_hand_carry_passes() -> None:
    cfg = {"actor": [aaron(), wolf()],
           "carry": [{"who": "亚伦", "what": "锤", "key": "p480", "on": "背", "t1": 2},
                     {"who": "亚伦", "what": "锤", "key": "p480", "on": "手", "t0": 2}],
           "hit": [{"t": 3, "who": "亚伦", "target": "狼甲", "with": "锤"}]}
    assert errs(cfg) == []


def test_bad_fields_are_blockers() -> None:
    for bad in ({"who": "米莉", "what": "锤", "on": "手"},          # 不是本镜的 actor
                {"who": "亚伦", "what": "锅", "on": "手"},          # 不认识的件
                {"who": "亚伦", "what": "锤", "on": "腰"},          # 不认识的位置
                {"who": "亚伦", "what": "锤", "on": "手", "t0": 5, "t1": 3},
                {"who": "亚伦", "what": "锤", "on": "手", "t1": 9},
                {"who": "亚伦", "what": "锤", "on": "手", "grip": "臂盾L"}):   # 锤不能挽在臂上
        assert errs({"actor": [aaron()], "carry": [bad]}), bad


def test_same_item_twice_at_once_is_blocker() -> None:
    cfg = {"actor": [aaron()], "carry": [{"who": "亚伦", "what": "锤", "on": "背", "t1": 3},
                                          {"who": "亚伦", "what": "锤", "on": "手", "t0": 2}]}
    assert any("重叠" in e for e in errs(cfg))


def test_same_key_on_two_people_or_on_the_ground_is_blocker() -> None:
    duke = {"key": "c2_Duke", "label": "杜克", "path": [[0, 2.0, 0.0], [8, 2.0, 0.0]]}
    cfg = {"actor": [aaron(), duke], "carry": [{"who": "亚伦", "what": "锤", "key": "p480", "on": "背", "t1": 5},
                                                {"who": "杜克", "what": "锤", "key": "p480", "on": "手", "t0": 4}]}
    assert any("p480" in e for e in errs(cfg))
    ground = {"actor": [aaron()], "carry": [{"who": "亚伦", "what": "锤", "key": "p480", "on": "手", "t0": 1.5}],
              "prop": [{"key": "p480", "label": "泥里的锤", "path": [[0, 1.0, 1.0]], "gone": 2.0}]}
    assert any("p480" in e for e in errs(ground))
    ground["prop"][0]["gone"] = 1.5                       # 1.5 s 捡起来：接得上
    assert errs(ground) == []


def test_weapon_hit_needs_that_weapon_in_hand() -> None:
    cfg = {"actor": [aaron(), wolf()], "carry": [{"who": "亚伦", "what": "锤", "on": "背"}],
           "hit": [{"t": 3, "who": "亚伦", "target": "狼甲", "with": "锤"}]}
    assert any("手里没有" in e for e in errs(cfg))
    cfg["hit"][0]["miss"] = True                          # 故意落空也得拿着锤
    assert any("手里没有" in e for e in errs(cfg))
    cfg["hit"] = [{"t": 3, "who": "狼甲", "target": "亚伦", "with": "咬"}]   # 身体出手不要家伙
    assert errs(cfg) == []
    duke = {"key": "c2_Duke", "label": "杜克", "shield": "左", "path": [[0, 2.0, 0.0], [8, 2.0, 0.0]]}
    shield_hit = {"actor": [duke, wolf()], "hit": [{"t": 3, "who": "杜克", "target": "狼甲", "with": "盾"}]}
    assert errs(shield_hit) == []                         # 盾由 [[actor]] shield 给
    shield_hit["carry"] = [{"who": "杜克", "what": "盾", "on": "手"}]
    assert any("shield" in e for e in errs(shield_hit))  # 手里的盾只在 shield 写一处


def poses(*pairs) -> list[dict]:
    return [{"t": t, "who": "亚伦", "pose": p} for t, p in pairs]


def test_hand_grip_follows_pose_and_back_is_slung() -> None:
    ov = {"actor": [aaron()],
          "carry": [{"who": "亚伦", "what": "锤", "on": "背", "t1": 2},
                    {"who": "亚伦", "what": "锤", "on": "手", "t0": 2}],
          "pose": poses((0, "站"), (2, "站+双手低握"), (3.4, "站+前砸"), (3.7, "站+前砸"), (4, "站+端物"))}
    segs = overhead_previz.carry_segments(ov, ov["actor"][0], ov["actor"][0], 8.0)
    assert [(s["件"], s["姿"], s.get("起"), s.get("止")) for s in segs] == [
        ("锤", "斜背", None, 2), ("锤", "双手低握", 2, 3.4), ("锤", "前砸", 3.4, 4), ("锤", "双手低握", 4, None)]
    assert all(s["长"] == planschema.CARRY_KINDS["锤"][0] for s in segs)


def test_whole_shot_carry_has_no_window_and_custom_grip_and_len() -> None:
    ov = {"actor": [{"key": "c35_Hale", "label": "黑尔", "path": [[0, 0, 0], [6, 0, 0]]}],
          "carry": [{"who": "黑尔", "what": "锤", "on": "手", "len": 0.45, "grip": "单手握R"}],
          "pose": [{"t": 3, "who": "黑尔", "pose": "站+前劈R"}]}
    segs = overhead_previz.carry_segments(ov, ov["actor"][0], ov["actor"][0], 6.0)
    assert [(s["姿"], s["长"], s.get("起"), s.get("止")) for s in segs] == [("单手握R", 0.45, None, 3), ("前劈R", 0.45, 3, None)]


def test_shield_comes_from_actor_shield_and_back_shield_is_named_for_hits() -> None:
    duke = {"key": "c2_Duke", "label": "杜克", "shield": "左", "shield_t": [0, 4], "path": [[0, 0, 0], [8, 0, 0]]}
    ov = {"actor": [duke], "carry": [{"who": "杜克", "what": "盾", "on": "背", "t0": 4}],
          "pose": [{"t": 2, "who": "杜克", "pose": "站+垂盾L"}]}
    segs = overhead_previz.carry_segments(ov, duke, duke, 8.0)
    assert [(s["件"], s["姿"], s.get("起"), s.get("止")) for s in segs] == [
        ("盾", "臂盾L", None, 2), ("盾", "垂盾L", 2, 4), ("背盾", "背盾", 4, None)]


def test_weapon_hits_become_previz_hit_checks() -> None:
    duke = {"key": "c2_Duke", "label": "杜克", "shield": "左", "path": [[0, 2, 0], [8, 2, 0]]}
    ov = {"actor": [aaron(), wolf(), duke],
          "hit": [{"t": 3, "who": "c1_Aaron", "target": "狼甲", "with": "锤", "part": "肩"},
                  {"t": 4, "who": "亚伦", "target": "狼甲", "with": "锤", "miss": True},
                  {"t": 5, "who": "狼甲", "target": "亚伦", "with": "咬"},
                  {"t": 6, "who": "亚伦", "target": "杜克", "with": "锤", "part": "盾面"}]}
    assert overhead_previz.hit_checks(ov) == [
        {"t": 3, "谁": "亚伦", "物件": "亚伦_锤头", "目标": "狼甲"},
        {"t": 6, "谁": "亚伦", "物件": "亚伦_锤头", "目标": "杜克", "部位": "盾"}]


def test_engine_knows_every_grip_the_generator_writes() -> None:
    src = (Path(__file__).resolve().parents[1] / "previz" / "build_previz.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    poses_keys = next(set(ast.literal_eval(k) for k in n.value.keys) for n in tree.body
                      if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "POSES")
    grips = set(planschema.HAND_GRIPS) | set(planschema.SHIELD_GRIPS) | set(planschema.BACK_GRIPS.values()) \
        | {g for _, g in planschema.CARRY_KINDS.values()} | {planschema.SLUNG}
    assert grips <= poses_keys
