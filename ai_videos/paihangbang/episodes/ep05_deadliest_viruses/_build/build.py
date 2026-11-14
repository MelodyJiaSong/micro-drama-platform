# -*- coding: utf-8 -*-
"""ep05 deadliest viruses：由调研结果（research/group_*.json + 代理补查）与 cumulative.json 生成 data.json。

口径（topic.md / sources.md §1）：
- T（documented）：权威机构或文献直接给出的累计数，窗口照原文。
- E（est.）：只有年度估计的病毒，按同一来源体系的 ≥2 个年度锚点逐年线性插值求和（cumulative.py），
  窗口 = 公开全球估计能支撑的最长区间；屏上标 est.。
- 只有单一年份估计（hMPV、副流感、腺病毒）、只有病例没有死亡数（脊灰、风疹、腮腺炎、CMV、HSV、HTLV-1）、
  或死亡数已并入别的病毒（丁肝并入乙肝）的不进榜。
"""
from __future__ import annotations

import json
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
CUM = json.loads((Path(__file__).parent / "cumulative.json").read_text(encoding="utf-8"))
TODAY = "2026-11-03"


def sig(v: float, est: bool) -> str:
    """bible §3.4：3 位有效数字；推算值 2 位。百万以下的有据总数直接写全数。"""
    if not est and v < 1_000_000:
        return f"{int(round(v)):,}"
    digits = 2 if est else 3
    v = float(f"{v:.{digits}g}")
    for div, suf in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
        if v >= div:
            x = v / div
            s = f"{x:.{max(0, digits - len(str(int(x))))}f}"
            if "." in s:
                s = s.rstrip("0").rstrip(".")
            return s + suf
    return f"{int(round(v)):,}"


def cum(key: str) -> float:
    return CUM[key]["value"]


# (key, name, transmission, family_tag, vaccine_tag, value, kind, window, badge, source, cross_check, notes)
#  kind: "T" documented / "E" est. / "R" reported
V = [
    ("smallpox", "Smallpox", "Airborne", "Poxvirus", "Vaccine since 1796", 300_000_000, "D", "1900–1977", "ERADICATED 1980",
     {"name": "D.A. Henderson (led WHO eradication), The eradication of smallpox, Vaccine 2011;29 Suppl 4:D7–D9", "url": "https://doi.org/10.1016/j.vaccine.2011.06.080", "tier": "peer-reviewed"},
     {"name": "Our World in Data citing Henderson 2009: 500M in its last 100 years", "url": "https://ourworldindata.org/smallpox", "value": 500_000_000},
     "Henderson calls 300M 'conservative' for the 20th century alone; 500M is for c.1877–1977. Earlier centuries uncounted."),
    ("influenza", "Influenza", "Airborne", "Orthomyxovirus", "Vaccine since 1945", 50_000_000 + 1_100_000 + 1_000_000 + 284_500, "D", "4 pandemics, 1918–2009", "",
     {"name": "CDC pandemic estimates: 1918 ~50M, 1957 1.1M, 1968 1M; 2009 284,500 (Dawood, Lancet ID 2012)", "url": "https://archive.cdc.gov/www_cdc_gov/flu/pandemic-resources/basics/past-pandemics.html", "tier": "primary"},
     {"name": "1918 range 17.4M (Spreeuwenberg 2018) to 50–100M (Johnson & Mueller 2002)", "url": "https://academic.oup.com/aje/article/187/12/2561/5092383", "value": 17_400_000},
     "Pandemics only. Seasonal flu adds 290,000–650,000 deaths a year (Iuliano, Lancet 2018) and is not included."),
    ("hiv", "HIV", "Blood & sex", "Retrovirus", "No vaccine", 44_200_000, "D", "1981–2025", "",
     {"name": "WHO/UNAIDS, HIV statistics, July 2026 (range 33.8–61.1M)", "url": "https://www.who.int/data/gho/data/themes/hiv-aids", "tier": "primary"},
     {"name": "UNAIDS 2025 release: 44.1M", "url": "https://www.unaids.org/en/resources/fact-sheet", "value": 44_100_000},
     "Each UNAIDS release re-models the whole series; one release cited."),
    ("measles", "Measles", "Airborne", "Paramyxovirus", "Vaccine since 1963", round((cum("measles") + 41_576_870) / 2, -5), "E", "1980–2024", "",
     {"name": "WHO/CDC global estimates: 1980 2.6M, 2000 780K, 2019 207.5K, 2022 136.2K, 2023 107.5K, 2024 95K (cumulative.py)", "url": "https://www.who.int/news-room/fact-sheets/detail/measles", "tier": "primary"},
     {"name": "Same anchors plus the older WHO 2010/2016/2018 series give 41.6M", "url": "https://stacks.cdc.gov/view/cdc/158140", "value": 41_576_870},
     "Midpoint of 41.6M–45.3M (two WHO series). The widely repeated '200M in 150 years' has no traceable source and is not used."),
    ("hbv", "Hepatitis B", "Blood & sex", "Hepadnavirus", "Vaccine since 1981", cum("hbv"), "E", "1990–2024", "",
     {"name": "GBD 2019 Hepatitis B Collaborators, Lancet Gastroenterol Hepatol 2022: 555K deaths in 2019, +5.9% since 1990", "url": "https://doi.org/10.1016/S2468-1253(22)00124-8", "tier": "peer-reviewed"},
     {"name": "WHO Global Hepatitis Report 2024: 1.1M deaths in 2022 (higher method)", "url": "https://www.who.int/news/item/09-04-2024-who-sounds-alarm-on-viral-hepatitis-infections-claiming-3500-lives-each-day", "value": 1_100_000},
     "Includes cirrhosis and liver cancer caused by HBV. GBD series used (conservative); WHO's newer annual figure is ~2x higher. Hepatitis D deaths sit inside this count."),
    ("rotavirus", "Rotavirus", "Food & water", "Reovirus", "Vaccine since 2006", cum("rotavirus"), "E", "1990–2024", "",
     {"name": "GBD 2019 (Du et al., Virology Journal 2022): 659K in 1990, 235K in 2019; GBD 2021: 170K", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9585833/", "tier": "peer-reviewed"},
     {"name": "Tate et al., Clin Infect Dis 2016: 528K (2000) → 215K (2013)", "url": "https://academic.oup.com/cid/article/62/suppl_2/S96/2478843", "value": 528_000},
     "Mostly children under 5, through diarrhoea."),
    ("hpv", "HPV", "Blood & sex", "Papillomavirus", "Vaccine since 2006", cum("hpv"), "E", "1990–2024", "CANCER DEATHS",
     {"name": "GBD 2019 cervical cancer (185K in 1990, 280K in 2019); GBD 2021; GLOBOCAN 2024 (280K)", "url": "https://doaj.org/article/cafdc2cb127642cea4929c407d6b0af1", "tier": "peer-reviewed"},
     {"name": "WHO cervical cancer fact sheet 2026: ~280K deaths in 2024", "url": "https://www.who.int/news-room/fact-sheets/detail/cervical-cancer", "value": 280_000},
     "Cervical cancer only (≈all cases caused by HPV). Other HPV cancers (throat, anal) not counted, so this is a floor."),
    ("covid", "COVID-19 (SARS-CoV-2)", "Airborne", "Coronavirus", "Vaccine since 2020", 7_117_689, "R", "2020–2026", "",
     {"name": "WHO COVID-19 dashboard data file, sum of reported deaths to 27 Sep 2026", "url": "https://data.who.int/dashboards/covid19/deaths", "tier": "primary"},
     {"name": "WHO excess-mortality estimate 2020–21: 14.83M (Msemburi, Nature 2023)", "url": "https://www.nature.com/articles/s41586-022-05522-2", "value": 14_830_000},
     "Reported deaths only. Excess-death models: 14.8M (WHO, 2020–21), 18.2M (IHME), 27–28.5M (The Economist, whole pandemic)."),
    ("hcv", "Hepatitis C", "Blood & sex", "Hepacivirus", "No vaccine", cum("hcv"), "E", "2013–2024", "",
     {"name": "GBD 2013 (Stanaway, Lancet 2016) 700K; GBD 2019 (Ou et al., J Infect Public Health 2024) 537K", "url": "https://doi.org/10.1016/j.jiph.2024.04.027", "tier": "peer-reviewed"},
     {"name": "WHO: 290K (2019), 242K (2022), 239K (2024)", "url": "https://www.who.int/news-room/fact-sheets/detail/hepatitis-c", "value": 239_000},
     "Includes cirrhosis and liver cancer. WHO's figures are ~half of GBD's; no global 1990 anchor found, so window starts 2013."),
    ("norovirus", "Norovirus", "Food & water", "Calicivirus", "No vaccine", cum("norovirus"), "E", "1990–2024", "",
     {"name": "GBD 2019 (Frontiers in Public Health 2022): 243K in 1990, 136K in 2019", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9247406/", "tier": "peer-reviewed"},
     {"name": "Lopman et al., PLoS Med 2016: 212K (2010)", "url": "https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1001999", "value": 212_000},
     ""),
    ("rsv", "RSV", "Airborne", "Pneumovirus", "Vaccine since 2023", cum("rsv"), "E", "1990–2024", "",
     {"name": "GBD 2021 (J Thorac Dis 2026): 140K (1990), 95K (2019), 32K (2021)", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC13190074/", "tier": "peer-reviewed"},
     {"name": "Li et al., Lancet 2022: 101K deaths in children under 5 alone (2019)", "url": "https://doi.org/10.1016/S0140-6736(22)00478-0", "value": 101_400},
     "2021 dip reflects COVID-era distancing; held flat after 2021, so a floor."),
    ("ebv", "Epstein–Barr virus", "Contact", "Herpesvirus", "No vaccine", cum("ebv"), "E", "2010–2024", "CANCER DEATHS",
     {"name": "Khan & Hashim 2014 (143K, 2010); Khan et al., BMJ Open 2020 (164K, 2017); Wong et al. 2022 (138–209K, 2020)", "url": "https://doi.org/10.1136/bmjopen-2020-037505", "tier": "peer-reviewed"},
     None, "Attributable cancer deaths (nasopharyngeal, gastric, lymphomas)."),
    ("hav", "Hepatitis A", "Food & water", "Picornavirus", "Vaccine since 1991", cum("hav"), "E", "1990–2024", "",
     {"name": "GBD 2019 (Cao et al., Hepatol Int 2021): 108K (1990), 39K (2019); WHO 2023: 35.6K", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8514357/", "tier": "peer-reviewed"},
     None, ""),
    ("dengue", "Dengue", "Mosquito & tick", "Flavivirus", "Vaccine since 2015", cum("dengue"), "E", "1990–2024", "",
     {"name": "GBD 2021 (Zhang et al., PLoS NTD 2025): 14.3K (1990), 36.1K (2019), 29.1K (2021)", "url": "https://doaj.org/article/fc984abe412d454ba203a63e2ab18cf9", "tier": "peer-reviewed"},
     {"name": "WHO reported deaths 2024: 9,404 (record cases, under-reported)", "url": "https://keele-repository.worktribe.com/output/1274792/global-dengue-epidemic-worsens-with-record-14-million-cases-and-9000-deaths-reported-in-2024", "value": 9_404},
     "Modelled deaths ~3x WHO reported deaths."),
    ("yellow_fever", "Yellow fever", "Mosquito & tick", "Flavivirus", "Vaccine since 1937", cum("yellow_fever"), "E", "2013–2024", "",
     {"name": "Garske et al., PLoS Med 2014 (78K, 2013); Gaythorpe et al., eLife 2021 (51K, 2018)", "url": "https://elifesciences.org/articles/64670", "tier": "peer-reviewed"},
     None, "Only modern global estimates; historic epidemics (Haiti 1802, Mississippi 1878) not totalled anywhere."),
    ("rabies", "Rabies", "Animals", "Rhabdovirus", "Vaccine since 1885", cum("rabies"), "E", "1990–2024", "",
     {"name": "GBD 2019 (Gan et al., IJID 2023) 13.7K; GBD 2021 (He & Tan 2025) 10.1K; GBD 1990 21.8K", "url": "https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2025.1683863/full", "tier": "peer-reviewed"},
     {"name": "Hampson et al., PLoS NTD 2015 / WHO: ~59,000 a year (would give ~2M)", "url": "https://journals.plos.org/plosntds/article?id=10.1371/journal.pntd.0003709", "value": 59_000},
     "GBD (conservative) used; WHO's 59K/yr is 4–6x higher."),
    ("varicella", "Varicella-zoster", "Airborne", "Herpesvirus", "Vaccine since 1986", cum("varicella"), "E", "1990–2024", "",
     {"name": "GBD 2021 (Wu et al., Front Public Health 2025): 15.6K (1990), 13.9K (2021); GBD 2019 14.6K", "url": "https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2025.1654535/full", "tier": "peer-reviewed"},
     None, "Chickenpox and shingles."),
    ("je", "Japanese encephalitis", "Mosquito & tick", "Flavivirus", "Vaccine since 1954", 275_792, "T", "1950–2018", "CHINA ONLY",
     {"name": "Chen et al., Biomed Environ Sci 2021;34(3): JE in China 1950–2018", "url": "https://www.besjournal.com/cn/article/doi/10.3967/bes2021.024", "tier": "peer-reviewed"},
     {"name": "Quan et al., eLife 2020: ~25,000 deaths a year across Asia (2015)", "url": "https://elifesciences.org/articles/51027", "value": 25_125},
     "Mainland China reported deaths only; no pan-Asian total exists."),
    ("kshv", "Kaposi sarcoma virus", "Contact", "Herpesvirus", "No vaccine", cum("kshv"), "E", "2020–2024", "CANCER DEATHS",
     {"name": "Fu et al., Lancet Glob Health 2023 (15.1K, 2020); GLOBOCAN 2024 (10.7K)", "url": "https://doi.org/10.1016/s2214-109x(23)00349-2", "tier": "peer-reviewed"},
     None, "KSHV/HHV-8 causes all Kaposi sarcoma; most of these deaths also involve HIV."),
    ("hanta", "Hantavirus", "Animals", "Hantavirus", "Vaccine since 1990", 46_427, "T", "1950–2007", "CHINA ONLY",
     {"name": "Zhang et al., Emerging Infectious Diseases 2010;16(8): HFRS in China 1950–2007", "url": "https://wwwnc.cdc.gov/eid/article/16/8/09-0470_article", "tier": "peer-reviewed"},
     None, "Haemorrhagic fever with renal syndrome, China only. Korea, Russia and the Americas not totalled."),
    ("hev", "Hepatitis E", "Food & water", "Hepevirus", "Vaccine since 2011", cum("hev"), "E", "2021–2024", "",
     {"name": "GBD 2021 (3,450) and WHO 2023 (4,431)", "url": "https://www.who.int/news-room/fact-sheets/detail/hepatitis-e", "tier": "primary"},
     {"name": "Older WHO estimate: 44,000 a year (2015)", "url": "https://www.who.int/news-room/fact-sheets/detail/hepatitis-e", "value": 44_000},
     "Older estimates (70K in 2005, 44K in 2015) used a different method; only the current series is summed."),
    ("ebola", "Ebola", "Contact", "Filovirus", "Vaccine since 2019", 15_465 + 4 + 45, "T", "1976–2025", "",
     {"name": "UKHSA outbreak table (4,142 deaths outside West Africa to Jan 2023) + West Africa 2014–16 (11,323, WHO) + Uganda 2025 (4) + DRC Kasai 2025 (45)", "url": "https://www.gov.uk/government/publications/ebola-origins-reservoirs-transmission-and-guidelines/ebola-overview-history-origins-and-transmission", "tier": "primary"},
     {"name": "WHO AFRO: DRC 16th outbreak over, 45 deaths (Dec 2025)", "url": "https://afro.who.int/countries/democratic-republic-congo/news/democratic-republic-congo-declares-end-16th-ebola-outbreak", "value": 45},
     "Sum of outbreak totals (all Ebola species)."),
    ("ev71", "Hand-foot-mouth viruses", "Contact", "Enteroviruses (EV-A71)", "Vaccine since 2015", 3_632, "T", "2008–2017", "CHINA ONLY",
     {"name": "Chinese HFMD surveillance analysis 2008–2017, Journal of Disease Surveillance: all HFMD deaths", "url": "https://www.jbjc.org/en/article/doi/10.3784/jbjc.202107090395", "tier": "peer-reviewed"},
     {"name": "Xing et al., Lancet ID 2014: 2,457 HFMD deaths 2008–2012", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4035015/", "value": 2_457},
     "All hand, foot and mouth disease deaths in mainland China (several enteroviruses; EV-A71 is the main cause of fatal cases), so the card is named for the virus group. Vaccine year = EV-A71 vaccines (China)."),
    ("wnv", "West Nile virus", "Mosquito & tick", "Flavivirus", "No vaccine", 2_330, "T", "1999–2018", "US ONLY",
     {"name": "CDC ArboNET yearly death counts 1999–2018 summed (2,330), as tabulated in Wikipedia's list of West Nile outbreaks", "url": "https://en.wikipedia.org/wiki/List_of_West_Nile_virus_outbreaks", "tier": "aggregator"},
     {"name": "CIDNI 2026 lecture citing CDC: about 3,000 US deaths 1999–2024", "url": "https://cidni.org/wp-content/uploads/2026/08/West_Nile_Virus_Nursing_Talk_1.pdf", "value": 3_000},
     "United States only, through 2018 (last CDC-based cumulative total found); later US deaths and Europe are not included."),
    ("tbe", "Tick-borne encephalitis", "Mosquito & tick", "Flavivirus", "Vaccine since 1976", 1_136, "T", "2000–2022", "RUSSIA ONLY",
     {"name": "Dzagurova et al., Epidemiology and Vaccinal Prevention 2024;23(5) (Russia, TBE 2000–2022)", "url": "https://www.epidemvac.ru/jour/article/download/2087/1073", "tier": "peer-reviewed"},
     None, "Russia only."),
    ("mers", "MERS", "Animals", "Coronavirus", "No vaccine", 960, "T", "2012–2026", "",
     {"name": "ECDC MERS-CoV worldwide overview, 2 July 2026: 2,649 cases, 960 deaths", "url": "https://www.ecdc.europa.eu/en/middle-east-respiratory-syndrome-coronavirus/threats-and-outbreaks", "tier": "primary"},
     {"name": "WHO DON May 2020: 876 deaths to Mar 2020", "url": "https://www.who.int/emergencies/disease-outbreak-news", "value": 876},
     "Camels are the source; most cases in Saudi Arabia."),
    ("sars", "SARS (SARS-CoV-1)", "Airborne", "Coronavirus", "No vaccine", 774, "T", "2002–2003", "",
     {"name": "WHO summary of probable SARS cases, Nov 2002–Jul 2003: 8,096 cases, 774 deaths", "url": "https://www.who.int/publications/m/item/summary-of-probable-sars-cases-with-onset-of-illness-from-1-november-2002-to-31-july-2003", "tier": "primary"},
     None, "No human cases since 2004."),
    ("marburg", "Marburg virus", "Contact", "Filovirus", "No vaccine", 479 + 2 + 35 + 6 + 15 + 10 + 9 + 5, "T", "1967–2025", "",
     {"name": "WHO tally 1967–2021 (479) + Ghana 2022 (2) + Eq. Guinea 2023 (35 incl. probable) + Tanzania 2023 (6) + Rwanda 2024 (15) + Tanzania 2025 (10) + Ethiopia 2025 (9 confirmed + 5 probable)", "url": "https://www.cdc.gov/marburg/outbreaks/index.html", "tier": "primary"},
     None, "Sum of outbreak totals; probable deaths counted where WHO reported them."),
    ("cchf", "Crimean-Congo fever", "Mosquito & tick", "Nairovirus", "No vaccine", 469, "T", "2002–2017", "TURKEY ONLY",
     {"name": "Peer-reviewed table: Turkey 2002–2017, 10,333 cases, 469 deaths (PMC6335890)", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6335890/", "tier": "peer-reviewed"},
     {"name": "Leblebicioglu et al. 2016: >9,700 patients, mortality <5%", "url": "https://acikerisim.omu.edu.tr/entities/publication/d1057151-ffb8-4835-9dda-58127a9e4b4d/full", "value": 480},
     "Turkey only (largest documented series). Tick-borne."),
    ("nipah", "Nipah virus", "Animals", "Paramyxovirus", "No vaccine", 435, "T", "1998–2024", "",
     {"name": "2024 geospatial study: 754 cases, 435 deaths in 5 countries through May 2024", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11414670/", "tier": "peer-reviewed"},
     None, "A handful more deaths since (Kerala 2024–25, Bangladesh 2025–26)."),
]

TAG_ICON = {"family": "virus", "vaccine": "vaccine"}
KIND_SEC = {"T": "", "D": "est.", "E": "est.", "R": "reported"}


def build() -> dict:
    rows = sorted(V, key=lambda r: -r[5])
    items = []
    for rank, r in enumerate(rows, 1):
        key, name, route, fam, vac, value, kind, window, badge, src, xc, notes = r
        it = {
            "rank": rank, "key": key, "name": name, "subtitle": "",
            "country_iso2": "", "country_name": f"Deaths · {window}", "continent": route,
            "value": value, "value_display": sig(value, kind == "E"), "secondary_display": KIND_SEC[kind],
            "badge": badge,
            "tags": [{"icon": "virus", "text": fam}, {"icon": "vaccine", "text": vac}],
            "source": {**src, "retrieved_at": TODAY},
            "value_kind": {"T": "counted (documented total)", "D": "published modelled estimate", "E": "estimated (cumulative.py)", "R": "reported"}[kind],
            "notes": notes,
        }
        if kind == "E":
            it["cumulative"] = CUM[key]
        if xc:
            it["cross_check"] = {**xc, "diff_pct": round(100 * (xc["value"] - value) / value, 1)}
        items.append(it)
    by = {it["key"]: it["rank"] for it in items}
    data = {
        "episode": "ep05_deadliest_viruses",
        "title": "Deadliest Viruses in History",
        "youtube_title": "Deadliest Viruses in History | Top 30 by Death Toll",
        "music_credit": "Music: original instrumental generated for this channel with Suno (job 90bd9426, clip 00fb676e).",
        "kicker": "TOP 30",
        "metric_label": "Deaths",
        "unit": "",
        "period_label": "est. = modelled estimate · years vary by virus · Nov 2026",
        "source_line": "Sources: WHO, UNAIDS, CDC, GBD (Lancet), peer-reviewed studies",
        "theme": "virus",
        "tally": {"by": "continent", "title": "How they spread", "icons": {"Airborne": "wind", "Blood & sex": "droplet", "Mosquito & tick": "bug", "Food & water": "bottle", "Animals": "paw", "Contact": "hand-stop"}},
        "layout": {"card_w": 720, "focus": [0.5, 0.5], "flags": False},
        "scope_note": ("Viruses only (no plague, TB, malaria). Each card shows its own years: est. = modelled estimate (published, or yearly "
                       "GBD/WHO estimates summed); no tag = counted deaths. Windows differ, so this ranks recorded deaths, and old or neglected viruses "
                       "are undercounted (measles before 1980, smallpox before 1900). Hepatitis B/C include liver cancer; HPV = cervical cancer only. "
                       "Badged totals cover one country. Polio, rubella and others without death estimates are left out."),
        "items": items,
        "insights": [
            {"after_rank": by["nipah"], "text": "How to read: est. = modelled estimate, no tag = counted deaths. Years differ per card."},
            {"after_rank": by["sars"], "text": "Rare viruses are barely tracked: several counts here cover only one country."},
            {"after_rank": by["ebola"], "text": "Ebola, SARS, MERS and Marburg together killed fewer than 18,000 people."},
            {"after_rank": by["rabies"], "text": "Rabies is almost always fatal once symptoms start, yet a vaccine has existed since 1885."},
            {"after_rank": by["covid"], "text": "COVID-19's reported toll is 7.1M. Excess-death studies put it at 15–28M."},
            {"after_rank": by["measles"], "text": "Measles and HIV are neck and neck, and measles is only counted from 1980."},
            {"after_rank": by["influenza"], "text": "Smallpox is the only human disease ever eradicated. Its last natural case was in 1977."},
        ],
    }
    return data


if __name__ == "__main__":
    d = build()
    old = EP / "data.json"
    if old.exists():   # 保留第二步（出图）写进去的图片字段
        prev = {it["key"]: it for it in json.loads(old.read_text(encoding="utf-8"))["items"]}
        for it in d["items"]:
            for k in ("image", "image_credit", "image_focus", "image_risk", "image_note"):
                if k in prev.get(it["key"], {}):
                    it[k] = prev[it["key"]][k]
    old.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for it in d["items"]:
        print(f"#{it['rank']:2d} {it['name']:24s} {it['value_display']:>7s} {it['secondary_display']:9s} {it['country_name']:32s} {it['badge']}")
