# 月光林地（Moonglade）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg611_月光林地全境/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/kalimdor/moonglade/`（卡利姆多 → 月光林地），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 地区 · — 级 · neutral |
| 相邻 | 费伍德森林 · 冬泉谷 |
| 世界地图尺寸 | 2110.7 × 1407.8 m（坐标表：WorldMapArea：2308.3 × 1539.6 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 群山围抱的深绿银白圣地，镜面般的湖泊映着满月，粗壮古树间浮着紫色萤光，永远是夜 |
| 备注 | 德鲁伊圣地与塞纳里奥议会总部，无等级带、双阵营中立不可攻击；德鲁伊可用「传送：月光林地」直接抵达，其他职业走木喉要塞隧道或飞行点 |
| 出处 | https://warcraft.wiki.gg/wiki/Moonglade |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-Moonglade_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/kalimdor/northern_kalimdor/moonglade/WorldMap-Moonglade_c60.jpg`


## 区级场地平面图

`bg611_月光林地全境/planning/bg611_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（4 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg611** | [月光林地全境](bg611_月光林地全境/bg611_月光林地全境.md) | 自造 | — |  |
| **bg612** | [永夜港](bg612_永夜港/bg612_永夜港.md) | 聚居点 · village | [48.6, 39.2] | 湖畔的精灵村镇，圆顶紫瓦木屋沿弧形石阶排列，水边浮着一排纸灯 |
| **bg613** | [月神湖](bg613_月神湖/bg613_月神湖.md) | 子区域 | — | 占据林地中央的大湖，水面静得像镜子，倒映满月与环湖山影，湖心一座小岛 |
| **bg614** | [怒风兽穴](bg614_怒风兽穴/bg614_怒风兽穴.md) | 子区域 | — | 山壁上并排的三个树根洞口，洞内是安静的圆形石室，中央石台上躺着沉睡的德鲁伊 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 月光林地飞行点（联盟，湖南岸）（`fp_moonglade_alliance` · transport · flightpath）
- 月光林地飞行点（部落，西南角）（`fp_moonglade_horde` · transport · flightpath）
- 木喉隧道月光林地出口（`moonglade_timbermaw_tunnel_exit` · 地标）
- 雷姆洛斯神殿（`shrine_of_remulos` · 地标）
- 永夜港飞行点（仅德鲁伊·单向）（`fp_nighthaven_druid_alliance` · transport · flightpath） → 属 永夜港
- 永夜港飞行点（仅德鲁伊·单向，部落）（`fp_nighthaven_druid_horde` · transport · flightpath） → 属 永夜港
- 德鲁伊传送落点（月光林地）（`moonglade_druid_teleport` · transport · portal） → 属 永夜港
- 永夜港飞行点（`nighthaven_flightpath` · transport · flightpath） → 属 永夜港
