# -*- coding: utf-8 -*-
"""data.json + assets.json + items_def.EXCLUDED → sources.md（逐条出处、交叉核对、争议、洞察依据、图片许可）。"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
EP = HERE.parent
sys.path.insert(0, str(HERE))
from items_def import EXCLUDED  # noqa: E402

d = json.loads((EP / "data.json").read_text(encoding="utf-8"))
assets = {a["file"]: a for a in json.loads((EP / "assets.json").read_text(encoding="utf-8"))}
L = []
w = L.append
w("# ep15 · 数据出处、交叉核对与许可（sources.md）\n")
w("> 2026-11-03 代理整理（用户授权自主决策）。本文件由 `_build/gen_sources.py` 生成；改数据请改 `_build/items_def.py` → `build.py` → `gen_sources.py`。"
  "原始抓取在 `_build/raw/`（Wikipedia wikitext 带 revid、ILEC 数据册页、论文 PDF/全文抽取）。所有网页取数日期 2026-11-03。\n")
w("## 1. 口径\n")
w("- **榜单**：天然湖泊按**最大水深**（米，降序；副显示英尺 = 米 × 3.28084 四舍五入）排序，收**最大水深 > 400 m** 的全部湖泊，共 "
  f"{len(d['items'])} 个（N 由可靠数据决定，不凑数；400 m 与 Wikipedia「List of lakes by depth」收录门槛一致，便于核对）。")
w("- **收**：天然湖，含被小坝略抬高水位的天然湖（Lake Chelan，1927 年坝抬高约 6.4 m）；含里海（地理学与该列表通行把它当作内陆咸水湖）。")
w("- **不收**：水库；**冰下湖**（Vostok 等，无开放水面，测深为地震波推算 510–900 m，口径不同）。")
w("- **取值规则**：① 优先**最新的同行评审测深**或主管机构 / 国家项目数据（primary）；② 没有时用 Wikipedia 条目所引的学术或机构来源（记「经 Wikipedia 转引」）；"
  "③ 只有无出处数值的标 aggregator 并在 notes 写明；④ 每条都与第二来源交叉核对，差异 > 0.5% 或影响名次的写进 notes；⑤ 来源互相矛盾时取最新实测，卡上标 `DEPTH DISPUTED` 或用标签写出旧值。")
w("- **同值同名次**（1,1,3 式）：505 m（Toba / Sarez）、460 m（Cochrane / Tinn）、453 m（Chelan / Mjøsa）、425 m（Como / Te Anau）；同名次内按英文名字母序。")
w("- **湖底高程标签**（Floor … below/above sea）= 湖面海拔 − 最大水深，四舍五入到整米（.5 远离零）；湖面海拔来源逐条见 §4。")
w("- **显示**：`value_display` 整米；Lago Viedma 为论文原文「∼750 m」，屏上写 `~750 m`。\n")
w("## 2. 国家归属、国旗与大洲（待用户复核）\n")
w("| 议题 | 本期做法 | 依据 |\n|---|---|---|")
w("| 跨国湖国旗 | 按**湖面面积占比最大**的国家；无公认水面划分的（里海）按**湖岸线最长**的国家。徽章：两国写 `SHARED WITH X`，三国以上写 `SHARED BY N COUNTRIES` | 用户建议口径 |")
w("| Tanganyika | 刚果（金）45%（14,800 km²）> 坦桑尼亚 41% > 布隆迪 8% > 赞比亚 6% → DR Congo 国旗 | FAO LTR 项目表；Wikipedia 写坦 46% / 刚 40%，与一手项目表不符，不用 |")
w("| 里海 | 无水面划分（2018 公约未划海床）；哈萨克斯坦湖岸 2,340 km / 约 7,000 km，最长 → Kazakhstan 国旗；大洲记 Asia（5 个沿岸国中 4 个属亚洲，湖跨欧亚分界） | oq.gov.kz |")
w("| Malawi | 马拉维管辖大部分水面，最深点在其西岸外；马坦边界有争议 → Malawi | ILEC、Wikipedia |")
w("| O'Higgins/San Martín | 智利 554 km² > 阿根廷 459 km² → Chile | 西语 Wikipedia |")
w("| General Carrera/Buenos Aires | 智利 978 km²（52.8%）> 阿根廷 872 km² → Chile | 西语 Wikipedia 引 Muñoz et al. 2006 |")
w("| Cochrane/Pueyrredón | 智利 175 km² > 阿根廷 150 km² → Chile | Wikipedia |")
w("| Kivu | 刚果（金）：惯例与常见描述中占比较大，**未找到可核的面积划分** → 待确认 | 惯例 |")
w("| Superior | 美国：惯例与常见描述中占比较大，**未逐项核面积划分** → 待确认 | 惯例 |")
w("| Viedma | 湖在阿根廷境内（西岸冰原段边界未定）→ Argentina，不加 SHARED | Wikipedia |")
w("| Tahoe | 加州 / 内华达两州，同一国，不加徽章 | — |")
w("| 大洲（计分板） | 按湖所在位置；结果 " + ", ".join(f"{k} {v}" for k, v in sorted(
    {c: sum(1 for i in d['items'] if i['continent'] == c) for c in {i['continent'] for i in d['items']}}.items(), key=lambda kv: -kv[1])) + " | data.json |\n")
w("## 3. 入榜边界与排除\n")
w("- 第 35 名 Lake Superior 406 m（US EPA 1,333 ft；ILEC 406 m）。门槛 400 m 以下最近的是 Lake Poso 395 m、Lake Hāwea 392 m、Lake Wakatipu ~380 m。")
w("- 2026-11-04 独立审片（qc.md B1）：Lake Wakatipu 原按 Wikipedia 420 m 收为 #33，该值无引注；LINZ 海图 NZ 252 为 376 m、MfE/LAWA 与 NZJMFR 1970 为 380 m、Britannica 378 m → 移出榜单，N 由 36 改为 35。")
w("- 下列湖或数据被排除 / 改正：\n")
w("| 湖 | 值 | 处理 |\n|---|---|---|")
for n, v, why in EXCLUDED:
    w(f"| {n} | {v} | {why} |")
w("\n- Wikipedia 列表（rev 1371850291）> 400 m 的 39 行里：去掉 Vostok（冰下湖）、Poso（新测 395 m）、Fagnano（实测 206 m），并改正 O'Higgins（列表已是 799）、Argentino（719 → 607）；Wakatipu（420 → ~380）出榜。\n")
w("## 4. 逐条出处与交叉核对\n")
w("差异 = |value − cross| / value。tier：primary = 测深论文 / 主管机构 / 国家项目；aggregator = 二手整理（屏上照常显示，notes 说明）。\n")
w("| # | 湖 | 国旗 | value (m) | 主值来源（tier；测量方式与年份） | 交叉核对 | 差异 % | 湖面海拔 | 备注 |\n|---|---|---|---|---|---|---|---|---|")
for it in d["items"]:
    s, x = it["source"], it["cross_check"]
    w(f"| {it['rank']} | {it['name']} | {it['country_name']} | {it['value']} | [{s['name']}]({s['url']})（{s['tier']}；{s['method']}） | "
      f"[{x['name']}]({x['url']}): {x['value']} | {x['diff_pct']} | {it['surface_m']} m（{it['surface_source']}） | {it['notes']} |")
w("\n## 5. 洞察卡与标签的依据\n")
w("| 洞察 / 标签 | 依据 |\n|---|---|")
w("| after 30：Poso 450 → 395 m、Wakatipu 420 → ~380 m | Poso：Tournier et al. 2025, *Sedimentologika* 正文 §4.1 \"maximum depth of 395 m\"（2022 年 11 月 Kongsberg EM2040 多波束），正文 PDF `_build/raw/poso_tournier2025_main.pdf`（oap.unige.ch 1604/2249；`poso_tournier2025.txt` 是补充材料）。Wakatipu：见 §3 |")
w("| after 17：Sarez 1911 年地震滑坡堵河成湖 | Wikipedia「Sarez Lake」：\"The lake formed in 1911, after a great earthquake, when the Murghab River was blocked by a big landslide\"（Middleton & Thomas） |")
w("| after 11：前 10 名有 3 个巴塔哥尼亚冰川湖，冰川仍在后退 | 前 10 名中 O'Higgins、Viedma、Argentino；Minowa et al. 2023 记录 O'Higgins、Viedma、Upsala 冰川后退及湖盆随之露出 |")
w("| after 6：Viedma 2022 年报 900 m（未发表），同行评审测深约 750 m | CONICET 2022-07-21 新闻稿（±3%，未见同行评审发表）；Minowa et al. 2023（测深 2017-01 至 2020-06）\"The deepest part of the lake was ∼750 m deep\" |")
w("| after 2：下一张冠军湖储有世界约 20% 未冻结淡水（悬念式，不点名） | UNESCO 世界遗产 754：\"It contains 20% of the world's total unfrozen freshwater reserve.\"（`_build/raw/web/unesco_754.html`） |")
w("| Floor 标签（如 Baikal 1,187 m below sea、Sarez 2,758 m above sea） | 湖面海拔 − 最大水深，见 §4 湖面海拔列 |")
w("| Deepest in N. America（Great Slave） / Deepest in Europe（Hornindalsvatnet） / Deepest in New Zealand（Hauroko） / Deepest in Japan（Tazawa） | Canadian Encyclopedia；Wikipedia 各条目首段（Hornindalsvatnet 引 SNL；Hauroko 引 Southland Times 2014；Tazawa 条目） |")
w("| Largest lake on Earth（Caspian） / Largest freshwater area（Superior） / Largest wholly in Canada（Great Bear） / Norway's largest lake（Mjøsa） | Wikipedia 各条目首段；ILEC Great Bear / Mjøsa 数据册 |")
w("| Supervolcano caldera（Toba） | Wikipedia「Lake Toba」：\"The lake is the massive caldera of the Toba supervolcano\" |")
w("| Survey 2020 (was 836 m)（O'Higgins） / Often listed as 719 m（Argentino） / Often listed as 702 m（Issyk-Kul） / Echo sounding (was 464)（Salvatnet） / USGS survey 2000（Crater） / Sonar map 2002（Baikal） / Survey 1946–47（Tanganyika） | 见 §4 对应行 method 与 notes |")
w("\n## 6. 争议与待复核（发布前 7 天内再核）\n")
w("1. **Lago Viedma** 750 vs 900 m：若 900 m 有同行评审发表，Viedma 升到第 4，洞察卡与 DEPTH DISPUTED 徽章需改。")
w("2. **Lago Argentino** 607 vs 719 vs 500 m：采用同行评审测深 607 m（第 9）；若 719 m 来源找回且可信，升到第 6。")
w("3. **Lake Toba** 505 vs 529 m（ILEC）：取 529 则升到第 13。")
w("4. **Lake Kivu** 475–485 m：取 485 与 Salvatnet（482）互换。")
w("5. **Adams Lake** 457 vs 397 m：取 397 则出榜。**Lake Wakatipu** 已按审片出榜（见 §3）。")
w("6. **Sarez Lake** 505 m 无一手出处（「约 500 m」）。**Nahuel Huapi** 464 / 454 / 438 m。**Great Slave** 614 m 可能偏小（深槽或再深 ~30 m）。")
w("7. 搜索预算：本期调研中途 WebSearch 共享额度用尽，此后只用直连抓取（WebFetch / curl 已知地址）核对；未能直接打开的一手文献（Murdie 1999、Crowe 2008、Petticrew 2015、Seppälä 2005、NVE 1984 图）均记为「经 Wikipedia 转引」。\n")
w("## 7. 图片许可\n")
w("- 2026-11-04 审片 M3：来源页明写版权所有的 4 张（#3 Caspian Tour-Mangystau、#4 O'Higgins gochile.cl、#22 Cochrane gochile.cl、#28 Great Bear dstewartfishing.com）已从风险版撤下，两版都用默认图；其余许可不明的照片只进风险版，卡面署名只写作者或来源站名。")
w("- 生成图（licence = AI-generated (Codex image_gen)）为本片生成，非真实照片，卡面标 \"AI-generated image (not a photo)\"。")
w("- 2026-11-04 审片 B2 / M1：#5 Viedma 改用 Flickr「Glacier Viedma and Lago Viedma」（Su--May，CC BY 2.0，游船上拍 Viedma 冰川前缘与湖面）；#8 Great Slave 默认版改用 Flickr「Great Slave Lake in Yellowknife」（Alan Sim，CC BY-SA 2.0）。\n")
if assets:
    w("| # | 湖 | 文件 | 作者 | 许可 | 来源页 | 备注 |\n|---|---|---|---|---|---|---|")
    for it in d["items"]:
        for key in ("image", "image_alt"):
            a = assets.get(it.get(key) or "")
            if a:
                tag = "（默认版替代图）" if key == "image_alt" else ("（风险图，仅风险版）" if it.get("image_risk") and it.get("image_alt") else "")
                w(f"| {it['rank']} | {it['name']}{tag} | {a['file']} | {a.get('author','')} | {a.get('licence','')} | {a.get('source_page','')} | {a.get('selected_by','')} {a.get('fop_note','')} |")
else:
    w("（尚未选图）")
(EP / "sources.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("sources.md", len("\n".join(L)))
