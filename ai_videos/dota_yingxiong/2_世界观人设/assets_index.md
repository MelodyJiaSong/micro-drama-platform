# 资产编号总表（唯一出处）


> 编号只追加、不复用、不重排；目录改名只改名字不改号（共用 `resources/assets.md`）。2026-10-18 首次分配。
> 英雄 c 号按 `0_research/dossier.md` 索引顺序（6.83d 酒馆出售顺序）。召唤物 m 号每格预留 20 个号段，用到哪号写到哪号，未用的号不回收给别格。

## 死亡动作资产（2026-10-22，follow-up 059）

**060 分类修订**：先分英雄、兵线小兵及其他待核类别，再看身体结构。m4 食尸鬼按兵线小兵，不能因与 c70 同模型就共用英雄死亡方案；旧8秒通用侧倒已撤回默认方案，需先核实小兵自身死亡与地面遗体。其他非英雄角色不自动归入小兵。

每个人物新增独立死亡动作视频，先做食尸鬼 m4 的研究与筹划。[阶段清单](characters/death_assets.json)按现有183张主体卡登记，沿用本表编号；换形态、坐骑和合体单位是否需要独立条目尚待核对，不把183当最终视频数。m4 已下载参考并完成[筹划稿](characters/天灾_scourge/m4_Ghoul/death/m4_Ghoul_death.md)，065用Codex出首尾姿态候选，末姿仅为电影化构图，待用户看图，尚无死亡视频；其余角色仅登记需求。立绘仍待重出或外观未定的，先锁造型再做死亡图。清单的图片存在标记仅是文件检查，不表示外观已获选定或 QC 通过。

## 目录结构（2026-10-18 follow-up 025：先按阵营分，再放资产）

```
2_世界观人设/
├─ characters/{近卫_sentinel, 天灾_scourge, 中立_neutral}/<卡目录>/   形态 / 换装子目录跟本体走
├─ background/{近卫_sentinel, 天灾_scourge, 中立_neutral}/<bg 目录>/
└─ props/{近卫_sentinel, 天灾_scourge, 中立_neutral}/<道具目录>/
```

| 资产 | 近卫_sentinel | 天灾_scourge | 中立_neutral | 分类规则 |
|---|---|---|---|---|
| 人物（183） | 83 | 70 | 30 | 基地商人 m300–m309 归中立（两方同模型）；英雄按卡首行 `近卫 /` `天灾 /`；兵线 m1–m3 近卫、m4–m6 天灾；召唤物 / 变形产物跟召唤者英雄；首行「中立野怪」「中立 Boss」归中立 |
| 背景（39） | 15 | 16 | 8 | 泉水与商店、基地、一塔、野区空地留各自阵营；河道、神符点、巨兽巢穴与公共商店（bg11 秘密商店、bg12 边路地精商店）归中立 |
| 道具（231；另 p95 取消制作、不复用） | 47 | 32 | 152 | 公共道具归中立，固定武器跟持有者阵营；武器图及人物重出状态见本页 follow-up 075 清单 |

分组目录只是存放位置，不带键、不进编号；工具与管理 UI 都认一层分组（`projects/ai_video_management/libs/common/asset_group.py`）。各 `request_log.md` 留在 `characters/` `background/` `props/` 根，历史条目保留旧路径。

## 英雄（c1–c112）

### 近卫 · 力量（21）· 召唤物号段 m100–m119

| 键 | 目录 | 中文 | 英文称号 / 本名 |
|---|---|---|---|
| c1 | `characters/近卫_sentinel/c1_Treant_Protector/` | 树精卫士 / 鲁夫特伦 | Treant Protector / Rooftrellen |
| c2 | `characters/近卫_sentinel/c2_Stone_Giant/` | 山岭巨人 / 小小 | Stone Giant / Tiny |
| c3 | `characters/近卫_sentinel/c3_Omniknight/` | 全能骑士 / 普里斯特．雷霆之怒 | Omniknight / Purist Thunderwrath |
| c4 | `characters/近卫_sentinel/c4_Centaur_Warchief/` | 半人马酋长 / 布兰德瓦登 | Centaur Warchief / Bradwarden |
| c5 | `characters/近卫_sentinel/c5_Earthshaker/` | 撼地神牛 / 瑞格．石蹄 | Earthshaker / Raigor Stonehoof |
| c6 | `characters/近卫_sentinel/c6_Beastmaster/` | 兽王 / 雷克萨 | Beastmaster / Rexxar |
| c7 | `characters/近卫_sentinel/c7_Admiral/` | 舰队统帅 / 戴林．普罗德摩尔 | Admiral / Daelin Proudmoore |
| c8 | `characters/近卫_sentinel/c8_Rogue_Knight/` | 流浪剑客 / 斯文 | Rogue Knight / Sven |
| c9 | `characters/近卫_sentinel/c9_Pandaren_Brewmaster/` | 熊猫酒仙 / 曼吉克斯 | Pandaren Brewmaster / Mangix |
| c10 | `characters/近卫_sentinel/c10_Tauren_Chieftain/` | 牛头人酋长 / 凯恩．血蹄 | Tauren Chieftain / Cairne Bloodhoof |
| c11 | `characters/近卫_sentinel/c11_Alchemist/` | 炼金术士 / 拉泽尔．黑酿 | Alchemist / Razzil Darkbrew |
| c12 | `characters/近卫_sentinel/c12_Guardian_Wisp/` | 守护精灵 / 伊俄 | Guardian Wisp / Io |
| c13 | `characters/近卫_sentinel/c13_Dragon_Knight/` | 龙骑士 / 达维安爵士 | Dragon Knight / Knight Davion |
| c14 | `characters/近卫_sentinel/c14_Sacred_Warrior/` | 神灵武士 / 哈斯卡 | Sacred Warrior / Huskar |
| c15 | `characters/近卫_sentinel/c15_Clockwerk_Goblin/` | 发条地精 / 瑞托崔普 | Clockwerk Goblin / Rattletrap |
| c16 | `characters/近卫_sentinel/c16_Tuskarr/` | 巨牙海民 / 尤弥尔 | Tuskarr / Ymir |
| c17 | `characters/近卫_sentinel/c17_Phoenix/` | 凤凰 / 伊卡洛斯 | Phoenix / Icarus |
| c18 | `characters/近卫_sentinel/c18_Bristleback/` | 刚背兽 / 瑞格沃 | Bristleback / Rigwarl |
| c19 | `characters/近卫_sentinel/c19_Legion_Commander/` | 军团指挥官 / 特斯丁 | Legion Commander / Tresdin |
| c20 | `characters/近卫_sentinel/c20_Goblin_Shredder/` | 地精撕裂者 / 瑞兹拉克 | Goblin Shredder / Rizzrak |
| c21 | `characters/近卫_sentinel/c21_Earth_Spirit/` | 大地之灵 / 考林 | Earth Spirit / Kaolin |

### 近卫 · 敏捷（18）· 召唤物号段 m120–m139

| 键 | 目录 | 中文 | 英文称号 / 本名 |
|---|---|---|---|
| c22 | `characters/近卫_sentinel/c22_Priestess_of_the_Moon/` | 月之女祭司 / 米拉娜．夜影 | Priestess of the Moon / Mirana Nightshade |
| c23 | `characters/近卫_sentinel/c23_Moon_Rider/` | 月之骑士 / 露娜．月痕 | Moon Rider / Luna Moonfang |
| c24 | `characters/近卫_sentinel/c24_Anti_Mage/` | 敌法师 / 玛吉纳 | Anti-Mage / Magina |
| c25 | `characters/近卫_sentinel/c25_Lone_Druid/` | 德鲁伊 / 悉拉贝尔 | Lone Druid / Syllabear |
| c26 | `characters/近卫_sentinel/c26_Juggernaut/` | 主宰 / 尤涅若 | Juggernaut / Yurnero |
| c27 | `characters/近卫_sentinel/c27_Phantom_Lancer/` | 幻影长矛手 / 阿兹瑞斯 | Phantom Lancer / Azwraith |
| c28 | `characters/近卫_sentinel/c28_Troll_Warlord/` | 巨魔战将 / 杰拉考 | Troll Warlord / Jah'rakal |
| c29 | `characters/近卫_sentinel/c29_Stealth_Assassin/` | 隐形刺客 / 力丸 | Stealth Assassin / Rikimaru |
| c30 | `characters/近卫_sentinel/c30_Naga_Siren/` | 娜迦海妖 / 司里希丝 | Naga Siren / Slithice |
| c31 | `characters/近卫_sentinel/c31_Morphling/` | 变体精灵 / 变体精灵 | Morphling / Morphling |
| c32 | `characters/近卫_sentinel/c32_Dwarven_Sniper/` | 矮人狙击手 / 卡德尔．鹰眼 | Dwarven Sniper / Kardel Sharpeye |
| c33 | `characters/近卫_sentinel/c33_Gyrocopter/` | 矮人直升机 / 奥雷尔．弗拉伊库 | Gyrocopter / Aurel Vlaicu |
| c34 | `characters/近卫_sentinel/c34_Ursa_Warrior/` | 熊战士 / 乌尔萨 | Ursa Warrior / Ulfsaar |
| c35 | `characters/近卫_sentinel/c35_Templar_Assassin/` | 圣堂刺客 / 拉娜娅 | Templar Assassin / Lanaya |
| c36 | `characters/近卫_sentinel/c36_Drow_Ranger/` | 卓尔游侠 / 崔希丝 | Drow Ranger / Traxex |
| c37 | `characters/近卫_sentinel/c37_Bounty_Hunter/` | 赏金猎人 / 刚铎 | Bounty Hunter / Gondar |
| c38 | `characters/近卫_sentinel/c38_Vengeful_Spirit/` | 复仇之魂 / 仙德尔莎．丝木 | Vengeful Spirit / Shendelzare Silkwood |
| c39 | `characters/近卫_sentinel/c39_Ember_Spirit/` | 灰烬之灵 / 新 | Ember Spirit / Xin |

### 近卫 · 智力（20）· 召唤物号段 m140–m159

| 键 | 目录 | 中文 | 英文称号 / 本名 |
|---|---|---|---|
| c40 | `characters/近卫_sentinel/c40_Lord_of_Olympus/` | 奥林匹斯之王 / 宙斯 | Lord of Olympus / Zeus |
| c41 | `characters/近卫_sentinel/c41_Crystal_Maiden/` | 水晶室女 / 莉莱．克丽丝芙 | Crystal Maiden / Rylai Crestfall |
| c42 | `characters/近卫_sentinel/c42_Slayer/` | 秀逗魔导士 / 莉娜．茵巴斯 | Slayer / Lina Inverse |
| c43 | `characters/近卫_sentinel/c43_Keeper_of_the_Light/` | 光之守卫 / 伊扎洛 | Keeper of the Light / Ezalor |
| c44 | `characters/近卫_sentinel/c44_Faerie_Dragon/` | 仙女龙 / 帕克 | Faerie Dragon / Puck |
| c45 | `characters/近卫_sentinel/c45_Windrunner/` | 风行者 / 奥蕾莉亚 | Windrunner / Alleria |
| c46 | `characters/近卫_sentinel/c46_Holy_Knight/` | 圣骑士 / 陈 | Holy Knight / Chen |
| c47 | `characters/近卫_sentinel/c47_Enchantress/` | 魅惑魔女 / 爱由莎 | Enchantress / Aiushtha |
| c48 | `characters/近卫_sentinel/c48_Prophet/` | 先知 / 弗里奥 | Prophet / Furion |
| c49 | `characters/近卫_sentinel/c49_Storm_Spirit/` | 风暴之灵 / 雷神．风暴烈酒 | Storm Spirit / Raijin Thunderkeg |
| c50 | `characters/近卫_sentinel/c50_Silencer/` | 沉默术士 / 诺崇 | Silencer / Nortrom |
| c51 | `characters/近卫_sentinel/c51_Disruptor/` | 干扰者 / 萨尔 | Disruptor / Thrall |
| c52 | `characters/近卫_sentinel/c52_Tinker/` | 地精修补匠 / 鲍什 | Tinker / Boush |
| c53 | `characters/近卫_sentinel/c53_Goblin_Techies/` | 地精工程师 / 斯奎，斯布林和斯布伦 | Goblin Techies / Squee Spleen and Spoon |
| c54 | `characters/近卫_sentinel/c54_Ogre_Magi/` | 食人魔魔法师 / 阿格隆．碎石者 | Ogre Magi / Aggron Stonebreaker |
| c55 | `characters/近卫_sentinel/c55_Twin_Head_Dragon/` | 双头龙 / 杰奇洛 | Twin Head Dragon / Jakiro |
| c56 | `characters/近卫_sentinel/c56_Shadow_Shaman/` | 暗影萨满 / 罗斯塔 | Shadow Shaman / Rhasta |
| c57 | `characters/近卫_sentinel/c57_Grand_Magus/` | 大魔导师 / 卢比克 | Grand Magus / Rubick |
| c58 | `characters/近卫_sentinel/c58_Skywrath_Mage/` | 天怒法师 / 扎贡纳斯 | Skywrath Mage / Dragonus |
| c59 | `characters/近卫_sentinel/c59_Oracle/` | 神谕者 / 奈里夫 | Oracle / Nerif |

### 天灾 · 力量（16）· 召唤物号段 m160–m179

| 键 | 目录 | 中文 | 英文称号 / 本名 |
|---|---|---|---|
| c60 | `characters/天灾_scourge/c60_Chaos_Knight/` | 混沌骑士 / 涅沙 | Chaos Knight / Nessaj |
| c61 | `characters/天灾_scourge/c61_Lycanthrope/` | 狼人 / 贝恩霍勒 | Lycanthrope / Banehallow |
| c62 | `characters/天灾_scourge/c62_Skeleton_King/` | 骷髅王 / 李奥瑞克王 | Skeleton King / King Leoric |
| c63 | `characters/天灾_scourge/c63_Lord_of_Avernus/` | 地狱领主 / 亚巴顿 | Lord of Avernus / Abaddon |
| c64 | `characters/天灾_scourge/c64_Slithereen_Guard/` | 鱼人守卫 / 斯拉达 | Slithereen Guard / Slardar |
| c65 | `characters/天灾_scourge/c65_Axe/` | 斧王 / 蒙哥．卡恩 | Axe / Mogul Kahn |
| c66 | `characters/天灾_scourge/c66_Pit_Lord/` | 深渊领主 / 阿兹加洛 | Pit Lord / Azgalor |
| c67 | `characters/天灾_scourge/c67_Undying/` | 不朽尸王 / 挽歌 | Undying / Dirge |
| c68 | `characters/天灾_scourge/c68_Butcher/` | 屠夫 / 胖子 | Butcher / Pudge |
| c69 | `characters/天灾_scourge/c69_Night_Stalker/` | 暗夜魔王 / 巴拉那 | Night Stalker / Balanar |
| c70 | `characters/天灾_scourge/c70_Lifestealer/` | 噬魂鬼 / 奈克斯 | Lifestealer / N'aix |
| c71 | `characters/天灾_scourge/c71_Doom_Bringer/` | 末日使者 / 路西法 | Doom Bringer / Lucifer |
| c72 | `characters/天灾_scourge/c72_Magnataur/` | 半人猛犸 / 马格纳斯 | Magnataur / Magnus |
| c73 | `characters/天灾_scourge/c73_Spiritbreaker/` | 裂魂人 / 巴拉森 | Spiritbreaker / Barathrum |
| c74 | `characters/天灾_scourge/c74_Tidehunter/` | 潮汐猎人 / 利维坦 | Tidehunter / Leviathan |
| c75 | `characters/天灾_scourge/c75_Sand_King/` | 沙王 / 克里瑟历斯 | Sand King / Crixalis |

### 天灾 · 敏捷（17）· 召唤物号段 m180–m199

| 键 | 目录 | 中文 | 英文称号 / 本名 |
|---|---|---|---|
| c76 | `characters/天灾_scourge/c76_Broodmother/` | 育母蜘蛛 / 布蕾克．艾拉齐娜 | Broodmother / Black Arachnia |
| c77 | `characters/天灾_scourge/c77_Bloodseeker/` | 嗜血狂魔 / 史德利古尔 | Bloodseeker / Strygwyr |
| c78 | `characters/天灾_scourge/c78_Spectre/` | 幽鬼 / 墨丘利 | Spectre / Mercurial |
| c79 | `characters/天灾_scourge/c79_Netherdrake/` | 冥界亚龙 / 蝮蛇 | Netherdrake / Viper |
| c80 | `characters/天灾_scourge/c80_Phantom_Assassin/` | 幻影刺客 / 茉崔蒂 | Phantom Assassin / Mortred |
| c81 | `characters/天灾_scourge/c81_Nerubian_Assassin/` | 地穴刺客 / 阿努巴拉克 | Nerubian Assassin / Anub'arak |
| c82 | `characters/天灾_scourge/c82_Bone_Fletcher/` | 骷髅射手 / 克林克兹 | Bone Fletcher / Clinkz |
| c83 | `characters/天灾_scourge/c83_Nerubian_Weaver/` | 地穴编织者 / 阿努伯瑟伦 | Nerubian Weaver / Anub'seran |
| c84 | `characters/天灾_scourge/c84_Venomancer/` | 剧毒术士 / 里瑟尔．死亡使者 | Venomancer / Lesale Deathbringer |
| c85 | `characters/天灾_scourge/c85_Soul_Keeper/` | 灵魂守卫 / 恐怖利刃 | Soul Keeper / Terrorblade |
| c86 | `characters/天灾_scourge/c86_Shadow_Fiend/` | 影魔 / 奈文魔尔 | Shadow Fiend / Nevermore |
| c87 | `characters/天灾_scourge/c87_Geomancer/` | 地卜师 / 米波 | Geomancer / Meepo |
| c88 | `characters/天灾_scourge/c88_Murloc_Nightcrawler/` | 鱼人夜行者 / 斯拉克 | Murloc Nightcrawler / Slark |
| c89 | `characters/天灾_scourge/c89_Gorgon/` | 蛇发女妖 / 美杜莎 | Gorgon / Medusa |
| c90 | `characters/天灾_scourge/c90_Faceless_Void/` | 虚空假面 / 暗惧者 | Faceless Void / Darkterror |
| c91 | `characters/天灾_scourge/c91_Lightning_Revenant/` | 闪电幽魂 / 剃刀 | Lightning Revenant / Razor |
| c92 | `characters/天灾_scourge/c92_Arc_Warden/` | 弧光守望者 / 泽特 | Arc Warden / Zet |

### 天灾 · 智力（20）· 召唤物号段 m200–m219

| 键 | 目录 | 中文 | 英文称号 / 本名 |
|---|---|---|---|
| c93 | `characters/天灾_scourge/c93_Enigma/` | 谜团 / 达克罗 | Enigma / Darchrow |
| c94 | `characters/天灾_scourge/c94_Lich/` | 巫妖 / 克尔苏加德 | Lich / Kel'Thuzad |
| c95 | `characters/天灾_scourge/c95_Death_Prophet/` | 死亡先知 / 克萝贝露丝 | Death Prophet / Krobelus |
| c96 | `characters/天灾_scourge/c96_Demon_Witch/` | 恶魔巫师 / 莱恩 | Demon Witch / Lion |
| c97 | `characters/天灾_scourge/c97_Queen_of_Pain/` | 痛苦女王 / 阿卡莎 | Queen of Pain / Akasha |
| c98 | `characters/天灾_scourge/c98_Oblivion/` | 湮灭法师 / 帕格纳 | Oblivion / Pugna |
| c99 | `characters/天灾_scourge/c99_Necrolyte/` | 死灵法师 / 罗坦德吉利 | Necrolyte / Rotund'jere |
| c100 | `characters/天灾_scourge/c100_Dark_Seer/` | 黑暗贤者 / 依什卡菲尔 | Dark Seer / Ish'kafel |
| c101 | `characters/天灾_scourge/c101_Obsidian_Destroyer/` | 黑曜毁灭者 / 先兆者 | Obsidian Destroyer / Harbinger |
| c102 | `characters/天灾_scourge/c102_Bane_Elemental/` | 祸乱之源 / 阿特洛波斯 | Bane Elemental / Atropos |
| c103 | `characters/天灾_scourge/c103_Warlock/` | 术士 / 戴蒙．莱尼克 | Warlock / Demnok Lannik |
| c104 | `characters/天灾_scourge/c104_Shadow_Demon/` | 暗影恶魔 / 艾瑞达 | Shadow Demon / Eredar |
| c105 | `characters/天灾_scourge/c105_Ancient_Apparition/` | 远古冰魄 / 卡尔德 | Ancient Apparition / Kaldr |
| c106 | `characters/天灾_scourge/c106_Tormented_Soul/` | 受折磨的灵魂 / 恶毒的拉席克 | Tormented Soul / Leshrac the Malicious |
| c107 | `characters/天灾_scourge/c107_Necrolic/` | 死灵飞龙 / 维萨吉 | Necro'lic / Visage |
| c108 | `characters/天灾_scourge/c108_Witch_Doctor/` | 巫医 / 沃金 | Witch Doctor / Vol'Jin |
| c109 | `characters/天灾_scourge/c109_Shadow_Priest/` | 暗影牧师 / 戴泽 | Shadow Priest / Dazzle |
| c110 | `characters/天灾_scourge/c110_Invoker/` | 祈求者 / 凯尔 | Invoker / Kael |
| c111 | `characters/天灾_scourge/c111_Batrider/` | 蝙蝠骑士 / 金扎卡 | Batrider / Jin'zakk |
| c112 | `characters/天灾_scourge/c112_Winter_Wyvern/` | 寒冬飞龙 / 傲洛斯 | Winter Wyvern / Auroth |
## 小兵、Roshan 与中立野怪（m1–m29）

超级兵是同卡的变体子目录 `m{N}-1_超级兵/`（同模型、更大，d01 §4）。

| 键 | 目录 | 中文 | 原典（d01） |
|---|---|---|---|
| m1 | `characters/近卫_sentinel/m1_Treant/` | 树人（近卫近战兵） | `esen` · Ent |
| m2 | `characters/近卫_sentinel/m2_Druid_of_the_Talon/` | 猛禽德鲁伊（近卫远程兵） | `edry` |
| m3 | `characters/近卫_sentinel/m3_Glaive_Thrower/` | 投刃车（近卫攻城） | `ebal` · Ballista |
| m4 | `characters/天灾_scourge/m4_Ghoul/` | 食尸鬼（天灾近战兵） | `ugho` |
| m5 | `characters/天灾_scourge/m5_Necromancer/` | 亡灵法师（天灾远程兵） | `unec` |
| m6 | `characters/天灾_scourge/m6_Meat_Wagon/` | 绞肉车（天灾攻城） | `umtw` |
| m7 | `characters/中立_neutral/m7_Roshan/` | Roshan | `n00L` · 紫色岩石傀儡 ×2 |
| m8 | `characters/中立_neutral/m8_Kobold/` | 狗头人（含工头、隧道工变体） | Kobold |
| m9 | `characters/中立_neutral/m9_Forest_Troll/` | 森林巨魔（狂战士、牧师变体） | ForestTroll |
| m10 | `characters/中立_neutral/m10_Gnoll_Assassin/` | 豺狼刺客 | GnollArcher |
| m11 | `characters/中立_neutral/m11_Ghost/` | 鬼魂 | BansheeGhost |
| m12 | `characters/中立_neutral/m12_Fel_Beast/` | 魔能野兽 | FelstalkerPurple |
| m13 | `characters/中立_neutral/m13_Harpy/` | 鹰身女妖（斥候、风暴变体） | Harpy |
| m14 | `characters/中立_neutral/m14_Giant_Wolf/` | 巨狼（头狼变体） | TimberWolf |
| m15 | `characters/中立_neutral/m15_Mud_Golem/` | 泥土傀儡 | RockGolem 褐 |
| m16 | `characters/中立_neutral/m16_Ogre/` | 食人魔（拳手、法师变体） | Ogre |
| m17 | `characters/中立_neutral/m17_Satyr/` | 萨特（诡计师、窃魂者、地狱召唤者变体） | Satyr |
| m18 | `characters/中立_neutral/m18_Centaur/` | 半人马（先行者、可汗变体） | Centaur |
| m19 | `characters/中立_neutral/m19_Dark_Troll/` | 黑暗巨魔（首领变体） | DarkTroll |
| m20 | `characters/中立_neutral/m20_Wildkin/` | 枭兽（暴怒变体） | Owlbear |
| m21 | `characters/中立_neutral/m21_Polar_Furbolg/` | 极地熊怪 | PolarFurbolg |
| m22 | `characters/中立_neutral/m22_Rock_Golem/` | 岩石傀儡（宝石傀儡变体） | RockGolem |
| m23 | `characters/中立_neutral/m23_Dragonspawn/` | 蓝龙人（监工、巫师变体） | DragonSpawn |
| m24 | `characters/中立_neutral/m24_Black_Dragon/` | 黑龙（黑色幼龙 Black Drake 变体；原误译「黑蜉蝣」，follow-up 057） | BlackDragon |
| m25 | `characters/中立_neutral/m25_Jungle_Stalker/` | 丛林捕猎者 | JungleBeast |
| m26 | `characters/中立_neutral/m26_Thunder_Lizard/` | 雷霆蜥蜴 | ThunderLizard |

m27–m29 预留给野怪补漏；召唤物从 m100 起按上表号段。


## 召唤物（m100+，已用的号）

| 键 | 目录 | 名称 |
|---|---|---|
| m100 | `characters/近卫_sentinel/m100_Hawk/` | 战鹰 · Hawk（Scout Hawk / Greater Hawk）· 兽王召唤的猛禽 |
| m101 | `characters/近卫_sentinel/m101_Boar/` | 野猪 · Boar（Fel Boar）· 兽王召唤的野兽 |
| m102 | `characters/近卫_sentinel/m102_Earth_Panda/` | 土熊猫 · Earth（Earth Pandaren Brewmaster）· 酒仙分出的土之分身 |
| m103 | `characters/近卫_sentinel/m103_Storm_Panda/` | 风熊猫 · Storm（Storm Pandaren Brewmaster）· 酒仙分出的风之分身 |
| m104 | `characters/近卫_sentinel/m104_Fire_Panda/` | 火熊猫 · Fire（Fire Pandaren Brewmaster）· 酒仙分出的火之分身 |
| m105 | `characters/近卫_sentinel/m105_Ghost_Ship/` | 幽灵船 · Ghost Ship · 舰队统帅召来的亡灵战船 |
| m110 | `characters/近卫_sentinel/m110_Wisp_Spirit/` | 幽魂光球 · Spirit · （无本名，地图单位 `h0CJ`） |
| m111 | `characters/近卫_sentinel/m111_Power_Cog/` | 能量齿轮 · Power Cog · （无本名） |
| m112 | `characters/近卫_sentinel/m112_Frozen_Sigil/` | 冰封魔印 · Frozen Sigil · （无本名） |
| m113 | `characters/近卫_sentinel/m113_Stone_Remnant/` | 残岩 · Stone Remnant · （无本名） |
| m120 | `characters/近卫_sentinel/m120_Spirit_Bear/` | 熊灵 · Spirit Bear · （德鲁伊的熊灵伙伴） |
| m121 | `characters/近卫_sentinel/m121_Healing_Ward/` | 治疗守卫 · Healing Ward · （主宰的治疗图腾） |
| m130 | `characters/近卫_sentinel/m130_Psionic_Trap/` | 灵能陷阱 · Psionic Trap · （圣堂刺客放置物，无本名） |
| m131 | `characters/近卫_sentinel/m131_Fire_Remnant/` | 火之余烬（火焰残影） · Fire Remnant · （灰烬之灵的残影，无本名） |
| m140 | `characters/近卫_sentinel/m140_Natures_Attendant/` | 小精灵（自然之助） · Nature's Attendant · 无本名 |
| m150 | `characters/近卫_sentinel/m150_Tinker_Robot/` | 发条小机器人 · March of the Machines Robot · HeroTinkerRobot |
| m151 | `characters/近卫_sentinel/m151_Land_Mine/` | 地雷 · Land Mine · GoblinLandMine |
| m152 | `characters/近卫_sentinel/m152_Stasis_Trap/` | 麻痹陷阱 · Stasis Trap · StasisTotem |
| m153 | `characters/近卫_sentinel/m153_Remote_Mine/` | 遥控炸弹 · Remote Mine · TNTBarrel |
| m154 | `characters/近卫_sentinel/m154_Serpent_Ward/` | 蛇形守卫 · Serpent Ward · SerpentWard |
| m155 | `characters/近卫_sentinel/m155_Voodoo_Chicken/` | 妖术小鸡 · Voodoo Chicken · EasterChicken |
| m160 | `characters/天灾_scourge/m160_Spirit_Wolf/` | 灵狼 · Spirit Wolf · （无本名） |
| m161 | `characters/天灾_scourge/m161_Tombstone/` | 墓碑 · Tombstone · （无本名） |
| m162 | `characters/天灾_scourge/m162_Tombstone_Zombie/` | 墓碑僵尸 · Tombstone Zombie · （无本名） |
| m180 | `characters/天灾_scourge/m180_Spiderling/` | 幼蛛 · Spiderling · （无本名） |
| m181 | `characters/天灾_scourge/m181_Swarm_Beetle/` | 噬甲虫 · Swarm Beetle · （无本名） |
| m182 | `characters/天灾_scourge/m182_Plague_Ward/` | 瘟疫守卫 · Plague Ward · （无本名） |
| m190 | `characters/天灾_scourge/m190_Spark_Wraith/` | 闪光怨灵 · Spark Wraith · （召唤物，无本名） |
| m200 | `characters/天灾_scourge/m200_Eidolon/` | 精神体 · Eidolon（恶魔转化变出的小虚空体） |
| m201 | `characters/天灾_scourge/m201_Exorcism_Ghost/` | 恶灵 · Ghosts（驱使恶灵放出的恶灵） |
| m202 | `characters/天灾_scourge/m202_Nether_Ward/` | 幽冥守卫 · Nether Ward |
| m210 | `characters/天灾_scourge/m210_Infernal/` | 地狱火 · Infernal · 术士的召唤物 |
| m211 | `characters/天灾_scourge/m211_Familiar/` | 佣兽 · Familiar · 死灵飞龙的石像鬼 |
| m212 | `characters/天灾_scourge/m212_Death_Ward/` | 死亡守卫 · Death Ward · 巫医的图腾 |
| m213 | `characters/天灾_scourge/m213_Forged_Spirit/` | 熔炉精灵 · Forged Spirit · 祈求者的召唤物 |

## 商人（m300–m309，follow-up 053）

人形商店的商人（两方基地是同一模型，归中立）；号段 m300–m319 留给商店与地图 NPC。原版外观见 `0_research/parts/d16_地图建筑与商店.md` §3。

| 键 | 目录 | 商店 | 站位 |
|---|---|---|---|
| m300 | `characters/中立_neutral/m300_Weapons_Dealer/` | 武器商人 Weapons Dealer | bg24 / bg34 能量圈旁 |
| m301 | `characters/中立_neutral/m301_Sena_the_Accessorizer/` | 饰品商人 希娜 Sena the Accessorizer | 同上 |
| m302 | `characters/中立_neutral/m302_Supportive_Vestments/` | 支援法衣 Supportive Vestments | bg24 / bg34 栅栏一排 |
| m303 | `characters/中立_neutral/m303_Gateway_Relics/` | 圣物关口 Gateway Relics | 同上 |
| m304 | `characters/中立_neutral/m304_Arcane_Sanctum/` | 秘法圣所 Arcane Sanctum | 同上 |
| m305 | `characters/中立_neutral/m305_Ancient_Weaponry/` | 远古兵器 Ancient Weaponry | 同上（排头） |
| m306 | `characters/中立_neutral/m306_Enchanted_Artifacts/` | 附魔古物 Enchanted Artifacts | 同上 |
| m307 | `characters/中立_neutral/m307_Protectorate/` | 保护领地 Protectorate | 同上 |
| m308 | `characters/中立_neutral/m308_Leragas_the_Vile/` | 秘密商店 黑市商人 雷拉格斯 | bg11 / bg35 |
| m309 | `characters/中立_neutral/m309_Goblin_Merchant/` | 边路商店 地精商人 | bg12 平台上 |

## 背景（bg1–bg39）

目录 `background/{阵营}/bg{N}_{主体}/`，号的唯一出处 `background/registry.toml`；「区」是地图上的位置，「阵营目录」是存放分组（公共商店归中立）。bg1 是世界锚点（自由生成），其余挂它图生图。

| 键 | 区 | 阵营目录 | 主体 | 用途（d01 §6 搭场景建议） |
|---|---|---|---|---|
| bg1 | river | 中立_neutral | 中路河道交叉口 | 世界锚点；技能主舞台 |
| bg2 | sentinel | 近卫_sentinel | 近卫基地·世界之树 | 近卫英雄亮相 |
| bg3 | scourge | 天灾_scourge | 天灾基地·冰封王座 | 天灾英雄亮相 |
| bg4 | sentinel | 近卫_sentinel | 近卫中路一塔 | 兵线交战、连放技能 |
| bg5 | scourge | 天灾_scourge | 天灾中路一塔 | 同上 |
| bg6 | river | 中立_neutral | 上河道神符点 | 入场、水与冰系技能 |
| bg7 | river | 中立_neutral | 下河道神符点 | 同上 |
| bg8 | sentinel | 近卫_sentinel | 近卫野区空地 | 隐身、位移类英雄 |
| bg9 | scourge | 天灾_scourge | 天灾野区空地 | 同上 |
| bg10 | river | 中立_neutral | 巨兽巢穴（Roshan 巢穴；目录名避开专名） | 大英雄压迫镜头 |
| bg11 | sentinel | 中立_neutral | 秘密商店 | 买装备过场 |
| bg12 | sentinel | 中立_neutral | 边路地精商店 | 同上 |
| bg13 | sentinel | 近卫_sentinel | 近卫泉水与商店 | 出生、亮相 |
| bg14 | scourge | 天灾_scourge | 天灾泉水与商店 | 同上 |
| bg15 | sentinel | 近卫_sentinel | 近卫泉水 | 单体建筑锚点（follow-up 053 起，原版外观见 `0_research/parts/d16`） |
| bg16 | sentinel | 近卫_sentinel | 近卫防御塔 | 单体建筑；bg4 锚点图形制与原版不符，待用户定 |
| bg17 | sentinel | 近卫_sentinel | 战争古树 | 近战兵营 |
| bg18 | sentinel | 近卫_sentinel | 知识古树 | 远程兵营 |
| bg19 | sentinel | 近卫_sentinel | 月亮井 | 附属建筑 ×11 |
| bg20 | sentinel | 近卫_sentinel | 风之古树 | 附属建筑 ×2（只有 WC3 经典资料） |
| bg21 | sentinel | 近卫_sentinel | 猎手大厅 | 附属建筑 ×2（同上） |
| bg22 | sentinel | 近卫_sentinel | 奇迹古树 | 商店建筑（消耗品） |
| bg23 | sentinel | 近卫_sentinel | 奎尔瑟兰的密室 | 商店建筑（杂货） |
| bg24 | sentinel | 近卫_sentinel | 近卫商人营地 | 8 家人形商店站位（商人 m300–m307） |
| bg25 | scourge | 天灾_scourge | 天灾泉水 | 单体建筑 |
| bg26 | scourge | 天灾_scourge | 天灾防御塔 | 单体建筑；bg5 锚点图形制与原版不符，待用户定 |
| bg27 | scourge | 天灾_scourge | 地穴 | 近战兵营 |
| bg28 | scourge | 天灾_scourge | 诅咒神庙 | 远程兵营 |
| bg29 | scourge | 天灾_scourge | 通灵塔 | 附属建筑 ×11（bg26 熄灭版） |
| bg30 | scourge | 天灾_scourge | 埋骨地 | 附属建筑 ×2 |
| bg31 | scourge | 天灾_scourge | 牺牲深渊 | 附属建筑 ×2 |
| bg32 | scourge | 天灾_scourge | 崩碎之穴 | 商店建筑（消耗品） |
| bg33 | scourge | 天灾_scourge | 恶魔遗物 | 商店建筑（杂货） |
| bg34 | scourge | 天灾_scourge | 天灾商人营地 | 8 家人形商店站位（商人 m300–m307） |
| bg35 | scourge | 中立_neutral | 天灾侧秘密商店 | 秘密商店天灾一侧（商人 m308） |
| bg36 | sentinel | 中立_neutral | 地精实验室 | 边路商店第二座建筑（bg12 是地精商人，商人 m309） |
| bg37 | scourge | 天灾_scourge | 天灾四级蛛魔塔 | 遗迹前两座四级塔共用，bg37#01/#02 |
| bg38 | sentinel | 近卫_sentinel | 近卫基地全景 | 30建筑实例的整体搭景；尺度候选、技术体块与三机位 |
| bg39 | scourge | 天灾_scourge | 天灾基地全景 | 30建筑实例的整体搭景；尺度候选、技术体块与三机位 |

## 道具（p 号）

由 `tools/props_lib.py` 的 `allocate()` 领号，唯一出处 `props/registry.toml`。范围：主动效果上镜的物品、Roshan 掉落、神符、魔瓶等 demo 可能入画的物件（d08 §4）；~~被动属性装不立卡~~——follow-up 310（2026-11-01）起 6.83d 全部 131 件商店 / Roshan 物品与通用合成卷轴都立卡，货单见下节。

| 键 | 名称 |
|---|---|
| p1 | 极速神符 |
| p2 | 回复神符 |
| p3 | 双倍伤害神符 |
| p4 | 幻象神符 |
| p5 | 隐形神符 |
| p6 | 赏金神符 |
| p7 | 不朽之守护 |
| p8 | 奶酪 |
| p9 | 魔瓶 |
| p10 | 圣剑 |
| p11 | 掉落物品棕皮书 |
| p12 | 科勒的匕首（跳刀） |
| p13 | Eul 的神圣法杖（吹风） |
| p14 | Guinsoo 的邪恶镰刀（羊刀） |
| p15 | 幻影斧（分身斧） |
| p16 | 希瓦的守护（冰甲） |
| p17 | 迈达斯之手（点金手） |
| p18 | 黑皇杖（BKB） |
| p19 | 辉耀 |
| p20 | 狂战斧 |
| p21 | 刷新球 |
| p22 | 回城卷轴 |
| p23 | 梅肯斯姆 |
| p24 | 达贡之神力 |
| p25 | 疯狂面具 |
| p26 | 洛萨之锋（隐刀） |
| p27 | 侦察守卫（假眼） |
| p28 | 艾西菲的远古祭祀（吃树） |
| p29 | 敌法师月刃（`c24` 双持；`props/近卫_sentinel/`，2026-10-21 follow-up 046） |
| p30 | 斧王巨斧（`c65` 双手持；`props/天灾_scourge/`，2026-10-22 follow-up 071：照现立绘斧头定形，斧王所有视频与峰值图都挂） |

### 商店物品（follow-up 310，2026-11-01）

6.83d 全部商店物品立卡出锚点图：新立 p122–p232（111 件，含通用合成卷轴 p232），加上已有的 p7–p10、p12–p28 共 132 件。**每个商店 / NPC 卖什么**看 [props/shop_items.md](props/shop_items.md)（机读源 `props/shop_items.json`；各商人卡、商店建筑卡末尾也有「售卖道具」节）。参考图只用 DotA 1 / 魔兽 3 原版物品图标（只作人眼参考）在 `0_research/item_refs/`，各目录 `refs.md` 写来源与 sha；follow-up 316 起严格 DotA 1，Dota 2 图标已删，39 件按 DotA 1 图标重写重出。

| 键 | 名称 |
|---|---|
| [p122](props/中立_neutral/p122_Mantle_of_Intelligence/p122_Mantle_of_Intelligence.md) | 智力斗篷｜Mantle of Intelligence（基础件） |
| [p123](props/中立_neutral/p123_Gauntlets_of_Strength/p123_Gauntlets_of_Strength.md) | 力量手套｜Gauntlets of Strength（基础件） |
| [p124](props/中立_neutral/p124_Slippers_of_Agility/p124_Slippers_of_Agility.md) | 敏捷便鞋｜Slippers of Agility（基础件） |
| [p125](props/中立_neutral/p125_Ironwood_Branch/p125_Ironwood_Branch.md) | 铁树枝干｜Ironwood Branch（基础件） |
| [p126](props/中立_neutral/p126_Circlet_of_Nobility/p126_Circlet_of_Nobility.md) | 贵族圆环｜Circlet of Nobility（基础件） |
| [p127](props/中立_neutral/p127_Belt_of_Giant_Strength/p127_Belt_of_Giant_Strength.md) | 巨人力量腰带｜Belt of Giant Strength（基础件） |
| [p128](props/中立_neutral/p128_Robe_of_the_Magi/p128_Robe_of_the_Magi.md) | 法师长袍｜Robe of the Magi（基础件） |
| [p129](props/中立_neutral/p129_Boots_of_Elvenskin/p129_Boots_of_Elvenskin.md) | 精灵皮靴｜Boots of Elvenskin（基础件） |
| [p130](props/中立_neutral/p130_Ogre_Axe/p130_Ogre_Axe.md) | 食人魔之斧｜Ogre Axe（基础件） |
| [p131](props/中立_neutral/p131_Staff_of_Wizardry/p131_Staff_of_Wizardry.md) | 魔力法杖｜Staff of Wizardry（基础件） |
| [p132](props/中立_neutral/p132_Blade_of_Alacrity/p132_Blade_of_Alacrity.md) | 欢欣之刃｜Blade of Alacrity（基础件） |
| [p133](props/中立_neutral/p133_Ultimate_Orb/p133_Ultimate_Orb.md) | 极限法球｜Ultimate Orb（基础件） |
| [p134](props/中立_neutral/p134_Quelling_Blade/p134_Quelling_Blade.md) | 压制之刃｜Quelling Blade（基础件） |
| [p135](props/中立_neutral/p135_Blades_of_Attack/p135_Blades_of_Attack.md) | 攻击之爪｜Blades of Attack（基础件） |
| [p136](props/中立_neutral/p136_Quarterstaff/p136_Quarterstaff.md) | 短棍｜Quarterstaff（基础件） |
| [p137](props/中立_neutral/p137_Broadsword/p137_Broadsword.md) | 阔剑｜Broadsword（基础件） |
| [p138](props/中立_neutral/p138_Claymore/p138_Claymore.md) | 大剑｜Claymore（基础件） |
| [p139](props/中立_neutral/p139_Javelin/p139_Javelin.md) | 标枪｜Javelin（基础件） |
| [p140](props/中立_neutral/p140_Mithril_Hammer/p140_Mithril_Hammer.md) | 秘银锤｜Mithril Hammer（基础件） |
| [p141](props/中立_neutral/p141_Ring_of_Protection/p141_Ring_of_Protection.md) | 守护指环｜Ring of Protection（基础件） |
| [p142](props/中立_neutral/p142_Stout_Shield/p142_Stout_Shield.md) | 圆盾｜Stout Shield（基础件） |
| [p143](props/中立_neutral/p143_Chainmail/p143_Chainmail.md) | 锁甲｜Chainmail（基础件） |
| [p144](props/中立_neutral/p144_Helm_of_Iron_Will/p144_Helm_of_Iron_Will.md) | 铁意头盔｜Helm of Iron Will（基础件） |
| [p145](props/中立_neutral/p145_Plate_Mail/p145_Plate_Mail.md) | 板甲｜Plate Mail（基础件） |
| [p146](props/中立_neutral/p146_Gem_of_True_Sight/p146_Gem_of_True_Sight.md) | 真视宝石｜Gem of True Sight（基础件） |
| [p147](props/中立_neutral/p147_Ghost_Scepter/p147_Ghost_Scepter.md) | 幽灵权杖｜Ghost Scepter（基础件） |
| [p148](props/中立_neutral/p148_Talisman_of_Evasion/p148_Talisman_of_Evasion.md) | 闪避护符｜Talisman of Evasion（基础件） |
| [p149](props/中立_neutral/p149_Magic_Stick/p149_Magic_Stick.md) | 魔棒｜Magic Stick（基础件） |
| [p150](props/中立_neutral/p150_Mask_of_Death/p150_Mask_of_Death.md) | 死亡面具｜Mask of Death（基础件） |
| [p151](props/中立_neutral/p151_Ring_of_Regeneration/p151_Ring_of_Regeneration.md) | 恢复指环｜Ring of Regeneration（基础件） |
| [p152](props/中立_neutral/p152_Sobi_Mask/p152_Sobi_Mask.md) | 艺人面罩｜Sobi Mask（基础件） |
| [p153](props/中立_neutral/p153_Planeswalker_s_Cloak/p153_Planeswalker_s_Cloak.md) | 流浪法师斗篷｜Planeswalker's Cloak（基础件） |
| [p154](props/中立_neutral/p154_Gloves_of_Haste/p154_Gloves_of_Haste.md) | 加速手套｜Gloves of Haste（基础件） |
| [p155](props/中立_neutral/p155_Boots_of_Speed/p155_Boots_of_Speed.md) | 速度之鞋｜Boots of Speed（基础件） |
| [p156](props/中立_neutral/p156_Shadow_Amulet/p156_Shadow_Amulet.md) | 暗影护符｜Shadow Amulet（基础件） |
| [p157](props/中立_neutral/p157_Clarity_Potion/p157_Clarity_Potion.md) | 净化药水｜Clarity Potion（消耗品） |
| [p158](props/中立_neutral/p158_Healing_Salve/p158_Healing_Salve.md) | 治疗药膏｜Healing Salve（消耗品） |
| [p159](props/中立_neutral/p159_Dust_of_Appearance/p159_Dust_of_Appearance.md) | 显影之尘｜Dust of Appearance（消耗品） |
| [p160](props/中立_neutral/p160_Sentry_Wards/p160_Sentry_Wards.md) | 岗哨守卫｜Sentry Wards（消耗品） |
| [p161](props/中立_neutral/p161_Smoke_of_Deceit/p161_Smoke_of_Deceit.md) | 诡计之雾｜Smoke of Deceit（消耗品） |
| [p162](props/中立_neutral/p162_Animal_Courier/p162_Animal_Courier.md) | 动物信使｜Animal Courier（消耗品） |
| [p163](props/中立_neutral/p163_Flying_Courier/p163_Flying_Courier.md) | 飞行信使｜Flying Courier（消耗品） |
| [p164](props/中立_neutral/p164_Demon_Edge/p164_Demon_Edge.md) | 恶魔刀锋｜Demon Edge（秘密商店基础件） |
| [p165](props/中立_neutral/p165_Eaglehorn/p165_Eaglehorn.md) | 鹰角弓｜Eaglehorn（秘密商店基础件） |
| [p166](props/中立_neutral/p166_Energy_Booster/p166_Energy_Booster.md) | 能量之球｜Energy Booster（秘密商店基础件） |
| [p167](props/中立_neutral/p167_Messerschmidt_s_Reaver/p167_Messerschmidt_s_Reaver.md) | 梅塞施密特的掠夺｜Messerschmidt's Reaver（秘密商店基础件） |
| [p168](props/中立_neutral/p168_Mystic_Staff/p168_Mystic_Staff.md) | 神秘法杖｜Mystic Staff（秘密商店基础件） |
| [p169](props/中立_neutral/p169_Point_Booster/p169_Point_Booster.md) | 精气之球｜Point Booster（秘密商店基础件） |
| [p170](props/中立_neutral/p170_Sacred_Relic/p170_Sacred_Relic.md) | 圣者遗物｜Sacred Relic（秘密商店基础件） |
| [p171](props/中立_neutral/p171_Vitality_Booster/p171_Vitality_Booster.md) | 活力之球｜Vitality Booster（秘密商店基础件） |
| [p172](props/中立_neutral/p172_Hyperstone/p172_Hyperstone.md) | 振奋宝石｜Hyperstone（秘密商店基础件） |
| [p173](props/中立_neutral/p173_Ring_of_Health/p173_Ring_of_Health.md) | 医疗指环｜Ring of Health（秘密商店基础件） |
| [p174](props/中立_neutral/p174_Void_Stone/p174_Void_Stone.md) | 虚无宝石｜Void Stone（秘密商店基础件） |
| [p175](props/中立_neutral/p175_Orb_of_Venom/p175_Orb_of_Venom.md) | 淬毒之珠｜Orb of Venom（秘密商店基础件） |
| [p176](props/中立_neutral/p176_Magic_Wand/p176_Magic_Wand.md) | 魔杖｜Magic Wand（合成成品） |
| [p177](props/中立_neutral/p177_Perseverance/p177_Perseverance.md) | 坚韧球｜Perseverance（合成成品） |
| [p178](props/中立_neutral/p178_Oblivion_Staff/p178_Oblivion_Staff.md) | 空明杖｜Oblivion Staff（合成成品） |
| [p179](props/中立_neutral/p179_Bracer/p179_Bracer.md) | 护腕｜Bracer（合成成品） |
| [p180](props/中立_neutral/p180_Wraith_Band/p180_Wraith_Band.md) | 怨灵系带｜Wraith Band（合成成品） |
| [p181](props/中立_neutral/p181_Null_Talisman/p181_Null_Talisman.md) | 空灵挂件｜Null Talisman（合成成品） |
| [p182](props/中立_neutral/p182_Boots_of_Travel/p182_Boots_of_Travel.md) | 远行鞋｜Boots of Travel（合成成品） |
| [p183](props/中立_neutral/p183_Phase_Boots/p183_Phase_Boots.md) | 相位鞋｜Phase Boots（合成成品） |
| [p184](props/中立_neutral/p184_Power_Treads/p184_Power_Treads.md) | 动力鞋｜Power Treads（合成成品） |
| [p185](props/中立_neutral/p185_Poor_Man_s_Shield/p185_Poor_Man_s_Shield.md) | 穷鬼盾｜Poor Man's Shield（合成成品） |
| [p186](props/中立_neutral/p186_Soul_Ring/p186_Soul_Ring.md) | 灵魂之戒｜Soul Ring（合成成品） |
| [p187](props/中立_neutral/p187_Urn_of_Shadows/p187_Urn_of_Shadows.md) | 影之灵龛｜Urn of Shadows（合成成品） |
| [p188](props/中立_neutral/p188_Ring_of_Basilius/p188_Ring_of_Basilius.md) | 王者之戒｜Ring of Basilius（合成成品） |
| [p189](props/中立_neutral/p189_Ring_of_Aquila/p189_Ring_of_Aquila.md) | 天鹰之戒｜Ring of Aquila（合成成品） |
| [p190](props/中立_neutral/p190_Headdress_of_Rejuvenation/p190_Headdress_of_Rejuvenation.md) | 恢复头巾｜Headdress of Rejuvenation（合成成品） |
| [p191](props/中立_neutral/p191_Nathrezim_Buckler/p191_Nathrezim_Buckler.md) | 玄冥盾牌｜Nathrezim Buckler（合成成品） |
| [p192](props/中立_neutral/p192_Khadgar_s_Pipe_of_Insight/p192_Khadgar_s_Pipe_of_Insight.md) | 卡嘉之洞察长笛｜Khadgar's Pipe of Insight（合成成品） |
| [p193](props/中立_neutral/p193_Vladmir_s_Offering/p193_Vladmir_s_Offering.md) | 弗拉迪米尔的祭品｜Vladmir's Offering（合成成品） |
| [p194](props/中立_neutral/p194_Arcane_Boots/p194_Arcane_Boots.md) | 秘法鞋｜Arcane Boots（合成成品） |
| [p195](props/中立_neutral/p195_Medallion_of_Courage/p195_Medallion_of_Courage.md) | 勇气勋章｜Medallion of Courage（合成成品） |
| [p196](props/中立_neutral/p196_Ancient_Janggo_of_Endurance/p196_Ancient_Janggo_of_Endurance.md) | 先祖韧鼓｜Ancient Janggo of Endurance（合成成品） |
| [p197](props/中立_neutral/p197_Tranquil_Boots/p197_Tranquil_Boots.md) | 静谧之鞋｜Tranquil Boots（合成成品） |
| [p198](props/中立_neutral/p198_Assault_Cuirass/p198_Assault_Cuirass.md) | 强袭装甲｜Assault Cuirass（合成成品） |
| [p199](props/中立_neutral/p199_Blade_Mail/p199_Blade_Mail.md) | 刃甲｜Blade Mail（合成成品） |
| [p200](props/中立_neutral/p200_Heart_of_Tarrasque/p200_Heart_of_Tarrasque.md) | 恐鳌之心｜Heart of Tarrasque（合成成品） |
| [p201](props/中立_neutral/p201_Soul_Booster/p201_Soul_Booster.md) | 振魂石｜Soul Booster（合成成品） |
| [p202](props/中立_neutral/p202_Bloodstone/p202_Bloodstone.md) | 血精石｜Bloodstone（合成成品） |
| [p203](props/中立_neutral/p203_Linken_s_Sphere/p203_Linken_s_Sphere.md) | 林肯法球｜Linken's Sphere（合成成品） |
| [p204](props/中立_neutral/p204_Hood_of_Defiance/p204_Hood_of_Defiance.md) | 挑战头巾｜Hood of Defiance（合成成品） |
| [p205](props/中立_neutral/p205_Vanguard/p205_Vanguard.md) | 先锋盾｜Vanguard（合成成品） |
| [p206](props/中立_neutral/p206_Crimson_Guard/p206_Crimson_Guard.md) | 赤红甲｜Crimson Guard（合成成品） |
| [p207](props/中立_neutral/p207_Sange/p207_Sange.md) | 散华｜Sange（合成成品） |
| [p208](props/中立_neutral/p208_Yasha/p208_Yasha.md) | 夜叉｜Yasha（合成成品） |
| [p209](props/中立_neutral/p209_Sange_and_Yasha/p209_Sange_and_Yasha.md) | 散夜对剑｜Sange and Yasha（合成成品） |
| [p210](props/中立_neutral/p210_Satanic/p210_Satanic.md) | 撒旦之邪力｜Satanic（合成成品） |
| [p211](props/中立_neutral/p211_Helm_of_the_Dominator/p211_Helm_of_the_Dominator.md) | 支配头盔｜Helm of the Dominator（合成成品） |
| [p212](props/中立_neutral/p212_Maelstrom/p212_Maelstrom.md) | 漩涡｜Maelstrom（合成成品） |
| [p213](props/中立_neutral/p213_Mjollnir/p213_Mjollnir.md) | 雷神之锤｜Mjollnir（合成成品） |
| [p214](props/中立_neutral/p214_Eye_of_Skadi/p214_Eye_of_Skadi.md) | 斯嘉蒂之眼｜Eye of Skadi（合成成品） |
| [p215](props/中立_neutral/p215_Stygian_Desolator/p215_Stygian_Desolator.md) | 黯灭｜Stygian Desolator（合成成品） |
| [p216](props/中立_neutral/p216_Diffusal_Blade/p216_Diffusal_Blade.md) | 净魂之刃｜Diffusal Blade（合成成品） |
| [p217](props/中立_neutral/p217_Heaven_s_Halberd/p217_Heaven_s_Halberd.md) | 天堂之戟｜Heaven's Halberd（合成成品） |
| [p218](props/中立_neutral/p218_Monkey_King_Bar/p218_Monkey_King_Bar.md) | 金箍棒｜Monkey King Bar（合成成品） |
| [p219](props/中立_neutral/p219_The_Butterfly/p219_The_Butterfly.md) | 蝴蝶｜The Butterfly（合成成品） |
| [p220](props/中立_neutral/p220_Buriza_do_Kyanon/p220_Buriza_do_Kyanon.md) | 大炮｜Buriza-do Kyanon（合成成品） |
| [p221](props/中立_neutral/p221_Cranium_Basher/p221_Cranium_Basher.md) | 碎颅锤｜Cranium Basher（合成成品） |
| [p222](props/中立_neutral/p222_Crystalys/p222_Crystalys.md) | 水晶剑｜Crystalys（合成成品） |
| [p223](props/中立_neutral/p223_Armlet_of_Mordiggian/p223_Armlet_of_Mordiggian.md) | 食尸鬼王的臂章｜Armlet of Mordiggian（合成成品） |
| [p224](props/中立_neutral/p224_Ethereal_Blade/p224_Ethereal_Blade.md) | 虚灵之刃｜Ethereal Blade（合成成品） |
| [p225](props/中立_neutral/p225_Abyssal_Blade/p225_Abyssal_Blade.md) | 深渊之刃｜Abyssal Blade（合成成品） |
| [p226](props/中立_neutral/p226_Orchid_Malevolence/p226_Orchid_Malevolence.md) | 紫怨｜Orchid Malevolence（合成成品） |
| [p227](props/中立_neutral/p227_Force_Staff/p227_Force_Staff.md) | 原力法杖｜Force Staff（合成成品） |
| [p228](props/中立_neutral/p228_Necronomicon/p228_Necronomicon.md) | 死灵书｜Necronomicon（合成成品） |
| [p229](props/中立_neutral/p229_Aghanim_s_Scepter/p229_Aghanim_s_Scepter.md) | 阿哈利姆神杖｜Aghanim's Scepter（合成成品） |
| [p230](props/中立_neutral/p230_Veil_of_Discord/p230_Veil_of_Discord.md) | 纷争面纱｜Veil of Discord（合成成品） |
| [p231](props/中立_neutral/p231_Rod_of_Atos/p231_Rod_of_Atos.md) | 阿托斯之棍｜Rod of Atos（合成成品） |
| [p232](props/中立_neutral/p232_Recipe/p232_Recipe.md) | 合成卷轴｜Recipe（合成卷轴） |

## 原图复核（2026-10-22/23，follow-up 057、066）

- 人物卡除 c5–c9、c24、c40、m1、m4、m102–m104（此前已按原图做过或用户定稿）与 m300–m309（商人，另案）外，161 张都下载了 DotA 1 / WC3 原图到各卡 `ref/model/`，`refs.md` 记来源、所见与差异等级。
- **差异大、已按原图改卡并重出立绘 146 张**（Codex 内置出图为主，follow-up 066；代理逐张看图通过，待用户看；旧图留 `_vN.png`）。含原本待截图的 c19、c27、c37、c93、c105、m200，以及有建立视频的 c65、m2、m3、m5、m6。
- **差异小、保留原图 13 张**：c17、c79、c82、c106、c107、m9、m10、m11、m19、m24、m112、m201、m210。
- **原图不足、未定 2 张**：m130 灵能陷阱、m202 幽冥守卫（需 6.83d 实机截图或地图模型路径）。
- **视频**（用户 follow-up 066 点）：c65、m2、m3、m5、m6 建立视频按新立绘重出并抽三视图；斧王 demo 技能 k651–k654 正式条重出、剪成 `demo/edit/final/ep01_final_v7.mp4`（之后另一会话按 p30 斧头再出 v8，follow-up 073/076）。
- **技能卡**：106 位英雄的技能卡外观描述与其中出场的小兵 / 召唤物同步到新外观；已有峰值图 107 张按新外观重出（Codex），没有峰值图的卡不新出。各卡均无「技能视频 prompt」节的（除 c40、c65）暂不出资料包。武器道具参考由 follow-up 075 另行加入。

## 出图状态（2026-10-18）

- 立绘 / 锚点图已出并逐张看图通过：英雄 107、小兵与野怪 26、召唤物 34、背景 14、道具 28（共 209 张；记录在各卡「生成记录」）。
- ~~**暂缓出图**~~（2026-10-22 已补原图、改卡，c93 已出图，其余随上节待出）：**暂缓出图（外观未取证，地图导入自制模型或骑乘未定，需先截图）**：c19 军团指挥官、c27 幻影长矛手、c37 赏金猎人、c93 谜团、c105 远古冰魄，以及 m200 精神体（随 c93）。
- **未做（视频由用户点）**：每人 4 秒建立视频 → 正侧背三视图 + 声样。turntable prompt 已写进各卡。

## 建筑三视图（2026-10-22，follow-up 064）

22 类建筑／固定设施已分别保存正面、右侧面、背面，共 66 张单图及 22 张合图；主代理看图初审完成，22 张合图已通过 ccconnect 发送，待用户确认。原 28 张来源锚点的 SHA256 均未改变。

| 建筑类型 | 正／右侧／背合图 |
|---|---|
| bg2_近卫基地·世界之树 | [查看](background/近卫_sentinel/bg2_近卫基地·世界之树/views/bg2_近卫基地·世界之树_views.png) |
| bg3_天灾基地·冰封王座 | [查看](background/天灾_scourge/bg3_天灾基地·冰封王座/views/bg3_天灾基地·冰封王座_views.png) |
| bg12_边路地精商店 | [查看](background/中立_neutral/bg12_边路地精商店/views/bg12_边路地精商店_views.png) |
| bg15_近卫泉水 | [查看](background/近卫_sentinel/bg15_近卫泉水/views/bg15_近卫泉水_views.png) |
| bg16_近卫防御塔 | [查看](background/近卫_sentinel/bg16_近卫防御塔/views/bg16_近卫防御塔_views.png) |
| bg17_战争古树 | [查看](background/近卫_sentinel/bg17_战争古树/views/bg17_战争古树_views.png) |
| bg18_知识古树 | [查看](background/近卫_sentinel/bg18_知识古树/views/bg18_知识古树_views.png) |
| bg19_月亮井 | [查看](background/近卫_sentinel/bg19_月亮井/views/bg19_月亮井_views.png) |
| bg20_风之古树 | [查看](background/近卫_sentinel/bg20_风之古树/views/bg20_风之古树_views.png) |
| bg21_猎手大厅 | [查看](background/近卫_sentinel/bg21_猎手大厅/views/bg21_猎手大厅_views.png) |
| bg22_奇迹古树 | [查看](background/近卫_sentinel/bg22_奇迹古树/views/bg22_奇迹古树_views.png) |
| bg23_奎尔瑟兰的密室 | [查看](background/近卫_sentinel/bg23_奎尔瑟兰的密室/views/bg23_奎尔瑟兰的密室_views.png) |
| bg25_天灾泉水 | [查看](background/天灾_scourge/bg25_天灾泉水/views/bg25_天灾泉水_views.png) |
| bg26_天灾防御塔 | [查看](background/天灾_scourge/bg26_天灾防御塔/views/bg26_天灾防御塔_views.png) |
| bg27_地穴 | [查看](background/天灾_scourge/bg27_地穴/views/bg27_地穴_views.png) |
| bg28_诅咒神庙 | [查看](background/天灾_scourge/bg28_诅咒神庙/views/bg28_诅咒神庙_views.png) |
| bg29_通灵塔 | [查看](background/天灾_scourge/bg29_通灵塔/views/bg29_通灵塔_views.png) |
| bg30_埋骨地 | [查看](background/天灾_scourge/bg30_埋骨地/views/bg30_埋骨地_views.png) |
| bg31_牺牲深渊 | [查看](background/天灾_scourge/bg31_牺牲深渊/views/bg31_牺牲深渊_views.png) |
| bg32_崩碎之穴 | [查看](background/天灾_scourge/bg32_崩碎之穴/views/bg32_崩碎之穴_views.png) |
| bg33_恶魔遗物 | [查看](background/天灾_scourge/bg33_恶魔遗物/views/bg33_恶魔遗物_views.png) |
| bg36_地精实验室 | [查看](background/中立_neutral/bg36_地精实验室/views/bg36_地精实验室_views.png) |

组合关系：bg2 的世界之树、bg16 防御塔、bg19 月井；bg3 的冰封王座、bg26 防御塔、bg30 埋骨地；bg13 复用 bg15／bg22／bg23，bg14 复用 bg25／bg32／bg33。bg12 的双茅屋连接在同一平台上，按一套固定结构制图。bg11、bg24、bg34、bg35 是空地或营地景观，不额外编造实体商店。

未知背面按本剧美术设计补全，非原版已考据结构；本轮为影视美术参考，未经独立终审或用户确认。每卡 `views/*_views.json` 存完整指纹与审查状态；旧失败候选保留，正式引用使用不带 `_candidate` 的文件。


## 固定武器与人物重出（follow-up 075）

更新时间：2026-10-23T01:10:57+08:00。共 93 名有外置武器的角色、92 套武器（含 p29/p30 复用，m131 与 c39 共用）。先武器看图，再重出人物；主代理初审不等于独立终审或用户定稿。旧图备份为 `_before_weapon_reference_075.png`；未通过候选不作为新的正式参考。详细状态及失败原因见 [武器清单](characters/weapon_assets.json)。

浏览：[武器与人物对照总览](weapon_reference_gallery.html)（可搜索编号、筛选未完成项，点击图片看原尺寸）；[总览 1](reference_review_075/contact_01.jpg)、[总览 2](reference_review_075/contact_02.jpg)、[总览 3](reference_review_075/contact_03.jpg)、[总览 4](reference_review_075/contact_04.jpg)。总览只供查看，不代替生成时分别挂人物原图和武器原图。

本轮未重生已有建立视频、三视图和技能峰值图，不能视为它们已随新武器验收；现存衍生产物路径记录在 `.audit/adhoc_agents/2026-10-22/dota-weapons/downstream_inventory.json`。未来生成仍分别附当前人物原图与独立武器原图；技能视频资料包已更新引用。

| 人物 | 武器图 | 武器状态 | 人物图状态 |
|---|---|---|---|
| c3 | [p31](props/近卫_sentinel/p31_c3_Omniknight_Weapons/p31_c3_Omniknight_Weapons.png) | 初审通过 | 初审通过 |
| c4 | [p32](props/近卫_sentinel/p32_c4_Centaur_Warchief_Weapons/p32_c4_Centaur_Warchief_Weapons.png) | 初审通过 | 初审通过 |
| c5 | [p33](props/近卫_sentinel/p33_c5_Earthshaker_Weapons/p33_c5_Earthshaker_Weapons.png) | 初审通过 | 初审通过 |
| c6 | [p34](props/近卫_sentinel/p34_c6_Beastmaster_Weapons/p34_c6_Beastmaster_Weapons.png) | 初审通过 | 初审通过 |
| c7 | [p35](props/近卫_sentinel/p35_c7_Admiral_Weapons/p35_c7_Admiral_Weapons.md) | 失败或未知，不自动重提 | 待武器通过后重出 |
| c8 | [p36](props/近卫_sentinel/p36_c8_Rogue_Knight_Weapons/p36_c8_Rogue_Knight_Weapons.png) | 初审通过 | 初审通过 |
| c9 | [p37](props/近卫_sentinel/p37_c9_Pandaren_Brewmaster_Weapons/p37_c9_Pandaren_Brewmaster_Weapons.png) | 初审通过 | 初审通过 |
| c10 | [p38](props/近卫_sentinel/p38_c10_Tauren_Chieftain_Weapons/p38_c10_Tauren_Chieftain_Weapons.png) | 初审通过 | 初审通过 |
| c11 | [p39](props/近卫_sentinel/p39_c11_Alchemist_Weapons/p39_c11_Alchemist_Weapons.png) | 初审通过 | 初审通过 |
| c13 | [p40](props/近卫_sentinel/p40_c13_Dragon_Knight_Weapons/p40_c13_Dragon_Knight_Weapons.png) | 初审通过 | 初审通过 |
| c14 | [p41](props/近卫_sentinel/p41_c14_Sacred_Warrior_Weapons/p41_c14_Sacred_Warrior_Weapons.md) | 失败或未知，不自动重提 | 待武器通过后重出 |
| c16 | [p42](props/近卫_sentinel/p42_c16_Tuskarr_Weapons/p42_c16_Tuskarr_Weapons.png) | 初审通过 | 初审通过 |
| c18 | [p43](props/近卫_sentinel/p43_c18_Bristleback_Weapons/p43_c18_Bristleback_Weapons.png) | 初审通过 | 初审通过 |
| c19 | [p44](props/近卫_sentinel/p44_c19_Legion_Commander_Weapons/p44_c19_Legion_Commander_Weapons.md) | 失败或未知，不自动重提 | 待武器通过后重出 |
| c22 | [p45](props/近卫_sentinel/p45_c22_Priestess_of_the_Moon_Weapons/p45_c22_Priestess_of_the_Moon_Weapons.png) | 初审通过 | 初审通过 |
| c23 | [p46](props/近卫_sentinel/p46_c23_Moon_Rider_Weapons/p46_c23_Moon_Rider_Weapons.png) | 初审通过 | 初审通过 |
| c24 | [p29](props/近卫_sentinel/p29_Anti_Mage_Glaive/p29_Anti_Mage_Glaive.png) | 现有图保留；061窄刃修改先前被拒，未冒充完成 | 待武器通过后重出 |
| c25 | [p47](props/近卫_sentinel/p47_c25_Lone_Druid_Weapons/p47_c25_Lone_Druid_Weapons.png) | 初审通过 | 初审通过 |
| c26 | [p48](props/近卫_sentinel/p48_c26_Juggernaut_Weapons/p48_c26_Juggernaut_Weapons.png) | 初审通过 | 初审通过 |
| c27 | [p49](props/近卫_sentinel/p49_c27_Phantom_Lancer_Weapons/p49_c27_Phantom_Lancer_Weapons.png) | 初审通过 | 初审通过 |
| c28 | [p50](props/近卫_sentinel/p50_c28_Troll_Warlord_Weapons/p50_c28_Troll_Warlord_Weapons.png) | 初审通过 | 初审通过 |
| c29 | [p51](props/近卫_sentinel/p51_c29_Stealth_Assassin_Weapons/p51_c29_Stealth_Assassin_Weapons.png) | 初审通过 | 初审通过 |
| c30 | [p52](props/近卫_sentinel/p52_c30_Naga_Siren_Weapons/p52_c30_Naga_Siren_Weapons.png) | 初审通过 | 初审通过 |
| c32 | [p53](props/近卫_sentinel/p53_c32_Dwarven_Sniper_Weapons/p53_c32_Dwarven_Sniper_Weapons.png) | 初审通过 | 初审通过 |
| c35 | [p54](props/近卫_sentinel/p54_c35_Templar_Assassin_Weapons/p54_c35_Templar_Assassin_Weapons.md) | 失败或未知，不自动重提 | 待武器通过后重出 |
| c36 | [p55](props/近卫_sentinel/p55_c36_Drow_Ranger_Weapons/p55_c36_Drow_Ranger_Weapons.md) | 失败或未知，不自动重提 | 待武器通过后重出 |
| c37 | [p56](props/近卫_sentinel/p56_c37_Bounty_Hunter_Weapons/p56_c37_Bounty_Hunter_Weapons.png) | 初审通过 | 初审通过 |
| c38 | [p57](props/近卫_sentinel/p57_c38_Vengeful_Spirit_Weapons/p57_c38_Vengeful_Spirit_Weapons.png) | 初审通过 | 初审通过 |
| c39 | [p58](props/近卫_sentinel/p58_c39_Ember_Spirit_Weapons/p58_c39_Ember_Spirit_Weapons.md) | 失败或未知，不自动重提 | 待武器通过后重出 |
| c40 | [p59](props/近卫_sentinel/p59_c40_Lord_of_Olympus_Weapons/p59_c40_Lord_of_Olympus_Weapons.png) | 初审通过 | 初审通过 |
| c41 | [p60](props/近卫_sentinel/p60_c41_Crystal_Maiden_Weapons/p60_c41_Crystal_Maiden_Weapons.png) | 初审通过 | 初审通过 |
| c43 | [p61](props/近卫_sentinel/p61_c43_Keeper_of_the_Light_Weapons/p61_c43_Keeper_of_the_Light_Weapons.png) | 初审通过 | 初审通过 |
| c45 | [p62](props/近卫_sentinel/p62_c45_Windrunner_Weapons/p62_c45_Windrunner_Weapons.png) | 初审通过 | 初审通过 |
| c46 | [p63](props/近卫_sentinel/p63_c46_Holy_Knight_Weapons/p63_c46_Holy_Knight_Weapons.png) | 初审通过 | 初审通过 |
| c47 | [p64](props/近卫_sentinel/p64_c47_Enchantress_Weapons/p64_c47_Enchantress_Weapons.png) | 初审通过 | 初审通过 |
| c48 | [p65](props/近卫_sentinel/p65_c48_Prophet_Weapons/p65_c48_Prophet_Weapons.png) | 初审通过 | 初审通过 |
| c50 | [p66](props/近卫_sentinel/p66_c50_Silencer_Weapons/p66_c50_Silencer_Weapons.png) | 初审通过 | 初审通过 |
| c51 | [p67](props/近卫_sentinel/p67_c51_Disruptor_Weapons/p67_c51_Disruptor_Weapons.png) | 初审通过 | 初审通过 |
| c53 | [p68](props/近卫_sentinel/p68_c53_Goblin_Techies_Weapons/p68_c53_Goblin_Techies_Weapons.png) | 初审通过 | 初审通过 |
| c54 | [p69](props/近卫_sentinel/p69_c54_Ogre_Magi_Weapons/p69_c54_Ogre_Magi_Weapons.png) | 初审通过 | 初审通过 |
| c56 | [p70](props/近卫_sentinel/p70_c56_Shadow_Shaman_Weapons/p70_c56_Shadow_Shaman_Weapons.png) | 初审通过 | 初审通过 |
| c57 | [p71](props/近卫_sentinel/p71_c57_Grand_Magus_Weapons/p71_c57_Grand_Magus_Weapons.png) | 初审通过 | 初审通过 |
| c58 | [p72](props/近卫_sentinel/p72_c58_Skywrath_Mage_Weapons/p72_c58_Skywrath_Mage_Weapons.md) | 失败或未知，不自动重提 | 待武器通过后重出 |
| c59 | [p73](props/近卫_sentinel/p73_c59_Oracle_Weapons/p73_c59_Oracle_Weapons.png) | 初审通过 | 初审通过 |
| c60 | [p74](props/天灾_scourge/p74_c60_Chaos_Knight_Weapons/p74_c60_Chaos_Knight_Weapons.png) | 初审通过 | 初审通过 |
| c62 | [p75](props/天灾_scourge/p75_c62_Skeleton_King_Weapons/p75_c62_Skeleton_King_Weapons.png) | 初审通过 | 初审通过 |
| c63 | [p76](props/天灾_scourge/p76_c63_Lord_of_Avernus_Weapons/p76_c63_Lord_of_Avernus_Weapons.md) | 失败或未知，不自动重提 | 待武器通过后重出 |
| c64 | [p77](props/天灾_scourge/p77_c64_Slithereen_Guard_Weapons/p77_c64_Slithereen_Guard_Weapons.png) | 初审通过 | 初审通过 |
| c65 | [p30](props/天灾_scourge/p30_Axe_Great_Axe/p30_Axe_Great_Axe.png) | 初审通过 | 初审通过 |
| c66 | [p78](props/天灾_scourge/p78_c66_Pit_Lord_Weapons/p78_c66_Pit_Lord_Weapons.png) | 初审通过 | 初审通过 |
| c68 | [p79](props/天灾_scourge/p79_c68_Butcher_Weapons/p79_c68_Butcher_Weapons.png) | 初审通过 | 初审通过 |
| c71 | [p80](props/天灾_scourge/p80_c71_Doom_Bringer_Weapons/p80_c71_Doom_Bringer_Weapons.png) | 初审通过 | 初审通过 |
| c72 | [p81](props/天灾_scourge/p81_c72_Magnataur_Weapons/p81_c72_Magnataur_Weapons.png) | 初审通过 | 初审通过 |
| c73 | [p82](props/天灾_scourge/p82_c73_Spiritbreaker_Weapons/p82_c73_Spiritbreaker_Weapons.png) | 初审通过 | 初审通过 |
| c74 | [p83](props/天灾_scourge/p83_c74_Tidehunter_Weapons/p83_c74_Tidehunter_Weapons.png) | 初审通过 | 初审通过 |
| c77 | [p84](props/天灾_scourge/p84_c77_Bloodseeker_Weapons/p84_c77_Bloodseeker_Weapons.png) | 初审通过 | 初审通过 |
| c78 | [p85](props/天灾_scourge/p85_c78_Spectre_Weapons/p85_c78_Spectre_Weapons.png) | 初审通过 | 初审通过 |
| c80 | [p86](props/天灾_scourge/p86_c80_Phantom_Assassin_Weapons/p86_c80_Phantom_Assassin_Weapons.png) | 初审通过 | 初审通过 |
| c82 | [p87](props/天灾_scourge/p87_c82_Bone_Fletcher_Weapons/p87_c82_Bone_Fletcher_Weapons.png) | 初审通过 | 初审通过 |
| c85 | [p88](props/天灾_scourge/p88_c85_Soul_Keeper_Weapons/p88_c85_Soul_Keeper_Weapons.png) | 初审通过 | 初审通过 |
| c87 | [p89](props/天灾_scourge/p89_c87_Geomancer_Weapons/p89_c87_Geomancer_Weapons.md) | 失败或未知，不自动重提 | 待武器通过后重出 |
| c88 | [p90](props/天灾_scourge/p90_c88_Murloc_Nightcrawler_Weapons/p90_c88_Murloc_Nightcrawler_Weapons.png) | 初审通过 | 初审通过 |
| c89 | [p91](props/天灾_scourge/p91_c89_Gorgon_Weapons/p91_c89_Gorgon_Weapons.png) | 初审通过 | 初审通过 |
| c90 | [p92](props/天灾_scourge/p92_c90_Faceless_Void_Weapons/p92_c90_Faceless_Void_Weapons.md) | 失败或未知，不自动重提 | 待武器通过后重出 |
| c91 | [p93](props/天灾_scourge/p93_c91_Lightning_Revenant_Weapons/p93_c91_Lightning_Revenant_Weapons.png) | 初审通过 | 初审通过 |
| c92 | [p94](props/天灾_scourge/p94_c92_Arc_Warden_Weapons/p94_c92_Arc_Warden_Weapons.png) | 初审通过 | 初审通过 |
| c96 | [p96](props/天灾_scourge/p96_c96_Demon_Witch_Weapons/p96_c96_Demon_Witch_Weapons.md) | 失败或未知，不自动重提 | 待武器通过后重出 |
| c97 | [p97](props/天灾_scourge/p97_c97_Queen_of_Pain_Weapons/p97_c97_Queen_of_Pain_Weapons.md) | 失败或未知，不自动重提 | 待武器通过后重出 |
| c99 | [p98](props/天灾_scourge/p98_c99_Necrolyte_Weapons/p98_c99_Necrolyte_Weapons.png) | 初审通过 | 初审通过 |
| c100 | [p99](props/天灾_scourge/p99_c100_Dark_Seer_Weapons/p99_c100_Dark_Seer_Weapons.png) | 初审通过 | 初审通过 |
| c101 | [p100](props/天灾_scourge/p100_c101_Obsidian_Destroyer_Weapons/p100_c101_Obsidian_Destroyer_Weapons.png) | 初审通过 | 初审通过 |
| c103 | [p101](props/天灾_scourge/p101_c103_Warlock_Weapons/p101_c103_Warlock_Weapons.png) | 初审通过 | 初审通过 |
| c108 | [p102](props/天灾_scourge/p102_c108_Witch_Doctor_Weapons/p102_c108_Witch_Doctor_Weapons.png) | 初审通过 | 初审通过 |
| c109 | [p103](props/天灾_scourge/p103_c109_Shadow_Priest_Weapons/p103_c109_Shadow_Priest_Weapons.png) | 初审通过 | 初审通过 |
| c111 | [p104](props/天灾_scourge/p104_c111_Batrider_Weapons/p104_c111_Batrider_Weapons.png) | 初审通过 | 初审通过 |
| m2 | [p105](props/近卫_sentinel/p105_m2_Druid_of_the_Talon_Weapons/p105_m2_Druid_of_the_Talon_Weapons.png) | 初审通过 | 初审通过 |
| m5 | [p106](props/天灾_scourge/p106_m5_Necromancer_Weapons/p106_m5_Necromancer_Weapons.png) | 初审通过 | 初审通过 |
| m8 | [p107](props/中立_neutral/p107_m8_Kobold_Weapons/p107_m8_Kobold_Weapons.png) | 初审通过 | 初审通过 |
| m9 | [p108](props/中立_neutral/p108_m9_Forest_Troll_Weapons/p108_m9_Forest_Troll_Weapons.png) | 初审通过 | 初审通过 |
| m10 | [p109](props/中立_neutral/p109_m10_Gnoll_Assassin_Weapons/p109_m10_Gnoll_Assassin_Weapons.png) | 初审通过 | 初审通过 |
| m16 | [p110](props/中立_neutral/p110_m16_Ogre_Weapons/p110_m16_Ogre_Weapons.md) | 失败或未知，不自动重提 | 待武器通过后重出 |
| m17 | [p111](props/中立_neutral/p111_m17_Satyr_Weapons/p111_m17_Satyr_Weapons.png) | 初审通过 | 初审通过 |
| m18 | [p112](props/中立_neutral/p112_m18_Centaur_Weapons/p112_m18_Centaur_Weapons.png) | 初审通过 | 初审通过 |
| m19 | [p113](props/中立_neutral/p113_m19_Dark_Troll_Weapons/p113_m19_Dark_Troll_Weapons.png) | 初审通过 | 初审通过 |
| m23 | [p114](props/中立_neutral/p114_m23_Dragonspawn_Weapons/p114_m23_Dragonspawn_Weapons.png) | 初审通过 | 初审通过 |
| m102 | [p115](props/近卫_sentinel/p115_m102_Earth_Panda_Weapons/p115_m102_Earth_Panda_Weapons.png) | 初审通过 | 初审通过 |
| m104 | [p116](props/近卫_sentinel/p116_m104_Fire_Panda_Weapons/p116_m104_Fire_Panda_Weapons.png) | 初审通过 | 初审通过 |
| m131 | [p58](props/近卫_sentinel/p58_c39_Ember_Spirit_Weapons/p58_c39_Ember_Spirit_Weapons.md) | 失败或未知，不自动重提 | 待武器通过后重出 |
| m300 | [p117](props/中立_neutral/p117_m300_Weapons_Dealer_Weapons/p117_m300_Weapons_Dealer_Weapons.png) | 初审通过 | 初审通过 |
| m302 | [p118](props/中立_neutral/p118_m302_Supportive_Vestments_Weapons/p118_m302_Supportive_Vestments_Weapons.png) | 初审通过 | 初审通过 |
| m304 | [p119](props/中立_neutral/p119_m304_Arcane_Sanctum_Weapons/p119_m304_Arcane_Sanctum_Weapons.png) | 初审通过 | 初审通过 |
| m305 | [p120](props/中立_neutral/p120_m305_Ancient_Weaponry_Weapons/p120_m305_Ancient_Weaponry_Weapons.png) | 初审通过 | 初审通过 |
| m307 | [p121](props/中立_neutral/p121_m307_Protectorate_Weapons/p121_m307_Protectorate_Weapons.png) | 初审通过 | 初审通过 |

## Luna 五条视频（2026-10-23，follow-up 078）

16:9、720p，已按 Axe 的亮相＋四技能组合生成并通过 ccconnect 发出 ZIP 原片；待用户看与试听。

| 视频 | 时长 | 当前文件 |
|---|---|---|
| 角色亮相 | 10.05 秒 | [MP4](characters/近卫_sentinel/c23_Moon_Rider/c23_Moon_Rider_turntable.mp4) |
| 月光 | 10.08 秒 | [MP4](characters/近卫_sentinel/c23_Moon_Rider/skills/k231_Lucent_Beam/renders/20261023-083107_184ea4ef/k231_Lucent_Beam_clip.mp4) |
| 月刃 | 10.08 秒 | [MP4](characters/近卫_sentinel/c23_Moon_Rider/skills/k232_Moon_Glaive/renders/20261023-082418_273ef911/k232_Moon_Glaive_clip.mp4) |
| 月之祝福 | 10.05 秒 | [MP4](characters/近卫_sentinel/c23_Moon_Rider/skills/k233_Lunar_Blessing/renders/20261023-082456_5a154d00/k233_Lunar_Blessing_clip.mp4) |
| 月蚀 | 12.06 秒 | [MP4](characters/近卫_sentinel/c23_Moon_Rider/skills/k234_Eclipse/renders/20261023-083524_a1eaaeb2/k234_Eclipse_clip.mp4) |

月光和月蚀各修正一次，首版保留。视觉偏差与音轨未试听边界见各卡本轮视频记录；此处不代表用户批准或独立终审。


## CM人物及四技能（2026-10-23 · follow-up 082）

[c41本轮素材与交付](characters/近卫_sentinel/c41_Crystal_Maiden/README.md)：人物图和法杖复用，亮相/三视图/合图/声样及四技能峰值图与视频已补齐并发送；附69秒初接预览。首轮候选存在数量与光效偏差，声音未人工核听，无独立终审，未锁片。


## 两方基地坐标与素材对照（2026-10-23，follow-up 096 / 099）

[打开参考总览](http://127.0.0.1:8766/base-layout?path=ai_videos%2Fdota_yingxiong%2F0_research%2Fbase_layout_refs%2Fbase_layout_manifest.json) · [近卫建筑坐标图](../0_research/base_layout_refs/sentinel_asset_layout.png) · [天灾建筑坐标图](../0_research/base_layout_refs/scourge_asset_layout.png) · [坐标与资产清单](../0_research/base_layout_refs/base_layout_manifest.json)。

按重新下载的原版 6.83d 脚本逐行核对：两方各 30 座建筑，共 60 座映射 21 类基地建筑资产；两座天灾四级塔已登记 `bg37#01/#02`，共用新增 bg37 主图，主图与正面图已出，侧/背面网络失败待补。16 位商人映射 m300–m307，10 个出生圈另列。`bg19#01` 等是场内实例号，不是资产变体。

总览含数字版、资产号版、泉水区放大图、10 张重点游戏参考（新增 2 张、复用 8 张）与已有三视图入口。bg38/bg39 搭景方案与电影概念候选见下方；原地图高程已提取，装饰、精模占地/高度与电影尺度仍待校准。既有素材用户确认状态不变。


## 两座完整基地搭景（follow-up 106）

新增 bg38 近卫基地全景、bg39 天灾基地全景。各自 `planning/blocks.toml` 保存30座建筑占位及三组机位；米制工作比例12游戏单位/米、占地和高度均为电影候选。保留全部原始点位和270度脚本角，不把它当成已确认的模型视觉正面。各有平面图、43行CSV/JSON摆放表、Blender技术体块文件及俯视/整体/遗迹/泉水区四张取景检查图。管理站点基地布局页的「搭景方案」中可看、下载。体块使用原版顶点高度场：泉水商店区高出主基地128游戏单位，按暂定比例约10.67米。体块不是建筑精模，悬崖/坡道模型和装饰未重建；美术概念不保证逐实例坐标准确。

两基地电影概念候选均已生成并由主代理看图，见管理页搭景方案；bg38第三次请求成功，bg39首次成功。未作独立终审，未获用户确认，不保证生成画面的30个实例精确落位。


## Tiny 五条720p审阅（2026-10-24，follow-up101/104）

[亮相与四技能](characters/近卫_sentinel/c2_Stone_Giant/demo/review_20261024/README.md) · [ZIP](characters/近卫_sentinel/c2_Stone_Giant/demo/Tiny_5_videos_720p_review_20261024.zip)。五条原片约10/10/10/10/12秒；新增三视图与2.1秒岩石声样，m4三视图按真实侧/背重选。16份新增公开参考SHA已核验；长大有已知blocker，其他四条可带瑕疵review，声音待试听；修正版提交超时不重提。


## 整图区域层级（follow-up 115）

`0_research/map_regions/map_regions.json` 管理8个大区、16个拍摄区及四机位槽位。区域编号 S/D/T/M/B/J/K/R 与 bg 资产编号分开；资产只引用、不复制。追加 `bg40_上路林缘走廊`、`bg41_下路林缘走廊`（中立）；已有 bg13/bg14 为泉水、出生点和商店组合区，bg15/bg25 继续是泉水单体。

## vlog 系列新增资产（2026-11-02，follow-up 325）

vlog「冰女旅行」第一段（穿越，`episodes/ep01/`）用到的新资产；设定见 `vlog/`。

| 键 | 名称 | 目录 | 状态 |
|---|---|---|---|
| `c113` | 旅行者（冰女现代装） | `characters/近卫_sentinel/c113_Traveler/` | 立绘（用户认可）、三视图合图、声样暂用 c41 |
| `m310` | 德鲁伊医者 | `characters/近卫_sentinel/m310_Druid_Healer/` | 立绘、三视图合图、4 秒建立视频与声样（取自视频对白） |
| `bg42` | 北极冰洞遗迹 | `background/中立_neutral/bg42_北极冰洞/` | 场景图（用户认可） |
| `bg43` | 圣泉湖广场 | `background/近卫_sentinel/bg43_圣泉湖广场/` | 场景图（用户认可） |
| `bg44` | 冰女小树屋 | `background/近卫_sentinel/bg44_冰女小树屋/` | 场景图（待用户看） |
| `p233` | 传送法器 | `props/近卫_sentinel/p233_传送法器/` | 锚点图（球形环架，晶石暗） |
| `p234` | 冰霜法典 | `props/近卫_sentinel/p234_冰霜法典/` | 锚点图（裁自道具图，用户认可） |
