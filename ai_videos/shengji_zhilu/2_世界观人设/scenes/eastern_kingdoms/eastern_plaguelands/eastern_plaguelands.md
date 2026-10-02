# 东瘟疫之地（Eastern Plaguelands）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg142_东瘟疫之地全境/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/eastern_kingdoms/eastern_plaguelands/`（东部王国 → 东瘟疫之地），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 地区 · 55-60 级 · contested |
| 相邻 | 西瘟疫之地 |
| 世界地图尺寸 | 3539.5 × 2360.3 m（坐标表：WorldMapArea：3870.8 × 2581.2 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 猩红橙色的毒土荒原，天空压着暗红云层，枯焦的黑色树干成片倒伏，地面裂口里渗出发亮的绿色脓液 |
| 备注 | 旧世 55-60 级争夺区（常用练级带 53-60），全大陆瘟疫最深的一块；斯坦索姆与纳克萨玛斯都在此。旧世唯一陆路入口是西面索多里尔河桥——北面的塔拉斯通道在旧世封死（燃烧的远征才通往幽暗森林），与辛特兰之间无陆路 |
| 出处 | https://warcraft.wiki.gg/wiki/Eastern_Plaguelands |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-EasternPlaguelands_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/eastern_kingdoms/lordaeron/eastern_plaguelands/WorldMap-EasternPlaguelands_c60.jpg`
- `ref/WorldMap-MicroDungeon-EasternPlaguelands-PaladinClassShrine.jpg.link.json` → 微型地下城图

## 区级场地平面图

`bg142_东瘟疫之地全境/planning/bg142_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（30 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg142** | [东瘟疫之地全境](bg142_东瘟疫之地全境/bg142_东瘟疫之地全境.md) | 自造 | — |  |
| **bg143** | [布洛米尔](bg143_布洛米尔/bg143_布洛米尔.md) | 聚居点 · farm | [77, 51] | 东部一座废弃的磨坊，风车叶片只剩骨架，磨坊旁堆着发霉的麦袋 |
| **bg144** | [考林路口](bg144_考林路口/bg144_考林路口.md) | 聚居点 · crossroads | — | 两条大路交汇处的小镇废墟，十字路口四角各一栋烧空的房子，路中央翻着一辆废弃货车 |
| **bg145** | [皇冠哨塔](bg145_皇冠哨塔/bg145_皇冠哨塔.md) | 聚居点 · tower | [40, 75] | 南部路边一座方形石塔，外墙有箭孔，塔基周围堆着沙袋与破损的旗杆 |
| **bg146** | [达隆郡](bg146_达隆郡/bg146_达隆郡.md) | 聚居点 · ruin | — | 南部一座只剩地基与断墙的小村废墟，村中十字路口立着半塌的石碑，夜里会浮出半透明的村民幽灵 |
| **bg147** | [东墙哨塔](bg147_东墙哨塔/bg147_东墙哨塔.md) | 聚居点 · tower | [67, 48] | 东部大路旁的石塔，塔顶垛口塌了一角，塔下是被压弯的木栅与散落的兵器 |
| **bg148** | [圣光之愿礼拜堂](bg148_圣光之愿礼拜堂/bg148_圣光之愿礼拜堂.md) | 聚居点 · town | [82, 59] | 焦土荒原中一小块仍是绿色的圣地，白石小教堂立在中央，彩窗透出暖光，四周围着银色黎明的帐篷与拒马 |
| **bg149** | [北谷](bg149_北谷/bg149_北谷.md) | 聚居点 · ruin | — | 北部山谷里的村镇废墟，成排的石墙房子只剩外壳，街道被塌下的屋梁堵住 |
| **bg150** | [北地哨塔](bg150_北地哨塔/bg150_北地哨塔.md) | 聚居点 · tower | [57, 24] | 北部路口的石塔，塔身最完整，塔前有一口废井与拴马的石桩 |
| **bg151** | [病木林哨塔](bg151_病木林哨塔/bg151_病木林哨塔.md) | 聚居点 · tower | [22, 32] | 枯林中一座方形石塔，塔身爬满黑色霉斑，顶层的窗口透出绿光 |
| **bg152** | [奎尔林斯小屋](bg152_奎尔林斯小屋/bg152_奎尔林斯小屋.md) | 聚居点 · village | — | 北部林边的高等精灵木屋群，蓝金配色的尖顶与雕花立柱，院里立着精灵样式的灯柱 |
| **bg153** | [血色十字军营地](bg153_血色十字军营地/bg153_血色十字军营地.md) | 聚居点 · camp | — | 荒原上的一小片红白帐篷，中间竖着血色十字军的旗杆，外围是木尖桩与巡逻的骑兵 |
| **bg154** | [恐惧谷](bg154_恐惧谷/bg154_恐惧谷.md) | 聚居点 · ruin | — | 最北端的废镇，被浓密的灰绿毒雾整个罩住，只能看见房屋的黑色轮廓 |
| **bg155** | [玛瑞斯农场](bg155_玛瑞斯农场/bg155_玛瑞斯农场.md) | 聚居点 · farm | — | 荒原上一座还立着的两层农舍，木栅围出的院子里拴着几匹瘦马，屋内点着灯 |
| **bg156** | [提尔之手](bg156_提尔之手/bg156_提尔之手.md) | 聚居点 · town | — | 东南角一座保存完好的人类城镇，白墙红顶、街道整洁，血色十字军的红白旗挂满街口，中央是一座高耸的大教堂 |
| **bg157** | [黑木湖](bg157_黑木湖/bg157_黑木湖.md) | 子区域 | — | 一潭近乎墨色的死水湖，湖面浮着一层油膜，岸边立着成片泡烂的枯树桩 |
| **bg158** | [达隆米尔湖](bg158_达隆米尔湖/bg158_达隆米尔湖.md) | 子区域 | — | 达隆米尔湖伸进东瘟疫之地一侧的水面，灰绿色、岸边全是枯死的芦苇 |
| **bg159** | [禁忌之海](bg159_禁忌之海/bg159_禁忌之海.md) | 子区域 | — | 东岸外的外海，海水颜色比南方更灰冷，近岸漂着从陆上冲下来的枯木 |
| **bg160** | [米雷达尔湖](bg160_米雷达尔湖/bg160_米雷达尔湖.md) | 子区域 | — | 东南部的大湖，水色比其他水面清一些，湖岸仍有零星绿草，对岸就是提尔之手的白墙 |
| **bg161** | [瘟疫之痕](bg161_瘟疫之痕/bg161_瘟疫之痕.md) | 子区域 | — | 另一条较浅的瘟疫裂沟，沟沿翻起干裂的土块，沟里积着暗绿色的稠液 |
| **bg162** | [病木林](bg162_病木林/bg162_病木林.md) | 子区域 | — | 西北一片病死的森林，树干发黑、树冠只剩枯枝，林间浮着绿色孢子雾，抬头能看见天上悬着的黑色要塞 |
| **bg163** | [瘟疫要塞](bg163_瘟疫要塞/bg163_瘟疫要塞.md) | 子区域 | [40, 26] | 病木林中一座露天的石砌传送尖塔，塔心地面刻着发绿光的符文圆环，塔外是成圈的骨堆 |
| **bg164** | [斯坦索姆](bg164_斯坦索姆/bg164_斯坦索姆.md) | 子区域 | — | 北部一整座被高墙围死的城，墙内是黑紫色的街区与腐臭的橙色浓雾，塔楼顶端飘着天灾的绿火 |
| **bg165** | [恶蛛隧道](bg165_恶蛛隧道/bg165_恶蛛隧道.md) | 子区域 | [15, 30] | 山体里被蛛丝糊满的隧道，洞壁挂着成串的茧，地面黏腻，深处有暗紫色的微光 |
| **bg166** | [蘑菇谷](bg166_蘑菇谷/bg166_蘑菇谷.md) | 子区域 | — | 一整片长满巨型菌伞的洼地，菌盖呈病态的紫褐色，空气里飘满发光的孢子 |
| **bg167** | [魔刃之痕](bg167_魔刃之痕/bg167_魔刃之痕.md) | 子区域 | — | 大地上一道被撕开的长条裂谷，谷底是翻涌的绿色脓浆，两壁的土是发黑的紫褐色 |
| **bg168** | [剧毒林地](bg168_剧毒林地/bg168_剧毒林地.md) | 子区域 | — | 东北一片死林，树皮剥落露出灰白木质，地面覆着一层黄绿色的毒粉 |
| **bg169** | [墓室](bg169_墓室/bg169_墓室.md) | 子区域 | — | 南部一片下沉的家族墓园，石棺盖被掀开散落一地，围墙内立着几座小型陵屋 |
| **bg170** | [索多里尔河](bg170_索多里尔河/bg170_索多里尔河.md) | 子区域 | — | 东岸一侧的河滩，河水浑灰，桥头石阶通向一片枯草坡 |
| **bg171** | [祖玛沙尔](bg171_祖玛沙尔/bg171_祖玛沙尔.md) | 子区域 | — | 东北高地上的巨魔遗迹群，阶梯式石台与图腾柱立在枯黄的坡地上 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 东墙大门（`eastwall_gate` · 地标）
- 圣光之愿礼拜堂飞行点（`fp_lights_hope_chapel` · transport · flightpath） → 属 圣光之愿礼拜堂
- 圣光之愿礼拜堂飞行点（联盟）（`fp_lights_hope_chapel_alliance` · transport · flightpath） → 属 圣光之愿礼拜堂
- 圣光之愿礼拜堂飞行点（部落）（`fp_lights_hope_chapel_horde` · transport · flightpath） → 属 圣光之愿礼拜堂
- 斯坦索姆（`stratholme_instance` · dungeon） → 属 斯坦索姆
- 斯坦索姆正门（`stratholme_main_gate` · 地标） → 属 斯坦索姆
- 斯坦索姆侧门（`stratholme_service_entrance` · 地标） → 属 斯坦索姆
- 血色十字军教堂（`the_scarlet_basilica` · 子区域） → 属 提尔之手
- 提尔之手修道院（`tyrs_hand_abbey` · 子区域） → 属 提尔之手
- 玛兹拉罗（`mazra_alor` · 子区域） → 属 祖玛沙尔
- 纳克萨玛斯（`naxxramas` · raid） → 属 瘟疫要塞
- 档案管理员加尔福特（`archivist_galford` · 地标） → 属 斯坦索姆
- 巴纳扎尔（`balnazzar` · 地标） → 属 斯坦索姆
- 瑞文戴尔男爵（`baron_rivendare` · 地标） → 属 斯坦索姆
- 安娜丝塔丽男爵夫人（`baroness_anastari` · 地标） → 属 斯坦索姆
- 黑衣守卫铸剑师（`black_guard_swordsmith` · 地标） → 属 斯坦索姆
- 炮手威利（`cannon_master_willey` · 地标） → 属 斯坦索姆
- 红衣铸锤师（`crimson_hammersmith` · 地标） → 属 斯坦索姆
- 艾兹拉·格里姆（`ezra_grimm` · 地标） → 属 斯坦索姆
- 弗雷斯特恩（`hearthsinger_forresten` · 地标） → 属 斯坦索姆
- 巴瑟拉斯镇长（`magistrate_barthilas` · 地标） → 属 斯坦索姆
- 苍白的玛勒基（`maleki_the_pallid` · 地标） → 属 斯坦索姆
- 狂热的玛洛尔（`malor_the_zealous` · 地标） → 属 斯坦索姆
- 奈鲁布恩坎（`nerubenkan` · 地标） → 属 斯坦索姆
- 邮差马龙（`postmaster_malown` · 地标） → 属 斯坦索姆
- 吞咽者拉姆斯登（`ramstein_the_gorger` · 地标） → 属 斯坦索姆
- 斯库尔（`skul` · 地标） → 属 斯坦索姆
- 石脊（`stonespine` · 地标） → 属 斯坦索姆
- 阿隆索斯礼拜堂（`strat_alonsus_chapel` · 子区域） → 属 斯坦索姆
- 安诺通灵塔（`strat_ano_ziggurat` · 子区域） → 属 斯坦索姆
- 贝拉通灵塔（`strat_bera_ziggurat` · 子区域） → 属 斯坦索姆
- 卡达通灵塔（`strat_cadra_ziggurat` · 子区域） → 属 斯坦索姆
- 十字军广场（`strat_crusaders_square` · 子区域） → 属 斯坦索姆
- 长者广场（`strat_elders_square` · 子区域） → 属 斯坦索姆
- 节日小道（`strat_festival_lane` · 子区域） → 属 斯坦索姆
- 圣光大厅（`strat_hall_of_lights` · 子区域） → 属 斯坦索姆
- 国王广场（`strat_kings_square` · 子区域） → 属 斯坦索姆
- 市场区（`strat_market_row` · 子区域） → 属 斯坦索姆
- 血色十字军堡垒（`strat_scarlet_bastion` · 子区域） → 属 斯坦索姆
- 屠杀广场（`strat_slaughter_square` · 子区域） → 属 斯坦索姆
- 赤色王座（`strat_the_crimson_throne` · 子区域） → 属 斯坦索姆
- 街巷（`strat_the_gauntlet` · 子区域） → 属 斯坦索姆
- 物资库（`strat_the_hoard` · 子区域） → 属 斯坦索姆
- 屠宰房（`strat_the_slaughter_house` · 子区域） → 属 斯坦索姆
- 不可宽恕者（`the_unforgiven` · 地标） → 属 斯坦索姆
- 悲惨的提米（`timmy_the_cruel` · 地标） → 属 斯坦索姆
- 阿努布雷坎（`anubrekhan` · 地标） → 属 纳克萨玛斯
- 格拉斯（`gluth` · 地标） → 属 纳克萨玛斯
- 收割者戈提克（`gothik_the_harvester` · 地标） → 属 纳克萨玛斯
- 黑女巫法琳娜（`grand_widow_faerlina` · 地标） → 属 纳克萨玛斯
- 格罗布鲁斯（`grobbulus` · 地标） → 属 纳克萨玛斯
- 肮脏的希尔盖（`heigan_the_unclean` · 地标） → 属 纳克萨玛斯
- 教官拉苏维奥斯（`instructor_razuvious` · 地标） → 属 纳克萨玛斯
- 克尔苏加德（`kelthuzad` · 地标） → 属 纳克萨玛斯
- 洛欧塞布（`loatheb` · 地标） → 属 纳克萨玛斯
- 迈克斯纳（`maexxna` · 地标） → 属 纳克萨玛斯
- Arachnid Quarter（`naxx_arachnid_quarter` · 子区域） → 属 纳克萨玛斯
- Construct Quarter（`naxx_construct_quarter` · 子区域） → 属 纳克萨玛斯
- Frostwyrm Lair（`naxx_frostwyrm_lair` · 子区域） → 属 纳克萨玛斯
- 克尔苏加德的大厅（`naxx_kelthuzad_chamber` · 子区域） → 属 纳克萨玛斯
- Military Quarter（`naxx_military_quarter` · 子区域） → 属 纳克萨玛斯
- Plague Quarter（`naxx_plague_quarter` · 子区域） → 属 纳克萨玛斯
- 冰霜巨龙的大厅（`naxx_sapphirons_lair` · 子区域） → 属 纳克萨玛斯
- 瘟疫使者诺斯（`noth_the_plaguebringer` · 地标） → 属 纳克萨玛斯
- 帕奇维克（`patchwerk` · 地标） → 属 纳克萨玛斯
- 萨菲隆（`sapphiron` · 地标） → 属 纳克萨玛斯
- 塔迪乌斯（`thaddius` · 地标） → 属 纳克萨玛斯
- 天启四骑士（`the_four_horsemen` · 地标） → 属 纳克萨玛斯
