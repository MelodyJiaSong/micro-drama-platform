import json
from pathlib import Path

from libs.common.exposed_tree import ExposedTree
from libs.infrastructure.readers.tree__reader import TreeReader


def _series(tmp_path: Path) -> Path:
    series = tmp_path / "ai_videos/xihuan"
    (series / "framework/templates").mkdir(parents=True)
    (series / "framework/README.md").write_text("# 西幻新剧开发框架", encoding="utf-8")
    (series / "series.json").write_text(json.dumps({"name_zh": "西幻"}), encoding="utf-8")
    return series


def test_framework_folder_becomes_one_dev_node_with_examples_and_drama_dev_docs(tmp_path: Path) -> None:
    series = _series(tmp_path)
    example = series / "framework/examples/lotr"
    example.mkdir(parents=True)
    (example / "01_主题.md").write_text("# 01 主题 · 指环王\n", encoding="utf-8")
    (series / "framework/examples/empty").mkdir()
    drama = series / "new_drama"
    (drama / "0_开发").mkdir(parents=True)
    (drama / "README.md").write_text("# 《银誓》\n", encoding="utf-8")
    (drama / "0_开发/01_主题.md").write_text("# 01 主题\n", encoding="utf-8")

    node = TreeReader(ExposedTree(tmp_path))._walk_series(series, lazy=True)
    dev = next(c for c in node["children"] if c["name"] == "framework")
    assert dev["display_name"] == "新剧开发框架"
    assert dev["navigation_href"] == "/dev-preview?path=ai_videos%2Fxihuan%2Fframework"
    assert not dev.get("is_drama")
    assert [c["display_name"] for c in dev["children"]] == ["试套 · 指环王", "开发稿 · 银誓"]
    assert dev["children"][1]["navigation_href"] == "/dev-preview?path=ai_videos%2Fxihuan%2Fnew_drama%2F0_%E5%BC%80%E5%8F%91"
    assert any(c.get("is_drama") and c["name"] == "new_drama" for c in node["children"])


def test_a_folder_named_framework_without_templates_stays_an_ordinary_member(tmp_path: Path) -> None:
    series = tmp_path / "ai_videos/xihuan"
    (series / "framework").mkdir(parents=True)
    (series / "framework/README.md").write_text("# 一部叫 framework 的剧", encoding="utf-8")
    (series / "series.json").write_text(json.dumps({"name_zh": "西幻"}), encoding="utf-8")
    node = TreeReader(ExposedTree(tmp_path))._walk_series(series, lazy=True)
    member = next(c for c in node["children"] if c["name"] == "framework")
    assert member.get("is_drama")
