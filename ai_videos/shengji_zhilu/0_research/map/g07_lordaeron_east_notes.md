# G07 · 洛丹伦东部与瘟疫之地 —— 测绘备注

本文件只放**不属于树**的东西。凡属于树的信息（节点、层级、坐标、等级、阵营、译名）一律只写在
`g07_lordaeron_east.yaml` 里，这里不重复一遍（仓库规则「一份东西只有一个出处，副本必漂」）。

- 片区：`G07`
- 覆盖 zone：阿拉希高地 / 辛特兰 / 西瘟疫之地 / 东瘟疫之地
- 版本锚点：**经典旧世 Vanilla / Classic Era（1.12 内容）**
- 节点总数：**122**（阿拉希高地 38 · 辛特兰 24 · 西瘟疫之地 21 · 东瘟疫之地 39，含各自的 zone 节点本身）

---

## ① 自查对账

### 1.1 本轮取源的关键决定：改用客户端原始数据当主源

第一轮按任务书去抓 `warcraft.wiki.gg` 的 zone 页，抓到了，但**立刻发现这条路不安全**：
该 wiki 的 zone 页描述的是**当前版本（大地的裂变之后）**的状态，Subzones 一节把
4.0.3 新增的地名和旧世地名**混在同一张表里、不作任何标记**。例如阿拉希高地那张表里，
`Ar'gorok`、`Galen's Fall`、`Highlands Mill`、`Newstead`、`Valorcall Pass` 与
`Hammerfall`、`Stromgarde Keep` 并排列出，肉眼分不出哪个是旧世的。
继续拉 `action=raw` 拿原始 wikitext 也没用——列表里没有 `{{cata-inline}}` 之类的版本标记
（只有 `{{replaced|旧名}}` 这一种改名标记偶尔出现）。**照抄这张表 = 直接把 4.0.3 的地名写进旧世树。**

于是改用**暴雪客户端自己的数据表**当主源：Classic Era 客户端（`wow_classic_era` 1.15.9.69722）
的 `AreaTable` 里**只有旧世的区域**，Cata 新增的区域根本不在表内。
这既解决了版本纯度，又顺带解决了国服官方译名（同一张表有 `zhCN` 本地化列）。

用到的表（全部经 `wago.tools` 导出、逐行本地比对，enUS 与 zhCN 两份对照）：

| 表 | 用途 | 行数/结果 |
|---|---|---|
| `AreaTable` | 区域层级（`ParentAreaID`）+ 官方中英文名 + `ExplorationLevel` | 四个 zone 共 95 条子区域记录 |
| `TaxiNodes` | 飞行点（含 `Flags` 判阵营、`CharacterBitNumber` 判是否真是玩家飞行点） | 本片区 6 个有效飞行点 |
| `AreaPOI` | 世界地图上的图标点（城镇 / 地标 / 哨塔） | 本片区取用 16 个 |
| `AreaTrigger` | 副本与战场入口触发器（含等级门槛原文） | 本片区取用 6 处入口 |
| `UiMap` + `UiMapAssignment` | 各 zone 的世界坐标包围盒，用来把世界坐标换算成地图百分比坐标 | 4 个 zone 的 bounds |

复现命令（任一台机器上可重跑，纯 HTTP GET、无需登录）：

```bash
for t in AreaTable TaxiNodes AreaPOI AreaTrigger UiMap UiMapAssignment; do
  for loc in enUS zhCN; do
    curl -sSL "https://wago.tools/db2/$t/csv?build=1.15.9.69722&locale=$loc" -o ${t}_$loc.csv
  done
done
```

坐标换算公式（`Region_*` 来自 `UiMapAssignment`，`OrderIndex=0` 那一行）：

```
mapX% = (Region_4 - worldY) / (Region_4 - Region_1) * 100
mapY% = (Region_3 - worldX) / (Region_3 - Region_0) * 100
```

**换算精度自检**：纳克萨玛斯入口算出 `[40, 26]`，与 wiki 独立记载的 `[39, 26]` 吻合；
避难谷地算出 `[46, 46]`、寒风营地 `[43, 85]`、圣光之愿礼拜堂 `[82, 59]`，
均与社区通行坐标相差 ≤2。故本片区坐标**误差按 ±2 计**，不要当作精确到小数位的数字用。

### 1.2 抓取结果逐条

**抓到并读了原文（`ai_read`）**

| 来源 | 结果 |
|---|---|
| `warcraft.wiki.gg/wiki/Arathi_Highlands` | ✅ 取开篇句 + 版本差异线索 |
| `warcraft.wiki.gg/wiki/Hinterlands` | ✅ 取开篇句（`The_Hinterlands` 是重定向页，正确标题为 `Hinterlands`） |
| `warcraft.wiki.gg/wiki/Western_Plaguelands` | ✅ 取开篇句 |
| `warcraft.wiki.gg/wiki/Eastern_Plaguelands` | ✅ 取开篇句 |
| 上述四页的 `?action=raw` 原始 wikitext | ✅ 用来确认「Maps and subregions」原始列表 + `{{replaced\|旧名}}` 改名标记 |
| `warcraft.wiki.gg/wiki/Stromgarde_Keep` | ✅ 取旧世三方占据状态 + 外观原句 |
| `warcraft.wiki.gg/wiki/Jintha%27Alor` | ✅ 取坐标 `[63.3, 70.3]` + 层级结构 + 山顶祭坛 |
| `warcraft.wiki.gg/wiki/Stratholme` | ✅ 取外观原句（**坐标不可用，见 ③**） |
| `warcraft.wiki.gg/wiki/Naxxramas_(Classic)` | ✅ 取 1.11 开放 + 坐标 + 传送尖塔机制 |
| `warcraft.wiki.gg/wiki/Arathi_Basin` | ✅ 取 1.7.0 开放 + 五资源点 + 开篇句 |
| `warcraft.wiki.gg/wiki/Scholomance` | ✅ 取入口所在地 + 外观原句 |
| `warcraft.wiki.gg/wiki/Revantusk_Village` | ✅ 取部族归属 + 加入补丁（置信中等，见 ③） |
| `warcraft.wiki.gg/wiki/Alterac_Mountains` | ✅ 用来判西瘟疫之地南向陆路 |
| `warcraft.wiki.gg/wiki/Hillsbrad_Foothills` | ✅ 用来判辛特兰 / 西瘟疫之地的旧世陆路入口 |
| `db.nfuwow.com/60/?zone=45/47/28/139` | ✅ 旧世 1.12 中文库，四个 zone 的中文名 + 等级带 + 「争夺中」逐个核对 |
| `wago.tools` 六张表 × 两个语言 | ✅ 全部 200，本地逐行解析 |

**抓不到的（`fetch_failures`）**

| 来源 | 结果 | 处置 |
|---|---|---|
| `wow.huijiwiki.com`（灰机 wiki，`/wiki/…` 与 `index.php?action=raw` 两种写法） | ❌ **HTTP 403**，全部被拒 | 任务书指定它查中文译名，走不通。**改用客户端 `AreaTable` 的 `zhCN` 本地化列**——这比灰机 wiki 更权威（它本身就是国服客户端里显示的那串字），本片区 122 个节点的 `name_zh` 全部由此而来，**无一条靠记忆音译** |
| `wiki.biligame.com/wow/阿拉希高地` | ❌ HTTP 404（该站无此条目） | 未使用 |
| `cn.wowhead.com/classic/zone=45` | ⚠️ 301 跳 `www.wowhead.com/classic/cn/zone=45`，未续抓 | 未使用（`db.nfuwow.com` 已覆盖同样需求） |
| `www.wowhead.com/cn/classic/zone=45&xml` | ❌ HTTP 404（locale 前缀写法不对） | 未使用 |
| `wago.tools/db2/WorldSafeLocs/...` | ❌ `{"errors":"Table not found."}` | 墓地（graveyard）点位拿不到，见 ③ |

---

## ② 版本差异：4.0.3（大地的裂变）改了什么，以及本树的处置

本片区是**头号雷区的隔壁**——任务书点名的艾尔文森林一带被 4.0.3 重做，本片区四个 zone
虽然没被整体重做，但**每一个都有地名增删或改名**。以下逐条列出，**凡标「不进树」的都已确认没有写进 YAML**。

### 2.1 阿拉希高地

wiki 明说「the Highlands were spared during the Cataclysm」（地形本身没重做），但地名照样动了：

**4.0.3 新增 —— 不进树**：
`Ar'gorok`（部落要塞）与其下 `Goblin Workshop`、`Galen's Fall`（被遗忘者据点，还带一个新飞行点）、
`Highlands Mill`、`Newstead`、`Northfold Crossing`、`Hatchet Ridge`、`High Perch`、
`Valorcall Pass`（矮人北向凿穿到辛特兰的隧道）、`Circle of Elements`、`Drywhisker Mine`
（旧世只有 `Drywhisker Gorge` 枯须峡谷这一个区域名）、`Galson's Lode`、
`Fishing Shack`（法迪尔海湾内）、`Stromgarde Keep` 下的 `Crypt` 与 `Barracks`、
`Baradin Bay`、`The Great Sea`。

**4.0.3 移除 —— 旧世有，本树收了**：
`Blackwater Shipwrecks` 黑水湾沉船、`O'Breen's Camp` 奥布瑞恩营地、`Witherbark Caverns` 枯木洞穴。
这三条在当前 wiki 上被归到「Removed locations」，**正是只有旧世树才该有的节点**。

**通行性变化（对剧本的路线设计有直接影响）**：
4.0.3 之前，阿拉希高地**北面没有通往辛特兰的陆路**；`Valorcall Pass` 那条矮人隧道是 Cata 才凿的。
旧世从阿拉希去辛特兰只能绕回希尔斯布莱德丘陵再往东上山。**本树的 `adjacent` 按旧世写，
只列希尔斯布莱德丘陵与湿地。**

**新增飞行点 —— 不进树**：落锤镇在 Cata 之后多出通往黑锋要塞港口、赤红庇护所（暮光高地）等航线，
旧世落锤镇只是个普通部落飞行点。

### 2.2 辛特兰

**4.0.3 新增/改名 —— 不进树**：
`Stormfeather Outpost`（新增的联盟哨站兼飞行点）；
`Hiri'watha Research Station` 是**把旧世的 `Hiri'watha`（西利瓦萨）原址改建并改名**——
本树收的是旧名 `Hiri'watha`，wiki 原始 wikitext 里写作
`[[Hiri'watha Research Station]]/{{replaced|Hiri'watha}}`，`{{replaced}}` 里那个就是旧世名。

**势力归属变化 —— 剧本要按旧世写**：
辛萨罗（Jintha'Alor）在**旧世属恶枝（Vilebranch）巨魔部族**；恶齿（Revantusk）部族夺下辛萨罗
是 4.0.3 的剧情（任务「It's Ours Now」）。当前 wiki 页直接写「The Revantusk tribe currently holds
Jintha'Alor」——**照抄会把旧世写错**。本树的 `note_zh` 已写死旧世归属。
同理，枯木（Witherbark）部族在 Cata 被赶出辛特兰，旧世它们还在。

### 2.3 西瘟疫之地

**4.0.3 改名 —— 本树用旧名**：
- `Ruins of Andorhal` 安多哈尔废墟 → Cata 重建后改名 `Andorhal`
- `Dalson's Tears` 达尔松之泪 → Cata 改名 `Dalson's Farm`
- `Chillwind Camp` 寒风营地 → Cata 改名 `Chillwind Point`（中文「冰风岗」）

**4.0.3 新增 —— 不进树**：
`The Menders' Stead`、`Malicia's Outpost`、`Charred Outpost`、`Redpine Dell`、`Taelan's Tower`、
`Path of Uther`、`Sorrow Hill Crypt`，以及 wiki 列在西瘟疫之地名下的 `Plaguemist Ravine`
（旧世这个区域只属于辛特兰，本树按旧世把它挂在辛特兰下）。

**剧情状态变化 —— 旧世不成立**：
Cata 之后塞纳里奥议会净化了大半土地、银色北伐军接管壁炉谷、被遗忘者在安多哈尔之战后拿下安多哈尔。
**旧世：全区仍是病态焦土，壁炉谷属血色十字军（泰兰·弗丁在），安多哈尔是天灾据点。**
镜头上这条差别最大——Cata 版的西瘟疫之地有大片重新变绿的草地，旧世**没有**。

**飞行点变化**：旧世西瘟疫之地**只有寒风营地一个飞行点、且只对联盟开放**；
wiki 上列的安多哈尔（联盟侧/部落侧）、壁炉谷、Menders' Stead 等航线全是 Cata 的。

### 2.4 东瘟疫之地

**4.0.3 改名 —— 本树用旧名**：`Scarlet Base Camp` 血色十字军营地 → Cata 改名
`Death Cultist Base Camp`（wikitext 里写作 `[[Death Cultist Base Camp]]/{{replaced|Scarlet Base Camp}}`）。

**后续版本新增 —— 不进树**：
- **巫妖王之怒**：`Ruins of the Scarlet Enclave`、`Acherus: The Ebon Hold`、`Death's Breach`、
  `New Avalon`、`Crypt of Remembrance`——这一整块是死亡骑士起始区，旧世**完全不存在**。
  （注：`New Avalon` 在 Classic Era 客户端的 `AreaTable` 里也有一条记录，ID 16335，
  属于后续版本混入的高位 ID，已人工剔除；**不能因为它出现在 Classic Era 数据里就当它是旧世的**。）
- **军团再临**：`Sanctum of Light`（圣光之愿礼拜堂地下的圣骑士职业大厅）。
- **大地的裂变**：`Death's Step`、`Ix'lar's Domain`、`Siege Vise`、`Darrowshire Hunting Grounds`、
  `Tyr's Hand Abbey` 及其 `Hall of Arms` / `Main Hall` / `Library Wing`。
- **燃烧的远征**：`Thalassian Pass` 北面通往幽暗森林的关口——**旧世是封死的**，
  东瘟疫之地在旧世的陆路出口**只有西面索多里尔河桥一个**。

**四座哨塔的性质变化（重要）**：
`Crown Guard Tower` / `Eastwall Tower` / `Northpass Tower` / `Plaguewood Tower`
在**旧世是被占据的据点**（世界地图上有图标），**不是飞行点**；4.0.3 才由银色北伐军接管并开出航线。
本轮是从数据层坐实的——这四个名字在 `TaxiNodes` 里确实有记录（ID 84–87），
但它们的 `CharacterBitNumber = 0`，即**没有分配探索位、玩家不可能发现并使用**；
对比同表的避难谷地（ID 16）、落锤镇（17）、鹰巢山（43）、寒风营地（66）、
圣光之愿礼拜堂（67/68）、恶齿村（76）都有正常的探索位。
**结论：旧世东瘟疫之地只有圣光之愿礼拜堂一个飞行点（两阵营各一名飞行管理员）。**

**纳克萨玛斯**：旧世 **1.11（2006-06-19）才开放**，悬在病木林上空，入口是林中的传送尖塔。
巫妖王之怒把它整体搬去了龙骨荒野——**旧世剧本里，纳克萨玛斯必须在天上**。
反过来，**如果剧情时间线设定在 1.11 之前，病木林上空就不该出现它**（见 ⑤）。

### 2.5 一条通用提醒

本片区四个 zone 的 `adjacent` 与「怎么走过去」全部按**旧世**写。当前 wiki 的信息框里，
希尔斯布莱德丘陵一栏会列出 5 个相邻区、辛特兰一栏会列出 4 个——那是 Cata 之后的连通性。
**旧世本片区相关的陆路连通只有以下六条**（已写进各 zone 的 `note_zh`）：
希尔斯布莱德丘陵↔阿拉希高地（穿索拉丁之墙豁口）、阿拉希高地↔湿地（过萨多尔大桥）、
希尔斯布莱德丘陵↔辛特兰（东侧上山，辛特兰旧世唯一陆路口）、
提瑞斯法林地↔西瘟疫之地（过亡灵壁垒）、西瘟疫之地↔东瘟疫之地（过索多里尔河桥）、
奥特兰克山脉↔西瘟疫之地（寒风营地那道南部山口）。

---

## ③ 存疑与未查

| # | 事项 | 现状 | 建议 |
|---|---|---|---|
| 1 | **任务书里的「辛特兰的祖阿曼」是错的** | 祖阿曼（Zul'Aman）在**幽暗城林地（Ghostlands）**，是**燃烧的远征**的团队副本，**不在辛特兰、也不属旧世**。辛特兰的森林巨魔大城是**辛萨罗 Jintha'Alor**（已收进树，含山顶祖尔祭坛） | 下游排镜时别去找祖阿曼；「辛特兰巨魔山城」= 辛萨罗 |
| 2 | 斯坦索姆两个入口**哪个通血色侧、哪个通亡灵侧** | 已从 `AreaTrigger` 坐实**位置**（偏西 `[30, 16]`、偏东 `[48, 22]`）与**等级门槛**（均 45 级），但**没有核到「正门→血色侧 / 侧门→亡灵侧」的原始出处** | 树里只写了位置与门槛、**没有断言哪扇门通哪一侧**。要拍男爵/血色相关剧情前，请进游戏或查专门的副本攻略页确认 |
| 3 | wiki 给的斯坦索姆坐标不可信 | `warcraft.wiki.gg/wiki/Stratholme` 抓回来说两个入口都在 `[27, 12]`（两个门同一坐标，显然不对） | 树里用的是 `AreaTrigger` 换算值，不是 wiki 值 |
| 4 | 通灵学院 / 斯坦索姆的**队伍规模沿革** | 树的 `note_zh` 写了「开服时为 10 人规模，1.10 改为 5 人」——这条**本轮没有单独核原始补丁说明**，属于常识性记忆 | 若剧本要演「十人本」情节，先核 1.10 补丁说明 |
| 5 | 恶齿村（Revantusk Village）的加入补丁 | wiki 页读回「Patch 1.5.0 (2005-06-07)」，但该页同时含大量 Cata 内容，取数置信中等 | 树里只写「旧世中期补丁加入」，没写死补丁号 |
| 6 | 寒风营地的**两个官方中文名打架** | 同一个客户端里：`AreaTable` 写**寒风营地**，`TaxiNodes` 的飞行点名串写**冰风岗**。两条都是官方本地化 | 树里 `name_zh` 用 `AreaTable` 的**寒风营地**（这是玩家进区域时屏幕上弹的那串），`note_zh` 记了飞行列表里的异名 |
| 7 | `Shindigger's Camp` 中英文不同源 | 官方中文是**拉普索迪营地**，与英文名对不上（客户端两列就是这么写的） | 已按客户端 `zhCN` 收录并在 `note_zh` 标注。**不要以为是译错就自行改成「辛迪格营地」** |
| 8 | `The Green Belt` 绿带草地 | 在旧世 `AreaTable` 里确实存在（ID 1019，挂在东瘟疫之地下），但**世界地图上不单独标注**，本轮没能定位它的具体位置 | 已收进树并在 `note_zh` 写明「实拍前进游戏再确认位置」 |
| 9 | **墓地（graveyard）点位全缺** | `WorldSafeLocs` 表在 `wago.tools` 上返回 `Table not found`，拿不到复活点坐标 | 任务书把「墓地」列为该挂的地标类型。本片区只收到了作为**区域**的墓地（悔恨岭、墓室、乌瑟尔之墓），**没有逐个复活点**。若下游要拍「倒地→墓地复活→跑尸」这类游戏感桥段，需要另找数据源 |
| 10 | 大部分子区域**没有坐标** | 只有在 `AreaPOI` / `TaxiNodes` / `AreaTrigger` 里出现过的点才有坐标（本片区 22 个节点有），其余 100 个 `coords` 留空 | 按任务书「查不到留空串」处理，**没有编造坐标**。需要时可再抓 `AreaPOI` 全表或进游戏补 |
| 11 | 圣光之愿礼拜堂的地下**银色黎明地穴** | 旧世确实可进，但 `AreaTable` 里没有独立区域条目，当前 wiki 页把它和军团再临的「圣光圣殿」混列 | **未收进树**。若要拍礼拜堂内景，按「教堂主殿 + 地下小地穴」处理并另行核实 |
| 12 | zone 等级带有两套口径 | 客户端/旧世数据库给的是阿拉希 30-40、辛特兰 40-50、西瘟疫 50-60、东瘟疫 55-60（`db.nfuwow.com` 逐个核过，已写进 `level` 字段）；社区常用的**练级带**口径是西瘟疫 51-58、东瘟疫 53-60 | 两套都不算错，树里用数据库口径，`note_zh` 记了练级带口径 |
| 13 | `Boulderfist Outpost` 石拳前哨的归属 | 它在 Classic Era 的 `AreaPOI` 里存在（ID 1010）、但**不是 `AreaTable` 区域**；当前 wiki 把它列在 `Boulder'gor` 下 | 已按 wiki 的层级挂在博德戈尔下，类型记为 `poi` 而非 `subzone` |

---

## ④ 本片区的地图图片链接清单

**只记 URL 与版权状态，本轮没有下载任何一张图。**
仓库既有裁定：暴雪美术资产**只进人眼、不入画、不上传给生成模型**——
下面这些图只能由人打开来核对地形与相对位置，**不得作为参考图喂进任何图像/视频生成模型**。

| # | 用途 | 链接 | 版权状态 |
|---|---|---|---|
| 1 | 阿拉希高地 · 当前版本地图 | `https://warcraft.wiki.gg/wiki/File:VZ-Arathi_Highlands-t1.jpg` | 暴雪美术资产（wiki 托管），**仅供人眼核对** |
| 2 | 辛特兰 · **1.5 补丁之前**的旧地图 | `https://warcraft.wiki.gg/wiki/File:WorldMap-Hinterlands-original.jpg` | 同上。对旧世考据价值最高的一张——它是本片区唯一一张明确标注「早于某补丁」的原始地图 |
| 3 | 西瘟疫之地 · **大地的裂变之前**的地图 | `https://warcraft.wiki.gg/wiki/File:WorldMap-WesternPlaguelands-old.jpg` | 同上。**旧世取景请看这张，不要看下一张** |
| 4 | 西瘟疫之地 · 当前版本地图 | `https://warcraft.wiki.gg/wiki/File:WorldMap-WesternPlaguelands.jpg` | 同上。仅用于对照「哪里被改了」 |
| 5 | 辛特兰 · 地形图（第三方绘制） | `http://wow.gamepressure.com/map.asp?ID=21` | 第三方站点自绘，版权归该站；仍按「仅人眼」处理 |
| 6 | 四个 zone 的分区图（通用入口） | `https://warcraft.wiki.gg/wiki/Arathi_Highlands` / `.../Hinterlands` / `.../Western_Plaguelands` / `.../Eastern_Plaguelands` 页内 Maps 一节 | 同上 |

> 东瘟疫之地的旧世专用地图**没有找到**独立的 `-old` 文件（wiki 上该 zone 只挂了当前版本地图）。
> 东瘟疫之地的地形在 4.0.3 改动相对小（主要是死亡骑士起始区那一块），但**北面塔拉斯通道一带**
> 当前地图与旧世不同，核对时注意。

---

## ⑤ 给下游的提醒

1. **合龙时必须有人认领 `lordaeron`。** 本片区 4 个 zone 的 `parent` 全部写 `lordaeron`
   （类型应为 `region`，其上接 `eastern_kingdoms` → `azeroth`）。我**没有**定义这个节点，
   以免和别的片区重复定义。**如果合龙时发现没人定义它，树会断在这里**——请指定一个片区补上。
   这是本片区唯一的跨片区 parent。
   **已核**：同目录的 `g06_lordaeron_north.yaml` 的 zone 也一律 `parent: lordaeron`，拼法与我一致；
   但扫过当前目录的全部片区文件，**没有任何一个片区定义了 `lordaeron` 这个节点本身**。

2. **跨片区的 `adjacent` 引用了四个不属于我的 id**：`hillsbrad_foothills`、`wetlands`、
   `tirisfal_glades`、`alterac_mountains`。合龙时请确认这四个 id 的拼法与对方片区一致。

3. **同一个实体被客户端拆成多个同名区域，本树按 zone 加了限定后缀**，合龙时不要合并：
   - 禁忌之海 → `forbidding_sea_arathi` / `forbidding_sea_hinterlands` / `forbidding_sea_eastern_plaguelands`
   - 达隆米尔湖 → `darrowmere_lake_wpl` / `darrowmere_lake_epl`（同一片湖，跨两个 zone）
   - 索多里尔河 → `thondroril_river_wpl` / `thondroril_river_epl`（同一条界河，跨两个 zone）
   - 斯坦索姆 → `stratholme_city`（野外区域）/ `stratholme_instance`（副本，独立地图）
   其他片区如果也测到了禁忌之海（例如提瑞斯法或幽暗城沿海），**请同样加限定后缀，不要复用我的 id**。

4. **本片区有一条剧情时间线开关：纳克萨玛斯。** 它是 1.11 才开放的。
   如果剧本把「主角练到 60 级」放在一条隐含的版本时间轴上，**病木林上空有没有那座黑色浮空要塞
   是一个会被观众一眼看出来的硬穿帮**。建议在立项时就把「本剧锚定在 1.12（含 1.11 内容）」
   写进系列圣经，然后放心让它出现在所有病木林镜头的天空里。
   同理，阿拉希盆地战场是 1.7.0 才有的。

5. **镜头价值排序（给选景用）。** 本片区可用的强画面点，按「一眼认得出 + 情绪浓度」排：
   乌瑟尔之墓（圣骑士题材的必到点）> 斯坦索姆城门 > 纳克萨玛斯悬在病木林上空 >
   激流堡废墟 + 阿拉索之塔 > 辛萨罗层叠山城 > 达隆郡鬼村 > 悔恨岭墓海 >
   凯尔达隆湖心鬼岛 > 壁炉谷（焦土中唯一完好的红瓦城镇）> 瑟拉丹翡翠传送门 >
   萨多尔大桥断口 > 阿拉希禁锢法阵石柱群 > 蘑菇谷巨型菌伞。
   **主角若是人族圣骑士，「乌瑟尔之墓 → 索多里尔河边的提里奥·弗丁 → 圣光之愿礼拜堂」
   是一条现成的、贯穿本片区的精神主线**，三处都在树里。

6. **色调分组（给 `style_guide` 用）。** 本片区四个 zone 的色调差异极大，不要用一套共用光色串：
   阿拉希高地＝金褐 + 灰蓝天，通透干燥；辛特兰＝深墨绿 + 湿气，光从树冠碎落；
   西瘟疫之地＝灰橙 + 淡绿雾，病态但还有农田轮廓；东瘟疫之地＝猩红橙 + 暗红天，
   全片区最饱和最压抑。**跨 zone 赶路的连场戏，色调必须跟着换**，这正是仓库
   `ai_video.md` 16.9 说的「全镜共用串里不能写死只属于部分镜的光线设定」。

7. **等级带与剧情推进的对应**（本片区是 30 级到 60 级的整条后半段）：
   阿拉希高地 30-40 → 辛特兰 40-50 → 西瘟疫之地 50-60 → 东瘟疫之地 55-60。
   这四个 zone 正好可以撑起「主角从中期打到满级」的整段，且**旧世的陆路只有一条主干**
   （见 §2.5），赶路戏的地理是自洽的、不用杜撰捷径。

8. **不要因为一条新规则就回头刷旧剧。** 本文件与 YAML 只是考据素材；
   若日后修订版本口径（例如决定改锚到 1.11 之前），按仓库规则**只对新增与改动的产物生效**。
