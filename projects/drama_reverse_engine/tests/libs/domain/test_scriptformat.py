from __future__ import annotations

from libs.domain.value_objects.scriptformat__valueobject import group_scenes, render_episode_script


def _analysis(scene_desc: str, action: str = "走动", characters: tuple[str, ...] = ("裴远",),
              lighting: str = "暖光", performance: str = "") -> dict:
    return {"scene_desc": scene_desc, "action": action, "characters": list(characters),
            "lighting": lighting, "performance": performance}


def test_same_location_consecutive_shots_group_into_one_scene() -> None:
    shots = [{"index": 1}, {"index": 2}, {"index": 3}]
    analyses = {
        1: _analysis("王府大堂内景，梁柱"), 2: _analysis("王府大堂，宫灯"),
        3: _analysis("街市外景，摊贩"),
    }
    scenes = group_scenes(shots, analyses)
    assert [(s.scene_index, s.location, s.interior, s.shot_indexes) for s in scenes] == [
        (1, "王府大堂", "内", (1, 2)), (2, "街市", "外", (3,)),
    ]


def test_halfwidth_comma_scene_desc_still_yields_short_location() -> None:
    """2026-07-18 real run: a scene_desc with half-width commas leaked the whole
    description into the scene heading."""
    scenes = group_scenes([{"index": 1}], {1: _analysis("镇北王府内堂,木质廊柱与悬挂灯笼,裴昭立于堂中")})
    assert scenes[0].location == "镇北王府内堂"


def test_night_detected_from_lighting() -> None:
    scenes = group_scenes([{"index": 1}], {1: _analysis("荒山", lighting="月色清冷")})
    assert scenes[0].time_of_day == "夜" and scenes[0].interior == "外"


def test_render_matches_sample_juben_structure() -> None:
    shots = [{"index": 1}, {"index": 2}]
    analyses = {
        1: _analysis("酒馆内堂，烛光", action="推门而入", performance="眼神冷峻"),
        2: _analysis("酒馆内堂", action="环视四周", characters=("裴远", "掌柜")),
    }
    lines = {
        1: [{"speaker": "掌柜", "text": "你还敢回来？", "dialogue_type": "对白"}],
        2: [{"speaker": "裴远", "text": "此地不宜久留。", "dialogue_type": "内心独白"},
            {"speaker": "旁白", "text": "三年之约已至。", "dialogue_type": "旁白"}],
    }
    script = render_episode_script(1, "废婿归来。", shots, analyses, lines)
    assert script.startswith("第1集：\n\n分集大纲：废婿归来。\n\n正文：\n")
    assert "1-1 日 内 酒馆内堂" in script
    assert "人物：裴远、掌柜" in script
    assert "△酒馆内堂，烛光，暖光。" in script  # follow-up 008: 场次首行氛围 △ 行
    assert "△推门而入，眼神冷峻" in script
    assert "掌柜：你还敢回来？" in script
    assert "裴远（内心独白）：此地不宜久留。" in script
    assert "旁白：三年之约已至。" in script


def test_first_spoken_line_carries_mood_parenthetical() -> None:
    """Follow-up 008: 每镜首句对白带 mood 表演括注，后续对白不重复."""
    analysis = _analysis("酒馆内堂", action="拍案而起")
    analysis["mood"] = "怒极"
    lines = {1: [{"speaker": "裴远", "text": "放肆！", "dialogue_type": "对白"},
                 {"speaker": "裴远", "text": "都给我出去。", "dialogue_type": "对白"}]}
    script = render_episode_script(1, "梗概。", [{"index": 1}], {1: analysis}, lines)
    assert "裴远（怒极）：放肆！" in script
    assert "裴远：都给我出去。" in script


def test_blocking_merged_into_action_line() -> None:
    analysis = _analysis("酒馆内堂", action="环视四周", performance="眼神冷峻")
    analysis["blocking"] = "自画面右侧入画"
    script = render_episode_script(1, "梗概。", [{"index": 1}], {1: analysis}, {})
    assert "△自画面右侧入画，环视四周，眼神冷峻。" in script
