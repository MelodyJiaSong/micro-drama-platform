# shot11 后处理钩子（S 档）：由 tools/previz/build_previz.py 在建完人与道具之后执行，共享引擎的全局名字空间。
# 只管本镜的手持物件与光：杜克的钢盾（整镜绑在左前臂）、背上的祖父圆木盾、亚伦父亲的旧锤（14.2s 前在手里，之后交给平面图
# [[prop]]「父亲的旧锤」躺在碎石上、被小矿工拖走）、掌心的光、落在杜克身上的光柱（时刻按技能卡）。时刻与 shot11.md `动作:`、overhead 的
# [[hit]] / [[cast]] 逐拍对齐。盾面与锤向都从 Cascadeur 骨架读（follow-up 052：人体一律 Cascadeur）。

STEEL = (0.55, 0.85, 0.04)           # 竖长十边形钢盾：宽 × 高 × 厚
WOOD_R, WOOD_T = 0.36, 0.05          # 祖父的圆木盾（背在背后）
HAMMER_L = 1.2                       # 父亲的旧双手锤全长约 1.2 m
DROP = 13.8                          # 跪下撂锤：此后手里没有锤，地上那把由平面图 [[prop]] 接管
PALM = cast_curve("亚伦", ("gather", "release"), 0.07, 0.2)      # 掌心光 / 光柱的时刻按技能卡 k201（[[施法]]，follow-up 065）
COLUMN = cast_curve("亚伦", ("effect",), 1.0)

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


def _step(keys, t):
    prev = keys[0]
    for k in keys:
        if k[0] > t:
            a = (t - prev[0]) / (k[0] - prev[0]) if k[0] > prev[0] else 1.0
            return prev[1] + (k[1] - prev[1]) * a
        prev = k
    return prev[1]


def _scale(ob, fr, s):
    ob.scale = (max(s, 1e-4),) * 3
    ob.keyframe_insert("scale", frame=fr)


LIGHT = mat("PREVIZ_光", (1.0, 0.82, 0.30), 8.0)
steel = box("杜克_盾", STEEL, (0, 0, 0), _mat_for("白"))                    # 局部 Z ＝ 盾面法线，局部 Y ＝ 盾的长边
boss = sphere("杜克_盾心", 0.06, (0, 0, 0), _mat_for("红"))
attach(boss, steel, (0, 0, STEEL[2] / 2 + 0.03))
wood = cyl("杜克_背盾", WOOD_R, WOOD_T, (0, 0, 0), _mat_for("褐"))           # 局部 Z ＝ 盾面法线
ham = cyl("亚伦_锤柄", 0.018, HAMMER_L, (0, 0, 0), _mat_for("褐"))           # 局部 Z ＝ 柄向，原点在柄中点
hhead = box("亚伦_锤头", (0.16, 0.1, 0.1), (0, 0, 0), _mat_for("深灰"))
attach(hhead, ham, (0, 0, HAMMER_L / 2))
palm_l = sphere("亚伦_左掌光", 1.0, (0, 0, 0), LIGHT)
palm_r = sphere("亚伦_右掌光", 1.0, (0, 0, 0), LIGHT)
column = cyl("光柱", 0.5, 4.0, (0, 0, 0), LIGHT)

pref = bpy.context.preferences.edit
_interp = pref.keyframe_new_interpolation_type
for fr in range(1, f(TOTAL) + 1):
    scene.frame_set(fr)
    t = (fr - 1) / FPS
    # ── 钢盾：整镜绑在左前臂手背一侧，法线 ＝ 前臂骨 -Z（shot02 / shot21 同一约定）──
    dfwd, up, dleft = _frame(duke)
    el, wr = _bone(duke, "forearm_l"), _bone(duke, "hand_l")
    n = -(duke.matrix_world @ duke.pose.bones["forearm_l"].matrix).to_3x3().normalized().col[2]
    _orient(steel, fr, (el + wr) / 2 + n * 0.08, n, (wr - el).normalized())
    # ── 祖父的圆木盾：背在背心，盾面朝后 ──
    chest = (_bone(duke, "arm_l") + _bone(duke, "arm_r")) / 2
    _orient(wood, fr, chest - dfwd * 0.2 - up * 0.25, -dfwd, up)
    # ── 父亲的旧锤：两手靠在一起时柄 ＝ 两前臂平均指向，分开时顺着右前臂；14.2s 撂下后手里没有锤 ──
    if t < DROP:
        hr, hl = _bone(aaron, "hand_r"), _bone(aaron, "hand_l")
        side = (_bone(aaron, "arm_l") - _bone(aaron, "arm_r")).normalized()
        if (hr - hl).length < 0.4:
            d = ((hr - _bone(aaron, "forearm_r")) + (hl - _bone(aaron, "forearm_l"))).normalized()
            grip = (hr + hl) / 2
        else:
            d = (hr - _bone(aaron, "forearm_r")).normalized()
            grip = hr
        _orient(ham, fr, grip + d * (HAMMER_L * 0.30), d, side if abs(d.dot(side)) < 0.95 else Vector((0, 0, 1)))
        _scale(ham, fr, 1.0)
    else:
        _scale(ham, fr, 0.0)
    # ── 光：两只掌心、罩住杜克全身的光柱 ──
    pref.keyframe_new_interpolation_type = "LINEAR"
    afwd = _frame(aaron)[0]
    for ob, hand in ((palm_l, "hand_l"), (palm_r, "hand_r")):
        ob.location = _bone(aaron, hand) + afwd * 0.05
        ob.keyframe_insert("location", frame=fr)
        _scale(ob, fr, _step(PALM, t))
    pelvis = duke.matrix_world @ duke.pose.bones["pelvis"].head if "pelvis" in duke.pose.bones else chest
    column.location = Vector((pelvis.x, pelvis.y, pelvis.z + 1.2))
    column.keyframe_insert("location", frame=fr)
    _scale(column, fr, _step(COLUMN, t))
    pref.keyframe_new_interpolation_type = _interp
scene.frame_set(1)
print("  后处理：钢盾 / 背上圆木盾 / 锤逐帧挂上（13.8s 撂下后交给地上那把）；掌心光、光柱按时刻表缩放")
