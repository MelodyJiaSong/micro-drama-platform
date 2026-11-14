# -*- coding: utf-8 -*-
"""Manim 场景按配音时间轴触发（timeline.json 由 tools/edu_video.py timeline 生成）。

    class S1(CuedScene):
        SEGMENT = "s1"
        def construct(self):
            self.at("l01"); self.play(...)      # 等到 l01 开口再播
            self.finish()                         # 补齐到本段配音时长
动画晚于下一句开口会打印「迟到」，渲染日志里查。

双语：同一套场景出两版。环境变量 EDU_LANG=en 时读 timeline.en.json，画面文字用 tr("中文", "English") 取当前语言：
    EDU_LANG=en manim ... --media_dir renders/en/media scenes/t01.py S1
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
from manim import DOWN, FadeOut, Mobject, Scene

LANG = os.environ.get("EDU_LANG", "zh")
if LANG not in ("zh", "en"):
    raise SystemExit(f"EDU_LANG 只支持 zh / en，现为 {LANG}")


def tr(zh: str, en: str) -> str:
    """画面文字取当前语言（EDU_LANG）。"""
    return en if LANG == "en" else zh


def timeline_path(path: Path) -> Path:
    """timeline.json → 当前语言的时间轴（英文 timeline.en.json）。"""
    path = Path(path)
    return path if LANG == "zh" else path.with_name(f"{path.stem}.{LANG}{path.suffix}")


TOP = 5            # 面板层级：面板与面板内容永远压在网格、点阵之上（整组 Rotate 等会把对象提到最上层）


class CuedScene(Scene):
    SEGMENT: str = ""
    TIMELINE: Path | None = None

    def setup(self) -> None:
        tl = json.loads(timeline_path(self.TIMELINE).read_text(encoding="utf-8"))
        seg = tl["segments"][self.SEGMENT]
        self.cues: dict[str, list[float]] = seg["lines"]
        self.seg_duration: float = seg["duration"]
        self.fps: int = tl["fps"]
        self._stack: list[Mobject] = []
        self.box: Mobject | None = None

    # ---------- 画面自检（edu_review.py validate 读渲染日志里的 [layout] 行） ----------
    SAFE_X = 0.25                 # 左右留边（Manim 单位）
    SUB_BAND = 0.95               # 底部字幕带高度，文字不能压进去

    def play(self, *args, **kwargs) -> None:
        super().play(*args, **kwargs)
        self._check_layout()

    def _texts(self) -> list[Mobject]:
        from manim import Text, MarkupText
        out = []
        for m in self.mobjects:
            out += [t for t in m.get_family() if isinstance(t, (Text, MarkupText))]
        return out

    def _check_layout(self) -> None:
        """每次动画后查：文字出画面左右、出上沿、压进底部字幕带；两段可见文字互相重叠。同一问题每段只报一次。"""
        from manim import config
        seen = self.__dict__.setdefault("_layout_seen", set())
        hw, hh = config.frame_width / 2, config.frame_height / 2
        vis = []
        for t in self._texts():
            try:
                if t.get_fill_opacity() < 0.15 or t.width < 1e-3:
                    continue
            except Exception:
                continue
            l, r, b, top = t.get_left()[0], t.get_right()[0], t.get_bottom()[1], t.get_top()[1]
            name = getattr(t, "text", "")[:24]
            probs = []
            if l < -hw + self.SAFE_X or r > hw - self.SAFE_X:
                probs.append("出左右边")
            if top > hh - 0.05:
                probs.append("出上沿")
            if b < -hh + self.SUB_BAND:
                probs.append("压字幕带")
            for p in probs:
                key = (p, name)
                if key not in seen:
                    seen.add(key)
                    print(f"[layout] {self.SEGMENT} t={self.now():.1f}s 「{name}」{p}")
            vis.append((name, l, r, b, top))
        for i in range(len(vis)):
            for j in range(i + 1, len(vis)):
                a, c = vis[i], vis[j]
                ox = min(a[2], c[2]) - max(a[1], c[1])
                oy = min(a[4], c[4]) - max(a[3], c[3])
                if ox > 0.08 and oy > 0.08 and a[0] != c[0]:
                    key = ("重叠", a[0], c[0])
                    if key not in seen:
                        seen.add(key)
                        print(f"[layout] {self.SEGMENT} t={self.now():.1f}s 「{a[0]}」与「{c[0]}」重叠")

    def stack(self, mob: Mobject, gap: float = 0.35) -> Mobject:
        """把 mob 排进 self.box（侧边面板）的下一行，居中、超宽缩放、溢出报警，并抬到面板层级之上。"""
        room = self.box.width - 0.6
        if mob.width > room:
            mob.scale_to_fit_width(room)
        if self._stack:
            mob.next_to(self._stack[-1], DOWN, buff=gap)
        else:
            mob.next_to(self.box.get_top() + DOWN * 0.35, DOWN, buff=0)
        mob.set_x(self.box.get_x())
        self.box.set_z_index(TOP)
        mob.set_z_index(TOP + 1)
        self._stack.append(mob)
        if mob.get_bottom()[1] < self.box.get_bottom()[1] + 0.15:
            print(f"[layout] {self.SEGMENT} 面板溢出")
        return mob

    def clear_stack(self) -> list[Mobject]:
        out, self._stack = self._stack, []
        return out

    def now(self) -> float:
        return self.renderer.time

    def end_of(self, cue: str) -> float:
        return self.cues[cue][1]

    def at(self, cue: str, offset: float = 0.0, edge: int = 0) -> None:
        self.until(self.cues[cue][edge] + offset, cue)

    def until(self, t: float, label: str = "") -> None:
        dt = t - self.now()
        if dt >= 1 / self.fps:
            self.wait(dt)
        elif dt < -0.25:
            print(f"[cue] {self.SEGMENT} {label} 迟到 {-dt:.2f}s")

    def dur(self, cue: str) -> float:
        return self.cues[cue][1] - self.cues[cue][0]

    def mid(self, cue: str, frac: float) -> None:
        """等到某句念到 frac（0–1）处。"""
        self.at(cue, offset=frac * self.dur(cue))

    def fit(self, cue: str, frac: float = 0.8, lo: float = 1.0, hi: float = 4.0) -> float:
        """动画时长：取该句剩余时间的 frac，夹在 [lo, hi]。"""
        return float(np.clip((self.cues[cue][1] - self.now()) * frac, lo, hi))

    def fade_all(self) -> None:
        """段尾淡出全部对象，下一段从干净画面开始。"""
        self.until(self.seg_duration - 0.7, "fade")
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

    def finish(self) -> None:
        self.until(self.seg_duration - 0.5 / self.fps, "end")
        if self.now() > self.seg_duration + 0.5 / self.fps:
            print(f"[cue] {self.SEGMENT} 超出配音 {self.now() - self.seg_duration:.2f}s")
