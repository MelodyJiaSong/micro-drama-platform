# shot02 后处理钩子（S 档）：由 tools/previz/build_previz.py 在建完人与道具之后执行，共享引擎的全局名字空间。
# 只管三件本镜细节：杜克左前臂上的盾、亚伦手里的锤、两只狼的扑咬 / 翻滚。时刻与 shot02.md `动作:` 逐拍对齐。
# 盾的朝向不写死：盾绑在前臂手背一侧，每帧取前臂骨的手背方向作盾面法线——手臂挡向哪、盾就朝哪（follow-up 032）。

SHIELD_R, SHIELD_T = 0.36, 0.05      # 祖父的大圆木盾：直径约 0.72 m，比他半个身子还大
HAMMER_L = 1.05
# 锤：(t, 状态, 俯仰°)。two ＝ 双手握、锤头沿「身体正前方转上俯仰角」的方向；shoulder ＝ 扛在右肩；ground ＝ 放在脚边
HAMMER = [(0, "shoulder", 0), (1.3, "shoulder", 0), (1.45, "ground", 0), (3.2, "ground", 0), (3.35, "two", -40),
          (5.8, "two", -35), (6.05, "two", 118), (6.4, "two", -62), (6.9, "two", -62), (7.4, "two", -35),
          (8, "two", 72), (8.45, "two", -48), (9, "two", -35), (10.5, "two", -72), (22, "two", -72)]
# 狼：(t, 抬高 m, 俯仰°[, 翻滚°])；负俯仰 ＝ 抬头扑起，正 ＝ 低头咬
WOLF = {
    "幼狼（正面）": [(5.2, 0, 0), (5.5, 0.05, 18), (5.8, 0, 0), (6.5, 0, 0), (6.8, 0.38, -28), (6.95, 0.30, -10),
                   (7.2, 0.15, 60, 120), (7.7, 0, 0, 360), (20, 0, 0, 360), (20.3, 0.05, 20, 360), (20.6, 0, 0, 360)],
    "幼狼（绕后）": [(8.1, 0, 0), (8.35, 0.22, -16), (8.55, -0.1, 25, 25), (8.9, 0, 0, 0)],
}

from mathutils import Matrix, Quaternion  # noqa: E402

aaron = ACTORS["亚伦"]["armature"]
duke = ACTORS["杜克"]["armature"]


def _bone(arm, name):
    return arm.matrix_world @ arm.pose.bones[name].head


def _frame(arm):
    """(身体正前方, 向上)：左肩减右肩叉乘竖直——人朝哪、这一向就朝哪。"""
    up = Vector((0, 0, 1))
    left = _bone(arm, "arm_l") - _bone(arm, "arm_r")
    fwd = left.cross(up)
    return fwd.normalized(), up


def _orient(ob, frame, loc, axis_z, axis_y):
    z = axis_z.normalized()
    y = (axis_y - z * axis_y.dot(z)).normalized()
    x = y.cross(z)
    ob.rotation_mode = "QUATERNION"
    ob.location = loc
    ob.rotation_quaternion = Matrix((x, y, z)).transposed().to_quaternion()
    ob.keyframe_insert("location", frame=frame)
    ob.keyframe_insert("rotation_quaternion", frame=frame)


m_face, m_mark = _mat_for("黄"), _mat_for("红")
shield = cyl("杜克_盾", SHIELD_R, SHIELD_T, (0, 0, 0), m_face)            # 圆柱轴 ＝ 盾面法线（局部 Z）
boss = sphere("杜克_盾心", 0.07, (0, 0, 0), m_mark)                        # 凸出的盾心只在正面：看得出哪面朝外
attach(boss, shield, (0, 0, SHIELD_T / 2 + 0.03))
shaft = cyl("亚伦_锤柄", 0.02, HAMMER_L, (0, 0, 0), _mat_for("褐"))       # 局部 Z ＝ 锤柄方向，原点在柄中点
head = box("亚伦_锤头", (0.22, 0.11, 0.11), (0, 0, 0), _mat_for("深灰"))
attach(head, shaft, (0, 0, HAMMER_L / 2))


def _hammer_state(t):
    prev = HAMMER[0]
    for k in HAMMER:
        if k[0] > t:
            break
        prev = k
    nxt = next((k for k in HAMMER if k[0] > t), prev)
    if prev[1] == nxt[1] == "two" and nxt[0] > prev[0]:
        a = (t - prev[0]) / (nxt[0] - prev[0])
        return "two", prev[2] + (nxt[2] - prev[2]) * a
    return prev[1], prev[2]


ground_pose = None
for fr in range(1, f(TOTAL) + 1):
    scene.frame_set(fr)
    t = (fr - 1) / FPS
    # ── 盾：绑在前臂手背一侧——盾面法线 ＝ 前臂骨的 -Z（实测格挡帧指向威胁），柄向 ＝ 前臂，盾心在前臂中点外 7 cm ──
    el, wr = _bone(duke, "forearm_l"), _bone(duke, "hand_l")
    fore = (wr - el).normalized()
    n = -(duke.matrix_world @ duke.pose.bones["forearm_l"].matrix).to_3x3().normalized().col[2]
    _orient(shield, fr, (el + wr) / 2 + n * 0.07, n, fore)
    # ── 锤 ──
    mode, pitch = _hammer_state(t)
    hr, hl = _bone(aaron, "hand_r"), _bone(aaron, "hand_l")
    afwd, aup = _frame(aaron)
    if mode == "shoulder":
        d = (_bone(aaron, "arm_r") + aup * 0.08 - hr).normalized()
        grip = hr
        ground_pose = None
    elif mode == "ground":
        if ground_pose is None:            # 放下的那一刻定在他右前方地上，此后不动
            side = afwd.cross(aup).normalized()
            base = Vector((hr.x, hr.y, 0)) + side * 0.15
            base.z = ground_z(base.x, base.y) if GROUND else ORIGIN.z
            ground_pose = (base + Vector((0, 0, 0.06)), afwd.copy())
        grip, d = ground_pose[0] - ground_pose[1] * (HAMMER_L * 0.45), ground_pose[1]
    else:
        p = math.radians(pitch)
        d = (afwd * math.cos(p) + aup * math.sin(p)).normalized()
        grip = (hr + hl) / 2
    _orient(shaft, fr, grip + d * (HAMMER_L * 0.30), d, aup if abs(d.dot(aup)) < 0.95 else afwd)

# ── 狼：身子的抬高 / 俯仰 / 翻滚，叠在引擎按 overhead 打好的位置与朝向上 ──
for label, keys in WOLF.items():
    body = ACTORS[label]["joints"]["body"]
    z0 = body.location.z
    for k in keys:
        tk, lift, pitch = k[0], k[1], k[2]
        roll = k[3] if len(k) > 3 else 0
        body.location.z = z0 + lift
        body.keyframe_insert("location", frame=f(tk))
        key_rot(body, f(tk), (pitch, roll, 0))
scene.frame_set(1)
print("  后处理：盾 / 锤逐帧挂上，狼的扑咬 %d 拍" % sum(len(v) for v in WOLF.values()))
