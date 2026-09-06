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

T_TOTAL = 27.40
# ---- 第二幕时刻（config 时长链，秒）----
T_WIND1, T_SLASH1, T_WIND2, T_SLASH2 = 15.25, 15.45, 15.90, 16.08
T_THROW_WIND, T_THROW, T_SWORD_HIGH, T_SEAL, T_EYES = 16.50, 16.65, 17.20, 17.50, 17.90
T_SPLIT, T_SPIN_END, T_RISE_END = 18.00, 21.40, 22.00
T_POINT, T_DROP0, T_DROP_DUR = 22.45, 22.60, 0.34
T_JUMP0, T_JUMP_TOP, T_JUMP1, T_GATHER1, T_MERGE = 24.28, 24.52, 24.76, 25.00, 25.02
T_BOUNCE = (25.10, 25.18, 25.26, 25.36)
T_FLIP0, T_FLIP1, T_LAND_DIP, T_LAND_UP = 25.42, 26.05, 26.12, 26.28
T_SWORD_UP, T_SWORD_APEX, T_SHEATH = 26.15, 26.28, 26.50
T_LAUGH, T_LAUGH_BOBS = 26.54, (26.70, 26.86, 27.02)
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


def pose_seal1():
    p = copy_pose(STAND); hand_straight(p, "r", (-4, 40, 22), (-45, 15, 5.0)); head_tilt(p, -22); return p


def pose_seal_still():
    p = copy_pose(STAND); hand_straight(p, "r", (-4, 40, 22), (-45, 15, 5.0)); head_tilt(p, -4); return p


def pose_point():                             # 亮相：右臂笔直斜指前下方，左手剑指收腰侧，右脚前踏半马步
    p = copy_pose(STAND); stance(p, GROUND_Y - 12, rz=40); hand_straight(p, "r", (-16, 22, 46), (-48, 25, 15.0)); hand_straight(p, "l", (24, 8, 6), BASE["forearm_LimbDir_l"]); upper_lean(p, 8); return p


def pose_spread():                            # 双臂平张、左腿抬起（右脚踩剑）
    p = copy_pose(STAND); hand_straight(p, "l", (66, 47, 0), (45, 15, -60.0)); hand_straight(p, "r", (-66, 47, 0), (-45, 15, -60.0)); raise_leg(p, "l"); return p


def pose_tuck():                              # 团身
    p = copy_pose(STAND)
    for side, sgn in (("l", 1), ("r", -1)):
        foot(p, side, np.array([sgn * 12, -38, 26.0]), Rx(-40)); p[f"calf_LimbDir_{side}"] = np.array([sgn * 20, -5, 95.0])
        hand_straight(p, side, (sgn * 22, 28, 30), (sgn * 50, 10, 20.0))
    head_tilt(p, 20); return p


def pose_land():                              # 落地屈膝、双臂外撑
    p = copy_pose(STAND); stance(p, GROUND_Y - 22, rz=10, lz=-10); hand_straight(p, "r", (-46, 22, 14), (-55, 15, -25.0)); hand_straight(p, "l", (46, 22, 14), (55, 15, -25.0)); upper_lean(p, 8); return p


def pose_laugh(bob=0.0):
    p = copy_pose(STAND); hand_straight(p, "r", (-36, 14, 10), BASE["forearm_LimbDir_r"]); hand_straight(p, "l", (36, 14, 10), BASE["forearm_LimbDir_l"])
    upper_lean(p, -8 + bob); head_tilt(p, -38 + bob * 1.5); return p


def lerp_pose(a, b, u):
    return {n: a[n] * (1 - u) + b[n] * u for n in a}


def KW(t, local, pelvis, yaw=0.0, title=""):
    ok = key_pose(F(t), local, np.array(pelvis, float), yaw, title or f"t{t}"); log(f"key {title or t} f{F(t)} ->", ok); return ok


PEL0 = P_LAND
if STAGE == "body2a":
    log("anim size ->", set_anim_size(F(T_TOTAL) + 1))
    KW(15.00, pose_end12(), PEL0, title="end12"); KW(T_WIND1 - 0.35, pose_end12(), PEL0, title="pre-wind1")
    KW(T_WIND1, pose_wind1(), PEL0, title="wind1"); KW(T_SLASH1, pose_slash1(), PEL0 - [0, 8, 0], title="slash1"); KW(T_WIND2 - 0.35, pose_slash1(), PEL0 - [0, 8, 0], title="slash1 hold")
    KW(T_WIND2, pose_wind2(), PEL0 - [0, 6, 0], title="wind2"); KW(T_SLASH2, pose_slash2(), PEL0 - [0, 6, 0], title="slash2"); KW(T_THROW_WIND - 0.25, pose_slash2(), PEL0 - [0, 6, 0], title="slash2 hold")
    KW(T_THROW_WIND, pose_throw_wind(), PEL0, title="throw wind"); KW(T_THROW, pose_throw(), PEL0, title="throw"); KW(T_SWORD_HIGH - 0.15, pose_throw(), PEL0, title="throw hold")
    KW(T_SEAL, pose_seal1(), PEL0, title="seal1"); KW(T_EYES, pose_seal_still(), PEL0, title="seal still"); KW(T_POINT - 0.5, pose_seal_still(), PEL0, title="seal hold")

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
    c, y, z = on_back(F(6.20)); K_(F(6.32), c + y * 55, y, z)               # 竖直拔出鞘
    K_(F(6.95), (0, 255, 73), (0, 1, 0)); K_(F(7.20), (0, 190, 178), (0, 1, 0))
    HOVER = np.array([0, 135, 210.0]); K_(F(8.10), HOVER, (0, 1, 0))
    for i, t in enumerate((8.30, 9.30, 10.30)): K_(F(t), HOVER + [0, 4.5 if i % 2 == 0 else -4.5, 0], (0, 1, 0))
    K_(F(11.0), HOVER, (0, 1, 0))
    fo0, fo1 = F(11.0), F(12.1)
    for fr in range(fo0, fo1 + 1, 2):                        # 绕身一圈：前 → 他的左 → 背后 → 他的右 → 前
        a = 2 * math.pi * (fr - fo0) / (fo1 - fo0); K_(fr, (210 * math.sin(a), 135, 210 * math.cos(a)), (0, 1, 0))
    K_(F(13.1), HOVER + [0, 4.5, 0], (0, 1, 0)); K_(F(14.0), HOVER, (0, 1, 0))
    fg0, fg1 = F(14.0), F(14.5)
    for fr in range(fg0 + 1, F(15.0) + 1):                    # 落回右手：剑竖直尖朝下、柄在手中，收势倾 26°
        u = min(1.0, (fr - fg0) / (fg1 - fg0)); tilt = 26.0 * u
        hand = np.array(gpos("hand_MainPoint_r", fr)); down = Rx(tilt) @ np.array([0, -1, 0.0])
        grip = hand + down * SWORD_HALF
        K_(fr, HOVER * (1 - u) + grip * u if fr <= fg1 else grip, -down)
    for fr in range(F(15.0), F(T_THROW) + 1):                 # 握剑斩击：剑沿前臂延伸，柄在手中
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
    F0, F1 = F(15.0), F(T_TOTAL)
    def mod(model, update, sc):
        le = model.layers_editor(); lv = scene.layers_viewer(); ids = set(); nodes = {}
        for side in ("l", "r"):
            for n in (f"hand_DirectionPoint_{side}", f"hand_AdditionalPoint_{side}"):
                nodes[n] = update.get_object_by_id(IDS[n]).root_group().node_deep("Position"); ids.add(nodes[n].data_id())
        for side in ("l", "r"):
            E0 = BASE[f"forearm_MainPoint_{side}"]; W0 = BASE[f"hand_MainPoint_{side}"]; m = f"hand_MainPoint_{side}"
            for f in list(range(F0, F1 + 1, 3)) + [F1]:
                E = np.array(gpos(f"forearm_MainPoint_{side}", f)); W = np.array(gpos(m, f)); R = _rot_between(W0 - E0, W - E)
                for n in (f"hand_DirectionPoint_{side}", f"hand_AdditionalPoint_{side}"):
                    nodes[n].set_value((W + R @ (BASE[n] - BASE[m])).astype("float32"), f)
                    le.set_fixed_interpolation_or_key_if_need(lv.layer_id_by_obj_id(IDS[n]), f, True)
        sc.run_update(ids, 0)
    log("wrists2 ->", scene.modify_update("straight wrists act2", mod))

elif STAGE == "finish":
    KT = [15.0, T_WIND1 - 0.35, T_WIND1, T_SLASH1, T_WIND2 - 0.35, T_WIND2, T_SLASH2, T_THROW_WIND - 0.25, T_THROW_WIND, T_THROW, T_SWORD_HIGH - 0.15,
          T_SEAL, T_EYES, T_POINT - 0.5, T_POINT, T_JUMP0 - 0.15, T_JUMP0, T_MERGE, *T_BOUNCE, T_FLIP0, T_LAND_DIP, T_LAND_UP, T_LAUGH, *T_LAUGH_BOBS, T_TOTAL]
    log("interp act2 ->", set_interpolation(PTS, sorted({F(t) for t in KT}), "BEZIER"))
    log("visible range ->", set_visible_range(0, F(T_TOTAL)))
    cam(CAM.tolist(), TARGET.tolist()); log("vis", hide_controllers("View"))
    import time as _t
    _p = os.path.join(OUT_DIR, "shot12_full_%s.casc" % _t.strftime("%H%M%S")); app.current_scene().save(_p); log("saved full casc", _p)
