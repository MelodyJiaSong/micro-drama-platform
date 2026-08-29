"""AI 短剧 previz 的「精致人形」层：用 MPFB（MakeHuman）真人网格替代方块拼的小绿人。

**为什么这一层要独立成模块。** `tools/previz_rig.py` 的关节 proxy 负责**动画逻辑**（所有
姿态 K 帧都打在它的关节空物件上，宿主脚本只认 `J[...]`）；本模块只负责**外观**：造一具
MPFB 真人网格，把它的骨骼逐根「Child Of」到那些关节空物件上，随之刚性运动。这样：

- 姿态库 / 时间轴 / 采样跟随（剑跟手、葫芦跟手）一行都不用改；
- 关节 proxy 网格隐藏（保留空物件），画面里只剩一具四肢、手指、脚都读得出的绿人。

**用法**（宿主脚本，在 `rig.build(P)` 之后、任何 K 帧之前调用；此时关节全部处于静默姿态）：

    from tools.previz_human import attach_mpfb_human
    human, arm = attach_mpfb_human(root, J, link=link_previz, body_mat=M_GREEN, skin_mat=M_SKIN, limb_mat=M_LIMB)

**要点**
- MPFB 默认静默是 A-pose（臂外张 40°、前臂前倾、手指前指），而 proxy 的静默是四肢与手指
  一律竖直向下。所以先把 MPFB 摆成 proxy 的静默姿态并 **应用为静止姿态**，再挂约束。
- 上臂 / 前臂 / 大腿用 MPFB targets 拉长到与 proxy 一致（0.30 / 0.30 / 0.46），关节枢纽位置
  才对得上；不对上，前臂会绕错误的枢纽转、肘部露缝。
- 每根被约束的骨骼先**脱离父骨**（否则父骨与子骨各自跟随会叠加两次变换——Child Of 在骨骼
  层级上的经典双重变换问题），未被约束的中间骨（扭转骨、颈、拇指掌骨）照常继承。
- 材质按骨权重分三档：手（腕 + 掌骨 + 指骨）与脚用亮色、头用浅色、其余绿——与 proxy 配色一致。
"""
from __future__ import annotations

import math
import os

import bpy
from mathutils import Matrix, Vector

# 关节空物件键 → MPFB default 骨名（被约束、且会脱离父骨）。
# 值可以是一根骨名，也可以是一组骨名（前脚掌要带动五根脚趾）。
BONE_MAP: dict[str, object] = {
    "__root__": "root",
    "pelvis": "spine05",
    # 颈只约束 neck01：neck02/03 不在表里、保留父子链，于是跟着 neck01 走，
    # 脖子因此是一段能弯的链而不是一块刚体。
    "neck": "neck01",
    "head": "head",
}
for _s in ("L", "R"):
    BONE_MAP.update({
        f"clavicle{_s}": f"clavicle.{_s}",
        f"shoulder{_s}": f"upperarm01.{_s}",
        f"elbow{_s}": f"lowerarm01.{_s}",
        f"hand{_s}": f"wrist.{_s}",
        f"hip{_s}": f"upperleg01.{_s}",
        f"knee{_s}": f"lowerleg01.{_s}",
        f"ankle{_s}": f"foot.{_s}",
        # 前脚掌带动五根脚趾根节；趾的第 2/3 节不在表里，跟着各自根节走
        f"ball{_s}": tuple(f"toe{_n}-1.{_s}" for _n in range(1, 6)),
        # 手指：proxy 每指三节 → MPFB finger{n}-{1,2,3}；拇指两节 → finger1-2/1-3（finger1-1 是掌骨，跟腕）
        f"hand{_s}_idx1": f"finger2-1.{_s}", f"hand{_s}_idx2": f"finger2-2.{_s}", f"hand{_s}_idx3": f"finger2-3.{_s}",
        f"hand{_s}_mid1": f"finger3-1.{_s}", f"hand{_s}_mid2": f"finger3-2.{_s}", f"hand{_s}_mid3": f"finger3-3.{_s}",
        f"hand{_s}_rng1": f"finger4-1.{_s}", f"hand{_s}_rng2": f"finger4-2.{_s}", f"hand{_s}_rng3": f"finger4-3.{_s}",
        f"hand{_s}_lit1": f"finger5-1.{_s}", f"hand{_s}_lit2": f"finger5-2.{_s}", f"hand{_s}_lit3": f"finger5-3.{_s}",
        f"hand{_s}_thb1": f"finger1-2.{_s}", f"hand{_s}_thb2": f"finger1-3.{_s}",
    })

MACRO = {
    "gender": 1.0, "age": 0.6, "muscle": 0.55, "weight": 0.45, "proportions": 0.6,
    "height": 0.58, "cupsize": 0.5, "firmness": 0.5,
    "race": {"asian": 1.0, "caucasian": 0.0, "african": 0.0},
}

# height 参数 → 实际身高（米）。实测标定（follow-up 061）：age=0.5 成年基准。
# 曲线在 0.5 以上斜率翻倍，直接线性外推会把人做矮一大截。
_HEIGHT_CURVE_M = ((0.20, 1.418), (0.35, 1.527), (0.50, 1.629),
                   (0.65, 1.829), (0.80, 2.044), (0.95, 2.259))
_HEIGHT_CURVE_F = ((0.35, 1.394), (0.50, 1.496), (0.65, 1.696), (0.80, 1.910))
# age 参数：< 0.5 是儿童生长曲线（会把成年人压成孩子身量），>= 0.5 才是成年。
AGE_ADULT_MIN = 0.50


def height_param_for(meters: float, gender: float = 1.0) -> float:
    """按目标身高（米）反查 MPFB 的 height 参数。超出标定区间时按两端斜率外推。"""
    curve = _HEIGHT_CURVE_M if gender >= 0.5 else _HEIGHT_CURVE_F
    if meters <= curve[0][1]:
        (p0, h0), (p1, h1) = curve[0], curve[1]
    elif meters >= curve[-1][1]:
        (p0, h0), (p1, h1) = curve[-2], curve[-1]
    else:
        for (p0, h0), (p1, h1) in zip(curve, curve[1:]):
            if h0 <= meters <= h1:
                break
    return p0 + (meters - h0) * (p1 - p0) / (h1 - h0)


def macro_for(spec: dict | None) -> dict:
    """把「人话体型」翻译成 MPFB macro 参数。

    spec 支持的键（都可省）：身高(米) / 体格(0..1 瘦→壮) / 年龄档(0..1，>=0.5 成年)
    / 性别(1 男 0 女) / 比例(0..1 敦实→修长)。缺省沿用 MACRO。
    """
    macro = dict(MACRO)
    if not spec:
        return macro
    gender = float(spec.get("性别", macro["gender"]))
    macro["gender"] = gender
    if "年龄档" in spec:
        age = float(spec["年龄档"])
        if age < AGE_ADULT_MIN:
            print(f"  [warn] 年龄档 {age} < {AGE_ADULT_MIN}：MPFB 会按儿童身量建模")
        macro["age"] = age
    if "体格" in spec:
        g = float(spec["体格"])
        macro["muscle"], macro["weight"] = 0.25 + g * 0.55, 0.28 + g * 0.42
    if "比例" in spec:
        macro["proportions"] = float(spec["比例"])
    if "身高" in spec:
        macro["height"] = height_param_for(float(spec["身高"]), gender)
    return macro
# 与 tools/previz_rig.py 的比例对齐：上臂 0.30 / 前臂 0.30 / 大腿 0.46 / 小腿 0.42
LIMB_TARGETS = (
    ("arms", "measure-upperarm-length-incr", 0.73),
    ("arms", "measure-lowerarm-length-incr", 0.77),
    ("legs", "measure-upperleg-height-incr", 0.36),
)


NEUTRALIZE_SUBJ_FRAC = 0.40
"""人占画高超过这个比例就自动中性化。

实测（follow-up 061）：人占画高 22% 时头约 16 像素，脸与解剖细节在成片分辨率下
不可读，中性化纯属浪费；近景才有必要——既防 rule 12.16 的长相泄漏，也避开把
裸体人形当参考素材上传的平台风险。
"""


def neutralize_human(body, *, material=None, head_parent=None):
    """去脸 + 压平解剖细节。**顺序不能换**：必须先烘 shape key。

    三条实测教训（follow-up 061，全部静默失效、不报错）：
    ① MPFB 体型是 shape key 驱动的，直接改基础网格顶点会被盖回去，不报错也不变形；
    ② 顶点组是绑骨之后才生成的，绑骨前按名字找组只会静默跳过；
    ③ 头必须**删除+替换**，不能把顶点投影到椭球——头部顶点组含口腔、眼窝、耳朵，
       整体投影会把它们拍到表面，产生自交与破洞，比原样更糟。

    `head_parent`＝替换头要挂的**关节空物件**（通常是 J["head"]）。**不能挂在 body 上**：
    body 是被骨架形变驱动的，而物件级父子关系不跟随形变——人一转头，网格头部在动，
    那颗椭球却纹丝不动。这个错误不会报错，只会在成片里露出一颗浮着的球。
    """
    import bmesh
    import math

    if body.data.shape_keys:          # ① 先烘焙，否则后面全白做
        body.shape_key_add(name="_bake", from_mix=True)
        for k in list(body.data.shape_keys.key_blocks):
            if k.name != "_bake":
                body.shape_key_remove(k)
        body.shape_key_remove(body.data.shape_keys.key_blocks["_bake"])

    def gverts(names, thresh):
        idx = {g.index for g in body.vertex_groups if g.name in names}
        if not idx:
            return set()
        return {v.index for v in body.data.vertices
                if sum(g.weight for g in v.groups if g.group in idx) >= thresh}

    head_ids = gverts({"head"}, 0.5)
    head_ob = None
    if head_ids:                      # ③ 删头 + 挂椭球
        pts = [body.matrix_world @ body.data.vertices[i].co for i in head_ids]
        c = sum(pts, Vector()) / len(pts)
        rx = max(abs(p.x - c.x) for p in pts)
        ry = max(abs(p.y - c.y) for p in pts)
        rz = max(abs(p.z - c.z) for p in pts)
        bm = bmesh.new()
        bm.from_mesh(body.data)
        bm.verts.ensure_lookup_table()
        bmesh.ops.delete(bm, geom=[bm.verts[i] for i in head_ids], context="VERTS")
        bm.to_mesh(body.data)
        bm.free()
        body.data.update()
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=24, ring_count=16, location=c)
        head_ob = bpy.context.object
        head_ob.name = body.name + "_head"
        # 0.78：头顶点组含下颌与颈上端，直接取 max 会把椭球撑成一颗大灯泡
        head_ob.scale = Vector((rx * 0.78, ry * 0.78, rz * 0.82))
        anchor = head_parent if head_parent is not None else body
        head_ob.parent = anchor
        head_ob.matrix_parent_inverse = anchor.matrix_world.inverted()
        if material is not None:
            head_ob.data.materials.append(material)
        for pol in head_ob.data.polygons:
            pol.use_smooth = True
        # 鼻锥：光溜溜的椭球读不出朝向——而朝向正是 previz 要传达的核心信息之一。
        # proxy 原本靠发髻解决这件事，换头后必须补回来，否则中性化是一次信息净损失。
        bpy.ops.mesh.primitive_cone_add(radius1=rx * 0.20, depth=ry * 0.55,
                                        vertices=12, location=c)
        nose = bpy.context.object
        nose.name = body.name + "_nose"
        nose.rotation_euler = (math.radians(-90), 0, 0)
        nose.location = c + Vector((0.0, -ry * 0.72, 0.0))
        nose.parent = head_ob
        nose.matrix_parent_inverse = head_ob.matrix_world.inverted()
        if material is not None:
            nose.data.materials.append(material)

    for groups, amount, thresh in ((("breast.L", "breast.R"), 0.75, 0.30),
                                   (("pelvis.L", "pelvis.R"), 0.45, 0.30)):
        ids = gverts(set(groups), thresh)
        if not ids:
            continue
        pts = [body.data.vertices[i].co for i in ids]
        c = sum(pts, Vector()) / len(pts)
        for i in ids:
            d = body.data.vertices[i].co - c
            body.data.vertices[i].co = c + Vector((d.x, d.y * (1.0 - amount), d.z))
    body.data.update()
    print(f"  中性化：换头 {'✓' if head_ob else '✗'}，压平胸/胯")
    return head_ob


def _mpfb():
    from bl_ext.blender_org.mpfb.services.humanservice import HumanService
    from bl_ext.blender_org.mpfb.services.targetservice import TargetService
    from bl_ext.blender_org.mpfb.services.rigservice import RigService
    import bl_ext.blender_org.mpfb as mpfb
    return HumanService, TargetService, RigService, os.path.join(os.path.dirname(mpfb.__file__), "data", "targets")


def _rot_bone_world(arm, name: str, R: Matrix) -> None:
    pb = arm.pose.bones[name]
    head = pb.matrix.to_translation()
    pb.matrix = Matrix.Translation(head) @ R @ Matrix.Translation(-head) @ pb.matrix
    bpy.context.view_layer.update()


def _aim(arm, bone: str, child: str, target_dir: Vector) -> None:
    """转动 `bone`，使 `child` 骨头的头（即 bone 所带的下一枢纽）从当前方向转到 target_dir。"""
    pb, pc = arm.pose.bones[bone], arm.pose.bones[child]
    cur = (pc.matrix.to_translation() - pb.matrix.to_translation()).normalized()
    q = cur.rotation_difference(target_dir.normalized())
    _rot_bone_world(arm, bone, q.to_matrix().to_4x4())


def _aim_tail(arm, bone: str, target_dir: Vector) -> None:
    """末节没有子骨可参照，用骨自身的 tail 方向对齐。

    漏掉这一步的话，手指前两节被摆竖直、**末节保留 MPFB 静默的后翘** —— 剑指的
    食中二指一根直一根翘，画面读成「分叉的 V」（follow-up 059 二次反馈的根因）。
    """
    pb = arm.pose.bones[bone]
    cur = (pb.tail - pb.head).normalized()
    q = cur.rotation_difference(target_dir.normalized())
    _rot_bone_world(arm, bone, q.to_matrix().to_4x4())


def _bone_verts(body, arm_names: set[str], thresh: float = 0.5) -> set[int]:
    idx = {g.index for g in body.vertex_groups if g.name in arm_names}
    out = set()
    for v in body.data.vertices:
        w = sum(g.weight for g in v.groups if g.group in idx)
        if w >= thresh:
            out.add(v.index)
    return out


def attach_mpfb_human(root, J: dict, *, link, body_mat, skin_mat, limb_mat,
                      name: str = "PVZ_human", body_spec: dict | None = None,
                      neutralize: bool | None = None, subj_frac: float | None = None):
    """`body_spec`＝该角色的体型（见 macro_for）。不给就用全局 MACRO。

    `neutralize` 不给时按景别自动决定：`subj_frac > NEUTRALIZE_SUBJ_FRAC` 才做。
    """
    HumanService, TargetService, RigService, tdir = _mpfb()
    origin = root.matrix_world.to_translation()

    # 重跑守卫：直接在**已建好**的 .blend 上重跑建场脚本，会再造一具人形叠上去
    # （实测叠到第四具才发现——画面里看到的是最早那一具，改动"看起来没生效"）。
    # 正确流程是先从场景主档 copy 一份干净的 .blend 再跑。
    _existing = [o for o in bpy.data.objects if o.name.startswith(name)]
    if _existing:
        print(f"  [warn] 场景里已有 {len(_existing)} 个 {name}* —— 你多半在已建好的 blend 上重跑了。"
              f"请先从场景主档 copy 一份干净的 .blend，否则人形会一具具叠加。")

    macro = macro_for(body_spec)
    if body_spec:
        print(f"  体型：{body_spec} → height={macro['height']:.3f} age={macro['age']:.2f} "
              f"muscle={macro['muscle']:.2f} weight={macro['weight']:.2f}")
    body = HumanService.create_human(macro_detail_dict=macro)
    body.name = name
    for sub, tname, w in LIMB_TARGETS:
        TargetService.load_target(body, os.path.join(tdir, sub, tname + ".target.gz"), weight=w, name=tname)
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = body
    body.select_set(True)
    arm = HumanService.add_builtin_rig(body, "default")
    arm.name = name + "_rig"
    bpy.context.view_layer.update()

    # ---- 静默姿态对齐 proxy：四肢竖直向下、手指向下 ----
    bpy.ops.object.select_all(action="DESELECT")
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="POSE")
    down = Vector((0, 0, -1))
    for s in ("L", "R"):
        _aim(arm, f"upperarm01.{s}", f"lowerarm01.{s}", down)
        _aim(arm, f"lowerarm01.{s}", f"wrist.{s}", down)
        _aim(arm, f"wrist.{s}", f"finger3-1.{s}", down)     # 手心朝内、指尖向下
        _aim(arm, f"upperleg01.{s}", f"lowerleg01.{s}", down)
        _aim(arm, f"lowerleg01.{s}", f"foot.{s}", down)
        for fn in (2, 3, 4, 5):
            _aim(arm, f"finger{fn}-1.{s}", f"finger{fn}-2.{s}", down)
            _aim(arm, f"finger{fn}-2.{s}", f"finger{fn}-3.{s}", down)
            _aim_tail(arm, f"finger{fn}-3.{s}", down)
    bpy.ops.object.mode_set(mode="OBJECT")
    RigService.apply_pose_as_rest_pose(arm)
    bpy.context.view_layer.update()

    # ---- 落地：最低点归零，并平移到 root 处 ----
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    zmin = min(v.co.z for v in ev.data.vertices)
    # MPFB 把网格挂在骨架下（body.parent == arm），只移骨架即可——两者都移会叠加成双倍偏移，
    # 骨架修改器随之把网格拉成长条（2026-08-18 实测教训）。
    arm.location = arm.location + origin + Vector((0.0, 0.0, -zmin))
    if body.parent is not arm:
        body.location = body.location + origin + Vector((0.0, 0.0, -zmin))
    bpy.context.view_layer.update()

    # ---- 中性化（去脸 / 去解剖细节）----
    # 插在这里有两个硬约束：必须在**绑骨之后**（顶点组才存在）、**赋材质之前**
    # （删头会改多边形集合）。判据见 NEUTRALIZE_SUBJ_FRAC。
    do_neutral = neutralize
    if do_neutral is None:
        do_neutral = subj_frac is not None and subj_frac > NEUTRALIZE_SUBJ_FRAC
    head_ob = None
    if do_neutral:
        head_ob = neutralize_human(body, material=skin_mat, head_parent=J.get("head"))
    elif subj_frac is not None:
        print(f"  中性化：跳过（人占画高 {subj_frac:.2f} ≤ {NEUTRALIZE_SUBJ_FRAC}，脸在成片里不可读）")

    # ---- 材质：手/脚亮色、头浅色、其余绿 ----
    hand_bones = set()
    foot_bones = set()
    head_bones = {"head", "neck01", "neck02", "neck03"}
    for b in arm.data.bones:
        n = b.name
        if n.startswith(("wrist", "metacarpal", "finger")):
            hand_bones.add(n)
        if n.startswith(("foot", "toe")):
            foot_bones.add(n)
        if n.startswith(("temporalis", "oculi", "jaw", "eye", "tongue", "oris", "levator", "risorius", "orbicularis", "special")):
            head_bones.add(n)
    v_hand = _bone_verts(body, hand_bones)
    v_foot = _bone_verts(body, foot_bones)
    v_head = _bone_verts(body, head_bones)
    body.data.materials.clear()
    body.data.materials.append(body_mat)   # 0
    body.data.materials.append(limb_mat)   # 1
    body.data.materials.append(skin_mat)   # 2
    for p in body.data.polygons:
        vs = p.vertices
        n_hand = sum(1 for i in vs if i in v_hand or i in v_foot)
        n_head = sum(1 for i in vs if i in v_head)
        if n_hand * 2 >= len(vs):
            p.material_index = 1
        elif n_head * 2 >= len(vs):
            p.material_index = 2
        else:
            p.material_index = 0
        p.use_smooth = True
    for m in body.modifiers:
        if m.type == "SUBSURF":
            m.levels, m.render_levels = 1, 2

    # ---- 约束：脱父 + Child Of（在静默姿态下 set inverse）----
    bpy.ops.object.select_all(action="DESELECT")
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    for key, bnames in BONE_MAP.items():
        for bname in ((bnames,) if isinstance(bnames, str) else bnames):
            eb = arm.data.edit_bones.get(bname)
            if eb is None:
                continue
            eb.use_connect = False
            eb.parent = None
    bpy.ops.object.mode_set(mode="POSE")
    for key, bnames in BONE_MAP.items():
        target = root if key == "__root__" else J.get(key)
        if target is None:
            continue
        for bname in ((bnames,) if isinstance(bnames, str) else bnames):
            pb = arm.pose.bones.get(bname)
            if pb is None:
                continue
            con = pb.constraints.new("CHILD_OF")
            con.name = f"follow_{key}"
            con.target = target
            with bpy.context.temp_override(object=arm, active_pose_bone=pb, pose_bone=pb, constraint=con):
                bpy.ops.constraint.childof_set_inverse(constraint=con.name, owner="BONE")
    bpy.ops.object.mode_set(mode="OBJECT")

    link(body)
    link(arm)
    if head_ob is not None:
        link(head_ob)
    arm.hide_render = True
    arm.hide_viewport = True
    return body, arm


def hide_proxy_meshes(collection, keep_prefixes: tuple[str, ...] = ()) -> int:
    """隐藏关节 proxy 的网格（保留空物件）。返回隐藏数。"""
    n = 0
    for ob in collection.objects:
        if ob.type == "MESH" and ob.name.startswith("PVZ_") and not ob.name.startswith(keep_prefixes):
            ob.hide_render = True
            ob.hide_viewport = True
            n += 1
    return n
