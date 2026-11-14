# -*- coding: utf-8 -*-
"""教学视频统一包装：片头、本期内容、章节转场、片尾（中英文）。模板 edu_videos/_shared/package/template.html，HyperFrames 渲染。

    python tools/edu_package.py render <知识点目录> --lang zh|en [--cards 卡 ...]   卡：intro agenda chapter:<id> outro（缺省全部）
    python tools/edu_package.py reel <知识点目录>                         全部卡按默认时长渲一遍并拼成样片 → renders/package/reel_{zh,en}.mp4

文字来源：系列 `_shared/package.json`（系列名、栏目标签、章节轨）+ 知识点 `package.json`（本期标题、内容、先修、章节名、一句话、下一期）。
本期内容与片尾的出场时间默认均匀铺开；接入讲稿时间轴后由配音句子触发（--cues 传秒数列表）。
产物：<知识点>/renders/package/{lang}/{卡}.mp4（1920×1080，30 fps，无声）。HyperFrames 遥测已关，不用 publish。
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TEMPLATE = REPO / "edu_videos" / "_shared" / "package" / "template.html"
NODE = REPO / ".cache" / "node" / "hyperframes" / "node_modules"
HF = NODE / ".bin" / ("hyperframes.cmd" if os.name == "nt" else "hyperframes")
FONT_DIR = REPO / ".cache" / "fonts" / "misans"
ASSETS = {"gsap.min.js": NODE / "gsap" / "dist" / "gsap.min.js",
          "tokens.css": REPO / "edu_videos" / "_shared" / "design" / "web" / "tokens.css",
          **{f"fonts/MiSans-{w}.ttf": FONT_DIR / f"MiSans-{w}.ttf" for w in ("Regular", "Medium", "Semibold", "Bold")}}
LANGS = ("zh", "en")
FPS = 30


def load(topic: Path) -> tuple[dict, dict]:
    series = topic.parent / "_shared" / "package.json"
    ep = topic / "package.json"
    for p in (series, ep):
        if not p.exists():
            raise SystemExit(f"缺 {p.relative_to(REPO)}")
    return json.loads(series.read_text(encoding="utf-8")), json.loads(ep.read_text(encoding="utf-8"))


def card_ids(S: dict) -> list[str]:
    return ["intro", "agenda", *[f"chapter:{c['id']}" for c in S["chapters"]], "outro"]


def spread(n: int, dur: float, start: float = 0.3, end_pad: float = 2.2) -> list[float]:
    step = (dur - start - end_pad) / max(n - 1, 1)
    return [round(start + i * step, 2) for i in range(n)]


def fit_cues(cues: list[float] | None, n: int, dur: float, end_pad: float) -> list[float]:
    """卡上 n 项的出场时间：给的不够就把剩下的项均匀铺到卡尾前，多了截掉。"""
    if not cues:
        return spread(n, dur, end_pad=end_pad)
    cues = list(cues[:n])
    if len(cues) < n:
        last, room = cues[-1], max(dur - end_pad - cues[-1], 0.6)
        k = n - len(cues)
        cues += [round(last + room * (i + 1) / k, 2) for i in range(k)]
    return cues


def card_data(S: dict, E: dict, lang: str, card: str, duration: float | None, cues: list[float] | None) -> dict:
    other = "en" if lang == "zh" else "zh"
    base = {"lang": lang, "series": {"main": S["series"][lang], "sub": S["series"][other]}}
    bi = S.get("bilingual_cards", True)     # 卡上是否附另一种语言的小字（AI 高频词 2026-11-08 起关：屏幕只放本语言）
    if not bi:
        base["series"]["sub"] = ""
    if card == "intro":
        d = duration or S["durations"]["intro"]
        return base | {"card": card, "duration": d, "eyebrow": S["eyebrow"][lang].format(ep=E["episode"], season=E.get("season", 1)),
                       "title": {"main": E["title"][lang], "sub": E["title"][other] if bi else ""}}
    if card == "agenda":
        d = duration or 9.5
        if E["agenda"] == "chapters":     # 目录就是章节卡标题，编号与章节卡一致（用户 2026-11-08：目录、章节卡、页眉一个叫法）
            # 与章节卡同一编号：按本期实际用到的章节（系列顺序）连续编 01、02…（t12 / t13 报 4 章编成 01/03/04/05，2026-11-10）
            ids = [c["id"] for c in S["chapters"] if c["id"] in E["chapters"]]
            rows = [{"tag": f"{i + 1:02d}", "text": E["chapters"][cid][lang]} for i, cid in enumerate(ids)]
        else:
            rows = [{"tag": r["tag"][lang], "text": r["text"][lang]} for r in E["agenda"]]
        pre = [{"text": r["text"][lang], "note": r.get("note", {}).get(lang, "")} for r in E.get("prereq", [])]
        # 没有先修卡时：标题跟第一句出，各行在口播里均匀铺开（口播用自然的话串，不逐行念目录）
        cue = fit_cues((cues or [0.4])[:1], len(rows) + 1 + bool(pre), d, 2.2)
        return base | {"card": card, "duration": d, "cues": cue,
                       "agenda_title": S["agenda_title"][lang], "prereq_title": S["prereq_title"][lang],
                       "prereq_hint": E.get("prereq_hint", S["prereq_hint"])[lang],   # 每期可覆盖（如第零期无前置）
                       "agenda": rows, "prereq": pre}
    if card.startswith("chapter:"):
        cid = card.split(":", 1)[1]
        # 编号与章节轨按本期实际用到的章节（系列顺序）：t01 v5 只用 5 章，就编 01–05（用户 2026-11-09 缩短）
        ids = [c["id"] for c in S["chapters"] if c["id"] in (E.get("chapters") or {})] or [c["id"] for c in S["chapters"]]
        if cid not in ids:
            raise SystemExit(f"系列章节里没有 {cid}（有 {', '.join(ids)}）")
        i = ids.index(cid)
        head = E["chapters"][cid]
        return base | {"card": "chapter", "duration": duration or S["durations"]["chapter"], "num": f"{i + 1:02d}",
                       "heading": head[lang], "heading_sub": head[other] if bi else "", "active": i,
                       "rail": [c["rail"][lang] if S.get("rail_labels", True) else "" for c in S["chapters"] if c["id"] in ids]}
    if card == "outro":
        d = duration or 7.5
        return base | {"card": card, "duration": d, "cues": fit_cues(cues, len(E["quote"][lang]) + 2, d, 3.0),
                       "eyebrow": E.get("outro_eyebrow", S["outro_eyebrow"])[lang], "quote": E["quote"][lang], "ai_note": S["ai_note"][lang],
                       "next": {"label": S["next_label"][lang], "name": E["next"][lang][0], "sub": E["next"][lang][1] if bi else ""}}
    raise SystemExit(f"未知卡：{card}")


def render(topic: Path, lang: str, card: str, duration: float | None = None, cues: list[float] | None = None,
           name: str | None = None) -> Path:
    """渲一张卡 → renders/package/{lang}/{name}.mp4（name 缺省按卡名；edu_video.py package 传时间轴段号）。"""
    S, E = load(topic)
    data = card_data(S, E, lang, card, duration, cues)
    name = name or card.replace(":", "_")
    proj = topic / "renders" / "package" / lang / f"_{name}"
    shutil.rmtree(proj, ignore_errors=True)
    (proj / "assets" / "fonts").mkdir(parents=True)
    for n, src in ASSETS.items():
        shutil.copy2(src, proj / "assets" / n)
    html = TEMPLATE.read_text(encoding="utf-8")
    dur = f'data-duration="{data["duration"]}"'
    html = html.replace('data-duration="4"', dur).replace(
        "/*__PKG__*/", "window.PKG = " + json.dumps(data, ensure_ascii=False) + ";")
    (proj / "index.html").write_text(html, encoding="utf-8")
    out = topic / "renders" / "package" / lang / f"{name}.mp4"
    env = os.environ | {"HYPERFRAMES_NO_TELEMETRY": "1", "DO_NOT_TRACK": "1", "HYPERFRAMES_NO_UPDATE_CHECK": "1"}
    r = subprocess.run([str(HF), "render", ".", "-o", str(out), "--fps", str(FPS), "--quality", "delivery", "--quiet"],
                       cwd=proj, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0 or not out.exists():
        raise SystemExit(f"渲染失败 {lang}/{card}：\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
    shutil.rmtree(proj, ignore_errors=True)
    print(f"{lang}/{name}.mp4  {data['duration']}s", flush=True)
    return out


def reel(topic: Path) -> None:
    S, _ = load(topic)
    for lang in LANGS:
        parts = [render(topic, lang, c) for c in card_ids(S)]
        lst = topic / "renders" / "package" / lang / "concat.txt"
        lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
        out = topic / "renders" / "package" / f"reel_{lang}.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                        "-c", "copy", str(out)], check=True)
        print("样片", out.relative_to(REPO).as_posix())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("render"); p.add_argument("topic", type=Path); p.add_argument("--cards", nargs="+")
    p.add_argument("--lang", choices=LANGS, required=True); p.add_argument("--duration", type=float)
    p.add_argument("--cues", type=lambda s: [float(x) for x in s.split(",")])
    sub.add_parser("reel").add_argument("topic", type=Path)
    a = ap.parse_args()
    topic = a.topic.resolve()
    if a.cmd == "reel":
        reel(topic)
    else:
        S, _ = load(topic)
        for c in a.cards or card_ids(S):
            render(topic, a.lang, c, a.duration, a.cues)


if __name__ == "__main__":
    sys.exit(main())
