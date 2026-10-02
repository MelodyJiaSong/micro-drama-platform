# 西瘟疫之地（Western Plaguelands）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg369_西瘟疫之地全境/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/eastern_kingdoms/western_plaguelands/`（东部王国 → 西瘟疫之地），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 地区 · 50-60 级 · contested |
| 相邻 | 提瑞斯法林地 · 东瘟疫之地 · 奥特兰克山脉 |
| 世界地图尺寸 | 3931.9 × 2621.3 m（坐标表：WorldMapArea：4300.0 × 2866.7 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 病态的灰橙色丘陵农田，枯死的白杨与歪斜篱笆，空气里浮着淡绿瘟疫雾，废弃农舍的屋顶大多塌了一半 |
| 备注 | 旧世 50-60 级争夺区（常用练级带 51-58）；联盟据点寒风营地、部落据点亡灵壁垒，通灵学院入口在凯尔达隆岛。西接提瑞斯法林地（经亡灵壁垒）、东接东瘟疫之地（经索多里尔河桥）、西南经奥特兰克山脉下希尔斯布莱德 |
| 出处 | https://warcraft.wiki.gg/wiki/Western_Plaguelands |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-WesternPlaguelands_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/eastern_kingdoms/lordaeron/western_plaguelands/WorldMap-WesternPlaguelands_c60.jpg`


## 区级场地平面图

`bg369_西瘟疫之地全境/planning/bg369_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（14 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg369** | [西瘟疫之地全境](bg369_西瘟疫之地全境/bg369_西瘟疫之地全境.md) | 自造 | — |  |
| **bg370** | [寒风营地](bg370_寒风营地/bg370_寒风营地.md) | 聚居点 · camp | [43, 85] | 山口处一圈帆布军帐与木栅，中央一堆常燃的篝火，帐外堆着补给箱与拒马 |
| **bg371** | [达尔松之泪](bg371_达尔松之泪/bg371_达尔松之泪.md) | 聚居点 · farm | — | 大路边的农庄，主屋门窗尽毁、田垄长满枯草，院角同样架着一口冒绿烟的瘟疫大锅 |
| **bg372** | [费尔斯通农场](bg372_费尔斯通农场/bg372_费尔斯通农场.md) | 聚居点 · farm | — | 荒废的农庄，塌了一半的谷仓与倒伏的篱笆，院子正中架着一口冒绿烟的大铁锅 |
| **bg373** | [盖罗恩农场](bg373_盖罗恩农场/bg373_盖罗恩农场.md) | 聚居点 · farm | — | 东北角最偏的一座农庄，果园的树全枯成黑色枝杈，院中大锅下的火还没灭 |
| **bg374** | [壁炉谷](bg374_壁炉谷/bg374_壁炉谷.md) | 聚居点 · town | — | 北部山坳里一座还完整的人类城镇，红瓦白墙的联排房屋沿坡而上，镇顶是一座带塔楼的石堡，血色十字军的红白旗帜到处都是 |
| **bg375** | [北山伐木场](bg375_北山伐木场/bg375_北山伐木场.md) | 聚居点 · camp | — | 山腰上的伐木营，倒伏的原木堆成小山，锯架与木屋散落在被砍秃的林地里 |
| **bg376** | [安多哈尔废墟](bg376_安多哈尔废墟/bg376_安多哈尔废墟.md) | 聚居点 · ruin | — | 一整座被烧空的人类城镇废墟，石墙焦黑、屋顶塌尽，街巷间立着倾斜的钟楼与成排的粮仓残架 |
| **bg377** | [嚎哭鬼屋](bg377_嚎哭鬼屋/bg377_嚎哭鬼屋.md) | 聚居点 · farm | — | 一处被鬼影缠住的农庄，谷仓门大敞、屋里浮着惨绿的光，院中大锅旁排着一列尸堆 |
| **bg378** | [凯尔达隆](bg378_凯尔达隆/bg378_凯尔达隆.md) | 子区域 | [70, 73] | 湖心孤岛上的城堡废墟，只剩外墙与几根断柱，岛上飘着半透明的幽灵村民，一条石桥从岸边通上岛 |
| **bg379** | [达隆米尔湖](bg379_达隆米尔湖/bg379_达隆米尔湖.md) | 子区域 | — | 一片灰绿色的大湖，湖面浮着薄雾与枯木，湖心是一座立着废墟城堡的孤岛 |
| **bg380** | [悔恨岭](bg380_悔恨岭/bg380_悔恨岭.md) | 子区域 | — | 一整片缓坡墓地，成百上千的歪斜墓碑排到山脊线，坡顶是一座独立的圆形石砌陵墓 |
| **bg381** | [哭泣之洞](bg381_哭泣之洞/bg381_哭泣之洞.md) | 子区域 | [65, 39] | 岩壁下的低矮洞口，洞内常年滴水，地面积着浅水洼，钟乳上挂着灰绿色黏液 |
| **bg382** | [索多里尔河](bg382_索多里尔河/bg382_索多里尔河.md) | 子区域 | — | 一条南北向的宽河，河水浑浊发灰，主路在此跨一座石桥过河，桥头有废弃的岗亭 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 冷风营地飞行点（`fp_chillwind_camp` · transport · flightpath） → 属 寒风营地
- 玛登霍尔德城堡（`mardenholde_keep` · 子区域） → 属 壁炉谷
- 墓穴（`sorrow_hill_crypt` · 子区域） → 属 悔恨岭
- 乌瑟尔之墓（`uthers_tomb` · 地标） → 属 悔恨岭
- 通灵学院（`scholomance` · dungeon） → 属 凯尔达隆
- 通灵学院入口（`scholomance_entrance` · 地标） → 属 凯尔达隆
- 通灵术学校（`school_of_necromancy` · 子区域） → 属 凯尔达隆
- 黑暗院长加丁（`darkmaster_gandling` · 地标） → 属 通灵学院
- 瑟尔林·卡斯迪诺夫教授（`doctor_theolen_krastinov` · 地标） → 属 通灵学院
- 讲师玛丽希亚（`instructor_malicia` · 地标） → 属 通灵学院
- 詹迪斯·巴罗夫（`jandice_barov` · 地标） → 属 通灵学院
- 基尔图诺斯（`kirtonos` · 地标） → 属 通灵学院
- 库尔莫克（`kormok` · 地标） → 属 通灵学院
- 伊露希亚·巴罗夫（`lady_illucia_barov` · 地标） → 属 通灵学院
- 阿雷克斯·巴罗夫（`lord_alexei_barov` · 地标） → 属 通灵学院
- 博学者普克尔特（`lorekeeper_polkelt` · 地标） → 属 通灵学院
- 马杜克·布莱克波尔（`marduk_blackpool` · 地标） → 属 通灵学院
- 莱斯·霜语（`ras_frostwhisperer` · 地标） → 属 通灵学院
- 血骨傀儡（`rattlegore` · 地标） → 属 通灵学院
- 巴罗夫家族宝库（`scholo_barov_family_vault` · 子区域） → 属 通灵学院
- 召唤大厅（`scholo_chamber_of_summoning` · 子区域） → 属 通灵学院
- 秘密之厅（`scholo_hall_of_secrets` · 子区域） → 属 通灵学院
- 谴责之厅（`scholo_hall_of_the_damned` · 子区域） → 属 通灵学院
- 院长的书房（`scholo_headmasters_study` · 子区域） → 属 通灵学院
- 巫师会所（`scholo_the_coven` · 子区域） → 属 通灵学院
- 尸骨储藏所（`scholo_the_great_ossuary` · 子区域） → 属 通灵学院
- 实验室（`scholo_the_laboratory` · 子区域） → 属 通灵学院
- 遗骨之穴（`scholo_the_reliquary` · 子区域） → 属 通灵学院
- 暗影墓穴（`scholo_the_shadow_vault` · 子区域） → 属 通灵学院
- 沉没的墓穴（`scholo_the_sunken_catacombs` · 子区域） → 属 通灵学院
- 诗歌之厅（`scholo_the_vault_of_the_poets` · 子区域） → 属 通灵学院
- 观察室（`scholo_the_viewing_room` · 子区域） → 属 通灵学院
- 掠夺者灵堂（`scholo_vault_of_the_ravenian` · 子区域） → 属 通灵学院
- 拉文尼亚（`the_ravenian` · 地标） → 属 通灵学院
- 维克图斯（`vectus` · 地标） → 属 通灵学院
