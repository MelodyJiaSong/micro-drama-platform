# -*- coding: utf-8 -*-
"""设计选型对比样张：同一画面只变一个变量（配色 P1–P3、字体 F1–F3），渲成 1920×1080 PNG，汇进 review.json 给用户按编号挑。

    python edu_videos/_shared/design/boards/build_boards.py
数据与 t01 实验相同（真实规律 1.2·sin(1.3x)+0.25x，种子 99，多项式 1/3/9 次）。产物：boards/renders/*.png、design/review.json。
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DESIGN = HERE.parent
REPO = DESIGN.parents[2]
FONTS = REPO / ".cache" / "fonts"
NODE = REPO / ".cache" / "node" / "hyperframes" / "node_modules"
OUT = HERE / "renders"

PALETTES = {
    "P1": {"name": "极简蓝（黑白灰 + 一个蓝）", "accent": "#2997FF", "accent2": "#2997FF", "train": "#F5F5F7", "test": "#2997FF",
           "warn": "#FF453A", "good": "#30D158", "grad": "linear-gradient(100deg,#F5F5F7,#F5F5F7)",
           "desc": "接近 Apple 官网：几乎全是黑白灰，只有一个蓝色强调；数据用白（练习）、蓝（考试）、红（出问题）。最克制。"},
    "P2": {"name": "青紫渐变（沿用现在的包装）", "accent": "#60A5FA", "accent2": "#A78BFA", "train": "#2DD4BF", "test": "#A78BFA",
           "warn": "#FB7185", "good": "#34D399", "grad": "linear-gradient(100deg,#2DD4BF,#60A5FA 45%,#A78BFA)",
           "desc": "片头片尾已经在用的青→蓝→紫渐变；数据用青（练习）、紫（考试）、珊瑚红（出问题）。更有科技感、更鲜艳。"},
    "P3": {"name": "暖琥珀（黑白灰 + 一个暖色）", "accent": "#FFB340", "accent2": "#FF8A3D", "train": "#F5F5F7", "test": "#FFB340",
           "warn": "#FF5E3A", "good": "#9BD5A9", "grad": "linear-gradient(100deg,#FFD27A,#FF8A3D)",
           "desc": "黑白灰 + 琥珀强调，偏人文、温暖；数据用白（练习）、琥珀（考试）、橙红（出问题）。和多数科技频道的冷色调区分开。"},
}
FONT_SETS = {
    "F1": {"name": "Noto Sans SC + Inter（现在用的）", "zh": "NotoSC", "latin": "Inter",
           "faces": [("NotoSC", "C:/Windows/Fonts/NotoSansSC-VF.ttf", "100 900"),
                     ("Inter", str(NODE / "@fontsource-variable/inter/files/inter-latin-wght-normal.woff2"), "100 900")],
           "desc": "思源黑体同源，中规中矩、最稳；英文配 Inter。OFL 开源，无署名要求。"},
    "F2": {"name": "HarmonyOS Sans SC（华为）", "zh": "HMOS", "latin": "HMOS",
           "faces": [("HMOS", str(FONTS / "harmonyos_sc/HarmonyOS_Sans_SC_Regular.ttf"), "400"),
                     ("HMOS", str(FONTS / "harmonyos_sc/HarmonyOS_Sans_SC_Medium.ttf"), "500"),
                     ("HMOS", str(FONTS / "harmonyos_sc/HarmonyOS_Sans_SC_Bold.ttf"), "700")],
           "desc": "笔画更几何、字面更开阔，观感最接近苹方 / SF；中英文同一家族。免费商用，须在作品中注明使用了 HarmonyOS Sans。"},
    "F3": {"name": "MiSans（小米）", "zh": "MiSans", "latin": "MiSans",
           "faces": [("MiSans", str(FONTS / "misans/MiSans-Regular.ttf"), "400"),
                     ("MiSans", str(FONTS / "misans/MiSans-Medium.ttf"), "500"),
                     ("MiSans", str(FONTS / "misans/MiSans-Bold.ttf"), "700")],
           "desc": "字形偏圆润、亲和，数字好看，字重最多（10 档）。免费商用，须注明使用了 MiSans。"},
}


def data() -> dict:
    truth = lambda x: 1.2 * np.sin(1.3 * x) + 0.25 * x
    rng = np.random.default_rng(99)
    xtr = np.linspace(-2.8, 2.8, 10) + rng.uniform(-0.12, 0.12, 10)
    ytr = truth(xtr) + rng.normal(0, 0.35, 10)
    xte = np.linspace(-2.5, 2.5, 6) + rng.uniform(-0.1, 0.1, 6)
    yte = truth(xte) + rng.normal(0, 0.3, 6)
    xs = np.linspace(-2.95, 2.95, 240)
    fits, mse = {}, {}
    for d in (1, 3, 9):
        c = np.polyfit(xtr, ytr, d)
        fits[d] = np.clip(np.polyval(c, xs), -3, 3).round(3).tolist()
        mse[d] = [round(float(np.mean((np.polyval(c, xtr) - ytr) ** 2)), 2), round(float(np.mean((np.polyval(c, xte) - yte) ** 2)), 2)]
    return {"xs": xs.round(3).tolist(), "train": np.c_[xtr, ytr].round(3).tolist(), "test": np.c_[xte, yte].round(3).tolist(),
            "fits": fits, "mse": mse}


BASE_CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
html,body { width:1920px; height:1080px; background:#000; overflow:hidden; }
.frame { position:relative; width:1920px; height:1080px; background:#000; color:#F5F5F7; }
.eyebrow { font-size:26px; letter-spacing:.16em; color:#86868B; font-weight:500; }
.sub { color:#86868B; }
"""


def faces_css(fs: dict) -> str:
    return "\n".join(f'@font-face {{ font-family:"{n}"; src:url("{Path(p).as_uri()}"); font-weight:{w}; }}' for n, p, w in fs["faces"])


def chart_frame(pid: str, D: dict) -> str:
    P = PALETTES[pid]
    fs = FONT_SETS["F1"]
    m = D["mse"]
    rows = [("①", "直线", "#86868B", m[1], "欠拟合"), ("②", "平缓曲线", P["good"], m[3], "刚刚好"), ("③", "弯曲线", P["warn"], m[9], "过拟合")]
    rows_html = "".join(f"""
      <div class="row"><div class="rh"><span style="color:{c}">{no} {name}</span><b style="color:{c}">{tag}</b></div>
        <div class="nums"><div><i>练习误差</i><em>{tr:.2f}</em></div><div><i>考试误差</i><em style="color:{c if no != '①' else '#F5F5F7'}">{te:.2f}</em></div></div></div>"""
                        for no, name, c, (tr, te), tag in rows)
    return f"""<!doctype html><html><head><meta charset="utf-8"><script src="{(NODE / 'd3/dist/d3.min.js').as_uri()}"></script>
<style>{faces_css(fs)}{BASE_CSS}
.frame {{ font-family:"{fs['latin']}","{fs['zh']}",sans-serif; }}
.head {{ position:absolute; left:120px; top:96px; }}
.head h1 {{ margin-top:18px; font-size:64px; font-weight:700; letter-spacing:.01em; }}
.head h1 span {{ background:{P['grad']}; -webkit-background-clip:text; color:transparent; }}
#c {{ position:absolute; left:80px; top:250px; }}
.side {{ position:absolute; left:1250px; top:300px; width:560px; display:grid; gap:44px; }}
.row {{ border-top:1px solid #2A2A2E; padding-top:22px; }}
.rh {{ display:flex; justify-content:space-between; font-size:30px; font-weight:600; }}
.rh b {{ font-weight:600; font-size:24px; letter-spacing:.08em; }}
.nums {{ display:grid; grid-template-columns:1fr 1fr; margin-top:14px; }}
.nums i {{ display:block; font-style:normal; font-size:20px; color:#86868B; letter-spacing:.06em; }}
.nums em {{ font-style:normal; font-size:56px; font-weight:600; font-variant-numeric:tabular-nums; }}
.legend {{ position:absolute; left:140px; top:948px; font-size:22px; color:#86868B; display:flex; gap:40px; align-items:center; }}
.legend span {{ display:inline-flex; gap:12px; align-items:center; }}
</style></head><body><div class="frame">
<div class="head"><div class="eyebrow">01 · 问题</div><h1>只看练习册，<span>第三种最好？</span></h1></div>
<svg id="c" width="1100" height="680"></svg>
<div class="side">{rows_html}</div>
<div class="legend"><span><svg width="16" height="16"><circle cx="8" cy="8" r="7" fill="{P['train']}"/></svg>练习题（训练数据）</span>
<span><svg width="18" height="18"><circle cx="9" cy="9" r="7" fill="none" stroke="{P['test']}" stroke-width="3"/></svg>考题（测试数据）</span></div>
</div><script>
const D = {json.dumps(D)};
const W = 1100, H = 680, x = d3.scaleLinear([-3, 3], [40, W - 40]), y = d3.scaleLinear([-3, 3], [H - 40, 40]);
const s = d3.select("#c");
s.append("line").attr("x1", 40).attr("x2", W - 40).attr("y1", y(0)).attr("y2", y(0)).attr("stroke", "#2A2A2E").attr("stroke-width", 2);
const line = d3.line().x((d, i) => x(D.xs[i])).y(d => y(d)).curve(d3.curveBasis);
const curves = [[1, "#86868B", 3, .6], [3, "{P['good']}", 5, 1], [9, "{P['warn']}", 5, 1]];
for (const [d, c, w, o] of curves) s.append("path").attr("d", line(D.fits[d])).attr("fill", "none").attr("stroke", c).attr("stroke-width", w).attr("opacity", o).attr("stroke-linecap", "round");
for (const [a, b] of D.train) s.append("circle").attr("cx", x(a)).attr("cy", y(b)).attr("r", 9).attr("fill", "{P['train']}");
for (const [a, b] of D.test) s.append("circle").attr("cx", x(a)).attr("cy", y(b)).attr("r", 9).attr("fill", "#000").attr("stroke", "{P['test']}").attr("stroke-width", 3.5);
</script></body></html>"""


STAGES = {
    "S1": {"name": "纯黑 + 光晕（现在的做法）", "bg": "#000000", "ink": "#F5F5F7", "sub": "#86868B", "hair": "#2A2A2E", "glow": True,
           "map": {},
           "desc": "纯黑舞台加柔和光晕。最有发布会的戏剧感；但 B 站上「黑底 + 发光 + 同款 BGM」已被大量 AI 量产视频用滥，有观众说审美疲劳。"},
    "S2": {"name": "深灰、不加光晕", "bg": "#161617", "ink": "#F5F5F7", "sub": "#8E8E93", "hair": "#38383A", "glow": False,
           "map": {},
           "desc": "Apple 官网深色区块的做法：近黑的深灰、不发光、靠排版和留白出质感。保留高级感，又和「黑底发光」的 AI 量产风拉开距离。"},
    "S3": {"name": "浅色（白底）", "bg": "#FBFBFD", "ink": "#1D1D1F", "sub": "#6E6E73", "hair": "#D2D2D7", "glow": False,
           "map": {"#2997FF": "#0071E3", "#FF453A": "#E5372B", "#30D158": "#1F9D4C"},
           "desc": "Apple 官网浅色区块的做法：白底深字，像一本精装书，长时间看最不累、字最清楚；在一片黑底 AI 视频里最显眼。数据颜色换成适合白底的深一档。"},
}


def stage_frame(sid: str, D: dict) -> str:
    """同一张「三种学法」（P1 配色、F1 字体），只换舞台底色。"""
    S = STAGES[sid]
    html = chart_frame("P1", D)
    for old, new in S["map"].items():
        html = html.replace(old, new)
    html = (html.replace("#F5F5F7", S["ink"]).replace("#86868B", S["sub"]).replace("#2A2A2E", S["hair"])
                .replace('"#000"', f'"{S["bg"]}"').replace("background:#000", f"background:{S['bg']}"))
    if S["glow"]:
        html = html.replace('<div class="frame">', '<div class="frame"><div style="position:absolute;left:120px;top:200px;width:1100px;height:760px;'
                            'background:radial-gradient(closest-side,rgba(41,151,255,.22),rgba(167,139,250,.10) 55%,transparent 78%);filter:blur(40px)"></div>', 1)
    return html


def font_frame(fid: str) -> str:
    fs = FONT_SETS[fid]
    P = PALETTES["P1"]
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{faces_css(fs)}{BASE_CSS}
.frame {{ font-family:"{fs['latin']}","{fs['zh']}",sans-serif; display:grid; grid-template-columns:1.05fr 1fr; }}
.l {{ padding:150px 0 0 140px; }}
.l .big {{ white-space:nowrap; font-size:128px; font-weight:700; letter-spacing:-.02em; color:{P['warn']}; line-height:1; margin-top:36px; font-variant-numeric:tabular-nums; }}
.l p {{ font-size:36px; margin-top:28px; font-weight:500; line-height:1.5; }}
.l .src {{ font-size:22px; color:#86868B; margin-top:48px; letter-spacing:.04em; }}
.r {{ padding:150px 100px 0 60px; border-left:1px solid #2A2A2E; margin:120px 0; }}
.r h2 {{ white-space:nowrap; font-size:50px; font-weight:700; line-height:1.3; margin-top:36px; }}
.r h2 span {{ color:{P['accent']}; }}
.r .en {{ font-size:30px; color:#86868B; margin-top:30px; line-height:1.5; font-weight:400; }}
.r .body {{ font-size:28px; margin-top:56px; line-height:1.75; font-weight:400; color:#D2D2D7; }}
.tag {{ position:absolute; right:60px; bottom:46px; font-size:20px; color:#55555A; letter-spacing:.06em; }}
</style></head><body><div class="frame">
<div class="l"><div class="eyebrow">05 · 现实里的代价</div><div class="big">16% → 54%</div>
<p>良性痣被误判为癌的比例<br>（皮肤上有标记笔迹时）</p><div class="src">Winkler 等 ·《JAMA Dermatology》· 2019</div></div>
<div class="r"><div class="eyebrow">一句话记住 · IN ONE SENTENCE</div><h2>过拟合，就是把答案背下来了，<br><span>却没学会规律。</span></h2>
<div class="en">Overfitting is memorizing the answers without learning the pattern.</div>
<div class="body">训练误差 0.00，测试误差 1.80，是第二种的 25 倍。<br>学习，其实是一种压缩：用 4 个数字，说清 10 个点。</div></div>
<div class="tag">{fs['name']}</div></div></body></html>"""


def main() -> None:
    from playwright.sync_api import sync_playwright
    OUT.mkdir(parents=True, exist_ok=True)
    D = data()
    jobs = ({f"palette_{k}": chart_frame(k, D) for k in PALETTES} | {f"font_{k}": font_frame(k) for k in FONT_SETS}
            | {f"stage_{k}": stage_frame(k, D) for k in STAGES})
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 1920, "height": 1080})
        for name, html in jobs.items():
            f = OUT / f"{name}.html"
            f.write_text(html, encoding="utf-8")
            pg.goto(f.as_uri())
            pg.wait_for_timeout(600)
            pg.screenshot(path=str(OUT / f"{name}.png"))
            print(name)
        b.close()
    rel = lambda q: q.relative_to(REPO).as_posix()
    samples = DESIGN / "samples"
    illus = [("I1", "clay", "哑光陶土 3D", "柔和棚拍光、哑光陶土质感，像 Apple 发布会的产品图；温和、高级，适合比喻和类比的场景。"),
             ("I2", "glass", "磨砂玻璃 3D", "半透明玻璃、内部透光、冷色渐变；最有科技感和未来感，和青紫渐变配色最搭。"),
             ("I3", "line", "极简线条图标", "单一粗细的白线、几乎不着色；最克制，像发布会上的图示；信息清楚但温度最低。")]
    out = {"title": "AI 高频词 · 设计选型", "character": "edu_videos 频道视觉", "updated": date.today().isoformat(),
           "notes": ["每组只变一个变量，其他都一样。每组挑一个编号告诉我，例如「S2、P1、F2、I1」；也可以说「P1 但强调色换成 P3 的」。",
                     "字体组用的是 P1 配色，配色组用的是 F1 字体，互不影响。插图组是同一个场景（沙发上睡着的猫）的三种画法。"],
           "sections": [
               {"id": "stage", "title": "舞台底色（S）", "hint": "同一张数据图（P1 配色），只换底色；B 站调研提醒「黑底发光」已被 AI 量产视频用滥", "items": [
                   {"id": k, "label": v["name"], "path": rel(OUT / f"stage_{k}.png"), "desc": v["desc"]} for k, v in STAGES.items()]},
               {"id": "palette", "title": "配色（P）", "hint": "同一张「三种学法」数据图，只换颜色", "items": [
                   {"id": k, "label": v["name"], "path": rel(OUT / f"palette_{k}.png"), "desc": v["desc"]} for k, v in PALETTES.items()]},
               {"id": "font", "title": "字体（F）", "hint": "同一张案例卡与一句话总结，只换字体", "items": [
                   {"id": k, "label": v["name"], "path": rel(OUT / f"font_{k}.png"), "desc": v["desc"]} for k, v in FONT_SETS.items()]},
               {"id": "illus", "title": "插图方向（I）", "hint": "同一个场景的三种美术方向（Codex 出图）", "items": [
                   {"id": i, "label": n, "path": rel(samples / f"illus_{k}.png"), "desc": d} for i, k, n, d in illus if (samples / f"illus_{k}.png").exists()]},
           ]}
    (DESIGN / "review.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("review.json →", f"/character-review?path={rel(DESIGN)}")


if __name__ == "__main__":
    main()
