# shot32 后处理钩子（S 档）：由 tools/previz/build_previz.py 在建完人与道具之后执行，共享引擎的全局名字空间。
# Cascadeur 体的手持物件逐帧挂到骨骼上（名字＝命中检查找的「人_件」）：杜克的钢盾挂左前臂；沃尔特的草叉双手握（1.6–2s 往前一挺）
# 生成器：spawns/shots-d2/scratch/make_hooks2.py（照 ep02 shot25_previz.py 的写法）。

STEEL = (0.55, 0.85, 0.04)           # 竖长十边形钢盾：宽 × 高 × 厚（e5205：高约 80 cm、宽约 50 cm）

from mathutils import Matrix  # noqa: E402


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


def _gz(p):
    return ground_z(p.x, p.y) if GROUND else 0.0


def _two_hand(ob, fr, arm, length, fwd, grip=0.35):
    """双手一前一后握长杆，杆头朝前（叉、斧枪、锤都这么拿）。"""
    hl, hr = _bone(arm, "hand_l"), _bone(arm, "hand_r")
    d = hr - hl
    d = d.normalized() if d.length > 0.08 else fwd
    if d.dot(fwd) < 0:
        d = -d
    base = (hl + hr) / 2 - d * grip
    _orient(ob, fr, base + d * (length / 2), d, fwd)


def _thrust(ob, fr, arm, length, fwd, tilt=0.15, grip=0.45):
    """挺着长杆往前捅 / 往下按：杆顺着身体朝向、略往下斜，双手握在杆后段。"""
    hl, hr = _bone(arm, "hand_l"), _bone(arm, "hand_r")
    d = (fwd - Vector((0, 0, tilt))).normalized()
    base = (hl + hr) / 2 - d * grip
    _orient(ob, fr, base + d * (length / 2), d, Vector((0, 0, 1)) if abs(d.z) < 0.95 else fwd)


def _leaning(ob, fr, arm, length, fwd, left):
    """靠腿：锤头朝下拄在右脚外侧，柄斜靠在右腿上，两手不扶。"""
    foot = _bone(arm, "foot_r") - left * 0.18 + fwd * 0.05
    tip = Vector((foot.x, foot.y, _gz(foot) + 0.06))
    top = _bone(arm, "thigh_r") - left * 0.12
    d = (tip - top).normalized()
    _orient(ob, fr, tip - d * (length / 2), d, fwd)


duke = ACTORS["杜克"]["armature"]
steel = box("杜克_盾", STEEL, (0, 0, 0), _mat_for("白"))                    # 局部 Z ＝ 盾面法线，局部 Y ＝ 盾的长边
boss = sphere("杜克_盾心", 0.06, (0, 0, 0), _mat_for("红"))
attach(boss, steel, (0, 0, STEEL[2] / 2 + 0.03))

fork_arm = ACTORS["沃尔特"]["armature"]
fork = cyl("沃尔特_叉", 0.02, 1.6, (0, 0, 0), _mat_for("褐"))       # 局部 Z ＝ 杆向，原点在杆中点
fork_head = box("沃尔特_叉头", (0.06, 0.2, 0.02), (0, 0, 0), _mat_for("深灰"))
attach(fork_head, fork, (0, 0, 1.6 / 2))

for fr in range(1, f(TOTAL) + 1):
    scene.frame_set(fr)
    t = (fr - 1) / FPS
    el, wr = _bone(duke, "forearm_l"), _bone(duke, "hand_l")
    n = -(duke.matrix_world @ duke.pose.bones["forearm_l"].matrix).to_3x3().normalized().col[2]
    _orient(steel, fr, (el + wr) / 2 + n * 0.08, n, (wr - el).normalized())
    fwd_fork, _u, _l = _frame(fork_arm)
    _thrust(fork, fr, fork_arm, 1.6, fwd_fork, next((k for a, b, k in ((1.6, 2.0, 0.0),) if a <= t < b), 0.15))
scene.frame_set(1)
print("  后处理：杜克的钢盾挂左前臂；沃尔特的草叉双手握（1.6–2s 往前一挺），逐帧挂上")
