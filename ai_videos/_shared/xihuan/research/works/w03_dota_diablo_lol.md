---
worker_id: w03-dota-diablo-lol
stage: research
role: researcher
angle: hero-games
status: complete
blockers: []
confidence: medium
---

# Dota 2 / Diablo / League of Legends 拆解

## 1. 概览

| 作品 | 版本范围 | 类型 | 对我们最有用的部分 |
|---|---|---|---|
| Dota 2（Valve，源自 DotA 地图） | 7.x 版本，重点 7.23（等级上限 30）、7.36（Facets / Innate）、7.38（Madstone 中立物品） | MOBA | 三属性（Str/Agi/Int/Universal）↔ 体修/敏修/法修；单局内「打钱—合成—神装」的爆发成长曲线；Aghanim 升级器；Roshan 掉落（复活盾）；「两位古神借凡人打代理战」的宇宙观 |
| Diablo I–IV（Blizzard） | D1（1996）至 D4 + Vessel of Hatred（2024）与后续赛季 | ARPG | 天堂/地狱/凡间（Sanctuary）三层宇宙 ↔ 三界；Nephalem「天使×恶魔混血＝人类潜能」↔ 修仙「凡人可逆天」；物品稀有度颜色阶梯（白/蓝/黄/金/橙/暗金）↔ 法宝品阶；符文字（Runeword）↔ 阵法/符箓组合；Paragon 满级后继续成长 ↔ 境界小层 |
| League of Legends / Runeterra（Riot） | Universe 官方设定 2014 后重启版 | MOBA + 跨媒体（Arcane、Legends of Runeterra） | 「地区＝文化＝魔法观」：禁魔王国、征服帝国、精神灵性之岛、冰雪血脉、沙漠飞升帝国、星灵附体圣山；Ascended（飞升者）↔ 飞升成仙；Darkin（被困武器里的堕落飞升者）↔ 器灵/魔兵；Void（虚空）↔ 天外邪魔；World Runes ↔ 天地本源 |

**为什么对我们有用**：三者都是欧美玩家（尤其 18–35 岁男性）最熟的「英雄打怪升级」视觉语言。它们不是严肃奇幻文学，而是把「成长数值化、道具颜色化、爆发可视化」做到极致——这恰好是短剧爽点需要的屏幕语法。本报告侧重**机制借鉴**，所有专名默认 [专有]，只可借形不可借名。

来源：[S1][S9][S20][S30]

## 2. 力量来源与魔法分类

### 2.1 Dota 2：属性即「修行路线」，宇宙层面是光/暗两古神

| 力量来源 | 原理（游戏/设定） | 代价 | 视觉惯例 | 标注 | 仙侠对应 |
|---|---|---|---|---|---|
| Strength 力量 | 每点 +22 最大生命（及回血）；力量主属性英雄额外获得攻击力 | 敏捷/法力成长低，靠肉身硬抗 | 红色属性图标、巨大体型、近战重击 | [通用] 概念 | 体修 / 炼体 |
| Agility 敏捷 | 每点约 +0.167 护甲、+1 攻速 | 前期脆，后期「一刀一个」 | 绿色图标、快攻残影、暴击数字 | [通用] | 剑修 / 身法流 |
| Intelligence 智力 | 每点 +12 最大法力、+0.05 回蓝、+0.1% 魔抗 | 血薄，被近身即死 | 蓝色图标、施法吟唱、大范围技能 | [通用] | 法修 |
| Universal 全才 | 三属性都提供上述加成，但「主属性加攻击」按三属性总和打折计算（具体系数版本间有调整，未核实） | 每项都不顶尖 | 紫/彩色图标 | [通用] | 三修兼顾 / 杂修 |
| Radiant 天辉 / Dire 夜魇 Ancient（古代遗迹） | 原初心智（Primordial Mind）分裂出的两块碎片，代表光明—秩序—生长 vs 毁灭—腐朽；彼此无法直接消灭，于是扭曲世界、操纵凡人和神祇为自己打仗 | 被卷入者沦为「小兵」（creeps，被转化的无意识士兵） | 天辉：绿树金光；夜魇：红岩熔浆 | [专有] 名称；「两大本源对立神借凡人代理战」为[通用]结构 | 正邪两道本源 / 天道与魔道 |
| Mad Moon / Radiant Ore / Direstone | Zet（Arc Warden）把两古神囚禁在 Mad Moon，月碎（the Sundering）后碎片落地成两种矿石，魔法由此在世间萌发 | — | 蓝白发光矿 / 黑红矿 | [专有] | 天外陨铁 / 灵石起源 |

来源：[S2][S3][S6]（属性数值来自 bo3.gg 与 Liquipedia 摘要，二者互证；Universal 系数未核实）

### 2.2 Diablo：天使 vs 恶魔，人类是两者混血

| 力量来源 | 原理 | 代价 | 视觉惯例 | 标注 | 仙侠对应 |
|---|---|---|---|---|---|
| Holy / Light（天堂之光） | 天使由 Crystal Arch（水晶拱门）中诞生，力量来自秩序与美德；圣骑士、十字军借圣光作战 | 教条、傲慢（天使议会常视人类为可牺牲品） | 金白光翼、无面兜帽天使、光剑 | [通用]：holy light/angel；[专有]：Crystal Arch | 仙界 / 天庭神力 |
| Infernal / Demonic（地狱） | 恶魔由七大魔王统领；Warlock 召唤恶魔、用 Soul Shards（D4 2026 资料片） | 腐化、契约、灵魂抵押 | 红黑、熔岩裂纹、犄角、肉质建筑 | [通用]：demon/warlock；[专有]：Prime Evils 名称 | 魔道 / 血祭 |
| Nephalem 血脉 | 叛逃天使 Inarius 与恶魔 Lilith 的后代，天生超越天使和恶魔的潜能；Inarius 调谐 Worldstone 让其逐代衰减 | 被天地两方忌惮、追杀 | 「普通人」外貌，觉醒时爆光 | [专有]：Nephalem / Worldstone；[通用]：半神半魔混血结构 | 「凡人血脉被封印，觉醒后可逆天」——非常接近仙侠废柴体质 |
| Arcane（Sorcerer/Wizard） | 学院式元素魔法（火/冰/电/奥术） | 法力、肉身脆 | 冰晶、火球、连锁闪电 | [通用] | 五行法术 |
| Necromancy（Rathma 祭司） | 维持生死平衡，以尸体与鲜血为资源；D3/D4 资源为 Essence + Corpses | 社会排斥、骨与血自损 | 骨甲、骨矛、绿白死灵光 | [通用]：necromancer；[专有]：Priests of Rathma | 尸修 / 鬼修 |
| Nature / Spirit（Druid、Spiritborn、Witch Doctor） | 德鲁伊变身熊狼、操风暴；Spiritborn 召唤四种动物守护灵（Jaguar 速度 / Gorilla 坚韧 / Eagle 精准 / Centipede 毒与控）；巫医召灵、诅咒 | 失去人形、灵界牵引 | 半兽化、动物幻影、绿色藤蔓与雷暴 | [通用]：druid/shaman/spirit animal；[专有]：Spiritborn 四灵名 Rezoka/Wumba/Kwatli/Balazan | 妖修（化形）、兽魂附体、巫蛊 |

来源：[S10][S11][S12][S14][S17]

### 2.3 Runeterra：「地区决定魔法观」

| 力量来源 | 原理 | 代价 | 视觉惯例 | 标注 | 仙侠对应 |
|---|---|---|---|---|---|
| Innate magic（天生施法者，社区常称 mageborn） | 所有生灵都能学魔法，但有人天生就会；不天生者靠严格训练、学习与纪律获得某种魔法 | 在禁魔国被当作「疾病」，被隔离、驱逐 | 失控时周身溢光、物件漂浮 | [通用] 概念 | 天生灵根 vs 后天苦修 |
| World Runes（世界符文） | 未知 Celestials 用来塑造世界的本源符文；首次使用重塑了整片国土，引发 Rune Wars；Ryze 收集封存 | 足以毁灭国家 | 发光几何符文石 | [专有] 名称；「创世本源符文」为[通用]结构 | 天道本源 / 造化玉碟一类至宝 |
| Ascension（太阳圆盘飞升） | Shurima 用 Sun Disc 让被选中的凡人获得不朽与「远超凡人」的天界之力；仪式后来不稳定，常致死或畸变 | 失败即死/畸形；仪式可被破坏（Xerath 篡改 Azir 的飞升致帝国覆灭） | 金色光柱、半兽神形（鹰、犬、鳄） | [通用]：ascension；[专有]：Sun Disc / Shurima | 飞升 / 渡劫——且有「渡劫失败」 |
| Aspect（星灵附体） | Targon 的星灵无实体，需要凡人宿主；被认为「配得上」的登山者才可能被附体，极罕见；宿主死后星灵回天界另找宿主 | 星灵离体宿主通常死亡；自我被淹没 | 日之金光 / 月之银光柱、星空纹身 | [通用]：avatar/host；[专有]：Targon/Aspect 体系 | 神降 / 天命之人 / 借神力 |
| Darkin（暗裔） | 堕落的飞升者，用禁忌原始魔法改造身体，后被封印在自己的武器里；武器挑选宿主，可共生也可寄生吞噬 | 宿主身体被重塑成怪物，生命力持续被抽干，耗尽后换宿主 | 血红武器、肉质缠绕手臂 | [专有] | 魔兵器灵 / 夺舍 |
| Void（虚空） | 「虚无之境」，本身无魔法，是饥饿的吞噬之力；Watchers 创造 Voidborn 作为耳目 | 被同化突变（Kai'Sa 式「适应」保留自我但身体变异） | 紫黑甲壳、裂隙、触须 | [专有] 名称；「天外虚空吞噬者」为[通用]类型（克苏鲁式） | 天外邪魔 / 域外天魔 |
| Black Mist（黑雾） | 国王 Viego 带亡妻到生命之水复活，引发 Ruination，黑雾吞没王国；死于雾中者灵魂永困；定期 Harrowing 渡海袭击生者；银、阳光、魔法可伤亡灵 | 永世不得超生 | 绿色/青灰雾、锁链、灯笼 | [专有]：Black Mist / Harrowing；[通用]：cursed isle、wraith | 鬼域 / 阴间百鬼夜行 |
| True Ice / Iceborn | 只在 Freljord 存在、永不融化的魔冰；只有 Iceborn 能驾驭 | 与 Watchers 的契约 | 蓝白冰晶弓、冰甲 | [专有] | 先天寒冰体 + 本命冰魄 |
| Petricite（禁魔石） | Demacia 用石化古树做城墙与监狱，吸收（非仅压制）魔法；供应有限 | — | 白色石材、法术打上去被吞 | [专有] 名称；「禁魔石」为[通用]类型 | 禁灵石 / 锁灵阵 |
| Hextech / techmaturgy | Piltover/Zaun 的魔法科技（符文水晶驱动），Arcane 的核心 | 失控、阶级对立 | 蓝色六角水晶、铜机械 | [专有]：Hextech；[通用]：magitech | 炼器 + 机关术（仙侠少见） |

来源：[S20][S21][S22][S23][S24][S25][S26][S27][S28][S29][S44]（Hextech 细节未打开正文，标「未核实」）

## 3. 等级 / 位阶 / 境界

### 3.1 Dota 2：单局 1–30 级（每局清零）

| 节点 | 解锁内容 | 标注 | 仙侠对应 / 差异 |
|---|---|---|---|
| Lv1 | 选定 Facet（两选一，开局前）＋天生 Innate 技能（预先激活）；学第一个技能 | [专有] 名称；「出生天赋分支」[通用] | 先天灵根属性（金/木/水…）——但 Dota 是每局重选 |
| Lv6 / 12 / 18 | 终极技能（Ultimate）1/2/3 级 | [通用]：ultimate | 每次「大境界突破」解锁/强化本命神通 |
| Lv10 / 15 / 20 / 25 | 天赋树（Talent Tree）四层，每层二选一，放弃的分支此后不可再选（7.00 规则） | [通用]：talent tree | 「道路抉择」——选了剑道就断了刀道；可做剧情两难 |
| Lv26–30 | 7.23 起上限 25→30；26–30 级所需经验 3500/4500/5500/6500/7500；满 30 级可得整棵天赋树（报道称，未见官方原文） | — | 圆满 / 大成：「两条路都走通」 |

要点：Dota 的等级是**局内临时修为**，每局从 1 级重来（参见 lore「每局都是独立时间线」的粉丝解释）。对短剧的启发是「速通一遍修行」——20–40 分钟内完成从凡人到神装的全过程。

来源：[S1][S4][S5][S6][S7]

### 3.2 Diablo：角色等级 + 满级后无限/有限巅峰

| 作品 | 角色等级上限 | 满级后成长 | 标注 | 仙侠对应 |
|---|---|---|---|---|
| Diablo II | 99（长期刷经验） | 无 | [通用] | 渡劫前的「九重天」苦熬 |
| Diablo III | 首发 60 → Reaper of Souls 70 | Paragon（1.0.4 引入时上限 100 → Paragon 2.0 取消上限，经验账号共享） | [专有]：Paragon（英文词本身通用，义为「典范」） | 「境界圆满后，修为仍可无限积累」——像「大乘期之后的无尽小层」 |
| Diablo IV | 首发 100 → 赛季 6（Vessel of Hatred）改为 60 + 账号共享 Paragon 上限 300 点、最多 5 块 Paragon Board；Lord of Hatred（2026-04）报道称上限提到 70 | Paragon Board（棋盘式节点 + Glyph 雕文，Glyph 最高 100 级） | [专有] | 「经脉/穴位图」点亮——视觉上极似打通奇经八脉 |

**天堂位阶（High Heavens）**：Anu（原初一体）→ Angiris Council（五大天使长：Malthael 智慧、Tyrael 正义、Imperius 勇气、Auriel 希望、Itherael 命运）→ 天使大军（Angelic Host，由 Crystal Arch 诞生）。全部 [专有] 名称；「五德天使议会」结构可借。
**地狱位阶（Burning Hells）**：七大魔王（Great Evils）= 三大魔王 Prime Evils（Diablo 恐惧、Mephisto 憎恨、Baal 毁灭；领域对应为常见设定，未核实正文）+ 四小魔王 Lesser Evils（Azmodan、Belial、Andariel、Duriel；部分来源以 Lilith 替换）→ 恶魔领主 → 群魔。小魔王曾政变把三大魔王流放到人间（官方 D2 剧情回顾）。全部 [专有]；「三尊四王」结构可借。
**仙侠对应**：天使议会 ↔ 天庭五方天帝；Prime Evils ↔ 三大魔尊；「下属篡位、流放旧主到人间」↔ 魔界内斗、魔尊降世。

来源：[S8][S9][S10][S11][S12][S13][S18]

### 3.3 LoL / Runeterra：游戏等级 1–18 + 设定中的「存在位阶」

游戏内英雄每局 1–18 级（未核实，为通行常识），对设定无直接意义。设定中的力量阶梯如下（本报告整理，非官方排行）：

| 位阶 | 代表 | 能做什么 | 标注 | 仙侠对应 |
|---|---|---|---|---|
| 凡人 / 战士 | Demacia 士兵、Noxus 军团 | 武艺、炼金、海克斯科技武器 | [通用] | 凡人武者 |
| 施法者（天生或苦修） | 各地法师 | 元素操控（可到物质属性层面） | [通用] | 炼气—金丹 |
| 半神 / 灵 | Freljord 半神（Ornn 锻造、Volibear 风暴、Anivia）、Ionia 精灵 | 塑造地形、受部落崇拜 | [专有] 人名；[通用] demi-god | 山神、地仙、妖神 |
| Ascended 飞升者 | Shurima 皇帝与将军 | 不朽、天界之力，可对抗虚空 | [专有] | 飞升真仙 |
| Darkin 暗裔 | 堕落飞升者 | 被封于武器、夺舍宿主 | [专有] | 堕仙 / 魔兵器灵 |
| Aspect 宿主 | 日、月、战争、守护、暮光等 | 借星灵之力；星灵本体无形 | [专有] | 神降之体 |
| Celestials / Aspects 本体 / Watchers | 宇宙层存在 | 创造 World Runes / 吞噬世界 | [专有] | 天道 / 天外天魔 |

来源：[S20][S22][S23][S24][S26][S27]

## 4. 职业 / 角色路线

### 4.1 Diablo 职业总表（力量来源最清晰的一套西幻职业库）

| 职业 | 出现作品 | 力量来源 | 资源（D3/D4） | 定位 / 视觉 | 标注 | 仙侠对应 |
|---|---|---|---|---|---|---|
| Barbarian 野蛮人 | D1 Hellfire（未核实）、D2、D3、D4 | 肉身、怒火、先祖之灵；守护圣山的部族 | Fury | 双持/巨斧、跳劈、战吼、旋风斩 | [通用] | 体修 / 炼体狂战 |
| Sorcerer / Sorceress / Wizard | D1 Sorcerer、D2 Sorceress、D3 Wizard、D4 Sorcerer | 天赋 + 学院魔法（火/冰/电/奥术） | Arcane Power / Mana | 法杖、冰甲、瞬移、陨石 | [通用] | 法修 / 五行术士 |
| Necromancer 死灵法师 | D2、D3（Rise of the Necromancer）、D4 | Rathma 祭司教团，维护生死平衡 | Essence + Corpses | 骨矛、血术、骷髅大军 | [通用] 职业；[专有] Rathma | 尸修 / 驭鬼 |
| Druid 德鲁伊 | D2 LoD、D4 | 自然灵、风暴、变身 | Spirit（D4） | 狼人/熊人化形、龙卷风、藤蔓 | [通用] | 妖修 / 化形 |
| Rogue / Amazon / Demon Hunter | D1/D4 Rogue、D2 Amazon、D3 Demon Hunter | 武艺、弓术、陷阱；DH 以仇恨驱动猎魔 | Energy（D4 Rogue）、Hatred+Discipline（DH） | 弓弩、匕首、烟雾、陷阱 | [通用]；Demon Hunter 偏专有组合词 | 暗器 / 刺客 / 游侠剑客 |
| Paladin / Crusader 圣骑士 / 十字军 | D2 Paladin、D3 Crusader、D4 Paladin（Lord of Hatred，2026） | 圣光信仰、光环（Aura） | Wrath（D3 十字军，未核实） | 重甲、盾击、光环、圣锤 | [通用] | 佛门金刚 / 正道护法（「光环」≈阵法加持） |
| Monk 武僧 | D1 Hellfire（未核实）、D3 | 内功、千神信仰 | Spirit | 拳掌、真言、瞬步 | [通用] | 武僧 / 内家拳 |
| Witch Doctor 巫医 | D3 | 灵界、巫毒、死者之灵 | Mana | 面具、蛙蛛蝇群、僵尸狗 | [通用]（有文化刻板印象风险） | 巫蛊 / 南疆巫师 |
| Assassin 刺客 | D2 LoD | 武学 + 机关陷阱，猎杀堕落法师 | — | 爪刃、影分身 | [通用] | 刺客 / 执法堂 |
| Spiritborn 灵魂之子 | D4 Vessel of Hatred（2024） | 灵界四动物守护灵 | Vigor（未核实） | 猴棍/长矛、动物幻影 | [专有] 职业名；[通用] 动物灵 | 兽魂附体 / 四象 |
| Warlock 术士 | D4 Lord of Hatred（2026） | 恶魔力量，用 Soul Shards 召唤恶魔；召唤/控制/持续伤害三路线（摘要） | — | 恶魔召唤、黑紫火 | [通用] | 魔修 / 驭魔 |

来源：[S12][S14][S17][S18][S19]（各作品资源名据 diablowiki 摘要；D1 Hellfire 职业凭记忆，未核实）

### 4.2 Dota 2：位置分工而非职业

Dota 没有职业，英雄按「Position 1–5」分工：1 号位 Carry（后期核心）、2 号位 Mid、3 号位 Offlane、4/5 号位 Support（未核实为官方术语，社区通行）。**对短剧有用的是「Carry 曲线」**：前期最弱、被保护、拿资源；后期一人碾压全场——完全等同「废柴逆袭」。

### 4.3 LoL：Riot 官方六类（Controller / Fighter / Mage / Marksman / Slayer(Assassin) / Tank，未核实正文）

更有价值的是**地区即路线**：Demacia 骑士（禁魔、重甲、正义）、Noxus 军团（力量至上、可凭武力晋升）、Ionia 武僧/忍者（与灵界和谐）、Freljord 部落（冰、野兽、母系）、Shurima 飞升者（神权帝国）、Targon 星灵宿主（登山试炼）、Shadow Isles 亡灵、Piltover/Zaun 发明家与改造人。见 §5、§8。

来源：[S20][S29][S30]

## 5. 种族

### 5.1 Diablo

| 种族 | 寿命/体型 | 力量来源 | 社会结构 | 与他族关系 | 标注 | 仙侠对应 |
|---|---|---|---|---|---|---|
| Angels 天使 | 不朽；无面、光翼、能量体 | 秩序、美德；出自 Crystal Arch | 五大天使长议会 + 天使军团 | 与恶魔永恒战争（Eternal Conflict）；对人类时庇护时漠视 | [通用] angel；[专有] 议会名 | 仙人 / 天兵天将（但缺「人修成仙」通道） |
| Demons 恶魔 | 不朽，可被打回地狱；形态多样（犄角、甲壳、肉团） | 罪与恶意；七大魔王各掌一种 | 三大四小魔王 + 恶魔领主 + 群魔 | 腐化人类，借邪教（Triune）渗透 | [通用] demon；[专有] 魔王名 | 魔族 |
| Nephalem / Humans 人类 | 普通寿命；上古 Nephalem 力量远超天使恶魔 | 天使×恶魔血脉，被 Worldstone 压制而衰减 | 王国、教团、部落 | 天地两方都想控制或抹除人类 | [专有] Nephalem；[通用] 半天使半恶魔 | 人族——「人族血脉被上界封印」 |
| Khazra（羊头人）等怪物种族 | — | 被恶魔腐化的部族（未核实） | 部落 | 敌对 | [专有] | 妖兽 / 被魔化的山民 |

### 5.2 Runeterra

| 种族 | 寿命/体型 | 力量来源 | 社会结构 / 亚种 | 与他族关系 | 标注 | 仙侠对应 |
|---|---|---|---|---|---|---|
| Humans 人类 | 普通 | 武艺、天生或修习魔法、科技 | 各地区国家 | 主导种族 | [通用] | 人族 |
| Vastaya 瓦斯塔亚 | 纯血至少约 180 岁以上，生活在时间不稳之处 | 祖先在 Ionia 对抗泰坦时吸收灵界之力，成为「不死化形者」 | 海/陆/天三类部族；如鸟形 Lhotlan、羊形 Ottrani；可变人形或兽形，变形速度取决于血脉浓度 | 与人类有共享自然魔法的古约；Noxus 入侵后人类滥用，瓦斯塔亚不满；已多代无新生 | [专有] 名称；[通用] 兽人/半兽化形 | **妖族**（化形、血脉浓淡决定能力、与人族古约）——高度对应 |
| Yordles 约德尔人 | 不老、不需呼吸，身体毁灭后精华回灵界再生 | 本身就是灵体，由魔法汇聚而生；可用幻术（glamour）伪装人形 | Bandle City 为主，入乡随俗，环境恶劣时会「失去约德尔之心」变恶 | 常被误认瓦斯塔亚；符文铁（Runic Iron）会让其失能 | [专有] | 灵 / 精怪（如山精、狐仙的「小型可爱」版） |
| Voidborn 虚空生物 | — | Watchers 赋予物质意识造出的「耳目」 | 无社会，蜂群 | 吞噬一切 | [专有] | 域外天魔 |
| Undead（Shadow Isles） | 永困 | 黑雾 | 亡灵、怨灵、被腐化的树精 | 定期袭击生者 | [通用] undead/wraith；[专有] Harrowing | 鬼族 / 阴兵 |
| Demi-gods / Spirits | 不朽 | 自然本源 | Freljord 半神被部落崇拜，Ionia 精灵无处不在 | 塑造土地 | [通用] demi-god | 山神水君、地仙 |
| Ascended / Darkin / Celestials | 不朽 | 飞升仪式 / 堕落 / 天界 | 帝国神将 / 武器囚徒 / 星界 | 见 §3.3 | [专有] | 仙 / 堕仙 / 神 |

### 5.3 Dota 2

Dota 有大量专有种族（Keen 族、Oglodi、Satyr 等，均凭记忆，未核实），多为单个英雄背景，无系统社会设定；对资料库价值低，不展开。

来源：[S10][S13][S23][S24][S25][S28][S31][S32]

## 6. 个人成长机制

| 机制 | 出处 | 运作方式 | 标注 | 仙侠对应 | 短剧用法 |
|---|---|---|---|---|---|
| 击杀经验 + 金钱滚雪球 | Dota | 补刀/击杀得金；死亡损失金钱（7.00：100 + 身价/50）；击杀赏金随连杀与等级上升（110 + 连杀 + 等级×8） | [通用] | 杀妖夺丹、越战越强 | 「连杀悬赏」：越强越被追杀，赏金越高——可做反派悬赏令 |
| 越级与反超（comeback） | Dota | 高身价英雄被杀掉金多，弱方击杀强方收益更大（据上条公式推论） | [通用] | 越级斩杀 | 「杀了他，你就拿走他半身家当」 |
| 二选一天赋 / Facet | Dota | 路线抉择不可回头 | [通用] | 道途抉择 | 关键集「选剑还是选盾」的仪式化抉择镜头 |
| Paragon 巅峰 | Diablo III/IV | 满级后继续获得巅峰点，D3 无上限、D4 有上限 300 且账号共享 | [专有] 名称 | 境界圆满后的无尽小层 / 「修为」 | 「他早就满级了，只是你们看不见他的巅峰」——隐藏实力 |
| 血脉觉醒 | Diablo（Nephalem） | 人类体内封印着天使与恶魔的双重血统，被 Worldstone 压制 | [专有] / 结构[通用] | 封印血脉、体质觉醒 | 主角被锁住的血统在危急时爆发金红双色光 |
| 灵兽契约 | D4 Spiritborn | 在灵界与四守护灵结缘，切换形态 | [通用] 结构 | 契约灵兽 / 四象 | 「四选一守护灵」可做季度换装 |
| 飞升仪式 | Runeterra（Shurima） | 被祭司选中，在太阳圆盘下接受飞升；可失败、可被篡改 | [通用] 结构 | 渡劫飞升 | 「仪式被篡改→天之骄子沦为废人」的经典开局 |
| 登山试炼 | Runeterra（Targon） | 攀登圣山，被认为配得上的人才可能被星灵附体，极罕见 | [专有] 地名；结构[通用] | 登天梯 / 问心路 | 一镜到底的登山试炼，逐级淘汰 |
| 武器夺舍 | Runeterra（Darkin） | 武器选主，共生或寄生；宿主被重塑、生命被抽干 | [专有] / 结构[通用] | 魔兵认主 / 器灵夺舍 | 「力量的代价」：每用一次，手臂多一圈血肉纹路 |
| 虚空适应 | Runeterra（Kai'Sa） | 被虚空侵蚀却保留自我，获得超能力与可见突变 | [专有] | 以魔入道 | 「我被它吃了一半，却活了下来」 |
| 学徒传承 | Runeterra（Ryze—Tyrus） | 师徒共同守护符文 | [通用] | 师门传承 | 师父牺牲、弟子接过使命 |

来源：[S1][S8][S9][S13][S17][S22][S23][S24][S28]

## 7. 道具与资源

### 7.1 Dota 2：局内「合成树」

| 层级 | 内容 | 例子（[专有] 名称） | 仙侠对应 |
|---|---|---|---|
| Consumables 消耗品 | 临时/瞬时增益，主要用于前期对线 | Tango（吃树回血）、Healing Salve、Clarity、Town Portal Scroll（传送回己方建筑） | 回血丹、回气丹、传送符 |
| Basics 基础件 | 属性、装备、杂项、Secret Shop（秘密商店，需冒险前往） | — | 低阶灵材、坊市 / 黑市 |
| Upgrades 合成装 | 基础件 + 卷轴（recipe）合成，更省格子 | Magic Wand、Bracer；Black King Bar（主动：魔免/减负面） | 法宝炼制（材料+图纸） |
| 升级器 | Aghanim's Scepter（4200 金，强化/新增技能）；Aghanim's Shard（1400 金，被动「升级现有技能或新增技能」，只能吃一次） | — | 「神通进阶灵物」——吃下后招式质变 |
| 神装 / 高风险装 | Divine Rapier：死亡即掉落，敌方可捡走并据为己有；Reincarnation/Aegis 复活不掉落 | — | 「重宝招灾」：身怀至宝被追杀，死则宝落敌手 |
| Neutral items（中立物品）Tier 1–5 | 7.38 起用 Madstone 合成，分别于 5/15/25/35/60 分钟解锁，不可跳级；由 Artifact（独特能力）+ Enchantment（属性词缀，如 Brawny 生命、Mystical 回蓝魔抗、Tough 攻击护甲）组成 | Mana Draught（T1） | 野外机缘 / 秘境奇遇——时间到了才开 |
| Roshan 掉落 | 每次击杀掉 Aegis of the Immortal（复活一次，5 分钟后失效）；第二次起掉 Cheese（回 2500 血/1500 蓝）等；第三次掉 Aghanim's Blessing / Refresher Shard（重置冷却）；掉落表随版本变化 | — | 镇守妖王 / 秘境 Boss 的「复活护身符」 |
| 背包与仓库 | 6 格装备 + 3 格背包（背包内物品不生效）+ 6 格仓库 | — | 储物戒 |

来源：[S1][S33][S34][S35][S36][S37]（Madstone 各级数量多源冲突，不采用具体数值）

### 7.2 Diablo：稀有度颜色阶梯（西方玩家最熟的「法宝品阶」）

| 品阶 | 颜色（惯例） | 词缀 | 标注 | 仙侠对应 |
|---|---|---|---|---|
| Low Quality / Normal / Superior（D2） | 白（D2 名称颜色凭记忆，官方 basics 页未列颜色，未核实） | 无或基础强化 | [通用] | 凡器 |
| Magic | 蓝 | 1–2 词缀 | [通用] | 下品法器 |
| Rare | 黄 | 多个随机词缀 | [通用] | 中品法器 |
| Set 套装 | 绿 | 集齐多件触发套装效果 | [通用] | 成套法宝 / 一套阵旗 |
| Legendary（D3/D4） | 橙 | D4：3 词缀 + 1 个传奇「威能」（Aspect，可拆入 Codex of Power 无限复用） | [通用] 品阶词；[专有] Aspect / Codex 系统名 | 上品法宝（可拆出「器魂」移植） |
| Unique | 暗金/金 | D4：4 个固定词缀 + 独特威能 | [通用] | 极品法宝 / 本命法宝 |
| Ancestral 先祖（D4） | 加星号 | 带 Greater Affix（约为普通词缀 1.5 倍）；赛季 6 起物品强度上限 800（非先祖 750） | [专有] | 「古宝」「上古遗器」 |
| Mythic Unique 神话（D4） | 紫/粉 | 词缀满值、独特威能 +30%、必为先祖 | [通用] 品阶词 | 仙器 / 神器 |
| Ethereal 虚无（D2） | 半透明 | 基础属性 +50%，耐久下降且不可修 | [通用] | 「一次性神兵」 |

**底材三档**：Normal → Exceptional → Elite（D2），可用 Horadric Cube 配方升档。（[通用] 概念）
**宝石与符文**：D2 宝石 7 种 ×5 等级（Chipped→Flawed→普通→Flawless→Perfect），3 合 1 升级；符文 El→Zod，低阶 3 合 1（El–Ort），高阶需加 Flawless 宝石（等级数 33 为常识，未核实）。
**Runeword 符文字**：在**孔数恰好相等**的白色底材中**按顺序**镶入特定符文，激活固定词条；顺序错则符文作废（如 Enigma = Jah + Ith + Ber，3 孔护甲）。D4 Vessel of Hatred 改为两枚：Ritual（条件，积累「供奉」）+ Invocation（消耗供奉触发效果）。
**Horadric Cube 赫拉迪克方块**：Act II 获得的任务物品，也是 2×2 随身空间，可「Transmute 转化」：3 宝石→高一级、3 符文→高一级、3 红 3 蓝 + 碎宝石→回春药、打孔、普通暗金升 Exceptional 底材（保留原词条）。D4 另有 Tempering（按手册追加词缀）、Masterworking（强化）。
**仙侠对应**：Runeword ↔ **阵法 / 符阵**（固定顺序的符文组合，错一步即废）；Horadric Cube ↔ **炼丹炉 / 炼器鼎**；Ritual+Invocation ↔ 「蓄势—引爆」型符箓。

来源：[S15][S16][S38][S39][S40][S41][S42][S43]

### 7.3 Runeterra：神器与材料

| 道具 | 作用 | 标注 | 仙侠对应 |
|---|---|---|---|
| World Runes | 塑造世界，可毁灭国家 | [专有] | 天道至宝 |
| Sun Disc | 飞升仪式装置 | [专有] | 飞升台 / 登仙台 |
| Darkin 武器 | 封印堕落飞升者，择主 | [专有] | 魔兵器灵 |
| True Ice 神器 | 永不融化，仅 Iceborn 可用（Ashe 的冰弓） | [专有] | 先天冰魄 |
| Petricite | 吸收魔法的石材 | [专有] | 禁灵石 |
| Runic Iron | 让约德尔人失能 | [专有] | 克制精怪的寒铁 |
| Waters of Life | 疗伤与复活之泉，被腐化后引发 Ruination | [专有] | 生命泉 / 不死泉 |
| Hextech 水晶 | 魔法科技能源（未核实细节） | [专有] | 灵石动力 |

来源：[S21][S22][S24][S25][S26][S28][S31]

## 8. 组织与社会

| 组织 | 作品 | 性质 / 运作 | 标注 | 仙侠对应 | 可借鉴冲突 |
|---|---|---|---|---|---|
| Horadrim 赫拉迪姆 | Diablo | 天使 Tyrael 组建的法师团，以 Worldstone 碎片制成的 soulstone 封印三大魔王，后衰落 | [专有]；结构「天授伏魔法师团」[通用] | 镇魔司 / 正道联盟 | 封印松动、守印者后人寥落 |
| Cathedral of Light / Triune | Diablo（Sin War） | 天堂与地狱分别扶植的人间教团，争夺人类信仰 | [专有] | 正道大宗 vs 魔教 | 两教其实都是上界傀儡 |
| Priests of Rathma | Diablo | 死灵法师教团，维持生死平衡 | [专有] | 阴阳家 / 鬼道宗 | 被世人误解为邪道 |
| Mageseekers 寻魔者 | LoL Demacia | 猎捕法师，监禁或驱逐；创始者把 Rune Wars 归咎于一切魔法；后被国王解散 | [专有]；[通用] witch hunter | 「斩妖司」/ 灭灵卫 | 主角天生灵根却生在禁魔国 |
| Illuminators | LoL Demacia | 秘密收编部分法师守边境 | [专有] | 暗卫 | 「被国家秘密利用的异类」 |
| Dauntless Vanguard | LoL Demacia | 精英骑士团 | [专有] | 禁军 / 护法 | 骑士与法师亲属的忠孝冲突 |
| Trifarix | LoL Noxus | 三人执政：Vision 谋略 / Might 武力 / Guile 诡诈；底下是军团；号称凭实力晋升 | [专有]；结构[通用] | 魔门三长老 | 「实力为尊」的帝国，平民可以打上去 |
| Black Rose 黑玫瑰 | LoL Noxus | 隐秘法师会，从暗处操纵帝国 | [专有]；[通用] secret cabal | 幕后老怪 / 隐宗 | 帝国真正的主人是谁 |
| Kinkou / Order of Shadow | LoL Ionia | 均衡派（和平、隐世）vs 影流（把魔法军事化复仇） | [专有] | 正宗 vs 叛出师门所创的分支 | 师兄弟反目、自立门户 |
| Frostguard / Avarosan / Winter's Claw | LoL Freljord | 守护深渊并篡改历史的冰卫 / 女王部族 / 掠夺部族；部落由女族长统治 | [专有] | 北地三大氏族 | 「历史被守护者篡改」 |
| Solari / Lunari | LoL Targon | 日教 / 月教 | [专有] | 日月二宗 | 姐妹被分别选为日月宿主后反目 |
| Sentinels of Light | LoL | 对抗黑雾的联盟 | [专有] | 伏魔联盟 | 跨地区组队 |
| Radiant / Dire 阵营 | Dota | 两古神的信徒与被转化的兵 | [专有] | 正邪两道 | 英雄在不同局站不同阵营（立场流动） |

来源：[S10][S11][S23][S24][S25][S28][S29][S30][S45]

## 9. 宇宙观

| 作品 | 层次 | 简述 | 仙侠对应 |
|---|---|---|---|
| Dota 2 | 原初心智 → 分裂（Schism）→ 两古神 + Zet；Mad Moon 囚笼 → 月碎（Sundering）→ 矿石落地、魔法萌生 → 古神被奉为神，凡人与诸神被卷入代理战 | 「每局一条时间线」为社区解释（[S6]） | 混沌分阴阳；天外陨石造就灵气复苏 |
| Diablo | **High Heavens**（天堂，五大天使长）／**Burning Hells**（燃烧地狱，七大魔王）／**Sanctuary 庇护所**（人间，由 Inarius 与 Lilith 用 Worldstone 创造并藏起，为逃离永恒战争）；另有 Void（Lilith 被放逐之处，同名但不同于 LoL Void）；Anu 与 Tathamet（原初神魔，据常见设定，未核实正文） | 人间本是「叛徒的避难所」，后被天地两界发现，引发 Sin War；结局为天地两界达成互不干涉人间的协定 | **三界（天界、魔界、人界）**——几乎一一对应；差异：Diablo 没有冥界轮回与「人修成仙」，人类本身就是神魔混血 |
| Runeterra | **Physical Realm**（物质界，含 Runeterra 星球）／**Spirit Realm**（灵界，Ionia 处边界最薄；约德尔人来自其独立口袋空间）／**Celestial Realm**（天界，Aspects 居于 Targon Prime「金银之城」）／**Void**（虚无之境，界外吞噬者）；死亡领域另有 Kindred、Shadow Isles 黑雾困魂 | Celestials 用 World Runes 塑造星球 | 人间 / 灵界（妖精界）/ 仙界 / 域外；Shadow Isles ↔ 鬼域 |

来源：[S6][S10][S11][S13][S20][S21][S23][S24][S25][S31]

## 10. 仙侠对照速查表

| 西幻概念（本报告出处） | 通用英文词（可直接用） | 仙侠对应 | 差异 / 注意 |
|---|---|---|---|
| Strength / Agility / Intelligence 主属性（Dota） | strength / agility / intellect build | 体修 / 剑修(身法) / 法修 | Dota 每局重选；仙侠是终身路线 |
| Universal 全能（Dota） | hybrid | 三修兼顾 | 「样样通样样松」 |
| 等级 1–30、Ultimate 6/12/18（Dota） | level, ultimate | 境界 + 大境界解锁本命神通 | 局内临时 |
| Talent tree 二选一（Dota） | talent, branch | 道途抉择 | 不可回头 |
| Facet / Innate（Dota） | innate gift | 先天灵根属性 | — |
| Paragon 巅峰（Diablo） | paragon level | 境界圆满后的修为积累 / 小层 | D3 无上限，D4 有上限 |
| Paragon Board + Glyph（D4） | skill board | 经脉穴位图 | 视觉对应极佳 |
| Consumables（Dota/Diablo） | potion, salve, elixir, scroll | 丹药、符箓 | 西方 potion 多为瓶装液体 |
| Town Portal Scroll | teleport scroll | 传送符 / 遁符 | — |
| 合成树 / recipe（Dota） | crafting recipe | 炼器图纸 + 材料 | 西方以「组合件」为主，仙侠以「火候」为主 |
| Aghanim's Scepter / Shard | upgrade relic / ability upgrade | 进阶灵物、神通升级 | 专名不可用 |
| Divine Rapier（死亡掉落） | cursed treasure that drops on death | 「怀璧其罪」重宝 | — |
| Aegis（复活护符） | resurrection charm, extra life | 替死符 / 保命玉佩 | — |
| Neutral items T1–5 | wild loot tiers | 秘境机缘（按时间开放） | — |
| 稀有度：白/蓝/黄/绿/橙/暗金/神话 | common/magic/rare/set/legendary/unique/mythic | 凡器 / 下中上品法器 / 套装法宝 / 法宝 / 本命法宝 / 仙器 | 颜色阶梯为西方玩家共识，应直接沿用 |
| Ancestral / Greater Affix | ancient / primal | 上古遗宝 | — |
| Gems 宝石 ×5 级 | chipped→perfect gem | 灵石品级（下/中/上/极品） | — |
| Runeword | runeword（偏专有，建议改称 rune sequence） | 阵法 / 符阵 | 顺序决定成败 |
| Horadric Cube 转化 | transmute, alchemy cube | 炼丹炉 / 炼器鼎 | 专名不可用 |
| Angels / High Heavens | angel, heaven | 仙人 / 天界 | 天使是「诞生」的，不是修来的 |
| Demons / Burning Hells / Prime Evils | demon lord, hell | 魔族 / 魔界 / 三大魔尊 | — |
| Nephalem / Sanctuary | demigod humans; sanctuary world | 人族血脉封印；人界 | 专名不可用 |
| Horadrim / soulstone | demon-hunting order; soul prison stone | 镇魔司；镇魔石 / 封魔塔 | — |
| Mageborn（innate magic） | born mage | 天生灵根 | — |
| Petricite / Mageseekers | anti-magic stone; witch hunters | 禁灵石；斩妖司 | — |
| Ascension（Sun Disc） | ascension | 飞升 / 渡劫 | 有失败与畸变 |
| Aspect host | avatar, divine vessel | 神降之体 | 宿主可能被吞没 |
| Darkin | sentient cursed weapon | 器灵 / 魔兵夺舍 | — |
| Void / Watchers | the void, eldritch horror | 域外天魔 | — |
| Black Mist / Harrowing | cursed mist, night of the dead | 鬼雾 / 百鬼夜行 | — |
| Vastaya | beastfolk, shapeshifter | 妖族（化形） | 血脉浓淡决定能力，对应极佳 |
| Yordles | fae folk | 精怪 | — |
| Spirit Realm（Ionia） | spirit world | 灵界 / 幽冥 | — |
| World Runes | primordial runes | 天道本源 / 先天至宝 | — |

## 11. 短剧可用性与 IP 风险

### 11.1 屏幕表现与熟悉度

| 元素 | 屏幕表现（颜色/光效/材质/动作） | 欧美观众熟悉度 | 可借鉴的爽点或冲突 |
|---|---|---|---|
| 稀有度颜色（白蓝黄绿橙金） | 掉落光柱按颜色区分，落地「叮」一声；橙/金光柱直冲天际 | **高**（游戏玩家几乎都认识「橙装」） | 「别人掉白装，他掉橙装」——一镜见高下 |
| 三属性路线 | 力量红、敏捷绿、智力蓝的气场 | 高 | 三兄弟/三弟子各走一条路 |
| 升级闪光 / 大招解锁 | 金色光环自下而上掠过全身，技能图标亮起 | 高 | 关键时刻「Level up」反杀 |
| 复活护符（Aegis 类） | 死亡后身体化光重组 | 高 | 敌人以为杀掉了，主角带着金光爬起来 |
| 死亡掉宝（Rapier 类） | 宝剑从尸体上滑落，敌我同时扑上去 | 中 | 「你杀了我，也得不到它——除非你先活过今晚」 |
| Paragon / 经脉图 | 身体浮现星图式节点，一个个点亮 | 中 | 隐藏的满级大佬，被逼出巅峰点数 |
| 符文字组合 | 符文按顺序嵌入剑身，最后一枚嵌入时整把剑「醒来」 | 中 | 顺序被反派篡改，剑反噬主人 |
| 天使/恶魔 | 无面金翼天使 vs 熔岩犄角恶魔；人间被夹在中间 | **高**（宗教基底） | 「天使也未必是好人」 |
| 禁魔王国 | 白色石墙吸走法术光，法师被关进白石牢 | 中（Arcane 带热） | 天生法师生于禁魔国——身份隐藏 + 被揭发 |
| 飞升仪式失败 | 金光柱被黑气污染，接受者变形 | 中 | 天之骄子一夜跌落，复仇主线 |
| 武器夺舍 | 血红纹路顺手臂爬上脸 | 中高 | 力量 vs 自我的拉扯 |
| 星灵附体 | 日金月银光柱从天而降 | 中 | 姐妹/挚友被选为对立星灵 |
| 黑雾亡灵 | 青绿雾气、锁链、灯笼 | 高（幽灵船/鬼岛母题） | 每月一次的「雾夜」限时生存 |

### 11.2 IP 风险

| 风险等级 | 内容 | 处理 |
|---|---|---|
| 禁用（专有名） | Dota：Radiant/Dire（作为阵营名）、Roshan、Aegis of the Immortal、Aghanim、Divine Rapier、Mad Moon、Zet、各英雄名；Diablo：Sanctuary（作为世界名）、Nephalem、Worldstone、Horadrim、Horadric Cube、Tyrael/Inarius/Lilith（Lilith 为神话名，但 Diablo 的「人类之母」设定是专有）、Prime Evils 组合及 Diablo/Mephisto/Baal 的 Blizzard 形象（Mephisto/Baal 本身来自民间传说与宗教）、Paragon Board、Spiritborn；LoL：Runeterra、Demacia、Noxus、Ionia、Freljord、Shurima、Targon、Petricite、Darkin、Voidborn、Watchers、Black Mist、Harrowing、Hextech、Vastaya、Yordle、所有英雄名 | 换名 + 换外观；不复刻标志造型（如无面天使+光翼丝带组合、海克斯蓝六角水晶） |
| 可用（通用词） | angel, demon lord, hell, heaven, paladin, necromancer, druid, barbarian, sorcerer, warlock, monk, witch doctor（注意刻板印象）, ascension, avatar, void, wraith, spirit realm, rune, runestone, gem tiers, potion, scroll of teleportation, set item, legendary, mythic, ancient, transmute | 直接使用 |
| 灰区（结构） | 「三大四小魔王」「五德天使议会」「禁魔石王国」「武器里的堕落神」「太阳圆盘飞升」 | 结构通用但组合辨识度高；需至少替换两个维度（数量、属性、视觉）再用 |

### 11.3 英雄类游戏的成长与道具设计对短剧爽点的启示

1. **把成长「数值可视化」**：Dota/Diablo 的爽感来自观众**看得见**数字在涨（等级、金钱、伤害跳字）。短剧可设一个可视化载体——掌心符文、胸口星图、武器上的刻度——每集至少亮一次，替代仙侠的「突破时灵气漩涡」。
2. **颜色就是阶级**：欧美观众天然读懂「蓝<黄<橙」。道具出场时用光色直接宣告品阶，无需台词解释。主角捡到「橙光」而反派是「黄光」，冲突瞬间成立。
3. **Carry 曲线 = 废柴逆袭**：前期被保护、被嘲笑、默默「打钱」，中期一件关键装备（Scepter 式「升级器」）让招式质变，后期一人清场。可把全剧分成「对线期—关键件—团战」三段节奏。
4. **升级器比新技能更爽**：Aghanim 的设计是「旧招吃了它就变形」——主角第 1 集就用的小招，在第 N 集被升级成大招，观众有「原来如此」的回收快感。
5. **高风险神装制造追杀**：Divine Rapier「死即掉落、敌人可捡」天然生成「怀璧其罪」剧情；Aegis 复活护符天然生成「假死反杀」。两者都是**一句话就能讲清**的规则，适合短剧。
6. **组合必须按顺序**：Runeword「顺序错即作废」把「合成」变成悬疑——谁知道正确顺序？谁偷换了一枚符文？这比仙侠阵法更易于镜头呈现（一枚一枚嵌入的特写）。
7. **满级之后还有隐藏层**：Paragon 让「大佬早已满级」仍可继续深不可测。适合「隐藏实力」型主角：表面等级顶格看似平平，巅峰点数却远超所有人。
8. **力量有价**：Darkin 夺舍、Aspect 吞没自我、Ascension 失败畸变、Ethereal「强 50% 但不能修」——每次爆发都付出可见代价，避免爽点通胀，同时给角色弧线提供燃料。
9. **立场可流动**：Dota 中同一英雄可在任一阵营，Diablo 的天使与恶魔都不是纯善纯恶——欧美观众接受「两边都在利用人类」的反转，适合「人类主角对抗上下两界」的主线（与仙侠「逆天」同构）。
10. **限时机缘**：中立物品 T1–5 按 5/15/25/35/60 分钟开放、黑雾 Harrowing 定期来袭——「到点才开」的时间锁天然制造倒计时张力，可直接映射为每集结尾的钩子。

## 12. 来源列表

访问日期均为 2026-11-08。「正文」= 用 WebFetch 打开并读取；「摘要」= 只看到搜索结果摘要；「受阻」= 打开时返回 403/402/空页面（内容取自同次搜索摘要）。

| 编号 | URL | 标题 | 状态 |
|---|---|---|---|
| S1 | https://www.dota2.com/700/gameplay | Dota 2 7.00 Gameplay Update（官方） | 正文 |
| S2 | https://bo3.gg/dota2/articles/dota-2-attribute-guide-strength-agility-and-intelligence-explained | Dota 2 Attribute Guide | 摘要 |
| S3 | https://liquipedia.net/dota2/Attributes | Liquipedia: Attributes | 受阻（403），用摘要 |
| S4 | https://www.dota2.com/outlanders | The Outlanders Update 7.23（官方） | 摘要 |
| S5 | https://www.esports.net/news/dota-2-patch-7-36-hero-facets-innate-abilities/ | Dota 2 patch 7.36 adds Hero Facets and Innate Abilities | 摘要 |
| S6 | https://www.hotspawn.com/dota2/news/dota-2-lore-explained | Dota 2 Lore Explained | 正文 |
| S7 | https://www.gosugamers.net/dota2/news/71459-dota-2-patch-7-36-brings-innate-abilities-and-facets-to-all-heroes-in-the-game | Patch 7.36 brings innate abilities and facets | 摘要 |
| S8 | https://www.pcgamer.com/diablo-3-paragon-reaper-souls | Diablo 3 2.0.1 patch will remove Paragon level cap | 摘要 |
| S9 | https://maxroll.gg/d4/news/season-6-change-log | Diablo 4 Season 6 Change Log | 摘要 |
| S10 | https://news.blizzard.com/en-gb/diablo2/23725427 | Diablo II: The story so far（官方） | 正文 |
| S11 | https://blizzardwatch.com/2019/03/08/know-lore-diablo-edition-angiris-council-fate-sanctuary | Know Your Lore: Angiris Council | 正文 |
| S12 | https://diablo-archive.fandom.com/wiki/Great_Evils | Diablo Wiki: Great Evils | 摘要 |
| S13 | https://blizzardwatch.com/2023/05/31/where-did-sanctuary-come-from/ | Where did Sanctuary come from | 摘要 |
| S14 | https://www.diablowiki.net/Resource | Diablo Wiki: Resource | 受阻（403），用摘要 |
| S15 | https://www.icy-veins.com/d4/gear-systems-and-itemization-overview | D4 Gear Systems and Itemization Overview | 受阻（403），用摘要 |
| S16 | https://thenerdstash.com/diablo-4-season-6-equipment-item-power-farming-guide-itemization-changes-explained/ | D4 Season 6 itemization changes | 摘要 |
| S17 | https://www.tweaktown.com/news/99414/diablo-4s-new-spiritborn-class-can-switch-between-jaguar-gorilla-eagle-and-centipede-powers/index.html | Spiritborn can switch between Jaguar, Gorilla, Eagle, Centipede | 摘要 |
| S18 | https://www.icy-veins.com/d4/news/diablo-4-lord-of-hatred-overview/ | Everything You Need to Know About Diablo 4: Lord of Hatred | 摘要 |
| S19 | https://www.digitalcitizen.life/diablo-4-lord-of-hatred-expansion-adds-the-paladin/ | Lord of Hatred Reveals New Classes, Including the Paladin | 摘要 |
| S20 | https://wiki.leagueoflegends.com/en-us/Universe:Runeterra | LoL Wiki: Universe:Runeterra | 正文（前 10 万字符） |
| S21 | https://wiki.leagueoflegends.com/en-us/Universe:Rune | LoL Wiki: World Rune | 正文 |
| S22 | https://wiki.leagueoflegends.com/en-us/Universe:Ascended | LoL Wiki: Ascended | 正文 |
| S23 | https://wiki.leagueoflegends.com/en-us/Universe:Aspect | LoL Wiki: Aspect | 正文 |
| S24 | https://wiki.leagueoflegends.com/en-us/Universe:Freljord | LoL Wiki: Freljord | 正文（前 10 万字符） |
| S25 | https://wiki.leagueoflegends.com/en-us/Universe:Shadow_Isles | LoL Wiki: Shadow Isles | 正文（前 10 万字符） |
| S26 | https://wiki.leagueoflegends.com/en-us/Universe:Darkin | LoL Wiki: Darkin | 正文（前 10 万字符） |
| S27 | https://wiki.leagueoflegends.com/en-us/Universe:Void | LoL Wiki: Void | 正文 |
| S28 | https://wiki.leagueoflegends.com/en-us/Universe:Ionia | LoL Wiki: Ionia | 正文（前 10 万字符） |
| S29 | https://wiki.leagueoflegends.com/en-us/Universe:Demacia | LoL Wiki: Demacia | 正文（前 10 万字符） |
| S30 | https://wiki.leagueoflegends.com/en-us/Universe:Noxus | LoL Wiki: Noxus | 正文（前 10 万字符） |
| S31 | https://wiki.leagueoflegends.com/en-us/Universe:Yordle | LoL Wiki: Yordle | 正文（前 10 万字符） |
| S32 | https://wiki.leagueoflegends.com/en-us/Universe:Vastaya | LoL Wiki: Vastaya | 正文（前 10 万字符） |
| S33 | https://esports.gg/guides/dota-2/dota-2-items-explained/ | Dota 2 items explained | 摘要 |
| S34 | https://dotacoach.gg/en/items/aghanims-shard | Aghanim's Shard – Dota 2 Guide | 正文 |
| S35 | https://dotacoach.gg/en/items/divine-rapier | Divine Rapier – Dota 2 Guide | 摘要 |
| S36 | https://bo3.gg/articles/neutral-items-guide-dota-2 | Dota 2 Neutral Items Guide | 受阻（空页面），用摘要 |
| S37 | https://hawk.live/posts/what-changed-with-roshan-and-the-tormentors-in-patch-738-dota-2 | Roshan and Tormentors in Patch 7.38 | 摘要 |
| S38 | https://classic.battle.net/diablo2exp/items/basics.shtml | Diablo II LoD: Item Basics（官方旧站） | 正文 |
| S39 | https://classic.battle.net/diablo2exp/items/cube.shtml | Diablo II LoD: Horadric Cube（官方旧站） | 正文 |
| S40 | https://StrategyWiki.org/wiki/Diablo_II:_Lord_of_Destruction/Rune_Words | Diablo II Rune Words | 摘要 |
| S41 | https://diablo2.diablowiki.net/Cube_Recipes | Horadric Cube Recipes | 摘要 |
| S42 | https://www.icy-veins.com/d4/guides/runewords-guide/ | D4 Runewords Guide | 摘要 |
| S43 | https://game8.co/games/Diablo-4/archives/408487 | Diablo 4: Vessel of Hatred（Codex/Tempering） | 摘要 |
| S44 | https://wiki.leagueoflegends.com/en-us/Magic | LoL Wiki: Magic | 摘要 |
| S45 | https://leagueoflegends.fandom.com/wiki/Lunari | LoL Fandom: Lunari | 摘要 |

**未能核实（凭记忆，正文中已标注）**：Universal 属性攻击系数；Diablo I 及 Hellfire 职业；D2 名称颜色对应（官方页未列）；D2 符文数量 33；D3 十字军资源 Wrath、D4 Spiritborn 资源 Vigor；三大魔王「恐惧/憎恨/毁灭」领域与 Anu/Tathamet 细节；Khazra 起源；LoL 等级 1–18 与 Riot 官方六大职业分类；Hextech 细节；Dota 位置 1–5 术语；Dota 种族；Lord of Hatred 等级上限 70（仅摘要）。
