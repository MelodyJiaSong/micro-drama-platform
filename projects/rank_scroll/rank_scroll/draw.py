"""Small skia drawing helpers: fonts, fitted text, wrapped text, images, icons, flags."""
from __future__ import annotations

import math
from functools import lru_cache
from pathlib import Path

import skia

from .theme import hex_color

ASSETS = Path(__file__).resolve().parents[1] / "assets"
FONT_DIR = ASSETS / "fonts"
ICON_DIR = ASSETS / "icons"
ICON_FILES = {
    "mountain": "mountain", "calendar": "calendar", "building": "building-skyscraper", "stairs": "stairs",
    "map-pin": "map-pin", "ruler": "ruler-measure", "flag": "flag", "trophy": "trophy", "users": "users",
    "globe": "world",
}


LANG = "en"         # 由 __main__ 按 --lang 设置；zh 时整套改用 Noto Sans SC（OFL，可商用；不用方正版权的微软雅黑）
CJK_WEIGHT = {"Regular": 400, "Medium": 500, "SemiBold": 600, "Bold": 700, "ExtraBold": 800, "Black": 900}


def _wght(tf: skia.Typeface, w: int) -> skia.Typeface:
    """可变字体按字重取实例；不设的话 Noto Sans SC 默认是 100（最细）。"""
    tag = (ord("w") << 24) | (ord("g") << 16) | (ord("h") << 8) | ord("t")
    VP = skia.FontArguments.VariationPosition
    pos = VP(VP.Coordinates([VP.Coordinate(tag, float(w))]))
    return tf.makeClone(skia.FontArguments().setVariationDesignPosition(pos))


@lru_cache(maxsize=None)
def typeface(weight: str = "Bold") -> skia.Typeface:
    if LANG == "zh":
        base = _fallback_typeface()
        if base is None:
            raise FileNotFoundError(f"中文版需要 NotoSansSC-Variable.ttf（{FONT_DIR}）")
        return _wght(base, CJK_WEIGHT.get(weight, 700))
    tf = skia.Typeface.MakeFromFile(str(FONT_DIR / f"Inter-{weight}.ttf"))
    if tf is None:
        raise FileNotFoundError(f"font Inter-{weight}.ttf missing in {FONT_DIR}")
    return tf


def font(size: float, weight: str = "Bold") -> skia.Font:
    f = skia.Font(typeface(weight), size)
    f.setSubpixel(True)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    f.setHinting(skia.FontHinting.kNone)
    return f


@lru_cache(maxsize=None)
def _fallback_typeface() -> skia.Typeface | None:
    # bundled copy is git-ignored (17 MB, see README); fall back to the Windows-shipped Noto Sans SC
    for cand in (FONT_DIR / "NotoSansSC-Variable.ttf", Path("C:/Windows/Fonts/NotoSansSC-VF.ttf")):
        if cand.is_file():
            return skia.Typeface.MakeFromFile(str(cand))
    return None


def for_text(f: skia.Font, s: str) -> skia.Font:
    """Return f, or a Noto Sans SC font of the same size if f lacks a glyph used in s."""
    if s and 0 in f.textToGlyphs(s):
        fb = _fallback_typeface()
        if fb is not None:
            g = skia.Font(_wght(fb, 700), f.getSize())
            g.setSubpixel(True)
            g.setEdging(skia.Font.Edging.kAntiAlias)
            return g
    return f


def paint(color: str | int, alpha: int = 255, style=None, stroke: float = 0) -> skia.Paint:
    c = hex_color(color, alpha) if isinstance(color, str) else color
    p = skia.Paint(AntiAlias=True, Color=c)
    if style == "stroke":
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
    return p


def fit(text: str, size: float, max_w: float, weight: str = "Bold", min_size: float | None = None) -> tuple[str, skia.Font]:
    """Shrink font until text fits max_w; below min_size, ellipsize."""
    min_size = min_size or size * 0.6
    s = size
    while s > min_size:
        f = for_text(font(s, weight), text)
        if f.measureText(text) <= max_w:
            return text, f
        s -= 1
    f = for_text(font(min_size, weight), text)
    if f.measureText(text) <= max_w:
        return text, f
    t = text
    while t and f.measureText(t + "…") > max_w:
        t = t[:-1]
    return t.rstrip() + "…", f


def text(canvas: skia.Canvas, s: str, x: float, y: float, f: skia.Font, p: skia.Paint, align: str = "left") -> float:
    f = for_text(f, s)
    w = f.measureText(s)
    if align == "center":
        x -= w / 2
    elif align == "right":
        x -= w
    canvas.drawString(s, x, y, f, p)
    return w


UNIT_RE = __import__("re").compile(r"(\d) (m|ft|km|mi|%)(?=[\s.,;:!?)]|$)")


CJK_RE = __import__("re").compile(r"[⺀-鿿豈-﫿　-〿＀-￯]")
CJK_TOKEN_RE = __import__("re").compile(r"[A-Za-z0-9 .,%'’+\-/:()]+|\s+|.")
NO_LINE_START = set("，。、；：！？）」』”’》〉】,.;:!?)%")


def wrap_cjk(s: str, f: skia.Font, max_w: float) -> list[str]:
    """中日韩文字没有空格：逐字断行，拉丁词与数字整体不拆，中文标点不放行首（rank_scroll follow-up 017）。"""
    lines, cur = [], ""
    for tok in CJK_TOKEN_RE.findall(s):
        if not cur and tok.isspace():
            continue
        trial = cur + tok
        if f.measureText(trial.rstrip()) <= max_w or not cur or tok[0] in NO_LINE_START:
            cur = trial
        else:
            lines.append(cur.rstrip())
            cur = tok.lstrip()
    if cur.strip():
        lines.append(cur.rstrip())
    return lines


def wrap(s: str, f: skia.Font, max_w: float) -> list[str]:
    if CJK_RE.search(s):
        return wrap_cjk(s, f, max_w)
    s = UNIT_RE.sub(lambda m: m.group(1) + " " + m.group(2), s)   # keep "4,095 m" together (no-break space)
    words, lines, cur = s.split(" "), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if f.measureText(trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


@lru_cache(maxsize=512)
def image(path: str) -> skia.Image | None:
    data = skia.Data.MakeFromFileName(path)
    if data is None:
        return None
    img = skia.Image.MakeFromEncoded(data)
    return img.makeRasterImage() if img is not None else None


def draw_cover(canvas: skia.Canvas, img: skia.Image, rect: skia.Rect, radius: float, focus_y: float = 0.45,
               focus_x: float = 0.5) -> None:
    """Draw img to fill rect (cover crop), rounded corners; focus picks which part of the overflow is kept."""
    iw, ih = img.width(), img.height()
    rw, rh = rect.width(), rect.height()
    scale = max(rw / iw, rh / ih)
    sw, sh = rw / scale, rh / scale
    sx = max(0.0, min(iw - sw, (iw - sw) * focus_x))
    sy = max(0.0, min(ih - sh, (ih - sh) * focus_y))
    canvas.save()
    canvas.clipRRect(skia.RRect.MakeRectXY(rect, radius, radius), skia.ClipOp.kIntersect, True)
    canvas.drawImageRect(img, skia.Rect.MakeXYWH(sx, sy, sw, sh), rect,
                         skia.SamplingOptions(skia.CubicResampler.Mitchell()), None)
    canvas.restore()


def draw_fit_portrait(canvas: skia.Canvas, img: skia.Image, rect: skia.Rect, radius: float) -> None:
    """Portrait photo in a landscape slot: blurred, darkened cover fill + the whole photo contained, centred."""
    draw_contain(canvas, img, rect, radius)


def draw_photo(canvas: skia.Canvas, img: skia.Image, rect: skia.Rect, radius: float, fit: str,
               focus: tuple[float, float]) -> None:
    """Card photo: cover crop (default) or contain (rank_scroll follow-up 016) per item.image_fit."""
    if fit == "contain":
        draw_contain(canvas, img, rect, radius, focus_x=focus[0], focus_y=focus[1])
    else:
        draw_cover(canvas, img, rect, radius, focus_y=focus[1], focus_x=focus[0])


def draw_contain(canvas: skia.Canvas, img: skia.Image, rect: skia.Rect, radius: float, focus_x: float = 0.5,
                 focus_y: float = 0.5) -> None:
    """Whole photo scaled to fit inside rect (no crop); the rest is the same photo cover-filled, blurred and darkened.
    focus places the contained photo within the leftover space (0 = left / top, 1 = right / bottom)."""
    canvas.save()
    canvas.clipRRect(skia.RRect.MakeRectXY(rect, radius, radius), skia.ClipOp.kIntersect, True)
    blur = skia.Paint(ImageFilter=skia.ImageFilters.Blur(18, 18))
    canvas.saveLayer(rect, blur)
    draw_cover(canvas, img, rect, 0, focus_y=0.5)
    canvas.restore()
    canvas.drawRect(rect, paint("#000000", 90))
    iw, ih = img.width(), img.height()
    scale = min(rect.width() / iw, rect.height() / ih)
    w, h = iw * scale, ih * scale
    dst = skia.Rect.MakeXYWH(rect.left() + (rect.width() - w) * focus_x, rect.top() + (rect.height() - h) * focus_y, w, h)
    canvas.drawImageRect(img, skia.Rect.MakeWH(iw, ih), dst, skia.SamplingOptions(skia.CubicResampler.Mitchell()), None)
    canvas.restore()


@lru_cache(maxsize=None)
def _icon_dom(name: str, color: str) -> skia.SVGDOM:
    svg = (ICON_DIR / f"{ICON_FILES.get(name, name)}.svg").read_text(encoding="utf-8").replace("currentColor", color)
    return skia.SVGDOM.MakeFromStream(skia.MemoryStream(svg.encode("utf-8"), True))


def icon(canvas: skia.Canvas, name: str, x: float, y: float, size: float, color: str) -> None:
    dom = _icon_dom(name, color)
    canvas.save()
    canvas.translate(x, y)
    canvas.scale(size / 24, size / 24)
    dom.setContainerSize(skia.Size(24, 24))
    dom.render(canvas)
    canvas.restore()


def flag(canvas: skia.Canvas, path: Path, x: float, y: float, w: float, h: float, border: str = "#00000033") -> None:
    img = image(str(path))
    rect = skia.Rect.MakeXYWH(x, y, w, h)
    if img is None:
        canvas.drawRect(rect, paint("#888888"))
        return
    draw_cover(canvas, img, rect, 5, focus_y=0.5)
    canvas.drawRRect(skia.RRect.MakeRectXY(rect, 5, 5), paint(hex_color(border[:7], int(border[7:9] or "ff", 16)), style="stroke", stroke=1.5))


def flag_natural(canvas: skia.Canvas, path: Path, x: float, y: float, h: float, max_w: float,
                 border: float = 4, shadow: bool = True) -> float:
    """Flag at its own aspect ratio (no crop), height h, white frame and soft shadow. Returns drawn width."""
    img = image(str(path))
    if img is None:
        return 0.0
    w = min(max_w, h * img.width() / img.height())
    hh = w * img.height() / img.width()
    rect = skia.Rect.MakeXYWH(x, y, w, hh)
    frame = rect.makeOutset(border, border)
    if shadow:
        sp = skia.Paint(AntiAlias=True, Color=hex_color("#000000", 120))
        sp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8))
        canvas.drawRRect(skia.RRect.MakeRectXY(frame.makeOffset(0, 4), 8, 8), sp)
    canvas.drawRRect(skia.RRect.MakeRectXY(frame, 8, 8), paint("#ffffff"))
    canvas.save()
    canvas.clipRRect(skia.RRect.MakeRectXY(rect, 5, 5), skia.ClipOp.kIntersect, True)
    canvas.drawImageRect(img, skia.Rect.MakeWH(img.width(), img.height()), rect,
                         skia.SamplingOptions(skia.CubicResampler.Mitchell()), None)
    canvas.restore()
    return w + 2 * border


FLAG_MARGIN = 20    # 层四周留给阴影和波浪起伏的余量（1080p 像素）


@lru_cache(maxsize=256)
def flag_layer(path: str, h: float, max_w: float, border: float, shadow: bool, scale: float) -> skia.Image | None:
    """flag_natural 画进一张透明小图（设备像素），飘动时逐帧切条重绘；同一面旗、同一尺寸只画一次。"""
    img = image(path)
    if img is None:
        return None
    w = min(max_w, h * img.width() / img.height())
    hh = w * img.height() / img.width()
    surf = surface(int((w + 2 * border + 2 * FLAG_MARGIN) * scale + 0.5), int((hh + 2 * border + 2 * FLAG_MARGIN) * scale + 0.5))
    c = surf.getCanvas()
    c.clear(skia.ColorTRANSPARENT)
    c.scale(scale, scale)
    flag_natural(c, Path(path), FLAG_MARGIN + border, FLAG_MARGIN + border, h, max_w, border, shadow)
    return surf.makeImageSnapshot()


def flag_waving(canvas: skia.Canvas, layer: skia.Image, x: float, y: float, t: float, phase: float = 0.0,
                amp_frac: float = 0.07, strip: int = 3) -> None:
    """把 flag_layer 按竖条错位重绘成随风飘的旗：旗杆一侧（左）不动，越往外摆幅越大，波峰亮、波谷暗。
    x, y 是层左上角的设备坐标；t 是秒。用户 2026-11-03（paihangbang follow-up 008）：国旗要一直轻轻飘动。"""
    lw, lh = layer.width(), layer.height()
    amp = amp_frac * lh
    canvas.saveLayer(skia.Rect.MakeXYWH(x, y - amp - 2, lw, lh + 2 * amp + 4), None)
    shade = skia.Paint(AntiAlias=False)
    shade.setBlendMode(skia.BlendMode.kSrcATop)
    for sx in range(0, lw, strip):
        u = sx / max(1, lw - 1)
        env = u ** 1.3
        ang = 2 * math.pi * (u * 0.9 - t * 0.55) + phase
        dy = amp * env * math.sin(ang)
        sw = min(strip + 1, lw - sx)
        canvas.drawImageRect(layer, skia.Rect.MakeXYWH(sx, 0, sw, lh), skia.Rect.MakeXYWH(x + sx, y + dy, sw, lh),
                             skia.SamplingOptions(skia.FilterMode.kLinear), None)
        k = 0.16 * env * math.cos(ang)
        shade.setColor(skia.Color4f(1, 1, 1, k) if k > 0 else skia.Color4f(0, 0, 0, -k))
        canvas.drawRect(skia.Rect.MakeXYWH(x + sx, y + dy, sw, lh), shade)
    canvas.restore()


def pill(canvas: skia.Canvas, x: float, y: float, s: str, f: skia.Font, bg: str, fg: str, pad_x: float = 16, h: float = 40) -> float:
    w = f.measureText(s) + 2 * pad_x
    canvas.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), h / 2, h / 2), paint(bg))
    # vertically centre using cap height approximation
    canvas.drawString(s, x + pad_x, y + h / 2 + f.getSize() * 0.36, f, paint(fg))
    return w


def surface(w: int, h: int) -> skia.Surface:
    return skia.Surface.MakeRaster(skia.ImageInfo.MakeN32Premul(w, h))
