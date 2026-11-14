# -*- coding: utf-8 -*-
"""逐项看全部候选：每项一行，所有候选按卡片比例 (720:800) 居中裁切，标 id / 分辨率 / 来源 / 许可（绿=可商用，红=不明）。
    python contact_sheet.py [idx ...]      # 默认全部，每页 5 项 → _build/reselect/sheet_NN.jpg
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[3] / "projects" / "rank_scroll"))
from rank_scroll.contract import _licence_ok  # noqa: E402

Image.MAX_IMAGE_PIXELS = None
TW, TH = 288, 320
F = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 18)
FS = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 13)


def main(only):
    data = json.load(open(EP / "data.json", encoding="utf-8"))
    rows = [(i, it) for i, it in enumerate(data["items"]) if not only or i in only]
    cand = EP / "_build" / "reselect" / "cand"
    for page in range(0, len(rows), 5):
        chunk = rows[page:page + 5]
        metas = []
        for i, it in chunk:
            d = cand / f"{i:02d}_{Path(it['image']).stem}"
            m = json.loads((d / "meta.json").read_text(encoding="utf-8")) if (d / "meta.json").exists() else []
            metas.append((i, it, d, m))
        ncol = max([len(m) for *_, m in metas] + [1])
        sheet = Image.new("RGB", (200 + ncol * (TW + 6), len(chunk) * (TH + 44) + 8), (22, 22, 26))
        dr = ImageDraw.Draw(sheet)
        for r, (i, it, d, meta) in enumerate(metas):
            y = 6 + r * (TH + 44)
            dr.text((6, y), f"#{it['rank']} {it['name'][:16]}", font=F, fill=(240, 240, 240))
            dr.text((6, y + 26), f"idx {i}", font=FS, fill=(170, 170, 170))
            dr.text((6, y + 46), it["subtitle"][:24], font=FS, fill=(170, 170, 170))
            for c, m in enumerate(meta):
                x = 200 + c * (TW + 6)
                try:
                    with Image.open(d / m["file"]) as im:
                        sheet.paste(ImageOps.fit(ImageOps.exif_transpose(im).convert("RGB"), (TW, TH)), (x, y))
                except Exception:  # noqa: BLE001
                    dr.text((x + 6, y + 6), "无法打开", font=FS, fill=(230, 90, 70))
                ok = _licence_ok(m.get("licence", ""))
                dr.text((x, y + TH + 2), f"{m['id']} {m.get('w','?')}x{m.get('h','?')} {m.get('source','')[:12]}", font=FS, fill=(220, 220, 220))
                dr.text((x, y + TH + 20), m.get("licence", "")[:30], font=FS, fill=(80, 200, 100) if ok else (230, 90, 70))
        sheet.save(EP / "_build" / "reselect" / f"sheet_{chunk[0][0]:02d}.jpg", quality=85)
        print("sheet", chunk[0][0])


if __name__ == "__main__":
    main([int(x) for x in sys.argv[1:]])
