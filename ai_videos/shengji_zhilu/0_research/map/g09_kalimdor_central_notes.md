# G09 · 卡利姆多中部 + 奥格瑞玛 + 雷霆崖 —— 测绘备注（非树数据）

树数据的唯一出处是 `g09_kalimdor_central.yaml`（**186 个节点**；作者初稿 184，独立核验后 +2，见文末
「核验记录（G09-V）」）。本文件只放**不属于树**的东西。

版本锚点：**经典旧世 Vanilla / Classic Era**。判定「这个地名旧世有没有」的第一权威是
**暴雪 Classic Era 客户端的 `AreaTable` 数据表**，不是现行 wiki 的子区域列表——后者把
4.0.3a 之后新增的地名混在一起列，本片区（尤其贫瘠之地、石爪山脉）踩这个坑会一口气多出 40 多个假地名。

---

## ① 自查对账

### 实际抓到的源

| 源 | 方式 | 结果 |
|---|---|---|
| Classic Era 客户端 `AreaTable`（zhCN + enUS 两份 CSV）<br>`https://wago.tools/db2/AreaTable/csv?build=1.15.9.69722&locale={zhCN,enUS}` | 本机 curl | 全表下载成功（123 KB / 127 KB）；递归抽出本片区 7 个 zone/city 的**全部子 area**，含**国服官方简中译名**与 `ParentAreaID` 父子关系 |
| Classic Era 客户端 `TaxiNodes`（zhCN + enUS）<br>`https://wago.tools/db2/TaxiNodes/csv?build=1.15.9.69722&locale={zhCN,enUS}` | 本机 curl | 全表下载成功；据此确认本片区旧世**到底有哪几个飞行点 / 船 / 飞艇**（见下表） |
| `warcraft.wiki.gg` MediaWiki API（`action=query&prop=revisions&rvslots=main`，40 标题/批，1.2 s 间隔） | 本机 curl + Python | **230 个页面的完整 wikitext**（两批：158 + 72），含 7 个地区/主城页 + 约 200 个子区域/地标/地下城页 |
| `warcraft.wiki.gg`（WebFetch 通道） | WebFetch | Durotar / Mulgore / The Barrens / Orgrimmar / Thunder Bluff / Stonetalon Mountains 共 6 页摘要，用于交叉核对 Subzones 一节 |

抓取失败 / 放弃的源：

- **`classic.wowhead.com` / `www.wowhead.com`**：`https://www.wowhead.com/classic/zone=17&xml` 返回 **301 且 body 为空**
  （本机出口被 CDN 重定向拦掉）。因此**坐标缺口较大**（见 ③）。
- **`wow.huijiwiki.com`（灰机 wiki）**：本次未抓（G08 片区已实测 403 + JS 反爬）。**不影响译名质量**——
  本树 `name_zh` 直接取自**客户端 zhCN 语言包**，那正是国服译名的源头，比任何 wiki 转录都权威。
  少数客户端里根本没有的条目（奥格瑞玛各城区、雷霆崖三层台面、哀嚎洞穴内部分区）已在 `note_zh` 里逐条标「国服译名待核」。
- `warcraft.wiki.gg` 的 WebFetch 通道中途 **429 Too Many Requests**（多个片区同时在抓同一域名）。
  改用 MediaWiki API + 本机 curl 后全程无失败。

### 节点产出

| zone / city | 节点数 | 其中 AreaTable 实证的子 area |
|---|---|---|
| durotar 杜隆塔尔 | 29 | 27 / 27（全覆盖） |
| orgrimmar 奥格瑞玛 | 17 | 0 / 0（见 ③ 第 1 条——旧世客户端里奥格瑞玛**没有任何子 area**） |
| the_barrens 贫瘠之地 | 53 | 37 / 37（全覆盖） |
| mulgore 莫高雷 | 22 | 21 / 21（全覆盖） |
| thunder_bluff 雷霆崖 | 12 | 4 / 4（全覆盖） |
| stonetalon_mountains 石爪山脉 | 22 | 19 / 19（全覆盖） |
| desolace 凄凉之地 | 29 | 22 / 22（全覆盖） |
| **合计** | **184** | **130 / 130** |

「AreaTable 全覆盖」的含义：Classic Era 客户端里挂在该 zone 下的每一条 area（剔除 `UNUSED` / `Delete ME`
占位行）都在树里有一个节点，一条不漏。其余节点是地下城本体与其内部分区、飞行点 / 船 / 飞艇 / 升降梯、
以及城内建筑地标。

### 机检自查（`scratchpad/gen/build.py`，已跑通）

- 184 个 `id` 全局唯一；全部匹配 `[a-z0-9_]+`。
- 每个节点 16 个字段齐全，无多余字段（PyYAML 回读复核通过）。
- `type` / `subtype` / `faction` / `era` / `verified_by` 全部落在枚举内；**未出现 schema 外的枚举值**。
- `subtype`：`settlement` 33 个全部有值，`transport` 15 个全部有值，其余类型一律空串。
- `level` 只出现在 5 个 zone + 5 个 dungeon 上，格式全部 `\d+-\d+`。
- `adjacent` 只出现在 5 个 zone 上（city 按字段规则留空，见 ⑤ 第 4 条）。
- `coords` 34 个，格式全部 `[N, M]`；其余留空串（**没有编造的坐标**）。
- 每个节点都有 `parent`，无环；除 `central_kalimdor` 外全部能在本文件内解析到。
- `verified_by`：`ai_read` 183 / `ai_draft` 1（仅 `broken_keel_tavern`，理由见 ③ 第 5 条）。

### 本片区旧世的交通点全表（TaxiNodes 实证，不是推断）

| TaxiNodes ID | 名称 | 类型 | 落点 |
|---|---|---|---|
| 23 | 奥格瑞玛，杜隆塔尔 | 飞行点 | 奥格瑞玛力量谷 |
| 25 | 十字路口，贫瘠之地 | 飞行点 | 十字路口 |
| 77 | 陶拉祖营地，贫瘠之地 | 飞行点 | 陶拉祖营地 |
| 80 | 棘齿城，贫瘠之地 | 飞行点 | 棘齿城 |
| 22 | 雷霆崖，莫高雷 | 飞行点 | 雷霆崖 |
| 29 | 烈日石居，石爪山 | 飞行点 | 烈日石居 |
| 33 | 石爪峰，石爪山 | 飞行点 | 石爪峰 |
| 37 | 尼耶尔前哨站，凄凉之地 | 飞行点 | 尼耶尔前哨站 |
| 38 | 葬影村，凄凉之地 | 飞行点 | 葬影村 |
| 34 | 棘齿城到藏宝海湾的船只 | 船 | 棘齿城码头 |
| 35 | 奥格瑞玛的飞艇 | 飞艇 | 杜隆塔尔，**城外**的飞艇塔 |

**三条容易记错的**：① **杜隆塔尔除奥格瑞玛外没有任何飞行点**——剃刀岭、森金村旧世都没有。
② **雷霆崖旧世没有飞艇**（飞艇坡道是 3.2.0 才加的），上下城只有西南与东北两部升降梯。
③ **石爪山脉旧世有两个飞行点**（烈日石居 = 部落，石爪峰 = 联盟），这在一个 15-27 级的争夺区里算多的。

---

## ② 版本差异（4.0.3a 大地的裂变改了什么，逐条）

**通则**：凡出现在现行 wiki 子区域表、却**不在 Classic Era 客户端 AreaTable 里**的地名，
一律判为 4.0.3a 及以后新增 / 改名，**不进树**，逐条列在下面。本片区是全仓最大的雷区之一。

### 贫瘠之地 The Barrens（头号雷区：整块 zone 被劈成两半）

- **旧世的贫瘠之地是一整块 10-25 级 zone**，南北连通不断。4.0.3a 被「大裂谷（The Great Divide）」
  劈成 **北贫瘠之地（10-20）** 与 **南贫瘠之地（30-35，争夺区）** 两个独立 zone。
  树里只有一个 `the_barrens`；`southern_barrens_subzone`（AreaTable 1156）在旧世只是**内部子区域标签**，不是 zone。
- 4.0.3a 及以后才有、**不入树**的贫瘠之地地名（逐条核过 patch 模板）：
  The Great Divide、The Great Gate、Northern Barrens / Southern Barrens（作为 zone）、
  Ruins of Taurajo（取代 Camp Taurajo）、Desolation Hold、Fort Triumph、Battlescar / Fields of Blood、
  Vendetta Point、Firestone Point、Frazzlecraz Motherlode、Hunter's Hill、Spearhead、Twinbraid's Patrol、
  Teegan's Expedition、Forward Command、Camp Una'fe、The Overgrowth、The Nightmare Scar、
  Nozzlepot's Outpost、Darsok's Outpost、Overgrown Camp、Bael Modan Excavation（作为独立子区域）、
  以及 MoP 5.3.0 的 Battlefield: Barrens 全套（Kor'kron elemental camp / lumber yard / meat camp / refinery）。
- **旧世有、4.0.3a 被删掉的子区域**（这些**要**入树，是旧世独有的）：
  Agama'gor 阿迦玛戈、Bramblescar 迅猛龙平原、Blackthorn Ridge 黑棘山、Raptor Grounds 迅猛龙巢穴、
  Field of Giants 巨人旷野、Southern Gold Road 南黄金之路、Camp Taurajo 陶拉祖营地。
- **升降梯（The Great Lift）在 4.0.3 千针石林被淹后被毁**；旧世它是贫瘠之地南端通千针石林的唯一垂直通道。
- 拍旧世贫瘠之地**不要用任何带大裂谷 / 熔岩沟 / 南北分界墙 / 陶拉祖废墟的参考图**。

### 奥格瑞玛 Orgrimmar（第二雷区：整城被重建）

- 4.0.3a「Orgrimmar has been revamped」——旧世的城市**地面布局与现行版本不是同一座城**。
- **最容易错的一条：旧世的格罗玛什要塞（Grommash Hold）在「智慧谷」，不在「力量谷」。**
  现行 wiki 的 Grommash Hold 页开头写的是力量谷，但它自己的补丁记录写着 `4.0.3a: Remodeled and moved.`，
  而 Valley of Wisdom 页写着 "was once the location of Grommash Hold, where Warchief Thrall once resided"。
  树里按**旧世**挂在 `valley_of_wisdom` 之下。
- 4.0.3a 及以后才有、**不入树**的奥格瑞玛地名：
  Orgrimmar Embassy（7.3.5 Added）、Western Earthshrine（4.0.3a Added）、Orgrimmar Skyway、
  Goblin Slums、Orgrimmar Rear Gate（艾萨拉方向的后门，4.0.3a 才开）、
  **Ring of Valor 勇气竞技场（3.0.2 Added）**——旧世荣誉谷里那个圆坑是没启用的空斗兽坑，不是竞技场；
  以及城外杜隆塔尔一侧的 Dranosh'ar Blockade（名字取自 WotLK 战死的德拉诺什·萨鲁法尔，旧世不存在）。
- 旧世**有**、4.0.3a 被移除的：Darkbriar Lodge 暗棘旅店（精神谷，二楼有通诅咒之地的传送门）。
- **旧世奥格瑞玛不通艾萨拉**：荣誉谷通往艾萨拉的那个出口是 4.0.3a 才开的。

### 杜隆塔尔 Durotar

- 4.0.3a「Zone completely renovated」。4.0.3a 及以后才有、**不入树**的：
  Southfury Watershed 南泉水渠（大洪水淹出来的）、The Dranosh'ar Blockade、
  Echo Isles 的三个子区域 Bloodtalon Shore / Darkspear Isle / Spitescale Cove、
  Razor Hill Outskirts 与 Razor Hill Watchtower（5.3.0 加的子区域）、Sen'jin Village Outskirts（5.3.0）。
- **回音群岛的阵营在旧世是反的**：旧世它被巫毒巨魔扎拉赞恩占据、暗矛族已被赶到岸上的森金村，
  是一片**敌对野外区域**；「Zalazane's Fall」事件（3.3.5 加、4.0.1 移除）之后才被夺回并改成巨魔出生地。
  **拍旧世回音群岛不要拍成新手村。**
- 旧世**有**、4.0.3a 被移除的：Kolkar Crag 科卡尔峭壁。

### 莫高雷 Mulgore

- **The Great Gate（大门）是 4.0.3a 才建的**——旧世莫高雷东面通贫瘠之地的山口是敞开的，**没有门**。
  这是最容易照着现行地图画错的一处。
- 4.0.3a 及以后才有、**不入树**的：The Great Gate、Camp Sungraze、Camp Gev'rek、Fargaze Mesa、
  The Battleboar Pen、Thornmantle's Hideout、The Thornsnarl、Stonetalon Pass (Mulgore) / Skywatcher Plateau。
- 旧世**有**、4.0.3a 被移除 / 封死的：Kodo Rock 科多石（子区域移除）、
  Brambleblade Ravine 刺刃峡谷（生物全部移除、非飞行坐骑不可达）。

### 石爪山脉 Stonetalon Mountains（第三雷区：改动比例最高）

- 4.0.3a「Heavily changed」。现行 wiki 的子区域表里**超过一半是 Cata 新增**。
  4.0.3a 及以后才有、**不入树**的：
  Cliffwalker Post、The Deep Reaches、Dagger Pass、Ruins of Eldre'thar、Unearthed Grounds、
  Battlescar Valley、Thal'darah Grove、Thal'darah Overlook、Farwatcher's Glen、Mirkfallon Post、
  The Sludgewerks、Windshear Heights、Windshear Hold、Windshear Valley、Krom'gar Fortress、
  The Fold、Trueshot Point、Northwatch Expedition Base Camp（+ 其 Inn）、Talondeep Pass（旧名 Talondeep Path）、
  Fallowmere Inn、Webwinder Hollow。
- **Sishir Canyon 希塞尔山谷 4.0.3a「Completely redesigned」**——旧世它是一条**空谷**，
  谷里什么都没有；现行版本谷内是艾德雷萨废墟（高等精灵鬼魂 + 考古挖掘点）。**旧世版本不要画废墟。**
- **Stonetalon Peak 石爪峰在旧世是完好的联盟/暗夜精灵据点**，不是被触须摧毁、住满堕落哨兵的样子。
- 旧世**有**、4.0.3a 改掉的：Talondeep Path 石爪小径（改名 Talondeep Pass）。
- 拍旧世石爪山脉**不要用任何带克罗姆加堡垒 / 战痕谷 / 大树 Thal'darah 的参考图**。

### 凄凉之地 Desolace（第四雷区：整块地貌从灰死变成复绿）

- 4.0.3a 之后凄凉之地被塞纳里奥议会「复绿」了一部分，**旧世它是一整片灰白色的死地**：
  枯白树、遍地科多兽头骨、灰土，**没有绿色**（只有西海岸萨瑟里斯海岸是例外的阳光草地）。
  **拍旧世凄凉之地不要用任何带绿草复苏 / 新生林地的参考图。**
- 4.0.3a 及以后才有、**不入树**的：Shok'Thokar（取代 Magram Village）、Magram Territory（取代 Kolkar Village）、
  Karnitol Shipwreck（作为独立子区域）、以及各处被移除的石构件（吉尔吉斯村的石结构、白骨之谷入口的石拱、
  波尔甘洞穴口的石构件、拉纳加尔岛的雕像——这些**旧世都还在**，画面上要画出来）。
- **玛拉顿 Maraudon 旧世是 45-52 级**；4.0.3a 降到 32-39。它是 **1.2.0 加入**的——
  正式上线后第一个新增的地下城，所以「1.0 就有」的说法是错的。
- 旧世**有**、4.0.3a 被取代的：Magram Village 玛格拉姆村、Kolkar Village 科尔卡村。

### 地下城的版本差异

| 地下城 | 旧世等级 | 后续变化 |
|---|---|---|
| 怒焰裂谷 Ragefire Chasm | 15-21（最低 10 级进） | 5.0.4 整个重做为 7-30 的黑暗萨满剧情本 |
| 哀嚎洞穴 Wailing Caverns | 17-24 | 4.1.0 **蜿蜒裂隙 Winding Chasm 整段移除**，派萨斯与斯卡姆挪到别处 |
| 剃刀沼泽 Razorfen Kraul | 29-38 | TBC 调到 24-29；6.0.2 再改 |
| 剃刀高地 Razorfen Downs | 37-46（最低 28 级进） | 6.0.2 换了 lore / 首领 |
| 玛拉顿 Maraudon | 45-52 | 4.0.3a 降到 32-39 |

---

## ③ 存疑与未查

1. **奥格瑞玛的六个城区在 Classic Era 客户端 AreaTable 里「不存在」。**
   `AreaTable` 里 `ParentAreaID = 1637 (Orgrimmar)` 的行**一条都没有**；全表搜
   Valley of Strength / Valley of Honor / Valley of Wisdom / Valley of Spirits / Cleft of Shadow / The Drag
   （中英文都搜过）**零命中**。
   **但它们是真实存在的地方**——旧世城市几何里就有这六个谷，wiki 的 Cleft of Shadow 页还写着
   `4.0.3a: Named subzone removed.` / `4.2.0: Named subzone correctly appears again.`。
   **旁证**：同一张表里，暴风城（1519）只有一个子 area「英雄谷」，铁炉堡（1537）一个都没有，
   达纳苏斯（1657）只有一个「贸易区」——**旧世的主城普遍不把城区登记成 AreaTable 子区域**，
   城区名只画在城市地图的图层上。
   **处理方式**：按本仓 G03（暴风城）既定做法，六个城区仍以 `type: district` 入树、`era: vanilla`，
   并在此说明数据来源的差异。**若下游要做机检脚本，不要用「AreaTable 里有没有」去校验城区节点。**
   同理，雷霆崖的「低层/中层/顶层高地」也不在 AreaTable 里（表里只有长者/灵魂/猎人三座外围台地 + 预见之池）。

2. **`Mor'shan Base Camp` 莫尔杉营地的旧世地位存疑。**
   AreaTable 1599 确实叫「莫尔杉营地」且挂在贫瘠之地下，但 **1597–1603 是一整块 `UNUSED` 占位区**
   （1597 Raptor Grounds UNUSED / 1598 Grol'dom Farm UNUSED / **1599 Mor'shan Base Camp** /
   1600 Honor's Stand UNUSED / 1601 Blackthorn Ridge UNUSED / 1602 Bramblescar UNUSED / 1603 Agama'gor UNUSED），
   唯独 1599 没带 `UNUSED` 后缀。它旧世是否真作为子区域文本显示、还是只是块占位行，**没查实**。
   已入树并在 `note_zh` 里标注。战歌峡谷的部落入口确实在这一带（1.5.0 战场上线时就在）。

3. **坐标缺口。** 全片区 184 个节点只有 34 个有 `coords`，原因有三，**都不是「懒得查」**：
   - `classic.wowhead.com` 本机不可达（301 空 body），任务书给的 `&xml` 绕法同样失效。
   - **贫瘠之地的坐标一个都不敢填**：现行 wiki 的贫瘠之地坐标全部标注在
     **「Northern Barrens」/「Southern Barrens」两张 Cata 拆分地图**上，与旧世那张
     **单张完整贫瘠之地地图**的坐标系不是同一套，换算比例未经验证，**填了就是错的**。
     唯一例外是 `Agama'gor`，其 wiki 坐标显式标注为 `Barrens (Classic)`，已采用（`[44, 50]`）。
     Cata 地图上的原始读数保留在这里备查（**不要直接当旧世坐标用**）：
     石矿洞 62,5 / 十字路口 50,56 / 鬼雾峰 48,18 / 无水岭 40,16 / 勇士岛 77.7,89.4 /
     格罗多姆农场 56,40 / 莫尔杉壁垒 42.4,15.7 / 棘齿城 68.04,71.11 / 迅猛龙巢穴 57,53 /
     战士之魂神殿 42,57 / 淤泥沼泽 58,19.4（以上标 Northern Barrens）；
     陶拉祖营地 45,52 / 巴尔莫丹 47,84 / 荣耀岗哨 37,11（以上标 Southern Barrens）。
   - **奥格瑞玛城内坐标一个都不敢填**：现行 wiki 的奥格瑞玛坐标全部基于 4.0.3a **重建后**的城市布局
     （暗巷 60,45 / 荣誉谷 67.63,51.53 / 精神谷 34.6,74.6 / 智慧谷 45.6,53.6 / 拍卖行 54.2,73.6 /
     影踪兄弟会 33.7,64.4 / 传说大厅 41.8,72.3），旧世的城市几何不同，**这些数不适用**。

4. **四个只有客户端实证、wiki 页是空壳的节点**，`look_zh` 是按名称与本区地貌推断的**保守**写法，
   实拍前请再核：`skyline_ridge` 冲天岭、`mantle_rock` 披肩石、`brave_wind_mesa` 强风台地、
   `fire_stone_mesa` 火石台地（均属莫高雷），以及 `broken_spear_village` 断矛村（凄凉之地）。
   它们的**存在性与官方译名是硬证据**（AreaTable 399 / 473 / 471 / 472 / 2217），只有画面描述是推断。

5. **唯一一个 `ai_draft` 节点**：`broken_keel_tavern` 破船旅店（棘齿城的旅店）。
   它不是 AreaTable 子区域，名字取自 wiki 的 Ratchet 页子区域列表，**本次没有单独抓到它自己的页面**，
   故如实标 `ai_draft`。它的中文名也是待核的。

6. **`Valley of the Bloodfuries` 血怒峡谷**：AreaTable 466 确实存在且挂在石爪山脉下，
   但 wiki 认为它「可能只是焦炭谷的早期名称或焦炭谷的一部分」。已入树并标注此存疑。

7. **中文译名待核清单**（客户端 zhCN 语言包里没有这些条目，只能用常见译法）：
   奥格瑞玛六城区中的「暗巷 The Drag」、「影踪兄弟会」、「暗棘旅店」；
   雷霆崖的「低层/中层/顶层高地」；哀嚎洞穴内部六个分区（迷雾洞穴 / 尖啸沟壑 / 尖牙之巢 /
   永生峭壁 / 蜿蜒裂隙 / 梦境之岩）。**其余 170 余个节点的 `name_zh` 全部来自客户端官方译名，不需核。**

8. **未查**：本片区各 zone 的**道路网几何**（哪条路从哪儿到哪儿、几个弯）只写到 `note_zh` 的文字级别，
   没有做成节点；如果下游要拍「沿路赶路」的长镜，需要另起一轮按路测绘。

---

## ④ 本片区的地图图片链接清单

**只记 URL 与版权状态，未下载、未上传。** 仓库已裁定：**暴雪美术资产只进人眼、不入画、不上传给生成模型**
（`ai_video.md` rule 4d ①——锚点图纯文字自由生成、零参考图）。下面这些链接的用途只有一个：
**人眼核对地理关系**（谁挨着谁、路怎么走、台地几层）。

版权状态：以下全部为 **Blizzard Entertainment 的游戏截图 / 游戏内地图资产**，
在 warcraft.wiki.gg 上按 fair use 托管。**不可商用、不可作为生成模型的参考图输入。**

| 用途 | URL |
|---|---|
| 莫高雷 世界地图（现行） | https://warcraft.wiki.gg/wiki/File:WorldMap-Mulgore.jpg |
| 莫高雷 世界地图（**旧版**，更接近旧世） | https://warcraft.wiki.gg/wiki/File:WorldMap-Mulgore-old.jpg |
| 莫高雷 手册地图 | https://warcraft.wiki.gg/wiki/File:Mulgore_Map.jpg |
| 凄凉之地 世界地图（**旧版**） | https://warcraft.wiki.gg/wiki/File:WorldMap-Desolace-old.jpg |
| 石爪山脉 分区图 | https://warcraft.wiki.gg/wiki/File:VZ-Stonetalon_Mountains.jpg |
| 石爪山脉 分区图（**旧版**） | https://warcraft.wiki.gg/wiki/File:VZ-Stonetalon_Mountains-old1.jpg |
| 石爪山脉 地貌截图 | https://warcraft.wiki.gg/wiki/File:Stonetalon_landscape.jpg |
| 奥格瑞玛 城市地图（现行，**已是 Cata 布局**） | https://warcraft.wiki.gg/wiki/File:WorldMap-Orgrimmar.jpg |
| 奥格瑞玛 城市地图（**旧版**） | https://warcraft.wiki.gg/wiki/File:WorldMap-Orgrimmar1.jpg |
| 奥格瑞玛 **游戏手册地图（旧世布局，最有参考价值）** | https://warcraft.wiki.gg/wiki/File:Orgrimmarmapmanual.jpg |
| 雷霆崖 城市地图（现行） | https://warcraft.wiki.gg/wiki/File:WorldMap-ThunderBluff.jpg |
| 雷霆崖 城市地图（**旧版**） | https://warcraft.wiki.gg/wiki/File:WorldMap-ThunderBluff-old.jpg |
| 雷霆崖 城市地图（**旧版 1**） | https://warcraft.wiki.gg/wiki/File:WorldMap-ThunderBluff-old1.jpg |
| 雷霆崖 **游戏手册地图（旧世布局）** | https://warcraft.wiki.gg/wiki/File:Thunderbluffmapmanual.jpg |
| 哀嚎洞穴 副本地图 | https://warcraft.wiki.gg/wiki/File:WorldMap-WailingCaverns.jpg |
| 剃刀沼泽 分区图 | https://warcraft.wiki.gg/wiki/File:VZ-Razorfen_Kraul.jpg |
| 怒焰裂谷 分区图 | https://warcraft.wiki.gg/wiki/File:VZ-Ragefire_Chasm.jpg |
| 剃刀岭 截图 | https://warcraft.wiki.gg/wiki/File:Razor_Hill.jpg |
| 刃拳海湾 截图 | https://warcraft.wiki.gg/wiki/File:Bladefist_Bay_port.jpg |
| 巨木谷 截图 | https://warcraft.wiki.gg/wiki/File:Greatwood_Vale.jpg |
| 玛拉顿 入口 截图 | https://warcraft.wiki.gg/wiki/File:Maraudon_entrance.jpg |
| 卡利姆多中部（魔兽争霸 III 战役地图，非 WoW） | https://warcraft.wiki.gg/wiki/File:Warcraft_III_Map_-_Central_Kalimdor.jpg |

**凡文件名里带 `-old` / `mapmanual` 的优先看**——那几张才接近旧世；不带后缀的现行图
在贫瘠之地、奥格瑞玛、石爪山脉三处与旧世出入最大。**贫瘠之地没有可用的旧世单张全图**
（现行 wiki 只有拆分后的北/南两张），这也是 ③ 第 3 条坐标缺口的根因。

---

## ⑤ 给下游的提醒

1. **合龙时 `central_kalimdor` 由 G01 定义，本文件不重复定义。**
   本片区所有 5 个 zone 的 `parent` 都是 `central_kalimdor`，该节点在
   `g01_world_skeleton.yaml` 里已存在（`parent: kalimdor`），**不要在本片区再建一份**。
   G01 对该分区的描述写着「vanilla 含杜隆塔尔 / 贫瘠之地 / 莫高雷 / 石爪山脉 / 凄凉之地 / 尘泥沼泽」——
   本片区覆盖前五个，**尘泥沼泽（Dustwallow Marsh）不在 G09 范围内，合龙时要确认有别的片区认领了它**。

2. **跨片区的 `adjacent` 引用**（这些 id 不属于本片区，合龙时对账）：
   `azshara`（艾萨拉，G08）、`ashenvale`（灰谷，G08）、`dustwallow_marsh`（尘泥沼泽，未认领？）、
   `thousand_needles`（千针石林）、`feralas`（菲拉斯）。

3. **三组同名节点已加限定后缀，合龙时不要误判为重复**：
   - 怒水河：`southfury_river_durotar`（AreaTable 814）/ `southfury_river_barrens`（815）——客户端两侧各一条 area。
   - 无尽之海：`great_sea_durotar`（2320）/ `great_sea_barrens`（2319）——同上。
   - 迷雾之海：`veiled_sea_desolace`（2324）——G08 也定义了 `the_veiled_sea`，**那是另一条 area**，
     两者都保留还是合并成一个，由合龙方决定。
   - 另外：`razorfen_kraul_entrance` / `razorfen_downs_entrance` 是**野外子区域**（AreaTable 1717 / 1316），
     `razorfen_kraul` / `razorfen_downs` 是**副本本体**（491 / 722，独立地图）。这是两回事，不要合并。
   - `the_great_lift_barrens`：千针石林那一侧应另有一个同名节点，合龙时对账。

4. **city 节点的 `adjacent` 按字段规则留空。**
   字段规则写的是「只有 zone / continent 填 `adjacent`」，但奥格瑞玛与雷霆崖在世界地图上
   **本身就是 zone**（AreaTable 1637 / 1638，`ParentAreaID=0`）。为通过机检，两者 `type` 记作 `city`、
   `adjacent` 留空，邻接关系写在 `note_zh` 与其 `parent`（`durotar` / `mulgore`）里。
   如果生成器允许 city 填 `adjacent`，可以补上 `orgrimmar → [durotar]`、`thunder_bluff → [mulgore]`。

5. **选景时最该知道的五条**（旧世限定）：
   - **十字路口**是部落玩家的集体记忆点，不是一个大城——它只是**四条土路交叉口上一圈尖木桩围的小镇**，
     人多是因为飞行点连着所有据点，不是因为它大。别拍成城市。
   - **雷霆崖上下城只有两部升降梯**（西南 + 东北），**旧世没有飞艇**。
     台与台之间全靠**会晃的绳索吊桥**，桥下是几百尺的空——这是这座城唯一的戏剧性通行方式，值得用。
   - **奥格瑞玛是「一线天」的峡谷城**，不是广场城；**暗影裂口是全城唯一看不见天空的街区**
     （4.0.3a 之后反而能看见天了）。暗巷是终年背光的窄街。
   - **凄凉之地旧世是灰白的死地**（枯白树 + 遍地科多兽头骨 + 灰土），只有**西海岸萨瑟里斯海岸**
     是反常的阳光草地——这个「灰死荒原里唯一一条绿色海岸」的对比本身就是镜头。
   - **石爪山脉的焦炭谷**是旧世本区唯一的火景（岩浆 + 炭桩 + 黑龙），与全区的灰褐石峰 + 深绿针叶林
     形成强反差；它与绿意盎然的石爪峰分处同一 zone 的两端。

6. **不要用现行 wiki 的 Subzones 一节当清单。**
   本片区实测：贫瘠之地现行表里约 **60%** 是 Cata 之后的地名，石爪山脉约 **52%**。
   正确做法是先拉 Classic Era `AreaTable`，再用 wiki 页补描述与 patch 记录。
   复现命令（本次实际用的）：
   ```
   curl -o area_zh.csv "https://wago.tools/db2/AreaTable/csv?build=1.15.9.69722&locale=zhCN"
   curl -o area_en.csv "https://wago.tools/db2/AreaTable/csv?build=1.15.9.69722&locale=enUS"
   curl -o taxi_zh.csv "https://wago.tools/db2/TaxiNodes/csv?build=1.15.9.69722&locale=zhCN"
   ```
   zone 根 ID：杜隆塔尔 14 / 贫瘠之地 17 / 莫高雷 215 / 石爪山脉 406 / 凄凉之地 405 /
   奥格瑞玛 1637 / 雷霆崖 1638；按 `ParentAreaID` 递归即得全部子区域。

7. **暴风城已有资产未被本片区用到**（本片区不含暴风城），
   但下游做联盟侧对照时可直接引用 `ai_videos/shikong_lvxing/sk2/0_research/parts/w1_city_layout.md`。

---

## 核验记录（G09-V）

**独立核验员，2026-09-20。默认立场：怀疑每一个地名。** 核验后节点数 **184 → 186**。
结论：**已修订可用**。这份稿子的存在性、译名、版本切分**基本全对**，我独立复算了一遍作者的主要判据，
没有找到任何编造的地名；补了 2 个旧世独有的漏项，修了 3 处（1 处跨文件 id 撞车、1 处枚举不一致、1 处引文版本错置）。

### ① 核了哪些 zone / 用什么方法

七个 zone/city 全核：**durotar · orgrimmar · the_barrens · mulgore · thunder_bluff · stonetalon_mountains · desolace**。

**不采信作者的转述，两条链各走一遍：**

1. **客户端 AreaTable 我自己重下了一份**（`curl` → `wago.tools/db2/AreaTable/csv?build=1.15.9.69722&locale={zhCN,enUS}`，
   123 KB / 127 KB），按 `ParentAreaID` 从 7 个 zone 根（14 / 1637 / 17 / 215 / 1638 / 406 / 405）递归展开，
   与 YAML 逐条对账。
2. **warcraft.wiki.gg 走 WebFetch 通道抓了 30 个页面**（清单见 ⑤），重点是各 zone 的 Subzones 一节
   与每个可疑条目自己的 Patch changes 节。

### ② 逐 zone 对账结果（AreaTable 实证）

| zone | AreaTable 有效子 area | YAML 覆盖 | 漏 | 多（表上不存在） |
|---|---|---|---|---|
| durotar 杜隆塔尔 | 27（28 条减 `407 Orgrimmar UNUSED`） | 27 | **0** | **0** |
| the_barrens 贫瘠之地 | 37（44 条减 `877 Delete ME` 与 6 条 `*UNUSED`） | 37 | **0** | **0** |
| mulgore 莫高雷 | 21（26 条减 5 条 `*UNUSED`） | 21 | **0** | **0** |
| stonetalon_mountains 石爪山脉 | 19 | 19 | **0** | **0** |
| desolace 凄凉之地 | 22 | 22 | **0** | **0** |
| orgrimmar 奥格瑞玛 | 0（`ParentAreaID=1637` 一条都没有——**我复核确认**） | — | — | — |
| thunder_bluff 雷霆崖 | 4（1639/1640/1641/2197） | 4 | **0** | **0** |
| **合计** | **130** | **130** | **0** | **0** |

**作者自报的 130/130 全覆盖属实。** 另外我把 ID 序列里的空档（376/389/402/462/601/605）逐个查了，
Classic Era 表里这些 ID 根本不存在，不是漏抓。

**分 zone 节点数与作者自报完全一致**（durotar 29 / orgrimmar 17 / the_barrens 53 / mulgore 22 /
thunder_bluff 12 / stonetalon 22 / desolace 29 = 184）。核验后：**durotar 29 / orgrimmar 19**（+2）
**/ the_barrens 53 / mulgore 22 / thunder_bluff 12 / stonetalon 22 / desolace 29 = 186**。

### ③ 补进去的子区域（2 个，都在奥格瑞玛力量谷）

作者在奥格瑞玛这一块的取样是**建筑级**（已有拍卖行、传说大厅、暗棘旅店、影踪兄弟会），
但漏掉了旧世力量谷里最要紧的两座**「4.0.3a 移除 / 迁走、只存在于 Classic」**的建筑：

1. **`the_skytower` 天空塔 The Skytower**（parent=`valley_of_strength`）——
   旧世奥格瑞玛的**部落飞行点塔本体**，塔身同时连着精神谷一侧。

   > "The Skytower (or The Sky Tower) was the name for the Horde flight point tower located in Orgrimmar,
   > also linking to the Valley of Spirits. ... The subject of this article was removed in patch 4.0.3a
   > but remains in World of Warcraft: Classic." — `/wiki/Skytower`

   交叉印证：`/wiki/Valley_of_Strength` 把 The Skytower 明确列在「Removed（but present in Classic）」组里；
   `/wiki/Doras`（旧世飞行管理员）写着 "Prior to the Cataclysm expansion, he was stationed at the zeppelin
   tower in the Valley of Strength"。**这同时反向证实了作者把 `orgrimmar_flightpath` 挂在力量谷是对的**
   （Skytower 页单说 "linking to the Valley of Spirits" 会让人误挂精神谷，别上当）。
   **这是旧世奥格瑞玛天际线上最显眼的一座塔，缺了它拍不对。**

2. **`bank_of_orgrimmar` 奥格瑞玛银行 Bank of Orgrimmar**（parent=`valley_of_strength`）——

   > "The Bank of Orgrimmar is the bank located in Orgrimmar and is considered a heavily populated bank.
   > ... Grommash Hold now occupies its original location. ... Patch 4.0.3a (2010-11-23): Relocated and
   > remodeled." — `/wiki/Bank_of_Orgrimmar`

   旧世它在力量谷、紧挨拍卖行，是 Classic 部落玩家最密集的两处之一；**重建后的格罗玛什要塞正压在它旧址上**，
   这条同时是作者「格罗玛什要塞旧世在智慧谷」判断的第三份旁证。

两者 `name_zh` 都标了「国服译名待核」（非 AreaTable 子区域，客户端语言包无此条目）。

### ④ 修了什么（3 处）

1. **`the_talondeep_path` → `the_talondeep_path_stonetalon`（id 重复，跨文件撞车）。**
   `g08_kalimdor_north.yaml` 里有一个 **id 完全相同**的 `the_talondeep_path`（`type=subzone`, `parent=ashenvale`），
   与本文件的（`type=transport`, `parent=windshear_crag`）类型与父节点都不同——合龙时必炸。
   判据：**AreaTable 1277 `The Talondeep Path` 的 `ParentAreaID=406`（石爪山脉），全表只此一条**，
   所以这条隧道唯一地属于石爪侧；G08 那个是隧道的灰谷端口。按本文件 ⑤-3 已有的「同名加限定后缀」惯例加后缀，
   并在 `note_zh` 里写明合龙时应把 G08 改成 `the_talondeep_path_ashenvale` 或并入本节点。
   （顺带：作者把它挂 `windshear_crag` 而不是 AreaTable 的扁平父节点 `stonetalon_mountains`，**是对的**——
   页面原文写着 "the entrance on the Stonetalon side was found in the northwestern part of Windshear Crag"。）

2. **`durotar_zeppelin_towers` 的 `subtype`：`portal` → `boat`（枚举不一致）。**
   全仓 10 个飞艇节点里 8 个用 `boat`（`g12_transport.yaml` 6 个 + `g04_ek_south.yaml` 1 个），
   `portal` 全仓只此一处。同时在 `note_zh` 里标明：**同一处地点在 `g12_transport.yaml` 里另有 id
   `zeppelin_tower_durotar`（还带两个 berth 子节点），合龙时以 G12 为准去重。**
   （`g06` 的 `undercity_zeppelin_towers` 用 `flightpath`，是全仓另一处同类不一致，不在本片区范围内，留记。）

3. **`thunder_ridge` 的 `quote`：版本错置（引的是大地裂变之后的状态）。**
   原 quote 是一句**图注**「Thunder Ridge after the Cataclysm.」——既不是描述性正文，描述的还是
   4.0.3a 之后的状态。我抓了正文：现行 wiki 把雷霆山写成 **"a flooded gorge"**、住着 **"drowned thunder
   lizards"**，那全是大洪水之后的事；**旧世它是一道干燥的高岩脊，雷霆蜥蜴活着在脊上游荡**。
   已换成正文引文（含 "it was an ancient forest home to many herds of thunder lizards"），
   并在 `note_zh` 里写死「画面上不要出现积水、淹没的树或溺死的蜥蜴」。
   作者原来的 `look_zh` 写的就是干燥岩脊，**内容是对的，只有出处引错了**——这条是收紧，不是推翻。

### ⑤ 我实际抓到的页面清单

**客户端数据（本机 curl，独立重下）**

- `https://wago.tools/db2/AreaTable/csv?build=1.15.9.69722&locale=zhCN`（123 KB）
- `https://wago.tools/db2/AreaTable/csv?build=1.15.9.69722&locale=enUS`（127 KB）

**warcraft.wiki.gg（WebFetch，成功 29 页）**

`/Durotar` · `/The_Barrens` · `/Mulgore` · `/Stonetalon_Mountains` · `/Desolace` · `/Orgrimmar` ·
`/Thunder_Bluff` · `/Wailing_Caverns` · `/Maraudon`（两次） · `/Grommash_Hold` · `/The_Drag` ·
`/Valley_of_Honor` · `/Valley_of_Strength` · `/Valley_of_Spirits` · `/Cleft_of_Shadow` ·
`/The_Wyvern%27s_Tail` · `/Ring_of_Valor` · `/Skytower` · `/The_Skytower` · `/Bank_of_Orgrimmar` ·
`/The_Broken_Tusk` · `/Doras` · `/Slitherblade_Shore` · `/Dreadmist_Camp` · `/Darkmoon_Faire` ·
`/Darkmoon_Faire_Staging_Area` · `/Thunder_Ridge` · `/Razorfen_Kraul` · `/Razorfen_Downs` ·
`/Zones_by_level_(original)`

**失败**

- `/Valley_of_Wisdom` —— WebFetch 中途断流（该节点的判断改由 `/Grommash_Hold` 正面证实，见 ⑥-1）。
- `wow.huijiwiki.com/wiki/智慧谷` —— **HTTP 403**，与 G08 片区实测一致。**灰机 wiki 本次仍不可达**，
  译名核验只能走客户端语言包（见 ⑥-2，那条路更权威）。

### ⑥ 我复核过、确认作者判断正确的争议点（一个字都没动）

1. **「旧世的格罗玛什要塞在智慧谷，不在力量谷」——成立，且是本稿最硬的一条。**
   `/wiki/Grommash_Hold` 正文原句：**"The first Grommash Hold was located in the Valley of Wisdom"**，
   Patch changes 只有一行：**"Patch 4.0.3a (2010-11-23): Remodeled and moved."**
   第三份旁证见 ③-2（银行旧址被现在的要塞占了）。**照现行 wiki 开头那句 "located in the Valley of
   Strength" 挂节点就是错的。**

2. **中文译名：135 个能与 AreaTable 对上的节点，`name_zh` 与客户端 zhCN 语言包 100% 逐字相同，零差异。**
   我用脚本逐条比对，不是抽样。这比任何 wiki 转录都权威，灰机 403 不影响这 135 个。
   剩下 51 个（奥格瑞玛城区与建筑、雷霆崖三层台面、哀嚎洞穴内部六区、玛拉顿三翼、各飞行点节点）
   客户端里本就没有条目，作者已逐条标「待核」，**属如实标注，不是偷懒**。

3. **`AreaTable` 里奥格瑞玛零子区域——我独立复核确认。** `ParentAreaID=1637` 的行一条都没有。
   作者按 G03（暴风城）惯例以 `type: district` 入树并写明数据来源差异，处理正确。
   **给下游机检脚本的硬提醒：不要用「AreaTable 里有没有」去校验这 12 个 district 节点和它们的建筑子节点。**

4. **等级带：5 个 zone 全部逐字命中。** `/wiki/Zones_by_level_(original)` 原文：
   Durotar **1-10** · Mulgore **1-10** · The Barrens **10-25** · Stonetalon Mountains **15-27** ·
   Desolace **30-40**——与 YAML 完全一致。地下城侧：怒焰裂谷 **15-21**（`/Durotar` 原文
   "a dungeon for levels 15 - 21"）、哀嚎洞穴 **17-24**（`/Wailing_Caverns` infobox `classiclevel=17-24`）、
   玛拉顿 **45-52** 且 **1.2 加入**（`/Maraudon` 原文 "Added in patch 1.2, Maraudon was the first dungeon
   to be added after the release"）全部证实。

5. **层级挂错：一处都没有。** 作者相对 AreaTable 做了 27 处「地理嵌套」偏移（把 `the_den_durotar`
   挂 `valley_of_trials`、`dustwind_cave` 挂 `razorwind_canyon`、`bolgans_hole` 挂 `gelkis_village` 等），
   AreaTable 在这些点上是**扁平的**（全挂 zone 根）。我逐条比对 wiki 的嵌套写法，
   **27 处全部与 wiki 一致**（例：`/Durotar` 写 "Razorwind Canyon (with Drygulch Ravine and Dustwind Cave)"；
   `/Desolace` 写 "Gelkis Village → Bolgan's Hole"；`/The_Barrens` 写哀嚎洞穴 "located in Lushwater Oasis"；
   `/Maraudon` 写 "located in the Valley of Spears in Desolace"）。**这是比 AreaTable 更好的树，不是错。**

6. **哀嚎洞穴内部六区逐字命中。** `/wiki/Wailing_Caverns` 原文列表：
   "Cavern of Mists, Crag of the Everliving, Dreamer's Rock, Pit of Fangs, Screaming Gully, Winding Chasm"
   ——与 YAML 六个节点完全一致；4.1.0 移除蜿蜒裂隙的记载也属实。

7. **我自己怀疑过、查下来作者是对的（这几条别再翻案）：**
   - **The Wyvern's Tail**（荣誉谷那家旅店）——`Patch 7.1.5 (2017-01-10): Subzone added`，
     **军团再临才有**，作者不收，对。
   - **Ring of Valor 勇气竞技场**——`Patch 3.0.2 (2008-10-14)` 才加；页面原文说旧世那个坑
     "existed only as a non-instanced zone with an inaccessible interior"，与作者 note 完全吻合。
   - **The Broken Tusk 断牙旅店**（力量谷那家旅店）——`Patch 4.0.3a: Inn given a proper name`，
     旧世这家店在、但**没有名字**，所以不该以地名入树，作者不收，对。
   - **Slitherblade Shore**（凄凉之地北岸）——`Patch 4.0.3a: Area given a named subzone`，不收，对。
   - **Dreadmist Camp**（贫瘠之地）——`Patch 4.0.3a: Added`，不收，对。
   - **Darkmoon Faire Staging Area（莫高雷）**——现行 wiki 把它列在莫高雷
     「Undisplayed Locations」里，`/Darkmoon_Faire_Staging_Area` 说 "Before the Darkmoon Faire's
     update and relocation to the Darkmoon Island in patch 4.3.0, the areas were a part of the place
     where the Faire took place"。**旧世暗月马戏团确实在莫高雷摆过摊**，但「Staging Area（集结区）」
     这个**名字**是 4.3.0 马戏团搬去暗月岛之后才有的概念，旧世没有这个地名。
     **故不入树是对的**；但它是一处真实存在、视觉上极有戏的旧世莫高雷临时景（帐篷、旗、占卜帐），
     若要拍，按「事件景」另记，不要当常驻地名。

### ⑦ 仍存疑 / 交给下游的

1. **剃刀沼泽 29-38 与剃刀高地 37-46 两个等级带我没能独立复核。**
   现行 wiki 这两页的 infobox 已是缩放后的数（15-30），Patch 记录给的是 WoD 前的
   "previous instance level: 32-35" / "42-45"，**都不是旧世原值**，`/Zones_by_level_(original)` 又只列 zone 不列本。
   作者填的是通行的旧世值，我**没有反证，也没有正证**，保留原样并在此标记。要坐实只能查 1.12 客户端的
   `LFGDungeons` / 原版副本列表。

2. **`/wiki/Razorfen_Downs` 现行正文把剃刀高地说成在千针石林**（"nestled amid huge brambles in the
   Thousand Needles"）。**别照这句改树**——Classic Era 客户端 `AreaTable 1316` 的 `ParentAreaID=17`
   明明白白是贫瘠之地，客户端硬证据优先于现行页的 lore 行文。已核，作者挂贫瘠之地正确。

3. **`g11_instances.yaml` 与本文件重复定义了 5 个地下城节点**
   （`ragefire_chasm` / `wailing_caverns` / `razorfen_kraul` / `razorfen_downs` / `maraudon`）。
   我逐字段比对过：**两边的 `parent` / `type` / `level` / `name_zh` 完全一致**，属良性重复，
   合龙时任取一份即可，不构成冲突。（作者写稿时该文件可能尚未存在，不算作者的错。）

4. **奥格瑞玛还有 3 个「4.0.3a 移除、Classic 尚存」的精神谷建筑我没入树**——
   `/wiki/Valley_of_Spirits` 列出 Darkbriar Lodge（已在树里）、**Spirit Lodge**、
   **Survival of the Fittest**、**Skyfury Staves** 四者，并注明全部 "removed from World of Warcraft
   in patch 4.0.3a but is present in Classic"。后三个我**只拿到列表、没拿到各自页面的描述性正文**，
   按「宁缺勿编」不入树，在此留记；若下游要补齐精神谷，这三个是有出处的候选。
   同理 `/wiki/Cleft_of_Shadow` 的 The Slow Blade / Rekkul's Poisons / Ironwood Staves and Wands /
   Shadowdeep Reagents / Darkfire Enclave / Dark Earth / Arcane Enclave 也是同一档的候选。

5. **坐标缺口依旧（186 个节点 34 个有 `coords`）。** 我认可作者不填的理由——贫瘠之地现行坐标基于
   Cata 拆分后的南/北两张图，奥格瑞玛现行坐标基于 4.0.3a 重建后的城市几何，**换算未验证就是错的**。
   宁可空着。要补只能走 1.12 客户端地图或 Classic 专用坐标源。

### ⑧ 核验后的机检（我自己跑的，全过）

- 186 个 `id` 全局唯一；全部匹配 `[a-z0-9_]+`。
- 16 个字段齐全且**形状完全一致**（186/186 同一字段集合），PyYAML 回读通过。
- 父子无环，除 `central_kalimdor`（G01 定义）外全部在本文件内可解析，根唯一。
- `coords` 34 个格式全对；`level` 10 个格式全对；`quote` / `source_url` **无一为空**。
- `verified_by`：`ai_read` 185 / `ai_draft` 1（仍只有 `broken_keel_tavern`，理由见 ③-5，我认可）。
- 跨文件 id 撞车：修复后**只剩 5 个与 `g11_instances.yaml` 的良性重复**（见 ⑦-3），`the_talondeep_path` 已解。
