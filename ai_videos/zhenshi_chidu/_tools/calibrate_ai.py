"""AI 模型（bible §4.1 第 3 档）标定：剪影校正 x_stretch、肩高 landmark_ratio、体长检查、标线图。

在 Blender 里运行（先 exec scene_lineup.py，再 exec 本文件）：
    calibrate(key, glb_path, sil_aspect, sh_m, hb_m, rule="auto", out_png=None) -> dict

rule：
  auto     shoulder_ratio() 自动估（颈部陡升前的最高点；无陡升则去掉最前 15%）
  croup    马科：臀高（后 45% 体长内的最高点；背线平，臀高≈肩高）
  foreleg  前腿正上方顶高：前腿所在 x（最前 40% 内、离地 15% 高处的顶点 x 中位数）处的顶高
  ratio=<r> 看图后人工给定
bible §7 3a：|x_stretch − 1| ≤ 0.08；模型长 ÷ 头体长在 0.7–1.15；标线图看图确认。
"""
from __future__ import annotations

import math

import bpy
from mathutils import Vector


def _profile_top(obj, x_a: float, x_b: float, z0: float, h: float) -> float:
    zs = [(obj.matrix_world @ v.co).z for v in obj.data.vertices if x_a <= (obj.matrix_world @ v.co).x < x_b]
    return (max(zs) - z0) / h if zs else 0.0


def foreleg_x(obj) -> float:
    """前腿 x：前半身内离地 15% 高以下顶点 x 的中位数（肩高标线画在这里，鬐甲在前腿正上方）。"""
    vs = [obj.matrix_world @ v.co for v in obj.data.vertices]
    lo_x, hi_x = min(v.x for v in vs), max(v.x for v in vs)
    z0, z1 = min(v.z for v in vs), max(v.z for v in vs)
    low = sorted(v.x for v in vs if v.z < z0 + (z1 - z0) * 0.15 and v.x > (lo_x + hi_x) / 2)
    return low[len(low) // 2]


def _ratio(obj, rule: str) -> tuple[float, str, float]:
    vs = [obj.matrix_world @ v.co for v in obj.data.vertices]
    lo_x, hi_x = min(v.x for v in vs), max(v.x for v in vs)
    z0, z1 = min(v.z for v in vs), max(v.z for v in vs)
    h, L = z1 - z0, hi_x - lo_x
    if rule.startswith("ratio="):
        return float(rule.split("=")[1]), "manual（看图标定）", lo_x + L * 0.6
    if rule == "croup":
        zs = [v for v in vs if v.x < lo_x + L * 0.45]
        top = max(zs, key=lambda v: v.z)
        return (top.z - z0) / h, "croup（马科臀高≈肩高）", top.x
    if rule == "foreleg":
        low = sorted(v.x for v in vs if v.z < z0 + h * 0.15 and v.x > hi_x - L * 0.4)
        fx = low[len(low) // 2]
        r = _profile_top(obj, fx - L * 0.04, fx + L * 0.04, z0, h)
        return r, "foreleg（前腿正上方顶高）", fx
    s = shoulder_ratio(obj)
    return s["ratio"], "auto-profile", s["x_m"]


def calibrate(key: str, glb: str, sil_aspect: float, sh_m: float, hb_m: float,
              rule: str = "auto", out_png: str | None = None) -> dict:
    base = {"key": key, "model_path": glb, "yaw_deg": 180, "auto_align": True,
            "vertex_color_srgb": True, "drop_islands": 0.02}
    obj = import_model(dict(base))
    lo, hi = world_bbox(obj)
    model_aspect = (hi.x - lo.x) / (hi.z - lo.z)
    fidelity = model_aspect / sil_aspect - 1
    stretch = round(sil_aspect / model_aspect, 4)
    bpy.data.objects.remove(obj, do_unlink=True)
    obj = import_model(dict(base, x_stretch=stretch))
    obj.location -= Vector((0, 0, world_bbox(obj)[0].z))
    bpy.context.view_layer.update()
    ratio, method, _x = _ratio(obj, rule)
    lo, hi = world_bbox(obj)
    x_at = foreleg_x(obj)
    k = sh_m / ((hi.z - lo.z) * ratio)
    length_m, width_m = (hi.x - lo.x) * k, (hi.y - lo.y) * k
    res = {
        "key": key, "x_stretch": stretch, "silhouette_fidelity": round(fidelity, 4),
        "x_stretch_ok": abs(stretch - 1) <= 0.08,
        "landmark_ratio": round(ratio, 4), "landmark_method": method,
        "length_m": round(length_m, 2), "width_m": round(width_m, 2),
        "length_over_hb": round(length_m / hb_m, 2), "length_ok": 0.7 <= length_m / hb_m <= 1.15,
        "landmark_x_frac": round((x_at - lo.x) / (hi.x - lo.x), 4),
        "islands_dropped": int(obj.get("islands_dropped", 0)),
    }
    if out_png:
        _landmark_render(obj, ratio, x_at, out_png)
    bpy.data.objects.remove(obj, do_unlink=True)
    return res


def _landmark_render(obj, ratio: float, x_at: float, out_png: str) -> None:
    """正交侧视标线图：红横线 = 肩高测量线，红竖线 = 成片肩高标杆位置（前腿）。"""
    scene = bpy.context.scene
    lo, hi = world_bbox(obj)
    h, L = hi.z - lo.z, hi.x - lo.x
    zline = lo.z + h * ratio
    tmp = []
    mat = bpy.data.materials.get("calib_red") or bpy.data.materials.new("calib_red")
    mat.use_nodes = True
    em = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    em.inputs["Base Color"].default_value = (1, 0, 0, 1)
    em.inputs["Emission Color"].default_value = (1, 0, 0, 1)
    em.inputs["Emission Strength"].default_value = 5
    for loc, scale in (((lo.x + L / 2, lo.y - 0.05 * L, zline), (L * 1.2, 0.001, h * 0.006)),
                       ((x_at, lo.y - 0.05 * L, lo.z + h / 2), (L * 0.004, 0.001, h * 1.1))):
        bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
        c = bpy.context.active_object
        c.scale = scale
        c.data.materials.append(mat)
        tmp.append(c)
    cam_data = bpy.data.cameras.new("calib_cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = max(L, h) * 1.25
    cam = bpy.data.objects.new("calib_cam", cam_data)
    scene.collection.objects.link(cam)
    cam.location = (lo.x + L / 2, lo.y - 10 * max(L, h), lo.z + h / 2)
    cam.rotation_euler = (math.pi / 2, 0, 0)
    old = (scene.camera, scene.render.resolution_x, scene.render.resolution_y, scene.render.filepath)
    hidden = [o for o in scene.objects if o.visible_get() and o not in (obj, *tmp, cam) and o.type == "MESH"]
    for o in hidden:
        o.hide_render = True
    scene.camera = cam
    scene.render.resolution_x = scene.render.resolution_y = 640
    scene.render.filepath = out_png
    fmt, scene.render.image_settings.file_format = scene.render.image_settings.file_format, "PNG"
    bpy.ops.render.render(write_still=True)
    scene.render.image_settings.file_format = fmt
    for o in hidden:
        o.hide_render = False
    scene.camera, scene.render.resolution_x, scene.render.resolution_y, scene.render.filepath = old
    for c in tmp:
        bpy.data.objects.remove(c, do_unlink=True)
    bpy.data.objects.remove(cam, do_unlink=True)
