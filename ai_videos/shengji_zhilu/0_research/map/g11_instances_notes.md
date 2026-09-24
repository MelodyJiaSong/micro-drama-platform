# G11 · 全副本 / 团本 / 战场总表 —— 备注（非树数据）

> 树数据的唯一出处是 `g11_instances.yaml`。本文件**不重复任何树里已有的字段**，
> 只放：自查对账 · 取源口径 · 版本差异 · 存疑与未查 · 与其它片区的对账 · 地图图片链接 · 下游提醒 · 副本推进表。

- `group_id`: **G11**
- 版本锚点：**经典旧世 Vanilla / Classic Era (1.12)**
- 节点数：**409**（副本根 37 · 内部分区 103 · boss 与地标 269）—— 独立核验 G11-V 补 5 个后的数，见文末 § 核验记录
- 覆盖：五人本 20 座（血色修道院拆四翼、厄运之槌拆三翼、黑石塔拆上下层，故根节点 27 个）· 团本 7 座 · 战场 3 座

---

## ① 自查对账

### A. 这一轮真正拿到手的东西

| 来源 | 拿到什么 | 结果 |
|---|---|---|
| `warcraft.wiki.gg` 各副本条目（**优先 `_(Classic)` 后缀页**） | 每个副本的 loc / classiclevel / players / 入口描述 / boss 英文名 | ✅ 30 个副本条目逐页抓下来读了 |
| `wago.tools` **`DungeonEncounter`**（Classic Era `1.15.9.69722`，enUS + zhCN） | **每个 boss 的国服官方简体名 + 官方 `OrderIndex` 战斗顺序** | ✅ 这是本片区最关键的一击，见 § ②B |
| `wago.tools` **`WMOAreaTable`**（enUS + zhCN） | 副本**内部分区**的国服官方简体名（黑石深渊 22 个厅、斯坦索姆 17 个街区、通灵学院 15 个房间、厄运之槌 12 个区…） | ✅ 全部拿到 |
| `wago.tools` `AreaTable`（enUS + zhCN） | 祖尔格拉布 11 区 / 安其拉废墟 6 区 / 阿拉希盆地 7 据点 / 奥特兰克山谷 27 个地名 | ✅ |
| `wago.tools` `Map`（enUS + zhCN） | **副本本身的官方中文名 + `MaxPlayers` 人数上限** | ✅ 29 个 vanilla 实例地图 |
| `wago.tools` `LFGDungeons`（enUS + zhCN） | **官方准入等级带** + 厄运之槌三翼的官方中文名（「厄运之槌 - 东 / 西 / 北」） | ✅ |

**取源方法沿用 G05 在 `g05_khaz_modan_notes.md` § ① 里趟出来的那条路**（直接拉暴雪自己的 DBC 当底稿，
wiki 只用来补描述与出处原句）。本片区在它基础上多挖出两张表：
`DungeonEncounter`（boss 名 + 顺序）与 `WMOAreaTable`（副本内部地名）——
**这两张表把「boss 中文名靠记忆」从一个必然要打折扣的环节变成了查表题**，强烈建议后续片区复用。

命令（照抄即可）：

```bash
B=1.15.9.69722
for t in Map AreaTable LFGDungeons WMOAreaTable DungeonEncounter; do
  for L in enUS zhCN; do
    curl -sS -o "${t}_${L}.csv" "https://wago.tools/db2/${t}/csv?build=${B}&locale=${L}"
  done
done
```

### B. 抓失败 / 没通的路

| 路 | 结果 | 补救 |
|---|---|---|
| `The_Stockade_(Classic)` | **404** | 正确标题是 `Stormwind_Stockade_(Classic)`，已抓到 |
| `Gnomeregan_(Classic)` / `Gnomeregan_(Classic_instance)` | **两个都 404** | 没有独立 Classic 页（4.0.3 只改了外围，本体未重做）。等级带改由 `LFGDungeons` 给，入口坐标由 `Gnomeregan` 正页给 |
| `Uldaman_(Classic)` / `Zul'Farrak_(Classic)` / `Maraudon_(Classic)` | **404** | 同上——这几个本从未被大改，**正页就是旧世内容**，已按正页取 |
| `Dire_Maul_East / West / North` | 都是 `#redirect` | 跟到真页 `Warpwood_Quarter` / `Capital_Gardens` / `Gordok_Commons`，已抓到 |
| `Scarlet_Monastery_(Classic)` | `#redirect` 回正页 | 改抓四翼各自的独立页（`Scarlet_Monastery_Graveyard` 等），四页全部拿到 |
| `Upper_Blackrock_Spire` 正页 | 是**德拉诺之王 6.0 版**（100 级、末 boss 扎艾拉） | 跟页首 `{{About}}` 跳到 `Upper_Blackrock_Spire_(Classic)`，已抓到 |
| `wow.huijiwiki.com`（灰机，任务书指定的中文源） | **HTTP 403**（与 G01/G05/G06 记录一致） | **不需要了**——官方中文名已由 zhCN DBC 全量覆盖，比灰机更权威（灰机本身也是照抄客户端） |
| `www.wowhead.com/classic/zone=721&xml`（任务书给的绕法） | 返回的是导航壳，没有 XML 数据 | 等级/人数已由 `LFGDungeons` + `Map` 覆盖且更权威 |
| `WebSearch` | **本 session 额度已耗尽（200/200），第一次调用就被拒** | 全程改走 WebFetch 直链 + DBC；对结论无影响 |
| `JournalEncounter` / `JournalInstance` / `DungeonMap`（1.15.9） | `Table not found` / 空 | Classic Era 没有地下城日志；纳克萨玛斯四区的中文名因此缺失，见 § ④.2 |

### C. 头号雷区：抓到了改版后的 boss 表

**任务书点名的「4.0.3 雷区」在本片区表现为一种更隐蔽的形式：wiki 正页默认给的是正式服 boss 名单。**
实测三例（都已弃用）：

- `Deadmines` 正页 → 格鲁布托克 / 螺丝钳 / 割草机 5000 / 瓦内萨·范克里夫 —— **全是大地裂变的**，
  旧世是拉克佐 / 斯尼德 / 基尔尼格 / 绿皮船长 / 重拳先生 / 曲奇 / 艾德温·范克里夫。
- `Shadowfang_Keep` 正页 → 阿什巴利男爵 / 瓦尔登勋爵 / 戈德弗雷勋爵 —— **也是大地裂变的**。
- `Ragefire_Chasm` 正页 → 阿达罗格 / 黑暗萨满科兰萨尔 / 熔口 —— **也是改版后的**。

**纪律：本片区每一个 boss 的英文名与顺序，最终都以 `_(Classic)` 页或 Classic Era `DungeonEncounter` 表为准，
正页只用来取「入口在哪」这种没被改过的描述。**

---

## ② 取源口径约定（下游必读）

### A. `level` 字段填的是哪个数

客户端里有**两个不同口径**的等级，它们不是矛盾，是两件事：

1. **wiki 的 `classiclevel`** —— 本里怪的实际等级带，也是玩家口语里「这本几级打」的那个数。
2. **客户端 `LFGDungeons` 的 `MinLevel`/`MaxLevel`** —— **准入区间**，比前者宽得多（死亡矿井 15-28、诺莫瑞根 24-40）。

**本表 `level` 取第 1 个（wiki classiclevel），第 2 个写在 `note_zh` 里标为「客户端准入带」。**
理由：下游是写剧本选景的，需要的是「主角这时候几级、打这本合不合适」。
§ ⑧ 的推进表两个数都给。

### B. `name_zh` 的可信度分级（**比 `verified_by` 更细，务必看这一节**）

`verified_by` 记的是「出处页/表有没有真的抓到」，不等于中文译名也核过。本片区分三档：

| 档 | 数量 | 说明 |
|---|---|---|
| **A · 客户端 zhCN 表直出** | 副本名 29 / boss 名 **211** / 内部分区名 99 | 出自 Classic Era `1.15.9.69722` 的 `Map` / `DungeonEncounter` / `WMOAreaTable` / `AreaTable` zhCN，**等于国服客户端里显示的字**，`quote` 字段写了「英文名 = 中文名」的原始行 |
| **B · 未查到，按规则留英文原名** | **21** | 都是客户端表里没有对应行的稀有精英 / 事件 boss / 地图美术标签，`note_zh` 一律写明「官方译名未查到（不在客户端 DungeonEncounter 表内）」。清单见 § ④.1 |
| **C · 部分核到** | **1** | `scarlet_commander_mograine`「血色十字军指挥官莫格莱尼」——客户端把他与怀特迈恩记作同一场，没有独立行；姓氏「莫格莱尼」由 `天启四骑士·大领主莫格莱尼` 与 `莫格莱尼之魂` 两行交叉印证，**完整头衔未核到** |

**一个字都没有自己音译。** 21 个 B 档全部保留英文原名。

### C. boss 为什么是 `poi`

schema 的 `type` 枚举没有 `boss`。boss 房 / boss 所在平台本身就是任务书定义的「地标」，
故一律 `type: poi`，`note_zh` 以「第 N 场 · 」开头，**N 就是客户端 `DungeonEncounter.OrderIndex` 的官方排序**，
YAML 里的出现顺序也与之一致。下游要「按顺序列 boss」直接按文件顺序读即可。

### D. 人数

`note_zh` / 本文件 § ⑧ 里的人数取自 `Map.MaxPlayers`（Classic Era 客户端）。注意两个反直觉的地方：

- **多数「五人本」的客户端上限是 10**（死亡矿井、哀嚎洞穴、影牙城堡、黑暗深渊、暴风城监狱、
  诺莫瑞根、剃刀沼泽、剃刀高地、血色修道院、奥达曼、祖尔法拉克、玛拉顿、怒焰裂谷）。
  它们**设计上是 5 人本，但旧世允许带满 10 人进**。
- **沉没的神庙上限是 20**；黑石塔（上下层共用一张地图）上限是 10；
  黑石深渊 / 通灵学院 / 斯坦索姆 / 厄运之槌是**硬 5 人**。

---

## ③ 版本差异（4.0.3 及之后改了什么，逐条）

**本树只收 vanilla。下面是「正式服有、但不进树」或「进树但形态不同」的条目。**

### A. 被整本重做，boss 表完全不同（正页不可用）

| 副本 | 旧世 | 4.0.3 / 5.x 之后 |
|---|---|---|
| 死亡矿井 | 7 场，末 boss 艾德温·范克里夫 | 重做为「格鲁布托克 / 螺丝钳赫利克斯 / 割草机 5000 / 断牙上将 / 库奇船长 / 瓦内萨·范克里夫」并加英雄难度 |
| 影牙城堡 | 8 场，末 boss 大法师阿鲁高 | 重做为「阿什巴利男爵 / 席瓦莱恩男爵 / 斯普林瓦尔指挥官 / 瓦尔登勋爵 / 戈德弗雷勋爵」 |
| 怒焰裂谷 | 4 场（奥格弗林特 / 塔拉加曼 / 耶戈什 / 巴扎兰） | 重做为「阿达罗格 / 黑暗萨满科兰萨尔 / 熔口 / 熔岩卫士戈多斯」 |
| 血色修道院 | **四翼独立**（墓地 / 图书馆 / 军械库 / 大教堂），7 场 | 熊猫人之谜起并成**两个**副本（墓地 + 大教堂），图书馆与军械库整个删除；旧四翼在 10.1.7 才以「血色钥匙」形式部分恢复 |
| 通灵学院 | 14 场，五层结构 | 熊猫人之谜起大幅精简 |
| 斯坦索姆 | 两侧入口、19 场 | 部分内容移入「时光之穴·旧斯坦索姆」 |
| 祖尔格拉布 | **20 人团本**，10 场 | 4.1 重做为 **5 人本**，只剩 4 场 |
| 纳克萨玛斯 | **旧世 40 人**，东瘟疫之地上空 | 巫妖王之怒整座搬到诺森德，改 10/25 人 |
| 黑石塔上层 | **10 人**，56-61 | 德拉诺之王重做为 100 级 5 人本，末 boss 换成扎艾拉 |
| 奥妮克希亚的巢穴 | 60 级 40 人 | 巫妖王之怒改为 80 级 10/25 人 |
| 厄运之槌三翼 | **55-60 级** | 大地裂变等级压缩到东 36-46 / 西 39-49 / 北 42-52 —— **wiki 正页给的就是这组压缩后的数，别抄** |
| 玛拉顿 | 45-52 | 改为随区域缩放 |
| 诺莫瑞根 | 29-38（准入 24-40） | 7.3.5 起等级缩放 |

### B. 本树收了、但客户端表里混进了非 vanilla 行（已剔除）

抓 `DungeonEncounter` 时，Classic Era `1.15.9` 这个 build **含探索赛季（SoD）与周年服的增补**，
下面几行**已判定不属于 1.12，未进树**：

- **黑暗深渊**：~~`Lorgus Jett 洛古斯·杰特`（SoD 增补）~~ —— **G11-V 推翻：他是旧世就有的稀有精英**，`Blackfathom_Deeps_(Classic)` 页把他列在 Encounters 表的 **Bosses 列**（「Tunnels」一行），他本人的条目写明「removed in patch 6.0.2 but remains in World of Warcraft: Classic」，且 4.0.3a 还给他改过等级——说明 6.0.2 之前一直在。**已补进树**（`lorgus_jett`，第 8 场·稀有精英）。整组负 `OrderIndex` 的重复行仍判为 SoD 难度变体，未进树。
- **诺莫瑞根**：`Mechanical Menagerie 机械博览馆`（SoD 增补）、`Endgineer Omegaplugg`（正式服增补）。
- **沉没的神庙**：`Festering Rotslime 腐溃烂泥` / `Atal'ai Defenders 阿塔莱防御者`（SoD 增补）。
- **怒焰裂谷**：wiki 的 Classic 页把 `Zelemar the Wrathful` 列进 boss 表，**是补丁 2.0.3（燃烧的远征）加入的**，
  1.12 没有，未进树。G11-V 已用该页 Patch history 原文核实，见 § ④.3。
- **黑石深渊**：wiki 正页列出的 `Coren Direbrew`（酿酒节，巫妖王之怒才加）未进树。

### C. 地名层面的 4.0.3 雷区（与本片区相关的）

- **南贫瘠之地 / 北贫瘠之地**：4.0.3 把贫瘠之地劈成两半。剃刀沼泽与剃刀高地在正式服写作
  「南贫瘠之地」，**vanilla 只有一个「贫瘠之地」**。本表 `note_zh` 提到方位时写「南贫瘠之地」是**方位描述**，
  不是区域名；区域节点归 G09 的 `the_barrens`。
- **奥特兰克山脉**：4.0.3 并入希尔斯布莱德丘陵。奥特兰克山谷战场的入口节点归 G06，本表沿用其 `alterac_valley_entrance`。
- **祖尔格拉布入口**：4.0.3 后荆棘谷被拆成两个区域，本表沿用 G04 的 `stranglethorn_vale`。

---

## ④ 存疑与未查

### 1. 21 个「官方译名未查到」的节点（B 档，保留英文原名）

它们都**确实存在于旧世**（wiki 的 boss 表 / 分区表里逐个读到了），只是不在客户端的
`DungeonEncounter` / `WMOAreaTable` 里，所以拿不到国服官方简体名。按任务书规则保留英文原名。

| 节点 id | 英文原名 | 所属 | 性质 |
|---|---|---|---|
| `deviate_faerie_dragon` | Deviate Faerie Dragon | 哀嚎洞穴 | 稀有精英（通行译「变异精灵龙」） |
| `miner_johnson` | Miner Johnson | 死亡矿井 | 稀有精英 |
| `bruegal_ironknuckle` | Bruegal Ironknuckle | 暴风城监狱 | 稀有精英 |
| `dark_iron_ambassador` | Dark Iron Ambassador | 诺莫瑞根 | 稀有精英 |
| `blind_hunter` / `earthcaller_halmgar` | Blind Hunter / Earthcaller Halmgar | 剃刀沼泽 | 稀有精英 ×2 |
| `azshir_the_sleepless` / `fallen_champion` / `ironspine` | Azshir the Sleepless / Fallen Champion / Ironspine | 血色修道院·墓地 | 稀有精英 ×3 |
| `sergeant_bly` | Sergeant Bly | 祖尔法拉克 | 角斗场事件 NPC |
| `sandarr_dunereaver` / `zerillis` / `dustwraith` | Sandarr Dunereaver / Zerillis / Dustwraith | 祖尔法拉克（城外） | 稀有精英 ×3 |
| `solakar_flamewreath` / `goraluk_anvilcrack` / `gyth` / `jed_runewatcher` | Solakar Flamewreath / Goraluk Anvilcrack / Gyth / Jed Runewatcher | 黑石塔上层 | 4 场真实战斗，但客户端把它们并进别的行或根本没记 |
| `naxx_arachnid_quarter` … `naxx_frostwyrm_lair` | Arachnid / Plague / Military / Construct Quarter、Frostwyrm Lair | 纳克萨玛斯 | **五个分区在旧世客户端里是地图美术标签，不是 `AreaTable` 条目**，见下条 |

### 2. 纳克萨玛斯的分区名缺口（**最需要后续补的一处**）

蜘蛛区 / 瘟疫区 / 军事区 / 构造区 / 冰龙区这五个名字在 Classic Era 客户端里
**查不到任何一张表**（`AreaTable`、`WMOAreaTable` 都没有；`JournalEncounter` 在 1.15.9 里不存在）。
只有 `Sapphiron's Lair 冰霜巨龙的大厅` 与 `Kel'Thuzad Chamber 克尔苏加德的大厅` 两间在 `WMOAreaTable`（WMOID 4491）里。
所以五个分区按规则留英文原名，`note_zh` 里附了通行译名（蜘蛛区 / 瘟疫区 / 军事区 / 憎恶区 · 构造区 / 冰龙区）**仅供参考，未核**。
补法：拉一个含地下城日志的正式服 build 的 `JournalInstance` + `JournalEncounter`（zhCN），
纳克萨玛斯在正式服仍在，译名沿用。

### 3. 怒焰裂谷的 Zelemar

`warcraft.wiki.gg` 的 `Ragefire_Chasm_(Classic)` 页把 `Zelemar the Wrathful` 列为第 5 场，
但客户端 `DungeonEncounter` 的 map 389 只有 4 行（奥格弗林特 / 塔拉加曼 / 耶戈什 / 巴扎兰）。
普遍认为 Zelemar 是燃烧的远征增补。**按「宁可漏一个存疑的、不可编一个假的」的反向——这里是「宁可不收存疑的」——未进树。**

> **G11-V 已核实，存疑解除**：该页的 Patch history 一节白纸黑字写着 `{{Patch 2.0.3|note= [[Zelemar the Wrathful]] added.}}`——
> 2.0.3 是燃烧的远征的前置补丁，**1.12 没有他**。不进树是对的，本条可以结案。
若后续确认 1.12 就有，补一个节点挂 `ragefire_chasm` 即可。

### 4. 祖尔法拉克的译名在客户端内部自相矛盾

- `Map` 表（ID 209）：**祖尔法拉克**
- `LFGDungeons` 表（ID 23）：英文拼作 `Zul'Farak`（少一个 r，客户端笔误），中文作 **祖尔法兰克**

**本表取 `Map` 表的「祖尔法拉克」**（地图名是玩家实际看到的那个），已在 `note_zh` 写明冲突。

### 5. 斯坦索姆正门坐标对不上

`Stratholme_(Classic)` 页给正门坐标 `27, 8`，而 G07 的 `stratholme_main_gate` 记的是 `[30, 16]`、
侧门 `[48, 22]`。**两组都没有从 DBC 核过**（`AreaPOI` 里没有斯坦索姆入口行）。
本表没有重建入口 POI（沿用 G07 的），把分歧记在这里，**请 G07 复核一次**。

### 6. 没能给出的坐标

`AreaPOI`（Classic Era）里只有 8 个副本入口，且存的是**世界坐标**（如奥妮克希亚 `-4698.06, -3720.58`），
要转成地图百分比坐标得再拉 `UiMapAssignment` 做区域包围盒换算。**本轮没做**，
所以除了 wiki 原文里直接给出百分比坐标的 4 个（死亡矿井 `[42, 72]`、影牙城堡 `[45, 68]`、
诺莫瑞根 `[24, 40]`、血色修道院 `[85, 32]`、奥达曼 `[44, 12]`、纳克萨玛斯 `[40, 26]`、通灵学院 `[70, 73]`），
其余 `coords` **按规则留空串，没有猜**。

### 7. 黑石深渊的 boss 取舍

客户端 `DungeonEncounter` 给 map 230 共 21 行，**已全部进树**。
但 wiki 正页还列出约 30 个额外的具名精英（秩序竞技场的角斗士轮换池 Anub'shiah / Eviscerator /
Gorosh the Dervish / Grizzle / Hedrum the Creeper / Ok'thor the Breaker / Theldren、
以及 Panzor the Invincible / Watchman Doomgrip / Verek / 各 Dark Keeper）。
它们**不是独立 encounter**，已折进 `ring_of_law`（秩序竞技场）等节点的 `note_zh`，未各建节点。
如果下游真要拍黑石深渊的斗兽场戏，轮换池的英文名在此，中文名未核。

---

## ⑤ 与其它片区的对账（**合龙前必读**）

### A. 27 个 id 与别的片区重名 —— 这是**故意的**

任务书要求本片区做「全副本总表」，所以**每一座 vanilla 实例在本表里都有根节点**，
其中 27 座别的片区已经建过。处理办法：**同 `id`、同 `parent` 重新发出，字段更全**（多了人数 / 入口 / 机制 / boss 层）。

| 重名 id | 另一处在 | parent 是否一致 |
|---|---|---|
| `ragefire_chasm` | g09 | ✅ `cleft_of_shadow` |
| `wailing_caverns` | g09 | ✅ `lushwater_oasis`（已按 g09 改，原写 `the_barrens`） |
| `razorfen_kraul` | g09 | ✅ `razorfen_kraul_entrance`（已按 g09 改） |
| `razorfen_downs` | g09 | ✅ `razorfen_downs_entrance`（已按 g09 改） |
| `maraudon` | g09 | ✅ `valley_of_spears`（已按 g09 改） |
| `the_deadmines` | g02 | ✅ `defias_hideout` |
| `stormwind_stockade` | g03 | ✅ `stormwind_canals` |
| `shadowfang_keep` | g06 | ✅ `shadowfang_keep_grounds` |
| `scarlet_monastery` + `sm_graveyard` / `sm_library` / `sm_armory` / `sm_cathedral` | g06 | ✅ 五个 id 全部沿用 g06 的写法 |
| `alterac_valley` | g06 | ✅ `alterac_valley_entrance` |
| `blackfathom_deeps` | g08 | ✅ `the_zoram_strand` |
| `warsong_gulch` | g08 | ✅ `ashenvale` |
| `arathi_basin` | g07 | ✅ `arathi_highlands` |
| `scholomance` | g07 | ✅ `caer_darrow` |
| `stratholme_instance` | g07 | ✅ `stratholme_city` |
| `naxxramas` | g07 | ✅ `scourgehold` |
| `gnomeregan` | g05 | ✅ `chill_breeze_valley` |
| `uldaman` | g05 | ✅ `the_makers_terrace` |
| `blackrock_depths` / `molten_core` / `blackwing_lair` / `zul_gurub` / `temple_of_atal_hakkar` | g04 | ✅ 五个 parent 全部沿用 g04 |

**给 `tools/build_world_tree.py` 的建议：按 `id` 去重，冲突时取「非空字段更多」的那条（即本表）。**
如果生成器选择硬报错，把上表 27 行当白名单即可。**27 行的 `parent` 我已逐条对齐，不会出现同一个东西挂两个爹。**

### B. 本表**没有**重建的东西（避免重复造）

下列副本的**内部分区**别的片区已经建好，本表一律不重建，只补 boss 层：

- 死亡矿井内部 4 区（G02）· 奥达曼内部 4 厅（G05）
- 黑石深渊 20 区 / 黑石塔 12 区 / 黑翼之巢 5 区 / 熔火之心 2 区 / 祖尔格拉布 11 区 / 沉没的神庙 14 区（G04）
- 奥特兰克山谷 27 个据点（G06）· 阿拉希盆地 7 个据点（G07）
- 入口 POI：`temple_of_atal_hakkar_entrance`（G04）· `stockade_meeting_stone`（G03）·
  `stratholme_main_gate` / `stratholme_service_entrance`（G07）· `blackrock_spire_entrance`（G04）

### C. **送给别的片区的礼物：89 个英文占位名的官方简体译名**

G02 / G04 / G05 建树时拿不到 `WMOAreaTable`，所以有一批节点的 `name_zh` 直接留了英文原名。
我这轮把那张表拉下来了，**下面 89 行是客户端 zhCN 的官方写法，可以直接回填**
（出处：`https://wago.tools/db2/WMOAreaTable/csv?build=1.15.9.69722&locale=zhCN` 与同 build 的 `AreaTable`）：

| 片区 | 节点 id | 现 `name_zh` | 客户端官方简体名 |
|---|---|---|---|
| g04 | `st_the_broken_hall` | The Broken Hall | **破碎大厅** |
| g04 | `st_hall_of_masks` | Hall of Masks | **面具大厅** |
| g04 | `st_hall_of_bones` | Hall of Bones | **白骨大厅** |
| g04 | `st_hall_of_ritual` | Hall of Ritual | **仪式大厅** |
| g04 | `st_the_butchery` | The Butchery | **屠宰房** |
| g04 | `st_chamber_of_blood` | Chamber of Blood | **鲜血之厅** |
| g04 | `st_den_of_the_caller` | Den of the Caller | **召唤者之穴** |
| g04 | `st_chamber_of_the_dreamer` | Chamber of the Dreamer | **沉睡者之厅** |
| g04 | `st_lair_of_the_chosen` | Lair of the Chosen | **天选者之巢** |
| g04 | `st_the_pit_of_sacrifice` | The Pit of Sacrifice | **牺牲之池** |
| g04 | `st_the_pit_of_refuse` | The Pit of Refuse | **抛弃之池** |
| g04 | `st_sanctum_of_the_fallen_god` | Sanctum of the Fallen God | **堕神圣地** |
| g04 | `st_hall_of_serpents` | Hall of Serpents | **毒蛇大厅** |
| g04 | `st_hall_of_the_cursed` | Hall of the Cursed | **诅咒大厅** |
| g04 | `brd_halls_of_the_law` | Halls of the Law | **秩序大厅** |
| g04 | `brd_the_lyceum` | The Lyceum | **讲学厅** |
| g04 | `brd_the_imperial_seat` | The Imperial Seat | **帝王之座** |
| g04 | `brd_the_molten_bridge` | The Molten Bridge | **熔火之桥** |
| g04 | `brd_shrine_of_thaurissan` | Shrine of Thaurissan | **索瑞森神殿** |
| g04 | `brd_the_manufactory` | The Manufactory | **制造厂** |
| g04 | `brd_the_black_vault` | The Black Vault | **黑色宝库** |
| g04 | `brd_summoners_tomb` | Summoners' Tomb | **召唤者之墓** |
| g04 | `brd_chamber_of_enchantment` | Chamber of Enchantment | **魔法之厅** |
| g04 | `brd_the_iron_hall` | The Iron Hall | **钢铁大厅** |
| g04 | `brd_hall_of_crafting` | Hall of Crafting | **工艺之厅** |
| g04 | `brd_mold_foundry` | Mold Foundry | **浇铸间** |
| g04 | `brd_the_domicile` | The Domicile | **住宅区** |
| g04 | `brd_dark_iron_highway` | Dark Iron Highway | **黑铁大道** |
| g04 | `brd_east_garrison` | East Garrison | **东区兵营** |
| g04 | `brd_west_garrison` | West Garrison | **西区兵营** |
| g04 | `hordemar_city` | Hordemar City | **霍德玛尔城** |
| g04 | `skitterweb_tunnels` | Skitterweb Tunnels | **蛛网隧道** |
| g04 | `halycons_lair` | Halycon's Lair | **哈雷肯之巢** |
| g04 | `mok_doom` | Mok'Doom | **摩多姆** |
| g04 | `tazzalor` | Tazz'Alaor | **塔萨洛尔** |
| g04 | `brs_chamber_of_battle` | Chamber of Battle | **战斗之厅** |
| g04 | `brs_the_storehouse` | The Storehouse | **仓库** |
| g04 | `dragonspire_hall` | Dragonspire Hall | **龙塔大厅** |
| g04 | `the_rookery` | The Rookery | **孵化间** |
| g04 | `blackrock_stadium` | Blackrock Stadium | **黑石竞技场** |
| g04 | `brs_the_furnace` | The Furnace | **熔炉** |
| g04 | `brs_hall_of_binding` | Hall of Binding | **禁锢之厅** |
| g04 | `brs_spire_throne` | Spire Throne | **尖塔王座** |
| g04 | `bwl_dragonmaw_garrison` | Dragonmaw Garrison | **龙喉兵营** |
| g04 | `bwl_halls_of_strife` | Halls of Strife | **征战大厅** |
| g04 | `bwl_shadow_wing_lair` | Shadow Wing Lair | **影翼巢穴** |
| g04 | `mc_magmadar_cavern` | Magmadar Cavern | **玛格曼达洞穴** |
| g04 | `altar_of_hireek` | Altar of Hir'eek | **希里克祭坛** |
| g04 | `altar_of_the_blood_god` | Altar of the Blood God | **血神祭坛** |
| g04 | `the_coil` | The Coil | **毒蛇小径** |
| g04 | `the_bloodfire_pit` | The Bloodfire Pit | **血火之池** |
| g04 | `naze_of_shirvallah` | Naze of Shirvallah | **希瓦拉尔之角** |
| g04 | `pagles_pointe` | Pagle's Pointe | **帕格渔点** |
| g04 | `shadrazaar` | Shadra'zaar | **沙德拉扎尔** |
| g04 | `temple_of_bethekk` | Temple of Bethekk | **贝瑟克神庙** |
| g04 | `zanzas_rise` | Zanza's Rise | **赞扎高地** |
| g04 | `the_molten_span` | The Molten Span | **熔岩之桥** |
| g04 | `the_grinding_quarry` | The Grinding Quarry | **碾石场** |
| g04 | `the_masonary` | The Masonary | **石匠区** |
| g05 | `uldaman_dig_one` | Dig One | **一号挖掘场** |
| g05 | `uldaman_map_chamber` | Map Chamber | **地图厅** |
| g05 | `uldaman_hall_of_the_keepers` | Hall of the Keepers | **守护者大厅** |
| g05 | `uldaman_khazgoroths_seat` | Khaz'goroth's Seat | **卡兹格罗斯的王座** |
| g05 | `the_high_seat` | The High Seat | **王座厅** |
| g05 | `hall_of_mysteries` | Hall of Mysteries | **秘法大厅** |
| g05 | `the_library_ironforge` | The Library | **图书馆** |
| g05 | `tinker_town` | Tinker Town | **侏儒区** |
| g05 | `old_ironforge` | Old Ironforge | **旧铁炉堡** |

> 上表只列了与副本 / 主城直接相关的 69 行。同一批数据还能回填 G04 荆棘谷与逆风小径的 20 个野外子区域
> （`the_stockpile` 储藏室 · `tkashi_ruins` 伽什废墟 · `the_salty_sailor_tavern` 水手之家旅店 ·
> `the_old_port_authority` 港务局 · `battle_ring` 大竞技场 · `spirit_den` 灵魂之穴 · `janeiros_point` 加尼罗哨站 ·
> `the_crystal_shore` 水晶海岸 · `southern_savage_coast` 南野人海岸 · `wild_shore` 蛮荒海岸 · `south_seas` 南海 ·
> `groshgok_compound` 格罗高克营地 · `the_masters_cellar` 主宰的庇护所 · `morgans_plot` 摩根墓场 ·
> `aridens_camp` 埃瑞丁营地 · `sleeping_gorge` 沉睡峡谷 · `deadwind_ravine` 逆风谷 · `crypt_deadwind_pass` 墓穴 ·
> `slither_rock` 滑石 · `the_slag_pit` 熔渣之池 · `stonewrought_pass` 石坝小径），一并送上。

### D. 7 处译名与客户端不一致（建议按客户端改）

| 片区 | 节点 id | 现 `name_zh` | 客户端官方简体名 | 备注 |
|---|---|---|---|---|
| g04 | `shadowforge_city` | 暗影裂口城 | **暗炉城** | 黑铁矮人的都城，国服通用「暗炉城」 |
| g04 | `brd_ring_of_the_law` | 命运大厅 | **秩序竞技场** | 斗兽场那间 |
| g04 | `brd_detention_block` | 监狱区 | **禁闭室** | |
| g04 | `mc_ragnaros_lair` | 拉格纳罗斯的巢穴 | **拉格纳罗斯之巢** | 差一个字 |
| g02 | `deadmines_goblin_foundry` | 地精熔炉 | **地精锻造厂** | |
| g02 | `deadmines_mast_room` | 桅杆房 | **船桅室** | |
| g06 | `sm_grand_vestibule` | 大前厅 | **大门廊** | |

### E. `cross_group_parents`（本表引用、但不属于本片区的 parent）

26 个。其中 **22 个在别的片区已经存在**（合龙时会自动接上），
**4 个尚无归属**——`feralas`（菲拉斯）· `tanaris`（塔纳利斯）· `silithus`（希利苏斯）· `wyrmbog`（巨龙沼泽，尘泥沼泽内）。
这四个都属于**卡利姆多南部**片区（G10），该片区在我提交时还没落盘。
**G10 请务必用这四个 id**，否则厄运之槌 / 祖尔法拉克 / 安其拉两本 / 奥妮克希亚会成为孤儿节点。

---

## ⑥ 地图图片链接清单（**只记 URL 与版权状态，未下载**）

仓库已裁定「暴雪美术资产只进人眼、不入画、不上传给生成模型」，故**一张都没下载**，只记路径。

| 类别 | 位置 | 版权状态 |
|---|---|---|
| 每个副本的**内部平面图**（`Deadmines map.jpg` 之类） | 嵌在对应的 `warcraft.wiki.gg` 条目页内，页内 `File:` 链接 | 暴雪美术资产（游戏内截图 / 客户端素材）。**仅供人眼参考，不得入画、不得喂生成模型** |
| 每个副本的**载入画面**（`{{Infobox instance|ss=}}` 字段指向，如 `The Deadmines loading screen.jpg`） | 同上 | 同上 |
| 战场全图（战歌峡谷 / 阿拉希盆地 / 奥特兰克山谷） | 对应战场条目页 | 同上 |
| 客户端原始地图贴图（`Interface/WorldMap/...`、`DungeonMaps`） | 需自行从客户端 MPQ/CASC 提取 | 同上，**且提取行为本身请先确认合规** |

**没有验证任何单张图片的直链**——本轮抓的是 `?action=raw`（wikitext），
里面的 `File:` 只是文件名而不是可直接取的 URL，硬拼直链会得到一个未经核实的地址，按纪律不写。
下游真要看图，从上表的条目页点进去即可。

---

## ⑦ 给下游的提醒

1. **要「按顺序列 boss」直接按 YAML 里的出现顺序读**，那就是客户端 `DungeonEncounter.OrderIndex` 的官方排序，
   `note_zh` 的「第 N 场」也是同一个 N。不要另行排序。
2. **`look_zh` 是为分镜选景写的，是我写的画面描述，不是引文。** 每条都给了色调 + 地貌 + 标志物三要素。
   `source_url` / `quote` 只为 `name_zh` / `name_en` / `level` / 入口位置这些**事实字段**背书，不为 `look_zh` 背书。
3. **写练级剧本时，等级带用 § ⑧ 的推进表**，别直接拿 `level` 字段当"主角必须几级"——
   `level` 是怪物等级带，客户端准入带比它宽得多（比如 35 级就能进死亡矿井）。
4. **21 个英文名节点不是漏了，是按规则留的。** 真要中文，去正式服 build 的 `JournalEncounter` zhCN 捞，
   纳克萨玛斯五个分区同理（§ ④.2）。
5. **别把 wiki 正页的 boss 表当旧世用。** 死亡矿井 / 影牙城堡 / 怒焰裂谷 / 血色修道院 / 祖尔格拉布 /
   纳克萨玛斯 / 黑石塔上层 / 厄运之槌八个本的正页全是改版后的内容（§ ③A）。
6. **黑石山是一座「嵌套三层」的地方**：`blackrock_mountain`（外部，G04）→ 内含
   `blackrock_depths`（本表）/ `blackrock_spire`（G04）→ 后者再分 `lower_blackrock_spire` 与
   `upper_blackrock_spire`（本表），熔火之心挂在山上、黑翼之巢挂在塔上。
   拍黑石山的戏时这四层要分清，不要当成一个"副本"。
7. **血色修道院与厄运之槌在游戏里是「一栋建筑、多个独立副本」**：
   走进同一个大门廊 / 同一片废城，再选不同的门进不同的翼，每翼是一个独立的实例。
   树里的结构（`scarlet_monastery` → 四翼 `dungeon` 子节点）就是照这个建的。
8. 三个战场的据点节点在 G06（奥山 27 个）与 G07（阿拉希 7 个）里，**战歌峡谷的两个基地在本表**
   （`wsg_silverwing_hold` 银翼要塞 / `wsg_warsong_lumber_mill` 战歌伐木场）。

---

## ⑧ 副本推进表（主角从 15 级打到 60 级，依次会打哪些本）

`level` = wiki classiclevel（怪物等级带）· `准入` = 客户端 `LFGDungeons` 的 Min-Max ·
`人数` = 客户端 `Map.MaxPlayers`（括号里是设计人数）

### 第一程 · 15 → 30

| # | 副本 | 等级带 | 准入 | 人数 | 阵营 | 入口在哪 |
|---|---|---|---|---|---|---|
| 1 | **怒焰裂谷** | 15-21 | 13-22 | 10(5) | 部落 | 奥格瑞玛·暗影裂谷（城内，部落专属的第一个本） |
| 2 | **死亡矿井** | 15-23 | 15-28 | 10(5) | 联盟向 | 西部荒野·月溪镇地下 `[42, 72]` |
| 3 | **哀嚎洞穴** | 17-24 | 15-28 | 10(5) | 中立 | 贫瘠之地·甜水绿洲北岸 |
| 4 | **影牙城堡** | 18-24 | 18-32 | 10(5) | 中立（部落向） | 银松森林南部高崖 `[45, 68]` |
| 5 | **暴风城监狱** | 22-30 | 22-34 | 10(5) | 联盟 | 暴风城·运河区（城内） |
| 6 | **黑暗深渊** | 24-32 | 20-34 | 10(5) | 中立 | 灰谷·佐拉姆海岸海底洞口 |

### 第二程 · 26 → 47（血色修道院是这一段的主力）

| # | 副本 | 等级带 | 准入 | 人数 | 入口在哪 |
|---|---|---|---|---|---|
| 7 | **血色修道院·墓地** | 26-36 | 29-48 | 10(5) | 提瑞斯法林地·耳语花园 `[85, 32]`，进大门廊后选门 |
| 8 | **诺莫瑞根** | 24-40 | 24-40 | 10(5) | 丹莫罗·寒风谷 `[24, 40]` |
| 9 | **剃刀沼泽** | 29-38 | 24-40 | 10(5) | 贫瘠之地南部·刺藤拱门 |
| 10 | **血色修道院·图书馆** | 29-39 | 29-48 | 10(5) | 同 7 |
| 11 | **血色修道院·军械库** | 32-42 | 29-48 | 10(5) | 同 7（最短的一翼，速刷点） |
| 12 | **血色修道院·大教堂** | 35-45 | 29-48 | 10(5) | 同 7（四翼最高） |
| 13 | **剃刀高地** | 37-46 | 33-47 | 10(5) | 贫瘠之地南部，剃刀沼泽以南 |

### 第三程 · 42 → 55

| # | 副本 | 等级带 | 准入 | 人数 | 入口在哪 |
|---|---|---|---|---|---|
| 14 | **奥达曼** | 42-52 | 38-53 | 10(5) | 荒芜之地·造物者遗迹 `[44, 12]`（另有艾卡默克洞穴后门） |
| 15 | **祖尔法拉克** | 44-54 | 43-54 | 10(5) | 塔纳利斯西北·流沙岗哨附近 |
| 16 | **玛拉顿** | 45-52 | 40-58 | 10(5) | 凄凉之地·长矛谷（橙晶 / 紫晶 / 地歌瀑布三个口） |
| 17 | **沉没的神庙** | 50-60 | 44-60 | **20**(5) | 悲伤沼泽·泪水之池湖心（要潜水） |

### 第四程 · 52 → 60（满级前的装备本）

| # | 副本 | 等级带 | 准入 | 人数 | 入口在哪 |
|---|---|---|---|---|---|
| 18 | **黑石深渊** | 52-60 | 48-60 | **5** | 黑石山内部下层（体量最大，一圈数小时） |
| 19 | **黑石塔下层** | 55-60 | 52-60 | 10 | 黑石塔正门后走左路 |
| 20 | **厄运之槌 - 东** | 54-60 | 54-60 | **5** | 菲拉斯·高地荒野（三翼各有独立入口） |
| 21 | **通灵学院** | 55-60 | 56-60 | **5** | 西瘟疫之地·凯尔达隆岛 `[70, 73]`（需钥匙） |
| 22 | **厄运之槌 - 西** | 56-60 | 56-60 | **5** | 同 20 |
| 23 | **厄运之槌 - 北** | 56-60 | 56-60 | **5** | 同 20（可走「贡品跑」） |
| 24 | **斯坦索姆** | 56-61 | 56-60 | **5** | 东瘟疫之地·病木林（正门＝活人侧 / 侧门＝亡灵侧，侧门需城市之匙） |
| 25 | **黑石塔上层** | 56-61 | 56-60 | 10 | 黑石塔正门后走右路（需黑石塔钥匙） |

### 第五程 · 60 级团本（按旧世开放顺序 / 难度阶梯）

| # | 团本 | 人数 | 上线补丁 | 入口在哪 |
|---|---|---|---|---|
| 26 | **奥妮克希亚的巢穴** | 40 | 1.0 | 尘泥沼泽·巨龙沼泽（需完成深渊项链任务链） |
| 27 | **熔火之心** | 40 | 1.0 | 黑石深渊最底部（需「核心通道」任务） |
| 28 | **黑翼之巢** | 40 | 1.6 | 黑石塔上层内侧，用命令宝珠进 |
| 29 | **祖尔格拉布** | **20** | 1.7 | 荆棘谷东北·祖尔格拉布城门（三天一刷） |
| 30 | **安其拉废墟（AQ20）** | **20** | 1.9 | 希利苏斯南端·安其拉之门内走左路 |
| 31 | **安其拉神殿（AQ40）** | 40 | 1.9 | 希利苏斯南端·穿甲虫之墙后走右路 |
| 32 | **纳克萨玛斯** | 40 | **1.11** | 东瘟疫之地·病木林传送尖塔 `[40, 26]`（需银色黎明声望 + 钥匙）—— 旧世的终点 |

### 战场（随时可打，与副本并行）

| 战场 | 人数 | 等级分段 | 玩法 | 入口 |
|---|---|---|---|---|
| **战歌峡谷** | 10 v 10 | 10-19 / 20-29 / … / 60 | 夺旗，先夺 3 次或 20 分钟内夺得多者胜；己方旗必须在基地才能得分 | 灰谷·银翼树林（联盟）/ 贫瘠之地·莫尔杉营地（部落） |
| **阿拉希盆地** | 15 v 15 | 20-29 / … / 60（客户端准入记 30-60） | 资源战，占农场·兽栏·铁匠铺·伐木场·矿洞五点，先满 1500 资源者胜 | 阿拉希高地·避难谷地（联盟）/ 落锤镇（部落） |
| **奥特兰克山谷** | 40 v 40 | 51-60 | 消耗战，双方各 700 点增援；打掉对方将军（范达尔·雷矛 / 德雷克塔尔）直接清零。沿途争夺碉堡·墓地·矿洞，可召唤 NPC 援军 | 希尔斯布莱德丘陵北端（南海镇以北 / 塔伦米尔东北） |

**给剧本的一句话总结**：主角 15 级下第一个本（部落进怒焰裂谷、联盟进死亡矿井），
26-45 级基本泡在血色修道院四翼，50 级前后转战奥达曼 / 祖尔法拉克 / 玛拉顿，
55 级起黑石山与厄运之槌是主场，60 级毕业本是斯坦索姆与黑石塔上层，
然后按 **奥妮克希亚 → 熔火之心 → 黑翼之巢 → 祖尔格拉布 → 安其拉 → 纳克萨玛斯** 的顺序走完团本线。

---

## 核验记录（G11-V）

> 独立核验员的复核记录。默认立场是**怀疑每一个地名**；下面每一条结论都有可复现的取证动作。
> 本节**只记复核过程与改动**，树数据仍以 `g11_instances.yaml` 为唯一出处。
> 结论：**已修订可用**。节点 404 → **409**。

### V-① 复核口径：把「读页判断」换成「机检对账」

作者留下的最有价值的一条路是 `wago.tools` 的 Classic Era DBC。核验员把同一批表重新拉了一遍
（`Map` / `AreaTable` / `LFGDungeons` / `WMOAreaTable` / `DungeonEncounter`，build `1.15.9.69722`，enUS + zhCN），
然后写脚本做了三道**全量**机检，而不是抽样读：

| 机检 | 做法 | 结果 |
|---|---|---|
| **译名对账** | 全部 404 个节点的 `name_en` 去 5 张表里查，命中的就比对 `name_zh` 是否等于该行 zhCN | **0 处不符**。作者「一个字都没有自己音译」的自评属实 |
| **英文名存在性** | 5 张表全不命中的节点挑出来逐个人工追 wiki | 43 个，全部落在作者 § ④.1 声明的 21 个 B 档、构造式入口名、或副本翼名上，**没有一个是凭空编的地名** |
| **子区域完整性** | 按 `WMOID` / `AreaTable.ContinentID` 把每座副本的官方内部分区全列出来，与树里的 `subzone` 做差集 | **查到 4 个漏项**，见 V-④ |

**这三道机检是本次复核的主结论来源**：它把「作者有没有编地名」从主观判断变成了集合运算。
凡是 DBC 命中的节点，其 `name_zh` / `name_en` 一律可视为已核。

### V-② 逐 zone 复核结果（30 个 zone）

| zone | 子区域完整性 | 等级带 | 阵营/归属 | 结论 |
|---|---|---|---|---|
| ragefire_chasm | 无内部分区（DBC 无） | 15-21 ✅ | horde ✅ | ✅ |
| wailing_caverns | 6/6 ✅（wiki Subregions 与 WMOID 1143+1069 一致） | 17-24 ✅ | contested ✅ | ⚠️ 出处 URL 404，已改 |
| the_deadmines | 内部 4 区归 G02（已核实 G02 真有 4 个） | 15-23 ✅ | alliance ✅ | ✅ |
| shadowfang_keep | wiki 无 Subzones 节，DBC 只有根 ✅ | 18-24 ✅ | contested ✅ | ✅ |
| blackfathom_deeps | 6/6 ✅ | 24-32 ✅ | contested ✅ | ⚠️ 漏 1 个 boss，已补 |
| stormwind_stockade | wiki/DBC 均无内部分区 ✅ | 22-30 ✅ | alliance ✅ | ✅ |
| gnomeregan | 7/7 ✅ | **24-40 ❌ → 29-38** | alliance ✅ | ⚠️ 已改 |
| razorfen_kraul | DBC 只有根 ✅ | 29-38 ✅ | contested ✅ | ✅ |
| scarlet_monastery（含四翼） | 墓地 3/3 · 图书馆 3/3 · 军械库 4/4 ✅；**大教堂 0/2 ❌** | 26-36 / 29-39 / 32-42 / 35-45 全 ✅ | contested ✅ | ⚠️ 补 2 个 |
| razorfen_downs | 4/4 ✅ | 37-46 ✅ | contested ✅ | ✅ |
| uldaman | 内部分区归 G05 | 42-52 ✅ | contested ✅ | ✅（但 G05 只建了 4 个，见 V-⑦） |
| zul_farrak | DBC 只有根 ✅ | 44-54 ✅ | contested ✅ | ✅ |
| maraudon | 10/10 ✅（7 个实例内 + 3 个前置洞窟） | 45-52 ✅ | contested ✅ | ⚠️ 3 个 id 与 G09 撞，已统一 |
| temple_of_atal_hakkar | 内部 14 区归 G04（已核实 G04 真有 14 个，与 `_(Classic)` 页逐一对上） | 50-60 ✅ | contested ✅ | ✅ |
| blackrock_depths | 内部区归 G04（G04 有 21 个，wiki 列 20 个） | 52-60 ✅ | contested ✅ | ✅ |
| lower/upper_blackrock_spire | 内部区归 G04 | 55-60 / 56-61 ✅ | contested ✅ | ✅（但 G04 挂在 `blackrock_spire` 而非上下层，见 V-⑦） |
| dire_maul（含三翼） | **11/13 ❌**（漏 `Eldreth Row` / `Broken Commons`）；另有 1 处挂错 | 见 V-⑦.5 口径说明 | contested ✅ | ⚠️ 补 2 个 + 改挂 1 个 |
| stratholme_instance | 16/16 ✅（比 wiki 列的 13 个还多 3 座通灵塔，DBC 有） | 56-61 ✅ | contested ✅ | ✅ |
| scholomance | 14/14 ✅（比 wiki 列的 12 个多 2 个，DBC 有） | 55-60 ✅ | contested ✅ | ✅ |
| onyxias_lair | 无内部分区 ✅ | 60 ✅ | contested ✅ | ✅ |
| molten_core | 内部 2 区归 G04 ✅ | 60 ✅ | contested ✅ | ✅ |
| blackwing_lair | 内部 5 区归 G04 ✅ | 60 ✅ | contested ✅ | ✅ |
| zul_gurub | 内部 11 区归 G04 ✅ | 58-60 ✅ | contested ✅ | ✅ |
| ruins_of_ahnqiraj | 6/6 ✅（＝ `AreaTable` 全部子区） | 60 ✅ | contested ✅ | ✅ |
| temple_of_ahnqiraj | DBC 无内部分区；wiki 的「temple gates / hive undergrounds / vault of C'Thun」只是**地图图注**、不是地名 ✅ | 60 ✅ | contested ✅ | ✅（未补，理由见 V-⑥.3） |
| naxxramas | 7 个（5 个分区 + 2 个 DBC 有名的厅）✅ | 60 ✅ | contested ✅ | ⚠️ 入口坐标错，已改 |
| warsong_gulch | 2/2 ✅ | 10-60 ✅ | pvp ✅ | ✅ |
| arathi_basin | 7 个据点归 G07（已核实 G07 真有 7 个） | 20-60 ✅ | pvp ✅ | ✅ |
| alterac_valley | 26 个据点归 G06（已核实 G06 真有 26 个，＝ `AreaTable` 全部子区） | 51-60 ✅ | pvp ✅ | ✅ |

### V-③ 改了什么（8 处）

**A. 等级带错 1 处**

- `gnomeregan` `level: 24-40` → **`29-38`**。
  24-40 是客户端 `LFGDungeons`（ID 13）的**准入带**，不是等级带；
  `Gnomeregan_(instance)` 的信息框写死 `|classiclevel=29-38`。
  作者自己在 § ②A 定的规矩就是「`level` 取 wiki classiclevel、准入带写进 `note_zh`」，
  这一条是**违反了自己的规矩**（`note_zh` 里「客户端准入带 24-40」本来就写对了）。
  § ③A 的对照表同步改成「29-38（准入 24-40）」。

**B. 坐标错 1 处**

- `naxxramas` `coords: [40, 26]` → **`[39, 26]`**。
  这条是**自相矛盾**：同一个节点的 `note_zh` 与 `quote` 都写 39,26，只有 `coords` 写 40,26。
  `Naxxramas_(Classic)` 的 wikitext 原文是 `{{Coords|39|26|Eastern Plaguelands}}`。
  `quote` 同时改成该句原文（原 `quote` 是转述，不是页面上的字）。

**C. 出处 URL 失效 2 处（无出处）**

- `wailing_caverns` / `deviate_faerie_dragon` 的 `source_url` 指向
  `https://warcraft.wiki.gg/wiki/Wailing_Caverns_(Classic)` —— 该页 **HTTP 404**（`action=raw` 返回 0 字节）。
  作者 § ①B 列了一串 404 清单，这一条漏记了。
  两节点改指 `https://warcraft.wiki.gg/wiki/Wailing_Caverns`（HTTP 200）。
  **原 `quote` 是真的**——「The Wailing Caverns is in the Northern Barrens, to the south of Crossroads,
  on the north side of the Lushwater Oasis.」在新页第 17 行逐字存在，所以只换 URL、不动引文。

**D. id 不一致 3 处（同一个地方两个 id）**

作者 § ⑤A 立的规矩是「别的片区已有的节点，同 `id` 同 `parent` 重新发出」，
但玛拉顿的内部分区没走这条规矩——G09 已经建了 3 个，G11 又用长前缀建了一遍：

| G09 已有 | G11 原写法 | 已统一为 |
|---|---|---|
| `wicked_grotto` | `maraudon_the_wicked_grotto` | **`wicked_grotto`** |
| `foulspore_cavern` | `maraudon_foulspore_cavern` | **`foulspore_cavern`** |
| `earth_song_falls` | `maraudon_earth_song_falls` | **`earth_song_falls`** |

不改的话，`build_world_tree.py` 会让玛拉顿长出 6 个子节点来表示 3 个房间。
**其余 7 个玛拉顿子区域（G09 没有的）保留 G11 的 `maraudon_` 前缀，不动。**
统一后全仓 id 碰撞 30 处，`parent` 100% 一致，0 处父节点冲突（机检过）。

> 顺带给 G09：这三个节点的 `name_zh` 请按客户端改——
> `foulspore_cavern` 现写「污臭洞穴」，客户端是 **毒菇洞穴**；
> `earth_song_falls` 现写「大地之歌瀑布」，客户端是 **地歌瀑布**；
> `wicked_grotto` 的「邪恶洞穴」是对的。（本表用的就是客户端写法，合龙时以本表为准。）

**E. 层级挂错 1 处**

- `dm_the_hidden_reach` 原挂在 `dire_maul` 根下（当成三翼共用的外圈区）。
  `Hidden_Reach` 条目原文：「The Hidden Reach is the name given to a **secret entrance to Dire Maul East**
  which bypasses the usual hazards of getting into the keep from its usual entrance.」
  —— 它是**东翼专属**的侧门，已改挂 `dire_maul_east`，`look_zh`（原写「直通北翼后方」）与 `note_zh` 同步改。

**F. 引文方位错 3 处**

- 三个玛拉顿入口 POI 的 `quote` 写的是「Portal from western / southern / eastern area」，
  其中「western」与 wiki 原文相反。`Maraudon` 页原文是：
  「Heading **north** leads to the upper Wicked Tunnels and the portal to the Wicked Grotto,
  heading **east** through Earth Song Gate leads to the lower Wicked Tunnels and the portal to Earth Song Falls,
  and heading **south** leads to the Foulspore Pools and the portal to Foulspore Cavern.」
  三条 `quote` 全部换成该句的对应分句（`name_zh` / `note_zh` 都是对的，没动）。

### V-④ 补了 5 个节点（漏 4 个子区域 + 漏 1 个 boss）

| 新 id | 名字 | 挂在 | 取证 |
|---|---|---|---|
| `dm_eldreth_row` | 艾德雷斯区 · Eldreth Row | `dire_maul` | `WMOAreaTable` WMOID **3633**（厄运之槌外圈那颗 WMO）；`Eldreth_Row` 条目：「the outermost area of Dire Maul, located **outside the instance portals** and before the Broken Commons」 |
| `dm_broken_commons` | 平民区废墟 · Broken Commons | `dire_maul` | 同 WMOID 3633；`Broken_Commons` 条目：「This is where each quarter entrance can be found: To the east Warpwood Quarter, to the west Capital Gardens, and to the north Gordok Commons. In the center is The Maul」 |
| `sm_chapel_gardens` | 教堂花园 · Chapel Gardens | `sm_cathedral` | `WMOAreaTable` WMOID **1630**（＝大教堂那颗 WMO，组里只有这两个名字）；`Scarlet_Monastery_Cathedral` 的 Subzones 节也列了它 |
| `sm_crusaders_chapel` | 十字军礼拜堂 · Crusader's Chapel | `sm_cathedral` | 同 WMOID 1630；同页 Subzones 节 |
| `lorgus_jett` | 洛古斯·杰特 · Lorgus Jett | `blackfathom_deeps` | 见下 |

**为什么大教堂这两个是硬漏项**：墓地 / 图书馆 / 军械库三翼的内部分区作者都建了（3+3+4），
唯独大教堂一个都没建。DBC 里大教堂的 WMO（1630）**只有这两行**，wiki 的 Subzones 节也**只列这两个**
（外加三翼共用的「大门廊」，那个在 G06 的 `sm_grand_vestibule`）。所以不是「大教堂本来就没有分区」，是漏了。

**为什么 `Eldreth Row` / `Broken Commons` 是硬漏项**：作者把厄运之槌 WMOID **3634**（实例内那颗）
的 12 个名字全建了（11 个分区 + 根），但漏了 WMOID **3633**（外圈那颗）的 2 个。
这两处是**走进三翼传送门之前**的公共区域，正是「主角走进废城、还没选门」这场戏的取景地——
对下游选景来说恰恰是最常用的一块。

**`lorgus_jett`：推翻作者的一条剔除判断。**
作者 § ③B 把他列为「SoD 增补，未进树」。复核查到三条反证：
① `Blackfathom_Deeps_(Classic)` 的 Encounters 表里，他在 **Bosses 列**（「Tunnels」一行），
   与加摩拉 / 萨利维丝 / 格里哈斯特 / 阿奎尼斯男爵并列，不在 Mobs 列；
② 他本人的条目写「The subject of this article was **removed in patch 6.0.2** but remains in World of Warcraft: Classic」
   —— 6.0.2 是德拉诺之王，远在 SoD 之前；
③ 该条目的 Patch history 有一行 4.0.3a「Level reduced from 26 to 25. Now Rare instead of Elite」
   —— 大地裂变都还能给他改数值，说明旧世本来就有他。
按作者自己给稀有精英的写法（附在该本末尾、`note_zh` 以「第 N 场 · 稀有精英」开头，不重排前面的场次号），
补为**第 8 场**。中文名 `洛古斯·杰特` 直接取自 Classic Era `DungeonEncounter` zhCN，属 A 档。
**作者判为 SoD 变体的「整组负 `OrderIndex` 重复行」仍然不进树——那个判断是对的。**

### V-⑤ 复核后的节点数对账

| | 原 | 现 |
|---|---|---|
| 副本根（dungeon 27 + raid 7 + battleground 3） | 37 | 37 |
| 内部分区 `subzone` | 99 | **103**（+2 厄运之槌外圈，+2 大教堂） |
| boss 与地标 `poi` | 268 | **269**（+洛古斯·杰特） |
| **合计** | **404** | **409** |

机检：id 无重复；`parent` 全部可解析（26 个 `cross_group_parents` 与作者 § ⑤E 一致，未新增）；
全量译名对账重跑一遍仍 **0 处不符**；跨片区 id 碰撞 30 处、`parent` 冲突 **0**。

### V-⑥ 复核确认「作者是对的」的几处（别再来回改）

1. **`Zelemar the Wrathful` 不进树是对的，且已从「存疑」升级为「已核实」。**
   `Ragefire_Chasm_(Classic)` 的 Patch history 里有一行 `{{Patch 2.0.3|note= Zelemar the Wrathful added.}}`。
   2.0.3 是燃烧的远征前置补丁，1.12 没有他。§ ④.3 已就地结案。
2. **诺莫瑞根的 `Train Depot 地铁站` / `Loading Room 装载室` / `Workshop Entrance 车间入口` 不进本表是对的。**
   它们在 `WMOAreaTable` 的 **WMOID 1220**，其 `AreaTableID` 指向 `AreaTable 133`（丹莫罗的诺莫瑞根外部），
   **不是实例内的 `AreaTable 721`**。wiki 的城市条目把内外混在一个列表里，容易误抄。
   → 这三个属于 **G05**，请 G05 挂到诺莫瑞根外围。
3. **安其拉神殿（AQ40）没有子区域节点是对的。** wiki 上的「the temple gates / the hive undergrounds /
   the vault of C'Thun」是 Geography 一节**三张地图截图的图注**（`File:VZ-Temple of Ahn'Qiraj-s1.jpg|The hive undergrounds.`），
   不是 Subzones 列表；`AreaTable` / `WMOAreaTable` 里也查无此名。按「宁可不收存疑的」不补。
4. **安其拉废墟的 20 人是对的，别按 wiki 改成 10 人。** wiki 信息框的 `|players=10` 是大地裂变之后的数；
   Classic Era `Map` 表（ID 509）`MaxPlayers=20`。
5. **祖尔法拉克取「祖尔法拉克」而不是 `LFGDungeons` 的「祖尔法兰克」是对的**（§ ④.4 的判断复核通过）。
6. **斯坦索姆 16 个分区、通灵学院 14 个分区比 wiki 列的还多**，多出来的（三座通灵塔 / 诗歌之厅 / 沉没的墓穴）
   在 `WMOAreaTable` 里都查得到，是 wiki 漏了，不是作者多写。
7. **玛拉顿那 3 个「前置洞窟」节点（五可汗神殿 / 琥珀碎片洞穴 / 暗影碎片洞穴）挂在 `maraudon` 下是对的。**
   它们在 WMOID **1376**（实例外那颗 WMO），是走进三个传送门之前的公共洞窟，属于「玛拉顿」这个地方。
8. **334 个 `wago.tools` 出处的 `quote` 写成「英文名 ＝ 中文名」的行摘要，不是逐字引文** ——
   形式上不合「逐字」，但核验员把这 334 行**全量**回查了 CSV，**0 处不符**，
   故**不降级为 `ai_draft`**；这种「行引用」对 DBC 类结构化出处是可接受且可机检的写法。
9. **69 个 wiki 出处的 `quote` 多数是信息框字段摘要**（`Location: …; Level …; Players …`）。
   逐条回查了 `?action=raw` 的信息框原文，**除本节 V-③B/F 点名的 4 条外全部属实**，同样不降级。

### V-⑦ 仍存疑 / 交给别的片区

1. **纳克萨玛斯五个分区仍是英文名。** 复核确认 Classic Era 的 `AreaTable` / `WMOAreaTable` 里
   **确实一行都没有**（只有 `Sapphiron's Lair 冰霜巨龙的大厅` 与 `Kel'Thuzad Chamber 克尔苏加德的大厅` 在 WMOID 4491）。
   英文名本身已在 `Naxxramas_(Classic)` 页核到。作者 § ④.2 给的补法（拉正式服 build 的 `JournalEncounter` zhCN）仍然是正解。
2. **`uldaman` 的内部分区 G05 只建了 4 个，wiki 列了 10 个**
   （`Chamber of Khaz'mul` · `Dig Two` · `Dig Three` · `Echomok Cavern` · `Hall of the Crafters` · `Hall of the Keepers` ·
   `Khaz'goroth's Seat` · `Map Chamber` · `The Stone Vault` · `Temple Hall`，另有 5 个在实例外）。
   本表按 § ⑤B 不重建，**请 G05 补齐**。
3. **G04 把黑石塔的内部分区挂在 `blackrock_spire` 上，而不是 `lower_blackrock_spire` / `upper_blackrock_spire`。**
   本表新建了上下层两个根节点，于是同一座塔出现了两级并行的挂法
   （`hordemar_city` 属下层；`dragonspire_hall` / `the_rookery` / `blackrock_stadium` 属上层）。
   合龙前请 G04 决定改挂到哪一层；**本表不动 G04 的节点**。
4. **`temple_of_atal_hakkar` 的 `source_url` 指的是正式服正页**（`Temple_of_Atal'Hakkar`，会跳到 retail 版）。
   该页的 `classiclevel=50-60` 与本表一致，故未改；
   但更稳的出处是 `Temple_of_Atal'Hakkar_(Classic)`（已验证 200，同样 50-60、14 个分区）。下次重生时换掉。
5. **厄运之槌三翼的 `level` 用的是客户端准入带（54-60 / 56-60 / 56-60），不是 wiki classiclevel。**
   三翼的 wiki `classiclevel` 一律是 `55-60`（不分翼）。**没有改**——
   准入带分翼、信息量更大，且与 § ⑧ 推进表自洽；这里记一笔口径偏差，下游若要严格按 § ②A 的定义读 `level`，
   厄运之槌是唯一的例外。（`scarlet_monastery` 根节点的 `29-48` 同理，是四翼合起来的准入带。）
6. **斯坦索姆正门坐标分歧（作者 § ④.5）未解。** 复核也没在 `AreaPOI` 里找到斯坦索姆入口行，
   两组坐标（wiki `27,8` / G07 `30,16`）都无 DBC 背书。仍请 G07 复核。

### V-⑧ 实际抓到的页面清单（本轮复核自己跑的，不是抄作者的）

**DBC（`wago.tools`，build `1.15.9.69722`，enUS + zhCN 各一份，全部 200）**
`Map`（8.0K / 7.7K）· `AreaTable`（127K / 123K）· `LFGDungeons`（6.7K / 6.7K）·
`WMOAreaTable`（554K / 544K）· `DungeonEncounter`（14.3K / 14.4K）

**`warcraft.wiki.gg`（以 `?action=raw` 为主，逐页落盘后再 grep，不靠摘要）**

| 结果 | 页面 |
|---|---|
| **200** | `Ragefire_Chasm_(Classic)` · `Wailing_Caverns` · `Deadmines` · `Deadmines_(Classic)` · `Shadowfang_Keep_(Classic)` · `Blackfathom_Deeps_(Classic)` · `Stormwind_Stockade_(Classic)` · `Gnomeregan` · `Gnomeregan_(instance)` · `Razorfen_Kraul_(Classic)` · `Razorfen_Downs_(Classic)` · `Uldaman` · `Zul'Farrak` · `Maraudon` · `Temple_of_Atal'Hakkar` · `Temple_of_Atal'Hakkar_(Classic)` · `Blackrock_Depths` · `Lower_Blackrock_Spire` · `Upper_Blackrock_Spire_(Classic)` · `Dire_Maul` · `Dire_Maul_West` · `Warpwood_Quarter` · `Capital_Gardens` · `Gordok_Commons` · `Eldreth_Row` · `Broken_Commons` · `Hidden_Reach` · `Lorgus_Jett` · `Stratholme_(Classic)` · `Scholomance_(Classic)` · `Onyxia's_Lair_(Classic)` · `Molten_Core` · `Blackwing_Lair` · `Zul'Gurub_(Classic)` · `Ruins_of_Ahn'Qiraj` · `Temple_of_Ahn'Qiraj` · `Naxxramas_(Classic)` · `Warsong_Gulch` · `Arathi_Basin` · `Alterac_Valley` · `Scarlet_Monastery` · `Scarlet_Monastery_Graveyard` · `Scarlet_Monastery_Library` · `Scarlet_Monastery_Armory` · `Scarlet_Monastery_Cathedral` |
| **404** | `Wailing_Caverns_(Classic)`（作者引了它，已改指 `Wailing_Caverns`） |
| **403** | `wow.huijiwiki.com`（换 UA 重试仍是 Cloudflare 拦截，与作者记录一致）。**不影响结论**：本片区的中文名 100% 出自客户端 zhCN DBC，比灰机更上游 |

**复核纪律**：`WebFetch` 的摘要模型在 `Gnomeregan_(instance)` 上把 `classiclevel` 读串过一次
（吐出 `29-38` 与 `10-30` 两个互斥的数）。**凡要落进 YAML 的数字，一律以 `?action=raw` 的
wikitext 原文为准，不采信摘要。** 本节所有等级带、坐标、子区域列表都是这么取的。
