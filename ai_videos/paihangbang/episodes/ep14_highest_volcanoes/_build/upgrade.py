# -*- coding: utf-8 -*-
"""追加要求 5 的升级轮：对低分辨率 / 观感一般的风险图，全网（Bing 图片，大图过滤）再找，下载到 _build/upgrade/<rank>/，
出拼图看图；选中后用 install 写回 assets/img、assets.json、data.json（许可照实，"unknown" 的标 image_risk）。

    python _build/upgrade.py search <rank> "<query>" "<kw1,kw2>"
    python _build/upgrade.py sheet  <rank> [<rank> ...]
    python _build/upgrade.py install <rank> <cand_no> [--licence "..."] [--author "..."]
"""
import hashlib
import json
import subprocess
import sys
import urllib.parse
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bing_search import BAD, search  # noqa: E402

H = Path(__file__).resolve().parent
EP = H.parent
UP = H / "upgrade"
CURL = "C:/Program Files/Git/mingw64/bin/curl.exe"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"


def do_search(rank: int, q: str, kws: str) -> None:
    d = UP / f"{rank:02d}"
    d.mkdir(parents=True, exist_ok=True)
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8")) if (d / "meta.json").exists() else []
    seen = {m["image_url"] for m in meta}
    keys = [k.strip().lower() for k in kws.split(",")]
    for f in search(q):
        low = (f["murl"] + " " + f["purl"]).lower()
        if f["murl"] in seen or any(b in low for b in BAD) or not any(k in (f["t"] + " " + low).lower() for k in keys):
            continue
        n = len(meta)
        out = d / f"u{n}.jpg"
        subprocess.run([CURL, "-s", "-L", "-m", "40", "-A", UA, "-o", str(out), f["murl"]])
        try:
            with Image.open(out) as im:
                w, h = im.size
        except Exception:  # noqa: BLE001
            out.unlink(missing_ok=True); continue
        if min(w, h) < 700:
            out.unlink(missing_ok=True); continue
        seen.add(f["murl"])
        meta.append({"id": f"u{n}", "file": out.name, "image_url": f["murl"], "page_url": f["purl"],
                     "source": urllib.parse.urlparse(f["purl"]).netloc, "title": f["t"], "w": w, "h": h})
    (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(rank, len(meta), [(m["id"], m["w"], m["h"], m["source"][:20]) for m in meta])


def sheet(ranks: list[int]) -> None:
    TW, TH = 260, 289
    f = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 12)
    rows = [(r, json.loads((UP / f"{r:02d}" / "meta.json").read_text(encoding="utf-8"))) for r in ranks]
    ncol = min(10, max(len(m) for _, m in rows))
    s = Image.new("RGB", (60 + ncol * (TW + 4), len(rows) * (TH + 30)), (20, 20, 24))
    dr = ImageDraw.Draw(s)
    for y, (r, meta) in enumerate(rows):
        dr.text((4, y * (TH + 30) + 4), f"#{r}", font=ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 18), fill=(255, 255, 255))
        for x, m in enumerate(meta[:ncol]):
            try:
                im = ImageOps.fit(Image.open(UP / f"{r:02d}" / m["file"]).convert("RGB"), (TW - 4, TH - 4))
                s.paste(im, (60 + x * (TW + 4), y * (TH + 30)))
            except Exception:  # noqa: BLE001
                pass
            dr.text((60 + x * (TW + 4), y * (TH + 30) + TH - 2), f"{m['id']} {m['w']}x{m['h']} {m['source'][:20]}", font=f, fill=(220, 220, 220))
    out = H / f"upgrade_sheet_{'_'.join(map(str, ranks))[:40]}.jpg"
    s.save(out, quality=85)
    print(out)


def install(rank: int, cid: str, licence: str = "unknown", author: str = "unknown") -> None:
    d = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    assets = json.loads((EP / "assets.json").read_text(encoding="utf-8"))
    it = d["items"][rank - 1]
    m = next(x for x in json.loads((UP / f"{rank:02d}" / "meta.json").read_text(encoding="utf-8")) if x["id"] == cid)
    was_gen = it["image"].endswith("_gen.png")
    if was_gen:                      # AI-only 项升级为真实照片：生成图转作默认版 image_alt
        it["image_alt"], it["image_alt_credit"] = it["image"], "AI-generated image (Codex)"
    rel = it["image"] if not was_gen else it["image"].replace("_gen.png", ".jpg")
    dst = EP / rel
    if dst.exists():
        (H / "old_img").mkdir(exist_ok=True)
        dst.replace(H / "old_img" / (dst.stem + "_pre_upgrade" + dst.suffix))
    with Image.open(UP / f"{rank:02d}" / m["file"]) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        if max(im.size) > 2400:
            im.thumbnail((2400, 2400), Image.LANCZOS)
        im.save(dst, quality=90)
        size = im.size
    entry = {"file": rel, "source_page": m["page_url"], "source_url": m["image_url"], "author": author, "licence": licence,
             "licence_url": "", "attribution_required": licence != "unknown",
             "modified": f"re-encoded as JPEG {size[0]}x{size[1]} px; renderer will crop", "sha256": hashlib.sha256(dst.read_bytes()).hexdigest(),
             "retrieved_at": date.today().isoformat(), "fop_note": "", "selected_by": "追加要求 5 升级轮：Claude 全网检索（Bing 图片）后看图挑选"}
    assets = [a for a in assets if a["file"] != rel] + [entry]
    it["image"] = rel
    it["image_credit"] = f"{author} / {licence}" if author != "unknown" else f"{m['source']} / licence unknown"
    it.pop("image_focus", None)
    if licence == "unknown":
        it["image_risk"] = "licence unknown"
    (EP / "data.json").write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (EP / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("installed", rank, rel, size)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "search":
        do_search(int(sys.argv[2]), sys.argv[3], sys.argv[4])
    elif cmd == "sheet":
        sheet([int(x) for x in sys.argv[2:]])
    elif cmd == "install":
        args = sys.argv[2:]
        kw = {}
        for k in ("--licence", "--author"):
            if k in args:
                i = args.index(k); kw[k[2:]] = args[i + 1]; del args[i:i + 2]
        install(int(args[0]), args[1], **kw)
