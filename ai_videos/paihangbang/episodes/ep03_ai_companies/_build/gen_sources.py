# -*- coding: utf-8 -*-
"""data.json + assets.json → sources.md（每条主值的出处、交叉核对、口径备注；图片来源与许可）。"""
import json
from collections import Counter
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
d = json.loads((EP / "data.json").read_text(encoding="utf-8"))
assets = {a["file"]: a for a in json.loads((EP / "assets.json").read_text(encoding="utf-8"))}

L = ["# ep03 · 数据出处、交叉核对与图片许可（sources.md）", "",
     "> 由 `_build/gen_sources.py` 从 `data.json` / `assets.json` 生成；改数据请改 `_build/items_ab.py` / `items_c.py` 后依次跑 "
     "`make_items_def.py` → `build.py` → `gen_sources.py`。调研原始记录在 `_build/research/batch_*.json`（含创始人全名单、员工数、"
     "未采用的洽谈中估值等）。", "",
     "## 1. 口径", "", d["scope_note"], "",
     "- 顺序：成立年月从老到新；只知道年份的用占位月份排序，屏上只显示年份（见 topic.md）。",
     "- 主值来源分级：公司公告 / 交易所 > 主流财经媒体（Bloomberg、Reuters、CNBC、TechCrunch、Caixin…）> 聚合站；维基百科只作交叉核对（follow-up 009）。",
     "- 调研子代理打不开部分新闻站，只见搜索摘要的条目已在 notes 注明；OpenAI、Anthropic、Cursor、Hugging Face 四条由主代理再次搜索核对（2026-11-03）。", "",
     "## 2. 逐条", ""]
for it in d["items"]:
    s = it.get("source") or {}
    L.append(f"### {it['rank']}. {it['name']}（{it.get('corner', '')}，{it['subtitle']}）")
    L.append("")
    L.append(f"- 卡上：**{it['value_display']}** {it.get('secondary_display', '')}" + (f"；徽章 {it['badge']}" if it.get("badge") else ""))
    L.append(f"- 主值来源：[{s.get('name')}]({s.get('url')})（取于 {s.get('retrieved_at')}）")
    cc = it.get("cross_check")
    if cc:
        L.append(f"- 交叉核对：[{cc['name']}]({cc['url']})，{cc['value'] / 1e9:g}B，差 {cc['diff_pct']}%")
    else:
        L.append("- 交叉核对：无第二独立来源（见备注）")
    if it.get("notes"):
        L.append(f"- 备注：{it['notes']}")
    p = it.get("person") or {}
    L.append(f"- 头像：{p.get('name')}（{p.get('role')}）")
    L.append("")

L += ["## 3. 洞察卡", ""]
for ins in d.get("insights", []):
    after = next(i["name"] for i in d["items"] if i["rank"] == ins["after_rank"])
    L.append(f"- 在 {after} 之后：{ins['text']}")
L += ["", "依据：Hugging Face 早期为青少年聊天机器人（调研 A fun_fact）；Aidan Gomez 为《Attention Is All You Need》作者之一（arXiv 1706.03762）；"
      "Midjourney 未外部融资、Meta 2025-08 授权其技术（Reuters / The Star）；DeepSeek-R1 发布后 Nvidia 单日市值蒸发约 $589B（2025-01，调研 C）；"
      "第 5 条由本表 badge 与 status 汇总。", ""]

L += ["## 4. 图片来源与许可", "",
      "全部候选与 meta 在 `assets/ref/<公司>/<logo|photo|person>/`（Codex 联网搜，6 轮，见 topic.md）。下表为进卡的图。", "",
      "| 文件 | 类 | 来源页 | 作者 / 来源 | 许可（照抄来源页） |", "|---|---|---|---|---|"]
risk = Counter()
for it in d["items"]:
    files = [it.get("image"), it.get("image_alt"), it.get("logo"), (it.get("person") or {}).get("image")]
    for f in files:
        if not f or f not in assets:
            continue
        a = assets[f]
        L.append(f"| `{f}` | {a['kind']} | {a.get('source_page') or '—'} | {a.get('author') or a.get('source_site') or '—'} | {a['licence']} |")
    if it.get("image_risk"):
        risk[it["image_risk"]] += 1
    if (it.get("person") or {}).get("image_risk"):
        risk["portrait: " + it["person"]["image_risk"]] += 1
L += ["", "风险标记汇总（默认母版扣下，`_with-risk-images` 版放进去，发布前由用户签字）：", ""]
L += [f"- {k}：{v}" for k, v in risk.most_common()]
L += ["", "`*_alt.jpg` 是默认母版用的可商用替代图（follow-up 020 / 032）：CC / Pexels / Unsplash 实拍，或 Claude 多轮搜索无可商用实拍时由 Codex 生成的插图（许可记 AI-generated，无真人、无 logo）。logo 按商标指认使用（bible §4），不改色、不变形；Midjourney 卡主图也是 Codex 生成的插图。含 AI 生成图，上传时勾选合成内容声明。", ""]
(EP / "sources.md").write_text("\n".join(L), encoding="utf-8")
print("sources.md written,", len(L), "lines")
