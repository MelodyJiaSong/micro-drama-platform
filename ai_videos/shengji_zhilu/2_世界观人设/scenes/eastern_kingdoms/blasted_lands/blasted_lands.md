# 诅咒之地（Blasted Lands）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg80_诅咒之地全境/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/eastern_kingdoms/blasted_lands/`（东部王国 → 诅咒之地），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 地区 · 45-55 级 · contested |
| 相邻 | 悲伤沼泽 |
| 世界地图尺寸 | 3063.2 × 2042.2 m（坐标表：WorldMapArea：3350.0 × 2233.3 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 寸草不生的暗红荒原，地表龟裂成深沟，嶙峋的紫黑岩柱斜插向天，天空是不祥的橙紫色，风里卷着红尘 |
| 备注 | 被黑暗之门的魔法扭曲而成；4.0.3 大改（新增瑟维奇、污染之林等），本树只收旧世 |
| 出处 | https://warcraft.wiki.gg/wiki/Blasted_Lands_(Classic) |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-BlastedLands_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/eastern_kingdoms/blasted_lands/WorldMap-BlastedLands_c60.jpg`


## 区级场地平面图

`bg80_诅咒之地全境/planning/bg80_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（8 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg80** | [诅咒之地全境](bg80_诅咒之地全境/bg80_诅咒之地全境.md) | 自造 | — |  |
| **bg81** | [巨槌要塞](bg81_巨槌要塞/bg81_巨槌要塞.md) | 聚居点 · camp | — | 红土坡上的食人魔营寨，巨大的粗木尖桩围栏，兽皮帐篷比人还高，营中央一堆烧得发黑的骨头 |
| **bg82** | [巨槌岗哨](bg82_巨槌岗哨/bg82_巨槌岗哨.md) | 聚居点 · camp | — | 荒原上的小股食人魔前哨，三两顶破帐与一根插着头骨的木杆，周围是裸露的红岩 |
| **bg83** | [守望堡](bg83_守望堡/bg83_守望堡.md) | 聚居点 · town | — | 荒原北缘的白石要塞，方形塔楼与雉堞在红土上格外突兀，蓝色旗帜猎猎，塔顶有法师的紫光结界 |
| **bg84** | [污染者高地](bg84_污染者高地/bg84_污染者高地.md) | 子区域 | — | 荒原上突起的台地，顶部一圈焦黑的仪式石，紫色的余烬从地缝里往上飘 |
| **bg85** | [盘蛇谷](bg85_盘蛇谷/bg85_盘蛇谷.md) | 子区域 | — | 盘绕成蛇形的干涸河谷，两壁是层层剥落的红岩，谷底散着巨大的蛇类骨节 |
| **bg86** | [荒芜之海](bg86_荒芜之海/bg86_荒芜之海.md) | 子区域 | — | 诅咒之地东缘的海面，被岸上的红尘染成浑浊的铁锈色，浪头低而钝，岸线是一路塌进海里的紫黑岩块 |
| **bg87** | [腐烂之痕](bg87_腐烂之痕/bg87_腐烂之痕.md) | 子区域 | — | 大地上一道巨大的焦黑裂痕，坑底冒着绿色毒雾，恶魔的骨骸与烧融的岩块混在一起 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 风暴祭坛（`altar_of_storms_blasted_lands` · 地标）
- 黑暗之门（旧世·关闭状态）（`poi_dark_portal_vanilla` · 地标）
- 黑暗之门（`the_dark_portal` · 地标）
- 尼萨格德要塞飞行点（`fp_nethergarde_keep` · transport · flightpath） → 属 守望堡
- 要塞军械库（`garrison_armory` · 地标） → 属 守望堡
- 守望堡飞行点（`nethergarde_keep_flightpath` · transport · flightpath） → 属 守望堡
- 黑暗之门坑地（`dark_portal_crater` · 地标） → 属 黑暗之门
