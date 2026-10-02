# 暴风城（Stormwind City）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg268_暴风城全城/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/eastern_kingdoms/stormwind_city/`（东部王国 → 暴风城），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 主城 · — 级 · alliance |
| 相邻 | 艾尔文森林 |
| 世界地图尺寸 | 1229.2 × 819.6 m（坐标表：WorldMapArea：1344.3 × 896.4 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 白灰石砌的人类王城，若干近似矩形的街区被碧蓝深水运河切开，石拱桥横跨水面，屋顶蓝灰石板、旗幡蓝金配色，每个街区角落都长着结果的苹果树 |
| 备注 | 人类首都；旧世只有两个入口——英雄谷陆路正门与矮人区的矿道地铁（港口是 3.0.2 才有）；全城约 640×600 m、步行穿城 4–5 分钟（sk2:stormwind.city.047/048）；adjacent 只在本节点填（暴风城在世界地图上本身就是一个 zone），见 notes §5 |
| 出处 | https://warcraft.wiki.gg/wiki/Stormwind_City |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-StormwindCity_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/eastern_kingdoms/azeroth_subcontinent/kingdom_of_stormwind/stormwind_city/WorldMap-StormwindCity_c60.jpg`


## 区级场地平面图

`bg268_暴风城全城/planning/bg268_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（11 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg268** | [暴风城全城](bg268_暴风城全城/bg268_暴风城全城.md) | 自造 | — |  |
| **bg10** | [光明大教堂](bg10_光明大教堂/bg10_光明大教堂.md) | 子区域 | — | 极高的石造教堂，主体两侧伸出多组侧翼，屋脊上林立着数量众多的细长尖塔、越靠中心越高；内厅是浅暖白石砌筑、嵌着饱和钴蓝色石 |
| **bg269** | [教堂广场](bg269_教堂广场/bg269_教堂广场.md) | 城区 | — | 一片开阔石铺广场，北端被一座多侧翼、多尖塔的巨大教堂立面完全统治，广场两侧是较矮的市政厅与孤儿院，衬得教堂更高 |
| **bg270** | [矮人区](bg270_矮人区/bg270_矮人区.md) | 城区 | — | 矮胖敦实的石构建筑，门窗比人类区低矮、比例更厚重，铁件与铆钉外露；数处露天广场上并排立着燃着炭火的锻炉与铁砧，橙红火星四 |
| **bg271** | [法师区](bg271_法师区/bg271_法师区.md) | 城区 | — | 一座爬满深绿藤蔓的高塔统领全区，四周是两层的裁缝铺与仓库，门口堆着捆扎布匹与封蜡陶罐，沿街摆着露天咖啡座 |
| **bg272** | [旧城区](bg272_旧城区/bg272_旧城区.md) | 城区 | — | 墙体是发黄发灰的旧石与外露的深褐木构架，街道狭窄曲折、地面湿污，墙面爬着水渍霉斑，屋檐低垂几乎相接，晾衣绳横跨巷口 |
| **bg273** | [运河区](bg273_运河区/bg273_运河区.md) | 城区 | — | 深而清澈的碧蓝水道穿城而过，两岸是大理石步道与系船石桩，堤顶到水面有明显落差，沿岸嵌着一排一两开间宽的小店门脸，石拱桥横 |
| **bg274** | [暴风要塞](bg274_暴风要塞/bg274_暴风要塞.md) | 城区 | — | 建在全城最高岩石台地上的多体量城堡群，主厅居中、四周簇拥方塔圆塔，塔顶覆深蓝灰石板，建筑之间以带连续券拱的高架廊道相连， |
| **bg275** | [花园区](bg275_花园区/bg275_花园区.md) | 城区 | — | 与全城的白石硬铺完全相反——地面是草与土径，高大乔木成荫、树影斑驳，建筑稀疏矮小依树而建，整体色调比别处更绿更柔；正中一 |
| **bg276** | [贸易区](bg276_贸易区/bg276_贸易区.md) | 城区 | — | 全城最中心也最吵的街区，两三层白石商铺围合出一片开阔石板广场，底层开敞为铺面、上层住人，摊位与行商挤满街面，正中一座石砌 |
| **bg277** | [英雄谷](bg277_英雄谷/bg277_英雄谷.md) | 城区 | — | 城门内外一整块绿意盎然的天然盆地，一座宽阔石桥横跨谷底的窄护城水面，桥两侧立着远超真人尺度的巨型石雕像，主路尽头在雕像前 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 暴风城城墙（`stormwind_city_walls` · 地标）
- 阿隆索斯·法奥纪念碑（`alonsus_faol_monument` · 地标） → 属 教堂广场
- 银色黎明（暴风城）（`argent_dawn_stormwind` · 子区域） → 属 教堂广场
- 战锤专卖店（`just_maces` · 子区域） → 属 教堂广场
- 正义之甲（`righteous_plates` · 子区域） → 属 教堂广场
- 城市大厅（`stormwind_city_hall` · 子区域） → 属 教堂广场
- 孤儿院（`stormwind_orphanage` · 子区域） → 属 教堂广场
- 割喉小巷（`cut_throat_alley` · 子区域） → 属 矮人区
- 矿道地铁齿轮隧道口（`deeprun_tram_cog_entrance` · 地标） → 属 矮人区
- 矿道地铁·暴风城站（`deeprun_tram_stormwind_station` · transport · tram） → 属 矮人区
- 露天锻造广场（`dwarven_district_forges` · 地标） → 属 矮人区
- 矮人区北部水井（`dwarven_district_well` · 地标） → 属 矮人区
- 石手矿业（`stonehand_mining` · 子区域） → 属 矮人区
- 炼金材料店（`alchemy_needs` · 子区域） → 属 法师区
- 古董店（`ancient_curios` · 子区域） → 属 法师区
- 蓝色隐士（`blue_recluse` · 子区域） → 属 法师区
- 邓肯的织物面料（`duncans_textiles` · 子区域） → 属 法师区
- 基本部件（`essential_components` · 子区域） → 属 法师区
- 拉尔森服装店（`larson_clothiers` · 子区域） → 属 法师区
- 法师区水井（`mage_quarter_well` · 地标） → 属 法师区
- 焰火店（`pyrotechnics` · 子区域） → 属 法师区
- 已宰的羔羊（`slaughtered_lamb` · 子区域） → 属 法师区
- 暴风法杖店（`stormwind_staves` · 子区域） → 属 法师区
- 巫师圣殿（`wizards_sanctum` · 子区域） → 属 法师区
- 勇士大厅（`champions_hall` · 子区域） → 属 旧城区
- 五种剧毒（`five_deadly_venoms` · 子区域） → 属 旧城区
- 重装武器（`heavy_handed_weapons` · 子区域） → 属 旧城区
- 诚实之刃（`honest_blades` · 子区域） → 属 旧城区
- 有限防护（`limited_immunity` · 子区域） → 属 旧城区
- 旧城区铁闸门（`old_town_portcullis` · 地标） → 属 旧城区
- 猪和哨声旅店（`pig_and_whistle_tavern` · 子区域） → 属 旧城区
- 护体皮甲（`protective_hide` · 子区域） → 属 旧城区
- 军情七处（`si7_stormwind` · 子区域） → 属 旧城区
- 白银之盾（`silver_shield` · 子区域） → 属 旧城区
- 指挥中心（`stormwind_command_center` · 子区域） → 属 旧城区
- 希恩靴店（`thanes_boots` · 子区域） → 属 旧城区
- Library of the Academy of Arcane Arts and Sciences（`academy_of_arcane_arts_library` · 子区域） → 属 运河区
- 运河裁缝店（`canal_tailor_and_fit_shop` · 子区域） → 属 运河区
- 运河边的附魔师铺子（`canals_enchanting_shop` · 地标） → 属 运河区
- 运河木码头（`canals_fishing_docks` · 地标） → 属 运河区
- 教堂广场↔矮人区人行桥（`cathedral_dwarven_footbridge` · 地标） → 属 运河区
- The Finest Thread（`finest_thread` · 子区域） → 属 运河区
- 芳香的花朵（`fragrant_flowers` · 子区域） → 属 运河区
- 加林纳酿酒厂（`gallina_winery` · 子区域） → 属 运河区
- 暴风城监狱（`stormwind_stockade` · dungeon） → 属 运河区
- 宝库（`stormwind_vault` · 地标） → 属 运河区
- 祈愿室（`petitioners_chamber` · 子区域） → 属 暴风要塞
- 要塞内庭院（`stormwind_keep_courtyard` · 地标） → 属 暴风要塞
- 要塞吊桥（`stormwind_keep_drawbridge` · 地标） → 属 暴风要塞
- 要塞花园（`stormwind_keep_garden` · 子区域） → 属 暴风要塞
- 王座厅（`stormwind_throne_room` · 子区域） → 属 暴风要塞
- 花园区月亮井（`stormwind_moonwell` · 地标） → 属 花园区
- 花园区入口旗幡（`stormwind_park_banner` · 地标） → 属 花园区
- 花园区中心广场（`stormwind_park_square` · 地标） → 属 花园区
- 空箭袋（`empty_quiver` · 子区域） → 属 贸易区
- 日用商品（`everyday_merchandise` · 子区域） → 属 贸易区
- 暴风城飞行点（`fp_stormwind` · transport · flightpath） → 属 贸易区
- 镶金玫瑰（`gilded_rose` · 聚居点 · inn） → 属 贸易区
- 狮鹫栖木（`gryphon_roost` · transport · flightpath） → 属 贸易区
- 狮心武器库（`lionheart_armory` · 子区域） → 属 贸易区
- 匹斯特的药剂店（`pestles_apothecary` · 子区域） → 属 贸易区
- 暴风城会计室（`stormwind_counting_house` · 子区域） → 属 贸易区
- 贸易区拍卖行（`stormwind_trade_auction_house` · 子区域） → 属 贸易区
- 暴风城接待中心（`stormwind_visitors_center` · 子区域） → 属 贸易区
- 贸易区喷泉（`trade_district_fountain` · 地标） → 属 贸易区
- 贸易区邮箱（`trade_district_mailbox` · 地标） → 属 贸易区
- 提亚斯奶酪店（`trias_cheese` · 子区域） → 属 贸易区
- 维勒武器店（`wellers_arsenal` · 子区域） → 属 贸易区
- 奥蕾莉亚·风行者像（`statue_alleria_windrunner` · 地标） → 属 英雄谷
- 达纳斯·托尔贝恩像（`statue_danath_trollbane` · 地标） → 属 英雄谷
- 大法师卡德加像（`statue_khadgar` · 地标） → 属 英雄谷
- 库德兰·蛮锤像（`statue_kurdran_wildhammer` · 地标） → 属 英雄谷
- 图拉扬像（`statue_turalyon` · 地标） → 属 英雄谷
- 暴风城大门（`stormwind_gate` · 地标） → 属 英雄谷
- 英雄谷石桥（`valley_of_heroes_bridge` · 地标） → 属 英雄谷
- 英雄谷护城水面（`valley_of_heroes_moat` · 地标） → 属 英雄谷
- 入城主路分岔口（`valley_of_heroes_road_fork` · 地标） → 属 英雄谷
- 俯瞰谷地的双塔（`valley_of_heroes_towers` · 地标） → 属 英雄谷
- 大教堂之钟（`cathedral_of_light_bell` · 地标） → 属 光明大教堂
- 大教堂地下墓穴（`cathedral_of_light_catacombs` · 子区域） → 属 光明大教堂
- 矿道地铁暴风城口·巨型齿轮门（`deeprun_tram_stormwind_gear_gate` · 地标） → 属 矿道地铁·暴风城站
- 已宰的羔羊地窖（`slaughtered_lamb_cellar` · 子区域） → 属 已宰的羔羊
- 圣殿外盘旋石阶（`wizards_sanctum_spiral_stair` · 地标） → 属 巫师圣殿
- 旧城区马厩（`old_town_stables` · 地标） → 属 指挥中心
- 露天训练场（`old_town_training_grounds` · 地标） → 属 指挥中心
- 巴吉尔·特雷德（`bazil_thredd` · 地标） → 属 暴风城监狱
- Bruegal Ironknuckle（`bruegal_ironknuckle` · 地标） → 属 暴风城监狱
- 迪克斯特·瓦德（`dextren_ward` · 地标） → 属 暴风城监狱
- 哈姆霍克（`hamhock` · 地标） → 属 暴风城监狱
- 卡姆·深怒（`kam_deepfury` · 地标） → 属 暴风城监狱
- 监狱门口集合石（`stockade_meeting_stone` · 地标） → 属 暴风城监狱
- 可怕的塔格尔（`targorr_the_dread` · 地标） → 属 暴风城监狱
- 宝库顶的大钟（`stormwind_vault_clock` · 地标） → 属 宝库
- 皇家画廊（`stormwind_royal_gallery` · 子区域） → 属 要塞花园
- 皇家图书馆（`stormwind_royal_library` · 子区域） → 属 要塞花园
- 作战室（`stormwind_war_room` · 子区域） → 属 王座厅
- 城门上悬挂的巨龙头颅（`dragon_head_on_stormwind_gate` · 地标） → 属 暴风城大门
- 城门外的双弩炮（`stormwind_gate_ballistae` · 地标） → 属 暴风城大门
