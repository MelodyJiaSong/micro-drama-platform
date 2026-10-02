# 奥特兰克山脉（Alterac Mountains）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg23_奥特兰克山脉全境/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/eastern_kingdoms/alterac_mountains/`（东部王国 → 奥特兰克山脉），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 地区 · 30-40 级 · contested |
| 相邻 | 希尔斯布莱德丘陵 · 西瘟疫之地 · 辛特兰 |
| 世界地图尺寸 | 2560.3 × 1706.9 m（坐标表：WorldMapArea：2800.0 × 1866.7 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 灰白积雪的高山与裸岩隘口，冷蓝天光，山脚是灰绿湖岸与枯树，雪地上是废墟的黑色轮廓 |
| 备注 | 奥特兰克王国（背叛者佩雷诺德家族）的故地，vanilla 是独立地区与独立地图；唯一步行入口来自南面的希尔斯布莱德。4.0.3 本区被整体并入希尔斯布莱德丘陵、不再是独立 zone——这是本片区最大的版本差异 |
| 出处 | https://warcraft.wiki.gg/wiki/Alterac_Mountains |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-Alterac_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/eastern_kingdoms/lordaeron/alterac_mountains/WorldMap-Alterac_c60.jpg`


## 区级场地平面图

`bg23_奥特兰克山脉全境/planning/bg23_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（18 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg23** | [奥特兰克山脉全境](bg23_奥特兰克山脉全境/bg23_奥特兰克山脉全境.md) | 自造 | — |  |
| **bg24** | [破碎岭城堡](bg24_破碎岭城堡/bg24_破碎岭城堡.md) | 聚居点 · camp | [47, 42] | 雪坡上的食人魔营地，粗木栅栏、兽皮帐篷与巨大的柴堆火 |
| **bg25** | [达拉然](bg25_达拉然/bg25_达拉然.md) | 聚居点 · ruin | [18, 62] | 湖边一座巨大的半透明紫色魔法穹顶，罩着城市废墟的尖塔，穹顶表面有符文缓缓流动 |
| **bg26** | [达伦德农场](bg26_达伦德农场/bg26_达伦德农场.md) | 聚居点 · farm | [42, 17] | 被雪埋了一半的农舍与畜栏，木头发黑，雪面没有脚印 |
| **bg27** | [洛丹米尔收容所](bg27_洛丹米尔收容所/bg27_洛丹米尔收容所.md) | 聚居点 · camp | [21, 80] | 湖畔的木栅栏营地，成排的兵营木屋与瞭望塔，墙角还挂着锁链 |
| **bg28** | [拉文霍德庄园](bg28_拉文霍德庄园/bg28_拉文霍德庄园.md) | 聚居点 · camp | — | 山间台地上的橙顶石砌庄园，后院是训练场与靶子，只有一条盘山小道与一个山洞通进来 |
| **bg29** | [奥特兰克废墟](bg29_奥特兰克废墟/bg29_奥特兰克废墟.md) | 聚居点 · ruin | [40, 49] | 雪中的石城废墟：还立着的宫殿主体、塌掉的教堂与议事厅、一道高大城门与两处墓地，散落着投石机残骸 |
| **bg30** | [斯坦恩布莱德](bg30_斯坦恩布莱德/bg30_斯坦恩布莱德.md) | 聚居点 · village | [73, 38] | 山间的人类小镇，屋顶积雪，铁匠铺与镇政厅还在，街上没有平民只有持刀的强盗 |
| **bg31** | [山头营地](bg31_山头营地/bg31_山头营地.md) | 聚居点 · camp | [40, 85] | 南端伸进湖里的岬角，扎着辛迪加的帐篷与篝火 |
| **bg32** | [奥特兰克山谷（入口）](bg32_奥特兰克山谷（入口）/bg32_奥特兰克山谷（入口）.md) | 子区域 | — | 山脉北端的雪谷谷口，两侧崖壁夹出一条通道，谷口立着双方的旗与传送法阵 |
| **bg33** | [冰风岗](bg33_冰风岗/bg33_冰风岗.md) | 子区域 | [80, 66] | 东侧的风口高地，积雪被风扫成波纹，几棵歪松 |
| **bg34** | [考兰之匕](bg34_考兰之匕/bg34_考兰之匕.md) | 子区域 | [50, 78] | 一道刀刃形的岩脊直插雪地，脊上一条窄路 |
| **bg35** | [绞刑场](bg35_绞刑场/bg35_绞刑场.md) | 子区域 | [50, 57] | 山路岔口立着一座绞刑架，横木上吊着空绳圈，雪地被踩乱 |
| **bg36** | [加文高地](bg36_加文高地/bg36_加文高地.md) | 子区域 | [30, 85] | 南部的裸岩坡地，草与雪交界，能俯瞰洛丹米尔湖 |
| **bg37** | [雾气湖岸](bg37_雾气湖岸/bg37_雾气湖岸.md) | 子区域 | [31, 41] | 洛丹米尔湖北岸，水汽成团贴着湖面，岸边是灰石与枯苇 |
| **bg38** | [屠杀谷](bg38_屠杀谷/bg38_屠杀谷.md) | 子区域 | — | 夹在岩壁间的凹谷，地上尽是骨头与血迹，帐篷边插着战利品杆 |
| **bg39** | [索菲亚高地](bg39_索菲亚高地/bg39_索菲亚高地.md) | 子区域 | [59, 70] | 东南方的高地台，视野开阔，地上是碎石与低矮灌木 |
| **bg40** | [高地](bg40_高地/bg40_高地.md) | 子区域 | [58, 26] | 山脉北部的开阔缓坡，积雪薄，残存着一格一格的旧田埂 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 无草洞（`growless_cave` · 地标）
- 洛丹米尔湖（奥特兰克段）（`lordamere_lake_alterac` · 地标）
- 丘陵洞穴（`the_foothill_caverns` · 地标）
- 奥特兰克山谷（`alterac_valley` · battleground） → 属 奥特兰克山谷（入口）
- 奥特兰克教堂废墟（`alterac_church` · 地标） → 属 奥特兰克废墟
- 奥特兰克城门（`alterac_gate` · 地标） → 属 奥特兰克废墟
- 奥特兰克墓地（`alterac_graveyards` · 地标） → 属 奥特兰克废墟
- 奥特兰克王宫（`alterac_palace` · 地标） → 属 奥特兰克废墟
- 奥特兰克议事厅废墟（`alterac_town_hall` · 地标） → 属 奥特兰克废墟
- 冷齿矿洞（`coldtooth_mine` · 地标） → 属 奥特兰克山谷
- 丹巴达尔（`dun_baldar` · 聚居点 · capital） → 属 奥特兰克山谷
- 丹巴达尔小径（`dun_baldar_pass` · 地标） → 属 奥特兰克山谷
- 征战平原（`field_of_strife` · 子区域） → 属 奥特兰克山谷
- 霜刀小径（`frost_dagger_pass` · 地标） → 属 奥特兰克山谷
- 霜狼墓地（`frostwolf_graveyard` · 地标） → 属 奥特兰克山谷
- 霜狼要塞（`frostwolf_keep` · 聚居点 · capital） → 属 奥特兰克山谷
- 霜狼小径（`frostwolf_pass` · 地标） → 属 奥特兰克山谷
- 霜狼村（`frostwolf_village` · 聚居点 · village） → 属 奥特兰克山谷
- 德雷克塔尔将军（`general_drekthar` · 地标） → 属 奥特兰克山谷
- 范达尔·雷矛将军（`general_vanndar_stormpike` · 地标） → 属 奥特兰克山谷
- 冰血要塞（`iceblood_garrison` · 聚居点 · camp） → 属 奥特兰克山谷
- 冰血墓地（`iceblood_graveyard` · 地标） → 属 奥特兰克山谷
- 冰翼碉堡（`icewing_bunker` · 聚居点 · tower） → 属 奥特兰克山谷
- 冰翼洞穴（`icewing_cavern` · 地标） → 属 奥特兰克山谷
- 冰翼小径（`icewing_pass` · 地标） → 属 奥特兰克山谷
- 深铁矿洞（`irondeep_mine` · 地标） → 属 奥特兰克山谷
- 杜隆坦之石（`rock_of_durotan` · 地标） → 属 奥特兰克山谷
- 雪落墓地（`snowfall_graveyard` · 地标） → 属 奥特兰克山谷
- 石炉碉堡（`stonehearth_bunker` · 聚居点 · tower） → 属 奥特兰克山谷
- 石炉墓地（`stonehearth_graveyard` · 地标） → 属 奥特兰克山谷
- 石炉哨站（`stonehearth_outpost` · 聚居点 · camp） → 属 奥特兰克山谷
- 雷矛墓地（`stormpike_graveyard` · 地标） → 属 奥特兰克山谷
- 迷雾裂隙（`the_veiled_cleft` · 地标） → 属 奥特兰克山谷
- 哨塔高地（`tower_point` · 聚居点 · tower） → 属 奥特兰克山谷
- 蛮爪洞穴（`wildpaw_cavern` · 地标） → 属 奥特兰克山谷
- 蛮爪岭（`wildpaw_ridge` · 子区域） → 属 奥特兰克山谷
- 冰斧要塞（`winterax_hold` · 聚居点 · camp） → 属 奥特兰克山谷
- 丹巴达尔北面碉堡（`dun_baldar_north_bunker` · 聚居点 · tower） → 属 丹巴达尔
- 丹巴达尔南面碉堡（`dun_baldar_south_bunker` · 聚居点 · tower） → 属 丹巴达尔
- 雷矛医疗站（`stormpike_aid_station` · 聚居点 · camp） → 属 丹巴达尔
- 东霜狼塔（`east_frostwolf_tower` · 聚居点 · tower） → 属 霜狼要塞
- 霜狼救援站（`frostwolf_relief_hut` · 聚居点 · camp） → 属 霜狼要塞
- 西霜狼塔（`west_frostwolf_tower` · 聚居点 · tower） → 属 霜狼要塞
- 冰血塔（`iceblood_tower` · 聚居点 · tower） → 属 冰血要塞
