# -*- coding: utf-8 -*-
"""S01–S07 的 previz：**在彩色的 `gate_scene.blend` 上手排机位**，不走通用机位。

为什么入城段这七镜单独走这条路
------------------------
① 这七镜全在入城段，而入城段有一份**查证过形制的高精彩色模型**
   （`gate_scene.blend`，形制出处 `_gate_research/gate_spec.md`）；
   全城 blockout 的城门段是照着猜搭的，已被证明与真实形制差五处。
② `previz_sk2.py` 的通用机位在密城里会**把相机抬到屋顶**
   （`base = 街心 - SAFE_BACK(12 m)`，而街半宽只有 3–6 m，退 12 m 必进旁边的房子，
   `find_clear_cam()` 随即升空兜底）——那条链路要单独修，不该拖住前三镜。
③ 这七镜是开场，值得手排（rule 4h ③：S 档 hero 长镜可写 per-shot 机位）。

与 shot md 的对齐
-----------------
每条的关键帧 `t` 与 `shotNN.md` 的 `动作:` 时间轴逐拍对齐（rule 4h ②）。
改时长或改动作，两边必须同步改。

用法：
    blender -b <gate_scene.blend> --python tools/previz_gate_sk2.py -- \\
        --out <目录> [--only S01,S03] [--fps 24] [--res 1280] [--samples 24]
"""
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import bpy

HUMAN_H = 1.75

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # blender 起的脚本不带仓库根
from tools.previz.sk2_gate_paths import SHOTS  # noqa: E402  机位表见该模块（rule 4i ①：只有一处定义）

# S03 的马与骑手：桥中段右侧，马头朝画面左（朝 -X）。previz 只要体量与站位。
HORSE = dict(loc=(3.4, 74.0), yaw=math.pi)

# 人物走位：shot_id -> [(t, x, y, 朝向弧度)]。+Y 为北，朝向 0＝面朝北、π＝面朝南。
ELLA_PATHS = {
    # S03 桥中段：她从画左进、马前三步停住、敬礼、再继续往北
    "S03": [(0.0, -4.5, 70.0, 0.0), (5.0, -1.2, 74.0, math.pi / 2),
            (14.0, -1.2, 74.0, math.pi / 2), (17.0, -1.2, 79.0, 0.0)],
    # S04 桥头对镜：站定 17 s 说逛单，最后转身向北
    "S04": [(0.0, 1.5, 113.5, math.pi), (17.0, 1.5, 113.5, math.pi),
            (21.0, 1.5, 116.0, 0.0)],
    # S05–S07 巨像段：**起点必须接上 S04 把她留下的位置（y=116）**，
    # 否则一开机她就倒退 9 m。走得慢（约 0.4 m/s）是因为五尊巨像全挤在北端 30 m 内
    # （gate_spec §4），而这三段共 64 s——边走边讲的主持人本来就是这个速度。
    "S05": [(0.0, 0.0, 116.0, 0.0), (19.0, 0.0, 124.0, 0.0)],
    "S06": [(0.0, 0.0, 124.0, 0.0), (19.0, 0.0, 130.0, 0.0)],
    "S07": [(0.0, 0.0, 130.0, 0.0), (20.0, -6.5, 135.0, 0.0),
            (26.0, -6.5, 135.0, -math.pi / 2)],   # 停在北侧左像基座前，侧身面向铭牌
}


def argv():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    return {x[2:]: a[i + 1] for i, x in enumerate(a) if x.startswith("--") and i + 1 < len(a)}


def make_ella():
    """1.75 m 的人形替身。previz 只需要**尺度、站位、朝向**三件事，不需要长相。"""
    parts = []
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.19, depth=0.85,
                                        location=(0, 0, 0.45))
    parts.append(bpy.context.object)                      # 腿
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1.16))
    o = bpy.context.object
    o.scale = (0.42, 0.24, 0.62)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    parts.append(o)                                       # 躯干
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.115, location=(0, 0, 1.60))
    parts.append(bpy.context.object)                      # 头
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.10, depth=0.26,
                                    location=(0, 0.20, 1.30))
    parts.append(bpy.context.object)                      # 朝向标（鼻尖，指 +Y）

    root = bpy.data.objects.new("ELLA", None)
    bpy.context.scene.collection.objects.link(root)
    m = bpy.data.materials.new("ella_proxy")
    m.use_nodes = True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.75, 0.22, 0.12, 1)
    for p in parts:
        p.parent = root
        p.data.materials.append(m)
    return root


def shot_sf():
    """从 `gen_shots_sk2.py` 读回每镜的 `subj_frac`，用来给本文件的手排机位对账。

    镜表是唯一真相（rule 4h ②）：手排的机位也必须回到同一把尺上量，
    否则「手排」就成了「随手排」。
    """
    import importlib.util
    import sys as _s
    p = Path(__file__).resolve().parent / "gen_shots_sk2.py"
    spec = importlib.util.spec_from_file_location("g_sf", str(p))
    m = importlib.util.module_from_spec(spec)
    keep, _s.argv = _s.argv, [_s.argv[0]]
    try:
        spec.loader.exec_module(m)
    finally:
        _s.argv = keep
    return {s["id"]: s["sf"] for s in m.SHOTS}


def make_horse():
    """马 + 骑手的体量替身。previz 只要**占多大地方、朝哪**，不要长相。"""
    parts = []
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1.35))
    o = bpy.context.object
    o.scale = (0.75, 2.30, 0.95)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    parts.append(o)                                       # 马身
    for sx in (-0.28, 0.28):
        for sy in (-0.85, 0.85):
            bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.10, depth=0.90,
                                                location=(sx, sy, 0.45))
            parts.append(bpy.context.object)              # 四条腿
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 1.35, 1.95))
    o = bpy.context.object
    o.scale = (0.34, 0.95, 0.45)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    parts.append(o)                                       # 马头颈（+Y 为马头朝向）
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.15, 2.45))
    o = bpy.context.object
    o.scale = (0.40, 0.26, 0.80)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    parts.append(o)                                       # 骑手躯干
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.115, location=(0, -0.15, 3.00))
    parts.append(bpy.context.object)                      # 骑手头

    root = bpy.data.objects.new("HORSE", None)
    bpy.context.scene.collection.objects.link(root)
    m = bpy.data.materials.new("horse_proxy")
    m.use_nodes = True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.20, 0.28, 0.62, 1)
    for p in parts:
        p.parent = root
        p.data.materials.append(m)
    root.location = (HORSE["loc"][0], HORSE["loc"][1], 0.0)
    root.rotation_euler = (0, 0, HORSE["yaw"])
    return root


def set_path(cam, tgt, keys, fps):
    for tsec, loc, look in keys:
        f = max(1, int(round(tsec * fps)))
        cam.location = loc
        cam.keyframe_insert("location", frame=f)
        tgt.location = look
        tgt.keyframe_insert("location", frame=f)


def render(shot, out_dir, fps, res, samples):
    dur, lens, keys = SHOTS[shot]
    sc = bpy.context.scene
    sc.render.fps = fps
    sc.frame_start, sc.frame_end = 1, int(round(dur * fps))
    rx = res - res % 2
    ry = int(res * 9 / 16)
    ry -= ry % 2
    sc.render.resolution_x, sc.render.resolution_y = rx, ry
    if hasattr(sc.eevee, "taa_render_samples"):
        sc.eevee.taa_render_samples = samples

    # Blender 5.1 的 Action 是分层结构、没有顶层 fcurves；插帧前设默认插值最省事。
    # 匀速穿越要线性，Bezier 会在关键帧处加减速。
    try:
        bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"
    except Exception:
        pass

    cam_d = bpy.data.cameras.new(f"cam_{shot}")
    cam_d.lens, cam_d.clip_start, cam_d.clip_end = lens, 0.1, 6000.0
    cam = bpy.data.objects.new(f"cam_{shot}", cam_d)
    sc.collection.objects.link(cam)
    sc.camera = cam
    tgt = bpy.data.objects.new(f"tgt_{shot}", None)
    sc.collection.objects.link(tgt)
    t = cam.constraints.new("TRACK_TO")
    t.target = tgt
    t.track_axis, t.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
    set_path(cam, tgt, keys, fps)

    horse = None
    if shot == "S03":
        horse = make_horse()

    ella = None
    if shot in ELLA_PATHS:
        ella = make_ella()
        for tsec, x, y, yaw in ELLA_PATHS[shot]:
            f = max(1, int(round(tsec * fps)))
            ella.location = (x, y, 0.0)
            ella.rotation_euler = (0, 0, yaw)
            ella.keyframe_insert("location", frame=f)
            ella.keyframe_insert("rotation_euler", frame=f)
        # **起落幅各算一次人占画高，和镜表逐个对账**（rule「景别档」/ rule 4h ②）。
        # 先前这里写死了 S03 的坐标与 0.19，换别的镜就是在报一个与本镜无关的数——
        # 一个永远「对得上」的对账等于没有对账。
        spec = shot_sf().get(shot)
        path = ELLA_PATHS[shot]
        # **传感器高度要问相机要，不能写死 24**：Blender 默认 sensor_width=36、
        # sensor_fit=AUTO，16:9 下竖向只有 36×9/16 ＝ 20.25 mm。写死 24 会让
        # 每个报出来的数都偏大 18%——一把自己就不准的尺，量什么都是错的。
        sensor_h = cam_d.sensor_width * ry / rx

        def frac_at(tsec):
            """t 时刻的人占画高：机位与人都按关键帧线性插值后再量。"""
            def lerp(seq, pick):
                if tsec <= seq[0][0]:
                    return pick(seq[0])
                for a, b in zip(seq, seq[1:]):
                    if tsec <= b[0]:
                        u = (tsec - a[0]) / max(1e-6, b[0] - a[0])
                        pa, pb = pick(a), pick(b)
                        return tuple(p + (q - p) * u for p, q in zip(pa, pb))
                return pick(seq[-1])
            c = lerp(keys, lambda k: k[1])
            p = lerp(path, lambda k: (k[1], k[2]))
            return HUMAN_H * lens / (sensor_h * max(0.5, math.dist(c, (p[0], p[1], 0.9))))

        # **按整条时间轴取样，报区间**——不要只看首尾两帧。
        # S07 实测：她从 6 m 外走进来、停 9 s、再走到 14 m 外，首尾是 0.56 / 0.25，
        # 而镜表写的 0.38 正是她**站定那 9 秒**的值。只看首尾会把「人在走」误判成「机位不对」。
        vals = [frac_at(dur * i / 24.0) for i in range(25)]
        lo, hi = min(vals), max(vals)
        note = f"（镜表 {spec[0]:.2f} → {spec[1]:.2f}）" if spec else ""
        flag = ""
        if spec:
            # 镜表要的值只要在本镜实际出现过，机位就给得出来
            miss = [v for v in spec if not (lo * 0.9 <= v <= hi * 1.1)]
            flag = f"  ⚠ 镜表要的 {miss} 全程没出现过" if miss else ""
        print(f"[previz] {shot} 人占画高 {vals[0]:.2f} → {vals[-1]:.2f}"
              f"（全程 {lo:.2f}–{hi:.2f}）{note}{flag}")

    tmp = Path(tempfile.mkdtemp(prefix=f"pv{shot}_"))
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    sc.render.filepath = str(tmp / "f_")
    bpy.ops.render.render(animation=True)

    out = out_dir / f"{shot.lower()}_previz.mp4"
    ff = shutil.which("ffmpeg") or "ffmpeg"
    subprocess.run([ff, "-y", "-loglevel", "error", "-framerate", str(fps),
                    "-start_number", "1", "-i", str(tmp / "f_%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", str(out)],
                   check=True)
    shutil.rmtree(tmp, ignore_errors=True)

    # **同时装进该镜的目录**：shot md 里写的 previz 路径是
    # `5_6_分镜与prompt/shots/shotNN/shotNN_previz.mp4`，而通用机位
    # （`previz_sk2.py`）也往同一个文件写。不在这里覆盖过去，入城段就会一直挂着
    # 通用机位那版**错的** previz，而且看不出来——两个文件同名、只有内容不同。
    n = shot[1:]
    dst_dir = (Path(__file__).resolve().parent.parent / "ai_videos" / "shikong_lvxing"
               / "sk2" / "5_6_分镜与prompt" / "shots" / f"shot{n}")
    if dst_dir.is_dir():
        shutil.copyfile(out, dst_dir / f"shot{n}_previz.mp4")
        print(f"[previz] {shot} 已装入 shots/shot{n}/")
    print(f"[previz] {shot} -> {out}  {sc.frame_end} 帧 @{fps}fps  {rx}x{ry}")

    # 清理，免得下一镜带着上一镜的相机与替身
    dead = [cam, tgt]
    for grp in (ella, horse):
        if grp:
            dead += [grp] + list(grp.children)
    for o in dead:
        try:
            bpy.data.objects.remove(o, do_unlink=True)
        except Exception:
            pass


def main():
    A = argv()
    out_dir = Path(A["out"])
    out_dir.mkdir(parents=True, exist_ok=True)
    fps, res = int(A.get("fps", 24)), int(A.get("res", 1280))
    samples = int(A.get("samples", 24))
    keep = {x.strip().upper() for x in A.get("only", "").split(",") if x.strip()}
    for shot in ("S01", "S02", "S03", "S04", "S05", "S06", "S07"):
        if keep and shot not in keep:
            continue
        render(shot, out_dir, fps, res, samples)


main()
