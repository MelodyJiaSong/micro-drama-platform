# ep02 · 各国最高峰 Top 50（每国取最高点，按海拔排序）

> 2026-11-03 代理起草（用户授权自主决策，**待用户点头**）。数据见 `data.json`、出处与判断依据见 `sources.md`、图片账本 `assets.json`；生成脚本在 `_build/`。

- 英文标题（≤60 字符）：**Highest Mountain in Every Country | Top 50 (2026)**（49 字符）
  - 屏上标题：Highest Mountain in Every Country · kicker「TOP 50」· 统计行「Elevation · Data as of Nov 2026」· 来源行「Sources: Wikidata (CC0), national surveys, Wikipedia」
- 指标与口径：每个主权国家（Wikidata Q3624078，含台湾）的最高点海拔，单位米，副显示英尺；取 Wikidata preferred 值，逐条用 Wikipedia「List of elevation extremes by country」及条目引用的测量交叉核对（详见 `sources.md` §1、§4）。统计期：2026-11-03 取数。
- N / 每名秒数 / 预计时长：
  - N = 50 张卡（47 个名次；珠峰、斯坦利山、勃朗峰各两国并列，排名 1,1,3 式跳号，第 50 名 = 第 50 个国家）。
  - 50→11 名每名约 5 s（40 张 ≈ 200 s）；前 10 名每名约 7 s（≈ 70 s）；洞察卡 5 张 × 3.5 s ≈ 18 s；片头 5 s；冠军停留 6 s；大洲计分板揭晓 7 s；来源卡 4 s；片尾 18 s。
  - **预计约 5:30**（不足 8 分钟，无中插广告，符合 bible「先用 Top 50 测完播率」）。
  - 冠军是**两张并列卡**（中国、尼泊尔，同一座珠峰，分别用北坡 / 南坡照片）：建议渲染器冠军段把两张卡并排同时放大，而不是先后出场——需在渲染器里支持「同名次并列强调」。
- 主源与交叉核对源（许可已核？）：
  - 主值：Wikidata P2044（CC0，已核）；珠峰 2020 中尼联合测量、勃朗峰 2023 上萨瓦省测量（均为 Wikidata preferred 值）；Denali 用 USGS 2015（公有领域）；Aconcagua 用库约国立大学 2012 测量；喀麦隆山、富士山、拉斯达申用 Wikipedia 条目引用的测量值（事实）。
  - 交叉核对：Wikipedia 列表（revid 1381548721）+ 条目 infobox 引用；只用事实，不搬文字（已核）。Peakbagger 拒绝脚本访问（403），未直接核到。
  - 图片：Wikimedia Commons，49/50 张，逐张核 extmetadata 许可（PD / CC0 / CC BY / CC BY-SA），见 `assets.json`。
- 国家归属口径：**按实际管辖**。印度取干城章嘉峰（印度官方主张 K2，K2 归巴基斯坦）；台湾保留并标「Taiwan」；同一山顶为两国最高点时各国一张卡，`badge` = SHARED WITH …（珠峰 中/尼、斯坦利山 刚果（金）/乌干达、勃朗峰 法/意，勃朗峰峰顶主权有争议，notes 写明）。大洲按山顶所在位置（厄尔布鲁士、什哈拉、巴扎尔杜久 → Europe；阿拉拉特、阿拉加茨 → Asia；查亚峰 → Oceania；泰德峰 → Europe）。全部列入 `sources.md` §2 待用户复核。
- 主题皮肤「alpine」（建议，渲染器 `theme.toml` 定稿）：
  - 背景：深夜蓝渐变 `#0B1A2E → #16324F`（雪山照片在深底上更亮，和 ep01 建筑期的浅色区分开）
  - 卡片：雪白 `#F5F8FB`，正文深蓝 `#0B1A2E`
  - 强调色：高山晨光橙 `#FF7A45`（名次、主数值）；辅助冰川蓝 `#8FD3FF`（英尺、洲别）
  - 主图类型：山峰实景照片（风景照不抠图，统一 16:10 居中裁切 + 轻微暗角）；缺图（乌兹别克斯坦 Khazret Sultan）用国旗大图 + 山形剪影占位
  - 主题图标：`mountain`（主数值左侧）；tag 用 `calendar`（首登年）、`trophy`（洲/世界之最）、`mountain`（火山类型）、`flag`（未登顶）
  - 国旗呈现：卡片顶部国旗条（默认）；共享山峰卡在国旗条下加 SHARED WITH 徽章
  - 计分板：右上角按大洲累计（Asia / Europe / Africa / South America / North America / Oceania），结尾揭晓 Asia 19 > Europe 8 = Africa 8 > South America 7 > North America 5 > Oceania 3
- 洞察卡候选（≥5 条；已定稿 5 条写入 `data.json`，均在 `sources.md` §5 核过）：
  1. after 41：Mount Cameroon is often listed at 4,095 m, but satellite data puts it nearer 4,040 m.
  2. after 32：Next: Mont Blanc. France and Italy still disagree over who owns its summit.
  3. after 21：Next: Elbrus, Europe's highest peak, 835 m taller than Mont Blanc.
  4. after 11：From here on, every peak tops 6,950 m, and 9 of the last 10 are in Asia.
  5. after 4：India also claims K2. We list each peak under the country that controls it.
  - 备选：Mont Blanc's ice cap changes its height every survey（4,810.02 m in 2013 → 4,805.59 m in 2023 → 4,807.47 m in 2026）；Chimborazo's summit is the farthest point from Earth's centre；Gangkhar Puensum (Bhutan) has never been climbed — climbing is banned；Only 9 countries have a peak above 7,000 m, all in Asia。
- 竞品同题（链接、播放、发布时间）与我们的差异：
  - List Data《Highest Mountain From Different Countries》https://www.youtube.com/watch?v=fUswTruk1Cg — 约 100 万播放，6:54，发布时间未取到（搜索结果无日期）。同频道《Tallest Mountain From Different Countries》https://www.youtube.com/watch?v=K5Q6EHubENY 约 23 万。
  - 其他：EARTHGENT《HIGHEST MOUNTAIN in each COUNTRY》5 万；THE MOST《Tallest Mountain in Every Country》0.4 万；Chicago Geographer 分洲系列 5–13 万。
  - 差异：① 每个数字有出处和日期，修正了常见错值（珠峰 8,849 而非 8,850/8,848；喀麦隆 4,040 而非 4,095；勃朗峰取 2023 实测），描述框附逐条来源；② 共享山峰与争议归属明确标注（SHARED WITH、K2/印度、勃朗峰主权）；③ 大洲计分板 + 结尾揭晓；④ 洞察卡讲「数据背后的争议」，不是纯滚动。
- 风险：
  1. **归属争议**（K2/克什米尔、台湾、勃朗峰、不丹边界）可能引发评论区争吵：好处是互动，坏处是可能被举报；片头口径行写「by de-facto control」，洞察卡 5 主动说明。中国大陆观众对「Taiwan」单列可能有负面反应——系列面向全球，按既定口径保留，用户如要调整需在发布前定。
  2. **数值争议**：什哈拉（5,193 vs 5,203，影响与肯尼亚的先后）、喀麦隆山、哥伦比亚双峰（可能低 ~1%）、Ras Dashen（4,533/4,550/4,620）——均写在 notes，评论区有人纠错时可直接指向 sources。
  3. **缺图 / 低清图**：Khazret Sultan 无可用照片（需占位设计）；Puncak Jaya 原图仅 640 px，Mount Logan 975 px，需渲染后抽检清晰度。Ismoil Somoni Peak 为黑白照，风格不一致。
  4. **署名量大**：49 张 Commons 图，CC BY-SA 占多数，带链接的完整署名约 6,750 字符，超过 YouTube 描述 5,000 字符上限，所以 `sources.md` §7 另生成约 1,900 字符的紧凑版放描述框，完整版放置顶评论或外部页面；片尾来源卡写「Photos: Wikimedia Commons contributors (see description)」。
  5. **YPP 原创性**：同题已有百万播放竞品；靠 D1（来源与修正）和 D4（争议洞察）区分，旁白（D5）本期仍不加。
  6. 发布前 7 天内复核：重点看勃朗峰（2026-09-17 新测 4,807.47 m，2026-10-14 公布，已采用；独立审片 2026-11-03 发现原稿用的是 2023 值）、珠峰与 K2 无变化。
