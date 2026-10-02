# shot25 后处理钩子（S 档）：由 tools/previz/build_previz.py 在建完人与道具之后执行，共享引擎的全局名字空间。
# 两人是 Cascadeur 体，手持物件由这里逐帧挂到骨骼上：杜克的竖长钢盾（挽在左前臂，名字「杜克_盾」——命中检查按它找盾）、
# 亚伦父亲的旧双手锤（名字「亚伦_锤头」——命中检查按它找锤头）。
# 锤的拿法跟 cascadeur/choreo.toml 的上身部件走：hammer_r_low 段右手提着、锤头拄在右脚边；twohand_* 段双手横握、锤头在身前。
# 时刻与 shot25.md `本镜状态` / `动作:`、overhead 的 [[hit]] 对齐（10s 盾磕丁的矛；12.8s 锤扫甲；13.2 / 13.9s 盾顶丁、丙）。

STEEL = (0.55, 0.85, 0.04)           # 竖长十边形钢盾：宽 × 高 × 厚（e5205：高约 80 cm、宽约 50 cm）
HAMMER_L = 1.2                       # 父亲的旧双手锤全长（e5110）
TWO_HAND = ((3.0, 6.1), (9.9, 13.2))    # 双手握的时段（choreo：twohand_low / twohand_sweep；9.9s 壳散横锤护身）
SWEEP = (12.4, 13.2)                    # 横扫：鱼人只到人胸口，锤头往下压着扫（柄向下倾 ~30°）

from mathutils import Matrix  # noqa: E402

duke = ACTORS["杜克"]["armature"]
aaron = ACTORS["亚伦"]["armature"]


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


def _grounded(ob, fr, arm, length, fwd):
    """右手提锤：右手握柄中段，锤头朝下拄在右脚边。"""
    hand = _bone(arm, "hand_r")
    foot = _bone(arm, "foot_r") + fwd * 0.15
    tip = Vector((foot.x, foot.y, _gz(foot) + 0.06))
    d = (tip - hand).normalized()
    _orient(ob, fr, tip - d * (length / 2), d, fwd)


def _two_hand(ob, fr, arm, length, fwd, down=0.0):
    """双手一前一后横握锤柄，锤头在身前（横扫时跟着两只手走；down＞0 时锤头往下压）。"""
    hl, hr = _bone(arm, "hand_l"), _bone(arm, "hand_r")
    d = hr - hl
    d = d.normalized() if d.length > 0.08 else fwd
    if d.dot(fwd) < 0:
        d = -d
    if down:
        d = (d - Vector((0, 0, down))).normalized()
    base = (hl + hr) / 2 - d * 0.35
    _orient(ob, fr, base + d * (length / 2), d, fwd)


steel = box("杜克_盾", STEEL, (0, 0, 0), _mat_for("白"))                    # 局部 Z ＝ 盾面法线，局部 Y ＝ 盾的长边
boss = sphere("杜克_盾心", 0.06, (0, 0, 0), _mat_for("红"))
attach(boss, steel, (0, 0, STEEL[2] / 2 + 0.03))
old = cyl("亚伦_锤柄", 0.018, HAMMER_L, (0, 0, 0), _mat_for("褐"))           # 局部 Z ＝ 柄向，原点在柄中点
ohead = box("亚伦_锤头", (0.16, 0.1, 0.1), (0, 0, 0), _mat_for("深灰"))
attach(ohead, old, (0, 0, HAMMER_L / 2))

for fr in range(1, f(TOTAL) + 1):
    scene.frame_set(fr)
    t = (fr - 1) / FPS
    el, wr = _bone(duke, "forearm_l"), _bone(duke, "hand_l")
    n = -(duke.matrix_world @ duke.pose.bones["forearm_l"].matrix).to_3x3().normalized().col[2]
    _orient(steel, fr, (el + wr) / 2 + n * 0.08, n, (wr - el).normalized())
    afwd, aup, _ = _frame(aaron)
    if any(a <= t < b for a, b in TWO_HAND):
        _two_hand(old, fr, aaron, HAMMER_L, afwd, 0.6 if SWEEP[0] <= t < SWEEP[1] else 0.0)
    else:
        _grounded(old, fr, aaron, HAMMER_L, afwd)
scene.frame_set(1)
print("  后处理：杜克的钢盾挂左前臂；亚伦的旧锤 3–6.1s、9.9–13.2s 双手横握，其余右手提着拄在脚边，逐帧挂上")
