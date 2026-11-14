# -*- coding: utf-8 -*-
"""ep14 sources.md 生成（由 data.json / assets.json 派生；改数据改 items_def.py / build.py 后重跑）。"""
import json
from collections import Counter
from pathlib import Path

H = Path(__file__).resolve().parent
EP = H.parent
d = json.loads((EP / "data.json").read_text(encoding="utf-8"))
assets = {a["file"]: a for a in json.loads((EP / "assets.json").read_text(encoding="utf-8"))}
items = d["items"]

L = []
w = L.append
w("# ep14 · 数据出处、交叉核对与许可（sources.md）\n")
w("> 2026-11-03 代理整理（follow-up 015 子代理）。本文件由 `_build/gen_sources.py` 从 `data.json` / `assets.json` 生成。\n")
w("## 1. 口径\n")
w("- **名单**：Smithsonian Institution Global Volcanism Program（GVP）《Volcanoes of the World》数据库的 **Holocene 火山表**（全新世约 11,700 年内有喷发或活动证据；含 GVP 标 *Evidence Uncertain* 的条目）。")
w("  - 取数：GVP 官方 GeoServer WFS `https://webservices.volcano.si.edu/geoserver/GVP-VOTW/ows`，图层 `GVP-VOTW:Smithsonian_VOTW_Holocene_Volcanoes`，2026-11-03 下载，共 1,214 座（原始文件 `_build/raw/gvp_holocene.json`）；Pleistocene 表同日下载 1,452 座（`_build/raw/gvp_pleistocene.json`），只用于说明口径与洞察卡 1。")
w("  - GVP 网页 `volcano.si.edu/volcano.cfm?vn=…` 当天对脚本返回 Cloudflare 验证页，卡片 `source.url` 仍写该火山的 GVP 页面地址，数值以 WFS 下载为准。")
w("- **排序**：GVP `Elevation` 字段（峰顶海拔，m）降序取前 50；前 50 无同值。San José 用 GVP 地质概述的 5,856 m（WFS 字段 6,070 m 实为邻峰 Marmolejo，审片问题 1）。第 50 名 Popocatépetl 5,393 m，第 51 名 Ticsani 5,382 m（差 11 m）。")
w("- **显示**：`value_display` 为 GVP 整米值；`secondary_display` = 米 × 3.28084 四舍五入到整英尺。")
w("- **不收**：GVP Pleistocene 表的火山（Kilimanjaro 5,881、Sajama 6,542、Tupungato 6,570、Tres Cruces 6,620、Ulagh Muztagh 6,945 等）；GVP 两表都没有的 Monte Pissis。")
w("- **标签**：`calendar` = GVP `Last_Eruption_Year`（负数写 BCE；1000 年以前写 c. … CE；无年份时按 GVP 证据类别写 *Eruption date unknown*（Evidence Credible）或 *Possible recent activity*（Evidence Uncertain）；GVP 为 Eruption Observed 但无年份的写 *Eruption observed*）；`mountain` = GVP `Primary_Volcano_Type`。GVP 对持续中的喷发把最近喷发年记为当年，2026 = 2026 年仍有喷发。\n")
w("## 2. 国家归属\n")
w("- 国旗 = GVP `Country` 字段第一个国家；字段含两国（如 `Chile-Argentina`）时加 `SHARED WITH <第二国>` 徽章。GVP 对智利与阿根廷 / 玻利维亚的跨境火山一律把 Chile 写在前。")
cnt = Counter(i["country_name"] for i in items)
w("- 计分板（tally.by = country）：" + "、".join(f"{k} {v}" for k, v in cnt.most_common()) + "。")
shared = [i for i in items if i.get("badge", "").startswith("SHARED")]
w(f"- 跨境 {len(shared)} 座：" + "、".join(f"#{i['rank']} {i['name']}（{i['badge'][12:].title()}）" for i in shared) + "。")
w("- 若把跨境火山同时计入第二国：Argentina 4 + 13 = 17，Bolivia 1 + 5 = 6（洞察卡 3 的依据）。\n")
w("## 3. 逐条出处与交叉核对\n")
w("交叉核对 = Wikipedia 条目 infobox `elevation_m` 或导言里的海拔（2026-11-03 经 MediaWiki API 取，`_build/raw/wiki_extracts_2026-11-03.json`）。Peakbagger 对脚本返回 403，未核。差 ≥1% 的加粗；排序一律用 GVP 值。\n")
w("| # | 火山（GVP 号） | 国旗 / 徽章 | GVP 海拔 | Wikipedia | 差 | 最近喷发（GVP） | 图片 |")
w("|---|---|---|---|---|---|---|---|")
for i in items:
    c = i["cross_check"]
    v = "—" if c.get("value") is None else f"{c['value']:,}"
    diff = "—" if c.get("value") is None else f"{c['diff_pct']:+.1f}%"
    if c.get("value") is not None and abs(c["diff_pct"]) >= 1:
        diff = f"**{diff}**"
    img = assets.get(i.get("image"), {})
    lic = img.get("licence", "（无）")
    if i.get("image_risk"):
        alt = assets.get(i.get("image_alt"), {})
        lic = f"风险图 {lic}（仅风险版）；默认版 {alt.get('licence', '?')}"
    w(f"| {i['rank']} | [{i['name']}]({i['source']['url']})（{i['gvp_volcano_number']}） | {i['country_name']}{' / ' + i['badge'] if i.get('badge') else ''} | {i['value_display']} | {v} | {diff} | {i['tags'][0]['text']} | {lic} |")
w("\n备注（逐条 notes 见 `data.json`）：")
w("- San José：GVP WFS 字段 6,070 m 是邻峰 Marmolejo 的高度；GVP 地质概述与 Wikipedia 都是 5,856 m，已改用 5,856 m 并重排为 #24（审片问题 1）。")
w("- Guayaques：GVP 5,598 m，Wikipedia 5,076 m（−9.3%）；按 Wikipedia 值会掉出前 50。差异接近 bible §3.4 的 10% 阈值，列入待用户确认。")
w("- Peinado：GVP 5,741 m，Wikipedia 5,890 m（+2.6%）。")
w("- Pico de Orizaba：GVP 5,564 m，Wikipedia 5,636 m（+1.3%）；Mount Damavand：GVP 5,670 m，Wikipedia 5,610 m（−1.1%）；Ubinas：GVP 5,608 m，Wikipedia 5,672 m（+1.1%）。")
w("- Pular、Olca-Paruma、Nevados Casiri、Yucamane、Corrida de Cori：Wikipedia 未给数值，只有 GVP 一源。")
w("- 边界：Ticsani（GVP 5,382 m，第 51）在 Wikipedia 写 5,408 m，按 Wikipedia 会超过 Popocatépetl（5,393 m）。单一来源排序下边界不受影响。\n")
w("## 4. 洞察卡核对\n")
w("| after | 文字 | 依据 |")
w("|---|---|---|")
basis = {
    43: "措辞改为「不在 GVP 近 11,700 年活动火山名单上」（审片问题 9）。GVP Pleistocene 表 222150 Kilimanjaro（5,881 m，无 Holocene 喷发记录）；Holocene 表里没有 Kilimanjaro。Holocene 起点约 11,700 年前（GVP 定义）。",
    34: "Guinness World Records「Tallest mountain」：Mauna Kea 从海底基座到峰顶 10,205 m；USGS Mauna Kea 页：从海底基座量是地球最高的山（峰顶 4,207 m）。本榜第 1 名 6,879 m。",
    26: "本表 §2：GVP 国家字段含两国的 18 座（Chile-Argentina 13、Chile-Bolivia 5）；不报国家总数，避免依赖 GVP 字段书写顺序（审片问题 8）。原：Chile 30 座，其中 18 座 GVP 国家字段为 Chile-Argentina（13）或 Chile-Bolivia（5）。",
    18: "GVP Holocene 表 Last_Eruption_Year = 2026 的有 Sabancaya（5,960 m）、Láscar（5,592 m）、Popocatépetl（5,393 m）；Sabancaya 最高。GVP 周报 2026-01-08/14：IGP 报告持续喷发；2026-05 仍有爆炸与灰柱（秘鲁媒体 / VAAC，二手）。",
    9: "2016 年 2 月法国–厄瓜多尔联合测量（IRD / Géoazur 与厄瓜多尔 IGM），峰顶距地心 6,384.4 km，为地表离地心最远点（El Universo 2016-04-07；Wikipedia Chimborazo）。本榜按海拔排第 8。",
    3: "不点名（审片问题 7）。GVP：Ojos del Salado 最近喷发 750 CE（± 250 年，Eruption Dated）；Llullaillaco 1877（Eruption Observed），都在 2,000 年内。",
}
for x in d["insights"]:
    w(f"| {x['after_rank']} | {x['text']} | {basis.get(x['after_rank'], '')} |")
w("\n## 5. 图片许可\n")
w("找图过程（follow-up 016 / 023 与追加要求 3–5）：①每项内容先落盘 `_build/content/`；②Codex 联网搜两轮（`codex_b*.json`、`codex_bR1_*.json`，follow-up 023 起停用）；③Claude 自己搜：Pexels 网页搜索（`claude_pexels_all.json`）、Bing 图片全网检索（`claude_bing_all.json`）、低清项再全网升级一轮（`_build/upgrade/`）；Flickr 可商用搜索因限流降级，结果未采用；Openverse / Unsplash 搜索页被拦；④全网都没有可商用图的项，默认版用 Codex 生成图（`tools/codex_image.py`，prompt 在 `_build/gen_prompts/`）。不用维基共享资源与 GVP 图库（CC BY-NC）。")
dflt = [(i.get("image_alt") if i.get("image_risk") else i["image"]) for i in items]
dc = Counter("AI 生成" if assets[f]["licence"].startswith("AI") else assets[f]["licence"] for f in dflt)
rc = Counter("AI 生成" if assets[i["image"]]["licence"].startswith("AI") else ("风险图" if i.get("image_risk") else assets[i["image"]]["licence"]) for i in items)
w("- 默认母版：" + "、".join(f"{k} {v}" for k, v in dc.most_common()) + "。NASA 图为 ISS 宇航员 / Earth Observatory 公有领域照片（审片修复 4），按看图确定的火山位置裁切。")
w("- `_with-risk-images` 版：" + "、".join(f"{k} {v}" for k, v in rc.most_common()) + "（风险图 = 许可不明或来源页写明保留所有权利，或 Pixnio 不在白名单；须用户发布前签字）。")
w("- 审片修复（2026-11-04）：#14 San José 改用 GVP 地质概述的 5,856 m 并重排；#25 Cordón de Puntas Negras 原风险图实为 Miscanti，已撤，两版都用生成图；Licancabur 换成以 Licancabur 为主体的 Pexels 图。")
w("- 复核小修（2026-11-04）：ISS 俯视图认不出火山的卡改用地面实拍——#1 Ojos del Salado、#2 Llullaillaco、#5 Coropuna、#12 Aracar、#13 Guallatiri 用 Flickr CC BY / CC BY-SA 实拍（单线程、3 s 间隔检索，逐张看图认对）；#6 El Cóndor、#9 Pular 没找到地面实拍，默认版改回生成图；保留 NASA 的是 #7 Parinacota（斜视）、#40 Ubinas（喷发灰柱）、#48 Tata Sabaya（锥体 + 崩塌丘）。#4 Incahuasi、#23 Taapaca、#44 Isluga 的生成图重出（去掉村庄 / 教堂，外形按真山特征）。")
w("- 逐张许可、作者、来源页见 `assets.json`；描述框署名由 `python -m rank_scroll publish` 生成。")
lic = Counter((a.get("licence") or "?") for f, a in assets.items())
w("- 许可分布：" + "、".join(f"{k} {v}" for k, v in lic.most_common()))
(EP / "sources.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("ok", len(L))
