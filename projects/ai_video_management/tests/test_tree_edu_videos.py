"""follow-up 357：左侧导航「教学视频」一节——系列 → 课程表的季 → 期。"""
from __future__ import annotations

from pathlib import Path

from libs.common.exposed_tree import ExposedTree
from libs.infrastructure.readers.tree__reader import TreeReader

SYLLABUS = """# 课程表

### 第 1 季 · 机器怎么学（2 期）
| 集 | ID | 词 | 一句话 | 前置 |
|---|---|---|---|---|
| 1-1 | t00 ✅ | 什么是 AI | x | 无 |
| 1-2 | t10 | 模型与参数 | x | 1-1 |

### 第 2 季 · 大模型（1 期）
| 集 | ID | 词 | 一句话 | 前置 |
|---|---|---|---|---|
| 2-1 | t05 | 大语言模型 | x | 1-1 |

### 两条观看路线
- 不是一季
"""


def _write(path: Path, text: str = "# x\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _edu(root: Path) -> dict:
    sections = TreeReader(ExposedTree(root)).build()["children"]
    assert [s["name"] for s in sections] == ["AI Videos", "教学视频"]
    return sections[1]


def test_series_lists_seasons_and_episodes_from_the_syllabus(tmp_path: Path) -> None:
    (tmp_path / "ai_videos").mkdir()
    series = tmp_path / "edu_videos/ai_terms"
    _write(series / "README.md", "# AI 高频词（ai_terms）\n")
    _write(series / "课程表.md", SYLLABUS)
    _write(series / "t00_what_is_ai/script.md")
    _write(series / "t00_what_is_ai/preview.json", "{}")
    _write(series / "t00_what_is_ai/storyboard/storyboard.json", "{}")
    _write(series / "t00_what_is_ai/final/t00.mp4", "")
    _write(series / "t10_model_params/script.md")
    _write(series / "t99_extra/script.md")
    _write(tmp_path / "edu_videos/_shared/style.md")

    edu = _edu(tmp_path)
    assert [s["display_name"] for s in edu["children"]] == ["AI 高频词"]
    node = edu["children"][0]
    assert node["navigation_href"] == "/file/edu_videos%2Fai_terms%2F%E8%AF%BE%E7%A8%8B%E8%A1%A8.md"
    labels = [c["display_name"] for c in node["children"]]
    assert labels == ["课程表", "系列说明", "第 1 季 · 机器怎么学（2 期）", "第 2 季 · 大模型（1 期）", "未排进课程表"]
    s1 = node["children"][2]["children"]
    assert [e["display_name"] for e in s1] == ["1-1 什么是 AI ✅", "1-2 模型与参数 · 制作中"]
    assert s1[0]["navigation_href"] == "/episode-preview?path=edu_videos%2Fai_terms%2Ft00_what_is_ai"
    storyboard = s1[0]["children"][0]
    assert storyboard["display_name"] == "故事板"
    assert storyboard["navigation_href"] == "/storyboard-preview?path=edu_videos%2Fai_terms%2Ft00_what_is_ai"
    assert [f["path"] for f in s1[0]["children"]] == ["edu_videos/ai_terms/syllabus/1-1/storyboard",
                                                      "edu_videos/ai_terms/t00_what_is_ai/preview.json",
                                                      "edu_videos/ai_terms/t00_what_is_ai/script.md"]
    assert "navigation_href" not in s1[1]
    assert all(child["name"] != "storyboard" for child in s1[1]["children"])
    planned = node["children"][3]["children"][0]
    assert planned["display_name"] == "2-1 大语言模型 · 规划" and planned["children"] == []
    assert planned["navigation_href"] == node["navigation_href"] + "?ep=2-1"
    paths = [e["path"] for e in s1] + [planned["path"]]
    assert len(set(paths)) == len(paths)   # 虚拟路径不撞
    assert node["children"][4]["children"][0]["name"] == "t99_extra"


def test_series_without_syllabus_lists_topic_folders(tmp_path: Path) -> None:
    (tmp_path / "ai_videos").mkdir()
    _write(tmp_path / "edu_videos/linear_algebra/README.md", "# 线性代数（linear_algebra）\n")
    _write(tmp_path / "edu_videos/linear_algebra/t03_matrix/script.md")
    node = _edu(tmp_path)["children"][0]
    assert node["display_name"] == "线性代数" and "navigation_href" not in node
    assert [c["display_name"] for c in node["children"]] == ["系列说明", "t03_matrix · 制作中"]


def test_no_edu_videos_no_section(tmp_path: Path) -> None:
    (tmp_path / "ai_videos").mkdir()
    assert [s["name"] for s in TreeReader(ExposedTree(tmp_path)).build()["children"]] == ["AI Videos"]
