---
worker_id: w01-dnd-pathfinder
stage: research
role: researcher
angle: dnd-pathfinder
status: complete
blockers: []
confidence: medium
---

# D&D 5e（2014/2024）+ Pathfinder 2e 拆解

## 1. 概览

| 项 | 内容 |
|---|---|
| 作品/传统 | Dungeons & Dragons 第5版（Wizards of the Coast，WotC）；对照 Pathfinder Second Edition（Paizo，含 2023 起的 Remaster：Player Core / GM Core） |
| 版本范围 | D&D 5e 2014 PHB/DMG/MM + 2024 修订版（俗称 5.5e / 「2024 Core Rules」）；SRD 5.1（2016 发布，2023-01 放入 CC-BY-4.0）与 SRD 5.2（2025-04-22 发布，5.2.1 于 2025-05-01，CC-BY-4.0）[S1][S2] |
| 为何有用 | ① 欧美奇幻「通用语法」的事实标准：八大学派、法术环级、职业/子职、Great Wheel 位面、天使/魔鬼/恶魔层级几乎是所有西幻游戏和影视的共同参照；② SRD 是 CC-BY-4.0 开放内容，只需署名即可使用，IP 风险最低；③ 规则化程度高，能直接拿来当「境界表」「品阶表」 |
| 对我们的定位 | 西幻资料库的「骨架」：其他作品（WoW、指环王、巫师等）的概念多数可以映射回这里 |

**SRD 5.2 开放/不开放的边界**（官方页 [S1]）：
- 包含：按 2024 规则改写的核心规则；新增物种 Goliath、Orc；15 个专长、20 个法术、15 个魔法物品、17 个怪物等；部分物品改名以避开商标（*Deck of Many Things* → *Mysterious Deck*，*Orb of Dragonkind* → *Dragon Orb*）。
- 不含：Artificer 职业、Aasimar 物种、Beholder 等怪物、Strahd/Orcus/Tiamat 等具名角色、Half-Elf/Half-Orc（已删）、"The Planes of Existence" 位面章节、"Fantasy-Historical Pantheons" 神系。
- 署名要求：使用 SRD 内容必须按 CC-BY-4.0 署名（标准署名语见 SRD 文档首页）。[S1][S3]

> 本文标记约定：**[SRD]** = 词条出现在 SRD 5.1/5.2 开放内容中；**[通用]** = 早于 D&D 的神话/民俗/文学通用词（就算 WotC 用过也不专属）；**[专有]** = WotC 或 Paizo 的产品身份/专有 IP，只能借机制不能用名。未逐条核对 SRD 正文的标「未核实」。

## 2. 力量来源与魔法分类

### 2.1 D&D 5e 的力量来源（谁给的力量）

D&D 自 AD&D（1977）起把魔法分成 arcane（来自世界本身、靠学习/天赋操控）和 divine（来自神或外层位面）；设计师 Jeremy Crawford 表示这种划分主要关乎施法者动机而非机制差异；4e 曾加入 primal，2022 One D&D 试玩稿又引入「arcane/divine/primal 三法术表」，2023 撤回。2024 规则所有施法职业改为「准备法术」制。[S4]

| 来源方式 | 典型职业 | 原理 | 代价/限制 | 仙侠对应 |
|---|---|---|---|---|
| 学习（study） | Wizard [SRD]、Eldritch Knight、Arcane Trickster | 研读法术书，理解魔法公式 | 依赖法术书（丢书=失法），抄录法术耗时耗金 [S5] | 法修/符修，靠功法典籍；「功法被盗」= 丢法术书 |
| 神恩（divine grant） | Cleric [SRD]、Paladin [SRD] | 神或理念赐予；Cleric 侍奉神的领域（domain），Paladin 力量来自誓言本身 | 背誓则失力（Oathbreaker 概念）；神可收回恩宠 | 佛道「愿力/信仰之力」，佛门金身；Paladin ≈ 发大誓愿的护法 |
| 契约（pact） | Warlock [SRD] | 与超凡存在（patron）签约换力量 | 力量随时可被收回、条件不透明；法术位少但短休回复 [S5] | 魔道「与心魔/魔尊签约」、借邪神之力；最接近「出卖寿元/灵魂换修为」 |
| 血统（bloodline/innate） | Sorcerer [SRD] | 体内天生魔力（龙血、混沌、天界血等） | 不用学，但法术少；靠 Sorcery Points 灵活改法术 [S5] | 天生灵根/血脉觉醒（如凤凰血脉、龙族血脉） |
| 自然（primal/nature） | Druid [SRD]、Ranger [SRD] | 自然本身、旧信仰、元素 | 常有禁忌（传统上 Druid 不穿金属甲，未核实为 2024 规则） | 妖修/灵修、草木精怪、山野散修 |
| 艺术/言灵 | Bard [SRD] | 「创世之歌」余音，以表演施法 | 需表演、嗓子/乐器 | 音修（琴魔、箫仙） |
| 技艺/器 | Artificer [专有：非 SRD] | 把魔法注入工具 | 依赖装置 | 炼器师 |

### 2.2 八大魔法学派（Schools of Magic）

官方定义（2024 Free Rules）：学派「本身没有规则」，只供其他规则引用 [S5]。历史：AD&D 学派原名 abjuration, alteration, conjuration, divination, enchantment, illusion, invocation, necromancy；后来 invocation→evocation、alteration→transmutation [S4]。

| 学派 | 官方一句话 [S5] | 代表法术（环级）[S6] | 屏幕视觉建议（我方设计，非官方） | 仙侠对应 | 熟悉度 |
|---|---|---|---|---|---|
| Abjuration 防护 | Prevents or reverses harmful effects | Shield (1)、Counterspell (3)、Dispel Magic (3)、Banishment (4) | 半透明六角/符文护盾，蓝白冷光；被击中时出现裂纹 | 护体罡气、结界、禁制；Counterspell ≈ 破法/截法 | 高 |
| Conjuration 咒法/召唤 | Transports creatures or objects | Mage Hand (0)、Misty Step (2)、Teleport (7)、Gate (9)、Wish (9) | 紫色/星空漩涡、传送门边缘烧灼 | 召唤灵兽、缩地成寸、挪移阵法、开天门 | 高 |
| Divination 预言 | Reveals information | Detect Magic (1)、Scrying (5)、Foresight (9) | 眼睛符号、金色瞳孔、水晶球/水镜画面 | 天眼通、卜算、推衍天机 | 中高 |
| Enchantment 惑控 | Influences minds | Charm Person (1)、Hold Person (2)、Dominate Monster (8)、Power Word: Kill (9) | 粉紫螺旋、被控者眼中泛光、低语回声 | 摄魂术、迷魂大法、言出法随；Power Word ≈ 真言/敕令 | 高 |
| Evocation 塑能 | Channels energy to create effects that are often destructive | Fire Bolt (0)、Magic Missile (1)、Fireball (3)、Lightning Bolt (3)、Meteor Swarm (9)；2024 Divine Smite 也是 1 环塑能 [S5] | 火球、闪电、陨石；最「爽」的大场面 | 五行法术、掌心雷、天雷、陨星 | 高（最高） |
| Illusion 幻术 | Deceives the mind or senses | Minor Illusion (0)、Invisibility (2)、Mirror Image (2) | 画面像水波一样抖动、分身闪烁 | 幻阵、障眼法、分身术 | 高 |
| Necromancy 死灵 | Manipulates life and death | Animate Dead (3)、True Resurrection (9)；注意 2024 版 Cure Wounds 是「Level 1 Abjuration」[S5]（2014 为塑能，记忆未核实）——治疗不归死灵 | 绿/黑雾、骨骼、灵魂被抽出的白色丝线 | 鬼修、尸道、夺舍、起死回生 | 高 |
| Transmutation 变化 | Transforms creatures or objects | Polymorph (4)、Time Stop (9)、Shapechange (9) | 身体扭曲变形、石化纹理蔓延 | 七十二变、点石成金、时间法则 | 中高 |

代表法术列中，经 [S6][S5] 核实学派与环级的是：Fire Bolt、Mage Hand、Shield、Magic Missile、Fireball、Counterspell、Animate Dead、Wish、Meteor Swarm、Power Word: Kill、True Resurrection、Gate、Time Stop、Cure Wounds；其余（Dispel Magic、Banishment、Misty Step、Teleport、Detect Magic、Scrying、Foresight、Charm Person、Hold Person、Dominate Monster、Lightning Bolt、Minor Illusion、Invisibility、Mirror Image、Polymorph、Shapechange）为记忆，**未核实**。视觉列全部是我方设计建议。

**Pathfinder 2e 差异**：Remaster 已删除八大学派的机制（只保留在背景设定里）[S7]。

### 2.3 Pathfinder 2e 四大传统 × 四种本质（对照）

PF2 不按「谁给的力量」分，而按「魔法是什么做的」分：四种本质 essence（matter 物质、spirit 灵、mind 心智、life 生命），每个传统掌握两种 [S7]。

| 传统 | 本质 | 官方/百科定义 | 施法职业 [S7] | 仙侠对应 |
|---|---|---|---|---|
| Arcane | matter + mind | 「built on logic and rationality」[S8] | Wizard、Magus、arcane 血统 Sorcerer | 法修/阵修（推演、算理） |
| Divine | spirit + life | 来自神祇及外层位面 | Cleric、Champion、Oracle、天界/魔鬼血统 Sorcerer | 佛门/道门香火神道 |
| Occult | mind + spirit | 心智与灵魂的隐秘、异质之理 | Bard、Psychic、occult 血统 Sorcerer | 神识/元神修炼、魂修、巫蛊 |
| Primal | matter + life | 自然循环、元素、本能 | Druid、Kineticist、部分 Ranger、fey/元素/兽血 Sorcerer | 妖修、五行灵根、体修 |
| 混合 | — | — | Thaumaturge 可借四传统 | 杂家/散修 |

> 仙侠启发：PF2 的「本质」很像仙侠「精-气-神 + 形」体系，可以做成我们西幻世界的「四源」设定；但 PF2 这套具体组合是 Paizo 设计，属**机制借鉴**，词本身（arcane/divine/occult/primal）是 [通用] 英语词。

### 2.4 神圣 / 邪恶 / 死亡 / 暗影 / 元素力量一览

| 力量 | D&D 载体 | 代价/特征 | 视觉 | 仙侠对应 |
|---|---|---|---|---|
| Holy / Radiant | Cleric、Paladin、天使；radiant 伤害类型 [SRD] | 依赖信仰或誓言 | 金白光柱、光环、羽翼 | 佛光、浩然正气、雷法（正道克邪） |
| Necrotic | Necromancy、Undead、Shadowfell | 吞噬生命力；常需献祭 | 黑紫雾、干枯皮肤 | 尸气、阴煞、死气 |
| Fiendish / Infernal | Warlock (Fiend Patron)、devils、demons | 灵魂抵押、契约 | 红黑火焰、硫磺、角与锁链 | 魔气、血祭 |
| Fey | Archfey Patron、Feywild | 讲规矩（名字、承诺、交换），情绪化 | 花瓣、萤光、季节变色 | 狐仙/山精，讲因果 |
| Elemental | Druid、Sorcerer、Elemental Planes；acid/cold/fire/lightning/thunder 伤害 [SRD] | 元素失控 | 四元素粒子 | 五行（注意西方是四元素：气水火土） |
| Psionic / Aberrant | Aberrant Sorcery、Psi Warrior、Soulknife | 异界污染 | 脑波纹、紫色裂隙、触手 | 神识攻击、心魔 |
| Wild Magic | Wild Magic Sorcerer | 随机效果（掷骰表） | 不可控的彩色乱流 | 走火入魔 |

来源：[S4][S5][S7][S8]；伤害类型列表为记忆，[未核实]。

## 3. 等级 / 位阶 / 境界

### 3.1 角色等级 1–20 与四档 Tiers of Play

经验值与熟练加值来自官方 Basic Rules 2014 [S9]；四档文字为官方描述的意译 [S9]。

| Tier | 等级 | XP 门槛 | 熟练加值 | 官方描述（意译） | 本档标志能力 | 仙侠建议对应 |
|---|---|---|---|---|---|---|
| 1 | 1–4 | 0 / 300 / 900 / 2,700 | +2 | 「学徒冒险者」；威胁是本地农场与村庄 | 3 级选子职（2024 全部职业 3 级选子职 [S10]） | 炼气期（入门、定方向） |
| 2 | 5–10 | 6,500 → 64,000 | +3/+4 | 「崭露头角」；施法者得 3 环（Fireball、Lightning Bolt），武者多次攻击；威胁城市与王国 | 3 环法术、Extra Attack | 筑基期（质变：能打群战） |
| 3 | 11–16 | 85,000 → 195,000 | +4/+5 | 远超常人；6 环法术；威胁区域与大陆 | 6 环法术、Mystic Arcanum | 金丹 / 元婴（一方霸主） |
| 4 | 17–20 | 225,000 → 355,000 | +6 | 职业巅峰，成为英雄或恶棍原型；关乎世界乃至多元宇宙秩序 | 9 环法术（Wish、Time Stop）；19 级 Epic Boon | 化神 / 合体（触及法则） |
| 「20+」 | — | — | — | 2014 DMG：20 级后以 Epic Boons 作为奖励（未核实细则）；2024：Epic Boon 改为 19 级专长 [S10][S11] | — | 渡劫 / 大乘（半步飞升） |

### 3.2 法术环级 cantrip – 9th

| 环级 | 2014 称呼 | 2024 称呼 | 最早可施（全施法者） | 代表 | 仙侠对应 |
|---|---|---|---|---|---|
| 0 | cantrip | Level 0 / cantrip | 1 级，随意施放、不耗法术位 [S12] | Fire Bolt, Mage Hand | 小法术、基础术法 |
| 1–2 | 1st–2nd level | Level 1–2 | 1 / 3 级 | Magic Missile, Shield, Misty Step | 低阶符箓/法诀 |
| 3–5 | 3rd–5th | Level 3–5 | 5 / 7 / 9 级 | Fireball, Counterspell, Raise Dead (5) | 中阶神通 |
| 6–8 | 6th–8th | Level 6–8 | 11 / 13 / 15 级 | Disintegrate, Teleport, Dominate Monster | 大神通 |
| 9 | 9th | Level 9 | 17 级 | Wish, Time Stop, Meteor Swarm, Gate, True Resurrection | 天地法则级 / 禁咒 |

规则要点 [S5][S12]：施法消耗「该环级或更高」的法术位；用高环位施低环法术＝upcast（效果增强）；每回合只能耗 1 个法术位；长休恢复；Ritual 多花 10 分钟可不耗法术位。法术环级 ≠ 角色等级（要 17 级才能施 9 环）。

> 仙侠对照差异：仙侠「境界」是人本身的层级，「法术品阶」是另一条轴（如黄/玄/地/天阶功法）。D&D 正好也是两条轴：角色等级 ↔ 境界，法术环级 ↔ 功法/神通品阶。法术位 ≈ 「灵力/真元储量」被切成格子，长休 ≈ 打坐回元。

### 3.3 神格 divine rank 0–20（「飞升」对照）

来源：3.5 版 *Deities and Demigods*（2002）的 d20 SRD 节选，属 OGL 1.0a 开放内容，**不是** 5e SRD [S13][S14]。5e 本身没有沿用数值化神格（5e DMG 只有「greater/lesser deity、quasi-deity」等描述性分类，未核实）。

| 神格 | 名称 | 信徒规模 | 遥感 | 领域感知（portfolio sense） | 神国（divine realm） | 仙侠对应 |
|---|---|---|---|---|---|---|
| 0 | Quasi-deity（含 hero deity 英雄神） | 少量 | — | — | — | 地仙 / 散仙；刚飞升的人仙 |
| 1–5 | Demigod 半神 | 数百–数千 | 同时 2 处 | 感知涉及 1,000+ 人的事件 | 外层位面小块领域 | 天仙 / 真仙 |
| 6–10 | Lesser deity 次神 | 数千–数万 | 5 处 | 500+ 人事件 | 外层位面约 1 英里 | 金仙 |
| 11–15 | Intermediate deity 中等神 | 数十万 | 10 处 | 全部相关事件，可回溯（每级 1 周） | 10 英里，可重塑地形 | 太乙 / 大罗金仙 |
| 16–20 | Greater deity 强大神 | 数百万 | 20 处 | 过去与未来（每级 1 周） | 100 英里，可改重力、元素、时间特性 | 道祖 / 天尊 |
| 21+ | Overdeity 超神（论坛/资料提及） | — | — | — | — | 天道 / 鸿蒙 |

来源 [S13][S14][S15]。注：d20srd 原表把 lesser 标成 11–15，属笔误，正文与其他来源均为 6–10 [S15 摘要]。

> 核心差异：D&D 的神格**由信徒数量决定**（信仰即力量），仙侠飞升**靠自身修为**。D&D 凡人成神多靠吞神/夺取神职（portfolio）或被神提拔，而不是「渡劫」。对短剧是好钩子：「信者越多我越强」→ 主角做网红/传教，比纯打坐更有戏。

### 3.4 Pathfinder 2e 对照（只写差异）

| 项 | PF2 | 与 D&D 差异 |
|---|---|---|
| 等级 | 1–20，每级都有选择（ancestry feat / class feat / skill feat / general feat） | 成长颗粒度更细 |
| 法术等级 | Remaster 以 spell **rank** 取代 spell level，并删除学派；最高 10 阶，Wizard 的 10 阶位来自 archwizard's spellcraft 特性（一个特殊法术位）[S17 摘要] | 多一个 10 阶（≈「仙术」）；rank 的称呼更像仙侠「阶」 |
| 熟练度 | Untrained / Trained / Expert / Master / Legendary 五档（记忆，未核实原文） | 很像「入门/小成/大成/圆满/化境」，可直接借做技艺境界 |
| 神话 | *War of Immortals*（2024）Mythic 规则：施放 mythic spell 需消耗 Mythic Point；mythic ritual 需「mythic proficiency」；有 Mythic Destiny（如 Wildspell）[S16] | 类似「天命/气运点」+「证道路线」 |

## 4. 职业 / 角色路线

### 4.1 D&D 2024 十二职业 + 48 子职

一句话描述与 SRD 子职来自 2024 Free Rules [S10]；48 子职列表来自 [S18]。2024 规则所有职业 3 级选子职，19 级获得 Epic Boon 专长 [S10]。SRD 5.2 每职业只开放 1 个子职（下表加粗者），其余子职名为 WotC 书内内容——但多数子职名是普通英语短语，真正专有的是具体文本与少数专名（标 [专有]）。

| 职业（全部 [SRD]） | 力量源 | 定位 | 2024 子职（**粗体**=SRD 5.2 开放） | 仙侠对应 |
|---|---|---|---|---|
| Barbarian 野蛮人 | 原始怒火（Rage） | 近战坦克 | **Path of the Berserker**、Wild Heart、World Tree、Zealot | 体修、狂战（燃血秘法） |
| Bard 吟游诗人 | 音乐/言语魔法 | 辅助、控场、全能 | **College of Lore**、Dance、Glamour、Valor | 音修、琴师 |
| Cleric 牧师 | 神恩（Wisdom） | 治疗、增益、惩击 | **Life Domain**、Light、Trickery、War | 佛门/道门法师；Domain ≈ 所奉神职的「道」 |
| Druid 德鲁伊 | 自然（Wisdom） | 变形、元素、治疗 | **Circle of the Land**、Moon、Sea、Stars | 妖修/山野散修；Wild Shape ≈ 化形 |
| Fighter 战士 | 训练 | 全武器全护甲 | **Champion**、Battle Master、Eldritch Knight、Psi Warrior | 武修、剑客；Eldritch Knight ≈ 剑修兼法修 |
| Monk 武僧 | 内在能量（2024 称 Focus，旧 Ki） | 快速徒手 | **Warrior of the Open Hand**、Mercy、Shadow、Elements | 少林/武当内家，最直接的「真气」类比 |
| Paladin 圣武士 | 誓言（Oath，Charisma） | 神圣近战、光环 | **Oath of Devotion**、Glory、Ancients、Vengeance | 护法金刚、正道剑仙 |
| Ranger 游侠 | 武艺 + 自然魔法 | 远程、追踪 | **Hunter**、Beast Master、Fey Wanderer、Gloom Stalker | 猎妖人、御兽师 |
| Rogue 游荡者 | 技巧 | 潜行、Sneak Attack | **Thief**、Arcane Trickster、Assassin、Soulknife | 刺客、神偷 |
| Sorcerer 术士 | 血统/天赋（Charisma） | 爆发施法 | **Draconic Sorcery**、Aberrant、Clockwork、Wild Magic | 天生灵根/血脉 |
| Warlock 邪术师 | 契约（Charisma） | 短休回复的施法者 | **Fiend Patron**、Archfey、Celestial、Great Old One | 魔修/与魔签约；「借来的力量」 |
| Wizard 法师 | 学习（Intelligence） | 最大法术库 | **Evoker**、Abjurer、Diviner、Illusionist | 法修/阵修/符修，宗门学院派 |
| Artificer 奇械师 [专有，非 SRD] | 注魔工艺 | 制造、辅助 | （见 *Eberron* 等书） | 炼器师 |

### 4.2 四个「力量来源」最强的职业细节

| 职业 | 关键机制 [S10] | 力量从哪来、怎么丢 | 视觉/戏剧点 |
|---|---|---|---|
| Paladin | Lay on Hands：治疗池 = 5×圣武士等级，长休回复；**2024 Divine Smite 变成 1 环塑能法术**，Paladin 2 级始终准备、每长休可免费施一次；Channel Divinity 2–3 次；6 级 Aura of Protection 给队友加豁免（18 级扩到 30 尺）；Oath of Devotion 誓词：「Let your word be your promise」「Protect the weak and never fear to act」「Let your honorable deeds be an example」 | 力量来自对誓言（理念）的信念，不一定需要神；背誓 → Oathbreaker（2014 DMG 子职，未核实细节） | 剑身燃起金光、跪地起誓、光环罩住队友；「背誓失光」是天然的高潮/低谷 |
| Cleric | Domain 子职（Life/Light/Trickery/War）；Channel Divinity；高级 Divine Intervention（神亲自出手，未核实 2024 细则） | 神赐，神可收回 | 神像发光、圣徽、祈祷→天降光柱 |
| Warlock | Pact Magic：法术位全部同环，**短休也能回**；Eldritch Invocations（含 Pact of the Blade/Chain/Tome）；11–17 级 Mystic Arcanum：每长休各施一次 6–9 环；Fiend Patron 特性：Dark One's Blessing、Dark One's Own Luck、Fiendish Resilience、Hurl Through Hell | 契约方给予，可附带条件 | 契约书、血签名、眼睛变色、背后巨大阴影 |
| Sorcerer | Innate Sorcery（激活 1 分钟增强）；Font of Magic：Sorcery Points 与法术位互换；Metamagic（Quickened、Twinned、Subtle 等）；Draconic Sorcery：龙鳞护甲、14 级 Dragon Wings 飞行、18 级 Dragon Companion | 血统，无法被收回但难以控制 | 皮肤浮现鳞片、瞳孔竖起、长出龙翼 |
| Wizard | 法术书（初始 6 个 1 环，每级 +2）；Arcane Recovery 短休回法术位；18 级 Spell Mastery（1、2 环免位施放）；20 级 Signature Spells | 学来的，丢书即困 | 法术书悬浮翻页、符文从书页飞出 |

### 4.3 Pathfinder 2e 差异（只写多出来的）

AoN 当前列出 Common 26 职业 + Uncommon 2 + Rare 1 [S19]。D&D 没有、对我们有用的：

| PF2 职业 | 机制要点 | 仙侠对应 |
|---|---|---|
| Champion | 取代 Paladin，Cause + Tenets；Remaster 起不再绑定阵营，有 holy/unholy 两类 Cause（具体 Cause 名未核实） | 正魔两道的护法 |
| Oracle | 神秘（Mystery）赐力 + 诅咒（curse）伴随 | 天选之人但有天谴 |
| Witch | 由 Patron 通过 familiar（使魔）教法术 | 巫蛊、师父附身灵宠 |
| Psychic | 心灵力量，Conscious/Subconscious Mind | 神识修炼 |
| Kineticist | 与元素门户相连，直接操控元素（Elements） | 最接近「五行灵根」的西幻职业 |
| Magus | 法剑合一（Hybrid Studies） | 剑修 |
| Summoner | 与 Eidolon 灵魂绑定 | 本命灵兽/元神分身 |
| Thaumaturge | 用民俗法器（Implements）、可借四传统 | 道士捉鬼（桃木剑、八卦镜） |
| Alchemist | 炼金为核心职业（Research Fields） | 丹师 |
| Animist / Exemplar | 与灵（Apparitions）共生 / 身负神火的英雄（Ikons、Epithets） | 萨满 / 半神肉身成圣 |
| Necromancer、Runesmith、Commander、Guardian | 2025 起新增（Common 列表中） | 鬼修、符箓师、将帅、护卫 |

> 重要差异：PF2 有独立的 **Alchemist** 和 **Runesmith**，最接近仙侠的「丹师」「符师」——D&D 在这两点很弱（D&D 没有炼药职业，只有工具熟练）。

## 5. 种族

2024 规则把 race 改称 **species**；物种不再给属性加值，属性加值改由背景（background）给（总 +3）[S20]。2024 PHB 共 10 个物种：Aasimar、Dragonborn、Dwarf、Elf、Gnome、Goliath、Halfling、Human、Orc、Tiefling；Free Rules 只含 9 个（无 Aasimar），SRD 5.2 也明确不含 Aasimar [S1][S20]。Half-Elf、Half-Orc 在 2024 已删除 [S1]。

### 5.1 物种总表

| 物种 | IP | 体型/身高 | 寿命 [S20] | 起源与力量来源 [S20] | 内部亚种 | 典型职业（我方归纳） | 仙侠对应 |
|---|---|---|---|---|---|---|---|
| Human 人类 | [通用][SRD] | Medium 或 Small | 约 80 年（「多数物种」） | 遍布多元宇宙，最多样；Resourceful、Skillful、Versatile（额外专长） | 无 | 任意 | 人族（寿短、可塑性最强——同仙侠） |
| Elf 精灵 | [通用][SRD] | Medium 5–6 尺 | 约 750 年 | 由神创造，曾能变形，受 Feywild 影响；Fey Ancestry、Trance（冥想代替睡眠） | Drow（暗精灵）、High Elf、Wood Elf | Wizard、Ranger、Druid | 仙族/灵族（长生、近妖仙） |
| Dwarf 矮人 | [通用][SRD] | Medium 4–5 尺 | 约 350 年 | 锻造之神自大地中造出；与石与金属亲和；Darkvision 120 尺、Stonecunning | （2024 无亚种） | Fighter、Cleric | 「器族」：炼器宗门、地底国度 |
| Halfling 半身人 | [通用][SRD]（hobbit 为托尔金专有） | Small 2–3 尺 | 约 150 年 | 受生命与家园之神宠爱；Luck（重掷 1）、Brave | （2024 无亚种） | Rogue、Bard | 小人国、福运族（气运加身） |
| Gnome 侏儒 | [通用][SRD] | Small 3–4 尺 | 约 425 年 | 发明、幻术与地下生命之神所造；Gnomish Cunning | Forest Gnome（幻术、与动物交谈）、Rock Gnome（可造发条小装置） | Wizard (Illusionist)、Artificer | 机关术世家 |
| Dragonborn 龙裔 | [SRD]（词为 WotC 造，但已在 SRD 开放） | Medium 5–7 尺 | 未写 | 色龙/金属龙后裔；Breath Weapon、Draconic Ancestry（定伤害类型）、5 级 Draconic Flight | 按龙色分（红/蓝/金等） | Paladin、Sorcerer | 龙族后裔、半妖（龙血） |
| Tiefling 提夫林 | [SRD]（词为 TSR/WotC 造，已 SRD 开放） | Medium 或 Small | 未写 | 生于下层位面或魔裔；Fiendish Legacy 三选一 | Abyssal（毒抗）、Chthonic（死灵抗）、Infernal（火抗） | Warlock、Sorcerer | 魔族混血 / 魔种（被歧视的「魔裔」很适合做主角） |
| Aasimar 阿斯莫 | [专有：非 SRD 5.2] | — | — | 天界血统（2024 PHB 有，Celestial Revelation 展开光翼等，未核实细节） | — | Paladin、Cleric | 仙裔 / 神裔 |
| Goliath 歌利亚 | [SRD 5.2 新增]（名源自《圣经》巨人，通用） | Medium 7–8 尺 | 未写 | 巨人远裔；Giant Ancestry 六选一：Cloud/Fire/Frost/Hill/Stone/Storm；5 级 Large Form 变大 | 按巨人血统分 | Barbarian、Fighter | 巨灵族、夸父后裔 |
| Orc 兽人 | [通用][SRD 5.2 新增] | Medium 6–7 尺 | 未写 | 由其神所造，耐力与决心为神赐；Adrenaline Rush、Relentless Endurance（濒死保留 1 HP） | — | Barbarian、Fighter | 蛮族/妖族（2024 不再写成天生邪恶） |

**IP 注意**：Free Rules 文本中提到的造物神名 Corellon（精灵）、Gruumsh（兽人）、人类起源 Sigil 都是 WotC 专有名 [专有] [S20]；SRD 5.2 是否保留这些名字未核实——原创剧只用「精灵之神」「兽人之神」等泛称。Drow 一词出自民俗（苏格兰「trow」变体），但「黑暗精灵住地下、蛛后崇拜」的组合高度绑定 D&D（Lolth [专有]）。

### 5.2 各族社会结构（2014 PHB/通行设定；多为未核实的通行印象，仅供方向）

| 物种 | 社会 | 与他族关系 | 冲突钩子 |
|---|---|---|---|
| Elf | 长寿贵族式，重艺术与传统；Drow 为地下母系神权（专有设定） | 与矮人传统不和 | 「千年老精灵 vs 百年人类恋人」寿命差 |
| Dwarf | 氏族（clan）+ 山中要塞，重荣誉、记仇、祖先崇拜 | 与精灵、兽人不和 | 世仇、失落的祖地 |
| Halfling | 乡村社区，家庭至上 | 与人类友好 | 小人物大运气 |
| Gnome | 好奇、发明家社区 | 中立 | 发明失控 |
| Tiefling | 无本族国度，散居、受歧视 | 常被人类排斥 | 「天生魔裔要证明自己」 |
| Dragonborn | 氏族荣誉，曾为龙仆 | — | 与龙祖的关系 |
| Orc | 部落、力量与神的意志 | 历史上与矮人、精灵为敌 | 洗白与偏见 |

来源：[S20]；社会描述为通行设定印象，**未核实**（2024 PHB 刻意弱化了「整族文化」写法）。

### 5.3 Pathfinder 2e 差异

PF2 称 **ancestry**，通过 heritage 细分亚种，并有 Versatile Heritage：Remaster 起旧 Aasimar、Tiefling 合并为 **Nephilim** 一个通用血统下的不同 lineage（天界/魔界外层位面后裔）[S21 摘要][S22 摘要]——「同一血统、善恶两面」的结构很适合仙魔混血主角。PF2 中 Leshy（植物灵）、Goblin 等为常见可玩族（未核实具体条目）；Leshy ≈ 草木精怪化形。

## 6. 个人成长机制

| 机制 | D&D 规则载体 | 说明 | 仙侠对应 | 戏剧用法 |
|---|---|---|---|---|
| 经验升级 | XP 0→355,000（20 级）；或 milestone（剧情里程碑）升级 [S9] | 打怪、完成任务得经验 | 修为积累 | 「一战破境」= milestone 升级 |
| 子职选择 | 2024 所有职业 3 级选子职 [S10] | 定终身方向 | 选主修功法 / 拜入哪一脉 | 入门考核后分流 |
| 学徒/学习 | Wizard 抄录法术书，按每环耗时耗金 [S10][S23] | 知识是可交易、可偷的资产 | 师承、藏经阁 | 偷师、抢秘籍 |
| 誓言 | Paladin Oath（tenets） [S10] | 遵守誓词即得力，违背则失 | 发大誓愿、道心 | 被迫在誓言与亲情间二选一 |
| 神恩 | Cleric Domain、Divine Intervention（未核实细则） | 力量随神意 | 香火神道、受箓 | 神沉默时信徒崩溃 |
| 契约 | Warlock Patron [S10] | 对价交易，条件隐藏 | 魔道契约、心魔誓 | 契约代价在关键时刻揭晓 |
| 血统觉醒 | Sorcerer Bloodline；Dragonborn 5 级 Draconic Flight、Goliath 5 级 Large Form [S10][S20] | 体内力量随等级觉醒 | 血脉觉醒 | 濒死时血脉觉醒（经典爽点） |
| 专长 | Feats：Origin feat（1 级）、General、Fighting Style、Epic Boon（19 级+）[S10][S11] | 横向补能力 | 副修神通 | — |
| Epic Boon | 2024 PHB 12 个：Combat Prowess、Dimensional Travel、Energy Resistance、Fate、Fortitude、Irresistible Offense、Recovery、Skill、Speed、Spell Recall、the Night Spirit、Truesight；属性上限可到 30 [S11 摘要] | 超越凡人上限 20 | 「肉身成圣」、突破人体极限 | 满级后的「超凡入圣」 |
| 超自然恩赐 | 2014 DMG：Blessings、Charms（神或强大存在赠予的一次性/永久恩赐）（未核实） | 剧情奖励 | 仙人赐福、机缘 | 奇遇 |
| 变异 | Lycanthropy（狼人诅咒）、Vampirism、Lich 化（见 §9） | 被动/主动「堕落」 | 入魔、尸变 | 主角被咬、黑化线 |
| 魔法物品 attunement | 最多同调 3 件；需短休专注 [S23] | 「本命法器」上限 | 认主、炼化本命法宝 | 抢到神器却无法认主 |
| PF2：熟练档 | Untrained→Legendary（未核实原文） | 技能也有境界 | 技艺境界 | — |

## 7. 道具与资源

### 7.1 稀有度（品阶）

2024 DMG 规则摘要（Free Rules 魔法物品章）[S24]：

| 稀有度 | 参考价值 (GP) | 制作时间 | 制作成本 (GP) | 仙侠对应 |
|---|---|---|---|---|
| Common | 100 | 5 天 | 50 | 凡品 / 下品法器 |
| Uncommon | 400 | 10 天 | 200 | 中品法器（mithral、adamantine 甲在此档 [S25]） |
| Rare | 4,000 | 50 天 | 2,000 | 上品法器 / 灵器 |
| Very Rare | 40,000 | 125 天 | 20,000 | 极品法器 / 宝器 |
| Legendary | 200,000 | 250 天 | 100,000 | 法宝 / 灵宝（如 Armor of Invulnerability、Defender、Hammer of Thunderbolts [S26]） |
| Artifact | 无价 | 不可制作 | — | 仙器 / 先天至宝：唯一、通常只能以特殊方式毁灭（需研究或任务），是高等级剧情装置 [S24] |

规则补充 [S24]：消耗品（非卷轴）价值减半、制作时间成本减半；制作要 Arcana 熟练 + 对应工具，每天 8 小时，每日须准备物品赋予的法术；原料在城市 75% 可得、他处 25%，缺货需等 7 天再查。

### 7.2 物品类别与仙侠对应

| 类别 [S24] | 说明 | 代表（IP 标注） | 仙侠对应 | 视觉 |
|---|---|---|---|---|
| Potion 药剂 | 一次性液体，Bonus Action 饮用；混服有 miscibility 表（可能爆炸或永久效果）| Potion of Healing 四档：普通 2d4+2 / Greater 4d4+4 / Superior 8d4+8 / Supreme 10d4+20 [S27][SRD] | 丹药（回血丹、品阶丹）；混服 ≈ 丹毒冲突 | 发光液体玻璃瓶，红=治疗 |
| Scroll 卷轴 | 一次性，识字即可用；Spell Scroll 存一个法术 [SRD] | 抄写时间/成本：cantrip 1 天 15 GP … 5 环 25 天 1,500 GP … 9 环 120 天 50,000 GP [S23] | 符箓（一次性、低门槛） | 羊皮卷燃烧化为光字 |
| Wand 魔杖 | 12–15 英寸，常兼 Arcane Focus；有充能 | Wand of Fireballs 等（未核实）[SRD] | 法诀令牌 / 小型法器 | 杖尖射出光束 |
| Staff 法杖 | 2–7 磅，可当长棍 + Focus | Staff of Power、Staff of the Magi（未核实）[SRD] | 宗门传承法杖 ≈ 镇派法宝 | 杖头宝石、敲地冲击波 |
| Rod 权杖 | 2–5 磅，常兼 Focus | Rod of Lordly Might（未核实）| 权柄类法宝（掌门令） | 王权象征 |
| Ring 戒指 | — | Ring of Invisibility 等（Tolkien 式「隐身戒」是通用母题，但「the One Ring」专有） | 储物戒/护身戒 | 戒面发光 |
| Weapon/Armor | 标准武器/护甲的魔法版；+1/+2/+3 | Holy Avenger、Vorpal Sword、Defender（未核实是否在 SRD 5.2 全部保留） | 法剑、法袍 | 剑身符文 |
| Wondrous Item | 杂项：腰带、袋、雕像、乐器 | Bag of Holding [SRD]、Belt of Giant Strength | 储物袋（完美对应）、各类奇物 | — |
| Spellcasting Focus | Arcane Focus：水晶/宝珠/权杖/法杖/魔杖；Druidic Focus：槲寄生/木杖/紫杉杖；Holy Symbol：护符/徽记/圣物匣 [S23] | — | 本命法器、拂尘、念珠 | 施法时 Focus 亮起 |
| Sentient Item 有灵智物品 | 多为武器；有阵营、交流方式、特殊目的；持有者违背其意志要过 Charisma 豁免，否则物品提要求，甚至魅惑持有者 1d12 小时 [S24] | — | 器灵！ | 剑会说话、夺主 |
| Cursed Item | 同调后无法主动解除，需 Remove Curse [S24] | Armor of Vulnerability [SRD 5.2] [S25] | 魔器、邪器反噬 | — |

### 7.3 特殊材料

| 材料 | 规则 | IP | 仙侠对应 |
|---|---|---|---|
| Adamantine 精金 | Adamantine Armor（Uncommon）：对穿戴者的重击变普通命中 [S25]；武器可破坏物体（未核实 2024） | [通用]（希腊语 adamas，「不可征服」）[SRD] | 玄铁/星辰钢 |
| Mithral 秘银 | Mithral Armor（Uncommon）：可穿在衣内，去除隐匿劣势与力量需求 [S28] | D&D 拼写 mithral [SRD]；Tolkien 原拼写 **mithril** 为专有（Middle-earth 版权方） | 冰蚕丝软甲 / 天蚕宝衣 |
| Silvered 镀银 | 对抗狼人等（未核实 2024 规则） | [通用]民俗 | 桃木/黑狗血（克邪材料） |
| Cold iron 寒铁 | 克 fey（PF2 系统化，D&D 偶见）（未核实） | [通用]民俗 | 寒铁、镇妖铁 |
| PF2 补充 | PF2 特殊材料有 low/standard/high grade 品级，另有 orichalcum、dawnsilver（Remaster 后 mithral 改名 dawnsilver、adamantine 保留，未核实） | Paizo | 材料品级 ≈ 灵材品阶 |

### 7.4 制作职业

| D&D | 内容 | 仙侠 |
|---|---|---|
| Herbalism Kit | 可制作 Potion of Healing（25 GP 原料 + 1 天）、Antitoxin、Healer's Kit [S23] | 丹师（D&D 中只是工具熟练，非职业） |
| Alchemist's Supplies | 酸液、Alchemist's Fire 等 [S23] | 火器/毒师 |
| Calligrapher's Supplies / Arcana | 抄写卷轴 [S23] | 符师 |
| Artificer [专有非 SRD] | 唯一以制造为核心的 D&D 职业 | 炼器师 |
| PF2 Alchemist、Runesmith、Inventor | 独立职业；PF2 武器/护甲用 runes（potency/striking/property runes）升级（未核实细则）[S19] | 丹师、符阵师；rune 镶嵌 ≈ 刻阵/铭文 |

## 8. 组织与社会

D&D 核心规则「设定中立」，组织多数写在具体世界书里（Forgotten Realms、Greyhawk、Eberron 等，全部 [专有]）。可直接用的是**组织类型**；具体组织名一律只借机制。

| 组织类型 [通用] | D&D 中的形态 | 内部结构（常见写法） | 仙侠对应 | 具名例子（[专有]，只借机制） |
|---|---|---|---|---|
| Wizard academy / arcane college / mage guild | 法师学院、法师塔、法师公会 | 学徒 apprentice → 法师 → 大法师 archmage [SRD 怪物 Archmage、Mage、Apprentice 为 SRD 数值块，未核实 5.2 是否保留] | 宗门（法修宗门） | Red Wizards of Thay（地区法师寡头）、Kirin Tor 属 Blizzard |
| Temple / Church / Faith | 神殿、教会，神职 Cleric；领域决定教义 | 侍祭 Acolyte → 祭司 Priest → 大祭司（SRD 有 Acolyte、Priest 数值块）| 寺院、道观、香火神道 | Church of Lathander 等 |
| Knightly order / Paladin order | 圣武士以誓言结社 | 侍从 → 骑士 → 团长；誓言 = 会规 | 护法宗门、正道联盟 | Order of the Gauntlet |
| Druid circle | 德鲁伊圈子（子职即名为 Circle） | 长老制、圣林 | 隐世妖修门派 | Emerald Enclave |
| Thieves' guild | 盗贼公会、刺客行会 | 首领、帮派分区 | 黑道、刺客楼 | Zhentarim（黑网） |
| Secret society | 情报网、反暴政秘密组织 | 分散小组 | 隐门、守护者 | Harpers |
| Monastery | 武僧寺院（子职 Warrior of …） | 师父-弟子 | 少林、武当 | — |
| Warlock cult | 邪教，崇拜契约方 | 教主（契约者）-信徒 | 魔教 | Cult of the Dragon |
| Kingdom / Noble house | 王国、贵族、联盟 | 封建 | 世家、皇朝 | Lords' Alliance |
| Adventuring company | 冒险者小队 / 公会（2024 DMG 有「团队/队伍」的描述，未核实细则） | 小队制 | 散修结伴、探秘小队 | — |

**PF2 差异**：Pathfinder 设定 Golarion 中，「Pathfinder Society」（探险家协会，主角团默认组织）是招牌 [专有]；其组织普遍以 faction / Society 形式提供成长路线（未核实细则）。

> 来源：组织类型为通行知识；SRD 数值块名称（Acolyte、Priest、Mage、Archmage 等）来自 SRD 5.1，SRD 5.2 是否全部保留 **未核实**；具名组织为 Forgotten Realms 专有名（记忆，**未核实**逐条）。

## 9. 宇宙观

### 9.1 Great Wheel（大轮回）结构

来源：[S29][S30]。注意 SRD 5.2 明确**不含**「The Planes of Existence」章节 [S1]，但 Astral/Ethereal Plane、Feywild、Shadowfell 等词在法术/怪物文本中出现（未逐条核实）；**Great Wheel 的具体外层位面名称与排列、Sigil、Outlands 属 WotC 设定**，但很多名字本身取自神话（Elysium、Hades、Arcadia、Limbo、Abyss、Gehenna、Acheron 等），只有组合与 Baator、Mechanus、Carceri（拉丁语「监狱」）、Bytopia、Sigil 等更偏专有。

| 层 | 位面 | 性质 | 仙侠对应 |
|---|---|---|---|
| 物质界 | Material Plane（Prime Material） | 凡人世界 | 人间 / 下界 |
| 物质界的回响 | **Feywild** 妖精荒野：物质界的镜像，情绪被放大（喜→狂喜，怒→暴怒），由 Seelie / Unseelie 宫廷的 Archfey 统治 [S30] | 鲜艳、魔幻、讲规则 | 洞天福地 / 青丘狐国 |
|  | **Shadowfell** 堕影冥界：物质界的暗影，情绪被压抑，导致抑郁；含 Ravenloft 恐怖领域（[专有]）[S30] | 灰暗、死气 | 幽冥 / 阴间（但不是审判之所） |
| 过渡界 | **Ethereal Plane** 以太界：连接内层诸界，可看见物质界而不被看见，可穿墙 [S30] | 灵体状态 | 阴阳界 / 灵魂出窍状态 |
|  | **Astral Plane / Astral Sea** 星界：外层诸界之间的虚空，时间流速诡异（千年似一日）[S30] | 银色虚空，诸神尸骸漂浮（通行设定，未核实） | 虚空 / 星海；「天上一日，人间千年」反过来 |
| 内层诸界 | Elemental Planes：Air、Earth、Fire、Water；para-/quasi-elemental；Positive / Negative Energy Plane [S29][S30] | 元素本源 | 五行本源之地；正/负能量 ≈ 阳气/阴气本源 |
| 外层诸界 | 按阵营排列的 16 个位面 + 中心 Outlands（Sigil 浮在其上）[S29] | 神国、灵魂归宿 | 天界 / 魔界 / 地府 |
| 远域 | Far Realm（4e World Axis 起常见，异怪 aberration 的来源）[S29] | 不可名状 | 天外 / 域外天魔 |

### 9.2 外层位面 × 阵营轴

阵营轴：Law–Chaos（秩序–混乱）× Good–Evil（善–恶），九宫格 [通用 + SRD 有阵营规则]。PF2 Remaster 已删除阵营机制，改用 holy/unholy 特性（Champion Cause）[S7 相关，未核实具体条文]。

| 阵营 | 位面（[S30] 列出的倾向） | 主宰者 | 仙侠对应 |
|---|---|---|---|
| LG 守序善良 | Mount Celestia（七重天山）；Bytopia（LG/NG）；Arcadia（LG/LN） | 天使、Celestial Paragons | 天庭 / 极乐 |
| NG 中立善良 | Elysium | — | 净土 |
| CG 混沌善良 | Arborea；Beastlands（NG/CG）；Ysgard（CG/CN） | 英灵、兽灵 | 蓬莱仙岛、英灵殿 |
| CN 混沌中立 | Limbo（混沌汤）；Pandemonium（CN/CE） | Slaad（[专有]） | 混沌 |
| CE 混沌邪恶 | **Abyss** 无底深渊：层数理论上无限 | Demon Lords | 魔界 / 无间 |
| NE 中立邪恶 | Hades（灰色荒原）；Carceri（监狱位面）；Gehenna（LE/NE） | Yugoloth（[专有]）| 地狱 / 枉死城 |
| LE 守序邪恶 | **Nine Hells**（Baator）：九层，Asmodeus 统领 [S31] | Archdevils | 十八层地狱（有官僚体系）|
| LN 守序中立 | Mechanus（齿轮位面）；Acheron | Modron（[专有]） | 天道 / 天规机制 |
| N 绝对中立 | Outlands（中心）+ Sigil 门之城 [专有] | Lady of Pain [专有] | 中州 / 鬼市 |

**Blood War（血战）**：魔鬼（devils，守序邪恶）与恶魔（demons，混沌邪恶）之间近乎永恒的歼灭战，1991 年引入；成因各版本不一 [S31][S32]。仙侠对照：正魔大战换成「魔与魔之间」的战争——双方都邪恶但理念不同（官僚 vs 无序），这在仙侠中少见，是可借的新冲突。

### 9.3 天界 / 魔界 / 亡灵：对应仙、魔、鬼

**Celestials（天界生物）**——SRD 5.2 收录：Deva、Planetar、Solar、Couatl、Pegasus、Unicorn、Sphinx 等 [S33]。

| 天使 | CR | 角色 | 仙侠对应 |
|---|---|---|---|
| Deva [SRD] | 10 [S34] | 神的信使、下凡执行者 | 天兵 / 仙使 |
| Planetar [SRD] | 16 [S34] | 神的战士、军团统领 | 天将 |
| Solar [SRD] | 21 [S34] | 神的右手，最强天使 | 天帝亲卫 / 大罗神将 |
| （Empyrean、Couatl 等） | — | — | 灵兽、天仙 |

**Devils（魔鬼，守序邪恶，Nine Hells）**：有严格晋升阶梯——灵魂变为 lemure（最低、无心智），按功绩晋升为更高形态 [S31]。SRD 5.2 收录：Lemure、Imp、Bearded、Barbed、Chain、Bone、Horned、Erinyes、Ice Devil、Pit Fiend [S35]。

| 阶层 [S31] | 代表 | 仙侠对应 |
|---|---|---|
| Least / Lesser | Lemure（灵魂所化，炮灰）、Imp、Barbed、Bone | 小鬼、夜叉 |
| Greater | Horned、Ice Devil、Erinyes、**Pit Fiend**（魔鬼领主，最强非独特魔鬼） | 鬼王、阎罗殿判官 |
| Archdevils / Lords of the Nine | 九层各一位统治者；Asmodeus 统领全域，名言「Read the fine print」[S31] | 十殿阎罗 / 魔尊 |

特点：灵魂交易与契约（Pact Primeval 神话、Ruby Rod 执行契约）[S31]——极适合短剧的「签字即入局」桥段。层名多取自但丁/希腊神话（Avernus、Dis、Phlegethos、Stygia、Malbolge、Nessus 等 [未核实全表]），Asmodeus 本身是《托比特书》中的魔鬼名 [通用]；但「Zariel 统治 Avernus」等具体设定 [专有]。

**Demons（恶魔，混沌邪恶，Abyss）**：无序、残暴、数量无穷；「真」tanar'ri 如 balor（原名 Balrog，因 Tolkien 版权改名）、六臂蛇身的 marilith 统率低等恶魔 [S32]。SRD 5.2 收录：Dretch、Quasit、Vrock、Hezrou、Glabrezu、Nalfeshnee、Marilith、Balor、Succubus、Incubus 等 [S35]。

| 层级 | 代表 | 仙侠对应 |
|---|---|---|
| 低等 | Dretch、Quasit、Manes（未核实 SRD） | 魔物、魔兵 |
| 中高等 | Vrock（秃鹫魔）、Hezrou、Glabrezu（交易愿望）、Nalfeshnee（审判灵魂） | 魔将 |
| 最高等 | Marilith（六臂蛇女）、Balor（火鞭炎魔） | 魔帅 / 天魔 |
| Demon Lords / Princes [专有名] | Orcus、Demogorgon、Juiblex、Zuggtmoy、Graz'zt 各统治深渊某层 [S32] | 魔君 / 魔主（Demogorgon 一词本身出自古典文献 [通用]，但 D&D 形象 [专有]）|

**Undead（亡灵）**——SRD 5.2 收录：Ghost、Ghoul、Ghast、Lich、Mummy、Mummy Lord、Shadow、Skeleton、Specter、Vampire、Vampire Spawn、Wight、Wraith、Will-o'-Wisp、Zombie 等 [S36]。

| 亡灵 | 关键规则 | 仙侠对应 |
|---|---|---|
| Lich 巫妖 | CR 21；**SRD 5.1 用「phylactery」**：毁灭后若命匣在，1d10 天后于命匣 5 尺内重生 [S37]；**SRD 5.2 改称「spirit jar」**：1d10 天后在巢穴内重生，巢穴内传奇抗性 5/天 [S38] | 修士以秘法「炼尸成就不死」+ 魂魄寄于本命魂器；最接近「元神寄于法宝/肉身毁而魂不灭」；也像「魂灯」——只要灯不灭人可复生 |
| Vampire 吸血鬼 | SRD 有 Vampire、Vampire Spawn [S36]（细则未核实）| 血尸、吸血魔修 |
| Ghost / Specter / Wraith | 灵体 | 鬼、怨灵、厉鬼 |
| Mummy Lord | 有巢穴的木乃伊王 | 古墓尸王 |
| Skeleton / Zombie | 被 Animate Dead 驱使 | 傀儡尸、炼尸 |

### 9.4 神祇

- 5e 核心规则不设固定神系；2014 PHB 附录给出若干世界的神系与「历史神话神系」（希腊、埃及、北欧等），SRD 5.2 删除了「Fantasy-Historical Pantheons」[S1]。
- 神的力量层级用 3.5 版 divine rank 对照最清楚（见 §3.3）。
- **仙侠差异**：D&D 神祇靠信仰存续、彼此争夺信徒与神职（portfolio），没有统一天庭；「天庭」更像外层位面的多个独立神国。

## 10. 仙侠对照速查表

| 西幻概念（D&D/PF2） | IP | 仙侠对应 | 对应质量 | 差异说明 |
|---|---|---|---|---|
| Character level 1–20 | [SRD] | 境界（炼气→大乘） | 中 | D&D 等级线性加数值；仙侠境界是质变+寿元增加 |
| Tier 1/2/3/4 | [SRD 规则概念] | 炼气 / 筑基 / 金丹–元婴 / 化神以上 | 高 | 四档威胁范围：村庄→王国→大陆→多元宇宙，与仙侠「影响范围随境界扩大」一致 |
| Epic Boon（19 级+，属性上限 30） | [SRD 5.2 部分] | 渡劫、肉身成圣 | 中 | 不是飞升，只是「超越凡人上限」 |
| Divine rank 0–20 | [3.5 OGL] | 地仙→天仙→金仙→大罗→天尊 | 中 | 神格靠信徒数量，仙位靠修为 |
| Spell level 0–9 | [SRD] | 功法/神通品阶 | 高 | 两条轴并存，正好对应 |
| Spell slot + Long Rest | [SRD] | 灵力储量 + 打坐回元 | 中高 | 法术位是「格子」，仙侠是连续的真元 |
| Cantrip | [SRD] | 基础法诀、小术 | 高 | — |
| Ritual casting | [SRD] | 开坛作法、布阵 | 高 | 时间换资源 |
| Concentration | [SRD] | 维持法术需心神专注 | 高 | 被打断＝破功 |
| 8 schools | [SRD 词为通用英语] | 法术分类：护体/挪移/卜算/摄魂/攻伐/幻术/鬼道/变化 | 中 | 仙侠按五行和道统分，西幻按作用分 |
| Arcane / Divine / Primal / Occult | [通用词]（PF2 体系 Paizo） | 法修 / 神道香火 / 妖修灵修 / 神识巫蛊 | 中高 | — |
| Wizard spellbook | [SRD] | 功法秘籍 | 高 | 丢书失法，仙侠功法记在脑中 |
| Warlock pact / patron | [SRD] | 魔道契约、借魔尊之力 | 高 | — |
| Sorcerer bloodline | [SRD] | 血脉、天生灵根 | 高 | — |
| Paladin oath / Divine Smite | [SRD] | 誓愿、浩然正气、雷法斩邪 | 高 | 誓言即力量源，不一定需要神 |
| Cleric domain | [SRD] | 所奉神之「道」（佛门/道门分支） | 中 | — |
| Monk Focus（旧 Ki） | [SRD] | 真气、内力 | 高 | 西幻里最东方的职业 |
| Druid Wild Shape | [SRD] | 化形、变身 | 高 | 方向相反：仙侠是妖化人，德鲁伊是人化兽 |
| Potion（4 档治疗药） | [SRD] | 丹药 | 高 | 药剂即时，丹药常需炼化 |
| Spell scroll | [SRD] | 符箓 | 高 | 都是一次性、可交易 |
| Wand / Staff / Rod | [SRD] | 法器 / 镇派法杖 / 掌门令 | 中高 | — |
| Rarity Common→Legendary | [SRD] | 法器品阶（下/中/上/极品→法宝） | 高 | — |
| Artifact | [SRD 概念] | 仙器、先天至宝 | 高 | 只能以特殊方式毁灭 |
| Attunement（上限 3） | [SRD] | 认主、炼化本命法宝 | 高 | — |
| Sentient item | [SRD] | 器灵 | 高 | 可夺主 |
| Bag of Holding | [SRD] | 储物袋 | 高 | — |
| Adamantine / Mithral | [SRD]（mithril 拼写属 Tolkien） | 玄铁 / 天蚕软甲 | 中 | — |
| Wizard academy / temple / order | [通用] | 宗门 / 寺观 / 护法盟 | 中高 | 西幻宗教组织更中央集权 |
| Material Plane | [SRD/通用] | 人间 | 高 | — |
| Feywild | [WotC 用词，未核实是否 SRD] | 洞天、青丘 | 中 | — |
| Shadowfell | [WotC 用词，未核实是否 SRD] | 幽冥 | 中 | 没有审判/轮回机制 |
| Astral Plane | [通用] | 星海 / 虚空 | 中 | — |
| Ethereal Plane | [通用] | 阴阳交界 / 灵体态 | 中 | — |
| Elemental Planes（四元素） | [通用] | 五行本源 | 中 | 四元素 vs 五行 |
| Upper Planes（Celestia、Elysium…） | [神话词通用，体系专有] | 天庭、净土 | 中 | 没有统一天庭 |
| Nine Hells（Baator） | 「Nine Hells」通用；Baator [专有] | 十八层地狱 + 地府官僚 | 高 | 魔鬼会晋升，像官场 |
| Abyss | [通用] | 魔界、无间 | 高 | — |
| Blood War | [WotC 设定] | （无直接对应）魔与魔的战争 | 低 | 可借的新冲突 |
| Angels: Deva / Planetar / Solar | [SRD] | 仙使 / 天将 / 帝君亲卫 | 高 | — |
| Devils（lemure→pit fiend→archdevil） | [SRD 怪名；baatezu 为 PI] | 小鬼→鬼王→阎罗 | 高 | — |
| Demons（dretch→balor→demon lord） | [SRD 怪名；tanar'ri 为 PI] | 魔兵→魔帅→魔君 | 高 | — |
| Lich + phylactery / spirit jar | [SRD] | 魂器、魂灯、元神寄体 | 高 | 「找到并毁掉命匣」= 经典任务结构 |
| Vampire | [通用][SRD] | 血尸、吸血魔修 | 中 | — |
| Tiefling / Aasimar | [SRD] / [专有] | 魔裔 / 仙裔 | 高 | — |
| Elf（750 年） | [通用][SRD] | 长生灵族、仙族 | 中高 | — |
| Dwarf（350 年） | [通用][SRD] | 炼器之族 | 中 | — |
| Orc | [通用][SRD 5.2] | 蛮族/妖族 | 中 | — |
| PF2 proficiency（Untrained→Legendary） | [Paizo 机制] | 入门/小成/大成/圆满/化境 | 高 | — |

## 11. 短剧可用性与 IP 风险

### 11.1 屏幕表现与爽点

| 元素 | 屏幕表现 | 欧美熟悉度 | 爽点 / 冲突 |
|---|---|---|---|
| Fireball / Evocation | 橙红火球、爆燃、冲击波 | 高（游戏、BG3、电影《龙与地下城：侠盗荣耀》2023）| 一招清场 |
| Shield / Counterspell | 半透明符文盾、对手法术在半空碎裂 | 高 | 「你的大招被我一句咒语取消」反杀 |
| Divine Smite / Paladin | 剑身燃金光、光环、跪誓 | 高 | 誓言破碎/重立；正义审判 |
| Warlock pact | 血签契约、眼睛变黑、巨大阴影投在背后 | 高 | 契约代价揭晓；「我从地狱借来力量」 |
| Sorcerer bloodline 觉醒 | 皮肤浮鳞、竖瞳、龙翼展开 | 高 | 濒死觉醒、被歧视血脉逆袭 |
| Lich phylactery | 发绿光的匣子/宝石、灰白骷髅法师 | 中高 | 「杀他无用，必须先找到命匣」——解谜+追逐 |
| Devil contract | 优雅西装魔鬼、燃烧的羊皮纸、小字条款 | 高 | 「Read the fine print」——条款反转（非常适合短剧） |
| Demon | 火鞭炎魔、六臂蛇女 | 高 | 纯暴力 boss |
| Angel（Deva/Solar） | 金白光、羽翼、无面头盔 | 高 | 天使下凡审判 / 天使堕落 |
| Feywild | 花瓣、萤光、过分鲜艳的色彩 | 中 | 「吃了妖精食物就回不去」、名字被夺 |
| Shadowfell | 低饱和灰蓝、雾 | 中 | 情绪被吞噬 |
| Attunement / Sentient item | 戒指/剑与手掌发光融合；剑会说话 | 中 | 神器不认主 / 器灵夺舍 |

**观众熟悉度总评**：D&D 体系在欧美玩家中熟悉度高（BG3、Critical Role、《怪奇物语》、2023 电影均有带动——为通行认知，未逐一核实）；PF2 熟悉度中低，只建议借机制不借名。

### 11.2 IP 风险分级

| 风险 | 内容 | 建议 |
|---|---|---|
| 低（可直接用） | SRD 5.1/5.2 中的规则术语与通用词：八学派名、spell slot、cantrip、Paladin/Warlock/Sorcerer 等职业名、Elf/Dwarf/Halfling/Gnome/Orc/Tiefling/Dragonborn/Goliath、Potion of Healing、Bag of Holding、Lich、Vampire、Deva/Planetar/Solar、Pit Fiend、Balor、Marilith 等 SRD 怪名 [S1][S33][S35][S36] | 用 SRD 内容需按 CC-BY-4.0 署名；我们只用通用词不复制文本时，风险更低（法律问题请以律师意见为准） |
| 中（谨慎） | WotC 自造但看起来像普通词：Feywild、Shadowfell、Great Wheel 的组合、Blood War；PF2 的四传统+四本质搭配 | 改名或换说法（如「妖精界」「暗影界」），借结构不借名 |
| 高（不用） | SRD 5.1 OGL 版法律页列为 Product Identity 的名字：beholder、gauth、carrion crawler、tanar'ri、baatezu、displacer beast、githyanki、githzerai、mind flayer/illithid、umber hulk、yuan-ti；CC 版 SRD 5.1 中这些词以「仅名称」出现，但法律效力社区有争议 [S39 摘要] → 一律当专有。SRD 5.2 明确排除的 Aasimar、Beholder、Strahd、Orcus、Tiamat [S1]；全部设定专名：Forgotten Realms、Faerûn、Waterdeep、Baldur's Gate、Greyhawk、Eberron、Ravenloft、Sigil、Lady of Pain、Mystra/the Weave、Asmodeus 作为 D&D 角色的形象（名字本身源自古典宗教文献）、Zariel、Lolth、Corellon、Gruumsh；Paizo：Golarion、Pathfinder Society、Nephilim 作为 PF 物种设定 | 不用；若要「圣经式」名字（Asmodeus、Demogorgon），只用古典文献层面的含义，不借 D&D 外观与设定 |
| 他方 IP 混入 | 「mithril」（Tolkien 拼写）、「Balrog」（D&D 早期曾用，后改 balor）[S32]、hobbit、ent | 用 mithral / 自造词；不用 Balrog、hobbit |

### 11.3 给资料库的建议（结论）

1. **骨架直接用 D&D**：「等级四档 × 法术十环 × 物品六档稀有度」三张表可作为西幻资料库的默认品阶体系，名称全部是 SRD/通用词。
2. **力量来源用「学习 / 神恩 / 誓言 / 契约 / 血统 / 自然」六分**（D&D 职业驱动），**本质用 PF2 四本质**作底层设定——前者给角色动机，后者给视觉配色。
3. **仙魔鬼**：天使三阶、魔鬼晋升制、恶魔无序、巫妖命匣，对应清晰，且 SRD 开放，是最安全的反派库。
4. **最大差异要显式写进设定**：西幻没有统一天庭和轮回审判；神靠信仰而非修为；没有「丹师」职业（PF2 Alchemist 可补）。

## 12. 来源列表

访问日期均为 2026-11-08。

| 编号 | URL | 标题 | 状态 |
|---|---|---|---|
| S1 | https://www.dndbeyond.com/srd | System Reference Document 5.2.1（D&D Beyond 官方） | 正文 |
| S2 | https://www.pcgamer.com/games/board-games/the-core-of-the-new-dungeons-and-dragons-rules-have-been-released-into-the-creative-commons-so-you-can-use-them-when-you-publish-your-own-d-and-d-material ；https://belloflostsouls.net/?p=569419 | SRD 5.2 发布报道 | 摘要 |
| S3 | https://www.dndbeyond.com/posts/1717-2024-core-rulebooks-to-expand-the-srd | 2024 Core Rulebooks to Expand the SRD | 摘要 |
| S4 | https://en.wikipedia.org/wiki/Magic_in_Dungeons_%26_Dragons | Magic in Dungeons & Dragons | 正文（前 10 万字） |
| S5 | https://www.dndbeyond.com/sources/dnd/free-rules/spells ；https://www.dndbeyond.com/sources/dnd/free-rules/spell-descriptions | D&D Free Rules (2024)：Spells / Spell Descriptions | 正文（部分） |
| S6 | https://dnd5e.wikidot.com/spells | DND 5th Edition Spells（fan wiki） | 正文 |
| S7 | https://pathfinderwiki.com/wiki/Magic | PathfinderWiki: Magic | 正文 |
| S8 | https://2e.aonprd.com/Traits.aspx?ID=11 | Archives of Nethys: Arcane trait（Player Core p.452） | 正文 |
| S9 | https://www.dndbeyond.com/sources/dnd/basic-rules-2014/step-by-step-characters | Basic Rules 2014: Step-by-Step Characters（Tiers of Play、XP 表） | 正文 |
| S10 | https://www.dndbeyond.com/sources/dnd/free-rules/character-classes | D&D Free Rules (2024): Character Classes | 正文（约 98%） |
| S11 | https://arcaneeye.com/mechanic-overview/dnd-2024-epic-boon-feats/ ；https://dungeonmister.com/guides/epic-boon-feats-in-dd-2024/ | Epic Boon 专长列表 | 摘要 |
| S12 | https://5thsrd.org/spellcasting/what_is_a_spell/ | 5th SRD: What Is a Spell? | 正文 |
| S13 | https://cayzle.com/3Esrd/divine.html | d20 SRD v3.5: Divine（Divine Ranks） | 正文 |
| S14 | https://www.d20srd.org/srd/divine/divineRanksAndPowers.htm | d20SRD: Divine Ranks and Powers | 受阻（403），仅摘要 |
| S15 | https://www.enworld.org/threads/deity-rankings.109276/ | EN World: deity rankings | 摘要 |
| S16 | https://cdn.paizo.com/blog/mythic-magic | Paizo blog: Mythic Magic（War of Immortals） | 正文 |
| S17 | https://paizo.com/community/blog/v5748dyo6siek ；https://paizo.com/corepreview | Player Core Preview: Spells and Spellcasting, Remastered | 摘要 |
| S18 | https://dexerto.com/gaming/every-subclass-in-dds-new-2024-players-handbook-2784139 | Every subclass in D&D's new 2024 Player's Handbook | 正文 |
| S19 | https://2e.aonprd.com/Classes.aspx | Archives of Nethys: Classes | 正文 |
| S20 | https://www.dndbeyond.com/sources/dnd/free-rules/character-origins | D&D Free Rules (2024): Character Origins | 正文 |
| S21 | https://paizo.com/threads/rzs43t50 | PF2 Remastered: Planar Scion -> Nephilim（论坛） | 摘要 |
| S22 | https://pathfinderwiki.com/wiki/Nephilim_(planar_scion) | PathfinderWiki: Nephilim | 摘要 |
| S23 | https://www.dndbeyond.com/sources/dnd/free-rules/equipment | D&D Free Rules (2024): Equipment | 正文 |
| S24 | https://www.dndbeyond.com/sources/dnd/free-rules/magic-items | D&D Free Rules (2024): Magic Items | 正文 |
| S25 | https://api.open5e.com/v2/magicitems/?document__key=srd-2024&search=adamantine | Open5e API：SRD 2024 magic items（含 Adamantine Armor） | 正文 |
| S26 | https://api.open5e.com/v2/magicitems/?document__key=srd-2014&rarity=legendary | Open5e API：SRD 5.1 legendary items | 正文（部分） |
| S27 | https://api.open5e.com/v2/magicitems/?document__key=srd-2024&name__icontains=potion | Open5e API：potions | 正文 |
| S28 | https://api.open5e.com/v2/magicitems/?document__key=srd-2014&name__icontains=mithral | Open5e API：Mithral Armor | 正文 |
| S29 | https://en.wikipedia.org/wiki/Great_Wheel_cosmology | Great Wheel cosmology | 正文（前 10 万字） |
| S30 | https://dungeonmister.com/lore/locations/the-planes-of-existence-in-dnd-5e/ | The Planes of Existence in D&D 5e | 正文 |
| S31 | https://en.wikipedia.org/wiki/Devil_(Dungeons_%26_Dragons) | Devil (Dungeons & Dragons) | 正文（前 10 万字） |
| S32 | https://en.wikipedia.org/wiki/Demon_(Dungeons_%26_Dragons) | Demon (Dungeons & Dragons) | 正文（前 10 万字） |
| S33 | https://api.open5e.com/v2/creatures/?document__key=srd-2024&type=celestial | Open5e API：SRD 2024 celestials | 正文 |
| S34 | https://5thsrd.org/gamemaster_rules/monsters/deva/ ；https://roll20.net/compendium/dnd5e/Monsters:Planetar ；https://roll20.net/compendium/dnd5e/Monsters:Solar | 天使 CR | 摘要 |
| S35 | https://api.open5e.com/v2/creatures/?document__key=srd-2024&type=fiend | Open5e API：SRD 2024 fiends | 正文 |
| S36 | https://api.open5e.com/v2/creatures/?document__key=srd-2024&type=undead | Open5e API：SRD 2024 undead | 正文 |
| S37 | https://api.open5e.com/v2/creatures/srd_lich/ | Open5e API：SRD 5.1 Lich（phylactery） | 正文 |
| S38 | https://api.open5e.com/v2/creatures/srd-2024_lich/ | Open5e API：SRD 5.2 Lich（spirit jar） | 正文 |
| S39 | https://www.enworld.org/goto/post?id=8918547 ；https://www.prismaticwasteland.com/blog/no-one-owns-these-monsters | Beholders, Mind Flayers… Released Into Creative Commons (Kinda)；SRD 5.1 Product Identity 讨论 | 摘要 |
| — | https://forgottenrealms.fandom.com/wiki/Nine_Hells_of_Baator ；https://forgottenrealms.fandom.com/wiki/Demon | Forgotten Realms Wiki | 受阻（402） |
| — | https://2e.aonprd.com/Traditions.aspx | AoN Traditions | 受阻（404） |
| — | https://5thsrd.org/spellcasting/magic_schools/ | 5th SRD: Magic Schools | 受阻（403） |
| — | https://www.dndbeyond.com/sources/dnd/basic-rules-2014/appendix-c-the-planes-of-existence | Basic Rules 2014 Appendix C | 受阻（404） |
