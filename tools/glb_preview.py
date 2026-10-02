# -*- coding: utf-8 -*-
"""把一个 GLB 渲成四视图 PNG，用来**先看一眼再决定要不要用**。

为什么要有它：`ai_video.md` rule 4h §G 的硬规矩——**出了模型必须先渲一眼再往下做**，
别拿没看过的网格去绑定、去做 previz。生成式 3D 的失败是沉默的：
文件大小正常、闸门也能过，但形状可能已经塌成一团（rule 4h §G1 实测过一次）。

用法：
    blender -b --factory-startup --python tools/glb_preview.py -- --src x.glb --out x_preview.png
"""
import sys
import math
from pathlib import Path

import bpy


def argv():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    d = {}
    for i, x in enumerate(a):
        if x.startswith("--") and i + 1 < len(a):
            d[x[2:]] = a[i + 1]
    return d


def main():
    A = argv()
    src, out = Path(A["src"]), Path(A["out"])

    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(src))
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if not meshes:
        raise SystemExit("GLB 里没有网格")

    # 包围盒 → 把模型归一到单位尺度、坐在原点
    xs, ys, zs = [], [], []
    for o in meshes:
        for c in o.bound_box:
            w = o.matrix_world @ __import__("mathutils").Vector(c)
            xs.append(w.x); ys.append(w.y); zs.append(w.z)
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    span = max(max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)) or 1.0
    root = bpy.data.objects.new("root", None)
    bpy.context.scene.collection.objects.link(root)
    for o in meshes:
        if o.parent is None:
            o.parent = root
    root.location = (-cx, -cy, -min(zs))
    root.scale = (2.0 / span,) * 3

    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in \
        {i.identifier for i in sc.render.bl_rna.properties["engine"].enum_items} else "BLENDER_WORKBENCH"
    sc.render.resolution_x, sc.render.resolution_y = 640, 640
    sc.render.film_transparent = False
    w = bpy.data.worlds.new("w"); w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.25, 0.25, 0.27, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 1.5
    sc.world = w

    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(55), 0, math.radians(40))
    sc.collection.objects.link(sun)

    cam_d = bpy.data.cameras.new("cam"); cam_d.lens = 60
    cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam)
    sc.camera = cam
    tgt = bpy.data.objects.new("tgt", None); sc.collection.objects.link(tgt)
    tgt.location = (0, 0, 1.0)
    t = cam.constraints.new("TRACK_TO"); t.target = tgt
    t.track_axis, t.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"

    tiles = []
    for i, ang in enumerate((0, 90, 180, 270)):
        r = math.radians(ang)
        cam.location = (math.sin(r) * 4.2, -math.cos(r) * 4.2, 2.2)
        p = out.with_name(f"{out.stem}_{ang:03d}.png")
        sc.render.filepath = str(p)
        bpy.ops.render.render(write_still=True)
        tiles.append(p)
    print("[preview] " + " ".join(t.name for t in tiles))


main()
