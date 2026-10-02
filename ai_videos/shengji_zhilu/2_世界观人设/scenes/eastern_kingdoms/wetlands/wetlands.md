# 湿地（Wetlands）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg401_湿地全境/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/eastern_kingdoms/wetlands/`（东部王国 → 湿地），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 地区 · 20-30 级 · contested |
| 相邻 | 洛克莫丹 · 阿拉希高地 · 尘泥沼泽 · 黑海岸 |
| 世界地图尺寸 | 3781.4 × 2520.3 m（坐标表：WorldMapArea：4135.4 × 2756.2 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 常年灰绿的低地沼泽，浅水塘与泥路交错，枯瘦的湿地乔木举着稀疏树冠，天色总是阴的，远处东边压着一座黑色山堡 |
| 备注 | 三面环山、西面开向大海；北经萨多尔大桥去阿拉希高地，南经丹奥加兹回洛克莫丹，米奈希尔港的船通塞拉摩与奥伯丁。旧世本区无夜精灵据点（绿色守护者之林等是 4.0.3 新增） |
| 出处 | https://warcraft.wiki.gg/wiki/Wetlands |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-Wetlands_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/eastern_kingdoms/khaz_modan/wetlands/WorldMap-Wetlands_c60.jpg`


## 区级场地平面图

`bg401_湿地全境/planning/bg401_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（12 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg401** | [湿地全境](bg401_湿地全境/bg401_湿地全境.md) | 自造 | — |  |
| **bg402** | [丹莫德](bg402_丹莫德/bg402_丹莫德.md) | 聚居点 · town | [46, 16] | 北端路边一小片石砌矮人聚落，屋顶破损、墙上留着烟熏痕，街上走动的是穿黑甲的黑铁矮人，炉火烧成暗红 |
| **bg403** | [米奈希尔港](bg403_米奈希尔港/bg403_米奈希尔港.md) | 聚居点 · port | [11, 55] | 建在沼泽尽头小岛上的石墙港镇，四座方塔拱着中央城堡，木栈桥伸进灰绿海水，桅杆与帆影挤在码头边 |
| **bg404** | [怒牙营地](bg404_怒牙营地/bg404_怒牙营地.md) | 子区域 | [46, 46] | 泥地上一圈尖木桩围起的兽人营，红黑兽皮帐篷、铁架火盆，营中央竖着龙喉氏族的旗与兽骨柱 |
| **bg405** | [黑水沼泽](bg405_黑水沼泽/bg405_黑水沼泽.md) | 子区域 | [20, 50] | 水色发墨的一片深沼，水面浮着油亮的黑膜，枯树根盘出水面，几乎没有光进得去 |
| **bg406** | [蓝腮沼泽](bg406_蓝腮沼泽/bg406_蓝腮沼泽.md) | 子区域 | [20, 35] | 西北一片浅水滩涂，泥岸上插着鱼人用的骨制尖桩与草棚，水面漂着成片浮萍 |
| **bg407** | [恶铁岭](bg407_恶铁岭/bg407_恶铁岭.md) | 子区域 | [63, 36] | 东北一座裸岩小丘，坡上支着黑铁矮人的铁棚与熔炉，炉口喷着暗红火，坡面被熏得焦黑 |
| **bg408** | [藓皮沼泽](bg408_藓皮沼泽/bg408_藓皮沼泽.md) | 子区域 | [63, 58] | 东南一片长满厚苔的湿林，树干裹着绿毛，地面软塌，豺狼人的草窝散在树根之间 |
| **bg409** | [恐龙岭](bg409_恐龙岭/bg409_恐龙岭.md) | 子区域 | [72, 38] | 东侧一片高地岩坡，地上散着蛋壳与啃净的骨头，岩缝间能看到成群迅猛龙来回巡走 |
| **bg410** | [盐沫沼泽](bg410_盐沫沼泽/bg410_盐沫沼泽.md) | 子区域 | [34, 24] | 北岸靠海的一段谷地，风大、草伏，海雾常年不散，地表结着一层白色盐霜 |
| **bg411** | [日落沼泽](bg411_日落沼泽/bg411_日落沼泽.md) | 子区域 | [24, 30] | 西北的开阔湿草甸，水洼一块接一块反着灰天，几丛高草和枯木立在水中 |
| **bg412** | [绿带草地](bg412_绿带草地/bg412_绿带草地.md) | 子区域 | [55, 37] | 湿地中部少见的一条干爽草带，草色偏亮绿，几株高大的阔叶树成行立着，像一条穿过沼泽的绿色缓坡 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 巴拉丁海湾（`baradin_bay` · 地标）
- 龙喉大门（`dragonmaw_gates` · 地标）
- 丹奥加兹（`dun_algaz_wetlands` · 地标）
- 铁须之墓（`ironbeards_tomb` · 地标）
- 米奈希尔海湾（`menethil_bay` · 地标）
- 萨多尔大桥（`thandol_span` · 地标）
- 禁忌之海（`the_forbidding_sea_wetlands` · 地标）
- 无尽之海（`the_great_sea_wetlands` · 地标）
- 瑟根石（`thelgen_rock` · 地标）
- 维尔加挖掘场（`whelgars_excavation_site` · 地标）
- 失落的舰队（`the_lost_fleet` · 地标） → 属 巴拉丁海湾
- 格瑞姆巴托（`grim_batol` · 地标） → 属 龙喉大门
- 深水旅店（`deepwater_tavern` · 聚居点 · inn） → 属 米奈希尔港
- 米奈希尔港·奥伯丁航线码头（`dock_menethil_to_auberdine` · transport · boat） → 属 米奈希尔港
- 米奈希尔港·塞拉摩航线码头（`dock_menethil_to_theramore` · transport · boat） → 属 米奈希尔港
- 米奈希尔港飞行点（`fp_menethil_harbor` · transport · flightpath） → 属 米奈希尔港
- 米奈希尔港码头（往奥伯丁）（`menethil_dock_auberdine` · transport · boat） → 属 米奈希尔港
- 米奈希尔港码头（往塞拉摩）（`menethil_dock_theramore` · transport · boat） → 属 米奈希尔港
- 米奈希尔港狮鹫场（`menethil_gryphon_roost` · transport · flightpath） → 属 米奈希尔港
- 米奈希尔城堡（`menethil_keep` · 地标） → 属 米奈希尔港
