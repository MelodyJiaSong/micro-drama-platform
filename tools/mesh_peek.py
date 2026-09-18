# -*- coding: utf-8 -*-
"""白模出炉后的那一眼：三张灰模快照（iso / top / side），给人看形状对不对。

存在的理由是 `ai_video.md` rule 4h §G「**出了模型必须先渲一眼再往下做**，
别拿没看过的网格去绑定 / 做 previz」。闸门只量得出体量与探针，量不出
「它长得像不像一条船」——那一条只能靠看。2026-09-17 sk1 实测：Rodin 把
4:1 的漕船出成了 1.25:1，闸门的包围盒读数会报出来，但**是这张 iso 快照
让人一眼看懂"它把船压方了"**，而不是看懂"偏差 236.9%"。

用法：
    blender -b --factory-startup --python tools/mesh_peek.py -- <mesh> <out.png>
写出 <out>_iso.png / _top.png / _side.png（路径必须是绝对路径）。
"""
import bpy, sys, math, os
from mathutils import Vector
a = sys.argv[sys.argv.index("--")+1:]
src, out = a[0], a[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
if src.lower().endswith(".blend"):
    with bpy.data.libraries.load(src) as (fr, to):
        to.objects = list(fr.objects)
    for o in to.objects:
        if o is not None:
            bpy.context.scene.collection.objects.link(o)
else:
    bpy.ops.import_scene.gltf(filepath=src)
obs = [o for o in bpy.data.objects if o.type == "MESH"]
for o in obs:
    for s in o.material_slots:
        s.material = None
lo = Vector((1e9,)*3); hi = Vector((-1e9,)*3)
for o in obs:
    for v in o.data.vertices:
        w = o.matrix_world @ v.co
        for i in range(3):
            lo[i] = min(lo[i], w[i]); hi[i] = max(hi[i], w[i])
c = (lo+hi)/2; r = max(hi-lo)
cam_d = bpy.data.cameras.new("c"); cam_d.type = "ORTHO"; cam_d.ortho_scale = r * 1.15; cam = bpy.data.objects.new("c", cam_d); bpy.context.scene.collection.objects.link(cam)
bpy.context.scene.camera = cam
sun_d = bpy.data.lights.new("s", 'SUN'); sun_d.energy = 4
sun = bpy.data.objects.new("s", sun_d); bpy.context.scene.collection.objects.link(sun)
sun.rotation_euler = (math.radians(50), 0, math.radians(40))
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = 900
sc.render.engine = 'BLENDER_WORKBENCH'
sc.render.film_transparent = False
for name, (az, el) in {"iso": (45, 25), "top": (0, 89), "side": (90, 0)}.items():
    ra, re_ = math.radians(az), math.radians(el)
    d = r * 2.2
    cam.location = c + Vector((math.cos(re_)*math.cos(ra), math.cos(re_)*math.sin(ra), math.sin(re_))) * d
    dirv = (c - cam.location).normalized()
    cam.rotation_euler = dirv.to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = out.replace(".png", f"_{name}.png")
    bpy.ops.render.render(write_still=True)
print("PEEK OK")
