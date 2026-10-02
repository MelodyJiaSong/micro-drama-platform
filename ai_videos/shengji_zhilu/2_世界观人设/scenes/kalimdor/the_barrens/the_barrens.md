# 贫瘠之地（The Barrens）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg707_贫瘠之地全境/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/kalimdor/the_barrens/`（卡利姆多 → 贫瘠之地），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 地区 · 10-25 级 · contested |
| 相邻 | 杜隆塔尔 · 莫高雷 · 石爪山脉 · 灰谷 · 尘泥沼泽 · 千针石林 |
| 世界地图尺寸 | 9265.9 × 6177.9 m（坐标表：WorldMapArea：10133.3 × 6756.2 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 一望无际的赭黄干草原，土黄的硬土路笔直穿过，稀疏的伞状金合欢树投下细影，低矮的红褐山脊当作天然边界 |
| 备注 | 旧世是**一整块**地区（10-25 级），南北连通不断；4.0.3a 才被大裂谷劈成北/南贫瘠之地两个 zone。部落玩家的集体记忆之地 |
| 出处 | https://warcraft.wiki.gg/wiki/Barrens |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-Barrens_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/kalimdor/central_kalimdor/the_barrens/WorldMap-Barrens_c60.jpg`
- `ref/WorldMap-MicroDungeon-Barrens-WailingCavernsBarrens.jpg.link.json` → 微型地下城图

## 区级场地平面图

`bg707_贫瘠之地全境/planning/bg707_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（30 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg707** | [贫瘠之地全境](bg707_贫瘠之地全境/bg707_贫瘠之地全境.md) | 自造 | — |  |
| **bg708** | [巴尔莫丹](bg708_巴尔莫丹/bg708_巴尔莫丹.md) | 聚居点 · mine | — | 南端一座矮墩墩的矮人石堡加一门巨型火炮，堡下是层层掘开的露天矿坑，脚手架与矿车轨道盘绕而下 |
| **bg709** | [陶拉祖营地](bg709_陶拉祖营地/bg709_陶拉祖营地.md) | 聚居点 · town | — | 草原上一片牛头人营地，高大的圆锥兽皮大帐围成环，帐顶垂着彩绘布条与羽饰，中央是长燃的篝火 |
| **bg710** | [前沿哨所](bg710_前沿哨所/bg710_前沿哨所.md) | 聚居点 · tower | — | 路边一座木石瞭望塔加一座兽人地穴，旁边立着两台蒙皮的投石车，南面有一圈狼栏 |
| **bg711** | [格罗多姆农场](bg711_格罗多姆农场/bg711_格罗多姆农场.md) | 聚居点 · farm | — | 路边一圈木栅围起的猪圈与两座兽人草顶棚屋，苦工赶着黑毛野猪，地上全是拱翻的干土 |
| **bg712** | [莫尔杉营地](bg712_莫尔杉营地/bg712_莫尔杉营地.md) | 聚居点 · camp | — | 壁垒南侧一小片兽人营帐与拴狼桩，营中立着战歌氏族的黑红狼头旗 |
| **bg713** | [北方城堡](bg713_北方城堡/bg713_北方城堡.md) | 聚居点 · tower | — | 海岸边一座石砌联盟要塞，方塔与雉堞城墙，蓝白狮鹫旗猎猎，墙下是成排的帐篷与投石机 |
| **bg714** | [棘齿城](bg714_棘齿城/bg714_棘齿城.md) | 聚居点 · port | — | 东海岸的哥布林港镇，铁皮与杂木拼起来的歪斜房子沿栈桥排开，吊车与货箱堆在码头上，空气里有油烟味 |
| **bg715** | [十字路口](bg715_十字路口/bg715_十字路口.md) | 聚居点 · crossroads | — | 两条土路交叉处的兽人小镇，一圈尖木桩墙围着几座半埋入土的兽人地穴与兽皮尖顶帐，路口立着高大的木制部落旗杆 |
| **bg716** | [莫尔杉壁垒](bg716_莫尔杉壁垒/bg716_莫尔杉壁垒.md) | 聚居点 · tower | — | 北端路口上的一道临时防御工事，削尖的原木栅栏配两座木制哨塔，塔上挂着部落旗，背后是灰谷的深绿林线 |
| **bg717** | [阿迦玛戈](bg717_阿迦玛戈/bg717_阿迦玛戈.md) | 子区域 | [44, 50] | 路北一片荆棘环绕的野猪人营地，圆顶草棚与插地木刺围成圈，地上散落血色的碎晶 |
| **bg718** | [黑棘山](bg718_黑棘山/bg718_黑棘山.md) | 子区域 | — | 长满黑色带刺灌木的一道山脊，脊顶一处小营地，脊下有一汪格外清澈的水潭 |
| **bg719** | [石矿洞](bg719_石矿洞/bg719_石矿洞.md) | 子区域 | — | 东北山壁上的矿洞口，洞外是兽人式的木架与红黑旗，矿车轨道从洞里伸出来 |
| **bg720** | [迅猛龙平原](bg720_迅猛龙平原/bg720_迅猛龙平原.md) | 子区域 | — | 路南一片带刺灌木围出的野猪人营地，草棚低矮，四周是被刨开的干土与骨堆 |
| **bg721** | [鬼雾峰](bg721_鬼雾峰/bg721_鬼雾峰.md) | 子区域 | — | 一座孤立的高岩峰，越往上空气越红越浊，峰顶被一层暗红雾罩住，能见度极低 |
| **bg722** | [巨人旷野](bg722_巨人旷野/bg722_巨人旷野.md) | 子区域 | — | 南部一大片开阔草场，成群的巨型科多兽在其中缓慢游走，地上零星散着巨大的白骨 |
| **bg723** | [勇士岛](bg723_勇士岛/bg723_勇士岛.md) | 子区域 | — | 东海岸外一座干燥小岛，一条贯穿全岛的石砌水道，岛上只有沙土与零星干草 |
| **bg724** | [荣耀岗哨](bg724_荣耀岗哨/bg724_荣耀岗哨.md) | 子区域 | — | 西路边上几座兽人地穴与两座木制哨塔，其中一部分被打塌了一半，苦工正在修补 |
| **bg725** | [甜水绿洲](bg725_甜水绿洲/bg725_甜水绿洲.md) | 子区域 | — | 十字路口正南的绿洲，几潭深碧的水被高棕榈围住，水汽让空气比周围凉，池边有一处向下的黑洞口 |
| **bg726** | [迅猛龙巢穴](bg726_迅猛龙巢穴/bg726_迅猛龙巢穴.md) | 子区域 | — | 一小块凹下去的谷地，散着迅猛龙用树枝与骨头搭起来的粗糙窝棚，地上亮闪闪的拾来物堆成小丘 |
| **bg727** | [剃刀高地](bg727_剃刀高地/bg727_剃刀高地.md) | 子区域 | — | 更南端的荆棘丘陵，藤刺更黑更枯，丘顶露出插在荆棘里的白骨与低矮的石冢 |
| **bg728** | [剃刀沼泽](bg728_剃刀沼泽/bg728_剃刀沼泽.md) | 子区域 | — | 南端西侧一大片高过人头的黑色荆棘丛，藤刺盘绕成拱与墙，中间只留一条勉强通过的窄道 |
| **bg729** | [南贫瘠之地](bg729_南贫瘠之地/bg729_南贫瘠之地.md) | 子区域 | — | 同一片赭黄草原的南半，草色更枯、红土裸露更多，地平线上是千针石林方向的台地剪影 |
| **bg730** | [无水岭](bg730_无水岭/bg730_无水岭.md) | 子区域 | — | 西北角的一片矮丘，反而是全区最绿的地方，草色偏青，崖上是鹰身女妖的枝巢 |
| **bg731** | [遗忘之池](bg731_遗忘之池/bg731_遗忘之池.md) | 子区域 | — | 干草原上一小片突兀的翠绿绿洲，几汪清水围着高大的棕榈与芦苇，水边长着独有的沉重蘑菇 |
| **bg732** | [商旅海岸](bg732_商旅海岸/bg732_商旅海岸.md) | 子区域 | — | 贫瘠之地的东侧海岸线，黄土断崖直落到青蓝浅海，崖下是细碎的贝壳沙滩 |
| **bg733** | [淤泥沼泽](bg733_淤泥沼泽/bg733_淤泥沼泽.md) | 子区域 | — | 东北角一片被钻井污染的黑色油泊，木架井塔与锈铁管道横在泥面上，油光在日光下泛彩 |
| **bg734** | [死水绿洲](bg734_死水绿洲/bg734_死水绿洲.md) | 子区域 | — | 水色发暗发绿的一片死水塘，浮着厚厚的水藻，岸边芦苇枯黄，几头瘦弱的科多兽独自饮水 |
| **bg735** | [提度斯阶梯](bg735_提度斯阶梯/bg735_提度斯阶梯.md) | 子区域 | — | 海边一组天然形成的层层岩台，像被凿出的巨型石阶一级级落向海面 |
| **bg736** | [荆棘岭](bg736_荆棘岭/bg736_荆棘岭.md) | 子区域 | — | 山顶北坡上一大片野猪人聚落，草泥圆顶棚屋一座挨一座，四处插着削尖的木刺与骨制图腾 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 黄金之路（`gold_road` · 地标）
- 无尽之海（`great_sea_barrens` · 地标）
- 战士之魂神殿（`shrine_of_the_fallen_warrior` · 地标）
- 南黄金之路（`southern_gold_road` · 地标）
- 怒水河（`southfury_river_barrens` · 地标）
- 升降梯（`the_great_lift_barrens` · transport · tram）
- 巴尔丹城堡（`bael_dun_keep` · 地标） → 属 巴尔莫丹
- 陶拉祖营地飞行点（`camp_taurajo_flightpath` · transport · flightpath） → 属 陶拉祖营地
- 鬼雾兽穴（`dreadmist_den` · 地标） → 属 鬼雾峰
- 哀嚎洞穴（`wailing_caverns` · dungeon） → 属 甜水绿洲
- 战歌峡谷战场入口（部落侧）（`warsong_gulch_horde_entrance` · transport · portal） → 属 莫尔杉营地
- 破船旅店（`broken_keel_tavern` · 地标） → 属 棘齿城
- 棘齿城·藏宝海湾航线码头（`dock_ratchet_to_booty_bay` · transport · boat） → 属 棘齿城
- 棘齿城飞行点（中立）（`fp_ratchet` · transport · flightpath） → 属 棘齿城
- 棘齿城—藏宝海湾航线（`ratchet_booty_bay_boat` · transport · boat） → 属 棘齿城
- 棘齿城飞行点（`ratchet_flightpath` · transport · flightpath） → 属 棘齿城
- 剃刀高地（`razorfen_downs` · dungeon） → 属 剃刀高地
- 剃刀沼泽（`razorfen_kraul` · dungeon） → 属 剃刀沼泽
- 十字路口飞行点（`crossroads_flightpath` · transport · flightpath） → 属 十字路口
- 十字路口飞行点（`fp_crossroads` · transport · flightpath） → 属 十字路口
- 迷雾洞穴（`cavern_of_mists` · 子区域） → 属 哀嚎洞穴
- 永生峭壁（`crag_of_the_everliving` · 子区域） → 属 哀嚎洞穴
- Deviate Faerie Dragon（`deviate_faerie_dragon` · 地标） → 属 哀嚎洞穴
- 梦境之岩（`dreamers_rock` · 子区域） → 属 哀嚎洞穴
- 克雷什（`kresh` · 地标） → 属 哀嚎洞穴
- 安娜科德拉（`lady_anacondra` · 地标） → 属 哀嚎洞穴
- 考布莱恩（`lord_cobrahn` · 地标） → 属 哀嚎洞穴
- 皮萨斯（`lord_pythas` · 地标） → 属 哀嚎洞穴
- 瑟芬迪斯（`lord_serpentis` · 地标） → 属 哀嚎洞穴
- 吞噬者穆坦努斯（`mutanus_the_devourer` · 地标） → 属 哀嚎洞穴
- 尖牙之巢（`pit_of_fangs` · 子区域） → 属 哀嚎洞穴
- 尖啸沟壑（`screaming_gully` · 子区域） → 属 哀嚎洞穴
- 斯卡姆（`skum` · 地标） → 属 哀嚎洞穴
- 永生者沃尔丹（`verdan_the_everliving` · 地标） → 属 哀嚎洞穴
- 迷雾洞穴（`wc_cavern_of_mists` · 子区域） → 属 哀嚎洞穴
- 永生峭壁（`wc_crag_of_the_everliving` · 子区域） → 属 哀嚎洞穴
- 美梦石（`wc_dreamers_rock` · 子区域） → 属 哀嚎洞穴
- 毒牙深渊（`wc_pit_of_fangs` · 子区域） → 属 哀嚎洞穴
- 激流溪谷（`wc_screaming_gully` · 子区域） → 属 哀嚎洞穴
- 狂风裂口（`wc_winding_chasm` · 子区域） → 属 哀嚎洞穴
- 蜿蜒裂隙（`winding_chasm` · 子区域） → 属 哀嚎洞穴
- 寒冰之王亚门纳尔（`amnennar_the_coldbringer` · 地标） → 属 剃刀高地
- 暴食者（`glutton` · 地标） → 属 剃刀高地
- 火眼莫德雷斯（`mordresh_fire_eye` · 地标） → 属 剃刀高地
- 腐烂的普雷莫尔（`plaguemaw_the_rotting` · 地标） → 属 剃刀高地
- 拉戈斯诺特（`ragglesnout` · 地标） → 属 剃刀高地
- 荆棘螺旋（`rfd_spiral_of_thorns` · 子区域） → 属 剃刀高地
- 白骨之堆（`rfd_the_bone_pile` · 子区域） → 属 剃刀高地
- 召唤者之厅（`rfd_the_callers_chamber` · 子区域） → 属 剃刀高地
- 谋杀者围栏（`rfd_the_murder_pens` · 子区域） → 属 剃刀高地
- 图特卡什（`tutenkash` · 地标） → 属 剃刀高地
- 暴怒的阿迦赛罗斯（`agathelos_the_raging` · 地标） → 属 剃刀沼泽
- 阿格姆（`aggem_thorncurse` · 地标） → 属 剃刀沼泽
- Blind Hunter（`blind_hunter` · 地标） → 属 剃刀沼泽
- 卡尔加·刺肋（`charlga_razorflank` · 地标） → 属 剃刀沼泽
- 亡语者贾格巴（`death_speaker_jargba` · 地标） → 属 剃刀沼泽
- Earthcaller Halmgar（`earthcaller_halmgar` · 地标） → 属 剃刀沼泽
- 主宰拉姆塔斯（`overlord_ramtusk` · 地标） → 属 剃刀沼泽
- 鲁古格（`roogug` · 地标） → 属 剃刀沼泽
