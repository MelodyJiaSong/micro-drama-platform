# 黑石山（Blackrock Mountain）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg76_黑石山全境/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/eastern_kingdoms/blackrock_mountain/`（东部王国 → 黑石山），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 地区 · 49-60 级 · contested |
| 相邻 | 燃烧平原 · 灼热峡谷 |
| 世界地图尺寸 | 914.4 × 609.6 m（推定：WorldMapArea 尺寸未取到一手出处，1000 × 667 码为估计值（1.12 无独立区图：黑石山 (areaID 25, map 0) 在 WorldMapArea.dbc 里没有条目，进山后世界地图回退到东部王国大陆图；1.15.7 UiMapAssignment 也没有条目（微地牢图是大灾变才加的）。此处给的是山体内部熔岩腔与两侧入口（灼热峡谷侧 X≈-7300、燃烧平原侧 X≈-7530；BRD 门 (-7179,-922)、BRS 门 (-7527,-1226)）外接的 3:2 估计框，约 1000×667 码。）） |
| 世界树画面 | 一座被掏空的巨型火山内腔，中央是深不见底的熔岩井，橙红光自下而上打亮环形石道与悬空铁链，热浪让所有轮廓微微发抖 |
| 备注 | 【挂靠裁定】黑石山在旧世是独立地区（zone id 25），地理上同时接燃烧平原与灼热峡谷。本树把它作为 zone 挂在 khaz_modan 下（依据 warcraft.wiki.gg 的 Khaz Modan 地区条目明确把 Blackrock Mountain 列入），并在燃烧平原、灼热峡谷两侧各挂一个入口 poi 指向它——「一份几何，两道门」，避免同一座山被登记两次 |
| 出处 | https://warcraft.wiki.gg/wiki/Blackrock_Mountain |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-Blackrock.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/eastern_kingdoms/khaz_modan/blackrock_mountain/WorldMap-Blackrock.jpg`


## 区级场地平面图

`bg76_黑石山全境/planning/bg76_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（4 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg76** | [黑石山全境](bg76_黑石山全境/bg76_黑石山全境.md) | 自造 | — |  |
| **bg77** | [碾石场](bg77_碾石场/bg77_碾石场.md) | 子区域 | — | 一条凿穿岩体的矿道，两壁留着粗糙的凿痕，地上铺着碎石与废弃轨道，尽头是黑石深渊的传送门 |
| **bg78** | [石匠区](bg78_石匠区/bg78_石匠区.md) | 子区域 | — | 山腹里的石工作业区，半成形的石砖与立柱靠墙排开，地面积着厚厚的石粉 |
| **bg79** | [熔岩之桥](bg79_熔岩之桥/bg79_熔岩之桥.md) | 子区域 | — | 山腹正中的巨型环形大厅，一圈宽阔的石道贴着岩壁盘绕，中央悬空一座石塔，下方是翻滚的熔岩海 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 黑石深渊（`blackrock_depths` · dungeon）
- 黑石塔（`blackrock_spire` · dungeon）
- 熔火之心（`molten_core` · raid）
- 弗莱拉斯大使（`ambassador_flamelash` · 地标） → 属 黑石深渊
- 贝尔加（`baelgar` · 地标） → 属 黑石深渊
- 魔法之厅（`brd_chamber_of_enchantment` · 子区域） → 属 黑石深渊
- 黑铁大道（`brd_dark_iron_highway` · 子区域） → 属 黑石深渊
- 监狱区（`brd_detention_block` · 子区域） → 属 黑石深渊
- 东区兵营（`brd_east_garrison` · 子区域） → 属 黑石深渊
- 工艺之厅（`brd_hall_of_crafting` · 子区域） → 属 黑石深渊
- 秩序大厅（`brd_halls_of_the_law` · 子区域） → 属 黑石深渊
- 浇铸间（`brd_mold_foundry` · 子区域） → 属 黑石深渊
- 命运大厅（`brd_ring_of_the_law` · 子区域） → 属 黑石深渊
- 索瑞森神殿（`brd_shrine_of_thaurissan` · 子区域） → 属 黑石深渊
- 召唤者之墓（`brd_summoners_tomb` · 子区域） → 属 黑石深渊
- 黑色宝库（`brd_the_black_vault` · 子区域） → 属 黑石深渊
- 住宅区（`brd_the_domicile` · 子区域） → 属 黑石深渊
- 黑铁酒吧（`brd_the_grim_guzzler` · 子区域） → 属 黑石深渊
- 帝王之座（`brd_the_imperial_seat` · 子区域） → 属 黑石深渊
- 钢铁大厅（`brd_the_iron_hall` · 子区域） → 属 黑石深渊
- 讲学厅（`brd_the_lyceum` · 子区域） → 属 黑石深渊
- 制造厂（`brd_the_manufactory` · 子区域） → 属 黑石深渊
- 熔火之桥（`brd_the_molten_bridge` · 子区域） → 属 黑石深渊
- 银行（`brd_the_vault` · 地标） → 属 黑石深渊
- 西区兵营（`brd_west_garrison` · 子区域） → 属 黑石深渊
- 达格兰·索瑞森大帝（`emperor_dagran_thaurissan` · 地标） → 属 黑石深渊
- 弗诺斯·达克维尔（`fineous_darkvire` · 地标） → 属 黑石深渊
- 安格弗将军（`general_angerforge` · 地标） → 属 黑石深渊
- 傀儡统帅阿格曼奇（`golem_lord_argelmach` · 地标） → 属 黑石深渊
- 审讯官格斯塔恩（`high_interrogator_gerstahn` · 地标） → 属 黑石深渊
- 驯犬者格雷布玛尔（`houndmaster_grebmar` · 地标） → 属 黑石深渊
- 霍尔雷·黑须（`hurley_blackbreath` · 地标） → 属 黑石深渊
- 伊森迪奥斯（`lord_incendius` · 地标） → 属 黑石深渊
- 洛考尔（`lord_roccor` · 地标） → 属 黑石深渊
- 玛格姆斯（`magmus` · 地标） → 属 黑石深渊
- 熔火之心入口（`molten_core_entrance` · 地标） → 属 黑石深渊
- 法拉克斯（`phalanx` · 地标） → 属 黑石深渊
- 普拉格（`plugger_spazzring` · 地标） → 属 黑石深渊
- 铁炉堡公主茉艾拉·铜须（`princess_moira_bronzebeard` · 地标） → 属 黑石深渊
- 控火师罗格雷恩（`pyromancer_loregrain` · 地标） → 属 黑石深渊
- 雷布里·斯库比格特（`ribbly_screwspigot` · 地标） → 属 黑石深渊
- 秩序竞技场（`ring_of_law` · 地标） → 属 黑石深渊
- 黑铁七贤（`the_seven` · 地标） → 属 黑石深渊
- 典狱官斯迪尔基斯（`warder_stilgiss` · 地标） → 属 黑石深渊
- 黑石竞技场（`blackrock_stadium` · 子区域） → 属 黑石塔
- 黑翼之巢（`blackwing_lair` · raid） → 属 黑石塔
- 禁锢之厅（`brs_hall_of_binding` · 子区域） → 属 黑石塔
- 尖塔王座（`brs_spire_throne` · 子区域） → 属 黑石塔
- 熔炉（`brs_the_furnace` · 子区域） → 属 黑石塔
- 龙塔大厅（`dragonspire_hall` · 子区域） → 属 黑石塔
- 黑手大厅（`hall_of_blackhand` · 子区域） → 属 黑石塔
- 霍德玛尔城（`hordemar_city` · 子区域） → 属 黑石塔
- 黑石塔下层（`lower_blackrock_spire` · dungeon） → 属 黑石塔
- 孵化间（`the_rookery` · 子区域） → 属 黑石塔
- 黑石塔上层（`upper_blackrock_spire` · dungeon） → 属 黑石塔
- 迦顿男爵（`baron_geddon` · 地标） → 属 熔火之心
- 加尔（`garr` · 地标） → 属 熔火之心
- 基赫纳斯（`gehennas` · 地标） → 属 熔火之心
- 焚化者古雷曼格（`golemagg_the_incinerator` · 地标） → 属 熔火之心
- 鲁西弗隆（`lucifron` · 地标） → 属 熔火之心
- 玛格曼达（`magmadar` · 地标） → 属 熔火之心
- 管理者埃克索图斯（`majordomo_executus` · 地标） → 属 熔火之心
- 玛格曼达洞穴（`mc_magmadar_cavern` · 子区域） → 属 熔火之心
- 拉格纳罗斯的巢穴（`mc_ragnaros_lair` · 子区域） → 属 熔火之心
- 拉格纳罗斯（`ragnaros` · 地标） → 属 熔火之心
- 沙斯拉尔（`shazzrah` · 地标） → 属 熔火之心
- 萨弗隆先驱者（`sulfuron_harbinger` · 地标） → 属 熔火之心
- 黑石塔入口（`blackrock_spire_entrance` · 地标） → 属 熔岩之桥
- 铸铁者之墓（`forgewrights_tomb` · 地标） → 属 熔岩之桥
- 熔岩上的铁链（`molten_span_chains` · 地标） → 属 熔岩之桥
- 勒什雷尔（`broodlord_lashlayer` · 地标） → 属 黑翼之巢
- Crimson Laboratories（`bwl_crimson_laboratories` · 子区域） → 属 黑翼之巢
- 龙喉兵营（`bwl_dragonmaw_garrison` · 子区域） → 属 黑翼之巢
- 征战大厅（`bwl_halls_of_strife` · 子区域） → 属 黑翼之巢
- 影翼巢穴（`bwl_shadow_wing_lair` · 子区域） → 属 黑翼之巢
- 克洛玛古斯（`chromaggus` · 地标） → 属 黑翼之巢
- 埃博诺克（`ebonroc` · 地标） → 属 黑翼之巢
- 费尔默（`firemaw` · 地标） → 属 黑翼之巢
- 弗莱格尔（`flamegor` · 地标） → 属 黑翼之巢
- 奈法利安（`nefarian` · 地标） → 属 黑翼之巢
- 奈法利安的巢穴（`nefarians_lair` · 子区域） → 属 黑翼之巢
- 狂野的拉佐格尔（`razorgore_the_untamed` · 地标） → 属 黑翼之巢
- 堕落的瓦拉斯塔兹（`vaelastrasz_the_corrupt` · 地标） → 属 黑翼之巢
- 战斗之厅（`brs_chamber_of_battle` · 子区域） → 属 霍德玛尔城
- 仓库（`brs_the_storehouse` · 子区域） → 属 霍德玛尔城
- 哈雷肯之巢（`halycons_lair` · 子区域） → 属 霍德玛尔城
- 摩多姆（`mok_doom` · 子区域） → 属 霍德玛尔城
- 蛛网隧道（`skitterweb_tunnels` · 子区域） → 属 霍德玛尔城
- 塔萨洛尔（`tazzalor` · 子区域） → 属 霍德玛尔城
- 奴役者基兹鲁尔（`gizrul_the_slavener` · 地标） → 属 黑石塔下层
- 哈雷肯（`halycon` · 地标） → 属 黑石塔下层
- 欧莫克大王（`highlord_omokk` · 地标） → 属 黑石塔下层
- 烟网蛛后（`mother_smolderweb` · 地标） → 属 黑石塔下层
- 维姆萨拉克（`overlord_wyrmthalak` · 地标） → 属 黑石塔下层
- 军需官兹格雷斯（`quartermaster_zigris` · 地标） → 属 黑石塔下层
- 暗影猎手沃什加斯（`shadow_hunter_voshgajin` · 地标） → 属 黑石塔下层
- 乌洛克（`urok_doomhowl` · 地标） → 属 黑石塔下层
- 指挥官沃恩（`war_master_voone` · 地标） → 属 黑石塔下层
- 达基萨斯将军（`general_drakkisath` · 地标） → 属 黑石塔上层
- Goraluk Anvilcrack（`goraluk_anvilcrack` · 地标） → 属 黑石塔上层
- Gyth（`gyth` · 地标） → 属 黑石塔上层
- Jed Runewatcher（`jed_runewatcher` · 地标） → 属 黑石塔上层
- 瓦塔拉克公爵（`lord_valthalak` · 地标） → 属 黑石塔上层
- 烈焰卫士艾博希尔（`pyroguard_emberseer` · 地标） → 属 黑石塔上层
- Solakar Flamewreath（`solakar_flamewreath` · 地标） → 属 黑石塔上层
- 比斯巨兽（`the_beast` · 地标） → 属 黑石塔上层
- 大酋长雷德·黑手（`warchief_rend_blackhand` · 地标） → 属 黑石塔上层
