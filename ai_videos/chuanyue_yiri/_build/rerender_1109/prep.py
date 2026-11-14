# -*- coding: utf-8 -*-
"""EP01 11-09 重出：给每条新条准备审片材料（只读视频，写到条目录的 _review/）。

    python prep.py <条目录> [<条目录> …]

产物：sheet_1fps.jpg（每秒一帧带时间码）、sheet_4fps_*.jpg（每 4 秒一张、每秒 4 帧，细看用）、
transcript.txt（faster-whisper small 逐词，带 VAD，自动语种）、motion.txt（tools/motion_check.py 定格/慢动作/剪切筛查）、
spec.md（这一镜分镜：时长、画面、走位、节拍、镜头、台词、人物道具）。
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
EP = REPO / "ai_videos/chuanyue_yiri/episodes/ep01"
_model = None


def whisper():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        _model = WhisperModel("small", device="cpu", compute_type="int8")
    return _model


def spec(take: Path) -> str:
    g = json.loads((take / "generation.json").read_text(encoding="utf-8"))
    _, sid, stid = g["key"].split("_")
    F = json.loads((EP / "filming.json").read_text(encoding="utf-8"))["content"]["scenes"]
    sc = next(s for s in F if s["id"] == sid)
    sh = next(x for x in sc["shots"] if x["id"] == stid)
    lines = [f"# {g['key']} · {sc.get('location', '')} · {sc.get('time', '')}", f"时长 {sh.get('duration')} 秒；场目的：{sc.get('purpose', '')}", ""]
    for k, lab in [("action", "画面"), ("blocking", "走位"), ("beats", "动作节拍"), ("camera", "镜头"), ("lighting", "光线"),
                   ("dialogue", "台词"), ("cast", "人物"), ("props", "道具")]:
        v = sh.get(k)
        if v:
            lines.append(f"## {lab}\n{v if isinstance(v, str) else '、'.join(v)}\n")
    return "\n".join(lines)


def run(take: Path) -> None:
    g = json.loads((take / "generation.json").read_text(encoding="utf-8"))
    video = take / g["video"]
    out = take / "_review"
    out.mkdir(exist_ok=True)
    (out / "spec.md").write_text(spec(take), encoding="utf-8")
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                               capture_output=True, text=True).stdout.strip() or 0)
    n = int(dur) + 1
    cols = 6
    rows = (n + cols - 1) // cols
    dt = "drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='%{pts\\:hms}':x=6:y=6:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.6"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-vf", f"fps=1,scale=426:-1,{dt},tile={cols}x{rows}",
                    "-frames:v", "1", str(out / "sheet_1fps.jpg")], check=False)
    for start in range(0, int(dur) + 1, 4):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-t", "4", "-i", str(video),
                        "-vf", f"fps=4,scale=480:-1,{dt.replace('%{pts', '%{pts')},tile=4x4", "-frames:v", "1",
                        str(out / f"sheet_4fps_{start:02d}.jpg")], check=False)
    segs, info = whisper().transcribe(str(video), word_timestamps=True, vad_filter=True)
    lines = [f"语种 {info.language}（{info.language_probability:.2f}），时长 {dur:.2f}s"]
    for s in segs:
        lines.append(f"{s.start:6.2f}-{s.end:6.2f} {s.text.strip()}")
        lines.append("    " + " ".join(f"{w.word.strip()}@{w.start:.2f}" for w in (s.words or [])))
    (out / "transcript.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    m = subprocess.run([sys.executable, str(REPO / "tools/motion_check.py"), str(video)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    (out / "motion.txt").write_text((m.stdout + m.stderr)[-4000:], encoding="utf-8")
    print("ok", take.relative_to(REPO).as_posix(), f"{dur:.1f}s")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for a in sys.argv[1:]:
        try:
            run(Path(a).resolve())
        except Exception as e:  # noqa: BLE001
            print("✗", a, e)
