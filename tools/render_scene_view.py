"""Render one clay (grey, untextured) perspective view from a scene .blend.

This is the structure reference a generation model actually uses: same camera,
same framing, exact building positions — and, being grey, it constrains
nothing about材质/色/光. Seedance 2.5 supports clay render as a first-class
reference modality for spatial structure and camera angle.

argv: <blend> <out.png> <px,py,pz> <tx,ty,tz> <focal_mm> [width]
"""
import os, sys, math
import bpy
from mathutils import Vector

a = sys.argv[sys.argv.index("--")+1:]
blend, out = a[0], a[1]
pos = Vector([float(v) for v in a[2].split(",")])
tgt = Vector([float(v) for v in a[3].split(",")])
focal = float(a[4])
width = int(a[5]) if len(a) > 5 else 1792

bpy.ops.wm.open_mainfile(filepath=blend)

cam_data = bpy.data.cameras.new("view_cam")
cam_data.lens = focal
cam_data.sensor_width = 36.0
cam = bpy.data.objects.new("view_cam", cam_data)
bpy.context.scene.collection.objects.link(cam)
cam.location = pos
d = (tgt - pos).normalized()
cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

sun = bpy.data.objects.new("view_sun", bpy.data.lights.new("view_sun", type="SUN"))
sun.data.energy = 2.5
bpy.context.scene.collection.objects.link(sun)
sun.rotation_euler = (math.radians(50), 0.0, math.radians(35))

sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sc.render.resolution_x = width
sc.render.resolution_y = int(round(width * 9 / 21))   # 21:9, same as the target
sc.render.resolution_percentage = 100
sc.render.filepath = os.path.abspath(out)
sc.render.image_settings.file_format = "PNG"
bpy.ops.render.render(write_still=True)
print("VIEW_OK " + out)
