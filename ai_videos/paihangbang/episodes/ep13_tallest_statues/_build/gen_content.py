# -*- coding: utf-8 -*-
"""follow-up 016 第一步：为每项写 _build/content/NN_<slug>.md（它是什么、在哪、长什么样、标志性视角、易混对象、出处摘录）。
只用已抓取的网页文字（WebSearch / WebFetch 调研记录 + 维基 API 摘要 raw/wp_extracts/），不调 Codex。"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parent
sys.path.insert(0, str(HERE))
from items_def import ITEMS  # noqa: E402
from hints import H  # noqa: E402

by_name = {d["name"]: d for d in ITEMS}
data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
out = HERE / "content"
out.mkdir(exist_ok=True)
for i, it in enumerate(data["items"]):
    src = by_name[it["name"]]
    h = H[it["name"]]
    key = Path(it["image"]).stem
    ex = ""
    if src.get("wp"):
        f = HERE / "raw" / "wp_extracts" / (re.sub(r"[^A-Za-z0-9]+", "_", src["wp"]) + ".txt")
        if f.exists():
            ex = f.read_text(encoding="utf-8").strip()
    md = [f"# {it['rank']} · {it['name']}（{it['country_name']}）", "",
          f"- 位置：{it['subtitle']}, {it['country_name']}",
          f"- 本体高：{it['value_display']}（{it['secondary_display']}）；含基座总高：{src.get('total') or '—'} m；建成：{src.get('year') or '未确认'}",
          f"- 主源：[{src['src'][0]}]({src['src'][1]})",
          f"- 全景自由：{src['fop']}" + (f"（{it.get('image_risk','')}）" if src["fop"] == "risk" else ""),
          "", "## 长什么样 / 辨认特征", h["look"], "",
          "## 标志性视角 / 最佳机位", h["view"], "",
          "## 易混淆对象（找图时排除）", h["avoid"], "",
          "## 调研笔记", src["notes"], ""]
    if ex:
        md += ["## 维基百科摘要（只作文字参考，图片不用维基）", ex[:1800], ""]
    (out / f"{key}.md").write_text("\n".join(md), encoding="utf-8")
print(f"写了 {len(data['items'])} 个 content 文件 → {out}")
