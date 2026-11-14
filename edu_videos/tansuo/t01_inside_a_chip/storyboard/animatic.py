"""动态故事板（animatic）：故事板图按节拍时长串成小样片，叠台词草稿字幕、比例尺读数与真实性角标，出片前给用户预览节奏。
不配音、不动画，只看「顺序、时长、画面配台词」是否对。输出 storyboard/animatic.mp4（媒体不进 git）。

    python edu_videos/tansuo/t01_inside_a_chip/storyboard/animatic.py
"""
import json
import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
spec = json.loads((HERE / "panels.json").read_text(encoding="utf-8"))
FONT = "C:/Windows/Fonts/NotoSansSC-VF.ttf"          # edu 约定：中文用 Noto Sans SC
W, H = 1920, 1080
# 每格秒数（合计约 4 分 45 秒，按节拍表的信息量分配；讲稿定稿后按配音时间轴重排）
DUR = {"P01": 12, "P02": 8, "P03": 16, "P04": 20, "P05": 22, "P06": 16, "P07": 30,
       "P08": 34, "P09": 20, "P10": 26, "P11": 14, "P12": 18, "P13": 8, "P14": 21}


def badge(source: str) -> str:
    if source.startswith("Seedance"):
        return "AI 画面 · 非结构"
    if "比例准确" in source:
        return "3D 示意 · 尺寸取自先进芯片"
    return "3D 示意"


def clean(line: str) -> str:
    return re.sub(r"（[^）]*）", "", line).strip()


def frame(img: Path, sub: str, scale: str, tag: str, pid: str) -> Image.Image:
    im = Image.open(img).convert("RGB").resize((W, H))
    d = ImageDraw.Draw(im, "RGBA")
    f_sub, f_small = ImageFont.truetype(FONT, 44), ImageFont.truetype(FONT, 28)
    d.rounded_rectangle((40, 36, 60 + d.textlength(tag, font=f_small), 84), 12, fill=(0, 0, 0, 120))
    d.text((50, 40), tag, font=f_small, fill=(255, 255, 255, 230))
    d.text((W - 110, 40), pid, font=f_small, fill=(255, 255, 255, 160))
    bar = 220
    d.rectangle((W - 60 - bar, H - 64, W - 60, H - 58), fill=(255, 255, 255, 220))
    tw = d.textlength(scale, font=f_small)
    d.text((W - 60 - bar / 2 - tw / 2, H - 108), scale, font=f_small, fill=(255, 255, 255, 230))
    if sub:
        tw = d.textlength(sub, font=f_sub)
        x = (W - tw) / 2
        d.rounded_rectangle((x - 24, H - 190, x + tw + 24, H - 118), 14, fill=(0, 0, 0, 140))
        d.text((x, H - 184), sub, font=f_sub, fill=(255, 255, 255))
    return im


def main() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="animatic_"))
    lst = []
    for p in spec["panels"]:
        img = HERE / f"{p['id']}.png"
        lines = [clean(l) for l in p["lines"] if clean(l) and not clean(l).startswith("（")] or [""]
        per = DUR[p["id"]] / len(lines)
        for i, line in enumerate(lines):
            out = tmp / f"{p['id']}_{i}.png"
            frame(img, line, p["scale"], badge(p["source"]), p["id"]).save(out)
            lst.append(f"file '{out.as_posix()}'\nduration {per:.2f}")
    lst.append(f"file '{out.as_posix()}'")
    (tmp / "list.txt").write_text("\n".join(lst), encoding="utf-8")
    dst = HERE / "animatic.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"),
                    "-vf", "fps=24,format=yuv420p", "-c:v", "libx264", "-crf", "20", str(dst)], check=True)
    print(dst, sum(DUR.values()), "s")


if __name__ == "__main__":
    main()
