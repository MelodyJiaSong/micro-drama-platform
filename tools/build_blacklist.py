# -*- coding: utf-8 -*-
"""误传黑名单合并器 —— 20 路调研各自的黑名单 → 全剧唯一的负向词库。

用法（仓库根目录）：
    python tools/build_blacklist.py ai_videos/shengji_zhilu

产物（写在 {drama}/0_research/ 下）：
    blacklist.md        合并表，保留每行的来源路与 fact 指针
    negatives.txt       去重后的负向词集合，一行一条，给生成器直接读

设计依据
--------
· **黑名单行的唯一出处是各路 part 的「误传黑名单」节**（rule 4i ①）。本文件是**派生快照**，
  手改无效——改黑名单 ＝ 改 part 重跑。
· 生成模型的默认输出本身就是误传的浓缩；`负向词` 一列是它的解药，
  直接进 shot prompt 的 `负面词:` 与 `style_guide.md § 负向锁定`。
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys
from dataclasses import dataclass

# 标题可带编号（「## 10. 误传黑名单」）：只认不带编号的写法时，w02 的整节从未进库（w23 查出，2026-09-26）
SECTION = re.compile(r"\n##+ *(?:\d+\.\s*)?误传黑名单[^\n]*\n(.*?)(?=\n## [^#]|\Z)", re.S)
ROW = re.compile(r"^\|\s*(?!#\s*\|)(?!-)(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$")
NEG_TOKEN = re.compile(r"[、,，;；]")
BACKTICKED = re.compile(r"`([^`]+)`")


@dataclass(frozen=True)
class Row:
    part: str
    myth: str
    truth: str
    negatives: str
    source: str


def harvest(parts_dir: str) -> list[Row]:
    rows: list[Row] = []
    for name in sorted(os.listdir(parts_dir)):
        if not name.endswith(".md"):
            continue
        text = io.open(os.path.join(parts_dir, name), encoding="utf-8").read()
        for body in SECTION.findall(text):
            for line in body.split("\n"):
                m = ROW.match(line.strip())
                if not m:
                    continue
                cells = [c.strip() for c in m.groups()]
                if set("".join(cells)) <= set("-: "):
                    continue
                if cells[1].startswith("误传") or cells[0] in ("#", "序"):
                    continue
                rows.append(Row(name, cells[1], cells[2], cells[3], cells[4]))
    return rows


def negatives(rows: list[Row]) -> list[str]:
    seen: dict[str, None] = {}
    for r in rows:
        chunks = BACKTICKED.findall(r.negatives) or [r.negatives]
        for chunk in chunks:
            for token in NEG_TOKEN.split(chunk):
                t = token.strip().strip("`*").strip()
                if 1 < len(t) <= 40 and not t.startswith("http"):
                    seen.setdefault(t, None)
    return list(seen)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("drama")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    research = os.path.join(args.drama, "0_research")
    rows = harvest(os.path.join(research, "parts"))
    negs = negatives(rows)

    by_part: dict[str, list[Row]] = {}
    for r in rows:
        by_part.setdefault(r.part, []).append(r)

    out: list[str] = [
        "# 误传黑名单 · 全剧负向词库",
        "",
        "> **本文件由 `tools/build_blacklist.py` 生成，不要手改。** 每行的唯一出处是 `parts/*.md` 的「误传黑名单」节；",
        "> 改黑名单 ＝ 改对应 part 重跑。",
        "",
        f"> 合计 **{len(rows)}** 行，去重后 **{len(negs)}** 条负向词（见同目录 `negatives.txt`）。",
        "> **生成模型的默认输出本身就是误传的浓缩**——这张表是它的解药。",
        "> `负向词` 一列直接进 shot prompt 的 `负面词:` 与 `style_guide.md § 负向锁定`。",
        "",
    ]
    for part in sorted(by_part):
        out += [f"## {part}（{len(by_part[part])} 行）", "", "| 误传（模型/攻略的默认输出） | 1.12 口径的正解 | 负向词 | 出处 |", "|---|---|---|---|"]
        for r in by_part[part]:
            out.append(f"| {r.myth} | {r.truth} | {r.negatives} | {r.source} |")
        out.append("")

    io.open(os.path.join(research, "blacklist.md"), "w", encoding="utf-8", newline="\n").write("\n".join(out))
    io.open(os.path.join(research, "negatives.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(negs) + "\n")
    print(f"黑名单 {len(rows)} 行（{len(by_part)} 路）→ {research}/blacklist.md")
    print(f"负向词 {len(negs)} 条 → {research}/negatives.txt")
    for part in sorted(by_part):
        print(f"  {part:36} {len(by_part[part]):>3} 行")
    missing = [n for n in sorted(os.listdir(os.path.join(research, "parts"))) if n.endswith(".md") and n not in by_part]
    if missing:
        print("\n没有黑名单节的路（可能是纯事实路，也可能是漏写）：")
        for n in missing:
            print("  ", n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
