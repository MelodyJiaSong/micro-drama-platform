# shot12 第一幕（0–15 s）身体动作 —— Cascadeur 版，接在落地脚本（第 1 段）之后。
# 时刻全部来自 previz/shot12_previz.py 的 _SEGS 时长链（config 默认值），30fps 取整。
# 分段投递（每次调用要短，脚本服务器 30s 超时、长脚本还曾把 Cascadeur 跑崩）：
#   STAGE "hands"  解右手剑指/握姿并打全部手型键        STAGE "body1" 饮酒/晃身/抛壶
#   STAGE "body2"  掐诀 + 三跺 + 保持                    STAGE "body3" 剑指弓步 / 收势
#   STAGE "finish" 插值 Bezier + 相机 + 存盘
# 需要外部注入：LIB、JZ_L、FALL_SCRIPT、OUT_DIR（ASCII 临时目录）、STAGE。
NO_SAVE = True; DEFS_ONLY = True
STAGE = globals().get("STAGE", "hands")
try:
    exec(open(FALL_SCRIPT, encoding="utf-8").read())        # 只取定义：BASE/hand/foot/Ry/Rz/Rx/pose_ground/key_pose/CAM…
except SystemExit:
    pass
LOG = OUT_DIR + r"\build.log"


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{STAGE}] {s}\n")


F = lambda t: int(round(t * FPS))
T_END = 15.0
BOX = {s: [n for n in IDS if n.startswith("f_") and n.endswith("_Box_" + s)] for s in ("l", "r")}
HAND_JSON = OUT_DIR + r"\hands_lr_cascy.json"
HAND_KEY_FRAMES = sorted({0, F(4.45), F(4.60), F(2.70), F(3.17), F(4.85), F(5.35), F(14.00), F(14.50), F(14.90), F(15.0)})

# ---------- 手型 ----------
NATURAL_HANDS = globals().get("NATURAL_HANDS", True)           # 用户 2026-09-05：手指全部不动、保持自然
if STAGE == "hands" and NATURAL_HANDS:
    log("anim size ->", set_anim_size(F(T_END) + 1)); log("hands natural: no finger keys")
elNATURAL_HANDS = globals().get("NATURAL_HANDS", True)           # 手指不做动作，保持自然
if STAGE == "hands" and NATURAL_HANDS:
    log("anim size ->", set_anim_size(F(T_END) + 1)); log("hands natural: no finger keys")
elif STAGE == "hands":
    log("anim size ->", set_anim_size(F(T_END) + 1))
    RELAX = {s: {n: q_to_rot(q) for n, q in tbl.items()} for s, tbl in json.load(open(OUT_DIR + r"\relax_lr.json")).items()}
    JZ = {"l": {n: q_to_rot(q) for n, q in json.load(open(JZ_L)).items()}}

    def build_jianzhi(side):
        d = {}
        for fg in ("index", "middle"):
            for seg in (1, 2, 3):
                b = bend_deg(side, fg, seg, 0); d[f"f_{fg}{seg}_Box_{side}"] = rot_axis(-(b if seg > 1 else b * 0.85), "z")
        for fg, extra in (("ring", (60, 90, 60)), ("pinky", (65, 90, 65))):
            for seg, e in zip((1, 2, 3), extra): d[f"f_{fg}{seg}_Box_{side}"] = rot_axis(e, "z")
        d[f"f_thumb1_Box_{side}"] = rot_mul(rot_axis(20, "x"), rot_axis(15, "z")); d[f"f_thumb2_Box_{side}"] = rot_axis(40, "z"); d[f"f_thumb3_Box_{side}"] = rot_axis(40, "z")
        return d

    set_box_rots(RELAX["r"], 0, "right relax", key=False)       # 右手先回到 Cascy 原始松弛手，再解剑指
    add_box_rots(build_jianzhi("r"), 0, "右手剑指 solve", key=False)
    JZ["r"] = read_box_rot(BOX["r"], 0)
    log("right 剑指 bends", [round(bend_deg("r", "index", s, 0), 1) for s in (1, 2, 3)], "spread", round(spread_deg("r", "index", "middle", 0), 1))
    GRIP = {}
    for s in ("l", "r"):
        base = RELAX[s]; g = {}
        for fg in ("index", "middle", "ring", "pinky"):
            for seg, e in zip((1, 2, 3), (45, 70, 40)): g[f"f_{fg}{seg}_Box_{s}"] = rot_mul(base[f"f_{fg}{seg}_Box_{s}"], rot_axis(e, "z"))
        g[f"f_thumb1_Box_{s}"] = rot_mul(base[f"f_thumb1_Box_{s}"], rot_axis(20, "x")); g[f"f_thumb2_Box_{s}"] = rot_mul(base[f"f_thumb2_Box_{s}"], rot_axis(30, "z")); g[f"f_thumb3_Box_{s}"] = rot_mul(base[f"f_thumb3_Box_{s}"], rot_axis(30, "z"))
        GRIP[s] = g
    json.dump({k: {s: {n: rot_to_q(r) for n, r in t[s].items()} for s in t} for k, t in (("JZ", JZ), ("GRIP", GRIP), ("RELAX", RELAX))}, open(HAND_JSON, "w"))
    HAND_KEYS = [
        (0, "r", GRIP), (F(4.45), "r", GRIP), (F(4.60), "r", RELAX),        # 右手一路拎葫芦，脱手后松开
        (0, "l", JZ), (F(2.70), "l", JZ), (F(3.17), "l", RELAX),            # 左手空中竖两指，落地饮酒时放松
        (F(4.85), "l", RELAX), (F(4.85), "r", RELAX),
        (F(5.35), "l", JZ), (F(5.35), "r", JZ),                             # 掐诀：两手剑指
        (F(14.00), "l", JZ), (F(14.00), "r", JZ),
        (F(14.50), "r", GRIP), (F(14.90), "l", RELAX), (F(15.0), "l", RELAX), (F(15.0), "r", GRIP),
    ]
    for fr, s, table in HAND_KEYS:
        set_box_rots(table[s], fr, f"hand {s} f{fr}")
    log("hand keys done", len(HAND_KEYS))

# ---------- 身体姿态（局部系）----------
STAND = pose_ground(GROUND_Y, 30, 6, 6)
LEG_KEYS = ("thigh_MainPoint", "calf_MainPoint", "calf_AdditionalPoint", "calf_LimbDir", "foot_MainPoint", "foot_Self0Point",
            "toe_MainPoint", "toe_AdditionalPoint", "toe_DirectionPoint")


def copy_pose(p): return {n: v.copy() for n, v in p.items()}


def upper_roll(p, deg):                      # 晃身：上半身绕骨盆 Z 轴侧倾
    R = Rz(deg)
    for n in p:
        if not any(n.startswith(k) for k in LEG_KEYS) and not n.startswith("pelvis"):
            p[n] = R @ p[n]


def head_tilt(p, deg):                       # 头绕颈点 X 轴：负＝仰头
    R = Rx(deg); c = p["neck_MainPoint"]
    for n in ("head_MainPoint", "head_AdditionalPoint", "head_DirectionPoint"):
        p[n] = c + R @ (p[n] - c)


def pose_drink():
    p = copy_pose(STAND)
    hand_straight(p, "r", (-7, 64, 13), (-62, 34, 2.0))   # 葫芦口抵唇：腕到嘴前，肘向体侧张开，腕不弯
    head_tilt(p, -32)                                                                           # 仰头灌酒
    return p


def pose_windup():
    p = copy_pose(STAND); hand_straight(p, "r", (-32, 24, -26), (-58, 30, -30.0)); return p


def pose_release():
    p = copy_pose(STAND); hand_straight(p, "r", (24, 42, 24), (-18, 16, 34.0)); return p   # 甩向画右：右臂横扫过身前、胸高


def pose_seal(foot_up=False):
    p = copy_pose(STAND)
    hand_straight(p, "r", (-2, 35, 25), (-44, 12, 4.0))      # 右手收到胸前
    hand_straight(p, "l", (3, 50, 27), (44, 30, 4.0))        # 左手在其上方
    if foot_up:
        foot(p, "r", BASE["foot_MainPoint_r"] + np.array([0, 22, 6.0]), Rx(-25)); p["calf_LimbDir_r"] = BASE["calf_LimbDir_r"] + np.array([0, 8, 25.0])
    return p


def pose_finger():                            # 两手剑指 + 右脚前迈弓步（骨盆世界坐标另给：下沉 11、前压 14）
    p = copy_pose(STAND)
    pel = np.array([0, GROUND_Y - 11, 14.0])
    foot(p, "r", np.array([-20, 9.3, 55.0]) - pel); foot(p, "l", np.array([20, 9.3, -8.0]) - pel)
    p["calf_LimbDir_r"] = np.array([-22, -30, 95.0]); p["calf_LimbDir_l"] = np.array([22, -40, 45.0])
    hand_straight(p, "r", (-17, 47, 47), (-42, 22, 18.0))   # 右臂平直前指
    hand_straight(p, "l", (-6, 40, 24), (52, 30, 8.0))       # 左臂横抱胸前
    return p, pel


def pose_end():
    p = copy_pose(STAND); hand_straight(p, "r", (-26, 8, 12), BASE["forearm_LimbDir_r"]); return p


def K(t, local, pelvis=None, title=""):
    ok = key_pose(F(t), local, P_LAND if pelvis is None else np.array(pelvis, float), 0.0, title or f"t{t}")
    log(f"key {title or t} f{F(t)} ->", ok)
    return ok


KEY_T = [2.32, 2.70, 3.35, 3.50, 3.80, 4.15, 4.30, 4.45, 5.00, 5.35, 5.45, 5.56, 5.73, 5.84, 6.01, 6.12, 6.20, 9.50, 10.20, 10.80, 13.90, 14.90, 15.00]

if STAGE == "body1":
    K(2.70, pose_drink(), title="drink in"); K(3.35, pose_drink(), title="drink hold")
    s = copy_pose(STAND); upper_roll(s, 4.5); K(3.50, s, title="sway A")
    s = copy_pose(STAND); upper_roll(s, -3.0); K(3.80, s, title="sway B")
    K(4.15, STAND, title="steady")
    K(4.30, pose_windup(), title="windup"); K(4.45, pose_release(), title="release"); K(5.00, STAND, title="arm back")
elif STAGE == "body2":
    K(5.35, pose_seal(), title="seal")
    for t0 in (5.32, 5.60, 5.88):                              # 右脚快跺三下：起→抬(+0.13)→落(+0.24)
        K(t0 + 0.13, pose_seal(foot_up=True), title=f"stomp up {t0}"); K(t0 + 0.24, pose_seal(), title=f"stomp down {t0}")
    K(6.20, pose_seal(), title="seal end"); K(9.50, pose_seal(), title="seal hold"); K(10.20, pose_seal(), title="legs neutral hold")
elif STAGE == "body3":
    fp, pel = pose_finger(); K(10.80, fp, pel, "finger lunge"); K(13.90, fp, pel, "finger hold")
    K(14.90, pose_end(), title="end"); K(15.00, pose_end(), title="end hold")
elif STAGE == "gourd":                           # 酒葫芦（用户 2026-09-05）：两颗球，随右手走，4.45s 抛向画右落地
    import common.mesh as c_mh
    def all_ids(): return {_MV.get_object_name(i): i for i in _MV.get_objects()}
    cur = all_ids()
    def find(prefix):                                          # Cascadeur 会给新物件名加 "(0)" 后缀
        return next((n for n in cur if n == prefix or n.startswith(prefix + "(")), None)
    have = [n for n in ("Gourd_body", "Gourd_neck") if find(n)]
    if len(have) < 2:
        before = set(cur.values())
        for _ in range(2 - len(have)):
            c_mh.add_object_with_mesh(scene, "objects/sphere.partscasc", "Gourd")
        cur = all_ids(); new_ids = [i for i in cur.values() if i not in before]
        log("created sphere objects:", [n for n, i in cur.items() if i in new_ids])
        want = [n for n in ("Gourd_body", "Gourd_neck") if n not in have]
        def mod_rename(model, update, sc):
            for oid, nm in zip(new_ids, want):
                model.set_object_name(oid, nm)
        scene.modify_update("name gourd", mod_rename)
    cur = all_ids(); IDS.update(cur)
    GB, GN = cur[find("Gourd_body")], cur[find("Gourd_neck")]
    R_BODY, R_NECK = 7.0, 4.5
    SPHERE_R0 = 60.0                                            # sphere.partscasc 基础半径 60 cm（实测）
    def node_of(update, oid, names):
        g = update.get_object_by_id(oid).root_group()
        for n in names:
            nd = g.node_deep(n)
            if nd is not None:
                return nd
        raise KeyError(names)
    def mod_scale(model, update, sc):
        g = update.get_object_by_id(GB).root_group(); log("gourd nodes:", [x.name() for x in g.nodes()][:40])
        for oid, r in ((GB, R_BODY), (GN, R_NECK)):
            try:
                s = r / SPHERE_R0; nd = node_of(update, oid, ("Local Scale", "Scale")); nd.set_value(np.array([s, s, s], dtype="float32")); log("scale set", r, "cm ->", round(s, 4))
            except Exception as e:
                log("scale err", str(e)[:80])
    scene.modify_update("gourd scale", mod_scale)
    F_REL = F(4.45)
    def hang(f):                                              # 拎着：挂在手下方；饮酒时翻到嘴前
        h = np.array(gpos("hand_MainPoint_r", f))
        if F(2.70) <= f <= F(3.35):
            return h + np.array([-3, 6, 7.0]), h + np.array([-7, 9, -1.0])
        return h + np.array([0, -16, 0.0]), h + np.array([0, -6, 0.0])
    LAND = np.array([150.0, R_BODY, 25.0]); REST = np.array([168.0, R_BODY, 30.0])
    def mod_keys(model, update, sc):
        le = model.layers_editor(); lv = scene.layers_viewer()
        pb = node_of(update, GB, ("Local Position",)); pn = node_of(update, GN, ("Local Position",))   # 网格物件要驱动 Local Position；"Position" 是计算输出
        ids = {pb.data_id(), pn.data_id()}
        def key(f, b, n):
            pb.set_value(np.array(b, dtype="float32"), int(f)); pn.set_value(np.array(n, dtype="float32"), int(f))
            for oid in (GB, GN):
                le.set_fixed_interpolation_or_key_if_need(lv.layer_id_by_obj_id(oid), int(f), True)
        for f in range(0, F_REL + 1):
            b, n = hang(f); key(f, b, n)
        b0, _ = hang(F_REL)
        apex = (b0 + LAND) / 2 + np.array([0, 45, 0]); bounce = LAND + np.array([8, 14, 2])
        key(F(4.62), apex, apex + np.array([6, 8, 0])); key(F(4.85), LAND, LAND + np.array([9, 4, 0]))
        key(F(4.95), bounce, bounce + np.array([9, 3, 0])); key(F(5.10), REST, REST + np.array([10, 2, 0])); key(F(T_END), REST, REST + np.array([10, 2, 0]))
        sc.run_update(ids, 0)
    log("gourd keys ->", scene.modify_update("gourd keys", mod_keys))
    log("gourd interp ->", set_interpolation([find("Gourd_body"), find("Gourd_neck")], [F_REL, F(4.62), F(4.85), F(4.95), F(5.10)], "BEZIER"))
elif STAGE == "wrists":                          # 腕校直（用户 2026-09-05「中间手腕又弯了」）：按每帧实际前臂方向重摆手的朝向点，逐帧打死
    F_LAST = F(T_END)
    def mod(model, update, sc):
        le = model.layers_editor(); lv = scene.layers_viewer(); ids = set()
        nodes = {}
        for side in ("l", "r"):
            for n in (f"hand_DirectionPoint_{side}", f"hand_AdditionalPoint_{side}"):
                nodes[n] = update.get_object_by_id(IDS[n]).root_group().node_deep("Position"); ids.add(nodes[n].data_id())
        for side in ("l", "r"):
            E0 = BASE[f"forearm_MainPoint_{side}"]; W0 = BASE[f"hand_MainPoint_{side}"]; m = f"hand_MainPoint_{side}"
            for f in list(range(0, F_LAST + 1, 3)) + [F_LAST]:          # 每 3 帧一键：逐帧打键会让 Cascadeur 卡死（2026-09-05）
                E = np.array(gpos(f"forearm_MainPoint_{side}", f)); W = np.array(gpos(m, f))
                R = _rot_between(W0 - E0, W - E)
                for n in (f"hand_DirectionPoint_{side}", f"hand_AdditionalPoint_{side}"):
                    nodes[n].set_value((W + R @ (BASE[n] - BASE[m])).astype("float32"), f)
                    le.set_fixed_interpolation_or_key_if_need(lv.layer_id_by_obj_id(IDS[n]), f, True)
        sc.run_update(ids, 0)
    log("wrists ->", scene.modify_update("straight wrists", mod))
elif STAGE == "finish":
    log("interp points ->", set_interpolation(PTS, sorted({F(t) for t in KEY_T} | {F_LAND, F_DIP, F_UP}), "BEZIER"))
    log("interp boxes ->", set_interpolation(BOX["l"] + BOX["r"], HAND_KEY_FRAMES, "BEZIER"))
    log("visible range ->", set_visible_range(0, F(T_END)))            # 否则时间轴仍停在落地段的 0-90 帧，播放只有 3 秒
    cam(CAM.tolist(), TARGET.tolist()); log("vis", hide_controllers("View"))
    import time as _t
    _p = os.path.join(OUT_DIR, "shot12_act1_%s.casc" % _t.strftime("%H%M%S")); app.current_scene().save(_p); log("saved act1 casc", _p)   # 每次新文件名：同名文件若已在别的 tab 打开会存盘失败
