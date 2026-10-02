# -*- coding: utf-8 -*-
"""暴风城平面图的输入生成器 —— 从 builder 的锚点表 + 建好的 blend 派生 `blocks.toml`。

用法（仓库根目录，两步）：
    blender -b ai_videos/shikong_lvxing/sk2/2_世界观人设/scenes/stormwind/_blender/stormwind.blend \
            --python tools/plan_stormwind.py
    python tools/build_floorplan.py ai_videos/shikong_lvxing/sk2/2_世界观人设/scenes/stormwind

为什么不手写 blocks.toml
------------------------
暴风城的几何**已经有一个出处**了：`tools/build_stormwind.py` 的 `ANCHORS`（14 个 GM 坐标锚点）
+ `CORRIDORS` / `LANDMARKS` / `CANAL`，以及它确定性生成出来的 `stormwind.blend`。
手写一份 `blocks.toml` 就是给同一份几何造第二个出处，两边必然漂（rule 4i ①）。
所以本脚本**只做派生**：位置与走向取锚点表，建筑体量的实际外接框与栋数取 blend。
改布局 ＝ 改 `build_stormwind.py` 重跑，再跑一次本脚本。

粒度：为什么不是 3411 个编号
----------------------------
blend 里有 3411 个网格，但「整城有多少建筑、布局在哪」这个问题在城市尺度上的正确粒度是
**街区带 + 地标**，不是单体。逐个编号 3411 次的图没人看得懂，也答不出面积对比。
所以：8 条走廊各聚成一个**街屋带**（名字里带栋数），6 个地标各自单列，城墙四面各一块。
单体仍在 blend 里，本图只回答「有什么、在哪、多大」——与 `build_floorplan.py` 的定位一致。
"""
from __future__ import annotations

import collections
import math
import os
import re
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_stormwind as sw  # noqa: E402

SCENE = os.path.join(sw.DRAMA, "2_世界观人设", "scenes", "stormwind")
OUT = os.path.join(SCENE, "planning", "blocks.toml")
PAD = 20.0          # 场地比墙外沿再放宽一圈，免得城墙块贴着画框边

# 名字不靠正则猜：走廊名与地标名都**直接取 builder 的表**（`CORRIDORS` / `LANDMARKS`），
# 只有「第几栋」这一段需要解析。第一版按 `-1/1` 猜侧向标记，实际是 `L/R`，于是一条街屋带都没匹配上 ——
# 凡是能从出处拿到的字符串就别猜（rule 4i ① 的同一条理由）。
BUILDING_RE = re.compile(r"^B_([ABC])_(.+?)_(\d{3})_([LR])(?:_\d+)?$")


def plan_xy(v: Vector) -> tuple[float, float]:
    """世界坐标 → 场地坐标（米，原点在场地西南角，+x 东 / +y 北）。"""
    return (v.x - X0 + PAD, v.y - Y0 + PAD)


def obb(pts: list[tuple[float, float]], theta: float) -> tuple[float, float, float, float]:
    """给定朝向的外接框 → (中心x, 中心y, 沿向长, 横向宽)。

    走廊是斜的，用轴对齐外接框会把面积算大一倍（一条 300 m 的斜街，AABB 能到 300×200）。
    所以按走廊自己的方向量：这才是「这一带的建筑占了多大一片」。
    """
    c, s = math.cos(-theta), math.sin(-theta)
    us = [p[0] * c - p[1] * s for p in pts]
    vs = [p[0] * s + p[1] * c for p in pts]
    u0, u1, v0, v1 = min(us), max(us), min(vs), max(vs)
    uc, vc = (u0 + u1) / 2, (v0 + v1) / 2
    ci, si = math.cos(theta), math.sin(theta)
    return (uc * ci - vc * si, uc * si + vc * ci, u1 - u0, v1 - v0)


def footprint(ob: bpy.types.Object) -> list[tuple[float, float]]:
    return [plan_xy(ob.matrix_world @ Vector(v)) for v in ob.bound_box]


def ztop(ob: bpy.types.Object) -> float:
    """物体顶面高度（米，已含 CITY_SCALE，因为 blend 本身就是缩放后的）。

    rule 4k 要求每块带 `h_m`——它是航线图**唯一算不出来**的那个数。
    这里从包围盒量，**绝不在图的生成器里手写高度**：手写的那一刻，
    这份图就从「blend 的派生物」变成了「blend 的第二份真相」。"""
    return max((ob.matrix_world @ Vector(v)).z for v in ob.bound_box)


# ── 场地范围：墙心线四至（缩放后）──────────────────────────────────
x0, y0, x1, y1 = sw.wall_bounds()
X0, Y0 = x0 * sw.CITY_SCALE, y0 * sw.CITY_SCALE
SITE_W = (x1 - x0) * sw.CITY_SCALE + PAD * 2
SITE_H = (y1 - y0) * sw.CITY_SCALE + PAD * 2

# ── 从 blend 聚合：街屋带（按走廊）与地标 ──────────────────────────
rows: dict[str, list[tuple[float, float]]] = collections.defaultdict(list)
units: dict[str, set[tuple[str, str]]] = collections.defaultdict(set)
rows_idx: dict[str, list[tuple[str, list[tuple[float, float]], tuple[str, str]]]] = collections.defaultdict(list)
marks: dict[str, list[tuple[float, float]]] = collections.defaultdict(list)
infill_by_zone: dict[str, list[tuple[float, float]]] = collections.defaultdict(list)
n_by_zone: dict[str, int] = collections.defaultdict(int)
h_rows: dict[str, float] = collections.defaultdict(float)
h_marks: dict[str, float] = collections.defaultdict(float)
h_infill: dict[str, float] = collections.defaultdict(float)
n_infill = 0


def nearest_anchor(v: Vector) -> str:
    """填充屋按**最近锚点**归到某个城区。

    第一版把 296 栋填充屋聚成一个外接框，结果是一个 307×255 m 的块盖住 93% 的场地、
    把整张图吃掉了 —— 它们本来就散布在九个城区里，聚合成一块既不真也不可读。
    """
    return min(sw.ANCHORS, key=lambda k: (v.x - sw.ANCHORS[k][0] * sw.CITY_SCALE) ** 2
               + (v.y - sw.ANCHORS[k][1] * sw.CITY_SCALE) ** 2)
for ob in bpy.data.objects:
    if ob.type != "MESH":
        continue
    m = BUILDING_RE.match(ob.name)
    if m:
        fp = footprint(ob)
        rows[m.group(2)] += fp
        h_rows[m.group(2)] = max(h_rows[m.group(2)], ztop(ob))
        rows_idx[m.group(2)].append((m.group(2), fp, (m.group(3), m.group(4))))
        units[m.group(2)].add((m.group(3), m.group(4)))      # 一栋可能由体块+屋顶多件组成，按 (序号, 侧) 去重
        continue
    if ob.name.startswith("F_infill") and "roof" not in ob.name:
        _z = nearest_anchor(ob.matrix_world.translation)
        infill_by_zone[_z] += footprint(ob)
        h_infill[_z] = max(h_infill[_z], ztop(ob))
        n_by_zone[nearest_anchor(ob.matrix_world.translation)] += 1
        n_infill += 1
        continue
    for lm_name, *_rest in sw.LANDMARKS:
        if ob.name == f"L_{lm_name}" or ob.name.startswith(f"L_{lm_name}_"):
            marks[lm_name] += footprint(ob)
            h_marks[lm_name] = max(h_marks[lm_name], ztop(ob))
            break

anchor_of = {n: sw.ANCHORS[n] for n in sw.ANCHORS}
blocks: list[dict] = []

def seg_of(p: tuple[float, float], segs: list[tuple[tuple[float, float], tuple[float, float]]]) -> int:
    """点归到折线的哪一段（按到线段的距离）。"""
    best, bi = 1e18, 0
    for i, (a, b) in enumerate(segs):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dy * dy or 1.0
        u = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
        d = (p[0] - a[0] - dx * u) ** 2 + (p[1] - a[1] - dy * u) ** 2
        if d < best:
            best, bi = d, i
    return bi


for name, anchors, _radius, _grade in sw.CORRIDORS:
    if name not in rows:
        continue
    pl = [plan_xy(Vector((anchor_of[a][0] * sw.CITY_SCALE, anchor_of[a][1] * sw.CITY_SCALE, 0.0)))
          for a in anchors]
    segs = list(zip(pl, pl[1:]))
    # 折线走廊（三个锚点）整条取外接框，会把两段并成一个横跨半城的大斜框；按段拆才贴合实际街面
    per: dict[int, list[tuple[float, float]]] = collections.defaultdict(list)
    cnt: dict[int, set[tuple[str, str]]] = collections.defaultdict(set)
    for key, quad, uid in rows_idx[name]:
        i = seg_of(((quad[0][0] + quad[6][0]) / 2, (quad[0][1] + quad[6][1]) / 2), segs) if len(quad) > 6             else seg_of(quad[0], segs)
        per[i] += quad
        cnt[i].add(uid)
    for i, pts in sorted(per.items()):
        a, b = segs[i]
        theta = math.atan2(b[1] - a[1], b[0] - a[0])
        cx, cy, L, Wd = obb(pts, theta)
        tag = name if len(segs) == 1 else f"{name}·第{i + 1}段"
        blocks.append(dict(name=f"{tag}·街屋带（{len(cnt[i])} 栋）", xy=(cx, cy), size=(L, Wd),
                           rot=round(math.degrees(theta), 1), src="坐标表",
                           h_m=round(h_rows[name], 1)))

for name, pts in marks.items():
    cx, cy, L, Wd = obb(pts, 0.0)
    blocks.append(dict(name=name, xy=(cx, cy), size=(L, Wd), rot=0.0, src="坐标表",
                       h_m=round(h_marks[name], 1)))

for zone, pts in sorted(infill_by_zone.items(), key=lambda kv: -n_by_zone[kv[0]]):
    cx, cy, L, Wd = obb(pts, 0.0)
    blocks.append(dict(name=f"{zone}·街区填充屋（{n_by_zone[zone]} 栋）", xy=(cx, cy),
                       size=(L, Wd), rot=0.0, src="推定", h_m=round(h_infill[zone], 1)))

# 城墙四面：各一块（沿用 bg2 修道院把院墙也当块的做法——墙是场地里最大的几何，不该隐形）
wx0, wy0 = plan_xy(Vector((X0, Y0, 0.0)))
wx1, wy1 = plan_xy(Vector((x1 * sw.CITY_SCALE, y1 * sw.CITY_SCALE, 0.0)))
T = sw.WALL_T
for tag, (cx, cy, lw, lh) in (
        ("南", ((wx0 + wx1) / 2, wy0, wx1 - wx0, T)),
        ("北", ((wx0 + wx1) / 2, wy1, wx1 - wx0, T)),
        ("西", (wx0, (wy0 + wy1) / 2, T, wy1 - wy0)),
        ("东", (wx1, (wy0 + wy1) / 2, T, wy1 - wy0))):
    blocks.append(dict(name=f"城墙·{tag}", xy=(cx, cy), size=(lw, lh), rot=0.0, src="坐标表",
                       h_m=round(sw.WALL_H * sw.CITY_SCALE, 1)))

# ── 运河与街道：折线层 ─────────────────────────────────────────────
canal = [plan_xy(Vector((*(c * sw.CITY_SCALE for c in anchor_of[a][:2]), 0.0))) for a in sw.CANAL]
roads = []
for name, anchors, _r, _g in sw.CORRIDORS:
    roads.append((name, [plan_xy(Vector((*(c * sw.CITY_SCALE for c in anchor_of[a][:2]), 0.0)))
                         for a in anchors]))
gate = plan_xy(Vector((0.0, 0.0, 0.0)))
roads.append(("南侧引道", [(gate[0], gate[1] - min(PAD, gate[1])), gate]))


def fmt(v: tuple[float, float]) -> str:
    return f"[{v[0]:.1f}, {v[1]:.1f}]"


lines = [
    "# 暴风城 · 平面图输入 —— **本文件由 tools/plan_stormwind.py 生成，不要手改**",
    "# 出处：tools/build_stormwind.py 的 ANCHORS/CORRIDORS/LANDMARKS/CANAL + 它生成的 stormwind.blend。",
    "# 改布局 ＝ 改 build_stormwind.py 重跑，再跑一次 plan_stormwind.py（rule 4i ①：一份东西只有一个出处）。",
    f"# 比例：坐标已按 build_stormwind.CITY_SCALE = {sw.CITY_SCALE} 缩放，尺寸 1:1。",
    "",
    "[meta]",
    'bg = "stormwind"',
    'name_zh = "暴风城"',
    f"size_m = [{SITE_W:.0f}, {SITE_H:.0f}]",
    ('scale_note = "坐标 ×0.5（sk2 沿 sk1 做法），尺寸 1:1；全城原尺 640×600 m，'
     '本图为缩放后的场地"'),
    'scale_src = "坐标表"',
    'label_mode = "number"',
    "",
]
for i, b in enumerate(blocks, 1):
    # id 是**可引用的稳定键**；圆牌号按面积降序生成，改一块尺寸就重排，不能当键（rule 4k）。
    lines += ["[[block]]", f'id = "b{i:02d}"', f'name = "{b["name"]}"', f"xy = {fmt(b['xy'])}",
              f"size = [{b['size'][0]:.1f}, {b['size'][1]:.1f}]",
              f"h_m = {b.get('h_m', 0.0):g}"]
    if abs(b["rot"]) > 0.05:
        lines.append(f"rot = {b['rot']}")
    lines += [f'src = "{b["src"]}"', ""]
lines += ["[[water]]", 'name = "运河"', "width_m = %.1f" % sw.CANAL_W,
          "path = [" + ", ".join(fmt(p) for p in canal) + "]", ""]
for name, path in roads:
    lines += ["[[road]]", f'name = "{name}"', "width_m = 8.0",
              "path = [" + ", ".join(fmt(p) for p in path) + "]", ""]

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))
total = sum(len(u) for u in units.values()) + n_infill
print(f"PLAN 写出 {OUT}")
print(f"PLAN 场地 {SITE_W:.0f} × {SITE_H:.0f} m；{len(blocks)} 块"
      f"（{len(rows)} 条街屋带 · {len(marks)} 个地标 · 4 面城墙）；整城 {total} 栋建筑")
