# -*- coding: utf-8 -*-
"""配图闸门补图：把选定的替换图写进一期（paihangbang follow-up 058）。

    python ai_videos/paihangbang/_tools/regate_apply.py <ep_dir> <key>=<file> [<key>=<file> ...] [--focus <key>=x,y ...] [--contain <key> ...]

- 候选在 `<ep>/_build/regate/<key>/`（研究员写的 candidates.json + cand/，或 Codex 出图 cand/ai1.png）。
  `<file>` 相对该目录，如 `cand/c3.jpg`；写 `pick` 则取 candidates.json 里研究员的 pick。
- 图缩到长边 2400、转 JPEG 存 `assets/img/<key>_regate.jpg`，登记 assets.json（许可照 candidates.json，出图记 AI-generated）。
- 卡上有 image_risk（默认版用替代图）的写进 image_alt，否则替换 image；去掉旧 image_focus（可用 --focus 重设）。
- 改完跑 zh_edition.py merge 同步 data.zh.json。之后须 tile_gate.py sheet + 独立审图，过闸门才能重渲。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from image_reselect import licence_url  # noqa: E402

LONG_SIDE = 2400
AI_LICENCE = "AI-generated (Codex image_gen)"
AI_CREDIT = "Illustration: AI-generated, not a photo"
FREE_NO_ATTRIB = re.compile(r"(public domain|pd|cc0|pexels|unsplash|pixabay)", re.I)


def tile_key(i: int, it: dict) -> str:
    return f"{i:02d}_" + re.sub(r"[^a-z0-9]+", "_", it["name"].lower()).strip("_")


def apply(ep: Path, picks: dict[str, str], focus: dict[str, list[float]], contain: set[str]) -> None:
    data = json.loads((ep / "data.json").read_text(encoding="utf-8"))
    assets = json.loads((ep / "assets.json").read_text(encoding="utf-8"))
    by_key = {tile_key(i, it): it for i, it in enumerate(data["items"])}
    for key, choice in picks.items():
        if key not in by_key:
            sys.exit(f"没有这张卡：{key}")
        it, d = by_key[key], ep / "_build" / "regate" / key
        cj = d / "candidates.json"
        meta = json.loads(cj.read_text(encoding="utf-8")) if cj.is_file() else {"downloaded": []}
        if choice == "pick":
            choice = meta.get("pick") or sys.exit(f"{key}：candidates.json 没有 pick")
        src = d / choice
        if not src.is_file():
            sys.exit(f"{key}：找不到 {src}")
        ai = src.name.startswith("ai")
        c = next((x for x in meta["downloaded"] if x["file"].replace("\\", "/") == choice), None)
        if not ai and c is None:
            sys.exit(f"{key}：{choice} 不在 candidates.json 的 downloaded 里，许可无从登记")
        rel = f"assets/img/{key}_regate.jpg"
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            if max(im.size) > LONG_SIDE:
                im.thumbnail((LONG_SIDE, LONG_SIDE), Image.LANCZOS)
            im.save(ep / rel, quality=92)
            size = im.size
        lic = AI_LICENCE if ai else c["licence"].strip()
        entry = {"file": rel, "source_page": "" if ai else c.get("page_url", ""), "source_url": "" if ai else c.get("image_url", ""),
                 "author": "AI illustration" if ai else c.get("author", ""), "licence": lic,
                 "licence_url": "" if ai else licence_url(lic),
                 "attribution_required": not ai and not FREE_NO_ATTRIB.match(lic),
                 "modified": f"downscaled to {size[0]}x{size[1]} px and re-encoded as JPEG; renderer crops to the card",
                 "sha256": hashlib.sha256((ep / rel).read_bytes()).hexdigest(), "retrieved_at": date.today().isoformat(),
                 "fop_note": "", "subject_check": "" if ai else c.get("subject_check", ""),
                 "selected_by": "follow-up 058：配图闸门补图（Claude 研究员找图 / Codex 出图），待独立审图"}
        if ai:
            prompt = d / "gen_prompt.txt"
            entry["prompt"] = prompt.read_text(encoding="utf-8") if prompt.is_file() else ""
        assets = [a for a in assets if a["file"] != rel] + [entry]
        credit = AI_CREDIT if ai else f"{c.get('author') or 'Unknown'} / {lic}"
        if it.get("image_risk"):
            it["image_alt"], it["image_alt_credit"] = rel, credit
        else:
            it["image"], it["image_credit"] = rel, credit
        it.pop("image_focus", None)
        it.pop("image_fit", None)
        if key in contain:
            it["image_fit"] = "contain"   # 整图放入、同图虚化填空（follow-up 061）
        if key in focus:
            it["image_focus"] = focus[key]
        print(f"{key} ← {choice}（{lic}，{size[0]}x{size[1]}）{'→ image_alt' if it.get('image_risk') else '→ image'}")
    (ep / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ep / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if (ep / "data.zh.json").is_file():
        r = subprocess.run([sys.executable, str(HERE / "zh_edition.py"), "merge", str(ep)], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        print("中文版 merge：", (r.stdout or r.stderr).strip()[-300:])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("ep", type=Path)
    ap.add_argument("picks", nargs="+")
    ap.add_argument("--focus", nargs="*", default=[])
    ap.add_argument("--contain", nargs="*", default=[], help="这些卡用整图放入（image_fit=contain，follow-up 061）")
    a = ap.parse_args()
    picks = dict(p.split("=", 1) for p in a.picks)
    focus = {k: [float(x) for x in v.split(",")] for k, v in (f.split("=", 1) for f in a.focus)}
    apply(a.ep.resolve(), picks, focus, set(a.contain))


if __name__ == "__main__":
    main()
