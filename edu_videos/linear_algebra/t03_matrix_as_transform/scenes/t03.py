# -*- coding: utf-8 -*-
"""t03 矩阵即线性变换：六段画面，按 timeline.json 的句子时间触发。

    manim -r 1920,1080 --fps 30 scenes/t03.py S1 S2 S3 S4 S5 S6

记号：原基向量 î、ĵ、v⃗；变换后一律带撇 î′、ĵ′、v⃗′；「落点」只说原向量的（「î 的落点 = î′」）。
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from manim import *

HERE = Path(__file__).resolve()
sys.path[:0] = [str(HERE.parents[4] / "tools"), str(HERE.parents[3] / "_shared")]
from edu_manim import TOP, CuedScene  # noqa: E402
from style import (BAD, BG, GOOD, HL, I_COLOR, INK, J_COLOR, MUTED, V_COLOR, backed, hat, panel, plane,  # noqa: E402
                   vec, zh)

SHEAR = np.array([[1, 1], [0, 1]])
O_SIDE = LEFT * 2.4 + UP * 0.25          # 右侧留公式面板时的原点
O_MID = UP * 0.3
U = 1.5                                   # 有公式面板的段放大网格，箭头与标签不挤


def cmat(cols: list[tuple[int, int]], colored: bool = True) -> Matrix:
    m = Matrix([[cols[0][0], cols[1][0]], [cols[0][1], cols[1][1]]], h_buff=1.1)
    if colored:
        for c, color in zip(m.get_columns(), (I_COLOR, J_COLOR)):
            c.set_color(color)
    return m


def V(o: np.ndarray, x: float, y: float, color: str, start: tuple[float, float] = (0, 0)) -> Arrow:
    return vec(o, x, y, color, start=start, unit=U)


def comp(o: np.ndarray, x: float, y: float, color: str, start: tuple[float, float]) -> Arrow:
    """拼法里的分量箭头：细一点、半透明，与基向量本身区分。"""
    return V(o, x, y, color, start=start).set_stroke(width=5).set_opacity(0.7)


def tpt(m: np.ndarray, p: tuple[float, float]) -> tuple[float, float]:
    q = m @ np.array(p)
    return float(q[0]), float(q[1])


def move_dots(dots: VGroup, m: np.ndarray, o: np.ndarray) -> list[Animation]:
    """只移动点的位置，不让点本身被拉歪。"""
    return [d.animate.move_to(o + np.append(m @ (d.get_center() - o)[:2], 0)) for d in dots]


def lab(mob: Mobject) -> VGroup:
    return backed(mob, 0.5)


def vname(prime: bool = False) -> MathTex:
    return MathTex(r"\vec v" + (r"\,'" if prime else ""), color=V_COLOR)


def check(ok: bool, text: str) -> VGroup:
    mark = MathTex(r"\checkmark" if ok else r"\times", color=GOOD if ok else BAD).scale(1.4)
    return backed(VGroup(mark, zh(text, 34, GOOD if ok else BAD)).arrange(RIGHT, buff=0.2)).set_z_index(TOP)


class Base(CuedScene):
    TIMELINE = HERE.parents[1] / "timeline.json"


class S1(Base):
    SEGMENT = "s1"

    def construct(self) -> None:
        teaser = plane(ORIGIN, span=20).set_opacity(0.35)
        self.play(FadeIn(teaser), run_time=0.4)
        m = cmat([(1, 0), (1, 1)], colored=False).scale(1.4)
        m_bg = BackgroundRectangle(m, color=BG, fill_opacity=0.85, buff=0.25)
        self.at("l01")
        self.play(FadeIn(m_bg), Write(m), teaser.animate.apply_matrix(SHEAR), run_time=self.fit("l01", 0.9, 1.5, 3))

        self.at("l02")
        eq = MathTex(r"\begin{bmatrix}1&1\\0&1\end{bmatrix}", r"\begin{bmatrix}x\\y\end{bmatrix}", "=",
                     r"\begin{bmatrix}1\cdot x+1\cdot y\\0\cdot x+1\cdot y\end{bmatrix}").scale(1.2).shift(UP * 0.3)
        self.play(FadeOut(teaser), FadeOut(m_bg), ReplacementTransform(m, eq[0]), run_time=0.8)
        self.play(Write(eq[1:]), run_time=self.fit("l02", 0.6, 1.2, 2.2))
        self.play(Indicate(eq[3], color=HL), run_time=0.8)

        self.at("l03")
        self.play(FadeOut(eq[1:]), eq[0].animate.scale(1.25).move_to(UP * 0.3), run_time=0.8)
        q = MathTex("?", color=HL).scale(3).next_to(eq[0], RIGHT, buff=0.6)
        self.mid("l03", 0.55)
        self.play(FadeIn(q, scale=0.5), Circumscribe(eq[0], color=HL), run_time=1.2)

        self.at("l04")
        p = plane(ORIGIN, span=20)
        p.z_index = -1
        corner = eq[0]
        self.play(FadeOut(q), corner.animate.scale(0.6).to_corner(UL, buff=0.5), FadeIn(p), run_time=1)
        corner_bg = BackgroundRectangle(corner, color=BG, fill_opacity=0.85, buff=0.15)
        self.add(corner_bg, corner)
        tag = backed(zh("矩阵 = 整个平面的一次变换", 40, HL)).to_edge(UP, buff=0.5)
        self.mid("l04", 0.45)
        self.play(FadeIn(tag), p.animate.apply_matrix(SHEAR), run_time=self.fit("l04", 0.9, 2, 3.5))
        self.fade_all()
        self.finish()


class S2(Base):
    SEGMENT = "s2"

    def construct(self) -> None:
        o = O_MID
        p = plane(o)
        self.play(FadeIn(p), run_time=0.5)

        self.at("l05")
        title = backed(VGroup(zh("变换：", 34, HL), zh("输入一个向量，输出一个向量", 34)).arrange(RIGHT, buff=0.1))
        title.to_corner(UL, buff=0.4).set_z_index(TOP)
        v = vec(o, 2, 1, V_COLOR)
        self.play(FadeIn(title), GrowArrow(v), run_time=1)
        self.mid("l05", 0.6)
        self.play(Transform(v, vec(o, 3, 1, V_COLOR)), run_time=1.2)

        self.at("l06")
        dots = VGroup(*[Dot(o + np.array([x, y, 0]), radius=0.065, color=HL) for x in range(-7, 8) for y in range(-3, 4)])
        self.play(FadeOut(v), LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.004),
                  run_time=self.fit("l06", 0.6, 1.2, 2.5))

        self.at("l07")
        axis = Line(o + LEFT * 7.5, o + RIGHT * 7.5, color=HL, stroke_width=7)
        self.play(Create(axis), run_time=0.6)
        p.save_state()
        dots.save_state()
        self.play(p.animate.apply_matrix(SHEAR, about_point=o), *move_dots(dots, SHEAR, o),
                  run_time=self.fit("l07", 0.85, 2, 4))
        self.play(FadeOut(axis), run_time=0.4)

        self.at("l08")
        title2 = backed(zh("线性变换", 40, HL)).to_corner(UL, buff=0.4).set_z_index(TOP)
        self.play(Restore(p), Restore(dots), ReplacementTransform(title, title2), run_time=1.2)

        self.at("l09")
        r1 = backed(zh("① 原点不动", 32)).set_z_index(TOP)
        r2 = backed(zh("② 直线仍是直线，网格线平行且等距", 32)).set_z_index(TOP)
        r1.next_to(title2, DOWN, aligned_edge=LEFT, buff=0.25)
        r2.next_to(r1, DOWN, aligned_edge=LEFT, buff=0.1)
        ring = Circle(radius=0.25, color=HL, stroke_width=5).move_to(o)
        self.play(FadeIn(r1), Create(ring), run_time=0.8)
        self.mid("l09", 0.4)
        self.play(FadeIn(r2), FadeOut(ring), run_time=0.8)
        self.mid("l09", 0.62)
        ok = check(True, "线性").to_corner(UR, buff=0.4)
        self.play(p.animate.apply_matrix(SHEAR, about_point=o), *move_dots(dots, SHEAR, o),
                  FadeIn(ok), run_time=self.fit("l09", 0.85, 1.5, 2.5))

        self.at("l10")
        bent = plane(o)
        bent.prepare_for_nonlinear_transform()
        self.play(FadeOut(dots), FadeOut(ok), FadeTransform(p, bent), run_time=0.6)
        bad1 = check(False, "线弯了").to_corner(UR, buff=0.4)
        wave = lambda q: q + 0.45 * np.array([np.sin(q[1] - o[1]), np.sin(q[0] - o[0]), 0])
        self.play(bent.animate.apply_function(wave), FadeIn(bad1), run_time=self.fit("l10", 0.85, 1.5, 2.5))

        self.at("l11")
        p2 = plane(o)
        origin = Dot(o, color=HL, radius=0.11)
        self.play(FadeOut(bad1), FadeTransform(bent, p2), FadeIn(origin), run_time=0.6)
        bad2 = check(False, "原点跑了").to_corner(UR, buff=0.4)
        was = Circle(radius=0.2, color=BAD, stroke_width=5).move_to(o)
        self.play(VGroup(p2, origin).animate.shift(RIGHT * 1.5 + UP * 0.8), FadeIn(bad2), Indicate(r1, color=BAD),
                  FadeIn(was), run_time=self.fit("l11", 0.7, 1.5, 2.2))
        trail = Arrow(o, origin.get_center(), buff=0.25, color=BAD, stroke_width=5, tip_length=0.22)
        self.play(GrowArrow(trail), run_time=0.6)
        self.fade_all()
        self.finish()


class S3(Base):
    SEGMENT = "s3"

    def construct(self) -> None:
        o = O_SIDE
        ghost, p = plane(o, faint=True, unit=U), plane(o, unit=U)
        self.box = panel()
        self.play(FadeIn(ghost), FadeIn(p), FadeIn(self.box), run_time=0.5)

        self.at("l12")
        dots = VGroup(*[Dot(o + U * np.array([x, y, 0]), radius=0.06, color=HL) for x in range(-3, 2) for y in range(-2, 3)])
        q = self.stack(VGroup(zh("无穷多个点，", 36), zh("怎么描述？", 36)).arrange(DOWN, buff=0.15))
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.01), FadeIn(q), run_time=1.5)

        self.at("l13")
        key = zh("只需盯住两个向量", 36, HL).move_to(q).set_z_index(TOP + 1)
        self.play(FadeOut(dots), ReplacementTransform(q, key), run_time=0.8)

        self.at("l14")
        i, j = V(o, 1, 0, I_COLOR), V(o, 0, 1, J_COLOR)
        il = lab(hat("i", I_COLOR)).add_updater(lambda m: m.next_to(i.get_end(), DR, buff=0.05))
        jl = lab(hat("j", J_COLOR)).add_updater(lambda m: m.next_to(j.get_end(), RIGHT, buff=0.08))
        self.play(GrowArrow(i), FadeIn(il), run_time=0.8)
        self.mid("l14", 0.3)
        self.play(GrowArrow(j), FadeIn(jl), run_time=0.8)
        self.mid("l14", 0.55)
        basis = self.stack(MathTex(r"\hat{\imath}=\begin{bmatrix}1\\0\end{bmatrix}", r",\quad",
                                   r"\hat{\jmath}=\begin{bmatrix}0\\1\end{bmatrix}").scale(0.9))
        basis[0].set_color(I_COLOR)
        basis[2].set_color(J_COLOR)
        self.play(Write(basis), Indicate(il, color=HL), Indicate(jl, color=HL), run_time=1.2)

        self.at("l15")
        v = V(o, -1, 2, V_COLOR)
        vl = lab(vname()).add_updater(lambda m: m.next_to(v.get_end(), UR, buff=0.05))
        self.play(GrowArrow(v), FadeIn(vl), run_time=0.9)
        self.mid("l15", 0.5)
        ci = comp(o, -1, 0, I_COLOR, start=(0, 0))
        cj1 = comp(o, -1, 1, J_COLOR, start=(-1, 0))
        cj2 = comp(o, -1, 2, J_COLOR, start=(-1, 1))
        cil = MathTex(r"-1\,\hat{\imath}", color=I_COLOR).scale(0.75).add_updater(lambda m: m.next_to(ci, DOWN, buff=0.12))
        cjl = MathTex(r"2\,\hat{\jmath}", color=J_COLOR).scale(0.75).add_updater(
            lambda m: m.move_to((cj1.get_start() + cj2.get_end()) / 2 + LEFT * 0.45))
        f1 = self.stack(MathTex(r"\vec v", "=", "-1", r"\,\hat{\imath}", "+", "2", r"\,\hat{\jmath}").scale(1.05))
        f1[0].set_color(V_COLOR)
        f1[2:4].set_color(I_COLOR)
        f1[5:7].set_color(J_COLOR)
        self.play(GrowArrow(ci), FadeIn(cil), Write(f1[:4]), run_time=0.9)
        self.mid("l15", 0.78)
        self.play(GrowArrow(cj1), GrowArrow(cj2), FadeIn(cjl), Write(f1[4:]), run_time=0.9)

        self.at("l16")
        self.mid("l16", 0.12)
        self.play(Indicate(ci, color=HL, scale_factor=1.05), run_time=0.8)
        self.mid("l16", 0.3)
        self.play(Indicate(cj1, color=HL, scale_factor=1.05), run_time=0.5)
        self.play(Indicate(cj2, color=HL, scale_factor=1.05), run_time=0.5)
        self.mid("l16", 0.5)
        self.play(p.animate.apply_matrix(SHEAR, about_point=o),
                  Transform(i, V(o, *tpt(SHEAR, (1, 0)), I_COLOR)), Transform(j, V(o, *tpt(SHEAR, (0, 1)), J_COLOR)),
                  Transform(v, V(o, *tpt(SHEAR, (-1, 2)), V_COLOR)),
                  Transform(ci, comp(o, *tpt(SHEAR, (-1, 0)), I_COLOR, start=(0, 0))),
                  Transform(cj1, comp(o, *tpt(SHEAR, (-1, 1)), J_COLOR, start=tpt(SHEAR, (-1, 0)))),
                  Transform(cj2, comp(o, *tpt(SHEAR, (-1, 2)), J_COLOR, start=tpt(SHEAR, (-1, 1)))),
                  run_time=self.fit("l16", 0.85, 2.5, 3.5))

        self.at("l17")
        f2 = self.stack(MathTex(r"\vec v\,'", "=", "-1", r"\,\hat{\imath}\,'", "+", "2", r"\,\hat{\jmath}\,'").scale(1.05))
        f2[0].set_color(V_COLOR)
        f2[2:4].set_color(I_COLOR)
        f2[5:7].set_color(J_COLOR)
        self.play(Transform(il, lab(hat("i", I_COLOR, prime=True)).move_to(il)),
                  Transform(jl, lab(hat("j", J_COLOR, prime=True)).move_to(jl)),
                  Transform(vl, lab(vname(prime=True)).move_to(vl)),
                  Transform(cil, MathTex(r"-1\,\hat{\imath}\,'", color=I_COLOR).scale(0.75).move_to(cil)),
                  Transform(cjl, MathTex(r"2\,\hat{\jmath}\,'", color=J_COLOR).scale(0.75).move_to(cjl)), run_time=0.6)
        self.play(TransformFromCopy(f1, f2), run_time=1.2)
        self.play(Indicate(ci, color=HL), Indicate(cj1, color=HL), Indicate(cj2, color=HL), run_time=1)

        self.at("l18")
        take = self.stack(VGroup(
            VGroup(MathTex(r"\hat{\imath},\ \hat{\jmath}", color=INK), zh("的落点", 34)).arrange(RIGHT, buff=0.15),
            VGroup(MathTex(r"\Rightarrow", color=HL), zh("整个平面的去向", 34, HL)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, buff=0.2), gap=0.5)
        self.play(FadeIn(take, shift=UP * 0.2), Flash(i.get_end(), color=I_COLOR), Flash(j.get_end(), color=J_COLOR),
                  run_time=1.2)

        self.until(self.end_of("l18") + 0.1)
        self.play(*[FadeOut(m) for m in (*self.clear_stack(), ci, cj1, cj2, cil, cjl, key)], run_time=0.5)
        self.finish()


class S4(Base):
    SEGMENT = "s4"

    def construct(self) -> None:
        o = O_SIDE
        ghost, p = plane(o, faint=True, unit=U), plane(o, unit=U).apply_matrix(SHEAR, about_point=o)
        i, j, v = V(o, 1, 0, I_COLOR), V(o, 1, 1, J_COLOR), V(o, 1, 2, V_COLOR)
        il = lab(hat("i", I_COLOR, prime=True)).next_to(i.get_end(), DR, buff=0.05)
        jl = lab(hat("j", J_COLOR, prime=True)).next_to(j.get_end(), RIGHT, buff=0.08)
        vl = lab(vname(prime=True)).next_to(v.get_end(), UR, buff=0.05)
        self.box = panel()
        self.add(ghost, p, i, j, v, il, jl, vl, self.box)

        self.at("l19")
        ci = lab(MathTex("=(1,0)", color=I_COLOR).scale(0.85)).next_to(il, RIGHT, buff=0.02)
        cj = lab(MathTex("=(1,1)", color=J_COLOR).scale(0.85)).next_to(jl, RIGHT, buff=0.02)
        self.play(Indicate(i, color=HL), Write(ci), run_time=1)
        self.mid("l19", 0.5)
        self.play(Indicate(j, color=HL), Write(cj), run_time=1)

        self.at("l20")
        mat = self.stack(cmat([(1, 0), (1, 1)]).scale(0.95))
        cols = mat.get_columns()
        self.play(FadeIn(mat.get_brackets()), TransformFromCopy(ci, cols[0]), run_time=1)
        self.mid("l20", 0.5)
        self.play(TransformFromCopy(cj, cols[1]), run_time=1)

        self.at("l21")
        caps = self.stack(VGroup(
            VGroup(zh("第 1 列", 30, I_COLOR), zh("=", 30), MathTex(r"\hat{\imath}", color=I_COLOR),
                   zh("的落点", 30)).arrange(RIGHT, buff=0.15),
            VGroup(zh("第 2 列", 30, J_COLOR), zh("=", 30), MathTex(r"\hat{\jmath}", color=J_COLOR),
                   zh("的落点", 30)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.15))
        rect = SurroundingRectangle(mat, color=HL, buff=0.12).set_z_index(TOP + 2)
        self.play(Create(rect), FadeIn(caps), run_time=1)

        self.at("l22")
        self.play(*[FadeOut(m) for m in (*self.clear_stack(), rect)], run_time=0.5)
        r1 = self.stack(MathTex(r"\vec v", "=", r"x\,\hat{\imath}", "+", r"y\,\hat{\jmath}"))
        r1[0].set_color(V_COLOR)
        r1[2].set_color(I_COLOR)
        r1[4].set_color(J_COLOR)
        self.play(Write(r1), run_time=1)
        self.mid("l22", 0.33)
        r2 = self.stack(MathTex(r"\vec v\,'", "=", r"x\,\hat{\imath}\,'", "+", r"y\,\hat{\jmath}\,'"))
        r2[0].set_color(V_COLOR)
        r2[2].set_color(I_COLOR)
        r2[4].set_color(J_COLOR)
        self.play(TransformFromCopy(r1, r2), run_time=1)
        self.mid("l22", 0.62)
        gen = self.stack(MathTex(r"\begin{bmatrix}1&1\\0&1\end{bmatrix}\begin{bmatrix}x\\y\end{bmatrix}", "=", "x",
                                 r"\begin{bmatrix}1\\0\end{bmatrix}", "+", "y", r"\begin{bmatrix}1\\1\end{bmatrix}"))
        gen[3].set_color(I_COLOR)
        gen[6].set_color(J_COLOR)
        self.play(Write(gen), run_time=self.fit("l22", 0.7, 1, 2))

        self.at("l33")
        exp = self.stack(VGroup(MathTex("=", r"\begin{bmatrix}x+y\\y\end{bmatrix}"),
                                MathTex(r"\checkmark", color=GOOD), zh("与行乘列相同", 28, GOOD)).arrange(RIGHT, buff=0.2))
        self.play(Write(exp[0]), run_time=1)
        self.play(FadeIn(exp[1:]), run_time=0.6)

        self.at("l23")
        self.play(FadeOut(r1), FadeOut(r2), run_time=0.4)
        keep = VGroup(gen, exp)
        self.play(keep.animate.next_to(self.box.get_top() + DOWN * 0.35, DOWN, buff=0), run_time=0.5)
        self._stack = [keep]
        sub = self.stack(MathTex(r"\begin{bmatrix}1&1\\0&1\end{bmatrix}\begin{bmatrix}-1\\2\end{bmatrix}", "=", "-1",
                                 r"\begin{bmatrix}1\\0\end{bmatrix}", "+", "2", r"\begin{bmatrix}1\\1\end{bmatrix}"))
        sub[3].set_color(I_COLOR)
        sub[6].set_color(J_COLOR)
        res = self.stack(MathTex("=", r"\begin{bmatrix}1\\2\end{bmatrix}"))
        res[1].set_color(V_COLOR)
        self.play(Write(sub[0]), run_time=0.8)
        self.mid("l23", 0.3)
        self.play(Write(sub[1:]), run_time=1.2)
        self.mid("l23", 0.78)
        self.play(Write(res), run_time=0.8)

        self.at("l24")
        cv = lab(MathTex("=(1,2)", color=V_COLOR).scale(0.85)).next_to(vl, RIGHT, buff=0.02)
        self.play(Flash(v.get_end(), color=V_COLOR), Write(cv), Indicate(vl, color=V_COLOR), run_time=1.2)
        self.mid("l24", 0.45)
        box_res = SurroundingRectangle(res, color=HL, buff=0.1).set_z_index(TOP + 2)
        self.play(Create(box_res), Circumscribe(cv, color=HL), run_time=1.4)
        self.fade_all()
        self.finish()


class S5(Base):
    SEGMENT = "s5"

    def construct(self) -> None:
        o = O_SIDE
        ghost, p = plane(o, faint=True, unit=U), plane(o, unit=U)
        i, j = V(o, 1, 0, I_COLOR), V(o, 0, 1, J_COLOR)
        il = lab(hat("i", I_COLOR)).add_updater(lambda m: m.next_to(i.get_end(), DR, buff=0.05))
        jl = lab(hat("j", J_COLOR)).add_updater(lambda m: m.next_to(j.get_end(), UL, buff=0.05))
        house = Polygon(*[o + U * np.array([x, y, 0]) for x, y in ((1.1, 0.4), (2.1, 0.4), (2.1, 1.2), (1.6, 1.7), (1.1, 1.2))],
                        color=HL, stroke_width=4, fill_color=HL, fill_opacity=0.25)
        self.box = panel()
        self.play(*[FadeIn(m) for m in (ghost, p, house, i, j, il, jl, self.box)], run_time=0.5)

        self.at("l25")
        title = self.stack(zh("练一个", 36, HL))
        mat = self.stack(cmat([(0, 1), (-1, 0)]).scale(1.05))
        cols = mat.get_columns()
        self.play(FadeIn(title), Write(mat), run_time=1)
        self.mid("l25", 0.45)
        r0 = SurroundingRectangle(cols[0], color=I_COLOR, buff=0.1).set_z_index(TOP + 2)
        self.play(Create(r0), run_time=0.6)
        self.mid("l25", 0.75)
        r1 = SurroundingRectangle(cols[1], color=J_COLOR, buff=0.1).set_z_index(TOP + 2)
        self.play(ReplacementTransform(r0, r1), run_time=0.6)

        self.at("l26")
        bars = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.18, height=0.6, fill_color=HL, fill_opacity=1,
                                         stroke_width=0) for _ in range(2)]).arrange(RIGHT, buff=0.18)
        pause = self.stack(VGroup(bars, zh("暂停，想一想", 40, HL)).arrange(RIGHT, buff=0.3), gap=0.6)
        ring = Circle(radius=0.45, color=HL, stroke_width=6).next_to(pause, DOWN, buff=0.3).set_z_index(TOP + 2)
        self.play(FadeOut(r1), FadeIn(pause, scale=1.1), run_time=0.6)
        self.until(self.end_of("l26"))
        self.play(Create(ring), run_time=max(self.cues["l27"][0] - self.now() - 0.2, 1.0), rate_func=linear)
        self.play(FadeOut(pause), FadeOut(ring), run_time=0.3)
        self._stack.remove(pause)

        i.save_state()
        j.save_state()
        self.at("l27")
        self.bring_to_front(i, il)
        r0 = SurroundingRectangle(cols[0], color=I_COLOR, buff=0.1).set_z_index(TOP + 2)
        self.play(Create(r0), Transform(i, V(o, 0, 1, I_COLOR)), j.animate.set_opacity(0.25), jl.animate.set_opacity(0.25),
                  Transform(il, lab(hat("i", I_COLOR, prime=True)).move_to(il)), run_time=1.4)
        ci = lab(MathTex("=(0,1)", color=I_COLOR).scale(0.85)).next_to(il, DOWN, aligned_edge=LEFT, buff=0.02)
        self.play(Write(ci), run_time=0.6)

        self.at("l28")
        r1 = SurroundingRectangle(cols[1], color=J_COLOR, buff=0.1).set_z_index(TOP + 2)
        self.play(ReplacementTransform(r0, r1), Transform(j, V(o, -1, 0, J_COLOR).set_opacity(1)),
                  Transform(jl, lab(hat("j", J_COLOR, prime=True)).move_to(jl)), run_time=1.4)
        cj = lab(MathTex("=(-1,0)", color=J_COLOR).scale(0.85)).next_to(j.get_end(), DOWN, buff=0.12)
        self.play(Write(cj), run_time=0.6)

        self.at("l29")
        arc = Arc(radius=2.4, start_angle=0.2, angle=PI / 2 - 0.4, arc_center=o, color=HL, stroke_width=6).add_tip(
            tip_length=0.25)
        ans = self.stack(VGroup(zh("逆时针转", 38, HL), MathTex(r"90^\circ", color=HL).scale(1.2)).arrange(RIGHT, buff=0.15),
                         gap=0.6)
        self.play(FadeOut(r1), FadeOut(ci), FadeOut(cj), Restore(i), Restore(j),
                  Transform(il, lab(hat("i", I_COLOR)).move_to(il)), Transform(jl, lab(hat("j", J_COLOR)).move_to(jl)),
                  run_time=0.8)
        self.play(Create(arc), FadeIn(ans), run_time=0.8)
        self.play(*[Rotate(m, PI / 2, about_point=o) for m in (p, house, i, j)], run_time=self.fit("l29", 0.8, 2.5, 4))
        self.play(Transform(il, lab(hat("i", I_COLOR, prime=True)).move_to(il)),
                  Transform(jl, lab(hat("j", J_COLOR, prime=True)).move_to(jl)), run_time=0.5)
        self.fade_all()
        self.finish()


class S6(Base):
    SEGMENT = "s6"

    def construct(self) -> None:
        self.at("l30")
        mat = cmat([(1, 0), (1, 1)]).scale(1.2).shift(UP * 1.9)
        labels = VGroup(
            VGroup(MathTex(r"\hat{\imath}", color=I_COLOR), zh("的落点", 28, I_COLOR)).arrange(RIGHT, buff=0.1),
            VGroup(MathTex(r"\hat{\jmath}", color=J_COLOR), zh("的落点", 28, J_COLOR)).arrange(RIGHT, buff=0.1))
        for lb, col in zip(labels, mat.get_columns()):
            lb.next_to(col, DOWN, buff=0.45)
        labels[0].shift(LEFT * 0.5)
        labels[1].shift(RIGHT * 0.5)
        line = VGroup(zh("矩阵的每一列", 50), zh("=", 50), zh("一个基向量的落点", 50, HL)).arrange(RIGHT, buff=0.25)
        line.shift(DOWN * 0.4)
        self.play(Write(mat), run_time=1)
        self.play(FadeIn(labels, shift=UP * 0.2), FadeIn(line, shift=UP * 0.2), run_time=1)

        self.at("l31")
        ask = VGroup(zh("看到矩阵，先问：", 38, MUTED), MathTex(r"\hat{\imath},\ \hat{\jmath}", color=INK).scale(1.1),
                     zh("去哪了？", 38, MUTED)).arrange(RIGHT, buff=0.15).next_to(line, DOWN, buff=0.7)
        self.play(FadeIn(ask, shift=UP * 0.2), run_time=1)

        self.at("l32")
        nxt = zh("下一集：两个变换接连发生 = 矩阵乘法", 30, MUTED).next_to(ask, DOWN, buff=0.6)
        self.play(FadeIn(nxt), run_time=1)
        self.finish()
