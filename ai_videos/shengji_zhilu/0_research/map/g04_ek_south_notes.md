# G04 · 东部王国南部 —— 测绘备注

> 本文件**不含树数据**。所有节点字段只写在 `g04_ek_south.yaml`，此处不重复（仓库规则「一份东西只有一个出处，副本必漂」）。
> 片区：荆棘谷 / 悲伤沼泽 / 诅咒之地 / 逆风小径 / 燃烧平原 / 灼热峡谷 / 黑石山
> 版本锚点：经典旧世 Vanilla / Classic Era 1.12

---

## ① 自查对账

### 真的抓到并读完的页（`verified_by: ai_read` 的依据）

**warcraft.wiki.gg —— 旧世专页（`(Classic)` 后缀，最关键的一批）**

| 页面 | 拿到了什么 |
|---|---|
| `Stranglethorn_Vale_(Classic)` + `?action=raw` | 30-45 等级、41 条旧世子区域全表、旧世飞行点、Cata 拆分说明 |
| `Swamp_of_Sorrows_(Classic)` + `?action=raw` | 35-45、14 条子区域、Stonard 航线、相邻地区表 |
| `Blasted_Lands_(Classic)` + `?action=raw` | 45-55、9 条子区域、卡扎克/腐烂之痕描述 |
| `Deadwind_Pass_(Classic)` + `?action=raw` | 55-60、10 条子区域 |
| `Burning_Steppes_(Classic)` + `?action=raw` | 50-58、12 条子区域、双阵营旧世航线 |
| `Searing_Gorge_(Classic)` + `?action=raw` | 45-50、11 条子区域、钥匙进入机制原句 |

**warcraft.wiki.gg —— 通用页**
`Stranglethorn_Vale`（零售版，取了 Booty Bay 海盗原句）· `Booty_Bay?action=raw`（店铺/设施/航线/船）· `Grom'gol_Base_Camp?action=raw`（坐标模板/飞艇/指挥官）· `Stonard?action=raw`（两座地穴/大厅/航线）· `Thorium_Point?action=raw`（坐标 36,27 / 监督者奥菲斯特 / 瑟银兄弟会）· `Nethergarde_Keep?action=raw`（坐标模板 65,19 / 守军 / 职责原句）· `Zul'Gurub_(Classic)`（20 人、1.7、11 个内部分区）· `Temple_of_Atal'Hakkar`（泪水之池入口、11 个内部分区、别名）· `Dark_Portal`（旧世不可通行原句）· `Karazhan`（南逆风小径 54,78、TBC 才开放）· `Blackrock_Mountain` + `?action=raw`（内部分区表、灼热峡谷侧入口 34,74）· `Blackrock_Depths`（BRD 路线原句、20 个内部分区）· `Blackrock_Spire?action=raw`（LBRS/UBRS/BWL 三段分区全表）· `Molten_Core`（「位于黑石深渊最底部」原句）· `Khaz_Modan`（地区归属裁定依据）· `Kingdom_of_Stormwind`（反证：只辖艾尔文/西部荒野/暮色/赤脊）

**中文来源**
`db.nfuwow.com/60/?zone=33 / 41 / 25`（1.12 数据库：荆棘谷 30-45、逆风小径 50-60、黑石山 55-60）·
`wow.17173.com`「世界地图全探索成就」页（**本片区绝大多数国服子区域中文名的来源**，逐区成组抓到）·
`ming1314.com/502`（旧世地图中英文＋等级对照）· `9game.cn`（斯通纳德飞行点坐标 46.1, 54.8）

### 抓不到的（已尝试并失败，逐条如实记）

| 站点 | 结果 | 影响 |
|---|---|---|
| `wowhead.com/classic/zone=33&xml`、`classic.wowhead.com/zone=33` | **403 / 301→403** | 拿不到旧世坐标与等级带的权威数值 —— 这是本片区 `coords` 大面积留空的主因 |
| `wow.huijiwiki.com`、`warcraft.huijiwiki.com`（多次、多路径） | **全部 403** | 中文官方译名无法从灰机 wiki 直接核；改用 17173 探索成就清单 + 中文数据库兜底 |
| `db.damijing.com/map/8`、`/map/33` | 可访问但是**零售版**（显示「北荆棘谷」），无子区域表 | 无用 |
| `classic-wow-archive.fandom.com/wiki/Blackrock_Mountain` | **402 Payment Required** | 黑石山内部动线改由 `Blackrock_Depths` / `Blackrock_Spire` 正文 + 搜索摘要拼出 |
| `warcraft.wiki.gg/wiki/Blackrock_Mountain_(Classic)` | **404，该页不存在** | 黑石山无旧世专页，其内部分区表按通用页 + 逐副本页交叉核，Cata 条目（黑石洞穴 / 黑翼血环）已剔除 |
| WebSearch | **会话预算 200/200 用尽**（被本次工作流其他 worker 共同消耗） | 最后一轮想做的「探索灼热峡谷 / 探索逆风小径 / 探索燃烧平原」成就清单补查没做成 —— 见 ③ 存疑 |

### 一个必须记下来的方法教训

**摘要式抓取会把零售版和旧世版的清单悄悄合并。**
第一轮用自然语言 prompt 抓 `*_(Classic)` 页时，返回的子区域表里混进了 Cata 才有的条目：
燃烧平原多出 Chiselgrip / Flamestar Post / Black Tooth Hovel / The Skull Warren / Firegut Furnace / Fields of Honor / Valley of Ashes / The Whelping Downs，
灼热峡谷多出 Iron Summit / Pyrox Flats / Thorium Advance，
荆棘谷多出 Fort Livingston / Bambala / The Sundering / Hardwrench Hideaway / Explorers' League Digsite。
改用 **`?action=raw` 取原始 wikitext** 后，上述条目在旧世表里全部不存在 —— 它们被剔除了。
**结论：凡「版本敏感」的清单，一律读 raw wikitext，不读摘要。** 本片区 6 个 zone 的子区域表最终都以 raw 为准。

### 完整性自评

| zone | 节点数 | 判断 |
|---|---|---|
| 荆棘谷 | 62 | 41 条旧世子区域 100% 覆盖 + 藏宝海湾内部 + 祖尔格拉布 11 个分区 |
| 黑石山 | 53 | BRD 20 + BRS/BWL 19 + 山体本身，副本枢纽挂满 |
| 悲伤沼泽 | 29 | 14 条子区域全覆盖 + 阿塔哈卡神庙 11 个分区 |
| 燃烧平原 | 15 | 12 条子区域全覆盖 + 飞行点 + 黑石山南入口 |
| 灼热峡谷 | 13 | 11 条子区域全覆盖 + 飞行点 + 黑石山北入口 |
| 诅咒之地 | 12 | **旧世本就只有 9 条子区域**（raw 已核） |
| 逆风小径 | 11 | **旧世本就只有 10 条子区域**，且全区无任务、近乎无 NPC |

> ⚠️ 对「少于 10 个 ＝ 没查全」这条启发式的一个例外说明：**诅咒之地与逆风小径是旧世最空的两张图**，
> 不是查得薄。两者的 raw wikitext 子区域表分别只有 9 条与 10 条，已全部落树；再往下挂就只能编地名了，没有编。
> 逆风小径在 1.12 甚至**没有任何任务**，卡拉赞也进不去——这恰恰是它作为「过路的荒凉走廊」的剧作价值所在。

---

## ② 版本差异：4.0.3a（大地的裂变）改了什么

**本片区是全服 4.0.3 改动最猛的区域之一，下面每条都是「旧世有 / 现在没有」或「名字变了」，逐条记，防止下游误用。**

1. **荆棘谷被劈成两张图。** 旧世 `Stranglethorn Vale`（一张 30-45 的大图）→ 4.0.3 拆为 `Northern Stranglethorn`（北荆棘谷）与 `The Cape of Stranglethorn`（荆棘谷海角）两张独立地图。
   → **连带后果：荆棘谷的地图坐标系整体重算。** 零售 wiki 上格罗姆高营地记作「北荆棘谷 38,50」，这个数**不能**当旧世坐标用。本树因此把荆棘谷全部节点的 `coords` 留空，而不是填一个错的。
2. **荆棘谷新增地名（不进树）：** Fort Livingston、Bambala、The Sundering（裂变劈出的大地裂谷）、Hardwrench Hideaway、Explorers' League Digsite、Rebel Camp 的 FP 化。
3. **悲伤沼泽整区重做。** 新增哥布林度假镇 Bogpaddle（淤泥沼泽）、联盟前哨 Marshtide Watch（沼泽之潮哨站）、The Bloodmire（浴血泥潭）、Purespring Cavern、Fortune's Fist 等；联盟转为对斯通纳德主动进攻。旧世的悲伤沼泽**几乎无人烟**，只有斯通纳德一个据点和一个飞行点——这个荒凉度是旧世独有的。
4. **诅咒之地重做。** 新增渔村 Surwich（瑟维奇）、Nethergarde Mines、Dreadmaul Furnace、Sunveil Excursion、Rockpool Village、Shattershore 等一大批地名；德鲁伊 Marl Wormthorn 把 **The Tainted Scar（腐烂之痕）腐化成 The Tainted Forest（污染之林）** —— 旧世那片冒绿毒雾的焦黑裂痕**现在已经不存在了**。
   同时 **巨槌要塞 Dreadmaul Hold 在旧世是食人魔的，4.0.3 后才被部落（Okril'lon）拿下**。本树按旧世记为 contested。
5. **黑暗之门在 1.12 不能走。** 旧世走进去只是穿到门背后，纯装饰；**2.0.1（燃烧的远征）才真正开启**。这一条对剧作影响最大——旧世的黑暗之门是一座「封死的纪念碑」，不是一道门。
6. **灼热峡谷在旧世要钥匙。** 洛克莫丹一侧（Stonewrought Pass）的闸门上锁，需走任务线拿 `灼热峡谷的钥匙`（或盗贼 225 开锁）；另两条路是荒芜之地的卡加斯、以及经黑石山。**4.0.3 取消上锁**，等级带也从旧世的 43/45-50 调成 47-51。
7. **灼热峡谷新增地名（不进树）：** Iron Summit（铁怒前哨，Cata 才有的飞行点）、Pyrox Flats、Thorium Advance。
8. **燃烧平原新增地名（不进树）：** Chiselgrip（凿壁据点）、Flamestar Post、Black Tooth Hovel、The Skull Warren、Firegut Furnace、Fields of Honor、Valley of Ashes、The Whelping Downs、Dragon's Mouth 飞行点。
   旧世燃烧平原只有 **摩根的岗哨（联盟）** 与 **烈焰峰（部落）** 两个据点、两个飞行点。
9. **卡拉赞在 1.12 进不去。** 只是逆风小径南端一座不可进入的地标建筑；**2.0（TBC）才开放为 10 人团队副本**。逆风小径的 `Karazhan Catacombs`、`Alturus' Sanctum`、`Abandoned Kirin Tor Camp`、`Forgotten Crypt`（及其 Pauper's Walk / Upside-down Sinners 等子区）都是后续版本加的，**不进树**。
10. **黑石山内部的后期增补（不进树）：** `Blackrock Caverns`（黑石洞穴，Cata 5 人本）、`Blackwing Descent`（黑翼血环，Cata 团本）、以及 UBRS 在 WoD 被重做成 100 级 5 人本。旧世黑石山只有 **黑石深渊 / 黑石塔（上下层共用一门）/ 熔火之心 / 黑翼之巢** 四个副本。
11. **祖尔格拉布在旧世是 1.7 才上线的 20 人团本**（Cata 后被移除、MoP 重做为 5 人「祖尔格拉布」。本树只收 1.7–1.12 的 20 人版）。约亚姆巴岛同批加入。
12. **阿塔哈卡神庙（沉没的神庙）** 旧世是 50-56 的 5 人本；零售已重做并下调等级。

---

## ③ 存疑与未查

### A. 坐标几乎全空，这是刻意的

只有 4 个节点带 `coords`，全部来自能对上旧世地图的来源：
瑟银哨塔 `[36,27]`、黑石山北入口 `[34,74]`、卡拉赞 `[54,78]`、斯通纳德 `[46,55]`（后者来自怀旧服攻略站）。
**其余一律留空**，理由：wowhead classic 403，而零售 wiki 的坐标对**荆棘谷（拆图重算）**和**诅咒之地（南扩）**已经失效，
填进去就是「看起来有、实际是错的」，比空着伤害大。
守望堡的 `{{coords|65|19|Blasted Lands}}` 我抓到了，但因为是零售图坐标、**没有**写进树。
→ **下游若需要坐标，见 ⑤ 的补查方案。**

### B. 中文译名的三档可信度（树里已逐条标注）

- **无标注** ＝ 来自 17173 探索成就清单或中文数据库/攻略站，属国服官方译名，可直接用。
- **`note_zh: 中文名未经官方页面核实`** ＝ 广泛使用但我没从官方页面直接核到。共 10 条，例：
  暗影裂口城、黑铁酒吧、命运大厅、监狱区、黑手大厅、铸铁者之墓、奈法利安的巢穴、拉格纳罗斯的巢穴、芦苇岗哨、雄鹿沼泽洞穴、荒芜之海、藏宝海湾码头。
- **`name_zh` 直接留英文 + `note_zh: 官方译名未查到`** ＝ **没有自己音译**。主要集中在副本内部房间名（ZG 11 条、ST 11 条、BRD/BRS/BWL 约 25 条）与几个旧世冷门子区域
  （Tkashi Ruins、Slither Rock、The Stockpile、Stonewrought Pass、Janeiro's Point、The Crystal Shore、Wild Shore、Southern Savage Coast、South Seas、Haunted Isle、Spirit Den、Battle Ring、Nazferiti river、Grosh'gok Compound、Ariden's Camp、Sleeping Gorge、Deadwind Ravine、Crypt、Morgan's Plot、The Master's Cellar 等）。
  → 这些**不是漏查，是拒绝编**。国服这些房间名确实存在，但我这轮没能从任何可访问的官方/半官方中文源核到。

### C. 三个「描述性命名、非官方地名」的节点（树里已明写）

`blackrock_mountain_south_entrance`（黑石山南入口）· `blackrock_mountain_north_entrance`（黑石山北入口）· `molten_span_chains`（熔岩上的铁链）· `dark_portal_crater`（黑暗之门坑地）。
游戏里**没有**这几个地名，但它们是真实存在且对动线/选景关键的地形，所以入树并逐条标注。**下游不要把它们当官方地名写进台词或字幕。**

### D. 等级带在几个来源之间有出入（树里取 wiki 旧世专页的值）

| zone | 树里取值（wiki Classic 信息框） | 其他来源 |
|---|---|---|
| 灼热峡谷 | `45-50` | 任务书派说 43-50；nfuwow 系怪物等级 43-56 |
| 逆风小径 | `55-60` | nfuwow 1.12 数据库记 50-60 |
| 燃烧平原 | `50-58` | ming1314 记 50-59 |
| 诅咒之地 | `45-55` | ming1314 记怪物 46-63；悲伤沼泽相邻表记 52-60 |
| 荆棘谷 | `30-45` | ming1314 记 30-50 |
| 悲伤沼泽 | `35-45` | ming1314 记 36-43 |

差异来源是「推荐练级带 vs 怪物实际等级带」两种口径，不是矛盾。**统一取了 wiki 旧世专页信息框**，口径一致即可。

### E. 「火焰之门」—— 核实结果：**本片区不存在这个地名**

任务书要求核实的「火焰之门?」，在旧世的燃烧平原 / 灼热峡谷 / 黑石山**都查不到**。
搜索只命中三个形近物：**火焰之地 Firelands**（Cata 团本，在海加尔山，不在本片区也不是旧世）、
**熔火之心 Molten Core**（就在黑石山内，已入树）、**烈焰峰 Flame Crest**（燃烧平原部落据点，已入树）。
→ **判断：「火焰之门」多半是「熔火之心」或「烈焰峰」的记忆串线。没有凭空造一个节点。**

### F. 黑石山怎么挂 —— 裁定与理由

**裁定：`blackrock_mountain` 作为 `zone` 挂在 `khaz_modan` 下；在燃烧平原侧与灼热峡谷侧各挂一个 `poi` 入口指向它。**

理由三条：
1. **它在旧世本来就是一个独立 zone**（zone id 25，nfuwow 记 55-60），不是谁的子区域。把它塞进燃烧平原或灼热峡谷任何一边，都会把另一边的入口变成跨区引用。
2. **父节点选 khaz_modan 是有出处的**：`warcraft.wiki.gg/wiki/Khaz_Modan` 的 Zones 一节明确把 Blackrock Mountain 列入（同列的还有 Searing Gorge、Badlands、Loch Modan、Dun Morogh、Wetlands）；
   同一页**没有**列入 Burning Steppes（燃烧平原属艾泽拉斯南部大陆一侧）。所以本树里灼热峡谷 + 黑石山归 `khaz_modan`，燃烧平原不归。
3. **「一份几何，两道门」**：山体只登记一次，两个入口各自作为所在 zone 的 poi。这样任何一侧的动线都走得通，而山不会被登记两遍。
   燃烧平原与灼热峡谷的 `adjacent` 里都写了 `blackrock_mountain`，合龙时是自洽的。

### G. 旧世黑石山的四道副本门，各在山体什么位置（这是任务书点名要的）

从任一入口进山，都会走到中央的环形大厅 **The Molten Span**：一圈宽石道贴着岩壁盘绕，中央悬着由数条粗铁链拉住的石塔 **铸铁者之墓**，塔下就是熔岩海。

- **黑石深渊 BRD** —— 过铁链到中央石柱 → 沿石柱一路向下到熔岩上方的平台 → 右转穿过矿道 **The Grinding Quarry** → 门就在尽头。（原句已入树 quote）
- **熔火之心 MC** —— **不在山体上，在黑石深渊的最底部**（wiki 原句：「The Molten Core lies at the very bottom of Blackrock Depths.」）。从 BRD 内部过图书馆大厅方向、熔岩桥一线下到底。完成钥匙任务线后另有传送门可直接传入。
- **黑石塔 BRS** —— 沿 The Molten Span 的环形大道**向上**绕到大厅的**东北角**，那道高石门就是。旧世**上下层共用这一道门**（进门后按走向分 LBRS / UBRS）。
- **黑翼之巢 BWL** —— 在**黑石塔上层的顶端**；需先在 **黑手大厅 Hall of Blackhand** 使用「奥术水晶球 Orb of Command」才能开。所以 BWL 在树里挂在 `blackrock_spire` 之下，不是挂在山体之下。

> 可信度说明：BRD 路线与 MC 位置有 wiki 原句支撑（`ai_read`）；
> **BRS 入口方位、铁链动线、铸铁者之墓的作用只有搜索摘要级证据，已标 `ai_draft`（共 4 条）。**
> 黑手大厅里的奥术水晶球那条是常识性通行知识，我没抓到原句，写在 `note_zh` 而没有当 quote。

---

## ④ 本片区地图图片链接清单

**仓库既有裁定：暴雪美术资产只进人眼、不入画、不上传给生成模型。下面只记 URL 与版权状态，一律不下载、不喂模型。**

| 用途 | URL | 版权状态 |
|---|---|---|
| 荆棘谷旧世全图 + 子区域图 | https://warcraft.wiki.gg/wiki/Stranglethorn_Vale_(Classic) | © Blizzard，wiki 以合理使用收录。**仅人眼参考** |
| 悲伤沼泽旧世图 | https://warcraft.wiki.gg/wiki/Swamp_of_Sorrows_(Classic) | 同上 |
| 诅咒之地旧世图 | https://warcraft.wiki.gg/wiki/Blasted_Lands_(Classic) | 同上 |
| 逆风小径旧世图 | https://warcraft.wiki.gg/wiki/Deadwind_Pass_(Classic) | 同上 |
| 燃烧平原旧世图 | https://warcraft.wiki.gg/wiki/Burning_Steppes_(Classic) | 同上 |
| 灼热峡谷旧世图 | https://warcraft.wiki.gg/wiki/Searing_Gorge_(Classic) | 同上 |
| 黑石山内部剖面/分层图 | https://warcraft.wiki.gg/wiki/Blackrock_Mountain | 同上。该页 Maps 一节有分层缩略图 |
| 黑石塔 LBRS/UBRS 分区图 | https://warcraft.wiki.gg/wiki/Blackrock_Spire | 同上。Maps 一节有分区缩略图 |
| 黑石深渊全图 | https://warcraft.wiki.gg/wiki/Blackrock_Depths | 同上 |
| 祖尔格拉布平面图 | https://warcraft.wiki.gg/wiki/Zul%27Gurub_(Classic) | 同上 |
| 阿塔哈卡神庙平面图 | https://warcraft.wiki.gg/wiki/Temple_of_Atal%27Hakkar | 同上 |
| 探索成就中文子区域清单（含示意图） | https://wow.17173.com/content/2008-12-25/20081225175346525_all.shtml | 第三方攻略站，转载暴雪素材 |
| 旧世 1.12 数据库（中文） | https://db.nfuwow.com/60/?zone=33（改 zone 参数换图） | 第三方数据库 |

> 说明：这一轮记的是**承载地图的 wiki 页面 URL**，不是图片文件直链——
> 因为没有抓图片清单（也不该抓）。需要看图时人工打开这些页的 Maps 一节即可。

---

## ⑤ 给下游的提醒

1. **`coords` 大面积为空是已知缺口，不是遗漏。** 要补坐标，走这条路最稳：
   在游戏/模拟器里开 Classic Era 客户端装坐标插件逐点记，或换一个能访问 wowhead classic 的出口再跑一遍
   `https://www.wowhead.com/classic/zone={33,8,4,41,46,51,25}`。**不要拿零售 wiki 的坐标回填荆棘谷和诅咒之地**——那两张图的坐标系在 4.0.3 变过。
2. **荆棘谷是本片区的「一张图两个气质」。** 北半部是雨林 + 巨魔废墟 + 狩猎营（湿、绿、闷），南半部海角是海盗 + 悬崖木城 + 竞技场（亮、蓝、吵）。
   选景时不要当成一个场景基调处理；树里已用 `the_cape_of_stranglethorn` 把南半部单独分出一层，正是为了这个。
3. **藏宝海湾是本片区唯一的「中立主城」**，也是全片区唯一一个**两阵营玩家都能正常走进去**的热闹场所。任何需要「人多、市井、讨价还价、碰头」的戏，落在这里最省事。
4. **黑石山是本片区的视觉高点，也是唯一的「垂直空间」。** 全片区别处都是平铺的地表，只有这里有：
   悬在岩浆上的铁链、中央悬空石塔、环形盘旋大道、层层向上的兽人要塞。**长镜头穿行 / 俯冲 / 仰拍的戏应该放这里。**
5. **旧世特供的三个「进不去」是剧作资产，不是 bug：**
   ① 黑暗之门封着（只是纪念碑）② 卡拉赞进不去（只是塔的剪影）③ 灼热峡谷要钥匙（有一道真的锁着的门）。
   做「练级玩家」题材时，这三处天然就是「看得见、进不去」的悬念点。**不要按零售版把它们写成可进入的。**
6. **`adjacent` 我只在 zone 层填了，且只填陆路接壤 / 固定通路。** 藏宝海湾↔棘齿城的船、格罗姆高的飞艇（通奥格瑞玛 / 幽暗城）挂成了 `transport` 子节点，没有写进 `adjacent`——合龙时若主树想把跨大陆航线也算邻接，需要另外处理。
7. **跨片区 parent 只有两个：`eastern_kingdoms`、`khaz_modan`。**
   - 5 个 zone（荆棘谷 / 悲伤沼泽 / 诅咒之地 / 逆风小径 / 燃烧平原）直接挂 `eastern_kingdoms`。
     它们的 lore 归属是「艾泽拉斯南部大陆」这一 region，但我**没有**自己创建这个 region 节点，怕和别的片区撞名。
     `note_zh` 里记了归属，主树若已有对应 region（如 `azeroth_continent`），把这 5 个 zone 的 parent 改过去即可。
     **已核过的反证：`Kingdom_of_Stormwind` 页只辖艾尔文森林 / 西部荒野 / 暮色森林 / 赤脊山，这 5 个 zone 都不属于暴风王国**，不要挂到 `kingdom_of_stormwind` 下。
   - 2 个 zone（灼热峡谷 / 黑石山）挂 `khaz_modan`，有 wiki 出处（见 ③ F）。
   - **合龙前已实测对账（写完当场跑的）**：扫过同目录下 g02 / g03 / g05 / g06 / g07 / g08 / g12 / g13 全部 YAML，
     结果是 —— ① `khaz_modan` **已由 g05 定义**，我的 parent 引用能解析，不是悬空；
     ② 我这 194 个 id **与其它任何片区零碰撞**，特别是 `searing_gorge` / `blackrock_mountain` **没有被 g05 重复定义**，
     不存在「两个片区各建一座黑石山」的问题；③ 各片区 YAML 均可被 `yaml.safe_load` 正常解析。
     → 主树合并时这两条 parent 边可以直接连，不需要人工裁决。
8. **同名节点我已经加了限定，合龙时请保留：**
   `altar_of_storms_blasted_lands` / `altar_of_storms_burning_steppes`（风暴祭坛两处）、
   `crypt_deadwind_pass`（Crypt 是通用词）、`the_forbidding_sea_sos`（荒芜之海多区共用）。
   另外 **`blackrock_mountain` 同时是燃烧平原和灼热峡谷各自子区域表里的一个条目** ——
   那是「从本区能看到/走到黑石山」的意思，不是两个不同的地方，**不要因此建出第二个黑石山节点**。
9. **暴风城不在本片区**，按任务书已直接引用 sk2 的既有成果（`ai_videos/shikong_lvxing/sk2/0_research/parts/w1_city_layout.md`），没有重复调研。
10. **若之后要做旧世练级动线**，本片区的天然顺序是：
    荆棘谷(30-45) → 悲伤沼泽(35-45) → 灼热峡谷(45-50) → 诅咒之地(45-55) → 燃烧平原(50-58) → 黑石山(55-60) → 逆风小径(55-60，纯过路)。
    这条线正好从「湿热雨林」一路走到「火山地底」，色调上是连续降饱和 + 升温的，做整季视觉曲线很顺。

---

## 核验记录（G04-V）

独立核验员复核，2026-09-20。默认立场：怀疑每一个地名。**全部结论均来自本次实际 WebFetch 抓页，不采用记忆判据。**
结果：**作者原稿的地名没有一个是编造的**——194 个节点逐一比对 `warcraft.wiki.gg` 的 Subzones 小节，
零「地名不存在」、零「层级挂错」、零「id 重复」、零「版本错置」。问题集中在**漏收**与**出处不够硬**两类。
节点数 **194 → 199**。裁决：**已修订可用**。

### A. 逐 zone 核过的清单（7 个 zone 全覆盖）

| zone | 作者节点 | wiki Subzones 比对结果 |
|---|---|---|
| 荆棘谷 Stranglethorn Vale | 62 | 41 条子区域 + 2 条 undisplayed **全部命中，无漏无多** |
| 悲伤沼泽 Swamp of Sorrows | 29→32 | 旧世 16 条全中；神庙内部**漏 3 条**（见 B1） |
| 诅咒之地 Blasted Lands | 12→13 | 旧世 10 条全中；**漏 The Forbidding Sea 一侧**（见 B2） |
| 逆风小径 Deadwind Pass | 11 | 旧世 10 条全中，**无漏无多** |
| 燃烧平原 Burning Steppes | 15 | 旧世 12 条全中，**无漏无多** |
| 灼热峡谷 Searing Gorge | 13 | Classic 页显式列的 10 条全中，**无漏无多** |
| 黑石山 Blackrock Mountain | 52→53 | BRM/BRD/BRS/MC 全中；**BWL 漏 1 条**（见 B3） |

### B. 补入的子区域（5 个，均带页面出处）

1. **沉没的神庙三厅** —— `st_hall_of_serpents`（Hall of Serpents）、`st_hall_of_the_cursed`（Hall of the Cursed）、
   `st_the_pit_of_refuse`（The Pit of Refuse）。三者在 `Temple_of_Atal'Hakkar` 页被单列为
   **"Removed (with the Shattering)"**，各自条目的 patch history 均写 **"Patch 4.0.3a (2010-11-23): Removed."**
   ——**「4.0.3 移除」正好等于「1.12 存在」**，是本树锚定旧世时**必须收、且只有旧世才有**的三条。
   这是本次最实质的一处漏收：作者只按现行页面的 Inside/Outside 两栏抄，漏掉了第三栏 Removed。
2. **`the_forbidding_sea_bl`（荒芜之海 · 诅咒之地一侧）** —— 荒芜之海在 `Blasted_Lands` 与 `Swamp_of_Sorrows`
   两个 zone 的 Subzones 里都列着，作者只收了沼泽一侧。按作者既有的 `_sos` 后缀惯例补了 `_bl`，note 里互相指认，
   **不是第二片海**。
3. **`bwl_crimson_laboratories`（Crimson Laboratories）** —— `Blackwing_Lair` 页列为 undisplayed location，
   位置在 Halls of Strife 与 Nefarian's Lair 之间，旧世即存在。

### C. 收紧的地方（原稿没错，但出处不够硬）

1. **`verified_by: ai_read` 滥用 —— 原稿 190 个 ai_read 里有 163 个 `quote` 是空的。** 已逐条处理：
   - **151 条补上页面原文**：其名在所引页面的 Subzones 小节里逐字出现，quote 填该页的原始写法
     （如 `Dreadmaul Hold/Okril'lon Hold`、`Purespring Cavern/Itharius's Cave`、`Black Tooth Hovel (The Pillar of Ash)`
     ——保留 wiki 的斜杠/括号写法，正是为了让人一眼看出「这是从哪一行抄来的」）。
   - **9 条降级 `ai_draft`**：`booty_bay_docks`、`boat_booty_bay_ratchet` 与 7 个 flight master 节点。
     它们是交通/码头类 POI，**不在所引页面的 Subzones 小节里**，本次也没有单独开页核实。
     内容大概率是对的，但按规程「页面上找不到原文就不能算 ai_read」，已在各自 note_zh 里写明降级理由。
     → ai_read 186 / ai_draft 13，**现在全树没有一个 ai_read 是空 quote**。
2. **`deadwind_pass` 的 quote 与页面对不上。** 原稿写 `"...giving it its name."`，
   `Deadwind_Pass_(Classic)` 页实际是 `"...giving it the name Deadwind."` 已订正为页面原文。
   ——这类「记忆里的句子」是 quote 字段最典型的失真方式。
3. **黑翼之巢一家五口全部错引 `Blackrock_Spire` / `Blackrock_Mountain` 页。**
   `blackwing_lair` / `bwl_dragonmaw_garrison` / `bwl_halls_of_strife` / `bwl_shadow_wing_lair` / `nefarians_lair`
   的名字其实都出自 `Blackwing_Lair` 页的 Subzones 小节。source_url 已全部改指该页，`blackwing_lair` 补了首句原文。
4. **`blackrock_mountain` 等级带 `55-60` → `49-60`。** 依据是它自己引用的 `Blackrock_Mountain` 页信息框
   （`49-60, 80-83, 85, 100`，后三段分别是 Cata 黑石洞穴 / 黑翼血环 / WoD）。旧世段就是 **49-60**；
   而且 55-60 与树内 `blackrock_depths` 的 52-60 自相矛盾。其余 6 个 zone 的等级带与阵营**逐一核过、全部正确**
   （30-45 / 35-45 / 45-55 / 55-60 / 50-58 / 45-50，阵营均为 Neutral＝contested）。

### D. 特别提醒：一处「看起来像错、其实是对的」，后来人不要改回去

**`tazzalor` 的 `name_en` 是 `Tazz'Alaor`，不是现行 wiki 条目名 `Tazz'Alor`。**
`Tazz'Alor` 页的 trivia 明写：该区名**在游戏里一直被拼作 `Tazz'Alaor`，直到大地的裂变才改拼**。
本树锚定 1.12，所以 **`Tazz'Alaor` 才是版本正确的拼写**，作者是对的。
已在 note_zh 里写死这条来龙去脉、并把 source_url 指向 `Tazz%27Alor` 页，**防止下一轮核验把它「订正」错**。

### E. 逐一排除的「疑似漏收」——全部确认为大地的裂变新增，不该进旧世树

作者的排除是对的，这里留下证据，免得下次再查一遍。以下**全部**查到各自条目的
`Patch 4.0.3a (2010-11-23): Added.`：

- 燃烧平原：**Chiselgrip · Flamestar Post · Black Tooth Hovel · Fields of Honor · Valley of Ashes · The Whelping Downs**
  （Whelping Downs 的 patch 行是 `Added. Partially replaced Draco'dar.` —— 反过来印证了作者收的 `Draco'dar` 是旧世货）；
  `Firegut Furnace` / `The Skull Warren` 的 patch 行是 `Cavern given its own subzone`，即 4.0.3 才独立成名。
- 灼热峡谷：**Iron Summit · Pyrox Flats**（Thorium Advance 同属模板但不在 Classic 页正文列表）。
- 诅咒之地：**Dreadmaul Furnace · The Red Reaches · Shattershore · Sunveil Excursion · The Tainted Forest ·
  Surwich · Maldraz**；**Nethergarde Mines 是 4.0.3 对 Garrison Armory 的改名**，作者收 Garrison Armory 正确。
- 悲伤沼泽：**The Bloodmire · Bogpaddle · Marshtide Watch · Fortune's Fist**；
  `Misty Reed Farm` / `Purespring Cavern` 是 4.0.3 对 `Misty Reed Post` / `Itharius's Cave` 的改名，作者用旧名正确。
- 逆风小径：**Abandoned Kirin Tor Camp · Alturus' Sanctum · Karazhan Catacombs** 及 Forgotten Crypt 的 6 个内部区
  （Pauper's Walk 等）全是军团再临（7.0/7.3）加的。作者的 `Crypt (Deadwind Pass)` 也已核实：
  `Forgotten_Crypt` 页写 **"Patch 7.0.3: Subzone renamed from Crypt to Forgotten Crypt"** —— 旧世就叫 `Crypt`，作者对。
- 跨区：**Redridge Pass** 虽在燃烧平原/悲伤沼泽的 undisplayed 栏，但 patch 行是 `4.0.3a: Area added.`，不收。
- 荆棘谷的两条 undisplayed **`Haunted isle` / `Nazferiti river` 已核实真实存在**（在 `Stranglethorn_Vale` 页的
  Undisplayed locations 栏），作者收得对，不是编的。

### F. 本次实际抓到的页面清单（全部 `warcraft.wiki.gg`）

`Stranglethorn_Vale_(Classic)` · `Stranglethorn_Vale` · `Zul'Gurub_(Classic)` · `Booty_Bay` · `Grom'gol_Base_Camp` ·
`Swamp_of_Sorrows` · `Swamp_of_Sorrows_(Classic)` · `Temple_of_Atal'Hakkar` · `Hall_of_Serpents` ·
`Hall_of_the_Cursed` · `The_Pit_of_Refuse` · `Blasted_Lands` · `Blasted_Lands_(Classic)` · `Dreadmaul_Furnace` ·
`Nethergarde_Mines` · `Deadwind_Pass` · `Deadwind_Pass_(Classic)` · `Forgotten_Crypt` · `Burning_Steppes` ·
`Burning_Steppes_(Classic)` · `The_Whelping_Downs` · `Fields_of_Honor` · `Valley_of_Ashes` · `Black_Tooth_Hovel` ·
`Firegut_Furnace` · `The_Skull_Warren` · `Redridge_Pass` · `Searing_Gorge` · `Searing_Gorge_(Classic)` ·
`Iron_Summit` · `Pyrox_Flats` · `Blackrock_Mountain` · `Blackrock_Depths` · `Blackrock_Spire` · `Tazz'Alor` ·
`Molten_Core` · `Blackwing_Lair` · `Crimson_Laboratories`

### G. 仍存疑（本次**没能**核实，交下一轮）

1. **国服官方中文译名一条都没能核。** `wow.huijiwiki.com` 对本环境的抓取一律返回 **HTTP 403**，
   `wowhead.com/classic/zh/` 返回 **404**，本 session 的 WebSearch 配额也已用尽。
   因此**规程第 3 条只完成了「不编音译」这半条**：全树 82 个 `name_zh` 仍是英文原名 + `官方译名未查到` 标注
   （这是合规写法，作者没有自造音译，**一处都没有**），另有 18 个 `name_zh` 带
   `中文名未经官方页面核实` 标注（`监狱区`/`命运大厅`/`黑铁酒吧`/`暗影裂口城` 等看着都对，但**没有页面背书**）。
   → **下一轮请换一个能访问 huijiwiki 的环境专做译名，不要在本轮结论上推断它们已核过。**
2. **`temple_of_atal_hakkar` 的 `level: "50-56"`。** 所引页面写的是 Classic `lvl 50-60`。
   50-56 是通行的「推荐等级」口径，两者都在流通，**未擅改**，留给下游按口径统一。
3. **三个标着【描述性命名，非官方地名】的 POI**（`dark_portal_crater`、`molten_span_chains`、
   两个 `blackrock_mountain_*_entrance`）**不是 wiki 地名**，作者已诚实标注、且 type 是 `poi` 不是 `subzone`，
   本次予以保留。**但它们不可作为「官方地名」出现在分镜或字幕里**，只能当场景描述用。
4. `the_forbidding_sea_sos` 与新补的 `the_forbidding_sea_bl` 是**同一片海的两个 zone 侧入口**，
   `name_en` 故意重复。主树合龙时若要去重，应合并成一个节点挂到更高层，**不要当成冲突删掉其中一个**。
