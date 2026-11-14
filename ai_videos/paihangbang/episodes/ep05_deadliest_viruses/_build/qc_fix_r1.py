# -*- coding: utf-8 -*-
"""第 1 轮独立审片（qc.md D1–D13）的数据修正，一次性改 build.py 源表。重复运行安全（已改过的跳过）。"""
from pathlib import Path

p = Path(__file__).with_name("build.py")
s = p.read_text(encoding="utf-8")
R = [
    # D2：已发表的模型估计也标 est.
    ('300_000_000, "T", "1900–1977"', '300_000_000, "D", "1900–1977"'),
    ('50_000_000 + 1_100_000 + 1_000_000 + 284_500, "T"', '50_000_000 + 1_100_000 + 1_000_000 + 284_500, "D"'),
    ('44_200_000, "T", "1981–2025"', '44_200_000, "D", "1981–2025"'),
    ('KIND_SEC = {"T": "", "E": "est.", "R": "reported"}', 'KIND_SEC = {"T": "", "D": "est.", "E": "est.", "R": "reported"}'),
    ('"value_kind": {"T": "documented", "E": "estimated (cumulative.py)", "R": "reported"}[kind]',
     '"value_kind": {"T": "counted (documented total)", "D": "published modelled estimate", "E": "estimated (cumulative.py)", "R": "reported"}[kind]'),
    # D3：具体论文页
    ('"url": "https://virologyj.biomedcentral.com/"', '"url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9585833/"'),
    ('"url": "https://gco.iarc.who.int/", "tier": "peer-reviewed"},\n     {"name": "WHO cervical',
     '"url": "https://doaj.org/article/cafdc2cb127642cea4929c407d6b0af1", "tier": "peer-reviewed"},\n     {"name": "WHO cervical'),
    ('"url": "https://www.frontiersin.org/journals/public-health", "tier": "peer-reviewed"},\n     {"name": "Lopman',
     '"url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9247406/", "tier": "peer-reviewed"},\n     {"name": "Lopman'),
    ('"url": "https://jtd.amegroups.org/"', '"url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC13190074/"'),
    ('"url": "https://www.who.int/news-room/fact-sheets/detail/hepatitis-a", "tier": "peer-reviewed"}',
     '"url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8514357/", "tier": "peer-reviewed"}'),
    ('"url": "https://journals.plos.org/plosntds/", "tier": "peer-reviewed"}',
     '"url": "https://doaj.org/article/fc984abe412d454ba203a63e2ab18cf9", "tier": "peer-reviewed"}'),
    ('"url": "https://www.frontiersin.org/journals/public-health", "tier": "peer-reviewed"},\n     {"name": "Hampson',
     '"url": "https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2025.1683863/full", "tier": "peer-reviewed"},\n     {"name": "Hampson'),
    ('"url": "https://www.frontiersin.org/journals/public-health", "tier": "peer-reviewed"},\n     None, "Chickenpox',
     '"url": "https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2025.1654535/full", "tier": "peer-reviewed"},\n     None, "Chickenpox'),
    ('"url": "https://www.besjournal.com/"', '"url": "https://www.besjournal.com/cn/article/doi/10.3967/bes2021.024"'),
    ('"url": "https://wwwnc.cdc.gov/eid/article/16/8/09-1745_article"', '"url": "https://wwwnc.cdc.gov/eid/article/16/8/09-0470_article"'),
    ('"url": "https://www.epidemvac.ru/"', '"url": "https://www.epidemvac.ru/jour/article/download/2087/1073"'),
    ('"url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10413696/"', '"url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11414670/"'),
    ('"url": "https://bmjopen.bmj.com/content/10/8/e037505"', '"url": "https://doi.org/10.1136/bmjopen-2020-037505"'),
    ('"url": "https://gco.iarc.who.int/", "tier": "peer-reviewed"},\n     None, "KSHV',
     '"url": "https://doi.org/10.1016/s2214-109x(23)00349-2", "tier": "peer-reviewed"},\n     None, "KSHV'),
    ('"url": "https://www.who.int/emergencies/disease-outbreak-news", "value": 9_404}',
     '"url": "https://keele-repository.worktribe.com/output/1274792/global-dengue-epidemic-worsens-with-record-14-million-cases-and-9000-deaths-reported-in-2024", "value": 9_404}'),
    # D1：3,632 是中国全部手足口病死亡，不是 EV-A71 一种
    ('("ev71", "Enterovirus A71", "Food & water", "Picornavirus", "Vaccine since 2015", 3_632, "T", "2008–2017", "CHINA ONLY",\n'
     '     {"name": "China HFMD surveillance 2008–2017 (all HFMD deaths; EV-A71 caused ~90%)", "url": "https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(13)70342-6/fulltext", "tier": "peer-reviewed"},\n'
     '     {"name": "Xing et al., Lancet ID 2014: 2,457 deaths 2008–2012", "url": "https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(13)70342-6/fulltext", "value": 2_457},\n'
     '     "Hand, foot and mouth disease deaths, mainland China."),',
     '("ev71", "Hand-foot-mouth viruses", "Contact", "Enteroviruses (EV-A71)", "Vaccine since 2015", 3_632, "T", "2008–2017", "CHINA ONLY",\n'
     '     {"name": "Chinese HFMD surveillance analysis 2008–2017, Journal of Disease Surveillance: all HFMD deaths", "url": "https://www.jbjc.org/en/article/doi/10.3784/jbjc.202107090395", "tier": "peer-reviewed"},\n'
     '     {"name": "Xing et al., Lancet ID 2014: 2,457 HFMD deaths 2008–2012", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4035015/", "value": 2_457},\n'
     '     "All hand, foot and mouth disease deaths in mainland China (several enteroviruses; EV-A71 is the main cause of fatal cases), so the card is named for the virus group. Vaccine year = EV-A71 vaccines (China)."),'),
    # D6：西尼罗改用 CDC 数据的 1999–2018 总数，不用讲座 PDF 的约数
    ('("wnv", "West Nile virus", "Mosquito & tick", "Flavivirus", "No vaccine", 3_000, "T", "1999–2024", "US ONLY",\n'
     '     {"name": "CDC ArboNET via CIDNI 2026 lecture: ~3,000 US deaths since 1999", "url": "https://cidni.org/wp-content/uploads/2026/08/West_Nile_Virus_Nursing_Talk_1.pdf", "tier": "aggregator"},\n'
     '     {"name": "CDC data via Wikipedia: 2,330 deaths 1999–2018", "url": "https://en.wikipedia.org/wiki/List_of_West_Nile_virus_outbreaks", "value": 2_330},\n'
     '     "United States only; Europe adds ~100+/yr recently. Approximate."),',
     '("wnv", "West Nile virus", "Mosquito & tick", "Flavivirus", "No vaccine", 2_330, "T", "1999–2018", "US ONLY",\n'
     '     {"name": "CDC ArboNET annual totals 1999–2018 (50,830 cases, 2,330 deaths), as tabulated from CDC data", "url": "https://www.cdc.gov/west-nile-virus/data-maps/historic-data.html", "tier": "aggregator"},\n'
     '     {"name": "CIDNI 2026 lecture citing CDC: about 3,000 US deaths 1999–2024", "url": "https://cidni.org/wp-content/uploads/2026/08/West_Nile_Virus_Nursing_Talk_1.pdf", "value": 3_000},\n'
     '     "United States only, through 2018 (last CDC-based cumulative total found); later US deaths and Europe are not included."),'),
    # D7：马尔堡埃塞俄比亚补 5 例 probable
    ('479 + 2 + 35 + 6 + 15 + 10 + 9, "T"', '479 + 2 + 35 + 6 + 15 + 10 + 9 + 5, "T"'),
    ('Tanzania 2025 (10) + Ethiopia 2025 (9)"', 'Tanzania 2025 (10) + Ethiopia 2025 (9 confirmed + 5 probable)"'),
    # D9：标签与命名
    ('("hcv", "Hepatitis C", "Blood & sex", "Flavivirus"', '("hcv", "Hepatitis C", "Blood & sex", "Hepacivirus"'),
    ('"Varicella-zoster", "Airborne", "Herpesvirus", "Vaccine since 1974"', '"Varicella-zoster", "Airborne", "Herpesvirus", "Vaccine since 1986"'),
    ('("covid", "SARS-CoV-2", "Airborne"', '("covid", "COVID-19 (SARS-CoV-2)", "Airborne"'),
    ('("sars", "SARS", "Airborne"', '("sars", "SARS (SARS-CoV-1)", "Airborne"'),
    # D2：片头统计行、方法洞察卡、描述框口径说明
    ('"period_label": "Best documented estimates · Nov 2026",', '"period_label": "est. = modelled estimate · years vary by virus · Nov 2026",'),
    ('        "insights": [\n            {"after_rank": by["sars"]',
     '        "insights": [\n            {"after_rank": by["nipah"], "text": "How to read: est. = modelled estimate, no tag = counted deaths. Years differ per card."},\n            {"after_rank": by["sars"]'),
]
done = 0
for old, new in R:
    if new in s:
        continue
    assert s.count(old) == 1, (old[:80], s.count(old))
    s = s.replace(old, new)
    done += 1
a = s.index('        "scope_note": (')
b = s.index('"items": items,')
s = s[:a] + '''        "scope_note": ("Viruses only (no plague, TB, malaria). Each card shows its own years: est. = modelled estimate (published, or yearly "
                       "GBD/WHO estimates summed); no tag = counted deaths. Windows differ, so this ranks recorded deaths, and old or neglected viruses "
                       "are undercounted (measles before 1980, smallpox before 1900). Hepatitis B/C include liver cancer; HPV = cervical cancer only. "
                       "Badged totals cover one country. Polio, rubella and others without death estimates are left out."),
        ''' + s[b:]
p.write_text(s, encoding="utf-8")
print("replacements:", done)
