# -*- coding: utf-8 -*-
"""教学视频频道统一的视觉常量与常用构件（Manim），各系列共用。来源：linear_algebra/t03 research.md「视觉约定」。"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
from manim import (DOWN, LEFT, RIGHT, UP, Arrow, BackgroundRectangle, MathTex, NumberPlane, RoundedRectangle,
                   Text, VGroup, config)

BG = "#0f1420"
GRID = "#3b5b8c"
GRID_FAINT = "#26324a"
AXIS = "#c9d4e5"
INK = "#f2f4f8"
MUTED = "#8b97ad"
I_COLOR = "#F59E0B"
J_COLOR = "#14B8A6"
V_COLOR = "#F472B6"
HL = "#FDE68A"
GOOD = "#4ADE80"
BAD = "#F87171"
FONT = "Noto Sans SC"
LATIN_FONT = "Inter"     # 纯西文（英文版、纯数字）用 Inter（OFL）：Noto Sans SC 的西文字距偏紧，粗体 rn 会糊成 m
LATIN_OK = re.compile(r"^[ -ɏ‐-‧′″]*$")   # Inter 拉丁子集能画的：拉丁字母、常用标点（“”—…·）


def _register_latin() -> None:
    """Inter 静态 TTF 在 .cache/fonts/inter/，只在本进程注册，不装进系统。缺了就从 .cache/node/hyperframes 里
    @fontsource/inter 的 woff2 转出（要 fonttools + brotli，Manim 环境已装）。"""
    try:
        import manimpango
    except ImportError:
        return
    repo = Path(__file__).resolve().parents[2]
    out = repo / ".cache" / "fonts" / "inter"
    if not any(out.glob("*.ttf")):
        src = repo / ".cache" / "node" / "hyperframes" / "node_modules" / "@fontsource" / "inter" / "files"
        try:
            from fontTools.ttLib import TTFont
            out.mkdir(parents=True, exist_ok=True)
            for w in (400, 600, 700):
                f = TTFont(src / f"inter-latin-{w}-normal.woff2")
                f.flavor = None
                f.save(out / f"Inter-{w}.ttf")
        except Exception as e:   # 缺字体时退回 Noto Sans SC，不挡渲染
            print(f"[style] Inter 不可用，英文退回 Noto Sans SC：{e}")
            return
    for f in sorted(out.glob("*.ttf")):
        manimpango.register_font(str(f))


_register_latin()
SUB_BAND = 0.95          # 底部留给字幕的高度（Manim 单位）

PANEL_EDGE = GRID_FAINT
config.background_color = BG


def set_stage(bg: str, edge: str = "#2a2a2e") -> None:
    """换舞台底色（AI 高频词用纯黑 #000000，与统一包装一致）；panel / backed 随之换底。在场景模块顶部调用一次。"""
    global BG, PANEL_EDGE
    BG, PANEL_EDGE = bg, edge
    config.background_color = bg


def zh(text: str, size: float = 36, color: str = INK, weight: str = "NORMAL") -> Text:
    """画面文字：纯西文 / 数字用 Inter；含中文或 Inter 拉丁子集没有的符号（→、①）用 Noto Sans SC。"""
    return Text(text, font=LATIN_FONT if LATIN_OK.match(text) else FONT, font_size=size, color=color, weight=weight)


def plane(origin: np.ndarray, faint: bool = False, span: int = 16, unit: float = 1.0) -> NumberPlane:
    p = NumberPlane(x_range=[-span, span, 1], y_range=[-span, span, 1],
                    background_line_style={"stroke_color": GRID_FAINT if faint else GRID,
                                           "stroke_width": 1.5 if faint else 2, "stroke_opacity": 1},
                    axis_config={"stroke_color": MUTED if faint else AXIS, "stroke_width": 2 if faint else 3})
    if faint:
        p.set_opacity(0.55)
    return p.scale(unit, about_point=np.zeros(3)).shift(origin)


def vec(origin: np.ndarray, x: float, y: float, color: str, start: tuple[float, float] = (0, 0),
        unit: float = 1.0) -> Arrow:
    return Arrow(origin + unit * np.array([start[0], start[1], 0]), origin + unit * np.array([x, y, 0]), buff=0,
                 color=color,
                 stroke_width=7, max_tip_length_to_length_ratio=0.22, tip_length=0.28)


def hat(name: str, color: str, prime: bool = False) -> MathTex:
    return MathTex(r"\hat{\imath}" if name == "i" else r"\hat{\jmath}", "'" if prime else "", color=color).scale(1.1)


def panel(width: float = 5.4, height: float = 6.4) -> RoundedRectangle:
    box = RoundedRectangle(corner_radius=0.2, width=width, height=height, stroke_color=PANEL_EDGE, stroke_width=2,
                           fill_color=BG, fill_opacity=0.92)
    return box.to_edge(RIGHT, buff=0.3).shift(UP * (SUB_BAND / 2))


def backed(mob, opacity: float = 0.85):
    return VGroup(BackgroundRectangle(mob, color=BG, fill_opacity=opacity, buff=0.15), mob)


__all__ = ["BG", "GRID", "INK", "MUTED", "I_COLOR", "J_COLOR", "V_COLOR", "HL", "GOOD", "BAD", "FONT", "SUB_BAND",
           "zh", "plane", "vec", "hat", "panel", "backed", "set_stage", "UP", "DOWN", "LEFT", "RIGHT"]
