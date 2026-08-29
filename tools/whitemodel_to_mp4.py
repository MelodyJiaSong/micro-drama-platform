"""把 Blender 渲出的白模 PNG 序列合成 MP4，喂给 Seedance 当 reference_video。

有些 Blender 构建没有编进 FFMPEG 支持（`image_settings.file_format` 的枚举里
只剩静帧格式），视频只能外部合成。build_orbit.py 探测到这种构建时会退回渲
PNG 序列到 `whitemodel/frames/`，由本脚本收尾。

    python tools/whitemodel_to_mp4.py shot12
    python tools/whitemodel_to_mp4.py shot12 --fps 24
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SHOTS = REPO / "ai_videos" / "xianjian_yi_mv" / "5_6_分镜与prompt" / "shots"


def _frames_dir(shot_id: str) -> Path:
    frames = SHOTS / shot_id / "whitemodel" / "frames"
    if not frames.is_dir():
        raise SystemExit(f"找不到 {frames}\n先在 Blender 里 Ctrl+F12 渲染动画。")
    if not sorted(frames.glob("*.png")):
        raise SystemExit(f"{frames} 里没有 PNG。渲染是不是还没跑完？")
    return frames


def _encode(frames: Path, dst: Path, fps: int) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise SystemExit("PATH 里找不到 ffmpeg。")
    # -pix_fmt yuv420p：Seedance 要 H.264；不加这个参数 ffmpeg 会因为源是 RGB PNG
    # 而选 yuv444p，部分播放器与上传端直接判为不支持。
    cmd = [
        ffmpeg, "-y",
        "-framerate", str(fps),
        "-pattern_type", "glob",
        "-i", str(frames / "*.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "16",
        str(dst),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        sys.stderr.write(result.stderr[-3000:])
        raise SystemExit(f"ffmpeg 失败，退出码 {result.returncode}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("shot_id", help="例如 shot12")
    parser.add_argument("--fps", type=int, default=24)
    args = parser.parse_args()

    frames = _frames_dir(args.shot_id)
    dst = frames.parent / f"{args.shot_id}_orbit_whitemodel.mp4"
    _encode(frames, dst, args.fps)

    count = len(sorted(frames.glob("*.png")))
    print(f"{count} 帧 → {dst}")
    print(f"时长 {count / args.fps:.1f} 秒，{args.fps}fps")
    print("传进即梦时排在所有参考图之后，作为 @视频1")


if __name__ == "__main__":
    main()
