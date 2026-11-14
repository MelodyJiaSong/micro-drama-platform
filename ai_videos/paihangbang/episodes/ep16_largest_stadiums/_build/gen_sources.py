# -*- coding: utf-8 -*-
"""data.json + assets.json → sources.md（逐条出处、交叉核对、FoP、图片账本）。python _build/gen_sources.py"""
from __future__ import annotations

import json
from pathlib import Path

B = Path(__file__).resolve().parent
EP = B.parent
data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
assets = {a["file"]: a for a in json.loads((EP / "assets.json").read_text(encoding="utf-8"))}


def cell(s) -> str:
    return str(s if s is not None else "").replace("|", "/").replace("\n", " ")


HEAD = """# ep16 · 数据出处、交叉核对与许可（sources.md）

> 2026-11-03 代理整理（用户授权自主决策）。本文件由 `_build/gen_sources.py` 从 `data.json` / `assets.json` 生成；改数据请改
> `_build/items_def.py`（选择与覆盖）或 `_build/research/{us,world}.json`（原始调研记录，含每条的其他版本数字），再跑 `build.py` → `gen_sources.py`。

## 1. 口径

- **榜单**：当前开放使用的体育场（足球、美式足球、板球、橄榄球、盖尔式足球、多用途），按**当前官方座位容量**降序取前 50。统计期：2026 年 11 月（美国大学球场取 2026 赛季官方数）。
- **只算座位**：站票区、临时看台、草坪区之外的扩容、纪录上座都不算。所以：
  - MCG 官方总容量 100,024 = 95,000 座位 + 约 5,000 站位，取 **95,000**（MCG Ticket Information）。
  - Signal Iduna Park（总 81,365，全座位 66,099）、Croke Park（82,300 含 Hill 16 站台，座位约 69,100）、Allianz Arena（75,024 含站票，全座位 70,000）按座位数都跌出前 50。
  - Clemson 81,500 是官方口径，含 Howard's Rock 一侧的草坡座区（约 4,000 人，Clemson 官网历史页说明）；草坡属于常设观众区，照官方数收录，`notes` 写明。
- **不收**：赛车场、赛马场（站票为主；Indianapolis Motor Speedway 约 235,000 座，Guinness World Records）；已拆除 / 关闭重建 / 在建的（Shah Alam 2020 关闭已拆；King Fahd Sports City 关闭重建；Grand Stade Hassan II、King Salman Stadium、广州足球公园在建）；**只部分重开的 Camp Nou**（2026-03 起可用 62,652 座，完工约 105,000，按当前可用数排不进前 50；洞察卡说明）。
- **国家** = 球场所在地；计分板按国家累计。
- **显示**：容量是精确计数，屏上显示完整整数（不按 bible §3.4 取 3 位有效数字——取整会把 102,733 / 102,321 / 102,041 并成同一个数，失去排名依据）；单位行 "seats"。北朝鲜五一体育场为外界估算，单位行写 "seats, est."。
- **同容量同名次**（标准竞赛排名 1,1,3）：82,000（JIS、Twickenham）并列 28；80,000 五座并列 36；同名次内按名称字母序。
- **D2 变化**：徽章标 2024–2026 的容量变化或新开 / 重开（NEW 2024、REOPENED 2026、RENOVATED 2025、EXPANDED 2024、±N SEATS），依据见各条 `notes` 与 `research/*.json` 的 `change_note`。

## 2. 争议与判断（待用户复核）

| 议题 | 本期做法 | 依据 |
|---|---|---|
| 朝鲜五一体育场 | 114,000，屏上 "seats, est."，徽章 ESTIMATE | 2014–15 改建后朝方未公布座位数；150,000 为改建前旧数；Wikipedia 113,281、StadiumDB 约 114,000，均为外界估算 |
| Beaver Stadium | 106,304（2025 赛季官方数，Georgia 2026 媒体指南「Top 10 Largest On-Campus Stadiums」），徽章「2025 OFFICIAL FIGURE」，并加洞察卡说明 2026-10-10 上座 114,419 | 2026 加了临时西侧上层看台，校方口头称约 108–109k，未公布官方数；若按 2026 实况可能超过 Michigan |
| Ohio Stadium | 102,041（2026 game notes），比 2025 的 102,780 少 739 | 2026 南端区加 field-level suites |
| Bernabéu | 78,297（2030 世界杯申办书 / FIFA 2024 场馆评估，经 StadiumDB 2026-03 文章转述） | 皇马未公布改建后座位数；LaLiga 2023 的 83,186 是施工中「技术容量」；2025/26 联赛最高上座 78,107 与 78,297 吻合 |
| Estadio Azteca | 87,500（AP 2026-03 重开报道） | 官网 403；Wikipedia 87,523 为 2018 旧数；IQ Magazine / StadiumDB 约 90,000、墨西哥城官方场馆页 87,000（取任一都仍是第 21 名） |
| Camp Randall | 76,130（Wisconsin 2026 game notes 年表 2026 行；徽章「+100 SEATS IN 2026」= 对比年表 2025 行 76,030） | 同文件 Quick Facts 写 76,057、正文 76,030（旧值）；第 51 名 Empower Field 76,125 只差 5 座，**第 50 名对此敏感** |
| Notre Dame | 77,622（2017 Campus Crossroads 后） | 官网设施页仍写 80,795（2001–2016 旧值） |
| Nebraska | 85,458（2017 起） | 官网另有「beyond 85,000」与 2024 新闻稿 82,841 两种口径；2026 赛季后大改建，2027 约 65,000 |
| Arrowhead | 76,416（Wikipedia 引 Chiefs 2025 media guide） | Wikipedia 列表页 76,640、StadiumDB 73,426，都不影响入榜 |
| Misr Stadium | 93,940（StadiumDB；无埃及官方页） | 2024-03-22 正式启用 |
| Borg El Arab | 86,000（常用数） | 承建商 Arab Contractors 项目页写 "around 80,000"；取 80,000 则落到并列第 36 |

## 3. 全景自由（FoP）核查

依据 Commons:Freedom of panorama 总表「Buildings」栏（2026-11-03 读取）与各国 Copyright rules by territory 页；图片本身不取自 Commons，但建筑著作权问题与图片来源无关，所以照 ep01 惯例按所在国标 `image_risk`。

| 国家 | 本期球场 | 建筑 FoP（商用） | 依据摘要 |
|---|---|---|---|
| 美国 | 25 | ✓ | 17 USC §120(a)：从公共场所可见的建筑可自由拍摄 |
| 印度 | 1 | ✓ | Commons 表 ✓（Copyright Act s.52(1)(s)） |
| 朝鲜 | 1 | ✓ | Commons 表 ✓，{{FoP-North Korea}}；朝鲜著作权法未把建筑列为作品（Commons 页注） |
| 澳大利亚、英国、西班牙、墨西哥、马来西亚、俄罗斯、秘鲁、中国、土耳其 | 各 1–3 | ✓ | Commons 表 ✓ |
| 阿根廷 | 1 | ✓（事实上） | 法律无 FoP 条款，Commons 依学说（Emery）认定建筑可拍摄商用，{{FoP-Argentina}} |
| **南非** | FNB Stadium | ✗ | Copyright Act 1978 s.15(3) 只豁免电影与广播收录，不含照片；Commons 标 "Not OK for architecture" |
| **埃及** | Misr Stadium、Borg El Arab | ✗ | Commons 表 ✗（Law 82/2002 仅个人使用） |
| **卡塔尔** | Lusail Stadium | ✗ | Commons 表 ✗ |
| **印度尼西亚** | JIS、Gelora Bung Karno | ✗ | 2014 著作权法第六章无商用豁免；第 43(d) 条仅非营利 |
| **法国** | Stade de France | ✗ | Commons 表 ✗（2016 年起仅限个人非营利） |
| **刚果（金）** | Stade des Martyrs | ✗ | Commons 表 ✗ |
| **伊朗** | Azadi Stadium | ✗ | Commons 表 ✗ |

FoP 风险图处理：风险照（`image`，带 `image_risk`）只进 `_with-risk-images` 版；默认母版用 `image_alt`（契约 v1.4）。FoP 国默认版（QC 第 1 轮后）：不以建筑为主体的可商用实拍——FNB 用 CC BY 球迷持国旗、Stade des Martyrs 用 CC BY-SA 场内仪式人群、GBK 用 CC BY-SA 持旗运动员；Lusail、Stade de France、Azadi 用 Codex 生成的「看台球迷背影」示意图（带 AI IMAGE 角标，不复现真实建筑）；Misr、Borg El Arab、JIS 用无图卡「Photo withheld: no freedom of panorama」。另有 3 座（广东奥体、杭州奥体、Atatürk）所在国有全景自由，但全网（Flickr CC 单线程补搜、Bing 可商用过滤、Unsplash / Pexels）都没找到可商用实拍，主代理定（用户要求每张卡有图）：默认版用 Codex 按资料描述生成的球场外观图（带 AI IMAGE 角标，账本 AI-generated），实拍只进风险版。

## 3b. 图片来源分布

- 找图：先 Flickr 公开搜索（只收 CC BY / BY-SA / CC0 / PD），被限流后改 Bing 图片（可商用许可过滤 + 放开许可两路），逐张看候选拼图挑选；维基共享资源一律不用。
- 质量优先（follow-up 追加要求 5）：全网最好的图若许可不明，标 `image_risk = licence unknown` 只进风险版，默认版配可商用 `image_alt`；可商用替代找不到的，默认版用 Codex 生成的球迷示意图。
"""


def main() -> None:
    out = [HEAD]
    out.append("\n## 4. 前 50 名边界\n")
    out.append("- 第 50 名 Camp Randall 76,130（2026）。第 51 名起：Empower Field at Mile High 76,125（Wikipedia / Walter P Moore；差 5 座）、"
               "San Siro 75,817（sansirostadium.com）、Bank of America Stadium 75,037、Naghsh-e Jahan 75,000、Cairo International 75,000、"
               "Spartan Stadium 74,866、Old Trafford 74,158（Premier League 2026/27 手册）、Principality 73,931、Olympiastadion Berlin 73,779。\n")
    out.append("- 若 Camp Randall 按 2025 值 76,030 计，它会和 Empower Field 互换第 50 / 51。\n")
    out.append("\n## 5. 逐条出处与交叉核对\n\n差异 = (cross − value) / value。retrieved_at 均为 2026-11-03。research 原始记录里每条另有 `other_figures`（历史容量、纪录上座、其他口径）。\n\n")
    out.append("| # | 球场 | 国家 | value | 主值来源 | 交叉核对 | 差异 % | 备注 |\n|---|---|---|---|---|---|---|---|\n")
    for it in data["items"]:
        s, c = it["source"], it.get("cross_check") or {}
        cc = f"[{cell(c.get('name'))}]({c.get('url')}): {c.get('value'):,}" if isinstance(c.get("value"), (int, float)) else cell(c.get("name"))
        out.append(f"| {it['rank']} | {cell(it['name'])}（{cell(it['subtitle'])}） | {it['country_name']} | {it['value']:,} | "
                   f"[{cell(s['name'])}]({s['url']}) {cell(s.get('period'))} | {cc} | {c.get('diff_pct', '')} | {cell(it.get('notes'))} |\n")
    out.append("\n## 6. 洞察卡依据\n\n")
    basis = {
        41: "第 36 名并列五座：AT&T Stadium（美国）、Beijing National Stadium、Hangzhou Olympic Stadium（中国）、Stade de France（法国）、Stade des Martyrs（刚果（金）），官方都标整数 80,000（见 §5）。这是标称取整值，不是精确座位数（例：Stade de France 官网写 80,000，常被引用的精确数是 80,698），所以措辞用「list a round 80,000」。",
        5: "Beaver Stadium 2026-10-10 对 USC 上座 114,419，创球场纪录（Penn State 公布、ClutchPoints 报道 https://clutchpoints.com/ncaa-football/penn-state-football-news-nittany-lions-set-beaver-stadium-attendance-record-vs-usc ，Wikipedia infobox 已更新）；2026 赛季加了西侧上层临时看台，校方未公布 2026 官方座位数，所以卡上仍用 2025 官方 106,304，徽章写「2025 OFFICIAL FIGURE」。Penn State 公布的上座数含包厢、记者席、乐队与工作人员。",
        31: "FC Barcelona 官方声明（research/world.json Camp Nou 条）：2025-11 重开约 45,000，2026-03 增至 62,652；完工约 105,000（2027 起）。",
        22: "beIN Sports 2026-06-02 / 2026-05-28：Estadio Azteca 1970、1986、2026 三届世界杯揭幕战，成为首座承办三届揭幕战的球场；2026-03-28 改建后重开（AP）。",
        11: "前 10 名中第 3–10 名均为美国大学橄榄球场（Michigan、Beaver、Kyle、Tiger、Ohio、Neyland、DKR、Bryant–Denny），均非 NFL 主场。",
        3: "朝鲜未公布 2014–15 改建后的座位数；114,000 为外界估算（StadiumDB；Wikipedia 113,281）。",
    }
    for ins in data["insights"]:
        out.append(f"- after {ins['after_rank']}：{ins['text']}\n  - 依据：{basis.get(ins['after_rank'], '')}\n")
    out.append("\n## 7. 图片账本摘要\n\n| # | 球场 | 默认版图片 | 许可 | 风险版图片 / 风险 |\n|---|---|---|---|---|\n")
    for it in data["items"]:
        img = it.get("image_alt") if it.get("image_risk") else it.get("image")
        a = assets.get(img or "", {})
        risk = ""
        if it.get("image_risk"):
            ra = assets.get(it.get("image") or "", {})
            risk = f"{cell(it['image'])}（{cell(ra.get('author'))} / {cell(ra.get('licence'))}；{cell(it['image_risk'])}）"
        page = a.get("source_page") or a.get("commons_page") or ""
        out.append(f"| {it['rank']} | {cell(it['name'])} | {cell(img)} [{cell(a.get('author'))}]({page}) | {cell(a.get('licence'))} | {risk} |\n")
    (EP / "sources.md").write_text("".join(out), encoding="utf-8")
    print("sources.md written")


if __name__ == "__main__":
    main()
