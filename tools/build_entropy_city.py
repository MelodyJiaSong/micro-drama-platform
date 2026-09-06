# -*- coding: utf-8 -*-
"""Build entropy_city.blend from scratch — the previz geometry source.

Every number here comes from ONE place: the geometry table in
`ai_videos/duikang_shangzeng/2_世界观人设/scenes/entropy_city/_blender/blender_build.md` §4,
which is itself read off the 26 定稿 reference images (and kept byte-consistent with
each subject md's `场景:` field and scene_build_flow.md's 空间事实表).

Why a builder and not hand-edits: the `.blend` is gitignored (media lives in R2), so
a hand-edited blend has no reviewable source. This script IS the source — delete the
blend, re-run, get the identical city. It supersedes the one-shot patch scripts
(add_city_fabric / add_tunnel / fix_plaza_opening), which patched a blend shape that
no longer exists.

Geometry only — no materials, no lights, no decoration (rule 4g §D: the .blend carries
几何, the reference images carry 长相).

Run:
  blender -b --factory-startup --python tools/build_entropy_city.py -- <out.blend>
"""
import sys
import math
import random

import bpy
import bmesh
from mathutils import Vector

sys.stdout.reconfigure(encoding="utf-8")
OUT = sys.argv[sys.argv.index("--") + 1:][0]

# ── 尺度 ────────────────────────────────────────────────────────────────────
FLOOR = 3.6                 # 层高，用来把「几层」换算成米
CAR_LEN = 4.84              # 唯一量尺：F80。任何尺寸都要能跟它比对得上

PLAZA_HALF = 30.0           # 广场 60×60
CORRIDOR_HALF = 11.5        # 楼到楼 23m —— 广场南北开口 ＝ 街廊，同一个宽度
ROAD_HALF = 7.5             # 车行道 15m
WALK_W = 4.0                # 人行道 4m/侧

STREET_Y0, STREET_Y1 = 30.0, 325.0    # 街面从广场北缘一路铺到水边
SHOP_Y0, SHOP_N, SHOP_PITCH, SHOP_LEN = 34.0, 10, 16.0, 15.0
SHOP_DEPTH = 12.0

# 高架 ＝ **跨水的弯桥**，不是跨街的直桥（bg3-1 / bg3-2：水面、对岸天际线、明显的平面弯、
# 旁边一座拱墩老桥）。它是主街往北的延续：街 → 匝道爬升 → 上桥 → 弯着跨过水面 → 对岸。
BRIDGE_Z = 9.3              # 桥面标高
RAMP_Y0, RAMP_Y1 = 190.0, 300.0       # 匝道：在主街上方爬升
BRIDGE_R = 900.0            # 平面曲线半径
BRIDGE_SWEEP = 0.72         # 弧度 → 弧长 648m，横向偏出 223m
DECK_HALF_W = 8.0           # 桥面 16m
PIER_PITCH = 30.0
WATER_Y0, WATER_Y1 = 330.0, 900.0     # 水面（河/海湾）
FARSHORE_Y0, FARSHORE_Y1 = 905.0, 1125.0   # 对岸天际线

# 洞门必须落在广场【之外】：广场是 60×60（y -30..30），旧 blend 把洞口放在 y=-20，
# 也就是广场里面——灰模一渲就看见拱门骑在广场地面上。引道从广场南缘 y=-30 起坡。
TUN_Y0, TUN_Y1 = -50.0, -200.0        # 洞门 / 洞尾，洞身 150m
TUN_RAMP_Y = -30.0          # 引道起点 ＝ 广场南缘
TUN_Z = -1.2                # 洞内路面标高（引道 20m 下坡 6%）
TUN_CLEAR_H = 6.0           # 净高
TUN_HALF_W = 6.0            # 总净宽 12m
CARRIAGE_HALF = 5.0         # 行车净宽 10m（两车道）
CURB_H = 0.4

# ── 基元 ────────────────────────────────────────────────────────────────────
COLS = {}


def collection(name):
    if name not in COLS:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
        COLS[name] = c
    return COLS[name]


def put(ob, col):
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    collection(col).objects.link(ob)


def box(name, col, center, size, rot_z=0.0):
    """Axis-aligned box by centre + full size."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.location = Vector(center)
    ob.rotation_euler[2] = rot_z
    put(ob, col)
    return ob


def loft(name, col, stations, section):
    """Sweep a 2D cross-section along a centreline.

    stations: [(x, y)] or [(x, y, z)] centreline points.
    section:  [(lateral, z)] closed profile, CCW, in the frame where +lateral is
              left of the direction of travel.
    """
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    rings = []
    n = len(stations)
    for i, st in enumerate(stations):
        x, y, z0 = (st + (0.0,))[:3] if len(st) == 2 else st
        nx, ny = stations[min(i + 1, n - 1)][:2]
        px, py = stations[max(i - 1, 0)][:2]
        t = Vector((nx - px, ny - py, 0.0))
        t.normalize()
        lat = Vector((-t.y, t.x, 0.0))          # 左法向
        rings.append([bm.verts.new(Vector((x, y, z0)) + lat * s + Vector((0, 0, z)))
                      for s, z in section])
    bm.verts.ensure_lookup_table()
    m = len(section)
    for i in range(n - 1):
        for j in range(m):
            k = (j + 1) % m
            bm.faces.new((rings[i][j], rings[i][k], rings[i + 1][k], rings[i + 1][j]))
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    put(ob, col)
    return ob


def prism(name, col, profile, y0, y1):
    """Extrude a 2D (x, z) polygon along Y. Used for the tunnel portal."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    front = [bm.verts.new((x, y0, z)) for x, z in profile]
    f = bm.faces.new(front)
    bmesh.ops.recalc_face_normals(bm, faces=[f])
    r = bmesh.ops.extrude_face_region(bm, geom=[f])
    moved = [e for e in r["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=Vector((0, y1 - y0, 0)), verts=moved)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    put(ob, col)
    return ob


# ── 干净起手 ────────────────────────────────────────────────────────────────
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.scene.unit_settings.system = "METRIC"

# ── BG1 广场 ────────────────────────────────────────────────────────────────
# 围合 ＝ 东西两道【连续街墙】（不是独立塔）+ 南北两块夹着 23m 开口的板楼。
# 依据 bg1-1 / bg1-2 / bg1-4：东壁玻璃幕墙 8–12 层，西壁旧楼 5–8 层。
box("BG1_PLAZA_GROUND", "BG1_PLAZA", (0, 0, -0.1), (60, 60, 0.2))
box("BG1_PLINTH", "BG1_PLAZA", (-9, 6, 0.6), (2.2, 2.2, 1.2))
box("BG1_PLINTH_STEP", "BG1_PLAZA", (-9, 6, 0.15), (3.4, 3.4, 0.3))

WALL_DEPTH = 18.0
SEG_LEN = 12.0
EAST_FLOORS = [10, 12, 9, 11, 8]            # 8–12 层 → 28.8–43.2m
EAST_SETBACK = [0.0, 0.8, 0.0, 1.2, 0.4]
WEST_FLOORS = [6, 5, 8, 7, 6]               # 5–8 层 → 18.0–28.8m
WEST_SETBACK = [0.6, 0.0, 1.0, 0.0, 0.8]

for i, (fl, sb) in enumerate(zip(EAST_FLOORS, EAST_SETBACK)):
    h = fl * FLOOR
    y = -PLAZA_HALF + SEG_LEN * (i + 0.5)
    box(f"BG1_EWALL_{i:02d}", "BG1_PLAZA",
        (PLAZA_HALF + sb + WALL_DEPTH / 2, y, h / 2), (WALL_DEPTH, SEG_LEN, h))
for i, (fl, sb) in enumerate(zip(WEST_FLOORS, WEST_SETBACK)):
    h = fl * FLOOR
    y = -PLAZA_HALF + SEG_LEN * (i + 0.5)
    box(f"BG1_WWALL_{i:02d}", "BG1_PLAZA",
        (-(PLAZA_HALF + sb + WALL_DEPTH / 2), y, h / 2), (WALL_DEPTH, SEG_LEN, h))

# 夹着开口的四块板楼：开口净宽 23m —— 铁律「走廊 ≥14m 且无遮挡」的兑现处
GATE_W = PLAZA_HALF - CORRIDOR_HALF          # 18.5
for tag, sy, floors in (("N", 1, (7, 8)), ("S", -1, (6, 7))):
    for side, sx, fl in (("L", -1, floors[0]), ("R", 1, floors[1])):
        h = fl * FLOOR
        box(f"BG1_{tag}GATE_{side}", "BG1_PLAZA",
            (sx * (CORRIDOR_HALF + GATE_W / 2),
             sy * (PLAZA_HALF + WALL_DEPTH / 2), h / 2),
            (GATE_W, WALL_DEPTH, h))

# ── BG2 主街 ────────────────────────────────────────────────────────────────
# 断面：车行道 15m + 人行道 4m×2 ＝ 楼到楼 23m（bg2-1 实读）
mid = (STREET_Y0 + STREET_Y1) / 2
span = STREET_Y1 - STREET_Y0
box("BG2_ROAD", "BG2_STREET", (0, mid, -0.1), (ROAD_HALF * 2, span, 0.2))
for side, sx in (("L", -1), ("R", 1)):
    box(f"BG2_WALK_{side}", "BG2_STREET",
        (sx * (ROAD_HALF + WALK_W / 2), mid, 0.075), (WALK_W, span, 0.15))

# 商铺：4–8 层、开间约 5m（每块 15m ＝ 3 开间）、沿街前后进退
L_FLOORS = [4, 6, 5, 8, 7, 4, 6, 5, 7, 8]
R_FLOORS = [5, 4, 7, 6, 8, 5, 4, 7, 6, 5]
SETBACK = [0.0, 0.8, 0.4, 1.2, 0.6, 0.0, 1.0, 0.4, 0.8, 0.2]
for i in range(SHOP_N):
    y = SHOP_Y0 + SHOP_LEN / 2 + SHOP_PITCH * i
    for side, sx, floors in (("L", -1, L_FLOORS), ("R", 1, R_FLOORS)):
        h = floors[i] * FLOOR
        sb = SETBACK[(i + (0 if side == "L" else 5)) % SHOP_N]
        box(f"BG2_SHOP_{i:02d}_{side}", "BG2_STREET",
            (sx * (CORRIDOR_HALF + sb + SHOP_DEPTH / 2), y, h / 2),
            (SHOP_DEPTH, SHOP_LEN, h))

# 商铺段（160m）之后到桥下这一截仍要有街墙夹着——bg1-1 里长街一路收敛到桥的剪影，
# 不会在中途豁然开阔。这一截没有店面，只有素体块。
FAR_L = [5, 7, 6]
FAR_R = [6, 4, 7]
for i in range(3):
    y = 201.0 + 7.5 + 16.0 * i
    for side, sx, floors in (("L", -1, FAR_L), ("R", 1, FAR_R)):
        h = floors[i] * FLOOR
        box(f"BG2_FARWALL_{i:02d}_{side}", "BG2_STREET",
            (sx * (CORRIDOR_HALF + 9.0), y, h / 2), (18.0, 15.0, h))

# 长街上方的横跨天桥：bg1-1 从广场望出去、bg5-1 从空中看，长街上方都有一道横跨结构。
# 它是**天桥**，不是 bg3 那座跨水高架（那座在城北的水面上）。两者别再混为一谈。
box("BG2_SKYBRIDGE", "BG2_STREET", (0, 150.0, 8.5), (CORRIDOR_HALF * 2, 6.0, 1.2))

# 广告屏：画左（西壁）4 块，屏心离地约两层楼高，间距 18m（bg2-1）
for i in range(4):
    box(f"BG2_SCREEN_{i:02d}", "BG2_STREET",
        (-(CORRIDOR_HALF + 0.2), 50.0 + 18.0 * i, 7.2), (0.4, 6.0, 4.0))

# 招牌拱架：广场开口以北 70m，跨全街，下缘净空 6.5m
box("BG2_SIGN_ARCH", "BG2_STREET", (0, 100.0, 7.1), (CORRIDOR_HALF * 2, 0.6, 1.2))
for side, sx in (("L", -1), ("R", 1)):
    box(f"BG2_ARCH_POST_{side}", "BG2_STREET",
        (sx * (CORRIDOR_HALF - 0.25), 100.0, 3.55), (0.5, 0.5, 7.1))

# ── BG3 高架 ────────────────────────────────────────────────────────────────
# 跨水弯桥：主街往北 → 匝道爬升 → 上桥 → 一道平面弯跨过水面 → 对岸城市。
# bg3-1 / bg3-2 两张都是这个：水在两侧、对岸密集天际线、明显的弯、旁边一座拱墩老桥。
def bridge_path():
    """[(x, y, z)] —— 匝道段（在主街上方爬升）+ 跨水段（等高、走圆弧）。"""
    pts = []
    n_ramp = 12
    for i in range(n_ramp + 1):
        u = i / n_ramp
        y = RAMP_Y0 + (RAMP_Y1 - RAMP_Y0) * u
        z = 0.2 + (BRIDGE_Z - 0.2) * (u * u * (3 - 2 * u))      # smoothstep，起坡收坡都平顺
        pts.append((0.0, y, z))
    n_arc = 48
    for i in range(1, n_arc + 1):
        th = BRIDGE_SWEEP * i / n_arc
        pts.append((BRIDGE_R * (1 - math.cos(th)),
                    RAMP_Y1 + BRIDGE_R * math.sin(th),
                    BRIDGE_Z))
    return pts


PATH = bridge_path()
BRIDGE_END = PATH[-1]

loft("BG3_DECK", "BG3_BRIDGE", PATH,
     [(-DECK_HALF_W, -0.6), (DECK_HALF_W, -0.6), (DECK_HALF_W, 0.0), (-DECK_HALF_W, 0.0)])
for side, sgn in (("L", -1), ("R", 1)):
    a, b = sgn * (DECK_HALF_W - 0.5), sgn * DECK_HALF_W
    lo, hi = min(a, b), max(a, b)
    loft(f"BG3_PARAPET_{side}", "BG3_BRIDGE", PATH, [(lo, 0.0), (hi, 0.0), (hi, 1.1), (lo, 1.1)])

# 桥墩：沿路径每 30m 一根，只在离地/离水面够高的地方立
acc, last = 0.0, None
n_pier = 0
for i, (x, y, z) in enumerate(PATH):
    if last is not None:
        acc += math.dist((x, y), last)
    last = (x, y)
    if z - 0.6 < 2.5 or (acc < PIER_PITCH and i):
        continue
    acc = 0.0
    box(f"BG3_PIER_{n_pier:02d}", "BG3_BRIDGE", (x, y, (z - 0.6) / 2), (3.0, 3.0, z - 0.6))
    n_pier += 1

# 水面：桥跨的就是它。previz 里它只是一块平面，管的是「这一段下面不是地」
box("BG3_WATER", "BG3_BRIDGE",
    ((WATER_Y1 - WATER_Y0) * 0.0 + 150.0, (WATER_Y0 + WATER_Y1) / 2, -0.25),
    (1300.0, WATER_Y1 - WATER_Y0, 0.5))

# 旁边那座拱墩老桥：bg3-1 与 bg3-2 都拍到了，是这一段水面的标志物
ALT = [(x - 150.0, y - 40.0, 6.5) for x, y, z in PATH if y >= WATER_Y0 - 30]
if len(ALT) > 3:
    loft("BG3_ALT_DECK", "BG3_BRIDGE", ALT,
         [(-7.0, -0.5), (7.0, -0.5), (7.0, 0.0), (-7.0, 0.0)])
    for i in range(0, len(ALT), 4):
        ax, ay, az = ALT[i]
        box(f"BG3_ALTPIER_{i // 4:02d}", "BG3_BRIDGE", (ax, ay, (az - 0.5) / 2),
            (4.0, 4.0, az - 0.5))

# ── BG4 隧道 ────────────────────────────────────────────────────────────────
# 断面：行车净宽 10m + 两侧 0.4m 高边石 ＝ 总净宽 12m，净高 6m（bg4-1 实读）
loft("BG4_RAMP", "BG4_TUNNEL",
     [(0.0, TUN_RAMP_Y), (0.0, TUN_Y0)],
     [(-TUN_HALF_W, -0.2), (TUN_HALF_W, -0.2), (TUN_HALF_W, 0.0), (-TUN_HALF_W, 0.0)])
for v in bpy.data.objects["BG4_RAMP"].data.vertices:   # 尾端整体下沉 → 6% 坡
    if v.co.y < TUN_Y0 + 0.01 and v.co.y > TUN_Y0 - 0.01:
        v.co.z += TUN_Z

tun_mid = (TUN_Y0 + TUN_Y1) / 2
tun_len = abs(TUN_Y1 - TUN_Y0)
ceil_z = TUN_Z + TUN_CLEAR_H
box("BG4_TUNNEL_FLOOR", "BG4_TUNNEL", (0, tun_mid, TUN_Z - 0.1), (TUN_HALF_W * 2, tun_len, 0.2))
box("BG4_TUNNEL_CEIL", "BG4_TUNNEL", (0, tun_mid, ceil_z + 0.15), (TUN_HALF_W * 2, tun_len, 0.3))
for side, sx in (("L", -1), ("R", 1)):
    box(f"BG4_TUNNEL_WALL_{side}", "BG4_TUNNEL",
        (sx * (TUN_HALF_W + 0.2), tun_mid, (TUN_Z + ceil_z) / 2),
        (0.4, tun_len, TUN_CLEAR_H))
    box(f"BG4_CURB_{side}", "BG4_TUNNEL",
        (sx * (CARRIAGE_HALF + 0.5), tun_mid, TUN_Z + CURB_H / 2),
        (1.0, tun_len, CURB_H))

# 顶灯：左右【双排】，排距 9m（bg4-1：两列，不是一列）
n_light = int((abs(TUN_Y1) - 4 - (abs(TUN_Y0) + 4)) / 9.0) + 1
for i in range(n_light):
    y = TUN_Y0 - 4.0 - 9.0 * i
    for side, sx in (("L", -1), ("R", 1)):
        box(f"BG4_LIGHT{side}_{i:02d}", "BG4_TUNNEL",
            (sx * 3.0, y, ceil_z - 0.15), (0.5, 2.4, 0.2))

# 拱形洞门：侧墙升到 3.0m 起拱，半椭圆收到净高 5.4m
ARCH_SPRING = TUN_Z + 3.6
prof = [(-15.0, TUN_Z), (-TUN_HALF_W, TUN_Z), (-TUN_HALF_W, ARCH_SPRING)]
for i in range(1, 24):
    a = math.pi * (1.0 - i / 24.0)
    prof.append((TUN_HALF_W * math.cos(a),
                 ARCH_SPRING + (ceil_z - ARCH_SPRING) * math.sin(a)))
prof += [(TUN_HALF_W, ARCH_SPRING), (TUN_HALF_W, TUN_Z), (15.0, TUN_Z),
         (15.0, TUN_Z + 11.0), (-15.0, TUN_Z + 11.0)]
prism("BG4_PORTAL", "BG4_TUNNEL", prof, TUN_Y0 - 1.5, TUN_Y0)

# ── FABRIC 城市肌理 ─────────────────────────────────────────────────────────
# 街区进深 40–80m、巷宽 4–8m、近广场 30–45m 高、边缘 15–20m（bg5-1 实读）。
# keep-out 让开全部走廊：广场 / 主街 / 隧道 / 桥。确定性种子——重跑得到同一座城。
KEEPOUT = [
    (-52, 52, -52, 52),                    # 广场 + 两道街墙 + 四块板楼
    (-26, 26, STREET_Y0, STREET_Y1),       # 主街走廊 + 两侧商铺
    (-18, 18, TUN_Y1 - 4, TUN_RAMP_Y),     # 隧道 + 引道
    (-700, 700, WATER_Y0 - 8, WATER_Y1),   # 水面：这一片不长楼
]
BRIDGE_CLEAR = 22.0


def blocked(cx, cy, hx, hy):
    for x0, x1, y0, y1 in KEEPOUT:
        if cx + hx > x0 and cx - hx < x1 and cy + hy > y0 and cy - hy < y1:
            return True
    for px, py, _ in PATH:                 # 让开桥的走廊（含匝道段）
        if abs(cx - px) - hx < BRIDGE_CLEAR and abs(cy - py) - hy < BRIDGE_CLEAR:
            return True
    return False


rng = random.Random(20260901)
BLOCK_PITCH = 60.0
# 覆盖范围要罩住【桥的全长】，不能用绕原点的圆形裁剪：桥在 y≈260、长 600m，
# 圆形裁到半径 320 就等于把桥两头旁边的城市全裁掉——桥上镜头（41/46/47/49/52）
# 一侧望出去会是空的。改成矩形范围，按需要拍到的东西定，不按到原点的距离定。
CITY_X, CITY_Y0, CITY_Y1 = 345.0, -300.0, 325.0
# 街区一律切成 2×2 个体量，远处也不要合成一整块：整块的 52m 底面一旦压到走廊
# 就会被整块剔掉，在桥边留出大洞（实测：合并后桥两侧 12 段里 5 段一栋楼都不剩）。
# 26m 的小体量塞得进走廊之间，城市才在桥全长上连续。
made = 0
for gx in range(-6, 7):
    for gy in range(-6, 8):
        bx = gx * BLOCK_PITCH + rng.uniform(-4, 4)
        by = gy * BLOCK_PITCH + rng.uniform(-4, 4)
        alley = rng.uniform(4.0, 8.0)
        bw = BLOCK_PITCH - alley                       # 街区进深 52–56m
        if abs(bx) > CITY_X or not (CITY_Y0 <= by <= CITY_Y1):
            continue
        dist = math.hypot(bx, by)
        core = max(0.0, 1.0 - dist / 280.0)
        base = 16.0 + core * 27.0                      # 边缘 16m → 近广场 43m
        for qx, qy in ((-1, 1), (1, 1), (-1, -1), (1, -1)):
            sx = bw / 2 * rng.uniform(0.82, 0.98)
            sy = bw / 2 * rng.uniform(0.82, 0.98)
            cx = bx + qx * bw / 4
            cy = by + qy * bw / 4
            if blocked(cx, cy, sx / 2, sy / 2):
                continue
            h = max(13.0, base * rng.uniform(0.82, 1.20))
            ob = box(f"FABRIC_BLOCK_{made:03d}", "FABRIC", (cx, cy, h / 2), (sx, sy, h))
            ob.rotation_euler[2] = rng.uniform(-0.04, 0.04)
            made += 1

# 打断天际线的高板楼：bg1-1 长街尽头、bg5-1 天际线上都有明显更高的一两栋。
# 没有它们，整座城从空中读成一张等高的席子。位置写死，不随机——它们是构图元素。
LANDMARKS = [(-155, 205, 74.0), (140, 95, 62.0), (-268, 120, 68.0),
             (215, -150, 58.0), (-250, -60, 66.0), (300, 60, 80.0)]
for i, (lx, ly, lh) in enumerate(LANDMARKS):
    box(f"FABRIC_TOWER_{i:02d}", "FABRIC", (lx, ly, lh / 2), (26.0, 22.0, lh))
    made += 1

# 对岸天际线：bg3-2 里桥的尽头是一片密集高层，是这两张图的画面主体之一。
# 密度和高度都比近岸高——它是"另一半城市"，不是背景板。
rng2 = random.Random(20260902)
for gx in range(-4, 12):
    for gy in range(0, 4):
        cx = -220.0 + gx * 62.0 + rng2.uniform(-6, 6)
        cy = FARSHORE_Y0 + 30.0 + gy * 62.0 + rng2.uniform(-6, 6)
        if cy > FARSHORE_Y1:
            continue
        for qx, qy in ((-1, 1), (1, 1), (-1, -1), (1, -1)):
            sx = 26.0 * rng2.uniform(0.7, 0.95)
            sy = 26.0 * rng2.uniform(0.7, 0.95)
            h = rng2.uniform(28.0, 95.0)
            ob = box(f"FABRIC_SHORE_{made:03d}", "FABRIC",
                     (cx + qx * 15.0, cy + qy * 15.0, h / 2), (sx, sy, h))
            ob.rotation_euler[2] = rng2.uniform(-0.03, 0.03)
            made += 1

# ── 报告 ────────────────────────────────────────────────────────────────────
bpy.context.view_layer.update()          # matrix_world 在 depsgraph 更新前是陈的
lo = Vector((1e9,) * 3)
hi = Vector((-1e9,) * 3)
for ob in bpy.context.scene.objects:
    if ob.type != "MESH":
        continue
    for c in ob.bound_box:
        w = ob.matrix_world @ Vector(c)
        lo = Vector(tuple(min(lo[i], w[i]) for i in range(3)))
        hi = Vector(tuple(max(hi[i], w[i]) for i in range(3)))

print("=== BUILD entropy_city ===")
for name in ("BG1_PLAZA", "BG2_STREET", "BG3_BRIDGE", "BG4_TUNNEL", "FABRIC"):
    print(f"  {name:12s} {len(collection(name).objects):4d} objects")
print(f"  TOTAL        {len(bpy.context.scene.objects):4d}")
print(f"  bbox min({lo.x:.1f},{lo.y:.1f},{lo.z:.1f}) max({hi.x:.1f},{hi.y:.1f},{hi.z:.1f})"
      f"  span {hi.x - lo.x:.1f} x {hi.y - lo.y:.1f} x {hi.z - lo.z:.1f}")
print(f"  广场→主街走廊净宽 {CORRIDOR_HALF * 2:.1f}m  ＝ {CORRIDOR_HALF * 2 / CAR_LEN:.1f} 个车长")
print(f"  隧道净宽 {TUN_HALF_W * 2:.1f}m / 行车 {CARRIAGE_HALF * 2:.1f}m / 净高 {TUN_CLEAR_H:.1f}m")
_blen = sum(math.dist(PATH[i][:2], PATH[i + 1][:2]) for i in range(len(PATH) - 1))
print(f"  桥全长 {_blen:.0f}m（匝道+跨水）  桥面宽 {DECK_HALF_W * 2:.0f}m  {n_pier} 墩"
      f"  横向偏出 {BRIDGE_END[0]:.0f}m  终点 y={BRIDGE_END[1]:.0f}")
print(f"  水面 y {WATER_Y0:.0f}→{WATER_Y1:.0f}  对岸 y {FARSHORE_Y0:.0f}→{FARSHORE_Y1:.0f}")

bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED " + OUT)
