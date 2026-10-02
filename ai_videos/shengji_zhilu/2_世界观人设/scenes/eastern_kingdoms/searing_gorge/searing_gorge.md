# 灼热峡谷（Searing Gorge）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg237_灼热峡谷全境/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/eastern_kingdoms/searing_gorge/`（东部王国 → 灼热峡谷），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 地区 · 45-50 级 · contested |
| 相邻 | 荒芜之地 · 洛克莫丹 · 燃烧平原 · 黑石山 |
| 世界地图尺寸 | 2040.3 × 1360.2 m（坐标表：WorldMapArea：2231.2 × 1487.5 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 被整片挖空的赤褐矿区盆地，露天矿坑层层下陷，蒸汽与黄烟从地缝喷出，空气浑浊呈橙黄色，四周是陡直的红岩崖壁 |
| 备注 | 【旧世关键差异】1.12 时洛克莫丹一侧的入口上着锁，需完成任务线拿到「灼热峡谷的钥匙」（或盗贼 225 开锁）；4.0.3 后才无条件开放 |
| 出处 | https://warcraft.wiki.gg/wiki/Searing_Gorge_(Classic) |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-SearingGorge_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/eastern_kingdoms/khaz_modan/searing_gorge/WorldMap-SearingGorge_c60.jpg`
- `ref/WorldMap-MicroDungeon-SearingGorge-BlackrockMountain.jpg.link.json` → 微型地下城图
- `ref/WorldMap-MicroDungeon-SearingGorge-BlackrockMountain1.jpg.link.json` → 微型地下城图
- `ref/WorldMap-MicroDungeon-SearingGorge-BlackrockMountain2.jpg.link.json` → 微型地下城图

## 区级场地平面图

`bg237_灼热峡谷全境/planning/bg237_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（9 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg237** | [灼热峡谷全境](bg237_灼热峡谷全境/bg237_灼热峡谷全境.md) | 自造 | — |  |
| **bg238** | [煤渣挖掘场](bg238_煤渣挖掘场/bg238_煤渣挖掘场.md) | 聚居点 · camp | — | 侏儒/哥布林式的露天挖掘营地，蒸汽机械与木制吊架，成堆的碎石与翻倒的矿车，空气里全是粉尘 |
| **bg239** | [制皮匠营地](bg239_制皮匠营地/bg239_制皮匠营地.md) | 聚居点 · camp | — | 岩壁下的小营地，木架上绷着正在鞣制的兽皮，地上几口浸皮的木桶，烟从小火堆里直直升起 |
| **bg240** | [瑟银哨塔](bg240_瑟银哨塔/bg240_瑟银哨塔.md) | 聚居点 · town | [36, 27] | 建在岩台上的黑铁矮人聚落，铁皮棚屋与高炉挤在一起，炉火把矮人的脸映成橘色，栈桥悬在矿坑上方 |
| **bg241** | [黑炭谷](bg241_黑炭谷/bg241_黑炭谷.md) | 子区域 | — | 崖壁上熏得全黑的洞口，洞内岩壁像木炭一样酥脆，深处透出微弱红光 |
| **bg242** | [尘火谷](bg242_尘火谷/bg242_尘火谷.md) | 子区域 | — | 常年扬尘的浅谷，风把红色细尘卷成低矮的旋涡，地上零散烧着几处自燃的火点 |
| **bg243** | [观火岭](bg243_观火岭/bg243_观火岭.md) | 子区域 | — | 西侧高地上的黑铁矮人营区，石砌哨塔与熔炉排成一线，岩脊上望下去是整条冒烟的峡谷 |
| **bg244** | [大熔炉](bg244_大熔炉/bg244_大熔炉.md) | 子区域 | — | 峡谷中央巨大的圆形下沉矿坑，像一口锅，坑壁盘旋着一圈圈作业平台，坑底是发亮的熔渣与火光 |
| **bg245** | [灰烬之海](bg245_灰烬之海/bg245_灰烬之海.md) | 子区域 | — | 一整片没过脚踝的灰白炭灰平地，踩上去会扬起灰雾，偶有暗红余烬在灰下闪一下 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 黑石山北入口（灼热峡谷侧）（`blackrock_mountain_north_entrance` · 地标）
- 石坝小径（`stonewrought_pass` · transport · portal）
- 熔渣之池（`the_slag_pit` · 子区域） → 属 大熔炉
- 瑟银哨塔飞行点（联盟）（`fp_thorium_point_alliance` · transport · flightpath） → 属 瑟银哨塔
- 瑟银哨塔飞行点（部落）（`fp_thorium_point_horde` · transport · flightpath） → 属 瑟银哨塔
- 瑟银哨塔飞行点（`thorium_point_flightpath` · transport · flightpath） → 属 瑟银哨塔
