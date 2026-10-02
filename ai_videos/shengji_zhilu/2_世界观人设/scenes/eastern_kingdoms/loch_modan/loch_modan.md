# 洛克莫丹（Loch Modan）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg214_洛克莫丹全境/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/eastern_kingdoms/loch_modan/`（东部王国 → 洛克莫丹），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 地区 · 10-20 级 · alliance |
| 相邻 | 丹莫罗 · 湿地 · 荒芜之地 · 灼热峡谷 |
| 世界地图尺寸 | 2522.2 × 1682.1 m（坐标表：WorldMapArea：2758.3 × 1839.6 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 环山抱着一整片碧蓝湖水的温带谷地，坡上是松树与白桦，湖岸是黄绿草坡与红瓦矮人屋，北端横着一道巨大的灰石水坝 |
| 备注 | 矮人第二区；旧世的湖是满的（4.0.3 大地裂变炸掉水坝后湖水几乎排干，这是本区头号版本差异）。往南可步行进荒芜之地，往北经丹奥加兹进湿地 |
| 出处 | https://warcraft.wiki.gg/wiki/Loch_Modan |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-LochModan_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/eastern_kingdoms/khaz_modan/loch_modan/WorldMap-LochModan_c60.jpg`


## 区级场地平面图

`bg214_洛克莫丹全境/planning/bg214_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（8 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg214** | [洛克莫丹全境](bg214_洛克莫丹全境/bg214_洛克莫丹全境.md) | 自造 | — |  |
| **bg215** | [奥加兹岗哨](bg215_奥加兹岗哨/bg215_奥加兹岗哨.md) | 聚居点 · camp | [24, 18] | 山路边一处矮石墙围起的驻防点，几顶军帐加一座瞭望木塔，路障后站着披斗篷的矮人山地兵 |
| **bg216** | [银泉矿洞](bg216_银泉矿洞/bg216_银泉矿洞.md) | 聚居点 · mine | [35, 22] | 北岸崖壁上一个木框加固的矿洞口，洞外停着两辆翻倒的矿车，洞内壁面泛着银灰色的矿脉光 |
| **bg217** | [旅行者营地](bg217_旅行者营地/bg217_旅行者营地.md) | 聚居点 · inn | [73, 52] | 湖东岸林边一座猎人木屋，门廊挂着兽皮与鹿角，屋前拴着猎犬，院里立着射箭靶 |
| **bg218** | [塞尔萨玛](bg218_塞尔萨玛/bg218_塞尔萨玛.md) | 聚居点 · town | [35, 47] | 湖西岸坡地上的矮人小镇，一排石基木墙的坡顶屋沿路展开，镇边一座敞篷狮鹫棚，屋后是马厩与铁砧 |
| **bg219** | [灰爪山](bg219_灰爪山/bg219_灰爪山.md) | 子区域 | [46, 73] | 南岸一道长满松林的缓岭，林下是厚厚的松针与倒木，常能看到熊与山猫在坡上活动 |
| **bg220** | [碎石怪之谷](bg220_碎石怪之谷/bg220_碎石怪之谷.md) | 子区域 | [34, 73] | 西南一条乱石谷，谷壁裂出数个穴居人洞口，地上满是碎岩与粗糙的石制工具 |
| **bg221** | [国王谷](bg221_国王谷/bg221_国王谷.md) | 子区域 | [21, 74] | 西南角一条笔直的石谷，两侧崖壁雕着巨大的矮人王像，谷底一条被车辙压实的商路直通南面山口 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 丹奥加兹（`dun_algaz_loch_modan` · 地标）
- 铁环挖掘场（`ironbands_excavation_site` · 地标）
- 莫格罗什要塞（`mo_grosh_stronghold` · 地标）
- 北门小径（`north_gate_pass_loch_modan` · 地标）
- 南门小径（`south_gate_pass_loch_modan` · 地标）
- 巨石水坝（`stonewrought_dam` · 地标）
- 洛克湖（`the_loch` · 地标）
- 奥加兹大门（`algaz_gate` · 地标） → 属 丹奥加兹
- 塞尔萨玛飞行点（`fp_thelsamar` · transport · flightpath） → 属 塞尔萨玛
- 烈酒旅店（`stoutlager_inn` · 聚居点 · inn） → 属 塞尔萨玛
- 塞尔萨玛狮鹫场（`thelsamar_gryphon_roost` · transport · flightpath） → 属 塞尔萨玛
