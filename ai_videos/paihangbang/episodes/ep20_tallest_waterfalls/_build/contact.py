# -*- coding: utf-8 -*-
"""逐项全部候选拼图（follow-up 016/023 亲眼看图用）：python -I contact.py [idx ...] → reselect/contact_NN.jpg（每张 4 项）。
绿框 = 可商用许可（与 rank_scroll 白名单同一判断）；红框 = 许可不明 / 不允许（只能进风险版）。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).parent
EP = HERE.parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO / "projects" / "rank_scroll"))
from rank_scroll.contract import _licence_ok  # noqa: E402

TW, TH = 180, 240


def main() -> None:
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    want = [int(x) for x in sys.argv[1:]] or list(range(len(data["items"])))
    f = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 16)
    fs = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 12)
    per = 4
    for page in range(0, len(want), per):
        rows = want[page:page + per]
        metas = []
        for i in rows:
            it = data["items"][i]
            d = HERE / "reselect" / "cand" / f"{i:02d}_{Path(it['image']).stem}"
            m = json.loads((d / "meta.json").read_text(encoding="utf-8")) if (d / "meta.json").exists() else []
            metas.append((i, it, d, m))
        ncol = 9
        heights = [26 + max(1, -(-len(m) // ncol)) * (TH + 34) for *_, m in metas]
        sheet = Image.new("RGB", (ncol * (TW + 6) + 10, sum(heights) + 10), (22, 22, 26))
        dr = ImageDraw.Draw(sheet)
        y = 5
        for (i, it, d, m), h in zip(metas, heights):
            dr.text((8, y), f"idx {i} · #{it['rank']} {it['name']} ({it['country_name']}) · {len(m)} cand", font=f, fill=(240, 240, 240))
            for k, c in enumerate(m):
                x = 5 + (k % ncol) * (TW + 6)
                yy = y + 26 + (k // ncol) * (TH + 34)
                ok = _licence_ok(c.get("licence", ""))
                dr.rectangle([x, yy, x + TW - 1, yy + TH - 1], fill=(40, 170, 80) if ok else (200, 50, 50))
                try:
                    with Image.open(d / c["file"]) as im:
                        sheet.paste(ImageOps.fit(ImageOps.exif_transpose(im).convert("RGB"), (TW - 6, TH - 6)), (x + 3, yy + 3))
                except Exception:  # noqa: BLE001
                    pass
                dr.text((x + 2, yy + TH + 1), f"{c['id']} {c.get('w','?')}x{c.get('h','?')}", font=fs, fill=(230, 230, 230))
                dr.text((x + 2, yy + TH + 16), f"{c.get('licence','')[:14]}|{c.get('source','')[:10]}", font=fs, fill=(160, 220, 160) if ok else (240, 150, 150))
            y += h
        out = HERE / "reselect" / f"contact_{page // per + 1:02d}.jpg"
        sheet.save(out, quality=85)
        print(out.name, rows)


if __name__ == "__main__":
    main()
