"""Cycles: animated MPFB cast walking on a depth-mesh shadow catcher; renders RGBA (characters + shadows) for
compositing over the still plate.  blender -b -P render_street.py -- cfg.json
"""
import bpy, sys, json, math
import numpy as np
from mathutils import Vector, Matrix

cfg = json.load(open(sys.argv[sys.argv.index("--") + 1], encoding="utf-8"))
FPS = 24; NF = cfg.get("frames", 192)
HFOV = math.radians(cfg.get("hfov", 55))
A_, B_ = cfg["disp_a"], cfg["disp_b"]

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
prefs = bpy.context.preferences.addons["cycles"].preferences
for dt in ("OPTIX", "CUDA"):
    try:
        prefs.compute_device_type = dt; prefs.get_devices()
        for d in prefs.devices: d.use = True
        sc.cycles.device = "GPU"; break
    except Exception as e:
        print("device", dt, e)
sc.cycles.samples = cfg.get("samples", 64)
sc.cycles.use_denoising = True
sc.render.film_transparent = True
sc.render.resolution_x, sc.render.resolution_y = cfg.get("res", [1280, 720])
sc.render.fps = FPS; sc.frame_start, sc.frame_end = 1, NF
sc.render.use_motion_blur = cfg.get("motion_blur", True); sc.render.motion_blur_shutter = 0.5
sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGBA"
sc.view_settings.view_transform = "Standard"
try: sc.view_settings.look = "None"
except Exception: pass
sc.view_settings.exposure = cfg.get("exposure", 0.0)

w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
bg.inputs[0].default_value = (*cfg.get("sky_color", [0.55, 0.62, 0.75]), 1)
bg.inputs[1].default_value = cfg.get("sky_strength", 0.6)

# ---------- depth mesh (shadow catcher + holdout) ----------
dimg = bpy.data.images.load(cfg["depth"]); dimg.colorspace_settings.name = "Non-Color"
W, H = dimg.size
dpx = np.array(dimg.pixels[:], np.float32).reshape(H, W, 4)[::-1, :, 0]
def dist_of(disp): return 1.0 / (A_ * disp + B_)
t = math.tan(HFOV / 2)
STEP = cfg.get("step", 2)
xs = np.arange(0, W, STEP); ys = np.arange(0, H, STEP)
gx, gy = np.meshgrid(xs, ys)
Dm = dist_of(dpx[gy, gx])
u = (gx + 0.5) / W; v = (gy + 0.5) / H
verts = np.stack([(u - 0.5) * 2 * t * Dm, Dm, (0.5 - v) * 2 * t * (H / W) * Dm], -1).reshape(-1, 3).astype(np.float32)
nx, ny = len(xs), len(ys)
idx = np.arange(nx * ny).reshape(ny, nx)
quads = np.stack([idx[:-1, :-1], idx[1:, :-1], idx[1:, 1:], idx[:-1, 1:]], -1).reshape(-1, 4)
me = bpy.data.meshes.new("ground")
me.vertices.add(len(verts)); me.vertices.foreach_set("co", verts.ravel())
me.loops.add(quads.size); me.loops.foreach_set("vertex_index", quads.ravel().astype(np.int32))
me.polygons.add(len(quads)); me.polygons.foreach_set("loop_start", np.arange(0, quads.size, 4, dtype=np.int32))
me.update(); me.validate()
gnd = bpy.data.objects.new("ground", me); sc.collection.objects.link(gnd)
gnd.is_shadow_catcher = True
gnd.visible_shadow = cfg.get("ground_casts_shadow", False)
gm = bpy.data.materials.new("gnd"); gm.use_nodes = True
gnd.data.materials.append(gm)

def px_ground(px, py):
    xi = int(min(max(px, 0), W - 1)); yi = int(min(max(py, 0), H - 1))
    dd = dist_of(float(np.median(dpx[max(0, yi - 2):yi + 3, max(0, xi - 2):xi + 3])))
    uu = (px + 0.5) / W; vv = (py + 0.5) / H
    return Vector(((uu - 0.5) * 2 * t * dd, dd, (0.5 - vv) * 2 * t * (H / W) * dd))

# ---------- camera & sun ----------
cd = bpy.data.cameras.new("cam"); cd.sensor_fit = "HORIZONTAL"; cd.angle = HFOV; cd.clip_end = 1000
cam = bpy.data.objects.new("cam", cd); sc.collection.objects.link(cam); sc.camera = cam
cam.rotation_euler = (math.pi / 2, 0, 0)
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
sun.data.energy = cfg.get("sun_strength", 4.0); sun.data.color = cfg.get("sun_color", [1.0, 0.82, 0.62])
sun.data.angle = math.radians(1.5)
dv = Vector(cfg.get("sun_dir", [0.35, 0.9, -0.3])).normalized()  # direction light travels
sun.rotation_euler = dv.to_track_quat("-Z", "Y").to_euler()
sc.collection.objects.link(sun)

# ---------- cast ----------
with bpy.data.libraries.load(cfg["cast_blend"], link=False) as (src, dst):
    dst.objects = [n for n in src.objects]
for o in dst.objects:
    if o is not None and o.type != "CAMERA" and not o.name.startswith(("psun", "pc")):
        sc.collection.objects.link(o)

def rig_children(rig):
    return [o for o in bpy.data.objects if o.parent == rig or
            any(c.type in ("COPY_LOCATION",) and c.target == rig for c in o.constraints)]

def duplicate_rig(rig, newname):
    objs = [rig] + rig_children(rig)
    objs += [c for o in objs for c in o.children if c not in objs]
    mp = {}
    for o in objs:
        n = o.copy(); n.name = newname + "_" + o.name; sc.collection.objects.link(n); mp[o] = n
    for o, n in mp.items():
        if o.parent in mp: n.parent = mp[o.parent]
        for m in n.modifiers:
            if m.type == "ARMATURE" and m.object in mp: m.object = mp[m.object]
        for c in n.constraints:
            if getattr(c, "target", None) in mp: c.target = mp[c.target]
    nr = mp[rig]
    if rig.animation_data and rig.animation_data.action:
        act = rig.animation_data.action.copy()
        slot = getattr(rig.animation_data, "action_slot", None)
        nr.animation_data.action = act
        try:
            if slot is not None and nr.animation_data.action_slot is None:
                nr.animation_data.action_slot = act.slots[0]
        except Exception as e:
            print("slot", e)
    return nr

def place(rig, path_px, speed, start_m=0.0, reverse_face=False, lateral=0.0):
    P = [px_ground(x, y) for x, y in path_px]
    seg = [0.0]
    for i in range(1, len(P)): seg.append(seg[-1] + (P[i] - P[i - 1]).length)
    def at(s):
        s = min(max(s, 0.0), seg[-1])
        i = max(0, min(len(P) - 2, next((k for k in range(len(seg) - 1) if seg[k + 1] >= s), len(P) - 2)))
        r = (s - seg[i]) / max(seg[i + 1] - seg[i], 1e-9)
        return P[i].lerp(P[i + 1], r)
    lift = -float(rig.get("foot_min", 0.0))
    for f in range(1, NF + 1):
        s = start_m + speed * (f - 1) / FPS
        p = at(s); p2 = at(s + 0.4)
        d = (p2 - p); d.z = 0
        if d.length < 1e-6: d = Vector((0, 1, 0))
        d.normalize()
        side = Vector((d.y, -d.x, 0)) * lateral
        rig.location = p + side + Vector((0, 0, lift))
        yaw = math.atan2(d.x, -d.y)
        rig.rotation_euler = (0, 0, yaw + (math.pi if reverse_face else 0))
        rig.keyframe_insert("location", frame=f); rig.keyframe_insert("rotation_euler", frame=f)
    print("placed", rig.name, "path m", round(seg[-1], 1), "walks m", round(speed * NF / FPS, 1))

for a in cfg["actors"]:
    rig = bpy.data.objects[a["rig"]]
    if a.get("dup_as"):
        rig = duplicate_rig(rig, a["dup_as"])
    if a.get("scale"):
        rig.scale = (a["scale"],) * 3
    place(rig, a["path_px"], a.get("speed", float(rig.get("speed_mps", 1.2))) * a.get("scale", 1.0),
          a.get("start_m", 0.0), a.get("reverse_face", False), a.get("lateral", 0.0))
# originals not used as actors are hidden
used = {a["rig"] for a in cfg["actors"] if not a.get("dup_as")}
for o in bpy.data.objects:
    if o.type == "ARMATURE" and o.name not in used and not any(o.name.startswith(a.get("dup_as", "~") + "_") for a in cfg["actors"]):
        for c in [o] + rig_children(o):
            c.hide_render = True

sc.render.filepath = cfg["out_frames"] + "/f"
if cfg.get("debug_script"):
    exec(open(cfg["debug_script"]).read())
elif cfg.get("still_frames"):
    for f in cfg["still_frames"]:
        sc.frame_set(f); sc.render.filepath = cfg["out_frames"] + f"/still_{f:04d}.png"
        bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
print("DONE")
