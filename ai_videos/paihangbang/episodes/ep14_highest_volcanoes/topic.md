# ep14 · 世界最高火山 Top 50（GVP Holocene 火山，按峰顶海拔）

> 2026-11-03 代理起草（follow-up 015 子代理，用户授权自主决策，**待用户点头**）。数据见 `data.json`，出处与核对见 `sources.md`，图片账本 `assets.json`；生成脚本在 `_build/`（`build.py` ← `items_def.py` + `raw/gvp_holocene.json`）。

- 英文标题（≤60 字符）：**Top 50 Highest Volcanoes in the World (2026)**（45 字符）
  - 屏上：Highest Volcanoes in the World · kicker「TOP 50」· 统计行「Summit elevation · Smithsonian GVP data, retrieved Nov 2026」· 来源行「Source: Smithsonian Global Volcanism Program (VOTW)」
- 需求证据：YouTube「largest volcanoes in the world」前 15 条中位数 72 万、最高 3,189 万（`0_research/data/yt_demand_2026-11-03.jsonl`）。
- 指标与口径：
  - **只收 Smithsonian GVP《Volcanoes of the World》Holocene 名单**（全新世约 11,700 年内有活动证据的火山，即通常说的「活火山或潜在活火山」，含 GVP 标 Evidence Uncertain 的条目）；按 GVP 给的峰顶海拔（m）排序，副显示 ft（× 3.28084 取整）。
  - GVP 的 Pleistocene 名单（更老、已熄灭的火山：Kilimanjaro 5,881、Sajama 6,542、Tupungato 6,570、Tres Cruces 6,620 及昆仑山的 Ulagh Muztagh / Bukadaban 等）**不收**；Monte Pissis（6,793 m）GVP 两张名单都没有，不收。理由：Holocene 名单是 GVP 的主表、口径清楚；混入 Pleistocene 名单会让前 50 被几十个无名的智利 / 玻利维亚古火山和「山体海拔不等于火山口海拔」的昆仑条目占满，Kilimanjaro 也只排第 47。洞察卡 1 直接回答「Kilimanjaro 去哪了」。
  - 海拔取 GVP 值（单一权威库、口径一致、可复现）；**唯一例外 San José**：WFS 字段 6,070 m 实为邻峰 Marmolejo，改用 GVP 同条目地质概述的 5,856 m（审片问题 1），排 #24；Wikipedia infobox / 导言值作交叉核对，写进 `cross_check`，差 ≥1% 的写进 notes（见 `sources.md` §3）。
  - 统计期：GVP WFS 2026-11-03 取数（`_build/raw/gvp_holocene.json`，1,214 座 Holocene 火山）。
- N / 每名秒数 / 预计时长：N = 50（无并列）；卡宽 720，每名约 6.3 s；洞察卡 6 张；`timeline` 实测 **6:20**。
- 主源与交叉核对源（许可已核？）：主值 Smithsonian GVP（事实数据，GVP 允许引用并注明出处）；交叉核对 Wikipedia（只用事实）；Peakbagger 未核（ep02 已知对脚本 403）。图片见 `assets.json`。
- 国家归属口径：**国旗 = GVP「Country」字段里的第一个国家**；跨境火山加 `SHARED WITH <第二国>` 徽章（共 18 座：智利–阿根廷 13、智利–玻利维亚 5）。GVP 对这些跨境火山一律把 Chile 写在前面，所以计分板 Chile 30 遥遥领先；洞察卡 3 说明其中 18 座在边境上。大洲字段按火山所在地填（Elbrus → Europe，Damavand → Asia，墨西哥 → North America，其余 South America）。
- 主题皮肤：`magma`（玄武岩黑 `#120706 → #3e120b`，熔岩橙强调色 `#ff5a1f`）；主图 = 火山实景满版（雪顶锥体、火山口、喷发烟柱）；标签：`calendar` 最近喷发（GVP Last Eruption Year），`mountain` 火山类型；徽章：SHARED WITH … / 2026 年有喷发的写 `ERUPTED IN 2026`（Sabancaya、Láscar、Popocatépetl）；计分板按国家。
- 洞察卡（6 条，审片后改写，已写入 `data.json`，均在 `sources.md` §4 核过；不提前点名冠军、不报国家总数）：
  1. after 43：No Kilimanjaro? It isn't on GVP's list of volcanoes active in the last 11,700 years.
  2. after 34：From the seafloor up, Hawaii's Mauna Kea stands about 10,200 m: taller than all of these.
  3. after 26：18 of these 50 volcanoes sit right on a national border.
  4. after 18：Next: Sabancaya, the highest volcano on this list that erupted in 2026.
  5. after 9：Chimborazo is only #8 here, yet its summit is the farthest point from Earth's centre.
  6. after 3：Both of the final two are active: each has erupted in the last 2,000 years.
  - 备选：Orizaba 的高度 GVP 5,564 m、Wikipedia 5,636 m——火山海拔各家差几十米；Llullaillaco 山顶 1999 年发现印加儿童木乃伊；Ojos del Salado 火山口附近有世界最高的湖之一。
- 竞品同题与差异：
  - Trend Max《THE BIGGEST VOLCANOES In The World》https://www.youtube.com/watch?v=8WsIqhkG8Ns ——约 197 万播放，10:02（按「最大」而非海拔，口径不明）。
  - Secret Truths《HIGHEST Volcanoes On Earth》https://www.youtube.com/watch?v=5DwD1PCsScc ——约 1.6 万播放，12:11。
  - GeologyHub《The Highest Volcano in the World; Chimborazo》https://www.youtube.com/watch?v=-zc536macQk ——约 3.4 万播放，4:23。
  - 发布时间：yt-dlp 被 YouTube「确认不是机器人」拦截，未取到（2026-11-03）。
  - 差异：D1 每个数字来自 GVP 并注明火山号与取数日期，口径（Holocene）在片头和描述框写清；D2 每张卡带最近喷发年份，2026 年仍在喷发的打 ERUPTED IN 2026；D3 国家计分板（智利压倒性领先，但 18 座在边境）；D4 洞察卡回答「Kilimanjaro 去哪了」「Mauna Kea 从海底量」「Chimborazo 离地心最远」。
- 风险：
  1. **口径争议**：观众会问 Kilimanjaro、Sajama、Pissis、Tupungato——洞察卡 1 + 描述框 scope_note 回答；用户若要改收 Pleistocene，见「待用户确认」1。
  2. **海拔分歧**：GVP 与 Wikipedia 差 ≥1% 的 5 座（San José 已按 GVP 地质概述改为 5,856 m，与 Wikipedia 一致；Guayaques −9.3%、Peinado +2.6%、Orizaba +1.3%、Damavand −1.1%、Ubinas +1.1%）；另 5 座（Pular、Olca-Paruma、Casiri、Yucamane、Corrida de Cori）Wikipedia 未给数值，只有 GVP 一源（`sources.md` §3）。按单一来源排，评论区纠错时可指向 GVP。
  3. **跨境火山国旗**：按 GVP 字段顺序，阿根廷、玻利维亚观众可能不满（Ojos del Salado 挂智利旗）。徽章写明共享。
  4. **图片**（复核后）：默认母版 = 实拍 19 张（Unsplash 8、Flickr CC 5、NASA 公有领域 3、Pexels 2、ESO CC BY 1）+ Codex 生成图 31 张（卡上黄色 AI IMAGE 徽章、署名「AI-generated image, not a photo」，来源卡与描述写明部分图为 AI 生成）。风险版不推荐发布。过程见 `sources.md` §5。

## 待用户确认

1. **只收 GVP Holocene 名单**（代理默认）还是 Holocene + Pleistocene？后者前 50 会混入约 20 座无名古火山，Kilimanjaro 第 47，昆仑山 Ulagh Muztagh（GVP 6,945 m，山体海拔）会成为第 1。
2. **海拔全部用 GVP 值**（代理默认），还是有国家测绘新值的（Chimborazo IGM 6,263、Orizaba INEGI、Damavand）逐条替换？替换会让排序依赖多源，第 50 名边界也会变（Ticsani 按 Wikipedia 5,408 m 会挤掉 Popocatépetl 5,393 m）。
3. **跨境火山国旗按 GVP 字段第一个国家**（代理默认，智利 30 座）；备选是按峰顶所在一侧逐座判定（多数峰顶就在国界线上，难以判定）。
4. **默认母版 31 张 AI 生成图是否可以接受**（复核后；其余 19 张为实拍），风险版不推荐发布（32 张许可不明 / 保留所有权利，复核结论「风险版必须修」，且复核小修后未重渲）。
5. Pixnio 图（#20 Miñiques，Pixnio License「free for personal and commercial use」）是否加进渲染器许可白名单；加了就能进默认版。

## 审片修复（2026-11-04，qc.md 第 1 轮）

- San José 改 5,856 m 并重排（原 #15–#24 上移一位，Sabancaya → #17，封面名次随之更新）。
- 洞察卡：冠军不点名；「Chile 30」改为「18 of these 50 volcanoes sit right on a national border」；Kilimanjaro 卡改为「不在 GVP 近 11,700 年活动名单上」。scope_note 写明跨境火山在计分板只按卡片国旗计一次、含 6 座 GVP 标为证据不确定的火山。
- 标签：Evidence Uncertain → 「Possible recent activity」；Olca-Paruma（GVP Eruption Observed、无年份）→「Eruption observed」。片头口径行改为「Active (Holocene) volcanoes by summit elevation」。
- 图：#1、#2、#5、#6、#7、#9、#12、#13、#40、#48 默认版改用 NASA 公有领域宇航员照片（ISS / Earth Observatory）；#25 原风险图实为 Miscanti，撤掉，两版都用生成图；#18 Licancabur 换成以它为主体的 Pexels 图；#11、#13、#42、#43 调裁切焦点。默认版 AI 图 39 → 29。

## 复核小修（2026-11-04，qc.md 文首复核段）

- #1、#2、#5、#12、#13 的 ISS 俯视图换成 Flickr CC 地面实拍；#6、#9 找不到地面实拍，默认版用生成图；#4、#23 Taapaca、#44 Isluga 生成图重出（无建筑）。默认版 AI 图 31 张。
- source_line 改为「Source: Smithsonian GVP (VOTW) · Some images are AI-generated」，来源卡和每帧底栏都显示；scope_note 补 San José 重音；publish 清单改为 AI IMAGE；只重渲默认版。
