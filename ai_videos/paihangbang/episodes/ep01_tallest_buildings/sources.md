# ep01 · 来源、交叉核对与许可记录

> 由 `_build/08_sources.py` 生成（2026-11-03）。改数据先改 `_build/` 里的输入再重跑，不手改本文件。
> 构建顺序：`01_parse_ctbuh.py` → `02_parse_wikipedia.py` → `03_wikidata.py` → `04_commons_candidates.py`（补充：`04b_category_candidates.py`）→ 目检 `09_contact_sheet.py` / `10_preview_candidates.py`，人工选择记在 `overrides.json` 与 `override_reasons.json` → `05_select_download.py . .. overrides.json` → `06_build_data.py` → `07_validate.py` → `08_sources.py`。原始抓取存在 `_build/raw/`，全部视为不可信数据，只解析不执行。

## 1. 数据来源与许可

| 用途 | 来源 | 抓取 | 许可 / 用法 |
|---|---|---|---|
| **主值**：名次、高度、层数、竣工年、城市、状态 | CTBUH Skyscraper Center「The 100 Tallest Completed Buildings in the World in 2026」 https://www.skyscrapercenter.com/buildings ；每座楼的 CTBUH 页面见下表 | 2026-11-03 | 只用事实并注明出处（描述框写明 CTBUH）。不搬运页面文字、版式和图片。**CTBUH 网站使用条款未逐条核对（待核）**：事实不受版权保护，但数据库条款可能有约束。 |
| 状态核实（不收的楼） | CTBUH 单楼页：International Land-Sea Center https://www.skyscrapercenter.com/building/chongqing-corporate-avenue-1/148 ；Greenland Shandong IFC https://www.skyscrapercenter.com/building/greenland-shandong-international-financial-center/30121 | 2026-11-03 | 同上 |
| 交叉核对：高度、层数、开业年、国家 | Wikidata（P2048 / P1101 / P1619 / P571 / P17 / P18），SPARQL 见 `_build/raw/wikidata_query.rq`，结果在 `wikidata_result.json` | 2026-11-03 | **CC0** |
| 交叉核对（Wikidata 缺高度时）、英文名、文章与图片线索 | Wikipedia「List of tallest buildings」https://en.wikipedia.org/wiki/List_of_tallest_buildings （API wikitext） | 2026-11-03 | 只取事实，不复制文字（CC BY-SA 正文不进视频）。它引用 CTBUH，**不是独立来源**。 |
| FoP 各国状态 | Commons:Freedom of panorama（含 /table 子页）及 Commons:Copyright rules by territory/{UAE, South Korea, Kuwait, Egypt, Vietnam} | 2026-11-03 | 参考信息 |

**统计口径**：CTBUH architectural height，含尖顶，不含天线；只收 CTBUH 状态为 Completed 的建筑，塔类构筑物（晴空塔、CN Tower）不算建筑。CTBUH 已建成榜单本身含 2024–2026 年竣工的楼（如 City Tower One，2026 年，第 74 名），说明它是最新的。

**是否最新（2026-11）**：
- 2024–2026 年进入 Top 50 的楼：JPMorganChase Tower（2025，第 33 名）、紫金金融大厦（2025，第 36 名）、宁波中心 T1（2025，第 41 名）、Iconic Tower（2024，第 44 名）、招商银行全球总部主塔（2025，第 45 名）。
- **不收**：International Land-Sea Center（重庆，458.2 m）和 Shandong IFC（济南，428 m）。CTBUH 状态都是 *Architecturally Topped Out*，山东 IFC 的 CTBUH 预计竣工年为 2026。Wikipedia 已把两座列为建成（第 18、30 名），这里按 CTBUH 口径不收。发布前复核，如果 CTBUH 改为 Completed，就重排名次并重渲染。
- **不收（未完工）**：Jeddah Tower、Burj Binghatti Jacob & Co、Marina 106、Tianfu Center（Panda Tower）、Cavalli Tower、Al Habtoor Tower 等，都不在 CTBUH 已建成前 100 名里。
- Wikipedia 和 CTBUH 按高度逐条比对（脚本输出见本次会话）：除上面两座外，其余 Top 50 一一对应。

**名次规则**：竞争排名，与 CTBUH 一致：第 8、20、22 名各有两座并列，所以没有第 9、21、23 名。同名次内按显示名字母序。

**显示值**：取整到米（3 位有效数字）。如果两座不同高度的楼取整后数字相同，就改显示 1 位小数，各条 notes 里注明。英尺取 CTBUH 公布的英尺值。

**名称**：默认用 CTBUH 名称。以下几座改用通行英文名：
- 大小写：TAIPEI 101 → Taipei 101，CITYMARK CENTRE → Citymark Centre；
- Menara Merdeka Maybank → **Merdeka 118**（通行名，官方名写在 notes；用户可改回）；
- CITIC Tower → CITIC Tower (China Zun)；
- Vincom Landmark 81 → Landmark 81；
- Petronas Twin Tower 1/2 → Petronas Tower 1/2；
- Wuhan Tower → Wuhan Center（Wikipedia 通行名）；
- One Vanderbilt Avenue → One Vanderbilt；
- China Merchants Bank Global Headquarters Main Tower → China Merchants Bank Global HQ（卡片长度）。

**国家口径**：取建筑所在地的主权国家。香港两座记为 `CN` China，副标题写 Hong Kong；Taipei 101 记为 `TW` Taiwan。Wikidata P17 与此全部一致：Wikidata 把香港记为 People's Republic of China，台北 101 记为 Taiwan。

**交叉核对规则**：
- 取 Wikidata P2048 中与 CTBUH 最接近的那条，英尺换算成米。同一条目常有多条高度，分别对应屋顶、尖顶、天线等口径，其余值写进 notes。
- Wikidata 没有高度的 4 座（紫金金融大厦、Two IFC、贵阳国际金融中心 T1、招商银行全球总部），改用 Wikipedia 列表核对，并标明它不是独立来源。
- 层数取 CTBUH 地上层数；竣工年取 CTBUH 竣工年。与 Wikidata 不一致的都写进 notes，以 CTBUH 为准。


## 2. 逐条来源与交叉核对

| # | 名称 | 城市 / 国家 | CTBUH 高度 (m) | 层数 / 年 | 主源 | 交叉核对 | 差异 % | 备注 |
|---|---|---|---|---|---|---|---|---|
| 1 | Burj Khalifa | Dubai, AE | 828 | 163 floors / Completed 2010 | [CTBUH](https://www.skyscrapercenter.com/building/burj-khalifa/3) | [Wikidata Q12495](https://www.wikidata.org/wiki/Q12495) 828 | 0.0 | Other Wikidata height statements (other height definitions): 584.5 m, 829.8 m. IMAGE: First-pass pick 'Burj dubai 3.11.08.jpg' is a 2008 aerial during construction (P18 and lead image carry {{NoFoP-UAE}} and were skipped). Chose 2024 sunset photo, CC BY 4.0, no NoFoP tag. Other untagged files are views FROM the tower (metro station, aerial) or construction-era; the sunset photo is kept but the tower is small/backlit -> composition flagged for human review. |
| 2 | Merdeka 118 | Kuala Lumpur, MY | 678.9 | 118 floors / Completed 2023 | [CTBUH](https://www.skyscrapercenter.com/building/menara-merdeka-maybank/10115) | [Wikidata Q7969454](https://www.wikidata.org/wiki/Q7969454) 678.9 | 0.0 | CTBUH name: Menara Merdeka Maybank. |
| 3 | Shanghai Tower | Shanghai, CN | 632 | 128 floors / Completed 2015 | [CTBUH](https://www.skyscrapercenter.com/building/shanghai-tower/56) | [Wikidata Q18547](https://www.wikidata.org/wiki/Q18547) 632 | 0.0 | Completion year: CTBUH 2015; Wikidata P1619 opening 2014 (CTBUH used). |
| 4 | Makkah Royal Clock Tower | Mecca, SA | 601 | 120 floors / Completed 2012 | [CTBUH](https://www.skyscrapercenter.com/building/makkah-royal-clock-tower/84) | [Wikidata Q189476](https://www.wikidata.org/wiki/Q189476) 607 | 1.0 | Wikidata 607 m (+1.0 %) is not referenced to CTBUH and likely uses a different height definition (e.g. to the finial tip); CTBUH architectural height 601 m used, Wikipedia list also 601 m. Completion year: CTBUH 2012; Wikidata P1619 opening 2011 (CTBUH used). |
| 5 | Ping An Finance Center | Shenzhen, CN | 599.05 | 115 floors / Completed 2017 | [CTBUH](https://www.skyscrapercenter.com/building/ping-an-finance-center/54) | [Wikidata Q1077308](https://www.wikidata.org/wiki/Q1077308) 599.05 | 0.0 |  |
| 6 | Lotte World Tower | Seoul, KR | 554.53 | 123 floors / Completed 2017 | [CTBUH](https://www.skyscrapercenter.com/building/lotte-world-tower/88) | [Wikidata Q494895](https://www.wikidata.org/wiki/Q494895) 554.5 | -0.01 | Other Wikidata height statements (other height definitions): 555.7 m. IMAGE: none (image=null) - Every unredacted candidate carries {{NoFoP-South Korea}}; the only untagged file is Commons' own redacted 'Lotte world tower (censored).jpg' (tower blacked out). Korea FoP is non-commercial only -> image=null. |
| 7 | One World Trade Center | New York City, US | 541.3 | 94 floors / Completed 2014 | [CTBUH](https://www.skyscrapercenter.com/building/one-world-trade-center/98) | [Wikidata Q11245](https://www.wikidata.org/wiki/Q11245) 541.3 | 0.0 | Other Wikidata height statements (other height definitions): 386.5 m, 546.2 m. |
| 8 | Guangzhou CTF Finance Centre | Guangzhou, CN | 530 | 111 floors / Completed 2016 | [CTBUH](https://www.skyscrapercenter.com/building/guangzhou-ctf-finance-centre/176) | [Wikidata Q168575](https://www.wikidata.org/wiki/Q168575) 530 | 0.0 |  |
| 8 | Tianjin CTF Finance Centre | Tianjin, CN | 530 | 97 floors / Completed 2019 | [CTBUH](https://www.skyscrapercenter.com/building/tianjin-ctf-finance-centre/310) | [Wikidata Q10939987](https://www.wikidata.org/wiki/Q10939987) 530 | 0.0 | Floors: CTBUH 97 above ground; Wikidata P1101 98 (CTBUH used). |
| 10 | CITIC Tower (China Zun) | Beijing, CN | 527.7 | 109 floors / Completed 2018 | [CTBUH](https://www.skyscrapercenter.com/building/citic-tower/11116) | [Wikidata Q197833](https://www.wikidata.org/wiki/Q197833) 528 | 0.06 | Floors: CTBUH 109 above ground; Wikidata P1101 108 (CTBUH used). CTBUH name: CITIC Tower. |
| 11 | Taipei 101 | Taipei, TW | 508 | 101 floors / Completed 2004 | [CTBUH](https://www.skyscrapercenter.com/building/taipei-101/117) | [Wikidata Q83101](https://www.wikidata.org/wiki/Q83101) 508 | 0.0 | Completion year: CTBUH 2004; Wikidata P1619 opening 2005 (CTBUH used). CTBUH name: TAIPEI 101. |
| 12 | Shanghai World Financial Center | Shanghai, CN | 492 | 101 floors / Completed 2008 | [CTBUH](https://www.skyscrapercenter.com/building/shanghai-world-financial-center/131) | [Wikidata Q80852](https://www.wikidata.org/wiki/Q80852) 492 | 0.0 | Other Wikidata height statements (other height definitions): 474 m, 494.3 m. |
| 13 | International Commerce Centre | Hong Kong, CN | 484 | 108 floors / Completed 2010 | [CTBUH](https://www.skyscrapercenter.com/building/international-commerce-centre/137) | [Wikidata Q317034](https://www.wikidata.org/wiki/Q317034) 484 | 0.0 | IMAGE: First-pass pick 'International Commerce Centre 200911.jpg' shows the tower during construction (crane on top). Replaced with completed-state overview. |
| 14 | Wuhan Greenland Center | Wuhan, CN | 475.6 | 101 floors / Completed 2023 | [CTBUH](https://www.skyscrapercenter.com/building/wuhan-greenland-center/33983) | [Wikidata Q143235](https://www.wikidata.org/wiki/Q143235) 475.6 | 0.0 | Floors: CTBUH 101 above ground; Wikidata P1101 97 (CTBUH used). |
| 15 | Central Park Tower | New York City, US | 472.44 | 98 floors / Completed 2020 | [CTBUH](https://www.skyscrapercenter.com/building/central-park-tower/14269) | [Wikidata Q2631701](https://www.wikidata.org/wiki/Q2631701) 472.4 | -0.01 | Other Wikidata height statements (other height definitions): 442 m. IMAGE: First-pass pick 'CentralParkTowerSep20.jpg' (2019) shows the tower under construction; 2025 files are tight partial close-ups. Chose 'Central Park Tower April 2021.jpg' (full completed tower). |
| 16 | Lakhta Center | St. Petersburg, RU | 462 | 87 floors / Completed 2019 | [CTBUH](https://www.skyscrapercenter.com/building/lakhta-center/12575) | [Wikidata Q4255374](https://www.wikidata.org/wiki/Q4255374) 462 | 0.0 | Completion year: CTBUH 2019; Wikidata P1619 opening 2022 (CTBUH used). |
| 17 | Landmark 81 | Ho Chi Minh City, VN | 461.2 | 81 floors / Completed 2018 | [CTBUH](https://www.skyscrapercenter.com/building/vincom-landmark-81/18192) | [Wikidata Q18640924](https://www.wikidata.org/wiki/Q18640924) 461.5 | 0.07 | CTBUH name: Vincom Landmark 81. |
| 18 | The Exchange 106 | Kuala Lumpur, MY | 453.62 | 95 floors / Completed 2019 | [CTBUH](https://www.skyscrapercenter.com/building/the-exchange-106/24971) | [Wikidata Q27670200](https://www.wikidata.org/wiki/Q27670200) 453.5 | -0.03 | Other Wikidata height statements (other height definitions): 392.3 m, 445.5 m. Wikidata preferred-rank value is 445.5 m. Floors: CTBUH 95 above ground; Wikidata P1101 106 (CTBUH used). |
| 19 | Changsha IFS Tower T1 | Changsha, CN | 452.07 | 94 floors / Completed 2018 | [CTBUH](https://www.skyscrapercenter.com/building/changsha-ifs-tower-t1/13144) | [Wikidata Q5410187](https://www.wikidata.org/wiki/Q5410187) 452.1 | 0.01 | Floors: CTBUH 94 above ground; Wikidata P1101 88 (CTBUH used). Shown with 1 decimal because another building rounds to the same whole metre. |
| 20 | Petronas Tower 1 | Kuala Lumpur, MY | 451.9 | 88 floors / Completed 1998 | [CTBUH](https://www.skyscrapercenter.com/building/petronas-twin-tower-1/149) | [Wikidata Q83063](https://www.wikidata.org/wiki/Q83063) 452.02 | 0.03 | Wikidata height stated as 1483 ft, converted. Completion year: CTBUH 1998; Wikidata P1619 opening 1999 (CTBUH used). CTBUH name: Petronas Twin Tower 1. Shown with 1 decimal because another building rounds to the same whole metre. |
| 20 | Petronas Tower 2 | Kuala Lumpur, MY | 451.9 | 88 floors / Completed 1998 | [CTBUH](https://www.skyscrapercenter.com/building/petronas-twin-tower-2/150) | [Wikidata Q83063](https://www.wikidata.org/wiki/Q83063) 452.02 | 0.03 | Wikidata height stated as 1483 ft, converted. Completion year: CTBUH 1998; Wikidata P1619 opening 1999 (CTBUH used). CTBUH name: Petronas Twin Tower 2. Shown with 1 decimal because another building rounds to the same whole metre. IMAGE: Avoid reusing the Tower 1 file; first remaining candidate was a tight close-up dominated by a flag. Chose full view of both towers from Jalan Semarak. |
| 22 | Suzhou IFS | Suzhou, CN | 450 | 95 floors / Completed 2019 | [CTBUH](https://www.skyscrapercenter.com/building/suzhou-ifs/196) | [Wikidata Q617082](https://www.wikidata.org/wiki/Q617082) 450 | 0.0 |  |
| 22 | Zifeng Tower | Nanjing, CN | 450 | 66 floors / Completed 2010 | [CTBUH](https://www.skyscrapercenter.com/building/zifeng-tower/165) | [Wikidata Q382121](https://www.wikidata.org/wiki/Q382121) 450 | 0.0 | Other Wikidata height statements (other height definitions): 316 m. |
| 24 | Wuhan Center | Wuhan, CN | 443.13 | 88 floors / Completed 2019 | [CTBUH](https://www.skyscrapercenter.com/building/wuhan-tower/8823) | [Wikidata Q2484373](https://www.wikidata.org/wiki/Q2484373) 438 | -1.16 | Wikidata 438 m (-1.2 %) matches the originally announced design height; CTBUH as-built architectural height 443.13 m used (Wikipedia list 443.1 m). CTBUH name: Wuhan Tower. |
| 25 | Willis Tower | Chicago, US | 442.14 | 108 floors / Completed 1974 | [CTBUH](https://www.skyscrapercenter.com/building/willis-tower/169) | [Wikidata Q29294](https://www.wikidata.org/wiki/Q29294) 442.1 | -0.01 | Completion year: CTBUH 1974; Wikidata P1619 opening 1973 (CTBUH used). Shown with 1 decimal because another building rounds to the same whole metre. |
| 26 | KK100 | Shenzhen, CN | 441.8 | 98 floors / Completed 2011 | [CTBUH](https://www.skyscrapercenter.com/building/kk100/173) | [Wikidata Q1470046](https://www.wikidata.org/wiki/Q1470046) 442 | 0.05 | Floors: CTBUH 98 above ground; Wikidata P1101 100 (CTBUH used). Shown with 1 decimal because another building rounds to the same whole metre. |
| 27 | Guangzhou International Finance Center | Guangzhou, CN | 438.6 | 101 floors / Completed 2010 | [CTBUH](https://www.skyscrapercenter.com/building/guangzhou-international-finance-center/174) | [Wikidata Q1043438](https://www.wikidata.org/wiki/Q1043438) 440 | 0.32 | Floors: CTBUH 101 above ground; Wikidata P1101 103 (CTBUH used). |
| 28 | 111 West 57th Street | New York City, US | 435.25 | 84 floors / Completed 2021 | [CTBUH](https://www.skyscrapercenter.com/building/111-west-57th-street/14320) | [Wikidata Q2631268](https://www.wikidata.org/wiki/Q2631268) 435.3 | 0.01 | Floors: CTBUH 84 above ground; Wikidata P1101 82 (CTBUH used). |
| 29 | One Vanderbilt | New York City, US | 427.02 | 62 floors / Completed 2020 | [CTBUH](https://www.skyscrapercenter.com/building/one-vanderbilt-avenue/15833) | [Wikidata Q18398409](https://www.wikidata.org/wiki/Q18398409) 427 | -0.0 | CTBUH name: One Vanderbilt Avenue. |
| 30 | 432 Park Avenue | New York City, US | 425.7 | 85 floors / Completed 2015 | [CTBUH](https://www.skyscrapercenter.com/building/432-park-avenue/13227) | [Wikidata Q233940](https://www.wikidata.org/wiki/Q233940) 425.5 | -0.05 |  |
| 31 | Marina 101 | Dubai, AE | 425 | 101 floors / Completed 2017 | [CTBUH](https://www.skyscrapercenter.com/building/marina-101/207) | [Wikidata Q1165269](https://www.wikidata.org/wiki/Q1165269) 425 | 0.0 | IMAGE: none (image=null) - All completed-state candidates (P18, skyline shots) carry {{NoFoP-UAE}}; untagged files in Category:Marina 101 / title search are 2007-08 construction photos or an ISS overview -> image=null. |
| 32 | Trump International Hotel & Tower | Chicago, US | 423.22 | 98 floors / Completed 2009 | [CTBUH](https://www.skyscrapercenter.com/building/trump-international-hotel-tower/203) | [Wikidata Q546221](https://www.wikidata.org/wiki/Q546221) 423.2 | -0.0 | Shown with 1 decimal because another building rounds to the same whole metre. |
| 33 | JPMorganChase Tower | New York City, US | 423.06 | 61 floors / Completed 2025 | [CTBUH](https://www.skyscrapercenter.com/building/jpmorganchase-tower/34450) | [Wikidata Q109648853](https://www.wikidata.org/wiki/Q109648853) 423.1 | 0.01 | Floors: CTBUH 61 above ground; Wikidata P1101 60 (CTBUH used). Shown with 1 decimal because another building rounds to the same whole metre. |
| 34 | Minying International Trade Center T2 | Dongguan, CN | 422.6 | 85 floors / Completed 2021 | [CTBUH](https://www.skyscrapercenter.com/building/minying-international-trade-center-t2/14196) | [Wikidata Q19458189](https://www.wikidata.org/wiki/Q19458189) 426.9 | 1.02 | Wikidata 426.9 m (+1.0 %) is not referenced to CTBUH (probably a design/tip figure); CTBUH 422.6 m used, Wikipedia list also 422.6 m. Floors: CTBUH 85 above ground; Wikidata P1101 88 (CTBUH used). Shown with 1 decimal because another building rounds to the same whole metre. |
| 35 | Jin Mao Tower | Shanghai, CN | 420.53 | 88 floors / Completed 1999 | [CTBUH](https://www.skyscrapercenter.com/building/jin-mao-tower/189) | [Wikidata Q80813](https://www.wikidata.org/wiki/Q80813) 420.5 | -0.01 |  |
| 36 | Zijin Financial Building | Nanjing, CN | 416.6 | 88 floors / Completed 2025 | [CTBUH](https://www.skyscrapercenter.com/building/zijin-financial-building/24137) | [Wikipedia 'List of tallest buildings'](https://en.wikipedia.org/wiki/List_of_tallest_buildings) 416.6 | 0.0 | Wikidata item has no height statement; cross-checked against Wikipedia list instead. |
| 37 | Princess Tower | Dubai, AE | 413.36 | 101 floors / Completed 2012 | [CTBUH](https://www.skyscrapercenter.com/building/princess-tower/206) | [Wikidata Q19492](https://www.wikidata.org/wiki/Q19492) 414 | 0.15 | Shown with 1 decimal because another building rounds to the same whole metre. IMAGE: none (image=null) - Completed-state candidates carry {{NoFoP-UAE}}; untagged ones are construction photos (2007-08) or views FROM the tower ('View from 90-th floor'), not of it -> image=null. |
| 38 | Al Hamra Tower | Kuwait City, KW | 412.6 | 80 floors / Completed 2011 | [CTBUH](https://www.skyscrapercenter.com/building/al-hamra-tower/208) | [Wikidata Q557933](https://www.wikidata.org/wiki/Q557933) 412 | -0.15 | Completion year: CTBUH 2011; Wikidata P1619 opening 2015 (CTBUH used). Shown with 1 decimal because another building rounds to the same whole metre. IMAGE: First-pass pick 'Al Hamra Kuwait Mai 2010.jpg' shows cladding/crane during construction. Replaced with 2022 completed-state view from Kuwait Towers (no NoFoP tag; Kuwait has no FoP -> RISK flag). |
| 39 | Two International Finance Centre | Hong Kong, CN | 412 | 88 floors / Completed 2003 | [CTBUH](https://www.skyscrapercenter.com/building/two-international-finance-centre/205) | [Wikipedia 'List of tallest buildings'](https://en.wikipedia.org/wiki/List_of_tallest_buildings) 412 | 0.0 | Wikidata item has no height statement; cross-checked against Wikipedia list instead. Shown with 1 decimal because another building rounds to the same whole metre. |
| 40 | LCT The Sharp Landmark Tower | Busan, KR | 411.6 | 101 floors / Completed 2019 | [CTBUH](https://www.skyscrapercenter.com/building/lct-the-sharp-landmark-tower/108) | [Wikidata Q5961370](https://www.wikidata.org/wiki/Q5961370) 411 | -0.15 | Shown with 1 decimal because another building rounds to the same whole metre. IMAGE: none (image=null) - the only candidates carry a {{NoFoP-...}} template (no commercial FoP in this country); renderer should use a silhouette/placeholder. |
| 41 | Ningbo Center Tower 1 | Ningbo, CN | 409 | 80 floors / Completed 2025 | [CTBUH](https://www.skyscrapercenter.com/building/ningbo-center-tower-1/13153) | [Wikidata Q1605680](https://www.wikidata.org/wiki/Q1605680) 409 | 0.0 |  |
| 42 | Guangxi China Resources Tower | Nanning, CN | 402.65 | 86 floors / Completed 2020 | [CTBUH](https://www.skyscrapercenter.com/building/guangxi-china-resources-tower/33180) | [Wikidata Q18347369](https://www.wikidata.org/wiki/Q18347369) 402.7 | 0.01 | Floors: CTBUH 86 above ground; Wikidata P1101 85 (CTBUH used). |
| 43 | Guiyang International Financial Center T1 | Guiyang, CN | 401 | 79 floors / Completed 2020 | [CTBUH](https://www.skyscrapercenter.com/building/guiyang-international-financial-center-t1/33699) | [Wikipedia 'List of tallest buildings'](https://en.wikipedia.org/wiki/List_of_tallest_buildings) 401 | 0.0 | Wikidata item has no height statement; cross-checked against Wikipedia list instead. IMAGE: none (image=null) - Only candidates ('Guizhou Financial City District.jpg' 2019, Bank of Guizhou HQ photos 2021) show towers with cranes on top and the T1 tower cannot be identified with confidence -> image=null rather than risk a wrong/under-construction building. |
| 44 | Iconic Tower | New Administrative Capital, EG | 393.8 | 77 floors / Completed 2024 | [CTBUH](https://www.skyscrapercenter.com/building/iconic-tower/34420) | [Wikidata Q102281065](https://www.wikidata.org/wiki/Q102281065) 393.8 | 0.0 | Floors: CTBUH 77 above ground; Wikidata P1101 80 (CTBUH used). |
| 45 | China Merchants Bank Global HQ | Shenzhen, CN | 393 | 77 floors / Completed 2025 | [CTBUH](https://www.skyscrapercenter.com/building/china-merchants-bank-global-headquarters-main-tower/42765) | [Wikipedia 'List of tallest buildings'](https://en.wikipedia.org/wiki/List_of_tallest_buildings) 393 | 0.0 | Wikidata item has no height statement; cross-checked against Wikipedia list instead. CTBUH name: China Merchants Bank Global Headquarters Main Tower. IMAGE: First-pass pick 'SHENZHEN TALENTS PARK (26) (cropped).jpg' (Dec 2024) shows cranes on top (before completion). Chose completed-state photo of the tower (file description names it 招银环球金融中心). |
| 46 | China Resources Tower | Shenzhen, CN | 392.5 | 68 floors / Completed 2018 | [CTBUH](https://www.skyscrapercenter.com/building/china-resources-tower/14589) | [Wikidata Q18111159](https://www.wikidata.org/wiki/Q18111159) 392.5 | 0.0 | Floors: CTBUH 68 above ground; Wikidata P1101 66, 67 (CTBUH used). Completion year: CTBUH 2018; Wikidata P1619 opening 2017 (CTBUH used). Shown with 1 decimal because another building rounds to the same whole metre. |
| 47 | 23 Marina | Dubai, AE | 392.35 | 88 floors / Completed 2012 | [CTBUH](https://www.skyscrapercenter.com/building/23-marina/247) | [Wikidata Q216264](https://www.wikidata.org/wiki/Q216264) 392.4 | 0.01 | Floors: CTBUH 88 above ground; Wikidata P1101 89 (CTBUH used). Shown with 1 decimal because another building rounds to the same whole metre. |
| 48 | CITIC Plaza | Guangzhou, CN | 390.2 | 80 floors / Completed 1996 | [CTBUH](https://www.skyscrapercenter.com/building/citic-plaza/242) | [Wikidata Q245246](https://www.wikidata.org/wiki/Q245246) 390.2 | 0.0 |  |
| 49 | Citymark Centre | Shenzhen, CN | 388.3 | 70 floors / Completed 2022 | [CTBUH](https://www.skyscrapercenter.com/building/citymark-centre/22997) | [Wikidata Q130693037](https://www.wikidata.org/wiki/Q130693037) 388 | -0.08 | CTBUH name: CITYMARK CENTRE. Shown with 1 decimal because another building rounds to the same whole metre. |
| 50 | Shum Yip Upperhills Tower 1 | Shenzhen, CN | 388.05 | 80 floors / Completed 2020 | [CTBUH](https://www.skyscrapercenter.com/building/shum-yip-upperhills-tower-1/16001) | [Wikidata Q18415349](https://www.wikidata.org/wiki/Q18415349) 388.1 | 0.01 | Completion year: CTBUH 2020; Wikidata P1619 opening 2017 (CTBUH used). Shown with 1 decimal because another building rounds to the same whole metre. IMAGE: First-pass pick is a street-level shot of a bank branch entrance; Wikipedia list image is only 219x390 px. Chose CC0 2023 view of both Upperhills towers from Sungang West Road (Tower 1 = taller one). |

**差异 > 0.5% 共 3 条**，原因已写进各条备注：Makkah Royal Clock Tower（+1.0%）；Wuhan Center（-1.16%）；Minying International Trade Center T2（+1.02%）。没有超过 10% 的。

**洞察卡数据核对**（按 `data.json` 计算）：

- after 41：「4 of the world's 50 tallest buildings were completed in 2025 alone.」
- after 31：「Shenzhen and New York City tie for the most towers in the top 50: 6 each.」
- after 19：「15 of the top 50 were completed in 2020 or later.」
- after 11：「Only 8 of the top 50 stand in the Americas, all of them in the United States.」
- after 4：「Only 4 completed buildings on Earth rise higher than 600 m.」
  - 依据：2025 年竣工 4 座；Shenzhen 6 座、New York City 6 座；2020 年及以后竣工 15 座；美洲 8 座（全在美国）；≥600 m 有 4 座。国家计分：CN 26, US 8, AE 4, MY 4, KR 2, SA 1, TW 1, RU 1, VN 1, KW 1, EG 1。

## 3. 全景自由（FoP）核查

依据 Commons:Freedom of panorama/table 的「Buildings」一栏（2026-11-03 抓取），并核对各国 Copyright rules by territory 页：

| 国家 / 地区 | 本期楼数 | 建筑 FoP（商用） | 依据摘要 |
|---|---|---|---|
| 中国大陆 | 24 | ✓ | Commons 表 ✓；文件常带 {{FoP-China}} |
| 香港 | 2 | ✓ | Commons 表 ✓ |
| 美国 | 8 | ✓ | 17 USC §120(a)：从公共场所可见的建筑可自由拍摄、发布 |
| 马来西亚 | 4 | ✓ | Commons 表 ✓；{{FoP-Malaysia}} |
| 沙特阿拉伯 | 1 | ✓ | Commons 表建筑栏 ✓；{{FoP-Saudi Arabia}} |
| 台湾 | 1 | ✓ | Commons 表建筑栏 ✓ |
| 俄罗斯 | 1 | ✓ | Commons 表建筑栏 ✓ |
| **阿联酋** | 4 | ✗ | 无可用 FoP（Federal Decree-Law 38/2021）。第 22.7 条允许「在广播节目中展示」永久置于公共场所的建筑作品，但 Commons 不认它为 FoP。YouTube 视频算不算「broadcasting programs」，**需法律判断** |
| **韩国** | 2 | ✗ | 著作权法第 35(2) 条：仅限非商用。Commons 实际会对乐天世界塔做打码处理（有 `Lotte world tower (censored).jpg`） |
| **科威特** | 1 | ✗ | Law 75/2019 没有 FoP 例外 |
| **埃及** | 1 | ✗ | Law 82/2002 第 171 条：仅限个人使用 |
| **越南** | 1 | ✗（2023 起） | Law 07/2022：2023-01-01 起仅限非商用；2023 年前上传到 Commons 的照片仍保留，带 {{FoP-Vietnam}} |

**选图规则**（`05_select_download.py`）：
1. 许可只接受 PD / CC0 / CC BY / CC BY-SA。带删除请求或侵权标记、过小（短边 < 700 px）、超宽全景（宽高比 > 2.2）的文件不用。
2. **带 {{NoFoP-…}} 模板的文件一律跳过**（按任务规则视为 FoP 问题文件）。
3. 无 FoP 国家的楼，如果有未加 NoFoP 标、也没有删除请求的文件，仍可选用，但在 `assets.json` 的 `fop_note` 里写 **RISK**。法律上它和带标的文件处境相同，未加标只说明 Commons 没人处理过，不说明可以商用。**发布前须人工决定**：保留、换成更远的天际线图，或去掉图片改用剪影。
4. 每个文件页上实际看到的 FoP 模板和分类都记在 `fop_note` 里。


### 逐张 FoP 与选图结果

| # | 名称 | 图片 | 许可 | FoP 记录 |
|---|---|---|---|---|
| 1 | Burj Khalifa | [01_burj_khalifa.jpg](https://commons.wikimedia.org/wiki/File:Burj_Khalifa_Dubai,_UAE_at_Sunset_001_by_Eric_Chamchoum.jpg) | CC BY 4.0 | File page FoP templates: none. Country: UAE: no usable FoP for commercial use (Decree-Law 38/2021 art. 22.7 only covers presenting works in broadcasting programs). RISK: building is copyrighted architecture in a no-commercial-FoP country; Commons hosts the file without a NoFoP tag or deletion request, but commercial (monetised) use needs human/legal sign-off. Skipped NoFoP-tagged candidates: Dubai skyline 2015 (crop).jpg; Burj Khalifa (worlds tallest building) and the Dubai skyline (25781049892).jpg; Burj Khalifa from a ferry, Dubai.jpg; Dubai Skyline mit Burj Khalifa (18241030269).jpg. |
| 2 | Merdeka 118 | [02_merdeka_118.jpg](https://commons.wikimedia.org/wiki/File:Merdeka_Tower_20241022_-_full_2.jpg) | CC0 | File page FoP templates: FoP-Malaysia. Country: Malaysia: FoP for buildings OK (commercial). |
| 3 | Shanghai Tower | [03_shanghai_tower.jpg](https://commons.wikimedia.org/wiki/File:20191114_Shanghai_Tower_(2).jpg) | CC0 | File page FoP templates: FoP-China. Country: China: FoP for buildings OK (commercial). |
| 4 | Makkah Royal Clock Tower | [04_makkah_royal_clock_tower.jpg](https://commons.wikimedia.org/wiki/File:Abraj-al-Bait-Towers.JPG) | CC BY-SA 3.0 | File page FoP templates: FoP-Saudi Arabia. Country: Saudi Arabia: FoP for buildings OK (Commons table). |
| 5 | Ping An Finance Center | [05_ping_an_finance_center.jpg](https://commons.wikimedia.org/wiki/File:Pingan_International_Finance_Center2020.jpg) | CC BY-SA 4.0 | File page FoP templates: FoP-China. Country: China: FoP for buildings OK (commercial). |
| 6 | Lotte World Tower | **无图（image=null）** | — | none (image=null) - Every unredacted candidate carries {{NoFoP-South Korea}}; the only untagged file is Commons' own redacted 'Lotte world tower (censored).jpg' (tower blacked out). Korea FoP is non-commercial only -> image=null. |
| 7 | One World Trade Center | [07_one_world_trade_center.jpg](https://commons.wikimedia.org/wiki/File:One_World_Trade_Center,_New_York_(33224081040).jpg) | CC BY-SA 2.0 | File page FoP templates: FoP-US. Country: United States: architecture photos are free (17 USC 120(a)). |
| 8 | Guangzhou CTF Finance Centre | [08_guangzhou_ctf_finance_centre.jpg](https://commons.wikimedia.org/wiki/File:Guangzhou_CTF_Finance_Centre_02-10-2018.jpg) | CC BY-SA 4.0 | File page FoP templates: FoP-China. Country: China: FoP for buildings OK (commercial). |
| 8 | Tianjin CTF Finance Centre | [08_tianjin_ctf_finance_centre.jpg](https://commons.wikimedia.org/wiki/File:Tianjin_CTF_Finance_Centre,_21_of_24.jpg) | CC BY-SA 4.0 | File page FoP templates: FoP-China. Country: China: FoP for buildings OK (commercial). |
| 10 | CITIC Tower (China Zun) | [10_citic_tower.jpg](https://commons.wikimedia.org/wiki/File:China_Zun_05-11-2018.jpg) | CC BY-SA 4.0 | File page FoP templates: FoP-China. Country: China: FoP for buildings OK (commercial). |
| 11 | Taipei 101 | [11_taipei_101.jpg](https://commons.wikimedia.org/wiki/File:Taipei_101_from_Xiangshan_20250731.jpg) | CC BY-SA 4.0 | File page FoP templates: none. Country: Taiwan: FoP for buildings OK (commercial). |
| 12 | Shanghai World Financial Center | [12_shanghai_world_financial_center.jpg](https://commons.wikimedia.org/wiki/File:%E4%B8%8A%E6%B5%B7%E5%9B%BD%E9%99%85%E9%87%91%E8%9E%8D%E4%B8%AD%E5%BF%83.jpg) | CC0 | File page FoP templates: FoP-China. Country: China: FoP for buildings OK (commercial). |
| 13 | International Commerce Centre | [13_international_commerce_centre.jpg](https://commons.wikimedia.org/wiki/File:International_Commerce_Centre_in_201008.jpg) | CC BY-SA 4.0 | File page FoP templates: none. Country: Hong Kong: FoP for buildings OK (commercial). |
| 14 | Wuhan Greenland Center | [14_wuhan_greenland_center.jpg](https://commons.wikimedia.org/wiki/File:(CHN-Hubei)_Wuhan_Greenland_Center_2024-12-01.jpg) | CC BY 4.0 | File page FoP templates: none. Country: China: FoP for buildings OK (commercial). |
| 15 | Central Park Tower | [15_central_park_tower.jpg](https://commons.wikimedia.org/wiki/File:Central_Park_Tower_April_2021.jpg) | CC BY-SA 3.0 | File page FoP templates: FoP-US. Country: United States: architecture photos are free (17 USC 120(a)). |
| 16 | Lakhta Center | [16_lakhta_center.jpg](https://commons.wikimedia.org/wiki/File:Lakhta_Center_(img4).jpg) | CC BY-SA 4.0 | File page FoP templates: none. Country: Russia: FoP for buildings OK (Commons table). |
| 17 | Landmark 81 | [17_landmark_81.jpg](https://commons.wikimedia.org/wiki/File:Landmark_81_in_2021.jpg) | CC BY-SA 4.0 | File page FoP templates: FoP-Vietnam. Country: Vietnam: FoP non-commercial only since 2023-01-01 (Law 07/2022); pre-2023 Commons uploads still hosted. RISK: building is copyrighted architecture in a no-commercial-FoP country; Commons hosts the file without a NoFoP tag or deletion request, but commercial (monetised) use needs human/legal sign-off. Skipped NoFoP-tagged candidates: Ho Chi Minh City panorama 2019 (cropped2).jpg. |
| 18 | The Exchange 106 | [18_the_exchange_106.jpg](https://commons.wikimedia.org/wiki/File:The_Exchange_106_skyline_Nov_of_2021.jpg) | CC BY-SA 4.0 | File page FoP templates: none. Country: Malaysia: FoP for buildings OK (commercial). |
| 19 | Changsha IFS Tower T1 | [19_changsha_ifs_tower_t1.jpg](https://commons.wikimedia.org/wiki/File:Changsha_IFS_2021.jpg) | CC BY-SA 4.0 | File page FoP templates: none. Country: China: FoP for buildings OK (commercial). |
| 20 | Petronas Tower 1 | [20_petronas_tower_1.jpg](https://commons.wikimedia.org/wiki/File:Kuala_Lumpur_-_panoramio_(18).jpg) | CC BY-SA 3.0 | File page FoP templates: none. Country: Malaysia: FoP for buildings OK (commercial). |
| 20 | Petronas Tower 2 | [20_petronas_tower_2.jpg](https://commons.wikimedia.org/wiki/File:Kuala_Lumpur_Malaysia_Petronas-Twin-Towers-01.jpg) | CC BY-SA 3.0 | File page FoP templates: FoP-Malaysia. Country: Malaysia: FoP for buildings OK (commercial). |
| 22 | Suzhou IFS | [22_suzhou_ifs.jpg](https://commons.wikimedia.org/wiki/File:Suzhou_IFS_27-10-2018.jpg) | CC BY-SA 4.0 | File page FoP templates: FoP-China. Country: China: FoP for buildings OK (commercial). |
| 22 | Zifeng Tower | [22_zifeng_tower.jpg](https://commons.wikimedia.org/wiki/File:Zifeng_Tower_2017.jpg) | CC BY-SA 4.0 | File page FoP templates: FoP-China. Country: China: FoP for buildings OK (commercial). |
| 24 | Wuhan Center | [24_wuhan_center.jpg](https://commons.wikimedia.org/wiki/File:Wuhan_Center_Tower_201901_%EF%BC%88view_from_the_Central_Square_of_Wuhan_CBD%EF%BC%89.jpg) | CC BY-SA 4.0 | File page FoP templates: none. Country: China: FoP for buildings OK (commercial). |
| 25 | Willis Tower | [25_willis_tower.jpg](https://commons.wikimedia.org/wiki/File:Chicago_Sears_Tower.jpg) | CC BY-SA 4.0 | File page FoP templates: none. Country: United States: architecture photos are free (17 USC 120(a)). |
| 26 | KK100 | [26_kk100.jpg](https://commons.wikimedia.org/wiki/File:KK100_exterior_southeast.jpg) | CC BY-SA 4.0 | File page FoP templates: none. Country: China: FoP for buildings OK (commercial). |
| 27 | Guangzhou International Finance Center | [27_guangzhou_international_finance_center.jpg](https://commons.wikimedia.org/wiki/File:GZIFC.jpg) | CC BY-SA 3.0 | File page FoP templates: none. Country: China: FoP for buildings OK (commercial). |
| 28 | 111 West 57th Street | [28_111_west_57th_street.jpg](https://commons.wikimedia.org/wiki/File:111_West_57th_Street.png) | CC BY-SA 4.0 | File page FoP templates: none. Country: United States: architecture photos are free (17 USC 120(a)). |
| 29 | One Vanderbilt | [29_one_vanderbilt.jpg](https://commons.wikimedia.org/wiki/File:One_Vanderbilt_42_Street.jpg) | CC BY-SA 4.0 | File page FoP templates: FoP-US. Country: United States: architecture photos are free (17 USC 120(a)). |
| 30 | 432 Park Avenue | [30_432_park_avenue.jpg](https://commons.wikimedia.org/wiki/File:432_Park_Avenue,_NY_(cropped).jpg) | CC BY-SA 4.0 | File page FoP templates: FoP-US. Country: United States: architecture photos are free (17 USC 120(a)). |
| 31 | Marina 101 | **无图（image=null）** | — | none (image=null) - All completed-state candidates (P18, skyline shots) carry {{NoFoP-UAE}}; untagged files in Category:Marina 101 / title search are 2007-08 construction photos or an ISS overview -> image=null. |
| 32 | Trump International Hotel & Tower | [32_trump_international_hotel_and_tower.jpg](https://commons.wikimedia.org/wiki/File:Trump_International_Hotel_and_Tower_2022.jpg) | CC BY-SA 4.0 | File page FoP templates: none. Country: United States: architecture photos are free (17 USC 120(a)). |
| 33 | JPMorganChase Tower | [33_jpmorganchase_tower.jpg](https://commons.wikimedia.org/wiki/File:270parkave_from_empirestate_03_14_2025.jpg) | CC BY-SA 4.0 | File page FoP templates: none. Country: United States: architecture photos are free (17 USC 120(a)). |
| 34 | Minying International Trade Center T2 | [34_minying_international_trade_center_t2.jpg](https://commons.wikimedia.org/wiki/File:%E6%9D%B1%E8%8E%9E%E5%9C%8B%E9%9A%9B%E8%B2%BF%E6%98%93%E4%B8%AD%E5%BF%83-2022.jpg) | CC BY-SA 4.0 | File page FoP templates: none. Country: China: FoP for buildings OK (commercial). |
| 35 | Jin Mao Tower | [35_jin_mao_tower.jpg](https://commons.wikimedia.org/wiki/File:Jin_Mao_Tower_Pudong_21860-Shanghai_(32939744091).jpg) | CC BY 2.0 | File page FoP templates: none. Country: China: FoP for buildings OK (commercial). |
| 36 | Zijin Financial Building | [36_zijin_financial_building.jpg](https://commons.wikimedia.org/wiki/File:%E5%8D%97%E4%BA%AC%E9%87%91%E8%9E%8D%E5%9F%8E%E4%BA%8C%E6%9C%9FC1_(20250325).jpg) | CC0 | File page FoP templates: none. Country: China: FoP for buildings OK (commercial). |
| 37 | Princess Tower | **无图（image=null）** | — | none (image=null) - Completed-state candidates carry {{NoFoP-UAE}}; untagged ones are construction photos (2007-08) or views FROM the tower ('View from 90-th floor'), not of it -> image=null. |
| 38 | Al Hamra Tower | [38_al_hamra_tower.jpg](https://commons.wikimedia.org/wiki/File:Kuwait_City_Kuwait_Towers_View_to_the_al-Hamra_Tower.jpg) | CC BY 4.0 | File page FoP templates: none. Country: Kuwait: no FoP (Law 75/2019). RISK: building is copyrighted architecture in a no-commercial-FoP country; Commons hosts the file without a NoFoP tag or deletion request, but commercial (monetised) use needs human/legal sign-off. Skipped NoFoP-tagged candidates: Kuwait City (37519834).jpeg; Kuwait Alhamra Tower (37472150).jpeg; Kuwait City skyline (39710595225).jpg. |
| 39 | Two International Finance Centre | [39_two_international_finance_centre.jpg](https://commons.wikimedia.org/wiki/File:HK_International_Finance_Centre_200809.jpg) | CC BY 3.0 | File page FoP templates: none. Country: Hong Kong: FoP for buildings OK (commercial). |
| 40 | LCT The Sharp Landmark Tower | **无图（image=null）** | — | none (image=null) - the only candidates carry a {{NoFoP-...}} template (no commercial FoP in this country); renderer should use a silhouette/placeholder. |
| 41 | Ningbo Center Tower 1 | [41_ningbo_center_tower_1.jpg](https://commons.wikimedia.org/wiki/File:Ningbo_Center_2025-07-20.jpg) | CC BY-SA 4.0 | File page FoP templates: none. Country: China: FoP for buildings OK (commercial). |
| 42 | Guangxi China Resources Tower | [42_guangxi_china_resources_tower.jpg](https://commons.wikimedia.org/wiki/File:Dongmeng_CBD_3.jpg) | CC BY-SA 4.0 | File page FoP templates: none. Country: China: FoP for buildings OK (commercial). |
| 43 | Guiyang International Financial Center T1 | **无图（image=null）** | — | none (image=null) - Only candidates ('Guizhou Financial City District.jpg' 2019, Bank of Guizhou HQ photos 2021) show towers with cranes on top and the T1 tower cannot be identified with confidence -> image=null rather than risk a wrong/under-construction building. |
| 44 | Iconic Tower | [44_iconic_tower.jpg](https://commons.wikimedia.org/wiki/File:Iconic_Tower_Egypt(18-6-2023)(cropped).jpg) | CC BY-SA 4.0 | File page FoP templates: none. Country: Egypt: no FoP (Law 82/2002 art. 171, personal use only). RISK: building is copyrighted architecture in a no-commercial-FoP country; Commons hosts the file without a NoFoP tag or deletion request, but commercial (monetised) use needs human/legal sign-off. |
| 45 | China Merchants Bank Global HQ | [45_china_merchants_bank_global_hq.jpg](https://commons.wikimedia.org/wiki/File:%E6%8B%9B%E9%93%B6%E7%8E%AF%E7%90%83%E9%87%91%E8%9E%8D%E4%B8%AD%E5%BF%83.jpg) | CC BY-SA 4.0 | File page FoP templates: none. Country: China: FoP for buildings OK (commercial). |
| 46 | China Resources Tower | [46_china_resources_tower.jpg](https://commons.wikimedia.org/wiki/File:China_Resources_Headquarters_by_the_side_of_shenzhen_bay2020.jpg) | CC BY-SA 4.0 | File page FoP templates: none. Country: China: FoP for buildings OK (commercial). |
| 47 | 23 Marina | [47_23_marina.jpg](https://commons.wikimedia.org/wiki/File:Mage_2024-05-14_at_19.29.21.jpg) | CC BY-SA 4.0 | File page FoP templates: none. Country: UAE: no usable FoP for commercial use (Decree-Law 38/2021 art. 22.7 only covers presenting works in broadcasting programs). RISK: building is copyrighted architecture in a no-commercial-FoP country; Commons hosts the file without a NoFoP tag or deletion request, but commercial (monetised) use needs human/legal sign-off. Skipped NoFoP-tagged candidates: Dubai Marina Skyline.jpg; Dubai Marina Aug2012.jpg. |
| 48 | CITIC Plaza | [48_citic_plaza.jpg](https://commons.wikimedia.org/wiki/File:CITIC_Plaza_2017.jpg) | CC BY-SA 4.0 | File page FoP templates: none. Country: China: FoP for buildings OK (commercial). |
| 49 | Citymark Centre | [49_citymark_centre.jpg](https://commons.wikimedia.org/wiki/File:Citymark_Centre_-_Chengmai_Center_Shenzhen_2025.jpeg) | CC BY-SA 4.0 | File page FoP templates: none. Country: China: FoP for buildings OK (commercial). |
| 50 | Shum Yip Upperhills Tower 1 | [50_shum_yip_upperhills_tower_1.jpg](https://commons.wikimedia.org/wiki/File:SZ_%E6%B7%B1%E5%9C%B3_Shenzhen_%E7%A6%8F%E7%94%B0_Futian_%E7%AD%8D%E5%B4%97%E8%A5%BF%E8%B7%AF_Sungang_West_Road_%E7%AD%86%E6%9E%B6%E5%B1%B1%E5%85%AC%E5%9C%92_Bijiashan_Park_Passover_footbridge_view_UpperHills_November_2023_R12S_06.jpg) | CC0 | File page FoP templates: none. Country: China: FoP for buildings OK (commercial). |

## 4. 署名决定

- Commons 署名格式按 Commons:Credit_line：作者 + 许可名 + 许可链接 + 文件页链接；署作者，不署上传者。
- 卡片上 `image_credit` 写短格式「作者 / 许可」，公有领域写「Public domain」；描述框附完整署名块（下节）。CC BY-SA 图片只做缩放和裁切，不做其他改编，`modified` 字段写明。
- 片尾来源卡写：「Photos: Wikimedia Commons contributors (see description)」。
- Wikidata 是 CC0，按惯例仍在来源行注明；CTBUH 作为事实出处注明。

## 5. YouTube 描述框署名块（可直接粘贴）

```
Data: CTBUH Skyscraper Center, "The 100 Tallest Completed Buildings in the World" (retrieved 3 Nov 2026), https://www.skyscrapercenter.com/buildings
Heights = CTBUH architectural height (incl. spires, excl. antennas); completed buildings only, per CTBUH status as of 3 Nov 2026.
Cross-checked with Wikidata (CC0).

Photos (Wikimedia Commons; resized/cropped):

#1 Burj Khalifa: ECWiki1, CC BY 4.0 https://creativecommons.org/licenses/by/4.0, https://commons.wikimedia.org/wiki/File:Burj_Khalifa_Dubai,_UAE_at_Sunset_001_by_Eric_Chamchoum.jpg
#2 Merdeka 118: Ahmad Ali Karim, CC0 http://creativecommons.org/publicdomain/zero/1.0/deed.en, https://commons.wikimedia.org/wiki/File:Merdeka_Tower_20241022_-_full_2.jpg
#3 Shanghai Tower: Balon Greyjoy, CC0 http://creativecommons.org/publicdomain/zero/1.0/deed.en, https://commons.wikimedia.org/wiki/File:20191114_Shanghai_Tower_(2).jpg
#4 Makkah Royal Clock Tower: King Eliot, CC BY-SA 3.0 https://creativecommons.org/licenses/by-sa/3.0, https://commons.wikimedia.org/wiki/File:Abraj-al-Bait-Towers.JPG
#5 Ping An Finance Center: Charlie fong, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:Pingan_International_Finance_Center2020.jpg
#7 One World Trade Center: Pedro Szekely from Los Angeles, USA, CC BY-SA 2.0 https://creativecommons.org/licenses/by-sa/2.0, https://commons.wikimedia.org/wiki/File:One_World_Trade_Center,_New_York_(33224081040).jpg
#8 Guangzhou CTF Finance Centre: Milkomède, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:Guangzhou_CTF_Finance_Centre_02-10-2018.jpg
#8 Tianjin CTF Finance Centre: BD2412, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:Tianjin_CTF_Finance_Centre,_21_of_24.jpg
#10 CITIC Tower (China Zun): Milkomède, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:China_Zun_05-11-2018.jpg
#11 Taipei 101: User:Sinsyuan, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:Taipei_101_from_Xiangshan_20250731.jpg
#12 Shanghai World Financial Center: GG001213, CC0 http://creativecommons.org/publicdomain/zero/1.0/deed.en, https://commons.wikimedia.org/wiki/File:%E4%B8%8A%E6%B5%B7%E5%9B%BD%E9%99%85%E9%87%91%E8%9E%8D%E4%B8%AD%E5%BF%83.jpg
#13 International Commerce Centre: WiNG, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:International_Commerce_Centre_in_201008.jpg
#14 Wuhan Greenland Center: S5A-0043, CC BY 4.0 https://creativecommons.org/licenses/by/4.0, https://commons.wikimedia.org/wiki/File:(CHN-Hubei)_Wuhan_Greenland_Center_2024-12-01.jpg
#15 Central Park Tower: Percival Kestreltail, CC BY-SA 3.0 https://creativecommons.org/licenses/by-sa/3.0, https://commons.wikimedia.org/wiki/File:Central_Park_Tower_April_2021.jpg
#16 Lakhta Center: Florstein (Telegram:WikiPhoto.Space), CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:Lakhta_Center_(img4).jpg
#17 Landmark 81: Joefrance1995, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:Landmark_81_in_2021.jpg
#18 The Exchange 106: LegendaryLim, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:The_Exchange_106_skyline_Nov_of_2021.jpg
#19 Changsha IFS Tower T1: 維基小霸王, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:Changsha_IFS_2021.jpg
#20 Petronas Tower 1: AwOiSoAk KaOsIoWa, CC BY-SA 3.0 https://creativecommons.org/licenses/by-sa/3.0, https://commons.wikimedia.org/wiki/File:Kuala_Lumpur_-_panoramio_(18).jpg
#20 Petronas Tower 2: CEphoto, Uwe Aranas, CC BY-SA 3.0 https://creativecommons.org/licenses/by-sa/3.0, https://commons.wikimedia.org/wiki/File:Kuala_Lumpur_Malaysia_Petronas-Twin-Towers-01.jpg
#22 Suzhou IFS: Milkomède, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:Suzhou_IFS_27-10-2018.jpg
#22 Zifeng Tower: Haha169, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:Zifeng_Tower_2017.jpg
#24 Wuhan Center: Wuchernchau, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:Wuhan_Center_Tower_201901_%EF%BC%88view_from_the_Central_Square_of_Wuhan_CBD%EF%BC%89.jpg
#25 Willis Tower: Daniel Schwen, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:Chicago_Sears_Tower.jpg
#26 KK100: Charlie fong, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:KK100_exterior_southeast.jpg
#27 Guangzhou International Finance Center: 慕尼黑啤酒, CC BY-SA 3.0 https://creativecommons.org/licenses/by-sa/3.0, https://commons.wikimedia.org/wiki/File:GZIFC.jpg
#28 111 West 57th Street: Short final, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:111_West_57th_Street.png
#29 One Vanderbilt: Gaiusahala, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:One_Vanderbilt_42_Street.jpg
#30 432 Park Avenue: Epistola8, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:432_Park_Avenue,_NY_(cropped).jpg
#32 Trump International Hotel & Tower: Pedro Szekely, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:Trump_International_Hotel_and_Tower_2022.jpg
#33 JPMorganChase Tower: Jfendi, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:270parkave_from_empirestate_03_14_2025.jpg
#34 Minying International Trade Center T2: David290, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:%E6%9D%B1%E8%8E%9E%E5%9C%8B%E9%9A%9B%E8%B2%BF%E6%98%93%E4%B8%AD%E5%BF%83-2022.jpg
#35 Jin Mao Tower: xiquinhosilva, CC BY 2.0 https://creativecommons.org/licenses/by/2.0, https://commons.wikimedia.org/wiki/File:Jin_Mao_Tower_Pudong_21860-Shanghai_(32939744091).jpg
#36 Zijin Financial Building: Fumikas Sagisavas, CC0 http://creativecommons.org/publicdomain/zero/1.0/deed.en, https://commons.wikimedia.org/wiki/File:%E5%8D%97%E4%BA%AC%E9%87%91%E8%9E%8D%E5%9F%8E%E4%BA%8C%E6%9C%9FC1_(20250325).jpg
#38 Al Hamra Tower: Zairon, CC BY 4.0 https://creativecommons.org/licenses/by/4.0, https://commons.wikimedia.org/wiki/File:Kuwait_City_Kuwait_Towers_View_to_the_al-Hamra_Tower.jpg
#39 Two International Finance Centre: WiNG, CC BY 3.0 https://creativecommons.org/licenses/by/3.0, https://commons.wikimedia.org/wiki/File:HK_International_Finance_Centre_200809.jpg
#41 Ningbo Center Tower 1: Cz4523, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:Ningbo_Center_2025-07-20.jpg
#42 Guangxi China Resources Tower: EditQ, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:Dongmeng_CBD_3.jpg
#44 Iconic Tower: Mohamed Ouda, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:Iconic_Tower_Egypt(18-6-2023)(cropped).jpg
#45 China Merchants Bank Global HQ: Lhzss8, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:%E6%8B%9B%E9%93%B6%E7%8E%AF%E7%90%83%E9%87%91%E8%9E%8D%E4%B8%AD%E5%BF%83.jpg
#46 China Resources Tower: Charlie fong, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:China_Resources_Headquarters_by_the_side_of_shenzhen_bay2020.jpg
#47 23 Marina: BS2024, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:Mage_2024-05-14_at_19.29.21.jpg
#48 CITIC Plaza: そらみみ, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:CITIC_Plaza_2017.jpg
#49 Citymark Centre: Ubahnverleih, CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0, https://commons.wikimedia.org/wiki/File:Citymark_Centre_-_Chengmai_Center_Shenzhen_2025.jpeg
#50 Shum Yip Upperhills Tower 1: Husyewl Lmsiuyu RAUOM, CC0 http://creativecommons.org/publicdomain/zero/1.0/deed.en, https://commons.wikimedia.org/wiki/File:SZ_%E6%B7%B1%E5%9C%B3_Shenzhen_%E7%A6%8F%E7%94%B0_Futian_%E7%AD%8D%E5%B4%97%E8%A5%BF%E8%B7%AF_Sungang_West_Road_%E7%AD%86%E6%9E%B6%E5%B1%B1%E5%85%AC%E5%9C%92_Bijiashan_Park_Passover_footbridge_view_UpperHills_November_2023_R12S_06.jpg
```
