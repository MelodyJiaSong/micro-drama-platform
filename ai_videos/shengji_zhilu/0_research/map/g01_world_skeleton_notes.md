---
worker_id: g01-world-skeleton
stage: 0
role: researcher
angle: wow-map-tree-g01
status: complete
blockers: []
confidence: high
---

# G01 · 世界与大陆骨架 —— 备注（非树数据）

**版本锚点：经典旧世 Vanilla / Classic Era（1.12）。**
树数据全部在 `g01_world_skeleton.yaml`，本文件**一个节点字段都不重复**（仓库规则「一份东西只有一个出处，副本必漂」）。
本文件只放：① 自查对账 ② 版本差异 ③ 存疑与未查 ④ 地图图片链接 ⑤ 全局图例 + zone 总表 + 给下游的提醒。

---

## ① 自查对账

### 真的抓下来读过的页（`verified_by: ai_read` 的依据）

全部用 `curl "https://warcraft.wiki.gg/index.php?title=X&action=raw"` 取的**维基原文**（不是渲染页、不是搜索摘要）：

| 页 | 字节 | 用途 |
|---|---:|---|
| `Azeroth` | 57 549 | 世界定义、四大陆、四海方位、大分裂 |
| `Eastern_Kingdoms` | 16 544 | 「三个、有时四个次大陆」的原话 + 全 zone 清单 + 主城归属 |
| `Kalimdor` | 15 510 | 北/中/南三分区的原话 + zone 清单 |
| `Azeroth_(continent)` | 8 245 | 南部次大陆 zone 清单、与卡兹莫丹的通路 |
| `Khaz_Modan` | 8 112 | 中部次大陆 zone 清单、名字词源 |
| `Lordaeron`（`Lordaeron_(continent)` 重定向至此） | 11 494 | 北部次大陆 zone 清单、南北端点 |
| `Quel'Thalas` | 19 366 | **vanilla 不可进**的原文证据 |
| `Stormwind_(kingdom)`（`Kingdom_of_Stormwind` 重定向至此） | 110 848 | 暴风王国逐 zone 领地表、「亦称艾泽拉斯王国」 |
| `Stranglethorn_Vale` | 22 141 | 荆棘谷分区 |
| `Ruins_of_Gilneas` / `Gilneas_(kingdom)` / `Greymane_Wall` | 43 507 / 94 101 / 13 450 | **vanilla 只有城墙**的原文证据 |
| `Northern/Central/Southern_Kalimdor` | 5 681 / 5 031 / 5 074 | 三分区定义与各自 zone 清单 |
| `Great_Sea` / `Maelstrom` / `Veiled_Sea` / `Forbidding_Sea` / `South_Seas` | 18 248 / 15 577 / 3 597 / 3 027 / 9 843 | 五片水体的定义与方位 |
| `Outland` / `Northrend` / `Pandaria` / `Broken_Isles` / `Zandalar` / `Kul_Tiras` | 36 816 / 46 538 / 29 269 / 33 822 / 15 307 / 17 451 | 非 vanilla 大陆各一句定义 |
| **`Classic_zones`** | 11 412 | **本路最重要的一页**——vanilla 全 zone 的等级带 + PvP 状态 + 主城镇 + 副本，下面 §⑤ 的总表逐行出自它 |
| `Zones_by_level` / `Zone` | 11 602 / 44 447 | 交叉印证 |

中文侧真的抓到的页：

| 页 | 拿到什么 |
|---|---|
| `zh.wikipedia.org/wiki/魔兽系列地名列表` | 东部王国 / 卡利姆多 / 洛丹伦 / 卡兹莫丹 / 艾泽拉斯（次大陆）/ 奎尔萨拉斯 / 吉尔尼斯 / 大漩涡 / 诺森德 / 破碎群岛 / 赞达拉 / 库尔提拉斯 / 巨龙群岛 的中文名 |
| `wowdb.cn/zone-{id}.html` × 87 页 | **47 个 vanilla 区域里 45 个的中文名**（见 §⑤ 总表；每个都是逐页抓下来的 `<title>`） |
| `wowdb.cn/zones.html` 导航 | 大陆级中文名：东部王国 / 卡利姆多 / 外域 / 诺森德 / 大漩涡 / 潘达利亚 / 德拉诺 |

### 抓不到的（如实记录，不是没查）

| 源 | 结果 | 影响 |
|---|---|---|
| `wow.huijiwiki.com`（灰机） | **全站 403**（curl 与 WebFetch 两条路都 403） | 中文官方译名无法从首选中文源取；已改用 `wowdb.cn` + `zh.wikipedia` 顶上 |
| `warcraft.huijiwiki.com`（灰机另一域） | **403** | 同上 |
| `classic.wowhead.com` / `www.wowhead.com/zh/...` / `cn.wowhead.com` | **403（curl）/ 404（WebFetch）**，任务书给的 `&xml` 绕法在本机也没通 | 坐标与等级改从 `Classic_zones` 维基页取；本路不需要坐标（上三层节点不在任何 zone 地图上） |
| `db.duowan.com/wow/zone-{id}.html` | 返回 17 字节空壳，站已废 | 无 |
| `zhihu.com/question/49516966` | **403** | 「无尽之海 / 迷雾之海 / 禁忌之海」三连的原文没读到，只看到标题——见 §③ |
| `wowdb.cn` 的 `zone-36`（奥特兰克山脉）与各海域 id | 无页面（该库是 6.0.3 版，奥特兰克山脉在 4.0.3 已被并入希尔斯布莱德） | 这两处中文名降级处理，见 §③ |
| WebSearch | **本 session 200 次配额已用尽** | 后续核验只能走 WebFetch / curl |

### 已有资产的复用

- **暴风城城市布局不重做**。`ai_videos/shikong_lvxing/sk2/0_research/parts/w1_city_layout.md`（93 KB，643 条带出处的事实注册表）已经做完：经典旧世暴风城 = **6 个正式城区**（贸易区 / 旧城区 / 法师区 / 矮人区 / 教堂广场 / 花园区）**＋ 暴风要塞 ＋ 英雄谷**，由运河串起，共 8 个可指认地名块；另有 GM 世界坐标 14 锚点（map=0 zone=1519，单位＝码，+X＝正北 / +Y＝正西 / +Z＝上）。
- **它同时给出一条本树必须继承的版本裁定**：**暴风城港口不属于经典旧世**（3.0.2 才加）。负责暴风城的片区组**必须先读 w1，直接引用它的结论**，不要重新调研，也不要把港口 / 雄狮之眠 / 城外郊区 / 矮人区第二个拍卖行与银行 / 理发店 建成节点。

---

## ② 版本差异（4.0.3《大地的裂变》及其它资料片改了什么）

**规则：下面每一条里 4.0.3 之后才有 / 才改的东西，一律不进树。** 逐条列，按对本树的杀伤力排序。

### A. 直接影响「上三层」结构的

| # | 差异 | 本树怎么处理 |
|---|---|---|
| A1 | **奎尔萨拉斯在 vanilla 是一块「能到、但没内容」的封闭 zone**（G01-V 修正，原写「不可进」有误）。1.x 存在一块官方命名为 `Quel'thalas` 的无标记地形（wiki 页名 `Quel'Thalas/Eastern Kingdoms terrain`），**贴着提瑞斯法北岸游过去可达**（避开疲劳区），里面只有一座进不去的白塔加一个码头。永歌森林 / 幽魂之地是 **2.0 TBC** 才加的，奎尔丹纳斯岛是 **2.4**。 | region 节点 `quel_thalas` 建了并标注「可游到、无内容」；**其下的 zone 一个都不建**（结论不变：里面确实没有可拍内容） |
| A2 | **吉尔尼斯在 vanilla 只有一堵墙**。格雷迈恩之墙立在银松森林南缘（入口靠近腐木村），墙后半岛完全不可进。狼人起始区 `Gilneas (starting zone)` 与 `Ruins of Gilneas` 都是 **4.0.3** 的。 | region 节点 `gilneas` 建了并标注只有墙；**其下的 zone 一个都不建**。墙本身是银松森林里的一个 poi，归负责银松的片区组 |
| A3 | **大漩涡在 vanilla 不是大陆**，只是世界地图上的一个图形。4.0.3 才成为可进入大陆（深岩之洲 / 巨石之核 / 大漩涡战役入口）。 | 建为 `region`（海域）挂在 `the_great_sea` 下，标注 4.0.3 才可进 |
| A4 | **瓦丝琪尔（Vashj'ir）整块不存在**，是 4.0.3 新增的水下「大陆」。 | 不建 |
| A5 | **托尔巴拉德 / 暮光高地 / 海加尔山 / 奥丹姆 / 安其拉：坠落的王国** 全是 4.0.3 新增 zone。 | 不建 |
| A6 | **秘蓝岛 / 秘血岛 / 地狱火半岛等外域全境** 是 2.0 TBC。 | 外域只建一个大陆节点、不往下展开 |

### B. 头号雷区：被 4.0.3 大改的 vanilla zone（**名字还在，长相全变了**）

**这些 zone 的名字在 1.12 和今天都存在，所以最容易出错——查资料时抓到的图文十有八九是改版后的。**

| zone | 4.0.3 改了什么 | 拍片时的硬约束 |
|---|---|---|
| **艾尔文森林** | 闪金镇被重画、北郡修道院被血色十字军占领（vanilla 是正常的人类新手据点、牧师训练师在里面）、法戈第矿洞与玉石矿洞的怪与任务改了 | 主角出生地就在这儿——**必须按 vanilla 演**：北郡修道院完好、里面有牧师/圣骑士训练师与新手任务链 |
| **西部荒野** | 整个区变成难民营主题（叹息岭、难民营 NPC），月溪镇被迪菲亚占领的叙事重写，迪菲亚兄弟会主线搬到 4.0 版本 | vanilla 是「麦田荒废、豺狼人与迪菲亚流窜、死亡矿井在月溪镇底下」 |
| **赤脊山** | 整区重做成「黑石兽人入侵 + 救援七人组」战争剧，湖畔镇被打烂 | vanilla 是「安静的湖边小镇 + 石堡要塞被兽人占据 + 索克光斧的鳄鱼任务」 |
| **暮色森林** | 时间线推进、乌鸦岭与守望堡剧情改写、等级带从 18–30 被压到 10–30 | vanilla 是 **18–30 级**的高难度雾林，夜幕镇夜里有坐骑级 elite 狼人巡逻 |
| **灼热峡谷** | 入口从「要挖开一堵墙 / 走黑石山」改成直接开放，黑铁矮人剧情重写 | vanilla 进灼热峡谷要先完成开门任务 |
| **贫瘠之地** | **被一刀劈成北贫瘠之地与南贫瘠之地两个 zone**（本树只记一个 `the_barrens`，10–25 级）。注意 `wowdb.cn` 的 zone-17 显示为「北贫瘠之地」，那是改版后的名字——**vanilla 叫「贫瘠之地」** | 十字路口、棘齿城、陶拉祖营地要按 vanilla 的相对位置放 |
| **荆棘谷** | **被劈成北荆棘谷 + 荆棘海岸两个 zone**（本树只记一个 `stranglethorn_vale`，30–45 级） | 藏宝海湾在南端，古拉巴什竞技场在中段 |
| **奥特兰克山脉** | **整个 zone 被删，并入希尔斯布莱德丘陵** | vanilla 它是独立 zone（30–40 级），奥特兰克山谷战场入口在这儿 |
| **希尔斯布莱德丘陵** | 南海镇被血色十字军/被遗忘者剧情炸掉（`Ruins of Southshore`） | vanilla 南海镇是完好的联盟城镇，对面是塔伦米尔，是经典的野外 PvP 热点 |
| **提瑞斯法林地 / 银松森林 / 东西瘟疫之地** | 剧情推进、部分据点易主 | 按 vanilla：西瘟疫之地的安多哈尔还在打三方拉锯 |
| **黑石山** | 上层黑石塔在 6.2 被重做 | 按 vanilla |

### C. 其它会误导的版本事实

- **暴风城港口（Stormwind Harbor）是 3.0.2 加的**，vanilla 没有。去诺森德的船因此在 vanilla 根本不存在。（来源：sk2 `w1_city_layout.md` 版本错置清单）
- **达拉然在 vanilla 是一个被紫色魔法罩扣住的废墟**，位于西瘟疫之地地面上，不是诺森德上空的浮空城（3.0 才搬）。
- **死亡骑士起始区（巫妖王之怒，东瘟疫之地：血色领地）** 是 3.0，vanilla 无。
- **英雄难度 / 随机队列 / 飞行坐骑在旧世** 全都不存在。
- 维基上大量 zone 主条目写的是**当前版本**；凡是引用 zone 页，要优先看 `{{replaced|XXX (Classic)|Classic}}` 指向的 **`XXX (Classic)` 页**。

---

## ③ 存疑与未查

### 中文译名核验状态（**下游必读**）

`verified_by` 字段记的是「英文源页有没有真的抓到」，**不等于中文译名也核过了**。两件事分开记：

| 节点 | name_zh | 中文译名核验 | 说明 |
|---|---|---|---|
| azeroth / eastern_kingdoms / kalimdor / lordaeron / khaz_modan / azeroth_subcontinent / quel_thalas / gilneas / the_maelstrom / outland / northrend / pandaria / broken_isles / zandalar / kul_tiras / dragon_isles | 艾泽拉斯 / 东部王国 / 卡利姆多 / 洛丹伦 / 卡兹莫丹 / 艾泽拉斯次大陆 / 奎尔萨拉斯 / 吉尔尼斯 / 大漩涡 / 外域 / 诺森德 / 潘达利亚 / 破碎群岛 / 赞达拉 / 库尔提拉斯 / 巨龙群岛 | ✅ 已核 | 中文源页（zh.wikipedia 地名列表 + wowdb.cn 导航）逐个抓到 |
| stranglethorn | 荆棘谷 | ✅ 已核 | `wowdb.cn/zone-33.html` 标题 |
| veiled_sea | 迷雾之海 | ✅ 已核 | `wowdb.cn/zone-457.html` 标题 |
| kingdom_of_stormwind | 暴风王国 | ⚠️ 半核 | zh.wikipedia 同一句里同时出现「暴风王国」与「暴风城王国」两种写法。取「暴风王国」，**请用国服客户端复核** |
| the_great_sea | 无尽之海 | ✅ 已核（G01-V 升级） | zh.wikipedia 地名列表原句「东部王国（Eastern Kingdoms）位于无尽之海的西边，由四块次大陆组成。」——**中文名实证成立**。同句的方位仍是错的（英文维基：东部王国在无尽之海**以东**），名可用、方位不可用。另一候选「大海」不采用。详见 §V.4 |
| forbidding_sea | 禁忌之海 | ⚠️ 存疑 | 同上，只有上述标题这一条线索 |
| south_seas | 南海 | ⚠️ 存疑 | 常见写法，未从抓到的页面上取证 |
| northern/central/southern_kalimdor | 北 / 中 / 南卡利姆多 | ⚠️ 直译 | 这三个是《游戏手册》《Lands of Mystery》的 lore 分区名，**国服官方译名未查到**。写的是直译（不是音译），下游如查到官方写法请直接改 YAML |
| khaz_algar | ~~卡兹阿加~~ → **`Khaz Algar`（英文原名）** | ❌ 查无，已按规则回退（G01-V） | 灰机 403 / zh.wikipedia 地名列表无此词 / WebSearch 配额耗尽，三路落空。按 §5.5.8「查不到就留英文原名，绝不自己音译」已把 YAML 的 `name_zh` 改回英文原名，音译候选「卡兹阿加」保留在该节点 `note_zh`。11.0 的大陆，本剧不拍，低优先。详见 §V.2.3 |

### 其它存疑

1. **奥特兰克山脉的中文名「奥特兰克山脉」未从抓到的页面取证**——`wowdb.cn` 是 6.0.3 版数据库，该 zone 已在 4.0.3 被删，所以没有页面。但「奥特兰克山谷」这个战场名在 `wowdb.cn` 的其它页里是通行写法，可信度高。负责该片区的组请复核一次。
2. **黑石山（Blackrock Mountain）到底挂谁**。维基自己写成「Azeroth / Khaz Modan」两边都算——它物理上卡在燃烧平原（艾泽拉斯次大陆）与灼热峡谷（卡兹莫丹）之间。本树**挂 `azeroth_subcontinent`**，`adjacent` 同时写两边。这是一个明确的取舍，不是疏漏。
3. **东部王国到底是「三块」还是「四块」次大陆**。维基原话：「The Eastern Kingdoms is divided into three and sometimes four continents」，第四块指奎尔萨拉斯。本树按**三块**建（`azeroth_subcontinent` / `khaz_modan` / `lordaeron`），把 `quel_thalas` 降一层挂在 `lordaeron` 下——依据是同一页的下一句：「most of the time it appears that the Eastern Kingdoms are divided into only three continents as Quel'Thalas is shown as part of northern Lordaeron」。zh.wikipedia 则写「由四块次大陆组成」，与英文维基的少数派说法一致。**若合龙时决定改成四块，只需把 `quel_thalas.parent` 从 `lordaeron` 改成 `eastern_kingdoms`，其余不动。**
4. **「七大王国」没有建成节点**。洛丹伦王国 / 斯托颂谷地(斯托姆加德) / 奥特兰克 / 达拉然 / 库尔提拉斯 / 吉尔尼斯 / 暴风城 是人类的七个王国（另加精灵的奎尔萨拉斯）。本树只建了 `kingdom_of_stormwind`（因为主角整个前 30 级都在它境内）与 `gilneas`（因为任务书点名）。**斯托姆加德、奥特兰克、达拉然一律不建 region 节点**——否则负责阿拉希高地 / 奥特兰克山脉 / 西瘟疫之地的组会不知道该写哪个 parent。它们在 vanilla 都只是各自 zone 里的一处废墟或据点，按 `settlement` / `poi` 挂在 zone 下即可。
5. **瘟疫之地（The Plaguelands）也没有建成 region 节点**，同理——东西瘟疫之地直接挂 `lordaeron`。
6. **外域的 parent 是妥协**。外域严格说不在艾泽拉斯星球上，它是另一个世界德拉诺的残骸。挂在世界根 `azeroth` 下纯粹为了树的连通性，`note_zh` 里写明了。若下游要严谨，可以另起一个 `great_dark_beyond` 根——但那会让树有两个根，得不偿失。

---

## ④ 本片区的地图图片链接清单

**只记 URL 与版权状态，没有下载。** 仓库既有裁定：**暴雪美术资产只进人眼、不入画、不上传给生成模型**——这些图只用来给人看清空间关系，任何一张都**不得**作为参考图喂给 Seedream / Seedance / 即梦。

| 图 | URL | 用途 | 版权 |
|---|---|---|---|
| 世界地图（大分裂后） | `https://warcraft.wiki.gg/wiki/File:WorldMap-World.jpg` | 四大陆 + 无尽之海 + 大漩涡的相对位置 | © Blizzard，仅人眼 |
| 东部王国 · **WoW 首发版** | `https://warcraft.wiki.gg/wiki/File:VZ-Eastern_Kingdoms-old.jpg` | **本树最该看的一张**——vanilla 的东部王国全图 | © Blizzard，仅人眼 |
| 东部王国 · WoW alpha | `https://warcraft.wiki.gg/wiki/File:WorldMap-Azeroth-alpha.jpg` | 对照早期地名 | © Blizzard，仅人眼 |
| 东部王国 · Classic 飞行点图 | `https://warcraft.wiki.gg/wiki/File:TaxiMap0_Classic.png` | **vanilla 的全部飞行点与航线**，下游建 `transport` 节点的一手依据 | © Blizzard，仅人眼 |
| 卡利姆多 · 预发布版 | `https://warcraft.wiki.gg/wiki/File:Kalimdor2.JPG` | vanilla 卡利姆多全图 | © Blizzard，仅人眼 |
| 艾泽拉斯次大陆（游戏手册） | `https://warcraft.wiki.gg/wiki/File:WoWAzeroth.jpg` | 南部次大陆范围 | © Blizzard，仅人眼 |
| 卡兹莫丹（游戏手册） | `https://warcraft.wiki.gg/wiki/File:WoWKhazModan.jpg` | 中部次大陆范围 | © Blizzard，仅人眼 |
| 洛丹伦（游戏手册） | `https://warcraft.wiki.gg/wiki/File:WoWLordaeron.jpg` | 北部次大陆范围 | © Blizzard，仅人眼 |
| 北 / 南卡利姆多（游戏手册） | `https://warcraft.wiki.gg/wiki/File:Northern_Kalimdor.jpg` · `https://warcraft.wiki.gg/wiki/File:Southernkalimdor.JPG` | 三分区边界 | © Blizzard，仅人眼 |
| 无尽之海 / 迷雾之海 / 禁忌之海（编年史） | `File:Chron3_map_of_Azeroth_after_the_Cataclysm.jpg` · `File:Veiled_Sea_Chronicle.jpg` · `File:Forbidding_Sea_Chronicle.jpg`（同域 `/wiki/` 前缀） | 三片海的范围 | © Blizzard 书籍插图，仅人眼 |
| 各 vanilla zone 的旧版地图 | `File:WorldMap-{Zone}-old.jpg` 系列（`Elwynn`/`Westfall`/`Redridge`/`Duskwood`/`DunMorogh`/`LochModan`/`Wetlands`/`Tirisfal`/`Silverpine`/`Hillsbrad`/`Arathi`/`Badlands`/`SwampOfSorrows`/`Hinterlands`/`SearingGorge`/`BlastedLands`/`BurningSteppes`/`WesternPlaguelands`/`EasternPlaguelands`/`DeadwindPass`/`Durotar`/`Mulgore`/`Teldrassil`/`Darkshore`/`Barrens`/`StonetalonMountains`/`Ashenvale`/`ThousandNeedles`/`Desolace`/`Dustwallow`/`Feralas`/`Tanaris`/`Aszhara`/`UngoroCrater`/`Felwood`/`Winterspring`/`Silithus`/`Moonglade`；另 `Stranglethorn` 与 `Hillsbrad` 无 `-old` 后缀） | **文件名带 `-old` 的就是 4.0.3 之前的版本**，各片区组测绘自己的 zone 时直接看这张 | © Blizzard，仅人眼 |

> 注意 `File:Aszhara` 的拼写——维基上的文件名把 Azshara 拼错成 Aszhara，照抄才找得到。

---

## ⑤ 全局图例 + zone 总表 + 给下游的提醒

### 5.1 全局图例（**本树的统一口径，12 路都按这个写**）

#### `type`

| 值 | 含义 | 本树的典型例子 |
|---|---|---|
| `world` | 行星 | `azeroth`（唯一一个，parent=null） |
| `continent` | 大陆 | `eastern_kingdoms` `kalimdor` `outland` … |
| `region` | 大陆内的 lore 分区 **＋ 海域** | `khaz_modan` `kingdom_of_stormwind` `the_great_sea` |
| `zone` | 地图上按 Esc-地图能选中的地区 | `elwynn_forest` `westfall` |
| `city` | 主城 | `stormwind_city` `ironforge` `undercity` `orgrimmar` `thunder_bluff` `darnassus`（vanilla 只有这 6 个） |
| `district` | 主城内的区 | `trade_district` `old_town` … |
| `subzone` | 走进去左上角小地图名会变的子区域 | `northshire_valley` `fargodeep_mine` |
| `settlement` | 有人住的点 | `goldshire` `sentinel_hill` |
| `dungeon` / `raid` / `battleground` | 副本 / 团本 / 战场 | `the_deadmines` / `molten_core` / `warsong_gulch` |
| `poi` | 地标：桥 / 塔 / 矿洞口 / 墓地 / 传送门 | `tower_of_azora` `stonecairn_lake` |
| `transport` | 飞行点 / 码头 / 地铁站 | `goldshire_flightpath`（无飞行点）`menethil_harbor_dock` |

> **schema 里没有 `sea` 这个值**，所以五片水体一律 `type: region` + `subtype: ""`，靠 `note_zh` 说明它是海域。**12 路不要自造 `sea` / `ocean` 枚举值。**

#### `subtype`（只有两种 type 需要填，其余一律空串 `""`）

- `settlement` 必填其一：`capital` / `town` / `village` / `camp` / `farm` / `mine` / `tower` / `port` / `inn` / `ruin` / `crossroads`
- `transport` 必填其一：`flightpath` / `boat` / `tram` / `portal`

#### `faction`

`alliance` / `horde` / `contested` / `neutral` / `pvp` / `""`

**vanilla 的 PvP 归属按 `Classic_zones` 维基页的 PvP Status 列写**，见下面总表的「阵营」栏。注意：`contested`（争夺）是 vanilla 绝大多数中高级 zone 的状态，别一看有联盟据点就写 `alliance`。

#### `era`

`vanilla`（旧世就有）/ `tbc` / `wotlk` / `cata_plus`。**本树只收 `vanilla`**；G01 里出现的非 vanilla 节点（外域 / 诺森德 / 潘达利亚 / 破碎群岛 / 赞达拉 / 库尔提拉斯 / 巨龙群岛 / 卡兹阿加）是任务书明确要求列出的「世界全貌」，**只到大陆这一层，不往下展开**。

#### `adjacent` 只有 `zone` 与 `continent` 填

schema 原话是「只有 zone / continent 填」，所以 G01 的 **10 个 region 节点与 5 片海域的 `adjacent` 一律留空 `[]`**，只有 `eastern_kingdoms` / `kalimdor` / `outland` 三个 continent 填了。
region 之间真实存在的邻接关系在这里留档（**不进 YAML**，以免机检报错；若合龙时决定放宽规则，照这张表回填即可）：

| region | 接壤 / 有固定通路的邻居 | 通路 |
|---|---|---|
| `azeroth_subcontinent` | `khaz_modan` | 唯一陆路是**燃烧平原→黑石山→灼热峡谷**；RPG 资料另称经灼热峡谷 |
| `khaz_modan` | `azeroth_subcontinent` · `lordaeron` | 北面靠**萨多尔大桥（Thandol Span）**跨海峡接洛丹伦 |
| `lordaeron` | `khaz_modan` | 同上 |
| `kingdom_of_stormwind` | `stranglethorn` | 暮色森林 → 荆棘谷北口 |
| `stranglethorn` | `kingdom_of_stormwind` · `south_seas` | 北接暮色森林；南岸藏宝海湾临南海 |
| `quel_thalas` | —— | vanilla 不可进，无通路 |
| `gilneas` | —— | vanilla 被格雷迈恩之墙封死，无通路 |
| `northern_kalimdor` | `central_kalimdor` | 灰谷 ←→ 石爪山脉 / 贫瘠之地 |
| `central_kalimdor` | `northern_kalimdor` · `southern_kalimdor` | 贫瘠之地 ←→ 千针石林；凄凉之地 ←→ 菲拉斯 |
| `southern_kalimdor` | `central_kalimdor` | 同上 |
| `the_great_sea` | `eastern_kingdoms` · `kalimdor` | 它就是把这两块大陆隔开的那片洋；`the_maelstrom` 在它正中，`south_seas` 是它靠南的一部分 |
| `veiled_sea` | `kalimdor` | 卡利姆多的西岸与北岸 |
| `forbidding_sea` | `eastern_kingdoms` | 东部王国的东岸 |

#### `id` 命名

小写英文 + 下划线，来自英文原名。**重名必须加限定**（`raven_hill_duskwood`）。已知会撞的：

| 撞名 | 怎么区分 |
|---|---|
| 世界 `azeroth` vs 南部次大陆 | 次大陆用 **`azeroth_subcontinent`** |
| 分区 `stranglethorn`（region）vs zone | zone 用 **`stranglethorn_vale`** |
| `khaz_modan`（次大陆）vs 铁炉堡王国 | 王国若要建，用 `kingdom_of_ironforge` |
| `lordaeron`（次大陆）vs 洛丹伦王国 vs 洛丹伦废墟 | 王国 `kingdom_of_lordaeron`、废墟 `ruins_of_lordaeron`（但见 §③.4：本树不建王国节点） |

### 5.2 vanilla zone 总表（**后面 12 路的对账基准，一个 zone 都不能漏**）

等级带与 PvP 状态逐行出自 `warcraft.wiki.gg/wiki/Classic_zones`（真的抓到并读过）。
中文名出自 `wowdb.cn/zone-{id}.html` 逐页抓取（`zone id` 列同时是 AreaTable id，可复查）。
**「parent id」是 G01 定死的，12 路直接照抄，不要自己想。**

#### 东部王国 · 23 个 zone

| # | zone id | name_en | name_zh | 次大陆 region | **parent id（照抄）** | vanilla 等级 | 阵营 |
|---:|---:|---|---|---|---|---|---|
| 1 | 12 | Elwynn Forest | 艾尔文森林 | 艾泽拉斯 | `kingdom_of_stormwind` | 1-10 | alliance |
| 2 | 1 | Dun Morogh | 丹莫罗 | 卡兹莫丹 | `khaz_modan` | 1-10 | alliance |
| 3 | 85 | Tirisfal Glades | 提瑞斯法林地 | 洛丹伦 | `lordaeron` | 1-10 | horde |
| 4 | 40 | Westfall | 西部荒野 | 艾泽拉斯 | `kingdom_of_stormwind` | 10-20 | alliance |
| 5 | 38 | Loch Modan | 洛克莫丹 | 卡兹莫丹 | `khaz_modan` | 10-20 | alliance |
| 6 | 130 | Silverpine Forest | 银松森林 | 洛丹伦 | `lordaeron` | 10-20 | horde |
| 7 | 44 | Redridge Mountains | 赤脊山 | 艾泽拉斯 | `kingdom_of_stormwind` | 15-25 | contested |
| 8 | 10 | Duskwood | 暮色森林 | 艾泽拉斯 | `kingdom_of_stormwind` | 18-30 | contested |
| 9 | 11 | Wetlands | 湿地 | 卡兹莫丹 | `khaz_modan` | 20-30 | contested |
| 10 | 267 | Hillsbrad Foothills | 希尔斯布莱德丘陵 | 洛丹伦 | `lordaeron` | 20-35 | contested |
| 11 | 45 | Arathi Highlands | 阿拉希高地 | 洛丹伦 | `lordaeron` | 30-40 | contested |
| 12 | 36 | Alterac Mountains | 奥特兰克山脉 ⚠️ | 洛丹伦 | `lordaeron` | 30-40 | contested |
| 13 | 33 | Stranglethorn Vale | 荆棘谷 | 艾泽拉斯 | `stranglethorn` | 30-45 | contested |
| 14 | 3 | Badlands | 荒芜之地 | 卡兹莫丹 | `khaz_modan` | 35-45 | contested |
| 15 | 8 | Swamp of Sorrows | 悲伤沼泽 | 艾泽拉斯 | `azeroth_subcontinent` | 35-45 | contested |
| 16 | 47 | The Hinterlands | 辛特兰 | 洛丹伦 | `lordaeron` | 40-50 | contested |
| 17 | 51 | Searing Gorge | 灼热峡谷 | 卡兹莫丹 | `khaz_modan` | 45-50 | contested |
| 18 | 4 | The Blasted Lands | 诅咒之地 | 艾泽拉斯 | `azeroth_subcontinent` | 45-55 | contested |
| 19 | 25 | Blackrock Mountain | 黑石山 | 艾泽拉斯 / 卡兹莫丹 跨界 | `azeroth_subcontinent` | 49-60 | contested |
| 20 | 46 | Burning Steppes | 燃烧平原 | 艾泽拉斯 | `azeroth_subcontinent` | 50-58 | contested |
| 21 | 28 | Western Plaguelands | 西瘟疫之地 | 洛丹伦 | `lordaeron` | 51-58 | contested |
| 22 | 139 | Eastern Plaguelands | 东瘟疫之地 | 洛丹伦 | `lordaeron` | 53-60 | contested |
| 23 | 41 | Deadwind Pass | 逆风小径 | 艾泽拉斯 | `kingdom_of_stormwind` | 55-60 | contested |

⚠️ 奥特兰克山脉的中文名未从抓到的页面取证，见 §③.1。

#### 卡利姆多 · 18 个 zone

| # | zone id | name_en | name_zh | 分区 region | **parent id（照抄）** | vanilla 等级 | 阵营 |
|---:|---:|---|---|---|---|---|---|
| 24 | 14 | Durotar | 杜隆塔尔 | 中 | `central_kalimdor` | 1-10 | horde |
| 25 | 215 | Mulgore | 莫高雷 | 中 | `central_kalimdor` | 1-10 | horde |
| 26 | 141 | Teldrassil | 泰达希尔 | 北 | `northern_kalimdor` | 1-10 | alliance |
| 27 | 148 | Darkshore | 黑海岸 | 北 | `northern_kalimdor` | 10-20 | alliance |
| 28 | 17 | The Barrens | 贫瘠之地 ⚠️ | 中 | `central_kalimdor` | 10-25 | horde |
| 29 | 406 | Stonetalon Mountains | 石爪山脉 | 中 | `central_kalimdor` | 15-27 | contested |
| 30 | 331 | Ashenvale | 灰谷 | 北 | `northern_kalimdor` | 18-30 | contested |
| 31 | 400 | Thousand Needles | 千针石林 | 南 | `southern_kalimdor` | 25-35 | contested |
| 32 | 405 | Desolace | 凄凉之地 | 中 | `central_kalimdor` | 30-40 | contested |
| 33 | 15 | Dustwallow Marsh | 尘泥沼泽 | 中 | `central_kalimdor` | 35-40 | contested |
| 34 | 357 | Feralas | 菲拉斯 | 南 | `southern_kalimdor` | 40-50 | contested |
| 35 | 440 | Tanaris | 塔纳利斯 | 南 | `southern_kalimdor` | 40-50 | contested |
| 36 | 16 | Azshara | 艾萨拉 | 北 | `northern_kalimdor` | 45-55 | contested |
| 37 | 490 | Un'Goro Crater | 安戈洛环形山 | 南 | `southern_kalimdor` | 48-55 | contested |
| 38 | 361 | Felwood | 费伍德森林 | 北 | `northern_kalimdor` | 48-55 | contested |
| 39 | 618 | Winterspring | 冬泉谷 | 北 | `northern_kalimdor` | 53-60 | contested |
| 40 | 1377 | Silithus | 希利苏斯 | 南 | `southern_kalimdor` | 55-60 | contested |
| 41 | 493 | Moonglade | 月光林地 | 北 | `northern_kalimdor` | N/A（几乎无怪） | contested |

⚠️ `wowdb.cn` 的 zone-17 标题是「北贫瘠之地」——那是 4.0.3 拆分后的名字。**vanilla 叫「贫瘠之地」，本树用它。**

#### 主城 · 6 个（vanilla 只有这 6 个）

| # | zone id | name_en | name_zh | **parent id（照抄）** | 阵营 |
|---:|---:|---|---|---|---|
| 42 | 1519 | Stormwind City | 暴风城 | `elwynn_forest` | alliance |
| 43 | 1537 | Ironforge | 铁炉堡 | `dun_morogh` | alliance |
| 44 | 1497 | Undercity | 幽暗城 | `tirisfal_glades` | horde |
| 45 | 1637 | Orgrimmar | 奥格瑞玛 | `durotar` | horde |
| 46 | 1638 | Thunder Bluff | 雷霆崖 | `mulgore` | horde |
| 47 | 1657 | Darnassus | 达纳苏斯 | `teldrassil` | alliance |

**合计 47 个：东部王国 23 zone + 卡利姆多 18 zone + 6 主城。**
**这 47 个一个都不能漏、一个都不能多**——多出来的多半是 4.0.3 之后的（北/南贫瘠之地、北荆棘谷、荆棘海岸、吉尔尼斯废墟、暮光高地、托尔巴拉德、海加尔山、奥丹姆、瓦丝琪尔），或 TBC 之后的（永歌森林、幽魂之地、奎尔丹纳斯岛、秘蓝岛、秘血岛、银月城、逃亡者营地）。

### 5.3 vanilla 副本 / 团本 / 战场的宿主 zone（下游建节点时的 parent 依据）

出自 `Classic_zones` 页的 Notes 栏 + `Eastern_Kingdoms` 页的 Dungeons 节。**节点由各 zone 的片区组建，G01 不建。**

| 类型 | 名称 | 宿主 zone |
|---|---|---|
| dungeon | 怒焰裂谷 Ragefire Chasm | 奥格瑞玛（杜隆塔尔） |
| dungeon | 死亡矿井 The Deadmines | 西部荒野（月溪镇） |
| dungeon | 哀嚎洞穴 Wailing Caverns | 贫瘠之地 |
| dungeon | 影牙城堡 Shadowfang Keep | 银松森林 |
| dungeon | 黑暗深渊 Blackfathom Deeps | 灰谷 |
| dungeon | 监狱 The Stockade | 暴风城（旧城区） |
| dungeon | 诺莫瑞根 Gnomeregan | 丹莫罗 |
| dungeon | 剃刀沼泽 Razorfen Kraul | 贫瘠之地 |
| dungeon | 血色修道院 Scarlet Monastery | 提瑞斯法林地 |
| dungeon | 剃刀高地 Razorfen Downs | 贫瘠之地 |
| dungeon | 奥达曼 Uldaman | 荒芜之地 |
| dungeon | 祖尔法拉克 Zul'Farrak | 塔纳利斯 |
| dungeon | 玛拉顿 Maraudon | 凄凉之地 |
| dungeon | 沉没的神庙 Temple of Atal'Hakkar | 悲伤沼泽 |
| dungeon | 黑石深渊 Blackrock Depths | 黑石山 |
| dungeon | 黑石塔（上/下层） Blackrock Spire | 黑石山 |
| dungeon | 厄运之槌 Dire Maul | 菲拉斯 |
| dungeon | 斯坦索姆 Stratholme | 东瘟疫之地 |
| dungeon | 通灵学院 Scholomance | 西瘟疫之地（凯尔达隆） |
| raid | 熔火之心 Molten Core | 黑石山 |
| raid | 奥妮克希亚的巢穴 Onyxia's Lair | 尘泥沼泽 |
| raid | 黑翼之巢 Blackwing Lair | 黑石山 |
| raid | 祖尔格拉布 Zul'Gurub | 荆棘谷 |
| raid | 安其拉废墟 / 安其拉神殿 | 希利苏斯 |
| raid | 纳克萨玛斯 Naxxramas | 东瘟疫之地 |
| battleground | 战歌峡谷 Warsong Gulch | 灰谷 / 贫瘠之地交界 |
| battleground | 阿拉希盆地 Arathi Basin | 阿拉希高地 |
| battleground | 奥特兰克山谷 Alterac Valley | 奥特兰克山脉 |

### 5.4 跨大陆固定通路（`transport` 节点由各 zone 的组建，G01 不建，避免撞 id）

vanilla **没有跨海飞行点**（游戏手册原话：There are no flight paths across the ocean linking Kalimdor and Azeroth）。两块大陆之间只有这几条：

| 类型 | 东部王国一侧 | 卡利姆多一侧 |
|---|---|---|
| boat | 米奈希尔港（湿地） | 奥伯丁（黑海岸） |
| boat | 米奈希尔港（湿地） | 塞拉摩岛（尘泥沼泽） |
| boat | 藏宝海湾（荆棘谷） | 棘齿城（贫瘠之地） |
| zeppelin | 幽暗城（提瑞斯法林地） | 奥格瑞玛（杜隆塔尔） |
| zeppelin | 格罗姆高营地（荆棘谷） | 奥格瑞玛（杜隆塔尔） |
| tram | 暴风城（矮人区） ←→ 铁炉堡 | —（深铁矿道地铁，是东部王国内部线，sk2 `w7_deeprun_tram.md` 已做完，直接引用别重查） |

### 5.5 给下游的提醒（**开工前逐条过一遍**）

1. **parent 照抄 §5.2 的「parent id」列**。`elwynn_forest` 的 parent 是 `kingdom_of_stormwind`，不是 `eastern_kingdoms`，也不是 `azeroth_subcontinent`。
2. **树不是等深的**。艾尔文森林在第 5 层（世界→大陆→次大陆→王国→zone），悲伤沼泽在第 4 层（世界→大陆→次大陆→zone）。这是对的，不是 bug——`kingdom_of_stormwind` 与 `stranglethorn` 是次大陆内的政治/地理分区，而悲伤沼泽 / 诅咒之地 / 燃烧平原 / 黑石山不属于任何一个。**不要为了对齐层数硬塞一个假 region。**
3. **`stranglethorn`（region）≠ `stranglethorn_vale`（zone）**。负责荆棘谷的组建的是后者，parent 写前者。
4. **黑石山挂 `azeroth_subcontinent`**，`adjacent` 写 `[burning_steppes, searing_gorge]`。
5. **暴风城先读 sk2**：`ai_videos/shikong_lvxing/sk2/0_research/parts/w1_city_layout.md`（城区布局 + 14 个 GM 世界坐标锚点）与 `w7_deeprun_tram.md`（矿道地铁）。**不要重新调研，直接引用它的结论。** vanilla 的暴风城是 6 个正式城区 + 暴风要塞 + 英雄谷，**没有港口**。
6. **查 zone 页时优先读 `{Zone} (Classic)` 页**，不要读 zone 主条目——主条目写的是当前版本。地图图片认准文件名里的 `-old`。
7. **`era` 一律写 `vanilla`**。查到的东西如果是 TBC/WotLK/Cata 才有的，**不是改 `era`，是根本不建这个节点**，改为写进你的 notes.md §版本差异。
8. **`name_zh` 查不到就留英文原名 + `note_zh` 写「官方译名未查到」，绝不自己音译。** `wowdb.cn/zone-{AreaTable id}.html` 这条路本机可通（灰机 wiki 与 wowhead 全 403），子区域也有页，优先试它。
9. **完整性硬指标**：每个 zone 的 wiki 页 Subzones 一节里列的子区域**一个都不能漏**，典型 zone 应有 15–40 个节点，**少于 10 个等于没查全**。
10. **暴雪美术资产只进人眼**——任何 wiki 地图截图 / 原画都不得喂给生成模型。

### 5.6 合龙对账 · 收尾时实测到的冲突（**必须在合成主树前解决**）

G01 收尾时 `map/` 目录下已经落了 9 份别路的 YAML（G02–G08、G12、G13；G09/G10/G11 当时还没落）。
把它们和本路逐条对了一遍，**下面是真实冲突，不是假设**。G01 是上三层的定义方，冲突一律**以本路为准**。

#### A. 重复 id（同一个 id 被两个文件各定义了一次）

| id | 出现在 | 判定 |
|---|---|---|
| `khaz_modan` | `g01` · `g05_khaz_modan.yaml` | **删 G05 的那份**。两边语义一致（`type: region`, `parent: eastern_kingdoms`），但定义权归 G01 |
| `northern_kalimdor` | `g01` · `g08_kalimdor_north.yaml` | **删 G08 的那份**，同上（`parent: kalimdor`） |
| `the_great_sea` | `g01` · `g08_kalimdor_north.yaml` | **删 G08 的那份** |
| `south_seas` | `g01` · `g04_ek_south.yaml` | **删 G04 的那份** |

> 另有 21 处重复 id 发生在**别路之间**（G02↔G13 的北郡/闪金镇一带 9 个、G02↔G03 的 `stormwind_gate`、G03↔G12 的 `deeprun_tram` 两个、G04↔G05 的 `stonewrought_pass`、G05↔G07 的 `thandol_span`/`the_green_belt`、G06↔G07 的 `thoradins_wall`/`the_bulwark`、G07↔G12 的 5 个 `fp_*` 飞行点）。**不归 G01 裁决**，但一并记在这里，合龙时要一个个定归属——`thandol_span`（萨多尔大桥）与 `thoradins_wall`（索拉丁之墙）尤其典型：它们本来就横跨两个片区的边界，必须指定唯一 owner。

#### B. parent 与 §5.2 总表不一致（**次大陆层被跳过**）

`g04_ek_south.yaml` 把 5 个 zone 直接挂到了 `eastern_kingdoms`，1 个挂错了次大陆：

| zone | G04 现写 | **§5.2 定的正确值** | 为什么 |
|---|---|---|---|
| `stranglethorn_vale` | `eastern_kingdoms` | **`stranglethorn`** | 荆棘谷是艾泽拉斯次大陆下的独立分区 |
| `swamp_of_sorrows` | `eastern_kingdoms` | **`azeroth_subcontinent`** | 跳了次大陆层 |
| `blasted_lands` | `eastern_kingdoms` | **`azeroth_subcontinent`** | 同上 |
| `burning_steppes` | `eastern_kingdoms` | **`azeroth_subcontinent`** | 同上 |
| `deadwind_pass` | `eastern_kingdoms` | **`kingdom_of_stormwind`** | 维基的暴风王国领地表把逆风小径列在王国境内 |
| `blackrock_mountain` | `khaz_modan` | **`azeroth_subcontinent`** | 见 §③.2——它跨界，本树裁定挂艾泽拉斯次大陆，`adjacent` 写 `[burning_steppes, searing_gorge]` |
| `searing_gorge` | `khaz_modan` | `khaz_modan` ✅ | 一致，不用改 |

**根因**：`azeroth_subcontinent` 这个 id 只有 G01 建（任务书的示例节点写的是 `parent: kingdom_of_stormwind`，没提次大陆层），所以 G04 无从得知。这不是 G04 的错，是分工缝隙。**合龙脚本按上表改 6 行即可，不用重跑 G04。**

#### C. 已经对上的（不用动）

- `g02_stormwind_kingdom_core.yaml`：`elwynn_forest` / `westfall` / `redridge_mountains` / `duskwood` → `kingdom_of_stormwind` ✅ 与 §5.2 完全一致
- `g03_stormwind_city.yaml`：`stormwind_city` → `kingdom_of_stormwind`。⚠️ §5.2 写的是 `elwynn_forest`（维基原话「Stormwind City in Elwynn Forest, Azeroth」）。**两种都说得通**——G03 挂的是政治归属，G01 挂的是地理归属。**合龙时二选一并统一**；本路建议按地理走（`elwynn_forest`），因为整棵树的其余部分都是地理递进
- `g06` / `g07`：8 个 zone → `lordaeron` ✅
- `g05`：`khaz_modan` → `eastern_kingdoms` ✅（删重复节点后，其下 zone 挂 G01 的 `khaz_modan` 即可）
- `g08`：`northern_kalimdor` → `kalimdor` ✅（同上）
- `g12_transport.yaml`：`deeprun_tram` → `eastern_kingdoms`。矿道地铁跨艾尔文森林与丹莫罗两地，挂大陆层合理；但它与 `g03` 里的同名节点重复，**owner 建议给 G12**

#### D. 还缺的片区

收尾时 **G09 / G10 / G11 的文件还没落**。按 §5.2 总表反查，这三路应当覆盖的是卡利姆多中部与南部（杜隆塔尔 / 莫高雷 / 贫瘠之地 / 石爪山脉 / 凄凉之地 / 尘泥沼泽 / 千针石林 / 菲拉斯 / 塔纳利斯 / 安戈洛环形山 / 希利苏斯 + 奥格瑞玛 / 雷霆崖）以及 `g12` 里那批指向它们的悬空 parent（`theramore_isle` / `ratchet` / `durotar` / `feathermoon_stronghold` / `stonetalon_peak` / `rutheran_village` / `forgotten_coast` / `gromgol_base_camp` 等）。**合龙前必须确认这些 id 有人建**，否则 G12 的 12 个 transport 节点会挂空。

---

## 核验记录（G01-V）

**独立核验员，2026-09-20。默认立场：怀疑每一个地名。**
核验后节点数 **26 → 28**（补 2，删 0）。判定：**已修订可用**。

### V.0 本次实际抓到的页面清单（每一条都是真的 fetch 过、不是搜索摘要）

`curl` 打 `warcraft.wiki.gg` 已被站方拦截（返回 `Blocked - wiki.gg` 的 HTML，作者当时能用的那条路现在不通了）；
本轮全部改用 **WebFetch**，并优先打 `index.php?title=X&action=raw`（拿 wikitext 原文）与
`api.php?action=parse&prop=wikitext&section=N`（拿指定小节原文），以便逐字比对 quote。

| 页 | 取法 | 用来核什么 |
|---|---|---|
| `Azeroth`（渲染页 + `section=1` Geography 原文） | WebFetch | 四大陆原句、潘达利亚迷雾句、五岛句、**全页只点名 5 片海** |
| `Eastern_Kingdoms`（`action=raw`） | WebFetch | 三/四次大陆原句、奎尔萨拉斯归北洛丹伦原句 |
| `Kalimdor`（渲染页） | WebFetch | 北/中/南三分区原句 + 各分区 zone 清单 |
| `Northern_Kalimdor` / `Central_Kalimdor`（`action=raw` 全文）/ `Southern_Kalimdor` | WebFetch | 三个分区的定义句与 zone 清单 |
| `Azeroth_(continent)`（`action=raw`） | WebFetch | 次大陆定义句、荆棘谷原句、章节结构 |
| `Khaz_Modan` / `Lordaeron`（`action=raw`） | WebFetch | 次大陆定义句 + 各自 zone/子分区树 |
| `Stormwind_(kingdom)`：`action=raw&section=0` + `api.php?prop=sections` + **`action=raw&section=29`（Territory and outposts 原文）** | WebFetch | 领地清单逐条 |
| `Quel'Thalas`（`action=raw`）+ `Quel'Thalas/Eastern_Kingdoms_terrain`（渲染页） | WebFetch | **vanilla 可达性**的原文 |
| `Greymane_Wall` | WebFetch | 城墙位置原句 |
| `Great_Sea`（渲染页 + `action=raw`） | WebFetch | **无尽之海的三个组成海域清单** |
| `Veiled_Sea` / `Forbidding_Sea` / `South_Seas` / `Maelstrom`（`section=0`） | WebFetch | 四片水体定义句 |
| **`Frozen_Sea`（`action=raw` 全文）** / **`Coral_Sea`（`action=raw` 全文）** | WebFetch | 本次新增两节点的全部依据 |
| `Outland` / `Northrend` | WebFetch | 非 vanilla 大陆定义句 |
| `zh.wikipedia.org/魔兽系列地名列表` | WebFetch ×2（定向查词） | 破碎群岛/赞达拉/库尔提拉斯/巨龙群岛中文句、**「无尽之海」实证**、卡兹阿加查无 |
| `wow.huijiwiki.com/wiki/艾泽拉斯` | WebFetch | **仍是 403**，作者的记录属实 |
| `wowdb.cn/zone-3979.html`（冰封之海） | WebFetch | **无该区域页**，落回站点首页，拿不到中文名 |

**两条能力边界如实记录**：① 本 session 的 **WebSearch 配额同样 200/200 用尽**（与作者同因），
所以「中文官方译名」这条线在本轮依旧无法补强；② `wow.huijiwiki.com` 403 复现，任务规程第 3 条
指定的中文源**本机不可达**，不是没查。

### V.1 逐 quote 的逐字比对结果（规程第 7 条）

**28 个节点全部 `verified_by: ai_read`，没有一个是只凭搜索摘要写的**，无需降级为 `ai_draft`。
逐字对下来，**大部分 quote 与页面原文完全一致**；3 条被作者「清洗」过（删掉了原句里的插入语），
已就地改回原文；另有 1 条引的不是定义句而是网页标题，已换源。

| 节点 | 问题 | 处置 |
|---|---|---|
| `central_kalimdor` | quote 写成 `Central Kalimdor is the central region of...`，页面原文是 `Central Kalimdor, also also spelled as central Kalimdor, is the central region of...`（`also also` 是维基自己的笔误）——**作者那个字符串在页面上并不存在** | 改回原文，含笔误一并保留 |
| `south_seas` | quote 删掉了 `, also known as the South Sea,` 这个同位语 | 改回原文 |
| `veiled_sea` | source_url 指向 `wowdb.cn/zone-457.html`，quote 是 `"迷雾之海 - 卡利姆多 - 区域"`——那是网页 `<title>`，**不是定义句**，不构成 `ai_read` 的依据 | 换成 `warcraft.wiki.gg/wiki/Veiled_Sea` + 其定义句；中文名的 wowdb 出处移进 `note_zh` 保留 |
| `pandaria` | quote 主干 `Pandaria, which had been isolated and shrouded by dense mists during the last 10,000 years.` 在 Geography 节逐字命中；前缀 `to the south the newly discovered landmass of` 是同一句上半段，取源工具多次截断在 125 字符，**未能逐字复现该前缀** | 不改（主干成立），此处留档 |
| `northrend` | quote 用 `...` 连接了同页两句 | 不改，两句均已逐字命中，省略号是显式标注 |
| `kingdom_of_stormwind` | **一度误判**：对渲染页搜 `divided into several territories` 返回 NOT FOUND。改抓 `action=raw&section=29` 后，原句 `The kingdom of Stormwind is divided into several territories, each overseen by local authorities sworn to the [[House of Wrynn]].` **逐字存在**。是渲染页被取源工具截断了 | **作者是对的，未改**。教训：110 KB 以上的页必须按 section 抓原文，渲染页的「查无此句」不可作为否证 |

### V.2 改掉的错（`errors_fixed` 的完整说明）

1. **`quel_thalas` · 版本错置**。`note_zh` 原写「**vanilla 不可进**」，但**本节点自己引的 quote 结尾就是
   `and was accessible in the game`**，且 `Quel'Thalas/Eastern Kingdoms terrain` 页原文写
   `This tower could be found by swimming around from northern Tirisfal Glades, staying close to the shoreline so as not to induce fatigue.`
   ——玩家**能游到**。正确表述是「vanilla 有一块官方命名为 `Quel'thalas` 的封闭 zone，贴岸游可达，但几乎是空地形，
   只有一座进不去的白塔和一个码头」，不是「不可进」。已改 `note_zh`。
   **对下游的影响**：§②.A1 那条裁定的口径要按此理解——**不建其下 zone 的结论不变**（里面确实没有内容可拍），
   但若本剧想要一个「远处白塔 + 无人海岸」的空镜，这块地形在 vanilla 是**真实存在、真能到**的。
2. **`outland` · 邻接写错（归属错误）**。`adjacent` 原写 `[eastern_kingdoms]`。两处不成立：
   ① 黑暗之门是**传送门**，外域与东部王国不接壤，而 `adjacent` 的语义是接壤；
   ② **单向**——`eastern_kingdoms.adjacent` 只有 `[kalimdor]`，没有回填 `outland`，机检一跑就是一处非对称邻接。
   已清空为 `[]`，通路关系保留在 `note_zh`（经诅咒之地的黑暗之门）。
3. **`khaz_algar` · 译名未经核实的音译**。`name_zh` 原写「卡兹阿加」。按规程第 3 条与本文件 §5.5.8
   「查不到就留英文原名 + 标注，绝不自己音译」，三条中文源全部落空（灰机 403 / zh.wikipedia 地名列表**无此词**
   / WebSearch 配额耗尽），已把 `name_zh` 改回英文原名 `Khaz Algar`，候选音译「卡兹阿加」保留在 `note_zh`。
   **§③ 表格里 `khaz_algar` 那一行的 `⚠️ 存疑` 现已落实为「改回英文原名」，以 YAML 为准。**
4. / 5. / 6. quote 三处换回原文或换源，见 §V.1 表（`central_kalimdor`、`south_seas`、`veiled_sea`）。

### V.3 补进去的节点（规程第 1 条「漏掉的子区域，你补进 YAML」）

G01 这一路没有 zone 级节点，所以「Subzones 一节」在本路对应的是**各父页自己列的下一层清单**。
逐页对完，**唯一真实的完整性缺口在水体层**：

`Great_Sea` 页明确枚举了无尽之海的**三个**组成海域，作者只建了其中一个（南海）：

| 补入 | 依据（逐字） | parent | era |
|---|---|---|---|
| `frozen_sea` 冰封之海 | `The Frozen Sea is the large body of water found south of Northrend.` ＋ `Since it is found in between the continents, the Frozen Sea is a portion of the Great Sea.` | `the_great_sea` | **`wotlk`**（zone id 3979 与全部内容都是 3.0；vanilla 不可见，列出只为水体层完整） |
| `coral_sea` 珊瑚之海 | `The Coral Sea is a dark sea near Azshara.` ＋ `Since this sea is found in between the continents, it is a part of the Great Sea.` | `the_great_sea` | `vanilla`（名字最早见于 2003 年 Warcraft RPG；**lore 地名，游戏内无可选中区域**） |

**珊瑚之海对本剧是有用的**：它就在**艾萨拉**外侧，而艾萨拉是 vanilla 45–55 级 zone，
水下是上古之战塌陷的暗夜精灵旧都金萨卡拉（Zin-Azshari）与永恒之井旧址——
艾萨拉海岸线的空镜从此有了可指认的水体名。冰封之海对本剧无用，只为「世界全貌」这一层不留洞。

两个中文名都是**直译**（不是音译），国服官方写法未查到，已在各自 `note_zh` 里写死这一点。

**没有补**的两片：`North Sea`（诺森德东岸与北岸）与 `Storming Sea`——`Great_Sea` 页**没有**把它们
列为无尽之海的组成部分，属于另一层级的水体，按「不确定就不进树」的纪律留在这里备查。

### V.4 核过之后确认作者是对的（一个字没动）

这些都是**实际打开页面核过**的，不是默认通过：

- **`the_great_sea` 的中文名「无尽之海」，作者标 ⚠️ 存疑，现可实证**。
  `zh.wikipedia` 地名列表原句：「东部王国（Eastern Kingdoms）位于无尽之海的西边，由四块次大陆组成。」
  ——**中文名成立**。顺带确认作者 §③ 的另一半判断也对：**这句的方位是错的**
  （英文维基：`The continent lie to the east of the Great Sea`，东部王国在无尽之海**以东**）。
  中文名可用、方位不可用，两件事分开记。`name_zh` 无需改动。
- **`kingdom_of_stormwind` 的领地范围**。`Territory and outposts` 原文逐条列的是：
  艾尔文森林（含暴风城）/ 西部荒野 / 赤脊山 / **荆棘谷** / Balor / 暮色森林 / **逆风小径** /
  **悲伤沼泽（玛什坦岗哨）** / **诅咒之地（守望堡）**，另加洛丹伦、卡利姆多、诺森德的域外前哨。
  → 作者 `note_zh` 的「核心领地＝艾尔文森林/西部荒野/赤脊山/暮色森林/逆风小径，另在荆棘谷/悲伤沼泽/诅咒之地有前哨」
  **与原文逐条对上**；§5.6.B 把 `deadwind_pass` 判给 `kingdom_of_stormwind` 也**有原文支撑**。
- **`azeroth_subcontinent` / `khaz_modan` / `lordaeron` 三块次大陆**的定义句、
  **`stranglethorn`** 的「唯一没被战争毁掉」原句、**`gilneas`** 的格雷迈恩之墙原句——全部逐字命中。
- **三个卡利姆多分区的 zone 归属零漏零多**：`Central_Kalimdor` 页原文只列
  贫瘠之地 / 凄凉之地 / 杜隆塔尔 / 尘泥沼泽 / 莫高雷 / 石爪山脉，与作者 `note_zh` 的六个**完全一致**；
  `Northern_Kalimdor` 页列的 10 个里，秘蓝岛 / 秘血岛（TBC）与海加尔山（Cata）本就不该进，
  剩下 7 个与作者写的 7 个**完全一致**；`Southern_Kalimdor` 的「六大 zone」原句里的奥丹姆是 Cata，作者也正确排除了。
- **等级带（规程第 2 条）**：G01 的 28 个节点全是 world / continent / region，**`level` 一律为空是对的**——
  等级带是 zone 级属性，不该出现在上三层。本路无可核之等级带；§5.2 总表的等级带出自 `Classic_zones`，
  归各片区组在自己那一路核。
- **阵营归属**：`zandalar: horde` / `kul_tiras: alliance` / 两块 vanilla 大陆 `contested` / 水体 `neutral`，
  与 8.0 阵营设定及本文件 §5.1 的口径一致。
- **无 id 重复、无悬空 parent、28 个节点 16 个字段一个不缺**（本轮用 `yaml.safe_load` 实机跑过）。

### V.5 复核过但**维持原判**的三处（不是漏看）

1. **`the_plaguelands` 没有建成 region 节点**（§③.5）。核实：`Lordaeron` 页的子分区树里
   **确实有 `The Plaguelands` 这一层**，东/西瘟疫之地挂在它下面。所以这是一个**有维基依据**的可建层。
   **但仍维持不建**——作者在 §③.4/§③.5 给了理由（避免下游不知道写哪个 parent），
   且 G06/G07 已按 `parent: lordaeron` 落盘。核验员的职责是补全与收紧，不是推翻有记录的取舍。
   **若合龙时改主意**：加一个 `the_plaguelands`（parent `lordaeron`）并同步改 §5.2 里那两行的 parent 即可，其余不动。
2. **`broken_isles` / `zandalar` / `kul_tiras` / `dragon_isles` 的 `type` 写成 `continent`**。
   `Azeroth` 页原话是 **`The islands of Zandalar, Kul Tiras, the Broken Isles...`——是 islands 不是 continents**。
   严格说这是个 type 近似。**维持不改**：§5.1 的 type 枚举里没有 `island`，而这四块在游戏里各自是独立大地图，
   降成 `region` 会更失真。已在此留档，下游不要据此以为它们在 lore 里是大陆。
3. **`outland` 的 parent 挂 `azeroth`**（§③.6）。外域确实不在艾泽拉斯星球上，这是作者明写的妥协。
   顺带核实：**德拉诺（6.0）、阿古斯（7.3）、暗影界（9.0）同样没进树**——它们与外域同类（异界），
   但只有外域因为「黑暗之门在诅咒之地、是 vanilla 地图上真实可见的建筑」而有理由出现。维持现状，此处备查。

### V.6 仍然存疑、下游必须自己解决的

1. **中文官方译名这条线整体没补强**。灰机 403 复现、WebSearch 两个 session 都是 200/200 用尽。
   目前仍挂 ⚠️ 的：`forbidding_sea` 禁忌之海 / `south_seas` 南海 / `northern·central·southern_kalimdor` 北中南卡利姆多 /
   本轮新增的 `frozen_sea` 冰封之海 / `coral_sea` 珊瑚之海——**全是直译、不是音译，可用但未经官方源确认**；
   `khaz_algar` 已按规则改回英文原名。**唯一可靠的解法是开国服客户端逐个对**，不要再在网上找了。
2. **`pandaria` quote 的前缀**未能逐字复现（见 §V.1），主干成立。若要 100% 干净，
   把 quote 缩到 `Pandaria, which had been isolated and shrouded by dense mists during the last 10,000 years.` 即可。
3. **§5.2 的 47 个 vanilla zone 总表本轮没有逐 zone 复核**——那是 G02–G13 各自那一路的核验范围。
   本路只核了它们的 **parent 归属口径**（次大陆层 / 王国层 / 分区层），口径成立。
