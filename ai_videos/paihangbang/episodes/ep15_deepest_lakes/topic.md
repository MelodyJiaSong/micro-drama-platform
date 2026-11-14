# ep15 · 世界最深湖泊 Top 35（最大水深 > 400 m 的全部天然湖）

> 2026-11-03 代理起草（用户授权自主决策，**待用户点头**）。数据 `data.json`、出处与争议 `sources.md`、图片账本 `assets.json`；生成脚本与原始抓取在 `_build/`（`items_def.py` 是数值唯一定义处）。

- 英文标题（≤60 字符）：**Deepest Lakes in the World | Top 35 Ranked (2026)**（49 字符）
  - 屏上标题：Deepest Lakes in the World · kicker「TOP 35」· 统计行「Maximum depth · Data as of Nov 2026」· 来源行「Sources: lake surveys & papers, ILEC, FAO, USGS, NVE, Wikipedia」
- 指标与口径：天然湖泊的**最大实测水深**（米，副显示英尺），收最大水深 > 400 m 的全部湖泊。收：天然湖（含被小坝略抬高的 Lake Chelan）、里海（按湖计）。不收：水库、冰下湖（Vostok 等）。来源冲突时取**最新的同行评审 / 机构实测**，卡上用 `DEPTH DISPUTED` 徽章或「Often listed as …」标签写出旧值。统计期：2026-11-03 取数。
- N / 每名秒数 / 预计时长：N = 35（门槛 400 m；2026-11-04 独立审片 B1：Wakatipu 的 420 m 无出处，LINZ/MfE 为 376–380 m，移出）。卡宽 720，每名约 6.3 s；片头首卡停留 2.5 s（layout.intro_hold）；5 张洞察卡；**总长约 4:43**（`timeline`）。
- 主源与交叉核对源（许可已核？）：
  - 主值逐条找一手：Baikal INTAS 2002 测深图；Tanganyika FAO LTR 项目表（1946–47 比利时考察测深）；O'Higgins / Viedma / Argentino 用 Minowa et al. 2023（J. Glaciology，CC BY，2012–2020 船载测深）；Crater USGS 2000 多波束；Tahoe USGS 1998 多波束；Grey Sugiyama et al. 2021（Nat. Commun.）；Issyk-Kul De Batist 回声测深（Zavialov 2018 评述）；Malawi ILEC；Van Degens 1984；挪威各湖 NVE 测深图 / Seppälä 2005 等。只作事实引用，不搬文字（已核）。
  - 交叉核对：Wikipedia「List of lakes by depth」（rev 1371850291）与各条目 infobox、ILEC World Lake Database。
  - 共享 WebSearch 额度中途用尽，之后只用直连抓取；未能直接打开的一手文献记「经 Wikipedia 转引」（详见 `sources.md` §6.7）。
- 国家归属口径：跨国湖按**湖面面积占比最大**的国家放国旗，加 `SHARED WITH X`（两国）或 `SHARED BY N COUNTRIES`（三国以上）徽章；没有公认水面划分的里海按**湖岸线最长**（哈萨克斯坦 2,340 km）。Tanganyika 按 FAO 一手表取刚果（金）45%（Wikipedia 写坦桑尼亚 46%，不用）。Kivu（刚果（金））、Superior（美国）未找到可核的面积划分，按惯例——**待用户确认**。计分板按大洲：Asia 9、North America 8、South America 7、Europe 5、Oceania 3、Africa 3（里海记 Asia）。
- 主题皮肤：`abyss`（渲染器已加）——深海青底、冰川青强调色；满版湖景横幅照片（卡宽 720，焦点居中）；标签图标 `map-pin`（湖底相对海平面高程）、`ruler`（测量年份 / 旧值）、`trophy`（洲 / 国之最）、`calendar`、`mountain`。
- 洞察卡（5 张，均在 `sources.md` §5 有依据）：
  1. after 30：Old lists: Poso 450 m, Wakatipu 420 m. Surveys show 395 m and ~380 m, so both are out.
  2. after 17：Next: Sarez Lake, born in 1911 when a quake-triggered landslide dammed a Pamir river.
  3. after 11：Three of the top 10 are Patagonian lakes, carved by glaciers that are still retreating.
  4. after 6：Next: Viedma. A 2022 survey reported 900 m (unpublished); peer-reviewed sonar: ~750 m.
  5. after 2：Next, No. 1: a lake holding about 20% of the world's unfrozen fresh water (UNESCO).
  - 备选：Baikal's floor lies 1,187 m below sea level; Sarez's floor is still 2,758 m above it（卡上 Floor 标签已体现）；Lago O'Higgins was quoted at 836 m until a 2020 survey measured 799 m（卡上标签已体现）；Lago Fagnano is often listed at 449 m, but its bathymetric map shows 206 m.
- 竞品同题（需求证据 `0_research/data/yt_demand_2026-11-03.jsonl`，查询「deepest lakes in the world」前 15 条中位数 46.9 万、最高 1,979 万）：
  - Free High-Quality Documentaries《The Fascinating World of Deep Mountain Lakes | Full Documentary》约 1,979 万（长纪录片，不是排行）。
  - Astrum Earth《The Underwater Lakes That Shouldn't Exist》约 410 万；New Nature and Deep Science with Mark Watts《Why the Deepest Lake on Earth Will Cause a Global Crisis》约 301 万（单湖解说）。发布时间：数据集无日期，未取到。
  - 差异：D1 每个深度有出处与测量年份，**主动改正常见错值**（Poso 450 → 395 出榜、Fagnano 449 → 206、O'Higgins 836 → 799、Argentino 719 → 607、Issyk-Kul 702 → 668），争议值（Viedma 750 / 900）明标；D2 卡上写「Survey 2020 (was 836 m)」「Often listed as …」；D3 大洲计分板（亚洲 9 vs 北美 8 悬念到最后）；D4 洞察卡讲测量与修正的故事。另加「湖底在海平面下 / 上多少米」标签，这是同题视频少见的角度。
- 风险：
  1. **数值争议**多（见 `sources.md` §6）：Viedma、Argentino、Toba、Kivu、Adams、Wakatipu、Sarez、Nahuel Huapi。评论区纠错可直接指向描述框来源。
  2. **国旗归属**：Kivu、Superior 按惯例；Malawi 有马坦边界争议；里海用「岸线最长」规则。
  3. **时长 4:47** 低于 bible 建议的 5–8 分钟（无中插广告）。
  4. 冷门湖图源少：默认母版 25 张可商用照片 + 10 张 Codex 生成图（卡上标「AI-generated image (not a photo)」，上传须勾选合成内容声明）；风险版 7 张许可不明照片待签字（明写版权所有的 4 张已撤下）。Flickr CC 真图因限流未下到，解禁后可替换生成图（见 `_build/handoff.md`）。

## 待用户确认

| # | 事项 | 代理默认 |
|---|---|---|
| 1 | N = 35（门槛 400 m，Wakatipu 出榜）、时长约 4:43 | 保持；不凑数 |
| 2 | 里海算湖 | 算（地理学通行），scope_note 写明 |
| 3 | 冰下湖（Vostok）不收 | 不收，scope_note 写明 |
| 4 | Viedma 取 ~750 m（2023 论文）而非 900 m（2022 新闻稿） | 750，DEPTH DISPUTED + 洞察卡 4 |
| 5 | Argentino 取 607 m（同一湖臂的同行评审测深）而非 719 m（死链） | 607，DEPTH DISPUTED |
| 6 | Kivu 国旗刚果（金）、Superior 国旗美国（按惯例，未核面积划分） | 保持 |
| 7 | Tanganyika 国旗按 FAO 表用刚果（金），不用 Wikipedia 的坦桑尼亚 | 刚果（金） |
