import json
from pathlib import Path

from libs.common.exposed_tree import ExposedTree
from libs.infrastructure.readers.tree__reader import TreeReader


def test_series_lists_shared_library_and_future_dramas(tmp_path: Path) -> None:
    series = tmp_path / "ai_videos/xianxia"
    (series / "first_drama").mkdir(parents=True)
    (series / "first_drama/README.md").write_text("# 第一部", encoding="utf-8")
    library = tmp_path / "ai_videos/_shared/xianxia"
    library.mkdir(parents=True)
    (library / "library.json").write_text('{"assets": []}', encoding="utf-8")
    (series / "series.json").write_text(json.dumps({"name_zh": "仙侠", "shared_library": "ai_videos/_shared/xianxia"}), encoding="utf-8")
    node = TreeReader(ExposedTree(tmp_path))._walk_series(series, lazy=True)
    assert node["type"] == "series"
    assert node["display_name"] == "仙侠"
    assert node["navigation_href"] == "/assets?library=ai_videos%2F_shared%2Fxianxia"
    assert node["children"][0]["display_name"] == "公用资产"
    assert not node["children"][0].get("is_drama")
    assert any(c.get("is_drama") and c["name"] == "first_drama" for c in node["children"])


def test_series_does_not_expose_a_library_outside_the_file_sandbox(tmp_path: Path) -> None:
    series = tmp_path / "ai_videos/xianxia"
    series.mkdir(parents=True)
    private = tmp_path / "private"
    private.mkdir()
    (private / "library.json").write_text("{}", encoding="utf-8")
    (series / "series.json").write_text(json.dumps({"name_zh": "仙侠", "shared_library": "private"}), encoding="utf-8")
    node = TreeReader(ExposedTree(tmp_path))._walk_series(series)
    assert "navigation_href" not in node
    assert all(c["name"] != "shared_library" for c in node["children"])


def test_shared_library_uses_chinese_category_subcategory_and_item_navigation(tmp_path: Path) -> None:
    series = tmp_path / "ai_videos/xianxia"
    library = tmp_path / "ai_videos/_shared/xianxia"
    series.mkdir(parents=True)
    library.mkdir(parents=True)
    (series / "series.json").write_text(json.dumps({"name_zh": "仙侠", "shared_library": "ai_videos/_shared/xianxia"}), encoding="utf-8")
    (library / "library.json").write_text(json.dumps({
        "assets": [{"id": "TAL001", "name": "护身符"}],
        "navigation": [{"id": "talismans", "name": "符咒", "children": [
            {"id": "protection", "name": "护身与避险", "asset_ids": ["TAL001"]}]}],
    }), encoding="utf-8")
    node = TreeReader(ExposedTree(tmp_path))._walk_series(series, lazy=True)
    public = node["children"][0]
    category = public["children"][0]
    subcategory = category["children"][0]
    asset = subcategory["children"][0]
    assert [n["display_name"] for n in [public, category, subcategory, asset]] == ["公用资产", "符咒", "护身与避险", "护身符"]
    assert category["navigation_href"].endswith("&group=talismans")
    assert subcategory["navigation_href"].endswith("&group=talismans&sub=protection")
    assert asset["navigation_href"].endswith("&group=talismans&sub=protection&open=TAL001")
    assert not any(n.get("lazy") for n in [category, subcategory, asset])
