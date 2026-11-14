"""英雄 demo 中文封面：每个英雄 4:3 横屏（1440×1080）与 3:4 竖屏（1080×1440）各三款。

    python ai_videos/dota_yingxiong/_tools/demo_covers.py [c42 c41 ...]

  ① 英雄大图：成片里的英雄主画面铺满 + 「DotA ×× 真人化」+ 抖音标题的钩子句
  ② 四技能：四个技能各取一帧，2×2 拼图，标技能中文名与快捷键
  ③ 大招特写：大招那一帧铺满 + 大号大招名

画面全部从该英雄 `demo/publish.md` 头部写的成片（edit/final/ep01_final_vN.mp4）按 FRAMES 里的秒数抽帧；
片内左上角的 DotA 原版技能图标（暴雪美术）不进封面（技能段的帧先裁掉最左一条）。文字从 publish.md 读：抖音标题（英雄简称、钩子句）、
B站简介的章节行（技能名与快捷键）、YouTube 标题（英文名）。输出 `demo/covers/cover_{1,2,3}_{4x3,3x4}.png`，
抽出的帧在 `demo/covers/frames/`。字体 Noto Sans SC（SIL OFL）。成片换版本后检查 FRAMES 秒数再重跑。
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

DRAMA = Path(__file__).resolve().parents[1]
REPO = DRAMA.parents[1]
CHARS = DRAMA / "2_世界观人设" / "characters"
FONT = REPO / "projects" / "rank_scroll" / "assets" / "fonts" / "NotoSansSC-Variable.ttf"
GOLD = (240, 184, 72)
INK = (12, 14, 20)
WHITE = (255, 255, 255)
FACTION = {"近卫_sentinel": ("近卫", (86, 170, 96)), "天灾_scourge": ("天灾", (196, 62, 58))}
FORMATS = {"4x3": (1440, 1080), "3x4": (1080, 1440)}
ICON_BOX = (18, 20, 160, 160)          # 1280×720 成片左上角技能图标（含边框）
INTRO_S = 12.0                          # 亮相段长度：之后各技能段都带图标

# 每个英雄挑的帧（秒，按 publish.md 头部的定版成片）：hero 英雄大图、ult 大招、skills 四技能；
# hx / ux：英雄大图 / 大招裁切时的水平取景（0 = 最左，0.5 = 居中，缺省居中），人物不在画面中间时用
FRAMES = {
    "c60": {"hero": 41.0, "hx": 0.3, "ult": 62.8, "skills": [15.1, 27.4, 42.8, 62.8]},
    "c63": {"hero": 46.4, "hx": 0.35, "ult": 57.7, "skills": [17.1, 29.5, 43.6, 57.7]},
    "c65": {"hero": 64.0, "ult": 60.8, "skills": [15.1, 30.5, 46.1, 60.8]},
    "c75": {"hero": 17.1, "ult": 59.7, "skills": [19.3, 30.3, 47.0, 59.7]},
    "c86": {"hero": 63.4, "ult": 60.8, "skills": [20.6, 28.9, 45.6, 60.8]},
    "c2": {"hero": 61.7, "ult": 59.1, "skills": [18.4, 29.6, 43.4, 59.1]},
    "c3": {"hero": 21.9, "ult": 64.0, "skills": [21.9, 33.1, 39.7, 64.0]},
    "c40": {"hero": 63.1, "ult": 54.1, "skills": [16.6, 25.7, 42.6, 54.1]},
    "c41": {"hero": 63.0, "ult": 56.5, "skills": [15.6, 29.2, 45.4, 56.5]},
    "c42": {"hero": 48.3, "ult": 59.1, "skills": [15.3, 28.6, 45.5, 59.1], "hx": 0.15, "ux": 0.2},
}
_fonts: dict = {}
W = H = 0


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


def fit(d, s, max_w, size, weight=900, min_size=24):
    while size > min_size and d.textlength(s, font=font(size, weight)) > max_w:
        size -= 4
    return font(size, weight)


def txt(d, xy, s, f, fill=WHITE, anchor="la", stroke=0):
    d.text((xy[0] + 4, xy[1] + 6), s, font=f, fill=(0, 0, 0, 170), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, 170))
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0))


def pill(d, x, y, s, size=48, bg=GOLD, fg=INK, center=False):
    f = font(size)
    pw, ph = d.textlength(s, font=f) + size * 0.9, size * 1.45
    if center:
        x -= pw / 2
    d.rounded_rectangle((x, y, x + pw, y + ph), radius=ph * 0.28, fill=bg)
    d.text((x + pw / 2, y + ph / 2), s, font=f, fill=fg, anchor="mm")
    return pw, ph


def grad(w, h, a0, a1, color=(0, 0, 0)):
    g = Image.new("L", (1, h))
    for i in range(h):
        g.putpixel((0, i), round(a0 + (a1 - a0) * i / max(h - 1, 1)))
    layer = Image.new("RGBA", (w, h), color + (0,))
    layer.putalpha(g.resize((w, h)))
    return layer


def cover(img: Image.Image, w: int, h: int, fx=0.5, fy=0.45) -> Image.Image:
    s = max(w / img.width, h / img.height)
    im = img.resize((max(w, round(img.width * s)), max(h, round(img.height * s))), Image.LANCZOS)
    x, y = round((im.width - w) * fx), round((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h)).convert("RGBA")


# ---------- 读资料 ----------

def publish_info(demo: Path) -> dict:
    pub = (demo / "publish.md").read_text(encoding="utf-8")
    video = re.search(r"视频：`(edit/final/[^`]+\.mp4)`", pub).group(1)

    def block_after(head: str) -> str:
        part = pub.split(head, 1)[1]
        return part.split("```text", 1)[1].split("```", 1)[0].strip()

    douyin = block_after("## 抖音")
    m = re.match(r"DotA(.+?)真人化[！!]?(.*)", douyin)
    short, hook = (m.group(1), m.group(2).strip()) if m else (douyin, "")
    yt = block_after("## YouTube")
    en = re.match(r"DotA (.+?) in Live Action", yt).group(1)
    bili = pub.split("## 哔哩哔哩", 1)[1]
    chapters = re.findall(r"^\d:\d\d (.+?)（(.+?)）\s*$", bili, re.M)
    skills = [(n.strip(), k.replace(" ", "")) for n, k in chapters][-4:]
    return {"video": demo / video, "short": short, "hook": hook, "en": en, "skills": skills}


def drop_icon(im: Image.Image) -> Image.Image:
    """技能段画面左上角有 DotA 原版技能图标：裁掉最左一条（1280 宽时 165 px）。
    封面是 4:3 / 3:4，本来就要从 16:9 两侧裁掉，图标条去掉不影响构图。"""
    cut = round(ICON_BOX[2] / 1280 * im.width) + 5
    return im.crop((cut, 0, im.width, im.height))


def frame(video: Path, t: float, out: Path) -> Image.Image:
    if not out.is_file():
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(video), "-frames:v", "1", str(out)], check=True)
    im = Image.open(out).convert("RGB")
    return drop_icon(im) if t >= INTRO_S else im       # 亮相段（前 12 秒）没有技能图标


# ---------- 三款 ----------

def head_block(d, im, info, faction, x, y, max_w, big=150):
    fname, fcol = faction
    pw, _ = pill(d, x, y, "DotA", 46)
    pill(d, x + pw + 14, y, fname, 46, bg=fcol, fg=WHITE)
    y += 96
    f = fit(d, info["short"], max_w, big)
    txt(d, (x, y), info["short"], f, fill=GOLD, stroke=3)
    y += f.size * 1.38
    f2 = font(round(big * 0.42))
    txt(d, (x + 4, y), "真人化", f2, stroke=2)
    fe = fit(d, info["en"].upper(), max_w - d.textlength("真人化", font=f2) - 30, round(big * 0.2), 800, min_size=18)
    txt(d, (x + 8 + d.textlength("真人化", font=f2) + 22, y + f2.size * 0.55), info["en"].upper(), fe, fill=(225, 228, 236))
    return y + f2.size * 1.45


def v_hero(info, faction, frames) -> Image.Image:
    """英雄大图：顶部只放角标与钩子句，名字压在底部，不挡人物的脸。"""
    im = cover(frames["hero"], W, H, frames["hx"], 0.4)
    im.alpha_composite(grad(W, 260, 200, 0), (0, 0))
    bottom = 620 if H > W else 520
    im.alpha_composite(grad(W, bottom, 0, 235), (0, H - bottom))
    d = ImageDraw.Draw(im)
    fname, fcol = faction
    pw, _ = pill(d, 64, 56, "DotA", 46)
    pw2, _ = pill(d, 64 + pw + 14, 56, fname, 46, bg=fcol, fg=WHITE)
    if info["hook"]:
        hx = 64 + pw + pw2 + 44
        txt(d, (hx, 60), info["hook"], fit(d, info["hook"], W - 64 - hx, 56), stroke=2)
    big = 240 if H > W else 220
    f = fit(d, info["short"], W - 128, big)
    f2 = font(round(big * 0.42))
    y2 = H - 70                                        # 「真人化 + 英文名」一行的基线
    y1 = y2 - f2.size * 1.25                           # 名字的基线
    txt(d, (60, y1), info["short"], f, fill=GOLD, anchor="ls", stroke=3)
    txt(d, (64, y2), "真人化", f2, anchor="ls", stroke=2)
    fe = fit(d, info["en"].upper(), W - 150 - d.textlength("真人化", font=f2), round(big * 0.2), 800, min_size=18)
    txt(d, (64 + d.textlength("真人化", font=f2) + 22, y2), info["en"].upper(), fe, fill=(225, 228, 236), anchor="ls")
    return im.convert("RGB")


def v_skills(info, faction, frames) -> Image.Image:
    im = Image.new("RGBA", (W, H), INK + (255,))
    d = ImageDraw.Draw(im)
    top = 300
    if H > W:
        top = int(head_block(d, im, info, faction, 60, 44, W - 120, 150)) + 10
    else:
        fname, fcol = faction
        pw, _ = pill(d, 60, 56, "DotA", 46)
        pill(d, 60 + pw + 14, 56, fname, 46, bg=fcol, fg=WHITE)
        title = f"{info['short']}真人化"
        txt(d, (60, 128), title, fit(d, title, W * 0.62, 100), fill=GOLD, stroke=2)
        sub = "四技能全还原"
        txt(d, (W - 60, 150), sub, fit(d, sub, W * 0.3, 64), anchor="ra")
    g = 8
    gh = H - top - (130 if H > W else 0)
    cw, ch = (W - g) // 2, (gh - g) // 2
    for k, (img, (name, key)) in enumerate(zip(frames["skills"], info["skills"])):
        r, c = divmod(k, 2)
        x, y = c * (cw + g), top + r * (ch + g)
        im.alpha_composite(cover(img, cw, ch, 0.5, 0.45), (x, y))
        im.alpha_composite(grad(cw, 190, 0, 220), (x, y + ch - 190))
        d = ImageDraw.Draw(im)
        pill(d, x + 20, y + 20, key, 34, bg=(20, 22, 30), fg=GOLD)
        txt(d, (x + 26, y + ch - 26), name, fit(d, name, cw - 52, 72), anchor="ls", stroke=2)
    if H > W:
        txt(d, (W / 2, H - 42), "四个技能一次看完", font(70), fill=GOLD, anchor="ms", stroke=2)
    return im.convert("RGB")


def v_ult(info, faction, frames) -> Image.Image:
    im = cover(frames["ult"], W, H, frames["ux"], 0.45)
    im.alpha_composite(grad(W, H // 2, 0, 230), (0, H - H // 2))
    im.alpha_composite(grad(W, 260, 170, 0), (0, 0))
    d = ImageDraw.Draw(im)
    fname, fcol = faction
    pw, _ = pill(d, 60, 56, "DotA", 46)
    pw2, _ = pill(d, 60 + pw + 14, 56, fname, 46, bg=fcol, fg=WHITE)
    txt(d, (60 + pw + pw2 + 40, 60), f"{info['short']} · 大招", fit(d, f"{info['short']} · 大招", W - 120 - pw - pw2 - 40, 60), stroke=2)
    ult, key = info["skills"][-1]
    f = fit(d, ult, W - 120, 260 if H > W else 230)
    y = H - (330 if H > W else 300)
    txt(d, (60, y), ult, f, fill=GOLD, anchor="ls", stroke=4)
    line = f"{info['short']}真人化，大招全还原" if not info["hook"] else info["hook"]
    txt(d, (64, y + 110), line, fit(d, line, W - 128, 70), anchor="ls", stroke=2)
    return im.convert("RGB")


def make(hero_dir: Path) -> list[Path]:
    global W, H
    key = hero_dir.name.split("_")[0]
    demo = hero_dir / "demo"
    info = publish_info(demo)
    faction = FACTION[hero_dir.parent.name]
    sel = FRAMES[key]
    out = demo / "covers"
    fr = out / "frames"
    vtag = info["video"].stem.split("_")[-1]
    frames = {"hero": frame(info["video"], sel["hero"], fr / f"{vtag}_{sel['hero']:.1f}.png"),
              "ult": frame(info["video"], sel["ult"], fr / f"{vtag}_{sel['ult']:.1f}.png"),
              "skills": [frame(info["video"], t, fr / f"{vtag}_{t:.1f}.png") for t in sel["skills"]],
              "hx": sel.get("hx", 0.5), "ux": sel.get("ux", 0.5)}
    paths = []
    for tag, (W, H) in FORMATS.items():
        for k, fn in enumerate((v_hero, v_skills, v_ult), 1):
            p = out / f"cover_{k}_{tag}.png"
            fn(info, faction, frames).save(p, optimize=True)
            paths.append(p)
    return paths


PAGE = DRAMA / "demo_covers.html"


def write_page() -> Path:
    """一页看全部英雄的封面候选（相对路径，直接用浏览器打开）。"""
    import html
    rows = []
    for hero_dir in sorted(CHARS.glob("*/*")):
        cov = hero_dir / "demo" / "covers"
        if not (cov / "cover_1_4x3.png").is_file():
            continue
        info = publish_info(hero_dir / "demo")
        rel = cov.relative_to(DRAMA).as_posix()
        pub = (hero_dir / "demo" / "publish.md").relative_to(DRAMA).as_posix()
        status = "未定版" if "尚未定版" in (hero_dir / "demo" / "publish.md").read_text(encoding="utf-8") else "定版"
        cells = "".join(f'<a href="{rel}/cover_{k}_{tag}.png" target="_blank"><img loading="lazy" class="{tag}" src="{rel}/cover_{k}_{tag}.png">'
                        f'<span>{lab} · {tag.replace("x", ":")}</span></a>'
                        for tag in ("4x3", "3x4") for k, lab in ((1, "① 英雄大图"), (2, "② 四技能"), (3, "③ 大招")))
        rows.append(f'<h2>{html.escape(hero_dir.name)} · {html.escape(info["short"])}（{html.escape(info["en"])}）'
                    f'<small>{status} · <a href="{pub}">publish.md</a> · <code>{html.escape(info["video"].name)}</code></small></h2><div class="row">{cells}</div>')
    css = """:root{--bg:#f4f5f7;--ink:#15171c;--mute:#5d6470;--card:#fff;--line:#e1e4ea}
@media (prefers-color-scheme:dark){:root{--bg:#111317;--ink:#e8eaee;--mute:#9aa1ad;--card:#1b1e23;--line:#2b2f36}}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 system-ui,"Microsoft YaHei",sans-serif}main{max-width:1500px;margin:0 auto;padding:24px 16px}
h2{font-size:18px;margin:28px 0 10px}h2 small{font-weight:400;color:var(--mute);margin-left:12px;font-size:13px}a{color:inherit}
.row{display:grid;grid-template-columns:repeat(3,4fr) repeat(3,3fr);gap:10px;align-items:end}.row a{text-decoration:none;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:6px}
.row img{width:100%;display:block;border-radius:5px}.row span{font-size:12px;color:var(--mute)}@media (max-width:900px){.row{grid-template-columns:repeat(3,1fr)}}"""
    body = ("<h1>DotA 英雄 demo · 中文封面候选</h1><p style='color:var(--mute)'>每个英雄 4:3 横屏（1440×1080，抖音横封面）与 3:4 竖屏（1080×1440，抖音竖封面 / 小红书）各三款。"
            "点图看原尺寸。画面取自各英雄 publish.md 头部的成片；重新生成：<code>python ai_videos/dota_yingxiong/_tools/demo_covers.py</code>。</p>" + "".join(rows))
    PAGE.write_text(f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                    f'<title>英雄封面挑选</title><style>{css}</style></head><body><main>{body}</main></body></html>', encoding="utf-8")
    return PAGE


def main() -> None:
    want = set(sys.argv[1:])
    for hero_dir in sorted(CHARS.glob("*/*")):
        key = hero_dir.name.split("_")[0]
        if key not in FRAMES or (want and key not in want):
            continue
        if not (hero_dir / "demo" / "publish.md").is_file():
            print("skip（没有 publish.md）", hero_dir.name)
            continue
        make(hero_dir)
        print("ok", hero_dir.name)
    print("page", write_page())


if __name__ == "__main__":
    main()
