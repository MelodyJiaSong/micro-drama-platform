# -*- coding: utf-8 -*-
"""demucs 拆人声：一镜或一集的音轨 → vocals.wav / no_vocals.wav（htdemucs，--two-stems=vocals）。

    python tools/post/stems.py <剧> <ep> [--shots 1-7] [--python PY]       # 逐镜 → {ep}/post/stems/shotNN/
    python tools/post/stems.py --input X.mp4 --out-dir DIR [--python PY]   # 任意一条（finish_ep 拆整集拼接片用）

no_vocals 是「无人声」的环境声与音效，tts_first 模式下垫在 TTS 台词下面（mux_av --source-stem）。
demucs 不在默认 Python 里：`--python` 指定装了它的解释器（默认 index-tts 的 venv）；导入失败即报错并给出安装命令，本工具不替你装。
逐单元落盘：源没变、两条 stem 都在就跳过。
"""
from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

import post_common as pc

MODEL = "htdemucs"
STEMS = ("vocals.wav", "no_vocals.wav")


def check_demucs(python: Path) -> None:
    if not python.is_file():
        raise SystemExit(f"找不到解释器 {python}：用 --python 指定一个装了 demucs 的 Python")
    r = subprocess.run([str(python), "-c", "import demucs.separate"], capture_output=True)
    if r.returncode != 0:
        why = (r.stderr.decode("utf-8", "replace").strip().splitlines() or ["?"])[-1]
        raise SystemExit(
            f"{python} 里导入 demucs 失败：{why}\n"
            f"本工具不替你装。装好后重跑：\n"
            f"  \"{python}\" -m pip install demucs\n"
            f"（demucs 依赖 torch / torchaudio，该解释器里已有就不会重装；首次运行会下载 htdemucs 权重约 80 MB。）")


def separate(src: Path, out_dir: Path, python: Path) -> Path:
    """src 的音轨 → out_dir/{vocals,no_vocals}.wav；返回 no_vocals.wav。"""
    no_voc = out_dir / "no_vocals.wav"
    sig = pc.signature([src], model=MODEL)
    if pc.fresh(no_voc, sig) and (out_dir / "vocals.wav").is_file():
        print(f"  {src.name}：stem 已是最新，跳过")
        return no_voc
    check_demucs(python)
    if not pc.probe(src).has_audio:
        raise SystemExit(f"{src} 没有音轨，拆不了")
    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=out_dir) as td:
        mix = Path(td) / "mix.wav"
        pc.run([pc.FFMPEG, "-y", "-i", src, "-vn", "-ac", "2", "-ar", "44100", mix])
        pc.run([python, "-m", "demucs", "--two-stems=vocals", "-n", MODEL, "-o", td, mix])
        got = Path(td) / MODEL / mix.stem
        for name in STEMS:
            (got / name).replace(out_dir / name)
    pc.stamp(no_voc, sig)
    print(f"  {src.name} → {out_dir}")
    return no_voc


def main() -> int:
    pc.utf8_console()
    ap = argparse.ArgumentParser(description="demucs 拆 vocals / no_vocals")
    ap.add_argument("drama", nargs="?")
    ap.add_argument("ep", nargs="?")
    ap.add_argument("--shots", default=None)
    ap.add_argument("--input", type=Path, default=None)
    ap.add_argument("--out-dir", type=Path, default=None)
    ap.add_argument("--python", type=Path, default=pc.POST_PYTHON)
    a = ap.parse_args()
    if a.input:
        separate(a.input, a.out_dir or a.input.with_suffix("").with_name(a.input.stem + "_stems"), a.python)
        return 0
    if not (a.drama and a.ep):
        ap.error("给 <剧> <ep>，或 --input")
    epd = pc.ep_dir(pc.drama_root(a.drama), a.ep)
    for d in pc.cut_shots(epd, a.shots):
        separate(pc.shot_mp4(d), epd / pc.POST_DIR / "stems" / d.name, a.python)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
