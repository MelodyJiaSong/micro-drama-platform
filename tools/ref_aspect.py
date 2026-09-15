"""Keep reference images inside Seedance's upload aspect window (1:3 – 3:1).

Seedance rejects any uploaded image whose width:height falls outside [1/3, 3].
Historical references are often scroll strips (4:1 up to 35:1), so every image
under a `ref/` folder must be brought inside the window before it is uploaded.

Two fixes, both lossless for content (nothing is cropped):
- mild strips (ratio <= 6, or >= 1/6): pad the short side with a neutral
  border up to exactly 3:1 / 1:3;
- extreme strips: cut the long side into k equal pieces and stack them with a
  thin gap (row-wrap), k = ceil(sqrt(ratio / 3)), so the result fills the frame
  instead of being a thin band floating in a blank canvas.

    python tools/ref_aspect.py check <path|dir> ...   # list violations, exit 1 if any
    python tools/ref_aspect.py fix   <path|dir> ...   # rewrite violating files in place

`tools/ref_fetch.py` calls `fit()` on every image it downloads or registers.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from PIL import Image

MAX_RATIO = 3.0
PAD_LIMIT = 6.0
PAD_COLOR = (238, 236, 232)
GAP_FRAC = 0.03
EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def ratio_of(path: Path) -> float:
    with Image.open(path) as im:
        return im.width / im.height


def in_window(ratio: float) -> bool:
    return 1 / MAX_RATIO <= ratio <= MAX_RATIO


def _pad(im: Image.Image, wide: bool) -> Image.Image:
    w, h = im.size
    size = (w, math.ceil(w / MAX_RATIO)) if wide else (math.ceil(h / MAX_RATIO), h)
    canvas = Image.new("RGB", size, PAD_COLOR)
    canvas.paste(im, ((size[0] - w) // 2, (size[1] - h) // 2))
    return canvas


def _wrap(im: Image.Image, wide: bool, ratio: float) -> Image.Image:
    k = math.ceil(math.sqrt(ratio / MAX_RATIO))
    w, h = im.size
    if wide:
        piece, gap = math.ceil(w / k), max(2, round(h * GAP_FRAC))
        canvas = Image.new("RGB", (piece, k * h + (k - 1) * gap), PAD_COLOR)
        for i in range(k):
            canvas.paste(im.crop((i * piece, 0, min(w, (i + 1) * piece), h)), (0, i * (h + gap)))
    else:
        piece, gap = math.ceil(h / k), max(2, round(w * GAP_FRAC))
        canvas = Image.new("RGB", (k * w + (k - 1) * gap, piece), PAD_COLOR)
        for i in range(k):
            canvas.paste(im.crop((0, i * piece, w, min(h, (i + 1) * piece))), (i * (w + gap), 0))
    return canvas


def fit(path: Path) -> tuple[int, int] | None:
    """Rewrite `path` in place if it is outside the window; return the new size, or None if untouched."""
    with Image.open(path) as src:
        im = src.convert("RGB")
    ratio = im.width / im.height
    if in_window(ratio):
        return None
    wide = ratio > 1
    stretch = ratio if wide else 1 / ratio
    out = _pad(im, wide) if stretch <= PAD_LIMIT else _wrap(im, wide, stretch)
    if path.suffix.lower() in (".jpg", ".jpeg"):
        out.save(path, quality=95)
    else:
        out.save(path)
    return out.size


def _images(targets: list[str]) -> list[Path]:
    files: list[Path] = []
    for t in map(Path, targets):
        files += sorted(p for p in t.rglob("*") if p.suffix.lower() in EXTS) if t.is_dir() else [t]
    return files


def main(argv: list[str]) -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    if len(argv) < 2 or argv[0] not in ("check", "fix"):
        print(__doc__)
        return 2
    bad = 0
    for p in _images(argv[1:]):
        r = ratio_of(p)
        if in_window(r):
            continue
        bad += 1
        if argv[0] == "check":
            print(f"{r:6.2f}  {p}")
        else:
            w, h = fit(p)
            print(f"{r:6.2f} -> {w / h:4.2f}  {w}x{h}  {p}")
    print(f"-- {bad} outside 1:3–3:1", file=sys.stderr)
    return 1 if bad and argv[0] == "check" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
