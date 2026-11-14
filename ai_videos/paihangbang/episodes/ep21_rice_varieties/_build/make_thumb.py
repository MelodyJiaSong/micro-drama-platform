# -*- coding: utf-8 -*-
"""ep21 自定封面（默认 thumb 取前 3 张，全是日本白米，看不出「各种不同」）：白 / 紫 / 红 / 黑四种米并排 + 大标题。
英文版 render/thumbnail.png；中文版 render/thumbnail_zh.png（Noto Sans SC）。AI 图角上标 AI IMAGE / AI图像。

    python ai_videos/paihangbang/episodes/ep21_rice_varieties/_build/make_thumb.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

EP = Path(__file__).resolve().parents[1]
FONTS = EP.parents[3] / "projects" / "rank_scroll" / "assets" / "fonts"
PICKS = [("15_basmati.jpg", "BASMATI", "巴斯马蒂香米"), ("09_riceberry.jpg", "RICEBERRY", "紫莓香米"),
         ("20_camargue_red.jpg", "CAMARGUE RED", "卡马格红米"), ("29_wild_rice.jpg", "WILD RICE", "野米")]
W, H = 1280, 720


def font(name: str, size: int, zh: bool) -> ImageFont.FreeTypeFont:
    if zh:
        f = ImageFont.truetype(str(FONTS / "NotoSansSC-Variable.ttf"), size)
        try:
            f.set_variation_by_name("Black")
        except Exception:  # noqa: BLE001
            pass
        return f
    return ImageFont.truetype(str(FONTS / name), size)


def make(zh: bool, out: Path) -> None:
    im = Image.new("RGB", (W, H), (26, 18, 8))
    pw, gap, top = 300, 14, 236
    x0 = (W - 4 * pw - 3 * gap) // 2
    d = ImageDraw.Draw(im)
    for i, (f, en, cn) in enumerate(PICKS):
        p = ImageOps.fit(Image.open(EP / "assets/img" / f).convert("RGB"), (pw, H - top - 24), Image.LANCZOS, centering=(0.5, 0.5))
        mask = Image.new("L", p.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, *p.size), 22, fill=255)
        x = x0 + i * (pw + gap)
        im.paste(p, (x, top), mask)
        lab = cn if zh else en
        lf = font("Inter-ExtraBold.ttf", 30 if not zh else 32, zh)
        tw = d.textlength(lab, font=lf)
        d.rounded_rectangle((x + 14, H - 24 - 70, x + 14 + tw + 28, H - 24 - 22), 24, fill=(255, 176, 46))
        d.text((x + 28, H - 24 - 66), lab, font=lf, fill=(26, 18, 8))
        cf = font("Inter-Bold.ttf", 15, zh)
        chip = "AI图像" if zh else "AI IMAGE"
        cw = d.textlength(chip, font=cf)
        d.rounded_rectangle((x + pw - cw - 30, top + 12, x + pw - 12, top + 40), 10, fill=(255, 214, 0))
        d.text((x + pw - cw - 21, top + 15), chip, font=cf, fill=(26, 18, 8))
    title = "世界各地 30 种大米" if zh else "30 KINDS OF RICE"
    sub = "从软糯到松散，从白米到黑米" if zh else "AROUND THE WORLD · white, purple, red, black"
    tf = font("Inter-Black.ttf", 92 if not zh else 96, zh)
    d.text((W // 2, 92), title, font=tf, fill=(255, 255, 255), anchor="mm")
    sf = font("Inter-ExtraBold.ttf", 34 if not zh else 38, zh)
    d.text((W // 2, 176), sub, font=sf, fill=(255, 176, 46), anchor="mm")
    im.save(out)
    print(out)


if __name__ == "__main__":
    make(False, EP / "render" / "thumbnail.png")
    make(True, EP / "render" / "thumbnail_zh.png")
