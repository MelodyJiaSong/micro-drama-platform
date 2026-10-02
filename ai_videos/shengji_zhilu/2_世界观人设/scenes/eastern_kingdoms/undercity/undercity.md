# 幽暗城（Undercity）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg360_幽暗城全城/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/eastern_kingdoms/undercity/`（东部王国 → 幽暗城），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 主城 · — 级 · horde |
| 相邻 | — |
| 世界地图尺寸 | 877.3 × 585.3 m（坐标表：WorldMapArea：959.4 × 640.1 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 没有天空的地下环形城：骨白拱顶、蜡黄火把、一圈墨绿瘟疫水渠横穿全城，空气里飘着药剂蒸汽 |
| 备注 | 被遗忘者主城；王宫地下三层，外环四大区围着圆形中庭，银行在最中心 |
| 出处 | https://warcraft.wiki.gg/wiki/Undercity |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-Undercity_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/eastern_kingdoms/lordaeron/tirisfal_glades/undercity/WorldMap-Undercity_c60.jpg`


## 区级场地平面图

`bg360_幽暗城全城/planning/bg360_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（9 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg360** | [幽暗城全城](bg360_幽暗城全城/bg360_幽暗城全城.md) | 自造 | — |  |
| **bg361** | [炼金房](bg361_炼金房/bg361_炼金房.md) | 城区 | — | 成排的铜釜与蒸馏架，毒绿蒸汽从釜口翻出，解剖台上摊着尸体 |
| **bg362** | [幽暗城运河](bg362_幽暗城运河/bg362_幽暗城运河.md) | 城区 | — | 环绕全城的墨绿色药水河道，河面浮着泡沫与残肢，石桥横跨 |
| **bg363** | [魔法区](bg363_魔法区/bg363_魔法区.md) | 城区 | — | 紫蓝色符文光的拱厅，浮空法阵与传送门，地面刻着大圆环 |
| **bg364** | [盗贼区](bg364_盗贼区/bg364_盗贼区.md) | 城区 | — | 低矮暗巷式拱厅，只点零星烛火，墙上挂着匕首靶与假人 |
| **bg365** | [皇家区](bg365_皇家区/bg365_皇家区.md) | 城区 | — | 窄深通道尽头的圆厅，黑绿烛火，高台上一张骨饰王座，女妖侍立 |
| **bg366** | [幽暗城下水道](bg366_幽暗城下水道/bg366_幽暗城下水道.md) | 城区 | — | 城西一条粗石管道，齐膝污水，鼠群与史莱姆 |
| **bg367** | [贸易区](bg367_贸易区/bg367_贸易区.md) | 城区 | — | 圆形中庭，中央一座铁笼状银行，四周拱门下是摊位与拍卖行，绿水从脚边流过 |
| **bg368** | [军事区](bg368_军事区/bg368_军事区.md) | 城区 | — | 铁砧、靶场与操练场，火光偏橙，墙边码着破盾 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 幽暗城，提瑞斯法林地（`undercity_flightpath` · transport · flightpath）
- 幽暗城飞行点（`fp_undercity` · transport · flightpath） → 属 贸易区
- 幽暗城银行（`undercity_bank` · 地标） → 属 贸易区
