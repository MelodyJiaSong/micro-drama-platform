"""Chinese display_name for staged-pipeline drama + scene folders (tree__reader).

Drama folders are pinyin/English on disk; their Chinese title now lives in
`1_立项/concept.md` (no top-level README). Scene folders are pinyin with the
Chinese name in `{name}.md`'s H1 `（中文）`. Both must surface as `display_name`
so the sidebar shows Chinese.
"""
from __future__ import annotations

import json
from pathlib import Path

from libs.infrastructure.readers.tree__reader import TreeReader


class _FakeExposed:
    def __init__(self, root: Path) -> None:
        self.root = root

    def excluded_dirs(self):
        return set()


def _reader(root: Path) -> TreeReader:
    return TreeReader(_FakeExposed(root))


def test_workflow_stages_expand_into_episode_outputs(tmp_path: Path) -> None:
    from libs.common.episode_workflow import MODULES, MODULE_NAV_LABELS, STATE_CHANGES_FILE, WORLD_FACTS_FILE, WORKFLOW_ID

    project = tmp_path / "ai_videos/demo"
    for episode in ("ep01", "ep02"):
        (project / "episodes" / episode).mkdir(parents=True)
    for directory in ("0_research", "2_世界观人设"):
        (project / directory).mkdir()
        (project / directory / "reference.md").write_text("保留", encoding="utf-8")
    (project / "workflow.json").write_text(json.dumps({"workflow": WORKFLOW_ID}), encoding="utf-8")
    (project / "2_世界观人设" / WORLD_FACTS_FILE).write_text("# 世界规则", encoding="utf-8")
    (project / "episodes/ep01" / STATE_CHANGES_FILE).write_text("# EP1状态变化", encoding="utf-8")
    node = _reader(tmp_path)._walk_project(project)
    assert [child["display_name"] for child in node["children"]] == ["0_research", "1_资产库", *MODULE_NAV_LABELS.values()]
    rules = next(child for child in node["children"][1]["children"] if child["name"] == WORLD_FACTS_FILE)
    assert rules["display_name"] == "世界规则"
    for stage, module in zip(node["children"][2:], MODULES):
        assert stage["type"] == "directory"
        assert [child["display_name"] for child in stage["children"]] == ["EP1", "EP2"]
        if module != "story":
            assert all(child["workflow_module"] == module for child in stage["children"])
            assert stage["children"][1]["path"] == f"ai_videos/demo/episodes/ep02/{module}.json"
        if module == "story":
            current = stage["children"][0]["children"][0]
            assert current["display_name"] == "当前 EP1 · 未选用" and current["type"] == "directory"
            assert "lifetime" not in current
            assert current["children"] == []
            assert len(stage["children"][1]["children"]) == 1


def test_drama_zh_title_from_concept(tmp_path: Path) -> None:
    proj = tmp_path / "ai_videos" / "wushen_juexing"
    (proj / "1_立项").mkdir(parents=True)
    (proj / "1_立项" / "concept.md").write_text("# 立项策划单 · 武神觉醒\n", encoding="utf-8")
    assert _reader(tmp_path)._project_zh_title(proj) == "武神觉醒"


def test_drama_zh_title_readme_still_wins(tmp_path: Path) -> None:
    proj = tmp_path / "ai_videos" / "foo"
    proj.mkdir(parents=True)
    (proj / "README.md").write_text("# 《重生之总裁夫人》— AI 视频项目\n", encoding="utf-8")
    assert _reader(tmp_path)._project_zh_title(proj) == "重生之总裁夫人"


def test_drama_zh_title_drops_paren_qualifier(tmp_path: Path) -> None:
    # `中文（限定语）` — the parenthetical is a qualifier, not the title
    # (`# 热血高校（预告片）` must read 热血高校, not 预告片).
    proj = tmp_path / "ai_videos" / "rexue_gaoxiao"
    proj.mkdir(parents=True)
    (proj / "README.md").write_text("# 热血高校（预告片）\n", encoding="utf-8")
    assert _reader(tmp_path)._project_zh_title(proj) == "热血高校"


def test_drama_zh_title_paren_qualifier_after_middle_dot(tmp_path: Path) -> None:
    proj = tmp_path / "ai_videos" / "rexue_gaoxiao"
    (proj / "1_立项").mkdir(parents=True)
    (proj / "1_立项" / "concept.md").write_text(
        "# 立项策划单 · 热血高校（预告片）\n", encoding="utf-8"
    )
    assert _reader(tmp_path)._project_zh_title(proj) == "热血高校"


def test_scene_zh_label_from_paren(tmp_path: Path) -> None:
    scene = tmp_path / "ai_videos" / "d" / "2_世界观人设" / "scenes" / "zhenbei_wangfu_zhengting"
    scene.mkdir(parents=True)
    (scene / "zhenbei_wangfu_zhengting.md").write_text(
        "# zhenbei_wangfu_zhengting（镇北王府正厅）\n", encoding="utf-8"
    )
    assert _reader(tmp_path)._sidecar_zh_label(scene) == "镇北王府正厅"


def test_non_scene_dir_gets_no_label(tmp_path: Path) -> None:
    # a character folder (parent != scenes) must NOT pick up a label from its .md
    char = tmp_path / "ai_videos" / "d" / "2_世界观人设" / "characters" / "c1_裴知秋"
    char.mkdir(parents=True)
    (char / "c1_裴知秋.md").write_text("# 裴知秋 · 角色档\n", encoding="utf-8")
    assert _reader(tmp_path)._sidecar_zh_label(char) is None


def test_missing_sources_return_none(tmp_path: Path) -> None:
    proj = tmp_path / "ai_videos" / "empty"
    proj.mkdir(parents=True)
    assert _reader(tmp_path)._project_zh_title(proj) is None


def test_scene_main_md_leaf_has_zh_display(tmp_path: Path) -> None:
    # the scene's main sidecar .md leaf shows Chinese (name/path stay pinyin)
    scene = tmp_path / "ai_videos" / "d" / "2_世界观人设" / "scenes" / "jishi_changjie"
    scene.mkdir(parents=True)
    f = scene / "jishi_changjie.md"
    f.write_text("# jishi_changjie（集市长街）\n", encoding="utf-8")
    node = _reader(tmp_path)._leaf_for(f)
    assert node["display_name"] == "集市长街"
    assert node["name"] == "jishi_changjie.md"          # name stays pinyin (routing/open)
    assert node["path"].endswith("jishi_changjie.md")   # path stays pinyin


def test_scene_plate_md_leaf_no_display(tmp_path: Path) -> None:
    # a plate .md never takes its H1 (a prompt title) as label — only the
    # routing-key label every keyed scenes-tree node gets (follow-up 173)
    plate = tmp_path / "ai_videos" / "d" / "2_世界观人设" / "scenes" / "jishi_changjie" / "bg1_顺街_全景"
    plate.mkdir(parents=True)
    f = plate / "bg1_顺街_全景.md"
    f.write_text("# bg1_顺街_全景 · 集市长街 顺街全景\n", encoding="utf-8")
    assert _reader(tmp_path)._leaf_for(f)["display_name"] == "bg1 顺街_全景.md"


def test_shot_md_leaf_no_display(tmp_path: Path) -> None:
    # ordinary md leaves (not scene main sidecar) unchanged
    d = tmp_path / "ai_videos" / "d" / "5_6_分镜与prompt" / "episodes" / "ep02" / "shots" / "shot01"
    d.mkdir(parents=True)
    f = d / "shot01.md"
    f.write_text("# ep02 / shot01 · 离家上路\n", encoding="utf-8")
    assert "display_name" not in _reader(tmp_path)._leaf_for(f)
