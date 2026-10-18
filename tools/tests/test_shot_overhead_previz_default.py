"""follow-up 281：默认所有镜头都不做 previz；只有 `[meta] previz = true` 并写理由才做。"""
import pytest

from tools import shot_overhead
from tools.shot_overhead import Bad, previz_decision

BUSY = {"meta": {}, "camera": [{"t": 0, "xy": [0, 0]}, {"t": 4, "xy": [20, 0]}], "actor": []}   # 机位连续移动 20 m
CALM = {"meta": {}, "camera": [{"t": 0, "xy": [0, 0]}], "actor": []}


def test_simple_shot_has_no_previz():
    need, why = previz_decision(CALM, 4)
    assert need is False and "默认不做" in why


def test_complex_shot_still_has_no_previz_but_is_flagged():
    assert shot_overhead.previz_triggers(BUSY, 4)
    need, why = previz_decision(BUSY, 4)
    assert need is False and "复杂镜提示" in why


def test_explicit_previz_needs_a_reason():
    with pytest.raises(Bad):
        previz_decision({**CALM, "meta": {"previz": True}}, 4)
    assert previz_decision({**CALM, "meta": {"previz": True, "previz_why": "打斗编排"}}, 4) == (True, "打斗编排")
