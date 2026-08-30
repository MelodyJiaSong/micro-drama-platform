"""Render a scene .blend as a straight-down plan view (the spatial contract).

Orthographic top-down so distances read as true distances: this image is a
floor plan, not a look reference. Frames the whole scene bounding box with a
5% margin and burns nothing else in.
"""
import os, sys, math
import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
blend, out = argv[0], argv[1]
res = int(argv[2]) if len(argv) > 2 else 2048
# Optional "x0,x1,y0,y1" to frame one Place instead of the whole World.
region = None
if len(argv) > 3 and argv[3]:
    region = [float(v) for v in argv[3].split(",")]

bpy.ops.wm.open_mainfile(filepath=blend)

lo = Vector(( 1e9,  1e9,  1e9))
hi = Vector((-1e9, -1e9, -1e9))
found = False
for ob in bpy.context.scene.objects:
    if ob.type != "MESH" or not ob.visible_get():
        continue
    found = True
    for c in ob.bound_box:
        w = ob.matrix_world @ Vector(c)
        lo = Vector((min(lo[i], w[i]) for i in range(3)))
        hi = Vector((max(hi[i], w[i]) for i in range(3)))
if not found:
    raise SystemExit("no visible mesh in scene")

if region is not None:
    x0, x1, y0, y1 = region
    lo = Vector((x0, y0, lo.z))
    hi = Vector((x1, y1, hi.z))

center = (lo + hi) / 2.0
ext_x = (hi.x - lo.x) * 1.05
ext_y = (hi.y - lo.y) * 1.05
span = max(ext_x, ext_y)

cam_data = bpy.data.cameras.new("plan_cam")
cam_data.type = "ORTHO"
cam_data.ortho_scale = span
cam = bpy.data.objects.new("plan_cam", cam_data)
bpy.context.scene.collection.objects.link(cam)
cam.location = (center.x, center.y, hi.z + max(span, 50.0))
cam.rotation_euler = (0.0, 0.0, 0.0)  # straight down, +Y up in frame
bpy.context.scene.camera = cam

sun_data = bpy.data.lights.new("plan_sun", type="SUN")
sun_data.energy = 3.0
sun = bpy.data.objects.new("plan_sun", sun_data)
bpy.context.scene.collection.objects.link(sun)
sun.rotation_euler = (math.radians(35), 0.0, math.radians(35))

sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
# Frame matches the scene's own aspect so a long street does not render as a
# thin ribbon inside a square of empty ground.
if ext_x >= ext_y:
    sc.render.resolution_x = res
    sc.render.resolution_y = max(64, int(round(res * ext_y / ext_x)))
else:
    sc.render.resolution_y = res
    sc.render.resolution_x = max(64, int(round(res * ext_x / ext_y)))
sc.render.resolution_percentage = 100
sc.render.film_transparent = False
sc.render.filepath = os.path.abspath(out)
sc.render.image_settings.file_format = "PNG"
bpy.ops.render.render(write_still=True)

print(f"PLAN_BBOX min=({lo.x:.2f},{lo.y:.2f},{lo.z:.2f}) "
      f"max=({hi.x:.2f},{hi.y:.2f},{hi.z:.2f}) "
      f"extent={ext_x:.1f}m x {ext_y:.1f}m")
print(f"PLAN_OK {out}")
