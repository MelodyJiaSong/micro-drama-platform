# -*- coding: utf-8 -*-
"""Seedance 参考视频的硬下限 / 上限，以及把超长 previz 切成可上传的几段——唯一出处（不 import bpy，引擎与生成器共用）。

实测 / 文档（ai_video.md rule 24）：宽×高 ≥ 409600 像素；每条参考视频 2–15 s、24–60 fps；Seedance 2.5 一次最多 10 条。
本仓库镜长可到 30 s，所以 previz 超过 15 s 的一律切段：段界优先落在镜内硬切上，落不上就均分。

    python tools/previz/seedance_ref.py <previz_config.toml>     # 把已渲好的 shotNN_previz.mp4 切成 _p1/_p2…（不重渲）
"""
from __future__ import annotations

import math
import subprocess
import sys
import tomllib
from pathlib import Path

LIMITS = {"min_s": 2.0, "max_s": 15.0, "min_fps": 24, "max_fps": 60, "min_pixels": 409_600, "max_videos": 10}
SNAP_S = 3.0      # 均分点 ±3 s 内有镜内硬切就对齐到它


def check(fps: float, res: tuple[int, int]) -> list[str]:
    out = []
    if not LIMITS["min_fps"] <= fps <= LIMITS["max_fps"]:
        out.append("previz 帧率 %g 不在 Seedance 参考视频的 %d–%d fps" % (fps, LIMITS["min_fps"], LIMITS["max_fps"]))
    if res[0] * res[1] < LIMITS["min_pixels"]:
        out.append("previz 分辨率 %dx%d = %d 像素 < Seedance 下限 %d" % (res[0], res[1], res[0] * res[1], LIMITS["min_pixels"]))
    return out


def parts(total: float, cuts: list[float]) -> list[tuple[float, float]]:
    """[(起, 止)]：总长 ≤ 15 s 就是一整段；否则切成最少的段数，段界尽量对齐镜内硬切，每段 2–15 s。"""
    if total <= LIMITS["max_s"]:
        return [(0.0, total)]
    n = math.ceil(total / LIMITS["max_s"])
    if n > LIMITS["max_videos"]:
        raise ValueError("镜长 %gs 要切 %d 段，超过 Seedance 一次 %d 条参考视频" % (total, n, LIMITS["max_videos"]))
    bounds = [0.0]
    for k in range(1, n):
        ideal = total * k / n
        near = [c for c in cuts if abs(c - ideal) <= SNAP_S]
        pick = min(near, key=lambda c: abs(c - ideal)) if near else ideal
        lo, hi = bounds[-1] + LIMITS["min_s"], min(bounds[-1] + LIMITS["max_s"], total - LIMITS["min_s"])
        if not lo <= pick <= hi or total - pick > LIMITS["max_s"] * (n - k):
            pick = ideal
        bounds.append(round(pick, 3))
    bounds.append(total)
    return list(zip(bounds, bounds[1:]))


def part_path(mp4: Path, i: int) -> Path:
    return mp4.with_name("%s_p%d.mp4" % (mp4.stem, i))


def split(mp4: Path, total: float, cuts: list[float]) -> list[Path]:
    """切段（重编码，段首不必落在关键帧上）；只有一段时不切、返回原文件。"""
    segs = parts(total, cuts)
    for old in mp4.parent.glob("%s_p*.mp4" % mp4.stem):
        old.unlink()
    if len(segs) == 1:
        return [mp4]
    out = []
    for i, (a, b) in enumerate(segs, 1):
        dst = part_path(mp4, i)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "%.3f" % a, "-to", "%.3f" % b, "-i", str(mp4),
                        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-an", str(dst)], check=True)
        out.append(dst)
    return out


def cuts_of(cfg: dict) -> list[float]:
    return [float(w["t"]) for w in cfg.get("机位", {}).get("路点", []) if w.get("切")]


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    p = Path(sys.argv[1]).resolve()
    cfg = tomllib.loads(p.read_text(encoding="utf-8"))
    g = cfg["全局"]
    mp4 = p.parent / ("%s_previz.mp4" % (g.get("shot") or p.parent.parent.name))
    bad = check(float(g.get("fps", 24)), tuple(g.get("分辨率", [960, 540])))
    if bad:
        print("\n".join(bad))
        return 2
    for f in split(mp4, float(g["total_sec"]), cuts_of(cfg)):
        print(f)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
