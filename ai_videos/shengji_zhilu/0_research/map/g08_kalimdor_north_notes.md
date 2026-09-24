# G08 · 卡利姆多北部 + 达纳苏斯 —— 测绘备注（非树数据）

树数据的唯一出处是 `g08_kalimdor_north.yaml`。本文件只放**不属于树**的东西。

版本锚点：**经典旧世 Vanilla / Classic Era**。判定「这个地名旧世有没有」的第一权威是
**暴雪 Classic Era 客户端的 `AreaTable` 数据表**（不是现行 wiki 的子区域列表——那份表是
混着 4.0.3 之后新增地名的）。

---

## ① 自查对账

### 实际抓到的源

| 源 | 方式 | 结果 |
|---|---|---|
| `warcraft.wiki.gg` MediaWiki API（`action=query&prop=revisions`，40 标题/批） | 本机 curl + Python | **182 个页面的完整 wikitext**，含 8 个地区页 + ~170 个子区域/地标页 |
| Classic Era 客户端 `AreaTable`（zhCN + enUS 两份 CSV）<br>`https://wago.tools/db2/AreaTable/csv?build=1.15.9.69722&locale=zhCN` | 本机 curl | 全表下载成功；抽出本片区 8 个地区的全部子 area（含**国服官方简中译名**与 `ParentAreaID` 父子关系） |
| Classic Era 客户端 `TaxiNodes`（zhCN + enUS）<br>`https://wago.tools/db2/TaxiNodes/csv?build=1.15.9.69722&locale=zhCN` | 本机 curl | 87 个旧世飞行点全表；据此确认本片区旧世**到底有哪几个飞行点** |
| `warcraft.wiki.gg` 页面（WebFetch 摘要） | WebFetch | Teldrassil / Darkshore / Ashenvale / Felwood / Winterspring / Moonglade / Azshara / Darnassus / Blackfathom Deeps / Auberdine 共 10 页 |

抓取失败 / 放弃的源：

- **`wow.huijiwiki.com`（灰机 wiki）**：WebFetch 403、本机 curl 也吃到 JS 反爬挑战页（403）。**未作为译名来源**。
  不影响质量——本树的 `name_zh` 直接取自**客户端 zhCN 语言包**，那正是国服译名的源头，比任何 wiki 转录更权威。
- **`wowhead.com` / `classic.wowhead.com`**：本机出口被 CloudFront 拦（403，含任务书里给的 `&xml` 绕法）。
  因此**坐标缺口较大**（见 ③）。
- `warcraft.wiki.gg` 的 WebFetch 通道中途开始 429（同一时间多个片区在抓同一域名）；
  改用 MediaWiki API + 本机 curl 后恢复，并以 40 标题/批 + 1 秒间隔的方式控速。

### 节点产出

| zone | 节点数 |
|---|---|
| teldrassil 泰达希尔 | 20 |
| darnassus 达纳苏斯（挂在泰达希尔下） | 12 |
| darkshore 黑海岸 | 19 |
| ashenvale 灰谷 | 46 |
| felwood 费伍德森林 | 21 |
| winterspring 冬泉谷 | 19 |
| moonglade 月光林地 | 8 |
| azshara 艾萨拉 | 29 |
| 片区级（`northern_kalimdor`、`the_veiled_sea`） | 2 |
| **合计** | **176** |

**月光林地只有 8 个节点，不是没查全**：Classic Era 客户端里月光林地一共只有 5 个 area
（月神湖 / 永夜港 / 雷姆洛斯神殿 / 怒风兽穴 / 木喉要塞），这是旧世的真实规模——它是一块
「一眼望尽」的圣地，不是练级区。已额外补了飞行点、德鲁伊传送落点、木喉隧道出口三个 POI。

### 机检自查（已跑通）

- 176 个 `id` 全局唯一，无重复。
- 每个节点 16 个字段齐全，无多余字段。
- `type` / `subtype` / `faction` / `era` / `verified_by` 全部落在枚举内。
- `level` 只出现在 zone / dungeon 上；`adjacent` 只出现在 zone 上。
- 每个节点都有 `parent`，且除 `kalimdor` 外全部能在本文件内解析到。

---

## ② 版本差异（4.0.3 大地的裂变改了什么）

**通则**：凡出现在现行 wiki 子区域表、却**不在 Classic Era 客户端 AreaTable 里**的地名，
一律判为 4.0.3 及以后新增 / 改名，**不进树**，逐条列在下面。

### 黑海岸 Darkshore（本片区头号雷区，改动最彻底）

- **奥伯丁（Auberdine）被死亡之翼摧毁**，变成「奥伯丁废墟 Ruins of Auberdine」；
  幸存者北迁建立 **洛达内尔 Lor'danel**，飞行点、旅店、船坞全部搬过去。
  **本树只收奥伯丁**，它在旧世是黑海岸唯一城镇 + 三向船运枢纽。
- 4.0.3 及以后才有、**不入树**的黑海岸地名：
  Lor'danel、Lor'danel Landing、Ruins of Auberdine、Auberdine Refugee Camp、The Moonspray、
  The Eye of the Vortex（漩涡之眼）、Shatterspear Vale / Shatterspear Pass / Shatterspear War Camp、
  Withering Thicket、Ashwood Depot、Bitterstone Quarry、Cinderfall Grove、Forlorn Crossing、
  Moontouched Den、Ruins of Lornesta + Lornesta Mine、Earthshatter Cavern、Maw of the Void、
  Bashal'Aran Collapse、Gloomtide Strand、Apothecary、Nazj'vel、The Blazing Strand、
  Blackwood Camp、Kor'gar、The Dredge、The Ashenvale Front、Wreckage of the Silver Dawning。
- 旧世地貌是**连续的海岸松林 + 断崖**；4.0.3 后地面被洪水与漩涡撕开。
  **拍旧世黑海岸不要用任何带裂谷 / 漩涡 / 洪水的参考图。**

### 艾萨拉 Azshara（第二雷区，被哥布林整块改造）

- 4.0.3 后艾萨拉变成**部落 5-12 级新手续接区**，风暴海湾被挖成部落徽记形状，
  等级带从旧世的 45-55 掉到 10-20 级段。**旧世它是 45-55 的高级野外区。**
- 4.0.3 及以后才有、**不入树**的艾萨拉地名：
  Bilgewater Harbor、Hull of the Foebreaker、Gallywix Pleasure Palace、The Secret Lab、
  Gallywix Rocketway Exchange / Northern Rocketway Exchange / Northern Rocketway Terminus /
  Orgrimmar Rocketway Exchange / Southern Rocketway Terminus（火箭之路各站）、
  Orgrimmar Rear Gate、Mountainfoot Strip Mine、Storm Cliffs、Sable Ridge、Horizon Scout、
  The Ancient Grove、Arcane Pinnacle、Trial of Fire / Trial of Frost / Trial of Shadow、
  Ruins of Nordressa、Ruins of Arkkoran、Darnassian Base Camp。
- 旧世有、4.0.3 被移除或改写的（wiki 上已用过去式或挂 `{{Classic}}`）：
  赫塔拉的巢穴（被比尔吉沃特港覆盖）、鳞须海龟洞穴（小岛消失）、哈达尔营地、影歌神殿、
  萨拉斯营地（高等精灵考察营 → 阵营营地）、凄凉山（被炸开）。
- **艾萨拉侧的「木喉要塞」（AreaID 1216）4.0.3 改名 Blackmaw Hold（黑颚要塞）**。
- **Vanndir Encampment 范迪尔营地**：客户端里有这个 area，但 wiki 标为 Removed / 从未启用，**不入树**。

### 灰谷 Ashenvale

- **伊瑞斯湖 Iris Lake 被抽干**，改名 Remains of Iris Lake（伊瑞斯湖遗迹）。旧世是有水的湖。
- **石爪小径 The Talondeep Path 被封**（旧世是灰谷↔石爪山的隧道通路）。
- 银风避难所 Silverwind Refuge 在 4.0.3 被写成部落前哨；**旧世不是**，只是精灵建筑群。
- 林歌神殿 Forest Song 在 4.0.3 才有联盟哨站与飞行点；**旧世只是遗址、没有飞行点**。
- 不在 Classic Era AreaTable、判为后来新增 / 纯地图标注、**不入树**：
  Stardust Spire、The Mor'shan Rampart、Hellscream's Watch、Thal'darah Overlook、
  Blackfathom Camp、The Skunkworks、House of Edune、Moonwell of Cleansing、Moonwell of Purity、
  Bolyun's Camp、Orendil's Retreat、Thunder Peak、Raynewood Tower、Thistlefur Hold、Ruuzel's Isle。
  （其中 Orendil's Retreat / Thunder Peak / Raynewood Tower / Thistlefur Hold 存疑，见 ③）

### 泰达希尔 Teldrassil + 达纳苏斯 Darnassus

- **旧世泰达希尔全区只有一个飞行点：鲁瑟兰村**。多兰纳尔与达纳苏斯的飞行点是 4.0.3 才加的
  （已用 Classic Era `TaxiNodes` 全表核过，87 个旧世飞行点里没有这两个）。
- 达纳苏斯的 **The Howling Oak 狼嚎橡树**（吉尔尼斯狼人区）是 4.0.3 新增，**不入树**。
- 客户端里达纳苏斯只有 **5 个区**：塞纳里奥区 / 工匠区 / 贸易区 / 战士区 / 神殿花园。
  **月神殿不是独立 area**，是神殿花园内的建筑（本树按 POI 挂在神殿花园下）。
- 泰达希尔的 area 表里还有 7 个带 `UNUSED` 后缀的废弃条目
  （Darnassus UNUSED / Cenarion Enclave UNUSED / Craftsmen's Terrace UNUSED /
  Temple of Elune UNUSED / The Temple Gardens UNUSED / Tradesmen's Terrace UNUSED /
  Warrior's Terrace UNUSED）——那是达纳苏斯独立成 zone 之前的旧结构残留，**不入树**。
- 更晚的 8.0「泰达希尔焚烧」把整棵世界树烧毁，所以现行 wiki 写 Status: Deceased、
  正文全用过去式。**本树按旧世收，树是活的。**

### 费伍德森林 Felwood

- 旧世只有**两个飞行点**：刺枝林地（联盟）、血毒岗哨（部落）。
  翡翠圣地的飞行点不在 Classic Era `TaxiNodes` 里，是后来加的。
- 不在 Classic Era AreaTable、**不入树**：Whisperwind Grove、Wildheart Point、
  Irontree Clearing、Shadowlurk Ridge、Sindweller's Rise、Bloodvenom Post 的重建版。

### 冬泉谷 Winterspring

- 旧世**只有永望镇一个飞行点**；坠星村的飞行点是 4.0.3 加的（旧世坠星村只有商人和任务）。
- 不在 Classic Era AreaTable、**不入树**：Snowden Chalet、Goodgrub Smoking Pit、
  Beryl Egress、Caverns of Consumption、The Laughing Yeti（永望镇旅店在旧世是有的，
  但「大笑的雪人」作为**独立子区域名**不在旧世 area 表里）。
- 暗语峡谷 Darkwhisper Gorge：旧世是冬泉谷南端的 60 级精英恶魔区；
  4.0.3 后被并进海加尔山方向的暮光之锤剧情（现行 wiki 的坐标已写成 Mount Hyjal `[76, 61]`）。
  **旧世取景按「冬泉谷最南端的黑色深谷」来。**

### 月光林地 Moonglade

- 结构基本未变。4.0.3 新增了通往海加尔山（诺达希尔）的飞行点，本树不收。
- 旧世非德鲁伊进月光林地只有两条路：**木喉要塞隧道**（要木喉声望）或**飞行点**；
  德鲁伊可用职业法术「传送：月光林地」。

---

## ③ 存疑与未查

1. **坐标缺口（最大的一处不完整）**：176 个节点里只有约 45 个填了 `coords`，
   全部来自 `warcraft.wiki.gg` 页面里的 `{{coords}}` 模板。原因是 wowhead 从本机出口被 CloudFront 拦死
   （任务书给的 `&xml` 绕法同样 403）。**没有编造任何一个坐标**——查不到的一律留空串。
   下游若需要补全，建议换一台能访问 wowhead classic 的机器，或直接读客户端 `AreaPOI` / `AreaTrigger` 表
   （`wago.tools` 同一 build 下可取，但需要 `UiMapAssignment` 做世界坐标→地图百分比的换算，本轮未做）。
2. **黑暗深渊入口的精确坐标未取到**。已确认的是：入口在**灰谷·佐拉姆海岸**的岸边洞口，
   在部落的佐拉姆加前哨站**以北**，需沿海滩走或游过去；副本本身在客户端里是灰谷的子 area（2797）。
   wiki 信息框只写 `loc = The Zoram Strand, Ashenvale`，没给数字。
3. **灰谷的两口月亮井**：客户端里只有一个 area 名「月亮井」（425）。wiki 的 Moonwell 页给了
   `[53, 46]` 与 `[59, 59]` 两组灰谷坐标，但没说哪组是北井、哪组是南井，故本树只建一个节点、
   在 `note_zh` 里并列两组坐标。下游若要分别取景需再核。
4. **大法师瑟莱姆（Archmage Xylem）的塔**：旧世艾萨拉确有此人与其塔（任务链「辛玛洛水晶」相关），
   但 **`Xylem's Tower` / `Arcane Pinnacle` 都不是 Classic Era AreaTable 里的 area 名**，
   而且 wiki 给的坐标（Xylem `[28.1, 50.1]`、Arcane Pinnacle `[55.9, 12.2]`）互相矛盾、
   且很可能是后续版本的位置。**本树未收，标为待核。**
5. **以下地名 wiki 列为子区域、但不在 Classic Era AreaTable 里，未收、待核**（它们可能是
   旧世的纯地图标注 / NPC 点，也可能是后来新增）：
   灰谷 —— Orendil's Retreat、Thunder Peak、Raynewood Tower、Thistlefur Hold、Ruuzel's Isle、House of Edune；
   泰达希尔 —— Wellspring Hovel。
6. **国服译名**：`name_zh` 全部取自 Classic Era 客户端 **zhCN 语言包**（AreaTable / TaxiNodes），
   **没有一个是自行音译的**。少数功能性节点（飞行点 / 码头 / 传送门 / 银行 / 拍卖行 / 墓地）
   的名字是「官方地名 + 功能词」的**组合标签**，不是游戏内地名——下游若要在台词里念出来，
   请用官方地名部分（例如念「奥伯丁的飞行管理员」，而不是念「奥伯丁飞行点」）。
   唯一一处明确的译名缺口：达纳苏斯银行所在建筑 **Bough of the Eternals** 的官方简中建筑名未查到，
   节点因此用功能名「达纳苏斯银行」，英文名保留在 `name_en` 里。
7. **客户端译名与 wiki 常用译名不一致的几处**（以客户端为准，下游不要「纠正」回去）：
   `Gnarlpine Hold` = **脊骨堡**（不是「木爪要塞」，虽然 Gnarlpine 熊怪译作木爪）、
   `Fel Rock` = **地狱石**、`Shadowthread Cave` = **黑丝洞**、`The Cleft` = **大断崖**、
   `The Long Wash` = **长桥码头**、`Mist's Edge` = **薄雾海**、`Raynewood Retreat` = **林中树居**、
   `The Shady Nook` = **林荫小径**、`Scalebeard's Cave` = **鳞须海龟洞穴**、
   `Bitter Reaches` = **痛苦海岸**、`Winterfall Village` = **寒水村**。
8. **一处客户端内部不一致**：费伍德血毒岗哨的飞行点，`TaxiNodes` 的中文标签写作
   「血毒河，费伍德森林」，而该地 area 名是「血毒岗哨」。已在节点 `note_zh` 里注明。

---

## ④ 本片区地图图片链接清单（**只记 URL 与版权状态，不下载**）

仓库已裁定：**暴雪美术资产只进人眼、不入画、不上传给生成模型。**
下面每条都已用 MediaWiki API 确认过文件页真实存在（`missing` 检查通过）。

| 内容 | 页面 URL | 说明 |
|---|---|---|
| 卡利姆多全图 | https://warcraft.wiki.gg/wiki/File:WorldMap-Kalimdor.jpg | 大陆级底图 |
| 泰达希尔（旧世版） | https://warcraft.wiki.gg/wiki/File:WorldMap-Teldrassil-old.jpg | **`-old` 后缀 = 4.0.3 之前的版本，本片区优先看这一版** |
| 泰达希尔（现行） | https://warcraft.wiki.gg/wiki/File:WorldMap-Teldrassil.jpg | 对照用 |
| 黑海岸（旧世版） | https://warcraft.wiki.gg/wiki/File:WorldMap-Darkshore-old.jpg | **必看**：旧世黑海岸与现行差异最大 |
| 黑海岸（现行） | https://warcraft.wiki.gg/wiki/File:WorldMap-Darkshore.jpg | 只作对照，**不要照它取景** |
| 灰谷（旧世版） | https://warcraft.wiki.gg/wiki/File:WorldMap-Ashenvale-old.jpg | 另有 `WorldMap-Ashenvale-old2.jpg` 为更早一版 |
| 费伍德森林（旧世版） | https://warcraft.wiki.gg/wiki/File:WorldMap-Felwood-old.jpg | |
| 冬泉谷（旧世版） | https://warcraft.wiki.gg/wiki/File:WorldMap-Winterspring-old.jpg | |
| 艾萨拉（旧世版） | https://warcraft.wiki.gg/wiki/File:WorldMap-Aszhara-old.jpg | 注意文件名是 **Aszhara**（wiki 上的拼写笔误，不是 Azshara） |
| 月光林地 | https://warcraft.wiki.gg/wiki/File:WorldMap-Moonglade.jpg | 该区未改动，无 `-old` 版本 |
| 达纳苏斯 | https://warcraft.wiki.gg/wiki/File:WorldMap-Darnassus.jpg | 城市图；狼嚎橡树是后加的，看图时请忽略该区块 |

版权状态：**全部为 Blizzard Entertainment 的游戏内美术资产**，wiki 以合理使用方式托管。
用途限于**人眼参考**；不得下载进仓库、不得作为生成模型的参考图、不得出现在成片画面里。

---

## ⑤ 给下游的提醒

### 合龙相关

- **未定义的跨片区 parent：`kalimdor`**（本片区 8 个地区的上级 `northern_kalimdor` 挂在它下面）。
  `azeroth` 本片区完全没引用。
- **`northern_kalimdor` 可能被别的片区重复定义**（杜隆塔尔 / 贫瘠之地 / 石爪山在 lore 上也属卡利姆多北部）。
  合龙时**保留一份即可**，本片区不介意由谁提供。
- **`adjacent` 里引用了 4 个外部 zone id**：`durotar`、`stonetalon_mountains`、`the_barrens`、`wetlands`。
  若对方片区用了别的拼写（例如 `northern_barrens`、`dustwallow_marsh`），以对方为准改我这边。
- **客户端里「一名多 area」的四处已去重，合龙时不要再拆开**：
  迷雾之海（泰达希尔 2322 / 黑海岸 2326 / 灰谷 2325 → 合成 `the_veiled_sea`）、
  怒水河（灰谷 879 / 艾萨拉 878 → 合成 `southfury_river`）、
  无尽之海（艾萨拉 2321，冬泉谷侧同名 → 合成 `the_great_sea`）、
  暗语峡谷（2256 / 16005 两条同名记录 → 合成一个节点）。
  **例外：木喉要塞是两个不同的地方**，已拆成 `timbermaw_hold`（费伍德，三向隧道）与
  `timbermaw_hold_azshara`（艾萨拉西北的独立熊怪洞穴），**不要合并**。

### 跨片区的交通接口（对面片区要对上）

- **船**：奥伯丁 ⇆ 米奈希尔港（湿地，东部王国方向）——旧世联盟横跨两块大陆的主干道。
  奥伯丁 ⇆ 鲁瑟兰村（本片区内部）。
- **战歌峡谷**：联盟入口在**灰谷·银翼树林**（本片区），**部落入口在贫瘠之地北部的莫尔杉营地**（跨片区）。
  战场本体我方按 `type: battleground` 挂在灰谷下。
- **陆路**：灰谷 ⇄ 石爪山走**石爪小径**隧道（旧世通、4.0.3 封）；灰谷 ⇄ 贫瘠之地走南部路口；
  艾萨拉 ⇄ 杜隆塔尔走南端海岸；灰谷 ⇄ 艾萨拉跨**怒水河桥**。
- **木喉要塞隧道**是费伍德 / 冬泉谷 / 月光林地三向互通的唯一陆路，且**要熊怪声望才不被打**——
  这在旧世是一个非常好的「练级旅途受阻」戏剧点。

### 取景与拍摄相关（给分镜）

- **本片区最具画面冲击力的几处**：
  ① **主宰之剑**（黑海岸最南，一柄高过树冠的古神战刃插在焦黑荒地上）；
  ② **翡翠圣地**（费伍德毒绿腐林里唯一一块鲜绿净土，界线分明，是天然的「对比镜」）；
  ③ **凯斯利尔湖**（冰面透明、冰下埋着白石古城、湖上飘着精灵亡魂）；
  ④ **埃达拉斯废墟 + 拉文凯斯雕像**（橙红秋林里的白色大理石巨城 + 崖顶断掉的巨人石像）；
  ⑤ **世界树内部的达纳苏斯**（月白靛蓝、弧形木桥、穹顶月神殿）；
  ⑥ **战歌伐木营地**（被剃光的秃地与伐木机，是「部落 vs 联盟」矛盾的具象景）。
- **时段是硬设定**：**泰达希尔与月光林地永远是夜**（不是昼夜循环里的夜，是设定上的永夜），
  艾萨拉永远是深秋。拍这三处不要出现正午顶光。
- **黑海岸拍旧世时，画面里不能有裂谷 / 漩涡 / 洪水 / 洛达内尔**——那些都是 4.0.3 之后的。
- **等级带与主角强度要对得上**：泰达希尔 1-12（任务线集中在 1-10）→ 黑海岸 9-25（主线 10-20，北端玛塞斯特拉废墟一带才到 18-25）
  → 灰谷 18-30 →（中间隔一大段别的片区）→ 艾萨拉 45-55 → 费伍德 48-55 → 冬泉谷 55-60。
  （前两条 G08-V 核验按 wiki 旧世专页信息框订正，详见文末「核验记录（G08-V）」。）
  **月光林地没有等级带**（中立圣地，不可攻击），是全程都能去的「歇脚 / 谈话」场景。

---

## 核验记录（G08-V）

**核验人**：独立核验员（与测绘作者不同一人）。**默认立场：怀疑每一个地名。**
**核验日期**：2026-09-20。**核验后节点数：177**（核验前 176，净 +1）。**结论：已修订可用。**

### 一、核验方法（为什么这轮的判据比上一轮硬）

上一轮作者自报「wago.tools AreaTable 导出」，但 YAML 里只留了单行 `quote`，无法复现。
本轮**把两张表整张拉下来逐行对账**，不再靠单行引用：

| 拉取物 | URL | 用途 |
|---|---|---|
| Classic Era AreaTable（zhCN） | `https://wago.tools/db2/AreaTable/csv?build=1.15.9.69722&locale=zhCN` | 1212 行，**节点存在性 + 国服官方简中译名**的第一权威 |
| Classic Era AreaTable（enUS） | 同上 `locale=enUS` | 与 zhCN 按 ID 对齐，拿英文原名 |
| Classic Era TaxiNodes（zh/en） | `https://wago.tools/db2/TaxiNodes/csv?build=1.15.9.69722&locale=...` | 87 行，核飞行点存在性与 ID |

用这两张表按 `ParentAreaID` 递归展开八个 zone 的完整子区域树，再与 YAML 做**双向 diff**
（YAML 有而表里没有 → 疑似编造；表里有而 YAML 没有 → 漏收）。

**实际抓到的页面清单**（全部 `warcraft.wiki.gg`，经 MediaWiki API `prop=extracts` / `action=raw` 取正文）：

- **八个 zone 页 + 旧世专页**：Teldrassil、Darkshore、Ashenvale、Felwood、Winterspring、Moonglade、Azshara、Darnassus；
  以及 `Teldrassil (Classic)`、`Darkshore (Classic)`、`Ashenvale (Classic)`、`Felwood (Classic)`、
  `Winterspring (Classic)`、`Azshara (Classic)`（`Moonglade (Classic)` 不存在，404）。
- **135 个节点引用的子区域页全量下载**，逐条验 `quote` 是否真出现在那一页。
- **单点求证页**：Vanndir Encampment、Wellspring Hovel、Ardan Softmoon、Xylem's Tower、Archmage Xylem、
  Sanath Lim-yo、Goodgrub Smoking Pit、Jez Goodgrub、Beryl Egress、Snowden Chalet、Laughing Yeti、
  Nighthaven Inn、Teldrassil furbolg village、Orendil's Retreat、Thistlefur Hold、Thunder Peak、
  Raynewood Tower、Ruuzel's Isle、House of Edune、Bolyun's Camp、Krolg's Hut、Blazing Strand、
  Nazj'vel、Irontree Clearing、Whisperwind Grove、Wildheart Point、Shadowlurk Ridge、
  Sindweller's Rise、Caverns of Consumption、Orendil Broadleaf。

### 二、子区域完整性：逐 zone 对账结果

把 Classic Era AreaTable 里每个 zone 的**全部子 area**（剔除 `*UNUSED` 与 `TESTAzshara` 占位行）
与本树逐条比对：

| zone | AreaTable 真实子区域数 | 本树已收 | 漏收 |
|---|---|---|---|
| 泰达希尔 141 | 17 | 17 | 0 |
| 达纳苏斯 1657 | 5（五大区） | 5 | 0 |
| 黑海岸 148 | 17（含迷雾之海） | 17 | 0 |
| 灰谷 331 | 42（含迷雾之海、黑暗深渊） | 42 | 0 |
| 费伍德森林 361 | 18 | 18 | 0 |
| 冬泉谷 618 | 17 | 17 | 0 |
| 月光林地 493 | 4 | 4 | 0 |
| 艾萨拉 16 | 28 | 27 | **1** |

**唯一的漏收：艾萨拉的怒水河（`Southfury River`，AreaID 878，ParentAreaID=16）。**
原树只收了灰谷段 879，艾萨拉的子区域清单因此少一条。已补为 `southfury_river_azshara`，
并在灰谷段 `southfury_river` 的 `note_zh` 里加了互指。
（怒水河在客户端里是逐地区各自一条 area：杜隆塔尔 814 / 贫瘠之地 815 / 艾萨拉 878 / 灰谷 879。）

**结论：除这一条外，八个 zone 的子区域覆盖率 100%。** 这与作者自报一致，复核属实。

### 三、查了但**确认不该收**的地名（怀疑 → 排除，附证据）

这一节是本轮的主要工作量。wiki 的 Subzones 一节是**现行版本**的，混着大量 4.0.3a 新增；
若不逐条查补丁记录，很容易「补全」成污染。

1. **艾萨拉 · Vanndir Encampment（范迪尔营地，AreaID 1217）** —— AreaTable 里**有**，但 wiki 明写
   *"Vanndir Encampment was a planned camp located in Azshara"*，且该地点 *"did not make it out of the beta stages"*。
   **是 beta 废案，游戏里不存在。** 作者不收是对的；这是本轮最值得记一笔的「AreaTable 有 ≠ 游戏里有」反例。
2. **泰达希尔 · Wellspring Hovel** —— wiki 列在泰达希尔子区域里，但不在 Classic AreaTable 中。
   决定性证据：该点唯一的驻场 NPC **Ardan Softmoon 的补丁记录写着 `Patch 4.0.3a|note=Added`**。
   → **大地的裂变新增，旧世没有。** 作者备注 ③-5 的待核项，**至此结掉**。
3. **艾萨拉 · Xylem's Tower** —— 作者备注 ③-4 的待核项，**至此结掉**：塔与大法师 Xylem、学徒 Sanath Lim-yo
   旧世都在（两人页面均无 4.0.3a 新增记录），wiki 明写塔在 **Bear's Head**；但 `Xylem's Tower`
   **7.2.0 才「成为独立子区域」**，Classic AreaTable 无此 area 名。
   → **不单开节点，信息已写进 `bears_head` 的 `note_zh`。** 顺带解释了作者发现的「坐标互相矛盾」：
   wiki 那组 `[28.1, 50.0]` 是传送人 Sanath Lim-yo 的站位，不是塔的位置。
4. **灰谷 · Thistlefur Hold（蓟皮要塞）** —— 洞窟本体旧世就有（部落任务「解救鲁尔·雪蹄」在此），
   但页面补丁记录写 `Patch 4.0.3a|note=Now its own subzone` —— **旧世它不是独立地名**。不收，口径与 3 相同。
5. **确认为 4.0.3a（大地的裂变）新增、一律不收**：
   灰谷 —— Thunder Peak、Raynewood Tower、Ruuzel's Isle、House of Edune、Bolyun's Camp、Krolg's Hut、
   Blackfathom Camp、Splintertree Mine、Stardust Spire、Talondeep Vale、Hellscream's Watch、
   The Mor'shan Rampart、The Skunkworks、Remains of Iris Lake、**Moonwell of Cleansing / Moonwell of Purity**
   （旧世两口井共用同一个 area 名「月亮井」425，本树只建一个节点是对的）；
   黑海岸 —— Blazing Strand、Nazj'vel、Lor'danel（及 Landing）、Shatterspear 系列、Ruins of Lornesta、
   Cinderfall Grove、Ashwood Depot、Bitterstone Quarry、Earthshatter Cavern、Maw of the Void、
   Wreckage of the Silver Dawning 等一整片；
   费伍德 —— Irontree Clearing、Whisperwind Grove、Wildheart Point、Shadowlurk Ridge、Sindweller's Rise；
   冬泉谷 —— Snowden Chalet（`4.0.3a|Added`）、Goodgrub Smoking Pit（其 NPC Jez Goodgrub `4.0.3a|Added`）、
   Beryl Egress（旧世 Haleh 在麦索瑞尔一带，但该「营地」非旧世 area）；
   艾萨拉 —— Bilgewater Harbor、Gallywix Pleasure Palace、The Secret Lab、Orgrimmar Rear Gate、
   Mountainfoot Strip Mine、Arcane Pinnacle、The Ancient Grove、Sable Ridge、Storm Cliffs、
   Ruins of Nordressa、Trial of Fire/Frost/Shadow；
   达纳苏斯 —— **The Howling Oak（狼嚎橡树）**，4.0.3 随狼人加入才有，旧世达纳苏斯只有五大区 + 月神殿。
6. **更晚版本新增、更不该收**：Caverns of Consumption（7.2.5）、Nighthaven Inn（7.1.5 才有名字）、
   The Laughing Yeti（永望镇旅店，7.1.5 才有名字——建筑旧世就在，但**名字不是旧世的**）。
7. **Teldrassil furbolg village** —— 页面挂着 `{{Bettername}}` 模板，是 wiki 自拟的描述性称呼，
   且该处「无人居住」。不收。
8. **Orendil's Retreat（灰谷）** —— 页面无补丁记录、不在 Classic AreaTable。其名祖 Orendil Broadleaf
   在旧世站在**迈斯特拉岗哨**，不在这个营地。作为旧世地名证据不足，维持不收，**仍列待核**。

### 四、实际改动清单（一共 9 处）

| # | 节点 | 问题类型 | 改了什么 |
|---|---|---|---|
| 1 | `teldrassil` | 等级带错误 | `level: 1-10` → `1-12`，按 wiki 旧世专页 `Teldrassil (Classic)` 信息框 `level=1-12`；`note_zh` 注明任务线仍集中在 1-10 |
| 2 | `darkshore` | 等级带错误 | `level: 10-20` → `9-25`，按 `Darkshore (Classic)` 信息框 `level=9-25`；`note_zh` 注明主线 10-20、北端才到 18-25 |
| 3 | `rut_theran_docks` | 无出处 | 原 `quote: "To Rut'theran Village (Teldrassil)"` **在 Auberdine 页上并不存在**（页面那一行实为列表项 `Rut'theran Village (free)`，不是句子）。换成该页真实原句（The Bravery / The Moonspray 两条航线） |
| 4 | `auberdine_docks` | 无出处 + 版本错置（引文） | 原 `quote: "To Stormwind Harbor (originally Menethil Harbor until Wrath of the Lich King)"` 同样不在页上，且**拿 3.0.2 之后的航线去给旧世航线背书**。换成同一句真实原句，并在 `note_zh` 写死「旧世南桥终点是米奈希尔港，3.0.2 才改暴风城」 |
| 5 | `moonglade_druid_teleport` | 无出处 | 原 `quote: "Druid-only (Nighthaven): Rut'theran Village (Teldrassil), Thunder Bluff (Mulgore)"` 不在 Moonglade 页上。换成真实原句（德鲁伊 14 级可学传送）；`note_zh` 补上永夜港内**德鲁伊专用**免费飞行管理员一条 |
| 6 | `moonglade_timbermaw_tunnel_exit` | 无出处 | 原 `quote: "Felwood (Both) - Through Timbermaw Hold or flightpath"` 不在页上（页面原文是 `By foot through the Timbermaw Hold or flightpath from Shrine of Remulos to ...`）。换成 Moonglade 页正文那句「唯一陆路经西南山脉的木喉要塞」 |
| 7 | `kargathia_keep` | 层级挂错 | `parent: ashenvale` → `warsong_lumber_camp`。依据是**该节点自己的 quote**：*"in the eastern part of the Warsong Lumber Camp"*，wiki 灰谷子区域列表也把它缩进在伐木营地下。`note_zh` 同步把「伐木营地东侧」改成「伐木营地的东部」，并说明本树按地理包含挂（与 Aldrassil 挂幽影谷、黑暗深渊挂佐拉姆海岸口径一致） |
| 8 | `the_great_sea` | 版本错置 | `note_zh` 原写「在艾萨拉与冬泉谷东侧以此名出现」。Classic AreaTable 里**没有任何一条无尽之海挂在冬泉谷 618 下**（全部 13 条已逐条列出核对），wiki 现行冬泉谷页那条是 4.0.3 之后的。已订正 |
| 9 | `southfury_river_azshara` | **漏收（新增节点）** | 见第二节 |

另有两处**非节点改动**：`bears_head` 的 `note_zh` 补进 Xylem's Tower 的核验结论（结掉备注 ③-4）；
本文件「取景与拍摄相关」一节的等级带链条同步改成 1-12 / 9-25。

### 五、复核通过、**一个字没动**的部分

1. **国服译名：152 个有 AreaTable 背书的节点，`name_zh` 与 Classic Era 客户端 zhCN 语言包逐字节全等，
   零错、零自拟音译。** 包括几个最容易被「好心改错」的：
   `Gnarlpine Hold = 脊骨堡`、`The Long Wash = 长桥码头`、`Mist's Edge = 薄雾海`、
   `Scalebeard's Cave = 鳞须海龟洞穴`、`Bitter Reaches = 痛苦海岸`、`Raynewood Retreat = 林中树居`。
   作者备注 ③-7 的提醒成立，**下游确实不要「纠正」回常见民间译名**。
   其余 25 个无 AreaTable 背书的节点全是功能性派生节点（飞行点 / 码头 / 传送门 / 银行 / 拍卖行 / 旅店 / 墓地 /
   隧道口），名字是「官方地名 + 功能词」的组合标签，不是游戏内地名——这一点作者已在 ③-6 讲清，口径正确。
   *（说明：`wow.huijiwiki.com` 本轮 WebFetch 与 curl 均被挡回 403 人机校验，未能取到。
   但译名判据用的是**暴雪自家 Classic Era zhCN 语言包**，权威性高于灰机 wiki——灰机的译名本就抄自同一份语言包。）*
2. **飞行点 11 条的 TaxiNodes ID 全部正确**：鲁瑟兰村 27 / 奥伯丁 26 / 阿斯特兰纳 28 / 佐拉姆加 58 /
   碎木岗哨 61 / 血毒岗哨 48 / 刺枝林地 65 / 永望镇 52·53 / 永夜港 62·63 / 塔伦迪斯 64 / 瓦罗莫克 44。
   连**客户端自身的那处不一致**（TaxiNode 48 的中文标签写作「血毒河，费伍德森林」而区域名是「血毒岗哨」）
   都如实记在 `note_zh` 里——核对 CSV 属实，不是作者笔误。
3. **「旧世没有飞行点」的三处否定性断言全部成立**：Classic Era TaxiNodes 全表 87 条里
   **没有** Darnassus、没有 Dolanaar、没有 Forest Song。作者在这三个节点的 `note_zh` 里写的
   「飞行点是 4.0.3 才加的」经查属实。
4. **id 唯一性、父指针完整性**：177 个 id 零重复，全部 `parent` 都能解析到树内节点或 `kalimdor`，
   无孤儿、无环；YAML 用 `yaml.safe_load` 解析通过。
5. **等级带与阵营其余各项**：灰谷 18-30 ✓、费伍德 48-55 ✓、冬泉谷 55-60 ✓、艾萨拉 45-55 ✓
   （均与对应 `(Classic)` 旧世专页信息框一致）；月光林地无等级带 ✓。
   艾萨拉 wiki 信息框写 `faction=Neutral`，本树写 `contested`——**这不是错**，
   本树对「无阵营归属的野外区」统一用 `contested`，与灰谷 / 费伍德 / 冬泉谷口径一致。
6. **层级挂法（除 #7 外）全部合理**：Aldrassil / 黑丝洞 挂幽影谷、班奈希尔兽穴 挂班尼希尔山谷、
   铁木山洞 挂铁木森林、暗影堡 + 欺诈者神祠 挂加德纳尔、黑暗深渊 + 佐拉姆加 挂佐拉姆海岸、
   亚考兰神殿 挂破碎海岸、雷瑟斯圣所 挂废墟海岸、凯斯利尔废墟 挂凯斯利尔湖 ——
   这些 AreaTable 的 `ParentAreaID` 都直接指向 zone，本树按**地理包含**下挂，与 wiki 子区域列表的缩进一致，
   也符合「dungeon 挂在入口所在地」的要求。**木喉要塞拆成费伍德 1769 与艾萨拉 1216 两个节点是对的**，
   实为两处互不连通的同名地点（4.0.3 后艾萨拉那处才改名 Blackmaw Hold）。
7. **迷雾之海 / 无尽之海的合并处理正确**：迷雾之海在 Classic 里是 7 条同名 area（含泰达希尔 2322 /
   灰谷 2325 / 黑海岸 2326，另有菲拉斯 2323 / 凄凉之地 2324 / 希利苏斯 2477 / 根节点 457），
   本片区合成一个片区级节点并在 `note_zh` 写明，口径干净。

### 六、`verified_by` 抽查结论

**146 个引用 `warcraft.wiki.gg` 的节点全部做了「quote 是否真在那一页」的机器比对。**

- **122 条完全逐字命中**；
- **4 条根本不在页上** —— 即改动清单 #3-#6，已换成真实原句（**这是本轮唯一一类真正的 `无出处`**）；
- **余下 9 条属同一种无害写法**：作者省略了原句中间的别名括注或 `<ref>`，例如
  wiki 原文 *"The **Cliffspring Falls** (also known as the **Cliffwater Falls**) are the origin of..."*
  被引成 *"The Cliffspring Falls are the origin of..."*。
  句子主干与事实逐字一致，**不构成编造，`verified_by: ai_read` 维持不降级**。
  受此影响的 9 条：teldrassil、cliffspring_falls、kargathia_keep、zoramgar_outpost、
  blackfathom_deeps、ashenvale_moonwell、winterspring、starfall_village、moonglade。
- 29 个引用 `wago.tools` 的节点，其 `quote` 全部按 `ID|英文名|中文名|ParentAreaID` 格式逐行与下载的 CSV 核对，
  **全部属实**（含 `478|Pools of Arlithrien|阿里斯瑞恩之池|ParentAreaID=141`、
  `1216|Timbermaw Hold|木喉要塞|ParentAreaID=16` 等）。

**没有发现任何一个编造的地名。** 本轮抓到的问题全部是「引文不精确」「等级带用了现行数值」
「同名 area 漏了一侧」这一类，属于收紧而非推翻。

### 七、仍然存疑（交给下游 / 下一轮）

1. **坐标仍是最大的不完整项**：177 个节点里约 45 个有 `coords`。作者说明 wowhead 被出口拦截，
   本轮未尝试补（不在核验范围）。建议下游按作者备注 ③-1 的路子走 `AreaPOI` + `UiMapAssignment`。
2. **Orendil's Retreat** 的旧世归属仍未落定（见第三节 8），维持不收。
3. **灰谷两口月亮井谁北谁南**仍未分清（作者备注 ③-3），本轮无新证据。
4. **黑暗深渊入口精确坐标**仍缺（作者备注 ③-2），本轮无新证据；但「入口在佐拉姆海岸、佐拉姆加以北」
   这一定性描述经 wiki 信息框 `loc = The Zoram Strand, Ashenvale` 复核属实。
5. **等级带的两套数字**：本轮改用了 wiki 旧世专页信息框的 1-12 / 9-25。若下游更认「任务线覆盖区间」
   那一套（1-10 / 10-20），两个数字在 `note_zh` 里都留着了，按需取用，不必再改 YAML。
