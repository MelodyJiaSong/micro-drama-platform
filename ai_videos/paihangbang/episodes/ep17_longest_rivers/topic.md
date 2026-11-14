# ep17 · 世界最长河流 Top 50（按长度排序，Britannica 统一口径）

> 2026-11-03 代理起草（用户授权自主决策，**待用户点头**）。数据见 `data.json`，出处与判断依据见 `sources.md`，图片账本 `assets.json`；生成脚本在 `_build/`（`items_def.py` → `build.py` → `gen_sources.py`）。

- 英文标题（≤60 字符）：**Top 50 Longest Rivers in the World (2026) | Nile vs Amazon**（58 字符）
  - 屏上标题：Longest Rivers in the World · kicker「TOP 50」· 统计行「Length · Data as of Nov 2026」· 来源行「Sources: Encyclopaedia Britannica, Geoscience Australia」
- 指标与口径：河长，km（副显示 mi）。**主值一律取 Encyclopaedia Britannica 公布值**——Britannica 给出「从最远源头量起」的水系长度时取水系值（Mississippi–Missouri 5,971、Ob–Irtysh 5,410、Yenisey–Angara–Selenga 5,539 等），否则取该河长度；Murray–Darling 取 Geoscience Australia 水系值 3,672 km（Britannica 无水系值）。已在更长水系主线上的河不单列（Missouri、Irtysh 等），大支流照列（Madeira、Purus、Ubangi…）。统计期：2026-11-03 取数。
- N / 每名秒数 / 预计时长：
  - N = 50（Rio Negro 与 Ubangi–Uele 同为 2,250 km 并列第 46）。
  - 卡宽 720：50→11 名每名约 6.3 s；洞察卡 6 张；片头 5 s，冠军停留 6 s，大洲计分板 7 s，来源卡 4 s，片尾 18 s。
  - `timeline` 实测 **约 6:20**（380 s）。
- 主源与交叉核对源（许可已核？）：
  - 主值：Encyclopaedia Britannica 各河条目（britannica.com 直连被 Cloudflare 拦，经 web.archive.org 2025–2026 快照取原文，`_build/raw/brit/`）；Britannica「World's longest rivers」表（前 15）；Geoscience Australia「Longest Rivers」（Murray–Darling）。只用事实数字、不搬文字。
  - 交叉核对：Wikipedia「List of river systems by length」（revid 1380355572，逐行解析 `_build/raw/wp_rows.json`）；前 10 名再对 Liu et al. 2009（Int. J. Digital Earth，卫星+实地，Zenodo 全文 `_build/raw/liu2009.pdf`）；Amazon 对 INPE 2008（FAPESP 报道、Britannica 专文）；Danube 对 ICPDR；Mekong 对 MRC/FAO。Wikidata P2043 作补充（`_build/raw/wd_rivers_2026-11-03.json`）。
  - 图片：Codex 联网搜索（不用维基共享资源），见 `assets.json` 与 `_build/handoff.md`。
- 国家归属口径：**河口所在国**（入海、入湖或汇入更大河流处）；河口在两国界上时取两国中流域面积较大的一国。所以 Nile → Egypt、Ganges / Brahmaputra → Bangladesh、Colorado → Mexico、Rio Grande → United States（徽章 US–MEXICO BORDER）。大洲按河口：Asia 20、South America 12、North America 7、Africa 6、Europe 4、Oceania 1。
- 徽章：BASIN: 11 COUNTRIES（Nile）、LENGTH DISPUTED（Amazon）、THROUGH 10 COUNTRIES（Danube）、THROUGH 6 COUNTRIES（Mekong、Zambezi）、RUSSIA–CHINA BORDER（Amur）、US–MEXICO BORDER（Rio Grande）——均有 Britannica 原文支持。标签：入海 / 汇入处（map-pin），支流另标「Amazon tributary」等（globe），各洲之最（trophy）。
- 主题皮肤「delta」（渲染器 `theme.py` 已有）：深河口蓝背景 `#081a26 → #1d5066`，强调色水蓝 `#4fc3f7`；主图为标志性河段实景横幅照片（卡宽 720，焦点居中）；图标 map-pin / globe / trophy；国旗左上角压在照片上。
- 洞察卡（6 条，已写入 `data.json`，均在 `sources.md` §5 核过）：
  1. after 44：Next: the Colorado. Dams and farms now take so much water it rarely reaches the sea.（D2 变化）
  2. after 38：Next: the Ganges. It meets the Brahmaputra in Bangladesh and they share one huge delta.
  3. after 29：Next: the Danube. It flows through 10 countries on its way to the Black Sea.
  4. after 21：The next 3 rivers are only tributaries of the Amazon, yet each is longer than the Danube.（反常识）
  5. after 13：Britannica gives the Mekong 4,350 km. A 2009 satellite survey measured 4,909 km.（D2 新测量 / D1 口径）
  6. after 2：In 2008 Brazil's INPE measured the Amazon at 6,992 km. Is the Nile really No. 1?（Nile vs Amazon 之争）
  - 备选：Amazon 携带地表径流约五分之一（Britannica）；Irtysh 4,248 km 比它汇入的 Ob 3,650 km 还长；Mississippi 本身 3,766 km，加 Missouri 才 5,971；Syr Darya 改道灌溉导致咸海萎缩；Yenisey 水系穿过贝加尔湖。
- 竞品同题（yt-dlp 搜索 2026-11-03，`_build/raw/yt_search_rivers_2026-11-03.jsonl`；发布时间 YouTube 要求登录未取到）：
  - Aesthetic Data《50 Longest Rivers Around The World 2026.》https://www.youtube.com/watch?v=Ocu-dNUEbe0 — 6.9 万播放，7:25。
  - RealLifeLore《Why Nobody Knows the World's Longest River》https://www.youtube.com/watch?v=litMp_GGOAc — 258 万，14:44（解说类，非榜单）；Atlas Pro《What's the Longest River on Earth?》288 万（需求数据）。
  - 其他榜单滚动类多为几十到几百播放（TDR World Ranking Top 50 522；Data Smash 253；Epic Stats 121）。需求：「longest rivers in the world」前 15 条中位数 13.7 万、最高 288 万（`0_research/data/yt_demand_2026-11-03.jsonl`）。
  - 差异：D1 每个数字一个出处（Britannica 原文 + 交叉核对，描述框附来源），统一口径而不是混用各处最大值；D2 洞察卡讲新测量与变化（INPE 2008、2009 卫星测量、Colorado 断流）；D3 大洲计分板（Asia 20 vs South America 12）；D4 把「长度到底怎么量」这件观众最爱吵的事讲清楚（LENGTH DISPUTED 徽章、Nile vs Amazon 压轴洞察）。
- 风险：
  1. **数值争议**：11 条与 Wikipedia 列表或 Liu 2009 差异 > 10%（Zambezi、Juruá、Orinoco、Brahmaputra、Euphrates、Tocantins、Salween、Irrawaddy、Colorado、Amur、Mekong），见 `sources.md` §3。最可能被评论区挑的是 **Zambezi 3,540 km**（常见值 2,574–2,740）和 **Orinoco 2,740**（常见 2,140）。按「统一 Britannica」保留，描述框写明口径；评论区可直接指向来源。
  2. **国旗**：河口规则让 Ganges / Brahmaputra 显示孟加拉国旗、Nile 显示埃及、Colorado 显示墨西哥——可能引来「应该是 India」类评论；口径行和描述框写明「Flag = country where the river ends」。
  3. **可能遗漏**：Songhua（经嫩江 2,309）、Pearl–Xi（2,214）、Red River (US)（2,188）没取到 Britannica 值（快照 404、搜索额度用尽），按维基值会进 44–49 名；按 Britannica 其他条目量级多半在 2,100 以下。见 `sources.md` §4。
  4. **图片**：西伯利亚 / 亚马孙小支流可商用实拍稀少。默认母版 42 张可商用实拍 + 8 张 AI 生成图（Purus、Lower Tunguska、Ubangi、Madeira、Japurá、Vilyuy、Olenyok、Kasai），无占位卡；风险版另放 12 张许可不明实拍。详见 `_build/handoff.md`。
  5. 发布前 7 天复核：Britannica 条目改动（尤其 Amazon / Nile 争议段落）。

## 待用户确认

| # | 事项 | 代理默认 |
|---|---|---|
| 1 | 长度口径：统一 Britannica（一致、可追溯）vs 逐条取「最常见值」 | 统一 Britannica；差异 > 10% 的 11 条写 notes |
| 2 | Zambezi 3,540 km（Britannica）明显高于常见 2,574–2,740 | 保留 Britannica；若改 2,740，Zambezi 降到约第 34，其后名次顺移 |
| 3 | 国旗：河口所在国 vs 流域最大国 | 河口所在国（Nile → Egypt，Ganges → Bangladesh） |
| 4 | Songhua / Pearl / Red River (US) 未收 | 不收（无 Britannica 值）；如收，Kasai、Irrawaddy、Dnieper 出榜 |
| 5 | 边界河口归属（Congo、Rio Grande、Ubangi、Paraguay、Pilcomayo） | 两国中流域较大者；Paraguay / Pilcomayo 未单独核实 |


## 2026-11-04 QC 后修订

补收 Araguaia（#32）；Zambezi 改 2,574 km、Orinoco 改 2,140 km 出榜（离群值例外规则）；屏上写明「Flag = where the river ends」、国家行「ENDS IN …」；Indus 换巴基斯坦境内图；intro_hold 2.5。上表「待用户确认」第 2 项已按主代理决定处理（Zambezi 改通行值）。详见 `_build/handoff.md` 末节、`sources.md` §1。
