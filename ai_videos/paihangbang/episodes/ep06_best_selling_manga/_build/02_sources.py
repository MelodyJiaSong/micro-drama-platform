# -*- coding: utf-8 -*-
"""ep06：由 data.json + 调研 JSON 生成 sources.md（逐条出处、交叉核对、口径与旧数字说明）。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
R = EP / "_build" / "research"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    d = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    research = {}
    for g in "abc":
        for r in json.loads((R / f"group_{g}.json").read_text(encoding="utf-8")):
            research.setdefault(r["name_en"], r)
    L = ["# ep06 · 出处与核对（sources.md）", "",
         "> 2026-11-03 取数。主值优先出版社一手公告（新闻稿、媒体资料、官方 X），其次主流媒体转述公告；",
         "> Wikipedia「List of best-selling manga」（2026-11-03 版，原始 `_build/raw/`）只作基线与交叉核对。",
         "> 调研原始记录：`_build/research/group_{a,b,c}.json`（三个独立子代理，每条带原文措辞、口径、来源分级、备注）。", "",
         "## 1. 逐条主值", "",
         "| # | 作品 | 主值 | 原文措辞 | 口径 | 公布日 | 主源（分级） | 交叉核对 | 备注 |",
         "|---|---|---|---|---|---|---|---|---|"]
    for it in d["items"]:
        s, c = it["source"], it["cross_check"]
        cc = f"[{c['name'] or 'link'}]({c['url']}) {c['value']:,}" if c.get("url") and c.get("value") else "—"
        note = (it.get("notes") or "").replace("|", "/").replace("\n", " ")
        L.append(f"| {it['rank']} | {it['name']}（{it.get('name_ja','')}） | {it['value']:,} | {it.get('value_text_original','').replace('|','/')} | "
                 f"{it.get('scope','')} | {s.get('as_of','')} | [{s.get('name') or 'source'}]({s['url']})（{s.get('tier','')}） | {cc} | {note} |")
    L += ["", "## 2. 取舍与口径判断（代理 2026-11-03，待用户复核）", "",
          "1. **剔除：Crayon Shin-chan（Wikipedia 1.48 亿）**。万代影视 2015 年官方页面明细（web.archive.org 存档）：漫画 50 卷 5500 万＋新蜡笔小新 300 万＝5800 万，"
          "国内关联书籍（文库、新书、游戏书、百科）约 2000 万，「海外関連書籍」7000 万。前 2000 万确定不是漫画，所以按本期「含非漫画书籍的数字不收」规则剔除。"
          "**审片 #3 指出**：海外 7000 万可能包含翻译版漫画，若全算漫画则约 1.28 亿、可排第 13 名左右；无法核实，洞察卡只写确定的部分（约 2000 万非漫画）。是否改为收录（如 est. 128M）留给用户。",
          "2. **剔除：Astro Boy（Wikipedia 1 亿）**。唯一出处为 1981 年「関連書籍」累计（含绘本、文库），非漫画单行本口径，且无出版社公告。",
          "3. **出榜：Major（Wikipedia 6666 万）**。Wikipedia 引用的纪伊国屋到货推文中没有部数；可考的最新数字为 5500 万（2025-04-02）。",
          "4. **旧数字照收**：累计发行量只增不减，旧公告是下限。超过 18 个月的主值（bible §3.3 本应不用）在本期按例外处理（21/30 条，待用户批准），"
          "每张卡在数值旁标「as of 年份」，**年份 = 该数字首次公布的年份，媒体后来复述不算**（审片 #4 后统一）：Golgo 13 2021、Dragon Ball 2022、Fist of the North Star 2019、"
          "Kindaichi 2019、Captain Tsubasa 2023、Sangokushi 2020、Touch 2004、Vagabond 2012、KochiKame 2014、Sazae-san 1999。片头统计行改为「Latest announced figure · year on each card」。"
          "旧值之间的相对名次未必真实（如 Vagabond 82M@2012 与 Kinnikuman 85M@2025），描述框 scope_note 已说明。",
          "5. **口径不统一**：各出版社公布的口径不同（全世界 / 仅日本、含不含电子版、是否含续作与外传），本期按公告原样采用，"
          "口径逐条写在上表；片头口径行与描述框 scope_note 说明。KochiKame（2014 集英社媒体资料）为日本国内、系列合计；Golgo 13 为系列合计（全部形式）。",
          "6. **计分板按原单行本出版社计**：Fist of the North Star 原版为集英社 Jump Comics（数字也来自集英社时代的累计），现行版权方为 Coamix，封面用的是英文版（VIZ），卡上署名写明；Baki 封面也是英文版。"
          "**Golgo 13 出版社**：单行本由 Leed Publishing（SP Comics）出版，连载于小学馆《Big Comic》；计分板按单行本出版社记 Leed。",
          "7. **The Kindaichi Case Files**：取 2022-05-27 电击 Online「12 か国累计 1 亿」（较 2019 讲谈社公告更新，同值）。",
          "8. **同值同名次**：2 名 ×2、14 名 ×2、16 名 ×7、23 名 ×2、28 名 ×2；同名次内按英文名排序。",
          "9. **榜外最近的作品**：Gintama 7300 万（2026-02）、Fairy Tail 7200 万、Rurouni Kenshin 7200 万、Berserk 7000 万、Blue Lock 6500 万（2026-09，三个月 +500 万，最可能下次进榜）。",
          "", "## 3. 洞察卡依据", ""]
    support = {
        28: "Crayon Shin-chan 明细见 §2-1：国内关联书籍约 2000 万确定不是漫画。",
        23: "16 名并列 7 部，见上表。",
        11: "Oricon 2025-12-20：2024-09 完结时 1 亿 → 2025-12-20 1.5 亿，「1年3ヶ月で5000万部増加」（审片 #1 纠正：原稿误作「一年」）。",
        8: "集英社 2025-07-17：全 23 卷 2.2 亿 → 每卷约 957 万，高于 One Piece（600M/115≈5.2M）、Dragon Ball（260M/42≈6.2M）、Slam Dunk（185M/31≈6.0M）等。原稿「4.5 年 +7000 万」口径错配（国内数减全世界数，审片 #2），已换掉。",
        2: "One Piece 6 亿 ÷ 第 2 名「3 億部超」（Doraemon、Golgo 13）≈ 2 倍（因对方是「超」，写 about twice，审片 #16）。",
    }
    for ins in d["insights"]:
        L.append(f"- after #{ins['after_rank']}：{ins['text']} —— {support.get(ins['after_rank'], '')}")
    L += ["", "## 4. 计分板（按单行本出版社）", ""]
    from collections import Counter
    for k, v in Counter(i["continent"] for i in d["items"]).most_common():
        L.append(f"- {k}：{v}")
    L += ["", "## 5. 图片", "", "见 `assets.json`（版权账本）与 topic.md「风险」。封面与官方插画均为版权作品，统一标 `image_risk`。", ""]
    (EP / "sources.md").write_text("\n".join(L), encoding="utf-8")
    print("sources.md 写好", len(L), "行")


if __name__ == "__main__":
    main()
