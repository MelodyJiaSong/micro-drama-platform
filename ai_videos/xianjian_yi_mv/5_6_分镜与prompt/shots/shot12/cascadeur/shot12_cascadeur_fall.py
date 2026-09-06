# shot12 第 2 拍「自画面右上角旋身斜落、双脚砸在场地正中」—— Cascadeur 版（运行在 Cascadeur 内，经 casc_run.py 投递）。
# 时刻/圈数与 previz/previz_config.toml + shot12_previz.py 对齐：A_ENTER 0.30s · A_LAND 2.00s · A_LAND_DIP 2.12s ·
# A_LAND_UP 2.32s · FALL_SPINS 5 · 俯角 20° · 人占画高 0.22。Cascadeur 场景 30fps、单位 cm、Y 向上、人面朝 +Z。
# 需要外部注入：LIB（casc_lib.py 路径）、JZ_L（左手剑指四元数 json）、OUT_DIR。
exec(open(LIB, encoding="utf-8").read())
DEFS_ONLY = bool(globals().get("DEFS_ONLY"))
if not DEFS_ONLY:
    reload_scene(r"C:\Program Files\Cascadeur\samples\Cascy.casc"); exec(open(LIB, encoding="utf-8").read())

FPS = 30
F_ENTER, F_LAND, F_DIP, F_UP, F_END = 9, 60, 64, 70, 90      # 0.30 / 2.00 / 2.12 / 2.32 s
SPINS = 5
SUBJ_H, SUBJ_FRAC, TILT, AZ = 180.0, 0.22, 20.0, 15.0        # 人高 cm · 占画高 · 俯角 · 机位偏离正前方的方位角
VFOV = 28.0                                                   # Cascadeur 视口实测竖向视角（520cm 处 180cm 高占画 69%）

bv = scene.model_viewer().behaviour_viewer()
PTS = sorted(n for n, i in IDS.items() if not bv.get_behaviour_by_name(i, "Point").is_null())
if DEFS_ONLY:
    BASE = {n: np.array(v) for n, v in json.load(open(os.path.join(OUT_DIR, "base_points.json"))).items()}
else:
    PV0 = np.array(gpos("pelvis_MainPoint", 0))
    BASE = {n: np.array(gpos(n, 0)) - PV0 for n in PTS}       # 身体局部系：骨盆为原点，面朝 +Z
    json.dump({n: v.tolist() for n, v in BASE.items()}, open(os.path.join(OUT_DIR, "base_points.json"), "w"))
GROUND_Y = -float(min(BASE[n][1] for n in PTS))               # 脚底到骨盆的高度（骨盆离地高）


def Ry(deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]], float)


def Rz(deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], float)


def Rx(deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]], float)


def hand(pose, side, wrist, rot):
    """把手腕主点放到 wrist，手的朝向点按 rot 旋转基础偏移（保持手的刚性）。"""
    m = f"hand_MainPoint_{side}"
    for n in (f"hand_DirectionPoint_{side}", f"hand_AdditionalPoint_{side}"):
        pose[n] = np.array(wrist) + rot @ (BASE[n] - BASE[m])
    pose[m] = np.array(wrist, float)



def _rot_between(a, b):
    """minimal rotation matrix taking unit vector a to unit vector b"""
    a = a / np.linalg.norm(a); b = b / np.linalg.norm(b); v = np.cross(a, b); c = float(np.dot(a, b))
    if np.linalg.norm(v) < 1e-6:
        return np.eye(3) if c > 0 else -np.eye(3)
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + vx + vx @ vx * (1 / (1 + c))


def hand_straight(pose, side, wrist, pole):
    """手腕不弯（用户 2026-09-05）：预测肘位（双骨 IK + 极向点），让手沿前臂方向延伸，手型相对前臂保持基础姿态。"""
    S = BASE[f"arm_MainPoint_{side}"]; E0 = BASE[f"forearm_MainPoint_{side}"]; W0 = BASE[f"hand_MainPoint_{side}"]
    L1 = np.linalg.norm(E0 - S); L2 = np.linalg.norm(W0 - E0)
    W = np.array(wrist, float); P = np.array(pole, float)
    d = min(np.linalg.norm(W - S), L1 + L2 - 0.5); u = (W - S) / (np.linalg.norm(W - S) + 1e-9)
    a = (L1 * L1 - L2 * L2 + d * d) / (2 * d); h = math.sqrt(max(L1 * L1 - a * a, 0.0))
    v = (P - S) - u * np.dot(P - S, u); v = v / (np.linalg.norm(v) + 1e-9)
    E = S + u * a + v * h
    R = _rot_between(W0 - E0, W - E)
    m = f"hand_MainPoint_{side}"
    for n in (f"hand_DirectionPoint_{side}", f"hand_AdditionalPoint_{side}"):
        pose[n] = W + R @ (BASE[n] - BASE[m])
    pose[m] = W; pose[f"forearm_LimbDir_{side}"] = P

def foot(pose, side, foot_pos, rot=np.eye(3)):
    m = f"foot_MainPoint_{side}"
    for n in (f"foot_Self0Point_{side}", f"toe_MainPoint_{side}", f"toe_AdditionalPoint_{side}", f"toe_DirectionPoint_{side}"):
        pose[n] = np.array(foot_pos) + rot @ (BASE[n] - BASE[m])
    pose[m] = np.array(foot_pos, float)


# ---------- 姿态（身体局部系，cm）----------
def pose_fall():
    p = {n: v.copy() for n, v in BASE.items()}
    hand_straight(p, "l", (66, 47, 0), (45, 15, -60.0))     # 左臂平张，腕不弯
    hand_straight(p, "r", (-66, 47, 0), (-45, 15, -60.0))   # 右臂平张（拎葫芦），腕不弯
    hip = BASE["thigh_MainPoint_r"]
    L1 = np.linalg.norm(BASE["calf_MainPoint_r"] - hip); L2 = np.linalg.norm(BASE["foot_MainPoint_r"] - BASE["calf_MainPoint_r"])
    knee = hip + L1 * np.array([0, -math.cos(math.radians(60)), math.sin(math.radians(60))])       # 右髋前屈 60°
    calf_dir = np.array([0, -math.cos(math.radians(18)), -math.sin(math.radians(18))])              # 膝屈 78° → 小腿向下略后
    p["calf_MainPoint_r"] = knee; p["calf_AdditionalPoint_r"] = knee + (BASE["calf_AdditionalPoint_r"] - BASE["calf_MainPoint_r"])
    foot(p, "r", knee + L2 * calf_dir, Rx(-25))
    p["calf_LimbDir_r"] = knee + np.array([-8, 10, 70.0])
    return p


def pose_ground(pelvis_h, arm_w, arm_h, arm_z):
    """双脚踩地、骨盆离地 pelvis_h；手放在 (±arm_w, arm_h, arm_z)。"""
    p = {n: v.copy() for n, v in BASE.items()}
    dy = GROUND_Y - pelvis_h                                   # 脚要比基础站姿高出多少（骨盆更低）
    for side in ("l", "r"):
        foot(p, side, BASE[f"foot_MainPoint_{side}"] + np.array([0, dy, 0]))
        p[f"calf_LimbDir_{side}"] = BASE[f"calf_LimbDir_{side}"] + np.array([0, dy * 0.5, 15.0])
    hand_straight(p, "l", (arm_w, arm_h, arm_z), BASE["forearm_LimbDir_l"] + np.array([arm_w - 25, 0, 0.0]))
    hand_straight(p, "r", (-arm_w, arm_h, arm_z), BASE["forearm_LimbDir_r"] + np.array([-(arm_w - 25), 0, 0.0]))
    return p


P_LAND = np.array([0.0, GROUND_Y, 0.0])                      # 落地时骨盆世界坐标（脚在 y=0）
FRAME_H = SUBJ_H / SUBJ_FRAC; FRAME_W = FRAME_H * 16 / 9
d = (FRAME_H / 2) / math.tan(math.radians(VFOV / 2))
t_, a_ = math.radians(TILT), math.radians(AZ)
TARGET = P_LAND + np.array([0, 40.0, 0])
CAM = TARGET + d * np.array([math.cos(t_) * math.sin(a_), math.sin(t_), math.cos(t_) * math.cos(a_)])
fwd = (TARGET - CAM) / np.linalg.norm(TARGET - CAM); RIGHT = np.cross(fwd, np.array([0, 1.0, 0])); RIGHT /= np.linalg.norm(RIGHT)
ENTER = P_LAND + RIGHT * (FRAME_W * 0.36) + np.array([0, FRAME_H * 0.62, 0])
ABOVE = P_LAND + RIGHT * (FRAME_W * 0.46) + np.array([0, FRAME_H * 1.70, 0])


def pelvis_at(f):
    if f <= F_ENTER:
        return ABOVE + (ENTER - ABOVE) * (f / F_ENTER)
    if f <= F_LAND:
        return ENTER + (P_LAND - ENTER) * ((f - F_ENTER) / (F_LAND - F_ENTER))
    return P_LAND


def theta_at(f):                                            # 绕竖轴 5 圈，落地时正对镜头(0°)
    return -360.0 * SPINS * (1 - min(f, F_LAND) / F_LAND)


def key_pose(f, local_pose, pelvis, theta, title):
    R = Ry(theta)
    world = {n: (pelvis + R @ v).tolist() for n, v in local_pose.items()}
    return set_point_pos(world, f, title)


if DEFS_ONLY:
    raise SystemExit  # 只要定义
print("anim size ->", set_anim_size(F_END + 1))
_BOX = {s: [n for n in IDS if n.startswith("f_") and n.endswith("_Box_" + s)] for s in ("l", "r")}
json.dump({s: {n: rot_to_q(r) for n, r in read_box_rot(_BOX[s], 0).items()} for s in ("l", "r")}, open(os.path.join(OUT_DIR, "relax_lr.json"), "w"))  # Cascy 原始松弛手型，供 act1 用
JZ = {n: q_to_rot(q) for n, q in json.load(open(JZ_L)).items()}
if not globals().get("NATURAL_HANDS", True):                   # 用户 2026-09-05：手指全部不动、保持自然，不再打剑指键
    set_box_rots(JZ, 0, "左手剑指")

FALL = pose_fall()
for f in range(0, F_LAND + 1):                              # 空中：逐帧打键（旋转靠密键，不靠插值）
    if f == F_LAND:
        break
    key_pose(f, FALL, pelvis_at(f), theta_at(f), f"fall f{f}")
key_pose(F_LAND, pose_ground(GROUND_Y, 58, 32, 6), P_LAND, 0.0, "land")               # 双脚砸地，臂略降
key_pose(F_DIP, pose_ground(GROUND_Y - 13, 50, 18, 12), P_LAND - np.array([0, 13.0, 0]), 0.0, "land dip")
key_pose(F_UP, pose_ground(GROUND_Y, 30, 6, 6), P_LAND, 0.0, "stand up")
if not globals().get("NO_SAVE"):
    key_pose(F_END, pose_ground(GROUND_Y, 30, 6, 6), P_LAND, 0.0, "hold")
print("interp ->", set_interpolation(PTS, [F_LAND, F_DIP, F_UP], "BEZIER"))

cam(CAM.tolist(), TARGET.tolist()); print("vis", hide_controllers("View"))
print("CAM", CAM.round(1).tolist(), "TARGET", TARGET.round(1).tolist(), "ENTER", ENTER.round(1).tolist(), "GROUND_Y", round(GROUND_Y, 1))
print("check: pelvis f30", [round(x, 1) for x in gpos("pelvis_MainPoint", 30)], "foot_l f60", [round(x, 1) for x in gpos("foot_MainPoint_l", 60)], "f64", [round(x, 1) for x in gpos("foot_MainPoint_l", 64)])
if not globals().get("NO_SAVE"):
    app.current_scene().save(os.path.join(OUT_DIR, "shot12_fall.casc")); print("saved casc")
