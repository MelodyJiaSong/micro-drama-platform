# -*- coding: utf-8 -*-
"""ep06 第一步（内容）：把三组调研（research/group_{a,b,c}.json）合成 data.json + assets.json 骨架。

取舍规则（topic.md / sources.md 同步）：
- 主值 = 出版社公布（或主流媒体转述其公告）的最新累计发行量；Wikipedia 只作交叉核对。
- 剔除口径不是「漫画本身」的数字：Crayon Shin-chan（1.48 亿含周边书，漫画约 5800 万）、Astro Boy（1 亿为 1981 年「相关书籍」）。
- Major 的 6666 万无出处，实为 5500 万，出榜。
- 旧数字（>18 个月）照收：累计量只增不减，旧值是下限；每张卡 secondary 写「as of 年份」。
- 同值同名次；同名次内按英文名排序（稳定）。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
R = EP / "_build" / "research"
TODAY = "2026-11-03"

rows = {}
for g in "abc":
    for r in json.loads((R / f"group_{g}.json").read_text(encoding="utf-8")):
        rows.setdefault(r["name_en"], r)          # Kindaichi 在 b、c 两组都有：c 组是 2022 新数字，下面单独覆盖
kin_c = next(r for r in json.loads((R / "group_c.json").read_text(encoding="utf-8")) if r["name_en"] == "The Kindaichi Case Files")

# name_en(调研里的键) → 屏上名、出版社（计分板键）、作者标签、年份标签、数字年份、徽章
PICK = [
    ("One Piece", "One Piece", "Shueisha", "Eiichiro Oda", "1997–present", 2026, ""),
    ("Doraemon", "Doraemon", "Shogakukan", "Fujiko F. Fujio", "1969–1996", 2024, ""),
    ("Golgo 13", "Golgo 13", "Leed Publishing", "Takao Saito", "1968–present", 2022, "RECORD 221 VOLUMES"),
    ("Case Closed / Detective Conan", "Detective Conan", "Shogakukan", "Gosho Aoyama", "1994–present", 2023, ""),
    ("Dragon Ball", "Dragon Ball", "Shueisha", "Akira Toriyama", "1984–1995", 2024, ""),
    ("Naruto", "Naruto", "Shueisha", "Masashi Kishimoto", "1999–2014", 2023, ""),
    ("Demon Slayer: Kimetsu no Yaiba", "Demon Slayer", "Shueisha", "Koyoharu Gotouge", "2016–2020", 2025, "ONLY 23 VOLUMES"),
    ("Slam Dunk", "Slam Dunk", "Shueisha", "Takehiko Inoue", "1990–1996", 2025, ""),
    ("KochiKame: Tokyo Beat Cops", "KochiKame", "Shueisha", "Osamu Akimoto", "1976–2016", 2014, ""),
    ("Jujutsu Kaisen", "Jujutsu Kaisen", "Shueisha", "Gege Akutami", "2018–2024", 2025, "+50M IN ONE YEAR"),
    ("Attack on Titan", "Attack on Titan", "Kodansha", "Hajime Isayama", "2009–2021", 2024, ""),
    ("Oishinbo", "Oishinbo", "Shogakukan", "Kariya & Hanasaki", "1983–2014", 2020, "ON HIATUS SINCE 2014"),
    ("Bleach", "Bleach", "Shueisha", "Tite Kubo", "2001–2016", 2022, ""),
    ("JoJo's Bizarre Adventure", "JoJo's Bizarre Adventure", "Shueisha", "Hirohiko Araki", "1987–present", 2023, ""),
    ("Kingdom", "Kingdom", "Shueisha", "Yasuhisa Hara", "2006–present", 2026, "NEW: 120M IN JAN 2026"),
    ("Baki the Grappler (Baki series)", "Baki", "Akita Shoten", "Keisuke Itagaki", "1991–present", 2024, ""),
    ("Fist of the North Star", "Fist of the North Star", "Shueisha", "Buronson & Tetsuo Hara", "1983–1988", 2025, ""),
    ("Hajime no Ippo", "Hajime no Ippo", "Kodansha", "George Morikawa", "1989–present", 2023, "145 VOLUMES SO FAR"),
    ("Hunter × Hunter", "Hunter × Hunter", "Shueisha", "Yoshihiro Togashi", "1998–present", 2026, "NEW: 100M IN JUNE 2026"),
    ("The Kindaichi Case Files", "The Kindaichi Case Files", "Kodansha", "Amagi, Kanari & Sato", "1992–present", 2022, ""),
    ("My Hero Academia", "My Hero Academia", "Shueisha", "Kohei Horikoshi", "2014–2024", 2024, ""),
    ("Touch", "Touch", "Shogakukan", "Mitsuru Adachi", "1981–1986", 2004, ""),
    ("Captain Tsubasa", "Captain Tsubasa", "Shueisha", "Yoichi Takahashi", "1981–2024", 2026, ""),
    ("Fullmetal Alchemist", "Fullmetal Alchemist", "Square Enix", "Hiromu Arakawa", "2001–2010", 2026, "NEW: 90M IN JULY 2026"),
    ("Sazae-san", "Sazae-san", "Shimaisha", "Machiko Hasegawa", "1946–1974", 1999, "OLDEST ON THE LIST"),
    ("Kinnikuman", "Kinnikuman", "Shueisha", "Yudetamago", "1979–present", 2025, ""),
    ("Vagabond", "Vagabond", "Kodansha", "Takehiko Inoue", "1998–2015", 2012, "ON HIATUS SINCE 2015"),
    ("Sangokushi (Romance of the Three Kingdoms)", "Sangokushi", "Ushio Shuppan", "Mitsuteru Yokoyama", "1971–1987", 2026, ""),
    ("Tokyo Revengers", "Tokyo Revengers", "Kodansha", "Ken Wakui", "2017–2022", 2024, ""),
    ("Haikyu!!", "Haikyu!!", "Shueisha", "Haruichi Furudate", "2012–2020", 2025, ""),
]

# Touch：2025 年报道里的 1 亿是 2004 年东宝公布的数字，按底层年份标。
TOUCH_NOTE = "The 100M figure dates from the 2004 Toho announcement for the live-action film; the 2025 article repeats it."

INSIGHTS = [
    (28, "Crayon Shin-chan is often listed at 148M, but only about 58M of that is the manga."),
    (23, "Next: seven series tied at the 100-million mark."),
    (11, "Jujutsu Kaisen added 50 million copies in a single year after its 2024 finale."),
    (8, "Demon Slayer ended in 2020 with 23 volumes, then sold 70M more in 4.5 years."),
    (2, "One Piece has sold twice as many copies as any other manga."),
]

SCOPE = ("What counts: manga series ranked by the latest cumulative circulation officially announced by the publisher "
         "(or reported from its announcement), including overseas and digital editions where the announcement does. "
         "Figures that bundle non-manga books are left out (Crayon Shin-chan's 148M, Astro Boy's 100M). "
         "Cumulative figures only go up, so older announcements are kept as minimums and labelled with their year. "
         "Equal figures share a rank.")


def disp(v: int) -> str:
    m = v / 1e6
    return f"{m:.0f}M" if m >= 100 or m == int(m) else f"{m:.0f}M"


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower().replace("×", "x")).strip("_")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    picked = []
    for key, name, pub, author, years, fig_year, badge in PICK:
        r = kin_c if key == "The Kindaichi Case Files" else rows[key]
        picked.append((r, name, pub, author, years, fig_year, badge))
    # 排名：值降序；同值按名字
    picked.sort(key=lambda t: (-t[0]["value"], t[1].lower()))
    items, rank, prev = [], 0, None
    for k, (r, name, pub, author, years, fig_year, badge) in enumerate(picked, 1):
        if r["value"] != prev:
            rank, prev = k, r["value"]
        cc = r.get("cross_check") or {}
        notes = r.get("notes", "")
        if name == "Touch":
            notes = TOUCH_NOTE + " " + notes
        it = {
            "rank": rank,
            "name": name,
            "name_ja": r.get("name_ja", ""),
            "author": r.get("author", ""),
            "publisher": r.get("publisher", ""),
            "subtitle": "",
            "country_iso2": "JP",
            "country_name": pub,
            "continent": pub,
            "value": r["value"],
            "value_display": disp(r["value"]),
            "secondary_display": f"copies · as of {fig_year}",
            "tags": [{"icon": "users", "text": author}, {"icon": "calendar", "text": years}],
            "image": f"assets/img/{rank:02d}_{slug(name)}.jpg",
            "source": {"name": r["source"].get("name", ""), "url": r["source"]["url"], "tier": r["source"].get("tier", ""),
                       "as_of": r.get("as_of", ""), "retrieved_at": TODAY},
            "cross_check": {"name": cc.get("name", ""), "url": cc.get("url", ""), "value": cc.get("value"),
                            "diff_pct": round(abs((cc.get("value") or r["value"]) - r["value"]) / r["value"] * 100, 1)},
            "scope": r.get("scope", ""),
            "value_text_original": r.get("value_text_original", ""),
            "figure_year": fig_year,
            "notes": notes,
        }
        if badge:
            it["badge"] = badge
        for t in it["tags"]:
            assert len(t["text"]) <= 24, t
        assert len(badge) <= 22, badge
        items.append(it)
    assert len(items) == 30, len(items)
    for a, t in INSIGHTS:
        assert len(t) <= 90, (len(t), t)
    assert len(SCOPE) <= 600, len(SCOPE)
    data = {
        "episode": "ep06_best_selling_manga",
        "title": "Best-Selling Manga of All Time",
        "kicker": "TOP 30",
        "metric_label": "Copies in circulation",
        "unit": "copies",
        "period_label": "Latest official figures · Nov 2026",
        "source_line": "Sources: publisher announcements, Oricon, Natalie, Mantan Web, ANN",
        "theme": "manga",
        "tally": {"by": "continent", "title": "Series by publisher"},
        "layout": {"card_w": 600, "focus": [0.5, 0.2], "flags": False},
        "scope_note": SCOPE,
        "insights": [{"after_rank": a, "text": t} for a, t in INSIGHTS],
        "items": items,
    }
    (EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not (EP / "assets.json").exists():
        (EP / "assets.json").write_text("[]\n", encoding="utf-8")
    for it in items:
        print(f"#{it['rank']:>2} {it['name']:<26} {it['value_display']:>5}  {it['secondary_display']:<22} {it['country_name']:<16} {it.get('badge','')}")
    from collections import Counter
    print(Counter(i["continent"] for i in items).most_common())


if __name__ == "__main__":
    main()
