# 《时空旅行》系列公共库 · glossary（称谓白名单 + TTS 读音表 + 台词纪律）

> **2026-09-14 起（系列 follow-up 008）当地人不开口**：本表的称谓白名单只用于旅行者在解说里提到别人时怎么叫（「脚店的大伯」「铺兵」），不再用于古人对白；TTS 专名读音表照常使用。
>
> **2026-09-18 起按站型分叉**：上句只对**游览型**站成立（sk1 等）。**Titanic 型**站按语言可考性分级开放 NPC 台词——sk3 伦敦 1666 是第一个，其 §1.2 白/黑名单**同时用于解说与对白**。见 `proposal.md` A §2 分型表。

> 首站 sk1（汴京 1120）建，逐站追加；每站新增一节。出处与 fact_id 见各站 `0_research/dossier.md` §10。
> 草案（2026-09-13，W5）：`verified_by: ai_read`，进 prompt 前需人工核原文页。

---

## 1. 称谓白名单 / 黑名单

### 1.1 sk1 · 北宋汴京（1120）

| 对象 | ✅ 中文白名单 | 英文版建议译法 | ⚠️ 可用不指认 | ❌ 黑名单 | fact |
|---|---|---|---|---|---|
| 皇帝（背称） | 官家 | "the Emperor" / 引号内保留 *Guanjia*（旁白解释一次「the Official Family」） | — | 皇上、万岁爷 | kaifeng.lang.001 |
| 陌生男子 / 顾客 | 官人、小官人（年轻） | "sir" / "young sir" | 客官 | 大人、公子 | 002 / 017 |
| 平辈男子 | 哥哥 | "brother" | — | 兄台 | 013 |
| 陌生女子 | 娘子、小娘子 | "ma'am" / "miss" | — | 姑娘、小姐、美女 | 003 |
| 已婚女摊主 | X 娘子（周娘子） | "Mrs. Zhou" | — | 老板娘 | 003 |
| 官员 | 姓＋官名（赵推官）；宰相＝相公；武官＝太尉 | "Magistrate Zhao" / "the Chancellor" / "Commander" | — | **大人**（宋人只叫爹）、老爷 | 004–008 |
| 官二代 | 衙内 | "the young master (an official's son)" | — | 少爷 | 007 |
| 店伙计 | 大伯（店中小儿子）、博士（酒博士） | "waiter"；旁白 *bóshì* 解释一次 | 主人家 | 小二、店小二 | 009 |
| 酒店女侍 / 跑腿 | 焌糟、厮波、闲汉、撒暂（旁白指认） | 音译＋一句解释 | — | 服务员 | 010 |
| 中介 | 行老、牙人 | "the labor broker" | — | 中介、经纪 | 011 |
| 富户 | 员外 | "Mr. Wang, a rich man" | — | 财主、老板 | 012 |
| 父母 | 爹爹 / 爹、妈妈 / 妈 | "dad" / "mom" | 娘娘（某些地区称母） | 娘亲、母亲大人 | 014 |
| 女子自称 | 我（默认）；奴家 / 奴（≤1 次） | "I" | 妾 | 本宫、小女子 | 015 |
| 男子自称 | 我（默认）；小人（对官）、某 | "I" / "this humble man"（对官一次） | 老汉、仆 | 在下、本官、鄙人 | 016 |
| 皇后（宫中） | 圣人 | "the Empress" | 娘娘 | 皇后娘娘（面称） | 018 |
| 平民人名 | 姓＋排行：李十六、周四娘、沈十九 | "Li Sixteen" / "Fourth Daughter Zhou" | — | 现代双字雅名 | 019 |

**英文版通则**：英文站当地人说英语，称谓走 *sir / ma'am / brother / young sir*；宋制专名（官家、衙内、博士、焌糟）只在旁白里保留拼音并解释一次，台词里用意译。

### 1.2 后续站追加位

- sk2 …（罗马 / 长安，开工时追加：拉丁 / 唐称谓白名单——唐人「阿郎 / 娘子 / 郎君」全部 ⚠️，见 proposal 候选卡）

---

## 2. TTS 专名读音表

> 拼音标调；「易错点」写配音最常读错的音。★ ＝ 本次抓到字典 / 注释页；无★ ＝ 通用读音（W5 依常用字典给出，配音前可再核）。
> **sk1 用法（2026-09-14，R1 R33）**：视频 prompt 与配音 prompt 的 `台词:` 由生成器逐字对齐，**台词里不括注拼音**（不用 §3 第 5 条的括注写法）；把本表整张导入 TTS 引擎的读音词典。

### 2.1 地名 / 年号 / 人名

| 专名 | 拼音 | 易错点 |
|---|---|---|
| 汴京 / 汴河 | biàn jīng / biàn hé | 不读 biǎn、biān |
| 宣和 | xuān hé | — |
| 崇宁 | chóng níng | 不读 zōng |
| 靖康 | jìng kāng | — |
| 绍兴（年号） | shào xīng | — |
| 州桥 | zhōu qiáo | 不是「洲桥」 |
| 东水门 | dōng shuǐ mén | — |
| 虹桥 | hóng qiáo | 不读 jiàng |
| 洛口 | luò kǒu | — |
| 泗州 | sì zhōu | 不读 sī |
| 艮岳 | gèn yuè | **不读 gěn** |
| 睦州 / 青溪 | mù zhōu / qīng xī | — |
| 张择端 | zhāng zé duān | — |
| 孟元老 | mèng yuán lǎo | — |
| 向氏（评论图画记） | xiàng shì | **姓氏读 xiàng，不读 xiāng** |
| 朱勔 | zhū miǎn | **勔 miǎn，不读 miàn / mǐn** |
| 蔡攸 | cài yōu | 攸 yōu |
| 童贯 | tóng guàn | 贯 guàn |
| 方腊 | fāng là | 腊 là |
| 吕淙 | lǚ cóng | 淙 cóng |
| 庄绰 | zhuāng chuò | 绰 chuò |
| 洪迈 | hóng mài | — |
| 蒋济 | jiǎng jì | — |
| 大定丙午 | dà dìng bǐng wǔ | — |
| 张耒 | zhāng lěi | **耒 lěi，不读 lái** |
| 丁都赛 | dīng dū sài | 都 dū，不读 dōu |
| 马行街 | mǎ háng jiē | **行 háng，不读 xíng** |
| 相国寺 | xiàng guó sì | 相 xiàng，不读 xiāng |

### 2.2 器物 / 服饰 / 食物 / 行当

| 专名 | 拼音 | 易错点 |
|---|---|---|
| 纲船 / 花石纲 / 汴纲 | gāng chuán / huā shí gāng | **纲 gāng，不读 gǎng** |
| 褙子 | bèi zi | **褙 bèi，不读 bēi** |
| 幞头 | fú tóu | **幞 fú，不读 pú / pǔ** |
| 鲊（鲊脯） | zhǎ | **不读 zhà / zuò** |
| 㸇（㸇冻鱼头） | zuǎn ★ | 汉典：㸇 zuǎn，义「烹」；极冷僻，旁白可只说「冻鱼头」 |
| 焌糟 | jùn zāo ★ | 焌另读 qū；《东京梦华录》语境读 jùn（gzstv 文）；配音取 jùn |
| 厮波 | sī bō | 厮 sī |
| 札客 | zhá kè | 札 zhá |
| 撒暂 | sǎ zàn | 暂 zàn |
| 馉饳 | gǔ duò | 两字都易读错 |
| 瓠羹 | hù gēng | **瓠 hù，不读 hú** |
| 饶骨头（叫卖） | ráo gǔ tou | 「饶」＝白送 |
| 丹雘 | dān huò | 雘 huò |
| 阑楯 | lán shǔn | 楯 shǔn（栏杆） |
| 雁柱 | yàn zhù | — |
| 阗塞 | tián sè | 阗 tián |
| 衮叠（纸衮叠） | gǔn dié | 衮 gǔn |
| 邸店 | dǐ diàn | 邸 dǐ |
| 牙人 / 行老 | yá rén / háng lǎo | **行 háng** |
| 交子 | jiāo zǐ | — |
| 一贯 / 缗 | yí guàn / mín | 缗 mín |
| 省陌 | shěng mò | 陌 mò |
| 石（粮） | dàn | **粮食单位读 dàn** |
| 斛 | hú | — |
| 料（五百料船） | liào | 船的载量单位 |
| 篙 / 梢工 | gāo / shāo gōng | 梢 shāo |
| 牵驾 | qiān jià | — |
| 汴河号子 | hào zi | 号 hào |
| 衙内 | yá nèi | — |
| 待制 / 推官 | dài zhì / tuī guān | — |
| 太丞 | tài chéng | 丞 chéng |
| 开封尹 / 少尹 | kāi fēng yǐn / shào yǐn | **尹 yǐn，不读 yīn**；少 shào |
| 六曹 | liù cáo | — |
| 稠饧 | chóu xíng | 饧另读 táng，此处取 xíng（R1 R33） |
| 杈子 | chà zi | **杈 chà，不读 chā** |
| 角带 | jiǎo dài | 角 jiǎo，不读 jué |
| 当铺 | dàng pù | **当 dàng、铺 pù** |
| 军巡铺 / 铺兵 | jūn xún pù / pù bīng | **铺 pù，不读 pū** |
| 一角（酒） | yì jiǎo | 盛酒的量器单位，不读 jué |
| 盘盏 | pán zhǎn | 盏 zhǎn |
| 傀儡 | kuǐ lěi | — |
| 刻漏 | kè lòu | — |

### 2.3 sk1 英文解说专名表（英文轨 voice_id 见 `sk1/2_世界观人设/casting.md`；按 shot 英文台词逐条抄，2026-09-14）

> 英文字幕、publish 英文文案、YouTube 自动配音抽听都按这张表拼写。改台词里的写法＝改生成器重跑，再回填本表。

| 中文 | 英文解说里的写法 | 说明 |
|---|---|---|
| 文 | wen | 钱的单位，不译成 coin；实数枚才说 coins（「两枚」＝two coins） |
| 一贯（钱） | one string of (copper) coins | — |
| 七十五陌 / 省陌 | seventy-five to the hundred | — |
| 时空考察队 | Time Expedition Team | 暂定（FIX_sk1 判断 4）；publish 英文文案不写队名 |
| 林问 | Lin Wen | — |
| 汴京 | Kaifeng | 英文一律用 Kaifeng；Bianjing 只进 YouTube 标签供搜索 |
| 宣和二年 | second year of Xuanhe | — |
| 清明 | Qingming / the Qingming Festival | — |
| 寒食 / 大寒食 | Cold Food / the Great Cold Food (day 105) | 大寒食≠清明（`festival.001/009`） |
| 《东京梦华录》 | The Dreams of the Eastern Capital | 列出处时写 *Dongjing Meng Hua Lu* |
| 《清明上河图》 | the Qingming scroll | 全称 *Along the River During the Qingming Festival* |
| 《文会图》 / 《瑞鹤图》 | Literary Gathering / Auspicious Cranes | — |
| 宋徽宗 | Emperor Huizong | — |
| 南宋 / 北宋 | Southern Song / Northern Song | — |
| 里 | li | — |
| 斗 / 石 | a peck / dan | — |
| 虹桥 | the Rainbow Bridge | — |
| 东水门 | the East Water Gate | — |
| 汴河 | the Bian River | — |
| 十千脚店 | the Shiqian tavern | — |
| 脚店 / 正店 | jiaodian / licensed brewers（S05）、grand wine house（publish） | — |
| 遇仙正店 | Yuxian | — |
| 彩楼欢门 | festoon gate | — |
| 焌糟 | juncao | — |
| 太平车 | taiping cart | — |
| 褙子 / 包髻 | beizi / baoji | — |
| 袋家 / 行老 / 闲汉 | daijia / hanglao / xianhan | — |
| 鞍马 | mounts | — |
| 赵太丞家 / 太丞 | Zhao Taicheng's / Taicheng | — |
| 马行街 | Mahang Street | 马行读 mǎ háng；shot15 英文台词已于 2026-09-14 改为 Mahang |
| 州桥 / 天汉桥 | Zhou Bridge / Tianhan Bridge | — |
| 御街 | the imperial avenue | — |
| 宣德楼 / 宣德门 | Xuande Tower / Xuande Gate | 楼＝城楼，门＝她穿过的门洞 |
| 大庆殿 | the Daqing Hall | — |
| 开封府 / 开封尹 | Kaifeng Prefecture / the Kaifeng yin | — |
| 尚书省 | the Secretariat | — |
| 包拯 | Judge Bao | — |
| 关扑 | guanpu | — |
| 迎祥池 | Yingxiang Pond | — |
| 摔脚 | shuaijiao | 口播点明 not wrestling |
| 铺兵 / 军巡铺的兵 | patrol soldier(s) | — |
| 瓦子 / 勾栏 | wazi / playhouses | — |
| 杂剧 / 丁都赛 | zaju / Ding Dusai | — |
| 两（银） | taels | — |
| 三更 / 五更 | the third watch / the fifth watch | — |
| 铁牌（报晓） | the iron plate | — |

---

## 3. 中文版台词纪律（五条，系列通用）

1. **现代普通话 ＋ 断代称谓白名单，二者缺一不可。** 语法、语气词、句长全按今天的人说话；只把「你 / 您 / 先生 / 小姐 / 大人」这些**称谓**替换成该站 ✅ 列。绝不生成古语（文言 / 拉丁语 / 「尔等」「此乃」）。
2. **黑名单零出现，白名单只用 ✅ 列口播指认。** ⚠️ 列（客官、老汉、娘娘…）可以说，但旁白不得把它当「宋制」讲；❌ 列只进纠错单元（记者说错→当地人纠正，一站一次）。
3. **自称默认「我」。** 「奴家 / 小人 / 某」每位受访者至多出现一次、只在第一次对陌生人或对官时；之后全用「我」。
4. **每句朗读过关。** 写完先在脑里念一遍：真人今天会不会这么说？有没有对仗、有没有唱礼腔（「众家新苗按序上前」这类）、有没有翻译腔？不过关就拆短句、换口语词。
5. **专名先查表再配音。** 台词里出现 §2 的字一律按表读；表里没有的先补表（带出处）再录；配音 prompt 的 `台词:` 行可在专名后括注拼音供 TTS（如「花石纲（gāng）」），成片字幕不显示括注。


---

## 1.2 sk3 · 伦敦 1666（Titanic 型 · **本站当地人开口**）

> **本站是系列第一个允许具名 NPC 说话的站**（`proposal.md` A §2 的 2026-09-18 站型分叉；I-7 按语言可考性分级开放）。
> 所以下表**同时用于旅行者的解说与 NPC 的对白**，与 sk1 只用于解说不同。
> 量尺不是印象，是计数——对 pepysdiary.com 全日记（1660-01-01–1669-05-31）逐词站内检索的**命中条目数**，
> 查询方式与逐条语境见 `sk3/0_research/parts/w5_language_customs_myths.md` §10.3。
> **下游若要新增一个称谓，照同样方式查一次再加，不要凭印象。**

### 称谓白名单（英语站）

| 对象 | ✅ 白名单 | Pepys 命中 | fact |
|---|---|---|---|
| 默认男性敬称（对上 / 平辈 / 陌生人通吃） | **Sir** | 2,019 条 | `london1666.lang.006` |
| 有身份的女性 | **Madam** | 73 条 | 007 |
| 已婚或有身份的城中女性 | **Mistress / Mrs.**（读作 Mistress） | 151 条 | 007 |
| 有身份的男性平民 | **Mr. / Master** | 极高频 | 007 |
| 礼貌请求 | **pray you**（**不是** prithee） | 163 条 | 005 |
| 市长 Bludworth | **my Lord Mayor**（`my Lord` 单用亦可） | 64 条 | 010 |
| 查理二世 | **his Majesty / the King** | 高频 | 010 |
| 约克公爵（火中实际指挥者） | **the Duke of York** | 高频 | 010 |
| Farriner 的身份说法 | **the King's baker**（Pepys 9/2 逐字） | 逐字 | 013-B |

### ⚠️ 可用但要克制

| 称谓 | 为什么打黄灯 | fact |
|---|---|---|
| **Goodman / Goody** | 是真词，但 Pepys 笔下 13 处**全部在乡下**（Brampton）。**放进 Cheapside 摊主嘴里＝把新英格兰殖民地口音搬进伦敦。** | 008 |
| **Goodwife** | 全日记 **0 命中**。学术上确有（乡村/殖民地），**无任何伦敦 1666 证据**。 | 008 |
| **your Worship** | **0 个真命中**（4 条全是 Mrs. Worship 这个姓 + 宗教义）。**不进台词。** | 009 |
| **prithee** | 词典上 17 世纪常见（复辟喜剧里很多），**Pepys 全日记 0 命中**。它是**戏台词**不是**街头话**。 | 005 |

### ❌ 黑名单

`thee / thou / thy / thine` 当日常（1666 年它的实际语用是**羞辱 / 拉平地位**——Pepys 把它动词化：`thou'd him all along`＝一路不给他体面；成系统 thee/thou 的是**贵格会**，正因此被起诉，让摊主这么说话＝把他写成正在被通缉的异见者）· `prithee / verily / forsooth / methinks` 堆砌（莎士比亚腔）· 维多利亚式客套（差 200 年）· 美式用语（gotten / sidewalk / I guess / okay / folks）· **`Gracechurch Street`（1666 年它还叫 `Gracious Street`）** · `Sire`（法式奇幻用语，对查理二世是 `your Majesty` / `Sir`）· 仿古拼写进台词或字幕（`ye olde` / `doth` / `hath` 当口语）。

### 1666 年的街名写法＝当时读法（台词与字卡都用左列）

`Gracious Street`（今 Gracechurch）· `Canning Street`（今 Cannon）· `Fanchurch Street`（今 Fenchurch）· `Southwarke` · `Queenhith`。

---

## 2.2 sk3 · TTS 专名读音表（伦敦 1666）

> 全表 21 条见 `sk3/0_research/parts/w5_language_customs_myths.md` §10.5（含 IPA、1666 写法、依据）。此处只摘**一定会读错的**。

| 专名 | 给 TTS 的重拼 | ⛔ 陷阱 |
|---|---|---|
| **Pepys** | **PEEPS** | 绝不读 "PEP-iss" / "PEP-eez" |
| **Thames** | **TEMZ** | 绝不读 "THAYMZ"；`th` 不发 θ |
| **Southwark** | **SUDH-uk** | 绝不读 "SOUTH-wark" |
| **Holborn** | **HOH-bun** | `l` 不发音 |
| **Evelyn**（人名） | **EEV-lin** | 绝不读 "EV-uh-lin"（那是现代女名）⚠️ 建议人工二核 |
| **Bloodworth** | **BLUD-wurth** | 不读长 oo；**Pepys 自己的拼法是 `Bludworth`** |
| **Cheapside** | **CHEEP-side** | 不是「便宜」，是古英语 cēap＝市场 |
| **Wren** | **REN** | `W` 不发音 |
| **Gracious Street** | **GRAY-shus STREET** | **1666 年不叫 Gracechurch** |
| **Islington** | **IZ-ling-tun** | `s` 读 /z/ |
| **Whitehall** | **wyte-HAWL** | 重音在后 |
| **Queenhithe** | ⚠️ **未核** | **进片前必须补核，不要让 TTS 自由发挥** |
