# -*- coding: utf-8 -*-
"""data.json + assets.json → sources.md（改数据请改 items_def.py → build.py → 本脚本）。"""
import json
from pathlib import Path

EP = Path(__file__).resolve().parent.parent
d = json.loads((EP / "data.json").read_text(encoding="utf-8"))
assets = {a["file"]: a for a in json.loads((EP / "assets.json").read_text(encoding="utf-8"))}

L = []
A = L.append
A("# ep18 · 数据出处、交叉核对与许可（sources.md）\n")
A("> 2026-11-03 代理整理（用户授权自主决策）。本文件由 `_build/gen_sources.py` 生成；改数据请改 `_build/items_def.py` → `build.py` → `gen_sources.py`。每项调研原文摘要见 `_build/content/`。\n")
A("## 1. 口径\n")
A("- **榜单**：量产、可上路注册的公路车，按最高时速（km/h）降序；副显示 mph。每个车型一张卡，同车型多版本取最快的公路版本（Chiron 家族、Veyron 家族、Agera 家族、Nevera / Nevera R、Aventador 家族各算一个车型；Divo、Centodieci、W16 Mistral 是单独命名销售的车型，各自一张）。")
A("- **量产门槛**：同规格客户车 ≥10 台，且 2026-11 前已开始交付客户。不收：纯赛车 / 赛道车（Bugatti Bolide、SSC Tuatara Aggressor、Valkyrie AMR Pro）、一次性特制车、改装车、概念车、尚未交付的车（Bugatti Tourbillon、Koenigsegg Gemera、Zenvo Aurora、Aspark Owl 未见交付证据）。")
A("- **VERIFIED（实测）**：由独立第三方计时（Racelogic VBOX 技术人员、TÜV / SGS-TÜV Saar、Guinness、ATP 试验场、Dewesoft、FMSCI、Nardò 光电计时、Johnny Bohmer Proving Grounds）的最快**单向**速度。有双向平均的，在卡上 tag 写「2-way avg」并在 notes 写明。纪录车是预产车 / 原型车的照实写（Chiron 300+、Yangwang U9 Xtreme、McLaren F1 XP5）。加速测试中的计时峰值也算（Koenigsegg Jesko Absolut：2024 年 0-400-0 测试峰值 412 km/h，Racelogic 数据、Racelogic 英国总部核验）。")
A("- **CLAIMED（厂方宣称）**：厂方额定或厂方自测的最高时速（含电子限速值）。**设计目标与仿真不算**：Hennessey Venom F5 的「311+ mph」是未达成的目标，改用 Hennessey 自报的实跑最高 271.6 mph；Koenigsegg Jesko Absolut 官方无额定极速（官网「Time will tell」），创始人口述的仿真 531 km/h 不采用；它以 412 km/h 实测峰值按 VERIFIED 入榜（#12）。「400+」这类「以上」按数字计（Koenigsegg CCX 官网 400+ km/h → 400，CLAIMED，#16）。")
A("- **入榜线**：严格高于 350 km/h。额定恰好 350 km/h 的车（McLaren P1、Ferrari F80、McLaren W1、LaFerrari「350 以上」、Lamborghini Revuelto「350 以上」、Xiaomi SU7 Ultra「350 以上」）不收——「以上」没有给出具体数字，按 350 计。N = 30（2026-11-04 审片后补入 CCX、Jesko Absolut；数据只够 30，不凑数）。")
A("- **国家**：品牌发源国（集团归属写 notes）。Bugatti → 法国（EB110 由意大利的 Bugatti Automobili S.p.A. 在 Campogalliano 制造，仍按品牌计法国）；Pininfarina → 意大利（Automobili Pininfarina 总部慕尼黑、属印度 Mahindra）；Yangwang → 中国（BYD）；Rimac → 克罗地亚（Bugatti Rimac 集团）；Lamborghini → 意大利（大众集团）；Dauer → 德国。")
A("- **显示**：value_display 取整到 km/h（3 位有效数字）；secondary_display 为 mph（厂方 / 计时方公布值，取整）。同值同名次（1,1,3 式）：Divo / Centodieci 并列 20；Countach / Aventador / EB110 并列 25。")
A("- **统计期**：2026-11-03 取数，2026-11-04 审片后复核补充。\n")
A("## 2. 逐条出处与交叉核对\n")
A("差异 = |value − cross| / value。retrieved_at 全部 2026-11-03。\n")
A("| # | 车型 | 国家 | 口径 | value (km/h) | 主值来源 | 交叉核对 | 差异 % | 备注 |")
A("|---|---|---|---|---|---|---|---|---|")
for it in d["items"]:
    s, c = it["source"], it["cross_check"]
    cv = f"[{c['name']}]({c['url']}): {c['value']}" if c.get("value") is not None else f"[{c['name']}]({c['url']})"
    A(f"| {it['rank']} | {it['name']} | {it['country_name']} | {it['measure'].upper()} | {it['value']} | [{s['name']}]({s['url']}) | {cv} | {c.get('diff_pct')} | {it['notes'].replace('|', '/')} |")
A("")
A("## 3. 入榜线与落选说明\n")
A("- 第 30 名 Porsche 918 Spyder 351.5 km/h（Johnny Bohmer Proving Grounds 2018 实测 218.4 mph；Porsche 额定 345 km/h）。若只认厂方额定，918 不入榜，N = 29。")
A("- 恰好 350 km/h：McLaren P1（电子限速 350）、Ferrari F80（官方 350）、McLaren W1（官方估计 350）、LaFerrari / Revuelto / SU7 Ultra（官方「350 以上」）。Xiaomi SU7 Ultra 原型车 2024 年在盐城试验场跑出 359.71 km/h（厂方自测、原型车与量产车不是同一规格），不采用。")
A("- 未交付：Bugatti Tourbillon（厂方 445 km/h，需 Speed Key；2026-10 媒体称仍在准备首批交付）、Koenigsegg Gemera（400 km/h，Wikipedia 写 2026 起生产，未见交付报道）、Zenvo Aurora（420 km/h 限速，2027 下半年交付）、Aspark Owl（SP600 原型 438.7 km/h 获 Guinness「原型车」纪录；量产 50 台计划，未见交付证据）。")
A("- 产量不足 10 台：Koenigsegg One:1（7）、CC8S（6）、W Motors Lykan HyperSport（7）、Rimac Concept One（8）。")
A("- 资料不足未收（待补）：Koenigsegg CCXR（CCX 的环保燃料版，9 台，官网未单列极速，归入 CCX 家族不另列）、Pagani Huayra（约 238 mph，非官方）、Ruf CTR3 Evo（厂方 236 mph，产量不明）、Gumpert Apollo（360 km/h，Wikipedia 标 citation needed）、Vector W8（218 mph 宣称，量产车无实测）、9ff GT9-R、Mazzanti Evantra Millecavalli、W Motors Fenyr（交付不明）。\n")
A("## 4. 洞察卡核对\n")
A("| after | 文本 | 依据 |")
A("|---|---|---|")
why = {
    28: "§2 measure 列：VERIFIED 15、CLAIMED 15",
    23: "McLaren P1 电子限速 350（Wikipedia McLaren P1）；Ferrari F80 官方 350（Wikipedia Ferrari F80）；McLaren W1 官方估计 350（Wikipedia McLaren W1）",
    17: "纯电：Yangwang U9 Xtreme（2025-09 纪录）、Rimac Nevera R（2025-07 纪录）、Pininfarina Battista（2023-02 纪录）",
    10: "Tourbillon 445 km/h（autoindustriya 等，Speed Key）；2026-10-14 DuPont Registry 称 Bugatti 仍在准备首批客户交付",
    6: "Bugatti newsroom（Chiron Super Sport 300+ 交付稿）与 Wikipedia 纪录表：客户车电子限速 440 km/h，490.484 km/h 由预产原型车跑出（见 #2 notes）",
    3: "Wikipedia List of production car speed records：SSC Tuatara 2021-01-17 双向平均 282.9 mph（455.3 km/h）为表中最新纪录；Hagerty 2022 亦称官方数字仍是 2021 双向平均（见 #3 notes）",
}
for ins in d["insights"]:
    A(f"| {ins['after_rank']} | {ins['text']} | {why.get(ins['after_rank'], '')} |")
A("")
A("## 5. 图片许可账本\n")
A("| # | 车型 | 文件 | 作者 | 许可 | 来源页 | 风险 |")
A("|---|---|---|---|---|---|---|")
for it in d["items"]:
    for f in [it.get("image"), it.get("image_alt")]:
        a = assets.get(f)
        if a:
            A(f"| {it['rank']} | {it['name']} | `{f}` | {a.get('author','')} | {a.get('licence','')} | {a.get('source_page') or a.get('commons_page') or a.get('source_url','')} | {it.get('image_risk','') if f == it.get('image') else 'alt'} |")
(EP / "sources.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("sources.md written")
