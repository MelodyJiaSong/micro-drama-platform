# shot21 后处理钩子（S 档）：由 tools/previz/build_previz.py 在建完人与道具之后执行，共享引擎的全局名字空间。
# 只管本镜的手持物件与光：杜克的钢盾（整镜绑在左前臂）、背上卡着斧刃的祖父木盾（两半，follow-up 047 / 049）、加瑞克的阔刃斧、
# 亚伦父亲的旧锤、掌心的光、光柱、加瑞克胸口炸开的那团光（审判）。时刻与 shot21.md `动作:`、overhead 的 [[hit]] / [[cast]] 逐拍对齐。
# 盾面与斧向都不写死：每帧从 Cascadeur 骨架读——前臂挡向哪、盾就朝哪；两只手的前臂指向哪、斧柄就朝哪。
# 049：0.8s 前斧刃卡在杜克背上那面圆木盾里（与 S20 落幅同一件道具，两半并成一面）；两半木盾与斧的落点读 overhead [[prop]]，交给 S22。

STEEL = (0.55, 0.85, 0.04)           # 竖长十边形钢盾：宽 × 高 × 厚
HALF_R, HALF_L = "右半块木盾", "左半块木盾"
AXE_PROP = "阔刃斧"
AXE_L, HAMMER_L = 1.1, 1.2           # 父亲的旧双手锤全长约 1.2 m
HALF_ON_BACK, HALF_R_OFF, HALF_L_OFF = 0.8, 1.8, 2.6
AXE_DROP, AXE_LAND = 23.4, 24.0
PALM = cast_curve("亚伦", ("gather", "release"), 0.09, 0.2, "k201")     # 时刻按技能卡（[[施法]]，follow-up 065）
COLUMN = cast_curve("亚伦", ("effect",), 1.0, 0.1, "k201")
BURST = cast_windows("亚伦", ("effect",), "k202")
# 审判：目标胸口炸开的一团光（技能卡 k202 effect，没有飞行物、不叫回——053）

from mathutils import Matrix  # noqa: E402

duke = ACTORS["杜克"]["armature"]
gar = ACTORS["加瑞克"]["armature"]
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
            nxt = k
            a = (t - prev[0]) / (nxt[0] - prev[0]) if nxt[0] > prev[0] else 1.0
            return prev[1] + (nxt[1] - prev[1]) * a
        prev = k
    return prev[1]


def _scale(ob, fr, s):
    ob.scale = (max(s, 1e-4),) * 3
    ob.keyframe_insert("scale", frame=fr)


def _prop_end(name):
    """overhead [[prop]] 的最后一个路点（配置里 [[道具.关键帧]] 的末帧位置）——落点只写在平面图一处。"""
    p = next(q for q in CFG.get("道具", []) if q["名"] == name)
    ks = [k for k in p.get("关键帧", []) if "位置" in k]
    xyz = ks[-1]["位置"] if ks else p["位置"]
    loc = ORIGIN + Vector([float(v) for v in xyz])
    if GROUND:
        loc.z = ground_z(loc.x, loc.y)
    return loc + Vector((0, 0, 0.03))


LIGHT = mat("PREVIZ_光", (1.0, 0.82, 0.30), 8.0)
steel = box("杜克_盾", STEEL, (0, 0, 0), _mat_for("白"))                    # 局部 Z ＝ 盾面法线，局部 Y ＝ 盾的长边
boss = sphere("杜克_盾心", 0.06, (0, 0, 0), _mat_for("红"))
attach(boss, steel, (0, 0, STEEL[2] / 2 + 0.03))
axe = cyl("加瑞克_斧柄", 0.025, AXE_L, (0, 0, 0), _mat_for("橙"))           # 局部 Z ＝ 柄向，原点在柄中点
blade = box("加瑞克_斧刃", (0.32, 0.04, 0.26), (0, 0, 0), _mat_for("白"))
attach(blade, axe, (0.12, 0, AXE_L / 2 - 0.1))
ham = cyl("亚伦_锤柄", 0.018, HAMMER_L, (0, 0, 0), _mat_for("褐"))
hhead = box("亚伦_锤头", (0.16, 0.1, 0.1), (0, 0, 0), _mat_for("深灰"))
attach(hhead, ham, (0, 0, HAMMER_L / 2))
palm = sphere("亚伦_掌心光", 1.0, (0, 0, 0), LIGHT)
column = cyl("光柱", 0.55, 5.0, (0, 0, 0), LIGHT)
orb = sphere("审判的光", 0.2, (0, 0, 0), LIGHT)
halves = {HALF_R: PROPS[HALF_R]["ob"], HALF_L: PROPS[HALF_L]["ob"]}
for _h in halves.values():            # 半面木盾换成棕色扁块（0.7 × 0.35 半圆的包围盒），两块并起来就是 S20 落幅那面圆木盾
    _h.data.materials.clear()
    _h.data.materials.append(_mat_for("褐"))
rest = {HALF_R: _prop_end(HALF_R), HALF_L: _prop_end(HALF_L)}
axe_land = _prop_end(AXE_PROP)
PROPS[AXE_PROP]["ob"].hide_render = PROPS[AXE_PROP]["ob"].hide_viewport = True   # 地上那把由下面的斧落地接管

pref = bpy.context.preferences.edit
_interp = pref.keyframe_new_interpolation_type
for fr in range(1, f(TOTAL) + 1):
    scene.frame_set(fr)
    t = (fr - 1) / FPS
    # ── 钢盾：整镜绑在左前臂手背一侧，法线 ＝ 前臂骨 -Z（shot02 实测格挡帧指向威胁）──
    dfwd, up, dleft = _frame(duke)
    el, wr = _bone(duke, "forearm_l"), _bone(duke, "hand_l")
    n = -(duke.matrix_world @ duke.pose.bones["forearm_l"].matrix).to_3x3().normalized().col[2]
    _orient(steel, fr, (el + wr) / 2 + n * 0.08, n, (wr - el).normalized())
    # ── 背上的圆木盾（0.8s 前）：两半并在杜克背心，盾面朝后 ──
    chest = (_bone(duke, "arm_l") + _bone(duke, "arm_r")) / 2
    back = chest - dfwd * 0.2 - up * 0.25
    # ── 斧：0.8s 前斧刃嵌在背上那面木盾的正中，柄指向加瑞克两手；之后两前臂的平均指向 ＝ 柄向 ──
    gfwd, _u, gleft = _frame(gar)
    hr, hl = _bone(gar, "hand_r"), _bone(gar, "hand_l")
    if t < HALF_ON_BACK:
        d = (back - (hr + hl) / 2).normalized()
        _orient(axe, fr, back - d * (AXE_L / 2 - 0.1), d, gleft)
    elif t < AXE_DROP:
        d = ((hr - _bone(gar, "forearm_r")) + (hl - _bone(gar, "forearm_l"))).normalized()
        _orient(axe, fr, (hr + hl) / 2 + d * (AXE_L * 0.25), d, gleft)
    elif t >= AXE_LAND:
        bounce = 0.12 if abs(t - (AXE_LAND + 0.18)) < 0.1 else 0.0
        _orient(axe, fr, axe_land + Vector((0, 0, bounce)), Vector((0, 1, 0)), Vector((0, 0, 1)))
    head = axe.matrix_world @ Vector((0, 0, AXE_L / 2 - 0.1))
    # ── 两半木盾：0.8s 前并在杜克背上；随后卡在斧刃上被拽走；右半 1.8s、左半 2.6s 落到平面图写的位置 ──
    for name, side, off_t in ((HALF_R, -1.0, HALF_R_OFF), (HALF_L, 1.0, HALF_L_OFF)):
        ob = halves[name]
        if t < HALF_ON_BACK:
            _orient(ob, fr, back + dleft * (0.18 * side), -dfwd, up)
        elif t < off_t:
            _orient(ob, fr, head + gleft * (0.1 * side), gfwd, up)
        elif fr <= f(off_t + 0.25):
            _orient(ob, fr, rest[name], Vector((0, 0, 1)), Vector((0, 1, 0)))
    # ── 父亲的旧锤：右手握、顺着右前臂，锤头拄地 ──
    ar, afwd = _bone(aaron, "hand_r"), _frame(aaron)[0]
    hd = (ar - _bone(aaron, "forearm_r")).normalized()
    _orient(ham, fr, ar + hd * 0.1, hd, afwd)          # 握在柄中段：垂手时锤头正好拄地
    # ── 光 ──
    pref.keyframe_new_interpolation_type = "LINEAR"
    palm.location = _bone(aaron, "hand_l") + afwd * 0.06
    palm.keyframe_insert("location", frame=fr)
    _scale(palm, fr, _step(PALM, t))
    column.location = chest + Vector((0, 0, 1.6))
    column.keyframe_insert("location", frame=fr)
    _scale(column, fr, _step(COLUMN, t))
    if any(a <= t <= b for a, b in BURST):
        orb.location = (_bone(gar, "arm_l") + _bone(gar, "arm_r")) / 2 - Vector((0, 0, 0.25))
        _scale(orb, fr, 1.0)
    else:
        _scale(orb, fr, 0.0)
    orb.keyframe_insert("location", frame=fr)
    pref.keyframe_new_interpolation_type = _interp
scene.frame_set(1)
print("  后处理：钢盾 / 背上圆木盾（两半）/ 斧 / 锤逐帧挂上；掌心光、光柱、审判的光按时刻表缩放")
