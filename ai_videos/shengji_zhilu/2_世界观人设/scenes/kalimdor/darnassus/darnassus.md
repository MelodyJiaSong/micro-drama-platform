# 达纳苏斯（Darnassus）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg495_达纳苏斯全城/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/kalimdor/darnassus/`（卡利姆多 → 达纳苏斯），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 主城 · — 级 · alliance |
| 相邻 | — |
| 世界地图尺寸 | 967.7 × 645.3 m（坐标表：WorldMapArea：1058.3 × 705.7 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 树冠西侧的月白靛蓝都城，环抱一片浅湖，弧形木桥跨水相连，紫顶白柱殿堂与萤火般的光点浮在夜色里 |
| 备注 | 暗夜精灵首都，客户端里是独立 zone（AreaID 1657）而非泰达希尔的子区域；五个大区 + 中央神殿花园 |
| 出处 | https://warcraft.wiki.gg/wiki/Darnassus |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-Darnassus_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/kalimdor/northern_kalimdor/teldrassil/darnassus/WorldMap-Darnassus_c60.jpg`


## 区级场地平面图

`bg495_达纳苏斯全城/planning/bg495_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（7 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg495** | [达纳苏斯全城](bg495_达纳苏斯全城/bg495_达纳苏斯全城.md) | 自造 | — |  |
| **bg496** | [塞纳里奥区](bg496_塞纳里奥区/bg496_塞纳里奥区.md) | 城区 | [36, 14] | 城北高处的树冠平台群，多层木台由斜坡与藤桥串起，台上立着巨大的守护巨树 |
| **bg497** | [工匠区](bg497_工匠区/bg497_工匠区.md) | 城区 | [54, 38] | 东北侧的环形作坊台地，沿弧墙排开铁匠炉、织机与炼金台，炉火是全城唯一的暖色 |
| **bg498** | [月神殿](bg498_月神殿/bg498_月神殿.md) | 城区 | [39, 76] | 城南隔水的一座独立台地，半球形白石穹顶压在成排立柱上，穹顶开口漏下一柱月光，落进殿心一池静水，柱间垂着银纱，周围是低矮花 |
| **bg499** | [神殿花园](bg499_神殿花园/bg499_神殿花园.md) | 城区 | — | 城市中央的开阔水景园，浅湖中一座圆形绿岛，环岛白石堤与低矮花丛，四面木桥辐射而出 |
| **bg500** | [贸易区](bg500_贸易区/bg500_贸易区.md) | 城区 | — | 城南的大片台地，成排货摊与卷边布棚，地面铺浅色木板，人流最密 |
| **bg501** | [战士区](bg501_战士区/bg501_战士区.md) | 城区 | [60, 44] | 东侧入城门廊，石砌台阶两侧立着持长刃的哨兵雕像，尽头是训练场的圆形沙地 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 达纳苏斯旅店（`darnassus_inn` · 聚居点 · inn） → 属 工匠区
- 达纳苏斯银行（`darnassus_bank` · 地标） → 属 神殿花园
- 达纳苏斯传送门（通鲁瑟兰村）（`darnassus_portal_rutheran` · transport · portal） → 属 神殿花园
- 达纳苏斯→鲁瑟兰村传送门（`portal_darnassus_to_rutheran` · transport · portal） → 属 神殿花园
- 月神殿（`temple_of_the_moon` · 地标） → 属 神殿花园
- 达纳苏斯拍卖行（`darnassus_auction_house` · 地标） → 属 贸易区
- 达纳苏斯墓地（`darnassus_cemetery` · 地标） → 属 战士区
