# shot12 第二幕（15.0–27.4 s）身体动作 + 单把剑全程（0–27.4 s）—— Cascadeur 版。
# 在已含第一幕的场景上追加。时刻来自 previz_config.toml 时长链（dur_spin=2.0 → 总长 27.4 s）。
# 单剑代替剑阵（用户 2026-09-05：做不出多把剑，一把总可以）：背上 → 出鞘飞到身前 → 绕身 → 归掌 → 两斩 →
# 抛剑高悬 → 升空出画 → 落回插地 → 拔起托在单脚下（踩剑）→ 冲天掉头 → 回鞘 → 随身。
# 分段投递：STAGE "body2a"（斩击/抛剑/结印）"body2b"（亮相/跳旋踩剑/跟斗/落地/大笑）"sword"（剑全程）"wrists2"（腕校直 15–27.4s）"finish"
# 需要外部注入：LIB、JZ_L、FALL_SCRIPT、ACT1_SCRIPT、OUT_DIR、STAGE。
STAGE2 = globals().get("STAGE", "body2a")
STAGE = "none"                                          # 先只取 act1 的定义（姿态构造器、K、STAND…）
exec(open(ACT1_SCRIPT, encoding="utf-8").read())
STAGE = STAGE2
LOG = os.path.join(OUT_DIR, "build.log")

T_TOTAL = 20.50                                          # 27.4 - 6.9（第一幕 15.0 → 8.1）
# ---- 第二幕时刻（config 时长链，秒）----
ACT2 = 8.10
T_WIND1, T_SLASH1, T_WIND2, T_SLASH2 = ACT2 + 0.25, ACT2 + 0.45, ACT2 + 0.90, ACT2 + 1.08
T_THROW_WIND, T_THROW, T_SWORD_HIGH, T_SEAL, T_EYES = ACT2 + 1.50, ACT2 + 1.65, ACT2 + 2.20, ACT2 + 2.50, ACT2 + 2.90
T_SPLIT, T_SPIN_END, T_RISE_END = ACT2 + 3.00, ACT2 + 6.40, ACT2 + 7.00
T_POINT, T_DROP0, T_DROP_DUR = ACT2 + 7.45, ACT2 + 7.60, 0.34
T_JUMP0, T_JUMP_TOP, T_JUMP1, T_GATHER1, T_MERGE = ACT2 + 9.28, ACT2 + 9.52, ACT2 + 9.76, ACT2 + 10.00, ACT2 + 10.02
T_BOUNCE = tuple(ACT2 + x for x in (10.10, 10.18, 10.26, 10.36))
T_FLIP0, T_FLIP1, T_LAND_DIP, T_LAND_UP = ACT2 + 10.42, ACT2 + 11.05, ACT2 + 11.12, ACT2 + 11.28
T_SWORD_UP, T_SWORD_APEX, T_SHEATH = ACT2 + 11.15, ACT2 + 11.28, ACT2 + 11.50
T_LAUGH, T_LAUGH_BOBS = ACT2 + 11.54, tuple(ACT2 + x for x in (11.70, 11.86, 12.02))
STAND_Z, HIGH_Y, RISE_Y = 170.0, 387.0, 900.0         # 踩剑悬空高度 / 抛剑高悬 / 升空出画（cm）
AIR_SPINS, FLIP_COUNT = 2, 2
SLOT = np.array([-110.0, 15.0, 60.0])                  # 单剑插地点（剑心；剑尖入土 35）
SWORD_L, SWORD_HALF = 100.0, 50.0

# ---- 姿态构造 ----
def stance(p, pelvis_h, rz=0.0, lz=0.0, rx=None, lx=None):
    """双脚踩地：骨盆离地 pelvis_h，右/左脚沿 z 前后挪 rz/lz（cm）。"""
    dy = GROUND_Y - pelvis_h
    for side, dz, dx in (("r", rz, rx), ("l", lz, lx)):
        base = BASE[f"foot_MainPoint_{side}"].copy(); base[1] += dy; base[2] += dz
        if dx is not None: base[0] = dx
        foot(p, side, base); p[f"calf_LimbDir_{side}"] = BASE[f"calf_LimbDir_{side}"] + np.array([0, dy * 0.5 + 5, 20.0 + dz * 0.5])


def upper_yaw(p, deg):                       # 拧腰：上半身绕骨盆竖轴
    R = Ry(deg)
    for n in p:
        if not any(n.startswith(k) for k in LEG_KEYS) and not n.startswith("pelvis"):
            p[n] = R @ p[n]


def upper_lean(p, deg):                      # 上半身绕骨盆 X 轴：负＝后仰
    R = Rx(deg)
    for n in p:
        if not any(n.startswith(k) for k in LEG_KEYS) and not n.startswith("pelvis"):
            p[n] = R @ p[n]


def raise_leg(p, side, hip_deg=70, knee_deg=95):
    sgn = 1 if side == "l" else -1
    hip = BASE[f"thigh_MainPoint_{side}"]
    L1 = np.linalg.norm(BASE[f"calf_MainPoint_{side}"] - hip); L2 = np.linalg.norm(BASE[f"foot_MainPoint_{side}"] - BASE[f"calf_MainPoint_{side}"])
    knee = hip + L1 * np.array([0, -math.cos(math.radians(hip_deg)), math.sin(math.radians(hip_deg))])
    calf_dir = np.array([0, -math.cos(math.radians(hip_deg - knee_deg)), math.sin(math.radians(hip_deg - knee_deg))])
    p[f"calf_MainPoint_{side}"] = knee; p[f"calf_AdditionalPoint_{side}"] = knee + (BASE[f"calf_AdditionalPoint_{side}"] - BASE[f"calf_MainPoint_{side}"])
    foot(p, side, knee + L2 * calf_dir, Rx(-25)); p[f"calf_LimbDir_{side}"] = knee + np.array([sgn * 8, 10, 70.0])


def pose_end12():                            # 持剑垂手立定（第一幕末）
    return pose_end()


GRAB = (-8, 47, 45)                          # 剑柄顶（身体局部系）：剑停在身前 0.45 m、剑心 0.9 m 高 → 柄顶 1.4 m


def pose_reach():                             # 用户 2026-09-06：右手伸出去拿停在身前的剑
    p = copy_pose(STAND); hand_straight(p, "r", GRAB, (-46, 30, 18.0)); upper_lean(p, 8); return p


def pose_wind1():
    p = copy_pose(STAND); hand_straight(p, "r", (-22, 92, -20), (-55, 75, -35.0)); hand_straight(p, "l", (32, 12, -18), (52, 8, -40.0)); upper_lean(p, -6); return p


def pose_slash1():
    p = copy_pose(STAND); stance(p, GROUND_Y - 8, rz=32); hand_straight(p, "r", (-14, 30, 52), (-45, 40, 25.0)); hand_straight(p, "l", (36, 22, 8), (52, 20, -20.0)); upper_lean(p, 10); return p


def pose_wind2():
    p = copy_pose(STAND); stance(p, GROUND_Y - 6, rz=32); hand_straight(p, "r", (24, 60, 14), (-10, 34, 40.0)); hand_straight(p, "l", (30, 25, -12), (52, 20, -30.0)); upper_yaw(p, -35); return p


def pose_slash2():
    p = copy_pose(STAND); stance(p, GROUND_Y - 6, rz=32); hand_straight(p, "r", (-64, 47, 4), (-45, 20, -30.0)); hand_straight(p, "l", (40, 30, -12), (52, 22, -30.0)); upper_yaw(p, 30); return p


def pose_throw_wind():
    p = copy_pose(STAND); hand_straight(p, "r", (-26, 34, 24), (-55, 30, -5.0)); return p


def pose_throw():
    p = copy_pose(STAND); hand_straight(p, "r", (-18, 94, 4), (-45, 60, -20.0)); head_tilt(p, -30); upper_lean(p, -5); return p


def pose_seal_up(tilt=-22):                   # 剑阵段：同一道家手印放在身前（用户 2026-09-06 二改 + 参考图），只加抬头
    p = pose_seal(); head_tilt(p, tilt); return p


def pose_seal1():
    return pose_seal_up(-22)


def pose_seal_still():
    return pose_seal_up(-10)


def pose_point():                             # 亮相：右臂伸直、剑指二指往前一指（用户 2026-09-06：特效结束后两指前指，剑依次落地），左手收腰侧，右脚前踏半马步
    p = copy_pose(STAND); stance(p, GROUND_Y - 12, rz=40); hand_straight(p, "r", (-16, 34, 50), (-48, 35, 18.0)); hand_straight(p, "l", (24, 8, 6), BASE["forearm_LimbDir_l"], roll=ROLL_IN["l"]); upper_lean(p, 8); return p


def pose_spread():                            # 双臂平张、左腿抬起（右脚踩剑）
    p = copy_pose(STAND); hand_straight(p, "l", (66, 47, 0), (45, 15, -60.0), roll=ROLL_IN["l"]); hand_straight(p, "r", (-66, 47, 0), (-45, 15, -60.0), roll=ROLL_IN["r"]); raise_leg(p, "l"); return p


def pose_tuck():                              # 团身
    p = copy_pose(STAND)
    for side, sgn in (("l", 1), ("r", -1)):
        foot(p, side, np.array([sgn * 12, -38, 26.0]), Rx(-40)); p[f"calf_LimbDir_{side}"] = np.array([sgn * 20, -5, 95.0])
        hand_straight(p, side, (sgn * 22, 28, 30), (sgn * 50, 10, 20.0))
    head_tilt(p, 20); return p


def pose_land():                              # 落地屈膝、双臂外撑
    p = copy_pose(STAND); stance(p, GROUND_Y - 22, rz=10, lz=-10); hand_straight(p, "r", (-46, 22, 14), (-55, 15, -25.0), roll=ROLL_IN["r"]); hand_straight(p, "l", (46, 22, 14), (55, 15, -25.0), roll=ROLL_IN["l"]); upper_lean(p, 8); return p


def pose_laugh(bob=0.0):
    p = copy_pose(STAND); hand_straight(p, "r", (-36, 14, 10), BASE["forearm_LimbDir_r"], roll=ROLL_IN["r"]); hand_straight(p, "l", (36, 14, 10), BASE["forearm_LimbDir_l"], roll=ROLL_IN["l"])
    upper_lean(p, -8 + bob); head_tilt(p, -38 + bob * 1.5); return p


def lerp_pose(a, b, u):
    return {n: a[n] * (1 - u) + b[n] * u for n in a}


def KW(t, local, pelvis, yaw=0.0, title=""):
    ok = key_pose(F(t), local, np.array(pelvis, float), yaw, title or f"t{t}"); log(f"key {title or t} f{F(t)} ->", ok); return ok


PEL0 = P_LAND
if STAGE == "body2a":
    log("anim size ->", set_anim_size(F(T_TOTAL) + 1)); log("visible ->", set_visible_range(0, F(T_TOTAL)))   # 可视范围外的帧不求值：读到的全是最后一个可视帧的姿态（2026-09-06 实测）
    KW(7.45, pose_seal(), PEL0, title="seal before reach"); KW(7.85, pose_reach(), PEL0, title="reach sword")
    KW(ACT2, pose_end12(), PEL0, title="end12"); KW(T_WIND1 - 0.15, pose_end12(), PEL0, title="pre-wind1")
    KW(T_WIND1, pose_wind1(), PEL0, title="wind1"); KW(T_SLASH1, pose_slash1(), PEL0 - [0, 8, 0], title="slash1"); KW(T_WIND2 - 0.35, pose_slash1(), PEL0 - [0, 8, 0], title="slash1 hold")
    KW(T_WIND2, pose_wind2(), PEL0 - [0, 6, 0], title="wind2"); KW(T_SLASH2, pose_slash2(), PEL0 - [0, 6, 0], title="slash2"); KW(T_THROW_WIND - 0.25, pose_slash2(), PEL0 - [0, 6, 0], title="slash2 hold")
    KW(T_THROW_WIND, pose_throw_wind(), PEL0, title="throw wind"); KW(T_THROW, pose_throw(), PEL0, title="throw"); KW(T_SWORD_HIGH - 0.15, pose_throw(), PEL0, title="throw hold")
    KW(T_SEAL, pose_seal1(), PEL0, title="seal1"); KW(T_EYES, pose_seal_still(), PEL0, title="seal still")
    KW(T_POINT - 0.15, pose_seal_still(), PEL0, title="seal hold")                    # 用户 2026-09-06：剑阵在空中时人物结印不动、双脚接地（不浮起）；手印保持到 T_POINT-0.15，再 0.15 s 内「猛然」前指（用户 2026-09-06）
    _nat = natural_hands(); _jz2 = {s: {n: q_to_rot(q) for n, q in json.load(open(HANDS_JSON_IN))["JZ"][s].items()} for s in ("l", "r")}
    _seal2 = {"r": _jz2["r"], "l": grip_hands()["l"]}                             # 剑阵段道家手印：右手剑指、左手握右拳
    _point = {"r": _jz2["r"], "l": _nat["l"]}                                     # 亮相：右手保持剑指二指前指，左手放松
    for fr, tbl in ((F(T_SEAL - 0.3), _nat), (F(T_SEAL), _seal2), (F(T_POINT - 0.15), _seal2), (F(T_POINT), _point), (F(T_JUMP0 - 0.15), _point), (F(T_JUMP0), _nat)):
        for s in ("l", "r"):
            set_box_rots(tbl[s], fr, f"seal2 fingers {s} f{fr}")

elif STAGE == "body2b":
    KW(T_POINT, pose_point(), PEL0 - [0, 12, -10], title="point"); KW(T_JUMP0 - 0.15, pose_point(), PEL0 - [0, 12, -10], title="point hold")
    KW(T_JUMP0, pose_spread(), PEL0, title="jump0")
    f0, f1, ftop = F(T_JUMP0), F(T_JUMP1), F(T_JUMP_TOP)
    SP = pose_spread()
    for fr in range(f0 + 1, f1 + 1):                          # 跳起 + 空中转 2 圈：逐帧
        u = (fr - f0) / (f1 - f0); yaw = 360.0 * AIR_SPINS * u
        if fr <= ftop:
            y = GROUND_Y + (STAND_Z + 35) * ((fr - f0) / (ftop - f0))
        else:
            y = GROUND_Y + STAND_Z + 35 * (1 - (fr - ftop) / (f1 - ftop))
        key_pose(fr, SP, np.array([0, y, 0.0]), yaw, f"jump f{fr}")
    log("jump keys done")
    KW(T_MERGE, pose_spread(), [0, GROUND_Y + STAND_Z, 0], title="merge")
    for tb, dz in zip(T_BOUNCE, (-9, 0, -6, 0)):
        KW(tb, pose_spread(), [0, GROUND_Y + STAND_Z + dz, 0], title=f"bounce {tb}")
    KW(T_FLIP0, pose_spread(), [0, GROUND_Y + STAND_Z, 0], title="flip0")
    fa, fb = F(T_FLIP0), F(T_FLIP1); TK, LD = pose_tuck(), pose_land()
    p0 = np.array([0, GROUND_Y + STAND_Z, 0.0]); p1 = np.array([0, GROUND_Y, 0.0])
    for fr in range(fa + 1, fb + 1):                           # 跃开翻两个跟斗：逐帧（骨盆抛物线 + 前空翻）
        u = (fr - fa) / (fb - fa)
        pel = p0 * (1 - u) + p1 * u + np.array([0, 110 * 4 * u * (1 - u), 90 * math.sin(math.pi * u)])
        tt = T_FLIP0 + u * (T_FLIP1 - T_FLIP0)
        if tt < T_FLIP0 + 0.25:   pose = lerp_pose(SP, TK, (tt - T_FLIP0) / 0.25)
        elif tt < T_FLIP1 - 0.15: pose = TK
        else:                     pose = lerp_pose(TK, LD, (tt - (T_FLIP1 - 0.15)) / 0.20)
        R = Rx(360.0 * FLIP_COUNT * u)
        world = {n: (pel + R @ v).tolist() for n, v in pose.items()}
        set_point_pos(world, fr, f"flip f{fr}")
    log("flip keys done")
    KW(T_LAND_DIP, pose_land(), [0, GROUND_Y - 22, 0], title="land dip"); KW(T_LAND_UP, STAND, PEL0, title="land up")
    KW(T_LAUGH, pose_laugh(), PEL0, title="laugh")
    for k, tb in enumerate(T_LAUGH_BOBS):
        KW(tb, pose_laugh(3.0 if k % 2 == 0 else -2.0), PEL0, title=f"laugh bob {k}")
    KW(T_TOTAL, pose_laugh(), PEL0, title="laugh end")

elif STAGE == "sword":
    import common.mesh as c_mh
    cur = {_MV.get_object_name(i): i for i in _MV.get_objects()}
    sw_name = next((n for n in cur if n.startswith("Sword")), None)
    if sw_name is None:
        before = set(cur.values()); c_mh.add_object_with_mesh(scene, "objects/cube.partscasc", "Sword")
        cur = {_MV.get_object_name(i): i for i in _MV.get_objects()}; sw_name = next(n for n, i in cur.items() if i not in before)
    SW = cur[sw_name]; IDS.update(cur); log("sword object:", sw_name)
    CUBE0 = float(globals().get("CUBE_NATIVE", 100.0))    # cube.partscasc 原始边长（cm）
    def frame_of(f):                                        # 身体坐标系：列 = [左, 上, 前]
        pel = np.array(gpos("pelvis_MainPoint", f)); up = np.array(gpos("chest_MainPoint", f)) - pel; up /= np.linalg.norm(up)
        left = np.array(gpos("thigh_MainPoint_l", f)) - np.array(gpos("thigh_MainPoint_r", f)); left -= up * np.dot(left, up); left /= np.linalg.norm(left)
        fwd = np.cross(left, up); return pel, np.stack([left, up, fwd], axis=1)
    def rot_y_to(ydir, zhint):
        y = np.array(ydir, float); y /= np.linalg.norm(y); z = np.array(zhint, float); z -= y * np.dot(z, y)
        if np.linalg.norm(z) < 1e-6: z = np.array([0, 0, 1.0]) - y * y[2]
        z /= np.linalg.norm(z); x = np.cross(y, z); return np.stack([x, y, z], axis=1)
    def on_back(f):
        pel, Fm = frame_of(f); Rt = Fm @ Rz(-14) @ Rx(18)
        return pel + Fm @ np.array([-6, 38, -20.0]), Rt @ np.array([0, 1, 0.0]), Rt @ np.array([0, 0, 1.0])
    keys = {}                                               # frame -> (center, ydir, zhint)
    def K_(f, c, y, z=(0, 0, 1.0)): keys[int(f)] = (np.array(c, float), np.array(y, float), np.array(z, float))
    for f in list(range(0, 61)) + list(range(62, F(6.20) + 1, 2)):
        c, y, z = on_back(f); K_(f, c, y, z)
    c, y, z = on_back(F(6.20)); K_(F(6.27), c + y * 55, y, z)               # 竖直拔出鞘（用户 2026-09-06：出鞘→身前→落手，不悬停）
    K_(F(6.64), (0, 255, 73), (0, 1, 0)); K_(F(6.79), (-4, 170, 110), (0, 1, 0))
    HOVER = np.array([-8, 90, 45.0]); K_(F(7.31), HOVER, (0, 1, 0)); K_(F(7.85), HOVER, (0, 1, 0))   # 停在身前等手来拿（用户 2026-09-06）
    fg0, fg1 = F(7.85), F(ACT2)
    for fr in range(fg0 + 1, fg1 + 1):                        # 握住后：剑从竖直渐变为沿前臂延伸，柄在手中
        u = (fr - fg0) / (fg1 - fg0)
        hand = np.array(gpos("hand_MainPoint_r", fr)); elbow = np.array(gpos("forearm_MainPoint_r", fr))
        fa = hand - elbow; fa /= np.linalg.norm(fa); a = (1 - u) * np.array([0, -1, 0.0]) + u * fa; a /= np.linalg.norm(a)
        K_(fr, hand + a * SWORD_HALF, -a)
    for fr in range(F(ACT2), F(T_THROW) + 1):                 # 握剑斩击：剑沿前臂延伸，柄在手中
        hand = np.array(gpos("hand_MainPoint_r", fr)); elbow = np.array(gpos("forearm_MainPoint_r", fr))
        a = hand - elbow; a /= np.linalg.norm(a); K_(fr, hand + a * SWORD_HALF, -a)
    hand = np.array(gpos("hand_MainPoint_r", F(T_THROW)))
    K_(F(T_THROW + 0.25), hand + [0, 90, 0], (0, -1, 0)); K_(F(T_SWORD_HIGH), (0, HIGH_Y, 0), (0, -1, 0))   # 剑尖朝上高悬
    K_(F(T_SPLIT), (0, HIGH_Y, 0), (0, -1, 0)); K_(F(T_SPIN_END), (0, HIGH_Y, 0), (0, -1, 0))
    K_(F(T_RISE_END), (0, RISE_Y, 0), (0, -1, 0))                                                        # 冲出画面上缘
    K_(F(T_DROP0), (SLOT[0], RISE_Y, SLOT[2]), (0, -1, 0)); K_(F(T_DROP0 + 0.2), (SLOT[0], RISE_Y * 0.45, SLOT[2]), (0, 1, 0))   # 途中掉头尖朝下
    K_(F(T_DROP0 + T_DROP_DUR), SLOT, (0, 1, 0)); K_(F(T_JUMP1), SLOT, (0, 1, 0))                          # 插地
    for fr in range(F(T_GATHER1), F(T_FLIP0) + 1):             # 拔起托在右脚底：竖直尖朝下、柄顶托脚底，随脚震
        sole = np.array(gpos("foot_MainPoint_r", fr)) - [0, 9.3, 0]
        K_(fr, sole - [0, 2 + SWORD_HALF, 0], (0, 1, 0))
    last = keys[F(T_FLIP0)][0]; K_(F(T_FLIP1), last, (0, 1, 0)); K_(F(T_SWORD_UP), last, (0, -1, 0))
    K_(F(T_SWORD_APEX), (0, 630, 0), (0, -1, 0)); K_(F(T_SWORD_APEX + 0.1), (0, 600, 0), (0, 1, 0))       # 冲天、掉头
    for fr in range(F(T_SHEATH), F(T_TOTAL) + 1, 2):           # 回鞘随身
        c, y, z = on_back(fr); K_(fr, c, y, z)
    def mod(model, update, sc):
        le = model.layers_editor(); lv = scene.layers_viewer(); g = update.get_object_by_id(SW).root_group()
        s = np.array([4.0, SWORD_L, 0.8]) / CUBE0; g.node_deep("Local Scale").set_value(s.astype("float32"))
        lp, lr = g.node_deep("Local Position"), g.node_deep("Local Rotation"); ids = {lp.data_id(), lr.data_id()}
        for f in sorted(keys):
            c, y, z = keys[f]; lp.set_value(c.astype("float32"), f)
            lr.set_value(csc.math.Rotation.from_rotation_matrix(rot_y_to(y, z).astype("float32")), f)
            le.set_fixed_interpolation_or_key_if_need(lv.layer_id_by_obj_id(SW), f, True)
        sc.run_update(ids, 0)
    log("sword keys ->", scene.modify_update("sword keys", mod), "n", len(keys))
    log("sword interp ->", set_interpolation([sw_name], sorted(keys), "LINEAR"))   # Bezier 在「插地保持」两端会甩出大幅过冲（剑钻到地下），单剑轨迹用线性

elif STAGE == "wrists2":
    GRID = sorted(set(list(range(F(ACT2), F(T_TOTAL) + 1, 3)) + [F(T_TOTAL)]))
    # 手的 MainPoint / DirectionPoint / AdditionalPoint 共用一条 Animation Track（2026-09-06 实测）：给朝向点打键会把整条轨道
    # 在该帧的当前值一起存下来，而逐帧顺序打键时后面帧读到的是前一个新键的 STEP 值 → 手位全部僵在第一帧。
    # 对策：先把全部网格帧的肘/腕位置一次读完，再写值 + 打键，并显式写回 MainPoint；最后把网格键的区间设成 BEZIER。
    # 改完插值后 Cascadeur 在后台慢慢重算时间轴，紧接着读到的是旧缓存（2026-09-06 实测：同一帧隔几秒再读才正确）→ 读两遍直到稳定
    import time as _time
    def _read_all():
        return {(s_, f_): (np.array(gpos(f"forearm_MainPoint_{s_}", f_)), np.array(gpos(f"hand_MainPoint_{s_}", f_))) for s_ in ("l", "r") for f_ in GRID}
    for _f in GRID[::max(1, len(GRID) // 12)] + [GRID[-1]]:   # 扫一遍时间轴触发后台求值（可视范围外/新扩展的帧不会自动算）
        goto(_f)
    _time.sleep(5.0)
    pre = _read_all()
    for _try in range(6):
        _time.sleep(2.0); _again = _read_all()
        if all(np.allclose(pre[k][1], _again[k][1], atol=0.5) and np.allclose(pre[k][0], _again[k][0], atol=0.5) for k in pre):
            break
        pre = _again
    log("wrist pre-read settled after", _try + 1, "checks")
    def mod(model, update, sc):
        le = model.layers_editor(); lv = scene.layers_viewer(); ids = set(); nodes = {}
        for side in ("l", "r"):
            for n in (f"hand_MainPoint_{side}", f"hand_DirectionPoint_{side}", f"hand_AdditionalPoint_{side}"):
                nodes[n] = update.get_object_by_id(IDS[n]).root_group().node_deep("Position"); ids.add(nodes[n].data_id())
        for side in ("l", "r"):
            E0 = BASE[f"forearm_MainPoint_{side}"]; W0 = BASE[f"hand_MainPoint_{side}"]; m = f"hand_MainPoint_{side}"
            for f in GRID:
                E, W = pre[(side, f)]; R = _rot_between(W0 - E0, W - E)
                nodes[m].set_value(W.astype("float32"), f)
                for n in (f"hand_DirectionPoint_{side}", f"hand_AdditionalPoint_{side}"):
                    nodes[n].set_value((W + R @ (BASE[n] - BASE[m])).astype("float32"), f)
                le.set_fixed_interpolation_or_key_if_need(lv.layer_id_by_obj_id(IDS[m]), f, True)
        sc.run_update(ids, 0)
    log("wrists2 ->", scene.modify_update("straight wrists act2", mod))
    log("wrists2 grid interp ->", set_interpolation(["hand_MainPoint_l", "hand_MainPoint_r"], GRID, "LINEAR"))
elif STAGE == "interp":                          # 必须在 wrists2 之前（新键默认 Fixed 区间，键间读到的是缓存旧姿态）
    KT = [7.45, 7.85, ACT2, T_WIND1 - 0.15, T_WIND1, T_SLASH1, T_WIND2 - 0.35, T_WIND2, T_SLASH2, T_THROW_WIND - 0.25, T_THROW_WIND, T_THROW, T_SWORD_HIGH - 0.15,
          T_SEAL, T_EYES, T_POINT - 0.15, T_POINT, T_JUMP0 - 0.15, T_JUMP0, T_MERGE, *T_BOUNCE, T_FLIP0, T_LAND_DIP, T_LAND_UP, T_LAUGH, *T_LAUGH_BOBS, T_TOTAL]
    log("interp act2 ->", set_interpolation(PTS, sorted({F(t) for t in KT}), "LINEAR"))
    # 每一段「保持」（相邻两键姿态相同）都必须 LINEAR：Cascadeur 的 Bezier 会把下一段的大位移拉进等值区间（亮相保持段曾让人凭空浮起 46 cm、双脚离地 1.1 m）
    HOLD_STARTS = (6.20, ACT2, T_SLASH1, T_SLASH2, T_THROW, T_SEAL, T_EYES, T_SPLIT, T_POINT)
    log("holds linear ->", set_interpolation(PTS, sorted({F(t) for t in HOLD_STARTS}), "LINEAR"))
    _boxes = BOX["l"] + BOX["r"]
    log("box interp ->", set_interpolation(_boxes, sorted({F(t) for t in (T_SEAL - 0.3, T_SEAL, T_POINT - 0.15, T_POINT, T_JUMP0 - 0.15, T_JUMP0)}), "LINEAR"))
    log("box holds linear ->", set_interpolation(_boxes, sorted({0, F(5.35), F(6.50), F(T_SEAL), F(T_POINT), F(T_JUMP0)}), "LINEAR"))
elif STAGE == "finish":
    KT = [7.45, 7.85, ACT2, T_WIND1 - 0.15, T_WIND1, T_SLASH1, T_WIND2 - 0.35, T_WIND2, T_SLASH2, T_THROW_WIND - 0.25, T_THROW_WIND, T_THROW, T_SWORD_HIGH - 0.15,
          T_SEAL, T_EYES, T_POINT - 0.15, T_POINT, T_JUMP0 - 0.15, T_JUMP0, T_MERGE, *T_BOUNCE, T_FLIP0, T_LAND_DIP, T_LAND_UP, T_LAUGH, *T_LAUGH_BOBS, T_TOTAL]
    log("interp act2 ->", set_interpolation(PTS, sorted({F(t) for t in KT}), "BEZIER"))
    # 每一段「保持」（相邻两键姿态相同）都必须 LINEAR：Cascadeur 的 Bezier 会把下一段的大位移拉进等值区间（亮相保持段曾让人凭空浮起 46 cm、双脚离地 1.1 m）
    HOLD_STARTS = (6.20, ACT2, T_SLASH1, T_SLASH2, T_THROW, T_SEAL, T_EYES, T_SPLIT, T_POINT)
    log("holds linear ->", set_interpolation(PTS, sorted({F(t) for t in HOLD_STARTS}), "LINEAR"))
    _boxes = BOX["l"] + BOX["r"]
    log("box interp ->", set_interpolation(_boxes, sorted({F(t) for t in (T_SEAL - 0.3, T_SEAL, T_POINT - 0.15, T_POINT, T_JUMP0 - 0.15, T_JUMP0)}), "BEZIER"))
    log("box holds linear ->", set_interpolation(_boxes, sorted({0, F(5.35), F(6.50), F(T_SEAL), F(T_POINT), F(T_JUMP0)}), "LINEAR"))
    log("visible range ->", set_visible_range(0, F(T_TOTAL)))
    cam(CAM.tolist(), TARGET.tolist()); log("vis", hide_controllers("View"))
    import time as _t
    _p = os.path.join(OUT_DIR, "shot12_full_%s.casc" % _t.strftime("%H%M%S")); app.current_scene().save(_p); log("saved full casc", _p)
