import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools import scene_blocking  # noqa: E402


def test_ranges_compress_consecutive_shots():
    assert scene_blocking._ranges([1]) == "1"
    assert scene_blocking._ranges([1, 2]) == "1·2"
    assert scene_blocking._ranges([3, 4, 5, 8, 9, 10, 11, 14]) == "3–5·8–11·14"


def test_same_card_twice_in_a_shot_is_told_apart_by_label():
    cfg = {"actor": [{"key": "m8_Guard", "label": "卫兵西"}, {"key": "m8_Guard", "label": "卫兵东"},
                     {"key": "c1_Aaron", "label": "亚伦"}]}
    assert scene_blocking._entity_ids(cfg) == ["m8_Guard|卫兵西", "m8_Guard|卫兵东", "c1_Aaron"]


def test_scene_without_any_overhead_draws_nothing(tmp_path):
    drama = tmp_path / "drama"
    (drama / "2_世界观人设").mkdir(parents=True)
    ep = drama / "episodes" / "ep01"
    (ep / "scenes" / "s1" / "shots" / "st1").mkdir(parents=True)
    doc = {"content": {"scenes": [{"id": "s1", "location": "门洞", "time": "清晨",
                                   "shots": [{"id": "st1", "duration": 5, "camera": "全景"}]}]},
           "source_revision": None, "approved_revision": None}
    (ep / "filming.json").write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    assert scene_blocking.render_scene(ep / "scenes" / "s1") is None
    assert not scene_blocking.out_path(ep / "scenes" / "s1").exists()


def test_real_episode_scene_renders_when_overheads_exist():
    scene = Path(__file__).resolve().parents[2] / "ai_videos/shengji_zhilu/episodes/ep01/scenes/s1"
    if not (scene / "shots/st1/planning/overhead.toml").is_file():
        return      # 媒体与镜头目录只在本机；没有就跳过
    out = scene_blocking.render_scene(scene)
    assert out is not None and out.is_file()
