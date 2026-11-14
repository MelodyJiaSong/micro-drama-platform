# ep12 · 世界面积最大的国家 Top 50（总面积 = 陆地 + 内陆水域）

> 2026-11-03 代理起草（用户授权自主决策，**待用户点头**）。数据见 `data.json`，出处与判断依据见 `sources.md`，图片账本 `assets.json`；脚本与原始文件在 `_build/`（交接说明 `_build/handoff.md`）。

- 英文标题（≤60 字符）：**Largest Countries in the World by Area | Top 50 (2026)**（54 字符）
  - 屏上：标题 Largest Countries in the World by Area · kicker「TOP 50」· 统计行「Total area (land + inland water) · UN Demographic Yearbook 2024」· 来源行「Sources: UN Demographic Yearbook 2024, CIA World Factbook」
- 指标与口径：每个主权国家的**总面积**（surface area = 陆地 + 湖泊、河流等内陆水域），km²，副显示 sq mi。主值取 UN DYB 2024 Table 3 的「Surface area 2024」列（各国报给 UN 的官方数；Sudan 缺值，改用 World Bank / FAO 2024）。不计：南极领土主张、UN 单列的属地（格陵兰、法属海外大区、西撒哈拉等）。
- N / 每名秒数 / 预计时长：N = 50（无并列）；卡宽 720，每名约 6.3 s；洞察卡 6 张；片头 5 s、冠军 6 s、计分板 7 s、来源 4 s、片尾 18 s。`timeline` 实测 **约 6:20**。
- 主源与交叉核对源（许可已核？）：
  - 主值：UN Statistics Division *Demographic Yearbook 2024*, Table 3（事实数据，注明出处；PDF 存 `_build/raw/`）。
  - 交叉核对：CIA World Factbook 最终版（2026-02 停刊，用 `factbook/factbook.json` 2026-01-22 最后同步，公有领域）；World Bank WDI AG.SRF.TOTL.K2 / AG.LND.TOTL.K2 2024（CC BY 4.0）只作参考——其 2024 面积序列有明显异常（Canada 15.6M、Norway 62 万等），不宜作主源。
  - 差异 > 1% 的 7 项（Saudi Arabia、Libya、Iran、Venezuela、South Sudan、Kenya、France）逐条写进 notes 与 `sources.md` §2；其中 Venezuela/Nigeria、South Sudan/Afghanistan、Kenya/Madagascar/Botswana 的先后随来源变。
- 国家归属口径：主权国家（系列惯例，Wikidata 主权国家含台湾；台湾 36,197 km² 不入前 50）。**争议地区按各国报给 UN 的标准口径**：印度含其主张的全部克什米尔，巴基斯坦不含其管辖的 AJK / 吉尔吉特-巴尔蒂斯坦；乌克兰按国际承认边界（含克里米亚）、俄罗斯不含；西撒哈拉单列，不计入摩洛哥；法国只算本土 + 科西嘉。卡上用徽章标出：India「INDIA'S OFFICIAL AREA」（QC 后改，避开 claimed）、Ukraine「RECOGNISED BORDERS」、France「EXCL. OVERSEAS REGIONS」、Sudan「SPLIT IN 2011」、South Sudan「INDEPENDENT 2011」。大洲按 UN M49 区域（Russia → Europe；Kazakhstan、Türkiye → Asia；Egypt → Africa）。
- 主题皮肤「atlas」（渲染器 `theme.py` 已加）：深林绿背景 `#0e2116 → #2c5136`、地图金强调色 `#e9c46a`；主图 = 每国一张**最有代表性的自然风光 / 标志性地貌**（地名写在卡上的地点行），尽量避开现代建筑（无 FoP 风险）；少数为古迹（Machu Picchu、Meroë 金字塔、Bagan）也无版权问题；主题图标 `globe` / `trophy` / `ruler` / `flag`；国旗左上角大国旗；计分板按大洲。
- 洞察卡（6 条，已写入 `data.json`，出处见 `sources.md` §3）：
  1. after 41：Next: South Sudan, the world's newest country. Its 2011 split took a quarter of Sudan.（D2 变化）
  2. after 32：Next: Venezuela, just 5,922 km² ahead of Nigeria in UN data. Other atlases flip them.（D1 来源分歧）
  3. after 21：Next: Chad and Peru, only 1,216 km² apart. That's barely bigger than Hong Kong.
  4. after 14：Greenland (2.17M km²) is self-governing and listed apart from Denmark; alone it'd be 13th.
  5. after 4：By land alone, China (9.33M km²) beats the US (9.15M km²), and Canada falls to 4th.（口径变化 → 名次变化）
  6. after 2：Next: Russia. Often called bigger than Pluto, it isn't: Pluto's surface is ~17.7M km².（反常识）
  - 备选：Algeria became Africa's largest only in 2011；Australia's Antarctic claim (5.9M km²) is not counted（已做成 Australia 卡的标签）；With Western Sahara, Morocco would rank 39th；Libya's area differs by 5% between UN and CIA data。
  - 卡片标签（D2）：Canada「By land only: #4」、China「By land only: #2」、Canada / US 水域占比、各洲最大与内陆国之最等。
- 竞品同题（链接、播放、发布时间）与我们的差异：
  - 需求证据：搜索「largest countries by area comparison」前 15 条播放中位数 154 万、最高 2,010 万（`0_research/data/yt_demand_2026-11-03.jsonl`）。
  - KLT《Country Size Comparison and Universe Size Comparison》https://www.youtube.com/watch?v=AGOwyVC3IA4 — 约 2,010 万播放，8:13；LeeZY Comparisons《Country Size Comparison All 195 Countrys》https://www.youtube.com/watch?v=76ksG4F9zAI — 约 1,532 万，6:24；Gravity《Country Size Comparison》https://www.youtube.com/watch?v=64t75CyQhmY — 约 1,200 万，13:36。同格式 Top 50：claireity《Top 50 Biggest Countries》16 万（0:52）、CountryBall Factory《Biggest Countries in the World 2026 – Top 50》0.6 万（8:02）。发布时间未取到（yt-dlp 单视频元数据请求失败，`_build/raw/yt_search_area.jsonl` 只有搜索结果）。
  - 差异：① D1 每个数字注明 UN DYB 2024 出处并与 Factbook 交叉核对，主动指出来源分歧（Venezuela/Nigeria 洞察卡、notes）；② 口径透明：争议地区、南极主张、海外属地用徽章与 scope_note 讲清；③ D2 用「换口径名次就变」（陆地 vs 总面积、South Sudan 分家）代替同比；④ 每张卡一张该国标志性风景，不是地图形状对比（竞品主流是 3D 地图 / 形状叠放），画面观感完全不同。
- 风险：
  1. **争议领土**（克什米尔、克里米亚、西撒哈拉、阿卜耶伊）会引来评论区争吵；按 UN 标准口径并在卡上和描述框写明，评论可直接指向 `sources.md`。
  2. **来源分歧**：Libya（UN 168 万 vs CIA 176 万）、Saudi Arabia、South Sudan、Kenya、Venezuela 差 2–5%；采用 UN 并在 notes 写明。
  3. **France 名次**（第 48，本土 vs 含海外大区约第 42）、**Morocco 是否计入西撒哈拉**（计入则第 39）是最可能被质疑的两处，见「待用户确认」。
  4. 冷门国家的风景照片少。结果：默认母版 49/50 张可商用照片（Pexels / Unsplash / CC BY / CC BY-SA / NASA），#43 Central African Rep. 找不到任何可商用图 → 默认版用 AI 生成的雨林瀑布图（主代理决定）；风险版 50/50（4 张许可不明或非商用：Angola、Venezuela Angel Falls、South Sudan、CAR）。因找不到可用图而换了题材的：Libya（绿洲航拍）、Iran（Damavand）、Niger（Agadez 大清真寺）、Mali（巴马科尼日尔河）、Ethiopia（Simien 狮尾狒）、Mozambique、Somalia、Mauritania（Richat，NASA）。详见 `_build/handoff.md`。

## 待用户确认（代理默认，可改）

| # | 事项 | 代理默认 |
|---|---|---|
| 1 | 主源 | UN DYB 2024（各国官方数）；Factbook 交叉核对；World Bank 2024 因口径异常只作参考 |
| 2 | France | 只算本土 + 科西嘉（551,500，第 48），徽章 EXCL. OVERSEAS REGIONS；若要含海外大区（643,801）则升到第 42 |
| 3 | 西撒哈拉 | 按 UN 单列，不计入 Morocco（Morocco 不进榜）；若计入则 Morocco 第 39、Thailand 掉出 |
| 4 | 克什米尔 | India 用含主张地区的官方数（徽章 INCL. CLAIMED AREAS），Pakistan 用不含 AJK/GB 的官方数；两国名次不受影响 |
| 5 | Ukraine / Russia | 国际承认边界（徽章 RECOGNISED BORDERS 放在 Ukraine 卡） |
| 6 | Sudan 缺 UN 值 | 用 World Bank / FAO 1,878,000（Factbook 1,861,484，差 0.9%，名次不变） |
| 7 | 标题年份 | 「(2026)」对应 UN DYB 2024（2025-26 发布）；屏上统计行写数据来源年份 |
