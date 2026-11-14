# ep02 · 数据出处、交叉核对与许可（sources.md）

> 2026-11-03 代理整理（用户授权自主决策）。本文件由 `_build/gen_sources.py` 从 `data.json` / `assets.json` 生成；改数据请改 `_build/items_def.py` 后重跑 `build.py` → `gen_sources.py`。

## 1. 口径

- **榜单**：每个主权国家的最高点，按海拔（米）降序，取前 50。
- **国家名单**：Wikidata「主权国家」(Q3624078) 且有 P297 ISO 代码、P610 最高点；查询见 `0_research/data/wikidata_country_highest_points.rq`，原始结果 `wikidata_country_highest_points_2026-11-03.json`。名单含台湾（卡上写 "Taiwan"）。格陵兰（3,694 m）、南极洲非主权国家，不入榜。
- **国名**：通用英文短名（China、DR Congo、United States、Turkey…）。
- **海拔取值规则**：
  1. 原查询对每座山取所有 P2044 声明的 **MAX**，会选中过时或错误的值（珠峰 8,850、勃朗峰 2013 年的 4,810.02、达马万德 5,628、塔胡穆尔科 4,220）。本期改为取 Wikidata **preferred rank** 的值；没有 preferred 时取 normal 值并与第二来源核对。
  2. 每一条都与第二来源核对：Wikipedia「List of elevation extremes by country」（revid 1381548721，2026-10-23）；差异处再查该山 Wikipedia 条目的 infobox 及其引用（USGS、大学测量、Peaklist 等）。
  3. 取「支持最好」的值作 `value`，另一来源写进 `cross_check`。差异 > 0.5% 或影响排序的，写进 `notes`。
  4. Peakbagger 对脚本请求返回 403，网页抓取工具也被拦，**本期没有直接核到 Peakbagger**；凡 Wikipedia 引用 Peakbagger / Peaklist 的值，记为「经 Wikipedia 转引」。
- **显示**：`value_display` 四舍五入到整米；`secondary_display` = 米 × 3.28084 四舍五入到整英尺。
- **同值同名次（标准竞赛排名 1,1,3）**：共享山峰两国同名次，下一名跳号，所以第 50 名就是第 50 个国家；同名次内按国名字母序，顺序稳定（China→Nepal、DR Congo→Uganda、France→Italy）。

## 2. 归属与大洲判断（待用户复核）

| 议题 | 本期做法 | 依据 |
|---|---|---|
| 归属总原则 | 按实际管辖（de-facto administration） | topics.md §3 |
| 台湾 | 保留，标 "Taiwan"（玉山 3,952 m，第 44） | Wikidata 主权国家名单含台湾；用户既定 |
| 印度 / K2 | 印度取干城章嘉峰 8,586 m；K2 归巴基斯坦。印度官方地图把 K2 所在地区划入拉达克，主张 K2 为本国最高点 | 实际管辖；洞察卡 4 说明 |
| 共享山峰 | 同一山顶同时是两国最高点的，各国一张卡，`badge` 写 SHARED WITH …：珠峰（中国/尼泊尔）、斯坦利山（刚果（金）/乌干达）、勃朗峰（法国/意大利） | topics.md §3 |
| 勃朗峰主权 | 法意两国对峰顶一带边界有争议（Wikipedia："Ownership of the summit area has long been disputed"）；两国都计入，`notes` 说明；洞察卡 2 提及 | Wikipedia 'Mont Blanc' |
| 其他边境峰 | K2、干城章嘉、诺沙克、托木尔、汗腾格里、奥霍斯-德尔萨拉多、什哈拉、巴扎尔杜久、卡里辛比、友谊峰、哈兹拉特苏丹等位于国界上，但另一国的最高点不是它，所以不加 SHARED 徽章，只在 `notes` 写明 | 徽章只表示「同为两国最高点」 |
| 不丹 | 冈仁布钦（Gangkhar Puensum）位于不丹—中国边界附近，边界走向有争议；按实际管辖计入不丹 | Wikipedia |
| 大洲（计分板） | 按**山顶所在位置**，不按国家习惯分组 | 用户既定 |
| 厄尔布鲁士 | Europe（在大高加索分水岭以北） | 用户既定 |
| 什哈拉（格鲁吉亚） | Europe（位于大高加索主分水岭上，分水岭作欧亚界时界上山峰计入欧洲） | 用户既定 |
| 巴扎尔杜久（阿塞拜疆） | Europe，与什哈拉同规则（同在主分水岭上）；注意阿塞拜疆通常被归入亚洲 | 代理判断，保持规则一致 |
| 阿拉拉特（土耳其）、阿拉加茨（亚美尼亚） | Asia（亚美尼亚高原，在高加索分水岭以南） | 用户既定 / 同规则 |
| 查亚峰（印尼） | Oceania（新几内亚岛位于澳大利亚大陆架上；七大洲最高峰惯例亦把它算大洋洲） | 代理判断 |
| 泰德峰（西班牙） | Europe（加那利群岛是大洋火山岛，不在任何大陆架上，按所属国计） | 代理判断：大陆架岛归该大陆，大洋岛随国家 |
| 计分结果 | Asia 19、Europe 8、Africa 8、South America 7、North America 5、Oceania 3 | data.json |

## 3. 前 50 名边界核对

- 第 49 西班牙 Teide 3,715 m（两源一致）；第 50 也门 Jabal an-Nabi Shu'ayb 3,666 m（两源一致；旧资料有 3,760 m，取哪一个都在榜内）。
- 第 51 伊拉克 Cheekha Dar 3,611 m（Wikidata 与 Wikipedia 一致，Wikipedia 转引 Peakbagger），比第 50 低 55 m；第 52 莱索托 3,482 m。
- 修正后唯一的名次移动：喀麦隆 4,095 → 4,040 m，从并列第 41 降到第 43；格鲁吉亚若取 5,203 m 会和肯尼亚（5,199 m）互换。**入榜的 50 国不因任何修正而改变。**
- 原查询结果第 19/20 行哥伦比亚出现两次（Simón Bolívar 与 Cristóbal Colón 同为 5,775 m），只取 Cristóbal Colón 一条。

## 4. 逐条出处与交叉核对

差异 = |value − cross| / value。所有条目 retrieved_at = 2026-11-03。

| # | 国家 | 山峰 | value (m) | 主值来源 | 交叉核对 | 差异 % | 备注 |
|---|---|---|---|---|---|---|---|
| 1 | China | Mount Everest | 8848.86 | [China–Nepal joint survey 2020 (Wikidata Q513 preferred P2044)](https://www.wikidata.org/wiki/Q513) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 8849 | 0.0 | Summit on the China (Tibet)–Nepal border; both countries count it as their highest point. Value = 8,848.86 m announced jointly by China and Nepal in Dec 2020 (Wikidata preferred rank). The original country query took MAX over all P2044 statements and returned 8,850 m (an older 1999 GPS figure, normal rank). Image: north face, seen from the Tibet side. |
| 1 | Nepal | Mount Everest | 8848.86 | [China–Nepal joint survey 2020 (Wikidata Q513 preferred P2044)](https://www.wikidata.org/wiki/Q513) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 8849 | 0.0 | Same summit as China's card (tie, same rank). Image: seen from Gokyo Ri on the Nepal side. |
| 3 | Pakistan | K2 | 8611 | [Wikidata Q43512 (P2044, CC0)](https://www.wikidata.org/wiki/Q43512) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 8611 | 0.0 | Summit on the Pakistan-administered Gilgit-Baltistan / China border. India officially claims the area (as part of Ladakh); listed under Pakistan by de-facto administration. |
| 4 | India | Kangchenjunga | 8586 | [Wikidata Q82019 (P2044, CC0)](https://www.wikidata.org/wiki/Q82019) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 8586 | 0.0 | India officially claims K2 (8,611 m) as its highest point; by de-facto administration India's highest point is Kangchenjunga on the Sikkim–Nepal border. Nepal's own highest point is Everest, so no SHARED badge. |
| 5 | Bhutan | Gangkhar Puensum | 7570 | [Wikidata Q219986 (P2044, CC0)](https://www.wikidata.org/wiki/Q219986) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 7571 | 0.01 | Lies on or near the Bhutan–China (Tibet) border, whose alignment here is disputed. Climbing banned in Bhutan since 2003; Wikipedia describes it as unclimbed. |
| 6 | Tajikistan | Ismoil Somoni Peak | 7495 | [Wikidata Q41413 (P2044, CC0)](https://www.wikidata.org/wiki/Q41413) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 7495 | 0.0 | Formerly Communism Peak. First ascent year from the Wikipedia infobox (Abalakov, 1933). Image is black-and-white (1985 expedition photo). |
| 7 | Afghanistan | Noshaq | 7492 | [Wikidata Q271700 (P2044, CC0)](https://www.wikidata.org/wiki/Q271700) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 7492 | 0.0 | Summit on the Afghanistan–Pakistan border (Pakistan's high point is K2). |
| 8 | Kyrgyzstan | Jengish Chokusu | 7439 | [Wikidata Q332762 (P2044, CC0)](https://www.wikidata.org/wiki/Q332762) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 7439 | 0.0 | Also called Victory Peak / Pik Pobedy; on the Kyrgyzstan–China border. |
| 9 | Kazakhstan | Khan Tengri | 7010 | [Wikidata Q211529 (P2044, CC0)](https://www.wikidata.org/wiki/Q211529) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 7010 | 0.0 | Near the China–Kazakhstan–Kyrgyzstan tripoint. 7,010 m includes the summit ice cap; the rock summit is often given as about 6,995 m. |
| 10 | Argentina | Aconcagua | 6960.8 | [Universidad Nacional de Cuyo survey 2012 (6,960.8 m), cited in Wikipedia 'Aconcagua'](http://www.unidiversidad.com.ar/informe-cientifico-que-estudia-el-aconcagua-el-coloso-de-america-mide-69608-metros) | [Wikidata Q39739 (P2044, CC0)](https://www.wikidata.org/wiki/Q39739): 6962 | 0.02 | Wikipedia list gives 6,961 m (= the 2012 survey rounded); Wikidata 6,962 m. The Wikipedia article infobox currently shows 6,967.16 m while citing the 6,960.8 m report (internal inconsistency, not used). |
| 11 | Chile | Ojos del Salado | 6893 | [Wikidata Q233836 (P2044, CC0)](https://www.wikidata.org/wiki/Q233836) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 6893 | 0.0 | Summit on the Chile–Argentina border (Argentina's high point is Aconcagua). 'Earth's highest volcano' per Wikipedia short description. |
| 12 | Peru | Huascarán | 6768 | [Wikidata Q200935 (P2044, CC0)](https://www.wikidata.org/wiki/Q200935) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 6768 | 0.0 | Huascarán Sur (main summit), first climbed 20 July 1932 (Wikipedia infobox). |
| 13 | Bolivia | Nevado Sajama | 6542 | [Wikidata Q272593 (P2044, CC0)](https://www.wikidata.org/wiki/Q272593) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 6542 | 0.0 |  |
| 14 | Ecuador | Chimborazo | 6263.47 | [Wikidata Q14081 (P2044, CC0)](https://www.wikidata.org/wiki/Q14081) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 6263 | 0.01 | Wikidata and the Wikipedia article agree on 6,263.47 m. Its summit is the point on Earth's surface farthest from Earth's centre (Wikipedia). |
| 15 | United States | Denali | 6190.49 | [USGS 2015 survey: 20,310 ft (Newell & Horner, 2 Sep 2015)](https://www.usgs.gov/news/new-elevation-nation%E2%80%99s-highest-peak) | [Wikidata Q130018 (P2044, CC0)](https://www.wikidata.org/wiki/Q130018): 6190 | 0.01 | Value = 20,310 ft converted to metres (6,190.49 m). Wikipedia list 6,190 m. |
| 16 | Canada | Mount Logan | 5959 | [Wikidata Q120306 (P2044, CC0)](https://www.wikidata.org/wiki/Q120306) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 5959 | 0.0 | Image source is only 975 px wide (public domain); best licensed whole-mountain view found. |
| 17 | Tanzania | Kilimanjaro | 5895 | [Wikidata Q7296 (P2044, CC0)](https://www.wikidata.org/wiki/Q7296) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 5895 | 0.0 | Uhuru Peak on Kibo. 5,895 m is the 1952 British survey value still used officially; later GNSS work measured 5,892 m (1999), 5,902 m (2008), 5,899 m (2014) per Wikipedia - all within 0.12%. The original country query linked Mount Kibo (Q1394606); Q7296 used for metadata. |
| 18 | Myanmar | Hkakabo Razi | 5881 | [Wikidata Q870063 (P2044, CC0)](https://www.wikidata.org/wiki/Q870063) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 5881 | 0.0 | Height poorly surveyed: a 2013 expedition to nearby Gamlang Razi (19,258 ft / 5,870 m, Myanmar Times via Wikipedia) challenged its status. Wikipedia article gives 19,295 ft (5,881 m). Image cropped to remove the uploader's elevation captions. |
| 19 | Colombia | Pico Cristóbal Colón | 5775 | [Wikidata Q578862 (P2044, CC0)](https://www.wikidata.org/wiki/Q578862) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 5775 | 0.0 | Twin of Pico Simón Bolívar (also 5,775 m in Wikidata). SRTM data and a 2015 handheld GPS reading (cited in Wikipedia 'Pico Simón Bolívar') suggest the twins are nearer 5,700–5,730 m (up to ~1.3% lower); not an official survey, so the conventional 5,775 m is kept. Rank unaffected (Russia 5,642 m is next). |
| 20 | Russia | Mount Elbrus | 5642 | [Wikidata Q43105 (P2044, CC0)](https://www.wikidata.org/wiki/Q43105) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 5642 | 0.0 | Continent: Europe (summit north of the Greater Caucasus watershed). First ascent year = West (main) summit, 1874; the lower East summit was climbed in 1829. |
| 21 | Mexico | Pico de Orizaba | 5636 | [Wikidata Q238147 (P2044, CC0)](https://www.wikidata.org/wiki/Q238147) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 5636 | 0.0 | Also Citlaltépetl. INEGI mapping gives 5,611 m (-0.44%); 5,636 m is the commonly cited value. Rank unaffected either way (Iran 5,610 m below). |
| 22 | Iran | Mount Damavand | 5610 | [Wikidata Q40758 (P2044, CC0)](https://www.wikidata.org/wiki/Q40758) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 5609 | 0.02 | Wikidata holds two statements (5,610 and 5,628 m); the original MAX query returned 5,628. 5,610 m matches the Wikipedia article and Iranian sources; Wikipedia list 5,609 m. With 5,628 m Iran would still rank below Mexico. |
| 23 | Kenya | Mount Kenya | 5199 | [Wikidata Q172070 (P2044, CC0)](https://www.wikidata.org/wiki/Q172070) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 5199 | 0.0 | Batian, the main summit. |
| 24 | Georgia | Shkhara | 5193.2 | [Wikidata Q217457 (P2044, CC0)](https://www.wikidata.org/wiki/Q217457) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 5203 | 0.19 | ⚠ ORDER-SENSITIVE: published heights range 5,193–5,203 m (Soviet map 5,157.8 m). 5,193.2 m = 2010 DGPS survey (Schoen & Avdeev), also CIA World Factbook 5,193 m; Wikipedia now uses 5,203 m (Georgian geography texts 2019/2022). With 5,203 m Georgia would rank above Kenya (5,199 m). Summit on the Georgia–Russia border on the main Caucasus watershed; continent set to Europe (see sources.md). |
| 25 | Turkey | Mount Ararat | 5137 | [Wikidata Q72303 (P2044, CC0)](https://www.wikidata.org/wiki/Q72303) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 5137 | 0.0 | Continent: Asia (eastern Anatolia). First ascent 1829 (Parrot and Abovian) per Wikipedia infobox. |
| 26 | DR Congo | Mount Stanley | 5109 | [Wikidata Q221666 (P2044, CC0)](https://www.wikidata.org/wiki/Q221666) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 5109 | 0.0 | Margherita Peak lies on the DR Congo–Uganda border; it is the highest point of both. |
| 26 | Uganda | Mount Stanley | 5109 | [Wikidata Q221666 (P2044, CC0)](https://www.wikidata.org/wiki/Q221666) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 5109 | 0.0 | Same summit as DR Congo's card (tie, same rank). |
| 28 | Venezuela | Pico Bolívar | 4978 | [Wikidata Q213704 (P2044, CC0)](https://www.wikidata.org/wiki/Q213704) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 4978 | 0.0 |  |
| 29 | Indonesia | Puncak Jaya | 4884 | [Wikidata Q1045888 (P2044, CC0)](https://www.wikidata.org/wiki/Q1045888) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 4884 | 0.0 | Carstensz Pyramid. Continent: Oceania - the summit is on New Guinea, on the Australian continental shelf (Sahul), although Indonesia is usually grouped with Asia. Elevation from the 1971–73 Australian Universities' Expedition. Image source only 640 px wide (best licensed photo found). |
| 30 | France | Mont Blanc | 4807.47 | [Haute-Savoie surveyors, survey of 17 Sept 2026 (published 14 Oct 2026)](https://www.euronews.com/2026/10/14/mont-blanc-new-french-measurements-summit-grows-to-4807m) | [Wikidata Q583 (P2044, CC0)](https://www.wikidata.org/wiki/Q583): 4805.59 | 0.04 | The summit ice cap changes height: 4,810.02 m (2013), 4,807.81 m (2021), 4,805.59 m (2023), and 4,807.47 m in the survey of 17 Sept 2026 (published 14 Oct 2026, Euronews) — used here; Wikidata still holds the 2023 value (cross_check). Updated after independent QC on 2026-11-03. The original MAX query returned the 2013 value. SOVEREIGNTY: 'Ownership of the summit area has long been disputed between France and Italy' (Wikipedia); the border line near the summit and Dôme du Goûter is contested. Counted as the high point of both countries. Image: French (Chamonix) side. |
| 30 | Italy | Mont Blanc | 4807.47 | [Haute-Savoie surveyors, survey of 17 Sept 2026 (published 14 Oct 2026)](https://www.euronews.com/2026/10/14/mont-blanc-new-french-measurements-summit-grows-to-4807m) | [Wikidata Q583 (P2044, CC0)](https://www.wikidata.org/wiki/Q583): 4805.59 | 0.04 | Monte Bianco. Same summit as France's card (tie, same rank); summit sovereignty disputed (see France). Image: Italian side (caption 'Monte Bianco, Italy'). |
| 32 | Uzbekistan | Khazret Sultan | 4643 | [Wikidata Q519822 (P2044, CC0)](https://www.wikidata.org/wiki/Q519822) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 4643 | 0.0 | On the Uzbekistan–Tajikistan border. NO IMAGE: no P18, no Commons category, and Commons searches (EN/RU/UZ/TJ spellings) found no identifiable licensed photo of the peak. Renderer needs a placeholder (e.g. flag/silhouette). |
| 33 | Switzerland | Dufourspitze | 4634 | [Wikidata Q3403 (P2044, CC0)](https://www.wikidata.org/wiki/Q3403) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 4634 | 0.0 | Highest summit of Monte Rosa, just inside Switzerland near the Italian border. |
| 34 | Ethiopia | Ras Dashen | 4550 | [Franco-Italian survey, via Peaklist.org (Wikipedia list and 'Ras Dashen' article)](https://en.wikipedia.org/wiki/Ras_Dashen) | [Wikidata Q275435 (P2044, CC0)](https://www.wikidata.org/wiki/Q275435): 4533 | 0.37 | Published heights diverge: 4,620 m (Italian military survey, still often quoted), 4,533 m (1970s triangulation; Wikidata), 4,550 m (later Franco-Italian survey; Wikipedia via Peaklist). Rank unaffected (between 4,634 and 4,509 m). First-ascent year 1841 from Wikidata. Image: approach to the flat-topped summit massif (no dramatic licensed photo found). |
| 35 | Papua New Guinea | Mount Wilhelm | 4509 | [Wikidata Q277441 (P2044, CC0)](https://www.wikidata.org/wiki/Q277441) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 4509 | 0.0 |  |
| 36 | Rwanda | Mount Karisimbi | 4507 | [Wikidata Q737859 (P2044, CC0)](https://www.wikidata.org/wiki/Q737859) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 4507 | 0.0 | Summit on the Rwanda–DR Congo border (DR Congo's high point is Mount Stanley). |
| 37 | Azerbaijan | Mount Bazardüzü | 4466 | [Wikidata Q725591 (P2044, CC0)](https://www.wikidata.org/wiki/Q725591) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 4466 | 0.0 | Summit on the Azerbaijan–Russia border on the main Caucasus watershed; continent set to Europe for consistency with Shkhara (Azerbaijan is usually grouped with Asia; see sources.md). Wikidata also carries an erroneous 2,706 m statement (ignored). First-ascent year conflicts (Wikidata 1847, Wikipedia 1849) - no tag. |
| 38 | Mongolia | Khüiten Peak | 4374 | [Wikidata Q1091113 (P2044, CC0)](https://www.wikidata.org/wiki/Q1091113) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 4356 | 0.41 | 4,374 m is the Mongolian official figure (Wikidata; also CIA World Factbook); Wikipedia uses Peakbagger's 4,356 m (-0.41%). Rank unaffected (between 4,466 and 4,203 m). On the Mongolia–China border. Image: Tavan Bogd massif seen from the Ukok Plateau (the photo Wikipedia uses for this peak). |
| 39 | Guatemala | Volcán Tajumulco | 4203 | [Wikidata Q818467 (P2044 preferred, CC0)](https://www.wikidata.org/wiki/Q818467) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 4203 | 0.0 | Wikidata also has a non-preferred 4,220 m statement, which the original MAX query returned (+0.40%). |
| 40 | Morocco | Toubkal | 4167 | [Wikidata Q503433 (P2044, CC0)](https://www.wikidata.org/wiki/Q503433) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 4167 | 0.0 | Jbel Toubkal. |
| 41 | Malaysia | Mount Kinabalu | 4095 | [Wikidata Q60967 (P2044, CC0)](https://www.wikidata.org/wiki/Q60967) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 4095.2 | 0.0 | First-ascent year conflicts (Wikidata 1888 vs Wikipedia 1851 summit plateau) - no tag. |
| 42 | Armenia | Mount Aragats | 4090 | [Wikidata Q203568 (P2044, CC0)](https://www.wikidata.org/wiki/Q203568) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 4090 | 0.0 | Continent: Asia (Armenian Highlands, south of the Caucasus watershed). |
| 43 | Cameroon | Mount Cameroon | 4040 | [Wikipedia 'Mount Cameroon' (4,040 m, consistent with SRTM)](https://en.wikipedia.org/wiki/Mount_Cameroon) | [Wikidata Q190562 (P2044, CC0)](https://www.wikidata.org/wiki/Q190562): 4095 | 1.36 | ⚠ DISCREPANCY 1.36%: Wikidata (and the original query) give the frequently quoted 4,095 m, but Wikipedia notes it is incompatible with SRTM data (no cells above ~4,027 m) and uses 4,040 m; Wikipedia list also 4,040 m. Using 4,040 m moves Cameroon from #41 (tied with Malaysia) to #43, below Armenia (4,090 m). Top-50 membership unaffected. |
| 44 | Taiwan | Yushan | 3952 | [Wikidata Q500275 (P2044, CC0)](https://www.wikidata.org/wiki/Q500275) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 3952 | 0.0 | Jade Mountain main peak (Wikipedia article 3,952.43 m). Taiwan is in the Wikidata sovereign-state list used for this series; labelled 'Taiwan'. First-ascent year conflicts (1896/1898/1900) - no tag. |
| 45 | Costa Rica | Cerro Chirripó | 3820 | [Wikidata Q252362 (P2044, CC0)](https://www.wikidata.org/wiki/Q252362) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 3821 | 0.03 | 3,820 m also on the official summit sign. |
| 46 | Austria | Grossglockner | 3798 | [Wikidata Q3388 (P2044, CC0)](https://www.wikidata.org/wiki/Q3388) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 3798 | 0.0 |  |
| 47 | Japan | Mount Fuji | 3776.24 | [Wikipedia 'Mount Fuji' (3,776.24 m, GSI figure)](https://en.wikipedia.org/wiki/Mount_Fuji) | [Wikidata Q39231 (P2044, CC0)](https://www.wikidata.org/wiki/Q39231): 3777.24 | 0.03 | Wikidata's 3,777.24 m looks like a 1 m typo of the GSI value 3,776.24 m; Wikipedia list 3,776 m. |
| 48 | New Zealand | Aoraki / Mount Cook | 3724 | [Wikidata Q5059 (P2044, CC0)](https://www.wikidata.org/wiki/Q5059) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 3724 | 0.0 | Wikidata and Wikipedia agree (3,724 m). |
| 49 | Spain | Teide | 3715 | [Wikidata Q38954 (P2044, CC0)](https://www.wikidata.org/wiki/Q38954) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 3715 | 0.0 | Continent: Europe. Teide is on an oceanic volcanic island off Africa, not on a continental shelf, so it is counted with its country (see sources.md). Mainland Spain's high point is Mulhacén (Wikipedia list footnote). |
| 50 | Yemen | Jabal an-Nabi Shu'ayb | 3666 | [Wikidata Q1261935 (P2044, CC0)](https://www.wikidata.org/wiki/Q1261935) | [Wikipedia: List of elevation extremes by country](https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country): 3666 | 0.0 | BOUNDARY: #50. Next is Iraq (Cheekha Dar, 3,611 m, #51), 55 m lower, so the boundary does not depend on any disputed value. Older sources quote 3,760 m for this peak; either value keeps it inside the top 50. Greenland (3,694 m) is not sovereign and is excluded. Image: distant view of the summit ridge from the Haraz (the photo Wikipedia uses). |

**Tag 出处**：`First ascent YYYY` 取自 Wikidata P793（first ascent）+ P585；Wikidata 没有的从该山 Wikipedia infobox 补（Ismoil Somoni、Aconcagua、Ojos del Salado、Huascarán、Hkakabo Razi、Pico de Orizaba、Mont Blanc、Mount Wilhelm、Toubkal、Mount Aragats、Cerro Chirripó、Mount Ararat）。两源年份冲突的不加（Bazardüzü、Kinabalu、Yushan、Damavand、Mount Cameroon）。火山类 tag 取 Wikidata P31 或 Wikipedia 短描述；"Highest in …" 取 Wikipedia 短描述 / 列表脚注。

## 5. 洞察卡核对

| after_rank | 文案 | 数据支持 |
|---|---|---|
| 41 | Mount Cameroon is often listed at 4,095 m, but satellite data puts it nearer 4,040 m. | Mount Cameroon：Wikidata 4,095 m vs Wikipedia（SRTM 无高于约 4,027 m 的格点）4,040 m；本期取 4,040 |
| 32 | Next: Mont Blanc. France and Italy still disagree over who owns its summit. | Mont Blanc notes：Wikipedia「Ownership of the summit area has long been disputed between France and Italy」 |
| 21 | Next: Elbrus, Europe's highest peak, 835 m taller than Mont Blanc. | Elbrus 5,642 − Mont Blanc 4,807.47（2026-09 测量）= 834.53 m，显示取整 835 m；Wikipedia「Highest mountain of Russia and Europe」 |
| 11 | From here on, every peak tops 6,950 m, and 9 of the last 10 are in Asia. | 第 1–10 名最低为 Aconcagua 6,960.8 m > 6,950；10 张卡中 9 张 continent = Asia（仅阿根廷例外） |
| 4 | India also claims K2. We list each peak under the country that controls it. | K2 notes：印度主张该地区；按实际管辖归巴基斯坦（Wikipedia 列表 K2 脚注） |

## 6. 许可

- **Wikidata**：CC0，数值可直接使用。
- **Wikipedia**：只用作事实来源（数值、年份、归属说明），不搬运文字；事实本身不受版权保护。屏上与描述框不复制 Wikipedia 文本。
- **USGS**：美国联邦政府作品，公有领域。Universidad Nacional de Cuyo、Peaklist 等只引用测量数值（事实）。
- **图片**：全部来自 Wikimedia Commons，逐张核对 extmetadata 的 LicenseShortName，只收 Public domain / CC0 / CC BY / CC BY-SA（含移植版本如 CC BY-SA 2.0 fr、2.5 nl、2.1 au、3.0 de）。拒绝：`Dejen misura da cima W.jpg`（许可仅为 "Attribution" 自由文本，非标准 CC，保守弃用）。所有改动只有缩放、重新编码 JPEG，Hkakabo Razi 一张为去掉上传者叠加的海拔字样做了裁切（CC0）。CC BY-SA 图只缩放裁切，不做其他改编。自然景观，无全景自由（FoP）问题。
- **缺图**：第 32 名乌兹别克斯坦 Khazret Sultan——无 P18、无 Commons 分类，英/俄/乌兹别克/塔吉克拼写搜索都找不到可确认是该峰且许可合格的照片，`image` = null，渲染器需用占位（国旗或剪影）。
- **低分辨率提示**：Puncak Jaya 原图仅 640×480、Mount Logan 975×639、Jabal an-Nabi Shu'ayb 1024×768、Pico de Orizaba 1024×768、Karisimbi 1134×504、Hkakabo Razi 裁后 1037×775；卡片主图区小，预计够用，渲染后抽检。
- **内容提示**：Ismoil Somoni Peak 为黑白老照片（1985）；Ras Dashen 是走向平顶山体的步道视角；Khüiten Peak 是从 Ukok 高原远眺 Tavan Bogd 山群；也门一张为从 Haraz 远眺山脊（均为 Wikipedia 条目所用图或最佳可得）。

## 7. 图片署名（可直接贴进 YouTube 描述）

```text
Mountain photos via Wikimedia Commons (resized/cropped):
#1 Mount Everest (China): Luca Galuzzi (Lucag), CC BY-SA 2.5 – https://commons.wikimedia.org/wiki/File:Everest_North_Face_toward_Base_Camp_Tibet_Luca_Galuzzi_2006.jpg
#1 Mount Everest (Nepal): Rdevany, CC BY-SA 3.0 – https://commons.wikimedia.org/wiki/File:Mt._Everest_from_Gokyo_Ri_November_5,_2012.jpg
#3 K2 (Pakistan): Zacharie Grossen, CC BY-SA 4.0 – https://commons.wikimedia.org/wiki/File:Chogori.jpg
#4 Kangchenjunga (India): Tomabarker, CC BY 3.0 – https://commons.wikimedia.org/wiki/File:Kangchenjunga_PangPema.JPG
#5 Gangkhar Puensum (Bhutan): Gradythebadger, CC BY-SA 4.0 – https://commons.wikimedia.org/wiki/File:Gangkhar_puensum_summit.JPG
#6 Ismoil Somoni Peak (Tajikistan): Jaan Künnap, CC BY-SA 4.0 – https://commons.wikimedia.org/wiki/File:Kommunismi_m%C3%A4etipp_85.jpg
#7 Noshaq (Afghanistan): Louis Meunier, CC BY 3.0 – https://commons.wikimedia.org/wiki/File:Mount_Noshaq_seen_from_the_base_camp_(photo_Louis_Meunier).jpg
#8 Jengish Chokusu (Kyrgyzstan): Maryliflower, CC BY-SA 4.0 – https://commons.wikimedia.org/wiki/File:Jengish_Chokusu_(Victory_Peak,_Pik_Pobeda),_Southern_Inylchek_Glacier,_Tien_Shan_%E2%80%94_Golden_Hour.jpg
#9 Khan Tengri (Kazakhstan): Frederic Heymes, CC BY-SA 2.0 fr – https://commons.wikimedia.org/wiki/File:Vue_globale_du_versant_N_du_khan_Tengri.jpg
#10 Aconcagua (Argentina): Bjørn Christian Tørrissen, CC BY-SA 4.0 – https://commons.wikimedia.org/wiki/File:Aconcagua2016.jpg
#11 Ojos del Salado (Chile): sergejf, CC BY-SA 2.0 – https://commons.wikimedia.org/wiki/File:Ojos_del_Salado_looming_big_on_the_horizon.jpg
#12 Huascarán (Peru): MrBasically, CC BY-SA 4.0 – https://commons.wikimedia.org/wiki/File:Nevado_Huascar%C3%A1n_(south_view).jpg
#13 Nevado Sajama (Bolivia): Léo Guellec, CC BY-SA 2.0 – https://commons.wikimedia.org/wiki/File:Sajama_National_Park.jpg
#14 Chimborazo (Ecuador): Eduardo Navas, CC BY-SA 2.0 – https://commons.wikimedia.org/wiki/File:Volc%C3%A1n_Chimborazo_desde_Riobamba.jpg
#15 Denali (United States): public domain – https://commons.wikimedia.org/wiki/File:Wonder_Lake_and_Denali.jpg
#16 Mount Logan (Canada): public domain – https://commons.wikimedia.org/wiki/File:Mount_Logan.jpg
#17 Kilimanjaro (Tanzania): Sergey Pesterev, CC BY-SA 4.0 – https://commons.wikimedia.org/wiki/File:Kilimanjaro_from_Amboseli.jpg
#18 Hkakabo Razi (Myanmar): Iexcell, CC0 – https://commons.wikimedia.org/wiki/File:Khakaborazi_southview-m_ft.jpg
#19 Pico Cristóbal Colón (Colombia): Sylvain Perret, CC BY-SA 3.0 – https://commons.wikimedia.org/wiki/File:Pico_Cristobal_Colon.jpg
#20 Mount Elbrus (Russia): Jason Blue-Smith, CC BY-SA 2.0 – https://commons.wikimedia.org/wiki/File:Mt._Elbrus_in_Russia.jpg
#21 Pico de Orizaba (Mexico): México en Fotos, CC BY-SA 2.0 – https://commons.wikimedia.org/wiki/File:Pico_de_Orizaba_desde_Hidalgo,_Puebla.jpg
#22 Mount Damavand (Iran): Safa.daneshvar, CC BY-SA 4.0 – https://commons.wikimedia.org/wiki/File:981012-Damavand-South-IMG_9861-2.jpg
#23 Mount Kenya (Kenya): Ruud Zwart, CC BY-SA 2.5 nl – https://commons.wikimedia.org/wiki/File:Mount_kenya.JPG
#24 Shkhara (Georgia): Aleksey Muhranoff, CC BY-SA 3.0 – https://commons.wikimedia.org/wiki/File:Mt_Shkhara_as_seen_from_Khalde_(Photo_A._Muhranoff,_2011).jpg
#25 Mount Ararat (Turkey): W. Bulach, CC BY-SA 4.0 – https://commons.wikimedia.org/wiki/File:00_2399_Mount_Ararat,_Turkey.jpg
#26 Mount Stanley (DR Congo): El.Sarmiento, CC BY-SA 3.0 – https://commons.wikimedia.org/wiki/File:MtStanley_2.JPG
#26 Mount Stanley (Uganda): Rafał Kozubek, CC BY-SA 4.0 – https://commons.wikimedia.org/wiki/File:Alexandra_Peak_Margherita_Peak_Rwenzori.jpg
#28 Pico Bolívar (Venezuela): Oscar Costero, CC BY-SA 4.0 – https://commons.wikimedia.org/wiki/File:Pico_Bol%C3%ADvar_desde_el_Pico_el_Toro.jpg
#29 Puncak Jaya (Indonesia): Alfindra Primaldhi, CC BY 2.0 – https://commons.wikimedia.org/wiki/File:Puncakjaya.jpg
#30 Mont Blanc (France): Christian David, CC BY-SA 4.0 – https://commons.wikimedia.org/wiki/File:Mont_Maudit_and_Mont_Blanc_from_Aiguille_du_Midi,_Chamonix,_Haute-Savoie.jpg
#30 Mont Blanc (Italy): Hseugut, CC BY-SA 4.0 – https://commons.wikimedia.org/wiki/File:Mont_Blanc_Aiguille.jpg
#33 Dufourspitze (Switzerland): TobiasBender, CC BY-SA 3.0 – https://commons.wikimedia.org/wiki/File:MonteRosaWestseite_gesehenVomGornergrat.JPG
#34 Ras Dashen (Ethiopia): Marcoetio, CC BY-SA 3.0 – https://commons.wikimedia.org/wiki/File:Ras_dejen.jpg
#35 Mount Wilhelm (Papua New Guinea): Nomadtales, CC BY-SA 2.1 au – https://commons.wikimedia.org/wiki/File:Mount_Wilhelm.jpg
#36 Mount Karisimbi (Rwanda): Amakuru, CC BY-SA 3.0 – https://commons.wikimedia.org/wiki/File:Karisimbi2.jpg
#37 Mount Bazardüzü (Azerbaijan): Freieck, CC BY-SA 3.0 – https://commons.wikimedia.org/wiki/File:Bazarduzu_detail.JPG
#38 Khüiten Peak (Mongolia): Kobsev, CC BY 2.5 – https://commons.wikimedia.org/wiki/File:Ukok_Plateau_2.jpg
#39 Volcán Tajumulco (Guatemala): JoePhoto, CC BY 2.0 – https://commons.wikimedia.org/wiki/File:Tajumulco_volcano_01.jpg
#40 Toubkal (Morocco): SimonKing74, CC0 – https://commons.wikimedia.org/wiki/File:My_Toubkal.jpg
#41 Mount Kinabalu (Malaysia): kallerna, CC BY-SA 4.0 – https://commons.wikimedia.org/wiki/File:Kinabalu_Sabah_Borneo_Kampong_Kundasang_2.jpg
#42 Mount Aragats (Armenia): Armenak Margarian, CC BY-SA 4.0 – https://commons.wikimedia.org/wiki/File:Mount_Aragats_2020-05-11.jpg
#43 Mount Cameroon (Cameroon): Eric Joel MAMA NKE, CC BY-SA 4.0 – https://commons.wikimedia.org/wiki/File:Le_Char_des_Dieux_-_Fako_Mountain_-_Mount_Cameroon_National_Park_-_R%C3%A9gion_du_Sud-ouest.jpg
#44 Yushan (Taiwan): Chi-Hung Lin, CC BY-SA 2.0 – https://commons.wikimedia.org/wiki/File:Yushan_Main_Peak_seen_from_Dongpu_Mountain_in_the_afternoon_on_28_January_2017.jpg
#45 Cerro Chirripó (Costa Rica): Peter Andersen; derivative work: Mariordo, CC BY-SA 3.0 – https://commons.wikimedia.org/wiki/File:Cerro_Chirripo_Picture_1191_zoom_in.jpg
#46 Grossglockner (Austria): public domain – https://commons.wikimedia.org/wiki/File:Gro%C3%9Fglockner1.jpg
#47 Mount Fuji (Japan): 名古屋太郎 (edited by Hannes_24), CC BY-SA 3.0 – https://commons.wikimedia.org/wiki/File:Kodaki_fuji_frm_shojinko_refurb.jpg
#48 Aoraki / Mount Cook (New Zealand): W. Bulach, CC BY-SA 4.0 – https://commons.wikimedia.org/wiki/File:00_0985_Mount_Cook_-_New_Zealand_Alps.jpg
#49 Teide (Spain): Thomas Wolf, www.foto-tw.de, CC BY-SA 3.0 de – https://commons.wikimedia.org/wiki/File:Teide_von_Nordosten_(Zuschnitt_2).jpg
#50 Jabal an-Nabi Shu'ayb (Yemen): Franco Pecchio from Milano, Italy, CC BY 2.0 – https://commons.wikimedia.org/wiki/File:Haraz_200612_Yemen-117_(353667919).jpg
Data: Wikidata (CC0); USGS; national and university surveys; cross-checked with Wikipedia.
```

上面完整版带链接，约 7,000+ 字符，**超过 YouTube 描述 5,000 字符上限**。描述框用下面的紧凑版（名次、国家代码、作者、许可，约 1,900 字符），完整版放置顶评论或频道外的公开页面，由用户发布时决定。

```text
Photos: Wikimedia Commons (resized/cropped). Licences: creativecommons.org/licenses
#1 CN: Luca Galuzzi (Lucag), CC BY-SA 2.5
#1 NP: Rdevany, CC BY-SA 3.0
#3 PK: Zacharie Grossen, CC BY-SA 4.0
#4 IN: Tomabarker, CC BY 3.0
#5 BT: Gradythebadger, CC BY-SA 4.0
#6 TJ: Jaan Künnap, CC BY-SA 4.0
#7 AF: Louis Meunier, CC BY 3.0
#8 KG: Maryliflower, CC BY-SA 4.0
#9 KZ: Frederic Heymes, CC BY-SA 2.0 fr
#10 AR: Bjørn Christian Tørrissen, CC BY-SA 4.0
#11 CL: sergejf, CC BY-SA 2.0
#12 PE: MrBasically, CC BY-SA 4.0
#13 BO: Léo Guellec, CC BY-SA 2.0
#14 EC: Eduardo Navas, CC BY-SA 2.0
#15 US: public domain
#16 CA: public domain
#17 TZ: Sergey Pesterev, CC BY-SA 4.0
#18 MM: Iexcell, CC0
#19 CO: Sylvain Perret, CC BY-SA 3.0
#20 RU: Jason Blue-Smith, CC BY-SA 2.0
#21 MX: México en Fotos, CC BY-SA 2.0
#22 IR: Safa.daneshvar, CC BY-SA 4.0
#23 KE: Ruud Zwart, CC BY-SA 2.5 nl
#24 GE: Aleksey Muhranoff, CC BY-SA 3.0
#25 TR: W. Bulach, CC BY-SA 4.0
#26 CD: El.Sarmiento, CC BY-SA 3.0
#26 UG: Rafał Kozubek, CC BY-SA 4.0
#28 VE: Oscar Costero, CC BY-SA 4.0
#29 ID: Alfindra Primaldhi, CC BY 2.0
#30 FR: Christian David, CC BY-SA 4.0
#30 IT: Hseugut, CC BY-SA 4.0
#33 CH: TobiasBender, CC BY-SA 3.0
#34 ET: Marcoetio, CC BY-SA 3.0
#35 PG: Nomadtales, CC BY-SA 2.1 au
#36 RW: Amakuru, CC BY-SA 3.0
#37 AZ: Freieck, CC BY-SA 3.0
#38 MN: Kobsev, CC BY 2.5
#39 GT: JoePhoto, CC BY 2.0
#40 MA: SimonKing74, CC0
#41 MY: kallerna, CC BY-SA 4.0
#42 AM: Armenak Margarian, CC BY-SA 4.0
#43 CM: Eric Joel MAMA NKE, CC BY-SA 4.0
#44 TW: Chi-Hung Lin, CC BY-SA 2.0
#45 CR: Peter Andersen; derivative work: Mariordo, CC BY-SA 3.0
#46 AT: public domain
#47 JP: 名古屋太郎 (edited by Hannes_24), CC BY-SA 3.0
#48 NZ: W. Bulach, CC BY-SA 4.0
#49 ES: Thomas Wolf, www.foto-tw.de, CC BY-SA 3.0 de
#50 YE: Franco Pecchio from Milano, Italy, CC BY 2.0
Data: Wikidata (CC0), USGS, national surveys; checked against Wikipedia.
```
