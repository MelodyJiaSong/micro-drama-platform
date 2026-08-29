"""AI 短剧 previz 的共用人形 proxy（`agent_refs/project/ai_video.md` rule 12.16 §3）。

**为什么是共用模块而不是各镜一份。** shot12 与 shot13 的 previz 原本各自持有一份
一模一样的人形代码。shot12 的人形按用户反馈细化了三轮（手建到三节指骨、四肢改收分
体、六处关节球、自动平滑），shot13 那份却停在最初版——两份复制品必然跑偏，而且跑偏
的方式很隐蔽：两镜相邻，观众会直接看到同一个人前后变了体型。所以人形只此一处。

**用法**（Blender 脚本里，先把仓库根目录加进 sys.path）：

    rig = PrevizRig(link=link_previz, body=M_GREEN, skin=M_SKIN, limb_end=M_LIMB)
    root, pelvis, J = rig.build(P)
    rig.hand_pose(J, "R", frame, HAND_SWORD_FINGER)

`link` 是宿主脚本的「把物件收进本镜 previz 集合」回调 —— 集合名各镜不同，模块不猜。

**坐标约定**：人形静默面朝 -Y、脚踩 z=0；四肢与手指静默指向 -Z，绕各自局部 X 正向
弯曲即为「向内屈」。`build()` 返回的 `J` 是可摆关节字典，键名见 `JOINT_KEYS`。
"""
from __future__ import annotations

import math

import bpy
from mathutils import Euler, Vector

BODY_H: float = 1.70
HIP_Z: float = 0.90
SHOULDER_X: float = 0.21   # 肩关节横向位置；躯干半宽约 0.18，肩球与上臂由此露在躯干外
THUMB_SPLAY_DEG: float = -42.0   # 拇指向掌侧张开的静默角；乘 sx 镜像到另一只手
ARM_L1: float = 0.30       # 肩枢纽 → 肘枢纽
ARM_L2: float = 0.30       # 肘枢纽 → 手枢纽
LEG_L1: float = 0.46       # 胯枢纽 → 膝枢纽
LEG_L2: float = 0.42       # 膝枢纽 → 踝枢纽

# ---------------------------------------------------------------- 手型
#
# 手型是这套 proxy 最要紧的部分，不是装饰：「两手都是道家剑指、掌心蜷握、指缝间没有
# 任何东西」这句 prompt 要说明的是**这只手物理上握不住剑柄**。手若只是一块扁板，这条
# 信息在参考视频里等于没有，模型照样把剑塞回手里。
#
# 每根手指三节，(掌指关节, 近指间关节, 远指间关节) 各一个 rot_x，正角＝蜷向掌心；
# 拇指两节。三节比两节多出来的是**蜷握时指尖真的扣回掌心**——两节只能折成直角。

HAND_RELAX = {
    "idx": (16, 20, 15), "mid": (18, 23, 17), "rng": (20, 25, 18), "lit": (22, 27, 20),
    "thb": (10, 14),
}
HAND_SWORD_FINGER = {   # 道家剑指（follow-up 061：**任何手指都不弯曲**——蜷指在代理网格上
    # 渲染成「鬼爪」）：食中并拢伸直，无名/小指/拇指也全部伸直放平，只靠并拢角区分二指。
    "idx": (0, 0, 0), "mid": (0, 0, 0), "rng": (0, 0, 0), "lit": (0, 0, 0),
    "thb": (0, 0),
    # 侧向并拢角（度，绕第一节的 Y 轴、自动按左右手镜像）。实测校准（follow-up 059-2）：
    # 两指给**同向近似同角**才平行并拢——腕关节以中指对齐后食中之间有 ~24° 的静默扇形张角，
    # idx≈19/mid≈17 把两根都摆到掌心正前方且互相贴住；同角异号会把两指越推越开。
    "close": {"idx": 19, "mid": 17},
}
HAND_SEAL_WRAP = {      # 掐诀里「握人」的那只手（follow-up 043：两手都伸二指；061：全部伸直不蜷）
    "idx": (0, 0, 0), "mid": (0, 0, 0), "rng": (0, 0, 0), "lit": (0, 0, 0),
    "thb": (0, 0),
    "close": {"idx": 19, "mid": 17},
}
HAND_GRIP = {           # 握住葫芦 / 剑柄：五指合拢扣回掌心
    "idx": (78, 82, 62), "mid": (82, 84, 64), "rng": (84, 86, 66), "lit": (86, 88, 68),
    "thb": (44, 42),
}

JOINT_KEYS: tuple[str, ...] = (
    "pelvis", "neck", "head",
    "clavicleL", "shoulderL", "elbowL", "handL", "hipL", "kneeL", "ankleL", "ballL",
    "clavicleR", "shoulderR", "elbowR", "handR", "hipR", "kneeR", "ankleR", "ballR",
)

_FINGER_LAYOUT = (
    ("idx", 0.029, (0.037, 0.026, 0.020), (0.0106, 0.0090, 0.0077)),
    ("mid", 0.0097, (0.040, 0.028, 0.021), (0.0110, 0.0093, 0.0079)),
    ("rng", -0.0097, (0.036, 0.025, 0.019), (0.0103, 0.0087, 0.0075)),
    ("lit", -0.028, (0.029, 0.020, 0.016), (0.0092, 0.0078, 0.0067)),
)


# ---------------------------------------------------------------- 反解

def _arm_hand_pos(shoulder: Vector, tx: float, ty: float, tz: float, te: float) -> Vector:
    """正向运动学，与 Blender 的 Euler XYZ 合成方式一致（R = Rz·Ry·Rx）。

    tz ＝ 肩的第三分量 ＝ **上臂绕自身长轴的旋转（肱骨内外旋）**。它不改变肘的
    位置，但决定**肘弯发生在哪个平面** —— 缺了它，解算器只能靠横抬大臂来把手
    送到胸前，肘尖被顶成水平外翻（follow-up 059 的「鸡翅膀」根因）。
    """
    r_sh = Euler((math.radians(tx), math.radians(ty), math.radians(tz)), "XYZ").to_matrix()
    r_el = Euler((math.radians(te), 0.0, 0.0), "XYZ").to_matrix()
    down = Vector((0.0, 0.0, -1.0))
    elbow = shoulder + (r_sh @ down) * ARM_L1
    return elbow + ((r_sh @ r_el) @ down) * ARM_L2


def elbow_pos(shoulder: Vector, tx: float, ty: float) -> Vector:
    r_sh = Euler((math.radians(tx), math.radians(ty), 0.0), "XYZ").to_matrix()
    return shoulder + (r_sh @ Vector((0.0, 0.0, -1.0))) * ARM_L1


def elbow_flare_deg(shoulder: Vector, tx: float, ty: float, sx: float) -> float:
    """肘外张角：0°＝肘尖垂直垂在肩下（贴身），90°＝肘尖水平外顶；负＝向身体中线里夹。

    这是用户直觉里「肘向里拐还是向外拐、多大幅度」的那个量（follow-up 059），
    也是解算器的软目标：位置够得到的解有无数个，按这个角挑最像人的那一个。
    """
    el = elbow_pos(shoulder, tx, ty)
    lateral = (el.x - shoulder.x) * sx          # 向体外为正
    drop = shoulder.z - el.z                    # 肘垂在肩下为正
    return math.degrees(math.atan2(lateral, max(drop, 1e-6)))


_FLARE_WEIGHT = 0.0018   # 每偏离 1° 计价 1.8mm 位置误差；25° 偏差 ≈ 4.5cm —— 软而不霸道


def _cost(shoulder: Vector, target: Vector, sx: float,
          tx: float, ty: float, tz: float, te: float, flare: float) -> float:
    """位置误差 + 解剖惩罚 + 肘外张角软目标。

    纯 FK 不知道躯干在哪：不加惩罚时解算器会给出「上臂横穿胸膛、肘落在身体中线」
    这种数学上完美、人体上不可能的解。硬惩罚两条：① 肘必须留在本侧体外；② 肘不许
    绕到背后；③ 肘不许抬过肩。软目标一条：肘外张角尽量贴 `flare`（用户可配）。
    """
    d = (_arm_hand_pos(shoulder, tx, ty, tz, te) - target).length
    el = elbow_pos(shoulder, tx, ty)
    pen = 0.0
    side_x = (el.x - shoulder.x) * sx + shoulder.x * sx
    if side_x < 0.13:
        pen += (0.13 - side_x) * 6.0
    if el.y > 0.10:      # +Y ＝ 身后
        pen += (el.y - 0.10) * 6.0
    if el.z > shoulder.z - 0.02:   # 肘高过肩＝耸成鸡翅膀
        pen += (el.z - (shoulder.z - 0.02)) * 4.0
    pen += abs(elbow_flare_deg(shoulder, tx, ty, sx) - flare) * _FLARE_WEIGHT
    return d + pen


def solve_arm(shoulder: Vector, target: Vector, *, flare: float = 20.0) -> tuple[float, float, float, float]:
    """反解 (肩x, 肩y, 肩twist, 肘弯)，单位度。粗扫一遍，再逐级细化。

    `flare`＝期望肘外张角（0 贴身垂下 / 正向外拐 / 负向里夹），见 elbow_flare_deg。
    粗扫必须覆盖整圈：肩 rot_y 的最优解可落在 ±90° 之外；twist 粗扫五档、细化时连续。
    """
    sx = 1.0 if shoulder.x >= 0.0 else -1.0
    best = (1e9, 0.0, 0.0, 0.0, 0.0)
    for tx in range(-180, 95, 6):
        for ty in range(-180, 185, 6):
            for tz in (-70, -35, 0, 35, 70):
                for te in range(-170, 10, 6):
                    c = _cost(shoulder, target, sx, tx, ty, tz, te, flare)
                    if c < best[0]:
                        best = (c, float(tx), float(ty), float(tz), float(te))
    for step in (3.0, 1.0, 0.25):
        improved = True
        while improved:
            improved = False
            for dx in (-step, 0.0, step):
                for dy in (-step, 0.0, step):
                    for dz in (-step, 0.0, step):
                        for de in (-step, 0.0, step):
                            cand = (best[1] + dx, best[2] + dy, best[3] + dz, best[4] + de)
                            c = _cost(shoulder, target, sx, *cand, flare)
                            if c < best[0] - 1e-6:
                                best = (c, *cand)
                                improved = True
    return best[1], best[2], best[3], best[4]


def solve_report(shoulder: Vector, target: Vector, sol: tuple[float, float, float, float]) -> str:
    """反解的自检行。**误差、肘位置、肘外张角必须打进建场日志** —— 否则「解出来了
    但不对」（手停在半空、鸡翅膀肘）只能靠肉眼看渲染图撞见。"""
    err = (_arm_hand_pos(shoulder, *sol) - target).length
    el = elbow_pos(shoulder, sol[0], sol[1])
    sx = 1.0 if shoulder.x >= 0.0 else -1.0
    fl = elbow_flare_deg(shoulder, sol[0], sol[1], sx)
    return (f"角度={tuple(round(v, 1) for v in sol)} 手位误差={err * 1000:.0f}mm "
            f"肘={tuple(round(v, 2) for v in el)} 肘外张={fl:.0f}°")


# ---------------------------------------------------------------- 建模

# ---------------------------------------------------------------- 腿部反解
#
# 与 solve_arm 同构，但约束不同：膝**只能向后弯**（tk ≥ 0），而肘可以向多个方向；
# 腿还要守「膝不越体中线」。缺了腿部反解，「脚踩在石阶上／踩在悬空的剑上」这类
# 接触点只能靠试角度，而接触点恰恰是戏眼所在。

def _leg_foot_pos(hip: Vector, tx: float, ty: float, tz: float, tk: float) -> Vector:
    """正向运动学，合成方式同 _arm_hand_pos（R = Rz·Ry·Rx）。tz ＝ 大腿绕自身长轴的旋转。"""
    r_hip = Euler((math.radians(tx), math.radians(ty), math.radians(tz)), "XYZ").to_matrix()
    r_kn = Euler((math.radians(tk), 0.0, 0.0), "XYZ").to_matrix()
    down = Vector((0.0, 0.0, -1.0))
    knee = hip + (r_hip @ down) * LEG_L1
    return knee + ((r_hip @ r_kn) @ down) * LEG_L2


def knee_pos(hip: Vector, tx: float, ty: float) -> Vector:
    r_hip = Euler((math.radians(tx), math.radians(ty), 0.0), "XYZ").to_matrix()
    return hip + (r_hip @ Vector((0.0, 0.0, -1.0))) * LEG_L1


def knee_flare_deg(hip: Vector, tx: float, ty: float, sx: float) -> float:
    """膝外张角：0°＝膝垂直垂在胯下，正＝膝向体外撇（外八），负＝向内夹（内八）。"""
    kn = knee_pos(hip, tx, ty)
    lateral = (kn.x - hip.x) * sx
    drop = hip.z - kn.z
    return math.degrees(math.atan2(lateral, max(drop, 1e-6)))


def _leg_cost(hip: Vector, target: Vector, sx: float,
              tx: float, ty: float, tz: float, tk: float, flare: float) -> float:
    d = (_leg_foot_pos(hip, tx, ty, tz, tk) - target).length
    kn = knee_pos(hip, tx, ty)
    pen = 0.0
    if kn.x * sx < 0.015:            # 膝越过体中线＝两腿绞在一起
        pen += (0.015 - kn.x * sx) * 6.0
    if kn.z > hip.z - 0.02:          # 膝高过胯＝把大腿抬成水平以上，弓步/跺脚用不到
        pen += (kn.z - (hip.z - 0.02)) * 4.0
    pen += abs(knee_flare_deg(hip, tx, ty, sx) - flare) * _FLARE_WEIGHT
    return d + pen


def solve_leg(hip: Vector, target: Vector, *, flare: float = 6.0) -> tuple[float, float, float, float]:
    """反解 (胯x, 胯y, 大腿twist, 膝弯)，单位度。target ＝ 踝枢纽要到达的位置。

    `flare`＝期望膝外张角（默认 6°，人站立时膝略外）。膝弯 tk 只扫 0..174：
    膝向前弯是反关节，previz 里出现一次，模型就会照着学。
    """
    sx = 1.0 if hip.x >= 0.0 else -1.0
    best = (1e9, 0.0, 0.0, 0.0, 0.0)
    for tx in range(-150, 65, 6):
        for ty in range(-70, 75, 6):
            for tz in (-30, 0, 30):
                for tk in range(0, 175, 6):
                    c = _leg_cost(hip, target, sx, tx, ty, tz, tk, flare)
                    if c < best[0]:
                        best = (c, float(tx), float(ty), float(tz), float(tk))
    for step in (3.0, 1.0, 0.25):
        improved = True
        while improved:
            improved = False
            for dx in (-step, 0.0, step):
                for dy in (-step, 0.0, step):
                    for dz in (-step, 0.0, step):
                        for dk in (-step, 0.0, step):
                            cand = (best[1] + dx, best[2] + dy, best[3] + dz,
                                    max(0.0, best[4] + dk))
                            c = _leg_cost(hip, target, sx, *cand, flare)
                            if c < best[0] - 1e-6:
                                best = (c, *cand)
                                improved = True
    return best[1], best[2], best[3], best[4]


def solve_leg_report(hip: Vector, target: Vector, sol: tuple[float, float, float, float]) -> str:
    err = (_leg_foot_pos(hip, *sol) - target).length
    sx = 1.0 if hip.x >= 0.0 else -1.0
    kn = knee_pos(hip, sol[0], sol[1])
    return (f"角度={tuple(round(v, 1) for v in sol)} 踝位误差={err * 1000:.0f}mm "
            f"膝=({kn.x:.2f}, {kn.y:.2f}, {kn.z:.2f}) 膝外张={knee_flare_deg(hip, sol[0], sol[1], sx):.0f}°")


class PrevizRig:
    def __init__(self, link, body, skin, limb_end) -> None:
        self._link = link
        self.body = body
        self.skin = skin
        self.limb_end = limb_end

    # -------------------------------------------------------------- 原语

    def _finish(self, ob, material, parent, do_smooth: bool = True):
        ob.data.materials.append(material)
        if do_smooth:
            self._smooth(ob)
        self._link(ob)
        if parent is not None:
            self._setpar(ob, parent)
        return ob

    @staticmethod
    def _setpar(child, parent) -> None:
        bpy.context.view_layer.update()
        child.parent = parent
        child.matrix_parent_inverse = parent.matrix_world.inverted()

    @staticmethod
    def _smooth(ob) -> None:
        """按角度自动平滑。低面数圆柱不平滑会露出明显的棱面带、读成塑料玩具；
        平滑后同样的面数就撑得起「有体积的肢体」，细微的转腕/屈指才看得出来。"""
        prev = bpy.context.view_layer.objects.active
        bpy.context.view_layer.objects.active = ob
        ob.select_set(True)
        try:
            bpy.ops.object.shade_auto_smooth(angle=math.radians(50.0))
        except (AttributeError, RuntimeError, TypeError):
            try:
                bpy.ops.object.shade_smooth()
            except RuntimeError:
                pass
        ob.select_set(False)
        if prev is not None:
            bpy.context.view_layer.objects.active = prev

    def empty(self, name: str, loc: Vector, parent=None):
        bpy.ops.object.empty_add(type="PLAIN_AXES", radius=0.08, location=loc)
        e = bpy.context.object
        e.name = name
        self._link(e)
        if parent is not None:
            self._setpar(e, parent)
        return e

    def sphere(self, name, r, loc, material, parent=None, segs=24, rings=14):
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=r, segments=segs, ring_count=rings, location=loc
        )
        ob = bpy.context.object
        ob.name = name
        return self._finish(ob, material, parent)

    def frustum(self, name, r_bottom, r_top, h, loc, material, parent=None, flatten_y=1.0):
        """带收分的圆台，可在 Y 向压扁成椭圆截面。

        躯干用方块会读成一块板 —— 肩胸与腰没有分界、上臂整个埋进去，胳膊看不出是
        独立肢体。圆台上下不同径 + 压扁成人体的「宽而薄」截面，同样的面数就自然得多。
        """
        bpy.ops.mesh.primitive_cone_add(
            radius1=r_bottom, radius2=r_top, depth=h, vertices=32, location=loc
        )
        ob = bpy.context.object
        ob.name = name
        ob.scale = (1.0, flatten_y, 1.0)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        return self._finish(ob, material, parent)

    def box(self, name, size, loc, material, parent=None):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
        ob = bpy.context.object
        ob.name = name
        ob.scale = Vector(size)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        return self._finish(ob, material, parent, do_smooth=False)

    def limb(self, name, r_top, r_bot, length, top, material, parent=None, joint_r=None):
        """一节收分的肢体：自 `top` 向下 `length`，上粗下细，顶端配一颗关节球。

        直圆柱拼出来的胳膊在弯折处会露断口，且上下等粗像根管子。收分 + 关节球之后
        肩/肘/腕、髋/膝/踝都有实体，肢体的细微转动才有可读的形体变化。
        """
        ob = self.frustum(
            name, r_bot, r_top, length, top + Vector((0.0, 0.0, -length / 2.0)),
            material, parent,
        )
        self.sphere(f"{name}_j", joint_r if joint_r is not None else r_top * 1.06,
                    top, material, parent)
        return ob

    # -------------------------------------------------------------- 手

    def _finger(self, tag, root_at, parent, joints, segs, radii) -> None:
        """一根多节手指：每节一个可转的枢纽 + 一段收分指骨 + 一颗指节球，末端补指尖球。

        指节球是关键：没有它，相邻两节在弯折处会露出两个圆管的断口，蜷指看起来像
        折断的吸管；有了球，屈指的每一节都读得出是关节在转。
        """
        z = root_at.z
        prev = parent
        for i, (seg_len, r) in enumerate(zip(segs, radii), start=1):
            joint = self.empty(f"PVZ_{tag}{i}", Vector((root_at.x, root_at.y, z)), prev)
            self.limb(f"PVZ_{tag}{i}m", r, r * 0.86, seg_len,
                      Vector((root_at.x, root_at.y, z)), self.limb_end, joint, joint_r=r * 1.15)
            joints[f"{tag}{i}"] = joint
            prev = joint
            z -= seg_len
        self.sphere(f"PVZ_{tag}_tip", radii[-1] * 0.88, Vector((root_at.x, root_at.y, z)),
                    self.limb_end, prev, segs=14, rings=9)

    def build_hand(self, side, sx, wrist, parent, joints) -> None:
        """掌 + 四指各三节 + 拇指两节，逐节可摆。"""
        self.sphere(f"PVZ_hand{side}_wrist", 0.030, wrist, self.limb_end, parent,
                    segs=18, rings=11)
        self.frustum(f"PVZ_hand{side}_palm", 0.043, 0.047, 0.086,
                     wrist + Vector((0, 0, -0.045)), self.limb_end, parent, flatten_y=0.42)
        for name, off_x, segs, radii in _FINGER_LAYOUT:
            self._finger(f"hand{side}_{name}", wrist + Vector((off_x * sx, 0, -0.086)),
                         parent, joints, segs, radii)
        th1 = self.empty(f"PVZ_hand{side}_thb1",
                         wrist + Vector((0.042 * sx, -0.010, -0.042)), parent)
        th1.rotation_euler = Euler((0.0, math.radians(THUMB_SPLAY_DEG * sx), 0.0))
        self.limb(f"PVZ_hand{side}_thb1m", 0.0128, 0.0110, 0.037,
                  wrist + Vector((0.042 * sx, -0.010, -0.042)), self.limb_end, th1,
                  joint_r=0.0140)
        th2 = self.empty(f"PVZ_hand{side}_thb2",
                         wrist + Vector((0.042 * sx, -0.010, -0.079)), th1)
        self.limb(f"PVZ_hand{side}_thb2m", 0.0108, 0.0090, 0.029,
                  wrist + Vector((0.042 * sx, -0.010, -0.079)), self.limb_end, th2,
                  joint_r=0.0118)
        self.sphere(f"PVZ_hand{side}_thb_tip", 0.0088,
                    wrist + Vector((0.042 * sx, -0.010, -0.108)), self.limb_end, th2,
                    segs=14, rings=9)
        joints[f"hand{side}_thb1"] = th1
        joints[f"hand{side}_thb2"] = th2

    # -------------------------------------------------------------- 整体

    def build(self, origin: Vector) -> tuple[object, object, dict]:
        """在 `origin`（脚下地面点）建一具人形，返回 (root, pelvis, joints)。"""
        root = self.empty("PVZ_root", origin)
        pelvis = self.empty("PVZ_pelvis", origin + Vector((0, 0, HIP_Z)), root)

        self.frustum("PVZ_hips", 0.160, 0.145, 0.26, origin + Vector((0, 0, HIP_Z + 0.11)),
                     self.body, pelvis, flatten_y=0.72)
        self.frustum("PVZ_chest", 0.145, 0.195, 0.32, origin + Vector((0, 0, HIP_Z + 0.40)),
                     self.body, pelvis, flatten_y=0.70)
        clavicles: dict = {}
        for sgn, tag in ((1.0, "L"), (-1.0, "R")):
            # 锁骨关节：肩球与整条手臂都挂在它下面。没有它就做不出耸肩、含胸、探肩。
            cl = self.empty(f"PVZ_clavicle{tag}",
                            origin + Vector((SHOULDER_X * sgn * 0.32, 0, HIP_Z + 0.46)), pelvis)
            clavicles[tag] = cl
            self.sphere(f"PVZ_shoulder{tag}_ball", 0.075,
                        origin + Vector((SHOULDER_X * sgn, 0, HIP_Z + 0.46)), self.body, cl)
        # 颈关节：颈段与头都挂在它下面。原先颈只是挂在 pelvis 上的一段静态几何，
        # 脖子不会弯、头只能整块转——「回头看」「仰头」全靠 head 一个关节硬掰。
        neck_j = self.empty("PVZ_neck_j", origin + Vector((0, 0, HIP_Z + 0.53)), pelvis)
        self.frustum("PVZ_neck", 0.052, 0.052, 0.10, origin + Vector((0, 0, HIP_Z + 0.58)),
                     self.body, neck_j)
        head_j = self.empty("PVZ_head_j", origin + Vector((0, 0, HIP_Z + 0.62)), neck_j)
        self.sphere("PVZ_head", 0.112, origin + Vector((0, 0, HIP_Z + 0.73)), self.skin, head_j)
        # 发髻：给头一个不对称顶饰，正/背/侧一眼分得开，朝向不会读反
        self.sphere("PVZ_topknot", 0.050, origin + Vector((0, 0.038, HIP_Z + 0.85)),
                    self.body, head_j)

        joints: dict = {"pelvis": pelvis, "neck": neck_j, "head": head_j}
        for side, sx in (("L", 1.0), ("R", -1.0)):
            arm_x = SHOULDER_X * sx
            sh = self.empty(f"PVZ_shoulder{side}",
                            origin + Vector((arm_x, 0, HIP_Z + 0.46)), clavicles[side])
            self.limb(f"PVZ_upperarm{side}", 0.053, 0.042, 0.30,
                      origin + Vector((arm_x, 0, HIP_Z + 0.46)), self.body, sh, joint_r=0.058)
            el = self.empty(f"PVZ_elbow{side}", origin + Vector((arm_x, 0, HIP_Z + 0.16)), sh)
            self.limb(f"PVZ_forearm{side}", 0.043, 0.032, 0.30,
                      origin + Vector((arm_x, 0, HIP_Z + 0.16)), self.body, el, joint_r=0.048)
            hd = self.empty(f"PVZ_hand{side}", origin + Vector((arm_x, 0, HIP_Z - 0.14)), el)
            self.build_hand(side, sx, origin + Vector((arm_x, 0, HIP_Z - 0.14)), hd, joints)

            leg_x = 0.11 * sx
            hip = self.empty(f"PVZ_hip{side}", origin + Vector((leg_x, 0, HIP_Z)), root)
            self.limb(f"PVZ_thigh{side}", 0.085, 0.064, 0.46,
                      origin + Vector((leg_x, 0, HIP_Z)), self.body, hip, joint_r=0.090)
            kn = self.empty(f"PVZ_knee{side}", origin + Vector((leg_x, 0, HIP_Z - 0.46)), hip)
            self.limb(f"PVZ_shin{side}", 0.064, 0.040, 0.42,
                      origin + Vector((leg_x, 0, HIP_Z - 0.46)), self.body, kn, joint_r=0.070)
            ank = self.empty(f"PVZ_ankle{side}", origin + Vector((leg_x, 0, HIP_Z - 0.88)), kn)
            self.sphere(f"PVZ_ankle{side}_ball", 0.042,
                        origin + Vector((leg_x, 0, HIP_Z - 0.88)), self.limb_end, ank,
                        segs=18, rings=11)
            # 脚：脚跟 + 前掌两段 —— 一块方砖读不出脚尖朝哪、也读不出踮/落
            self.box(f"PVZ_heel{side}", (0.092, 0.075, 0.062),
                     origin + Vector((leg_x, 0.020, 0.031)), self.limb_end, ank)
            # 前脚掌关节（足弓）：绕它转＝踮脚／脚跟离地／蹬地。
            # 枢纽必须落在**跖趾关节**上。实测 MPFB default 骨架（2026-08-25）：
            # 五根 toe*-1 的骨头位于踝前方 y=-0.135±0.008、离地 z≈0.027，
            # 而踝（foot.L）在 y=-0.002。把枢纽估在 -0.030 会让脚绕一个远在后方
            # 10cm 的轴转，抬脚跟时脚趾直接扎进地面（实测穿插根因）。
            ball = self.empty(f"PVZ_ball{side}", origin + Vector((leg_x, -0.130, 0.028)), ank)
            fore = self.frustum(f"PVZ_forefoot{side}", 0.048, 0.052, 0.185,
                                origin + Vector((leg_x, -0.078, 0.030)), self.limb_end, ball)
            fore.rotation_euler = Euler((math.radians(90), 0, 0))

            joints[f"shoulder{side}"] = sh
            joints[f"elbow{side}"] = el
            joints[f"hand{side}"] = hd
            joints[f"clavicle{side}"] = clavicles[side]
            joints[f"hip{side}"] = hip
            joints[f"knee{side}"] = kn
            joints[f"ankle{side}"] = ank
            joints[f"ball{side}"] = ball
        return root, pelvis, joints

    # -------------------------------------------------------------- 摆姿

    @staticmethod
    def hand_pose(joints: dict, side: str, frame: int, spec: dict) -> None:
        sx = 1.0 if side == "L" else -1.0
        close: dict = spec.get("close", {})
        for finger, angles in spec.items():
            if finger == "close":
                continue
            # 拇指的外张是它的静默姿态，K 帧时必须一起写回 —— 只写 rot_x 会把外张
            # 抹掉，拇指与四指并成一排，剑指的「拇指压住蜷起的指节」直接消失。
            splay = math.radians(THUMB_SPLAY_DEG * sx) if finger == "thb" else 0.0
            if finger in close:
                # 食中并拢：绕第一节 Y 轴的侧向角（正=向中指靠，按左右手镜像）
                splay = math.radians(close[finger] * sx)
            for i, deg in enumerate(angles, start=1):
                key = f"hand{side}_{finger}{i}"
                if key in joints:
                    j = joints[key]
                    j.rotation_euler = Euler(
                        (math.radians(deg), splay if i == 1 else 0.0, 0.0)
                    )
                    j.keyframe_insert("rotation_euler", frame=frame)

    def both_hands(self, joints: dict, frame: int, spec: dict) -> None:
        self.hand_pose(joints, "L", frame, spec)
        self.hand_pose(joints, "R", frame, spec)
