# 悲伤沼泽（Swamp of Sorrows）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg303_悲伤沼泽全境/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/eastern_kingdoms/swamp_of_sorrows/`（东部王国 → 悲伤沼泽），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 地区 · 35-45 级 · contested |
| 相邻 | 诅咒之地 · 逆风小径 |
| 世界地图尺寸 | 2097.4 × 1398.3 m（坐标表：WorldMapArea：2293.8 × 1529.2 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 终年阴雨的墨绿沼泽，枯死的巨树从齐腰浑水里立起，树冠垂满苔须，水面浮着绿藻与气泡，天光始终是铅灰色 |
| 备注 | 旧世的悲伤沼泽比 4.0.3 后更荒凉、几乎无人烟；绿龙眷族巡守于此 |
| 出处 | https://warcraft.wiki.gg/wiki/Swamp_of_Sorrows_(Classic) |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-SwampofSorrows_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/eastern_kingdoms/swamp_of_sorrows/WorldMap-SwampofSorrows_c60.jpg`


## 区级场地平面图

`bg303_悲伤沼泽全境/planning/bg303_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（14 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg303** | [悲伤沼泽全境](bg303_悲伤沼泽全境/bg303_悲伤沼泽全境.md) | 自造 | — |  |
| **bg304** | [农田避难所](bg304_农田避难所/bg304_农田避难所.md) | 聚居点 · village | — | 荒废的农田与残垣，泥水漫过田埂，失落者搭的简陋窝棚散在田间，木栅东倒西歪 |
| **bg305** | [芦苇岗哨](bg305_芦苇岗哨/bg305_芦苇岗哨.md) | 聚居点 · camp | — | 东岸滩头的小木哨所，苇丛齐肩，栈道通向水边，哨所顶上一盏未点的油灯 |
| **bg306** | [断矛路口](bg306_断矛路口/bg306_断矛路口.md) | 聚居点 · crossroads | — | 沼泽中的泥路交汇点，路中央插着一支折断的长矛做路标，四面都是齐腰水草 |
| **bg307** | [斯通纳德](bg307_斯通纳德/bg307_斯通纳德.md) | 聚居点 · town | [46, 55] | 沼泽高地上的兽人要塞，粗木与兽皮搭的圆顶大厅，两座土制地穴入口，红旗插在泥岸边，四周是死水与枯木 |
| **bg308** | [避难营](bg308_避难营/bg308_避难营.md) | 聚居点 · village | — | 沼泽西侧的小村落，几间草顶棚屋围着一堆篝火，木桩上晾着破布，四周积水没过脚踝 |
| **bg309** | [伊萨里奥斯的洞穴](bg309_伊萨里奥斯的洞穴/bg309_伊萨里奥斯的洞穴.md) | 子区域 | — | 藏在崖壁后的干燥洞窟，洞内比外面亮，一条绿龙化身盘踞在中央，鳞片泛着翡翠光 |
| **bg310** | [芦苇海滩](bg310_芦苇海滩/bg310_芦苇海滩.md) | 子区域 | — | 悲伤沼泽东侧的泥沙海滩，成片高芦苇被风压出波纹，浅水里埋着鱼人的贝壳窝 |
| **bg311** | [迷雾谷](bg311_迷雾谷/bg311_迷雾谷.md) | 子区域 | — | 被岩壁夹住的狭长谷地，浓雾贴地不散，枯树只剩黑色剪影，能见度不足十步 |
| **bg312** | [泪水之池](bg312_泪水之池/bg312_泪水之池.md) | 子区域 | — | 沼泽东部的大片深水湖，水色近黑，湖心隐约露出淹没神庙的尖顶与破损石阶 |
| **bg313** | [忧伤湿地](bg313_忧伤湿地/bg313_忧伤湿地.md) | 子区域 | — | 北部最深的黑水区，水几乎没胸，死树成排站在雾里，水面漂着一层油亮的膜 |
| **bg314** | [雄鹿沼泽](bg314_雄鹿沼泽/bg314_雄鹿沼泽.md) | 子区域 | — | 南部的浅水湿地，成片的睡莲与浮草，水下能看到游动的鳄鱼背脊 |
| **bg315** | [荒芜之海](bg315_荒芜之海/bg315_荒芜之海.md) | 子区域 | — | 沼泽东侧的灰绿海面，天色压得很低，浪不大但颜色浑浊，看不到对岸 |
| **bg316** | [流沙泥潭](bg316_流沙泥潭/bg316_流沙泥潭.md) | 子区域 | — | 一片会吞人的灰褐泥沼，表面结着薄壳，踩下去咕嘟冒泡，枯枝从泥里斜插出来 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 阿塔哈卡神庙（`temple_of_atal_hakkar` · dungeon）
- 阿塔哈卡神庙入口（`temple_of_atal_hakkar_entrance` · 地标） → 属 泪水之池
- 雄鹿沼泽洞穴（`stagalbog_cave` · 子区域） → 属 雄鹿沼泽
- 斯通纳德飞行点（`fp_stonard` · transport · flightpath） → 属 斯通纳德
- 斯通纳德飞行点（`stonard_flightpath` · transport · flightpath） → 属 斯通纳德
- 阿塔拉利恩（`atalalarion` · 地标） → 属 阿塔哈卡神庙
- 哈卡的化身（`avatar_of_hakkar` · 地标） → 属 阿塔哈卡神庙
- 德姆塞卡尔与德拉维沃尔（`dreamscythe_and_weaver` · 地标） → 属 阿塔哈卡神庙
- 预言者迦玛兰（`jammalan_the_prophet` · 地标） → 属 阿塔哈卡神庙
- 摩弗拉斯和哈扎斯（`morphaz_and_hazzas` · 地标） → 属 阿塔哈卡神庙
- 伊兰尼库斯的阴影（`shade_of_eranikus` · 地标） → 属 阿塔哈卡神庙
- 鲜血之厅（`st_chamber_of_blood` · 子区域） → 属 阿塔哈卡神庙
- 沉睡者之厅（`st_chamber_of_the_dreamer` · 子区域） → 属 阿塔哈卡神庙
- 召唤者之穴（`st_den_of_the_caller` · 子区域） → 属 阿塔哈卡神庙
- 白骨大厅（`st_hall_of_bones` · 子区域） → 属 阿塔哈卡神庙
- 面具大厅（`st_hall_of_masks` · 子区域） → 属 阿塔哈卡神庙
- 仪式大厅（`st_hall_of_ritual` · 子区域） → 属 阿塔哈卡神庙
- 毒蛇大厅（`st_hall_of_serpents` · 子区域） → 属 阿塔哈卡神庙
- 诅咒大厅（`st_hall_of_the_cursed` · 子区域） → 属 阿塔哈卡神庙
- 天选者之巢（`st_lair_of_the_chosen` · 子区域） → 属 阿塔哈卡神庙
- 堕神圣地（`st_sanctum_of_the_fallen_god` · 子区域） → 属 阿塔哈卡神庙
- 破碎大厅（`st_the_broken_hall` · 子区域） → 属 阿塔哈卡神庙
- 屠宰房（`st_the_butchery` · 子区域） → 属 阿塔哈卡神庙
- 抛弃之池（`st_the_pit_of_refuse` · 子区域） → 属 阿塔哈卡神庙
- 牺牲之池（`st_the_pit_of_sacrifice` · 子区域） → 属 阿塔哈卡神庙
