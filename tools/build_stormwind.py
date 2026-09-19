# -*- coding: utf-8 -*-
"""暴风城（sk2）整城 Blender 建模 —— 走廊制、确定性生成、不手改。

用法（仓库根目录）：
    blender -b --factory-startup --python tools/build_stormwind.py
    blender -b --factory-startup --python tools/build_stormwind.py -- --check   # 只出校验 PNG

产物：
    ai_videos/shikong_lvxing/sk2/2_世界观人设/scenes/stormwind/_blender/stormwind.blend
    同目录 check_plan.png / check_persp.png（校验图，给人眼比体量用）

设计依据
--------
· 坐标与锚点：`0_research/parts/w1_city_layout.md`（GM 世界坐标表 14 锚点，与 wiki 文字方位 10/10 互验）
· 换算：east = -(y-451.377)×0.9144，north = (x+9040.899)×0.9144，up = (z-93.056)×0.9144（米）
· **比例 0.5**（沿 sk1 做法）：全城 640×600×37 m → 320×300×18.5 m，单 blend 吃得下
· **走廊制**（rule 4g ④ + sk1 divergence #25）：只建航线与镜头贴近处的一条带，带外一栋不建
· **三条模数**：人类区开间 4 m / 层高 3.5 m / 门洞 2.4 m；**矮人区层高 2.8 m / 门洞 2.0 m**
  （这是画面上最可靠的识别特征，比任何材质变化都管用）；运河宽 12 m、堤高 4 m

纪律
----
· **blend 由本脚本确定性生成，不手改**（rule 4h ④）。改几何 ＝ 改脚本重跑。
· 只出**布局层**几何：零材质、零灯光（rule 4h §D1）。写实化是另一道 look pass。
· 资产替身（`ASSET_SLOTS`）先摆同包围盒的占位盒；`props/pN_*/whitemodel/pN_*.blend`
  一旦存在，`resolve_asset()` 自动换成真网格，**布局代码一个字都不用改**。
"""
from __future__ import annotations

import math
import os
import sys

import bpy
from mathutils import Vector

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DRAMA = os.path.join(REPO, "ai_videos", "shikong_lvxing", "sk2")
A = os.path.join(DRAMA, "2_世界观人设")
OUT_DIR = os.path.join(A, "scenes", "stormwind", "_blender")

CITY_SCALE = 0.5

# ── W1 的米制锚点（东, 北, 高），原点＝城门 ──────────────────────────
ANCHORS = {
    "城门_英雄谷":      (0.0, 0.0, 0.0),
    "贸易区南入口":     (-112.8, 141.1, -0.3),
    "旧城区中心":       (41.4, 292.6, 4.3),
    "暴风要塞入口":     (12.8, 471.8, 11.4),
    "要塞北端":         (-57.5, 636.5, 26.7),
    "矮人区水井":       (-164.1, 600.0, 1.6),
    "割喉小巷":         (-131.4, 470.7, 7.6),
    "教堂广场入口":     (-295.3, 381.9, 3.3),
    "光明大教堂入口":   (-342.6, 442.8, 12.3),
    "花园区中心":       (-559.5, 273.1, -3.0),
    "法师区水井":       (-465.2, 102.1, 22.2),
    "已宰的羔羊":       (-508.1, 73.9, 26.5),
    "巫师圣殿入口":     (-380.8, 32.3, 33.5),
    "监狱入口":         (-318.5, 199.4, 4.2),
}

# ── 走廊：只建这些折线两侧的带 ────────────────────────────────────
# 每条 = (名字, [锚点名...], 半径 m, 建筑等级)
#   等级 A = 真立面（贴身而过）· B = 体块+屋顶形制（中景）· C = 纯体块（远景剪影）
CORRIDORS = [
    ("入城主路", ["城门_英雄谷", "贸易区南入口"], 55, "A"),
    ("贸易区→旧城区", ["贸易区南入口", "旧城区中心"], 45, "A"),
    ("旧城区→要塞", ["旧城区中心", "暴风要塞入口"], 45, "B"),
    ("要塞→矮人区", ["暴风要塞入口", "矮人区水井"], 45, "B"),
    ("矮人区→教堂广场", ["矮人区水井", "割喉小巷", "教堂广场入口"], 45, "B"),
    ("教堂广场→花园区", ["教堂广场入口", "花园区中心"], 40, "B"),
    ("花园区→法师区", ["花园区中心", "法师区水井"], 40, "B"),
    ("法师区→贸易区", ["法师区水井", "监狱入口", "贸易区南入口"], 45, "A"),
]

# 运河折线（逆时针一圈，串起各区）
CANAL = ["贸易区南入口", "旧城区中心", "暴风要塞入口", "矮人区水井",
         "教堂广场入口", "花园区中心", "法师区水井", "监狱入口", "贸易区南入口"]
CANAL_W, CANAL_BANK_H = 12.0, 4.0

# ── 分区模数 ──────────────────────────────────────────────────────
MODULES = {
    "human": dict(bay=4.0, floor=3.5, door=2.4, floors=(2, 3)),
    "dwarf": dict(bay=4.0, floor=2.8, door=2.0, floors=(1, 2)),   # 层高压低＝识别特征
}
DWARF_ZONE = ("矮人区水井",)          # 这些锚点半径内用矮人模数
DWARF_R = 90.0

# ── 地标体块（名字, 锚点, 尺寸[东,北,高], 顶部形制） ───────────────
LANDMARKS = [
    ("暴风要塞", "要塞北端", (70, 90, 34), "keep"),
    ("光明大教堂", "光明大教堂入口", (46, 72, 58), "spires"),
    ("巫师圣殿", "巫师圣殿入口", (26, 26, 46), "tower"),
    ("监狱石堡", "监狱入口", (22, 22, 18), "clock"),
    ("金库石堡", None, (20, 20, 17), "clock"),      # 位置在监狱对岸，下面算
    ("地铁齿轮洞口", "矮人区水井", (14, 10, 14), "gear"),
]

# ── 资产替身槽（键, 锚点, 数量, 沿走廊间距 m, 包围盒[X,Y,Z]） ──────
ASSET_SLOTS = [
    ("p1", None, 0, 26.0, (0.45, 0.45, 3.6)),    # 街灯：沿所有走廊等距摆
    ("p6", None, 0, 70.0, (3.2, 3.2, 4.5)),      # 苹果树
    ("p19", "花园区中心", 1, 0.0, (5.0, 5.0, 3.2)),   # 月亮井
    ("p20", "监狱入口", 1, 0.0, (0.8, 0.8, 1.6)),     # 集合石
    ("p10", "矮人区水井", 1, 0.0, (6.0, 0.8, 6.0)),   # 地铁齿轮
    ("p22", "贸易区南入口", 2, 0.0, (2.2, 3.4, 2.4)), # 狮鹫
]


# ── 城墙 / 城门楼 / 南侧引道 ───────────────────────────────────────
# 原先这里只有 `ANCHORS["城门_英雄谷"]` 这**一个坐标锚点、零几何**，
# 于是 S01「镜头对准城门洞笔直穿过去」根本无处可穿（2026-09-19 用户看 previz 指出）。
# 墙线不硬编：从锚点包围盒外扩 WALL_MARGIN 推出来，南墙**穿过原点**（城门就在原点上）。
WALL_MARGIN = 55.0
WALL_H, WALL_T = 12.0, 4.0
MERLON_H, MERLON_W, MERLON_GAP = 1.5, 2.0, 2.0    # 方齿城垛（方齿，不是尖齿）
WALL_TOWER_STEP, WALL_TOWER_W = 96.0, 9.0
GATE_W, GATE_H = 12.0, 9.0          # 门洞**净宽 / 净高**——相机要从这中间飞过去
GATE_PIER_W, GATE_DEPTH = 10.0, 16.0
GATEHOUSE_H, GATE_TOWER_R = 20.0, 7.0
APPROACH_LEN, APPROACH_W = 180.0, 12.0


def wall_bounds():
    """墙心线的四至（米，缩放前）。南墙 y=0，正好压在城门锚点上。"""
    xs = [a[0] for a in ANCHORS.values()]
    ys = [a[1] for a in ANCHORS.values()]
    return (min(xs) - WALL_MARGIN, 0.0, max(xs) + WALL_MARGIN, max(ys) + WALL_MARGIN)


def inside_walls(x, y, inset=8.0):
    x0, y0, x1, y1 = wall_bounds()
    return (x0 + inset) < x < (x1 - inset) and (y0 + inset) < y < (y1 - inset)


def s(v):
    """坐标缩放（尺寸 1:1，坐标 ×CITY_SCALE）。"""
    return tuple(c * CITY_SCALE for c in v)


def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def coll(name):
    c = bpy.data.collections.get(name)
    if not c:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    return c


def box(name, loc, size, parent):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = (size[0], size[1], size[2])   # primitive size=1.0 立方体，直接乘目标尺寸
    # **只 apply scale**。不写全参数时这个 op 会把 location 一并烘进网格，
    # 之后再设一次 o.location 就等于把位置加了两次——全城物体都会跑到两倍远处，
    # 间距翻倍而尺寸不变，俯视看就是「一格实一格空」的棋盘 + 被拉稀的走廊。
    # （2026-09-19 实测：ground 瓦片 loc=-269.3 而包围盒中心在 -538.6）
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    for c in list(o.users_collection):
        c.objects.unlink(o)
    parent.objects.link(o)
    return o


def prism(name, loc, size, parent, verts=4, rot=0.0):
    """圆锥 / 棱锥顶，用来做蓝色尖顶母题的体块。"""
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=size[0] / 2.0,
                                    depth=size[2], location=loc, rotation=(0, 0, rot))
    o = bpy.context.active_object
    o.name = name
    o.scale = (1.0, size[1] / size[0] if size[0] else 1.0, 1.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)   # 同上，只吃 scale
    for c in list(o.users_collection):
        c.objects.unlink(o)
    parent.objects.link(o)
    return o


def polyline(pts):
    return [ANCHORS[p] for p in pts]


def lerp(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def seg_points(pts, step):
    """沿折线按 step（米，缩放前）取点，返回 (位置, 切向角)。"""
    out = []
    for a, b in zip(pts, pts[1:]):
        d = math.dist(a[:2], b[:2])
        if d < 1e-6:
            continue
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        n = max(1, int(d // step))
        for i in range(n):
            out.append((lerp(a, b, i / n), ang))
    return out


def in_dwarf(p):
    for k in DWARF_ZONE:
        a = ANCHORS[k]
        if math.dist(p[:2], a[:2]) < DWARF_R:
            return True
    return False


def build_ground(root):
    # 地面必须盖住城墙外沿与**整条南侧引道**（引道南端 y=-180 是 S01 的起幅点），
    # 否则开场那几秒是悬在黑里的路面。按墙线推，不按锚点包围盒推。
    x0, y0, x1, y1 = wall_bounds()
    lo_x, hi_x = x0 - 60.0, x1 + 60.0
    lo_y, hi_y = y0 - APPROACH_LEN - 70.0, y1 + 60.0
    cx, cy = (lo_x + hi_x) / 2, (lo_y + hi_y) / 2
    w, h = hi_x - lo_x, hi_y - lo_y
    # 分块铺地：一整块巨型四边形的四个顶点会同时落在相机远裁剪面之外而被整块裁掉，
    # 画面就只剩近处建筑悬在黑里（2026-09-19 实测）。切成网格后总有近处的块在视锥内。
    nx = ny = 12
    tw, th = w / nx, h / ny
    for i in range(nx):
        for j in range(ny):
            tx = cx - w / 2 + tw * (i + 0.5)
            ty = cy - h / 2 + th * (j + 0.5)
            # 放大 2% 相互叠压：几何上本应严丝合缝，但渲染出来仍有规则黑缝，
            # 与其继续追根因，不如用零代价的重叠把它焊死（地面只作 previz 地平面）
            box(f"G_ground_{i:02d}_{j:02d}", s((tx, ty, -1.0)),
                s((tw * 1.01, th * 1.01, 2.0)), root)
    return None


def build_canal(root):
    pts = polyline(CANAL)
    for i, (p, ang) in enumerate(seg_points(pts, 24.0)):
        # 水面
        box(f"G_canal_water_{i:03d}", s((p[0], p[1], p[2] - CANAL_BANK_H + 0.4)),
            s((26.0, CANAL_W, 0.8)), root).rotation_euler = (0, 0, ang)
        # 两侧护岸
        for sgn in (-1, 1):
            off = (CANAL_W / 2 + 1.6) * sgn
            bx = p[0] + math.sin(ang) * -off
            by = p[1] + math.cos(ang) * off
            o = box(f"G_canal_bank_{i:03d}_{'L' if sgn < 0 else 'R'}",
                    s((bx, by, p[2] - CANAL_BANK_H / 2)), s((26.0, 3.2, CANAL_BANK_H)), root)
            o.rotation_euler = (0, 0, ang)


_ALL_CENTERLINES = None


def all_centerlines():
    """所有走廊的中心线采样点（缩放前）。用来防止走廊互相压街。"""
    global _ALL_CENTERLINES
    if _ALL_CENTERLINES is None:
        out = []
        for nm, names, _r, _g in CORRIDORS:
            out += [(pt, nm) for pt, _a in seg_points(polyline(names), 10.0)]
        _ALL_CENTERLINES = out
    return _ALL_CENTERLINES


def blocks_other_street(x, y, own_name, clear=13.0):
    """这个位置会不会压到**别的**走廊的街心？会就别放楼。

    两条走廊在同一个锚点交汇时（如贸易区），各自的街墙会盖到对方的街面上，
    相机站在街心也会贴着墙（2026-09-19 实测 shot08 整片灰）。
    """
    for (px, py, _pz), nm in all_centerlines():
        if nm == own_name:
            continue
        if math.dist((x, y), (px, py)) < clear:
            return True
    return False


def build_corridor(root, name, pts, radius, grade):
    """沿走廊砌**连续的街墙**：贴街一排密排不留缝，后面再加一到两排进深，
    并在中轴铺出街面。原来每侧只摆一排、还按 14–20 m 跳着放，
    俯视看就是几条虚线——不像城，像示意图（2026-09-19 用户指出）。"""
    mod_key = "dwarf"
    # 贴街第一排的开间：按模数走，密排（step ＝ 开间宽，相邻建筑共墙）
    bay_w = 12.0                      # 一栋贴街建筑的面宽（3 个 4 m 开间）
    rows = {"A": 3, "B": 2, "C": 1}[grade]
    depth0 = 11.0
    # 主干道要真的宽：W1 记的英雄谷石桥「可容马车并行」，贸易区是全城最开阔处。
    # 16 m 的街在 0.5 比例下只有 8 个单位，28° 镜头里两侧全是墙，读不出街景。
    street_w = {"A": 34.0, "B": 22.0, "C": 14.0}[grade]

    # 街面
    for i, (p, ang) in enumerate(seg_points(pts, 18.0)):
        st = box(f"S_{name}_{i:03d}", s((p[0], p[1], max(0.0, p[2]) + 0.06)),
                 s((19.0, street_w, 0.12)), root)   # 街面随街宽
        st.rotation_euler = (0, 0, ang)

    for i, (p, ang) in enumerate(seg_points(pts, bay_w)):
        mod = MODULES["dwarf" if in_dwarf(p) else "human"]
        for sgn in (-1, 1):
            for r in range(rows):
                # 第一排贴街，后排逐层退后
                off = street_w / 2 + depth0 / 2 + r * (depth0 + 1.5)
                off *= sgn
                bx = p[0] + math.sin(ang) * -off
                by = p[1] + math.cos(ang) * off
                # 高度按排数递减 + 用位置做确定性抖动，避免整排等高像一堵墙
                jitter = ((i * 7 + r * 13 + (0 if sgn < 0 else 5)) % 3)
                nf = max(1, mod["floors"][1] - r) + (1 if jitter == 2 else 0)
                bh = mod["floor"] * nf
                w = bay_w * (0.92 + 0.06 * jitter)
                if blocks_other_street(bx, by, name):
                    continue
                # 墙外不建。入城主路的第 0 个采样点就在城门上，
                # 不挡的话一排楼会砌到南墙外侧、挡在引道尽头（S01 全程看得见）
                if not inside_walls(bx, by):
                    continue
                tag = f"{name}_{i:03d}_{'L' if sgn < 0 else 'R'}_{r}"
                # 底落到地面：p[2] 是锚点高程，地面在 0，不补齐就整排悬空
                base_z = max(0.0, p[2])
                total_h = bh + base_z
                body = box(f"B_{grade}_{tag}", s((bx, by, total_h / 2)),
                           s((w, depth0, total_h)), root)
                body.rotation_euler = (0, 0, ang)
                # 屋顶：贴街两排给形制（蓝色尖顶母题），最外排只给体块
                if r < 2:
                    rh = 3.6 + 0.4 * jitter
                    roof = prism(f"R_{grade}_{tag}", s((bx, by, total_h + rh / 2)),
                                 s((w * 1.04, depth0 * 1.04, rh)), root, verts=4)
                    roof.rotation_euler = (0, 0, ang + math.pi / 4)


def build_infill(root):
    """走廊之间的街区填充（只给远景剪影用，不做形制）。

    走廊制的前提是「镜头看不到的不建」（rule 4g ④）。sk1 能用纯走廊制，是因为它
    **取消了俯视全城的镜头**（sk1 divergence #26）。本片不同：**S01 / S02 是航拍扫全城**，
    那两镜会直接拍到环内的空地。所以这里补一层低精度体块——只有体量与屋顶轮廓，
    没有门窗、没有材质，贴身镜头永远不会走到它们跟前。
    """
    pts = [ANCHORS[k] for k in CANAL]
    # 用走廊折线算出城区的凸形范围，在其内部按网格撒体块，离走廊太近的跳过（那儿已有街墙）
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    corridor_pts = []
    for _n, names, _r, _g in CORRIDORS:
        corridor_pts += [pt for pt, _a in seg_points(polyline(names), 16.0)]

    step = 26.0
    n = 0
    x = min(xs)
    while x <= max(xs):
        y = min(ys)
        while y <= max(ys):
            # 只在多边形内部（用「到各锚点的最近距离」粗判，够远景用）
            d_anchor = min(math.dist((x, y), (a[0], a[1])) for a in ANCHORS.values())
            d_corr = min((math.dist((x, y), (c[0], c[1])) for c in corridor_pts), default=1e9)
            if d_anchor < 210 and d_corr > 34:
                j = (int(x / step) * 7 + int(y / step) * 13) % 5
                nf = 2 + (j % 3)
                bh = 3.5 * nf
                w, dpt = 13.0 + j, 12.0 + (j % 3) * 2
                z = 0.0
                box(f"F_infill_{n:04d}", s((x, y, z + bh / 2)), s((w, dpt, bh)), root)
                if j % 2 == 0:
                    prism(f"F_infillroof_{n:04d}", s((x, y, z + bh + 2.0)),
                          s((w * 1.05, dpt * 1.05, 4.0)), root, verts=4)
                n += 1
            y += step
        x += step
    return n


def build_wall_run(root, tag, x0, y0, x1, y1):
    """一段直墙：墙体 + 墙顶方齿 + 定距方塔。端点是墙心线的两端（米，缩放前）。"""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    if L < 1e-6:
        return 0
    ang = math.atan2(dy, dx)
    n_obj = 0
    body = box(f"W_wall_{tag}", s(((x0 + x1) / 2, (y0 + y1) / 2, WALL_H / 2)),
               s((L, WALL_T, WALL_H)), root)
    body.rotation_euler = (0, 0, ang)
    n_obj += 1
    step = MERLON_W + MERLON_GAP
    n = max(1, int(L // step))
    for i in range(n):
        t = (i + 0.5) / n
        m = box(f"W_wall_{tag}_m{i:03d}",
                s((x0 + dx * t, y0 + dy * t, WALL_H + MERLON_H / 2)),
                s((MERLON_W, WALL_T, MERLON_H)), root)
        m.rotation_euler = (0, 0, ang)
        n_obj += 1
    nt = max(1, int(L // WALL_TOWER_STEP))
    for i in range(nt):
        t = (i + 0.5) / nt
        tx, ty = x0 + dx * t, y0 + dy * t
        th = WALL_H + 7.0
        o = box(f"W_wall_{tag}_t{i:02d}", s((tx, ty, th / 2)),
                s((WALL_TOWER_W, WALL_TOWER_W, th)), root)
        o.rotation_euler = (0, 0, ang)
        cap = box(f"W_wall_{tag}_tcap{i:02d}", s((tx, ty, th + MERLON_H / 2)),
                  s((WALL_TOWER_W * 1.18, WALL_TOWER_W * 1.18, MERLON_H)), root)
        cap.rotation_euler = (0, 0, ang)
        n_obj += 2
    return n_obj


def build_walls(root):
    """城区外缘一圈城墙。南墙在城门左右断开，把口子让给城门楼。"""
    x0, y0, x1, y1 = wall_bounds()
    gate_half = GATE_W / 2 + GATE_PIER_W + 2 * GATE_TOWER_R      # 门楼总半宽 ＝ 30 m
    n = 0
    n += build_wall_run(root, "S_L", x0, y0, -gate_half, y0)
    n += build_wall_run(root, "S_R", gate_half, y0, x1, y0)
    n += build_wall_run(root, "N", x0, y1, x1, y1)
    n += build_wall_run(root, "W", x0, y0, x0, y1)
    n += build_wall_run(root, "E", x1, y0, x1, y1)
    return n


def build_gatehouse(root):
    """跨在原点上的城门楼。**左右墩子 + 上方过梁，中间是真正贯通的门洞**——
    绝不能拿一整块实心体当门楼，S01 的相机要从门洞净空里飞过去。"""
    half = GATE_W / 2.0
    n = 0
    for sgn in (-1, 1):
        box(f"W_gate_pier_{'L' if sgn < 0 else 'R'}",
            s((sgn * (half + GATE_PIER_W / 2), 0.0, GATE_H / 2)),
            s((GATE_PIER_W, GATE_DEPTH, GATE_H)), root)
        n += 1
    span = GATE_W + 2 * GATE_PIER_W
    lin_h = GATEHOUSE_H - GATE_H
    box("W_gate_lintel", s((0.0, 0.0, GATE_H + lin_h / 2)),
        s((span, GATE_DEPTH, lin_h)), root)
    n += 1
    step = MERLON_W + MERLON_GAP
    for i in range(int(span // step)):
        box(f"W_gate_m{i:02d}", s((-span / 2 + step * (i + 0.5), 0.0,
                                   GATEHOUSE_H + MERLON_H / 2)),
            s((MERLON_W, GATE_DEPTH, MERLON_H)), root)
        n += 1
    for sgn in (-1, 1):
        tx = sgn * (half + GATE_PIER_W + GATE_TOWER_R)
        th = GATEHOUSE_H + 8.0
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16, radius=GATE_TOWER_R * CITY_SCALE, depth=th * CITY_SCALE,
            location=s((tx, 0.0, th / 2)))
        o = bpy.context.active_object
        o.name = f"W_gate_tower_{'L' if sgn < 0 else 'R'}"
        for c in list(o.users_collection):
            c.objects.unlink(o)
        root.objects.link(o)
        prism(f"W_gate_towercap_{'L' if sgn < 0 else 'R'}", s((tx, 0.0, th + 3.0)),
              s((GATE_TOWER_R * 2.4, GATE_TOWER_R * 2.4, 6.0)), root, verts=12)
        n += 2
    return n


def build_approach(root):
    """南侧引道：自城门向南 APPROACH_LEN 的石板道 + 两侧巨像**基座**与矮墩 + 夹道林带。

    · 基座只有基座：巨像本体在城内的英雄谷（`build_heroes_vale`），不在两处重复摆。
    · 林带是 S01 起幅高度的唯一参照（「在引道南端上空、树冠高度」），树冠顶 16–20 m。
    """
    n = 0
    seg = 20.0
    for i in range(int(APPROACH_LEN // seg)):
        box(f"W_appr_road_{i:02d}", s((0.0, -seg * (i + 0.5), 0.15)),
            s((APPROACH_W, seg * 1.02, 0.5)), root)
        n += 1
    for i, y in enumerate((-34.0, -72.0, -110.0, -148.0)):
        for sgn in (-1, 1):
            box(f"W_appr_plinth_{i}_{'L' if sgn < 0 else 'R'}",
                s((sgn * 13.0, y, 1.8)), s((7.0, 7.0, 3.6)), root)
            box(f"W_appr_plinthtop_{i}_{'L' if sgn < 0 else 'R'}",
                s((sgn * 13.0, y, 3.6 + 0.5)), s((8.0, 8.0, 1.0)), root)
            n += 2
    y, k = -8.0, 0
    while y > -APPROACH_LEN:
        for sgn in (-1, 1):
            box(f"W_appr_bollard_{k:02d}_{'L' if sgn < 0 else 'R'}",
                s((sgn * 7.5, y, 0.5)), s((1.2, 1.2, 1.0)), root)
            n += 1
        y -= 14.0
        k += 1
    y, k = -16.0, 0
    while y > -APPROACH_LEN - 20.0:
        for sgn in (-1, 1):
            for row in range(2):
                tx = sgn * (24.0 + row * 16.0)
                th = 16.0 + ((k * 7 + row * 5) % 3) * 2.0
                trunk = th * 0.35
                box(f"W_tree_t{k:02d}_{row}_{'L' if sgn < 0 else 'R'}",
                    s((tx, y, trunk / 2)), s((1.2, 1.2, trunk)), root)
                prism(f"W_tree_c{k:02d}_{row}_{'L' if sgn < 0 else 'R'}",
                      s((tx, y, trunk + (th - trunk) / 2)),
                      s((9.0, 9.0, th - trunk)), root, verts=6)
                n += 2
        y -= 22.0
        k += 1
    return n


def build_heroes_vale(root):
    """英雄谷的巨像：沿入城主路中轴夹道排开（S01 出洞后「巨像依次从两侧掠过」、
    S04「走过前两尊巨像」）。横向 13.5 m ＜ 街半宽 17 m，不与街墙互穿。"""
    a, b = ANCHORS["城门_英雄谷"], ANCHORS["贸易区南入口"]
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    nx, ny = -math.sin(ang), math.cos(ang)
    n = 0
    for i in range(5):
        along = 26.0 + i * 30.0
        px, py = a[0] + math.cos(ang) * along, a[1] + math.sin(ang) * along
        for sgn in (-1, 1):
            bx, by = px + nx * 13.5 * sgn, py + ny * 13.5 * sgn
            tag = f"{i}_{'L' if sgn < 0 else 'R'}"
            for nm, z, size in (("base", 3.0, (6.0, 6.0, 6.0)),
                                ("body", 6.0 + 5.5, (3.2, 2.4, 11.0))):
                o = box(f"L_colossus_{nm}_{tag}", s((bx, by, z)), s(size), root)
                o.rotation_euler = (0, 0, ang)
                n += 1
            h = prism(f"L_colossus_head_{tag}", s((bx, by, 17.5 + 1.1)),
                      s((2.2, 2.2, 2.2)), root, verts=8)
            h.rotation_euler = (0, 0, ang)
            n += 1
    return n


def build_landmarks(root):
    # 金库在监狱对岸：沿运河法线偏移
    pris = ANCHORS["监狱入口"]
    vault = (pris[0] - 34.0, pris[1] + 16.0, pris[2])
    for name, anchor, size, kind in LANDMARKS:
        base = ANCHORS[anchor] if anchor else vault
        if kind == "gear":
            base = (base[0] + 52.0, base[1] - 22.0, base[2])
        loc = s((base[0], base[1], base[2] + size[2] / 2))
        o = box(f"L_{name}", loc, s(size), root)
        top = base[2] + size[2]
        # W1 的锚点带高程，而地面是平的：不补基座地标就会悬在半空
        # （2026-09-19 用户指出要塞飘着）。从锚点高程砌到地面，兼作台基。
        if base[2] > 0.5:
            box(f"L_{name}_plinth", s((base[0], base[1], base[2] / 2)),
                s((size[0] * 1.12, size[1] * 1.12, base[2])), root)
        if kind == "spires":
            # 尖塔森林：中心最高、四周渐低
            for k, (dx, dy, hh) in enumerate([(0, 0, 26), (-12, -18, 17), (12, -18, 17),
                                              (-15, 14, 13), (15, 14, 13), (0, 26, 11)]):
                prism(f"L_{name}_spire{k}", s((base[0] + dx, base[1] + dy, top + hh / 2)),
                      s((7.0, 7.0, hh)), root, verts=8)
        elif kind == "tower":
            prism(f"L_{name}_cap", s((base[0], base[1], top + 9.0)), s((22.0, 22.0, 18.0)),
                  root, verts=12)
        elif kind == "keep":
            for k, (dx, dy) in enumerate([(-28, -34), (28, -34), (-28, 34), (28, 34)]):
                box(f"L_{name}_tower{k}", s((base[0] + dx, base[1] + dy, base[2] + 22)),
                    s((13, 13, 44)), root)
                prism(f"L_{name}_towercap{k}", s((base[0] + dx, base[1] + dy, base[2] + 44 + 5)),
                      s((14, 14, 10)), root, verts=8)
        elif kind == "clock":
            box(f"L_{name}_clocktower", s((base[0], base[1], top + 7.0)), s((7, 7, 14)), root)
            prism(f"L_{name}_clockcap", s((base[0], base[1], top + 14 + 2.5)),
                  s((8, 8, 5)), root, verts=8)
        elif kind == "gear":
            bpy.ops.mesh.primitive_torus_add(
                major_radius=3.0 * CITY_SCALE, minor_radius=0.4 * CITY_SCALE,
                location=s((base[0], base[1], base[2] + 7.0)),
                rotation=(math.pi / 2, 0, 0))
            g = bpy.context.active_object
            g.name = f"L_{name}_gear"
            for c in list(g.users_collection):
                c.objects.unlink(g)
            root.objects.link(g)


def resolve_asset(key):
    """白模存在就返回路径，否则 None（布局层用同包围盒占位盒）。"""
    props = os.path.join(A, "props")
    if not os.path.isdir(props):
        return None
    for d in os.listdir(props):
        if d.split("_")[0] == key:
            wm = os.path.join(props, d, "whitemodel", f"{d}.blend")
            if os.path.isfile(wm):
                return wm
    return None


_ASSET_CACHE = {}


def load_asset_mesh(key):
    """把 whitemodel/{name}.blend 里的网格 append 进来，返回一个可复制的源物体。"""
    if key in _ASSET_CACHE:
        return _ASSET_CACHE[key]
    path = resolve_asset(key)
    if not path:
        _ASSET_CACHE[key] = None
        return None
    before = set(bpy.data.objects)
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.objects = [n for n in src.objects]
    new_objs = [o for o in set(bpy.data.objects) - before if o.type == "MESH"]
    if not new_objs:
        _ASSET_CACHE[key] = None
        return None
    # 多块就合成一个父级空物体，整组一起复制
    if len(new_objs) == 1:
        srcobj = new_objs[0]
    else:
        bpy.context.scene.collection.objects.link(new_objs[0]) if new_objs[0].name not in bpy.context.scene.objects else None
        srcobj = new_objs[0]
        for o in new_objs[1:]:
            o.parent = srcobj
    for o in new_objs:
        o.hide_render = True            # 源件只作模板，不入画
        if o.name not in bpy.context.scene.objects:
            bpy.context.scene.collection.objects.link(o)
    # **把模板挪出世界**。append 进来的源件停在各自 whitemodel 里的原点附近，
    # 也就是正压在城门洞与英雄谷上。hide_render 只让它们不入画，**射线照样打得到**：
    # previz 的 `find_clear_cam()` 会把这团看不见的东西当成挡视线的实体
    # （2026-09-19 实测：沿 x=0 穿门的射线全被 p10 齿轮挡下）。挪走不影响
    # `place_asset()`——它复制后会显式设 location，而 `dimensions` 与位置无关。
    srcobj.location = (0.0, 0.0, -2000.0)
    _ASSET_CACHE[key] = srcobj
    return srcobj


# 只有「独一份的地标道具」用真网格。重复街具（街灯 ×142、苹果树 ×48）用占位盒——
# 它们加起来约四百万顶点，会把 previz 从每帧零点几秒压到十秒以上（2026-09-19 实测：
# 十分钟渲不完一镜的前十帧），而 previz 要的是**机位与体量**，不是街灯的倒角。
# 出片不经过这个 blend，所以这里省下的精度不影响画面。
REAL_MESH_KEYS = {"p19", "p20", "p10", "p22"}


def place_asset(key, name, loc, bbox, parent):
    """地标道具复制真网格并按包围盒缩放归位；重复街具摆同尺寸占位盒。"""
    if key not in REAL_MESH_KEYS:
        return box(name, loc, bbox, parent), False
    src = load_asset_mesh(key)
    if src is None:
        return box(name, loc, bbox, parent), False
    o = src.copy()
    o.data = src.data.copy()
    o.name = name
    o.hide_render = False
    dim = [max(1e-6, d) for d in src.dimensions]
    o.scale = tuple(bbox[i] / dim[i] for i in range(3))
    o.location = loc
    parent.objects.link(o)
    return o, True


def build_assets(root):
    placed = 0
    for key, anchor, count, step, bbox in ASSET_SLOTS:
        real = resolve_asset(key)
        tag = "M" if real else "P"      # M=真网格, P=占位盒
        if anchor:
            base = ANCHORS[anchor]
            for i in range(max(1, count)):
                ang = 2 * math.pi * i / max(1, count)
                loc = s((base[0] + math.cos(ang) * 12, base[1] + math.sin(ang) * 12,
                         base[2] + bbox[2] / 2))
                place_asset(key, f"A_{tag}_{key}_{i:02d}", loc, s(bbox), root)
                placed += 1
        else:
            for cname, names, radius, grade in CORRIDORS:
                pts = polyline(names)
                for i, (p, ang) in enumerate(seg_points(pts, step)):
                    off = radius * 0.30
                    for sgn in (-1, 1):
                        bx = p[0] + math.sin(ang) * -off * sgn
                        by = p[1] + math.cos(ang) * off * sgn
                        place_asset(key, f"A_{tag}_{key}_{cname}_{i:03d}_{sgn}",
                                    s((bx, by, p[2] + bbox[2] / 2)), s(bbox), root)
                        placed += 1
    return placed


def render_checks():
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.render.resolution_x, sc.render.resolution_y = 1600, 900
    sc.render.film_transparent = False
    try:
        sh = sc.display.shading
        sh.light = "STUDIO"
        sh.show_shadows = False
        sh.show_cavity = False
    except Exception:
        pass
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    xs = [o.location.x for o in objs]
    ys = [o.location.y for o in objs]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    ar = sc.render.resolution_x / sc.render.resolution_y
    span = max((max(xs) - min(xs)) * 1.15, (max(ys) - min(ys)) * ar * 1.15)

    def shoot(name, loc, rot, ortho=None):
        cam_d = bpy.data.cameras.new(name)
        cam = bpy.data.objects.new(name, cam_d)
        bpy.context.scene.collection.objects.link(cam)
        cam.location, cam.rotation_euler = loc, rot
        if ortho:
            cam_d.type, cam_d.ortho_scale = "ORTHO", ortho
        sc.camera = cam
        sc.render.filepath = os.path.join(OUT_DIR, name + ".png")
        bpy.ops.render.render(write_still=True)

    shoot("check_plan", (cx, cy, 420), (0, 0, 0), ortho=span)
    shoot("check_persp", (cx + span * 0.85, cy - span * 0.95, span * 0.55),
          (math.radians(60), 0, math.radians(42)))


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    os.makedirs(OUT_DIR, exist_ok=True)
    clear()
    root = coll("stormwind_layout")
    build_ground(root)
    build_canal(root)
    for name, names, radius, grade in CORRIDORS:
        build_corridor(root, name, polyline(names), radius, grade)
    n_infill = build_infill(root)
    n_wall = build_walls(root)
    n_gate = build_gatehouse(root)
    n_appr = build_approach(root)
    n_col = build_heroes_vale(root)
    build_landmarks(root)
    n_assets = build_assets(root)

    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    xs = [o.location.x for o in objs]
    ys = [o.location.y for o in objs]
    zs = [o.location.z for o in objs]
    x0, y0, x1, y1 = wall_bounds()
    print(f"[stormwind] 物体 {len(objs)} 个（资产槽 {n_assets}，街区填充 {n_infill}，"
          f"城墙 {n_wall}，城门楼 {n_gate}，引道 {n_appr}，巨像 {n_col}）")
    print(f"[stormwind] 墙心线 东 {x0:.1f}~{x1:.1f} / 北 {y0:.1f}~{y1:.1f} m；"
          f"门洞净宽 {GATE_W} m × 净高 {GATE_H} m（x ±{GATE_W/2}，y ±{GATE_DEPTH/2}）")
    print(f"[stormwind] 包围盒 东 {min(xs):.1f}~{max(xs):.1f} / "
          f"北 {min(ys):.1f}~{max(ys):.1f} / 高 {min(zs):.1f}~{max(zs):.1f} m（已按 {CITY_SCALE} 比例）")

    blend = os.path.join(OUT_DIR, "stormwind.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    print(f"[stormwind] 已存 {blend}")
    render_checks()
    print("[stormwind] 校验图已出：check_plan.png / check_persp.png")


main()
