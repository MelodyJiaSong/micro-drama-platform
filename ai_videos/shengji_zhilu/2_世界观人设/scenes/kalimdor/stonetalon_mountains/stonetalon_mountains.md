# 石爪山脉（Stonetalon Mountains）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg657_石爪山脉全境/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/kalimdor/stonetalon_mountains/`（卡利姆多 → 石爪山脉），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 地区 · 15-27 级 · contested |
| 相邻 | 贫瘠之地 · 灰谷 · 凄凉之地 |
| 世界地图尺寸 | 4465.3 × 2977.5 m（坐标表：WorldMapArea：4883.3 × 3256.2 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 层叠的灰褐石峰夹着深绿的针叶谷地，山腰常挂低云，被砍秃的山坡上留着成片树桩与锯木架 |
| 备注 | 旧世 15-27 级的争夺区；西接迷雾之海、东接贫瘠之地、北接灰谷、南接凄凉之地。4.0.3a 被大改，地形与据点几乎重排 |
| 出处 | https://warcraft.wiki.gg/wiki/Stonetalon_Mountains |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-StonetalonMountain_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/kalimdor/central_kalimdor/stonetalon_mountains/WorldMap-StonetalonMountain_c60.jpg`


## 区级场地平面图

`bg657_石爪山脉全境/planning/bg657_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（13 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg657** | [石爪山脉全境](bg657_石爪山脉全境/bg657_石爪山脉全境.md) | 自造 | — |  |
| **bg658** | [阿帕拉耶营地](bg658_阿帕拉耶营地/bg658_阿帕拉耶营地.md) | 聚居点 · camp | [77, 90] | 东部山坡上几顶被掀翻烧过的牛头人帐篷，帐架焦黑，地上散着打翻的器物 |
| **bg659** | [恐怖图腾岗哨](bg659_恐怖图腾岗哨/bg659_恐怖图腾岗哨.md) | 聚居点 · camp | [74, 85] | 山坳里一片牛头人营地，帐面是发暗的深色兽皮、图腾柱涂黑，营中来回走动的牛头人全副武装 |
| **bg660** | [玛拉卡金](bg660_玛拉卡金/bg660_玛拉卡金.md) | 聚居点 · camp | [70, 91] | 山道旁一小片巨魔营地，兽骨与彩绘木杆撑起的低矮茅棚，架子上晾着猎来的兽皮与肉干 |
| **bg661** | [石爪峰](bg661_石爪峰/bg661_石爪峰.md) | 聚居点 · town | [43, 16] | 山脉最高处一片被绿色围住的山谷聚落，暗夜精灵的紫瓦弧顶建筑与发光的月井立在林间，四周是灰岩绝壁 |
| **bg662** | [烈日石居](bg662_烈日石居/bg662_烈日石居.md) | 聚居点 · town | [50, 61] | 藏在峰间的一小片部落聚落，兽皮尖顶帐与牛头人图腾柱贴着岩壁排开，一侧是直落的悬崖 |
| **bg663** | [滚岩峡谷](bg663_滚岩峡谷/bg663_滚岩峡谷.md) | 子区域 | [65, 91] | 一条落满滚石的小峡谷，谷壁碎裂、随时还在掉石头，山羊在石堆间跳跃 |
| **bg664** | [巨木谷](bg664_巨木谷/bg664_巨木谷.md) | 子区域 | — | 东南山麓一片还没被砍的高针叶林谷，树干笔直高耸，林下光线很暗，地面铺着厚松针 |
| **bg665** | [暗色湖](bg665_暗色湖/bg665_暗色湖.md) | 子区域 | [47, 40] | 群峰正中一潭墨绿色的静水，四周被高针叶林围死，水面几乎不起波，常年浮着一层薄雾 |
| **bg666** | [希塞尔山谷](bg666_希塞尔山谷/bg666_希塞尔山谷.md) | 子区域 | [54, 75] | 一条从主路岔出去的空旷石谷，两侧是笔直的灰岩壁，谷底几乎什么都没有 |
| **bg667** | [焦炭谷](bg667_焦炭谷/bg667_焦炭谷.md) | 子区域 | — | 西南一整片被烧成焦黑的谷地，地缝里淌着橙红岩浆，枯树只剩炭桩，空气被热浪扭曲 |
| **bg668** | [血怒峡谷](bg668_血怒峡谷/bg668_血怒峡谷.md) | 子区域 | — | 焦炭谷边缘一段更窄的火谷，崖上密布鹰身女妖的骨枝巢，地面覆着黑灰 |
| **bg669** | [狂风峭壁](bg669_狂风峭壁/bg669_狂风峭壁.md) | 子区域 | — | 曾是老龄巨木林的谷地，现在只剩成片齐腰的树桩与堆起的原木，哥布林的铁架厂房横跨在谷上 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 蛛网小径（`webwinder_path` · 地标）
- 滚岩洞穴（`boulderslide_cavern` · 地标） → 属 滚岩峡谷
- 石爪峰飞行点（`fp_stonetalon_peak` · transport · flightpath） → 属 石爪峰
- 石爪峰飞行点（`stonetalon_peak_flightpath` · transport · flightpath） → 属 石爪峰
- 猛禽洞穴（`the_talon_den` · 地标） → 属 石爪峰
- 烈日石居飞行点（`fp_sun_rock_retreat` · transport · flightpath） → 属 烈日石居
- 烈日石居飞行点（`sun_rock_flightpath` · transport · flightpath） → 属 烈日石居
- 黑狼河（`blackwolf_river` · 地标） → 属 狂风峭壁
- 峭壁湖（`cragpool_lake` · 子区域） → 属 狂风峭壁
- 石爪小径（`the_talondeep_path_stonetalon` · transport · portal） → 属 狂风峭壁
- 狂风矿洞（`windshear_mine` · 地标） → 属 狂风峭壁
