import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import audience_check

README = "# 剧\n\n## Vision（观众体验）\n\n> **一句话体验。**\n\n核心：一个问题。\n\n说明。\n\n## 其他\n"
STORY = """# 决策

本集体验：一次探索。
Vision：服务「每到一处都震撼」。

## 体验地图

| 段 | 体验 | 事件 |
|---|---|---|
| 开场 | 震撼 | 抵达城门 |
| 第一段 | 心疼 | 救人失手 |

## 观众轨

| 段 | 知道 | 在等 | 处理 |
|---|---|---|---|
| 开场 | 他要进城 | 城有多大 | 兑现 |
"""
SCENE = "# s1\n\nVision：抵达的宏伟。\n\n## 观众\n\n进场时观众在等城门。\n\n## 场的设定\n"


def _drama(tmp: Path, story=STORY, scene=SCENE, readme=README, review=None) -> Path:
    d = tmp / "drama"
    ep = d / "episodes" / "ep01"
    (ep / "decisions").mkdir(parents=True)
    (ep / "scenes" / "s1").mkdir(parents=True)
    (d / "README.md").write_text(readme, encoding="utf-8")
    (ep / "decisions" / "story.md").write_text(story, encoding="utf-8")
    (ep / "decisions" / "filming.md").write_text("# f\n\nVision：x\n", encoding="utf-8")
    (ep / "scenes" / "s1" / "decisions.md").write_text(scene, encoding="utf-8")
    if review is not None:
        for name, text in review.items():
            r = ep / "scenes" / "s1" / "shots" / "st1" / "renders" / name
            r.mkdir(parents=True)
            (r / "review.md").write_text(text, encoding="utf-8")
    return d


def test_complete_drama_passes(tmp_path):
    assert audience_check.run(_drama(tmp_path)) == []


def test_missing_vision_section_or_multi_sentence_is_reported(tmp_path):
    d = _drama(tmp_path, readme="# 剧\n\n## 其他\n")
    assert any("Vision（观众体验）" in i for i in audience_check.run(d))
    two = README.replace("> **一句话体验。**", "> 第一句\n> 第二句")
    d2 = _drama(tmp_path / "b", readme=two)
    assert any("一句话" in i for i in audience_check.run(d2))


def test_orphan_event_without_experience_is_reported(tmp_path):
    story = STORY.replace("| 第一段 | 心疼 | 救人失手 |", "| 第一段 |  | 救人失手 |")
    issues = audience_check.run(_drama(tmp_path, story=story), module="story")
    assert issues == [i for i in issues if "第一段" in i and "体验" in i] and len(issues) == 1


def test_story_missing_episode_experience_and_audience_track(tmp_path):
    story = STORY.replace("本集体验：一次探索。\n", "").split("## 观众轨")[0]
    issues = audience_check.run(_drama(tmp_path, story=story), module="story")
    assert any("本集体验" in i for i in issues)
    assert any("观众轨" in i for i in issues)


def test_scene_missing_audience_section_is_reported(tmp_path):
    scene = "# s1\n\nVision：x\n\n## 观众\n\n## 场的设定\n"
    issues = audience_check.run(_drama(tmp_path, scene=scene), module="filming")
    assert len(issues) == 1 and "## 观众" in issues[0]


def test_render_review_vision_only_required_after_cutoff(tmp_path):
    review = {"20261011-120000_aaaa": "对的：x", "20261012-090000_bbbb": "对的：x",
              "20261013-090000_cccc": "Vision：抵达的宏伟到位\n对的：x"}
    issues = audience_check.run(_drama(tmp_path, review=review), module="render")
    assert len(issues) == 1 and "20261012-090000_bbbb" in issues[0]


def test_cli_exit_code(tmp_path):
    assert audience_check.main([str(_drama(tmp_path))]) == 0
    assert audience_check.main([str(_drama(tmp_path / "b", readme="# x\n"))]) == 1


def test_missing_core_line_is_reported(tmp_path):
    d = _drama(tmp_path, readme=README.replace("核心：一个问题。\n\n", ""))
    issues = audience_check.run(d, module="story")
    assert len(issues) == 1 and "核心" in issues[0]


def test_empty_item_does_not_borrow_the_next_line():
    assert audience_check._line_value("状态：待审核\nVision：\n\n## 对的\n", "Vision") == ""
    assert audience_check._line_value("Vision：\n核心：x\n", "Vision") == ""
    assert audience_check._line_value("Vision：\n核心：x\n", "核心") == "x"
