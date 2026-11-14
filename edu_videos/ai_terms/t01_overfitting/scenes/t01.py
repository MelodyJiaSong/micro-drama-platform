# -*- coding: utf-8 -*-
"""t01 过拟合（v2，节目模板 v2）：s1–s8 八段画面，按时间轴的句子触发；s0 本期内容、s9 片尾与章节转场是统一包装卡
（tools/edu_package.py）。所有数据与误差由下方 numpy 实验算出，不手写。中英两版共用本文件，画面文字用 T(中文, English)。

    python tools/edu_video.py render edu_videos/ai_terms/t01_overfitting [--lang en] [S1 ...]
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from manim import *

HERE = Path(__file__).resolve()
sys.path[:0] = [str(HERE.parents[4] / "tools"), str(HERE.parents[3] / "_shared")]
from edu_manim import TOP, CuedScene, tr  # noqa: E402
import style  # noqa: E402
from style import BAD, GOOD, HL, INK, J_COLOR, MUTED, V_COLOR, backed, panel, zh  # noqa: E402

style.set_stage("#000000")          # AI 高频词：纯黑舞台，与片头 / 转场 / 片尾一致
ASSETS = HERE.parents[1] / "assets"
TRAIN_C, TEST_C, VALID_C = J_COLOR, HL, V_COLOR
LINE_C, MID_C, WIGGLE_C = MUTED, GOOD, BAD


def T(cn: str, en: str, size: float = 36, color: str = INK, weight: str = "NORMAL") -> Text:
    """按当前语言（EDU_LANG）出字。英文字号略小一档，行宽与中文接近。"""
    return zh(tr(cn, en), size if tr("zh", "en") == "zh" else size * 0.92, color, weight)


# ---------- 实验（讲稿 script.md 头部写明同样的设定） ----------
def truth(x: np.ndarray | float) -> np.ndarray | float:
    return 1.2 * np.sin(1.3 * x) + 0.25 * x


def make_data(seed: int = 99) -> tuple[np.ndarray, ...]:
    rng = np.random.default_rng(seed)
    xtr = np.linspace(-2.8, 2.8, 10) + rng.uniform(-0.12, 0.12, 10)
    ytr = truth(xtr) + rng.normal(0, 0.35, 10)
    xte = np.linspace(-2.5, 2.5, 6) + rng.uniform(-0.1, 0.1, 6)
    yte = truth(xte) + rng.normal(0, 0.3, 6)
    return xtr, ytr, xte, yte


XTR, YTR, XTE, YTE = make_data()
DEGREES = (1, 3, 9)
FITS = {d: np.polyfit(XTR, YTR, d) for d in DEGREES}
MSE = {d: (float(np.mean((np.polyval(FITS[d], XTR) - YTR) ** 2)), float(np.mean((np.polyval(FITS[d], XTE) - YTE) ** 2)))
       for d in DEGREES}
RATIO = MSE[9][1] / MSE[3][1]
assert MSE[9][0] < 1e-6 and 20 <= RATIO < 30, "讲稿说「训练误差为零」「二十多倍」，数据变了要同步改讲稿"
assert len(FITS[3]) == 4 and len(FITS[9]) == len(XTR) == 10, "讲稿 s6 说「四个数字」「十个数字、十个点」"


def error_curves(runs: int = 300) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(0)
    tr_, te = np.zeros((runs, 9)), np.zeros((runs, 9))
    for k in range(runs):
        xtr = np.linspace(-2.8, 2.8, 10) + rng.uniform(-0.12, 0.12, 10)
        ytr = truth(xtr) + rng.normal(0, 0.35, 10)
        xte = rng.uniform(-2.6, 2.6, 50)
        yte = truth(xte) + rng.normal(0, 0.35, 50)
        for d in range(1, 10):
            c = np.polyfit(xtr, ytr, d)
            tr_[k, d - 1] = np.mean((np.polyval(c, xtr) - ytr) ** 2)
            te[k, d - 1] = np.mean((np.polyval(c, xte) - yte) ** 2)
    return np.median(tr_, axis=0), np.median(te, axis=0)


def more_data_fit() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(3)
    x = np.sort(rng.uniform(-2.8, 2.8, 40))
    y = truth(x) + rng.normal(0, 0.35, 40)
    return x, y, np.polyfit(x, y, 9)


RIDGE_LAMBDA = 0.01


def ridge_fit() -> np.ndarray:
    v = np.vander(XTR / 3, 10, increasing=True)
    return np.linalg.solve(v.T @ v + RIDGE_LAMBDA * np.eye(10), v.T @ YTR)


def ridge_eval(w: np.ndarray, x: float) -> float:
    return float((np.vander(np.array([x]) / 3, 10, increasing=True) @ w)[0])


# ---------- 画面构件 ----------
AX_POS = LEFT * 2.6 + UP * 0.35


def data_axes() -> Axes:
    ax = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=8.0, y_length=5.6, tips=False,
              axis_config={"stroke_color": MUTED, "stroke_width": 2, "include_ticks": False})
    return ax.move_to(AX_POS)


def train_dots(ax: Axes) -> VGroup:
    return VGroup(*[Dot(ax.c2p(x, y), radius=0.1, color=TRAIN_C) for x, y in zip(XTR, YTR)])


def test_marks(ax: Axes) -> VGroup:
    return VGroup(*[Square(0.2, color=TEST_C, fill_color=TEST_C, fill_opacity=1, stroke_width=0).rotate(PI / 4)
                    .move_to(ax.c2p(x, y)) for x, y in zip(XTE, YTE)])


def fit_curve(ax: Axes, d: int, color: str) -> VMobject:
    return ax.plot(lambda x: float(np.clip(np.polyval(FITS[d], x), -3, 3)), x_range=[-2.95, 2.95, 0.01], color=color,
                   stroke_width=6)


def truth_curve(ax: Axes) -> VMobject:
    return DashedVMobject(ax.plot(truth, x_range=[-2.95, 2.95, 0.01], color=INK, stroke_width=3), num_dashes=60
                          ).set_opacity(0.6)


def legend(color: str, text: Text, square: bool = False) -> VGroup:
    mark = (Square(0.2, color=color, fill_color=color, fill_opacity=1, stroke_width=0).rotate(PI / 4) if square
            else Dot(radius=0.1, color=color))
    return backed(VGroup(mark, text).arrange(RIGHT, buff=0.15)).set_z_index(TOP)


def gaps(ax: Axes, xs: np.ndarray, ys: np.ndarray, f, color: str) -> VGroup:
    return VGroup(*[Line(ax.c2p(x, y), ax.c2p(x, f(x)), color=color, stroke_width=4) for x, y in zip(xs, ys)])


def model_row(no: str, name: Text, color: str, train: float, test: float) -> VGroup:
    head = VGroup(zh(no, 30, color), name).arrange(RIGHT, buff=0.15)
    tr_ = T(f"训练误差 {train:.2f}", f"Training error {train:.2f}", 26, INK)
    te = T(f"测试误差 {test:.2f}", f"Test error {test:.2f}", 26, color).set_opacity(0)
    return VGroup(head, tr_, te).arrange(DOWN, aligned_edge=LEFT, buff=0.1)


ROWS = (("①", ("直线", "Line"), LINE_C, 1), ("②", ("平缓曲线", "Gentle"), MID_C, 3),
        ("③", ("弯曲线", "Wiggly"), WIGGLE_C, 9))
VERDICT = {1: ("欠拟合", "Underfit"), 3: ("刚刚好", "Just right"), 9: ("过拟合", "Overfit")}


def verdict(row: VGroup, d: int, color: str) -> Text:
    """结论标签贴在该行标题右侧：① 欠拟合（l11）、② 刚刚好（l16）、③ 过拟合（l18）。"""
    return T(*VERDICT[d], 28, color, weight="BOLD").next_to(row[0], RIGHT, buff=0.35).set_z_index(TOP + 1)


def statement(*lines: Text, buff: float = 0.3) -> VGroup:
    """居中大字（发布会式）：一到两行，留白。"""
    return VGroup(*lines).arrange(DOWN, buff=buff).move_to(UP * 0.4)


def image(name: str, height: float) -> ImageMobject:
    return ImageMobject(str(ASSETS / name)).set_height(height)


class Base(CuedScene):
    TIMELINE = HERE.parents[1] / "timeline.json"

    def chart(self) -> tuple[Axes, VGroup, VGroup]:
        ax = data_axes()
        dots = train_dots(ax)
        lg = legend(TRAIN_C, T("训练数据（练习题）", "Training data (practice)", 28)).next_to(ax.c2p(-3, 3), DR, buff=0.1)
        return ax, dots, lg

    def rows(self) -> list[VGroup]:
        self.box = panel(width=5.2, height=6.3)
        return [self.stack(model_row(no, T(*name, 30, c), c, *MSE[d]), gap=0.35) for no, name, c, d in ROWS]


class S1(Base):
    """① 问题：开场一问 + 模型在学什么。"""
    SEGMENT = "s1"

    def construct(self) -> None:
        self.at("l07")
        good = T("手里的数据：几乎满分", "On your data: nearly perfect", 54, GOOD, weight="BOLD")
        bad = T("新数据：一塌糊涂", "On new data: a mess", 54, BAD, weight="BOLD")
        why = T("为什么？", "Why?", 40, MUTED)
        block = statement(good, bad, why, buff=0.45)
        self.play(FadeIn(good, shift=UP * 0.2), run_time=0.8)
        self.mid("l07", 0.4)
        self.play(FadeIn(bad, shift=UP * 0.2), run_time=0.8)
        self.mid("l07", 0.85)
        self.play(FadeIn(why), run_time=0.5)

        ax, dots, lg = self.chart()
        self.at("l08")
        self.play(FadeOut(block), run_time=0.4)
        self.play(Create(ax), run_time=0.5)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.12), FadeIn(lg), run_time=1.6)

        self.at("l09")
        tc = truth_curve(ax)
        tl = backed(T("背后的规律", "The hidden pattern", 26)).next_to(ax.c2p(-1.4, truth(-1.4)), DOWN, buff=0.35).set_z_index(TOP)
        self.play(Create(tc), FadeIn(tl), run_time=self.fit("l09", 0.4, 1.2, 2))
        self.mid("l09", 0.6)
        noise = gaps(ax, XTR, YTR, truth, BAD)
        nl = backed(T("噪声", "Noise", 28, BAD)).next_to(noise[1], LEFT, buff=0.12).set_z_index(TOP)
        self.play(Create(noise), FadeIn(nl), run_time=1)

        self.at("l10")
        task = backed(VGroup(T("任务：", "The job:", 32, HL), T("从这些点找出规律，预测新数据", "find the pattern, predict new data", 32))
                      .arrange(RIGHT, buff=0.15)).to_edge(UP, buff=0.3).shift(RIGHT * 2.2).set_z_index(TOP)
        self.play(FadeOut(tc), FadeOut(tl), FadeOut(noise), FadeOut(nl), FadeIn(task), run_time=1)
        self.until(self.seg_duration - 0.7)
        self.play(FadeOut(task), run_time=0.5)
        self.finish()


class S2(Base):
    """三种学法。"""
    SEGMENT = "s2"

    def construct(self) -> None:
        ax, dots, lg = self.chart()
        self.add(ax, dots, lg)
        rows = self.rows()
        self.play(FadeIn(self.box), run_time=0.5)
        line, mid, wig = fit_curve(ax, 1, LINE_C), fit_curve(ax, 3, MID_C), fit_curve(ax, 9, WIGGLE_C)

        self.at("l11")
        miss = gaps(ax, XTR, YTR, lambda x: np.polyval(FITS[1], x), LINE_C).set_opacity(0.8)
        self.play(Create(line), FadeIn(rows[0]), run_time=1.2)
        self.mid("l11", 0.55)
        self.play(Create(miss), FadeIn(verdict(rows[0], 1, LINE_C)), run_time=1)

        self.at("l12")
        self.play(FadeOut(miss), line.animate.set_stroke(opacity=0.25), run_time=0.5)
        self.play(Create(mid), FadeIn(rows[1]), run_time=self.fit("l12", 0.6, 1.2, 2.2))

        self.at("l13")
        self.play(mid.animate.set_stroke(opacity=0.35), run_time=0.4)
        self.play(Create(wig), run_time=self.fit("l13", 0.5, 1.5, 2.5))
        self.play(FadeIn(rows[2]), run_time=0.6)
        self.mid("l13", 0.8)
        self.play(Indicate(rows[2][1], color=HL), Flash(dots[4].get_center(), color=WIGGLE_C), run_time=1)

        self.at("l14")
        q = T("练习题满分，最好？", "Perfect score. Best?", 30, HL).next_to(rows[2][1], DOWN, aligned_edge=LEFT, buff=0.25)
        q.set_z_index(TOP + 1)
        self.play(FadeIn(q, scale=1.3), Circumscribe(rows[2], color=HL, buff=0.1), run_time=1)
        self.until(self.seg_duration - 0.7)
        self.play(FadeOut(q), run_time=0.5)
        self.finish()


class S3(Base):
    """考试 + 代价：过拟合比欠拟合更危险。"""
    SEGMENT = "s3"

    def construct(self) -> None:
        ax, dots, lg = self.chart()
        rows = self.rows()
        line, mid, wig = fit_curve(ax, 1, LINE_C), fit_curve(ax, 3, MID_C), fit_curve(ax, 9, WIGGLE_C)
        line.set_stroke(opacity=0.25)
        mid.set_stroke(opacity=0.35)
        self.add(ax, dots, lg, self.box, *rows, verdict(rows[0], 1, LINE_C), line, mid, wig)

        self.at("l15")
        marks = test_marks(ax)
        lg2 = legend(TEST_C, T("测试数据（考试）", "Test data (the exam)", 28), square=True).next_to(lg, DOWN, aligned_edge=LEFT, buff=0.1)
        self.play(LaggedStart(*[GrowFromCenter(m) for m in marks], lag_ratio=0.15), FadeIn(lg2), run_time=1.6)

        self.at("l16")
        g_mid = gaps(ax, XTE, YTE, lambda x: np.polyval(FITS[3], x), MID_C)
        self.play(mid.animate.set_stroke(opacity=1), wig.animate.set_stroke(opacity=0.2), run_time=0.6)
        self.play(Create(g_mid), run_time=0.8)
        self.play(rows[1][2].animate.set_opacity(1), FadeIn(verdict(rows[1], 3, MID_C)), run_time=0.6)

        self.at("l17")
        g_wig = gaps(ax, XTE, YTE, lambda x: np.polyval(FITS[9], x), WIGGLE_C)
        self.play(FadeOut(g_mid), mid.animate.set_stroke(opacity=0.35), wig.animate.set_stroke(opacity=1), run_time=0.6)
        self.play(Create(g_wig), run_time=1)
        self.play(rows[2][2].animate.set_opacity(1), run_time=0.6)
        self.mid("l17", 0.7)
        times = T(f"是 ② 的 {RATIO:.0f} 倍", f"{RATIO:.0f}× model ②", 30, WIGGLE_C, weight="BOLD")
        times.next_to(rows[2][2], DOWN, aligned_edge=LEFT, buff=0.2).set_z_index(TOP + 2)
        self.play(FadeIn(times, scale=1.4), run_time=0.6)

        self.at("l18")
        tc = truth_curve(ax)
        msg = backed(VGroup(T("把噪声也背下来了", "It memorized the noise", 34), T("= 过拟合", "= overfitting", 34, HL))
                     .arrange(RIGHT, buff=0.15))
        msg.to_edge(UP, buff=0.25).shift(LEFT * 2.3).set_z_index(TOP + 2)
        tl = backed(T("背后的规律", "The hidden pattern", 26)).next_to(ax.c2p(-1.4, truth(-1.4)), DOWN, buff=0.35).set_z_index(TOP)
        noise = gaps(ax, XTR, YTR, truth, BAD)
        self.play(FadeOut(g_wig), Create(tc), FadeIn(tl), run_time=1.2)
        self.play(FadeIn(msg, shift=DOWN * 0.2), Create(noise), Indicate(wig, color=WIGGLE_C), FadeOut(times),
                  FadeIn(verdict(rows[2], 9, WIGGLE_C)), run_time=1.2)

        self.at("l19")
        self.play(FadeOut(msg), FadeOut(tc), FadeOut(tl), FadeOut(noise), FadeOut(marks), FadeOut(lg2), FadeOut(lg),
                  line.animate.set_stroke(opacity=1), run_time=0.5)
        u = backed(T("欠拟合：一眼就能看出不行", "Underfit: obviously bad", 32, MUTED)).set_z_index(TOP + 2)
        o = backed(T("过拟合：看起来好极了", "Overfit: looks great", 32, BAD, weight="BOLD")).set_z_index(TOP + 2)
        VGroup(u, o).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.35)
        self.play(FadeIn(u, shift=DOWN * 0.15), Indicate(rows[0][1], color=MUTED), run_time=0.9)
        self.mid("l19", 0.45)
        self.play(FadeIn(o, shift=DOWN * 0.15), Circumscribe(rows[2][1], color=BAD, buff=0.08), run_time=1.1)
        self.fade_all()
        self.finish()


class S4(Base):
    """② 类比：背答案的学生；只在沙发上见过猫的小朋友。"""
    SEGMENT = "s4"

    def card(self, head: Text, body: Text) -> VGroup:
        return backed(VGroup(head, body).arrange(DOWN, buff=0.15))

    def construct(self) -> None:
        stu, exam = image("student_v2.png", 5.4), image("exam_v2.png", 5.4)
        stu.to_edge(LEFT, buff=0.3).shift(UP * 0.4)
        exam.move_to(stu)
        self.at("l20")
        self.play(FadeIn(stu, shift=UP * 0.2), run_time=1)
        self.mid("l20", 0.55)
        c1 = self.card(T("练习册", "Workbook", 34), T("100 分", "100%", 54, GOOD, weight="BOLD")).move_to(RIGHT * 4.4 + UP * 1.4)
        self.play(FadeIn(c1, shift=LEFT * 0.3), run_time=0.8)

        self.at("l21")
        c2 = self.card(T("考试", "Exam", 34), T("换个样子就不会", "Lost on new questions", 40, BAD)).move_to(RIGHT * 4.4 + DOWN * 0.9)
        self.play(FadeOut(stu), FadeIn(exam), FadeIn(c2, shift=LEFT * 0.3), run_time=1)

        self.at("l22")
        self.play(FadeOut(exam), FadeOut(c1), FadeOut(c2), run_time=0.5)
        cats = image("cats_sofa_v1.png", 5.2).move_to(UP * 0.5)
        cap = T("训练照片：猫，全在沙发上", "Training photos: every cat is on a sofa", 30, MUTED).next_to(cats, DOWN, buff=0.15)
        self.play(FadeIn(cats, scale=0.96), FadeIn(cap), run_time=1)

        self.at("l23")
        rule = T("学到的规则：沙发 = 猫", "Rule learned: sofa = cat", 40, HL, weight="BOLD").to_edge(UP, buff=0.35)
        self.play(FadeOut(cap), cats.animate.set_height(2.4).move_to(LEFT * 4.6 + DOWN * 0.2), FadeIn(rule), run_time=1)
        dog = image("dog_sofa_v1.png", 2.4).move_to(DOWN * 0.2)
        grass = image("cat_grass_v1.png", 2.4).move_to(RIGHT * 4.6 + DOWN * 0.2)
        say1 = T("“是猫！”", "“Cat!”", 36, BAD, weight="BOLD").next_to(dog, DOWN, buff=0.2)
        say2 = T("“不是猫。”", "“Not a cat.”", 36, BAD, weight="BOLD").next_to(grass, DOWN, buff=0.2)
        self.mid("l23", 0.3)
        self.play(FadeIn(dog, shift=UP * 0.2), FadeIn(say1), run_time=0.9)
        self.mid("l23", 0.72)
        self.play(FadeIn(grass, shift=UP * 0.2), FadeIn(say2), run_time=0.9)

        self.at("l24")
        self.play(*[FadeOut(m) for m in (cats, dog, grass, say1, say2, rule)], run_time=0.6)
        a = T("背下来的答案 · 记住的巧合", "Memorized answers · memorized coincidences", 44)
        b = T("场景一换，全失灵", "Change the setting, and they fail", 56, BAD, weight="BOLD")
        st = statement(a, b, buff=0.5)
        self.play(FadeIn(a, shift=UP * 0.2), run_time=0.8)
        self.mid("l24", 0.6)
        self.play(FadeIn(b, shift=UP * 0.2), run_time=0.8)
        self.fade_all()
        self.finish()


class S5(Base):
    """③ 实验：300 次重复，两条误差曲线。"""
    SEGMENT = "s5"

    def construct(self) -> None:
        tr_, te = error_curves()
        ax = Axes(x_range=[1, 9, 1], y_range=[0, 0.7, 0.1], x_length=8.4, y_length=4.6, tips=False,
                  axis_config={"stroke_color": MUTED, "stroke_width": 2},
                  ).shift(UP * 1.0 + LEFT * 1.4)
        nums = VGroup(*[zh(str(d), 26, MUTED).next_to(ax.c2p(d, 0), DOWN, buff=0.18) for d in range(1, 10)])
        xl = T("模型复杂度（多项式次数）", "Model complexity (polynomial degree)", 28, MUTED).next_to(nums, DOWN, buff=0.3)
        yl = T("误差", "Error", 28, MUTED).next_to(ax.c2p(1, 0.7), LEFT, buff=0.25)
        note = T("300 次实验的中位数", "Median of 300 runs", 26, MUTED).next_to(xl, RIGHT, buff=0.8)
        degrees = list(range(1, 10))

        self.at("l25")
        self.play(Create(ax), FadeIn(nums), FadeIn(xl), FadeIn(yl), FadeIn(note), run_time=1.2)

        self.at("l26")
        g_tr = ax.plot_line_graph(degrees, tr_, line_color=TRAIN_C, stroke_width=6,
                                  vertex_dot_radius=0.08, vertex_dot_style={"color": TRAIN_C})
        l_tr = T("训练误差", "Training error", 30, TRAIN_C).next_to(ax.c2p(9, tr_[-1]), RIGHT, buff=0.25)
        self.play(Create(g_tr), run_time=self.fit("l26", 0.7, 1.5, 3))
        self.play(FadeIn(l_tr), run_time=0.5)

        self.at("l27")
        g_te = ax.plot_line_graph(degrees, te, line_color=TEST_C, stroke_width=6,
                                  vertex_dot_radius=0.08, vertex_dot_style={"color": TEST_C})
        l_te = T("测试误差", "Test error", 30, TEST_C).next_to(ax.c2p(9, te[-1]), UR, buff=0.15)
        self.play(Create(g_te), run_time=self.fit("l27", 0.45, 1.5, 3))
        self.play(FadeIn(l_te), run_time=0.4)
        under = [d for d in degrees if tr_[d - 1] > 0.3]
        best = int(np.argmin(te)) + 1
        over = [d for d in degrees if d > best and te[d - 1] > 1.5 * te.min()]
        zones = VGroup()
        for ds, color, d in ((under, MUTED, 1), ([d for d in degrees if d not in under + over], GOOD, 3), (over, BAD, 9)):
            left, right = ax.c2p(min(ds) - 0.45, 0), ax.c2p(max(ds) + 0.45, 0.7)
            rect = Rectangle(width=right[0] - left[0], height=right[1] - left[1], stroke_width=0, fill_color=color,
                             fill_opacity=0.12).move_to((left + right) / 2)
            edge, way = (rect.get_bottom(), UP) if d == 1 else (rect.get_top(), DOWN)
            zones.add(VGroup(rect, T(*VERDICT[d], 28, color).next_to(edge, way, buff=0.12)))
        zones.set_z_index(-1)
        self.mid("l27", 0.55)
        self.play(LaggedStart(*[FadeIn(z) for z in zones], lag_ratio=0.3), run_time=1.5)

        self.at("l28")
        top, bot = ax.c2p(9, te[-1]), ax.c2p(9, tr_[-1])
        brace = BraceBetweenPoints(bot, top, direction=RIGHT, color=HL)
        bl = VGroup(T("训练低、测试高", "Big gap:", 28, HL),
                    T("过拟合的信号", "overfitting sign", 28, HL)).arrange(DOWN, buff=0.08)
        bl = backed(bl).next_to(brace, RIGHT, buff=0.15).set_z_index(TOP)
        self.play(GrowFromCenter(brace), FadeIn(bl), run_time=1)
        self.fade_all()
        self.finish()


def num_grid(values: np.ndarray, color: str, cols: int = 5, size: float = 24) -> VGroup:
    fmt = lambda v: f"{v:+.2f}" if abs(v) >= 0.005 else f"{v:+.3f}"      # 很小的系数不显示成 +0.00
    cells = VGroup(*[zh(fmt(v), size, color) for v in values])
    return cells.arrange_in_grid(cols=cols, buff=(0.28, 0.14))


class S6(Base):
    """④ 视角：学习就是压缩。10 个高度 → 4 个数字（② 三次多项式）vs 10 个数字（③ 九次，没有压缩）。"""
    SEGMENT = "s6"

    def block(self, head: Text, body: Mobject) -> VGroup:
        return VGroup(head, body).arrange(DOWN, buff=0.18)

    def construct(self) -> None:
        self.at("l29")
        title = T("学习 = 压缩", "Learning = compression", 96, HL, weight="BOLD").move_to(UP * 0.4)
        if title.width > 11.5:
            title.scale_to_fit_width(11.5)
        self.play(FadeIn(title, scale=0.94), run_time=1.0)

        ax, dots, lg = self.chart()
        self.at("l30")
        self.play(title.animate.scale(0.42).to_corner(UL, buff=0.3), run_time=0.7)
        self.play(Create(ax), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.08), run_time=1.2)
        self.box = panel(width=5.2, height=6.3)
        self.play(FadeIn(self.box), run_time=0.4)
        b1 = self.stack(self.block(T("原样记住：10 个数字", "Store exactly: 10 numbers", 28, TRAIN_C),
                                   num_grid(YTR, TRAIN_C)))
        hs = VGroup(*[DashedLine(ax.c2p(x, 0), ax.c2p(x, y), color=TRAIN_C, stroke_width=2) for x, y in zip(XTR, YTR)])
        self.play(Create(hs), FadeIn(b1), run_time=1.2)

        self.at("l31")
        mid = fit_curve(ax, 3, MID_C)
        b2 = self.stack(self.block(T("② 平缓曲线：4 个数字", "② Gentle curve: 4 numbers", 28, MID_C),
                                   num_grid(FITS[3], MID_C, cols=4)))
        self.play(FadeOut(hs), Create(mid), FadeIn(b2), run_time=1.4)
        self.mid("l31", 0.6)
        marks = test_marks(ax)
        ok = gaps(ax, XTE, YTE, lambda x: np.polyval(FITS[3], x), MID_C)
        self.play(LaggedStart(*[GrowFromCenter(m) for m in marks], lag_ratio=0.1), Create(ok), run_time=1.2)

        self.at("l32")
        wig = fit_curve(ax, 9, WIGGLE_C)
        b3 = self.stack(self.block(T("③ 弯曲线：10 个数字", "③ Wiggly curve: 10 numbers", 28, WIGGLE_C),
                                   num_grid(FITS[9], WIGGLE_C)))
        self.play(FadeOut(ok), FadeOut(marks), mid.animate.set_stroke(opacity=0.3), Create(wig), FadeIn(b3), run_time=1.4)
        self.mid("l32", 0.45)
        nz = T("10 → 10：没有压缩", "10 → 10: no compression", 30, BAD, weight="BOLD")
        nz.next_to(self.box, DOWN, buff=0.12).set_z_index(TOP + 1)
        self.play(Circumscribe(b3[1], color=BAD, buff=0.08), Circumscribe(b1[1], color=BAD, buff=0.08), FadeIn(nz), run_time=1.2)

        self.at("l33")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        line = T("用更少的东西，解释更多的事", "Explain more with less", 64, HL, weight="BOLD").move_to(UP * 0.4)
        self.play(FadeIn(line, scale=0.94), run_time=1.0)
        self.fade_all()
        self.finish()


CASES = (   # 现实案例：逐条核对原文（research.md）
    ("flu", ("Google 流感趋势", "Google Flu Trends"), ("Lazer 等 ·《Science》· 2014", "Lazer et al. · Science · 2014")),
    ("xray", ("胸片肺炎模型", "Pneumonia X-ray model"), ("Zech 等 ·《PLOS Medicine》· 2018", "Zech et al. · PLOS Medicine · 2018")),
    ("skin", ("黑色素瘤识别", "Melanoma detector"), ("Winkler 等 ·《JAMA Dermatology》· 2019", "Winkler et al. · JAMA Dermatology · 2019")),
)


class S7(Base):
    """⑤ 现实：三个有出处的案例，一次一张大字卡；顶部三个标签标当前案例。"""
    SEGMENT = "s7"

    def tabs(self) -> VGroup:
        return VGroup(*[T(*name, 28, MUTED) for _, name, _ in CASES]).arrange(RIGHT, buff=1.1).to_edge(UP, buff=0.45)

    def show(self, tabs: VGroup, k: int, *parts: Mobject) -> VGroup:
        src = T(*CASES[k][2], 24, MUTED).to_edge(DOWN, buff=1.25)
        body = VGroup(*parts).arrange(DOWN, buff=0.35).move_to(UP * 0.2)
        under = Line(tabs[k].get_corner(DL), tabs[k].get_corner(DR), color=HL, stroke_width=3).shift(DOWN * 0.12)
        self.play(*[t.animate.set_color(INK if i == k else MUTED) for i, t in enumerate(tabs)], Create(under),
                  FadeIn(body, shift=UP * 0.2), FadeIn(src), run_time=0.9)
        return VGroup(body, src, under)

    def construct(self) -> None:
        tabs = self.tabs()
        self.at("l34")
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.15) for t in tabs], lag_ratio=0.25), run_time=1.2)

        self.at("l35")
        q = T("“一部分在测流感，一部分在测冬天”", "“Part flu detector, part winter detector”", 52, INK, weight="BOLD")
        why = T("5000 万个搜索词 · 贴合 1152 个数据点 = 过拟合", "50 million search terms fit to 1,152 data points = overfitting", 32, HL)
        cur = self.show(tabs, 0, q, why)

        self.at("l36")
        big = T("100 / 108 周", "100 / 108 weeks", 120, BAD, weight="BOLD")
        sub = T("流感估高（2011–2013）", "flu overestimated (2011–2013)", 34, MUTED)
        new = VGroup(big, sub).arrange(DOWN, buff=0.3).move_to(cur[0])
        self.play(FadeOut(cur[0], shift=UP * 0.2), FadeIn(new, shift=UP * 0.2), run_time=0.8)
        cur = VGroup(new, cur[1], cur[2])

        self.at("l37")
        self.play(FadeOut(cur), run_time=0.4)
        big = T("99.9%", "99.9%", 120, HL, weight="BOLD")
        sub = T("另训一个模型，就能认出胸片来自哪家医院", "a separate model could tell which hospital", 34, INK)
        cur = self.show(tabs, 1, big, sub)
        self.mid("l37", 0.72)
        drop = T("肺炎模型换到新医院 → 成绩下降", "Pneumonia model at a new hospital → worse", 36, BAD, weight="BOLD")
        drop.next_to(cur[0], DOWN, buff=0.35)
        self.play(FadeIn(drop, shift=UP * 0.15), run_time=0.7)
        cur.add(drop)

        self.at("l38")
        self.play(FadeOut(cur), run_time=0.4)
        big = T("16% → 54%", "16% → 54%", 120, BAD, weight="BOLD")
        sub = T("良性痣被误判为癌（皮肤上有标记笔迹时）", "harmless moles flagged as cancer (with ink marks)", 34, INK)
        cur = self.show(tabs, 2, big, sub)

        self.at("l39")
        self.play(FadeOut(cur), run_time=0.4)
        brace = Brace(VGroup(tabs[1], tabs[2]), DOWN, color=HL)
        lab = T("捷径学习 · 过拟合的近亲", "Shortcut learning · a cousin of overfitting", 30, HL).next_to(brace, DOWN, buff=0.12)
        self.play(*[t.animate.set_color(INK) for t in tabs[1:]], GrowFromCenter(brace), FadeIn(lab), run_time=0.9)
        self.mid("l39", 0.55)
        end = T("学到的是巧合，不是规律", "Coincidence, not the pattern", 60, INK, weight="BOLD").move_to(DOWN * 0.3)
        self.play(FadeIn(end, shift=UP * 0.2), run_time=0.9)
        self.fade_all()
        self.finish()


class S8(Base):
    """⑥ 对策：验证集、更多数据、正则化。"""
    SEGMENT = "s8"

    def mini_axes(self) -> Axes:
        return Axes(x_range=[-3, 3, 1], y_range=[-2.5, 2.5, 1], x_length=3.4, y_length=2.0, tips=False,
                    axis_config={"stroke_color": MUTED, "stroke_width": 1.5, "include_ticks": False})

    def card(self, title: Text, body: Mobject) -> VGroup:
        box = RoundedRectangle(corner_radius=0.2, width=4.2, height=4.9, stroke_color=style.PANEL_EDGE, stroke_width=2,
                               fill_color=style.BG, fill_opacity=1)
        content = VGroup(title, body).arrange(DOWN, buff=0.4)
        return VGroup(box, content.move_to(box))

    def construct(self) -> None:
        self.at("l40")
        title = T("发现和避免过拟合的三个办法", "Three ways to spot and prevent overfitting", 44, INK).to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1)
        xs = [-4.55, 0, 4.55]

        self.at("l41")
        parts = VGroup(*[Rectangle(width=w, height=0.6, stroke_width=0, fill_color=c, fill_opacity=0.9)
                         for w, c in ((1.9, TRAIN_C), (0.9, VALID_C), (0.9, TEST_C))]).arrange(RIGHT, buff=0.04)
        names = VGroup(T("训练", "Train", 26), T("验证", "Valid.", 26), T("测试", "Test", 26))
        for n, r in zip(names, parts):
            n.next_to(r, DOWN, buff=0.12)
        sub1 = VGroup(T("验证集 = 模拟考", "Validation = mock exam", 28, VALID_C),
                      T("挑模型、早发现", "pick models, catch it early", 26, MUTED)).arrange(DOWN, buff=0.12)
        c1 = self.card(T("① 留出验证集", "① Hold out validation", 30, HL),
                       VGroup(VGroup(parts, names), sub1).arrange(DOWN, buff=0.5)).move_to(RIGHT * xs[0] + DOWN * 0.3)
        self.play(FadeIn(c1, shift=UP * 0.3), run_time=1)

        self.at("l42")
        ax2 = self.mini_axes()
        mx, my, mc = more_data_fit()
        d10 = VGroup(*[Dot(ax2.c2p(x, y), radius=0.06, color=TRAIN_C) for x, y in zip(XTR, YTR)])
        sub2 = VGroup(T("从 10 个点到 40 个点", "From 10 points to 40", 26, MUTED),
                      T("同样的复杂模型", "same complex model", 26, MUTED)).arrange(DOWN, buff=0.1)
        c2 = self.card(T("② 收集更多数据", "② More data", 30, HL),
                       VGroup(VGroup(ax2, d10), sub2).arrange(DOWN, buff=0.3)).move_to(RIGHT * xs[1] + DOWN * 0.3)
        d40 = VGroup(*[Dot(ax2.c2p(x, y), radius=0.045, color=TRAIN_C) for x, y in zip(mx, my)])
        f10 = ax2.plot(lambda x: float(np.clip(np.polyval(FITS[9], x), -2.5, 2.5)), x_range=[-2.95, 2.95, 0.01],
                       color=WIGGLE_C, stroke_width=4)
        f40 = ax2.plot(lambda x: float(np.clip(np.polyval(mc, x), -2.5, 2.5)), x_range=[-2.9, 2.9, 0.01], color=MID_C,
                       stroke_width=4)
        self.play(FadeIn(c2, shift=UP * 0.3), Create(f10), run_time=1)
        self.mid("l42", 0.4)
        self.play(ReplacementTransform(d10, d40), Transform(f10, f40), run_time=1.6)

        self.at("l43")
        ax3 = self.mini_axes()
        d3 = VGroup(*[Dot(ax3.c2p(x, y), radius=0.06, color=TRAIN_C) for x, y in zip(XTR, YTR)])
        sub3 = VGroup(T("同样 10 个点", "Same 10 points", 26, MUTED),
                      T("加上约束", "add a constraint", 26, MUTED)).arrange(DOWN, buff=0.1)
        c3 = self.card(T("③ 正则化", "③ Regularization", 30, HL),
                       VGroup(VGroup(ax3, d3), sub3).arrange(DOWN, buff=0.3)).move_to(RIGHT * xs[2] + DOWN * 0.3)
        w = ridge_fit()
        f3a = ax3.plot(lambda x: float(np.clip(np.polyval(FITS[9], x), -2.5, 2.5)), x_range=[-2.95, 2.95, 0.01],
                       color=WIGGLE_C, stroke_width=4)
        f3b = ax3.plot(lambda x: ridge_eval(w, x), x_range=[-2.95, 2.95, 0.01], color=MID_C, stroke_width=4)
        self.play(FadeIn(c3, shift=UP * 0.3), Create(f3a), run_time=1)
        self.mid("l43", 0.5)
        self.play(Transform(f3a, f3b), run_time=1.6)
        self.fade_all()
        self.finish()
