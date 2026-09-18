# -*- coding: utf-8 -*-
"""量一个网格文件的包围盒，打印 `BBOX dx dy dz`。给 build_objects.py 自动判朝向用。

用法：blender -b --factory-startup --python tools/mesh_bbox.py -- <mesh>
"""
import sys
import bpy
from mathutils import Vector

src = sys.argv[sys.argv.index("--") + 1:][0]
bpy.ops.wm.read_factory_settings(use_empty=True)
low = src.lower()
if low.endswith((".glb", ".gltf")):
    bpy.ops.import_scene.gltf(filepath=src)
elif low.endswith(".obj"):
    bpy.ops.wm.obj_import(filepath=src)
elif low.endswith(".fbx"):
    bpy.ops.import_scene.fbx(filepath=src)
else:
    bpy.ops.wm.open_mainfile(filepath=src)
ms = [o for o in bpy.data.objects if o.type == "MESH"]
lo = Vector(tuple(min(min((o.matrix_world @ Vector(c))[i] for c in o.bound_box) for o in ms) for i in range(3)))
hi = Vector(tuple(max(max((o.matrix_world @ Vector(c))[i] for c in o.bound_box) for o in ms) for i in range(3)))
d = hi - lo
print("BBOX %.6f %.6f %.6f" % (d.x, d.y, d.z))
