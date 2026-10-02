# Point-cloud FK for the Cascy rig, exec'd INSIDE Cascadeur after casc_lib.py (needs gpos / set_point_pos / IDS).
#
# A pose is a dict of joint angles (degrees) in the character's own frame (Cascy faces +Z, up +Y, left +X);
# pose_points() rotates the rest positions of every IK point distal-to-proximal (elbow before shoulder, knee before hip,
# limbs before torso lean), then yaws + places the body on the ground at a plan position.
#   armL / armR   = (flex, abd, twist)  flex: arm raised forward; abd: out to the side
#   elbowL/elbowR = flex                hipL / hipR = (flex, abd)   kneeL / kneeR = flex
#   lean = torso pitch forward about the pelvis, twist = torso yaw, head = nod down (+) / up (-)
#   drop = extra pelvis lowering (cm) on top of auto-grounding; ground="feet" | "knee" (kneeling pose)
# Plan (x east, y south, metres) -> Cascadeur (cm): cx = (x - ox) * 100, cz = (y - oy) * 100 — with the Y-up -> Z-up FBX
# import that lands exactly on Blender X = x - ox, Y = -(y - oy), i.e. the previz plan transform around origin (ox, oy).
import json
import math
import os
import tempfile
import numpy as np

POINTS = [n for n in IDS if (n.endswith(("Point", "Point_l", "Point_r", "LimbDir_l", "LimbDir_r"))
                             and not n.startswith("EdgeView") and n != "Points")]
# 静止姿态只能从刚载入的 Cascy 读：分批投递时第二批起第 0 帧早已摆过姿势，再从它读会把后面每个键都叠在转过向的底子上。
# 载入新场景后先 exec 本文件、并把 REST_FRESH 设成 True，静止姿态写进缓存；之后的批次读缓存。
REST_CACHE = os.path.join(tempfile.gettempdir(), "casc_fk_rest.json")
if globals().get("REST_FRESH") or not os.path.exists(REST_CACHE):
    REST = {n: np.array(gpos(n, 0), float) for n in POINTS}
    json.dump({n: v.tolist() for n, v in REST.items()}, open(REST_CACHE, "w"))
else:
    REST = {n: np.array(v, float) for n, v in json.load(open(REST_CACHE)).items()}
FOOT_Y = min(REST[n][1] for n in POINTS if n.startswith(("foot_", "toe_")))


def _grp(*prefixes, side=None):
    out = []
    for n in POINTS:
        if side and not n.endswith("_" + side):
            continue
        if n.startswith(prefixes):
            out.append(n)
    return out


UPPER = _grp("stomach_", "chest_", "neck_", "head_", "clavicle_", "arm_", "forearm_", "hand_")
HEAD = _grp("head_")
ARM = {s: _grp("arm_", "forearm_", "hand_", side=s) for s in "lr"}
FORE = {s: _grp("hand_", side=s) + ["forearm_AdditionalPoint_" + s] for s in "lr"}
LEG = {s: _grp("calf_", "foot_", "toe_", side=s) for s in "lr"}
SHIN = {s: _grp("foot_", "toe_", side=s) + ["calf_AdditionalPoint_" + s] for s in "lr"}


def rot(axis, deg):
    a = math.radians(deg)
    x, y, z = axis
    c, s, t = math.cos(a), math.sin(a), 1 - math.cos(a)
    return np.array([[t * x * x + c, t * x * y - s * z, t * x * z + s * y],
                     [t * x * y + s * z, t * y * y + c, t * y * z - s * x],
                     [t * x * z - s * y, t * y * z + s * x, t * z * z + c]])


X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)


def _apply(P, names, pivot, R):
    c = P[pivot]
    for n in names:
        P[n] = c + R @ (P[n] - c)


def pose_points(pose, x, y, face, origin):
    """pose dict -> {point: [cx, cy, cz]} at plan (x, y) facing plan vector `face`."""
    P = {n: v.copy() for n, v in REST.items()}
    for s, sgn in (("l", 1), ("r", -1)):
        _apply(P, FORE[s], "forearm_MainPoint_" + s, rot(X, -pose.get("elbow" + s.upper(), 0)))
        fl, ab, tw = (tuple(pose.get("arm" + s.upper(), (0, 0, 0))) + (0, 0, 0))[:3]
        R = rot(X, -fl) @ rot(Z, sgn * ab) @ rot(Y, sgn * tw)
        _apply(P, ARM[s], "arm_MainPoint_" + s, R)
        _apply(P, SHIN[s], "calf_MainPoint_" + s, rot(X, pose.get("knee" + s.upper(), 0)))
        hf, ha = (tuple(pose.get("hip" + s.upper(), (0, 0))) + (0, 0))[:2]
        _apply(P, LEG[s], "thigh_MainPoint_" + s, rot(X, -hf) @ rot(Z, sgn * ha))
    _apply(P, HEAD, "neck_MainPoint", rot(X, pose.get("head", 0)))
    _apply(P, UPPER, "pelvis_MainPoint", rot(Y, pose.get("twist", 0)) @ rot(X, pose.get("lean", 0)))
    # ground: lowest foot on the floor, or the lower knee ~6 cm above it when kneeling
    if pose.get("ground") == "knee":
        low = min(P["calf_MainPoint_l"][1], P["calf_MainPoint_r"][1]) - 6.0
    else:
        low = min(P[n][1] for n in POINTS if n.startswith(("foot_", "toe_"))) - FOOT_Y
    dy = -low - pose.get("drop", 0) + pose.get("lift", 0)
    yaw = math.degrees(math.atan2(face[0], face[1]))
    Ry = rot(Y, yaw)
    pc = REST["pelvis_MainPoint"].copy()
    pc[1] = 0
    base = np.array([(x - origin[0]) * 100.0, dy, (y - origin[1]) * 100.0])
    return {n: (Ry @ (P[n] - pc) + base + np.array([0, 0, 0])).tolist() for n in POINTS}


def key_pose(frame, pose, x, y, face, origin, title="fk pose"):
    return set_point_pos(pose_points(pose, x, y, face, origin), int(frame), title)
