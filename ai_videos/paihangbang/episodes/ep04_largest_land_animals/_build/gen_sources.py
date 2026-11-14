# -*- coding: utf-8 -*-
"""data.json → ../sources.md（每条主值的出处、交叉核对、IUCN、数量、国旗依据）。用法：python -I <本目录>/gen_sources.py"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EP = Path(__file__).resolve().parent.parent
d = json.loads((EP / "data.json").read_text(encoding="utf-8"))



# 第 4 轮复核 R4-m2：data.json 的 notes 是调研初稿 + 逐轮改动的流水，前文旧说法在此更正（不改 data.json，免得母版 manifest 的输入 sha 失配）
ERRATA = {
    "African Buffalo": "前文「按最大、最常见的开普水牛口径」「唯一性别分开来源经 Wikipedia 转引」是调研初稿说法，已被 M1 取代：主值现为 HMW 雄性 500–900 kg 的中点 700，维基 775 只作交叉核对。",
    "Brown Bear": "前文「Chosen value (Katmai mid-summer)… consider a lower species-wide figure」是调研初稿意见，已被 M2 取代：主值现为 SDZ 雄性 130–550 kg 的中点 340，NPS Katmai 340 只作交叉核对。",
}

def esc(s):
    return str(s if s is not None else "").replace("|", "\\|").replace("\n", " ")


def link(name, url):
    return f"[{esc(name)}]({url})" if url else esc(name or "—")


L = []
A = L.append
A("# ep04 · 数据出处与交叉核对（sources.md）")
A("")
A("> 2026-11-03 代理整理。本文件由 `_build/gen_sources.py` 从 `data.json` 生成；改数据改 `_build/build.py` 后重跑 build → gen_sources。")
A("> 调研：三路子代理（`_build/research/batch_{A,B,C}.json`，说明见 `BRIEF.md`）＋主会话补查。**限制**：iucnredlist.org 对脚本与抓取工具返回 403，很多 IUCN 类别、年份取自评估 DOI、专家组页面或转载，`iucn.url` 为空的未直接打开评估页；维基百科只作交叉核对。")
A("")
A("## 1. 口径")
A("")
A("- **主值**：成年雄性典型（平均）体重，kg；副显示 lb（×2.20462，取整到 10 lb，2,000 lb 以上取整到 100 lb）。屏上 1,000 kg 以上取整到 50 kg，以下照出处原值。")
A("- **只给范围的取中点**（`kind = range midpoint`），在下表标出。排序用原值。")
A("- **收录**：IUCN Red List 现行分类的现存野生物种；不收家畜 / 家养型、海兽、鳄类；收河马、北极熊。亚种不单列。")
A("- **国旗**：该物种野外个体数最多的国家；**大洲**按国旗国家的 UN M49 分区（俄罗斯 → Europe）。")
A("- **徽章**：IUCN 类别 NT / VU / EN / CR；LC 不显示。**标签**：野外数量、「Up to ~X kg」（出处给出的最大值：范围上限、个别大个体或推算值，象类为按肩高推算，不是称重记录；独立审片 M6）；非洲森林象另标「Estimate: none weighed」。")
A("- **口径统一（独立审片 M2）**：凡出处只给雄性体重范围的，一律取该范围中点（棕熊 SDZ 雄性 130–550 → 340 入榜）；非洲水牛主值改用《Handbook of the Mammals of the World》雄性 500–900 的中点 700（M1）；gaur 用 Walker's 雄性 588–1,500 的中点 1,044（经维基转读，secondary；复审 N2），卡上首位标「Estimates: 650–1,500 kg」（第 3 轮 R3-M1）。")
A("")
A("## 2. 逐条")
A("")
A("| # | 物种 | 主值 | 出处（取值方式） | 交叉核对 | 差异 | IUCN | 国旗依据（可信度） |")
A("|---|---|---|---|---|---|---|---|")
for it in d["items"]:
    s, cc, iu, st = it["source"], it.get("cross_check") or {}, it.get("iucn") or {}, it.get("stronghold") or {}
    diff = ""
    if cc.get("value"):
        diff = f"{(cc['value'] - it['value']) / it['value'] * 100:+.0f}%"
    A(f"| {it['rank']} | {esc(it['name'])} *{esc(it['scientific_name'])}* | {it['value']:g} kg | {link(s['name'], s['url'])}（{esc(s.get('kind'))}；{esc(s.get('tier'))}） "
      f"| {link(cc.get('source_name'), cc.get('source_url'))} {cc.get('value') or ''} | {diff} "
      f"| {link((iu.get('category') or '?') + ' ' + str(iu.get('assessed_year') or ''), iu.get('url'))} {esc(iu.get('population_trend') or '')} "
      f"| {esc(st.get('country'))}：{link(st.get('evidence'), st.get('source_url'))}（{esc(st.get('confidence'))}） |")
A("")
A("### 野外数量与最大记录")
A("")
A("| # | 物种 | 野外数量（年份） | 最大记录 |")
A("|---|---|---|---|")
for it in d["items"]:
    p, m = it.get("wild_population") or {}, it.get("max_mass") or {}
    A(f"| {it['rank']} | {esc(it['name'])} | {link((p.get('display') or '') + (' (' + str(p.get('year')) + ')' if p.get('year') else ''), p.get('source_url')) if p else '—'} "
      f"| {link(str(m.get('value') or '') + ' kg ' + esc(m.get('text') or ''), m.get('source_url')) if m and m.get('value') else '—'} |")
A("")
A("### 备注（口径疑点、来源冲突）")
A("")
for it in d["items"]:
    if it.get("notes"):
        A(f"- **#{it['rank']} {esc(it['name'])}**：{esc(it['notes'])}" + (f" ｜**第 4 轮复核更正（R4-m2）**：{ERRATA[it['name']]}" if it['name'] in ERRATA else ""))
A("")
A("## 3. 落选与边界")
A("")
A("| 物种 | 雄性典型体重 | 不收 / 落选原因 |")
A("|---|---|---|")
for row in [
    ("湾鳄 Saltwater crocodile", "~464 kg（408–520 中点，吉尼斯）", "按口径鳄类算水生、不收（本片的选择，非生物学定论）；洞察卡 after #22 主动说明"),
    ("尼罗鳄 Nile crocodile", "~450 kg（来源弱）", "同上"),
    ("高棉牛 Kouprey", "~750 kg（600–900，两性合并；雄性可能更高）", "IUCN CR（Possibly Extinct）；最后确认记录说法不一（1963/64、1969、1983）；洞察卡写「几十年未确认存活」"),
    ("野生双峰驼 Wild Bactrian camel", "查不到野生个体的雄性体重（ADW 300–690 kg 混合家养）", "无可靠数值，不排；口径说明（scope_note）写明原因（独立审片 M4）"),
    ("加拉帕戈斯象龟 C. porteri", "295 kg（272–318 中点，旧金山动物园）", "第 31 名，差第 30 名 2 kg；洞察卡 after #26 提及"),
    ("马来貘 Malayan tapir", "285 kg（中点，维基）", "落选"),
    ("中美貘 Baird's tapir", "275 kg（中点）", "落选"),
    ("普氏野马 Przewalski's horse", "270 kg（两性合并中点）", "落选"),
    ("马羚 Roan antelope", "268–280 kg", "落选"),
    ("霍加狓 / 亚达伯拉象龟", "~250 kg", "落选"),
    ("民都洛水牛 Tamaraw / 水鹿 Sambar", "237 / 225 kg", "落选"),
    ("老虎、狮子、大猩猩、美洲黑熊、鸵鸟", "115–180 kg", "远低于门槛"),
]:
    A(f"| {' | '.join(row)} |")
A("")
A("第 26–31 名（325–295 kg）彼此相差都在 10% 内、第 28–31 名（300–295 kg）不到 2%，换来源就可能换位；描述框口径行已写「相差约 5% 以内视为并列」。")
A("")
A("## 4. 洞察卡")
A("")
ins_src = {
    30: "口径说明（国旗规则），见 §1",
    26: "象龟：batch_C（旧金山动物园 C. porteri 272–318 kg，中点 295）",
    22: "湾鳄：batch_A（吉尼斯，408–520 kg 中点 464）；「count crocodiles as aquatic」是本片口径选择",
    15: "高棉牛：batch_B（IUCN SSC 亚洲野牛专家组；最后确认记录 1963/64–1983 说法不一，故写 in decades）",
    12: "data.json：第 11 名野牦牛 1,000 kg 起均 ≥ 1 吨（第 10 名 gaur 1,044）；第 12 名野水牛 950 kg",
    8: "长颈鹿：batch_A（IUCN SSC 长颈鹿与霍加狓专家组 2025-08 认定 4 种；红色名录仍按 1 种，VU 2016；发布前 7 天复核）",
}
for x in d["insights"]:
    A(f"- after #{x['after_rank']}：\"{x['text']}\" — {ins_src.get(x['after_rank'], '')}")
A("")
A("## 5. 原始数据")
A("")
A("- `_build/research/batch_A.json`（象、犀牛、河马、长颈鹿、鳄）、`batch_B.json`（牛科、驼）、`batch_C.json`（鹿、熊、猫科、马科、貘等）。")
A("- 主会话补查与改动写在 `_build/build.py` 的 `EXTRA` / `OVERRIDE`（每条带原因）。")
A("- 竞品检索：`0_research/data/yt_search_land_animals_2026-11-03.jsonl`。")
(EP / "sources.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("sources.md", len(L), "行")
