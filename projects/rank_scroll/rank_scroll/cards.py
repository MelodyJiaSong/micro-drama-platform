"""Card and insight-card pre-rendering (cached skia Images, drawn once per episode).

Layout v0.2 (2026-11-03, user feedback: photo first, flag second, key stat third):
the photo fills the whole card; a large flag at its own aspect ratio sits top-left; the rank sits
top-right; the bottom third carries country, name and the value on a dark scrim; place and tags
are merged into one small line; the photo credit is the last, smallest line.

Company card (contract v1.3, rank_scroll follow-up 004): when an item has a logo or a person, the
flag shrinks, the top-right shows `corner` (e.g. EST. 2015) instead of the rank, a white logo plate
and a founder headshot circle sit above the name, and the country line is dropped (the flag and the
place line carry it). List mode never shows the rank.
"""
from __future__ import annotations

import skia

from . import draw as D
from .contract import Episode, Insight, Item
from .i18n import t as tr
from .theme import Theme, hex_color
from .timeline import CARD_H, insight_w

PAD = 36            # transparent margin around the card for the shadow / glow
RADIUS = 24
M = 24              # inner margin
FLAG_H = 128        # top-left flag height (the second thing the eye should land on)
FLAG_MAX_W_FRAC = 0.42
CO_FLAG_H = 100     # company card: flag yields room to the logo and the founder
CO_FACE_D = 156     # founder headshot circle diameter
CO_PLATE_H = 84     # logo plate height
CO_TOP = 474        # top of the logo plate / founder circle row (circle bottom-aligned with the plate)


def _shadow(c: skia.Canvas, w: float, h: float) -> None:
    p = skia.Paint(AntiAlias=True, Color=hex_color("#000000", 120))
    p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(PAD + 4, PAD + 12, w, h), RADIUS, RADIUS), p)


def _text_paint(color: str, alpha: int = 255) -> skia.Paint:
    p = D.paint(color, alpha)
    p.setImageFilter(skia.ImageFilters.DropShadow(0, 2, 3, 3, hex_color("#000000", 150)))
    return p


def _vgrad(c: skia.Canvas, rect: skia.Rect, colors: list[int], pos: list[float]) -> None:
    c.drawRect(rect, skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [skia.Point(0, rect.top()), skia.Point(0, rect.bottom())], colors, pos)))


def _surface(cw: int, scale: float) -> tuple[skia.Surface, skia.Canvas]:
    sw, sh = int((cw + 2 * PAD) * scale + 0.5), int((CARD_H + 2 * PAD) * scale + 0.5)
    surf = D.surface(sw, sh)
    c = surf.getCanvas()
    c.clear(skia.ColorTRANSPARENT)
    c.scale(scale, scale)
    _shadow(c, cw, CARD_H)
    c.translate(PAD, PAD)
    return surf, c


def _flag(c: skia.Canvas, path, x: float, y: float, h: float, max_w: float, border: float, flag_out: list | None) -> None:
    if flag_out is None:
        D.flag_natural(c, path, x, y, h, max_w, border=border)
    else:
        flag_out.append({"path": str(path), "x": x, "y": y, "h": h, "max_w": max_w, "border": border})


def _placeholder(c: skia.Canvas, ep: Episode, it: Item, th: Theme, cw: int, flag_out: list | None = None) -> None:
    rect = skia.Rect.MakeWH(cw, CARD_H)
    c.drawRect(rect, D.paint(th.strip))
    _vgrad(c, rect, [hex_color(th.strip), hex_color(th.accent, 80)], [0.0, 1.0])
    # big centred flag stands in for the photo; neutral theme icon; honest one-line reason
    if ep.show_flags:
        img = D.image(str(ep.flag_path(it.country_iso2)))
        fh = 170
        fw = min(cw - 120, fh * img.width() / img.height()) if img is not None else fh * 1.5
        _flag(c, ep.flag_path(it.country_iso2), cw / 2 - fw / 2, 130, fh, cw - 120, 5, flag_out)
    ic = {"alpine": "mountain", "skyline": "building", "virus": "virus"}.get(th.name, "globe")
    D.icon(c, ic, cw / 2 - 40, 350, 80, "#ffffff")
    note = it.image_note or tr(D.LANG, "no_photo")
    nt, nf = D.fit(note, 24, cw - 2 * M - 40, "Bold", 16)
    nw = nf.measureText(nt)
    pill_r = skia.Rect.MakeXYWH(cw / 2 - nw / 2 - 18, 456, nw + 36, 44)
    c.drawRRect(skia.RRect.MakeRectXY(pill_r, 22, 22), D.paint("#000000", 170))
    D.text(c, nt, cw / 2, 486, nf, D.paint("#ffffff"), align="center")


def _info_line(c: skia.Canvas, it: Item, x: float, y: float, max_w: float, color: str = "#ffffff",
               shadow: bool = True, center: bool = False, size: float = 22) -> None:
    """Place + tags on one small line: '[pin] High Atlas  · [trophy] Highest in the Atlas'. Drops what won't fit.
    color / shadow / center / size serve the card styles in styles.py (paihangbang follow-up 055)."""
    f = D.font(size, "SemiBold")
    parts = ([("map-pin", it.subtitle)] if it.subtitle else []) + [(t.icon, t.text) for t in it.tags]
    ico, gap = 24, 8
    sep = 26

    def width(ps):
        return sum(ico + gap + D.for_text(f, t).measureText(t) for _, t in ps) + sep * max(0, len(ps) - 1)

    while len(parts) > 1 and width(parts) > max_w:
        parts = parts[:-1]
    if not parts:
        return
    if width(parts) > max_w:                         # single long part: shrink / ellipsize it
        t, f = D.fit(parts[0][1], size, max_w - ico - gap, "SemiBold", 16)
        parts = [(parts[0][0], t)]
    if center:
        x -= width(parts) / 2
    tp = _text_paint(color, 215) if shadow else D.paint(color, 215)
    for n, (icon_name, t) in enumerate(parts):
        if n:
            c.drawCircle(x + sep / 2 - 2, y - 8, 2.5, D.paint(color, 150))
            x += sep - 4
        D.icon(c, icon_name, x, y - 20, ico, color)
        x += ico + gap
        x += D.text(c, t, x, y, f, tp)


def _initials(name: str) -> str:
    parts = [w for w in name.replace("-", " ").split() if w[:1].isalpha()]
    return "".join(w[0].upper() for w in (parts[:1] + parts[-1:] if len(parts) > 1 else parts)) or "?"


def _logo_plate(c: skia.Canvas, it: Item, x: float, y: float, max_w: float, h: float = CO_PLATE_H) -> float:
    """White (or logo_bg) rounded plate with the logo fitted inside; returns plate width."""
    img = D.image(str(it.logo)) if it.logo else None
    if img is None:
        return 0.0
    pad_x, pad_y = 18, 14
    box_h = h - 2 * pad_y
    k = min(box_h / img.height(), (max_w - 2 * pad_x) / img.width())
    lw, lh = img.width() * k, img.height() * k
    pw = max(lw + 2 * pad_x, h)
    sh = skia.Paint(AntiAlias=True, Color=hex_color("#000000", 110))
    sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y + 3, pw, h), 16, 16), sh)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, pw, h), 16, 16), D.paint(it.logo_bg))
    c.drawImageRect(img, skia.Rect.MakeWH(img.width(), img.height()),
                    skia.Rect.MakeXYWH(x + (pw - lw) / 2, y + (h - lh) / 2, lw, lh),
                    skia.SamplingOptions(skia.CubicResampler.Mitchell()), None)
    return pw


def _face(c: skia.Canvas, it: Item, th: Theme, cx: float, cy: float, d: float) -> None:
    """Founder headshot in a white-ringed circle; initials on the accent colour when there is no usable photo."""
    sh = skia.Paint(AntiAlias=True, Color=hex_color("#000000", 140))
    sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8))
    c.drawCircle(cx, cy + 4, d / 2 + 5, sh)
    c.drawCircle(cx, cy, d / 2 + 5, D.paint("#ffffff"))
    img = D.image(str(it.person_image)) if it.person_image else None
    rect = skia.Rect.MakeXYWH(cx - d / 2, cy - d / 2, d, d)
    if img is not None:
        D.draw_cover(c, img, rect, d / 2, focus_y=it.person_focus[1], focus_x=it.person_focus[0])
    else:
        c.drawCircle(cx, cy, d / 2, D.paint(th.accent))
        f = D.font(d * 0.38, "Black")
        D.text(c, _initials(it.person_name), cx, cy + d * 0.135, f, D.paint(th.accent_text), align="center")


def _company_block(c: skia.Canvas, it: Item, th: Theme, cw: int) -> None:
    """Logo plate + founder circle row, then name, value (+ secondary), place line and credits."""
    inner = cw - 2 * M
    cap_w = 0.0
    if it.person_name:
        d = CO_FACE_D
        cx, cy = cw - M - d / 2 - 6, CO_TOP + CO_PLATE_H - d / 2
        _face(c, it, th, cx, cy, d)
        nm, nf = D.fit(it.person_name, 24, 250, "ExtraBold", 16)
        rl, rf = D.fit(it.person_role, 18, 250, "SemiBold", 13)
        cap_w = max(D.for_text(nf, nm).measureText(nm), D.for_text(rf, rl).measureText(rl) if rl else 0)
        D.text(c, nm, cw - M, CO_TOP + CO_PLATE_H + 34, nf, _text_paint("#ffffff"), align="right")
        if rl:
            D.text(c, rl, cw - M, CO_TOP + CO_PLATE_H + 58, rf, _text_paint("#ffffff", 200), align="right")
    face_w = CO_FACE_D + 30 if it.person_name else 0
    _logo_plate(c, it, M, CO_TOP, min(400, inner - face_w))

    y_value = CARD_H - 96
    sec = it.secondary_display
    sec_f = D.font(28, "SemiBold")
    sec_w = sec_f.measureText(sec) + 18 if sec else 0
    val, vf = D.fit(it.value_display, 84, inner - sec_w, "Black", 60)
    if val != it.value_display:
        sec, sec_w = "", 0
        val, vf = D.fit(it.value_display, 84, inner, "Black", 52)
    vw = D.text(c, val, M, y_value, vf, _text_paint(th.accent))
    if sec:
        D.text(c, sec, M + vw + 18, y_value, sec_f, _text_paint("#ffffff", 200))
    name_w = inner - (cap_w + 40 if cap_w else 0)   # keep a clear gap to the founder caption (ep03 QC: SSI)
    name, nf2 = D.fit(it.name, 46, name_w, "ExtraBold", 26)
    D.text(c, name, M, y_value - vf.getSize() * 0.78 - 26, nf2, _text_paint("#ffffff"))

    _info_line(c, it, M, CARD_H - 50, inner)
    pfx = "" if it.image_credit.startswith(("Render:", "Illustration:")) else tr(D.LANG, "photo")   # AI images are not photos (follow-up 013)
    credits = [x for x in ((pfx + it.image_credit) if it.image_credit else "",
                           (tr(D.LANG, "portrait") + it.person_credit) if it.person_image and it.person_credit else "") if x]
    if credits:
        cr, crf = D.fit(" · ".join(credits), 14, inner, "Medium", 10)
        D.text(c, cr, cw - M, CARD_H - 16, crf, D.paint("#ffffff", 150), align="right")


def _company_placeholder(c: skia.Canvas, it: Item, th: Theme, cw: int) -> None:
    rect = skia.Rect.MakeWH(cw, CARD_H)
    c.drawRect(rect, D.paint(th.strip))
    _vgrad(c, rect, [hex_color(th.strip), hex_color(th.accent, 90)], [0.0, 1.0])
    img = D.image(str(it.logo)) if it.logo else None
    if img is not None:                               # the logo, large, stands in for the photo
        k = min(150 / img.height(), (cw - 200) / img.width())
        lw, lh = img.width() * k, img.height() * k
        plate = skia.Rect.MakeXYWH(cw / 2 - lw / 2 - 40, 250 - lh / 2 - 34, lw + 80, lh + 68)
        c.drawRRect(skia.RRect.MakeRectXY(plate, 28, 28), D.paint(it.logo_bg))
        c.drawImageRect(img, skia.Rect.MakeWH(img.width(), img.height()),
                        skia.Rect.MakeXYWH(cw / 2 - lw / 2, 250 - lh / 2, lw, lh),
                        skia.SamplingOptions(skia.CubicResampler.Mitchell()), None)
    if it.image_note:
        nt, nf = D.fit(it.image_note, 22, cw - 2 * M - 40, "Bold", 15)
        nw = nf.measureText(nt)
        pill_r = skia.Rect.MakeXYWH(cw / 2 - nw / 2 - 18, 380, nw + 36, 42)
        c.drawRRect(skia.RRect.MakeRectXY(pill_r, 21, 21), D.paint("#000000", 150))
        D.text(c, nt, cw / 2, 409, nf, D.paint("#ffffff"), align="center")


def card_image(ep: Episode, it: Item, th: Theme, scale: float, flag_out: list | None = None) -> skia.Image:
    """flag_out 给了就不把国旗画进卡片，而是把国旗参数追加进去，由渲染器每帧画飘动的旗（follow-up 008）。"""
    cw = ep.card_w
    surf, c = _surface(cw, scale)
    card = skia.Rect.MakeWH(cw, CARD_H)
    if ep.card_style != "poster" and not it.company_card:   # layout.card_style（paihangbang follow-up 055）
        from .styles import STYLE_FUNCS
        c.save()
        c.clipRRect(skia.RRect.MakeRectXY(card, RADIUS, RADIUS), skia.ClipOp.kIntersect, True)
        STYLE_FUNCS[ep.card_style](c, ep, it, th, cw, flag_out)
        c.restore()
        surf.flushAndSubmit()
        return surf.makeImageSnapshot()
    c.save()
    c.clipRRect(skia.RRect.MakeRectXY(card, RADIUS, RADIUS), skia.ClipOp.kIntersect, True)

    # 1. the photo, full bleed
    img = D.image(str(it.image)) if it.image else None
    co = it.company_card
    if img is not None:
        D.draw_photo(c, img, card, 0, it.image_fit, it.image_focus)
    elif co:
        _company_placeholder(c, it, th, cw)
    else:
        _placeholder(c, ep, it, th, cw, flag_out)

    # scrims: light at the top (flag / rank), strong at the bottom (text)
    _vgrad(c, skia.Rect.MakeXYWH(0, 0, cw, 230), [hex_color("#000000", 120), hex_color("#000000", 0)], [0.0, 1.0])
    bottom = (skia.Rect.MakeXYWH(0, CARD_H * 0.40, cw, CARD_H * 0.60) if co else
              skia.Rect.MakeXYWH(0, CARD_H * 0.47, cw, CARD_H * 0.53))
    _vgrad(c, bottom, [hex_color(th.strip, 0), hex_color(th.strip, 175), hex_color(th.strip, 240)], [0.0, 0.38, 1.0])
    c.restore()

    # 2. the flag (top-left, own aspect ratio); badge under it
    flag_h = CO_FLAG_H if co else FLAG_H
    if ep.show_flags and (img is not None or co):
        _flag(c, ep.flag_path(it.country_iso2), M + 4, M + 4, flag_h, cw * FLAG_MAX_W_FRAC, 4, flag_out)
        badge_y = M + 4 + flag_h + 22
    else:
        badge_y = M + 8
    if it.badge:
        D.pill(c, M, badge_y, it.badge, D.font(20, "ExtraBold"), th.strip, "#ffffff", pad_x=14, h=38)  # dark: white blends into snow
    if it.image_ai and img is not None:   # synthetic image must read as such on a phone (rank_scroll follow-up 010)
        D.pill(c, M, badge_y + (50 if it.badge else 0), tr(D.LANG, "ai_image"), D.font(20, "ExtraBold"), "#f5c518", "#111111", pad_x=14, h=38)

    # rank (or the corner label), top-right; list mode never shows the rank
    rs = it.corner or ("" if ep.is_list else f"#{it.rank}")
    if rs:
        rf = D.font(40 if it.corner else 50, "Black")
        rw = rf.measureText(rs) + 2 * 20
        D.pill(c, cw - M - rw, M + 4, rs, rf, th.accent, th.accent_text, pad_x=20, h=64 if it.corner else 74)

    if co:
        _company_block(c, it, th, cw)
        surf.flushAndSubmit()
        return surf.makeImageSnapshot()

    # 3. the key stat block at the bottom
    inner = cw - 2 * M
    y_value = CARD_H - 96
    sec = it.secondary_display
    sec_f = D.font(30, "SemiBold")
    sec_w = sec_f.measureText(sec) + 18 if sec else 0
    val, vf = D.fit(it.value_display, 84, inner - sec_w, "Black", 60)
    if val != it.value_display:                      # value never ellipsizes: drop the secondary first
        sec, sec_w = "", 0
        val, vf = D.fit(it.value_display, 84, inner, "Black", 52)
    vw = D.text(c, val, M, y_value, vf, _text_paint("#ffffff"))
    if sec:
        D.text(c, sec, M + vw + 18, y_value, sec_f, _text_paint("#ffffff", 190))
    name, nf = D.fit(it.name, 46, inner, "ExtraBold", 28)
    y_name = y_value - vf.getSize() * 0.78 - 26
    D.text(c, name, M, y_name, nf, _text_paint("#ffffff"))
    y_country = y_name - nf.getSize() * 0.78 - 20
    cn, cf = D.fit(it.country_name.upper(), 26, inner, "ExtraBold", 18)
    D.text(c, cn, M, y_country, cf, _text_paint(th.accent))

    _info_line(c, it, M, CARD_H - 50, inner)
    if it.image_credit:
        label = it.image_credit if it.image_credit.startswith(("Render:", "Illustration:")) else tr(D.LANG, "photo") + it.image_credit  # follow-up 007
        if it.image_ai:
            label = tr(D.LANG, "ai_credit")
        cr, crf = D.fit(label, 14, inner, "Medium", 10)
        D.text(c, cr, cw - M, CARD_H - 16, crf, D.paint("#ffffff", 150), align="right")
    surf.flushAndSubmit()
    return surf.makeImageSnapshot()


def insight_image(ep: Episode, ins: Insight, th: Theme, scale: float) -> skia.Image:
    cw = insight_w(ep.card_w)
    surf, c = _surface(cw, scale)
    rect = skia.Rect.MakeWH(cw, CARD_H)
    c.drawRRect(skia.RRect.MakeRectXY(rect, RADIUS, RADIUS), D.paint(th.insight_bg))
    size = 46
    while size > 26:
        f = D.font(size, "Bold")
        lines = D.wrap(ins.text, f, cw - 80)
        if len(lines) * size * 1.25 <= CARD_H - 360:
            break
        size -= 2
    head = 64 + 30 + 44 + 30 + 7 + 50                 # icon, gap, title, gap, rule, gap
    block = head + (len(lines) - 1) * size * 1.25 + size * 0.75
    y0 = (CARD_H - block) / 2
    D.icon(c, "globe", 40, y0, 64, th.insight_text)
    D.text(c, tr(D.LANG, "did_you_know"), 40, y0 + 64 + 30 + 34, D.font(40, "Black"), D.paint(th.insight_text))
    c.drawRect(skia.Rect.MakeXYWH(40, y0 + 64 + 30 + 44 + 30 - 18, 120, 7), D.paint(th.insight_text))
    y = y0 + head + size * 0.75
    for line in lines:
        D.text(c, line, 40, y, f, D.paint(th.insight_text))
        y += size * 1.25
    surf.flushAndSubmit()
    return surf.makeImageSnapshot()
