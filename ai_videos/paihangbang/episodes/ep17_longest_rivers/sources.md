# ep17 · 数据出处、交叉核对与许可（sources.md）

> 2026-11-03 代理整理（用户授权自主决策）。本文件由 `_build/gen_sources.py` 从 `data.json` / `assets.json` 生成；改数据请改 `_build/items_def.py` 后重跑 `build.py` → `gen_sources.py`。

## 1. 口径

- **榜单**：世界最长的 50 条河（含大支流），按长度（km）降序；副显示英里（km × 0.621371 四舍五入）。
- **长度主值**：一律取 **Encyclopaedia Britannica** 当前条目公布值（britannica.com 直连被 Cloudflare 拦，经 web.archive.org 2025–2026 快照取原文，存于 `_build/raw/brit/`）。Britannica 给出「从最远源头量起」的水系长度时取水系值（Mississippi–Missouri、Yenisey–Angara–Selenga、Ob–Irtysh、Amur–Argun、Mackenzie–Peace–Finlay、Syr Darya–Naryn、Madeira–Mamoré、Japurá–Caquetá、Ubangi–Uele、Nelson–Saskatchewan），否则取该河本身长度。例外两条（2026-11-04 QC 后写定）：
  1. **缺水系合计**：仅当 Britannica 给出了各段长度、却没有水系合计时，才改用国家机构的水系值——Murray–Darling 取 Geoscience Australia 3,672 km（Britannica 只分别给 Murray 2,530、Darling 2,739）。Pearl–Xi 不满足（Britannica 无任何总长），**不收**；Red River (US) 的 Britannica 条目无长度，不收。
  2. **离群值**：Britannica 值与同一源头、同一河口的其他权威数值相差 > 25%，且没有不同源头 / 河口等口径可以解释时，改用通行值并注明 Britannica 的数：Zambezi 3,540 → 2,574 km（第 34 名）；Orinoco 2,740 → 2,140 km（落到第 51 名，出榜）。其余差 > 10% 的条目（Amur、Mekong、Juruá、Brahmaputra、Euphrates、Tocantins、Salween、Colorado、Irrawaddy）都能用源头 / 河口 / 测法解释，保留 Britannica（见 §3）。
- **不重复计**：已作为更长水系一段的河不再单列（Missouri、Mississippi 本干、Irtysh、Ob 本干、Yenisey 本干、Selenga、Angara、Argun、Ucayali、Darling、Peace、Naryn、Mamoré、Caquetá、Uele）；不在水系主线上的大支流照列（Madeira、Purus、Juruá、Japurá、Negro、Lower Tunguska、Vilyuy、Aldan、Ishim、Arkansas、Paraguay、Pilcomayo、Araguaia、Ubangi、Kasai）。
- **为什么不用维基列表的数**：Wikipedia「List of river systems by length」(revid 见 data.json cross_check) 绝大多数行无引用，且混用「到汇入点」与「到海」两种量法（如 Brahmaputra 3,969 含 Padma–Meghna；Tocantins–Araguaia 3,650；Irrawaddy 2,809 含 N'Mai 源）。本期只作交叉核对。
- **国家（国旗）**：河口所在国——入海、入湖或汇入更大河流的地方。河口在两国界上（Congo、Rio Grande、Ubangi、Paraguay、Pilcomayo）取两国中流域面积较大的一国（代理判断，见 §2）。**屏上写明**：片头 / 页眉统计行「Flag = where the river ends」，卡上国家行写「ENDS IN …」（QC M3）。
- **大洲（计分板）**：河口所在大洲。Ural 河口阿特劳跨欧亚界，按惯例计 Europe；Murray–Darling 计 Oceania。
- **同值同名次**：Rio Negro 与 Ubangi–Uele 同为 2,250 km，并列第 46，按名称字母序；下一名为 48。
- **统计期**：2026-11-03 取数（Britannica 快照 2025-08 至 2026-02）。河长不是年度数据，标题年份 (2026) 指取数时间。

## 2. 归属与判断（待用户复核）

| 议题 | 本期做法 | 依据 |
|---|---|---|
| 国旗规则 | 河口所在国（不是流域最大国，也不是「最出名的国家」） | brief 二选一；河口是可核实的单点，跨国大河少争议 |
| Nile → Egypt | 河口在埃及 | 流域最大国是 Sudan；按河口规则取 Egypt |
| Ganges / Brahmaputra → Bangladesh | 两河在孟加拉汇合入海（Padma/Meghna） | 河口规则；观众多以为 India，卡片地点行写 Himalaya → Bay of Bengal；notes 写明 |
| Congo → DR Congo | 河口在刚果（金）–安哥拉界上，取流域较大的刚果（金） | 边界河口规则 |
| Rio Grande → United States | 河口在美墨界上，取流域较大的美国；徽章 US–MEXICO BORDER | 边界河口规则 |
| Colorado → Mexico | 河口在墨西哥加利福尼亚湾 | 河口规则；洞察卡说明它如今很少流到海 |
| Paraguay / Pilcomayo → Paraguay | 两河都在巴拉圭–阿根廷界上汇入，取 Paraguay | 代理判断，流域份额未单独核实 |
| Ubangi → DR Congo | 在刚果（金）–刚果（布）界上汇入 Congo，取刚果（金） | 边界河口规则 |
| Ishim → Russia | 源头与大半在哈萨克斯坦（流经阿斯塔纳），在俄罗斯汇入 Irtysh | 河口规则 |
| Ural → Kazakhstan / Europe | 河口阿特劳；大洲按惯例计 Europe | Wikipedia 列表着色亦为 Europe |
| Amazon 徽章 LENGTH DISPUTED | Britannica 称其长度仍有争议 | Britannica Amazon 条目、INPE 2008、Liu 2009 |

## 3. 差异 > 10% 的条目（交叉核对，需人决定是否换值）

| # | 河 | 主值（Britannica） | 交叉核对 | 差异 | 说明 |
|---|---|---|---|---|---|
| 10 | Amur–Argun | 4,444 | 5,498（Liu et al. 2009） | 23.7% | Amur proper (from the Shilka–Argun confluence) is 2,824 km (Britannica article); system with the Argun 4,444 km (Britannica table). For ~1,600 km the Amur forms |
| 12 | Mekong | 4,350 | 4,909（Liu et al. 2009） | 12.9% | Flows through China, Myanmar, Laos, Thailand, Cambodia and Vietnam (Britannica). Liu et al. 2009 measured 4,909 km (12.8% longer); MRC/FAO materials use about 4 |
| 18 | Juruá | 3,283 | 2,410（Wikipedia: List of river systems by leng） | 26.6% | FLAGGED: Wikipedia list gives 2,410 km and Wikidata 3,100 km. Britannica calls it the most winding river in the Amazon basin — its length depends strongly on ho |
| 26 | Brahmaputra | 2,900 | 3,969（Wikipedia: List of river systems by leng） | 36.9% | Yarlung Tsangpo in Tibet, Siang/Dihang and Brahmaputra in India, Jamuna in Bangladesh, where it joins the Ganges (Padma). Wikipedia list 3,969 km counts on thro |
| 29 | Euphrates | 2,800 | 3,596（Wikipedia: List of river systems by leng） | 28.4% | Joins the Tigris at al-Qurnah, Iraq, to form the Shatt al-Arab. Wikipedia list counts Shatt al-Arab–Euphrates–Murat as 3,596 km. |
| 30 | Tocantins | 2,699 | 3,650（Wikipedia: List of river systems by leng） | 35.2% | Wikipedia list counts Tocantins–Araguaia as 3,650 km; Britannica gives the Tocantins course only. Reaches the Atlantic through the Pará estuary next to the Amaz |
| 34 | Zambezi | 2,574 | 3,540（Encyclopaedia Britannica: Zambezi River ） | 37.5% | OUTLIER EXCEPTION: Britannica's 3,540 km is 38% above other figures for the SAME source (bog near Kalene Hill, Zambia) and the same mouth, with no different hea |
| 41 | Salween | 2,400 | 3,060（Wikipedia: List of river systems by leng） | 27.5% | Nu Jiang in China, Thanlwin in Myanmar. FLAGGED: Wikipedia list 3,060 km, Wikidata 2,815 km (diff 15–22%). Kept Britannica. |
| 43 | Colorado | 2,330 | 2,945（Wikipedia: List of river systems by leng） | 26.4% | Carves the Grand Canyon. Mouth in Mexico. Britannica links a Nature article: 'why the Colorado River no longer reaches the sea' — diversions take nearly all its |
| 49 | Irrawaddy | 2,170 | 2,809（Wikipedia: List of river systems by leng） | 29.4% | Ayeyarwady. FLAGGED: Wikipedia list counts the N'Mai–Dulong headstream system as 2,809 km (29%). Kept Britannica. |

说明：长度差异多来自「到哪个源头」「河口划在哪」「用多大比例尺量弯道」（海岸线悖论）。本期为口径一致，**不逐条挑最大值**，统一用 Britannica（离群值例外见 §1）；若改用 Wikipedia 列表值，名次会明显变化（Brahmaputra、Tocantins、Euphrates、Salween、Irrawaddy 会上升）。

## 4. 前 50 名边界

- 第 50 名 Kasai 2,153 km（Britannica；Wikipedia 列表同值）。2026-11-04 QC：补收 Araguaia（Britannica 2,627 km，第 32 名）；Orinoco 按离群值规则改 2,140 km 后出榜（第 51）。QC 另核 Kolyma、Songhua、Orange、Xingu、Tarim、Columbia、Brazos 的 Britannica 值都在线下，无其他漏项。
- Orinoco：2,140 km — OUTLIER EXCEPTION (same rule as Zambezi): Britannica 'some 1,700 miles (2,740 km) from its source in the Guiana Highlands' is 28% above Wikidata 2,140 / Wikipedia list 2,101 for the same source; on 2,140 km it ranks #51, just below Kasai 2,153
- Kolyma：2,129 km — Britannica (Kolyma-River) — #52
- Orange：2,092 km — Britannica gives 'some 1,300 miles' (≈2,090 km) only; Wikipedia list 2,432 km, Wikidata 2,200 km
- Xingu：2,100 km — Britannica ≈1,300 mi (2,100 km)
- Brazos：2,060 km — Britannica
- Columbia：2,000 km — Britannica
- Songhua (Sungari)：1,925 km — Britannica Sungari ≈1,925 km (QC 2026-11-04) — below the cut; Wikipedia list 2,309 counts the Nen as headstream
- Pearl–Xi：2,214 km — NOT LISTED (rule): Britannica gives no total length. The national-agency exception is used only where Britannica gives the segment lengths but no system total (Murray–Darling: Murray 2,530 + Darling 2,739 → Geoscience Australia 3,672). Pearl does not meet it. On the Pearl River Commission main-stem figure (~2,214 km) it would rank ~#47
- Red River (US)：2,188 km — NOT LISTED: the Britannica article gives no length (checked); Wikipedia list 2,188 km; lower course partly diverted to the Atchafalaya
- Saint Lawrence–Great Lakes：3,058 km — NOT LISTED: system length through the Great Lakes appears only in the Wikipedia list / Atlas of Canada (not verified); Britannica gives only the river below Lake Ontario (~1,200 km)
- Tocantins–Araguaia system：3,650 km — Wikipedia-only system figure; Britannica Tocantins 2,699 used

## 5. 洞察卡核对

- after 44：Next: the Colorado. Dams and farms now take so much water it rarely reaches the sea.  
  依据：Britannica Colorado 条目外链 Nature 文章「New water accounting reveals why the Colorado River no longer reaches the sea」；只在少数年份（如 2014 脉冲放水）入海——用 rarely。
- after 38：Next: the Ganges. It meets the Brahmaputra in Bangladesh and they share one huge delta.  
  依据：Britannica Ganges：『ends in the Ganges, or Ganges-Brahmaputra, delta』；Brahmaputra 条目：在孟加拉 Goalundo Ghat 以北与 Ganges 汇合。
- after 28：Next: the Danube. It flows through 10 countries on its way to the Black Sea.  
  依据：Britannica Danube：『Along its course it passes through 10 countries: Germany, Austria, Slovakia, Hungary, Croatia, Serbia, Bulgaria, Romania, Moldova, and Ukraine』。
- after 20：The next 3 rivers are only tributaries of the Amazon, yet each is longer than the Danube.  
  依据：#19 Purus 3,211、#18 Juruá 3,283、#17 Madeira 3,352 均为 Amazon 支流（Britannica），都大于 Danube 2,850。
- after 13：Britannica gives the Mekong 4,350 km. A 2009 satellite survey measured 4,909 km.  
  依据：Britannica Mekong 4,350；Liu et al. 2009（Int. J. Digital Earth 2(1):80–87, Table 1）Mekong 4,909 km。
- after 2：In 2008 Brazil's INPE measured the Amazon at 6,992 km. Is the Nile really No. 1?  
  依据：INPE 2008：Amazon 6,992 km、比 Nile 长约 140 km（FAPESP 2008-07 报道；Britannica「How long is the Amazon River?」亦引 6,992 / Nile 6,853，并说明河口划在 Marajó 岛南侧有争议）。

## 6. 逐条出处

| # | 河 | 国旗 | 大洲 | 主值 | 出处（原文） | 交叉核对 | notes |
|---|---|---|---|---|---|---|---|
| 1 | Nile | Ends in Egypt | Africa | 6,650 km | [Encyclopaedia Britannica: Nile River](https://www.britannica.com/place/Nile-River)：“a length of about 4,132 miles (6,650 kilometres)” | WP 列表 6,650（0.0%）；Liu 2009 7,088（6.6%） | Britannica lists the Nile as the longest river. Liu et al. 2009 (satellite + field survey) measured 7,088 km. Brazil's INPE (2008) measured 6,853 km while putting the Amazon at 6,992 km. Basin countries per Britannica: Egypt, Sudan, South Sudan, Eritrea, Ethiopia, Kenya, DR Congo, Burundi, Rwanda, Uganda, Tanzania. |
| 2 | Amazon | Ends in Brazil | South America | 6,400 km | [Encyclopaedia Britannica: Amazon River](https://www.britannica.com/place/Amazon-River)：“at least 4,000 miles (6,400 km) long” | WP 列表 6,400（0.0%）；Liu 2009 6,575（2.7%） | Britannica: 'at least 6,400 km', measured from the Ucayali–Apurímac headwaters; length 'open to interpretation'. INPE (Brazil, 2008) gave 6,992 km by placing the mouth south of Marajó Island (Pará estuary); Liu et al. 2009 gave 6,575 km. Britannica says the Amazon carries about one-fifth of all surface runoff on Earth. |
| 3 | Yangtze | Ends in China | Asia | 6,300 km | [Encyclopaedia Britannica: Yangtze River](https://www.britannica.com/place/Yangtze-River)：“with a length of 3,915 miles (6,300 km)” | WP 列表 6,300（0.0%）；Liu 2009 6,236（1.0%） | Longest river in Asia and in a single country. Liu et al. 2009: 6,236 km; Wikipedia list gives 6,300 (6,418 alternative). |
| 4 | Mississippi–Missouri | Ends in United States | North America | 5,971 km | [Encyclopaedia Britannica: Mississippi River](https://www.britannica.com/place/Mississippi-River)：“combined length of 3,710 miles (5,971 km)” | WP 列表 6,275（5.1%）；Liu 2009 6,084（1.9%） | System length measured from the Missouri–Jefferson–Red Rock headwaters (Britannica). The Mississippi alone is 3,766 km; the Missouri alone 3,726 km. Wikipedia list gives 6,275 km to Hell Roaring Creek; Liu et al. 2009: 6,084 km (diff 4.8% / 1.9%). |
| 5 | Yenisey–Angara–Selenga | Ends in Russia | Asia | 5,539 km | [Encyclopaedia Britannica: Yenisey River](https://www.britannica.com/place/Yenisey-River)：“With the inclusion of the Selenga, the Yenisey is 3,442 miles (5,539 km) long” | WP 列表 5,539（0.0%）；Liu 2009 5,816（5.0%） | System through Lake Baikal: Selenga (Mongolia) → Baikal → Angara → Yenisey. Yenisey proper 3,487 km. Britannica's world table rounds to 5,540. Liu et al. 2009: 5,816 km. |
| 6 | Yellow River | Ends in China | Asia | 5,464 km | [Encyclopaedia Britannica: Yellow River (Huang He)](https://www.britannica.com/place/Huang-He)：“with a length of 3,395 miles (5,464 kilometres)” | WP 列表 5,464（0.0%）；Liu 2009 5,778（5.7%） | Huang He. 5,464 km is also China's official figure. Liu et al. 2009: 5,778 km (5.7% longer). |
| 7 | Ob–Irtysh | Ends in Russia | Asia | 5,410 km | [Encyclopaedia Britannica: Ob River](https://www.britannica.com/place/Ob-River)：“the maximum length, from the source of the Black (Chorny) Irtysh ... is 3,362 miles (5,410 km)” | WP 列表 5,410（0.0%）；Liu 2009 5,525（2.1%） | Irtysh (4,248 km) is longer than the Ob proper (3,650 km), so the system is counted from the Black Irtysh source in China. Liu et al. 2009: 5,525 km. |
| 8 | Paraná | Ends in Argentina | South America | 4,880 km | [Encyclopaedia Britannica: Paraná River](https://www.britannica.com/place/Parana-River)：“after a course of 3,032 miles (4,880 km), it joins the Uruguay River” | WP 列表 4,880（0.0%） | Ends in the Paraná Delta (Argentina), where it joins the Uruguay River to form the Río de la Plata. |
| 9 | Congo | Ends in DR Congo | Africa | 4,700 km | [Encyclopaedia Britannica: Congo River](https://www.britannica.com/place/Congo-River)：“With a length of 2,900 miles (4,700 km)” | WP 列表 4,700（0.0%）；Liu 2009 5,118（8.9%） | Mouth lies on the DR Congo–Angola border; flag = DR Congo (larger share of the basin of the two). Liu et al. 2009: 5,118 km (8.9% longer). |
| 10 | Amur–Argun | Ends in Russia | Asia | 4,444 km | [Encyclopaedia Britannica: World's longest rivers (table)](https://www.britannica.com/topic/worlds-longest-rivers-2225894)：“10 Amur–Argun 4,444 2,761” | WP 列表 4,444（0.0%）；Liu 2009 5,498（23.7%） | Amur proper (from the Shilka–Argun confluence) is 2,824 km (Britannica article); system with the Argun 4,444 km (Britannica table). For ~1,600 km the Amur forms the Russia–China border. Liu et al. 2009: 5,498 km (23.7% longer — measured from a different headstream east of Mongolia). |
| 11 | Lena | Ends in Russia | Asia | 4,400 km | [Encyclopaedia Britannica: Lena River](https://www.britannica.com/place/Lena-River)：“It flows 2,734 miles (4,400 km)” | WP 列表 4,400（0.0%） | Wikipedia list 4,400; Wikidata 4,294 (Russian State Water Register main-stem figure). |
| 12 | Mekong | Ends in Vietnam | Asia | 4,350 km | [Encyclopaedia Britannica: Mekong River](https://www.britannica.com/place/Mekong-River)：“It has a length of about 2,700 miles (4,350 km)” | WP 列表 4,350（0.0%）；Liu 2009 4,909（12.9%） | Flows through China, Myanmar, Laos, Thailand, Cambodia and Vietnam (Britannica). Liu et al. 2009 measured 4,909 km (12.8% longer); MRC/FAO materials use about 4,800 km. Kept Britannica for consistency; >10% difference flagged for review. |
| 13 | Mackenzie–Peace–Finlay | Ends in Canada | North America | 4,241 km | [Encyclopaedia Britannica: Mackenzie River](https://www.britannica.com/place/Mackenzie-River)：“the entire river system runs for 2,635 miles (4,241 km)” | WP 列表 4,241（0.0%） | Mackenzie proper (from Great Slave Lake) is 1,650 km; system from the Finlay headwaters 4,241 km (same figure in the Atlas of Canada as cited by Wikipedia). |
| 14 | Niger | Ends in Nigeria | Africa | 4,200 km | [Encyclopaedia Britannica: Niger River](https://www.britannica.com/place/Niger-River)：“With a length of 2,600 miles (4,200 km)” | WP 列表 4,200（0.0%） | Rises 240 km from the Atlantic in Guinea but flows inland first, through Mali and Niger, before reaching the sea in Nigeria. |
| 15 | Murray–Darling | Ends in Australia | Oceania | 3,672 km | [Geoscience Australia: Longest Rivers](https://www.ga.gov.au/scientific-topics/national-location-information/landforms/longest-rivers)：“Murray-Darling: 3672 km, from its headwaters in Queensland down to the River Murray mouth near Goolwa” | WP 列表 3,672（0.0%） | System = Condamine/Balonne/Culgoa (1,195 km) + Darling below the Culgoa (1,545 km) + Murray below the Darling (828 km). Britannica gives the Murray alone 2,530 km and the Darling 2,739 km but no system figure; Geoscience Australia is used here. |
| 16 | Volga | Ends in Russia | Europe | 3,530 km | [Encyclopaedia Britannica: Volga River](https://www.britannica.com/place/Volga-River)：“the Volga discharges into the Caspian Sea, some 2,193 miles (3,530 kilometres) to the south” | WP 列表 3,645（3.3%） | Longest river in Europe. Wikipedia list 3,645 km (3.3%). |
| 17 | Madeira–Mamoré | Ends in Brazil | South America | 3,352 km | [Encyclopaedia Britannica: Madeira River](https://www.britannica.com/place/Madeira-River)：“The Madeira is 2,082 miles (3,352 km) long from the upper reaches of the Mamoré” | WP 列表 3,380（0.8%） | Largest tributary of the Amazon by volume. Wikipedia list 3,380 km. |
| 18 | Juruá | Ends in Brazil | South America | 3,283 km | [Encyclopaedia Britannica: Juruá River](https://www.britannica.com/place/Jurua-River)：“the Juruá is calculated to exceed 2,040 miles (3,283 km) in length” | WP 列表 2,410（26.6%） | FLAGGED: Wikipedia list gives 2,410 km and Wikidata 3,100 km. Britannica calls it the most winding river in the Amazon basin — its length depends strongly on how meanders are measured. |
| 19 | Purus | Ends in Brazil | South America | 3,211 km | [Encyclopaedia Britannica: Purus River](https://www.britannica.com/place/Purus-River)：“Most of its 1,995-mile (3,211-km) course is navigable” | WP 列表 3,211（0.0%） | Wikipedia list 3,211 km (same); Wikidata 2,960 km. |
| 20 | Indus | Ends in Pakistan | Asia | 3,200 km | [Encyclopaedia Britannica: Indus River](https://www.britannica.com/place/Indus-River)：“with a length of some 2,000 miles (3,200 km)” | WP 列表 3,180（0.6%） | Rises in Tibet (China), crosses India-administered Ladakh, flows the length of Pakistan. Wikipedia list 3,180 km. |
| 21 | Yukon | Ends in United States | North America | 3,190 km | [Encyclopaedia Britannica: Yukon River](https://www.britannica.com/place/Yukon-River)：“It measures 1,980 miles (3,190 km) from the headwaters” | WP 列表 3,185（0.2%） | Rises in British Columbia, crosses Yukon (Canada) and Alaska. Wikipedia list 3,185 km. |
| 22 | Rio Grande | Ends in United States | North America | 3,060 km | [Encyclopaedia Britannica: Rio Grande](https://www.britannica.com/place/Rio-Grande-river-United-States-Mexico)：“The total length of the river is about 1,900 miles (3,060 km)” | WP 列表 3,057（0.1%） | Forms about 2,000 km of the US–Mexico border; the mouth is on the border. Flag = United States (larger share of the basin of the two). Called Río Bravo in Mexico. |
| 23 | Syr Darya–Naryn | Ends in Kazakhstan | Asia | 3,019 km | [Encyclopaedia Britannica: Syr Darya](https://www.britannica.com/place/Syr-Darya)：“1,374 miles (2,212 km)—1,876 miles (3,019 km) including the Naryn” | WP 列表 3,078（2.0%） | Longest river in Central Asia. Irrigation diversions shrank its flow and contributed to the Aral Sea's collapse (Britannica). Wikipedia list 3,078 km. |
| 24 | Lower Tunguska | Ends in Russia | Asia | 2,989 km | [Encyclopaedia Britannica: Nizhnyaya Tunguska River](https://www.britannica.com/place/Nizhnyaya-Tunguska-River)：“Its length is 1,857 miles (2,989 km)” | WP 列表 2,989（0.0%） | Nizhnyaya Tunguska. Wikipedia list 2,989 km (same). |
| 25 | São Francisco | Ends in Brazil | South America | 2,914 km | [Encyclopaedia Britannica: São Francisco River](https://www.britannica.com/place/Sao-Francisco-River)：“With a length of 1,811 miles (2,914 kilometres)” | WP 列表 3,180（9.1%） | Largest river wholly within Brazil (Britannica). Wikipedia list 3,180 km (alt. 2,900). |
| 26 | Brahmaputra | Ends in Bangladesh | Asia | 2,900 km | [Encyclopaedia Britannica: Brahmaputra River](https://www.britannica.com/place/Brahmaputra-River)：“It flows some 1,800 miles (2,900 km) from its source” | WP 列表 3,969（36.9%） | Yarlung Tsangpo in Tibet, Siang/Dihang and Brahmaputra in India, Jamuna in Bangladesh, where it joins the Ganges (Padma). Wikipedia list 3,969 km counts on through the Padma–Meghna to the sea. |
| 27 | Danube | Ends in Romania | Europe | 2,850 km | [Encyclopaedia Britannica: Danube River](https://www.britannica.com/place/Danube-River)：“flows for some 1,770 miles (2,850 km) to its mouth on the Black Sea. Along its course it passes through 10 countries” | WP 列表 2,888（1.3%） | Passes through Germany, Austria, Slovakia, Hungary, Croatia, Serbia, Bulgaria, Romania, Moldova and Ukraine (Britannica). Delta mostly in Romania (Kilia branch on the Ukraine border). ICPDR: basin shared by 19 countries. Wikipedia list 2,888 km. |
| 28 | Japurá–Caquetá | Ends in Brazil | South America | 2,820 km | [Encyclopaedia Britannica: Japurá River](https://www.britannica.com/place/Japura-River)：“Its total length, including the Caquetá, is about 1,750 miles (2,820 km)” | WP 列表 2,615（7.3%） | Called Caquetá in Colombia. Wikipedia list 2,615 km (7.8%). |
| 29 | Euphrates | Ends in Iraq | Asia | 2,800 km | [Encyclopaedia Britannica: Euphrates River](https://www.britannica.com/place/Euphrates-River)：“it is 1,740 miles (2,800 km) long” | WP 列表 3,596（28.4%） | Joins the Tigris at al-Qurnah, Iraq, to form the Shatt al-Arab. Wikipedia list counts Shatt al-Arab–Euphrates–Murat as 3,596 km. |
| 30 | Tocantins | Ends in Brazil | South America | 2,699 km | [Encyclopaedia Britannica: Tocantins River](https://www.britannica.com/place/Tocantins-River)：“its 1,677-mile (2,699-kilometre) course” | WP 列表 3,650（35.2%） | Wikipedia list counts Tocantins–Araguaia as 3,650 km; Britannica gives the Tocantins course only. Reaches the Atlantic through the Pará estuary next to the Amazon mouth. |
| 31 | Vilyuy | Ends in Russia | Asia | 2,650 km | [Encyclopaedia Britannica: Vilyuy River](https://www.britannica.com/place/Vilyuy-River)：“it has a length of 1,647 miles (2,650 km)” | WP 列表 2,720（2.6%） | Longest tributary of the Lena. Wikipedia list 2,720 km. |
| 32 | Araguaia | Ends in Brazil | South America | 2,627 km | [Encyclopaedia Britannica: Araguaia River](https://www.britannica.com/place/Araguaia-River)：“flows north-northeast for 1,632 miles (2,627 km) to its junction with the Tocantins (Britannica print article 31943, via QC WebSearch)” | Wikipedia 'Araguaia River' infobox 2,627（0.0%） | Added after QC 2026-11-04 (B1): a major tributary not on Britannica's Tocantins 2,699 km main line, so it is listed like Vilyuy or Paraguay. Rises near Alto Araguaia (Mato Grosso), joins the Tocantins at São João do Araguaia; flows past Bananal, the world's largest river island. Not in the Wikipedia list as a separate row (counted there inside 'Tocantins–Araguaia' 3,650 km). |
| 33 | Nelson–Saskatchewan | Ends in Canada | North America | 2,575 km | [Encyclopaedia Britannica: Nelson River](https://www.britannica.com/place/Nelson-River)：“Together with the Bow and North and South Saskatchewan rivers, it forms a ... 1,600-mile (2,575-km) waterway” | WP 列表 2,570（0.2%） | System Bow → South Saskatchewan → Saskatchewan → Lake Winnipeg → Nelson. Wikipedia list 2,570 km. |
| 34 | Zambezi | Ends in Mozambique | Africa | 2,574 km | [Zambezi length 2,574 km (Wikipedia 'Zambezi' / Wikidata; same Kalene Hill source and Indian Ocean mouth as Britannica)](https://en.wikipedia.org/wiki/Zambezi)：“Length 2,574 km (1,599 mi); Britannica gives 'about 2,200 miles (3,540 kilometres)' from the same source” | WP 列表 2,740（6.4%）；Encyclopaedia Britannica 3,540（37.5%） | OUTLIER EXCEPTION: Britannica's 3,540 km is 38% above other figures for the SAME source (bog near Kalene Hill, Zambia) and the same mouth, with no different headstream to explain it (QC 2026-11-04 M1). Rule: when Britannica differs by >25% from other authoritative figures for the same source and mouth with no definitional explanation, use the consensus figure and note Britannica's. 2,574 km = Wikipedia article / Wikidata (Wikipedia list 2,740; Zambia Tourism ~2,700). Britannica: 'crosses or forms the boundaries of six countries'. Home of Victoria Falls. |
| 35 | Paraguay | Ends in Paraguay | South America | 2,550 km | [Encyclopaedia Britannica: Paraguay River](https://www.britannica.com/place/Paraguay-River)：“It is 1,584 miles (2,550 km) long” | WP 列表 2,549（0.0%） | Joins the Paraná on the Paraguay–Argentina border; flag = Paraguay (agent default: larger share of this river's basin of the two border countries — not separately verified). Flows through the Pantanal. |
| 36 | Amu Darya | Ends in Uzbekistan | Asia | 2,540 km | [Encyclopaedia Britannica: Amu Darya](https://www.britannica.com/place/Amu-Darya)：“1,578 miles (2,540 km), measured from the remotest source of the Panj (Britannica summary)” | WP 列表 2,620（3.1%） | Measured from the Panj headwaters. Archived Britannica article body was not captured; value from Britannica summary page via search snippet. Wikipedia list 2,620 km. |
| 37 | Ganges | Ends in Bangladesh | Asia | 2,510 km | [Encyclopaedia Britannica: Ganges River](https://www.britannica.com/place/Ganges-River)：“The Ganges River, which is 1,560 miles (2,510 km) long” | WP 列表 2,704（7.7%） | Ends in the Ganges–Brahmaputra delta; the main channel reaches the sea in Bangladesh as the Padma/Meghna (the Hooghly distributary runs through India). Flag by mouth rule = Bangladesh; most of the course and basin is in India. Wikipedia list 2,704 km. |
| 38 | Pilcomayo | Ends in Paraguay | South America | 2,500 km | [Encyclopaedia Britannica: Pilcomayo River](https://www.britannica.com/place/Pilcomayo-River-South-America)：“course of 1,550 miles (2,500 km) (Britannica, via search snippet)” | WP 列表 2,500（0.0%） | Forms part of the Argentina–Paraguay border and joins the Paraguay River opposite Asunción; flag = Paraguay (agent default for a border mouth). Its lower course often dries into marshes. Wikipedia list 2,500 km (same). |
| 39 | Ishim | Ends in Russia | Asia | 2,450 km | [Encyclopaedia Britannica: Ishim River](https://www.britannica.com/place/Ishim-River)：“Its total length is 1,522 miles (2,450 km)” | WP 列表 2,450（0.0%） | Rises in Kazakhstan (flows through Astana), joins the Irtysh at Ust-Ishim, Russia. Wikipedia list 2,450 km (same). |
| 40 | Ural | Ends in Kazakhstan | Europe | 2,428 km | [Encyclopaedia Britannica: Ural River](https://www.britannica.com/place/Ural-River)：“The Ural is 1,509 miles (2,428 km) long” | WP 列表 2,428（0.0%） | Traditionally part of the Europe–Asia boundary; the mouth at Atyrau straddles both. Counted as Europe (as in the Wikipedia list colouring). Wikipedia list 2,428 km (same). |
| 41 | Salween | Ends in Myanmar | Asia | 2,400 km | [Encyclopaedia Britannica: Salween River](https://www.britannica.com/place/Salween-River)：“the river flows generally south for about 1,500 miles (2,400 km)” | WP 列表 3,060（27.5%） | Nu Jiang in China, Thanlwin in Myanmar. FLAGGED: Wikipedia list 3,060 km, Wikidata 2,815 km (diff 15–22%). Kept Britannica. |
| 42 | Arkansas | Ends in United States | North America | 2,350 km | [Encyclopaedia Britannica: Arkansas River](https://www.britannica.com/place/Arkansas-River)：“flowing generally east-southeastward for 1,460 miles (2,350 km)” | WP 列表 2,348（0.1%） | Wikipedia list 2,348 km; Wikidata 2,364 km. |
| 43 | Colorado | Ends in Mexico | North America | 2,330 km | [Encyclopaedia Britannica: Colorado River](https://www.britannica.com/place/Colorado-River-United-States-Mexico)：“flowing generally west and south for 1,450 miles (2,330 kilometres) into the Gulf of California” | WP 列表 2,945（26.4%） | Carves the Grand Canyon. Mouth in Mexico. Britannica links a Nature article: 'why the Colorado River no longer reaches the sea' — diversions take nearly all its water. Wikipedia list counts Colorado–Green as 2,945 km. |
| 44 | Olenyok | Ends in Russia | Asia | 2,292 km | [Encyclopaedia Britannica: Olenyok River](https://www.britannica.com/place/Olenyok-River)：“total length of 1,424 miles (2,292 km) (Britannica, via search snippet)” | WP 列表 2,292（0.0%） | Wikipedia list 2,292 km (same); Wikidata 2,270 km. |
| 45 | Aldan | Ends in Russia | Asia | 2,273 km | [Encyclopaedia Britannica: Aldan River](https://www.britannica.com/place/Aldan-River)：“The Aldan River is 1,412 miles (2,273 km) long” | WP 列表 2,273（0.0%） | Wikipedia list 2,273 km (same). |
| 46 | Rio Negro | Ends in Brazil | South America | 2,250 km | [Encyclopaedia Britannica: Negro River](https://www.britannica.com/place/Negro-River-South-America)：“Its length is about 1,400 miles (2,250 km)” | WP 列表 2,250（0.0%） | Black-water river; meets the muddy Solimões at Manaus ('Meeting of Waters'). Wikipedia list 2,250 km (same). |
| 46 | Ubangi–Uele | Ends in DR Congo | Africa | 2,250 km | [Encyclopaedia Britannica: Ubangi River](https://www.britannica.com/place/Ubangi-River)：“The total length of the Ubangi, with the Uele, is approximately 1,400 miles (2,250 km)” | WP 列表 2,270（0.9%） | Forms the DR Congo–Central African Republic and DR Congo–Republic of the Congo borders; joins the Congo on the DR Congo–Republic of the Congo border. Flag = DR Congo (border-mouth rule). Wikipedia list 2,270 km. |
| 48 | Dnieper | Ends in Ukraine | Europe | 2,200 km | [Encyclopaedia Britannica: Dnieper River](https://www.britannica.com/place/Dnieper-River)：“It is 1,367 miles (2,200 km) in length” | WP 列表 2,287（4.0%） | Rises in Russia's Valdai Hills, crosses Belarus and Ukraine (flows through Kyiv). Wikipedia list 2,287 km; Wikidata 2,285 km. |
| 49 | Irrawaddy | Ends in Myanmar | Asia | 2,170 km | [Encyclopaedia Britannica: Irrawaddy River](https://www.britannica.com/place/Irrawaddy-River)：“it is about 1,350 miles (2,170 km) long” | WP 列表 2,809（29.4%） | Ayeyarwady. FLAGGED: Wikipedia list counts the N'Mai–Dulong headstream system as 2,809 km (29%). Kept Britannica. |
| 50 | Kasai | Ends in DR Congo | Africa | 2,153 km | [Encyclopaedia Britannica: Kasai River](https://www.britannica.com/place/Kasai-River)：“it measures 1,338 miles (2,153 km) from its source” | WP 列表 2,153（0.0%） | Rises in Angola, forms part of the Angola–DR Congo border, joins the Congo at Kwamouth, DR Congo. Wikipedia list 2,153 km (same). |

## 7. 图片许可账本摘要

| # | 河 | 文件 | 作者 | 许可 | 来源页 | 风险 / 替代 |
|---|---|---|---|---|---|---|
| 1 | Nile | assets/img/01_nile.jpg | Eszter Kisgyura | Unsplash License | https://unsplash.com/photos/7ObNCbySGGc |  |
| 2 | Amazon | assets/img/02_amazon.jpg | Nando Freitas | Pexels License | https://www.pexels.com/photo/aerial-view-of-muddy-river-through-rainforest-17025853/ |  |
| 3 | Yangtze | assets/img/03_yangtze.jpg | Yux Xiang | Unsplash License | https://unsplash.com/photos/a-sunset-view-of-a-body-of-water-with-mountains-in-the-background-5VcLojayu_g |  |
| 4 | Mississippi–Missouri | assets/img/04_mississippi_missouri.jpg | Kenny Nguyễn | Unsplash License | https://unsplash.com/photos/YqBX_TIZh1U |  |
| 5 | Yenisey–Angara–Selenga | assets/img/05_yenisey.jpg | Kir Shu | Unsplash License | https://unsplash.com/photos/green-trees-on-mountain-beside-body-of-water-during-daytime-xQqUxfht4V4 |  |
| 6 | Yellow River | assets/img/06_yellow.jpg | 岩 孙 | Pexels License | https://www.pexels.com/photo/spectacular-view-of-hukou-waterfall-in-china-40325653/ |  |
| 7 | Ob–Irtysh | assets/img/07_ob_irtysh.jpg | WJ Y | Pexels License | https://www.pexels.com/photo/scenic-view-of-irtysh-river-and-colorful-hills-at-sunset-39623596/ |  |
| 8 | Paraná | assets/img/08_parana.jpg | Franco Garcia | Pexels License | https://www.pexels.com/photo/sunset-over-rosario-s-iconic-bridge-32050778/ |  |
| 9 | Congo | assets/img/09_congo.jpg | Valdhy Mbemba | Unsplash License | https://unsplash.com/photos/abandoned-shipwrecks-rest-in-shallow-water-under-a-blue-sky-ONwhjj4yR60 |  |
| 10 | Amur–Argun | assets/img/10_amur.jpg | bor1nic | All rights reserved | https://www.dronestagr.am/utes-on-the-embankment-of-the-amur-river/ | licence unknown；默认版用 assets/img/10_amur_alt.jpg（Ruslan Mingazhov / Unsplash License） |
| 11 | Lena | assets/img/11_lena.jpg | Artem Svetlov | CC BY 2.0 | https://www.flickr.com/photos/trolleway/35052951020 |  |
| 12 | Mekong | assets/img/12_mekong.jpg | Leandro De Torres | Unsplash License | https://unsplash.com/photos/a-boat-travels-down-a-wide-muddy-river-with-mountains-uvmoQNj9o1Y |  |
| 13 | Mackenzie–Peace–Finlay | assets/img/13_mackenzie.jpg | Kabit Bhattarai | Pexels License | https://www.pexels.com/photo/forest-near-river-in-autumn-9677854/ |  |
| 14 | Niger | assets/img/14_niger.jpg | Fatih Turan | Pexels License | https://www.pexels.com/photo/view-of-a-riverbank-17676147/ |  |
| 15 | Murray–Darling | assets/img/15_murray_darling.jpg | unknown | unknown | https://www.big4.com.au/caravan-parks/sa/riverland/renmark-riverfront-holiday-park/whats-local/murray-river-trails-5f35dad905353201342d48c6 | licence unknown；默认版用 assets/img/15_murray_darling_alt.jpg（Zac Edmonds / Unsplash License） |
| 16 | Volga | assets/img/17_volga.jpg | Alexey | Unsplash License | https://unsplash.com/photos/a-river-with-a-mountain-in-the-background-cMMLy-ELR3o |  |
| 17 | Madeira–Mamoré | assets/img/18_madeira.jpg | Leandro Morais / Defesa Civil Municipal | Todos os direitos reservados. | https://www.portovelho.ro.gov.br/noticias/estiagem-defesa-civil-explica-mudanca-climatica-que-provocou-a-seca-historica-do-rio-madeira-e-orienta-populacao | licence unknown；默认版用 assets/img/18_madeira_alt.jpg（AI-generated / AI-generated (Codex image_gen)） |
| 18 | Juruá | assets/img/19_jurua.jpg | Bruno Bimbato / ICMBio | unknown | https://mcm.redelivre.org.br/2018/10/30/medio-jurua-recebe-seminario-de-cadeias-produtivas/ | licence unknown；默认版用 assets/img/19_jurua_alt.jpg（Marinha do Brasil (Oficial) / CC BY-SA 2.0） |
| 19 | Purus | assets/img/20_purus.jpg | AI-generated | AI-generated (Codex image_gen) |  |  |
| 20 | Indus | assets/img/21_indus.jpg | Danish Rasool | Unsplash License | https://unsplash.com/photos/a-large-body-of-water-with-a-bridge-in-the-background-BfKHN4uIUx8 |  |
| 21 | Yukon | assets/img/22_yukon.jpg | Quentin Krattiger | Pexels License | https://www.pexels.com/photo/stunning-aerial-view-of-dawson-city-and-yukon-river-33646746/ |  |
| 22 | Rio Grande | assets/img/23_rio_grande.jpg | Kyle Glenn | Unsplash License | https://unsplash.com/photos/river-between-rocky-mountains-under-clear-sky-va80jk-OY2w |  |
| 23 | Syr Darya–Naryn | assets/img/24_syr_darya.jpg | Azamat E | Unsplash License | https://unsplash.com/photos/brown-rocky-mountain-beside-blue-lake-under-blue-sky-during-daytime-F8RPA3u1_n8 |  |
| 24 | Lower Tunguska | assets/img/25_lower_tunguska.jpg | AI-generated | AI-generated (Codex image_gen) |  |  |
| 25 | São Francisco | assets/img/26_sao_francisco.jpg | Italo Delani Lopez | Pexels License | https://www.pexels.com/photo/scenic-view-of-sao-francisco-river-cliffs-in-brazil-37993631/ |  |
| 26 | Brahmaputra | assets/img/27_brahmaputra.jpg | Mohit Gupta | Pexels License | https://www.pexels.com/photo/scenic-view-of-brahmaputra-river-and-bridge-36868420/ |  |
| 27 | Danube | assets/img/28_danube.jpg | Krisztian Tabori | Unsplash License | https://unsplash.com/photos/budapest-cityscape-with-danube-river-chain-bridge-and-parliament-building-zC2nZDiv7YI |  |
| 28 | Japurá–Caquetá | assets/img/29_japura.jpg | unknown | unknown | https://www.redcaquetapaz.org/llegamos-hasta-el-araracuara-con-el-sistema-local-de-justicia-de-solano/ | licence unknown；默认版用 assets/img/29_japura_alt.jpg（AI-generated / AI-generated (Codex image_gen)） |
| 29 | Euphrates | assets/img/30_euphrates.jpg | Adem Albayrak | Pexels License | https://www.pexels.com/photo/scenic-view-of-halfeti-village-by-the-euphrates-river-39965136/ |  |
| 30 | Tocantins | assets/img/32_tocantins.jpg | Anderson Mathias | Unsplash License | https://unsplash.com/photos/the-sun-is-setting-over-a-long-bridge-8xrM2ZwZYMc |  |
| 31 | Vilyuy | assets/img/33_vilyuy.jpg | Саргы Тупсарт | unknown | https://supersnimki.ru/ru/photo/17/63007280e2cfda6c916855e2 | licence unknown；默认版用 assets/img/33_vilyuy_alt.jpg（AI-generated / AI-generated (Codex image_gen)） |
| 32 | Araguaia | assets/img/32_araguaia.jpg | Augusto Miranda / MTur | Public domain | https://www.flickr.com/photos/mturdestinos/26088774777 |  |
| 33 | Nelson–Saskatchewan | assets/img/34_nelson.jpg | Maryam Samadi | Pexels License | https://www.pexels.com/photo/trees-by-the-lake-during-autumn-9991328/ |  |
| 34 | Zambezi | assets/img/16_zambezi.jpg | Ed Wingate | Unsplash License | https://unsplash.com/photos/majestic-waterfall-cascading-into-a-rocky-gorge-at-sunset-ZqggK6JPRiI |  |
| 35 | Paraguay | assets/img/35_paraguay.jpg | unknown | Todos os direitos reservados | https://corumba.ms.gov.br/noticias/com-planejamento-e-investimento-publico-corumba-se-consolida-entre-destinos-turisticos-do-centro-oeste | licence unknown；默认版用 assets/img/35_paraguay_alt.jpg（aranha / Pixabay Content License） |
| 36 | Amu Darya | assets/img/36_amu_darya.jpg | Dragon_XXC | Pixabay Content License | https://pixabay.com/photos/tajikistan-panj-river-mountains-9883725/ |  |
| 37 | Ganges | assets/img/37_ganges.jpg | Arto Suraj | Pexels License | https://www.pexels.com/photo/peaceful-boating-scene-on-the-ganges-at-sunrise-34741296/ |  |
| 38 | Pilcomayo | assets/img/38_pilcomayo.jpg | unknown | Todos los derechos reservados. | https://gotadelchaco.com/villamontes/atractivos/angosto-del-pilcomayo | licence unknown；默认版用 assets/img/38_pilcomayo_alt.jpg（Dan Lundberg / CC BY-SA 2.0） |
| 39 | Ishim | assets/img/39_ishim.jpg | forzaalisherka | Unsplash License | https://unsplash.com/photos/a-body-of-water-with-buildings-in-the-background-q1TyvuxEw0U |  |
| 40 | Ural | assets/img/40_ural.jpg | unknown | Все права защищены | https://historical-baggage.ru/post/belyy-most-evropa-%E2%80%94-aziya-cherez-ural-1623 | licence unknown；默认版用 assets/img/40_ural_alt.jpg（Aibek Skakov / Pexels License） |
| 41 | Salween | assets/img/41_salween.jpg | jason hu | Pexels License | https://www.pexels.com/photo/forest-on-hills-around-river-in-valley-26746835/ |  |
| 42 | Arkansas | assets/img/42_arkansas.jpg | Alessandra Esquivel | Unsplash License | https://unsplash.com/photos/a-view-of-a-river-running-through-a-canyon-mPgNVtVK5oA |  |
| 43 | Colorado | assets/img/43_colorado.jpg | Francesco Ungaro | Unsplash License | https://unsplash.com/photos/horseshoe-bend-arizona-WJ1O3BX69mY |  |
| 44 | Olenyok | assets/img/44_olenyok.jpg | Sergey Karpukhin | unknown | https://photogeographic.ru/reka-olenyok | licence unknown；默认版用 assets/img/44_olenyok_alt.jpg（AI-generated / AI-generated (Codex image_gen)） |
| 45 | Aldan | assets/img/45_aldan.jpg | Ф. И. Белялов | unknown | https://therapy.irkutsk.ru/foto52i.htm | licence unknown；默认版用 assets/img/45_aldan_alt.jpg（James St. John / CC BY 2.0） |
| 46 | Rio Negro | assets/img/46_negro.jpg | Vinícius Bastos | Pexels License | https://www.pexels.com/photo/sunset-over-long-bridge-16552629/ |  |
| 46 | Ubangi–Uele | assets/img/46_ubangi.jpg | AI-generated | AI-generated (Codex image_gen) |  |  |
| 48 | Dnieper | assets/img/48_dnieper.jpg | Pavel Shakotko | Pexels License | https://www.pexels.com/photo/river-in-city-12993837/ |  |
| 49 | Irrawaddy | assets/img/49_irrawaddy.jpg | Kyaw Zin Thu | Unsplash License | https://unsplash.com/photos/a-boat-floating-on-top-of-a-large-body-of-water-DBzhiRh2Is0 |  |
| 50 | Kasai | assets/img/50_kasai.jpg | Matti Barthel / ETH Zurich | unknown | https://ethz.ch/en/news-and-events/eth-news/news/2026/02/peatland-lakes-in-the-congo-basin-release-carbon-that-is-thousands-of-years-old.html | licence unknown；默认版用 assets/img/50_kasai_alt.jpg（AI-generated / AI-generated (Codex image_gen)） |


- 默认母版：有 `image_risk` 的条目改用 `image_alt`（可商用照片或 AI 生成图）；`_with-risk-images` 版用 `image`。
- AI 生成图（Codex image_gen，经 `tools/codex_image.py`，请求日志在 `ai_videos/paihangbang/request_log.md`；prompt 在 `_build/gen/`）：不冒充任何真实照片，无人物、无品牌；上传时须勾选合成内容声明。
- 候选与逐项依据：`_build/reselect/cand/*/meta.json`、`_build/reselect/claude_*.json`、`codex_b*.json`；内容摘要 `_build/content/`。

其他素材：国旗 flagcdn（公有领域）；字体 Inter（SIL OFL）；图标 Tabler Icons（MIT）。
