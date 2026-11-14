"""Blender: 2.5D parallax night establishing shot.
blender -b -P render_parallax.py -- config.json
"""
import bpy, sys, json, math
import numpy as np

cfg = json.load(open(sys.argv[sys.argv.index("--") + 1], encoding="utf-8"))
FPS = cfg.get("fps", 24)
SECS = cfg.get("seconds", 9)
NF = FPS * SECS
HFOV = math.radians(cfg.get("hfov", 60))
NEAR, FAR = cfg.get("near", 2.5), cfg.get("far", 80.0)
STEP = cfg.get("step", 2)
TILT = math.radians(cfg.get("tilt_deg", 22))
PUSH = cfg.get("push", 0.3)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
    try:
        sc.render.engine = eng
        break
    except TypeError:
        pass
sc.render.resolution_x, sc.render.resolution_y = cfg.get("res", [1280, 720])
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, NF
sc.render.image_settings.file_format = "PNG"
sc.render.filepath = cfg["out_frames"] + "/f"
sc.view_settings.view_transform = "Standard"
try:
    sc.view_settings.look = "None"
except Exception:
    pass
try:
    sc.eevee.taa_render_samples = cfg.get("samples", 32)
except Exception:
    pass
sc.render.film_transparent = False
w = bpy.data.worlds.new("W"); sc.world = w
w.use_nodes = True
bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
bg.inputs[0].default_value = (0, 0, 0, 1)

def img(path, noncolor=False):
    i = bpy.data.images.load(path)
    if noncolor:
        i.colorspace_settings.name = "Non-Color"
    return i

def frame_driver(sock, expr):
    fc = sock.driver_add("default_value")
    fc.driver.expression = expr

# ---------------- plate mesh ----------------
plate = img(cfg["plate_rgba"])
W, H = plate.size
dimg = img(cfg["depth"], True)
dpx = np.array(dimg.pixels[:], np.float32).reshape(H, W, 4)[::-1, :, 0]  # top row first
xs = np.arange(0, W, STEP); ys = np.arange(0, H, STEP)
if xs[-1] != W - 1: xs = np.append(xs, W - 1)
if ys[-1] != H - 1: ys = np.append(ys, H - 1)
gx, gy = np.meshgrid(xs, ys)
disp = dpx[gy, gx]
dist = 1.0 / (disp * (1 / NEAR - 1 / FAR) + 1 / FAR)
t = math.tan(HFOV / 2)
u = (gx + 0.5) / W; v = (gy + 0.5) / H
X = (u - 0.5) * 2 * t * dist
Z = (0.5 - v) * 2 * t * (H / W) * dist
Y = dist
verts = np.stack([X, Y, Z], -1).reshape(-1, 3).astype(np.float32)
nx, ny = len(xs), len(ys)
idx = np.arange(nx * ny).reshape(ny, nx)
quads = np.stack([idx[:-1, :-1], idx[1:, :-1], idx[1:, 1:], idx[:-1, 1:]], -1).reshape(-1, 4)
me = bpy.data.meshes.new("plate")
me.vertices.add(len(verts)); me.vertices.foreach_set("co", verts.ravel())
me.loops.add(quads.size); me.loops.foreach_set("vertex_index", quads.ravel().astype(np.int32))
me.polygons.add(len(quads)); me.polygons.foreach_set("loop_start", np.arange(0, quads.size, 4, dtype=np.int32))
uvl = me.uv_layers.new(name="UV")
uvs = np.stack([u.ravel(), 1 - v.ravel()], -1)[quads.ravel()]
uvl.data.foreach_set("uv", uvs.ravel().astype(np.float32))
me.update(); me.validate()
ob = bpy.data.objects.new("plate", me); sc.collection.objects.link(ob)

m = bpy.data.materials.new("plate"); m.use_nodes = True
try: m.surface_render_method = "DITHERED"
except Exception: m.blend_method = "HASHED"
nt = m.node_tree; N = nt.nodes; L = nt.links
for n in list(N):
    if n.type != "OUTPUT_MATERIAL": N.remove(n)
out = next(n for n in N if n.type == "OUTPUT_MATERIAL")
uvn = N.new("ShaderNodeUVMap"); uvn.uv_map = "UV"
tex = N.new("ShaderNodeTexImage"); tex.image = plate; tex.interpolation = "Cubic"
lm = N.new("ShaderNodeTexImage"); lm.image = img(cfg["lamp_mask"], True)
noise = N.new("ShaderNodeTexNoise"); noise.noise_dimensions = "4D"
noise.inputs["Scale"].default_value = 60; noise.inputs["Detail"].default_value = 1
frame_driver(noise.inputs["W"], "frame/24*2.2")
L.new(uvn.outputs[0], tex.inputs[0]); L.new(uvn.outputs[0], lm.inputs[0]); L.new(uvn.outputs[0], noise.inputs["Vector"])
# flick = 1 + mask*(noise-0.5)*amp
sub = N.new("ShaderNodeMath"); sub.operation = "SUBTRACT"; sub.inputs[1].default_value = 0.5
L.new(noise.outputs["Fac"], sub.inputs[0])
mul = N.new("ShaderNodeMath"); mul.operation = "MULTIPLY"
L.new(sub.outputs[0], mul.inputs[0]); L.new(lm.outputs["Color"], mul.inputs[1])
amp = N.new("ShaderNodeMath"); amp.operation = "MULTIPLY_ADD"
amp.inputs[1].default_value = cfg.get("lamp_flicker", 1.3); amp.inputs[2].default_value = 1.0
L.new(mul.outputs[0], amp.inputs[0])
cm = N.new("ShaderNodeVectorMath"); cm.operation = "SCALE"
L.new(tex.outputs["Color"], cm.inputs[0]); L.new(amp.outputs[0], cm.inputs["Scale"])
em = N.new("ShaderNodeEmission"); L.new(cm.outputs[0], em.inputs["Color"])
tr = N.new("ShaderNodeBsdfTransparent")
mix = N.new("ShaderNodeMixShader")
L.new(tex.outputs["Alpha"], mix.inputs[0]); L.new(tr.outputs[0], mix.inputs[1]); L.new(em.outputs[0], mix.inputs[2])
L.new(mix.outputs[0], out.inputs[0])
ob.data.materials.append(m)

# ---------------- sky plane ----------------
sky = img(cfg["sky"]); SW, SH = sky.size
D = 500.0
elev = math.radians(cfg.get("sky_center_deg", 17.5))
half_h = D * math.tan(math.radians(cfg.get("sky_half_deg", 26)))
half_w = half_h * SW / SH * cfg.get("sky_stretch", 1.0)
bpy.ops.mesh.primitive_plane_add(size=2)
sp = bpy.context.active_object; sp.name = "sky"
sp.scale = (half_w, half_h, 1)
sp.rotation_euler = (math.pi / 2 + elev, 0, 0)  # plane perpendicular to view dir at elev
sp.location = (0, D * math.cos(elev), D * math.sin(elev))
sm = bpy.data.materials.new("sky"); sm.use_nodes = True
nt = sm.node_tree; N = nt.nodes; L = nt.links
for n in list(N):
    if n.type != "OUTPUT_MATERIAL": N.remove(n)
out = next(n for n in N if n.type == "OUTPUT_MATERIAL")
tc = N.new("ShaderNodeTexCoord")
st = N.new("ShaderNodeTexImage"); st.image = sky; st.interpolation = "Cubic"
sk = N.new("ShaderNodeTexImage"); sk.image = img(cfg["star_mask"], True)
nz = N.new("ShaderNodeTexNoise"); nz.noise_dimensions = "4D"
nz.inputs["Scale"].default_value = 300; nz.inputs["Detail"].default_value = 0
frame_driver(nz.inputs["W"], "frame/24*3.0")
for x in (st, sk, nz): L.new(tc.outputs["UV"], x.inputs[0])
s2 = N.new("ShaderNodeMath"); s2.operation = "SUBTRACT"; s2.inputs[1].default_value = 0.5
L.new(nz.outputs["Fac"], s2.inputs[0])
m2 = N.new("ShaderNodeMath"); m2.operation = "MULTIPLY"
L.new(s2.outputs[0], m2.inputs[0]); L.new(sk.outputs["Color"], m2.inputs[1])
a2 = N.new("ShaderNodeMath"); a2.operation = "MULTIPLY_ADD"
a2.inputs[1].default_value = cfg.get("twinkle", 1.6); a2.inputs[2].default_value = 1.0
L.new(m2.outputs[0], a2.inputs[0])
c2 = N.new("ShaderNodeVectorMath"); c2.operation = "SCALE"
L.new(st.outputs["Color"], c2.inputs[0]); L.new(a2.outputs[0], c2.inputs["Scale"])
e2 = N.new("ShaderNodeEmission"); L.new(c2.outputs[0], e2.inputs["Color"])
L.new(e2.outputs[0], out.inputs[0])
sp.data.materials.append(sm)

# ---------------- camera ----------------
cam_d = bpy.data.cameras.new("cam"); cam_d.sensor_fit = "HORIZONTAL"; cam_d.angle = HFOV
cam_d.clip_start = 0.05; cam_d.clip_end = 2000
cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam); sc.camera = cam
cam.rotation_mode = "XYZ"
def smooth(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * x * (x * (x * 6 - 15) + 10)
t0, t1 = cfg.get("tilt_start", 0.4), cfg.get("tilt_end", 9.0)
for f in range(1, NF + 1):
    ts = (f - 1) / FPS
    k = smooth((ts - t0) / (t1 - t0))
    kp = (f - 1) / (NF - 1)
    cam.rotation_euler = (math.pi / 2 + TILT * k, 0, 0)
    cam.location = (cfg.get("drift_x", 0.05) * kp, PUSH * (0.5 - 0.5 * math.cos(math.pi * kp)), 0)
    cam.keyframe_insert("rotation_euler", frame=f); cam.keyframe_insert("location", frame=f)

# ---------------- lantern sprites ----------------
def sprite(name, color, strength, sigma, sx=1.0, sy=1.0):
    bpy.ops.mesh.primitive_plane_add(size=2)
    o = bpy.context.active_object; o.name = name
    mt = bpy.data.materials.new(name); mt.use_nodes = True
    try: mt.surface_render_method = "BLENDED"
    except Exception: mt.blend_method = "BLEND"
    nt = mt.node_tree; N = nt.nodes; L = nt.links
    for n in list(N):
        if n.type != "OUTPUT_MATERIAL": N.remove(n)
    out = next(n for n in N if n.type == "OUTPUT_MATERIAL")
    tc = N.new("ShaderNodeTexCoord")
    ln = N.new("ShaderNodeVectorMath"); ln.operation = "LENGTH"
    L.new(tc.outputs["Generated"], ln.inputs[0])
    # Generated is 0..1; center 0.5 -> use Object coords instead (-1..1)
    L.new(tc.outputs["Object"], ln.inputs[0])
    sq = N.new("ShaderNodeMath"); sq.operation = "POWER"; sq.inputs[1].default_value = 2
    L.new(ln.outputs["Value"], sq.inputs[0])
    sc_ = N.new("ShaderNodeMath"); sc_.operation = "MULTIPLY"; sc_.inputs[1].default_value = -1.0 / (2 * sigma * sigma)
    L.new(sq.outputs[0], sc_.inputs[0])
    ex = N.new("ShaderNodeMath"); ex.operation = "EXPONENT"; L.new(sc_.outputs[0], ex.inputs[0])
    st_ = N.new("ShaderNodeMath"); st_.operation = "MULTIPLY"; st_.inputs[1].default_value = strength
    L.new(ex.outputs[0], st_.inputs[0])
    em = N.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (*color, 1)
    L.new(st_.outputs[0], em.inputs["Strength"])
    tr = N.new("ShaderNodeBsdfTransparent")
    ad = N.new("ShaderNodeAddShader"); L.new(tr.outputs[0], ad.inputs[0]); L.new(em.outputs[0], ad.inputs[1])
    L.new(ad.outputs[0], out.inputs[0])
    o.data.materials.append(mt)
    return o, st_

lan = cfg.get("lantern")
if lan:
    pts = np.array(lan["path_px"], np.float32)  # ground points along street (x,y px), in order
    def px_to_world(px, py, lift_px=0.0, closer=0.97):
        xi = int(min(max(px, 0), W - 1)); yi = int(min(max(py, 0), H - 1))
        dd = 1.0 / (dpx[yi, xi] * (1 / NEAR - 1 / FAR) + 1 / FAR) * closer
        uu = (px + 0.5) / W; vv = (py - lift_px + 0.5) / H
        return (uu - 0.5) * 2 * t * dd, dd, (0.5 - vv) * 2 * t * (H / W) * dd, dd
    seg = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
    pxw = 2 * t / W  # world size of 1px at distance 1
    glow, gstr = sprite("lantern_glow", (1.0, 0.62, 0.28), lan.get("glow", 0.9), 0.35)
    core, cstr = sprite("lantern_core", (1.0, 0.85, 0.6), lan.get("core", 6.0), 0.18)
    pool, pstr = sprite("lantern_pool", (1.0, 0.55, 0.25), lan.get("pool", 0.35), 0.45)
    for o in (glow, core, pool):
        o.rotation_euler = (math.pi / 2, 0, 0)
    a0, a1 = lan.get("t_start", 0.0), lan.get("t_end", SECS)
    for f in range(1, NF + 1):
        ts = (f - 1) / FPS
        p = min(max((ts - a0) / (a1 - a0), 0), 1)
        s = p * seg[-1]
        i = min(np.searchsorted(seg, s, side="right") - 1, len(pts) - 2)
        r = (s - seg[i]) / max(seg[i + 1] - seg[i], 1e-6)
        gx_, gy_ = pts[i] + (pts[i + 1] - pts[i]) * r
        bob = math.sin(2 * math.pi * 1.6 * ts) * lan.get("bob_px", 1.2)
        lift = lan.get("lift_px", 16) + bob
        X_, Y_, Z_, dd = px_to_world(gx_, gy_, lift)
        for o, rad in ((glow, lan.get("glow_px", 22)), (core, lan.get("core_px", 2.6))):
            o.location = (X_, Y_, Z_); o.scale = (rad * pxw * dd,) * 3
            o.keyframe_insert("location", frame=f); o.keyframe_insert("scale", frame=f)
        Xp, Yp, Zp, dp = px_to_world(gx_, gy_ + 2, 0, 0.965)
        pr = lan.get("pool_px", 26)
        pool.location = (Xp, Yp, Zp); pool.scale = (pr * pxw * dp, 1, pr * 0.35 * pxw * dp)
        pool.keyframe_insert("location", frame=f); pool.keyframe_insert("scale", frame=f)
        fl = 1 + 0.12 * math.sin(ts * 17.3) * math.sin(ts * 5.1 + 1)
        for node, base in ((gstr, lan.get("glow", 0.9)), (cstr, lan.get("core", 6.0)), (pstr, lan.get("pool", 0.35))):
            node.inputs[1].default_value = base * fl
            node.inputs[1].keyframe_insert("default_value", frame=f)

wk = cfg.get("walker")
if wk:
    pxw = 2 * t / W
    def ground(px, py, closer=0.995):
        xi = int(min(max(px, 0), W - 1)); yi = int(min(max(py, 0), H - 1))
        dd = 1.0 / (dpx[yi, xi] * (1 / NEAR - 1 / FAR) + 1 / FAR) * closer
        uu = (px + 0.5) / W; vv = (py + 0.5) / H
        return np.array([(uu - 0.5) * 2 * t * dd, dd, (0.5 - vv) * 2 * t * (H / W) * dd]), dd
    # append walker objects
    with bpy.data.libraries.load(wk["blend"], link=False) as (src, dst):
        dst.objects = [n for n in src.objects]
    for o in dst.objects:
        if o is not None:
            sc.collection.objects.link(o)
    rig = bpy.data.objects["walker_rig"]
    lantern = bpy.data.objects["lantern"]; llight = bpy.data.objects["lantern_light"]
    try: lantern.visible_shadow = False
    except Exception as e: print("visible_shadow", e)
    # world scale: person of person_px pixels tall standing at ref_px
    rp, rd = ground(*wk["ref_px"])
    Hw = wk.get("person_px", 75) * pxw * rd
    k = Hw / 1.67
    rig.scale = (k, k, k)
    llight.data.energy = wk.get("lantern_w", 60) * k * k
    llight.data.shadow_soft_size = 0.05 * k
    # 3D path on the ground, arc-length parametrized
    P = np.array([ground(x, y)[0] for x, y in wk["path_px"]])
    seg = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]
    speed = wk.get("speed_mps", 1.05) * k
    print("arc_m per point", [round(float(x / k), 1) for x in seg])
    print("walker scale", k, "path len", seg[-1], "needs s", seg[-1] / speed,
          "px height far", Hw / (pxw * ground(*wk["path_px"][0])[1]), "near", Hw / (pxw * ground(*wk["path_px"][-1])[1]))
    def at(s):
        s = min(max(s, 0), seg[-1])
        i = min(np.searchsorted(seg, s, side="right") - 1, len(P) - 2)
        r = (s - seg[i]) / max(seg[i + 1] - seg[i], 1e-9)
        return P[i] + (P[i + 1] - P[i]) * r
    if rig.animation_data and rig.animation_data.action:
        act = rig.animation_data.action
        try:
            for fc in [fc for fc in act.fcurves if fc.data_path in ("location",)]:
                act.fcurves.remove(fc)
        except Exception as e:
            print("fcurve cleanup skipped", e)
    s0 = wk.get("start_m", 0.0) * k
    CYC = 1.2
    for f in range(1, NF + 1):
        ts = (f - 1) / FPS
        s = s0 + speed * ts
        p = at(s); p2 = at(s + 0.3 * k)
        dx, dy = p2[0] - p[0], p2[1] - p[1]
        bob = 0.0 if "foot_min" in rig.keys() else 0.018 * k * abs(math.cos(2 * math.pi * ts / CYC))
        lift = -float(rig.get("foot_min", 0.0)) * k
        rig.location = (p[0], p[1], p[2] + bob + lift)
        rig.rotation_euler = (0, 0, math.atan2(dx, -dy))
        rig.keyframe_insert("location", frame=f); rig.keyframe_insert("rotation_euler", frame=f)
    # world ambient (cool, dark) + faint moonlight; affect only the 3D character (plate is unlit)
    bg.inputs[0].default_value = tuple(wk.get("ambient", (0.010, 0.014, 0.028))) + (1,)
    moon = bpy.data.objects.new("moon", bpy.data.lights.new("moon", "SUN"))
    moon.data.energy = wk.get("moon", 0.08); moon.data.color = (0.6, 0.7, 1.0)
    moon.rotation_euler = (math.radians(50), 0, math.radians(150)); sc.collection.objects.link(moon)
    # glow sprite following the lantern, facing camera
    glow2, g2 = sprite("walker_glow", (1.0, 0.6, 0.28), wk.get("glow", 0.6), 0.35)
    glow2.parent = lantern; glow2.matrix_parent_inverse.identity(); glow2.location = (0, 0, 0)
    cr = glow2.constraints.new("COPY_ROTATION"); cr.target = cam
    gs = wk.get("glow_m", 0.6)
    glow2.scale = (gs,) * 3  # lantern inherits rig scale k
    pool2, p2s = sprite("walker_pool", (1.0, 0.55, 0.25), wk.get("pool", 0.3), 0.30)
    for f in range(1, NF + 1):
        sc.frame_set(f)
        lp = lantern.matrix_world.translation
        gpos = rig.matrix_world.translation
        pool2.location = (lp.x, lp.y - 0.02 * k, gpos.z + 0.05 * k)
        pool2.rotation_euler = (0, 0, 0)
        pr = wk.get("pool_m", 1.6) * k
        pool2.scale = (pr, pr, pr)
        pool2.keyframe_insert("location", frame=f); pool2.keyframe_insert("scale", frame=f)
        fl = 1 + 0.10 * math.sin(f / FPS * 17.3) * math.sin(f / FPS * 5.1 + 1)
        llight.data.energy = wk.get("lantern_w", 60) * k * k * fl
        llight.data.keyframe_insert("energy", frame=f)

if cfg.get("debug_script"):
    exec(open(cfg["debug_script"]).read())  # DEBUG_ONLY
elif cfg.get("still_frames"):
    for f in cfg["still_frames"]:
        sc.frame_set(f)
        sc.render.filepath = cfg["out_frames"] + f"/still_{f:04d}.png"
        bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
print("DONE")
