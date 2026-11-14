# ep20 · 世界最高瀑布 Top 35（按总落差）

> 2026-11-03 代理起草（follow-up 015 / 016，用户授权自主决策，**待用户点头**）。数据 `data.json`、出处与核对 `sources.md`、图片账本 `assets.json`；生成脚本与调研原料在 `_build/`（`build.py` 生成 data.json，`items_def.py` 定入选，`raw/` 存 WWD 与 Wikipedia 抓取，`content/` 是每条瀑布的内容笔记）。

- 英文标题（≤60 字符）：**Tallest Waterfalls in the World | Top 35 (2026)**（47 字符）
  - 屏上标题：Tallest Waterfalls in the World · kicker「TOP 35」· 统计行「Total height · Data as of Nov 2026」· 来源行「Sources: World Waterfall Database, Guinness, IGN Peru, USGS」
- 指标与口径：
  - **主值 = 总落差（total height）**，米，副显示英尺；从最高一级的顶到最低一级的底，含各级之间的急流段（WWD 定义）。标签里给最长单级落差（有数据时）。
  - **主源**：World Waterfall Database（WWD）「Overall Height」榜，2026-11-03 抓取前 105 条及每条瀑布页（`_build/raw/wwd_top.json`）。**有公开测量或权威记录的条目优先用它**：Angel Falls 用 Guinness 世界纪录的 979 m（1949 年测量），Yumbilla 用秘鲁国家地理研究所 IGN 2007 年激光测量的 895.4 m。Gocta（2006 年测量 771 m）、Yosemite（1913 年 USGS 测量 739 m）与 WWD 一致。
  - **入选规则**（一致执行）：① 有名字（WWD 里的 Unnamed 不收）；② WWD 状态为 Cataloged（WWD 实地勘测），或 Confirmed 且条目写明高度依据（测量、地形图分析或官方数值）；③ WWD 状态 Unconfirmed 的只在有独立权威测量 / 记录时收（Tugela：Guinness 采用 948 m；Yumbilla：IGN 2007）；④ 水被水电引走、基本断流的不收（Mongefossen 773 m、Brufossen 640 m）；⑤ 取 ≥ 631 m，第 35 名 Sentinel Fall，下一名 625 m，没有并列跨线。
  - 被规则排除、观众可能问到的：Tres Hermanas（秘鲁，914 m）、Olo'upena（夏威夷，878 m 估）、Haloku、Pu'uka'oku、Los Chorros de Cura 等为 WWD Unconfirmed 且无独立测量；Helgåfossen、Terror Falls、Brurasløret、Solitary Falls、Breiteigsfossen、Buskefoss 为 Confirmed 但条目只有一个数字、无任何依据；Mutarazi（津巴布韦）常见 762 m，WWD 现记 479 m（Unconfirmed），不论按哪种都不进。
  - **季节性（二选一：收，标徽章）**：WWD「Flow Consistency」< 12 个月，或 WWD / Wikipedia 写明只在融雪或雨季有水的，标 `SEASONAL`（14 条）；没有流量月数资料的不标，在 notes 写「flow months not documented」。水电调节、每年保证放水的 Mardalsfossen 标 `HYDRO-REGULATED`。
  - 并列：同值同名次（标准竞赛排名），同名次内按名称字母序（Kjeragfossen / Yutajé 22；Tågfossen / Ølmåfossen 24）。
- N / 每名秒数 / 预计时长：N = 35（可靠数据到 631 m 为止，不凑 40 / 50）；卡宽 600，每名约 5.3 s；洞察卡 5 张；timeline 实测 4:02（片头 5 s、滚动 202 s、冠军 6 s、计分板 7 s、来源 4 s、片尾 18 s）。
- 主源与交叉核对源（许可已核？）：
  - WWD 法律页（`/legal-disclaimer`，2026-11-03 读）：版权条款只针对照片（「All photographs … protected … may not be used … without written consent」），数据库文字与数值无专门条款。本期**只引事实数值**（高度、落差、流量月数），不搬运文字和照片；描述框写「Heights: World Waterfall Database」。
  - Guinness 世界纪录页（Angel 979 m / 807 m、Tugela 948 m 的说法）、MercoPress 2007（IGN Yumbilla 895.4 m）、USGS（Yosemite 2,425 ft）。
  - 交叉核对：Wikipedia「List of waterfalls by height」（rev 1379783845）及条目导语，只作核对。
  - 图片：Codex 联网搜索只跑了前 20 项（follow-up 023 起停用），其余由代理自己检索（Flickr CC、WebSearch、来源页）；找不到合格照片的用 Codex 生成（只做出图）。许可逐张记 `assets.json`，分布见 `_build/handoff.md`。
- 国家归属口径：瀑布所在地。留尼汪的两条（Trou de Fer、Cascade Blanche）计 France，subtitle 写 Réunion，大洲记 Africa（只作字段，计分板按国家）。
- 主题皮肤：`cascade`（渲染器已加）——深苔绿底 `#0a1f1a`、雾白 / 水绿强调；主图类型：竖幅瀑布实景照片，整条从顶到底尽量可见；主题图标 `ruler`（落差）、`stairs`（级数）、`calendar`（流量季节 / 测量年份）、`mountain`（冰川 / 山）、`map-pin`；国旗：左上角原比例。计分板：按国家（结尾 Norway 11 > United States 10 > Venezuela 3 = New Zealand 3 > …）。
- 洞察卡（5 条，已写入 data.json，均在 `sources.md` §4 核过）：
  1. after 30：SEASONAL = it flows only part of the year, fed by snowmelt or rainy-season runoff.
  2. after 21：Zimbabwe's Mutarazi is often listed at 762 m, but World Waterfall Database estimates ~479 m.
  3. after 12：Norway's Mongefossen (773 m) would rank here, but hydropower has kept it dry since 1977.
  4. after 4：Next: a Swiss fall that grew 90 m in 2020, when canyoneers abseiled down and measured it.
  5. after 2：Angel's 979 m adds rapids below its 807 m drop. Drop those and Tugela (948 m) wins.
  - 备选：Gocta was unknown to the outside world until a 2006 survey measured 771 m；Hawaii's Olo'upena (878 m est.) is left out: its height has never been confirmed；Browne Falls is listed at 619 m in older sources but 836 m on topo maps；Tugela was measured at 983 m by a Czech team in 2016, but from 1 km downstream。
- 竞品同题（yt-dlp 搜索 2026-11-03，`_build/raw/yt_search_waterfalls_2026-11-03.jsonl`；YouTube 拦了逐条详情，发布时间未取到）：
  - MetaBallStudios《WATERFALLS HEIGHT in perspective》https://www.youtube.com/watch?v=oPSHg0oJpX4 — 约 36.6 万播放，3:17（3D 比例动画）。
  - List Data《Tallest Waterfalls From Different Countries》https://www.youtube.com/watch?v=kc825zy1YWI — 约 6.8 万，6:13。
  - Aesthetic Data《50 Tallest WATERFALLS In The World 2025.》https://www.youtube.com/watch?v=jD7IjwVrwxc — 约 3,100，7:36（同模板跟拍频道）。
  - 需求证据：「tallest waterfalls in the world」前 15 条中位数 6.2 万、最高 657 万（`0_research/data/yt_demand_2026-11-03.jsonl`）。
  - 我们的差异：D1 每个数字有出处（WWD 条目 / Guinness / IGN），并写出谁测的、怎么测的；D2 讲变化与修正（Mattenbach 2020 年绳降实测 +90 m、Mongefossen 1977 年断流、Mutarazi 被下调、Sprænefossen 从 850 m 修到 700 m）；D3 国家计分板挪威 vs 美国 11:10 的悬念；D4 洞察卡讲「Angel 还是 Tugela」之争。竞品大都照搬 Angel 979 / Tres Hermanas 914 / Olo'upena 900 的旧榜，我们明确不收未证实高度。
- 风险：
  1. **冠军争议**：WWD 认为 Angel 只该算 807 m、Tugela 才是第一。本期按「公开测量 / 记录优先」用 979 m 并标 HEIGHT DISPUTED、洞察卡说明。评论区会有人站 Tugela——好处是互动。
  2. **知名瀑布缺席**：Tres Hermanas、Olo'upena 常在别家榜单前五，这里因高度未证实而不收，scope_note 与置顶评论写明。
  3. **冷门瀑布多、照片难找**：约三分之一条目几乎没有公开照片（Cloudcap、Seahpo、Isella、Cabin Boy、Ägertenbach…），按 follow-up 016 用 Codex 补搜，仍无可用图的用 AI 生成图并在 publish.md 声明。
  4. **WWD 是私人网站**（aggregator 级）：多数高度来自地形图估算，片头口径行与描述框写「mostly topographic estimates」。
  5. 发布前 7 天内复核 WWD 榜单（Tugela 页 2026-10-17 刚更新、Vinnu 页 2026-10-13 更新）。

## 待用户确认

| # | 事项 | 代理默认 |
|---|---|---|
| 1 | 冠军：Angel 979 m（Guinness）还是按 WWD 只算 807 m（那样 Tugela 第一、Angel 按本期入选规则排第 10） | 用 979 m，徽章 HEIGHT DISPUTED，洞察卡 5 说明 |
| 2 | 只收「有依据」的条目，排除 Tres Hermanas、Olo'upena 等 Unconfirmed 估值 | 排除；如要收，可加 UNCONFIRMED 徽章另做版本（N 约 42） |
| 3 | 季节性瀑布：收并标 SEASONAL（14 条） | 收 |
| 4 | N = 35（≥ 631 m）而非 40 / 50 | 35；放宽到 610 m 会出现 4 条并列、多为估值区间很宽的条目 |
| 5 | 留尼汪计 France | 是 |
