# -*- coding: utf-8 -*-
"""data.json + assets.json + 下列固定章节 → sources.md。改数据请改 items_def.py 后重跑 build.py → gen_sources.py。"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parent
data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
assets = {a["file"]: a for a in json.loads((EP / "assets.json").read_text(encoding="utf-8"))}

HEAD = """# ep13 · 数据出处、交叉核对、全景自由与图片许可（sources.md）

> 2026-11-03 代理整理（follow-up 015，用户授权自主决策）。本文件由 `_build/gen_sources.py` 从 `data.json` / `assets.json` 生成；改数据请改 `_build/items_def.py` 后重跑 `build.py` → `gen_sources.py`。调研原料：`_build/raw/`（维基表 wikitext、Commons 各国 FoP 规则页、维基摘要），每项内容摘要 `_build/content/`。

## 1. 口径

- **榜单**：世界上已建成的雕像，按**雕像本体高**降序，收录所有能核实到的本体 ≥ 49 m 的雕像，共 41 尊。
- **本体高**：形象从脚底（或坐像底面）到形象最高点，含手持物（伏尔加格勒「祖国母亲在召唤」的剑、自由女神的火炬同理）；不含莲花座 / 宝座 / 基座 / 内含建筑 / 山体。含基座总高另在卡片标签上写「… m with base」，`data.json` 字段 `total_height_m`。
- **为什么不用「含基座」**：基座高度差别极大（统一像 58 m 基座、春泉大佛 100 m 叠台、炎黄二帝 55 m 山体），比较的是「人造台子」而不是雕像；本体口径与维基表的大部分条目、Guinness 的「最高雕像」一致。维基表本身口径不统一：春泉大佛 128 m 含 20 m 莲花座，拉开坤 115.8 m 不含 13.4 m 莲花座。本期统一不含：春泉大佛 108 m，因此排第 3（含莲花座统一算则 128 vs 129.2，拉开坤仍在前）。
- **只收已建成**：在建 / 规划不收（孟买 Ambedkar 像 2026 年 11 月仍在建；柬埔寨 Bokor 108 m 大佛预计 2027；越南广义观音、泰国纳黎萱王像、Maha Sarakham 坐佛等在建）；已拆不收（荆州关公 2021–22 拆除迁移；巴米扬大佛 2001 年被毁）。
- **不收**：按长度计的卧像（江西弋阳卧佛 416 m 长）、浮雕、塔中佛像（室内）。胸像算雕像（炎黄二帝）。
- **同高同名次**（1,1,3 式），同名次内按 data.json 顺序稳定。
- **国家** = 雕像所在地；香港计入中国（同 ep01）；台湾单列。
- **显示**：`value_display` 取 3 位有效数字（≥ 100 m 取整米；带小数的来源值保留 1 位），`secondary_display` = 米 × 3.28084 取整英尺。
- **来源分级**：每条主值至少一个非维基来源（建设方行业刊物、官方 / 政府旅游机构、新闻、百科出版物，个别只有旅游网站——表中照写）；维基表（rev 1382307847，2026-10-27）只作交叉核对。差异 > 10% 写进备注。

## 1b. Statue of Belief 口径修正（2026-11-04，qc #6）

- 揭幕新闻一律写「369 ft」；维基正文：overall statue 369 ft (112 m)、pedestal 110 ft (34 m)；The Daily Guardian：「34 m high pedestal, reaches a height of 112 m」。369 ft 是含台座的总高。
- 施工方行业刊物 NBM&CW 2020 年的「351 ft」是施工期的总高；后来在发髻上加了恒河水流造型，总高变为 369 ft（Zee News / Rajasthan Tour Planner）。
- 按本期口径（不含台座），本体 = 369 − 110 = 259 ft = 78.9 m（推算值，两处来源的分项相减），排第 12；维基表的 106 m / 112 m 隐含台座只有 6 m，与 110 ft 台座和 110 ft 观景层矛盾，不采用。
- 片头卖点「the usual No. 2 drops to No. 3」不受影响（春泉大佛第 3，因为莲花座不计）。

## 2. 名单边界：剔除与未收

| 对象 | 维基表值 | 处理 | 原因 |
|---|---|---|---|
| Chao Mae Kuan Im（清莱 Wat Huay Pla Kang 观音） | 69 m | 剔除 | 来源 69 / 79 / 90 m 三说，均为旅游网站，无官方数 |
| 太湖西山观音（苏州大如意圣境） | 67 m | 剔除 | 唯一中文来源写 88 m（未分本体 / 基座），67 m 无出处 |
| Lung Por Tuad（呵叻 Wat Khao Yai） | 59 m | 剔除 | 泰文报道多写 111 m，并有文章质疑；59 m 无出处 |
| Phra Kakusunto（素攀） | 58 m | 剔除 | 旅游指南写 26 m；58 m 只见维基 |
| Bodhi Tahtaung 坐佛（蒙育瓦） | 74 m | 剔除 | 维基同时列在「已建成 2022」与「在建」，未找到完工证据 |
| Mother of All Asia（菲律宾八打雁） | 98.15 m | 剔除 | 98.15 m 含其下台座 / 建筑（Montemaria），本体高未公开；完工年也有 2021 / 未完两说 |
| 慈山寺观音（香港） | 76 m | 剔除 | 70 m 像高含三层莲花座（慈山寺博物馆导览），另有 6 m 花岗岩基座；不含莲座的像身高未公开（qc #7） |
| 开元寺阿弥陀佛（越南河内山西） | 72 m | 剔除 | 72 m 为坐佛连多层台座建筑（内部 13–16 层）的总高，本体高未公开；另有 70 m 说法 |
| 越南 Ba Den 山观音（西宁） | 未收 | 未收 | 72 m 为含莲花座与五层台基的总高，本体高未公开 |
| 佛光山佛光大佛（高雄） | 未收 | 未收 | 本体 40 / 48 / 50 m 说法不一，含建筑 108 m |
| 江西弋阳卧佛 | 68 m | 不收 | 卧像，68 m 是卧姿的高度、416 m 是长度 |
| Our Lady of Mercy（波兰 Konotopie） | 40.6 m | 不够高 | 本体 40.6 m |
| 巴西 Santa Rita de Cássia | 未收 | 不够高 | 本体 42 m（含座 56 m，Correio Braziliense / Audiala） |
| Statue of Liberty | 未收 | 不够高 | NPS：基座顶到火炬 46.05 m（151 ft 1 in）——洞察卡 1 |
| 荆州关公 | 58 m（已拆） | 不收 | 2021-09 起拆除迁移（SCMP）——洞察卡 2 |
| 孟买 Ambedkar 像 | 在建 | 不收 | 2025-12 州政府称 2026 年内完工，至今未揭幕；发布前复核 |

**可能的遗漏**：维基表只收 ≥ 50 m，49–55 m 段落（泰国、中国地方寺院、东南亚新建佛像）可能还有未被任何英文列表收录的雕像。本期补了维基漏收的不丹 Buddha Dordenma（54 m），并核过巴西、印度、墨西哥、日本常见的 40–50 m 级大像（均 < 49 m）。

## 3. 全景自由（FoP）：所在国是否允许商用复制雕塑的照片

依据：Wikimedia Commons「Copyright rules by territory / 国家」FoP 一节（2026-11-03 取，原文存 `_build/raw/fop/`）及其引用的法条。雕像大多是近几十年的作品，雕塑作者仍享有版权；照片的许可（Pexels / CC 等）只解决摄影师的版权，不解决雕塑本身的版权。

| 国家 | 本期件数 | 雕塑商用 FoP | 法律依据 | 处理 |
|---|---|---|---|---|
| 中国 | 12 | ✅ | 著作权法（2020）第 24 条第 1 款第 10 项：对设置或陈列在公共场所的艺术作品进行临摹、绘画、摄影、录像；香港《版权条例》第 71 条 | 照常 |
| 印度 | 2 | ✅ | Copyright Act 1957 s.52(1)(t)：公共场所永久陈列的雕塑可绘画、摄影并发表 | 照常 |
| 泰国 | 5 | ✅ | Copyright Act B.E. 2537 s.39：公共场所永久陈列的艺术品可绘画、摄影、摄像 | 照常 |
| 墨西哥 | 1 | ✅ | Ley Federal del Derecho de Autor Art. 148(VII)：公共场所可见的作品可摄影、视听复制（须注明出处） | 照常 |
| 日本 | 9 | ⚠️ | 著作权法第 46 条：室外永久设置的美术作品可利用，但第 4 项排除「以出售复制品为目的」的复制；Commons 视为 NoFoP | `image_risk` |
| 台湾 | 2 | ⚠️ | 著作权法第 58 条第 4 款，同日本 | `image_risk` |
| 菲律宾 | 1 | ❌ | IP Code（RA 8293）无 FoP 条款；IPOPHL 2021 表示商用需授权 | `image_risk` |
| 缅甸 | 2 | ❌ | Copyright Law 2019 第 24–33 条无 FoP | `image_risk` |
| 印度尼西亚 | 2 | ❌ | 著作权法 2014 无商用 FoP（CC Indonesia 2018 声明） | `image_risk` |
| 越南 | 1 | ❌ | 知识产权法 2022 修正（2023-01-01 起）：公共场所艺术作品只可非商业摄影 | `image_risk` |
| 俄罗斯 | 1 | ❌ | 民法典第 1276 条：雕塑为主要对象或用于营利时不适用（Vuchetich 1974 年去世，版权至 2044） | `image_risk` |
| 乌克兰 | 1 | ❌ | 著作权法 2022 第 22 条第 10 项：只限「无独立经济价值」的使用 | `image_risk` |
| 不丹 | 1 | ❌ | Copyright Act 2001 无 FoP | `image_risk` |
| 塞内加尔 | 1 | ❌ | 著作权法 2008 第 46 条：作为主要对象并用于商业时不适用 | `image_risk` |
| （古代作品）乐山大佛 | 1 | ✅ | 713–803 年作品，公有领域 | 照常 |

**默认版的处理（follow-up 016）**：用户要求默认母版每张卡都有图。FoP 风险项默认版用一张可商用许可的照片（`image_alt`），风险版（`_with-risk-images`）用最好的那张（可能许可不明）。注意：`image_alt` 仍然是该雕像的照片，**FoP 风险在默认版并未消除**，只是摄影许可干净；是否发布、是否改用远景 / 占位，需用户在发布前决定。

**2026-11-04 主代理决定（qc 必须修）**：雕塑 FoP 安全的国家（中国、泰国、墨西哥）里找不到可商用实拍的项，默认版改用 Codex 生成的写实图（`tools/codex_image.py`，无人物 / 文字 / 横幅，渲染器自动标 AI IMAGE）；其中炎黄二帝、赤山明神两项的风险版原图（真人合影带横幅 / 来源页保留权利）也一并换成生成图。日本、台湾、缅甸、印尼、菲律宾等国许可不明的项默认版维持占位，原因写「licence unclear」；风险版里来源页明写 All rights reserved 的图（东京湾观音、The Victor 原图）已换成许可不明的其他图。

"""

INS = """## 5. 洞察卡依据

| after | 文字 | 依据 |
|---|---|---|
| 37 | The Statue of Liberty is 46 m from base to torch: too short to make this list. | NPS Statue Statistics：Top of base to torch 151'1" = 46.05 m（https://home.nps.gov/stli/learn/historyculture/statue-statistics.htm）；本榜第 41 名 49 m |
| 28 | China now curbs statues over 30 m. Jingzhou took down its 58 m Guan Yu in 2021-22. | 人民日报客户端 2020-10（剑河仰阿莎争议报道引住建部通知：严格控制高度超过 30 m 或宽度超过 45 m 的大型雕塑）；SCMP 2021：荆州 57.3 / 58 m 关公像违反古城限高，耗资 1.55 亿元迁移，2021-09 起拆除（https://scmp.com/news/china/article/3116103/）；拆除完成于 2022 上半年（多源） |
| 20 | Japan has 9 statues on this list, but the newest of them went up back in 1994. | data.json：日本 9 项建成年 1961–1994，最新为小豆岛大观音 1994 |
| 11 | 4 statues here were unveiled since 2022: in India, Thailand, the Philippines, Indonesia. | Statue of Belief 2022-10-29（ThePrint；本体 78.9 m 由总高 369 ft − 台座 110 ft 推得）；Wat Paknam 大佛 2023-02-05 御临开光（Sino Sculpture / Khaosod）；The Victor 2023-08（Inquirer）；Sibea-bea 耶稣像 2024-09（The Star） |
| 4 | Spring Temple Buddha is often listed at 128 m. That includes its 20 m lotus throne. | 郑州晚报 2013-05-28：佛身 108 m + 莲花座 20 m；维基与多数榜单写 128 m |
| 2 | Next: the Statue of Unity, 66 m taller than any other statue on Earth. | 182 − 115.8 = 66.2 m（BBC；拉开坤见第 2 名出处） |

## 6. 竞品

| 视频 | 频道 | 播放 | 时间 | 口径 |
|---|---|---|---|---|
| ◄ Tallest statue size comparison ► 3d animation | Real Data | 约 5,828 万 | 约 2021（Artribune 2022-01 报道） | 3D 体量对比，数值取维基、本体 / 含基座混用（如自由女神 93 m 含基座） |
| World Tallest Statues size Comparison \\| Upcoming Tallest Statues | WorldTV Studio | 约 1,790 万 | 未取到 | 3D 体量对比，含在建 |

需求数据：`ai_videos/paihangbang/0_research/data/yt_demand_2026-11-03.jsonl`（「tallest statues in the world」前 15 条中位数 1,449,466，最高 58,284,039）。
"""


def main() -> None:
    rows = ["## 4. 逐条出处与交叉核对", "",
            "差异 = |本期值 − 维基表值| / 本期值。所有条目 retrieved_at = 2026-11-03。FoP 列：ok / risk / pd。", "",
            "| # | 雕像 | 国家 | 本体 m | 含基座 m | 主值来源 | 维基表 | 差异 % | FoP | 备注 |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    for it in data["items"]:
        cc = it.get("cross_check") or {}
        rows.append(f"| {it['rank']} | {it['name']} | {it['country_name']} | {it['value']} | {it.get('total_height_m') or '—'} | "
                    f"[{it['source']['name']}]({it['source']['url']}) | {cc.get('value', '—')} | {cc.get('diff_pct', '—')} | "
                    f"{it['fop']} | {it['notes'].replace('|', '/')} |")
    img = ["", "## 7. 图片许可（assets.json 摘要）", "",
           "| # | 雕像 | 默认版用图 | 许可 | 风险版用图 | 许可 | 说明 |", "|---|---|---|---|---|---|---|"]
    for it in data["items"]:
        a = assets.get(it.get("image", ""), {})
        alt = assets.get(it.get("image_alt", ""), {}) if it.get("image_alt") else {}
        if it.get("image_risk"):
            d_file, d_lic = (it.get("image_alt", "（占位）"), alt.get("licence", "")) if it.get("image_alt") else ("（占位）", "")
            r_file, r_lic = it.get("image", ""), a.get("licence", "")
        else:
            d_file, d_lic, r_file, r_lic = it.get("image", ""), a.get("licence", ""), "同左", ""
        note = (it.get("image_risk") or "")
        img.append(f"| {it['rank']} | {it['name']} | `{d_file}` | {d_lic} | `{r_file}` | {r_lic} | {note} |")
    text = HEAD + "\n".join(rows) + "\n\n" + INS + "\n".join(img) + "\n"
    (EP / "sources.md").write_text(text, encoding="utf-8")
    print("sources.md written", len(text))


if __name__ == "__main__":
    main()
