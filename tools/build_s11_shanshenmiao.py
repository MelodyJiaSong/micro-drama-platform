# -*- coding: utf-8 -*-
"""Build s11_十里坡山神庙.blend from scratch — the previz geometry source.

Every number here comes from ONE place: the geometry table in
`ai_videos/xianjian_yi_mv/2_世界观人设/scenes/s11_十里坡山神庙/_blender/blender_build.md` §4,
which is itself read off the world anchor image `bg1_庙前空地/bg1-1.png`.

Why a builder and not hand-edits (ai_video.md rule 4h §D): the `.blend` is gitignored
(media lives in R2), so a hand-edited blend has no reviewable source. This script IS
the source — delete the blend, re-run, get the identical place. It supersedes the
hand-built `s11_十里坡山神庙.blend` (retired to `_deleted/xianjian_yi_mv_20260905/`).

Geometry only — no materials, no lights, no decoration (rule 4g §D: the .blend carries
几何, the reference image carries 长相).

Coordinate frame — **inherited from the validated shot12 previz contract**, not invented here.
`shot12_previz.py` solves its camera from these three numbers; the scene must be built in the
same frame or the previz framing report (庙/人头 的 UV) stops meaning anything:

    P (酒剑仙站位 / 动作中心) = (0, 4, 0)
    CAM_AZ (相机 → 主体的水平方向) = (-0.259, 0.966, 0)   → 机位在主体的【南偏东】
    TEMPLE (小庙中心) = (-21, 19, 0)                      → 主体西北 25.8m，落在画左作边框

    解出来的机位：pos ≈ (3.44, -8.84, 5.74)，aim ≈ (-2.11, 3.44, 0.90)，35mm，俯角 20°
    主体处画框 8.18m(高) × 14.55m(宽)；庙所在深度 33.2m 处画框半宽 17.1m，
    庙的横向偏移 16.4m < 17.1m → 庙贴着画左边缘进画。**这一条是本文件全部坐标的由来。**

    +X = 东   +Y = 北   +Z = 上

Precision grading (rule 4g §E) — driven by what shot12 actually frames:
    B 级（体块 + 屋顶形制 + 开窗位置）：小庙、矮木栅栏
    C 级（纯体块剪影）：密林树冠、山壁、上坡小路
    D（不建）：拉远一档之外的一切；野草、枯叶、苔痕（属长相，归参考图与出片模型）

Run:
  blender -b --factory-startup --python tools/build_s11_shanshenmiao.py -- <out.blend>
"""
import math
import sys

import bpy
from mathutils import Vector

sys.stdout.reconfigure(encoding="utf-8")
OUT = sys.argv[sys.argv.index("--") + 1:][0]

# ── previz 契约（与 shot12_previz.py 的同名常量必须逐值一致）────────────────
P = Vector((0.0, 4.0, 0.0))                  # 酒剑仙站位 / 动作中心
CAM_AZ = Vector((-0.259, 0.966, 0.0))        # 相机 → 主体的水平方向
R_VEC = Vector((CAM_AZ.y, -CAM_AZ.x, 0.0))   # 画面向右
CAM_LENS, SUBJ_FRAC, TILT_DEG, PULL = 35.0, 0.22, 20.0, 1.30
SENSOR_W = 36.0
SENSOR_V = SENSOR_W * 1080.0 / 1920.0

# ── 唯一量尺 ────────────────────────────────────────────────────────────────
MAN_H = 1.80                # 酒剑仙身高（previz_config ["体型"].body_height_m）
ZHANG = 3.33                # 一丈

FRAME_H = MAN_H / SUBJ_FRAC                  # 主体处画框高 8.18m
FRAME_W = FRAME_H * 1920.0 / 1080.0          # 主体处画框宽 14.55m
D_SUBJ = FRAME_H * CAM_LENS / SENSOR_V       # 相机到主体 14.14m
CAM_POS = (P + Vector((0.0, 0.0, 0.9))
           - CAM_AZ * (D_SUBJ * math.cos(math.radians(TILT_DEG)))
           + Vector((0.0, 0.0, D_SUBJ * math.sin(math.radians(TILT_DEG)))))

# 空地：镜头要铺得开「贴地绕行数丈 + 群剑成环 + 腾空翻落」，且拉远一档后四面仍留余量。
# 按 rule 4h §E —— 范围由【镜头要拍到什么】定，不由「场地设定有多大」定。
# 画框在最远处（庙那一带，深 33m）半宽 17m，故硬土面要盖到 x −30…+16、y −12…+28。
FIELD_X0, FIELD_X1 = -30.0, 16.0
FIELD_Y0, FIELD_Y1 = -12.0, 28.0

# 小庙：单开间，通面阔一丈五 ≈ 5m。位置由 previz 契约钉死（画左边框），不可随手挪
TEMPLE_POS = Vector((-21.0, 19.0, 0.0))
TEMPLE_W, TEMPLE_D = 5.0, 4.2          # 通面阔 × 进深
TEMPLE_WALL_H = 2.8                    # 檐口（墙高）
TEMPLE_RIDGE_H = 4.6                   # 脊高 → 四坡顶举高 1.8m
TEMPLE_EAVE = 1.2                      # 出檐很深且压得低
TEMPLE_YAW = math.radians(-58.0)       # 正面朝东南 ＝ 朝机位；门开在正面
DOOR_W, DOOR_H = 1.3, 2.15             # 门洞高约七尺
WIN_W, WIN_H = 1.0, 1.1                # 窗宽约三尺
STEP_N, STEP_H, STEP_D = 2, 0.14, 0.45

# 矮木栅栏：场地南界。**它不在 shot12 的画框里**——shot12 只有 14m 机距、20° 俯角，
# 画面下缘就是身前几米的裸地。锚点图里那道栅栏属于一幅更宽的建场构图，不是本镜的构图。
# 建它是为 shot11（落幅）与将来的宽镜留几何，不是为 shot12。（rule 4g §E / 4h §E）
FENCE_N = 26
FENCE_SEG = 1.5
FENCE_H = 0.9
FENCE_MID = Vector((-5.0, -10.5, 0.0))
FENCE_YAW = math.radians(6.0)          # 近乎东西向，略斜

# 上坡小路：自空地东北向东北斜上坡（C 级）
PATH_W = 2.5
PATH_A = Vector((13.0, 16.0, 0.0))
PATH_B = Vector((31.0, 34.0, 3.2))

# 密林 / 山壁：包住北半圈 + 庙后。C 级纯体块，只为遮挡与构图边框服务
CANOPY_R0, CANOPY_R1 = 34.0, 50.0
CANOPY_H0, CANOPY_H1 = 8.0, 14.0
CLIFF_R = 64.0
CLIFF_H = 18.0

COLS = {}


def collection(name):
    if name not in COLS:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
        COLS[name] = c
    return COLS[name]


def box(coll, name, center, size, yaw=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = Vector(size)
    ob.location = Vector(center)
    ob.rotation_euler[2] = yaw
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    collection(coll).objects.link(ob)
    return ob


def wipe():
    bpy.ops.wm.read_factory_settings(use_empty=True)


wipe()

# ── 地面：空地 + 一圈外扩的草地基面（草本身不建，只给一个可站可投影的面）────────
_fcx, _fcy = (FIELD_X0 + FIELD_X1) / 2, (FIELD_Y0 + FIELD_Y1) / 2
_fw, _fd = FIELD_X1 - FIELD_X0, FIELD_Y1 - FIELD_Y0
box("S11_GROUND", "GND_field", (_fcx, _fcy, -0.05), (_fw, _fd, 0.1))
box("S11_GROUND", "GND_apron", (_fcx, _fcy, -0.16), (_fw + 60, _fd + 60, 0.1))

# ── 小庙（B 级：体块 + 四坡顶形制 + 门窗位置）──────────────────────────────
tx, ty, _ = TEMPLE_POS
box("S11_TEMPLE", "TMP_body", (tx, ty, TEMPLE_WALL_H / 2),
    (TEMPLE_W, TEMPLE_D, TEMPLE_WALL_H), TEMPLE_YAW)

# 四坡顶：三段收分的板叠出举折，够读出「小青瓦四坡顶」的形制而不建瓦垄
roof_layers = 3
for i in range(roof_layers):
    f = i / roof_layers
    w = TEMPLE_W + TEMPLE_EAVE * 2 * (1.0 - f)
    d = TEMPLE_D + TEMPLE_EAVE * 2 * (1.0 - f)
    z = TEMPLE_WALL_H + (TEMPLE_RIDGE_H - TEMPLE_WALL_H) * f
    h = (TEMPLE_RIDGE_H - TEMPLE_WALL_H) / roof_layers
    box("S11_TEMPLE", f"TMP_roof{i + 1}", (tx, ty, z + h / 2), (w, d, h), TEMPLE_YAW)

# 门洞（朝南 = −Y）：挖不动布尔，就用一块内凹的暗板表达「门内纯黑」
_fwd = Vector((math.sin(TEMPLE_YAW), -math.cos(TEMPLE_YAW), 0.0))   # 正面朝外的法线
_rgt = Vector((math.cos(TEMPLE_YAW), math.sin(TEMPLE_YAW), 0.0))    # 沿正面向右


def on_face(out, side, z):
    q = TEMPLE_POS + _fwd * (TEMPLE_D / 2 + out) + _rgt * side
    return (q.x, q.y, z)


box("S11_TEMPLE", "TMP_door", on_face(-0.12, 0.0, DOOR_H / 2), (DOOR_W, 0.22, DOOR_H), TEMPLE_YAW)
for i in range(STEP_N):
    box("S11_TEMPLE", f"TMP_step{i + 1}",
        on_face(STEP_D * (i + 0.5), 0.0, STEP_H * (STEP_N - i) - STEP_H / 2),
        (DOOR_W + 0.9, STEP_D, STEP_H), TEMPLE_YAW)
# 门旁红漆木格窗 + 独立小披檐（位置要对，长相归参考图）
box("S11_TEMPLE", "TMP_window", on_face(-0.10, 1.55, 1.55), (WIN_W, 0.18, WIN_H), TEMPLE_YAW)
box("S11_TEMPLE", "TMP_win_eave", on_face(0.22, 1.55, 2.28), (WIN_W + 0.5, 0.6, 0.12), TEMPLE_YAW)

# ── 矮木栅栏（B 级：逐段桩，previz 要它作画面下缘的前景基准线）──────────────
for i in range(FENCE_N):
    t = (i - (FENCE_N - 1) / 2) * FENCE_SEG
    px = FENCE_MID.x + math.cos(FENCE_YAW) * t
    py = FENCE_MID.y + math.sin(FENCE_YAW) * t
    h = FENCE_H * (0.86 + 0.28 * ((i * 7) % 5) / 4.0)      # 高低不齐，确定性、不随机
    lean = math.radians(-4.0 + 2.0 * ((i * 3) % 5))
    ob = box("S11_FENCE", f"FEN_post{i + 1:02d}", (px, py, h / 2), (0.12, 0.12, h), FENCE_YAW)
    ob.rotation_euler[0] = lean
box("S11_FENCE", "FEN_rail",
    (FENCE_MID.x, FENCE_MID.y, FENCE_H * 0.62),
    (FENCE_N * FENCE_SEG, 0.08, 0.09), FENCE_YAW)

# ── 上坡小路（C 级：一条抬起的带）───────────────────────────────────────────
seg = 8
for i in range(seg):
    a = PATH_A.lerp(PATH_B, i / seg)
    b = PATH_A.lerp(PATH_B, (i + 1) / seg)
    mid = (a + b) / 2
    L = (b - a).length
    yaw = math.atan2(b.y - a.y, b.x - a.x)
    box("S11_PATH", f"PTH_{i + 1:02d}", (mid.x, mid.y, mid.z + 0.05), (L, PATH_W, 0.1), yaw)

# ── 密林树冠 + 山壁（C 级纯体块，包北半圈与庙后）────────────────────────────
n_tree = 46
for i in range(n_tree):
    # 确定性角度分布：从西南（庙后）扫到东北，跳过东南（机位方向）
    a = math.radians(150.0 + 240.0 * i / (n_tree - 1))
    r = CANOPY_R0 + (CANOPY_R1 - CANOPY_R0) * (((i * 13) % 7) / 6.0)
    h = CANOPY_H0 + (CANOPY_H1 - CANOPY_H0) * (((i * 5) % 9) / 8.0)
    w = 4.0 + 3.0 * (((i * 11) % 6) / 5.0)
    box("S11_FOREST", f"TRE_{i + 1:02d}",
        (P.x + math.cos(a) * r, P.y + math.sin(a) * r, h / 2), (w, w, h))
n_cliff = 9
for i in range(n_cliff):
    a = math.radians(170.0 + 200.0 * i / (n_cliff - 1))
    box("S11_FOREST", f"CLF_{i + 1}",
        (P.x + math.cos(a) * CLIFF_R, P.y + math.sin(a) * CLIFF_R, CLIFF_H / 2),
        (26.0, 26.0, CLIFF_H))

# ── 报告 ────────────────────────────────────────────────────────────────────
bpy.context.view_layer.update()
lo = Vector((1e9,) * 3)
hi = Vector((-1e9,) * 3)
for ob in bpy.context.scene.objects:
    if ob.type != "MESH":
        continue
    for c in ob.bound_box:
        w = ob.matrix_world @ Vector(c)
        lo = Vector(tuple(min(lo[i], w[i]) for i in range(3)))
        hi = Vector(tuple(max(hi[i], w[i]) for i in range(3)))

print("=== BUILD s11_十里坡山神庙 ===")
for name in ("S11_GROUND", "S11_TEMPLE", "S11_FENCE", "S11_PATH", "S11_FOREST"):
    print(f"  {name:12s} {len(collection(name).objects):4d} objects")
print(f"  TOTAL        {len(bpy.context.scene.objects):4d}")
print(f"  bbox min({lo.x:.1f},{lo.y:.1f},{lo.z:.1f}) max({hi.x:.1f},{hi.y:.1f},{hi.z:.1f})"
      f"  span {hi.x - lo.x:.1f} x {hi.y - lo.y:.1f} x {hi.z - lo.z:.1f}")
print(f"  硬土面 {_fw:.0f} x {_fd:.0f}m ＝ {_fw / MAN_H:.1f} 个身高宽")
print(f"  小庙 通面阔 {TEMPLE_W:.1f}m（{TEMPLE_W / ZHANG:.1f} 丈）脊高 {TEMPLE_RIDGE_H:.1f}m"
      f"  ＝ 硬土面横宽的 1/{_fw / TEMPLE_W:.0f}")
print(f"  栅栏 {FENCE_N} 段 / 段长 {FENCE_SEG:.1f}m / 桩高 ~{FENCE_H:.1f}m")

# ── 自查：几何是否落在 shot12 的画框里（rule 4h §E —— 覆盖范围按镜头定）────────
# 建完就算一遍，不必等渲图。u=0 画左缘 / u=1 画右缘 / v=0 画下缘 / v=1 画上缘。
AIM = P + Vector((0.0, 0.0, 0.9)) - R_VEC * (FRAME_W * 0.15)


def uv_of(pt, pull=1.0):
    """把世界点投到画框坐标。pull>1 ＝ 拉远一档后的画框。"""
    cam = (P + Vector((0.0, 0.0, 0.9))
           - CAM_AZ * (D_SUBJ * pull * math.cos(math.radians(TILT_DEG)))
           + Vector((0.0, 0.0, D_SUBJ * pull * math.sin(math.radians(TILT_DEG)))))
    fwd = (AIM - cam).normalized()
    rgt = fwd.cross(Vector((0.0, 0.0, 1.0))).normalized()
    up = rgt.cross(fwd).normalized()
    v = pt - cam
    depth = v.dot(fwd)
    if depth <= 0.01:
        return None
    half_v = math.tan(math.atan(SENSOR_V / 2.0 / CAM_LENS)) * depth
    half_u = half_v * 1920.0 / 1080.0
    return 0.5 + v.dot(rgt) / (2 * half_u), 0.5 + v.dot(up) / (2 * half_v)


print("  --- 画框自查（shot12 起幅机位）---")
# want: True = 本镜必须在画内；False = 本镜画外是【设计如此】（为 shot11 / 宽镜而建）
checks = [
    ("庙右缘", TEMPLE_POS + _rgt * (TEMPLE_W / 2 + TEMPLE_EAVE) + Vector((0, 0, 1.5)), True),
    ("庙脊", TEMPLE_POS + Vector((0, 0, TEMPLE_RIDGE_H)), False),
    ("人头", P + Vector((0, 0, MAN_H)), True),
    ("人脚", P, True),
    ("栅栏中", FENCE_MID + Vector((0, 0, FENCE_H)), False),
    ("路起点", PATH_A, False),
]
bad = 0
for label, pt, must in checks:
    r = uv_of(pt)
    inside = r is not None and 0 <= r[0] <= 1 and 0 <= r[1] <= 1
    if must and not inside:
        bad += 1
    note = ("✓在画内" if inside else ("✗本镜必须在画内，却出画" if must else "—画外（设计如此，供 shot11/宽镜）"))
    pos = "镜后" if r is None else f"u={r[0]:6.3f} v={r[1]:6.3f}"
    print(f"    {label:8s} {pos}  {note}")
_t = uv_of(TEMPLE_POS + Vector((0, 0, TEMPLE_RIDGE_H)))
print(f"  庙落在画左边框？{'✓' if _t and 0.0 <= _t[0] <= 0.30 else '✗ —— 挪 TEMPLE_POS 或改 AIM_SHIFT'}")
print(f"  必须在画内的点，出画 {bad} 个" + ("" if bad == 0 else "  ← 先修这个再往下做 previz"))

bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED " + OUT)
