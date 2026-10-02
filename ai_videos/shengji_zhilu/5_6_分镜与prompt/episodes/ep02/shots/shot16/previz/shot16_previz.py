# shot16 后处理钩子（S 档）：由 tools/previz/build_previz.py 在建完人与道具之后执行，共享引擎的全局名字空间。
# 杜克是 Cascadeur 体：竖长钢盾由这里逐帧挂在他左前臂上（名字「杜克_盾」——5.6s 冲锋那一下的命中检查按它量）。
# 亚伦是色块人偶，父亲的锤走 Shot.previz['carry']；金牙的镐同理。
# ⚠ blend 里上下两层同一地坪（build_scene 没有坡道），0–2.8s 下坡在 previz 里是平地走，只锁时刻与方向。

STEEL = (0.55, 0.85, 0.04)           # 竖长十边形钢盾：宽 × 高 × 厚（e5205）

from mathutils import Matrix  # noqa: E402

duke = ACTORS["杜克"]["armature"]


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


steel = box("杜克_盾", STEEL, (0, 0, 0), _mat_for("白"))                    # 局部 Z ＝ 盾面法线，局部 Y ＝ 盾的长边
boss = sphere("杜克_盾心", 0.06, (0, 0, 0), _mat_for("红"))
attach(boss, steel, (0, 0, STEEL[2] / 2 + 0.03))

for fr in range(1, f(TOTAL) + 1):
    scene.frame_set(fr)
    el, wr = _bone(duke, "forearm_l"), _bone(duke, "hand_l")
    n = -(duke.matrix_world @ duke.pose.bones["forearm_l"].matrix).to_3x3().normalized().col[2]
    _orient(steel, fr, (el + wr) / 2 + n * 0.08, n, (wr - el).normalized())
scene.frame_set(1)
print("  后处理：杜克的钢盾逐帧挂在左前臂上")
