# shot05 后处理钩子（S 档）：由 tools/previz/build_previz.py 在建完人与道具之后执行，共享引擎的全局名字空间。
# 只管本镜细节：杜克左前臂上的祖父圆木盾、亚伦手里的父亲旧锤（14.3s 锤头一闪）、头狼的三次扑。时刻与 shot05.md `动作:` 逐拍对齐。
# 盾面与锤向都从 Cascadeur 骨架读：盾面法线 ＝ 左前臂骨 -Z；两手靠在一起时锤柄 ＝ 两前臂平均指向，分开时顺着右前臂。

SHIELD_R, SHIELD_T = 0.36, 0.05
HAMMER_L = 1.05
FLASH = [(0.0, 0.0), (14.2, 0.0), (14.3, 0.16), (14.45, 0.16), (14.6, 0.0)]
# 头狼：(t, 抬高 m, 俯仰°[, 翻滚°])；负俯仰 ＝ 抬头扑起，正 ＝ 低头咬
WOLF = {
    "森林狼（头狼）": [(9.7, 0, 0), (10.0, 0.35, -25), (10.3, 0.1, 10), (10.6, 0, 0),
                   (12.2, 0, 0), (12.45, 0.3, -22), (12.6, 0.1, 15, 20), (12.9, 0, 0, 0),
                   (14.1, 0, 0, 0), (14.3, 0.3, -20, 0), (14.5, 0.3, 40, 150), (14.8, 0, 0, 360)],
    "森林狼（西）": [(7.0, 0, 12), (14.8, 0, 12), (15.2, 0, 0)],
    "森林狼（东）": [(7.0, 0, 12), (14.8, 0, 12), (15.2, 0, 0)],
}

from mathutils import Matrix  # noqa: E402

duke = ACTORS["杜克"]["armature"]
aaron = ACTORS["亚伦"]["armature"]


def _bone(arm, name):
    return arm.matrix_world @ arm.pose.bones[name].head


def _orient(ob, frame, loc, axis_z, axis_y):
    z = axis_z.normalized()
    y = (axis_y - z * axis_y.dot(z)).normalized()
    x = y.cross(z)
    ob.rotation_mode = "QUATERNION"
    ob.location = loc
    ob.rotation_quaternion = Matrix((x, y, z)).transposed().to_quaternion()
    ob.keyframe_insert("location", frame=frame)
    ob.keyframe_insert("rotation_quaternion", frame=frame)


def _step(keys, t):
    prev = keys[0]
    for k in keys:
        if k[0] > t:
            a = (t - prev[0]) / (k[0] - prev[0]) if k[0] > prev[0] else 1.0
            return prev[1] + (k[1] - prev[1]) * a
        prev = k
    return prev[1]


shield = cyl("杜克_盾", SHIELD_R, SHIELD_T, (0, 0, 0), _mat_for("黄"))
boss = sphere("杜克_盾心", 0.07, (0, 0, 0), _mat_for("红"))
attach(boss, shield, (0, 0, SHIELD_T / 2 + 0.03))
shaft = cyl("亚伦_锤柄", 0.02, HAMMER_L, (0, 0, 0), _mat_for("褐"))
head = box("亚伦_锤头", (0.22, 0.11, 0.11), (0, 0, 0), _mat_for("深灰"))
attach(head, shaft, (0, 0, HAMMER_L / 2))
flash = sphere("亚伦_锤头闪光", 1.0, (0, 0, 0), mat("PREVIZ_光", (1.0, 0.82, 0.30), 8.0))

pref = bpy.context.preferences.edit
_interp = pref.keyframe_new_interpolation_type
for fr in range(1, f(TOTAL) + 1):
    scene.frame_set(fr)
    t = (fr - 1) / FPS
    el, wr = _bone(duke, "forearm_l"), _bone(duke, "hand_l")
    n = -(duke.matrix_world @ duke.pose.bones["forearm_l"].matrix).to_3x3().normalized().col[2]
    _orient(shield, fr, (el + wr) / 2 + n * 0.07, n, (wr - el).normalized())
    hr, hl = _bone(aaron, "hand_r"), _bone(aaron, "hand_l")
    side = (_bone(aaron, "arm_l") - _bone(aaron, "arm_r")).normalized()
    if (hr - hl).length < 0.4:
        d = ((hr - _bone(aaron, "forearm_r")) + (hl - _bone(aaron, "forearm_l"))).normalized()
        grip = (hr + hl) / 2
    else:
        d = (hr - _bone(aaron, "forearm_r")).normalized()
        grip = hr
    _orient(shaft, fr, grip + d * (HAMMER_L * 0.30), d, side if abs(d.dot(side)) < 0.95 else Vector((0, 0, 1)))
    pref.keyframe_new_interpolation_type = "LINEAR"
    flash.location = shaft.matrix_world @ Vector((0, 0, HAMMER_L / 2))
    flash.keyframe_insert("location", frame=fr)
    s = max(_step(FLASH, t), 1e-4)
    flash.scale = (s, s, s)
    flash.keyframe_insert("scale", frame=fr)
    pref.keyframe_new_interpolation_type = _interp

IN_FERNS = [(0.0, 0.0), (6.8, 0.0), (7.1, 1.0), (17.2, 1.0), (17.6, 0.0)]   # 7s 前、17.5s 后在蕨丛里：previz 场景没有蕨丛，只能藏起来
for label, keys in WOLF.items():
    root = ACTORS[label]["root"]
    for tk, s in IN_FERNS:
        root.scale = (max(s, 1e-4),) * 3
        root.keyframe_insert("scale", frame=f(tk))
    body = ACTORS[label]["joints"]["body"]
    z0 = body.location.z
    for k in keys:
        body.location.z = z0 + k[1]
        body.keyframe_insert("location", frame=f(k[0]))
        key_rot(body, f(k[0]), (k[2], k[3] if len(k) > 3 else 0, 0))
scene.frame_set(1)
print("  后处理：盾 / 锤逐帧挂上；头狼三次扑、两侧的狼压着头；14.3s 锤头一闪")
