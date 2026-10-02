# shot15 后处理钩子（S 档）：由 tools/previz/build_previz.py 在建完人与道具之后执行，共享引擎的全局名字空间。
# 两人是 Cascadeur 体，手持物件由这里逐帧挂到骨骼上：杜克的竖长钢盾（左前臂，「杜克_盾」——挨棒与 8.7s 盾沿一磕都按它量）、
# 亚伦父亲的旧双手锤（0–7.2s 右手握柄中段拄地；7.2–13.3s 双手握，8.1s 一锤砸在监工左肩，「亚伦_锤头」按它量；13.3s 起又拄地），
# 审判的光（技能卡 k202 effect：4.6s 起手、5.4–5.9s 监工胸口炸开一团，没有飞行物）。鬣狗人监工的钉刺木棒是色块人偶的持物。

STEEL = (0.55, 0.85, 0.04)           # 竖长十边形钢盾：宽 × 高 × 厚（e5205）
HAMMER_L = 1.2                       # 父亲的旧双手锤全长（e5110）
TWO_HAND = (7.2, 13.3)               # 双手握锤的时段（与 shot15.md 本镜状态、choreo 同一组时刻）
BURST = (5.4, 5.9)

from mathutils import Matrix  # noqa: E402

duke = ACTORS["杜克"]["armature"]
aaron = ACTORS["亚伦"]["armature"]
gnoll = ACTORS["鬣狗人监工"]["root"]


def _bone(arm, name):
    return arm.matrix_world @ arm.pose.bones[name].head


def _frame(arm):
    up = Vector((0, 0, 1))
    left = _bone(arm, "arm_l") - _bone(arm, "arm_r")
    return left.cross(up).normalized(), up, left.normalized()


def _orient(ob, frame, loc, axis_z, axis_y):
    z = axis_z.normalized()
    y = (axis_y - z * axis_y.dot(z)).normalized()
    x = y.cross(z)
    ob.rotation_mode = "QUATERNION"
    ob.location = loc
    ob.rotation_quaternion = Matrix((x, y, z)).transposed().to_quaternion()
    ob.keyframe_insert("location", frame=frame)
    ob.keyframe_insert("rotation_quaternion", frame=frame)


def _scale(ob, fr, s):
    ob.scale = (max(s, 1e-4),) * 3
    ob.keyframe_insert("scale", frame=fr)


def _gz(p):
    return ground_z(p.x, p.y) if GROUND else 0.0


def _two_hands(ob, fr, arm, length, side):
    """双手握：柄＝两前臂平均指向，握在两手中点（ep01 shot05 / shot11 同一约定）。"""
    hr, hl = _bone(arm, "hand_r"), _bone(arm, "hand_l")
    d = ((hr - _bone(arm, "forearm_r")) + (hl - _bone(arm, "forearm_l"))).normalized()
    _orient(ob, fr, (hr + hl) / 2 + d * (length * 0.30), d, side if abs(d.dot(side)) < 0.95 else Vector((0, 0, 1)))


def _grounded(ob, fr, arm, length, fwd):
    """单手拄地：右手握柄中段，锤头朝下拄在右脚边。"""
    hand = _bone(arm, "hand_r")
    foot = _bone(arm, "foot_r") + fwd * 0.15
    tip = Vector((foot.x, foot.y, _gz(foot) + 0.06))
    d = (tip - hand).normalized()
    _orient(ob, fr, tip - d * (length / 2), d, fwd)


LIGHT = mat("PREVIZ_光", (1.0, 0.82, 0.30), 8.0)
steel = box("杜克_盾", STEEL, (0, 0, 0), _mat_for("白"))                    # 局部 Z ＝ 盾面法线，局部 Y ＝ 盾的长边
boss = sphere("杜克_盾心", 0.06, (0, 0, 0), _mat_for("红"))
attach(boss, steel, (0, 0, STEEL[2] / 2 + 0.03))
old = cyl("亚伦_锤柄", 0.018, HAMMER_L, (0, 0, 0), _mat_for("褐"))           # 局部 Z ＝ 柄向，原点在柄中点
ohead = box("亚伦_锤头", (0.16, 0.1, 0.1), (0, 0, 0), _mat_for("深灰"))
attach(ohead, old, (0, 0, HAMMER_L / 2))
orb = sphere("审判的光", 0.16, (0, 0, 0), LIGHT)

pref = bpy.context.preferences.edit
_interp = pref.keyframe_new_interpolation_type
for fr in range(1, f(TOTAL) + 1):
    scene.frame_set(fr)
    t = (fr - 1) / FPS
    el, wr = _bone(duke, "forearm_l"), _bone(duke, "hand_l")
    n = -(duke.matrix_world @ duke.pose.bones["forearm_l"].matrix).to_3x3().normalized().col[2]
    _orient(steel, fr, (el + wr) / 2 + n * 0.08, n, (wr - el).normalized())
    afwd, aup, aleft = _frame(aaron)
    if TWO_HAND[0] <= t < TWO_HAND[1]:
        _two_hands(old, fr, aaron, HAMMER_L, aleft)
    else:
        _grounded(old, fr, aaron, HAMMER_L, afwd)
    pref.keyframe_new_interpolation_type = "LINEAR"
    orb.location = gnoll.matrix_world.translation + Vector((0, 0, 1.15))
    orb.keyframe_insert("location", frame=fr)
    _scale(orb, fr, 1.0 if BURST[0] <= t <= BURST[1] else 0.0)
    pref.keyframe_new_interpolation_type = _interp
scene.frame_set(1)
print("  后处理：杜克的钢盾挂左前臂；亚伦的旧锤拄地 / 双手握逐帧挂上；审判的光 5.4–5.9s 在监工胸口炸开")
