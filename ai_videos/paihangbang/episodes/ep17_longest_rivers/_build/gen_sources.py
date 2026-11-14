# -*- coding: utf-8 -*-
"""data.json + assets.json + items_def.OUTSIDE → ../sources.md"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from items_def import OUTSIDE  # noqa: E402

EP = Path(__file__).resolve().parents[1]
data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
assets = {a["file"]: a for a in json.loads((EP / "assets.json").read_text(encoding="utf-8"))}

L = []
w = L.append
w("# ep17 · 数据出处、交叉核对与许可（sources.md）\n")
w("> 2026-11-03 代理整理（用户授权自主决策）。本文件由 `_build/gen_sources.py` 从 `data.json` / `assets.json` 生成；改数据请改 `_build/items_def.py` 后重跑 `build.py` → `gen_sources.py`。\n")
w("## 1. 口径\n")
w("- **榜单**：世界最长的 50 条河（含大支流），按长度（km）降序；副显示英里（km × 0.621371 四舍五入）。")
w("- **长度主值**：一律取 **Encyclopaedia Britannica** 当前条目公布值（britannica.com 直连被 Cloudflare 拦，经 web.archive.org 2025–2026 快照取原文，存于 `_build/raw/brit/`）。"
  "Britannica 给出「从最远源头量起」的水系长度时取水系值（Mississippi–Missouri、Yenisey–Angara–Selenga、Ob–Irtysh、Amur–Argun、Mackenzie–Peace–Finlay、Syr Darya–Naryn、Madeira–Mamoré、Japurá–Caquetá、Ubangi–Uele、Nelson–Saskatchewan），否则取该河本身长度。"
  "例外两条（2026-11-04 QC 后写定）：\n"
  "  1. **缺水系合计**：仅当 Britannica 给出了各段长度、却没有水系合计时，才改用国家机构的水系值——Murray–Darling 取 Geoscience Australia 3,672 km（Britannica 只分别给 Murray 2,530、Darling 2,739）。Pearl–Xi 不满足（Britannica 无任何总长），**不收**；Red River (US) 的 Britannica 条目无长度，不收。\n"
  "  2. **离群值**：Britannica 值与同一源头、同一河口的其他权威数值相差 > 25%，且没有不同源头 / 河口等口径可以解释时，改用通行值并注明 Britannica 的数：Zambezi 3,540 → 2,574 km（第 34 名）；Orinoco 2,740 → 2,140 km（落到第 51 名，出榜）。其余差 > 10% 的条目（Amur、Mekong、Juruá、Brahmaputra、Euphrates、Tocantins、Salween、Colorado、Irrawaddy）都能用源头 / 河口 / 测法解释，保留 Britannica（见 §3）。")
w("- **不重复计**：已作为更长水系一段的河不再单列（Missouri、Mississippi 本干、Irtysh、Ob 本干、Yenisey 本干、Selenga、Angara、Argun、Ucayali、Darling、Peace、Naryn、Mamoré、Caquetá、Uele）；不在水系主线上的大支流照列（Madeira、Purus、Juruá、Japurá、Negro、Lower Tunguska、Vilyuy、Aldan、Ishim、Arkansas、Paraguay、Pilcomayo、Araguaia、Ubangi、Kasai）。")
w("- **为什么不用维基列表的数**：Wikipedia「List of river systems by length」(revid 见 data.json cross_check) 绝大多数行无引用，且混用「到汇入点」与「到海」两种量法（如 Brahmaputra 3,969 含 Padma–Meghna；Tocantins–Araguaia 3,650；Irrawaddy 2,809 含 N'Mai 源）。本期只作交叉核对。")
w("- **国家（国旗）**：河口所在国——入海、入湖或汇入更大河流的地方。河口在两国界上（Congo、Rio Grande、Ubangi、Paraguay、Pilcomayo）取两国中流域面积较大的一国（代理判断，见 §2）。**屏上写明**：片头 / 页眉统计行「Flag = where the river ends」，卡上国家行写「ENDS IN …」（QC M3）。")
w("- **大洲（计分板）**：河口所在大洲。Ural 河口阿特劳跨欧亚界，按惯例计 Europe；Murray–Darling 计 Oceania。")
w("- **同值同名次**：Rio Negro 与 Ubangi–Uele 同为 2,250 km，并列第 46，按名称字母序；下一名为 48。")
w("- **统计期**：2026-11-03 取数（Britannica 快照 2025-08 至 2026-02）。河长不是年度数据，标题年份 (2026) 指取数时间。\n")

w("## 2. 归属与判断（待用户复核）\n")
w("| 议题 | 本期做法 | 依据 |\n|---|---|---|")
for a, b, c in [
    ("国旗规则", "河口所在国（不是流域最大国，也不是「最出名的国家」）", "brief 二选一；河口是可核实的单点，跨国大河少争议"),
    ("Nile → Egypt", "河口在埃及", "流域最大国是 Sudan；按河口规则取 Egypt"),
    ("Ganges / Brahmaputra → Bangladesh", "两河在孟加拉汇合入海（Padma/Meghna）", "河口规则；观众多以为 India，卡片地点行写 Himalaya → Bay of Bengal；notes 写明"),
    ("Congo → DR Congo", "河口在刚果（金）–安哥拉界上，取流域较大的刚果（金）", "边界河口规则"),
    ("Rio Grande → United States", "河口在美墨界上，取流域较大的美国；徽章 US–MEXICO BORDER", "边界河口规则"),
    ("Colorado → Mexico", "河口在墨西哥加利福尼亚湾", "河口规则；洞察卡说明它如今很少流到海"),
    ("Paraguay / Pilcomayo → Paraguay", "两河都在巴拉圭–阿根廷界上汇入，取 Paraguay", "代理判断，流域份额未单独核实"),
    ("Ubangi → DR Congo", "在刚果（金）–刚果（布）界上汇入 Congo，取刚果（金）", "边界河口规则"),
    ("Ishim → Russia", "源头与大半在哈萨克斯坦（流经阿斯塔纳），在俄罗斯汇入 Irtysh", "河口规则"),
    ("Ural → Kazakhstan / Europe", "河口阿特劳；大洲按惯例计 Europe", "Wikipedia 列表着色亦为 Europe"),
    ("Amazon 徽章 LENGTH DISPUTED", "Britannica 称其长度仍有争议", "Britannica Amazon 条目、INPE 2008、Liu 2009"),
]:
    w(f"| {a} | {b} | {c} |")
w("")

w("## 3. 差异 > 10% 的条目（交叉核对，需人决定是否换值）\n")
w("| # | 河 | 主值（Britannica） | 交叉核对 | 差异 | 说明 |\n|---|---|---|---|---|---|")
for it in data["items"]:
    cc = [it["cross_check"]] + ([it["cross_check_2"]] if it.get("cross_check_2") else [])
    big = [c for c in cc if c["diff_pct"] > 10]
    if big:
        w(f"| {it['rank']} | {it['name']} | {it['value']:,} | " + "；".join(f"{c['value']:,.0f}（{c['name'].split(',')[0][:40]}）" for c in big)
          + f" | {max(c['diff_pct'] for c in big)}% | {it['notes'][:160]} |")
w("")
w("说明：长度差异多来自「到哪个源头」「河口划在哪」「用多大比例尺量弯道」（海岸线悖论）。本期为口径一致，**不逐条挑最大值**，统一用 Britannica（离群值例外见 §1）；"
  "若改用 Wikipedia 列表值，名次会明显变化（Brahmaputra、Tocantins、Euphrates、Salween、Irrawaddy 会上升）。\n")

w("## 4. 前 50 名边界\n")
w("- 第 50 名 Kasai 2,153 km（Britannica；Wikipedia 列表同值）。2026-11-04 QC：补收 Araguaia（Britannica 2,627 km，第 32 名）；Orinoco 按离群值规则改 2,140 km 后出榜（第 51）。QC 另核 Kolyma、Songhua、Orange、Xingu、Tarim、Columbia、Brazos 的 Britannica 值都在线下，无其他漏项。")
for n, v, why in OUTSIDE:
    w(f"- {n}：{v:,} km — {why}")
w("")

w("## 5. 洞察卡核对\n")
SUP = {
    44: "Britannica Colorado 条目外链 Nature 文章「New water accounting reveals why the Colorado River no longer reaches the sea」；只在少数年份（如 2014 脉冲放水）入海——用 rarely。",
    38: "Britannica Ganges：『ends in the Ganges, or Ganges-Brahmaputra, delta』；Brahmaputra 条目：在孟加拉 Goalundo Ghat 以北与 Ganges 汇合。",
    28: "Britannica Danube：『Along its course it passes through 10 countries: Germany, Austria, Slovakia, Hungary, Croatia, Serbia, Bulgaria, Romania, Moldova, and Ukraine』。",
    20: "#19 Purus 3,211、#18 Juruá 3,283、#17 Madeira 3,352 均为 Amazon 支流（Britannica），都大于 Danube 2,850。",
    13: "Britannica Mekong 4,350；Liu et al. 2009（Int. J. Digital Earth 2(1):80–87, Table 1）Mekong 4,909 km。",
    2: "INPE 2008：Amazon 6,992 km、比 Nile 长约 140 km（FAPESP 2008-07 报道；Britannica「How long is the Amazon River?」亦引 6,992 / Nile 6,853，并说明河口划在 Marajó 岛南侧有争议）。",
}
for x in data["insights"]:
    w(f"- after {x['after_rank']}：{x['text']}  \n  依据：{SUP.get(x['after_rank'], '')}")
w("")

w("## 6. 逐条出处\n")
w("| # | 河 | 国旗 | 大洲 | 主值 | 出处（原文） | 交叉核对 | notes |\n|---|---|---|---|---|---|---|---|")
for it in data["items"]:
    s = it["source"]
    cc = it["cross_check"]
    c2 = it.get("cross_check_2")
    lab = lambda c: "WP 列表" if c["name"].startswith("Wikipedia: List") else ("Liu 2009" if c["name"].startswith("Liu") else c["name"].split(":")[0].split("(")[0].strip())
    cct = f"{lab(cc)} {cc['value']:,.0f}（{cc['diff_pct']}%）" + (f"；{lab(c2)} {c2['value']:,}（{c2['diff_pct']}%）" if c2 else "")
    w(f"| {it['rank']} | {it['name']} | {it['country_name']} | {it['continent']} | {it['value_display']} | [{s['name']}]({s['url']})：“{s['quote']}” | {cct} | {it['notes']} |")
w("")

w("## 7. 图片许可账本摘要\n")
w("| # | 河 | 文件 | 作者 | 许可 | 来源页 | 风险 / 替代 |\n|---|---|---|---|---|---|---|")
for it in data["items"]:
    a = assets.get(it.get("image", ""), {})
    alt = assets.get(it.get("image_alt", ""), {}) if it.get("image_alt") else {}
    risk = it.get("image_risk", "")
    extra = f"{risk}；默认版用 {it['image_alt']}（{alt.get('author','')} / {alt.get('licence','')}）" if risk and alt else risk
    w(f"| {it['rank']} | {it['name']} | {it.get('image','')} | {a.get('author','')} | {a.get('licence','')} | {a.get('source_page','')} | {extra} |")
w("")
w("")
w("- 默认母版：有 `image_risk` 的条目改用 `image_alt`（可商用照片或 AI 生成图）；`_with-risk-images` 版用 `image`。")
w("- AI 生成图（Codex image_gen，经 `tools/codex_image.py`，请求日志在 `ai_videos/paihangbang/request_log.md`；prompt 在 `_build/gen/`）：不冒充任何真实照片，无人物、无品牌；上传时须勾选合成内容声明。")
w("- 候选与逐项依据：`_build/reselect/cand/*/meta.json`、`_build/reselect/claude_*.json`、`codex_b*.json`；内容摘要 `_build/content/`。")
w("")
w("其他素材：国旗 flagcdn（公有领域）；字体 Inter（SIL OFL）；图标 Tabler Icons（MIT）。")

(EP / "sources.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("sources.md", len("\n".join(L)))
