import sys, bpy
argv = sys.argv[sys.argv.index("--")+1:]
blend, out = argv[0], argv[1]
bpy.ops.wm.open_mainfile(filepath=blend)
for ob in [o for o in bpy.data.objects if o.name.startswith("BG4_")]:
    bpy.data.objects.remove(ob, do_unlink=True)

Y0, Y1 = -20.0, -170.0
W, H = 14.0, 6.0
cy, ly = (Y0+Y1)/2.0, abs(Y1-Y0)

def box(name, dim, loc):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = dim
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return ob

box("BG4_TUNNEL_FLOOR", (W, ly, 0.2), (0, cy, -0.1))
box("BG4_TUNNEL_CEIL",  (W, ly, 0.3), (0, cy, H))
box("BG4_TUNNEL_WALL_L", (0.4, ly, H), (-W/2, cy, H/2))
box("BG4_TUNNEL_WALL_R", (0.4, ly, H), ( W/2, cy, H/2))
n = 0
y = Y0 - 6.0
while y > Y1 + 4.0:
    box("BG4_LIGHT_%02d" % n, (2.4, 0.5, 0.2), (0, y, H - 0.35))
    n += 1
    y -= 12.0
bpy.ops.wm.save_as_mainfile(filepath=out)
print("TUNNEL_OK lights=%d span=%.0fm" % (n, ly))
