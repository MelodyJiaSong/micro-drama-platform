# -*- coding: utf-8 -*-
"""Build `london.blend` — the one piece of sk3 geometry everything else renders from.

Why a script and not a hand-modelled file (`ai_video.md` rule 4h ④): a blend that
somebody edited by hand has no reviewable source, and blends are gitignored and
live in R2. Geometry changes mean changing this file and re-running.

What this is NOT: `build_bianjing.py` is a 4600-line artisanal reconstruction of
Kaifeng. This is deliberately parametric and far smaller, because sk3's blend has
exactly one job — **give previz the geometry and the camera paths** (rule 4g ③:
一致性来自只有一份几何; 长相由锚点图给, 不由白模给). Nothing here is ever an
image reference (rule 4d ①).

Precision is graded by how close the camera gets (rule 4g ④), not by importance:
    A 真立面   镜头贴身走过（布丁巷南 38 m、桥面）   → 逐层外挑的 jetty、门窗洞
    B 体块+屋顶 中景背景（Cheapside、泰晤士街）      → 体量 + 坡屋顶形制
    C 纯体块   航拍远景（其余全城）                  → 盒子 + 屋顶棱
    D 不建     镜头拍不到

Origin = the Monument site. The fire starts **61.6 m due east of origin**
(`london1666.city.*`: Monument 现址在起火点正西 202 ft). The Monument itself is
never built — it is a 1671 structure and appearing in frame is a continuity
break (blacklist L03); it is a coordinate anchor only.

⚠️ Coordinates are **推算** from the distances the dossier does pin down (bridge
926 ft, Cheapside 450 yds, Thames Street 1800 yds, wall 10608 ft). Street widths
are among dossier §14's four "禁止编数字" items, so they are parameters here with
a stated basis, not invented facts. Before this drives a hero shot, overlay
**Ogilby & Morgan 1676 (100 ft/inch)** and replace these numbers.

Run:
    blender -b --factory-startup --python tools/build_london.py -- --out <path>
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import bpy
import bmesh  # noqa: F401  (kept: bpy pulls it in for mesh ops we may add)
from mathutils import Vector

REPO = Path(__file__).resolve().parent.parent
SCENE_DIR = REPO / "ai_videos" / "shikong_lvxing" / "sk3" / "2_世界观人设" / "scenes" / "london"
DEFAULT_OUT = SCENE_DIR / "_blender" / "london.blend"

# ── 尺度参数（每个都标出处或「推算」） ──────────────────────────────────────────
FT = 0.3048
YD = 0.9144

BRIDGE_LEN = 926 * FT              # ✅ city.006
BRIDGE_W = 8.0                     # ⚠️ 推算：桥面街道 + 两侧房屋，按 1682 立面比例
CHEAPSIDE_LEN = 450 * YD           # ✅ city.024
THAMES_ST_LEN = 1800 * YD          # ✅ city.*
WALL_PERIM = 10608 * FT            # ✅ city.*

FIRE_X = 202 * FT                  # ✅ 起火点在 Monument 现址正东 61.6 m

LANE_W = 4.0                       # ⚠️ 推算上限：1667 年法要拓宽「一切窄于 14 ft（4.27 m）的通道」
CHEAPSIDE_W = 14.0                 # ⚠️ 推算：全城最宽，按「日光能落到街面」反推
THAMES_ST_W = 7.0                  # ⚠️ 推算

STOREY = [10 * FT, 10.5 * FT, 9 * FT, 8.5 * FT]   # ✅ housing.*：四等房层高表
JETTY = 0.45                       # ✅ housing.*：逐层外挑 0.35–0.55 m，取中值
ROOF_PITCH = math.radians(50.0)    # ⚠️ 推算：陡坡瓦顶

RIVER_Y = -150.0
RIVER_W = 250.0                    # ⚠️ 推算
BANK_Z = 3.0

COL = {                            # 白模只分档，不分长相（rule 4g ⑤：ID 色非服装）
    "A": (0.78, 0.75, 0.70, 1.0),
    "B": (0.62, 0.60, 0.57, 1.0),
    "C": (0.48, 0.47, 0.45, 1.0),
    "water": (0.30, 0.34, 0.38, 1.0),
    "ground": (0.40, 0.39, 0.37, 1.0),
    "stone": (0.82, 0.80, 0.76, 1.0),
}


# ══════════════════════════════════════════════════════════════════════════════
# 基元
# ══════════════════════════════════════════════════════════════════════════════

def _clear() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)


def _mat(name: str, rgba) -> bpy.types.Material:
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        bsdf = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
        if bsdf is not None:
            bsdf.inputs["Base Color"].default_value = rgba
            if "Roughness" in bsdf.inputs:
                bsdf.inputs["Roughness"].default_value = 0.85
    return m


def box(name: str, center, size, grade: str = "C", coll=None) -> bpy.types.Object:
    cx, cy, cz = center
    sx, sy, sz = (s / 2.0 for s in size)
    v = [(cx - sx, cy - sy, cz - sz), (cx + sx, cy - sy, cz - sz),
         (cx + sx, cy + sy, cz - sz), (cx - sx, cy + sy, cz - sz),
         (cx - sx, cy - sy, cz + sz), (cx + sx, cy - sy, cz + sz),
         (cx + sx, cy + sy, cz + sz), (cx - sx, cy + sy, cz + sz)]
    f = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    me = bpy.data.meshes.new(name)
    me.from_pydata(v, [], f)
    # 建完就地校验：不做的话每次打开 blend 都要现修一遍拓扑，
    # 一次 previz 渲染的日志里刷出十万行 "edge appears twice, correcting"。
    me.validate(verbose=False)
    me.update()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(_mat("M_%s" % grade, COL.get(grade, COL["C"])))
    (coll or bpy.context.scene.collection).objects.link(ob)
    return ob


def gable(name: str, center, size, grade: str = "C", coll=None) -> bpy.types.Object:
    """坡屋顶：两坡，脊沿 x。size=(长x, 进深y, 檐到脊高z)。"""
    cx, cy, cz = center
    sx, sy, sz = size[0] / 2.0, size[1] / 2.0, size[2]
    v = [(cx - sx, cy - sy, cz), (cx + sx, cy - sy, cz),
         (cx + sx, cy + sy, cz), (cx - sx, cy + sy, cz),
         (cx - sx, cy, cz + sz), (cx + sx, cy, cz + sz)]
    f = [(0, 1, 5, 4), (2, 3, 4, 5), (0, 4, 3), (1, 2, 5), (0, 3, 2, 1)]
    me = bpy.data.meshes.new(name)
    me.from_pydata(v, [], f)
    # 建完就地校验：不做的话每次打开 blend 都要现修一遍拓扑，
    # 一次 previz 渲染的日志里刷出十万行 "edge appears twice, correcting"。
    me.validate(verbose=False)
    me.update()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(_mat("M_%s" % grade, COL.get(grade, COL["C"])))
    (coll or bpy.context.scene.collection).objects.link(ob)
    return ob


def coll(name: str) -> bpy.types.Collection:
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    return c


# ══════════════════════════════════════════════════════════════════════════════
# 构件：一栋 jetty 木构架房（A 档给真立面，B/C 档退化成体块）
# ══════════════════════════════════════════════════════════════════════════════

def jetty_house(name: str, x: float, y: float, facing: str, width: float,
                depth: float, grade: str, c, axis: str = "x") -> None:
    """一栋四层木构架房，逐层向街心外挑 JETTY。

    `axis` 是**街的走向**，不是房子的朝向 —— 初版漏了它，于是南北走向的布丁巷
    被按东西走向建了出来，整排房子转了 90°，校验图里相机直接埋进墙里。
      axis='x' 街沿 x 走：面宽沿 x，进深沿 y，朝向 facing ∈ {'+y','-y'}
      axis='y' 街沿 y 走：面宽沿 y，进深沿 x，朝向 facing ∈ {'+x','-x'}
    """
    sign = 1.0 if facing in ("+y", "+x") else -1.0
    z = 0.0
    for i, h in enumerate(STOREY):
        step = (i * JETTY) if grade == "A" else 0.0
        d_i = depth + step
        off = sign * step / 2.0
        if axis == "x":
            box("%s_L%d" % (name, i + 1), (x, y + off, z + h / 2.0), (width, d_i, h), grade, c)
        else:
            box("%s_L%d" % (name, i + 1), (x + off, y, z + h / 2.0), (d_i, width, h), grade, c)
        z += h
    top_d = depth + (len(STOREY) - 1) * JETTY if grade == "A" else depth
    rise = top_d * math.tan(ROOF_PITCH) / 2.0
    if axis == "x":
        gable("%s_roof" % name, (x, y, z), (width, top_d, rise), grade, c)
    else:
        gable("%s_roof" % name, (x, y, z), (top_d, width, rise), grade, c)


def street_row(tag: str, x0: float, x1: float, y: float, facing: str,
               grade: str, c, bay: float = 5.0, depth: float = 7.0,
               gaps: tuple[tuple[float, float], ...] = ()) -> None:
    """沿 x 的一排临街房。`gaps` ＝ 横穿街的开口，落在开口里的开间不建。

    没有 gaps 的初版把泰晤士街整排房子盖到了布丁巷口上，巷子南端被堵死，
    校验渲图是一个封闭的盒子 —— 靠看图猜了两轮才查出来，教训是直接查包围盒。
    """
    n = max(1, int(abs(x1 - x0) / bay))
    for i in range(n):
        x = x0 + (i + 0.5) * (x1 - x0) / n
        half = bay / 2.0
        if any(x + half > g0 and x - half < g1 for g0, g1 in gaps):
            continue
        jetty_house("%s_%02d" % (tag, i), x, y, facing, bay * 0.96, depth, grade, c)


# 横穿主街的路口（街心 ± 半宽 + 1 m 余量）——所有沿街排房都要让开它们
CROSSINGS: tuple[tuple[float, float], ...] = (
    (FIRE_X - LANE_W / 2 - 1.0, FIRE_X + LANE_W / 2 + 1.0),   # 布丁巷
    (-3.5, 3.5),                                              # Fish Street Hill
    (-86.0, -74.0),                                           # 桥头引道
)


# ══════════════════════════════════════════════════════════════════════════════
# 城
# ══════════════════════════════════════════════════════════════════════════════

def build_river(c) -> None:
    box("river", (0, RIVER_Y, -0.5), (1500, RIVER_W, 1.0), "water", c)
    box("bank_north", (0, RIVER_Y + RIVER_W / 2 + 6, BANK_Z / 2), (1500, 12, BANK_Z), "C", c)
    box("bank_south", (0, RIVER_Y - RIVER_W / 2 - 6, BANK_Z / 2), (1500, 12, BANK_Z), "C", c)


def build_bridge(c) -> None:
    """旧伦敦桥：**北端 42 栋 1633 年烧掉后到 1666 年仍未重建**（city.008）。

    这道空档是 shot09 的切口，也是明天挡住火烧向南岸的防火带 —— 几何上必须是空的。
    """
    bx = -80.0
    y_s = RIVER_Y - RIVER_W / 2 - 10
    y_n = RIVER_Y + RIVER_W / 2 + 10
    box("bridge_deck", (bx, (y_s + y_n) / 2, BANK_Z), (BRIDGE_W, y_n - y_s, 1.2), "A", c)
    # 桥墩
    npier = 19                                   # ⚠️ 推算：按跨度均分
    for i in range(npier):
        py = y_s + (i + 0.5) * (y_n - y_s) / npier
        box("pier_%02d" % i, (bx, py, -1.0), (BRIDGE_W + 3.0, 5.0, 6.0), "B", c)
    # 桥上房屋：只盖到北端留出空档
    gap_start = y_n - 62.0                       # ✅ 42 栋的空档，按 BAY 反推
    y = y_s + 14.0
    i = 0
    while y < gap_start:
        for side, fx in (("W", -1), ("E", +1)):
            jetty_house("brhouse_%s%02d" % (side, i), bx + fx * (BRIDGE_W / 2 + 3.0), y,
                        "+y", 4.6, 6.0, "A", c)
        # 每隔一栋一道跨街 cross building（city.009）
        if i % 2 == 1:
            box("cross_%02d" % i, (bx, y, BANK_Z + 11.0), (BRIDGE_W + 12.0, 4.4, 3.2), "A", c)
        y += 5.0
        i += 1
    # 北端空档：只有桥面与一排松木挡板
    box("plank_fence_W", (bx - BRIDGE_W / 2 - 0.2, (gap_start + y_n) / 2, BANK_Z + 1.2),
        (0.25, y_n - gap_start, 1.1), "A", c)
    box("plank_fence_E", (bx + BRIDGE_W / 2 + 0.2, (gap_start + y_n) / 2, BANK_Z + 1.2),
        (0.25, y_n - gap_start, 1.1), "A", c)


def build_pudding_lane(c) -> None:
    """A 档：镜头贴身走过的 38 m（shot15 一镜到底）。"""
    x = FIRE_X
    y0, y1 = -100.0, -40.0
    box("pudding_ground", (x, (y0 + y1) / 2, BANK_Z - 0.05),
        (LANE_W, y1 - y0, 0.1), "ground", c)
    # 南北走向的街 → axis='y'：面宽沿 y、进深沿 x，临街面朝街心
    for fx, facing, tag in ((-1, "+x", "W"), (+1, "-x", "E")):
        n = int((y1 - y0) / 5.0)
        for i in range(n):
            yy = y0 + (i + 0.5) * (y1 - y0) / n
            jetty_house("pl_%s%02d" % (tag, i), x + fx * (LANE_W / 2 + 3.5), yy,
                        facing, 4.8, 7.0, "A", c, axis="y")
    # 面包铺的炉膛：巷西侧，起火点（ANCHOR_fire_origin 与它对位）
    box("bakehouse_oven", (x - LANE_W / 2 - 1.2, y0 + 18.0, BANK_Z + 1.0),
        (2.2, 2.2, 2.0), "A", c)


def build_cheapside(c) -> None:
    box("cheapside_ground", (0, 120.0, BANK_Z - 0.05), (CHEAPSIDE_LEN, CHEAPSIDE_W, 0.1), "ground", c)
    street_row("chs_N", -CHEAPSIDE_LEN / 2, CHEAPSIDE_LEN / 2, 120.0 + CHEAPSIDE_W / 2 + 4, "-y", "B", c,
               gaps=CROSSINGS)
    street_row("chs_S", -CHEAPSIDE_LEN / 2, CHEAPSIDE_LEN / 2, 120.0 - CHEAPSIDE_W / 2 - 4, "+y", "B", c,
               gaps=CROSSINGS)


def build_thames_street(c) -> None:
    y = -100.0
    box("thames_st_ground", (0, y, BANK_Z - 0.05), (THAMES_ST_LEN, THAMES_ST_W, 0.1), "ground", c)
    street_row("ths_N", -THAMES_ST_LEN / 2, THAMES_ST_LEN / 2, y + THAMES_ST_W / 2 + 5, "-y", "B", c,
               bay=8.0, depth=10.0, gaps=CROSSINGS)
    # 南侧是码头与货栈
    street_row("ths_S", -THAMES_ST_LEN / 2, THAMES_ST_LEN / 2, y - THAMES_ST_W / 2 - 6, "+y", "B", c,
               bay=10.0, depth=12.0, gaps=CROSSINGS)


def build_st_pauls(c) -> None:
    """航拍最容易画废的一处：**无尖顶、无圆顶**，只剩 204 ft 方塔残段 + 古典柱廊 + 满墙脚手架。"""
    px, py = -430.0, 150.0
    nave_l, nave_w = 178.0, 31.0                 # ⚠️ 推算：中世纪旧堂体量
    box("stp_nave", (px, py, BANK_Z + 16.0), (nave_l, nave_w, 32.0), "B", c)
    gable("stp_nave_roof", (px, py, BANK_Z + 32.0), (nave_l, nave_w, 11.0), "B", c)
    box("stp_transept", (px + 10, py, BANK_Z + 15.0), (26.0, 74.0, 30.0), "B", c)
    gable("stp_transept_roof", (px + 10, py, BANK_Z + 30.0), (26.0, 74.0, 9.0), "B", c)
    # 方塔残段：204 ft，**顶是平的**
    tower_h = 204 * FT
    box("stp_tower", (px + 10, py, BANK_Z + tower_h / 2), (22.0, 22.0, tower_h), "B", c)
    box("stp_tower_flat_top", (px + 10, py, BANK_Z + tower_h + 0.6), (23.0, 23.0, 1.2), "B", c)
    # Inigo Jones 西端柱廊：十柱 × 四排，柱高 45 ft
    ch = 45 * FT
    for i in range(10):
        for j in range(4):
            box("stp_col_%d_%d" % (i, j),
                (px - nave_l / 2 - 4.0 - j * 3.2, py - 13.5 + i * 3.0, BANK_Z + ch / 2),
                (1.5, 1.5, ch), "B", c)
    box("stp_portico_arch", (px - nave_l / 2 - 8.8, py, BANK_Z + ch + 2.0), (14.0, 31.0, 4.0), "B", c)
    # 满墙勘修脚手架（1666 年正在勘修）
    for i in range(24):
        box("stp_scaff_%02d" % i, (px - nave_l / 2 + i * 7.5, py - nave_w / 2 - 1.2, BANK_Z + 17.0),
            (0.35, 0.35, 34.0), "B", c)


def build_royal_exchange(c) -> None:
    ex, ey = 150.0, 165.0
    side, h = 56.0, 13.0
    for dx, dy, sx, sy in ((0, side / 2, side, 8.0), (0, -side / 2, side, 8.0),
                           (side / 2, 0, 8.0, side), (-side / 2, 0, 8.0, side)):
        box("rex_wing_%d_%d" % (dx, dy), (ex + dx, ey + dy, BANK_Z + h / 2), (sx, sy, h), "B", c)
    box("rex_tower", (ex, ey - side / 2 - 3, BANK_Z + 21.0), (10.0, 10.0, 42.0), "B", c)


def build_inn(c) -> None:
    ix, iy = -6.0, -62.0                         # Fish Street Hill
    side = 22.0
    for dx, dy, sx, sy in ((0, side / 2, side, 7.0), (0, -side / 2, side, 7.0),
                           (side / 2, 0, 7.0, side), (-side / 2, 0, 7.0, side)):
        box("inn_%d_%d" % (dx, dy), (ix + dx, iy + dy, BANK_Z + 5.0), (sx, sy, 10.0), "A", c)
    box("inn_stable", (ix, iy - side / 2 - 8, BANK_Z + 2.2), (14.0, 8.0, 4.4), "A", c)
    box("inn_hay", (ix + 5.0, iy - side / 2 - 8, BANK_Z + 1.2), (4.0, 4.0, 2.4), "A", c)


def build_wall_and_fill(c) -> None:
    """C 档：航拍远景的纯体块城 + 城墙 + 教堂塔林。"""
    half_x, half_y = 560.0, 330.0
    for tag, x0, x1, y, in (("N", -half_x, half_x, half_y), ("S", -half_x, half_x, -half_y + 190)):
        box("wall_%s" % tag, ((x0 + x1) / 2, y, BANK_Z + 3.5), (x1 - x0, 4.0, 7.0), "C", c)
    for tag, y0, y1, x in (("W", -half_y + 190, half_y, -half_x), ("E", -half_y + 190, half_y, half_x)):
        box("wall_%s" % tag, (x, (y0 + y1) / 2, BANK_Z + 3.5), (4.0, y1 - y0, 7.0), "C", c)

    # 填充街区：确定性伪随机，保证每次重跑完全一样
    rng = 12345
    n = 0
    for gx in range(-20, 21):
        for gy in range(-4, 13):
            x, y = gx * 27.0, gy * 27.0 - 40.0
            if abs(x) > half_x - 20 or y > half_y - 20 or y < -half_y + 205:
                continue
            if abs(y - 120.0) < 18 or abs(y + 100.0) < 14 or abs(x - FIRE_X) < 8:
                continue                          # 让开主街与布丁巷
            rng = (rng * 1103515245 + 12345) & 0x7FFFFFFF
            h = 9.0 + (rng % 700) / 100.0
            rng = (rng * 1103515245 + 12345) & 0x7FFFFFFF
            w = 16.0 + (rng % 900) / 100.0
            box("blk_%02d_%02d" % (gx + 20, gy + 4), (x, y, BANK_Z + h / 2), (w, w, h), "C", c)
            gable("blkroof_%02d_%02d" % (gx + 20, gy + 4), (x, y, BANK_Z + h), (w, w, w * 0.35), "C", c)
            n += 1
            # 约每 12 个街区插一座教堂塔 —— 天际线是塔林（city.025）
            if n % 12 == 0:
                th = 26.0 + (rng % 1400) / 100.0
                box("tower_%02d_%02d" % (gx + 20, gy + 4), (x + 9, y + 9, BANK_Z + th / 2),
                    (5.0, 5.0, th), "C", c)
                box("spire_%02d_%02d" % (gx + 20, gy + 4), (x + 9, y + 9, BANK_Z + th + 5.0),
                    (2.0, 2.0, 10.0), "C", c)


def join_per_collection() -> None:
    """把每个 collection 里的网格并成一个对象。

    **这一步不是洁癖，是 previz 能不能跑完的分水岭。** 初版留下 4383 个独立网格，
    EEVEE 的逐对象开销把 960×540 的一帧拖到 **23 秒**——单镜 360 帧要 2.3 小时，
    38 镜 87 小时，整条 previz 管线直接不可行。合并后对象数降到十几个，
    几何一个面都没少，分档材质也还在（按 collection 分，正好一档一个对象）。
    """
    import bpy
    before = len([o for o in bpy.data.objects if o.type == "MESH"])
    for c in list(bpy.context.scene.collection.children):
        objs = [o for o in c.objects if o.type == "MESH"]
        if len(objs) < 2:
            continue
        bpy.ops.object.select_all(action="DESELECT")
        for o in objs:
            o.select_set(True)
        bpy.context.view_layer.objects.active = objs[0]
        bpy.ops.object.join()
        objs[0].name = "%s_merged" % c.name
    after = len([o for o in bpy.data.objects if o.type == "MESH"])
    print("[london] 合并网格 %d → %d 个对象" % (before, after))


def build_ground(c) -> None:
    """两岸分开建 —— 一整块地形会把河整个盖掉（初版就是这么翻的车，校验图一眼看出来）。"""
    north_y0 = RIVER_Y + RIVER_W / 2
    south_y1 = RIVER_Y - RIVER_W / 2
    # 范围只包住城 + 余量。**这不只是洁癖**：三盏 sun 的阴影要覆盖整个场景范围，
    # 2400×1000 的地形把 previz 单帧拖到十几秒；城本身只有约 1120×660。
    box("terrain_north", (0, north_y0 + 330, BANK_Z / 2 - 0.2), (1500, 660, BANK_Z), "ground", c)
    box("terrain_south", (0, south_y1 - 120, BANK_Z / 2 - 0.2), (1500, 240, BANK_Z), "ground", c)


# ══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args(argv)

    _clear()
    sc = bpy.context.scene
    sc.unit_settings.system = "METRIC"

    # 这个 blend **只服务 previz**（rule 4g ③：几何一致来自只有一份几何；长相由锚点图给）。
    # 所以这里可以为 previz 的成本做取舍——实测本场景 640×360 单帧：
    #   开阴影 6.4 s ／ 关阴影 1.0 s（6.4×）。38 镜 × 240 帧的差别是 ~16 小时 vs ~2.5 小时。
    # build_previz 会删掉本文件里的灯、换成它自己的三灯 rig，所以只能在**场景级**关；
    # 白模的体积靠 AO + 三灯的主/补/轮廓比读得出来，不靠投影。
    sc.render.engine = "BLENDER_EEVEE"
    if hasattr(sc.eevee, "use_shadows"):
        sc.eevee.use_shadows = False

    build_ground(coll("00_terrain"))
    build_river(coll("01_river"))
    build_wall_and_fill(coll("02_city_C"))
    build_thames_street(coll("03_thames_street_B"))
    build_cheapside(coll("04_cheapside_B"))
    build_st_pauls(coll("05_st_pauls_B"))
    build_royal_exchange(coll("06_royal_exchange_B"))
    build_bridge(coll("07_bridge_A"))
    build_pudding_lane(coll("08_pudding_lane_A"))
    build_inn(coll("09_inn_A"))

    join_per_collection()

    # 坐标锚点：Monument 现址（**不建几何**，只放一个 empty 供对位）
    anchor = bpy.data.objects.new("ANCHOR_monument_site_1671_DO_NOT_RENDER", None)
    anchor.empty_display_type = "PLAIN_AXES"
    anchor.location = Vector((0, 0, BANK_Z))
    sc.collection.objects.link(anchor)
    fire = bpy.data.objects.new("ANCHOR_fire_origin", None)
    fire.empty_display_type = "SPHERE"
    fire.location = Vector((FIRE_X, -82.0, BANK_Z))
    sc.collection.objects.link(fire)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out))
    n = len([o for o in bpy.data.objects if o.type == "MESH"])
    print("[london] %d meshes → %s" % (n, out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
