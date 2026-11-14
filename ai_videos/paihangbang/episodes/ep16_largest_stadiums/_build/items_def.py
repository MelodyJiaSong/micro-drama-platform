# -*- coding: utf-8 -*-
"""ep16 条目定义：主值、来源、交叉核对取自 _build/research/{us,world}.json（2026-11-03 调研），
本文件只做选择、屏上文字与少量覆盖（覆盖原因写在 notes）。改完运行 python _build/build.py。"""
from __future__ import annotations

import json
from pathlib import Path

B = Path(__file__).resolve().parent
R = {x["short_name"]: x for f in ("us", "world") for x in json.loads((B / "research" / f"{f}.json").read_text(encoding="utf-8"))}

EPISODE = {
    "episode": "ep16_largest_stadiums",
    "title": "Largest Stadiums in the World",
    "kicker": "TOP 50",
    "metric_label": "Seated capacity",
    "unit": "seats",
    "period_label": "Official seats, Nov 2026",
    "source_line": "Sources: stadium, club & league official data; StadiumDB",
    "theme": "arena",
    "tally": {"by": "country", "title": "Stadiums by country"},
    "scope_note": ("What counts: open sports stadiums of any code (football, American football, cricket, rugby, multi-use), "
                   "ranked by current official SEATED capacity as of Nov 2026 (standing areas, temporary stands and record "
                   "crowds don't count). Race tracks and racecourses are excluded. Stadiums that are closed, being rebuilt "
                   "or only partly reopened (e.g. Camp Nou) are left out. Equal capacities share a rank. Country = where "
                   "the stadium stands."),
    "layout": {"card_w": 720, "focus": [0.5, 0.5], "intro_hold": 2.5,
               "image_prefer": ("the whole stadium clearly visible and recognisable: an aerial or elevated exterior view "
                                "showing its full size, or a packed full-house bowl view on match day; landscape fine")},
}

FOP = "No commercial freedom of panorama in {} (see sources.md §3)"

# key = research short_name；slug = 内容文件 / 图片文件名；v = 主值覆盖（None = 用 research）
ROWS = [
    # key, slug, name, subtitle, iso2, country, continent, opened_tag, use_tag, badge, fop_country, override
    ("Narendra Modi Stadium", "narendra_modi_stadium", "Narendra Modi Stadium", "Ahmedabad, Gujarat", "IN", "India", "Asia", "Rebuilt 2020", "Cricket", "", None, {}),
    ("Rungrado May Day Stadium", "rungrado_1st_of_may_stadium", "Rungrado May Day Stadium", "Pyongyang", "KP", "North Korea", "Asia", "Opened 1989", "Football", "ESTIMATE", None, {}),
    ("Michigan Stadium", "michigan_stadium", "Michigan Stadium", "Ann Arbor, Michigan", "US", "United States", "North America", "Opened 1927", "American football", "", None, {}),
    ("Beaver Stadium", "beaver_stadium", "Beaver Stadium", "University Park, Pennsylvania", "US", "United States", "North America", "Opened 1960", "American football", "2025 OFFICIAL FIGURE", None, {}),
    ("Kyle Field", "kyle_field", "Kyle Field", "College Station, Texas", "US", "United States", "North America", "Opened 1927", "American football", "", None, {}),
    ("Tiger Stadium (LSU)", "tiger_stadium_lsu", "Tiger Stadium", "Baton Rouge, Louisiana (LSU)", "US", "United States", "North America", "Opened 1924", "American football", "", None, {}),
    ("Ohio Stadium", "ohio_stadium", "Ohio Stadium", "Columbus, Ohio", "US", "United States", "North America", "Opened 1922", "American football", "-739 SEATS IN 2026", None, {}),
    ("Neyland Stadium", "neyland_stadium", "Neyland Stadium", "Knoxville, Tennessee", "US", "United States", "North America", "Opened 1921", "American football", "", None, {}),
    ("DKR–Texas Memorial Stadium", "dkr_texas_memorial_stadium", "DKR–Texas Memorial Stadium", "Austin, Texas", "US", "United States", "North America", "Opened 1924", "American football", "", None, {}),
    ("Bryant–Denny Stadium", "bryant_denny_stadium", "Bryant–Denny Stadium", "Tuscaloosa, Alabama", "US", "United States", "North America", "Opened 1929", "American football", "", None, {}),
    ("Melbourne Cricket Ground", "melbourne_cricket_ground", "Melbourne Cricket Ground", "Melbourne, Victoria", "AU", "Australia", "Oceania", "Opened 1853", "Cricket, Aussie rules", "", None, {}),
    ("FNB Stadium (Soccer City)", "fnb_stadium", "FNB Stadium", "Johannesburg (Soccer City)", "ZA", "South Africa", "Africa", "Rebuilt 2009", "Football", "", "South Africa", {}),
    ("Misr Stadium", "misr_stadium", "Misr Stadium", "New Administrative Capital", "EG", "Egypt", "Africa", "Opened 2024", "Football", "NEW 2024", "Egypt", {}),
    ("Sanford Stadium", "sanford_stadium", "Sanford Stadium", "Athens, Georgia", "US", "United States", "North America", "Opened 1929", "American football", "+287 SEATS IN 2024", None, {}),
    ("Cotton Bowl", "cotton_bowl", "Cotton Bowl", "Dallas, Texas", "US", "United States", "North America", "Opened 1930", "American football", "", None, {}),
    ("Wembley Stadium", "wembley_stadium", "Wembley Stadium", "London", "GB", "United Kingdom", "Europe", "Opened 2007", "Football", "", None, {}),
    ("Rose Bowl", "rose_bowl", "Rose Bowl", "Pasadena, California", "US", "United States", "North America", "Opened 1922", "American football", "", None, {}),
    ("Lusail Stadium", "lusail_stadium", "Lusail Stadium", "Lusail", "QA", "Qatar", "Asia", "Opened 2021", "Football", "2022 WORLD CUP FINAL", "Qatar", {}),
    ("Ben Hill Griffin Stadium", "ben_hill_griffin_stadium", "Ben Hill Griffin Stadium", "Gainesville, Florida", "US", "United States", "North America", "Opened 1930", "American football", "", None, {}),
    ("Jordan-Hare Stadium", "jordan_hare_stadium", "Jordan–Hare Stadium", "Auburn, Alabama", "US", "United States", "North America", "Opened 1939", "American football", "", None, {}),
    ("Estadio Azteca (Banorte)", "estadio_banorte", "Estadio Azteca", "Mexico City (Estadio Banorte)", "MX", "Mexico", "North America", "Opened 1966", "Football", "REOPENED 2026", None, {}),
    ("Borg El Arab Stadium", "borg_el_arab_stadium", "Borg El Arab Stadium", "Alexandria", "EG", "Egypt", "Africa", "Opened 2007", "Football", "", "Egypt", {}),
    ("Bukit Jalil Stadium", "bukit_jalil_national_stadium", "Bukit Jalil National Stadium", "Kuala Lumpur", "MY", "Malaysia", "Asia", "Opened 1998", "Football", "", None, {}),
    ("Memorial Stadium Nebraska", "memorial_stadium_nebraska", "Memorial Stadium", "Lincoln, Nebraska", "US", "United States", "North America", "Opened 1923", "American football", "", None, {}),
    ("Mâs Monumental", "estadio_monumental_buenos_aires", "Estadio Monumental", "Buenos Aires (River Plate)", "AR", "Argentina", "South America", "Opened 1938", "Football", "EXPANDED 2024", None, {}),
    ("Accor Stadium", "accor_stadium", "Stadium Australia", "Sydney (Accor Stadium)", "AU", "Australia", "Oceania", "Opened 1999", "Rugby, football", "", None, {}),
    ("MetLife Stadium", "metlife_stadium", "MetLife Stadium", "East Rutherford, New Jersey", "US", "United States", "North America", "Opened 2010", "American football", "2026 WORLD CUP FINAL", None, {}),
    ("Jakarta Intl Stadium", "jakarta_international_stadium", "Jakarta International Stadium", "Jakarta", "ID", "Indonesia", "Asia", "Opened 2022", "Football", "", "Indonesia", {}),
    ("Twickenham", "twickenham_stadium", "Twickenham Stadium", "London (Allianz Stadium)", "GB", "United Kingdom", "Europe", "Opened 1909", "Rugby union", "", None, {}),
    ("Memorial Stadium Clemson", "memorial_stadium_clemson", "Memorial Stadium", "Clemson, South Carolina", "US", "United States", "North America", "Opened 1942", "American football", "", None, {}),
    ("Lambeau Field", "lambeau_field", "Lambeau Field", "Green Bay, Wisconsin", "US", "United States", "North America", "Opened 1957", "American football", "", None, {}),
    ("Luzhniki Stadium", "luzhniki_stadium", "Luzhniki Stadium", "Moscow", "RU", "Russia", "Europe", "Opened 1956", "Football", "", None, {}),
    ("Oklahoma Memorial Stadium", "oklahoma_memorial_stadium", "Oklahoma Memorial Stadium", "Norman, Oklahoma", "US", "United States", "North America", "Opened 1923", "American football", "", None, {}),
    ("Estadio Monumental (Lima)", "estadio_monumental_lima", "Estadio Monumental", "Lima (Universitario)", "PE", "Peru", "South America", "Opened 2000", "Football", "", None, {}),
    ("Guangdong Olympic Stadium", "guangdong_olympic_stadium", "Guangdong Olympic Stadium", "Guangzhou", "CN", "China", "Asia", "Opened 2001", "Football, athletics", "", None, {}),
    ("AT&T Stadium", "att_stadium", "AT&T Stadium", "Arlington, Texas", "US", "United States", "North America", "Opened 2009", "American football", "", None, {}),
    ("Stade de France", "stade_de_france", "Stade de France", "Saint-Denis, Paris", "FR", "France", "Europe", "Opened 1998", "Football, rugby", "", "France", {}),
    ("Beijing National Stadium", "beijing_national_stadium", "Beijing National Stadium", "Beijing (Bird's Nest)", "CN", "China", "Asia", "Opened 2008", "Football, athletics", "", None, {}),
    ("Hangzhou Olympic Stadium", "hangzhou_olympic_sports_centre_stadium", "Hangzhou Olympic Stadium", "Hangzhou (Big Lotus)", "CN", "China", "Asia", "Opened 2018", "Football, athletics", "", None, {}),
    ("Stade des Martyrs", "stade_des_martyrs", "Stade des Martyrs", "Kinshasa", "CD", "DR Congo", "Africa", "Opened 1994", "Football", "", "DR Congo", {}),
    ("Santiago Bernabéu", "santiago_bernabeu", "Santiago Bernabéu", "Madrid", "ES", "Spain", "Europe", "Opened 1947", "Football", "RENOVATED 2025", None, {
        "value": 78297,
        "source": {"name": "FIFA World Cup 2030 bid book / FIFA venue evaluation (Nov 2024), as reported by StadiumDB 23 Mar 2026",
                   "url": "https://stadiumdb.com/news/2026/03/spain_what_is_the_capacity_of_the_new_bernabeu_uncovering_the_secret_of_real_madrids_stadium",
                   "retrieved_at": "2026-11-03"},
        "cross_check": {"name": "LaLiga, 19 Jun 2023 ('technical capacity', before works ended)",
                        "url": "https://www.laliga.com/noticias/laliga-bate-record-historico-de-asistencia-a-los-estadios-con-mas-de-15-millones-de-espectadores",
                        "value": 83186},
        "notes": ("Real Madrid has not published a post-renovation seat count. Figures in circulation: 78,297 (2030 World Cup bid book "
                  "and FIFA evaluation, 2024), 80,000 +/- 1,000 'authorised' (Florentino Perez, 2023 assembly), 83,186 (LaLiga 2023, "
                  "during works), 84,000 (LaLiga 2024). Highest 2025/26 league crowd 78,107 (El Clasico) fits 78,297, so that is used. "
                  "Pre-works capacity 81,044.")}),
    ("Azadi Stadium", "azadi_stadium", "Azadi Stadium", "Tehran", "IR", "Iran", "Asia", "Opened 1971", "Football", "", "Iran", {}),
    ("Gelora Bung Karno", "gelora_bung_karno_stadium", "Gelora Bung Karno Stadium", "Jakarta", "ID", "Indonesia", "Asia", "Opened 1962", "Football, athletics", "", "Indonesia", {}),
    ("Notre Dame Stadium", "notre_dame_stadium", "Notre Dame Stadium", "Notre Dame, Indiana", "US", "United States", "North America", "Opened 1930", "American football", "", None, {}),
    ("Atatürk Olympic Stadium", "ataturk_olympic_stadium", "Atatürk Olympic Stadium", "Istanbul", "TR", "Turkey", "Europe", "Opened 2002", "Football, athletics", "", None, {}),
    ("Williams-Brice Stadium", "williams_brice_stadium", "Williams-Brice Stadium", "Columbia, South Carolina", "US", "United States", "North America", "Opened 1934", "American football", "", None, {}),
    ("LA Memorial Coliseum", "la_memorial_coliseum", "LA Memorial Coliseum", "Los Angeles, California", "US", "United States", "North America", "Opened 1923", "American football", "2028 OLYMPICS VENUE", None, {}),
    ("Arrowhead Stadium", "arrowhead_stadium", "Arrowhead Stadium", "Kansas City, Missouri", "US", "United States", "North America", "Opened 1972", "American football", "", None, {}),
    ("Razorback Stadium", "razorback_stadium", "Razorback Stadium", "Fayetteville, Arkansas", "US", "United States", "North America", "Opened 1938", "American football", "", None, {}),
    ("Camp Randall Stadium", "camp_randall_stadium", "Camp Randall Stadium", "Madison, Wisconsin", "US", "United States", "North America", "Opened 1917", "American football", "+100 SEATS IN 2026", None, {}),
]


def _src(r: dict) -> dict:
    s = r["source"]
    return {"name": s["name"], "url": s["url"], "period": s.get("date_or_period", ""), "retrieved_at": "2026-11-03"}


def _cross(r: dict) -> dict:
    c = r.get("cross_check") or {}
    v = c.get("value")
    out = {"name": c.get("name", ""), "url": c.get("url", ""), "value": v}
    if isinstance(v, (int, float)) and r["capacity"]:
        out["diff_pct"] = round((v - r["capacity"]) / r["capacity"] * 100, 2)
    return out


ITEMS = []
for key, slug, name, sub, iso2, country, cont, opened, use, badge, fop, ov in ROWS:
    r = R[key]
    d = {"slug": slug, "name": name, "subtitle": sub, "iso2": iso2, "country": country, "continent": cont,
         "value": int(ov.get("value", r["capacity"])), "badge": badge,
         "tags": [{"icon": "calendar", "text": opened}, {"icon": "trophy", "text": use}],
         "source": ov.get("source") or _src(r), "cross_check": ov.get("cross_check") or _cross(r),
         "notes": ov.get("notes") or "; ".join(x for x in (r.get("capacity_basis", ""), r.get("change_note", ""), r.get("notes") or "") if x),
         "opened": r.get("opened"), "use": r.get("primary_use", "")}
    if "cross_check" in ov and isinstance(ov["cross_check"].get("value"), (int, float)):
        d["cross_check"]["diff_pct"] = round((ov["cross_check"]["value"] - d["value"]) / d["value"] * 100, 2)
    if fop:
        d["fop_risk"] = FOP.format(fop)
    ITEMS.append(d)

INSIGHTS = [
    {"after_rank": 41, "text": "Five stadiums list a round 80,000 seats: in China, France, the USA and DR Congo."},
    {"after_rank": 31, "text": "Missing: Camp Nou. Mid-rebuild it has 62,652 seats open; about 105,000 are planned."},
    {"after_rank": 22, "text": "Next: Estadio Azteca, reopened in 2026: the first stadium to host three World Cup openers."},
    {"after_rank": 11, "text": "8 of the top 10 are US college football stadiums. Not one is an NFL home."},
    {"after_rank": 5, "text": "Next: Beaver Stadium. On Oct 10, 2026, temporary stands let in a record 114,419 fans."},
    {"after_rank": 3, "text": "North Korea hasn't published a seat count since its 2014 rebuild; 114,000 is an estimate."},
]


# 官方页取不到、research 以 Wikipedia 为主值来源的：有 StadiumDB 同值的改用 StadiumDB（aggregator）作主值来源、Wikipedia 作交叉核对；
# 不同值的保留 Wikipedia（其引用的官方文件）作主值，StadiumDB 作交叉核对（差异写 notes）。2026-11-03 curl 抓取。
SDB = "https://stadiumdb.com/stadiums/usa/"
SRC_OVERRIDE = {
    "cotton_bowl": ("swap", "StadiumDB – Cotton Bowl", SDB + "cotton_bowl", 92100),
    "rose_bowl": ("swap", "StadiumDB – Rose Bowl", SDB + "rose_bowl", 89702),
    "memorial_stadium_clemson": ("swap", "StadiumDB – Memorial Stadium (Clemson)", SDB + "memorial_stadium_clemson", 81500),
    "att_stadium": ("swap", "StadiumDB – AT&T Stadium", SDB + "cowboys_stadium", 80000),
    "lambeau_field": ("cross", "StadiumDB – Lambeau Field", SDB + "lambeau_field", 81041),
    "arrowhead_stadium": ("cross", "StadiumDB – Arrowhead Stadium", SDB + "arrowhead_stadium", 73426),
}
for d in ITEMS:
    o = SRC_OVERRIDE.get(d["slug"])
    if not o:
        continue
    mode, nm, url, v = o
    wiki = {"name": "Wikipedia infobox (" + d["name"] + ")", "url": d["source"]["url"], "value": d["value"]}
    sdb = {"name": nm, "url": url, "value": v, "diff_pct": round((v - d["value"]) / d["value"] * 100, 2)}
    if mode == "swap":
        d["source"] = {"name": nm + " (aggregator; official page not reachable)", "url": url, "period": "accessed 2026-11-03", "retrieved_at": "2026-11-03"}
        d["cross_check"] = {**wiki, "diff_pct": 0.0}
    else:
        d["source"]["name"] = "Wikipedia infobox, citing the team's media guide (aggregator; official page not reachable)"
        d["cross_check"] = sdb
        d["notes"] += f"; StadiumDB lists {v:,} ({sdb['diff_pct']}%), treated as outdated/other configuration."

# 屏外（描述框 / 置顶评论）用的来源名一律英文；research 里带中文注释的来源名在这里改写（中文说明保留在 research 与 notes）。
EN_SRC = {
    "rungrado_1st_of_may_stadium": "StadiumDB – Rungrado May Day Stadium (estimate; no official figure)",
    "beaver_stadium": "Georgia Football 2026 Media Guide – Top 10 Largest On-Campus Stadiums",
    "ohio_stadium": "Ohio State Football 2026 Game Notes – Ohio Stadium information",
    "misr_stadium": "StadiumDB news, Feb 2025 (no official page found)",
    "sanford_stadium": "Georgia Athletics – Dooley Field at Sanford Stadium",
    "estadio_banorte": "AP via theScore – Estadio Azteca reopening, Mar 2026",
    "borg_el_arab_stadium": "The Arab Contractors – Borg El Arab Stadium project page",
    "memorial_stadium_nebraska": "Nebraska Athletics – Memorial Stadium",
    "estadio_monumental_buenos_aires": "Emol, 28 Jan 2026 – River Plate expansion announcement",
    "accor_stadium": "Wikipedia – Stadium Australia (aggregator; official page lists no capacity)",
    "jakarta_international_stadium": "StadiumDB – Jakarta International Stadium (aggregator)",
    "twickenham_stadium": "Wikipedia – Twickenham Stadium, citing englandrugby.com (aggregator)",
    "guangdong_olympic_stadium": "Wikipedia – Guangdong Olympic Stadium (aggregator)",
    "beijing_national_stadium": "StadiumDB – Beijing National Stadium (aggregator)",
    "hangzhou_olympic_sports_centre_stadium": "Wikipedia – Hangzhou Olympic Expo Center (aggregator)",
    "stade_des_martyrs": "StadiumDB – Stade des Martyrs (aggregator)",
    "notre_dame_stadium": "Notre Dame Athletics – Notre Dame Stadium (77,622 since 2017)",
    "razorback_stadium": "Georgia Football 2026 Media Guide – Capacity of SEC Stadiums",
    "camp_randall_stadium": "Wisconsin Football 2026 Game Notes (GM9 vs Rutgers), capacities table",
}
for d in ITEMS:
    if d["slug"] in EN_SRC:
        d["source"]["name"] = EN_SRC[d["slug"]]

THUMB = {"rose_bowl", "wembley_stadium", "melbourne_cricket_ground"}   # 封面不放冠军（QC M6）
for d in ITEMS:
    if d["slug"] in THUMB:
        d["thumb"] = True
