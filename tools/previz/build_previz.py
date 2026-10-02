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

import json
import math
import re
import shutil
import sys
import tomllib
from pathlib import Path

import bpy
from mathutils import Euler, Matrix, Vector
from bpy_extras.object_utils import world_to_camera_view

sys.path.insert(0, str(Path(__file__).resolve().parent))
from curves import mono_hermite  # noqa: E402  与航线生成端同一份插值
import seedance_ref  # noqa: E402  Seedance 参考视频的上下限（像素 / 帧率 / 单条时长）唯一出处
from planschema import BODY_HITS, HIT_OBJ, PREVIZ_STAMP, STILLS_STAMP, render_inputs  # noqa: E402

# ---------------------------------------------------------------- 配置 schema

# 键名白名单：拼错直接报错，绝不静默忽略（沿用 shot12 previz 的既定规则）
SCHEMA = {
    "全局": {"shot", "fps", "total_sec", "场景", "分辨率", "地面", "原点偏移", "贴地", "素模场景", "项目", "地形", "参考截止", "绿幕",
             "后处理"},
    "机位": {"俯角", "焦距", "基准主体", "占画高", "横向偏移", "距离倍数", "方位角", "位置", "切墙", "起始俯仰偏移", "锁定主体",
             "路点"},
    # 路点机位（2026-09-26）：overhead.toml 的 [[camera]] 一一对应——机位在世界里走一条路、中途可硬切。
    # 有路点时不解算、不运镜：位置与瞄点逐帧由路点插值，`切 = true` 的路点在它那一刻跳过去。
    "机位.路点": {"t", "位置", "瞄", "焦距", "切"},
    "运镜": {"类型", "起", "止", "量"},
    # 模型 ＝ Cascadeur 导出的烘焙动画 FBX（相对本配置；动画已带世界位移，模型原点 ＝ 它的 (0,0) 落在本镜哪里）；
    # 四足 ＝ 用四足代理（狼等），身高读作肩高（follow-up 032）
    # 持物 ＝ 手里 / 肩上拿的长物件（follow-up 042：shot04 的锤只在文字里，出片锤子悬在肩上没手扶）
    "角色": {"名", "色", "身高", "关键帧", "模型", "模型原点", "模型帧率", "四足", "持物", "入场", "离场"},   # 入场 / 离场：之前 / 之后藏起来（钻进洞里）
    "角色.持物": {"件", "姿", "长", "起", "止", "形"},  # 起 / 止：这种拿法的时段（秒），缺省整镜；形：盾的外形（圆 / 竖长）
    # 命中（overhead [[hit]] 抄过来）：t 那一刻「物件」要贴到「目标」身上；远程（扔光）不查
    "命中": {"t", "谁", "物件", "目标", "远程", "部位", "友方"},   # 部位：打在目标身上的哪件东西（「背盾」→ 量「{目标}_背盾」）
    "角色.关键帧": {"t", "位置", "朝向", "姿态"},
    "道具": {"名", "形", "尺寸", "位置", "色", "朝向", "关键帧", "档"},
    "道具.关键帧": {"t", "位置", "朝向", "尺寸"},
    # 施法（follow-up 065）：生成器按技能卡算好的阶段窗 [[阶段名, 起, 止], …]；钩子的光代理用 cast_curve() 取，不手抄时刻
    "施法": {"技能", "谁", "目标", "阶段"},
}

COLORS = {
    "绿": (0.10, 0.75, 0.15), "蓝": (0.10, 0.30, 0.90), "红": (0.85, 0.10, 0.10),
    "青": (0.10, 0.80, 0.80), "黄": (0.90, 0.80, 0.10), "紫": (0.55, 0.15, 0.85),
    "橙": (0.95, 0.45, 0.05), "白": (0.90, 0.90, 0.90), "灰": (0.35, 0.35, 0.38), "褐": (0.40, 0.26, 0.13),
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
    "伸左手": {"shoulderL": (-80, 0, 0), "elbowL": (-10, 0, 0)},     # 左手按在前面那人的背上（shot11 盾后施法）
    "按左手": {"shoulderL": (-55, 0, 0), "elbowL": (-10, 0, 0)},     # 左手往前下按在对面那人垂着的前臂上（shot13 祝福）
    "举手R": {"shoulderR": (-170, 0, 0), "elbowR": (-5, 0, 0)},   # 圣光术放出去的那一下：一只手笔直举过头顶（w25 wow.lightvfx.003）
    "举手L": {"shoulderL": (-170, 0, 0), "elbowL": (-5, 0, 0)},
    "双手前伸": {"shoulderL": (-85, 0, 0), "elbowL": (-8, 0, 0),
                 "shoulderR": (-85, 0, 0), "elbowR": (-8, 0, 0)},
    "端物": {"shoulderL": (-55, 0, -12), "elbowL": (-70, 0, 0),
             "shoulderR": (-55, 0, 12), "elbowR": (-70, 0, 0)},
    # 圣光术蓄光两段（w25 hl01–hl03，follow-up 065）：起手两手掌心朝上在腰侧，随即左手抬到头侧、右手留在腰侧
    "托光低": {"shoulderL": (-30, 0, -12), "elbowL": (-60, 0, 0),
               "shoulderR": (-30, 0, 12), "elbowR": (-60, 0, 0)},
    "托光L高": {"shoulderL": (-95, 0, -12), "elbowL": (-85, 0, 0),
                "shoulderR": (-30, 0, 12), "elbowR": (-60, 0, 0)},
    "抬头": {"head": (-28, 0, 0)},
    "低头": {"head": (30, 0, 0)},
    "俯身": {"pelvis": (45, 0, 0), "head": (-25, 0, 0),
             "shoulderL": (-25, 0, 0), "shoulderR": (-25, 0, 0)},
    "半躬": {"pelvis": (28, 0, 0), "head": (-15, 0, 0)},
    "蹲": {"hipL": (-85, 0, 0), "kneeL": (105, 0, 0), "ankleL": (-20, 0, 0),
           "hipR": (-85, 0, 0), "kneeR": (105, 0, 0), "ankleR": (-20, 0, 0),
           "pelvis": (18, 0, 0)},
    # 049 G10：旧版两条大腿都朝前平伸、小腿朝下，最低点是脚——按最低点贴地后膝盖离地 0.4 m，人像坐在隐形凳子上
    "单膝跪": {"hipL": (-90, 0, 0), "kneeL": (90, 0, 0),            # 左腿在前：大腿平、小腿竖、脚踩地
               "hipR": (5, 0, 0), "kneeR": (90, 0, 0), "pelvis": (5, 0, 0)},   # 右腿在后：大腿竖、膝盖着地
    "跪": {"hipL": (-5, 0, 0), "kneeL": (92, 0, 0),
           "hipR": (-5, 0, 0), "kneeR": (92, 0, 0), "pelvis": (5, 0, 0)},     # 直身双膝跪：大腿竖、小腿平贴地
    "扑跪": {"pelvis": (70, 0, 0), "hipL": (-70, 0, 0), "kneeL": (92, 0, 0), "hipR": (-70, 0, 0), "kneeR": (92, 0, 0),
             "shoulderL": (-72, 0, 0), "shoulderR": (-72, 0, 0), "head": (-35, 0, 0)},   # 往前扑倒：双膝双手撑地
    "坐": {"hipL": (-90, 0, 0), "kneeL": (88, 0, 0),
           "hipR": (-90, 0, 0), "kneeR": (88, 0, 0)},
    # 049（S20 加瑞克坐在劈柴墩上）：人偶只贴地形、不贴道具，人在墩子占地里就嵌进墩子（矮的看着像立在顶上）。
    # 坐墩＝骨盆落在身下那件静态 [[道具]]（没有就地面）的顶面，大腿平、小腿垂到地上；站高＝站在它顶上（S11 矿堆上那只）
    "坐墩": {"hipL": (-90, 0, 0), "kneeL": (90, 0, 0),
             "hipR": (-90, 0, 0), "kneeR": (90, 0, 0)},
    "站高": {},
    "跌坐": {"hipL": (-85, 0, 12), "kneeL": (15, 0, 0),              # 屁股着地、两腿朝前伸（旧版膝弯 70°，脚着地、屁股悬空）
             "hipR": (-85, 0, -12), "kneeR": (15, 0, 0), "pelvis": (-12, 0, 0)},
    "躺": {"pelvis": (-88, 0, 0)},
    "踏剑": {"hipL": (-18, 0, 0), "kneeL": (25, 0, 0),
             "hipR": (-8, 0, 0), "kneeR": (12, 0, 0),
             "shoulderL": (0, 0, -35), "shoulderR": (0, 0, 35)},
    "行走": {"hipL": (-25, 0, 0), "kneeL": (15, 0, 0), "hipR": (22, 0, 0),
             "shoulderL": (18, 0, 0), "shoulderR": (-18, 0, 0)},
    "背对": {},
    # 持物姿态：只动持物那只手，跟着 [[角色.持物]] 在每个关键帧叠上去（走路的腿照走）
    "扛肩R": {"shoulderR": (-30, 0, 0), "elbowR": (-130, 0, 0)},
    "双手低握": {"shoulderL": (-35, 0, -15), "elbowL": (-45, 0, 0), "shoulderR": (-35, 0, 15), "elbowR": (-45, 0, 0)},
    "靠腿": {},
    # follow-up 047 G5：盾与单手家伙（shot11 previz 里杜克没盾、矿工手里没镐，命中检查就量身体混过去了）
    "臂盾L": {"shoulderL": (-50, 0, -25), "elbowL": (-70, 0, 0)},
    "背盾": {},
    "单手握R": {"shoulderR": (-35, 0, 10), "elbowR": (-50, 0, 0)},
    # 出手那一下（follow-up 047 G5：色块人偶的兵器是挂死的，锤头在身侧下方，命中检查量出来差半米——只有在命中前后
    # 各 0.2 s 切到这两个姿势，锤头 / 斧头才真的伸到身前一米处）
    "前砸": {"shoulderL": (-80, 0, -10), "elbowL": (-10, 0, 0), "shoulderR": (-80, 0, 10), "elbowR": (-10, 0, 0)},
    "前劈R": {"shoulderR": (-80, 0, 0), "elbowR": (-10, 0, 0)},
    # 049（S20）：斧柄往外一磕格开锤头、反腿侧踹、跪下护人时钢盾垂在身侧
    "外磕R": {"shoulderR": (-60, 0, 40), "elbowR": (-45, 0, 0)},
    "侧踹R": {"hipR": (-75, -25, 0), "kneeR": (10, 0, 0)},
    "垂盾L": {"shoulderL": (-10, 0, -10), "elbowL": (-15, 0, 0)},
}
CARRY_POSES = {"扛肩R", "双手低握", "靠腿", "臂盾L", "背盾", "垂盾L", "单手握R", "外磕R", "前砸", "前劈R"}
LEAN_TOL = 20.0          # 自检：Cascadeur 烘出来的躯干前倾与编排相差超过这个角度（°）即 blocker
HIT_TOL = 0.35           # 自检：命中那一刻物件离目标身体超过这个距离（m）即 blocker

JOINTS = ("pelvis", "head", "shoulderL", "shoulderR", "elbowL", "elbowR",
          "hipL", "hipR", "kneeL", "kneeR", "ankleL", "ankleR")

# 基础姿态定义全身；修饰姿态只动它点名的关节，叠在当前基础姿态之上并跨关键帧保持。
# 没这个区分的话，"抬头" 会把 "跌坐" 的腿一起清零——人物会当场站起来。
# 配置里可写 "跌坐+抬头" 显式组合；只写修饰姿态则沿用上一个基础姿态。
BASE_POSES = {"站", "站定", "站高", "坐", "坐墩", "跌坐", "跪", "单膝跪", "扑跪", "蹲", "躺", "行走", "踏剑", "背对"}

# 少数姿态光靠关节摆不出来，要整体翻转躯干（躺＝整个人放平，不是坐着往后仰）
ROOT_TILT = {"躺": -78.0}
# 弯腿姿态只转关节、不降骨盆：不把最低点按回地面，跌坐 / 蹲 / 跪的人就悬在半空（follow-up 035 shot19 静帧）。
# 这两种本来就不贴地：坐＝坐在东西上（石头、台阶），踏剑＝站在飞剑上。
OFF_GROUND = {"坐", "踏剑"}
FLOAT_MAX = 0.15          # 自检：人偶最低点离地超过这个高度（米）即 blocker
# 049 G10：按最低点贴地只保证「有一处着地」，着地的是不是该着地的那处它不管（跌坐的人脚着地、屁股悬空照样过）。
# 每种底姿态点名该着地的关节：（关节, 贴地时关节中心离地多高——None＝照旧按最低点贴地, 自检上限）；左右取低的那只
POSE_CONTACT = {"站": ("ankle", None, 0.15), "站定": ("ankle", None, 0.15), "站高": ("ankle", None, 0.15), "蹲": ("ankle", None, 0.15),
                "跌坐": ("pelvis", 0.10, 0.25), "跪": ("knee", 0.05, 0.12), "单膝跪": ("knee", 0.05, 0.12),
                "扑跪": ("knee", 0.05, 0.15), "躺": ("pelvis", 0.12, 0.3), "坐墩": ("pelvis", 0.10, 0.25)}
ON_TOP = {"坐墩", "站高"}   # 着地面＝身下那件静态道具的顶面（seat_z），不是地形；szzl 引擎按 AST 读这张表
WALK_STEP_M = 0.7         # 052：人偶一步的步长（米）；走路时两腿按走过的距离交替摆，不再一个迈步姿势整体平移
WALK_MIN_MPS = 0.35       # 根位置每秒挪得比它快才算在走
WALK_HIP, WALK_KNEE = 26.0, 40.0   # 大腿前后摆幅、后腿屈膝（°）
ROOT_DEV_MAX = 0.3        # 自检：关键时刻人物根（Cascadeur 体取骨盆）的水平位置偏离配置超过这个距离（米）即 blocker
SIT_PELVIS_M = 0.45       # Cascadeur 体骨盆离地低于它＝坐在地上：站位取骨盆，不取两脚中点（腿往前伸，脚在屁股前面 0.7 m）


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
# --stills[=t1,t2,…]：不渲 MP4，只在这些秒数（缺省按机位切点 / 段中 / 每 3 秒）出半分辨率静帧到 previz/frames/stills/，
# 几十秒看完一镜的站位、朝向与遮挡；看过再渲整条（follow-up 032 复盘：shot01 三轮返工都是渲完整条才发现）。
STILLS = next((a for a in argv if a.startswith("--stills")), None)
if not CFG_PATH.is_file():
    die(f"配置不存在：{CFG_PATH}")

CFG = tomllib.loads(CFG_PATH.read_text(encoding="utf-8"))
G = CFG.get("全局", {})
check_keys(G, SCHEMA["全局"], "[全局]")
CAM = CFG.get("机位", {})
check_keys(CAM, SCHEMA["机位"], "[机位]")
CASTS = CFG.get("施法", [])
for _c in CASTS:
    check_keys(_c, SCHEMA["施法"], "[[施法]]")


def cast_windows(who: str, phases: tuple, key: str | None = None) -> list:
    """[[施法]] 里 who 施法（只看某张卡时写 key）这几个阶段的时间窗 [(起, 止)]，相邻的并成一段。"""
    wins = sorted((float(a), float(b)) for c in CASTS if c["谁"] == who and key in (None, c["技能"])
                  for ph, a, b in c["阶段"] if ph in phases)
    merged: list = []
    for a, b in wins:
        if merged and a <= merged[-1][1] + 1e-6:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    return merged


def cast_curve(who: str, phases: tuple, peak: float = 1.0, ramp: float = 0.1, key: str | None = None) -> list:
    """钩子的光代理时刻表 [(秒, 值)]：这几个阶段里为 peak，前后各 ramp 秒线性起落。"""
    keys = [(0.0, 0.0)]
    for a, b in cast_windows(who, phases, key):
        keys += [(max(0.0, a - ramp), 0.0), (a, peak), (b, peak), (b + ramp, 0.0)]
    return keys

SHOT = G.get("shot") or CFG_PATH.parent.parent.name
FPS = int(G.get("fps", 24))
TOTAL = float(G["total_sec"]) if "total_sec" in G else die("[全局] 缺 total_sec")
RES = G.get("分辨率", [960, 540])
OUT_DIR = CFG_PATH.parent
for _msg in seedance_ref.check(FPS, (int(RES[0]), int(RES[1]))):
    die(_msg + "（previz 要上传给 Seedance 当参考，下限不过就是废片，ai_video.md rule 24）")
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
    # rule: 场景主档按 [全局].项目 解析；缺省 xianjian_yi_mv（向后兼容既有 shot 配置）
    _proj = G.get("项目", "xianjian_yi_mv")
    # 场景 .blend 住在 `scenes/{name}/_blender/`——它是 blender 侧产物，
    # 与出图用的主体目录分开放（ai_video.md rule 4e）。旧布局（放在场景根）作兜底。
    # 场景 可以是 scenes/ 下的嵌套路径（rule 4e 2026-09-22：大陆/区/bg{N}_主体）；
    # 主档名取叶子目录名，或 bg 主体的 `bg{N}.blend`（build_scene.py 的产物名）
    _scene_dir = REPO / "ai_videos" / _proj / "2_世界观人设" / "scenes" / scene_name
    _leaf = Path(scene_name).name
    _cands = [_scene_dir / "_blender" / f"{_leaf}.blend", _scene_dir / "_blender" / f"{_leaf.split('_')[0]}.blend",
              _scene_dir / f"{_leaf}.blend"]
    src = next((c for c in _cands if c.is_file()), _cands[0])
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

# 逐点地形（2026-09-26，shengji bg20 隘口：墙外土路南低北高约 2m）：[全局].地形 ＝ 场景里算作地面的物体名片段。
# 设了它，角色 / 道具的 z 与路点机位的高度都按「离地」解释——overhead 的 h 本来就是离地高度。
# 只对名字或所在集合名带这些片段的网格打射线（树冠、门洞过梁、贴地道具一概不算），多件取最高。
GROUND = tuple(G.get("地形", ()))


_GROUND_TREES: list | None = None


def _ground_trees() -> list:
    """地面件的 BVH（名字或所在集合名带 地形 片段的网格）。只对它们打射线：
    贴地的道具底面与地面共面，逐个穿过去的射线会从缝里漏过地面（shot05 的石头、bg19 的柴垛）。"""
    global _GROUND_TREES
    if _GROUND_TREES is None:
        from mathutils.bvhtree import BVHTree
        deps = bpy.context.evaluated_depsgraph_get()
        _GROUND_TREES = [(ob, ob.matrix_world.copy(), BVHTree.FromObject(ob, deps))
                         for ob in scene.objects
                         if ob.type == "MESH" and PREVIZ.objects.get(ob.name) is None
                         and any(g in ob.name or any(g in c.name for c in ob.users_collection) for g in GROUND)]
        if not _GROUND_TREES:
            die(f"场景里没有名字或集合名带 地形={list(GROUND)} 的网格")
    return _GROUND_TREES


def _ground_hit(x: float, y: float) -> float | None:
    best = None
    for ob, mw, tree in _ground_trees():
        inv = mw.inverted()
        o, d = inv @ Vector((x, y, 300.0)), (inv.to_3x3() @ Vector((0, 0, -1))).normalized()
        loc = tree.ray_cast(o, d)[0]
        if loc is not None:
            z = (mw @ loc).z
            best = z if best is None else max(best, z)
    return best


_OFF_GROUND: set = set()


def ground_z(x: float, y: float) -> float:
    if not GROUND:
        return ORIGIN.z
    z = _ground_hit(x, y)
    if z is not None:
        return z
    # 场地外（overhead 允许机位在场地边外 5 m 内）：按最近的地面边缘取高度
    pts = [mw @ Vector(c) for ob, mw, _t in _ground_trees() for c in ob.bound_box]
    cx = min(max(x, min(v.x for v in pts) + 0.05), max(v.x for v in pts) - 0.05)
    cy = min(max(y, min(v.y for v in pts) + 0.05), max(v.y for v in pts) - 0.05)
    z = _ground_hit(cx, cy)
    if z is None or math.hypot(cx - x, cy - y) > 6.0:
        die(f"({x:.1f}, {y:.1f}) 脚下没有地面：地形={list(GROUND)} 的件都不覆盖这一点，离场地边也超过 6 m")
    if not _OFF_GROUND:
        print(f"  [warning] ({x:.1f}, {y:.1f}) 在场地外，按最近的场地边缘 ({cx:.1f}, {cy:.1f}) 取地面高度")
    _OFF_GROUND.add((round(x), round(y)))
    return z


def seat_z(x: float, y: float) -> float:
    """坐墩 / 站高的着地面：(x, y) 落在哪个静态方盒 [[道具]] 的占地里就取它的顶面，否则取地面。
    人偶贴地时道具还没建出来，按配置算（位置 / 尺寸 / 朝向与建道具那一段同约定）。"""
    z = ground_z(x, y)
    for p in CFG.get("道具", []):
        if p.get("关键帧") or p.get("形", "box") != "box":
            continue
        pos = [float(v) for v in p.get("位置", [0, 0, 0])]
        px, py = ORIGIN.x + pos[0], ORIGIN.y + pos[1]
        w, d, h = (float(v) for v in p["尺寸"][:3])
        r = math.radians(float(p.get("朝向", 0.0)))
        u = (x - px) * math.cos(r) + (y - py) * math.sin(r)
        v = -(x - px) * math.sin(r) + (y - py) * math.cos(r)
        if abs(u) <= w / 2 and abs(v) <= d / 2:
            z = max(z, ground_z(px, py) + (pos[2] if len(pos) > 2 else 0.0) + h)
    return z


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
    if G.get("绿幕"):        # 绿幕小人偶 previz（follow-up 085）：纯绿地面 + 纯绿世界，没有任何场景
        MATS["绿幕"] = mat("M_GREENSCREEN", (0.0, 0.55, 0.12))
        box("GROUND", (200, 200, 0.02), tuple(ORIGIN + Vector((0, 0, -0.01))), MATS["绿幕"])
        _gw = bpy.data.worlds.new("PREVIZ_GREEN")
        _gw.use_nodes = True
        _gb = _gw.node_tree.nodes.get("Background")
        if _gb is not None:
            _gb.inputs[0].default_value = (0.0, 0.55, 0.12, 1.0)
            _gb.inputs[1].default_value = 1.0
        scene.world = _gw
        bpy.ops.mesh.primitive_uv_sphere_add(radius=160, location=tuple(ORIGIN))     # 包住整个场地的绿幕穹顶（世界色在 AgX 下会发灰）
        _dome = bpy.context.active_object
        _dome.name = "GS_DOME"
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.flip_normals()
        bpy.ops.object.mode_set(mode="OBJECT")
        _dome.data.materials.append(mat("M_GS_DOME", (0.0, 0.55, 0.12), 1.0))
    else:
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


def make_carry(name: str, j: dict, h: float, c: dict, root=None, idx: int = 0) -> None:
    """长柄锤的三种拿法（与同名手臂姿态配套）。名字按「{人}_锤柄 / {人}_锤头」起（同一镜多段时第二段起加序号）：
    可见性表把它归给主人，命中检查按这个名字找锤头。有「起 / 止」时只在那一段出现（follow-up 043）。
    扛肩R：右手握在右肩前一掌处，锤柄往后上斜搭过右肩、锤头在肩后；
    双手低握：两手一前一后握在腰前，锤柄斜过身前、锤头在左下；靠腿：锤头朝下立在右脚边，柄斜靠右腿，手不碰。"""
    sfx = "" if idx == 0 else str(idx + 1)
    pose = c["姿"]
    item = str(c.get("件", "锤"))
    if "盾" in item:
        _segment(make_shield(name, j, h, c, item, sfx), c)
        return
    L = float(c.get("长", 1.2))
    if pose in ("单手握R", "外磕R"):        # 单手家伙（镐 / 短斧）：右手握在胯前，柄朝前上斜 30°（外磕＝同一握法把柄往外一横）
        par, grip, back = j["pelvis"], Vector((-0.13 * h, -0.14 * h, 0.02 * h)), 0.1
        d, rot = Vector((0.0, -0.5, 0.866)), (math.radians(30), 0.0, 0.0)
    elif pose in ("前砸", "前劈R"):   # 出手：握在胸前，柄朝前下斜 20°，头在身前一米上下
        par, grip, back = j["pelvis"], Vector((0.0 if pose == "前砸" else -0.08 * h, -0.25 * h, 0.25 * h)), 0.1
        d, rot = Vector((0.0, -0.94, -0.34)), (math.radians(110), 0.0, 0.0)
    elif pose == "扛肩R":
        par, grip, back = j["pelvis"], Vector((-0.105 * h, -0.128 * h, 0.296 * h)), 0.15
        d, rot = Vector((0.0, math.cos(math.radians(25)), math.sin(math.radians(25)))), (math.radians(-65), 0.0, 0.0)
    elif pose == "双手低握":
        par, grip, back = j["pelvis"], Vector((0.0, -0.239 * h, 0.13 * h)), 0.35
        d, rot = Vector((0.894, 0.0, -0.447)), (0.0, math.radians(116.6), 0.0)
    else:   # 靠腿：挂在人的根上（不跟骨盆前倾）
        par, grip, back = root, Vector((-0.13 * h, -0.05 * h, 0.05)), 0.0
        d, rot = Vector((0.07, 0.05, 0.996)).normalized(), (math.radians(-3), math.radians(4), 0.0)
    shaft = cyl(f"{name}_{item}柄{sfx}", 0.018, L, (0, 0, 0), _mat_for("褐"))
    shaft.rotation_euler = Euler(rot)
    head = box(f"{name}_{HIT_OBJ.get(item[:1], item + '头')}{sfx}", (0.10, 0.16, 0.10), (0, 0, 0), _mat_for("深灰"))
    head.rotation_euler = Euler(rot)
    if pose == "靠腿":            # 锤头在下、柄朝上
        attach(head, par, tuple(grip))
        attach(shaft, par, tuple(grip + d * (L / 2)))
    else:
        attach(shaft, par, tuple(grip + d * (L / 2 - back)))
        attach(head, par, tuple(grip + d * (L - back - 0.05)))
    _segment((shaft, head), c)


def make_shield(name: str, j: dict, h: float, c: dict, item: str, sfx: str) -> tuple:
    """盾（follow-up 047 G5）：臂盾L＝挽在左前臂、挡在胸前偏左，盾面朝前；背盾＝背在背后，盾面朝后。
    形＝圆（木圆盾，直径取「长」缺省 0.7 m）/ 竖长（钢盾 0.72 × 1.15 m）。名字「{人}_{件}」——命中检查按它找盾。"""
    shape = c.get("形", "圆")
    nm = f"{name}_{item}{sfx}"
    if shape == "圆":
        ob = cyl(nm, float(c.get("长", 0.7)) / 2, 0.04, (0, 0, 0), _mat_for("褐"))
        ob.rotation_euler = Euler((math.radians(90), 0.0, 0.0))
    elif shape == "竖长":
        ob = box(nm, (0.72, 0.03, 1.15), (0, 0, 0), _mat_for("灰"))      # 钢盾 0.72 × 1.15 m（用户 2026-10-01：原 0.5 × 0.8 太小）
    else:
        die(f"「{nm}」盾的形「{shape}」不认识；可用＝圆 / 竖长")
    if c["姿"] == "垂盾L":       # 垂在身体左侧：盾面朝左、下沿离地一拳（049 S20 落幅）
        ob.rotation_euler = Euler((ob.rotation_euler.x, ob.rotation_euler.y, math.radians(90)))
        attach(ob, j["pelvis"], (0.15 * h, 0.0, -0.05 * h))
        return (ob,)
    front = c["姿"] == "臂盾L"
    lift = 0.08 * h if shape == "竖长" else 0.16 * h        # 钢盾变大后中心下移：盾顶略高过肩、下沿到膝
    attach(ob, j["pelvis"], (0.05 * h if front else 0.0, (-0.16 if front else 0.09) * h, lift))
    return (ob,)


def _segment(objs: tuple, c: dict) -> None:
    """有「起 / 止」时只在那一段出现：时段外缩成一个点（藏起来）。"""
    if "起" in c or "止" in c:
        a0, a1 = float(c.get("起", 0.0)), float(c.get("止", TOTAL + 1))
        for ob in objs:
            for fr, s in ((1, 1e-4), (f(a0) - 1, 1e-4), (f(a0), 1.0), (f(a1) - 1, 1.0), (f(a1), 1e-4)):
                if fr >= 1:          # 换段两帧紧挨着，插值只跨一帧，等于瞬切（新版 Blender 的 Action 没有 fcurves，不去改插值）
                    ob.scale = (s, s, s)
                    ob.keyframe_insert("scale", frame=fr)


def make_quadruped(name: str, color: str, shoulder: float):
    """四足代理（狼）：朝 -Y 为前，与 make_figure 同向；joints["body"] 供后处理钩子做扑咬 / 翻滚的俯仰与抬高。"""
    m = _mat_for(color)
    m_lim = _mat_for("白" if color != "白" else "黄")
    s = shoulder
    root = empty(f"{name}", (0, 0, 0))
    body = empty(f"{name}_body", (0, 0, 0))
    attach(body, root, (0, 0, s * 0.78))
    torso = box(f"{name}_torso", (s * 0.38, s * 1.45, s * 0.42), (0, 0, 0), m)
    attach(torso, body, (0, 0, 0))
    head = box(f"{name}_head_m", (s * 0.30, s * 0.34, s * 0.28), (0, 0, 0), m)
    attach(head, body, (0, -s * 0.86, s * 0.22))
    snout = box(f"{name}_snout", (s * 0.14, s * 0.26, s * 0.13), (0, 0, 0), m_lim)
    attach(snout, body, (0, -s * 1.12, s * 0.16))
    for sx in (-1, 1):
        ear = box(f"{name}_ear{sx}", (s * 0.06, s * 0.04, s * 0.13), (0, 0, 0), m)
        attach(ear, body, (sx * s * 0.10, -s * 0.80, s * 0.42))
        for sy, tag in ((-1, "f"), (1, "b")):
            leg = box(f"{name}_leg{tag}{sx}", (s * 0.09, s * 0.09, s * 0.78), (0, 0, 0), m)
            attach(leg, body, (sx * s * 0.13, sy * s * 0.55, -s * 0.39))
    tail = box(f"{name}_tail", (s * 0.09, s * 0.55, s * 0.09), (0, 0, 0), m_lim)
    tail.rotation_euler = Euler((math.radians(-35), 0, 0))
    attach(tail, body, (0, s * 0.95, -s * 0.12))
    return root, {"body": body}


def import_body(a: dict) -> dict:
    """Cascadeur 烘焙动画 FBX → 本镜里的一个人：动画已带位移，只需平移到模型原点、按帧率重定时。"""
    nm = a["名"]
    src = (CFG_PATH.parent / a["模型"]).resolve()
    if not src.is_file():
        die(f"角色「{nm}」的模型 {src} 不存在（先跑 tools/cascadeur/choreo.py <shot 目录> --build）")
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=str(src))
    new = [o for o in bpy.data.objects if o not in before]
    arm = next((o for o in new if o.type == "ARMATURE"), None)
    if arm is None:
        die(f"{src.name} 里没有骨架")
    for o in new:
        link_previz(o)
        if o.type == "MESH":
            o.data.materials.clear()
            o.data.materials.append(_mat_for(a.get("色", "绿")))
    o0 = [float(v) for v in a.get("模型原点", [0, 0])]
    base = ORIGIN + Vector((o0[0], o0[1], 0.0))
    if GROUND:
        base.z = ground_z(base.x, base.y)
    arm.location = arm.location + base
    ad = arm.animation_data
    act = ad.action if ad else None
    if act is None:
        die(f"{src.name} 没有烘焙动画")
    src_fps = float(a.get("模型帧率", 30))
    ad.action = None
    strip = ad.nla_tracks.new().strips.new(act.name, 1, act)
    if hasattr(strip, "action_slot") and getattr(act, "slots", None):
        strip.action_slot = act.slots[0]
    strip.scale = FPS / src_fps
    dur = (act.frame_range[1] - act.frame_range[0]) / src_fps
    if dur + 1.0 / src_fps < TOTAL - 0.05:
        die(f"{src.name} 只有 {dur:.2f}s，短于镜长 {TOTAL}s")
    # 机位解算与占画比自检要一个「站在地上、跟着人走」的点：跟骨盆的水平位置、高度钉在原点地面
    root = empty(nm, base)
    con = root.constraints.new("COPY_LOCATION")
    con.target, con.subtarget, con.use_z = arm, "pelvis", False
    if GROUND:   # 动画是在平地上做的：逐帧把整个人抬 / 压到骨盆正下方的地面高度（坡上的小路不会把人埋进土里）
        for fr in range(1, f(TOTAL) + 1):
            scene.frame_set(fr)
            pel = arm.matrix_world @ arm.pose.bones["pelvis"].head
            z = ground_z(pel.x, pel.y)
            arm.location.z = z
            arm.keyframe_insert("location", index=2, frame=fr)
            root.location.z = z
            root.keyframe_insert("location", index=2, frame=fr)
    kj = src.parent / "keys.json"      # choreo.py 发给 Cascadeur 的逐键数据：烘焙对账用
    keys = json.loads(kj.read_text(encoding="utf-8"))["actors"].get(nm, []) if kj.is_file() else []
    return {"root": root, "joints": {}, "height": float(a.get("身高", 1.72)), "armature": arm, "keys": keys}


def lowest_z(root) -> float:
    """这一帧人偶网格的最低点（世界 Z）。"""
    return min((ob.matrix_world @ Vector(c)).z for ob in root.children_recursive if ob.type == "MESH" for c in ob.bound_box)


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
    for c in state.get("carry", ()):
        spec.update(POSES[c])
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
    if a.get("模型"):
        ACTORS[nm] = import_body(a)
        LAST_KEY_T = max([LAST_KEY_T] + [float(k["t"]) for k in a.get("关键帧", [])])
        continue
    quad = bool(a.get("四足"))
    root, joints = (make_quadruped if quad else make_figure)(nm, a.get("色", "绿"), float(a.get("身高", 1.72)))
    pose_state = {"base": "站", "root_tilt": 0.0, "carry": []}
    carries = a.get("持物", [])
    for i, c in enumerate(carries):
        check_keys(c, SCHEMA["角色.持物"], f"[[角色.持物]] of {nm}")
        if c.get("姿") not in CARRY_POSES:
            die(f"角色「{nm}」持物姿「{c.get('姿')}」不认识；可用＝{sorted(CARRY_POSES)}")
        make_carry(nm, joints, float(a.get("身高", 1.72)), c, root, i)

    def _carry_at(t: float) -> list:
        return [c["姿"] for c in carries if float(c.get("起", 0.0)) - 1e-6 <= t < float(c.get("止", 1e9))]
    last_yaw = 0.0
    bases: list[tuple[int, str]] = []
    kfs = a.get("关键帧", [])
    if not kfs:
        die(f"角色「{nm}」没有关键帧——A 档至少要给一帧站位")
    # 拿法换段的那一刻补一帧姿态（前一帧是旧拿法、这一帧是新拿法），不让手臂在两段之间慢慢飘过去
    _bounds = sorted({float(c[k]) for c in carries for k in ("起", "止") if k in c})
    kfs = sorted(list(kfs) + [{"t": tb} for tb in _bounds if not any(abs(float(k["t"]) - tb) < 1e-6 for k in kfs)],
                 key=lambda k: float(k["t"])) if _bounds else kfs
    for kf in kfs:
        check_keys(kf, SCHEMA["角色.关键帧"], f"[[角色.关键帧]] of {nm}")
        t = float(kf["t"])
        pose_state["carry"] = _carry_at(t)
        if _bounds and any(abs(t - tb) < 1e-6 for tb in _bounds) and not quad and t > 0:
            _prev = dict(pose_state, carry=_carry_at(t - 0.05))
            apply_pose(joints, f(t) - 1, pose_state["base"], _prev, root)
        LAST_KEY_T = max(LAST_KEY_T, t)
        fr = f(t)
        pos = kf.get("位置")
        if pos is not None:
            p = ORIGIN + Vector((float(pos[0]), float(pos[1]), float(pos[2]) if len(pos) > 2 else 0.0))
            if GROUND:
                p.z = ground_z(p.x, p.y) + (float(pos[2]) if len(pos) > 2 else 0.0)
            key_loc(root, fr, p)
        if not quad and ("姿态" in kf or carries):
            apply_pose(joints, fr, kf.get("姿态", pose_state["base"]), pose_state, root)
        bases.append((fr, pose_state["base"]))
        # 朝向与整体翻转同写一条 rotation_euler，必须一起打帧
        key_rot(root, fr, (pose_state["root_tilt"], 0.0,
                           float(kf["朝向"]) if "朝向" in kf else last_yaw))
        last_yaw = float(kf["朝向"]) if "朝向" in kf else last_yaw
    if not quad:   # 052：走路时两腿交替迈步（相位按走过的距离算），站 / 行走以外的底姿态不动
        _dist, _prev = 0.0, None
        for fr in range(1, f(TOTAL) + 1, 2):
            scene.frame_set(fr)
            _p = root.matrix_world.translation.copy()
            _step = 0.0 if _prev is None else math.hypot(_p.x - _prev.x, _p.y - _prev.y)
            _prev = _p
            _base = next((b for k, b in reversed(bases) if k <= fr), "站")
            if _base not in ("站", "站定", "行走") or _step * FPS / 2 < WALK_MIN_MPS:
                continue
            _dist += _step
            _s = math.sin(math.pi * _dist / WALK_STEP_M)
            key_rot(joints["hipL"], fr, (-WALK_HIP * _s, 0, 0))
            key_rot(joints["hipR"], fr, (WALK_HIP * _s, 0, 0))
            key_rot(joints["kneeL"], fr, (WALK_KNEE * max(0.0, _s), 0, 0))
            key_rot(joints["kneeR"], fr, (WALK_KNEE * max(0.0, -_s), 0, 0))
    if GROUND:   # 关键帧之间的直线插值会穿进坡里或悬空：逐帧把脚按回地面；弯腿姿态再按最低点压下去
        track = []
        for fr in range(1, f(TOTAL) + 1):
            scene.frame_set(fr)
            base = next((b for k, b in reversed(bases) if k <= fr), "站")
            _con = POSE_CONTACT.get(base)
            if quad or base in OFF_GROUND:
                lift = 0.0
            elif _con and _con[1] is not None:     # 049 G10：跌坐 / 跪按该着地的那处贴地，不按最低点（脚着地、屁股悬空）
                _js = [joints[j] for j in (_con[0], _con[0] + "L", _con[0] + "R") if j in joints]
                lift = min(j.matrix_world.translation.z for j in _js) - root.location.z - _con[1]
            else:
                lift = max(0.0, lowest_z(root) - root.location.z)
            track.append((fr, root.location.x, root.location.y, lift, base in ON_TOP))
        for fr, x, y, lift, seat in track:
            root.location = Vector((x, y, (seat_z(x, y) if seat else ground_z(x, y)) - lift))
            root.keyframe_insert("location", frame=fr)
    ACTORS[nm] = {"root": root, "joints": joints, "height": float(a.get("身高", 1.72)), "quad": quad, "bases": bases}
    _vis = []             # 049：入场前 / 离场后缩成一点（色块人偶的根带着全身与持物）
    if "入场" in a:
        _fe = f(float(a["入场"]))
        _vis += [(1, 1e-4), (max(1, _fe - 1), 1e-4), (_fe, 1.0)]
        ACTORS[nm]["enter"] = float(a["入场"])
    if "离场" in a:
        _fg = f(float(a["离场"]))
        _vis += [(max(1, _fg - 1), 1.0), (_fg, 1e-4)]
        ACTORS[nm]["gone"] = float(a["离场"])
    for _fr, _s in _vis:
        root.scale = (_s,) * 3
        root.keyframe_insert("scale", frame=_fr)

PROPS: dict[str, dict] = {}
for p in CFG.get("道具", []):
    check_keys(p, SCHEMA["道具"], "[[道具]]")
    nm, shape = p["名"], p.get("形", "box")
    size = [float(x) for x in p["尺寸"]]
    loc = list(ORIGIN + Vector([float(x) for x in p.get("位置", [0, 0, 0])]))
    if GROUND:
        loc[2] = ground_z(loc[0], loc[1]) + float(p.get("位置", [0, 0, 0])[2] if len(p.get("位置", [])) > 2 else 0.0)
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
    elif shape == "模型":
        # 从一份 .blend 追加真实网格当 proxy。给「产品即长相」的镜用（如车体白模）：
        # 色块方盒能定机位与尺度，但定不了「这台车看上去对不对」。
        rel = p.get("档")
        if not rel:
            die(f"道具「{nm}」形＝模型，必须给「档」＝白模 .blend 的仓库相对路径")
        blend_path = (REPO / str(rel)).resolve()
        if not blend_path.is_file():
            die(f"道具「{nm}」的白模档不存在：{blend_path}")
        _before = {o.name for o in bpy.data.objects}
        with bpy.data.libraries.load(str(blend_path), link=False) as (_src, _dst):
            _dst.objects = list(_src.objects)
        _new = [o for o in bpy.data.objects if o.name not in _before]
        _meshes = [o for o in _new if o.type == "MESH"]
        if not _meshes:
            die(f"道具「{nm}」的白模档里没有 MESH 物体：{blend_path}")
        for o in _new:
            if o.type != "MESH":
                bpy.data.objects.remove(o, do_unlink=True)
        for o in _meshes:
            scene.collection.objects.link(o)
        bpy.ops.object.select_all(action="DESELECT")
        for o in _meshes:
            o.select_set(True)
        bpy.context.view_layer.objects.active = _meshes[0]
        if len(_meshes) > 1:
            bpy.ops.object.join()
        ob = bpy.context.view_layer.objects.active
        ob.name = f"P_{nm}"
        # 归一化到「尺寸」给的包围盒，原点挪到底面中心（与 box 分支同约定）
        bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
        _d = ob.dimensions
        if min(_d) <= 0:
            die(f"道具「{nm}」白模包围盒异常：{tuple(_d)}")
        ob.scale = Vector((size[0] / _d.x, size[1] / _d.y, size[2] / _d.z))
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        ob.data.materials.clear()
        # 白模 prop 不用 MATS 的 ID 色——那套材质带 emission 0.25，自发光是平的，
        # 会把这个物体的型面抹平。而白模 prop 恰恰是全场唯一需要读出型面的东西
        # （色块方盒只需要读位置，读不读得出形状无所谓）。给它专用的无自发光灰模。
        _wm = bpy.data.materials.get("M_WHITEMODEL")
        if _wm is None:
            _wm = mat("M_WHITEMODEL", (0.62, 0.62, 0.63), 0.0)
            _wb = _wm.node_tree.nodes.get("Principled BSDF")
            _wb.inputs["Roughness"].default_value = 0.65
            if "Specular IOR Level" in _wb.inputs:
                _wb.inputs["Specular IOR Level"].default_value = 0.2
        ob.data.materials.append(_wm)
        ob.location = Vector((loc[0], loc[1], loc[2] + size[2] / 2))
        link_previz(ob)
        dim_h = size[2]
    else:
        die(f"道具「{nm}」的形＝{shape} 不认识；可用＝box/plane/cyl/sphere/模型")
    if "朝向" in p:
        ob.rotation_euler = Euler((0, 0, math.radians(float(p["朝向"]))))
    for kf in p.get("关键帧", []):
        check_keys(kf, SCHEMA["道具.关键帧"], f"[[道具.关键帧]] of {nm}")
        t = float(kf["t"])
        LAST_KEY_T = max(LAST_KEY_T, t)
        fr = f(t)
        if "位置" in kf:
            q = list(ORIGIN + Vector([float(x) for x in kf["位置"]]))
            if GROUND:     # 049 G9：会动的道具每个路点都贴地（与起点同一规则）
                q[2] = ground_z(q[0], q[1]) + (float(kf["位置"][2]) if len(kf["位置"]) > 2 else 0.0)
            key_loc(ob, fr, (q[0], q[1], q[2] + dim_h / 2))
        if "朝向" in kf:
            key_rot(ob, fr, (0, 0, float(kf["朝向"])))
        if "尺寸" in kf:
            s = [float(x) for x in kf["尺寸"]]
            key_scale(ob, fr, (s[0] / size[0], s[1] / size[1] if len(s) > 1 else 1.0,
                               s[2] / size[2] if len(s) > 2 else 1.0))
    PROPS[nm] = {"ob": ob, "height": dim_h}


# ---------------------------------------------------------------- 每镜后处理（S 档：手持物件、四足的扑咬等镜内细节）
# 钩子是本镜目录里的 shot{NN}_previz.py，在建完人与道具之后、解算机位之前，以本引擎的全局名字空间执行
# （rule 4h ③：per-shot 代码只补本镜细节、引擎本体不拷贝）。
if G.get("后处理"):
    _hook = (CFG_PATH.parent / G["后处理"]).resolve()
    if not _hook.is_file():
        die(f"[全局].后处理 {_hook} 不存在")
    exec(compile(_hook.read_text(encoding="utf-8"), str(_hook), "exec"), globals())

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

WAYPTS = CAM.get("路点", [])
if WAYPTS:
    if MOVES or CAM.get("锁定主体") or "位置" in CAM:
        die("[机位] 路点 与 运镜 / 锁定主体 / 位置 互斥：路点本身就是整条机位路径")
    for w in WAYPTS:
        check_keys(w, SCHEMA["机位.路点"], "[[机位.路点]]")
    wts = [float(w["t"]) for w in WAYPTS]
    if wts[0] != 0 or wts != sorted(wts):
        die(f"[[机位.路点]] 的 t 必须从 0 起且递增：{wts}")
    LAST_KEY_T = max(LAST_KEY_T, wts[-1])
    runs: list[list[dict]] = [[]]          # 硬切把路点分成几段，段与段之间不插值
    for i, w in enumerate(WAYPTS):
        if i and w.get("切"):
            runs.append([])
        runs[-1].append(w)

    def _way(t: float) -> tuple[Vector, Vector, float]:
        run = next(r for r in reversed(runs) if float(r[0]["t"]) <= t + 1e-9)
        ts = [float(w["t"]) for w in run]

        def comp(key: str, i: int) -> float:
            return mono_hermite(ts, [float(w[key][i]) for w in run], t, ease_in=False)
        pos = ORIGIN + Vector([comp("位置", i) for i in range(3)])
        at = ORIGIN + Vector([comp("瞄", i) for i in range(3)])
        if GROUND:   # 路点的 z 是离地高度（overhead 的 h）
            pos.z = ground_z(pos.x, pos.y) + comp("位置", 2)
            at.z = ground_z(at.x, at.y) + comp("瞄", 2)
        return pos, at, mono_hermite(ts, [float(w.get("焦距", lens)) for w in run], t, ease_in=False)

    cam.parent = None
    prev = None
    for fr in range(1, f(TOTAL) + 1):
        pos, at, ln = _way((fr - 1) / FPS)
        rot = (at - pos).to_track_quat("-Z", "Y").to_euler("XYZ", prev) if prev else \
            (at - pos).to_track_quat("-Z", "Y").to_euler("XYZ")
        prev = rot
        cam.location, cam.rotation_euler = pos, rot
        cam.keyframe_insert("location", frame=fr)
        cam.keyframe_insert("rotation_euler", frame=fr)
        cam_data.lens = ln
        cam_data.keyframe_insert("lens", frame=fr)
    cam_world, aim = _way(0.0)[:2]


# ---------------------------------------------------------------- 自动切墙
# 内景 previz 的老问题：相机与主体之间隔着墙/天花板/屋顶。previz 师傅的做法是
# 手动把挡镜的那面墙藏掉（cutaway）。这里沿 相机→主体 射线自动做：命中谁藏谁，
# 直到通路打开。只藏场景主档的件，PREVIZ 集合里的 proxy 永不隐藏。
# 路点机位默认不切墙：只按起幅一条射线判挡镜，会把机位后来才穿过的门墙（本镜的主体）整面藏掉
if G.get("场景") and CAM.get("切墙", not WAYPTS):
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
# 三点布光。previz 要读的是【型面】——曲面往哪拐、哪里鼓、哪里凹。
# 平光（等能量对打的两盏 sun）会把这些信息抹平：灰模在平光下就是一片均匀的灰。
# 所以主光压低角度、拉开与补光的比值，再加一盏背侧轮廓光把剪影从背景里剥出来。
sun = bpy.data.lights.new("PREVIZ_SUN", type="SUN")
sun.energy = 5.0
sun.angle = math.radians(6)          # 软一点，避免硬边切碎型面
sun_ob = bpy.data.objects.new("PREVIZ_SUN", sun)
link_previz(sun_ob)
sun_ob.rotation_euler = Euler((math.radians(38), 0, math.radians(35)))
sun2 = bpy.data.lights.new("PREVIZ_FILL", type="SUN")   # 补光：只抬暗部，不许压平主光
sun2.energy = 0.9                                       # 主:补 ≈ 5.5:1，原来是 2.5:1
fill_ob = bpy.data.objects.new("PREVIZ_FILL", sun2)
link_previz(fill_ob)
fill_ob.rotation_euler = Euler((math.radians(65), 0, math.radians(-140)))
sun3 = bpy.data.lights.new("PREVIZ_RIM", type="SUN")    # 轮廓光：剥离剪影
sun3.energy = 3.0
rim_ob = bpy.data.objects.new("PREVIZ_RIM", sun3)
link_previz(rim_ob)
rim_ob.rotation_euler = Euler((math.radians(72), 0, math.radians(196)))
if scene.world is None or not scene.world.name.startswith("PREVIZ"):
    _w = bpy.data.worlds.new("PREVIZ_WORLD")
    _w.use_nodes = True
    _bg = _w.node_tree.nodes.get("Background")
    if _bg is not None:
        _bg.inputs[0].default_value = (0.42, 0.45, 0.50, 1.0)
        _bg.inputs[1].default_value = 1.0
    scene.world = _w

# ---------------------------------------------------------------- 形状可读性
# previz 的唯一职责是把【形】和【走位】交给 Seedance。参考图只覆盖 4 个固定角度，
# 其余角度上「这台车是什么形状」，Seedance 只能从 previz 里读——读不到就自己编，
# 编出来就是逐镜车型漂移（benchmark_teardown.md 点名的竞品头号缺陷）。
# 默认渲染设置（平光 + 无 AO + 无描边）会在渲染这一步就把型面信息丢掉，
# 网格再好也传不出去。下面三项是把形状真正渲进画面的最低配置。

# ① 环境光遮蔽——凹陷、缝隙、轮拱内侧、扩散器叶片之间靠它才有暗部
scene.eevee.use_raytracing = True
scene.eevee.use_fast_gi = True
scene.eevee.fast_gi_method = "AMBIENT_OCCLUSION_ONLY"
scene.eevee.fast_gi_distance = 0.6          # 米。车身尺度下 0.6 能吃住轮拱与进气口
scene.eevee.fast_gi_ray_count = 4
scene.eevee.fast_gi_step_count = 12
scene.eevee.fast_gi_resolution = "1"
scene.eevee.taa_render_samples = max(scene.eevee.taa_render_samples, 32)   # AO 要采样才不噪

# ② Freestyle 轮廓描边——灰模上读转折最有效的一招，且不引入任何美术
# 同 render_object_turntable：高面数网格关掉 Freestyle——它在生成网格的非流形
# 拓扑上会崩，且高面数靠 AO 就读得出型面。
_dense = sum(len(o.data.polygons) for o in bpy.data.objects if o.type == "MESH")
scene.render.use_freestyle = _dense < 60000   # 原 200k：ep01 shot08 有七块 2.3 万面的 Rodin 石头（共 16.8 万面），描边一帧 20 s，整条要 3 小时
scene.render.line_thickness_mode = "ABSOLUTE"
scene.render.line_thickness = 1.0
_fs = bpy.context.view_layer.freestyle_settings
for _ls in list(_fs.linesets):
    _fs.linesets.remove(_ls)
_ls = _fs.linesets.new("PREVIZ_FORM")
_ls.select_silhouette = True        # 外轮廓
_ls.select_border = True            # 开放边界
_ls.select_crease = True            # 硬转折
_ls.select_ridge_valley = True      # 曲面脊/谷：泪滴座舱、后轮拱外鼓靠这条才显形
_ls.select_contour = False
_ls.select_edge_mark = False
_fs.crease_angle = math.radians(130)
_ls.linestyle.color = (0.05, 0.05, 0.06)
# Blender 5.1 的粗细着色器对 BORDER 边读 fe.normal_left，光滑网格的边是 FEdgeSmooth、没有这个属性：
# 整条描边逐帧抛错（ep01 shot08 矿洞：满屏 traceback、一帧 20 s）。碰到就退回居中粗细。
try:
    import parameter_editor as _pe

    _orig_set = _pe.ThicknessModifierMixIn.set_thickness

    def _safe_set(self, sv, outer, inner):
        try:
            _orig_set(self, sv, outer, inner)
        except AttributeError:
            sv.attribute.thickness = ((outer + inner) / 2, (outer + inner) / 2)

    _pe.ThicknessModifierMixIn.set_thickness = _safe_set
except ImportError:
    pass
_ls.linestyle.thickness = 1.2

# ③ 背景压深一档，让轮廓光剥出来的剪影有对比可读
if scene.world is not None and scene.world.use_nodes:
    _bgn = scene.world.node_tree.nodes.get("Background")
    if _bgn is not None:
        _bgn.inputs[0].default_value = (0.20, 0.22, 0.26, 1.0)

print("  形状可读性：AO(0.6m) + Freestyle(轮廓/边界/折痕/脊谷) + 三点光 已启用")


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
# 2026-09-12：容差原为绝对值 0.08——在 frac=0.3 时是 ±27%（够松），到 frac=1.2 时只剩 ±6.7%（过严）。
# 横置构件（如 shot36 的房梁：7.0×0.34×0.30 的横梁）被仰角拍时，投影纵向跨度天然不等于声明的「高」，
# 实测恒为目标的九成左右，于是任何 >0.8 的目标都必然判失败。改成随目标放大的相对容差。
_tol = max(0.08, 0.12 * frac)
if abs(occ_j - frac) > _tol:
    # 自动解算时占画比是硬约束；手动指定机位时作者已经自己定了距离，只报不拦
    msg = f"占画比实测 {occ_j:.2f} 与目标 {frac:.2f} 偏差过大（容差 ±{_tol:.2f}）"
    (print(f"  [warning] {msg}（手动机位）") if "位置" in CAM or WAYPTS else problems.append(msg))
if not judge_at_end and not (0.0 <= lo.x <= 1.0):
    # 路点机位的第一段可以是「先给环境、人再入画」的横移（ep01 shot13 摊位横移）：主体在第一段结束前入画即可
    _run_end = next((float(w["t"]) for w in WAYPTS[1:] if w.get("切")), TOTAL) if WAYPTS else 0.0
    _enter = next((fr for fr in range(1, f(_run_end) + 1)
                   if 0.0 <= occupancy(subj_ob, subj_h, fr)[1].x <= 1.0), None) if WAYPTS else None
    if _enter is None:
        problems.append("基准主体起幅不在画面内（横向偏移过大？）")
    else:
        print(f"  基准主体起幅在画外，{(_enter - 1) / FPS:.1f}s 随机位移动入画（第一段 0–{_run_end:g}s 内）")

# 2026-09-12：occupancy() 只量【纵向跨度】，从不检查主体是否真的落在画框纵向区间里，
# 也不检查机位有没有钻到地面以下 —— shot09 的「自检报 49%、实渲主体只有两三像素 + 中途一帧糊掉」
# 就是这么漏过去的（俯角 -10° 仰拍，解算出的机位 z = -0.17m，埋在地里）。补两道硬检查：
def _cam_z(fr):
    scene.frame_set(fr); bpy.context.view_layer.update()
    return cam.matrix_world.translation.z

for _fr, _tag in ((1, "起幅"), (scene.frame_end, "落幅")):
    if _cam_z(_fr) < 0.05:
        problems.append(f"{_tag}机位在地面以下（z={_cam_z(_fr):.2f}m）——俯角为负(仰拍)时会把机位解到地里，改俯角或用「位置」手动指定")
    _o, _lo, _hi = occupancy(subj_ob, subj_h, _fr)
    _top, _bot = max(_lo.y, _hi.y), min(_lo.y, _hi.y)
    if _bot > 1.0 or _top < 0.0:
        problems.append(f"{_tag}基准主体整个在画框外（纵向 {_bot:.2f}–{_top:.2f}）")
    elif _bot < -0.25 or _top > 1.25:
        print(f"  [warning] {_tag}基准主体大幅超出画框纵向范围（{_bot:.2f}–{_top:.2f}）")
scene.frame_set(1); bpy.context.view_layer.update()

occ_end, _, _ = occupancy(subj_ob, subj_h, scene.frame_end)
print(f"  基准主体落幅占画高 {occ_end * 100:.1f}%")

# ③′ 人不许站进场景实体（follow-up 032：shot01 两名卫兵整个埋在门塔里——门塔是 gate_wall 构件自己长出来的，
#     平面图上没有，平面图闸门抓不到；几何第一次存在的地方就是这里）。
#     不看面法线（场景构件的法线朝向不可靠，实测把门洞过梁下的人误报、把塔里的人漏掉）：从腰高竖直往上打穿，
#     同一物体被穿过奇数次、且腰点落在它的包围盒里 ＝ 人在它里面。previz 自建物与地形不算。
_deps = bpy.context.evaluated_depsgraph_get()


def _inside_scene(pt):
    counts: dict[str, int] = {}
    o = pt.copy()
    for _ in range(80):
        _hit, _loc, _n, _i, _ob, _m = scene.ray_cast(_deps, o, Vector((0, 0, 1)), distance=60.0)
        if not _hit:
            break
        if PREVIZ.objects.get(_ob.name) is None and not any(g in _ob.name for g in GROUND):
            counts[_ob.name] = counts.get(_ob.name, 0) + 1
        o = _loc + Vector((0, 0, 0.005))
    for name, c in counts.items():
        if c % 2:
            ob = bpy.data.objects[name]
            lp = ob.matrix_world.inverted() @ pt
            bb = [Vector(v) for v in ob.bound_box]
            if all(min(v[k] for v in bb) <= lp[k] <= max(v[k] for v in bb) for k in range(3)):
                return name
    return None


for nm, a in ACTORS.items():
    for _fr in range(1, scene.frame_end + 1, max(1, FPS // 2)):
        if not a.get("enter", -1.0) <= (_fr - 1) / FPS <= a.get("gone", 1e9):    # 场外（洞里）的人不算站进墙里
            continue
        scene.frame_set(_fr)
        _in = _inside_scene(a["root"].matrix_world.translation + Vector((0, 0, 1.0)))
        if _in:
            problems.append(f"角色「{nm}」{(_fr - 1) / FPS:.1f}s 站进了场景实体「{_in}」—— 改 overhead 站位")
            break
scene.frame_set(1)

# ③″ 可见性表（follow-up 032：shot01 问话段西侧卫兵被挡、东侧卫兵在画外，渲完整条才看见）。
#     每段机位的段中，从相机向每个人的胸口打一条射线：先打中的不是这个人自己，就报「被 X 挡住」；
#     不在画框里报「画外」。只报不拦（有的人本来就该在画外），`review.py` 与 --no-render 都会打印。
_owner: dict[str, str] = {}
for nm, a in ACTORS.items():
    for ob in [a["root"], *a["root"].children_recursive, *((a["armature"], *a["armature"].children_recursive)
                                                          if a.get("armature") else ())]:
        _owner[ob.name] = nm
_cuts = [0.0] + [float(w["t"]) for w in WAYPTS if w.get("切")] + [TOTAL]
for _a, _b in zip(_cuts, _cuts[1:]):
    _tm = (_a + _b) / 2
    scene.frame_set(f(_tm))
    bpy.context.view_layer.update()
    _dg = bpy.context.evaluated_depsgraph_get()
    _cp = cam.matrix_world.translation.copy()
    _rows = []
    _walled = []      # 被场景件（不是别的人、不是手持物）挡住的人
    for nm, a in ACTORS.items():
        if a.get("armature"):
            _arm = a["armature"]
            _pt = _arm.matrix_world @ _arm.pose.bones["chest"].head if "chest" in _arm.pose.bones else \
                a["root"].matrix_world.translation + Vector((0, 0, a["height"] * 0.7))
        else:
            _pt = a["root"].matrix_world.translation + Vector((0, 0, a["height"] * (0.45 if a.get("quad") else 0.7)))
        _v = world_to_camera_view(scene, cam, _pt)
        if not (0.0 <= _v.x <= 1.0 and 0.0 <= _v.y <= 1.0 and _v.z > 0):
            _rows.append(f"{nm} 画外")
            continue
        _d = _pt - _cp
        _hit, _loc, _n, _i, _ob, _m = scene.ray_cast(_dg, _cp, _d.normalized(), distance=_d.length - 0.05)
        # 钩子挂的手持物（「杜克_盾」「亚伦_锤柄」）按名字前缀归到它的主人：自己的盾不算挡住自己
        _who = _owner.get(_ob.name) or next((k for k in ACTORS if _ob.name.startswith(k + "_")), None) if _hit else None
        if _hit and _who != nm:
            _rows.append(f"{nm} 被「{_who or _ob.name}」挡住")
            if _who is None and PREVIZ.objects.get(_ob.name) is None:
                _walled.append(nm)
    print(f"  [可见性] {_a:g}–{_b:g}s（段中 {_tm:g}s）：" + ("；".join(_rows) if _rows else "全员在画、无遮挡"))
    # 人物离地（follow-up 035：跌坐的人悬在半空，静帧才看出来）。只查色块人偶：Cascadeur 体是蒙皮网格，
    # bound_box 是静止姿势的，量不准；它的贴地由 import_body 按骨盆逐帧做
    for nm, a in ACTORS.items():
        if a.get("quad") or a.get("armature") or not GROUND:
            continue
        _base = next((b for k, b in reversed(a.get("bases", [])) if k <= f(_tm)), "站")
        if _base in OFF_GROUND:
            continue
        _gp = a["root"].matrix_world.translation
        _lift = lowest_z(a["root"]) - (seat_z if _base in ON_TOP else ground_z)(_gp.x, _gp.y)
        if _lift > FLOAT_MAX:
            problems.append(f"{_a:g}–{_b:g}s 段中「{nm}」最低点离地 {_lift:.2f} m（姿态 {_base}）——人物悬空")
    # 画里的人全被场景件挡住 ＝ 机位对着墙 / 屋顶在拍（ep01 shot06 窝棚、shot08 内景外壳）：这一段是废的
    _inframe = [nm for nm in ACTORS if f"{nm} 画外" not in _rows]
    if _inframe and set(_inframe) <= set(_walled):
        problems.append(f"{_a:g}–{_b:g}s 段中画里的人全被场景件挡住（{'、'.join(_walled)}）—— 机位在对着墙拍，改 overhead 机位")
scene.frame_set(1)

# ③″ 该着地的那处着地、人在配置写的位置上（049 G10：S11 / S20 跌坐的人脚着地、屁股悬在矿工肩高，
#     最低点检查照样过）。每个关键帧时刻：色块人偶按底姿态量 POSE_CONTACT 的关节离地；
#     根的水平位置（Cascadeur 体取骨盆）与配置差 > ROOT_DEV_MAX 即 blocker。
for a0 in CFG.get("角色", []):
    a = ACTORS.get(a0["名"])
    if a is None or a.get("quad"):
        continue
    _cuts = [float(w["t"]) for w in WAYPTS if w.get("切")]
    for kf in a0.get("关键帧", []):
        _t = float(kf["t"])
        if any(0.0 <= c - _t <= 0.2 for c in _cuts) or _t > a.get("gone", 1e9):   # 切点前一刻人要「跳」到下一段的站位；离场的不量
            continue
        scene.frame_set(f(_t))
        bpy.context.view_layer.update()
        arm = a.get("armature")
        _feet = [arm.pose.bones[b] for b in ("foot_l", "foot_r") if b in arm.pose.bones] if arm is not None else []
        _pel = arm.matrix_world @ arm.pose.bones["pelvis"].head if arm is not None and "pelvis" in arm.pose.bones else None
        if len(_feet) == 2 and not (_pel is not None and _pel.z - ground_z(_pel.x, _pel.y) < SIT_PELVIS_M):
            # Cascadeur 体：站位＝两脚中点（摆架势时骨盆会前后偏，不是人挪了位置）；坐在地上两腿往前伸，站位是屁股（052 shot11）
            _p = (arm.matrix_world @ _feet[0].head + arm.matrix_world @ _feet[1].head) / 2
        elif arm is not None and "pelvis" in arm.pose.bones:
            _p = arm.matrix_world @ arm.pose.bones["pelvis"].head
        else:
            _p = a["root"].matrix_world.translation
        if "位置" in kf:
            _want = ORIGIN + Vector((float(kf["位置"][0]), float(kf["位置"][1]), 0.0))
            _dev = math.hypot(_p.x - _want.x, _p.y - _want.y)
            if _dev > ROOT_DEV_MAX:
                problems.append(f"「{a0['名']}」{_t:g}s 人在 ({_p.x - ORIGIN.x:.2f}, {_p.y - ORIGIN.y:.2f})，配置要的是 "
                                f"({float(kf['位置'][0]):.2f}, {float(kf['位置'][1]):.2f})，差 {_dev:.2f} m（> {ROOT_DEV_MAX} m）")
        if arm is not None or not GROUND:
            continue
        _base = next((b for k, b in reversed(a.get("bases", [])) if k <= f(_t)), "站")
        if _base not in POSE_CONTACT:
            continue
        _jn, _rest, _lim = POSE_CONTACT[_base]
        _js = [a["joints"][j] for j in (_jn,) + tuple(_jn + s for s in "LR") if j in a["joints"]]
        _surf = seat_z if _base in ON_TOP else ground_z
        _z = min(j.matrix_world.translation.z - _surf(j.matrix_world.translation.x, j.matrix_world.translation.y) for j in _js)
        if _z > _lim:
            problems.append(f"「{a0['名']}」{_t:g}s 姿态「{_base}」该着地的{_jn}离地 {_z:.2f} m（> {_lim} m）——悬空，改姿态定义或配置")
scene.frame_set(1)

# ③‴ Cascadeur 烘焙与编排对账（follow-up 042：shot05 亚伦 8–11.8s 编排是站着的应战架势、前倾 6°，
#     烘出来弯腰低头到 73°——Bezier 把后面大抡的动作提前拉了进来，出片里他「看见狼就低头」）。
#     每段 ≥ 0.6 s 的键间隔取 ¼ / ½ / ¾ 三点，骨盆→头的连线与竖直的夹角对编排的 lean（线性插值），差 > LEAN_TOL 即 blocker。
for nm, a in ACTORS.items():
    ks = a.get("keys") or []
    arm = a.get("armature")
    if not ks or arm is None or "head" not in arm.pose.bones:
        continue
    for k0, k1 in zip(ks, ks[1:]):
        t0, t1 = float(k0["t"]), float(k1["t"])
        if t1 - t0 < 0.6:
            continue
        l0, l1 = float(k0["pose"].get("lean", 0)), float(k1["pose"].get("lean", 0))
        for u in (0.25, 0.5, 0.75):
            tm = t0 + (t1 - t0) * u
            scene.frame_set(f(tm))
            bpy.context.view_layer.update()
            hp = arm.matrix_world @ arm.pose.bones["head"].head
            pp = arm.matrix_world @ arm.pose.bones["pelvis"].head
            got = math.degrees(math.atan2(math.hypot(hp.x - pp.x, hp.y - pp.y), hp.z - pp.z))
            want = l0 + (l1 - l0) * u
            if abs(got - abs(want)) > LEAN_TOL:      # 量的是离竖直多少度（不分前后），编排的后仰写负数
                problems.append(f"「{nm}」{tm:.1f}s 烘出来躯干前倾 {got:.0f}°，编排是 {want:.0f}°（{k0['expr']} → {k1['expr']}）"
                                f"——Cascadeur 插值走样，同姿势保持段要 LINEAR；改 choreo 后重跑 --build")
                break
scene.frame_set(1)

# ③⁗ 命中贴身（follow-up 042：shot05 亚伦的锤一下都没打到狼）：overhead [[hit]] 抄来的每一下，
#     t ± 0.12 s 里「物件」离「目标」任何一块身体的包围盒最近距离 ≤ HIT_TOL；物件或目标找不到也是 blocker。
FRIEND_CLEAR = 0.45


def _aabb_gap(pt, ob):
    cs = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
    lo = Vector((min(c.x for c in cs), min(c.y for c in cs), min(c.z for c in cs)))
    hi = Vector((max(c.x for c in cs), max(c.y for c in cs), max(c.z for c in cs)))
    q = Vector((min(max(pt.x, lo.x), hi.x), min(max(pt.y, lo.y), hi.y), min(max(pt.z, lo.z), hi.z)))
    return (pt - q).length


for hdef in CFG.get("命中", []):
    check_keys(hdef, SCHEMA["命中"], "[[命中]]")
    if hdef.get("远程"):
        continue
    tgt = ACTORS.get(hdef["目标"])
    part_obs = ([o for o in bpy.data.objects if re.fullmatch(re.escape(hdef["目标"] + "_" + hdef["部位"]) + r"\d*", o.name)]
                if hdef.get("部位") else None)
    if part_obs is not None and not part_obs:
        problems.append(f"命中 {float(hdef['t']):g}s：打在{hdef['目标']}的「{hdef['部位']}」上，previz 里他身上没有这件——在 [[角色.持物]] 给他")
        continue
    # 同一件分几段拿法时第二段起带序号（「亚伦_锤头2」）：只量命中那一刻显形的那一个
    wobs = [o for o in bpy.data.objects if re.fullmatch(re.escape(hdef["物件"]) + r"\d*", o.name)]
    atk = ACTORS.get(hdef["谁"])
    body_hit = hdef["物件"].rpartition("_")[2] in BODY_HITS
    if tgt is None or (not wobs and atk is None):
        problems.append(f"命中 {float(hdef['t']):g}s：「{hdef['目标'] if tgt is None else hdef['谁']}」在 previz 里找不到")
        continue
    if not wobs and not body_hit:          # follow-up 047 G5：兵器件缺了就是缺了，不许退成量身体、放宽容差混过去
        problems.append(f"命中 {float(hdef['t']):g}s：{hdef['谁']}的「{hdef['物件']}」previz 里没有——在 [[角色.持物]] 给他这件")
        continue
    tol = HIT_TOL if wobs else HIT_TOL + 0.2
    srcs = wobs or [o for o in (atk.get("armature") or atk["root"]).children_recursive if o.type == "MESH"]
    body = part_obs or [o for o in (tgt.get("armature") or tgt["root"]).children_recursive if o.type == "MESH"]
    best = 9e9
    for fr in range(f(float(hdef["t"]) - 0.12), f(float(hdef["t"]) + 0.12) + 1):
        scene.frame_set(fr)
        bpy.context.view_layer.update()
        for so_ in srcs:
            if wobs and so_.scale.x < 0.5:          # 这一段没拿这件（缩成点藏着）
                continue
            c = so_.matrix_world @ (sum((Vector(v) for v in so_.bound_box), Vector()) / 8)
            best = min([best] + [_aabb_gap(c, o) for o in body if not part_obs or o.scale.x >= 0.5])
    # G19 友方不入挥击线（用户 2026-10-02：亚伦的锤砸向杜克的盾）：挥击窗口里家伙离每个自己人（含他的盾）都得 ≥ FRIEND_CLEAR
    for fname in hdef.get("友方", []):
        fa = ACTORS.get(fname)
        if fa is None or not wobs:
            continue
        fbody = [o for o in (fa.get("armature") or fa["root"]).children_recursive if o.type == "MESH"] +                 [o for o in bpy.data.objects if o.name.startswith(fname + "_") and o.type == "MESH"]
        gap = 9e9
        for fr in range(f(float(hdef["t"]) - 0.3), f(float(hdef["t"]) + 0.1) + 1):
            scene.frame_set(fr)
            bpy.context.view_layer.update()
            for so_ in wobs:
                if so_.scale.x < 0.5:
                    continue
                c = so_.matrix_world @ (sum((Vector(v) for v in so_.bound_box), Vector()) / 8)
                gap = min([gap] + [_aabb_gap(c, o) for o in fbody if o.scale.x >= 0.5])
        if gap < FRIEND_CLEAR:
            problems.append(f"命中 {float(hdef['t']):g}s：{hdef['谁']}的「{hdef['物件']}」挥击时离自己人{fname}（含他的盾）只有 {gap:.2f} m（< {FRIEND_CLEAR} m）"
                            "——挥击线上有自己人，换站位 / 面朝（G19）")
    if best > tol:
        problems.append(f"命中 {float(hdef['t']):g}s：{hdef['谁']}的「{hdef['物件']}」离{hdef['目标']}最近 {best:.2f} m（> {tol:.2f} m）"
                        "——打空了，改动作时刻或站位")
    else:
        print(f"  [命中] {float(hdef['t']):g}s {hdef['谁']} → {hdef['目标']}{'的' + hdef['部位'] if hdef.get('部位') else ''}：贴身 {best:.2f} m ✓")
scene.frame_set(1)

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



def _still_times() -> list[float]:
    if STILLS and "=" in STILLS:
        return sorted(float(x) for x in STILLS.split("=", 1)[1].split(",") if x.strip())
    cuts = [0.0] + [float(w["t"]) for w in WAYPTS if w.get("切")] + [TOTAL]
    ts = [0.3, TOTAL - 0.3]
    for a, b in zip(cuts, cuts[1:]):
        ts += [a + 0.3, (a + b) / 2, b - 0.3]
    ts += [k * 3.0 for k in range(1, int(TOTAL // 3) + 1)]
    out: list[float] = []
    for x in sorted(ts):
        if 0 <= x <= TOTAL and all(abs(x - y) > 0.8 for y in out):
            out.append(round(x, 2))
    return out[:16]


if STILLS:   # 有 blocker 也照出静帧——静帧正是用来看 blocker 长什么样的
    _sd = OUT_DIR / "frames" / "stills"
    _sd.mkdir(parents=True, exist_ok=True)
    for _old in _sd.glob(f"{SHOT}_*.png"):
        _old.unlink()
    if hasattr(scene.render.image_settings, "media_type"):
        scene.render.image_settings.media_type = "IMAGE"
    scene.render.image_settings.file_format = "PNG"
    scene.render.resolution_percentage = 50
    if hasattr(scene, "eevee") and hasattr(scene.eevee, "taa_render_samples"):
        scene.eevee.taa_render_samples = 8
    for _t in _still_times():
        scene.frame_set(f(_t))
        scene.render.filepath = str(_sd / f"{SHOT}_{_t:05.2f}s.png")
        bpy.ops.render.render(write_still=True)
    print(f"[previz] 静帧 → {_sd}")
    if not problems:     # 049 G10：静帧只在自检过了时盖戳；带 blocker 的静帧是拿来看问题的，不算交付
        (OUT_DIR / "frames" / f"{SHOT}{STILLS_STAMP}").write_text(
            json.dumps(render_inputs(CFG_PATH), ensure_ascii=False, indent=1), encoding="utf-8")

if problems:
    print("\n  [blocker]")
    for p in problems:
        print(f"    ✗ {p}")
    print()
    sys.exit(2)
print("  自检通过 ✓\n")
if STILLS:
    sys.exit(0)

if DO_RENDER:
    bpy.ops.render.render(animation=True)
    print(f"[previz] 渲毕 → {scene.render.filepath}")
    (OUT_DIR / f"{SHOT}{PREVIZ_STAMP}").write_text(json.dumps(render_inputs(CFG_PATH), ensure_ascii=False, indent=1),
                                                   encoding="utf-8")      # 049 G10：生成器拿当前输入重算、对不上即 raise
    # Seedance 单条参考视频 ≤ 15 s：超长的切成几段（段界优先落在镜内硬切上），shot md 的参考行按段挂
    _parts = seedance_ref.split(Path(scene.render.filepath), float(G.get("参考截止", TOTAL)), [float(w["t"]) for w in WAYPTS if w.get("切")])
    if len(_parts) > 1:
        print("[previz] 超过 %gs，切成 %d 段：%s" % (seedance_ref.LIMITS["max_s"], len(_parts), "、".join(p.name for p in _parts)))
