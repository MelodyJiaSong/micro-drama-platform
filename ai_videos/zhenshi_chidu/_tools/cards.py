"""真实尺度 · 叠加层（bible §2.2 / §2.4）：标签卡、人体参照标签、钩子、片头、洞察、来源卡。全部 1920×1080 RGBA PNG。

    python ai_videos/zhenshi_chidu/_tools/cards.py <集目录>

读 <集目录>/data.json 与 sources.md（来源卡用），写 <集目录>/_build/cards/。
字体 Inter（SIL OFL 1.1，projects/rank_scroll/assets/fonts/）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO = Path(__file__).resolve().parents[3]
FONTS = REPO / "projects" / "rank_scroll" / "assets" / "fonts"
W, H = 1920, 1080
ACCENT = (255, 196, 0, 255)
WHITE = (255, 255, 255, 255)
GREY = (200, 204, 210, 255)
PANEL = (16, 20, 26, 205)


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / f"Inter-{weight}.ttf"), size)


def _canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def _shadowed_panel(im: Image.Image, box: tuple[int, int, int, int], radius: int = 22) -> None:
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((box[0] + 6, box[1] + 8, box[2] + 6, box[3] + 8), radius, fill=(0, 0, 0, 110))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(im).rounded_rectangle(box, radius, fill=PANEL)


def _tw(d: ImageDraw.ImageDraw, text: str, f) -> int:
    return int(d.textlength(text, font=f))


def label_card(it: dict, n_total: int) -> Image.Image:
    im, d = _canvas()
    x0, y0 = 60, 770
    f_rank, f_name, f_sci = font("Black", 60), font("ExtraBold", 54), font("Medium", 29)
    f_val, f_imp, f_meta, f_src = font("Black", 70), font("Bold", 34), font("Medium", 29), font("Medium", 25)
    rank = f"{'=' if it['tied'] else '#'}{it['rank']}"
    name_w = _tw(d, it["name"], f_name)
    val_w = _tw(d, it["value_display"], f_val) + 24 + _tw(d, it["secondary_display"], f_imp)
    meta = f"{it['basis'].capitalize()}  ·  {it['region']}"
    rank_w = max(_tw(d, rank, f_rank), 120)
    tag_w = 150 if it.get("model") and it["model"].get("ai_model") else 0   # 右上角 AI 标签占位
    inner = max(rank_w + 28 + name_w + tag_w, val_w, _tw(d, meta, f_meta), _tw(d, "Source: " + it["source_short"], f_src), 560)
    box = (x0, y0, x0 + inner + 76, y0 + 286)
    _shadowed_panel(im, box)
    cx, cy = x0 + 38, y0 + 26
    d.text((cx, cy - 4), rank, font=f_rank, fill=ACCENT)
    d.text((cx + rank_w + 28, cy + 4), it["name"], font=f_name, fill=WHITE)
    d.text((cx + rank_w + 30, cy + 66), it["scientific_name"], font=f_sci, fill=GREY)
    d.text((cx, cy + 92), it["value_display"], font=f_val, fill=WHITE)
    d.text((cx + _tw(d, it["value_display"], f_val) + 24, cy + 130), it["secondary_display"], font=f_imp, fill=GREY)
    d.text((cx, cy + 176), meta, font=f_meta, fill=GREY)
    d.text((cx, cy + 214), "Source: " + it["source_short"], font=f_src, fill=(160, 166, 175, 255))
    if it.get("model", {}) and it["model"].get("ai_model"):
        tag, f_tag = ("AI IMAGE" if it.get("cutout") else "AI MODEL"), font("ExtraBold", 22)
        tw = _tw(d, tag, f_tag)
        bx1 = box[2] - 22
        d.rounded_rectangle((bx1 - tw - 28, y0 + 22, bx1, y0 + 58), 8, fill=ACCENT)
        d.text((bx1 - tw - 14, y0 + 27), tag, font=f_tag, fill=(20, 20, 20, 255))
    return im


def man_label() -> Image.Image:
    """人体参照标签（小图，叠加位置由 timeline.json 给出：底边中点对准人头顶上方）。"""
    f = font("Bold", 26)
    text = "1.75 m man"
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    tw = _tw(tmp, text, f)
    im = Image.new("RGBA", (tw + 36, 62), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, tw + 36, 44), 10, fill=(16, 20, 26, 200))
    d.text((18, 7), text, font=f, fill=WHITE)
    cx = (tw + 36) // 2
    d.polygon([(cx - 10, 44), (cx + 10, 44), (cx, 60)], fill=(16, 20, 26, 200))
    return im


def _center(d, text, f, y, fill=WHITE):
    d.text(((W - _tw(d, text, f)) // 2, y), text, font=f, fill=fill)


def hook_card(data: dict) -> Image.Image:
    im, d = _canvas()
    _shadowed_panel(im, (W // 2 - 820, 50, W // 2 + 820, 270), 28)   # 日落天空很亮：白字要有底板
    _center(d, "Which giant stands tallest?", font("Black", 96), 70)
    _center(d, "30 of the largest land animals  ·  true scale  ·  next to a 1.75 m man", font("Bold", 36), 200, WHITE)
    return im


def title_card(data: dict) -> Image.Image:
    # 放在画面下 1/3 的地面上（第 6 轮审片：原居中的卡盖住参照人和扭角羚）；扭角羚标签卡在本卡淡出后才出现，同一位置不冲突
    im, d = _canvas()
    _shadowed_panel(im, (300, 772, 1620, 1050), 28)
    _center(d, data["kicker"], font("ExtraBold", 32), 790, ACCENT)
    _center(d, "The 30 Largest Land Animals", font("Black", 70), 830)
    _center(d, "ranked by shoulder height  ·  next to a 1.75 m man", font("Bold", 38), 922)
    _center(d, data["period_label"], font("Medium", 28), 985, (160, 166, 175, 255))
    return im


def group_card() -> Image.Image:
    im, d = _canvas()
    _shadowed_panel(im, (W // 2 - 760, 30, W // 2 + 760, 190), 24)   # 第 4 轮审片：白字压在浅蓝天上看不清
    _center(d, "All 30 together, true scale", font("Black", 64), 48)
    _center(d, "smallest in front, tallest at the back  ·  1.75 m man front left", font("Bold", 30), 130, WHITE)
    return im


def insight_card(text: str) -> Image.Image:
    im, d = _canvas()
    f = font("ExtraBold", 46)        # 两行放得下，卡高 ≤ 约 260 px，压在脚线以下的地面上
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if _tw(d, t, f) > 1480 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = t
    lines.append(cur)
    h = 76 + 60 * len(lines) + 56
    y0 = H - h - 24          # 下 1/3 地面上（第 6 轮审片：居中会盖住动物）；洞察卡只出现在标签卡淡出后
    _shadowed_panel(im, (180, y0, W - 180, y0 + h), 28)
    _center(d, "DID YOU KNOW?", font("ExtraBold", 30), y0 + 28, ACCENT)
    for i, ln in enumerate(lines):
        _center(d, ln, f, y0 + 78 + 60 * i)
    return im


def sources_card(data: dict, music_credit: str) -> Image.Image:
    im = Image.new("RGBA", (W, H), (14, 17, 22, 255))
    d = ImageDraw.Draw(im)
    d.text((110, 70), "SOURCES & CREDITS", font=font("Black", 50), fill=ACCENT)
    f, fb = font("Medium", 24), font("Bold", 26)
    srcs: dict[str, list[str]] = {}
    for it in data["items"]:
        srcs.setdefault(it["source_short"], []).append(it["name"])
    col_x, y, x = [110, 1000], 160, 0
    d.text((col_x[0], y), "Shoulder heights (typical adults, males where data allow; full citations with links in the pinned comment):", font=fb, fill=WHITE)
    y += 44
    y_start = y
    for s, names in sorted(srcs.items(), key=lambda kv: -len(kv[1])):
        line = f"{s}: " + ", ".join(names)
        wrapped, cur = [], ""
        for w in line.split(" "):
            t = (cur + " " + w).strip()
            if _tw(d, t, f) > 830 and cur:
                wrapped.append(cur)
                cur = "    " + w
            else:
                cur = t
        wrapped.append(cur)
        if y + 33 * len(wrapped) > 700 and x == 0:
            x, y = 1, y_start
        for ln in wrapped:
            d.text((col_x[x], y), ln, font=f, fill=GREY)
            y += 33
        y += 8
    y = 800
    cut = any(it.get("cutout") for it in data["items"])
    credit = [
        "Animals and the 1.75 m man: AI-generated images made for this video, cut out and scaled by script to the heights shown.",
        "Landscape backdrop and acacias: AI-generated for this video. Poly Haven (CC0): HDRIs Mpumalanga Veld (G. Zaal), Plains Sunset (D. Savva & J. Guest);",
        "Grass Ground (C. Baglioni); grass and rock models by R. Cilliers, R. Tuytel, G. Zaal, J. van Heerden.",
    ] if cut else [
        "3D animals: AI-generated for this video (reference images made with AI, converted to 3D with TripoSR, MIT license),",
        "scaled by script to the shoulder height shown. Human reference: MakeHuman / MPFB base mesh (CC0), 1.75 m.",
    ]
    for ln in credit + [
        music_credit + "  Font: Inter (SIL Open Font License 1.1).",
        data["scope_note"].split(";")[0] + ".",
    ]:
        d.text((110, y), ln, font=f, fill=GREY)
        y += 34
    return im


def main() -> None:
    ep = Path(sys.argv[1]).resolve()
    music = sys.argv[2] if len(sys.argv) > 2 else "Music: original instrumental generated for this channel with Suno."
    data = json.loads((ep / "data.json").read_text(encoding="utf-8"))
    out = ep / "_build" / "cards"
    out.mkdir(parents=True, exist_ok=True)
    n = len(data["items"])
    for i, it in enumerate(data["items"]):
        label_card(it, n).save(out / f"label_{i:02d}.png")   # i = data.json 中的序号（肩高从高到低）
    man_label().save(out / "man_label.png")
    hook_card(data).save(out / "hook.png")
    title_card(data).save(out / "title.png")
    group_card().save(out / "group.png")
    for i, ins in enumerate(data["insights"]):
        insight_card(ins["text"]).save(out / f"insight_{i}.png")
    sources_card(data, music).save(out / "sources.png")
    print("cards ->", out)


if __name__ == "__main__":
    main()
