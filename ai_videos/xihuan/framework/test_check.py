"""check.py 回归测试（框架 v0.4）：沿用两部试套找出的漏报（汉字旁的编号、只有表头的表、种族行没有库映射），
加上 v0.4 的「图要画得出来」与「不谈季与集」。

    python -m pytest ai_videos/xihuan/framework/test_check.py -q -p no:cacheprovider
"""
from __future__ import annotations

from pathlib import Path

import check

PAGES = {
    "01_主题": "## 一句话\n权力会腐蚀想用它行善的人。\n## 一段\n一段。\n## 一页\n一页。\n",
    "02_世界": "## 舞台\n一片大陆。\n## 种族与势力\n| 名称 | 库 | 一句话 |\n|---|---|---|\n| 精灵 | RC02 | 正在离开 |\n| 魔君 | 原创 | 想要戒指 |\n## 关系\n| 从 | 关系 | 到 |\n|---|---|---|\n| 精灵 | 世仇 | 魔君 |\n## 正在发生的变化\n战争将起。\n",
    "03_力量": "## 力量源\n| 力量 | 库 | 谁拥有 | 代价 |\n|---|---|---|---|\n| 戒指 | IT26 | 持戒人 | 腐蚀 |\n## 强弱阶梯\n| 层级 | 谁在这一层 |\n|---|---|\n| 顶 | 魔君 |\n| 底 | 小人物 |\n## 克制\n| 克制者 | 被克制 |\n|---|---|\n| 怜悯 | 戒指 |\n",
    "04_人物": "## 人物\n| 编号 | 名字 | 身份 | 想要 | 缺陷 |\n|---|---|---|---|---|\n| P01 | 弗罗多 | 小人物 | 回家 | 天真 |\n| **P02** | 山姆 | 园丁 | 守护 | 胆小 |\n## 能力\n| 编号 | 外在 | 外 | 内在 | 内 |\n|---|---|---|---|---|\n| P01 | 体弱 | 1 | 能扛 | 5 |\n| P02 | 能打 | 3 | 忠心 | 4 |\n## 关系\n| 从 | 关系 | 到 |\n|---|---|---|\n| P02 | 誓死追随 | P01 |\n",
    "05_矛盾": "## 主要矛盾\nP01 与魔君争夺戒指的归宿。\n## 矛盾图\n| 一方 | 争什么 | 另一方 | 主次 |\n|---|---|---|---|\n| P01 | 戒指 | 魔君 | 主 |\n| P01 | 信任 | P02 | 次 |\n## 内在矛盾\n想放下与想占有。\n",
}


def write(tmp: Path, **overrides: str) -> Path:
    for page, text in {**PAGES, **overrides}.items():
        (tmp / f"{page}.md").write_text(text, encoding="utf-8")
    return tmp


def errs(tmp: Path, **overrides: str) -> list[str]:
    return check.check(write(tmp, **overrides))


def test_clean_folder_passes(tmp_path: Path) -> None:
    warnings: list[str] = []
    assert check.check(write(tmp_path), warnings) == []
    assert warnings == []


def test_ids_glued_to_chinese_are_still_checked(tmp_path: Path) -> None:
    e = errs(tmp_path, **{"05_矛盾": PAGES["05_矛盾"].replace("想放下与想占有。", "人物P99与库条目RC99型。")})
    assert any("P99" in x for x in e) and any("RC99" in x for x in e)


def test_header_only_table_counts_as_empty(tmp_path: Path) -> None:
    e = errs(tmp_path, **{"03_力量": PAGES["03_力量"].replace("| 怜悯 | 戒指 |\n", "")})
    assert any("克制" in x and "只有表头" in x for x in e)


def test_world_row_needs_library_mapping(tmp_path: Path) -> None:
    e = errs(tmp_path, **{"02_世界": PAGES["02_世界"].replace("| 魔君 | 原创 |", "| 魔君 | — |")})
    assert any("魔君" in x and "库" in x for x in e)


def test_diagram_edges_must_resolve(tmp_path: Path) -> None:
    world = PAGES["02_世界"].replace("| 精灵 | 世仇 | 魔君 |", "| 精灵 | 世仇 | 矮人 |")
    people = PAGES["04_人物"].replace("| P02 | 誓死追随 | P01 |", "| P02 | 誓死追随 | 弗罗多 |")
    conflict = PAGES["05_矛盾"].replace("| P01 | 信任 | P02 | 次 |", "| P01 | 信任 | 兽人 | 次 |")
    e = errs(tmp_path, **{"02_世界": world, "04_人物": people, "05_矛盾": conflict})
    assert any("矮人" in x for x in e)
    assert any("弗罗多" in x and "编号" in x for x in e)
    assert any("兽人" in x for x in e)


def test_power_source_can_be_a_conflict_endpoint(tmp_path: Path) -> None:
    """《指环王》试套：真正的主要矛盾是 P01 对魔戒本身（v0.4 复测）。"""
    conflict = PAGES["05_矛盾"].replace("| P01 | 戒指 | 魔君 | 主 |", "| P01 | 放下 | 戒指 | 主 |")
    assert errs(tmp_path, **{"05_矛盾": conflict}) == []


def test_abilities_cover_every_person_with_scores(tmp_path: Path) -> None:
    """人物能力分外在 / 内在，各打 1–5 分（xihuan follow-up 004）。"""
    no_row = PAGES["04_人物"].replace("| P02 | 能打 | 3 | 忠心 | 4 |\n", "")
    assert any("能力" in x and "P02" in x for x in errs(tmp_path, **{"04_人物": no_row}))
    bad = PAGES["04_人物"].replace("| P01 | 体弱 | 1 | 能扛 | 5 |", "| P01 | 体弱 | 低 | 能扛 | 7 |")
    e = errs(tmp_path, **{"04_人物": bad})
    assert any("「外」" in x for x in e) and any("「内」" in x for x in e)
    stranger = PAGES["04_人物"].replace("| P02 | 能打 |", "| P09 | 能打 |")
    assert any("P09" in x for x in errs(tmp_path, **{"04_人物": stranger}))
    empty = PAGES["04_人物"].replace("| P01 | 体弱 | 1 | 能扛 | 5 |\n| P02 | 能打 | 3 | 忠心 | 4 |\n", "")
    assert any("能力" in x and "只有表头" in x for x in errs(tmp_path, **{"04_人物": empty}))


def test_conflict_map_needs_a_main_conflict(tmp_path: Path) -> None:
    e = errs(tmp_path, **{"05_矛盾": PAGES["05_矛盾"].replace("| 魔君 | 主 |", "| 魔君 | 次 |")})
    assert any("主次" in x for x in e)


def test_undefined_person_and_row_limit(tmp_path: Path) -> None:
    e = errs(tmp_path, **{"03_力量": PAGES["03_力量"].replace("| 顶 | 魔君 |", "| 顶 | P07 |")})
    assert any("P07" in x for x in e)
    many = PAGES["03_力量"].replace("| 底 | 小人物 |", "\n".join(f"| {i} | 某人 |" for i in range(13)))
    assert any("超过 12" in x for x in errs(tmp_path, **{"03_力量": many}))


def test_prose_limit_for_core_pages(tmp_path: Path) -> None:
    e = errs(tmp_path, **{"02_世界": PAGES["02_世界"].replace("一片大陆。", "字" * 301)})
    assert any("超过 300" in x for x in e)


def test_season_and_episode_concepts_are_rejected(tmp_path: Path) -> None:
    """季与集是下一步的事（用户 2026-11-08）。"""
    for bad in ("第 2 季揭开。", "每集结尾留钩子。", "在 1-09 揭开。", "S2E09 揭开。", "季末大战。", "集长 90 秒。"):
        e = errs(tmp_path, **{"05_矛盾": PAGES["05_矛盾"] + bad + "\n"})
        assert any("季 / 集" in x for x in e), bad
    for fine in ("四季轮转的森林。", "诸族集结。", "中点之前揭开。"):
        assert errs(tmp_path, **{"05_矛盾": PAGES["05_矛盾"] + fine + "\n"}) == [], fine


def test_optional_pages_are_optional_but_checked_when_present(tmp_path: Path) -> None:
    warnings: list[str] = []
    secret = "## 秘密\n| 秘密 | 谁知道 | 何时揭开 | 揭开后改变什么 |\n|---|---|---|---|\n| 戒指身份 | P01 | 很久以后 | 一切 |\n"
    assert check.check(write(tmp_path, **{"06_秘密与伏笔": secret}), warnings) == []
    assert any("故事阶段" in w for w in warnings)


def test_missing_page_is_reported(tmp_path: Path) -> None:
    write(tmp_path)
    (tmp_path / "05_矛盾.md").unlink()
    assert "缺页：05_矛盾.md" in check.check(tmp_path)
