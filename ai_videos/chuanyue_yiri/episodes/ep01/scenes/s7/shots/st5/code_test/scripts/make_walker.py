"""Blender (with MPFB extension loaded): build a Roman lantern-carrier with a procedural walk cycle.
blender -b -P make_walker.py -- out.blend [preview_dir]
Walk is in place (root fixed), facing -Y in local space; the render script moves/rotates the root.
"""
import bpy, sys, math, importlib

argv = sys.argv[sys.argv.index("--") + 1:]
OUT = argv[0]
PREV = argv[1] if len(argv) > 1 else None
FPS = 24
NF = 9 * FPS

mp = importlib.import_module("bl_ext.blender_org.mpfb.services.humanservice")
HumanService = mp.HumanService

# clean scene
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

macro = None
try:
    ts = importlib.import_module("bl_ext.blender_org.mpfb.services.targetservice").TargetService
    macro = ts.get_default_macro_info_dict()
    macro["gender"] = 1.0
    macro["age"] = 0.6
    macro["muscle"] = 0.45
    macro["weight"] = 0.5
    macro["height"] = 0.45
except Exception as e:
    print("macro fail", e)
body = HumanService.create_human(scale=0.1, macro_detail_dict=macro)
body.name = "walker_body"
HumanService.add_builtin_rig(body, "game_engine", import_weights=True)
rig = next(o for o in bpy.data.objects if o.type == "ARMATURE")
rig.name = "walker_rig"
print("height", max((body.matrix_world @ v.co).z for v in body.data.vertices))

# ---- simple materials (seen from ~40 m: flat colors are enough) ----
def mat(name, rgb, rough=0.8):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough
    return m
skin = mat("skin", (0.42, 0.26, 0.18), 0.6)
body.data.materials.clear(); body.data.materials.append(skin)

# ---- tunic: flared tube from shoulders to knees, skinned to the rig ----
H = max((body.matrix_world @ v.co).z for v in body.data.vertices)
top, bot = H * 0.81, H * 0.26
bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.25, radius2=0.20, depth=top - bot, end_fill_type="NOTHING",
                                location=(0, 0, (top + bot) / 2))
tun = bpy.context.active_object; tun.name = "tunic"
tun.scale = (1.0, 0.78, 1.0)
bpy.ops.object.transform_apply(scale=True)
bpy.ops.object.modifier_add(type="SUBSURF"); tun.modifiers[-1].levels = 1
tun.data.materials.append(mat("tunic", (0.52, 0.45, 0.35), 0.95))
# paenula-like hooded cloak: shoulders to mid-thigh
bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.27, radius2=0.11, depth=H * 0.34, end_fill_type="NOTHING",
                                location=(0, 0, H * 0.66))
cape = bpy.context.active_object; cape.name = "cape"; cape.scale = (1, 0.75, 1)
bpy.ops.object.transform_apply(scale=True)
bpy.ops.object.modifier_add(type="SUBSURF"); cape.modifiers[-1].levels = 1
cape.data.materials.append(mat("cape", (0.20, 0.13, 0.09), 0.95))
for o in (tun, cape):
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True); rig.select_set(True); bpy.context.view_layer.objects.active = rig
    bpy.ops.object.parent_set(type="ARMATURE_AUTO")

# hair cap
bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.105)
hair = bpy.context.active_object; hair.name = "hair"
hair.data.materials.append(mat("hair", (0.05, 0.035, 0.025), 0.9))
hb = rig.data.bones["head"]
hair.parent = rig; hair.parent_type = "BONE"; hair.parent_bone = "head"
hair.location = (0, -hb.length * 0.55, 0.0); hair.scale = (1.0, 1.0, 1.05)
# ---- lantern in right hand ----
pb = rig.pose.bones
hand = rig.data.bones["hand_r"]
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.07, depth=0.16)
lan = bpy.context.active_object; lan.name = "lantern"
lm = bpy.data.materials.new("lantern"); lm.use_nodes = True
e = lm.node_tree.nodes.new("ShaderNodeEmission")
e.inputs["Color"].default_value = (1.0, 0.55, 0.2, 1); e.inputs["Strength"].default_value = 6
out = next(n for n in lm.node_tree.nodes if n.type == "OUTPUT_MATERIAL")
lm.node_tree.links.new(e.outputs[0], out.inputs[0]); lan.data.materials.append(lm)
light_d = bpy.data.lights.new("lantern_light", "POINT"); light_d.energy = 60; light_d.color = (1.0, 0.6, 0.3)
light_d.shadow_soft_size = 0.05
light = bpy.data.objects.new("lantern_light", light_d); bpy.context.collection.objects.link(light)
for o in (lan, light):
    o.parent = rig; o.parent_type = "BONE"; o.parent_bone = "hand_r"
    o.location = (0, hand.length * 1.0 + 0.12, 0)

# ---- procedural walk cycle (in place), rotations defined in WORLD axes ----
from mathutils import Matrix, Quaternion, Vector
CYC = 1.2  # seconds per full stride (slow night walk)
X, Y, Z = Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))
def to_local(name, qw):
    M = rig.data.bones[name].matrix_local.to_3x3().to_quaternion()
    return M.inverted() @ qw @ M
def hang(name, side):
    b = rig.data.bones[name]
    d = (b.tail_local - b.head_local); d.y = 0; d.normalize()
    tgt = Vector((side * math.sin(math.radians(8)), 0, -math.cos(math.radians(8))))
    return d.rotation_difference(tgt)
HANG = {"upperarm_l": hang("upperarm_l", 1), "upperarm_r": hang("upperarm_r", -1)}
def aim(name, target, parent_q):
    b = rig.data.bones[name]
    d = (b.tail_local - b.head_local).normalized()
    return d.rotation_difference(parent_q.inverted() @ target.normalized())
def R(name, qw):
    b = pb[name]; b.rotation_mode = "QUATERNION"; b.rotation_quaternion = to_local(name, qw)
    b.keyframe_insert("rotation_quaternion", frame=f)
def ax(axis, deg): return Quaternion(axis, math.radians(deg))
for f in range(1, NF + 1):
    ph = 2 * math.pi * ((f - 1) / FPS) / CYC
    s = math.sin(ph)
    R("thigh_l", ax(X, -22 * s)); R("thigh_r", ax(X, 22 * s))
    R("calf_l", ax(X, 30 * max(0, math.sin(ph - 1.0))))
    R("calf_r", ax(X, 30 * max(0, math.sin(ph - 1.0 + math.pi))))
    R("foot_l", ax(X, 8 * s)); R("foot_r", ax(X, -8 * s))
    qul = ax(X, 16 * s) @ HANG["upperarm_l"]
    R("upperarm_l", qul)
    R("lowerarm_l", aim("lowerarm_l", ax(X, 16 * s) @ Vector((0.04, -0.25, -1)), qul))
    qur = ax(X, -6 + 2 * s) @ HANG["upperarm_r"]
    R("upperarm_r", qur)
    R("lowerarm_r", aim("lowerarm_r", Vector((-0.03, -0.75, -0.65)), qur))
    R("spine_01", ax(Z, 3 * s))
    p = pb["pelvis"]; p.location = (0, 0, 0); p.keyframe_insert("location", frame=f)
    rig.location = (0, 0, 0.018 * abs(math.cos(ph))); rig.keyframe_insert("location", frame=f)

# axes of the game-engine rig can differ: report a pose sanity check
bpy.context.scene.frame_set(int(CYC * FPS / 4) + 1)
for n in ("foot_l", "foot_r", "hand_l"):
    print(n, tuple(round(c, 3) for c in (rig.matrix_world @ pb[n].head)))

bpy.context.scene.render.fps = FPS
bpy.context.scene.frame_end = NF
if PREV:
    sc = bpy.context.scene
    for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try: sc.render.engine = eng; break
        except TypeError: pass
    sc.render.resolution_x, sc.render.resolution_y = 640, 640
    cd = bpy.data.cameras.new("pc"); cam = bpy.data.objects.new("pc", cd)
    bpy.context.collection.objects.link(cam); sc.camera = cam
    cd.lens = 50; cam.location = (3.2, -3.2, 1.0); cam.rotation_euler = (math.radians(88), 0, math.radians(45))
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN")); sun.data.energy = 3
    sun.rotation_euler = (0.8, 0.2, 0.6); bpy.context.collection.objects.link(sun)
    w = bpy.data.worlds.new("w"); sc.world = w
    for i, fr in enumerate((1, 8, 15, 22, 29)):
        sc.frame_set(fr); sc.render.filepath = f"{PREV}/walk_{i}.png"
        bpy.ops.render.render(write_still=True)
    for o in (cam, sun): bpy.data.objects.remove(o)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT)
