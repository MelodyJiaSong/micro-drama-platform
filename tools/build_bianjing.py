# -*- coding: utf-8 -*-
"""Build bianjing.blend (sk1 北宋汴京) from scratch — the previz geometry source.

The ONLY placement input is `scenes/bianjing/_blender/city_plan.md` §2 (three tables) plus
the camera paths in §3 (Place B entry) and §4 (Place A one-take TOML). Interface contract:
`scenes/bianjing/_blender/blender_build.md` §7. Rules: ai_video.md 4g (environment geometry)
and 4h (builder is the source; never hand-edit the blend).

Two layout layers (rule 4g ④ precision by camera proximity):
  G   global massing layer — whole-city walls / gates / moats / rivers / main streets and
      same-size block boxes at aerial precision. Input: `0_research/parts/w11_city_layout.md`
      (metre coordinate table). Stub until that input lands; whole-city coordinates are never
      invented here.
  A…  detailed Places from `city_plan.md` §2 (A 虹桥 / B 东水门 / C 州桥御街 / D 宣德楼 / E 汴河码头 /
      F 开封府 / H 相国寺 / I 桑家瓦子 / J 南薰门外; no G — that letter is the global layer); a new
      Place = a new `### Place X` table + its generators in SCRIPTS + an anchor (W11 place_anchor or
      DERIVED_ANCHORS, which only names W11 entries and never carries coordinates).

Every building row carries a plan index (方块号) and an asset key (`pN`); `resolve_asset`
maps pN → `props/pN_*/whitemodel/…blend` (+ `object.toml` front axis). Present → linked
collection instance; absent → same-bbox proxy prototype instanced into a `_PROXY` collection.
Re-running after a whitemodel lands swaps it in without touching layout code.
Geometry only: no materials, no lights.

Run (repo root):
  blender -b --factory-startup --python tools/build_bianjing.py -- [out.blend] [--place A|B|C]
  blender -b --factory-startup --python tools/build_bianjing.py -- [out.blend] --qc-only
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import math
import random
import re
import sys
import tomllib
import traceback
from dataclasses import dataclass, field
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
SK1 = REPO / "ai_videos" / "shikong_lvxing" / "sk1" / "2_世界观人设"
BLENDER_DIR = SK1 / "scenes" / "bianjing" / "_blender"
PLAN_MD = BLENDER_DIR / "city_plan.md"
DEFAULT_OUT = BLENDER_DIR / "bianjing.blend"
PROPS = SK1 / "props"

# ── §3 坐标契约（与 city_plan.md §1 / blender_build.md §3 逐值一致）────────────────
Z_WATER = 0.0
Z_STREET = 2.0              # 判断值：画中土坡高出水面约一人多（city_plan §1）
Z_BED = -1.5
Z_DECK_CROWN = 5.6          # ⚠️ bridge.004：拱顶净空 5.0 + 板厚 0.6，按画推算（doubt.004）
DECK_THICK = 0.6
BAY = 4.0                   # 面阔模数（p9 / p10 / 御廊）⚠️ 模数判断值（p9 卡 shop.*）
RIVER_W = 20.0              # ⚠️ 由桥长 21 推算（city_plan 方块 17，无 fact_id）
# Place 的世界锚点与旋转取 W11 [[place_anchor]]（FRAMES，由 load_w11 填；旧的 −400 / −900 压缩偏移已作废）
PLACE_RANGE: dict[str, tuple[float, float, float, float]] = {
    "A": (-75.0, 75.0, -35.0, 35.0), "B": (-50.0, 120.0, -45.0, 45.0), "C": (-48.0, 48.0, -80.0, 120.0),
    "D": (-82.0, 82.0, -80.0, 345.0), "E": (-60.0, 50.0, -40.0, 86.0), "F": (-110.0, 110.0, -150.0, 112.0),
    "H": (-130.0, 215.0, -155.0, 155.0), "I": (-105.0, 105.0, -80.0, 115.0), "J": (-150.0, 150.0, -400.0, 80.0)}

BRIDGE_HALF_W = 3.9         # ⚠️ bridge.004：桥面宽 7.8
BRIDGE_ARCH_HALF = 10.5     # 方块 1：坡道 y ±10.5…±18
BRIDGE_FOOT = 18.0
P8_ORIGIN_Z = Z_WATER       # 判断：p8 object.toml 高 6.5 ＝ 拱顶桥面 5.6 + 栏杆约 1，是从水面量起的

CORRIDOR_R_A = 2.5          # blender_build §4 步 5
CORRIDOR_DZ = 2.0
CORRIDOR_R_B = 2.0          # 判断：入城通道本身只有 4 m 宽（门洞 4、木桥宽 4），2.5 m 管径物理上穿不过；按通道半宽查
DOOR_CLEAR_MIN = 6.0        # blender_build §1 / §6 #4

# Place B（数值出自 city_plan 方块 20–27；⚠️ 城墙三值为 gate.004 ai_draft，只用于几何、不进 prompt）
# 2026-09-17（照 bg2 东水门锚点图量形制）：原值 底宽 34 / 顶宽 4（gate.004 ⚠️ ai_draft）在 8.7 m 高上是 1:1.7 的坡，
# 渲出来是一道能走上去的土坡、不是城墙；bg2 上墙面近乎直立、只带轻微收分（约 1:4），墙顶是一条可行走的平台。
# 数值来源由「ai_draft 的底宽」改为「锚点图量出的收分 + 可行走顶宽」，底宽随之缩到 16 m（divergence #27）。
WALL_BASE_W = 16.0
WALL_TOP_W = 12.0
WALL_H = 8.7
WATER_GATE_SPAN = 22.0
SLUICE_Z = (6.0, 8.0)       # blender_build §4 步 2：闸门薄板吊起态
GUAIZI_H = 5.0              # 判断值（方块 23）
GUAIZI_T = 3.0
TREE_B_X_TABLE = -8.0
TREE_B_X_BUILT = -(WALL_BASE_W / 2) - 3.0   # 判断：表里 x=−8 落在底宽 34 的墙体里（墙脚 x=−17），树线移到墙脚内 3 m

# Place C（方块 30–42）
ZQ_DECK_Z = 2.6             # ⚠️ zhouqiao.001/002：宽按明桥 30 m
STONE_WALL_H = 3.3          # ⚠️ ai_draft（zhouqiao.001/002），几何用
C_D_HALF = 46.0             # 御街两侧 ±46 m 以外 ＝ D 级不建

SHOT_LAYER_BLOCKS = {15, 16, 28, 43, 61, 77, 89, 99, 106, 117}
PLACES = ("A", "B", "C", "D", "E", "F", "H", "I", "J")


class PlanError(RuntimeError):
    pass


# ── 表解析（blender_build.md §7：解析失败直接 raise、不猜）────────────────────────
NUM = r"[-+]?\d+(?:\.\d+)?"
PM_NUM = r"±?[-+]?\d+(?:\.\d+)?"
MODEL_RE = re.compile(r"`(p10a|p10b|p10c|p10|p9|p8)`")
COORD_RE = re.compile(rf"\(\s*({PM_NUM})\s*,\s*({PM_NUM})\s*\)")
SIZE_RE = re.compile(rf"({NUM})\s*×\s*[^\d×，；（）|+]{{0,3}}?({NUM})(?:\s*×\s*[^\d×，；（）|+]{{0,3}}?({NUM}))?")
Z_RE = re.compile(rf"z=\+?({NUM})")
HEADER = ["方块", "要素", "主体 / 建法", "局部中心 · 朝向", "尺寸", "级", "依据", "⚠️"]
DOOR_YAW: dict[str, float] = {"门朝南": 0.0, "门朝北": 180.0, "门朝东": 90.0, "门朝西": -90.0}
SCRIPT_KEYS = ("河道", "土坡", "街", "城墙", "水门", "旱门", "拐子城", "护龙河", "木桥", "杈子",
               "御沟", "御廊", "阙楼", "望火楼", "井", "表木", "柳", "仓", "码头", "州桥", "石壁", "正店",
               "宫墙", "墩台", "门扇", "门楼", "朵楼", "阙亭", "金水河", "廊庑", "大殿", "刻漏楼",
               "仓门", "仓廒", "院墙", "府门", "内门", "廊房", "戒石", "正厅", "殿宇",
               "寺墙", "寺东门", "大三门", "资圣门", "东西廊", "栅栏", "布招杆", "大看棚", "看棚群",
               "大路", "横路", "田埂", "农舍")
ABSORBED: dict[str, str] = {"岸边桃李梨杏": "御沟"}


def norm(s: str) -> str:
    return s.replace("−", "-").replace("\\|", "|").replace("**", "").strip()


@dataclass(frozen=True)
class Row:
    place: str
    block: int
    index: int
    element: str
    method: str
    where: str
    size: str
    level: str
    warn: str
    kind: str                       # whitemodel | script | shot | placeholder
    model: str | None
    center: tuple[float, float] | None
    yaw: float | None               # 门朝向，0 ＝ 南（−Y）
    sizes: tuple[tuple[float, ...], ...]
    zs: tuple[float, ...]
    keys: tuple[str, ...]

    @property
    def text(self) -> str:
        return " ".join((self.element, self.method, self.where, self.size))

    def need(self, *snippets: str) -> None:
        for s in snippets:
            if s not in self.text:
                raise PlanError(f"方块 {self.block}：表里找不到「{s}」——表改了而脚本常量没跟上")


def expand_pm(v: str) -> list[float]:
    if v.startswith("±"):
        x = float(v[1:])
        return [x, -x]
    return [float(v)]


def dispatch_keys(element: str) -> tuple[str, ...]:
    e = re.sub(r"（[^）]*）|\([^)]*\)", "", element)
    e = re.sub(r"×\s*\d+\s*行?", "", e)
    keys: list[str] = []
    for part in (p.strip() for p in re.split(r"[+与]", e)):
        if not part:
            continue
        hits = [(part.rfind(k) + len(k), len(k), k) for k in SCRIPT_KEYS if k in part]
        if hits:
            keys.append(max(hits)[2])
        elif part in ABSORBED:
            if ABSORBED[part] not in keys:
                keys.append(ABSORBED[part])
        else:
            raise PlanError(f"要素「{element}」里的「{part}」没有对应的脚本生成器")
    if not keys:
        raise PlanError(f"要素「{element}」解析不出生成器")
    return tuple(dict.fromkeys(keys))


def parse_row(place: str, cells: list[str]) -> list[Row]:
    blocks = [int(b) for b in norm(cells[0]).split()]
    element, method, where, size, level, _src, warn = (norm(c) for c in cells[1:8])
    lm = re.fullmatch(r"(A|B|C|—)(?:（[^）]*）)?", level)
    if not lm:
        raise PlanError(f"方块 {blocks}：级「{level}」不是 A/B/C/—（可带括注）")
    level = lm.group(1)
    if "shot 层道具" in method:
        kind, model = "shot", None
    elif (m := MODEL_RE.search(method)):
        kind, model = "whitemodel", m.group(1)
    elif "留位" in method or "留位" in where:
        kind, model = "placeholder", None
    elif "脚本" in method:
        kind, model = "script", None
    else:
        raise PlanError(f"方块 {blocks}：主体 / 建法「{method}」认不出是白模 / 脚本 / 道具 / 留位")

    coords: list[tuple[float, float]] = []
    if kind != "shot":
        for mx, my in COORD_RE.findall(where):
            coords += list(itertools.product(expand_pm(mx), expand_pm(my)))
    if len(blocks) > 1 and len(coords) != len(blocks):
        raise PlanError(f"方块 {blocks}：{len(blocks)} 个方块号却有 {len(coords)} 个坐标")
    if kind in ("whitemodel", "placeholder") and not coords:
        raise PlanError(f"方块 {blocks}：白模 / 留位行没有 (x, y) 局部中心")

    door = [yaw for k, yaw in DOOR_YAW.items() if k in where]
    if len(door) > 1:
        raise PlanError(f"方块 {blocks}：朝向写了不止一个")
    if "绕 Z 转 180°" in method and door and door[0] != 180.0:
        raise PlanError(f"方块 {blocks}：「绕 Z 转 180°」与「{where}」矛盾")
    sizes = tuple(tuple(float(v) for v in g if v) for g in SIZE_RE.findall(size))
    zs = tuple(float(v) for v in Z_RE.findall(size))
    keys = dispatch_keys(element) if kind == "script" else ()

    rows: list[Row] = []
    for i, c in enumerate(coords or [None]):
        yaw: float | None = door[0] if door else None
        if "门朝街心" in where and c is not None:
            yaw = -90.0 if c[0] > 0 else 90.0           # 判断：「门朝街心」＝ 门朝 x=0
        if kind == "whitemodel" and yaw is None:
            if "桥尾＝北" in where:
                yaw = 180.0                                # 白模「前」＝ 桥尾，朝北
            elif "桥尾＝南" in where:
                yaw = 0.0
            else:
                raise PlanError(f"方块 {blocks}：白模行没有朝向")
        rows.append(Row(place, blocks[i] if len(blocks) > 1 else blocks[0], i, element, method,
                        where, size, level, warn, kind, model, c, yaw, sizes, zs, keys))
    return rows


def parse_plan(md: str) -> list[Row]:
    sec = md.split("## 2. 要素表", 1)
    if len(sec) != 2:
        raise PlanError("city_plan.md 缺「## 2. 要素表」")
    body = sec[1].split("\n## ", 1)[0]
    rows: list[Row] = []
    seen: set[str] = set()
    for chunk in re.split(r"\n(?=### Place )", body)[1:]:
        m = re.match(r"### Place ([A-Z])\b", chunk)
        if not m:
            raise PlanError("「### Place X」段头格式不对")
        place = m.group(1)
        seen.add(place)
        lines = [ln for ln in chunk.splitlines() if ln.startswith("|")]
        head = [norm(c).replace("\ufe0f", "") for c in re.split(r"(?<!\\)\|", lines[0])[1:-1]]
        if head != [h.replace("\ufe0f", "") for h in HEADER]:
            raise PlanError(f"Place {place} 表头不是固定八列：{head}")
        for ln in lines[2:]:
            cells = re.split(r"(?<!\\)\|", ln)[1:-1]
            if len(cells) != 8:
                raise PlanError(f"Place {place} 行列数 {len(cells)} ≠ 8：{ln[:40]}")
            rows += parse_row(place, cells)
    if seen != set(PLACES):
        raise PlanError(f"要素表只找到 Place {sorted(seen)}")
    return rows


def parse_one_take(md: str) -> list[Vector]:
    sec = md.split("## 4. 一镜到底路径", 1)
    m = re.search("```toml" + chr(10) + "(.*?)```", sec[1] if len(sec) == 2 else "", re.S)
    if not m:
        raise PlanError("city_plan.md §4 缺 toml 块")
    cfg = tomllib.loads(m.group(1))
    ox, oy, oz = cfg["全局"]["原点偏移"]
    return [Vector((p["位置"][0] + ox, p["位置"][1] + oy, p["位置"][2] + oz)) for p in cfg["机位路径"]]


def parse_entry_path(md: str, rows: list[Row]) -> list[Vector]:
    m = re.search(r"^入城镜路径[^\n]*$", md, re.M)
    if not m:
        raise PlanError("city_plan.md §3 缺「入城镜路径」")
    line = norm(m.group(0))
    hm = re.search(rf"机高 ({NUM})", line)
    if not hm:
        raise PlanError("入城镜路径缺「机高」")
    z = Z_STREET + float(hm.group(1))
    pts: list[tuple[float, float]] = []
    for tok in line.split("→"):
        c = COORD_RE.search(tok)
        if c:
            pts.append((float(c.group(1)), float(c.group(2))))
            continue
        b = re.search(r"(\d+)", tok)
        if not b:
            raise PlanError(f"入城镜路径段「{tok}」既无坐标也无方块号")
        cands = [r.center for r in rows if r.place == "B" and r.block == int(b.group(1)) and r.center]
        if not cands or not pts:
            raise PlanError(f"入城镜路径段「{tok}」找不到方块坐标")
        py = pts[-1][1]
        pts.append(min(cands, key=lambda c2: abs(c2[1] - py)))
    return [Vector((x, y, z)) for x, y in pts]


# ── 几何基元 ────────────────────────────────────────────────────────────────────
COLS: dict[str, bpy.types.Collection] = {}


def collection(name: str) -> bpy.types.Collection:
    c = COLS.get(name) or bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
    if c.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(c)
    COLS[name] = c
    return c


class Batch:
    """Accumulates many primitives into ONE mesh object (post arrays, tree rows)."""

    def __init__(self) -> None:
        self.bm = bmesh.new()

    def poly_solid(self, bottom: list[Vector], top: list[Vector]) -> None:
        vb = [self.bm.verts.new(v) for v in bottom]
        vt = [self.bm.verts.new(v) for v in top]
        n = len(vb)
        self.bm.faces.new(list(reversed(vb)))
        self.bm.faces.new(vt)
        for i in range(n):
            j = (i + 1) % n
            self.bm.faces.new((vb[i], vb[j], vt[j], vt[i]))

    def box(self, lo: tuple[float, float, float], hi: tuple[float, float, float]) -> None:
        (x0, y0, z0), (x1, y1, z1) = lo, hi
        ring = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        self.poly_solid([Vector((x, y, z0)) for x, y in ring], [Vector((x, y, z1)) for x, y in ring])

    def cbox(self, c: tuple[float, float, float], s: tuple[float, float, float]) -> None:
        self.box((c[0] - s[0] / 2, c[1] - s[1] / 2, c[2] - s[2] / 2),
                 (c[0] + s[0] / 2, c[1] + s[1] / 2, c[2] + s[2] / 2))

    def cyl(self, x: float, y: float, z0: float, z1: float, r: float, seg: int = 8) -> None:
        ring = [(x + r * math.cos(2 * math.pi * i / seg), y + r * math.sin(2 * math.pi * i / seg))
                for i in range(seg)]
        self.poly_solid([Vector((a, b, z0)) for a, b in ring], [Vector((a, b, z1)) for a, b in ring])

    def ball(self, c: tuple[float, float, float], r: float) -> None:
        g = bmesh.ops.create_icosphere(self.bm, subdivisions=1, radius=r)
        bmesh.ops.translate(self.bm, vec=Vector(c), verts=g["verts"])

    def prism_x(self, x0: float, x1: float, profile_yz: list[tuple[float, float]]) -> None:
        self.poly_solid([Vector((x0, y, z)) for y, z in profile_yz], [Vector((x1, y, z)) for y, z in profile_yz])

    def prism_y(self, y0: float, y1: float, profile_xz: list[tuple[float, float]]) -> None:
        self.poly_solid([Vector((x, y0, z)) for x, z in profile_xz], [Vector((x, y1, z)) for x, z in profile_xz])

    def gable_x(self, x0: float, x1: float, y0: float, y1: float, z_eave: float, z_ridge: float) -> None:
        """悬山两坡屋面，脊平行 X（平行街面）。"""
        self.prism_x(x0, x1, [(y0, z_eave), (y1, z_eave), ((y0 + y1) / 2, z_ridge)])

    def hip(self, cx: float, cy: float, lx: float, ly: float, z0: float, h: float) -> None:
        """歇山体块近似：脊沿长轴，脊长 ＝ 长边 − 短边。"""
        hr = abs(lx - ly) / 2
        if hr < 1e-6:
            vb = [self.bm.verts.new(v) for v in ((cx - lx / 2, cy - ly / 2, z0), (cx + lx / 2, cy - ly / 2, z0),
                                                 (cx + lx / 2, cy + ly / 2, z0), (cx - lx / 2, cy + ly / 2, z0))]
            apex = self.bm.verts.new((cx, cy, z0 + h))
            self.bm.faces.new(list(reversed(vb)))
            for i in range(4):
                self.bm.faces.new((vb[i], vb[(i + 1) % 4], apex))
            return
        vb = [self.bm.verts.new(v) for v in ((cx - lx / 2, cy - ly / 2, z0), (cx + lx / 2, cy - ly / 2, z0),
                                             (cx + lx / 2, cy + ly / 2, z0), (cx - lx / 2, cy + ly / 2, z0))]
        if lx >= ly:
            r0 = self.bm.verts.new((cx - hr, cy, z0 + h))
            r1 = self.bm.verts.new((cx + hr, cy, z0 + h))
            faces = [(vb[0], vb[1], r1, r0), (vb[1], vb[2], r1), (vb[2], vb[3], r0, r1), (vb[3], vb[0], r0)]
        else:
            r0 = self.bm.verts.new((cx, cy - hr, z0 + h))
            r1 = self.bm.verts.new((cx, cy + hr, z0 + h))
            faces = [(vb[0], vb[1], r0), (vb[1], vb[2], r1, r0), (vb[2], vb[3], r1), (vb[3], vb[0], r0, r1)]
        self.bm.faces.new(list(reversed(vb)))
        for f in faces:
            if len(set(f)) == len(f):
                self.bm.faces.new(f)

    def loft_y(self, stations: list[tuple[float, float, float]], x0: float, x1: float) -> None:
        """Solid band along Y: stations (y, z_bottom, z_top), rectangle section x0..x1."""
        rings = [[self.bm.verts.new((x0, y, zb)), self.bm.verts.new((x1, y, zb)),
                  self.bm.verts.new((x1, y, zt)), self.bm.verts.new((x0, y, zt))] for y, zb, zt in stations]
        for a, b in zip(rings, rings[1:]):
            for j in range(4):
                k = (j + 1) % 4
                self.bm.faces.new((a[j], a[k], b[k], b[j]))
        self.bm.faces.new(list(reversed(rings[0])))
        self.bm.faces.new(rings[-1])

    def finish(self, name: str, col: str | bpy.types.Collection, row: int = 0) -> bpy.types.Object:
        bmesh.ops.recalc_face_normals(self.bm, faces=self.bm.faces)
        me = bpy.data.meshes.new(name)
        self.bm.to_mesh(me)
        self.bm.free()
        ob = bpy.data.objects.new(name, me)
        ob["bj_row"] = row
        (collection(col) if isinstance(col, str) else col).objects.link(ob)
        return ob


def solid_box(name: str, col: str, lo: tuple[float, float, float], hi: tuple[float, float, float],
              row: int = 0) -> bpy.types.Object:
    b = Batch()
    b.box(lo, hi)
    return b.finish(name, col, row)


# ── 资产登记：方块行 pN → 白模文件或同尺寸替身（布局代码从不写文件路径）─────────────────
@dataclass(frozen=True)
class Asset:
    key: str
    card: Path
    whitemodel: Path
    spec: Path

    def spec_data(self) -> dict:
        return tomllib.loads(self.spec.read_text(encoding="utf-8")) if self.spec.is_file() else {}

    def front(self) -> Vector:
        axis = str(self.spec_data().get("几何", {}).get("目标朝向", {}).get("前", "+Y"))
        v = {"+X": (1, 0), "-X": (-1, 0), "+Y": (0, 1), "-Y": (0, -1)}.get(axis)
        if v is None:
            raise PlanError(f"{self.key}：object.toml 目标朝向.前「{axis}」不是水平轴")
        return Vector((v[0], v[1], 0.0))


def resolve_asset(key: str) -> Asset:
    m = re.fullmatch(r"p(\d+)([a-z]?)", key)
    if not m:
        raise PlanError(f"资产键「{key}」不是 pN / pNa")
    cards = sorted(PROPS.glob(f"p{m.group(1)}_*"))
    if len(cards) != 1:
        raise PlanError(f"资产 {key}：props/ 下 p{m.group(1)}_* 目录数 {len(cards)} ≠ 1")
    card = cards[0]
    wm = card / "whitemodel" / (f"{key}.blend" if m.group(2) else f"{card.name}.blend")
    return Asset(key, card, wm, card / "object.toml")


def deck_top(y: float) -> float:
    return Z_STREET + (Z_DECK_CROWN - Z_STREET) * 0.5 * (1 + math.cos(math.pi * max(-1.0, min(1.0, y / BRIDGE_FOOT))))


def proxy_p8(b: Batch) -> None:
    """拱形板带：拱身 |y|≤10.5 为 0.6 厚板带（拱下通透），坡道 10.5…18 实心落到水面；两侧 21 根栏柱。"""
    st: list[tuple[float, float, float]] = []
    for i in range(int(2 * BRIDGE_FOOT / 0.5) + 1):
        y = -BRIDGE_FOOT + 0.5 * i
        zt = deck_top(y)
        if abs(abs(y) - BRIDGE_ARCH_HALF) < 1e-6:
            pair = [(y, Z_WATER, zt), (y, zt - DECK_THICK, zt)]
            st += pair if y < 0 else pair[::-1]
        else:
            st.append((y, zt - DECK_THICK if abs(y) < BRIDGE_ARCH_HALF else Z_WATER, zt))
    b.loft_y(st, -BRIDGE_HALF_W, BRIDGE_HALF_W)
    for sx in (-1, 1):
        x = sx * (BRIDGE_HALF_W - 0.1)
        for i in range(21):
            y = -10.0 + i
            b.cbox((x, y, deck_top(y) + 0.55), (0.15, 0.15, 1.1))
        b.loft_y([(y, deck_top(y) + 1.0, deck_top(y) + 1.1) for y in (-10.5 + 0.5 * i for i in range(43))],
                 x - 0.06, x + 0.06)


def proxy_p9(b: Batch) -> None:
    """8 × 7.5 × 7.5，前 +Y。店身 4 × 6（二层檐 5.4 / 脊 7）、欢门骨架 5 宽 7.5 高在店前、席棚在观者右（−X）。"""
    b.box((-0.5, -3.75, 0.0), (3.5, 2.25, 5.4))
    b.gable_x(-0.5, 3.5, -3.75, 2.25, 5.4, 7.0)
    for x in (-0.9, 3.9):
        b.cbox((x, 3.65, 3.75), (0.2, 0.2, 7.5))
    for z in (2.6, 5.0, 7.4):
        b.cbox((1.5, 3.65, z), (5.0, 0.2, 0.2))
    for x in (-3.9, -0.6):
        for y in (-0.65, 2.15):
            b.cbox((x, y, 1.25), (0.1, 0.1, 2.5))
    b.box((-4.0, -0.75, 2.5), (-0.5, 2.25, 2.58))


def proxy_unit(b: Batch, x0: float, y_back: float, y_front: float, eave: float, ridge: float) -> None:
    b.box((x0, y_back, 0.0), (x0 + BAY, y_front, eave))
    b.gable_x(x0, x0 + BAY, y_back, y_front, eave, ridge)


def proxy_p10(b: Batch) -> None:
    """12 × 6.5 × 6.6，前 +Y。三栋低高低（檐/脊 2.7/4.3 · 5.0/6.6 · 2.7/4.3），披檐只在观者右栋（−X）。"""
    proxy_unit(b, 2.0, -3.25, 1.75, 2.7, 4.3)
    proxy_unit(b, -2.0, -3.25, 1.75, 5.0, 6.6)
    proxy_unit(b, -6.0, -3.25, 1.75, 2.7, 4.3)
    b.prism_x(-6.0, -2.0, [(1.75, 2.62), (3.25, 2.12), (3.25, 2.2), (1.75, 2.7)])
    for x in (-5.9, -2.1):
        b.cbox((x, 3.15, 1.06), (0.12, 0.12, 2.12))


def proxy_p10a(b: Batch) -> None:
    proxy_unit(b, -2.0, -2.5, 2.5, 2.7, 4.3)


PROXY_BUILDERS = {"p8": proxy_p8, "p9": proxy_p9, "p10": proxy_p10, "p10a": proxy_p10a}


@dataclass
class Proto:
    collection: bpy.types.Collection
    is_proxy: bool
    asset: Asset
    lo: Vector
    hi: Vector


PROTOS: dict[tuple[str, str], Proto] = {}


def proto_bounds(col: bpy.types.Collection) -> tuple[Vector, Vector]:
    pts = [ob.matrix_world @ Vector(c) for ob in col.all_objects if ob.type == "MESH" for c in ob.bound_box]
    return (Vector([min(p[i] for p in pts) for i in range(3)]), Vector([max(p[i] for p in pts) for i in range(3)]))


def get_proto(key: str, level: str) -> Proto:
    """A 级＝白模全部型面；B 级＝同一份 link 网格挂 decimate ≤ 5k 面；缺白模＝替身。"""
    asset = resolve_asset(key)
    real = asset.whitemodel.is_file()
    tier = ("B" if level == "B" else "A") if real else "PROXY"
    if (key, tier) in PROTOS:
        return PROTOS[(key, tier)]
    name = f"PROTO_{key}_{tier}"
    col = bpy.data.collections.get(name)
    if col is None and real:
        with bpy.data.libraries.load(str(asset.whitemodel), link=True) as (_src, dst):
            dst.objects = list(_src.objects)
        meshes = [o for o in dst.objects if o is not None and o.type == "MESH"]
        if not meshes:
            raise PlanError(f"{asset.whitemodel} 里没有 MESH")
        col = bpy.data.collections.new(name)
        for o in meshes:
            if tier == "A":
                col.objects.link(o)
                continue
            loc = bpy.data.objects.new(f"{o.name}_B", o.data)
            if len(o.data.polygons) > 5000:
                loc.modifiers.new("decimate_B", "DECIMATE").ratio = 5000.0 / len(o.data.polygons)
            col.objects.link(loc)
    elif col is None:
        b = Batch()
        if key in PROXY_BUILDERS:
            PROXY_BUILDERS[key](b)
        else:
            size = asset.spec_data().get("几何", {}).get("尺寸")
            if not size:
                raise PlanError(f"资产 {key}：无内置替身，object.toml 也没有 [几何].尺寸")
            b.box((-size[0] / 2, -size[1] / 2, 0.0), (size[0] / 2, size[1] / 2, size[2]))
        col = bpy.data.collections.new(name)
        b.finish(f"{key}_proxy_mesh", col)
    proto = Proto(col, not real, asset, *proto_bounds(col))
    PROTOS[(key, tier)] = proto
    return proto


def place_asset(row: Row, col_base: str, origin_z: float = Z_STREET, jitter: bool = False) -> bpy.types.Object:
    """方块行 → 集合实例。资产「前」转到行的朝向（0 ＝ 南）；原点落 origin_z。"""
    if row.center is None or row.model is None:
        raise PlanError(f"方块 {row.block}：摆白模缺坐标或资产键")
    proto = get_proto(row.model, row.level)
    d = Matrix.Rotation(math.radians(row.yaw or 0.0), 3, "Z") @ Vector((0.0, -1.0, 0.0))
    f = proto.asset.front()
    yaw = math.atan2(d.y, d.x) - math.atan2(f.y, f.x)
    s, mirror, drot = 1.0, False, 0.0
    if jitter:
        rng = random.Random(row.block * 1000 + row.index)
        mirror = rng.random() < 0.5
        drot = rng.uniform(-2.0, 2.0)
        s = rng.uniform(0.97, 1.03)
    ob = bpy.data.objects.new(f"{row.place}_{row.block:02d}_{row.index}_{row.model}", None)
    ob.instance_type = "COLLECTION"
    ob.instance_collection = proto.collection
    ob.location = (row.center[0], row.center[1], origin_z)
    ob.rotation_euler = (0.0, 0.0, yaw + math.radians(drot))
    ob.scale = (-s if mirror else s, s, s)
    ob["bj_row"] = row.block
    ob["bj_asset"] = row.model
    ob["bj_jitter"] = f"mirror={int(mirror)} drot={drot:+.2f}° scale={s:.4f}"
    front_half = proto.hi.dot(f) if f.x + f.y > 0 else proto.lo.dot(f)
    ob["bj_front_local"] = (f.x * front_half, f.y * front_half, 0.0)
    ob["bj_lo"] = tuple(proto.lo)
    ob["bj_hi"] = tuple(proto.hi)
    ob["bj_proxy"] = int(proto.is_proxy)
    collection(f"{row.place}_{col_base}{'_PROXY' if proto.is_proxy else ''}").objects.link(ob)
    return ob


# ── 布局层 ① 全城体块层（航拍精度）───────────────────────────────────────────────
# 城墙/城门/壕/河/主街 + 同尺寸盒子街区，每个盒子带方块号 → 资产键（box N → pN），
# 替身换白模不动布局代码（同 place_asset）。坐标只来自 w11 的米制坐标表，绝不自编。
W11_LAYOUT = SK1.parent / "0_research" / "parts" / "w11_city_layout.md"
NOTES: list[str] = []
Pt = tuple[float, float]


@dataclass(frozen=True)
class Frame:
    """Place 局部 → 世界：先绕 Z 转 rot_deg，再平移到 W11 锚点。"""
    x: float
    y: float
    rot_deg: float

    def world(self, lx: float, ly: float) -> Pt:
        c, s = math.cos(math.radians(self.rot_deg)), math.sin(math.radians(self.rot_deg))
        return (self.x + c * lx - s * ly, self.y + s * lx + c * ly)

    def local(self, wx: float, wy: float) -> Pt:
        c, s = math.cos(math.radians(self.rot_deg)), math.sin(math.radians(self.rot_deg))
        dx, dy = wx - self.x, wy - self.y
        return (c * dx + s * dy, -s * dx + c * dy)

    def matrix(self) -> Matrix:
        return Matrix.Translation((self.x, self.y, 0.0)) @ Matrix.Rotation(math.radians(self.rot_deg), 4, "Z")

    def local_v(self, v: Vector) -> Vector:
        lx, ly = self.local(v.x, v.y)
        return Vector((lx, ly, v.z))

    def world_v(self, v: tuple[float, float, float] | Vector) -> Vector:
        wx, wy = self.world(v[0], v[1])
        return Vector((wx, wy, v[2]))


FRAMES: dict[str, Frame] = {}
# 判断：开洞范围 ＝ Place 自己铺了地面的范围（A 房后 |y|>30 是 D 级、不铺地，由全城地面接管）
PLACE_HOLE: dict[str, tuple[float, float, float, float]] = {
    "A": (-75.0, 75.0, -30.0, 30.0), "B": (-50.0, 120.0, -45.0, 45.0), "C": (-46.0, 46.0, -80.0, 120.0),
    **{p: PLACE_RANGE[p] for p in ("D", "E", "F", "H", "I", "J")}}
# 折线穿过 Place 时足迹内改走 Place 自己的轴：河沿局部 X（y ＝ 偏移）、城墙沿给定轴；没登记的 Place 被穿过即报错
RIVER_AXIS_Y: dict[str, float] = {"A": 0.0, "B": 0.0, "C": 0.0, "D": -62.0, "E": 0.0, "I": -17.0,
                                  # follow-up 017：城缩到 0.5 后汴河进了相国寺足迹（足迹 1:1、中心距缩了）。
                                  # 相国寺在航线上、不能挪，于是给它登记改道轴：河沿足迹南缘走，
                                  # 与史地关系一致（寺在汴河之北），大殿与院落照旧在干地上。
                                  "H": -140.0}
WALL_AXIS: dict[str, tuple[str, float]] = {"B": ("y", 0.0), "D": ("x", 0.0)}


# ── 航线走廊（follow-up 014：只建拍得到的那一段；口径与代价见 city_plan §8.2）──────────
CORRIDOR: "Corridor | None" = None


class Corridor:
    """镜头先于几何（rule 4g ④）：先有航线，才决定哪儿建、建多细。

    走廊 ＝ 汴河折线的一段 ∪ 每个 Place 的锚点；三档半径决定 A / B / C 级，
    超出 `r_far` 一栋不建。**一个坐标都不新写**——线取 W11 `[[river]]`，点取 place_anchor。
    """

    def __init__(self, cfg: dict, spec: dict) -> None:
        self.r = (float(spec["r_full"]), float(spec["r_mid"]), float(spec["r_far"]))
        self.rp = (float(spec["place_r_full"]), float(spec["place_r_mid"]), float(spec["place_r_far"]))
        self.segs: list[tuple[Pt, Pt]] = []
        for leg in spec["leg"]:
            kind = leg["kind"]
            if kind == "river":
                pts = [(float(a), float(b)) for a, b in next(r for r in cfg["river"] if r["name"] == leg["name"])["points"]]
                s0, s1, acc = float(leg["s0"]), float(leg["s1"]), 0.0
                for a, b2 in zip(pts, pts[1:]):
                    ln = v2len(v2sub(b2, a))
                    if acc + ln > s0 and acc < s1:      # 与 [s0,s1] 有交集的折线段整段收下
                        self.segs.append((a, b2))
                    acc += ln
            elif kind == "street":
                st = next((x for x in cfg["street"] if x["name"] == leg["name"]), None)
                if st is None:
                    raise PlanError(f"§8.2 [[leg]] 街「{leg['name']}」不在 W11 [[street]] 里")
                pts = [(float(a), float(b)) for a, b in st["points"]]
                self.segs += list(zip(pts, pts[1:]))
            else:
                raise PlanError(f"§8.2 [[leg]] kind 只支持 river / street，见到 {kind}")
        if not self.segs:
            raise PlanError("§8.2 走廊没有落到任何折线上（s0/s1 写反了？）")
        self.pts: list[Pt] = [(f.x, f.y) for f in FRAMES.values()]
        self.culled = 0
        self.built: dict[str, int] = {}

    def level(self, p: Pt) -> str | None:
        """线走廊与点走廊各自分档，取最细的那一档（rule 4g ④）。"""
        dl = min(dist_point_seg(p, a, b) for a, b in self.segs)
        dp = min((v2len(v2sub(p, q)) for q in self.pts), default=1e9)
        for k, lv in enumerate("ABC"):
            if dl <= self.r[k] or dp <= self.rp[k]:
                return lv
        return None


def load_corridor(md: str, cfg: dict) -> Corridor:
    sec = md.split("### 8.2", 1)
    if len(sec) != 2:
        raise PlanError("city_plan.md 缺 §8.2 航线走廊")
    m = re.search("```toml" + chr(10) + "(.*?)```", sec[1], re.S)
    if not m:
        raise PlanError("city_plan.md §8.2 缺 toml 块")
    spec = tomllib.loads(m.group(1))
    for k in ("r_full", "r_mid", "r_far", "place_r_full", "place_r_mid", "place_r_far", "leg"):
        if k not in spec:
            raise PlanError(f"§8.2 TOML 缺 {k}")
    return Corridor(cfg, spec)


# ── 拍摄用尺度（follow-up 017，2026-09-18 用户定调「城市面积可以缩小，只需要够拍」）──
# W11 的**坐标**统一乘 CITY_SCALE，**尺寸不乘**：街还是 25 m 宽、房还是 11 m 面宽、墙还是 8.7 m 高，
# 变的只是「两处地点之间有多远」。为什么这是对的取舍：
#   · 一镜到底的航线原本 4 km / 60 s ＝ 67 m/s 平均、城内汴河那段要 95 m/s，比真无人机快一倍；
#     压到 0.5 之后全程 33–45 m/s，**速度问题从根上消失，而且不用切镜**（follow-up 010 的一镜到底照旧）。
#   · 全片没有俯视全城的镜头了（follow-up 014 把末段爬升取消），观众无从对照城的总尺寸；
#     能看出比例的只有「街多宽、房多高、门洞多大」——这些保持 1:1。
# 代价（已登记 divergence #28）：几何不再与「外城周长五十里」这类**距离类**史料对得上。
# 几何只服务 previz，不进 prompt；口播里的里程数照旧引 W11，不引 blend。
CITY_SCALE = 0.5
# 压缩后个别 Place 的 1:1 足迹会压到河/街上（足迹不缩、中心距缩）。逐个挪开，只挪不在航线上的：
#   开封府（Place F）——压缩后汴河从它足迹里穿过（实测 k≤0.7 起冲突）。它是地面镜地点、不在一镜到底的
#   航线上，往北挪 70 m 即让出河道；相对州桥的方位不变（仍在州桥西北），地面镜的取景不受影响。
SCALE_NUDGE: dict[str, tuple[float, float]] = {"开封府": (0.0, 70.0)}
_SCALE_XY = {"gate": ("xy",), "landmark": ("xy",), "place_anchor": ("xy",)}
_SCALE_PTS = {"wall": ("points",), "river": ("points",), "street": ("points",)}


def scale_w11(cfg: dict) -> dict:
    """只缩坐标：xy / points / waypoint 的 pos 与 look_at。宽度、高度、足迹尺寸原样。"""
    k = CITY_SCALE
    if k == 1.0:
        return cfg
    for sec, fields in _SCALE_XY.items():
        for row in cfg.get(sec, []):
            for f in fields:
                row[f] = [float(v) * k for v in row[f]]
    for sec, fields in _SCALE_PTS.items():
        for row in cfg.get(sec, []):
            for f in fields:
                row[f] = [[float(a) * k, float(b) * k] for a, b in row[f]]
    for row in cfg.get("waypoint", []):
        for f in ("pos", "look_at"):
            if f in row:
                v = [float(x) for x in row[f]]
                row[f] = [v[0] * k, v[1] * k] + v[2:]          # z 是高度，不缩
    for row in cfg.get("landmark", []):
        for name, (dx, dy) in SCALE_NUDGE.items():
            if row["name"].startswith(name):
                row["xy"] = [row["xy"][0] + dx, row["xy"][1] + dy]
    return cfg


def load_w11() -> dict:
    md = W11_LAYOUT.read_text(encoding="utf-8")
    sec = md.split("### 2.8", 1)
    m = re.search(r"```toml\n(.*?)```", sec[1] if len(sec) == 2 else "", re.S)
    if not m:
        raise PlanError("w11_city_layout.md §2.8 缺 toml 块")
    cfg = scale_w11(tomllib.loads(m.group(1)))
    for key in ("wall", "gate", "river", "street", "landmark", "place_anchor", "waypoint"):
        if not cfg.get(key):
            raise PlanError(f"W11 TOML 缺 [[{key}]]")
    FRAMES.clear()
    for a in cfg["place_anchor"]:
        pm = re.match(r"Place ([A-Z])\b", a["name"])
        if not pm:
            raise PlanError(f"W11 place_anchor 名「{a['name']}」认不出 Place")
        FRAMES[pm.group(1)] = Frame(float(a["xy"][0]), float(a["xy"][1]), float(a["rot_z_deg"]))
    for p, spec in DERIVED_ANCHORS.items():
        FRAMES[p] = derived_frame(cfg, *spec)
    if set(FRAMES) != set(PLACES):
        raise PlanError(f"Place 锚点只有 {sorted(FRAMES)}，缺 {sorted(set(PLACES) - set(FRAMES))}")
    return cfg


# W11 没有 place_anchor 的 Place：锚点只从 W11 已有条目推出（名字 + 沿线距离），旋转对齐所在街 / 河（city_plan §1）
DERIVED_ANCHORS: dict[str, tuple[str, str, float]] = {
    "D": ("gate", "宣德门（宣德楼）", 0.0),                 # 原点＝门点（在宫城南墙线上），+Y 沿御街向北
    "E": ("river", "汴河|东水门", -220.0),                 # 东水门上游 220 m 的汴河中线，+X 沿下游（判断：卡「便桥以西、沿城根」）
    "F": ("landmark", "开封府", 0.0),
    "H": ("landmark", "相国寺", 0.0),
    "I": ("landmark", "桑家瓦子（中瓦、里瓦）", 0.0),
    "J": ("street_out", "御街·龙津桥—南薰门", 180.0),       # 南薰门外 180 m 的出城路口，+Y 朝城
}


def derived_frame(cfg: dict, kind: str, name: str, dist: float) -> Frame:
    grid = next(float(a["rot_z_deg"]) for a in cfg["place_anchor"] if a["name"].startswith("Place C"))
    if kind in ("gate", "landmark"):
        e = next((x for x in cfg[kind] if x["name"] == name), None)
        if e is None:
            raise PlanError(f"W11 没有 [[{kind}]]「{name}」")
        return Frame(float(e["xy"][0]), float(e["xy"][1]), grid)
    if kind == "river":
        rname, gname = name.split("|")
        pts = [(float(p[0]), float(p[1])) for p in next(r for r in cfg["river"] if r["name"] == rname)["points"]]
        g = next(x for x in cfg["gate"] if x["name"] == gname)
        acc, best = 0.0, (math.inf, 0.0)
        for a, b in zip(pts, pts[1:]):
            d = v2sub(b, a)
            ln = v2len(d)
            t = max(0.0, min(1.0, v2dot(v2sub((float(g["xy"][0]), float(g["xy"][1])), a), d) / (ln * ln)))
            q = (a[0] + d[0] * t, a[1] + d[1] * t)
            if v2len(v2sub(q, (float(g["xy"][0]), float(g["xy"][1])))) < best[0]:
                best = (v2len(v2sub(q, (float(g["xy"][0]), float(g["xy"][1])))), acc + t * ln)
            acc += ln
        target, acc = best[1] + dist, 0.0
        for a, b in zip(pts, pts[1:]):
            d = v2sub(b, a)
            ln = v2len(d)
            if acc + ln >= target:
                t = (target - acc) / ln
                return Frame(a[0] + d[0] * t, a[1] + d[1] * t, math.degrees(math.atan2(d[1], d[0])))
            acc += ln
        raise PlanError(f"{name} 沿线 {dist} m 超出河线")
    if kind == "street_out":
        st = next(s for s in cfg["street"] if s["name"] == name)
        a, b = (float(v) for v in st["points"][0]), (float(v) for v in st["points"][-1])
        a, b = tuple(a), tuple(b)
        d = v2sub(b, a)
        u = (d[0] / v2len(d), d[1] / v2len(d))
        return Frame(b[0] + u[0] * dist, b[1] + u[1] * dist, math.degrees(math.atan2(u[0], -u[1])))
    raise PlanError(f"锚点推导方式「{kind}」未实现")


def v2sub(a: Pt, b: Pt) -> Pt:
    return (a[0] - b[0], a[1] - b[1])


def v2dot(a: Pt, b: Pt) -> float:
    return a[0] * b[0] + a[1] * b[1]


def v2len(a: Pt) -> float:
    return math.hypot(a[0], a[1])


def seg_quad(a: Pt, b: Pt, half: float, ext: float = 0.0) -> list[Pt]:
    d = v2sub(b, a)
    ln = max(v2len(d), 1e-9)
    ux, uy = d[0] / ln, d[1] / ln
    nx, ny = -uy * half, ux * half
    ax, ay = a[0] - ux * ext, a[1] - uy * ext
    bx, by = b[0] + ux * ext, b[1] + uy * ext
    return [(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)]


def sat_overlap(p: list[Pt], q: list[Pt]) -> bool:
    for poly in (p, q):
        for i, a in enumerate(poly):
            b = poly[(i + 1) % len(poly)]
            ax = (a[1] - b[1], b[0] - a[0])
            pp = [v2dot(ax, v) for v in p]
            qq = [v2dot(ax, v) for v in q]
            if max(pp) < min(qq) or max(qq) < min(pp):
                return False
    return True


def point_in_poly(pt: Pt, poly: list[Pt]) -> bool:
    x, y = pt
    inside = False
    for i, a in enumerate(poly):
        b = poly[(i + 1) % len(poly)]
        if (a[1] > y) != (b[1] > y) and x < (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]) + a[0]:
            inside = not inside
    return inside


def dist_point_seg(p: Pt, a: Pt, b: Pt) -> float:
    d = v2sub(b, a)
    t = max(0.0, min(1.0, v2dot(v2sub(p, a), d) / max(v2dot(d, d), 1e-12)))
    return v2len(v2sub(p, (a[0] + d[0] * t, a[1] + d[1] * t)))


def place_poly(place: str, margin: float = 0.0, hole: bool = False) -> list[Pt]:
    x0, x1, y0, y1 = (PLACE_HOLE if hole else PLACE_RANGE)[place]
    f = FRAMES[place]
    return [f.world(x0 - margin, y0 - margin), f.world(x1 + margin, y0 - margin),
            f.world(x1 + margin, y1 + margin), f.world(x0 - margin, y1 + margin)]


def reroute(points: list[Pt], place: str, axis: str | None, offset: float = 0.0,
            what: str = "") -> tuple[list[Pt], tuple[Pt, Pt] | None]:
    """折线穿过 Place 足迹时，足迹内改走 Place 自己的轴线（x 轴在局部 y＝offset、y 轴在局部 x＝offset），接缝处不错位。"""
    f = FRAMES[place]
    x0, x1, y0, y1 = PLACE_RANGE[place]
    foot = place_poly(place)
    inside = [i for i, p in enumerate(points) if point_in_poly(p, foot)]
    cross = [i for i in range(len(points) - 1) if sat_overlap(seg_quad(points[i], points[i + 1], 0.01), foot)]
    if not inside and not cross:
        return points, None
    if axis is None:
        raise PlanError(f"{what} 穿过 Place {place} 足迹，但该 Place 没有登记改道轴（RIVER_AXIS_Y / WALL_AXIS）")
    ends = [f.world(x0, offset), f.world(x1, offset)] if axis == "x" else [f.world(offset, y0), f.world(offset, y1)]
    if inside:
        lo_i, hi_i = min(inside), max(inside)
        if inside != list(range(lo_i, hi_i + 1)) or lo_i == 0 or hi_i == len(points) - 1:
            raise PlanError(f"折线在 Place {place} 足迹内的点不连续或在端点，无法改道")
        before, after = points[:lo_i], points[hi_i + 1:]
    else:
        before, after = points[:cross[0] + 1], points[cross[0] + 1:]
    d = v2sub(after[0], before[-1])
    ends.sort(key=lambda p: v2dot(v2sub(p, before[-1]), d))
    return before + ends + after, (ends[0], ends[1])


@dataclass(frozen=True)
class LandmarkPlan:
    index: int
    name: str
    method: str
    height: float | None
    asset: str | None
    level: str


def parse_global_plan(md: str) -> tuple[dict[str, LandmarkPlan], tuple[str, ...]]:
    sec = md.split("## 8. 全城层", 1)
    if len(sec) != 2:
        raise PlanError("city_plan.md 缺「## 8. 全城层」")
    body = sec[1].split("\n## ", 1)[0]
    km = re.search(r"住宅单元键：(.+)", body)
    if not km:
        raise PlanError("city_plan.md §8 缺「住宅单元键」")
    unit_keys = tuple(re.findall(r"`(p\d+[a-z]?)`", km.group(1)))
    plans: dict[str, LandmarkPlan] = {}
    head = "| 编号 | W11 地标 | 建法 | 高 m | 资产键 | 级 | 说明 |"
    if head not in body:
        raise PlanError("city_plan.md §8.1 表头不对")
    for ln in body.split(head, 1)[1].splitlines()[2:]:
        if not ln.startswith("|"):
            break
        c = [norm(x) for x in re.split(r"(?<!\\)\|", ln)[1:-1]]
        if len(c) != 7:
            raise PlanError(f"§8.1 行列数 {len(c)} ≠ 7：{ln[:40]}")
        if c[2] not in GLOBAL_METHODS:
            raise PlanError(f"§8.1「{c[1]}」建法「{c[2]}」未实现")
        plans[c[1]] = LandmarkPlan(int(c[0]), c[1], c[2], None if c[3] == "—" else float(c[3]),
                                   None if c[4] == "—" else c[4], c[5])
    if not unit_keys or not plans:
        raise PlanError("city_plan.md §8 住宅单元键或地标表为空")
    return plans, unit_keys


GLOBAL_METHODS = {"跳过", "殿基", "殿院", "桥", "楼群", "瓦子", "客店带", "工地", "坛", "塔", "池", "苑", "冈"}


G_EXTENT = (-9000.0, 10000.0, -9000.0, 9000.0)   # 判断：WP3 高空全景的画框要落在地面里，不露地面边
G_WATER_Z = -0.02
STREET_H = 0.15                                   # 判断：街面比地面高一点，灰模阴影才读得出街
WALL_TOP_FALLBACK = {"里城": 4.0, "宫城": 3.0}      # ⚠️ C：W11 顶宽「未查」（top_m=0），按外城顶宽类推
GATE_GAP = {"外城": 12.0, "里城": 10.0, "宫城": 8.0}  # 判断：W11 未给门洞宽的门一律按此开口
WENG_DEFAULT = (80.0, 50.0)                        # ⚠️ C：「瓮城三层」无尺寸，沿墙 80 × 外凸 50（只建一层）
MAMIAN = (12.0, 16.0)                              # 判断：马面沿墙宽 × 外凸（W11 只给间距 161 m）


@dataclass
class World:
    cfg: dict
    rivers: dict[str, tuple[list[Pt], float]]
    rings: dict[str, list[Pt]]
    ring_skip: dict[str, tuple[Pt, Pt] | None]
    keepout: list[list[Pt]]
    keepout_street: list[list[Pt]] = field(default_factory=list)


WORLD: list[World] = []


def ring_key(name: str) -> str:
    return name.split("（", 1)[0]


def octagon(c: Pt, r: float) -> list[Pt]:
    return [(c[0] + r * math.cos(math.pi * (i + 0.5) / 4), c[1] + r * math.sin(math.pi * (i + 0.5) / 4)) for i in range(8)]


def extrude(b: Batch, poly: list[Pt], z0: float, z1: float) -> None:
    b.poly_solid([Vector((x, y, z0)) for x, y in poly], [Vector((x, y, z1)) for x, y in poly])


def ring_ccw(ring: list[Pt]) -> bool:
    return sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(ring, ring[1:] + ring[:1])) > 0


def seg_frame(a: Pt, b: Pt, ccw: bool) -> tuple[Pt, Pt, float]:
    d = v2sub(b, a)
    ln = v2len(d)
    u = (d[0] / ln, d[1] / ln)
    out = (u[1], -u[0]) if ccw else (-u[1], u[0])
    return u, out, ln


def world_setup(cfg: dict) -> World:
    rivers: dict[str, tuple[list[Pt], float]] = {}
    for rv in cfg["river"]:
        pts = [(float(p[0]), float(p[1])) for p in rv["points"]]
        for p in PLACES:
            pts, _ = reroute(pts, p, "x" if p in RIVER_AXIS_Y else None, RIVER_AXIS_Y.get(p, 0.0), rv["name"])
        rivers[rv["name"]] = (pts, float(rv["width_m"]))
    rings: dict[str, list[Pt]] = {}
    skips: dict[str, tuple[Pt, Pt] | None] = {}
    for w in cfg["wall"]:
        pts = [(float(p[0]), float(p[1])) for p in w["points"]]
        skip = None
        for p in PLACES:
            ax, off = WALL_AXIS.get(p, (None, 0.0))
            pts, sk = reroute(pts, p, ax, off, w["name"])
            skip = skip or sk
        if pts[0] == pts[-1]:
            pts = pts[:-1]
        rings[ring_key(w["name"])] = pts
        skips[ring_key(w["name"])] = skip
    world = World(cfg, rivers, rings, skips, [])
    WORLD[:] = [world]
    return world


def cut_places(ob: bpy.types.Object, margin: float = 0.0) -> None:
    """全城层几何在 Place 足迹内让位：四个平面切开，删掉足迹内的面。"""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    xs = [v.co.x for v in bm.verts]
    ys = [v.co.y for v in bm.verts]
    for p in PLACES:
        poly = place_poly(p, margin, hole=True)
        if max(xs) < min(q[0] for q in poly) or min(xs) > max(q[0] for q in poly) or \
           max(ys) < min(q[1] for q in poly) or min(ys) > max(q[1] for q in poly):
            continue
        for i, a in enumerate(poly):
            c = poly[(i + 1) % 4]
            geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
            bmesh.ops.bisect_plane(bm, geom=geom, plane_co=Vector((a[0], a[1], 0.0)),
                                   plane_no=Vector((c[1] - a[1], a[0] - c[0], 0.0)).normalized())
        kill = [f for f in bm.faces if point_in_poly((f.calc_center_median().x, f.calc_center_median().y), poly)]
        bmesh.ops.delete(bm, geom=kill, context="FACES")
    bm.to_mesh(ob.data)
    bm.free()


def moat_quads(world: World) -> list[list[Pt]]:
    w = next(x for x in world.cfg["wall"] if float(x.get("moat_width_m", 0)) > 0)
    ring = world.rings[ring_key(w["name"])]
    skip = world.ring_skip[ring_key(w["name"])]
    inner_g = float(w["base_m"]) / 2 + float(w["moat_offset_m"])          # 判断：「距墙 30 m」从墙脚量起
    outer_g = inner_g + float(w["moat_width_m"])
    bx0, bx1 = span(row_of("B", 24).where, "x")
    if abs(bx0 - inner_g) > 0.05 or abs(bx1 - outer_g) > 0.05:
        raise PlanError(f"方块 24 护龙河 x {bx0:g}…{bx1:g} 与 W11（墙脚外 {w['moat_offset_m']} m、宽 {w['moat_width_m']} m → {inner_g:g}…{outer_g:g}）不一致")
    ccw = ring_ccw(ring)
    quads: list[list[Pt]] = []
    for i, a in enumerate(ring):
        b = ring[(i + 1) % len(ring)]
        if skip and {a, b} == set(skip):
            continue
        u, out, ln = seg_frame(a, b, ccw)
        quads.append([(a[0] + out[0] * inner_g, a[1] + out[1] * inner_g), (b[0] + out[0] * inner_g, b[1] + out[1] * inner_g),
                      (b[0] + out[0] * outer_g, b[1] + out[1] * outer_g), (a[0] + out[0] * outer_g, a[1] + out[1] * outer_g)])
        mid = (inner_g + outer_g) / 2
        quads.append(octagon((b[0] + out[0] * mid, b[1] + out[1] * mid), (outer_g - inner_g) / 2 + 6.0))
    return quads


def build_ground(world: World, ponds: list[list[Pt]]) -> None:
    x0, x1, y0, y1 = G_EXTENT
    ground = solid_box("G_000_ground", "G_GROUND", (x0, y0, -1.0), (x1, y1, Z_STREET))
    gbm = bmesh.new()
    gbm.from_mesh(ground.data)
    top_edges = list({e for f in gbm.faces if f.normal.z > 0.9 for e in f.edges})
    # 布尔后整片地面顶面只剩几个带洞的巨型 n-gon，显示三角化会翻面、拉出放射状暗纹——先切成网格
    bmesh.ops.subdivide_edges(gbm, edges=top_edges, cuts=40, use_grid_fill=True)
    gbm.to_mesh(ground.data)
    gbm.free()
    solid_box("G_000_water", "G_WATER", (x0, y0, G_WATER_Z - 0.05), (x1, y1, G_WATER_Z))
    cut = Batch()
    for pts, wd in world.rivers.values():
        for a, b in zip(pts, pts[1:]):
            extrude(cut, seg_quad(a, b, wd / 2), -2.0, Z_STREET + 1.0)
        for p in pts[1:-1]:
            extrude(cut, octagon(p, wd / 2 / math.cos(math.pi / 8)), -2.0, Z_STREET + 1.0)
    for q in moat_quads(world) + ponds:
        extrude(cut, q, -2.0, Z_STREET + 1.0)
    for p in PLACES:
        extrude(cut, place_poly(p, 0.0, hole=True), -2.0, Z_STREET + 1.0)
    cutter = cut.finish("G_000_ground_cutter", "G_TMP")
    mod = ground.modifiers.new("cut", "BOOLEAN")
    mod.operation, mod.solver, mod.object = "DIFFERENCE", "EXACT", cutter
    mod.use_self, mod.use_hole_tolerant = True, True
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ground.evaluated_get(dg))
    me.materials.clear()
    old = ground.data
    ground.modifiers.clear()
    ground.data = me
    bpy.data.meshes.remove(old)
    tmp = COLS.pop("G_TMP")
    bpy.data.objects.remove(cutter)
    bpy.data.collections.remove(tmp)


def gate_gap(g: dict, world: World) -> float:
    form = g["form"]
    for pat in (r"缺口宽约(\d+) ?m", r"通阔约(\d+) ?m"):
        m = re.search(pat, form)
        if m:
            return float(m.group(1))
    if "水门" in form:
        near = [wd for pts, wd in world.rivers.values()
                if min(dist_point_seg(tuple(g["xy"]), a, b) for a, b in zip(pts, pts[1:])) < 120.0]
        return max(30.0, max(near, default=0.0) + 12.0)
    return GATE_GAP[g["ring"]]


def gate_segment(g: dict, world: World) -> tuple[int, float]:
    ring = world.rings[g["ring"]]
    best = min(range(len(ring)), key=lambda i: dist_point_seg(tuple(g["xy"]), ring[i], ring[(i + 1) % len(ring)]))
    a, b = ring[best], ring[(best + 1) % len(ring)]
    d = v2sub(b, a)
    s = v2dot(v2sub(tuple(g["xy"]), a), d) / v2len(d)
    return best, s


def in_any_place(pt: Pt, margin: float) -> bool:
    return any(point_in_poly(pt, place_poly(p, margin)) for p in PLACES)


def rect_in_any_place(rect: list[Pt], margin: float = 0.0) -> bool:
    """矩形与任一 Place 足迹相交（AABB 相交判定）——压缩后中心点判定不够用了。"""
    rx0, rx1 = min(q[0] for q in rect), max(q[0] for q in rect)
    ry0, ry1 = min(q[1] for q in rect), max(q[1] for q in rect)
    for p in PLACES:
        poly = place_poly(p, margin)
        px0, px1 = min(q[0] for q in poly), max(q[0] for q in poly)
        py0, py1 = min(q[1] for q in poly), max(q[1] for q in poly)
        if rx0 < px1 and px0 < rx1 and ry0 < py1 and py0 < ry1:
            return True
    return False


def build_walls(world: World) -> dict[str, list[tuple[int, float, float]]]:
    gaps: dict[str, list[tuple[int, float, float]]] = {}
    for idx, w in enumerate(world.cfg["wall"]):
        key = ring_key(w["name"])
        ring, skip = world.rings[key], world.ring_skip[key]
        base, h = float(w["base_m"]), float(w["height_m"])
        top = float(w["top_m"]) or WALL_TOP_FALLBACK[key]            # ⚠️ C：顶宽 / 墙高未查时见 WALL_TOP_FALLBACK 与 W11 note
        ccw = ring_ccw(ring)
        cuts: list[tuple[int, float, float]] = []
        for g in world.cfg["gate"]:
            if g["ring"] == key and not in_any_place(tuple(g["xy"]), 20.0):
                i, s = gate_segment(g, world)
                cuts.append((i, s - gate_gap(g, world) / 2, s + gate_gap(g, world) / 2))
        for i, a in enumerate(ring):
            b = ring[(i + 1) % len(ring)]
            for pts, wd in world.rivers.values():
                for c, d in zip(pts, pts[1:]):
                    den = (b[0] - a[0]) * (d[1] - c[1]) - (b[1] - a[1]) * (d[0] - c[0])
                    if abs(den) < 1e-9:
                        continue
                    t = ((c[0] - a[0]) * (d[1] - c[1]) - (c[1] - a[1]) * (d[0] - c[0])) / den
                    r = ((c[0] - a[0]) * (b[1] - a[1]) - (c[1] - a[1]) * (b[0] - a[0])) / den
                    if 0 <= t <= 1 and 0 <= r <= 1:
                        s = t * v2len(v2sub(b, a))
                        cuts.append((i, s - wd / 2 - 4.0, s + wd / 2 + 4.0))
        gaps[key] = cuts
        wall = Batch()
        mam = Batch()
        prof = [(-base / 2, Z_STREET - 1.0), (base / 2, Z_STREET - 1.0), (top / 2, Z_STREET + h), (-top / 2, Z_STREET + h)]
        for i, a in enumerate(ring):
            b = ring[(i + 1) % len(ring)]
            if skip and {a, b} == set(skip):
                continue
            u, out, ln = seg_frame(a, b, ccw)
            holes = sorted((s0, s1) for j, s0, s1 in cuts if j == i)
            pieces, cur = [], -base / 2
            for s0, s1 in holes:
                if s0 > cur:
                    pieces.append((cur, s0))
                cur = max(cur, s1)
            if cur < ln + base / 2:
                pieces.append((cur, ln + base / 2))
            if skip and a in skip:
                pieces = [(max(p0, 0.0), p1) for p0, p1 in pieces if p1 > 0.0]
            if skip and b in skip:
                pieces = [(p0, min(p1, ln)) for p0, p1 in pieces if p0 < ln]
            for s0, s1 in pieces:
                p0 = (a[0] + u[0] * s0, a[1] + u[1] * s0)
                p1 = (a[0] + u[0] * s1, a[1] + u[1] * s1)
                wall.poly_solid([Vector((p0[0] + out[0] * o, p0[1] + out[1] * o, z)) for o, z in prof],
                                [Vector((p1[0] + out[0] * o, p1[1] + out[1] * o, z)) for o, z in prof])
            spacing = float(w.get("mamian_spacing_m", 0))
            if spacing > 0:
                for k in range(1, int(ln // spacing) + 1):
                    s = k * spacing
                    if s > ln - 30 or any(s0 - 30 < s < s1 + 30 for s0, s1 in holes):
                        continue
                    c = (a[0] + u[0] * s + out[0] * (base / 2 + MAMIAN[1] / 2), a[1] + u[1] * s + out[1] * (base / 2 + MAMIAN[1] / 2))
                    q = [(c[0] + u[0] * du + out[0] * do, c[1] + u[1] * du + out[1] * do)
                         for du, do in ((-MAMIAN[0] / 2, -MAMIAN[1] / 2 - 6), (MAMIAN[0] / 2, -MAMIAN[1] / 2 - 6),
                                        (MAMIAN[0] / 2, MAMIAN[1] / 2), (-MAMIAN[0] / 2, MAMIAN[1] / 2))]
                    extrude(mam, q, Z_STREET - 1.0, Z_STREET + h)
        wall.finish(f"G_{101 + idx}_wall_{key}", "G_WALL", 101 + idx)
        if spacing > 0:
            mam.finish(f"G_{101 + idx}_mamian_{key}", "G_WALL", 101 + idx)
        NOTES.append(f"G 城墙 {key}：底 {base:g} / 顶 {top:g} / 高 {h:g} m" + ("（顶宽 ⚠️ C 类推）" if not float(w['top_m']) else ""))
    return gaps


def build_gates(world: World) -> int:
    built = 0
    for gi, g in enumerate(world.cfg["gate"]):
        if in_any_place(tuple(g["xy"]), 20.0):
            NOTES.append(f"G 城门 {g['name']}：在 Place 足迹内，由 Place 自己建")
            continue
        key = g["ring"]
        w = next(x for x in world.cfg["wall"] if ring_key(x["name"]) == key)
        base, h = float(w["base_m"]), float(w["height_m"])
        top = float(w["top_m"]) or WALL_TOP_FALLBACK[key]
        ring = world.rings[key]
        i, s = gate_segment(g, world)
        a, b = ring[i], ring[(i + 1) % len(ring)]
        u, out, _ = seg_frame(a, b, ring_ccw(ring))
        c = (a[0] + u[0] * s, a[1] + u[1] * s)
        gap = gate_gap(g, world)
        form = g["form"]
        bt = Batch()

        def rect(cu: float, co: float, lu: float, lo: float) -> list[Pt]:
            return [(c[0] + u[0] * du + out[0] * do, c[1] + u[1] * du + out[1] * do)
                    for du, do in ((cu - lu / 2, co - lo / 2), (cu + lu / 2, co - lo / 2), (cu + lu / 2, co + lo / 2), (cu - lu / 2, co + lo / 2))]

        if "五门洞" in form:
            raise PlanError(f"{g['name']}：五门洞门楼只由 Place D 建，全城层不该走到这里")
        if "角门" not in form:
            extrude(bt, rect(0.0, 0.0, gap + 4.0, top + 8.0), Z_STREET + (6.0 if "水门" in form else 7.0), Z_STREET + h)
            extrude(bt, rect(0.0, 0.0, gap + 14.0, top + 6.0), Z_STREET + h, Z_STREET + h + 6.0)
        if "瓮城" in form or "直门两重" in form:
            m = re.search(r"(东西|南北)(\d+)×(东西|南北)(\d+)", form)
            if m:
                dims = {m.group(1): float(m.group(2)), m.group(3): float(m.group(4))}
                along_axis = "南北" if g["wall"] in ("东", "西") else "东西"
                along, outw = dims[along_axis], dims["东西" if along_axis == "南北" else "南北"]
            else:
                along, outw = WENG_DEFAULT if "瓮城" in form else (60.0, 40.0)
            t = 12.0
            o0 = base / 2
            straight = "直门" in form
            side_gap = 0.0 if straight else 14.0
            extrude(bt, rect(-along / 2 + t / 2, o0 + outw / 2, t, outw), Z_STREET - 1.0, Z_STREET + h)
            extrude(bt, rect(along / 2 - t / 2, o0 + outw / 2 + side_gap / 2, t, outw - side_gap), Z_STREET - 1.0, Z_STREET + h)
            if straight:
                for sg in (-1, 1):
                    extrude(bt, rect(sg * (along / 4 + gap / 4), o0 + outw - t / 2, along / 2 - gap / 2, t), Z_STREET - 1.0, Z_STREET + h)
            else:
                extrude(bt, rect(0.0, o0 + outw - t / 2, along, t), Z_STREET - 1.0, Z_STREET + h)
        bt.finish(f"G_{201 + gi}_gate_{g['name']}", "G_GATES", 201 + gi)
        built += 1
    return built


def build_streets(world: World) -> int:
    for si, st in enumerate(world.cfg["street"]):
        pts = [(float(p[0]), float(p[1])) for p in st["points"]]
        wd = float(st["width_m"])
        b = Batch()
        for a, c in zip(pts, pts[1:]):
            extrude(b, seg_quad(a, c, wd / 2), Z_STREET - 0.05, Z_STREET + STREET_H)
        for p in pts[1:-1]:
            extrude(b, octagon(p, wd / 2 / math.cos(math.pi / 8)), Z_STREET - 0.05, Z_STREET + STREET_H)
        ob = b.finish(f"G_{401 + si}_street", "G_STREETS", 401 + si)
        ob["bj_name"] = st["name"]
        cut_places(ob)
        quads = [seg_quad(a, c, wd / 2 + 3.0, 3.0) for a, c in zip(pts, pts[1:])]
        world.keepout += quads
        # 同一份也单独记一份：街面挡的是**房子**。街上的东西（行道柳、杈子、摊、车）
        # 本来就该站在街上，撒点时要能把这一层摘掉（follow-up 016，city_plan §12 `on_street`）
        world.keepout_street += quads
    return len(world.cfg["street"])


BLOCK_PITCH, BLOCK_SIZE = 80.0, 64.0             # 判断：北宋坊巷无实测街区尺度，按 80 m 网格、16 m 巷道
B_CORRIDOR_YUJIE, B_RADIUS_S36 = 250.0, 400.0     # rule 4g ④：S02 御街俯冲走廊 / S36 起飞点周围升 B 级


def lm_rect(lm: dict, pad: float = 0.0) -> list[Pt]:
    ew, ns = (float(v) for v in lm["extent_m"])
    ew, ns = (ew or 40.0) + 2 * pad, (ns or 40.0) + 2 * pad      # 判断：点位地标按 40 × 40
    x, y = (float(v) for v in lm["xy"])
    return [(x - ew / 2, y - ns / 2), (x + ew / 2, y - ns / 2), (x + ew / 2, y + ns / 2), (x - ew / 2, y + ns / 2)]


def house(b: Batch, c: Pt, u: Pt, n: Pt, dims: tuple[float, float, float], level: str) -> None:
    """一个住宅单元（长边沿 u、门脸朝 n）。

    精度三档（rule 4g ④，走廊制见 city_plan §8.2）：
      C  纯体块 —— 只当远景轮廓
      B  体块 + 悬山屋面 —— 中景，看得出屋顶形制
      A  台基 + 墙身 + 出檐悬山 + 正脊 + 临街披檐 —— 贴身而过的那几百米

    **走廊是在这里闸的**：城外关厢、田间村落、城内街区三条路都汇进本函数，
    在这里判一次，就不会有哪条路漏掉（follow-up 014）。
    """
    if CORRIDOR is not None:
        lv = CORRIDOR.level(c)
        if lv is None:
            CORRIDOR.culled += 1
            return
        level = lv
        CORRIDOR.built[lv] = CORRIDOR.built.get(lv, 0) + 1
    lx, ly, h = dims

    def quad(ex: float) -> list[Pt]:
        a, d = lx / 2 + ex, ly / 2 + ex
        return [(c[0] + u[0] * sa + n[0] * sd, c[1] + u[1] * sa + n[1] * sd)
                for sa, sd in ((-a, -d), (a, -d), (a, d), (-a, d))]

    q = quad(0.0)
    if level == "C":
        extrude(b, q, Z_STREET, Z_STREET + h)
        return
    base = Z_STREET
    if level == "A":                                  # 台基：各边宽出 0.45 m、高 0.45 m
        base = Z_STREET + 0.45
        extrude(b, quad(0.45), Z_STREET, base)
    eave = base + h * (0.60 if level == "A" else 0.65)
    extrude(b, q, base, eave)                         # 墙身
    ov = quad(0.85) if level == "A" else q            # A 级出檐 0.85 m（宋木构出檐深，这是轮廓的关键）
    ridge_z = base + h
    mid = [((ov[0][0] + ov[3][0]) / 2, (ov[0][1] + ov[3][1]) / 2),
           ((ov[1][0] + ov[2][0]) / 2, (ov[1][1] + ov[2][1]) / 2)]
    sec0 = [Vector((ov[0][0], ov[0][1], eave)), Vector((ov[3][0], ov[3][1], eave)), Vector((mid[0][0], mid[0][1], ridge_z))]
    sec1 = [Vector((ov[1][0], ov[1][1], eave)), Vector((ov[2][0], ov[2][1], eave)), Vector((mid[1][0], mid[1][1], ridge_z))]
    b.poly_solid(sec0, sec1)
    if level != "A":
        return
    extrude(b, seg_quad(mid[0], mid[1], 0.18), ridge_z - 0.10, ridge_z + 0.28)   # 正脊
    # 临街披檐：门脸一侧（+n）挑出 1.5 m 的一坡草棚，是宋代街屋最认得出的一笔
    fo, fi = quad(0.0)[3], quad(0.0)[2]
    po = [(fo[0] + n[0] * 1.5, fo[1] + n[1] * 1.5), (fi[0] + n[0] * 1.5, fi[1] + n[1] * 1.5)]
    z_hi, z_lo = base + h * 0.42, base + h * 0.30
    b.poly_solid([Vector((fo[0], fo[1], z_hi)), Vector((po[0][0], po[0][1], z_lo)), Vector((po[0][0], po[0][1], z_lo - 0.12)), Vector((fo[0], fo[1], z_hi - 0.12))],
                 [Vector((fi[0], fi[1], z_hi)), Vector((po[1][0], po[1][1], z_lo)), Vector((po[1][0], po[1][1], z_lo - 0.12)), Vector((fi[0], fi[1], z_hi - 0.12))])


def unit_dims(keys: tuple[str, ...]) -> dict[str, tuple[float, float, float]]:
    out = {}
    for k in keys:
        pr = get_proto(k, "A")
        d = pr.hi - pr.lo
        out[k] = (max(d.x, d.y), min(d.x, d.y), d.z)
    return out


def hall(b: Batch, cx: float, cy: float, lx: float, ly: float, h: float) -> None:
    b.box((cx - lx / 2, cy - ly / 2, Z_STREET), (cx + lx / 2, cy + ly / 2, Z_STREET + h * 0.7))
    b.hip(cx, cy, lx + 2.0, ly + 2.0, Z_STREET + h * 0.7, h * 0.3)


def build_landmarks(world: World, plans: dict[str, LandmarkPlan], keys: tuple[str, ...]) -> dict[str, int]:
    names = [lm["name"] for lm in world.cfg["landmark"]]
    if set(names) != set(plans):
        raise PlanError(f"§8.1 地标表与 W11 不一致：缺 {sorted(set(names) - set(plans))}，多 {sorted(set(plans) - set(names))}")
    dims = unit_dims(keys)
    counts: dict[str, int] = {}
    for lm in world.cfg["landmark"]:
        plan = plans[lm["name"]]
        x, y = (float(v) for v in lm["xy"])
        world.keepout.append(lm_rect(lm, 6.0))          # follow-up 007：地标四周只留一条街宽
        if plan.method in ("跳过", "池"):
            counts[plan.method] = counts.get(plan.method, 0) + 1
            continue
        if rect_in_any_place(lm_rect(lm)):
            # 判定看**整块足迹是否相交**，不只看中心点：城压到 0.5 之后（follow-up 017）
            # 地标中心还在 Place 之外、体量却压进去了，于是全城层与 Place 的精细版重叠。
            NOTES.append(f"G 地标 {lm['name']}：足迹与 Place 相交，跳过（Place 自己建精细版）")
            continue
        r = lm_rect(lm)
        ew, ns = r[1][0] - r[0][0], r[2][1] - r[1][1]
        h = plan.height or 0.0
        rng = random.Random(plan.index)
        b = Batch()
        m = plan.method
        if plan.asset:
            ob = bpy.data.objects.new(f"G_{plan.index}_lm_{plan.asset}", None)
            pr = get_proto(plan.asset, plan.level)
            ob.instance_type, ob.instance_collection = "COLLECTION", pr.collection
            ob.location = (x, y, Z_STREET)
            ob["bj_row"], ob["bj_asset"], ob["bj_name"] = plan.index, plan.asset, lm["name"]
            collection("G_LANDMARKS").objects.link(ob)
            counts["资产实例"] = counts.get("资产实例", 0) + 1
            continue
        if m == "殿基":
            b.box((x - ew / 2, y - ns / 2, Z_STREET), (x + ew / 2, y + ns / 2, Z_STREET + 4.0))
            b.box((x - ew * 0.35, y - ns * 0.3, Z_STREET + 4.0), (x + ew * 0.35, y + ns * 0.3, Z_STREET + h - 6.0))
            b.hip(x, y, ew * 0.75, ns * 0.65, Z_STREET + h - 6.0, 6.0)
        elif m == "殿院":
            for (x0, y0), (x1, y1) in zip(r, r[1:] + r[:1]):
                extrude(b, seg_quad((x0, y0), (x1, y1), 1.5, 1.5), Z_STREET, Z_STREET + 5.0)
            for k in range(3):
                hall(b, x, y - ns * 0.3 + k * ns * 0.3, ew * 0.5, ns * 0.16, h)
        elif m == "桥":
            b.box((x - ew / 2, y - ns / 2, Z_STREET - 0.2), (x + ew / 2, y + ns / 2, Z_STREET + h))
        elif m == "楼群":
            for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1), (0, 1)):
                hall(b, x + dx * ew * 0.3, y + dy * ns * 0.3, ew * 0.3, ns * 0.3, h)
        elif m == "瓦子":
            for k in range(rng.randint(4, 6)):
                cx, cy = x + rng.uniform(-ew * 0.3, ew * 0.3), y + rng.uniform(-ns * 0.3, ns * 0.3)
                b.box((cx - 15, cy - 10, Z_STREET), (cx + 15, cy + 10, Z_STREET + h * 0.7))
                b.gable_x(cx - 15, cx + 15, cy - 10, cy + 10, Z_STREET + h * 0.7, Z_STREET + h)
        elif m == "客店带":
            long_x = ew >= ns
            u, n = ((1.0, 0.0), (0.0, 1.0)) if long_x else ((0.0, 1.0), (1.0, 0.0))
            ln = max(ew, ns)
            s = -ln / 2
            while s < ln / 2 - 12:
                k = rng.choice(keys)
                c = (x + u[0] * (s + dims[k][0] / 2), y + u[1] * (s + dims[k][0] / 2))
                house(b, c, u, n, dims[k], plan.level)
                s += dims[k][0] + rng.choice((0.0, 1.0, 2.0))
        elif m == "工地":
            for k in range(3):
                cx, cy = x + rng.uniform(-ew * 0.25, ew * 0.25), y + rng.uniform(-ns * 0.3, ns * 0.3)
                b.hip(cx, cy, rng.uniform(90, 150), rng.uniform(90, 150), Z_STREET, h * rng.uniform(0.55, 1.0))
            for k in range(40):
                cx, cy = x + rng.uniform(-ew * 0.45, ew * 0.45), y + rng.uniform(-ns * 0.45, ns * 0.45)
                b.cbox((cx, cy, Z_STREET + 1.0), (rng.uniform(3, 6), rng.uniform(2, 4), 2.0))
            for k in range(8):
                c = (x - ew * 0.45 + 14.0 * k, y - ns * 0.45 + 4.0)
                house(b, c, (1.0, 0.0), (0.0, 1.0), dims[keys[-1]] if len(keys) else (8, 7.5, 7.5), "C")
            for (x0, y0), (x1, y1) in zip(r, r[1:] + r[:1]):
                extrude(b, seg_quad((x0, y0), (x1, y1), 0.3), Z_STREET, Z_STREET + 2.0)
        elif m == "坛":
            steps = 3 if h >= 8 else (2 if h >= 5 else 1)
            for k in range(steps):
                sc = 1.0 - 0.25 * k
                b.box((x - ew * sc / 2, y - ns * sc / 2, Z_STREET), (x + ew * sc / 2, y + ns * sc / 2, Z_STREET + h * (k + 1) / steps))
        elif m == "塔":
            tiers = 9 if h >= 70 else 13                    # 判断：繁塔初建九层、铁塔十三层
            r0 = ew / 2
            for k in range(tiers):
                z0 = Z_STREET + h * k / tiers
                rk = r0 * (1.0 - 0.45 * k / tiers)
                b.poly_solid([Vector((px, py, z0)) for px, py in octagon((x, y), rk)],
                             [Vector((px, py, z0 + h / tiers * 0.8)) for px, py in octagon((x, y), rk * 0.95)])
                b.poly_solid([Vector((px, py, z0 + h / tiers * 0.8)) for px, py in octagon((x, y), rk * 1.25)],
                             [Vector((px, py, z0 + h / tiers)) for px, py in octagon((x, y), rk * 0.9)])
        elif m == "苑":
            gx = int(ew // 25)
            gy = int(ns // 25)
            for i in range(gx):
                for j in range(gy):
                    if rng.random() < 0.6:
                        px, py = x - ew / 2 + 12.5 + 25 * i, y - ns / 2 + 12.5 + 25 * j
                        b.cyl(px, py, Z_STREET, Z_STREET + h - 3.0, 0.3, 6)
                        b.ball((px, py, Z_STREET + h - 3.0), 3.0)
        elif m == "冈":
            b.hip(x, y, ew, ns, Z_STREET, h)
        ob = b.finish(f"G_{plan.index}_lm", "G_LANDMARKS", plan.index)
        ob["bj_name"] = lm["name"]
        counts[m] = counts.get(m, 0) + 1
    return counts


def build_palace(world: World) -> int:
    ring = [(float(p[0]), float(p[1])) for p in next(w for w in world.cfg["wall"] if ring_key(w["name"]) == "宫城")["points"]][:4]
    sw, se, ne, nw = ring                       # W11 原始四角；world.rings 里的宫城圈已被 Place D 改道成六点
    cx = sum(p[0] for p in ring) / 4
    cy = sum(p[1] for p in ring) / 4
    ax = v2sub(((ne[0] + nw[0]) / 2, (ne[1] + nw[1]) / 2), ((sw[0] + se[0]) / 2, (sw[1] + se[1]) / 2))
    ay = (ax[0] / v2len(ax), ax[1] / v2len(ax))
    axx = (ay[1], -ay[0])
    lms = [(float(lm["xy"][0]), float(lm["xy"][1])) for lm in world.cfg["landmark"]]
    rng = random.Random(103)
    b = Batch()
    n = 0
    # 2026-09-15 follow-up 007（bg0 宫城里殿阁成片）：由三列 × 六排改为 60 × 45 m 网格铺满宫城，中轴殿更大
    for gx in range(-300, 301, 60):
        for gy in range(-250, 251, 45):
            px, py = cx + axx[0] * gx + ay[0] * gy, cy + axx[1] * gx + ay[1] * gy
            if not point_in_poly((px, py), ring) or any(v2len(v2sub((px, py), q)) < 70.0 for q in lms) \
               or rng.random() < 0.2 or in_any_place((px, py), 30.0):
                continue
            w_, d_, h_ = (46.0, 24.0, 14.0) if gx == 0 else (rng.choice((22.0, 28.0, 34.0)), 16.0, rng.choice((8.0, 10.0)))
            house(b, (px, py), axx, ay, (w_, d_, h_), "B")
            n += 1
    b.finish("G_103_palace_halls", "G_LANDMARKS", 103)
    NOTES.append(f"G 宫城内殿宇：{n} 座体块（⚠️ C 判断：60 × 45 m 网格铺满宫城，避开 W11 地标 70 m；形制归 W8）")
    return n


class KeepIndex:
    """keep-out 多边形的格网索引：逐栋判断，而不是整块街区一碰就丢（follow-up 007：旧做法沿街沿河沿墙留出大片空地）。"""

    def __init__(self, polys: list[list[Pt]], tile: float = 300.0) -> None:
        self.polys, self.tile = polys, tile
        self.grid: dict[tuple[int, int], list[int]] = {}
        for k, poly in enumerate(polys):
            xs, ys = [q[0] for q in poly], [q[1] for q in poly]
            for i in range(int(min(xs) // tile), int(max(xs) // tile) + 1):
                for j in range(int(min(ys) // tile), int(max(ys) // tile) + 1):
                    self.grid.setdefault((i, j), []).append(k)

    def hits(self, quad: list[Pt]) -> bool:
        xs, ys = [q[0] for q in quad], [q[1] for q in quad]
        cands = {k for i in range(int(min(xs) // self.tile), int(max(xs) // self.tile) + 1)
                 for j in range(int(min(ys) // self.tile), int(max(ys) // self.tile) + 1) for k in self.grid.get((i, j), [])}
        return any(sat_overlap(quad, self.polys[k]) for k in cands)


def house_quad(c: Pt, u: Pt, n: Pt, dims: tuple[float, float, float]) -> list[Pt]:
    lx, ly, _h = dims
    return [(c[0] + u[0] * a + n[0] * d, c[1] + u[1] * a + n[1] * d)
            for a, d in ((-lx / 2, -ly / 2), (lx / 2, -ly / 2), (lx / 2, ly / 2), (-lx / 2, ly / 2))]


BLOCK_RIVER_PAD, BLOCK_WALL_PAD, BLOCK_GATE_PAD = 6.0, 12.0, 45.0

# ── 城内肌理参数（follow-up 008：降密、去整齐、大小高低有别）────────────────────────────────────────────
# 取值依据见 city_plan.md §8「城内肌理」；S ＝ 有史料支撑，J ＝ 判断
FABRIC = {
    "superblock": 300.0,          # S/J：「每坊巷三百步许有军巡铺屋一所」≈465 m，大街区取 300 m 再按 BSP 切小
    "jitter_deg": 11.0,           # J：巷线角度抖动 ±5–15°（research w12 §f）
    "lot_area": (1200.0, 9000.0), # J：细分到的地块面积；另有 8% 地块不再细分（大院 / 营地 / 园圃）
    "lane_choices": (0.0, 0.0, 2.5, 3.0, 4.0, 6.0),   # J：普通巷 2–4 m、大巷 4–6 m、共墙 0
    "dens_inner": 0.68,           # S*：里城 0.6–0.75（1021 年里城户密度约为外城 3.5 倍）
    "dens_outer_es": 0.42,        # S*：外城中部东、南 0.35–0.5（城东左厢 26 800 户）
    "dens_outer_nw": 0.22,        # S：外城中部北、西 0.15–0.3（城北左厢 4 000 户；城西营区）
    "dens_wallside": 0.10,        # J：外城距城墙 500 m 内 0.05–0.15（菜地 / 池塘 / 草场 / 零星草屋）
    "wallside_band": 500.0,
    "street_boost": 0.35, "street_decay": 60.0,   # S*：繁华沿街 60 m 内 ≈ 1.0（清明上河图：密度沿街沿河一层进深）
    "river_boost": 0.25, "river_decay": 60.0,
    "city_centre": (-100.0, 1050.0),
}
# 地块类型权重（dense ≈ 里城 / 干道边，sparse ≈ 城墙边）；shops 另按离街距离加权，barracks 另按偏西北加权
LOT_MIX = {
    #            dense  sparse
    "shops":     (0.10, 0.00),   # 前店后宅 1–5 间（S*：临街店铺以 3 间最多）
    "row":       (0.42, 0.25),   # 1–3 间小屋，院子 / 房廊里成排（S*：「团转盖屋，向背聚居，谓之院子」）
    "courtyard": (0.22, 0.10),   # 一至三进院落（J）
    "compound":  (0.06, 0.03),   # 府第 / 官署 / 寺观 / 正店大院（S*：按面积占建成区约 30%）
    "huts":      (0.10, 0.25),   # 草屋棚屋，越近城墙越多（J）
    "garden":    (0.08, 0.30),   # 园圃 / 池塘 / 空地
    "barracks":  (0.02, 0.07),   # 军营（S：外城西、北为主，占外城面积 10–15%）
}


def split_lots(x0: float, x1: float, y0: float, y1: float, rng: random.Random, out: list[tuple[float, float, float, float]]) -> None:
    """大街区递归二分成大小不一的地块（BSP），巷宽随机、有的地块共墙。"""
    lo, hi = FABRIC["lot_area"]
    area = (x1 - x0) * (y1 - y0)
    if area <= rng.uniform(lo, hi) or min(x1 - x0, y1 - y0) < 18.0 or (area < 25000.0 and rng.random() < 0.08):
        out.append((x0, x1, y0, y1))
        return
    lane = rng.choice(FABRIC["lane_choices"])
    r = rng.uniform(0.3, 0.7)
    if (x1 - x0) >= (y1 - y0):
        m = x0 + (x1 - x0) * r
        split_lots(x0, m - lane / 2, y0, y1, rng, out)
        split_lots(m + lane / 2, x1, y0, y1, rng, out)
    else:
        m = y0 + (y1 - y0) * r
        split_lots(x0, x1, y0, m - lane / 2, rng, out)
        split_lots(x0, x1, m + lane / 2, y1, rng, out)


def build_blocks(world: World, keys: tuple[str, ...]) -> tuple[int, int]:
    outer, inner_ring, palace = world.rings["外城"], world.rings["里城"], world.rings["宫城"]
    keep = list(world.keepout)
    for pts, wd in world.rivers.values():
        keep += [seg_quad(a, b, wd / 2 + BLOCK_RIVER_PAD, 3.0) for a, b in zip(pts, pts[1:])]
    for w in world.cfg["wall"]:
        ring = world.rings[ring_key(w["name"])]
        keep += [seg_quad(a, ring[(i + 1) % len(ring)], float(w["base_m"]) / 2 + BLOCK_WALL_PAD, BLOCK_WALL_PAD) for i, a in enumerate(ring)]
    keep += [octagon(tuple(g["xy"]), BLOCK_GATE_PAD) for g in world.cfg["gate"]]
    keep += [place_poly(p, 15.0) for p in PLACES]
    idx = KeepIndex(keep)
    streets = [[(float(q[0]), float(q[1])) for q in st["points"]] for st in world.cfg["street"]]
    rivers = [pts for pts, _wd in world.rivers.values()]
    barrack_st = [[(float(q[0]), float(q[1])) for q in st["points"]] for st in world.cfg["street"] if "封丘门" in st["name"]]
    yujie = [(float(q[0]), float(q[1])) for st in world.cfg["street"] if st["name"].startswith("御街") for q in st["points"]]

    def dist_lines(p: Pt, lines: list[list[Pt]]) -> float:
        return min((dist_point_seg(p, a, b) for ln in lines for a, b in zip(ln, ln[1:])), default=1e9)

    def es_score(p: Pt) -> float:
        cx0, cy0 = FABRIC["city_centre"]
        return max(0.0, min(1.0, 0.5 + (p[0] - cx0) / 7000.0 - (p[1] - cy0) / 7000.0))

    def density(p: Pt) -> tuple[float, float, float]:
        """返回（占用概率, dense 权重 0..1, 沿街系数 0..1）。"""
        sp = math.exp(-dist_lines(p, streets) / FABRIC["street_decay"])
        if point_in_poly(p, inner_ring):
            base = FABRIC["dens_inner"]
        else:
            mid = FABRIC["dens_outer_nw"] + (FABRIC["dens_outer_es"] - FABRIC["dens_outer_nw"]) * es_score(p)
            dw = min(dist_point_seg(p, q, outer[(k + 1) % len(outer)]) for k, q in enumerate(outer))
            t = min(1.0, dw / FABRIC["wallside_band"])
            base = FABRIC["dens_wallside"] + (mid - FABRIC["dens_wallside"]) * t
        d = base + FABRIC["street_boost"] * sp + FABRIC["river_boost"] * math.exp(-dist_lines(p, rivers) / FABRIC["river_decay"])
        d = max(0.04, min(0.95, d))
        dense_w = max(0.0, min(1.0, (d - FABRIC["dens_wallside"]) / (FABRIC["dens_inner"] + FABRIC["street_boost"] - FABRIC["dens_wallside"])))
        return d, dense_w, sp

    fr = Frame(0.0, 0.0, FRAMES["C"].rot_deg)
    loc = [fr.local(*q) for q in outer]
    SB = FABRIC["superblock"]
    made, boxes = 0, 0
    counts: dict[str, int] = {}
    for i in range(int(min(q[0] for q in loc) // SB), int(max(q[0] for q in loc) // SB) + 1):
        for j in range(int(min(q[1] for q in loc) // SB), int(max(q[1] for q in loc) // SB) + 1):
            lcx, lcy = (i + 0.5) * SB, (j + 0.5) * SB
            c = fr.world(lcx, lcy)
            corners = [fr.world(lcx + a, lcy + d) for a, d in ((-SB / 2, -SB / 2), (SB / 2, -SB / 2), (SB / 2, SB / 2), (-SB / 2, SB / 2))]
            if not any(point_in_poly(q, outer) for q in corners + [c]):
                continue
            # 走廊闸门的粗筛：整块大街区都在走廊外就整块跳过（省掉 BSP 切地块与
            # 上万次 keep-out 查询）。细筛在 house() 里逐栋做 —— 这里只是快进。
            if CORRIDOR is not None and all(CORRIDOR.level(q) is None for q in corners + [c]):
                continue
            idx_n = 10001 + made
            rng = random.Random(idx_n)
            ang = math.radians(FRAMES["C"].rot_deg + rng.uniform(-FABRIC["jitter_deg"], FABRIC["jitter_deg"]))
            u, n = (math.cos(ang), math.sin(ang)), (-math.sin(ang), math.cos(ang))
            near_yujie = min(dist_point_seg(c, a, b2) for a, b2 in zip(yujie, yujie[1:])) < B_CORRIDOR_YUJIE if len(yujie) > 1 else False
            level = "B" if near_yujie or v2len(v2sub(c, (FRAMES["B"].x, FRAMES["B"].y))) < B_RADIUS_S36 else "C"
            lots: list[tuple[float, float, float, float]] = []
            hb = SB / 2 - 4.0                       # 大街区之间留一条 8 m 的街
            split_lots(-hb, hb, -hb, hb, rng, lots)
            bt, walls, yard, water, trees = Batch(), Batch(), Batch(), Batch(), Batch()
            n_b = {"h": 0, "w": 0, "y": 0, "p": 0, "t": 0}

            def W(x: float, y: float) -> Pt:
                return (c[0] + u[0] * x + n[0] * y, c[1] + u[1] * x + n[1] * y)

            def ok_quad(q: list[Pt]) -> bool:
                return all(point_in_poly(pp, outer) for pp in q) and not any(point_in_poly(pp, palace) for pp in q) and not idx.hits(q)

            def bld(x: float, y: float, lx: float, ly: float, h: float, face: int = 1, along_x: bool = True) -> None:
                wu, wn = (u, n) if along_x else (n, (-u[0], -u[1]))
                if face < 0:
                    wn = (-wn[0], -wn[1])
                    wu = (-wu[0], -wu[1])
                pc = W(x, y)
                if not ok_quad(house_quad(pc, wu, wn, (lx, ly, h))):
                    return
                house(bt, pc, wu, wn, (lx, ly, h), level)
                n_b["h"] += 1

            def wall_rect(x0: float, x1: float, y0: float, y1: float, gate_side: int) -> None:
                t = 0.5
                segs = [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]
                for si, (a, b) in enumerate(segs):
                    if si == gate_side:
                        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
                        pieces = [(a, (mx - (b[0] - a[0]) * 0.08, my - (b[1] - a[1]) * 0.08)), ((mx + (b[0] - a[0]) * 0.08, my + (b[1] - a[1]) * 0.08), b)]
                    else:
                        pieces = [(a, b)]
                    for pa, pb in pieces:
                        q = seg_quad(W(*pa), W(*pb), t / 2)
                        if ok_quad(q):
                            extrude(walls, q, Z_STREET, Z_STREET + 2.6)
                            n_b["w"] += 1

            def tree(x: float, y: float, hgt: float) -> None:
                pc = W(x, y)
                if idx.hits(octagon(pc, 2.0)) or not point_in_poly(pc, outer):
                    return
                r = hgt * 0.3
                trees.cyl(pc[0], pc[1], Z_STREET, Z_STREET + hgt - r, 0.25, 6)
                trees.ball((pc[0], pc[1], Z_STREET + hgt - r), r)
                n_b["t"] += 1

            for (x0, x1, y0, y1) in lots:
                lw, ld = x1 - x0, y1 - y0
                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                occ, dw, sp = density(W(cx, cy))
                if rng.random() > occ:
                    kind = "garden"
                else:
                    wts = {k: a * dw + b * (1 - dw) for k, (a, b) in LOT_MIX.items() if k != "garden"}
                    wts["shops"] += 0.55 * sp
                    if point_in_poly(W(cx, cy), inner_ring):
                        wts["barracks"] = 0.0
                    else:
                        wts["barracks"] *= 1.0 + 2.0 * (1.0 - es_score(W(cx, cy)))
                        if barrack_st and dist_lines(W(cx, cy), barrack_st) < 350.0:
                            wts["barracks"] += 0.25
                    if lw * ld < 3500.0:
                        wts["compound"] = 0.0
                    tot = sum(wts.values())
                    r = rng.uniform(0.0, tot)
                    kind = "row"
                    for k, v in wts.items():
                        r -= v
                        if r <= 0:
                            kind = k
                            break
                counts[kind] = counts.get(kind, 0) + 1
                along_x = lw >= ld
                L, D = (lw, ld) if along_x else (ld, lw)          # L 沿地块长边，D 进深
                def P(a: float, b: float) -> tuple[float, float]:  # 地块局部（a 沿长边，b 沿进深，原点地块中心）
                    return (cx + a, cy + b) if along_x else (cx + b, cy + a)
                face = 1 if rng.random() < 0.5 else -1
                if kind == "garden":
                    sub = rng.random()
                    if sub < 0.45 and lw * ld > 600:
                        q = [W(x0 + 2, y0 + 2), W(x1 - 2, y0 + 2), W(x1 - 2, y1 - 2), W(x0 + 2, y1 - 2)]
                        if ok_quad(q):
                            extrude(yard, q, Z_STREET, Z_STREET + 0.05)
                            n_b["y"] += 1
                    elif sub < 0.6 and lw * ld > 2000:
                        q = [W(cx - lw * 0.3, cy - ld * 0.3), W(cx + lw * 0.3, cy - ld * 0.3), W(cx + lw * 0.3, cy + ld * 0.3), W(cx - lw * 0.3, cy + ld * 0.3)]
                        if ok_quad(q):
                            extrude(water, q, Z_STREET - 0.4, Z_STREET + 0.02)
                            n_b["p"] += 1
                    for _ in range(min(5, int(lw * ld / 1500)) + rng.randint(0, 2)):   # 园圃 / 空地里的树按地块大小，别种成林子
                        if rng.random() < 0.7:
                            tree(rng.uniform(x0 + 2, x1 - 2), rng.uniform(y0 + 2, y1 - 2), rng.uniform(6.0, 11.0))
                    if rng.random() < 0.3:                           # 菜园边看园的小屋
                        bld(*P(rng.uniform(-L / 3, L / 3), D / 2 - 3.0), 4.0, 3.5, 3.6, face, along_x)
                elif kind == "huts":
                    for _ in range(max(1, int(L * D / 140))):
                        if rng.random() < 0.6:
                            bld(*P(rng.uniform(-L / 2 + 3, L / 2 - 3), rng.uniform(-D / 2 + 3, D / 2 - 3)),
                                rng.uniform(3.5, 5.0), rng.uniform(3.5, 4.5), rng.uniform(3.2, 4.0), rng.choice((1, -1)), along_x)
                    if rng.random() < 0.5:
                        tree(cx + rng.uniform(-lw / 3, lw / 3), cy + rng.uniform(-ld / 3, ld / 3), rng.uniform(6.0, 9.0))
                elif kind in ("row", "shops"):
                    shop = kind == "shops"
                    for side in (1, -1) if D > 24 else (face,):
                        s0 = -L / 2
                        while s0 < L / 2 - 4:
                            bays = rng.choice((1, 1, 2, 2, 3)) if not shop else rng.choice((1, 2, 2, 3, 3, 4, 5))
                            wbld = bays * rng.uniform(3.1, 4.4)
                            if s0 + wbld > L / 2:
                                break
                            depth = rng.uniform(9.0, 13.0) if shop else rng.uniform(5.5, 8.5)
                            two = rng.random() < (0.4 if sp > 0.5 else 0.06) if shop else rng.random() < 0.02
                            h = rng.uniform(7.5, 9.5) if two else rng.uniform(4.3, 6.2)   # S*：全城单层约九成，两层集中在繁华沿街
                            if shop and sp > 0.6 and rng.random() < 0.012:
                                h = rng.uniform(11.0, 13.0)               # 三层只给正店（全城 72 户）
                            # 临街要紧凑：宋代街屋是**共墙成排**的（「屋宇雄壮，门面广阔」），
                            # 原来 12% 空位 + 四成概率留 1.5–3 m 空当，渲出来是一颗颗独立小房。
                            # 现在沿街热闹处几乎不留缝（sp 越高越密），背街才留巷口与空地。
                            skip = 0.03 + 0.16 * (1.0 - sp)
                            if rng.random() > skip:
                                bld(*P(s0 + wbld / 2, side * (D / 2 - depth / 2 - 0.5)), wbld, depth, h, side, along_x)
                            gaps = ((0.0,) * 7 + (1.2, 2.5)) if sp > 0.45 else ((0.0,) * 3 + (1.5, 3.0))
                            s0 += wbld + rng.choice(gaps)
                    if D > 30 and rng.random() < 0.6:
                        tree(cx + rng.uniform(-lw / 4, lw / 4), cy + rng.uniform(-ld / 4, ld / 4), rng.uniform(7.0, 10.0))
                elif kind in ("courtyard", "compound"):
                    big = kind == "compound"
                    inset = 1.5
                    ax0, ax1 = -L / 2 + inset, L / 2 - inset
                    bd0, bd1 = -D / 2 + inset, D / 2 - inset
                    corners_l = [P(ax0, bd0), P(ax1, bd0), P(ax1, bd1), P(ax0, bd1)]
                    xs, ys = [q[0] for q in corners_l], [q[1] for q in corners_l]
                    wall_rect(min(xs), max(xs), min(ys), max(ys), rng.randrange(4))
                    jin = min(3, max(1, int(D / (18.0 if big else 14.0))))
                    hall_w = min(L * 0.55, rng.uniform(14.0, 22.0) if big else rng.uniform(8.0, 13.0))
                    step = (bd1 - bd0) / (jin + 0.6)
                    for k in range(jin + 1):
                        b = bd0 + step * (k + 0.5)
                        if k == 0:
                            bld(*P(0.0, b), min(hall_w, 9.0), 4.5, rng.uniform(4.5, 5.5), 1, along_x)       # 门屋
                            continue
                        hh = (rng.uniform(8.0, 11.0) if big else rng.uniform(5.5, 7.5)) + (1.2 if k == jin else 0.0)
                        bld(*P(0.0, b), hall_w, rng.uniform(9.0, 12.0) if big else rng.uniform(7.0, 9.0), hh, 1, along_x)
                        for sx in (-1, 1):                                               # 厢房
                            if rng.random() < 0.8:
                                bld(*P(sx * (hall_w / 2 + 5.0), b - step * 0.45), min(step * 0.7, 12.0), 4.5, rng.uniform(4.2, 5.5), sx, not along_x)
                    for _ in range(rng.randint(1, 4 if big else 2)):
                        tree(*P(rng.uniform(ax0 + 3, ax1 - 3), rng.uniform(bd0 + 3, bd1 - 3)), rng.uniform(8.0, 13.0))
                elif kind == "barracks":
                    b = -D / 2 + 6.0
                    while b < D / 2 - 6.0:
                        bld(*P(0.0, b), max(12.0, L - 10.0), 7.0, rng.uniform(5.0, 6.0), 1, along_x)
                        b += 16.0
            if n_b["h"]:
                ob = bt.finish(f"G_{idx_n}_blk", "G_BLOCKS", idx_n)
                ob["bj_level"] = level
                boxes += n_b["h"]
            else:
                bt.bm.free()
            for batch, tag, cnt in ((walls, "yardwalls", n_b["w"]), (yard, "garden", n_b["y"]), (water, "pond_water", n_b["p"]), (trees, "trees", n_b["t"])):
                if cnt:
                    batch.finish(f"G_{idx_n}_{tag}", "G_YARDS", idx_n)
                else:
                    batch.bm.free()
            made += 1
    NOTES.append("G 城内肌理（follow-up 008）：地块类型计数 " + "、".join(f"{k} {v}" for k, v in sorted(counts.items())) + f"；房 {boxes}")
    return made, boxes


def build_suburbs(world: World, keys: tuple[str, ...]) -> tuple[int, int]:
    """东水门外关厢 + 汴河两岸郊外（S01 低飞走廊）；只建外城以东（判断：其余城外不入镜）。

    2026-09-19 重做（用户：「城门外的建筑规划也不理想，拍出来像劣质动画」）。原来三条都反了：
      · **每 14 m 抽一个随机型号、两排、行距 5 m 的独立盒子**——站在裸土上，没有街、没有连排，
        低空掠过时就是一地积木。真实的关厢是**共墙连排的店面直接压着河岸大道**
        （《清明上河图》最挤的一段就在东水门外），所以改用城内 row/shops 那一套：
        开间 3.1–4.4 m、1–4 开间一户、进深 8–13 m、缝几乎为 0。
      · **密度写反了**：真实是越靠城门越密、楼越高。sp 现在按「离护龙河外岸多远」衰减，
        两层房只出现在近城那几百米。
      · **`离城墙 140 m 内不建`**——那恰好是相机压得最低的最后 6 秒，于是飞过的是一片
        保证空无一物的场地。现在建到护龙河外岸 +10 m 为止。
    精度档不在这里定：`house()` 里 CORRIDOR 会按 city_plan §8.2 的半径带覆写（rule 4g ④）。
    """
    pts, wd = world.rivers[next(k for k in world.rivers if k.startswith("汴河"))]
    outer = world.rings["外城"]
    ocx = sum(p[0] for p in outer) / len(outer)
    wcfg = next(x for x in world.cfg["wall"] if ring_key(x["name"]) == "外城")
    moat_out = float(wcfg["base_m"]) / 2 + float(wcfg["moat_offset_m"]) + float(wcfg["moat_width_m"])
    made, boxes, trees = 0, 0, 0
    acc = 0.0
    chunk, chunk_i = Batch(), 0
    tb, rd = Batch(), Batch()
    rng = random.Random(20001)
    ROAD_W, BANK = 8.0, 2.5                  # 水边 2.5 m 土坡 + 8 m 河岸大道，街面压着路沿
    FRONT = wd / 2 + BANK + ROAD_W
    # 关厢要尽量铺到城门根下：原来 `in_any_place(p, 40)` 把门外 160 m 整块让掉，而 Place B 的足迹
    # 本身就有 120 m、且 B 只建墙 / 门 / 码头 / 护龙河、不建房。余量收到 0——**但不能真的进 B**：
    # 「全城层在 Place 足迹内让位」是硬不变式（Place 的地面是开了洞的，城层房子摆进去就浮在洞上）。
    # B 足迹内那一段关厢属于 B 自己的活，要建就加 city_plan 的 Place B 表行，不能从城层伸进去。
    keep = [lm_rect(lm, 6.0) for lm in world.cfg["landmark"]] + moat_quads(world)
    keep += [place_poly(pl, 18.0 if pl != "B" else 0.0) for pl in PLACES]
    for wl in world.cfg["wall"]:
        rg = world.rings[ring_key(wl["name"])]
        keep += [seg_quad(q, rg[(i + 1) % len(rg)], float(wl["base_m"]) / 2 + 12.0, 12.0) for i, q in enumerate(rg)]
    idx = KeepIndex(keep)

    def d_wall(q: Pt) -> float:
        return min(dist_point_seg(q, r, outer[(i + 1) % len(outer)]) for i, r in enumerate(outer))

    for a, b2 in zip(pts, pts[1:]):
        d = v2sub(b2, a)
        ln = v2len(d)
        tu = (d[0] / ln, d[1] / ln)
        tn = (-tu[1], tu[0])
        for side in (-1.0, 1.0):
            nn = (tn[0] * side, tn[1] * side)
            s = 0.0
            while s < ln:
                p0 = (a[0] + tu[0] * s, a[1] + tu[1] * s)
                dw = d_wall(p0)
                if p0[0] < ocx or point_in_poly(p0, outer) or dw < moat_out + 6.0:
                    s += 12.0
                    continue
                sp = max(0.08, math.exp(-max(0.0, dw - moat_out) / 320.0))     # 越靠城门越繁华
                bays = rng.choice((1, 2, 2, 3, 3, 4)) if sp > 0.45 else rng.choice((1, 1, 2, 2, 3))
                lx = bays * rng.uniform(3.1, 4.4)
                if s + lx > ln:
                    break
                ly = rng.uniform(8.0, 13.0) if sp > 0.4 else rng.uniform(5.5, 8.5)
                two = rng.random() < 0.34 * sp
                h = rng.uniform(7.4, 9.2) if two else rng.uniform(4.3, 6.2)
                c = (p0[0] + tu[0] * lx / 2 + nn[0] * (FRONT + ly / 2),
                     p0[1] + tu[1] * lx / 2 + nn[1] * (FRONT + ly / 2))
                if idx.hits(house_quad(c, tu, (-nn[0], -nn[1]), (lx, ly, h))):
                    s += lx
                    continue
                if rng.random() > 0.05 + 0.30 * (1.0 - sp):                     # 沿街几乎不留缝
                    house(chunk, c, tu, (-nn[0], -nn[1]), (lx, ly, h), "A")
                    boxes += 1
                    if rng.random() < 0.55 * sp:                                # 第二进：背街一排，矮一档
                        ly2 = rng.uniform(5.0, 8.0)
                        c2 = (c[0] + nn[0] * (ly / 2 + 3.0 + ly2 / 2), c[1] + nn[1] * (ly / 2 + 3.0 + ly2 / 2))
                        house(chunk, c2, tu, (-nn[0], -nn[1]), (lx, ly2, rng.uniform(3.9, 5.4)), "A")
                        boxes += 1
                elif rng.random() < 0.5:                                        # 空当种柳，别露裸地
                    tp = (p0[0] + nn[0] * (wd / 2 + 1.2), p0[1] + nn[1] * (wd / 2 + 1.2))
                    tb.cyl(tp[0], tp[1], Z_STREET, Z_STREET + 4.5, 0.2, 6)
                    tb.ball((tp[0], tp[1], Z_STREET + 4.5), 2.2)
                    trees += 1
                gaps = ((0.0,) * 7 + (1.2, 2.5)) if sp > 0.45 else ((0.0,) * 3 + (1.5, 3.5))
                step = lx + rng.choice(gaps)
                p1 = (p0[0] + tu[0] * step, p0[1] + tu[1] * step)
                extrude(rd, [(p0[0] + nn[0] * (wd / 2 + BANK), p0[1] + nn[1] * (wd / 2 + BANK)),
                             (p1[0] + nn[0] * (wd / 2 + BANK), p1[1] + nn[1] * (wd / 2 + BANK)),
                             (p1[0] + nn[0] * FRONT, p1[1] + nn[1] * FRONT),
                             (p0[0] + nn[0] * FRONT, p0[1] + nn[1] * FRONT)],
                        Z_STREET - 0.05, Z_STREET + STREET_H)
                s += step
                acc += step
                if acc >= 280.0:
                    acc = 0.0
                    if chunk.bm.verts:
                        chunk.finish(f"G_{20001 + chunk_i}_suburb", "G_SUBURBS", 20001 + chunk_i)
                        chunk_i += 1
                        made += 1
                    else:
                        chunk.bm.free()
                    chunk = Batch()
    if chunk.bm.verts:
        chunk.finish(f"G_{20001 + chunk_i}_suburb", "G_SUBURBS", 20001 + chunk_i)
        made += 1
    else:
        chunk.bm.free()
    tb.finish("G_20000_suburb_willows", "G_SUBURBS", 20000)
    rd.finish("G_20500_suburb_riverroad", "G_STREETS", 20500)
    NOTES.append(f"G 关厢与郊外（东水门—虹桥汴河两岸）：{made} 段、{boxes} 户共墙街面、{trees} 棵柳；"
                 f"密度随离城门距离衰减，建到护龙河外岸 +10 m")
    return made, boxes


class HouseChunks:
    """城外成片房子分块成若干网格物件（每块 ≤ 600 栋），树另成一个物件（look pass 按名字 `_trees` 认树）。"""

    def __init__(self, base: int, tag: str) -> None:
        self.base, self.tag, self.i, self.count, self.houses = base, tag, 0, 0, 0
        self.b = Batch()
        self.trees = Batch()
        self.n_trees = 0

    def house(self, c: Pt, u: Pt, n: Pt, dims: tuple[float, float, float]) -> None:
        house(self.b, c, u, n, dims, "B")
        self.count += 1
        self.houses += 1
        if self.count >= 600:
            self.flush()

    def tree(self, p: Pt, h: float, r: float) -> None:
        self.trees.cyl(p[0], p[1], Z_STREET, Z_STREET + h - r, 0.25, 6)
        self.trees.ball((p[0], p[1], Z_STREET + h - r), r)
        self.n_trees += 1

    def flush(self) -> None:
        if self.count:
            self.b.finish(f"G_{self.base + self.i}_{self.tag}", "G_SUBURBS", self.base + self.i)
            self.i += 1
        else:
            self.b.bm.free()
        self.b, self.count = Batch(), 0

    def finish(self) -> None:
        self.flush()
        self.b.bm.free()
        if self.n_trees:
            self.trees.finish(f"G_{self.base + 999}_{self.tag}_trees", "G_SUBURBS", self.base + 999)
        else:
            self.trees.bm.free()


def outside_keep(world: World, river_pad: float, place_pad: float) -> KeepIndex:
    # 城外不用城内的 world.keepout（街道 +3 m 会把紧贴出城大道的第一排房全挡掉）：只避地标、池、窄街宽
    keep = [lm_rect(lm, 6.0) for lm in world.cfg["landmark"]] + moat_quads(world) + [place_poly(p, place_pad) for p in PLACES]
    for st in world.cfg["street"]:
        sp = [(float(q[0]), float(q[1])) for q in st["points"]]
        keep += [seg_quad(a, b, float(st["width_m"]) / 2 + 1.0) for a, b in zip(sp, sp[1:])]
    for pts, wd in world.rivers.values():
        keep += [seg_quad(a, b, wd / 2 + river_pad, 3.0) for a, b in zip(pts, pts[1:])]
    for w in world.cfg["wall"]:
        ring = world.rings[ring_key(w["name"])]
        keep += [seg_quad(a, ring[(i + 1) % len(ring)], float(w["base_m"]) / 2 + 12.0, 12.0) for i, a in enumerate(ring)]
    return KeepIndex(keep)


SUBURB_ROAD_LEN, SUBURB_ROAD_W = 1200.0, 12.0   # follow-up 011：郊区收窄（用户：郊区尤其要小，应该很快就进城）


def build_gate_suburbs(world: World, keys: tuple[str, ...]) -> tuple[int, int]:
    """外城每座旱门外的关厢（bg0：城门外沿出城大道成街、护龙河外沿城一带房屋）；follow-up 007。

    判断（无 W11 数据，C）：出城道路长 2.4 km、宽 12 m、微弯；两侧三排房，密度随离城距离 e^(−d/650) 衰减；
    门两侧沿护龙河外 ±350 m 两排；前 900 m 随机横巷；道路两侧成行柳。水门、Place 足迹内的门不做。
    """
    outer = world.rings["外城"]
    ccw = ring_ccw(outer)
    w = next(x for x in world.cfg["wall"] if ring_key(x["name"]) == "外城")
    base = float(w["base_m"]) / 2
    moat_in = base + float(w["moat_offset_m"])
    moat_out = moat_in + float(w["moat_width_m"])
    dims = unit_dims(keys)
    idx = outside_keep(world, 8.0, 25.0)
    chunks = HouseChunks(21001, "guanxiang")
    roads = Batch()
    bridges = Batch()
    gates = 0
    x0, x1, y0, y1 = G_EXTENT

    def put(pc: Pt, wu: Pt, wn: Pt, k: str) -> None:
        q = house_quad(pc, wu, wn, dims[k])
        if any(point_in_poly(p, outer) for p in q) or idx.hits(q) or not all(x0 + 100 < p[0] < x1 - 100 and y0 + 100 < p[1] < y1 - 100 for p in q):
            return
        chunks.house(pc, wu, wn, dims[k])

    for gi, g in enumerate(world.cfg["gate"]):
        form = g["form"]
        if g["ring"] != "外城" or ("水门" in form and "旱门" not in form) or in_any_place(tuple(g["xy"]), 80.0):
            continue
        i, s0 = gate_segment(g, world)
        a, b = outer[i], outer[(i + 1) % len(outer)]
        u, out, _ = seg_frame(a, b, ccw)
        c = (a[0] + u[0] * s0, a[1] + u[1] * s0)
        rng = random.Random(5000 + gi)
        pts: list[Pt] = []
        lat = 0.0
        for k in range(9):
            d = base + SUBURB_ROAD_LEN * k / 8
            lat += rng.uniform(-1.0, 1.0) * 30.0 * k / 8
            p = (c[0] + out[0] * d + u[0] * lat, c[1] + out[1] * d + u[1] * lat)
            if pts and (any(sat_overlap(seg_quad(pts[-1], p, SUBURB_ROAD_W / 2 + 6.0), place_poly(pl, 30.0)) for pl in PLACES)
                        or not (x0 + 200 < p[0] < x1 - 200 and y0 + 200 < p[1] < y1 - 200)):
                break
            pts.append(p)
        if len(pts) < 3:
            continue
        gates += 1
        for pa, pb in zip(pts, pts[1:]):
            extrude(roads, seg_quad(pa, pb, SUBURB_ROAD_W / 2), Z_STREET - 0.05, Z_STREET + STREET_H)
        for pm in pts[1:-1]:
            extrude(roads, octagon(pm, SUBURB_ROAD_W / 2 / math.cos(math.pi / 8)), Z_STREET - 0.05, Z_STREET + STREET_H)
        bq0 = (c[0] + out[0] * (moat_in - 6.0), c[1] + out[1] * (moat_in - 6.0))
        bq1 = (c[0] + out[0] * (moat_out + 6.0), c[1] + out[1] * (moat_out + 6.0))
        extrude(bridges, seg_quad(bq0, bq1, 4.0), Z_STREET + 0.2, Z_STREET + 0.7)
        dist = 0.0
        for pa, pb in zip(pts, pts[1:]):
            dv = v2sub(pb, pa)
            ln = v2len(dv)
            t = (dv[0] / ln, dv[1] / ln)
            nn = (-t[1], t[0])
            s = 0.0
            while s < ln:
                k = rng.choice(keys)
                lx, ly, h = dims[k]
                along = dist + s
                dens = max(0.12, math.exp(-max(0.0, along - moat_out - 300.0) / 1000.0))
                for side in (-1.0, 1.0):
                    for row in range(4):
                        if rng.random() > dens * (1.0 - 0.15 * row):
                            continue
                        off = SUBURB_ROAD_W / 2 + 2.0 + ly / 2 + row * (ly + 5.0)
                        pc = (pa[0] + t[0] * (s + lx / 2) + nn[0] * side * off, pa[1] + t[1] * (s + lx / 2) + nn[1] * side * off)
                        put(pc, t, (-nn[0] * side, -nn[1] * side), k)
                    if rng.random() < 0.35 and along < 1600.0:
                        tp = (pa[0] + t[0] * s + nn[0] * side * (SUBURB_ROAD_W / 2 + 1.0), pa[1] + t[1] * s + nn[1] * side * (SUBURB_ROAD_W / 2 + 1.0))
                        if not idx.hits(octagon(tp, 2.0)):
                            chunks.tree(tp, rng.uniform(7.0, 10.0), 2.6)
                if along < 900.0 and rng.random() < lx / 150.0:
                    for side in (-1.0, 1.0):
                        lane_len = rng.uniform(60.0, 150.0)
                        bx0 = pa[0] + t[0] * s + nn[0] * side * (SUBURB_ROAD_W / 2 + 37.5)
                        by0 = pa[1] + t[1] * s + nn[1] * side * (SUBURB_ROAD_W / 2 + 37.5)
                        e = 0.0
                        while e < lane_len:
                            k2 = rng.choice(keys)
                            lx2, ly2, _h2 = dims[k2]
                            for lside in (-1.0, 1.0):
                                if rng.random() < 0.8:
                                    pc = (bx0 + nn[0] * side * (e + lx2 / 2) + t[0] * lside * (4.0 + ly2 / 2),
                                          by0 + nn[1] * side * (e + lx2 / 2) + t[1] * lside * (4.0 + ly2 / 2))
                                    put(pc, (nn[0] * side, nn[1] * side), (-t[0] * lside, -t[1] * lside), k2)
                            e += lx2 + 1.0
                s += lx + rng.choice((0.0, 1.0, 3.0))
            dist += ln
        along = -650.0
        while along < 650.0:
            k = rng.choice(keys)
            lx, ly, h = dims[k]
            if abs(along) > SUBURB_ROAD_W / 2 + 8.0:
                for row in range(3):
                    if rng.random() < (0.9 - 0.2 * row) * max(0.35, 1.0 - abs(along) / 900.0):
                        off = moat_out + 10.0 + ly / 2 + row * (ly + 5.0)
                        pc = (c[0] + u[0] * (along + lx / 2) + out[0] * off, c[1] + u[1] * (along + lx / 2) + out[1] * off)
                        put(pc, u, (-out[0], -out[1]), k)
            along += lx + rng.choice((0.0, 1.0, 2.0))
    # 外廓散居：护龙河外沿整圈城墙一带零散房屋（bg0 城墙外一圈都有人家），门前关厢以外密度较低
    for si, a in enumerate(outer):
        b = outer[(si + 1) % len(outer)]
        u, out, ln = seg_frame(a, b, ccw)
        rng = random.Random(7000 + si)
        s = 0.0
        while s < ln:
            k = rng.choice(keys)
            lx, ly, h = dims[k]
            for row in range(3):
                if rng.random() < 0.32 - 0.08 * row:
                    off = moat_out + 12.0 + ly / 2 + row * (ly + 6.0) + rng.uniform(0.0, 25.0)
                    put((a[0] + u[0] * (s + lx / 2) + out[0] * off, a[1] + u[1] * (s + lx / 2) + out[1] * off), u, (-out[0], -out[1]), k)
            s += lx + rng.uniform(1.0, 8.0)
    roads.finish("G_4090_suburb_roads", "G_STREETS", 4090)
    bridges.finish("G_4091_moat_bridges", "G_STREETS", 4091)
    chunks.finish()
    NOTES.append(f"G 关厢（follow-up 007，C 判断）：{gates} 座城门外成街，{chunks.houses} 栋、{chunks.n_trees} 棵行道柳、出城路 {SUBURB_ROAD_LEN:g} m")
    return gates, chunks.houses


HAMLET_CELL = 700.0
HAMLET_BELT = 2600.0     # follow-up 011：村落只留在城墙外 0.8–2.6 km 的一圈里，郊野不再铺满 19 × 18 km


def build_hamlets(world: World, keys: tuple[str, ...]) -> tuple[int, int]:
    """田野里的村落（bg0 / bg8：城外麦田间散布小村、土墙草顶、村边有树）；follow-up 007，C 判断：850 m 格网 70% 有村。"""
    outer = world.rings["外城"]
    dims = unit_dims(keys)
    small = [k for k in keys if dims[k][0] <= 8.5] or list(keys)
    idx = outside_keep(world, 25.0, 60.0)
    chunks = HouseChunks(31001, "hamlet")
    x0, x1, y0, y1 = G_EXTENT
    n_h = 0
    for i in range(int(x0 // HAMLET_CELL), int(x1 // HAMLET_CELL) + 1):
        for j in range(int(y0 // HAMLET_CELL), int(y1 // HAMLET_CELL) + 1):
            rng = random.Random(30000 + i * 977 + j)
            if rng.random() > 0.7:
                continue
            cx = (i + 0.5) * HAMLET_CELL + rng.uniform(-280.0, 280.0)
            cy = (j + 0.5) * HAMLET_CELL + rng.uniform(-280.0, 280.0)
            if not (x0 + 300 < cx < x1 - 300 and y0 + 300 < cy < y1 - 300) or point_in_poly((cx, cy), outer) \
               or not (800.0 <= min(dist_point_seg((cx, cy), q, outer[(k + 1) % len(outer)]) for k, q in enumerate(outer)) <= HAMLET_BELT):
                continue
            yaw = rng.uniform(0.0, math.pi / 2)
            u, n = (math.cos(yaw), math.sin(yaw)), (-math.sin(yaw), math.cos(yaw))
            taken: set[tuple[int, int]] = set()
            placed = 0
            for _ in range(rng.randint(8, 22)):
                gx, gy = rng.randint(-4, 4), rng.randint(-3, 3)
                if (gx, gy) in taken:
                    continue
                taken.add((gx, gy))
                k = rng.choice(small)
                face = n if rng.random() < 0.5 else (-n[0], -n[1])
                pc = (cx + u[0] * gx * 16.0 + n[0] * gy * 18.0, cy + u[1] * gx * 16.0 + n[1] * gy * 18.0)
                if idx.hits(house_quad(pc, u, face, dims[k])):
                    continue
                chunks.house(pc, u, face, dims[k])
                placed += 1
            if placed:
                n_h += 1
                for _ in range(rng.randint(4, 10)):
                    a = rng.uniform(0.0, 2 * math.pi)
                    r = rng.uniform(70.0, 130.0)
                    tp = (cx + math.cos(a) * r, cy + math.sin(a) * r)
                    if not idx.hits(octagon(tp, 3.0)):
                        chunks.tree(tp, rng.uniform(8.0, 12.0), 3.2)
    chunks.finish()
    NOTES.append(f"G 田间村落（follow-up 007，C 判断）：{n_h} 村、{chunks.houses} 户、{chunks.n_trees} 棵树")
    return n_h, chunks.houses


def build_yujie_extension(world: World) -> int:
    """御街设施从 Place C 北缘延伸到 Place D 南缘（S02 段 2 沿中轴低飞 / S17 长焦，B 级）。

    偏移量只取 Place C 方块 33–36（朱 / 黑杈子、御沟两岸树、御廊），不另写数值；御沟沟槽不再切地面，只建两岸树行。
    """
    f = FRAMES["C"]
    dx, dy = FRAMES["D"].world(0.0, PLACE_RANGE["D"][2])
    y1 = f.local(dx, dy)[1]
    y0 = PLACE_RANGE["C"][3]
    red = float(re.search(rf"x=±({NUM})", row_of("C", 33).where).group(1))
    black = float(re.search(rf"x=±({NUM})", row_of("C", 34).where).group(1))
    dx0, dx1 = span(row_of("C", 35).where, "x")
    gx0, gx1 = span(row_of("C", 36).where, "x")
    z0 = Z_STREET + STREET_H
    for tag, sx in (("E", 1), ("W", -1)):
        b = Batch()
        for xs in (red, black):
            for k in range(int((y1 - y0) / 2.0) + 1):
                wx, wy = f.world(sx * xs, y0 + 2.0 * k)
                b.cbox((wx, wy, z0 + 0.6), (0.15, 0.15, 1.2))
        for xr in (dx0 - 1.2, dx1 + 1.2):
            for k in range(int((y1 - y0) / 6.0)):
                wx, wy = f.world(sx * xr, y0 + 3.0 + 6.0 * k)
                b.cyl(wx, wy, z0, z0 + 2.8, 0.12, 6)
                b.ball((wx, wy, z0 + 2.8), 1.2)
        gallery(b, f, sx, gx0, gx1, y0, y1, z0)
        cut_places(b.finish(f"G_4011_yujie_{tag}", "G_STREETS", 4011))   # 压缩后御街设施会压进开封府 / 相国寺足迹，照街道的规矩让位
    NOTES.append(f"G 御街设施延伸：Place C 北缘（局部 y={y0:g}）→ Place D 南缘（y={y1:.0f}），杈子 / 御沟树 / 御廊按 Place C 方块 33–36 偏移"
                 f"（御街宽取 W11 320 m：黑杈子 ±{black:g}、御廊 ±{gx0:g}…±{gx1:g}）")
    return 2


def gallery(b: Batch, f: Frame, sx: int, gx0: float, gx1: float, y0: float, y1: float, z0: float) -> None:
    """御廊：廊下铺砖台 0.3 + 两排柱（开间 BAY）+ 檐板；f 为坐标系（全城层给 Place C 的 Frame、Place 内给恒等）。"""
    floor = [f.world(sx * gx0, y0), f.world(sx * gx1, y0), f.world(sx * gx1, y1), f.world(sx * gx0, y1)]
    extrude(b, floor, z0, z0 + 0.3)
    for xc in (gx0 + 0.3, gx1 - 0.3):
        for k in range(int((y1 - y0) / BAY) + 1):
            wx, wy = f.world(sx * xc, max(y0 + 0.15, min(y1 - 0.15, y0 + BAY * k)))
            b.cbox((wx, wy, z0 + 0.3 + 1.75), (0.3, 0.3, 3.5))
    roof = [f.world(sx * (gx0 - 0.4), y0), f.world(sx * gx1, y0), f.world(sx * gx1, y1), f.world(sx * (gx0 - 0.4), y1)]
    extrude(b, roof, z0 + 3.8, z0 + 4.1)


# ── 布局层 ③ 物件布点（follow-up 016；口径与代价见 city_plan §12）────────────────────
# 这是「物件清单」到「场景 blend」之间那根线：沿已有的河 / 街折线撒实例，
# 白模没到货就撒同尺寸替身盒（`resolve_asset` 自动降级），到货了自动换成真网格。
SCATTER_COUNTS: dict[str, int] = {}
REJECTS: dict[str, dict[str, int]] = {}


def load_scatter(md: str) -> list[dict]:
    sec = md.split("## 12. 物件布点", 1)
    if len(sec) != 2:
        return []
    m = re.search("```toml" + chr(10) + "(.*?)```", sec[1], re.S)
    if not m:
        raise PlanError("city_plan.md §12 缺 toml 块")
    return tomllib.loads(m.group(1)).get("scatter", [])


def scatter_line(world: World, along: dict) -> list[Pt]:
    kind, name = along["kind"], along["name"]
    if kind == "river":
        pts = [(float(a), float(b)) for a, b in next(r for r in world.cfg["river"] if r["name"] == name)["points"]]
        s0, s1 = float(along.get("s0", 0.0)), float(along.get("s1", 1e9))
        out, acc = [], 0.0
        for a, b in zip(pts, pts[1:]):
            ln = v2len(v2sub(b, a))
            if acc + ln > s0 and acc < s1:
                out += [a, b]
            acc += ln
        return out
    if kind == "street":
        st = next((x for x in world.cfg["street"] if x["name"] == name), None)
        if st is None:
            raise PlanError(f"§12 街「{name}」不在 W11 [[street]] 里")
        return [(float(a), float(b)) for a, b in st["points"]]
    if kind == "place":
        # Place 局部坐标里的一条直线——寺内 / 府前 / 瓦子里这类东西没有河街可沿，
        # 但它们都属于某个 Place。坐标依旧一个都不新写：只用 Place 自己的
        # frame 与 PLACE_RANGE（§8 铁律），`at` 是另一轴上的局部偏移。
        if name not in FRAMES:
            raise PlanError(f"§12 place「{name}」不是 Place（可用 {sorted(FRAMES)}）")
        f = FRAMES[name]
        x0, x1, y0, y1 = PLACE_RANGE[name]
        at = float(along.get("at", 0.0))
        if along.get("axis", "y") == "x":
            a0, a1 = float(along.get("s0", x0)), float(along.get("s1", x1))
            return [f.world(a0, at), f.world(a1, at)]
        a0, a1 = float(along.get("s0", y0)), float(along.get("s1", y1))
        return [f.world(at, a0), f.world(at, a1)]
    raise PlanError(f"§12 along.kind 只支持 river / street / place，见到 {kind}")


def place_object(key: str, level: str, c: Pt, yaw_deg: float, z: float, tag: str, n: int) -> None:
    proto = get_proto(key, level)
    f = proto.asset.front()
    yaw = math.radians(yaw_deg) - math.atan2(f.y, f.x)
    ob = bpy.data.objects.new(f"SC_{key}_{n:04d}", None)
    ob.instance_type, ob.instance_collection = "COLLECTION", proto.collection
    ob.location = (c[0], c[1], z)
    ob.rotation_euler = (0.0, 0.0, yaw)
    ob["bj_asset"], ob["bj_proxy"], ob["bj_scatter"] = key, int(proto.is_proxy), tag
    collection("G_OBJECTS" + ("_PROXY" if proto.is_proxy else "")).objects.link(ob)


def build_scatter(world: World, md: str) -> dict[str, int]:
    specs = load_scatter(md)
    if not specs:
        return {}
    street_keep = {id(q) for q in world.keepout_street}
    keep_nostreet = [q for q in world.keepout if id(q) not in street_keep]

    base_keep: list[list[Pt]] = []
    for pts, wd in world.rivers.values():
        base_keep += [seg_quad(a, b, wd / 2 + BLOCK_RIVER_PAD, 3.0) for a, b in zip(pts, pts[1:])]
    for w in world.cfg["wall"]:
        ring = world.rings[ring_key(w["name"])]
        base_keep += [seg_quad(a, ring[(i + 1) % len(ring)], float(w["base_m"]) / 2 + BLOCK_WALL_PAD, BLOCK_WALL_PAD)
                      for i, a in enumerate(ring)]
    base_keep += [octagon(tuple(g["xy"]), BLOCK_GATE_PAD) for g in world.cfg["gate"]]
    # Place 足迹默认剔除（里面有自己的详细几何）；`in_place = "H"` 的 spec 撒的正是
    # "属于那个 Place 的东西"（寺前门枕、府前拴马石、瓦子里的长凳），对它要做两件事：
    #   ① 摘掉 Place 足迹这一层；
    #   ② **连同落在该足迹里的全城层 keep-out 一起摘掉** —— 那些街区/河/墙的禁区四边形
    #      是在 Place 挖洞之前建的，几何早已让位，禁区却还留着。不摘，Place 里一个都撒不出来
    #      （2026-09-17 实测：相国寺书市 60 个只落 5 个、瓦子看棚 0 个，全被这层挡着）。
    place_keep = [place_poly(pl, 8.0) for pl in PLACES]
    idx_place = KeepIndex(place_keep)

    def dry_index(on_street: bool, in_place: str | None) -> KeepIndex:
        keep = list(keep_nostreet if on_street else world.keepout)
        if in_place is None:
            return KeepIndex(keep + base_keep + place_keep)
        foot = place_poly(in_place, 0.0)
        return KeepIndex([q for q in keep + base_keep if not sat_overlap(q, foot)])

    idx_cache: dict[tuple[bool, str | None], KeepIndex] = {}
    made: dict[str, int] = {}
    n = 0
    for spec in specs:
        key = spec["key"]
        line = scatter_line(world, spec["along"])
        rng = random.Random(int(spec.get("seed", 1)))
        off0, off1 = (float(v) for v in spec["offset"])
        step = float(spec["spacing"])
        jit = spec.get("jitter", {})
        jp, jy = float(jit.get("pos", 0.0)), float(jit.get("yaw", 0.0))
        cross = spec.get("face") == "cross"
        on_street = bool(spec.get("on_street"))
        # in_place = true 时取 along.name（place 模式）；也可以直接写 Place 字母
        in_place: str | None = None
        if spec.get("in_place"):
            v = spec["in_place"]
            in_place = v if isinstance(v, str) else str(spec["along"].get("name", ""))
            if in_place not in PLACES:
                raise PlanError(f"§12 {key} 的 in_place 认不出 Place：{in_place!r}")
        if (on_street, in_place) not in idx_cache:
            idx_cache[(on_street, in_place)] = dry_index(on_street, in_place)
        idx_dry = idx_cache[(on_street, in_place)]
        water = bool(spec.get("in_water"))
        cap = int(spec.get("max", 400))
        cnt = 0
        # 撒不出来的时候要说得出为什么：三道剔除各自记一笔（2026-09-17）。
        # 「0 个」不带原因等于让下一个人重新猜一遍——今晚已经在这上面栽过一次。
        rej = {"走廊外": 0, "Place内": 0, "禁区": 0}
        for a, b in zip(line, line[1:]):
            d = v2sub(b, a)
            ln = v2len(d)
            if ln < 1e-6:
                continue
            u = (d[0] / ln, d[1] / ln)
            nrm = (-u[1], u[0])
            head = math.degrees(math.atan2(d[1], d[0]))
            t = step * 0.5
            while t < ln and cnt < cap:
                for side in (1, -1):
                    if cnt >= cap:
                        break
                    off = side * rng.uniform(off0, off1)
                    px = a[0] + u[0] * t + nrm[0] * off + rng.uniform(-jp, jp)
                    py = a[1] + u[1] * t + nrm[1] * off + rng.uniform(-jp, jp)
                    pt = (px, py)
                    if CORRIDOR is not None and CORRIDOR.level(pt) is None:
                        rej["走廊外"] += 1
                        continue
                    if water:
                        if in_place is None and idx_place.hits(octagon(pt, 2.0)):
                            rej["Place内"] += 1
                            continue
                    else:
                        if idx_dry.hits(octagon(pt, 1.5)):
                            rej["禁区"] += 1
                            continue
                    yaw = head + (90.0 if cross else 0.0) + (180.0 if side < 0 and cross else 0.0)
                    place_object(key, "B", pt, yaw + rng.uniform(-jy, jy),
                                 Z_WATER if water else Z_STREET, spec.get("name", key), n)
                    n += 1
                    cnt += 1
                t += step
        label = f"{key} {spec.get('name', '')}".strip()
        made[label] = cnt
        if cnt < int(spec.get("max", 400)) * 0.5:
            REJECTS[label] = {k: v for k, v in rej.items() if v}
        SCATTER_COUNTS[key] = SCATTER_COUNTS.get(key, 0) + cnt
    if REJECTS:
        NOTES.append("G 物件布点·撒不满的原因（拿到不足一半上限的 spec）："
                     + "；".join(f"{k} {v}" for k, v in REJECTS.items()))
    NOTES.append("G 物件布点（follow-up 016，city_plan §12）："
                 + "；".join(f"{k} {v} 个" for k, v in made.items())
                 + f"　合计 {sum(made.values())} 个实例")
    return made



def build_global_layer(md: str) -> dict[str, object]:
    cfg = load_w11()
    global CORRIDOR
    CORRIDOR = load_corridor(md, cfg)
    plans, keys = parse_global_plan(md)
    world = world_setup(cfg)
    ponds = [lm_rect(lm) for lm in cfg["landmark"] if plans[lm["name"]].method == "池"]
    build_ground(world, ponds)
    build_walls(world)
    n_gates = build_gates(world)
    n_streets = build_streets(world)
    n_yujie = build_yujie_extension(world)
    lm_counts = build_landmarks(world, plans, keys)
    n_halls = build_palace(world)
    n_blocks, n_boxes = build_blocks(world, keys)
    n_sub, n_sub_boxes = build_suburbs(world, keys)
    n_gate_sub, n_gate_houses = build_gate_suburbs(world, keys)
    n_hamlets, n_hamlet_houses = build_hamlets(world, keys)
    scat = build_scatter(world, md)          # follow-up 016：物件清单 → 场景 blend 的那根线
    counts: dict[str, object] = {
        "城墙": len(cfg["wall"]), "城门（建 / 表）": f"{n_gates} / {len(cfg['gate'])}", "河道": len(cfg["river"]),
        "街道": n_streets, "御街设施延伸": n_yujie, "地标建法": lm_counts, "宫内殿宇": n_halls, "街区": n_blocks, "街区单元盒": n_boxes,
        "郊外段": n_sub, "郊外单元盒": n_sub_boxes, "关厢城门": n_gate_sub, "关厢房": n_gate_houses,
        "田间村落": n_hamlets, "村落房": n_hamlet_houses,
        "走廊内建房（按级）": dict(sorted(CORRIDOR.built.items())) if CORRIDOR else {},
        "走廊外砍掉的房": CORRIDOR.culled if CORRIDOR else 0,
        "物件布点": scat, "物件实例合计": sum(scat.values())}
    if CORRIDOR:
        NOTES.append("G 航线走廊（follow-up 014，city_plan §8.2）：线半径 %g / %g / %g m，"
                     "Place 半径 %g / %g / %g m；走廊内建房 %d 栋（A %d / B %d / C %d），走廊外砍掉 %d 栋"
                     % (*CORRIDOR.r, *CORRIDOR.rp, sum(CORRIDOR.built.values()), CORRIDOR.built.get("A", 0),
                        CORRIDOR.built.get("B", 0), CORRIDOR.built.get("C", 0), CORRIDOR.culled))
    NOTES.append("G 全城层计数：" + "；".join(f"{k} {v}" for k, v in counts.items()))
    return counts


# ── 布局层 ② 细节 Place（city_plan.md §2；新 Place 加一张表 + 在 PLACE_LAYERS 注册）──────
ROWS: list[Row] = []
FOOTPRINTS: dict[str, list[tuple[float, float, float, float]]] = {p: [] for p in PLACES}


def row_of(place: str, block: int) -> Row:
    for r in ROWS:
        if r.place == place and r.block == block:
            return r
    raise PlanError(f"Place {place} 找不到方块 {block}")


def span(text: str, label: str) -> tuple[float, float]:
    m = re.search(rf"{label}\s*±?({NUM})…±?({NUM})", text)
    if not m:
        raise PlanError(f"找不到「{label} a…b」：{text[:60]}")
    return float(m.group(1)), float(m.group(2))


def hits_footprint(place: str, x0: float, x1: float, y0: float, y1: float) -> bool:
    return any(x0 < fx1 and x1 > fx0 and y0 < fy1 and y1 > fy0 for fx0, fx1, fy0, fy1 in FOOTPRINTS[place])


def tree_row(name: str, col: str, row: int, pts: list[tuple[float, float, float]], h: float, crown_r: float,
             trunk_r: float) -> None:
    b = Batch()
    for x, y, z0 in pts:
        b.cyl(x, y, z0, z0 + h - crown_r, trunk_r, 6)
        b.ball((x, y, z0 + h - crown_r), crown_r)
    b.finish(name, col, row)


def a_river(r: Row) -> None:
    r.need("y -10…10", "河宽 20")
    x0, x1, _, _ = PLACE_RANGE["A"]
    solid_box("A_17_river_water", "A_RIVER", (x0, -RIVER_W / 2, Z_WATER - 0.05), (x1, RIVER_W / 2, Z_WATER), 17)
    solid_box("A_17_river_bed", "A_RIVER", (x0, -RIVER_W / 2, -2.0), (x1, RIVER_W / 2, Z_BED), 17)


def a_slope(r: Row) -> None:
    r.need("土坡 |y| 10…13", "z 0→2")
    x0, x1, _, _ = PLACE_RANGE["A"]
    for tag, s in (("N", 1), ("S", -1)):
        b = Batch()
        b.prism_x(x0, x1, [(s * 10, Z_WATER), (s * 10, Z_BED), (s * 13, Z_BED), (s * 13, Z_STREET)])
        b.finish(f"A_18_slope_{tag}", "A_STREET", 18)


def s_street(r: Row) -> None:
    if r.place == "A":
        r.need("街 y ±13…±19", "街宽 6")
        x0, x1, _, _ = PLACE_RANGE["A"]
        for tag, s in (("N", 1), ("S", -1)):
            solid_box(f"A_18_street_{tag}", "A_STREET", (x0, min(s * 13, s * 19), Z_BED), (x1, max(s * 13, s * 19), Z_STREET), 18)
            solid_box(f"A_00_plot_{tag}", "A_STREET", (x0, min(s * 19, s * 30), Z_STREET - 0.5), (x1, max(s * 19, s * 30), Z_STREET))
        return
    r.need("x -40…40", "y 12…120", "中央 80 m")              # ⚠️ 截宽：御街阔二百余步只建中央 80 m（route.009）
    dx0, dx1 = span(row_of("C", 35).where, "x")
    y0, y1 = 12.0, 120.0
    for i, (a, b2) in enumerate(((-40.0, -dx1), (-dx0, dx0), (dx1, 40.0))):
        solid_box(f"C_32_yujie_{i}", "C_STREET", (a, y0, 1.0), (b2, y1, Z_STREET), 32)


def a_dock(r: Row) -> None:
    r.need("码头 (48, 12)", "码头 24 × 4", "z=+2 石岸 + 木栈")
    m = re.search(r"码头 \(([-\d.]+), ([-\d.]+)\)", r.where)
    cx, cy = float(m.group(1)), float(m.group(2))
    lx, ly = r.sizes[1]
    solid_box("A_12_quay", "A_DOCK", (cx - lx / 2, cy - ly / 2 + 1.0, Z_BED), (cx + lx / 2, cy + ly / 2, Z_STREET), 12)
    solid_box("A_12_timber_step", "A_DOCK", (cx - lx / 2, cy - ly / 2, Z_BED), (cx + lx / 2, cy - ly / 2 + 1.0, 1.0), 12)
    FOOTPRINTS["A"].append((cx - lx / 2, cx + lx / 2, cy - ly / 2, cy + ly / 2))


def a_granary(r: Row) -> None:
    r.need("仓 (49, 27) 门朝南", "仓 18 × 12 × 8")          # ⚠️ 仓的形制无图（job.001）：纯体块 + 悬山
    m = re.search(r"仓 \(([-\d.]+), ([-\d.]+)\)", r.where)
    cx, cy = float(m.group(1)), float(m.group(2))
    lx, ly, h = r.sizes[0]
    b = Batch()
    b.box((cx - lx / 2, cy - ly / 2, Z_STREET), (cx + lx / 2, cy + ly / 2, Z_STREET + h - 3.0))
    b.gable_x(cx - lx / 2, cx + lx / 2, cy - ly / 2, cy + ly / 2, Z_STREET + h - 3.0, Z_STREET + h)
    b.finish("A_12_granary", "A_DOCK", 12)
    FOOTPRINTS["A"].append((cx - lx / 2, cx + lx / 2, cy - ly / 2, cy + ly / 2))


def a_poles(r: Row) -> None:
    r.need("高 8", "径 0.3", "横木 1.0")                     # 表木功能不口播：doubt.005 / bridge.007
    x, y = r.center
    b = Batch()
    b.cyl(x, y, Z_STREET, Z_STREET + 8.0, 0.15)
    b.cbox((x, y, Z_STREET + 7.9), (1.0, 0.12, 0.12))
    b.cbox((x, y, Z_STREET + 8.1), (0.3, 0.12, 0.25))
    b.finish(f"A_13_{r.index}_biaomu", "A_POLES", 13)


def s_willow(r: Row) -> None:
    if r.place == "A":
        r.need("y=±12", "x 每 8 m 一棵", "桥头 ±8 m 内不放", "高 6–8", "冠径 4")
        for tag, s in (("N", 1), ("S", -1)):
            pts = []
            for k in range(-9, 10):
                x = 8.0 * k
                if abs(x) <= 8.0 or hits_footprint("A", x - 2, x + 2, s * 12 - 2, s * 12 + 2):
                    continue
                pts.append((x, s * 12.0, Z_STREET * (12.0 - 10.0) / 3.0))
            b = Batch()
            for i, (x, y, z0) in enumerate(pts):
                h = 6.0 + 2.0 * random.Random(14000 + (i if s > 0 else 100 + i)).random()
                b.cyl(x, y, z0, z0 + h - 2.0, 0.2, 6)
                b.ball((x, y, z0 + h - 2.0), 2.0)
            b.finish(f"A_14_willow_{tag}", "A_TREES", 14)
        return
    if r.place == "E":
        r.need("y=-16", "x 每 8 m", "高 7", "冠径 4")
        pts = [(-56.0 + 8.0 * k, -17.0, Z_STREET) for k in range(14)]
        tree_row("E_76_willows", "E_TREES", 76, pts, 7.0, 2.0, 0.2)
        return
    if r.place == "J" and r.block == 116:
        r.need("(-22, -150)", "高 12", "冠径 9")
        x, y = r.center
        tree_row("J_116_big_willow", "J_TREES", 116, [(x, y, Z_STREET)], 12.0, 4.5, 0.45)
        return
    if r.place == "J":
        r.need("x=±8", "y -390…-12", "每 8 m", "高 10", "冠径 6")
        y0, y1 = span(r.where, "y")
        pts = [(s * 8.0, y0 + 8.0 * k, Z_STREET) for s in (-1, 1) for k in range(int((y1 - y0) / 8.0) + 1)
               if not hits_footprint("J", s * 8.0 - 1.5, s * 8.0 + 1.5, y0 + 8.0 * k - 1.5, y0 + 8.0 * k + 1.5)]
        tree_row("J_113_willows", "J_TREES", 113, pts, 10.0, 3.0, 0.25)
        return
    r.need("墙内 x=-8", "y 每 8 m", "高 7")
    NOTES.append(f"方块 27：表内 x={TREE_B_X_TABLE:g} 落在底宽 {WALL_BASE_W:g} m 的城墙体内（墙脚 x=−17，gate.004 ai_draft），"
                 f"树线建在 x={TREE_B_X_BUILT:g}；避开门道 / 马道 / 客店 / 河")
    pts = [(TREE_B_X_BUILT, -40.0 + 8.0 * k, Z_STREET) for k in range(11)
           if not hits_footprint("B", TREE_B_X_BUILT - 2, TREE_B_X_BUILT + 2, -42 + 8.0 * k, -38 + 8.0 * k)
           and abs(-40.0 + 8.0 * k) > 13.0]
    tree_row("B_27_trees", "B_TREES", 27, pts, 7.0, 2.0, 0.2)


def b_ground() -> None:
    x0, x1, _, y1 = PLACE_RANGE["B"]
    solid_box("B_00_river_water", "B_RIVER", (x0, -RIVER_W / 2, Z_WATER - 0.05), (x1, RIVER_W / 2, Z_WATER))
    solid_box("B_00_river_bed", "B_RIVER", (x0, -RIVER_W / 2, -2.0), (x1, RIVER_W / 2, Z_BED))
    mx0, mx1 = span(row_of("B", 24).where, "x")
    for tag, s in (("N", 1), ("S", -1)):
        ya, yb = sorted((s * RIVER_W / 2, s * y1))
        solid_box(f"B_00_ground_in_{tag}", "B_STREET", (x0, ya, Z_BED), (mx0, yb, Z_STREET))
        solid_box(f"B_00_ground_out_{tag}", "B_STREET", (mx1, ya, Z_BED), (x1, yb, Z_STREET))


def gate_dims() -> tuple[float, float, float, float]:
    r = row_of("B", 21)
    (dw, dh), (px, py, ph), _tower = r.sizes
    return dw, dh, px, py


def b_water_gate(r: Row) -> None:
    r.need("水门净跨 22", "城台高 8.7", "楼 歇山 12 × 8 × 6")
    _dw, _dh, px, _py = gate_dims()
    top = Z_STREET + WALL_H
    ly, lx, th = r.sizes[-1]
    solid_box("B_20_lintel", "B_GATES", (-px / 2, -WATER_GATE_SPAN / 2, SLUICE_Z[1]), (px / 2, WATER_GATE_SPAN / 2, top), 20)
    solid_box("B_20_sluice_raised", "B_GATES", (px / 2, -WATER_GATE_SPAN / 2, SLUICE_Z[0]), (px / 2 + 0.25, WATER_GATE_SPAN / 2, SLUICE_Z[1]), 20)
    # 2026-09-18 照 bg2-1 对账：锚点图里**水门上是一座大城楼**（面阔比城台窄不了多少、出檐很深、
    # 带一圈栏杆平座），两侧旱门只是小门洞；而我们把三座楼做成了一样大的小盒子，一眼就是模型。
    # W11 的 12 × 8 × 6 是楼身净尺寸，这里按图把**主楼放大到 1.45 倍**、出檐再挑出 1.2 m。
    # 2026-09-19 用户定调「城门要再雄伟壮丽一点」：原来是「城台 8.7 m ＋ 单檐小楼 7.2 m」，
    # 在 48 m 宽的河面上压不住场，低空迎面飞来时城楼只占画面很小一块。三处放大，都是真实做法：
    #   ① **城台比两侧城墙再高出一截**（真实城门台座就是抬起来的，这是「门」区别于「墙」的第一眼），
    #   ② **单檐改重檐**（腰檐 + 上檐，中间夹一层平座），楼身加高加阔，面阔占满台座，
    #   ③ **台座边缘加垛口**，让轮廓线不再是一条平板直线。
    PLINTH = 3.6                                                  # 城台高出两侧城墙的量
    ptop = top + PLINTH
    solid_box("B_20_plinth", "B_GATES", (-px / 2 - 0.6, -WATER_GATE_SPAN / 2 - 7.0, top),
              (px / 2 + 0.6, WATER_GATE_SPAN / 2 + 7.0, ptop), 20)
    b = Batch()
    for sx in (-1, 1):                                            # 垛口：台座两长边各一排
        n = 13
        for k in range(n):
            wy = -(WATER_GATE_SPAN / 2 + 6.2) + (WATER_GATE_SPAN + 12.4) * k / (n - 1)
            b.cbox((sx * (px / 2 + 0.3), wy, ptop + 0.6), (1.1, 1.6, 1.2))
    mw, md = lx * 1.95, ly * 1.75                                 # 面阔/进深：原 1.45 倍再放大
    body = th * 1.55
    b.box((-mw / 2, -md / 2, ptop), (mw / 2, md / 2, ptop + body * 0.52))          # 下层楼身
    b.hip(0.0, 0.0, mw + 3.0, md + 3.0, ptop + body * 0.52, 2.6)                   # 腰檐（出檐 1.5 m）
    for sx in (-1, 1):                                            # 腰檐上的平座栏杆
        for k in range(11):
            wy = -md / 2 + md * k / 10
            b.cbox((sx * (mw / 2 + 0.75), wy, ptop + body * 0.52 + 0.85), (0.12, 0.12, 1.6))
        b.box((sx * (mw / 2 + 0.62), -md / 2, ptop + body * 0.52 + 1.5),
              (sx * (mw / 2 + 0.88), md / 2, ptop + body * 0.52 + 1.65))
    uw, ud = mw * 0.86, md * 0.86
    b.box((-uw / 2, -ud / 2, ptop + body * 0.52 + 1.7), (uw / 2, ud / 2, ptop + body))   # 上层楼身
    b.hip(0.0, 0.0, uw + 3.4, ud + 3.4, ptop + body, 4.2)                          # 上檐：更深的出檐 + 更高的屋面
    b.finish("B_20_tower", "B_GATES", 20)

    # 马道：城台两侧各一道夯土坡道（bg2-1 里是城门最认得出的一笔，我们之前只给旱门做了）
    hb = WALL_BASE_W / 2
    for sy, tag in ((1, "N"), (-1, "S")):
        # 马道要落在**旱门之外**：旱门门洞在 y ±16，坡道压上去就把门洞堵死（QC §4步5 实测抓到）。
        y0 = sy * 26.0
        y1 = y0 + sy * 24.0
        rb = Batch()
        rb.prism_x(-px / 2 - 2.5, -px / 2 + 1.0,
                   sorted([(y0, top), (y0, Z_STREET), (y1, Z_STREET)], key=lambda q: (q[0] * sy, -q[1])))
        rb.finish(f"B_20_madao_{tag}", "B_GATES", 20)
        FOOTPRINTS["B"].append((-px / 2 - 2.5, -px / 2 + 1.0, min(y0, y1), max(y0, y1)))


def b_dry_gate(r: Row) -> None:
    r.need("门洞 4 × 5", "台 14 × 10 × 8.7", "楼 8 × 5 × 5", "马道")
    dw, dh, px, py = gate_dims()
    ty, tx, th = r.sizes[2]
    c = r.center[1]
    s = 1 if c > 0 else -1
    top = Z_STREET + WALL_H
    for i, (ya, yb) in enumerate(((c - py / 2, c - dw / 2), (c + dw / 2, c + py / 2))):
        solid_box(f"B_21_{r.index}_jamb{i}", "B_GATES", (-px / 2, ya, Z_STREET), (px / 2, yb, top), 21)
    solid_box(f"B_21_{r.index}_lintel", "B_GATES", (-px / 2, c - dw / 2, Z_STREET + dh), (px / 2, c + dw / 2, top), 21)
    b = Batch()
    b.box((-tx / 2, c - ty / 2, top), (tx / 2, c + ty / 2, top + th - 2.0))
    b.hip(0.0, c, tx, ty, top + th - 2.0, 2.0)
    b.finish(f"B_21_{r.index}_tower", "B_GATES", 21)
    y_edge = c + s * py / 2
    b = Batch()
    b.prism_x(-px / 2 - 3.0, -px / 2, sorted([(y_edge, top), (y_edge, Z_STREET), (y_edge + s * 18.0, Z_STREET)],
                                             key=lambda p: (p[0] * s, -p[1])))
    b.finish(f"B_21_{r.index}_madao", "B_GATES", 21)
    NOTES.append(f"方块 21：马道＝每座旱门一条，贴墙内侧背河方向（x −10…−7，长 18 m），与夯土墙坡面相交部分埋入墙体（判断）")
    FOOTPRINTS["B"] += [(-px / 2, px / 2, c - py / 2, c + py / 2), (-px / 2 - 3.0, -px / 2, min(y_edge, y_edge + s * 18), max(y_edge, y_edge + s * 18)),
                        (-50.0, -px / 2, c - dw / 2 - 2.0, c + dw / 2 + 2.0)]


def b_wall(r: Row) -> None:
    r.need("y -45…45", "底宽 34", "顶宽 4", "高 8.7")        # ⚠️ gate.004 ai_draft：只用于几何，不进 prompt
    _dw, _dh, _px, py = gate_dims()
    c = abs(row_of("B", 21).center[1])
    hb, ht, top = WALL_BASE_W / 2, WALL_TOP_W / 2, Z_STREET + WALL_H
    prof = [(-hb, Z_BED), (-hb, Z_STREET), (-ht, top), (ht, top), (hb, Z_STREET), (hb, Z_BED)]
    for tag, (ya, yb) in (("N", (c + py / 2, 45.0)), ("S", (-45.0, -c - py / 2))):
        b = Batch()
        b.prism_y(ya, yb, prof)
        b.finish(f"B_22_wall_{tag}", "B_WALL", 22)
        FOOTPRINTS["B"].append((-hb, hb, ya, yb))
    NOTES.append("方块 22：每百步马面按距旱门 ≈150 m 起算，落在本站 ±45 m 范围外 → 0 个（判断）")


def b_guaizi(r: Row) -> None:
    r.need("门外 x 0…47", "y=±14", "高 5", "厚 3")
    _dw, _dh, px, _py = gate_dims()
    x_end = span(row_of("B", 24).where, "x")[0]
    for tag, s in (("N", 1), ("S", -1)):
        ya, yb = sorted((s * (14.0 - GUAIZI_T), s * 14.0))
        solid_box(f"B_23_guaizi_{tag}", "B_WALL", (px / 2, ya, Z_WATER), (x_end, yb, Z_STREET + GUAIZI_H), 23)
    NOTES.append("方块 23：y=±14 取为墙外皮（|y| 11…14）——取中线会压住 4 m 宽的门道与木桥（y 14…18）；x 0…7 在旱门台内，从 x=7 起建，"
                 "止于护龙河内沿（判断：夹岸百余丈的其余段不入镜）")


def b_moat(r: Row) -> None:
    r.need("x 47.1…85.1", "宽 38")                         # ⚠️ 交汇处形制未查（route.001 / gate.003）；位置与宽取 W11（moat_quads 核对）
    x0, x1 = span(r.where, "x")
    _, _, _, y1 = PLACE_RANGE["B"]
    for tag, s in (("N", 1), ("S", -1)):
        ya, yb = sorted((s * RIVER_W / 2, s * y1))
        solid_box(f"B_24_moat_water_{tag}", "B_MOAT", (x0, ya, Z_WATER - 0.05), (x1, yb, Z_WATER), 24)
        solid_box(f"B_24_moat_bed_{tag}", "B_MOAT", (x0, ya, -2.0), (x1, yb, Z_BED), 24)


def b_bridge(r: Row) -> None:
    r.need("长 40 × 宽 4")                                 # ⚠️ 判断值，无 fact_id：跨 38 m 护龙河两端各搭 1 m
    lx, ly = r.sizes[0]
    x, y = r.center
    solid_box(f"B_25_{r.index}_wooden_bridge", "B_MOAT", (x - lx / 2, y - ly / 2, Z_STREET - 0.3), (x + lx / 2, y + ly / 2, Z_STREET), 25)


def c_ground() -> None:
    solid_box("C_00_river_water", "C_RIVER", (-C_D_HALF, -RIVER_W / 2, Z_WATER - 0.05), (C_D_HALF, RIVER_W / 2, Z_WATER))
    solid_box("C_00_river_bed", "C_RIVER", (-C_D_HALF, -RIVER_W / 2, -2.0), (C_D_HALF, RIVER_W / 2, Z_BED))
    solid_box("C_00_bank_N", "C_STREET", (-C_D_HALF, RIVER_W / 2, Z_BED), (C_D_HALF, 12.0, Z_STREET))
    solid_box("C_00_ground_S", "C_STREET", (-C_D_HALF, -80.0, Z_BED), (C_D_HALF, -RIVER_W / 2, Z_STREET))


def c_zhouqiao(r: Row) -> None:
    r.need("长 24 × 宽 30", "桥面 z=+2.6", "桥下密排石柱")       # ⚠️ zhouqiao.002：宽按明桥 30 m
    ly, lx = r.sizes[0]
    if r.zs[0] != ZQ_DECK_Z:
        raise PlanError("方块 30：桥面 z 与常量不符")
    solid_box("C_30_deck", "C_ZHOUQIAO", (-lx / 2, -ly / 2, Z_STREET), (lx / 2, ly / 2, ZQ_DECK_Z), 30)
    b = Batch()
    for i in range(int(lx / 2)):
        for j in range(int(RIVER_W / 2)):
            b.cbox((-lx / 2 + 1.0 + 2.0 * i, -RIVER_W / 2 + 1.0 + 2.0 * j, (Z_BED + Z_STREET) / 2), (0.4, 0.4, Z_STREET - Z_BED))
    b.finish("C_30_piers", "C_ZHOUQIAO", 30)
    b = Batch()
    for sx in (-1, 1):
        b.box((sx * lx / 2 - (0.3 if sx > 0 else 0.0), -ly / 2, ZQ_DECK_Z), (sx * lx / 2 + (0.0 if sx > 0 else 0.3), ly / 2, ZQ_DECK_Z + 1.0))
    for sy in (-1, 1):
        b.prism_x(-lx / 2, lx / 2, sorted([(sy * ly / 2, Z_STREET), (sy * ly / 2, ZQ_DECK_Z), (sy * (ly / 2 + 6.0), Z_STREET)],
                                          key=lambda p: (p[0] * sy, -p[1])))
    b.finish("C_30_rails_ramps", "C_ZHOUQIAO", 30)
    NOTES.append("方块 30：桥面 z=2.6 高出街面 0.6，两端各加 6 m 缓坡（判断）")


def c_stone_walls(r: Row) -> None:
    r.need("河岸 y=±10", "x ±15…±45", "高 3.3", "长 30")        # ⚠️ ai_draft（zhouqiao.001/002），几何用
    x0, x1 = span(r.where, "x")
    for i, (sx, sy) in enumerate(itertools.product((1, -1), (1, -1))):
        ya, yb = sorted((sy * RIVER_W / 2, sy * (RIVER_W / 2 - 0.4)))
        xa, xb = sorted((sx * x0, sx * x1))
        solid_box(f"C_31_{i}_stone_wall", "C_ZHOUQIAO", (xa, ya, Z_STREET - STONE_WALL_H), (xb, yb, Z_STREET), 31)


def c_chazi(r: Row) -> None:
    ref = row_of("C", 33)
    ref.need("y 12…120", "每 2 m 一根", "高 1.2")
    if r.block == 34:
        r.need("同上")
    xs = float(re.search(rf"x=±({NUM})", r.where).group(1))
    y0, y1 = span(ref.where, "y")
    z0 = Z_STREET + (STREET_H if xs > C_D_HALF else 0.0)          # 足迹外的一行立在全城层街面上
    for tag, sx in (("E", 1), ("W", -1)):
        b = Batch()
        for k in range(int((y1 - y0) / 2.0) + 1):
            b.cbox((sx * xs, max(y0 + 0.075, min(y1 - 0.075, y0 + 2.0 * k)), z0 + 0.6), (0.15, 0.15, 1.2))
        b.finish(f"C_{r.block}_chazi_{tag}", "C_CHAZI", r.block)


def c_ditch(r: Row) -> None:
    r.need("x ±14…±17", "宽 3 深 1", "树高 4", "每 6 m")         # 荷叶是长相，不建
    x0, x1 = span(r.where, "x")
    for tag, sx in (("E", 1), ("W", -1)):
        xa, xb = sorted((sx * x0, sx * x1))
        solid_box(f"C_35_ditch_floor_{tag}", "C_DITCH", (xa, 12.0, 0.8), (xb, 120.0, Z_STREET - 1.0), 35)
        pts = [(sx * xr, 15.0 + 6.0 * k, Z_STREET) for xr in (x0 - 1.2, x1 + 1.2) for k in range(18)]
        tree_row(f"C_35_trees_{tag}", "C_DITCH", 35, pts, 4.0, 1.2, 0.12)
    NOTES.append("方块 35：桃李梨杏按御沟两岸各一行（近岸 1.2 m），每 6 m（判断）")


def c_gallery(r: Row) -> None:
    r.need("x ±154…±160", "y 12…120", "进深 6", "檐高 3.5", "开间 4 m 模数")
    x0, x1 = span(r.where, "x")
    y0, y1 = span(r.where, "y")
    for tag, sx in (("E", 1), ("W", -1)):
        b = Batch()
        gallery(b, Frame(0.0, 0.0, 0.0), sx, x0, x1, y0, y1, Z_STREET + STREET_H)
        b.finish(f"C_36_gallery_{tag}", "C_GALLERY", 36)


def c_que(r: Row) -> None:
    lx, ly, h = r.sizes[0]
    x, y = r.center
    solid_box(f"C_37_{r.index}_que", "C_MISC", (x - lx / 2, y - ly / 2, Z_STREET), (x + lx / 2, y + ly / 2, Z_STREET + h), 37)


def c_fire_tower(r: Row) -> None:
    r.need("台 6 × 6 × 10 + 亭 3 × 3 × 3")
    (px, py, ph), (tx, ty, th) = r.sizes
    x, y = r.center
    b = Batch()
    b.box((x - px / 2, y - py / 2, Z_STREET), (x + px / 2, y + py / 2, Z_STREET + ph))
    z = Z_STREET + ph
    for dx, dy in itertools.product((-1, 1), (-1, 1)):
        b.cbox((x + dx * (tx / 2 - 0.1), y + dy * (ty / 2 - 0.1), z + (th - 1.0) / 2), (0.2, 0.2, th - 1.0))
    b.hip(x, y, tx + 0.4, ty + 0.4, z + th - 1.0, 1.0)
    b.finish("C_39_fire_tower", "C_MISC", 39)


def c_well(r: Row) -> None:
    """⚠️ 形制 ai_draft（street.004）：只建方木栏井口，不建辘轳 / 石井圈。"""
    lx, ly, h = r.sizes[0]
    x, y = r.center
    b = Batch()
    for sx in (-1, 1):
        b.box((x + sx * lx / 2 - (0.1 if sx > 0 else 0.0), y - ly / 2, Z_STREET), (x + sx * lx / 2 + (0.0 if sx > 0 else 0.1), y + ly / 2, Z_STREET + h))
        b.box((x - lx / 2 + 0.1, y + sx * ly / 2 - (0.1 if sx > 0 else 0.0), Z_STREET), (x + lx / 2 - 0.1, y + sx * ly / 2 + (0.0 if sx > 0 else 0.1), Z_STREET + h))
    b.finish("C_40_well", "C_MISC", 40)


# ── 细节 Place 公用构件（木构殿屋 / 墙圈 / 台阶 / 栏杆 / 席棚）──────────────────────────
def ground_box(place: str, name: str, x0: float, x1: float, y0: float, y1: float, z: float = Z_STREET) -> None:
    solid_box(f"{place}_00_{name}", f"{place}_GROUND", (x0, y0, Z_BED), (x1, y1, z))


def slab(b: Batch, x0: float, x1: float, y0: float, y1: float, z0: float, z1: float) -> None:
    b.box((min(x0, x1), min(y0, y1), z0), (max(x0, x1), max(y0, y1), z1))


def gable(b: Batch, x0: float, x1: float, y0: float, y1: float, z_eave: float, z_ridge: float, ridge: str) -> None:
    if ridge == "x":
        b.gable_x(x0, x1, y0, y1, z_eave, z_ridge)
    else:
        b.prism_y(y0, y1, [(x0, z_eave), (x1, z_eave), ((x0 + x1) / 2, z_ridge)])


def timber_hall(b: Batch, cx: float, cy: float, lx: float, ly: float, z0: float, col_h: float, roof_h: float, *,
                bays: tuple[int, int] = (3, 2), base_h: float = 0.0, roof: str = "hip", ridge: str = "x",
                walls: tuple[str, ...] = ("N", "E", "W"), door: float = 0.0, overhang: float = 1.2) -> float:
    """木构殿屋：台基 + 周圈柱 + 指定面墙（前面可留门）+ 额枋带 + 屋面；返回檐口 z。前 ＝ −Y。"""
    if base_h > 0:
        slab(b, cx - lx / 2 - 1.0, cx + lx / 2 + 1.0, cy - ly / 2 - 1.0, cy + ly / 2 + 1.0, z0, z0 + base_h)
    zc = z0 + base_h
    xs = [cx - lx / 2 + lx * i / bays[0] for i in range(bays[0] + 1)]
    ys = [cy - ly / 2 + ly * j / bays[1] for j in range(bays[1] + 1)]
    for x in xs:
        for y in ys:
            if x in (xs[0], xs[-1]) or y in (ys[0], ys[-1]):
                b.cyl(x, y, zc, zc + col_h, 0.22, 8)
    t = 0.3
    faces = {"N": (xs[0], xs[-1], ys[-1] - t / 2, ys[-1] + t / 2), "S": (xs[0], xs[-1], ys[0] - t / 2, ys[0] + t / 2),
             "E": (xs[-1] - t / 2, xs[-1] + t / 2, ys[0], ys[-1]), "W": (xs[0] - t / 2, xs[0] + t / 2, ys[0], ys[-1])}
    for w in walls:
        x0, x1, y0, y1 = faces[w]
        if w == "S" and door > 0:
            slab(b, x0, cx - door / 2, y0, y1, zc, zc + col_h)
            slab(b, cx + door / 2, x1, y0, y1, zc, zc + col_h)
            slab(b, cx - door / 2, cx + door / 2, y0, y1, zc + min(col_h - 0.4, 3.2), zc + col_h)
        else:
            slab(b, x0, x1, y0, y1, zc, zc + col_h)
    band = 0.7
    slab(b, xs[0] - 0.3, xs[-1] + 0.3, ys[0] - 0.3, ys[-1] + 0.3, zc + col_h, zc + col_h + band)
    ze = zc + col_h + band
    rx, ry = lx + 2 * overhang, ly + 2 * overhang
    if roof == "hip":
        b.hip(cx, cy, rx, ry, ze, roof_h)
    else:
        gable(b, cx - rx / 2, cx + rx / 2, cy - ry / 2, cy + ry / 2, ze, ze + roof_h, ridge)
    return ze


def ridge_beasts(b: Batch, cx: float, cy: float, half: float, z_ridge: float, axis: str = "x", size: float = 1.0) -> None:
    """正脊 + 两端鸱吻（形状只到「脊端翘起的一块」）。"""
    if axis == "x":
        slab(b, cx - half, cx + half, cy - 0.3 * size, cy + 0.3 * size, z_ridge - 0.2, z_ridge + 0.5 * size)
        for s in (-1, 1):
            b.cbox((cx + s * half, cy, z_ridge + 1.3 * size), (0.6 * size, 1.3 * size, 2.6 * size))
            b.cbox((cx + s * (half + 0.55 * size), cy, z_ridge + 2.3 * size), (0.5 * size, 0.7 * size, 0.9 * size))
    else:
        slab(b, cx - 0.3 * size, cx + 0.3 * size, cy - half, cy + half, z_ridge - 0.2, z_ridge + 0.5 * size)
        for s in (-1, 1):
            b.cbox((cx, cy + s * half, z_ridge + 1.3 * size), (1.3 * size, 0.6 * size, 2.6 * size))


def steps(b: Batch, x0: float, x1: float, y_edge: float, direction: int, z0: float, z1: float, n: int, tread: float = 0.35) -> None:
    """台阶：从 y_edge 向 direction（±1）方向逐级下落；每级是一块实心板。"""
    for k in range(n):
        top = z1 - (z1 - z0) * k / n
        slab(b, x0, x1, y_edge + direction * tread * k, y_edge + direction * tread * (k + 1), z0, top)


def steps_x(b: Batch, y0: float, y1: float, x_edge: float, direction: int, z0: float, z1: float, n: int, tread: float = 0.35) -> None:
    for k in range(n):
        top = z1 - (z1 - z0) * k / n
        slab(b, x_edge + direction * tread * k, x_edge + direction * tread * (k + 1), y0, y1, z0, top)


def railing(b: Batch, pts: list[tuple[float, float]], z0: float, h: float, pitch: float = 1.5) -> None:
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        ln = math.hypot(bx - ax, by - ay)
        n = max(1, int(ln // pitch))
        for k in range(n + 1):
            b.cbox((ax + (bx - ax) * k / n, ay + (by - ay) * k / n, z0 + h / 2), (0.12, 0.12, h))
        q = seg_quad((ax, ay), (bx, by), 0.05)
        extrude(b, q, z0 + h - 0.1, z0 + h)


def wall_ring(b: Batch, x0: float, x1: float, y0: float, y1: float, t: float, z0: float, h: float,
              gaps: list[tuple[str, float, float]]) -> None:
    """矩形墙圈；gaps ＝ (边 N/S/E/W, 开口中心, 开口宽)。"""
    for side, (a0, a1, fixed) in {"S": (x0, x1, y0), "N": (x0, x1, y1), "W": (y0, y1, x0), "E": (y0, y1, x1)}.items():
        cuts = sorted((c - w / 2, c + w / 2) for s, c, w in gaps if s == side)
        cur = a0 - (t / 2 if side in "SN" else 0.0)
        end = a1 + (t / 2 if side in "SN" else 0.0)
        for c0, c1 in cuts + [(end, end)]:
            if c0 > cur:
                if side in "SN":
                    slab(b, cur, c0, fixed - t / 2, fixed + t / 2, z0, z0 + h)
                else:
                    slab(b, fixed - t / 2, fixed + t / 2, cur, c0, z0, z0 + h)
            cur = max(cur, c1)


def mat_shed(b: Batch, cx: float, cy: float, lx: float, ly: float, eave: float, ridge_h: float, ridge: str,
             open_side: str = "", mouth: float = 0.0, walls: bool = True, shell: bool = False) -> None:
    """木杆绑扎、席顶席墙的看棚：周圈杆每 5 m；shell＝屋面做成两块薄坡板（棚内可拍）。"""
    z = Z_STREET
    nx, ny = max(1, round(lx / 5)), max(1, round(ly / 5))
    for i in range(nx + 1):
        for j in range(ny + 1):
            if i in (0, nx) or j in (0, ny):
                b.cyl(cx - lx / 2 + lx * i / nx, cy - ly / 2 + ly * j / ny, z, z + eave, 0.12, 6)
    if walls:
        segs = {"S": (cx - lx / 2, cx + lx / 2, cy - ly / 2, cy - ly / 2), "N": (cx - lx / 2, cx + lx / 2, cy + ly / 2, cy + ly / 2),
                "W": (cx - lx / 2, cx - lx / 2, cy - ly / 2, cy + ly / 2), "E": (cx + lx / 2, cx + lx / 2, cy - ly / 2, cy + ly / 2)}
        for s, (ax, bx, ay, by) in segs.items():
            wh = eave - 1.2
            if s == open_side and mouth > 0:
                if s in "SN":
                    slab(b, ax, cx - mouth / 2, ay - 0.04, ay + 0.04, z, z + wh)
                    slab(b, cx + mouth / 2, bx, ay - 0.04, ay + 0.04, z, z + wh)
                else:
                    slab(b, ax - 0.04, ax + 0.04, ay, cy - mouth / 2, z, z + wh)
                    slab(b, ax - 0.04, ax + 0.04, cy + mouth / 2, by, z, z + wh)
            elif s != open_side:
                slab(b, min(ax, bx) - 0.04, max(ax, bx) + 0.04, min(ay, by) - 0.04, max(ay, by) + 0.04, z, z + wh)
    ze, zr = z + eave, z + eave + ridge_h
    if not shell:
        gable(b, cx - lx / 2 - 0.5, cx + lx / 2 + 0.5, cy - ly / 2 - 0.5, cy + ly / 2 + 0.5, ze, zr, ridge)
        return
    if ridge == "y":
        for s in (-1, 1):
            b.prism_y(cy - ly / 2 - 0.5, cy + ly / 2 + 0.5,
                      [(cx + s * (lx / 2 + 0.5), ze), (cx, zr), (cx, zr + 0.25), (cx + s * (lx / 2 + 0.5), ze + 0.25)])
    else:
        for s in (-1, 1):
            b.prism_x(cx - lx / 2 - 0.5, cx + lx / 2 + 0.5,
                      [(cy + s * (ly / 2 + 0.5), ze), (cy, zr), (cy, zr + 0.25), (cy + s * (ly / 2 + 0.5), ze + 0.25)])


def street_slab(place: str, block: int, x0: float, x1: float, y0: float, y1: float, h: float = 0.08) -> None:
    solid_box(f"{place}_{block}_street", f"{place}_STREET", (x0, y0, Z_STREET), (x1, y1, Z_STREET + h), block)


# ── Place C 方块 42：正店门首（bg5 卡）──────────────────────────────────────────────
def c_zhengdian(r: Row) -> None:
    r.need("主楼 12 × 14 × 9.5", "欢门 高 12.5", "左邻脚店 6 × 8 × 5", "右邻铺面 6 × 8 × 5.5")
    x, y = r.center                                     # 门朝西：店面临 x 小的一侧（街心）
    fx = x - 7.0                                        # 主楼前檐柱线
    b = Batch()
    slab(b, fx - 1.2, x + 7.0, y - 7.0, y + 7.0, Z_STREET, Z_STREET + 0.3)
    steps_x(b, y - 2.5, y + 2.5, fx - 1.2, -1, Z_STREET, Z_STREET + 0.3, 3)
    z1 = Z_STREET + 0.3
    for yy in (y - 7.0, y - 2.3, y + 2.3, y + 7.0):
        b.cyl(fx, yy, z1, z1 + 3.8, 0.2, 8)
    slab(b, fx + 0.1, x + 7.0, y - 7.0, y + 7.0, z1 + 3.8, z1 + 4.3)          # 二层楼板
    slab(b, fx + 1.5, x + 7.0, y - 7.0, y + 7.0, z1, z1 + 3.8)                 # 一层店堂（门里退 1.5 m）
    b.prism_x(fx - 2.4, fx + 0.1, [(y - 7.0, z1 + 3.0), (y + 7.0, z1 + 3.0), (y + 7.0, z1 + 3.2), (y - 7.0, z1 + 3.2)])  # 芦席披檐
    railing(b, [(fx + 0.3, y - 7.0), (fx + 0.3, y + 7.0)], z1 + 4.3, 1.0, 1.0)  # 二层临街栏杆（离地约一丈二）
    slab(b, fx + 1.6, x + 7.0, y - 7.0, y + 7.0, z1 + 4.3, z1 + 7.6)           # 二层阁子一排（吊窗在栏杆后）
    b.prism_y(y - 7.6, y + 7.6, [(fx + 0.5, z1 + 7.6), (x + 7.5, z1 + 7.6), ((fx + x + 8.0) / 2, Z_STREET + 9.5)])
    hz = Z_STREET + 12.5                                # 三层彩楼欢门：长木杆绑扎、镂空，比屋檐高出一人
    gx = fx - 2.8
    for yy in (y - 3.2, y + 3.2):
        b.cbox((gx, yy, (Z_STREET + hz) / 2), (0.22, 0.22, hz - Z_STREET))
        b.cbox((gx + 1.2, yy, (Z_STREET + hz - 2.0) / 2), (0.18, 0.18, hz - 2.0 - Z_STREET))
    for zz in (Z_STREET + 4.2, Z_STREET + 7.6, Z_STREET + 10.8):
        b.cbox((gx, y, zz), (0.18, 7.2, 0.18))
        b.cbox((gx + 0.6, y, zz - 0.6), (1.2, 6.6, 0.12))
    for k in range(7):                                  # 镂空斜撑
        yy = y - 3.0 + k
        b.cbox((gx, yy, Z_STREET + 9.2), (0.08, 0.08, 3.0))
    b.cbox((gx - 0.05, y, Z_STREET + 3.4), (0.12, 2.6, 0.7))                   # 匾
    b.cbox((gx - 0.05, y, Z_STREET + 2.1), (0.05, 2.6, 1.7))                   # 珠帘（一片薄板）
    for k in range(6):                                  # 酒梢桶 × 6，靠墙码
        b.cyl(fx - 0.6, y + 3.6 + 0.55 * k, Z_STREET, Z_STREET + 1.0, 0.24, 10)
    b.finish("C_42_zhengdian", "C_ZHENGDIAN", 42)
    b = Batch()
    for (ny, lx, ly, h, small_gate) in ((y + 11.0, 6.0, 8.0, 5.0, True), (y - 11.0, 6.0, 8.0, 5.5, False)):
        cxn = x - 3.0
        slab(b, cxn - lx / 2 + 1.0, cxn + lx / 2 + 1.0, ny - ly / 2 + 0.2, ny + ly / 2 - 0.2, Z_STREET, Z_STREET + h - 1.6)
        b.prism_y(ny - ly / 2, ny + ly / 2, [(cxn - lx / 2 - 0.4, Z_STREET + h - 1.6), (cxn + lx / 2 + 1.4, Z_STREET + h - 1.6),
                                            (cxn + 0.5, Z_STREET + h)])
        if small_gate:
            for yy in (ny - 2.2, ny + 2.2):
                b.cbox((cxn - lx / 2 - 1.2, yy, Z_STREET + 3.2), (0.16, 0.16, 6.4))
            for zz in (Z_STREET + 3.0, Z_STREET + 6.2):
                b.cbox((cxn - lx / 2 - 1.2, ny, zz), (0.14, 4.6, 0.14))
    b.finish("C_42_neighbours", "C_ZHENGDIAN", 42)
    FOOTPRINTS["C"].append((fx - 4.0, x + 8.0, y - 15.0, y + 15.0))


# ── Place D 宣德楼内外（W11 宣德门 + bg12 卡；⚠️ 墩台 / 门洞 / 朵楼 / 阙亭尺寸无原文数值）──────────────
D_DOORS = tuple((-2 + k) * 16.0 for k in range(5))
D_DUN = (100.0, 24.0, 12.0)
D_DOOR = (6.0, 7.2)


def d_ground() -> None:
    x0, x1, y0, y1 = PLACE_RANGE["D"]
    ground_box("D", "plaza_S", x0, x1, y0, -65.0)
    ground_box("D", "plaza_N", x0, x1, -59.0, y1)


def d_wall(r: Row) -> None:
    r.need("y=0", "x ±50…±82", "底宽 12", "高 8.7")
    a, c = span(r.where, "x")
    b = Batch()
    prof = [(-6.0, Z_STREET - 1.0), (6.0, Z_STREET - 1.0), (1.5, Z_STREET + 8.7), (-1.5, Z_STREET + 8.7)]
    for s in (-1, 1):
        x0, x1 = sorted((s * a, s * c))
        b.prism_x(x0, x1, prof)
    b.finish("D_50_palace_wall", "D_WALL", 50)


def d_dun(r: Row) -> None:
    r.need("墩台 100 × 24 × 12", "门洞 5 个 6 × 7.2", "中距 16")
    lx, ly, h = D_DUN
    dw, dh = D_DOOR
    b = Batch()
    cur = -lx / 2
    for dc in D_DOORS:
        slab(b, cur, dc - dw / 2, -ly / 2, ly / 2, Z_STREET, Z_STREET + h)
        slab(b, dc - dw / 2, dc + dw / 2, -ly / 2, ly / 2, Z_STREET + dh, Z_STREET + h)
        cur = dc + dw / 2
    slab(b, cur, lx / 2, -ly / 2, ly / 2, Z_STREET, Z_STREET + h)
    for s in (-1, 1):                                   # 墩台顶两侧女墙
        slab(b, -lx / 2, lx / 2, s * (ly / 2 - 0.25) - 0.25, s * (ly / 2 - 0.25) + 0.25, Z_STREET + h, Z_STREET + h + 1.0)
    b.finish("D_51_dun", "D_DUN", 51)
    for dc in D_DOORS:
        FOOTPRINTS["D"].append((dc - dw / 2, dc + dw / 2, -ly / 2, ly / 2))


def d_doors(r: Row) -> None:
    r.need("扇 3 × 7.2 × 0.25", "门钉 7 × 9", "向内开 80°", "门洞南口内 4 m")
    dw, dh = D_DOOR
    y_h = -D_DUN[1] / 2 + 4.0
    b = Batch()
    nails = Batch()
    for dc in D_DOORS:
        for s in (-1, 1):
            hx = dc + s * dw / 2                         # 铰点在门洞侧壁
            ang = math.radians(80.0 if s < 0 else -80.0)
            u0 = (-s * 1.0, 0.0)                          # 关闭时指向门洞中线
            u = (u0[0] * math.cos(ang) - u0[1] * math.sin(ang), u0[0] * math.sin(ang) + u0[1] * math.cos(ang))
            n = (math.sin(ang), -math.cos(ang))          # 关闭时的门面法向 (0, −1) 随门扇同转 → 开启后朝门洞中线
            ln, t = 3.0, 0.25
            base = [(hx - s * 0.05, y_h), (hx - s * 0.05 + u[0] * ln, y_h + u[1] * ln)]
            q = [(base[0][0] - n[0] * t / 2, base[0][1] - n[1] * t / 2), (base[1][0] - n[0] * t / 2, base[1][1] - n[1] * t / 2),
                 (base[1][0] + n[0] * t / 2, base[1][1] + n[1] * t / 2), (base[0][0] + n[0] * t / 2, base[0][1] + n[1] * t / 2)]
            extrude(b, q, Z_STREET + 0.05, Z_STREET + dh - 0.05)
            for i in range(7):
                for j in range(9):
                    sl = 0.35 + (ln - 0.7) * i / 6
                    zz = Z_STREET + 0.9 + (dh - 1.8) * j / 8
                    px = base[0][0] + u[0] * sl + n[0] * (t / 2 + 0.03)
                    py = base[0][1] + u[1] * sl + n[1] * (t / 2 + 0.03)
                    nails.ball((px, py, zz), 0.07)
    b.finish("D_52_door_leaves", "D_DUN", 52)
    nails.finish("D_52_door_nails", "D_DUN", 52)


def d_menlou(r: Row) -> None:
    r.need("平坐 46 × 22 × 1.2", "殿身 42 × 18，柱高 6", "屋面高 8")
    z = Z_STREET + D_DUN[2]
    b = Batch()
    slab(b, -23.0, 23.0, -11.0, 11.0, z, z + 1.2)
    railing(b, [(-23.0, -11.0), (23.0, -11.0), (23.0, 11.0), (-23.0, 11.0), (-23.0, -11.0)], z + 1.2, 0.8, 1.2)
    ze = timber_hall(b, 0.0, 0.0, 42.0, 18.0, z + 1.2, 6.0, 8.0, bays=(7, 4), roof="hip", walls=("N", "E", "W"), overhang=3.0)
    ridge_beasts(b, 0.0, 0.0, (48.0 - 24.0) / 2, ze + 8.0, "x", 1.0)
    b.finish("D_53_menlou", "D_MENLOU", 53)


def d_duolou(r: Row) -> None:
    r.need("朵楼 12 × 12，柱高 5，屋面高 5")
    z = Z_STREET + D_DUN[2]
    b = Batch()
    for s in (-1, 1):
        cx = s * 40.0
        slab(b, cx - 7.0, cx + 7.0, -7.0, 7.0, z, z + 0.8)
        ze = timber_hall(b, cx, 0.0, 12.0, 12.0, z + 0.8, 5.0, 5.0, bays=(3, 3), roof="hip", walls=("N", "E", "W", "S"), door=4.0, overhang=1.5)
        x_in, x_out = s * 21.5, s * 33.5                # 斜廊：门楼平坐边 → 朵楼，屋面由高到低
        slab(b, min(x_in, x_out), max(x_in, x_out), -2.5, 2.5, z, z + 1.0)
        for xx in (x_in, (x_in + x_out) / 2, x_out):
            for yy in (-2.5, 2.5):
                b.cyl(xx, yy, z + 1.0, z + 4.6, 0.16, 6)
        hi_z, lo_z = z + 1.2 + 6.0 + 0.7, ze - 0.6
        b.poly_solid([Vector((x_in, -3.5, hi_z)), Vector((x_out, -3.5, lo_z)), Vector((x_out, 3.5, lo_z)), Vector((x_in, 3.5, hi_z))],
                     [Vector((x_in, -3.5, hi_z + 1.6)), Vector((x_out, -3.5, lo_z + 1.6)), Vector((x_out, 3.5, lo_z + 1.6)), Vector((x_in, 3.5, hi_z + 1.6))])
    b.finish("D_54_duolou", "D_MENLOU", 54)


def d_que(r: Row) -> None:
    r.need("长廊 x ±50…±56，y -50…-12", "阙亭 (±53, -57)", "长廊檐高 4", "阙亭台基 12 × 12 × 1.4，亭 9 × 9 × 9")
    gx0, gx1 = span(r.where, "x")
    ly0, ly1 = -50.0, -12.0
    b = Batch()
    for s in (-1, 1):
        xa, xb = sorted((s * gx0, s * gx1))
        slab(b, xa, xb, ly0, ly1, Z_STREET, Z_STREET + 0.3)
        for k in range(int((ly1 - ly0) / BAY) + 1):
            b.cyl(s * (gx0 + 0.3), ly0 + BAY * k, Z_STREET + 0.3, Z_STREET + 4.3, 0.18, 6)
        slab(b, s * gx1 - 0.15, s * gx1 + 0.15, ly0, ly1, Z_STREET + 0.3, Z_STREET + 4.3)
        b.prism_y(ly0, ly1, [(xa - 0.8, Z_STREET + 4.3), (xb + 0.8, Z_STREET + 4.3), ((xa + xb) / 2, Z_STREET + 6.3)])
        cx, cy = s * 53.0, -57.0
        slab(b, cx - 6.0, cx + 6.0, cy - 6.0, cy + 6.0, Z_STREET, Z_STREET + 1.4)
        z1 = Z_STREET + 1.4
        for i in range(4):
            for j in range(4):
                if i in (0, 3) or j in (0, 3):
                    b.cyl(cx - 4.5 + 3 * i, cy - 4.5 + 3 * j, z1, z1 + 4.0, 0.2, 8)
        slab(b, cx - 5.2, cx + 5.2, cy - 5.2, cy + 5.2, z1 + 4.0, z1 + 4.6)
        railing(b, [(cx - 5.2, cy - 5.2), (cx + 5.2, cy - 5.2), (cx + 5.2, cy + 5.2), (cx - 5.2, cy + 5.2), (cx - 5.2, cy - 5.2)], z1 + 4.6, 0.8, 1.3)
        timber_hall(b, cx, cy, 8.0, 8.0, z1 + 4.6, 3.4, 3.6, bays=(2, 2), roof="hip", walls=("N", "E", "W", "S"), door=2.4, overhang=1.4)
    b.finish("D_55_que", "D_QUE", 55)


def d_river(r: Row) -> None:
    r.need("广场 y -80…-12", "金水河 y -65…-59", "桥 x -30…30", "河宽 6")
    x0, x1, _, _ = PLACE_RANGE["D"]
    solid_box("D_56_jinshui_water", "D_RIVER", (x0, -65.0, Z_WATER - 0.05), (x1, -59.0, Z_WATER), 56)
    solid_box("D_56_jinshui_bed", "D_RIVER", (x0, -65.0, -2.0), (x1, -59.0, Z_BED), 56)
    b = Batch()
    slab(b, -30.0, 30.0, -66.0, -58.0, Z_STREET - 0.4, Z_STREET + 0.12)
    for sx in (-1, 1):
        slab(b, sx * 30.0 - 0.3, sx * 30.0 + 0.3, -66.0, -58.0, Z_STREET + 0.12, Z_STREET + 0.9)
    b.finish("D_56_stone_bridge", "D_STREET", 56)


def d_chazi(r: Row) -> None:
    r.need("x=±19.5", "y -80…-20", "每 2 m 一根", "高 1.2")
    xs = float(re.search(rf"x=±({NUM})", r.where).group(1))
    y0, y1 = span(r.where, "y")
    b = Batch()
    for sx in (-1, 1):
        for k in range(int((y1 - y0) / 2.0) + 1):
            yy = y0 + 2.0 * k
            if -66.5 < yy < -57.5:
                continue
            b.cbox((sx * xs, yy, Z_STREET + 0.6), (0.15, 0.15, 1.2))
    b.finish("D_57_chazi", "D_CHAZI", 57)


def d_court(r: Row) -> None:
    r.need("殿庭 x ±70，y 12…335", "廊庑宽 10", "廊庑台 1.0 + 檐高 4.5")
    b = Batch()
    runs = [("W", -80.0, -70.0, 12.0, 335.0), ("E", 70.0, 80.0, 12.0, 150.0), ("E", 70.0, 80.0, 160.0, 335.0),
            ("N", -80.0, 80.0, 325.0, 335.0), ("S", -80.0, -50.0, 12.0, 22.0), ("S", 50.0, 80.0, 12.0, 22.0)]
    for side, x0, x1, y0, y1 in runs:
        slab(b, x0, x1, y0, y1, Z_STREET, Z_STREET + 1.0)
        z1 = Z_STREET + 1.0
        if side in "WE":
            inner = x1 if side == "W" else x0
            outer = x0 if side == "W" else x1
            for k in range(int((y1 - y0) / 5.0) + 1):
                b.cyl(inner + (-0.3 if side == "E" else 0.3), y0 + 5.0 * k, z1, z1 + 4.5, 0.2, 6)
            slab(b, outer - 0.2, outer + 0.2, y0, y1, z1, z1 + 4.5)
            b.prism_y(y0, y1, [(x0 - 0.8, z1 + 4.5), (x1 + 0.8, z1 + 4.5), ((x0 + x1) / 2, z1 + 7.0)])
        else:
            inner = y0 if side == "N" else y1
            outer = y1 if side == "N" else y0
            for k in range(int((x1 - x0) / 5.0) + 1):
                b.cyl(x0 + 5.0 * k, inner, z1, z1 + 4.5, 0.2, 6)
            slab(b, x0, x1, outer - 0.2, outer + 0.2, z1, z1 + 4.5)
            b.gable_x(x0, x1, y0 - 0.8, y1 + 0.8, z1 + 4.5, z1 + 7.0)
    b.finish("D_58_langwu", "D_COURT", 58)
    NOTES.append("方块 58：东廊庑 y 150…160 留横门缺口（S19 东边廊庑方向下马步行，判断）")


def d_hall(r: Row) -> None:
    r.need("台基 80 × 60 × 6", "月台 30 × 16", "殿身 56 × 26，柱高 10，屋面高 10")
    b = Batch()
    slab(b, -40.0, 40.0, 231.0, 291.0, Z_STREET, Z_STREET + 6.0)
    slab(b, -15.0, 15.0, 215.0, 231.0, Z_STREET, Z_STREET + 6.0)
    steps(b, -5.0, 5.0, 215.0, -1, Z_STREET, Z_STREET + 6.0, 16, 1.0)
    railing(b, [(-40.0, 231.0), (-15.0, 231.0), (-15.0, 215.0), (-5.0, 215.0)], Z_STREET + 6.0, 0.9, 2.0)
    railing(b, [(5.0, 215.0), (15.0, 215.0), (15.0, 231.0), (40.0, 231.0)], Z_STREET + 6.0, 0.9, 2.0)
    ze = timber_hall(b, 0.0, 261.0, 56.0, 26.0, Z_STREET + 6.0, 10.0, 10.0, bays=(9, 5), roof="hip",
                     walls=("N", "E", "W"), overhang=3.0)
    ridge_beasts(b, 0.0, 261.0, (62.0 - 32.0) / 2, ze + 10.0, "x", 1.3)
    b.finish("D_59_daqingdian", "D_HALL", 59)


def d_tower(r: Row) -> None:
    r.need("10 × 10，高 14 + 屋面 4")
    x, y = r.center
    b = Batch()
    slab(b, x - 5.0, x + 5.0, y - 5.0, y + 5.0, Z_STREET, Z_STREET + 6.0)
    slab(b, x - 5.8, x + 5.8, y - 5.8, y + 5.8, Z_STREET + 6.0, Z_STREET + 6.6)
    railing(b, [(x - 5.8, y - 5.8), (x + 5.8, y - 5.8), (x + 5.8, y + 5.8), (x - 5.8, y + 5.8), (x - 5.8, y - 5.8)], Z_STREET + 6.6, 0.8, 1.2)
    timber_hall(b, x, y, 8.0, 8.0, Z_STREET + 6.6, 6.7, 4.0, bays=(2, 2), roof="hip", walls=("N", "E", "W", "S"), door=2.0, overhang=1.4)
    b.finish(f"D_60_{r.index}_kelou", "D_COURT", 60)


# ── Place E 汴河码头（城内东水门以西；bg3 卡 + W11 汴河）──────────────────────────────
E_RIVER_HALF = 13.0


def e_ground() -> None:
    x0, x1, y0, y1 = PLACE_RANGE["E"]
    ground_box("E", "bank_N_quayside", x0, -16.0, E_RIVER_HALF, 17.0)
    ground_box("E", "bank_N_quayside_e", 16.0, x1, E_RIVER_HALF, 17.0)
    ground_box("E", "bank_N", x0, x1, 17.0, y1)
    ground_box("E", "bank_S", x0, x1, y0, -E_RIVER_HALF - 3.0)
    b = Batch()
    b.prism_x(x0, x1, [(-E_RIVER_HALF, Z_WATER), (-E_RIVER_HALF, Z_BED), (-E_RIVER_HALF - 3.0, Z_BED), (-E_RIVER_HALF - 3.0, Z_STREET)])
    b.finish("E_00_slope_S", "E_GROUND")


def e_river(r: Row) -> None:
    r.need("y -13…13", "河宽 26")
    x0, x1, _, _ = PLACE_RANGE["E"]
    solid_box("E_70_river_water", "E_RIVER", (x0, -E_RIVER_HALF, Z_WATER - 0.05), (x1, E_RIVER_HALF, Z_WATER), 70)
    solid_box("E_70_river_bed", "E_RIVER", (x0, -E_RIVER_HALF, -2.0), (x1, E_RIVER_HALF, Z_BED), 70)


def e_quay(r: Row) -> None:
    r.need("x -16…16，y 13…17，z=+2", "长 32 × 宽 4")
    x0, x1 = span(r.where, "x")
    y0, y1 = span(r.where, "y")
    b = Batch()
    slab(b, x0, x1, y0, y1, Z_STREET - 0.3, Z_STREET)
    slab(b, x0, x1, y1 - 0.4, y1, Z_BED, Z_STREET - 0.3)
    for k in range(int((x1 - x0) / 2.0) + 1):
        b.cyl(x0 + 2.0 * k, y0 + 0.2, Z_BED, Z_STREET - 0.3, 0.16, 6)
        b.cyl(x0 + 2.0 * k, (y0 + y1) / 2, Z_BED, Z_STREET - 0.3, 0.16, 6)
    for k in range(5):
        b.cbox((x0 + 0.5 + 7.75 * k, y0 + 0.35, Z_STREET + 0.4), (0.3, 0.3, 0.8))
    b.finish("E_71_quay", "E_DOCK", 71)
    FOOTPRINTS["E"].append((x0, x1, y0, y1))


def e_street(r: Row) -> None:
    r.need("y 17…30", "街宽 13")
    x0, x1, _, _ = PLACE_RANGE["E"]
    street_slab("E", 72, x0, x1, 17.0, 30.0)


def e_gatehouse(r: Row) -> None:
    r.need("门屋 12 × 7 × 7", "院墙 x ±30，y 30…84，高 3.5")
    x, y = r.center
    b = Batch()
    wall_ring(b, -30.0, 30.0, 30.0, 84.0, 0.8, Z_STREET, 3.5, [("S", 0.0, 12.0)])
    slab(b, x - 6.5, x + 6.5, y - 3.5, y + 3.5, Z_STREET, Z_STREET + 0.25)
    timber_hall(b, x, y, 12.0, 7.0, Z_STREET + 0.25, 4.0, 2.5, bays=(3, 2), roof="gable", ridge="x",
                walls=("E", "W", "S"), door=4.0, overhang=0.8)
    slab(b, x - 2.0, x + 2.0, y - 3.65, y - 3.35, Z_STREET, Z_STREET + 0.5)         # 门槛高过膝
    b.finish("E_73_granary_gate", "E_GRANARY", 73)
    FOOTPRINTS["E"].append((-31.0, 31.0, 29.0, 85.0))


def e_granary(r: Row) -> None:
    r.need("40 × 11 × 8")
    x, y = r.center
    b = Batch()
    slab(b, x - 20.0, x + 20.0, y - 5.5, y + 5.5, Z_STREET, Z_STREET + 5.0)
    b.gable_x(x - 20.6, x + 20.6, y - 6.1, y + 6.1, Z_STREET + 5.0, Z_STREET + 8.0)
    b.finish(f"E_74_{r.index}_granary", "E_GRANARY", 74)


# ── Place F 开封府（W11 开封府 + bg11 卡）────────────────────────────────────────────
def f_ground() -> None:
    x0, x1, y0, y1 = PLACE_RANGE["F"]
    ground_box("F", "ground", x0, x1, y0, y1)


def f_street(r: Row) -> None:
    r.need("y -130…-112，x -110…110", "街宽 18")
    street_slab("F", 80, *span(r.where, "x"), *span(r.where, "y"))


def f_wall(r: Row) -> None:
    r.need("x ±90，y ±110", "高 4，厚 1.2")
    b = Batch()
    wall_ring(b, -90.0, 90.0, -110.0, 110.0, 1.2, Z_STREET, 4.0, [("S", 0.0, 15.0)])
    b.finish("F_81_compound_wall", "F_WALL", 81)


def f_gate(r: Row) -> None:
    r.need("15 × 8，台基 0.4，柱高 4.2，屋面高 3", "两级石阶")
    x, y = r.center
    b = Batch()
    ze = timber_hall(b, x, y, 15.0, 8.0, Z_STREET, 4.2, 3.0, bays=(3, 2), base_h=0.4, roof="gable", ridge="x",
                     walls=(), overhang=1.0)
    for s in (-1, 1):                                   # 两次间实墙（门前条凳在 shot 层），明间开门
        slab(b, x + s * 2.5, x + s * 7.5, y - 0.15, y + 0.15, Z_STREET + 0.4, ze - 0.7)
        slab(b, x + s * 2.5, x + s * 7.3, y - 1.2, y - 0.8, Z_STREET + 0.4, Z_STREET + 0.85)
    for s in (-1, 1):                                   # 门扇向内开
        slab(b, x + s * 2.35, x + s * 2.5, y, y + 1.6, Z_STREET + 0.4, ze - 1.2)
    steps(b, x - 4.0, x + 4.0, y - 5.0, -1, Z_STREET, Z_STREET + 0.4, 2)
    b.finish("F_82_fumen", "F_GATE", 82)
    FOOTPRINTS["F"].append((x - 9.0, x + 9.0, y - 6.0, y + 6.0))


def f_inner(r: Row) -> None:
    r.need("甬道 y -106…-72", "甬道宽 4", "内门 12 × 6")
    x, y = r.center
    b = Batch()
    slab(b, -2.0, 2.0, -106.0, -72.0, Z_STREET, Z_STREET + 0.06)
    wall_ring(b, -42.0, 42.0, y, y, 0.9, Z_STREET, 3.5, [("S", 0.0, 12.0), ("N", 0.0, 200.0), ("E", 0.0, 1.0), ("W", 0.0, 1.0)])
    timber_hall(b, x, y, 12.0, 6.0, Z_STREET, 3.8, 2.4, bays=(3, 2), base_h=0.3, roof="gable", ridge="x",
                walls=("S",), door=4.0, overhang=0.8)
    b.finish("F_83_inner_gate", "F_GATE", 83)


def f_court(r: Row) -> None:
    r.need("庭院 x ±34，y -70…-20", "廊房 x ±34…±42", "廊房檐高 3.6")
    b = Batch()
    slab(b, -34.0, 34.0, -70.0, -20.0, Z_STREET, Z_STREET + 0.05)
    slab(b, -1.5, 1.5, -70.0, -21.5, Z_STREET + 0.05, Z_STREET + 0.1)
    for s in (-1, 1):
        xa, xb = sorted((s * 34.0, s * 42.0))
        slab(b, xa, xb, -68.0, -22.0, Z_STREET, Z_STREET + 0.3)
        for k in range(12):
            b.cyl(s * 34.3, -68.0 + 4.0 * k, Z_STREET + 0.3, Z_STREET + 3.9, 0.18, 6)
        slab(b, s * 42.0 - 0.15, s * 42.0 + 0.15, -68.0, -22.0, Z_STREET + 0.3, Z_STREET + 3.9)
        b.prism_y(-68.6, -21.4, [(xa - 0.8, Z_STREET + 3.9), (xb + 0.8, Z_STREET + 3.9), ((xa + xb) / 2, Z_STREET + 5.9)])
    b.finish("F_84_court", "F_COURT", 84)


def f_stones(r: Row) -> None:
    r.need("戒石 (0, -30)", "题名碑 (22, -45)", "戒石高 1.3", "碑高 2.2")
    b = Batch()
    slab(b, -0.6, 0.6, -30.4, -29.6, Z_STREET, Z_STREET + 0.3)
    slab(b, -0.4, 0.4, -30.18, -29.82, Z_STREET + 0.3, Z_STREET + 1.3)
    slab(b, 21.3, 22.7, -46.0, -44.0, Z_STREET, Z_STREET + 0.5)
    slab(b, 21.85, 22.15, -45.55, -44.45, Z_STREET + 0.5, Z_STREET + 2.2)
    b.finish("F_85_stones", "F_COURT", 85)


def f_hall(r: Row) -> None:
    r.need("27.5 × 14，台基 0.8，柱高 5，屋面高 5")
    x, y = r.center
    b = Batch()
    timber_hall(b, x, y, 27.5, 14.0, Z_STREET, 5.0, 5.0, bays=(5, 2), base_h=0.8, roof="hip", walls=("N", "E", "W"), overhang=1.6)
    steps(b, x - 5.0, x + 5.0, y - 8.0, -1, Z_STREET, Z_STREET + 0.8, 4)
    b.finish("F_86_zhengting", "F_COURT", 86)


def f_rear(r: Row) -> None:
    r.need("30 × 16 × 9")
    x, y = r.center
    b = Batch()
    hall(b, x, y, 30.0, 16.0, 9.0)
    b.finish(f"F_87_{r.index}_rear_hall", "F_COURT", 87)


# ── Place H 相国寺（W11 相国寺 + bg13 卡；东半与中轴，站五所见）────────────────────────────
def h_ground() -> None:
    x0, x1, y0, y1 = PLACE_RANGE["H"]
    ground_box("H", "ground", x0, x1, y0, y1)


def h_wall(r: Row) -> None:
    r.need("x ±125，y ±150", "高 4，厚 1.5")
    b = Batch()
    wall_ring(b, -125.0, 125.0, -150.0, 150.0, 1.5, Z_STREET, 4.0, [("E", 0.0, 15.0), ("S", 0.0, 24.0)])
    wall_ring(b, -125.0, 125.0, -150.0, 150.0, 1.8, Z_STREET, 1.2, [("E", 0.0, 15.0), ("S", 0.0, 24.0)])
    b.finish("H_90_temple_wall", "H_WALL", 90)


def h_east_gate(r: Row) -> None:
    r.need("15 × 7，台基 0.5，柱高 4.5，屋面高 3", "三级石阶")
    x, y = r.center
    b = Batch()
    slab(b, x - 4.5, x + 4.5, y - 8.5, y + 8.5, Z_STREET, Z_STREET + 0.5)
    for yy in (-7.5, -2.5, 2.5, 7.5):
        for xx in (-3.5, 3.5):
            b.cyl(x + xx, y + yy, Z_STREET + 0.5, Z_STREET + 5.0, 0.22, 8)
    for s in (-1, 1):
        slab(b, x - 0.15, x + 0.15, y + s * 2.5, y + s * 7.5, Z_STREET + 0.5, Z_STREET + 5.0)
    slab(b, x - 4.0, x + 4.0, y - 8.0, y + 8.0, Z_STREET + 5.0, Z_STREET + 5.7)
    b.prism_y(y - 9.0, y + 9.0, [(x - 5.0, Z_STREET + 5.7), (x + 5.0, Z_STREET + 5.7), (x, Z_STREET + 8.7)])
    steps_x(b, y - 3.0, y + 3.0, x + 4.5, 1, Z_STREET, Z_STREET + 0.5, 3)
    b.finish("H_91_east_gate", "H_GATE", 91)
    FOOTPRINTS["H"].append((x - 5.0, x + 6.0, y - 9.0, y + 9.0))


def h_south_gate(r: Row) -> None:
    r.need("24 × 10 × 12")
    x, y = r.center
    b = Batch()
    hall(b, x, y, 24.0, 10.0, 12.0)
    b.finish("H_92_sanmen", "H_GATE", 92)


def h_hall(r: Row) -> None:
    r.need("38 × 24，台基 1.5，柱高 7，屋面高 9")
    x, y = r.center
    b = Batch()
    ze = timber_hall(b, x, y, 38.0, 24.0, Z_STREET, 7.0, 9.0, bays=(7, 5), base_h=1.5, roof="hip", walls=("N", "E", "W"), overhang=2.4)
    ridge_beasts(b, x, y, (42.8 - 28.8) / 2, ze + 9.0, "x", 1.0)
    steps(b, x - 6.0, x + 6.0, y - 13.0, -1, Z_STREET, Z_STREET + 1.5, 5)
    steps(b, x - 6.0, x + 6.0, y + 13.0, 1, Z_STREET, Z_STREET + 1.5, 5)
    b.finish("H_93_main_hall", "H_HALL", 93)


def h_zisheng(r: Row) -> None:
    r.need("18 × 10，台基 1.0，下层 5，平坐 1.5，上层 4.5，屋面高 4", "五级踏步")
    x, y = r.center
    b = Batch()
    slab(b, x - 10.0, x + 10.0, y - 6.0, y + 6.0, Z_STREET, Z_STREET + 1.0)
    steps(b, x - 4.0, x + 4.0, y - 6.0, -1, Z_STREET, Z_STREET + 1.0, 5)
    z1 = Z_STREET + 1.0
    for xx in (-9.0, -3.0, 3.0, 9.0):
        for yy in (-5.0, 0.0, 5.0):
            b.cyl(x + xx, y + yy, z1, z1 + 5.0, 0.24, 8)
    for s in (-1, 1):
        slab(b, x + s * 3.0, x + s * 9.0, y - 0.15, y + 0.15, z1, z1 + 5.0)
    slab(b, x - 10.2, x + 10.2, y - 6.2, y + 6.2, z1 + 5.0, z1 + 6.5)
    railing(b, [(x - 10.2, y - 6.2), (x + 10.2, y - 6.2), (x + 10.2, y + 6.2), (x - 10.2, y + 6.2), (x - 10.2, y - 6.2)], z1 + 6.5, 0.9, 1.2)
    ze = timber_hall(b, x, y, 16.0, 8.0, z1 + 6.5, 4.5 - 0.7, 4.0, bays=(3, 2), roof="hip", walls=("N", "E", "W", "S"), door=3.0, overhang=1.8)
    ridge_beasts(b, x, y, (19.6 - 11.6) / 2, ze + 4.0, "x", 0.6)
    b.finish("H_94_zisheng_gate", "H_HALL", 94)


def h_corridors(r: Row) -> None:
    r.need("x ±45…±53，y 20…130", "台 0.3，檐高 4，屋面高 2.5")
    x0, x1 = span(r.where, "x")
    y0, y1 = span(r.where, "y")
    b = Batch()
    for s in (-1, 1):
        xa, xb = sorted((s * x0, s * x1))
        slab(b, xa, xb, y0, y1, Z_STREET, Z_STREET + 0.3)
        for k in range(int((y1 - y0) / BAY) + 1):
            b.cyl(s * (x0 + 0.3), y0 + BAY * k, Z_STREET + 0.3, Z_STREET + 4.0, 0.18, 6)
        slab(b, s * x1 - 0.15, s * x1 + 0.15, y0, y1, Z_STREET + 0.3, Z_STREET + 4.0)
        b.prism_y(y0 - 0.6, y1 + 0.6, [(xa - 0.8, Z_STREET + 4.0), (xb + 0.8, Z_STREET + 4.0), ((xa + xb) / 2, Z_STREET + 6.5)])
    b.finish("H_95_corridors", "H_HALL", 95)


def h_street(r: Row) -> None:
    r.need("x 125…215，y -9…9", "街宽 18")
    street_slab("H", 96, *span(r.where, "x"), *span(r.where, "y"))


# ── Place I 桑家瓦子（W11 + bg6 卡；大看棚内部按 S29 判断）─────────────────────────────
def i_ground() -> None:
    x0, x1, y0, y1 = PLACE_RANGE["I"]
    ground_box("I", "ground_S", x0, x1, y0, -20.0)
    ground_box("I", "ground_N", x0, x1, -14.0, y1)


def i_channel(r: Row) -> None:
    r.need("y -20…-14", "河宽 6", "板桥 x -2…2")
    x0, x1, _, _ = PLACE_RANGE["I"]
    y0, y1 = span(r.where, "y")
    solid_box("I_107_channel_water", "I_RIVER", (x0, y0, Z_WATER - 0.05), (x1, y1, Z_WATER), 107)
    solid_box("I_107_channel_bed", "I_RIVER", (x0, y0, -2.0), (x1, y1, Z_BED), 107)
    b = Batch()
    slab(b, -2.0, 2.0, y0 - 0.6, y1 + 0.6, Z_STREET - 0.25, Z_STREET + 0.05)
    b.finish("I_107_plank_bridge", "I_STREET", 107)


def i_street(r: Row) -> None:
    r.need("y 78…96，x -105…105", "街宽 18")
    street_slab("I", 100, *span(r.where, "x"), *span(r.where, "y"))


def i_fence(r: Row) -> None:
    r.need("x ±100，y ±75", "门口 x ±4", "高 2.6")
    b = Batch()
    for (ax, ay), (bx, by) in (((-100.0, -75.0), (100.0, -75.0)), ((100.0, -75.0), (100.0, 75.0)), ((-100.0, 75.0), (-100.0, -75.0)),
                               ((-100.0, 75.0), (-4.0, 75.0)), ((4.0, 75.0), (100.0, 75.0))):
        railing(b, [(ax, ay), (bx, by)], Z_STREET, 2.6, 2.0)
        q = seg_quad((ax, ay), (bx, by), 0.04)
        q = [(p[0] + (0.0 if ax != bx else (0.2 if ax < 0 else -0.2)), p[1] + (0.0 if ay != by else (0.2 if ay < 0 else -0.2))) for p in q]
        extrude(b, q, Z_STREET + 0.1, Z_STREET + 2.4)
    slab(b, -4.0, 4.0, 74.9, 75.1, Z_STREET, Z_STREET + 0.12)
    b.finish("I_102_fence", "I_FENCE", 102)


def i_poles(r: Row) -> None:
    r.need("杆高 6.5")
    x, y = r.center
    b = Batch()
    b.cyl(x, y, Z_STREET, Z_STREET + 6.5, 0.1, 8)
    b.cbox((x, y - 0.4, Z_STREET + 6.0), (0.08, 0.9, 0.08))
    b.cbox((x, y - 0.8, Z_STREET + 4.4), (0.6, 0.04, 3.0))
    b.finish(f"I_103_{r.index}_banner_pole", "I_FENCE", 103)


def i_big_shed(r: Row) -> None:
    r.need("30 × 26，檐高 8，脊高 11", "露台 12 × 6 × 0.8", "傀儡棚 3 × 2.5 × 3.2")
    x, y = r.center
    b = Batch()
    mat_shed(b, x, y, 30.0, 26.0, 8.0, 3.0, "y", open_side="N", mouth=10.0, shell=True)
    for s in (-1, 1):                                   # 北山墙：开口两侧席墙 + 两幅长布招
        slab(b, x + s * 5.0, x + s * 15.0, y + 13.0 - 0.04, y + 13.0 + 0.04, Z_STREET + 6.8, Z_STREET + 8.0)
        b.cbox((x + s * 5.6, y + 13.3, Z_STREET + 4.2), (1.0, 0.05, 5.0))
    b.cbox((x, y + 13.0, Z_STREET + 7.4), (10.0, 0.08, 1.2))
    sy = y - 13.0 + 3.0
    slab(b, x - 6.0, x + 6.0, sy - 3.0, sy + 3.0, Z_STREET, Z_STREET + 0.8)
    steps(b, x - 1.5, x + 1.5, sy + 3.0, 1, Z_STREET, Z_STREET + 0.8, 3, 0.3)
    px, py = x + 9.0, sy
    for dx, dy in itertools.product((-1.5, 1.5), (-1.25, 1.25)):
        b.cbox((px + dx, py + dy, Z_STREET + 1.3), (0.1, 0.1, 2.6))
    slab(b, px - 1.5, px + 1.5, py + 1.2, py + 1.3, Z_STREET + 0.9, Z_STREET + 2.6)
    slab(b, px - 1.5, px + 1.5, py - 1.3, py + 1.3, Z_STREET + 2.6, Z_STREET + 2.7)
    b.hip(px, py, 3.4, 2.9, Z_STREET + 2.7, 0.5)
    b.finish("I_104_big_shed", "I_SHED", 104)
    FOOTPRINTS["I"].append((x - 15.5, x + 15.5, y - 13.5, y + 13.5))


def i_sheds(r: Row) -> None:
    r.need("20 × 16，檐高 6，脊高 8")
    x, y = r.center
    b = Batch()
    mat_shed(b, x, y, 20.0, 16.0, 6.0, 2.0, "x", open_side="N", mouth=6.0)
    b.finish(f"I_105_{r.index}_shed", "I_SHED", 105)
    FOOTPRINTS["I"].append((x - 10.5, x + 10.5, y - 8.5, y + 8.5))


# ── Place J 南薰门外踏青路（W11 南薰门 + 御街南段走向；bg8 卡）──────────────────────────────
def j_ground() -> None:
    x0, x1, y0, y1 = PLACE_RANGE["J"]
    ground_box("J", "fields", x0, x1, y0, y1)


def j_road(r: Row) -> None:
    r.need("x -4.8…4.8，y -400…80", "路宽 9.6")
    x0, x1 = span(r.where, "x")
    y0, y1 = span(r.where, "y")
    b = Batch()
    b.prism_y(y0, y1, [(x0 - 1.0, Z_STREET), (x1 + 1.0, Z_STREET), (x1, Z_STREET + 0.3), (x0, Z_STREET + 0.3)])
    b.finish("J_110_road", "J_ROAD", 110)
    FOOTPRINTS["J"].append((x0 - 1.0, x1 + 1.0, y0, y1))


def j_cross(r: Row) -> None:
    r.need("y -3…3，x -150…150", "路宽 6")
    y0, y1 = span(r.where, "y")
    b = Batch()
    for xa, xb in ((-150.0, -4.8), (4.8, 150.0)):
        b.prism_x(xa, xb, [(y0 - 0.8, Z_STREET), (y1 + 0.8, Z_STREET), (y1, Z_STREET + 0.25), (y0, Z_STREET + 0.25)])
    b.finish("J_111_cross_road", "J_ROAD", 111)
    FOOTPRINTS["J"].append((-150.0, 150.0, y0 - 1.0, y1 + 1.0))


def j_mound(r: Row) -> None:
    r.need("44 × 30 × 6")
    x, y = r.center
    lx, ly, h = r.sizes[0]
    b = Batch()
    ring = lambda hx, hy, z: [Vector((x - hx, y - hy, z)), Vector((x + hx, y - hy, z)), Vector((x + hx, y + hy, z)), Vector((x - hx, y + hy, z))]
    b.poly_solid(ring(lx / 2, ly / 2, Z_STREET - 0.2), ring(lx / 2 - 10.0, ly / 2 - 9.0, Z_STREET + h))
    b.finish("J_112_mound", "J_ROAD", 112)
    FOOTPRINTS["J"].append((x - lx / 2, x + lx / 2, y - ly / 2, y + ly / 2))


def j_ridges(r: Row) -> None:
    r.need("x ±12…±150", "每 25 m", "高 0.15")
    b = Batch()
    _, _, y0, y1 = PLACE_RANGE["J"]
    for s in (-1, 1):
        for k in range(6):
            xx = s * (12.0 + 25.0 * k)
            for ya, yb in ((y0, -4.0), (4.0, y1)):
                if not hits_footprint("J", xx - 0.3, xx + 0.3, ya, yb):
                    slab(b, xx - 0.25, xx + 0.25, ya, yb, Z_STREET, Z_STREET + 0.15)
        for k in range(1, 16):
            yy = -25.0 * k
            xa, xb = sorted((s * 12.0, s * 150.0))
            slab(b, xa, xb, yy - 0.25, yy + 0.25, Z_STREET, Z_STREET + 0.15)
    b.finish("J_114_ridges", "J_FIELDS", 114)


def j_farms(r: Row) -> None:
    r.need("x ±40…±140", "y -380…-60", "种子 115", "8 × 6 × 3.6", "篱笆高 1.2")
    rng = random.Random(115)
    b = Batch()
    n = 0
    for gy in range(-380, -59, 45):
        for s in (-1, 1):
            if rng.random() < 0.35:
                continue
            x = s * rng.uniform(45.0, 135.0)
            y = gy + rng.uniform(0.0, 30.0)
            if hits_footprint("J", x - 9, x + 9, y - 7, y + 7):
                continue
            along_x = rng.random() < 0.5
            lx, ly = (8.0, 6.0) if along_x else (6.0, 8.0)
            slab(b, x - lx / 2, x + lx / 2, y - ly / 2, y + ly / 2, Z_STREET, Z_STREET + 2.4)
            gable(b, x - lx / 2 - 0.5, x + lx / 2 + 0.5, y - ly / 2 - 0.5, y + ly / 2 + 0.5, Z_STREET + 2.4, Z_STREET + 3.6,
                  "x" if along_x else "y")
            fx, fy = lx / 2 + 4.0, ly / 2 + 3.0
            railing(b, [(x - fx + 2.0, y - fy), (x - fx, y - fy), (x - fx, y + fy), (x + fx, y + fy), (x + fx, y - fy), (x + 2.0, y - fy)],
                    Z_STREET, 1.2, 1.5)
            FOOTPRINTS["J"].append((x - fx, x + fx, y - fy, y + fy))
            n += 1
    b.finish("J_115_farms", "J_FIELDS", 115)
    NOTES.append(f"方块 115：农舍 {n} 座（种子 115，避开路 / 土坡）")


def placeholder(r: Row) -> None:
    lx, ly, h = r.sizes[0]
    x, y = r.center
    solid_box(f"{r.place}_{r.block:02d}_{r.index}_PLACEHOLDER", f"{r.place}_MISC", (x - lx / 2, y - ly / 2, Z_STREET),
              (x + lx / 2, y + ly / 2, Z_STREET + h), r.block)


SCRIPTS: dict[tuple[str, str], callable] = {
    ("A", "河道"): a_river, ("A", "土坡"): a_slope, ("A", "街"): s_street, ("A", "码头"): a_dock, ("A", "仓"): a_granary,
    ("A", "表木"): a_poles, ("A", "柳"): s_willow,
    ("B", "水门"): b_water_gate, ("B", "旱门"): b_dry_gate, ("B", "城墙"): b_wall, ("B", "拐子城"): b_guaizi,
    ("B", "护龙河"): b_moat, ("B", "木桥"): b_bridge, ("B", "柳"): s_willow,
    ("C", "州桥"): c_zhouqiao, ("C", "石壁"): c_stone_walls, ("C", "街"): s_street, ("C", "杈子"): c_chazi,
    ("C", "御沟"): c_ditch, ("C", "御廊"): c_gallery, ("C", "阙楼"): c_que, ("C", "望火楼"): c_fire_tower, ("C", "井"): c_well,
    ("C", "正店"): c_zhengdian,
    ("D", "宫墙"): d_wall, ("D", "墩台"): d_dun, ("D", "门扇"): d_doors, ("D", "门楼"): d_menlou, ("D", "朵楼"): d_duolou,
    ("D", "阙亭"): d_que, ("D", "金水河"): d_river, ("D", "杈子"): d_chazi, ("D", "廊庑"): d_court, ("D", "大殿"): d_hall,
    ("D", "刻漏楼"): d_tower,
    ("E", "河道"): e_river, ("E", "码头"): e_quay, ("E", "街"): e_street, ("E", "仓门"): e_gatehouse, ("E", "仓廒"): e_granary,
    ("E", "柳"): s_willow,
    ("F", "街"): f_street, ("F", "院墙"): f_wall, ("F", "府门"): f_gate, ("F", "内门"): f_inner, ("F", "廊房"): f_court,
    ("F", "戒石"): f_stones, ("F", "正厅"): f_hall, ("F", "殿宇"): f_rear,
    ("H", "寺墙"): h_wall, ("H", "寺东门"): h_east_gate, ("H", "大三门"): h_south_gate, ("H", "大殿"): h_hall,
    ("H", "资圣门"): h_zisheng, ("H", "东西廊"): h_corridors, ("H", "街"): h_street,
    ("I", "街"): i_street, ("I", "金水河"): i_channel, ("I", "栅栏"): i_fence, ("I", "布招杆"): i_poles, ("I", "大看棚"): i_big_shed, ("I", "看棚群"): i_sheds,
    ("J", "大路"): j_road, ("J", "横路"): j_cross, ("J", "土坡"): j_mound, ("J", "柳"): s_willow, ("J", "田埂"): j_ridges,
    ("J", "农舍"): j_farms,
}
WHITEMODEL_COL = {"p8": "BRIDGE", "p9": "HOUSES", "p10": "HOUSES", "p10a": "HOUSES"}
JITTERED = {"p10"}                                        # blender_build §4 步 3：只有 p10 母网格逐实例微抖
ORIGIN_Z = {"p8": P8_ORIGIN_Z}
PLACE_PRE = {"B": b_ground, "C": c_ground, "D": d_ground, "E": e_ground, "F": f_ground, "H": h_ground, "I": i_ground, "J": j_ground}
# 树 / 田埂 / 农舍要避开已建体量 → 按依赖顺序，而不是表序
ROW_ORDER_LAST = {("B", 27), ("A", 14), ("J", 113), ("J", 116), ("J", 114), ("J", 115)}


def build_place(place: str) -> None:
    if place in PLACE_PRE:
        PLACE_PRE[place]()
    rows = [r for r in ROWS if r.place == place]
    rows = [r for r in rows if (r.place, r.block) not in ROW_ORDER_LAST] + \
           [r for r in rows if (r.place, r.block) in ROW_ORDER_LAST]
    for r in rows:
        if r.kind == "shot":
            continue
        if r.kind == "placeholder":
            placeholder(r)
        elif r.kind == "whitemodel":
            ob = place_asset(r, WHITEMODEL_COL[r.model], ORIGIN_Z.get(r.model, Z_STREET), r.model in JITTERED)
            if r.model != "p8":
                h = max(abs(v) for v in (*ob["bj_lo"][:2], *ob["bj_hi"][:2])) * 1.03
                FOOTPRINTS[place].append((r.center[0] - h, r.center[0] + h, r.center[1] - h, r.center[1] + h))
        else:
            for key in r.keys:
                if len(r.keys) > 1 and r.index > 0:
                    continue
                fn = SCRIPTS.get((place, key))
                if fn is None:
                    raise PlanError(f"Place {place} 方块 {r.block}：生成器「{key}」未实现")
                fn(r)
    m = FRAMES[place].matrix()
    for c in bpy.context.scene.collection.children:
        if c.name.startswith(f"{place}_"):
            for ob in c.objects:
                ob.matrix_world = m @ ob.matrix_basis


LAYERS = ("G",) + PLACES
# 门洞 / 门口通透（Place 局部坐标盒；地面与街面豁免）——人物要从这些口子里走过
DOORWAYS: tuple[tuple[str, str, tuple[float, float, float], tuple[float, float, float], tuple[str, ...]], ...] = (
    *((("D", f"宣德门门洞 x={dc:+g} ", (dc - 2.0, -11.9, Z_STREET + 0.05), (dc + 2.0, 11.9, Z_STREET + 7.0), ("D_GROUND", "D_STREET")))
      for dc in D_DOORS),
    ("F", "府门明间", (-2.2, -108.0, Z_STREET + 0.5), (2.2, -104.0, Z_STREET + 3.8), ("F_GROUND", "F_STREET")),
    ("F", "内门", (-1.8, -70.4, Z_STREET + 0.35), (1.8, -69.6, Z_STREET + 3.3), ("F_GROUND", "F_STREET")),
    ("H", "寺东门明间", (121.0, -2.1, Z_STREET + 0.6), (129.0, 2.1, Z_STREET + 4.8), ("H_GROUND", "H_STREET")),
    ("I", "瓦子门口", (-3.8, 74.0, Z_STREET + 0.2), (3.8, 76.5, Z_STREET + 2.5), ("I_GROUND", "I_STREET")),
)


# ── QC（blender_build §1 表 + §6 可机检项；Place 检查一律换回 Place 局部坐标做）───────────────
@dataclass(frozen=True)
class Tri:
    owner: str
    col: str
    row: int
    v: tuple[Vector, Vector, Vector]


def holder_of(inst: bpy.types.DepsgraphObjectInstance) -> bpy.types.Object:
    return inst.parent.original if inst.is_instance and inst.parent else inst.object.original


def gather_tris(prefixes: tuple[str, ...]) -> list[Tri]:
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    out: list[Tri] = []
    for inst in dg.object_instances:
        ob = inst.object
        if ob.type != "MESH" or ob.original.get("look"):
            continue
        holder = holder_of(inst)
        cols = holder.users_collection
        col = cols[0].name if cols else ""
        if not col.startswith(prefixes):
            continue
        mw = inst.matrix_world.copy()
        verts = [mw @ v.co for v in ob.data.vertices]
        row = int(holder.get("bj_row", 0))
        for poly in ob.data.polygons:
            idx = list(poly.vertices)
            for k in range(1, len(idx) - 1):
                out.append(Tri(holder.name, col, row, (verts[idx[0]], verts[idx[k]], verts[idx[k + 1]])))
    return out


def local_tris(place: str, tris: list[Tri]) -> list[Tri]:
    f = FRAMES[place]
    return [Tri(t.owner, t.col, t.row, (f.local_v(t.v[0]), f.local_v(t.v[1]), f.local_v(t.v[2])))
            for t in tris if t.col.startswith(f"{place}_")]


def bvh_of(tris: list[Tri]) -> BVHTree:
    verts: list[Vector] = []
    faces: list[tuple[int, int, int]] = []
    for i, t in enumerate(tris):
        verts += list(t.v)
        faces.append((3 * i, 3 * i + 1, 3 * i + 2))
    return BVHTree.FromPolygons(verts, faces, all_triangles=True)


def clip_axis(poly: list[Vector], axis: int, bound: float, keep_ge: bool) -> list[Vector]:
    out: list[Vector] = []
    for i, a in enumerate(poly):
        b = poly[(i + 1) % len(poly)]
        ina = a[axis] >= bound if keep_ge else a[axis] <= bound
        inb = b[axis] >= bound if keep_ge else b[axis] <= bound
        if ina:
            out.append(a)
        if ina != inb:
            out.append(a.lerp(b, (bound - a[axis]) / (b[axis] - a[axis])))
    return out


def dist2d(p: Vector, poly: list[Vector]) -> float:
    if not poly:
        return math.inf
    if len(poly) >= 3:
        cr = [(b.x - a.x) * (p.y - a.y) - (b.y - a.y) * (p.x - a.x) for a, b in zip(poly, poly[1:] + poly[:1])]
        area = sum(a.x * b.y - b.x * a.y for a, b in zip(poly, poly[1:] + poly[:1]))
        if abs(area) > 1e-9 and (all(c >= -1e-9 for c in cr) or all(c <= 1e-9 for c in cr)):
            return 0.0
    best = math.inf
    for a, b in zip(poly, poly[1:] + poly[:1]):
        ab = b - a
        t = 0.0 if ab.length_squared < 1e-12 else max(0.0, min(1.0, (p - a).dot(ab) / ab.length_squared))
        best = min(best, (a + ab * t - p).length)
    return best


def sample_path(path: list[Vector], step: float = 0.25) -> list[Vector]:
    pts: list[Vector] = [path[0]]
    for a, b in zip(path, path[1:]):
        n = max(1, int(math.ceil((b - a).length / step)))
        pts += [a.lerp(b, i / n) for i in range(1, n + 1)]
    return pts


def corridor(tris: list[Tri], path: list[Vector], r: float, exempt: tuple[str, ...]) -> dict[str, float]:
    keep = [t for t in tris if not t.col.startswith(exempt)]
    bvh = bvh_of(keep)
    worst: dict[str, float] = {}
    for s in sample_path(path):
        for _loc, _n, idx, _d in bvh.find_nearest_range(s, math.hypot(r, CORRIDOR_DZ)):
            t = keep[idx]
            poly = clip_axis(clip_axis(list(t.v), 2, s.z - CORRIDOR_DZ, True), 2, s.z + CORRIDOR_DZ, False)
            d = dist2d(Vector((s.x, s.y)), [Vector((q.x, q.y)) for q in poly])
            if d < r - 0.01:
                worst[t.owner] = min(worst.get(t.owner, math.inf), d)
    return worst


def box_hits(tris: list[Tri], lo: Vector, hi: Vector, exempt: tuple[str, ...]) -> set[str]:
    hit: set[str] = set()
    for t in tris:
        if t.col.startswith(exempt):
            continue
        poly = list(t.v)
        for ax in range(3):
            poly = clip_axis(poly, ax, lo[ax], True) if poly else poly
            poly = clip_axis(poly, ax, hi[ax], False) if poly else poly
        if poly:
            hit.add(t.owner)
    return hit


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    hard: bool = True


def instances(prefix: str, asset: str | None = None) -> list[bpy.types.Object]:
    return sorted((o for o in bpy.context.scene.objects if o.instance_type == "COLLECTION" and o.name.startswith(prefix)
                   and (asset is None or o.get("bj_asset") == asset)), key=lambda o: o.name)


def mesh_points(ob: bpy.types.Object) -> list[tuple[float, float]]:
    from array import array
    me = ob.data
    co = array("f", [0.0]) * (len(me.vertices) * 3)
    me.vertices.foreach_get("co", co)
    mw = ob.matrix_world
    return [((mw @ Vector((co[i], co[i + 1], co[i + 2]))).x, (mw @ Vector((co[i], co[i + 1], co[i + 2]))).y)
            for i in range(0, len(co), 3)]


def qc(one_take: list[Vector], entry: list[Vector], qc_only: bool) -> int:
    from array import array
    sc = bpy.context.scene
    checks: list[Check] = []
    place_tris = gather_tris(tuple(f"{p}_" for p in PLACES))
    loc = {p: local_tris(p, place_tris) for p in PLACES}

    dg = bpy.context.evaluated_depsgraph_get()
    lo = Vector((1e18, 1e18, 1e18))
    hi = Vector((-1e18, -1e18, -1e18))
    faces: dict[str, int] = {}
    for inst in dg.object_instances:
        ob = inst.object
        if ob.type != "MESH":
            continue
        holder = holder_of(inst)
        cols = holder.users_collection
        col = cols[0].name if cols else ""
        faces[col] = faces.get(col, 0) + len(ob.data.polygons)
        for c in ob.bound_box:
            w = inst.matrix_world @ Vector(c)
            lo = Vector([min(lo[i], w[i]) for i in range(3)])
            hi = Vector([max(hi[i], w[i]) for i in range(3)])

    polys = {p: place_poly(p) for p in PLACES}
    overlaps = [f"{a}×{b}" for a, b in itertools.combinations(PLACES, 2) if sat_overlap(polys[a], polys[b])]
    checks.append(Check("§6#2 三块 Place（W11 真实锚点）互不重叠", not overlaps,
                        "锚点 " + "；".join(f"{p} ({FRAMES[p].x:g}, {FRAMES[p].y:g}) 转 {FRAMES[p].rot_deg:g}°" for p in PLACES)
                        + "；重叠：" + ("、".join(overlaps) or "无")))
    for p in PLACES:
        pv = [v for t in loc[p] for v in t.v]
        if not pv:
            continue
        x0, x1, y0, y1 = PLACE_RANGE[p]
        plo = Vector([min(v[i] for v in pv) for i in range(3)])
        phi = Vector([max(v[i] for v in pv) for i in range(3)])
        over = max(x0 - plo.x, phi.x - x1, y0 - plo.y, phi.y - y1, 0.0)
        checks.append(Check(f"Place {p} 局部范围", over <= 0.05,
                            f"局部 x {plo.x:.1f}…{phi.x:.1f}  y {plo.y:.1f}…{phi.y:.1f}  z {plo.z:.1f}…{phi.z:.1f}"
                            f"（声明 x {x0:g}…{x1:g} y {y0:g}…{y1:g}，超出 {over:.1f} m）", hard=False))

    holes = {p: place_poly(p, -0.5, hole=True) for p in PLACES}
    culled: set[str] = set()
    g_objs = 0
    for ob in sc.objects:
        cols = ob.users_collection
        col = cols[0].name if cols else ""
        if not col.startswith("G_") or ob.type != "MESH":
            continue
        g_objs += 1
        if col in ("G_GROUND", "G_WATER"):
            continue
        bb = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
        rect = [(min(v.x for v in bb), min(v.y for v in bb)), (max(v.x for v in bb), min(v.y for v in bb)),
                (max(v.x for v in bb), max(v.y for v in bb)), (min(v.x for v in bb), max(v.y for v in bb))]
        for p, poly in holes.items():
            if sat_overlap(rect, poly) and any(point_in_poly(q, poly) for q in mesh_points(ob)):
                culled.add(f"{ob.name}→{p}")
    if g_objs:
        checks.append(Check("全城层在 Place 足迹内让位（地面开洞，街区 / 街 / 墙 / 门 / 地标零侵入）", not culled,
                            f"G 网格物件 {g_objs}；侵入：" + ("、".join(sorted(culled)) or "无")))

    if loc["A"]:
        bridge = [t for t in loc["A"] if t.col.startswith("A_BRIDGE")]
        bb = bvh_of(bridge)
        crown = bb.ray_cast(Vector((0.0, 0.0, 50.0)), Vector((0, 0, -1)))[0]
        by0 = min(v.y for t in bridge for v in t.v)
        by1 = max(v.y for t in bridge for v in t.v)
        feet = [bb.ray_cast(Vector((0.0, y, 50.0)), Vector((0, 0, -1)))[0] for y in (by1 - 0.05, by0 + 0.05)]
        cz = crown.z if crown else math.nan
        fz = [f.z if f else math.nan for f in feet]
        checks.append(Check("§6#3 虹桥拱顶 z=5.6±0.1 / 坡道脚 y=±18 z=2",
                            abs(cz - Z_DECK_CROWN) <= 0.1 and all(abs(z - Z_STREET) <= 0.1 for z in fz)
                            and abs(by1 - BRIDGE_FOOT) <= 0.1 and abs(by0 + BRIDGE_FOOT) <= 0.1,
                            f"拱顶 z={cz:.3f}；坡道脚 y={by1:+.2f}/{by0:+.2f} z={fz[0]:.3f}/{fz[1]:.3f}"))

        shop = instances("A_02_", "p9")
        if shop:
            s = shop[0]
            door = FRAMES["A"].local_v(s.matrix_world @ Vector(tuple(s["bj_front_local"])))
            foot_v = [v for t in bridge for v in t.v if v.y >= by1 - 0.05]
            fx0, fx1 = min(v.x for v in foot_v), max(v.x for v in foot_v)
            nx = max(fx0, min(fx1, door.x))
            clear = math.hypot(door.x - nx, door.y - by1)
            eye = Vector((0.0, by1, Z_STREET + 1.6))
            tgt = Vector((door.x, door.y, Z_STREET + 1.5))
            others = [t for t in loc["A"] if t.owner != s.name]
            hit = bvh_of(others).ray_cast(eye, (tgt - eye).normalized(), (tgt - eye).length - 0.3)
            blocked = others[hit[2]].owner if hit[0] is not None else ""
            checks.append(Check("§6#4 脚店 A 门口 ↔ 坡道脚净距 ≥ 6 m 且桥尾可见", clear >= DOOR_CLEAR_MIN and not blocked,
                                f"门脸中点 ({door.x:.2f}, {door.y:.2f}) → 坡道脚边 ({nx:.2f}, {by1:.2f}) 净距 {clear:.2f} m；"
                                f"桥尾视线 {'被 ' + blocked + ' 挡' if blocked else '通'}"))

        p10a = instances("A_", "p10")
        jit = [str(o["bj_jitter"]) for o in p10a]
        drots = [float(re.search(r"drot=([-+\d.]+)", j).group(1)) for j in jit]
        scales = [float(re.search(r"scale=([\d.]+)", j).group(1)) for j in jit]
        checks.append(Check("§6#5 沿河民居逐实例微抖（种子＝方块号）",
                            len(set(jit)) == len(jit) and all(abs(d) <= 2.0 for d in drots) and all(abs(x - 1) <= 0.03 for x in scales),
                            "；".join(f"{o.name}: {j}" for o, j in zip(p10a, jit))))

        rows_dev = []
        for tag, blocks in (("北岸", range(4, 9)), ("南岸", range(9, 12))):
            backs = []
            for o in p10a:
                if o["bj_row"] in blocks:
                    lo_l, hi_l = Vector(tuple(o["bj_lo"])), Vector(tuple(o["bj_hi"]))
                    fl = Vector(tuple(o["bj_front_local"])).normalized()
                    yb = lo_l.y if fl.y > 0 else hi_l.y
                    backs += [FRAMES["A"].local_v(o.matrix_world @ Vector((x, yb, 0))).y for x in (lo_l.x, hi_l.x)]
            rows_dev.append((tag, max(backs) - min(backs) if backs else 0.0))
        checks.append(Check("§6#11 民居后墙成直线（偏差 ≤ 0.5 m，判断容差）", all(d <= 0.5 for _t, d in rows_dev),
                            "；".join(f"{t} 后墙线偏差 {d:.2f} m" for t, d in rows_dev)))

        bad = corridor(loc["A"], one_take, CORRIDOR_R_A, ("A_RIVER", "A_STREET", "A_BRIDGE"))
        checks.append(Check(f"§6#6 一镜到底走廊 r={CORRIDOR_R_A} dz=±{CORRIDOR_DZ} 零几何（河 / 街 / 桥除外）", not bad,
                            f"{len(sample_path(one_take))} 采样点；侵入："
                            + ("、".join(f"{k}（距轴 {v:.2f} m）" for k, v in sorted(bad.items())) or "无")))

    if loc["B"]:
        bad = corridor(loc["B"], entry, CORRIDOR_R_B, ("B_RIVER", "B_STREET", "B_MOAT", "B_GATES"))
        checks.append(Check(f"§4步5 入城镜走廊 r={CORRIDOR_R_B} dz=±{CORRIDOR_DZ}（地 / 水 / 木桥 / 门台除外）", not bad,
                            "路径 " + " → ".join(f"({q.x:g},{q.y:g})" for q in entry) + "；侵入："
                            + ("、".join(f"{k}（距轴 {v:.2f} m）" for k, v in sorted(bad.items())) or "无")))
        dw, dh, px, _py = gate_dims()
        gates_ok = []
        for r in (x for x in ROWS if x.place == "B" and x.block == 21):
            c = r.center[1]
            hit = box_hits(loc["B"], Vector((-px / 2 - 0.5, c - dw / 2 + 0.05, Z_STREET + 0.05)),
                           Vector((px / 2 + 0.5, c + dw / 2 - 0.05, Z_STREET + dh - 0.05)), ("B_STREET",))
            gates_ok.append(f"门洞 y={c:+g}：" + ("、".join(sorted(hit)) or "通"))
        checks.append(Check("§4步5 旱门门洞通透", all(h.endswith("通") for h in gates_ok), "；".join(gates_ok)))

    for p, label, lo_v, hi_v, exempt in DOORWAYS:
        if not loc[p]:
            continue
        hit = box_hits(loc[p], Vector(lo_v), Vector(hi_v), exempt)
        checks.append(Check(f"Place {p} {label}通透", not hit, "、".join(sorted(hit)) or "通"))

    d_bad: list[str] = []
    d_warn: list[str] = []
    for p in ("A", "C"):
        for t in loc[p]:
            beyond = (p == "A" and any(abs(v.y) > 30.0 + 1e-3 for v in t.v)) or \
                     (p == "C" and any(abs(v.x) > C_D_HALF + 1e-3 for v in t.v))
            if beyond:
                (d_warn if t.row else d_bad).append(t.owner)
    checks.append(Check("§6#9 D 级区域为空（A 房后 |y|>30、C 御街 ±46 外）", not d_bad,
                        "非表行越界：" + ("、".join(sorted(set(d_bad))) or "无") + "；表行自身尺寸越界（WARN）："
                        + ("、".join(sorted(set(d_warn))) or "无")))

    # look pass（tools/look_bianjing.py，sk1 divergence #19）的材质 / 灯 / 相机都带 look 标记，不算布局层的违规
    n_mat = sum(1 for m in bpy.data.materials if m.users and not m.get("look"))
    slots = sum(1 for me in bpy.data.meshes if len(me.materials) and not me.get("look_slots") and not any(m and m.get("look") for m in me.materials))
    lights = [lt for lt in bpy.data.lights if not lt.get("look")]
    cams = [c for c in bpy.data.cameras if not c.get("look")]
    checks.append(Check("§6#7 布局层零材质 / 零灯光 / 零相机", n_mat == 0 and slots == 0 and not lights and not cams,
                        f"材质 {n_mat}、带材质槽网格 {slots}、灯 {len(lights)}、相机 {len(cams)}（look 标记的不计）"))
    shot = sorted({o.name for o in sc.objects if int(o.get("bj_row", 0)) in SHOT_LAYER_BLOCKS})
    checks.append(Check("§6#8 shot 层道具行未进 blend", not shot, "越界对象：" + ("、".join(shot) or "无")))

    digest = hashlib.sha256()
    for ob in sorted((o for o in bpy.data.objects if not o.get("look")), key=lambda o: o.name):
        digest.update(ob.name.encode())
        digest.update(repr(tuple(round(v, 4) for row in ob.matrix_world for v in row)).encode())
        if ob.type == "MESH":
            co = array("f", [0.0]) * (len(ob.data.vertices) * 3)
            ob.data.vertices.foreach_get("co", co)
            digest.update(co.tobytes())

    print("\n" + "=" * 96)
    print(f"[build_bianjing] {'QC ONLY ' if qc_only else ''}{bpy.data.filepath or '(unsaved)'}")
    print("| 集合 | 物件 | 面 |\n|---|---:|---:|")
    for c in sorted(sc.collection.children, key=lambda c: c.name):
        print(f"| `{c.name}` | {len(c.objects)} | {faces.get(c.name, 0)} |")
    print(f"| **合计** | {len(sc.objects)} | {sum(faces.values())} |")
    protos = sorted(c.name for c in bpy.data.collections if c.name.startswith("PROTO_"))
    print(f"原型集合（不在场景树里，被实例引用）：{', '.join(protos)}")
    print(f"世界包围盒 x {lo.x:.1f}…{hi.x:.1f}  y {lo.y:.1f}…{hi.y:.1f}  z {lo.z:.2f}…{hi.z:.2f}")
    print(f"几何摘要 sha256 {digest.hexdigest()}")
    for n in dict.fromkeys(NOTES):
        print(f"  · {n}")
    corridor_ok = True
    hard_ok = True
    for c in checks:
        print(f"  {'✓' if c.ok else ('✗' if c.hard else '!')} {c.name}：{c.detail}")
        if not c.ok and c.hard:
            hard_ok = False
        if "走廊" in c.name or "门洞" in c.name:
            corridor_ok = corridor_ok and c.ok
    print("=" * 96)
    sys.stdout.flush()
    return (0 if corridor_ok else 1) if qc_only else (0 if hard_ok else 1)


# ── previz 公用：S 档航拍（shotNN_previz.py 只调这里；本镜编排只写在 shots/shotNN/previz_config.toml）──────────
AERIAL_SCHEMA: dict[str, set[str]] = {
    "全局": {"shot", "fps", "total_sec", "分辨率", "匀速", "平滑"},
    # 停留：该关键帧附近「每米花多少秒」的相对倍数（默认 1.0）。时间按弧长 × 停留分配，
    # 权重再经 ±1.5 s 宽窗平滑——既能给某一拍多几秒，又不会出现一脚油门。
    "机位": {"t", "位置", "看向", "焦距", "切", "停留"},
    "道具": {"名", "Place", "尺寸", "桅高", "水手", "关键帧"},
    "道具.关键帧": {"t", "位置", "桅角"},
    "人群": {"名", "Place", "数", "起点", "终点", "横向", "速度", "种子", "贴桥面"},
}


def load_aerial(cfg_path: Path) -> dict:
    cfg = tomllib.loads(cfg_path.read_text(encoding="utf-8"))
    if set(cfg) - {"全局", "机位", "道具", "人群"}:
        raise PlanError(f"{cfg_path}：未知段 {sorted(set(cfg) - {'全局', '机位', '道具', '人群'})}")
    for cr in cfg.get("人群", []):
        if set(cr) - AERIAL_SCHEMA["人群"] or not {"名", "Place", "数", "起点", "终点", "速度"} <= set(cr):
            raise PlanError(f"{cfg_path} [[人群]] 键不对：{sorted(cr)}")
    if set(cfg.get("全局", {})) - AERIAL_SCHEMA["全局"]:
        raise PlanError(f"{cfg_path} [全局] 未知键 {sorted(set(cfg['全局']) - AERIAL_SCHEMA['全局'])}")
    keys = cfg.get("机位", [])
    if len(keys) < 2:
        raise PlanError(f"{cfg_path}：[[机位]] 至少两帧")
    for k in keys:
        if set(k) - AERIAL_SCHEMA["机位"] or not {"t", "位置", "看向", "焦距"} <= set(k):
            raise PlanError(f"{cfg_path} [[机位]] 键不对：{sorted(k)}")
    for k0, k1 in zip(keys, keys[1:]):
        if k1["t"] < k0["t"] or (k1["t"] == k0["t"] and not k1.get("切")):
            raise PlanError(f"{cfg_path}：机位 t 必须递增；同一时刻的两帧只许后一帧标「切」（t={k1['t']}）")
    if keys[0]["t"] != 0.0 or keys[-1]["t"] != cfg["全局"]["total_sec"]:
        raise PlanError(f"{cfg_path}：机位 t 必须从 0 到 total_sec")
    for pr in cfg.get("道具", []):
        if set(pr) - AERIAL_SCHEMA["道具"]:
            raise PlanError(f"{cfg_path} [[道具]] 未知键 {sorted(set(pr) - AERIAL_SCHEMA['道具'])}")
        for kf in pr.get("关键帧", []):
            if set(kf) - AERIAL_SCHEMA["道具.关键帧"]:
                raise PlanError(f"{cfg_path} 道具关键帧未知键 {sorted(set(kf) - AERIAL_SCHEMA['道具.关键帧'])}")
    return cfg


def aerial_world() -> World:
    if not WORLD:
        md = PLAN_MD.read_text(encoding="utf-8")
        ROWS[:] = parse_plan(md)
        world_setup(load_w11())
    return WORLD[0]


def river_at(world: World, ref: str, ds: float) -> Pt:
    pts, _ = world.rivers[next(k for k in world.rivers if k.startswith("汴河"))]
    if ref.startswith("WP"):
        wp = next((w for w in world.cfg["waypoint"] if w["id"] == ref), None)
        if wp is None:
            raise PlanError(f"W11 没有航点 {ref}")
        anchor = (float(wp["pos"][0]), float(wp["pos"][1]))
    elif ref in FRAMES:
        anchor = (FRAMES[ref].x, FRAMES[ref].y)
    else:
        raise PlanError(f"汴河@{ref}：REF 只能是 WPn 或 A / B / C")
    best, acc = (math.inf, 0.0), 0.0
    for a0, b0 in zip(pts, pts[1:]):
        d = v2sub(b0, a0)
        ln = v2len(d)
        t = max(0.0, min(1.0, v2dot(v2sub(anchor, a0), d) / (ln * ln)))
        q = (a0[0] + d[0] * t, a0[1] + d[1] * t)
        if v2len(v2sub(anchor, q)) < best[0]:
            best = (v2len(v2sub(anchor, q)), acc + t * ln)
        acc += ln
    target = max(0.0, min(acc, best[1] + ds))
    acc = 0.0
    for a0, b0 in zip(pts, pts[1:]):
        ln = v2len(v2sub(b0, a0))
        if acc + ln >= target:
            t = (target - acc) / ln
            return (a0[0] + (b0[0] - a0[0]) * t, a0[1] + (b0[1] - a0[1]) * t)
        acc += ln
    return pts[-1]


def sibling_config(cfg_path: Path, shot: str) -> Path:
    return cfg_path.parent.parent / shot / "previz_config.toml"


def resolve_spec(world: World, spec: list, what: str, cfg_path: Path) -> Vector:
    head = str(spec[0])
    if head.startswith("汴河@") and len(spec) == 3:
        x, y = river_at(world, head.split("@", 1)[1], float(spec[1]))
        return Vector((x, y, float(spec[2])))
    m = re.fullmatch(r"(WP\d+)(看向)?", head)
    if m and len(spec) == 1:
        wp = next((w for w in world.cfg["waypoint"] if w["id"] == m.group(1)), None)
        if wp is None:
            raise PlanError(f"W11 没有航点 {m.group(1)}")
        v = wp["look_at"] if m.group(2) else wp["pos"]
        return Vector((float(v[0]), float(v[1]), float(v[2]) + Z_STREET))      # 判断：W11 z 是离地高，加街面 2 m
    if head == "Place" and len(spec) == 5:
        return FRAMES[str(spec[1])].world_v((float(spec[2]), float(spec[3]), float(spec[4])))
    if head == "世界" and len(spec) == 4:
        return Vector((float(spec[1]), float(spec[2]), float(spec[3])))
    if head == "承接" and len(spec) == 2:
        return aerial_keys(sibling_config(cfg_path, str(spec[1])))[-1][what]
    raise PlanError(f"{cfg_path}：{what} 写法认不出 {spec}")


def aerial_keys(cfg_path: Path) -> list[dict]:
    cfg = load_aerial(cfg_path)
    world = aerial_world()
    keys = []
    for k in cfg["机位"]:
        inherit = str(k["位置"][0]) == "承接"
        lens = aerial_keys(sibling_config(cfg_path, str(k["位置"][1])))[-1]["焦距"] if inherit else float(k["焦距"])
        keys.append({"t": float(k["t"]), "位置": resolve_spec(world, k["位置"], "位置", cfg_path),
                     "看向": resolve_spec(world, k["看向"], "看向", cfg_path), "焦距": lens,
                     "切": bool(k.get("切", False)), "承接": inherit,
                     "停留": float(k.get("停留", 1.0))})
    return keys


def mono_hermite(ts: list[float], vs: list[float], t: float, ease_in: bool) -> float:
    """Fritsch–Carlson 单调三次插值：关键帧之间不过冲；相邻两帧同值＝悬停（速度归零）。"""
    n = len(ts)
    if n == 1 or t <= ts[0]:
        return vs[0]
    if t >= ts[-1]:
        return vs[-1]
    d = [(vs[i + 1] - vs[i]) / (ts[i + 1] - ts[i]) for i in range(n - 1)]
    m = [d[0]] + [0.0 if d[i - 1] * d[i] <= 0 else (d[i - 1] + d[i]) / 2 for i in range(1, n - 1)] + [d[-1]]
    if ease_in:
        m[0] = 0.0
    for i in range(n - 1):
        if d[i] == 0.0:
            m[i] = m[i + 1] = 0.0
            continue
        a0, b0 = max(0.0, m[i] / d[i]), max(0.0, m[i + 1] / d[i])
        m[i], m[i + 1] = a0 * d[i], b0 * d[i]
        if a0 * a0 + b0 * b0 > 9.0:
            tau = 3.0 / math.sqrt(a0 * a0 + b0 * b0)
            m[i], m[i + 1] = tau * a0 * d[i], tau * b0 * d[i]
    i = max(k for k in range(n - 1) if ts[k] <= t)
    h = ts[i + 1] - ts[i]
    u = (t - ts[i]) / h
    return ((2 * u ** 3 - 3 * u ** 2 + 1) * vs[i] + (u ** 3 - 2 * u ** 2 + u) * h * m[i]
            + (-2 * u ** 3 + 3 * u ** 2) * vs[i + 1] + (u ** 3 - u ** 2) * h * m[i + 1])


UNIFORM_ON = False        # build_aerial 打开匀速时置 True（见 camera_at 的 ease 判断）


def camera_at(keys: list[dict], t: float) -> tuple[Vector, Vector, float]:
    segs: list[list[dict]] = []
    for k in keys:
        if not segs or k["切"]:
            segs.append([k])
        else:
            segs[-1].append(k)
    seg = [sg for sg in segs if sg[0]["t"] <= t + 1e-9][-1]
    ts = [k["t"] for k in seg]
    ease = seg is segs[0] and keys[0]["承接"] and not UNIFORM_ON
    pos = Vector([mono_hermite(ts, [k["位置"][i] for k in seg], t, ease) for i in range(3)])
    look = Vector([mono_hermite(ts, [k["看向"][i] for k in seg], t, ease) for i in range(3)])
    return pos, look, mono_hermite(ts, [k["焦距"] for k in seg], t, ease)


def curve_lateral(pts: list[Vector], fps: int) -> tuple[float, float]:
    """逐帧位置 → 最大侧向加速度 (t, a)：二阶差分取加速度，再取垂直于速度的分量。

    为什么是这个量：相机就是**按帧**被 key 的，帧率下的二阶差分就是它真实经历的加速度；
    而「相邻速度夹角 ÷ dt」随采样间隔漂移（密采样上任何抖动都读成几十 g，闸门失灵），
    三点外接圆半径在近共线时又会数值退化 —— 两个都试过，都不能用（2026-09-18）。
    """
    worst = (0.0, 0.0)
    for i in range(1, len(pts) - 1):
        v = (pts[i + 1] - pts[i - 1]) * (fps / 2.0)
        if v.length < 1.0:                       # 近乎悬停：侧向加速度无意义
            continue
        a = (pts[i + 1] - pts[i] * 2.0 + pts[i - 1]) * (fps * fps)
        a_lat = (a - v.normalized() * a.dot(v.normalized())).length
        if a_lat > worst[1]:
            worst = ((i + 1) / fps, a_lat)
    return worst


def aerial_path(keys: list[dict], total: float, fps: int, n_frames: int,
                smooth_g: float = 1.0, step_m: float = 0.5) -> dict:
    """解出逐帧机位。三步，顺序与「在什么空间做」都要紧（2026-09-18 踩了三次）：

      1. **等弧长重采样**：先按名义 t 密采样，再沿路径每 `step_m` 米取一点。
         为什么：按 t 采样得到的点在空间上是不均匀的（慢的地方密、快的地方疏），
         在这种点列上做滑动平均等于变频滤波 —— 会造出新的折角，还把航线拖偏两百米。
      2. **等距低通**：窗口以米为单位自适应放大，直到逐帧侧向加速度 ≤ `平顺` g。
         窗口是米，直接对应转弯半径，物理意义清楚。平滑只动机位、不动看向。
      3. **按弧长 × 停留权重配时间**：`停留` 大的地方每米多花时间（权重经宽窗平滑），
         于是既能给某一拍多几秒，又不会出现一脚油门。
    """
    dense_n = 6000
    ts = [total * i / dense_n for i in range(dense_n + 1)]
    raw = [camera_at(keys, t)[0] for t in ts]
    acc_raw = [0.0]
    for a, b in zip(raw, raw[1:]):
        acc_raw.append(acc_raw[-1] + (b - a).length)
    L = acc_raw[-1] or 1.0

    m = max(8, int(L / step_m))
    P_uni, T_uni = [], []                      # 等弧长点列 + 每点对应的名义 t
    j = 1
    for i in range(m + 1):
        target = L * i / m
        while j < len(acc_raw) - 1 and acc_raw[j] < target:
            j += 1
        a0, a1 = acc_raw[j - 1], acc_raw[j]
        r = 0.0 if a1 - a0 < 1e-9 else (target - a0) / (a1 - a0)
        P_uni.append(raw[j - 1] + (raw[j] - raw[j - 1]) * r)
        T_uni.append(ts[j - 1] + (ts[j] - ts[j - 1]) * r)

    def low_pass(pts: list[Vector], win: int) -> list[Vector]:
        """等距点列的箱式低通。两端**沿切向延长补齐**——否则窗口在端点被截断、
        端点附近等于没滤，起飞后一秒就会留下一个 1.5 g 的折角（2026-09-18 实测 1.36s 处 14.3 m/s²）。"""
        if win <= 0:
            return list(pts)
        head_dir = (pts[1] - pts[0]) if len(pts) > 1 else Vector((1.0, 0.0, 0.0))
        tail_dir = (pts[-1] - pts[-2]) if len(pts) > 1 else Vector((1.0, 0.0, 0.0))
        pad_head = [pts[0] - head_dir * (win - i) for i in range(win)]
        pad_tail = [pts[-1] + tail_dir * (i + 1) for i in range(win)]
        ext = pad_head + list(pts) + pad_tail
        out = []
        for i in range(win, win + len(pts)):
            a = Vector((0.0, 0.0, 0.0))
            for q in ext[i - win:i + win + 1]:
                a += q
            out.append(a / (2 * win + 1))
        return out

    def weight_at(t: float) -> float:
        ks = sorted(keys, key=lambda k: k["t"])
        if t <= ks[0]["t"]:
            return float(ks[0].get("停留", 1.0))
        for a, b in zip(ks, ks[1:]):
            if t <= b["t"] + 1e-9:
                wa, wb = float(a.get("停留", 1.0)), float(b.get("停留", 1.0))
                r = 0.0 if b["t"] - a["t"] < 1e-9 else (t - a["t"]) / (b["t"] - a["t"])
                return wa + (wb - wa) * r
        return float(ks[-1].get("停留", 1.0))

    w = [weight_at(t) for t in T_uni]
    wspan = max(1, m // 20)
    for _ in range(2):
        w = [sum(w[max(0, i - wspan):min(len(w), i + wspan + 1)])
             / len(w[max(0, i - wspan):min(len(w), i + wspan + 1)]) for i in range(len(w))]

    MAX_DEV = 5.0     # 平滑允许偏离作者航线的上限（米）

    def solve(win: int) -> dict:
        pts = low_pass(P_uni, win)
        # 带约束的平滑：平滑是为了压掉折角，但它会把航线整体推偏（实测 ±108 m 窗口推偏 24 m），
        # 在二十来米宽的门洞里，推偏就是撞墙；事后再拉回来又会拐出 258 m/s² 的尖峰。
        # 所以在平滑这一步就夹住：任何点偏离原线不得超过 MAX_DEV，超了就投影回球面。
        for i, (a, b) in enumerate(zip(pts, P_uni)):
            d = a - b
            if d.length > MAX_DEV:
                pts[i] = b + d.normalized() * MAX_DEV
        acc = [0.0]
        for i in range(len(pts) - 1):
            acc.append(acc[-1] + (pts[i + 1] - pts[i]).length * (w[i] + w[i + 1]) / 2)
        tot = acc[-1] or 1.0
        pos, tnom = [], []
        k = 1
        for f in range(n_frames):
            target = tot * f / max(1, n_frames - 1)
            while k < len(acc) - 1 and acc[k] < target:
                k += 1
            a0, a1 = acc[k - 1], acc[k]
            r = 0.0 if a1 - a0 < 1e-9 else (target - a0) / (a1 - a0)
            pos.append(pts[k - 1] + (pts[k] - pts[k - 1]) * r)
            tnom.append(T_uni[k - 1] + (T_uni[k] - T_uni[k - 1]) * r)
        spd = [(pos[i + 1] - pos[i]).length * fps for i in range(len(pos) - 1)]
        return {"pos": pos, "t_nom": tnom, "pts": pts, "spd": spd,
                "path": sum((pts[i + 1] - pts[i]).length for i in range(len(pts) - 1)),
                "lat": curve_lateral(pos, fps),
                "accel": max((abs(b - a) * fps for a, b in zip(spd, spd[1:])), default=0.0)}

    def backtrack(pts: list[Vector]) -> tuple[float, float]:
        """折返检查：把每帧位置投影到「首→末」这条弦上，投影值必须一路不减。

        为什么用投影而不是看转角：**平缓的折返一样是折返**——半径 200 m 的 180° 掉头
        侧向加速度完全合规，却依然是「飞过去又飞回来」。投影单调性把这类全抓住，
        而正常的弯（哪怕 90°）在弦上的投影仍然递增，不会误报。
        """
        if len(pts) < 3:
            return (0.0, 0.0)
        chord = pts[-1] - pts[0]
        if chord.length < 1e-6:
            return (0.0, 0.0)
        u = chord.normalized()
        proj = [(q - pts[0]).dot(u) for q in pts]
        worst, peak = (0.0, 0.0), proj[0]
        for i, v in enumerate(proj):
            back = peak - v
            if back > worst[1]:
                worst = ((i + 1) / fps, back)
            peak = max(peak, v)
        return worst

    win, sol = 0, solve(0)
    cap = 0 if smooth_g <= 0 else max(4, m // 12)   # 平滑 = 0：不做空间平滑，完全按关键帧线飞
    while cap and sol["lat"][1] > smooth_g * 9.81 and win < cap:
        win = max(2, min(cap, win * 2 if win else max(2, int(4.0 / step_m))))
        sol = solve(win)
    sol["win"] = win
    sol["win_m"] = win * step_m
    sol["back"] = backtrack(sol["pos"])

    # ── 看向平滑：把逐帧看点低通，直到云台偏转速率 ≤ 25°/s（真云台平缓摇的量级）。
    # 只平滑「看哪儿」，不动「飞哪儿」；窗口按帧数自适应。
    look_raw = [camera_at(keys, t)[1] for t in sol["t_nom"]]

    def yaw_rate(ls: list[Vector], ps: list[Vector]) -> tuple[float, float]:
        worst, prev = (0.0, 0.0), None
        for i, (lk, ps_i) in enumerate(zip(ls, ps)):
            d = lk - ps_i
            if d.length < 1e-6:
                continue
            yaw = math.degrees(math.atan2(d.y, d.x))
            if prev is not None:
                r = abs((yaw - prev + 180.0) % 360.0 - 180.0) * fps
                if r > worst[1]:
                    worst = (i / fps, r)
            prev = yaw
        return worst

    def smooth_pts(ls: list[Vector], win: int) -> list[Vector]:
        if win <= 0:
            return list(ls)
        out = []
        for i in range(len(ls)):
            lo, hi = max(0, i - win), min(len(ls), i + win + 1)
            a = Vector((0.0, 0.0, 0.0))
            for q in ls[lo:hi]:
                a += q
            out.append(a / (hi - lo))
        return out

    lwin, looks = 0, look_raw
    while yaw_rate(looks, sol["pos"])[1] > 25.0 and lwin < len(look_raw) // 4:
        lwin = max(3, lwin * 2 if lwin else max(3, fps // 3))
        looks = smooth_pts(look_raw, lwin)
    sol["look"] = looks
    sol["look_win"] = lwin
    sol["yaw"] = yaw_rate(looks, sol["pos"])
    sol["dev"] = max(((a - b).length for a, b in zip(P_uni, sol["pts"])), default=0.0)
    return sol


def verify_camera(cfg_path: Path, fps: int, n: int, smooth_g: float) -> dict:
    """从 blend 里**已打好关键帧的相机**回读，逐帧重算四项判据。

    为什么必须这样（2026-09-19 事故）：净空修正一度写在打帧之后，于是闸门量的是修正后的数组、
    blend 里留的是修正前的路径 —— 闸门报「净空 4.0 m」，成片却直接撞墙。
    **闸门要测产物。** 这里读的就是渲染时真正会用的那条相机轨迹。
    """
    sc = bpy.context.scene
    dg = bpy.context.evaluated_depsgraph_get()
    cam = sc.camera
    pos, look = [], []
    for f in range(1, n + 1):
        sc.frame_set(f)
        m = cam.matrix_world
        pos.append(m.translation.copy())
        look.append((m.to_3x3() @ Vector((0.0, 0.0, -1.0))).normalized())
    rays = [Vector(d) for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1))]
    worst_clr = (0.0, 1e9, "-")
    for i in range(0, n, 2):
        for d in rays + [look[i]]:
            hit, loc, _nr, _ix, ob, _mx = sc.ray_cast(dg, pos[i], d, distance=15.0)
            if not hit:
                continue
            nm = ob.name if ob else "-"
            if nm.startswith(("G_000", "B_00_river", "B_00_ground")):
                continue
            dist = (loc - pos[i]).length
            if dist < worst_clr[1]:
                worst_clr = ((i + 1) / fps, dist, nm)
    spd = [(pos[i + 1] - pos[i]).length * fps for i in range(n - 1)]
    lat = curve_lateral(pos, fps)
    view = (0.0, 0.0)
    for i in range(1, n):
        v = pos[i] - pos[i - 1]
        if v.length < 1e-6:
            continue
        v2, d2 = Vector((v.x, v.y, 0.0)), Vector((look[i].x, look[i].y, 0.0))
        if v2.length < 1e-6 or d2.length < 1e-6:
            continue
        a = math.degrees(v2.normalized().angle(d2.normalized(), 0.0))
        if a > view[1]:
            view = ((i + 1) / fps, a)
    chord = pos[-1] - pos[0]
    back = (0.0, 0.0)
    if chord.length > 1e-6:
        u = chord.normalized()
        peak = (pos[0] - pos[0]).dot(u)
        for i, p in enumerate(pos):
            v = (p - pos[0]).dot(u)
            if peak - v > back[1]:
                back = ((i + 1) / fps, peak - v)
            peak = max(peak, v)
    out = {"clr": worst_clr, "lat": lat, "view": view, "back": back,
           "spd_lo": min(spd), "spd_hi": max(spd),
           "accel": max((abs(b - a) * fps for a, b in zip(spd, spd[1:])), default=0.0)}
    print(f"VERIFY（从相机回读）净空 {worst_clr[1]:.1f} m @ {worst_clr[0]:.2f}s（{worst_clr[2]}）；"
          f"速度 {out['spd_lo']:.0f}–{out['spd_hi']:.0f} m/s；切向 {out['accel']:.1f}；"
          f"侧向 {lat[1]:.1f} m/s² @ {lat[0]:.2f}s；视线偏航向 {view[1]:.0f}°；折返 {back[1]:.1f} m")
    if worst_clr[1] < 2.5:
        raise PlanError(f"{cfg_path}：{worst_clr[0]:.2f}s 相机离 {worst_clr[2]} 只有 {worst_clr[1]:.1f} m —— 撞墙。")
    if lat[1] > smooth_g * 1.2 * 9.81:
        raise PlanError(f"{cfg_path}：{lat[0]:.2f}s 侧向 {lat[1]:.1f} m/s² 超 1.2 g —— 这个速度转不过来。")
    if view[1] > 100.0:
        raise PlanError(f"{cfg_path}：{view[0]:.2f}s 视线偏航向 {view[1]:.0f}° —— 边往前飞边回头看。")
    if back[1] > 3.0:
        raise PlanError(f"{cfg_path}：{back[0]:.2f}s 折返 {back[1]:.1f} m —— 一镜到底不许折返。")
    return out


def build_aerial(cfg_path: Path) -> dict:
    cfg = load_aerial(cfg_path)
    g = cfg["全局"]
    fps, total = int(g["fps"]), float(g["total_sec"])
    n = int(round(total * fps))
    keys = aerial_keys(cfg_path)
    global UNIFORM_ON
    uniform = bool(g.get("匀速", True))
    UNIFORM_ON = uniform
    # 键名以 AERIAL_SCHEMA 为准：曾经 schema 写 `平滑`、这里读 `平顺`，于是 TOML 里调的阈值
    # 一律不生效，默认值悄悄接管（2026-09-19 实测）。一个东西只能有一个名字。
    smooth_g = float(g.get("平滑", g.get("平顺", 1.0)))   # 允许的侧向加速度上限，单位 g
    sol = aerial_path(keys, total, fps, n, smooth_g) if uniform else None
    t_of = (lambda x: x)

    # 净空修正必须在**打关键帧之前**跑：2026-09-19 实测事故——修正写在诊断段（打帧之后），
    # 于是闸门量的是修正后的数组、blend 里留的是修正前的路径，闸门报「净空 4.0 m」而成片直接撞墙。
    # 教训：**闸门要测产物，不要测中间变量**；任何改路径的步骤都得排在产物生成之前。
    if sol and smooth_g > 0:
        # ── 净空修正：平滑是为了压掉折角，但它会把航线推偏（实测 ±108 m 窗口推偏 24 m），
        # 在门洞这种只有二十来米宽的窗口里，推偏就等于撞墙。做法是**紧处不平滑**：
        # 净空不足的帧（含前后各 10 帧）把位置按权重拉回作者写的原始关键帧线——
        # 那条线是照洞口中心穿的，本来就不需要平滑。
        dg0 = bpy.context.evaluated_depsgraph_get()
        rays = [Vector(d) for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1))]

        def clearance(pt) -> tuple[float, str]:
            best = (1e9, "-")
            for d in rays:
                hit, loc, _n, _i, ob, _m = bpy.context.scene.ray_cast(dg0, pt, d, distance=12.0)
                if not hit:
                    continue
                nm = ob.name if ob else "-"
                if nm.startswith(("G_000", "B_00_river", "B_00_ground")):
                    continue
                dd = (loc - pt).length
                if dd < best[0]:
                    best = (dd, nm)
            return best

        raw_pos = [camera_at(keys, t)[0] for t in sol["t_nom"]]
        FEATHER = 30                      # 羽化半径（帧）：1.2 s 内把修正量渐入渐出
        for _ in range(8):
            tight = [i for i in range(len(sol["pos"])) if clearance(sol["pos"][i])[0] < 4.0]
            if not tight:
                break
            # 硬边界会造成瞬移：窗口内拉回 70%、窗口外不动，相邻两帧就差好几米
            # （2026-09-19 实测：8.68s 处速度 38→263 m/s、切向加速度 5610 m/s²，观感就是「撞一下」）。
            # 改成余弦羽化：修正量在 ±FEATHER 帧内平滑渐入渐出，路径保持连续。
            pull = [0.0] * len(sol["pos"])
            for i in tight:
                for j in range(max(0, i - FEATHER), min(len(sol["pos"]), i + FEATHER + 1)):
                    w = 0.8 * 0.5 * (1.0 + math.cos(math.pi * abs(j - i) / FEATHER))
                    if w > pull[j]:
                        pull[j] = w
            for j, w in enumerate(pull):
                if w > 0.0:
                    sol["pos"][j] = sol["pos"][j] * (1 - w) + raw_pos[j] * w


    sc = bpy.context.scene
    sc.frame_start, sc.frame_end, sc.render.fps = 1, n, fps

    col = collection("PREVIZ")
    cam_data = bpy.data.cameras.new("PREVIZ_CAM")
    # 远裁剪要够到远郊地面外圈（look_bianjing.FAR_GROUND_HALF），否则高空机位地平线下露出一条深蓝天空带
    cam_data.sensor_width, cam_data.clip_start, cam_data.clip_end = 36.0, 1.0, 2000000.0
    cam = bpy.data.objects.new("PREVIZ_CAM", cam_data)
    tgt = bpy.data.objects.new("PREVIZ_CAM_TARGET", None)
    col.objects.link(cam)
    col.objects.link(tgt)
    con = cam.constraints.new("TRACK_TO")
    con.target, con.track_axis, con.up_axis = tgt, "TRACK_NEGATIVE_Z", "UP_Y"
    for f in range(1, n + 1):
        t_nom = sol["t_nom"][min(f - 1, n - 1)] if sol else (f - 1) / fps
        pos, look, lens = camera_at(keys, t_nom)
        if sol:
            pos = sol["pos"][min(f - 1, n - 1)]
            look = sol["look"][min(f - 1, n - 1)]
        cam.location, tgt.location, cam_data.lens = pos, look, lens
        cam.keyframe_insert("location", frame=f)
        tgt.keyframe_insert("location", frame=f)
        cam_data.keyframe_insert("lens", frame=f)
        # 近裁剪面随离地高度走：高空时 1 m 近裁剪面让 8 km 外的地面（z 2）与水面（z −0.02）深度打架、露出暗斑
        cam_data.clip_start = min(150.0, max(1.0, (pos.z - Z_STREET) / 40.0))
        cam_data.keyframe_insert("clip_start", frame=f)
    sc.camera = cam

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import look_bianjing as lk
    mats = lk.ensure_mats()          # 场景已写实化（divergence #19）→ 船与人用细模；灰模场景 → 盒子，与 look 之前一致

    def figure(name: str, pose: str, parent: bpy.types.Object | None) -> bpy.types.Object:
        if mats:
            ob = lk.figure_object(name, pose, mats)
            col.objects.link(ob)
        else:
            fb = Batch()
            fb.box((-0.2, -0.12, 0.0), (0.2, 0.12, 1.45))
            fb.ball((0.0, 0.0, 1.6), 0.13)
            ob = fb.finish(name, col)
        ob.parent = parent
        return ob

    for pr in cfg.get("道具", []):
        f0 = FRAMES[pr["Place"]]
        ln, wd, hh = (float(v) for v in pr["尺寸"])
        root = bpy.data.objects.new(f"PREVIZ_{pr['名']}", None)
        col.objects.link(root)
        if mats:
            hull = lk.boat_object(f"PREVIZ_{pr['名']}_hull", ln, wd, hh, mats)
            col.objects.link(hull)
        else:
            bt = Batch()
            bt.box((-ln / 2, -wd / 2, -0.6), (ln / 2, wd / 2, 1.2))
            bt.box((-ln * 0.3, -wd * 0.4, 1.2), (ln * 0.2, wd * 0.4, hh))
            hull = bt.finish(f"PREVIZ_{pr['名']}_hull", col)
        hull.parent = root
        pivot = None
        if float(pr.get("桅高", 0.0)) > 0:
            pivot = bpy.data.objects.new(f"PREVIZ_{pr['名']}_mast_pivot", None)
            col.objects.link(pivot)
            pivot.parent = root
            pivot.location = (0.0, 0.0, 1.2)
            mb = Batch()
            mb.cyl(0.0, 0.0, 0.0, float(pr["桅高"]), 0.15)
            mast = mb.finish(f"PREVIZ_{pr['名']}_mast", col)
            if mats:
                mast.data.materials.append(bpy.data.materials["LOOK_TIMBER"])
            mast.parent = pivot
        # 水手：两人在桅杆根部（船尾一侧）面朝船头抱桅，随桅杆放倒向后仰；一人在船尾撑篙（shot md `走位:`）
        haulers: list[bpy.types.Object] = []
        poler = None
        crew = int(pr.get("水手", 0))
        for i in range(min(crew, 2)):
            lean = bpy.data.objects.new(f"PREVIZ_{pr['名']}_sailor{i}_lean", None)
            col.objects.link(lean)
            lean.parent = root
            lean.location = (0.9, (-0.8, 0.8)[i], 1.0)
            fig = figure(f"PREVIZ_{pr['名']}_sailor{i}", "haul", lean)
            fig.rotation_euler = (0.0, 0.0, math.radians(90.0))
            haulers.append(lean)
        if crew >= 3:
            poler = bpy.data.objects.new(f"PREVIZ_{pr['名']}_poler_pivot", None)
            col.objects.link(poler)
            poler.parent = root
            poler.location = (ln * 0.42, 1.0, 1.0)
            fig = figure(f"PREVIZ_{pr['名']}_poler", "pole", poler)
            fig.rotation_euler = (0.0, 0.0, math.radians(180.0))
            pb = Batch()
            pb.cyl(0.0, 0.0, -3.2, 3.4, 0.04, 6)
            pole = pb.finish(f"PREVIZ_{pr['名']}_pole", col)
            if mats:
                pole.data.materials.append(bpy.data.materials["LOOK_TIMBER"])
            pole.parent = poler
            pole.location = (0.0, -0.4, 1.2)
            pole.rotation_euler = (math.radians(-25.0), 0.0, 0.0)
        kfs = pr["关键帧"]
        ts = [float(k["t"]) for k in kfs]
        root.rotation_euler = (0.0, 0.0, math.radians(f0.rot_deg))
        for f in range(1, n + 1):
            t = (f - 1) / fps
            lx = mono_hermite(ts, [float(k["位置"][0]) for k in kfs], t, False)
            ly = mono_hermite(ts, [float(k["位置"][1]) for k in kfs], t, False)
            root.location = f0.world_v((lx, ly, 0.0))
            root.keyframe_insert("location", frame=f)
            mast_deg = mono_hermite(ts, [float(k.get("桅角", 0.0)) for k in kfs], t, False)
            if pivot is not None:
                pivot.rotation_euler = (0.0, math.radians(mast_deg), 0.0)
                pivot.keyframe_insert("rotation_euler", frame=f)
            for lean in haulers:
                lean.rotation_euler = (0.0, math.radians(min(22.0, 0.25 * mast_deg)), 0.0)
                lean.keyframe_insert("rotation_euler", frame=f)
            if poler is not None:
                poler.rotation_euler = (math.radians(10.0 * math.sin(2 * math.pi * t / 3.2)), 0.0, 0.0)
                poler.keyframe_insert("rotation_euler", frame=f)

    # 人群：沿「起点 → 终点」直线走、两个方向各半，30 s 内不折返（出发点留足余量）；贴桥面时 z 跟虹桥桥面
    for cr in cfg.get("人群", []):
        f0 = FRAMES[cr["Place"]]
        a, b = Vector((*cr["起点"], 0.0)), Vector((*cr["终点"], 0.0))
        ln = (b - a).length
        d = (b - a).normalized()
        side = Vector((-d.y, d.x, 0.0))
        rng = random.Random(int(cr.get("种子", 1)))
        speed = float(cr["速度"])
        travel = speed * total
        if travel >= ln:
            raise PlanError(f"{cfg_path} [[人群]] {cr['名']}：{total:g} s × {speed:g} m/s 超过路段长 {ln:.0f} m")
        for i in range(int(cr["数"])):
            sgn = 1 if i % 2 == 0 else -1
            s0 = rng.uniform(0.0, ln - travel) if sgn > 0 else rng.uniform(travel, ln)
            off = rng.uniform(-1.0, 1.0) * float(cr.get("横向", 1.0))
            sp = speed * rng.uniform(0.85, 1.15)
            ob = figure(f"PREVIZ_{cr['名']}_{i}", "walk", None)
            yaw = math.atan2(d.y * sgn, d.x * sgn) - math.pi / 2 + math.radians(f0.rot_deg)
            ob.rotation_euler = (0.0, 0.0, yaw)
            for f in range(1, n + 1, 2):
                t = (f - 1) / fps
                p = a + d * (s0 + sgn * sp * t) + side * off
                z = deck_top(p.y) if cr.get("贴桥面") and abs(p.x) <= BRIDGE_HALF_W else Z_STREET + STREET_H
                ob.location = f0.world_v((p.x, p.y, z))
                ob.keyframe_insert("location", frame=f)

    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light, sh.color_type = "STUDIO", "OBJECT"
    # 不开阴影（阴影体积在布尔地面 / 裁开的街面等非流形网格上拉长条假影），也不开 cavity（同样吃深度缓冲，高空远景不稳）；
    # 灰模体块靠 studio 光的面朝向明暗就读得出
    sh.show_shadows, sh.show_cavity = False, False
    if sc.world is None:
        sc.world = bpy.data.worlds.new("PREVIZ_WORLD")
    sc.world.color = (0.58, 0.62, 0.68)
    for ob in bpy.data.objects:
        if ob.type != "MESH" or ob.library is not None:
            continue
        name = ob.name.lower()
        ob.color = (0.30, 0.34, 0.38, 1.0) if "water" in name else ((0.22, 0.22, 0.22, 1.0) if name.startswith("previz_") else (0.78, 0.78, 0.76, 1.0))
    people = bpy.data.objects.get("LOOK_people")      # look 层的全城静态行人只进写实渲染，灰模 previz 不带（免得被当成定格人群）
    if people is not None:
        people.hide_render = True
    sc.render.resolution_x, sc.render.resolution_y = (int(v) for v in g["分辨率"])
    sc.render.resolution_percentage = 100
    im = sc.render.image_settings
    if hasattr(im, "media_type"):
        im.media_type = "VIDEO"
    im.file_format = "FFMPEG"
    sc.render.ffmpeg.format, sc.render.ffmpeg.codec = "MPEG4", "H264"
    sc.render.ffmpeg.constant_rate_factor = "MEDIUM"
    sc.render.filepath = f"//{g['shot']}_previz.mp4"
    cuts = [k["t"] for k in keys if k["切"]]
    info = {"frames": n, "fps": fps, "first": keys[0], "last": keys[-1], "cuts": cuts}
    info["verify"] = verify_camera(cfg_path, fps, n, smooth_g)
    if sol:
        # 云台闸门：一边往前飞、一边把镜头拧到后方，看着就是「原地打转」。
        # 视线与航向夹角 > 100° 直接报错（2026-09-19 用户实测 shot01 摇到 176°）。
        view_off = []
        for i in range(1, len(sol["pos"])):
            vel = sol["pos"][i] - sol["pos"][i - 1]
            if vel.length < 1e-6:
                continue
            look = sol["look"][i] - sol["pos"][i]
            if look.length < 1e-6:
                continue
            v2, d2 = Vector((vel.x, vel.y, 0.0)), Vector((look.x, look.y, 0.0))
            if v2.length < 1e-6 or d2.length < 1e-6:
                continue
            ang = math.degrees(v2.normalized().angle(d2.normalized(), 0.0))
            view_off.append(((i + 1) / fps, ang))
        worst_view = max(view_off, key=lambda x: x[1], default=(0.0, 0.0))
        info["view"] = worst_view
        # 净空闸门：逐帧朝六个方向投射短射线，机位离任何几何 < 2.5 m 就报错。
        # 2026-09-19 实测：航线平滑（±108 m 窗口）把飞行线从河心推偏 24 m，挤进了旱门门垛与
        # 沿河民居之间的缝里，最近处 0.6 m —— 观众看到的就是「像撞在墙上」。
        dg = bpy.context.evaluated_depsgraph_get()
        dirs = [Vector(d) for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1))]
        worst_clr = (0.0, 1e9, "-")
        for i in range(0, len(sol["pos"]), 2):
            p0 = sol["pos"][i]
            for d in dirs:
                hit, loc, _n, _idx, ob, _m = bpy.context.scene.ray_cast(dg, p0, d, distance=12.0)
                if not hit:
                    continue
                dist = (loc - p0).length
                nm = ob.name if ob else "-"
                if nm.startswith(("G_000_ground", "G_000_water", "B_00_river", "B_00_ground", "G_000")):
                    continue                     # 脚下的地与水不算「撞」
                if dist < worst_clr[1]:
                    worst_clr = ((i + 1) / fps, dist, nm)
        info["clr"] = worst_clr
        if worst_clr[1] < 2.5:
            raise PlanError(
                f"{cfg_path}：{worst_clr[0]:.2f}s 处机位离 {worst_clr[2]} 只有 {worst_clr[1]:.1f} m（< 2.5 m）"
                f"—— 贴着几何飞，观众看到的是「撞墙」（用户 2026-09-19 实测反馈）。"
                f"把该段关键帧挪到洞口 / 街道中线上，或减小平滑窗口（平滑会把航线推偏）。")
        if sol["yaw"][1] > 40.0:
            raise PlanError(
                f"{cfg_path}：{sol['yaw'][0]:.2f}s 处云台偏转 {sol['yaw'][1]:.0f}°/s（>40°/s ＝ 甩镜头）"
                f"—— 用户 2026-09-19 再次定调「不要总是 180 度转镜头」。把该段的 `看向` 改成沿航向渐变的点，"
                f"别让云台在一两秒里横扫过去。")
        if worst_view[1] > 100.0:
            raise PlanError(
                f"{cfg_path}：{worst_view[0]:.2f}s 处视线偏离航向 {worst_view[1]:.0f}°（>100° ＝ 边往前飞边回头看）"
                f"—— 用户 2026-09-19 定调「不要总是 180 度转镜头」。把该段主体沿航线铺长、"
                f"或把 `看向` 改成前方偏侧的点，别用云台补路线的短。")
        if sol["back"][1] > 3.0:
            raise PlanError(
                f"{cfg_path}：{sol['back'][0]:.2f}s 处航线**折返** {sol['back'][1]:.1f} m"
                f"（沿首末弦的投影往回走了）—— 用户 2026-09-18 定调「折返全去掉，没必要折返」。"
                f"把该段关键帧改成沿航向单调推进；要回看某个主体就用 `看向`，别把机身掉回去。")
        if sol["lat"][1] > smooth_g * 1.2 * 9.81:
            raise PlanError(
                f"{cfg_path}：{sol['lat'][0]:.2f}s 处侧向加速度 {sol['lat'][1]:.1f} m/s²"
                f"（> {smooth_g * 1.2:.1f} g）—— 这个速度下转不过来（follow-up 011「不要转弯、要流线型」）。"
                f"出路：① 该段改直线飞过、靠 `看向` 摇过去看主体；② 该段 `停留` 加大（降速）后再转。")
        beats = []
        for k in keys:
            j = min(range(len(sol["t_nom"])), key=lambda i: abs(sol["t_nom"][i] - k["t"]))
            beats.append((k["t"], j / fps))
        info.update({"path": sol["path"], "win": sol["win"], "win_m": sol["win_m"],
                     "dev": sol["dev"], "accel": sol["accel"], "back": sol["back"],
                     "yaw": sol["yaw"], "look_win": sol["look_win"],
                     "lat": sol["lat"], "beats": beats,
                     "spd_lo": min(sol["spd"]), "spd_hi": max(sol["spd"]),
                     "prof": [(i / fps, v) for i, v in enumerate(sol["spd"]) if i % fps == 0]})
    return info


def run_aerial_previz(script_file: str) -> None:
    cfg_path = Path(script_file).resolve().with_name("previz_config.toml")
    blend = Path(bpy.data.filepath).resolve() if bpy.data.filepath else None
    if blend is None or blend == DEFAULT_OUT.resolve() or blend.parent != cfg_path.parent:
        raise PlanError("只许改本镜目录里的场景副本：先 copy bianjing.blend 到本镜目录再跑（rule 4h §A）")
    info = build_aerial(cfg_path)
    bpy.ops.wm.save_mainfile()
    a0, z0 = info["first"], info["last"]
    print(f"PREVIZ OK frames=1..{info['frames']} fps={info['fps']} cuts={info['cuts']} "
          f"first=({a0['位置'].x:.2f},{a0['位置'].y:.2f},{a0['位置'].z:.2f}) last=({z0['位置'].x:.2f},{z0['位置'].y:.2f},{z0['位置'].z:.2f})")
    if info.get("path"):
        print(f"PREVIZ 速度 路径 {info['path']:.0f} m  {info['spd_lo']:.0f}–{info['spd_hi']:.0f} m/s  "
              f"最大切向加速度 {info['accel']:.1f} m/s²  最大侧向 {info['lat'][1]:.1f} m/s² @ {info['lat'][0]:.2f}s")
        print(f"PREVIZ 云台 视线偏航向 最大 {info['view'][1]:.0f}° @ {info['view'][0]:.2f}s（>100 报错）；"
              f"偏转速率 最大 {info['yaw'][1]:.0f}°/s @ {info['yaw'][0]:.2f}s（>40 报错）；看向平滑 ±{info['look_win']} 帧")
        print(f"PREVIZ 净空 最近 {info['clr'][1]:.1f} m @ {info['clr'][0]:.2f}s（{info['clr'][2]}；<2.5 报错）")
        print(f"PREVIZ 平滑 窗口 ±{info['win_m']:.0f} m  航线最大偏离 {info['dev']:.1f} m  "
              f"最大折返 {info['back'][1]:.1f} m @ {info['back'][0]:.2f}s（>3 m 报错）")
        print("PREVIZ 速度曲线 " + " ".join(f"{t:.0f}s:{v:.0f}" for t, v in info["prof"] if int(t) % 3 == 0))
        print("PREVIZ 关键帧落点 " + " ".join(f"{a:.1f}→{b:.1f}" for a, b in info["beats"]))
    sys.stdout.flush()


def camera_report(frames: list[int]) -> None:
    sc = bpy.context.scene
    for f in frames:
        sc.frame_set(f)
        m = sc.camera.matrix_world
        e = m.to_euler()
        print(f"CAM f={f} loc=({m.translation.x:.4f},{m.translation.y:.4f},{m.translation.z:.4f}) "
              f"rot=({math.degrees(e.x):.4f},{math.degrees(e.y):.4f},{math.degrees(e.z):.4f}) lens={sc.camera.data.lens:.4f}")
    sys.stdout.flush()


def render_stills(frames: list[int], out_dir: str) -> None:
    sc = bpy.context.scene
    im = sc.render.image_settings
    if hasattr(im, "media_type"):
        im.media_type = "IMAGE"
    im.file_format = "PNG"
    out = Path(out_dir)
    out = out if out.is_absolute() else (REPO / out)
    out.mkdir(parents=True, exist_ok=True)
    stem = Path(bpy.data.filepath).stem
    for f in frames:
        sc.frame_set(f)
        target = out / f"{stem}_f{f:04d}.png"
        sc.render.filepath = str(target)
        bpy.ops.render.render(write_still=True)
        if not target.is_file():
            raise PlanError(f"静帧没写出来：{target}")
        print(f"STILL {target}")
    camera_report(frames)


def png_diff(a: str, b: str) -> None:
    from array import array
    imgs = [bpy.data.images.load(str(REPO / x) if not Path(x).is_absolute() else x) for x in (a, b)]
    if tuple(imgs[0].size) != tuple(imgs[1].size):
        raise PlanError(f"尺寸不同：{tuple(imgs[0].size)} vs {tuple(imgs[1].size)}")
    px = []
    for im_ in imgs:
        arr = array("f", [0.0]) * (im_.size[0] * im_.size[1] * im_.channels)
        im_.pixels.foreach_get(arr)
        px.append(arr)
    diff = [abs(x - y) for x, y in zip(px[0], px[1])]
    print(f"PNG_DIFF mean={sum(diff) / len(diff):.6f} max={max(diff):.6f} {a} vs {b}")
    sys.stdout.flush()


# ── 入口 ───────────────────────────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser(prog="build_bianjing.py")
    ap.add_argument("out", nargs="?", default=str(DEFAULT_OUT))
    ap.add_argument("--qc-only", action="store_true", help="只读现有 blend 出 §1 表；退出码 ＝ 走廊检查是否通过")
    ap.add_argument("--place", choices=PLACES, help="只重建一块（其余从表读但不生成；全城层不动）")
    ap.add_argument("--no-look", action="store_true", help="只出布局灰模，不跑 tools/look_bianjing.py 写实化")
    return ap.parse_args(argv)


def main() -> int:
    args = parse_args()
    out = Path(args.out)
    out = out if out.is_absolute() else (REPO / out)
    md = PLAN_MD.read_text(encoding="utf-8")
    ROWS[:] = parse_plan(md)
    load_w11()
    one_take = parse_one_take(md)
    entry = parse_entry_path(md, ROWS)
    COLS.clear()
    PROTOS.clear()
    if args.qc_only:
        if not out.is_file():
            raise PlanError(f"{out} 不存在")
        bpy.ops.wm.open_mainfile(filepath=str(out))
        return qc(one_take, entry, True)
    if args.place and out.is_file():
        bpy.ops.wm.open_mainfile(filepath=str(out))
        for c in [c for c in bpy.context.scene.collection.children if c.name.startswith(f"{args.place}_")]:
            for ob in list(c.objects):
                bpy.data.objects.remove(ob)
            bpy.data.collections.remove(c)
        bpy.data.orphans_purge(do_recursive=True)
        build_place(args.place)
    else:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.context.scene.unit_settings.system = "METRIC"
        if not args.place:
            build_global_layer(md)
        for p in ((args.place,) if args.place else PLACES):
            build_place(p)
    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out))
    print(f"SAVED {out}")
    code = qc(one_take, entry, False)
    if not args.no_look:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import look_bianjing
        look_bianjing.dress()
        bpy.ops.wm.save_mainfile()
        print(f"LOOK SAVED {out}")
    return code


if __name__ == "__main__":
    try:
        code = main()
    except Exception:
        traceback.print_exc()
        code = 2
    sys.stdout.flush()
    sys.exit(code)
