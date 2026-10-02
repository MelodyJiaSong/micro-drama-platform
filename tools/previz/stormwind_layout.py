# -*- coding: utf-8 -*-
"""暴风城（sk2）城市布局的**纯几何**层 —— 不依赖 bpy。

`tools/build_stormwind.py` 从这里取锚点、走廊、运河、城墙与**逐栋建筑落位**去建 blend；
`tools/shot_plan.py` 从这里取同一批数去画航线图的城市层。**一份东西只有一个出处**
（rule 4i ①）——改布局改这里，blend 与俯视图一起变，不会各画各的。

坐标一律是**缩放前的米，原点＝城门**（南墙 y=0 压在城门锚点上，+Y 进城/北）。
`tools/previz_gate_sk2.py` 的机位表用的是同一个原点、同为 1:1，两者可直接叠。
建 blend 时坐标再乘 `CITY_SCALE`（尺寸不缩），画图时不乘。
"""
from __future__ import annotations

import math

CITY_SCALE = 0.5

# ── W1 的米制锚点（东, 北, 高），原点＝城门 ──────────────────────────
ANCHORS: dict[str, tuple[float, float, float]] = {
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

WALL_MARGIN = 55.0
WALL_H, WALL_T = 12.0, 4.0
MERLON_H, MERLON_W, MERLON_GAP = 1.5, 2.0, 2.0    # 方齿城垛（方齿，不是尖齿）
WALL_TOWER_STEP, WALL_TOWER_W = 96.0, 9.0
GATE_W, GATE_H = 12.0, 9.0          # 门洞**净宽 / 净高**——相机要从这中间飞过去
GATE_PIER_W, GATE_DEPTH = 10.0, 16.0
GATEHOUSE_H, GATE_TOWER_R = 20.0, 7.0
APPROACH_LEN, APPROACH_W = 180.0, 12.0

# 街墙参数（`corridor_footprints` 与 `build_corridor` 共用）
BAY_W = 12.0                                          # 一栋贴街建筑的面宽（3 个 4 m 开间）
ROWS = {"A": 3, "B": 2, "C": 1}
DEPTH0 = 11.0
STREET_W = {"A": 34.0, "B": 22.0, "C": 14.0}
INFILL_STEP = 26.0


def wall_bounds():
    """墙心线的四至（米，缩放前）。南墙 y=0，正好压在城门锚点上。"""
    xs = [a[0] for a in ANCHORS.values()]
    ys = [a[1] for a in ANCHORS.values()]
    return (min(xs) - WALL_MARGIN, 0.0, max(xs) + WALL_MARGIN, max(ys) + WALL_MARGIN)


def inside_walls(x, y, inset=8.0):
    x0, y0, x1, y1 = wall_bounds()
    return (x0 + inset) < x < (x1 - inset) and (y0 + inset) < y < (y1 - inset)


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
    """这个位置会不会压到**别的**走廊的街心？会就别放楼。"""
    for (px, py, _pz), nm in all_centerlines():
        if nm == own_name:
            continue
        if math.dist((x, y), (px, py)) < clear:
            return True
    return False


def street_plates(name, pts, grade):
    """街面板：(中心 xyz, 尺寸 xyz, 转角)。"""
    street_w = STREET_W[grade]
    return [((p[0], p[1], max(0.0, p[2]) + 0.06), (19.0, street_w, 0.12), ang)
            for p, ang in seg_points(pts, 18.0)]


def corridor_footprints(name, pts, grade):
    """一条走廊两侧的**逐栋**街墙建筑。

    返回 [(中心 x, 中心 y, 面宽 w, 进深 d, 转角 rad, 总高, 有无屋顶形制)]，
    缩放前米制。`build_stormwind.build_corridor` 与航线图的城市层都读这一份。
    """
    rows = ROWS[grade]
    street_w = STREET_W[grade]
    out = []
    for i, (p, ang) in enumerate(seg_points(pts, BAY_W)):
        mod = MODULES["dwarf" if in_dwarf(p) else "human"]
        for sgn in (-1, 1):
            for r in range(rows):
                off = (street_w / 2 + DEPTH0 / 2 + r * (DEPTH0 + 1.5)) * sgn
                bx = p[0] + math.sin(ang) * -off
                by = p[1] + math.cos(ang) * off
                jitter = ((i * 7 + r * 13 + (0 if sgn < 0 else 5)) % 3)
                nf = max(1, mod["floors"][1] - r) + (1 if jitter == 2 else 0)
                bh = mod["floor"] * nf
                w = BAY_W * (0.92 + 0.06 * jitter)
                if blocks_other_street(bx, by, name):
                    continue
                if not inside_walls(bx, by):
                    continue
                out.append((bx, by, w, DEPTH0, ang, bh + max(0.0, p[2]), r < 2))
    return out


def infill_footprints():
    """走廊之间的街区填充体块（只给远景剪影用）。返回 [(x, y, w, d, 高)]。"""
    pts = [ANCHORS[k] for k in CANAL]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    corridor_pts = []
    for _n, names, _r, _g in CORRIDORS:
        corridor_pts += [pt for pt, _a in seg_points(polyline(names), 16.0)]

    out = []
    x = min(xs)
    while x <= max(xs):
        y = min(ys)
        while y <= max(ys):
            d_anchor = min(math.dist((x, y), (a[0], a[1])) for a in ANCHORS.values())
            d_corr = min((math.dist((x, y), (c[0], c[1])) for c in corridor_pts), default=1e9)
            if d_anchor < 210 and d_corr > 34:
                j = (int(x / INFILL_STEP) * 7 + int(y / INFILL_STEP) * 13) % 5
                nf = 2 + (j % 3)
                out.append((x, y, 13.0 + j, 12.0 + (j % 3) * 2, 3.5 * nf))
            y += INFILL_STEP
        x += INFILL_STEP
    return out


def landmark_base(anchor, kind):
    """地标底面中心（缩放前米）。金库在监狱对岸沿运河法线偏移；齿轮洞口再偏一次。"""
    pris = ANCHORS["监狱入口"]
    base = ANCHORS[anchor] if anchor else (pris[0] - 34.0, pris[1] + 16.0, pris[2])
    if kind == "gear":
        base = (base[0] + 52.0, base[1] - 22.0, base[2])
    return base


def landmark_boxes():
    """地标体块：[(名字, x, y, 东西宽, 南北深, 高)]，缩放前米制。"""
    return [(nm, *landmark_base(anchor, kind)[:2], float(sx), float(sy), float(sz))
            for nm, anchor, (sx, sy, sz), kind in LANDMARKS]
