# -*- coding: utf-8 -*-
"""data.json + assets.json + research/*.json → ../sources.md。用法：python -I _build/gen_sources.py"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parent
d = json.loads((EP / "data.json").read_text(encoding="utf-8"))
assets = {a["file"]: a for a in json.loads((EP / "assets.json").read_text(encoding="utf-8"))}


def esc(s):
    return str(s if s is not None else "").replace("|", "\\|").replace("\n", " ")


def link(name, url):
    return f"[{esc(name)}]({url})" if url else esc(name)


L = []
A = L.append
A("# ep19 · 数据出处、交叉核对与许可（sources.md）")
A("")
A("> 2026-11-03 代理整理（follow-up 015 / 016）。本文件由 `_build/gen_sources.py` 生成；改数据请改 `_build/items_def.py` → `build.py` → `gen_sources.py`。调研原料：`_build/research/{europe,asia,africa_americas}.json`（逐国来源、原文引句、口径说明），UN Tourism 原始表 `_build/raw/`。")
A("")
A("## 1. 口径")
A("")
A("- **指标**：international tourist arrivals（入境过夜游客，overnight visitors），2024 全年，百万人次；同一人多次入境分别计。")
A("- **主源**：UN Tourism Statistics Database，批量下载 `UN_Tourism_bulk_data_download_12_2025.zip`（2025-12-23 更新，2025-12-29 发布；https://pre-webunwto.s3.amazonaws.com/s3fs-public/2025-12/UN_Tourism_bulk_data_download_12_2025.zip），序列 `INBD_TRIP_TOTL_TOTL_TOUR`（澳大利亚只有 `..._VSTR`，因无当日入境访客，按 UN 惯例用之）。2026-05 版批量包里的入境表与 2025-12 版逐字节相同。")
A("- **数据库缺 2024 时**：用本国官方**同一序列**（用数据库 2019 值匹配官方序列，即「2019 指纹」）。法国 2024 只有官方估计「plus de 100 millions」。")
A("- **变化（D2）**：`secondary_display` = 与 2019 同一序列相比的 ▲▼%（四舍五入到整数；|变化| < 0.5% 写「≈ 2019 level」）。序列断档：巴林、爱尔兰改与 2023 比；印度 2019 用 FTAs 10.93M（数据库 2019 的 17.75M 含海外印度人）；葡萄牙 2019 用 INE 估计序列 24.6M（数据库 2019 的 17.28M 是住宿口径）；瑞典、瑞士 2019 用 Eurostat 同口径值。")
A("- **显示**：3 位有效数字（100M、93.8M、9.82M），排序用原值；无并列。")
A("- **NEW SINCE 2019**：2019 年同序列值低于当年第 50 名（约 6.35M）一大截的国家（哥伦比亚 4.15M）。阿尔巴尼亚（6.13M）、挪威（5.88M）在 2019 年处于第 50 名边缘，不标。")
A("")
A("## 2. 未入榜与归属判断（待用户复核）")
A("")
A("| 国家 / 地区 | 做法 | 依据 |")
A("|---|---|---|")
A("| 中国 | 不入榜 | 2019 UN TOUR 65.7M（文旅部入境过夜游客，含港澳台）。2020 年后文旅部 / 统计局只公布入境游客（含一日游）：2024 为 13,190 万人次（港澳台 10,496 万、外国人 2,694 万）。维基 World Tourism rankings 的 China 2024 = 64.9M 实为国家移民管理局「外国人出入境 6,488.2 万人次」（出入境合计），不是入境过夜游客。见 `_build/research/asia.json`。 |")
A("| 阿联酋 | 不入榜 | UN 2019 TOUR 21.56M = 全国酒店外国住客；2024 全国外国住客无公开值。常见 18.72M 只是迪拜 DET 的国际过夜游客。 |")
A("| 丹麦 | 不入榜 | UN 2019 TOUR 14.73M 对不上 Danmarks Statistik 任何公开序列，2024 无同口径值。 |")
A("| 保加利亚、俄罗斯 | 不入榜 | 无同口径 2024 全年值（保加利亚只有住宿口径 3.77M；俄罗斯只有 1–9 月及边防「旅游目的」1.57M）。 |")
A("| 卡塔尔、伊朗、老挝 | 不入榜 | 无可核实 2024 官方值（卡塔尔约 5.1M 访客、伊朗「7M+」含侨民与朝圣、老挝「5M+」未分内外，均未核到）。 |")
A("| 波多黎各 | 不列入 | UN DB 单列 5.55M，但它是美国属地，游客几乎全是美国本土居民（国内航班），不符合「国家」榜。 |")
A("| 香港、澳门 | 单列，badge SAR OF CHINA | UN Tourism 单列报告单位；用过夜访客（香港 21.9M、澳门 16.0M），不是含一日游的 44.5M / 34.9M。 |")
A("| 台湾 | 列入，写 Taiwan | 系列惯例（ep02）；UN 名称 Taiwan Province of China。 |")
A("| 大洲 | UN M49 | 土耳其、哈萨克斯坦、乌兹别克斯坦、沙特、巴林 → Asia；墨西哥、多米尼加 → North America；埃及、摩洛哥、突尼斯 → Africa。 |")
cc = {}
for it in d["items"]:
    cc[it["continent"]] = cc.get(it["continent"], 0) + 1
A(f"| 计分结果 | — | {', '.join(f'{k} {v}' for k, v in sorted(cc.items(), key=lambda x: -x[1]))} |")
A("")
A("## 3. 边界")
A("")
A("- 第 50 名菲律宾 5.949M（DOT，Manila Times 转引原文 5,949,350，含海外菲律宾人 510,383；维基表 6,435,438 引 DOT 年报 PDF，403 未核，任一值都在榜内）。")
A("- 第 51 智利 5.239M、第 52 约旦 5.217M、第 53 格鲁吉亚 5.092M、第 54 斯洛文尼亚 5.054M、芬兰 4.475M（序列断档）、安道尔 4.168M、塞浦路斯 4.040M（均为 UN DB 2024 TOUR）。")
A("")
A("## 4. 逐条出处与交叉核对")
A("")
A("差异 = |cross − value| / value。retrieved_at 均为 2026-11-03。「未核到」= 本会话联网搜索额度（10 个代理共用）用尽，只有 UN Tourism 数据库一个来源，发布前复核时补。")
A("")
A("| # | 国家 | 2024 (M) | 主值来源 | 交叉核对 | 差异 % | 基准 | 变化 | 备注 |")
A("|---|---|---|---|---|---|---|---|---|")
for it in d["items"]:
    s, x, b = it["source"], it.get("cross_check"), it["change_base"]
    xs = f"{link(x['name'], x['url'])}: {x['value']}" if x else "未核到"
    A(f"| {it['rank']} | {esc(it['name'])} | {it['value']} | {link(s['name'], s['url'])} | {xs} | {x['diff_pct'] if x else ''} | "
      f"{b['year']}: {b['value']} | {esc(it['secondary_display'])} | {esc(it['notes'])} |")
A("")
A("交叉核对差异 > 3% 的条目（口径不同，主值不变）：土耳其 TÜİK 62.2M 含当日游；英国 ONS 42.6M（2024 年中途换调查设计，含少量当日访问）；新加坡 STB 16.5M 含当日访客；捷克 36.3M 是全部入境访客（过夜部分 14.36M 与主值一致）；瑞士、瑞典核对值只含酒店；阿尔巴尼亚、爱尔兰、塞浦路斯核对值是住宿口径（只作量级参考）；哥伦比亚 6.7M 含 0.31M 邮轮客。")
A("")
A("## 5. 洞察卡支持")
A("")
for ins in d["insights"]:
    A(f"- after {ins['after_rank']}：{ins['text']}")
A("  - 1 台湾：7.858 / 11.864 − 1 = −33.8%，本榜同序列 2019 对比中跌幅最大（其次菲律宾 −28.0%、匈牙利 −22.3%）；巴林、爱尔兰与 2023 比不计。")
A("  - 2 阿尔巴尼亚：11.483 / 6.128 − 1 = +87.4%，本榜最大（其次沙特 +69.6%、哥伦比亚 +53.8%）。")
A("  - 3 中国：见 §2；2019 UN TOUR 65.725M。")
A("  - 4 沙特：29.727 / 17.526 − 1 = +69.6%；前 15 名中其次为土耳其、葡萄牙 +18%。")
A("  - 5 土耳其 60.6 / 51.192 − 1 = +18.4%；意大利 57.725 / 64.513 − 1 = −10.5%；2019 年意大利（64.5M）高于土耳其（51.2M），2024 土耳其第 4、意大利第 5。")
A("")
A("## 6. 图片许可")
A("")
A("| # | 国家 | 景点 | 文件 | 作者 | 许可 | 来源页 | 风险 |")
A("|---|---|---|---|---|---|---|---|")
for it in d["items"]:
    for f, tag in ((it.get("image"), ""), (it.get("image_alt"), "（默认版替代图）")):
        if not f:
            continue
        a = assets.get(f, {})
        A(f"| {it['rank']} | {esc(it['name'])} | {esc(it.get('landmark', ''))}{tag} | `{f}` | {esc(a.get('author', ''))} | {esc(a.get('licence', '（未入账）'))} | "
          f"{a.get('source_page', '')} | {esc(it.get('image_risk', '') if not tag else '')} |")
(EP / "sources.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("sources.md", len(L), "lines")
