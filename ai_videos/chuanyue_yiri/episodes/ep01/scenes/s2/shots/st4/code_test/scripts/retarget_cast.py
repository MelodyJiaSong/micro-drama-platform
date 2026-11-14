"""Retarget CMU BVH walks onto several MPFB game_engine rigs in one .blend; loop a gait cycle in place.
blender -b cast.blend -P retarget_cast.py -- jobs.json out.blend
jobs.json: [{"rig":"riley_rig","bvh":"...","frames":192,
             "arms":{"upperarm_l":[x,y,z],"lowerarm_l":[x,y,z],...}, "arm_weight":0.85,
             "match_speed_of":"oldman_rig" (optional)}]
Writes per-rig custom props: speed_mps, foot_min, cycle_frames.
"""
import bpy, sys, json, math
import numpy as np
from mathutils import Matrix, Quaternion, Vector

argv = sys.argv[sys.argv.index("--") + 1:]
JOBS = json.load(open(argv[0], encoding="utf-8"))
OUT = argv[1]
FPS = 24
sc = bpy.context.scene
sc.render.fps = FPS

MAP = {"pelvis": "Hips", "spine_01": "LowerBack", "spine_02": "Spine", "spine_03": "Spine1",
       "neck_01": "Neck", "head": "Head",
       "clavicle_l": "LeftShoulder", "upperarm_l": "LeftArm", "lowerarm_l": "LeftForeArm", "hand_l": "LeftHand",
       "clavicle_r": "RightShoulder", "upperarm_r": "RightArm", "lowerarm_r": "RightForeArm", "hand_r": "RightHand",
       "thigh_l": "LeftUpLeg", "calf_l": "LeftLeg", "foot_l": "LeftFoot", "ball_l": "LeftToeBase",
       "thigh_r": "RightUpLeg", "calf_r": "RightLeg", "foot_r": "RightFoot", "ball_r": "RightToeBase"}

def wpos(obj, name, tail=False):
    b = obj.data.bones[name]
    return obj.matrix_world @ (b.tail_local if tail else b.head_local)
def rest_rot(obj, name):
    return (obj.matrix_world.to_3x3() @ obj.data.bones[name].matrix_local.to_3x3()).to_quaternion()
def pose_rot(obj, name):
    return (obj.matrix_world.to_3x3() @ obj.pose.bones[name].matrix.to_3x3()).to_quaternion()
def rest_dir(obj, name):
    b = obj.data.bones[name]
    return (obj.matrix_world.to_3x3() @ (b.tail_local - b.head_local)).normalized()

def retarget(job, speeds):
    rig = bpy.data.objects[job["rig"]]
    NF = job.get("frames", 192)
    if rig.animation_data:
        rig.animation_data_clear()
    loc0, rot0 = rig.location.copy(), rig.rotation_euler.copy()
    rig.location = (0, 0, 0); rig.rotation_euler = (0, 0, 0)
    for pb in rig.pose.bones:
        pb.rotation_mode = "QUATERNION"; pb.rotation_quaternion = (1, 0, 0, 0); pb.location = (0, 0, 0)
    bpy.context.view_layer.update()
    for o in bpy.context.selected_objects: o.select_set(False)
    bpy.ops.import_anim.bvh(filepath=job["bvh"], global_scale=1.0, frame_start=1, use_fps_scale=True,
                            update_scene_fps=False, update_scene_duration=False, rotate_mode="NATIVE")
    src = bpy.context.active_object
    f0, f1 = [int(round(x)) for x in src.animation_data.action.frame_range]
    sc.frame_set(f0)
    left = wpos(src, "LeftUpLeg") - wpos(src, "RightUpLeg"); left.z = 0; left.normalize()
    yaw = left.to_2d().angle_signed(Vector((1, 0)))
    src.matrix_world = Matrix.Rotation(-yaw, 4, "Z") @ src.matrix_world
    bpy.context.view_layer.update()
    ratio = (wpos(rig, "thigh_l") - wpos(rig, "foot_l")).length / (wpos(src, "LeftUpLeg") - wpos(src, "LeftFoot")).length
    OFF = {t: (rest_dir(rig, t).rotation_difference(rest_dir(src, s)) if t != "pelvis" else Quaternion()) for t, s in MAP.items()}
    RR_t = {t: rest_rot(rig, t) for t in MAP}
    RR_s = {s: rest_rot(src, s) for s in MAP.values()}
    pelvis_rest = rig.data.bones["pelvis"].head_local.copy()
    order = sorted([b.name for b in rig.data.bones if b.name in MAP], key=lambda n: len(rig.data.bones[n].parent_recursive))
    arms = {k: Vector(v).normalized() for k, v in job.get("arms", {}).items()}
    aw = job.get("arm_weight", 0.85)
    frames = []
    for fr in range(f0, f1 + 1):
        sc.frame_set(fr)
        rec = {}
        for t in order:
            s = MAP[t]
            want = pose_rot(src, s) @ RR_s[s].inverted() @ OFF[t] @ RR_t[t]
            if t in arms:
                cur = (want @ RR_t[t].inverted()) @ rest_dir(rig, t)
                want = Quaternion().slerp(cur.rotation_difference(arms[t]), aw) @ want
            pb = rig.pose.bones[t]
            M = want.to_matrix().to_4x4()
            if t == "pelvis":
                hp = src.matrix_world @ src.pose.bones["Hips"].head
                off = (hp - (src.matrix_world @ src.data.bones["Hips"].head_local)) * ratio
                M.translation = Vector((pelvis_rest.x + off.x, pelvis_rest.y + off.y, hp.z * ratio))
            else:
                M.translation = pb.head
            pb.matrix = M
            bpy.context.view_layer.update()
            rec[t] = pb.rotation_quaternion.copy()
            if t == "pelvis":
                rec["_pelM"] = pb.matrix.copy()
        rec["_hips"] = (src.matrix_world @ src.pose.bones["Hips"].head) * ratio
        frames.append(rec)
    n = len(frames)
    H = np.array([list(fr["_hips"]) for fr in frames])
    speed = math.hypot(np.polyfit(np.arange(n), H[:, 1], 1)[0], np.polyfit(np.arange(n), H[:, 0], 1)[0]) * FPS
    keys = [t for t in order if t != "pelvis"]
    V = np.array([np.concatenate([list(frames[i][t]) for t in keys]) for i in range(n)])
    best = None
    for a in range(0, max(1, n // 2)):
        for P in range(int(0.85 * FPS), int(1.7 * FPS)):
            b = a + P
            if b >= n: break
            d = np.minimum(np.abs(V[a] - V[b]), np.abs(V[a] + V[b])).sum()
            if best is None or d < best[0]:
                best = (d, a, P)
    _, A, P = best
    ts = 1.0
    if job.get("match_speed_of") and job["match_speed_of"] in speeds:
        ts = speeds[job["match_speed_of"]] / speed
    rig.animation_data_create()
    MA = frames[A]["_pelM"].translation; MB = frames[A + P]["_pelM"].translation
    phase0 = job.get("phase", 0.0)
    for f in range(1, NF + 1):
        u = ((f - 1) * ts + phase0 * P) % P
        j0 = int(math.floor(u)); fr_ = u - j0; j1 = (j0 + 1) % P
        i0, i1 = A + j0, A + j1
        for t in order:
            if t == "pelvis": continue
            pb = rig.pose.bones[t]
            pb.rotation_quaternion = frames[i0][t].slerp(frames[i1][t], fr_)
            pb.keyframe_insert("rotation_quaternion", frame=f)
        M0 = frames[i0]["_pelM"]; M1 = frames[i1]["_pelM"]
        q = M0.to_quaternion().slerp(M1.to_quaternion(), fr_)
        tr = M0.translation.lerp(M1.translation, fr_)
        trend = MA + (MB - MA) * (u / P)
        d = tr - trend
        M = q.to_matrix().to_4x4(); M.translation = Vector((pelvis_rest.x + d.x, pelvis_rest.y + d.y, tr.z))
        pb = rig.pose.bones["pelvis"]; pb.matrix = M
        bpy.context.view_layer.update()
        pb.keyframe_insert("location", frame=f); pb.keyframe_insert("rotation_quaternion", frame=f)
    lows = []
    for f in range(1, min(NF, int(P / max(ts, 1e-3)) + 2) + 1):
        sc.frame_set(f)
        z = min((rig.matrix_world @ rig.pose.bones[b].tail).z for b in ("ball_l", "ball_r"))
        z = min(z, min((rig.matrix_world @ rig.pose.bones[b].head).z for b in ("foot_l", "foot_r")) - 0.06 * ratio / 0.058)
        lows.append(z)
    rig["foot_min"] = float(min(lows))
    rig["speed_mps"] = float(speed * ts)
    rig["cycle_frames"] = float(P / ts)
    speeds[rig.name] = speed * ts
    bpy.data.objects.remove(src, do_unlink=True)
    rig.location, rig.rotation_euler = loc0, rot0
    print("RIG", rig.name, "speed", round(speed * ts, 3), "cycle", P, "ts", round(ts, 3), "foot_min", round(rig["foot_min"], 3))

speeds = {}
for job in JOBS:
    retarget(job, speeds)
sc.frame_end = max(j.get("frames", 192) for j in JOBS)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT)
