# 凄凉之地（Desolace）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg502_凄凉之地全境/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/kalimdor/desolace/`（卡利姆多 → 凄凉之地），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 地区 · 30-40 级 · contested |
| 相邻 | 石爪山脉 · 菲拉斯 |
| 世界地图尺寸 | 4111 × 2741.3 m（坐标表：WorldMapArea：4495.8 × 2997.9 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 一整片灰白到土灰色的干裂荒原，枯死的白树只剩枝杈，遍地是风化的科多兽头骨，天光总是发灰发暗 |
| 备注 | 旧世 30-40 级的争夺区，原名玛珊'舍；北接石爪山脉、南接菲拉斯，西临迷雾之海。半人马各部族的家园，燃烧之刃邪教也在此活动 |
| 出处 | https://warcraft.wiki.gg/wiki/Desolace |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-Desolace_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/kalimdor/central_kalimdor/desolace/WorldMap-Desolace_c60.jpg`
- `ref/WorldMap-MicroDungeon-Desolace-MaraudonOutside.jpg.link.json` → 微型地下城图
- `ref/WorldMap-MicroDungeon-Desolace-MaraudonOutside1.jpg.link.json` → 微型地下城图

## 区级场地平面图

`bg502_凄凉之地全境/planning/bg502_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（21 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg502** | [凄凉之地全境](bg502_凄凉之地全境/bg502_凄凉之地全境.md) | 自造 | — |  |
| **bg503** | [断矛村](bg503_断矛村/bg503_断矛村.md) | 聚居点 · village | — | 荒原上一处被打烂的半人马营地，帐篷塌了一半，折断的长矛插在土里 |
| **bg504** | [吉尔吉斯村](bg504_吉尔吉斯村/bg504_吉尔吉斯村.md) | 聚居点 · village | [35, 81] | 西南一圈沿着大裂谷边缘搭起的半人马村落，谷底的崖台之间用吊桥相连，帐篷挂在崖边 |
| **bg505** | [幽灵岗哨](bg505_幽灵岗哨/bg505_幽灵岗哨.md) | 聚居点 · camp | — | 荒原正中一小片牛头人营地，几顶灰褐兽皮帐围着一堆火，帐外插着招魂布条，四周一览无遗、毫无遮蔽 |
| **bg506** | [科尔卡村](bg506_科尔卡村/bg506_科尔卡村.md) | 聚居点 · village | — | 东缘一小片半人马营地，帐篷破旧、拴马桩东倒西歪，有被洗劫过的痕迹 |
| **bg507** | [考米克小屋](bg507_考米克小屋/bg507_考米克小屋.md) | 聚居点 · camp | [62, 39] | 荒原中部一座孤零零的破木屋，屋外一圈木栅围着散落骨头的空地 |
| **bg508** | [玛格拉姆村](bg508_玛格拉姆村/bg508_玛格拉姆村.md) | 聚居点 · village | — | 东南几汪发黄的污水塘与塘中小岛，粗糙的木桥把岛连起来，半人马的兽皮帐搭在岛上与岸边 |
| **bg509** | [尼耶尔前哨站](bg509_尼耶尔前哨站/bg509_尼耶尔前哨站.md) | 聚居点 · town | — | 北部山口上的联盟营地，石砌矮墙围着几座木屋与蓝白帐篷，塞纳里奥议会的绿色旗与联盟旗并排 |
| **bg510** | [瑟卡布斯库的营地](bg510_瑟卡布斯库的营地/bg510_瑟卡布斯库的营地.md) | 聚居点 · camp | [61, 62] | 坟场边一顶小小的哥布林帐篷与一辆停着的科多兽拉车，车边堆着捆好的骨料 |
| **bg511** | [葬影村](bg511_葬影村/bg511_葬影村.md) | 聚居点 · port | [26, 75] | 海边一排高脚木桩托起的巨魔棚屋，屋前伸出几条窄栈桥直入海水，晾渔网与骨制风铃挂在檐下 |
| **bg512** | [雷斧堡垒](bg512_雷斧堡垒/bg512_雷斧堡垒.md) | 聚居点 · ruin | — | 西北荒原上一座半塌的石砌堡垒，几处常燃的火堆在断墙间跳动，燃烧之刃的黑色刀旗插在垛口上 |
| **bg513** | [艾瑟雷索](bg513_艾瑟雷索/bg513_艾瑟雷索.md) | 子区域 | [41, 31] | 西北海边一片大半沉在水下的暗夜精灵废墟，只剩一座孤塔立在水上，一道小石桥通向塔那扇封死的门 |
| **bg514** | [科多兽坟场](bg514_科多兽坟场/bg514_科多兽坟场.md) | 子区域 | — | 满地都是巨大的科多兽白骨与半埋的头骨，肋骨拱成一座座天然的骨架棚，地面是灰白的骨屑 |
| **bg515** | [玛诺洛克集会所](bg515_玛诺洛克集会所/bg515_玛诺洛克集会所.md) | 子区域 | — | 一片被邪能二次烧过的暗夜精灵废墟，断柱间浮着绿色的邪能雾，空气一进入就压得人发闷 |
| **bg516** | [拉纳加尔岛](bg516_拉纳加尔岛/bg516_拉纳加尔岛.md) | 子区域 | [28, 8] | 西北外海一座多岩小岛，岛上散着暗夜精灵废墟的残柱，地上横着被杀的纳迦尸体 |
| **bg517** | [萨格隆](bg517_萨格隆/bg517_萨格隆.md) | 子区域 | [74, 28] | 东北一片倒塌的暗夜精灵城市废墟，紫白断柱斜插在灰土里，仇恨之刃萨特在残垣间游荡 |
| **bg518** | [萨瑟里斯海岸](bg518_萨瑟里斯海岸/bg518_萨瑟里斯海岸.md) | 子区域 | — | 凄凉之地的整条西海岸，与内陆的灰枯相反，这里阳光充足、有成片的绿草铺到沙滩 |
| **bg519** | [破影峡谷](bg519_破影峡谷/bg519_破影峡谷.md) | 子区域 | [79, 78] | 东南山中一条藏得很深的峡谷，谷里立着几丛巨型蘑菇与一圈拖着巨链的召唤法阵 |
| **bg520** | [塔迪萨兰](bg520_塔迪萨兰/bg520_塔迪萨兰.md) | 子区域 | [54, 14] | 北部荒原上一串低矮的暗夜精灵断墙与倒柱，没有任何人烟，只有野兽在废墟间穿行 |
| **bg521** | [白骨之谷](bg521_白骨之谷/bg521_白骨之谷.md) | 子区域 | — | 南缘一道石崖夹出的窄谷，两侧崖壁下瘫着两具巨大到不成比例的骸骨，谷中骷髅与鬼火飘动 |
| **bg522** | [长矛谷](bg522_长矛谷/bg522_长矛谷.md) | 子区域 | [33, 57] | 西部一条被石壁夹住的谷地，谷中插满半人马的图腾长矛与骨幡，帐篷沿谷壁一排排搭着 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 迷雾之海（`veiled_sea_desolace` · 地标）
- 波尔甘的洞穴（`bolgans_hole` · 地标） → 属 吉尔吉斯村
- 尼耶尔前哨站飞行点（`fp_nijels_point` · transport · flightpath） → 属 尼耶尔前哨站
- 尼耶尔前哨站飞行点（`nijels_point_flightpath` · transport · flightpath） → 属 尼耶尔前哨站
- 葬影村飞行点（`fp_shadowprey_village` · transport · flightpath） → 属 葬影村
- 葬影村飞行点（`shadowprey_flightpath` · transport · flightpath） → 属 葬影村
- 玛拉顿（`maraudon` · dungeon） → 属 长矛谷
- 被诅咒的塞雷布拉斯（`celebras_the_cursed` · 地标） → 属 玛拉顿
- 大地之歌瀑布（`earth_song_falls` · 子区域） → 属 玛拉顿
- 污臭洞穴（`foulspore_cavern` · 子区域） → 属 玛拉顿
- 兰斯利德（`landslide` · 地标） → 属 玛拉顿
- 维利塔恩（`lord_vyletongue` · 地标） → 属 玛拉顿
- 琥珀碎片洞穴（`maraudon_ambershard_cavern` · 子区域） → 属 玛拉顿
- 地歌瀑布入口（`maraudon_earth_song_falls_entrance` · 地标） → 属 玛拉顿
- 橙水晶入口（`maraudon_orange_crystal_entrance` · 地标） → 属 玛拉顿
- 毒水瀑布（`maraudon_poison_falls` · 子区域） → 属 玛拉顿
- 紫水晶入口（`maraudon_purple_crystal_entrance` · 地标） → 属 玛拉顿
- 暗影碎片洞穴（`maraudon_shadowshard_cavern` · 子区域） → 属 玛拉顿
- 五可汗神殿（`maraudon_shrine_of_the_five_khans` · 子区域） → 属 玛拉顿
- 毒水谷（`maraudon_the_noxious_hollow` · 子区域） → 属 玛拉顿
- 草藤之座（`maraudon_vyletongue_seat` · 子区域） → 属 玛拉顿
- 扎尔塔之墓（`maraudon_zaetars_grave` · 子区域） → 属 玛拉顿
- 诺克赛恩（`noxxion` · 地标） → 属 玛拉顿
- 瑟莱德丝公主（`princess_theradras` · 地标） → 属 玛拉顿
- 锐刺鞭笞者（`razorlash` · 地标） → 属 玛拉顿
- 洛特格里普（`rotgrip` · 地标） → 属 玛拉顿
- 工匠吉兹洛克（`tinkerer_gizlock` · 地标） → 属 玛拉顿
- 邪恶洞穴（`wicked_grotto` · 子区域） → 属 玛拉顿
