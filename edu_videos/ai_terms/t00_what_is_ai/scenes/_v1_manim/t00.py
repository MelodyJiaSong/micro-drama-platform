# -*- coding: utf-8 -*-
"""t00 什么是 AI（v1，节目模板 v2）：s1–s7 七段画面，按时间轴的句子触发；s0 本期内容、s8 片尾与章节转场是统一包装卡
（tools/edu_package.py）。手写数字、准确率与「把握」都来自 experiment.py 算出的 assets/digits_experiment.json，
不手写数据。中英两版共用本文件，画面文字用 T(中文, English)。

    python edu_videos/ai_terms/t00_what_is_ai/experiment.py          # 先算实验（系统 Python，要 sklearn）
    python tools/edu_video.py render edu_videos/ai_terms/t00_what_is_ai [--lang en] [S1 ...]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from manim import *

HERE = Path(__file__).resolve()
sys.path[:0] = [str(HERE.parents[4] / "tools"), str(HERE.parents[3] / "_shared")]
from edu_manim import TOP, CuedScene, tr  # noqa: E402
import style  # noqa: E402
from style import BAD, GOOD, HL, I_COLOR, INK, J_COLOR, MUTED, V_COLOR, backed, zh  # noqa: E402

style.set_stage("#000000")          # AI 高频词：纯黑舞台，与片头 / 转场 / 片尾一致
ASSETS = HERE.parents[1] / "assets"
EXP = json.loads((ASSETS / "digits_experiment.json").read_text(encoding="utf-8"))
ACC = dict(zip(EXP["sizes"], EXP["accuracy"]))
PCT = lambda v: round(100 * v)
assert EXP["n_total"] == 1797 and EXP["n_test"] == 300 and EXP["n_pool"] == 1497, "讲稿 l20/l21/l24 的张数"
assert (PCT(ACC[10]), PCT(ACC[100]), PCT(ACC[1497])) == (37, 88, 97), "讲稿 l22–l24 的准确率，实验变了要同步改讲稿"
assert EXP["full_wrong"] == 10, "讲稿 l26「错了十道」"
assert EXP["probe"]["true"] == 3 and PCT(max(EXP["probe"]["proba"])) == 96, "讲稿 l28「96% 是三」"
OOD_A = EXP["ood"]["A"]
WRONG_2 = next(w for w in EXP["wrong_examples"] if w["true"] == 2)
assert (OOD_A["pred"], PCT(OOD_A["conf"])) == (4, 92), "讲稿 l38「字母 A，92% 是四」"
assert (WRONG_2["pred"], PCT(WRONG_2["conf"])) == (1, 81), "讲稿 l39「这张二，81% 说是一」"

RULE_C, DATA_C, MODEL_C, ANS_C = I_COLOR, J_COLOR, V_COLOR, HL
SRC_DIGITS = ("数据：UCI 手写数字（Alpaydin & Kaynak，1998），CC BY 4.0 · 经 scikit-learn 加载，已改画",
              "Data: Optical Recognition of Handwritten Digits, Alpaydin & Kaynak (1998), UCI ML Repository, CC BY 4.0 · via scikit-learn, adapted")


def T(cn: str, en: str, size: float = 36, color: str = INK, weight: str = "NORMAL") -> Text:
    """按当前语言（EDU_LANG）出字。英文字号略小一档，行宽与中文接近。"""
    return zh(tr(cn, en), size if tr("zh", "en") == "zh" else size * 0.92, color, weight)


def fit_w(mob: Mobject, w: float) -> Mobject:
    return mob.scale_to_fit_width(w) if mob.width > w else mob


# ---------- 画面构件 ----------
def digit(img: list[list[float]], size: float = 1.2, color: str = INK, frame: bool = False) -> VGroup:
    """8×8 手写数字：每格一个方块，墨水越浓越亮（数据 0–1）。frame=True 画出格线（讲「八乘八个格子」时用）。"""
    a = np.asarray(img, dtype=float)
    cell = size / 8
    g = VGroup()
    for r in range(8):
        for c in range(8):
            sq = Square(cell, stroke_width=0, fill_color=color, fill_opacity=float(np.clip(a[r, c], 0, 1)) * 0.95)
            if frame:
                sq.set_stroke(MUTED, 1, opacity=0.6)
            g.add(sq.move_to(np.array([(c - 3.5) * cell, (3.5 - r) * cell, 0])))
    return g


def tile(img, size: float = 1.0, color: str = INK) -> VGroup:
    """带暗底的数字小卡，排成网格时彼此分得开。"""
    d = digit(img, size * 0.82, color)
    bg = RoundedRectangle(corner_radius=0.06, width=size, height=size, stroke_color=style.PANEL_EDGE, stroke_width=1.5,
                          fill_color="#111114", fill_opacity=1)
    return VGroup(bg, d)


def box(label: Text, color: str, w: float = 2.6, h: float = 1.2) -> VGroup:
    r = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=0.12)
    fit_w(label, w - 0.3)
    return VGroup(r, label.move_to(r))


def arrow(a: Mobject, b: Mobject, color: str = MUTED) -> Arrow:
    return Arrow(a.get_right(), b.get_left(), buff=0.15, color=color, stroke_width=5, max_tip_length_to_length_ratio=0.25)


def statement(*lines: Text, buff: float = 0.35) -> VGroup:
    """居中大字（发布会式）：一到两行，留白。"""
    g = VGroup(*lines).arrange(DOWN, buff=buff).move_to(UP * 0.4)
    return fit_w(g, 12.5)


def image(name: str, height: float) -> ImageMobject:
    return ImageMobject(str(ASSETS / name)).set_height(height)


def cross(m: Mobject, color: str = BAD) -> VGroup:
    return Cross(m, stroke_color=color, stroke_width=6, scale_factor=0.9)


def icon_camera() -> VGroup:
    body = RoundedRectangle(corner_radius=0.12, width=1.2, height=0.8, stroke_color=INK, stroke_width=4)
    lens = Circle(0.24, color=INK, stroke_width=4).move_to(body)
    bump = Rectangle(width=0.36, height=0.14, stroke_color=INK, stroke_width=4).next_to(body, UP, buff=0).shift(LEFT * 0.25)
    return VGroup(body, lens, bump)


def icon_wave() -> VGroup:
    hs = [0.2, 0.5, 0.85, 0.45, 0.7, 0.3, 0.6, 0.25]
    return VGroup(*[Line(DOWN * h / 2, UP * h / 2, color=INK, stroke_width=6) for h in hs]).arrange(RIGHT, buff=0.12)


def icon_chat() -> VGroup:
    a = RoundedRectangle(corner_radius=0.18, width=1.1, height=0.5, stroke_color=INK, stroke_width=4)
    b = RoundedRectangle(corner_radius=0.18, width=0.9, height=0.45, stroke_color=INK, stroke_width=4, fill_color=INK,
                         fill_opacity=0.25).next_to(a, DOWN, buff=0.12).shift(RIGHT * 0.3)
    return VGroup(a, b)


class Base(CuedScene):
    TIMELINE = HERE.parents[1] / "timeline.json"

    def flow(self, items: list[VGroup], y: float = 0.6) -> VGroup:
        """一行流程：盒子 → 盒子 → 盒子（含箭头），水平居中。"""
        row = VGroup(*items).arrange(RIGHT, buff=1.0).move_to(UP * y)
        fit_w(row, 12.8)
        arrows = VGroup(*[arrow(items[i], items[i + 1]) for i in range(len(items) - 1)])
        return VGroup(row, arrows)


class S1(Base):
    """① 问题：身边的 AI → 传统程序靠人写规则 → 手写的 3 写不出规则。"""
    SEGMENT = "s1"

    def construct(self) -> None:
        self.at("l07")
        cards = []
        for ic, (cn, en), out in ((icon_camera(), ("相册认猫", "Find the cat"), T("猫", "Cat", 30, HL)),
                                  (icon_wave(), ("语音转文字", "Speech to text"), T("文字", "Text", 30, HL)),
                                  (icon_chat(), ("聊天机器人", "Chatbots"), T("回答", "Reply", 30, HL))):
            frame = RoundedRectangle(corner_radius=0.25, width=3.4, height=3.0, stroke_color=style.PANEL_EDGE,
                                     stroke_width=2, fill_color="#111114", fill_opacity=1)
            ic.move_to(frame.get_center() + UP * 0.45)
            lab = fit_w(T(cn, en, 28, MUTED), 3.0).next_to(ic, DOWN, buff=0.35)
            cards.append(VGroup(frame, ic, lab))
        row = VGroup(*cards).arrange(RIGHT, buff=0.5).move_to(UP * 0.7)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.25) for c in cards], lag_ratio=0.35), run_time=self.fit("l07", 0.4, 1.5, 2.6))
        self.mid("l07", 0.62)
        tag = T("这些都叫 AI", "We call all of this AI", 44, INK, weight="BOLD").next_to(row, DOWN, buff=0.55)
        self.play(FadeIn(tag, shift=UP * 0.15), run_time=0.7)
        self.mid("l07", 0.85)
        q = T("它到底是什么？", "But what is it, really?", 44, HL, weight="BOLD").move_to(tag)
        self.play(ReplacementTransform(tag, q), run_time=0.6)

        self.at("l08")
        self.play(FadeOut(row), FadeOut(q), run_time=0.5)
        head = T("传统程序", "A traditional program", 36, MUTED).to_edge(UP, buff=0.6)
        rules = box(T("人写的规则", "Rules people write", 30, RULE_C), RULE_C)
        inp = box(T("输入", "Input", 30, DATA_C), DATA_C, w=2.0)
        left = VGroup(rules, inp).arrange(DOWN, buff=0.35)
        prog = box(T("电脑执行", "Computer runs it", 30), INK, w=2.8)
        ans = box(T("答案", "Answer", 30, ANS_C), ANS_C, w=2.0)
        fl = self.flow([left, prog, ans], y=0.4)
        self.play(FadeIn(head), FadeIn(rules, shift=RIGHT * 0.2), run_time=0.8)
        self.play(FadeIn(inp, shift=RIGHT * 0.2), GrowArrow(fl[1][0]), FadeIn(prog), run_time=1.0)
        self.play(GrowArrow(fl[1][1]), FadeIn(ans), run_time=0.8)

        self.at("l09")
        ok = VGroup(T("算工资", "Payroll", 32), T("订机票", "Booking flights", 32), T("✓ 规则说得清", "✓ clear rules", 32, GOOD))
        ok.arrange(RIGHT, buff=0.7).next_to(fl, DOWN, buff=0.8)
        self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.15) for o in ok], lag_ratio=0.3), run_time=1.2)

        self.at("l10")
        self.play(FadeOut(VGroup(head, fl, ok)), run_time=0.5)
        three = digit(EXP["threes"][0], 3.2, INK, frame=True).move_to(LEFT * 3.0 + UP * 0.4)
        qq = T("规则是什么？", "What's the rule?", 44, HL, weight="BOLD").move_to(RIGHT * 3.0 + UP * 0.4)
        self.play(FadeIn(three, scale=0.9), run_time=0.9)
        self.play(FadeIn(qq), run_time=0.6)

        self.at("l11")
        tiles = VGroup(*[tile(t, 1.1) for t in EXP["threes"]]).arrange_in_grid(rows=2, buff=0.2).move_to(UP * 1.95)
        self.play(FadeOut(qq), ReplacementTransform(three, tiles[0]), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(t, scale=0.8) for t in tiles[1:]], lag_ratio=0.08), run_time=1.4)
        # 每条规则配一个反例：别的数字也符合，所以规则分不出 3（审稿 M4：否定要有理由）
        rules = (("规则 1：上下两个弯？", "Rule 1: two bumps?", "8", "8 也是", "So is an 8"),
                 ("规则 2：下半开口朝左？", "Rule 2: bottom opens left?", "5", "5 也是", "So is a 5"),
                 ("规则 3：一笔连下来？", "Rule 3: one stroke?", "2", "2 也是", "So is a 2"))
        tries = VGroup()
        for cn, en, k, ccn, cen in rules:
            r = T(cn, en, 26, RULE_C)
            ex = VGroup(tile(EXP["samples"][k][0], 0.75), T(ccn, cen, 24, BAD)).arrange(RIGHT, buff=0.15)
            tries.add(VGroup(r, ex).arrange(DOWN, buff=0.15))
        tries.arrange(RIGHT, buff=0.7)
        fit_w(tries, 12.5).next_to(tiles, DOWN, buff=0.4)
        self.mid("l11", 0.5)
        for t in tries:     # 规则先亮出来，再出反例、规则变灰
            self.play(FadeIn(t[0], shift=UP * 0.1), run_time=0.3)
            self.play(FadeIn(t[1], shift=UP * 0.1), t[0].animate.set_color(MUTED), run_time=0.35)
        self.mid("l11", 0.85)
        never = T("写多少条都不够", "No number of rules is enough", 36, BAD, weight="BOLD").next_to(tries, DOWN, buff=0.3)
        self.play(FadeIn(never, shift=UP * 0.15), run_time=0.6)
        self.fade_all()
        self.finish()


class S2(Base):
    """换个做法：不写规则、给例子 → 机器学习 → 模型。"""
    SEGMENT = "s2"

    def construct(self) -> None:
        self.at("l12")
        a = T("写规则", "Write rules", 64, INK, weight="BOLD")
        b = T("给例子", "Give examples", 64, HL, weight="BOLD")
        st = statement(a, b, buff=0.45)
        self.play(FadeIn(a, shift=UP * 0.2), run_time=0.7)
        self.play(Create(cross(a, BAD)), a.animate.set_color(MUTED), run_time=0.4)
        self.play(FadeIn(b, shift=UP * 0.2), run_time=0.7)

        self.at("l13")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)
        picks = []
        for k in range(10):
            for j in range(2):
                picks.append((EXP["samples"][str(k)][j], k))
        cards = VGroup()
        for img, k in picks:
            t = tile(img, 0.95)
            lab = zh(str(k), 24, ANS_C).next_to(t, DOWN, buff=0.08)
            cards.add(VGroup(t, lab))
        cards.arrange_in_grid(rows=2, buff=(0.22, 0.3)).move_to(UP * 0.9)
        fit_w(cards, 12.6)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in cards], lag_ratio=0.06), run_time=self.fit("l13", 0.55, 1.8, 3.2))
        hint = T("每张都带着答案", "Every one comes with its answer", 30, ANS_C).next_to(cards, DOWN, buff=0.45)
        self.play(FadeIn(hint), *[Indicate(c[1], color=ANS_C) for c in cards], run_time=1.0)

        self.at("l14")
        ex = box(T("例子 + 答案", "Examples + answers", 30, DATA_C), DATA_C, w=3.2)
        learn = box(T("学习", "Learning", 32, INK, weight="BOLD"), INK, w=2.2)
        model = box(T("规律（模型）", "Pattern (model)", 30, MODEL_C), MODEL_C, w=3.2)
        fl = self.flow([ex, learn, model], y=-0.2)
        self.play(FadeOut(hint), cards.animate.scale(0.55).to_edge(UP, buff=0.35), run_time=0.7)
        self.play(FadeIn(ex), GrowArrow(fl[1][0]), FadeIn(learn), run_time=0.9)
        self.play(GrowArrow(fl[1][1]), FadeIn(model), run_time=0.8)
        self.mid("l14", 0.6)
        name = T("机器学习", "Machine learning", 44, HL, weight="BOLD").next_to(fl, DOWN, buff=0.6)
        sub = T("machine learning", "机器学习", 28, MUTED).next_to(name, DOWN, buff=0.12)
        self.play(FadeIn(name, shift=UP * 0.15), FadeIn(sub), run_time=0.7)

        self.at("l15")
        self.play(FadeOut(VGroup(cards, name, sub, ex, learn, fl[1])), model.animate.move_to(ORIGIN + UP * 0.3), run_time=0.7)
        new = tile(EXP["probe"]["img"], 1.6).next_to(model, LEFT, buff=1.4)
        ql = T("新图", "New image", 26, MUTED).next_to(new, DOWN, buff=0.15)
        out = zh("3", 96, ANS_C, weight="BOLD").next_to(model, RIGHT, buff=1.4)
        a1, a2 = arrow(new, model), arrow(model, out)
        self.play(FadeIn(new, shift=RIGHT * 0.2), FadeIn(ql), GrowArrow(a1), run_time=0.8)
        self.play(Indicate(model, color=MODEL_C), run_time=0.6)
        self.play(GrowArrow(a2), FadeIn(out, scale=1.3), run_time=0.7)
        self.fade_all()
        self.finish()


class S3(Base):
    """② 类比：教小孩认字（不给说明书，给例子）；照菜谱做菜 vs 尝遍百菜自己总结菜谱。"""
    SEGMENT = "s3"

    def construct(self) -> None:
        self.at("l16")
        kid = image("child_v1.png", 5.0).set_width(6.8).to_edge(LEFT, buff=0.3).shift(UP * 0.45)
        self.play(FadeIn(kid, shift=UP * 0.2), run_time=0.9)
        self.mid("l16", 0.35)
        book = RoundedRectangle(corner_radius=0.15, width=5.2, height=2.4, stroke_color=MUTED, stroke_width=2,
                                fill_color="#111114", fill_opacity=1)
        bt = VGroup(T("说明书", "The manual", 28, MUTED),
                    T("三 = 两个半圆叠在一起", "3 = two half circles, stacked", 32)).arrange(DOWN, buff=0.25).move_to(book)
        fit_w(bt, 4.8)
        manual = VGroup(book, bt).move_to(RIGHT * 3.6 + UP * 0.45)
        self.play(FadeIn(manual, shift=LEFT * 0.2), run_time=0.8)
        self.mid("l16", 0.8)
        x = cross(manual)
        self.play(Create(x), run_time=0.5)

        self.at("l17")
        self.play(FadeOut(manual), FadeOut(x), run_time=0.4)
        threes = VGroup(*[tile(t, 1.0) for t in EXP["threes"][:6]]).arrange_in_grid(rows=2, buff=0.2)
        say = T("“这是三。”", "“This is a three.”", 36, ANS_C, weight="BOLD")
        grp = VGroup(say, threes).arrange(DOWN, buff=0.4).move_to(RIGHT * 3.6 + UP * 0.45)
        self.play(FadeIn(say), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(t, scale=0.8) for t in threes], lag_ratio=0.25), run_time=self.fit("l17", 0.45, 1.5, 3.0))
        self.mid("l17", 0.75)
        got = T("没见过的写法也认得出", "Even handwriting they've never seen", 30, GOOD).next_to(threes, DOWN, buff=0.35)
        fit_w(got, 5.6)
        self.play(FadeIn(got, shift=UP * 0.1), run_time=0.6)

        self.at("l18")
        self.play(FadeOut(Group(kid, grp, got)), run_time=0.5)
        c1 = image("cook_recipe_v1.png", 3.6).move_to(LEFT * 3.4 + UP * 1.0)
        c2 = image("cook_taste_v1.png", 3.6).move_to(RIGHT * 3.4 + UP * 1.0)
        l1 = T("照着菜谱，一步一步做", "Follows the recipe, step by step", 30, RULE_C).next_to(c1, DOWN, buff=0.25)
        l2 = T("尝过一千道菜，自己琢磨出菜谱", "Tastes a thousand dishes, works out the recipe", 30, DATA_C).next_to(c2, DOWN, buff=0.25)
        fit_w(l1, 6.0), fit_w(l2, 6.0)
        self.play(FadeIn(c1, shift=UP * 0.2), FadeIn(l1), run_time=0.9)
        self.mid("l18", 0.5)
        self.play(FadeIn(c2, shift=UP * 0.2), FadeIn(l2), run_time=0.9)

        self.at("l19")
        t1 = T("传统程序", "Traditional program", 36, RULE_C, weight="BOLD").next_to(l1, DOWN, buff=0.35)
        t2 = T("机器学习", "Machine learning", 36, DATA_C, weight="BOLD").next_to(l2, DOWN, buff=0.35)
        self.play(FadeIn(t1, shift=UP * 0.15), run_time=0.6)
        self.mid("l19", 0.45)
        self.play(FadeIn(t2, shift=UP * 0.15), Circumscribe(Group(c2, l2, t2), color=DATA_C, buff=0.12), run_time=1.0)
        self.fade_all()
        self.finish()


class S4(Base):
    """③ 实验：1797 张真实手写数字；300 张锁起来当考试；10 / 100 / 1497 个例子 → 37% / 88% / 97%。"""
    SEGMENT = "s4"

    def construct(self) -> None:
        self.at("l20")
        imgs = [EXP["samples"][str(k)][j] for j in range(3) for k in range(10)]
        wall = VGroup(*[tile(im, 0.62) for im in imgs]).arrange_in_grid(rows=3, buff=0.1).move_to(LEFT * 2.6 + UP * 0.6)
        src = fit_w(T(*SRC_DIGITS, 20, MUTED), 12.6).to_edge(DOWN, buff=1.15)
        self.play(LaggedStart(*[FadeIn(t) for t in wall], lag_ratio=0.03), FadeIn(src), run_time=1.4)
        n = T("1797 张", "1,797 images", 52, INK, weight="BOLD").move_to(RIGHT * 4.0 + UP * 1.8)
        self.play(FadeIn(n, shift=UP * 0.15), run_time=0.6)
        self.mid("l20", 0.65)
        big = digit(EXP["threes"][0], 2.4, INK, frame=True).move_to(RIGHT * 4.0 + DOWN * 0.3)
        g = T("8 × 8 个格子", "8 × 8 squares", 30, MUTED).next_to(big, DOWN, buff=0.2)
        self.play(FadeIn(big, scale=0.9), FadeIn(g), run_time=1.0)

        self.at("l21")
        self.play(FadeOut(VGroup(wall, n, big, g)), run_time=0.4)
        bar = VGroup(Rectangle(width=9.0 * 1497 / 1797, height=0.8, stroke_width=0, fill_color=DATA_C, fill_opacity=0.9),
                     Rectangle(width=9.0 * 300 / 1797, height=0.8, stroke_width=0, fill_color=ANS_C, fill_opacity=0.9)
                     ).arrange(RIGHT, buff=0).move_to(UP * 1.4)
        lt = T("练习用的例子 1497", "Practice examples: 1,497", 30, DATA_C).next_to(bar[0], DOWN, buff=0.2)
        self.play(GrowFromEdge(bar[0], LEFT), GrowFromEdge(bar[1], LEFT), run_time=0.9)
        self.play(FadeIn(lt), run_time=0.4)
        self.mid("l21", 0.4)
        lock_box = RoundedRectangle(corner_radius=0.2, width=3.6, height=1.6, stroke_color=ANS_C, stroke_width=3)
        lock_box.move_to(RIGHT * 4.3 + DOWN * 1.0)
        lock_t = VGroup(T("考试题 300", "Exam: 300", 32, ANS_C, weight="BOLD"),
                        T("训练时不许看", "never seen in training", 24, MUTED)).arrange(DOWN, buff=0.12).move_to(lock_box)
        fit_w(lock_t, 3.3)
        self.play(ReplacementTransform(bar[1], lock_box), FadeIn(lock_t), run_time=1.0)
        exam = VGroup(lock_box, lock_t)

        self.at("l22")
        self.play(FadeOut(VGroup(bar[0], lt, src)), exam.animate.scale(0.7).to_corner(UR, buff=0.35), run_time=0.6)
        ax = Axes(x_range=[1, np.log10(1600), 1], y_range=[0, 100, 20], x_length=8.6, y_length=4.4, tips=False,
                  axis_config={"stroke_color": MUTED, "stroke_width": 2, "include_ticks": False}).move_to(LEFT * 1.3 + UP * 0.55)
        X = lambda n_: np.log10(n_)
        yt = VGroup(*[zh(f"{v}%", 22, MUTED).next_to(ax.c2p(1, v), LEFT, buff=0.15) for v in (0, 50, 100)])
        xt = VGroup(*[zh(f"{v:,}", 22, MUTED).next_to(ax.c2p(X(v), 0), DOWN, buff=0.15) for v in (10, 100, 1000)])
        xl = T("看过的例子（张）", "Examples seen", 26, MUTED).next_to(xt, DOWN, buff=0.2)
        yl = T("考试答对", "Exam score", 26, MUTED).next_to(ax.c2p(1, 100), UP, buff=0.2)
        guess = DashedLine(ax.c2p(1, 10), ax.c2p(X(1600), 10), color=BAD, stroke_width=2, dash_length=0.12)
        gl = T("瞎猜 10%", "Guessing 10%", 24, BAD).next_to(guess.get_end(), UP, buff=0.1).shift(LEFT * 0.6)
        how = T("每个点：随机抽 20 次取中位数 · 横轴每格多 10 倍", "Each point: median of 20 random draws · each step = 10× more",
                20, MUTED).next_to(xl, DOWN, buff=0.12)
        self.play(Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(xl), FadeIn(yl), FadeIn(how), run_time=0.9)
        sizes = EXP["sizes"]
        pts = [ax.c2p(X(s), 100 * ACC[s]) for s in sizes]
        dots = VGroup(*[Dot(p, radius=0.09, color=ANS_C) for p in pts])

        def callout(i: int, color: str = ANS_C) -> Text:     # 标在点的外侧，不压曲线：最左点放右下，中间点放左上
            way = DR if i == 0 else UL
            return T(f"{PCT(ACC[sizes[i]])}%", f"{PCT(ACC[sizes[i]])}%", 40, color, weight="BOLD").next_to(dots[i], way, buff=0.12)

        c10 = callout(0)
        self.play(GrowFromCenter(dots[0]), FadeIn(c10, scale=1.3), run_time=0.7)
        self.mid("l22", 0.55)
        self.play(Create(guess), FadeIn(gl), run_time=0.8)

        self.at("l23")
        seg1 = VMobject(stroke_color=ANS_C, stroke_width=5).set_points_as_corners(pts[:3])
        c100 = callout(2)
        self.play(Create(seg1), GrowFromCenter(dots[1]), run_time=0.9)
        self.play(GrowFromCenter(dots[2]), FadeIn(c100, scale=1.3), c10.animate.set_opacity(0.45), run_time=0.7)

        self.at("l24")
        seg2 = VMobject(stroke_color=ANS_C, stroke_width=5).set_points_as_corners(pts[2:])
        call = callout(5).next_to(dots[5], UP, buff=0.2)
        self.play(Create(seg2), *[GrowFromCenter(d) for d in dots[3:]], run_time=1.1)
        self.play(FadeIn(call, scale=1.3), c100.animate.set_opacity(0.45), run_time=0.6)

        self.at("l25")
        chart = VGroup(ax, yt, xt, xl, yl, how, guess, gl, dots, seg1, seg2, c10, c100, call)
        msg = VGroup(T("没人告诉它 3 长什么样", "No one told it what a 3 looks like", 34, MUTED),
                     T("见得越多，认得越准", "The more it sees, the better it gets", 44, HL, weight="BOLD")).arrange(DOWN, buff=0.2)
        self.play(chart.animate.scale(0.7).to_edge(LEFT, buff=0.4).shift(DOWN * 0.3), FadeOut(exam), run_time=0.7)
        msg.next_to(chart, RIGHT, buff=0.5)
        fit_w(msg, config.frame_width / 2 - 0.4 - msg.get_left()[0]).next_to(chart, RIGHT, buff=0.5)
        self.play(FadeIn(msg[0], shift=UP * 0.1), run_time=0.6)
        self.mid("l25", 0.55)
        self.play(FadeIn(msg[1], shift=UP * 0.1), run_time=0.6)

        self.at("l26")
        self.play(FadeOut(VGroup(chart, msg)), run_time=0.5)
        head = T("300 题，错了 10 道", "300 questions, 10 wrong", 44, INK, weight="BOLD").to_edge(UP, buff=0.7)
        ws = VGroup()
        for w in EXP["wrong_examples"]:
            t = tile(w["img"], 1.9)
            lab = VGroup(T(f"真：{w['true']}", f"Truth: {w['true']}", 28, GOOD),
                         T(f"它猜：{w['pred']}", f"Guess: {w['pred']}", 28, BAD)).arrange(DOWN, buff=0.08)
            ws.add(VGroup(t, lab).arrange(DOWN, buff=0.2))
        ws.arrange(RIGHT, buff=0.7).move_to(DOWN * 0.1)
        self.play(FadeIn(head), LaggedStart(*[FadeIn(w, shift=UP * 0.2) for w in ws], lag_ratio=0.2), run_time=1.4)
        self.mid("l26", 0.6)
        hmm = T("有几张，人看了也犹豫", "A few would make a person hesitate too", 30, MUTED).next_to(ws, DOWN, buff=0.45)
        self.play(FadeIn(hmm), run_time=0.6)
        self.fade_all()
        self.finish()


class S5(Base):
    """④ 视角：AI 是一台预测机器（给东西 → 猜答案 + 把握）；AI ⊃ 机器学习 ⊃ 深度学习 ⊃ 大语言模型。"""
    SEGMENT = "s5"

    def machine(self, w: float = 2.8) -> VGroup:
        return box(T("预测机器", "Prediction machine", 30, MODEL_C, weight="BOLD"), MODEL_C, w=w, h=1.3)

    def construct(self) -> None:
        self.at("l27")
        title = T("今天的 AI ≈ 一台预测机器", "Today's AI ≈ a prediction machine", 80, HL, weight="BOLD").move_to(UP * 0.4)
        fit_w(title, 12)
        self.play(FadeIn(title, scale=0.94), run_time=1.0)

        self.at("l28")
        self.play(title.animate.scale(0.45).to_corner(UL, buff=0.35), run_time=0.6)
        m = self.machine().move_to(LEFT * 1.6 + UP * 0.4)
        img = tile(EXP["probe"]["img"], 1.8).next_to(m, LEFT, buff=1.0)
        a1 = arrow(img, m)
        self.play(FadeIn(img, shift=RIGHT * 0.2), GrowArrow(a1), FadeIn(m), run_time=0.9)
        proba = EXP["probe"]["proba"]
        bars = VGroup()
        for k in range(10):
            h = max(0.03, 3.2 * proba[k])
            col = ANS_C if k == 3 else MUTED
            r = Rectangle(width=0.32, height=h, stroke_width=0, fill_color=col, fill_opacity=0.95)
            lab = zh(str(k), 22, col)
            bars.add(VGroup(r, lab))
        for i, b in enumerate(bars):
            b[0].move_to(np.array([i * 0.45, 0, 0]), aligned_edge=DOWN)
            b[1].next_to(b[0], DOWN, buff=0.1).set_y(-0.2)
        bars.move_to(RIGHT * 4.0 + UP * 0.4)
        a2 = Arrow(m.get_right(), bars.get_left() + LEFT * 0.1, buff=0.15, color=MUTED, stroke_width=5,
                   max_tip_length_to_length_ratio=0.25)
        self.mid("l28", 0.35)
        self.play(GrowArrow(a2), LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.05),
                  FadeIn(VGroup(*[b[1] for b in bars])), run_time=1.2)
        conf = T(f"{PCT(proba[3])}% 是 3", f"{PCT(proba[3])}% sure: 3", 40, ANS_C, weight="BOLD")
        conf.next_to(bars, UP, buff=0.3)
        self.play(FadeIn(conf, scale=1.3), run_time=0.6)
        top = VGroup(img, a1, m, a2, bars, conf)

        self.at("l29")
        self.play(top.animate.scale(0.55).to_edge(UP, buff=1.0).shift(LEFT * 1.5), run_time=0.6)
        rows = VGroup()
        for ic, (cn, en) in ((icon_camera(), ("有没有猫？", "Is there a cat?")), (icon_wave(), ("说的是哪几个字？", "Which words were said?"))):
            mm = self.machine(2.4).scale(0.75)
            out = T(cn, en, 30, ANS_C)
            ic.scale(0.8)
            r = VGroup(ic, mm, out).arrange(RIGHT, buff=0.9)
            r.add(arrow(ic, mm), arrow(mm, out))
            rows.add(r)
        rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT).next_to(top, DOWN, buff=0.5).align_to(top, LEFT)
        self.play(FadeIn(rows[0], shift=UP * 0.15), run_time=0.7)
        self.mid("l29", 0.5)
        self.play(FadeIn(rows[1], shift=UP * 0.15), run_time=0.7)

        self.at("l30")
        self.play(FadeOut(VGroup(top, rows)), run_time=0.5)
        half = T("今天天气真……", "The weather today is so…", 52, INK).move_to(LEFT * 3.2 + UP * 0.6)
        mm = self.machine(2.6).next_to(half, RIGHT, buff=0.8)
        cands = VGroup(T("好", "nice", 44, ANS_C, weight="BOLD"), T("热", "hot", 36, MUTED), T("不错", "lovely", 32, MUTED)
                       ).arrange(DOWN, buff=0.25).next_to(mm, RIGHT, buff=0.9)
        VGroup(half, mm, cands).arrange(RIGHT, buff=0.8).move_to(UP * 0.6)
        fit_w(VGroup(half, mm, cands), 12.8)
        a1, a2 = arrow(half, mm), arrow(mm, cands)
        self.play(FadeIn(half), run_time=0.6)
        self.play(GrowArrow(a1), FadeIn(mm), run_time=0.6)
        self.play(GrowArrow(a2), LaggedStart(*[FadeIn(c, shift=LEFT * 0.1) for c in cands], lag_ratio=0.2), run_time=0.9)
        llm = T("大语言模型（LLM）：一个词接一个词地猜", "Large language model (LLM): guess word after word", 36, HL, weight="BOLD")
        fit_w(llm, 12).to_edge(DOWN, buff=1.6)
        self.mid("l30", 0.5)
        self.play(FadeIn(llm, shift=UP * 0.15), run_time=0.7)

        self.at("l31")
        self.play(FadeOut(VGroup(half, mm, cands, a1, a2, llm, title)), run_time=0.5)   # 角标在此淡出：下面的圈图说 AI 也包括规则
        center = DOWN * 0.25 + LEFT * 1.8        # 同心圆（审稿 B2）：每一环等宽，规则标签放进 AI 环带，看得出它属于 AI
        rings = [("AI", "AI", INK, 2.8), ("机器学习", "Machine learning", DATA_C, 2.1),
                 ("深度学习", "Deep learning", MODEL_C, 1.4), ("大语言模型", "LLMs", ANS_C, 0.7)]
        circles = VGroup()
        for i, (cn, en, col, r) in enumerate(rings):
            c = Circle(r, color=col, stroke_width=4, fill_color=col, fill_opacity=0.08).move_to(center)
            lab = T(cn, en, 30 if i < 3 else 24, col, weight="BOLD")
            depth = 0.35            # 标签放在本圈顶与下一圈顶之间的窄带里，宽度不超过该深度处的弦长
            fit_w(lab, 2 * np.sqrt(r ** 2 - (r - depth - lab.height / 2) ** 2) * 0.8 if i < 3 else 2 * r * 0.8)
            lab.move_to(c.get_top() + DOWN * depth if i < 3 else c.get_center())
            if i < 3:       # 标签底衬：圈线从字后面过，不压字
                lab = VGroup(BackgroundRectangle(lab, color=style.BG, fill_opacity=1, buff=0.06), lab)
            circles.add(VGroup(c, lab))
        rule = T("人写规则（传统办法）", "Hand-written rules", 22, RULE_C)
        fit_w(rule, 2 * np.sqrt(2.8 ** 2 - (2.8 - 0.35 - rule.height / 2) ** 2) * 0.8)
        rule = VGroup(BackgroundRectangle(rule, color=style.BG, fill_opacity=1, buff=0.05), rule)
        rule.move_to(center + DOWN * (2.8 - 0.35))
        self.play(FadeIn(circles[0]), run_time=0.7)
        self.play(FadeIn(rule), run_time=0.5)
        self.mid("l31", 0.3)
        self.play(FadeIn(circles[1]), run_time=0.6)
        self.mid("l31", 0.45)
        self.play(FadeIn(circles[2]), run_time=0.6)
        self.mid("l31", 0.6)
        self.play(FadeIn(circles[3]), run_time=0.6)
        self.mid("l31", 0.78)
        today = T("今天说的 AI，大多是这个", "What “AI” usually means today", 30, DATA_C, weight="BOLD")
        fit_w(today, 4.4).next_to(circles[0][0], RIGHT, buff=0.35).shift(DOWN * 0.6)
        link = Line(today.get_left() + LEFT * 0.1, circles[1][0].point_at_angle(-PI / 8), color=DATA_C, stroke_width=2)
        self.play(Circumscribe(circles[1][0], shape=Circle, color=DATA_C, buff=0.05), FadeIn(today), Create(link), run_time=1.0)
        self.fade_all()
        self.finish()


CASES = (   # 现实案例：逐条核对原文（research.md）
    ("alphafold", ("AlphaFold", "AlphaFold"), ("诺贝尔奖官网 2024 · Jumper 等《Nature》2021", "NobelPrize.org 2024 · Jumper et al., Nature 2021")),
    ("chatgpt", ("ChatGPT", "ChatGPT"), ("路透社 2023（UBS 引 Similarweb 估计）", "Reuters 2023 (UBS, citing Similarweb estimates)")),
    ("amazon", ("亚马逊招聘 AI", "Amazon hiring AI"), ("路透社 2018", "Reuters 2018")),
)


class S6(Base):
    """⑤ 现实：三个有出处的案例，一次一张大字卡；顶部三个标签标当前案例。"""
    SEGMENT = "s6"

    def tabs(self) -> VGroup:
        return VGroup(*[T(*name, 28, MUTED) for _, name, _ in CASES]).arrange(RIGHT, buff=1.1).to_edge(UP, buff=0.45)

    def show(self, tabs: VGroup, k: int, *parts: Mobject, y: float = 0.2) -> VGroup:
        src = T(*CASES[k][2], 24, MUTED).to_edge(DOWN, buff=1.25)
        body = VGroup(*parts).arrange(DOWN, buff=0.35).move_to(UP * y)
        fit_w(body, 12.4)
        under = Line(tabs[k].get_corner(DL), tabs[k].get_corner(DR), color=HL, stroke_width=3).shift(DOWN * 0.12)
        self.play(*[t.animate.set_color(INK if i == k else MUTED) for i, t in enumerate(tabs)], Create(under),
                  FadeIn(body, shift=UP * 0.2), FadeIn(src), run_time=0.9)
        return VGroup(body, src, under)

    def construct(self) -> None:
        tabs = self.tabs()
        self.at("l32")
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.15) for t in tabs], lag_ratio=0.25), run_time=1.2)

        self.at("l33")
        a = T("实验测结构：常要好几年 → 直接预测", "By experiment: often years → predicted directly", 40, INK)
        b = T("分享 2024 诺贝尔化学奖的一半", "Shared half the 2024 Nobel Prize in Chemistry", 64, HL, weight="BOLD")
        cur = self.show(tabs, 0, a, y=1.0)
        self.mid("l33", 0.62)
        b.next_to(cur[0], DOWN, buff=0.4)
        fit_w(b, 12)
        self.play(FadeIn(b, shift=UP * 0.2), run_time=0.8)
        cur.add(b)

        self.at("l34")
        self.play(FadeOut(cur), run_time=0.4)
        big = T("≈ 1 亿", "≈ 100 million", 120, HL, weight="BOLD")
        sub = T("月活跃用户 · 上线约两个月（估计）", "monthly active users · ~2 months after launch (estimate)", 34, INK)
        cur = self.show(tabs, 1, big, sub)

        self.at("l35")
        self.play(FadeOut(cur), run_time=0.4)
        a = T("学的是 10 年的简历，大多来自男性", "Learned from 10 years of résumés, mostly men's", 36, INK)
        b = T("“women's”（女子的）→ 扣分", "“women's” → marked down", 72, BAD, weight="BOLD")
        cur = self.show(tabs, 2, a, y=1.5)
        self.mid("l35", 0.5)
        fit_w(b, 12.4).next_to(cur[0], DOWN, buff=0.45)
        self.play(FadeIn(b, shift=UP * 0.2), run_time=0.8)
        self.mid("l35", 0.85)
        sc = T("工具后来被放弃", "The tool was scrapped", 32, MUTED).next_to(b, DOWN, buff=0.35)
        self.play(FadeIn(sc), run_time=0.5)
        cur.add(b, sc)

        self.at("l36")
        self.play(FadeOut(cur), FadeOut(tabs), run_time=0.5)
        st = statement(T("数据里有什么，它就学什么", "Whatever is in the data, it learns", 56, INK, weight="BOLD"),
                       T("包括偏见", "Bias included", 56, BAD, weight="BOLD"))
        self.play(FadeIn(st[0], shift=UP * 0.2), run_time=0.8)
        self.mid("l36", 0.55)
        self.play(FadeIn(st[1], shift=UP * 0.2), run_time=0.6)
        self.fade_all()
        self.finish()


class S7(Base):
    """⑥ 用好它的三个提醒：只会学过的（字母 A → 4，92%）；是预测不是真理（这张 2 → 1，81%）；本事和毛病都来自数据。"""
    SEGMENT = "s7"

    def card(self, title: Text, body: Mobject) -> VGroup:
        frame = RoundedRectangle(corner_radius=0.2, width=4.2, height=4.9, stroke_color=style.PANEL_EDGE, stroke_width=2,
                                 fill_color=style.BG, fill_opacity=1)
        fit_w(title, 3.8)
        content = VGroup(title, body).arrange(DOWN, buff=0.4)
        return VGroup(frame, content.move_to(frame))

    def guess(self, img, pred: int, conf: float, note: Text) -> VGroup:
        t = tile(img, 1.6)
        say = T(f"“{PCT(conf)}% 是 {pred}”", f"“{PCT(conf)}% sure: {pred}”", 32, BAD, weight="BOLD")
        return VGroup(t, say, fit_w(note, 3.7)).arrange(DOWN, buff=0.25)

    def construct(self) -> None:
        self.at("l37")
        title = T("用好 AI 的三个提醒", "Three things to keep in mind", 44, INK).to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1)
        xs = [-4.55, 0, 4.55]

        self.at("l38")
        c1 = self.card(T("① 只会它学过的", "① Only knows what it learned", 30, HL),
                       self.guess(OOD_A["img"], OOD_A["pred"], OOD_A["conf"],
                                  VGroup(T("没见过字母，", "Never seen a letter,", 22, MUTED),
                                         T("也没有「不认识」这个选项", "and “none of these” isn't an option", 22, MUTED)
                                         ).arrange(DOWN, buff=0.06))).move_to(RIGHT * xs[0] + DOWN * 0.3)
        self.play(FadeIn(c1, shift=UP * 0.3), run_time=1)

        self.at("l39")
        c2 = self.card(T("② 是预测，不是真理", "② Predictions, not truth", 30, HL),
                       self.guess(WRONG_2["img"], WRONG_2["pred"], WRONG_2["conf"],
                                  T("其实是 2（写得很潦草）", "Actually a scrawled 2", 24, GOOD))).move_to(RIGHT * xs[1] + DOWN * 0.3)
        self.play(FadeIn(c2, shift=UP * 0.3), run_time=1)

        self.at("l40")
        d = box(T("数据", "Data", 28, DATA_C), DATA_C, w=1.4, h=0.9)
        mm = box(T("模型", "Model", 28, MODEL_C), MODEL_C, w=1.4, h=0.9)
        pair = VGroup(d, mm).arrange(RIGHT, buff=0.6)
        pair.add(arrow(d, mm))
        gb = VGroup(T("本事", "Strengths", 26, GOOD), T("毛病", "Flaws", 26, BAD)).arrange(RIGHT, buff=0.8)
        ask = T("先问：从什么数据学的？", "Ask first: what data?", 26, HL)
        body = VGroup(pair, gb, fit_w(ask, 3.7)).arrange(DOWN, buff=0.4)
        c3 = self.card(T("③ 本事和毛病都来自数据", "③ Data shapes it all", 30, HL), body
                       ).move_to(RIGHT * xs[2] + DOWN * 0.3)
        self.play(FadeIn(c3, shift=UP * 0.3), run_time=1)
        self.mid("l40", 0.6)
        self.play(Indicate(ask, color=HL), run_time=0.8)
        self.fade_all()
        self.finish()
