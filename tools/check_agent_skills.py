"""Validate shared Kimi / Codex skills stored directly under .agents/skills."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
SOURCES = REPO / ".agents" / "skills"


def validate() -> list[str]:
    problems: list[str] = []
    paths = sorted(SOURCES.glob("*/SKILL.md"))
    if not paths:
        return [f"no skills found: {SOURCES}"]
    for path in paths:
        alias = path.parent.name
        text = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
        if match is None:
            problems.append(f"missing frontmatter: {alias}")
            continue
        meta = yaml.safe_load(match[1])
        if not isinstance(meta, dict):
            problems.append(f"invalid frontmatter: {alias}")
            continue
        if meta.get("name") != alias or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", alias):
            problems.append(f"skill name must match its kebab-case directory: {alias}")
        description = meta.get("description")
        if not isinstance(description, str) or not description.strip() or len(description) > 500 or "\n" in description:
            problems.append(f"description must be one line, 1..500 characters: {alias}")
        if meta.get("type", "prompt") not in {"prompt", "inline", "flow"}:
            problems.append(f"unsupported Kimi skill type: {alias}")
        if "claude" in (meta.get("metadata") or {}):
            problems.append(f"legacy Claude metadata remains: {alias}")
    return problems


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    problems = validate()
    for problem in problems:
        print(problem)
    if problems:
        return 1
    print(f"{len(list(SOURCES.glob('*/SKILL.md')))} shared Kimi / Codex skills checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
