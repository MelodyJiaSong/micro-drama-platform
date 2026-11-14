# -*- coding: utf-8 -*-
"""教学视频网页场景：scenes/web/sN.html（排版、D3 图表、GSAP 动效）按配音时间轴渲成视频，或在任意时刻截图。

    python tools/edu_web.py tokens                                   tokens.json → design/web/tokens.css
    python tools/edu_web.py render <知识点目录> [sN ...] [--lang en]   → renders/[en/]sN.mp4（HyperFrames）
    python tools/edu_web.py still <知识点目录> sN --at l11:1,l12:0.5 [--lang en] [--out x.png]   截图（样张、审片）
    python tools/edu_web.py check <知识点目录> [--lang en]            每句收口处截图前自检版式 → renders/[en/]web_check.log

场景文件格式：一个 HTML 片段，可含 <style>、标签与 <script>。标签写 data-zh / data-en 双语；脚本用 window.EDU
（edu_videos/_shared/design/web/runtime.js）按句排动画，最后不用自己调 done()；本期共用的构件放 scenes/web/_lib.js。数据来自 scenes/data.json
（由 scenes/data.py 算出，带断言）。图片放 assets/，在场景里写 src="img/xxx.png"。
视频片段：<video id=… src="img/footage/x.mp4" data-start="{{t:l02}}" data-duration="{{d:l02>l03:1|6}}" data-track-index="1" muted>，
句号时刻在搭工程时换成秒数（HyperFrames 只认写死在 HTML 里的时刻）。
设计规范：edu_videos/_shared/design/design_system.md 与 tokens.json；字体 MiSans（免费商用，片尾 / 简介注明）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
import edu_video as ev  # noqa: E402

DESIGN = REPO / "edu_videos" / "_shared" / "design"
WEB = DESIGN / "web"
NODE = REPO / ".cache" / "node" / "hyperframes" / "node_modules"
HF = NODE / ".bin" / ("hyperframes.cmd" if os.name == "nt" else "hyperframes")
FONTS = REPO / ".cache" / "fonts"
LIBS = {"gsap.min.js": NODE / "gsap" / "dist" / "gsap.min.js", "d3.min.js": NODE / "d3" / "dist" / "d3.min.js"}


def tokens() -> dict:
    return json.loads((DESIGN / "tokens.json").read_text(encoding="utf-8"))


def cmd_tokens() -> Path:
    T = tokens()
    c, f, l = T["color"], T["font"], T["layout"]
    v = {"bg": c["bg"], "surface": c["surface"], "surface2": c["surface2"], "hair": c["hair"], "ink": c["ink"], "ink2": c["ink2"],
         "sub": c["sub"], "faint": c["faint"], "accent": c["accent"], "accent-text": c["accent_text"], "accent-soft": c["accent_soft"],
         "grad-from": c["grad_from"], "grad-to": c["grad_to"],
         **{f"d-{k}": x for k, x in c["data"].items()},
         **{f"fs-{k}": f"{x}px" for k, x in f["scale"].items()}, **{f"fw-{k}": str(x) for k, x in f["weight"].items()},
         **{f"tr-{k}": x for k, x in f["tracking"].items()},
         "mx": f"{l['margin_x']}px", "mt": f"{l['margin_top']}px", "band": f"{l['subtitle_band']}px", "radius": f"{l['radius']}px",
         "shadow": l["shadow"], "ease-out": T["motion"]["ease_out"], "ease-in": T["motion"]["ease_in"]}
    css = "/* 由 tools/edu_web.py tokens 从 tokens.json 生成，勿手改 */\n:root {\n" + "".join(f"  --{k}: {x};\n" for k, x in v.items()) + "}\n"
    out = WEB / "tokens.css"
    out.write_text(css, encoding="utf-8")
    return out


def split_fragment(src: str) -> tuple[str, str, str]:
    styles = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", src, re.S))
    scripts = "\n".join(re.findall(r"<script[^>]*>(.*?)</script>", src, re.S))
    markup = re.sub(r"<style[^>]*>.*?</style>|<script[^>]*>.*?</script>", "", src, flags=re.S)
    return styles, markup, scripts


def scene_info(topic: ev.Topic, sid: str) -> dict:
    tl = json.loads(topic.timeline_path.read_text(encoding="utf-8"))
    seg = tl["segments"][sid]
    data_p = topic.dir / "scenes" / "data.json"
    return {"id": sid, "lang": topic.lang, "duration": seg["duration"], "cues": seg["lines"],
            "data": json.loads(data_p.read_text(encoding="utf-8")) if data_p.exists() else {}}


CUE_TOKEN = re.compile(r"\{\{(t|d):([^}]+)\}\}")


def cue_tokens(markup: str, cues: dict) -> str:
    """把标签属性里的句号时刻换成秒数（HyperFrames 只认 HTML 里写死的 data-start / data-duration，脚本改的不生效）：
    {{t:l02:0.3}} = l02 开口到收口 30% 处的秒数；{{d:l01:0.2>l02:0.6|6}} = 两个时刻之差，| 后是上限（如素材只有 6 秒）。
    用于 <video data-start=… data-duration=…>，动画仍按句触发、不写死秒数。"""
    def at(spec: str) -> float:
        cue, _, frac = spec.strip().partition(":")
        a, b = cues[cue]
        return a + (b - a) * float(frac or 0)

    def rep(m: re.Match) -> str:
        if m.group(1) == "t":
            return f"{at(m.group(2)):.3f}"
        span, _, cap = m.group(2).partition("|")
        a, b = span.split(">")
        v = at(b) - at(a)
        return f"{max(min(v, float(cap)) if cap else v, 0.1):.3f}"
    return CUE_TOKEN.sub(rep, markup)


def build(topic: ev.Topic, sid: str, proj: Path) -> Path:
    """搭一个 HyperFrames 工程：index.html + assets（字体、库、样式、图片）。"""
    src = topic.dir / "scenes" / "web" / f"{sid}.html"
    if not src.exists():
        raise SystemExit(f"缺场景 {src.relative_to(REPO)}")
    cmd_tokens()
    shutil.rmtree(proj, ignore_errors=True)
    (proj / "assets" / "fonts").mkdir(parents=True)
    for k, f in tokens()["font"]["files"].items():
        shutil.copy2(FONTS / f, proj / "assets" / "fonts" / Path(f).name)
    for n, f in LIBS.items():
        shutil.copy2(f, proj / "assets" / n)
    for n in ("tokens.css", "base.css", "runtime.js"):
        shutil.copy2(WEB / n, proj / "assets" / n)
    img = topic.dir / "assets"
    if img.exists():
        shutil.copytree(img, proj / "img", ignore=shutil.ignore_patterns("*.txt", "*.log", "*.md", "*.json"))
    info = scene_info(topic, sid)
    styles, markup, scripts = split_fragment(src.read_text(encoding="utf-8"))
    markup = cue_tokens(markup, info["cues"])
    lib_p = topic.dir / "scenes" / "web" / "_lib.js"          # 本期各场景共用的图表构件
    lib = lib_p.read_text(encoding="utf-8") if lib_p.exists() else ""
    d = info["duration"]
    html = f"""<!doctype html>
<html lang="{topic.lang}"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920, height=1080">
<link rel="stylesheet" href="assets/tokens.css"><link rel="stylesheet" href="assets/base.css">
<script src="assets/gsap.min.js"></script><script src="assets/d3.min.js"></script>
<script>window.SCENE = {json.dumps(info, ensure_ascii=False)};</script><script src="assets/runtime.js"></script>
<style>{styles}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{d}" data-width="1920" data-height="1080">
<div id="stage" class="clip stage" data-start="0" data-duration="{d}" data-track-index="0">
{markup}
</div></div>
<script>EDU.i18n();</script>
<script>{lib}</script>
<script>{scripts}</script>
<script>EDU.done();</script>
</body></html>"""
    (proj / "index.html").write_text(html, encoding="utf-8")
    return proj / "index.html"


def proj_dir(topic: ev.Topic, sid: str) -> Path:
    return topic.render_dir / "_web" / sid


def cmd_render(topic: ev.Topic, sids: list[str]) -> None:
    tl = json.loads(topic.timeline_path.read_text(encoding="utf-8"))
    web = topic.dir / "scenes" / "web"
    sids = sids or [s for s, seg in tl["segments"].items() if "card" not in seg and (web / f"{s}.html").exists()]
    env = os.environ | {"HYPERFRAMES_NO_TELEMETRY": "1", "DO_NOT_TRACK": "1", "HYPERFRAMES_NO_UPDATE_CHECK": "1"}
    topic.render_dir.mkdir(parents=True, exist_ok=True)
    for sid in sids:
        proj = proj_dir(topic, sid)
        build(topic, sid, proj)
        out = topic.render_dir / f"{sid}.mp4"
        r = subprocess.run([str(HF), "render", ".", "-o", str(out), "--fps", str(ev.FPS), "--quality", "delivery", "--quiet"],
                           cwd=proj, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0 or not out.exists():
            raise SystemExit(f"渲染失败 {sid}：\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
        print(f"{topic.lang}/{sid}.mp4", flush=True)


CHECK_JS = """([band, mx, minPx]) => {
  const out = [], vis = [];
  const W = 1920, H = 1080;
  const leafs = [...document.querySelectorAll('#stage *')].filter(e => [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()));
  for (const e of leafs) {
    let op = 1, x = e;
    while (x && x.id !== 'root') { op *= parseFloat(getComputedStyle(x).opacity || 1); x = x.parentElement; }
    if (op < 0.15) continue;
    const rg = document.createRange(); rg.selectNodeContents(e);
    const r = rg.getBoundingClientRect();          // 量文字本身的范围，不量整块元素（居中的整行块会误报出界）
    if (r.width < 1 || r.height < 1) continue;
    const name = e.textContent.trim().slice(0, 24);
    const fs = parseFloat(getComputedStyle(e).fontSize);
    if (fs < minPx) out.push(`「${name}」字号 ${fs}px 小于 ${minPx}`);
    if (r.left < mx / 2 || r.right > W - mx / 2) out.push(`「${name}」出左右安全边`);
    if (r.top < 30) out.push(`「${name}」出上沿`);
    if (r.bottom > H - band) out.push(`「${name}」压字幕带`);
    vis.push([name, r, e]);
  }
  for (let i = 0; i < vis.length; i++) for (let j = i + 1; j < vis.length; j++) {
    const [a, ra, ea] = vis[i], [b, rb, eb] = vis[j];
    if (ea.contains(eb) || eb.contains(ea)) continue;
    // 字形比行框矮：上下各收 18% 字号再比，避免大字行高造成的误报
    const ia = parseFloat(getComputedStyle(ea).fontSize) * .18, ib = parseFloat(getComputedStyle(eb).fontSize) * .18;
    const ox = Math.min(ra.right, rb.right) - Math.max(ra.left, rb.left);
    const oy = Math.min(ra.bottom - ia, rb.bottom - ib) - Math.max(ra.top + ia, rb.top + ib);
    if (ox > 4 && oy > 4) out.push(`「${a}」与「${b}」重叠`);
  }
  return out;
}"""


def shots(topic: ev.Topic, sid: str, times: list[tuple[str, float]], out_dir: Path, check: bool = False) -> list[str]:
    """在给定时刻截图；check=True 时同时跑版式自检。"""
    from playwright.sync_api import sync_playwright
    proj = proj_dir(topic, sid)
    index = build(topic, sid, proj)
    T = tokens()
    out_dir.mkdir(parents=True, exist_ok=True)
    problems: list[str] = []
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 1920, "height": 1080})
        pg.goto(index.as_uri())
        pg.wait_for_function("() => !!(window.__timelines && window.__timelines.main)", polling=100, timeout=60000)
        pg.evaluate("async () => { await document.fonts.ready; }")
        for label, t in times:
            pg.evaluate(f"() => {{ window.__timelines.main.seek({t:.3f}, false); }}")     # 不把时间线对象传回 Python（序列化会让页面崩）
            pg.wait_for_timeout(80)
            pg.screenshot(path=str(out_dir / f"{sid}_{label}.png"))
            if check:
                for msg in pg.evaluate(CHECK_JS, [T["layout"]["subtitle_band"], T["layout"]["margin_x"], T["font"]["min_px"]]):
                    line = f"[layout] {sid} {label} t={t:.1f}s {msg}"
                    if line not in problems:
                        problems.append(line)
        b.close()
    return problems


TEXT_JS = """() => {
  // 屏幕上看得见的文字块：带 data-zh / data-en 的元素算一块；不在这类元素里的带字叶子（如数字）另算一块
  const op = e => { let o = 1; for (let x = e; x && x.id !== 'root'; x = x.parentElement) o *= parseFloat(getComputedStyle(x).opacity || 1); return o; };
  const blocks = [];
  const keyed = [...document.querySelectorAll('#stage [data-zh], #stage [data-en]')];
  const loose = [...document.querySelectorAll('#stage *')].filter(e => !e.closest('[data-zh],[data-en]') &&
      [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && !e.closest('svg'));
  for (const e of [...keyed, ...loose]) {
    if (op(e) < 0.3) continue;
    const r = e.getBoundingClientRect(); if (r.width < 1 || r.height < 1) continue;
    // 只算看得见的字：子元素自己透明（如还没淡入的标签）不算（台词审 lines5_r3 I44）
    let text = '';
    const tw = document.createTreeWalker(e, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT);
    for (let n = tw.nextNode(); n; n = tw.nextNode()) {
      if (n.nodeType === 1) { if (n.tagName === 'BR') text += ' / '; continue; }
      if (op(n.parentElement) >= 0.3) text += n.textContent;
    }
    text = text.replace(/\\s+/g, ' ').trim(); if (!text) continue;
    const cn = (e.className && e.className.baseVal === undefined ? e.className : '').split(' ');
    const cls = cn.includes('eyebrow') ? 'eyebrow' : cn.includes('chart') ? 'chart' : cn.filter(c => /^(eyebrow|chart|display|h1|h2|body|caption|micro|quote|tab|n|u)$/.test(c))[0] || e.tagName.toLowerCase();
    blocks.push({ text, cls, px: Math.round(parseFloat(getComputedStyle(e).fontSize)), y: Math.round(r.top), x: Math.round(r.left) });
  }
  // 图表里的文字（坐标轴、标签）
  for (const t of document.querySelectorAll('#stage svg text')) {
    if (op(t) < 0.3 || !t.textContent.trim()) continue;
    const r = t.getBoundingClientRect();
    blocks.push({ text: t.textContent.trim(), cls: 'chart', px: Math.round(parseFloat(getComputedStyle(t).fontSize)), y: Math.round(r.top), x: Math.round(r.left) });
  }
  blocks.sort((a, b) => a.y - b.y || a.x - b.x);
  return blocks;
}"""


def screen_dump(topic: ev.Topic, out_dir: Path) -> dict:
    """每句说完前 0.15 秒：屏幕上看得见的文字块（层级、字号）＋截图。给屏幕文字审稿用。"""
    from playwright.sync_api import sync_playwright
    tl = json.loads(topic.timeline_path.read_text(encoding="utf-8"))
    web = topic.dir / "scenes" / "web"
    out_dir.mkdir(parents=True, exist_ok=True)
    res: dict = {}
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 1920, "height": 1080})
        for sid, seg in tl["segments"].items():
            if "card" in seg or not (web / f"{sid}.html").exists():
                continue
            index = build(topic, sid, proj_dir(topic, sid))
            pg.goto(index.as_uri())
            pg.wait_for_function("() => !!(window.__timelines && window.__timelines.main)", polling=100, timeout=60000)
            pg.evaluate("async () => { await document.fonts.ready; }")
            for lid, (_, t1) in seg["lines"].items():
                pg.evaluate(f"() => {{ window.__timelines.main.seek({t1 - 0.15:.3f}, false); }}")
                pg.wait_for_timeout(80)
                shot = out_dir / f"{sid}_{lid}.png"
                pg.screenshot(path=str(shot))
                res[lid] = {"scene": sid, "blocks": pg.evaluate(TEXT_JS), "shot": shot.relative_to(ev.REPO).as_posix()}
        b.close()
    return res


def parse_at(info: dict, spec: str) -> list[tuple[str, float]]:
    out = []
    for part in spec.split(","):
        cue, _, frac = part.partition(":")
        if re.fullmatch(r"\d+(\.\d+)?", cue):
            out.append((f"t{cue}", float(cue)))
        else:
            a, b = info["cues"][cue]
            f = float(frac or 1)
            out.append((f"{cue}_{int(f * 100)}", a + (b - a) * f - (0.15 if f >= 1 else 0)))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("tokens")
    p = sub.add_parser("render"); p.add_argument("topic", type=Path); p.add_argument("sids", nargs="*")
    p.add_argument("--lang", choices=ev.LANGS, default="zh")
    p = sub.add_parser("still"); p.add_argument("topic", type=Path); p.add_argument("sid"); p.add_argument("--at", required=True)
    p.add_argument("--lang", choices=ev.LANGS, default="zh"); p.add_argument("--out", type=Path)
    p = sub.add_parser("check"); p.add_argument("topic", type=Path); p.add_argument("--lang", choices=ev.LANGS, default="zh")
    a = ap.parse_args()
    if a.cmd == "tokens":
        print(cmd_tokens()); return
    topic = ev.Topic(a.topic, a.lang)
    if a.cmd == "render":
        cmd_render(topic, a.sids)
    elif a.cmd == "still":
        info = scene_info(topic, a.sid)
        out = a.out or (topic.render_dir / "stills")
        probs = shots(topic, a.sid, parse_at(info, a.at), out, check=True)
        print("\n".join(probs) or "版式自检：无问题", f"\n截图 → {out}")
    else:
        tl = json.loads(topic.timeline_path.read_text(encoding="utf-8"))
        web = topic.dir / "scenes" / "web"
        log = []
        for sid, seg in tl["segments"].items():
            if "card" in seg or not (web / f"{sid}.html").exists():
                continue
            times = [(lid, b - 0.15) for lid, (_, b) in seg["lines"].items()]
            log += shots(topic, sid, times, topic.render_dir / "web_check", check=True)
        (topic.render_dir / "web_check.log").write_text("\n".join(log) + "\n", encoding="utf-8")
        print("\n".join(log) or "版式自检：无问题")


if __name__ == "__main__":
    main()
