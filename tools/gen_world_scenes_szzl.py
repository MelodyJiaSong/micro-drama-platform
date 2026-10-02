# -*- coding: utf-8 -*-
"""《圣光刚好够用》全图 scene 骨架生成器 —— 世界树 → `scenes/{大陆}/{区}/bg{N}_{主体}/`。

用法（仓库根目录）：
    python tools/gen_world_scenes_szzl.py            # 建/刷新骨架（幂等）
    python tools/gen_world_scenes_szzl.py --check    # 只报告，不写盘
    python tools/gen_world_scenes_szzl.py --plans    # 骨架 + 重出所有区级 floor plan PNG

输入（都是单一出处，本脚本一个地名、一个坐标都不手写）：
    0_research/map/world_tree.json          地理树（由 build_world_tree.py 从片区 YAML 生成）
    0_research/map/zone_extents.toml        每区世界地图尺寸（码），来源与置信度各一列
    0_research/map/refs/                    原版区图（fetch_wow_maps.py 抓的，图只进人眼）
    2_世界观人设/scenes/registry.toml       bg 编号登记簿（本脚本追加、永不改号）

产物：
    scenes/{大陆}/{大陆}.md                          大陆卡（索引）
    scenes/{大陆}/ref/*.link.json                    指向大陆图
    scenes/{大陆}/{区}/{区}.md                       区卡（索引 + bg 清单 + 未立 bg 的地标）—— **每次重生成**
    scenes/{大陆}/{区}/ref/*.link.json               指向该区原版区图（rule 4b-B：不拷贝、不软链）
    scenes/{大陆}/{区}/bg{N}_{区名}全境/             区级主体：拥有区级 floor plan
        planning/blocks.toml                         **生成**（块＝世界树里有坐标的 bg；地形由 terrain.toml 合并）
        planning/terrain.toml                        作者写：ridge / water / road（+ 可选的 block 覆盖）
    scenes/{大陆}/{区}/bg{N}_{主体}/                 每个聚居点 / 野外子区域 / 城区一个
        {dir}.md                                     只在不存在时写骨架（作者把〔作者填写〕处补完）
        planning/blocks.toml                         只在不存在时写骨架（作者补 block / ridge / water / road）
        ref/{区图}.link.json + ref/{dir}_map_crop.png 原版区图指针 + 本点位裁切图（有坐标才有）
    scenes/scenes_index.md                           全图索引（派生）

选 bg 的判据（用户 2026-09-22 拍板：区 = scene，聚居点 + 野外子区域 = bg）：
    · settlement：全收；`inn` 只在直接挂区上时收（城里的旅店是室内，归城区）
    · subzone：直接挂区上的收；嵌套的只在有坐标时收（无坐标的嵌套子区域 = 父主体的一部分，如修道院里的主厅）
    · district：主城城区全收
    · 祖先里有 dungeon / raid / battleground 的一律不收；poi / transport 不立 bg（列进区卡「地标」）
    · 登记簿里手工登记的节点（bg1–bg22）无条件收
"""
from __future__ import annotations

import argparse
import collections
import io
import json
import math
import os
import re
import subprocess
import sys
import tomllib

sys.stdout.reconfigure(encoding="utf-8")

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DRAMA = os.path.join(REPO, "ai_videos", "shengji_zhilu")
TREE = os.path.join(DRAMA, "0_research", "map", "world_tree.json")
EXTENTS = os.path.join(DRAMA, "0_research", "map", "zone_extents.toml")
REFS = os.path.join(DRAMA, "0_research", "map", "refs")
SCENES = os.path.join(DRAMA, "2_世界观人设", "scenes")
REGISTRY = os.path.join(SCENES, "registry.toml")
WORLD_ANCHOR = "scenes/eastern_kingdoms/elwynn_forest/bg1_北郡山谷/bg1_北郡山谷.png"

YD = 0.9144
CONTINENTS = ("eastern_kingdoms", "kalimdor")
CONT_ZH = {"eastern_kingdoms": "东部王国", "kalimdor": "卡利姆多"}
TYPE_ZH = {"settlement": "聚居点", "subzone": "子区域", "district": "城区", "zone": "地区", "city": "主城", "poi": "地标"}
FILL = "〔作者填写〕"

# 区级平面图上，一个 bg 方块的默认边长（m）与体块高（m）。只是示意尺寸——真尺寸在各 bg 自己的图里。
SIZE_M: dict[str, float] = {"capital": 600, "town": 220, "village": 160, "camp": 100, "farm": 140, "ruin": 180,
                            "tower": 60, "port": 200, "mine": 80, "crossroads": 60, "inn": 40,
                            "settlement": 120, "subzone": 320, "district": 160, "zone": 400, "poi": 40}
H_M: dict[str, float] = {"capital": 20, "town": 8, "village": 6, "camp": 3, "farm": 5, "ruin": 5, "tower": 15,
                         "port": 6, "mine": 5, "crossroads": 0, "inn": 6, "settlement": 6, "subzone": 0,
                         "district": 10, "zone": 0, "poi": 3}
# bg 自己的图：默认场地边长（m）。作者可改 size_m。
BG_SIZE_M: dict[str, float] = {"capital": 800, "town": 260, "village": 200, "camp": 140, "farm": 180, "ruin": 220,
                               "tower": 90, "port": 240, "mine": 120, "crossroads": 100, "inn": 60,
                               "settlement": 160, "subzone": 320, "district": 220, "zone": 300, "poi": 80}


def q(s: str) -> str:
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


def parse_coords(s: str) -> tuple[float, float] | None:
    m = re.match(r"\s*\[\s*([0-9.]+)\s*,\s*([0-9.]+)\s*\]", s or "")
    return (float(m.group(1)), float(m.group(2))) if m else None


def safe_name(zh: str, en: str) -> str:
    """bg 目录名的主体段：优先官方简中，查不到留英文原名（仓库规则：绝不自己音译）。不含 `_`。"""
    s = (zh or "").strip() or (en or "").strip()
    s = s.replace("_", "").replace("/", "").replace("\\", "").replace(":", "").replace("*", "").replace("?", "")
    s = s.replace('"', "").replace("<", "").replace(">", "").replace("|", "").replace("'", "")
    s = re.sub(r"\s+", "-", s)
    return s or "unnamed"


def compact(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


class World:
    def __init__(self) -> None:
        raw = json.load(io.open(TREE, encoding="utf-8"))
        self.n: dict[str, dict] = {x["id"]: x for x in raw["nodes"]}
        self.order: dict[str, int] = {x["id"]: i for i, x in enumerate(raw["nodes"])}
        self.kids: dict[str, list[str]] = collections.defaultdict(list)
        for x in raw["nodes"]:
            self.kids[x.get("parent")].append(x["id"])

    def chain(self, nid: str) -> list[str]:
        out, cur = [], nid
        while cur:
            out.append(cur)
            cur = self.n.get(cur, {}).get("parent")
        return list(reversed(out))

    def continent(self, nid: str) -> str | None:
        for a in self.chain(nid):
            if self.n[a]["type"] == "continent":
                return a
        return None

    def zone_of(self, nid: str) -> str | None:
        """节点归哪个 scene（zone/city）。北郡山谷折进艾尔文；嵌套主城（铁炉堡挂丹莫罗）归自己。"""
        ch = self.chain(nid)
        for a in reversed(ch[:-1] if self.n[nid]["type"] in ("zone", "city") else ch):
            if a == "northshire_valley":
                continue
            if self.n[a]["type"] in ("zone", "city"):
                return a
        return None

    def scenes(self) -> list[dict]:
        out = []
        for x in self.n.values():
            if x["type"] in ("zone", "city") and x["id"] != "northshire_valley" and self.continent(x["id"]) in CONTINENTS:
                out.append(x)
        out.sort(key=lambda z: (CONTINENTS.index(self.continent(z["id"])), z["id"]))
        return out

    def descendants(self, zid: str) -> list[str]:
        out, stack = [], list(self.kids[zid])
        while stack:
            c = stack.pop(0)
            if self.n[c]["type"] in ("zone", "city") and c != "northshire_valley":
                continue
            out.append(c)
            stack.extend(self.kids[c])
        return out

    def refs_dir(self, zid: str) -> str:
        parts = [p for p in self.chain(zid) if self.n[p]["type"] in ("continent", "region", "zone", "city")]
        return os.path.join(REFS, *parts)


# ── 登记簿 ──────────────────────────────────────────────────────────────
def load_registry() -> tuple[dict, list[dict]]:
    with open(REGISTRY, "rb") as f:
        r = tomllib.load(f)
    return r["meta"], list(r.get("bg", []))


def save_registry(meta: dict, rows: list[dict]) -> None:
    head = io.open(REGISTRY, encoding="utf-8").read().split("[meta]")[0].rstrip("\n")
    lines = [head, "", "[meta]", f"drama = {q(meta['drama'])}", f"next = {meta['next']}", ""]
    for r in sorted(rows, key=lambda x: x["n"]):
        lines += ["[[bg]]", f"n = {r['n']}", f"node = {q(r.get('node', ''))}", f"dir = {q(r['dir'])}",
                  f"zone = {q(r['zone'])}", f"continent = {q(r['continent'])}"]
        if r.get("note"):
            lines.append(f"note = {q(r['note'])}")
        if r.get("kind"):
            lines.append(f"kind = {q(r['kind'])}")
        lines.append("")
    io.open(REGISTRY, "w", encoding="utf-8", newline="\n").write("\n".join(lines))


# ── 选 bg ────────────────────────────────────────────────────────────────
def select_nodes(w: World, zid: str, forced: set[str]) -> list[str]:
    out = []
    for nid in w.descendants(zid):
        n = w.n[nid]
        if nid in forced:
            out.append(nid)
            continue
        ch = w.chain(nid)
        anc = [w.n[a]["type"] for a in ch[ch.index(zid) + 1:-1]] if zid in ch else [w.n[a]["type"] for a in ch[:-1]]
        # 只看「区 → 节点」之间的祖先：暗炉城本身挂在黑石深渊（副本）下面，城里的城区不能因此被当成副本内部
        if any(t in ("dungeon", "raid", "battleground") for t in anc):
            continue
        if (n.get("era") or "vanilla") != "vanilla":      # 4.0.3a / TBC / WotLK 才有的地点不进 1.12 的 scene
            continue
        t = n["type"]
        if t == "settlement":
            if n.get("subtype") == "inn" and n.get("parent") != zid:
                continue
            out.append(nid)
        elif t == "subzone":
            if "district" in anc:
                continue
            if n.get("parent") in (zid, "northshire_valley") or parse_coords(n.get("coords", "")):
                out.append(nid)
        elif t == "district":
            out.append(nid)
    order = {"settlement": 0, "subzone": 1, "district": 2, "zone": 0, "poi": 1}
    out.sort(key=lambda i: (order.get(w.n[i]["type"], 9), w.order[i]))
    return out


# ── 尺寸 ────────────────────────────────────────────────────────────────
def load_extents() -> dict:
    if not os.path.isfile(EXTENTS):
        return {}
    with open(EXTENTS, "rb") as f:
        return tomllib.load(f)


def zone_size_m(ext: dict, zid: str) -> tuple[float, float, str, str]:
    e = ext.get(zid)
    if not e:
        return 3000.0, 2000.0, "推定", "zone_extents.toml 里没有本区条目，按 3:2 标准区图取 3000×2000 m 占位"
    w, h = float(e["w_yd"]) * YD, float(e["h_yd"]) * YD
    src = "坐标表" if e.get("confidence") == "source" else "推定"
    note = ("WorldMapArea：%.1f × %.1f 码 × 0.9144（%s）" % (e["w_yd"], e["h_yd"], e.get("source_url", ""))
            if src == "坐标表" else
            "WorldMapArea 尺寸未取到一手出处，%.0f × %.0f 码为估计值（%s）" % (e["w_yd"], e["h_yd"], e.get("note", "")))
    return round(w, 1), round(h, 1), src, note


# ── 文件产出 ───────────────────────────────────────────────────────────
def write(path: str, text: str, dry: bool, only_if_missing: bool = False) -> bool:
    if only_if_missing and os.path.exists(path):
        return False
    if os.path.exists(path) and io.open(path, encoding="utf-8").read() == text:
        return False
    if not dry:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        io.open(path, "w", encoding="utf-8", newline="\n").write(text)
    return True


def link_json(path: str, target_abs: str, note: str, dry: bool) -> bool:
    rel = os.path.relpath(target_abs, REPO).replace(os.sep, "/")
    return write(path, json.dumps({"target": rel, "note": note}, ensure_ascii=False, indent=2) + "\n", dry)


def zone_maps(w: World, zid: str) -> tuple[str | None, list[str]]:
    d = w.refs_dir(zid)
    if not os.path.isdir(d):
        return None, []
    files = sorted(f for f in os.listdir(d) if f.lower().endswith((".jpg", ".png")))
    if not files:
        return None, []
    files.sort(key=lambda f: (0 if "c60" in f else 1 if "vanilla" in f.lower() else 2, f))
    md = os.path.join(d, "microdungeons")
    micro = sorted(os.path.join(md, f) for f in os.listdir(md)) if os.path.isdir(md) else []
    best = os.path.join(d, files[0])
    if "c60" not in files[0] and "vanilla" not in files[0].lower():
        # 本区只有后期版图（藏宝海湾只有大灾变后的荆棘谷总图）：1.12 里它显示的就是上级区的地图，用上级区的 c60
        up = os.path.dirname(d)
        c60 = sorted(f for f in os.listdir(up) if "c60" in f and f.lower().endswith((".jpg", ".png"))) if os.path.isdir(up) else []
        if c60:
            best = os.path.join(up, c60[0])
    return best, micro


def crop(map_path: str, xy: tuple[float, float], out: str, dry: bool) -> bool:
    if dry:
        return not os.path.exists(out)
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return False
    try:
        im = Image.open(map_path).convert("RGB")
    except OSError:
        return False
    W, H = im.size
    fx, fy = 0.09, 0.09
    cx, cy = xy[0] / 100.0 * W, xy[1] / 100.0 * H
    x0, y0 = max(0, int(cx - fx * W)), max(0, int(cy - fy * H))
    x1, y1 = min(W, int(cx + fx * W)), min(H, int(cy + fy * H))
    c = im.crop((x0, y0, x1, y1))
    scale = max(1, int(720 / max(1, c.size[0])))
    c = c.resize((c.size[0] * scale, c.size[1] * scale), Image.LANCZOS)
    d = ImageDraw.Draw(c)
    px, py = (cx - x0) * scale, (cy - y0) * scale
    d.line([(px - 18, py), (px + 18, py)], fill=(255, 40, 40), width=3)
    d.line([(px, py - 18), (px, py + 18)], fill=(255, 40, 40), width=3)
    d.ellipse([px - 8, py - 8, px + 8, py + 8], outline=(255, 40, 40), width=2)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    c.save(out)
    return True


def zone_blocks_toml(w: World, ext: dict, z: dict, bgs: list[dict], reg_dir: str, terrain: dict) -> str:
    zid = z["id"]
    Wm, Hm, src, note = zone_size_m(ext, zid)
    px = round(min(3.0, 2200.0 / max(Wm, Hm)), 3)
    kind = "全城" if z["type"] == "city" else "全境"
    L = [f"# {z['name_zh']}（{z['name_en']}）· 区级场地平面图 —— **本文件由 tools/gen_world_scenes_szzl.py 生成，不要手改**",
         "#", "# 块 ＝ 世界树里有坐标的 bg（坐标百分比 × 本区 WorldMapArea 尺寸），`bg` 键指向同级主体目录。",
         "# 山脊 / 水系 / 道路（以及要覆盖的块）请写在同目录 `terrain.toml`（作者拥有），本脚本重跑时合并进来。",
         f"# 换算：x% → x × {Wm / 100:.3f} m（东西）；y% → y × {Hm / 100:.3f} m（南北）；原点在区图左上角。",
         "", "[meta]", f"bg = {q(reg_dir.split('_', 1)[0])}", f"name_zh = {q(z['name_zh'] + kind)}",
         f"size_m = [{Wm:g}, {Hm:g}]", f"px_per_m = {px}", f"scale_src = {q(src)}", f"scale_note = {q(note)}",
         'label_mode = "number"', "grid_m = 200", f"generated_by = {q('tools/gen_world_scenes_szzl.py')}",
         f"zone = {q(zid)}"]
    absent = terrain.get("meta", {}).get("absent")
    if absent:
        L.append("absent = [" + ", ".join(q(a) for a in absent) + "]")
    L.append("")
    for sec in ("ridge", "water", "road"):
        for item in terrain.get(sec, []):
            L.append(f"[[{sec}]]")
            for k, v in item.items():
                L.append(f"{k} = {toml_val(v)}")
            L.append("")
    overrides = {(b.get("bg") or ""): b for b in terrain.get("block", []) if b.get("bg")}
    extra = [b for b in terrain.get("block", []) if not b.get("bg")]
    for b in bgs:
        key = b["dir"].split("_", 1)[0]
        if key in overrides:
            continue
        node = w.n.get(b.get("node") or "")
        if not node:
            continue
        c = parse_coords(node.get("coords", ""))
        if not c:
            continue
        st = node.get("subtype") or node["type"]
        s = SIZE_M.get(st, SIZE_M.get(node["type"], 100))
        s = min(s, Wm * 0.9, Hm * 0.9)
        x = min(max(c[0] / 100.0 * Wm, s / 2), Wm - s / 2)
        y = min(max(c[1] / 100.0 * Hm, s / 2), Hm - s / 2)
        # 块名取登记簿目录名（区内唯一）；世界树 name_zh 可以同名（提瑞斯法有三座「十字军前哨」）
        L += ["[[block]]", f"id = {q('b%03d' % b['n'])}", f"name = {q(b['dir'].split('_', 1)[1])}", f"bg = {q(key)}",
              f"xy = [{x:.1f}, {y:.1f}]", f"size = [{s:g}, {s:g}]", f"h_m = {H_M.get(st, H_M.get(node['type'], 0)):g}",
              "rot = 0", 'src = "坐标表"', f"note = {q(TYPE_ZH.get(node['type'], node['type']) + ((' · ' + node['subtype']) if node.get('subtype') else '') + ' · 坐标 ' + node['coords'])}", ""]
    for b in list(overrides.values()) + extra:
        L.append("[[block]]")
        for k, v in b.items():
            L.append(f"{k} = {toml_val(v)}")
        L.append("")
    return "\n".join(L)


def toml_val(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return f"{v:g}"
    if isinstance(v, str):
        return q(v)
    if isinstance(v, list):
        return "[" + ", ".join(toml_val(x) for x in v) + "]"
    raise TypeError(type(v))


def bg_blocks_skeleton(b: dict, node: dict | None, z: dict) -> str:
    st = (node.get("subtype") if node else "") or (node["type"] if node else "subzone")
    s = BG_SIZE_M.get(st, BG_SIZE_M.get(node["type"] if node else "subzone", 200))
    px = round(min(4.0, 1400.0 / s), 2)
    key = b["dir"].split("_", 1)[0]
    look = (node or {}).get("look_zh", "")
    return "\n".join([
        f"# {b['name']} · 场地平面图的几何唯一出处（rule 4k）。改布局 ＝ 改本文件重跑",
        f"#   python tools/build_floorplan.py \"<本目录>\"",
        "# 作者填：[[block]]（有 id / name / xy / size / h_m / src）、[[ridge]] / [[water]] / [[road]]；零个 block 合法（自然场景）。",
        "# src 只许 原典方位 / 坐标表 / 地图量取 / 推定；推定的画虚线。坐标原点在场地左上角，x 向东、y 向南，单位 m。",
        "", "[meta]", f"bg = {q(key)}", f"name_zh = {q(b['name'])}", f"size_m = [{s:g}, {s:g}]",
        f"px_per_m = {px}", 'scale_src = "推定"',
        f"scale_note = {q('场地边长按主体类型（' + st + '）取默认 ' + f'{s:g}' + ' m，无一手尺寸出处；作者按区图裁切与原典描述校正')}",
        f"# 世界树画面：{look}" if look else "# 世界树无画面描述",
        "absent = []", "",
    ])


def bg_md_skeleton(w: World, b: dict, node: dict | None, z: dict, cont: str, map_file: str | None, has_crop: bool,
                   micro_links: list[str]) -> str:
    d = b["dir"]
    key = d.split("_", 1)[0]
    c = parse_coords((node or {}).get("coords", ""))
    t_zh = TYPE_ZH.get((node or {}).get("type", ""), "剧本自造地点")
    st = (node or {}).get("subtype") or ""
    src = (node or {}).get("source_url") or "—"
    ref_lines = []
    if map_file:
        ref_lines.append(f"`ref/{os.path.basename(map_file)}.link.json` → 原版区图（{os.path.basename(map_file)}）")
    if has_crop:
        ref_lines.append(f"`ref/{d}_map_crop.png` → 本点位在区图上的裁切（坐标 {node['coords']}，红十字＝中心）")
    for m in micro_links:
        ref_lines.append(f"`ref/{os.path.basename(m)}.link.json` → 微型地下城图（{os.path.basename(m)}）")
    if not ref_lines:
        ref_lines.append("（世界树无坐标，暂无裁切图；原版区图见上级区目录 `ref/`）")
    parent = w.n.get((node or {}).get("parent", ""), {})
    facts = [
        f"- **世界树节点**：`{node['id']}`（{t_zh}{(' · ' + st) if st else ''}）· 上级 `{node.get('parent', '')}`（{parent.get('name_zh', '')}）" if node
        else "- **世界树节点**：无（剧本自造地点，见 registry.toml 的 note）",
        f"- **坐标**：{node['coords']}（区图百分比）" if c else "- **坐标**：世界树未记录（待核：wiki `{{Coords}}` 或实机量取）",
    ]
    if node:     # 无节点（区级主体 / 自造地点）时这三行只会是「无」，区级主体的调用方另补区的画面与出处
        facts += [
            f"- **世界树画面**：{node['look_zh']}" if node.get("look_zh") else "- **世界树画面**：无",
            f"- **世界树备注**：{node['note_zh']}" if node.get("note_zh") else "- **世界树备注**：无",
            f"- **出处**：{src}（`verified_by: {node.get('verified_by', '')}`）",
        ]
    return f"""# {b['name']}

> **档级：锚点级**（stage2 playbook §3b ④ / rule 4f：必做只有锚点图；反向 / 侧向 / 内景 plate 用到才建）。
> **bg 代号：`{key}`** · 目录 `scenes/{cont}/{z['id']}/{d}/` · 所属 {CONT_ZH[cont]} / {z['name_zh']}（{z['name_en']}）
> **版本红线**：Vanilla 1.12 · Year 25 ADP。4.0.3a 之后才有的东西一样都不许出现（`tools/wow_version_gate.py`）。
> **参考地图只进人眼，不进模型**（divergence #8）：
{chr(10).join('> - ' + r for r in ref_lines)}
> **场地平面图（rule 4k）**：`planning/blocks.toml` → `python tools/build_floorplan.py <本目录>` → `planning/{key}_floorplan.png`。
> **世界锚点**：本档锚点图挂 `{WORLD_ANCHOR}` 继承全剧影像质感（rule 4e ②）；配色 / 地貌 / 光线由本档 prompt 自己写死。

## 场景定位

{FILL}——两三段：这地方是什么、在区里的方位与相邻、空间结构给分镜的硬约束（天际线 / 出入口 / 河与路）、
本剧可能怎么用它（不确定就写「暂无排镜」）。

{chr(10).join(facts)}

## 锁定描述符（跨集 byte-identical，自然色名无 hex）

| # | 字段 | 值 |
|---|---|---|
| 1 | 类型 / 时代 / 室内外 | {FILL} |
| 2 | **空间结构 + 方位** | {FILL} |
| 3 | 主要建筑或自然元素 | {FILL} |
| 4 | 标志道具或装饰 | {FILL} |
| 5 | 默认光源 / 时辰 | {FILL} |
| 6 | 配色 | {FILL} |
| 7 | 氛围关键词 | {FILL} |
| 8 | **一句话锁定**（≤30 字，byte-identical 复制到所有 shot 的 `场景:` 行） | `{FILL}` |

## 关键变化态

| 变体 | 归属 | 处置 |
|---|---|---|
| 默认态 | 本档常态 | 锁定描述符 #5 即此态 |
| 天气 / 时辰变体 | 本档按镜条件分句 | shot 的 `光线:` 里写；不另立 bg |
| 结构变体（完好→废墟 / 日→夜烛火态） | 若要拍必须另立 bg（rule 4e ③） | 本季无 |

## 出现镜头

| 集 | 内容 | 用法 |
|---|---|---|
| — | 暂无排镜 | 阶段 5 排镜后回填 `ep##/shotNN` |

---

# 步骤一 · 锚点图 seed prompt（Seedream）— {b['name']}

> **用法**：上传世界锚点 `{WORLD_ANCHOR}` 作 image→image reference + 下方 prompt → 输出 `{d}.png` 落本目录。
> **生成块首行 ＝ `{d}`**（路由 handle，纯 ASCII 键 `{key}` 在首位，导入按它归位本目录）。
> **纯空间背景、无人物、无动物。** 画幅作 reference 用，16:9 亦可。
> **IP 合规（concept C3）**：正文只用绿级「不点名的形制描述」——不出现游戏名 / 公司名 / 世界内专名（地名 / 种族名 / 职业名）。
> **验收**：① 与区图裁切的方位关系一致；② 无 4.0.3a 元素；③ 画面零文字、零人物；④ 屋顶 / 墙体 / 植被色与锁定描述符 #6 一致。任一不过＝重跑。

## Prompt

```text
{d}
参考: `bg1_北郡山谷 世界锚点(图)=>@` —— 只继承影像质感与材质语汇，不继承地貌与配色；本地貌与配色以下文为准。
{FILL}
```

## 负向

```
人脸变形，五官漂移，畸形肢体，画面文字，字幕，水印，logo，夸张金光，人物自发光，现代服饰，现代建筑，现代器物，
塑料感材质，游戏引擎渲染感，游戏截图质感，UI 界面，血条，头顶名牌，伤害数字，低模棱角，贴图拉伸，卡通渲染，三维动画感，任何人物，任何动物
```
"""


def zone_md(w: World, z: dict, cont: str, bgs: list[dict], map_file: str | None, micro: list[str], ext: dict,
            skipped: list[str], reg_full: dict) -> str:
    Wm, Hm, src, note = zone_size_m(ext, z["id"])
    adj = [w.n[a]["name_zh"] for a in (z.get("adjacent") or []) if a in w.n]
    rows = []
    for b in bgs:
        node = w.n.get(b.get("node") or "")
        t = TYPE_ZH.get(node["type"], node["type"]) if node else "自造"
        st = (node or {}).get("subtype") or ""
        rows.append(f"| **{b['dir'].split('_', 1)[0]}** | [{b['name']}]({b['dir']}/{b['dir']}.md) | {t}{(' · ' + st) if st else ''} | "
                    f"{(node or {}).get('coords', '') or '—'} | {(node or {}).get('look_zh', '')[:60]} |")
    others = []
    for nid in w.descendants(z["id"]):
        if nid in reg_full or nid in skipped:
            continue
        n = w.n[nid]
        if n["type"] in ("poi", "transport", "dungeon", "raid", "battleground", "settlement", "subzone", "district"):
            others.append(f"- {n['name_zh'] or n['name_en']}（`{nid}` · {TYPE_ZH.get(n['type'], n['type'])}{(' · ' + n['subtype']) if n.get('subtype') else ''}）"
                          f"{(' → 属 ' + w.n[n['parent']]['name_zh']) if n.get('parent') in w.n and n['parent'] != z['id'] else ''}")
    kind = "全城" if z["type"] == "city" else "全境"
    return f"""# {z['name_zh']}（{z['name_en']}）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `{bgs[0]['dir']}/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/{cont}/{z['id']}/`（{CONT_ZH[cont]} → {z['name_zh']}），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | {TYPE_ZH.get(z['type'], z['type'])} · {z.get('level') or '—'} 级 · {z.get('faction') or '—'} |
| 相邻 | {' · '.join(adj) or '—'} |
| 世界地图尺寸 | {Wm:g} × {Hm:g} m（{src}：{note}） |
| 世界树画面 | {z.get('look_zh', '')} |
| 备注 | {z.get('note_zh', '')} |
| 出处 | {z.get('source_url', '')} |

## 原版参考地图（只进人眼，不进模型）

{('- `ref/' + os.path.basename(map_file) + '.link.json` → `' + os.path.relpath(map_file, REPO).replace(os.sep, '/') + '`') if map_file else '- ⚠ 参考图库里没有本区的原版区图（`tools/fetch_wow_maps.py --zone ' + z['id'] + '`）'}
{chr(10).join('- `ref/' + os.path.basename(m) + '.link.json` → 微型地下城图' for m in micro) if micro else ''}

## 区级场地平面图

`{bgs[0]['dir']}/planning/{bgs[0]['dir'].split('_', 1)[0]}_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（{len(bgs)} 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
{chr(10).join(rows)}

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

{chr(10).join(others) if others else '- 无'}
"""


def continent_md(w: World, cid: str, zones: list[dict], counts: dict[str, int]) -> str:
    c = w.n[cid]
    rows = [f"| [{z['name_zh']}]({z['id']}/{z['id']}.md) | {TYPE_ZH.get(z['type'], z['type'])} | {z.get('level') or '—'} | {counts.get(z['id'], 0)} |"
            for z in zones]
    return f"""# {c['name_zh']}（{c['name_en']}）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改。** 大陆一级的索引：区目录见下表；大陆图在 `ref/`。
> {c.get('look_zh', '')}

| 区 / 主城 | 类型 | 等级 | bg 数 |
|---|---|---|---|
{chr(10).join(rows)}
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--plans", action="store_true", help="重出所有区级 floor plan PNG")
    ap.add_argument("--zone", default="", help="只重生成这一个区（合并 terrain.toml → blocks.toml、区卡、ref 链接）；不动登记簿")
    args = ap.parse_args()
    dry = args.check

    w = World()
    ext = load_extents()
    meta, rows = load_registry()
    by_node = {r["node"]: r for r in rows if r.get("node")}
    by_dir = {r["dir"]: r for r in rows}
    forced = set(by_node)
    nxt = int(meta["next"])
    stats = collections.Counter()
    index_lines = ["# 全图索引（派生 · 由 tools/gen_world_scenes_szzl.py 生成）", ""]
    zone_counts: dict[str, int] = {}
    zones_by_cont: dict[str, list[dict]] = collections.defaultdict(list)

    for z in w.scenes():
        zid, cont = z["id"], w.continent(z["id"])
        zones_by_cont[cont].append(z)
        if args.zone and zid != args.zone:
            continue
        zdir = os.path.join(SCENES, cont, zid)
        kind = "全城" if z["type"] == "city" else "全境"
        # 区级主体
        whole_id = f"__whole__{zid}"
        if whole_id not in by_node:
            r = {"n": nxt, "node": whole_id, "dir": f"bg{nxt}_{safe_name(z['name_zh'], z['name_en'])}{kind}",
                 "zone": zid, "continent": cont, "kind": "zone_whole"}
            rows.append(r); by_node[whole_id] = r; by_dir[r["dir"]] = r; nxt += 1
        bgs = [dict(by_node[whole_id], name=z["name_zh"] + kind)]
        # 成员 bg
        selected = select_nodes(w, zid, forced)
        skipped: list[str] = []
        for nid in selected:
            n = w.n[nid]
            if nid in by_node:
                r = by_node[nid]
                if r["zone"] != zid:
                    skipped.append(nid)
                    continue
            else:
                base = safe_name(n["name_zh"], n["name_en"])
                d = f"bg{nxt}_{base}"
                r = {"n": nxt, "node": nid, "dir": d, "zone": zid, "continent": cont}
                rows.append(r); by_node[nid] = r; by_dir[d] = r; nxt += 1
            bgs.append(dict(r, name=n["name_zh"] or n["name_en"]))
        # 登记簿里挂在本区、但不对应世界树节点的自造 bg
        for r in rows:
            if r["zone"] == zid and not r.get("node"):
                bgs.append(dict(r, name=r["dir"].split("_", 1)[1]))
        bgs[1:] = sorted(bgs[1:], key=lambda b: b["n"])
        zone_counts[zid] = len(bgs)

        map_file, micro = zone_maps(w, zid)
        # 区目录：ref 链接
        if map_file:
            stats["link"] += link_json(os.path.join(zdir, "ref", os.path.basename(map_file) + ".link.json"), map_file,
                                       f"{z['name_zh']} 原版区图（{'c60' if 'c60' in map_file else '非 c60'}）· 只进人眼不进模型", dry)
        for m in micro:
            stats["link"] += link_json(os.path.join(zdir, "ref", os.path.basename(m) + ".link.json"), m, "微型地下城图 · 只进人眼不进模型", dry)
        else:
            if not map_file:
                stats["no_map"] += 1
                print(f"  ⚠ {z['name_zh']}（{zid}）没有原版区图")
        # 区卡
        stats["zone_md"] += write(os.path.join(zdir, f"{zid}.md"), zone_md(w, z, cont, bgs, map_file, micro, ext, skipped, by_node), dry)
        # 区级主体：terrain.toml（作者）+ blocks.toml（生成）+ md 骨架
        wd = os.path.join(zdir, bgs[0]["dir"])
        tpath = os.path.join(wd, "planning", "terrain.toml")
        terrain = {}
        if os.path.isfile(tpath):
            with open(tpath, "rb") as f:
                terrain = tomllib.load(f)
        else:
            stats["terrain_skel"] += write(tpath, "\n".join([
                f"# {z['name_zh']}{kind} · 区级平面图的地形层（作者拥有；blocks.toml 由生成器合并本文件后重写）",
                "# 从原版区图（ref/）量取：山脊 [[ridge]]（poly 多边形）/ 水系 [[water]]（path 折线）/ 道路 [[road]]（path 折线），单位 m。",
                f"# 换算见 blocks.toml 头两行。要覆盖某个自动块，写 [[block]] 且带同一个 bg 键；要加没坐标的块，写 [[block]] 不带 bg 键。",
                "", "[meta]", "absent = []", "",
            ]), dry)
        stats["zone_plan"] += write(os.path.join(wd, "planning", "blocks.toml"), zone_blocks_toml(w, ext, z, bgs[1:], bgs[0]["dir"], terrain), dry)
        stats["bg_md"] += write(os.path.join(wd, f"{bgs[0]['dir']}.md"),
                                bg_md_skeleton(w, bgs[0], None, z, cont, map_file, False, []).replace(
                                    "- **世界树节点**：无（剧本自造地点，见 registry.toml 的 note）",
                                    f"- **世界树节点**：`{zid}`（{TYPE_ZH.get(z['type'], z['type'])}，区级主体 ＝ 整个区的建场底图）\n- **世界树画面**：{z.get('look_zh', '')}\n- **世界树备注**：{z.get('note_zh', '')}\n- **出处**：{z.get('source_url', '')}"),
                                dry, only_if_missing=True)
        if map_file:
            stats["link"] += link_json(os.path.join(wd, "ref", os.path.basename(map_file) + ".link.json"), map_file, "原版区图 · 只进人眼不进模型", dry)
        # 成员 bg
        for b in bgs[1:]:
            node = w.n.get(b.get("node") or "")
            bd = os.path.join(zdir, b["dir"])
            c = parse_coords((node or {}).get("coords", ""))
            has_crop = False
            if map_file and c:
                has_crop = True
                stats["crop"] += crop(map_file, c, os.path.join(bd, "ref", f"{b['dir']}_map_crop.png"), dry)
            micro_links = [m for m in micro if node and compact(node["name_en"]) and compact(node["name_en"]) in compact(os.path.basename(m))]
            if map_file:
                stats["link"] += link_json(os.path.join(bd, "ref", os.path.basename(map_file) + ".link.json"), map_file, "原版区图 · 只进人眼不进模型", dry)
            for m in micro_links:
                stats["link"] += link_json(os.path.join(bd, "ref", os.path.basename(m) + ".link.json"), m, "微型地下城图 · 只进人眼不进模型", dry)
            stats["bg_md"] += write(os.path.join(bd, f"{b['dir']}.md"), bg_md_skeleton(w, b, node, z, cont, map_file, has_crop, micro_links), dry, only_if_missing=True)
            stats["bg_plan"] += write(os.path.join(bd, "planning", "blocks.toml"), bg_blocks_skeleton(b, node, z), dry, only_if_missing=True)
        index_lines.append(f"- **{CONT_ZH[cont]} / {z['name_zh']}**（`{cont}/{zid}/`）：{len(bgs)} 个 bg — " +
                           "、".join(f"`{b['dir']}`" for b in bgs))

    if args.zone:
        if nxt != int(meta["next"]):
            raise SystemExit("--zone 模式不许新增登记（发现 %d 个未登记节点）——先跑一次全量" % (nxt - int(meta["next"])))
        print(f"[zone {args.zone}] 写盘：" + " ".join(f"{k}={v}" for k, v in sorted(stats.items())))
        return 0
    for cid, zones in zones_by_cont.items():
        cdir = os.path.join(SCENES, cid)
        stats["cont_md"] += write(os.path.join(cdir, f"{cid}.md"), continent_md(w, cid, zones, zone_counts), dry)
        cref = os.path.join(REFS, cid, "_continent")
        if os.path.isdir(cref):
            for f in sorted(os.listdir(cref)):
                if f.lower().endswith((".jpg", ".png")):
                    stats["link"] += link_json(os.path.join(cdir, "ref", f + ".link.json"), os.path.join(cref, f), "大陆图 · 只进人眼不进模型", dry)

    stats["index"] += write(os.path.join(SCENES, "scenes_index.md"), "\n".join(index_lines) + "\n", dry)
    if not dry:
        meta["next"] = nxt
        save_registry(meta, rows)
    print(f"{'[check] ' if dry else ''}bg 登记 {len(rows)} 个（next={nxt}）· 区 {len(zone_counts)} 个 · 写盘：" +
          " ".join(f"{k}={v}" for k, v in sorted(stats.items())))

    if args.plans and not dry:
        fails = 0
        for z in w.scenes():
            zid, cont = z["id"], w.continent(z["id"])
            whole = by_node[f"__whole__{zid}"]
            d = os.path.join(SCENES, cont, zid, whole["dir"])
            r = subprocess.run([sys.executable, os.path.join(REPO, "tools", "build_floorplan.py"), d],
                               capture_output=True, text=True, encoding="utf-8")
            if r.returncode:
                fails += 1
                print(f"  ❌ {whole['dir']}: {r.stdout.strip()[-400:]}{r.stderr.strip()[-400:]}")
        print(f"区级 floor plan 重出完成，失败 {fails}")
        return 1 if fails else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
