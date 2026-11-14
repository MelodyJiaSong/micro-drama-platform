# -*- coding: utf-8 -*-
"""由 data.json / assets.json 生成 sources.md（改数据请改 items_def.py → build.py → 本脚本）。"""
import json
from pathlib import Path

B = Path(__file__).parent
EP = B.parent
d = json.load(open(EP / "data.json", encoding="utf-8"))
assets = {a["file"]: a for a in json.load(open(EP / "assets.json", encoding="utf-8"))}

L = []
w = L.append
w("# ep12 · 数据出处、交叉核对与许可（sources.md）\n")
w("> 2026-11-03 代理整理（用户授权自主决策）。本文件由 `_build/gen_sources.py` 从 `data.json` / `assets.json` 生成；"
  "改数据请改 `_build/items_def.py` 后重跑 `build.py` → `gen_sources.py`。原始文件在 `_build/raw/`。\n")
w("## 1. 口径\n")
w("- **指标**：总面积（surface area）= 陆地 + 内陆水域（湖泊、河流、水库），km²；副显示 sq mi（× 0.386102）。")
w("- **主源**：UN Statistics Division《Demographic Yearbook 2024》Table 3「Population by sex, annual rate of population change, surface area and density」，"
  "Surface area (km²) 2024 列（[PDF](https://unstats.un.org/unsd/demographic-social/products/dyb/documents/dyb2024/table03.pdf)，"
  "`raw/dyb2024_table03.pdf`，用 `parse_dyb.py` 按坐标抽列 → `raw/dyb2024_area_rows.json`）。UN 技术说明：surface area 指陆地加内陆水域的总面积，不含极地与无人岛。"
  "UN 数据为事实，引用并注明出处。")
w("  - 例外：**Sudan** 在 DYB 2024 中为「...」（无数据），改用 World Bank WDI `AG.SRF.TOTL.K2` 2024 值（来源 FAO，CC BY 4.0）。")
w("  - PDF 中 Argentina（2 796 427，脚注 68）与 Indonesia（1 892 410，脚注 97）的数字与脚注上标粘连、列位偏移，已逐字核读后写死在 `build.py`。")
w("- **交叉核对**：CIA World Factbook 最终版（2026-02-04 停刊；取 `factbook/factbook.json` 镜像 2026-01-22 最后一次同步，公有领域 / CC0，`raw/factbook_area.json`）。"
  "另记 World Bank `AG.SRF.TOTL.K2` / `AG.LND.TOTL.K2` 2024 值（`raw/wb_*.json`，data.json 每项 `extra` 字段）。")
w("  - **World Bank 2024 面积序列不适合作主源**：Canada 15,634,410 km²（实际约 998 万）、Norway 624,500、Sweden 528,860、France 606,410 等明显口径不一，"
  "所以本期只把它作第二参考，不用它排序（Sudan 除外，与 Factbook 差 0.9%）。")
w("- **国家名单**：主权国家（与系列惯例一致：Wikidata 主权国家，含台湾）。台湾 36,197 km² 不入前 50；"
  "格陵兰（2,166,086 km²，UN 单列）、西撒哈拉（266,000 km²，UN 单列）、法属圭亚那等海外省、南极领土主张都不计。")
w("- **争议地区**：一律用各国报给 UN 的数（UN 标准口径），在 notes 与 scope_note 写明：")
w("  - 克什米尔：India 3,287,263 含其主张的全部原查谟-克什米尔土邦（含巴基斯坦、中国实际管辖部分，约 12 万 km²）；Pakistan 796,096 不含 AJK 与吉尔吉特-巴尔蒂斯坦。两国名次不受影响（印度去掉后仍第 7）。")
w("  - 西撒哈拉：UN 单列，不计入 Morocco（446,550）。若按 Factbook 计入（716,550），Morocco 会排第 39。")
w("  - Ukraine 603,500 = 国际承认边界（含克里米亚与被占领土）；Russia 17,098,246 不含克里米亚等（Rosstat 2014 后自报约 1,712.5 万）。")
w("  - France 551,500 = 本土 + 科西嘉；Factbook 643,801 含五个海外大区，按它 France 会到第 42 左右。")
w("  - 部分争议区可能被两国重复计入（India 与 China 都含阿克赛钦约 3.8 万 km²；Kenya 与 South Sudan 的 UN 值可能都含伊莱米三角），名次不受影响。")
w("  - 南极：Australia、Argentina、Chile、France 的南极主张都不计（DYB 脚注 68 明写 Argentina 不含南极；Australia 的南极领土约 590 万 km²，42% 南极，据 Australian Antarctic Division）。")
w("- **大洲（计分板）**：按 UN M49 区域（跨洲国家：Russia → Europe，Kazakhstan / Türkiye → Asia，Egypt → Africa，Mexico → North America，Indonesia → Asia）。")
w("- **显示**：`value_display` 3 位有效数字（≥ 100 万写 M），`secondary_display` 同规则换算 sq mi；排序用原值。差异 = |cross − value| / value。\n")

w("## 2. 交叉核对差异 > 1% 与名次敏感项\n")
w("| # | 国家 | UN DYB | Factbook | 差异 % | 影响 |\n|---|---|---|---|---|---|")
for it in d["items"]:
    cc = it["cross_check"]
    if cc["diff_pct"] > 1 or "ORDER-SENSITIVE" in it["notes"]:
        w(f"| {it['rank']} | {it['country_name']} | {it['value']:,} | {cc['value']:,.0f} | {cc['diff_pct']} | {it['notes'][:260]} |")
w("\n- 第 50 Thailand 513,140；第 51 Spain 506,009（Factbook 505,370），第 52 Turkmenistan 488,100。若整体改用 Factbook：Factbook 把西撒哈拉计入 Morocco（716,550），Morocco 进榜约第 39、Thailand 掉出——这是唯一改变成员的口径；其余只有名次微调（Venezuela/Nigeria、South Sudan/Afghanistan、Kenya/Madagascar/Botswana 互换，France 含海外大区升到约第 42）。")
w("- Peru 1,285,216 与 Chad 1,284,000 三个来源一致，差 1,216 km²（香港 1,115 km²，DYB）。\n")

w("## 3. 洞察卡出处\n")
facts = {
    41: "South Sudan 独立 2011-07-09；分离前 Sudan 约 2.5M km²（Permanent Mission of Sudan to the UN：Sudan 现为非洲第三大，次于 Algeria、DR Congo），658,841 / (1,878,000 + 658,841) ≈ 26%。",
    32: "Venezuela 929,690（DYB）− Nigeria 923,768 = 5,922 km²；Factbook 与 World Bank 的 Venezuela 都是 912,050，排在 Nigeria 后。",
    21: "Peru 1,285,216 − Chad 1,284,000 = 1,216 km²；Hong Kong 1,115 km²（DYB 2024，同表）。",
    14: "Greenland 2,166,086 km²（DYB 2024 单列，脚注 133：Denmark 不含 Faroe 与 Greenland），介于 Saudi Arabia 2,206,714 与 Mexico 1,964,375 之间 → 第 13。",
    4: "Factbook 陆地：China 9,326,410、US 9,147,593、Canada 9,093,507（Russia 16,377,742）；World Bank 陆地 2024 同序（China 9,388,210 > US 9,147,420 > Canada 8,788,700）。",
    2: "NASA Pluto Facts：赤道直径约 2,377 km → 表面积 π·d² ≈ 17.75M km²；Russia 17,098,246 km²。旧说「俄罗斯比冥王星大」用的是 New Horizons（2015）之前的较小直径估计。",
}
for ins in d["insights"]:
    w(f"- after {ins['after_rank']}：“{ins['text']}” — {facts.get(ins['after_rank'], '')}")
w("")
w("## 4. 逐条出处与交叉核对\n")
w("所有条目 retrieved_at = 2026-11-03。WB = World Bank 2024 surface area（只作参考）。\n")
w("| # | 国家 | value (km²) | 主值来源 | Factbook | 差异 % | WB | 备注 |\n|---|---|---|---|---|---|---|---|")
for it in d["items"]:
    s, cc, ex = it["source"], it["cross_check"], it["extra"]
    wbv = f"{ex['wb_2024_surface_km2']:,.0f}" if ex.get("wb_2024_surface_km2") else "—"
    w(f"| {it['rank']} | {it['country_name']} | {it['value']:,} | [{s['name']}]({s['url']}) | {cc['value']:,.0f} | {cc['diff_pct']} | {wbv} | {it['notes']} |")
w("")
w("## 5. 图片许可（assets.json）\n")
w("| # | 国家 | 题材 | 文件 | 作者 | 许可 | 来源页 | 风险 / 默认版替代 |\n|---|---|---|---|---|---|---|---|")
for it in d["items"]:
    a = assets.get(it.get("image"), {})
    alt = assets.get(it.get("image_alt", ""), {})
    risk = it.get("image_risk", "")
    if alt:
        risk += f"；默认版用 `{it['image_alt']}`（{alt.get('author','')} / {alt.get('licence','')}）"
    w(f"| {it['rank']} | {it['country_name']} | {it['subtitle']} | `{it.get('image','')}` | {a.get('author','')} | {a.get('licence','')} | {a.get('source_page','')} | {risk} |")
w("")
(EP / "sources.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("sources.md", len("\n".join(L)))
