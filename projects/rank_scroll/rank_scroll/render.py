"""Frame compositor + ffmpeg pipe."""
from __future__ import annotations

import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
import skia

from . import __version__
from . import draw as D
from .cards import PAD, card_image, insight_image
from .i18n import t as tr
from .contract import Episode
from .theme import Theme, get_theme, hex_color
from .timeline import CARD_H, FPS, H, TOP_SCALE, W, XFADE, Timeline, build, insight_w

BAND_CY = 575
COUNT_MARGIN = 20      # a card is counted once it is fully on screen (right edge ≤ W - margin)


def _ease_out(u: float) -> float:
    u = min(1.0, max(0.0, u))
    return 1 - (1 - u) ** 3


@dataclass
class RenderOptions:
    out_scale: float = 1.0      # 1.0 → 1920x1080; 0.5 → 960x540
    step: int = 1               # 1 → 60 fps; 2 → 30 fps
    draft: bool = False


class Renderer:
    def __init__(self, ep: Episode, opts: RenderOptions | None = None):
        self.ep = ep
        self.opts = opts or RenderOptions()
        self.th, self.theme_warning = get_theme(ep.theme)
        self.tl: Timeline = build(ep)
        s = self.opts.out_scale
        self.w, self.h = int(W * s), int(H * s)
        self.buf = np.zeros((self.h, self.w, 4), dtype=np.uint8)
        self.surf = skia.Surface(self.buf, colorType=skia.kBGRA_8888_ColorType, alphaType=skia.kPremul_AlphaType)
        self.canvas = self.surf.getCanvas()
        self._bg = self._make_bg()
        self._elem_img: dict[int, skia.Image] = {}
        self._elem_flags: dict[int, list] = {}
        self._header = self._make_header()
        self._passed_centers = [e.center for e in self.tl.elements]
        self.n_cards = len(ep.items)
        self._top_rank = min(it.rank for it in ep.items)
        self._count_ahead = W / 2 - ep.card_w / 2 - COUNT_MARGIN

    # ---------- cached layers ----------
    def _make_bg(self) -> skia.Image:
        surf = D.surface(self.w, self.h)
        c = surf.getCanvas()
        shader = skia.GradientShader.MakeLinear(
            [skia.Point(0, 0), skia.Point(0, self.h)],
            [hex_color(self.th.bg_top), hex_color(self.th.bg_bottom)])
        c.drawPaint(skia.Paint(Shader=shader))
        # soft vignette
        vg = skia.GradientShader.MakeRadial(skia.Point(self.w / 2, self.h * 0.55), self.w * 0.75,
                                            [hex_color("#000000", 0), hex_color("#000000", 90)])
        c.drawPaint(skia.Paint(Shader=vg))
        return surf.makeImageSnapshot()

    def _elem(self, k: int) -> skia.Image:
        img = self._elem_img.get(k)
        if img is None:
            e = self.tl.elements[k]
            sc = e.scale * self.opts.out_scale
            if e.kind == "card":
                flags: list = []
                img = card_image(self.ep, self.ep.items[e.index], self.th, sc, flag_out=flags)
                self._elem_flags[k] = flags
            else:
                img = insight_image(self.ep, self.ep.insights[e.index], self.th, sc)
            self._elem_img[k] = img
            if len(self._elem_img) > 12:            # keep memory bounded: drop far-left elements
                for old in sorted(self._elem_img)[:-12]:
                    if old < k - 4:
                        del self._elem_img[old]
                        self._elem_flags.pop(old, None)
        return img

    def _make_header(self) -> skia.Image:
        surf = D.surface(W, 130)
        c = surf.getCanvas()
        c.clear(skia.ColorTRANSPARENT)
        kf = D.font(26, "Black")
        kw = D.pill(c, 48, 36, self.ep.kicker, kf, self.th.accent, self.th.accent_text, pad_x=18, h=48)
        title, tf = D.fit(self.ep.title, 40, 1000 - kw, "ExtraBold", 28)
        D.text(c, title, 48 + kw + 20, 74, tf, D.paint(self.th.header_text))
        D.text(c, f"{self.ep.metric_label} · {self.ep.period_label}", 48 + kw + 20, 104, D.font(20, "Medium"),
               D.paint(self.th.header_muted))
        return surf.makeImageSnapshot()

    def _tally_counts(self, upto: int) -> list[tuple[str, str, int]]:
        """(key, label, count) sorted desc for the first `upto` items in countdown order that passed centre."""
        counts: dict[str, list] = {}
        order: list[str] = []
        for e in self.tl.elements[:upto]:
            if e.kind != "card":
                continue
            it = self.ep.items[e.index]
            if self.ep.tally_by == "country":
                key, label = it.country_iso2, it.country_name
            else:
                key, label = it.continent, it.continent
            label = self.ep.tally_labels.get(key, label)   # 固定名称表优先：CN 永远是「中国」，不被「中国台湾」的卡带偏
            if key not in counts:
                counts[key] = [label, 0, it.rank]
                order.append(key)
            counts[key][1] += 1
            counts[key][2] = min(counts[key][2], it.rank)
        # ties: the group holding the better (smaller) best rank goes first
        rows = [(k, counts[k][0], counts[k][1]) for k in order]
        rows.sort(key=lambda r: (-r[2], counts[r[0]][2]))
        return rows

    @lru_cache(maxsize=256)
    def _tally_img(self, upto: int) -> skia.Image:
        rows = self._tally_counts(upto)[:5]
        nf0, lf0 = D.font(30, "Black"), D.font(20, "Bold")

        def block_w(r):
            nw = nf0.measureText(str(r[2]))
            if self.ep.tally_by == "country":
                return 52 + 8 + nw
            return 16 + lf0.measureText(r[1].upper()) + 10 + nw + 16

        while rows and sum(block_w(r) + 22 for r in rows) > 860:   # never spill under the title
            rows = rows[:-1]
        surf = D.surface(900, 130)
        c = surf.getCanvas()
        c.clear(skia.ColorTRANSPARENT)
        D.text(c, self.ep.tally_title.upper(), 880, 30, D.font(16, "Bold"), D.paint(self.th.header_muted), align="right")
        x = 880.0
        nf = D.font(30, "Black")
        for key, label, n in reversed(rows):
            ns = str(n)
            nw = nf.measureText(ns)
            if self.ep.tally_by == "country":
                block = 52 + 8 + nw
                x -= block
                D.flag(c, self.ep.flag_path(key), x, 46, 52, 39, border="#ffffff66")
                D.text(c, ns, x + 60, 77, nf, D.paint(self.th.header_text))
            else:
                lf = D.font(20, "Bold")
                lab = label.upper()
                lw = lf.measureText(lab)
                block = 16 + lw + 10 + nw + 16
                x -= block
                c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, 44, block, 44), 22, 22),
                            D.paint("#ffffff", 34))
                D.text(c, lab, x + 16, 73, lf, D.paint(self.th.header_muted))
                D.text(c, ns, x + 16 + lw + 10, 77, nf, D.paint(self.th.header_text))
            x -= 22
        return surf.makeImageSnapshot()

    # ---------- per-frame drawing (1080p coordinates unless noted) ----------
    def _draw_band(self, f: int, cam: float, offset: float, glow: float = 0.0) -> int:
        """Draw visible elements; return number of elements whose centre is at/left of screen centre."""
        s = self.opts.out_scale
        c = self.canvas
        passed = 0
        for k, e in enumerate(self.tl.elements):
            if e.center <= cam + self._count_ahead:
                passed = k + 1
            sx = W / 2 + (e.center - cam) + offset
            ew = self.ep.card_w if e.kind == "card" else insight_w(self.ep.card_w)
            half = (ew / 2 + PAD) * e.scale
            if sx + half < -50 or sx - half > W + 50:
                continue
            img = self._elem(k)
            anchor_x = round(half * s)
            anchor_y = round((CARD_H / 2 + PAD) * e.scale * s)
            dx = sx * s - anchor_x
            dy = round(BAND_CY * s) - anchor_y
            if glow > 0 and e.kind == "card" and self.ep.items[e.index].rank == self._top_rank:
                gp = skia.Paint(AntiAlias=True, Color=hex_color(self.th.accent, int(230 * glow)))
                gp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30 * s))
                gw, gh = self.ep.card_w * e.scale * s, CARD_H * e.scale * s
                c.save()
                c.resetMatrix()
                c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(sx * s - gw / 2 - 6 * s, BAND_CY * s - gh / 2 - 6 * s,
                                                                     gw + 12 * s, gh + 12 * s), 30 * s, 30 * s), gp)
                c.restore()
            c.save()
            c.resetMatrix()
            c.drawImage(img, dx, dy, skia.SamplingOptions(skia.FilterMode.kLinear), None)
            sc = e.scale * s
            for fl in self._elem_flags.get(k, ()):          # 国旗每帧单独画，一直轻轻飘（follow-up 008）
                layer = D.flag_layer(fl["path"], fl["h"], fl["max_w"], fl["border"], True, round(sc, 4))
                if layer is not None:
                    # 卡片图左上角＝dx,dy；卡片内容再往里 PAD；层比旗框多出 FLAG_MARGIN
                    lx = dx + (PAD + fl["x"] - fl["border"] - D.FLAG_MARGIN) * sc
                    ly = dy + (PAD + fl["y"] - fl["border"] - D.FLAG_MARGIN) * sc
                    D.flag_waving(c, layer, lx, ly, f / FPS, phase=1.7 * k)
            c.restore()
        return passed

    def _chrome(self, passed_elems: int, alpha: int = 255) -> None:
        """Header, tally, progress bar, source line."""
        s = self.opts.out_scale
        c = self.canvas
        c.save()
        c.scale(s, s)
        if alpha < 255:
            c.saveLayerAlpha(None, alpha)
        c.drawImage(self._header, 0, 0, skia.SamplingOptions(skia.FilterMode.kLinear), None)
        c.drawImage(self._tally_img(passed_elems), W - 900 - 30, 0, skia.SamplingOptions(skia.FilterMode.kLinear), None)
        cards_passed = sum(1 for e in self.tl.elements[:passed_elems] if e.kind == "card")
        frac = cards_passed / max(1, self.n_cards)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(48, 1024, W - 96, 6), 3, 3), D.paint("#ffffff", 40))
        if frac > 0:
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(48, 1024, (W - 96) * frac, 6), 3, 3), D.paint(self.th.accent))
        D.text(c, self.ep.source_line, 48, 1062, D.font(19, "Medium"), D.paint(self.th.header_muted))
        D.text(c, self.ep.period_label, W - 48, 1062, D.font(19, "Medium"), D.paint(self.th.header_muted), align="right")
        if alpha < 255:
            c.restore()
        c.restore()

    def _champion_panel(self, t: float) -> None:
        """Right-hand 'No. 1' callout while the champion is centred."""
        champ = self.ep.items[self.tl.elements[-1].index]
        c = self.canvas
        s = self.opts.out_scale
        a = int(255 * _ease_out(t / 0.7))
        dx = 40 * (1 - _ease_out(t / 0.7))
        x0 = W / 2 + self.ep.card_w * TOP_SCALE / 2 + 50 + dx
        c.save()
        c.scale(s, s)
        c.saveLayerAlpha(None, a)
        D.icon(c, "trophy", x0, 300, 150, self.th.accent)
        D.text(c, tr(self.ep.lang, "no1"), x0, 560, D.font(120, "Black"), D.paint(self.th.header_text))
        val, vf = D.fit(champ.value_display, 64, 1880 - x0, "Black", 36)
        D.text(c, val, x0, 650, vf, D.paint(self.th.accent))
        if champ.secondary_display:
            D.text(c, champ.secondary_display, x0, 700, D.font(34, "SemiBold"), D.paint(self.th.header_muted))
        c.restore()
        c.restore()

    def _intro(self, t: float) -> None:
        c = self.canvas
        fade = 1.0 - _ease_out((t - 3.0) / 0.7) if t > 3.0 else 1.0
        if fade <= 0:
            return
        rise = 30 * (1 - _ease_out(t / 0.9))
        a_in = _ease_out(t / 0.6)
        alpha = int(255 * min(fade, a_in))
        s = self.opts.out_scale
        c.save()
        c.scale(s, s)
        c.saveLayerAlpha(None, alpha)
        c.translate(0, rise)
        kf = D.font(34, "Black")
        kw = kf.measureText(self.ep.kicker) + 44
        D.pill(c, W / 2 - kw / 2, 300, self.ep.kicker, kf, self.th.accent, self.th.accent_text, pad_x=22, h=60)
        title, tf = D.fit(self.ep.title, 104, 1720, "Black", 60)
        D.text(c, title, W / 2, 480, tf, D.paint(self.th.header_text), align="center")
        D.text(c, f"{self.ep.metric_label} · {self.ep.period_label}", W / 2, 560, D.font(40, "SemiBold"),
               D.paint(self.th.header_muted), align="center")
        D.text(c, self.ep.source_line, W / 2, 620, D.font(28, "Medium"), D.paint(self.th.header_muted), align="center")
        c.restore()
        c.restore()

    def _panel_bg(self) -> None:
        self.canvas.save()
        self.canvas.resetMatrix()
        self.canvas.drawImage(self._bg, 0, 0)
        self.canvas.restore()

    def _tally_scene(self, t: float) -> None:
        c = self.canvas
        s = self.opts.out_scale
        self._panel_bg()
        all_rows = self._tally_counts(len(self.tl.elements))
        rows = all_rows if len(all_rows) <= 12 else all_rows[:11]
        others = all_rows[len(rows):]
        top = max(r[2] for r in rows) if rows else 1
        c.save()
        c.scale(s, s)
        D.text(c, self.ep.tally_title, W / 2, 150, D.font(64, "Black"), D.paint(self.th.header_text), align="center")
        sub = self.ep.title if self.ep.is_list else tr(self.ep.lang, "tally_sub", kicker=self.ep.kicker if self.ep.lang != "en" else self.ep.kicker.title(), title=self.ep.title)
        D.text(c, sub, W / 2, 200, D.font(28, "Medium"),
               D.paint(self.th.header_muted), align="center")
        n_lines = len(rows) + (1 if others else 0)
        y0, rh = 250, min(92, 770 // max(1, n_lines))
        k = rh / 92                                     # shrink rows when there are many groups
        for i, (key, label, n) in enumerate(rows):
            u = _ease_out((t - 0.3 - i * 0.12) / 1.0)
            y = y0 + i * rh
            x = 300
            if self.ep.tally_by == "country":
                D.flag(c, self.ep.flag_path(key), x, y + 12 * k, 80 * k, 60 * k, border="#ffffff66")
            else:
                D.icon(c, self.ep.tally_icons.get(key, "globe"), x + 18 * k, y + 18 * k, 48 * k, self.th.header_text)
            lab, lf = D.fit(label, 36 * k, 380, "Bold", 18)
            D.text(c, lab, x + 104, y + 56 * k, lf, D.paint(self.th.header_text))
            bar_x, bar_max = 820, 760
            bw = max(8.0, bar_max * n / top * u)
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(bar_x, y + 18 * k, bw, 48 * k), 12 * k, 12 * k),
                        D.paint(self.th.accent if n == top else "#ffffff", 255 if n == top else 70))
            D.text(c, str(n) if u > 0.05 else "", bar_x + bw + 18, y + 56 * k, D.font(36 * k, "Black"),
                   D.paint(self.th.header_text))
        if others:
            y = y0 + len(rows) * rh
            counts = ", ".join(sorted({str(o[2]) for o in others}))
            D.text(c, tr(self.ep.lang, "more", n=len(others), counts=counts) + ("、" if self.ep.lang == "zh" else ", ").join(o[1] for o in others),
                   300, y + 50 * k, D.font(28 * k, "SemiBold"), D.paint(self.th.header_muted))
        c.restore()

    def _sources_scene(self) -> None:
        c = self.canvas
        s = self.opts.out_scale
        self._panel_bg()
        c.save()
        c.scale(s, s)
        D.text(c, tr(self.ep.lang, "sources_title"), W / 2, 330, D.font(60, "Black"), D.paint(self.th.header_text), align="center")
        lines = [
            (self.ep.source_line, 34, "SemiBold", self.th.header_text),
            (self.ep.period_label, 30, "Medium", self.th.header_muted),
            ((tr(self.ep.lang, "image_credits_line")
              if any(it.image is not None and not it.image_withheld for it in self.ep.items)
              else "No images are shown in this version"), 28, "Medium", self.th.header_muted),   # follow-up 008
            (("Flags: flagcdn.com (public domain) · " if self.ep.show_flags else "") + "Icons: Tabler Icons (MIT) · Font: " + ("Noto Sans SC (OFL)" if self.ep.lang == "zh" else "Inter (OFL)"), 24, "Medium",
             self.th.header_muted),
        ]
        y = 430
        for txt, size, wt, col in lines:
            t2, f = D.fit(txt, size, 1700, wt, 18)
            D.text(c, t2, W / 2, y, f, D.paint(col), align="center")
            y += size * 2.0
        c.restore()

    def _end_scene(self, t: float) -> None:
        c = self.canvas
        s = self.opts.out_scale
        self._panel_bg()
        c.save()
        c.scale(s, s)
        a = int(255 * _ease_out(t / 0.6))
        c.saveLayerAlpha(None, a)
        D.text(c, tr(self.ep.lang, "thanks"), W / 2, 190, D.font(72, "Black"), D.paint(self.th.header_text), align="center")
        D.text(c, tr(self.ep.lang, "next_list" if self.ep.is_list else "next_rank"), W / 2, 260, D.font(34, "Medium"),
               D.paint(self.th.header_muted), align="center")
        c.restore()
        c.restore()

    def frame(self, f: int) -> np.ndarray:
        tl = self.tl
        c = self.canvas
        c.save()
        c.resetMatrix()
        c.drawImage(self._bg, 0, 0)
        c.restore()
        name, a, b = tl.segment_at(f)
        t = (f - a) / FPS
        last = len(tl.elements)
        if name in ("intro", "scroll", "champion") or (name == "tally" and t < XFADE):
            cam = tl.camera(min(f, tl.segments[1][2]))
            offset = tl.band_offset(f) if name == "intro" else 0.0
            glow = 0.0
            if self.ep.is_list:
                pass                                         # list mode: no champion glow
            elif name == "champion":
                glow = 0.65 + 0.35 * math.sin(t * math.pi * 1.2)
            elif name == "scroll" and f >= tl.segments[1][2] - tl.f_ease:
                glow = 0.65 * (f - (tl.segments[1][2] - tl.f_ease)) / tl.f_ease
            elif name == "tally":
                glow = 0.65
            passed = self._draw_band(f, cam, offset, glow) if (name != "intro" or offset < W + 150) else 0
            n_top = sum(1 for it in self.ep.items if it.rank == self._top_rank)
            if n_top == 1 and not self.ep.is_list and (name == "champion" or (name == "tally" and t < XFADE)):
                self._champion_panel(t if name == "champion" else tl.f_champ / FPS)
            if name == "intro":
                ti = f / FPS
                if ti > 4.2:
                    self._chrome(passed, int(255 * _ease_out((ti - 4.2) / 0.8)))
                self._intro(ti)
            else:
                self._chrome(passed if name != "tally" else last)
        if name == "tally":
            if t < XFADE:
                c.saveLayerAlpha(None, int(255 * t / XFADE))
                self._tally_scene(t)
                c.restore()
            else:
                self._tally_scene(t)
        elif name == "sources":
            if t < XFADE:
                self._tally_scene(tl.f_tally / FPS)
                c.saveLayerAlpha(None, int(255 * t / XFADE))
                self._sources_scene()
                c.restore()
            else:
                self._sources_scene()
        elif name == "end":
            if t < XFADE:
                self._sources_scene()
                c.saveLayerAlpha(None, int(255 * t / XFADE))
                self._end_scene(t)
                c.restore()
            else:
                self._end_scene(t)
        self.surf.flushAndSubmit()
        return self.buf

    # ---------- outputs ----------
    def save_png(self, f: int, path: Path) -> None:
        self.frame(f)
        self.surf.makeImageSnapshot().save(str(path), skia.kPNG)


def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


MUSIC_XFADE = 4.0


def parse_track(spec: str | Path) -> tuple[Path, float | None, float | None]:
    """'song.mp3', 'song.mp3@12.5', 'song.mp3@:188' or 'song.mp3@12.5:188' → (path, in, out) in seconds."""
    s = str(spec)
    if "@" in s:
        p, rng = s.rsplit("@", 1)
        m = re.fullmatch(r"(\d+(?:\.\d+)?)?(?::(\d+(?:\.\d+)?))?", rng)
        if m and rng:
            return Path(p), (float(m.group(1)) if m.group(1) else None), (float(m.group(2)) if m.group(2) else None)
    return Path(s), None, None


def _duration(ffprobe: str, p: Path) -> float:
    r = subprocess.run([ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def build_music_bed(specs: list, full_dur: float, t_from: float, dur: float, fit: str, out_wav: Path,
                    log=print) -> dict:
    """Music bed as a WAV, built before the video so loudnorm can run two passes (linear, no gain drift).

    Tracks are trimmed to their in/out points and chained with 4 s crossfades; the chain loops if still short.
    fit='end': if the chain is longer than the video, skip the surplus from the START of the last track, so the
    last track plays to its own natural ending exactly at the end of the video (rank_scroll follow-up: audio QC
    found an intro/outro energy hole at the junction and a cut-off ending).
    """
    ffmpeg, ffprobe = shutil.which("ffmpeg"), shutil.which("ffprobe")
    segs = []
    for spec in specs:
        p, a, b = parse_track(spec)
        length = _duration(ffprobe, p)
        segs.append([p, a or 0.0, min(b, length) if b else length])
    total = sum(b - a for _, a, b in segs) - MUSIC_XFADE * (len(segs) - 1)
    if fit == "end" and total > full_dur:
        last = segs[-1]
        last[1] = min(last[1] + (total - full_dur), last[2] - 2 * MUSIC_XFADE)
    inputs, parts = [], []
    for k, (p, a, b) in enumerate(segs):
        inputs += ["-i", str(p)]
        parts.append(f"[{k}:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo[s{k}]")
    last = "s0"
    for k in range(1, len(segs)):
        parts.append(f"[{last}][s{k}]acrossfade=d={MUSIC_XFADE}:c1=qsin:c2=qsin[x{k}]")
        last = f"x{k}"
    base = (";".join(parts) + f";[{last}]aloop=loop=-1:size=2147483647,atrim={t_from:.3f}:{t_from + dur:.3f},"
            f"asetpts=PTS-STARTPTS,afade=t=in:st=0:d=1,afade=t=out:st={max(0.0, dur - 3.0):.3f}:d=3")
    target = "I=-16:TP=-1.5:LRA=11"
    r = subprocess.run([ffmpeg, "-hide_banner", "-nostats", *inputs, "-filter_complex",
                        f"{base},loudnorm={target}:print_format=json[a]", "-map", "[a]", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1]
    meas = json.loads(blob)
    second = (f"loudnorm={target}:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
              f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}:linear=true")
    subprocess.run([ffmpeg, "-y", "-hide_banner", "-loglevel", "error", *inputs, "-filter_complex",
                    f"{base},{second},aresample=48000[a]", "-map", "[a]", "-c:a", "pcm_s16le", str(out_wav)], check=True)
    log(f"music bed: {len(segs)} track(s), chain {total:.1f}s for {full_dur:.1f}s video, fit={fit}, "
        f"input {meas['input_i']} LUFS → -16 (linear)")
    return {"tracks": [{"path": str(p), "sha256": _sha(p), "in_s": round(a, 3), "out_s": round(b, 3)} for p, a, b in segs],
            "fit": fit, "crossfade_s": MUSIC_XFADE, "loudnorm_pass1": meas}


def render_video(ep: Episode, out: Path, opts: RenderOptions, music: Path | list | None = None,
                 t_from: float | None = None, t_to: float | None = None, log=print, music_fit: str = "none") -> dict:
    r = Renderer(ep, opts)
    tl = r.tl
    f0 = int((t_from or 0) * FPS)
    f1 = min(tl.total_frames, int(t_to * FPS) if t_to else tl.total_frames)
    frames = list(range(f0, f1, opts.step))
    fps_out = FPS // opts.step
    dur = len(frames) / fps_out
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found on PATH")
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{r.w}x{r.h}", "-r", str(fps_out), "-i", "-"]
    specs = list(music) if isinstance(music, (list, tuple)) else ([music] if music else [])
    bed_wav, bed_info = out.with_name(out.stem + ".music.wav"), None
    if specs:
        bed_info = build_music_bed(specs, tl.total_frames / FPS, f0 / FPS, dur, music_fit, bed_wav, log)
        cmd += ["-i", str(bed_wav), "-map", "0:v", "-map", "1:a"]
    else:
        cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-map", "0:v", "-map", "1:a"]
    if opts.draft:
        cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "23"]  # NVENC needs driver >= 610 (2026-11-03: 596.58)
    else:
        cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "16", "-profile:v", "high"]
    cmd += ["-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-t", f"{dur:.3f}",
            "-movflags", "+faststart", str(out)]
    log(f"rendering {len(frames)} frames ({dur:.1f}s @ {fps_out}fps, {r.w}x{r.h}) → {out}")
    t0 = time.time()
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    try:
        for n, f in enumerate(frames):
            buf = r.frame(f)
            proc.stdin.write(buf.data)
            if n and n % (fps_out * 30) == 0:
                el = time.time() - t0
                log(f"  {n}/{len(frames)} frames, {n / el:.1f} fps, eta {(len(frames) - n) / (n / el):.0f}s")
        proc.stdin.close()
    except BrokenPipeError:
        pass
    rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"ffmpeg exited with {rc}")
    elapsed = time.time() - t0
    inputs = {"data.json": _sha(ep.root / "data.json")}
    if (ep.root / "assets.json").is_file():
        inputs["assets.json"] = _sha(ep.root / "assets.json")
    for it in ep.items:
        if it.image:
            inputs[str(it.image.relative_to(ep.root)).replace("\\", "/")] = _sha(it.image)
    if bed_info:
        inputs["music"] = bed_info["tracks"]
        inputs["music_bed"] = {k: v for k, v in bed_info.items() if k != "tracks"}
        bed_wav.unlink(missing_ok=True)
    manifest = {
        "renderer": f"rank_scroll {__version__}", "output": str(out), "output_sha256": _sha(out),
        "duration_s": round(dur, 3), "fps": fps_out, "size": [r.w, r.h], "draft": opts.draft,
        "range_s": [f0 / FPS, f1 / FPS], "theme": r.th.name, "render_seconds": round(elapsed, 1),
        "timeline": [[n, a / FPS, b / FPS] for n, a, b in tl.segments], "inputs": inputs,
        "ffmpeg": cmd, "python": sys.version.split()[0], "skia": skia.__version__,
    }
    out.with_suffix(".manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    log(f"done in {elapsed:.0f}s ({len(frames) / elapsed:.1f} fps)")
    return manifest


def render_thumb(ep: Episode, out: Path) -> None:
    th, _ = get_theme(ep.theme)
    w, h = 1280, 720
    surf = D.surface(w, h)
    c = surf.getCanvas()
    shader = skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, h)],
                                            [hex_color(th.bg_top), hex_color(th.bg_bottom)])
    c.drawPaint(skia.Paint(Shader=shader))
    picked = [it for it in ep.items if it.thumb]
    top3 = (picked or sorted(ep.items, key=lambda it: it.rank))[:3]
    pw = (w - 80) / 3
    for i, it in enumerate(top3):
        x = 40 + i * pw
        rect = skia.Rect.MakeXYWH(x + 8, 250, pw - 16, 420)
        img = D.image(str(it.image)) if it.image else None
        if img is not None:
            D.draw_cover(c, img, rect, 18)
        else:
            c.drawRRect(skia.RRect.MakeRectXY(rect, 18, 18), D.paint(th.strip))
            ic = {"alpine": "mountain", "skyline": "building", "virus": "virus"}.get(th.name, "globe")
            D.icon(c, ic, rect.centerX() - 70, rect.centerY() - 90, 140, th.accent)
            nm, nf = D.fit(it.name, 40, rect.width() - 40, "Black", 24)
            D.text(c, nm, rect.centerX(), rect.centerY() + 100, nf, D.paint("#ffffff"), align="center")
        if ep.show_flags:
            D.flag(c, ep.flag_path(it.country_iso2), x + 24, 266, 84, 63, border="#ffffffaa")
        if it.image_ai and img is not None:   # 与卡片同款 AI IMAGE 角标（rank_scroll follow-up 010 / 016）
            D.pill(c, x + 24, 266 + (63 + 12 if ep.show_flags else 0), tr(D.LANG, "ai_image"), D.font(22, "ExtraBold"),
                   "#f5c518", "#111111", pad_x=14, h=40)
        if it.logo is not None:             # company card: logo plate so the viewer knows whose photo it is
            from .cards import _logo_plate
            _logo_plate(c, it, x + 24, 526, pw - 64, h=62)
        D.pill(c, x + 24, 600, it.value_display if ep.is_list else f"#{it.rank}  {it.value_display}" + (f" {it.secondary_display}" if it.secondary_display in ("est.", "reported") else ""), D.font(30, "Black"), th.accent, th.accent_text, 16, 52)
    kf = D.font(40, "Black")
    kw = D.pill(c, 40, 50, ep.kicker, kf, th.accent, th.accent_text, 20, 64)
    full = ep.title.upper()
    avail = w - 80 - kw - 30
    title, tf = D.fit(full, 76, avail, "Black", 40)
    if title != full:                       # too long even at the minimum size: wrap to two lines, never ellipsize
        f2 = D.font(50, "Black")
        for n, line in enumerate(D.wrap(full, f2, avail)[:2]):
            D.text(c, line, 40 + kw + 30, 80 + n * 58, f2, D.paint(th.header_text))
    else:
        D.text(c, title, 40 + kw + 30, 104, tf, D.paint(th.header_text))
    D.text(c, ep.period_label, 40, 200, D.font(34, "SemiBold"), D.paint(th.header_muted))
    surf.makeImageSnapshot().save(str(out), skia.kPNG)
