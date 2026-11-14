# -*- coding: utf-8 -*-
"""逐张看过候选拼图后的人工选择 → assets/img + assets.json + data.json 图片字段（替代 image_reselect apply，支持 image_alt）。

SEL[name] = (主图候选 id, 默认版替代图候选 id 或 None, 焦点 [x, y] 或 None)
- 主图 = 画面最好的一张（许可不明也可以，只进 _with-risk-images 版）；
- 有 image_risk（FoP 或许可不明）时，默认版用 alt（必须可商用许可）；alt 与主图相同 id 时直接引用主图文件。
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
EP = HERE.parent
sys.path.insert(0, str(EP.parents[3] / "projects" / "rank_scroll"))
from rank_scroll.contract import _licence_ok  # noqa: E402

TODAY = date.today().isoformat()
LONG = 2400

SEL: dict[str, tuple] = json.loads((HERE / "selection.json").read_text(encoding="utf-8"))


def licence_url(lic: str) -> str:
    low = lic.lower()
    if "pexels" in low: return "https://www.pexels.com/license/"
    if "unsplash" in low: return "https://unsplash.com/license"
    if "pixabay" in low: return "https://pixabay.com/service/license-summary/"
    if "cc0" in low: return "https://creativecommons.org/publicdomain/zero/1.0/"
    if "public domain mark" in low: return "https://creativecommons.org/publicdomain/mark/1.0/"
    m = re.search(r"cc[ -]by(-sa)?\s*([\d.]+)?", low)
    if m:
        return f"https://creativecommons.org/licenses/{'by-sa' if m.group(1) else 'by'}/{m.group(2) or '4.0'}/"
    return ""


def put(cand_dir: Path, m: dict, rel: str, fop_note: str) -> dict:
    dst = EP / rel
    with Image.open(cand_dir / m["file"]) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        if max(im.size) > LONG:
            im.thumbnail((LONG, LONG), Image.LANCZOS)
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, quality=90)
        size = im.size
    lic = m["licence"].strip()
    return {"file": rel, "source_page": m.get("page_url", ""), "source_url": m.get("image_url", ""),
            "author": m.get("author", "") or "Unknown", "licence": lic, "licence_url": licence_url(lic),
            "attribution_required": not re.match(r"(public domain|pd|cc0|pexels|unsplash|pixabay|ai-generated)", lic, re.I),
            "modified": f"downscaled to {size[0]}x{size[1]} px and re-encoded as JPEG; renderer will crop",
            "sha256": hashlib.sha256(dst.read_bytes()).hexdigest(), "retrieved_at": TODAY, "fop_note": fop_note,
            "selected_by": f"follow-up 016/023 人工看图挑选（候选来源 {m.get('source', '')}）"}


GEN_LIC = "AI-generated (Codex image_gen)"


def gen_meta(spec: str) -> tuple[Path, dict]:
    """selection 里写 'gen:<相对期目录的 png 路径>' 表示 Codex 生成图（追加要求 4 / 主代理 11-04 决定）。"""
    src = EP / spec[4:]
    return src.parent, {"file": src.name, "licence": GEN_LIC, "author": "AI-generated", "page_url": "",
                        "image_url": "tools/codex_image.py (Codex built-in image_gen); prompt in _build/gen/", "source": "Codex image_gen"}


def main() -> None:
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    assets = []
    for it in data["items"]:
        stem = Path(it["image"]).stem
        sel = SEL.get(it["name"])
        for k in ("image_credit", "image_alt", "image_alt_credit", "image_focus", "image_note"):
            it.pop(k, None)
        fop = [r for r in str(it.get("image_risk") or "").split("; ") if r.startswith("FoP:")]
        it.pop("image_risk", None)
        if not sel or not sel[0]:
            it["image_note"] = "No licensed photo found yet"
            if fop:
                it["image_risk"] = "; ".join(fop)
            continue
        main_id, alt_id, focus = (list(sel) + [None, None])[:3]
        d = HERE / "reselect" / "cand" / stem
        meta = {m["id"]: m for m in json.loads((d / "meta.json").read_text(encoding="utf-8"))}
        for m_ in meta.values():   # PublicDomainPictures.net 的「Free public domain image」= 公有领域发布（download 会重写 meta，这里统一归一）
            if m_["licence"].strip().lower().startswith("free public domain"):
                m_["licence"] = "Public domain (PublicDomainPictures.net, 'Free public domain image')"
        fop_note = fop[0] if fop else ""
        if str(main_id).startswith("gen:"):
            gd, m = gen_meta(main_id)
            a = put(gd, m, it["image"], fop_note)
        else:
            m = meta[main_id]
            a = put(d, m, it["image"], fop_note)
        assets.append(a)
        it["image_credit"] = "AI-generated image (Codex)" if a["licence"].startswith("AI-generated") else f"{a['author']} / {a['licence']}"
        risks = list(fop)
        if not _licence_ok(a["licence"]):
            risks.append("licence unknown")
        if risks:
            it["image_risk"] = "; ".join(risks)
            if alt_id and str(alt_id).startswith("gen:"):
                gd, am = gen_meta(alt_id)
                rel = f"assets/img/{stem}_alt.jpg"
                aa = put(gd, am, rel, fop_note)
                aa["attribution_required"] = False
                assets.append(aa)
                it["image_alt"], it["image_alt_credit"] = rel, "AI-generated image (Codex)"
            elif alt_id:
                am = meta[alt_id]
                if not _licence_ok(am["licence"]):
                    raise SystemExit(f"{it['name']}: alt {alt_id} licence not acceptable: {am['licence']}")
                if alt_id == main_id:
                    it["image_alt"], it["image_alt_credit"] = it["image"], it["image_credit"]
                else:
                    rel = f"assets/img/{stem}_alt.jpg"
                    aa = put(d, am, rel, fop_note)
                    assets.append(aa)
                    it["image_alt"], it["image_alt_credit"] = rel, f"{aa['author']} / {aa['licence']}"
            else:
                it["image_note"] = ("Photo withheld: licence unclear" if not _licence_ok(a["licence"])
                                    else "Photo withheld: sculpture copyright")   # 写真实原因（qc #10）
        if focus:
            it["image_focus"] = focus
    (EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (EP / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    n_img = sum(1 for it in data["items"] if it.get("image_credit"))
    n_alt = sum(1 for it in data["items"] if it.get("image_alt"))
    n_def = sum(1 for it in data["items"] if it.get("image_credit") and (not it.get("image_risk") or it.get("image_alt")))
    print(f"主图 {n_img}/{len(data['items'])}；默认版有图 {n_def}；image_alt {n_alt}；assets {len(assets)}")


if __name__ == "__main__":
    main()
