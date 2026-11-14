# -*- coding: utf-8 -*-
"""把网页图标式 SVG（height="1em"、fill="currentColor"）规整成按 viewBox 定尺寸的独立 SVG，供 skia 栅格化。"""
from __future__ import annotations

import re
from pathlib import Path


def load_svg(path: Path, height: int = 480):
    import skia
    from PIL import Image
    txt = path.read_text(encoding="utf-8", errors="replace")
    txt = txt.replace("currentColor", "#000000")
    m = re.search(r'viewBox="\s*([-\d.]+)[\s,]+([-\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)', txt)
    head = re.search(r"<svg\b[^>]*>", txt, re.S)
    if m and head:
        vw, vh = float(m.group(3)), float(m.group(4))
        tag = re.sub(r'\s(width|height)="[^"]*"', "", head.group(0))
        tag = tag.replace("<svg", f'<svg width="{vw}" height="{vh}"', 1)
        txt = txt[:head.start()] + tag + txt[head.end():]
    dom = skia.SVGDOM.MakeFromStream(skia.MemoryStream(txt.encode("utf-8"), True))
    if dom is None:
        return None
    cs = dom.containerSize()
    w, h = cs.width() or 400, cs.height() or 120
    k = height / h
    surf = skia.Surface(max(1, int(w * k)), height)
    cv = surf.getCanvas()
    cv.clear(skia.ColorTRANSPARENT)
    cv.scale(k, k)
    dom.setContainerSize(skia.Size(w, h))
    dom.render(cv)
    return Image.fromarray(surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType), "RGBA")
