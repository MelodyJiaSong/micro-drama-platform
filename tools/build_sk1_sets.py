# -*- coding: utf-8 -*-
"""Build the sk1 small previz sets (套景) — deterministic geometry, one .blend per set.

Sets are the scene-card spaces that are not in the city blend (rule 4g ③ keeps ONE copy of each
geometry: a set exists only here, and every shot that needs it appends / links it). Geometry only —
no materials, no lights, no cameras. Local frame per set: metres, +Z up, floor top z = 0, front of
the main furniture faces −Y unless the set says otherwise.

Output: `scenes/bianjing/_blender/sets/{name}.blend`, one collection `SET_{name}` (a blend may hold
extra `SET_*` variant collections). `--stills` also writes `sets/check_{name}.png` (workbench grey).

Run (repo root):
  blender -b --factory-startup --python tools/build_sk1_sets.py -- [--only NAME ...] [--stills]
"""
from __future__ import annotations

import argparse
import hashlib
import math
import random
import sys
from array import array
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_bianjing as bj  # noqa: E402
from build_bianjing import Batch, extrude, gable, railing, seg_quad, slab, steps, steps_x, timber_hall  # noqa: E402

SETS_DIR = bj.BLENDER_DIR / "sets"


@dataclass(frozen=True)
class CheckView:
    pos: tuple[float, float, float]
    target: tuple[float, float, float]
    lens: float


def fin(b: Batch, name: str, col: str) -> None:
    b.finish(name, col)


def legs(b: Batch, x0: float, x1: float, y0: float, y1: float, h: float, t: float = 0.06) -> None:
    for x in (x0 + t / 2, x1 - t / 2):
        for y in (y0 + t / 2, y1 - t / 2):
            b.cbox((x, y, h / 2), (t, t, h))


def table(b: Batch, cx: float, cy: float, lx: float, ly: float, h: float) -> None:
    slab(b, cx - lx / 2, cx + lx / 2, cy - ly / 2, cy + ly / 2, h - 0.05, h)
    legs(b, cx - lx / 2 + 0.03, cx + lx / 2 - 0.03, cy - ly / 2 + 0.03, cy + ly / 2 - 0.03, h - 0.05)


def chair(b: Batch, cx: float, cy: float, facing: str, seat: float = 0.45) -> None:
    """靠背椅：facing 为坐下后人脸朝向（N/S/E/W），靠背在背后。"""
    table(b, cx, cy, 0.45, 0.45, seat)
    back = {"N": (0.0, -0.21), "S": (0.0, 0.21), "E": (-0.21, 0.0), "W": (0.21, 0.0)}[facing]
    bx, by = cx + back[0], cy + back[1]
    wide_x = facing in "NS"
    b.cbox((bx, by, seat + 0.28), (0.45 if wide_x else 0.04, 0.04 if wide_x else 0.45, 0.5))


def tree(b: Batch, x: float, y: float, z0: float, h: float, crown: float, trunk: float = 0.2) -> None:
    b.cyl(x, y, z0, z0 + h - crown, trunk, 6)
    b.ball((x, y, z0 + h - crown), crown)


def house(b: Batch, x0: float, x1: float, y0: float, y1: float, eave: float, ridge: float, ridge_axis: str = "x") -> None:
    slab(b, x0, x1, y0, y1, 0.0, eave)
    gable(b, x0 - 0.4, x1 + 0.4, y0 - 0.4, y1 + 0.4, eave, ridge, ridge_axis)


# ── 1 客店房间（bg7-2 日 / bg14 夜：同一间房；S07 S08 S33 S34）─────────────────────────────
def set_inn_room(col: str) -> CheckView:
    b = Batch()
    W, D, H = 4.2, 5.0, 3.3
    slab(b, -W / 2, W / 2, -D / 2, D / 2, -0.05, 0.0)
    t = 0.2
    slab(b, -W / 2 - t, W / 2 + t, D / 2, D / 2 + t, 0.0, H)                 # 北墙（床靠这面）
    slab(b, -W / 2 - t, W / 2 + t, -D / 2 - t, -D / 2, 0.0, H)               # 南墙
    for y0, y1, z0, z1 in ((-D / 2, 0.2, 0.0, H), (1.4, D / 2, 0.0, H), (0.2, 1.4, 0.0, 1.3), (0.2, 1.4, 2.2, H)):
        slab(b, -W / 2 - t, -W / 2, y0, y1, z0, z1)                        # 西墙 + 直棂窗洞（窗台齐胸 1.3）
    for k in range(7):
        yy = 0.2 + 1.2 * (k + 0.5) / 7
        b.cbox((-W / 2 - t / 2, yy, 1.75), (0.05, 0.05, 0.9))
    for y0, y1, z0, z1 in ((-D / 2, 1.3, 0.0, H), (2.4, D / 2, 0.0, H), (1.3, 2.4, 2.1, H)):
        slab(b, W / 2, W / 2 + t, y0, y1, z0, z1)                          # 东墙 + 门洞（两扇木板门在 shot 层）
    slab(b, W / 2, W / 2 + t, 1.3, 2.4, 0.0, 0.15)                          # 门槛高出地面半尺
    for k in range(8):
        xx = -W / 2 + W * (k + 0.5) / 8
        slab(b, xx - 0.05, xx + 0.05, -D / 2, D / 2, H - 0.12, H)          # 椽子
    slab(b, -W / 2 - t, W / 2 + t, -D / 2 - t, D / 2 + t, H, H + 0.05)      # 望板
    fin(b, "inn_room_shell", col)
    b = Batch()
    slab(b, -1.8, 0.4, 1.35, 2.45, 0.40, 0.46)                               # 床板离地一尺半
    legs(b, -1.8, 0.4, 1.35, 2.45, 0.40, 0.08)
    slab(b, -1.75, 0.35, 1.4, 2.4, 0.46, 0.58)                              # 草荐 + 褥
    slab(b, 0.05, 0.35, 1.75, 2.05, 0.58, 0.72)                              # 瓷枕（床东头）
    chair(b, 0.85, 1.55, "W")
    table(b, 0.95, 0.55, 0.9, 0.6, 0.85)                                     # 高桌齐腰
    b.cyl(1.15, 0.55, 0.85, 1.0, 0.03, 8)                                    # 灯柱
    b.cyl(1.15, 0.55, 1.0, 1.03, 0.07, 10)                                   # 浅碟灯盏
    b.cyl(0.75, 0.45, 0.85, 0.92, 0.07, 10)                                  # 白瓷碗
    b.cyl(0.7, 0.7, 0.85, 1.07, 0.08, 10)                                    # 粗陶水壶
    table(b, 0.95, -0.15, 0.35, 0.35, 0.45)                                  # 兀子
    b.cyl(1.8, -2.2, 0.0, 0.6, 0.28, 12)                                     # 陶缸
    b.cyl(1.8, -2.2, 0.6, 0.64, 0.3, 12)
    fin(b, "inn_room_furniture", col)
    return CheckView((-1.9, -2.3, 1.45), (1.2, 1.6, 0.8), 24.0)


# ── 2 粥饭摊（S09 S10；早市，落位在 Place C 桥南街口）──────────────────────────────────
def set_congee_stall(col: str) -> CheckView:
    b = Batch()
    table(b, 0.0, 0.0, 2.0, 0.9, 0.85)                                       # 案板（顾客站 −Y 一侧）
    slab(b, 0.45, 0.95, 0.6, 1.1, 0.0, 0.6)                                  # 泥炉
    b.cyl(0.7, 0.85, 0.6, 0.9, 0.25, 12)                                     # 釜
    for x, y, h in ((-1.3, -0.7, 2.3), (1.3, -0.7, 2.3), (-1.3, 1.4, 2.1), (1.3, 1.4, 2.1)):
        b.cyl(x, y, 0.0, h, 0.04, 6)
    b.poly_solid([Vector((-1.45, -0.85, 2.3)), Vector((1.45, -0.85, 2.3)), Vector((1.45, 1.55, 2.1)), Vector((-1.45, 1.55, 2.1))],
                 [Vector((-1.45, -0.85, 2.34)), Vector((1.45, -0.85, 2.34)), Vector((1.45, 1.55, 2.14)), Vector((-1.45, 1.55, 2.14))])
    table(b, 2.2, 0.0, 0.25, 1.8, 0.45)                                      # 长凳（摊边，沿 Y）
    for k in range(4):
        b.cyl(-0.7 + 0.18 * k, 0.1, 0.85, 0.93, 0.07, 10)                    # 叠碗
    fin(b, "congee_stall", col)
    return CheckView((3.2, -4.2, 1.5), (0.4, 0.3, 0.9), 35.0)


# ── 3 饮子摊（S11；伞 + 担子 + 汤瓶，落位在 Place C 桥南街口）─────────────────────────────
def set_drink_stall(col: str) -> CheckView:
    b = Batch()
    for x in (-0.55, 0.55):
        slab(b, x - 0.25, x + 0.25, -0.2, 0.2, 0.0, 0.6)                     # 担子两头木箱
    slab(b, -0.85, 0.85, -0.22, 0.22, 0.6, 0.64)                             # 搁板
    b.cyl(0.55, 0.0, 0.64, 0.8, 0.15, 12)                                    # 小风炉
    b.cyl(0.55, 0.0, 0.8, 1.06, 0.09, 12)                                    # 汤瓶
    b.cyl(0.55, 0.0, 1.06, 1.14, 0.03, 8)
    for k in range(3):
        b.cyl(-0.55, 0.0, 0.64 + 0.06 * k, 0.69 + 0.06 * k, 0.07, 10)        # 叠碗
    b.cyl(-0.9, 0.45, 0.0, 2.45, 0.035, 6)                                   # 伞柄
    b.hip(-0.9, 0.45, 2.6, 2.6, 2.1, 0.35)                                   # 伞面（方锥近似）
    fin(b, "drink_stall", col)
    return CheckView((1.6, -2.4, 1.5), (-0.2, 0.1, 1.0), 35.0)


# ── 4 夜市食摊（S30；p1 形制：矮木案 + 四竹竿苇席棚 + 棚柱木托灯盏；三个变体）──────────────────────
def night_stall_base(b: Batch) -> None:
    table(b, 0.0, 0.0, 1.8, 0.7, 0.65)                                       # 摊案齐大腿高
    for x in (-1.0, 1.0):
        for y in (-0.45, 0.45):
            b.cyl(x, y, 0.0, 2.1, 0.035, 6)
    slab(b, -1.15, 1.15, -0.65, 0.65, 2.1, 2.14)                              # 苇席棚顶比人高出一头
    slab(b, -1.08, -0.92, -0.53, -0.37, 1.22, 1.25)                          # 前左棚柱木托
    b.cyl(-1.0, -0.45, 1.25, 1.29, 0.05, 10)                                  # 敞口陶灯盏（离案面约 60 cm）
    b.cyl(0.8, -0.28, 0.65, 0.69, 0.05, 10)                                   # 案角灯盏
    table(b, 0.0, -0.85, 1.6, 0.25, 0.4)                                      # 摊前长条凳


def set_night_stall(col: str) -> CheckView:
    b = Batch()
    night_stall_base(b)
    for k in range(3):
        b.cyl(-0.5 + 0.35 * k, 0.05, 0.65, 0.75, 0.1, 10)                    # 陶盆（水饭 / 爊肉 / 干脯）
    fin(b, "night_stall", col)
    return CheckView((2.6, -3.2, 1.4), (0.0, 0.0, 0.8), 35.0)


def variant_baozi(col: str) -> None:
    b = Batch()
    night_stall_base(b)
    slab(b, 0.2, 0.6, -0.2, 0.2, 0.65, 0.9)                                   # 矮泥炉（案右端）
    b.cyl(0.4, 0.0, 0.9, 1.05, 0.2, 12)                                       # 陶釜
    b.cyl(0.4, 0.0, 1.05, 1.17, 0.22, 12)                                     # 竹编笼屉 × 2
    b.cyl(0.4, 0.0, 1.17, 1.29, 0.22, 12)
    fin(b, "baozi_stall", col)


def variant_baichang(col: str) -> None:
    b = Batch()
    night_stall_base(b)
    slab(b, -0.8, -0.4, -0.2, 0.2, 0.65, 0.9)                                 # 矮泥炉（案左端）
    b.cyl(-0.6, 0.0, 0.9, 0.93, 0.25, 16)                                     # 平底铁鏊
    fin(b, "baichang_stall", col)


# ── 5 坊巷街口（bg7-1；S13 街口行人 + 赁驴 + 骑驴跟拍）────────────────────────────────────
def set_lane_mouth(col: str) -> CheckView:
    b = Batch()
    slab(b, -40.0, 40.0, -20.0, 58.0, -0.05, 0.0)
    slab(b, -40.0, 40.0, -10.0, 0.0, 0.0, 0.05)                               # 大街（东西向）
    rng = random.Random(1307)
    for x0 in range(-40, 40, 8):                                              # 大街南侧铺面（门朝北）
        h2 = rng.random() < 0.3
        house(b, x0 + 0.3, x0 + 7.7, -17.0, -10.5, 5.6 if h2 else 3.2, 7.2 if h2 else 4.8, "x")
    for x0, x1 in ((-40.0, -9.5), (9.5, 40.0)):                               # 大街北侧（巷口两边）
        for k in range(int((x1 - x0) // 7.5)):
            xa = x0 + 7.5 * k
            house(b, xa + 0.3, xa + 7.2, 0.5, 7.5, 3.4, 5.0, "x")
    slab(b, -3.1, 3.1, 7.0, 45.0, 0.0, 0.05)                                  # 巷面宽约两丈
    for k in range(5):                                                         # 巷西侧民居
        ya = 9.0 + 7.2 * k
        house(b, -10.0, -3.4, ya, ya + 6.8, 3.2, 4.8, "y")
    for k in range(3):                                                         # 巷东侧：客店两层 + 民居
        ya = 9.0 + 12.0 * k
        if k == 0:
            slab(b, 3.4, 10.0, ya, ya + 11.0, 0.0, 6.2)
            gable(b, 3.0, 10.4, ya - 0.4, ya + 11.4, 6.2, 8.0, "y")
            railing(b, [(3.2, ya), (3.2, ya + 11.0)], 3.8, 1.0, 1.0)          # 二层临街栏杆离地约一丈二
            b.prism_y(ya + 1.0, ya + 10.0, [(1.6, 2.5), (3.4, 2.9), (3.4, 3.0), (1.6, 2.6)])   # 芦席披檐
            table(b, 2.4, ya + 5.5, 0.6, 1.6, 0.5)                             # 披檐下矮木案
        else:
            house(b, 3.4, 10.0, ya, ya + 11.0, 3.2, 4.8, "y")
    slab(b, -7.2, -4.8, 2.3, 4.7, 0.0, 0.31)                                  # 井台高出地面一尺
    railing(b, [(-6.5, 3.0), (-5.5, 3.0), (-5.5, 4.0), (-6.5, 4.0), (-6.5, 3.0)], 0.31, 0.6, 0.5)
    house(b, 4.5, 8.5, 1.5, 5.5, 2.8, 4.2, "y")                               # 军巡铺屋
    tree(b, -8.0, 8.5, 0.0, 9.0, 3.5, 0.35)                                   # 老槐
    b.poly_solid([Vector((-14.0, 45.0, 0.0)), Vector((14.0, 45.0, 0.0)), Vector((14.0, 58.0, 0.0)), Vector((-14.0, 58.0, 0.0))],
                     [Vector((-14.0, 52.0, 8.0)), Vector((14.0, 52.0, 8.0)), Vector((14.0, 58.0, 8.0)), Vector((-14.0, 58.0, 8.0))])  # 远端城墙斜坡
    fin(b, "lane_mouth", col)
    return CheckView((14.0, -8.0, 1.6), (0.0, 6.0, 2.0), 28.0)


# ── 6 赵太丞家（bg10-1 门面 / bg10-2 铺内；坐北朝南，街沿 X；S14 S15）─────────────────────────────
def set_zhao_clinic(col: str) -> CheckView:
    b = Batch()
    slab(b, -30.0, 30.0, -32.0, 16.0, -0.05, 0.0)
    slab(b, -30.0, 30.0, -26.0, 0.0, 0.0, 0.05)                               # 大街（卡：街对面约二十步 → 街宽取 26 m）
    slab(b, -6.0, 6.0, 0.0, 8.0, 0.0, 0.18)                                   # 铺面地面比街面高一级
    for x in (-6.0, -2.0, 2.0, 6.0):
        b.cyl(x, 0.3, 0.18, 3.8, 0.14, 8)                                     # 前檐下无墙无门板
    slab(b, -6.0, 6.0, 7.85, 8.0, 0.18, 3.8)                                  # 后墙
    for k in range(9):
        b.cbox((-1.5 + 3.0 * k / 8, 7.8, 1.5), (0.05, 0.08, 1.0))             # 柜台后直棂窗（棂条）
    for x in (-6.0, 6.0):
        slab(b, x - 0.1, x + 0.1, 0.3, 8.0, 0.18, 3.8)                        # 两侧白灰墙
    gable(b, -6.6, 6.6, -0.8, 8.6, 3.8, 6.0, "x")
    slab(b, -2.0, 2.0, 0.15, 0.3, 3.2, 3.7)                                   # 贴檐口的窄长木匾
    table(b, 0.0, 6.9, 9.0, 0.6, 1.0)                                         # 齐腰柜台
    chair(b, 2.6, 5.9, "S")                                                   # 横档靠背椅（空着）
    chair(b, -1.8, 3.4, "E")                                                  # 素木椅（抱孩子的妇人）
    for x in (-6.7, 6.7):
        slab(b, x - 0.3, x + 0.3, -0.9, -0.5, 0.0, 0.4)                       # 立招木座
        slab(b, x - 0.27, x + 0.27, -0.75, -0.65, 0.4, 5.6)                   # 立招顶端高出屋檐一截
    slab(b, -5.6, -5.2, 0.6, 0.68, 0.18, 2.6)                                 # 门里左柱矮立招
    slab(b, -13.0, -7.0, -0.5, 7.0, 0.0, 0.3)                                 # 门屋（西）台基
    for x in (-13.0, -7.0):
        for y in (-0.3, 6.8):
            slab(b, x - 0.35, x + 0.35, y - 0.35, y + 0.35, 0.3, 0.45)        # 方石柱础高出地面半尺
            b.cbox((x, y, 2.6), (0.35, 0.35, 4.3))
    slab(b, -13.6, -6.4, -1.0, 7.5, 4.75, 5.35)                               # 斗拱层把屋檐挑远
    gable(b, -14.4, -5.6, -1.8, 8.3, 5.35, 7.4, "x")
    house(b, -14.0, -6.0, 9.0, 16.0, 6.0, 8.6, "x")                           # 第二重屋顶往里退、更高
    steps(b, -11.0, -9.0, -0.5, -1, 0.0, 0.3, 2, 0.4)                         # 门屋前两块青石踏步
    table(b, -9.8, -1.3, 1.6, 0.3, 0.45)                                      # 门屋旁长木凳
    house(b, 7.5, 13.0, 0.5, 8.0, 3.0, 4.6, "x")                              # 东邻矮一截的铺子（隔窄巷）
    b.prism_x(7.5, 13.0, [(-1.2, 2.3), (0.5, 2.8), (0.5, 2.9), (-1.2, 2.4)])  # 芦席披檐
    for x0 in (-30.0, -22.0, 14.5, 22.0):
        house(b, x0 + 0.3, x0 + 7.5, 0.5, 8.0, 3.4, 5.2, "x")
    for x0 in range(-30, 30, 8):
        house(b, x0 + 0.3, x0 + 7.7, -32.0, -26.5, 3.2, 4.8, "x")             # 街南
    tree(b, -8.6, -2.4, 0.0, 8.0, 2.8, 0.3)                                   # 门前老柳
    fin(b, "zhao_clinic", col)
    return CheckView((-2.5, -24.5, 1.6), (-2.0, 4.0, 2.6), 35.0)


# ── 7 园林雅集（bg15-1；园地高出池水半人，曲栏、大案、茶床；S23）─────────────────────────────
def set_garden(col: str) -> CheckView:
    b = Batch()
    slab(b, -25.0, 25.0, -20.0, 10.0, -1.0, 0.0)                              # 园地
    slab(b, -25.0, 25.0, 10.0, 30.0, -1.3, -1.0)                              # 池底
    slab(b, -25.0, 25.0, 10.0, 30.0, -0.85, -0.8)                             # 池水（园地高出半人）
    slab(b, -25.0, 25.0, 9.8, 10.0, -1.0, 0.0)                                # 岸石
    railing(b, [(-25.0, 9.6), (8.0, 9.6)], 0.0, 0.9, 1.2)                     # 沿池曲栏（只到腰）
    railing(b, [(10.0, 9.6), (25.0, 9.6)], 0.0, 0.9, 1.2)
    for k in range(3):
        slab(b, 8.0, 10.0, 10.0 + 0.4 * k, 10.4 + 0.4 * k, -1.0, -0.27 * (k + 1))   # 曲栏断口三级石阶下水
    tree(b, -8.0, 7.5, 0.0, 9.0, 3.0, 0.3)                                    # 老垂柳 × 2
    tree(b, 4.0, 8.0, 0.0, 8.5, 2.8, 0.28)
    tree(b, 15.0, 6.5, 0.0, 12.0, 4.5, 0.45)                                  # 大树
    b.hip(12.8, 6.8, 1.4, 1.0, 0.0, 1.6)                                      # 湖石（大树左侧）
    table(b, 0.0, 2.0, 2.6, 1.2, 0.8)                                         # 黑漆大案（高到坐着的人胸口）
    slab(b, -1.2, 1.2, 1.5, 2.5, 0.12, 0.18)                                  # 腿间横撑
    for x, y in ((-0.95, 3.0), (0.2, 3.0), (1.3, 3.0), (-1.9, 2.0), (1.95, 1.4)):
        b.cyl(x, y, 0.0, 0.45, 0.22, 12)                                      # 藤编鼓墩 × 5
    table(b, -2.6, -1.2, 1.2, 0.6, 0.7)                                       # 茶床（大案前、靠机位一侧）
    slab(b, -3.55, -3.2, -1.38, -1.02, 0.0, 0.45)                             # 小风炉
    b.cyl(-3.375, -1.2, 0.45, 0.72, 0.08, 10)                                 # 汤瓶
    table(b, -2.6, -0.3, 0.4, 0.4, 1.0)                                       # 高几
    b.cyl(-2.6, -0.3, 1.0, 1.15, 0.09, 10)                                    # 三足香炉
    for k in range(10):
        b.cyl(-20.0 + 1.6 * k, 28.0 + (k % 3) * 0.6, -1.0, 6.0, 0.06, 6)      # 对岸竹丛
    slab(b, 0.0, 25.0, 29.0, 29.4, -1.0, 2.2)                                 # 对岸灰瓦矮墙
    gable(b, -0.2, 25.2, 28.8, 29.6, 2.2, 2.6, "x")
    railing(b, [(-12.0, -14.0), (25.0, -14.0)], 0.0, 0.9, 1.2)                # 前景另一道曲栏（她站栏外）
    fin(b, "garden", col)
    return CheckView((12.0, -16.0, 1.6), (0.0, 2.0, 0.8), 50.0)


# ── 8 正店阁子（bg5-2 内容表；二层临内廊的一间小阁子；S31 7–26 s · S32）─────────────────────────────
def set_zhengdian_booth(col: str) -> CheckView:
    b = Batch()
    slab(b, -3.0, 3.0, -1.6, 3.2, -0.05, 0.0)
    slab(b, -3.0, 3.0, 3.0, 3.2, 0.0, 1.0)                                    # 临街外墙：吊窗下
    slab(b, -3.0, -0.8, 3.0, 3.2, 1.0, 1.9)
    slab(b, 0.8, 3.0, 3.0, 3.2, 1.0, 1.9)
    slab(b, -3.0, 3.0, 3.0, 3.2, 1.9, 2.8)
    slab(b, -0.8, 0.8, 3.05, 3.15, 1.5, 1.9)                                  # 竹帘半垂
    for x in (-3.0, -1.5, 1.5, 3.0):
        slab(b, x - 0.05, x + 0.05, 0.0, 3.0, 0.0, 2.6)                       # 阁子隔断（左右各有邻间）
    slab(b, -1.5, 1.5, -0.05, 0.05, 2.2, 2.6)                                 # 帘额（帘子本身在 shot 层）
    for x0, x1 in ((-3.0, -1.5), (1.5, 3.0)):
        slab(b, x0, x1, -0.05, 0.05, 0.0, 2.6)                                # 邻间门面
    railing(b, [(-3.0, -1.6), (3.0, -1.6)], 0.0, 0.9, 0.8)                    # 内廊栏杆
    table(b, 0.0, 1.65, 1.0, 0.7, 0.85)                                       # 高桌
    chair(b, 0.0, 0.85, "N")                                                  # 她的座（背后是帘）
    chair(b, 0.0, 2.45, "S")
    b.cyl(0.35, 1.85, 0.85, 1.1, 0.03, 8)                                     # 烛台一支
    fin(b, "zhengdian_booth", col)
    return CheckView((0.3, -1.3, 1.45), (0.0, 1.8, 0.9), 35.0)


# ── 9 今日州桥遗址（bg9-1；坑沿 z＝0，坑底 −10；东西向故道 + 南北向明代砖券桥；S36）───────────────────
def set_excavation(col: str) -> CheckView:
    b = Batch()
    for x0, x1, y0, y1 in ((-50.0, 50.0, 22.0, 35.0), (-50.0, 50.0, -35.0, -22.0), (-50.0, -35.0, -22.0, 22.0), (35.0, 50.0, -22.0, 22.0)):
        slab(b, x0, x1, y0, y1, -1.0, 0.0)                                    # 坑沿外地面
    for inset, z in ((0.0, -3.3), (2.0, -6.6)):                               # 退台（每层 2 m 宽）
        xi, yi = 35.0 - inset, 22.0 - inset
        for x0, x1, y0, y1 in ((-xi, xi, yi - 2.0, yi), (-xi, xi, -yi, -yi + 2.0), (-xi, -xi + 2.0, -yi, yi), (xi - 2.0, xi, -yi, yi)):
            slab(b, x0, x1, y0, y1, -10.0, z)
    slab(b, -31.0, 31.0, -18.0, 18.0, -10.5, -10.0)                           # 坑底（故道河床）
    slab(b, -31.0, 31.0, -8.0, 8.0, -9.98, -9.93)                             # 浅水
    for s in (-1, 1):
        slab(b, -4.5, 4.5, s * 2.9, s * 12.0, -10.0, -2.4)                    # 券桥两侧桥身（南北向跨故道）
    slab(b, -4.5, 4.5, -2.9, -2.1, -10.0, -6.3)                               # 券脚
    slab(b, -4.5, 4.5, 2.1, 2.9, -10.0, -6.3)
    for k in range(12):                                                        # 券洞 宽 5.8、高 6.58（半圆拱顶）；逐段做凸块，免得凹多边形三角化错面
        a0, a1 = math.pi * k / 12, math.pi * (k + 1) / 12
        p0 = (2.9 * math.cos(a0), -6.3 + 2.9 * math.sin(a0))
        p1 = (2.9 * math.cos(a1), -6.3 + 2.9 * math.sin(a1))
        b.prism_x(-4.5, 4.5, [p0, p1, (p1[0], -2.4), (p0[0], -2.4)] if p1[0] < p0[0] else [p1, p0, (p0[0], -2.4), (p1[0], -2.4)])
    for s in (-1, 1):
        slab(b, 5.0, 28.0, s * 8.0 - 0.3, s * 8.0 + 0.3, -10.0, -6.7)         # 桥东两岸浮雕石壁（高 3.3）
    steps_x(b, -3.0, 3.0, 13.5, -1, -10.0, -8.2, 10, 0.35)                    # 桥东河床里一段青石台阶
    b.poly_solid([Vector((-20.0, 14.0, -10.0)), Vector((-19.2, 14.0, -10.0)), Vector((-19.2, 20.0, -3.3)), Vector((-20.0, 20.0, -3.3))],
                 [Vector((-20.0, 14.0, -9.9)), Vector((-19.2, 14.0, -9.9)), Vector((-19.2, 20.0, -3.2)), Vector((-20.0, 20.0, -3.2))])  # 钢梯
    b.poly_solid([Vector((20.0, -16.0, -10.0)), Vector((20.8, -16.0, -10.0)), Vector((30.8, -25.0, 0.0)), Vector((30.0, -25.0, 0.0))],
                 [Vector((20.0, -16.0, -9.8)), Vector((20.8, -16.0, -9.8)), Vector((30.8, -25.0, 0.2)), Vector((30.0, -25.0, 0.2))])   # 传送带
    railing(b, [(-35.3, -22.3), (35.3, -22.3), (35.3, 22.3), (-35.3, 22.3), (-35.3, -22.3)], 0.0, 1.1, 2.0)   # 坑沿木栏杆
    railing(b, [(-38.5, -25.5), (38.5, -25.5), (38.5, 25.5), (-38.5, 25.5), (-38.5, -25.5)], 0.0, 0.9, 2.5)   # 外沿白色金属护栏
    slab(b, -30.0, 10.0, 30.0, 34.0, 0.0, 3.0)                                # 对面坑沿平房
    slab(b, 12.0, 45.0, 31.0, 31.1, 0.0, 2.5)                                 # 绿色围挡
    for x, y, a in ((-12.0, 10.0, 0.0), (6.0, -13.0, 0.5), (-22.0, -6.0, 0.2)):
        b.cbox((x, y, -9.75), (0.7 + a, 0.35, 0.3))                           # 掉落的长条石
    fin(b, "excavation", col)
    return CheckView((38.0, 4.5, 1.5), (0.0, 0.0, -7.5), 28.0)


SETS: dict[str, Callable[[str], CheckView]] = {
    "客店房间": set_inn_room,
    "粥饭摊": set_congee_stall,
    "饮子摊": set_drink_stall,
    "夜市食摊": set_night_stall,
    "坊巷街口": set_lane_mouth,
    "赵太丞家": set_zhao_clinic,
    "园林": set_garden,
    "正店阁子": set_zhengdian_booth,
    "遗址坑": set_excavation,
}
VARIANTS: dict[str, dict[str, Callable[[str], None]]] = {"夜市食摊": {"包子摊": variant_baozi, "羊白肠摊": variant_baichang}}


def bbox(col: bpy.types.Collection) -> tuple[Vector, Vector]:
    pts = [ob.matrix_world @ Vector(c) for ob in col.all_objects if ob.type == "MESH" for c in ob.bound_box]
    return (Vector([min(p[i] for p in pts) for i in range(3)]), Vector([max(p[i] for p in pts) for i in range(3)]))


def digest() -> str:
    h = hashlib.sha256()
    for ob in sorted(bpy.data.objects, key=lambda o: o.name):
        h.update(ob.name.encode())
        if ob.type == "MESH":
            co = array("f", [0.0]) * (len(ob.data.vertices) * 3)
            ob.data.vertices.foreach_get("co", co)
            h.update(co.tobytes())
    return h.hexdigest()


STILL_KEYS: dict[str, str] = {"客店房间": "inn_room", "粥饭摊": "congee_stall", "饮子摊": "drink_stall", "夜市食摊": "night_stall",
                              "坊巷街口": "lane_mouth", "赵太丞家": "zhao_clinic", "园林": "garden", "正店阁子": "zhengdian_booth",
                              "遗址坑": "excavation"}


def still(name: str, view: CheckView) -> Path:
    sc = bpy.context.scene
    cam_data = bpy.data.cameras.new("check_cam")
    cam_data.lens, cam_data.sensor_width, cam_data.clip_start, cam_data.clip_end = view.lens, 36.0, 0.05, 2000.0
    cam = bpy.data.objects.new("check_cam", cam_data)
    sc.collection.objects.link(cam)
    cam.location = view.pos
    cam.rotation_euler = (Vector(view.target) - Vector(view.pos)).to_track_quat("-Z", "Y").to_euler()
    sc.camera = cam
    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light, sh.color_type, sh.show_shadows, sh.show_cavity = "STUDIO", "SINGLE", False, False
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1280, 720, 100
    im = sc.render.image_settings
    if hasattr(im, "media_type"):
        im.media_type = "IMAGE"
    im.file_format = "PNG"
    out = SETS_DIR / f"check_{STILL_KEYS[name]}.png"       # 注意：ai_video_management 的媒体重命名（MediaWriter）会把这里的 png 改成 sets{N}.png
    out.unlink(missing_ok=True)
    sc.render.filepath = str(out)
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam)
    bpy.data.cameras.remove(cam_data)
    if not out.is_file():
        raise SystemExit(f"静帧没写出来：{out}")
    return out


def main() -> int:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser(prog="build_sk1_sets.py")
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--stills", action="store_true")
    args = ap.parse_args(argv)
    names = args.only or list(SETS)
    unknown = set(names) - set(SETS)
    if unknown:
        raise SystemExit(f"未知套景 {sorted(unknown)}；可用 {list(SETS)}")
    SETS_DIR.mkdir(parents=True, exist_ok=True)
    random.seed(0)
    for name in names:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bj.COLS.clear()
        col = f"SET_{name}"
        view = SETS[name](col)
        for vname, fn in VARIANTS.get(name, {}).items():
            fn(f"SET_{vname}")
        out = SETS_DIR / f"{name}.blend"
        bpy.ops.wm.save_as_mainfile(filepath=str(out))
        for c in sorted(bpy.data.collections, key=lambda c: c.name):
            if c.name.startswith("SET_"):
                lo, hi = bbox(c)
                faces = sum(len(o.data.polygons) for o in c.all_objects if o.type == "MESH")
                print(f"SET_BBOX {c.name} lo=({lo.x:.3f},{lo.y:.3f},{lo.z:.3f}) hi=({hi.x:.3f},{hi.y:.3f},{hi.z:.3f}) "
                      f"size=({hi.x - lo.x:.3f},{hi.y - lo.y:.3f},{hi.z - lo.z:.3f}) objects={len(c.all_objects)} faces={faces}")
        print(f"SET_SAVED {out} sha256={digest()}")
        if args.stills:
            print(f"SET_STILL {still(name, view)}")
        sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
