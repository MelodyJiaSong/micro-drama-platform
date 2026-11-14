"""chuanyue_yiri ep01 出片前审查 T4：俯视图把同一位置的路点合成一个点后只画最后一个朝向，
「先对镜说话、再转身看城门」前面的朝向丢了；景别（shot_size）没写时人物画高的距离机检从没跑过。"""
import math

from PIL import Image, ImageDraw

from tools import shot_overhead as so

# st4 式：原地（挪了 0.14 m）先看渔夫、转身对镜说话、再回头看鱼筐
RILEY = [[0, 39.1, 57.4, 37.6, 54.0], [7.5, 39.1, 57.4, 37.6, 54.0], [8.5, 39.0, 57.3, 37.4, 54.15],
         [11, 39.0, 57.3, 36.9, 53.9], [12, 39.0, 57.3, 38.5, 59.5], [16.5, 39.0, 57.3, 38.5, 59.5],
         [17.5, 39.0, 57.3, 37.4, 54.15], [18, 39.0, 57.3, 37.4, 54.15]]


def test_half_step_waypoints_merge_into_one_stay():
    assert so.stay_groups(RILEY) == [list(range(8))]
    walk = [[0, 0, 0], [2, 3, 0], [3, 3.1, 0], [5, 6, 0]]
    assert so.stay_groups(walk) == [[0], [1, 2], [3]]


def test_every_distinct_facing_at_a_stay_is_kept_with_its_seconds():
    faces = so.stay_facings(RILEY, list(range(8)))
    assert len(faces) == 2
    (a_fish, spans_fish), (a_cam, spans_cam) = faces
    assert spans_fish == [(0, 11), (17.5, 18)]          # 离开又回来：另记一段
    assert spans_cam == [(12, 16.5)]
    assert abs(math.degrees(a_cam) - math.degrees(math.atan2(59.5 - 57.3, 38.5 - 39.0))) < 1
    assert so.span_text(spans_fish) == "0–11s、17.5–18s"


def test_stay_without_turning_has_one_facing():
    path = [[0, 1, 1, 5, 1], [4, 1, 1, 5, 1.2], [8, 1, 1, 5, 0.8]]
    faces = so.stay_facings(path, [0, 1, 2])
    assert len(faces) == 1 and faces[0][1] == [(0, 8)]


def test_facing_falls_back_to_walking_direction_like_face_vec():
    path = [[0, 0, 0], [2, 0, 0], [4, 0, 3]]         # 停着、没写面朝（0s 无朝向可画），2s 起往南走
    faces = so.stay_facings(path, [0, 1])
    assert len(faces) == 1 and faces[0][1] == [(2, 2)]
    assert abs(math.degrees(faces[0][0]) - 90) < 1


def test_person_glyph_draws_one_wedge_per_facing():
    img = Image.new("RGB", (200, 200), (255, 255, 255))
    d = ImageDraw.Draw(img, "RGBA")
    tips = so._person_glyph(d, (100, 100), [-math.pi / 2, math.pi / 2, 0.0], (38, 110, 196), True)
    assert len(tips) == 3
    for tip in tips:                                   # 每个尖角在圆外那一截都画上了人物色
        q = (round(100 + (tip[0] - 100) * 0.8), round(100 + (tip[1] - 100) * 0.8))
        assert img.getpixel(q) == (38, 110, 196)
    assert so._person_glyph(d, (50, 50), None, (38, 110, 196), False) == []


CAM = {"t": 0, "xy": [0, 0], "look": [0, -5], "lens": 35}


def _cfg(cam: dict, y: float) -> dict:
    return {"meta": {}, "camera": [cam], "actor": [{"key": "c1_A", "label": "甲", "path": [[0, 0, y]]}]}


def test_missing_shot_size_warns_that_the_size_check_was_skipped():
    bad, warn = so.size_errors(_cfg({**CAM, "tag": "他拍·中景"}, -2.1))
    assert bad == []
    assert len(warn) == 1 and "跳过" in warn[0] and "中景" in warn[0]


def test_no_warning_when_shot_has_no_people():
    assert so.size_errors({"meta": {}, "camera": [CAM], "actor": []}) == ([], [])


def test_shot_size_runs_the_distance_check():
    assert so.size_errors(_cfg({**CAM, "shot_size": "中景"}, -2.1)) == ([], [])     # 35mm 中景 ≈ 2.1 m
    bad, warn = so.size_errors(_cfg({**CAM, "shot_size": "特写"}, -8.0))           # 8 m 外拍不成特写
    assert bad == [] and len(warn) == 1 and "特写" in warn[0] and "8.0m" in warn[0]


def test_unknown_shot_size_is_a_blocker():
    bad, _warn = so.size_errors(_cfg({**CAM, "shot_size": "中景0.6"}, -2.1))
    assert len(bad) == 1 and "shot_size" in bad[0]


def test_shot_size_is_an_allowed_camera_key():
    assert "shot_size" in so.KEYS["camera"]
