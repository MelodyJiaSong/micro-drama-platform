"""通用 A 档 previz 引擎 —— 读一份声明式 TOML，建场 + 解算机位 + 渲 MP4。

用法（仓库根目录）：
    blender -b --factory-startup --python tools/previz/build_previz.py -- <config.toml> [--no-render]

设计边界（ai_video.md rule 12.16 + 2026-08-22 分工裁定）：
    3D 只承担「机位几何 / 构图占比 / 站位朝向 / 尺度 / 遮挡 / 轨迹 / 时刻表」；
    长相、材质、光色、表演质感、次级运动、特效形态一律不碰，交 Seedance。
    因此本引擎只有色块 proxy 与灰模摆件，没有材质、没有灯光美术、没有粒子。

per-shot 的 previz_config.toml 是 3D 层的唯一真相：shot md 的 prompt 不再复述
它管的画面坐标与相对大小，README 只记「为什么这么摆」不记数值。
"""

from __future__ import annotations

import math
import shutil
import sys
import tomllib
from pathlib import Path

import bpy
from mathutils import Euler, Matrix, Vector
from bpy_extras.object_utils import world_to_camera_view

# ---------------------------------------------------------------- 配置 schema

# 键名白名单：拼错直接报错，绝不静默忽略（沿用 shot12 previz 的既定规则）
SCHEMA = {
    "全局": {"shot", "fps", "total_sec", "场景", "分辨率", "地面", "原点偏移", "贴地", "素模场景"},
    "机位": {"俯角", "焦距", "基准主体", "占画高", "横向偏移", "距离倍数", "方位角", "位置", "切墙", "起始俯仰偏移", "锁定主体"},
    "运镜": {"类型", "起", "止", "量"},
    "角色": {"名", "色", "身高", "关键帧"},
    "角色.关键帧": {"t", "位置", "朝向", "姿态"},
    "道具": {"名", "形", "尺寸", "位置", "色", "朝向", "关键帧"},
    "道具.关键帧": {"t", "位置", "朝向", "尺寸"},
}

COLORS = {
    "绿": (0.10, 0.75, 0.15), "蓝": (0.10, 0.30, 0.90), "红": (0.85, 0.10, 0.10),
    "青": (0.10, 0.80, 0.80), "黄": (0.90, 0.80, 0.10), "紫": (0.55, 0.15, 0.85),
    "橙": (0.95, 0.45, 0.05), "白": (0.90, 0.90, 0.90), "灰": (0.35, 0.35, 0.38),
    "深灰": (0.18, 0.18, 0.20), "粉": (0.95, 0.45, 0.65),
}

# 定式姿态：关节名 → [X, Y, Z] 欧拉角(度)。
# X 正 = 该肢向前抬 / 前屈；Y = 向体侧张开（左右镜像）；Z = 扭转。
# 没列的关节 = 竖直中立位。A 档只给这几个定式，指节级姿态属 B 档、不在本引擎。
POSES = {
    "站": {},
    "站定": {},
    "叉腰": {"shoulderL": (0, 0, -55), "elbowL": (0, 0, -75),
             "shoulderR": (0, 0, 55), "elbowR": (0, 0, 75)},
    "抱": {"shoulderL": (-70, 0, -20), "elbowL": (-75, 0, 0),
           "shoulderR": (-70, 0, 20), "elbowR": (-75, 0, 0)},
    "伸手": {"shoulderR": (-85, 0, 0), "elbowR": (-8, 0, 0)},
    "双手前伸": {"shoulderL": (-85, 0, 0), "elbowL": (-8, 0, 0),
                 "shoulderR": (-85, 0, 0), "elbowR": (-8, 0, 0)},
    "端物": {"shoulderL": (-55, 0, -12), "elbowL": (-70, 0, 0),
             "shoulderR": (-55, 0, 12), "elbowR": (-70, 0, 0)},
    "抬头": {"head": (-28, 0, 0)},
    "低头": {"head": (30, 0, 0)},
    "俯身": {"pelvis": (45, 0, 0), "head": (-25, 0, 0),
             "shoulderL": (-25, 0, 0), "shoulderR": (-25, 0, 0)},
    "半躬": {"pelvis": (28, 0, 0), "head": (-15, 0, 0)},
    "蹲": {"hipL": (-85, 0, 0), "kneeL": (105, 0, 0), "ankleL": (-20, 0, 0),
           "hipR": (-85, 0, 0), "kneeR": (105, 0, 0), "ankleR": (-20, 0, 0),
           "pelvis": (18, 0, 0)},
    "单膝跪": {"hipL": (-95, 0, 0), "kneeL": (95, 0, 0),
               "hipR": (-75, 0, 0), "kneeR": (100, 0, 0), "pelvis": (10, 0, 0)},
    "跪": {"hipL": (-88, 0, 0), "kneeL": (115, 0, 0),
           "hipR": (-88, 0, 0), "kneeR": (115, 0, 0), "pelvis": (8, 0, 0)},
    "坐": {"hipL": (-90, 0, 0), "kneeL": (88, 0, 0),
           "hipR": (-90, 0, 0), "kneeR": (88, 0, 0)},
    "跌坐": {"hipL": (-92, 0, 12), "kneeL": (70, 0, 0),
             "hipR": (-92, 0, -12), "kneeR": (70, 0, 0), "pelvis": (-12, 0, 0)},
    "躺": {"pelvis": (-88, 0, 0)},
    "踏剑": {"hipL": (-18, 0, 0), "kneeL": (25, 0, 0),
             "hipR": (-8, 0, 0), "kneeR": (12, 0, 0),
             "shoulderL": (0, 0, -35), "shoulderR": (0, 0, 35)},
    "行走": {"hipL": (-25, 0, 0), "kneeL": (15, 0, 0), "hipR": (22, 0, 0),
             "shoulderL": (18, 0, 0), "shoulderR": (-18, 0, 0)},
    "背对": {},
}

JOINTS = ("pelvis", "head", "shoulderL", "shoulderR", "elbowL", "elbowR",
          "hipL", "hipR", "kneeL", "kneeR", "ankleL", "ankleR")

# 基础姿态定义全身；修饰姿态只动它点名的关节，叠在当前基础姿态之上并跨关键帧保持。
# 没这个区分的话，"抬头" 会把 "跌坐" 的腿一起清零——人物会当场站起来。
# 配置里可写 "跌坐+抬头" 显式组合；只写修饰姿态则沿用上一个基础姿态。
BASE_POSES = {"站", "站定", "坐", "跌坐", "跪", "单膝跪", "蹲", "躺", "行走", "踏剑", "背对"}

# 少数姿态光靠关节摆不出来，要整体翻转躯干（躺＝整个人放平，不是坐着往后仰）
ROOT_TILT = {"躺": -78.0}


def die(msg: str) -> None:
    print(f"\n[previz] 错误：{msg}\n", file=sys.stderr)
    sys.exit(1)


def check_keys(table: dict, allowed: set, where: str) -> None:
    bad = set(table) - allowed
    if bad:
        die(f"{where} 出现未知键 {sorted(bad)}；合法键＝{sorted(allowed)}（拼错不静默忽略）")


# ---------------------------------------------------------------- 载入配置

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
if not argv:
    die("用法：blender -b --factory-startup --python tools/previz/build_previz.py -- <config.toml> [--no-render]")
CFG_PATH = Path(argv[0]).resolve()
DO_RENDER = "--no-render" not in argv
if not CFG_PATH.is_file():
    die(f"配置不存在：{CFG_PATH}")

CFG = tomllib.loads(CFG_PATH.read_text(encoding="utf-8"))
G = CFG.get("全局", {})
check_keys(G, SCHEMA["全局"], "[全局]")
CAM = CFG.get("机位", {})
check_keys(CAM, SCHEMA["机位"], "[机位]")

SHOT = G.get("shot") or CFG_PATH.parent.parent.name
FPS = int(G.get("fps", 24))
TOTAL = float(G["total_sec"]) if "total_sec" in G else die("[全局] 缺 total_sec")
RES = G.get("分辨率", [960, 540])
OUT_DIR = CFG_PATH.parent
REPO = Path(__file__).resolve().parents[2]
# 本镜局部坐标 → 场景坐标的平移。场景主档是米制的，但每个镜发生在场景的不同角落
# （s1 二层地板 z≈4.53、临街正门 y≈0…），配置里只写「本镜局部」坐标，靠这行落位。
ORIGIN = Vector([float(x) for x in G.get("原点偏移", [0, 0, 0])])


def f(t: float) -> int:
    """秒 → 帧（1-based，与 Blender 一致）。"""
    return max(1, int(round(t * FPS)) + 1)


# ---------------------------------------------------------------- 场景底座

scene_name = G.get("场景")
scene_blend = None
if scene_name:
    src = REPO / "ai_videos" / "xianjian_yi_mv" / "2_世界观人设" / "scenes" / scene_name / f"{scene_name}.blend"
    if src.is_file():
        # rule 12.16：场景主档永不修改，只在 previz 目录里改副本
        scene_blend = OUT_DIR / f"{SHOT}_previz.blend"
        shutil.copyfile(src, scene_blend)
        bpy.ops.wm.open_mainfile(filepath=str(scene_blend))
    else:
        print(f"[previz] 提示：场景 {scene_name} 无 .blend，改用灰模地面")

if scene_blend is None:
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)

scene = bpy.context.scene
PREVIZ = bpy.data.collections.new("PREVIZ")
scene.collection.children.link(PREVIZ)


def link_previz(ob):
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    PREVIZ.objects.link(ob)


def mat(name: str, rgb, emit: float = 0.0):
    m = bpy.data.materials.new(name=name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.6
    if "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
    if "Emission Strength" in bsdf.inputs:
        bsdf.inputs["Emission Strength"].default_value = emit
    return m


MATS = {k: mat(f"M_{k}", v, 0.25) for k, v in COLORS.items()}

# 户外场景地形起伏，原点的 Z 手填必错：朝下打一条射线找真实地面高度。
if G.get("贴地") and scene_name:
    bpy.context.view_layer.update()
    _d = bpy.context.evaluated_depsgraph_get()
    _hit, _loc, *_ = scene.ray_cast(_d, Vector((ORIGIN.x, ORIGIN.y, 400.0)),
                                    Vector((0, 0, -1)), distance=2000.0)
    if _hit:
        print(f"  贴地：原点 Z {ORIGIN.z:.2f} → {_loc.z:.2f}")
        ORIGIN = Vector((ORIGIN.x, ORIGIN.y, _loc.z))
    else:
        print("  贴地：射线没打到地面，沿用配置里的 Z")


def _mat_for(color_name: str):
    if color_name not in MATS:
        die(f"未知颜色「{color_name}」；可用＝{sorted(COLORS)}")
    return MATS[color_name]


def setpar(child, parent):
    """保持世界位置的绑定（用于机位 rig）。"""
    bpy.context.view_layer.update()
    child.parent = parent
    child.matrix_parent_inverse = parent.matrix_world.inverted()


def attach(child, parent, local_loc):
    """按局部偏移绑定（用于关节人骨架）。

    setpar 会保留子件的世界位置，拿它搭骨架的话每一节都会留在「本该是局部
    偏移」的世界坐标上——整个人会塌成地面上一小块。骨架必须走这条。
    """
    child.parent = parent
    child.matrix_parent_inverse = Matrix.Identity(4)
    child.location = Vector(local_loc)


def empty(name, loc, parent=None):
    bpy.ops.object.empty_add(type="PLAIN_AXES", radius=0.1, location=loc)
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


def cyl(name, r, h, loc, material, parent=None):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, vertices=20, location=loc)
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


def key_loc(ob, frame, loc):
    ob.location = Vector(loc)
    ob.keyframe_insert("location", frame=frame)


def key_rot(ob, frame, rot_deg):
    ob.rotation_euler = Euler([math.radians(d) for d in rot_deg])
    ob.keyframe_insert("rotation_euler", frame=frame)


def key_scale(ob, frame, s):
    ob.scale = Vector(s)
    ob.keyframe_insert("scale", frame=frame)


# 地面：没有场景主档时给一块，让 proxy 有参照、影子有落点
if G.get("地面", scene_blend is None):
    box("GROUND", (200, 200, 0.02), tuple(ORIGIN + Vector((0, 0, -0.01))), MATS["深灰"])


# ---------------------------------------------------------------- 关节人 proxy

def make_figure(name: str, color: str, height: float):
    """一个有四肢与手脚的关节替身。比例按 7.5 头身粗算。

    rule 12.16 要求 proxy 是 articulated 且手脚可辨——所以四肢分上下段、
    手脚与鼻锥用更亮的对比色，好让「谁在朝哪、手伸到哪」在小画面里也读得出。
    骨架一律用 attach（局部偏移），不能用 setpar。
    """
    m = _mat_for(color)
    m_lim = _mat_for("白" if color != "白" else "黄")
    h = height
    root = empty(f"{name}", (0, 0, 0))
    j = {}

    j["pelvis"] = empty(f"{name}_pelvis", (0, 0, 0))
    attach(j["pelvis"], root, (0, 0, h * 0.53))
    torso = box(f"{name}_torso", (h * 0.17, h * 0.10, h * 0.30), (0, 0, 0), m)
    attach(torso, j["pelvis"], (0, 0, h * 0.15))
    j["head"] = empty(f"{name}_head", (0, 0, 0))
    attach(j["head"], j["pelvis"], (0, 0, h * 0.30))
    hd = sphere(f"{name}_head_m", h * 0.065, (0, 0, 0), m)
    attach(hd, j["head"], (0, 0, h * 0.065))
    # 鼻锥：朝向的可读性全靠它（小画面里躯干看不出正反）
    nose = cyl(f"{name}_nose", h * 0.020, h * 0.060, (0, 0, 0), m_lim)
    nose.rotation_euler = Euler((math.radians(90), 0, 0))
    attach(nose, j["head"], (0, -h * 0.080, h * 0.065))

    for side, sx in (("L", 1.0), ("R", -1.0)):
        sh = empty(f"{name}_shoulder{side}", (0, 0, 0))
        attach(sh, j["pelvis"], (sx * h * 0.105, 0, h * 0.28))
        j[f"shoulder{side}"] = sh
        ua = box(f"{name}_uarm{side}", (h * 0.045, h * 0.045, h * 0.15), (0, 0, 0), m)
        attach(ua, sh, (0, 0, -h * 0.075))
        el = empty(f"{name}_elbow{side}", (0, 0, 0))
        attach(el, sh, (0, 0, -h * 0.15))
        j[f"elbow{side}"] = el
        la = box(f"{name}_larm{side}", (h * 0.04, h * 0.04, h * 0.13), (0, 0, 0), m)
        attach(la, el, (0, 0, -h * 0.065))
        hnd = box(f"{name}_hand{side}", (h * 0.05, h * 0.035, h * 0.055), (0, 0, 0), m_lim)
        attach(hnd, el, (0, 0, -h * 0.155))

        hp = empty(f"{name}_hip{side}", (0, 0, 0))
        attach(hp, j["pelvis"], (sx * h * 0.06, 0, 0))
        j[f"hip{side}"] = hp
        ul = box(f"{name}_uleg{side}", (h * 0.055, h * 0.055, h * 0.26), (0, 0, 0), m)
        attach(ul, hp, (0, 0, -h * 0.13))
        kn = empty(f"{name}_knee{side}", (0, 0, 0))
        attach(kn, hp, (0, 0, -h * 0.26))
        j[f"knee{side}"] = kn
        ll = box(f"{name}_lleg{side}", (h * 0.048, h * 0.048, h * 0.24), (0, 0, 0), m)
        attach(ll, kn, (0, 0, -h * 0.12))
        an = empty(f"{name}_ankle{side}", (0, 0, 0))
        attach(an, kn, (0, 0, -h * 0.24))
        j[f"ankle{side}"] = an
        ft = box(f"{name}_foot{side}", (h * 0.05, h * 0.11, h * 0.035), (0, 0, 0), m_lim)
        attach(ft, an, (0, -h * 0.025, -h * 0.018))

    return root, j


def apply_pose(joints, frame, pose_name, state, root=None):
    parts = [x.strip() for x in str(pose_name).split("+") if x.strip()]
    for part in parts:
        if part not in POSES:
            die(f"未知姿态「{part}」；可用＝{sorted(POSES)}")
    bases = [p for p in parts if p in BASE_POSES]
    if bases:
        state["base"] = bases[-1]
    spec = dict(POSES[state["base"]])
    for m in (p for p in parts if p not in BASE_POSES):
        spec.update(POSES[m])
    for jn in JOINTS:
        if jn in joints:
            key_rot(joints[jn], frame, spec.get(jn, (0, 0, 0)))
    if root is not None:
        state["root_tilt"] = ROOT_TILT.get(state["base"], 0.0)


# ---------------------------------------------------------------- 建角色 / 道具

ACTORS: dict[str, dict] = {}
LAST_KEY_T = 0.0

for a in CFG.get("角色", []):
    check_keys(a, SCHEMA["角色"], "[[角色]]")
    nm = a["名"]
    root, joints = make_figure(nm, a.get("色", "绿"), float(a.get("身高", 1.72)))
    pose_state = {"base": "站", "root_tilt": 0.0}
    last_yaw = 0.0
    kfs = a.get("关键帧", [])
    if not kfs:
        die(f"角色「{nm}」没有关键帧——A 档至少要给一帧站位")
    for kf in kfs:
        check_keys(kf, SCHEMA["角色.关键帧"], f"[[角色.关键帧]] of {nm}")
        t = float(kf["t"])
        LAST_KEY_T = max(LAST_KEY_T, t)
        fr = f(t)
        pos = kf.get("位置")
        if pos is not None:
            key_loc(root, fr, ORIGIN + Vector((float(pos[0]), float(pos[1]),
                                               float(pos[2]) if len(pos) > 2 else 0.0)))
        if "姿态" in kf:
            apply_pose(joints, fr, kf["姿态"], pose_state, root)
        # 朝向与整体翻转同写一条 rotation_euler，必须一起打帧
        key_rot(root, fr, (pose_state["root_tilt"], 0.0,
                           float(kf["朝向"]) if "朝向" in kf else last_yaw))
        last_yaw = float(kf["朝向"]) if "朝向" in kf else last_yaw
    ACTORS[nm] = {"root": root, "joints": joints, "height": float(a.get("身高", 1.72))}

PROPS: dict[str, dict] = {}
for p in CFG.get("道具", []):
    check_keys(p, SCHEMA["道具"], "[[道具]]")
    nm, shape = p["名"], p.get("形", "box")
    size = [float(x) for x in p["尺寸"]]
    loc = list(ORIGIN + Vector([float(x) for x in p.get("位置", [0, 0, 0])]))
    m = _mat_for(p.get("色", "灰"))
    if shape == "box":
        ob = box(f"P_{nm}", size, (loc[0], loc[1], loc[2] + size[2] / 2), m)
        dim_h = size[2]
    elif shape == "plane":
        ob = box(f"P_{nm}", (size[0], size[1], 0.02), loc, m)
        dim_h = 0.02
    elif shape == "cyl":
        ob = cyl(f"P_{nm}", size[0], size[1], (loc[0], loc[1], loc[2] + size[1] / 2), m)
        dim_h = size[1]
    elif shape == "sphere":
        ob = sphere(f"P_{nm}", size[0], (loc[0], loc[1], loc[2] + size[0]), m)
        dim_h = size[0] * 2
    else:
        die(f"道具「{nm}」的形＝{shape} 不认识；可用＝box/plane/cyl/sphere")
    if "朝向" in p:
        ob.rotation_euler = Euler((0, 0, math.radians(float(p["朝向"]))))
    for kf in p.get("关键帧", []):
        check_keys(kf, SCHEMA["道具.关键帧"], f"[[道具.关键帧]] of {nm}")
        t = float(kf["t"])
        LAST_KEY_T = max(LAST_KEY_T, t)
        fr = f(t)
        if "位置" in kf:
            q = list(ORIGIN + Vector([float(x) for x in kf["位置"]]))
            key_loc(ob, fr, (q[0], q[1], q[2] + dim_h / 2))
        if "朝向" in kf:
            key_rot(ob, fr, (0, 0, float(kf["朝向"])))
        if "尺寸" in kf:
            s = [float(x) for x in kf["尺寸"]]
            key_scale(ob, fr, (s[0] / size[0], s[1] / size[1] if len(s) > 1 else 1.0,
                               s[2] / size[2] if len(s) > 2 else 1.0))
    PROPS[nm] = {"ob": ob, "height": dim_h}


# ---------------------------------------------------------------- 机位解算

SUBJ = CAM.get("基准主体")
if SUBJ and SUBJ in ACTORS:
    subj_ob, subj_h = ACTORS[SUBJ]["root"], ACTORS[SUBJ]["height"]
elif SUBJ and SUBJ in PROPS:
    subj_ob, subj_h = PROPS[SUBJ]["ob"], PROPS[SUBJ]["height"]
elif ACTORS:
    first = next(iter(ACTORS.values()))
    subj_ob, subj_h = first["root"], first["height"]
elif PROPS:
    first = next(iter(PROPS.values()))
    subj_ob, subj_h = first["ob"], first["height"]
else:
    die("既无角色也无道具，没法解算机位")

lens = float(CAM.get("焦距", 35.0))
tilt = math.radians(float(CAM.get("俯角", 0.0)))
azim = math.radians(float(CAM.get("方位角", 0.0)))
frac = float(CAM.get("占画高", 0.5))
shift = float(CAM.get("横向偏移", 0.0))

cam_data = bpy.data.cameras.new("PREVIZ_CAM")
cam_data.lens = lens
cam_data.sensor_fit = "HORIZONTAL"
sensor_v = cam_data.sensor_width * (RES[1] / RES[0])
fov_v = 2 * math.atan(sensor_v / (2 * lens))

# 主体占画高 frac ⇒ 画面高 = subj_h / frac ⇒ 距离 d
dist = (subj_h / frac) / (2 * math.tan(fov_v / 2)) * float(CAM.get("距离倍数", 1.0))

# 必须按【起幅】解算：关键帧循环跑完后物体停在末帧位置，直接读会照着落幅摆机位
scene.frame_start = 1
scene.frame_end = f(TOTAL)
scene.frame_set(1)
bpy.context.view_layer.update()
sx, sy, sz = subj_ob.matrix_world.translation
aim = Vector((sx, sy, sz + subj_h * 0.5))

# 两级 rig：PIVOT 在主体上（绕它转＝环绕），RIG 在机位上（绕它转＝原地摇、平移＝推拉横移）
# tilt/azim 在手动机位分支里会被反解覆盖，故先算默认值
horiz = dist * math.cos(tilt)
cam_world = Vector((
    aim.x + horiz * math.sin(azim),
    aim.y - horiz * math.cos(azim),
    aim.z + dist * math.sin(tilt),
))
if "位置" in CAM:   # 手动机位：内景里自动解算常把相机塞进墙，需要能直接指定
    cam_world = ORIGIN + Vector([float(x) for x in CAM["位置"]])
    to_aim = aim - cam_world
    tilt = math.atan2(to_aim.z, math.hypot(to_aim.x, to_aim.y)) * -1
    azim = math.atan2(-to_aim.x, to_aim.y)   # 与基准式 cam=aim+(sin,-cos)*horiz 反解一致

cam_pivot = empty(f"{SHOT}_CAMPIVOT", aim)
cam_rig = empty(f"{SHOT}_CAMRIG", cam_world)
setpar(cam_rig, cam_pivot)
cam_rig.rotation_euler = Euler((math.pi / 2 - tilt, 0, azim))

cam = bpy.data.objects.new("PREVIZ_CAM", cam_data)
link_previz(cam)
cam.parent = cam_rig          # 局部零位：机位的位置与朝向全由 rig 持有
cam.location = Vector((0, 0, 0))
cam.rotation_euler = Euler((0, 0, 0))
scene.camera = cam
cam_data.shift_x = -shift

# 运镜：全部 K 在 rig 上，与机位解算解耦
# 锁定主体：运镜只平移不重新对准，相机一上浮/一推近主体就滑出画外。
# 打开后相机全程盯住主体（Track To 约束），代价是本镜的「上摇/下摇」失效——
# 摇镜与「盯住主体」在语义上互斥，需要摇镜的镜不要开这个。
if CAM.get("锁定主体"):
    _tgt = empty(f"{SHOT}_TRACK", (aim.x, aim.y, aim.z))
    _tgt.parent = subj_ob
    _tgt.matrix_parent_inverse = Matrix.Identity(4)
    _tgt.location = Vector((0.0, 0.0, subj_h * 0.5))   # 瞄主体中段，瞄原点＝瞄脚、头会被切
    _con = cam.constraints.new(type="TRACK_TO")
    _con.target = _tgt
    _con.track_axis = "TRACK_NEGATIVE_Z"
    _con.up_axis = "UP_Y"
    if any(m["类型"] in ("上摇", "下摇") for m in CFG.get("运镜", [])):
        die("[机位] 锁定主体 与 上摇/下摇 互斥：盯住主体时摇镜不起作用")

MOVES = CFG.get("运镜", [])
view_dir = (aim - cam_world).normalized()
right = Vector((math.cos(azim), math.sin(azim), 0.0))
# 起始俯仰偏移：t=0 时机位先偏离「对准主体」的姿态（如 shot02 起幅仰拍房梁），
# 再由第一段摇镜摇回来。正＝起幅更仰。
if "起始俯仰偏移" in CAM:
    cam_rig.rotation_euler = Euler((cam_rig.rotation_euler.x
                                    + math.radians(float(CAM["起始俯仰偏移"])),
                                    cam_rig.rotation_euler.y, cam_rig.rotation_euler.z))
loc_now, rot_now = cam_rig.location.copy(), cam_rig.rotation_euler.copy()
piv_now = cam_pivot.rotation_euler.copy()
# 多段运镜先合成再打帧：若干段同时起跑（推近＋升降＋上摇）时，逐段各打各的
# 起止帧会互相踩掉起始关键帧——必须把它们合成同一条曲线，按时间边界统一打。
deltas = []      # (t0, t1, dloc, drot) 作用在 RIG 上
orbits = []      # (t0, t1, ddeg)      作用在 PIVOT 上
for mv in MOVES:
    check_keys(mv, SCHEMA["运镜"], "[[运镜]]")
    kind, t0, t1, amt = mv["类型"], float(mv["起"]), float(mv["止"]), float(mv["量"])
    LAST_KEY_T = max(LAST_KEY_T, t1)
    if kind == "环绕":
        orbits.append((t0, t1, amt))
        continue
    dl, dr = Vector((0, 0, 0)), Vector((0, 0, 0))
    if kind in ("推近", "后拉"):
        dl = view_dir * (amt if kind == "推近" else -amt)
    elif kind == "横移":
        dl = right * amt
    elif kind == "升降":
        dl = Vector((0, 0, amt))
    elif kind in ("上摇", "下摇"):
        dr = Vector((math.radians(amt if kind == "上摇" else -amt), 0, 0))
    else:
        die(f"[[运镜]] 类型「{kind}」不认识；可用＝推近/后拉/横移/升降/上摇/下摇/环绕")
    deltas.append((t0, t1, dl, dr))


def _ramp(t, t0, t1):
    if t <= t0:
        return 0.0
    if t >= t1:
        return 1.0
    return (t - t0) / (t1 - t0) if t1 > t0 else 1.0


if deltas:
    marks = sorted({0.0, TOTAL} | {t for d in deltas for t in (d[0], d[1])})
    for t in marks:
        dl = Vector((0, 0, 0))
        dr = Vector((0, 0, 0))
        for t0, t1, l, r in deltas:
            k = _ramp(t, t0, t1)
            dl = dl + l * k
            dr = dr + r * k
        key_loc(cam_rig, f(t), loc_now + dl)
        key_rot(cam_rig, f(t), [math.degrees(a) for a in
                                (rot_now.x + dr.x, rot_now.y + dr.y, rot_now.z + dr.z)])

if orbits:
    marks = sorted({0.0, TOTAL} | {t for o in orbits for t in (o[0], o[1])})
    for t in marks:
        dz = sum(amt * _ramp(t, t0, t1) for t0, t1, amt in orbits)
        key_rot(cam_pivot, f(t), (math.degrees(piv_now.x), math.degrees(piv_now.y),
                                  math.degrees(piv_now.z) + dz))


# ---------------------------------------------------------------- 自动切墙
# 内景 previz 的老问题：相机与主体之间隔着墙/天花板/屋顶。previz 师傅的做法是
# 手动把挡镜的那面墙藏掉（cutaway）。这里沿 相机→主体 射线自动做：命中谁藏谁，
# 直到通路打开。只藏场景主档的件，PREVIZ 集合里的 proxy 永不隐藏。
if G.get("场景") and CAM.get("切墙", True):
    ours = {o.name for o in PREVIZ.objects}
    deps = bpy.context.evaluated_depsgraph_get()
    seg = aim - cam_world
    hidden = []
    for _ in range(24):
        bpy.context.view_layer.update()
        deps = bpy.context.evaluated_depsgraph_get()
        hit, loc, nrm, idx, ob, mw = scene.ray_cast(deps, cam_world, seg.normalized(),
                                                    distance=seg.length * 0.97)
        if not hit or ob is None or ob.name in ours:
            break
        ob.hide_render = True
        ob.hide_viewport = True
        hidden.append(ob.name)
    if hidden:
        print(f"  切墙：隐藏 {len(hidden)} 件挡镜场景物 → {', '.join(hidden[:6])}"
              + (" …" if len(hidden) > 6 else ""))


# ---------------------------------------------------------------- 输出设置

scene.frame_start = 1
scene.frame_end = f(TOTAL)
scene.render.fps = FPS
scene.render.resolution_x, scene.render.resolution_y = int(RES[0]), int(RES[1])
scene.render.resolution_percentage = 100
try:
    scene.render.engine = "BLENDER_EEVEE_NEXT"
except TypeError:
    scene.render.engine = "BLENDER_EEVEE"
if hasattr(scene.render.image_settings, "media_type"):
    scene.render.image_settings.media_type = "VIDEO"   # Blender 5.x：先切媒体类型才有 FFMPEG
scene.render.image_settings.file_format = "FFMPEG"
scene.render.ffmpeg.format = "MPEG4"
scene.render.ffmpeg.codec = "H264"
scene.render.ffmpeg.constant_rate_factor = "MEDIUM"
scene.render.filepath = str(OUT_DIR / f"{SHOT}_previz.mp4")

# 素模化：把场景主档的材质整体换成中性灰。
# 两个理由：① 场景是按成片调色做的（s11 是月夜、s2 是夜戏），照搬渲出来是一片黑，
# 而 previz 要读的是形状与站位；② rule 12.16 明令 previz 不得携带美术——
# 素模化从源头保证它连"像成片"的机会都没有，模型也就无从照抄。
if scene_name and G.get("素模场景", True):
    clay = mat("M_CLAY", (0.52, 0.52, 0.50))
    ours = {o.name for o in PREVIZ.objects}
    n_clay = 0
    for ob in bpy.data.objects:
        if ob.type != "MESH" or ob.name in ours:
            continue
        ob.data.materials.clear()
        ob.data.materials.append(clay)
        n_clay += 1
    print(f"  素模化：{n_clay} 件场景物换成中性灰")
    _w = bpy.data.worlds.new("PREVIZ_WORLD")   # 整个换掉，不去改夜景世界的节点树
    _w.use_nodes = True
    _wb = _w.node_tree.nodes.get("Background")
    if _wb is not None:
        _wb.inputs[0].default_value = (0.42, 0.45, 0.50, 1.0)
        _wb.inputs[1].default_value = 1.0
    scene.world = _w

# previz 用中性照明，不继承场景主档的灯光。
# s11 是月夜场景、s2 是夜戏——沿用它们的灯，previz 渲出来是一片黑，
# 而 previz 要读的是形状与站位，不是气氛。气氛归 Seedance。
for _ob in list(bpy.data.objects):
    if _ob.type == "LIGHT" and _ob.name != "PREVIZ_SUN":
        _ob.hide_render = True
        _ob.hide_viewport = True
sun = bpy.data.lights.new("PREVIZ_SUN", type="SUN")
sun.energy = 4.0
sun_ob = bpy.data.objects.new("PREVIZ_SUN", sun)
link_previz(sun_ob)
sun_ob.rotation_euler = Euler((math.radians(48), 0, math.radians(35)))
sun2 = bpy.data.lights.new("PREVIZ_FILL", type="SUN")   # 补光，压暗部
sun2.energy = 1.6
fill_ob = bpy.data.objects.new("PREVIZ_FILL", sun2)
link_previz(fill_ob)
fill_ob.rotation_euler = Euler((math.radians(65), 0, math.radians(-140)))
if scene.world is None or not scene.world.name.startswith("PREVIZ"):
    _w = bpy.data.worlds.new("PREVIZ_WORLD")
    _w.use_nodes = True
    _bg = _w.node_tree.nodes.get("Background")
    if _bg is not None:
        _bg.inputs[0].default_value = (0.42, 0.45, 0.50, 1.0)
        _bg.inputs[1].default_value = 1.0
    scene.world = _w

blend_out = OUT_DIR / f"{SHOT}_previz.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(blend_out))


# ---------------------------------------------------------------- 自检报告

print("\n" + "=" * 68)
print(f"[previz] {SHOT}  {TOTAL}s @ {FPS}fps = {scene.frame_end} 帧  {RES[0]}x{RES[1]}")
print("=" * 68)

problems = []

# ① 末关键帧不得越界（changelog 046 的静默截断 bug，在这里变成硬报错）
if LAST_KEY_T > TOTAL + 1e-6:
    problems.append(f"末关键帧 {LAST_KEY_T}s > total_sec {TOTAL}s —— 超出部分会被静默截掉")
print(f"  末关键帧 {LAST_KEY_T:.2f}s / 总长 {TOTAL:.2f}s "
      f"{'✗ 越界' if LAST_KEY_T > TOTAL + 1e-6 else '✓'}")

# ② 实测主体占画比（rule 12.16 要求用 world_to_camera_view 核验，不靠估）
def occupancy(ob, height, frame):
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    base = ob.matrix_world.translation
    lo = world_to_camera_view(scene, cam, Vector((base.x, base.y, base.z)))
    hi = world_to_camera_view(scene, cam, Vector((base.x, base.y, base.z + height)))
    return abs(hi.y - lo.y), lo, hi

occ, lo, hi = occupancy(subj_ob, subj_h, 1)
# 起幅带摇角偏移时（如 shot02 仰拍房梁起幅），主体本就不在起幅画面里 → 判落幅
judge_at_end = "起始俯仰偏移" in CAM
print(f"  基准主体「{SUBJ or '(自动)'}」起幅占画高 {occ * 100:.1f}%（目标 {frac * 100:.0f}%）"
      f"  画面横向 {lo.x:.2f}")
occ_j = occupancy(subj_ob, subj_h, scene.frame_end)[0] if judge_at_end else occ
if abs(occ_j - frac) > 0.08:
    # 自动解算时占画比是硬约束；手动指定机位时作者已经自己定了距离，只报不拦
    msg = f"占画比实测 {occ_j:.2f} 与目标 {frac:.2f} 偏差过大"
    (print(f"  [warning] {msg}（手动机位）") if "位置" in CAM else problems.append(msg))
if not judge_at_end and not (0.0 <= lo.x <= 1.0):
    problems.append("基准主体起幅不在画面内（横向偏移过大？）")

occ_end, _, _ = occupancy(subj_ob, subj_h, scene.frame_end)
print(f"  基准主体落幅占画高 {occ_end * 100:.1f}%")

# ③ 每个道具起幅是否在画内——「庙被顶出画外」那类几何冲突要在这里暴露
for nm, p in PROPS.items():
    scene.frame_set(1)
    bpy.context.view_layer.update()
    v = world_to_camera_view(scene, cam, p["ob"].matrix_world.translation)
    inside = 0.0 <= v.x <= 1.0 and 0.0 <= v.y <= 1.0 and v.z > 0
    print(f"  道具「{nm}」起幅 {'画内' if inside else '画外'}  (x={v.x:.2f}, y={v.y:.2f})")

scene.frame_set(1)
print(f"  角色 {len(ACTORS)} / 道具 {len(PROPS)} / 运镜 {len(MOVES)} 段")
print(f"  写出 {blend_out.name}")

if problems:
    print("\n  [blocker]")
    for p in problems:
        print(f"    ✗ {p}")
    print()
    sys.exit(2)
print("  自检通过 ✓\n")

if DO_RENDER:
    bpy.ops.render.render(animation=True)
    print(f"[previz] 渲毕 → {scene.render.filepath}")
