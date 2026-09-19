---
station: sk3
city: 伦敦 London
date_old_style: 1666-09-01（儒略历，星期六）
span: 1666-09-01 清晨 → 1666-09-02 黄昏
event: 伦敦大火前一夜 + 大火第一日
series: shikong_lvxing
task_id: sk3-20260918-211545
research_date: 2026-09-18
---

# sk3 · 史料 dossier —— 伦敦 1666 年 9 月 1 日

> **事实的唯一出处是 `0_research/parts/w*.md` 里 yaml 围栏中的 `- fact_id:` 列表**（rule 4i ①）。
> 本文件只写**综合、表格与 `fact_id` 指针**，不复制 YAML。
> 机检：`python tools/facts_registry.py ai_videos/shikong_lvxing/sk3`
> 当前：**253 条事实 · 242 条 `ai_read` · 11 条 `ai_draft`（隔离，不得进 prompt）· ✅179 / ⚠️53 / ❌21 · blocker 0**
>
> **形态**：Titanic 型（见 `_series/format_teardown_chloe.md` §7 选站四问，本站四问全中）。
> 偏离登记见 `specs/ai_video/sk3/divergence.md` D1–D6。

## §0 先读这里 · 三件会改变创作的事

**① 9 月 1 日全天，没有任何可逐字引用的对白。** 所有能照念的原话都在 9 月 2 日凌晨之后（w5 §10.4）。这是「跨到 9 月 2 日黄昏」这个决定的直接原因（D5）。**严禁把 2 日的话搬到 1 日的嘴里。**

**② 流传最广的那句市长原话是假的。** 「Pish! A woman might piss it out」**不在皮普斯日记里**——全日记检索 "piss" 18 条命中无一出自 1666-09-02（`london1666.people.005`；w1 与 w5 独立复核一致，parent 另行逐字抓取 9/2 全文确认）。维基脚注指向 Malcolm《Londinium Redivivum》vol.4（1807，晚 141 年）。**Bloodworth 不得说这句。**

火场唯一合法的逐字直接引语只有一句（`people.004`，T0）：

> Lord! what can I do? I am spent: people will not obey me. I have been pulling down houses; but the fire overtakes us faster than we can do it.

那句传言可由旅行者**间接提及并当场点明「查无一手出处」**——本站独有的诚实亮点。

**③ 火场里其他人的话全是转述，没有原话。** 女仆 Jane、伦敦塔副官、国王、Houblon——皮普斯写的都是间接引语。**改写成引号内的直接引语就是伪造**（w5 §10.4 B）。只能做旁白或字卡。

### §0b 待人工抽查（进 prompt / 进台词前必须核成 `human`）

| # | fact_id | 为什么 |
|---|---|---|
| 1 | `people.005` | pepysdiary 底本是 Wheatley 1893 版，**该版对秽语有删节**。要彻底定论须查 Latham & Matthews 版第 7 卷 9/2 条；Malcolm vol.4 三份 archive.org 扫描件 OCR 全坏 |
| 2 | `timeline.003` | Farriner 晚 8–9 点打烊、女儿 Hanna 午夜巡查——**整集就架在这个时刻上**，却是全 dossier tier 最低的一条（T2，Tinniswood 复原，节选未标注据何史料） |
| 3 | `timeline.011` | 起火时刻两份一手史料**对不上**：《伦敦公报》「one of the Clock in the morning」vs 伊夫林 9/2 条「This fatal night, about ten」。**⚠️ 2026-09-19 更正：w1 写的「差 11 小时」算不出来**——把伊夫林读成当晚 10 点是差 21 小时，读成前一夜 10 点是差 3 小时，9/2 上午 10 点是差 9 小时。**成片已改为不报数字、只说两份记载对不上**（不替史料裁决）。伊夫林那句到底指哪个「ten」，需人工判 |
| 4 | `timeline.004/.006` `people.007/.009` | 四条同引一份**人工转录 PDF**（Rege Sincera 1667），官方 Gazette 扫描件无文字层无法交叉核对；转录件已见手误 |
| 5 | `coord.002` | 儒略/格里高利 10 天差是**按规则推的**，读到的原文只说「10 或 11 天」 |
| 6 | w5 §10.4 全部 quote | 本站是第一个允许 NPC 开口的站，**台词合法性不能建在未经人眼核对的抓取上** |

---

## §1 时空坐标 · w1（`coord.001–006`）

1666 年 9 月 1 日（儒略历）＝ **星期六**；次日 9 月 2 日皮普斯亲笔开篇「(Lord's day)」。

干旱与东风**两条独立 T0 互证**：1667 年 Rege Sincera 小册「the preceding Summer which was extraordinarily hot and dry, the East wind that blew violently all that while」；皮普斯「after so long a drought…even the very stones of churches」；伊夫林「a fierce eastern wind in a very dry season」；《伦敦公报》「a violent Easterly winde fomented it」。

## §2 城市地图与街区 · w2（`city.001–026`）

- **旧伦敦桥不是连贯的房屋长廊**：1633 年火烧掉北端 42 栋，**到 1666 年仍未重建**，只钉松木挡板防人落水——这道 33 年的空档正是挡住火烧向 Southwark 的防火带。正确形态：北端光桥面＋木挡板 → 中段密集房屋（4–5 层，每隔一栋一道跨街 cross building）→ Nonsuch House → 吊桥段 → 南端石门（顶上插头颅）。`city.006–010`
- **旧圣保罗：无尖顶、无圆顶。** 1561 年雷击后尖顶从未重建，1666 年只剩 204 ft 方塔残段，外包 Inigo Jones 的石灰岩古典皮，西端十柱×四排、柱高 45 ft 柱廊，**整座教堂架满勘修脚手架**。**航拍最容易画废的一处。** `city.018–022`
- **方位纠正**：Old Swan 在桥**上游西侧**、Swan Lane 底；布丁巷在桥**下游东侧**。两者不相邻。与布丁巷贴身的是 Fish Street Hill（西）、Botolph Lane（东）、Little Eastcheap（北）、Thames Street（南）。
- **建模原点**：Monument 现址 ＝ 起火点**正西 202 ft（61.6 m）**。以它为原点建 blend，全片位置关系锁死。
- **天际线** ＝ 约 100 座教堂塔的森林 + 一座**顶是平的**巨物；**大气是煤烟不是清空气**（伊夫林《Fumifugium》1661：旅人「在许多英里之外先闻到、而不是先看到这座城」）。
- **一日路线 5 站 + 宿**：桥 → 布丁巷 → 泰晤士街码头 → 交易所/Cheapside/Guildhall → 旧圣保罗/Ludgate → 回 Fish Street Hill 客栈过夜。纯步行 62–72 min。全表见 w2 §2g。
- **整城白模建模要点**（四级精度分级、模数表、航拍飞行路径、一镜到底选段）见 w2 §2b。其中一条算过的硬约束：**跟拍 27 s 只能走约 35 m**，所以「一镜穿完 Fish Street Hill 再拐进布丁巷」（330 m）物理上不可能——一镜到底首选**布丁巷南半段 38 m**（Thames Street 口 → 面包铺门前）。

## §3 衣 · w3（`dress.001–023`）

- **【头号时代错乱】波斯式外套 vest 是火灾之后的事**：查理二世 **1666-10-07** 才在枢密院宣布，比本站晚五周、且大火夹在中间（两条皮普斯 T0 原文）。9 月 1 日男装仍是**短 doublet + petticoat breeches（鹅笼裤）**，后者在英格兰正好流行到 1666 年为止。
- **【第二大误传】清教徒黑衣**：黑染料贵且易褪，黑衣是主日与画像用的最好衣裳；实际色系是 1638 年清单里的 "sadd colours"（russet / 枯叶褐 / 茶褐 / 肝褐 / 法国绿）。高顶窄檐 capotain 到 1666 年已过时十几年，**帽上那枚方形金属扣纯属 19 世纪想象**。
- **五套锁定描述串**（中等市民女性 / 劳动阶层男性 / 中等商人男性 / 女仆 / 旅行者本人）已按模板写好、每串带「不是 X」子句，见 w3 §3.1，可直接进人物锚点图 prompt。

## §4 食 · w3（`food.001–029`）

- **禁**：土豆（1662 年皇家学会才推广，富人花园稀罕物）、番茄（毒苹果，纯观赏）、玉米、辣椒（1669 年伊夫林才有第一条食谱用法）。
- **不禁但要写对**：**巧克力 1666 年伦敦有**（皮普斯 1664-11-24「to a Coffee-house, to drink jocolatte, very good」——禁的是固体巧克力，热饮成立）；**茶有但极稀**（英语首条喝茶记载就是皮普斯 1660-09-25「a cup of tee (a China drink) of which I never had drank before」——**「英国人＝喝茶」在 1666 年完全不成立，是极好的反差点**）；火鸡 1570 年代就传入、1660 年代常见。
- **叉子**：1666 年平民不用，靠手指 + 刀尖 + 勺；「意大利式外国做作」。上流餐桌可有（双齿）。
- **⚠️ 会影响分镜的硬约束**：咖啡馆名义开放、**实际排除体面女性**（1674《Women's Petition Against Coffee》）。「一口一问」设在咖啡馆时她**进不去**——w3 §4.4 给了三种有意设计的处理（门口口播 / 硬进去把「被排除」拍成戏 / 改去酒馆），**别让它变成穿帮**。
- 两顿可拍的饭：街头（正午）+ 咖啡馆或酒馆（下午），见 w3 §4.6。

## §5 住 · w2（`housing.001–020`）

- **jetty 逐层外挑 0.35–0.55 m，四层累计 1.4–1.6 m**，lane 顶部净空只剩 1.5–2 m。1667 年法要求拓宽「一切窄于 **14 ft** 的通道」→ 反推火前大量 lane < 4.3 m。四等房层高（10/10.5/9/8.5 ft）可直接当层高表。
- **法规存在且被无视**：1661 年查理二世公告禁 jetty 与悬挑窗，被地方当局无视；1665 年更严厉的一份同样无效。都铎至斯图亚特早期至少 3 部法案 + 9 道公告，市民「几乎不予理会」。
- **9 月 1 日夜里没有任何公共照明**。1416 年挂灯令只覆盖 Hallowtide–Candlemas 的冬夜；住户每晚挂灯是大火**之后**（1668）的规定；玻璃罩路灯 1683 年才第一次出现在 Cornhill。夜戏只有窗内烛光、角质提灯和月亮。`housing.013`
- 客栈：回廊式、门洞进院、后院马厩与干草堆、共睡的床。`housing.016/.018`

## §6 行 · w4（`transport.001–017`）

泰晤士河是真正的主干道；**1666 年船夫正在被强征入海军**——皮普斯 T0 原话「could not get watermen; they being now so scarce, by reason of the great presse」，**唯一一条 1666 年限定的交通摩擦，建议至少一镜**。

1662 年出租马车法（逐字法条，T0）：400 辆牌照上限、£5/年、**10s/天（12 小时）、头一小时 18d、之后 12d**。轿子 sedan chair 已有。

## §7 物价与货币 · w4（`price.001–024` `money.001–010`）

- **锚 A · 面包**：Assize of Bread 锁的是**价格不是重量**——**一便士永远买一条面包，涨价的方式是把面包做小**。最接近的可核重量是伦敦自己的记录：penny wheat loaf 13→17 oz（1618–19，T0，⚠️ Δ−47 年）。**1666 年的重量查不到，未内插。**
- **锚 B · 日工钱**：国王工程署 1660 年伦敦塔与白厅账目（T1 引 TNA WORK 5/1）——**小工 16d/天、石匠木匠 24–30d/天**。以 **16d 为全片唯一除数**。⚠️ 这是承包商报价，实际到手低 20–30%。
- **冷开场口播锚**：**小工一天 ＝ 16 条面包；工匠一天 ＝ 30 条面包。**
- **猜价格卡（≥1 张）**：**雇一小时马车 18d ＞ 小工一整天 16d。**
- **私铸代币**：城墙内 1648/9–1672 年有 **4,000 多种**，铜/黄铜，**只能在发行的那家店兑**——「出了这条街它就不是钱了」字面属实。旅行者该带银先令 + 当地铜代币。
- **几尼 1666 年是商品不是钱**：皮普斯的金匠当年 11 月把兑换升水从 18½d 提到 22d，「very few to be had at any price」。
- §7.3 价格表 32 行，每行 `÷16d ＝ 几天工钱` + fact_id + 年代差标注，**全表零现代货币换算**。

## §8 职业与社会阶层 · w4（`work.001–031`）

八种人：面包师（Farriner，当天的主角）· 煤炭搬运工（火的燃料）· 船夫 · 酒馆/咖啡馆女性从业者 · 学徒 · 教区 constable / ward beadle / 更夫（官方视角）· 街头小贩 · 清道夫掏粪工。阶层速查表见 w4 §8.9。

**1662 年同一部法令要求住户每周三、周六自扫门前**——**而 9 月 1 日正是周六**，这条定死了全片的街道基准状态。

## §9 节令与习俗 · w5（`custom.001–011`）

瘟疫刚过去但没过干净；宵禁钟 Bow Bells 每晚九点——**curfew 词源查实为真**：古法语 cuevrefeu「盖火」，中世纪敲钟命令压好炉火，**目的正是防止无人看管的炉火酿成大火**，而**那口钟自己次日就烧掉了**。免费的好钩子。

⚠️ **U4：1666 年伦敦哪天是集日没查到可靠证据，未核前不要在片中断言周六赶集。**

## §10 语言与称谓 · w5（`lang.001–014`）

- **档位：直接说现代英语（带极少量时代词），禁仿古拼写。** 依据是 1666-09-01 日记原文本身——「Up and at the office all the morning, and then dined at home.」句法与今天无异。
- **白/黑名单用可复核计数，不用印象**（pepysdiary 全日记 1660–69 站内检索并逐条看过上下文）：`Sir` 2,019 / `pray you` 163 / `Mistress` 151 / `Madam` 73 / `my Lord Mayor` 64 / `Goody` 10 / `thee` 6 / `thou` 5 / `your Worship` 4 / `Goodman` 3 / `Goodwife` 0 / `prithee` 0。三条推翻了默认假设：
  - **`your Worship` 4 条命中全是假的**（3 条是 Mrs. Worship 这个姓，1 条是宗教义）→ **撤下白名单，不进台词**。
  - **`Goody`/`Goodman` 全部出现在乡下**（Brampton）→ 放进 Cheapside 摊主嘴里等于把塞勒姆口音搬到伦敦。
  - **`thou` 5 条全在特殊语域**：临终私语、驱痉挛咒语、圣经引文、以及 `thou'd him all along`（把 thou 动词化＝一路不给他体面）。1666 年成系统 thee/thou 的是贵格会，正因此被起诉。
- **§10.4 合法弹药库**：唯一逐字直接引语（市长那句）+ 皮普斯 12 句 + 伊夫林 7 句第一人称原文（含 closer 候选 `London was, but is no more.`）。
- **§10.5 TTS 专名读音表**已产出。**追加一条（parent 复核所得）**：皮普斯日记注里市长的拼写是 **Bludworth**，不是 Bloodworth。

## §11 当日大事时间线 · w1（`timeline.001–014`）

全表见 w1 §11。骨架：

9/1 上午办公 → 午后**把新书房打扫干净「against to-morrow」** → 下午看木偶戏 Polichinelly、躲 Young Killigrew 一伙 → 傍晚 Islington 吃喝「mighty merry」→ **一路唱着歌回家** → 夜里写一两封信就寝
→ 约 20–21 点 Farriner 打烊、耙拢炉煤（⚠️ T2）→ 约 24 点女儿 Hanna 巡查（⚠️ T2）
→ **9/2 约 01:00 起火**（官方口径；伊夫林记「about ten」，两说对不上、未裁决，**不报小时差**）→ 帮工被烟呛醒 → 全家翻窗沿檐槽逃生，**女仆不敢跟、死在屋里**
→ 约 03:00 **Jane 叫醒皮普斯**，他判断「far enough off」回去睡 → 上午上塔楼、下船看全景 → 塔楼副官告知火起于「国王的面包师」家
→ **正午前面奏国王**，国王下令「spare no houses, but to pull down before the fire every way」→ 正午前后**坎宁街遇市长崩溃**。

> **本片最强的戏剧反讽**（w1 意外收获）：伊夫林日记 **1666-08-27**——大火前六天——他与**雷恩**勘查旧圣保罗，议定要给它加一个 "a noble cupola, a form of church-building not as yet known in England"。九天后教堂烧掉。旅行者站在脚手架下听他们规划那个圆顶，是白送的钩子。

## §12 可观察 / 可对话的人物 · w1（`people.001–013`）

- **真实人物（只念有记载的原话）**：皮普斯（**本站「跟着的那个人」**，D6）、伊夫林、Bludworth、Farriner、查理二世与约克公爵。
- **虚构但有据的四位 + 各自的「盼头」**（Titanic「问乘客到了美国要做什么」的等价物）：泰晤士街货栈搬工 / 比林斯盖特码头脚夫 / 泰晤士河船夫 / 圣保罗旁的书商学徒。全表见 w1 §12 B。

  **写作纪律**：前三位的盼头用「明天 / 下周」的短尺度，与 7 小时后的起火形成落差；第四位用「满师以后」的长尺度托底余味。**旅行者绝不剧透——问的人知道、被问的人不知道，镜头只拍被问者的脸。**

## §13 常见误传（本站）· w3 + w4 + w5（`myth.001–014` + 各部 ❌ 条目，共 21 条）

头三条：**茅草顶**（伦敦城内**自 1189 年禁茅草**，1666 年绝大多数是瓦顶——给图像模型的头号负向）· **长马甲 vest**（晚五周）· **Monument**（1671 年才动工，出现在布丁巷画面里就是穿帮）。

其余见各部 §13：清教徒黑帽扣、capotain、平民用叉子、新世界作物、`thee/thou` 满口、圣保罗有雷恩圆顶、「只死了 6 个人」、伦敦桥被烧毁、1665 年瘟疫车、Hubert 被处决（火**之后**的事，不得提前）。

## §14 未定与推测项（全部 ⚠️ 汇总）

- **禁止编数字的四项**（w2 §0③）：Cheapside 宽度 · 布丁巷宽度 · Thames Street 宽度 · 桥上房屋 1666 年栋数。
- **查不到、已标注未内插**：1666 年 penny loaf 重量 · 1666 年小麦每夸特价 · 1660 年代船夫资费（只有 1559 与 18 世纪两端）· 1660 年代 ale 零售价 · 1660 年代客栈住宿价 · 1666 年伦敦 assize 重量表。
- **两说并存待裁决**：伊丽莎白朝「政治性鱼日」法在 1666 年的实际约束力（直接决定她周六能不能点肉）· 起火时刻 11 小时冲突。
- **11 条 `ai_draft` 已隔离**（w4 五条 + w2 六条）：不得进 prompt、不得口播数字。
- **来源受限**：OED 需登录（改用 etymonline，tier 已下调）· Boulton 2000（唯一能给 1660 年代伦敦分项食品价的文献，两条 PDF 路径均 404/付费墙）· 1661/1665 两道公告原文只拿到 T3 转述，需查 *Stuart Royal Proclamations* · **建模前应以 Ogilby & Morgan 1676 实测图（100 ft/inch）套合替换 w2 的推算坐标**。

## §15 参考来源与参考图库 · w6

文献来源分组 T0/T1/T2 见各 part 文末；系列级来源库 `_series/sources.md`。

### 15a 参考图库（`0_research/refs/{asset}/`，索引 `refs.md` 进 git、图走 R2）

**130 张公版图，9 个资产全部过 ≥8 张门槛，257 MB；零重号。**

| 资产 | 张数 | 一手底本 |
|---|---|---|
| `bg0_london_panorama` | 12 | Hollar 1647 Long View、**Hollar 1666 火前/火后双联（Yale, CC0）**、Visscher 1616 |
| `bg1_london_bridge` | 11 | Visscher 1616、de Jongh 1632 油画、1682/1724 立面 |
| `bg2_old_st_pauls` | 15 | Hollar 为 Dugdale 1658 所作全套（西/北/南立面 + 中殿 + 唱诗席 + 平面），门廊与无尖顶状态对得上 |
| `bg3_pudding_lane_street` | 22 | Hollar 宅邸街景 + Laroon《Cryes》1687（Rijks CC0）+ Staple Inn 实物照 |
| `bg4_royal_exchange` | 10 | Hollar《Byrsa Londinensis》c.1647（Met + Yale, CC0） |
| `bg5_great_fire` | 14 | Verschuier / Ludgate 两张油画、Met CC0 火前火后双联 |
| `dress_restoration_1660s` | 26 | Hollar《Ornatus Muliebris Anglicanus》《Theatrum Mulierum》全套 Rijks CC0 |
| `map_london_1658` | 12 | Faithorne & Newcourt 1658、Hollar 火前火后对照平面 |
| `thames_watermen` | 8 | Hollar 河景 3 张 + Hondius《冰冻泰晤士河》1677 |

**许可逐图记录**：CC0 42 / PD 81 / CC BY 4 / CC BY-SA 3 / No restrictions 1。**127 张可入画**；3 张 CC BY-SA 现代照片按 ShareAlike 传染性标为「只进 prompt 不入画」（同一建筑另有一张 CC BY 2.0 可入画）。Royal Collection Trust 与大英博物馆按条款**未默认公版、直接跳过**。130 条 `evidences` 全部指向 w1–w5 已注册的真实 `fact_id`（37 个），零悬空。

### 15b img2img 可用性评估（下游阶段 2 建卡的直接依据）

1. **只有约 12 张油画能一步 img2img 出照片级**；其余约 100 张是**铜版线条画，必须两步走**（低 denoise 压线条 → 二次提 denoise 补材质），否则第一批图会全是「线描感照片」。
2. **人物不走 img2img**——版画线条会刻进脸。五套人物锁定串照 rule 18.1 走文字。详见 `divergence.md` D7 与 `ai_video.md` rule 18.1b。
3. **年代状态陷阱**：Visscher 1616 与 de Jongh 1632 画的伦敦桥北段是满的，而 1666 年那段自 1633 年火后一直空着（`city.008`）。**img2img 会忠实保留错误状态**，建卡时写死或切片避开。
4. **两个史料空白，提前认下、不靠 img2img 解决**：布丁巷式**窄巷平民民居无同时代图像存世**（火烧了实物、火前没人画平民窄巷）；泰晤士河客运 **wherry 无近景一手**。两者靠全景图切局部 + 白模 + 文字合成。
5. **hero 原始底片另存 `0_research/masters/`**（1 件 73 MB）。`ref_fetch.py pull` 固定取 `iiurlwidth=2000` 缩略图，130 张里 109 张恰好就是原尺寸，但 **Hollar 1647 长卷原图 28661×5560 被截成 3840px（7.5× 损失）**。masters **刻意放在 `refs/` 树外**——该图 5.15:1 超出上传窗口，留在 `ref/` 会被 `ref_aspect fix` 补边成 2.74 亿像素而毁掉；现 `ref_aspect check refs/` 为 0 outside。

### 15c 工具侧：`ref_fetch.py` 并发 bug 已修（2026-09-18）

`_next_index()` 是 read-then-write、`append_ref()` 是对 `refs.md` 的 read-modify-write，**同一 `asset_dir` 并行 pull 会互相覆盖**——本次实测出现 10 个重号、1 个文件漏进索引，整目录删掉串行重下才干净。已加**按 asset 目录的文件锁**（`.ref_fetch.lock`，索引分配与 refs.md 改写在锁内，下载在锁外），4 线程 48 次分配复测零重号。**不同 asset_dir 仍可并行。**

