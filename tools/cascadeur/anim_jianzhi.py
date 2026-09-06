exec(open(LIB, encoding="utf-8").read())
reload_scene(); exec(open(LIB, encoding="utf-8").read())
print("anim size ->", set_anim_size(101))
JZ = {n: rot_from_xyz(v) for n, v in json.load(open(JZ_PATH)).items()}
json.dump({n: rot_to_q(r) for n, r in JZ.items()}, open(JZ_PATH.replace(".json", "_q.json"), "w"))
BOXES = list(JZ)
GRIP = read_box_rot(BOXES, 0)
PTS = ["hand_MainPoint_r", "hand_DirectionPoint_r", "hand_AdditionalPoint_r"]


def hand_frame(frame):
    H = np.array(gpos("hand_r", frame)); M2 = np.array(gpos("f_middle2_r", frame))
    I1 = np.array(gpos("f_index1_r", frame)); K1 = np.array(gpos("f_pinky1_r", frame))
    f = M2 - H; f /= np.linalg.norm(f)
    n = np.cross(I1 - H, K1 - H); n /= np.linalg.norm(n)
    return np.stack([f, n, np.cross(n, f)], axis=1)


def place_hand(frame, wrist_t, fdir_t, n_t, pole=None, title="place hand"):
    fdir_t = np.array(fdir_t, float); fdir_t /= np.linalg.norm(fdir_t)
    n_t = np.array(n_t, float); n_t -= fdir_t * np.dot(n_t, fdir_t); n_t /= np.linalg.norm(n_t)
    Rt = np.stack([fdir_t, n_t, np.cross(n_t, fdir_t)], axis=1)
    Rot = Rt @ hand_frame(frame).T
    P = {n: np.array(gpos(n, frame)) for n in PTS}
    new = {n: (np.array(wrist_t) + Rot @ (P[n] - P["hand_MainPoint_r"])).tolist() for n in PTS}
    if pole is not None:
        new["forearm_LimbDir_r"] = list(pole)
    return set_point_pos(new, frame, title)


def key_all(frame, title):
    """pin the current pose of the right arm points + finger boxes at `frame`."""
    P = {n: gpos(n, frame) for n in PTS + ["forearm_LimbDir_r", "forearm_MainPoint_r", "arm_MainPoint_r"]}
    set_point_pos(P, frame, title)
    set_box_rots(read_box_rot(BOXES, frame), frame, title)


# f0: grip stance pinned
key_all(0, "f0 grip")
# f35: 剑指 raised vertical beside the right cheek
UP = [-20.0, 118.0, 14.0]
set_box_rots(JZ, 35, "f35 剑指")
place_hand(35, UP, [0, 1, 0], [1, 0, 0], pole=[-35.0, 63.0, -6.0], title="f35 raise")
# f45: hold
key_all(45, "f45 hold")
# f20: halfway, hand already leaving the hilt (breakdown) - fingers interpolate on their own
MID = [-16.0, 98.0, 26.0]
place_hand(20, MID, [0.3, 0.9, 0.3], [0.9, 0, -0.3], pole=[-38.0, 70.0, -12.0], title="f20 breakdown")
# f55: 点出 thrust forward at eye level, fingers +Z, thumb up (palm faces -X)
STRIKE = [-12.0, 126.0, 52.0]
set_box_rots(JZ, 55, "f55 剑指")
place_hand(55, STRIKE, [0, 0.05, 1], [1, 0.2, 0], pole=[-40.0, 100.0, 10.0], title="f55 strike")
# f70: settle back a little, hold gesture
SETTLE = [-13.0, 123.0, 44.0]
set_box_rots(JZ, 70, "f70 剑指")
place_hand(70, SETTLE, [0, 0.15, 1], [1, 0.2, 0], pole=[-40.0, 98.0, 8.0], title="f70 settle")

lv = scene.layers_viewer()
lay = lv.layer(lv.layer_id_by_obj_id(IDS["hand_MainPoint_r"]))
print("hand_MainPoint_r keys:", [f for f in range(0, 101) if lay.is_key(f)])
for pos in (10, 28, 40, 50, 62):
    try:
        sec = lay.find_section(pos)
        print("section@", pos, sec.interval.interpolation if sec is not None else None)
    except Exception as e:
        print("section err", pos, str(e)[:80])
lay2 = lv.layer(lv.layer_id_by_obj_id(IDS["f_index2_Box_r"]))
print("f_index2_Box_r keys:", [f for f in range(0, 101) if lay2.is_key(f)])
print("wrist f35", [round(x,1) for x in gpos("hand_r", 35)], "f55", [round(x,1) for x in gpos("hand_r", 55)], "f20", [round(x,1) for x in gpos("hand_r", 20)])
