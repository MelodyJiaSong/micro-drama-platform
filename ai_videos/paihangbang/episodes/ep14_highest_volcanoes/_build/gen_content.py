# 找图第一步（follow-up 016）：每项内容落盘 content/NN_<slug>.md —— GVP 地质概述（官方文字）+ Wikipedia 导言 + 代理整理的辨认要点。
import json
from pathlib import Path
from items_def import ITEMS
H = Path(__file__).resolve().parent
d = json.loads((H.parent / "data.json").read_text(encoding="utf-8"))
gvp = {f["properties"]["Volcano_Number"]: f["properties"] for f in json.loads((H / "raw/gvp_holocene.json").read_text(encoding="utf-8"))["features"]}
wk = json.loads((H / "raw/wiki_extracts_2026-11-03.json").read_text(encoding="utf-8"))
norm = wk.get("_norm", {})
(H / "content").mkdir(exist_ok=True)
for it in d["items"]:
    vn = it["gvp_volcano_number"]; p = gvp[vn]; name, sub, wt, hint = ITEMS[vn]
    t = norm.get(wt, wt); t = norm.get(t, t)
    ex = (wk.get(t) or {}).get("extract", "") or "（Wikipedia 导言未取到）"
    stem = Path(it["image"]).stem
    md = f"""# #{it['rank']} {name}（GVP {vn}: {p['Volcano_Name']}）

- 位置：{sub}；GVP 国家字段 {p['Country']}；坐标 {p['Latitude']}, {p['Longitude']}；GVP 海拔 {p['Elevation']} m
- 类型：{p['Primary_Volcano_Type']}；最近喷发：{p.get('Last_Eruption_Year')}（{p.get('Evidence_Category')}）
- 来源：GVP WFS（2026-11-03 取数）；Wikipedia「{t}」导言（2026-11-03）
- GVP 主图说明（只作辨认参考，不用其图）：{p.get('Primary_Photo_Caption') or '无'}

## 辨认要点 / 标志性视角 / 易混对象 / 最佳拍摄点（代理整理，写进 image_hint）

{hint}

## GVP 地质概述

{p.get('Geological_Summary') or ''}

## Wikipedia 导言

{ex}
"""
    (H / "content" / f"{stem}.md").write_text(md, encoding="utf-8")
print(len(list((H / "content").glob("*.md"))))
