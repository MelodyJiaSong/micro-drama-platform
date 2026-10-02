# -*- coding: utf-8 -*-
"""场景层通用建模引擎 —— 一个 scene 一份 `blocks.toml`，**不拷脚本**。

用法（仓库根目录）：
    blender -b --factory-startup --python tools/build_scene.py -- <scene 目录>
    blender -b --factory-startup --python tools/build_scene.py -- <scene 目录> --no-render
    blender -b --factory-startup --python tools/build_scene.py -- --all <scenes 根目录>

产物（落 `<scene>/_blender/`，rule 4h-K）：
    {bg}.blend           场景层几何（零材质、零灯光 —— rule 4h §D1）+ 汇总进来的图与 prompt（见下）
    check_plan.png       正射俯视校验图，与 planning/{bg}_floorplan.png 同构，用来对账
    check_{锚点}.png     每个 plate 锚点机位的灰模透视

**blend ＝ 图 + prompt + 单物体 GLB 的汇总**（2026-09-25 用户定调）：
    · 场景图 `{bg 目录}/{bg 目录}.png` 与各方位 plate 图——**没有场景图不建 blend**（图先行、3D 在后）；
      [[anchor]] 的 key ＝ plate 目录名（或写 `image = "{文件名}"`）时，该图挂成这台相机的背景图，对着几何对账。
    · 卡里的 prompt 进 Blender 文本块（Text Editor 里读）：场景卡、各 plate 卡、本场景用到的每件资产卡。
    · 每件物件 = 本剧 `props/p{N}_{名}/mesh/p{N}.glb` **一个物体**（场景只引用，不自带资产库）；一个块里有几样东西就写 `parts`，
      由本引擎按各自的 size_m 摆在一起——多物体的组合是 Blender 的活，**绝不导出场景级 GLB**。

纪律
----
· **几何唯一出处 ＝ `<scene>/planning/blocks.toml`**（rule 4i ①）。
  本引擎一个坐标字面量都不写；改布局 ＝ 改 toml 重跑。
· **`kind` 未登记直接 raise**，**布局违规直接 raise**——左移进生成器，
  不留给出片前的 reviewer（CLAUDE.md「能量化的反馈必须落成可机检闸门」）。
· **A/B 档一律走本引擎，禁止拷进 scene 目录改**（rule 4h ③）。
  某个 hero 场景真需要独有构件时，加一个 `kind` 到本文件，而不是复制一份脚本。
· **环境永不用 image-to-3D**（rule 4g §B）：墙 / 屋顶 / 街面 / 桥拱一律脚本建。
· **图先行、3D 在后**（rule 4e ①）：白模只服务 previz 与站位对账，
  **绝不拿它渲的图去当出图参考**。

模数（人类建筑，跨剧一致，与 sk2 暴风城同一套）
    开间 4.0 m · 层高 3.5 m · 门洞 2.4 m · 墙厚 0.8 m
"""
from __future__ import annotations

import math
import os
import re
import sys

import bpy
from mathutils import Matrix

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

BAY = 4.0
FLOOR = 3.5
DOOR_W = 2.4
DOOR_H = 3.0
WALL_T = 0.8

CELL_MAX_VERTS = 40000     # 地形网格上限，按场地自适应选格距
RIDGE_FALLOFF = 34.0
BANK = 5.0


class Scene:
    """一个场景的全部可读状态。引擎里所有几何函数都从它取数，不读全局字面量。"""

    def __init__(self, scene_dir: str) -> None:
        self.dir = os.path.abspath(scene_dir)
        self.toml = os.path.join(self.dir, "planning", "blocks.toml")
        if not os.path.isfile(self.toml):
            raise SystemExit("找不到 %s —— 每个 bg 的几何唯一出处就是这份 toml（rule 4h-K）"
                             % self.toml)
        with open(self.toml, "rb") as f:
            self.cfg = tomllib.load(f)

        # **「每个 bg 必备 floor plan」是靠这里咬人的**（rule 4k）：消费者跑不起来，
        # 而不是靠一次全仓盘点去点名。这样新活被挡住、没动过的旧剧一个都不扫。
        # schema 判据只有一份，住在 bpy-free 的 planschema 里——不在这里重写一遍。
        if REPO not in sys.path:
            sys.path.insert(0, REPO)
        from tools.previz import planschema
        errs = planschema.check(self.cfg, self.dir)
        if errs:
            raise SystemExit("[%s] 平面图 schema %d 条不合格，未建 blend：\n  - %s"
                             % (os.path.basename(self.dir), len(errs), "\n  - ".join(errs)))

        self.meta = self.cfg["meta"]
        self.bg = self.meta["bg"]
        self.name_zh = self.meta.get("name_zh", self.bg)
        self.W, self.H = self.meta["size_m"]
        self.interior = bool(self.meta.get("interior", False))
        self.slope_m = float(self.meta.get("slope_m", 6.0))
        self.out = os.path.join(self.dir, "_blender")
        base = os.path.basename(self.dir)
        self.image = os.path.join(self.dir, base + ".png")
        self.card = os.path.join(self.dir, base + ".md")
        self.plates = sorted(d for d in os.listdir(self.dir)
                             if d.startswith(self.bg + "-") and os.path.isfile(os.path.join(self.dir, d, d + ".md")))

        bad = [b["name"] for b in self.blocks if "kind" not in b or "h_m" not in b]
        if bad:
            raise SystemExit("[%s] 这些块缺 kind / h_m，说不清怎么建：%s" % (self.bg, "、".join(bad)))

        self.ridges = [(r["poly"], float(r["height_m"])) for r in self.cfg.get("ridge", [])]
        self.waters = [(w["path"], float(w.get("width_m", 6)), float(w.get("depth_m", 2.0)))
                       for w in self.cfg.get("water", [])]
        self.roads = [(r["path"], float(r.get("width_m", 4)), r.get("name", ""))
                      for r in self.cfg.get("road", [])]

    @property
    def blocks(self):
        return self.cfg.get("block", [])

    @property
    def anchors(self):
        return self.cfg.get("anchor", [])

    def P(self, x, y):
        """平面图坐标（x 东，y 南）→ Blender（+X 东，+Y 北），原点在场地中心。"""
        return (x - self.W / 2.0, self.H / 2.0 - y)

    def base_z(self, x, y):
        """底面：自北向南缓降。室内场景是平的。"""
        if self.interior:
            return 0.0
        return self.slope_m * (1.0 - y / self.H)

    def relief(self, x, y):
        """确定性微起伏。**不用 random**：同一份 toml 必须出同一个 blend。"""
        if self.interior:
            return 0.0
        return (0.55 * math.sin(x * 0.11) * math.cos(y * 0.09)
                + 0.30 * math.sin((x + y) * 0.21))

    def z(self, x, y):
        z = self.base_z(x, y) + self.relief(x, y)
        for poly, h in self.ridges:
            if poly_inside((x, y), poly):
                z += h * smoothstep(dist_to_poly_edge((x, y), poly) / RIDGE_FALLOFF)
        for path, w, depth in self.waters:
            d = dist_to_path((x, y), path)
            half = w / 2.0
            if d < half:
                z -= depth
            elif d < half + BANK:
                z -= depth * (1.0 - smoothstep((d - half) / BANK))
        for path, w, _ in self.roads:
            d = dist_to_path((x, y), path)
            half = w / 2.0 + 1.5
            if d < half:
                z -= self.relief(x, y) * (1.0 - smoothstep(d / half)) * 0.9
        return self.shelf_z(x, y, z)

    def shelf_z(self, x, y, z):
        """浅滩：`over_water = true` 且写了 `shallow_m` 的块，块内地面抬到水面下 shallow_m 米。
        湖面是几条粗折线拼的，岸边浅水常落在湖心那么深（bg8 芦苇浅滩在两片湖水叠加处被算成 −10 m，
        ep02 S25 人和机位都在水下 6 m，2026-09-30）；站人的浅水要在块里写明有多深。"""
        for b in self.blocks:
            if not (b.get("over_water") and "shallow_m" in b):
                continue
            (cx, cy), (sx, sy) = b["xy"], b["size"]
            if abs(x - cx) > sx / 2.0 or abs(y - cy) > sy / 2.0:
                continue
            surf = [self.base_z(x, y) - depth + 0.9 for path, w, depth in self.waters
                    if dist_to_path((x, y), path) < w / 2.0 + BANK]
            if not surf:
                raise SystemExit("[%s] 「%s」写了 shallow_m，可块里没有水" % (self.bg, b["name"]))
            return min(surf) - float(b["shallow_m"])
        return z


# ── 平面几何 ──────────────────────────────────────────────────────────
def poly_inside(pt, poly):
    x, y = pt
    inside = False
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        if (y0 > y) != (y1 > y):
            if x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
                inside = not inside
    return inside


def dist_to_seg(p, a, b):
    px, py = p
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    if L2 < 1e-9:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def dist_to_poly_edge(pt, poly):
    return min(dist_to_seg(pt, poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly)))


def dist_to_path(pt, path):
    return min(dist_to_seg(pt, path[i], path[i + 1]) for i in range(len(path) - 1))


def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def densify(path, step):
    out = []
    for a, b in zip(path, path[1:]):
        k = max(1, int(math.dist(a, b) // step))
        for i in range(k):
            out.append((a[0] + (b[0] - a[0]) * i / k, a[1] + (b[1] - a[1]) * i / k))
    out.append(tuple(path[-1]))
    return out


def path_x_at(path, gy):
    """折线在给定 y 上的 x；没穿过就 None。"""
    for a, b in zip(path, path[1:]):
        if (a[1] - gy) * (b[1] - gy) <= 0 and abs(b[1] - a[1]) > 1e-6:
            return a[0] + (b[0] - a[0]) * (gy - a[1]) / (b[1] - a[1])
    return None


# ── Blender 基础件 ────────────────────────────────────────────────────
def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def coll(name, parent=None):
    c = bpy.data.collections.new(name)
    (parent or bpy.context.scene.collection).children.link(c)
    return c


def mesh_from(name, verts, faces, parent):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    parent.objects.link(o)
    return o


def box(name, cx, cy, cz, sx, sy, sz, parent, rot=0.0):
    hx, hy, hz = sx / 2.0, sy / 2.0, sz / 2.0
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    v = []
    for dz in (-hz, hz):
        for dx, dy in ((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)):
            v.append((cx + dx * c - dy * s, cy + dx * s + dy * c, cz + dz))
    f = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    return mesh_from(name, v, f, parent)


def gable(name, cx, cy, z0, sx, sy, wall_h, ridge_h, parent, rot=0.0, along_x=True):
    box(name + "_墙", cx, cy, z0 + wall_h / 2.0, sx, sy, wall_h, parent, rot)
    hx, hy = sx / 2.0, sy / 2.0
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))

    def W(dx, dy, dz):
        return (cx + dx * c - dy * s, cy + dx * s + dy * c, z0 + wall_h + dz)

    e = 0.6
    if along_x:
        v = [W(-hx - e, -hy - e, 0), W(hx + e, -hy - e, 0), W(hx + e, hy + e, 0),
             W(-hx - e, hy + e, 0), W(-hx, 0, ridge_h), W(hx, 0, ridge_h)]
    else:
        v = [W(-hx - e, -hy - e, 0), W(hx + e, -hy - e, 0), W(hx + e, hy + e, 0),
             W(-hx - e, hy + e, 0), W(0, -hy, ridge_h), W(0, hy, ridge_h)]
    f = [(0, 1, 5, 4), (3, 2, 5, 4), (0, 3, 4), (1, 2, 5), (0, 1, 2, 3)]
    return mesh_from(name + "_顶", v, f, parent)


def cone(name, cx, cy, z0, r, h, parent, seg=10):
    v = [(cx, cy, z0 + h)]
    for i in range(seg):
        a = 2 * math.pi * i / seg
        v.append((cx + r * math.cos(a), cy + r * math.sin(a), z0))
    f = [(0, 1 + i, 1 + (i + 1) % seg) for i in range(seg)]
    f.append(tuple(range(1, seg + 1)))
    return mesh_from(name, v, f, parent)


def cyl(name, cx, cy, z0, r, h, parent, seg=10, r_top=None):
    rt = r if r_top is None else r_top
    v = []
    for dz, rr in ((0.0, r), (h, rt)):
        for i in range(seg):
            a = 2 * math.pi * i / seg
            v.append((cx + rr * math.cos(a), cy + rr * math.sin(a), z0 + dz))
    f = [(i, (i + 1) % seg, seg + (i + 1) % seg, seg + i) for i in range(seg)]
    f.append(tuple(range(seg)))
    f.append(tuple(range(seg, 2 * seg)))
    return mesh_from(name, v, f, parent)


def ribbon(S, name, path, width, parent, lift=0.12):
    verts, faces = [], []
    for i, (px, py) in enumerate(path):
        a = path[max(0, i - 1)]
        b = path[min(len(path) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L * width / 2.0, dx / L * width / 2.0
        for sgn in (-1, 1):
            gx, gy = px + sgn * nx, py + sgn * ny
            bx, by = S.P(gx, gy)
            verts.append((bx, by, S.z(gx, gy) + lift))
    for i in range(len(path) - 1):
        faces.append((2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2))
    return mesh_from(name, verts, faces, parent)


# ── 地形 / 水 / 路 ────────────────────────────────────────────────────
def build_terrain(S, root):
    g = coll("地形", root)
    cell = max(1.0, math.sqrt(S.W * S.H / CELL_MAX_VERTS))
    nx, ny = int(S.W / cell) + 1, int(S.H / cell) + 1
    verts = []
    for j in range(ny):
        for i in range(nx):
            gx, gy = min(i * cell, S.W), min(j * cell, S.H)
            bx, by = S.P(gx, gy)
            verts.append((bx, by, S.z(gx, gy)))
    faces = [(j * nx + i, j * nx + i + 1, (j + 1) * nx + i + 1, (j + 1) * nx + i)
             for j in range(ny - 1) for i in range(nx - 1)]
    mesh_from("地面" if S.interior else "地形", verts, faces, g)
    return nx * ny


def build_water(S, root):
    if not S.waters:
        return 0
    g = coll("水系", root)
    for path, w, depth in S.waters:
        dense = densify(path, 6.0)
        verts, faces = [], []
        for i, (px, py) in enumerate(dense):
            a = dense[max(0, i - 1)]
            b = dense[min(len(dense) - 1, i + 1)]
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy) or 1.0
            nx, ny = -dy / L * w / 2.0, dx / L * w / 2.0
            for sgn in (-1, 1):
                gx, gy = px + sgn * nx, py + sgn * ny
                bx, by = S.P(gx, gy)
                verts.append((bx, by, S.base_z(px, py) - depth + 0.9))
        for i in range(len(dense) - 1):
            faces.append((2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2))
        mesh_from("水面", verts, faces, g)
    return len(S.waters)


def build_roads(S, root):
    if not S.roads:
        return 0
    g = coll("道路", root)
    for path, w, name in S.roads:
        ribbon(S, name or "路", densify(path, 6.0), w, g)
    return len(S.roads)


# ══ kind 建法 ═════════════════════════════════════════════════════════
# 每个函数签名 (S, b, g) -> 构件数。新增建法加在这里，**不要拷脚本**。

def _xy(S, b):
    gx, gy = b["xy"]
    sx, sy = b["size"]
    bx, by = S.P(gx, gy)
    return gx, gy, sx, sy, bx, by, S.z(gx, gy), float(b["h_m"])


# 朝向面 → (外法线方向, 沿墙方向)，都在 Blender 帧（+X 东、+Y 北）。
# 卡里写的是「门朝西」「柱正面朝东南」这种方位契约，建法必须能照着摆，
# 否则每个非南向的建筑都要靠作者在 toml 里手算一个 rot —— 那是会漂的。
FACES = {
    "south": ((0.0, -1.0), (1.0, 0.0)),
    "north": ((0.0, 1.0), (-1.0, 0.0)),
    "west": ((-1.0, 0.0), (0.0, -1.0)),
    "east": ((1.0, 0.0), (0.0, 1.0)),
    "southeast": ((0.7071, -0.7071), (0.7071, 0.7071)),
    "southwest": ((-0.7071, -0.7071), (-0.7071, 0.7071)),
    "northeast": ((0.7071, 0.7071), (-0.7071, 0.7071)),
    "northwest": ((-0.7071, 0.7071), (-0.7071, -0.7071)),
}


def face_of(b):
    f = str(b.get("face", "south"))
    if f not in FACES:
        raise SystemExit("「%s」的 face=%s 不认识。只许：%s"
                         % (b["name"], f, " / ".join(sorted(FACES))))
    return f


def face_frame(b, sx, sy):
    """返回 (法线, 切向, 该面到中心的半距, 该面的面宽, 面朝向角度)。"""
    f = face_of(b)
    (nx, ny), (tx, ty) = FACES[f]
    half = abs(nx) * sx / 2.0 + abs(ny) * sy / 2.0
    width = abs(tx) * sx + abs(ty) * sy
    ang = math.degrees(math.atan2(ny, nx)) + 90.0
    return (nx, ny), (tx, ty), half, width, ang


def k_hall(S, b, g):
    """通用坡屋顶建筑：墙 + 双坡 + 南面一门两窗。多数房子用它就够。"""
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    rot = float(b.get("rot", 0))
    gable(b["name"], bx, by, z0, sx, sy, h * 0.65, h * 0.35, g, rot,
          along_x=b.get("ridge_axis", "x") == "x")
    (nx, ny), (tx, ty), half, width, ang = face_frame(b, sx, sy)
    dx, dy = bx + nx * (half + 0.1), by + ny * (half + 0.1)
    box(b["name"] + "_门", dx, dy, z0 + DOOR_H / 2.0, DOOR_W, 0.4, DOOR_H, g, ang)
    if width >= DOOR_W + 4.0:
        for sgn in (-1, 1):
            o = sgn * (DOOR_W / 2.0 + 1.8)
            box(b["name"] + "_窗%d" % (1 if sgn < 0 else 2),
                bx + nx * (half + 0.08) + tx * o, by + ny * (half + 0.08) + ty * o,
                z0 + h * 0.42, 1.1, 0.4, 1.5, g, ang)
    return 1


def k_abbey_hall(S, b, g):
    """修道院主厅：南立面居中半圆拱门 + 三级石阶，两侧高处一排拱形高窗。

    **没有钟楼**——`bg2` 卡的 `abbey.012` negative 明排「地下室 / 钟楼 / 回廊庭院 /
    多层塔楼」。第一版建了一座，属版本错置，已删。
    两翼在**东西两侧**（`bg2` 卡：主厅西通武器厅、东通图书馆翼），所以
    **南立面就是正脸**，正门开在这里，而不是某个翼上。
    """
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    wall_h = h * 0.62
    gable("主厅", bx, by, z0, sx, sy, wall_h, h - wall_h, g, along_x=True)
    ys = by - sy / 2.0
    box("正门_门洞", bx, ys - 0.12, z0 + DOOR_H / 2.0, DOOR_W, 0.45, DOOR_H, g)
    seg = 13
    for i in range(seg + 1):    # 半圆拱券：竖向楔块砌出轮廓，比贴一块门板好读得多
        a = math.pi * i / seg
        box("拱券石%d" % (i + 1), bx - (DOOR_W / 2.0 + 0.28) * math.cos(a), ys - 0.16,
            z0 + DOOR_H + (DOOR_W / 2.0 + 0.28) * math.sin(a), 0.42, 0.34, 0.42, g)
    for i in range(3):
        box("门前石阶%d" % (i + 1), bx, ys - 0.7 - i * 0.6, z0 + 0.45 - i * 0.2,
            DOOR_W + 3.0 - i * 0.6, 1.2, 0.4, g)
    nb = max(2, int((sx - BAY) // BAY))
    for i in range(nb):
        wx = bx - (nb - 1) * BAY / 2.0 + i * BAY
        if abs(wx - bx) < DOOR_W + 1.2:
            continue
        box("南立面高窗%d" % (i + 1), wx, ys - 0.15, z0 + wall_h * 0.74, 1.2, 0.5, 2.8, g)
    for sgn, tag in ((-1, "西"), (1, "东")):
        for i in range(3):
            box("侧高窗_%s%d" % (tag, i + 1), bx + sgn * (sx / 2.0 + 0.1),
                by - sy / 4.0 + i * sy / 4.0, z0 + wall_h * 0.74, 0.5, 1.2, 2.6, g)
    return 1


def k_low_wall(S, b, g):
    """矮院墙 / 矮石墙：`size = [长, 厚]`，`rot` 定走向，墙头一排不规则压顶石。
    `gate_w > 0` 时正中留一道口子并装铁栅与门柱。"""
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    sx, sy, rot = _along(sx, sy, float(b.get("rot", 0)))
    rr = math.radians(rot)
    gw = float(b.get("gate_w", 0.0))
    nm = b["name"]
    n = 0
    spans = [(-sx / 2.0, sx / 2.0)] if gw <= 0 else [(-sx / 2.0, -gw / 2.0), (gw / 2.0, sx / 2.0)]
    for a, b2 in spans:
        if b2 - a < 0.3:
            continue
        d = (a + b2) / 2.0
        box(nm, bx + d * math.cos(rr), by + d * math.sin(rr), z0 + h / 2.0,
            b2 - a, sy, h, g, rot)
        n += 1
        k = max(2, int((b2 - a) // 0.9))
        for i in range(k):
            dd = a + (b2 - a) * (i + 0.5) / k
            box(nm + "_压顶%d" % (i + 1), bx + dd * math.cos(rr), by + dd * math.sin(rr),
                z0 + h + 0.09, (b2 - a) / k * 0.85, sy * 1.25, 0.18, g, rot)
            n += 1
    if gw > 0:
        for sgn in (-1, 1):
            d = sgn * gw / 2.0
            box(nm + "_门柱%d" % (1 if sgn < 0 else 2), bx + d * math.cos(rr),
                by + d * math.sin(rr), z0 + h * 0.75, sy * 1.4, sy * 1.4, h * 1.5, g, rot)
            n += 1
        k = max(3, int(gw // 0.28))
        for i in range(k):
            dd = -gw / 2.0 + gw * (i + 0.5) / k
            box(nm + "_栅条%d" % (i + 1), bx + dd * math.cos(rr), by + dd * math.sin(rr),
                z0 + h * 0.55, 0.06, 0.06, h * 1.1, g, rot)
            n += 1
    return n


def k_hall_shell(S, b, g):
    """**空心**厅：四壁 + 坡顶 + 南面门洞，室内机位进得去。
    `bg2` 的堂内 / 书翼 / 楼上三张 plate 靠它才有东西可拍。"""
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    t = float(b.get("wall_t", WALL_T))
    wall_h = h * float(b.get("wall_ratio", 0.62))
    nm = b["name"]
    (fnx, fny), _t2, _h2, _w2, _a2 = face_frame(b, sx, sy)
    for ux, uy, tag, ln in ((-1, 0, "西", sy), (1, 0, "东", sy),
                            (0, -1, "南", sx), (0, 1, "北", sx)):
        if abs(ux - fnx) < 0.4 and abs(uy - fny) < 0.4:
            continue            # 正面那一堵由下面带门洞地砌
        along_x = uy != 0
        box(nm + "_壁" + tag, bx + ux * (sx - t) / 2.0, by + uy * (sy - t) / 2.0,
            z0 + wall_h / 2.0, (ln - 2 * t) if along_x else t,
            t if along_x else ln, wall_h, g)
    dw = float(b.get("door_w", DOOR_W))
    (nx, ny), (tx, ty), half, fw, ang = face_frame(b, sx, sy)
    segw = (fw - 2 * t - dw) / 2.0
    for sgn in (-1, 1):
        o = sgn * (dw + segw) / 2.0
        box(nm + "_正面壁%d" % (1 if sgn < 0 else 2),
            bx + nx * (half - t / 2.0) + tx * o, by + ny * (half - t / 2.0) + ty * o,
            z0 + wall_h / 2.0, segw, t, wall_h, g, ang)
    box(nm + "_门楣", bx + nx * (half - t / 2.0), by + ny * (half - t / 2.0),
        z0 + DOOR_H + (wall_h - DOOR_H) / 2.0, dw, t, wall_h - DOOR_H, g, ang)
    if b.get("arch"):
        seg = 13
        for i in range(seg + 1):
            a = math.pi * i / seg
            o = -(dw / 2.0 + 0.28) * math.cos(a)
            box(nm + "_拱券石%d" % (i + 1), bx + nx * (half + 0.06) + tx * o,
                by + ny * (half + 0.06) + ty * o,
                z0 + DOOR_H + (dw / 2.0 + 0.28) * math.sin(a), 0.42, 0.34, 0.42, g, ang)
        for i in range(3):
            box(nm + "_石阶%d" % (i + 1), bx + nx * (half + 0.7 + i * 0.6),
                by + ny * (half + 0.7 + i * 0.6), z0 + 0.45 - i * 0.2,
                dw + 3.0 - i * 0.6, 1.2, 0.4, g, ang)
    box(nm + "_地坪", bx, by, z0 + 0.05, sx, sy, 0.1, g)
    nf = max(1, int((fw - dw - 2 * BAY) // BAY))
    for i in range(nf):         # 正面开间窗：没有它，立面渲出来就是一堵白板
        o = -(nf - 1) * BAY / 2.0 + i * BAY
        if abs(o) < dw / 2.0 + 1.0:
            continue
        box(nm + "_正面窗%d" % (i + 1), bx + nx * (half + 0.08) + tx * o,
            by + ny * (half + 0.08) + ty * o, z0 + wall_h * 0.68, 1.2, 0.45, 2.4, g, ang)
    k = max(2, int((sx - 2 * BAY) // BAY))
    for sgn in (-1, 1):         # 两侧高处一排拱形高窗（堂内的主光来源）
        for i in range(k):
            box(nm + "_高窗%s%d" % ("西" if sgn < 0 else "东", i + 1),
                bx + sgn * (sx / 2.0 - t / 2.0), by - sy / 2.0 + sy * (i + 0.5) / k,
                z0 + wall_h * 0.76, t * 1.2, 1.2, 2.2, g)
    hx, hy, e = sx / 2.0, sy / 2.0, 0.6
    v = [(bx - hx - e, by - hy - e, z0 + wall_h), (bx + hx + e, by - hy - e, z0 + wall_h),
         (bx + hx + e, by + hy + e, z0 + wall_h), (bx - hx - e, by + hy + e, z0 + wall_h),
         (bx - hx, by, z0 + h), (bx + hx, by, z0 + h)]
    mesh_from(nm + "_顶", v, [(0, 1, 5, 4), (3, 2, 5, 4), (0, 3, 4), (1, 2, 5)], g)
    return 8 + 2 * k


def k_altar(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    box("祭台_基", bx, by, z0 + h * 0.18, sx + 1.2, sy + 1.0, h * 0.36, g)
    box("祭台_体", bx, by, z0 + h * 0.6, sx, sy, h * 0.55, g)
    box("祭台_面", bx, by, z0 + h + 0.08, sx + 0.5, sy + 0.4, 0.16, g)
    return 3


def k_stair(S, b, g):
    """石旋梯：绕中心柱盘上去的踏步。给室内机位一个纵向锚。"""
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    r = min(sx, sy) / 2.0
    cyl("旋梯_心柱", bx, by, z0, 0.32, h, g, seg=8)
    k = max(6, int(h / 0.22))
    for i in range(k):
        a = 2 * math.pi * i / 12.0
        box("旋梯_踏步%d" % (i + 1), bx + math.cos(a) * r * 0.55, by + math.sin(a) * r * 0.55,
            z0 + 0.11 + i * (h / k), r * 0.9, 0.7, 0.16, g, rot=math.degrees(a))
    return k + 1


def k_shelves(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    k = int(b.get("count", 4))
    for i in range(k):
        py = by - sy / 2.0 + sy * (i + 0.5) / k
        box("书架%d_体" % (i + 1), bx, py, z0 + h / 2.0, sx * 0.9, 0.5, h, g)
        for j in range(3):
            box("书架%d_层%d" % (i + 1, j + 1), bx, py - 0.3, z0 + h * (0.3 + 0.24 * j),
                sx * 0.88, 0.22, 0.1, g)
    return k


def k_tables(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    k = int(b.get("count", 2))
    for i in range(k):
        py = by - sy / 2.0 + sy * (i + 0.5) / k
        box("长桌%d_面" % (i + 1), bx, py, z0 + h, sx * 0.85, 1.0, 0.12, g)
        for sgn in (-1, 1):
            box("长桌%d_腿%d" % (i + 1, 1 if sgn < 0 else 2), bx + sgn * sx * 0.36, py,
                z0 + h / 2.0, 0.16, 0.9, h, g)
            box("长凳%d-%d" % (i + 1, 1 if sgn < 0 else 2), bx, py + sgn * 1.0,
                z0 + h * 0.6, sx * 0.8, 0.35, 0.1, g)
    return k * 2


def k_yard(S, b, g):
    """夯土 / 石板混铺空场。**默认不放训练假人**——Vanilla 1.12 的北郡院内院外
    都没有木桩靶，那是 4.0.3a 加的（本剧黑名单第 15 条）。别的剧要假人写 `dummies = N`。"""
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    box(b["name"] + "_地面", bx, by, z0 + 0.05, sx, sy, 0.1, g)
    n = 1
    for i in range(int(b.get("dummies", 0))):
        px = bx - sx / 4.0 + i * 2.6
        cyl("木人桩%d_身" % (i + 1), px, by, z0, 0.22, 1.7, g, seg=8)
        box("木人桩%d_臂" % (i + 1), px, by, z0 + 1.45, 1.5, 0.2, 0.2, g)
        n += 2
    return n


def k_post(S, b, g):
    """木柱 + 挂板：通缉告示柱 / 路牌 / 旗杆。`h_m` 是柱高。"""
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    nm = b["name"]
    papers = int(b.get("papers", 3))
    cyl(nm + "_柱", bx, by, z0, max(0.12, min(sx, sy) * 0.18), h, g, seg=8)
    box(nm + "_板", bx, by - min(sx, sy) * 0.2, z0 + h * 0.62,
        max(0.7, sx * 0.9), 0.12, max(0.9, h * 0.34), g)
    for i in range(papers):
        box(nm + "_告示%d" % (i + 1), bx - sx * 0.12 + i * sx * 0.12,
            by - min(sx, sy) * 0.2 - 0.07, z0 + h * 0.6 + i * 0.06,
            0.42, 0.02, 0.56, g, rot=(i - 1) * 6)
    return 2 + papers


def k_rock_shelf(S, b, g):
    """裸岩台：水平层理的岩板 + 风化断口。霍格山丘顶那块。"""
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    nm = b["name"]
    layers = max(2, int(b.get("layers", 3)))
    for i in range(layers):
        f = 1.0 - 0.13 * i
        box(nm + "_层%d" % (i + 1), bx + i * 0.4, by - i * 0.3,
            z0 + h * (i + 0.5) / layers, sx * f, sy * f, h / layers, g, rot=i * 5)
    for i in range(3):
        cone(nm + "_断口%d" % (i + 1), bx - sx * 0.3 + i * sx * 0.3,
             by - sy * 0.45, z0, 0.9, h * 0.8, g, seg=5)
    return layers + 3


def k_entrance_wing(S, b, g):
    """门廊 range —— 低入口体量，正门开在它南面，高堂从它屋顶上方升起。"""
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    wall_h = h * 0.6
    gable(b["name"], bx, by, z0, sx, sy, wall_h, h - wall_h, g, along_x=True)
    ys = by - sy / 2.0
    pd = 2.6
    gable("门廊", bx, ys - pd / 2.0, z0, DOOR_W + 2.4, pd, DOOR_H + 0.4, 1.6, g, along_x=False)
    box("门洞", bx, ys - pd - 0.05, z0 + DOOR_H / 2.0, DOOR_W, 0.4, DOOR_H, g)
    for sgn in (-1, 1):
        cyl("门柱%s" % ("西" if sgn < 0 else "东"), bx + sgn * (DOOR_W / 2.0 + 0.45),
            ys - pd + 0.3, z0, 0.28, DOOR_H, g, seg=8)
    for i in range(3):
        box("门前阶%d" % (i + 1), bx, ys - pd - 0.55 - i * 0.6, z0 + 0.5 - i * 0.2,
            DOOR_W + 2.8 - i * 0.6, 1.2, 0.4, g)
    for sgn in (-1, 1):
        box("门侧窗%s" % ("西" if sgn < 0 else "东"), bx + sgn * (DOOR_W / 2.0 + 2.6),
            ys - 0.15, z0 + wall_h * 0.6, 1.1, 0.4, 2.2, g)
    return 1


def k_wing(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    gable(b["name"], bx, by, z0, sx, sy, h * 0.65, h * 0.35, g, along_x=True)
    box(b["name"] + "_门", bx, by - sy / 2.0 - 0.1, z0 + DOOR_H / 2, DOOR_W, 0.5, DOOR_H, g)
    return 1


def k_lawn(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    box(b["name"] + "_地坪", bx, by, z0 + 0.05, sx, sy, 0.1, g)
    for sgn in (-1, 1):
        box(b["name"] + "_院墙%s" % ("西" if sgn < 0 else "东"),
            bx + sgn * sx / 2.0, by, z0 + 0.55, 0.5, sy, 1.1, g)
    return 1


def k_plaza(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    box(b["name"], bx, by, z0 + 0.06, sx, sy, 0.12, g)
    return 1


def k_graveyard(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    cols = max(2, int(sx // 4.5))
    rows = max(2, int(sy // 4.5))
    n = 0
    for i in range(cols):
        for j in range(rows):
            px = bx - sx / 2.0 + sx * (i + 0.5) / cols
            py = by - sy / 2.0 + sy * (j + 0.5) / rows
            tall = (i + j) % 4 == 0
            if tall:
                box("十字碑%d-%d_立" % (i + 1, j + 1), px, py, z0 + 0.8, 0.26, 0.26, 1.6, g)
                box("十字碑%d-%d_横" % (i + 1, j + 1), px, py, z0 + 1.25, 0.9, 0.22, 0.24, g)
            else:
                box("墓碑%d-%d" % (i + 1, j + 1), px, py, z0 + 0.55, 0.72, 0.22, 1.1, g)
            n += 1
    return n


def k_crypt(S, b, g):
    """小石室 / 陵屋：平顶厚墙 + 一个拱口。墓地里的视觉锚。"""
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    box(b["name"] + "_体", bx, by, z0 + h / 2.0, sx, sy, h, g)
    box(b["name"] + "_檐", bx, by, z0 + h + 0.2, sx + 1.0, sy + 1.0, 0.4, g)
    box(b["name"] + "_口", bx, by - sy / 2.0 - 0.1, z0 + DOOR_H / 2.0, DOOR_W * 0.8, 0.4, DOOR_H, g)
    return 1


def k_stalls(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    k = int(b.get("count", 4))
    for i in range(k):
        py = by - sy / 2.0 + sy * (i + 0.5) / k
        box("摊台%d" % (i + 1), bx, py, z0 + 0.5, sx * 0.55, 1.6, 1.0, g)
        box("顶棚%d" % (i + 1), bx, py, z0 + 2.5, sx * 0.8, 2.4, 0.2, g)
        for sgn in (-1, 1):
            cyl("棚柱%d%s" % (i + 1, "西" if sgn < 0 else "东"), bx + sgn * sx * 0.38,
                py, z0, 0.09, 2.5, g, seg=6)
    return k


def k_stable(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    gable("马厩", bx, by, z0, sx, sy, h * 0.6, h * 0.4, g, along_x=True)
    for i in range(3):
        box("马栏隔板%d" % (i + 1), bx - sx / 2.0 + sx * (i + 1) / 4.0,
            by - sy / 2.0 - 1.4, z0 + 0.6, 0.18, 2.8, 1.2, g)
    box("草料槽", bx, by - sy / 2.0 - 2.6, z0 + 0.35, sx * 0.7, 0.8, 0.7, g)
    return 1


def k_kobold_camp(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    cyl("火堆_石圈", bx, by, z0, 1.5, 0.35, g, seg=9)
    cone("火堆_柴", bx, by, z0 + 0.3, 0.8, 1.1, g, seg=6)
    n = 1
    k = int(b.get("count", 4))
    for i in range(k):
        a = math.pi * (0.25 + i * 2.0 / k)
        cone("狗头人帐篷%d" % (i + 1), bx + math.cos(a) * sx * 0.32,
             by + math.sin(a) * sy * 0.32, z0, 2.0, 2.6, g, seg=7)
        n += 1
    for i in range(3):
        box("矿石箱%d" % (i + 1), bx - sx * 0.3 + i * 2.2, by - sy * 0.34,
            z0 + 0.45, 1.3, 1.0, 0.9, g)
        n += 1
    return n


def k_mine_portal(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    mw, mh = sx * 0.45, h * 0.62
    for sgn in (-1, 1):
        box("洞口岩壁%s" % ("西" if sgn < 0 else "东"), bx + sgn * (mw / 2 + sx * 0.18),
            by, z0 + h / 2.0, sx * 0.36, sy, h, g)
    box("洞口过梁", bx, by, z0 + mh + 0.5, mw + sx * 0.36, sy, 1.0, g)
    for sgn in (-1, 1):
        box("洞口木柱%s" % ("西" if sgn < 0 else "东"), bx + sgn * mw / 2.0,
            by - sy / 2.0 + 0.4, z0 + mh / 2.0, 0.45, 0.45, mh, g)
    box("洞口横木", bx, by - sy / 2.0 + 0.4, z0 + mh, mw + 0.9, 0.45, 0.45, g)
    box("矿车", bx - mw * 0.55, by - sy / 2.0 - 2.2, z0 + 0.7, 1.6, 1.0, 1.0, g)
    for sgn in (-1, 1):
        cyl("矿车轮%s" % ("前" if sgn < 0 else "后"), bx - mw * 0.55,
            by - sy / 2.0 - 2.2 + sgn * 0.5, z0 + 0.35, 0.35, 0.16, g, seg=8)
    return 5


def k_vineyard(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    rows = max(2, int(b.get("rows", max(2, int(sy // 6)))))
    for j in range(rows):
        py = by - sy / 2.0 + sy * (j + 0.5) / rows
        box("藤垄%d_架" % (j + 1), bx, py, z0 + h * 0.72, sx * 0.86, 0.35, 0.22, g)
        box("藤垄%d_叶" % (j + 1), bx, py, z0 + h * 0.5, sx * 0.86, 1.5, h * 0.42, g)
        for i in range(5):
            cyl("藤垄%d_桩%d" % (j + 1, i + 1), bx - sx * 0.43 + sx * 0.86 * i / 4.0,
                py, z0, 0.1, h * 0.75, g, seg=6)
    return rows


def k_hut_camp(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    gable("小屋", bx, by, z0, sx * 0.62, sy * 0.68, h * 0.62, h * 0.38, g, along_x=False)
    box("小屋_门", bx, by - sy * 0.34 - 0.1, z0 + DOOR_H / 2, DOOR_W * 0.8, 0.4, DOOR_H, g)
    for sgn in (-1, 1):
        cone("随从帐篷%s" % ("西" if sgn < 0 else "东"), bx + sgn * sx * 0.42,
             by - sy * 0.3, z0, 1.8, 2.4, g, seg=7)
    cyl("营火_石圈", bx, by - sy * 0.42, z0, 1.1, 0.3, g, seg=8)
    return 5


def k_gate_wall(S, b, g):
    """关墙：走人的窄门 + 河的水门。**水门位置从水系折线算**，改河道自动跟着走。"""
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    gate_w, gate_h = float(b.get("gate_w", 5.0)), DOOR_H + 1.6
    openings = [(gx, gate_w, "人门")]
    for path, w, _d in S.waters:
        cx = path_x_at(path, gy)
        if cx is not None and abs(cx - gx) < sx / 2.0 - w:
            openings.append((cx, w + 3.0, "水门"))
    openings.sort()

    n = 0
    edges = [gx - sx / 2.0] + [c for c, _w, _t in openings] + [gx + sx / 2.0]
    widths = [0.0] + [w for _c, w, _t in openings] + [0.0]
    for i in range(len(edges) - 1):
        a = edges[i] + widths[i] / 2.0
        b2 = edges[i + 1] - widths[i + 1] / 2.0
        if b2 - a < 0.5:
            continue
        segw = b2 - a
        px, _ = S.P((a + b2) / 2.0, gy)
        box("关墙_段%d" % (i + 1), px, by, z0 + h / 2.0, segw, sy, h, g)
        n += 1
        k = max(2, int(segw // 2.4))
        for j in range(0, k, 2):
            mx, _ = S.P(a + segw * (j + 0.5) / k, gy)
            box("垛口%d-%d" % (i + 1, j + 1), mx, by, z0 + h + 0.55,
                segw / k * 0.8, sy * 0.8, 1.1, g)
            n += 1
    for c, w, tag in openings:
        px, _ = S.P(c, gy)
        top = gate_h if tag == "人门" else h * 0.42
        box("关墙_%s过梁" % tag, px, by, z0 + top + (h - top) / 2.0, w, sy, h - top, g)
        n += 1
    from tools.previz import planschema   # 门塔尺寸与平面图共用一处（shot_overhead 按同一份查人与机位）
    for d in planschema.derived(b):
        px, _ = S.P(d["xy"][0], gy)
        box(d["name"], px, by, z0 + d["h_m"] / 2.0, d["size"][0], d["size"][1], d["h_m"], g)
        n += 1
    return n


def k_arch_bridge(S, b, g):
    """拱桥：沿占地的长轴跨（东西长就东西跨；南北长就南北跨——平面图里南北向的桥不必再写 rot）。"""
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    ns = sy > sx
    L, Wd = (sy, sx) if ns else (sx, sy)
    ends = ((gx, gy - L / 2.0), (gx, gy + L / 2.0)) if ns else ((gx - L / 2.0, gy), (gx + L / 2.0, gy))
    deck = max(S.z(*ends[0]), S.z(*ends[1])) + 1.0
    box("桥面", bx, by, deck, sx, sy, 0.6, g)
    for sgn in (-1, 1):
        if ns:
            box("桥栏%s" % ("东" if sgn > 0 else "西"), bx + sgn * (Wd / 2.0 - 0.25), by, deck + 0.75, 0.4, L, 1.1, g)
        else:
            box("桥栏%s" % ("北" if sgn > 0 else "南"), bx, by + sgn * (Wd / 2.0 - 0.25), deck + 0.75, L, 0.4, 1.1, g)
    steps = 7
    for i in range(steps):
        a0 = -L / 2.0 * math.cos(math.pi * i / steps)
        a1 = -L / 2.0 * math.cos(math.pi * (i + 1) / steps)
        mid, seg = (a0 + a1) / 2.0, abs(a1 - a0) + 0.1
        if ns:
            box("拱石%d" % (i + 1), bx, by + mid, deck - 0.35, Wd * 0.9, seg, 0.55, g)
        else:
            box("拱石%d" % (i + 1), bx + mid, by, deck - 0.35, seg, Wd * 0.9, 0.55, g)
    return 3


def k_guard_post(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    for dx in (-1, 1):
        for dy in (-1, 1):
            cyl("哨位柱%d%d" % (dx, dy), bx + dx * sx * 0.38, by + dy * sy * 0.38,
                z0, 0.14, h * 0.8, g, seg=6)
    box("哨位_顶", bx, by, z0 + h * 0.85, sx, sy, 0.3, g)
    box("哨位_兵器架", bx, by + sy * 0.3, z0 + 0.6, sx * 0.7, 0.3, 1.2, g)
    return 3


def k_tower(S, b, g):
    """方塔 / 箭塔：塔身 + 出挑战台 + 垛口 + 锥顶。要塞的识别母题。"""
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    box(b["name"] + "_身", bx, by, z0 + h / 2.0, sx, sy, h, g)
    box(b["name"] + "_战台", bx, by, z0 + h + 0.35, sx + 1.2, sy + 1.2, 0.7, g)
    k = max(3, int((sx + 1.2) // 1.4))
    n = 2
    for i in range(0, k, 2):
        for sgn in (-1, 1):
            box("塔垛%d%s" % (i + 1, "南" if sgn < 0 else "北"),
                bx - (sx + 1.2) / 2.0 + (sx + 1.2) * (i + 0.5) / k,
                by + sgn * (sy + 1.2) / 2.0, z0 + h + 1.2, (sx + 1.2) / k * 0.8, 0.5, 1.0, g)
            n += 1
    if b.get("roof", True):
        cone(b["name"] + "_顶", bx, by, z0 + h + 1.7, max(sx, sy) * 0.72, 3.2, g, seg=4)
        n += 1
    for i in range(2):
        box(b["name"] + "_箭窗%d" % (i + 1), bx, by - sy / 2.0 - 0.05,
            z0 + h * (0.45 + 0.28 * i), 0.4, 0.4, 1.4, g)
        n += 1
    return n


def _along(sx, sy, rot):
    """线性构件（栅 / 墙 / 坑道）的「长、厚、走向」。平面图的 size 是世界轴向的占地（东西, 南北），
    南北走向的墙自然写成 [3, 40]、不写 rot——那样平面图画对了，这里却会把 3 m 当长度。
    所以占地南北更长时对调并转 90°；已经写了 rot 的保持原意（作者显式给了走向）。"""
    if sy > sx and not rot:
        return sy, sx, 90.0
    return sx, sy, rot


def k_palisade(S, b, g):
    """木栅栏 / 寨墙：一排尖头原木。`rot` 决定走向。"""
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    sx, sy, r = _along(sx, sy, float(b.get("rot", 0)))
    rot = math.radians(r)
    k = max(3, int(sx // 0.65))
    for i in range(k):
        d = -sx / 2.0 + sx * (i + 0.5) / k
        px, py = bx + d * math.cos(rot), by + d * math.sin(rot)
        cyl("寨桩%d" % (i + 1), px, py, z0, 0.28, h * 0.88, g, seg=6)
        cone("寨尖%d" % (i + 1), px, py, z0 + h * 0.88, 0.28, h * 0.16, g, seg=6)
    return k


def k_barracks(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    gable(b["name"], bx, by, z0, sx, sy, h * 0.6, h * 0.4, g, along_x=True)
    ys = by - sy / 2.0
    box(b["name"] + "_门", bx, ys - 0.1, z0 + DOOR_H / 2.0, DOOR_W, 0.4, DOOR_H, g)
    k = max(2, int(sx // BAY))
    for i in range(k):
        wx = bx - (k - 1) * BAY / 2.0 + i * BAY
        if abs(wx - bx) < DOOR_W:
            continue
        box(b["name"] + "_窗%d" % (i + 1), wx, ys - 0.12, z0 + h * 0.4, 1.0, 0.4, 1.3, g)
    for i in range(2):          # 门口两支旗杆
        cyl(b["name"] + "_旗杆%d" % (i + 1), bx + (-1 if i == 0 else 1) * (DOOR_W + 1.2),
            ys - 1.6, z0, 0.11, 6.0, g, seg=6)
        box(b["name"] + "_旗%d" % (i + 1), bx + (-1 if i == 0 else 1) * (DOOR_W + 1.2) + 0.7,
            ys - 1.6, z0 + 4.8, 1.4, 0.08, 1.8, g)
    return 1


def k_training_yard(S, b, g):
    """训练场：木人桩 + 兵器架 + 靶。
    ⚠ **本剧（魔兽 Vanilla 1.12）不得使用**——北郡院内院外都没有训练假人，
    那是 4.0.3a 加的（黑名单第 15 条）。本剧的空场走 `yard`。"""
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    box("训练场_地坪", bx, by, z0 + 0.05, sx, sy, 0.1, g)
    k = int(b.get("count", 4))
    n = 1
    for i in range(k):
        px = bx - sx / 2.0 + sx * (i + 0.5) / k
        cyl("木人桩%d_身" % (i + 1), px, by + sy * 0.18, z0, 0.22, 1.7, g, seg=8)
        box("木人桩%d_臂" % (i + 1), px, by + sy * 0.18, z0 + 1.45, 1.5, 0.2, 0.2, g)
        n += 2
    box("兵器架_杆", bx, by - sy * 0.3, z0 + 1.15, sx * 0.6, 0.18, 0.18, g)
    for i in range(2):
        box("兵器架_腿%d" % (i + 1), bx + (-1 if i == 0 else 1) * sx * 0.28,
            by - sy * 0.3, z0 + 0.6, 0.18, 0.5, 1.2, g)
    for i in range(int(b.get("targets", 2))):
        box("箭靶%d" % (i + 1), bx - sx * 0.25 + i * sx * 0.5, by - sy * 0.42,
            z0 + 0.9, 1.3, 0.25, 1.8, g)
        n += 1
    return n + 3


def k_well(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    r = min(sx, sy) / 2.0
    cyl("井圈", bx, by, z0, r, 1.0, g, seg=12)
    for sgn in (-1, 1):
        box("井架柱%s" % ("西" if sgn < 0 else "东"), bx + sgn * r * 0.9, by,
            z0 + h / 2.0, 0.2, 0.2, h, g)
    box("井架梁", bx, by, z0 + h, r * 2.2, 0.22, 0.22, g)
    return 3


def k_crates(S, b, g):
    """箱桶堆：可复用的杂物簇，给画面加前景遮挡。"""
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    k = int(b.get("count", 5))
    for i in range(k):
        a = 2 * math.pi * i / k
        px, py = bx + math.cos(a) * sx * 0.3, by + math.sin(a) * sy * 0.3
        if i % 2:
            cyl("木桶%d" % (i + 1), px, py, z0, 0.5, 0.95, g, seg=8)
        else:
            box("板条箱%d" % (i + 1), px, py, z0 + 0.4, 1.0, 0.9, 0.8, g, rot=i * 17)
    return k


def k_boulders(S, b, g):
    """岩块簇：山地、洞口、河岸的通用碎石。棱锥近似，别当球。"""
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    k = int(b.get("count", 6))
    for i in range(k):
        a = 2 * math.pi * i / k + 0.4
        f = 0.45 + 0.35 * ((i * 7) % 5) / 4.0
        cone("岩块%d" % (i + 1), bx + math.cos(a) * sx * 0.32, by + math.sin(a) * sy * 0.32,
             z0 - h * 0.15, h * f * 0.9, h * f, g, seg=5)
    return k


def k_tree_cluster(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    k = int(b.get("count", 5))
    for i in range(k):
        a = 2 * math.pi * i / k + 0.9
        px, py = bx + math.cos(a) * sx * 0.32, by + math.sin(a) * sy * 0.32
        cyl("树干%d" % (i + 1), px, py, z0, 0.32, h * 0.45, g, seg=6)
        cone("树冠%d" % (i + 1), px, py, z0 + h * 0.4, h * 0.3, h * 0.6, g, seg=7)
    return k * 2


def k_campfire(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    cyl("火塘石圈", bx, by, z0, min(sx, sy) * 0.4, 0.32, g, seg=10)
    cone("柴堆", bx, by, z0 + 0.28, min(sx, sy) * 0.22, h * 0.7, g, seg=6)
    for sgn in (-1, 1):
        box("原木座%s" % ("西" if sgn < 0 else "东"), bx + sgn * sx * 0.42, by,
            z0 + 0.25, 0.5, sy * 0.6, 0.5, g)
    return 4


def k_tent_cluster(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    k = int(b.get("count", 3))
    for i in range(k):
        px = bx - sx / 2.0 + sx * (i + 0.5) / k
        cone("帐篷%d" % (i + 1), px, by, z0, min(2.4, sx / k * 0.42), h, g, seg=7)
    return k


def k_cave_mouth(S, b, g):
    """山体上的洞口：一圈岩唇 + 黑口 + 散石。与 mine_portal 的区别是没有人工木框。"""
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    for sgn in (-1, 1):
        cone("洞唇%s" % ("西" if sgn < 0 else "东"), bx + sgn * sx * 0.34, by,
             z0, sx * 0.3, h, g, seg=6)
    cone("洞顶岩", bx, by + sy * 0.3, z0, sx * 0.34, h * 1.1, g, seg=6)
    box("洞口_暗腔", bx, by, z0 + h * 0.3, sx * 0.4, sy * 0.5, h * 0.6, g)
    for i in range(4):
        cone("口前落石%d" % (i + 1), bx - sx * 0.3 + i * sx * 0.2, by - sy * 0.55,
             z0 - 0.2, 0.8, 1.2, g, seg=5)
    return 7


def _tunnel_cuts(S, b, along_x: bool, fixed: float, t: float) -> list[tuple[float, float, float]]:
    """穿过这面墙的坑道：(开口起, 开口止, 坑道净高)，Blender 帧、沿墙轴。坑道得垂直于墙才算穿墙（顺着墙走的不开洞）。"""
    out = []
    for o in S.blocks:
        if o is b or o["kind"] != "tunnel":
            continue
        L, Wd, r = _along(float(o["size"][0]), float(o["size"][1]), float(o.get("rot", 0)))
        ox, oy = S.P(*o["xy"])
        runs_y = round(r) % 180 == 90
        if runs_y == along_x:        # 墙沿 X（南北墙）要南北走的坑道；墙沿 Y（东西墙）要东西走的
            hx, hy = (Wd / 2.0, L / 2.0) if runs_y else (L / 2.0, Wd / 2.0)
            lo_n, hi_n, c, half = (oy - hy, oy + hy, ox, hx) if along_x else (ox - hx, ox + hx, oy, hy)
            if lo_n - 0.05 <= fixed + t / 2.0 and hi_n + 0.05 >= fixed - t / 2.0:
                out.append((c - half, c + half, float(o["h_m"])))
    return sorted(out)


def _wall(name, along_x, fixed, lo, hi, t, z0, h, cuts, g):
    """一面墙，按 cuts 开洞；洞口上方留过梁（坑道比洞室矮时）。"""
    edges, k = lo, 0
    for c0, c1, ch in cuts + [(hi, hi, h)]:
        c0, c1 = max(lo, c0), min(hi, c1)
        for a0, a1, zb, zh in ((edges, c0, z0, h), (c0, c1, z0 + min(ch, h), h - min(ch, h))):
            if a1 - a0 > 0.05 and zh > 0.05:
                k += 1
                m = (a0 + a1) / 2.0
                box("%s%s" % (name, "" if k == 1 else k), m if along_x else fixed, fixed if along_x else m,
                    zb + zh / 2.0, (a1 - a0) if along_x else t, t if along_x else (a1 - a0), zh, g)
        edges = max(edges, c1)


def k_chamber(S, b, g):
    """室内洞室：地坪 + 四壁 + 顶板的壳体。用于 `interior = true` 的场景。
    垂直穿过某面墙的 tunnel 块在那面墙上开同宽的洞（2026-09-27：原先四壁封死，矿洞的主巷与支巷都撞在岔口墙上）。"""
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    t = 1.2
    box(b["name"] + "_顶", bx, by, z0 + h + t / 2.0, sx + 2 * t, sy + 2 * t, t, g)
    for sgn in (-1, 1):
        fx = bx + sgn * (sx + t) / 2.0
        _wall(b["name"] + "_壁" + ("西" if sgn < 0 else "东"), False, fx, by - (sy + 2 * t) / 2.0,
              by + (sy + 2 * t) / 2.0, t, z0, h, _tunnel_cuts(S, b, False, fx, t), g)
        fy = by + sgn * (sy + t) / 2.0
        _wall(b["name"] + "_壁" + ("南" if sgn < 0 else "北"), True, fy, bx - sx / 2.0, bx + sx / 2.0,
              t, z0, h, _tunnel_cuts(S, b, True, fy, t), g)
    for i in range(int(b.get("pillars", 0))):
        cyl(b["name"] + "_石柱%d" % (i + 1),
            bx - sx * 0.25 + i * sx * 0.5 / max(1, int(b.get("pillars", 1)) - 1 or 1),
            by, z0, 0.9, h, g, seg=7, r_top=1.2)
    return 5


def k_tunnel(S, b, g):
    """室内坑道：一段带顶的走廊。`rot` 决定走向，`h_m` 是净高。"""
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    sx, sy, rot = _along(sx, sy, float(b.get("rot", 0)))
    t = 1.0
    box(b["name"] + "_顶", bx, by, z0 + h + t / 2.0, sx, sy + 2 * t, t, g, rot)
    rr = math.radians(rot)
    for sgn in (-1, 1):
        px = bx - sgn * (sy + t) / 2.0 * math.sin(rr)
        py = by + sgn * (sy + t) / 2.0 * math.cos(rr)
        box(b["name"] + "_壁%d" % (1 if sgn < 0 else 2), px, py, z0 + h / 2.0,
            sx, t, h, g, rot)
    k = max(1, int(sx // 4.0))
    for i in range(k):           # 支撑木框
        d = -sx / 2.0 + sx * (i + 0.5) / k
        px, py = bx + d * math.cos(rr), by + d * math.sin(rr)
        box(b["name"] + "_框%d" % (i + 1), px, py, z0 + h - 0.2, 0.3, sy, 0.35, g, rot)
    return 2 + k


def k_ore_vein(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    k = int(b.get("count", 4))
    for i in range(k):
        cone("矿脉结核%d" % (i + 1), bx - sx * 0.3 + i * sx * 0.6 / max(1, k - 1),
             by, z0 + h * 0.4, 0.55, 0.8, g, seg=6)
    box("矿脉_面", bx, by, z0 + h / 2.0, sx, 0.4, h, g)
    return k + 1


def k_pool(S, b, g):
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    box(b["name"] + "_水面", bx, by, z0 + 0.15, sx, sy, 0.1, g)
    for i in range(6):
        a = 2 * math.pi * i / 6
        cone(b["name"] + "_岸石%d" % (i + 1), bx + math.cos(a) * sx * 0.48,
             by + math.sin(a) * sy * 0.48, z0 - 0.2, 0.7, 0.9, g, seg=5)
    return 7


# ── asset：本剧 props/ 里的单物体 Rodin 网格（follow-up 007 / 013，`tools/gen_bg_assets.py` 出的） ──
# 块写 `kind = "asset"` + `asset = "p{N}"`；`count > 1` 的块（橡树林 / 帐篷群）在占地里确定性散布同一件物件。
# 网格进来先归一：拆父级、合并、剥材质（rule 4h §D1）、底面中心落原点、正面朝南（−Y）——
# 与 face_frame 的角度约定一致，于是 `face` / `rot` 对物件块与脚本块是同一个意思。
_ASSET_PROTO = {}


def _prop_dir(S, key):
    """p{N} → props/p{N}_{名}/。场景只引用，不自带资产库（follow-up 013）；目录定位只在 props_lib 一处。"""
    from tools import props_lib
    d = props_lib.find(S.dir, key)
    if d is None or not (d / "asset.toml").is_file():
        raise SystemExit("[%s] 物件 %s 在 %s 下没有（带 asset.toml 的）目录" % (S.bg, key, props_lib.props_root(S.dir)))
    return str(d)


def _asset_proto(S, key):
    if key in _ASSET_PROTO:
        return _ASSET_PROTO[key]
    d = _prop_dir(S, key)
    glb = os.path.join(d, "mesh", key + ".glb")
    with open(os.path.join(d, "asset.toml"), "rb") as f:
        spec = tomllib.load(f)["asset"]
    if not os.path.isfile(glb):
        # Rodin 额度是瓶颈（2026-09-24 实测 0.5 credit / 件，余额只够约 300 件）：没出模的资产先用
        # 块尺寸的方盒占位，blend 照样能建、机位照样能对；名字带「待出模」，构建日志逐件报出来。
        # 补了 GLB 重跑本引擎即替换，不必改 toml。
        print("[%s] ⚠ 资产 %s 还没有 GLB，用方盒占位（python tools/gen_bg_assets.py mesh %s）" % (S.bg, key, d))
        _ASSET_PROTO[key] = (None, (1.0, 1.0, 1.0), spec)
        return _ASSET_PROTO[key]

    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=glb)
    new = [o for o in bpy.data.objects if o not in before]
    meshes = [o for o in new if o.type == "MESH"]
    if not meshes:
        raise SystemExit("[%s] %s 的 GLB 里没有网格" % (S.bg, key))
    bpy.ops.object.select_all(action="DESELECT")
    for o in meshes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    if len(meshes) > 1:
        bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    me = obj.data
    me.materials.clear()
    xs = [v.co.x for v in me.vertices]
    ys = [v.co.y for v in me.vertices]
    zs = [v.co.z for v in me.vertices]
    me.transform(Matrix.Translation((-(min(xs) + max(xs)) / 2.0, -(min(ys) + max(ys)) / 2.0, -min(zs))))
    # Rodin 有时把细长物体躺着出（实测 bg172-a32 灰石圆柱：size_m 1×1×9，网格却横卧）——
    # size_m 是权威：两边的最长轴都明确（≥1.5 倍次长轴）却对不上时，把网格转 90° 让最长轴落到 size_m 的最长轴上。
    want = [float(v) for v in spec["size_m"]]
    have = [max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)]

    def _long(v):
        o = sorted(range(3), key=lambda i: -v[i])
        return o[0] if v[o[0]] >= 1.5 * max(v[o[1]], 1e-6) else None

    wl, hl = _long(want), _long(have)
    if wl is not None and hl is not None and wl != hl:
        axis = "XYZ"[3 - wl - hl]           # 绕剩下那根轴转 90°，把 hl 轴换到 wl 轴
        me.transform(Matrix.Rotation(math.pi / 2.0, 4, axis))
        print("[%s] ⚠ 资产 %s 网格最长轴 %s ≠ size_m 最长轴 %s，已转 90° 立正" % (S.bg, key, "XYZ"[hl], "XYZ"[wl]))
        xs, ys, zs = ([v.co[i] for v in me.vertices] for i in range(3))
        me.transform(Matrix.Translation((-(min(xs) + max(xs)) / 2.0, -(min(ys) + max(ys)) / 2.0, -min(zs))))
        xs, ys, zs = ([v.co[i] for v in me.vertices] for i in range(3))
    yaw = math.radians(float(spec.get("yaw_deg", 0.0)))
    if yaw:
        me.transform(Matrix.Rotation(yaw, 4, "Z"))
        xs = [v.co.x for v in me.vertices]
        ys = [v.co.y for v in me.vertices]
    dims = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
    me.name = key
    me.use_fake_user = True
    for o in new:
        bpy.data.objects.remove(o, do_unlink=True)
    _ASSET_PROTO[key] = (me, dims, spec)
    return _ASSET_PROTO[key]


def _golden(i):
    return (i * 0.6180339887) % 1.0


def k_parts(S, b, g):
    """一个块里的几样东西（长桌 + 两条长凳、一摞木箱 + 几只木桶）：每样一个单物体 GLB，按各自 size_m 摆。

    `parts = [{asset = "{key}", at = [x, y], yaw = 0}, …]`——`at` 是块自身坐标（米；正面朝南时 x 向东、y 向北），
    随块的 face / rot 一起转；`yaw` 是该件相对块的附加转角（度）。GLB 的比例不作数，size_m 才是权威（同单件逐轴缩放）。
    """
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    ang = face_frame(b, sx, sy)[4] + float(b.get("rot", 0))
    c, sn = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    n = 0
    for i, p in enumerate(b["parts"]):
        me, (dx, dy, dz), spec = _asset_proto(S, p["asset"])
        ew, ed, eh = (float(v) for v in spec["size_m"])
        lx, ly = (float(v) for v in p.get("at", (0.0, 0.0)))
        px, py = bx + lx * c - ly * sn, by + lx * sn + ly * c
        pz = S.z(gx + lx * c - ly * sn, gy - (lx * sn + ly * c))
        a = ang + float(p.get("yaw", 0.0))
        name = "%s·%d·%s" % (b["name"], i + 1, spec.get("name_zh", p["asset"]))
        if me is None:
            box(name + "·待出模", px, py, pz + eh / 2.0, ew, ed, eh, g, rot=a)
        else:
            o = bpy.data.objects.new(name, me)
            o.location = (px, py, pz)
            o.rotation_euler = (0.0, 0.0, math.radians(a))
            o.scale = (ew / max(dx, 1e-3), ed / max(dy, 1e-3), eh / max(dz, 1e-3))
            g.objects.link(o)
        n += 1
    return n


def k_asset(S, b, g):
    if b.get("parts"):
        return k_parts(S, b, g)
    if "asset" not in b:
        raise SystemExit("「%s」写了 kind = \"asset\" 却没写 asset = \"{key}\"（或 parts = [...]）" % b["name"])
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    me, (dx, dy, dz), spec = _asset_proto(S, b["asset"])
    if me is None:
        box("%s·待出模" % b["name"], bx, by, z0 + max(h, 0.5) / 2.0, sx, sy, max(h, 0.5), g,
            rot=float(b.get("rot", 0)))
        return 1
    ang = face_frame(b, sx, sy)[4] + float(b.get("rot", 0))
    n = int(b.get("count", 1))
    if n <= 1:
        # 单件：逐轴撑满块的占地与 h_m。占地与高度来自坐标表 / 原典，是权威；Rodin 网格自己的比例不是
        # （实测 bg172-a01：41×17 m 的两层旅店出成 1:2.5 的瘦高楼，等比缩放会把它变成 40 m 高塔）。
        # 正面朝东 / 西时物体的「宽」沿南北，占地两轴对调。
        a90 = ang % 180.0
        w_t, d_t = (sy, sx) if 45.0 < a90 < 135.0 else (sx, sy)
        s = (w_t / max(dx, 1e-3), d_t / max(dy, 1e-3), (h if h > 0 else min(sx, sy)) / max(dz, 1e-3))
        print("[%s] %s ← %s 逐轴缩放 %.2f / %.2f / %.2f" % (S.bg, b["name"], b["asset"], s[0], s[1], s[2]))
        placements = [(bx, by, z0, ang, s)]
    else:
        ew, ed, eh = (float(v) for v in spec["size_m"])
        s = min(ew / max(dx, 1e-3), ed / max(dy, 1e-3), eh / max(dz, 1e-3))
        c, sn = math.cos(math.radians(float(b.get("rot", 0)))), math.sin(math.radians(float(b.get("rot", 0))))
        placements = []
        if b.get("layout") == "row":
            # 一排等距（柱列 / 栅柱 / 成排长凳）：沿块的长轴均分，不抖位置、不抖角度、不抖大小
            along_x = sx >= sy
            for i in range(n):
                t = (i + 0.5) / n - 0.5
                lx, ly = (t * sx, 0.0) if along_x else (0.0, t * sy)
                px, py = bx + lx * c - ly * sn, by + lx * sn + ly * c
                placements.append((px, py, S.z(gx + lx * c - ly * sn, gy - (lx * sn + ly * c)), ang, (s, s, s)))
        for i in range(0 if placements else n):
            u, v = _golden(i + 1) - 0.5, (i + 0.5) / n - 0.5
            lx, ly = u * sx * 0.85, v * sy * 0.85
            px, py = bx + lx * c - ly * sn, by + lx * sn + ly * c
            gxw, gyw = gx + lx * c - ly * sn, gy - (lx * sn + ly * c)
            k = s * (0.85 + 0.3 * _golden(i + 7))
            if h > 0:                  # 平面图的 h_m 是权威上限（bg3 碎石坡写 1.4 m，按资产卡出成 2.3 m 的巨石，把洞口整个堵死）
                k = min(k, h / max(dz, 1e-3))
            placements.append((px, py, S.z(gxw, gyw), ang + (i * 137.5) % 360.0, (k, k, k)))
    for i, (px, py, pz, a, sc) in enumerate(placements):
        o = bpy.data.objects.new("%s%s" % (b["name"], ("·%d" % (i + 1)) if n > 1 else ""), me)
        o.location = (px, py, pz)
        o.rotation_euler = (0.0, 0.0, math.radians(a))
        o.scale = sc
        g.objects.link(o)
    return len(placements)


def k_proxy(S, b, g):
    """通用方盒：资产规划还没给判定的块先占住位置与高度（apply_asset_plan.py 写入，报告里逐条列出）。"""
    gx, gy, sx, sy, bx, by, z0, h = _xy(S, b)
    box(b["name"] + "·占位", bx, by, z0 + max(h, 0.5) / 2.0, sx, sy, max(h, 0.5), g, rot=float(b.get("rot", 0)))
    return 1


KINDS = {
    "asset": k_asset, "proxy": k_proxy,
    "hall": k_hall, "abbey_hall": k_abbey_hall, "entrance_wing": k_entrance_wing,
    "low_wall": k_low_wall, "hall_shell": k_hall_shell, "altar": k_altar,
    "stair": k_stair, "shelves": k_shelves, "tables": k_tables, "yard": k_yard,
    "post": k_post, "rock_shelf": k_rock_shelf,
    "wing": k_wing, "lawn": k_lawn, "plaza": k_plaza, "graveyard": k_graveyard,
    "crypt": k_crypt, "stalls": k_stalls, "stable": k_stable,
    "kobold_camp": k_kobold_camp, "mine_portal": k_mine_portal, "vineyard": k_vineyard,
    "hut_camp": k_hut_camp, "gate_wall": k_gate_wall, "arch_bridge": k_arch_bridge,
    "guard_post": k_guard_post, "tower": k_tower, "palisade": k_palisade,
    "barracks": k_barracks, "training_yard": k_training_yard, "well": k_well,
    "crates": k_crates, "boulders": k_boulders, "tree_cluster": k_tree_cluster,
    "campfire": k_campfire, "tent_cluster": k_tent_cluster, "cave_mouth": k_cave_mouth,
    "chamber": k_chamber, "tunnel": k_tunnel, "ore_vein": k_ore_vein, "pool": k_pool,
}


# ── 布局闸门 ──────────────────────────────────────────────────────────
def footprint(b):
    """块的平面外廓采样点：四角 + 四边中点 + 中心，**按 rot 旋转过**。

    不吃 rot 的版本会把一段 `rot = 90` 的 18 m 长矮墙当成 18 m 宽 × 0.6 m 深的横条，
    于是「扎进山脊 / 块压块」两条闸门在所有旋转过的墙上都报错位的结论。
    """
    gx, gy = b["xy"]
    sx, sy = b["size"]
    rot = math.radians(float(b.get("rot", 0)))
    c, sn = math.cos(rot), math.sin(rot)
    return [(gx + dx * c - dy * sn, gy + dx * sn + dy * c)
            for dx in (-sx / 2.0, 0.0, sx / 2.0) for dy in (-sy / 2.0, 0.0, sy / 2.0)]


def aabb(b):
    """旋转后的轴对齐包围盒，闸门的块压块判定用它。"""
    pts = footprint(b)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def gate_geometry(S):
    """**不合格直接 raise，blend 根本生成不出来。**

    四类错误，每一类都在本仓库踩过：
      ① 未登记的 `kind` —— 往 toml 加一块而不说怎么建。
      ② 块扎进山脊 —— 加瑞克的小屋曾坐在东侧山脊里，商贩区曾陷进西侧山脊 12 m。
         真要嵌进山体的（矿洞口 / 倚崖而建的关墙）必须写 `into_ridge = true` **显式声明**。
      ③ 块压块 —— 修道院那一簇五个盒子曾互相重叠。
      ④ 块坐在河道上 —— 桥除外（`over_water = true`）。
    留给出片前的 reviewer 抓，等于每次改布局都要重看一遍图；放在这里，一次都不用。
    """
    errs = []
    for b in S.blocks:
        if b["kind"] not in KINDS:
            errs.append("「%s」的 kind=%s 未登记。已有：%s"
                        % (b["name"], b["kind"], " / ".join(sorted(KINDS))))
        gx, gy = b["xy"]
        sx, sy = b["size"]
        if not (0 <= gx <= S.W and 0 <= gy <= S.H):
            errs.append("「%s」的 xy (%g, %g) 超出场地 %g × %g" % (b["name"], gx, gy, S.W, S.H))

    for b in S.blocks:
        if b.get("into_ridge"):
            continue
        hit = next((p for p in footprint(b)
                    for poly, _h in S.ridges if poly_inside(p, poly)), None)
        if hit:
            errs.append("「%s」的外廓点 (%g, %g) 落在山脊里。要么挪回谷内，"
                        "要么写 into_ridge = true 说明它是嵌进山体的" % (b["name"], hit[0], hit[1]))

    for i, a in enumerate(S.blocks):
        for b in S.blocks[i + 1:]:
            if a.get("may_overlap") or b.get("may_overlap"):
                continue
            ax0, ay0, ax1, ay1 = aabb(a)
            bx0, by0, bx1, by1 = aabb(b)
            ox = min(ax1, bx1) - max(ax0, bx0)
            oy = min(ay1, by1) - max(ay0, by0)
            if ox > 0.05 and oy > 0.05:
                errs.append("「%s」与「%s」平面重叠 %.1f × %.1f m"
                            % (a["name"], b["name"], ox, oy))

    for b in S.blocks:
        if b.get("over_water"):
            continue
        for path, w, _d in S.waters:
            if any(dist_to_path(p, path) < w / 2.0 for p in footprint(b)):
                errs.append("「%s」坐在河道上。桥要写 over_water = true" % b["name"])
                break

    if not S.anchors:
        errs.append("没有 [[anchor]]：每个 plate 都该有一个校验机位，否则这份 blend 没法对账")

    # ⑤ 机位埋在块里 —— bg22-1「丘脚全景」的眼位落在北侧密林的体块内部，
    #    渲出来是一整幅树冠底面，而渲之前完全看不出来。室内机位（堂内 / 坑道 / 屋内）
    #    是合法的，但必须在 anchor 上写 `inside = true` 显式声明。
    for a in S.anchors:
        if a.get("inside"):
            continue
        for b in S.blocks:
            if b["kind"] in ("lawn", "plaza", "yard", "graveyard", "vineyard"):
                continue        # 贴地的地坪类，站在上面本来就对
            x0, y0, x1, y1 = aabb(b)
            ex, ey = a["eye"]
            if x0 < ex < x1 and y0 < ey < y1:
                errs.append("机位「%s」的眼位 (%g, %g) 落在「%s」体块内部。"
                            "室内机位要在 anchor 上写 inside = true 声明"
                            % (a["key"], ex, ey, b["name"]))
                break

    if errs:
        raise SystemExit("[%s] 布局闸门 %d 条，未生成 blend：\n  - %s"
                         % (S.bg, len(errs), "\n  - ".join(errs)))


def build_room(S, root):
    """`interior = true`：场地边界就是这间屋——四壁 + 顶板由引擎建，室内机位才拍得到墙。

    编号块只写屋里的东西；屋子本身不是一个块（写成块会盖满整张平面图）。块写 `opening = true`
    （门 / 拱门 / 通道口）且贴着某面墙（外廓离边界 ≤ 1.5 m）时，那面墙在它的宽度上留洞、洞顶压门楣。
    墙高取 `[meta] wall_h_m`，缺省为最高的块再高 1 m。墙立在边界**外侧**，不侵占场地。
    """
    if not S.interior:
        return 0
    g = coll("厅体", root)
    t = WALL_T
    H = float(S.meta.get("wall_h_m", max([float(b["h_m"]) for b in S.blocks] + [FLOOR]) + 1.0))
    n = 0
    for tag, axis, c, out in (("北", "x", 0.0, -1), ("南", "x", S.H, 1), ("西", "y", 0.0, -1), ("东", "y", S.W, 1)):
        L = S.W if axis == "x" else S.H
        holes = []
        for b in S.blocks:
            if not b.get("opening"):
                continue
            x0, y0, x1, y1 = aabb(b)
            lo, hi, a, z = (y0, y1, (x0, x1), float(b["h_m"])) if axis == "x" else (x0, x1, (y0, y1), float(b["h_m"]))
            if min(abs(lo - c), abs(hi - c)) <= 1.5:
                holes.append((max(0.0, a[0]), min(L, a[1]), min(H, max(z, DOOR_H))))
        holes.sort()
        segs, cur = [], 0.0
        for a0, a1, _ in holes:
            if a0 > cur:
                segs.append((cur, a0))
            cur = max(cur, a1)
        if cur < L:
            segs.append((cur, L))

        def place(name, a0, a1, z0, z1):
            if axis == "x":         # 南北墙在转角处各伸出一个墙厚，把东西墙的端头包住
                a0, a1 = (a0 - t if a0 == 0.0 else a0), (a1 + t if a1 == L else a1)
            mid, ln = (a0 + a1) / 2.0, a1 - a0
            if axis == "x":
                px, py = S.P(mid, c + out * t / 2.0)
                box(name, px, py, (z0 + z1) / 2.0, ln, t, z1 - z0, g)
            else:
                px, py = S.P(c + out * t / 2.0, mid)
                box(name, px, py, (z0 + z1) / 2.0, t, ln, z1 - z0, g)

        for i, (a0, a1) in enumerate(segs):
            place("厅体_%s墙%d" % (tag, i + 1), a0, a1, 0.0, H)
            n += 1
        for i, (a0, a1, top) in enumerate(holes):
            if top < H:
                place("厅体_%s门楣%d" % (tag, i + 1), a0, a1, top, H)
                n += 1
    box("厅体_顶板", 0.0, 0.0, H + t / 2.0, S.W + 2 * t, S.H + 2 * t, t, g)
    return n + 1


def build_blocks(S, root):
    g = coll("建筑组", root)
    return sum(KINDS[b["kind"]](S, b, g) for b in S.blocks)


# ── 图 + prompt 汇总进 blend ─────────────────────────────────────────
def _aim(cam, eye, target):
    cam.location = eye
    dx, dy, dz = (target[i] - eye[i] for i in range(3))
    flat = math.hypot(dx, dy)
    # 两个踩过的坑：
    # ① 正下方俯视时 dx=dy=0，atan2(0,0)=0，再加 90° 会把整幅俯视图转 90°。
    # ② 偏航角是**减** 90° 不是加：Blender 相机在 rot=(90°,0,0) 时朝 +Y（北），
    #    而朝北的 atan2(dy,dx) ＝ +90°，所以必须减回去。加号会让每个机位掉头看反向。
    yaw = (math.atan2(dy, dx) - math.pi / 2.0) if flat > 1e-6 else 0.0
    cam.rotation_euler = (math.atan2(flat, -dz), 0.0, yaw)


def _anchor_pose(S, a):
    ex, ey = S.P(*a["eye"])
    tx, ty = S.P(*a["target"])
    return ((ex, ey, S.z(*a["eye"]) + float(a.get("eye_h", 1.65))),
            (tx, ty, S.z(*a["target"]) + float(a.get("target_h", 2.0))))


def _prompt_block(md, first_line):
    """卡里首行 ＝ first_line 的 ```text 块；资产卡的三视图块首行是 `{key}-1_正面` 这种，按前缀匹配。"""
    try:
        with open(md, encoding="utf-8") as f:
            t = f.read()
    except OSError:
        return []
    return re.findall(r"```text\n(" + re.escape(first_line) + r"[^\n]*\n.*?)\n```", t, re.S)


def _used_assets(S):
    keys = set()
    for b in S.blocks:
        if b.get("kind") == "asset":
            keys |= {p["asset"] for p in b.get("parts", [])} | ({b["asset"]} if b.get("asset") else set())
    return sorted(keys)


def _image_empty(name, path, loc, size, parent, rot=(math.pi / 2.0, 0.0, 0.0)):
    e = bpy.data.objects.new(name, None)
    e.empty_display_type = "IMAGE"
    e.data = bpy.data.images.load(path, check_existing=True)
    e.empty_display_size = size
    e.location = loc
    e.rotation_euler = rot
    parent.objects.link(e)
    return e


def add_refs(S, root):
    """场景图 / plate 图挂到同名机位相机的背景；图本身再立成图片 empty（只在视口里看得见，不进渲染）；
    全部 prompt 进文本块。返回 (相机数, 挂了背景图的相机数, 文本块数, 图片数)。"""
    base = os.path.basename(S.dir)
    images = {base: S.image}
    for p in S.plates:
        png = os.path.join(S.dir, p, p + ".png")
        if os.path.isfile(png):
            images[p] = png
    nt = 0
    for name, md in [(base, S.card)] + [(p, os.path.join(S.dir, p, p + ".md")) for p in S.plates]:
        blocks = _prompt_block(md, name)
        if blocks:
            bpy.data.texts.new(name + ".prompt").write(blocks[0])
            nt += 1
    shelf = coll("参考图", root)
    span = max(S.W, S.H)
    for i, key in enumerate(_used_assets(S)):
        d = _prop_dir(S, key)
        blocks = _prompt_block(os.path.join(d, os.path.basename(d) + ".md"), key + "-")
        if blocks:
            bpy.data.texts.new(key + ".prompt").write("\n\n".join(blocks))
            nt += 1
        views = sorted(x for x in os.listdir(d) if re.match(re.escape(key) + r"-[123]_.*\.png$", x))
        for j, v in enumerate(views):   # 资产三视图排在场地南缘外一行：每件一列，正 / 侧 / 背自下而上
            _image_empty(v[:-4], os.path.join(d, v), (-span / 2.0 + i * 4.0, -S.H / 2.0 - 6.0, 1.5 + j * 3.2), 3.0, shelf)
    for j, (name, path) in enumerate(sorted(images.items())):   # 场景图与 plate 图立在场地北缘外一排
        _image_empty(name, path, (-span / 2.0 + j * 18.0, S.H / 2.0 + 8.0, 6.0), 16.0, shelf)
    cams = coll("机位", root)
    nbg = 0
    for a in S.anchors:
        cd = bpy.data.cameras.new(a["key"])
        cd.lens = float(a.get("lens_mm", 35))
        cd.clip_start, cd.clip_end = 0.05, max(1200.0, span * 4.0)
        cam = bpy.data.objects.new(a["key"], cd)
        cams.objects.link(cam)
        _aim(cam, *_anchor_pose(S, a))
        img = a.get("image") or (a["key"] if a["key"] in images else None)
        path = images.get(img) or (os.path.join(S.dir, img) if img else None)
        if path and os.path.isfile(path):
            cd.show_background_images = True
            bgi = cd.background_images.new()
            bgi.image = bpy.data.images.load(path, check_existing=True)
            bgi.alpha = 0.5
            bgi.frame_method = "FIT"
            nbg += 1
    return len(S.anchors), nbg, nt, len(images)


# ── 校验渲图 ─────────────────────────────────────────────────────────
def render_checks(S):
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.render.film_transparent = False
    try:
        sh = sc.display.shading
        sh.light, sh.show_shadows, sh.show_cavity = "STUDIO", True, True
    except Exception:
        pass
    span = max(S.W, S.H) * 1.05

    def shoot(fname, eye, target, lens=35.0, ortho=None):
        cd = bpy.data.cameras.new(fname)
        cd.clip_start, cd.clip_end = 0.05, max(1200.0, span * 4.0)
        cd.lens = lens
        cam = bpy.data.objects.new(fname, cd)
        sc.collection.objects.link(cam)
        _aim(cam, eye, target)
        if ortho:
            cd.type, cd.ortho_scale = "ORTHO", ortho
        sc.camera = cam
        sc.render.filepath = os.path.join(S.out, fname + ".png")
        bpy.ops.render.render(write_still=True)

    ar = S.W / S.H
    sc.render.resolution_x = int(1500 * min(1.0, ar))
    sc.render.resolution_y = int(1500 / max(1.0, ar))
    roof = [o for o in bpy.data.objects if o.name.startswith("厅体_顶")]
    for o in roof:                  # 室内的顶板会把俯视校验图整张盖住：只在这一张里藏起来
        o.hide_render = True
    shoot("check_plan", (0.0, 0.0, span * 2.0), (0.0, 0.0, 0.0), ortho=span)
    for o in roof:
        o.hide_render = False

    sc.render.resolution_x, sc.render.resolution_y = 1600, 900
    for a in S.anchors:
        shoot("check_" + a["key"], *_anchor_pose(S, a), lens=float(a.get("lens_mm", 35)))
    return len(S.anchors)


def build(scene_dir, render=True):
    S = Scene(scene_dir)
    if not os.path.isfile(S.image):
        raise SystemExit("[%s] 没有场景图 %s —— 图先行、3D 在后：先 python tools/gen_bg_images.py run %s"
                         % (S.bg, os.path.relpath(S.image, REPO), os.path.relpath(S.dir, REPO)))
    gate_geometry(S)
    os.makedirs(S.out, exist_ok=True)
    clear()
    root = coll(S.bg + "_" + S.name_zh)
    nv = build_terrain(S, root)
    nw = build_water(S, root)
    nr = build_roads(S, root)
    nb = build_blocks(S, root) + build_room(S, root)

    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    print("[%s] %s：物体 %d 个（地形 1 / %d 顶点，水 %d，路 %d，建筑构件 %d），场地 %g × %g m"
          % (S.bg, S.name_zh, len(objs), nv, nw, nr, nb, S.W, S.H))

    nc, nbg, nt, ni = add_refs(S, root)
    blend = os.path.join(S.out, S.bg + ".blend")
    bpy.context.preferences.filepaths.save_version = 0     # 不留 .blend1 备份：blend 随时可从 toml 重建
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    bpy.ops.file.make_paths_relative()      # 图按相对路径引用：blend 走 R2 换机器也找得到
    bpy.ops.wm.save_mainfile()
    stale = os.path.join(S.out, S.bg + ".glb")
    if os.path.isfile(stale):               # 场景级 GLB 已废止（GLB 只装单个物体）；旧产物顺手清掉
        os.remove(stale)
    print("[%s] 已存 %s：机位相机 %d（挂背景图 %d）· 图 %d · prompt 文本块 %d"
          % (S.bg, os.path.basename(blend), nc, nbg, ni, nt))
    if render:
        print("[%s] 校验图：check_plan.png + %d 张锚点透视" % (S.bg, render_checks(S)))
    return S


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    render = "--no-render" not in argv
    argv = [a for a in argv if a != "--no-render"]
    if not argv:
        raise SystemExit("用法：... --python tools/build_scene.py -- <scene 目录> [--no-render]\n"
                         "      ... --python tools/build_scene.py -- --all <scenes 根目录>")
    if argv[0] == "--all":
        root = argv[1] if len(argv) > 1 else os.path.join(REPO, "ai_videos")
        dirs = sorted(os.path.join(root, d) for d in os.listdir(root)
                      if os.path.isfile(os.path.join(root, d, "planning", "blocks.toml")))
        if not dirs:
            raise SystemExit("[%s] 下没有任何含 planning/blocks.toml 的 scene 目录" % root)
        ok, bad = [], []
        for d in dirs:
            try:
                build(d, render)
                ok.append(os.path.basename(d))
            except SystemExit as e:
                bad.append((os.path.basename(d), str(e)))
        print("\n[build_scene] 成功 %d：%s" % (len(ok), " ".join(ok)))
        for name, msg in bad:
            print("[build_scene] 失败 %s\n%s" % (name, msg))
        if bad:
            sys.exit(1)
    else:
        build(argv[0], render)


main()
