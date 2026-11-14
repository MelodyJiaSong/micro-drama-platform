# -*- coding: utf-8 -*-
"""找图第一步：每个条目写 content/NN_<slug>.md（景点是什么、在哪、长什么样、标志性视角、易混对象、最佳拍摄点）。
文字来源：维基百科摘要（content/raw，只取文字）+ landmarks.py 里的拍摄要点。"""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
EP = HERE.parent
sys.path.insert(0, str(HERE))
from landmarks import LANDMARKS
from build import LM_KEY, slug

data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
for it in data["items"]:
    key = LM_KEY.get(it["name"], it["name"])
    name, place, wp, note = LANDMARKS[key]
    raw = HERE / "content" / "raw" / f"{re.sub(r'[^a-z0-9]+', '_', key.lower()).strip('_')}.json"
    r = json.loads(raw.read_text(encoding="utf-8")) if raw.exists() else {}
    ext = r.get("extract", "")
    paras = [p.strip() for p in ext.split("\n") if len(p.strip()) > 80]
    intro = " ".join(paras[:3])[:1500]
    look = [p for p in paras if re.search(r"\b(view|seen|visible|colou?r|towers?|façade|facade|white|red|blue|granite|marble|dome|peak|cliff|lake|beach|island)\b", p, re.I)]
    coords = r.get("coordinates") or []
    co = f"{coords[0]['lat']:.4f}, {coords[0]['lon']:.4f}" if coords else "—"
    view, *excl = note.split("; NOT ")
    L = [f"# {it['rank']:02d} · {it['name']} — {name}", "",
         f"- 卡片：{it['name']}（{it['value_display']}，{it['secondary_display']}），地点行「{place}」",
         f"- 景点：**{name}**；维基条目 {r.get('wp_title', wp)}（{r.get('url', '')}，仅取文字，{r.get('retrieved_at', '')}）",
         f"- 一句话：{r.get('description') or '—'}；坐标 {co}", "",
         "## 它是什么、在哪", "", intro or "（未取到摘要）", "",
         "## 长什么样（摘录）", ""] + [f"- {p[:400]}" for p in look[:3]] + ["",
         "## 标志性视角与最佳拍摄点", "", f"- {view}", "",
         "## 易混淆 / 要排除", ""] + ([f"- NOT {e}" for e in excl] or ["- 无明显同名对象；排除带水印、文字叠加、拼贴、AI 渲染图"]) + ["",
         "## 版权提示", "", "- 优先自然景观或古迹；现代建筑需看所在国全景自由（FoP）。", ""]
    (HERE / "content" / f"{it['rank']:02d}_{slug(it['name'])}.md").write_text("\n".join(L), encoding="utf-8")
print("ok", len(data["items"]))
