# -*- coding: utf-8 -*-
"""锚点图 ↔ blend 同机位对账：把「blend 要尽量接近图片」变成可跑的判据。

为什么要有这个文件
------------------
`ai_video.md` rule 4e ⑥ 说「`.blend` 是图的下游」，用户 2026-09-18 再次定调「blender 要做的尽量和
图片接近」。但此前对账全靠人眼抽查——bg2 那次才发现夯层被渲成竖条纹、城墙收分成了土坡；
没抽到的（水色、耕地、街面）就一直错着。人眼抽查漏得多，所以把它做成一条命令：
**同一个机位，左边锚点图、右边 blend 渲图，并排出一张 PNG，再打出可量的色差**。

量什么（都可证伪，不靠审美）
    · 画面分区（天 / 中景 / 近景三带）的平均色与亮度差 —— 抓「水太蓝、地太绿、墙太亮」这类整体偏色
    · 主体色的饱和度差 —— 抓「CG 味」（生成图普遍比脚本渲图脏、饱和度低）
    · 天际线高度差 —— 抓机位俯角与焦距对不上（画面里城的位置差一截，说明机位没对上图）

用法（仓库根目录；渲染批任务跑完再用，别和 previz 抢 GPU —— rule 4h ⑥）：
    blender -b <bianjing.blend> --python tools/plate_match.py -- --plates bg2-1,bg3-1
    blender -b <bianjing.blend> --python tools/plate_match.py -- --all --samples 64

产物：`scenes/bianjing/_blender/match/{key}_match.png`（左图右渲）+ 终端一张色差表。
每次改完 look pass 跑一次，差值只许变小。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import bpy
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_bianjing as bj  # noqa: E402
import look_bianjing as lk  # noqa: E402

# 锚点图 → look_bianjing.VIEWS 里的机位。只登记「机位能对上」的那些：
# 地面镜的机位由 previz 给、不在 VIEWS 里，此表不强求覆盖全部 26 张（rule 4e ④）。
PLATE_VIEW: dict[str, str] = {
    "bg0-1": "01_aerial_city",
    "bg1-1": "02_aerial_bianhe_hongqiao",
    "bg2-1": "05_dongshuimen",
    "bg4-1": "06_yujie_xuandelou",
    "bg7-1": "07_city_blocks_low",
}
BANDS = (("天", 0.00, 0.33), ("中景", 0.33, 0.66), ("近景", 0.66, 1.00))


def plate_path(key: str) -> Path | None:
    stem = key.split("-")[0]
    hits = sorted(lk.SCENES.glob(f"{stem}_*/{key}.png"))
    return hits[0] if hits else None


def load_rgb(path: Path) -> np.ndarray:
    _img, px = lk.load_pixels(path)
    return lk.srgb_to_linear(px[..., :3])


def band_stats(rgb: np.ndarray) -> list[tuple[str, float, float, np.ndarray]]:
    h = rgb.shape[0]
    out = []
    for name, a, b in BANDS:
        seg = rgb[int(h * a):int(h * b)].reshape(-1, 3)
        m = seg.mean(axis=0)
        lum = float(lk.luminance(m))
        sat = float((m.max() - m.min()) / max(1e-4, m.max()))
        out.append((name, lum, sat, m))
    return out


def skyline(rgb: np.ndarray) -> float:
    """天际线高度：自上往下第一行「不再是天」的相对位置（天＝蓝且亮且横向方差极小）。"""
    h = rgb.shape[0]
    for y in range(0, h, max(1, h // 400)):
        row = rgb[y]
        ratio = float((row[:, 2] / np.maximum(row[:, 0], 1e-4)).mean())
        if ratio < 1.02:                 # 蓝不再压过红 ＝ 已经是地面（原判据过严，整张图都判成非天、恒回 0）
            return y / h
    return 1.0


def render_view(view: str, out: Path, res: tuple[int, int], samples: int) -> Path:
    lk.enable_gpu()
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device, sc.cycles.samples, sc.cycles.use_denoising = "GPU", samples, True
    pos, look, lens = lk.VIEWS[view]
    cam_d = bpy.data.cameras.new("MATCH_CAM")
    cam_d.clip_start, cam_d.clip_end, cam_d.sensor_width, cam_d.lens = 0.1, 2000000.0, 36.0, lens
    cam = bpy.data.objects.new("MATCH_CAM", cam_d)
    lk.look_collection("LOOK_CITY").objects.link(cam)
    sc.camera = cam
    p, t = lk.world_of(pos), lk.world_of(look)
    cam.location = p
    cam.rotation_euler = (t - p).to_track_quat("-Z", "Y").to_euler()
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = res[0], res[1], 100
    im = sc.render.image_settings
    if hasattr(im, "media_type"):
        im.media_type = "IMAGE"
    im.file_format = "PNG"
    out.parent.mkdir(parents=True, exist_ok=True)
    sc.render.filepath = str(out)
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam)
    bpy.data.cameras.remove(cam_d)
    return out


def stack(plate: np.ndarray, shot: np.ndarray, out: Path) -> None:
    h = min(plate.shape[0], shot.shape[0])

    def fit(a: np.ndarray) -> np.ndarray:
        step = max(1, a.shape[0] // h)
        return a[::step][:h]

    both = np.concatenate([fit(plate), fit(shot)], axis=1)
    both = np.clip(both, 0.0, 1.0) ** (1 / 2.2)
    hh, ww = both.shape[:2]
    img = bpy.data.images.new(out.stem, ww, hh, float_buffer=True)
    rgba = np.concatenate([both, np.ones((hh, ww, 1), np.float32)], axis=2)
    img.pixels.foreach_set(rgba.astype(np.float32).ravel())
    img.filepath_raw = str(out)
    img.file_format = "PNG"
    img.save()
    bpy.data.images.remove(img)


def main() -> int:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--plates", default="", help="逗号分隔的锚点键，如 bg2-1,bg3-1")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--samples", type=int, default=48)
    a = ap.parse_args(argv)
    keys = list(PLATE_VIEW) if a.all or not a.plates else [k.strip() for k in a.plates.split(",")]
    if not bj.ROWS:
        bj.ROWS[:] = bj.parse_plan(bj.PLAN_MD.read_text(encoding="utf-8"))
        bj.load_w11()
    out_dir = lk.SCENES / "_blender" / "match"
    print(f"{'锚点':8s} {'带':6s} {'图亮度':>7s} {'渲亮度':>7s} {'Δ亮':>6s} {'图饱和':>7s} {'渲饱和':>7s} {'Δ饱':>6s}")
    for key in keys:
        view = PLATE_VIEW.get(key)
        p = plate_path(key)
        if view is None or p is None:
            print(f"{key}: 跳过（无登记机位或图不在盘上）")
            continue
        plate = load_rgb(p)
        res = (plate.shape[1], plate.shape[0])
        shot_png = render_view(view, out_dir / f"{key}_blend.png", res, a.samples)
        shot = load_rgb(shot_png)
        for (n, pl, ps, _pm), (_n2, rl, rs, _rm) in zip(band_stats(plate), band_stats(shot)):
            print(f"{key:8s} {n:6s} {pl:7.3f} {rl:7.3f} {rl - pl:+6.3f} {ps:7.2f} {rs:7.2f} {rs - ps:+6.2f}")
        print(f"{key:8s} 天际线  图 {skyline(plate):.3f}  渲 {skyline(shot):.3f}  Δ {skyline(shot) - skyline(plate):+.3f}")
        stack(plate, shot, out_dir / f"{key}_match.png")
        print(f"{key:8s} 并排图 → {out_dir / f'{key}_match.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
