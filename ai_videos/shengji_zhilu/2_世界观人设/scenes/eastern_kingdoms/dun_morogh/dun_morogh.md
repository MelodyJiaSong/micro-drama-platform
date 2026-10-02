# 丹莫罗（Dun Morogh）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg106_丹莫罗全境/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/eastern_kingdoms/dun_morogh/`（东部王国 → 丹莫罗），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 地区 · 1-10 级 · alliance |
| 相邻 | 铁炉堡 · 洛克莫丹 |
| 世界地图尺寸 | 4503.4 × 3002.3 m（坐标表：WorldMapArea：4925.0 × 3283.3 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 终年积雪的高山盆地，深绿云杉压着厚雪，灰蓝天光下是冻住的湖面、石砌矮人小屋的红瓦斜顶与冒黑烟的矿车轨道 |
| 备注 | 矮人与侏儒共用的新手区；旧世里唯一的陆路出口是东边南北两条门径通往洛克莫丹，另有铁炉堡大门进城。4.0.3 后地貌大改（新增新工匠镇 / 冰雪谷塌陷等），本树一概不收 |
| 出处 | https://warcraft.wiki.gg/wiki/Dun_Morogh |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-DunMorogh_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/eastern_kingdoms/khaz_modan/dun_morogh/WorldMap-DunMorogh_c60.jpg`
- `ref/WorldMap-MicroDungeon-DunMorogh-ColdridgePass.jpg.link.json` → 微型地下城图
- `ref/WorldMap-MicroDungeon-DunMorogh-Gnomeregan.jpg.link.json` → 微型地下城图
- `ref/WorldMap-MicroDungeon-DunMorogh-GolBolarQuarry.jpg.link.json` → 微型地下城图
- `ref/WorldMap-MicroDungeon-DunMorogh-TheGrizzledDen.jpg.link.json` → 微型地下城图

## 区级场地平面图

`bg106_丹莫罗全境/planning/bg106_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（20 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg106** | [丹莫罗全境](bg106_丹莫罗全境/bg106_丹莫罗全境.md) | 自造 | — |  |
| **bg107** | [冻石农场](bg107_冻石农场/bg107_冻石农场.md) | 聚居点 · farm | [64, 51] | 雪坡上一圈木栅栏围出的牧场，棚屋顶压雪，围栏里站着长毛白羊与几头矮种山羊 |
| **bg108** | [安威玛尔](bg108_安威玛尔/bg108_安威玛尔.md) | 聚居点 · village | [29, 69] | 山谷尽头一座半嵌进岩壁的石砌大屋，门口两盏铁灯笼、屋内一座常烧的火塘，门外雪地上排着一列训练假人 |
| **bg109** | [烈酒村](bg109_烈酒村/bg109_烈酒村.md) | 聚居点 · camp | [31, 46] | 雪地上几顶帆布帐篷加一圈篝火，中间架着一口冒泡的酿酒铜锅，旁边横七竖八堆着空酒桶 |
| **bg110** | [铁环营地](bg110_铁环营地/bg110_铁环营地.md) | 聚居点 · farm | [77, 60] | 湖畔一座带矮石墙的独门院落，院里堆着木箱与考古工具，烟囱冒着细白烟 |
| **bg111** | [卡拉诺斯](bg111_卡拉诺斯/bg111_卡拉诺斯.md) | 聚居点 · village | [46, 52] | 大路边一圈石墙围起的矮人小镇，陡坡屋顶压着厚雪，镇心一座露天铁砧与红火炉，旁边就是冒着麦芽热气的酿酒厂 |
| **bg112** | [雾松避难所](bg112_雾松避难所/bg112_雾松避难所.md) | 聚居点 · camp | [56, 45] | 雪松林里一小片空地，两顶帐篷围着一堆将熄的篝火，树影间常年吊着一层薄雾 |
| **bg113** | [北门哨岗](bg113_北门哨岗/bg113_北门哨岗.md) | 聚居点 · tower | [82, 38] | 门径口的一座方形石塔加一段矮墙，塔顶挂着铁炉堡的铁砧旗，墙根堆着火药桶 |
| **bg114** | [南门哨岗](bg114_南门哨岗/bg114_南门哨岗.md) | 聚居点 · tower | [85, 51] | 隘路口一座石塔与木栅栏哨所，门口架着一门小火炮，旗杆上是铁炉堡旗 |
| **bg115** | [钢架补给站](bg115_钢架补给站/bg115_钢架补给站.md) | 聚居点 · camp | [50, 49] | 卡拉诺斯东边路口的侏儒机械场，铁皮棚下停着几台漏油的蒸汽机械与机械陆行鸟，地上铺着油渍与零件 |
| **bg116** | [寒风峡谷](bg116_寒风峡谷/bg116_寒风峡谷.md) | 子区域 | [36, 54] | 通往诺莫瑞根的那条风口谷地，两侧灰岩壁夹着一条被风吹净的雪路，谷底立着侏儒的废弃管道与歪掉的路标 |
| **bg117** | [寒脊山谷](bg117_寒脊山谷/bg117_寒脊山谷.md) | 子区域 | [32, 71] | 丹莫罗西南角一处被雪山合围的小盆地，一条冻溪穿过缓坡，坡上散着小木屋与训练假人，雪地被踩成泥灰色的小路 |
| **bg118** | [霜鬃巨魔要塞](bg118_霜鬃巨魔要塞/bg118_霜鬃巨魔要塞.md) | 子区域 | [28, 52] | 雪坡下凿开的巨魔洞穴群，洞口插着骨制图腾与兽皮旗，里面燃着幽蓝的火盆与成排的木笼 |
| **bg119** | [古博拉采掘场](bg119_古博拉采掘场/bg119_古博拉采掘场.md) | 子区域 | [69, 56] | 被削成阶梯状的露天石坑，坑壁一层层灰白岩台，坑底停着矿车与木架，深处开着一个黑洞洞的矿道口 |
| **bg120** | [铁炉堡飞行器机坪](bg120_铁炉堡飞行器机坪/bg120_铁炉堡飞行器机坪.md) | 子区域 | [77.9, 22.5] | 铁炉堡东北高处一片被雪峰环抱的山间平谷，两条压实的雪地跑道并排铺开，旁边几栋石砌矮人营房与木塔，停机位上蹲着侏儒式的螺旋 |
| **bg121** | [Newman's Landing](bg121_Newmans-Landing/bg121_Newmans-Landing.md) | 子区域 · ruin | [18.0, 74.5] | 西海岸一处被雪山从内陆完全挡住的小海湾，灰绿海水拍着一座朽烂的木码头，岸上孤零零一栋人类样式的破木屋，门口一台锈蒸馏器、 |
| **bg122** | [闪光岭](bg122_闪光岭/bg122_闪光岭.md) | 子区域 | [41, 39] | 北侧一道结满冰晶的山脊，阳光下岩面泛出细碎反光，脊背上扎着霜鬃巨魔的兽皮帐篷与骨堆 |
| **bg123** | [灰色洞穴](bg123_灰色洞穴/bg123_灰色洞穴.md) | 子区域 | [41, 60] | 南坡林间一处敞口熊窟，洞口垂着冰凌与枯藤，洞内是踩实的泥地、散落的骨头与湿毛皮的腥气 |
| **bg124** | [The Mountain Den](bg124_The-Mountain-Den/bg124_The-Mountain-Den.md) | 子区域 | — | 南门哨岗东北山坡上一个不起眼的黑洞口，洞内是一条短短的岩石通道与一间空荡的圆形石室，没有火光、没有任何摆设，只有积雪从洞 |
| **bg125** | [冻土岭](bg125_冻土岭/bg125_冻土岭.md) | 子区域 | [60, 58] | 一串起伏的雪丘，雪层薄到露出深褐冻土与碎石，稀疏几棵被风压弯的矮松 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 铁炉堡大门（`gates_of_ironforge` · 地标）
- 盔枕湖（`helms_bed_lake` · 地标）
- 涌冰湖（`iceflow_lake` · 地标）
- 北门小径（`north_gate_pass_dun_morogh` · 地标）
- 南门小径（`south_gate_pass_dun_morogh` · 地标）
- 诺莫瑞根（`gnomeregan` · dungeon） → 属 寒风峡谷
- 寒脊山小径（`coldridge_pass` · 地标） → 属 寒脊山谷
- 雷酒酿制厂（`thunderbrew_distillery` · 聚居点 · inn） → 属 卡拉诺斯
- 群体打击者9-60（`crowd_pummeler_9_60` · 地标） → 属 诺莫瑞根
- Dark Iron Ambassador（`dark_iron_ambassador` · 地标） → 属 诺莫瑞根
- 电刑器6000型（`electrocutioner_6000` · 地标） → 属 诺莫瑞根
- 工程实验室（`gnomeregan_engineering_labs` · 子区域） → 属 诺莫瑞根
- 发射台（`gnomeregan_launch_bay` · 子区域） → 属 诺莫瑞根
- 清洁区（`gnomeregan_the_clean_zone` · 子区域） → 属 诺莫瑞根
- 发条小径（`gnomeregan_the_clockwerk_run` · 子区域） → 属 诺莫瑞根
- 宿舍（`gnomeregan_the_dormitory` · 子区域） → 属 诺莫瑞根
- 齿轮大厅（`gnomeregan_the_hall_of_gears` · 子区域） → 属 诺莫瑞根
- 工匠议会（`gnomeregan_tinkers_court` · 子区域） → 属 诺莫瑞根
- 格鲁比斯（`grubbis` · 地标） → 属 诺莫瑞根
- 机械师瑟玛普拉格（`mekgineer_thermaplugg` · 地标） → 属 诺莫瑞根
- 粘性辐射尘（`viscous_fallout` · 地标） → 属 诺莫瑞根
