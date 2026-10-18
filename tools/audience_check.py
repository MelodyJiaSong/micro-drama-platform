"""交稿前自检：观众原则与全剧 Vision 有没有写下来（只查有没有写，不评判好坏）。

代理把草稿交给用户确定之前运行；缺项先补齐再交。用户仍可带着缺项确定。
格式见 .agents/skills/ai-videos-pipeline/modules/decisions.md「交稿前自检」。

    python tools/audience_check.py <剧目录> [epNN] [--module story|filming|render]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MODULES = ("story", "filming", "render")
# 出片审核的 Vision 项从这天起要求，之前的条不追溯（follow-up 249）。
RENDER_CUTOFF = "20261012"
VISION_HEADING = "## Vision（观众体验）"


def _section(text: str, heading: str) -> str | None:
    """Body of a `## heading` section up to the next heading of the same or higher level."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == heading:
            body = []
            for nxt in lines[i + 1:]:
                if re.match(r"^#{1,2} ", nxt):
                    break
                body.append(nxt)
            return "\n".join(body)
    return None


def _table(body: str) -> tuple[list[str], list[list[str]]]:
    rows = [l.strip() for l in body.splitlines() if l.strip().startswith("|")]
    cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
    if len(cells) < 2:
        return [], []
    data = [r for r in cells[2:] if not all(re.fullmatch(r":?-+:?", c) for c in r)]
    return cells[0], data


def _line_value(text: str, label: str) -> str:
    m = re.search(rf"^[ \t]*(?:[-*][ \t]*)?\**{label}\**[:：]\**[ \t]*(.*)$", text, re.M)
    return m.group(1).strip() if m else ""


def check_readme(drama: Path) -> list[str]:
    readme = drama / "README.md"
    if not readme.is_file():
        return [f"{readme}: 缺 README"]
    body = _section(readme.read_text(encoding="utf-8"), VISION_HEADING)
    if body is None:
        return [f"{readme}: 缺「{VISION_HEADING}」"]
    quotes = [l for l in body.splitlines() if l.startswith(">") and l.strip("> *")]
    out = []
    if len(quotes) != 1:
        out.append(f"{readme}: Vision 应是一句话（一行引用），现在 {len(quotes)} 行")
    if not _line_value(body, "核心"):
        out.append(f"{readme}: Vision 一节缺「核心：」行")
    return out


def _table_issues(path: Path, text: str, heading: str, need: tuple[str, ...]) -> list[str]:
    body = _section(text, heading)
    if body is None:
        return [f"{path}: 缺「{heading}」"]
    head, rows = _table(body)
    cols = [next((i for i, h in enumerate(head) if key in h), None) for key in need]
    if not rows or None in cols:
        return [f"{path}: 「{heading}」要有表格，列含 {'、'.join(need)}"]
    out = []
    for row in rows:
        empty = [need[k] for k, i in enumerate(cols) if i >= len(row) or not row[i]]
        if empty:
            out.append(f"{path}: 「{heading}」第「{row[0]}」行缺 {'、'.join(empty)}")
    return out


def check_story(ep: Path) -> list[str]:
    path = ep / "decisions" / "story.md"
    if not path.is_file():
        return [f"{path}: 缺集级故事决策记录"]
    text = path.read_text(encoding="utf-8")
    out = [f"{path}: 缺「{k}：」行" for k in ("本集体验", "Vision") if not _line_value(text, k)]
    out += _table_issues(path, text, "## 体验地图", ("段", "体验", "事件"))
    out += _table_issues(path, text, "## 观众轨", ("段", "知道", "在等", "处理"))
    out += _table_issues(path, text, "## 目标影响", ("事件", "影响"))
    out += _table_issues(path, text, "## 台词逐句", ("对谁", "台词", "为什么", "新信息"))
    out += _table_issues(path, text, "## 站位与视线", ("场", "谁", "在哪", "看得见"))
    return out


def check_episode_length(ep: Path) -> list[str]:
    """剧 workflow.json 的 episode_seconds（[下限, 上限] 秒）是硬规则：分镜总时长不得越界。"""
    wf, filming = ep.parent.parent / "workflow.json", ep / "filming.json"
    if not wf.is_file() or not filming.is_file():
        return []
    limits = json.loads(wf.read_text(encoding="utf-8")).get("episode_seconds")
    if limits is None:
        return []
    if not (isinstance(limits, list) and len(limits) == 2 and 0 < limits[0] <= limits[1]):
        raise ValueError(f"{wf}: episode_seconds 应是 [下限, 上限] 秒，现在是 {limits!r}")
    scenes = json.loads(filming.read_text(encoding="utf-8"))["content"]["scenes"]
    total = sum(shot.get("duration", 0) for scene in scenes for shot in scene["shots"])
    if limits[0] <= total <= limits[1]:
        return []
    return [f"{filming}: 分镜总时长 {total} 秒，超出本剧每集 {limits[0]}–{limits[1]} 秒的硬规则"]


def check_filming(ep: Path) -> list[str]:
    out = check_episode_length(ep)
    path = ep / "decisions" / "filming.md"
    if not path.is_file():
        out.append(f"{path}: 缺集级影视改编决策记录")
    elif not _line_value(path.read_text(encoding="utf-8"), "Vision"):
        out.append(f"{path}: 缺「Vision：」行")
    for scene in sorted((ep / "scenes").glob("s*/")):
        path = scene / "decisions.md"
        if not path.is_file():
            out.append(f"{path}: 缺场级决策记录")
            continue
        text = path.read_text(encoding="utf-8")
        if not _line_value(text, "Vision"):
            out.append(f"{path}: 缺「Vision：」行")
        body = _section(text, "## 观众")
        if body is None or not body.strip():
            out.append(f"{path}: 缺「## 观众」或内容为空")
    return out


def check_render(ep: Path) -> list[str]:
    out = []
    for review in sorted(ep.glob("scenes/s*/shots/st*/renders/*/review.md")):
        if review.parent.name[:8] < RENDER_CUTOFF:
            continue
        if not _line_value(review.read_text(encoding="utf-8"), "Vision"):
            out.append(f"{review}: 缺「Vision：」项")
    return out


def run(drama: Path, episode: str | None = None, module: str | None = None) -> list[str]:
    issues = check_readme(drama)
    eps = [drama / "episodes" / episode] if episode else sorted((drama / "episodes").glob("ep*/"))
    checks = {"story": check_story, "filming": check_filming, "render": check_render}
    for ep in eps:
        for name in ([module] if module else MODULES):
            issues += checks[name](ep)
    return issues


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("drama", type=Path)
    ap.add_argument("episode", nargs="?")
    ap.add_argument("--module", choices=MODULES)
    a = ap.parse_args(argv)
    issues = run(a.drama, a.episode, a.module)
    for line in issues:
        print(f"缺：{line}")
    print(f"交稿前自检：{len(issues)} 项缺失" if issues else "交稿前自检：齐全")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
