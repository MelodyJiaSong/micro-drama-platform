"""抖音合集「全球之最排行榜」封面候选（3:4，1080×1440）。

    python ai_videos/paihangbang/_tools/collection_cover.py

只用免署名可商用的实拍图（Pexels / Unsplash License、CC0），不用有全景自由风险的建筑和雕像；
字体 Noto Sans SC（SIL OFL）。输出到 `_assets/collection_cover/`，另出一张对比图 `contact_sheet.jpg`。
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SERIES = Path(__file__).resolve().parents[1]
REPO = SERIES.parents[1]
FONT = REPO / "projects" / "rank_scroll" / "assets" / "fonts" / "NotoSansSC-Variable.ttf"
OUT = SERIES / "_assets" / "collection_cover"
W, H = 1080, 1440
GOLD = (245, 184, 46)
NAVY = (14, 20, 34)
WHITE = (255, 255, 255)

# 题材代表图：(期, 文件, 标签, 卡上数字)
PICS = {
    "everest": ("ep02_highest_peak_by_country", "00_mount_everest.jpg", "最高", "8849米"),
    "elephant": ("ep04_largest_land_animals", "01_african_bush_elephant.jpg", "最大", "6000千克"),
    "nile": ("ep17_longest_rivers", "01_nile.jpg", "最长", "6650公里"),
    "baikal": ("ep15_deepest_lakes", "01_lake_baikal.jpg", "最深", "1642米"),
    "bugatti": ("ep18_fastest_cars", "02_bugatti_chiron_super_sport_300.jpg", "最快", "490km/h"),
    "amazon": ("ep17_longest_rivers", "02_amazon.jpg", "", ""),
    "chimborazo": ("ep14_highest_volcanoes", "08_chimborazo.jpg", "", ""),
    "russia": ("ep12_largest_countries_by_area", "01_russia.jpg", "", ""),
    "france": ("ep19_most_visited_countries", "01_france.jpg", "最热门", "1亿人次"),
}


def font(size: int, weight: int = 900) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(str(FONT), size)
    try:
        f.set_variation_by_axes([weight])
    except (OSError, ValueError):
        pass
    return f


def photo(key: str) -> Image.Image:
    ep, name, *_ = PICS[key]
    return Image.open(SERIES / "episodes" / ep / "assets" / "img" / name).convert("RGB")


def cover(img: Image.Image, w: int, h: int, fy: float = 0.5) -> Image.Image:
    s = max(w / img.width, h / img.height)
    im = img.resize((round(img.width * s) + 1, round(img.height * s) + 1), Image.LANCZOS)
    x = (im.width - w) // 2
    y = int((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h))


def gradient(w: int, h: int, top: int, bottom: int, color=(0, 0, 0)) -> Image.Image:
    g = Image.new("L", (1, h))
    for y in range(h):
        g.putpixel((0, y), round(top + (bottom - top) * y / max(h - 1, 1)))
    layer = Image.new("RGBA", (w, h), color + (0,))
    layer.putalpha(g.resize((w, h)))
    return layer


def text(d: ImageDraw.ImageDraw, xy, s: str, f, fill=WHITE, anchor="la", stroke=0, shadow=True):
    if shadow:
        d.text((xy[0] + 4, xy[1] + 6), s, font=f, fill=(0, 0, 0, 150), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, 150))
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0))


def badge(d: ImageDraw.ImageDraw, x: int, y: int, s: str, size: int = 54, anchor_center=False):
    f = font(size)
    tw = d.textlength(s, font=f)
    pw, ph = tw + size * 0.9, size * 1.45
    if anchor_center:
        x -= pw / 2
    d.rounded_rectangle((x, y, x + pw, y + ph), radius=ph * 0.28, fill=GOLD)
    d.text((x + pw / 2, y + ph / 2), s, font=f, fill=NAVY, anchor="mm")
    return pw, ph


def title_block(d, cx: int, y: int, big=170, small=110):
    text(d, (cx, y), "全球之最", font(big), fill=GOLD, anchor="ma")
    text(d, (cx, y + big * 1.12), "排行榜", font(small), anchor="ma")


# ---------- A 拼图 ----------
def v_mosaic() -> Image.Image:
    im = Image.new("RGB", (W, H), NAVY)
    keys = ["everest", "elephant", "nile", "baikal", "bugatti", "chimborazo", "amazon", "russia", "france"]
    gap, cols, rows = 8, 3, 3
    cw, ch = (W - gap * (cols + 1)) // cols, 300
    top = 560
    for i, k in enumerate(keys):
        r, c = divmod(i, cols)
        x, y = gap + c * (cw + gap), top + r * (ch + gap)
        im.paste(cover(photo(k), cw, ch), (x, y))
    im = im.convert("RGBA")
    im.alpha_composite(gradient(W, 300, 255, 0, NAVY), (0, 560))
    d = ImageDraw.Draw(im)
    badge(d, W // 2, 70, "TOP 50", 56, anchor_center=True)
    title_block(d, W // 2, 175)
    im.alpha_composite(gradient(W, 260, 0, 235, NAVY), (0, H - 260))
    d = ImageDraw.Draw(im)
    text(d, (W // 2, 1395), "最高 · 最大 · 最长 · 最深 · 最快 · 最热门", font(46, 700), anchor="ms")
    return im.convert("RGB")


# ---------- B 单图大片 ----------
def v_hero() -> Image.Image:
    im = cover(photo("everest"), W, H, 0.45).convert("RGBA")
    im.alpha_composite(gradient(W, 620, 230, 0), (0, 0))
    im.alpha_composite(gradient(W, 520, 0, 235), (0, H - 520))
    d = ImageDraw.Draw(im)
    badge(d, 70, 80, "TOP 50", 52)
    text(d, (70, 200), "全球之最", font(200), fill=GOLD)
    text(d, (74, 445), "排行榜", font(130))
    text(d, (74, 1190), "第1名是谁？", font(84))
    text(d, (76, 1305), "从倒数第一数到第一", font(50, 600))
    return im.convert("RGB")


# ---------- C 排行条 ----------
def v_bars() -> Image.Image:
    im = Image.new("RGBA", (W, H), NAVY + (255,))
    d = ImageDraw.Draw(im)
    for y in range(0, H, 6):                      # 细网格底纹
        d.line((0, y, W, y), fill=(19, 26, 41, 255))
    badge(d, 70, 70, "TOP 50", 50)
    text(d, (70, 175), "全球之最", font(170), fill=GOLD, shadow=False)
    text(d, (76, 385), "排行榜", font(104), shadow=False)
    rows = ["everest", "elephant", "nile", "baikal", "france"]
    botgap = (H - 70 - 590 - 5 * 150) // 4          # 五条铺满到底边留 70
    widths = [930, 850, 770, 690, 610]
    y = 590
    for k, bw in zip(rows, widths):
        _, _, label, val = PICS[k]
        bh = 150
        bar = cover(photo(k), bw, bh).convert("RGBA")
        bar.alpha_composite(gradient(bw, bh, 70, 200).rotate(90, expand=True).resize((bw, bh)))
        mask = Image.new("L", (bw, bh), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, bw - 1, bh - 1), radius=22, fill=255)
        im.paste(bar, (75, y), mask)
        lw = max(150, d.textlength(label, font=font(56)) + 44)
        d.rounded_rectangle((75, y, 75 + lw, y + bh), radius=22, fill=GOLD)
        d.text((75 + lw / 2, y + bh / 2), label, font=font(56), fill=NAVY, anchor="mm")
        text(d, (75 + bw - 28, y + bh / 2), val, font(50, 800), anchor="rm", stroke=2)
        y += bh + botgap
    return im.convert("RGB")


# ---------- D No.1 ----------
def v_no1() -> Image.Image:
    keys = ["everest", "elephant", "baikal", "nile"]
    sw = W // len(keys)
    im = Image.new("RGB", (W, H), NAVY)
    for i, k in enumerate(keys):
        im.paste(cover(photo(k), sw, H), (i * sw, 0))
    im = im.convert("RGBA")
    im.alpha_composite(Image.new("RGBA", (W, H), NAVY + (120,)))
    blur = im.filter(ImageFilter.GaussianBlur(0))
    im = blur
    im.alpha_composite(gradient(W, 760, 0, 245, NAVY), (0, H - 760))
    d = ImageDraw.Draw(im)
    for i in range(1, len(keys)):
        d.line((i * sw, 0, i * sw, H), fill=(255, 255, 255, 90), width=3)
    text(d, (W // 2, 210), "No.1", font(330), fill=GOLD, anchor="ma", stroke=4)
    title_block(d, W // 2, 900, big=180, small=112)
    return im.convert("RGB")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    variants = {"A_mosaic": v_mosaic(), "B_hero": v_hero(), "C_bars": v_bars(), "D_no1": v_no1()}
    for name, im in variants.items():
        im.save(OUT / f"cover_{name}.png", optimize=True)
    tw, th, pad = 360, 480, 24
    sheet = Image.new("RGB", (pad + len(variants) * (tw + pad), th + pad * 2 + 50), (235, 237, 241))
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(variants.items()):
        x = pad + i * (tw + pad)
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, pad))
        d.text((x + tw / 2, pad + th + 30), name.split("_")[0], font=font(36, 800), fill=(30, 30, 30), anchor="mm")
    sheet.save(OUT / "contact_sheet.jpg", quality=90)
    print("\n".join(str(OUT / f"cover_{n}.png") for n in variants))


if __name__ == "__main__":
    main()
