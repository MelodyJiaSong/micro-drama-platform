# -*- coding: utf-8 -*-
"""把 `gate_scene.blend` 按 S01 的路径渲成一条彩色 MP4。

与 `previz_sk2.py` 的分工
------------------------
`previz_sk2.py` 出的是**白模动画**（Workbench 灰模），给生成模型当运动与几何参考，
44 条一批、快而糙。本文件出的是**一条彩色成片预览**：让人眼判断
「这个入城段到底像不像暴风城」，所以走 EEVEE、带材质与光。

路径与 `previz_sk2.py` 的 `PATHS["S01"]` 同源（都是 0–9s 引道 / 9–16s 穿门 / 16–25s 英雄谷），
但**这里是 1:1 米，不乘 CITY_SCALE**——gate_scene 本来就是实尺。

用法：
    blender -b <gate_scene.blend> --python tools/render_gate_flythrough.py -- \\
        --out <绝对路径>.mp4 [--fps 24] [--res 1280] [--samples 32]
"""
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import bpy

# (t 秒, 相机 xyz, 看向 xyz)。米，原点＝门洞正中，+Y 进城。
# 三段与 shot01.md 的 `动作:` 逐拍对齐（rule 4h ②）
# (t 秒, 相机 xyz, 看向 xyz)。米，原点＝城门正中，+Y 进城。
# 三段与 shot01.md 的 `动作:` 逐拍对齐（rule 4h ②）：
#   0–9s 城外土路低飞、城墙自地平线升起 / 9–16s 穿过城门（门上方是敞的，不是隧道）
#   16–25s 进入英雄谷，五尊巨像依次从两侧掠过，尽头是屏墙与大阶梯
PATH = [
    (0.0,  (0.0, -175.0, 14.0), (0.0, -110.0, 11.0)),  # 城外土路南端，树冠高度
    (9.0,  (0.0,  -38.0, 11.0), (0.0,   14.0, 11.0)),  # 逼近城门，与门扇同高
    (13.0, (0.0,    0.0,  8.0), (0.0,   58.0,  9.0)),  # 正在门洞平面
    (16.0, (0.0,   22.0,  8.0), (0.0,   96.0, 10.0)),  # 刚进谷
    (25.0, (0.0,  127.0, 11.0), (0.0,  178.0, 14.0)),  # 穿到五像之间，望向屏墙与大屋
]
DUR = 25.0


def argv():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    d = {}
    for i, x in enumerate(a):
        if x.startswith("--") and i + 1 < len(a):
            d[x[2:]] = a[i + 1]
    return d


def main():
    A = argv()
    out = Path(A["out"])
    fps = int(A.get("fps", 24))
    res = int(A.get("res", 1280))
    samples = int(A.get("samples", 32))

    sc = bpy.context.scene
    sc.render.fps = fps
    sc.frame_start = 1
    sc.frame_end = int(round(DUR * fps))
    # 宽高都要偶数：libx264 的 yuv420p 不吃奇数边
    rx = res - res % 2
    ry = int(res * 9 / 16)
    ry -= ry % 2
    sc.render.resolution_x, sc.render.resolution_y = rx, ry
    if hasattr(sc.eevee, "taa_render_samples"):
        sc.eevee.taa_render_samples = samples

    cam_d = bpy.data.cameras.new("fly")
    cam_d.lens = 24.0                 # 航拍低空前飞，广角
    cam_d.clip_start, cam_d.clip_end = 0.1, 4000.0
    cam = bpy.data.objects.new("fly", cam_d)
    sc.collection.objects.link(cam)
    sc.camera = cam

    tgt = bpy.data.objects.new("fly_t", None)
    sc.collection.objects.link(tgt)
    t = cam.constraints.new("TRACK_TO")
    t.target = tgt
    t.track_axis, t.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"

    # Blender 5.1 的 Action 改成了分层结构，`action.fcurves` 已不存在。
    # 与其去翻 layers/strips/channelbag，不如**在插帧之前**把默认插值设成线性——
    # 匀速穿越要的就是线性，Bezier 会在关键帧处加减速、把「匀速前飞」变成一顿一顿。
    try:
        bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"
    except Exception:
        pass

    for tsec, loc, look in PATH:
        f = max(1, int(round(tsec * fps)))
        cam.location = loc
        cam.keyframe_insert("location", frame=f)
        tgt.location = look
        tgt.keyframe_insert("location", frame=f)

    tmp = Path(tempfile.mkdtemp(prefix="gatefly_"))
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    sc.render.filepath = str(tmp / "f_")
    bpy.ops.render.render(animation=True)

    ff = shutil.which("ffmpeg") or "ffmpeg"
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [ff, "-y", "-loglevel", "error", "-framerate", str(fps),
           "-start_number", "1", "-i", str(tmp / "f_%04d.png"),
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", str(out)]
    subprocess.run(cmd, check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"[fly] {out}  {sc.frame_end} 帧 @{fps}fps  {rx}x{ry}")


main()
