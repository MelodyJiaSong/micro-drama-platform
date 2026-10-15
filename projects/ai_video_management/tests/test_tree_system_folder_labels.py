"""The shared library system-folders under `ai_videos/` carry Chinese display
labels (they have no README H1 to derive a title from): `_research` → 选题调研.
The UI renders it as its own library page. (`_actors` → 演员库 went with the
actor pool in follow-up 233; the folder now shows its own name.)"""
from __future__ import annotations

from pathlib import Path

from libs.common.exposed_tree import ExposedTree
from libs.infrastructure.readers.tree__reader import TreeReader


def _ai_videos_children(root: Path) -> dict[str, dict]:
    tree = TreeReader(ExposedTree(root)).build()
    section = next(s for s in tree["children"] if s["name"] == "AI Videos")
    return {c["name"]: c for c in section["children"]}


def test_research_has_chinese_library_label(tmp_path: Path) -> None:
    (tmp_path / "ai_videos" / "_research").mkdir(parents=True)
    by_name = _ai_videos_children(tmp_path)
    assert by_name["_research"]["display_name"] == "选题调研"


def test_removed_libraries_get_no_label(tmp_path: Path) -> None:
    for name in ("_actors", "_performances", "_voices"):
        (tmp_path / "ai_videos" / name).mkdir(parents=True)
    by_name = _ai_videos_children(tmp_path)
    for name in ("_actors", "_performances", "_voices"):
        assert "display_name" not in by_name[name], by_name[name]


def test_drama_folder_label_is_untouched(tmp_path: Path) -> None:
    drama = tmp_path / "ai_videos" / "td"
    drama.mkdir(parents=True)
    (drama / "README.md").write_text("# 《测试剧》— pilot", encoding="utf-8")
    by_name = _ai_videos_children(tmp_path)
    # system-folder map must not shadow a real drama's own H1-derived title
    assert by_name["td"].get("display_name") == "测试剧"
