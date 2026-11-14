# ep11 · 世界最大船舶 Top 42（按船级，登记总吨 GT，2026-11 在役）

> 2026-11-03 代理起草（用户授权自主决策，**待用户点头**）。数据见 `data.json`，出处与判断依据见 `sources.md`，图片账本 `assets.json`；生成脚本在 `_build/`（`vf_bands.py` → `compute_classes.py` → `build.py` → `gen_sources.py`）。

- 英文标题（≤60 字符）：**Biggest Ships in the World 2026 | Top 42 by Gross Tonnage**（57 字符）
  - 屏上标题：Biggest Ships in the World · kicker「TOP 42」· 统计行「Gross tonnage · Ships in service · Nov 2026」· 来源行「Sources: DNV Vessel Register, VesselFinder, Lloyd's Register」
- 指标与口径：
  - **登记总吨 GT**（ITC 1969，衡量围蔽容积，不是重量），屏上写全数（248,663 GT）。前 13 名只差几百到几千 GT，取 3 位有效数字会出现大量假并列，所以偏离 bible §3.4（代理判断）。
  - **一张卡 = 一个船级**：同一船东同一建造计划、同一名义尺寸的姊妹船合并（即使分在几家船厂造），数值取该级在役船中最大的登记 GT；卡上副标题写船型与艘数，例如「Container ship · 13 ships」。
  - **只收 2026-11 在役的船**；不收永久系泊的海工装置（FPSO / FLNG / FSO，含 Prelude、TI 级改装的储油轮）、军舰、在建与已拆船。
  - **下限 = 比仍在营运的最大油轮（170,618 GT）还大**。这条线把 160–170k GT 一大群几乎一样的 VLCC 挡在外面，也给片子一个说法（洞察卡 1）。
  - 结果：**N = 42**（数据决定，不凑 50）。类型：集装箱船 29、邮轮 8、矿砂船 4、起重船 1。
  - 统计期：2026-11-03 取数。主源 DNV Vessel Register（13 个船级，船级社一手登记）+ VesselFinder（IHS 数据，其余 28 个；与 DNV 重叠部分全部一致）；维基只作交叉核对。
- N / 每名秒数 / 预计时长：42 张卡；卡宽 800，每名约 7.3 s；洞察卡 6 张；片头停留 intro_hold 2.5 s；总长约 6:03（`timeline`）。
- 主源与交叉核对源（许可已核？）：数据为事实，DNV 公开登记与 VesselFinder 公开详情页只取数值不搬文字；维基只作核对（已核）。图片：Flickr 可商用 CC 许可（逐张核照片页许可），见 `assets.json`。
- 国家归属口径：**运营公司总部所在国**（不是船旗国）。OOCL → Hong Kong；ONE → Singapore；Valemax / Guaibamax → Brazil（Vale，按其规格建造并长期租用运矿）；Excellence 级 → Italy（取值船 Costa Toscana 的运营方 Costa，与其他卡同一规则；QC M3 改）。计分板按 country：Switzerland 8（MSC、MSC Cruises、Allseas）> France 6 > Denmark 5 > United States 4 = China 4 > 其余。
- 主题皮肤「maritime」（渲染器已内置）：深海军蓝底、白卡，信号橙强调色；主图 = 真实船舶照片（整船侧面或四分之三船首视角）；图标 ruler（长度）+ calendar（首制年）；国旗左上角。
- 洞察卡（6 条，均在 `sources.md` §5 核过）：
  1. after 39：No oil tanker makes this list: the biggest still trading is 170,618 GT, just below No. 42.
  2. after 31：7 of these 42 ship classes did not exist before 2025. The race to build bigger isn't over.（D2 变化）
  3. after 22：Gross tonnage measures a ship's enclosed volume, not its weight. Cruise ships score high.（反常识）
  4. after 15：Next: the class of Ever Given, the ship that blocked the Suez Canal for six days in 2021.
  5. after 7：MSC Irina carries the most boxes (24,346 TEU), yet 3 container classes outrank it.（反常识）
  6. after 2：No. 1 is 62% bigger than Icon of the Seas, and it's neither a cargo nor a cruise ship.
  - 备选：世界最大的四艘油轮（TI 级）都已改成系泊储油轮；Prelude FLNG 488 m 比任何上榜船都长但不航行；瑞士是内陆国却运营最多巨轮。
- D2 变化：徽章 NEW 2025（CMA CGM Seine 级、Disney Adventure、Berlin Maersk 级、Ever E 级）、NEW 2026（OOCL Wisdom 级、Yuan Hai Si Lu、Winning Ambition 级）；其他徽章 LARGEST CRUISE SHIP、RECORD 24,346 TEU、EVER GIVEN'S CLASS、BIGGEST BULK CARRIER、OLDEST ON THE LIST。
- 竞品同题（需求证据 `0_research/data/yt_demand_2026-11-03.jsonl`，搜索「biggest ships in the world」前 15 条播放中位数 183 万、最高 946 万）：
  - BE AMAZED《LARGEST Ships On Earth》946 万播放（发布时间未取到）——混讲历史巨轮、航母、已拆的 Seawise Giant，数字多为宣传值、无出处。
  - Free Documentary《World's Biggest Containership | Mega Transports》874 万——单船纪录片。
  - Supercar Blondie《Inside the World's Biggest Cruise Ship | Icon of the Seas》676 万——单船探访。
  - （本次 WebSearch 配额已用尽，未再查更多同题排行视频的日期。）
  - 我们的差异：D1 每个数字是船级社 / 登记数据，片头写清口径（在役、按 GT、按船级、海工装置不收），描述框逐条来源；D2 标出 2025–26 新下水的六个船级；D3 运营国计分板（瑞士压轴是反常识点）；D4 六张洞察卡讲「GT 不是重量」「箱量冠军不是体积冠军」「油轮已经不是最大」。
- 风险：
  1. **口径争议**：观众常以为最大船是油轮 / 航母 / Prelude。片头口径行 + 洞察卡 1、3 + 描述框说明；评论区可直接指向 sources。
  2. **集装箱船占 29/42**：这是 GT 口径的真实结果（同级已合并）；靠不同船公司涂装、邮轮与矿砂船穿插缓解。
  3. **数值**：13 个船级有 DNV 一手登记；其余 28 个只有 VesselFinder（IHS）+ 维基核对；2026 新交付船（OOCL Wisdom、Ever E、Winning、Berlin Maersk）的 GT 发布前 7 天复核。
  4. **国家归属**：Hong Kong 单列、ONE 归新加坡、Valemax 归巴西都可能有人不同意（见下「待用户确认」）。
  5. **图片**：默认母版 34 张 Flickr 可商用照片 + 2 张可商用替代图 + 5 张 AI 生成写实插图（Valemax 主图；OOCL Wisdom、Sphere、Winning Ambition、Guaibamax 的默认版替代，卡上标 AI IMAGE；上传须勾选合成内容声明），无占位卡；风险版 6 张许可不明照片待签字。CC BY-SA 为主，需在描述框 / 置顶评论署名；卡上写的是船级，照片可为姊妹船（assets.json `subject_note` 写明）。

## 待用户确认

| # | 事项 | 代理默认 |
|---|---|---|
| 1 | 一张卡 = 一个船级，数值取级内最大登记 GT | 采用；卡名写船级（如「Oasis class」），照片可为任一姊妹船 |
| 2 | 下限 = 大于最大营运油轮 170,618 GT，N = 42 | 采用；若坚持 Top 50 需降到 ~166k，会混进 6–8 个几乎一样的 VLCC 船型和 Q-Max（168,189） |
| 3 | 永久系泊海工装置（Prelude 等）不收 | 不收；Prelude 写进描述框说明 |
| 4 | 国家 = 运营公司总部；OOCL → Hong Kong，ONE → Singapore | 采用，片内来源行「Flag = operator HQ」+ 描述框写明；若并入中国，China 7 升到第二 |
| 5 | Valemax / Guaibamax 归 Brazil（Vale） | 采用；按船东则多数归中国 |
| 6 | YUAN HAI SI LU（远海丝路，2026）180,011 GT | 已收为第 31 名（独立审片 M2）；GT 发布前复核 |
| 7 | 屏上 GT 写全数（偏离 bible §3.4 的 3 位有效数字） | 采用 |
