# -*- coding: utf-8 -*-
"""sk1 S 档 previz 运行库 —— `shots/shotNN/shotNN_previz.py` 只调 `run(__file__)`，本镜编排只写同目录 `previz_config.toml`。

为什么 A 档引擎之外还要这一层（rule 4h ③：S 档 per-shot Python + 共享库，绝不复制引擎）：
  · 镜内切镜：机位按 `切` 分段，关键帧 t 直接是 shot md `动作:` 的全镜时刻，不拆成段内局部时间；
  · 变焦、摇镜、跟拍（机位 / 看向可挂在角色或道具上）；
  · 一镜里城景与套景来回切（套景从 `sets/*.blend` 链接进来，停在城外的「影棚区」）；
  · 人物用 `previz_rig.PrevizRig` 关节人（手有指节），姿态按「基础 + 头 + 手臂」拼；
  · workbench 灰模渲染，全城 97 万面也能逐帧渲。

坐标：`["全局"]."坐标系"` 给默认系（["Place", X] / ["世界"] / ["布景", 名]），角色 / 道具 / 人群 / 机位里裸写的
[x, y(, z)] 都在这个系里；也可逐项写成完整 spec。朝向一律「系内角度，0 ＝ +X、90 ＝ +Y（逆时针）」。
"""
from __future__ import annotations

import math
import random
import re
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

import bpy
from mathutils import Euler, Matrix, Vector
from mathutils.bvhtree import BVHTree

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_bianjing as bj  # noqa: E402
from build_bianjing import Batch, PlanError, mono_hermite  # noqa: E402

SETS_DIR = bj.BLENDER_DIR / "sets"
STAGE_LOT = Vector((-30000.0, -30000.0, 0.0))        # 套景停放区：在全城地面（±9 km）之外，镜头远裁剪收到 3 km 就看不到城

SCHEMA: dict[str, set[str]] = {
    "全局": {"shot", "fps", "total_sec", "分辨率", "坐标系"},
    "布景": {"名", "集合", "位置", "朝向"},
    "机位": {"t", "位置", "看向", "焦距", "切"},
    "角色": {"名", "色", "身高", "形", "关键帧"},
    "角色.关键帧": {"t", "位置", "朝向", "姿态", "看", "显", "系"},
    "道具": {"名", "型", "尺寸", "色", "挂", "偏移", "关键帧", "阵列"},
    "道具.关键帧": {"t", "位置", "朝向", "显", "桅角", "开", "尺寸", "系"},
    "人群": {"名", "数", "区域", "方向", "速度", "种子", "起", "止", "色", "身高", "系"},
}

COLORS: dict[str, tuple[float, float, float]] = {
    "绿": (0.10, 0.75, 0.15), "蓝": (0.10, 0.30, 0.90), "红": (0.85, 0.10, 0.10), "青": (0.10, 0.80, 0.80),
    "黄": (0.90, 0.80, 0.10), "紫": (0.55, 0.15, 0.85), "橙": (0.95, 0.45, 0.05), "粉": (0.95, 0.45, 0.65),
    "米": (0.80, 0.74, 0.62), "白": (0.90, 0.90, 0.90), "灰": (0.45, 0.45, 0.47), "深灰": (0.22, 0.22, 0.24),
    "木": (0.55, 0.42, 0.30), "剪影": (0.30, 0.31, 0.33),
}
CITY_GREY = (0.78, 0.78, 0.76, 1.0)
WATER = (0.30, 0.34, 0.38, 1.0)


def die(msg: str) -> None:
    raise PlanError(msg)


def check_keys(table: dict, allowed: set[str], where: str) -> None:
    bad = set(table) - allowed
    if bad:
        die(f"{where} 出现未知键 {sorted(bad)}；合法键＝{sorted(allowed)}")


# ── 坐标系与 spec ─────────────────────────────────────────────────────────────
@dataclass
class Ctx:
    cfg_path: Path
    fps: int
    total: float
    default_frame: list
    sets: dict[str, Matrix] = field(default_factory=dict)
    tracks: dict[str, "Track"] = field(default_factory=dict)


def frame_matrix(ctx: Ctx, spec: list) -> Matrix:
    head = str(spec[0])
    if head == "世界":
        return Matrix.Identity(4)
    if head == "Place":
        return bj.FRAMES[str(spec[1])].matrix()
    if head == "布景":
        if str(spec[1]) not in ctx.sets:
            die(f"坐标系 {spec}：本镜没有这个布景")
        return ctx.sets[str(spec[1])]
    die(f"坐标系写法认不出 {spec}")
    return Matrix.Identity(4)


def split_frame(ctx: Ctx, spec: list) -> tuple[Matrix, list[float]]:
    """完整 spec → (系矩阵, 局部数值)；裸数组 → 默认系。"""
    if spec and isinstance(spec[0], (int, float)):
        return frame_matrix(ctx, ctx.default_frame), [float(v) for v in spec]
    head = str(spec[0])
    if head == "世界":
        return Matrix.Identity(4), [float(v) for v in spec[1:]]
    if head in ("Place", "布景"):
        return frame_matrix(ctx, spec[:2]), [float(v) for v in spec[2:]]
    die(f"位置写法认不出 {spec}")
    return Matrix.Identity(4), []


def yaw_of(m: Matrix) -> float:
    return math.degrees(m.to_euler().z)


@dataclass
class Track:
    """逐帧已算好的世界位置与朝向（度，世界系），供跟拍 / 骑乘 / 看向引用。"""
    pos: list[Vector]
    yaw: list[float]
    height: float


def resolve_point(ctx: Ctx, spec: list, f: int) -> Vector:
    head = str(spec[0]) if spec and not isinstance(spec[0], (int, float)) else ""
    if head in ("角色", "道具"):
        tr = ctx.tracks.get(str(spec[1]))
        if tr is None:
            die(f"{spec}：找不到「{spec[1]}」的轨迹")
        dx, dy, dz = (float(v) for v in spec[2:5])
        m, _ = split_frame(ctx, [0.0])
        r = m.to_3x3()
        return tr.pos[f] + r @ Vector((dx, dy, 0.0)) + Vector((0.0, 0.0, dz))
    if head in ("角色朝向", "道具朝向"):
        tr = ctx.tracks.get(str(spec[1]))
        if tr is None:
            die(f"{spec}：找不到「{spec[1]}」的轨迹")
        fwd, left, dz = (float(v) for v in spec[2:5])
        a = math.radians(tr.yaw[f])
        return tr.pos[f] + Vector((math.cos(a) * fwd - math.sin(a) * left, math.sin(a) * fwd + math.cos(a) * left, dz))
    if head in ("汴河@A", "汴河@B", "汴河@C") or head.startswith("汴河@") or re.fullmatch(r"WP\d+(看向)?", head):
        return bj.resolve_spec(bj.aerial_world(), spec, "位置", ctx.cfg_path)
    m, vals = split_frame(ctx, spec)
    if len(vals) != 3:
        die(f"{spec}：需要 x, y, z 三个数")
    return m @ Vector(vals)


# ── 插值 ──────────────────────────────────────────────────────────────────────
def unwrap(angles: list[float]) -> list[float]:
    out = [angles[0]]
    for a in angles[1:]:
        d = (a - out[-1] + 180.0) % 360.0 - 180.0
        out.append(out[-1] + d)
    return out


def hold_or_hermite(ts: list[float], vs: list[float], t: float) -> float:
    return mono_hermite(ts, vs, t, False) if len(ts) > 1 else vs[0]


def step_value(ts: list[float], vs: list, t: float):
    i = max([k for k, tk in enumerate(ts) if tk <= t + 1e-9], default=0)
    return vs[i]


# ── 道具库（原点＝底面中心，前＝+X；尺寸只给到机位 / 尺度 / 遮挡需要的程度）──────────────────────────
def mesh_from(b: Batch, name: str, col: bpy.types.Collection) -> bpy.types.Object:
    return b.finish(name, col)


def prop_geometry(kind: str, size: list[float]) -> tuple[Batch, dict[str, Vector]]:
    """返回几何与挂点（mast_pivot / saddle / hinge 等，道具局部坐标）。"""
    b = Batch()
    pts: dict[str, Vector] = {}
    s = size
    if kind == "盒":
        b.box((-s[0] / 2, -s[1] / 2, 0.0), (s[0] / 2, s[1] / 2, s[2]))
    elif kind == "柱":
        b.cyl(0.0, 0.0, 0.0, s[1], s[0], 12)
    elif kind == "球":
        b.ball((0.0, 0.0, s[0]), s[0])
    elif kind in ("驴", "骡", "马"):
        k = {"驴": 1.0, "骡": 1.15, "马": 1.4}[kind] * (s[0] if s else 1.0)
        b.box((-0.55 * k, -0.22 * k, 0.62 * k), (0.55 * k, 0.22 * k, 1.05 * k))
        b.poly_solid([Vector((0.45 * k, -0.1 * k, 0.9 * k)), Vector((0.75 * k, -0.1 * k, 1.35 * k)),
                      Vector((0.75 * k, 0.1 * k, 1.35 * k)), Vector((0.45 * k, 0.1 * k, 0.9 * k))],
                     [Vector((0.6 * k, -0.1 * k, 0.8 * k)), Vector((0.9 * k, -0.1 * k, 1.25 * k)),
                      Vector((0.9 * k, 0.1 * k, 1.25 * k)), Vector((0.6 * k, 0.1 * k, 0.8 * k))])
        b.box((0.75 * k, -0.1 * k, 1.12 * k), (1.15 * k, 0.1 * k, 1.38 * k))
        for dy in (-0.06, 0.06):
            b.box((0.78 * k, dy * k - 0.02 * k, 1.38 * k), (0.84 * k, dy * k + 0.02 * k, 1.6 * k))
        for dx in (-0.45, 0.45):
            for dy in (-0.15, 0.15):
                b.cyl(dx * k, dy * k, 0.0, 0.66 * k, 0.05 * k, 6)
        pts["saddle"] = Vector((0.0, 0.0, 1.05 * k))
    elif kind == "骆驼":
        b.box((-0.9, -0.35, 1.2), (0.9, 0.35, 1.8))
        b.ball((-0.35, 0.0, 1.9), 0.35)
        b.ball((0.35, 0.0, 1.9), 0.35)
        b.poly_solid([Vector((0.8, -0.12, 1.5)), Vector((1.3, -0.12, 2.2)), Vector((1.3, 0.12, 2.2)), Vector((0.8, 0.12, 1.5))],
                     [Vector((1.0, -0.12, 1.4)), Vector((1.45, -0.12, 2.1)), Vector((1.45, 0.12, 2.1)), Vector((1.0, 0.12, 1.4))])
        b.box((1.3, -0.12, 2.05), (1.75, 0.12, 2.3))
        for dx in (-0.7, 0.7):
            for dy in (-0.22, 0.22):
                b.cyl(dx, dy, 0.0, 1.25, 0.08, 6)
    elif kind == "太平车":
        b.box((-2.0, -1.0, 0.9), (2.0, 1.0, 1.3))
        b.box((-2.0, -1.0, 1.3), (2.0, -0.9, 1.9))
        b.box((-2.0, 0.9, 1.3), (2.0, 1.0, 1.9))
        for dy in (-1.1, 1.1):
            b.prism_y(dy - 0.08, dy + 0.08, [(0.8 * math.cos(math.pi * k / 6), 0.8 + 0.8 * math.sin(math.pi * k / 6)) for k in range(12)])
        for dy in (-0.5, 0.5):
            b.box((2.0, dy - 0.05, 1.0), (4.2, dy + 0.05, 1.1))
        b.cyl(0.0, 0.0, 0.55, 0.9, 0.12, 8)
        pts["bell"] = Vector((0.0, 0.0, 0.7))
    elif kind == "平头车":
        b.box((-1.3, -0.8, 0.7), (1.3, 0.8, 0.85))
        for dy in (-0.9, 0.9):
            b.prism_y(dy - 0.06, dy + 0.06, [(0.6 * math.cos(math.pi * k / 6), 0.6 + 0.6 * math.sin(math.pi * k / 6)) for k in range(12)])
        for dy in (-0.4, 0.4):
            b.box((1.3, dy - 0.05, 0.75), (3.2, dy + 0.05, 0.85))
    elif kind in ("纲船", "小船", "方头船"):
        ln, wd, hh = (s + [16.0, 4.0, 3.0][len(s):])[:3] if kind == "纲船" else (s + [6.0, 1.8, 0.8][len(s):])[:3]
        b.box((-ln / 2, -wd / 2, -0.6), (ln / 2, wd / 2, 1.0))
        if kind == "纲船":
            b.box((-ln * 0.3, -wd * 0.4, 1.0), (ln * 0.2, wd * 0.4, hh))
            pts["mast_pivot"] = Vector((ln * 0.25, 0.0, hh))       # 转轴取在船篷顶高：放倒的桅杆砸平落在船篷上，不插进船篷里
        elif kind == "方头船":
            for k in range(3):
                b.cyl(ln / 2 - 0.4, -0.5 + 0.5 * k, 1.0, 4.0, 0.04, 6)
    elif kind == "轿子":
        b.box((-0.5, -0.45, 0.45), (0.5, 0.45, 1.75))
        b.hip(0.0, 0.0, 1.2, 1.1, 1.75, 0.35)
        for dy in (-0.52, 0.52):
            b.box((-1.7, dy - 0.04, 0.95), (1.7, dy + 0.04, 1.05))
        for k in range(9):
            b.ball((-0.45 + 0.11 * k, 0.4 * math.sin(k), 2.15), 0.14)
    elif kind == "伞":
        b.cyl(0.0, 0.0, 0.0, s[0] if s else 2.0, 0.02, 6)
        b.hip(0.0, 0.0, 2.2, 2.2, (s[0] if s else 2.0) - 0.35, 0.35)
    elif kind == "话筒":
        b.cyl(0.0, 0.0, 0.0, 0.18, 0.018, 8)
        b.ball((0.0, 0.0, 0.2), 0.035)
    elif kind == "本子":
        b.box((-0.075, -0.105, 0.0), (0.075, 0.105, 0.02))
    elif kind == "长杆":
        b.cyl(0.0, 0.0, 0.0, s[0], s[1] if len(s) > 1 else 0.03, 6)
    elif kind == "骨朵":
        b.cyl(0.0, 0.0, 0.0, 1.2, 0.02, 6)
        b.ball((0.0, 0.0, 1.25), 0.07)
    elif kind == "旗":
        b.cyl(0.0, 0.0, 0.0, 3.2, 0.025, 6)
        b.box((0.03, -0.01, 2.2), (1.0, 0.01, 3.1))
    elif kind == "柳枝":
        b.cyl(0.0, 0.0, 0.0, 0.45, 0.006, 5)
        for k in range(4):
            b.ball((0.02 * k, 0.0, 0.18 + 0.08 * k), 0.025)
    elif kind == "门扇":
        b.box((0.0, -0.03, 0.0), (s[0], 0.03, s[1]))
        pts["hinge"] = Vector((0.0, 0.0, 0.0))
    elif kind == "纸楼阁":
        b.box((-0.6, -0.6, 0.0), (0.6, 0.6, 0.9))
        b.hip(0.0, 0.0, 1.5, 1.5, 0.9, 0.3)
        b.box((-0.45, -0.45, 1.2), (0.45, 0.45, 1.8))
        b.hip(0.0, 0.0, 1.2, 1.2, 1.8, 0.35)
    elif kind == "挑担":
        b.box((-0.8, -0.02, 0.0), (0.8, 0.02, 0.05))
        for dx in (-0.75, 0.75):
            b.cyl(dx, 0.0, -0.9, -0.5, 0.22, 10)
    elif kind == "绳":
        b.box((0.0, -0.01, -0.01), (1.0, 0.01, 0.01))
    else:
        die(f"道具型「{kind}」不认识")
    return b, pts


# ── 配置载入 ────────────────────────────────────────────────────────────────────
def load(cfg_path: Path) -> dict:
    cfg = tomllib.loads(cfg_path.read_text(encoding="utf-8"))
    bad = set(cfg) - {"全局", "布景", "机位", "角色", "道具", "人群"}
    if bad:
        die(f"{cfg_path}：未知段 {sorted(bad)}")
    check_keys(cfg.get("全局", {}), SCHEMA["全局"] | {"城景", "远裁剪"}, "[全局]")
    for sec in ("布景", "机位", "角色", "道具", "人群"):
        for item in cfg.get(sec, []):
            check_keys(item, SCHEMA[sec] | ({"系"} if sec in ("角色", "道具") else set()), f"[[{sec}]]")
            for kf in item.get("关键帧", []):
                check_keys(kf, SCHEMA[f"{sec}.关键帧"], f"[[{sec}.关键帧]] of {item.get('名')}")
            if "关键帧" in item and any(b["t"] < a["t"] for a, b in zip(item["关键帧"], item["关键帧"][1:])):
                die(f"[[{sec}]]「{item.get('名')}」关键帧 t 必须递增")
    g = cfg["全局"]
    keys = cfg.get("机位", [])
    if len(keys) < 2 or keys[0]["t"] != 0.0 or abs(keys[-1]["t"] - float(g["total_sec"])) > 1e-6:
        die(f"{cfg_path}：[[机位]] 至少两帧，且 t 从 0 到 total_sec")
    for k0, k1 in zip(keys, keys[1:]):
        if k1["t"] < k0["t"] or (k1["t"] == k0["t"] and not k1.get("切")):
            die(f"{cfg_path}：机位 t 必须递增；同一时刻两帧只许后一帧标「切」（t={k1['t']}）")
    for item in cfg.get("角色", []) + cfg.get("道具", []):
        for kf in item.get("关键帧", []):
            if kf["t"] > float(g["total_sec"]) + 1e-6:
                die(f"「{item['名']}」关键帧 t={kf['t']} 超出 total_sec")
    return cfg


# ── 布景（套景）─────────────────────────────────────────────────────────────────
def link_sets(ctx: Ctx, items: list[dict]) -> list[bpy.types.Object]:
    placed: list[bpy.types.Object] = []
    col = bj.collection("SETS")
    for i, it in enumerate(items):
        name = str(it["名"])
        path = SETS_DIR / f"{name}.blend"
        if not path.is_file():
            die(f"布景「{name}」没有 {path}（先跑 tools/build_sk1_sets.py）")
        cname = str(it.get("集合", f"SET_{name}"))
        with bpy.data.libraries.load(str(path), link=False) as (src, dst):
            if cname not in src.collections:
                die(f"{path} 里没有集合 {cname}")
            dst.collections = [cname]
        src_col = dst.collections[0]
        if "位置" in it:
            m_frame, vals = split_frame(ctx, list(it["位置"]))
            loc = m_frame @ Vector((vals + [0.0, 0.0, 0.0])[:3])
            yaw = yaw_of(m_frame) + float(it.get("朝向", 0.0))
        else:
            loc, yaw = STAGE_LOT + Vector((2000.0 * i, 0.0, 0.0)), float(it.get("朝向", 0.0))
        m = Matrix.Translation(loc) @ Matrix.Rotation(math.radians(yaw), 4, "Z")
        for ob in list(src_col.all_objects):
            ob.matrix_world = m @ ob.matrix_world
            col.objects.link(ob)
            placed.append(ob)
        ctx.sets[name] = m
    return placed


# ── 地面探针：从深度图层实例里收三角面建 BVH（集合实例的桥面也算），人与车贴着它走 ─────────────────
class Ground:
    def __init__(self, boxes: list[tuple[float, float, float, float]]) -> None:
        verts: list[Vector] = []
        faces: list[tuple[int, int, int]] = []
        if boxes:
            bpy.context.view_layer.update()
            dg = bpy.context.evaluated_depsgraph_get()
            for inst in dg.object_instances:
                ob = inst.object
                if ob.type != "MESH" or ob.original.get("look"):      # look 层（房、树、行人）不当地面，只打布局网格
                    continue
                holder = inst.parent.original if inst.is_instance and inst.parent else ob.original
                if any(c.name == "PREVIZ" for c in holder.users_collection):
                    continue
                mw = inst.matrix_world.copy()
                bb = [mw @ Vector(c) for c in ob.bound_box]
                x0, x1 = min(v.x for v in bb), max(v.x for v in bb)
                y0, y1 = min(v.y for v in bb), max(v.y for v in bb)
                if not any(x0 <= bx1 and x1 >= bx0 and y0 <= by1 and y1 >= by0 for bx0, bx1, by0, by1 in boxes):
                    continue
                me = ob.data
                base = len(verts)
                verts += [mw @ v.co for v in me.vertices]
                for poly in me.polygons:
                    vs = list(poly.vertices)
                    for k in range(1, len(vs) - 1):
                        faces.append((base + vs[0], base + vs[k], base + vs[k + 1]))
        self.bvh = BVHTree.FromPolygons(verts, faces, all_triangles=True) if faces else None
        self.tris = len(faces)

    def z_at(self, x: float, y: float, hint: float, floor: float) -> float:
        # 探针起点不低于本系街面：一旦跟着跳板掉到水面 / 河床，再从下面往下打只会打到实体内壁，人就一路埋在地里走
        start = max(hint, floor)
        if self.bvh is None:
            return start
        down = Vector((0.0, 0.0, -1.0))
        low = self.bvh.ray_cast(Vector((x, y, start + 1.6)), down, 6.0)
        if low[0] is not None and low[0].z >= floor - 0.5:
            return low[0].z
        # 探针落进水面 / 河床：可能人其实在桥面上（拱顶桥面比街面高 2.7 m，从街面 +1.6 m 往下打会从桥面底下穿过去）。
        # 从街面 +4 m 再打一次，只认朝上的面、且不高于街面 +4 m——雨棚这类更高的顶板不会被当成地面
        high = self.bvh.ray_cast(Vector((x, y, floor + 4.0)), down, 6.0)
        if high[0] is not None and high[1].z > 0.3 and floor - 0.5 <= high[0].z <= floor + 4.0:
            return high[0].z
        if low[0] is not None:
            return low[0].z
        far = self.bvh.ray_cast(Vector((x, y, start + 40.0)), down, 90.0)
        return far[0].z if far[0] is not None else start


# ── 轨迹 ──────────────────────────────────────────────────────────────────────
def entity_frame(ctx: Ctx, item: dict) -> list:
    return list(item.get("系", ctx.default_frame))


def key_point(ctx: Ctx, spec: list, frame_spec: list, f: int) -> tuple[Vector, bool]:
    """→ (世界点, z 是否给定)。裸 [x, y] 在实体默认系里、z 待贴地。"""
    if spec and isinstance(spec[0], (int, float)):
        m = frame_matrix(ctx, frame_spec)
        vals = [float(v) for v in spec]
        return m @ Vector((vals[0], vals[1], vals[2] if len(vals) > 2 else 0.0)), len(vals) > 2
    head = str(spec[0])
    if head in ("角色", "道具"):
        tr = ctx.tracks.get(str(spec[1]))
        if tr is None:
            die(f"{spec}：「{spec[1]}」的轨迹还没算（跟随对象要先声明）")
        fwd, left, up = (float(v) for v in (list(spec[2:5]) + [0.0, 0.0, 0.0])[:3])
        a = math.radians(tr.yaw[f])
        return tr.pos[f] + Vector((math.cos(a) * fwd - math.sin(a) * left, math.sin(a) * fwd + math.cos(a) * left, up)), True
    m, vals = split_frame(ctx, spec)
    return m @ Vector((vals[0], vals[1], vals[2] if len(vals) > 2 else 0.0)), len(vals) > 2


def ground_hint(ctx: Ctx, frame_spec: list) -> float:
    m = frame_matrix(ctx, frame_spec)
    return m.translation.z + (bj.Z_STREET if str(frame_spec[0]) in ("Place", "世界") else 0.0)


def positions(ctx: Ctx, item: dict, ground: Ground, n: int) -> list[Vector]:
    kfs = [k for k in item.get("关键帧", []) if "位置" in k]
    if not kfs:
        die(f"「{item['名']}」没有任何带 位置 的关键帧")
    fs = entity_frame(ctx, item)
    ts = [float(k["t"]) for k in kfs]
    floor = ground_hint(ctx, fs)
    hint = floor
    out: list[Vector] = []
    for f in range(n):
        t = f / ctx.fps
        pts = [key_point(ctx, list(k["位置"]), list(k.get("系", fs)), f) for k in kfs]
        x = hold_or_hermite(ts, [p[0].x for p in pts], t)
        y = hold_or_hermite(ts, [p[0].y for p in pts], t)
        i = max([j for j, tj in enumerate(ts) if tj <= t + 1e-9], default=0)
        j = min(i + 1, len(ts) - 1)
        if pts[i][1] and pts[j][1]:
            z = hold_or_hermite(ts, [p[0].z for p in pts], t)
        else:
            z = ground.z_at(x, y, hint, floor)
        hint = z
        out.append(Vector((x, y, z)))
    return out


def smooth_angles(targets: list[float], fps: int, rate: float) -> list[float]:
    out = [targets[0]]
    step = rate / fps
    for a in targets[1:]:
        d = (a - out[-1] + 180.0) % 360.0 - 180.0
        out.append(out[-1] + max(-step, min(step, d)))
    return out


def smooth_values(targets: list[float], fps: int, tau: float = 0.12) -> list[float]:
    k = 1.0 - math.exp(-1.0 / (fps * tau))
    out = [targets[0]]
    for v in targets[1:]:
        out.append(out[-1] + (v - out[-1]) * k)
    return out


PRE_ROLL = 0.25


def active_value(kfs: list[dict], key: str, t: float, default=None):
    val = default
    for k in kfs:
        if key in k and float(k["t"]) - PRE_ROLL <= t + 1e-9:
            val = k[key]
    return val


def yaw_targets(ctx: Ctx, item: dict, pos: list[Vector], cam: list[Vector] | None) -> list[float]:
    kfs = item.get("关键帧", [])
    fs = entity_frame(ctx, item)
    base = yaw_of(frame_matrix(ctx, fs))
    out: list[float] = []
    last = 0.0
    for f, p in enumerate(pos):
        t = f / ctx.fps
        spec = active_value(kfs, "朝向", t, "行进")
        if spec == "行进":
            a, b = pos[max(0, f - 3)], pos[min(len(pos) - 1, f + 3)]
            d = b - a
            if d.xy.length > 0.08:
                last = math.degrees(math.atan2(d.y, d.x))
            out.append(last)
            continue
        if spec == "镜头":
            target = cam[f] if cam else p + Vector((1.0, 0.0, 0.0))
            last = math.degrees(math.atan2(target.y - p.y, target.x - p.x))
        elif isinstance(spec, list) and str(spec[0]) in ("看", "看角色", "看道具"):
            if str(spec[0]) == "看":
                target = frame_matrix(ctx, fs) @ Vector((float(spec[1]), float(spec[2]), 0.0))
            else:
                target = ctx.tracks[str(spec[1])].pos[f]
            last = math.degrees(math.atan2(target.y - p.y, target.x - p.x))
        else:
            last = float(spec) + base
        out.append(last)
    return out


# ── 关节人姿态 ─────────────────────────────────────────────────────────────────
ARM: dict[str, tuple[float, float, float, float]] = {
    "垂": (0, 0, 0, 0), "胸前": (-25, -12, 0, -110), "持话筒": (-18, -8, 0, -100), "前伸": (-80, -5, 0, -5),
    "前伸低": (-42, -5, 0, -28), "指前": (-85, 5, 0, 0), "指后": (30, 28, 0, -10), "扶栏": (-12, 28, 0, -25),
    "捂耳": (-38, 55, 0, -150), "捂嘴": (-55, -20, 0, -140), "挥": (-165, 15, 0, -20), "摆手": (-45, -5, 0, -105),
    "抓鞍": (-18, -10, 0, -48), "端碗": (-30, -15, 0, -88), "揉头": (-150, 35, 0, -140), "按墙": (-85, -10, 0, -8),
    "扛袋": (-160, 25, 0, -150), "揉腿": (-75, -5, 0, 0), "比一": (-38, -10, 0, -100), "掀帘": (-115, -5, 0, -20),
    "折枝": (-140, 10, 0, -20), "插髻": (-150, 20, 0, -140), "敲": (-55, -10, 0, -50), "放": (-45, -5, 0, -40),
    "抱文书": (-20, -15, 0, -100), "拍": (-35, 5, 0, -30), "撑膝": (-40, 5, 0, -10), "举钱": (-70, -8, 0, -45),
    "写": (-35, -18, 0, -100), "拿本": (-30, -10, 0, -95), "按胸": (-20, -18, 0, -125), "叉腰": (0, 35, 0, -80),
    "抹汗": (-120, -20, 0, -140), "扶桌": (-30, 8, 0, -15), "拉纤": (40, 10, 0, -10), "撑篙": (-60, -10, 0, -60),
    "抱桅": (-70, -20, 0, -60), "递": (-60, -5, 0, -30), "端杯": (-45, -15, 0, -115), "摇扇": (-50, -10, 0, -120),
}
BASE: dict[str, dict[str, float]] = {
    "站": {}, "走": {},
    "坐": {"hipLx": -90, "hipRx": -90, "kneeLx": 90, "kneeRx": 90, "seat": 0.45},
    "蹲": {"hipLx": -100, "hipRx": -100, "kneeLx": 125, "kneeRx": 125, "ankleLx": -25, "ankleRx": -25, "pelvisx": 20, "drop": 0.58},
    "跪": {"kneeLx": 90, "kneeRx": 90, "drop": 0.40},
    "单跪": {"hipLx": -90, "kneeLx": 90, "kneeRx": 90, "drop": 0.40},
    "躺": {"pitch": -90.0, "seat": 0.0, "lay": 1.0},
    "骑": {"hipLx": -60, "hipRx": -60, "hipLy": -28, "hipRy": 28, "kneeLx": 75, "kneeRx": 75, "seat": 0.0},
}
MODS: dict[str, dict[str, float]] = {
    "俯身": {"pelvisx": 40}, "半躬": {"pelvisx": 20}, "弯腰": {"pelvisx": 70}, "后仰": {"pelvisx": -12},
    "抬头": {"headx": -25}, "仰头": {"headx": -40, "neckx": -15}, "低头": {"headx": 35}, "缩脖": {"neckx": 12, "headx": 10},
    "回头左": {"neckz": 45, "headz": 65, "pelvisz": 20}, "回头右": {"neckz": -45, "headz": -65, "pelvisz": -20},
    "侧头左": {"heady": -15}, "侧头右": {"heady": 15}, "踮脚": {"rise": 0.06}, "探身": {"pelvisx": 25},
}
CHANNELS = ("pelvisx", "pelvisz", "neckx", "neckz", "headx", "heady", "headz",
            "shLx", "shLy", "shLz", "elLx", "shRx", "shRy", "shRz", "elRx",
            "hipLx", "hipLy", "hipRx", "hipRy", "kneeLx", "kneeRx", "ankleLx", "ankleRx",
            "seat", "drop", "rise", "pitch", "lay")


def parse_pose(text: str) -> dict[str, float]:
    vals: dict[str, float] = {c: 0.0 for c in CHANNELS}
    use_seat = False
    for tok in (s.strip() for s in str(text).split("+") if s.strip()):
        m = re.fullmatch(r"(坐|躺|骑)@([-\d.]+)", tok)
        if m:
            vals.update(BASE[m.group(1)])
            vals["seat"] = float(m.group(2))
            use_seat = True
            continue
        if tok in BASE:
            vals.update(BASE[tok])
            use_seat = use_seat or "seat" in BASE[tok]
            continue
        if tok in MODS:
            for k, v in MODS[tok].items():
                vals[k] += v
            continue
        m = re.fullmatch(r"(L|R|双):(.+)", tok)
        if m and m.group(2) in ARM:
            x, y, z, e = ARM[m.group(2)]
            for side in (("L", "R") if m.group(1) == "双" else (m.group(1),)):
                sx = 1.0 if side == "L" else -1.0
                vals[f"sh{side}x"], vals[f"sh{side}y"], vals[f"sh{side}z"], vals[f"el{side}x"] = x, -sx * y, z, e
            continue
        die(f"姿态「{text}」里的「{tok}」不认识；基础 {sorted(BASE)}，修饰 {sorted(MODS)}，手臂 L:/R:/双: + {sorted(ARM)}")
    vals["useseat"] = 1.0 if use_seat else 0.0
    return vals


@dataclass
class Figure:
    name: str
    height: float
    root: bpy.types.Object
    joints: dict
    objects: list[bpy.types.Object]


def material(name: str, rgb: tuple[float, float, float]) -> bpy.types.Material:
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (*rgb, 1.0)
    return m


def _bind_without_update(child: bpy.types.Object, parent: bpy.types.Object) -> None:
    # 建骨架时整条链都是静默姿态：父件的 matrix_world ＝ 它自己的 matrix_basis。previz_rig 原版每挂一件就 view_layer.update()，
    # 场景里有整座城（6.7k 物件）时一具人要刷七十次深度图、九具人十几分钟——这里直接用 basis 求逆，结果相同。
    child.parent = parent
    child.matrix_parent_inverse = parent.matrix_basis.inverted()


def _smooth_data(ob: bpy.types.Object) -> None:
    # 5.x 的 shade_auto_smooth 给每件加一个几何节点修改器，几百件一起逐帧重算；面平滑标记在数据上，效果够用
    if ob.type == "MESH":
        ob.data.polygons.foreach_set("use_smooth", [True] * len(ob.data.polygons))


def _data_empty(self, name: str, loc: Vector, parent=None):
    e = bpy.data.objects.new(name, None)
    e.empty_display_size = 0.08
    e.location = loc
    self._link(e)
    if parent is not None:
        self._setpar(e, parent)
    return e


def _data_mesh(name: str, bm, loc: Vector) -> bpy.types.Object:
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.location = loc
    return ob


def _data_sphere(self, name, r, loc, material, parent=None, segs=24, rings=14):
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=max(8, segs // 2), v_segments=max(6, rings // 2), radius=r)
    return self._finish(_data_mesh(name, bm, loc), material, parent)


def _data_frustum(self, name, r_bottom, r_top, h, loc, material, parent=None, flatten_y=1.0):
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=12, radius1=r_bottom, radius2=r_top, depth=h)
    for v in bm.verts:
        v.co.y *= flatten_y
    return self._finish(_data_mesh(name, bm, loc), material, parent)


def _data_box(self, name, size, loc, material, parent=None):
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
    return self._finish(_data_mesh(name, bm, loc), material, parent, do_smooth=False)


def build_figure(name: str, color: str, height: float, col: bpy.types.Collection) -> Figure:
    import previz_rig
    # previz_rig 的原语走 bpy.ops：场景里有整座城时每个 ops 都重建一次依赖关系（一具人上百次），九具人要二十分钟；
    # 换成 bpy.data + bmesh 造同形网格（段数减半，1280/1920 画幅下看不出），关节枢纽位置与原版一致
    previz_rig.PrevizRig._setpar = staticmethod(_bind_without_update)
    previz_rig.PrevizRig._smooth = staticmethod(_smooth_data)
    previz_rig.PrevizRig.empty = _data_empty
    previz_rig.PrevizRig.sphere = _data_sphere
    previz_rig.PrevizRig.frustum = _data_frustum
    previz_rig.PrevizRig.box = _data_box
    rgb = COLORS[color]
    made: list[bpy.types.Object] = []

    def link(ob: bpy.types.Object) -> None:
        for c in list(ob.users_collection):
            c.objects.unlink(ob)
        col.objects.link(ob)
        made.append(ob)

    body = material(f"PVZ_{color}_body", rgb)
    skin = material("PVZ_skin", (0.93, 0.80, 0.70))
    limb = material(f"PVZ_{color}_limb", tuple(0.55 * c + 0.45 for c in rgb))
    rig = previz_rig.PrevizRig(link=link, body=body, skin=skin, limb_end=limb)
    root, _pelvis, joints = rig.build(Vector((0.0, 0.0, 0.0)))
    root.name = f"PVZ_{name}"
    # 头是一颗光球：转脸看镜头与后脑对镜头渲出来一模一样，走位表里「看谁」在参考视频里读不出。补一个朝脸前（−Y）的鼻锥
    nose = rig.frustum("PVZ_nose", 0.03, 0.008, 0.07, Vector((0.0, -0.14, previz_rig.HIP_Z + 0.72)), limb, joints["head"])
    nose.rotation_euler = (math.radians(90.0), 0.0, 0.0)
    for ob in made:
        if ob.type == "MESH" and ob.data.materials:
            ob.color = ob.data.materials[0].diffuse_color
    rig.both_hands(joints, 1, previz_rig.HAND_RELAX)
    s = height / previz_rig.BODY_H
    root.scale = (s, s, s)
    return Figure(name, height, root, joints, made)


def key_channel(ob: bpy.types.Object, path: str, index: int, values: list[float], deg: bool) -> None:
    if max(values) - min(values) < 1e-4:
        cur = list(getattr(ob, path))
        cur[index] = math.radians(values[0]) if deg else values[0]
        setattr(ob, path, cur)
        return
    for f, v in enumerate(values):
        cur = list(getattr(ob, path))
        cur[index] = math.radians(v) if deg else v
        setattr(ob, path, cur)
        ob.keyframe_insert(path, index=index, frame=f + 1)


def visibility(obs: list[bpy.types.Object], kfs: list[dict], n: int, fps: int, start: float = 0.0, stop: float = 1e9) -> None:
    states: list[bool] = []
    for f in range(n):
        t = f / fps
        v = bool(active_value([{**k, "t": float(k["t"]) + PRE_ROLL} for k in kfs], "显", t, True)) and start - 1e-9 <= t < stop
        states.append(v)
    if all(states):
        return
    for ob in obs:
        prev = None
        for f, v in enumerate(states):
            if v != prev:
                if prev is not None:
                    # 布尔通道的关键帧也按贝塞尔插值、取整在两键正中翻转：只在切换帧打键，隐藏会提前好几秒——前一帧补一个旧状态键
                    ob.hide_render = not prev
                    ob.hide_viewport = not prev
                    ob.keyframe_insert("hide_render", frame=f)
                    ob.keyframe_insert("hide_viewport", frame=f)
                ob.hide_render = not v
                ob.hide_viewport = not v
                ob.keyframe_insert("hide_render", frame=f + 1)
                ob.keyframe_insert("hide_viewport", frame=f + 1)
                prev = v


def animate_figure(ctx: Ctx, fig: Figure, item: dict, pos: list[Vector], yaw: list[float], cam: list[Vector], n: int) -> None:
    import previz_rig
    kfs = item.get("关键帧", [])
    s = fig.height / previz_rig.BODY_H
    poses = [parse_pose(active_value(kfs, "姿态", f / ctx.fps, "站")) for f in range(n)]
    ch = {c: smooth_values([p[c] for p in poses], ctx.fps) for c in CHANNELS}
    useseat = smooth_values([p["useseat"] for p in poses], ctx.fps)
    moving_phase, phase = [], 0.0
    amps: list[float] = []
    for f in range(n):
        d = (pos[min(n - 1, f + 1)] - pos[max(0, f - 1)]).xy.length / (2.0 / ctx.fps)
        base_walk = active_value(kfs, "姿态", f / ctx.fps, "站")
        seated = poses[f]["useseat"] > 0.5 or poses[f]["drop"] > 0.0
        amp = 0.0 if seated else min(1.0, d / 1.1) if d > 0.15 else 0.0
        if f > 0:
            phase += (pos[f] - pos[f - 1]).xy.length / (1.35 * s) * 2.0 * math.pi
        amps.append(amp)
        moving_phase.append(phase)
        del base_walk
    amps = smooth_values(amps, ctx.fps, 0.2)
    head_z = previz_rig.HIP_Z + 0.73
    look_yaw: list[float] = []
    look_pitch: list[float] = []
    for f in range(n):
        spec = active_value(kfs, "看", f / ctx.fps, None)
        if spec is None or spec == "前":
            look_yaw.append(0.0)
            look_pitch.append(0.0)
            continue
        eye = pos[f] + Vector((0.0, 0.0, head_z * s))
        if spec == "镜头":
            tgt = cam[f]
        elif isinstance(spec, list) and str(spec[0]) in ("角色", "道具"):
            tr = ctx.tracks[str(spec[1])]
            tgt = tr.pos[f] + Vector((0.0, 0.0, float(spec[2]) if len(spec) > 2 else tr.height * 0.85))
        else:
            tgt, _given = key_point(ctx, list(spec), entity_frame(ctx, item), f)
        d = tgt - eye
        rel = (math.degrees(math.atan2(d.y, d.x)) - yaw[f] + 180.0) % 360.0 - 180.0
        look_yaw.append(max(-95.0, min(95.0, rel)))
        look_pitch.append(max(-45.0, min(50.0, -math.degrees(math.atan2(d.z, d.xy.length)))))
    look_yaw = smooth_values(look_yaw, ctx.fps, 0.1)
    look_pitch = smooth_values(look_pitch, ctx.fps, 0.1)

    root = fig.root
    J = fig.joints
    locs, rots = [], []
    for f in range(n):
        a = math.radians(yaw[f])
        lay = ch["lay"][f]
        seat_z = ch["seat"][f] + 0.03 - previz_rig.HIP_Z * s
        z = pos[f].z + useseat[f] * seat_z - ch["drop"][f] * s + ch["rise"][f] + lay * 0.12
        shift = Vector((math.cos(a), math.sin(a), 0.0)) * (lay * previz_rig.HIP_Z * s)
        locs.append(pos[f] + shift + Vector((0.0, 0.0, z - pos[f].z)))
        rots.append((ch["pitch"][f], 0.0, yaw[f] + 90.0))
    for i in range(3):
        key_channel(root, "location", i, [v[i] for v in locs], False)
        key_channel(root, "rotation_euler", i, [r[i] for r in rots], True)
    gait = [(amps[f], moving_phase[f]) for f in range(n)]
    sw = [a * math.sin(p) for a, p in gait]
    key_channel(J["pelvis"], "rotation_euler", 0, ch["pelvisx"], True)
    key_channel(J["pelvis"], "rotation_euler", 2, [ch["pelvisz"][f] + 4.0 * sw[f] for f in range(n)], True)
    key_channel(J["neck"], "rotation_euler", 0, [ch["neckx"][f] + 0.35 * look_pitch[f] for f in range(n)], True)
    key_channel(J["neck"], "rotation_euler", 2, [ch["neckz"][f] + 0.4 * look_yaw[f] for f in range(n)], True)
    key_channel(J["head"], "rotation_euler", 0, [ch["headx"][f] + 0.65 * look_pitch[f] for f in range(n)], True)
    key_channel(J["head"], "rotation_euler", 1, ch["heady"], True)
    key_channel(J["head"], "rotation_euler", 2, [ch["headz"][f] + 0.6 * look_yaw[f] for f in range(n)], True)
    for side, sgn in (("L", 1.0), ("R", -1.0)):
        free = [abs(ch[f"sh{side}x"][f]) + abs(ch[f"el{side}x"][f]) < 5.0 for f in range(n)]
        key_channel(J[f"shoulder{side}"], "rotation_euler", 0,
                    [ch[f"sh{side}x"][f] + (sgn * 16.0 * sw[f] if free[f] else 0.0) for f in range(n)], True)
        key_channel(J[f"shoulder{side}"], "rotation_euler", 1, ch[f"sh{side}y"], True)
        key_channel(J[f"shoulder{side}"], "rotation_euler", 2, ch[f"sh{side}z"], True)
        key_channel(J[f"elbow{side}"], "rotation_euler", 0,
                    [ch[f"el{side}x"][f] - (8.0 * amps[f] if free[f] else 0.0) for f in range(n)], True)
        key_channel(J[f"hip{side}"], "rotation_euler", 0, [ch[f"hip{side}x"][f] - sgn * 26.0 * sw[f] for f in range(n)], True)
        key_channel(J[f"hip{side}"], "rotation_euler", 1, ch[f"hip{side}y"], True)
        knee = [ch[f"knee{side}x"][f] + amps[f] * (6.0 + 38.0 * max(0.0, sgn * math.cos(gait[f][1]))) for f in range(n)]
        key_channel(J[f"knee{side}"], "rotation_euler", 0, knee, True)
        key_channel(J[f"ankle{side}"], "rotation_euler", 0, ch[f"ankle{side}x"], True)
    visibility([o for o in fig.objects] + [fig.root], kfs, n, ctx.fps)


# ── 道具 / 人群 ───────────────────────────────────────────────────────────────
def build_prop(ctx: Ctx, item: dict, col: bpy.types.Collection, figures: dict[str, Figure],
               props: dict[str, tuple[bpy.types.Object, dict[str, bpy.types.Object]]], n: int) -> None:
    import previz_rig
    kind = str(item["型"])
    size = [float(v) for v in item.get("尺寸", [])]
    b, pts = prop_geometry(kind, size)
    name = str(item["名"])
    ob = b.finish(f"PVZ_P_{name}", col)
    ob.color = (*COLORS[str(item.get("色", "灰"))], 1.0)
    kfs = item.get("关键帧", [])
    subs: dict[str, bpy.types.Object] = {}
    if "mast_pivot" in pts:
        pivot = bpy.data.objects.new(f"PVZ_P_{name}_mast_pivot", None)
        col.objects.link(pivot)
        pivot.parent = ob
        pivot.location = pts["mast_pivot"]
        mb = Batch()
        mb.cyl(0.0, 0.0, 0.0, size[3] if len(size) > 3 else 9.0, 0.14, 8)
        mast = mb.finish(f"PVZ_P_{name}_mast", col)
        mast.color = ob.color
        mast.parent = pivot
        subs["mast_pivot"] = pivot
        subs["mast"] = mast
        vals = [hold_or_hermite([float(k["t"]) for k in kfs if "桅角" in k] or [0.0],
                                [float(k["桅角"]) for k in kfs if "桅角" in k] or [0.0], f / ctx.fps) for f in range(n)]
        key_channel(pivot, "rotation_euler", 1, vals, True)
    for key, p in pts.items():
        if key != "mast_pivot":
            e = bpy.data.objects.new(f"PVZ_P_{name}_{key}", None)
            col.objects.link(e)
            e.parent = ob
            e.location = p
            subs[key] = e
    if "开" in {k2 for k in kfs for k2 in k}:
        ks = [k for k in kfs if "开" in k]
        key_channel(ob, "rotation_euler", 2, [hold_or_hermite([float(k["t"]) for k in ks], [float(k["开"]) for k in ks], f / ctx.fps)
                                               for f in range(n)], True)
    if "挂" in item:
        att = list(item["挂"])
        off = Vector([float(v) for v in item.get("偏移", [0.0, 0.0, 0.0])])
        if str(att[0]) == "角色":
            fig = figures[str(att[1])]
            jname = {"R": "handR", "L": "handL", "头": "head", "背": "neck", "腰": "pelvis"}[str(att[2])]
            ob.parent = fig.joints[jname]
            ob.matrix_parent_inverse = Matrix.Identity(4)
            ob.location = off
            if len(att) > 3:
                ob.rotation_euler = Euler([math.radians(float(v)) for v in att[3:6]])
        else:
            host = props[str(att[1])][1].get(str(att[2]), props[str(att[1])][0]) if len(att) > 2 else props[str(att[1])][0]
            ob.parent = host
            ob.matrix_parent_inverse = Matrix.Identity(4)
            ob.location = off
        if kfs:
            visibility([ob] + list(subs.values()), kfs, n, ctx.fps)
        props[name] = (ob, subs)
        return
    tr = ctx.tracks[name]
    for i in range(3):
        key_channel(ob, "location", i, [p[i] for p in tr.pos], False)
    key_channel(ob, "rotation_euler", 2, tr.yaw, True)
    visibility([ob] + list(subs.values()), kfs, n, ctx.fps)
    props[name] = (ob, subs)
    del previz_rig


def build_crowd(ctx: Ctx, item: dict, col: bpy.types.Collection, ground: Ground, n: int) -> int:
    rng = random.Random(int(item.get("种子", 1)))
    fs = list(item.get("系", ctx.default_frame))
    m = frame_matrix(ctx, fs)
    x0, x1, y0, y1 = (float(v) for v in item["区域"])
    heading = math.radians(float(item.get("方向", 0.0)))
    speed = float(item.get("速度", 1.2))
    count = int(item.get("数", 10))
    h = float(item.get("身高", 1.68))
    start, stop = float(item.get("起", 0.0)), float(item.get("止", 1e9))
    rgb = COLORS[str(item.get("色", "剪影"))]
    hint = ground_hint(ctx, fs)
    u = Vector((math.cos(heading), math.sin(heading)))
    for i in range(count):
        b = Batch()
        k = h / 1.7
        b.cyl(0.0, 0.0, 0.0, 0.85 * k, 0.13 * k, 6)
        b.cyl(0.0, 0.0, 0.85 * k, 1.45 * k, 0.19 * k, 8)
        b.ball((0.0, 0.0, 1.57 * k), 0.11 * k)
        ob = b.finish(f"PVZ_C_{item['名']}_{i:02d}", col)
        tint = rng.uniform(0.85, 1.1)
        ob.color = (*(min(1.0, c * tint) for c in rgb), 1.0)
        px, py = rng.uniform(x0, x1), rng.uniform(y0, y1)
        sp = speed * rng.uniform(0.75, 1.25) * (1.0 if rng.random() < 0.7 or speed == 0 else -1.0)
        xs, ys, zs = [], [], []
        z = hint
        for f in range(n):
            t = f / ctx.fps
            lx = px + u.x * sp * t
            ly = py + u.y * sp * t
            if x1 > x0:
                lx = x0 + (lx - x0) % (x1 - x0)
            if y1 > y0:
                ly = y0 + (ly - y0) % (y1 - y0)
            w = m @ Vector((lx, ly, 0.0))
            z = ground.z_at(w.x, w.y, z, hint)
            xs.append(w.x)
            ys.append(w.y)
            zs.append(z)
        key_channel(ob, "location", 0, xs, False)
        key_channel(ob, "location", 1, ys, False)
        key_channel(ob, "location", 2, zs, False)
        ob.rotation_euler = (0.0, 0.0, heading + yaw_of(m) / 57.29578)
        visibility([ob], [], n, ctx.fps, start, stop)
    return count


# ── 机位 ──────────────────────────────────────────────────────────────────────
def camera_frames(ctx: Ctx, keys: list[dict], n: int) -> tuple[list[Vector], list[Vector], list[float], list[float]]:
    segs: list[list[dict]] = []
    for k in keys:
        if not segs or k.get("切"):
            segs.append([k])
        else:
            segs[-1].append(k)
    pos, look, lens, starts = [], [], [], [float(sg[0]["t"]) for sg in segs]
    for f in range(n):
        t = f / ctx.fps
        seg = [sg for sg in segs if float(sg[0]["t"]) <= t + 1e-9][-1]
        ts = [float(k["t"]) for k in seg]
        ps = [resolve_point(ctx, list(k["位置"]), f) for k in seg]
        ls = [resolve_point(ctx, list(k["看向"]), f) for k in seg]
        pos.append(Vector([hold_or_hermite(ts, [p[i] for p in ps], t) for i in range(3)]))
        look.append(Vector([hold_or_hermite(ts, [p[i] for p in ls], t) for i in range(3)]))
        lens.append(hold_or_hermite(ts, [float(k["焦距"]) for k in seg], t))
    return pos, look, lens, starts


# ── 建场 ──────────────────────────────────────────────────────────────────────
def region_boxes(ctx: Ctx, cfg: dict) -> list[tuple[float, float, float, float]]:
    boxes: list[tuple[float, float, float, float]] = []
    for item in cfg.get("角色", []) + cfg.get("道具", []):
        fs = entity_frame(ctx, item)
        for k in item.get("关键帧", []):
            spec = k.get("位置")
            if spec is None or (not isinstance(spec[0], (int, float)) and str(spec[0]) in ("角色", "道具")):
                continue
            p, _ = key_point(ctx, list(spec), list(k.get("系", fs)), 0)
            boxes.append((p.x - 8.0, p.x + 8.0, p.y - 8.0, p.y + 8.0))
    for item in cfg.get("人群", []):
        m = frame_matrix(ctx, list(item.get("系", ctx.default_frame)))
        x0, x1, y0, y1 = (float(v) for v in item["区域"])
        cs = [m @ Vector((x, y, 0.0)) for x in (x0, x1) for y in (y0, y1)]
        boxes.append((min(c.x for c in cs) - 3, max(c.x for c in cs) + 3, min(c.y for c in cs) - 3, max(c.y for c in cs) + 3))
    return boxes


T0: list[float] = []


def stage(msg: str) -> None:
    import time
    if not T0:
        T0.append(time.time())
    print(f"STAGE {time.time() - T0[0]:7.1f}s {msg}")
    sys.stdout.flush()


def build(cfg_path: Path) -> dict:
    from bpy_extras.object_utils import world_to_camera_view
    stage("load config")
    cfg = load(cfg_path)
    g = cfg["全局"]
    fps, total = int(g.get("fps", 25)), float(g["total_sec"])
    n = int(round(total * fps))
    bj.aerial_world()
    ctx = Ctx(cfg_path, fps, total, list(g.get("坐标系", ["世界"])))
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end, sc.render.fps = 1, n, fps
    set_objs = link_sets(ctx, cfg.get("布景", []))
    if not g.get("城景", True):
        for lc in bpy.context.view_layer.layer_collection.children:
            if lc.name not in ("SETS", "PREVIZ"):
                lc.exclude = True
    col = bj.collection("PREVIZ")
    stage(f"sets linked ({len(set_objs)} objects); building ground probe")
    ground = Ground(region_boxes(ctx, cfg))
    stage(f"ground probe {ground.tris} tris; computing tracks")

    root_props = [p for p in cfg.get("道具", []) if "挂" not in p]
    chars = cfg.get("角色", [])
    pending = root_props + chars
    done: set[str] = set()
    for _ in range(len(pending) + 1):
        progressed = False
        for item in pending:
            name = str(item["名"])
            if name in done:
                continue
            deps = {str(k["位置"][1]) for k in item.get("关键帧", []) if "位置" in k and not isinstance(k["位置"][0], (int, float))
                    and str(k["位置"][0]) in ("角色", "道具")}
            if not deps <= done:
                continue
            pos = positions(ctx, item, ground, n)
            is_char = item in chars
            height = float(item.get("身高", 1.65)) if is_char else 1.0
            ctx.tracks[name] = Track(pos, smooth_angles(yaw_targets(ctx, item, pos, None), fps, 240.0), height)
            done.add(name)
            progressed = True
        if not progressed:
            break
    missing = {str(i["名"]) for i in pending} - done
    if missing:
        die(f"跟随关系成环或引用了不存在的对象：{sorted(missing)}")

    cam_pos, cam_look, cam_lens, cuts = camera_frames(ctx, cfg["机位"], n)
    for item in pending:
        if any(k.get("朝向") == "镜头" for k in item.get("关键帧", [])):
            tr = ctx.tracks[str(item["名"])]
            tr.yaw = smooth_angles(yaw_targets(ctx, item, tr.pos, cam_pos), fps, 240.0)
    cam_pos, cam_look, cam_lens, cuts = camera_frames(ctx, cfg["机位"], n)

    stage("tracks + camera path done; building figures")
    figures: dict[str, Figure] = {}
    for item in chars:
        shape = str(item.get("形", "人"))
        name = str(item["名"])
        tr = ctx.tracks[name]
        stage(f"figure {name}")
        if shape == "剪影":
            b = Batch()
            k = tr.height / 1.7
            b.cyl(0.0, 0.0, 0.0, 0.85 * k, 0.13 * k, 6)
            b.cyl(0.0, 0.0, 0.85 * k, 1.45 * k, 0.19 * k, 8)
            b.ball((0.0, 0.0, 1.57 * k), 0.11 * k)
            ob = b.finish(f"PVZ_S_{name}", col)
            ob.color = (*COLORS[str(item.get("色", "剪影"))], 1.0)
            for i in range(3):
                key_channel(ob, "location", i, [p[i] for p in tr.pos], False)
            visibility([ob], item.get("关键帧", []), n, fps)
            continue
        fig = build_figure(name, str(item.get("色", "米")), tr.height, col)
        animate_figure(ctx, fig, item, tr.pos, tr.yaw, cam_pos, n)
        figures[name] = fig
    stage("props")
    props: dict[str, tuple[bpy.types.Object, dict[str, bpy.types.Object]]] = {}
    for item in root_props + [p for p in cfg.get("道具", []) if "挂" in p]:
        build_prop(ctx, item, col, figures, props, n)
    stage("crowds")
    crowd = sum(build_crowd(ctx, item, col, ground, n) for item in cfg.get("人群", []))
    stage("camera + render settings")

    cam_data = bpy.data.cameras.new("PREVIZ_CAM")
    cam_data.sensor_width = 36.0
    cam_data.clip_end = float(g.get("远裁剪", 4000.0))
    cam = bpy.data.objects.new("PREVIZ_CAM", cam_data)
    tgt = bpy.data.objects.new("PREVIZ_CAM_TARGET", None)
    col.objects.link(cam)
    col.objects.link(tgt)
    con = cam.constraints.new("TRACK_TO")
    con.target, con.track_axis, con.up_axis = tgt, "TRACK_NEGATIVE_Z", "UP_Y"
    for f in range(n):
        cam.location, tgt.location, cam_data.lens = cam_pos[f], cam_look[f], cam_lens[f]
        cam.keyframe_insert("location", frame=f + 1)
        tgt.keyframe_insert("location", frame=f + 1)
        cam_data.keyframe_insert("lens", frame=f + 1)
        near = max(0.01, min(2.0, (cam_look[f] - cam_pos[f]).length / 300.0), (cam_pos[f].z - ground_hint(ctx, ctx.default_frame)) / 60.0)
        cam_data.clip_start = min(near, 2.0)
        cam_data.keyframe_insert("clip_start", frame=f + 1)
    sc.camera = cam

    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light, sh.color_type = "STUDIO", "OBJECT"
    sh.show_shadows, sh.show_cavity = False, False
    sh.show_object_outline = True
    if sc.world is None:
        sc.world = bpy.data.worlds.new("PREVIZ_WORLD")
    sc.world.color = (0.58, 0.62, 0.68)
    ours = {o.name for o in col.all_objects}
    for ob in bpy.data.objects:
        if ob.type != "MESH" or ob.name in ours or ob.library is not None:
            continue
        nm = ob.name.lower()
        ob.color = WATER if "water" in nm else CITY_GREY
    people = bpy.data.objects.get("LOOK_people")     # 全城静态行人只进写实渲染（follow-up 007）
    if people is not None:
        people.hide_render = True
    sc.render.resolution_x, sc.render.resolution_y = (int(v) for v in g.get("分辨率", [1280, 720]))
    sc.render.resolution_percentage = 100
    im = sc.render.image_settings
    if hasattr(im, "media_type"):
        im.media_type = "VIDEO"
    im.file_format = "FFMPEG"
    sc.render.ffmpeg.format, sc.render.ffmpeg.codec = "MPEG4", "H264"
    sc.render.ffmpeg.constant_rate_factor = "MEDIUM"
    sc.render.filepath = f"//{g['shot']}_previz.mp4"

    report: list[str] = []
    marks = sorted({0} | {max(0, int(round(c * fps)) - 1) for c in cuts[1:]} | {int(round(c * fps)) for c in cuts[1:]} | {n - 1})
    for f in marks:
        sc.frame_set(f + 1)
        bpy.context.view_layer.update()
        line = f"CAMKEY f={f + 1} t={f / fps:.2f} pos=({cam_pos[f].x:.2f},{cam_pos[f].y:.2f},{cam_pos[f].z:.2f}) lens={cam_lens[f]:.1f}"
        if "林问" in ctx.tracks:
            tr = ctx.tracks["林问"]
            lo = world_to_camera_view(sc, cam, tr.pos[f])
            hi = world_to_camera_view(sc, cam, tr.pos[f] + Vector((0.0, 0.0, tr.height)))
            line += f" 林问 frac={abs(hi.y - lo.y):.2f} x={lo.x:.2f} y={lo.y:.2f}..{hi.y:.2f} front={int(lo.z > 0)}"
        report.append(line)
        for nm, fig in figures.items():
            tr = ctx.tracks[nm]
            lo = world_to_camera_view(sc, cam, tr.pos[f])
            hi = world_to_camera_view(sc, cam, tr.pos[f] + Vector((0.0, 0.0, tr.height)))
            inside = lo.z > 0 and -0.05 <= lo.x <= 1.05 and max(lo.y, hi.y) >= 0.0 and min(lo.y, hi.y) <= 1.0
            report.append(f"CAMFIG f={f + 1} {nm} ground_z={tr.pos[f].z:.2f} frac={abs(hi.y - lo.y):.2f} x={lo.x:.2f} "
                          f"y={lo.y:.2f}..{hi.y:.2f} in_frame={int(inside)} visible={int(not fig.root.hide_render)}")
    sc.frame_set(1)
    return {"frames": n, "fps": fps, "cuts": cuts, "sets": len(set_objs), "figures": len(figures), "props": len(props),
            "crowd": crowd, "ground_tris": ground.tris, "report": report}


def run(script_file: str) -> None:
    cfg_path = Path(script_file).resolve().with_name("previz_config.toml")
    blend = Path(bpy.data.filepath).resolve() if bpy.data.filepath else None
    if blend is None or blend == bj.DEFAULT_OUT.resolve() or blend.parent != cfg_path.parent:
        die("只许改本镜目录里的场景副本：先把 bianjing.blend 复制到本镜目录再跑（rule 4h §A）")
    info = build(cfg_path)
    bpy.ops.wm.save_mainfile()
    # 机位与人占画高的量测报告落盘在本镜目录（`tools/previz_frame_fix.py` 读它反解机位；
    # 日志在 scratchpad 里会被清掉，报告必须跟产物同寿）。
    cfg_path.with_name(cfg_path.parent.name + "_previz_report.txt").write_text(
        "\n".join(info["report"]) + "\n", encoding="utf-8")
    for line in info["report"]:
        print(line)
    print(f"PREVIZ OK frames=1..{info['frames']} fps={info['fps']} cuts={info['cuts']} sets={info['sets']} "
          f"figures={info['figures']} props={info['props']} crowd={info['crowd']} ground_tris={info['ground_tris']}")
    sys.stdout.flush()
