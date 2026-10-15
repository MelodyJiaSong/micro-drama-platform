from __future__ import annotations

from pathlib import Path

from tools.workflow_catalog import metadata_problems, plan


def catalog() -> dict:
    return {
        "categories": [{"id": "ai", "number": "1"}],
        "groups": [{"id": "story", "number": "1.1", "category": "ai"}, {"id": "prod", "number": "1.3", "category": "ai"}],
        "sources": [{"path": "a.md", "group": "story"}, {"path": "moved.md", "group": "prod"}],
        "discover": [{"glob": "refs/*.md", "group": "prod"}],
        "source_numbers": {"repo:a.md": "1.1.2", "repo:moved.md": "1.1.4", "repo:refs/old.md": "1.3.7",
                           "repo:gone.md": "1.3.1", "user:.codex/other-machine.toml": "1.3.9"},
    }


def test_fix_compacts_groups_and_sources_and_appends_new(tmp_path: Path) -> None:
    (tmp_path / "refs").mkdir()
    (tmp_path / "refs" / "old.md").write_text("x", encoding="utf-8")
    (tmp_path / "refs" / "new.md").write_text("x", encoding="utf-8")
    result = plan(catalog(), repo=tmp_path, home=tmp_path / "home")
    assert [group["number"] for group in result.groups] == ["1.1", "1.2"]
    assert result.numbers == {
        "repo:a.md": "1.1.1",
        "repo:refs/old.md": "1.2.1", "user:.codex/other-machine.toml": "1.2.2", "repo:moved.md": "1.2.3", "repo:refs/new.md": "1.2.4",
    }
    assert "失效编号 1.3.1 repo:gone.md" in result.problems and "待编号 repo:refs/new.md" in result.problems


def test_sub_pages_number_under_their_parent(tmp_path: Path) -> None:
    data = catalog()
    data["sources"] += [{"path": "a2.md", "group": "story", "parent": "a.md"}, {"path": "a1.md", "group": "story", "parent": "a.md"},
                        {"path": "b.md", "group": "story"}]
    data["source_numbers"].update({"repo:a1.md": "1.1.2.1", "repo:b.md": "1.1.3"})
    result = plan(data, repo=tmp_path, home=tmp_path)
    assert {key: result.numbers[key] for key in ("repo:a.md", "repo:a1.md", "repo:a2.md", "repo:b.md")} == {
        "repo:a.md": "1.1.1", "repo:a1.md": "1.1.1.1", "repo:a2.md": "1.1.1.2", "repo:b.md": "1.1.2"}


def test_clean_catalog_has_no_problems(tmp_path: Path) -> None:
    data = catalog()
    first = plan(data, repo=tmp_path, home=tmp_path)
    data["groups"], data["source_numbers"] = first.groups, first.numbers
    assert plan(data, repo=tmp_path, home=tmp_path).problems == []


def test_format_metadata_references_are_checked(tmp_path: Path) -> None:
    (tmp_path / "film.md").write_text("# 电影\n\n## 节点位置\n", encoding="utf-8")
    data = {
        "formats": [{"id": "film", "title": "电影"}],
        "sources": [
            {"path": "acts.md", "group": "story"},
            {"path": "film.md", "group": "story", "formats": ["film"], "adapts": [{"source": "acts.md", "section": "节点位置"}]},
        ],
    }
    assert metadata_problems(data, repo=tmp_path) == []
    data["sources"][1]["formats"] = ["tv"]
    data["sources"][1]["adapts"] = [{"source": "acts.md", "section": "不存在"}, {"source": "other.md"}]
    data["sources"].append({"path": "shared.md", "group": "story", "adapts": [{"source": "acts.md"}]})
    problems = metadata_problems(data, repo=tmp_path)
    assert "未知片种 tv repo:film.md" in problems
    assert "adapts 小节不存在 repo:film.md #不存在" in problems
    assert "adapts 目标未登记或不在同组 repo:film.md → other.md" in problems
    assert "共用源不能声明 adapts repo:shared.md" in problems


def test_overview_group_is_numbered_zero_and_keeps_module_numbers(tmp_path: Path) -> None:
    data = catalog()
    data["groups"].insert(0, {"id": "overview", "number": "", "category": "ai", "overview": True})
    data["sources"].append({"path": "map.json", "group": "overview"})
    data["source_numbers"]["repo:map.json"] = "1.0.1"
    result = plan(data, repo=tmp_path, home=tmp_path)
    assert [group["number"] for group in result.groups] == ["1.0", "1.1", "1.2"]
    assert result.numbers["repo:map.json"] == "1.0.1" and result.numbers["repo:a.md"] == "1.1.1"

