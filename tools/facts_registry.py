# -*- coding: utf-8 -*-
"""史料事实注册表读取器（ai_video.md rule 17 · 格式契约 K34）。

事实的唯一出处是 `{片}/0_research/parts/*.md` 里 ```yaml 围栏中的 `- fact_id:` 列表；
dossier.md 只写综合与指针，任何合并 JSON 都是派生快照（rule 4i ①）。生成器直接 import 本模块读 parts。

用法（仓库根目录）：
    python tools/facts_registry.py ai_videos/shikong_lvxing/sk1               # 统计 + 机检
    python tools/facts_registry.py ai_videos/shikong_lvxing/sk1 --json OUT    # 另存一份 JSON 快照
"""
from __future__ import annotations

import argparse
import collections
import io
import json
import os
import re
import sys
from dataclasses import dataclass

TAGS: tuple[str, ...] = ("✅", "⚠️", "❌")
VERIFIED: tuple[str, ...] = ("human", "ai_read", "ai_draft")

_FENCE = re.compile(r"```yaml\n(.*?)\n```", re.S)
_KEY = re.compile(r"^  ([A-Za-z_]+):\s?(.*)$")
_ITEM = re.compile(r"^\s{4}-\s+(.*)$")
_CONT = re.compile(r"^\s{4}(\S.*)$")


@dataclass(frozen=True)
class Problem:
    level: str
    fact_id: str
    detail: str


def _scalar(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    return v


def _inline_list(v: str) -> list[str]:
    body = v.strip()[1:-1].strip()
    return [_scalar(x) for x in body.split(",")] if body else []


def parse_block(text: str, part: str) -> list[dict]:
    facts: list[dict] = []
    cur: dict | None = None
    last: str | None = None
    block_scalar = False
    for line in text.split("\n"):
        if line.startswith("- fact_id:"):
            cur = {"fact_id": _scalar(line.split(":", 1)[1]), "part": part}
            facts.append(cur)
            last, block_scalar = None, False
            continue
        if cur is None:
            continue
        m = _KEY.match(line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            block_scalar = False
            if val == "":
                cur[key], last = [], key
            elif val in ("|", ">", "|-", ">-"):
                cur[key], last, block_scalar = "", key, True
            elif val.startswith("[") and val.endswith("]"):
                cur[key], last = _inline_list(val), None
            else:
                cur[key], last = _scalar(val), key
            continue
        if last is None:
            continue
        item = _ITEM.match(line)
        if item and isinstance(cur.get(last), list):
            cur[last].append(_scalar(item.group(1)))
            continue
        cont = _CONT.match(line)
        if cont and block_scalar:
            cur[last] = (cur[last] + "\n" + cont.group(1)).lstrip("\n")
    return facts


def load(drama_dir: str) -> tuple[dict[str, dict], list[Problem]]:
    parts_dir = os.path.join(drama_dir, "0_research", "parts")
    out: dict[str, dict] = {}
    problems: list[Problem] = []
    for name in sorted(os.listdir(parts_dir)):
        if not name.endswith(".md"):
            continue
        text = io.open(os.path.join(parts_dir, name), encoding="utf-8").read()
        for block in _FENCE.findall(text):
            for f in parse_block(block, name):
                fid = f["fact_id"]
                if fid in out:
                    problems.append(Problem("blocker", fid, "重复 fact_id：%s 与 %s" % (out[fid]["part"], name)))
                    continue
                out[fid] = f
    for fid, f in out.items():
        if f.get("tag") not in TAGS:
            problems.append(Problem("blocker", fid, "tag 非法：%r" % f.get("tag")))
        if f.get("verified_by") not in VERIFIED:
            problems.append(Problem("blocker", fid, "verified_by 非法：%r" % f.get("verified_by")))
        if f.get("verified_by") == "ai_read" and (not f.get("quote") or not f.get("source_url")):
            problems.append(Problem("warning", fid, "ai_read 缺 quote 或 source_url"))
        if f.get("tag") in ("✅", "⚠️") and not f.get("negative"):
            problems.append(Problem("info", fid, "negative 为空（由本站黑名单兜底，K-F5）"))
    return out, problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("drama_dir")
    ap.add_argument("--json", dest="json_out")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    facts, problems = load(args.drama_dir)
    by_part = collections.Counter(f["part"] for f in facts.values())
    by_tag = collections.Counter(f.get("tag") for f in facts.values())
    by_ver = collections.Counter(f.get("verified_by") for f in facts.values())
    by_prefix = collections.Counter(re.sub(r"\.\d+$", "", fid) for fid in facts)
    print("facts: %d" % len(facts))
    print("by part:", dict(sorted(by_part.items())))
    print("by tag:", dict(by_tag))
    print("by verified_by:", dict(by_ver))
    print("by prefix:", dict(sorted(by_prefix.items())))
    counts = collections.Counter(p.level for p in problems)
    for p in problems:
        if p.level != "info":
            print("  %s %s %s" % ("❌" if p.level == "blocker" else "⚠️", p.fact_id, p.detail))
    print("problems:", dict(counts))
    if args.json_out:
        io.open(args.json_out, "w", encoding="utf-8").write(json.dumps(list(facts.values()), ensure_ascii=False, indent=1))
        print("wrote", args.json_out)
    return 1 if counts.get("blocker") else 0


if __name__ == "__main__":
    raise SystemExit(main())
