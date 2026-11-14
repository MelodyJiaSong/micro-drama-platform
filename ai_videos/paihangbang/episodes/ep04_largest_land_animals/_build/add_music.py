"""给已渲好的静音母版补配乐（不重渲画面）。

画面渲染在本机繁忙时约 1 小时 / 版；静音母版已用最终 data.json / assets.json 渲好（manifest 的 sha 对得上），
所以只重建音乐床并复制视频流。音乐床用 rank_scroll 自己的 build_music_bed（同样的交叉淡化、两遍 loudnorm -16 LUFS），
与 `python -m rank_scroll render --music ... --music-fit end` 的音轨一致；manifest 补 inputs.music / music_bed。

用法：python _build/add_music.py <render/xxx_master.mp4> [--fit end] a.mp3[@IN:OUT] b.mp3 ...
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "projects" / "rank_scroll"))
from rank_scroll.render import build_music_bed  # noqa: E402


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("master")
    ap.add_argument("tracks", nargs="+")
    ap.add_argument("--fit", choices=("none", "end"), default="end")
    a = ap.parse_args()
    mp4 = Path(a.master).resolve()
    man_path = mp4.with_suffix(".manifest.json")
    man = json.loads(man_path.read_text(encoding="utf-8"))
    if man.get("output_sha256") != sha(mp4):
        print("母版与 manifest 的 sha 不符，停止", file=sys.stderr)
        return 2
    t0, t1 = man["range_s"]
    full = man["timeline"][-1][2] if man.get("timeline") else man["duration_s"]
    dur = float(man["duration_s"])
    wav = mp4.with_name(mp4.stem + ".music.wav")
    bed = build_music_bed(a.tracks, full, t0, dur, a.fit, wav)
    tmp = mp4.with_name(mp4.stem + ".remux.mp4")
    cmd = [shutil.which("ffmpeg"), "-y", "-hide_banner", "-loglevel", "error", "-i", str(mp4), "-i", str(wav),
           "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
           "-t", f"{dur:.3f}", "-movflags", "+faststart", str(tmp)]
    subprocess.run(cmd, check=True)
    wav.unlink(missing_ok=True)
    try:
        tmp.replace(mp4)
    except PermissionError:      # Windows：预览页正在串流母版时不能改名，退回原地覆盖写
        with tmp.open("rb") as src, mp4.open("r+b") as dst:
            shutil.copyfileobj(src, dst, 1 << 20)
            dst.truncate()
        tmp.unlink()
    man["inputs"]["music"] = bed["tracks"]
    man["inputs"]["music_bed"] = {k: v for k, v in bed.items() if k != "tracks"}
    man["music_remux"] = {"note": "视频流复制自静音母版（同一 data/assets），只换音轨", "ffmpeg": cmd,
                          "video_sha256_before": man["output_sha256"]}
    man["output_sha256"] = sha(mp4)
    man_path.write_text(json.dumps(man, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"ok {mp4.name}: {len(bed['tracks'])} track(s), {dur:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
