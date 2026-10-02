# 逆风小径（Deadwind Pass）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg99_逆风小径全境/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/eastern_kingdoms/deadwind_pass/`（东部王国 → 逆风小径），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 地区 · 55-60 级 · contested |
| 相邻 | 暮色森林 · 悲伤沼泽 |
| 世界地图尺寸 | 2286 × 1524 m（坐标表：WorldMapArea：2500.0 × 1666.7 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 终年昏暗的狭长峡谷，枯死的黑树与灰白岩壁，浓雾贴着谷底走，天光只剩一线；南端是卡拉赞黑塔的剪影 |
| 备注 | 旧世本区几乎没有任务与 NPC，是最荒凉的过路区；连接暮色森林与悲伤沼泽 |
| 出处 | https://warcraft.wiki.gg/wiki/Deadwind_Pass_(Classic) |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-DeadwindPass_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/eastern_kingdoms/deadwind_pass/WorldMap-DeadwindPass_c60.jpg`
- `ref/WorldMap-MicroDungeon-DeadwindPass-Dalaran.jpg.link.json` → 微型地下城图
- `ref/WorldMap-MicroDungeon-DeadwindPass-KarazhanCatacombs.jpg.link.json` → 微型地下城图
- `ref/WorldMap-MicroDungeon-DeadwindPass-TheMastersCellar.jpg.link.json` → 微型地下城图
- `ref/WorldMap-MicroDungeon-DeadwindPass-TheMastersCellar1.jpg.link.json` → 微型地下城图
- `ref/WorldMap-MicroDungeon-DeadwindPass-TheMastersCellar2.jpg.link.json` → 微型地下城图

## 区级场地平面图

`bg99_逆风小径全境/planning/bg99_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（7 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg99** | [逆风小径全境](bg99_逆风小径全境/bg99_逆风小径全境.md) | 自造 | — |  |
| **bg100** | [死者十字](bg100_死者十字/bg100_死者十字.md) | 聚居点 · ruin | — | 谷中一处废弃的人类村落十字路口，石砌房屋只剩墙框，屋顶早塌，路边一座倒地的木制路牌 |
| **bg101** | [格罗高克营地](bg101_格罗高克营地/bg101_格罗高克营地.md) | 聚居点 · camp | — | 罪恶谷里的食人魔营地，歪斜的木栅与兽皮棚，营中一堆常年不灭的火，四周插满削尖的木桩 |
| **bg102** | [墓穴](bg102_墓穴/bg102_墓穴.md) | 子区域 | — | 崖壁里凿出的墓穴入口，铁栅半开，石阶向下没入黑暗，门楣刻着风化的人形浮雕 |
| **bg103** | [逆风谷](bg103_逆风谷/bg103_逆风谷.md) | 子区域 | — | 切进岩层的深沟，底部窄到只容一人通过，抬头只能看见一条灰色天缝 |
| **bg104** | [沉睡峡谷](bg104_沉睡峡谷/bg104_沉睡峡谷.md) | 子区域 | — | 谷中一段异常安静的河床，水几乎不流，两岸枯树倒影一动不动 |
| **bg105** | [罪恶谷](bg105_罪恶谷/bg105_罪恶谷.md) | 子区域 | — | 两侧崖壁向中间挤压的窄谷，像被钳住一样，谷底堆着滚落的碎石与食人魔的粗木栅 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 埃瑞丁营地（`aridens_camp` · 地标）
- 卡拉赞（`karazhan` · 地标）
- 摩根墓场（`morgans_plot` · 地标） → 属 卡拉赞
- 主宰的庇护所（`the_masters_cellar` · 子区域） → 属 卡拉赞
