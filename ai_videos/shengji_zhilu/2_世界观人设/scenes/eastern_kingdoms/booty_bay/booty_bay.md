# 藏宝海湾（Booty Bay）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg88_藏宝海湾全城/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/eastern_kingdoms/booty_bay/`（东部王国 → 藏宝海湾），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 主城 · — 级 · neutral |
| 相邻 | — |
| 世界地图尺寸 | 411.5 × 274.3 m（推定：WorldMapArea 尺寸未取到一手出处，450 × 300 码为估计值（1.12 无独立区图：藏宝海湾是荆棘谷 (areaID 33) 的子区 (areaID 35)，客户端显示荆棘谷全图。此处给的是城区本身的物理跨度估计（沿海湾东西约 450 码、南北约 300 码，含港口栈桥），按 3:2 取整；1.15.7 UiMapAssignment 也没有单独条目。）） |
| 世界树画面 | 嵌在悬崖裂口里的多层木板海港城，房屋层层叠叠沿崖壁钉出去，栈桥与吊梯交错，灯笼在海风里晃，港内停着帆船 |
| 备注 | 荆棘谷中立主城，黑水卡特尔哥布林所辖；统治者雷维尔加兹男爵；有旅店、银行、拍卖行、飞行点、通棘齿城的船 |
| 出处 | https://warcraft.wiki.gg/wiki/Booty_Bay |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-Stranglethorn_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/eastern_kingdoms/stranglethorn_vale/WorldMap-Stranglethorn_c60.jpg`


## 区级场地平面图

`bg88_藏宝海湾全城/planning/bg88_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（1 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg88** | [藏宝海湾全城](bg88_藏宝海湾全城/bg88_藏宝海湾全城.md) | 自造 | — |  |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 藏宝海湾码头（`booty_bay_docks` · 地标）
- 藏宝海湾飞行点（`booty_bay_flightpath` · transport · flightpath）
- 藏宝海湾·棘齿城航线码头（`dock_booty_bay_to_ratchet` · transport · boat）
- 藏宝海湾飞行点（联盟）（`fp_booty_bay_alliance` · transport · flightpath）
- 藏宝海湾飞行点（部落）（`fp_booty_bay_horde` · transport · flightpath）
- Stranglethorn Trust Bank（`stranglethorn_trust_bank` · 地标）
- 港务局（`the_old_port_authority` · 地标）
- 水手之家旅店（`the_salty_sailor_tavern` · 地标）
- 藏宝海湾—棘齿城航线（`boat_booty_bay_ratchet` · transport · boat） → 属 藏宝海湾码头
