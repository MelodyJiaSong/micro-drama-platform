# -*- coding: utf-8 -*-
"""data.json → sources.md（每条主值的出处、交叉核对、推算锚点）。"""
import json
from pathlib import Path
EP = Path(__file__).resolve().parents[1]
d = json.loads((EP / "data.json").read_text(encoding="utf-8"))
L = ["# ep05 · 出处与核对", "", "> 由 `_build/gen_sources.py` 从 `data.json` 生成，取数日 2026-11-03。调研原始记录（含原文引句）在 `_build/research/group_{a,b,c}.json`。", "",
     "## §1 口径", "", "- **documented**：机构或文献直接给出的累计数，窗口照原文。",
     "- **est.**：同一来源体系 ≥2 个全球年度估计为锚点，逐年线性插值后对窗口内每年求和；窗口两端超出锚点的年份按最近锚点持平（`_build/cumulative.py`，结果 `cumulative.json`）。屏上 2 位有效数字。",
     "- **reported**：官方报告病例死亡（新冠）。", "- 只收病毒；晚期并发症（肝硬化、肝癌、宫颈癌等）算入，徽章与 notes 写明；单一国家的总数在卡上标 ONLY 徽章。", "",
     "## §2 逐条", ""]
for it in d["items"]:
    s = it["source"]
    L.append(f"### #{it['rank']} {it['name']} — {it['value_display']} {it['secondary_display']}（{it['country_name'].replace('Deaths · ', '')}，{it['value_kind']}）")
    L.append(f"- 主值：{it['value']:,.0f}；来源：{s['name']}（{s['tier']}）<{s['url']}>")
    if it.get("cumulative"):
        c = it["cumulative"]
        L.append(f"- 推算锚点（{c['basis']}）：" + "，".join(f"{y}: {v:,}" for y, v in c["anchors"].items()) + f"；窗口 {c['start']}–{c['end']}")
    if it.get("cross_check"):
        x = it["cross_check"]
        L.append(f"- 交叉核对：{x['name']} = {x['value']:,}（与主值差 {x['diff_pct']}%）<{x['url']}>")
    if it.get("notes"):
        L.append(f"- 备注：{it['notes']}")
    L.append(f"- 传播途径（计分板）：{it['continent']}；标签：" + " / ".join(t["text"] for t in it["tags"]) + (f"；徽章：{it['badge']}" if it["badge"] else ""))
    L.append("")
L += ["## §3 洞察卡依据", ""]
for ins in d["insights"]:
    L.append(f"- after #{ins['after_rank']}：{ins['text']}")
L += ["  - 依据：#27 之后——第 18、20、23、24、25、29 名为单国计数；#22 之后——15,514 + 774 + 960 + 561 = 17,809；狂犬病——WHO 狂犬病情况说明书（发病后几乎 100% 致死），巴斯德 1885 年 7 月 6 日首次给 Joseph Meister 接种；新冠——WHO 报告 7,117,689，WHO 超额 14.83M（2020–21，Nature 2023），The Economist 27.1–28.5M；麻疹 vs HIV——43M（1980–2024 est.）vs 44.2M；天花——WHO：1980 年宣布根除，最后一例自然病例 1977 年索马里。", "",
      "## §4 不进榜的病毒与原因", "",
      "- 脊髓灰质炎：只有麻痹病例数（1988 年约 35 万例），没有全球死亡估计。", "- 风疹、腮腺炎、巨细胞病毒、单纯疱疹、HTLV-1：只有病例或局部死亡数。",
      "- 人偏肺病毒（2018 年 1.61 万）、副流感（3.44 万）、腺病毒（3.69 万）：只有单一年份、5 岁以下儿童估计，不满足 ≥2 个锚点。",
      "- 丁肝：GBD 不单列，死亡含在乙肝里。", "- 拉沙热：CDC/ECDC「每年约 5,000」为粗估；尼日利亚 2025 年确诊死亡 215（NCDC 第 52 周）。没有累计数。",
      "- 寨卡、基孔肯雅：全球死亡数零散（基孔肯雅 2025 年 WHO 报告 155–186）。", ""]
(EP / "sources.md").write_text("\n".join(L), encoding="utf-8")
print("ok", len(L))
