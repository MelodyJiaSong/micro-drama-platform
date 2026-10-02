# -*- coding: utf-8 -*-
"""previz 先看静帧、再渲整条：一条命令建场 + 自检 + 出关键时刻静帧 + 拼成一张带秒数的审阅图。

    python tools/previz/review.py <shot 目录>/previz/previz_config.toml            # 缺省时刻：机位切点、段中、每 3 秒
    python tools/previz/review.py <config> --times 5.5,9,13.9,14.3                  # 指定秒数

产物：`previz/frames/stills/shotNN_{秒}.png` 与拼图 `previz/frames/shotNN_stills.png`（`previz/frames/` 不进 R2，随时重出）。
静帧通过、看过，再跑 `blender -b --factory-startup --python tools/previz/build_previz.py -- <config>` 渲整条 MP4。
整条要 4–7 分钟，这里几十秒（follow-up 032 复盘：shot01 三轮返工都是渲完整条才看到问题）。
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))
from blender_exe import BLENDER  # noqa: E402

COLS = 4
KEEP = ("自检", "✗", "[命中]", "[warning]", "[可见性]", "静帧", "错误", "占画", "Traceback", "Error")


def tile(stills: list[Path], out: Path) -> None:
    ims = [Image.open(p).convert("RGB") for p in stills]
    w, h = ims[0].size
    rows = (len(ims) + COLS - 1) // COLS
    sheet = Image.new("RGB", (w * min(COLS, len(ims)), h * rows), (30, 30, 30))
    try:
        font = ImageFont.truetype("msyh.ttc", max(18, h // 14))
    except OSError:
        font = ImageFont.load_default()
    d = ImageDraw.Draw(sheet)
    for i, (p, im) in enumerate(zip(stills, ims)):
        x, y = (i % COLS) * w, (i // COLS) * h
        sheet.paste(im, (x, y))
        label = p.stem.rsplit("_", 1)[-1]
        d.rectangle((x, y, x + len(label) * font.size * 0.62 + 16, y + font.size + 12), fill=(0, 0, 0))
        d.text((x + 8, y + 4), label, font=font, fill=(255, 255, 255))
    sheet.save(out)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--times", default="", help="逗号分隔的秒数")
    args = ap.parse_args()
    cfg = Path(args.config).resolve()
    shot = cfg.parent.parent.name
    for old in (cfg.parent / "frames" / "stills").glob(f"{shot}_*.png"):   # 052：建场失败时不许拿上一轮的静帧拼图冒充
        old.unlink()
    flag = "--stills" + ("=" + args.times if args.times else "")
    r = subprocess.run([BLENDER, "-b", "--factory-startup", "--python", str(REPO / "tools" / "previz" / "build_previz.py"),
                        "--", str(cfg), flag], capture_output=True, text=True, encoding="utf-8", errors="replace")
    for ln in (r.stdout + r.stderr).splitlines():
        if any(k in ln for k in KEEP):
            print(ln)
    stills = sorted((cfg.parent / "frames" / "stills").glob(f"{shot}_*.png"),
                    key=lambda p: float(p.stem.rsplit("_", 1)[-1].rstrip("s")))
    if not stills:
        print("没有出静帧（建场失败？看上面的报错）")
        return r.returncode or 1
    out = cfg.parent / "frames" / f"{shot}_stills.png"
    tile(stills, out)
    print("拼图 → %s（%d 张）" % (out.relative_to(REPO), len(stills)))
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
