# -*- coding: utf-8 -*-
"""Shared previz engine for the 仙剑奇侠传一 episodes.

An episode's previz is ONE continuous camera curve sliced per shot, never six
independently placed cameras (`_series/series_bible.md` § 一镜到底的机械契约 6) — that is
the only way each shot's first frame can meet the previous shot's last frame.

Per-episode data lives in `gen_previz_xjN.py`: the blend to open, the building envelope,
and the keyframes. Everything else is here, for the same reason the shot engine is shared.

Assertions run before any render: keyframes must cover the whole shot, the camera must stay
inside the building, and — the one that actually matters — **each seam's two ends must carry
an identical position and aim**, because a handoff that is merely close is not a handoff.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import bpy
from mathutils import Vector

REPO = Path(__file__).resolve().parent.parent
DRAMA = REPO / "ai_videos" / "xianjian_yi"

FPS = 12
RES = (640, 360)


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


@dataclass(frozen=True)
class Envelope:
    x: tuple[float, float]
    y: tuple[float, float]
    z: tuple[float, float]


def check(paths: tuple[ShotPath, ...], env: Envelope) -> None:
    for p in paths:
        assert p.keys[0].t == 0 and p.keys[-1].t == p.secs, f"shot{p.n:02d}: 关键帧未覆盖整镜"
        ts = [k.t for k in p.keys]
        assert ts == sorted(ts), f"shot{p.n:02d}: 关键帧时间未递增"
        for k in p.keys:
            x, y, z = k.loc
            assert env.x[0] <= x <= env.x[1] and env.y[0] <= y <= env.y[1] \
                and env.z[0] <= z <= env.z[1], f"shot{p.n:02d} t={k.t}: 机位 {k.loc} 越出建筑包络"
            assert k.loc != k.aim, f"shot{p.n:02d} t={k.t}: 机位与目标重合"
    for a, b in zip(paths, paths[1:]):
        assert a.keys[-1].loc == b.keys[0].loc and a.keys[-1].aim == b.keys[0].aim, (
            f"shot{a.n:02d}→shot{b.n:02d}: 接缝两端的机位/视点不相等——"
            f"承接链要求上一镜末帧与下一镜首帧逐值相同")
    print(f"相机曲线自检通过：{len(paths)} 段，接缝 {len(paths) - 1} 处逐值闭合")


def setup_scene(blend: Path, hide_roof: bool = True) -> bpy.types.Object:
    bpy.ops.wm.open_mainfile(filepath=str(blend))
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
    if roof is not None and hide_roof:
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


def run(ep: str, blend: Path, paths: tuple[ShotPath, ...], env: Envelope) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots", type=int, nargs="*", default=None)
    ap.add_argument("--stills", action="store_true", help="只出每镜首末帧 PNG（秒级，用于查接缝）")
    ap.add_argument("--check", action="store_true", help="只跑相机曲线自检，不开 Blender 场景")
    args = ap.parse_args(argv)

    check(paths, env)
    if args.check:
        return 0
    if not blend.is_file():
        print(f"几何不存在：{blend}——先跑对应的 build_*.py", file=sys.stderr)
        return 1

    shots_dir = DRAMA / ep / "5_6_分镜与prompt" / "shots"
    wanted = [p for p in paths if not args.shots or p.n in args.shots]
    cam = setup_scene(blend)
    sc = bpy.context.scene

    for p in wanted:
        last = bake(cam, p)
        out = shots_dir / f"shot{p.n:02d}" / "previz"
        out.mkdir(parents=True, exist_ok=True)
        if args.stills:
            for tag, frame in (("first", 1), ("last", last)):
                sc.frame_set(frame)
                sc.render.image_settings.file_format = "PNG"
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
