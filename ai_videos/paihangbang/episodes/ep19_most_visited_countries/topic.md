# ep19 · 世界最受欢迎旅游国家 Top 50（2024 年国际入境过夜游客数）

> 2026-11-03 代理起草（follow-up 015 / 016，用户授权自主推进，**待用户点头**）。数据见 `data.json`，逐条出处 `sources.md`，生成脚本 `_build/`（`items_def.py` → `build.py` → `gen_sources.py`），调研原料 `_build/research/`、`_build/raw/`。

- 英文标题（≤60 字符）：**Most Visited Countries in the World | Top 50 (2026)**（51 字符）
  - 屏上：标题 Most Visited Countries in the World · kicker「TOP 50」· 统计行「International tourist arrivals · Data: 2024 full year」· 来源行「Sources: UN Tourism, national tourism statistics」
  - 标题年份 (2026) 写发布年，屏上与描述框写清「2024 full year」（与 bible §3.3「标题年份写统计期」有出入，见文末待确认 1）。
- 指标与口径：**国际入境过夜游客数（international tourist arrivals, overnight visitors），2024 全年，单位百万人次**。
  - 主源：UN Tourism Statistics Database（2025-12 批量下载，`_build/raw/UN_Tourism_inbound_arrivals_12_2025.xlsx`，序列 INBD_TRIP_TOTL_TOTL_TOUR）。数据库有 2024 值的 30 国直接用（澳大利亚用 VSTR，见 sources.md）。
  - 数据库缺 2024 的 20 国（法、土、希、泰、奥、马来、荷、越、摩、克、埃、捷、瑞士、突、瑞典、柬、挪、爱、哥伦比亚、菲律宾）用**本国官方同一序列**：先看数据库 2019 值与哪个国家序列吻合（「2019 指纹」），再取该序列的 2024 值。详见 `_build/research/brief_research.md` 与三组调研 JSON。
  - 为什么用 2024 不用 2025：UN Tourism 已发布 2025 全球总数（1.52 亿增长 4%），但截至 2026-11 法国、英国、德国、葡萄牙等的 2025 国别值仍缺；数据库批量版只到 2024。
  - **UN Tourism 本身就是混合口径**：有的国家边境计数（TF），有的按住宿登记的外国客人到达（TCE，每次入住都计，德、奥、荷、克、瑞士、比、瑞典、挪），越南、罗马尼亚、哈萨克斯坦、乌兹别克斯坦含当日往返（VF），摩洛哥、突尼斯、哥伦比亚、土耳其含本国海外侨民。本期照 UN Tourism 的选择，不自行换算；口径特殊的卡在信息行用小标签注明（Counted at lodgings / Incl. same-day visits / Incl. 8.6M diaspora…），片头口径行与描述框 scope_note 写明。
  - **D2 变化**：每张卡主数值右侧显示与 2019（疫情前）**同一序列**的变化 ▲▼%；序列断档的巴林、爱尔兰改与 2023 比（卡上写 vs 2023）。印度（数据库 2019 含海外印度人）、葡萄牙（数据库 2019 是住宿口径）用官方同口径 2019 值重算。
  - **未入榜（缺 2024 同口径值，不硬补）**：中国（文旅部 2020 年后只公布含一日游的「入境游客」，2024 为 1.319 亿人次；维基常见的 64.9M 实为移民局「外国人出入境合计人次」，误用）、阿联酋（只有迪拜 18.72M，全国外国住客无公开值）、丹麦（2019 的 14.7M 对不上任何官方序列）、保加利亚、俄罗斯。另波多黎各（5.55M，美国属地、游客几乎都是美国本土居民）不列入「国家」榜。这些写进 scope_note 和洞察卡 3（中国）。
- N / 每名秒数 / 预计时长：N = 50（第 50 名菲律宾 5.95M——主代理在搜索额度恢复后核到 DOT 5,949,350，进榜并把智利 5.24M 挤到第 51）；卡宽 720，每名约 6.7 s；洞察卡 5 张；渲染器时间线 **约 6:15**（片头 5 s、滚动 335 s、冠军 6 s、计分板 7 s、来源 4 s、片尾 18 s）。
- 主源与交叉核对源（许可已核？）：
  - UN Tourism Statistics Database：© UN Tourism，数据事实引用并注明出处（只用数字，不搬表）。OWID 转载版（UN Tourism 2025，CC BY 处理）作为下载核对：`_build/raw/owid_international-tourist-trips_2026-11-03.csv`，与批量版 TOUR 序列一致。
  - 本国官方：INE、Banca d'Italia、Statistik Austria、CBS、DZS、CZSO、JNTO、Tourism Malaysia、泰国旅游体育部、越南统计局、柬埔寨旅游部、CSO Ireland、MinCIT、Eurostat tour_occ_arnat（瑞士 / 瑞典 / 挪威住宿口径）等，逐条见 `sources.md`。
  - **交叉核对不全**：本会话 WebSearch 额度（10 个代理共用）中途用完，额度恢复后主代理补核了墨西哥、香港、澳门、巴西、台湾、多米尼加、南非、澳大利亚；加拿大（StatCan 只给含当日的 29.8M）、阿根廷、印尼、哈萨克斯坦、乌兹别克斯坦、巴林等仍只有 UN Tourism 数据库一个来源（UN Tourism 本身是各国官方报送）；`sources.md` 标「未核到」，发布前 7 天复核时补。
- 国家归属口径：每个国家 / 地区一张卡，按 UN Tourism 的报告单位；香港、澳门按 UN Tourism 单列，badge「SAR OF CHINA」；台湾按系列惯例写 "Taiwan"（UN 名称 Taiwan Province of China）。大洲按 UN M49：土耳其（Western Asia）、哈萨克斯坦、乌兹别克斯坦、巴林、沙特计入 Asia；墨西哥、多米尼加计入 North America。计分结果 Europe 20 / Asia 18 / Africa 4 / North America 4 / South America 3 / Oceania 1。
- 主题皮肤「voyage」（渲染器已加，暮光紫底 + 珊瑚橙强调）：
  - 主图类型：每国一张辨识度最高、色彩好的**标志性景点**照片（`_build/landmarks.py`：优先自然景观或古迹，避开受版权保护的现代建筑——阿联酋、卡塔尔不用现代地标；巴西用糖面包山而不是基督像；马来西亚用京那巴鲁山而不是双子塔）。**找图（follow-up 023）**：不再用 Codex；第 1–40 名保留此前 Codex 联网搜到的候选（2–3 张 / 项），其余候选由 Claude 子代理用 WebFetch / WebSearch 在 Unsplash / Pexels / Pixabay / Flickr CC 补齐到每项 ≥ 6 张，横幅风景为主，卡宽 720。
  - 国家卡解剖：国家行写所在地区（如 WESTERN EUROPE）→ 名称写国名 → 大号数值（百万）→ 右侧 ▲▼% vs 2019；信息行 = 📍景点名 + 口径小标签。
  - 计分板：按大洲累计上榜国家数。
- 洞察卡（已定稿 5 条，均可由 `sources.md` 支持）：
  1. after 41：Taiwan is still 34% below its 2019 level, the biggest shortfall in this Top 50.
  2. after 31：Albania (#32) nearly doubled since 2019 (+87%), the fastest growth on this list.
  3. after 21：China isn't ranked: it hasn't published 2024 overnight arrivals. In 2019: 65.7M.
  4. after 11：Saudi Arabia (#13) has 70% more visitors than in 2019, the fastest rise in the top 15.
  5. after 4：Türkiye (+18%) has overtaken Italy (-11%) since 2019 to take No. 4.
  - 备选：Morocco's 17.4M includes 8.6M Moroccans living abroad; foreigners alone: 8.8M. / Greece is often quoted at 40.7M, but that counts 5M cruise passengers. / Hong Kong had 44.5M visitors, but only 21.9M stayed the night. / Hungary is still 22% below 2019. / Colombia +54% since 2019, new in the Top 50. / Philippines is still 28% below 2019.
- 竞品同题（`_build/raw/yt_search_most_visited_2026-11-03.jsonl`；YouTube 拦截了详情页，发布时间未取到）：
  - Reigarw Comparisons《Tourism Popularity Comparison》约 452 万播放（14:54，对比体）；touropia《12 Most Visited Countries in the World》约 47 万（15:17，旅行解说）；GRAPHXplore《Most Visited Countries by Tourists | Travel Trends 2025》约 13 万（3:07）。
  - 同格式（卡片滚动 Top 50）：Nerd Cassette《Most Visited Countries in the World (2026)》约 1.4 万；The Screen Data / okz data point / Earth Info 等 Top 50 均 < 4,000。
  - 差异：D1 每个数字有出处和统计期，纠正常见错值（中国 64.9M 误用、希腊 40.7M 含邮轮、香港 45M / 澳门 35M 含一日游、马来西亚 38M 含一日游、阿联酋 18.7M 只是迪拜）；D2 每卡 vs 2019 同口径变化 + NEW SINCE 2019；D3 大洲计分板；D4 洞察卡讲「谁恢复了、谁还没恢复、谁不在榜上」。竞品多把不同口径直接混排、或沿用 2019 数据。
- 风险：
  1. **口径争议**：评论区会说「中国怎么不在」「法国明明 102M」「意大利应该 65M+」——scope_note、洞察卡 3 与 sources.md 都有答案。
  2. **混合口径**：住宿计数国家（德、奥等）会高估（一人多次入住），当日往返国家（罗马尼亚、哈萨克斯坦）更高估；这是 UN Tourism 官方做法，卡上已标签提示。
  3. 英国：数据库 38.2M 与 ONS 2024 发布的 42.6M 差 4.4M（调查设计 2024 年中途更换）；用哪一个都不改变英国第 7。
  4. 法国 100M 是官方估计（Atout France 外推），UN Tourism 正式值未见；102M 说法见 notes。
  5. 发布前 7 天复核：UN Tourism 若发布新批量（含 2025 或补全 2024），重排名次。

## 待用户确认

1. 标题年份写 (2026)（发布年，同赛道惯例）还是 (2024)（统计期，bible §3.3）。代理默认 (2026)，屏上和描述框明确「Data: 2024 full year」。
2. 中国、阿联酋、丹麦、保加利亚、俄罗斯缺同口径 2024 值不入榜（默认）；如要用估算值补中国（按 2019 过夜占比推约 59.7M，会排第 5），需用户同意并标 est.。
3. 波多黎各不列入（默认）；香港、澳门单列并标 SAR OF CHINA（默认）。
4. 大洲按 UN M49（土耳其算亚洲）——默认；若要按 UN Tourism 区域（土耳其、中亚、高加索算欧洲）可改。
5. 英国用 UN Tourism 数据库 38.2M（默认）还是 ONS 42.6M。
