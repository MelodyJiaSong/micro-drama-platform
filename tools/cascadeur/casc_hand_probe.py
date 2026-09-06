# Probe which local axis of each finger box is the curl axis (run inside Cascadeur).
exec(open(LIB, encoding="utf-8").read())

SIDE = "r"
FINGERS = ["index", "middle", "ring", "pinky", "thumb"]
FRAME = 0
PROBE_DEG = 20.0


def seg_dir(a, b):
    v = np.array(gpos(b, FRAME)) - np.array(gpos(a, FRAME))
    return v / (np.linalg.norm(v) + 1e-9)


def bend(finger, seg):
    """angle (deg) between the segment before and after joint `seg` (1=MCP,2=PIP,3=DIP)."""
    chain = [f"hand_{SIDE}"] + [f"f_{finger}{k}_{SIDE}" for k in (1, 2, 3, 4)]
    v_in = seg_dir(chain[seg - 1], chain[seg])
    v_out = seg_dir(chain[seg], chain[seg + 1])
    return float(math.degrees(math.acos(np.clip(np.dot(v_in, v_out), -1, 1))))


def spread(finger_a, finger_b):
    """angle between the proximal segments of two fingers."""
    va = seg_dir(f"f_{finger_a}1_{SIDE}", f"f_{finger_a}2_{SIDE}")
    vb = seg_dir(f"f_{finger_b}1_{SIDE}", f"f_{finger_b}2_{SIDE}")
    return float(math.degrees(math.acos(np.clip(np.dot(va, vb), -1, 1))))


report = {}
for f in FINGERS:
    for seg in (1, 2, 3):
        box = f"f_{f}{seg}_Box_{SIDE}"
        base_bend = bend(f, seg)
        base_spread = spread(f, "middle") if f != "middle" else spread(f, "index")
        axes = {}
        for ax in ("x", "y", "z"):
            add_box_rots({box: rot_axis(PROBE_DEG, ax)}, FRAME, "probe", key=False)
            axes[ax] = {"d_bend": round(bend(f, seg) - base_bend, 1),
                        "d_spread": round((spread(f, "middle") if f != "middle" else spread(f, "index")) - base_spread, 1)}
            add_box_rots({box: rot_axis(-PROBE_DEG, ax)}, FRAME, "probe undo", key=False)
        report[box] = {"bend": round(base_bend, 1), "spread": round(base_spread, 1), "probe": axes}

# keys check
lv = scene.layers_viewer()
track = lv.layer_id_by_obj_id(IDS[f"f_index2_Box_{SIDE}"])
lay = lv.layer(track)
print("KEYFRAMES f_index2_Box_r:", [fr for fr in range(0, 101) if lay.is_key(fr)])
print("REPORT " + json.dumps(report))
