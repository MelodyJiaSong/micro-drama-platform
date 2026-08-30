"""Fill entropy_city with surrounding city fabric so the aerial shots (01, 52)
read as a city rather than a film-set strip.

Additive only: blocks are placed OUTSIDE the existing corridor footprints
(plaza, street, bridge deck, tunnel), so no existing previz framing changes.
Deterministic seed — re-running produces the identical city.
"""
import sys, random
import bpy

argv = sys.argv[sys.argv.index("--") + 1:]
blend, out = argv[0], argv[1]
bpy.ops.wm.open_mainfile(filepath=blend)

PREFIX = "FABRIC_"
for ob in [o for o in bpy.data.objects if o.name.startswith(PREFIX)]:
    bpy.data.objects.remove(ob, do_unlink=True)

# Keep-out footprints (x_min, x_max, y_min, y_max) with clearance already baked in.
KEEPOUT = [
    (-34, 34, -34, 34),      # plaza + its towers
    (-22, 22, 30, 210),      # main street + shops
    (-64, 64, 244, 276),     # bridge deck + parapets
    (-14, 14, -170, -20),    # tunnel approach
]

def blocked(x, y, hx, hy):
    for x0, x1, y0, y1 in KEEPOUT:
        if x + hx > x0 and x - hx < x1 and y + hy > y0 and y - hy < y1:
            return True
    return False

rng = random.Random(20260830)
coll = bpy.context.scene.collection
made = 0
# Grid over the whole city extent; jitter each cell so the skyline is not a lattice.
for gx in range(-9, 10):
    for gy in range(-8, 20):
        cx = gx * 30.0 + rng.uniform(-6, 6)
        cy = gy * 30.0 + rng.uniform(-6, 6)
        # Taller towers toward the plaza core, low-rise at the edges.
        dist = (cx * cx + cy * cy) ** 0.5
        if dist > 300:
            continue
        core = max(0.0, 1.0 - dist / 300.0)
        h = rng.uniform(8, 20) + core * rng.uniform(10, 46)
        sx = rng.uniform(10, 22)
        sy = rng.uniform(10, 22)
        if blocked(cx, cy, sx / 2, sy / 2):
            continue
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, h / 2))
        ob = bpy.context.active_object
        ob.name = f"{PREFIX}BLOCK_{made:03d}"
        ob.scale = (sx, sy, h)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        ob.rotation_euler[2] = rng.uniform(-0.05, 0.05)
        made += 1

bpy.ops.wm.save_as_mainfile(filepath=out)
print(f"FABRIC_ADDED {made}")
