# -*- coding: utf-8 -*-
"""生成人物审阅页的数据 review.json（ai_video_management follow-up 329，/character-review?path=<人物目录>）。

    python tools/character_review.py ai_videos/<剧>/2_世界观人设/characters/<人物目录>

按约定位置收集：建立视频（V）、声样（A）、三视图（T）、表情（E，按 expressions/_index.json 的顺序与中文名）、
换装阶段三视图（O）。每项一个稳定编号，用户按编号说哪一项要修。已有 review.json 里同编号、同文件的
status / note 会保留（审阅结论不因重跑丢失）；文件换了（sha 变了）则状态清回「待审」。只读文件、只写 review.json。
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def rel(p: Path) -> str:
    return p.resolve().relative_to(REPO).as_posix()


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:12]


def build(d: Path) -> dict:
    name = d.name
    old = {}
    if (d / "review.json").is_file():
        for s in json.loads((d / "review.json").read_text(encoding="utf-8")).get("sections", []):
            for it in s.get("items", []):
                old[it["id"]] = it
    sections = []

    def item(i: str, label: str, p: Path, desc: str = "") -> dict:
        x = {"id": i, "label": label, "path": rel(p), "sha": sha(p)}
        if desc:
            x["desc"] = desc
        o = old.get(i)
        if o and o.get("path") == x["path"] and o.get("sha") == x["sha"]:
            for k in ("status", "note"):
                if o.get(k):
                    x[k] = o[k]
        return x

    vids = sorted(p for p in d.glob("*turntable*.mp4"))
    sections.append({"id": "V", "title": "建立视频", "layout": "wide",
                     "hint": "看：同一张脸、嘴型和台词对得上、声音、转身时侧面与背面、全程没有文字和配乐。",
                     "items": [item(f"V{n}", p.stem, p) for n, p in enumerate(vids, 1)]})
    audio = d / "views" / f"{name}_audio.mp3"
    sections.append({"id": "A", "title": "声样", "hint": "每个说话镜头都挂这一份，听口音、音色是否对。",
                     "items": [item("A1", "声样", audio)] if audio.is_file() else []})
    views = [(f"T{n}", lab, d / "views" / f"{name}_{k}.png") for n, (k, lab) in enumerate((("front", "正面"), ("side", "侧面"), ("back", "背面")), 1)]
    sections.append({"id": "T", "title": "三视图", "hint": "所有镜头参考脸与体型的标准。",
                     "items": [item(i, lab, p) for i, lab, p in views if p.is_file()]})
    idx = d / "expressions" / "_index.json"
    exprs = []
    if idx.is_file():
        for e in json.loads(idx.read_text(encoding="utf-8")):
            p = REPO / e["path"]
            if p.is_file():
                exprs.append(item(e["id"], e["label"], p, e.get("desc", "")))
    sections.append({"id": "E", "title": "表情", "hint": "像电影演员的表演：真实、克制、好看。", "items": exprs})
    outfits = []
    for n, od in enumerate(sorted(x for x in d.iterdir() if x.is_dir() and x.name.startswith(name.split("_")[0] + "-")), 1):
        sheet = next(iter(sorted(od.glob("*_views.png"))), None)
        if sheet:
            outfits.append(item(f"O{n}", od.name, sheet))
    if outfits:
        sections.append({"id": "O", "title": "换装阶段", "hint": "旧脸画的换装要随新脸重做时，在这里标。", "items": outfits})
    card = next(iter(sorted(d.glob(f"{name}.md"))), None)
    title = name
    if card:
        first = card.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        title = first or name
    return {"title": f"{title} · 人物审阅", "character": name, "updated": time.strftime("%Y-%m-%d %H:%M"), "sections": sections}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    d = (REPO / sys.argv[1]).resolve() if not Path(sys.argv[1]).is_absolute() else Path(sys.argv[1])
    data = build(d)
    (d / "review.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    n = sum(len(s["items"]) for s in data["sections"])
    print(f"{rel(d / 'review.json')}：{n} 项（" + "、".join(f"{s['title']} {len(s['items'])}" for s in data["sections"]) + "）")
    print(f"审阅页：/character-review?path={rel(d)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
