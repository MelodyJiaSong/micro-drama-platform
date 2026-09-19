---
worker_id: researcher-w5-language
stage: 0
role: researcher
angle: language-customs-myths
status: complete
blockers: []
confidence: medium
fact_count_ai_read: 39
sections: ["§9 节令与习俗", "§10 语言与称谓", "§13 常见误传（本站）"]
notes: >
  全部 quote 均来自本次 curl / WebFetch 实际抓到的页面（见每条 source_url），verified_by 一律 ai_read，
  **尚无人眼核过原文页**。按 stage0 playbook「每条进 prompt 的事实必须有人眼看过的原文页」，
  §10 的「可直接引用原话清单」在进台词前必须逐条人工把 verified_by 改为 human——
  本站是系列里第一个允许 NPC 开口的站，这份清单就是台词的合法性来源，不能带着 ai_read 出片。
  逐字抓到全文的一手源：pepysdiary.com 的 Pepys 日记 1666-08-31 / 09-01 / 09-02 / 09-03 / 09-04
  与 1662-05-09；同站 in-depth 页的 Evelyn 日记 1666-09-02/03/04/06/07 全文；
  London Museum 的「Three myths about the Great Fire」与「The Great Plague of 1665」两页全文；
  Londonist 死亡人数长文全文；etymonline「curfew」词条；artinsociety.com 守夜人长文。
  pepysdiary.com 站内检索的命中计数（§10.3）是本次亲自发的查询、逐条看过命中上下文，
  是本文最硬的一类证据——它把「1666 年伦敦人说不说这个词」从直觉变成了可复核的计数。
  oed.com 需登录（302 到 SSO），OED 侧改用 etymonline + 维基 Early Modern English 词条替代，tier 相应下调。
---

# W5 · 语言 · 习俗 · 误传（sk3 伦敦 · 1666-09-01 · 大火前一夜）

> **本站的一句话结论**：1666 年的伦敦人说的是**今天听得懂的英语**，所以本站可以让具名 NPC 开口；
> 但「听得懂」不等于「可以随便编」——系列 I-7 的理由在这里换了形式仍然成立：
> **能开口，是因为有逐字记载；所以只能说有逐字记载的话。**
> 全文围绕这一条展开：§10 给「怎么说」，§10.4 给「能说哪些话」（真实原话弹药库），
> §10.5 给 TTS 读音，§9 给「那天到底是什么日子」，§13 给「模型和影视会替你编什么」。

> **⚠️ 给下游（stage1 立项 / stage4 剧本）的一条硬提醒，先说在前面**：
> 本站定在 **9 月 1 日星期六（大火前一夜）**，而**几乎所有可逐字引用的原话都在 9 月 2 日凌晨之后**。
> 9 月 1 日当天，Pepys 的日记里**一句对白都没有**（见 custom.001 的全文引录）。
> 所以「让具名 NPC 说真实原话」这条在**前一夜是落不了地的**，三个出口二选一：
> ① 把片子的时间轴推到 **9 月 2 日凌晨 1 点之后**，Bloodworth 的那句真话（lang.013-A）才成为合法弹药；
> ② 前一夜只让**无名 NPC**（摊主、船家、守夜人）开口，说的话标为**创作台词**、不冒充史料；
> ③ 前一夜用 Pepys 9 月 1 日日记里**真实发生的事**（木偶戏 → Islington 吃喝 → 一路唱着回家）做场景，
>    人物不说原话、只做原事。
> **不许**把 9 月 2 日的话搬到 9 月 1 日的嘴里——那正是本站最容易犯、也最致命的一种伪造。

---

## §10 语言与称谓（`london1666.lang.NNN`）

### 10.1 核心判断：直接说现代英语（带极少量时代词），禁仿古拼写

三条依据叠起来：

1. **1666 年处在早期现代英语的末段，其文本对今天的读者是可读的**（lang.001）。
2. **元音大推移的主体在 1400–1700 之间完成**，1666 年离今天只剩口音差，不是语言差（lang.011）。
3. **最硬的一条：Pepys 的日记本身就是 1660 年代的口语化英语**。本次逐字抓到的 1666-09-01 全文是
   「Up and at the office all the morning, and then dined at home.」——
   去掉拼写习惯，这是**今天的英语**。而 1666-09-04 那封他亲笔写给 Coventry 的信
   （"SIR, The fire is now very neere us…"）除了 `ye`＝the、`neere`＝near，句法与今天无异。

**所以本站的语言档位定为：**

| 档位 | 采用？ | 说明 |
|---|---|---|
| **A. 直接说现代英语** | ✅ **本站主档** | 主叙述、旅行者口播、大多数 NPC 对白 |
| **B. 现代英语 + 极少量时代词/称谓** | ✅ **点缀用** | 每场至多 1–2 个（`my Lord Mayor`、`Gracious Street`、`the King's baker`），做质感不做门槛 |
| **C. 仿古拼写 / 莎士比亚腔 / thee-thou 满嘴** | ❌ **本系列禁止** | 见 10.2 黑名单；也违反 CLAUDE.md「台词白话 self-check」 |

> **英文轨与中文轨的对齐**：本站英文先行。中文轨**不要**用文言/半文言去「对应」英文的时代感——
> 那会同时踩两个坑（英文没古、中文却古了）。中文轨照 CLAUDE.md 的**大白话铁律**走，
> 时代感全部由**名词**（Pudding Lane、the King's baker、curfew bell）承载，不由**语法**承载。

### 10.2 称谓白名单 / 黑名单表

**这张表可直接给 stage4 剧本 / stage6 prompt 用。**
「Pepys 命中」一列是本次对 pepysdiary.com 全日记（1660-01-01 – 1669-05-31）站内检索的命中**日记条目数**，
是本表最可复核的量尺（查询方式与原始计数见 §10.3）。

#### ✅ 白名单

| 称谓 | 用于谁 / 什么场合 | Pepys 命中 | fact |
|---|---|---|---|
| **Sir** | **默认男性敬称**，对上、对平辈、对陌生人通吃；书信开头也是它 | **2,019 条** | 006 |
| **Madam** | 有身份的女性（绅士之妻、宫廷女性）；比 Mistress 更敬 | **73 条** | 007 |
| **Mistress / Mrs.** | 已婚或有身份的城中女性（读作 "Mistress"，此时 Mrs. 是它的缩写而非独立词） | **151 条** | 007 |
| **Mr. / Master** | 有身份的男性平民（商人、书记、教区牧师）；Pepys 满篇都是 `Mr.` | 极高频 | 007 |
| **my Lord Mayor** | **市长 Bloodworth 的唯一正确叫法**；`my Lord` 单用亦可 | **64 条** | 010 |
| **his Majesty / the King** | 查理二世 | 高频 | 010 |
| **the Duke of York** | 约克公爵（后来的詹姆斯二世），火中的实际指挥者 | 高频 | 010 |
| **the King's baker** | Farriner 的身份说法（Pepys 2 Sept 原文用语） | 逐字 | 013-B |
| **Gracious Street** | 1666 年 Gracechurch Street 的**当时叫法**，Pepys 与 Evelyn 都这么写 | 逐字 | 012 |
| **Canning Street / Fanchurch Street** | Cannon St / Fenchurch St 的 1666 年写法＝当时读音 | 逐字 | 012 |

#### ⚠️ 可用但要克制

| 称谓 | 为什么打黄灯 | fact |
|---|---|---|
| **Goodman / Goody** | **是真词，但在 Pepys 笔下是「乡下人」的词**——10 处 Goody 全部出现在他父亲所在的 Brampton 乡村，3 处 goodman 也都在城外。**放进伦敦街头的摊主嘴里就是把新英格兰殖民地的口音搬到了 Cheapside。** | 008 |
| **Goodwife** | 全日记 **0 命中**。学术上确有此词（乡村/殖民地），但**没有任何伦敦 1666 的证据**。 | 008 |
| **your Worship** | 全日记 **0 个真命中**（4 个命中全是 Mrs. Worship 这个姓 + 宗教义的 worship）。对市政官/治安法官可能成立，但本次**没找到证据**，**不进台词**。 | 009 |
| **prithee** | 词典上 17 世纪确实常见（复辟喜剧里很多），但 **Pepys 全日记 0 命中**（prithee / prethee 各 0）。它是**戏台词**不是**街头话**。 | 005 |

#### ❌ 黑名单（影视最常塞进 17 世纪英语的错误货色）

| 错误货色 | 为什么错 | fact |
|---|---|---|
| **thee / thou / thy / thine 当日常** | 到 1650 年 thou 已经「显得过时或书面」；Pepys 全日记 thou 只 5 处、thee 只 6 处，而且**全在特殊语域**：临终私语、街头咒骂式喊话、驱痉挛的**咒语**、圣经引文。**1666 年的伦敦人日常不说 thou。** | 002 / 003 |
| **用 thou 表示「亲切」或「古味」** | 1666 年它的实际语用是**羞辱 / 拉平地位**。Pepys 1663/64 年 1 月 11 日直接把它动词化：`and thou'd him all along`——「一路 thou 他」＝一路不给他体面。 | 003 |
| **让随便一个路人满口 thee/thou** | 1666 年成系统地对所有人 thee/thou 的，是**贵格会**。他们正因此被起诉（Quakers Act 1662 / Conventicle Act 1664）。让一个摊主这么说话＝无意中把他写成了正在被通缉的异见者。 | 004 |
| **prithee / verily / forsooth / methinks 堆砌** | 莎士比亚腔／戏台腔，不是 1666 的街头英语（见 ⚠️ 表）。 | 005 |
| **维多利亚式客套**（"I do declare"、"my dear lady"、"I should be much obliged"） | 差 200 年。 | 002 |
| **美式用语**（"gotten"、"sidewalk"、"I guess"、"okay"、"folks"、"Goodwife" 当街头称呼） | 美式/殖民地色彩；`Goodwife`/`Goody` 的影视印象来自塞勒姆题材。 | 008 |
| **"Gracechurch Street"** | **1666 年它还叫 Gracious Street**，Gracechurch 这个拼法要到火后重建才通行。 | 012 |
| **"Sire"** | 法式/奇幻剧用语，英格兰对查理二世是 `your Majesty` / `Sir`。 | 006 |
| **仿古拼写进台词或字幕**（`ye olde`、`doth`、`hath` 当口语） | 本系列明令禁止；`hath`/`doth` 在 Pepys 的**书面**里有，在台词里没有理由。 | 001 |

### 10.3 白/黑名单的量化依据（可复核）

本次对 `https://www.pepysdiary.com/search/?q=<term>`（scope = diary entries）逐词发查询，
命中数是「包含该词的日记条目数」，覆盖 1660–1669 全本日记：

| 查询词 | 命中条目数 | 命中的实际语境（逐条看过） |
|---|---|---|
| `Sir` | **2,019** | 默认敬称，遍布全书 |
| `pray you` | **163** | 「请你…」的**当时标准说法**——要礼貌请求用这个，不要用 prithee |
| `Mistress` | **151** | 城中女性 |
| `Madam` | **73** | 更高身份的女性 |
| `my Lord Mayor` | **64** | 市长 |
| `Goody` | **10** | **全部在 Brampton 乡下**：Goody Gorum、Goody Mulliner、Goody Best "a little out of the towne" |
| `thee` | **6** | 圣经/布道引文（"Woe unto thee"、"blessed is the womb that bare thee"）+ 临终私语 |
| `thou` | **5** | 临终私语、街头喊话、**驱痉挛咒语**、`thou'd him`（羞辱） |
| `your Worship` | **4** | **0 个真命中**（Mrs. Worship 这个姓 3 处、宗教义 worship 1 处） |
| `Goodman` | **3** | "old goodman Taylor"（他家花园的老头）、"goodman Arthur"（城外路上遇到）、"Mr. Goodman"（姓） |
| `Goodwife` | **0** | — |
| `prithee` | **0** | — |
| `prethee` | **0** | — |

**这张表本身就是本节的核心产出**：它把「1666 年伦敦人会不会这么说」从审美判断变成了计数。
下游若想新增一个称谓，**照同样的方式查一次再加**，不要凭印象。

### 10.4 可直接引用的真实原话清单（本站 NPC 台词的合法弹药库）

> **使用规则（必须逐条遵守）**：
> **A. 具名真实历史人物（Bloodworth / Pepys / Evelyn / Farriner）只念本表里有的话。**
> 本表之外的一个字都不许安在他们嘴里。
> **B. 每条标了日期/时刻的，只能在该时刻之后的镜里出现。**
> **C. 「转述」一列标 ✅ 的才是逐字直接引语；标 ⚠️ 的是 Pepys 的间接转述——
> 那是他在复述别人的意思，不是那个人的原话，改写成直接引语就等于伪造。**

#### A. 唯一一句火灾中的逐字直接引语 —— 市长 Bloodworth（1666-09-02 中午前，Canning Street）

| # | 原话（逐字） | 直接引语？ | 出处 |
|---|---|---|---|
| A1 | **"Lord! what can I do? I am spent: people will not obey me. I have been pulling down houses; but the fire overtakes us faster than we can do it."** | ✅ | Pepys 日记 1666-09-02 |

Pepys 对他当时状态的描写（可做导演提示、可做旁白，**不可做他的台词**）：
`like a man spent, with a handkercher about his neck` / `he cried, like a fainting woman`。
Pepys 还补了一句转述：`That he needed no more soldiers; and that, for himself, he must go and refresh himself, having been up all night.`（⚠️ 转述，非原话）

> **这是全片最贵的一句台词。** 它同时满足系列 sk3 的两条分型不变量：
> I-5①「允许试着说一句并失败——且只在失败本身有史料记载时才做」，与
> I-15「允许一道边界与一次越界」。**旅行者越过阶级边界见到市长、说了一句、市长崩溃地回了这一句、
> 然后城还是烧了**——这是有据可依的完整戏剧动作，不需要编任何一个字。

#### B. 转述（⚠️ 不可改写成直接引语，只能做旁白或字卡）

| # | 内容 | 出处 |
|---|---|---|
| B1 | 女仆 Jane 凌晨三点把 Pepys 夫妇叫起来，说城里烧起来了 —— 原文 `Jane called us up about three in the morning, to tell us of a great fire they saw in the City.` **Jane 没有任何逐字原话留下。** | Pepys 09-02 |
| B2 | Jane 稍后再报：`she hears that above 300 houses have been burned down to-night by the fire we saw, and that it is now burning down all Fish-street, by London Bridge.` | Pepys 09-02 |
| B3 | 伦敦塔副官告诉 Pepys：`it begun this morning in the King's baker's house in Pudding-lane, and that it hath burned St. Magnus's Church and most part of Fish-street already.` | Pepys 09-02 |
| B4 | Pepys 对国王说的话（转述）：`unless his Majesty did command houses to be pulled down nothing could stop the fire.` | Pepys 09-02 |
| B5 | 国王的命令（转述）：`the King commanded me to go to my Lord Mayor from him, and command him to spare no houses, but to pull down before the fire every way.` | Pepys 09-02 |
| B6 | 商人 Isaake Houblon 在 Dowgate 自家门口收兄弟们的家当，说已经搬过两次了 —— `and, as he says, have been removed twice already` | Pepys 09-02 |

#### C. Pepys 自己的第一人称句（可做旁白 / OS / 字卡，**不可安给别人**）

| # | 原话（逐字） | 出处 |
|---|---|---|
| C1 | `Up and at the office all the morning, and then dined at home. Got my new closet made mighty clean against to-morrow.` | **09-01（本站当天！）** |
| C2 | `and so, the play being done, we to Islington, and there eat and drank and mighty merry; and so home singing` | **09-01（本站当天！）** |
| C3 | `Everybody endeavouring to remove their goods, and flinging into the river or bringing them into lighters that layoff` | 09-02 |
| C4 | `the poor pigeons, I perceive, were loth to leave their houses, but hovered about the windows and balconys till they were, some of them burned, their wings, and fell down.` | 09-02 |
| C5 | `And to see the churches all filling with goods by people who themselves should have been quietly there at this time.` | 09-02 |
| C6 | `all over the Thames, with one's face in the wind, you were almost burned with a shower of firedrops.` | 09-02 |
| C7 | `in a most horrid malicious bloody flame, not like the fine flame of an ordinary fire` | 09-02 |
| C8 | `we saw the fire as only one entire arch of fire from this to the other side the bridge, and in a bow up the hill for an arch of above a mile long: it made me weep to see it.` | 09-02 |
| C9 | `the streets full of nothing but people and horses and carts loaden with goods, ready to run over one another` | 09-02 |
| C10 | `Sir W. Batten not knowing how to remove his wine, did dig a pit in the garden, and laid it in there… and I my Parmazan cheese, as well as my wine and some other things.` | 09-04 |
| C11 | **1666 年的书面英语实样（整封信）**：`SIR, The fire is now very neere us as well on Tower Streete as Fanchurch Street side, and we little hope of our escape but by this remedy, to ye want whereof we doe certainly owe ye loss of ye City namely, ye pulling down of houses, in ye way of ye fire.` | Pepys 致 Coventry 函，09-04 |
| C12 | **守夜人的实录（1663）**：`this morning, about two or three o'clock, [I was] knocked up in our back yard, and rising to the window, being moonshine, I found it was the constable and his watch, who had found our back yard door open, and so came in to see what the matter was. So I desired them to shut the door, and bid them good night, and so to bed again` | Pepys 1663（经 artinsociety 转引） |

#### D. Evelyn 的句子（第二个可具名的目击者，可做对位旁白）

| # | 原话（逐字） | 出处 |
|---|---|---|
| D1 | `This fatal night about ten, began that deplorable fire, neere Fish-streete in London.` ⚠️ **Evelyn 把起火时刻记成了「约十点」，与 Pepys 的凌晨三点、以及主流认定的午夜后起火不符——引用时不要当计时依据。** | Evelyn 09-02 |
| D2 | `the whole Citty in dreadfull flames neere the Water side` | Evelyn 09-02 |
| D3 | `God grant mine eyes may never behold the like` | Evelyn 09-03 |
| D4 | `o the miserable & calamitous speectacle, such as happly the whole world had not seene the like since the foundation of it` | Evelyn 09-03 |
| D5 | **`London was, but is no more.`** ← 全片最强的一句 closer 候选 | Evelyn 09-03 |
| D6 | `the stones of Paules flew like granados, the Lead mealting down the streetes in a streame, & the very pavements of them glowing with a fiery rednesse` | Evelyn 09-04 |
| D7 | `the shreeking of Women & children, the hurry of people, the fall of towers, houses & churches was like an hideous storme` | Evelyn 09-03 |

### 10.5 TTS 专名读音表

> 直接给配音用。「陷阱」一列标 ⛔ 的是**一定会读错**的，必须在 TTS 里写死读音或改用音标输入。
> 「1666 写法」一列非空的，说明**当时的拼法就是当时的读法**，比现代拼法更接近片中人物的嘴。

| 专名 | IPA | 英文重拼（给 TTS） | 陷阱 | 1666 写法 | 依据 |
|---|---|---|---|---|---|
| **Pepys** | /ˈpiːps/ | **PEEPS** | ⛔ 绝不读 "PEP-iss" / "PEP-eez" | Pepys | 维基 Samuel Pepys 词条 IPA 模板 `p\|iː\|p\|s` |
| **Thames** | /tɛmz/ | **TEMZ** | ⛔ 绝不读 "THAYMZ"；`th` 不发 θ | Thames | 维基 River Thames 词条 `t\|ɛ\|m\|z`，respell `TEMZ` |
| **Southwark** | /ˈsʌðək/ | **SUDH-uk** | ⛔ 绝不读 "SOUTH-wark" | Southwarke | 维基 Southwark 词条 `ˈ\|s\|ʌ\|ð\|ə\|k`，respell `SUDH-ək` |
| **Holborn** | /ˈhəʊbən/ | **HOH-bun** | ⛔ `l` 不发音（亦有 HOHL-bərn 读法） | Holborn | 维基 Holborn 词条 `ˈ\|h\|əʊ\|b\|ər\|n` |
| **Evelyn**（人名） | /ˈiːvlɪn/ | **EEV-lin** | ⛔ 绝不读 "EV-uh-lin"（那是现代女名） | Evelyn | ⚠️ 搜索摘要，未逐字抓页；进片前建议人工二核 |
| **Bloodworth** | /ˈblʌdwɜːθ/ | **BLUD-wurth** | 不读 "BLOOD-worth"（长 oo） | **Bludworth**（Pepys 拼法） | 维基 Thomas Bloodworth；Pepys 09-02 注文作 `Sir Thomas Bludworth` |
| **Farriner** | /ˈfærɪnə/ | **FARR-in-er** | 拼法多变，读音统一 | Faryner / Farynor / Faynor | ⚠️ 搜索摘要；Pepys 本人只写 `the King's baker's house` |
| **Pudding Lane** | /ˈpʊdɪŋ leɪn/ | **PUD-ing LAYN** | 规则读音 | Pudding-lane | Pepys 09-02 逐字 |
| **St Magnus** | /seɪnt ˈmæɡnəs/ | **saint MAG-nuss** | 规则读音 | St. Magnus's Church | Pepys 09-02 逐字 |
| **Cheapside** | /ˈtʃiːpsaɪd/ | **CHEEP-side** | 不是 "cheap"（便宜）而是古英语 cēap＝市场 | Cheape side | Pepys / Evelyn 逐字 |
| **Wren** | /rɛn/ | **REN** | `W` 不发音 | Wren | 规则读音 |
| **Gracious Street** | /ˈɡreɪʃəs striːt/ | **GRAY-shus STREET** | ⛔ **1666 年不叫 Gracechurch** | Gracious Streete | Evelyn 09-03 逐字；MoEML / 维基 Gracechurch Street |
| **Cannon Street** | /ˈkænɪŋ striːt/ | **KAN-ing STREET**（当时音） | 现代读 KAN-un | **Canningstreet**（Pepys） | Pepys 09-02 逐字 |
| **Fenchurch Street** | /ˈfænʃɜːtʃ/（当时音） | **FAN-church** | 现代 FEN-church | **Fanchurch Street**（Pepys 亲笔信） | Pepys 09-04 函逐字 |
| **Islington** | /ˈɪzlɪŋtən/ | **IZ-ling-tun** | `s` 读 /z/ | Islington | Pepys 09-01 / Evelyn 09-07 逐字 |
| **Moorfields** | /ˈmɔːfiːldz/ | **MORE-feeldz** | 规则 | Moore filds（Evelyn） | Evelyn 09-04 逐字 |
| **Billingsgate** | /ˈbɪlɪŋzɡeɪt/ | **BIL-ingz-gayt** | 规则 | Billingsgate | 常见 |
| **Ludgate / Newgate / Aldersgate** | /-ɡeɪt/ 或弱读 /-ɡɪt/ | **-GAYT** | 伦敦老派弱读为 -git，本片统一用 -GAYT | Ludgate 等 | Evelyn 09-04 / 09-07 逐字 |
| **Bankside** | /ˈbæŋksaɪd/ | **BANK-side** | 规则 | bank side（Evelyn） | Evelyn 09-02 逐字 |
| **Whitehall** | /waɪtˈhɔːl/ | **wyte-HAWL** | 重音在后 | White Hall | Pepys 09-02 逐字 |
| **Queenhithe** | ⚠️ 未核 | ⚠️ 未核 | ⛔ **本次未查到可靠读音，进片前必须补核**，不要让 TTS 自由发挥 | Queenhith（Pepys） | Pepys 09-02 逐字（仅拼法） |

### 10.6 §10 fact 清单

```yaml
- fact_id: london1666.lang.001
  claim: 1666 年的英语属早期现代英语末段；该阶段文本对今天的读者是可理解的，因此本站 NPC 直接说现代英语即可，不需要也不允许仿古拼写
  tag: ✅
  source: Wikipedia「Early Modern English」；佐以 Pepys 1666-09-01 与 1666-09-04 日记/书信原文的可读性
  source_url: https://en.wikipedia.org/wiki/Early_Modern_English ; https://www.pepysdiary.com/diary/1666/09/01/ ; https://www.pepysdiary.com/diary/1666/09/04/
  quote: "Most modern readers of English can understand texts written in the late phase of early modern English, such as the King James Bible and the works of William Shakespeare"（维基）／实样："Up and at the office all the morning, and then dined at home."（Pepys 1666-09-01 全句）
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "台词一律现代英语，句法与今天无异；时代感只由名词承担"
  negative: "仿古拼写、ye olde、doth/hath 当口语、莎士比亚腔、字幕用古体拼写"

- fact_id: london1666.lang.002
  claim: 到 1650 年 thou 已显得过时或书面；在 Pepys 1660–1669 全本日记中 thou 仅 5 条命中、thee 仅 6 条，且全部落在圣经引文、临终私语、咒语、羞辱等特殊语域，不是 1666 年伦敦的日常用语
  tag: ❌
  source: Wikipedia「Early Modern English」§ Pronouns；pepysdiary.com 站内全日记检索（本次亲查）
  source_url: https://en.wikipedia.org/wiki/Early_Modern_English ; https://www.pepysdiary.com/search/?q=thou ; https://www.pepysdiary.com/search/?q=thee
  quote: "by 1650, 'thou' seems old-fashioned or literary. It has effectively completely disappeared from Modern Standard English."（维基）／检索结果："Searching for thou, in diary entries … Five found." / "Searching for thee … Six found."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "所有对白用 you / your，不出现 thee / thou / thy / thine"
  negative: "thee、thou、thy、thine、ye（第二人称）、doth、hath、art thou"

- fact_id: london1666.lang.003
  claim: 1666 年前后对人用 thou 的实际语用是羞辱或拉平地位，而非亲昵或古雅；Pepys 直接把它动词化写作「thou'd him」
  tag: ❌
  source: Pepys 日记 1663/64-01-11（经 pepysdiary.com 检索命中上下文）
  source_url: https://www.pepysdiary.com/search/?q=thou
  quote: "…words, \"O King!\" and thou'd him all along."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "若确需表现冒犯，可用一次 thou——它在 1666 年等于当面不给体面"
  negative: "用 thou 表示亲切、温柔、古雅或敬意"

- fact_id: london1666.lang.004
  claim: 1666 年成系统地对所有人使用 thee/thou 的群体是贵格会（以此主张人人平等），而他们正因宗教不从被 Quakers Act 1662 / Conventicle Act 1664 起诉；因此让一个普通伦敦摊主满口 thee/thou，等于把他写成了正在被通缉的异见者
  tag: ⚠️
  source: QuakerSpeak「The History of Quaker Plain Speech」；Quaker Theology「Resisting Oppression: Friends and the Stuart Restoration, 1660-1689」；Wikipedia「Quakers Act 1662」
  source_url: https://quakerspeak.com/video/history-quaker-plain-speech/ ; https://quakertheology.org/quakers-and-stuart-restoration/ ; https://en.wikipedia.org/wiki/Quakers_Act_1662
  quote: "By consistently using 'thee' and 'thou' to all people regardless of status, Quaker plain language reflected their convictions about social equality."／"The Restoration in 1660 brought twenty-four years of occasional persecution…"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "thee/thou 只留给明确写成贵格会的角色；他同时不脱帽"
  negative: "普通市民、摊主、船家、守夜人满口 thee/thou"

- fact_id: london1666.lang.005
  claim: prithee 在 17 世纪的戏剧文本里常见（源自 I pray thee，1577 年首见），但在 Pepys 全本日记中 prithee / prethee 命中均为 0；相对地「pray you」有 163 条命中，是当时表达礼貌请求的实际说法
  tag: ⚠️
  source: etymonline「prithee」（经搜索摘要）；pepysdiary.com 站内全日记检索（本次亲查）
  source_url: https://www.etymonline.com/word/prithee ; https://www.pepysdiary.com/search/?q=prithee ; https://www.pepysdiary.com/search/?q=pray+you
  quote: "The earliest recorded appearance of the word prithee listed in the Oxford English Dictionary is from 1577, while it is most commonly found in works from the seventeenth century."／检索："Searching for prithee, in diary entries … Nothing was found." / "pray you … 163 found."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "礼貌请求说 \"pray you\" 或直接说现代英语 please，不说 prithee"
  negative: "prithee、prethee、verily、forsooth、methinks（当口语）"

- fact_id: london1666.lang.006
  claim: Sir 是 1666 年伦敦男性敬称的绝对默认值，口语与书信通用；Pepys 全日记 2,019 条含之，且他 1666-09-04 写给 Coventry 的亲笔信正是以「SIR,」开头
  tag: ✅
  source: pepysdiary.com 站内全日记检索；Pepys 致 Sir W. Coventry 函（1666-09-04 日记附录，Pepys MSS 手稿）
  source_url: https://www.pepysdiary.com/search/?q=Sir ; https://www.pepysdiary.com/diary/1666/09/04/
  quote: "Searching for Sir, in diary entries … 2,019 found."／"SIR, The fire is now very neere us as well on Tower Streete as Fanchurch Street side…"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "陌生男子、上级、平辈一律 Sir；书信开头 SIR,"
  negative: "Sire、my liege、good sir knight、Mister（单用称呼陌生人）"

- fact_id: london1666.lang.007
  claim: 女性称谓按身份分层——Madam（更高身份，73 条）、Mistress/Mrs.（城中已婚或有身份女性，151 条）；男性平民用 Mr./Master。当时 Mrs. 是 Mistress 的缩写而非独立读法
  tag: ✅
  source: pepysdiary.com 站内全日记检索；Wikipedia「Mistress (form of address)」「Goodman (title)」
  source_url: https://www.pepysdiary.com/search/?q=Madam ; https://www.pepysdiary.com/search/?q=Mistress ; https://en.wikipedia.org/wiki/Mistress_(form_of_address)
  quote: "Searching for Madam … 73 found." / "Searching for Mistress … 151 found."／"'Mr.' or 'Master' was an honorific title used for gentlemen, professional men and substantial citizens … while their wives would be referred to as 'Mrs.' or 'Mistress.'"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "对城中女性说 Mistress；对有身份女性说 Madam；对男性平民说 Mr."
  negative: "Miss（此时未定型）、Ma'am（更晚）、Lady（乱用）"

- fact_id: london1666.lang.008
  claim: Goodman / Goody / Goodwife 在 1666 年的伦敦不是街头称谓——Pepys 全日记 Goody 10 条全部出现在他父亲所在的 Brampton 乡村，goodman 3 条也都在城外或是姓氏，Goodwife 0 条；把它放进 Cheapside 摊主嘴里是把新英格兰殖民地口音搬到了伦敦
  tag: ⚠️
  source: pepysdiary.com 站内全日记检索（逐条看过命中上下文）；Wikipedia「Goodwife」「Goodman (title)」给出的社会等级说明
  source_url: https://www.pepysdiary.com/search/?q=Goody ; https://www.pepysdiary.com/search/?q=Goodman ; https://www.pepysdiary.com/search/?q=Goodwife ; https://en.wikipedia.org/wiki/Goodwife
  quote: 命中上下文："at Goody Gorum's" / "Goody Mulliner over against the College" / "one Goody Best's, a little out of the towne" / "old goodman Taylor puts his brooms and dirt" / "by direction of one goodman Arthur, whom we met on the way"；"Goodwife … Nothing was found."／维基："a man addressed by this title was of a lesser social rank than a man addressed as 'Mister.'"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "伦敦街头 NPC 一律 Sir / Mistress / Mr.；Goody 只留给明确写成乡下来的角色"
  negative: "Goodwife、Goody、Goodman（作为伦敦市内的日常称呼）"

- fact_id: london1666.lang.009
  claim: 「your Worship」在 Pepys 全日记中无任何作为称谓的真命中（4 条命中全是 Mrs. Worship 这个姓与宗教义的 worship）；本次未找到 1666 年伦敦街头使用它的证据，故不进台词
  tag: ⚠️
  source: pepysdiary.com 站内全日记检索（逐条看过 4 条命中）
  source_url: https://www.pepysdiary.com/search/?q=your+Worship
  quote: "Searching for your Worship, in diary entries … Four found."；4 条分别为 "Mrs. Worship's daughter"、"Mrs. Worship did give us three or four very good songs"、"their particular worship"、"things illegal in the worship of God"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "对市长与官员用 my Lord / my Lord Mayor / Sir，不用 your Worship"
  negative: "your Worship、your Honour、milord（拼写）"

- fact_id: london1666.lang.010
  claim: 市长 Thomas Bloodworth 的正确称呼是「my Lord Mayor」（Pepys 全日记 64 条命中，且 1666-09-02 原文两次这样称他）；国王称 his Majesty / the King，约克公爵称 the Duke of York
  tag: ✅
  source: Pepys 日记 1666-09-02；pepysdiary.com 站内检索
  source_url: https://www.pepysdiary.com/diary/1666/09/02/ ; https://www.pepysdiary.com/search/?q=my+Lord+Mayor
  quote: "the King commanded me to go to my Lord Mayor from him"／"At last met my Lord Mayor in Canningstreet, like a man spent, with a handkercher about his neck."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "称市长为 my Lord Mayor；称国王为 his Majesty"
  negative: "Mayor Bloodworth（美式）、Mr. Mayor、your Worship"

- fact_id: london1666.lang.011
  claim: 元音大推移主要发生在 1400–1700 之间，1666 年处在其尾段；这意味着 1666 年伦敦人与今人的差别主要是口音而非语言，现代观众听得懂
  tag: ✅
  source: Wikipedia「Great Vowel Shift」；Wikipedia「Early Modern English」；David Crystal 原声复原（Original Pronunciation）研究的通行结论
  source_url: https://en.wikipedia.org/wiki/Great_Vowel_Shift ; https://en.wikipedia.org/wiki/Early_Modern_English
  quote: "The Great Vowel Shift took place primarily between 1400 and 1700"／"Shakespeare's plays are therefore still familiar and comprehensible 400 years after they were written, but the works of Geoffrey Chaucer and William Langland, which had been written only 200 years earlier, are considerably more difficult for the average modern reader."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "配音用现代英式发音即可，不做原声复原（OP）实验"
  negative: "刻意做 17 世纪重构口音、爱尔兰/西部乡音冒充古音、假伦敦腔"

- fact_id: london1666.lang.012
  claim: 1666 年 Gracechurch Street 的当时名称是「Gracious Street」，Pepys 与 Evelyn 都这样写；Gracechurch 这一拼法要到大火后重建才通行。同理 Cannon Street 当时写作 Canningstreet、Fenchurch Street 写作 Fanchurch Street
  tag: ✅
  source: Evelyn 日记 1666-09-03；Pepys 日记 1666-09-02 与 1666-09-04 函；MoEML / Wikipedia「Gracechurch Street」
  source_url: https://www.pepysdiary.com/indepth/2009/09/02/evelyns-fire/ ; https://www.pepysdiary.com/diary/1666/09/02/ ; https://en.wikipedia.org/wiki/Gracechurch_Street
  quote: Evelyn："Tower-Streete, Fen-church-streete, Gracious Streete, & so along to Bainard Castle"／Pepys："At last met my Lord Mayor in Canningstreet"／Pepys 函："as well on Tower Streete as Fanchurch Street side"／维基："'Gracechurch' not used until after the destruction of the street in the Great Fire of London in 1666."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "片中街名说 Gracious Street / Canning Street；字卡可注现名"
  negative: "1666 场景中出现 Gracechurch Street 这一名称"

- fact_id: london1666.lang.013
  claim: 大火期间 Pepys 日记里唯一一句逐字直接引语出自市长 Bloodworth（1666-09-02 于 Canning Street）；其余人物的话（女仆 Jane、伦敦塔副官、国王、Houblon）全部是 Pepys 的间接转述，没有原话留下
  tag: ✅
  source: Pepys 日记 1666-09-02 全文（本次逐字抓取）
  source_url: https://www.pepysdiary.com/diary/1666/09/02/
  quote: "To the King's message he cried, like a fainting woman, \"Lord! what can I do? I am spent: people will not obey me. I have been pulling down houses; but the fire overtakes us faster than we can do it.\""
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "具名真实人物只念此清单内的原话；转述内容只做旁白，绝不改写成直接引语"
  negative: "给 Jane / Farriner / 国王 / 伦敦塔副官编造直接台词；把转述改写成引号内的话"

- fact_id: london1666.lang.014
  claim: 本站定在 9 月 1 日（大火前一夜），而全部可逐字引用的原话都在 9 月 2 日凌晨之后；9 月 1 日的 Pepys 日记全文中没有任何对白
  tag: ⚠️
  source: Pepys 日记 1666-09-01 全文（本次逐字抓取，全文仅一段，无引号）
  source_url: https://www.pepysdiary.com/diary/1666/09/01/
  quote: 全文："Up and at the office all the morning, and then dined at home. Got my new closet made mighty clean against to-morrow. Sir W. Pen and my wife and Mercer and I to 'Polichinelly,' but were there horribly frighted to see Young Killigrew come in with a great many more young sparks; but we hid ourselves, so as we think they did not see us. By and by, they went away, and then we were at rest again; and so, the play being done, we to Islington, and there eat and drank and mighty merry; and so home singing, and, after a letter or two at the office, to bed."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "前一夜镜次：具名人物只做原事（看木偶戏、去 Islington 吃喝、唱着回家），不说原话"
  negative: "把 9 月 2 日的台词提前到 9 月 1 日；让 Bloodworth 在前一夜说出那句崩溃的话"
```

---

## §9 节令与习俗（`london1666.custom.NNN`）

### 9.1 那两天到底是什么日子

| 项 | 内容 |
|---|---|
| **1666-09-01** | **星期六**。Pepys 日记全文见 lang.014：上午办公、家里吃饭、把新书房收拾干净准备明天（他明天要请客）、下午带妻子和 Mercer 去看 **Polichinelly（木偶戏）**、演完去 **Islington 吃喝**、**一路唱着回家**。**这是本站可以完全照搬的一夜。** |
| **1666-09-02** | **星期日（主日）**。Pepys 原文第一个词就是 `(Lord's day)`。火在午夜后于 Pudding Lane 的**国王御用面包师**家中起。**很多人本该在做礼拜，实际在往教堂里搬家当**——Pepys 那句 `And to see the churches all filling with goods by people who themselves should have been quietly there at this time.` 就是这场景的原始注脚。 |
| **强制礼拜** | 复辟后 Act of Uniformity 1662 确立国教统一；主日到本教区礼拜为义务，无正当理由缺席罚 **12 便士**（该罚则沿自伊丽莎白时期《统一法令》，1666 年仍有效）。 |
| **天气** | **反常的炎热与长期干旱 + 强劲东风**。Pepys：`after so long a drought`、`the wind mighty high`；Evelyn：`in a very drie season`、`a fierce Eastern Wind`、`a long set of faire & warme weather`。 |

### 9.2 瘟疫：刚过去，但没过干净

**这是本站气氛设计的关键，也是最容易做错的一节。**

- 1665 年大瘟疫已过峰值，**1665 年冬天起死亡数持续下降**。
- **1666 年 2 月国王认为伦敦已安全，带朝廷回城**；乡绅随之回流，法院、商贸、作坊陆续恢复。
- 但**没有干净的终点**：1666 全年仍有约 1,800 例瘟疫下葬，零星病例延续到 1666 年 9 月，此后数年仍偶见于死亡周报。
- **因此 1666 年 9 月 1 日的伦敦是「刚缓过来、人正在回来、但每个人都记得去年」的城**——
  这是本站情绪的底色：**不是废墟，也不是太平，是劫后返场**。
- **但 1665 年那套画面（封门红十字、夜间死人车、"Bring out your dead"、宵禁禁夜行）是去年的事**，
  写进 1666 年 9 月的街头就是错位一年（详见 myth.004）。

### 9.3 夜里的声音：宵禁钟 + 守夜人

**这是本站质量最高的一个「片中知识点」，词源经查为真：**

- **curfew ← 盎格鲁-法语 coeverfu ← 古法语 cuevrefeu，字面「盖火」**（cuevre = covrir 的命令式「盖」+ feu「火」）。
  14 世纪初进入英语，义为「在固定时刻敲钟的晚间信号」。
  **中世纪的做法是在晚上八点或九点敲钟，命令把炉火压好、准备就寝，目的正是防止无人看管的炉火酿成大火。**
  「限制出行」这层现代义要到 1800 年代才发展出来。
- **→ 片中的钩子**：**这个词本来的意思就是「把火盖上」，是专门为了防止今晚这种事而发明的。**
  这句在 9 月 1 日夜里说出来，和次日凌晨 Pudding Lane 的火炉形成对位——**免费的、真的、不需要编。**
- **伦敦的那口钟**：St Mary-le-Bow（Bow Bells）自 1469 年起由市议会令**每晚九点**鸣宵禁，
  同时标志学徒收工、城门关闭、炉火覆盖。**这座教堂本身在大火中被烧毁。**
- **守夜人（watchmen）**：1663 年查理二世朝的立法整顿夜巡，因此得名 **"Charlies"**。
  典型班次 **21:00–06:00**，无制服，配**提灯、木棍、响板**，有值班岗亭；
  **逐时报时并报天气**，顺带查门是否上锁、**留意火情**。
  Pepys 1663 年亲历：半夜二三点被巡夜的治安官敲门，因为他家后院门没关。
  ⚠️ 「Past three o'clock, and a cold frosty morning」这类报时唱词与「老弱昏聩的 Charlie」笑话，
  多见于 18–19 世纪材料，**不要当 1666 年的实录**；1666 年可确定的只有：有巡夜、有提灯、有报时、会查火。

### 9.4 娱乐与市集

- **木偶戏（Polichinello / Punch 的前身）**：1662 年 5 月 9 日 Pepys 在 Covent Garden 首次记录英格兰的意大利木偶戏
  （`a Italian puppet play that is within the rayles there, which is very pretty, the best that ever I saw, and great resort of gallants`），
  演出者是博洛尼亚的 Pietro Gimonde（Signor Bologna）；1662 年 10 月获查理二世御前献演，赏金链与纪念章值 £25。
  **1666 年 9 月 1 日 Pepys 看的正是这个**（他写作 `Polichinelly`）。
  ⚠️ 此时用的是**提线木偶（marionettes）**，不是后世的手套偶；Judy 此时还叫 **Joan**。
- **市集**：火前伦敦的主要市场——**Cheapside**（西市主街）、**Stocks Market**（肉与鱼）、**Leadenhall**（此时尚未加顶）、
  **Newgate Market**、**Eastcheap**、**Billingsgate**（鱼／国际货）、**Queenhithe**（上游来货）。
  ⚠️ **本次未查到「1666 年伦敦哪天是集日」的可靠证据**——伦敦城内多数市场是**日常营业**而非周期集日，
  不要在片中断言「星期六是赶集日」。可安全说的是：**这些市场在 1666 年 9 月都还在，几天后全部烧掉。**
- **时令**：9 月 29 日是 **Michaelmas（米迦勒节）**，英格兰四个结账日（quarter day）之一，
  收租、清债、收获季收尾；**鹅在九月最肥，米迦勒节吃鹅**。9 月 1 日正处在收获季与米迦勒节之间。

### 9.5 §9 fact 清单

```yaml
- fact_id: london1666.custom.001
  claim: 1666 年 9 月 1 日是星期六；Pepys 当天的实际行程为上午办公、家中用饭、收拾新书房备次日宴客、下午偕妻与 Mercer 去看 Polichinelly 木偶戏、演毕赴 Islington 吃喝、一路唱着回家
  tag: ✅
  source: Pepys 日记 1666-09-01 全文
  source_url: https://www.pepysdiary.com/diary/1666/09/01/
  quote: "Saturday 1 September 1666 … Sir W. Pen and my wife and Mercer and I to 'Polichinelly,' … and so, the play being done, we to Islington, and there eat and drank and mighty merry; and so home singing, and, after a letter or two at the office, to bed."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "前一夜：街头木偶戏棚、Islington 的吃喝、夜里唱着走回城的人"
  negative: "把前一夜写成末日预兆的阴郁夜；空街；人人惶惶"

- fact_id: london1666.custom.002
  claim: 1666 年 9 月 2 日是星期日（主日），火在午夜后于 Pudding Lane 国王御用面包师家中起；当天很多人本该在做礼拜，实际在把家当往教堂里搬
  tag: ✅
  source: Pepys 日记 1666-09-02 全文
  source_url: https://www.pepysdiary.com/diary/1666/09/02/
  quote: "(Lord's day). … it begun this morning in the King's baker's house in Pudding-lane"／"And to see the churches all filling with goods by people who themselves should have been quietly there at this time."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "主日清晨：教堂里塞满了别人家的箱笼，没人在做礼拜"
  negative: "把 9 月 2 日写成平常工作日；写成礼拜正常进行"

- fact_id: london1666.custom.003
  claim: 复辟后主日到本教区礼拜为法定义务，无正当理由缺席罚 12 便士（Act of Uniformity 1662 确立国教统一，罚则沿自伊丽莎白时期统一法令）
  tag: ⚠️
  source: Wikipedia「Elizabethan Religious Settlement」/「Act of Uniformity 1662」；legislation.gov.uk 原文
  source_url: https://en.wikipedia.org/wiki/Act_of_Uniformity_1662 ; https://www.legislation.gov.uk/aep/Cha2/14/4/enacted
  quote: "Attendance at church service on Sunday at the parish church was rendered compulsory, and any person absent without reasonable cause was to pay a fine of twelve pence."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "旅行者口播可提：星期天不去教堂要罚十二便士"
  negative: "把 1666 年写成宗教宽容的城市；把清教徒禁令当仍在施行"

- fact_id: london1666.custom.004
  claim: 1666 年夏天异常炎热干旱、火起时刮强劲东风，这是火势失控的物理前提；两位目击者各自独立记下
  tag: ✅
  source: Pepys 日记 1666-09-02；Evelyn 日记 1666-09-03
  source_url: https://www.pepysdiary.com/diary/1666/09/02/ ; https://www.pepysdiary.com/indepth/2009/09/02/evelyns-fire/
  quote: Pepys："the wind mighty high and driving it into the City; and every thing, after so long a drought, proving combustible, even the very stones of churches"／Evelyn："consp[ir]ing with a fierce Eastern Wind, in a very drie season"、"the heate (with a long set of faire & warme weather) had even ignited the aire"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "干透的木构、扬尘、东风把布幡吹向西、闷热的九月夜"
  negative: "湿冷的雾伦敦、雨后街面、无风的静夜、泥泞"

- fact_id: london1666.custom.005
  claim: curfew 一词源自古法语 cuevrefeu「盖火」，14 世纪初进入英语，指晚上八九点敲钟命令把炉火压好、准备就寝，目的正是防止无人看管的炉火酿成大火；「限制出行」这层义 1800 年代才出现
  tag: ✅
  source: etymonline「curfew」词条
  source_url: https://www.etymonline.com/word/curfew
  quote: "from Anglo-French coeverfu (late 13c.), from Old French cuevrefeu, literally 'cover fire'"／"The medieval practice of ringing a bell (usually at 8 or 9 p.m.) as an order to bank the hearths and prepare for sleep was to prevent conflagrations from untended fires."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "片中知识点：curfew 这个词本来的意思就是「把火盖上」——它就是为了防止今晚这种事发明的"
  negative: "把 curfew 解释成「宵禁＝不许上街」并当作 1666 年的含义"

- fact_id: london1666.custom.006
  claim: 伦敦的宵禁钟由 St Mary-le-Bow（Bow Bells）敲响，1469 年市议会令定为每晚九点，同时标志学徒收工、城门关闭、覆火；这座教堂本身在大火中焚毁
  tag: ⚠️
  source: St Mary le Bow 教堂官网「Bells」；Wikipedia「St Mary-le-Bow」「Curfew bell」
  source_url: https://www.stmarylebow.org.uk/bells/ ; https://en.wikipedia.org/wiki/St_Mary-le-Bow
  quote: "The first known reference to Bow bells is in 1469 when the Common Council ordered that a curfew should be rung at 9 o'clock each evening."／"from at least as early as 1334, the bell rang the curfew at the end of the working day, signalling that apprentices should be back in their masters' homes, that the City gates should be closed and that fires should be covered."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "夜里九点，Bow 的钟；明天它会在火里烧掉"
  negative: "把 Bow Bells 写成大本钟式的巨型钟楼；写成火后仍在的同一口钟"

- fact_id: london1666.custom.007
  claim: 1666 年伦敦的夜巡由守夜人承担，1663 年查理二世朝立法整顿后得名 Charlies；典型班次 21:00–06:00，无制服，配提灯、木棍、响板，有值班岗亭，逐时报时并报天气，查门是否上锁并留意火情；Pepys 1663 年半夜被巡夜治安官敲门（后院门没关）
  tag: ✅
  source: Philip McCouat「Watchmen, goldfinders and the plague bearers of the night」(Journal of Art in Society) 引 Pepys 日记 1663
  source_url: https://www.artinsociety.com/watchmen-goldfinders-and-the-plague-bearers-of-the-night.html
  quote: "the 1663 legislation passed during the reign of Charles II, a circumstance which gave rise to the watchmen's semi-affectionate, semi-sarcastic nickname of 'Charlies'"／"These London watchmen patrolled the streets of the parish, typically between the hours of 9 pm to 6 am … 'armed' with a lantern, a staff and a rattle"／"The watchmen also kept a lookout for fires, and checked that occupiers had locked their doors."／Pepys 1663："I found it was the constable and his watch, who had found our back yard door open"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "夜巡人：提灯、木棍、响板、破旧大衣与软塌的帽，边走边报时；他会查你家门锁没锁、有没有明火"
  negative: "统一制服的警察、警徽、哨子、成队巡逻、19 世纪高顶礼帽"

- fact_id: london1666.custom.008
  claim: Polichinello（Punch 的前身）1662 年 5 月 9 日由博洛尼亚的 Pietro Gimonde 在 Covent Garden 首次见于英格兰记载，1662 年 10 月获查理二世御前献演；1666 年 9 月 1 日 Pepys 看的就是它。此时用的是提线木偶，Judy 还叫 Joan
  tag: ✅
  source: Pepys 日记 1662-05-09 全文；pepysdiary.com「Polichinello」百科页注释（引 V&A）
  source_url: https://www.pepysdiary.com/diary/1662/05/09/ ; https://www.pepysdiary.com/encyclopedia/10289/
  quote: Pepys 1662："Thence to see a Italian puppet play that is within the rayles there, which is very pretty, the best that ever I saw, and great resort of gallants."／百科页："performed by the Italian puppet showman Pietro Gimonde from Bologna, otherwise known as Signor Bologna. Unlike today's Punch and Judy, Bologna used marionettes – stringed puppets – rather than glove puppets."／"He argues with his wife, Judy (in Pepys' day she was called 'Joan')."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "街头木偶戏棚：提线木偶、围观的年轻绅士、露天围栏内"
  negative: "手套偶、红白条纹的现代 Punch & Judy 戏台、鳄鱼与香肠、Judy 这个名字"

- fact_id: london1666.custom.009
  claim: 大瘟疫在 1665 年冬起持续消退，1666 年 2 月国王认为伦敦已安全而返城、人口随之回流；但 1666 年仍有约 1,800 例瘟疫下葬、零星病例延续到 1666 年 9 月
  tag: ✅
  source: London Museum「The Great Plague of 1665」；Wikipedia「Great Plague of London」
  source_url: https://www.londonmuseum.org.uk/collections/london-stories/the-great-plague-of-1665/ ; https://en.wikipedia.org/wiki/Great_Plague_of_London
  quote: London Museum："the numbers suggest a slow decline in deaths, starting in the winter of 1665. By February 1666 even King Charles II felt safe enough to return."／维基："By late autumn, the death toll in London and the suburbs began to slow until, in February 1666, it was considered safe enough for the King and his entourage to come back to the city. With the return of the monarch, others began to return"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "劫后返场的城：铺面重开、外地人往城里涌、但每个人都记得去年"
  negative: "空城、遍地尸体、人人捂口鼻、街上无人"

- fact_id: london1666.custom.010
  claim: 9 月 29 日为 Michaelmas，是英格兰四个结账日之一（收租清债）、收获季收尾的标志；鹅在九月最肥，米迦勒节吃鹅。1666-09-01 正处在收获季与米迦勒节之间
  tag: ⚠️
  source: Wikipedia「Michaelmas」；Weald & Downland Living Museum；General Society of Mayflower Descendants
  source_url: https://en.wikipedia.org/wiki/Michaelmas ; https://www.wealddown.co.uk/museum-news/michaelmas/
  quote: "Michaelmas was an important day both in the liturgical calendar and as an English quarter day—one of four days in the year when financial matters were traditionally settled, including rent payments and debt collection."／"A goose was considered best in September, and Michaelmas Day, on September 29, was considered the day for goose."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "九月初：收获季尾声，鹅正肥，再过四周就是收租的日子"
  negative: "把 9 月写成春播；出现反季食材"

- fact_id: london1666.custom.011
  claim: 火前伦敦的主要市场为 Cheapside、Stocks Market、Leadenhall（此时尚未加顶）、Newgate Market、Eastcheap、Billingsgate、Queenhithe，均在 1666 年 9 月仍在运作、数日后焚毁；但本次未查到「1666 年伦敦哪天是集日」的可靠证据，城内多数市场为日常营业
  tag: ⚠️
  source: Map of Early Modern London (MoEML)「Cheapside Street」「Billingsgate」；Wikipedia「Stocks Market」；Leadenhall Market 官方史
  source_url: https://mapoflondon.uvic.ca/CHEA2.htm ; https://en.wikipedia.org/wiki/Stocks_Market ; https://leadenhallmarket.co.uk/history-of-leadenhall-market/
  quote: "Stocks Market was destroyed in the Great Fire of London in 1666 and then rebuilt."／"The Great Fire of 1666 destroyed much of the City of London, including parts of the market. When it was rebuilt not long after, it became a covered structure for the first time."／"The infrastructure on Cheapside Street was destroyed in the Great Fire of 1666, as was the rest of Cheap Ward."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "露天摊架、无顶的 Leadenhall、Cheapside 主街两侧的铺面"
  negative: "有玻璃顶棚的维多利亚式市场（Leadenhall 现貌）；断言「星期六是集日」"
```

---

## §13 常见误传（本站）（`london1666.myth.NNN`）

> 格式：**误传 → 史实 → 负向词**。负向词可直接进 prompt 的 `负面词:` 行。
> 共 **14 条**（要求 ≥ 8），逐条查证过，**其中 3 条推翻了任务书里给出的候选说法**（004 / 011 / 014 下方有标注）。

| # | 误传 | 史实 | 负向词 |
|---|---|---|---|
| 001 | 全城清教徒式黑衣高帽、帽上带扣 | 1666 是**复辟期**，清教共和已结束六年。所谓「清教徒黑衣」本身也是误传——连清教徒日常也穿 sadd colours（russet、tawny、深绿、暗蓝、李子色），黑染料贵且易褪，只用于长老与画像等最正式场合；带扣高帽（capotain）是**朝圣先辈的图像学**，非 1666 伦敦 | `Puritan black, capotain buckle hat, Pilgrim costume, all-black crowd, Salem` |
| 002 | 大火「只死了 6 人」 | 数字**有争议**。官方仅记录寥寥数人（Monument 铭文甚至称「对市民的生命无害」）；Tinniswood 认为「个位数」但承认必有漏记，Field 认为「可能高于 6，但不太可能上百」，**Hanson 则估「数百乃至数千」**，理由是火场温度高于现代火化炉、穷人与外来者本就不入册。**片中不要断言任何一个数字。**（另：**9 月 1 日还没有人死**） | `"only six died" caption, definitive death toll, corpses in the street on Sept 1` |
| 003 | 伦敦桥在火中被烧毁 | **桥保住了。** 1633 年的一场火烧掉了桥北段 42 户、留下一道缺口且未重建，这道意外的**防火带**挡住了 1666 年的火南渡。**但桥北端的房子确实烧了**——Pepys 亲眼所见 | `London Bridge collapsing, bridge engulfed in flames, fire crossing to Southwark` |
| 004 | 街上到处是「Bring out your dead」的瘟疫车 | **错位一整年。** 那是 1665 年的做法，且**只在夜间**进行（白天收尸会引发恐慌）、由持火把的 linke man 与摇铃人引路。到 1666 年 9 月瘟疫已大幅消退、国王 2 月已返城。**且这句喊话之所以家喻户晓，主要来自 Defoe 1722 年的《瘟疫年纪事》——他写的时候距事件 60 年、事发时他才 5 岁**（⚠️ **这一条推翻了候选说法的默认前提**：不只是「1666 年 9 月还有没有」的问题，这句话本身的一手证据就薄） | `plague cart, "bring out your dead", red cross on doors, corpse pit, daytime body collection` |
| 005 | 人人满口 thee/thou、莎士比亚腔 | 见 §10：1650 年 thou 已过时；Pepys 全日记 thou 仅 5 处且全在特殊语域；1666 年成系统用 thou 的是贵格会（正在被起诉） | `thee, thou, prithee, forsooth, verily, Shakespearean dialogue` |
| 006 | 三角帽、长马甲、18 世纪套装 | 三角帽（tricorne）是 18 世纪的事。**长马甲（vest）恰恰是查理二世在 1666 年 10 月 7 日才宣布采用的**——比大火晚**五周**，Evelyn 10 月 18 日记下国王首次正式穿它。**1666 年 9 月 1 日的伦敦没有一件 vest。** 此时男装是 doublet、宽大的 petticoat breeches、大量缎带、假发（Pepys 1663 年起戴，查理二世 1663 年底开始戴） | `tricorne hat, three-piece suit, waistcoat, frock coat, 18th-century tailoring, Georgian dress` |
| 007 | 宽阔铺装街道、玻璃大窗、整齐立面 | 街道**窄**，木构联排屋层层**出挑（jetty）**，顶层几乎在窄巷上空相接；当时人已经在说这「既助长火势，又妨碍施救」。查理二世 1661 与 1665 两次公告禁止出挑窗与 jetty，**均被地方当局无视** | `wide paved boulevard, large plate glass windows, regular Georgian facades, clean straight street` |
| 008 | 茅草屋顶把火引着了（**给图像模型的头号负向**） | **伦敦城内自 1189 年起禁茅草顶**，1212 年大火后规定新屋必须瓦、木瓦或木板顶，旧茅草顶须抹泥。到 1666 年绝大多数房子是**瓦顶**。当时的两份记述指的是**木构**不是茅草 | `thatched roof, straw roof, reed thatch, medieval village roofline` |
| 009 | 桌上有土豆 / 番茄 / 玉米 / 辣椒 | 土豆虽 1570 年前后入欧，但在英国饮食中占主位要到 **19 世纪**；番茄长期作观赏植物、被疑有毒，约 **1750 年**才进英国餐桌；玉米、甜椒、可可等新世界作物要到 17 世纪末—18 世纪初才普遍 | `potatoes, tomatoes, corn on the cob, chili peppers, bell peppers on the table` |
| 010 | 圣保罗大教堂顶着 Wren 的圆顶 | 1666 年是**旧圣保罗**：**1561 年雷击烧毁尖塔后一直没有重建**（所以它是**平的、秃的**），西面挂着 Inigo Jones 1630 年代加的**古典门廊**，火起时**脚手架正架在教堂外面**（Evelyn 明说 `the Scaffalds contributed exceedingly`）。**Wren 此时 33 岁，是个天文学家，还不是大教堂的建筑师** | `Wren dome, St Paul's dome, baroque cathedral, twin west towers, modern St Paul's silhouette` |
| 011 | 火灾被归咎于天主教徒／法国人（Hubert 被处决） | **时间线要卡死，别提前。** 9 月 1 日：无。9 月 2–6 日：起火、蔓延。**9 月 7 日 Evelyn 才记下「法国人与荷兰人登陆了」的恐慌与随之而来的私刑。** Robert Hubert **10 月 27 日**才在 Tyburn 绞死——而且瑞典船长作证他在**起火两天后**才上岸，面包师也说那面墙根本没有窗户。Monument 上的反天主教铭文是 **1681 年**加的（Popish Plot 期间）、**1830 年**凿掉（⚠️ **候选说法只提醒「别提前」是对的，但本次还查出：这条错误在 1681 年被官方刻上了石头，直到 1830 年才铲掉——这个细节比「别提前」本身更有戏**） | `anti-Catholic mob on Sept 1, Hubert's execution, Monument inscription, "popish frenzy", French scapegoat in early September` |
| 012 | 大火终结了大瘟疫 | **London Museum 明确否定。** 理由四条：火后卫生与排污没有实质改善；瘟疫最重的 Whitechapel、Clerkenwell、Southwark **没被烧到**；死亡数**从 1665 年冬起就在降**；火后伦敦**仍有人死于瘟疫** | `"the fire ended the plague" caption, rats burning, purifying flame narrative` |
| 013 | 砖房是大火之后才有的 | 1666 **之前伦敦就有很多砖房**，连起火的 Pudding Lane 上都有。詹姆斯一世 1605 年即令新屋须用砖石（因海军要木料），1607 年重申——只是执行得很差。1667 年《重建法》是**强制执行既有规则**，不是发明砖 | `"brick was introduced after the fire", all-timber city with zero brick` |
| 014 | 火灾纪念碑（the Monument）矗立在现场 | **1666 年 9 月 1 日没有纪念碑。** 它 1671 年才动工、1677 年完成。**任何出现纪念碑的 1666 年镜头都是穿帮**（⚠️ 本条为本 worker 追加，不在候选清单内——但它是 AI 出图时极易自动加进 Pudding Lane 画面的元素） | `the Monument column, commemorative column, Doric column with flaming urn` |

### 13.1 §13 fact 清单

```yaml
- fact_id: london1666.myth.001
  claim: 1666 年的伦敦不是清教徒黑衣高帽的城；复辟已六年，且「清教徒只穿黑」本身就是误传——日常穿的是 sadd colours（russet、tawny、深绿、暗蓝、李子色），黑染料贵且易褪、仅用于最正式场合；带扣高帽是朝圣先辈的图像学
  tag: ❌
  source: Wikipedia「Sadd colors」；Historic Dress「What did the pilgrims wear? Not just black and white!」；Wikipedia「Capotain」
  source_url: https://en.wikipedia.org/wiki/Sadd_colors ; https://historicdress.org/wordpress/what-did-the-pilgrims-wear-not-just-black-and-white/
  quote: "black was actually considered too bold for regular use and was reserved for community elders and for highly formal occasions"／"A list of these 'sadd colors' in 1638 included 'liver color, de Boys, tawney, russet, purple, French green, ginger lyne, deer colour, orange.'"／"The concept that Puritans only wore black came from cultural representations in film and literature"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "街上是 russet、tawny、暗绿、李子色的毛料，间杂缎带与亮色；不是一片黑"
  negative: "Puritan black, capotain buckle hat, Pilgrim costume, all-black crowd, Salem witch trial look"

- fact_id: london1666.myth.002
  claim: 「大火只死了 6 人」是有争议的数字而非定论——Tinniswood 主张「个位数」但承认必有漏记，Field 认为「可能高于六但不太可能上百」，Hanson 估「数百乃至数千」（理由：火场温度高于现代火化炉、穷人与外来者本就不入册）；片中不应断言任何一个数字
  tag: ⚠️
  source: Londonist「Is It True That Only Six People Died In The Great Fire?」；Wikipedia「Great Fire of London」§ Deaths and destruction
  source_url: https://londonist.com/2016/08/is-it-true-that-only-six-people-died-in-the-great-fire ; https://en.wikipedia.org/wiki/Great_Fire_of_London
  quote: Londonist："Tinniswood, who puts the death toll 'in single figures', adds that there must have been deaths that went unrecorded… Hanson, by contrast, cites 'common sense' … 'several hundred or quite possibly several thousand' is his estimation."／维基："Field argues that the number 'may have been higher than the traditional figure of six, but it is likely it did not run into the hundreds'"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "口播只说「官方只记下几个人，历史学家至今争论真实数字」，不给具体数"
  negative: "\"only six died\" caption, definitive death toll on screen, corpses on the street on Sept 1"

- fact_id: london1666.myth.003
  claim: 伦敦桥没有在大火中被烧毁——1633 年一场火烧掉桥北段并留下未重建的缺口，这道意外防火带挡住了火南渡；但桥北端那些房子确实烧了
  tag: ✅
  source: London Museum「London Bridge」；Wikipedia「Early fires of London」；Pepys 日记 1666-09-02（目击）
  source_url: https://www.londonmuseum.org.uk/collections/london-stories/london-bridge/ ; https://en.wikipedia.org/wiki/Early_fires_of_London ; https://www.pepysdiary.com/diary/1666/09/02/
  quote: "A previous major fire in 1633 had destroyed a section of the bridge and created a gap… this accidental 'firebreak' prevented the bridge from being damaged by the Great Fire of London three decades later"／Pepys："there I did see the houses at that end of the bridge all on fire"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "桥北端房屋燃烧，桥身与南段完好；缺口处可见断掉的房排"
  negative: "London Bridge collapsing, whole bridge engulfed, fire crossing to Southwark over the bridge"

- fact_id: london1666.myth.004
  claim: 「Bring out your dead」的瘟疫车属 1665 年且只在夜间进行（白天收尸会引发恐慌），1666 年 9 月已不是街头景象；且这句喊话的知名度主要来自 Defoe 1722 年的小说《瘟疫年纪事》——他写作时距事件 60 年、事发时才 5 岁
  tag: ❌
  source: Philip McCouat「Watchmen, goldfinders and the plague bearers of the night」；London Museum「The Great Plague of 1665」；Defoe『A Journal of the Plague Year』(1722) 的成书背景
  source_url: https://www.artinsociety.com/watchmen-goldfinders-and-the-plague-bearers-of-the-night.html ; https://www.londonmuseum.org.uk/collections/london-stories/the-great-plague-of-1665/ ; https://www.gutenberg.org/files/376/376-h/376-h.htm
  quote: "Collection of the corpses was permitted only at night. An early experiment of doing it by day had to be abandoned because it induced fear and panic among the public"／"typically preceded by a 'linke' man holding a burning torch and another ringing a warning bell, with the driver calling out 'Bring out your dead!'"／London Museum："By February 1666 even King Charles II felt safe enough to return."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "1666 年 9 月的街上没有死人车；若要提，作为「去年的事」由口播带过"
  negative: "plague cart, \"bring out your dead\", red cross painted on doors, corpse pit, daytime body collection, boarded-up plague houses"

- fact_id: london1666.myth.005
  claim: 1666 年伦敦人不满口 thee/thou、不说莎士比亚腔（详见 §10 lang.002–005 的量化证据）
  tag: ❌
  source: 见 lang.002 / 003 / 004 / 005
  source_url: https://en.wikipedia.org/wiki/Early_Modern_English ; https://www.pepysdiary.com/search/?q=thou
  quote: "by 1650, 'thou' seems old-fashioned or literary."／Pepys 全日记 thou 5 条、thee 6 条、prithee 0 条
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "对白一律现代英语 + you"
  negative: "thee, thou, prithee, forsooth, verily, Shakespearean dialogue, ye olde"

- fact_id: london1666.myth.006
  claim: 三角帽与长马甲不属 1666 年 9 月——vest（长马甲）是查理二世 1666 年 10 月 7 日宣布采用的，比大火晚五周，Evelyn 10 月 18 日记下国王首次正式穿着；三角帽是 18 世纪的事。此时男装是 doublet、宽大的 petticoat breeches、大量缎带与假发
  tag: ❌
  source: Pepys 日记 1666-10 系列；Evelyn 日记 1666-10-18；witness2fashion「Birth of the Three Piece Suit: October, 1666」；Fashion History Timeline「1660-1669」
  source_url: https://witness2fashion.wordpress.com/2020/09/04/birth-of-the-three-piece-suit-october-1666/ ; https://fashionhistory.fitnyc.edu/1660-1669/ ; https://www.pepysdiary.com/diary/1666/10/15/
  quote: "On October 7 1666 Charles issued a declaration that his court would no longer wear 'French fashions'. Instead, it would adopt what was known at the time as the Persian vest"／Evelyn："it being the first time of his Majesties putting himselfe solemnly into the Eastern fashion of Vest, changing doublet, stiff Collar & Cloake &; into a comely Vest"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "1666 年 9 月男装：doublet、宽松及膝 petticoat breeches、成束缎带、宽檐软帽、长卷假发"
  negative: "tricorne hat, three-piece suit, waistcoat, vest, frock coat, 18th-century tailoring, Georgian dress"

- fact_id: london1666.myth.007
  claim: 1666 年伦敦街道狭窄、木构联排层层出挑（jetty），顶层几乎在窄巷上空相接；当时人已明说这既助长火势又妨碍施救；查理二世 1661 与 1665 两次公告禁止出挑，均被地方当局无视
  tag: ✅
  source: Wikipedia「Great Fire of London」§ 火前的伦敦；London Museum 引 Wych Street 旧照说明
  source_url: https://en.wikipedia.org/wiki/Great_Fire_of_London ; https://www.londonmuseum.org.uk/collections/london-stories/myths-great-fire-london/
  quote: "The typical multi-storey timbered London tenement houses had 'jetties' (projecting upper floors)."／"the top jetties all but met across the narrow alleys—'as it does facilitate a conflagration, so does it also hinder the remedy', wrote one observer."／"In 1661, Charles II issued a proclamation forbidding overhanging windows and jetties, but this was largely ignored by the local government."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "窄巷，木构屋一层层向街心出挑，顶层几乎相接，天只剩一条缝"
  negative: "wide paved boulevard, large plate glass windows, regular Georgian facades, clean straight street, open sky above the street"

- fact_id: london1666.myth.008
  claim: 伦敦城内自 1189 年起禁茅草顶，1212 年大火后规定新屋须瓦/木瓦/木板顶、旧茅草须抹泥；到 1666 年绝大多数房子是瓦顶，当时的记述指的是木构不是茅草
  tag: ❌
  source: London Museum「Three myths about the Great Fire of London」（策展人 Meriel Jeater）
  source_url: https://www.londonmuseum.org.uk/collections/london-stories/myths-great-fire-london/
  quote: "Thatch roofs made with reeds or straw had actually been banned within the City of London since 1189."／"By 1666, the vast majority of houses in London had tiled roofs. If some thatched buildings remained, they weren't noted as a cause of the fire."／"Two accounts from the time mention timber buildings as a problem – but not thatch."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "屋顶一律陶瓦/木瓦，墙体木构填灰泥；不是村舍"
  negative: "thatched roof, straw roof, reed thatch, medieval village roofline, cottage"

- fact_id: london1666.myth.009
  claim: 1666 年英国餐桌上不该出现土豆、番茄、玉米、辣椒——土豆成为英国饮食主位要到 19 世纪，番茄长期作观赏植物、约 1750 年才进英国餐桌，玉米与甜椒等要到 17 世纪末—18 世纪初
  tag: ❌
  source: Wikipedia「Potato」「Early modern European cuisine」；Warwick GHCC blog；Tastes of History「Food in the 17th-Century」
  source_url: https://en.wikipedia.org/wiki/Potato ; https://en.wikipedia.org/wiki/Early_modern_European_cuisine ; https://www.tastesofhistory.co.uk/post/food-in-the-17th-century
  quote: "The earliest potatoes were brought to Europe in about 1570 by Spanish explorers. However, widespread cultivation and prominence in the British diet did not take place until the 19th century."／"The tomato … was largely kept as an ornamental plant… tomatoes only became part of the British diet by around 1750."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "吃食：面包、肉派、烤肉、鱼、麦酒、奶酪、苹果与李子；九月的鹅"
  negative: "potatoes, tomatoes, corn on the cob, chili peppers, bell peppers, chocolate, tea service"

- fact_id: london1666.myth.010
  claim: 1666 年的圣保罗是旧圣保罗——1561 年雷击焚毁尖塔后一直未重建（塔顶是平的），西立面挂着 Inigo Jones 1630 年代加的古典门廊，火起时脚手架正架在建筑外面；Wren 当时 33 岁、身份是天文学家，尚未成为大教堂建筑师
  tag: ❌
  source: Evelyn 日记 1666-09-03 / 09-07；Wikipedia「Old St Paul's Cathedral」；monumentoffame.org「The Final Years of Old St. Paul's」
  source_url: https://www.pepysdiary.com/indepth/2009/09/02/evelyns-fire/ ; https://en.wikipedia.org/wiki/Old_St_Paul%27s_Cathedral
  quote: Evelyn 09-03："was now taking hold of St. Paules-Church, to which the Scaffalds contributed exceedingly."／Evelyn 09-07："that beautifull Portico (for structure comparable to any in Europ, as not long before repaird by the late King) now rent in pieces"／"In 1561, lightning struck the spire and it caught fire… They never replaced the spire."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "旧圣保罗：巨大的哥特体量、塔顶平秃无尖塔、西面一排古典柱廊、外墙搭着木脚手架"
  negative: "Wren dome, St Paul's dome, baroque cathedral, twin west towers, modern St Paul's silhouette, tall gothic spire"

- fact_id: london1666.myth.011
  claim: 归咎天主教徒/法国人的时间线必须卡死——9 月 7 日 Evelyn 才记下「法国人与荷兰人登陆」的恐慌与随之的私刑；Robert Hubert 10 月 27 日才在 Tyburn 绞死（瑞典船长作证他在起火两天后才上岸、面包师说那面墙没有窗户）；Monument 上的反天主教铭文 1681 年加、1830 年凿掉
  tag: ❌
  source: Evelyn 日记 1666-09-07；British Library「Robert Hubert and the Great Fire of London」；Wikipedia「Robert Hubert」「Monument to the Great Fire of London」
  source_url: https://www.pepysdiary.com/indepth/2009/09/02/evelyns-fire/ ; https://www.bl.uk/stories/blogs/posts/robert-hubert-and-the-great-fire-of-london ; https://en.wikipedia.org/wiki/Monument_to_the_Great_Fire_of_London
  quote: Evelyn 09-07："there was (I know not how) an Alarme begun, that the French & Dutch (with whom we were now in hostility) were not onely landed, but even entring the Citty"／"Hubert was hanged at Tyburn on 27 October 1666"／"a Swedish ship's captain testified that he had landed the watchmaker ashore two days after the fire had started"／"In 1681, the words 'but Popish frenzy, which wrought such horrors, is not yet quenched' were added… The words were chiselled out in 1830."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "9 月 1 日的伦敦没有排外私刑；若做此线，只能出现在 9 月 7 日之后的镜"
  negative: "anti-Catholic mob on Sept 1, Hubert's execution, Monument inscription, \"popish frenzy\", French scapegoat in early September"

- fact_id: london1666.myth.012
  claim: 大火没有终结大瘟疫——火后卫生与排污无实质改善；瘟疫最重的 Whitechapel、Clerkenwell、Southwark 没被烧到；死亡数从 1665 年冬起就在降；火后仍有人死于瘟疫
  tag: ❌
  source: London Museum「Three myths about the Great Fire of London」
  source_url: https://www.londonmuseum.org.uk/collections/london-stories/myths-great-fire-london/
  quote: "There were no major improvements to hygiene or the systems for getting rid of human waste afterwards. Many of the areas worst affected by the plague, such as Whitechapel, Clerkenwell and Southwark, weren't destroyed by the fire. The number of people dying from plague was already falling from the winter of 1665 onwards. People continued to die from plague in London after the Great Fire was over."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "口播若提瘟疫，明说：火没有把瘟疫烧掉，那是个流传很广的误会"
  negative: "\"the fire ended the plague\" caption, rats burning, purifying flame narrative"

- fact_id: london1666.myth.013
  claim: 砖房不是大火之后才出现的——1666 年前伦敦已有很多砖房，连起火的 Pudding Lane 上都有；詹姆斯一世 1605 年即令新屋须用砖石（因海军需木料），1607 年重申，只是执行很差。1667 年《重建法》是强制执行既有规则而非发明砖
  tag: ❌
  source: London Museum「Three myths about the Great Fire of London」
  source_url: https://www.londonmuseum.org.uk/collections/london-stories/myths-great-fire-london/
  quote: "But there were many brick buildings in London before 1666. Even on Pudding Lane where the fire began."／"In March 1605, King James I said that no one should build a new house in London unless it was made from brick or stone because he needed timber for the navy's ships."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "街景里可以有砖砌立面与木构屋混杂，不必做成纯木城"
  negative: "\"brick was introduced after the fire\" caption, all-timber city with zero brick"

- fact_id: london1666.myth.014
  claim: 大火纪念碑（the Monument）1671 年才动工、1677 年完成；1666 年 9 月 1 日现场没有纪念碑，任何出现它的 1666 年镜头都是穿帮
  tag: ❌
  source: Wikipedia「Monument to the Great Fire of London」；themonument.org.uk 官方史
  source_url: https://en.wikipedia.org/wiki/Monument_to_the_Great_Fire_of_London ; https://www.themonument.org.uk/history
  quote: "Monument to the Great Fire of London … built between 1671 and 1677"（词条概述）／官方史页同期给出 1671 起建、1677 竣工
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "Pudding Lane / Fish Street Hill 画面里没有任何纪念柱"
  negative: "the Monument column, commemorative column, Doric column with flaming urn, golden urn on a pillar"
```

---

## 未决项 / 建议后续补核

| # | 项 | 为什么重要 | 建议动作 |
|---|---|---|---|
| U1 | **所有 quote 的 verified_by 仍是 ai_read** | §10.4 的原话清单是本站 NPC 台词的合法性来源，带着 ai_read 出片等于把「真实原话」建在未经人眼核对的抓取上 | 出台词前逐条人工打开 source_url 核对，改 `verified_by: human` |
| U2 | **Evelyn 姓氏读音 /ˈiːvlɪn/** | 会直接进配音 | 只有搜索摘要，未逐字抓到词典页；人工二核或换用有音频的词典 |
| U3 | **Queenhithe 读音** | 出现在 Pepys 9 月 2 日原文里，若入片会被 TTS 乱读 | 补核；未核前不要让 TTS 自由发挥 |
| U4 | **「1666 年伦敦哪天是集日」** | 关系到前一夜能不能拍市集 | 本次未找到可靠证据；建议查 MoEML 或 London Metropolitan Archives。**未核前不要在片中断言** |
| U5 | **Farriner 女仆的姓名** | 她是大火第一个死者，是极强的情感锚点 | Londonist 称其为 "unnamed maid"；London Museum 另有「首位目击者被查明」的新闻稿，值得追 |
| U6 | **「your Worship」在 1666 年伦敦的市政场合是否成立** | 若成立，可给市政场景加一层质感 | Pepys 语料 0 证据；建议查 Old Bailey Proceedings（惜其始于 1674） |
| U7 | **Bloodworth「A woman might piss it out」** | 全网最流行的那句「原话」 | **已查实：不在 Pepys 日记里。** 维基给的出处是 James Malcolm『Londinium Redivivum』(1807)，晚 141 年。**本片不得把它当原话用**；若要用，必须标为后世流传的说法。这条已在 lang.013 与 §10.4 的规则 A 里落地 |
