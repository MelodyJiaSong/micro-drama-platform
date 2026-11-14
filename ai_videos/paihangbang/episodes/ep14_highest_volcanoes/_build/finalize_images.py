# -*- coding: utf-8 -*-
"""apply 之后的收尾（follow-up 016/023 + 追加要求 3/4）：
- Llullaillaco：ESO 全景（5180×1061）按峰顶裁成 9:10 原分辨率，不缩到 2400 长边。
- Purico：风险图（Andeshandbook Cerro Toco）配 ESO 全景裁切作 image_alt（可商用 CC BY 4.0）。
- 其余风险图项：image_alt = Codex 生成图（_gen.png）；AI-only 项：image = 生成图。
- 生成图记账本：licence "AI-generated (Codex image_gen)"，author "AI-generated"。
- 风险说明：image_risk 写清是「许可不明」还是「保留所有权利」或「许可不在白名单（Pixnio）」。
"""
import hashlib
import json
from datetime import date
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None
H = Path(__file__).resolve().parent
EP = H.parent
TODAY = date.today().isoformat()
AI_ONLY = {33, 36, 38, 39, 41, 47, 49}
AI_LIC = "AI-generated (Codex image_gen)"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def crop_save(src: Path, dst: Path, cx: float, cy: float | None = None, ratio: float = 0.9) -> tuple[int, int]:
    im = Image.open(src).convert("RGB")
    w, h = im.size
    cw = min(w, int(h * ratio))
    x0 = max(0, min(w - cw, int(cx - cw / 2)))
    im.crop((x0, 0, x0 + cw, h)).save(dst, quality=92)
    return cw, h


def main() -> None:
    d = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    assets = json.loads((EP / "assets.json").read_text(encoding="utf-8"))
    A = {a["file"]: a for a in assets}

    def put(entry: dict) -> None:
        if entry["file"] in A:
            assets[assets.index(A[entry["file"]])] = entry
        else:
            assets.append(entry)
        A[entry["file"]] = entry

    cand = H / "reselect" / "cand"
    for it in d["items"]:
        r = it["rank"]
        stem = Path(it["image"]).stem if it.get("image") else None
        gen = EP / "assets" / "img" / f"{stem}_gen.png"
        gen_rel = f"assets/img/{stem}_gen.png"
        gen_entry = {"file": gen_rel, "source_page": "", "source_url": "", "author": "AI-generated", "licence": AI_LIC,
                     "licence_url": "", "attribution_required": False,
                     "modified": "generated with Codex image_gen (tools/codex_image.py); prompt in _build/gen_prompts/; renderer will crop",
                     "sha256": sha(gen) if gen.exists() else "", "retrieved_at": TODAY, "fop_note": "",
                     "selected_by": "follow-up 016 / 追加要求 4：两轮自搜无可商用图，Codex 只做生成"}
        if False and r == 2:   # （已弃用：ESO 全景太软，改用风险图 + 生成图）Llullaillaco ESO panorama → native-resolution 9:10 crop on the summit
            src = cand / "01_02_llullaillaco" / "c13.jpg"
            dst = EP / it["image"]
            size = crop_save(src, dst, cx=2590)
            A[it["image"]]["modified"] = f"cropped to {size[0]}x{size[1]} px around the summit from the 5180x1061 original"
            A[it["image"]]["sha256"] = sha(dst)
            it["image_focus"] = [0.5, 0.3]
        if r == 34:  # Purico: ESO panorama crop around Cerro Toco as the commercial alternative
            src = cand / "33_34_purico_complex" / "c13.jpg"
            alt_rel = f"assets/img/{stem}_alt.jpg"
            size = crop_save(src, EP / alt_rel, cx=7600)
            meta = next(m for m in json.loads((cand / "33_34_purico_complex" / "meta.json").read_text(encoding="utf-8")) if m["id"] == "c13")
            put({"file": alt_rel, "source_page": meta["page_url"], "source_url": meta["image_url"], "author": meta["author"],
                 "licence": "CC BY 4.0", "licence_url": "https://creativecommons.org/licenses/by/4.0/", "attribution_required": True,
                 "modified": f"cropped to {size[0]}x{size[1]} px around Cerro Toco from the 21452x2685 panorama",
                 "sha256": sha(EP / alt_rel), "retrieved_at": TODAY, "fop_note": "",
                 "selected_by": "Codex 第二轮联网搜（ESO 图库）；Claude 看图裁切"})
            it["image_alt"] = alt_rel
            it["image_alt_credit"] = f"{meta['author']} / CC BY 4.0"
        if r in AI_ONLY:
            if not gen.exists():
                print("MISSING gen", r, gen.name); continue
            put(gen_entry)
            it["image"] = gen_rel
            it["image_credit"] = "AI-generated image (Codex)"
            for k in ("image_risk", "image_note", "image_alt", "image_alt_credit", "image_focus"):
                it.pop(k, None)
            continue
        if it.get("image_risk") and r != 34:
            if not gen.exists():
                print("MISSING gen (alt)", r, gen.name); continue
            put(gen_entry)
            it["image_alt"] = gen_rel
            it["image_alt_credit"] = "AI-generated image (Codex)"
        if it.get("image_risk"):
            lic = A[it["image"]]["licence"].lower()
            if "pixnio" in lic:
                it["image_risk"] = "licence not on whitelist (Pixnio License: free for commercial use)"
            elif "reserv" in lic:
                it["image_risk"] = "licence unknown (source page: all rights reserved)"
            else:
                it["image_risk"] = "licence unknown"
            it.pop("image_note", None)
    # 清掉不再被引用的账本条目
    used = {it.get("image") for it in d["items"]} | {it.get("image_alt") for it in d["items"]}
    assets = [a for a in assets if a["file"] in used]
    (EP / "data.json").write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (EP / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("ok", len(assets), "assets")


if __name__ == "__main__":
    main()
