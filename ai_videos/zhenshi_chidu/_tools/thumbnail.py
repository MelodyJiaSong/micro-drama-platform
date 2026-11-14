"""封面：中英两版 × 两种构图 × 各平台尺寸，从 Blender 高清静帧合成，不调用收费服务。

    python ai_videos/zhenshi_chidu/_tools/thumbnail.py <集目录>

构图 A：冠军长颈鹿 + 1.75 m 人 + 「HOW TALL ARE THEY?」；B：全体合影 + 「30 GIANTS TRUE SCALE」。
尺寸（与排行榜频道 zh_covers.py 同一套）：
  16x9  1920×1080：B站、西瓜、视频号横版、快手横版
  yt    1280×720 （≤ 2 MB）：YouTube，另存为 render/thumb_{A,B}{,_zh}.jpg（upload.py 用）
  4x3   1440×1080：抖音横封面、B站动态
  3x4   1080×1440：抖音 / 快手 / 视频号竖封面、小红书、TikTok（只出 A；B 是横排合影，竖版里动物太小，封面审片后去掉）
输出 render/covers/{en,zh}/A_{16x9,yt,4x3,3x4}.jpg、B_{16x9,yt,4x3}.jpg。
AI 标（AI IMAGE / AI 生成图，与片中一致）：横版放右上（右下会被 YouTube 时长角标盖住）；
竖版的标题、人物标签、AI 标都在居中 1:1 与居中 9:16 裁切的公共安全区（x 150–930、y 190–1250）内，平台裁成方图或全屏时不丢。

静帧先用 render_ep.py --still 渲（同一相机位置，只改焦距与平移，所以各尺寸里人与动物的比例完全相同；视野坐标是原 1920×1080 画面的像素）：
  lineup 6283 3840x2160 960 1920 0      → _build/cover_stills/A_wide.png
  lineup 6283 1080x1440 967 1300 -577   → A_3x4.png（人到长颈鹿头 845 px 放进 9:16 安全宽 810 px）
  group  299  3840x2160 960 1920 0      → B_wide.png
  group  299  1440x1080 960 1760 -237   → B_4x3.png
完整命令：blender -b <集>/scene/ep.blend --python ai_videos/zhenshi_chidu/_tools/render_ep.py -- <集> <段> --still …
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cards_zh  # noqa: E402
from cards import ACCENT, WHITE, font  # noqa: E402

# 静帧的视野（原画面像素坐标）：中心 x、视野宽、顶；与上面 docstring 的渲染命令一致
STILLS = {"A_wide": (960, 1920, 0), "A_3x4": (967, 1300, -577), "B_wide": (960, 1920, 0),
          "B_4x3": (960, 1760, -237)}
TEXT = {
    "en": {"A": ("HOW TALL", "ARE THEY?"), "A_sub": "TRUE SCALE · 30 GIANTS · 1.75 m MAN",
           "B": ("30 GIANTS", "TRUE SCALE"), "man": "1.75 m man", "ai": "AI IMAGE"},
    "zh": {"A": ("它们到底", "有多高？"), "A_sub": "按肩高排名 · 30 种巨兽 · 1.75 m 的人",
           "B": ("30 种巨兽", "真实比例"), "man": "1.75 m 的人", "ai": "AI 生成图"},
}
SIZES = {"16x9": (1920, 1080), "yt": (1280, 720), "4x3": (1440, 1080), "3x4": (1080, 1440)}
DESIGN_SIZES = {"A": ("16x9", "yt", "4x3", "3x4"), "B": ("16x9", "yt", "4x3")}
SAFE_3X4 = (150, 190, 930, 1250)     # 居中 1:1（y 180–1260）与居中 9:16（x 135–945）的公共区，略收
INK = (10, 12, 16)


def _text(d, xy, text, f, fill, stroke):
    d.text(xy, text, font=f, fill=fill, stroke_width=stroke, stroke_fill=INK)


def crop_still(src: Image.Image, key: str, win: tuple[float, float, float], size: tuple[int, int]) -> Image.Image:
    """从静帧裁出原画面坐标里的窗口 (x0, y0, 宽)，按 size 的宽高比，缩放到 size。"""
    cx, w, top = STILLS[key]
    k = src.width / w                       # 静帧像素 / 原画面像素
    x0, y0, ww = win
    hh = ww * size[1] / size[0]
    box = ((x0 - (cx - w / 2)) * k, (y0 - top) * k, (x0 + ww - (cx - w / 2)) * k, (y0 + hh - top) * k)
    return src.crop(tuple(round(v) for v in box)).resize(size, Image.LANCZOS)


def to_px(pt: tuple[float, float], win: tuple[float, float, float], size: tuple[int, int]) -> tuple[float, float]:
    x0, y0, ww = win
    s = size[0] / ww
    return (pt[0] - x0) * s, (pt[1] - y0) * s


def man_tag(im: Image.Image, xy: tuple[float, float], text: str, fnt, scale: float, margin: float | None = None) -> None:
    """人头顶的指示标签（与片中 man_label 同样式）：底尖对准 xy。"""
    d = ImageDraw.Draw(im)
    f = fnt("Bold", round(26 * scale))
    tw = d.textlength(text, font=f)
    pad, h, tip = 16 * scale, 44 * scale, 16 * scale
    x, y = xy
    bx = max(x, tw / 2 + pad + (im.width * 0.025 if margin is None else margin))   # 框整体留在左缘安全边距内，底尖仍对准人
    box = (bx - tw / 2 - pad, y - tip - h, bx + tw / 2 + pad, y - tip)
    d.rounded_rectangle(box, round(10 * scale), fill=(16, 20, 26, 225))
    d.polygon([(x - 10 * scale, box[3]), (x + 10 * scale, box[3]), (x, y)], fill=(16, 20, 26, 225))
    d.text((bx, (box[1] + box[3]) / 2), text, font=f, fill=WHITE, anchor="mm")


def ai_badge(im: Image.Image, text: str, fnt, s: float, corner: tuple[float, float], top: bool) -> None:
    """AI 标：corner 是标的右上角（top=True）或右下角坐标。"""
    d = ImageDraw.Draw(im)
    f = fnt("ExtraBold", round(29 * s))
    tw = d.textlength(text, font=f)
    x1, yy = corner
    y0, y1 = (yy, yy + 44 * s) if top else (yy - 44 * s, yy)
    d.rounded_rectangle((x1 - tw - 30 * s, y0, x1, y1), round(8 * s), fill=ACCENT)
    d.text((x1 - tw / 2 - 15 * s, (y0 + y1) / 2), text, font=f, fill=(20, 20, 20), anchor="mm")


def compose(ep: Path, lang: str, design: str, ratio: str, tl: dict, stills: Path) -> Image.Image:
    T = TEXT[lang]
    fnt = cards_zh.font if lang == "zh" else font
    size = SIZES[ratio]
    W, H = size
    s = W / 1280 if W > H else W / 1080
    if design == "A":
        champ = tl["items"][-1]
        man = champ["man_label_xy"]
        if ratio == "3x4":
            key, win = "A_3x4", (967 - 650, -577, 1300)
        elif ratio == "4x3":
            key, win = "A_wide", (200, 0, 1300)       # 长颈鹿靠右，左上标题不压到它背上（封面审片）
        else:   # 16:9 与 YouTube：沿用第 3 版审过的取景（人与肩线中点偏右 60 px、宽 1500）
            cx = (man[0] + champ["marker"]["top"][0]) / 2 + 60
            key, win = "A_wide", (max(0, min(1920 - 1500, cx - 750)), 0, 1500)
    else:
        man = tl["group_man_label_xy"][1]
        if ratio == "4x3":
            key, win = "B_4x3", (960 - 880, -237, 1760)
        else:   # 16:9：左缘留住人（第 8 轮审片），上下按比例
            x0 = max(0.0, min(120.0, man[0] - 135))
            key, win = "B_wide", (x0, 67.5 * x0 / 120, 1920 - x0)
    im = crop_still(Image.open(stills / f"{key}.png").convert("RGB"), key, win, size).convert("RGBA")
    d = ImageDraw.Draw(im)
    l1, l2 = T[design]
    tall = ratio == "3x4"
    big = round((108 if design == "A" else 116) * s)     # A 的标题收小一点，问号不贴长颈鹿背（封面审片）
    zy = -round(22 * s) if lang == "zh" else 0          # Noto Sans SC 字身上方留白比 Inter 大
    x0, y0, x1, y1 = SAFE_3X4 if tall else (round(40 * s), round(30 * s), W - round(24 * s), H - round(24 * s))
    y = y0 + zy
    _text(d, (x0, y), l1, fnt("Black", big), WHITE, round(8 * s))
    _text(d, (x0, y + round(big * 1.07)), l2, fnt("Black", round(big * (1 if design == "A" else 0.86))), ACCENT, round(8 * s))
    if design == "A":
        sub = T["A_sub"]
        fs = fnt("ExtraBold", round(42 * s))
        while d.textlength(sub, font=fs) > x1 - x0:
            fs = fnt("ExtraBold", fs.size - 2)
        sub_y = (y1 - round(120 * s)) if tall else (H - round(78 * s))   # 横版压到蹄子以下
        _text(d, (x0, sub_y), sub, fs, WHITE, round(5 * s))
    man_tag(im, to_px(man, win, size), T["man"], fnt, s * (1.2 if design == "A" else 1.5),
            margin=(x0 + 10) if tall else None)
    if tall:   # 竖版：AI 标在安全区右下
        ai_badge(im, T["ai"], fnt, s, (x1, y1), top=False)
    else:      # 横版：右上，避开 YouTube 右下角时长角标
        ai_badge(im, T["ai"], fnt, s, (W - round(24 * s), round(24 * s)), top=True)
    return im.convert("RGB")


def main() -> None:
    ep = Path(sys.argv[1]).resolve()
    tl = json.loads((ep / "_build/timeline.json").read_text(encoding="utf-8"))
    stills = ep / "_build" / "cover_stills"
    missing = [k for k in STILLS if not (stills / f"{k}.png").is_file()]
    if missing:
        raise SystemExit(f"缺静帧 {missing}：先按本文件 docstring 用 render_ep.py --still 渲")
    for lang in ("en", "zh"):
        out = ep / "render" / "covers" / lang
        out.mkdir(parents=True, exist_ok=True)
        for design in ("A", "B"):
            for ratio in DESIGN_SIZES[design]:
                im = compose(ep, lang, design, ratio, tl, stills)
                im.save(out / f"{design}_{ratio}.jpg", quality=92)
                if ratio == "yt":
                    im.save(ep / "render" / f"thumb_{design}{'_zh' if lang == 'zh' else ''}.jpg", quality=92)
    print("covers ->", ep / "render" / "covers")


if __name__ == "__main__":
    main()
