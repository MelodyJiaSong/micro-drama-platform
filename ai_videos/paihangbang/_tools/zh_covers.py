"""每期三张中文封面候选，三种尺寸：16:9（1920×1080，随片）、4:3 横屏（1440×1080）、3:4 竖屏（1080×1440）。

    python ai_videos/paihangbang/_tools/zh_covers.py [ep13_tallest_statues ...]

输出 `episodes/<期>/render/covers_zh/cover_zh_{1,2,3}{,_4x3,_3x4}.png`：
  1 冠军大图：第 1 名实拍铺满 + 题目 + 第 1 名数值（标题写「第1名你猜对了吗」的期不剧透，改成悬念）
  2 柱状对比：前 5 名做成高低不同的照片柱，按数值比例
  3 悬念大字：大号 TOP N + 题目 + 「第1名你猜得到吗？」，右侧 2–5 名四宫格
图片只取稳妥版能用的（load_episode 默认不放风险图）；AI 图角上标「AI图像」，与片中一致。
没有可用照片的期（ep06 封面全部扣下）自动改成纯文字版式。字体 Noto Sans SC（SIL OFL）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SERIES = Path(__file__).resolve().parents[1]
REPO = SERIES.parents[1]
sys.path.insert(0, str(REPO / "projects" / "rank_scroll"))
from rank_scroll.contract import Episode, Item, load_episode  # noqa: E402

FONT = REPO / "projects" / "rank_scroll" / "assets" / "fonts" / "NotoSansSC-Variable.ttf"
W, H = 1920, 1080
GOLD = (245, 184, 46)
NAVY = (14, 20, 34)
WHITE = (255, 255, 255)
AIY = (255, 214, 0)
_fonts: dict = {}


def font(size: int, weight: int = 900) -> ImageFont.FreeTypeFont:
    key = (int(size), weight)
    if key not in _fonts:
        f = ImageFont.truetype(str(FONT), int(size))
        try:
            f.set_variation_by_axes([weight])
        except (OSError, ValueError):
            pass
        _fonts[key] = f
    return _fonts[key]


def fit(d: ImageDraw.ImageDraw, s: str, max_w: float, size: int, weight: int = 900, min_size: int = 28):
    while size > min_size and d.textlength(s, font=font(size, weight)) > max_w:
        size -= 4
    return font(size, weight)


def cover(img: Image.Image, w: int, h: int, focus=(0.5, 0.4)) -> Image.Image:
    s = max(w / img.width, h / img.height)
    im = img.resize((max(w, round(img.width * s)), max(h, round(img.height * s))), Image.LANCZOS)
    x = round((im.width - w) * focus[0])
    y = round((im.height - h) * focus[1])
    return im.crop((x, y, x + w, y + h))


def photo(it: Item, w: int, h: int) -> Image.Image:
    return cover(Image.open(it.image).convert("RGB"), w, h, it.image_focus).convert("RGBA")


def grad(w: int, h: int, a0: int, a1: int, color=NAVY, horizontal=False) -> Image.Image:
    n = w if horizontal else h
    g = Image.new("L", (n, 1))
    for i in range(n):
        g.putpixel((i, 0), round(a0 + (a1 - a0) * i / max(n - 1, 1)))
    g = g.resize((w, h)) if horizontal else g.rotate(-90, expand=True).resize((w, h))
    layer = Image.new("RGBA", (w, h), color + (0,))
    layer.putalpha(g)
    return layer


def txt(d, xy, s, f, fill=WHITE, anchor="la", stroke=0, shadow=True):
    if shadow:
        d.text((xy[0] + 5, xy[1] + 7), s, font=f, fill=(0, 0, 0, 160), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, 160))
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0))


def pill(d, x, y, s, size=56, bg=GOLD, fg=NAVY, center=False):
    f = font(size)
    pw, ph = d.textlength(s, font=f) + size * 0.9, size * 1.45
    if center:
        x -= pw / 2
    d.rounded_rectangle((x, y, x + pw, y + ph), radius=ph * 0.28, fill=bg)
    d.text((x + pw / 2, y + ph / 2), s, font=f, fill=fg, anchor="mm")
    return pw, ph


def ai_chip(d, x, y, size=30):
    pill(d, x, y, "AI 生成图", size, bg=AIY, fg=(20, 20, 20))   # 与卡面 i18n ai_image 一致


def flag(ep: Episode, it: Item, h: int) -> Image.Image | None:
    if not ep.show_flags or not it.country_iso2:
        return None
    p = ep.flag_path(it.country_iso2)
    if not p.is_file():
        return None
    f = Image.open(p).convert("RGBA")
    return f.resize((round(f.width * h / f.height), h), Image.LANCZOS)


def lines(title: str) -> list[str]:
    """长题目断成两行：优先断在「的」后，否则对半。"""
    if len(title) <= 8:
        return [title]
    mid = len(title) // 2
    cands = [i + 1 for i, ch in enumerate(title) if ch == "的" and 3 <= i + 1 <= len(title) - 3]
    cut = min(cands, key=lambda i: abs(i - mid)) if cands else mid
    return [title[:cut], title[cut:]]


OV: dict = {}   # 每期封面覆盖（<期>/zh_publish.json 的 cover_* 字段；paihangbang follow-up 067）


def top_items(ep: Episode, n: int, with_image: bool = False, start_rank: int = 1) -> list[Item]:
    if OV.get("cover_ranks"):                  # 列表期按指定顺序挑卡（如 ep21 大米挑白 / 紫 / 红 / 黑）
        by = {i.rank: i for i in ep.items}
        picks = [by[r] for r in OV["cover_ranks"] if r in by and (not with_image or by[r].image)]
        return picks[(1 if start_rank > 1 else 0):][:n]
    seen, out = set(), []
    for it in sorted(ep.items, key=lambda i: (i.rank, i.image is None)):
        if it.rank < start_rank or it.name in seen or (with_image and not it.image):
            continue
        seen.add(it.name)
        out.append(it)
        if len(out) == n:
            break
    return out


def kicker(ep: Episode) -> str:
    return ep.kicker.replace("TOP ", "TOP")


# 尺寸：16:9 横屏（随片）、4:3 横屏、3:4 竖屏（抖音上传页的横 / 竖封面）
FORMATS = {"": (1920, 1080), "_4x3": (1440, 1080), "_3x4": (1080, 1440)}


def portrait() -> bool:
    return H > W


# ---------- 1 冠军大图 ----------
def v_hero(ep: Episode, spoil: bool) -> Image.Image:
    champ = top_items(ep, 1)[0]
    bg_item = champ if champ.image else next(iter(top_items(ep, 1, with_image=True)), None)
    if bg_item and (champ.image or not spoil):
        im = photo(bg_item, W, H)
        if not spoil:
            im = im.filter(ImageFilter.GaussianBlur(28))
    else:
        im = Image.new("RGBA", (W, H), NAVY + (255,))
    if portrait():
        im.alpha_composite(grad(W, int(H * 0.62), 235, 0), (0, 0))
        im.alpha_composite(grad(W, 420, 0, 225), (0, H - 420))
        tw = W - 2 * 80
    else:
        im.alpha_composite(grad(int(W * 0.68), H, 235, 0, horizontal=True), (0, 0))
        im.alpha_composite(grad(W, 300, 0, 200), (0, H - 300))
        tw = int(W * 0.56)
    d = ImageDraw.Draw(im)
    x = 80 if portrait() else 96
    pill(d, x, 90, kicker(ep), 60)
    y = 210
    for ln in lines(ep.title):
        f = fit(d, ln, tw, 150)
        txt(d, (x, y), ln, f)
        y += f.size * 1.18
    y += 30
    if spoil and not ep.is_list:
        if portrait():                      # 竖屏：冠军名与数值放到底部，中间留给照片
            y = H - 470
        txt(d, (x, y), "第1名", font(64), fill=GOLD)
        fl = flag(ep, champ, 56)
        nx = x + d.textlength("第1名", font=font(64)) + 24
        if fl:
            im.alpha_composite(fl, (int(nx), int(y + 14)))
            nx += fl.width + 18
        txt(d, (nx, y), champ.name, fit(d, champ.name, x + tw + 40 - nx, 64))
        txt(d, (x - 6, y + 90), champ.value_display, fit(d, champ.value_display, tw + 20, 220), fill=GOLD, stroke=3)
    elif ep.is_list:
        sub = OV.get("cover_sub", "估值、融资一次看完")
        txt(d, (x, y), sub, fit(d, sub, tw, 72), fill=GOLD)
    else:
        txt(d, (x, y), "第1名是？", font(150), fill=GOLD, stroke=3)
    if bg_item and bg_item is champ and champ.image_ai and spoil:
        ai_chip(d, W - 220, 50)
    return im.convert("RGB")


def _bar_photo(it: Item, w: int, h: int, hide: bool, horizontal=False) -> Image.Image:
    if it.image and not hide:
        col = photo(it, w, h)
        col.alpha_composite(grad(w, h, 0, 160, (0, 0, 0), horizontal=horizontal))
    else:
        col = Image.new("RGBA", (w, h), (34, 44, 66, 255))
    return col


def _stripes(d: ImageDraw.ImageDraw) -> None:
    for yy in range(0, H, 6):
        d.line((0, yy, W, yy), fill=(19, 26, 41, 255))


# ---------- 2 柱状对比 ----------
def v_bars(ep: Episode, spoil: bool) -> Image.Image:
    if portrait():
        return v_bars_rows(ep, spoil)
    im = Image.new("RGBA", (W, H), NAVY + (255,))
    d = ImageDraw.Draw(im)
    _stripes(d)
    items = top_items(ep, 5)
    base, top_max = H - 150, 340                    # 最高柱的名次牌落在 y≈250，题目在其上方
    gap = 34 if W > 1600 else 24
    bw = (W - 160 - gap * (len(items) - 1)) // len(items)
    pw, _ = pill(d, 80, 60, kicker(ep), 52)
    tx = 80 + pw + 40
    txt(d, (tx, 52), ep.title, fit(d, ep.title, W - 80 - tx, 104), shadow=False)
    vmax = max(it.value for it in items)
    order = list(reversed(items)) if not ep.is_list else items      # 第 5 名在左、第 1 名在右
    for i, it in enumerate(order):
        x = 80 + i * (bw + gap)
        if ep.is_list or vmax <= 0:
            top = top_max + 60
        else:                                   # 按数值真实比例（不放大差距），最矮留 40%
            r = max(it.value / vmax, 0.4)
            top = round(base - (base - top_max) * r)
        bh = base - top
        hide = (not spoil) and it.rank == 1 and not ep.is_list
        col = _bar_photo(it, bw, bh, hide)
        mask = Image.new("L", (bw, bh), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, bw - 1, bh + 30), radius=26, fill=255)
        im.paste(col, (x, top), mask)
        if hide:
            d.text((x + bw / 2, top + bh / 2), "？", font=font(220), fill=GOLD, anchor="mm")
        elif not it.image:
            d.text((x + bw / 2, top + bh / 2), it.name[:6], font=fit(d, it.name[:6], bw - 40, 64), fill=(200, 208, 224), anchor="mm")
        if it.image and it.image_ai and not hide:
            ai_chip(d, x + 16, top + 16, 26)
        if not ep.is_list:
            pill(d, x + bw / 2, top - 92, f"第{it.rank}名", 44, bg=GOLD if it.rank == 1 else (232, 236, 244), center=True)
        val = "？？" if hide else it.value_display
        txt(d, (x + bw / 2, top + bh - 30), val, fit(d, val, bw - 24, 64, min_size=20), anchor="ms", stroke=2)
        name = "你猜对了吗" if hide else it.name
        fl = flag(ep, it, 40) if not hide else None
        nf = fit(d, name, bw - (fl.width + 16 if fl else 10), 46, 800, min_size=18)
        nw = d.textlength(name, font=nf) + ((fl.width + 12) if fl else 0)
        nx = x + (bw - nw) / 2
        if fl:
            im.alpha_composite(fl, (int(nx), base + 42))
            nx += fl.width + 12
        txt(d, (nx, base + 30), name, nf, shadow=False)
    return im.convert("RGB")


def v_bars_rows(ep: Episode, spoil: bool) -> Image.Image:
    """竖屏版柱状对比：第 1 名在上的横向照片条，条长按数值比例。"""
    im = Image.new("RGBA", (W, H), NAVY + (255,))
    d = ImageDraw.Draw(im)
    _stripes(d)
    items = top_items(ep, 5)
    x0 = 70
    pill(d, x0, 70, kicker(ep), 56)
    y = 190
    for ln in lines(ep.title):
        f = fit(d, ln, W - 2 * x0, 130)
        txt(d, (x0, y), ln, f, shadow=False)
        y += f.size * 1.18
    top = max(int(y) + 50, 500)
    rh = 168
    gap = (H - 70 - top - rh * len(items)) // max(len(items) - 1, 1)
    full = W - 2 * x0
    vmax = max(it.value for it in items)
    for i, it in enumerate(items):
        ry = top + i * (rh + gap)
        r = 1.0 if ep.is_list or vmax <= 0 else max(it.value / vmax, 0.45)
        bw = round(full * r)
        hide = (not spoil) and it.rank == 1 and not ep.is_list
        col = _bar_photo(it, bw, rh, hide, horizontal=True)
        mask = Image.new("L", (bw, rh), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, bw - 1, rh - 1), radius=22, fill=255)
        im.paste(col, (x0, ry), mask)
        lw = 0
        if not ep.is_list:                      # 名次牌在条的左上角，名字紧跟其后同一行
            lab = f"第{it.rank}名"
            lw = d.textlength(lab, font=font(42)) + 36
            d.rounded_rectangle((x0, ry, x0 + lw, ry + 70), radius=18, fill=GOLD if it.rank == 1 else (232, 236, 244))
            d.text((x0 + lw / 2, ry + 35), lab, font=font(42), fill=NAVY, anchor="mm")
        if it.image and it.image_ai and not hide:
            ai_chip(d, x0 + bw - 150, ry + 12, 24)
        if hide:
            d.text((x0 + bw / 2, ry + rh / 2 + 6), "？", font=font(120), fill=GOLD, anchor="mm")
            txt(d, (x0 + lw + 18, ry + 35), "你猜对了吗", font(46, 800), anchor="lm")
            continue
        nx = x0 + lw + 18
        fl = flag(ep, it, 38)
        name_room = (x0 + max(bw, full * 0.62)) - nx - 20 - (fl.width + 12 if fl else 0)   # 条短时名字可伸出条外
        nf = fit(d, it.name, name_room, 50, 800, min_size=24)
        if fl:
            im.alpha_composite(fl, (int(nx), int(ry + 35 - fl.height / 2)))
            nx += fl.width + 12
        txt(d, (nx, ry + 35), it.name, nf, anchor="lm", stroke=2)
        val = it.value_display
        txt(d, (x0 + bw - 22, ry + rh - 18), val, fit(d, val, bw - 44, 72, min_size=24), anchor="rs", stroke=2)
    return im.convert("RGB")


# ---------- 3 悬念大字 ----------
def _grid(im: Image.Image, ep: Episode, gx: int, gy: int, gw: int, gh: int) -> None:
    g = 6
    cw, ch = (gw - g) // 2, (gh - g) // 2
    grid = top_items(ep, 4, with_image=True, start_rank=2)
    d = ImageDraw.Draw(im)
    if grid:
        for k, it in enumerate(grid):
            r, c = divmod(k, 2)
            x, y = gx + c * (cw + g), gy + r * (ch + g)
            im.alpha_composite(photo(it, cw, ch), (x, y))
            gh2 = min(170, ch)
            im.alpha_composite(grad(cw, gh2, 0, 210, (0, 0, 0)), (x, y + ch - gh2))
            d = ImageDraw.Draw(im)
            if not ep.is_list:
                pill(d, x + 22, y + 22, f"第{it.rank}名", 36)
            if it.image_ai:
                ai_chip(d, x + cw - 150, y + 22, 26)
            txt(d, (x + 26, y + ch - 30), it.name, fit(d, it.name, cw - 52, 50, 800, min_size=20), anchor="ls")
    else:                                                           # 没有可用照片：文字格
        for k, it in enumerate(top_items(ep, 4, start_rank=2)):
            r, c = divmod(k, 2)
            x, y = gx + c * (cw + g), gy + r * (ch + g)
            d.rectangle((x, y, x + cw, y + ch), fill=(28 + 8 * k, 38 + 6 * k, 60 + 6 * k))
            d.text((x + cw / 2, y + ch / 2 - 60), f"第{it.rank}名", font=font(46), fill=GOLD, anchor="mm")
            d.text((x + cw / 2, y + ch / 2 + 10), it.name, font=fit(d, it.name, cw - 60, 70), fill=WHITE, anchor="mm")
            d.text((x + cw / 2, y + ch / 2 + 90), it.value_display, font=font(46, 700), fill=(200, 208, 224), anchor="mm")


def v_teaser(ep: Episode, spoil: bool) -> Image.Image:
    im = Image.new("RGBA", (W, H), NAVY + (255,))
    is_top = ep.kicker.upper().startswith("TOP")
    num = ep.kicker.split()[-1] if is_top else str(len({i.name for i in ep.items}))
    hook = OV.get("cover_hook", "看看都有谁？") if ep.is_list else "第1名你猜得到吗？"
    tl = lines(ep.title)
    if portrait():                              # 竖屏：上半 TOP + 大数字 + 题目 + 钩子，下半四宫格
        d = ImageDraw.Draw(im)
        txt(d, (80, 60), "TOP" if is_top else "盘点", font(100), shadow=False)
        nf = font(300)
        txt(d, (70, 120), num, nf, fill=GOLD, shadow=False)
        pill(d, 80 + d.textlength(num, font=nf) + 50, 300, hook, 52)
        y = 520
        for ln in tl:
            f = fit(d, ln, W - 160, 120 if len(tl) == 1 else 100)
            txt(d, (80, y), ln, f, shadow=False)
            y += f.size * 1.2
        gy = int(y) + 40
        _grid(im, ep, 0, gy, W, H - gy)
        return im.convert("RGB")
    gx = W // 2
    _grid(im, ep, gx, 0, W - gx, H)
    d = ImageDraw.Draw(im)
    txt(d, (90, 70), "TOP" if is_top else "盘点", font(110), shadow=False)
    txt(d, (80, 150), num, font(400 if W > 1600 else 340), fill=GOLD, shadow=False)
    y = 650 if len(tl) == 1 else 610
    for ln in tl:
        f = fit(d, ln, gx - 90 - 50, 104 if len(tl) == 1 else 92)
        txt(d, (90, y), ln, f, shadow=False)
        y += f.size * 1.22
    hsize = 58 if len(tl) == 1 else 50
    while d.textlength(hook, font=font(hsize)) + hsize * 0.9 > gx - 130:
        hsize -= 4
    pill(d, 90, max(y + 34, 900), hook, hsize)
    return im.convert("RGB")


def make(ep_dir: Path) -> list[Path]:
    global W, H, OV
    ep, _ = load_episode(ep_dir, lang="zh")
    ovp = ep_dir / "zh_publish.json"
    OV = json.loads(ovp.read_text(encoding="utf-8")) if ovp.is_file() else {}
    pub = (ep_dir / "publish.zh.md").read_text(encoding="utf-8") if (ep_dir / "publish.zh.md").is_file() else ""
    douyin = pub.split("## 抖音", 1)[-1]
    title = douyin.split("```text", 1)[-1].split("```", 1)[0] if "```text" in douyin else ""
    spoil = "你猜" not in title          # 抖音标题写「第1名你猜对了吗」的期，封面也不剧透
    out = ep_dir / "render" / "covers_zh"
    out.mkdir(parents=True, exist_ok=True)
    paths = []
    for suffix, (W, H) in FORMATS.items():
        for k, fn in enumerate((v_hero, v_bars, v_teaser), 1):
            p = out / f"cover_zh_{k}{suffix}.png"
            fn(ep, spoil).save(p, optimize=True)
            paths.append(p)
    W, H = FORMATS[""]
    return paths


def main() -> None:
    names = sys.argv[1:]
    eps = sorted(p for p in (SERIES / "episodes").iterdir() if (p / "data.zh.json").is_file()
                 and (not names or p.name in names or p.name.split("_")[0] in names))
    for ep_dir in eps:
        make(ep_dir)
        print("ok", ep_dir.name)


if __name__ == "__main__":
    main()
