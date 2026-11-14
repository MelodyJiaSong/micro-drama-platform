"""Retarget a CMU BVH walk onto the MPFB game_engine rig in walker.blend, loop one gait cycle to 9 s (in place).
blender -b walker.blend -P retarget_mocap.py -- clip.bvh out.blend preview_dir
Prints: SPEED_MPS (forward speed in metres for a 1.67 m character).
"""
import bpy, sys, math
import numpy as np
from mathutils import Matrix, Quaternion, Vector

argv = sys.argv[sys.argv.index("--") + 1:]
BVH, OUT, PREV = argv[0], argv[1], argv[2] if len(argv) > 2 else None
FPS, NF = 24, 9 * 24
CARRY = 0.35  # how much mocap swing the lantern arm keeps

sc = bpy.context.scene
sc.render.fps = FPS
rig = bpy.data.objects["walker_rig"]
if rig.animation_data:
    rig.animation_data_clear()
rig.location = (0, 0, 0); rig.rotation_euler = (0, 0, 0); rig.scale = (1, 1, 1)
for pb in rig.pose.bones:
    pb.rotation_mode = "QUATERNION"; pb.rotation_quaternion = (1, 0, 0, 0); pb.location = (0, 0, 0)

bpy.ops.import_anim.bvh(filepath=BVH, global_scale=1.0, frame_start=1, use_fps_scale=True,
                        update_scene_fps=False, update_scene_duration=False, rotate_mode="NATIVE")
src = bpy.context.active_object
act = src.animation_data.action
f0, f1 = [int(round(x)) for x in act.frame_range]
print("bvh frames", f0, f1)

MAP = {"pelvis": "Hips", "spine_01": "LowerBack", "spine_02": "Spine", "spine_03": "Spine1",
       "neck_01": "Neck", "head": "Head",
       "clavicle_l": "LeftShoulder", "upperarm_l": "LeftArm", "lowerarm_l": "LeftForeArm", "hand_l": "LeftHand",
       "clavicle_r": "RightShoulder", "upperarm_r": "RightArm", "lowerarm_r": "RightForeArm", "hand_r": "RightHand",
       "thigh_l": "LeftUpLeg", "calf_l": "LeftLeg", "foot_l": "LeftFoot", "ball_l": "LeftToeBase",
       "thigh_r": "RightUpLeg", "calf_r": "RightLeg", "foot_r": "RightFoot", "ball_r": "RightToeBase"}

# ---- align facing: BVH left (+) should map to target left (+X), up = +Z ----
sc.frame_set(f0)
def wrest(obj, name):  # world-space rest head/tail
    b = obj.data.bones[name]
    return obj.matrix_world @ b.head_local, obj.matrix_world @ b.tail_local
lh, _ = wrest(src, "LeftUpLeg"); rh, _ = wrest(src, "RightUpLeg")
left = (lh - rh); left.z = 0; left.normalize()
yaw = left.to_2d().angle_signed(Vector((1, 0)))
src.matrix_world = Matrix.Rotation(-yaw, 4, "Z") @ src.matrix_world
bpy.context.view_layer.update()
lh, _ = wrest(src, "LeftUpLeg"); print("bvh left now", tuple(round(c, 2) for c in (lh - wrest(src, "RightUpLeg")[0])))

# size ratio by leg length
def leglen(obj, up, low, foot):
    a = wrest(obj, up)[0]; c = wrest(obj, foot)[0]; return (a - c).length
ratio = leglen(rig, "thigh_l", "calf_l", "foot_l") / leglen(src, "LeftUpLeg", "LeftLeg", "LeftFoot")
print("scale ratio", ratio)

def rest_rot(obj, name):
    return (obj.matrix_world.to_3x3() @ obj.data.bones[name].matrix_local.to_3x3()).to_quaternion()
def pose_rot(obj, name):
    return (obj.matrix_world.to_3x3() @ obj.pose.bones[name].matrix.to_3x3()).to_quaternion()
def dirv(obj, name, posed):
    if posed:
        pb = obj.pose.bones[name]; v = obj.matrix_world.to_3x3() @ (pb.tail - pb.head)
    else:
        b = obj.data.bones[name]; v = obj.matrix_world.to_3x3() @ (b.tail_local - b.head_local)
    return v.normalized()

# rest-direction offsets (T-pose vs A-pose): rotate target rest dir onto bvh rest dir
OFF = {}
for t, s in MAP.items():
    OFF[t] = dirv(rig, t, False).rotation_difference(dirv(src, s, False)) if t not in ("pelvis",) else Quaternion()
RR_t = {t: rest_rot(rig, t) for t in MAP}
RR_s = {s: rest_rot(src, s) for s in MAP.values()}
hips_rest = wrest(src, "Hips")[0]
pelvis_rest = rig.data.bones["pelvis"].head_local.copy()

# hierarchy order
order = [b.name for b in rig.data.bones if b.name in MAP]
order.sort(key=lambda n: len(rig.data.bones[n].parent_recursive))

# carry pose for lantern arm (world dirs)
def carry_world(name):
    return {"upperarm_r": Vector((-0.12, -0.08, -1)), "lowerarm_r": Vector((-0.03, -0.75, -0.65))}.get(name)

frames = []
for fr in range(f0, f1 + 1):
    sc.frame_set(fr)
    rec = {}
    for t in order:
        s = MAP[t]
        delta = pose_rot(src, s) @ RR_s[s].inverted()
        want = delta @ OFF[t] @ RR_t[t]
        if t in ("upperarm_r", "lowerarm_r"):
            cur_dir = (want @ RR_t[t].inverted()) @ dirv(rig, t, False)
            tgt = carry_world(t).normalized()
            fix = cur_dir.rotation_difference(tgt)
            want = Quaternion().slerp(fix, 1 - CARRY) @ want
        pb = rig.pose.bones[t]
        M = want.to_matrix().to_4x4()
        M.translation = pb.head if t != "pelvis" else pb.head
        if t == "pelvis":
            hp = src.matrix_world @ src.pose.bones["Hips"].head
            off = (hp - hips_rest) * ratio
            M.translation = Vector((pelvis_rest.x + off.x, pelvis_rest.y + off.y, hp.z * ratio))
        pb.matrix = M
        bpy.context.view_layer.update()
        rec[t] = (pb.rotation_quaternion.copy(), pb.location.copy())
        if t == "pelvis":
            rec["_pelM"] = pb.matrix.copy()
    hp = src.matrix_world @ src.pose.bones["Hips"].head
    rec["_hips"] = Vector(hp) * ratio
    frames.append(rec)
print("retargeted", len(frames))

# ---- remove forward travel, measure speed ----
H = np.array([list(fr["_hips"]) for fr in frames])
n = len(H)
fwd = np.polyfit(np.arange(n), H[:, 1], 1)[0]; side = np.polyfit(np.arange(n), H[:, 0], 1)[0]
speed = math.hypot(fwd, side) * FPS
print("SPEED_MPS", round(speed, 3), "dir", round(fwd, 4), round(side, 4))

# ---- find gait cycle: frames a<b with b-a in [0.9,1.7]s and minimal pose difference ----
keys = [t for t in order if t != "pelvis"]
def pose_vec(i):
    return np.concatenate([list(frames[i][t][0]) for t in keys])
V = np.array([pose_vec(i) for i in range(n)])
best = None
for a in range(0, n // 2):
    for P in range(int(0.9 * FPS), int(1.7 * FPS)):
        b = a + P
        if b >= n: break
        d = np.minimum(np.abs(V[a] - V[b]), np.abs(V[a] + V[b])).sum()
        if best is None or d < best[0]:
            best = (d, a, P)
_, A, P = best
print("cycle start", A, "period frames", P, "diff", round(best[0], 3))

# pelvis in-place offsets (detrended within cycle)
locs = np.array([list(frames[i]["pelvis"][1]) for i in range(n)])
idx = np.arange(n)
for c in range(3):
    pass
# keyframe 216 frames
rig.animation_data_create()
for f in range(1, NF + 1):
    i = A + ((f - 1) % P)
    j = (f - 1) % P
    for t in order:
        q, loc = frames[i][t]
        pb = rig.pose.bones[t]
        pb.rotation_quaternion = q
        pb.keyframe_insert("rotation_quaternion", frame=f)
    # pelvis: armature-space position, horizontal travel removed (loops in place around the rest xy)
    MA = frames[A]["_pelM"].translation; MB = frames[A + P]["_pelM"].translation
    trend = MA + (MB - MA) * (j / P)
    M = frames[i]["_pelM"].copy()
    d = M.translation - trend
    M.translation = Vector((pelvis_rest.x + d.x, pelvis_rest.y + d.y, M.translation.z))
    pb = rig.pose.bones["pelvis"]
    pb.matrix = M
    bpy.context.view_layer.update()
    pb.keyframe_insert("location", frame=f); pb.keyframe_insert("rotation_quaternion", frame=f)
# ground: lowest foot point over the cycle -> store as rig property (render script lifts by it)
lows = []
for f in range(1, P + 1):
    sc.frame_set(f)
    z = min((rig.matrix_world @ rig.pose.bones[b].tail).z for b in ("foot_l", "foot_r", "ball_l", "ball_r"))
    z = min(z, min((rig.matrix_world @ rig.pose.bones[b].head).z for b in ("foot_l", "foot_r")) - 0.06)
    lows.append(z)
rig["foot_min"] = float(min(lows))
print("FOOT_MIN", rig["foot_min"])
# remove BVH armature
bpy.data.objects.remove(src, do_unlink=True)
sc.frame_end = NF

if PREV:
    for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try: sc.render.engine = eng; break
        except TypeError: pass
    sc.render.resolution_x, sc.render.resolution_y = 480, 640
    cd = bpy.data.cameras.new("pc"); cd.lens = 50; cam = bpy.data.objects.new("pc", cd)
    bpy.context.collection.objects.link(cam); sc.camera = cam
    cam.location = (5.0, 0, 0.9 + rig["foot_min"]); cam.rotation_euler = (math.radians(90), 0, math.radians(90))
    rig.location.z = -rig["foot_min"]
    bpy.ops.mesh.primitive_plane_add(size=6); gp = bpy.context.active_object
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN")); sun.data.energy = 3
    sun.rotation_euler = (0.8, 0.2, 0.6); bpy.context.collection.objects.link(sun)
    if sc.world is None: sc.world = bpy.data.worlds.new("w")
    step = max(1, P // 6)
    for k in range(6):
        sc.frame_set(1 + k * step); sc.render.filepath = f"{PREV}/mc_{k}.png"
        bpy.ops.render.render(write_still=True)
    for o in (cam, sun, gp): bpy.data.objects.remove(o)
    rig.location.z = 0
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT)
