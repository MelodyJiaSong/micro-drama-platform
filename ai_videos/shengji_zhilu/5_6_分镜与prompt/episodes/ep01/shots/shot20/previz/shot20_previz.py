# shot20 后处理钩子（S 档）：由 tools/previz/build_previz.py 在建完人与道具之后执行，共享引擎的全局名字空间。
# 只管本镜的手持物件：杜克的钢盾（绑在左前臂）、背上的祖父圆木盾（23s 挨一斧、斧刃卡进去）、亚伦父亲的旧锤（15s 前扛右肩，
# 之后双手握，21s 挨踹后右手拖着）、加瑞克的单手阔刃斧（e5113，右手握；23s 起斧刃卡在杜克背上的木盾里）。
# 时刻与 shot20.md `动作:`、overhead 的 [[hit]] 逐拍对齐（follow-up 052：人体一律 Cascadeur）。

STEEL = (0.55, 0.85, 0.04)           # 竖长十边形钢盾：宽 × 高 × 厚
WOOD_R, WOOD_T = 0.36, 0.05          # 祖父的圆木盾（背在背后）
HAMMER_L, AXE_L = 1.2, 0.7           # 父亲的旧双手锤 / 加瑞克的单手阔刃斧
STUCK = 23.0                         # 斧刃劈进背上的木盾、卡住

from mathutils import Matrix  # noqa: E402

duke = ACTORS["杜克"]["armature"]
aaron = ACTORS["亚伦"]["armature"]
gar = ACTORS["加瑞克"]["armature"]


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


steel = box("杜克_盾", STEEL, (0, 0, 0), _mat_for("白"))                    # 局部 Z ＝ 盾面法线，局部 Y ＝ 盾的长边
boss = sphere("杜克_盾心", 0.06, (0, 0, 0), _mat_for("红"))
attach(boss, steel, (0, 0, STEEL[2] / 2 + 0.03))
wood = cyl("杜克_背盾", WOOD_R, WOOD_T, (0, 0, 0), _mat_for("褐"))           # 局部 Z ＝ 盾面法线
ham = cyl("亚伦_锤柄", 0.018, HAMMER_L, (0, 0, 0), _mat_for("褐"))           # 局部 Z ＝ 柄向，原点在柄中点
hhead = box("亚伦_锤头", (0.16, 0.1, 0.1), (0, 0, 0), _mat_for("深灰"))
attach(hhead, ham, (0, 0, HAMMER_L / 2))
axe = cyl("加瑞克_斧柄", 0.02, AXE_L, (0, 0, 0), _mat_for("橙"))
blade = box("加瑞克_斧头", (0.26, 0.04, 0.22), (0, 0, 0), _mat_for("白"))
attach(blade, axe, (0.08, 0, AXE_L / 2 - 0.08))

for fr in range(1, f(TOTAL) + 1):
    scene.frame_set(fr)
    t = (fr - 1) / FPS
    dfwd, up, dleft = _frame(duke)
    el, wr = _bone(duke, "forearm_l"), _bone(duke, "hand_l")
    n = -(duke.matrix_world @ duke.pose.bones["forearm_l"].matrix).to_3x3().normalized().col[2]
    _orient(steel, fr, (el + wr) / 2 + n * 0.08, n, (wr - el).normalized())
    chest = (_bone(duke, "arm_l") + _bone(duke, "arm_r")) / 2
    back_n = (-dfwd + up * 0.6 * max(0.0, (chest - _bone(duke, "pelvis")).normalized().dot(dfwd))).normalized()
    back = chest - dfwd * 0.2 - up * 0.25
    _orient(wood, fr, back, back_n, up)
    _in_hand(ham, fr, aaron, HAMMER_L, _frame(aaron)[2])
    gfwd, gup, gleft = _frame(gar)
    if t < STUCK:
        _in_hand(axe, fr, gar, AXE_L, gleft)
    else:            # 斧刃卡在杜克背上的木盾里：斧头钉在盾面上，柄指向加瑞克的右手
        hr = _bone(gar, "hand_r")
        d = (back + back_n * 0.05 - hr).normalized()
        _orient(axe, fr, back + back_n * 0.05 - d * (AXE_L / 2 - 0.08), d, gleft)
scene.frame_set(1)
print("  后处理：钢盾 / 背上圆木盾 / 父亲的旧锤 / 阔刃斧逐帧挂上（23s 起斧刃卡在木盾里）")
