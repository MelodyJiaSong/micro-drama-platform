# 奥格瑞玛（Orgrimmar）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg629_奥格瑞玛全城/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/kalimdor/orgrimmar/`（卡利姆多 → 奥格瑞玛），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 主城 · — 级 · horde |
| 相邻 | — |
| 世界地图尺寸 | 1282.5 × 855.3 m（坐标表：WorldMapArea：1402.6 × 935.4 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 嵌在赭红岩壁里的一串峡谷城，粗圆木与兽皮搭的尖顶屋顶一层层贴着崖壁，红黑部落旗与骨制图腾插满谷壁，抬头只见一线天 |
| 备注 | 兽人与整个部落的首都，以奥格瑞姆·毁灭之锤命名，建在杜隆塔尔北缘的一套山谷与洞穴里；旧世大酋长萨尔坐镇智慧谷的格罗玛什要塞。作为 zone 它挂在杜隆塔尔之下（AreaTable 1637 的 ParentAreaID 为 0，但世界地图上它落在杜隆塔尔境内） |
| 出处 | https://warcraft.wiki.gg/wiki/Orgrimmar |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-Orgrimmar_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/kalimdor/central_kalimdor/durotar/orgrimmar/WorldMap-Orgrimmar_c60.jpg`


## 区级场地平面图

`bg629_奥格瑞玛全城/planning/bg629_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（7 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg629** | [奥格瑞玛全城](bg629_奥格瑞玛全城/bg629_奥格瑞玛全城.md) | 自造 | — |  |
| **bg630** | [暗影裂口](bg630_暗影裂口/bg630_暗影裂口.md) | 城区 | — | 从暗巷往西凿进山体的一处洞穴式街区，完全不见天空，墙上只有紫绿色的幽光与零星火盆，空气里飘着烟 |
| **bg631** | [暗巷](bg631_暗巷/bg631_暗巷.md) | 城区 | — | 夹在两面高崖之间的一条终年背光的窄street，两侧一家挨一家的专业作坊与摊铺，头顶只露出一线天光 |
| **bg632** | [荣誉谷](bg632_荣誉谷/bg632_荣誉谷.md) | 城区 | — | 城东北的军事谷地，铁匠炉的橙红火光与锤击声不断，谷中一口方形水池，地上立满练功木桩与兵器架 |
| **bg633** | [精神谷](bg633_精神谷/bg633_精神谷.md) | 城区 | — | 一条又长又窄的支谷，巨魔风格的高脚茅顶棚屋与彩绘骨面具立在两侧，谷底常年半明，挂满串珠与羽饰 |
| **bg634** | [力量谷](bg634_力量谷/bg634_力量谷.md) | 城区 | — | 进门后第一片开阔谷地，两侧崖壁被凿出层层平台与木梯，兽皮顶摊位挤满谷底，地面是踩实的暗红夯土 |
| **bg635** | [智慧谷](bg635_智慧谷/bg635_智慧谷.md) | 城区 | — | 城西北一片较安静的谷地，牛头人式的大帐与图腾柱立在谷侧，谷正中是全城最高大的一座尖顶石木要塞 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 传说大厅（`hall_of_legends` · 地标）
- 奥格瑞玛正门（`orgrimmar_main_gate` · 地标）
- 怒焰裂谷（`ragefire_chasm` · dungeon） → 属 暗影裂口
- 影踪兄弟会（`shadowswift_brotherhood` · 地标） → 属 暗影裂口
- 勇者大厅（`hall_of_the_brave` · 地标） → 属 荣誉谷
- 猎人大厅（`hunters_hall` · 地标） → 属 荣誉谷
- 暗棘旅店（`darkbriar_lodge` · 地标） → 属 精神谷
- 奥格瑞玛银行（`bank_of_orgrimmar` · 地标） → 属 力量谷
- 奥格瑞玛飞行点（`fp_orgrimmar` · transport · flightpath） → 属 力量谷
- 奥格瑞玛拍卖行（`orgrimmar_auction_house` · 地标） → 属 力量谷
- 奥格瑞玛双足飞龙栖木（`orgrimmar_flightpath` · transport · flightpath） → 属 力量谷
- 天空塔（`the_skytower` · 地标） → 属 力量谷
- 格罗玛什要塞（`grommash_hold` · 地标） → 属 智慧谷
- 巴扎兰（`bazzalan` · 地标） → 属 怒焰裂谷
- 祈求者耶戈什（`jergosh_the_invoker` · 地标） → 属 怒焰裂谷
- 奥格弗林特（`oggleflint` · 地标） → 属 怒焰裂谷
- 饥饿者塔拉加曼（`taragaman_the_hungerer` · 地标） → 属 怒焰裂谷
