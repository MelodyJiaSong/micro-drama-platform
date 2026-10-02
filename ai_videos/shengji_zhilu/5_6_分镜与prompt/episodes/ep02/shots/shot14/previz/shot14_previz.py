# shot14 后处理钩子（S 档）：由 tools/previz/build_previz.py 在建完人与道具之后执行，共享引擎的全局名字空间。
# 两人是 Cascadeur 体，手持物件由这里逐帧挂到骨骼上：杜克的竖长钢盾（挽在左前臂，名字「杜克_盾」——命中检查按它找盾）、
# 亚伦父亲的旧双手锤（0–6.3s 扛在右肩：右手握柄、锤头在肩后；6.2s 右腕挨鞭、锤从肩上滑下来，6.4s 起右手握柄中段、锤头拄在右脚边）。
# 鬣狗人监工左手的长皮鞭（鞭身「鬣狗人监工_鞭身」＋鞭梢「鬣狗人监工_鞭」——鞭梢是 overhead [[hit]] 6.2s 的 obj，命中自检按它量）：平时垂在左手下；2s 半空甩个响；
# 4.8s 扬到身后，5.9–6.35s 抽直、鞭梢落在亚伦右腕上；之后收回垂着。
# 时刻与 shot14.md `本镜状态` / `动作:`、overhead 的 [[hit]] 对齐；鬣狗人监工的钉刺木棒是色块人偶的持物（Shot.previz['carry']）。

STEEL = (0.55, 0.85, 0.04)           # 竖长十边形钢盾：宽 × 高 × 厚（e5205：高约 80 cm、宽约 50 cm）
HAMMER_L = 1.2                       # 父亲的旧双手锤全长（e5110）
LOWER = 6.3                          # 右腕挨鞭，锤从肩上滑下来拄地
CRACK = (1.8, 2.2)                   # 鞭子在半空甩个响
WINDUP = (4.8, 5.9)                  # 扬鞭
LASH = (5.9, 6.35)                   # 抽直、鞭梢落在亚伦右腕护腕上

from mathutils import Matrix  # noqa: E402

duke = ACTORS["杜克"]["armature"]
aaron = ACTORS["亚伦"]["armature"]
gnoll = ACTORS["鬣狗人监工"]["root"]
GH = ACTORS["鬣狗人监工"]["height"]


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


def _shoulder(ob, fr, arm, length, fwd, up):
    """扛肩：右手握柄，柄往后上斜搭过右肩，锤头在肩后。"""
    hand = _bone(arm, "hand_r")
    top = _bone(arm, "arm_r") - fwd * 0.22 + up * 0.08
    d = (top - hand).normalized()
    _orient(ob, fr, hand + d * (length * 0.30), d, fwd)


def _grounded(ob, fr, arm, length, fwd):
    """单手拄地：右手握柄中段，锤头朝下拄在右脚边。"""
    hand = _bone(arm, "hand_r")
    foot = _bone(arm, "foot_r") + fwd * 0.15
    tip = Vector((foot.x, foot.y, _gz(foot) + 0.06))
    d = (tip - hand).normalized()
    _orient(ob, fr, tip - d * (length / 2), d, fwd)


steel = box("杜克_盾", STEEL, (0, 0, 0), _mat_for("白"))                    # 局部 Z ＝ 盾面法线，局部 Y ＝ 盾的长边
boss = sphere("杜克_盾心", 0.06, (0, 0, 0), _mat_for("红"))
attach(boss, steel, (0, 0, STEEL[2] / 2 + 0.03))
whip = cyl("鬣狗人监工_鞭身", 0.012, 1.0, (0, 0, 0), _mat_for("褐"))     # 局部 Z ＝ 鞭身方向，原点在中点，长度靠 Z 缩放
lash = sphere("鬣狗人监工_鞭", 0.035, (0, 0, 0), _mat_for("褐"))          # 鞭梢：命中自检量它的中心（与锤头同一口径）
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
    if t < LOWER:
        _shoulder(old, fr, aaron, HAMMER_L, afwd, aup)
    else:
        _grounded(old, fr, aaron, HAMMER_L, afwd)
    gm = gnoll.matrix_world
    gfwd = (gm.to_3x3() @ Vector((0, -1, 0))).normalized()          # 人偶朝 -Y 为前
    grip = gm @ Vector((0.15 * GH, -0.16 * GH, 0.55 * GH))          # 左手（人偶的 +X 是左）
    if LASH[0] <= t <= LASH[1]:
        tip = _bone(aaron, "hand_r")
    elif CRACK[0] <= t <= CRACK[1]:
        tip = grip + gfwd * 2.0 + Vector((0, 0, 0.7))
    elif WINDUP[0] <= t < LASH[0]:
        tip = grip - gfwd * 0.6 + Vector((0, 0, 1.1))
    else:
        tip = grip + gfwd * 0.25 + Vector((0, 0, -0.9))
    d = tip - grip
    _orient(whip, fr, (grip + tip) / 2, d, gfwd if abs(d.normalized().dot(gfwd)) < 0.95 else Vector((0, 0, 1)))
    whip.scale = (1.0, 1.0, max(d.length, 0.05))
    whip.keyframe_insert("scale", frame=fr)
    lash.location = tip
    lash.keyframe_insert("location", frame=fr)
scene.frame_set(1)
print("  后处理：杜克的钢盾挂左前臂；亚伦的旧锤 0–6.3s 扛肩、之后拄地；监工的鞭子 6.2s 抽在亚伦右腕上，逐帧挂上")
