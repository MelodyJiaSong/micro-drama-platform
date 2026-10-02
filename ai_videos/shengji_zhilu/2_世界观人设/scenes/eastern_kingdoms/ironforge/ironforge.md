# 铁炉堡（Ironforge）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg202_铁炉堡全城/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/eastern_kingdoms/ironforge/`（东部王国 → 铁炉堡），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 主城 · — 级 · alliance |
| 相邻 | 丹莫罗 · 暴风城 |
| 世界地图尺寸 | 722.9 × 482.4 m（坐标表：WorldMapArea：790.6 × 527.6 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 整座挖在山腹里的环形石城，穹顶是凿出的黑岩，一圈圈台地朝中央的熔岩大锻炉落下去，火光把砖石烤成橙红，处处是黄铜管道与铁轨 |
| 备注 | 联盟矮人主城，独立地图；coords 是它在丹莫罗地图上的图标位置。经 Deeprun Tram 直通暴风城。铁炉堡城内各区在 Classic AreaTable 里没有条目（属地图美术标签），故下属节点的坐标大多未查到 |
| 出处 | https://warcraft.wiki.gg/wiki/Ironforge |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-Ironforge_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/eastern_kingdoms/khaz_modan/dun_morogh/ironforge/WorldMap-Ironforge_c60.jpg`


## 区级场地平面图

`bg202_铁炉堡全城/planning/bg202_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（12 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg202** | [铁炉堡全城](bg202_铁炉堡全城/bg202_铁炉堡全城.md) | 自造 | — |  |
| **bg203** | [武器大厅](bg203_武器大厅/bg203_武器大厅.md) | 城区 | — | 军事区里的大练武厅，中央一圈沙地擂台，四周兵器架列满长柄武器，墙上是历代矮人战旗 |
| **bg204** | [探险者大厅](bg204_探险者大厅/bg204_探险者大厅.md) | 城区 | — | 高穹顶的展陈大厅，中庭立着完整的恐龙骨架与泰坦石碑残块，四壁是书架与玻璃展柜 |
| **bg205** | [秘法大厅](bg205_秘法大厅/bg205_秘法大厅.md) | 城区 | — | 秘法区深处的高顶圣堂，中央一口圣光照亮的水池，两侧是雕着圣徽的石柱与长明烛台 |
| **bg206** | [旧铁炉堡](bg206_旧铁炉堡/bg206_旧铁炉堡.md) | 城区 | — | 王座厅下方一层更古老的石窟，柱式粗笨、没有黄铜装饰，只有裸岩与旧火盆，空气里有陈年的冷 |
| **bg207** | [平民区](bg207_平民区/bg207_平民区.md) | 城区 | — | 进城后第一圈宽环廊，两侧一长排石砌商铺与摊位，穹顶垂下铁链吊灯，地面被人流踩出光亮的石板道 |
| **bg208** | [荒弃的洞穴](bg208_荒弃的洞穴/bg208_荒弃的洞穴.md) | 城区 | — | 一段刻意不加修饰的天然岩洞，顶上垂着钟乳，地下暗河从中间淌过，光源只有零星几支火把，是全城最暗的一块 |
| **bg209** | [大锻炉](bg209_大锻炉/bg209_大锻炉.md) | 城区 | — | 城心一口巨大的熔岩坑，橙红岩浆上架着环形铁桥，四周石台上立着一座座铁砧，火星与热浪把整片空气烤得发抖 |
| **bg210** | [王座厅](bg210_王座厅/bg210_王座厅.md) | 城区 | — | 大锻炉尽头抬高的王座厅，一条石阶直上，厅中一张黑铁王座背靠雕满符文的石壁，两侧立着持斧卫兵 |
| **bg211** | [军事区](bg211_军事区/bg211_军事区.md) | 城区 | — | 墙上挂满盾牌与战斧的环形厅，地面铺深色石板，角落是训练假人与兵器架，灯光偏暗偏红 |
| **bg212** | [秘法区](bg212_秘法区/bg212_秘法区.md) | 城区 | — | 一圈安静的蓝调厅堂，石柱之间悬着发光的符文水盆，水从壁槽流下来，光线比别处冷得多 |
| **bg213** | [侏儒区](bg213_侏儒区/bg213_侏儒区.md) | 城区 | — | 挤满黄铜管道与蒸汽阀的侏儒区，中央一台巨大的球形机械上架着一把小王座，四周是零件摊与冒火花的工作台 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 图书馆（`the_library_ironforge` · 子区域） → 属 探险者大厅
- The Museum（`the_museum_ironforge` · 子区域） → 属 探险者大厅
- 铁炉堡拍卖行（`ironforge_auction_house` · 地标） → 属 平民区
- 铁炉堡金库（`vault_of_ironforge` · 地标） → 属 平民区
- 酒桶与铁砧（`cask_n_anvil` · 聚居点 · inn） → 属 大锻炉
- 铁炉堡飞行点（`fp_ironforge` · transport · flightpath） → 属 大锻炉
- 铁炉堡狮鹫场（`ironforge_gryphon_roost` · transport · flightpath） → 属 大锻炉
- 大铁砧（`the_great_anvil` · 地标） → 属 大锻炉
- Bruuk's Corner（`bruuks_corner` · 聚居点 · inn） → 属 军事区
- 石火旅店（`the_stonefire_tavern` · 聚居点 · inn） → 属 军事区
- Berryfizz's Potions and Mixed Drinks（`berryfizzs_potions` · 地标） → 属 侏儒区
- 矿道地铁（`deeprun_tram_ironforge` · transport · tram） → 属 侏儒区
- 矿道地铁·铁炉堡站（`deeprun_tram_ironforge_station` · transport · tram） → 属 侏儒区
- 矿道地铁铁炉堡口·巨型齿轮门（`deeprun_tram_ironforge_gear_gate` · 地标） → 属 矿道地铁·铁炉堡站
