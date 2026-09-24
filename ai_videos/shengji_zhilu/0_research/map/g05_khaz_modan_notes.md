# G05 · 卡兹莫丹 + 铁炉堡 —— 测绘备注

> 本文件**只放不属于树的东西**。所有节点数据在 `g05_khaz_modan.yaml`，此处不重复。
> 版本锚点：**经典旧世 Vanilla / Classic Era（1.12）**。

---

## ① 自查对账

### 方法上的一个关键改变（建议其他片区也照做）

原计划是「逐个 zone 抓 wiki 页 + 读 Subzones 一节」。实际做下来发现，**warcraft.wiki.gg 的 zone 页默认是
大地裂变后的版本**，Subzones 一节把旧世地名和 4.0.3 新增地名混在一起列，逐条判断版本要抓几十个子页面，
既慢又容易判错（第一轮抓 Algaz Station / Direforge Hill 两个页面，页面里根本没有版本信息，问不出结果）。

改用的办法是：**直接拉 Blizzard 自己的 DBC 数据当底稿，wiki 只用来补描述与出处原句。**

- `https://wago.tools/api/builds` → 找到 **`wow_classic_era` 构建 `1.15.9.69722`**（Classic Era ＝ 旧世内容）。
- `https://wago.tools/db2/AreaTable/csv?build=1.15.9.69722&locale=enUS`（与 `locale=zhCN`）
  → 得到旧世**完整**的 area 列表（含 `ParentAreaID` / `ExplorationLevel`）与**国服官方简体译名**，1212 行。
- `UiMap` + `UiMapAssignment` → 每张区域地图的世界坐标包围盒。
- `WorldMapOverlay` + `UiMapXMapArt` → 每个子区域高亮贴图的画布偏移，换算出**每个子区域的地图坐标**。
- `AreaPOI`、`TaxiNodes` → 聚居地图标与飞行点的世界坐标，同样换算成地图百分比。
- `LFGDungeons` → 副本的旧世等级区间。

**这一步把「哪些地名属于旧世」从判断题变成了查表题**：凡是在 Classic Era AreaTable 里的就是旧世的，
不在的就不是。交叉验证的结果见 § ②，与 wiki 的 Cataclysm 标注**逐条吻合**，没有冲突。

### 抓到的页面（人眼读过 ＝ `ai_read`）

| 来源 | 内容 | 结果 |
|---|---|---|
| `wago.tools` AreaTable / UiMap / UiMapAssignment / WorldMapOverlay / UiMapXMapArt / AreaPOI / TaxiNodes / LFGDungeons（Classic Era 1.15.9.69722，enUS+zhCN） | 旧世 area 全表 + 官方中文名 + 坐标 + 副本等级 | ✅ 全部拿到 |
| `wago.tools` AreaTable（正式服 12.1.0.69875，enUS+zhCN） | 仅用于补铁炉堡城内分区的官方中文名 | ✅ 拿到（部分条目仍缺，见 § ③） |
| `github.com/cmangos/issues/wiki/AreaTable.dbc` | 第一轮用的 DBC 列表 | ⚠️ 实测是 **WotLK 版**（含诺森德、达拉然），且缺行；已弃用，仅作交叉参考 |
| warcraft.wiki.gg：Dun_Morogh / Loch_Modan / Wetlands / Badlands / Ironforge | zone 信息框 + Subzones + 邻接 + 交通 | ✅ |
| warcraft.wiki.gg：Kharanos / Thelsamar / Menethil_Harbor / Dun_Modr / Kargath / Uldaman / Gnomeregan / Angor_Fortress / Coldridge_Valley / Brewnall_Village / Stonewrought_Dam / Thandol_Span / The_Lost_Fleet / Camp_Wurg / Algaz_Station / Direforge_Hill / Stonewrought_Pass / The_Great_Forge / Tinker_Town | 描述、坐标、版本差异、原句 | ✅ |

### 抓不到的

| 站点 | 结果 | 影响 |
|---|---|---|
| `classic.wowhead.com` / `www.wowhead.com/classic/zone=N&xml` | **HTTP 403**（含 `&xml` 绕法、换 UA 直连均被拒） | 无。坐标与等级已由 DBC 覆盖，且精度更高 |
| `wow.huijiwiki.com`（灰机） | 中文标题 404、英文标题被 **Cloudflare 挑战**、`api.php` 被拒 | 无。官方中文名已由 zhCN DBC 覆盖，比灰机更权威 |
| `db.nfuwow.com` | 可访问，但只给区域级中文名，不给子区域清单 | 仅用作中文区域名的旁证 |
| `wowgaming.altervista.org/aowow` | 页面基本为空壳 | 无 |
| WebSearch | **本 session 搜索额度已用尽（200/200）** | 少量铁炉堡分区的中文名无法再查，已按规则保留英文原名 |

### 节点统计

| zone | 节点数（含 zone 自身） | 备注 |
|---|---|---|
| dun_morogh 丹莫罗 | 25 | Classic AreaTable 里丹莫罗共 24 个子 area，**一个不漏**，全部入树 |
| ironforge 铁炉堡 | 23 | 城内分区在 AreaTable 里**没有条目**（见 § ③），按 wiki 的 Subzones 一节建树 |
| loch_modan 洛克莫丹 | 19 | AreaTable 16 个子 area 全收 + 飞行点 + 石门通道；本区旧世地名本身就少，不是没查全 |
| wetlands 湿地 | 29 | AreaTable 25 个子 area 全收（含两片外海）+ 飞行点 + 两条船 |
| badlands 荒芜之地 | 24 | AreaTable 17 个子 area 全收 + 飞行点 + 奥达曼内部 4 个厅 + 灼热峡谷山口 |
| khaz_modan（region） | 1 | |
| **合计** | **121** | 全部 `era: vanilla`，全部 `verified_by: ai_read` |

---

## ② 版本差异（4.0.3 大地裂变改了什么）—— 逐条

判据：**该地名是否出现在 Classic Era（1.15.9）AreaTable 中**。不在 ＝ 4.0.3 及之后才有，不进树。

### 丹莫罗 Dun Morogh（本片区受灾最重）

| wiki 上列着、但**不是旧世**的地名 | 说明 |
|---|---|
| New Tinkertown 新工匠镇 | 4.0.3 新增的**侏儒专属新手区**。旧世侏儒和矮人一起从寒脊山谷出生 |
| Crushcog's Arsenal、The Toxic Airfield | 随新工匠镇一起加的侏儒剧情点 |
| Frostmane Front、Frostmane Retreat、Frostmane Hovel | 4.0.3 新增的霜鬃巨魔点位（旧世只有 Frostmane Hold 霜鬃巨魔要塞） |
| Whitebeard's Encampment | 4.0.3 新增，在寒脊山谷内 |
| The Mountain Den、Ironforge Airfield、Newman's Landing、Bahrum's Post | 均不在旧世 AreaTable |
| Brewfest Grounds 啤酒节会场 | 2.2（TBC）才加的节日场地 |
| Gol'Bolar Quarry Mine | 采石场深处的矿洞在旧世**有洞体但没有独立地名**，不作为节点 |
| 卡拉诺斯飞行点、古博拉采掘场飞行点 | **4.0.3a 才加**。旧世丹莫罗全区**没有任何飞行点**，进出只能靠走或进铁炉堡坐狮鹫 |
| 寒脊山小径塌方 | 4.0.3 patch note 原文：`Coldridge Pass caved in. Major changes to landscape.` 旧世是通的 |

### 洛克莫丹 Loch Modan

| 变化 | 说明 |
|---|---|
| **巨石水坝被死亡之翼炸毁、洛克湖排干九成** | 本区最大的版本差异。**旧世湖是满的**，水面几乎铺满谷底——拍摄时这是决定性的画面差别，参考图千万别用 4.0.3 后的截图 |
| Twilight Camp、Ironwing Cavern | 4.0.3 新增 |
| 旅行者营地（Farstrider Lodge）的飞行点 | 4.0.3 才加；旧世本区**只有塞尔萨玛一个飞行点** |
| 碎石怪之谷的深层洞穴系统 | 4.0.3 扩建；旧世只有谷地和浅洞 |
| 灰爪山的黑铁间谍 | 4.0.3 才加的 NPC |

### 湿地 Wetlands

| 变化 | 说明 |
|---|---|
| Greenwarden's Grove 绿色守护者之林 | 4.0.3 新增的**夜精灵据点**。旧世湿地没有任何夜精灵聚落 |
| Slabchisel's Survey、Swiftgear Station、Whelgar's Retreat | 4.0.3 新增，并各带一个飞行点 |
| 丹莫德归属 | **旧世是黑铁矮人占领的敌对据点**（首领术士 Balgaras the Foul）；4.0.3 后被铁炉堡夺回变成友方。阵营完全相反，别弄反 |
| 米奈希尔港半沉 | 4.0.3 后港镇一部分沉入海中、少女之贞号沉没、城堡受损。**旧世港镇是完好的** |
| 奥伯丁航线 | 旧世 `米奈希尔港 ↔ 奥伯丁（黑海岸）` 成立；3.0.2（WotLK）后改线 |
| 瓦尔加德航线 | WotLK 才有，不属旧世 |
| 湿地飞行点数量 | 旧世**只有米奈希尔港一个**；4.0.3 后变成五个 |

### 荒芜之地 Badlands（阵营格局整个换掉）

| 变化 | 说明 |
|---|---|
| **卡加斯被山崩掩埋，代之以 New Kargath 新卡加斯** | 旧世卡加斯还在，且是**卡兹莫丹唯一的部落据点** |
| Fuselight、Fuselight-by-the-Sea | 4.0.3 新增的哥布林城镇 |
| Dragon's Mouth、Dustwind Dig、Bloodwatcher Point、Rhea's Camp | 4.0.3 新增。**旧世荒芜之地没有任何联盟据点、也没有任何联盟飞行点** |
| Scar of the Worldbreaker、The Hidden Clutch、Crypt | 4.0.3 新增（灭世者之痕正好犁过瓦格营地） |
| Tomb of the Watchers 观察者的陵墓（作为荒芜之地的地面区域） | 旧世该名称只存在于**奥达曼副本内部**，不是地面 area |
| 洛克莫丹 ↔ 荒芜之地 | **旧世可以步行南下**；4.0.3 在交界处裂出深渊，通路被切断 |

### 铁炉堡 Ironforge

| 变化 | 说明 |
|---|---|
| Dark Iron Embassy 黑铁大使馆 | 4.0.3 后三锤议会成立才有 |
| Old Ironforge 旧铁炉堡 | 地图数据里旧世就存在，但**玩家不可进入**，4.0.3 后才开放。若要入镜只能当「不可达的封闭区域」处理 |
| The Forlorn Cavern 荒弃的洞穴 | 洞体旧世即有，但作为**带名字的子区域**是后来才加进 AreaTable 的（ID 4679 属 WotLK 段） |
| 统治者 | 旧世是**麦格尼·铜须**；三锤议会（穆拉丁 / 茉艾拉 / 法斯特）是 4.0.3 之后。wiki 信息框写的是后者，别照抄 |

---

## ③ 存疑与未查

1. **铁炉堡城内分区在 Classic AreaTable 里完全没有条目。**
   实测：`ParentAreaID == 1537` 的行在 Classic Era 全表里**只有一条**（The Forlorn Cavern，且是后加的）。
   暴风城同理（`ParentAreaID == 1519` 只有英雄谷）。结论：**「大锻炉 / 秘法区 / 军事区 / 平民区 / 提克小镇」
   这类城内分区名是城市地图的美术标签，不是游戏内的子区域**。
   带来的两个后果：
   - **城内节点的 `coords` 基本为空**（没有 overlay 数据可换算）。唯一有坐标的是铁炉堡狮鹫场
     `[56, 48]`，由 TaxiNodes 世界坐标换算得出。wiki 的 Ironforge 页面**通篇没有任何坐标对**（已确认）。
   - 中文名只能从**正式服** AreaTable 取（同名同地，译名沿用），已取到：
     平民区 / 大锻炉 / 秘法区 / 军事区 / 武器大厅 / 探险者大厅 / 荒弃的洞穴 / 石火旅店 / 酒桶与铁砧 / 矿道地铁。

2. **官方译名未查到、`name_zh` 按规则保留英文原名的节点**（共 9 个，全部在 `note_zh` 里写明）：
   `the_high_seat`、`hall_of_mysteries`、`bruuks_corner`、`the_library_ironforge`、`the_museum_ironforge`、
   `tinker_town`、`berryfizzs_potions`、`old_ironforge`，以及奥达曼内部的
   `uldaman_dig_one` / `uldaman_map_chamber` / `uldaman_hall_of_the_keepers` / `uldaman_khazgoroths_seat`。
   这些在 Classic 与正式服 AreaTable 里都查无此条，灰机 wiki 被 Cloudflare 拦、WebSearch 额度已尽。
   `the_high_seat` 与 `hall_of_mysteries` 的记忆候选译名已写进 `note_zh` 并标「待核」，**没有直接当成事实写进 `name_zh`**。
   另有 3 个节点用了**常见译法但 DBC 无条目**，已在 `note_zh` 标为存疑：
   `vault_of_ironforge`（铁炉堡金库）、`the_great_anvil`（大铁砧）、`stonewrought_pass`（石门通道）。

3. **正式服 `Hall of the Keepers 守护者大厅` 不能直接套给旧世奥达曼**——正式服那条（ID 14144）属于
   巨龙时代重做的**新奥达曼副本**，与旧世奥达曼不是同一处地图。故旧世奥达曼内部厅名一律留英文。

4. **坐标有两种口径，混用会对不上**：
   - **区域质心**（由 `WorldMapOverlay` 贴图中心换算）——用于 subzone / 大片区域。
   - **图标点位**（由 `AreaPOI` / `TaxiNodes` 世界坐标换算，或 wiki 给的数值）——用于聚居地、副本口、飞行点。
   两者对同一个地方可以差 10 个点以上（例：苦痛堡垒 质心 `[42, 37]` vs wiki 点位 `[41, 25]`；
   卡加斯 质心 `[12, 41]` vs 图标 `[4, 47]`）。**本片区的聚居地 / 副本 / 飞行点一律取图标点位**，
   subzone 取质心。下游如果要做「镜头站位」，请按这个口径读，别把两种混在一张图上量距离。

5. **诺莫瑞根等级区间**用的是 Classic Era `LFGDungeons` 的 `MinLevel 24 / MaxLevel 40`，
   奥达曼是 `38 / 53`。这与玩家社区常说的「推荐 29-38 / 42-52」不是一回事——
   DBC 给的是**准入区间**，社区给的是**推荐区间**。树里记的是前者。

6. **未查**：本片区所有 zone 的**具体任务链、怪物刷新点、NPC 名录**均不在本次范围内，
   只在 `note_zh` 里点到为止（例如「旧世被穴居人占据」）。下游若要排「练级路线」还得单开一轮。

---

## ④ 本片区的地图图片链接清单

> **仓库已裁定：暴雪美术资产只进人眼、不入画、不上传给生成模型。**
> 下列链接**只记 URL 与版权状态，不下载、不落盘、不喂模型**，仅供人工比对地形用。

| 用途 | URL | 版权状态 |
|---|---|---|
| 丹莫罗 zone 页（含旧世/新版两张地图切换） | https://warcraft.wiki.gg/wiki/Dun_Morogh | Blizzard 美术资产，warcraft.wiki.gg 以 fair use 托管；**禁止下载／喂模型** |
| 洛克莫丹 zone 页（Classic 地图版本可切） | https://warcraft.wiki.gg/wiki/Loch_Modan | 同上 |
| 湿地 zone 页 | https://warcraft.wiki.gg/wiki/Wetlands | 同上 |
| 荒芜之地 zone 页 | https://warcraft.wiki.gg/wiki/Badlands | 同上 |
| 铁炉堡城市地图（`Map of Ironforge` / `Map of Old Ironforge` 两张） | https://warcraft.wiki.gg/wiki/Ironforge | 同上；**这是铁炉堡分区布局的唯一可视来源**（数据层没有） |
| 奥加兹岗哨页（页面内同时挂 Cataclysm 与 Classic 两版地图） | https://warcraft.wiki.gg/wiki/Algaz_Station | 同上 |
| 石门通道（灼热峡谷一侧截图） | https://warcraft.wiki.gg/wiki/Stonewrought_Pass | 同上 |
| 失落的舰队（沉船实拍截图数张） | https://warcraft.wiki.gg/wiki/The_Lost_Fleet | 同上 |

**提醒**：warcraft.wiki.gg 的 zone 地图默认显示 Cataclysm 版；页面上通常有 `Classic` 切换。
人工比对地形时**务必先切到 Classic**，否则看到的洛克莫丹是排干的、米奈希尔港是半沉的。

---

## ⑤ 给下游的提醒

1. **任务书里有三处地名张冠李戴，已按实际订正**：
   - 「铁环水坝 Thelsamar」→ **Thelsamar 的官方译名是「塞尔萨玛」**。
     「铁环」是 Ironband（对应 `铁环挖掘场` / `铁环营地` 两个不同地点），
     「水坝」是 Stonewrought Dam `巨石水坝`。三个是三处不同的东西，别合并。
   - 「提尔的手 Tinker Town」→ **提尔的手是东瘟疫之地的 Tyr's Hand**，跟铁炉堡无关。
     铁炉堡的侏儒区英文是 Tinker Town，官方中文名本轮未查到（见 § ③）。
   - 「诺莫瑞根入口在提尔的手?」→ **不是**。入口在**丹莫罗的寒风峡谷（Chill Breeze Valley）**，
     坐标 `[24, 40]`，与铁炉堡城内无关。
   - 「血色修道院? 不在这里」→ 确认**不在本片区**（在提瑞斯法林地）。

2. **两条「阵营会拍错」的硬事实**：
   - **旧世荒芜之地没有任何联盟据点、没有任何联盟飞行点**，唯一城镇卡加斯是部落的。
     主角若是人族圣骑士，到这一区只能露营、没有落脚点——这本身是很好的戏剧素材，别顺手给他安排个联盟小镇。
   - **旧世丹莫德是黑铁矮人的敌对据点**，不是友方矮人村。

3. **旧世飞行点在本片区只有 4 个**（已全部入树，Classic Era TaxiNodes 实测）：
   铁炉堡（城内·大锻炉东侧）、塞尔萨玛（洛克莫丹）、米奈希尔港（湿地）、卡加斯（荒芜之地·仅部落）。
   **卡拉诺斯、古博拉采掘场、旅行者营地这三处的飞行点全部是 4.0.3a 之后才有的**，
   写练级路线时别让角色在这些地方起飞。

4. **画面上最该注意的版本差异**（会一眼穿帮的）：
   洛克湖**是满的**、米奈希尔港**是完整的**、寒脊山小径**是通的**、卡加斯**还在**、
   丹莫德**冒着黑铁矮人的黑烟**、铁炉堡王座上坐的是**麦格尼·铜须**。

5. **合龙时要对账的跨片区引用**：
   - 唯一的跨片区 parent 是 **`eastern_kingdoms`**（`khaz_modan` 挂在它下面）。
   - `adjacent` 里引用了本片区之外的 id：`searing_gorge`、`arathi_highlands`、`dustwallow_marsh`、
     `darkshore`、`stormwind_city`。请确认对方片区用的是同一批 id。
   - **`ironforge` 的 parent 我挂在 `dun_morogh` 下**（因为进城的门 `铁炉堡大门` 在丹莫罗境内，
     地理上递进更顺）。如果主树统一规定主城与 zone 平级、直接挂 region，改 `parent: khaz_modan` 即可，
     其余 22 个城内节点不受影响。**暴风城那边请确认用的是同一种挂法**，别一个挂 zone 一个挂 region。
   - `dun_algaz` 这个地名在 AreaTable 里**洛克莫丹和湿地各有一条**（同一条隧道的两端），
     本树按规则加了限定：`dun_algaz_loch_modan` / `dun_algaz_wetlands`。
     `north_gate_pass` / `south_gate_pass` 同理，也是两端各一条，已加 `_dun_morogh` / `_loch_modan` 限定。

6. **建议主树生成器加两条机检**（本片区已自查通过）：
   - 所有 `parent` 必须能在合并后的 id 全集里解析（本片区仅 `eastern_kingdoms` 外指）。
   - `type in {settlement, transport}` 时 `subtype` 必填；`type in {zone, dungeon, raid}` 时 `level` 必填、
     其余必须为空串；`adjacent` 非空时 `type` 必须是 `zone` / `continent` / `city`。

7. **这套 DBC 取源方法可以直接复用到别的片区**，命令都在 § ① 里。
   对「旧世到底有没有这个地名」这类问题，它比逐页读 wiki 快一个数量级，而且**结论可机检、可复现**。
