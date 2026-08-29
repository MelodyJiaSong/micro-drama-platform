"""shot12 previz（30s 合并镜）—— 在 s11 场景副本里搭一套彩色 proxy，按 shot12.md 的 `动作:` 时间轴 K 满 30 秒。

第一幕 0–15s ＝ 原 shot12 previz（15s 版）**逐值一致、不压缩**（用户 2026-08-18 裁定）；
第二幕 15–30s ＝ 原 shot13（22.5s 版）压进 15s，用户裁定的三处不动：剑气 0.22/0.26s（快）、一化多 1.4s 与平转 5.6s（慢）。

用法（本目录）：
    cp ../../../../2_世界观人设/scenes/s11_十里坡山神庙/s11_十里坡山神庙.blend shot12_previz.blend
    blender -b shot12_previz.blend --python build_previz.py            # 默认俯角 20°
    blender -b shot12_previz.blend --python build_previz.py -- 24      # 换俯角
    blender -b shot12_previz.blend -a                                  # 渲 PNG 序列 frames/f####.png
    ffmpeg -y -framerate 24 -i frames/f%04d.png -c:v libx264 -pix_fmt yuv420p -crf 18 shot12_previz.mp4

脚本只动副本，绝不写回 2_世界观人设/scenes 下的原场景文件。人形 proxy 用 tools/previz_rig.py（rule 12.16 §3）。

proxy 配色（Seedance 靠颜色认人认物）：
    绿 / 亮黄绿 = 酒剑仙（带关节人形，手掌与脚亮黄绿）
    蓝 = 长剑 / 二十把长剑（亮蓝＝裹着剑光；插地后转暗灰蓝＝光灭恢复金属本色）
    暗蓝灰 = 剑鞘（留背上不动）
    红 = 酒葫芦
    黑 + 土黄 = 两道沟壑（沟内全黑深槽 + 两侧土垄）—— 示意级
    青 = 地面剑气环 / 光柱 / 剑气薄片 —— 示意级低亮度，不是成品特效（follow-up 040）
"""
import math
import random
import sys

import bpy
from pathlib import Path

_here = Path(__file__).resolve()
for _anc in _here.parents:
    if (_anc / "tools" / "previz_rig.py").is_file():
        sys.path.insert(0, str(_anc))
        break
from mathutils import Euler, Matrix, Vector

from tools.previz_config import apply_config  # noqa: E402
from tools.previz_human import attach_mpfb_human  # noqa: E402
from tools.previz_rig import (  # noqa: E402
    HAND_GRIP, HAND_RELAX, HAND_SEAL_WRAP, HAND_SWORD_FINGER,
    HIP_Z, SHOULDER_X, PrevizRig, elbow_pos, solve_arm, solve_report,
)

# 场景主档（仓库相对路径）：webapp「出片」按钮据此自动 copy + 重建本 .blend（follow-up 058）
SCENE_MASTER = "ai_videos/xianjian_yi_mv/2_世界观人设/scenes/s11_十里坡山神庙/s11_十里坡山神庙.blend"

FPS = 24
TOTAL = 678  # 28.2s ＝ 第一幕 15.0s（＝ shot12 previz 原样）+ 第二幕 13.2s（follow-up 050：头顶平转 5.6→2.8s，省出的 2.8s 一部分还给插地/跳跃/跟斗/大笑，其余直接从总长剪掉——不必凑满 30s）

TEMPLE = Vector((-21.0, 19.0, 0.0))
P = Vector((0.0, 4.0, 0.0))

_argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
CAM_AZ = Vector((-0.259, 0.966, 0.0))
CAM_LENS = 35.0
BODY_H = 1.70
# 与 shot12 previz 同一套机位公式（follow-up 040：人占画高 ≈1/4.5、俯角 20°，庙仍在画内且四肢可辨）
SUBJ_FRAC = 0.22
# ---- 体型（rule 12.16 §0.2）：写人话，不写 MPFB 原始参数 ----
BODY_HEIGHT_M = 1.80        # 目标身高（米）。按实测标定表反查 MPFB height 参数
BODY_BUILD = 0.60           # 体格 0..1：瘦 → 壮（同时驱动 muscle 与 weight）
BODY_AGE = 0.62             # 年龄档 0..1。**必须 ≥0.5**，低于 0.5 是儿童生长曲线
BODY_GENDER = 1.0           # 1 男 / 0 女
BODY_PROPORTIONS = 0.55     # 比例 0..1：敦实 → 修长
TILT_DEG = 20.0
SENSOR_V = 36.0 * 9.0 / 16.0
PULL_FACTOR = 1.30                     # 齐冲夜空时机位向后拉开一档（视野放大 30%）
AIM_SHIFT_FRAC = 0.15                  # 视觉中心左移量（画宽比例）
BODY_YAW_DEG = -30.0                   # 身体侧转角（三分面；负=转向画左/庙）
RING_R_FRAC = 0.16                     # 高空二十剑成环半径（画宽比例）
GROUND_R_FRAC = 0.20                   # 落地剑环基准半径（画宽比例）
RISE_FRAC = 8.0                        # 冲出画面上缘的高度（画高倍数）
SEED = 13                              # 落点散布的随机种子

HIP_Z = 0.90
N_SWORDS = 20
# —— MVP 语义键（follow-up 055）：config 只暴露这些粗粒度参数，细节由下方派生 ——
ORBIT_TIME = 1.10       # 剑绕身一圈的用时（秒）→ 派生 A_ORBIT1
STOMP_COUNT = 3         # 右脚快跺几下 → 派生 A_STOMPS / A_STOMP_DUST 数组
STOMP_GAP = 0.28        # 相邻两跺的间隔（秒）
STOMP_DUST_LAG = 0.12   # 扬尘晚于跺脚的延迟（秒）
RING_COUNT = 4          # 光环圈数
# —— 肘部形态（follow-up 059：修「鸡翅膀肘」，用户可配）——
SEAL_ELBOW_FLARE = 40.0     # 掐诀时肘外张角：0=肘尖垂直垂在肩下贴身，正=向外拐，负=向里夹（度）
FINGER_ELBOW_FLARE = 40.0   # 剑指横抱臂的肘外张角，含义同上
RING_GAP = 0.30         # 相邻两圈的起扩间隔（秒）
# —— 时长链（follow-up 057）：动作顺序固定、逐段首尾相接；config 只填每段 duration，
#    段起点 = 前面各段时长之和，段内细节节拍按「该段时长 / 默认时长」等比伸缩，总长 = Σ。
DUR_FALL = 2.70
DUR_DRINK = 1.60
DUR_GOURD = 1.02
DUR_SEAL = 0.88
DUR_SWORD_IN = 2.05
DUR_RINGS = 1.55
DUR_ORBIT = 2.30
DUR_PILLAR = 1.90
DUR_GRIP = 1.00
DUR_SLASH = 1.50
DUR_THROW = 1.50
DUR_SPLIT = 1.40
DUR_SPIN = 2.80
DUR_RISE = 0.70
DUR_DROP = 2.18
DUR_JUMP = 1.14
DUR_FLIP = 0.73
DUR_SHEATH = 0.40
DUR_LAUGH = 0.85
AIR_SPINS = 2           # 单脚跳起后绕竖直体轴转几圈
FLIP_COUNT = 2          # 跃开后翻几个前空翻
STAND_Z = BODY_H                       # 踩剑悬空：脚底离地约一个身高

# ---------------------------------------------------------------- 时间轴（秒）
# ================= 第一幕（＝ shot12 的 15s 时间轴，逐值一致，不压缩）=================
# 用户 2026-08-18 裁定：合并镜的前半段必须与 shot12 previz 完全一致（此前按 0.83 压到 12.5s
# 是不对的）。因此第一幕原样占 0–15.0s，第二幕（原 shot13·22.5s 版）压进 15.0–30.0s。
FALL_SPINS = 5          # 下落自转圈数
ORBIT_R = 2.10          # 绕身半径：整圈轨迹都在人的剪影之外
ORBIT_Z = 1.35          # 悬停/绕行高度
LUNGE_SINK = 0.11       # 弓步沉胯

A_ENTER = 0.30          # 入场点（画外右上角）
A_LAND = 2.00           # 双脚砸地
A_LAND_DIP = 2.12       # 落地屈膝最低点
A_LAND_UP = 2.32        # 起身站定
A_DRINK_IN = 2.70       # 葫芦口抵唇
A_DRINK_OUT = 3.35      # 放下葫芦
A_SWAY_A = 3.50         # 身形一晃
A_SWAY_B = 3.80
A_STEADY = 4.15         # 晃定
A_WINDUP = 4.30         # 抛壶起手
A_RELEASE = 4.45        # 脱手
A_GOURD_APEX = 4.62     # 平抛最高点
A_GOURD_BOUNCE = 4.85   # 触地弹一下
A_GOURD_REST = 5.10     # 翻滚两圈停住
A_ARM_BACK = 5.00       # 抛完手臂回位
A_SEAL = 5.35           # 两手掐诀到位
A_STOMPS = (5.32, 5.60, 5.88)   # 右脚快跺三下的起拍
A_STOMP_DUST = (5.44, 5.72, 6.00)
A_SEAL_END = 6.20       # 结印段收
A_SWORD_OUT = 6.20      # 剑自行出鞘
A_SWORD_LEAVE = 6.32    # 离开背部
A_SWORD_TOP = 6.95      # 越过头顶（不冲天，用户 2026-08-18）
A_SWORD_HOLD = 7.20     # 在身前下落中
A_SWORD_HOVER = 8.10    # 身前悬停到位（竖直、剑尖朝下，随后微幅上下浮动）
A_RING_T0 = (8.25, 8.55, 8.85, 9.15)  # 四圈依次起扩
A_RING_MAX = 9.80       # 扩到最大即停
A_FINGER = 10.80        # 两手剑指 + 右脚前迈到位
A_ORBIT0 = 11.00        # ★ 绕身起
A_ORBIT1 = 12.10        # ★ 绕身收（1.1s 走完一整圈）
A_PILLAR0 = 12.10       # 光柱自地面升起
A_PILLAR_TOP = 13.30    # 走到最高
A_PILLAR_GONE = 14.00   # 自顶端散尽
A_GRIP0 = 14.00         # 剑开始落向右掌
A_GRIP1 = 14.50         # 握住
A_FADE0 = 14.00         # 地面光圈开始褪成暗痕
A_FADE1 = 14.80
ACT2_T0 = 15.00         # 第二幕起点（＝ shot12 的 TOTAL）

# ================= 第二幕（原 shot13·拍 11–22）=================
# 22.5s 版压进 15.0s（37.5 → 30 的全部 7.5s 都在这一幕砍），但**用户裁定的三处一律不动**：
# 剑气 0.22/0.26s（要快）、一化多 1.4s（要慢）；平转按 follow-up 050 减半为一圈 2.8s；压缩落在助跑与收势的尾巴。
# 固定 7.48s + 弹性 7.52s。**最后一个关键帧必须 ≤ 30.0s**（超出的会被静默截掉）。
def _a2(t: float) -> float:
    return ACT2_T0 + t

T_WIND1 = _a2(0.25)     # 沉肩坠肘起手
T_SLASH1 = _a2(0.45)    # 第一剑斩出
T_QI1_END = _a2(0.67)   # 剑气 0.22s 飞完全长（快，不压缩）
T_WIND2 = _a2(0.90)
T_SLASH2 = _a2(1.08)    # 第二剑侧斩
T_ARC_END = _a2(1.34)   # 月牙剑气 0.26s（快，不压缩）
T_THROW_WIND = _a2(1.50)
T_THROW = _a2(1.65)     # 脱手
T_SWORD_HIGH = _a2(2.20)  # 剑到高空停住
T_SEAL = _a2(2.50)      # 单手两指收胸前
T_EYES_CLOSED = _a2(2.90)  # 闭眼定住
T_SPLIT = _a2(3.00)     # 分化起
T_SPLIT_DONE = _a2(4.40)   # 1.4s 展开（慢，不压缩）
SPIN_TURNS = 1          # follow-up 050：转圈时间至少减半——一圈 2.8s，保住「每把剑走向看得清」的慢
T_SPIN_END = _a2(7.20)     # 平转一圈 2.8s（follow-up 050 减半）
T_RISE_END = _a2(7.80)
T_PULL0, T_PULL1 = _a2(7.20), _a2(7.90)
T_POINT = _a2(8.25)    # 睁眼亮相指地
T_DROP0 = _a2(8.40)
T_DROP_SPAN = 1.30      # follow-up 050：还给逐把插地一点时间      # 二十把落完
T_DROP_DUR = 0.34
T_RING_DONE = _a2(10.00)   # 插定成环（决定性瞬间）
T_JUMP0 = _a2(10.08)
T_JUMP_TOP = _a2(10.32)
T_JUMP1 = _a2(10.56)
T_GATHER1 = _a2(10.80)
T_MERGE = _a2(10.82)    # 合成一柄竖直悬于单脚正下方
T_BOUNCE = (_a2(10.90), _a2(10.98), _a2(11.06), _a2(11.16))
T_FLIP0 = _a2(11.22)
T_FLIP1 = _a2(11.85)    # 翻两个跟斗落地
T_LAND_DIP = _a2(11.92)
T_LAND_UP = _a2(12.08)
T_SWORD_UP = _a2(11.95)
T_SWORD_APEX = _a2(12.08)
T_SHEATH = _a2(12.30)   # 归背鞘、剑光灭
T_LAUGH = _a2(12.34)
T_LAUGH_BOBS = (_a2(12.50), _a2(12.66), _a2(12.82))
# ---------------------------------------------------------------- 用户配置（follow-up 051）
# previz_config.toml 与本脚本同目录：按「动作段 × 主体」组织，用户直接改秒数/圈数/机位。
# 键名 = 常量名小写；见 tools/previz_config.py 的契约。CLI 俯角参数仍最高优先。
_applied = apply_config(globals(), Path(__file__).with_name("previz_config.toml"), exclude_prefixes=("pose_", "hand_"))
if _argv:
    TILT_DEG = float(_argv[0])
print(f"previz_config: {len(_applied)} 个参数生效" if _applied else "previz_config: 未找到配置文件，用脚本默认值")

# ---- 派生量（config 之后统一算）----
FRAME_H = BODY_H / SUBJ_FRAC          # 人所在深度处的画面覆盖高度（米）
FRAME_W = FRAME_H * 16.0 / 9.0
D_SUBJ = FRAME_H * CAM_LENS / SENSOR_V
D_SUBJ_FAR = D_SUBJ * PULL_FACTOR
AIM_SHIFT = FRAME_W * AIM_SHIFT_FRAC
RING_R = FRAME_W * RING_R_FRAC
GROUND_R = FRAME_W * GROUND_R_FRAC
RISE_Z = FRAME_H * RISE_FRAC
# MVP 语义键 → 细节时刻（这些细节键不再直接可配；要更细的控制按需把键加回 config）
# ---- 时长链 → 全部时间常量（rel = 与旧绝对时刻精确对齐的段内偏移，按段时长等比伸缩）----
_SEGS = (
    ("FALL", DUR_FALL, 2.70, {"A_ENTER": 0.30, "A_LAND": 2.00, "A_LAND_DIP": 2.12, "A_LAND_UP": 2.32}),
    ("DRINK", DUR_DRINK, 1.60, {"A_DRINK_IN": 0.00, "A_DRINK_OUT": 0.65, "A_SWAY_A": 0.80, "A_SWAY_B": 1.10, "A_STEADY": 1.45}),
    ("GOURD", DUR_GOURD, 1.02, {"A_WINDUP": 0.00, "A_RELEASE": 0.15, "A_GOURD_APEX": 0.32, "A_GOURD_BOUNCE": 0.55, "A_ARM_BACK": 0.70, "A_GOURD_REST": 0.80}),
    ("SEAL", DUR_SEAL, 0.88, {"_STOMP0": 0.00, "A_SEAL": 0.03, "A_SEAL_END": 0.88, "A_SWORD_OUT": 0.88}),
    ("SWORD_IN", DUR_SWORD_IN, 2.05, {"A_SWORD_LEAVE": 0.12, "A_SWORD_TOP": 0.75, "A_SWORD_HOLD": 1.00, "A_SWORD_HOVER": 1.90}),
    ("RINGS", DUR_RINGS, 1.55, {"_RING_START": 0.00, "A_RING_MAX": 1.55}),
    ("ORBIT", DUR_ORBIT, 2.30, {"A_FINGER": 1.00, "A_ORBIT0": 1.20}),
    ("PILLAR", DUR_PILLAR, 1.90, {"A_PILLAR0": 0.00, "A_PILLAR_TOP": 1.20, "A_PILLAR_GONE": 1.90}),
    ("GRIP", DUR_GRIP, 1.00, {"A_GRIP0": 0.00, "A_FADE0": 0.00, "A_GRIP1": 0.50, "A_FADE1": 0.80}),
    ("SLASH", DUR_SLASH, 1.50, {"T_WIND1": 0.25, "T_SLASH1": 0.45, "T_QI1_END": 0.67, "T_WIND2": 0.90, "T_SLASH2": 1.08, "T_ARC_END": 1.34}),
    ("THROW", DUR_THROW, 1.50, {"T_THROW_WIND": 0.00, "T_THROW": 0.15, "T_SWORD_HIGH": 0.70, "T_SEAL": 1.00, "T_EYES_CLOSED": 1.40}),
    ("SPLIT", DUR_SPLIT, 1.40, {"T_SPLIT": 0.00, "T_SPLIT_DONE": 1.40}),
    ("SPIN", DUR_SPIN, 2.80, {"T_SPIN_END": 2.80}),
    ("RISE", DUR_RISE, 0.70, {"T_PULL0": 0.00, "T_RISE_END": 0.60, "T_PULL1": 0.70}),
    ("DROP", DUR_DROP, 2.18, {"T_POINT": 0.35, "T_DROP0": 0.50, "_DROP_SPAN": 1.30, "T_RING_DONE": 2.10}),
    ("JUMP", DUR_JUMP, 1.14, {"T_JUMP0": 0.00, "T_JUMP_TOP": 0.24, "T_JUMP1": 0.48, "T_GATHER1": 0.72, "T_MERGE": 0.74,
                              "_BOUNCE0": 0.82, "_BOUNCE1": 0.90, "_BOUNCE2": 0.98, "_BOUNCE3": 1.08}),
    ("FLIP", DUR_FLIP, 0.73, {"T_FLIP0": 0.00, "T_FLIP1": 0.63, "T_LAND_DIP": 0.70, "T_LAND_UP": 0.86}),
    ("SHEATH", DUR_SHEATH, 0.40, {"T_SWORD_UP": 0.00, "T_SWORD_APEX": 0.13, "T_SHEATH": 0.35}),
    ("LAUGH", DUR_LAUGH, 0.85, {"T_LAUGH": -0.01, "_BOB0": 0.15, "_BOB1": 0.31, "_BOB2": 0.47}),
)
_t = 0.0
_derived: dict = {}
for _name, _dur, _default, _rels in _SEGS:
    _scale = _dur / _default
    for _k, _rel in _rels.items():
        _derived[_k] = _t + _rel * _scale
    _derived[f"_SEG_{_name}"] = _t
    _t += _dur
TOTAL_SEC = _t
TOTAL = 1 + int(round(TOTAL_SEC * FPS))
globals().update({k: v for k, v in _derived.items() if not k.startswith("_")})
ACT2_T0 = _derived["_SEG_SLASH"]

A_ORBIT1 = A_ORBIT0 + ORBIT_TIME
A_STOMPS = tuple(_derived["_STOMP0"] + STOMP_GAP * i for i in range(STOMP_COUNT))
A_STOMP_DUST = tuple(t + STOMP_DUST_LAG for t in A_STOMPS)
A_RING_T0 = tuple(_derived["_RING_START"] + RING_GAP * i for i in range(RING_COUNT))
T_DROP_SPAN = _derived["_DROP_SPAN"] * (DUR_DROP / 2.18)
T_BOUNCE = tuple(_derived[f"_BOUNCE{i}"] for i in range(4))
T_LAUGH_BOBS = tuple(_derived[f"_BOB{i}"] for i in range(3))
random.seed(SEED)
assert ORBIT_TIME < DUR_ORBIT, "orbit_time 必须小于绕身段时长 dur_orbit"


def f(t: float) -> int:
    return 1 + int(round(t * FPS))


# ---------------------------------------------------------------- 材质 / 建模

def mat(name: str, rgb, emit: float, alpha: float = 1.0):
    m = bpy.data.materials.new(name=name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.55
    if "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
    if "Emission Strength" in bsdf.inputs:
        bsdf.inputs["Emission Strength"].default_value = emit
    if alpha < 1.0:
        bsdf.inputs["Alpha"].default_value = alpha
        try:
            m.surface_render_method = "BLENDED"
        except AttributeError:
            m.blend_method = "BLEND"
    return m


def link_previz(ob):
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    PREVIZ.objects.link(ob)


def setpar(child, parent):
    bpy.context.view_layer.update()
    child.parent = parent
    child.matrix_parent_inverse = parent.matrix_world.inverted()


def empty(name, loc, parent=None):
    bpy.ops.object.empty_add(type="PLAIN_AXES", radius=0.08, location=loc)
    e = bpy.context.object
    e.name = name
    link_previz(e)
    if parent is not None:
        setpar(e, parent)
    return e


def box(name, size, loc, material, parent=None, rot=None):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    ob = bpy.context.object
    ob.name = name
    ob.scale = Vector(size)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if rot is not None:
        ob.rotation_euler = Euler(rot)
    ob.data.materials.append(material)
    link_previz(ob)
    if parent is not None:
        setpar(ob, parent)
    return ob


def cyl(name, r, h, loc, material, parent=None, caps=True):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=r, depth=h, vertices=16 if caps else 40, location=loc,
        end_fill_type="NGON" if caps else "NOTHING",
    )
    ob = bpy.context.object
    ob.name = name
    ob.data.materials.append(material)
    link_previz(ob)
    if parent is not None:
        setpar(ob, parent)
    return ob


def sphere(name, r, loc, material, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=16, ring_count=10, location=loc)
    ob = bpy.context.object
    ob.name = name
    ob.data.materials.append(material)
    link_previz(ob)
    if parent is not None:
        setpar(ob, parent)
    return ob


def ring(name, rgb, emit, alpha, rmax):
    material = mat(f"PVZ_mat_{name}", rgb, emit, alpha)
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.0, minor_radius=0.13 / rmax, major_segments=64, minor_segments=6,
        location=(P.x, P.y, 0.20),
    )
    ob = bpy.context.object
    ob.name = name
    ob.scale = (1.0, 1.0, 0.25)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ob.data.materials.append(material)
    link_previz(ob)
    return ob


# ---------------------------------------------------------------- K 帧工具

def key_loc(ob, frame, loc):
    ob.location = Vector(loc)
    ob.keyframe_insert("location", frame=frame)


def key_rot(ob, frame, rot):
    ob.rotation_euler = Euler(rot)
    ob.keyframe_insert("rotation_euler", frame=frame)


def key_scale(ob, frame, s):
    ob.scale = Vector(s)
    ob.keyframe_insert("scale", frame=frame)


def key_vis(ob, frame, visible: bool):
    """显隐用缩放 K（CONSTANT 插值）—— hide_render 的动画在后台渲染里不可靠。"""
    prefs = bpy.context.preferences.edit
    prev = prefs.keyframe_new_interpolation_type
    prefs.keyframe_new_interpolation_type = "CONSTANT"
    ob.scale = Vector((1.0, 1.0, 1.0)) if visible else Vector((0.0001, 0.0001, 0.0001))
    ob.keyframe_insert("scale", frame=frame)
    prefs.keyframe_new_interpolation_type = prev


def key_alpha(ob, frame, a):
    bsdf = ob.data.materials[0].node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Alpha"].default_value = a
    bsdf.inputs["Alpha"].keyframe_insert("default_value", frame=frame)


def key_emit(ob, frame, e):
    bsdf = ob.data.materials[0].node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Emission Strength"].default_value = e
    bsdf.inputs["Emission Strength"].keyframe_insert("default_value", frame=frame)


def pose(joints, frame, spec):
    for jname, deg in spec.items():
        key_rot(joints[jname], frame, [math.radians(d) for d in deg])


def fcurves_of(ob):
    ad = ob.animation_data
    if not ad or not ad.action:
        return []
    act = ad.action
    if hasattr(act, "fcurves"):
        return list(act.fcurves)
    out = []
    for layer in act.layers:
        for strip in layer.strips:
            for cb in strip.channelbags:
                out.extend(cb.fcurves)
    return out


def set_interp(ob, kind, data_path=None, frame_range=None):
    """显式改 K 帧插值（偏好设置法在 5.1 后台不可靠）。"""
    for fc in fcurves_of(ob):
        if data_path and fc.data_path != data_path:
            continue
        for kp in fc.keyframe_points:
            if frame_range and not (frame_range[0] <= kp.co.x <= frame_range[1]):
                continue
            kp.interpolation = kind


class Interp:
    def __init__(self, kind):
        self.kind = kind

    def __enter__(self):
        self.prefs = bpy.context.preferences.edit
        self.prev = self.prefs.keyframe_new_interpolation_type
        self.prefs.keyframe_new_interpolation_type = self.kind
        return self

    def __exit__(self, *exc):
        self.prefs.keyframe_new_interpolation_type = self.prev


# ---------------------------------------------------------------- 机位几何

_tilt = math.radians(TILT_DEG)
R_VEC = Vector((CAM_AZ.y, -CAM_AZ.x, 0.0)).normalized()  # 画面向右


def cam_pos_for(d):
    return (P + Vector((0.0, 0.0, 0.9)) - CAM_AZ * (d * math.cos(_tilt)) + Vector((0.0, 0.0, d * math.sin(_tilt))))


CAM_POS = cam_pos_for(D_SUBJ)
CAM_POS_FAR = cam_pos_for(D_SUBJ_FAR)
CAM_AIM = P + Vector((0.0, 0.0, 0.9)) - R_VEC * AIM_SHIFT
_d = Vector((CAM_POS.x - P.x, CAM_POS.y - P.y)).normalized()
RZ_FACE = math.atan2(_d.x, -_d.y)  # 正身面朝镜头
# 身体侧 30° 转成三分面（rule 12.16 §6）：向前的斩击、前指、前踏都沿视线轴，正身对镜头会被透视压扁。
# 负角＝转向画左（庙的方向），第一剑与前指扫向画左的空场，而不是画右的葫芦。
BODY_YAW = math.radians(BODY_YAW_DEG)
RZ = RZ_FACE + BODY_YAW
FRONT = Vector((math.sin(RZ), -math.cos(RZ), 0.0))  # 身前

PREVIZ = bpy.data.collections.new("PREVIZ_shot12")
bpy.context.scene.collection.children.link(PREVIZ)

# 机位先建（后面要用它反求「画面上三分之一线」对应的高度）
bpy.ops.object.camera_add(location=CAM_POS)
cam = bpy.context.object
cam.name = "PVZ_Cam_shot12"
cam.data.lens = CAM_LENS
link_previz(cam)
aim = empty("PVZ_Cam_aim", CAM_AIM)
trk = cam.constraints.new(type="TRACK_TO")
trk.target = aim
trk.track_axis = "TRACK_NEGATIVE_Z"
trk.up_axis = "UP_Y"
bpy.context.scene.camera = cam
sc = bpy.context.scene
sc.render.resolution_x = 1920
sc.render.resolution_y = 1080
sc.frame_set(1)
bpy.context.view_layer.update()

from bpy_extras.object_utils import world_to_camera_view  # noqa: E402


def z_for_v(target_v, cam_pos):
    """反求 P 正上方多高的一点会落在画面纵向 v（0 底 1 顶）—— 用起幅机位。"""
    cam.location = cam_pos
    bpy.context.view_layer.update()
    lo, hi = 1.0, 60.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        v = world_to_camera_view(sc, cam, P + Vector((0, 0, mid))).y
        if v < target_v:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


HIGH_Z = z_for_v(0.88, CAM_POS)   # 抛剑高悬：剑在画面上三分之一线（起幅机位）
cam.location = CAM_POS
bpy.context.view_layer.update()
print(f"HIGH_Z={HIGH_Z:.2f} (head v={world_to_camera_view(sc, cam, P + Vector((0, 0, 1.6))).y:.3f})")

# ---------------------------------------------------------------- 材质

M_GREEN = mat("PVZ_酒剑仙_绿", (0.06, 0.80, 0.20), 1.1)
M_SKIN = mat("PVZ_头_浅绿", (0.35, 0.95, 0.45), 1.4)
M_LIMB = mat("PVZ_手脚_亮黄绿", (0.72, 1.00, 0.28), 1.6)   # 手掌与脚：更亮的对比色
M_BLUE = mat("PVZ_剑_蓝", (0.10, 0.40, 1.00), 3.2)
M_SHEATH = mat("PVZ_剑鞘_暗蓝", (0.05, 0.08, 0.20), 0.0)
M_RED = mat("PVZ_酒葫芦_红", (0.95, 0.10, 0.08), 1.6)
M_TRENCH = mat("PVZ_沟_黑", (0.004, 0.004, 0.005), 0.0)
M_RIDGE = mat("PVZ_土垄_土黄", (0.22, 0.16, 0.09), 0.0)
C_CYAN = (0.35, 0.85, 1.00)
C_DUST = (0.60, 0.58, 0.54)
M_QI = mat("PVZ_剑气_青", C_CYAN, 2.5, alpha=0.75)

# ---------------------------------------------------------------- 绿人（同 shot12）

# 人形 proxy 走公共模块（rule 12.16 §3）—— shot12/shot13 共用同一具身体。
# 这里原先是 shot12 初版人形的**复制品**，shot12 细化了三轮它却没跟上：
# 两镜相邻，观众会直接看到同一个人前后变了体型。所以只此一处。
rig = PrevizRig(link=link_previz, body=M_GREEN, skin=M_SKIN, limb_end=M_LIMB)
_before_rig = set(bpy.data.objects)
root, pelvis, J = rig.build(P)
_rig_meshes = [o for o in bpy.data.objects if o not in _before_rig and o.type == "MESH"]
# 精致人形（用户 2026-08-18：方块拼的小绿人像火柴棍、肢体细节看不出来）：
# 用 MPFB 真人网格套在关节 proxy 上——骨骼逐根 Child Of 到关节空物件，姿态 K 帧照旧打在 J[...] 上；
# 关节 proxy 的网格隐藏（空物件保留），画面里只剩一具四肢/手指/脚都读得出的绿人。
# 体型：配置里写人话（身高米 / 体格 / 年龄档 / 性别 / 比例），由 macro_for 翻成 MPFB 参数。
# 身高按实测标定表反查（rule 12.16 §0.2）——直接填 MPFB 的 height 参数必错：
# 曲线非线性，且 age<0.5 是儿童生长曲线，会把成年人压成孩子身量。
_BODY_SPEC = {
    "身高": BODY_HEIGHT_M, "体格": BODY_BUILD, "年龄档": BODY_AGE,
    "性别": BODY_GENDER, "比例": BODY_PROPORTIONS,
}
human, human_rig = attach_mpfb_human(
    root, J, link=link_previz, body_mat=M_GREEN, skin_mat=M_SKIN, limb_mat=M_LIMB,
    body_spec=_BODY_SPEC, subj_frac=SUBJ_FRAC)
for _o in _rig_meshes:
    _o.hide_render = True
    _o.hide_viewport = True


# 剑鞘留背上
sheath = box("PVZ_sheath", (0.075, 0.05, 0.90), P + Vector((0, 0.22, HIP_Z + 0.40)), M_SHEATH)
setpar(sheath, pelvis)
sheath.rotation_euler = Euler((math.radians(18), 0, math.radians(-14)))



# 酒葫芦：第一幕握在手里 → 抛向画右 → 此后一直躺在地上（第二幕沿用）
gourd = sphere("PVZ_gourd", 0.115, P + Vector((0, 0, HIP_Z)), M_RED)
gourd.scale = (1.0, 1.0, 1.35)

# ---------------- 第一幕道具：地面剑气环 / 光柱 / 尘
C_CYAN = (0.35, 0.85, 1.00)
C_DUST = (0.60, 0.58, 0.54)
# 特效层（地面光圈 + 光柱）＝示意级，不是成品（follow-up 040）。
# 压到这个亮度/透明度，是为了让它一眼不像成片 —— 它只交代「在哪儿、第几秒、多大范围」，
# 真正的光效由 Seedance 自行设计渲染。太亮太实模型就会照抄白模的样子。
EFX_EMIT = 0.35
EFX_ALPHA = 0.45
M_PILLAR = mat("PVZ_光柱_青", (0.45, 0.88, 1.00), 0.18, alpha=0.09)





# 环半径按画面宽度定 —— 画面收紧后沿用旧的 3/5.5/8/11m 会让外三圈整圈跑到画外，
# 「一圈圈往外推」这件事就读不出来了（follow-up 040）
QI_RMAX = tuple(FRAME_W * k for k in (0.16, 0.30, 0.46, 0.64))
RINGS = [ring(f"PVZ_qi_ring{i}", C_CYAN, EFX_EMIT, EFX_ALPHA, QI_RMAX[i]) for i in range(4)]
pillar = cyl("PVZ_light_pillar", 1.45, 1.0, Vector((P.x, P.y, 0.5)), M_PILLAR, caps=False)
land_dust = ring("PVZ_land_dust", C_DUST, 0.0, 0.55, 3.6)
STOMP_DUST = [ring(f"PVZ_stomp_dust{i}", C_DUST, 0.0, 0.5, 1.15) for i in range(3)]





# ---------------------------------------------------------------- 剑：单剑 + 二十把

def make_sword(name, material):
    """剑体沿 Z、剑尖在 -Z（原点在剑体中心）。"""
    blade = box(f"{name}_blade", (0.05, 0.016, 0.84), Vector((0, 0, 0)), material)
    guard = box(f"{name}_guard", (0.22, 0.05, 0.035), Vector((0, 0, 0.44)), material)
    setpar(guard, blade)
    hilt = cyl(f"{name}_hilt", 0.032, 0.20, Vector((0, 0, 0.56)), material)
    setpar(hilt, blade)
    return blade


sword = make_sword("PVZ_sword", M_BLUE)
SWORDS = []
SW_MATS = []
for i in range(N_SWORDS):
    m_i = mat(f"PVZ_剑{i:02d}_蓝", (0.10, 0.40, 1.00), 3.2)
    SW_MATS.append(m_i)
    SWORDS.append(make_sword(f"PVZ_sw{i:02d}", m_i))

# ---------------------------------------------------------------- 沟壑

TRENCH_W = 0.50   # 沟口≈一个人肩宽
TRENCH_D = 0.9    # 沟深（只为让沟内全黑，俯视看不见底）
RIDGE_H = 0.20
RIDGE_W = 0.35

# 直沟：自他脚前一路划到画面下缘之外（沿身前方向）；用局部 Y 缩放从脚前长出去
T1_LEN = FRAME_H * 1.35   # 直沟长度：稳出画面下缘
t1_root = empty("PVZ_trench1_root", P + FRONT * 0.7)
t1_root.rotation_euler = Euler((0, 0, RZ + math.pi))  # 局部 +Y = FRONT
box("PVZ_trench1", (TRENCH_W, T1_LEN, TRENCH_D), P + FRONT * (0.7 + T1_LEN / 2) + Vector((0, 0, -TRENCH_D / 2 + 0.02)), M_TRENCH, t1_root, rot=t1_root.rotation_euler)
for sgn in (1, -1):
    box(f"PVZ_trench1_ridge{'L' if sgn > 0 else 'R'}", (RIDGE_W, T1_LEN, RIDGE_H),
        P + FRONT * (0.7 + T1_LEN / 2) + R_VEC * (sgn * (TRENCH_W / 2 + RIDGE_W / 2)) + Vector((0, 0, RIDGE_H / 2)),
        M_RIDGE, t1_root, rot=t1_root.rotation_euler)

# 月牙沟：以他为圆心半径 8m 的弧，自他身侧（画左）甩过身前到画面另一侧；40 段逐段出现
ARC_R = FRAME_W * 0.30    # 月牙沟半径
ARC_N = 40
ARC_A0, ARC_A1 = math.radians(-105), math.radians(105)  # 0 = 正前；负 = 画左（他的右侧）
ARC_SEGS = []
for k in range(ARC_N):
    a0 = ARC_A0 + (ARC_A1 - ARC_A0) * k / ARC_N
    a1 = ARC_A0 + (ARC_A1 - ARC_A0) * (k + 1) / ARC_N
    am = 0.5 * (a0 + a1)
    c = P + FRONT * (ARC_R * math.cos(am)) + R_VEC * (ARC_R * math.sin(am))
    seg_len = ARC_R * (a1 - a0) * 1.06
    seg = empty(f"PVZ_arc{k:02d}", c)
    # 段的局部 Y 沿弧切线
    tangent = (-FRONT * math.sin(am) + R_VEC * math.cos(am)).normalized()
    seg.rotation_euler = Euler((0, 0, math.atan2(tangent.y, tangent.x) - math.pi / 2))
    normal = (FRONT * math.cos(am) + R_VEC * math.sin(am)).normalized()
    box(f"PVZ_arc{k:02d}_t", (TRENCH_W, seg_len, TRENCH_D), c + Vector((0, 0, -TRENCH_D / 2 + 0.02)), M_TRENCH, seg, rot=seg.rotation_euler)
    for sgn in (1, -1):
        box(f"PVZ_arc{k:02d}_r{sgn}", (RIDGE_W, seg_len, RIDGE_H), c + normal * (sgn * (TRENCH_W / 2 + RIDGE_W / 2)) + Vector((0, 0, RIDGE_H / 2)), M_RIDGE, seg, rot=seg.rotation_euler)
    ARC_SEGS.append(seg)

# 剑气示意：一块青色薄片贴地飞
qi1 = box("PVZ_qi_slab1", (0.9, 0.35, 0.10), P, M_QI)
qi2 = box("PVZ_qi_slab2", (0.9, 0.35, 0.10), P, M_QI)

# 落地尘环
land_dust = ring("PVZ_land_dust", C_DUST, 0.0, 0.55, 3.0)
jump_dust = ring("PVZ_jump_dust", C_DUST, 0.0, 0.5, 2.0)

# ---------------------------------------------------------------- 姿态库

POSE_END12 = {  # = shot12 末帧：持剑垂手立定
    "shoulderR": (-10, 10, 0), "elbowR": (-16, 0, 0),
    "shoulderL": (0, -12, 0), "elbowL": (-8, 0, 0), "head": (0, 0, 0),
    "hipR": (0, 0, 0), "kneeR": (0, 0, 0), "hipL": (0, 0, 0), "kneeL": (0, 0, 0), "pelvis": (0, 0, 0),
}
POSE_WIND1 = {"shoulderR": (-150, 20, 0), "elbowR": (-40, 0, 0), "shoulderL": (-30, -30, 0), "elbowL": (-40, 0, 0), "pelvis": (0, 0, 25), "head": (-8, 0, 0)}
POSE_SLASH1 = {"shoulderR": (-30, 0, 0), "elbowR": (-5, 0, 0), "shoulderL": (10, -35, 0), "elbowL": (-20, 0, 0), "pelvis": (8, 0, -12), "hipR": (-25, 0, 0), "kneeR": (30, 0, 0), "head": (14, 0, 0)}
POSE_WIND2 = {"shoulderR": (-95, -70, 0), "elbowR": (-70, 0, 0), "shoulderL": (-20, -20, 0), "elbowL": (-30, 0, 0), "pelvis": (0, 0, -35), "hipR": (0, 0, 0), "kneeR": (0, 0, 0), "head": (0, 0, -20)}
POSE_SLASH2 = {"shoulderR": (-8, 88, 0), "elbowR": (0, 0, 0), "shoulderL": (0, -60, 0), "elbowL": (-10, 0, 0), "pelvis": (0, 0, 30), "hipR": (0, 0, 0), "kneeR": (0, 0, 0), "head": (0, 0, 25)}
POSE_THROW_WIND = {"shoulderR": (-30, 15, 0), "elbowR": (-70, 0, 0), "shoulderL": (0, -12, 0), "elbowL": (-8, 0, 0), "pelvis": (0, 0, 0), "head": (0, 0, 0)}
POSE_THROW = {"shoulderR": (-175, 5, 0), "elbowR": (-5, 0, 0), "shoulderL": (0, -12, 0), "elbowL": (-8, 0, 0), "pelvis": (-6, 0, 0), "head": (-30, 0, 0)}
POSE_SEAL1 = {"shoulderR": (-52, -36, 0), "elbowR": (-115, 0, 0), "shoulderL": (0, -12, 0), "elbowL": (-8, 0, 0), "pelvis": (0, 0, 0), "head": (-22, 0, 0)}
POSE_SEAL_STILL = {"shoulderR": (-52, -36, 0), "elbowR": (-115, 0, 0), "shoulderL": (0, -12, 0), "elbowL": (-8, 0, 0), "pelvis": (0, 0, 0), "head": (6, 0, 0)}
POSE_POINT = {  # 亮相指地：右臂自肩到指尖一条斜线指前下方，左手剑指收腰侧，前踏半马步
    "shoulderR": (-55, 0, 0), "elbowR": (0, 0, 0), "shoulderL": (30, -20, 0), "elbowL": (-100, 0, 0),
    "hipR": (-45, 0, 0), "kneeR": (55, 0, 0), "hipL": (12, 0, 0), "kneeL": (25, 0, 0),
    "pelvis": (14, 0, -8), "head": (10, 0, 0),
}
POSE_SPREAD = {  # 双臂平张、两手各竖两指、单脚
    "shoulderR": (0, 90, 0), "elbowR": (0, 0, 0), "shoulderL": (0, -90, 0), "elbowL": (0, 0, 0),
    "hipR": (0, 0, 0), "kneeR": (0, 0, 0), "hipL": (-70, 0, 0), "kneeL": (95, 0, 0),
    "pelvis": (0, 0, 0), "head": (0, 0, 0),
}
POSE_TUCK = {  # 翻跟斗团身
    "shoulderR": (-40, 30, 0), "elbowR": (-90, 0, 0), "shoulderL": (-40, -30, 0), "elbowL": (-90, 0, 0),
    "hipR": (-90, 0, 0), "kneeR": (110, 0, 0), "hipL": (-90, 0, 0), "kneeL": (110, 0, 0),
    "pelvis": (0, 0, 0), "head": (20, 0, 0),
}
POSE_LAND = {
    "shoulderR": (-20, 40, 0), "elbowR": (-20, 0, 0), "shoulderL": (-20, -40, 0), "elbowL": (-20, 0, 0),
    "hipR": (-35, 0, 0), "kneeR": (50, 0, 0), "hipL": (-35, 0, 0), "kneeL": (50, 0, 0),
    "pelvis": (12, 0, 0), "head": (0, 0, 0),
}
POSE_STAND = {
    "shoulderR": (0, 12, 0), "elbowR": (-8, 0, 0), "shoulderL": (0, -12, 0), "elbowL": (-8, 0, 0),
    "hipR": (0, 0, 0), "kneeR": (0, 0, 0), "hipL": (0, 0, 0), "kneeL": (0, 0, 0), "pelvis": (0, 0, 0), "head": (0, 0, 0),
}
POSE_LAUGH = {
    "shoulderR": (10, 30, 0), "elbowR": (-30, 0, 0), "shoulderL": (10, -30, 0), "elbowL": (-30, 0, 0),
    "hipR": (0, 0, 0), "kneeR": (0, 0, 0), "hipL": (0, 0, 0), "kneeL": (0, 0, 0), "pelvis": (-8, 0, 0), "head": (-38, 0, 0),
}

# ---------------- 第一幕动画：身体

POSE_FALL = {
    "shoulderL": (0, -95, 0), "shoulderR": (0, 95, 0), "elbowL": (0, 0, 0), "elbowR": (0, 0, 0),
    "hipR": (-60, 0, 0), "kneeR": (78, 0, 0), "hipL": (6, 0, 0), "kneeL": (0, 0, 0),
    "pelvis": (0, 0, 0), "head": (0, 0, 0),
}
POSE_STAND = {
    "shoulderL": (0, -12, 0), "shoulderR": (0, 12, 0), "elbowL": (-8, 0, 0), "elbowR": (-8, 0, 0),
    "hipR": (0, 0, 0), "kneeR": (0, 0, 0), "hipL": (0, 0, 0), "kneeL": (0, 0, 0),
    "pelvis": (0, 0, 0), "head": (0, 0, 0),
}
POSE_DRINK = {
    "shoulderR": (-48, 14, 0), "elbowR": (-128, 0, 0), "head": (26, 0, 0),
    "shoulderL": (0, -12, 0), "elbowL": (-8, 0, 0),
}
POSE_WINDUP = {"shoulderR": (34, 22, 0), "elbowR": (-45, 0, 0), "head": (0, 0, 0)}
POSE_RELEASE = {"shoulderR": (-72, -34, 0), "elbowR": (-12, 0, 0)}
# 结印＝两手剑指相抱**收到胸前**。手位是硬要求，所以反解、不猜角度。
# 第一版手调的 (-52, ±36, -108) 渲出来是「两手抬在胸前但没合拢」——肘的 rot_x 折在
# 被肩 rot_y 转过的局部系里，把手甩到了体侧。
_SH_L = Vector((SHOULDER_X, 0.0, HIP_Z + 0.46))
_SH_R = Vector((-SHOULDER_X, 0.0, HIP_Z + 0.46))
# 道家掐诀（follow-up 043 用户校正）：**两只手都伸出两指，一只手握住另一只手的两指**，
# 不是两掌对合。所以两腕要在竖向错开一个手掌的距离 —— 下面那只（右手）剑指朝上前伸出，
# 上面那只（左手）的蜷指正好扣在它伸出的两指上。两腕若落在同一点，两只手会互相穿模，
# 「谁握着谁」就读不出来了。
_SEAL_HAND_R = Vector((-0.020, -0.250, HIP_Z + 0.35))  # 被握的手：剑指伸出，收到胸前高度
_sr = solve_arm(_SH_R, _SEAL_HAND_R, flare=SEAL_ELBOW_FLARE)

# 握的那只手，落点由**右手两指的实际位置反推**，不是另外拍脑袋给一个坐标。
# 手没有自己的旋转、朝向完全跟着小臂走，所以两腕各自摆一个位置的话，两只手的
# 手指只会平行地各指各的 —— 画面上是「上下两只手」，不是「一只手握住另一只手」。
# 右手指尖方向 ＝ 小臂方向（手无自转），沿它取两指中段，左掌心就落在那儿。
_elbow_R = elbow_pos(_SH_R, _sr[0], _sr[1])
_DIR_R = (_SEAL_HAND_R - _elbow_R).normalized()
SEAL_GRIP_PT = _SEAL_HAND_R + _DIR_R * 0.115      # 右手食中二指的中段
PALM_DEPTH = 0.048                                 # 腕到掌心的距离
_SEAL_HAND_L = SEAL_GRIP_PT + Vector((0.0, -0.030, 0.052))
_sl = solve_arm(_SH_L, _SEAL_HAND_L, flare=SEAL_ELBOW_FLARE)
POSE_SEAL = {
    "shoulderL": (_sl[0], _sl[1], _sl[2]), "shoulderR": (_sr[0], _sr[1], _sr[2]),
    "elbowL": (_sl[3], 0, 0), "elbowR": (_sr[3], 0, 0), "head": (6, 0, 0),
}
# follow-up 040：右手前指的同一拍，右脚向前迈出一步成弓步 —— 只伸手不动脚，
# 上半身在使劲下半身像钉住，动作不自然。前膝微屈、后腿蹬直、重心沉下去。
# 横抱臂目标：左腕收到胸前中线略偏右（画面上横抱过胸），高度胸口
_FINGER_HAND_L = Vector((-0.06, -0.24, HIP_Z + 0.40))
_fl = solve_arm(_SH_L, _FINGER_HAND_L, flare=FINGER_ELBOW_FLARE)
POSE_FINGER = {
    "shoulderL": (_fl[0], _fl[1], _fl[2]), "elbowL": (_fl[3], 0, 0),
    "shoulderR": (-90, 0, 0), "elbowR": (0, 0, 0), "head": (0, 0, 0),
    "hipR": (-42, 0, 0), "kneeR": (22, 0, 0),   # 右腿前迈、前膝微屈
    "hipL": (24, 0, 0), "kneeL": (0, 0, 0),     # 左腿后蹬、蹬直
    "pelvis": (-8, 0, 0),                        # 重心前压
}
print("SEAL R:", solve_report(_SH_R, _SEAL_HAND_R, _sr))
print("SEAL L:", solve_report(_SH_L, _SEAL_HAND_L, _sl))
print("FINGER L:", solve_report(_SH_L, _FINGER_HAND_L, _fl))

POSE_END = {
    "shoulderR": (-10, 10, 0), "elbowR": (-16, 0, 0),
    "shoulderL": (0, -12, 0), "elbowL": (-8, 0, 0), "head": (0, 0, 0),
    "hipR": (0, 0, 0), "kneeR": (0, 0, 0), "hipL": (0, 0, 0), "kneeL": (0, 0, 0),
    "pelvis": (0, 0, 0),   # 收弓步、垂手立定
}

# 姿态库定义完毕后再套用户配置（follow-up 051：姿态级全部可配；pose_*/hand_* 整表覆盖）
_applied_pose = apply_config(globals(), Path(__file__).with_name("previz_config.toml"), include_prefixes=("pose_", "hand_"))
print(f"previz_config: {len(_applied_pose)} 个姿态生效")


# 自画面右上角斜落：入场点沿画面向右 + 抬高，落点＝P。root 无父级，location 即世界坐标。
# 按画面尺寸推导，改 SUBJ_FRAC / 俯角时入场点自动跟着缩放，不用手调。
ENTER = P + R_VEC * (FRAME_W * 0.36) + Vector((0.0, 0.0, FRAME_H * 0.62))
ABOVE = P + R_VEC * (FRAME_W * 0.46) + Vector((0.0, 0.0, FRAME_H * 1.70))

with Interp("BEZIER"):
    # 0-1.6s 自画面右上角旋转斜落 → 双脚砸在场地正中（follow-up 040 加长，让「飞下来」读得出来）
    key_loc(root, 1, ABOVE)
    key_loc(root, f(A_ENTER), ENTER)
    key_loc(root, f(A_LAND), P)
    key_loc(root, f(A_LAND_DIP), P + Vector((0, 0, -0.13)))
    key_loc(root, f(A_LAND_UP), P)
    # 11.7s 起沉胯成弓步，18.6s 剑归掌后收势起身
    key_loc(root, f(A_FINGER - 0.6), P)
    key_loc(root, f(A_FINGER), P + Vector((0, 0, -LUNGE_SINK)))
    key_loc(root, f(A_GRIP1), P + Vector((0, 0, -LUNGE_SINK)))
    key_loc(root, f(A_GRIP1 + 0.4), P)
    key_loc(root, f(ACT2_T0), P)

    key_rot(root, 1, (0, 0, RZ - math.radians(360 * FALL_SPINS)))
    key_rot(root, f(A_LAND), (0, 0, RZ))
    key_rot(root, f(A_SWAY_A), (0.0, math.radians(4.5), RZ))
    key_rot(root, f(A_SWAY_B), (0.0, math.radians(-3.0), RZ))
    key_rot(root, f(A_STEADY), (0, 0, RZ))
    key_rot(root, f(ACT2_T0), (0, 0, RZ))

    pose(J, 1, POSE_FALL)
    pose(J, f(A_LAND - 0.15), POSE_FALL)
    pose(J, f(A_LAND_UP - 0.10), POSE_STAND)
    # 1.6-3.2s 葫芦口抵唇饮一口（加长）
    pose(J, f(A_DRINK_IN - 0.40), POSE_STAND)
    pose(J, f(A_DRINK_IN), POSE_DRINK)
    pose(J, f(A_DRINK_OUT), POSE_DRINK)
    # 3.2-4.2s 身形一晃即稳
    pose(J, f(A_SWAY_A), POSE_STAND)
    pose(J, f(A_STEADY), POSE_STAND)
    # 4.2-5.2s 右腕一甩把葫芦朝画右抛出（加长）
    pose(J, f(A_WINDUP), POSE_WINDUP)
    pose(J, f(A_RELEASE), POSE_RELEASE)
    pose(J, f(A_ARM_BACK), POSE_STAND)
    # 5.5-6.7s 两手结印收到胸前（跺脚在下方单独 K）
    pose(J, f(A_SEAL), POSE_SEAL)
    pose(J, f(A_FINGER - 1.30), POSE_SEAL)
    # 双腿保持中立到迈步前一刻 —— 不加这道 hold，弓步会从跺完脚起就开始缓慢渗出
    pose(J, f(A_FINGER - 0.60), {
        "hipR": (0, 0, 0), "kneeR": (0, 0, 0), "hipL": (0, 0, 0), "kneeL": (0, 0, 0),
        "pelvis": (0, 0, 0),
    })
    # 11.7-12.9s 两手剑指 + 右脚前迈成弓步（follow-up 040）
    pose(J, f(A_FINGER), POSE_FINGER)
    pose(J, f(A_GRIP0 - 0.10), POSE_FINGER)
    # 18.6-20s 剑归掌、垂手立定
    pose(J, f(A_GRIP1 + 0.40), POSE_END)
    pose(J, f(ACT2_T0), POSE_END)

    # --- 手型时间线
    # 右手一路握着葫芦，脱手后才松开；结印起两手转剑指并保持到剑归掌；
    # 最后右手重新握住 —— 全镜唯一一次手真的合拢在物件上。
    rig.hand_pose(J, "R", 1, HAND_GRIP)
    rig.hand_pose(J, "R", f(A_RELEASE), HAND_GRIP)
    rig.hand_pose(J, "R", f(A_RELEASE + 0.15), HAND_RELAX)
    rig.hand_pose(J, "L", 1, HAND_RELAX)
    rig.hand_pose(J, "L", f(A_SEAL - 0.5), HAND_RELAX)
    rig.hand_pose(J, "R", f(A_SEAL - 0.5), HAND_RELAX)
    # 掐诀：右手剑指伸出被握，左手两指也伸出、其余三指扣住右手那两指。
    # 左腕额外转一个角度 —— 手的朝向本来完全跟着小臂走，不转腕两只手的手指就平行，
    # 「扣住」变成「并排」。
    key_rot(J["handL"], 1, (0.0, 0.0, 0.0))
    key_rot(J["handL"], f(A_SEAL - 0.5), (0.0, 0.0, 0.0))
    key_rot(J["handL"], f(A_SEAL), (math.radians(-62), 0.0, math.radians(28)))
    key_rot(J["handL"], f(A_SEAL_END), (math.radians(-62), 0.0, math.radians(28)))
    key_rot(J["handL"], f(A_FINGER), (0.0, 0.0, 0.0))
    rig.hand_pose(J, "R", f(A_SEAL), HAND_SWORD_FINGER)
    rig.hand_pose(J, "L", f(A_SEAL), HAND_SEAL_WRAP)
    rig.hand_pose(J, "R", f(A_SEAL_END), HAND_SWORD_FINGER)
    rig.hand_pose(J, "L", f(A_SEAL_END), HAND_SEAL_WRAP)
    rig.both_hands(J, f(A_FINGER), HAND_SWORD_FINGER)  # 分开后两手各自剑指
    rig.both_hands(J, f(A_GRIP0), HAND_SWORD_FINGER)   # 剑指保持到剑落回掌心
    rig.hand_pose(J, "L", f(A_GRIP1 + 0.4), HAND_RELAX)
    rig.hand_pose(J, "R", f(A_GRIP1), HAND_GRIP)
    rig.both_hands(J, f(ACT2_T0), HAND_RELAX)
    rig.hand_pose(J, "R", f(ACT2_T0), HAND_GRIP)

    # 只用右脚原地快跺三下，左脚站定支撑、脚掌不离地
    for i, t0 in enumerate(A_STOMPS):
        key_rot(J["hipR"], f(t0), (0, 0, 0))
        key_rot(J["kneeR"], f(t0), (0, 0, 0))
        key_rot(J["hipR"], f(t0 + 0.13), (math.radians(-34), 0, 0))
        key_rot(J["kneeR"], f(t0 + 0.13), (math.radians(58), 0, 0))
        key_rot(J["hipR"], f(t0 + 0.24), (0, 0, 0))
        key_rot(J["kneeR"], f(t0 + 0.24), (0, 0, 0))
    key_rot(J["hipR"], f(A_SEAL_END), (0, 0, 0))
    key_rot(J["kneeR"], f(A_SEAL_END), (0, 0, 0))

bpy.context.view_layer.update()

FRONT = Vector((math.sin(RZ), -math.cos(RZ), 0.0))  # 局部 -Y 的世界朝向 = 身前
HOVER = Vector((P.x, P.y, 0.0)) + FRONT * ORBIT_R + Vector((0, 0, ORBIT_Z))
ORBIT_C = Vector((P.x, P.y, ORBIT_Z))

# 剑鞘：全程留背上不动 —— 直接挂 pelvis
setpar(sheath, pelvis)
sheath.rotation_euler = Euler((math.radians(18), 0, math.radians(-14)))

# ---------------- 第一幕动画：采样跟随

SWORD_ON_BACK = Matrix.Translation((-0.06, 0.20, 0.30)) @ Euler(
    (math.radians(18), 0.0, math.radians(-14))
).to_matrix().to_4x4()

F_SWORD_OUT = f(A_SWORD_OUT)
F_GOURD_OUT = f(A_RELEASE)

with Interp("BEZIER"):
    for fr in range(1, F_SWORD_OUT + 1):
        bpy.context.scene.frame_set(fr)
        bpy.context.view_layer.update()
        m = pelvis.matrix_world @ SWORD_ON_BACK
        key_loc(sword, fr, m.to_translation())
        key_rot(sword, fr, m.to_euler())

    for fr in range(1, F_GOURD_OUT + 1):
        bpy.context.scene.frame_set(fr)
        bpy.context.view_layer.update()
        hand = J["handR"].matrix_world.to_translation()
        key_loc(gourd, fr, hand + Vector((0, 0, -0.10)))

# 躺在画右地上；偏移按画面宽度定，画面收紧时才不会被挤出画外
GOURD_REST = P + R_VEC * (FRAME_W * 0.19) + FRONT * 1.4 + Vector((0.0, 0.0, 0.13))
bpy.context.scene.frame_set(F_GOURD_OUT)
bpy.context.view_layer.update()
release_pt = J["handR"].matrix_world.to_translation() + Vector((0, 0, -0.10))

with Interp("BEZIER"):
    # 4.5-5.2s 抛出走一段平抛弧 → 落地翻滚两圈 → 停住不再动
    key_loc(gourd, f(A_GOURD_APEX), release_pt.lerp(GOURD_REST, 0.45) + Vector((0, 0, 0.55)))
    key_loc(gourd, f(A_GOURD_BOUNCE), GOURD_REST.lerp(release_pt, 0.22) + Vector((0, 0, 0.14)))
    key_loc(gourd, f(A_GOURD_REST), GOURD_REST)
    key_loc(gourd, TOTAL, GOURD_REST)
    key_rot(gourd, F_GOURD_OUT, (0, 0, 0))
    key_rot(gourd, f(A_GOURD_REST), (math.radians(720), 0, math.radians(50)))
    key_rot(gourd, TOTAL, (math.radians(720), 0, math.radians(50)))

# ---------------- 第一幕动画：剑

bpy.context.scene.frame_set(F_SWORD_OUT)
bpy.context.view_layer.update()
back_pt = (pelvis.matrix_world @ SWORD_ON_BACK).to_translation()
back_rot = (pelvis.matrix_world @ SWORD_ON_BACK).to_euler()

with Interp("BEZIER"):
    # 用户 2026-08-18：剑不冲天——落地、喝完酒、摆完手势后，剑自背后出鞘、越过肩头飞到身前，
    # 竖直剑尖朝下停住悬空（然后微幅上下浮动，再绕身一圈）。
    # 6.2-6.32s 竖直向上拔出鞘 → 6.95s 越过头顶（略偏身前）→ 7.2s 在身前下落 → 8.1s 停在 HOVER
    key_rot(sword, f(A_SWORD_LEAVE), (0, 0, 0))
    key_loc(sword, f(A_SWORD_LEAVE), back_pt + Vector((0, 0, 0.55)))
    key_loc(sword, f(A_SWORD_TOP), P + FRONT * (ORBIT_R * 0.35) + Vector((0, 0, 2.55)))
    key_rot(sword, f(A_SWORD_TOP), (0, 0, 0))
    key_loc(sword, f(A_SWORD_HOLD), P + FRONT * (ORBIT_R * 0.85) + Vector((0, 0, ORBIT_Z + 0.55)))
    key_loc(sword, f(A_SWORD_HOVER), HOVER)
    key_rot(sword, f(A_SWORD_HOVER), (0, 0, 0))

with Interp("BEZIER"):
    # 悬停期极缓慢微幅上下浮动：幅度不超过一指宽、约两秒一个起伏
    tt = A_SWORD_HOVER + 0.2
    up = True
    while tt <= A_ORBIT0:
        key_loc(sword, f(tt), HOVER + Vector((0, 0, 0.045 if up else -0.045)))
        up = not up
        tt += 1.0

with Interp("LINEAR"):
    # 13.2-15.4s 剑绕他的身体走整整一圈，匀速、同一方向：前→他的左→背后→他的右→回前。
    # follow-up 040：2.2s 走完一圈，比原来的 4.5s 快 2.05 倍。
    fr = f(A_ORBIT0)
    fr_end = f(A_ORBIT1)
    span = fr_end - fr
    step = 2
    for k in range(0, span + 1, step):
        u = k / span
        ang = 2.0 * math.pi * u
        v = Vector((FRONT.x, FRONT.y, 0.0)) * ORBIT_R
        v.rotate(Euler((0, 0, ang)))
        key_loc(sword, fr + k, ORBIT_C + v)
    key_rot(sword, fr, (0, 0, 0))
    key_rot(sword, fr_end, (0, 0, 0))

with Interp("BEZIER"):
    key_loc(sword, f(A_ORBIT1), HOVER)
    tt = A_ORBIT1 + 1.0
    up = True
    while tt <= A_GRIP0:
        key_loc(sword, f(tt), HOVER + Vector((0, 0, 0.045 if up else -0.045)))
        up = not up
        tt += 1.0
    key_loc(sword, f(A_GRIP0), HOVER)

# 18.6-20s 剑落回右手掌心（全镜唯一一次手碰到剑）
# 剑体原点在剑身中心：剑身 ±0.42、剑格 +0.44、缠绳剑柄 +0.46…+0.66。
# 手要落在**柄**上，所以剑原点要放在手的下方 HILT_GRIP_Z 处——旧值 0.30 落在剑身
# 范围内，等于攥着**刃**（follow-up 043 用户指出）。偏移必须跟着剑的倾角一起转，
# 否则收势那 26° 一倾，手又滑回刃上。
HILT_GRIP_Z = 0.55
END_TILT = math.radians(26.0)

with Interp("BEZIER"):
    fr0, fr1 = f(A_GRIP0), f(A_GRIP1)
    for fr in range(fr0, f(ACT2_T0) + 1):
        bpy.context.scene.frame_set(fr)
        bpy.context.view_layer.update()
        hand = J["handR"].matrix_world.to_translation()
        u = min(1.0, (fr - fr0) / (fr1 - fr0))
        tilt = END_TILT * u
        offset = Euler((tilt, 0.0, 0.0)).to_matrix() @ Vector((0.0, 0.0, HILT_GRIP_Z))
        grip = hand - offset
        key_loc(sword, fr, HOVER.lerp(grip, u) if fr <= fr1 else grip)
        key_rot(sword, fr, (tilt, 0.0, 0.0))

# ---------------- 第一幕动画：剑气 / 光柱 / 尘

with Interp("BEZIER"):
    # 9.2-11.7s 地面同心圆环自脚下单向外扩到最大即停、不回缩（示意级亮度）
    for i, (t0, rmax) in enumerate(zip(A_RING_T0, QI_RMAX)):
        r = RINGS[i]
        key_scale(r, 1, (0.02, 0.02, 1.0))
        key_scale(r, f(t0), (0.02, 0.02, 1.0))
        key_scale(r, f(A_RING_MAX), (rmax, rmax, 1.0))
        key_scale(r, f(ACT2_T0), (rmax, rmax, 1.0))
        key_alpha(r, f(t0), 0.0)
        key_alpha(r, f(t0 + 0.4), EFX_ALPHA)
        # 尾帧锁定：光效散尽、地上只留被推伏的同心痕迹
        key_alpha(r, f(A_FADE0), EFX_ALPHA)
        key_alpha(r, f(A_FADE1), 0.10)
        key_alpha(r, f(ACT2_T0), 0.10)

    # 15.4-18.6s 光柱自下而上走完一次即从顶端散尽
    key_scale(pillar, f(A_PILLAR0), (1.0, 1.0, 0.02))
    key_loc(pillar, f(A_PILLAR0), Vector((P.x, P.y, 0.05)))
    key_scale(pillar, f(A_PILLAR_TOP), (1.0, 1.0, 10.5))
    key_loc(pillar, f(A_PILLAR_TOP), Vector((P.x, P.y, 5.3)))
    key_scale(pillar, f(A_PILLAR_GONE), (1.0, 1.0, 10.5))
    key_loc(pillar, f(A_PILLAR_GONE), Vector((P.x, P.y, 11.5)))
    key_alpha(pillar, 1, 0.0)
    key_alpha(pillar, f(A_PILLAR0), 0.0)
    key_alpha(pillar, f(A_PILLAR0 + 0.5), 0.09)
    key_alpha(pillar, f(A_PILLAR_GONE - 0.8), 0.09)
    key_alpha(pillar, f(A_PILLAR_GONE), 0.0)
    key_alpha(pillar, f(ACT2_T0), 0.0)

    # 落地砸出一圈尘环
    key_scale(land_dust, f(A_LAND), (0.05, 0.05, 1.0))
    key_scale(land_dust, f(A_LAND + 0.9), (3.6, 3.6, 1.0))
    key_scale(land_dust, f(ACT2_T0), (3.6, 3.6, 1.0))
    key_alpha(land_dust, 1, 0.0)
    key_alpha(land_dust, f(A_LAND), 0.55)
    key_alpha(land_dust, f(A_LAND + 1.1), 0.0)
    key_alpha(land_dust, f(ACT2_T0), 0.0)

    # 每跺一下扬起一小圈细尘
    for i, t0 in enumerate(A_STOMP_DUST):
        d = STOMP_DUST[i]
        d.location = Vector((P.x - 0.11 * math.cos(RZ), P.y - 0.11 * math.sin(RZ), 0.06))
        key_scale(d, f(t0), (0.05, 0.05, 1.0))
        key_scale(d, f(t0 + 0.55), (1.15, 1.15, 1.0))
        key_scale(d, f(ACT2_T0), (1.15, 1.15, 1.0))
        key_alpha(d, 1, 0.0)
        key_alpha(d, f(t0), 0.5)
        key_alpha(d, f(t0 + 0.6), 0.0)
        key_alpha(d, f(ACT2_T0), 0.0)


# ---------------- 第二幕动画：身体


with Interp("BEZIER"):
    pose(J, f(ACT2_T0), POSE_END12)
    # 0-2s 沉肩坠肘、腰身一拧，向正前方斩出一剑，收势剑尖斜指地面定住半拍
    pose(J, f(T_WIND1 - 0.35), POSE_END12)
    pose(J, f(T_WIND1), POSE_WIND1)
    pose(J, f(T_SLASH1), POSE_SLASH1)
    pose(J, f(T_WIND2 - 0.35), POSE_SLASH1)
    # 2-3.5s 转腕拧腰向侧面再斩一剑，手臂展成一条直线、收势定住半拍
    pose(J, f(T_WIND2), POSE_WIND2)
    pose(J, f(T_SLASH2), POSE_SLASH2)
    pose(J, f(T_THROW_WIND - 0.25), POSE_SLASH2)
    # 3.5-5s 抬手把剑向上抛出
    pose(J, f(T_THROW_WIND), POSE_THROW_WIND)
    pose(J, f(T_THROW), POSE_THROW)
    pose(J, f(T_SWORD_HIGH - 0.15), POSE_THROW)
    # 5-6.5s 单手两指收到胸前、闭眼（仰头看剑 → 头回正）
    pose(J, f(T_SEAL), POSE_SEAL1)
    pose(J, f(T_EYES_CLOSED), POSE_SEAL_STILL)
    pose(J, f(T_POINT - 0.5), POSE_SEAL_STILL)
    # 13.5-14.5s 睁眼、亮相指地、前踏半马步、定住半拍
    pose(J, f(T_POINT), POSE_POINT)
    pose(J, f(T_JUMP0 - 0.15), POSE_POINT)
    # 17.5-18.5s 双臂平张、单脚跳起、身体转两圈
    pose(J, f(T_JUMP0 + 0.1), POSE_SPREAD)
    pose(J, f(T_FLIP0 - 0.05), POSE_SPREAD)
    # 19.5-20.5s 跃开翻两个跟斗落地
    pose(J, f(T_FLIP0 + 0.25), POSE_TUCK)
    pose(J, f(T_FLIP1 - 0.15), POSE_TUCK)
    pose(J, f(T_FLIP1 + 0.05), POSE_LAND)
    pose(J, f(T_LAND_UP + 0.05), POSE_STAND)
    # 21.2-22s 仰头大笑，肩背随笑起伏
    pose(J, f(T_LAUGH), POSE_LAUGH)
    for k, t in enumerate(T_LAUGH_BOBS):
        d = dict(POSE_LAUGH)
        d["pelvis"] = (-8 + (3 if k % 2 == 0 else -2), 0, 0)
        d["head"] = (-38 + (4 if k % 2 == 0 else -3), 0, 0)
        pose(J, f(t), d)
    pose(J, TOTAL, POSE_LAUGH)

# root：位置 / 自转 / 跳起 / 踩剑 / 跟斗
JUMP_T0, JUMP_T1 = T_JUMP0, T_JUMP1
with Interp("BEZIER"):
    key_loc(root, f(ACT2_T0), P)
    key_loc(root, f(JUMP_T0), P)
    key_loc(root, f(T_JUMP_TOP), P + Vector((0, 0, STAND_Z + 0.35)))
    key_loc(root, f(JUMP_T1), P + Vector((0, 0, STAND_Z)))
    # 18.9-19.4 随剑上下震两下即稳
    key_loc(root, f(T_MERGE), P + Vector((0, 0, STAND_Z)))
    for tb, dz in zip(T_BOUNCE, (-0.09, 0.0, -0.06, 0.0)):
        key_loc(root, f(tb), P + Vector((0, 0, STAND_Z + dz)))
    key_loc(root, f(T_FLIP0), P + Vector((0, 0, STAND_Z)))
    key_rot(root, f(ACT2_T0), (0, 0, RZ))
    key_rot(root, f(JUMP_T0), (0, 0, RZ))
with Interp("LINEAR"):
    key_rot(root, f(JUMP_T1), (0, 0, RZ + math.radians(360 * AIR_SPINS)))  # 空中绕竖直体轴转 AIR_SPINS 圈
with Interp("BEZIER"):
    key_rot(root, f(T_FLIP0), (0, 0, RZ + math.radians(360 * AIR_SPINS)))

# 19.5-20.5s 跃开、空中连翻两个跟斗、落回原地：逐帧算 root，使骨盆走一条抛物线
FLIP_T0, FLIP_T1 = T_FLIP0, T_FLIP1
with Interp("LINEAR"):
    fr0, fr1 = f(FLIP_T0), f(FLIP_T1)
    p0 = P + Vector((0, 0, STAND_Z + HIP_Z))   # 起跳时骨盆
    p1 = P + Vector((0, 0, HIP_Z))             # 落地时骨盆
    peak = 1.1
    for fr in range(fr0, fr1 + 1):
        u = (fr - fr0) / (fr1 - fr0)
        pel = p0.lerp(p1, u) + Vector((0, 0, peak * 4 * u * (1 - u))) + FRONT * (0.9 * math.sin(math.pi * u))
        ang_x = -math.radians(360 * FLIP_COUNT) * u  # 前空翻 FLIP_COUNT 周
        rot = Euler((ang_x, 0, RZ + math.radians(360 * AIR_SPINS)))
        off = rot.to_matrix() @ Vector((0, 0, HIP_Z))
        key_loc(root, fr, pel - off)
        key_rot(root, fr, rot)
with Interp("BEZIER"):
    key_loc(root, f(T_LAND_DIP), P + Vector((0, 0, -0.06)))
    key_loc(root, f(T_LAND_UP), P)
    key_loc(root, TOTAL, P)
    key_rot(root, f(T_LAND_DIP), (0, 0, RZ + math.radians(360 * AIR_SPINS)))
    key_rot(root, TOTAL, (0, 0, RZ + math.radians(360 * AIR_SPINS)))

bpy.context.view_layer.update()

# ---------------------------------------------------------------- 动画：单剑

GRIP = Vector((0, 0, -0.30))       # 剑体中心相对手心
F_THROW = f(T_THROW)                  # 脱手
HIGH = P + Vector((0, 0, HIGH_Z))

with Interp("BEZIER"):
    # 第二幕起点到脱手：剑在右手里、逐帧跟手（剑沿前臂方向、剑尖朝前臂延伸方向）。
    # ⚠ 只能从 ACT2_T0 起——原合并版从第 1 帧起采样，把第一幕「剑在背上 / 飞到身前 / 绕身」的
    #   全部 K 帧覆盖成了「握在手里」，即用户看到的「一开始飞下来手里就拿着剑」（2026-08-18 修）。
    for fr in range(f(ACT2_T0), F_THROW + 1):
        sc.frame_set(fr)
        bpy.context.view_layer.update()
        hm = J["handR"].matrix_world
        em = J["elbowR"].matrix_world
        hand = hm.to_translation()
        axis = (hand - em.to_translation()).normalized()  # 前臂方向 = 剑指向（剑尖朝前臂延伸方向）
        rot = axis.to_track_quat("-Z", "Y").to_euler()    # 剑体 -Z 是剑尖
        key_loc(sword, fr, hand + axis * 0.50)
        key_rot(sword, fr, rot)
    # 3.85-5s 竖着剑尖朝上一路飞到高空停住（HIGH_Z 是画面上三分之一线）
    key_rot(sword, f(T_THROW + 0.25), (math.pi, 0, 0))            # 剑尖朝上
    key_loc(sword, f(T_SWORD_HIGH), HIGH)
    key_rot(sword, f(T_SWORD_HIGH), (math.pi, 0, 0))
    key_loc(sword, f(T_SPLIT), HIGH)
    key_rot(sword, f(T_SPLIT), (math.pi, 0, 0))

# 化二十把：**过程，不是瞬间替换**（follow-up 044）。原本单剑同帧隐去、二十把
# 同帧在环半径上出现，等于没给 Seedance 做分化特效的时间窗。现在二十把自单剑所在
# 的那一点向外推到环半径，用掉 T_SPLIT→T_SPLIT_DONE 一整段；单剑在这段里淡到不见。
F_SPLIT = f(T_SPLIT)
F_SPLIT_DONE = f(T_SPLIT_DONE)
key_vis(sword, 1, True)
key_emit(sword, F_SPLIT, 3.2)
key_emit(sword, f(T_SPLIT + 0.55), 0.3)
key_vis(sword, f(T_SPLIT + 0.6), False)

# 二十把：成环 → 平转三圈（6.5-11s，LINEAR）→ 齐冲天（11-13.5s）→ 逐把落下插地（14.5-17.5s）
# → 一齐拔起并作一柄（18.5-18.9s）
RING_ANG = [2 * math.pi * i / N_SWORDS for i in range(N_SWORDS)]
GROUND_SLOTS = []
for i in range(N_SWORDS):
    a = RING_ANG[i] + math.radians(random.uniform(-9, 9))
    r = GROUND_R + random.uniform(-0.55, 0.55)
    GROUND_SLOTS.append(P + FRONT * (r * math.cos(a)) + R_VEC * (r * math.sin(a)) + Vector((0, 0, 0.42 - 0.35)))
DROP_ORDER = list(range(N_SWORDS))
random.shuffle(DROP_ORDER)

F_MERGE = f(T_MERGE)
FOOT_SWORD_C = None  # 稍后算

for i, sw in enumerate(SWORDS):
    key_vis(sw, 1, False)
    key_vis(sw, F_SPLIT, True)
    with Interp("BEZIER"):
        # 分化段：自单剑那一点向外推到环半径（慢，留给 Seedance 做分化特效）
        ang0 = RING_ANG[i]
        key_loc(sw, F_SPLIT, HIGH)
        key_rot(sw, F_SPLIT, (math.pi, 0, 0))
        key_loc(sw, F_SPLIT_DONE,
                P + FRONT * (RING_R * math.cos(ang0)) + R_VEC * (RING_R * math.sin(ang0))
                + Vector((0, 0, HIGH_Z)))
        key_rot(sw, F_SPLIT_DONE, (math.pi, 0, 0))
    with Interp("LINEAR"):
        # 成环后平转一圈（2.8s／圈，follow-up 050 由两圈减半）
        fr0, fr1 = F_SPLIT_DONE, f(T_SPIN_END)
        span = fr1 - fr0
        for k in range(0, span + 1, 2):
            u = k / span
            ang = RING_ANG[i] + SPIN_TURNS * 2 * math.pi * u
            key_loc(sw, fr0 + k, P + FRONT * (RING_R * math.cos(ang)) + R_VEC * (RING_R * math.sin(ang)) + Vector((0, 0, HIGH_Z)))
            key_rot(sw, fr0 + k, (math.pi, 0, 0))
    with Interp("BEZIER"):
        # 11-13.5s 同时向上加速齐冲上半空、脱出画面上缘
        ang = RING_ANG[i]
        top = P + FRONT * (RING_R * math.cos(ang)) + R_VEC * (RING_R * math.sin(ang)) + Vector((0, 0, RISE_Z))
        key_loc(sw, f(T_SPIN_END), P + FRONT * (RING_R * math.cos(ang)) + R_VEC * (RING_R * math.sin(ang)) + Vector((0, 0, HIGH_Z)))
        key_loc(sw, f(T_RISE_END), top)
        key_rot(sw, f(T_RISE_END), (math.pi, 0, 0))
        # 14.5-17.5s 一把接一把极速落下、途中翻成剑尖朝下、插进他四周地面
        order = DROP_ORDER.index(i)
        t0 = T_DROP0 + order * (T_DROP_SPAN / (N_SWORDS - 1))
        t1 = t0 + T_DROP_DUR
        slot = GROUND_SLOTS[i]
        start = Vector((slot.x, slot.y, RISE_Z))
        key_loc(sw, f(t0), start)
        key_rot(sw, f(t0), (math.pi, 0, 0))
        key_rot(sw, f(t0 + 0.2), (0, 0, 0))            # 途中一次性翻转成剑尖朝下
        key_loc(sw, f(t1), slot)
        key_rot(sw, f(t1), (0, 0, 0))
        key_loc(sw, f(T_JUMP1), slot)
        key_rot(sw, f(T_JUMP1), (0, 0, 0))
        # 触地即光灭、恢复金属本色
        key_emit(sw, 1, 3.2)
        key_emit(sw, f(t1 - 0.02), 3.2)
        key_emit(sw, f(t1 + 0.04), 0.15)
        key_emit(sw, f(T_JUMP1), 0.15)
        key_emit(sw, f(T_JUMP1 + 0.2), 3.2)                       # 拔起时重新亮起
    key_vis(sw, F_MERGE, False)

# 18.5-18.9s 二十把一齐拔地而起、在半空并作一柄悬在单脚正下方
sc.frame_set(f(T_MERGE))
bpy.context.view_layer.update()
foot = J["kneeR"].matrix_world.to_translation() + Vector((0, 0, -0.42))  # 右脚底附近
# 踩剑时**剑身垂直向下、剑尖朝下**（follow-up 044 用户指出，原来摆成了水平）。
# 这也是 s11 场景卡「御剑态」的锁定形象：一柄剑尖朝下的竖直长剑，人悬于其正上方。
# 剑体原点在剑身中心，柄顶在 +0.66 —— 让柄顶正好托住脚底。
HILT_TOP_Z = 0.66
FOOT_SWORD_C = Vector((foot.x, foot.y, foot.z - 0.02 - HILT_TOP_Z))
with Interp("BEZIER"):
    for i, sw in enumerate(SWORDS):
        key_loc(sw, f(T_JUMP1), GROUND_SLOTS[i])
        key_loc(sw, f(T_GATHER1), FOOT_SWORD_C)
        key_rot(sw, f(T_JUMP1), (0, 0, 0))
        key_rot(sw, f(T_GATHER1), (0.0, 0.0, 0.0))   # 竖直、剑尖朝下

# 合成的那一柄：竖直悬在他单脚正下方、剑尖朝下、柄顶托住脚底，震两下即稳；19.5s 他跃开后剑仍悬着；
# 20.5-20.85s 冲向高空；20.85-21.2s 垂直落回自身后插回背鞘
key_vis(sword, F_MERGE, True)
SW_FLAT = Euler((0.0, 0.0, 0.0))   # 竖直剑尖朝下（原为水平，follow-up 044 校正）
with Interp("BEZIER"):
    key_loc(sword, F_MERGE, FOOT_SWORD_C)
    key_rot(sword, F_MERGE, SW_FLAT)
    for tb, dz in zip(T_BOUNCE, (-0.09, 0.0, -0.06, 0.0)):
        key_loc(sword, f(tb), FOOT_SWORD_C + Vector((0, 0, dz)))
    key_loc(sword, f(T_FLIP1), FOOT_SWORD_C)
    key_rot(sword, f(T_FLIP1), SW_FLAT)
    key_rot(sword, f(T_SWORD_UP), (math.pi, 0, 0))                                   # 剑尖朝上冲天
    key_loc(sword, f(T_SWORD_APEX), Vector((P.x, P.y, RISE_Z * 0.7)))
    key_rot(sword, f(T_SWORD_APEX), (math.pi, 0, 0))
    key_rot(sword, f(T_SWORD_APEX + 0.1), (0, 0, 0))                                         # 掉头剑尖朝下落回

sc.frame_set(f(T_SHEATH))
bpy.context.view_layer.update()
SWORD_ON_BACK = Matrix.Translation((-0.06, 0.22, 0.42)) @ Euler((math.radians(18), 0.0, math.radians(-14))).to_matrix().to_4x4()
with Interp("BEZIER"):
    m = pelvis.matrix_world @ SWORD_ON_BACK
    key_loc(sword, f(T_SHEATH - 0.15), m.to_translation() + Vector((0, 0, 0.9)))
    key_rot(sword, f(T_SHEATH - 0.15), (0, 0, 0))
    for fr in range(f(T_SHEATH), TOTAL + 1):
        sc.frame_set(fr)
        bpy.context.view_layer.update()
        m = pelvis.matrix_world @ SWORD_ON_BACK
        key_loc(sword, fr, m.to_translation())
        key_rot(sword, fr, m.to_euler())
# 入鞘瞬间剑光熄灭
key_emit(sword, 1, 3.2)
key_emit(sword, f(T_SHEATH - 0.05), 3.2)
key_emit(sword, f(T_SHEATH + 0.05), 0.15)
key_emit(sword, TOTAL, 0.15)

# ---------------------------------------------------------------- 动画：沟壑 / 剑气 / 尘

with Interp("LINEAR"):
    # 直沟：0.95s 起自脚前向正前方长出去，1.75s 到画面下缘
    key_scale(t1_root, 1, (1.0, 0.001, 1.0))
    key_scale(t1_root, f(T_SLASH1), (1.0, 0.001, 1.0))
    key_scale(t1_root, f(T_QI1_END), (1.0, 1.0, 1.0))
    key_scale(t1_root, TOTAL, (1.0, 1.0, 1.0))
    # 剑气薄片沿沟飞
    key_vis(qi1, 1, False)
    key_vis(qi1, f(T_SLASH1), True)
    key_loc(qi1, f(T_SLASH1), P + FRONT * 0.7 + Vector((0, 0, 0.12)))
    key_loc(qi1, f(T_QI1_END), P + FRONT * (0.7 + T1_LEN) + Vector((0, 0, 0.12)))
    key_vis(qi1, f(T_QI1_END + 0.05), False)
    # 月牙沟：2.5s 起自画左（他的右侧）沿弧甩到画面另一侧，3.4s 走完
    for k, seg in enumerate(ARC_SEGS):
        t = T_SLASH2 + (T_ARC_END - T_SLASH2) * k / (ARC_N - 1)
        key_scale(seg, 1, (0.001, 0.001, 0.001))
        key_scale(seg, f(t), (0.001, 0.001, 0.001))
        key_scale(seg, f(t + 0.06), (1.0, 1.0, 1.0))
        key_scale(seg, TOTAL, (1.0, 1.0, 1.0))
    key_vis(qi2, 1, False)
    key_vis(qi2, f(T_SLASH2), True)
    for k, seg in enumerate(ARC_SEGS):
        t = T_SLASH2 + (T_ARC_END - T_SLASH2) * k / (ARC_N - 1)
        key_loc(qi2, f(t), Vector(seg.location) + Vector((0, 0, 0.12)))
    key_vis(qi2, f(T_ARC_END + 0.05), False)

with Interp("BEZIER"):
    # 20.5s 落地压出一圈细尘
    for d, t0, rmax in ((land_dust, T_FLIP1, 3.0), (jump_dust, T_JUMP0, 2.0)):
        d.location = Vector((P.x, P.y, 0.06))
        key_scale(d, 1, (0.05, 0.05, 1.0))
        key_scale(d, f(t0), (0.05, 0.05, 1.0))
        key_scale(d, f(t0 + 0.8), (rmax, rmax, 1.0))
        key_scale(d, TOTAL, (rmax, rmax, 1.0))
        key_alpha(d, 1, 0.0)
        key_alpha(d, f(t0), 0.55)
        key_alpha(d, f(t0 + 1.0), 0.0)
        key_alpha(d, TOTAL, 0.0)

# ---------------------------------------------------------------- 机位：11s 齐冲天时向后拉开一档

with Interp("BEZIER"):
    key_loc(cam, 1, CAM_POS)
    key_loc(cam, f(T_PULL0), CAM_POS)
    key_loc(cam, f(T_PULL1), CAM_POS_FAR)
    key_loc(cam, TOTAL, CAM_POS_FAR)

# ---------------------------------------------------------------- 插值后处理

for sw in SWORDS + [sword]:
    set_interp(sw, "CONSTANT", data_path="scale")
    set_interp(sw, "LINEAR", data_path="location", frame_range=(F_SPLIT_DONE, f(T_SPIN_END)))
    set_interp(sw, "LINEAR", data_path="rotation_euler", frame_range=(F_SPLIT_DONE, f(T_SPIN_END)))
set_interp(root, "LINEAR", data_path="rotation_euler", frame_range=(f(JUMP_T0), f(JUMP_T1)))
set_interp(root, "LINEAR", frame_range=(f(FLIP_T0), f(FLIP_T1)))
for o in (qi1, qi2, t1_root):
    set_interp(o, "LINEAR")
for o in (qi1, qi2):
    set_interp(o, "CONSTANT", data_path="scale")
for seg in ARC_SEGS:
    set_interp(seg, "LINEAR")

# ---------------------------------------------------------------- 输出

sc.render.resolution_percentage = 100
sc.render.fps = FPS
sc.frame_start = 1
sc.frame_end = TOTAL
sc.frame_set(1)
sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_mode = "RGB"
sc.render.filepath = "//frames/f"
bpy.ops.wm.save_mainfile()

sc.frame_set(f(9.0))
bpy.context.view_layer.update()
for label, pt in (("庙", TEMPLE + Vector((0, 0, 3.0))), ("人头", P + Vector((0, 0, 1.6))), ("高悬剑", HIGH), ("直沟末端", P + FRONT * (0.7 + T1_LEN))):
    uv = world_to_camera_view(sc, cam, pt)
    print(f"UV@9s {label:6s} u={uv.x:6.3f} v={uv.y:6.3f}")
sc.frame_set(f(16.0))
bpy.context.view_layer.update()
for label, pt in (("庙", TEMPLE + Vector((0, 0, 3.0))), ("人头", P + Vector((0, 0, 1.6)))):
    uv = world_to_camera_view(sc, cam, pt)
    print(f"UV@16s {label:6s} u={uv.x:6.3f} v={uv.y:6.3f}")
print(f"PREVIZ OK frames=1..{TOTAL} fps={FPS} tilt={TILT_DEG}deg HIGH_Z={HIGH_Z:.2f}")
