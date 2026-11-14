# ep18 · 世界最快量产车 Top 28（按最高时速，区分实测与厂方宣称）

> 2026-11-03 代理起草（用户授权自主决策，**待用户点头**）。数据见 `data.json`，出处与判断依据见 `sources.md`，每项调研摘要见 `_build/content/`，生成脚本在 `_build/`（`items_def.py` → `build.py` → `gen_sources.py`）。

- 英文标题（≤60 字符）：**Fastest Production Cars in the World | Top 28 (2026)**（52 字符）
  - 屏上：标题 Fastest Production Cars in the World · kicker「TOP 28」· 统计行「Top speed · Data as of Nov 2026」· 来源行「Sources: maker releases; Racelogic, TÜV, Guinness, FMSCI timing; motoring press」
- 指标与口径：
  - 最高时速 km/h（副显示 mph）。只收**量产、可上路注册**的公路车：同规格客户车 ≥10 台，且 2026-11 前已开始交付。不收纯赛车 / 赛道车、一次性特制车、改装车、概念车和尚未交付的车。
  - **每个车型一张卡**，同车型多版本取最快的公路版本（Chiron 家族、Veyron 家族、Agera 家族、Nevera / Nevera R、Aventador 家族各算一个；Divo、Centodieci、W16 Mistral 单独命名销售，各一张）。
  - **VERIFIED**：独立第三方计时的最快**单向**速度（Racelogic、TÜV、Guinness、ATP、Dewesoft、FMSCI、Nardò、Johnny Bohmer Proving Grounds）；有双向平均的在 tag 写「2-way avg」。**CLAIMED**：厂方额定或厂方自测数字；设计目标与仿真不算。卡上 badge 写 VERIFIED / CLAIMED（新上榜加 NEW 2025）。
  - 入榜线：严格高于 350 km/h。实测 14 张、宣称 14 张。
- N / 每名秒数 / 预计时长：N = 28（25 个名次：18、23 两处并列）。卡宽 800（汽车照片多为横幅），每名约 6.7 s，前 10 名约 7 s；洞察卡 6 张；预计约 4 分钟（见 `timeline`）。
- 主源与交叉核对源（许可已核？）：
  - 主值：厂方新闻稿（BYD、Bugatti、Rimac、Koenigsegg、Mercedes-Benz、Chevrolet、Lamborghini、Aston Martin）与计时方 / 权威媒体报道（Top Gear、Motor1、Autoblog、Hagerty、Car and Driver、Road & Track、Autocar、Motor Authority、Hindustan Times / Autocar India）。只引事实。
  - 交叉核对：Wikipedia「List of production car speed records」及各车型条目（只作核对）。差异与原因逐条写在 `sources.md` §2。
  - 两项只有 aggregator 级来源（Dauer 962 Le Mans、Bugatti EB110 Super Sport），已在 notes 标出。
  - 图片：Claude 自己在 Flickr（只收 CC BY / BY-SA / CC0 / PDM）与 Pexels 找，许可照来源页写，见 `assets.json`。
- 国家归属口径：**品牌发源国**，集团归属写 notes。计分板按国家：United States 7 > France 6 > United Kingdom 4 > Sweden 3 = Germany 3 = Italy 3 > China 1 = Croatia 1。
- 主题皮肤「velocity」（渲染器已内置）：近黑底、赛车红强调色；主图 = 车辆真实照片（全车、四分之三前侧或正侧）；tag 图标用 calendar（纪录年份 / 车型年份）、ruler（双向平均）、users（产量）、trophy / flag（特殊说明）。
- 洞察卡（已定稿 6 条写入 `data.json`，均在 `sources.md` §4 核过）：
  1. after 26：Every speed here carries a label: 14 independently VERIFIED runs and 14 makers' CLAIMS.
  2. after 21：Just out: McLaren P1, Ferrari F80 and McLaren W1, all rated at exactly 350 km/h.
  3. after 15：Only 3 of these 28 cars are fully electric, and two set their records in 2025.
  4. after 10：Not ranked yet: the Bugatti Tourbillon (445 km/h claimed) isn't in customers' hands.
  5. after 6：Guinness wants a 2-way average. In our top 5 only the Tuatara and Agera RS have one.
  6. after 3：Where's the Jesko Absolut? Koenigsegg's 531 km/h is a simulation; it never ran flat out.
  - 备选：The Corvette ZR1 is the only car here built in the thousands；Hennessey's Venom F5 target is 311 mph, its best reported run is 271.6 mph；The McLaren F1 (1998) is still the fastest naturally aspirated car on the list。
- D2 变化信息：NEW 2025 三张（Yangwang U9 Xtreme 2025-09 新纪录登顶、Rimac Nevera R 2025-07、Corvette ZR1 2025 年款）；电动 3 / 28；「下一位」Tourbillon 与 Gemera 尚未交付。
- 竞品同题（需求证据 `0_research/data/yt_demand_2026-11-03.jsonl`，搜索「fastest cars in the world top 50」前 15 条播放中位数 35.9 万、最高 397 万）：
  - Trend Max《Top 10 FASTEST CARS In The World 2022》约 397 万播放（2022）。
  - Data Ball《Cars Top Speed Comparison | Fastest Car on Earth over 1200kmph》约 364 万（混入陆地速度纪录车、概念车）。
  - BYD Company《FASTEST CAR ON THE PLANET》约 348 万（厂方宣传片，只讲 U9 Xtreme）。
  - 差异：① D1 每个数字区分「独立实测」与「厂方宣称」、写出计时方和单向 / 双向，竞品普遍把目标值（Venom F5 311 mph、Jesko 531 km/h）当成真实速度；② D2 2025 新纪录与「尚未交付」的车；③ D3 品牌国家计分板（美国 7 张出人意料地多于法国）；④ D4 洞察卡解释 Guinness 双向规则与仿真值。
- 待用户确认：
  1. **入榜线与 N**：严格 >350 km/h 得 28 张，没有凑到 30。若想到 30+，可把「额定 350」并列收进来（会多出 6 张以上并列同名次），代理默认不收。
  2. **实测取单向最高**：与 Guinness 双向平均口径不同（Agera RS 显示 458 而不是常见的 447）；tag 已写双向平均。备选：一律显示双向平均（只有 5 辆车有），其余照单向。
  3. **预产 / 原型纪录车**：Chiron Super Sport 300+（预产车，客户车限速 440）、Yangwang U9 Xtreme（Wikipedia 称原型、单向）、McLaren F1（XP5 原型，转速限制放宽）按其纪录计；替代做法是这几辆改用客户车规格（Chiron 440、F1 约 356）。
  4. **未交付的车不收**（Tourbillon、Gemera、Aspark Owl），Jesko Absolut 因无官方数字不收。
  5. **国家按品牌发源国**：EB110（意大利制造）计法国、Pininfarina（总部慕尼黑、印度 Mahindra 所有）计意大利。
  6. Porsche 918 Spyder 以第三方实测 351.5 km/h 入榜（额定 345）；若只认额定，第 28 名去掉。
- 风险：
  1. 争议多：Yangwang「量产」资格、Chiron 300+ 预产车、Tuatara 2020 年作废的 331 mph 风波（本期只用 2021/2022 有 Racelogic 记录的数据）。评论区会争，好处是互动；描述框写清口径。
  2. 两项来源只到 aggregator（Dauer 962、EB110），发布前若能找到期刊原文再补。
  3. 图片：稀有车（Dauer 962 LM、Yangwang U9 Xtreme、SSC Ultimate Aero、Czinger）可商用实拍少，见 `_build/handoff.md`。
  4. 发布前 7 天复核：Tourbillon 是否开始交付、Jesko Absolut / Venom F5 是否完成实测、Yangwang 是否有新纪录。
