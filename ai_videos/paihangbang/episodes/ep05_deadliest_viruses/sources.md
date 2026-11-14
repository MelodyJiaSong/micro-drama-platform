# ep05 · 出处与核对

> 由 `_build/gen_sources.py` 从 `data.json` 生成，取数日 2026-11-03。调研原始记录（含原文引句）在 `_build/research/group_{a,b,c}.json`。

## §1 口径

- **documented**：机构或文献直接给出的累计数，窗口照原文。
- **est.**：同一来源体系 ≥2 个全球年度估计为锚点，逐年线性插值后对窗口内每年求和；窗口两端超出锚点的年份按最近锚点持平（`_build/cumulative.py`，结果 `cumulative.json`）。屏上 2 位有效数字。
- **reported**：官方报告病例死亡（新冠）。
- 只收病毒；晚期并发症（肝硬化、肝癌、宫颈癌等）算入，徽章与 notes 写明；单一国家的总数在卡上标 ONLY 徽章。

## §2 逐条

### #1 Smallpox — 300M est.（1900–1977，published modelled estimate）
- 主值：300,000,000；来源：D.A. Henderson (led WHO eradication), The eradication of smallpox, Vaccine 2011;29 Suppl 4:D7–D9（peer-reviewed）<https://doi.org/10.1016/j.vaccine.2011.06.080>
- 交叉核对：Our World in Data citing Henderson 2009: 500M in its last 100 years = 500,000,000（与主值差 66.7%）<https://ourworldindata.org/smallpox>
- 备注：Henderson calls 300M 'conservative' for the 20th century alone; 500M is for c.1877–1977. Earlier centuries uncounted.
- 传播途径（计分板）：Airborne；标签：Poxvirus / Vaccine since 1796；徽章：ERADICATED 1980

### #2 Influenza — 52.4M est.（4 pandemics, 1918–2009，published modelled estimate）
- 主值：52,384,500；来源：CDC pandemic estimates: 1918 ~50M, 1957 1.1M, 1968 1M; 2009 284,500 (Dawood, Lancet ID 2012)（primary）<https://archive.cdc.gov/www_cdc_gov/flu/pandemic-resources/basics/past-pandemics.html>
- 交叉核对：1918 range 17.4M (Spreeuwenberg 2018) to 50–100M (Johnson & Mueller 2002) = 17,400,000（与主值差 -66.8%）<https://academic.oup.com/aje/article/187/12/2561/5092383>
- 备注：Pandemics only. Seasonal flu adds 290,000–650,000 deaths a year (Iuliano, Lancet 2018) and is not included.
- 传播途径（计分板）：Airborne；标签：Orthomyxovirus / Vaccine since 1945

### #3 HIV — 44.2M est.（1981–2025，published modelled estimate）
- 主值：44,200,000；来源：WHO/UNAIDS, HIV statistics, July 2026 (range 33.8–61.1M)（primary）<https://www.who.int/data/gho/data/themes/hiv-aids>
- 交叉核对：UNAIDS 2025 release: 44.1M = 44,100,000（与主值差 -0.2%）<https://www.unaids.org/en/resources/fact-sheet>
- 备注：Each UNAIDS release re-models the whole series; one release cited.
- 传播途径（计分板）：Blood & sex；标签：Retrovirus / No vaccine

### #4 Measles — 43M est.（1980–2024，estimated (cumulative.py)）
- 主值：43,400,000；来源：WHO/CDC global estimates: 1980 2.6M, 2000 780K, 2019 207.5K, 2022 136.2K, 2023 107.5K, 2024 95K (cumulative.py)（primary）<https://www.who.int/news-room/fact-sheets/detail/measles>
- 推算锚点（WHO/CDC 全球估计）：1980: 2,600,000，2000: 780,000，2019: 207,500，2022: 136,200，2023: 107,500，2024: 95,000；窗口 1980–2024
- 交叉核对：Same anchors plus the older WHO 2010/2016/2018 series give 41.6M = 41,576,870（与主值差 -4.2%）<https://stacks.cdc.gov/view/cdc/158140>
- 备注：Midpoint of 41.6M–45.3M (two WHO series). The widely repeated '200M in 150 years' has no traceable source and is not used.
- 传播途径（计分板）：Airborne；标签：Paramyxovirus / Vaccine since 1963

### #5 Hepatitis B — 19M est.（1990–2024，estimated (cumulative.py)）
- 主值：18,960,000；来源：GBD 2019 Hepatitis B Collaborators, Lancet Gastroenterol Hepatol 2022: 555K deaths in 2019, +5.9% since 1990（peer-reviewed）<https://doi.org/10.1016/S2468-1253(22)00124-8>
- 推算锚点（GBD 2019（1990 值由 2019 值与 +5.9% 反推））：1990: 524,000，2019: 555,000；窗口 1990–2024
- 交叉核对：WHO Global Hepatitis Report 2024: 1.1M deaths in 2022 (higher method) = 1,100,000（与主值差 -94.2%）<https://www.who.int/news/item/09-04-2024-who-sounds-alarm-on-viral-hepatitis-infections-claiming-3500-lives-each-day>
- 备注：Includes cirrhosis and liver cancer caused by HBV. GBD series used (conservative); WHO's newer annual figure is ~2x higher. Hepatitis D deaths sit inside this count.
- 传播途径（计分板）：Blood & sex；标签：Hepadnavirus / Vaccine since 1981

### #6 Rotavirus — 14M est.（1990–2024，estimated (cumulative.py)）
- 主值：14,298,425；来源：GBD 2019 (Du et al., Virology Journal 2022): 659K in 1990, 235K in 2019; GBD 2021: 170K（peer-reviewed）<https://pmc.ncbi.nlm.nih.gov/articles/PMC9585833/>
- 推算锚点（GBD 2019 / GBD 2021）：1990: 659,053，2019: 235,331，2021: 170,000；窗口 1990–2024
- 交叉核对：Tate et al., Clin Infect Dis 2016: 528K (2000) → 215K (2013) = 528,000（与主值差 -96.3%）<https://academic.oup.com/cid/article/62/suppl_2/S96/2478843>
- 备注：Mostly children under 5, through diarrhoea.
- 传播途径（计分板）：Food & water；标签：Reovirus / Vaccine since 2006

### #7 HPV — 8.4M est.（1990–2024，estimated (cumulative.py)）
- 主值：8,416,163；来源：GBD 2019 cervical cancer (185K in 1990, 280K in 2019); GBD 2021; GLOBOCAN 2024 (280K)（peer-reviewed）<https://doaj.org/article/cafdc2cb127642cea4929c407d6b0af1>
- 推算锚点（GBD 宫颈癌 + GLOBOCAN 2024）：1990: 184,527，2019: 280,479，2021: 296,667，2024: 279,583；窗口 1990–2024
- 交叉核对：WHO cervical cancer fact sheet 2026: ~280K deaths in 2024 = 280,000（与主值差 -96.7%）<https://www.who.int/news-room/fact-sheets/detail/cervical-cancer>
- 备注：Cervical cancer only (≈all cases caused by HPV). Other HPV cancers (throat, anal) not counted, so this is a floor.
- 传播途径（计分板）：Blood & sex；标签：Papillomavirus / Vaccine since 2006；徽章：CANCER DEATHS

### #8 COVID-19 (SARS-CoV-2) — 7.12M reported（2020–2026，reported）
- 主值：7,117,689；来源：WHO COVID-19 dashboard data file, sum of reported deaths to 27 Sep 2026（primary）<https://data.who.int/dashboards/covid19/deaths>
- 交叉核对：WHO excess-mortality estimate 2020–21: 14.83M (Msemburi, Nature 2023) = 14,830,000（与主值差 108.4%）<https://www.nature.com/articles/s41586-022-05522-2>
- 备注：Reported deaths only. Excess-death models: 14.8M (WHO, 2020–21), 18.2M (IHME), 27–28.5M (The Economist, whole pandemic).
- 传播途径（计分板）：Airborne；标签：Coronavirus / Vaccine since 2020

### #9 Hepatitis C — 7M est.（2013–2024，estimated (cumulative.py)）
- 主值：7,013,080；来源：GBD 2013 (Stanaway, Lancet 2016) 700K; GBD 2019 (Ou et al., J Infect Public Health 2024) 537K（peer-reviewed）<https://doi.org/10.1016/j.jiph.2024.04.027>
- 推算锚点（GBD 2013（Stanaway 2016）/ GBD 2019（Ou 2024））：2013: 700,000，2019: 536,833；窗口 2013–2024
- 交叉核对：WHO: 290K (2019), 242K (2022), 239K (2024) = 239,000（与主值差 -96.6%）<https://www.who.int/news-room/fact-sheets/detail/hepatitis-c>
- 备注：Includes cirrhosis and liver cancer. WHO's figures are ~half of GBD's; no global 1990 anchor found, so window starts 2013.
- 传播途径（计分板）：Blood & sex；标签：Hepacivirus / No vaccine

### #10 Norovirus — 6.4M est.（1990–2024，estimated (cumulative.py)）
- 主值：6,360,900；来源：GBD 2019 (Frontiers in Public Health 2022): 243K in 1990, 136K in 2019（peer-reviewed）<https://pmc.ncbi.nlm.nih.gov/articles/PMC9247406/>
- 推算锚点（GBD 2019）：1990: 242,996，2019: 135,798；窗口 1990–2024
- 交叉核对：Lopman et al., PLoS Med 2016: 212K (2010) = 212,000（与主值差 -96.7%）<https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1001999>
- 传播途径（计分板）：Food & water；标签：Calicivirus / No vaccine

### #11 RSV — 3.7M est.（1990–2024，estimated (cumulative.py)）
- 主值：3,709,522；来源：GBD 2021 (J Thorac Dis 2026): 140K (1990), 95K (2019), 32K (2021)（peer-reviewed）<https://pmc.ncbi.nlm.nih.gov/articles/PMC13190074/>
- 推算锚点（GBD 2021）：1990: 139,762，2019: 94,918，2021: 31,525；窗口 1990–2024
- 交叉核对：Li et al., Lancet 2022: 101K deaths in children under 5 alone (2019) = 101,400（与主值差 -97.3%）<https://doi.org/10.1016/S0140-6736(22)00478-0>
- 备注：2021 dip reflects COVID-era distancing; held flat after 2021, so a floor.
- 传播途径（计分板）：Airborne；标签：Pneumovirus / Vaccine since 2023

### #12 Epstein–Barr virus — 2.4M est.（2010–2024，estimated (cumulative.py)）
- 主值：2,431,716；来源：Khan & Hashim 2014 (143K, 2010); Khan et al., BMJ Open 2020 (164K, 2017); Wong et al. 2022 (138–209K, 2020)（peer-reviewed）<https://doi.org/10.1136/bmjopen-2020-037505>
- 推算锚点（归因癌症死亡：Khan 2014 / Khan 2020 / Wong 2022（区间中点））：2010: 142,979，2017: 164,000，2020: 173,300；窗口 2010–2024
- 备注：Attributable cancer deaths (nasopharyngeal, gastric, lymphomas).
- 传播途径（计分板）：Contact；标签：Herpesvirus / No vaccine；徽章：CANCER DEATHS

### #13 Hepatitis A — 2.4M est.（1990–2024，estimated (cumulative.py)）
- 主值：2,391,412；来源：GBD 2019 (Cao et al., Hepatol Int 2021): 108K (1990), 39K (2019); WHO 2023: 35.6K（peer-reviewed）<https://pmc.ncbi.nlm.nih.gov/articles/PMC8514357/>
- 推算锚点（GBD 2019 + WHO 2023）：1990: 107,920，2019: 39,280，2023: 35,569；窗口 1990–2024
- 传播途径（计分板）：Food & water；标签：Picornavirus / Vaccine since 1991

### #14 Dengue — 900K est.（1990–2024，estimated (cumulative.py)）
- 主值：904,415；来源：GBD 2021 (Zhang et al., PLoS NTD 2025): 14.3K (1990), 36.1K (2019), 29.1K (2021)（peer-reviewed）<https://doaj.org/article/fc984abe412d454ba203a63e2ab18cf9>
- 推算锚点（GBD 2021）：1990: 14,315，2019: 36,055，2021: 29,075；窗口 1990–2024
- 交叉核对：WHO reported deaths 2024: 9,404 (record cases, under-reported) = 9,404（与主值差 -99.0%）<https://keele-repository.worktribe.com/output/1274792/global-dengue-epidemic-worsens-with-record-14-million-cases-and-9000-deaths-reported-in-2024>
- 备注：Modelled deaths ~3x WHO reported deaths.
- 传播途径（计分板）：Mosquito & tick；标签：Flavivirus / Vaccine since 2015

### #15 Yellow fever — 690K est.（2013–2024，estimated (cumulative.py)）
- 主值：693,000；来源：Garske et al., PLoS Med 2014 (78K, 2013); Gaythorpe et al., eLife 2021 (51K, 2018)（peer-reviewed）<https://elifesciences.org/articles/64670>
- 推算锚点（Garske 2014 / Gaythorpe 2021）：2013: 78,000，2018: 51,000；窗口 2013–2024
- 备注：Only modern global estimates; historic epidemics (Haiti 1802, Mississippi 1878) not totalled anywhere.
- 传播途径（计分板）：Mosquito & tick；标签：Flavivirus / Vaccine since 1937

### #16 Rabies — 590K est.（1990–2024，estimated (cumulative.py)）
- 主值：585,484；来源：GBD 2019 (Gan et al., IJID 2023) 13.7K; GBD 2021 (He & Tan 2025) 10.1K; GBD 1990 21.8K（peer-reviewed）<https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2025.1683863/full>
- 推算锚点（GBD 2019 / GBD 2021）：1990: 21,806，2019: 13,743，2021: 10,084；窗口 1990–2024
- 交叉核对：Hampson et al., PLoS NTD 2015 / WHO: ~59,000 a year (would give ~2M) = 59,000（与主值差 -89.9%）<https://journals.plos.org/plosntds/article?id=10.1371/journal.pntd.0003709>
- 备注：GBD (conservative) used; WHO's 59K/yr is 4–6x higher.
- 传播途径（计分板）：Animals；标签：Rhabdovirus / Vaccine since 1885

### #17 Varicella-zoster — 520K est.（1990–2024，estimated (cumulative.py)）
- 主值：522,756；来源：GBD 2021 (Wu et al., Front Public Health 2025): 15.6K (1990), 13.9K (2021); GBD 2019 14.6K（peer-reviewed）<https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2025.1654535/full>
- 推算锚点（GBD 2019 / GBD 2021）：1990: 15,633，2019: 14,553，2021: 13,931；窗口 1990–2024
- 备注：Chickenpox and shingles.
- 传播途径（计分板）：Airborne；标签：Herpesvirus / Vaccine since 1986

### #18 Japanese encephalitis — 275,792 （1950–2018，counted (documented total)）
- 主值：275,792；来源：Chen et al., Biomed Environ Sci 2021;34(3): JE in China 1950–2018（peer-reviewed）<https://www.besjournal.com/cn/article/doi/10.3967/bes2021.024>
- 交叉核对：Quan et al., eLife 2020: ~25,000 deaths a year across Asia (2015) = 25,125（与主值差 -90.9%）<https://elifesciences.org/articles/51027>
- 备注：Mainland China reported deaths only; no pan-Asian total exists.
- 传播途径（计分板）：Mosquito & tick；标签：Flavivirus / Vaccine since 1954；徽章：CHINA ONLY

### #19 Kaposi sarcoma virus — 65K est.（2020–2024，estimated (cumulative.py)）
- 主值：64,532；来源：Fu et al., Lancet Glob Health 2023 (15.1K, 2020); GLOBOCAN 2024 (10.7K)（peer-reviewed）<https://doi.org/10.1016/s2214-109x(23)00349-2>
- 推算锚点（Kaposi 肉瘤死亡：Fu 2023 / GLOBOCAN 2024）：2020: 15,086，2024: 10,727；窗口 2020–2024
- 备注：KSHV/HHV-8 causes all Kaposi sarcoma; most of these deaths also involve HIV.
- 传播途径（计分板）：Contact；标签：Herpesvirus / No vaccine；徽章：CANCER DEATHS

### #20 Hantavirus — 46,427 （1950–2007，counted (documented total)）
- 主值：46,427；来源：Zhang et al., Emerging Infectious Diseases 2010;16(8): HFRS in China 1950–2007（peer-reviewed）<https://wwwnc.cdc.gov/eid/article/16/8/09-0470_article>
- 备注：Haemorrhagic fever with renal syndrome, China only. Korea, Russia and the Americas not totalled.
- 传播途径（计分板）：Animals；标签：Hantavirus / Vaccine since 1990；徽章：CHINA ONLY

### #21 Hepatitis E — 16K est.（2021–2024，estimated (cumulative.py)）
- 主值：16,252；来源：GBD 2021 (3,450) and WHO 2023 (4,431)（primary）<https://www.who.int/news-room/fact-sheets/detail/hepatitis-e>
- 推算锚点（GBD 2021 / WHO 2023）：2021: 3,450，2023: 4,431；窗口 2021–2024
- 交叉核对：Older WHO estimate: 44,000 a year (2015) = 44,000（与主值差 170.7%）<https://www.who.int/news-room/fact-sheets/detail/hepatitis-e>
- 备注：Older estimates (70K in 2005, 44K in 2015) used a different method; only the current series is summed.
- 传播途径（计分板）：Food & water；标签：Hepevirus / Vaccine since 2011

### #22 Ebola — 15,514 （1976–2025，counted (documented total)）
- 主值：15,514；来源：UKHSA outbreak table (4,142 deaths outside West Africa to Jan 2023) + West Africa 2014–16 (11,323, WHO) + Uganda 2025 (4) + DRC Kasai 2025 (45)（primary）<https://www.gov.uk/government/publications/ebola-origins-reservoirs-transmission-and-guidelines/ebola-overview-history-origins-and-transmission>
- 交叉核对：WHO AFRO: DRC 16th outbreak over, 45 deaths (Dec 2025) = 45（与主值差 -99.7%）<https://afro.who.int/countries/democratic-republic-congo/news/democratic-republic-congo-declares-end-16th-ebola-outbreak>
- 备注：Sum of outbreak totals (all Ebola species).
- 传播途径（计分板）：Contact；标签：Filovirus / Vaccine since 2019

### #23 Hand-foot-mouth viruses — 3,632 （2008–2017，counted (documented total)）
- 主值：3,632；来源：Chinese HFMD surveillance analysis 2008–2017, Journal of Disease Surveillance: all HFMD deaths（peer-reviewed）<https://www.jbjc.org/en/article/doi/10.3784/jbjc.202107090395>
- 交叉核对：Xing et al., Lancet ID 2014: 2,457 HFMD deaths 2008–2012 = 2,457（与主值差 -32.4%）<https://pmc.ncbi.nlm.nih.gov/articles/PMC4035015/>
- 备注：All hand, foot and mouth disease deaths in mainland China (several enteroviruses; EV-A71 is the main cause of fatal cases), so the card is named for the virus group. Vaccine year = EV-A71 vaccines (China).
- 传播途径（计分板）：Contact；标签：Enteroviruses (EV-A71) / Vaccine since 2015；徽章：CHINA ONLY

### #24 West Nile virus — 2,330 （1999–2018，counted (documented total)）
- 主值：2,330；来源：CDC ArboNET yearly death counts 1999–2018 summed (2,330), as tabulated in Wikipedia's list of West Nile outbreaks（aggregator）<https://en.wikipedia.org/wiki/List_of_West_Nile_virus_outbreaks>
- 交叉核对：CIDNI 2026 lecture citing CDC: about 3,000 US deaths 1999–2024 = 3,000（与主值差 28.8%）<https://cidni.org/wp-content/uploads/2026/08/West_Nile_Virus_Nursing_Talk_1.pdf>
- 备注：United States only, through 2018 (last CDC-based cumulative total found); later US deaths and Europe are not included.
- 传播途径（计分板）：Mosquito & tick；标签：Flavivirus / No vaccine；徽章：US ONLY

### #25 Tick-borne encephalitis — 1,136 （2000–2022，counted (documented total)）
- 主值：1,136；来源：Dzagurova et al., Epidemiology and Vaccinal Prevention 2024;23(5) (Russia, TBE 2000–2022)（peer-reviewed）<https://www.epidemvac.ru/jour/article/download/2087/1073>
- 备注：Russia only.
- 传播途径（计分板）：Mosquito & tick；标签：Flavivirus / Vaccine since 1976；徽章：RUSSIA ONLY

### #26 MERS — 960 （2012–2026，counted (documented total)）
- 主值：960；来源：ECDC MERS-CoV worldwide overview, 2 July 2026: 2,649 cases, 960 deaths（primary）<https://www.ecdc.europa.eu/en/middle-east-respiratory-syndrome-coronavirus/threats-and-outbreaks>
- 交叉核对：WHO DON May 2020: 876 deaths to Mar 2020 = 876（与主值差 -8.8%）<https://www.who.int/emergencies/disease-outbreak-news>
- 备注：Camels are the source; most cases in Saudi Arabia.
- 传播途径（计分板）：Animals；标签：Coronavirus / No vaccine

### #27 SARS (SARS-CoV-1) — 774 （2002–2003，counted (documented total)）
- 主值：774；来源：WHO summary of probable SARS cases, Nov 2002–Jul 2003: 8,096 cases, 774 deaths（primary）<https://www.who.int/publications/m/item/summary-of-probable-sars-cases-with-onset-of-illness-from-1-november-2002-to-31-july-2003>
- 备注：No human cases since 2004.
- 传播途径（计分板）：Airborne；标签：Coronavirus / No vaccine

### #28 Marburg virus — 561 （1967–2025，counted (documented total)）
- 主值：561；来源：WHO tally 1967–2021 (479) + Ghana 2022 (2) + Eq. Guinea 2023 (35 incl. probable) + Tanzania 2023 (6) + Rwanda 2024 (15) + Tanzania 2025 (10) + Ethiopia 2025 (9 confirmed + 5 probable)（primary）<https://www.cdc.gov/marburg/outbreaks/index.html>
- 备注：Sum of outbreak totals; probable deaths counted where WHO reported them.
- 传播途径（计分板）：Contact；标签：Filovirus / No vaccine

### #29 Crimean-Congo fever — 469 （2002–2017，counted (documented total)）
- 主值：469；来源：Peer-reviewed table: Turkey 2002–2017, 10,333 cases, 469 deaths (PMC6335890)（peer-reviewed）<https://pmc.ncbi.nlm.nih.gov/articles/PMC6335890/>
- 交叉核对：Leblebicioglu et al. 2016: >9,700 patients, mortality <5% = 480（与主值差 2.3%）<https://acikerisim.omu.edu.tr/entities/publication/d1057151-ffb8-4835-9dda-58127a9e4b4d/full>
- 备注：Turkey only (largest documented series). Tick-borne.
- 传播途径（计分板）：Mosquito & tick；标签：Nairovirus / No vaccine；徽章：TURKEY ONLY

### #30 Nipah virus — 435 （1998–2024，counted (documented total)）
- 主值：435；来源：2024 geospatial study: 754 cases, 435 deaths in 5 countries through May 2024（peer-reviewed）<https://pmc.ncbi.nlm.nih.gov/articles/PMC11414670/>
- 备注：A handful more deaths since (Kerala 2024–25, Bangladesh 2025–26).
- 传播途径（计分板）：Animals；标签：Paramyxovirus / No vaccine

## §3 洞察卡依据

- after #30：How to read: est. = modelled estimate, no tag = counted deaths. Years differ per card.
- after #27：Rare viruses are barely tracked: several counts here cover only one country.
- after #22：Ebola, SARS, MERS and Marburg together killed fewer than 18,000 people.
- after #16：Rabies is almost always fatal once symptoms start, yet a vaccine has existed since 1885.
- after #8：COVID-19's reported toll is 7.1M. Excess-death studies put it at 15–28M.
- after #4：Measles and HIV are neck and neck, and measles is only counted from 1980.
- after #2：Smallpox is the only human disease ever eradicated. Its last natural case was in 1977.
  - 依据：#27 之后——第 18、20、23、24、25、29 名为单国计数；#22 之后——15,514 + 774 + 960 + 561 = 17,809；狂犬病——WHO 狂犬病情况说明书（发病后几乎 100% 致死），巴斯德 1885 年 7 月 6 日首次给 Joseph Meister 接种；新冠——WHO 报告 7,117,689，WHO 超额 14.83M（2020–21，Nature 2023），The Economist 27.1–28.5M；麻疹 vs HIV——43M（1980–2024 est.）vs 44.2M；天花——WHO：1980 年宣布根除，最后一例自然病例 1977 年索马里。

## §4 不进榜的病毒与原因

- 脊髓灰质炎：只有麻痹病例数（1988 年约 35 万例），没有全球死亡估计。
- 风疹、腮腺炎、巨细胞病毒、单纯疱疹、HTLV-1：只有病例或局部死亡数。
- 人偏肺病毒（2018 年 1.61 万）、副流感（3.44 万）、腺病毒（3.69 万）：只有单一年份、5 岁以下儿童估计，不满足 ≥2 个锚点。
- 丁肝：GBD 不单列，死亡含在乙肝里。
- 拉沙热：CDC/ECDC「每年约 5,000」为粗估；尼日利亚 2025 年确诊死亡 215（NCDC 第 52 周）。没有累计数。
- 寨卡、基孔肯雅：全球死亡数零散（基孔肯雅 2025 年 WHO 报告 155–186）。
