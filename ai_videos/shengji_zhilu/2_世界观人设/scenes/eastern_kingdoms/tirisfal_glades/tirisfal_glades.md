# 提瑞斯法林地（Tirisfal Glades）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg338_提瑞斯法林地全境/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/eastern_kingdoms/tirisfal_glades/`（东部王国 → 提瑞斯法林地），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 地区 · 1-10 级 · horde |
| 相邻 | 银松森林 · 西瘟疫之地 |
| 世界地图尺寸 | 4131.9 × 2754.6 m（坐标表：WorldMapArea：4518.8 × 3012.5 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 病绿色天光下的橡木疏林与枯黄草坡，贴地白雾，石篱笆、歪斜墓碑与被瘟疫熏黑的农舍散落其间 |
| 备注 | 亡灵新手区；洛丹伦王国旧都所在地，被遗忘者的地盘。4.0.3 未大改，但 BfA 洛丹伦之战后布瑞尔与幽暗城被毁，本树取 vanilla 状态 |
| 出处 | https://warcraft.wiki.gg/wiki/Tirisfal_Glades |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-Tirisfal_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/eastern_kingdoms/lordaeron/tirisfal_glades/WorldMap-Tirisfal_c60.jpg`
- `ref/WorldMap-MicroDungeon-Tirisfal-KeepersRest.jpg.link.json` → 微型地下城图
- `ref/WorldMap-MicroDungeon-Tirisfal-ScarletMonasteryEntrance.jpg.link.json` → 微型地下城图

## 区级场地平面图

`bg338_提瑞斯法林地全境/planning/bg338_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（22 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg338** | [提瑞斯法林地全境](bg338_提瑞斯法林地全境/bg338_提瑞斯法林地全境.md) | 自造 | — |  |
| **bg339** | [阿加曼德磨坊](bg339_阿加曼德磨坊/bg339_阿加曼德磨坊.md) | 聚居点 · farm | [46, 37] | 山坡上的木制风车与谷仓群，风车叶片还在空转，坡下一片翻开的家族墓地 |
| **bg340** | [巴尼尔农场](bg340_巴尼尔农场/bg340_巴尼尔农场.md) | 聚居点 · farm | [74, 62] | 东部缓坡上的完整农舍与围栏，马匹散步，是提瑞斯法少见的「还像活人住处」的地方 |
| **bg341** | [布瑞尔](bg341_布瑞尔/bg341_布瑞尔.md) | 聚居点 · town | [60, 57] | 十字路口上的一圈木石小屋，屋顶压着茅草，中间一座尖顶钟楼，路面是湿泥 |
| **bg342** | [炉灰庄园](bg342_炉灰庄园/bg342_炉灰庄园.md) | 聚居点 · ruin | [55, 59] | 烧空的庄园宅子，只剩焦黑梁架与半截烟囱，院里散着家具残骸 |
| **bg343** | [十字军前哨](bg343_十字军前哨/bg343_十字军前哨.md) | 聚居点 · camp | [78, 53] | 红白十字旗的帆布营帐与木栅，篝火边架着长枪 |
| **bg344** | [十字军前哨](bg344_十字军前哨（南）/bg344_十字军前哨（南）.md) | 聚居点 · tower | — | 幽暗城西侧下水道出口附近一座半塌的石砌哨塔，塔身缺了一角、爬满枯藤，塔下几顶红帆布帐篷与一架望台正对着城门方向。 |
| **bg345** | [十字军前哨](bg345_十字军前哨（西）/bg345_十字军前哨（西）.md) | 聚居点 · tower | [34, 48] | 索利丹农场西侧一座孤立的木石哨塔，塔顶挑着血色十字军的红旗，塔脚拴着马、堆着补给箱，四周是荒了一半的南瓜田。 |
| **bg346** | [丧钟镇](bg346_丧钟镇/bg346_丧钟镇.md) | 聚居点 · village | [35, 64] | 灰白雾气锁住的小山谷，半塌的木屋与一座石砌小教堂，墓地就在村口，土是翻开的 |
| **bg347** | [加伦鬼屋](bg347_加伦鬼屋/bg347_加伦鬼屋.md) | 聚居点 · ruin | [58, 38] | 荒废的农舍与畜栏，木料发黑，院中立着稻草人 |
| **bg348** | [洛丹伦废墟](bg348_洛丹伦废墟/bg348_洛丹伦废墟.md) | 聚居点 · ruin | — | 巨大的白石王宫外墙已成焦黑残垣，庭院裂开，断柱间飘着幽灵，正门后是通往地下的升降梯 |
| **bg349** | [血色十字军哨岗](bg349_血色十字军哨岗/bg349_血色十字军哨岗.md) | 聚居点 · tower | [77, 34] | 林间一座石砌方塔，塔顶挂血色十字军红旗，塔下扎着两顶帐篷 |
| **bg350** | [索利丹农场](bg350_索利丹农场/bg350_索利丹农场.md) | 聚居点 · farm | [37, 49] | 西部海边的一组农舍与麦垛，田埂荒了一半 |
| **bg351** | [亡灵壁垒](bg351_亡灵壁垒/bg351_亡灵壁垒.md) | 聚居点 · camp | [81, 70] | 用碎石、断木与尸骨垒起的横向路障墙，两侧插满尖桩，墙后是黄灰色的瘟疫雾 |
| **bg352** | [Mass Graves](bg352_Mass-Graves/bg352_Mass-Graves.md) | 子区域 | — | 林间一片被翻开的乱葬岗，成排的浅坑与歪倒的木牌，土堆上散着骨头和破布，豺狼人在坑边刨土。 |
| **bg353** | [噩梦谷](bg353_噩梦谷/bg353_噩梦谷.md) | 子区域 | [48, 67] | 低洼谷地，遍地沼泽色的软泥与枯藤，雾比别处更厚 |
| **bg354** | [休息区](bg354_休息区/bg354_休息区.md) | 子区域 | — | 修道院前的石砌平台与阶梯，两侧立着圣光雕像 |
| **bg355** | [无尽之海](bg355_无尽之海/bg355_无尽之海.md) | 子区域 | — | 提瑞斯法北岸外铅灰色的开阔海面，浪头短而碎，远处水天一色没有地平线，近岸礁石上挂着海藻和腐烂的鱼。 |
| **bg356** | [北部海岸](bg356_北部海岸/bg356_北部海岸.md) | 子区域 | — | 灰黑色卵石海滩与断崖，浪打礁石，天色铅灰 |
| **bg357** | [毒蛛峡谷](bg357_毒蛛峡谷/bg357_毒蛛峡谷.md) | 子区域 | [87, 47] | 山谷两壁拉满灰白蛛网，树干上挂着裹尸茧，地面爬满蜘蛛 |
| **bg358** | [耳语花园](bg358_耳语花园/bg358_耳语花园.md) | 子区域 | [85, 33] | 修道院围墙外的整齐花园与石径，修剪过的树篱在瘟疫天光下显得不合时宜 |
| **bg359** | [耳语海岸](bg359_耳语海岸/bg359_耳语海岸.md) | 子区域 | — | 东北角的砂砾海岸，风从海上来，草被压成一个方向 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 澈水湖（`brightwater_lake` · 地标）
- 法奥之墓（`faols_rest` · 地标）
- 静水池（`stillwater_pond` · 地标）
- 提瑞斯法林地飞艇塔（幽暗城外）（`zeppelin_tower_tirisfal` · transport · boat）
- 阿加曼德家族墓穴（`agamand_family_crypt` · 子区域） → 属 阿加曼德磨坊
- 冈瑟尔的居所（`gunthers_retreat` · 地标） → 属 澈水湖
- 布瑞尔铁匠铺（`brill_blacksmith` · 地标） → 属 布瑞尔
- 布瑞尔城镇大厅（`brill_town_hall` · 地标） → 属 布瑞尔
- 恐惧之末旅店（`gallows_end_tavern` · 聚居点 · inn） → 属 布瑞尔
- 丧钟镇教堂（`deathknell_chapel` · 地标） → 属 丧钟镇
- 夜行蜘蛛洞穴（`night_webs_hollow` · 子区域） → 属 丧钟镇
- 灰影墓穴（`shadow_grave` · 子区域） → 属 丧钟镇
- 洛丹伦王座厅（`lordaeron_throne_room` · 地标） → 属 洛丹伦废墟
- 幽暗城升降梯（`undercity_elevators` · 地标） → 属 洛丹伦废墟
- 幽暗城飞艇平台（`undercity_zeppelin_towers` · transport · flightpath） → 属 洛丹伦废墟
- 血色修道院（`scarlet_monastery` · dungeon） → 属 耳语花园
- 提瑞斯法塔·格罗姆高飞艇位（`zeppelin_berth_tirisfal_to_gromgol` · transport · boat） → 属 提瑞斯法林地飞艇塔（幽暗城外）
- 提瑞斯法塔·奥格瑞玛飞艇位（`zeppelin_berth_tirisfal_to_orgrimmar` · transport · boat） → 属 提瑞斯法林地飞艇塔（幽暗城外）
- 血色修道院军械库（`sm_armory` · dungeon） → 属 血色修道院
- 血色修道院大教堂（`sm_cathedral` · dungeon） → 属 血色修道院
- 大前厅（`sm_grand_vestibule` · 子区域） → 属 血色修道院
- 血色修道院墓地（`sm_graveyard` · dungeon） → 属 血色修道院
- 血色修道院图书馆（`sm_library` · dungeon） → 属 血色修道院
- 赫洛德（`herod` · 地标） → 属 血色修道院军械库
- 十字军武器库（`sm_crusaders_armory` · 子区域） → 属 血色修道院军械库
- 步兵武器库（`sm_footmans_armory` · 子区域） → 属 血色修道院军械库
- 勇士大厅（`sm_hall_of_champions` · 子区域） → 属 血色修道院军械库
- 训练场（`sm_training_grounds` · 子区域） → 属 血色修道院军械库
- 大检察官法尔班克斯（`high_inquisitor_fairbanks` · 地标） → 属 血色修道院大教堂
- 大检察官怀特迈恩（`high_inquisitor_whitemane` · 地标） → 属 血色修道院大教堂
- 血色十字军指挥官莫格莱尼（`scarlet_commander_mograine` · 地标） → 属 血色修道院大教堂
- 教堂花园（`sm_chapel_gardens` · 子区域） → 属 血色修道院大教堂
- 十字军礼拜堂（`sm_crusaders_chapel` · 子区域） → 属 血色修道院大教堂
- Azshir the Sleepless（`azshir_the_sleepless` · 地标） → 属 血色修道院墓地
- 血法师萨尔诺斯（`bloodmage_thalnos` · 地标） → 属 血色修道院墓地
- Fallen Champion（`fallen_champion` · 地标） → 属 血色修道院墓地
- 审讯员韦沙斯（`interrogator_vishas` · 地标） → 属 血色修道院墓地
- Ironspine（`ironspine` · 地标） → 属 血色修道院墓地
- 忏悔室（`sm_chamber_of_atonement` · 子区域） → 属 血色修道院墓地
- 遗忘回廊（`sm_forlorn_cloister` · 子区域） → 属 血色修道院墓地
- 荣耀之墓（`sm_honors_tomb` · 子区域） → 属 血色修道院墓地
- 奥法师杜安（`arcanist_doan` · 地标） → 属 血色修道院图书馆
- 驯犬者洛克希（`houndmaster_loksey` · 地标） → 属 血色修道院图书馆
- 图书馆（`sm_athenaeum` · 子区域） → 属 血色修道院图书馆
- 珍宝陈列室（`sm_gallery_of_treasures` · 子区域） → 属 血色修道院图书馆
- 猎手回廊（`sm_huntsmans_cloister` · 子区域） → 属 血色修道院图书馆
