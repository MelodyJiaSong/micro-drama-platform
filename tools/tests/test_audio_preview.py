from tools.audio_preview import display, layout, line_id, spoken


def test_display_and_spoken_use_the_two_sides_of_pronunciation_markup():
    text = "这堵墙叫{栅极|珊极}。（作者备注）"
    assert display(text) == "这堵墙叫栅极。"
    assert spoken({"say": {"珊极": "山极"}}, text) == "这堵墙叫山极。"


def test_layout_splits_long_source_shot_and_keeps_pause():
    spec = {
        "defaults": {"split": True, "max": 15},
        "scenes": [{"id": "s1", "shots": [{"id": "s1", "lines": [
            {"speaker": "林工", "text": "第一句", "pause": 1},
            {"speaker": "林工", "text": "第二句"},
        ]}]}],
    }
    takes = {}
    for text, seconds in (("第一句", 9.0), ("第二句", 9.0)):
        takes[line_id("林工", text)] = {"seconds": seconds, "wav": "unused.wav", "cer": 0}

    shots, total = layout(spec, takes)

    assert [s["id"] for s in shots] == ["s1-1", "s1-2"]
    assert all(not s["over_max"] for s in shots)
    assert shots[0]["duration"] == 12
    assert total == sum(s["duration"] for s in shots)
