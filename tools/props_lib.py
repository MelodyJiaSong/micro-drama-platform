# -*- coding: utf-8 -*-
"""本剧物件库 `props/` 的唯一定位与编号出处（2026-09-25，shengji_zhilu follow-up 013）。

物件只住一处：`{剧}/2_世界观人设/props/p{N}_{名}/`——剧情物件（p1–p14）与场景物件
（同一格式：三视图卡 + asset.toml + ref/ + 三视图 + `mesh/p{N}.glb`）共用一套编号。场景只引用 `p{N}`，不自带资产库。

编号唯一出处：`props/registry.toml`（`[[prop]] key / name_zh / kind = "story" | "scene_object" / from = [旧键]`）。
新物件一律 `allocate()` 领号，**不许手填**——手填会和剧情物件撞号（它们由 gen_props_szzl.py 按固定键写卡）。

不 import bpy：build_scene（跑在 Blender 里）与各命令行工具共用。
"""
from __future__ import annotations

import re
import tomllib
from pathlib import Path

KEY = re.compile(r"^p(\d+)$")
DIR = re.compile(r"^p(\d+)_(.+)$")
WORLD = "2_世界观人设"


def props_root(anywhere: Path | str) -> Path:
    """从剧里任意路径（bg 目录 / 区目录 / scenes 根 / props 本身）找到本剧的 props/。"""
    p = Path(anywhere).resolve()
    for q in [p, *p.parents]:
        if q.name == WORLD:
            return q / "props"
        if q.name == "props" and q.parent.name == WORLD:
            return q
    raise SystemExit(f"{anywhere} 不在任何 {WORLD}/ 之下，找不到 props/")


def registry_path(anywhere: Path | str) -> Path:
    return props_root(anywhere) / "registry.toml"


def registry(anywhere: Path | str) -> list[dict]:
    p = registry_path(anywhere)
    return tomllib.loads(p.read_text(encoding="utf-8")).get("prop", []) if p.is_file() else []


def find(anywhere: Path | str, key: str) -> Path | None:
    """p{N} → 它的目录；没有目录返回 None。目录名 `p{N}_{名}` 是判据，同号两个目录直接报错。"""
    root = props_root(anywhere)
    hits = [d for d in root.glob(f"{key}_*") if d.is_dir() and DIR.match(d.name) and d.name.split("_", 1)[0] == key]
    if len(hits) > 1:
        raise SystemExit(f"{key} 在 {root} 下有 {len(hits)} 个目录：{[h.name for h in hits]}")
    return hits[0] if hits else None


def scene_objects(anywhere: Path | str) -> list[Path]:
    """有 asset.toml 的 prop 目录 ＝ 走三视图流程的物件（场景物件 + 2026-09-25 起的剧情物件 p1–p14）。"""
    root = props_root(anywhere)
    return sorted((d for d in root.iterdir() if d.is_dir() and DIR.match(d.name) and (d / "asset.toml").is_file()),
                  key=lambda d: int(DIR.match(d.name).group(1)))


def _fmt(v) -> str:
    if isinstance(v, list):
        return "[" + ", ".join(_fmt(x) for x in v) + "]"
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'


def write_registry(anywhere: Path | str, rows: list[dict]) -> None:
    head = ("# 本剧物件编号唯一出处（tools/props_lib.py；follow-up 013）。新物件用 props_lib.allocate() 领号，不许手填。\n"
            "# kind: story ＝ 剧情物件（gen_props_szzl.py 写卡）；scene_object ＝ 场景物件（三视图 + GLB，场景用 blocks.toml 引用）。\n")
    body = []
    for r in sorted(rows, key=lambda r: int(KEY.match(r["key"]).group(1))):
        body.append("[[prop]]\n" + "".join(f"{k} = {_fmt(r[k])}\n" for k in ("key", "name_zh", "kind", "from") if k in r))
    text = head + "\n" + "\n".join(body)
    tomllib.loads(text)
    registry_path(anywhere).write_text(text, encoding="utf-8", newline="\n")


def allocate(anywhere: Path | str, name_zh: str, kind: str = "scene_object") -> str:
    """领下一个号并登记；返回 `p{N}`。"""
    rows = registry(anywhere)
    n = max([int(KEY.match(r["key"]).group(1)) for r in rows] + [0]) + 1
    rows.append({"key": f"p{n}", "name_zh": name_zh, "kind": kind})
    write_registry(anywhere, rows)
    return f"p{n}"


if __name__ == "__main__":      # python tools/props_lib.py new <剧里任意路径> <名> [story]
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 4 or sys.argv[1] != "new":
        raise SystemExit("用法：python tools/props_lib.py new <剧里任意路径> <名> [story]")
    print(allocate(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "scene_object"))
