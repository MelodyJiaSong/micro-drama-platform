import json
from pathlib import Path

from tools import episode_post as ep


def _ev(tmp_path: Path, words, start=10.0, cut_in=1.0, cut_out=9.0):
    d = tmp_path / "take"; d.mkdir(exist_ok=True)
    (d / "annotation.json").write_text(json.dumps({"words": words}), encoding="utf-8")
    return {"scene": "s1", "shot": "st2", "in": cut_in, "out": cut_out, "start": start, "take_dir": d}


def test_subtitles_follow_spoken_words_in_order(tmp_path):
    words = [{"w": "Brother", "s": 2.0, "e": 2.3}, {"w": "sent", "s": 2.3, "e": 2.6}, {"w": "me.", "s": 2.6, "e": 3.0},
             {"w": "Brother", "s": 5.0, "e": 5.3}, {"w": "Samuel?", "s": 5.3, "e": 5.8}]
    ev = _ev(tmp_path, words)
    subs = [{"scene": "s1", "shot": "st2", "from": "brother", "to": "me", "en": "a", "zh": "甲"},
            {"scene": "s1", "shot": "st2", "from": "brother", "to": "samuel", "en": "b", "zh": "乙"}]
    a, b = ep.subtitle_times(subs, [ev])
    assert (a["start"], a["end"]) == (11.0, 12.0)            # 条里 2.0 秒 → 成片 10 + (2.0 − 入点 1.0)
    assert (b["start"], b["end"]) == (14.0, 14.8)            # 第二个 Brother 往后找
    assert a["show_end"] == 12.3                            # 说完多留 0.3 秒
    assert b["show_end"] == 15.2                            # 0.8 秒的短句至少显示 1.2 秒
    assert "00:00:11,000 --> 00:00:12,300\n甲\na" in ep.srt([a, b])


def test_words_outside_the_cut_are_not_used(tmp_path):
    ev = _ev(tmp_path, [{"w": "Hello", "s": 0.2, "e": 0.5}], cut_in=1.0)
    try:
        ep.subtitle_times([{"scene": "s1", "shot": "st2", "from": "hello", "to": "hello", "en": "x", "zh": "x"}], [ev])
    except SystemExit as e:
        assert "找不到" in str(e)
    else:
        raise AssertionError("剪掉的词不该当字幕")


def test_gain_is_one_inside_dialogue_and_scene_gain_outside():
    expr = ep.gain_expr([(2.0, 3.0)], [(0.0, 10.0, 0.5)], 0.2)
    assert "clip(min((t-1.800)/0.200" in expr and "between(t\,0.000\,10.000)*0.50000" in expr


def _at(expr: str, t: float) -> float:
    env = {"t": t, "min": min, "clip": lambda x, lo, hi: max(lo, min(hi, x))}
    return eval(expr.replace("\,", ","), {}, env)


def test_music_ducks_under_dialogue_and_recovers():
    expr = ep.duck_expr([(5.0, 8.0)], -12, 0.3)
    assert abs(_at(expr, 6.0) - 10 ** (-12 / 20)) < 1e-4       # 台词里压低 12 dB
    assert _at(expr, 2.0) == 1 and _at(expr, 9.0) == 1          # 台词外原样
    assert 10 ** (-12 / 20) < _at(expr, 4.85) < 1               # 进台词前 0.3 秒内渐变
    assert ep.duck_expr([], -12, 0.3) == "1-0.74881*min(1\,(0))"
