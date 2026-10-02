# 燃烧平原（Burning Steppes）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg89_燃烧平原全境/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/eastern_kingdoms/burning_steppes/`（东部王国 → 燃烧平原），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 地区 · 50-58 级 · contested |
| 相邻 | 赤脊山 · 灼热峡谷 · 黑石山 |
| 世界地图尺寸 | 2678.4 × 1785 m（坐标表：WorldMapArea：2929.2 × 1952.1 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 焦黑龟裂的火山原野，地表爬着橙红熔岩纹，空中飘着灰烬与火星，天色被烟熏成暗橙，远处黑石山的轮廓吞掉半个天际 |
| 备注 | 扼守暴风王国通往卡兹莫丹与洛丹伦的唯一陆路；黑石兽人、黑龙军团与拉格纳罗斯的仆从所据 |
| 出处 | https://warcraft.wiki.gg/wiki/Burning_Steppes_(Classic) |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-BurningSteppes_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/eastern_kingdoms/burning_steppes/WorldMap-BurningSteppes_c60.jpg`
- `ref/WorldMap-MicroDungeon-BurningSteppes-BlackrockMountain.jpg.link.json` → 微型地下城图
- `ref/WorldMap-MicroDungeon-BurningSteppes-BlackrockMountain1.jpg.link.json` → 微型地下城图
- `ref/WorldMap-MicroDungeon-BurningSteppes-BlackrockMountain2.jpg.link.json` → 微型地下城图

## 区级场地平面图

`bg89_燃烧平原全境/planning/bg89_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（10 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg89** | [燃烧平原全境](bg89_燃烧平原全境/bg89_燃烧平原全境.md) | 自造 | — |  |
| **bg90** | [黑石要塞](bg90_黑石要塞/bg90_黑石要塞.md) | 聚居点 · camp | — | 山脚下的黑石兽人营寨，黑铁尖刺围栏与烧红的炉膛，营中竖着黑色狼头旗，地面被踩成焦黑硬土 |
| **bg91** | [烈焰峰](bg91_烈焰峰/bg91_烈焰峰.md) | 聚居点 · camp | — | 火山岩台地上的小型部落前哨，几顶兽皮帐与一根图腾柱，红旗被热风吹得笔直，脚下岩缝透出橘光 |
| **bg92** | [摩根的岗哨](bg92_摩根的岗哨/bg92_摩根的岗哨.md) | 聚居点 · camp | — | 东南角残破小镇上的联盟营地，石墙只剩半截，帆布帐搭在废墟之间，蓝旗插在焦土上，营外就是通赤脊山的山口 |
| **bg93** | [索瑞森废墟](bg93_索瑞森废墟/bg93_索瑞森废墟.md) | 聚居点 · ruin | — | 大片被熔岩吞掉一半的矮人城市废墟，石砌拱门与方塔焦黑倾斜，街道被凝固的岩浆封死，缝隙里仍透出橘光 |
| **bg94** | [黑石小径](bg94_黑石小径/bg94_黑石小径.md) | 子区域 | — | 从平原盘旋而上的黑岩栈道，一侧是岩壁一侧是深渊，路面被熔岩烤得发脆，尽头是黑石山的南侧门洞 |
| **bg95** | [德拉考达尔](bg95_德拉考达尔/bg95_德拉考达尔.md) | 子区域 | — | 熔岩湖边的黑龙聚集地，岩台上卧着成年黑龙，热浪让空气不断扭动，地面呈暗红玻璃质 |
| **bg96** | [巨槌石](bg96_巨槌石/bg96_巨槌石.md) | 子区域 | — | 东北角一座顶部平坦的巨大岩丘，坡上散着食人魔的粗木营棚与骨堆，丘顶有一口熔炉 |
| **bg97** | [滑石](bg97_滑石/bg97_滑石.md) | 子区域 | — | 平原上一块盘曲如蛇身的长条岩脊，表面布满横向裂纹，岩缝里透出暗红 |
| **bg98** | [龙翼小径](bg98_龙翼小径/bg98_龙翼小径.md) | 子区域 | — | 沿山脊延伸的窄道，两侧岩柱林立，黑龙与幼龙在头顶盘旋，地上散着新旧不一的龙蛋壳 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 风暴祭坛（`altar_of_storms_burning_steppes` · 地标）
- 灰烬之柱（`the_pillar_of_ash` · 地标）
- 黑石山南入口（燃烧平原侧）（`blackrock_mountain_south_entrance` · 地标） → 属 黑石小径
- 烈焰峰飞行点（`flame_crest_flightpath` · transport · flightpath） → 属 烈焰峰
- 烈焰峰飞行点（`fp_flame_crest` · transport · flightpath） → 属 烈焰峰
- 莫根的岗哨飞行点（`fp_morgans_vigil` · transport · flightpath） → 属 摩根的岗哨
- 摩根的岗哨飞行点（`morgans_vigil_flightpath` · transport · flightpath） → 属 摩根的岗哨
