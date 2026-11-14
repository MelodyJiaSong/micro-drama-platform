# ep16 · 世界最大体育场 Top 50（按当前官方座位容量）

> 2026-11-03 代理起草（用户授权自主决策，**待用户点头**）。数据见 `data.json`，出处与判断依据见 `sources.md`，图片账本 `assets.json`；生成脚本与原始调研在 `_build/`（`research/{us,world}.json` 记了每座球场的全部版本数字）。

- 英文标题（≤60 字符）：**Top 50 Largest Stadiums in the World (2026)**（43 字符）
  - 屏上标题：Largest Stadiums in the World · kicker「TOP 50」· 统计行「Seated capacity · Official seats, Nov 2026」· 来源行「Sources: stadium, club & league official data; StadiumDB」
- 指标与口径：当前**官方座位容量**（seated capacity），2026 年 11 月为准（美国大学球场取 2026 赛季官方数；改建后以最新官方数为准）。收足球、美式足球、板球、橄榄球、盖尔式足球与多用途体育场；**不收**赛车场、赛马场，不收已拆除 / 关闭重建 / 在建 / 只部分重开的球场（Camp Nou）。站票区、临时看台和纪录上座不算（MCG 取 95,000 座位而非 100,024 总容量；Signal Iduna Park、Croke Park、Allianz Arena 按座位数跌出榜外）。同容量同名次。
- N / 每名秒数 / 预计时长：N = 50（47 个名次：82,000 两座并列 28，80,000 五座并列 36）。卡宽 720（体育场照片多为横幅），渲染器时间线约 **6:23**（intro_hold 2.5 s）（片头 5 s、滚动约 340 s 含 6 张洞察卡、冠军 6 s、计分板 7 s、来源 4 s、片尾 18 s）。
- 主源与交叉核对源（许可已核？）：
  - 主值：球场 / 大学体育部 / 俱乐部 / 协会官方页与官方文件（Georgia 2026 媒体指南的 SEC 与校园球场容量表、Ohio State 与 Wisconsin 2026 game notes、BCCI、MCG、Wembley、QFA、TFF、Luzhniki、Universitario、伊朗足协 2027 亚洲杯申办书、马来西亚体育场机构等）。官方页取不到的用 StadiumDB 或 Wikipedia 转引的官方文件（aggregator，共约 15 项，`sources.md` §5 逐条注明）。
  - 交叉核对：Wikipedia「List of stadiums by capacity」及各球场条目 infobox（只用事实）；差异与其他版本写进 `notes`。
  - 图片：代理自己检索（Flickr 公开搜索 + Bing 图片，可商用与放开许可两路，不用维基共享资源），逐张看候选拼图挑选。质量优先：最好的图许可不明就标 `licence unknown` 只进风险版，QC 第 1 轮后默认版：可商用实拍 41、AI 生成 6（3 张 FoP 国球迷示意 + 广东 / 杭州 / Atatürk 3 张球场外观）、无图卡 3（Misr、Borg El Arab、JIS）；风险版实拍 38 张须签字。
- 国家归属口径：球场所在地；计分板按国家。结尾揭晓预计 United States 25 > China 3 > Australia / Egypt / United Kingdom / Indonesia 各 2。
- 主题皮肤「arena」（渲染器已有）：深草坪绿底 `#061509 → #14421f`，强调色荧光青柠 `#c6ff3d`；主图 = 球场航拍 / 满场全景照片；tag 图标 `calendar`（开放年份）、`trophy`（主要运动）；国旗左上角原比例。
- 洞察卡（6 条，已写入 `data.json`，依据见 `sources.md` §6）：
  2. after 41：Five stadiums list a round 80,000 seats: in China, France, the USA and DR Congo.
  3. after 31：Missing: Camp Nou. Mid-rebuild it has 62,652 seats open; about 105,000 are planned.
  4. after 22：Next: Estadio Azteca, reopened in 2026: the first stadium to host three World Cup openers.
  5. after 11：8 of the top 10 are US college football stadiums. Not one is an NFL home.
  5b. after 5：Next: Beaver Stadium. On Oct 10, 2026, temporary stands let in a record 114,419 fans.（QC M3）
  6. after 3：North Korea hasn't published a seat count since its 2014 rebuild; 114,000 is an estimate.
  - 备选：Bernabéu's new capacity is a club secret: FIFA's 2030 file says 78,297；Camp Randall (76,130) beats Denver's Empower Field (76,125) for No. 50 by 5 seats；Nebraska's Memorial Stadium drops to about 65,000 in 2027 during a rebuild；Beaver Stadium may pass Michigan in 2026 with temporary seats (no official figure)。
- 竞品同题（YouTube 搜索「largest stadiums in the world」，2026-11-03 用 yt-dlp 取；发布日期被 YouTube 机器人验证拦住未取到）：
  - Gravity《Top 50 Biggest Football Stadiums in the World》https://www.youtube.com/watch?v=lPhGOdHO3aw — 445 万播放，5:36
  - Gravity《Biggest Stadium by Country》https://www.youtube.com/watch?v=ymJMQa7VjvU — 406 万，6:17
  - Real Data《Biggest Stadiums In The World》https://www.youtube.com/watch?v=1fdErLADErc — 245 万，2:42
  - StadiumDB《20 Biggest All-Seater STADIUMS in the World (2025 Update)》https://www.youtube.com/watch?v=DFc3FZgGWho — 15.6 万，11:16
  - 需求证据：同搜索前 15 条中位数 15.7 万、最高 445 万（`0_research/data/yt_demand_2026-11-03.jsonl`）。
  - 我们的差异：D1 每个数字有官方出处和统计期，按「座位」统一口径（竞品多混用含站票总容量、纪录上座和 150,000 旧数，例如五一体育场、MCG、Dortmund）；D2 标 2024–2026 的容量变化与新开 / 重开（Misr 2024、Azteca 2026、Bernabéu 改建、Ohio −739 等）；D3 国家计分板（美国 25 座的悬念）；D4 洞察卡讲口径背后的故事（赛车场、Camp Nou 缺席、五座并列 80,000、朝鲜估算）。竞品的「Top 50」只收足球场，本期收全部运动，美国大学橄榄球场是观众原本不知道的主角。
- 风险：
  1. **容量口径争议**：五一体育场是估算；Bernabéu、Beaver、Nebraska、Notre Dame、Borg El Arab 官方口径不一；评论区会有人拿 150,000、100,024、81,365 纠错——片头口径行和描述框 scope_note 已写「seated capacity」，sources.md 逐条列出其他版本。
  2. **第 50 名对 5 个座位敏感**（Camp Randall 76,130 vs Empower Field 76,125），发布前 7 天复核。
  3. **FoP**：9 座球场（南非、埃及 ×2、卡塔尔、印尼 ×2、法国、刚果（金）、伊朗）所在国无商用全景自由，原照只进 `_with-risk-images` 版；默认版的替代图见 `_build/handoff.md`。
  4. **图片许可**：默认版 39 张可商用实拍（CC BY / BY-SA / PD / Unsplash / Pexels，需署名的在 `publish.md` 描述框与置顶评论列全）+ 11 张 AI 生成示意图（上传勾选合成内容声明）；风险版 41 张实拍里 32 张许可不明，发布前须用户签字。
  5. **YPP 原创性**：同题百万播放竞品多；靠 D1 口径统一与 D4 洞察卡区分，旁白（D5）本期不加。

## 待用户确认

1. 主值口径用「座位」而不是含站票的总容量（影响 MCG 名次、Dortmund / Croke Park 入榜与否）。
2. Beaver Stadium 用 2025 官方 106,304，不用 2026 临时扩容的口头估计 108–109k。
3. Bernabéu 用 FIFA 申办书 78,297（排第 41），不用 LaLiga 2023 的 83,186（会排第 26）。
4. Camp Nou 不收（当前只开放 62,652 座）。
5. Clemson 81,500 含草坡座区，照官方数收录。
6. FoP 风险国 9 座球场的默认版替代图做法（见 handoff）。
