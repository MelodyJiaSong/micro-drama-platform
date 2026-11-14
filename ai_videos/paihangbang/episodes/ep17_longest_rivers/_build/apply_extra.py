# -*- coding: utf-8 -*-
"""主图 apply 之后的补充：默认版替代图 image_alt（契约 v1.4）与 AI 生成图。
python apply_extra.py alt  idx=cid|gen:<png> ...   → assets/img/NN_<key>_alt.jpg + image_alt / image_alt_credit
python apply_extra.py main idx=gen:<png> ...        → 用生成图作主图（不标 image_risk）
"""
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

from PIL import Image, ImageOps

sys.path.insert(0, str(Path(__file__).parent))
from image_reselect_ep17 import licence_url  # noqa: E402

EP = Path(__file__).resolve().parents[1]
C = EP / "_build" / "reselect" / "cand"
GEN_LIC = "AI-generated (Codex image_gen)"


def save(src: Path, dst: Path) -> tuple[int, int]:
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        if max(im.size) > 2400:
            im.thumbnail((2400, 2400), Image.LANCZOS)
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, quality=90)
        return im.size


def meta_for(i: int, it: dict, spec: str) -> tuple[Path, dict]:
    if spec.startswith("gen:"):
        p = Path(spec[4:])
        prompt = (EP / "_build" / "gen" / (p.stem.replace("_gen", "") + ".txt"))
        return p, {"author": "AI-generated", "licence": GEN_LIC, "page_url": "", "image_url": "",
                   "source": "Codex image_gen", "note": f"prompt: _build/gen/{prompt.name}; see ai_videos/paihangbang/request_log.md"}
    key = f"{i:02d}_{Path(it['image']).stem}"
    m = next(x for x in json.loads((C / key / "meta.json").read_text(encoding="utf-8")) if x["id"] == spec)
    return C / key / m["file"], m


def entry(rel: str, dst: Path, size, m: dict) -> dict:
    lic = m["licence"].strip()
    gen = lic == GEN_LIC
    return {"file": rel, "source_page": m.get("page_url", ""), "source_url": m.get("image_url", ""), "author": m.get("author", ""),
            "licence": lic, "licence_url": "" if gen else licence_url(lic),
            "attribution_required": not gen and not re.match(r"(public domain|pd|cc0|pexels|unsplash|pixabay)", lic, re.I),
            "modified": (f"generated image, downscaled to {size[0]}x{size[1]} px JPEG; renderer will crop" if gen else
                         f"downscaled to {size[0]}x{size[1]} px and re-encoded as JPEG; renderer will crop"),
            "sha256": hashlib.sha256(dst.read_bytes()).hexdigest(), "retrieved_at": date.today().isoformat(), "fop_note": "",
            "selected_by": "ep17 Claude 选图（follow-up 016/023/025）" + (f"；{m['note']}" if m.get("note") else "")}


def main():
    mode, specs = sys.argv[1], dict(a.split("=", 1) for a in sys.argv[2:])
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    assets = json.loads((EP / "assets.json").read_text(encoding="utf-8"))
    by = {a["file"]: k for k, a in enumerate(assets)}
    for si, spec in specs.items():
        i = int(si)
        it = data["items"][i]
        src, m = meta_for(i, it, spec)
        stem = Path(it["image"]).stem
        rel = f"assets/img/{stem}_alt.jpg" if mode == "alt" else it["image"]
        dst = EP / rel
        size = save(src, dst)
        e = entry(rel, dst, size, m)
        if rel in by:
            assets[by[rel]] = e
        else:
            assets.append(e)
            by[rel] = len(assets) - 1
        credit = m["licence"] if m["licence"] == GEN_LIC else f"{m.get('author') or 'Unknown'} / {m['licence']}"
        if mode == "alt":
            it["image_alt"], it["image_alt_credit"] = rel, credit
        else:
            it["image_credit"] = credit
            for k in ("image_risk", "image_note", "image_alt", "image_alt_credit"):
                it.pop(k, None)
        print(i, it["name"], mode, rel, credit)
    (EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (EP / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
