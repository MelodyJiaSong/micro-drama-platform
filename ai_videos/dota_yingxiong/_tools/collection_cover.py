"""抖音合集「DotA英雄真人化」封面候选（3:4，1080×1440）。

    python ai_videos/dota_yingxiong/_tools/collection_cover.py

画面复用各英雄 demo 封面挑好的帧（demo_covers.FRAMES，取自成片，技能段裁掉原版技能图标），
输出 `ai_videos/dota_yingxiong/_assets/collection_cover/cover_{A,B,C}.png` 与对比图 `contact_sheet.jpg`。
  A 群像九宫格  B 单英雄大片（斧王）  C 近卫 VS 天灾（各五位）
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import demo_covers as dc  # noqa: E402

OUT = dc.DRAMA / "_assets" / "collection_cover"
W, H = 1080, 1440
GREEN, RED = dc.FACTION["近卫_sentinel"][1], dc.FACTION["天灾_scourge"][1]


def heroes() -> list[dict]:
    out = []
    for hero_dir in sorted(dc.CHARS.glob("*/*")):
        key = hero_dir.name.split("_")[0]
        if key not in dc.FRAMES or not (hero_dir / "demo" / "publish.md").is_file():
            continue
        info = dc.publish_info(hero_dir / "demo")
        sel = dc.FRAMES[key]
        vtag = info["video"].stem.split("_")[-1]
        fr = hero_dir / "demo" / "covers" / "frames"
        img = dc.frame(info["video"], sel["hero"], fr / f"{vtag}_{sel['hero']:.1f}.png")
        ult = dc.frame(info["video"], sel["ult"], fr / f"{vtag}_{sel['ult']:.1f}.png")
        out.append({"key": key, "faction": hero_dir.parent.name, "short": info["short"], "img": img, "ult": ult,
                    "hx": sel.get("hx", 0.5)})
    return out


def title(d, y, size=150):
    dc.txt(d, (W / 2, y), "DotA英雄", dc.font(size), fill=dc.GOLD, anchor="ma", stroke=4)
    dc.txt(d, (W / 2, y + size * 1.15), "真人化", dc.font(round(size * 0.72)), anchor="ma", stroke=3)


def v_grid(hs) -> Image.Image:
    im = Image.new("RGBA", (W, H), dc.INK + (255,))
    pick = [h for h in hs if h["key"] != "c3"][:9]          # 九宫格放九位
    g, top = 6, 470
    cw, ch = (W - 2 * g) // 3, (H - top - 2 * g) // 3
    for k, h in enumerate(pick):
        r, c = divmod(k, 3)
        x, y = c * (cw + g), top + r * (ch + g)
        im.alpha_composite(dc.cover(h["img"], cw, ch, h["hx"], 0.35), (x, y))
        im.alpha_composite(dc.grad(cw, 120, 0, 210), (x, y + ch - 120))
        d = ImageDraw.Draw(im)
        dc.txt(d, (x + 16, y + ch - 18), h["short"], dc.fit(d, h["short"], cw - 32, 46), anchor="ls", stroke=2)
    im.alpha_composite(dc.grad(W, 160, 255, 0, dc.INK), (0, top))
    d = ImageDraw.Draw(im)
    pw, _ = dc.pill(d, W / 2, 50, "DotA 1 · 魔兽争霸3", 40, center=True)
    title(d, 130)
    return im.convert("RGB")


def v_hero(hs) -> Image.Image:
    axe = next(h for h in hs if h["key"] == "c65")
    im = dc.cover(axe["img"], W, H, 0.5, 0.3)
    im.alpha_composite(dc.grad(W, 220, 200, 0), (0, 0))
    im.alpha_composite(dc.grad(W, 720, 0, 240), (0, H - 720))
    d = ImageDraw.Draw(im)
    dc.pill(d, W / 2, 60, "DotA 1 · 魔兽争霸3", 40, center=True)
    title(d, H - 600, 170)                       # 标题压在下方，不挡斧王的脸
    line = "近卫 · 天灾 英雄技能全还原"
    dc.txt(d, (W / 2, H - 150), line, dc.fit(d, line, W - 120, 66), anchor="ms", stroke=2)
    dc.txt(d, (W / 2, H - 70), "持续更新 · 下一个做谁？", dc.font(46, 700), fill=dc.GOLD, anchor="ms", stroke=2)
    return im.convert("RGB")


def v_versus(hs) -> Image.Image:
    im = Image.new("RGBA", (W, H), dc.INK + (255,))
    sent = [h for h in hs if h["faction"] == "近卫_sentinel"][:5]
    scou = [h for h in hs if h["faction"] == "天灾_scourge"][:5]
    top, g = 360, 6
    cw = (W - g) // 2
    ch = (H - top - g * 4) // 5
    for col, (group, colr) in enumerate(((sent, GREEN), (scou, RED))):
        x = col * (cw + g)
        for r, h in enumerate(group):
            y = top + r * (ch + g)
            im.alpha_composite(dc.cover(h["ult"], cw, ch, 0.5, 0.4), (x, y))
            im.alpha_composite(dc.grad(cw, ch, 0, 150), (x, y))
            d = ImageDraw.Draw(im)
            d.rectangle((x, y, x + 8, y + ch), fill=colr) if col == 0 else d.rectangle((x + cw - 8, y, x + cw, y + ch), fill=colr)
            anchor, tx = ("ls", x + 24) if col == 0 else ("rs", x + cw - 24)
            dc.txt(d, (tx, y + ch - 16), h["short"], dc.fit(d, h["short"], cw - 60, 52), anchor=anchor, stroke=2)
    d = ImageDraw.Draw(im)
    dc.pill(d, cw / 2, top - 76, "近卫", 46, bg=GREEN, fg=dc.WHITE, center=True)
    dc.pill(d, cw + g + cw / 2, top - 76, "天灾", 46, bg=RED, fg=dc.WHITE, center=True)
    dc.txt(d, (W / 2, 40), "DotA英雄真人化", dc.fit(d, "DotA英雄真人化", W - 100, 130), fill=dc.GOLD, anchor="ma", stroke=4)
    dc.txt(d, (W / 2, 205), "四个技能全还原", dc.font(54, 800), anchor="ma", stroke=2)
    vs = dc.font(150)
    d.ellipse((W / 2 - 105, top + (H - top) / 2 - 105, W / 2 + 105, top + (H - top) / 2 + 105), fill=dc.INK, outline=dc.GOLD, width=8)
    d.text((W / 2, top + (H - top) / 2), "VS", font=dc.font(110), fill=dc.GOLD, anchor="mm")
    return im.convert("RGB")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    hs = heroes()
    variants = {"A_grid": v_grid(hs), "B_hero": v_hero(hs), "C_versus": v_versus(hs)}
    for name, im in variants.items():
        im.save(OUT / f"cover_{name}.png", optimize=True)
    tw, th, pad = 360, 480, 20
    sheet = Image.new("RGB", (pad + 3 * (tw + pad), th + 2 * pad + 40), (235, 237, 241))
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(variants.items()):
        x = pad + i * (tw + pad)
        sheet.paste(im.resize((tw, th)), (x, pad))
        d.text((x + tw / 2, pad + th + 22), name.split("_")[0], font=dc.font(30, 800), fill=(30, 30, 30), anchor="mm")
    sheet.save(OUT / "contact_sheet.jpg", quality=90)
    print("\n".join(str(OUT / f"cover_{n}.png") for n in variants))


if __name__ == "__main__":
    main()
