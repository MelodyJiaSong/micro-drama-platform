# ep14 · 数据出处、交叉核对与许可（sources.md）

> 2026-11-03 代理整理（follow-up 015 子代理）。本文件由 `_build/gen_sources.py` 从 `data.json` / `assets.json` 生成。

## 1. 口径

- **名单**：Smithsonian Institution Global Volcanism Program（GVP）《Volcanoes of the World》数据库的 **Holocene 火山表**（全新世约 11,700 年内有喷发或活动证据；含 GVP 标 *Evidence Uncertain* 的条目）。
  - 取数：GVP 官方 GeoServer WFS `https://webservices.volcano.si.edu/geoserver/GVP-VOTW/ows`，图层 `GVP-VOTW:Smithsonian_VOTW_Holocene_Volcanoes`，2026-11-03 下载，共 1,214 座（原始文件 `_build/raw/gvp_holocene.json`）；Pleistocene 表同日下载 1,452 座（`_build/raw/gvp_pleistocene.json`），只用于说明口径与洞察卡 1。
  - GVP 网页 `volcano.si.edu/volcano.cfm?vn=…` 当天对脚本返回 Cloudflare 验证页，卡片 `source.url` 仍写该火山的 GVP 页面地址，数值以 WFS 下载为准。
- **排序**：GVP `Elevation` 字段（峰顶海拔，m）降序取前 50；前 50 无同值。San José 用 GVP 地质概述的 5,856 m（WFS 字段 6,070 m 实为邻峰 Marmolejo，审片问题 1）。第 50 名 Popocatépetl 5,393 m，第 51 名 Ticsani 5,382 m（差 11 m）。
- **显示**：`value_display` 为 GVP 整米值；`secondary_display` = 米 × 3.28084 四舍五入到整英尺。
- **不收**：GVP Pleistocene 表的火山（Kilimanjaro 5,881、Sajama 6,542、Tupungato 6,570、Tres Cruces 6,620、Ulagh Muztagh 6,945 等）；GVP 两表都没有的 Monte Pissis。
- **标签**：`calendar` = GVP `Last_Eruption_Year`（负数写 BCE；1000 年以前写 c. … CE；无年份时按 GVP 证据类别写 *Eruption date unknown*（Evidence Credible）或 *Possible recent activity*（Evidence Uncertain）；GVP 为 Eruption Observed 但无年份的写 *Eruption observed*）；`mountain` = GVP `Primary_Volcano_Type`。GVP 对持续中的喷发把最近喷发年记为当年，2026 = 2026 年仍有喷发。

## 2. 国家归属

- 国旗 = GVP `Country` 字段第一个国家；字段含两国（如 `Chile-Argentina`）时加 `SHARED WITH <第二国>` 徽章。GVP 对智利与阿根廷 / 玻利维亚的跨境火山一律把 Chile 写在前。
- 计分板（tally.by = country）：Chile 30、Peru 7、Argentina 4、Ecuador 4、Mexico 2、Iran 1、Russia 1、Bolivia 1。
- 跨境 18 座：#1 Ojos del Salado（Argentina）、#2 Llullaillaco（Argentina）、#4 Incahuasi（Argentina）、#7 Parinacota（Bolivia）、#10 El Solo（Argentina）、#11 Sierra Nevada（Argentina）、#14 Socompa（Argentina）、#16 Sairecabur（Bolivia）、#18 Licancabur（Bolivia）、#21 Falso Azufre（Argentina）、#24 San José（Argentina）、#32 Lastarria（Argentina）、#33 Olca-Paruma（Bolivia）、#36 Tupungatito（Argentina）、#41 Guayaques（Bolivia）、#46 Cordón del Azufre（Argentina）、#47 Corrida de Cori（Argentina）、#49 Cerro Bayo（Argentina）。
- 若把跨境火山同时计入第二国：Argentina 4 + 13 = 17，Bolivia 1 + 5 = 6（洞察卡 3 的依据）。

## 3. 逐条出处与交叉核对

交叉核对 = Wikipedia 条目 infobox `elevation_m` 或导言里的海拔（2026-11-03 经 MediaWiki API 取，`_build/raw/wiki_extracts_2026-11-03.json`）。Peakbagger 对脚本返回 403，未核。差 ≥1% 的加粗；排序一律用 GVP 值。

| # | 火山（GVP 号） | 国旗 / 徽章 | GVP 海拔 | Wikipedia | 差 | 最近喷发（GVP） | 图片 |
|---|---|---|---|---|---|---|---|
| 1 | [Ojos del Salado](https://volcano.si.edu/volcano.cfm?vn=355130)（355130） | Chile / SHARED WITH ARGENTINA | 6,879 m | 6,893 | +0.2% | Last eruption c. 750 CE | 风险图 todos los derechos reservados（仅风险版）；默认版 CC BY-SA 2.0 |
| 2 | [Llullaillaco](https://volcano.si.edu/volcano.cfm?vn=355110)（355110） | Chile / SHARED WITH ARGENTINA | 6,739 m | 6,723 | -0.2% | Last eruption 1877 | 风险图 unknown（仅风险版）；默认版 CC BY 2.0 |
| 3 | [Tipas](https://volcano.si.edu/volcano.cfm?vn=355220)（355220） | Argentina | 6,658 m | 6,670 | +0.2% | Eruption date unknown | 风险图 todos los derechos reservados（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 4 | [Incahuasi](https://volcano.si.edu/volcano.cfm?vn=355125)（355125） | Chile / SHARED WITH ARGENTINA | 6,638 m | 6,621 | -0.3% | Possible recent activity | 风险图 unknown（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 5 | [Coropuna](https://volcano.si.edu/volcano.cfm?vn=354003)（354003） | Peru | 6,377 m | 6,377 | +0.0% | Eruption date unknown | 风险图 unknown（仅风险版）；默认版 CC BY-SA 2.0 |
| 6 | [El Cóndor](https://volcano.si.edu/volcano.cfm?vn=355190)（355190） | Argentina | 6,373 m | 6,414 | +0.6% | Eruption date unknown | 风险图 unknown（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 7 | [Parinacota](https://volcano.si.edu/volcano.cfm?vn=355012)（355012） | Chile / SHARED WITH BOLIVIA | 6,336 m | 6,380 | +0.7% | Last eruption c. 290 CE | 风险图 unknown（仅风险版）；默认版 Public domain (NASA) |
| 8 | [Chimborazo](https://volcano.si.edu/volcano.cfm?vn=352071)（352071） | Ecuador | 6,261 m | 6,263.47 | +0.0% | Last eruption c. 550 CE | Unsplash License |
| 9 | [Pular](https://volcano.si.edu/volcano.cfm?vn=355107)（355107） | Chile | 6,233 m | — | — | Possible recent activity | 风险图 todos los derechos reservados（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 10 | [El Solo](https://volcano.si.edu/volcano.cfm?vn=355131)（355131） | Chile / SHARED WITH ARGENTINA | 6,205 m | 6,215 | +0.2% | Eruption date unknown | 风险图 todos los derechos reservados（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 11 | [Sierra Nevada](https://volcano.si.edu/volcano.cfm?vn=355123)（355123） | Chile / SHARED WITH ARGENTINA | 6,173 m | 6,137 | -0.6% | Eruption date unknown | 风险图 todos los derechos reservados（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 12 | [Aracar](https://volcano.si.edu/volcano.cfm?vn=355160)（355160） | Argentina | 6,095 m | 6,095 | +0.0% | Eruption date unknown | 风险图 todos los derechos reservados（仅风险版）；默认版 CC BY 2.0 |
| 13 | [Guallatiri](https://volcano.si.edu/volcano.cfm?vn=355020)（355020） | Chile | 6,071 m | 6,071 | +0.0% | Last eruption 1960 | 风险图 unknown（仅风险版）；默认版 CC BY-SA 2.0 |
| 14 | [Socompa](https://volcano.si.edu/volcano.cfm?vn=355109)（355109） | Chile / SHARED WITH ARGENTINA | 6,031 m | 6,051 | +0.3% | Last eruption 5250 BCE | 风险图 unknown（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 15 | [Acamarachi](https://volcano.si.edu/volcano.cfm?vn=355096)（355096） | Chile | 6,023 m | 6,046 | +0.4% | Eruption date unknown | 风险图 todos los derechos reservados（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 16 | [Sairecabur](https://volcano.si.edu/volcano.cfm?vn=355091)（355091） | Chile / SHARED WITH BOLIVIA | 5,961 m | 5,971 | +0.2% | Eruption date unknown | 风险图 todos los derechos reservados（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 17 | [Sabancaya](https://volcano.si.edu/volcano.cfm?vn=354006)（354006） | Peru / ERUPTED IN 2026 | 5,960 m | 5,960 | +0.0% | Last eruption 2026 | Unsplash License |
| 18 | [Licancabur](https://volcano.si.edu/volcano.cfm?vn=355092)（355092） | Chile / SHARED WITH BOLIVIA | 5,916 m | 5,916 | +0.0% | Eruption date unknown | Pexels License |
| 19 | [Cotopaxi](https://volcano.si.edu/volcano.cfm?vn=352050)（352050） | Ecuador | 5,911 m | 5,897 | -0.2% | Last eruption 2023 | Unsplash License |
| 20 | [Miñiques](https://volcano.si.edu/volcano.cfm?vn=355102)（355102） | Chile | 5,910 m | 5,910 | +0.0% | Possible recent activity | 风险图 Pixnio License（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 21 | [Falso Azufre](https://volcano.si.edu/volcano.cfm?vn=355124)（355124） | Chile / SHARED WITH ARGENTINA | 5,906 m | 5,906 | +0.0% | Possible recent activity | 风险图 todos los derechos reservados（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 22 | [Putana](https://volcano.si.edu/volcano.cfm?vn=355090)（355090） | Chile | 5,884 m | 5,884 | +0.0% | Last eruption 1810 | 风险图 unknown（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 23 | [Taapaca](https://volcano.si.edu/volcano.cfm?vn=355011)（355011） | Chile | 5,860 m | 5,860 | +0.0% | Last eruption 320 BCE | 风险图 todos los derechos reservados（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 24 | [San José](https://volcano.si.edu/volcano.cfm?vn=357020)（357020） | Chile / SHARED WITH ARGENTINA | 5,856 m | 5,856 | +0.0% | Last eruption 1960 | 风险图 todos los derechos reservados（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 25 | [Cordón de Puntas Negras](https://volcano.si.edu/volcano.cfm?vn=355101)（355101） | Chile | 5,852 m | 5,852 | +0.0% | Eruption date unknown | AI-generated (Codex image_gen) |
| 26 | [Tutupaca](https://volcano.si.edu/volcano.cfm?vn=354040)（354040） | Peru | 5,801 m | 5,815 | +0.2% | Last eruption 1802 | 风险图 unknown（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 27 | [El Misti](https://volcano.si.edu/volcano.cfm?vn=354010)（354010） | Peru | 5,793 m | 5,822 | +0.5% | Last eruption 1985 | Unsplash License |
| 28 | [Cayambe](https://volcano.si.edu/volcano.cfm?vn=352006)（352006） | Ecuador | 5,790 m | 5,790 | +0.0% | Last eruption 1786 | 风险图 unknown（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 29 | [Chiliques](https://volcano.si.edu/volcano.cfm?vn=355098)（355098） | Chile | 5,778 m | 5,778 | +0.0% | Possible recent activity | 风险图 unknown（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 30 | [Antisana](https://volcano.si.edu/volcano.cfm?vn=352030)（352030） | Ecuador | 5,753 m | 5,753 | +0.0% | Last eruption 1802 | Unsplash License |
| 31 | [Peinado](https://volcano.si.edu/volcano.cfm?vn=355200)（355200） | Argentina | 5,741 m | 5,890 | **+2.6%** | Eruption date unknown | 风险图 unknown（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 32 | [Lastarria](https://volcano.si.edu/volcano.cfm?vn=355120)（355120） | Chile / SHARED WITH ARGENTINA | 5,706 m | 5,706 | +0.0% | Eruption date unknown | 风险图 todos los derechos reservados（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 33 | [Olca-Paruma](https://volcano.si.edu/volcano.cfm?vn=355050)（355050） | Chile / SHARED WITH BOLIVIA | 5,705 m | — | — | Eruption observed | AI-generated (Codex image_gen) |
| 34 | [Purico Complex](https://volcano.si.edu/volcano.cfm?vn=355094)（355094） | Chile | 5,703 m | 5,703 | +0.0% | Eruption date unknown | 风险图 todos los derechos reservados（仅风险版）；默认版 CC BY 4.0 |
| 35 | [Mount Damavand](https://volcano.si.edu/volcano.cfm?vn=232010)（232010） | Iran | 5,670 m | 5,610 | **-1.1%** | Last eruption 5350 BCE | Unsplash License |
| 36 | [Tupungatito](https://volcano.si.edu/volcano.cfm?vn=357010)（357010） | Chile / SHARED WITH ARGENTINA | 5,660 m | 5,682 | +0.4% | Last eruption 1987 | AI-generated (Codex image_gen) |
| 37 | [Mount Elbrus](https://volcano.si.edu/volcano.cfm?vn=214010)（214010） | Russia | 5,642 m | 5,642 | +0.0% | Last eruption c. 50 CE | Unsplash License |
| 38 | [Colachi](https://volcano.si.edu/volcano.cfm?vn=355095)（355095） | Chile | 5,631 m | 5,631 | +0.0% | Eruption date unknown | AI-generated (Codex image_gen) |
| 39 | [Nevados Casiri](https://volcano.si.edu/volcano.cfm?vn=354060)（354060） | Peru | 5,626 m | — | — | Eruption date unknown | AI-generated (Codex image_gen) |
| 40 | [Ubinas](https://volcano.si.edu/volcano.cfm?vn=354020)（354020） | Peru | 5,608 m | 5,672 | **+1.1%** | Last eruption 2024 | 风险图 unknown（仅风险版）；默认版 Public domain (NASA) |
| 41 | [Guayaques](https://volcano.si.edu/volcano.cfm?vn=355093)（355093） | Chile / SHARED WITH BOLIVIA | 5,598 m | 5,076 | **-9.3%** | Eruption date unknown | AI-generated (Codex image_gen) |
| 42 | [Láscar](https://volcano.si.edu/volcano.cfm?vn=355100)（355100） | Chile / ERUPTED IN 2026 | 5,592 m | 5,592 | +0.0% | Last eruption 2026 | 风险图 unknown（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 43 | [Pico de Orizaba](https://volcano.si.edu/volcano.cfm?vn=341100)（341100） | Mexico | 5,564 m | 5,636 | **+1.3%** | Last eruption 1846 | Pexels License |
| 44 | [Isluga](https://volcano.si.edu/volcano.cfm?vn=355030)（355030） | Chile | 5,550 m | 5,550 | +0.0% | Last eruption 1913 | 风险图 unknown（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 45 | [Yucamane](https://volcano.si.edu/volcano.cfm?vn=354050)（354050） | Peru | 5,495 m | — | — | Last eruption 1320 BCE | 风险图 unknown（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 46 | [Cordón del Azufre](https://volcano.si.edu/volcano.cfm?vn=355121)（355121） | Chile / SHARED WITH ARGENTINA | 5,481 m | 5,481 | +0.0% | Eruption date unknown | 风险图 unknown（仅风险版）；默认版 AI-generated (Codex image_gen) |
| 47 | [Corrida de Cori](https://volcano.si.edu/volcano.cfm?vn=355112)（355112） | Chile / SHARED WITH ARGENTINA | 5,451 m | — | — | Possible recent activity | AI-generated (Codex image_gen) |
| 48 | [Tata Sabaya](https://volcano.si.edu/volcano.cfm?vn=355032)（355032） | Bolivia | 5,430 m | 5,430 | +0.0% | Eruption date unknown | 风险图 unknown（仅风险版）；默认版 Public domain (NASA) |
| 49 | [Cerro Bayo](https://volcano.si.edu/volcano.cfm?vn=355122)（355122） | Chile / SHARED WITH ARGENTINA | 5,413 m | 5,401 | -0.2% | Eruption date unknown | AI-generated (Codex image_gen) |
| 50 | [Popocatépetl](https://volcano.si.edu/volcano.cfm?vn=341090)（341090） | Mexico / ERUPTED IN 2026 | 5,393 m | 5,393 | +0.0% | Last eruption 2026 | Unsplash License |

备注（逐条 notes 见 `data.json`）：
- San José：GVP WFS 字段 6,070 m 是邻峰 Marmolejo 的高度；GVP 地质概述与 Wikipedia 都是 5,856 m，已改用 5,856 m 并重排为 #24（审片问题 1）。
- Guayaques：GVP 5,598 m，Wikipedia 5,076 m（−9.3%）；按 Wikipedia 值会掉出前 50。差异接近 bible §3.4 的 10% 阈值，列入待用户确认。
- Peinado：GVP 5,741 m，Wikipedia 5,890 m（+2.6%）。
- Pico de Orizaba：GVP 5,564 m，Wikipedia 5,636 m（+1.3%）；Mount Damavand：GVP 5,670 m，Wikipedia 5,610 m（−1.1%）；Ubinas：GVP 5,608 m，Wikipedia 5,672 m（+1.1%）。
- Pular、Olca-Paruma、Nevados Casiri、Yucamane、Corrida de Cori：Wikipedia 未给数值，只有 GVP 一源。
- 边界：Ticsani（GVP 5,382 m，第 51）在 Wikipedia 写 5,408 m，按 Wikipedia 会超过 Popocatépetl（5,393 m）。单一来源排序下边界不受影响。

## 4. 洞察卡核对

| after | 文字 | 依据 |
|---|---|---|
| 43 | No Kilimanjaro? It isn't on GVP's list of volcanoes active in the last 11,700 years. | 措辞改为「不在 GVP 近 11,700 年活动火山名单上」（审片问题 9）。GVP Pleistocene 表 222150 Kilimanjaro（5,881 m，无 Holocene 喷发记录）；Holocene 表里没有 Kilimanjaro。Holocene 起点约 11,700 年前（GVP 定义）。 |
| 34 | From the seafloor up, Hawaii's Mauna Kea stands about 10,200 m: taller than all of these. | Guinness World Records「Tallest mountain」：Mauna Kea 从海底基座到峰顶 10,205 m；USGS Mauna Kea 页：从海底基座量是地球最高的山（峰顶 4,207 m）。本榜第 1 名 6,879 m。 |
| 26 | 18 of these 50 volcanoes sit right on a national border. | 本表 §2：GVP 国家字段含两国的 18 座（Chile-Argentina 13、Chile-Bolivia 5）；不报国家总数，避免依赖 GVP 字段书写顺序（审片问题 8）。原：Chile 30 座，其中 18 座 GVP 国家字段为 Chile-Argentina（13）或 Chile-Bolivia（5）。 |
| 18 | Next: Sabancaya, the highest volcano on this list that erupted in 2026. | GVP Holocene 表 Last_Eruption_Year = 2026 的有 Sabancaya（5,960 m）、Láscar（5,592 m）、Popocatépetl（5,393 m）；Sabancaya 最高。GVP 周报 2026-01-08/14：IGP 报告持续喷发；2026-05 仍有爆炸与灰柱（秘鲁媒体 / VAAC，二手）。 |
| 9 | Chimborazo is only #8 here, yet its summit is the farthest point from Earth's centre. | 2016 年 2 月法国–厄瓜多尔联合测量（IRD / Géoazur 与厄瓜多尔 IGM），峰顶距地心 6,384.4 km，为地表离地心最远点（El Universo 2016-04-07；Wikipedia Chimborazo）。本榜按海拔排第 8。 |
| 3 | Both of the final two are active: each has erupted in the last 2,000 years. | 不点名（审片问题 7）。GVP：Ojos del Salado 最近喷发 750 CE（± 250 年，Eruption Dated）；Llullaillaco 1877（Eruption Observed），都在 2,000 年内。 |

## 5. 图片许可

找图过程（follow-up 016 / 023 与追加要求 3–5）：①每项内容先落盘 `_build/content/`；②Codex 联网搜两轮（`codex_b*.json`、`codex_bR1_*.json`，follow-up 023 起停用）；③Claude 自己搜：Pexels 网页搜索（`claude_pexels_all.json`）、Bing 图片全网检索（`claude_bing_all.json`）、低清项再全网升级一轮（`_build/upgrade/`）；Flickr 可商用搜索因限流降级，结果未采用；Openverse / Unsplash 搜索页被拦；④全网都没有可商用图的项，默认版用 Codex 生成图（`tools/codex_image.py`，prompt 在 `_build/gen_prompts/`）。不用维基共享资源与 GVP 图库（CC BY-NC）。
- 默认母版：AI 生成 31、Unsplash License 8、CC BY-SA 2.0 3、Public domain (NASA) 3、CC BY 2.0 2、Pexels License 2、CC BY 4.0 1。NASA 图为 ISS 宇航员 / Earth Observatory 公有领域照片（审片修复 4），按看图确定的火山位置裁切。
- `_with-risk-images` 版：风险图 32、Unsplash License 8、AI 生成 8、Pexels License 2（风险图 = 许可不明或来源页写明保留所有权利，或 Pixnio 不在白名单；须用户发布前签字）。
- 审片修复（2026-11-04）：#14 San José 改用 GVP 地质概述的 5,856 m 并重排；#25 Cordón de Puntas Negras 原风险图实为 Miscanti，已撤，两版都用生成图；Licancabur 换成以 Licancabur 为主体的 Pexels 图。
- 复核小修（2026-11-04）：ISS 俯视图认不出火山的卡改用地面实拍——#1 Ojos del Salado、#2 Llullaillaco、#5 Coropuna、#12 Aracar、#13 Guallatiri 用 Flickr CC BY / CC BY-SA 实拍（单线程、3 s 间隔检索，逐张看图认对）；#6 El Cóndor、#9 Pular 没找到地面实拍，默认版改回生成图；保留 NASA 的是 #7 Parinacota（斜视）、#40 Ubinas（喷发灰柱）、#48 Tata Sabaya（锥体 + 崩塌丘）。#4 Incahuasi、#23 Taapaca、#44 Isluga 的生成图重出（去掉村庄 / 教堂，外形按真山特征）。
- 逐张许可、作者、来源页见 `assets.json`；描述框署名由 `python -m rank_scroll publish` 生成。
- 许可分布：AI-generated (Codex image_gen) 32、unknown 18、todos los derechos reservados 13、Unsplash License 8、Public domain (NASA) 3、CC BY-SA 2.0 3、Pexels License 2、CC BY 2.0 2、Pixnio License 1、CC BY 4.0 1
