"""BG1_TOWER_4 sat at (0,30) 22m wide — squarely across the plaza's north
opening, so the car in shot16 (冲出广场驶入主街) had a building in its path.
Split it into two blocks flanking the corridor; the opening (x -7..7, the road
width) is now clear and the two blocks frame the street mouth."""
import sys, bpy
argv = sys.argv[sys.argv.index("--")+1:]
blend, out = argv[0], argv[1]
bpy.ops.wm.open_mainfile(filepath=blend)

old = bpy.data.objects.get("BG1_TOWER_4")
if old:
    bpy.data.objects.remove(old, do_unlink=True)

def box(name, dim, loc):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = dim
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

box("BG1_TOWER_4L", (14.0, 10.0, 20.0), (-15.0, 31.0, 10.0))
box("BG1_TOWER_4R", (14.0, 10.0, 24.0), ( 15.0, 31.0, 12.0))

blockers = []
for ob in bpy.context.scene.objects:
    if ob.type != "MESH":
        continue
    l = ob.location
    d = ob.dimensions
    # anything overlapping the plaza→street corridor (x -8..8, y 25..45)
    if (abs(l.x) - d.x/2) < 8 and (l.y + d.y/2) > 25 and (l.y - d.y/2) < 45:
        if not ob.name.startswith(("BG2_ROAD", "BG1_PLAZA")):
            blockers.append(ob.name)
bpy.ops.wm.save_as_mainfile(filepath=out)
print("CORRIDOR_BLOCKERS:", blockers if blockers else "none")
