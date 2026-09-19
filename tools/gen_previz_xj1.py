# -*- coding: utf-8 -*-
"""Render xj1's previz as ONE continuous camera curve, sliced per shot.

The episode is a 一镜到底 chain, so its previz must be one path cut into segments, not six
independently placed cameras (`_series/series_bible.md` § 一镜到底的机械契约 6) — that is the
only way each shot's first frame can actually meet the previous shot's last frame.

Geometry comes from 余杭客栈.blend and is never edited here: this script only adds a camera
and renders. Coordinates are read off `_blender/blender_build.md`; a keyframe that leaves the
building or clips a wall trips an assertion instead of rendering nonsense.

shot01 has no previz — its first 19s are the dream slope, which has no geometry (and per
rule 4g environments are never image-to-3D). Its second half reuses shot02's opening framing.

Run (repo root):
  blender -b --factory-startup --python tools/gen_previz_xj1.py
  blender -b --factory-startup --python tools/gen_previz_xj1.py -- --shots 5
  blender -b --factory-startup --python tools/gen_previz_xj1.py -- --stills   # 每镜首末帧 PNG，快
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import bpy
from mathutils import Vector

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
SCENE_DIR = REPO / "ai_videos" / "xianjian_yi" / "_series" / "scenes" / "余杭客栈" / "_blender"
BLEND = SCENE_DIR / "余杭客栈.blend"
SHOTS_DIR = REPO / "ai_videos" / "xianjian_yi" / "xj1" / "5_6_分镜与prompt" / "shots"

FPS = 12
RES = (640, 360)

# 建筑包络（blender_build.md §2/§3），相机不得越出
X_MIN, X_MAX = -0.30, 10.80
Y_MIN, Y_MAX = -0.60, 11.90
Z_MIN, Z_MAX = 0.30, 6.20


@dataclass(frozen=True)
class Key:
    t: float                                  # 该镜内的秒数
    loc: tuple[float, float, float]
    aim: tuple[float, float, float]
    lens: float = 35.0


@dataclass(frozen=True)
class ShotPath:
    n: int
    secs: int
    keys: tuple[Key, ...]


# 一条连续路径：逍遥房(东)→房门→二层回廊(向西)→楼梯→大堂。
# 每镜的首关键帧 = 上一镜的末关键帧，逐值相等——接缝就是这么成立的。
PATHS: tuple[ShotPath, ...] = (
    ShotPath(2, 28, (
        Key(0,  (9.90, 10.20, 5.05), (8.90, 11.30, 4.45), 35),
        Key(14, (9.30,  9.85, 5.20), (8.90, 11.20, 4.55), 35),
        Key(28, (8.85,  9.55, 5.30), (9.00, 11.10, 4.65), 35),
    )),
    ShotPath(3, 30, (
        Key(0,  (8.85, 9.55, 5.30), (9.00, 11.10, 4.65), 35),
        Key(22, (8.85, 9.95, 5.30), (9.05, 11.05, 4.80), 35),
        Key(30, (8.85, 9.90, 5.30), (9.05, 11.05, 4.80), 35),
    )),
    ShotPath(4, 30, (
        Key(0,  (8.85, 9.90, 5.30), (9.05, 11.05, 4.80), 35),
        Key(12, (8.85, 9.70, 5.30), (8.60, 11.00, 4.70), 35),
        Key(20, (8.85, 9.60, 5.00), (9.60, 11.40, 4.10), 35),
        Key(30, (8.85, 9.50, 5.35), (8.85, 10.60, 4.90), 35),
    )),
    ShotPath(5, 28, (
        Key(0,  (8.85, 9.50, 5.35), (8.85, 10.60, 4.90), 35),
        Key(4,  (8.85, 8.60, 5.35), (8.20,  8.25, 5.00), 35),
        Key(12, (6.20, 8.30, 5.35), (3.60,  8.25, 5.00), 35),
        Key(16, (4.60, 8.30, 5.35), (4.20,  6.60, 4.30), 35),
        Key(20, (2.40, 8.30, 5.35), (0.90,  8.00, 4.90), 35),
        Key(25, (0.60, 6.10, 3.20), (0.60,  4.20, 1.80), 35),
        Key(28, (0.70, 3.60, 1.65), (3.40,  3.30, 1.60), 35),
    )),
    ShotPath(6, 26, (
        Key(0,  (0.70, 3.60, 1.65), (3.40, 3.30, 1.60), 35),
        Key(26, (1.80, 3.45, 1.62), (4.60, 3.25, 1.45), 35),
    )),
    ShotPath(7, 30, (
        Key(0,  (1.80, 3.45, 1.62), (4.60, 3.25, 1.45), 35),
        Key(20, (3.10, 3.35, 1.55), (5.10, 3.20, 1.30), 42),
        Key(30, (3.90, 3.30, 1.45), (5.25, 3.15, 1.15), 50),
    )),
)


def check() -> None:
    for p in PATHS:
        assert p.keys[0].t == 0 and p.keys[-1].t == p.secs, f"shot{p.n:02d}: 关键帧未覆盖整镜"
        for k in p.keys:
            x, y, z = k.loc
            assert X_MIN <= x <= X_MAX and Y_MIN <= y <= Y_MAX and Z_MIN <= z <= Z_MAX, \
                f"shot{p.n:02d} t={k.t}: 机位 {k.loc} 越出建筑包络"
            assert k.loc != k.aim, f"shot{p.n:02d} t={k.t}: 机位与目标重合"
    for a, b in zip(PATHS, PATHS[1:]):
        assert a.keys[-1].loc == b.keys[0].loc and a.keys[-1].aim == b.keys[0].aim, (
            f"shot{a.n:02d}→shot{b.n:02d}: 接缝两端的机位/视点不相等——"
            f"承接链要求上一镜末帧与下一镜首帧逐值相同")
    print(f"相机曲线自检通过：{len(PATHS)} 段，接缝 {len(PATHS) - 1} 处逐值闭合")


def setup_scene() -> bpy.types.Object:
    bpy.ops.wm.open_mainfile(filepath=str(BLEND))
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.render.resolution_x, sc.render.resolution_y = RES
    sc.render.fps = FPS
    sh = sc.display.shading
    sh.light, sh.color_type, sh.show_cavity = "STUDIO", "SINGLE", True
    cam = bpy.data.objects.new("PREVIZ_CAM", bpy.data.cameras.new("PREVIZ_CAM"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    roof = bpy.data.collections.get("20_屋面")
    if roof is not None:
        roof.hide_render = True          # 室内镜看不到瓦，隐掉省渲染时间
    return cam


def _fcurves(obj: bpy.types.Object) -> list[bpy.types.FCurve]:
    """Blender 5.x moved an Action's curves into layers/strips/channelbags; 4.x had
    `action.fcurves`. Walk whichever exists so the easing pass works on both."""
    ad = obj.animation_data
    if ad is None or ad.action is None:
        return []
    action = ad.action
    if hasattr(action, "fcurves"):
        return list(action.fcurves)
    out: list[bpy.types.FCurve] = []
    for layer in getattr(action, "layers", []):
        for strip in getattr(layer, "strips", []):
            for bag in getattr(strip, "channelbags", []):
                out.extend(bag.fcurves)
    return out


def bake(cam: bpy.types.Object, path: ShotPath) -> int:
    cam.animation_data_clear()
    cam.data.animation_data_clear()
    for k in path.keys:
        frame = int(round(k.t * FPS)) + 1
        cam.location = Vector(k.loc)
        cam.rotation_euler = (Vector(k.aim) - Vector(k.loc)).to_track_quat("-Z", "Y").to_euler()
        cam.data.lens = k.lens
        cam.keyframe_insert("location", frame=frame)
        cam.keyframe_insert("rotation_euler", frame=frame)
        cam.data.keyframe_insert("lens", frame=frame)
    for fc in _fcurves(cam):
        for kp in fc.keyframe_points:
            kp.interpolation = "BEZIER"
            kp.easing = "EASE_IN_OUT"
    return int(round(path.secs * FPS)) + 1


def main() -> int:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots", type=int, nargs="*", default=None)
    ap.add_argument("--stills", action="store_true", help="只出每镜首末帧 PNG（秒级，用于查接缝）")
    args = ap.parse_args(argv)

    check()
    paths = [p for p in PATHS if not args.shots or p.n in args.shots]
    cam = setup_scene()
    sc = bpy.context.scene

    for p in paths:
        last = bake(cam, p)
        out = SHOTS_DIR / f"shot{p.n:02d}" / "previz"
        out.mkdir(parents=True, exist_ok=True)
        if args.stills:
            for tag, frame in (("first", 1), ("last", last)):
                sc.frame_set(frame)
                sc.render.filepath = str(out / f"shot{p.n:02d}_previz_{tag}.png")
                bpy.ops.render.render(write_still=True)
            print(f"  shot{p.n:02d} 首末帧 → {out.name}/", flush=True)
            continue
        # PNG 序列 → ffmpeg 合片。不用 Blender 的 FFMPEG 输出：5.x 把 'FFMPEG' 从
        # image_settings.file_format 枚举里移走了，各版本写法不一；而 previz/frames/ 本就是
        # 仓库约定的可重算目录（gitignore + assets_sync 跳过），走序列更稳也更好查单帧。
        frames = out / "frames"
        frames.mkdir(parents=True, exist_ok=True)
        sc.frame_start, sc.frame_end = 1, last
        sc.render.image_settings.file_format = "PNG"
        sc.render.filepath = str(frames / "f")
        bpy.ops.render.render(animation=True)
        mp4 = out / f"shot{p.n:02d}_previz.mp4"
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y",
                        "-framerate", str(FPS), "-start_number", "1",
                        "-i", str(frames / "f%04d.png"),
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", str(mp4)],
                       check=True)
        print(f"  shot{p.n:02d} {p.secs}s / {last} 帧 → previz/{mp4.name}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
