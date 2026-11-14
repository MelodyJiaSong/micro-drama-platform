# ep20 · 数据出处、交叉核对与许可（sources.md）

> 2026-11-03 代理整理（follow-up 015 / 016）。本文件由 `_build/gen_sources.py` 生成；改数据请改 `_build/build.py` / `items_def.py` 后重跑 `build.py` → `gen_sources.py`。

## 1. 口径

- **榜单**：天然瀑布按**总落差**（total height：最高一级顶 → 最低一级底，含级间急流段）降序，取 ≥ 631 m 的 35 条。
- **主源**：World Waterfall Database（WWD）「Overall Height」榜 https://www.worldwaterfalldatabase.com/tallest-waterfalls/total-height ，2026-11-03 抓取前 3 页（105 条，≥ 549 m）及每条瀑布页（`_build/wwd_crawl.py` → `_build/raw/wwd_top.json`，原始 HTML 在 `_build/raw/wwd/`）。WWD 是私人网站（aggregator 级）；多数高度来自地形图 / 激光雷达估算或其实地三角测量，条目里写明依据。
- **主值覆盖规则**：有公开测量或权威记录的，用它而不用 WWD：
  - Angel Falls：979 m，Guinness World Records（1949 年 National Geographic 资助、Ruth Robertson 带队的测量）。WWD 只记主跌落 807 m（差 −17.6%，>10%，写入 notes，待用户确认）。
  - Yumbilla：895.4 m，秘鲁 IGN 2007 年激光测量（MercoPress 2007-12-04 报道；WWD 也引此数，列 896 m）。
  - 与 WWD 一致、只作佐证的：Gocta 771 m（2006 年 Ziemendorff 与秘鲁政府组织的测量，±13 m）、Yosemite 739 m（1913 年 USGS Matthes 测量；WWD 用 1 m 激光雷达复核）、Tugela 948 m（Guinness 引同一数）、Kukenán 674 m（委内瑞拉国家公园文件，经 WWD 转引）。
- **入选**：① 有名字；② WWD 状态 Cataloged（实地勘测）或 Confirmed 且条目写明高度依据；③ Unconfirmed 只在有独立权威测量 / 记录时收（Tugela、Yumbilla）；④ 水电引水后基本断流的不收。状态定义见 WWD 榜单页 Key。
- **显示**：`value_display` 四舍五入到整米；`secondary_display` = 米 × 3.28084 取整英尺（Yosemite 2,425 ft、Angel 3,212 ft 与官方英尺数一致）。
- **同值同名次**（1,1,3 式），同名次内按名称字母序。
- **季节性**：WWD「Flow Consistency」（一年里有水的月数，**不计冬季封冻**）< 12，或 WWD / Wikipedia 写明只在融雪或雨季有水 → `SEASONAL`；水电调节、每年保证放水 → `HYDRO-REGULATED`；无流量资料 → 不标，notes 写明。
- **国家**：所在地；留尼汪计 France。

## 2. 入选与排除（WWD 前 105 条里 ≥ 631 m 的条目）

| WWD 名次 | 瀑布 | WWD 高度 | WWD 状态 | 处理 | 原因 |
|---|---|---|---|---|---|
| 2 | Mattenbachfälle | 930 | Confirmed | 收 | 2020 年绳降实测 |
| 5 | Haloku Falls（夏威夷） | 887 | Unconfirmed | 不收 | 无独立测量 |
| 6 | Olo'upena Falls（夏威夷） | 878 | Unconfirmed | 不收 | 无独立测量（Wikipedia 列 900 m） |
| 3 | Tres Hermanas（秘鲁） | 914 | Unconfirmed | 不收 | 只有 WWD 数（Mongabay 等也引 WWD），无独立测量 |
| 12 | Los Chorros de Cura（委内瑞拉） | 821 | Unconfirmed | 不收 | 同上 |
| 13 | Pu'uka'oku Falls（夏威夷） | 812 | Unconfirmed | 不收 | 同上 |
| 17 | Mongefossen（挪威） | 773 | Confirmed（hydro） | 不收 | 1977 年并入 Grytten 水电站，WWD：「functionally dry」；洞察卡 3 |
| 21、27 | Unnamed Waterfall ×2（夏威夷） | 756 / 742 | Unconfirmed | 不收 | 无名、未证实 |
| 23 | Terror Falls（新西兰） | 750 | Confirmed | 不收 | 条目只有数字，无依据、无描述 |
| 25 | Helgåfossen（挪威） | 750 | Confirmed | 不收 | 同上，无坐标 |
| 28 | Wailele Falls（夏威夷） | 741 | Unconfirmed | 不收 | 无独立测量 |
| 33 | Mana'wai'nui Falls（夏威夷） | 719 | Unconfirmed | 不收 | 同上（Wikipedia 也标 citation needed） |
| 40 | Drivfoss（挪威） | 700 | Unconfirmed | 不收 | 无独立测量 |
| 41 | Brurasløret（挪威） | 700 | Confirmed | 不收 | 只有一句「700 m（possibly more）」，无依据 |
| 43 | Solitary Falls（新西兰） | 680 | Confirmed | 不收 | 条目只有数字 |
| 47 | Hidden Falls（新西兰） | 660 | Unconfirmed | 不收 | 无独立测量 |
| 51 | Aimoo Falls（夏威夷） | 640 | Unconfirmed | 不收 | 同上 |
| 52 | Brufossen（挪威） | 640 | Confirmed（hydro） | 不收 | 引水后崖面基本无水 |
| 53 | Breiteigsfossen（挪威） | 640 | Confirmed | 不收 | 条目只有数字 |
| 54 | Stäfelifälle（瑞士） | 634 | Unconfirmed | 不收 | 无独立测量 |
| — | Mutarazi Falls（津巴布韦） | 479 | Unconfirmed | 不收 | 常见 762 m；WWD 依高程剖面认为 762 m 是台地边缘到谷底的总落差，记 479 m；洞察卡 2 |
| 55 | Sentinel Fall（美国） | 631 | Cataloged | 收（第 35） | 下一条 Buskefoss 625 m（Confirmed、无依据），再下 Heggurfossen 620 m |

（WWD 名次栏是榜单原始位置；Angel Falls 在 WWD 榜上列第 14、807 m。）

## 3. 逐条主值、交叉核对与流量


| # | 瀑布 | 国家 | 主值 | 主源 | 交叉核对 | 差异 | WWD 状态 / 流量月数 / 页面更新 | 徽章 |
|---|---|---|---|---|---|---|---|---|
| 1 | Angel Falls | Venezuela | 979 m（979） | [Guinness World Records: Tallest waterfall (1949 survey, 979 m)](https://www.guinnessworldrecords.com/world-records/highest-waterfall) | [World Waterfall Database (counts only the 807 m main plunge)](https://www.worldwaterfalldatabase.com/waterfall/Kerepakupai-Meru-1)：807 m | -17.6% | Confirmed / 12 months / May 10, 2020 | HEIGHT DISPUTED |
| 2 | Tugela Falls | South Africa | 948 m（948） | [World Waterfall Database: Tugela Falls (total height 948 m); same figure in Guinness World Records](https://www.worldwaterfalldatabase.com/waterfall/Tugela-Falls-2) | [Wikipedia: List of waterfalls by height (rev 1379783845)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：947 m | -0.1% | Unconfirmed / 4 months / October 17, 2026 | SEASONAL |
| 3 | Mattenbach Falls | Switzerland | 930 m（930） | [World Waterfall Database: Mattenbachfälle (total height 930 m)](https://www.worldwaterfalldatabase.com/waterfall/Mattenbachf%C3%A4lle-27386) | [Wikipedia: List of waterfalls by height (rev 1379783845)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：840 m | -9.7% | Confirmed / — / October 10, 2020 | REMEASURED 2020 |
| 4 | Yumbilla Falls | Peru | 895 m（895.4） | [Instituto Geográfico Nacional (Peru) laser survey 2007, 895.4 m (reported by MercoPress 2007-12-04; WWD)](https://en.mercopress.com/2007/12/04/the-world-s-third-highest-waterfall-discovered-in-peru) | [World Waterfall Database: Yumbilla (896 m)](https://www.worldwaterfalldatabase.com/waterfall/Yumbilla-Catarata-811)：896 m | +0.1% | Unconfirmed / — / March 19, 2017 |  |
| 5 | Skorga Falls | Norway | 875 m（875） | [World Waterfall Database: Skorga (total height 875 m)](https://www.worldwaterfalldatabase.com/waterfall/Skorga-11652) | [Wikipedia: List of waterfalls by height (rev 1379783845)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：875 m | +0.0% | Cataloged / 9 months / September 26, 2020 | SEASONAL |
| 6 | Vinnufossen | Norway | 845 m（845） | [World Waterfall Database: Vinnu (total height 845 m)](https://www.worldwaterfalldatabase.com/waterfall/Vinnufallet-11651) | [Wikipedia: List of waterfalls by height (rev 1379783845)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：845 m | +0.0% | Cataloged / 9 months / October 13, 2026 | SEASONAL |
| 7 | James Bruce Falls | Canada | 840 m（840） | [World Waterfall Database: James Bruce Falls (total height 840 m)](https://www.worldwaterfalldatabase.com/waterfall/James-Bruce-Falls-1191) | [Wikipedia: List of waterfalls by height (rev 1379783845)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：840 m | +0.0% | Confirmed / — / March 19, 2017 |  |
| 8 | Browne Falls | New Zealand | 836 m（836） | [World Waterfall Database: Browne Falls (total height 836 m)](https://www.worldwaterfalldatabase.com/waterfall/Browne-Falls-18) | [Wikipedia: List of waterfalls by height (rev 1379783845)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：836 m | +0.0% | Confirmed / — / December 17, 2017 |  |
| 9 | Kjerrskredfossen | Norway | 831 m（831） | [World Waterfall Database: Kjerrskredfossen (total height 831 m)](https://www.worldwaterfalldatabase.com/waterfall/Kjerrskredfossen-5552) | 无第二来源（只有 WWD） | — | Cataloged / 7 months / May 10, 2020 | SEASONAL |
| 10 | Waihilau Falls | United States | 792 m（792） | [World Waterfall Database: Waihilau Falls (total height 792 m)](https://www.worldwaterfalldatabase.com/waterfall/Waihilau-Falls-639) | [Wikipedia: List of waterfalls by height (rev 1379783845)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：792 m | +0.0% | Confirmed / 12 months / March 19, 2017 |  |
| 11 | Colonial Creek Falls | United States | 783 m（783） | [World Waterfall Database: Colonial Creek Falls (total height 783 m)](https://www.worldwaterfalldatabase.com/waterfall/Colonial-Creek-Falls-4738) | [Wikipedia: List of waterfalls by height (rev 1379783845)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：788 m | +0.6% | Cataloged / 12 months / March 19, 2017 |  |
| 12 | Gocta Falls | Peru | 771 m（771） | [World Waterfall Database: Gocta (total height 771 m)](https://www.worldwaterfalldatabase.com/waterfall/Gocta-Catarata-805) | [Wikipedia: List of waterfalls by height (rev 1379783845)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：771 m | +0.0% | Confirmed / 12 months / May 31, 2021 |  |
| 13 | Kjelfossen | Norway | 765 m（765） | [World Waterfall Database: Kjelfossen (total height 765 m)](https://www.worldwaterfalldatabase.com/waterfall/Kjelfossen-45) | [Wikipedia: List of waterfalls by height (rev 1379783845)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：755 m | -1.3% | Cataloged / 10 months / May 10, 2020 | SEASONAL |
| 14 | Isella Falls | United States | 762 m（762） | [World Waterfall Database: Isella Falls (total height 762 m)](https://www.worldwaterfalldatabase.com/waterfall/Isella-Falls-4550) | 无第二来源（只有 WWD） | — | Confirmed / — / March 30, 2025 |  |
| 15 | Johannesburg Falls | United States | 751 m（751） | [World Waterfall Database: Johannesburg Falls (total height 751 m)](https://www.worldwaterfalldatabase.com/waterfall/Johannesburg-Falls-3083) | [Wikipedia: List of waterfalls by height (rev 1379783845)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：751 m | +0.0% | Cataloged / — / August 27, 2017 |  |
| 16 | Tjøtafossen | Norway | 750 m（750） | [World Waterfall Database: Tjøtafossen (total height 750 m)](https://www.worldwaterfalldatabase.com/waterfall/Tjotafossen-415) | 无第二来源（只有 WWD） | — | Cataloged / 9 months / October 05, 2020 | SEASONAL |
| 17 | Døntefossen | Norway | 745 m（745） | [World Waterfall Database: Døntefossen (total height 745 m)](https://www.worldwaterfalldatabase.com/waterfall/Dontefossen-11) | [Wikipedia: List of waterfalls by height (rev 1379783845)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：700 m | -6.0% | Cataloged / — / October 13, 2026 |  |
| 18 | Yosemite Falls | United States | 739 m（739） | [World Waterfall Database: Yosemite Falls (total height 739 m)](https://www.worldwaterfalldatabase.com/waterfall/Yosemite-Falls-9) | [USGS: highest measured waterfall in North America, 2,425 ft (739 m)](https://www.usgs.gov/media/images/yosemite-falls-all-three-sections)：739 m | +0.0% | Cataloged / 8 months / April 04, 2026 | SEASONAL |
| 19 | Cloudcap Falls | United States | 732 m（732） | [World Waterfall Database: Cloudcap Falls (total height 732 m)](https://www.worldwaterfalldatabase.com/waterfall/Cloudcap-Falls-4959) | [Wikipedia: List of waterfalls by height (rev 1379783845)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：732 m | +0.0% | Confirmed / — / March 01, 2024 | SEASONAL |
| 20 | Boulder Glacier Falls | United States | 727 m（727） | [World Waterfall Database: Boulder Glacier Falls (total height 727 m)](https://www.worldwaterfalldatabase.com/waterfall/Boulder-Glacier-Falls-10285) | 无第二来源（只有 WWD） | — | Confirmed / — / January 03, 2025 |  |
| 21 | Trou de Fer Falls | France | 725 m（725） | [World Waterfall Database: Trou de Fer (total height 725 m)](https://www.worldwaterfalldatabase.com/waterfall/Trou-de-Fer-Cascades-de-130) | [Wikipedia: List of waterfalls by height (rev 1379783845)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：725 m | +0.0% | Confirmed / 12 months / May 31, 2021 |  |
| 22 | Kjeragfossen | Norway | 715 m（715） | [World Waterfall Database: Kjeragfossen (total height 715 m)](https://www.worldwaterfalldatabase.com/waterfall/Kjeragfossen-671) | [Wikipedia: List of waterfalls by height (rev 1379783845)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：715 m | +0.0% | Confirmed / — / March 29, 2020 | SEASONAL |
| 22 | Yutajé Falls | Venezuela | 715 m（715） | [World Waterfall Database: Yutajé (total height 715 m)](https://www.worldwaterfalldatabase.com/waterfall/Yutaje-Salto-19) | [Wikipedia: List of waterfalls by height (rev 1379783845)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：671 m | -6.2% | Confirmed / 12 months / May 31, 2021 |  |
| 24 | Tågfossen | Norway | 710 m（710） | [World Waterfall Database: Tågfossen (total height 710 m)](https://www.worldwaterfalldatabase.com/waterfall/Tagfossen-6273) | 无第二来源（只有 WWD） | — | Cataloged / 8 months / October 05, 2020 | SEASONAL |
| 24 | Ølmåfossen | Norway | 710 m（710） | [World Waterfall Database: Ølmåfossen (total height 710 m)](https://www.worldwaterfalldatabase.com/waterfall/%C3%98lm%C3%A5fossen-30753) | [Wikipedia: List of waterfalls by height (rev 1379783845)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：720 m | +1.4% | Cataloged / — / October 13, 2026 |  |
| 26 | Cabin Boy Falls | New Zealand | 701 m（701） | [World Waterfall Database: Cabin Boy Falls (total height 701 m)](https://www.worldwaterfalldatabase.com/waterfall/Cabin-Boy-Falls-22806) | 无第二来源（只有 WWD） | — | Confirmed / — / May 10, 2020 |  |
| 27 | Sprænefossen | Norway | 700 m（700） | [World Waterfall Database: Sprænefossen (total height 700 m)](https://www.worldwaterfalldatabase.com/waterfall/Balaifossen-633) | [Wikipedia list (as 'Balåifossen', old WWD estimate)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：850 m | +21.4% | Cataloged / 7 months / January 03, 2026 | SEASONAL |
| 28 | Lake Unknown Falls | New Zealand | 680 m（680） | [World Waterfall Database: Lake Unknown Falls (total height 680 m)](https://www.worldwaterfalldatabase.com/waterfall/Lake-Unknown-Falls-699) | [Wikipedia: List of waterfalls by height (rev 1379783845)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：680 m | +0.0% | Confirmed / — / December 17, 2017 |  |
| 29 | Kukenán Falls | Venezuela | 674 m（674） | [World Waterfall Database: Kukenaam (total height 674 m)](https://www.worldwaterfalldatabase.com/waterfall/Kukenaam-Salto-21) | [Wikipedia: List of waterfalls by height (rev 1379783845)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：674 m | +0.0% | Confirmed / 7 months / March 19, 2017 | SEASONAL |
| 30 | Seahpo Peak Falls | United States | 671 m（671） | [World Waterfall Database: Seahpo Peak Falls (total height 671 m)](https://www.worldwaterfalldatabase.com/waterfall/Seahpo-Peak-Falls-4962) | [Wikipedia: Seahpo Peak Falls (about 2,200 ft / 670 m)](https://en.wikipedia.org/wiki/Seahpo_Peak_Falls)：670 m | -0.1% | Cataloged / — / March 19, 2017 | SEASONAL |
| 31 | Sulphide Creek Falls | United States | 665 m（665） | [World Waterfall Database: Sulphide Creek Falls (total height 665 m)](https://www.worldwaterfalldatabase.com/waterfall/Sulphide-Creek-Falls-3367) | 无第二来源（只有 WWD） | — | Cataloged / 12 months / March 19, 2017 |  |
| 32 | Ägertenbach Falls | Switzerland | 660 m（660） | [World Waterfall Database: Äegertenbachfall (total height 660 m)](https://www.worldwaterfalldatabase.com/waterfall/%C3%84egertenbachfall-27203) | 无第二来源（只有 WWD） | — | Confirmed / — / December 13, 2021 |  |
| 33 | Mardalsfossen | Norway | 645 m（645） | [World Waterfall Database: Mardalsfossen (total height 645 m)](https://www.worldwaterfalldatabase.com/waterfall/Mardalsfossen-14) | [Statistics Norway (SSB) via WWD — head of the hydro scheme, 704 m](https://www.worldwaterfalldatabase.com/waterfall/Mardalsfossen-14)：704 m | +9.1% | Cataloged / 9 months / October 13, 2026 | HYDRO-REGULATED |
| 34 | Cascade Blanche | France | 640 m（640） | [World Waterfall Database: Blanche (total height 640 m)](https://www.worldwaterfalldatabase.com/waterfall/Blanche-Cascade-60) | [Wikipedia: List of waterfalls by height (rev 1379783845)](https://en.wikipedia.org/w/index.php?title=List_of_waterfalls_by_height&oldid=1379783845)：640 m | +0.0% | Confirmed / — / April 29, 2025 |  |
| 35 | Sentinel Fall | United States | 631 m（631） | [World Waterfall Database: Sentinel Fall (total height 631 m)](https://www.worldwaterfalldatabase.com/waterfall/Sentinel-Fall-24) | [Wikipedia: Sentinel Falls (1,920 ft / 590 m)](https://en.wikipedia.org/wiki/Sentinel_Fall)：590 m | -6.5% | Cataloged / 6 months / February 14, 2026 | SEASONAL |

### notes（逐条判断依据）

- **#1 Angel Falls**：979 m = 1949 survey of an expedition funded by National Geographic (Ruth Robertson), recognised by Guinness. WWD argues the survey was sighted from the Río Carrao/Caroní ~2 km away and includes ~170 m of river below the falls; it lists only the 807 m main plunge (−17.6%, >10%: kept 979 by our 'published survey/record first' rule — user to confirm). Guinness itself notes that if only 807 m counts, Tugela (948 m) is the tallest. Wikipedia list: 979 m.
- **#2 Tugela Falls**：WWD flow consistency 4 months (rainy season, Nov–Mar); WWD status 'Unconfirmed' but the 948 m figure is the one Guinness quotes, so it passes our 'independent record' rule. 2016 Czech team (Petr Jan Juračka) measured 983 m, but WWD says from >1 km below the falls; not used. Lower tiers hidden in a gorge; true height not settled.
- **#3 Mattenbach Falls**：Earlier estimate 840 m (still in Wikipedia list, −9.7%). In 2020 the Vertical Water Canyoning Team abseiled the falls and measured ~930 m (WWD), making it the tallest in Eurasia. Tiny 0.9 km² catchment — can dry out in late-summer drought, so no SEASONAL badge (WWD gives no flow-months figure).
- **#4 Yumbilla Falls**：IGN Peru laser survey 2007: 895.4 m (displayed 895 m). WWD 896 m, Wikipedia list 896 m. WWD status Unconfirmed, admitted under our independent-survey rule. Flow regime not documented (best in rainy season); no badge.
- **#5 Skorga Falls**：Height from 1-m contour maps (WWD, visited/catalogued). Only the lower ~600 m is visible from the valley floor. WWD flow consistency 9 months (best April–July).
- **#6 Vinnufossen**：WWD (2026-10-13) says the recognised name is Vinnu (Vinnufallet) and calls Vinnufossen incorrect; kept the widely used name Vinnufossen on screen. Earlier WWD estimate 865 m, revised to 845 m. Glacier-fed; flow consistency 9 months (best May–Sept).
- **#7 James Bruce Falls**：WWD: tallest fall it has catalogued in North America; small glacial source likely sustains year-round flow, but volume is low. No flow-months figure; no badge.
- **#8 Browne Falls**：WWD: falls drop out of Lake Browne at 836 m straight to Doubtful Sound; Te Ara and older sources give 619 m (2,031 ft) (−26%, >10%: WWD figure kept, it follows the topographic lake level). Year-round flow (WWD high-volume months 12).
- **#9 Kjerrskredfossen**：Two side-by-side streams; surveyed by WWD in 2011. Not in the Wikipedia list (no second source). Flow consistency 7 months (best March–June).
- **#10 Waihilau Falls**：Height = amphitheatre wall per USGS topo (WWD). Flow consistency 12 months.
- **#11 Colonial Creek Falls**：WWD triangulated 783 m in Aug 2011 (earlier topo estimate 788 m, still in Wikipedia list; Wikipedia article 783 m). Flows all year (WWD).
- **#12 Gocta Falls**：Measured 771 m (±13 m) by a survey organised by Stefan Ziemendorff and the Peruvian government, announced 2006; known to locals for centuries but not to the outside world. Perennial (Wikipedia; WWD 12 months).
- **#13 Kjelfossen**：WWD re-evaluated several times; current 765 m is for the centre stream (Vetle Kjelfossen). Wikipedia list 755 m (−1.3%). Flow consistency 10 months (best March–July).
- **#14 Isella Falls**：WWD estimate from topographic data: top tentatively at 6,650 ft, total ~762 m; could be taller. No second source. Glacier-fed; flow months not documented; no badge.
- **#15 Johannesburg Falls**：WWD from USGS topo: just over 2,400 ft from the glacier, ending in a ~800 ft drop. Flow months not documented; no badge.
- **#16 Tjøtafossen**：WWD: ~750 m from the glacier toe; top shifts as the glacier advances/retreats. Flow consistency 9 months. No second source.
- **#17 Døntefossen**：WWD from 1-m contour maps: 745 m in three sections; Wikipedia list and Norwegian Wikipedia ~700 m (−6%). Lakes above keep a fairly steady flow most of the year (frozen in winter); no flow-months figure, no badge.
- **#18 Yosemite Falls**：2,425 ft from François Matthes' 1913 USGS survey; WWD confirms with 1-m USGS lidar. Usually stops flowing in late summer/fall (WWD flow consistency 8 months).
- **#19 Cloudcap Falls**：WWD: ~2,400 ft of continuous bedrock cascades, almost all hidden in an incised channel; flows only during the melt season. Wikipedia calls it more seasonal than Seahpo Peak Falls.
- **#20 Boulder Glacier Falls**：WWD: ~2,350 ft chain of falls and cascades at the head of Bowman Creek's valley; glacier nearly gone, may become seasonal. No second source; no badge.
- **#21 Trou de Fer Falls**：WWD: initial horsetail ~213 m, then ~183 m, then ~305 m streams into the gorge and an ~24 m final plunge. Flows year-round (WWD 12 months). Réunion is an overseas region of France: flag = France.
- **#22 Kjeragfossen**：Single near-free-falling plunge, tallest free leap in Europe (WWD). Flows only with snowmelt or heavy rain; about 5 months a year (Wikipedia).
- **#22 Yutajé Falls**：WWD: surveyed 715 m (survey source not named), satellite relief consistent. Wikipedia list 'Salto Yutaj' 671 m (−6.2%). Flows year-round (WWD).
- **#24 Tågfossen**：WWD visited: one delicate horsetail of 710 m from a small lake; usually dry in late summer. Flow consistency 8 months. No second source.
- **#24 Ølmåfossen**：WWD: ~710 m veiling down the Trollveggen massif cliffs; Wikipedia list 720 m (+1.4%). Glacier and lakes; flow months not documented; no badge.
- **#26 Cabin Boy Falls**：WWD from 1:50,000 topo maps vs imagery: 700–750 m, possibly up to 800 m; listed at 701 m. Topo maps mark only a 124 m drop. No second source.
- **#27 Sprænefossen**：Official name Sprænefossen (Norgeskart); formerly listed as Balåifossen 850 m — WWD's 2011 survey cut it to ~700 m (Wikipedia still shows 850, +21%). Low volume, may dry in late summer (WWD 7 months).
- **#28 Lake Unknown Falls**：WWD: falls drop out of Lake Unknown in several leaps to the Dart River valley floor; NZ topo shows only the 150 m upper leap. Flow months not documented.
- **#29 Kukenán Falls**：674 m quoted from a Venezuelan National Park document (via WWD). WWD flow consistency 7 months. Often wrongly called one of the five tallest falls.
- **#30 Seahpo Peak Falls**：WWD: about 2,200 ft in several narrow tiers; flows well in summer but only while snow melts; Wikipedia calls it intermittent → SEASONAL.
- **#31 Sulphide Creek Falls**：WWD: almost 2,200 ft below Sulphide Lake outlet, mostly hidden in a narrow flume; year-round (WWD 12 months). Wikipedia article gives similar height (number not retrieved, API rate limit).
- **#32 Ägertenbach Falls**：WWD from topographic models: two tiers of ~230 m and ~330 m. No second source; flow months not documented.
- **#33 Mardalsfossen**：Diverted into the Grytten hydro plant since 1977; licence guarantees a minimum release 20 June–20 August. WWD 645 m from topography; SSB 704 m reflects hydro head (+9%); often cited 655–705 m. WWD tallest drop 328 m (lower tier); upper free fall 262 m (often quoted 297 m).
- **#34 Cascade Blanche**：WWD from French topo maps: from the ~840 m to ~200 m contour, four leaps, top drop ~400 m; some sources say up to 800 m. Best in the wet season; flow months not documented.
- **#35 Sentinel Fall**：WWD (visited 2013): 2,070 ft in ~11 steps; Wikipedia 1,920 ft (−6.5%). Usually dries out by July (WWD flow consistency 6 months).

## 4. 洞察卡依据

| after | 文字 | 依据 |
|---|---|---|
| 30 | SEASONAL = it flows only part of the year, fed by snowmelt or rainy-season runoff. | WWD Flow Consistency 定义（一年有水月数，不计封冻）；14 条 SEASONAL 的月数见 §3 |
| 21 | Zimbabwe's Mutarazi is often listed at 762 m; World Waterfall Database estimates ~479 m. | Wikipedia 列表 762 m、条目 772 m；WWD Mutarazi 页（2025-05-27 更新）记 479 m，理由：762 m 是台地边缘到 Honde 谷底的高程差（Google Earth 高程剖面），WWD 状态 Unconfirmed，所以屏上写成 WWD 的估算（审片第 7 条） |
| 12 | Norway's Mongefossen (773 m) would rank here, but hydropower has kept it dry since 1977. | WWD Mongefossen 页：773 m；1977 年 Mongeelva 并入 Grytten 水电站，此后「functionally dry」。773 m 正好落在第 11（783）与第 12（771）之间 |
| 4 | Next: a Swiss fall that grew 90 m in 2020, when canyoneers abseiled down and measured it. | WWD Mattenbachfälle 页：原估 840 m，2020 年 Vertical Water Canyoning Team 绳降实测约 930 m（+90 m）；Wikipedia 列表仍是 840 m |
| 2 | Angel's 979 m adds rapids below its 807 m drop. Drop those and Tugela (948 m) wins. | Guinness 页：979 m 总落差、807 m 最长单级，「若 Angel 的实际高度只有最初 807 m 那一段，多级的 948 m Tugela 就是最高」（比的是 Angel 807 m 与 Tugela 948 m 总落差，不是单级对单级；2026-11-04 审片第 3 条改措辞）；Wikipedia Angel Falls：979 m 含主跌落下方约 400 m 的斜坡急流；WWD 同论 |

## 5. 许可核实

- **WWD**：`/legal-disclaimer`（2026-11-03 读，存 `_build/raw/wwd_legal.html`）。版权条款只写照片：「All photographs utilized throughout the World Waterfall Database are protected under International Copyright Law … may not be used … without written consent」。对文字与数值没有限制条款；本期只引事实数值（高度、落差、流量月数、状态），不复制描述文字、不用其照片。描述框注明「Heights: World Waterfall Database」。
- **Guinness**：只引纪录数值（事实）。**MercoPress / USGS**：只引数值；USGS 为美国政府公有领域。
- **Wikipedia**：只作交叉核对（CC BY-SA 文字不搬运）。抓取时 query API 多次 429，部分条目只取到 REST 导语，已在 `_build/content/` 标明。
- **图片**：Codex 联网搜索（follow-up 009 / 016），逐张许可见 `assets.json` 与 §6。

## 6. 图片来源

| # | 瀑布 | 文件 | 作者 | 许可 | 来源页 | 备注 |
|---|---|---|---|---|---|---|
| 1 | Angel Falls | `assets/img/01_angel_falls.jpg` | Jorge Saturno | CC BY-SA 3.0 | https://imaggeo.egu.eu/view/19005/ | 主图 |
| 2 | Tugela Falls | `assets/img/02_tugela_falls.jpg` | Hougaard Malan | unknown (fine-art print gallery) | https://osnerartgallery.com/products/tugela-falls | 主图；licence unknown |
| 2 | Tugela Falls | `assets/img/02_tugela_falls_alt.jpg` | Mike and Lara Wolfe | CC0 1.0 | https://www.flickr.com/photos/threepwolfe/39498453682/ | 默认版替代图 |
| 3 | Mattenbach Falls | `assets/img/03_mattenbach_falls.jpg` | unknown | All rights reserved | https://www.europeanwaterfalls.com/waterfalls/mattenbachfall/ | 主图；licence unknown |
| 3 | Mattenbach Falls | `assets/img/03_mattenbach_falls_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 默认版替代图 |
| 4 | Yumbilla Falls | `assets/img/04_yumbilla_falls.jpg` | Paulo Tomaz | CC BY-SA 2.0 | https://www.flickr.com/photos/locoperucho/4658174737/ | 主图 |
| 5 | Skorga Falls | `assets/img/05_skorga_falls.jpg` | Sylwia Smolkowska | All rights reserved (Wszystkie prawa zastrzeżone) | https://kieruneknorwegia.pl/najwyzszy-wodospad-w-norwegii/ | 主图；licence unknown |
| 5 | Skorga Falls | `assets/img/05_skorga_falls_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 默认版替代图 |
| 6 | Vinnufossen | `assets/img/06_vinnufossen.jpg` | Johnny Cheng | All Rights Reserved | https://www.world-of-waterfalls.com/waterfalls/norway-vinnufossen/ | 主图；licence unknown |
| 6 | Vinnufossen | `assets/img/06_vinnufossen_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 默认版替代图 |
| 7 | James Bruce Falls | `assets/img/07_james_bruce_falls_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 主图 |
| 8 | Browne Falls | `assets/img/08_browne_falls.jpg` | Floyd Wilde | CC BY-SA 2.0 | https://www.wondermondo.com/browne-falls/ | 主图 |
| 9 | Kjerrskredfossen | `assets/img/09_kjerrskredfossen.jpg` | John Wise | unknown | https://www.johnwise.com/2023/09/08/fjord-cruise-to-gudvangen-norway/ | 主图；licence unknown |
| 9 | Kjerrskredfossen | `assets/img/09_kjerrskredfossen_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 默认版替代图 |
| 10 | Waihilau Falls | `assets/img/10_waihilau_falls.jpg` | Bruce Omori | unknown | https://instagrammernews.com/detail/2517112525483551226 | 主图；licence unknown |
| 10 | Waihilau Falls | `assets/img/10_waihilau_falls_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 默认版替代图 |
| 11 | Colonial Creek Falls | `assets/img/11_colonial_creek_falls.jpg` | Northwest Waterfall Survey | All rights reserved (© Northwest Waterfall Survey) | https://www.waterfallsnorthwest.com/waterfall/Colonial-Creek-Falls-4738 | 主图；licence unknown |
| 11 | Colonial Creek Falls | `assets/img/11_colonial_creek_falls_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 默认版替代图 |
| 12 | Gocta Falls | `assets/img/12_gocta_falls.jpg` | MI PERÚ | Public Domain Mark 1.0 | https://www.flickr.com/photos/134894678@N07/30849364486/ | 主图 |
| 13 | Kjelfossen | `assets/img/13_kjelfossen.jpg` | Øyvind Holmstad | CC BY-SA 2.0 | https://www.flickr.com/photos/78304219@N06/54396656048/ | 主图 |
| 14 | Isella Falls | `assets/img/14_isella_falls.jpg` | Kyle McCrohan | unknown | https://climberkyle.com/2023/10/06/golden-holden-high-route/ | 主图；licence unknown |
| 14 | Isella Falls | `assets/img/14_isella_falls_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 默认版替代图 |
| 15 | Johannesburg Falls | `assets/img/15_johannesburg_falls_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 主图 |
| 16 | Tjøtafossen | `assets/img/16_tjotafossen.jpg` | Arnt Flatmo | unknown | https://www.westcoastpeaks.com/Peaks/kattanakken1.html | 主图；licence unknown |
| 16 | Tjøtafossen | `assets/img/16_tjotafossen_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 默认版替代图 |
| 17 | Døntefossen | `assets/img/17_dontefossen.jpg` | World of Waterfalls (Johnny Cheng) | All Rights Reserved | https://www.world-of-waterfalls.com/waterfalls/norway-dontefossen/ | 主图；licence unknown |
| 17 | Døntefossen | `assets/img/17_dontefossen_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 默认版替代图 |
| 18 | Yosemite Falls | `assets/img/18_yosemite_falls.jpg` | Barbara Sheldrake | Pexels License | https://www.pexels.com/photo/photo-of-yosemite-national-park-5967655/ | 主图 |
| 19 | Cloudcap Falls | `assets/img/19_cloudcap_falls_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 主图 |
| 20 | Boulder Glacier Falls | `assets/img/20_boulder_glacier_falls_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 主图 |
| 21 | Trou de Fer Falls | `assets/img/21_trou_de_fer_falls.jpg` | Jean-Marc Astesana | CC BY-SA 2.0 | https://www.flickr.com/photos/jean-marc_astesana/2639508789/ | 主图 |
| 22 | Kjeragfossen | `assets/img/22_kjeragfossen_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 主图 |
| 22 | Yutajé Falls | `assets/img/23_yutaje_falls_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 主图 |
| 24 | Tågfossen | `assets/img/24_tagfossen.jpg` | World Waterfall Database | All rights reserved (WWD: photos may not be used without written consent) | https://www.worldwaterfalldatabase.com/waterfall/Tagfossen-6273 | 主图；licence unknown |
| 24 | Tågfossen | `assets/img/24_tagfossen_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 默认版替代图 |
| 24 | Ølmåfossen | `assets/img/25_olmafossen_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 主图 |
| 26 | Cabin Boy Falls | `assets/img/26_cabin_boy_falls_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 主图 |
| 27 | Sprænefossen | `assets/img/27_spraenefossen_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 主图 |
| 28 | Lake Unknown Falls | `assets/img/28_lake_unknown_falls_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 主图 |
| 29 | Kukenán Falls | `assets/img/29_kukenan_falls_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 主图 |
| 30 | Seahpo Peak Falls | `assets/img/30_seahpo_peak_falls.jpg` | Northwest Waterfall Survey | All rights reserved (© Northwest Waterfall Survey) | https://www.waterfallsnorthwest.com/waterfall/Seahpo-Peak-Falls-4962 | 主图；licence unknown |
| 30 | Seahpo Peak Falls | `assets/img/30_seahpo_peak_falls_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 默认版替代图 |
| 31 | Sulphide Creek Falls | `assets/img/31_sulphide_creek_falls.jpg` | Northwest Waterfall Survey | All rights reserved (© Northwest Waterfall Survey) | https://www.waterfallsnorthwest.com/waterfall/Sulphide-Creek-Falls-3367 | 主图；licence unknown |
| 31 | Sulphide Creek Falls | `assets/img/31_sulphide_creek_falls_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 默认版替代图 |
| 32 | Ägertenbach Falls | `assets/img/32_agertenbach_falls_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 主图 |
| 33 | Mardalsfossen | `assets/img/33_mardalsfossen.jpg` | Stefan Serena | CC0 1.0 | https://www.flickr.com/photos/146738176@N02/46267954504/ | 主图 |
| 34 | Cascade Blanche | `assets/img/34_cascade_blanche.jpg` | VillageHero | CC BY-SA 2.0 | https://www.flickr.com/photos/villagehero/31440817111/ | 主图 |
| 35 | Sentinel Fall | `assets/img/35_sentinel_fall.jpg` | World Waterfall Database | All rights reserved (WWD: photos may not be used without written consent) | https://www.worldwaterfalldatabase.com/waterfall/Sentinel-Fall-24 | 主图；licence unknown |
| 35 | Sentinel Fall | `assets/img/35_sentinel_fall_gen.png` | AI-generated | AI-generated (Codex image_gen) |  | 默认版替代图 |
