"""配乐拼接（bible §5）：Suno 同一任务的两首纯音乐 A、B，等功率交叉淡化（acrossfade qsin，排行榜 ep01 QC 结论），
再加一段前低后高的音量爬升，让整体向前 5 名、冠军推进；结尾淡出。

    python ai_videos/zhenshi_chidu/_tools/music.py A.mp3 B.mp3 --a-end 125 --b-start 23 --total 245.2 \
        [--ramp-db -4 --ramp-end 190] --out mix.wav

A 取 [0, a_end]，B 从 b_start 起接上（交叉 4 s）。B 的时刻 b 落在视频 a_end − 4 + (b − b_start)。
选点依据：两首都在约 110–125 s 最响、约 130 s 有一处停顿；让 B 的高潮落在前 5 名与冠军，B 的停顿落在切到合影处。
"""
from __future__ import annotations

import argparse
import subprocess

XF = 4.0


def dur(p: str) -> float:
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--a-end", type=float, required=True)
    ap.add_argument("--b-start", type=float, required=True)
    ap.add_argument("--total", type=float, required=True)
    ap.add_argument("--ramp-db", type=float, default=-4.0, help="开头相对增益（dB），线性升到 0")
    ap.add_argument("--ramp-end", type=float, default=190.0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    need = a.total - (a.a_end - XF)
    if dur(a.b) - a.b_start < need:
        raise SystemExit(f"B 从 {a.b_start}s 起不够长：要 {need:.1f}s")
    g0 = 10 ** (a.ramp_db / 20)
    fc = (f"[0:a]atrim=0:{a.a_end:.3f}[A];[1:a]atrim=start={a.b_start:.3f},asetpts=PTS-STARTPTS[B];"
          f"[A][B]acrossfade=d={XF}:c1=qsin:c2=qsin[m];"
          f"[m]atrim=0:{a.total:.3f},volume='min(1,{g0:.4f}+(1-{g0:.4f})*t/{a.ramp_end})':eval=frame,"
          f"afade=t=out:st={a.total - 5:.3f}:d=5[o]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.a, "-i", a.b, "-filter_complex", fc,
                    "-map", "[o]", "-ar", "48000", a.out], check=True)
    for bt in (100, 125, 130):
        print(f"B {bt}s → 视频 {a.a_end - XF + bt - a.b_start:.1f}s")
    print("->", a.out, f"{dur(a.out):.1f}s")


if __name__ == "__main__":
    main()
