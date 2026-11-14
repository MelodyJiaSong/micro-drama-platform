"""真实尺度 · 并排横移场景原型（剧级 _tools，bible §2.3 / §8）。

在 Blender 里运行（MCP execute_blender_code 或 `blender --background --python`）：
    exec(open(r"<本文件>", encoding="utf-8").read())
    build_lineup(items, out_check_path)

items: [{"key": str, "label": str, "height_m": float, "length_m": float, "width_m": float | None,
         "object": str | None, "landmark_ratio": float | None, "sort_value": float | None}]
  - height_m 是该期主口径的高度（ep01 = 肩高）。
  - object 为空时用占位方块（原型阶段）；给出已导入模型的对象名时，按 height_m 缩放并落地。
  - model_path：模型文件（.glb/.gltf/.fbx/.obj）；给出时先 import_model() 导入、合并成一个网格、
    命名 subj_<key>，再按 height_m 缩放。yaw_deg：绕竖轴转多少度才让头朝 +X（统一朝向）；
    vertex_color_srgb：顶点色是 sRGB 值却按线性存的模型（TripoSR 产物，见其 .json），导入时补伽马。
    auto_align：先按水平面主成分把身体长轴转到 X（只转最近的方向，不翻头尾），再按 yaw_deg 转。
    drop_islands：删掉面数不到最大块该比例的离散碎块（TripoSR 尾尖等会断成浮空小块；AI 模型取 0.02）。
    x_stretch：转正后沿 X（体长方向）的校正倍数，让侧视长高比对上参考图剪影（AI 模型；≤ 8%，bible §7 3a）。
  - landmark_ratio：模型上「主口径测量点」的离地高度 ÷ 模型包围盒总高（例如肩高 ÷ 头顶高），
    每个模型标定一次、记进该期 models.json；缺省 1.0 表示主口径就是包围盒总高（bible §4.3）。
  - sort_value：列队排序依据，缺省用 height_m；从小到大登场，冠军最后。
产出：场景（主体、人体参照、地面、相机动画）与比例机检 JSON（bible §7 第 2、3 条）。
注意：build_lineup 是早期试排原型（人站在主体前方、35 mm），正片用 build_ep.py（人与主体同纵深、135 mm）；本文件其余函数为公共函数。
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import bpy
from mathutils import Vector

HUMAN_HEIGHT_M = 1.75
FRAME_FILL = 0.6          # 当前对象占画面高度的比例
PITCH_DEG = 6.0           # 相机俯角
FPS = 30
HOLD_S = 3.0              # 每个对象停留
MOVE_S = 1.5              # 相邻对象之间的移动
TOP_SLOW = 1.5            # 前 5 名停留倍数
TOLERANCE = 0.02          # 比例机检阈值（bible §7）
COLL = "TrueScale"


def _collection() -> bpy.types.Collection:
    coll = bpy.data.collections.get(COLL)
    if coll is None:
        coll = bpy.data.collections.new(COLL)
        bpy.context.scene.collection.children.link(coll)
    return coll


def _clear() -> None:
    coll = bpy.data.collections.get(COLL)
    if coll is None:
        return
    for obj in list(coll.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


def _link(obj: bpy.types.Object) -> bpy.types.Object:
    for c in obj.users_collection:
        c.objects.unlink(obj)
    _collection().objects.link(obj)
    return obj


def world_bbox(obj: bpy.types.Object) -> tuple[Vector, Vector]:
    """对象及其子网格的世界包围盒（min, max）。"""
    objs = [obj] + [c for c in obj.children_recursive]
    pts = [o.matrix_world @ Vector(c) for o in objs if o.type == "MESH" for c in o.bound_box]
    if not pts:
        loc = obj.matrix_world.translation
        return loc.copy(), loc.copy()
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return lo, hi


def _placeholder(item: dict) -> bpy.types.Object:
    w = item.get("width_m") or item["length_m"] * 0.35
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    obj = bpy.context.active_object
    obj.name = f"subj_{item['key']}"
    obj.scale = (item["length_m"], w, item["height_m"])
    bpy.ops.object.transform_apply(scale=True)
    return _link(obj)


def _vcol_material(obj: bpy.types.Object) -> None:
    """顶点色（sRGB 值按线性存）→ 伽马 2.2 → Principled；节点按类型找，不按名字。"""
    mat = bpy.data.materials.new(f"mat_{obj.name}")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    vc = nt.nodes.new("ShaderNodeVertexColor")
    vc.layer_name = obj.data.color_attributes[0].name
    gamma = nt.nodes.new("ShaderNodeGamma")
    gamma.inputs[1].default_value = 2.2
    nt.links.new(vc.outputs["Color"], gamma.inputs[0])
    nt.links.new(gamma.outputs[0], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.8
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def _major_axis_angle(obj: bpy.types.Object) -> float:
    """水平面内顶点主成分方向与 +X 的夹角（弧度，取 ±90° 内）。"""
    import numpy as np
    xy = np.array([v.co[:2] for v in obj.data.vertices])
    xy -= xy.mean(0)
    w, v = np.linalg.eigh(np.cov(xy.T))
    ax = v[:, int(np.argmax(w))]
    if ax[0] < 0:
        ax = -ax
    return math.atan2(ax[1], ax[0])


def _drop_islands(obj: bpy.types.Object, frac: float) -> int:
    """按连通块删碎块，返回删掉的块数。"""
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    seen: set[int] = set()
    parts: list[list] = []
    for f in bm.faces:
        if f.index in seen:
            continue
        stack, part = [f], []
        seen.add(f.index)
        while stack:
            cur = stack.pop()
            part.append(cur)
            for e in cur.edges:
                for nb in e.link_faces:
                    if nb.index not in seen:
                        seen.add(nb.index)
                        stack.append(nb)
        parts.append(part)
    biggest = max(len(pp) for pp in parts)
    small = [pp for pp in parts if len(pp) < biggest * frac]
    if small:
        bmesh.ops.delete(bm, geom=[f for pp in small for f in pp], context="FACES")
        loose = [v for v in bm.verts if not v.link_faces]
        bmesh.ops.delete(bm, geom=loose, context="VERTS")
        bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
    return len(small)


def import_model(item: dict) -> bpy.types.Object:
    """导入 model_path，合并网格、应用变换、按 yaw_deg 转到头朝 +X，命名 subj_<key>。"""
    path = Path(item["model_path"])
    before = set(bpy.data.objects)
    ext = path.suffix.lower()
    if ext in (".glb", ".gltf"):
        bpy.ops.import_scene.gltf(filepath=str(path))
    elif ext == ".fbx":
        bpy.ops.import_scene.fbx(filepath=str(path))
    elif ext == ".obj":
        bpy.ops.wm.obj_import(filepath=str(path))
    else:
        raise ValueError(f"不支持的模型格式：{path}")
    new = [o for o in bpy.data.objects if o not in before]
    meshes = [o for o in new if o.type == "MESH"]
    if not meshes:
        raise ValueError(f"模型里没有网格：{path}")
    bpy.ops.object.select_all(action="DESELECT")
    for o in meshes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    if len(meshes) > 1:
        bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    obj.parent = None
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    for o in new:
        if o.name in bpy.data.objects and o is not obj:
            bpy.data.objects.remove(o, do_unlink=True)
    obj.name = f"subj_{item['key']}"
    if item.get("drop_islands"):
        obj["islands_dropped"] = _drop_islands(obj, item["drop_islands"])
    yaw = math.radians(item.get("yaw_deg") or 0.0)
    if item.get("auto_align"):
        yaw -= _major_axis_angle(obj)
    obj.rotation_mode = "XYZ"   # glTF 导入默认四元数模式，不改的话 rotation_euler 不生效
    obj.rotation_euler = (0.0, 0.0, yaw)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    if item.get("x_stretch"):
        obj.scale = (item["x_stretch"], 1.0, 1.0)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if item.get("vertex_color_srgb") and obj.data.color_attributes:
        _vcol_material(obj)
    bpy.context.view_layer.update()
    return _link(obj)


def shoulder_ratio(obj: bpy.types.Object, slices: int = 30, jump: float = 0.06) -> dict:
    """头朝 +X 的四足模型：自动估肩高 ÷ 包围盒总高（bible §4.3 标定的初值）。

    沿 X 切片取各段顶高（÷ 总高）。从尾向头找第一处陡升（相邻段升幅 > jump，且在后 40% 之后）
    作为颈部起点，肩高 = 起点之前各段顶高的最大值；没有陡升（犀牛、象），去掉最前 15% 再取最大。
    只是初值：必须看侧视标线图确认后才写进 models.json。
    """
    vs = [obj.matrix_world @ v.co for v in obj.data.vertices]
    lo_x, hi_x = min(v.x for v in vs), max(v.x for v in vs)
    z0, z1 = min(v.z for v in vs), max(v.z for v in vs)
    h = z1 - z0
    prof: list[float | None] = []
    for i in range(slices):
        a, b = lo_x + (hi_x - lo_x) * i / slices, lo_x + (hi_x - lo_x) * (i + 1) / slices
        zs = [v.z for v in vs if a <= v.x < b]
        prof.append((max(zs) - z0) / h if zs else None)
    start = int(slices * 0.4)
    neck = next((i for i in range(start, slices)
                 if prof[i] is not None and prof[i - 1] is not None and prof[i] - prof[i - 1] > jump), None)
    body = prof[:neck] if neck is not None else prof[: int(slices * 0.85)]
    vals = [p for p in body if p is not None]
    ratio = max(vals)
    idx = body.index(ratio)
    return {"ratio": round(ratio, 4), "x_m": lo_x + (hi_x - lo_x) * (idx + 0.5) / slices,
            "neck_slice": neck, "method": "auto-profile", "profile": [None if p is None else round(p, 3) for p in prof]}


def _fit_model(item: dict) -> bpy.types.Object:
    """已导入模型：按主口径高度等比缩放，落地。"""
    obj = import_model(item) if item.get("model_path") else bpy.data.objects[item["object"]]
    lo, hi = world_bbox(obj)
    ratio = item.get("landmark_ratio") or 1.0
    k = item["height_m"] / max((hi.z - lo.z) * ratio, 1e-9)
    obj.scale = obj.scale * k
    bpy.context.view_layer.update()
    return _link(obj)


HUMAN_TEMPLATE = "human_template_mpfb"


def _human_template() -> bpy.types.Object | None:
    """MPFB（自带素材 CC0）男性基础人体，烘焙成静态网格并缩放到 1.75 m；没装 MPFB 时返回 None。"""
    tpl = bpy.data.objects.get(HUMAN_TEMPLATE)
    if tpl is not None:
        return tpl
    try:
        from bl_ext.blender_org.mpfb.services.humanservice import HumanService
        from bl_ext.blender_org.mpfb.services.targetservice import TargetService
    except ImportError:
        return None
    macro = TargetService.get_default_macro_info_dict()
    macro.update({"gender": 1.0, "age": 0.5, "muscle": 0.5, "weight": 0.5})
    base = HumanService.create_human(macro_detail_dict=macro)
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    mesh = bpy.data.meshes.new_from_object(base.evaluated_get(deps))
    tpl = bpy.data.objects.new(HUMAN_TEMPLATE, mesh)
    bpy.context.scene.collection.objects.link(tpl)
    for o in [base] + list(base.children_recursive):
        bpy.data.objects.remove(o, do_unlink=True)
    lo, hi = world_bbox(tpl)
    tpl.scale = (HUMAN_HEIGHT_M / (hi.z - lo.z),) * 3
    bpy.context.view_layer.update()
    lo, _ = world_bbox(tpl)
    tpl.location.z -= lo.z
    mat = bpy.data.materials.get("human_clay") or bpy.data.materials.new("human_clay")
    mat.use_nodes = True
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (0.82, 0.80, 0.77, 1)
    bsdf.inputs["Roughness"].default_value = 0.6
    tpl.data.materials.clear()
    tpl.data.materials.append(mat)
    tpl.hide_render = True
    tpl.hide_set(True)
    return tpl


def _human(name: str) -> bpy.types.Object:
    """人体参照 1.75 m（bible §1 D3）：优先 MPFB 模板的共享网格副本，否则胶囊体占位。"""
    tpl = _human_template()
    if tpl is not None:
        man = tpl.copy()
        man.name = name
        man.hide_render = False
        _link(man)
        man.hide_set(False)
        man.location = (0.0, 0.0, 0.0)
        return man
    r = 0.2
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=HUMAN_HEIGHT_M - 2 * r)
    body = bpy.context.active_object
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(0, 0, (HUMAN_HEIGHT_M - 2 * r) / 2))
    top = bpy.context.active_object
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(0, 0, -(HUMAN_HEIGHT_M - 2 * r) / 2))
    bottom = bpy.context.active_object
    for o in (body, top, bottom):
        o.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.join()
    body.name = name
    return _link(body)


def _ground(extent_x: float, depth: float) -> None:
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(extent_x / 2, 0, 0))
    g = bpy.context.active_object
    g.name = "ground"
    g.scale = (extent_x + 200, depth * 2 + 200, 1)
    mat = bpy.data.materials.new("ground_grid")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    tex = nt.nodes.new("ShaderNodeTexChecker")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    nt.links.new(geo.outputs["Position"], tex.inputs["Vector"])
    tex.inputs["Scale"].default_value = 1.0          # 世界坐标；棋盘格每格边长 = 1 / Scale = 1 m
    tex.inputs["Color1"].default_value = (0.42, 0.38, 0.31, 1)
    tex.inputs["Color2"].default_value = (0.36, 0.325, 0.26, 1)
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    g.data.materials.append(mat)
    _link(g)


def _camera_for(obj: bpy.types.Object, man: bpy.types.Object, cam: bpy.types.Object) -> tuple[Vector, float]:
    """主体与它的人体参照一起入画：高度占 FRAME_FILL，宽度不超过画面 85%。"""
    lo, hi = world_bbox(obj)
    mlo, mhi = world_bbox(man)
    x0, x1 = min(lo.x, mlo.x), max(hi.x, mhi.x)
    h = max(hi.z - lo.z, HUMAN_HEIGHT_M)
    fov_y, fov_x = cam.data.angle_y, cam.data.angle_x
    dist_h = (h / FRAME_FILL / 2) / math.tan(fov_y / 2)
    dist_w = ((x1 - x0) / 0.85 / 2) / math.tan(fov_x / 2)
    dist = max(dist_h, dist_w) + (hi.y - lo.y) / 2
    pitch = math.radians(PITCH_DEG)
    target = Vector(((x0 + x1) / 2, 0.0, h * 0.5))
    eye = target + Vector((0.0, -dist * math.cos(pitch), dist * math.sin(pitch)))
    return eye, pitch


def build_lineup(items: list[dict], out_check_path: str | None = None) -> dict:
    _clear()
    items = sorted(items, key=lambda it: it.get("sort_value") or it["height_m"])
    subjects: list[tuple[dict, bpy.types.Object]] = []
    x = 0.0
    prev_len = 0.0
    for it in items:
        obj = _fit_model(it) if (it.get("object") or it.get("model_path")) else _placeholder(it)
        lo, hi = world_bbox(obj)
        length = hi.x - lo.x
        gap = max(prev_len, length) * 0.6 + 1.0 + 0.6   # 0.6 m 给人体参照留位
        x += gap if subjects else 0.0
        obj.location.x += x - lo.x
        obj.location.y -= (lo.y + hi.y) / 2
        obj.location.z -= lo.z
        bpy.context.view_layer.update()
        man = _human(f"human_{it['key']}")
        man.location = (x - 0.5, -((hi.y - lo.y) / 2) - 0.3, 0.0)
        bpy.context.view_layer.update()
        mlo, mhi = world_bbox(man)
        man.location += Vector((x - 0.5 - (mlo.x + mhi.x) / 2, 0.0, -mlo.z))   # 站在主体左前方、脚底落地
        x += length
        prev_len = length
        subjects.append((it, obj))
    bpy.context.view_layer.update()
    depth = max((world_bbox(o)[1].y - world_bbox(o)[0].y) for _, o in subjects)
    _ground(x, depth)

    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
    cam = scene.camera
    if cam is None:
        bpy.ops.object.camera_add()
        cam = bpy.context.active_object
        scene.camera = cam
    cam.data.lens = 35
    cam.data.clip_end = 100000
    cam.animation_data_clear()
    frame = 1
    n = len(subjects)
    for i, (it, obj) in enumerate(subjects):
        eye, pitch = _camera_for(obj, bpy.data.objects[f"human_{it['key']}"], cam)
        cam.location = eye
        cam.rotation_euler = (math.pi / 2 - pitch, 0.0, 0.0)
        hold = HOLD_S * (TOP_SLOW if i >= n - 5 else 1.0)
        for f in (frame, frame + int(hold * FPS)):
            cam.keyframe_insert("location", frame=f)
            cam.keyframe_insert("rotation_euler", frame=f)
        frame += int((hold + MOVE_S) * FPS)
    scene.frame_start, scene.frame_end = 1, frame
    return scale_check(subjects, out_check_path)


def scale_check(subjects: list[tuple[dict, bpy.types.Object]], out_path: str | None) -> dict:
    """bible §7：每个主体实测高度 vs 数据；每个人体参照 1.75 m ± 1%。"""
    rows = []
    for it, obj in subjects:
        lo, hi = world_bbox(obj)
        measured = (hi.z - lo.z) * (it.get("landmark_ratio") or 1.0)
        err = abs(measured - it["height_m"]) / it["height_m"]
        man = bpy.data.objects[f"human_{it['key']}"]
        mlo, mhi = world_bbox(man)
        h_err = abs((mhi.z - mlo.z) - HUMAN_HEIGHT_M) / HUMAN_HEIGHT_M
        rows.append({
            "key": it["key"], "expected_height_m": it["height_m"], "measured_height_m": round(measured, 4),
            "error": round(err, 5), "grounded": abs(lo.z) < 0.01,
            "human_height_m": round(mhi.z - mlo.z, 4), "human_ok": h_err <= 0.01,
            "pass": err <= TOLERANCE and abs(lo.z) < 0.01 and h_err <= 0.01,
        })
    result = {"tolerance": TOLERANCE, "all_pass": all(r["pass"] for r in rows), "items": rows}
    if out_path:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        Path(out_path).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result
