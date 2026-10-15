# -*- coding: utf-8 -*-
"""工作流目录编号整理：组号在类别内连续，源号在组内从 1 连续，子页（`parent`）在父页编号下从 1 连续，界面按编号排序。

    python tools/workflow_catalog.py --check [--quiet]   # 有缺号、乱号、待编号或失效编号时退出码 1（Claude Stop hook 用）
    python tools/workflow_catalog.py --fix               # 按现有相对顺序重排；新发现的源追加到所在组末尾

总览组（follow-up 219）：组上写 `"overview": true`，编号为「类别号.0」，排在模块之前，不占模块编号。
片种（follow-up 211）：顶层 `formats` 声明片种；源的 `formats` 标明只适用哪些片种（缺省=共用），
`adapts` 列出它改写的共用源及本文对应小节标题。--check 一并核对这些引用。

源身份是 `scope:path`，改标题不改号；增删或迁移源后跑 --fix。用户级源只在本机能发现，
本机找不到的用户级编号保留原位（可能存在于别的电脑）。
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CATALOG = REPO / ".agents" / "references" / "project" / "workflow_catalog.json"


@dataclass(frozen=True)
class Plan:
    groups: list[dict[str, str]]
    numbers: dict[str, str]
    problems: list[str]


def _key(scope: str, path: str) -> str:
    return f"{scope}:{path}"


def _order(number: str) -> tuple[int, ...]:
    return tuple(int(part) for part in number.split("."))


def _discovered(data: dict, repo: Path, home: Path) -> dict[str, str]:
    found: dict[str, str] = {}
    for rule in data["discover"]:
        scope = rule.get("scope", "repo")
        base = home if scope == "user" else repo
        for path in sorted(base.glob(rule["glob"])):
            if path.is_file():
                found.setdefault(_key(scope, path.relative_to(base).as_posix()), rule["group"])
    return found


def plan(data: dict, repo: Path = REPO, home: Path = Path.home()) -> Plan:
    old_numbers: dict[str, str] = data.get("source_numbers", {})
    old_group_by_number = {group["number"]: group["id"] for group in data["groups"]}
    groups = [dict(group) for group in data["groups"]]
    for category in data["categories"]:
        members = [group for group in groups if group.get("category") == category["id"]]
        # An overview group sits above the modules: it is {category}.0 and does not take a module number.
        for group in members:
            if group.get("overview"):
                group["number"] = f"{category['number']}.0"
        for index, group in enumerate([group for group in members if not group.get("overview")], 1):
            group["number"] = f"{category['number']}.{index}"
    owners: dict[str, str] = _discovered(data, repo, home)
    owners.update({_key(source.get("scope", "repo"), source["path"]): source["group"] for source in data["sources"]})
    problems: list[str] = []
    for key, number in old_numbers.items():
        if key in owners:
            continue
        group = old_group_by_number.get(number.rsplit(".", 1)[0])
        if key.startswith("user:") and group:
            owners[key] = group
        else:
            problems.append(f"失效编号 {number} {key}")
    numbers: dict[str, str] = {}
    by_number = {group["id"]: group["number"] for group in groups}
    old_prefix = {group["id"]: group["number"] for group in data["groups"]}
    parents = {_key(source.get("scope", "repo"), source["path"]): _key(source.get("scope", "repo"), source["parent"])
               for source in data["sources"] if source.get("parent")}
    for child, parent in parents.items():
        if owners.get(parent) != owners.get(child):
            problems.append(f"父页不存在或不在同组 {child} → {parent}")

    def rank(key: str, old_container: str) -> tuple[int, tuple[int, ...], str]:
        if key not in old_numbers:
            return 2, (), key
        native = old_numbers[key].rsplit(".", 1)[0] == old_container
        return (0 if native else 1), _order(old_numbers[key]), key

    def assign(prefix: str, old_container: str, keys: list[str]) -> None:
        for index, key in enumerate(sorted(keys, key=lambda key: rank(key, old_container)), 1):
            numbers[key] = f"{prefix}.{index}"
            children = [child for child, parent in parents.items() if parent == key and child in owners]
            if children:
                assign(numbers[key], old_numbers.get(key, ""), children)

    for group_id, group_number in by_number.items():
        assign(group_number, old_prefix.get(group_id, ""), [key for key, owner in owners.items() if owner == group_id and key not in parents])
    for key in owners:
        if key not in old_numbers:
            problems.append(f"待编号 {key}")
        elif old_numbers[key] != numbers.get(key):
            problems.append(f"编号不连续 {old_numbers[key]} → {numbers.get(key)} {key}")
    for old, new in zip(data["groups"], groups):
        if old["number"] != new["number"]:
            problems.append(f"组号不连续 {old['number']} → {new['number']} {old['id']}")
    unknown = {owner for owner in owners.values()} - set(by_number)
    problems.extend(f"未知组 {group}" for group in sorted(unknown))
    return Plan(groups, numbers, problems)


def metadata_problems(data: dict, repo: Path = REPO) -> list[str]:
    format_ids = {entry["id"] for entry in data.get("formats", [])}
    by_key = {_key(source.get("scope", "repo"), source["path"]): source for source in data["sources"]}
    problems: list[str] = []
    for key, source in by_key.items():
        problems.extend(f"未知片种 {value} {key}" for value in source.get("formats", []) if value not in format_ids)
        adapts = source.get("adapts", [])
        if adapts and not source.get("formats"):
            problems.append(f"共用源不能声明 adapts {key}")
        headings: set[str] | None = None
        for entry in adapts:
            target = by_key.get(_key(source.get("scope", "repo"), entry["source"]))
            if not target or target["group"] != source["group"]:
                problems.append(f"adapts 目标未登记或不在同组 {key} → {entry['source']}")
            elif target.get("formats"):
                problems.append(f"adapts 目标须是共用源 {key} → {entry['source']}")
            if headings is None:
                path = repo / source["path"]
                text = path.read_text(encoding="utf-8") if path.is_file() else ""
                headings = {line.lstrip("#").strip() for line in text.splitlines() if line.startswith("#")}
            if entry.get("section") and entry["section"] not in headings:
                problems.append(f"adapts 小节不存在 {key} #{entry['section']}")
    return problems


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--fix", action="store_true")
    parser.add_argument("--quiet", action="store_true", help="没有问题时不输出")
    args = parser.parse_args()
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    result = plan(data)
    if args.check:
        result = Plan(result.groups, result.numbers, result.problems + metadata_problems(data))
        for problem in result.problems:
            print(f"⚠ 工作流目录：{problem}")
        if result.problems:
            print("运行 python tools/workflow_catalog.py --fix 整理编号")
        elif not args.quiet:
            print(f"工作流目录：{len(result.groups)} 组 / {len(result.numbers)} 源，编号连续")
        return 1 if result.problems else 0
    if any(problem.startswith("未知组") for problem in result.problems):
        print("\n".join(result.problems))
        return 1
    data["groups"] = result.groups
    data["source_numbers"] = result.numbers
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="")
    print(f"已整理：{len(result.groups)} 组 / {len(result.numbers)} 源；变更 {len(result.problems)} 处")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
