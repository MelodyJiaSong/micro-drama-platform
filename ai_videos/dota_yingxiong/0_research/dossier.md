# DotA 英雄 · Research 总览

> **版本锚点**：DotA Allstars **6.83d（2015-06-09）**，IceFrog 官方渠道的最后一版（d01 §1.3）。6.84–6.88 是 Dota 2 补丁号；魔兽地图版「6.85k / 6.88」是 DracoL1ch 等人的非官方改图，不作依据。
> **主据**：web.archive.org 存档的 PlayDotA 官方 6.83d 地图（英文版 + 官方中文版）解包文本：酒馆与商店出售列表、单位与物品名、模型路径、缩放、染色、语音集、特效文件、出兵脚本。旁证为 PlayDotA 英雄库存档、17173、百度百科、Liquipedia、warcraft.wiki.gg 等，见各分卷出处。
> **三级标签**：`✅` 有可指认出处 · `⚠️` 推测或单一弱来源 · `❌` 常见误传（只进各分卷「易错」节）。
> **Dota 2 不是 DotA 1**：名字、技能、模型、物品都可能不同；Dota 2 资料只作对账线索。
> 2026-10-18 八路并行调研合成；派单与各路回报存 `.audit/adhoc_agents/2026-10-18/dota-research/`。未调用收费服务。

## 0. 分卷与对账

| 分卷 | 内容 | 条目 | 名单对账 |
|---|---|---|---|
| [d01 版本与地图](parts/d01_版本与地图.md) | 版本史、112 人总名单、12 座酒馆、地图布局、建筑、商店、神符、Roshan、昼夜、兵线小兵、中立野怪、搭场景建议 | 里程碑 20 · 英雄 112 · 小兵 12 种 · 野怪 12 营 | 地图说明「112 unique heroes」= 12 酒馆合计 = PlayDotA 2015 英雄库 |
| [d02 近卫力量](parts/d02_近卫力量英雄.md) | 每人：模型、外观、4 技能与画面、台词、拍法提示 | 21 | 地图 + PlayDotA + 83dota |
| [d03 近卫敏捷](parts/d03_近卫敏捷英雄.md) | 同上 | 18 | 地图 + 17173 + 百度百科 |
| [d04 近卫智力](parts/d04_近卫智力英雄.md) | 同上 | 20 | 地图 + PlayDotA 2015/2016（17173 2013 年缺神谕者，当时未加入） |
| [d05 天灾力量](parts/d05_天灾力量英雄.md) | 同上 | 16 | 地图 + PlayDotA 2013 + EcuRed + 2008 博客 |
| [d06 天灾敏捷](parts/d06_天灾敏捷英雄.md) | 同上 | 17 | 地图 + PlayDotA 2015/2016 |
| [d07 天灾智力](parts/d07_天灾智力英雄.md) | 同上 | 20 | 地图 + PlayDotA 存档 |
| [d08 物品体系](parts/d08_物品体系.md) | 商店、合成、131 件物品、主动效果画面、掉落模型、上镜建议 | 131 | 对 PlayDotA 2014 物品库 129 条闭合 |

**合成时机检**：六格 21 + 18 + 20 + 16 + 17 + 20 = 112；d01 总名单逐个对到 d02–d07 的英雄小节，112/112，无缺无重，中文名一致（脚本核对，2026-10-18）。

## 1. 对 demo 最要紧的结论

1. **模型是魔兽 3 单位，不是 Dota 2 的英雄**。很多英雄和 Dota 2 外观完全不同，参考图必须来自 WC3 / DotA 1：例如宙斯＝金色山丘之王天神下凡形态，陈＝骑狼的兽人先知，剑圣＝红皮混沌剑圣，狼人＝品红色基尔加丹 / 紫恐狼，骷髅王＝放大染绿的骷髅战士（无王冠），沙王＝蝎形甲虫，天怒＝风蛇，大魔导师＝麦迪文，干扰者＝萨尔。模型路径、缩放、染色见下方索引与各分卷。
2. **英雄外观与技能特效的「长什么样」大多是 ⚠️**：名字、模型路径、特效文件名是地图里读出的 ✅；颜色、形状、动作是按 WC3 资源常识推断，没有截图核对。地图自带的导入模型（幻影长矛手、赏金猎人、谜团、远古冰魄、世界之树、神符等）和导入特效（月蚀、黑洞等）完全没见过成品。约一半脚本技能的特效对不上模型（脚本混淆）。**出片前需要一轮看图取证**：WC3 里录参考视频，或用模型查看器看 mdx。
3. **不少技能对小兵无效或只锁英雄**，demo 要在小兵之外安排一个**敌方英雄替身**（各分卷拍法提示已写替代拍法）：
   - 近卫：宙斯·雷神之怒，修补匠·热导飞弹，干扰者·一闪，拉比克·技能窃取，天怒·震荡射击 / 神秘之耀；仙女龙·梦境缠绕是否作用小兵存疑（d04）。
   - 天灾：末日·死亡等级？，猛犸·獠牙冲刺（只带英雄）（d05）；幽鬼·荒芜 / 鬼影重重，鱼人·突袭 / 能量转移，电魂·静电连接，血魔·嗜血渴望（d06）；黑曜·星体禁锢 / 神智之蚀，黑贤·复制之墙，暗影恶魔·崩裂禁锢，巫医·死亡守卫（只写攻击敌方英雄，待核）（d07）。
   - 另有一批技能需要**友军配合**或对自己放：查克拉魔法、嗜血术、上帝之手、虚妄诺言、薄葬，陈的神圣劝化可把敌方小兵收编（d04、d07）。
4. **小兵**：近卫＝树人、猛禽德鲁伊、投刃车；天灾＝食尸鬼、亡灵法师、绞肉车（d01 §4）。被打的小兵首选树人与食尸鬼：体型中等、轮廓好认、倒地明显。中立野怪 12 营可作补充（d01 §5）。
5. **场景**：亮相放本方基地（世界之树 / 冰封王座），技能主舞台建议中路河道交叉口；野区空地适合隐身位移类，Roshan 巢穴适合大英雄压迫镜头（d01 §6，创作建议）。
6. **台词**：每人用哪套 WC3 语音集是 ✅，英文原句多有出处；**中文配音原文全部未取证**，分卷里的中文是意译。谜团、黑曜毁灭者、祸乱之源、死灵飞龙、远古冰魄、寒冬飞龙、变体精灵没有人声台词。
7. **物品不改英雄外观**；地面掉落多为 WC3 棕色魔法书。14 件主动效果对上 WC3 原生特效（跳刀紫色闪烁、BKB＝天神下凡、羊刀＝变形术、分身斧＝剑圣镜像、吹风＝飓风等，d08 §2）。

## 2. 待用户决定（创作选择，Research 不替你定）

> 2026-10-18 用户已定（follow-up 001）：真人电影质感；片种为无连续剧情的短视频；先备齐资产再选英雄。Vision / 核心与首个英雄仍待定。

- **画面风格**：还原 WC3 模型的卡通低模感，还是像魔兽剧那样转成真人电影质感？这决定参考图从哪来、负面词怎么写。
- **全剧 Vision 与核心**、**片种**（`workflow.json` 未声明 `format`）。
- **先做哪个英雄**：建议从「4 个技能都能打小兵、特效已对上 WC3 原生资源」的英雄开始 POC（候选在各分卷拍法提示里）。

## 3. 未取证汇总（详见各分卷末尾）

- 外观与特效的截图核对（全卷）；导入模型 / 导入特效成品外观。
- 商店坐标与边路商店位置（缺 `war3mapUnits.doo`）；天灾「恶魔遗物」商店模型疑为 MageTower。
- 国内流行版本（6.27b / 6.59d / 6.64 等）当年流行度无出处。
- 中文配音原文；玩家俗称（大树、小牛、跳刀、羊刀等）未逐条取证。
- 个别数据矛盾：地卜师初始力量中英文地图不一（23 / 17）；飞行信使、纷争面纱提示价格与标价不一。

## 5. 台词（2026-10-18 补）

| 分卷 | 范围 |
|---|---|
| [d09 近卫力量](parts/d09_台词_近卫力量.md) · [d10 近卫敏捷](parts/d10_台词_近卫敏捷.md) · [d11 近卫智力](parts/d11_台词_近卫智力.md) | c1–c59 |
| [d12 天灾力量](parts/d12_台词_天灾力量.md) · [d13 天灾敏捷](parts/d13_台词_天灾敏捷.md) · [d14 天灾智力](parts/d14_台词_天灾智力.md) | c60–c112 |

每个英雄借用的 WC3 语音组全部台词：英文原句、意译中文（官方中文配音文本未找到）、wiki 音频文件名与链接、出处（warcraft.wiki.gg 与 PlayDotA 存档 Sounds 栏对照）。**未下载音频**（版权与商用由用户定）。更正：术士用兽人萨满语音组（d07 写的先知有误）；幽鬼的人声是倒放女声（d06「无台词」有误）。

## 4. 英雄索引（112 人，6.83d 酒馆出售顺序；模型取 UnitUI `file`，导入模型以分卷为准）

### 近卫 · 力量（21）· [d02_近卫力量英雄.md](parts/d02_近卫力量英雄.md)

| 中文（6.83d 中文版）| 英文称号 / 本名 | WC3 模型 | 缩放 |
|---|---|---|---|
| 树精卫士 / 鲁夫特伦 | Treant Protector / Rooftrellen | `buildings\nightelf\AncientProtector\AncientProtector` | 0.72 |
| 山岭巨人 / 小小 | Stone Giant / Tiny | `units\nightelf\MountainGiant\MountainGiant` | 0.5 |
| 全能骑士 / 普里斯特．雷霆之怒 | Omniknight / Purist Thunderwrath | `units\human\Arthas\Arthas` | 1.1 |
| 半人马酋长 / 布兰德瓦登 | Centaur Warchief / Bradwarden | `units\creeps\CentaurKhan\CentaurKhan` | 1.75 |
| 撼地神牛 / 瑞格．石蹄 | Earthshaker / Raigor Stonehoof | `units\orc\Tauren\Tauren` | 1.1 |
| 兽王 / 雷克萨 | Beastmaster / Rexxar | `Units\Creeps\Beastmaster\Beastmaster` | 1 |
| 舰队统帅 / 戴林．普罗德摩尔 | Admiral / Daelin Proudmoore | `units\other\Proudmoore\Proudmoore` | 1.1 |
| 流浪剑客 / 斯文 | Rogue Knight / Sven | `units\demon\FelgaurdBlue\FelgaurdBlue` | 1 |
| 熊猫酒仙 / 曼吉克斯 | Pandaren Brewmaster / Mangix | `Units\Creeps\PandarenBrewmaster\PandarenBrewmaster` | 1 |
| 牛头人酋长 / 凯恩．血蹄 | Tauren Chieftain / Cairne Bloodhoof | `units\orc\HeroTaurenChieftain\HeroTaurenChieftain` | 1.1 |
| 炼金术士 / 拉泽尔．黑酿 | Alchemist / Razzil Darkbrew | `Units\Creeps\HeroGoblinAlchemist\HeroGoblinAlchemist` | 1 |
| 守护精灵 / 伊俄 | Guardian Wisp / Io | `units\nightelf\Wisp\Wisp` | 1.3 |
| 龙骑士 / 达维安爵士 | Dragon Knight / Knight Davion | `units\human\TheCaptain\TheCaptain` | 1.35 |
| 神灵武士 / 哈斯卡 | Sacred Warrior / Huskar | `units\orc\HeadHunter\HeadHunter` | 1.15 |
| 发条地精 / 瑞托崔普 | Clockwerk Goblin / Rattletrap | `Units\Creeps\HeroTinkerRobot\HeroTinkerRobot` | 1.5 |
| 巨牙海民 / 尤弥尔 | Tuskarr / Ymir | `Units\Creeps\tuskarLord\tuskarLord` | 1 |
| 凤凰 / 伊卡洛斯 | Phoenix / Icarus | `units\human\phoenix\phoenix` | 1.05 |
| 刚背兽 / 瑞格沃 | Bristleback / Rigwarl | `units\creeps\RazorMane\RazorMane` | 1.65 |
| 军团指挥官 / 特斯丁 | Legion Commander / Tresdin | `units\creeps\LordGarithos\LordGarithos` | 1.3 |
| 地精撕裂者 / 瑞兹拉克 | Goblin Shredder / Rizzrak | `units\creeps\IronGolem\IronGolem` | 1 |
| 大地之灵 / 考林 | Earth Spirit / Kaolin | `Units\Creeps\EarthPandarenBrewmaster\EarthPandarenBrewmaster` | 1 |

### 近卫 · 敏捷（18）· [d03_近卫敏捷英雄.md](parts/d03_近卫敏捷英雄.md)

| 中文（6.83d 中文版）| 英文称号 / 本名 | WC3 模型 | 缩放 |
|---|---|---|---|
| 月之女祭司 / 米拉娜．夜影 | Priestess of the Moon / Mirana Nightshade | `units\nightelf\HeroMoonPriestess\HeroMoonPriestess` | 1 |
| 月之骑士 / 露娜．月痕 | Moon Rider / Luna Moonfang | `units\nightelf\Huntress\Huntress` | 1 |
| 敌法师 / 玛吉纳 | Anti-Mage / Magina | `units\nightelf\HeroDemonHunter\HeroDemonHunter` | 1 |
| 德鲁伊 / 悉拉贝尔 | Lone Druid / Syllabear | `units\nightelf\DruidoftheClaw\DruidoftheClaw` | 1 |
| 主宰 / 尤涅若 | Juggernaut / Yurnero | `units\demon\HeroChaosBladeMaster\HeroChaosBladeMaster` | 1 |
| 幻影长矛手 / 阿兹瑞斯 | Phantom Lancer / Azwraith | `units\orc\Hellscream\Hellscream` | 1 |
| 巨魔战将 / 杰拉考 | Troll Warlord / Jah'rakal | `units\creeps\ForestTrollTrapper\ForestTrollTrapper` | 1.25 |
| 隐形刺客 / 力丸 | Stealth Assassin / Rikimaru | `units\creeps\SatyrTrickster\SatyrTrickster` | 1 |
| 娜迦海妖 / 司里希丝 | Naga Siren / Slithice | `Units\Naga\NagaSiren\NagaSiren` | 1 |
| 变体精灵 / 变体精灵 | Morphling / Morphling | `Units\Creeps\SeaElemental\SeaElemental` | 1 |
| 矮人狙击手 / 卡德尔．鹰眼 | Dwarven Sniper / Kardel Sharpeye | `units\human\Rifleman\Rifleman` | 1.1 |
| 矮人直升机 / 奥雷尔．弗拉伊库 | Gyrocopter / Aurel Vlaicu | `units\human\Gyrocopter\Gyrocopter_V1` | 1.1 |
| 熊战士 / 乌尔萨 | Ursa Warrior / Ulfsaar | `units\creeps\FurbolgTracker\FurbolgTracker` | 1.2 |
| 圣堂刺客 / 拉娜娅 | Templar Assassin / Lanaya | `units\creeps\assassin\assassin` | 1.2 |
| 卓尔游侠 / 崔希丝 | Drow Ranger / Traxex | `Units\Creeps\BansheeRanger\BansheeRanger` | 1 |
| 赏金猎人 / 刚铎 | Bounty Hunter / Gondar | `units\other\DranaiAkama\DranaiAkama` | 1.2 |
| 复仇之魂 / 仙德尔莎．丝木 | Vengeful Spirit / Shendelzare Silkwood | `units\nightelf\Vengeance\Vengeance` | 1.35 |
| 灰烬之灵 / 新 | Ember Spirit / Xin | `Units\Creeps\FirePandarenBrewmaster\FirePandarenBrewmaster` | 1 |

### 近卫 · 智力（20）· [d04_近卫智力英雄.md](parts/d04_近卫智力英雄.md)

| 中文（6.83d 中文版）| 英文称号 / 本名 | WC3 模型 | 缩放 |
|---|---|---|---|
| 奥林匹斯之王 / 宙斯 | Lord of Olympus / Zeus | `units\human\HeroMountainKing\HeroMountainKing` | 1.3 |
| 水晶室女 / 莉莱．克丽丝芙 | Crystal Maiden / Rylai Crestfall | `units\human\Jaina\Jaina` | 1 |
| 秀逗魔导士 / 莉娜．茵巴斯 | Slayer / Lina Inverse | `units\human\Sorceress\Sorceress` | 1.2 |
| 光之守卫 / 伊扎洛 | Keeper of the Light / Ezalor | `units\human\HeroArchMage\HeroArchMage` | 1.2 |
| 仙女龙 / 帕克 | Faerie Dragon / Puck | `units\nightelf\FaerieDragon\FaerieDragon` | 1.1 |
| 风行者 / 奥蕾莉亚 | Windrunner / Alleria | `units\creeps\SylvanusWindrunner\SylvanusWindrunner` | 1.1 |
| 圣骑士 / 陈 | Holy Knight / Chen | `units\orc\HeroFarSeer\HeroFarSeer` | 1 |
| 魅惑魔女 / 爱由莎 | Enchantress / Aiushtha | `units\nightelf\Dryad\Dryad` | 1 |
| 先知 / 弗里奥 | Prophet / Furion | `units\nightelf\MalFurion\MalFurionNoStag` | 1.2 |
| 风暴之灵 / 雷神．风暴烈酒 | Storm Spirit / Raijin Thunderkeg | `Units\Creeps\StormPandarenBrewmaster\StormPandarenBrewmaster` | 1 |
| 沉默术士 / 诺崇 | Silencer / Nortrom | `units\human\BloodElfSpellThief\BloodElfSpellThief` | 1 |
| 干扰者 / 萨尔 | Disruptor / Thrall | `units\orc\Thrall\Thrall` | 1.1 |
| 地精修补匠 / 鲍什 | Tinker / Boush | `Units\Creeps\HeroTinker\HeroTinker` | 1 |
| 地精工程师 / 斯奎，斯布林和斯布伦 | Goblin Techies / Squee Spleen and Spoon | `units\creeps\GoblinSapper\GoblinSapper` | 1 |
| 食人魔魔法师 / 阿格隆．碎石者 | Ogre Magi / Aggron Stonebreaker | `units\creeps\OgreMagi\OgreMagi` | 1.4 |
| 双头龙 / 杰奇洛 | Twin Head Dragon / Jakiro | `units\nightelf\Chimaera\Chimaera` | 1 |
| 暗影萨满 / 罗斯塔 | Shadow Shaman / Rhasta | `units\orc\HeroShadowHunter\HeroShadowHunter` | 1 |
| 大魔导师 / 卢比克 | Grand Magus / Rubick | `units\creeps\Medivh\Medivh` | 1.15 |
| 天怒法师 / 扎贡纳斯 | Skywrath Mage / Dragonus | `units\creeps\WindSerpent\WindSerpent` | 1.1 |
| 神谕者 / 奈里夫 | Oracle / Nerif | `Units\Human\Priest\Priest_V1` | 1.25 |

### 天灾 · 力量（16）· [d05_天灾力量英雄.md](parts/d05_天灾力量英雄.md)

| 中文（6.83d 中文版）| 英文称号 / 本名 | WC3 模型 | 缩放 |
|---|---|---|---|
| 混沌骑士 / 涅沙 | Chaos Knight / Nessaj | `units\demon\ChaosWarlord\ChaosWarlord` | 1.05 |
| 狼人 / 贝恩霍勒 | Lycanthrope / Banehallow | `units\demon\Kiljaeden\Kiljaeden` | 1.2 |
| 骷髅王 / 李奥瑞克王 | Skeleton King / King Leoric | `units\undead\Skeleton\Skeleton` | 1.8 |
| 地狱领主 / 亚巴顿 | Lord of Avernus / Abaddon | `units\undead\HeroDeathKnight\HeroDeathKnight` | 1 |
| 鱼人守卫 / 斯拉达 | Slithereen Guard / Slardar | `units\naga\NagaRoyalGuard\NagaRoyalGuard` | 1 |
| 斧王 / 蒙哥．卡恩 | Axe / Mogul Kahn | `units\demon\ChaosHellscream\ChaosHellscream` | 1 |
| 深渊领主 / 阿兹加洛 | Pit Lord / Azgalor | `units\demon\HeroPitLord\HeroPitLord` | 0.95 |
| 不朽尸王 / 挽歌 | Undying / Dirge | `units\creeps\Zombie\Zombie` | 2 |
| 屠夫 / 胖子 | Butcher / Pudge | `units\undead\Abomination\Abomination` | 1 |
| 暗夜魔王 / 巴拉那 | Night Stalker / Balanar | `units\undead\Tichondrius\Tichondrius` | 1 |
| 噬魂鬼 / 奈克斯 | Lifestealer / N'aix | `units\undead\Ghoul\Ghoul` | 1.5 |
| 末日使者 / 路西法 | Doom Bringer / Lucifer | `units\demon\DoomGuard\DoomGuard` | 1.1 |
| 半人猛犸 / 马格纳斯 | Magnataur / Magnus | `Units\Creeps\MagnataurBlue\MagnataurBlue` | 1 |
| 裂魂人 / 巴拉森 | Spiritbreaker / Barathrum | `units\orc\spiritwalker\spiritwalker` | 1.2 |
| 潮汐猎人 / 利维坦 | Tidehunter / Leviathan | `Units\Creeps\SeaGiantGreen\SeaGiantGreen` | 1 |
| 沙王 / 克里瑟历斯 | Sand King / Crixalis | `Units\Creeps\ArchnathidGreen\ArchnathidGreen` | 1 |

### 天灾 · 敏捷（17）· [d06_天灾敏捷英雄.md](parts/d06_天灾敏捷英雄.md)

| 中文（6.83d 中文版）| 英文称号 / 本名 | WC3 模型 | 缩放 |
|---|---|---|---|
| 育母蜘蛛 / 布蕾克．艾拉齐娜 | Broodmother / Black Arachnia | `units\creeps\SpiderBlack\SpiderBlack` | 1.36 |
| 嗜血狂魔 / 史德利古尔 | Bloodseeker / Strygwyr | `units\orc\Shaman\Shaman` | 1.25 |
| 幽鬼 / 墨丘利 | Spectre / Mercurial | `units\nightelf\SpiritOfVengeance\SpiritOfVengeance` | 0.8 |
| 冥界亚龙 / 蝮蛇 | Netherdrake / Viper | `units\creeps\NetherDragon\NetherDragon` | 1.2 |
| 幻影刺客 / 茉崔蒂 | Phantom Assassin / Mortred | `units\nightelf\herowarden\herowarden` | 1 |
| 地穴刺客 / 阿努巴拉克 | Nerubian Assassin / Anub'arak | `units\undead\HeroCryptLord\HeroCryptLord` | 0.8 |
| 骷髅射手 / 克林克兹 | Bone Fletcher / Clinkz | `Units\Creeps\BurningArcher\BurningArcher` | 1 |
| 地穴编织者 / 阿努伯瑟伦 | Nerubian Weaver / Anub'seran | `units\creeps\NerubianQueen\NerubianQueen` | 1 |
| 剧毒术士 / 里瑟尔．死亡使者 | Venomancer / Lesale Deathbringer | `Units\Critters\Hydralisk\Hydralisk` | 1 |
| 灵魂守卫 / 恐怖利刃 | Soul Keeper / Terrorblade | `units\nightelf\EvilIllidan\IllidanEvil` | 1 |
| 影魔 / 奈文魔尔 | Shadow Fiend / Nevermore | `Units\Creeps\HeroFlameLord\HeroFlameLord` | 1.15 |
| 地卜师 / 米波 | Geomancer / Meepo | `units\creeps\KoboldGeomancer\KoboldGeomancer` | 1.4 |
| 鱼人夜行者 / 斯拉克 | Murloc Nightcrawler / Slark | `units\creeps\MurlocNightcrawler\MurlocNightcrawler` | 1.25 |
| 蛇发女妖 / 美杜莎 | Gorgon / Medusa | `units\naga\LadyVashj\LadyVashj` | 1 |
| 虚空假面 / 暗惧者 | Faceless Void / Darkterror | `Units\Creeps\FacelessOne\FacelessOne` | 1.3 |
| 闪电幽魂 / 剃刀 | Lightning Revenant / Razor | `units\creeps\Revenant\Revenant` | 1 |
| 弧光守望者 / 泽特 | Arc Warden / Zet | `units\creeps\GnollWarden\GnollWarden` | 1.1 |

### 天灾 · 智力（20）· [d07_天灾智力英雄.md](parts/d07_天灾智力英雄.md)

| 中文（6.83d 中文版）| 英文称号 / 本名 | WC3 模型 | 缩放 |
|---|---|---|---|
| 谜团 / 达克罗 | Enigma / Darchrow | `VoidWalker` | 1.5 |
| 巫妖 / 克尔苏加德 | Lich / Kel'Thuzad | `units\undead\HeroLich\HeroLich_V1` | 1.3 |
| 死亡先知 / 克萝贝露丝 | Death Prophet / Krobelus | `units\undead\Banshee\Banshee` | 1.35 |
| 恶魔巫师 / 莱恩 | Demon Witch / Lion | `units\demon\ChaosWarlock\ChaosWarlock` | 1.3 |
| 痛苦女王 / 阿卡莎 | Queen of Pain / Akasha | `units\demon\DemonessBlue\DemonessBlue` | 1.3 |
| 湮灭法师 / 帕格纳 | Oblivion / Pugna | `units\undead\SkeletonMage\SkeletonMage` | 1 |
| 死灵法师 / 罗坦德吉利 | Necrolyte / Rotund'jere | `units\undead\KelThuzadGhost\KelThuzadGhost` | 1.3 |
| 黑暗贤者 / 依什卡菲尔 | Dark Seer / Ish'kafel | `units\other\DranaiMage\DranaiMage` | 1.15 |
| 黑曜毁灭者 / 先兆者 | Obsidian Destroyer / Harbinger | `units\undead\ObsidianStatue\ObsidianStatue` | 0.85 |
| 祸乱之源 / 阿特洛波斯 | Bane Elemental / Atropos | `units\creeps\VoidWalker\VoidWalker` | 1.5 |
| 术士 / 戴蒙．莱尼克 | Warlock / Demnok Lannik | `units\orc\OrcWarlockGuldan\OrcWarlockGuldan` | 1.5 |
| 暗影恶魔 / 艾瑞达 | Shadow Demon / Eredar | `units\demon\Warlock\Warlock` | 1.25 |
| 远古冰魄 / 卡尔德 | Ancient Apparition / Kaldr | `war3mapImported\IcyGhost` | 1.2 |
| 受折磨的灵魂 / 恶毒的拉席克 | Tormented Soul / Leshrac the Malicious | `units\nightelf\HeroKeeperoftheGroveGhost\HeroKeeperoftheGroveGhost` | 1 |
| 死灵飞龙 / 维萨吉 | Necro'lic / Visage | `units\orc\SpiritWyvern\SpiritWyvern` | 1 |
| 巫医 / 沃金 | Witch Doctor / Vol'Jin | `units\orc\WitchDoctor\WitchDoctor` | 1.25 |
| 暗影牧师 / 戴泽 | Shadow Priest / Dazzle | `units\creeps\DarkTrollShadowPriest\DarkTrollShadowPriest` | 1.2 |
| 祈求者 / 凯尔 | Invoker / Kael | `units\human\HeroBloodElf\HeroBloodElf` | 1.25 |
| 蝙蝠骑士 / 金扎卡 | Batrider / Jin'zakk | `units\orc\BatTroll\BatTroll` | 1.2 |
| 寒冬飞龙 / 傲洛斯 | Winter Wyvern / Auroth | `units\undead\FrostWyrm\FrostWyrm` | 0.9 |
