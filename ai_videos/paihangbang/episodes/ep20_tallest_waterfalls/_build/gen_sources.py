# -*- coding: utf-8 -*-
"""生成 ../sources.md（从 data.json / assets.json）。改数据请改 build.py / items_def.py 后重跑 build.py → 本脚本。"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).parent
EP = HERE.parent

HEAD = """# ep20 · 数据出处、交叉核对与许可（sources.md）

> 2026-11-03 代理整理（follow-up 015 / 016）。本文件由 `_build/gen_sources.py` 生成；改数据请改 `_build/build.py` / `items_def.py` 后重跑 `build.py` → `gen_sources.py`。

## 1. 口径

- **榜单**：天然瀑布按**总落差**（total height：最高一级顶 → 最低一级底，含级间急流段）降序，取 ≥ 631 m 的 35 条。
- **主源**：World Waterfall Database（WWD）「Overall Height」榜 https://www.worldwaterfalldatabase.com/tallest-waterfalls/total-height ，2026-11-03 抓取前 3 页（105 条，≥ 549 m）及每条瀑布页（`_build/wwd_crawl.py` → `_build/raw/wwd_top.json`，原始 HTML 在 `_build/raw/wwd/`）。WWD 是私人网站（aggregator 级）；多数高度来自地形图 / 激光雷达估算或其实地三角测量，条目里写明依据。
- **主值覆盖规则**：有公开测量或权威记录的，用它而不用 WWD：
  - Angel Falls：979 m，Guinness World Records（1949 年 National Geographic 资助、Ruth Robertson 带队的测量）。WWD 只记主跌落 807 m（差 −17.6%，>10%，写入 notes，待用户确认）。
  - Yumbilla：895.4 m，秘鲁 IGN 2007 年激光测量（MercoPress 2007-12-04 报道；WWD 也引此数，列 896 m）。
  - 与 WWD 一致、只作佐证的：Gocta 771 m（2006 年 Ziemendorff 与秘鲁政府组织的测量，±13 m）、Yosemite 739 m（1913 年 USGS Matthes 测量；WWD 用 1 m 激光雷达复核）、Tugela 948 m（Guinness 引同一数）、Kukenán 674 m（委内瑞拉国家公园文件，经 WWD 转引）。
- **入选**：① 有名字；② WWD 状态 Cataloged（实地勘测）或 Confirmed 且条目写明高度依据；③ Unconfirmed 只在有独立权威测量 / 记录时收（Tugela、Yumbilla）；④ 水电引水后基本断流的不收。状态定义见 WWD 榜单页 Key。
- **显示**：`value_display` 四舍五入到整米；`secondary_display` = 米 × 3.28084 取整英尺（Yosemite 2,425 ft、Angel 3,212 ft 与官方英尺数一致）。
- **同值同名次**（1,1,3 式），同名次内按名称字母序。
- **季节性**：WWD「Flow Consistency」（一年里有水的月数，**不计冬季封冻**）< 12，或 WWD / Wikipedia 写明只在融雪或雨季有水 → `SEASONAL`；水电调节、每年保证放水 → `HYDRO-REGULATED`；无流量资料 → 不标，notes 写明。
- **国家**：所在地；留尼汪计 France。

## 2. 入选与排除（WWD 前 105 条里 ≥ 631 m 的条目）

| WWD 名次 | 瀑布 | WWD 高度 | WWD 状态 | 处理 | 原因 |
|---|---|---|---|---|---|
| 2 | Mattenbachfälle | 930 | Confirmed | 收 | 2020 年绳降实测 |
| 5 | Haloku Falls（夏威夷） | 887 | Unconfirmed | 不收 | 无独立测量 |
| 6 | Olo'upena Falls（夏威夷） | 878 | Unconfirmed | 不收 | 无独立测量（Wikipedia 列 900 m） |
| 3 | Tres Hermanas（秘鲁） | 914 | Unconfirmed | 不收 | 只有 WWD 数（Mongabay 等也引 WWD），无独立测量 |
| 12 | Los Chorros de Cura（委内瑞拉） | 821 | Unconfirmed | 不收 | 同上 |
| 13 | Pu'uka'oku Falls（夏威夷） | 812 | Unconfirmed | 不收 | 同上 |
| 17 | Mongefossen（挪威） | 773 | Confirmed（hydro） | 不收 | 1977 年并入 Grytten 水电站，WWD：「functionally dry」；洞察卡 3 |
| 21、27 | Unnamed Waterfall ×2（夏威夷） | 756 / 742 | Unconfirmed | 不收 | 无名、未证实 |
| 23 | Terror Falls（新西兰） | 750 | Confirmed | 不收 | 条目只有数字，无依据、无描述 |
| 25 | Helgåfossen（挪威） | 750 | Confirmed | 不收 | 同上，无坐标 |
| 28 | Wailele Falls（夏威夷） | 741 | Unconfirmed | 不收 | 无独立测量 |
| 33 | Mana'wai'nui Falls（夏威夷） | 719 | Unconfirmed | 不收 | 同上（Wikipedia 也标 citation needed） |
| 40 | Drivfoss（挪威） | 700 | Unconfirmed | 不收 | 无独立测量 |
| 41 | Brurasløret（挪威） | 700 | Confirmed | 不收 | 只有一句「700 m（possibly more）」，无依据 |
| 43 | Solitary Falls（新西兰） | 680 | Confirmed | 不收 | 条目只有数字 |
| 47 | Hidden Falls（新西兰） | 660 | Unconfirmed | 不收 | 无独立测量 |
| 51 | Aimoo Falls（夏威夷） | 640 | Unconfirmed | 不收 | 同上 |
| 52 | Brufossen（挪威） | 640 | Confirmed（hydro） | 不收 | 引水后崖面基本无水 |
| 53 | Breiteigsfossen（挪威） | 640 | Confirmed | 不收 | 条目只有数字 |
| 54 | Stäfelifälle（瑞士） | 634 | Unconfirmed | 不收 | 无独立测量 |
| — | Mutarazi Falls（津巴布韦） | 479 | Unconfirmed | 不收 | 常见 762 m；WWD 依高程剖面认为 762 m 是台地边缘到谷底的总落差，记 479 m；洞察卡 2 |
| 55 | Sentinel Fall（美国） | 631 | Cataloged | 收（第 35） | 下一条 Buskefoss 625 m（Confirmed、无依据），再下 Heggurfossen 620 m |

（WWD 名次栏是榜单原始位置；Angel Falls 在 WWD 榜上列第 14、807 m。）

## 3. 逐条主值、交叉核对与流量

"""


def main() -> None:
    d = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    assets = {a["file"]: a for a in json.loads((EP / "assets.json").read_text(encoding="utf-8"))}
    out = [HEAD, "| # | 瀑布 | 国家 | 主值 | 主源 | 交叉核对 | 差异 | WWD 状态 / 流量月数 / 页面更新 | 徽章 |", "|---|---|---|---|---|---|---|---|---|"]
    for it in d["items"]:
        c = it.get("cross_check")
        cc = f"[{c['name']}]({c['url']})：{c['value']} m" if c else "无第二来源（只有 WWD）"
        diff = f"{c['diff_pct']:+.1f}%" if c else "—"
        w = it.get("wwd", {})
        out.append(f"| {it['rank']} | {it['name']} | {it['country_name']} | {it['value_display']}（{it['value']}） | [{it['source']['name']}]({it['source']['url']}) | {cc} | {diff} | "
                   f"{w.get('status','')} / {w.get('flow_consistency') or '—'} / {w.get('updated','')} | {it.get('badge','')} |")
    out += ["", "### notes（逐条判断依据）", ""]
    for it in d["items"]:
        out.append(f"- **#{it['rank']} {it['name']}**：{it['notes']}")
    out += ["", """## 4. 洞察卡依据

| after | 文字 | 依据 |
|---|---|---|
| 30 | SEASONAL = it flows only part of the year, fed by snowmelt or rainy-season runoff. | WWD Flow Consistency 定义（一年有水月数，不计封冻）；14 条 SEASONAL 的月数见 §3 |
| 21 | Zimbabwe's Mutarazi is often listed at 762 m; World Waterfall Database estimates ~479 m. | Wikipedia 列表 762 m、条目 772 m；WWD Mutarazi 页（2025-05-27 更新）记 479 m，理由：762 m 是台地边缘到 Honde 谷底的高程差（Google Earth 高程剖面），WWD 状态 Unconfirmed，所以屏上写成 WWD 的估算（审片第 7 条） |
| 12 | Norway's Mongefossen (773 m) would rank here, but hydropower has kept it dry since 1977. | WWD Mongefossen 页：773 m；1977 年 Mongeelva 并入 Grytten 水电站，此后「functionally dry」。773 m 正好落在第 11（783）与第 12（771）之间 |
| 4 | Next: a Swiss fall that grew 90 m in 2020, when canyoneers abseiled down and measured it. | WWD Mattenbachfälle 页：原估 840 m，2020 年 Vertical Water Canyoning Team 绳降实测约 930 m（+90 m）；Wikipedia 列表仍是 840 m |
| 2 | Angel's 979 m adds rapids below its 807 m drop. Drop those and Tugela (948 m) wins. | Guinness 页：979 m 总落差、807 m 最长单级，「若 Angel 的实际高度只有最初 807 m 那一段，多级的 948 m Tugela 就是最高」（比的是 Angel 807 m 与 Tugela 948 m 总落差，不是单级对单级；2026-11-04 审片第 3 条改措辞）；Wikipedia Angel Falls：979 m 含主跌落下方约 400 m 的斜坡急流；WWD 同论 |

## 5. 许可核实

- **WWD**：`/legal-disclaimer`（2026-11-03 读，存 `_build/raw/wwd_legal.html`）。版权条款只写照片：「All photographs utilized throughout the World Waterfall Database are protected under International Copyright Law … may not be used … without written consent」。对文字与数值没有限制条款；本期只引事实数值（高度、落差、流量月数、状态），不复制描述文字、不用其照片。描述框注明「Heights: World Waterfall Database」。
- **Guinness**：只引纪录数值（事实）。**MercoPress / USGS**：只引数值；USGS 为美国政府公有领域。
- **Wikipedia**：只作交叉核对（CC BY-SA 文字不搬运）。抓取时 query API 多次 429，部分条目只取到 REST 导语，已在 `_build/content/` 标明。
- **图片**：Codex 联网搜索（follow-up 009 / 016），逐张许可见 `assets.json` 与 §6。
"""]
    out += ["## 6. 图片来源", "", "| # | 瀑布 | 文件 | 作者 | 许可 | 来源页 | 备注 |", "|---|---|---|---|---|---|---|"]
    for it in d["items"]:
        for key, tag in (("image", "主图"), ("image_alt", "默认版替代图")):
            f = it.get(key)
            if not f:
                continue
            a = assets.get(f, {})
            note = tag + ("；" + it["image_risk"] if key == "image" and it.get("image_risk") else "")
            out.append(f"| {it['rank']} | {it['name']} | `{f}` | {a.get('author','')} | {a.get('licence','（未入账）')} | {a.get('source_page') or a.get('commons_page','')} | {note} |")
    (EP / "sources.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("sources.md written")


if __name__ == "__main__":
    main()
