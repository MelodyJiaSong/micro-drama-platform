"""Card styles（layout.card_style，paihangbang follow-up 055 / rank_scroll follow-up 019）.

poster＝v0.2 满版照片（cards.card_image 的主体），其余四种用于对比与按期选用。都画在同一张 cw×CARD_H 卡里；
国旗经 cards._flag（flag_out）交给渲染器每帧画、保持飘动；polaroid 的国旗当邮票斜贴，静态。

- split     上图下文：上 58% 照片，下 42% 纯色信息区，文字不压照片
- duo       双图：上方成品大图，右下角压一枚圆形小图（如生米粒特写，item.inset_image），下方信息区
- polaroid  杂志 / 拍立得：米白相纸、照片嵌在纸上、深色图注
- spotlight 聚光圆图：深色卡，中央大圆形照片配强调色圆环，文字居中
"""
from __future__ import annotations

import skia

from . import draw as D
from .contract import Episode, Item
from .i18n import t as tr
from .theme import Theme, hex_color
from .timeline import CARD_H


def _cards():
    from . import cards   # cards imports this module; resolve lazily to avoid the cycle
    return cards


def _credit_text(it: Item) -> str:
    if it.image_ai:
        return tr(D.LANG, "ai_credit")
    if not it.image_credit:
        return ""
    if it.image_credit.startswith(("Render:", "Illustration:")):
        return it.image_credit
    return tr(D.LANG, "photo") + it.image_credit


def _top_badges(c: skia.Canvas, it: Item, th: Theme, img, x: float, y: float) -> None:
    yy = y
    if it.badge:
        D.pill(c, x, yy, it.badge, D.font(20, "ExtraBold"), th.strip, "#ffffff", pad_x=14, h=38)
        yy += 50
    if it.image_ai and img is not None:
        D.pill(c, x, yy, tr(D.LANG, "ai_image"), D.font(20, "ExtraBold"), "#f5c518", "#111111", pad_x=14, h=38)


def _corner(c: skia.Canvas, ep: Episode, it: Item, th: Theme, cw: int, y: float) -> None:
    rs = it.corner or ("" if ep.is_list else f"#{it.rank}")
    if rs:
        rf = D.font(40 if it.corner else 50, "Black")
        rw = rf.measureText(rs) + 2 * 20
        D.pill(c, cw - _cards().M - rw, y, rs, rf, th.accent, th.accent_text, pad_x=20, h=64 if it.corner else 74)


def _photo(c: skia.Canvas, ep: Episode, it: Item, th: Theme, rect: skia.Rect, radius: float, flag_out):
    img = D.image(str(it.image)) if it.image else None
    if img is not None:
        D.draw_photo(c, img, rect, radius, it.image_fit, it.image_focus)
    else:
        c.save()
        c.clipRect(rect)
        c.translate(rect.left(), rect.top())
        _cards()._placeholder(c, ep, it, th, int(rect.width()), flag_out)
        c.restore()
    return img


def _panel_text(c, ep: Episode, it: Item, th: Theme, x: float, y_top: float, w: float, fg: str, sub: str,
                accent: str, flag_out, center: bool = False, flag_h: float = 46) -> float:
    """Flag + country, name, big value (+ secondary). Returns the baseline y of the last line."""
    cx = x + w / 2
    y = y_top
    if ep.show_flags and it.country_iso2:
        cn, cf = D.fit(it.country_name.upper(), 24, w - 120, "ExtraBold", 16)
        fimg = D.image(str(ep.flag_path(it.country_iso2)))
        fw = min(120.0, flag_h * fimg.width() / fimg.height()) if fimg is not None else flag_h * 1.5
        tw = D.for_text(cf, cn).measureText(cn)
        fx = cx - (fw + 14 + tw) / 2 if center else x
        _cards()._flag(c, ep.flag_path(it.country_iso2), fx, y, flag_h, 120, 2, flag_out)
        D.text(c, cn, fx + fw + 14, y + flag_h * 0.68, cf, D.paint(accent))
        y += flag_h + 46
    else:
        y += 30
    name, nf = D.fit(it.name, 46, w, "ExtraBold", 28)
    D.text(c, name, cx if center else x, y, nf, D.paint(fg), align="center" if center else "left")
    sec = it.secondary_display
    sec_f = D.font(26, "SemiBold")
    val, vf = D.fit(it.value_display, 60, w, "Black", 38)
    y += 18 + vf.getSize() * 0.86
    if center:
        D.text(c, val, cx, y, vf, D.paint(accent), align="center")
        if sec:
            y += 36
            s2, sf2 = D.fit(sec, 26, w, "SemiBold", 18)
            D.text(c, s2, cx, y, sf2, D.paint(sub), align="center")
        return y
    vw = D.text(c, val, x, y, vf, D.paint(accent))
    if sec and vw + 18 + sec_f.measureText(sec) <= w:
        D.text(c, sec, x + vw + 18, y, sec_f, D.paint(sub))
    elif sec:
        y += 36
        s2, sf2 = D.fit(sec, 26, w, "SemiBold", 18)
        D.text(c, s2, x, y, sf2, D.paint(sub))
    return y


def _credit_line(c, it: Item, cw: int, y: float, color: str, extra: str = "") -> None:
    M = _cards().M
    parts = [p for p in (_credit_text(it), extra) if p]
    if parts:
        cr, crf = D.fit(" · ".join(parts), 14, cw - 2 * M, "Medium", 10)
        D.text(c, cr, cw - M, y, crf, D.paint(color, 150), align="right")


def split(c, ep: Episode, it: Item, th: Theme, cw: int, flag_out) -> None:
    M = _cards().M
    ph = int(CARD_H * 0.58)
    c.drawRect(skia.Rect.MakeWH(cw, CARD_H), D.paint(th.strip))
    img = _photo(c, ep, it, th, skia.Rect.MakeWH(cw, ph), 0, flag_out)
    c.drawRect(skia.Rect.MakeXYWH(0, ph, cw, 6), D.paint(th.accent))
    _top_badges(c, it, th, img, M, M + 4)
    _corner(c, ep, it, th, cw, M + 4)
    _panel_text(c, ep, it, th, M, ph + 30, cw - 2 * M, "#ffffff", "#cfd6e4", th.accent, flag_out)
    _cards()._info_line(c, it, M, CARD_H - 50, cw - 2 * M)
    _credit_line(c, it, cw, CARD_H - 16, "#ffffff")


def _inset_circle(c, it: Item, th: Theme, cx: float, cy: float, d: float) -> None:
    img = D.image(str(it.inset_image)) if it.inset_image else None
    if img is None:
        return
    sh = skia.Paint(AntiAlias=True, Color=hex_color("#000000", 150))
    sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10))
    c.drawCircle(cx, cy + 6, d / 2 + 7, sh)
    c.drawCircle(cx, cy, d / 2 + 7, D.paint("#ffffff"))
    D.draw_cover(c, img, skia.Rect.MakeXYWH(cx - d / 2, cy - d / 2, d, d), d / 2, focus_y=0.5, focus_x=0.5)
    if it.inset_label:
        lf = D.font(17, "ExtraBold")
        lw = lf.measureText(it.inset_label) + 24
        D.pill(c, cx - lw / 2, cy + d / 2 - 14, it.inset_label, lf, th.accent, th.accent_text, pad_x=12, h=32)


def duo(c, ep: Episode, it: Item, th: Theme, cw: int, flag_out) -> None:
    if it.inset_image is None:
        split(c, ep, it, th, cw, flag_out)
        return
    M = _cards().M
    ph = int(CARD_H * 0.56)
    c.drawRect(skia.Rect.MakeWH(cw, CARD_H), D.paint(th.strip))
    img = _photo(c, ep, it, th, skia.Rect.MakeWH(cw, ph), 0, flag_out)
    c.drawRect(skia.Rect.MakeXYWH(0, ph, cw, 6), D.paint(th.accent))
    _top_badges(c, it, th, img, M, M + 4)
    _corner(c, ep, it, th, cw, M + 4)
    d = 200
    _inset_circle(c, it, th, cw - M - d / 2 - 4, ph - 8, d)
    _panel_text(c, ep, it, th, M, ph + 30, cw - 2 * M - d - 10, "#ffffff", "#cfd6e4", th.accent, flag_out)
    _cards()._info_line(c, it, M, CARD_H - 50, cw - 2 * M)
    _credit_line(c, it, cw, CARD_H - 16, "#ffffff", ("Inset: " + it.inset_credit) if it.inset_credit else "")


def polaroid(c, ep: Episode, it: Item, th: Theme, cw: int, flag_out) -> None:
    M = _cards().M
    paper, ink, warm = "#f6f1e7", "#2a2622", "#8a3b12"
    c.drawRect(skia.Rect.MakeWH(cw, CARD_H), D.paint(paper))
    fr = skia.Rect.MakeXYWH(M, M, cw - 2 * M, CARD_H * 0.64)
    sh = skia.Paint(AntiAlias=True, Color=hex_color("#000000", 70))
    sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6))
    c.drawRect(skia.Rect.MakeXYWH(fr.left(), fr.top() + 3, fr.width(), fr.height()), sh)
    img = _photo(c, ep, it, th, fr, 4, flag_out)
    _top_badges(c, it, th, img, M + 16, M + 16)
    if ep.show_flags and it.country_iso2:          # stamp: white border, slight tilt, drawn statically
        c.save()
        c.translate(cw - M - 74, M + 44)
        c.rotate(8)
        D.flag_natural(c, ep.flag_path(it.country_iso2), -62, -32, 76, 140, border=6)
        c.restore()
    y = fr.bottom() + 46
    cn, cf = D.fit(it.country_name.upper(), 22, cw - 2 * M, "ExtraBold", 16)
    D.text(c, cn, M + 4, y, cf, D.paint(warm))
    name, nf = D.fit(it.name, 48, cw - 2 * M, "Black", 28)
    D.text(c, name, M + 4, y + 52, nf, D.paint(ink))
    val, vf = D.fit(it.value_display, 40, cw - 2 * M, "ExtraBold", 26)
    vw = D.text(c, val, M + 4, y + 104, vf, D.paint(warm))
    if it.secondary_display:
        s2, sf2 = D.fit(it.secondary_display, 24, cw - 2 * M - vw - 20, "SemiBold", 16)
        D.text(c, s2, M + 4 + vw + 16, y + 104, sf2, D.paint(ink, 170))
    _cards()._info_line(c, it, M + 4, CARD_H - 50, cw - 2 * M, color=ink, shadow=False)
    _credit_line(c, it, cw, CARD_H - 16, ink)


def spotlight(c, ep: Episode, it: Item, th: Theme, cw: int, flag_out) -> None:
    M = _cards().M
    rect = skia.Rect.MakeWH(cw, CARD_H)
    c.drawRect(rect, D.paint(th.strip))
    c.drawRect(rect, skia.Paint(Shader=skia.GradientShader.MakeRadial(
        skia.Point(cw / 2, 300), cw * 0.7, [hex_color(th.accent, 70), hex_color(th.strip, 0)])))
    d = min(cw - 140, 440)
    cx, cy = cw / 2, 60 + d / 2
    glow = skia.Paint(AntiAlias=True, Color=hex_color(th.accent, 160))
    glow.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18))
    c.drawCircle(cx, cy, d / 2 + 10, glow)
    c.drawCircle(cx, cy, d / 2 + 8, D.paint(th.accent))
    img = D.image(str(it.image)) if it.image else None
    if img is not None:
        D.draw_cover(c, img, skia.Rect.MakeXYWH(cx - d / 2, cy - d / 2, d, d), d / 2,
                     focus_y=it.image_focus[1], focus_x=it.image_focus[0])
    else:
        c.drawCircle(cx, cy, d / 2, D.paint("#2b3445"))
    _top_badges(c, it, th, img, M, M + 4)
    _corner(c, ep, it, th, cw, M + 4)
    _panel_text(c, ep, it, th, M, cy + d / 2 + 34, cw - 2 * M, "#ffffff", "#cfd6e4", th.accent, flag_out,
                center=True, flag_h=40)
    _cards()._info_line(c, it, cw / 2, CARD_H - 46, cw - 2 * M, center=True, size=20)
    _credit_line(c, it, cw, CARD_H - 14, "#ffffff")


STYLE_FUNCS = {"split": split, "duo": duo, "polaroid": polaroid, "spotlight": spotlight}
