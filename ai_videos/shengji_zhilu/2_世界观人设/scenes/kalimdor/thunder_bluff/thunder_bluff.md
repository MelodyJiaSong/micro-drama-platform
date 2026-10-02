# 雷霆崖（Thunder Bluff）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg757_雷霆崖全城/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/kalimdor/thunder_bluff/`（卡利姆多 → 雷霆崖），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 主城 · — 级 · horde |
| 相邻 | — |
| 世界地图尺寸 | 954.4 × 636.3 m（坐标表：WorldMapArea：1043.8 × 695.8 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 几座平顶红岩高台悬在数百尺高空，台面铺满圆锥兽皮大帐与木架，台与台之间只靠晃动的绳索吊桥相连，帐顶的图腾与羽饰在风里一直响 |
| 备注 | 牛头人的首都，由凯恩·血蹄建立，坐落在莫高雷北部；整座城建在高崖上，只能靠西南与东北两侧的升降梯上下。旧世**没有飞艇**（飞艇坡道要到 3.2.0 才加） |
| 出处 | https://warcraft.wiki.gg/wiki/Thunder_Bluff |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-ThunderBluff_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/kalimdor/central_kalimdor/mulgore/thunder_bluff/WorldMap-ThunderBluff_c60.jpg`


## 区级场地平面图

`bg757_雷霆崖全城/planning/bg757_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（7 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg757** | [雷霆崖全城](bg757_雷霆崖全城/bg757_雷霆崖全城.md) | 自造 | — |  |
| **bg758** | [长者高地](bg758_长者高地/bg758_长者高地.md) | 城区 | — | 主台正东的一座独立平顶台地，台上立着几顶绘满自然纹样的大帐与活着的树桩图腾，绿意比别处明显 |
| **bg759** | [猎人高地](bg759_猎人高地/bg759_猎人高地.md) | 城区 | — | 主台正南的一座台地，台上立着成排的练功木桩与晾皮架，帐外拴着猎豹与巨狼 |
| **bg760** | [灵魂高地](bg760_灵魂高地/bg760_灵魂高地.md) | 城区 | — | 主台西北的一座台地，台面插满高矮不一的图腾柱，柱间系着招魂的彩布条，台下岩缝里冒出白色水汽 |
| **bg761** | [顶层高地](bg761_顶层高地/bg761_顶层高地.md) | 城区 | — | 中央主台的最顶层，正中一顶格外高大的酋长大帐，帐前是一圈露天的石阶议事场，四面全是天空 |
| **bg762** | [低层高地](bg762_低层高地/bg762_低层高地.md) | 城区 | — | 中央主台最低的一层，一圈摊位与挑高的兽皮商帐围着中心空地，地面是夯实的红土与铺开的编席 |
| **bg763** | [中层高地](bg763_中层高地/bg763_中层高地.md) | 城区 | — | 主台的中间一层，沿崖边一圈作坊帐篷，架子上摊着皮子、草药与织物，风把布幡吹得笔直 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 雷霆崖飞行点（`fp_thunder_bluff` · transport · flightpath）
- 雷霆崖升降梯（`tb_elevators` · transport · tram）
- 雷霆崖双足飞龙栖木（`tb_flightpath` · transport · flightpath）
- 雷霆崖绳索吊桥（`tb_rope_bridges` · 地标）
- 长者大厅（`hall_of_elders` · 地标） → 属 长者高地
- 预见之池（`the_pools_of_vision` · 子区域） → 属 灵魂高地
