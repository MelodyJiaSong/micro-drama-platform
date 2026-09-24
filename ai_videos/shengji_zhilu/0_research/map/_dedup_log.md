# 接缝收口记录（一次性）

13 路分头测绘必然在边界处重复描述同一个节点。本表记录每个重复 id 的归属裁定。
归属规则（按序）：① 副本/团本/战场归 `g11_instances` ② 交通归 `g12_transport` ③ 世界/大陆/分区归 `g01_world_skeleton` ④ 北郡与闪金镇的建筑级节点归 `g13` ⑤ 其余记录更丰富者胜。

| id | type | 归属 | 规则 | 原出现于 |
|---|---|---|---|---|
| `alterac_valley` | battleground | **g11_instances** | type=battleground 归专业路 | g06_lordaeron_north, g11_instances |
| `arathi_basin` | battleground | **g11_instances** | type=battleground 归专业路 | g07_lordaeron_east, g11_instances |
| `blackfathom_deeps` | dungeon | **g11_instances** | type=dungeon 归专业路 | g08_kalimdor_north, g11_instances |
| `blackrock_depths` | dungeon | **g11_instances** | type=dungeon 归专业路 | g04_ek_south, g11_instances |
| `blackwing_lair` | raid | **g11_instances** | type=raid 归专业路 | g04_ek_south, g11_instances |
| `deeprun_tram` | transport | **g12_transport** | type=transport 归专业路 | g03_stormwind_city, g12_transport |
| `deeprun_tram_stormwind_station` | transport | **g12_transport** | type=transport 归专业路 | g03_stormwind_city, g12_transport |
| `earth_song_falls` | subzone | **g09_kalimdor_central** | 记录更丰富者胜 | g09_kalimdor_central, g11_instances |
| `foulspore_cavern` | subzone | **g09_kalimdor_central** | 记录更丰富者胜 | g09_kalimdor_central, g11_instances |
| `fp_aerie_peak` | transport | **g12_transport** | type=transport 归专业路 | g07_lordaeron_east, g12_transport |
| `fp_chillwind_camp` | transport | **g12_transport** | type=transport 归专业路 | g07_lordaeron_east, g12_transport |
| `fp_hammerfall` | transport | **g12_transport** | type=transport 归专业路 | g07_lordaeron_east, g12_transport |
| `fp_refuge_pointe` | transport | **g12_transport** | type=transport 归专业路 | g07_lordaeron_east, g12_transport |
| `fp_revantusk_village` | transport | **g12_transport** | type=transport 归专业路 | g07_lordaeron_east, g12_transport |
| `gnomeregan` | dungeon | **g11_instances** | type=dungeon 归专业路 | g05_khaz_modan, g11_instances |
| `khaz_modan` | region | **g01_world_skeleton** | type=region 归专业路 | g01_world_skeleton, g05_khaz_modan |
| `maraudon` | dungeon | **g11_instances** | type=dungeon 归专业路 | g09_kalimdor_central, g11_instances |
| `molten_core` | raid | **g11_instances** | type=raid 归专业路 | g04_ek_south, g11_instances |
| `naxxramas` | raid | **g11_instances** | type=raid 归专业路 | g07_lordaeron_east, g11_instances |
| `northern_kalimdor` | region | **g01_world_skeleton** | type=region 归专业路 | g01_world_skeleton, g08_kalimdor_north |
| `ragefire_chasm` | dungeon | **g11_instances** | type=dungeon 归专业路 | g09_kalimdor_central, g11_instances |
| `razorfen_downs` | dungeon | **g11_instances** | type=dungeon 归专业路 | g09_kalimdor_central, g11_instances |
| `razorfen_kraul` | dungeon | **g11_instances** | type=dungeon 归专业路 | g09_kalimdor_central, g11_instances |
| `scarlet_monastery` | dungeon | **g11_instances** | type=dungeon 归专业路 | g06_lordaeron_north, g11_instances |
| `scholomance` | dungeon | **g11_instances** | type=dungeon 归专业路 | g07_lordaeron_east, g11_instances |
| `shadowfang_keep` | dungeon | **g11_instances** | type=dungeon 归专业路 | g06_lordaeron_north, g11_instances |
| `sm_armory` | dungeon | **g11_instances** | type=dungeon 归专业路 | g06_lordaeron_north, g11_instances |
| `sm_cathedral` | dungeon | **g11_instances** | type=dungeon 归专业路 | g06_lordaeron_north, g11_instances |
| `sm_graveyard` | dungeon | **g11_instances** | type=dungeon 归专业路 | g06_lordaeron_north, g11_instances |
| `sm_library` | dungeon | **g11_instances** | type=dungeon 归专业路 | g06_lordaeron_north, g11_instances |
| `south_seas` | region | **g01_world_skeleton** | type=region 归专业路 | g01_world_skeleton, g04_ek_south |
| `stonewrought_pass` | transport | **g04_ek_south** | 记录更丰富者胜 | g04_ek_south, g05_khaz_modan |
| `stormwind_stockade` | dungeon | **g11_instances** | type=dungeon 归专业路 | g03_stormwind_city, g11_instances |
| `stratholme_instance` | dungeon | **g11_instances** | type=dungeon 归专业路 | g07_lordaeron_east, g11_instances |
| `temple_of_atal_hakkar` | dungeon | **g11_instances** | type=dungeon 归专业路 | g04_ek_south, g11_instances |
| `thandol_span` | poi | **g05_khaz_modan** | 记录更丰富者胜 | g05_khaz_modan, g07_lordaeron_east |
| `the_bulwark` | settlement | **g06_lordaeron_north** | 记录更丰富者胜 | g06_lordaeron_north, g07_lordaeron_east |
| `the_great_sea` | region | **g01_world_skeleton** | type=region 归专业路 | g01_world_skeleton, g08_kalimdor_north |
| `the_green_belt` | subzone | **g05_khaz_modan** | 记录更丰富者胜 | g05_khaz_modan, g07_lordaeron_east |
| `thoradins_wall` | poi | **g07_lordaeron_east** | 记录更丰富者胜 | g06_lordaeron_north, g07_lordaeron_east |
| `uldaman` | dungeon | **g11_instances** | type=dungeon 归专业路 | g05_khaz_modan, g11_instances |
| `wailing_caverns` | dungeon | **g11_instances** | type=dungeon 归专业路 | g09_kalimdor_central, g11_instances |
| `warsong_gulch` | battleground | **g11_instances** | type=battleground 归专业路 | g08_kalimdor_north, g11_instances |
| `wicked_grotto` | subzone | **g09_kalimdor_central** | 记录更丰富者胜 | g09_kalimdor_central, g11_instances |
| `zul_gurub` | raid | **g11_instances** | type=raid 归专业路 | g04_ek_south, g11_instances |


## 第二轮（修正引号匹配后）

| id | type | 归属 | 规则 | 原出现于 |
|---|---|---|---|---|
| `crystal_lake` | subzone | **g13_northshire_goldshire_detail** | 建筑级细化路拥有 | g02_stormwind_kingdom_core, g13_northshire_goldshire_detail |
| `crystal_lake_islet` | poi | **g13_northshire_goldshire_detail** | 建筑级细化路拥有 | g02_stormwind_kingdom_core, g13_northshire_goldshire_detail |
| `echo_ridge_mine` | subzone | **g13_northshire_goldshire_detail** | 建筑级细化路拥有 | g02_stormwind_kingdom_core, g13_northshire_goldshire_detail |
| `goldshire` | settlement | **g13_northshire_goldshire_detail** | 建筑级细化路拥有 | g02_stormwind_kingdom_core, g13_northshire_goldshire_detail |
| `lions_pride_inn` | subzone | **g13_northshire_goldshire_detail** | 建筑级细化路拥有 | g02_stormwind_kingdom_core, g13_northshire_goldshire_detail |
| `northshire_abbey` | subzone | **g13_northshire_goldshire_detail** | 建筑级细化路拥有 | g02_stormwind_kingdom_core, g13_northshire_goldshire_detail |
| `northshire_river` | poi | **g13_northshire_goldshire_detail** | 建筑级细化路拥有 | g02_stormwind_kingdom_core, g13_northshire_goldshire_detail |
| `northshire_valley` | subzone | **g13_northshire_goldshire_detail** | 建筑级细化路拥有 | g02_stormwind_kingdom_core, g13_northshire_goldshire_detail |
| `northshire_vineyards` | subzone | **g13_northshire_goldshire_detail** | 建筑级细化路拥有 | g02_stormwind_kingdom_core, g13_northshire_goldshire_detail |
| `stormwind_gate` | subzone | **g03_stormwind_city** | 记录更丰富者胜 | g02_stormwind_kingdom_core, g03_stormwind_city |
| `the_deadmines` | dungeon | **g11_instances** | type=dungeon 归专业路 | g02_stormwind_kingdom_core, g11_instances |
