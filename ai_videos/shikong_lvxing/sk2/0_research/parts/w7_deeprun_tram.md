---
worker_id: researcher-w7-deeprun-tram
stage: 0
role: researcher
angle: deeprun-tram
status: complete
blockers: []
confidence: high
---

# W7 · 矿道地铁（Deeprun Tram）——sk2「当天的大事」专项

> 版本锚点：**经典旧世 Vanilla / WoW 1.x / Classic**（世界内当下 ＝ **Year 25 ADP**）。
> 本路只管矿道地铁这一条线：命名、建造史、车站、矿车、隧道、水下段、运营、可拍性、「那一天」方案。
> 城市布局 / 衣着 / 物价 / 其他机构不在本路范围。

---

## 0. 结论先行（三条，请先读）

### 结论 1 ❌ 名字错了：官方简中译名是「**矿道地铁**」，不是「深铁矿道」

派给本路的任务书写的是「深铁矿道」。查证下来，简体中文客户端与魔兽世界中文维基用的官方译名是
**矿道地铁**（英文 Deeprun Tram）。「深铁矿道」在中文魔兽语料里查不到任何官方出处，疑似是把
Deeprun 硬译成「深铁」＋ Tram 误读成「矿道」的二次组合。

**本片一切口播、字幕、文档名请统一改用「矿道地铁」。** 若要保留一点异域感，可在口播里说
「矿道地铁，Deeprun Tram」——中英并置，不要自造译名。

### 结论 2 ❌ 最关键的一条：**游戏内设定从未记载任何「通车典礼 / 落成仪式 / 首班车」**

我穷尽查了 warcraft.wiki.gg 的 History 全节、Gelbin Mekkatorque 词条的全部引注、暴雪官方短篇
《Cut Short》原文、以及 *Beyond the Dark Portal* 第 5 章的引注链。**没有任何一处写过通车仪式、
剪彩、首班车、开通致辞、纪念日。** 设定只写到「新建成的矿道地铁**发展成为**两座首都之间不可或缺
的纽带」——一句"后来它变得很重要"，中间的落成瞬间是**空白**。

**连竣工年份都没有。** 只知道开建背景是 6 ADP（第二次战争之后），之后就直接跳到成品。

### 结论 3 ⚠️ 更硬的冲突：**在 Vanilla 这一天，地铁已经通了大约十九年**

- 开建：**6 ADP**（第二次战争后，Magni 委托 Mekkatorque）
- Vanilla 当下：**Year 25 ADP**
- 差：**约 19 年**

所以「Vanilla 版本锚点 ＋ 当天大事 ＝ 通车」是**自相矛盾的**：在旅行者踏进暴风城矮人区的那一天，
这条线早已是通勤日常，站台上站着的是灭鼠工和卖鼠肉串的小贩，不是剪彩的贵宾。

**唯一出现「Grand Opening（隆重开通）」这个词的官方文本，是 2004 年 9 月 18 日的 0.10 版本补丁说明**
——那是**开发者对玩家说的话**，不是世界内发生的事件。见 `stormwind.event.003`。它可以被聪明地利用
（见方案 C），但**不能当成世界内的通车典礼来拍**。

> 一句话交底：**想拍"通车日"，就得放弃 Vanilla 锚点；想守 Vanilla 锚点，就得换一件"当天的大事"。**
> 第 4 节给了三个方案，各自写清代价。

---

## 1. 事实注册表

### 1.1 命名与身份

```yaml
- fact_id: stormwind.tram.001
  claim: 英文正式名 Deeprun Tram，别称 the Tram；是一条全封闭、地下（且部分在水下）的双轨线，线上跑两列各三节的车厢，整体归功于侏儒的工程技术。
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram（首段）
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "The Deeprun Tram (or simply the Tram) is a long, fully enclosed, underground (and partially underwater) set of double tracks upon which rolls two sets of three wagons, all credited to the gnomes' technical engineering."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "地下双轨隧道，两条并行的铁灰色钢轨嵌在深褐色枕木上，轨距窄，隧道全封闭无天光，岩壁为青灰色花岗岩凿面"
  negative: "露天铁路, 阳光, 蒸汽机车头, 宽轨, 现代地铁车厢"

- fact_id: stormwind.tram.002
  claim: 官方简体中文译名为「矿道地铁」；「深铁矿道」不是官方译名，查无出处。
  tag: ❌
  source: 魔兽世界中文维基（灰机 wiki）条目标题「矿道地铁」
  source_url: https://warcraft.huijiwiki.com/wiki/%E7%9F%BF%E9%81%93%E5%9C%B0%E9%93%81
  quote: "矿道地铁 - 魔兽世界中文维基"
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "（命名事实，不入画）"
  negative: "深铁矿道, 深跑电车, 迪普伦电车"

- fact_id: stormwind.tram.003
  claim: 服务快速平稳，对旅客完全免费，往返于联盟阵营的铁炉堡与暴风城之间。
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram（首段）
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "The service is fast and smooth, and is provided free of charge to travelers between the Alliance-aligned cities of Ironforge and Stormwind City."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "站台无闸机、无售票窗口、无收费员，乘客径直走上车厢"
  negative: "闸机, 检票口, 售票亭, 投币箱, 车票"

- fact_id: stormwind.tram.004
  claim: 两端车站分别位于暴风城的矮人区（Dwarven District）与铁炉堡的机械侏儒区（Tinker Town）。
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram / Travel guide
  source_url: https://warcraft.wiki.gg/wiki/Travel_guide_to_Deeprun_Tram_and_boats
  quote: "the northeast part called the [[Dwarven District]] mostly inhabited by [[Dwarf|dwarves]] ... the northeast part called [[Tinker Town]] mostly inhabited by [[Gnome|gnomes]]"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（方位事实，配合车站形制使用）"
  negative: "地面车站, 城外车站"

- fact_id: stormwind.tram.005
  claim: 地精飞艇的经营者会把矿道地铁说成是谣言，向部落乘客贬低它；飞艇管理员 Hin Denburg 的原话可直接引用。
  tag: ✅
  source: Warcraft Wiki - Hin Denburg（gossip 文本）
  source_url: https://warcraft.wiki.gg/wiki/Hin_Denburg
  quote: "This here is the finest, most state of the art mode of transportation money can build. What? Deeprun Tram? Gnomes? Listen pal. If you believe that garbage then I've got a statue down in Stranglethorn to sell ya."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（台词素材，不入画）"
  negative: ""
```

### 1.2 建造历史（本路核心）

```yaml
- fact_id: stormwind.tram.006
  claim: 起因是 6 ADP 第二次战争之后，暴风城人类开始重建被战火摧毁的家园。
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram，History 节
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "Following the Second War in 6 ADP, the humans of the Stormwind began the grueling task of rebuilding the war-torn lands surrounding their battered kingdom."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（年代事实，不入画）"
  negative: ""

- fact_id: stormwind.tram.007
  claim: 铁炉堡的矮人迅速向人类盟友伸出援手，当时洛丹伦联盟的兄弟情谊正处在最强的时候。
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram，History 节
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "In those days, the bonds of brotherhood that cradled the Alliance of Lordaeron were still at their strongest, and the dwarves of Ironforge were quick to lend aid to their human allies."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（背景事实，不入画）"
  negative: ""

- fact_id: stormwind.tram.008
  claim: 建这条线的真正动机有两个——麦格尼·铜须国王受不了援助运抵暴风城的速度太慢，同时也想建立一条能在必要时把矮人士兵送去增援人类王国的通道。
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram，History 节
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "King Magni Bronzebeard was frustrated, however, at the sluggish pace with which his country's aid was being delivered to Stormwind, and eager as well to establish a means of reinforcing the human kingdom with dwarven soldiers should the need arise."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（动机事实，不入画；可作口播——这条线是运货的，也是运兵的）"
  negative: ""

- fact_id: stormwind.tram.009
  claim: 铜须国王找的是当时艾泽拉斯最负盛名的工程师、大工匠格尔宾·梅卡托克，后者立刻开始为一套连接暴风城与铁炉堡的宏大地下铁路系统绘制设计图。
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram，History 节
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "King Bronzebeard turned to Azeroth's most esteemed engineer, High Tinker Gelbin Mekkatorque, who immediately began drafting designs for a grand subterranean railway system that would link the cities of Stormwind City and Ironforge."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "侏儒设计室：黄铜色绘图仪器、卷起的蓝灰色图纸、木制绘图桌、齿轮镇纸"
  negative: "人类风格书房, 羊皮卷轴, 魔法符文"

- fact_id: stormwind.tram.010
  claim: 梅卡托克是在诺莫瑞根 17 区（sector 17）的自己办公室里画出矿道地铁的施工图的。
  tag: ✅
  source: Warcraft Wiki - Gelbin Mekkatorque（引注 Cut Short, pg.2）
  source_url: https://warcraft.wiki.gg/wiki/Gelbin_Mekkatorque
  quote: "From his office at sector 17, Gelbin prepared the schematics for the Deeprun Tram,"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（背景事实，不入画）"
  negative: ""

- fact_id: stormwind.tram.011
  claim: 梅卡托克还用派盘（烤盘）拼出过一个矿道地铁的等比模型；在暴雪官方短篇《Cut Short》原文里，它被形容成「像是用派盘搭出来的兔子窝」。
  tag: ✅
  source: 暴雪官方短篇 Gelbin Mekkatorque - Cut Short（Cameron Dayton, 2011-06-15）
  source_url: https://worldofwarcraft.blizzard.com/en-us/media/short-story/gelbin-mekkatorque-cut-short
  quote: "something that looked like a coney burrow built out of pie tins ... Well, I suppose the Deeprun Tram scale mock-up does kind of look that way...."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "桌面上一座用一圈圈锡色烤盘扣接而成的粗糙隧道模型，像一窝叠起来的碗，锡色金属反光，旁边散落小螺丝"
  negative: "精致沙盘, 水晶模型, 发光全息投影"

- fact_id: stormwind.tram.012
  claim: 梅卡托克设计这条地下交通线时，至少有另外四名侏儒协助。
  tag: ✅
  source: Warcraft Wiki - Gelbin Mekkatorque
  source_url: https://warcraft.wiki.gg/wiki/Gelbin_Mekkatorque
  quote: "Mekkatorque began working on designing the underground transport with the help of at least four other gnomes."
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "五名侏儒围在一张大图纸前，各自拿着不同的黄铜色量具"
  negative: "人类工程师, 独自一人"

- fact_id: stormwind.tram.013
  claim: 施工期间遭遇了两个大麻烦：一个地下湖，和一场老鼠入侵。
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram，History 节（引注 Beyond the Dark Portal ch.5）
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "Despite problems with a subterranean lake and a rat invasion, the newly-built Deeprun Tram developed into an indispensable link between the two great capitals,"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "隧道掌子面破口涌入的地下水，墨绿色冷水漫过碎石，矿灯照出水面反光"
  negative: "温泉, 岩浆, 阳光下的湖"

- fact_id: stormwind.tram.014
  claim: 建成后的矿道地铁成为两大首都之间不可或缺的纽带，为成千上万的市民提供快速安全的交通，并加强了两支联盟军队之间的军事协作。
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram，History 节
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "the newly-built Deeprun Tram developed into an indispensable link between the two great capitals, providing swift and safe transportation for thousands of their citizens, and bolstering military cooperation between the armies of these two proud Alliance strongholds."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "站台上人流密集，矮人、人类、侏儒混杂候车，像通勤高峰"
  negative: "空荡站台, 观光客, 典礼来宾"

- fact_id: stormwind.tram.015
  claim: 梅卡托克在施工期间持续向图拉扬将军汇报进展与问题，尤其是老鼠的问题。
  tag: ✅
  source: Warcraft Wiki - Gelbin Mekkatorque（引注 Beyond the Dark Portal, chapter 5）
  source_url: https://warcraft.wiki.gg/wiki/Gelbin_Mekkatorque
  quote: "He kept General Turalyon informed about updates or problems, notably a problem of rats."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（背景事实，不入画）"
  negative: ""

- fact_id: stormwind.event.001
  claim: 【核心结论】遍查全部可及来源，矿道地铁在游戏内设定中【没有任何通车典礼 / 落成仪式 / 首班车 / 开通致辞 / 纪念日的记载】；History 节从"施工遇到麻烦"直接跳到"后来它变得不可或缺"，落成瞬间是空白。
  tag: ❌
  source: Warcraft Wiki - Deeprun Tram（History 全节读毕，无仪式段落）
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "Despite problems with a subterranean lake and a rat invasion, the newly-built Deeprun Tram developed into an indispensable link between the two great capitals"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（负面结论，不入画——严禁凭空拍剪彩/致辞/贵宾席）"
  negative: "剪彩, 红绸, 典礼台, 贵宾致辞, 通车纪念碑揭幕, 礼炮"

- fact_id: stormwind.event.002
  claim: 设定同样没有给出矿道地铁的竣工年份——只写明 6 ADP 开建的背景，没有写它哪一年建成通车。
  tag: ⚠️
  source: Warcraft Wiki - Deeprun Tram（History 节只标 6 ADP / 25 ADP / 28 ADP / 30 ADP 四个年份，无竣工年）
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "Following the Second War in 6 ADP ... By the Year 25 ADP, the rat problem remained and was handled by Monty."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（年代空白，不入画）"
  negative: "明确年份字幕, 通车 XX 周年横幅（除非按方案 C 明说是推测）"
```

### 1.3 「Grand Opening」这个词的唯一真实出处（游戏外）

```yaml
- fact_id: stormwind.event.003
  claim: 【唯一出现「Grand Opening」的官方文本】2004 年 9 月 18 日的 WoW 测试版 0.10 补丁说明宣布了矿道地铁的隆重开通，原文由"侏儒工程兵团"的口吻写成；这是开发者对玩家的公告，不是世界内事件。
  tag: ⚠️
  source: Warcraft Wiki - Patch 0.10（补丁说明原文复刻）
  source_url: https://warcraft.wiki.gg/wiki/Patch_0.10
  quote: "The Gnomish Engineering Corps has been hard at work building a subway to connect the great cities of Ironforge and Stormwind City. Final work on this new mass transit system was completed recently, allowing us to announce the Grand Opening of the Deeprun Tram! Two trains make round trip runs between Stormwind City and Ironforge regularly, allowing quick and easy access to all your shopping and training needs. If you happen to miss a train, you only need to wait a few minutes for a new one to appear. We only ask that you be careful during your trip as the run out of the tunnel can be long and uneventful should you happen to fall off the tram during transit."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "站台墙上一块黄铜色铭牌，铭牌四角以铆钉固定，表面为哑光黄铜、边缘氧化成暗褐色，刻满密排小字"
  negative: "电子屏, 现代海报, 纸质告示, 发光字"

- fact_id: stormwind.event.004
  claim: 该补丁说明由第三方独立复述过，措辞一致，可交叉印证不是维基编者的再创作。
  tag: ✅
  source: Engadget「WoW Archivist: World of Warcraft beta patch 0.10」
  source_url: https://www.engadget.com/2011-04-12-wow-archivist-world-of-warcraft-beta-patch-0-10.html
  quote: "The Gnomish Engineering Corps has been hard at work building a subway to connect the great cities of Ironforge and Stormwind City. Final work on this new mass transit system was completed recently, allowing us to announce the Grand Opening of the Deeprun Tram!"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "（交叉印证，不入画）"
  negative: ""

- fact_id: stormwind.event.005
  claim: 0.10 补丁的发布日期是 2004 年 9 月 18 日；到 2026 年 9 月 18 日恰好整二十二年——这是现实层面可以正大光明说的周年数字。
  tag: ✅
  source: Warcraft Wiki - Patch 0.10（信息框发布日期）
  source_url: https://warcraft.wiki.gg/wiki/Patch_0.10
  quote: "September 18, 2004"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（现实日期，可用于片尾字卡，不入画面内世界）"
  negative: "把 2004 年当成世界内年份"

- fact_id: stormwind.event.006
  claim: Vanilla 的世界内当下是 Year 25 ADP；地铁开建于 6 ADP，因此旅行者到访的这一天，这条线已经运营了约十九年，"当天通车"与版本锚点直接冲突。
  tag: ⚠️
  source: Warcraft Wiki - ADP / Deeprun Tram History 两处年份相减
  source_url: https://warcraft.wiki.gg/wiki/ADP
  quote: "ADP is shorthand for After the Dark Portal ... Vanilla World of Warcraft takes place 25 years after the Dark Portal opening."
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "（时间线判定，不入画）"
  negative: "Vanilla 场景里出现在建工地、脚手架、未完工隧道"
```

### 1.4 车站形制

```yaml
- fact_id: stormwind.tram.016
  claim: 暴风城端的线路通过矮人区东侧的一条隧道进入，隧道口被一个巨大的旋转齿轮围住；铁炉堡端的入口是同样的巨大旋转齿轮形制。
  tag: ✅
  source: Warcraft Wiki - Travel guide to Deeprun Tram and boats
  source_url: https://warcraft.wiki.gg/wiki/Travel_guide_to_Deeprun_Tram_and_boats
  quote: "through a tunnel at the east-most side surrounded by a great big rotating gear as in Ironforge"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "隧道口外圈是一枚直径数倍于人高的巨型齿轮，铁灰色铸铁齿牙，齿面有黄铜色镶边与铆钉，齿轮绕洞口缓慢转动，洞口内部黑暗"
  negative: "静止齿轮, 木门, 石拱门, 吊桥, 发光法阵"

- fact_id: stormwind.tram.017
  claim: 中文侧的描述同样指认入口为"旋转的大螺母/齿轮状的门"，位于暴风城矮人区，可与英文来源交叉印证。
  tag: ✅
  source: 游侠网 - 魔兽世界暴风城地铁位置介绍
  source_url: https://gl.ali213.net/wenda/44533.html
  quote: "玩家能看到一个齿轮状的门 ... 在这里可以找到一个旋转的大螺母，进入到这个地点后就可以来到矿道地铁"
  tier: T3
  verified_by: ai_draft
  used_in: []
  prompt_string: "（交叉印证，形制串见 016）"
  negative: ""

- fact_id: stormwind.tram.018
  claim: 暴风城矮人区本身是第二次战争后为安置麦格尼国王派来的工匠而设立的聚居区；区内的锻炉持续吐出烟霭，伴随不断的铁锤敲击声。
  tag: ✅
  source: Warcraft Wiki - Dwarven District
  source_url: https://warcraft.wiki.gg/wiki/Dwarven_District
  quote: "The forges in the district produce a constant haze, supplemented by the constant strokes of smiths' hammers."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "街面上方悬着一层灰白色烟霭，烟霭被锻炉口的暖橙色火光从下方染出边缘，锤击声的节奏感通过飞散的火星表现"
  negative: "清澈天空, 无烟, 冷清街道；若该镜画面里没有锻炉炉口，则不得出现暖橙色火光"

- fact_id: stormwind.tram.019
  claim: 矮人区的房屋是把人类"过大而浪费"的原设计加层、分隔后改造成矮人尺度的；该区是商业与工业中心，工坊通宵开工。
  tag: ✅
  source: Warcraft Wiki - Dwarven District
  source_url: https://warcraft.wiki.gg/wiki/Dwarven_District
  quote: "large houses heavily modified for dwarf use with additional floors and rooms dividing the original, overly large and wasteful, human designs ... the local factories work all night to supply Stormwind with all of its goods."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "人类比例的高大石屋被硬塞进夹层，窗户被横向切成上下两排，门框加低，木构件与石墙的接缝粗糙外露"
  negative: "统一风格的新建筑, 精致对称立面"

- fact_id: stormwind.tram.020
  claim: 铁炉堡一侧的次序是【先有车站、后有街区】——侏儒失去诺莫瑞根后，是在铁炉堡矿道地铁车站已经建成的那个区域里造起了机械侏儒区。
  tag: ✅
  source: Warcraft Wiki - Tinker Town
  source_url: https://warcraft.wiki.gg/wiki/Tinker_Town
  quote: "The gnomes constructed Tinker Town in the district where the Ironforge Deeprun Tram station had been built."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（叙事事实，可作口播——这座街区是围着车站长出来的）"
  negative: ""

- fact_id: stormwind.tram.021
  claim: 机械侏儒区围绕一台巨大的球形机械展开，机械上附有一个小王座。
  tag: ✅
  source: Warcraft Wiki - Tinker Town
  source_url: https://warcraft.wiki.gg/wiki/Tinker_Town
  quote: "the district is built around a large spherical machine with a small throne attached to it."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一台数层楼高的球形金属机械，外壳为铆接铁灰色钢板与黄铜色环箍，球体侧面伸出一座小型座椅"
  negative: "水晶球, 魔法装置, 木质结构"

- fact_id: stormwind.tram.022
  claim: 两座车站内都设有坡道，供从轨道层爬回站台。
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram，Notes
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "There are ramps in the two stations to climb out."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "站台端头一道向下的石砌斜坡，坡面有横向防滑凿槽，接入轨道层"
  negative: "电梯, 楼梯, 扶梯"

- fact_id: stormwind.tram.023
  claim: 乘客不会被矿车碾到——掉下站台的话，车会无害地从头顶开过。
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram，Notes
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "You cannot be 'run over' by the Deeprun Tram. Should you fall off the platform, the train will pass harmlessly over your head."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "仰角：车厢底盘自画面上方掠过，底盘为铁灰色铆接钢板，轮对与轨道之间火星四溅"
  negative: "碾压, 血, 撞击, 惊恐尖叫"
```

### 1.5 矿车与运营

```yaml
- fact_id: stormwind.tram.024
  claim: 全线共两列车，每列三节车厢，跑在双轨上（一去一回）。
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram（首段）
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "two sets of three wagons"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "三节车厢串成一列，节与节之间以短连杆相接，车厢等长等高，无独立车头"
  negative: "单节车厢, 五节以上, 蒸汽机车头, 驾驶室"

- fact_id: stormwind.tram.025
  claim: 单程运行时间 60 秒，每站停靠 12 秒。
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram，Notes
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "The transit time between each end is 60 seconds and remains at each stop for 12 seconds."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（运营参数，可作口播数字）"
  negative: ""

- fact_id: stormwind.tram.026
  claim: 补丁说明称两列车"定期往返"，错过一班只需等几分钟就会有新的一班出现。
  tag: ✅
  source: WoW Patch 0.10 补丁说明
  source_url: https://warcraft.wiki.gg/wiki/Patch_0.10
  quote: "Two trains make round trip runs between Stormwind City and Ironforge regularly ... If you happen to miss a train, you only need to wait a few minutes for a new one to appear."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "（运营参数，可作口播）"
  negative: "固定时刻表, 站牌上的发车时间表"

- fact_id: stormwind.tram.027
  claim: 补丁说明明确警告：行驶途中如果掉下矿车，从隧道里走出去的路会很长、很枯燥。
  tag: ✅
  source: WoW Patch 0.10 补丁说明
  source_url: https://warcraft.wiki.gg/wiki/Patch_0.10
  quote: "We only ask that you be careful during your trip as the run out of the tunnel can be long and uneventful should you happen to fall off the tram during transit."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "一个人影独自沿轨道走在空隧道里，人在画面中极小，隧道向纵深收束成一点"
  negative: "有人接应, 照明充足的近景, 短隧道"

- fact_id: stormwind.tram.028
  claim: 每天都有侏儒在这条线上做维护，以保证运行平稳安全、出了问题能被迅速处理。
  tag: ⚠️
  source: 多个魔兽百科转述（未能定位到带页码的一手引注，按 T3 收）
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "To keep the tram running smoothly and safely, there are gnomes that work on it daily, so any problems with it can be quickly addressed."
  tier: T3
  verified_by: ai_draft
  used_in: []
  prompt_string: "轨道边一名侏儒工人蹲跪着，腰间挂满黄铜色扳手，面前摊开一块油污的深褐色帆布工具垫"
  negative: "大规模施工队, 重型机械, 人类工人"

- fact_id: stormwind.tram.029
  claim: 【设定没写】矿车的动力来源（蒸汽 / 发条 / 魔法）、有没有司机、如何启动，在所有可及来源中均无记载。
  tag: ⚠️
  source: 遍查 Warcraft Wiki 主条目、Gnomish technology、0.10 补丁说明，均无动力描述
  source_url: https://warcraft.wiki.gg/wiki/Gnomish_technology
  quote: "all credited to the gnomes' technical engineering."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（空白项——若要拍，须按侏儒机械逻辑推：铆接钢板、外露齿轮、无明火锅炉，并在口播标注为推测）"
  negative: "明火锅炉, 冒黑烟的烟囱, 发光魔法核心, 缰绳牵引"

- fact_id: stormwind.tram.030
  claim: 与部落飞艇不同，矿道地铁没有联盟卫兵把守；在 PvE 服务器上它属于中立区域。
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram，Notes
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "Unlike Horde zeppelins, the Deeprun Tram is not guarded by Alliance guards. ... On PvE realms, the Deeprun Tram is neutral territory"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "站台上没有任何披甲卫兵、没有岗哨、没有盘查"
  negative: "卫兵, 岗亭, 检查哨, 长戟"
```

### 1.6 隧道与水下段

```yaml
- fact_id: stormwind.tram.031
  claim: 所谓的"水下段"其实是一个地下湖——与施工期遇到的那个地下湖是同一个东西。
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram，Notes
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "The underwater section of the tram is, in fact, a subterranean lake."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "隧道穿过一片幽闭的地下水体，水色为深墨绿转青黑，无天光，光线只来自隧道自身，水面在上方看不见"
  negative: "海面, 天光, 波浪, 阳光光柱, 蓝色泳池水"

- fact_id: stormwind.tram.032
  claim: 这片大水域被设定为不可进入，但里面确实放了若干值得一看的物件。
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram，Notes
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "The large body of water the tram passes through is considered to be inaccessible, but does contain a few notable objects."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（可看不可达——镜头只能隔着通道往外看）"
  negative: "乘客下水, 游泳, 潜水"

- fact_id: stormwind.tram.033
  claim: 水下段里有：一口宝箱、一名潜水员、数艘沉船、一头名叫 Nessy 的大型生物、一只巨蚌、两只娜迦海妖、以及一条姥鲨。
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram，Notes
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "a treasure chest, a diver, shipwrecks, a large beast named 'Nessy', a giant clam, two Naga Sirens, and a Basking Shark."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "水底散布：半埋在灰褐色淤泥里的木质沉船残骸、一口带黄铜色包角的木箱、一只半开的巨大灰白色蚌壳"
  negative: "珊瑚礁, 热带鱼, 海草丛, 沉船宝藏金光"

- fact_id: stormwind.tram.034
  claim: Nessy 是一头 threshadon 类的 boss 级生物，位于矿道地铁隧道的水域中，玩家无法接近；它是对尼斯湖水怪的致敬。
  tag: ✅
  source: Warcraft Wiki - Nessy
  source_url: https://warcraft.wiki.gg/wiki/Nessy
  quote: "Water feature in the Deeprun Tram tunnel ... Nessy is inaccessible to players. ... Nessy is a reference to the Loch Ness Monster."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一头长颈巨兽在深水远处缓慢游过，体色青灰偏墨绿，颈部细长、躯干厚重、四片桨状鳍，轮廓被水雾软化，始终看不清全貌"
  negative: "清晰特写, 攻击姿态, 张口露齿, 发光眼睛, 近距离对峙"

- fact_id: stormwind.tram.035
  claim: 为了营造"整片水域是连通的一大片"的错觉，Nessy 会游向远处、隔几分钟传送到另一侧再游一趟。
  tag: ⚠️
  source: Hidden Azeroth 探索文（无一手引注，作机制说明收）
  source_url: https://hiddenazeroth.com/2018/01/12/beneath-depths-exploring-deeprun-tram-aquarium/
  quote: "In order to give the appearance of the aquarium being part of one large connected body of water, Nessie will swim into the distance and teleport to the other side every few minutes."
  tier: T3
  verified_by: ai_draft
  used_in: []
  prompt_string: "（机制说明——拍摄上可用作"它总是从同一个方向再来一次"的节奏点）"
  negative: ""

- fact_id: stormwind.tram.036
  claim: Deeprun Diver 是一名戴着潜水头盔的侏儒，有时在矿道地铁水下段的水底游荡；可以右键点他，他会像普通侏儒平民一样打招呼。
  tag: ✅
  source: Warcraft Wiki - Deeprun Diver
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Diver
  quote: "Deeprun Diver is a gnome wearing a diving helmet who sometimes wanders at the sea bottom around Deeprun Tram's underwater tunnels. He can be right-clicked, in which case it greets you in the same way as a Gnome Commoner would."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "水底一名侏儒身着球形黄铜色潜水头盔，头盔正面圆形观察窗，厚重帆布潜水服为暗褐色，脚踩铅底靴，在淤泥上缓慢行走"
  negative: "现代潜水装备, 氧气瓶, 脚蹼, 紧身潜水衣"

- fact_id: stormwind.tram.037
  claim: Deeprun Diver 在 Vanilla 数据库中存在（NPC 14121），矿道地铁内有三个刷新点。
  tag: ✅
  source: ClassicDB（Vanilla 数据库）NPC 14121
  source_url: https://classicdb.ch/?npc=14121
  quote: "Deeprun Tram (3)"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（版本核验，不入画）"
  negative: ""

- fact_id: stormwind.tram.038
  claim: 由于引擎限制存在地理上的不自洽——矿道地铁实际上从"无尽之海"极小的一角底下穿过。
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram，Notes
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "the Deeprun Tram actually passes under a very small portion of 'The Great Sea'."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（地理注记，可作口播冷知识）"
  negative: ""

- fact_id: stormwind.tram.039
  claim: 矿道地铁有自己独立的载入画面，但它的行为是普通公共空间，不是队伍专属的副本实例。
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram，Notes
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "it has its own loading screen, but it functions like a regular public space, and not like the party-exclusive dungeon instances."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（机制注记，不入画）"
  negative: ""

- fact_id: stormwind.tram.040
  claim: 【设定没写】隧道的支撑结构、照明方式、水下段是否为玻璃穹顶、沿线有无中途停靠点或维修区，在文字来源中均无描述——只能靠看图确认。
  tag: ⚠️
  source: 遍查 Warcraft Wiki 主条目全文，无任何隧道构造/照明/玻璃的文字描述
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "a long, fully enclosed, underground (and partially underwater) set of double tracks"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（空白项——须人工看第 5 节参考图后填写；本路不代填）"
  negative: "在未看图前写死玻璃穹顶 / 拱肋 / 灯型"
```

### 1.7 Vanilla 当代的站内人物（25 ADP，全部可用）

```yaml
- fact_id: stormwind.event.007
  claim: 到了 Year 25 ADP（＝Vanilla 当下），老鼠问题依然存在，由 Monty 负责处理——这是这条线上【唯一一件有明确年份、且年份正好落在本片版本锚点上】的事件。
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram，History 节
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "By the Year 25 ADP, the rat problem remained and was handled by Monty."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "站台角落堆着捕鼠笼与麻绳，笼子为锈褐色细铁条编成，旁边一块手写的悬赏木牌"
  negative: "灭鼠药剂瓶, 现代捕鼠器, 魔法阵"

- fact_id: stormwind.tram.041
  claim: Monty 的头衔是「灭鼠专家」（Rat Extermination Specialist），是侏儒，站在铁炉堡一侧；他说话是一口海盗腔。
  tag: ✅
  source: Warcraft Wiki - Monty ＋ Wowhead Classic 任务 6661 文本
  source_url: https://www.wowhead.com/classic/quest=6661/deeprun-rat-roundup
  quote: "Avast ye scallywag. Arrrr... Arrrr ye looking fer work? We gots a serious rat problem down here an' not enough hands on the poop deck."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一名侏儒站在站台边，身形矮小、姿态叉腰，衣着为磨旧的深褐色皮围裙，腰后别着一支细长木笛"
  negative: "海盗帽, 独眼罩, 钩子手, 鹦鹉"

- fact_id: stormwind.tram.042
  claim: Vanilla 任务《Deeprun Rat Roundup》（任务 ID 6661）要求用「捕鼠笛」吹奏旋律，把五只活老鼠引回 Monty 处；必须活捉，右键会误杀。
  tag: ✅
  source: Wowhead Classic 任务 6661
  source_url: https://www.wowhead.com/classic/quest=6661/deeprun-rat-roundup
  quote: "All ye needs to do is take this here rat catchin' flute and play the melody around the vermin. They'll follow ye to the ends of the world! Just capture five of the little buggers and bring em back here. We needs em alive. Arrrrr..."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一支细长的浅色木笛横在手中；数只灰褐色老鼠排成松散一列跟在人身后，尾巴拖地"
  negative: "巨鼠, 怪物化老鼠, 发光老鼠, 老鼠攻击人"

- fact_id: stormwind.tram.043
  claim: Monty 要活老鼠是因为他弟弟 Nipsy 要用它们做烤串——"我兄弟需要它们还活蹦乱跳的，不然就馊了"。
  tag: ✅
  source: Wowhead Classic 任务 6661 完成文本
  source_url: https://www.wowhead.com/classic/quest=6661/deeprun-rat-roundup
  quote: "These'll werk nicely, matey. Me brother needs em still tickin' and kickin,' else they go sour... Ye don't want to taste no sour rat kabob."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（叙事事实——两端车站由一对兄弟串起来）"
  negative: ""

- fact_id: stormwind.tram.044
  claim: Nipsy 是侏儒商贩，站在暴风城一侧，卖「矿道鼠肉串」；他的吆喝是"在卡兹莫丹这一侧你找不到更好的鼠肉串了"。
  tag: ✅
  source: Warcraft Wiki - Nipsy
  source_url: https://warcraft.wiki.gg/wiki/Nipsy
  quote: "You'll find no finer rat kabob this side of Khaz Modan!"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "站台一侧的小摊，摊上一排穿在细铁扦上的深褐色烤肉串，摊面为粗木板，下方一只小炭盆"
  negative: "大型餐车, 精致餐盘, 现代烧烤架；若该镜不含炭盆入画则不得出现暖橙色火光"

- fact_id: stormwind.tram.045
  claim: Haggle 是一名麻风侏儒，在铁炉堡一侧漫无目的地游荡，翻垃圾、自言自语、睡觉。
  tag: ✅
  source: Warcraft Wiki - Haggle
  source_url: https://warcraft.wiki.gg/wiki/Haggle
  quote: "Haggle is a leper gnome located on the Ironforge side of the Deeprun Tram who is often seen wandering aimlessly, sifting through the trash, talking to himself, and sleeping."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一名病态瘦小的侏儒，皮肤呈灰绿色、有溃烂斑块，衣物为破烂的脏灰色布片，弓背蹲在一堆垃圾旁翻找"
  negative: "健康侏儒, 整洁衣物, 攻击姿态, 僵尸化"

- fact_id: stormwind.tram.046
  claim: Haggle 在 Vanilla 数据库中存在（NPC 14041），确认为经典旧世内容。
  tag: ✅
  source: ClassicDB（Vanilla 数据库）NPC 14041
  source_url: https://classicdb.ch/?npc=14041
  quote: "This NPC can be found in Deeprun Tram"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（版本核验，不入画）"
  negative: ""
```

### 1.8 版本错置警告（❌ 这些不能出现在 Vanilla 片里）

```yaml
- fact_id: stormwind.event.008
  claim: 比兹莫的搏击俱乐部（Bizmo's Brawlpub）开在暴风城车站下方，但那是 Year 30 ADP 的事（熊猫人之谜 5.1/5.3），Vanilla 时不存在。
  tag: ❌
  source: Warcraft Wiki - Deeprun Tram，History / Notes
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "In Year 30 ADP, Bizmo's Brawlpub was opened under the tram, in Stormwind's station. ... As of patch 5.1, it hosts the Alliance Brawler's Guild in Stormwind's station."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（禁止入画）"
  negative: "搏击俱乐部, 拳赛场, 观众席, 擂台, 赌注摊"

- fact_id: stormwind.event.009
  claim: 茉艾拉·萨沃里安在 28 ADP 麦格尼石化后入侵铁炉堡并关闭了地铁——那是大地的裂变时期，Vanilla 时未发生。
  tag: ❌
  source: Warcraft Wiki - Deeprun Tram，History 节
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "After the petrification of Magni in 28 ADP, Moira Thaurissan invaded Ironforge and closed the tram, isolating the dwarves in the city."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（禁止入画）"
  negative: "地铁停运, 封闭站口, 铁炉堡被封锁, 黑铁矮人把守"

- fact_id: stormwind.event.010
  claim: 「诺莫瑞根大奔跑」是每年十月的微型节日，路线穿过矿道地铁（铁炉堡站是第 11 关卡、暴风城站是第 12 关卡）——但它是军团再临 7.2.5 才加入的，Vanilla 时不存在。可作为"地铁上办活动"的先例参考，不可作为 Vanilla 事实。
  tag: ❌
  source: Warcraft Wiki - Great Gnomeregan Run
  source_url: https://warcraft.wiki.gg/wiki/Great_Gnomeregan_Run
  quote: "The Great Gnomeregan Run is a micro-holiday that takes place in October. In this gnome-themed, Alliance-only event, players can partake in a footrace from New Tinkertown in Dun Morogh to Booty Bay in the Cape of Stranglethorn."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（禁止作为 Vanilla 事实；仅作方案设计的先例参考）"
  negative: "赛跑关卡旗门, 计时牌, 现代赛事横幅"

- fact_id: stormwind.event.011
  claim: 暴风城入口前的那道坡道是 4.0.3a（大地的裂变）才加的，Vanilla 站口形制与之不同。
  tag: ❌
  source: Warcraft Wiki - Deeprun Tram，Patch changes
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "Patch 4.0.3a added a ramp before the Stormwind entrance."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（禁止入画）"
  negative: "暴风城站口前的坡道"
```

**统计：共 57 条（tram 46 ＋ event 11）；`ai_read` 51 条，`ai_search` 6 条。**

---

## 2. 矿道地铁形制卡

> **重要使用提示**：下列四段中，凡带 ⚠️ 的句子是**文字来源里没有、我按世界逻辑推的**。
> 隧道构造 / 照明 / 是否玻璃穹顶 / 矿车外形细节，**文字来源全都没写**（`stormwind.tram.029` / `040`）。
> 第 5 节的参考图必须由人工过一遍眼、把 ⚠️ 换成实测描述之后，形制卡才算定稿。

### 2.1 车站（两端）

```text
地下车站，站厅由整块岩体凿出，岩面为青灰色花岗岩，凿痕粗大清晰。站台为石砌，高出轨面约半人，
台沿以铁灰色铸铁包边、表面有防滑凸点。站台端头一道向下的石砌斜坡接入轨道层，坡面有横向凿槽。
站厅通向城市的那一侧是隧道口，洞口外圈套着一枚直径数倍于人高的巨型齿轮——铁灰色铸铁齿牙、
齿面黄铜色镶边与成排铆钉，齿轮绕洞口缓慢转动，是全站最醒目的形制符号。站内没有闸机、没有售票口、
没有披甲卫兵。⚠️ 照明推为侏儒式固定灯具（黄铜色灯罩、罩内暖色光源、以支架固定在岩壁上），
间距均匀、亮度偏低，光斑之间留有暗段——此项待看图核实。
两端差异：⚠️ 暴风城端在矮人区东侧，站厅之外即是烟霭与锤声的矮人工坊街；铁炉堡端在机械侏儒区，
街区本身是围着这座已建成的车站长出来的，站外机械密度更高。
```
- ✅ 齿轮洞口（`016`/`017`）、坡道（`022`）、无闸机无卫兵（`003`/`030`）、两端方位（`004`）、铁炉堡先有站后有街（`020`）
- ⚠️ 岩面材质、站台高度、灯具形制、光斑节奏

### 2.2 矿车

```text
一列三节车厢，节与节之间以短连杆相接，各节等长等高，全列没有独立车头、没有驾驶室、没有烟囱。
⚠️ 车体推为侏儒机械语汇：铆接铁灰色钢板车身，边角与围栏件用黄铜色金属，轮对外露、可见齿轮与连杆。
⚠️ 载客部分推为半敞式——有顶棚与立柱、侧面不封闭，故行驶中乘客能直接看见隧道与水下段掠过。
车启动与停靠均平稳（设定明写"快速平稳"），不冒黑烟、不见明火。
```
- ✅ 两列各三节（`024`）、快速平稳（`003`）、60 秒/12 秒（`025`）
- ⚠️ **车体材质、颜色、顶棚、座位、扶手、动力、有无司机——文字来源全部空白（`029`）。必须看图。**
- ❌ 禁止：蒸汽机车头、冒黑烟的烟囱、发光魔法核心、缰绳牵引、现代地铁车厢

### 2.3 隧道

```text
全封闭地下双轨。两条铁灰色钢轨嵌在深褐色枕木上，轨距窄。隧道自始至终无天光，光线只来自隧道自身的灯具。
⚠️ 支撑结构与断面形制、灯具形制与间距、沿线有无中途停靠点或维修区——文字来源无任何描述，待看图。
可确证的两件事：① 隧道很长——补丁说明警告"掉下车之后走出隧道的路会很长、很枯燥"；
② 它从无尽之海极小的一角底下穿过。
```
- ✅ 全封闭双轨（`001`）、隧道很长（`027`）、穿过无尽之海一角（`038`）
- ⚠️ 断面、拱肋、灯具、停靠点（`040`）

### 2.4 水下段（本线的戏眼）

```text
隧道穿过一片幽闭的地下水体——它不是海，是一个地下湖，正是当年施工时挖穿的那个地下湖。
水色深墨绿转青黑，无天光、无波浪、无阳光光柱；光线只来自隧道内部，越往水体深处越暗，远处消失在黑里。
水底散布着半埋在灰褐色淤泥中的木质沉船残骸、一口带黄铜色包角的木箱、一只半开的灰白色巨蚌壳。
水中有一头长颈巨兽缓慢游过——青灰偏墨绿体色，细长颈、厚重躯干、四片桨状鳍，轮廓被水雾软化，
自始至终看不清全貌；它游向远处，过一会儿又从同一个方向再来一次。另有一条姥鲨与两只娜迦海妖。
水底还有一名戴球形黄铜色潜水头盔、穿暗褐色厚帆布潜水服、脚踩铅底靴的侏儒，在淤泥上缓慢行走。
这整片水域是可看不可达的——乘客只能隔着通道往外看。
⚠️ 「玻璃穹顶」的说法在文字来源中查无实据；乘客能看见水下景物是确证的，但用什么看见（玻璃管 / 敞口通道 /
水被挡在某个边界外）未见记载，待看图。
```
- ✅ 地下湖（`031`）、不可进入（`032`）、物件清单（`033`）、Nessy 形态与不可达（`034`）、潜水员（`036`）
- ⚠️ 玻璃穹顶（**不可写死**）、水体照明来源、Nessy 循环节奏（`035`，T3）
- ❌ 禁止：珊瑚礁、热带鱼、阳光光柱、Nessy 特写或攻击姿态

---

## 3. 可拍画面清单（8 条）

| # | 画面 | 镜头看到什么 | 依据 |
|---|---|---|---|
| 1 | **齿轮洞口** | 旅行者走近矮人区东侧，画面被一枚缓慢转动的巨型铸铁齿轮填满，齿牙从画外转入、洞口在齿轮正中是一团黑——人走进那团黑里 | ✅ `016` |
| 2 | **烟霭中的矮人区街口** | 前景是锻炉口飞出的火星，中景一层灰白烟霭悬在街面上方，远景是被加层改造、窗户被横切成两排的人类石屋——锤声的节奏由火星的爆闪表现 | ✅ `018`/`019` |
| 3 | **站台候车** | 站台不是空的，是通勤的：矮人、人类、侏儒混杂站着，没有卫兵、没有闸机；台沿铸铁包边在灯下泛哑光 | ✅ `014`/`030`/`003` |
| 4 | **鼠肉串小摊** | 站台一角，Nipsy 的粗木摊板上一排细铁扦穿着的深褐色烤串，下方一只小炭盆；他正在吆喝 | ✅ `044` |
| 5 | **矿车进站 · 仰角** | 低机位贴着轨面：三节车厢自画面上方掠过，底盘铆接钢板、轮对与钢轨之间火星迸溅，然后停稳 | ✅ `023`/`024` |
| 6 | **隧道飞驰** | 车内视角向侧前方，隧道壁在画面两侧拉成速度线，灯具一盏盏掠过形成明暗节拍，纵深收束成一点 | ⚠️ 灯具形制待看图 |
| 7 | **入水一刻（全片的决定性瞬间）** | 岩壁两侧忽然退开，画面外侧从"石头"换成"深墨绿的水"——沉船残骸、半开的巨蚌、淤泥缓缓向后掠去，光一下变冷 | ✅ `031`/`033` |
| 8 | **Nessy 掠过** | 远处水里一道长颈剪影缓慢横穿，始终不清晰、不靠近、不张口；它游出画外，几拍之后又从同一个方向再来一次——旅行者转头追着看 | ✅ `034` ＋ ⚠️ `035` |

> 备选（若时长有余）：**水底的潜水员**——黄铜球盔的侏儒在淤泥上走过，抬头朝掠过的矿车挥了挥手（✅ `036`；"挥手"是 ⚠️ 推演，设定只说他会像普通侏儒一样打招呼）。

---

## 4. 「当天的大事」方案

> **先把话说死**：`stormwind.event.001` —— **矿道地铁没有任何通车典礼的设定记载**。
> `stormwind.event.006` —— **Vanilla 当天，这条线已经通了约十九年**。
> 所以下面没有一个方案能做到"既守 Vanilla 锚点、又拍到设定里真实存在的通车典礼"。**那个东西不存在。**
> 三个方案是三种不同的诚实处理方式，代价各不相同。

### 方案 A ✅ 推荐 ——「灭鼠日」：拍 25 ADP 这条线上真正在发生的事

把"当天的大事"从**工程事件**换成**市井事件**。

**成立需要的事实**
- ✅ `stormwind.event.007`：Year 25 ADP（正是 Vanilla 当下），鼠患仍在，由 Monty 处理。**这是全线唯一一件年份正好压在本片锚点上的事件。**
- ✅ `041`：Monty 是「灭鼠专家」，海盗腔，铁炉堡侧。
- ✅ `042`：捕鼠笛引鼠、须活捉五只（Vanilla 任务 6661，原文可直接当台词）。
- ✅ `043`：要活的，是因为他弟弟要拿去做烤串。
- ✅ `044`：弟弟 Nipsy 在**另一头**的暴风城站卖鼠肉串。
- ⚠️ 推测部分极少：只有"今天恰好是集中灭鼠的一天"这一句是安排，且不与任何设定冲突。

**能拍出什么**
一条由**一对分居两端的兄弟**串起来的地铁线：铁炉堡站台上，海盗腔的灭鼠工把木笛塞给刚下车的外乡人；
外乡人蹲在轨道边吹笛，灰褐色老鼠排成一列跟上来；矿车呼啸进站，队伍被惊散、重新聚拢；
笼子装车，人和鼠一起坐完这趟 60 秒；到了暴风城端，摊板上的铁扦、炭盆、吆喝——
**"这条线运的是货，是兵，也是他哥的老鼠。"**

**风险**：极低。全部在版本锚点内，无一处需要虚构典礼。
**代价**：它不是"工程日"的气质，是"通勤日/市井日"的气质。题眼要从"通车"改成"这条线今天照常在跑"。

---

### 方案 B ⚠️ 不推荐 ——「通车日」：把时间锚点从 Vanilla 搬到 6 ADP 施工期

如果**必须**拍通车，只能搬时间。

**成立需要的事实**
- ✅ `006`–`015`：第二次战争后重建、Magni 的两个动机、Mekkatorque 受托设计、派盘模型、17 区办公室、四名以上侏儒、地下湖、鼠患、向图拉扬汇报。素材其实相当厚。
- ⚠️ **典礼本身、剪彩、首班车、致辞、到场人物、竣工日期——全部是虚构。** 设定连竣工年份都没给（`event.002`）。

**能拍出什么**
未贯通的掌子面、脚手架、举着量具的侏儒、破口涌入的墨绿色地下水、派盘拼出来的模型被摆在图纸上、
第一列车驶进黑暗——**施工纪录片**比典礼好看得多，而且施工部分是有据可依的。

**风险：高，且是两重的。**
1. **撞版本锚点**：6 ADP 的暴风城仍在重建，矮人区刚刚设立，整座城的样子不是 Vanilla 的样子。选这个方案 ＝ **放弃 Vanilla 视觉锚点**，本站要重做全部城市形制——这会波及 W1–W6 其他各路的成果。
2. **典礼是纯虚构**：口播必须逐字明说"设定里没有写通车典礼，这一段是我们按工程逻辑推的"。

**结论**：除非系列愿意为本站单独换掉版本锚点，否则不要选。

---

### 方案 C ⚠️ 推荐次选 ——「工程日 · 大修后复通」＋ 把 0.10 补丁说明做成站台铜牌

一个不撞设定的折中：**今天不是通车日，是这条线年度大修后重新发车的那一天。**

**成立需要的事实**
- ⚠️ "年度大修/停运检修"整件事是虚构的——但它**不与任何已知设定冲突**：设定只说"每天有侏儒在这条线上维护"（`028`），从没说过有没有过集中检修。这是一块干净的空白，填它不会踩到任何既有记载。
- ✅ `event.003`：把 0.10 补丁说明那段文字做成站台墙上的**黄铜色铭牌**——它确实是暴雪写下的、关于这条线"开通"的唯一一段文字，措辞还正好是侏儒工程兵团的口吻（"Final work on this new mass transit system was completed recently"）。口播明说：**这段话来自开发者的通车公告，我们把它当成这条线自己的纪念碑。**
- ✅ `026`/`027`：铭牌上那两句"错过一班等几分钟"和"掉下去走出隧道的路会很长很枯燥"，原样刻上去就是最好的站台告示。
- ✅ `event.005`：2004-09-18 → 2026-09-18 恰好二十二年。若本片在 9 月 18 日前后发布，可在片尾打一张**现实层面的**真字卡："矿道地铁开通二十二周年"——这不是虚构，这是真事实。

**能拍出什么**
收工的维修侏儒把工具垫卷起来；铭牌被擦亮；第一列车重新发车、站台上的人一拥而上；
隧道灯一段段亮起来；入水一刻；Nessy 照常游过——**"它停了几天，今天又开始跑了。"**

**风险**：中低。典礼不存在，但"复通"只是把"每天都在维护"放大成"今天修完了"，没有反设定。
唯一要守的纪律：**口播必须明说这是推演**，铭牌那段引文必须说清是开发者公告而非世界内碑文。

---

### 推荐排序与理由

**A > C > B。**

- 选 **A**，因为它是唯一一个**零虚构**的方案，而且素材意外地好：一对分居两端的兄弟、一支笛子、一列跟着人走的老鼠、一根烤串——这条地铁线自己就长出了一个有头有尾的小故事，还正好卡在 Year 25 ADP。旅行者纪录片要的就是这种"我今天遇上了这么一档子事"。
- 若制片坚持"工程日/通车"的题眼，选 **C**：它保住了题眼，代价只是一句诚实的口播。
- **B 不要选**，除非系列愿意为这一站换掉 Vanilla 锚点并连带重做城市形制。

**无论选哪个，有一条是死的**：`stormwind.event.001` —— **不要拍剪彩、红绸、典礼台、贵宾致辞、礼炮。**
设定里没有这些东西，编一个不存在的通车典礼，比诚实地说"查不到"糟糕得多。

---

## 5. 参考图候选表

> ⚠️ **版权与用途**：全部为暴雪娱乐版权素材。**只作形制依据，不入画、不上传给任何生成模型。**
> 用法是人工看图之后，把第 2 节形制卡里带 ⚠️ 的描述换成实测的中文形制串。
> **我没有看过这些图**——只核出了它们的稳定直链。带 ⚠️ 的"预期内容"是按文件名推的，须人工确认。

| # | 文件 | 直链 | 预期内容 | 优先级 |
|---|---|---|---|---|
| 1 | Deeprun Tram - Strowmind entrance.jpg（原站拼写如此） | https://warcraft.wiki.gg/images/Deeprun_Tram_-_Strowmind_entrance.jpg | ⚠️ 暴风城端站口／齿轮洞口 | **最高**（填 2.1 两端差异） |
| 2 | Deeprun Tram - Ironforge entrance.jpg | https://warcraft.wiki.gg/images/Deeprun_Tram_-_Ironforge_entrance.jpg | ⚠️ 铁炉堡端站口 | **最高**（填 2.1） |
| 3 | Deeprun Tram wagon - Pearl of Pandaria.jpg | https://warcraft.wiki.gg/images/Deeprun_Tram_wagon_-_Pearl_of_Pandaria.jpg | ⚠️ 官方漫画《Pearl of Pandaria》中的**车厢**画面——目前唯一能定车体形制的候选 | **最高**（填 2.2 全部 ⚠️） |
| 4 | Tramunderwater.jpg | https://warcraft.wiki.gg/images/Tramunderwater.jpg | ⚠️ 水下段——判定"有没有玻璃穹顶"就看这张 | **最高**（填 2.4 关键 ⚠️） |
| 5 | Deepruntram.jpg | https://warcraft.wiki.gg/images/Deepruntram.jpg | ⚠️ 主图，可能是站台或隧道全景 | 高（填 2.1/2.3） |
| 6 | Deeprun Tram - Pearl of Pandaria.jpg | https://warcraft.wiki.gg/images/Deeprun_Tram_-_Pearl_of_Pandaria.jpg | ⚠️ 同一部漫画中的地铁场景（非车厢特写） | 高 |
| 7 | Deeprun Tram loading screen.jpg | https://warcraft.wiki.gg/images/Deeprun_Tram_loading_screen.jpg | ⚠️ 载入画面——通常是官方绘制的全景，气氛与色调参考价值高 | 中高 |
| 8 | WorldMap-DeeprunTram.jpg | https://warcraft.wiki.gg/images/WorldMap-DeeprunTram.jpg | ⚠️ 线路地图——可判读全线走向、水下段位置、有无中途节点 | 中（填 2.3 停靠点空白） |

**补充图源（未取直链）**：Wowhead Classic 区域页 `https://www.wowhead.com/classic/zone=2257/deeprun-tram` 的
Screenshots 标签页，是 Vanilla 版本实拍截图的集中处——**若要严守版本锚点，它比上表任何一张都更可靠**
（上表多数图未标注版本，`Pearl of Pandaria` 是熊猫人时期的漫画，车体形制可能已与 Vanilla 不同）。

---

## 6. 未查 / Open questions

**必须由人工看图解决（文字来源确认为空白）**
1. **矿车长什么样**——车体材质、主色、有无顶棚、座位、扶手、连接方式。文字来源全空（`029`）。→ 看候选图 3、6。
2. **水下段是不是玻璃穹顶**——乘客确实能看见水下景物，但"用什么看见"无记载。这是本片最重要的一个画面，**绝不能靠猜写死**。→ 看候选图 4。
3. **隧道断面与照明**——支撑结构、灯具形制、灯距、明暗节奏（`040`）。→ 看候选图 5、7。
4. **沿线有无中途停靠点或维修区**——无任何记载。→ 看候选图 8（线路图）。
5. **两端车站的实际差异**——文字只给了方位与街区性格，站厅本身的差异未知。→ 对比候选图 1、2。

**查不到、且大概率不存在的（不要再花时间）**
6. **全长与真实耗时**——设定只给游戏内的 60 秒，没有给世界内的里程或时长。（曾有第三方文章做过速度估算，`dotesports` 该文 403 无法读取，且属玩家推算，T4，只能作反例。）
7. **动力来源、有没有司机、怎么启动**（`029`）——遍查无果。若要拍，须按侏儒机械逻辑推并在口播标注。
8. **竣工年份**（`event.002`）——设定从未给出。
9. **通车典礼**（`event.001`）——**确认不存在**。这不是"没查到"，是"查遍了，没有"。

**留给其他路的（本路不越界）**
10. 0.10 补丁说明里"侏儒工程兵团（Gnomish Engineering Corps）"这个建制在世界内是否另有记载——本路只在补丁文本中见到，未在世界内设定中找到同名组织。若 W-机构路要用，需另行查证。
11. 暴风城矮人区的完整街区形制、商铺、居民构成——归城市布局路。

---

*W7 交稿。事实 57 条，`ai_read` 51。核心结论：官方译名是「矿道地铁」；通车典礼在设定中不存在；Vanilla 当天这条线已通车约十九年。推荐走方案 A（灭鼠日），次选方案 C（大修复通 ＋ 0.10 铭牌）。*
