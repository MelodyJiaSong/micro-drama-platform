# -*- coding: utf-8 -*-
"""Build 余杭客栈.blend — the previz geometry source for xianjian_yi 余杭镇 interiors.

The ONLY numeric input is
`ai_videos/xianjian_yi/_series/scenes/余杭客栈/_blender/blender_build.md`.
Every constant below is a transcription of a row in that file; change geometry by editing
the spec and this generator and re-running — never by hand-editing the .blend
(ai_video.md rule 4h ④).

Geometry only: no materials, no lights (rule 4g ⑤ — the building stays a grey model; its
look comes from the scene 主体卡 and the generation model).

Precision is graded by camera proximity (rule 4g ④). xj1 is entirely interior, so the roof
is only ever seen FROM BELOW, across the double-height hall: 檩 / 椽 / 望板 are on camera and
are built at full precision, while the tile field above them is a swept corrugation — correct
in profile and 举折 curve, but not articulated into individual courses, because no xj1 shot
can see it. Exterior episodes that need the roof should raise TILE_COURSES.

Run (repo root):
  blender -b --factory-startup --python tools/build_yuhang_kezhan.py
  blender -b --factory-startup --python tools/build_yuhang_kezhan.py -- --qc
  blender -b --factory-startup --python tools/build_yuhang_kezhan.py -- out.blend --qc
"""
from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
SCENE_DIR = REPO / "ai_videos" / "xianjian_yi" / "_series" / "scenes" / "余杭客栈" / "_blender"
DEFAULT_OUT = SCENE_DIR / "余杭客栈.blend"

# ── §1 模数 ─────────────────────────────────────────────────────────────────
M: float = 0.30
D_YAN: float = 0.24
D_JIN: float = 0.28
TAPER: float = 0.93
T_WALL: float = 0.24
T_PLANK: float = 0.04

# ── §2 柱网 ─────────────────────────────────────────────────────────────────
BAY_X: tuple[float, ...] = (0.0, 3.30, 7.20, 10.50)
BAY_Y: tuple[float, ...] = (0.0, 1.50, 7.50, 10.50, 12.00)
Y_YANQIAN, Y_JINQIAN, Y_ZHONG, Y_JINHOU, Y_YANHOU = BAY_Y

# ── §3 竖向 ─────────────────────────────────────────────────────────────────
Z_GROUND: float = 0.0
Z_BEAM1: float = 3.60
Z_FLOOR2: float = 3.80
Z_BEAM2: float = 6.35
Z_EAVE: float = 6.60
Z_RIDGE: float = 9.30

# ── §4 屋架（举折：y, 檩顶标高）────────────────────────────────────────────────
PURLINS: tuple[tuple[float, float], ...] = (
    (-0.90, 6.600), (1.50, 7.180), (3.75, 8.000), (6.00, 9.300),
    (8.25, 8.000), (10.50, 7.180), (12.90, 6.600),
)
D_PURLIN: float = 0.20
GABLE_OVERHANG: float = 0.60
RAFTER_W, RAFTER_H, RAFTER_PITCH = 0.09, 0.07, 0.35
SHEATH_T: float = 0.025
TILE_PITCH: float = 0.16
TILE_COURSES: bool = False          # xj1 是纯内景，屋面只从下面看 → 不做逐垄分陇分皮
RIDGE_H, RIDGE_T = 0.28, 0.10

# ── §5 二层 ─────────────────────────────────────────────────────────────────
Y_GALLERY_S, Y_GALLERY_N = 7.50, 9.00
ROOM_SPANS: tuple[tuple[str, float, float], ...] = (
    ("客房丙", 0.00, 2.40), ("客房乙", 2.40, 4.80),
    ("客房甲", 4.80, 7.20), ("李逍遥房", 7.20, 10.50),
)
STAIR_STEPS: int = 18
STAIR_TREAD: float = 0.26
STAIR_WIDTH: float = 1.10
STAIR_X0: float = 0.00
STAIR_TOP_Y: float = 8.25
RAIL_Y: float = 7.62
RAIL_H: float = 0.95
RAIL_X0: float = 1.20           # 楼梯口：栏杆必须在此让开，否则从走廊下不去楼梯
RAIL_POSTS: int = 9
RAIL_BALUSTERS: int = 5

# ── §6 门窗 ─────────────────────────────────────────────────────────────────
DOOR_LEAF_W, DOOR_LEAF_H = 0.60, 2.80
LATTICE_BAR = 0.03
GEXIN_RATIO = 0.55
SILL_H, WIN_H = 0.90, 1.60
WIN2_SILL, WIN2_H = 4.70, 1.40
ROOM_DOOR = (0.80, 1.95)
XY_WINDOW = (1.00, 1.00)
WIN_EAST_Y: float = 11.25       # 必须落在 y=10.50 与 y=12.00 两根柱之间，否则柱子立在窗当中
# 穿枋标高：二层两道必须避开窗洞带 (WIN2_SILL, WIN2_SILL+WIN2_H)，否则横穿窗口
TIE_LEVELS_1: tuple[float, ...] = (1.35, 2.55, Z_BEAM1)
TIE_LEVELS_2: tuple[float, ...] = (Z_FLOOR2 + 0.55, Z_FLOOR2 + 2.35)

# ── §7 地面 ─────────────────────────────────────────────────────────────────
BRICK = (0.28, 0.28, 0.04)
BRICK_JOINT = 0.012
PLANK_W = 0.22

# ── §8 家具 ─────────────────────────────────────────────────────────────────
HALL_TABLES: tuple[tuple[float, float], ...] = ((1.85, 3.10), (5.25, 3.10), (8.65, 3.10), (5.25, 5.95))


@dataclass(frozen=True)
class Build:
    root: bpy.types.Collection
    frame: bpy.types.Collection
    roof: bpy.types.Collection
    floor2: bpy.types.Collection
    envelope: bpy.types.Collection
    ground: bpy.types.Collection
    furniture: bpy.types.Collection


# ── mesh helpers ────────────────────────────────────────────────────────────

def _link(name: str, bm: bmesh.types.BMesh, coll: bpy.types.Collection) -> bpy.types.Object:
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.validate()
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    return ob


def box(name: str, size: tuple[float, float, float], center: tuple[float, float, float],
        coll: bpy.types.Collection, rot_z: float = 0.0) -> bpy.types.Object:
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    if rot_z:
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(rot_z, 3, "Z"))
    bmesh.ops.translate(bm, vec=Vector(center), verts=bm.verts)
    return _link(name, bm, coll)


def cylinder(name: str, r_bottom: float, r_top: float, depth: float,
             center: tuple[float, float, float], coll: bpy.types.Collection,
             axis: str = "Z", segments: int = 24) -> bpy.types.Object:
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segments,
                          radius1=r_bottom, radius2=r_top, depth=depth)
    if axis == "X":
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, "Y"))
    elif axis == "Y":
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, "X"))
    bmesh.ops.translate(bm, vec=Vector(center), verts=bm.verts)
    return _link(name, bm, coll)


def prism(name: str, profile: list[tuple[float, float]], length: float, axis: str,
          origin: tuple[float, float, float], coll: bpy.types.Collection) -> bpy.types.Object:
    """Extrude a 2-D profile (in the plane normal to `axis`) into a solid of `length`."""
    bm = bmesh.new()
    verts = [bm.verts.new((u, v, 0.0)) for u, v in profile]
    face = bm.faces.new(verts)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, -length / 2.0), verts=bm.verts)
    ret = bmesh.ops.extrude_face_region(bm, geom=[face])
    moved = [e for e in ret["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0.0, 0.0, length), verts=moved)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if axis == "X":
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, "Y"))
    elif axis == "Y":
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(-math.pi / 2, 3, "X"))
    bmesh.ops.translate(bm, vec=Vector(origin), verts=bm.verts)
    return _link(name, bm, coll)


def cut_opening(name: str, size: tuple[float, float, float], center: tuple[float, float, float],
                coll: bpy.types.Collection) -> None:
    """Boolean a real hole through every wall the cutter touches.

    Doors and windows must be actual apertures, not panels laid on a solid wall: the whole
    point of the east window is the morning shafts it throws across 李逍遥's floor, and a
    previz with no aperture cannot produce them.
    """
    cutter = box(f"__cut_{name}", size, center, coll)
    targets = [ob for ob in coll.objects if ob is not cutter and not ob.name.startswith("__cut_")]
    for ob in targets:
        mod = ob.modifiers.new(name="opening", type="BOOLEAN")
        mod.operation = "DIFFERENCE"
        mod.object = cutter
        mod.solver = "EXACT"
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.modifier_apply(modifier="opening")
    bpy.data.objects.remove(cutter, do_unlink=True)


def frange(start: float, stop: float, step: float) -> list[float]:
    out: list[float] = []
    x = start
    while x <= stop + 1e-9:
        out.append(round(x, 6))
        x += step
    return out


# ── 屋架几何 ────────────────────────────────────────────────────────────────

def purlin_z(y: float) -> float:
    """Roof surface height at plan position y, following the 举折 polyline."""
    pts = PURLINS
    if y <= pts[0][0]:
        return pts[0][1]
    if y >= pts[-1][0]:
        return pts[-1][1]
    for (y0, z0), (y1, z1) in zip(pts, pts[1:]):
        if y0 <= y <= y1:
            return z0 + (z1 - z0) * (y - y0) / (y1 - y0)
    raise AssertionError("举折折线未覆盖 y=%r" % y)


def column_top(y: float) -> float:
    """穿斗式：柱通到顶，柱顶止于该柱位的檩底。"""
    return purlin_z(y) - D_PURLIN


# ── 构件生成 ────────────────────────────────────────────────────────────────

def build_plinths_and_columns(b: Build) -> int:
    n = 0
    for xi, x in enumerate(BAY_X):
        for yi, y in enumerate(BAY_Y):
            box(f"础_{xi}{yi}", (0.45, 0.45, 0.12), (x, y, 0.06), b.frame)
            cylinder(f"鼓镜_{xi}{yi}", 0.17, 0.17, 0.06, (x, y, 0.15), b.frame, segments=20)
            d = D_YAN if y in (Y_YANQIAN, Y_YANHOU) else D_JIN
            z_top = column_top(y)
            h = z_top - 0.18
            cylinder(f"柱_{xi}{yi}", d / 2, d / 2 * TAPER, h, (x, y, 0.18 + h / 2), b.frame, segments=20)
            n += 1
    return n


def build_ties(b: Build) -> None:
    """穿枋：沿进深方向穿过柱身把一榀架子拉结；额枋：沿面阔方向连柱头。"""
    for xi, x in enumerate(BAY_X):
        for z in TIE_LEVELS_1 + TIE_LEVELS_2:
            for (y0, y1) in zip(BAY_Y, BAY_Y[1:]):
                if z > min(column_top(y0), column_top(y1)):
                    continue
                box(f"穿枋_{xi}_{y0:.2f}_{z:.2f}", (0.06, y1 - y0, 0.22), (x, (y0 + y1) / 2, z), b.frame)
    for yi, y in enumerate(BAY_Y):
        z = column_top(y) - 0.20
        for (x0, x1) in zip(BAY_X, BAY_X[1:]):
            box(f"额枋_{yi}_{x0:.2f}", (x1 - x0, 0.14, 0.34), ((x0 + x1) / 2, y, z), b.frame)


def build_purlins_rafters_sheathing(b: Build) -> None:
    length = (BAY_X[-1] - BAY_X[0]) + D_JIN + 2 * GABLE_OVERHANG
    cx = (BAY_X[0] + BAY_X[-1]) / 2
    for i, (y, z) in enumerate(PURLINS):
        cylinder(f"檩_{i}", D_PURLIN / 2, D_PURLIN / 2, length,
                 (cx, y, z - D_PURLIN / 2), b.frame, axis="X", segments=16)

    xs = frange(BAY_X[0] - GABLE_OVERHANG, BAY_X[-1] + GABLE_OVERHANG, RAFTER_PITCH)
    for (y0, z0), (y1, z1) in zip(PURLINS, PURLINS[1:]):
        dy, dz = y1 - y0, z1 - z0
        span = math.hypot(dy, dz)
        pitch_angle = math.atan2(dz, dy)
        my, mz = (y0 + y1) / 2, (z0 + z1) / 2
        for xi, x in enumerate(xs):
            bm = bmesh.new()
            bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=Vector((RAFTER_W, span, RAFTER_H)), verts=bm.verts)
            bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0),
                             matrix=Matrix.Rotation(pitch_angle, 3, "X"))
            bmesh.ops.translate(bm, vec=Vector((x, my, mz + RAFTER_H / 2)), verts=bm.verts)
            _link(f"椽_{y0:.2f}_{xi}", bm, b.frame)

        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=Vector((length, span, SHEATH_T)), verts=bm.verts)
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(pitch_angle, 3, "X"))
        bmesh.ops.translate(bm, vec=Vector((cx, my, mz + RAFTER_H + SHEATH_T / 2)), verts=bm.verts)
        _link(f"望板_{y0:.2f}", bm, b.roof)


def build_tiles(b: Build) -> None:
    """仰合瓦：沿坡向（y）成垄，垄距 TILE_PITCH，逐段贴合举折折线。"""
    x0 = BAY_X[0] - GABLE_OVERHANG
    x1 = BAY_X[-1] + GABLE_OVERHANG
    base = SHEATH_T + RAFTER_H
    for (y0, z0), (y1, z1) in zip(PURLINS, PURLINS[1:]):
        dy, dz = y1 - y0, z1 - z0
        span = math.hypot(dy, dz)
        pitch_angle = math.atan2(dz, dy)
        my, mz = (y0 + y1) / 2, (z0 + z1) / 2
        for gi, gx in enumerate(frange(x0, x1 - TILE_PITCH, TILE_PITCH)):
            bm = bmesh.new()
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=12,
                                  radius1=0.075, radius2=0.075, depth=span)
            bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, "X"))
            bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(pitch_angle, 3, "X"))
            bmesh.ops.translate(bm, vec=Vector((gx, my, mz + base + 0.02)), verts=bm.verts)
            _link(f"仰瓦垄_{y0:.2f}_{gi}", bm, b.roof)

            bm = bmesh.new()
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=12,
                                  radius1=0.055, radius2=0.055, depth=span)
            bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, "X"))
            bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(pitch_angle, 3, "X"))
            bmesh.ops.translate(bm, vec=Vector((gx + TILE_PITCH / 2, my, mz + base + 0.09)), verts=bm.verts)
            _link(f"合瓦垄_{y0:.2f}_{gi}", bm, b.roof)

    box("正脊", (x1 - x0, RIDGE_T, RIDGE_H), ((x0 + x1) / 2, 6.00, Z_RIDGE + RIDGE_H / 2), b.roof)


# ── 楼面 / 楼梯 / 栏杆 ───────────────────────────────────────────────────────

def build_floor2(b: Build) -> None:
    x_lo, x_hi = BAY_X[0] - D_JIN / 2, BAY_X[-1] + D_JIN / 2
    for (y0, y1) in ((Y_ZHONG, Y_JINHOU), (Y_JINHOU, Y_YANHOU)):
        box(f"楼板大梁_{y0:.2f}", (x_hi - x_lo, 0.20, 0.30),
            ((x_lo + x_hi) / 2, y0, Z_BEAM1 - 0.15), b.floor2)
    for yj in frange(Y_ZHONG + 0.40, Y_YANHOU - 0.10, 0.40):
        box(f"楼栅_{yj:.2f}", (x_hi - x_lo, 0.07, 0.14), ((x_lo + x_hi) / 2, yj, Z_FLOOR2 - 0.11), b.floor2)
    for i, px in enumerate(frange(x_lo, x_hi - PLANK_W, PLANK_W)):
        box(f"楼板_{i}", (PLANK_W - 0.004, Y_YANHOU - Y_ZHONG, T_PLANK),
            (px + PLANK_W / 2, (Y_ZHONG + Y_YANHOU) / 2, Z_FLOOR2 - T_PLANK / 2), b.floor2)


def build_stair(b: Build) -> None:
    rise = Z_FLOOR2 / STAIR_STEPS
    cx = STAIR_X0 + STAIR_WIDTH / 2
    for i in range(STAIR_STEPS):
        z = rise * (i + 1)
        y = STAIR_TOP_Y - STAIR_TREAD * i
        box(f"踏步_{i:02d}", (STAIR_WIDTH, STAIR_TREAD, 0.05), (cx, y, z - 0.025), b.floor2)
        box(f"踢面_{i:02d}", (STAIR_WIDTH, 0.04, rise), (cx, y - STAIR_TREAD / 2, z - rise / 2), b.floor2)
    y_bot = STAIR_TOP_Y - STAIR_TREAD * (STAIR_STEPS - 1)
    length = math.hypot(STAIR_TOP_Y - y_bot, Z_FLOOR2)
    ang = math.atan2(Z_FLOOR2, STAIR_TOP_Y - y_bot)
    for side in (-1, 1):
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=Vector((0.06, length, 0.30)), verts=bm.verts)
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(-ang, 3, "X"))
        bmesh.ops.translate(bm, vec=Vector((cx + side * (STAIR_WIDTH / 2 + 0.03),
                                            (STAIR_TOP_Y + y_bot) / 2, Z_FLOOR2 / 2 - 0.18)), verts=bm.verts)
        _link(f"梯帮_{side}", bm, b.floor2)


def build_railing(b: Build) -> None:
    x_lo, x_hi = RAIL_X0, BAY_X[-1]
    pitch = (x_hi - x_lo) / RAIL_POSTS
    box("绦环板", (x_hi - x_lo, 0.04, 0.22), ((x_lo + x_hi) / 2, RAIL_Y, Z_FLOOR2 + 0.11), b.floor2)
    box("寻杖", (x_hi - x_lo, 0.09, 0.07), ((x_lo + x_hi) / 2, RAIL_Y, Z_FLOOR2 + RAIL_H - 0.035), b.floor2)
    for i in range(RAIL_POSTS + 1):
        px = x_lo + pitch * i
        box(f"望柱_{i:02d}", (0.10, 0.10, RAIL_H + 0.06), (px, RAIL_Y, Z_FLOOR2 + (RAIL_H + 0.06) / 2), b.floor2)
    for i in range(RAIL_POSTS):
        for j in range(1, RAIL_BALUSTERS + 1):
            px = x_lo + pitch * i + pitch * j / (RAIL_BALUSTERS + 1)
            h = RAIL_H - 0.22 - 0.07
            box(f"棂_{i:02d}_{j}", (0.035, 0.035, h), (px, RAIL_Y, Z_FLOOR2 + 0.22 + h / 2), b.floor2)


# ── 围护：墙 / 门 / 窗 ───────────────────────────────────────────────────────

def lattice(name: str, w: float, h: float, center: tuple[float, float, float],
            coll: bpy.types.Collection, plane: str, cols: int, rows: int) -> None:
    """步步锦格心：等距横竖棂。plane 'XZ' = 墙面法向沿 Y；'YZ' = 法向沿 X。"""
    t = LATTICE_BAR
    cx, cy, cz = center
    for i in range(cols + 1):
        u = -w / 2 + w * i / cols
        size = (t, t, h) if plane == "XZ" else (t, t, h)
        pos = (cx + u, cy, cz) if plane == "XZ" else (cx, cy + u, cz)
        box(f"{name}_竖{i}", (size[0] if plane == "XZ" else t, t if plane == "XZ" else size[1], h), pos, coll)
    for j in range(rows + 1):
        v = -h / 2 + h * j / rows
        pos = (cx, cy, cz + v)
        box(f"{name}_横{j}", (w, t, t) if plane == "XZ" else (t, w, t), pos, coll)


def build_gexin_door(name: str, x_center: float, coll: bpy.types.Collection) -> None:
    """一层明间六扇隔扇门（南面 y=0 墙线）。"""
    total = 6 * DOOR_LEAF_W
    for k in range(6):
        lx = x_center - total / 2 + DOOR_LEAF_W * (k + 0.5)
        box(f"{name}_边挺{k}", (0.05, 0.06, DOOR_LEAF_H), (lx - DOOR_LEAF_W / 2, 0.0, DOOR_LEAF_H / 2), coll)
        gex_h = DOOR_LEAF_H * GEXIN_RATIO
        gex_z = DOOR_LEAF_H - gex_h / 2
        lattice(f"{name}_格心{k}", DOOR_LEAF_W - 0.10, gex_h - 0.06, (lx, 0.0, gex_z), coll, "XZ", 4, 7)
        box(f"{name}_绦环{k}", (DOOR_LEAF_W - 0.10, 0.04, 0.18), (lx, 0.0, DOOR_LEAF_H - gex_h - 0.12), coll)
        skirt_h = DOOR_LEAF_H - gex_h - 0.24
        box(f"{name}_裙板{k}", (DOOR_LEAF_W - 0.10, 0.035, skirt_h), (lx, 0.0, skirt_h / 2), coll)
    box(f"{name}_边挺6", (0.05, 0.06, DOOR_LEAF_H), (x_center + total / 2, 0.0, DOOR_LEAF_H / 2), coll)
    box(f"{name}_上槛", (total + 0.10, 0.10, 0.18), (x_center, 0.0, DOOR_LEAF_H + 0.09), coll)


def build_kanchuang(name: str, x0: float, x1: float, y: float, sill: float, height: float,
                    leaves: int, coll: bpy.types.Collection, base: float = 0.0) -> None:
    """`base` 是槛墙底标高：一层窗坐在地面（0），二层窗坐在楼面（Z_FLOOR2）。
    漏掉它会把槛墙从地面一路砌到二层窗台，把整个一层立面封死。"""
    parapet = sill - base
    assert parapet > 0, f"{name}: 窗台 {sill} 必须高于槛墙底 {base}"
    box(f"{name}_槛墙", (x1 - x0, T_WALL, parapet), ((x0 + x1) / 2, y, base + parapet / 2), coll)
    w = (x1 - x0) / leaves
    for k in range(leaves):
        cx = x0 + w * (k + 0.5)
        lattice(f"{name}_格心{k}", w - 0.08, height - 0.08, (cx, y, sill + height / 2), coll, "XZ", 3, 5)
        box(f"{name}_边挺{k}", (0.05, 0.06, height), (x0 + w * k, y, sill + height / 2), coll)
    box(f"{name}_边挺{leaves}", (0.05, 0.06, height), (x1, y, sill + height / 2), coll)
    box(f"{name}_上槛", (x1 - x0, 0.10, 0.14), ((x0 + x1) / 2, y, sill + height + 0.07), coll)


def build_walls(b: Build) -> None:
    # 山墙：随举折折线收顶，逐段砌
    for x, tag in ((BAY_X[0] - D_JIN / 2 - T_WALL / 2, "西"), (BAY_X[-1] + D_JIN / 2 + T_WALL / 2, "东")):
        for (y0, z0), (y1, z1) in zip(PURLINS, PURLINS[1:]):
            profile = [(y0, 0.0), (y1, 0.0), (y1, z1), (y0, z0)]
            bm = bmesh.new()
            verts = [bm.verts.new((0.0, u, v)) for u, v in profile]
            bm.faces.new(verts)
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            ret = bmesh.ops.extrude_face_region(bm, geom=list(bm.faces))
            moved = [e for e in ret["geom"] if isinstance(e, bmesh.types.BMVert)]
            bmesh.ops.translate(bm, vec=(T_WALL, 0.0, 0.0), verts=moved)
            bmesh.ops.translate(bm, vec=(x - T_WALL / 2, 0.0, 0.0), verts=bm.verts)
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            _link(f"山墙_{tag}_{y0:.2f}", bm, b.envelope)

    box("后檐墙", (BAY_X[-1] - BAY_X[0] + D_JIN + 2 * T_WALL, T_WALL, Z_EAVE),
        ((BAY_X[0] + BAY_X[-1]) / 2, Y_YANHOU + T_WALL / 2, Z_EAVE / 2), b.envelope)

    # 南立面：明间隔扇门 + 两次间槛窗；二层通长槛窗
    build_gexin_door("隔扇门", (BAY_X[1] + BAY_X[2]) / 2, b.envelope)
    build_kanchuang("次间槛窗西", BAY_X[0], BAY_X[1], 0.0, SILL_H, WIN_H, 4, b.envelope)
    build_kanchuang("次间槛窗东", BAY_X[2], BAY_X[3], 0.0, SILL_H, WIN_H, 4, b.envelope)
    build_kanchuang("二层南槛窗", BAY_X[0], BAY_X[3], 0.0, WIN2_SILL, WIN2_H, 12, b.envelope,
                    base=Z_FLOOR2)
    # 南立面补壁：一层门窗顶 → 二层窗台，以及二层窗顶 → 檐口，两条带都要封上
    band_lo_z0, band_lo_z1 = DOOR_LEAF_H + 0.18, Z_FLOOR2
    box("南立面_腰壁", (BAY_X[-1] - BAY_X[0], T_PLANK, band_lo_z1 - band_lo_z0),
        ((BAY_X[0] + BAY_X[-1]) / 2, 0.0, (band_lo_z0 + band_lo_z1) / 2), b.envelope)
    box("南立面_檐下壁", (BAY_X[-1] - BAY_X[0], T_PLANK, Z_EAVE - (WIN2_SILL + WIN2_H)),
        ((BAY_X[0] + BAY_X[-1]) / 2, 0.0, (WIN2_SILL + WIN2_H + Z_EAVE) / 2), b.envelope)

    # 后堂隔断（中柱线 y=7.50）：两次间砌板壁，明间留通道，李大娘由此进出厨房
    for x0, x1 in ((BAY_X[0], BAY_X[1]), (BAY_X[2], BAY_X[3])):
        box(f"后堂板壁_{x0:.2f}", (x1 - x0, T_PLANK, Z_BEAM1),
            ((x0 + x1) / 2, Y_ZHONG, Z_BEAM1 / 2), b.envelope)

    # 二层隔墙：走廊北侧客房墙 + 客房之间隔墙
    for name, x0, x1 in ROOM_SPANS:
        box(f"{name}_南墙", (x1 - x0, T_PLANK, Z_BEAM2 - Z_FLOOR2),
            ((x0 + x1) / 2, Y_GALLERY_N, (Z_FLOOR2 + Z_BEAM2) / 2), b.envelope)
        box(f"{name}_东隔墙", (T_PLANK, Y_YANHOU - Y_GALLERY_N, Z_BEAM2 - Z_FLOOR2),
            (x1, (Y_GALLERY_N + Y_YANHOU) / 2, (Z_FLOOR2 + Z_BEAM2) / 2), b.envelope)

    # 门窗：先在墙上挖真洞，再把门扇/窗棂摆进洞口
    dw, dh = ROOM_DOOR
    for name, x0, x1 in ROOM_SPANS:
        dx = (x0 + x1) / 2
        cut_opening(f"{name}_门洞", (dw, T_PLANK * 4, dh), (dx, Y_GALLERY_N, Z_FLOOR2 + dh / 2), b.envelope)
    cut_opening("逍遥房东窗洞", (T_WALL * 4, XY_WINDOW[0], XY_WINDOW[1]),
                (BAY_X[-1] + D_JIN / 2 + T_WALL / 2, WIN_EAST_Y, WIN2_SILL + XY_WINDOW[1] / 2), b.envelope)

    for name, x0, x1 in ROOM_SPANS:
        dx = (x0 + x1) / 2
        box(f"{name}_门框左", (0.05, 0.10, dh), (dx - dw / 2, Y_GALLERY_N, Z_FLOOR2 + dh / 2), b.envelope)
        box(f"{name}_门框右", (0.05, 0.10, dh), (dx + dw / 2, Y_GALLERY_N, Z_FLOOR2 + dh / 2), b.envelope)
        box(f"{name}_门楣", (dw + 0.10, 0.10, 0.10), (dx, Y_GALLERY_N, Z_FLOOR2 + dh + 0.05), b.envelope)
        # 门扇朝走廊一侧微凸，免得与墙面共面而在渲染里消失
        box(f"{name}_门扇", (dw - 0.04, 0.045, dh - 0.03),
            (dx, Y_GALLERY_N - T_PLANK / 2 - 0.025, Z_FLOOR2 + (dh - 0.03) / 2), b.envelope)

    x_win = BAY_X[-1] + D_JIN / 2 + T_WALL / 2
    lattice("逍遥房东窗", XY_WINDOW[0], XY_WINDOW[1],
            (x_win, WIN_EAST_Y, WIN2_SILL + XY_WINDOW[1] / 2), b.envelope, "YZ", 4, 3)
    for dy in (-XY_WINDOW[0] / 2, XY_WINDOW[0] / 2):
        box(f"逍遥房东窗框_{dy:+.2f}", (T_WALL, 0.06, XY_WINDOW[1] + 0.12),
            (x_win, WIN_EAST_Y + dy, WIN2_SILL + XY_WINDOW[1] / 2), b.envelope)
    for dz in (-XY_WINDOW[1] / 2, XY_WINDOW[1] / 2):
        box(f"逍遥房东窗框_z{dz:+.2f}", (T_WALL, XY_WINDOW[0] + 0.12, 0.06),
            (x_win, WIN_EAST_Y, WIN2_SILL + XY_WINDOW[1] / 2 + dz), b.envelope)


def build_ground(b: Build) -> None:
    box("地坪", (BAY_X[-1] - BAY_X[0] + 1.2, Y_YANHOU - BAY_Y[0] + 1.2, 0.20),
        ((BAY_X[0] + BAY_X[-1]) / 2, (BAY_Y[0] + Y_YANHOU) / 2, -0.10), b.ground)
    bw, bd, bh = BRICK
    step = bw + BRICK_JOINT
    xs = frange(-0.12, 10.62 - bw, step)
    ys = frange(Y_JINQIAN, Y_ZHONG - bd, bd + BRICK_JOINT)
    for j, yy in enumerate(ys):
        offset = (step / 2) if j % 2 else 0.0
        for i, xx in enumerate(xs):
            box(f"青砖_{j}_{i}", (bw, bd, bh), (xx + bw / 2 + offset, yy + bd / 2, bh / 2), b.ground)


def build_furniture(b: Build) -> None:
    for i, (tx, ty) in enumerate(HALL_TABLES):
        box(f"方桌{i}_面", (0.92, 0.92, 0.06), (tx, ty, 0.75), b.furniture)
        for sx in (-0.40, 0.40):
            for sy in (-0.40, 0.40):
                box(f"方桌{i}_腿_{sx}_{sy}", (0.07, 0.07, 0.72), (tx + sx, ty + sy, 0.36), b.furniture)
        for sy in (-0.72, 0.72):
            box(f"长凳{i}_{sy}_面", (0.92, 0.26, 0.05), (tx, ty + sy, 0.445), b.furniture)
            for sx in (-0.38, 0.38):
                box(f"长凳{i}_{sy}_腿{sx}", (0.06, 0.06, 0.42), (tx + sx, ty + sy, 0.21), b.furniture)
    box("柜台_长边", (2.40, 0.60, 1.05), (1.40, 6.90, 0.525), b.furniture)
    box("柜台_短边", (0.60, 1.20, 1.05), (0.50, 6.00, 0.525), b.furniture)

    rx0, rx1 = ROOM_SPANS[-1][1], ROOM_SPANS[-1][2]
    box("木床_面", (1.90, 0.90, 0.10), (rx0 + 1.30, Y_YANHOU - 0.60, Z_FLOOR2 + 0.40), b.furniture)
    for sx in (-0.88, 0.88):
        for sy in (-0.38, 0.38):
            box(f"木床_腿{sx}_{sy}", (0.08, 0.08, 0.35),
                (rx0 + 1.30 + sx, Y_YANHOU - 0.60 + sy, Z_FLOOR2 + 0.175), b.furniture)
    box("木床_屏", (1.90, 0.05, 0.55), (rx0 + 1.30, Y_YANHOU - 0.16, Z_FLOOR2 + 0.72), b.furniture)
    box("五斗柜", (0.80, 0.42, 1.05), (rx0 + 0.45, 10.20, Z_FLOOR2 + 0.525), b.furniture)
    box("矮凳", (0.36, 0.28, 0.32), (rx0 + 0.50, 9.60, Z_FLOOR2 + 0.16), b.furniture)
    for k, zy in enumerate((9.75, 10.95)):
        box(f"立轴{k}", (0.02, 0.44, 1.30), (rx0 + 0.03, zy, Z_FLOOR2 + 1.55), b.furniture)


# ── QC ──────────────────────────────────────────────────────────────────────

QC_VIEWS: tuple[tuple[str, tuple[float, float, float], tuple[float, float, float], float], ...] = (
    ("qc_01_东南鸟瞰", (22.0, -16.0, 14.0), (5.25, 6.0, 3.0), 35.0),
    ("qc_02_大堂内景", (5.25, 1.90, 1.62), (5.25, 7.5, 2.6), 20.0),
    ("qc_03_二层走廊", (10.05, 8.25, 5.35), (0.30, 8.25, 4.9), 24.0),
    ("qc_04_逍遥房内", (7.55, 9.35, 5.35), (10.3, 11.3, 4.4), 20.0),
)


def render_qc(out_dir: Path, hide_roof_for: frozenset[str]) -> None:
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.resolution_x, scene.render.resolution_y = 1600, 900
    scene.render.image_settings.file_format = "PNG"
    shading = scene.display.shading
    shading.light = "STUDIO"
    shading.color_type = "SINGLE"
    shading.show_cavity = True
    cam_data = bpy.data.cameras.new("QC_CAM")
    cam = bpy.data.objects.new("QC_CAM", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam
    roof = bpy.data.collections.get("20_屋面")
    for name, loc, target, lens in QC_VIEWS:
        cam_data.lens = lens
        cam.location = Vector(loc)
        direction = Vector(target) - Vector(loc)
        cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
        if roof is not None:
            roof.hide_render = name in hide_roof_for
        scene.render.filepath = str(out_dir / f"{name}.png")
        bpy.ops.render.render(write_still=True)
        print(f"  QC → {name}.png", flush=True)
    if roof is not None:
        roof.hide_render = False


# ── 自检 ────────────────────────────────────────────────────────────────────

def assertions() -> None:
    assert BAY_X[-1] == 10.50, "总面阔必须 10.50"
    assert BAY_Y[-1] == 12.00, "总进深必须 12.00"
    ys = [y for y, _ in PURLINS]
    assert ys == sorted(ys), "檩位必须沿 y 单调"
    half = PURLINS[: len(PURLINS) // 2 + 1]
    slopes = [(z1 - z0) / (y1 - y0) for (y0, z0), (y1, z1) in zip(half, half[1:])]
    assert all(b > a for a, b in zip(slopes, slopes[1:])), f"举折必须逐段变陡，实得 {slopes}"
    assert abs(PURLINS[3][1] - Z_RIDGE) < 1e-9, "脊檩标高须等于 Z_RIDGE"
    assert abs(STAIR_STEPS * (Z_FLOOR2 / STAIR_STEPS) - Z_FLOOR2) < 1e-9, "楼梯总高须等于二层楼面"
    rise = Z_FLOOR2 / STAIR_STEPS
    assert 0.15 <= rise <= 0.23, f"踏步高 {rise:.3f} 超出可走范围"
    assert RAIL_X0 >= STAIR_X0 + STAIR_WIDTH, "栏杆起点须让开楼梯口，否则走廊下不去楼梯"
    rail_pitch = (BAY_X[-1] - RAIL_X0) / RAIL_POSTS
    assert 0.90 <= rail_pitch <= 1.15, f"栏杆档距 {rail_pitch:.3f} 超出常规"
    assert sum(x1 - x0 for _, x0, x1 in ROOM_SPANS) == BAY_X[-1], "客房面阔之和须等于总面阔"
    assert ROOM_SPANS[-1][0] == "李逍遥房" and ROOM_SPANS[-1][2] == BAY_X[-1], "逍遥房须在东端"
    for y in (0.0, 3.0, 6.0, 9.0, 12.0):
        assert Z_EAVE - 1e-9 <= purlin_z(y) <= Z_RIDGE + 1e-9, f"y={y} 屋面标高越界"
    win_band = (WIN2_SILL, WIN2_SILL + WIN2_H)
    for z in TIE_LEVELS_2:
        assert not (win_band[0] < z < win_band[1]), f"穿枋标高 {z} 落在窗洞带 {win_band} 内，会横穿窗口"
    w0, w1 = WIN_EAST_Y - XY_WINDOW[0] / 2, WIN_EAST_Y + XY_WINDOW[0] / 2
    for cy in BAY_Y:
        assert not (w0 - D_JIN / 2 < cy < w1 + D_JIN / 2), f"y={cy} 的柱子落在东窗洞口内"
    assert Y_GALLERY_N < w0 and w1 < Y_YANHOU, "东窗须落在李逍遥房进深范围内"


def new_collection(name: str, parent: bpy.types.Collection) -> bpy.types.Collection:
    coll = bpy.data.collections.new(name)
    parent.children.link(coll)
    return coll


def wipe() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)


def main() -> int:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("out", nargs="?", default=str(DEFAULT_OUT))
    parser.add_argument("--qc", action="store_true")
    parser.add_argument("--glb", action="store_true",
                        help="另导出 glTF-Binary（网页预览 / 外部工具用；.blend 仍是唯一真相）")
    args = parser.parse_args(argv)

    assertions()
    print("契约自检通过", flush=True)

    wipe()
    root = bpy.data.collections.new("余杭客栈")
    bpy.context.scene.collection.children.link(root)
    b = Build(
        root=root,
        frame=new_collection("10_木构架", root),
        roof=new_collection("20_屋面", root),
        floor2=new_collection("30_楼面", root),
        envelope=new_collection("40_围护", root),
        ground=new_collection("50_地面", root),
        furniture=new_collection("60_家具", root),
    )

    n_col = build_plinths_and_columns(b)
    build_ties(b)
    build_purlins_rafters_sheathing(b)
    build_tiles(b)
    build_floor2(b)
    build_stair(b)
    build_railing(b)
    build_walls(b)
    build_ground(b)
    build_furniture(b)

    total = len(bpy.data.objects)
    print(f"柱 {n_col} 根；对象总数 {total}", flush=True)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out))
    print(f"已写出 {out}", flush=True)

    if args.glb:
        glb = out.with_suffix(".glb")
        bpy.ops.export_scene.gltf(filepath=str(glb), export_format="GLB",
                                  use_selection=False, export_apply=True,
                                  export_materials="NONE", export_cameras=False,
                                  export_lights=False, export_yup=True)
        print(f"已导出 {glb}（{glb.stat().st_size // 1024} KB）", flush=True)

    if args.qc:
        render_qc(out.parent, frozenset({"qc_02_大堂内景", "qc_03_二层走廊", "qc_04_逍遥房内"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
