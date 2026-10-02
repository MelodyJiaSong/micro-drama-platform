# shot16 后处理钩子（S 档）：由 tools/previz/build_previz.py 在建完人与道具之后执行，共享引擎的全局名字空间。
# 只管本镜的手持物件与光：杜克的钢盾（绑在左前臂）、背上的祖父圆木盾、他 9.8–19s 举过亚伦头顶的蜡烛、亚伦的单手练习锤
# （9s 前右手握，之后挂在腰带左侧）、父亲的旧锤（17.4s 前在小矿工怀里＝平面图 [[prop]]，之后双手抱起、18.7s 扛上右肩）、
# 矿工胸口炸开的两团光（审判，亚伦从杜克肩后一指）。时刻与 shot16.md `动作:`、overhead 的 [[hit]] / [[cast]] 逐拍对齐（follow-up 052：人体一律 Cascadeur）。

STEEL = (0.55, 0.85, 0.04)           # 竖长十边形钢盾：宽 × 高 × 厚
WOOD_R, WOOD_T = 0.36, 0.05          # 祖父的圆木盾（背在背后）
PRACT_L, HAMMER_L = 0.5, 1.2         # 单手练习锤 / 父亲的旧双手锤
HANG = 9.0                           # 练习锤挂回腰上
TAKE = 17.4                          # 小矿工松手，亚伦把父亲的锤抱起来
CANDLE = (9.8, 19.0)                 # 杜克举着那根蜡烛
BURST = cast_windows("亚伦", ("effect",), "k202")
# 审判：目标胸口炸开的一团光（技能卡 k202 effect，没有飞行物、不叫回——053）；时刻按技能卡（[[施法]]，follow-up 065）

from mathutils import Matrix  # noqa: E402

duke = ACTORS["杜克"]["armature"]
aaron = ACTORS["亚伦"]["armature"]
kob = ACTORS["矿工（一次只上一只）"]["root"]


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


def _in_hand(ob, fr, arm, length, side):
    """两手靠在一起时柄 ＝ 两前臂平均指向，分开时顺着右前臂（shot05 / shot11 同一约定）。"""
    hr, hl = _bone(arm, "hand_r"), _bone(arm, "hand_l")
    if (hr - hl).length < 0.4:
        d = ((hr - _bone(arm, "forearm_r")) + (hl - _bone(arm, "forearm_l"))).normalized()
        grip = (hr + hl) / 2
    else:
        d = (hr - _bone(arm, "forearm_r")).normalized()
        grip = hr
    _orient(ob, fr, grip + d * (length * 0.30), d, side if abs(d.dot(side)) < 0.95 else Vector((0, 0, 1)))


LIGHT = mat("PREVIZ_光", (1.0, 0.82, 0.30), 8.0)
steel = box("杜克_盾", STEEL, (0, 0, 0), _mat_for("白"))                    # 局部 Z ＝ 盾面法线，局部 Y ＝ 盾的长边
boss = sphere("杜克_盾心", 0.06, (0, 0, 0), _mat_for("红"))
attach(boss, steel, (0, 0, STEEL[2] / 2 + 0.03))
wood = cyl("杜克_背盾", WOOD_R, WOOD_T, (0, 0, 0), _mat_for("褐"))
candle = cyl("杜克_蜡烛", 0.02, 0.15, (0, 0, 0), _mat_for("白"))
flame = sphere("杜克_烛火", 0.03, (0, 0, 0), LIGHT)
pract = cyl("亚伦_锤柄", 0.015, PRACT_L, (0, 0, 0), _mat_for("褐"))           # 局部 Z ＝ 柄向，原点在柄中点
phead = box("亚伦_锤头", (0.1, 0.07, 0.07), (0, 0, 0), _mat_for("深灰"))
attach(phead, pract, (0, 0, PRACT_L / 2))
old = cyl("亚伦_旧锤柄", 0.018, HAMMER_L, (0, 0, 0), _mat_for("褐"))
ohead = box("亚伦_旧锤头", (0.16, 0.1, 0.1), (0, 0, 0), _mat_for("深灰"))
attach(ohead, old, (0, 0, HAMMER_L / 2))
orb = sphere("审判的光", 0.16, (0, 0, 0), LIGHT)

pref = bpy.context.preferences.edit
_interp = pref.keyframe_new_interpolation_type
for fr in range(1, f(TOTAL) + 1):
    scene.frame_set(fr)
    t = (fr - 1) / FPS
    dfwd, up, dleft = _frame(duke)
    el, wr = _bone(duke, "forearm_l"), _bone(duke, "hand_l")
    n = -(duke.matrix_world @ duke.pose.bones["forearm_l"].matrix).to_3x3().normalized().col[2]
    _orient(steel, fr, (el + wr) / 2 + n * 0.08, n, (wr - el).normalized())
    chest = (_bone(duke, "arm_l") + _bone(duke, "arm_r")) / 2
    _orient(wood, fr, chest - dfwd * 0.2 - up * 0.25, -dfwd, up)
    lit = CANDLE[0] <= t <= CANDLE[1]
    candle.location = _bone(duke, "hand_r") + up * 0.08
    candle.keyframe_insert("location", frame=fr)
    flame.location = candle.location + up * 0.11
    flame.keyframe_insert("location", frame=fr)
    _scale(candle, fr, 1.0 if lit else 0.0)
    _scale(flame, fr, 1.0 if lit else 0.0)
    afwd, aup, aleft = _frame(aaron)
    if t < HANG:
        _in_hand(pract, fr, aaron, PRACT_L, aleft)
    else:            # 挂在腰带左侧（item.toml [carry] 挂腰）
        hip = _bone(aaron, "thigh_l") + aleft * 0.12 + Vector((0, 0, 0.05))
        _orient(pract, fr, hip - aup * (PRACT_L / 2 - 0.05), -aup, afwd)
    if t >= TAKE:
        _in_hand(old, fr, aaron, HAMMER_L, aleft)
        _scale(old, fr, 1.0)
    else:
        _scale(old, fr, 0.0)
    pref.keyframe_new_interpolation_type = "LINEAR"
    if any(a <= t <= b for a, b in BURST):
        orb.location = kob.matrix_world.translation + Vector((0, 0, 0.55))
        _scale(orb, fr, 1.0)
    else:
        _scale(orb, fr, 0.0)
    orb.keyframe_insert("location", frame=fr)
    pref.keyframe_new_interpolation_type = _interp
scene.frame_set(1)
print("  后处理：钢盾 / 背上圆木盾 / 蜡烛 / 练习锤 / 父亲的旧锤逐帧挂上；审判的光按时刻表在矿工胸口炸开")
