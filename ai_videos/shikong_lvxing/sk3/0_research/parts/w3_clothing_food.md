---
worker_id: researcher-w3-clothing-food
stage: 0
role: researcher
angle: clothing-and-food
status: complete
blockers: []
confidence: medium
facts_ai_read: 53
facts_dress: 24
facts_food: 29
facts_negative_for_s13: 16
station: london-1666-09-01
run: sk3-20260918-211545
---

# W3 · 衣 + 食：伦敦 1666 年 9 月 1 日（大火前一夜）

> 供 `sk3/0_research/dossier.md` §3「衣」与 §4「食」合并。
> **所有 fact 均为本次抓取页面所得（`verified_by: ai_read`），进 prompt 前须人眼核原文页并改 `human`。**
> 色名一律零 hex。锁定串模板：`{形制名词}（{材质}，{色名}，{关键结构 2–3 处}），{穿着方式}；不是 {最常见误传形制}`。

---

## 0. 本站时间锚（先立这个，否则衣食全错）

**1666 年 9 月 1 日是星期六。** Pepys 当天日记标题就写着 `Saturday 1 September 1666`；大火在**次日（星期日 9 月 2 日）凌晨**从 Pudding Lane 的 Farriner 面包铺烧起来。所以本站拍的是**大火前最后一个平常的星期六**——街上一切如常，没有一个人知道明天会发生什么。

Pepys 这一天的日记全文很短，但对 vlog 极好用（他去看了木偶戏、去 Islington 吃喝、唱着歌回家）：

```yaml
- fact_id: london1666.dress.000
  claim: 1666-09-01 是星期六；Pepys 当天看木偶戏「Polichinelly」、到 Islington 吃喝、唱着歌回家。大火在次日（周日 9/2）凌晨才起
  tag: ✅
  source: The Diary of Samuel Pepys, Saturday 1 September 1666
  source_url: https://www.pepysdiary.com/diary/1666/09/01/
  quote: "Saturday 1 September 1666 … Sir W. Pen and my wife and Mercer and I to \"Polichinelly,\" … and so, the play being done, we to Islington, and there eat and drank and mighty merry; and so home singing, and, after a letter or two at the office, to bed."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "1666 年 9 月 1 日星期六傍晚的伦敦城内街道，一切如常：店铺还在开门，人们在街上吃喝说笑，没有任何火灾、烟尘、慌乱、逃难迹象"
  negative: "浓烟、火光、灰烬、逃难人群、废墟、烧塌的房子、末日氛围"
```

---

# §3 衣：1660 年代复辟时期伦敦日常服装

## 3.0 总纲（贯穿五套装束）

### 3.0.1 【本站头号时代错乱】「波斯式外套 vest」是**火灾之后**的事，9 月 1 日绝不可出现

这是本站最容易犯、也最致命的错。三条独立史料互相咬死：

```yaml
- fact_id: london1666.dress.001
  claim: 查理二世是 1666 年 10 月 7 日在枢密院（in Council）宣布要定一种永不更改的新服装；Pepys 10 月 8 日记「昨日」。这比大火（9/2–9/6）晚了整整一个月
  tag: ✅
  source: The Diary of Samuel Pepys, Monday 8 October 1666
  source_url: https://www.pepysdiary.com/diary/1666/10/08/
  quote: "The King hath yesterday in Council declared his resolution of setting a fashion for clothes, which he will never alter. It will be a vest, I know not well how; but it is to teach the nobility thrift, and will do good."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "（负向用）本站时点全城无一人穿及膝长身外套 vest / 三件套雏形"
  negative: "vest、波斯式外套、及膝长身外套、三件套、马甲+外套+马裤的组合"

- fact_id: london1666.dress.002
  claim: 国王本人第一次穿上 vest 是 1666 年 10 月 15 日。形制＝贴身黑呢长 cassock、下衬白绸挑花、外罩一件 coat、腿上系黑缎带如鸽腿
  tag: ✅
  source: The Diary of Samuel Pepys, Monday 15 October 1666
  source_url: https://www.pepysdiary.com/diary/1666/10/15/
  quote: "This day the King begins to put on his vest, and I did see several persons of the House of Lords and Commons too, great courtiers, who are in it; being a long cassocke close to the body, of black cloth, and pinked with white silke under it, and a coat over it, and the legs ruffled with black riband like a pigeon's leg; and, upon the whole, I wish the King may keep it, for it is a very fine and handsome garment."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "（负向用）9 月 1 日的伦敦男人上身是短到腰的 doublet，绝不是及膝长外套"
  negative: "长 cassock、黑呢及膝外套、白绸挑花衬里、鸽腿式黑缎带束膝"

- fact_id: london1666.dress.003
  claim: 「波斯式（Persian mode）」这个说法出自 John Evelyn；他 1661 年的小册子 Tyrannus, or the Mode 已在鼓吹英国人别再学法国、改穿波斯式 vest 与腰带，但那只是**提案**，真正落地是 1666 年 10 月
  tag: ✅
  source: John Evelyn, Tyrannus or the Mode (London, 1661)，经 Internet Archive 与 Bodleian Conveyor 转述
  source_url: https://archive.org/details/bim_early-english-books-1641-1700_tyrannus-or-the-mode-_evelyn-john_1661
  quote: "In the Tyrannus, Evelyn not only touched on the history and psychology of fashion but also went as far as to recommend a reformed dress for men, including the Persian vest and sash which was to be reflected to a certain extent in the fashions of the mid-1660s."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（背景，不入画）1666 年 9 月伦敦上流男装仍是法式路线：短 doublet + 鹅笼裤 + 满身缎带"
  negative: "东方风格腰带 sash、波斯长袍、土耳其式外袍"
```

**给「穿搭检查」栏目的一句口播素材**：旅行者可以在镜头前说「这条街上没有一个人穿那件后来被叫作『三件套祖宗』的长外套——国王要到五个星期以后才在枢密院宣布它，而那时候这条街已经烧没了」。这是本站最强的一个时间点包袱，**但只能用在口播里，画面上一件都不许出现**。

### 3.0.2 男装此刻的形制：**短 doublet + petticoat breeches（鹅笼裤）**，正处在寿命最后一年

```yaml
- fact_id: london1666.dress.004
  claim: petticoat breeches（又称 rhinegraves，鹅笼裤）＝极宽的打褶短裤，形似裙；1660 年复辟随查理二世传入英格兰，在英格兰流行到 1666 年为止
  tag: ✅
  source: Wikipedia「Petticoat breeches」/「Rhinegraves」（交叉核对用，非权威）
  source_url: https://en.wikipedia.org/wiki/Petticoat_breeches
  quote: "Petticoat breeches were voluminously wide, pleated pants, reminiscent of a skirt, worn by men in Western Europe during the 1650s and early 1670s. … In England, rhinegraves were fashionable from 1660 until 1666, when Charles II dropped the style."
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "宽得像短裙的及膝褶裤，裤管极阔、走动时整片摆动，腰侧与裤口垂着成束的缎带环"
  negative: "紧腿马裤、18 世纪及膝紧身马裤、现代长裤、灯笼裤收口"

- fact_id: london1666.dress.005
  claim: 1650–1665 年 doublet 越缩越短，短到与裤腰之间露出一截衬衫；这是 doublet 在男装里的最后形态，1660 年代末即被外套取代
  tag: ✅
  source: Fashion History Timeline (FIT/SUNY)「doublet」「1660-1669」
  source_url: https://fashionhistory.fitnyc.edu/1660-1669/
  quote: "Men wore the short bolero-style doublet with a bloused shirt appearing at the open seams, with large ruffled cuffs. … from 1650 to 1665, doublets shortened so that there was a gap between doublet and breeches."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "短到肋下的小马甲式上衣（bolero 长度），下摆与裤腰之间露出一圈鼓起的白亚麻衬衫，袖口是宽大的褶边"
  negative: "长及大腿的上衣、收在裤腰里的衬衫、现代衬衫领"

- fact_id: london1666.dress.006
  claim: 1660 年代男装缎带用量极夸张：一套现存礼服用了六种缎带、合计 216 码
  tag: ✅
  source: Fashion History Timeline (FIT/SUNY)「1660-1669」
  source_url: https://fashionhistory.fitnyc.edu/1660-1669/
  quote: "One surviving suit featured \"six different types of ribbon that total 216 yards in length,\" demonstrating how \"several hundred yards of ribbon might be used to decorate one suit.\""
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（仅限阔绰男性）肩头、袖口、腰侧、膝头成簇成束的丝缎带环，多到像流苏"
  negative: "劳动阶层身上出现大量缎带、素净上衣却挂满绸带"

- fact_id: london1666.dress.007
  claim: 领子此时是 cravat（长条亚麻围颈、前面打结，端头常缀蕾丝），或更朴素的 falling band（平翻领）；Randle Holme 1688 定义 cravat 为「一条长巾围在领上、前面打一个蝴蝶结」
  tag: ✅
  source: Randle Holme, The Academy of Armory (Chester, 1688)，经 costumehistorian「The Cravat」转录
  source_url: http://costumehistorian.blogspot.com/2020/07/the-cravat.html
  quote: "A Cravatt is nothing else but a long Towel put about the Collar, and so tyed before with a Bow Knott."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "颈上一条白亚麻长巾绕过、在喉前打成一个松蝴蝶结，两端垂在胸前（讲究人端头缀细蕾丝，平民一律素边）"
  negative: "现代领带、蝴蝶结领结、拉夫领（ruff，已过时三十年）、立领衬衫"
```

### 3.0.3 布料 · 颜色 · 清洁度（最影响成片质感的三件事）

```yaml
- fact_id: london1666.dress.008
  claim: 亚麻贴身（衬衫、女式 shift、领巾、coif 都是亚麻），外层是羊毛与毛混纺
  tag: ✅
  source: The Vincent Conglomeration「Working class costume of 17th century women」（英国内战再现社群考据页）
  source_url: https://www.vincents.org.uk/re-enacting/caroline/ordwomen
  quote: "Linen was worn next to the skin, shifts, shirts, collars, coifs, kerchiefs were made of linen." / "wool and wool mixtures" for skirts, stays, and bodices.
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "贴身是亚麻（织纹清楚、微微发皱、不反光），外层是羊毛呢（略起毛、有厚度、垂坠沉）"
  negative: "丝缎光泽、涤纶垂感、针织棉 T 恤质感、牛仔布、现代化纤"

- fact_id: london1666.dress.009
  claim: 平民的亚麻不可能是纯白的，应是奶白、灰、米褐；毛料只有天然染料，且褪色快，成色应是「洗旧的柔和色」而非鲜艳强色
  tag: ✅
  source: The Vincent Conglomeration「Working class costume of 17th century women」
  source_url: https://www.vincents.org.uk/re-enacting/caroline/ordwomen
  quote: "use cream, grey or beige linen – or cotton dyed with tea or coffee grounds make a good substitute." / "Only natural dyes were available … washed out muted colours look better than harsh, strong bright colours."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "所有布色都是洗过很多次的柔和色：奶白、灰白、米褐、铁锈红褐、暗芥黄、灰蓝、深橄榄；同一件衣服上有深浅不匀的褪色"
  negative: "荧光色、鲜红、宝蓝、亮紫、纯黑、纯白、化学染料的均匀饱和色、崭新无褶"

- fact_id: london1666.dress.010
  claim: 蕾丝在 17 世纪是穷人做、富人穿的昂贵物；扮演劳动阶层时不该出现蕾丝，装饰性的织带与缎带也不该有（除非是富人转手的旧衣）
  tag: ✅
  source: The Vincent Conglomeration「Working class costume of 17th century women」
  source_url: https://www.vincents.org.uk/re-enacting/caroline/ordwomen
  quote: "Lace was expensive, made by the poor, worn by the rich, when portraying working class people avoid lace." / "Bodices were unlikely to have had braid or ribbon unless second hand from richer women."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "劳动阶层衣服上零蕾丝、零织带、零绸带装饰，只有素面布与实用的系带"
  negative: "劳动者身上出现蕾丝领、蕾丝袖口、花边围裙、装饰性绸带"
```

### 3.0.4 头：女性遮发是常规，coif 正在被 hood 取代

```yaml
- fact_id: london1666.dress.011
  claim: 女性除非富到能请人做发型，否则头一律要遮；街头劳动女性用亚麻方巾、coif（贴头软帽）或 hood（兜帽）
  tag: ✅
  source: The Vincent Conglomeration「Working class costume of 17th century women」
  source_url: https://www.vincents.org.uk/re-enacting/caroline/ordwomen
  quote: "Women covered their heads unless they were rich enough to have their hair dressed in the fashionable style." / "no hat and no hairstyle is pure laziness"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "女性头上一律有遮盖：亚麻贴头软帽 coif、或包头兜帽 hood、或对折成三角的亚麻方巾；鬓边最多露出极少碎发"
  negative: "披散长发、露出整个发型、马尾辫、空着头不戴任何东西"

- fact_id: london1666.dress.012
  claim: 1640 年代到 1680 年代之间，hood（兜帽）在下层女性中逐步取代 coif；到 1688 年 Laroon《伦敦叫卖》里 28 名女商贩中 18 人戴 hood、仅 3 人明显戴 coif；深色与浅色 hood 各占一半
  tag: ✅
  source: Costume Historian「Women's Hoods 1600-1690」（统计自 Marcellus Laroon, The Cryes of the City of London, 1688）
  source_url: http://costumehistorian.blogspot.com/2016/01/womens-hoods-1600-1690.html
  quote: "18 are wearing hoods, and only 3 obvious coifs" / "9 of the hoods in Laroon are dark and 9 are light."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "1666 年正处在过渡期：街上 coif 与 hood 并存，hood 已略占上风；深色（黑褐、深灰）与浅色（本白、米）各半"
  negative: "全街统一头饰、只有 coif 没有 hood、19 世纪的圆筒女帽 bonnet"

- fact_id: london1666.dress.013
  claim: 亚麻大方巾对折成三角、围在颈上并别住或系住，是劳动女性的常见穿法（既保暖又防晒）
  tag: ✅
  source: The Vincent Conglomeration「Working class costume of 17th century women」
  source_url: https://www.vincents.org.uk/re-enacting/caroline/ordwomen
  quote: "A large square of linen, folded diagonally and pinned or tied about the neck was worn, especially by labouring women. … covering the back of the neck heat is kept in when cold and sunstroke avoided when warm."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "一块本白亚麻大方巾对折成三角，尖角朝后盖住后颈，两端在胸前交叠并用一根别针别住"
  negative: "现代围巾打法、丝巾、蕾丝披肩、敞胸不遮"
```

### 3.0.5 鞋

```yaml
- fact_id: london1666.dress.014
  claim: 此时的鞋是 latchet shoe——鞋面两侧各伸出一条「耳带（latchet）」在脚背上方交叠，用皮绳或缎带穿孔系住；鞋头在 17 世纪由圆转方
  tag: ✅
  source: Fashion History Timeline (FIT/SUNY)「1660-1669」+ Encyclopedia.com「Seventeenth-Century Footwear」
  source_url: https://fashionhistory.fitnyc.edu/1660-1669/
  quote: "a pair of women's blue velvet latchet-tie shoes with narrow squared toes" / "During the seventeenth century, shoes began to fasten with ribbons and buckles. The toes of shoes changed from being round to square."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "低帮皮鞋，鞋头方，脚背上方两条耳带交叠、用一根皮绳或布带穿孔系住；平底或极矮的堆跟；皮面粗糙、沾泥、鞋头磨白"
  negative: "尖头鞋、高跟、长筒马靴（步行者不穿）、现代皮鞋、运动鞋、木屐"

- fact_id: london1666.dress.015
  claim: 鞋扣（buckle）在 1660 年已经出现但仍是新潮：Pepys 1660 年 1 月 22 日记下「今天我开始在鞋上装扣」；所以 1666 年阔绰男性可用鞋扣，劳动阶层仍是系带
  tag: ✅
  source: The Diary of Samuel Pepys, Sunday 22 January 1659/60
  source_url: https://www.pepysdiary.com/diary/1660/01/22/
  quote: "This day I began to put on buckles to my shoes, which I have bought yesterday of Mr. Wotton."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "有钱人的鞋面上一枚小方形金属扣（朴素、不大、无宝石）；劳动者仍是两条皮绳系结"
  negative: "巨大的方形装饰扣（那是 18 世纪）、帽扣、腰带上的大金属扣、闪亮镀铬"
```

### 3.0.6 【第二大误传】清教徒式全黑高帽 + 帽扣

```yaml
- fact_id: london1666.dress.016
  claim: 「清教徒穿全黑」是后世（尤其维多利亚时代绘画）造出的印象。黑色染料昂贵且易褪，黑衣是主日与正式场合（含画像）的最好衣裳，不是日常（判定说明：误传）
  tag: ❌
  source: Two Nerdy History Girls「How (Not) to Dress a 17th c. Puritan Maiden」+ Wikipedia「Sadd colors」
  source_url: https://twonerdyhistorygirls.blogspot.com/2015/01/how-not-to-dress-17th-cpuritan-maiden.html
  quote: "Black fabric was very expensive to make and the color once achieved tended to fade fast. These black gowns were worn for portraits because they were the sitter's Sunday best, not necessarily their everyday clothing."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "街上几乎看不到纯黑衣服；最深的颜色是深褐、暗橄榄、炭灰，而且都带褪色不匀"
  negative: "全黑套装、清教徒式黑白配、成排穿黑的路人、纯黑高顶帽"

- fact_id: london1666.dress.017
  claim: 17 世纪实际流行的是「sadd colours（沉色）」，1638 年的一份清单列出：肝色、de Boys、茶褐（tawney）、赤褐（russet）、紫、法国绿、姜黄、鹿色、橙；最受偏爱的是 russet 与 philly mort（枯叶色）
  tag: ✅
  source: David Hackett Fischer, Albion's Seed（「Massachusetts Dress Ways: The Puritan Taste for Simple Clothes and 'Sadd' Colors」章）
  source_url: https://erenow.org/common/fourbritishfolkwaysinamerica1989/26.php
  quote: "A list of these \"sadd colors\" in 1638 included \"liver color, de Boys, tawney, russet, purple, French green, ginger lyne, deer colour, orange.\" Specially favored was russet, and a color called philly mort from the French feuille morte (\"dead leaf\")."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "服色锁定在这组沉色里：赤褐 russet、枯叶褐、茶褐、肝褐、鹿皮色、暗芥黄、法国绿（发灰的橄榄绿）、暗橙"
  negative: "饱和纯色、亮紫、亮绿、亮橙、荧光、纯黑、纯白"
  note: 该 1638 年清单出自新英格兰语境，用于伦敦须注明是同期英语世界的色名体系；tier 定 T2、待人工核 Fischer 原书注脚

- fact_id: london1666.dress.018
  claim: 高顶窄檐的 capotain（就是影视里的「清教徒高帽 / 朝圣者帽」）属于内战前与共和时期，到 17 世纪后期已过时——帽冠变矮、帽檐变宽；1660 年代男性开始戴大假发（判定说明：误传：1666 年戴 capotain ＝ 早了十五到三十年）
  tag: ❌
  source: Wikipedia「Capotain」+「Cavalier hat」（交叉核对用）
  source_url: https://en.wikipedia.org/wiki/Capotain
  quote: "The capotain … especially associated with Puritan costume in England in the years leading up to the English Civil War and during the Commonwealth. … tall conical styles grew outmoded by the later 17th century as hat crowns lowered and brims widened."
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "男帽是矮冠宽檐的软毡帽（骑士帽路线），帽檐常一侧上翻；帽上零金属扣、零缎带扣环"
  negative: "高顶窄檐黑帽、帽子正面一枚方形大金属扣（纯属 19 世纪想象）、三角帽 tricorne（18 世纪）、圆顶礼帽"
```

---

## 3.1 五套锁定描述串

> 模板：`{形制名词}（{材质}，{色名}，{关键结构 2–3 处}），{穿着方式}；不是 {最常见误传形制}`
> 每套的分件依据见 §3.0 各 fact；`⚠️` 标记的分件表示细节未查到硬出处、需人工补。

### 套 A · 城内中等市民女性（店家娘子 / 主妇）

> **锁定串（A）**
> 「**女式 waistcoat 上衣**（羊毛呢，赤褐 russet，前襟对襟系带、腰下裁出三角衬片 gore 所以下摆外撇、袖到腕），套在**贴身亚麻 shift**（本白微泛灰，领口横开至锁骨、袖到腕）与**无袖硬撑胸衣 bodice**（亚麻外面、内里用鲸须或成束芦苇 bents 撑起，背后系带）之外；下身两到三层**petticoat**（羊毛呢，外层暗芥黄、内层本白亚麻，腰部密褶，长至脚踝），腰上系一条**亚麻围裙**（米白，四角方正、腰绳在前打结）；颈上**对折成三角的亚麻方巾**（本白，尖角朝后、胸前交叠别针固定）；头戴**贴头 coif 或包头 hood**（本白亚麻 coif，或深褐呢 hood），**不露发**；脚上**方头 latchet 低帮皮鞋**（褐皮，脚背两条耳带皮绳系结）配**手织羊毛袜**（灰白或暗绿，膝下用一根布带扎住）。整身零蕾丝、零装饰绸带，布色全部是洗旧了的柔和沉色。
> **不是**清教徒式全黑白配、**不是**戴高顶窄檐黑帽、**不是**露着长发系花边围裙的『农家女』扮相、**不是**紧身束腰＋蓬蓬裙的舞台戏服。」

- 依据：dress.008 / 009 / 010 / 011 / 013 / 014 / 016 / 017 / 018
- waistcoat 与 petticoat 的形制定义（T1 原文，Randle Holme 1688）：

```yaml
- fact_id: london1666.dress.019
  claim: waistcoat＝没有 stays/bodies 连在上面的外穿上衣，是中下层女性普遍穿的衣服，下摆用三角衬片 gore 撑开，有人配 stomacher；petticoat＝去掉上身的袍子下半截，可穿在 gown 里面也可单穿
  tag: ✅
  source: Randle Holme, The Academy of Armory (1688), Book III，经 Sarah A. Bendall 转录
  source_url: https://sarahabendall.com/2021/01/02/randle-holme-academy-of-armory-1688-late-seventeenth-century-womens-dress-terminology/
  quote: "A waistcoat is the outside of a gown without either stayes or bodies fastned to it; it is an habit or garment generally worn by the middle and lower sort of women, having goared skirts, and some wear them with stomachers." / "A petticoat is the skirt of a gown without its body; but that is generally termed a petticoat, which is worn either under a gown, or without it." / "A goare is a cant or three cornered piece of cloth put into a skirt, to make the bottom wider than the top: so are goared petticoats."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "女性外穿上衣是 waistcoat：腰以上贴合、腰以下因插了三角衬片而外撇成短摆；裙子叫 petticoat，可以叠穿两三层"
  negative: "连身长裙一片式、19 世纪钟形裙撑、束腰蓬裙、现代连衣裙"
  note: Holme 出版于 1688 年，比本站晚 22 年；术语与形制在 1660 年代已成立，但作为 1666 年证据须标注年代差

- fact_id: london1666.dress.020
  claim: 劳动阶层女性买不起鲸须，用「bents」——成束的芦苇——代替，或用本地削的木撑条，做无袖硬撑 bodice
  tag: ✅
  source: The Vincent Conglomeration「Working class costume of 17th century women」
  source_url: https://www.vincents.org.uk/re-enacting/caroline/ordwomen
  quote: "boned sleeveless bodices" … "bents. These were bundles of reeds which acted as whalebone"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "女性上身有一件无袖硬撑胸衣把躯干撑成平直的圆锥形，不是自然体型也不是沙漏腰；撑条不匀、布面有横向压痕"
  negative: "现代胸衣、维多利亚沙漏束腰、无支撑的自然垂坠上身"

- fact_id: london1666.dress.021
  claim: 所有裙子此时都叫 petticoat，而且是叠穿好几条；1650–60 年代时髦胸衣腰线长、前中收成深尖角、领口横开露肩，1660–1675 年为主流
  tag: ✅
  source: Fashion History Timeline (FIT/SUNY)「1660-1669」
  source_url: https://fashionhistory.fitnyc.edu/1660-1669/
  quote: "long-waisted, sloping to a deep point in front" and "mainly in vogue from 1660 to 1675" … "low, off-the-shoulder neckline"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "时髦女性上身腰线拉长、前中收成一个向下的深尖角，领口横着开、露出两侧肩头；裙子层层叠叠在腰上打密褶"
  negative: "高腰帝政线（那是 1800 年代）、V 领、方形高领、圆领 T 恤式领口"
```

### 套 B · 劳动阶层男性（搬运工 / 面包师）

> **锁定串（B）**
> 「**及腰短 doublet**（粗羊毛呢，肝褐色，前襟一排布包扣、袖肘处磨得发亮、下摆短到肋下），下摆与裤腰之间露出一圈**鼓起的白亚麻衬衫**（本白泛灰，袖口宽大翻出、领口敞开）；下身**素面及膝褶裤**（羊毛呢，暗橄榄，裤管宽但**无一根缎带**、膝下用布带扎住）；腰前系一条**粗亚麻围裙**（米白到灰白，面包师的沾着干面粉与焦斑，搬运工的是皮的、磨出油光）；头戴**矮冠宽檐软毡帽**（深褐，檐一侧上翻、毡面起球）或索性**裹一块布巾**；脚上**方头 latchet 低帮皮鞋**（深褐，皮绳系结、鞋头开裂沾泥）配**粗羊毛袜**（本色灰）。手背与指节脏、指甲有黑边；衣服有补丁、接缝处开线。
> **不是**及膝长外套 vest（那要到一个月后）、**不是**满身缎带的鹅笼裤（那是有钱人的）、**不是**皮革紧身束胸的『幻想中世纪佣兵』、**不是**干净挺括的舞台工装。」

- 依据：dress.004 / 005 / 008 / 009 / 010 / 014 / 018；面包师身份见 food.002
- ⚠️ **未查到**：搬运工 / 面包师专属的行业服色或行会规定（不像宋代汴京有「百工百衣」的法定本色）。本次未找到 1660 年代伦敦同类规定的一手出处，**不要编行业制服**；只能靠「围裙 + 工具 + 脏污部位」区分行当。

### 套 C · 中等商人男性

> **锁定串（C）**
> 「**及腰短 doublet**（细羊毛呢，炭灰偏暖，前襟一排布包扣、袖上开细缝 panes 透出底下白衬衫、袖口大褶边），下摆与裤腰之间露出一圈**白亚麻衬衫**；下身**petticoat breeches / 鹅笼裤**（羊毛呢，深橄榄，裤管极阔像短裙、腰侧与裤口各一束**克制的丝缎带环**——只三五束，不是几百码那种）；颈上**白亚麻 cravat**（在喉前打一个松蝴蝶结，两端垂胸，端头素边或极细蕾丝）；肩上**斜披一件短斗篷**；头戴**矮冠宽檐软毡帽**（黑褐，檐一侧上翻，帽上**无扣**），帽下是**及肩的自然长发**或**深褐色长假发 periwig**；脚上**方头 latchet 皮鞋**（黑褐，一枚小方形金属鞋扣）配**丝袜或细羊毛袜**（灰白），膝下一圈**cannons**（裤口下垂到袜上的褶边）。衣服干净但不新，呢面有细绒。
> **不是**及膝长外套 vest 或三件套、**不是**三角帽＋长马甲＋紧身马裤的 18 世纪绅士、**不是**拉夫领（过时三十年）、**不是**穿长筒马靴在城里走路。」

- 依据：dress.004 / 005 / 006 / 007 / 014 / 015 / 018
- 假发时点：Pepys 1663 年开始戴假发（见 dress.022），所以 1666 年中等商人戴假发是合理但非必然。

```yaml
- fact_id: london1666.dress.022
  claim: 1660 年代男性头发比世纪前期更长更蓬，自然感假发（periwig）开始流行；Pepys 1663 年开始戴
  tag: ✅
  source: Fashion History Timeline (FIT/SUNY)「1660-1669」
  source_url: https://fashionhistory.fitnyc.edu/1660-1669/
  quote: "Men's hair is now longer and fuller than was fashionable earlier in the seventeenth century." / "Natural-looking wigs" began appearing; "The naval administrator Samuel Pepys took the plunge in 1663."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "男性头发及肩、中分或偏分、自然卷曲蓬松；有钱人戴深褐长假发，假发做得像真发不像后来的白色卷筒假发"
  negative: "白色扑粉卷筒假发（那是 18 世纪）、短寸头、现代发型、光头、马尾辫扎发"

- fact_id: london1666.dress.023
  claim: 膝下的 cannons/boothose＝裤口处垂下来盖在袜子上的宽褶边，1660 年代取代了更早的靴袜样式
  tag: ✅
  source: Fashion History Timeline (FIT/SUNY)「1660-1669」+ Nicole Kipar「The 1660s Restoration Costume Comes to Life」
  source_url: https://fashionhistory.fitnyc.edu/1660-1669/
  quote: "Wide ruffles at the knees … typically were fastened to the tops of the stockings."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（仅限阔绰男性）膝盖下面一圈宽褶边，从裤口垂下来盖在袜筒上端"
  negative: "劳动者腿上出现膝下褶边、现代袜口、长筒靴"
```

### 套 D · 仆役（城内人家的女仆）

> **锁定串（D）**
> 「与套 A 同骨架但**更旧、更素、更短**：**女式 waistcoat 上衣**（粗羊毛呢，茶褐 tawney，对襟系带、肘部与前襟有深色补丁），**贴身亚麻 shift**（灰白、袖口洗得起毛）；下身**两层 petticoat**（外层灰褐羊毛，长度**到脚踝略短一点以便干活**，下摆有一圈泥渍与洗白痕），腰上一条**大幅粗亚麻围裙**（本白发灰，沾水渍与灰迹，围到几乎裹住整条裙子）；颈上**亚麻方巾**（灰白）；头戴**贴头 coif**（本白亚麻，边缘发黄，**无蕾丝**），发全部收进去；脚上**方头 latchet 低帮皮鞋**（深褐，鞋面裂纹、皮绳打了结又断过）配**粗羊毛袜**（本色）；袖子常**挽到肘上**露出前臂。
> **不是**法式黑裙白围裙白蕾丝帽的『维多利亚女仆』制服（那晚两百年）、**不是**露肩低胸的『酒馆女招待』戏服、**不是**一身干净新布。」

- 依据：dress.008 / 009 / 010 / 011 / 013 / 014 / 019 / 020
- ⚠️ **未查到**：1660 年代伦敦仆役是否有雇主提供的成套「制服 livery」惯例（男仆的 livery 有据，女仆未查到）。不要给女仆画统一制服。

### 套 E · 旅行者自己（外来女性，不显眼、便于走路）

> 这一套的设计目标是：**站在 1666 年 9 月 1 日的伦敦街上，没有一个路人会多看她第二眼**，同时她要能走一整天、能蹲下、能上下窄楼梯。

> **锁定串（E）**
> 「**女式 waistcoat 上衣**（中等厚度羊毛呢，枯叶褐 philly mort，对襟系带、腰下三角衬片撑出短摆、袖到腕可挽起），内**贴身亚麻 shift**（本白微灰，领口横开至锁骨）与**无袖硬撑 bodice**（背后系带，撑得住但不勒）；下身**两层 petticoat**（外层羊毛呢，灰蓝；内层亚麻，本白；**长度恰到脚踝、不拖地**——避免下摆吸水往上洇），腰上**一条素亚麻围裙**（米白，四角方正）；颈上**亚麻方巾**（本白，三角形，胸前交叠别针固定）；头戴**深褐呢 hood**（包住整个头与后颈、颌下系带，兜帽可放下露出底层本白 coif），**发全部收进去**；肩上可加一件**无袖短斗篷 / 半身披风**（深灰褐羊毛，前面一枚素金属扣）；脚上**方头 latchet 低帮皮鞋**（深褐厚底，脚背两条耳带以皮绳系死，鞋底钉过掌）配**厚羊毛袜**（灰白，膝下布带扎紧）。全身**零蕾丝、零绸带、零金属亮饰**，色只用枯叶褐 / 灰蓝 / 米白三色，布面都带均匀的旧感。
> **不是**清教徒黑白装、**不是**戴高顶帽的朝圣者、**不是**低胸紧腰的『复辟时期贵妇』（那会让她在市井街上立刻成为焦点）、**不是**拖地长裙（在 1666 年伦敦的街上等于把裙摆浸进污水沟）。」

- 设计依据：dress.009（洗旧沉色）/ 010（零蕾丝）/ 011 + 012（必须遮发，hood 已占上风）/ 013（方巾）/ 014（方头系带鞋）/ 019（waistcoat 是中下层通用外衣）
- ⚠️ **裙长**这条是**从 T2 再现社群的实务建议推来的**（原话是 "Use ankle-length skirts to prevent capillary action problems where wet hems draw moisture upward through fabric"），不是 1666 年的一手记载；作为设计决策可用，作为「史实」须降级标注。

---

# §4 食：1666 年伦敦平民一天吃什么

## 4.0 一日三餐的结构

```yaml
- fact_id: london1666.food.001
  claim: 当时不兴坐下来吃早餐，代之以在酒馆喝一杯「morning draught（晨饮）」；女性与儿童的晨饮是 small beer，且多在家里喝、不在酒馆
  tag: ✅
  source: Henry B. Wheatley 1893 版 Pepys 日记脚注（pepysdiary「Morning draught」条）+ 该页注解
  source_url: https://www.pepysdiary.com/encyclopedia/1562/
  quote: "It was not usual at this time to sit down to breakfast, but instead a morning draught was taken at a tavern." / "Certainly women (and children) took a morning draught of small beer. Most morning draughts would have been taken at home, not in a tavern."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "早上没有『一桌早餐』这回事：站着或坐着喝一杯淡啤酒，配一块面包或干酪，就算吃过早饭"
  negative: "丰盛英式早餐（煎蛋培根香肠烤番茄焗豆）、咖啡配可颂、餐桌摆盘的早餐场景"

- fact_id: london1666.food.002
  claim: 正餐（dinner）在正午，是一天的主餐；晚餐（supper）是小餐，常与早餐类似——面包、干酪、糊状粥，或把中午剩的肉热一下（判定说明：二手综述，未核到一手）
  tag: ⚠️
  source: 综合检索摘要（未定位到可引的一手页面）
  source_url: https://www.pepysdiary.com/encyclopedia/1562/
  quote: "Dinner was at midday … Supper was a smaller meal, often similar to breakfast: bread, cheese, mush or hasty pudding, or warmed-over meat from the noon meal."
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "一天的正餐在正午；傍晚那顿小而随便——面包、干酪、一碗糊粥或中午剩下热过的肉"
  negative: "晚上七八点的正式晚宴作为平民日常、三道式上菜"
  note: ⚠️ 这条只查到综述转述，**未找到可逐字引用的一手或学术页面**。进 prompt 前必须人工补一个硬出处（建议查 Liza Picard《Restoration London》相应章节）。

- fact_id: london1666.food.003
  claim: Pepys 常吃的最简单的一餐就是「一块面包和干酪」，在市集上或酒馆里解决
  tag: ✅
  source: The Diary of Samuel Pepys（经 pepysdiary 检索摘要）
  source_url: https://www.pepysdiary.com/
  quote: "ate bread and cheese for his dinner in the marketplace" / "nothing but a piece of bread and cheese at the ale-house"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "最常见的一餐：一块厚切面包 + 一块硬干酪，用手拿着吃，配一杯淡啤酒"
  negative: "刀叉餐具齐全的摆盘、三明治（那是 1760 年代才得名）、沙拉配菜"
  note: ⚠️ 引文来自站内检索摘要，**未定位到具体日期的日记页**；进 prompt 前须补日期与原页 URL

- fact_id: london1666.food.004
  claim: Pepys 的记述里肉压倒性地多、蔬菜与沙拉极少被提，但蔬菜其实是日常上桌的；复辟后斋戒与吃鱼的宗教硬规矩松了，但很多人仍在四旬斋尽量少吃肉
  tag: ✅
  source: Pawel Kaptur, To Dinner and There Merry (2022)，Sue Nicholson 书评（pepysdiary in-depth, 2025-01-16）
  source_url: https://www.pepysdiary.com/indepth/2025/01/16/dinner-merry/
  quote: "meat predominates in all Pepys' descriptions of meals, partly because its presence on the table was a marker of affluence." / "the strict religious rules around fasting and the eating of fish relaxed" / Pepys 1661-03-10: "a poor Lenten dinner of coleworts and bacon."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "桌上肉是身份的证明，所以显眼；蔬菜（甘蓝 coleworts、豌豆、洋葱、萝卜）实际有，但摆得不起眼"
  negative: "沙拉盘作为主角、蔬菜精致摆盘、一桌全素"
```

## 4.1 面包（Farriner 就是面包师，这一节必须查透）

```yaml
- fact_id: london1666.food.005
  claim: Thomas Farriner 是伦敦城内知名面包师，第二次英荷战争期间是皇家海军**船用硬饼干（ship's biscuit）**的供应商；1666 年 9 月 2 日凌晨他 Pudding Lane 的铺子起火，成为大火的起点
  tag: ✅
  source: Wikipedia「Thomas Farriner」+ The Monument「History」（交叉核对）
  source_url: https://en.wikipedia.org/wiki/Thomas_Farriner
  quote: "the official supplier of ship's biscuits to the Royal Navy during the Second Anglo-Dutch War, Farriner held a prominent position within the Bakers' Company." / "In the early hours of 2 September 1666, in his house on Pudding Lane, Farriner was awakened by smoke billowing under the door of his bedroom."
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "Pudding Lane 的面包铺：临街木构窄门面，一层是烤炉与操作台，炉口砖砌、余火未熄；面粉袋、木揉槽、长柄木铲、成摞的硬饼干"
  negative: "现代烘焙店玻璃橱窗、蛋糕、可颂、法棍、电烤箱、白色瓷砖"
  note: ⚠️ Farriner 是本站的关键人物，Wikipedia 只能作交叉核对。**人工核证优先级最高**：Bakers' Company 档案 / National Archives 的 Farriner 壁炉税记录（https://www.nationalarchives.gov.uk/education/resources/great-fire-of-london-examine-the-evidence/hearth-tax-for-thomas-farriner/）

- fact_id: london1666.food.006
  claim: 17 世纪英格兰面包按精粗分级：manchet＝最细的白面包，白麦粉筛两到三遍、几乎无麸，贵、贵族与乡绅吃；cheat＝去掉最粗一层麸的麦粉面包，中等人家的日常；maslin＝小麦掺黑麦，更黑更实，劳动者吃
  tag: ✅
  source: Gervase Markham, The English Huswife / Maison Rustique 系相关考据（William Rubel「Cheat Bread」「The Coarse Cheat」）+ Wikipedia「Manchet」
  source_url: https://williamrubel.com/2022/03/14/cheat-bread-gervase-markhams-everyday-loaf-from-1614/
  quote: "Manchet was a very fine white bread made from wheat flour … twice- or thrice-bolted white wheat flour, very low in bran, high-status and more costly, eaten by nobles and gentry." / "Cheat was a wheaten bread with the coarsest part of the bran removed … the daily bread of the middling sort." / "Maslin bread was a wheat-and-rye mix, darker and denser, common among laborers."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "面包按颜色分三档，同一个摊子上并排摆着：最贵的 manchet 是小而圆、表皮浅金、内里近白；中档 cheat 是米黄带细麸点；最便宜的 maslin 是大而扁、灰褐色、气孔粗、外皮硬"
  negative: "统一雪白的切片吐司、法棍、可颂、酸种乡村包的现代造型、包装袋"

- fact_id: london1666.food.007
  claim: Assize of Bread 的机制是「**价钱固定、重量浮动**」——面包价钱（一便士 / 半便士 / 四分之一便士）不变，小麦涨价时官方下调法定重量；短斤两的面包师会被罚款甚至上枷示众
  tag: ✅
  source: Wikipedia「Assize of Bread and Ale」+「Penny bun」+ William Rubel 相关考据
  source_url: https://en.wikipedia.org/wiki/Assize_of_Bread_and_Ale
  quote: "A penny loaf was a small bread loaf which cost one old penny … The size of the loaf could vary depending on the prevailing cost of the flour used in the baking." / "These assizes adjusted the weight of bread according to the price of wheat. The price of bread was always the same, even though the price of grain fluctuated." / "Bakers could be fined or even pilloried for short-weight bread."
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "面包按「几便士的面包」叫卖，不按重量叫卖；同样是一便士，丰年的那个明显更大"
  negative: "按克/磅标价、价签、现代秤、条形码"

- fact_id: london1666.food.008
  claim: ⚠️ **未查到**：1666 年伦敦市长颁行的具体 assize 表（一便士白面包/wheaten/household 各应重几盎司，对应当年小麦价）
  tag: ⚠️
  source: 多轮检索均只返回 1750s–1800s 的数据与中世纪 1266 年原文
  source_url: https://www.jefftk.com/p/english-bread-regulations
  quote: "The search results don't contain specific regulatory details from 1666 London. Most detailed examples found are from the 1750s-1765 period or earlier medieval regulations."
  tier: n/a
  verified_by: ai_read
  used_in: []
  prompt_string: "（不可用）本站台词里**不要报具体盎司数或具体面包价**"
  negative: "在「一口一问」里念出未经核实的重量与价格数字"
  note: 人工补证途径：London Metropolitan Archives 的 Corporation of London assize 记录；British History Online 的 17 世纪 City records；或 1709 年《Assize of Bread Act》(8 Anne c.18) 往前回溯。**在补到硬数字之前，「一口一问」环节只报「一便士的面包」这种定性说法。**

- fact_id: london1666.food.009
  claim: 伦敦面包师行会历史上分白面包师（White Bakers）与黑面包师（Brown Bakers）两支，黑面包师 1621 年获单独法人资格、1635 年在 Aldersgate 有过自己的会馆，1645 年因生意与影响力衰落重新并回白面包师，合为一个 Bakers' Company。所以 1666 年只有**一个**面包师行会
  tag: ✅
  source: Worshipful Company of Bakers 官网「A Brief History – Brown Bakers」+ Wikipedia
  source_url: http://www.bakers.co.uk/A-Brief-History/Brown-Bakers.aspx
  quote: "The Brown-Bakers obtained their own Coat of Arms in 1572, a Charter in 1614, a Grant of Incorporation in 1621, and for ten years their own Hall in Aldersgate in 1635. … It was not until 1645 that, due to their ever declining trade and influence, they finally reunited with the White-Bakers into the single Company existing now."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（背景设定）1666 年伦敦的面包师同属一个行会；白面包与黑面包可以出自同一家铺子"
  negative: "两家对门的敌对面包行会、街上出现两种行会徽记"
```

## 4.2 啤酒：**这是日常饮料，不是酒**

```yaml
- fact_id: london1666.food.010
  claim: 伦敦没有干净的饮用水；上至老下至小孩，日常喝的都是低度的 small beer
  tag: ✅
  source: Pawel Kaptur, To Dinner and There Merry 书评（pepysdiary in-depth, 2025-01-16）
  source_url: https://www.pepysdiary.com/indepth/2025/01/16/dinner-merry/
  quote: "There was no clean drinking water in London; everyone, whatever their age, drank low alcohol \"small\" beer."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "每个人手边都有一杯淡啤酒（浑浊的浅琥珀色、几乎没有泡沫顶）；小孩也喝"
  negative: "喝清水、透明玻璃水杯、瓶装水、水壶、清澈见底的饮料"

- fact_id: london1666.food.011
  claim: small beer 酒精度约 1–2%（一说 0.5–2.8%），是同一批麦芽的第二、第三次淋洗所得；重体力劳动者一天能喝十品脱以上
  tag: ✅
  source: Wikipedia「Small beer」（pepysdiary 百科条目转录）+ 该页 Mark McDermott 注解
  source_url: https://www.pepysdiary.com/encyclopedia/14051/
  quote: "Small beer (also known as small ale or table beer) is a lager or ale that contains a lower amount of alcohol by volume than most others, usually between 1% and 2%." / "The \"first runnings\" … would then make Strong Beer; then a \"Second Running\" would be collected, much weaker and lighter" / "It was common for workers who engaged in laborious tasks to drink more than ten imperial pints (5.7 litres) of small beer a day to quench their thirst."
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "淡啤酒颜色浑浊、偏浅琥珀到淡棕，装在锡镴大杯或陶杯里，没有现代啤酒那层厚白泡沫"
  negative: "金黄透亮的现代拉格、厚厚的奶油泡沫头、玻璃扎啤杯、冰镇水珠"

- fact_id: london1666.food.012
  claim: ⚠️ 未核实的价格：「一加仑 small beer 作晨饮约一便士半，烈啤两倍」
  tag: ⚠️
  source: 检索摘要（未定位到出处页）
  source_url: https://www.pepysdiary.com/encyclopedia/1562/
  quote: "A gallon of small beer taken as the morning draught would have cost about a penny-halfpenny and strong beer would have been twice that price."
  tier: n/a
  verified_by: ai_read
  used_in: []
  prompt_string: "（不可用）「一口一问」环节不要报这个价"
  negative: "在成片里念出未核实的啤酒价格"
  note: 出处不明，必须人工核。进 prompt 前若核不到，改为定性表述（「便宜到人人喝得起」）。
```

## 4.3 肉 · 鱼 · 菜 · 熟食铺

```yaml
- fact_id: london1666.food.013
  claim: 熟食铺（the cook's / cookshop）是伦敦人买现成热菜的地方；Pepys 大火期间（1666-09-04）就是从熟食铺买了一块**羊肩肉**回办公室，「没有餐巾也没有别的东西」地吃
  tag: ✅
  source: The Diary of Samuel Pepys, Tuesday 4 September 1666
  source_url: https://www.pepysdiary.com/diary/1666/09/04/
  quote: "This night Mrs. Turner … and her husband supped with my wife and I at night, in the office; upon a shoulder of mutton from the cook's, without any napkin or any thing, in a sad manner, but were merry."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "熟食铺：临街敞开的铺面，炭火上转着烤肉，整块羊肩、整只鸡挂着；买回去是连着骨头的一大块，用一块布或木盘托着"
  negative: "外卖纸盒、打包袋、保温箱、玻璃保温柜、现代快餐柜台"

- fact_id: london1666.food.014
  claim: 牡蛎是当时的**廉价食物**，从泰晤士河运上来、吃得很凶，Pepys 常在早上就吞牡蛎；腌牡蛎是伦敦穷人的常规口粮。装牡蛎的小桶只有 7–13 英寸高
  tag: ✅
  source: pepysdiary 百科「Oysters」注解（David Quidnunc 等）
  source_url: https://www.pepysdiary.com/encyclopedia/373/
  quote: "The oysters eaten by Pepys and his friends were brought up the Thames and were eaten in large quantities and were not regarded as being as exotic as they are today." / "Pickled oysters were a regular food of the poor in London." / "The barrels used to store shellfish were much smaller than modern ale-house barrels—between 7 and 13 inches tall."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "牡蛎成堆摆在街边浅筐里或小木桶里，现开现吃、直接从壳里吸；壳堆在脚边"
  negative: "冰床摆盘、柠檬角、精致海鲜塔、白手套侍者、牡蛎作为奢侈品呈现"

- fact_id: london1666.food.015
  claim: 火鸡是**新世界来的、但 1666 年早已是常见食物**的反例：约 1570 年代传入英格兰，1660 年代 Pepys 会吃到鸭、鹿、鸡、火鸡、野禽与云雀
  tag: ✅
  source: pepysdiary 百科「Turkey」条目相关注解 + 综合检索
  source_url: https://www.pepysdiary.com/encyclopedia/378/
  quote: "Turkeys were introduced into England about 90 years before the date of this first entry in the diary" / "Pepys would have eaten duck, venison, chicken, turkey, game birds and of course songbirds like larks."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "肉摊上有鸡、鸭、鹅、火鸡、鹿肉、野禽，还有成串的小鸟（云雀）"
  negative: "把火鸡当成『还没传入的新世界食物』而刻意回避；工业化白羽鸡的体型与肤色"
  note: 这条是给 §13 用的「反向」条目——不是所有新世界物产在 1666 年都不存在，火鸡已经彻底本地化了。别一刀切。

- fact_id: london1666.food.016
  claim: ⚠️ 斋戒 / 吃鱼日的实际约束力存疑：Lenten 公告在 1660 年代仍在重发、豁免仍在收费，但伦敦鱼商行会抱怨屠户阳奉阴违；而复辟后「吃鱼的宗教硬规矩」被普遍认为松了（判定说明：两说并存，须人工裁决）
  tag: ⚠️
  source: Political Theology Network「Lent, the Maintenance of Seafaring Men, and the Politics of Fasting」+ pepysdiary in-depth 书评
  source_url: https://politicaltheology.com/lent-the-maintenance-of-seafaring-men-and-the-politics-of-fasting/
  quote: "Lenten proclamations were reissued as late as the 1660s and people continued to pay for exemptions" / "The London Company of Fishmongers petitioned Parliament to complain of failures to heed the Lenten proclamations" ／ 对照："the strict religious rules around fasting and the eating of fish relaxed"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "（谨慎）1666-09-01 是星期六、不在四旬斋内；街上肉摊与鱼摊同时在卖，不必把这一天设计成『只许吃鱼』"
  negative: "把 9 月 1 日拍成强制斋戒日、全城只卖鱼、屠户全部关门"
  note: ⚠️ **未查证**：伊丽莎白朝「政治性鱼日」法（周三/周五/周六禁肉）在 1666 年 9 月 1 日这个**星期六**是否仍有实际约束。这会直接影响「一口一问」能不能点肉。人工核证优先级：高。
```

## 4.4 咖啡馆（1666 年伦敦已经很兴盛）

```yaml
- fact_id: london1666.food.017
  claim: 1663 年伦敦已有 82 家咖啡馆；一「碟（dish）」咖啡一便士，故咖啡馆被称作「penny universities（便士大学）」——一便士买到的不只是一杯咖啡，还有取暖、座位、报纸与一斗烟
  tag: ✅
  source: pepysdiary 百科「Coffee」注解 + Historic UK「English Coffeehouses, Penny Universities」
  source_url: https://www.pepysdiary.com/encyclopedia/361/
  quote: "In 1663 there were 82 coffee houses in london." / "For an inclusive admission charge of a penny, a suitably dressed man could gain access to the well-heated and furnished premises where he could expand his mind through discourse or reading, and the coffeehouses offered all this in addition to a dish of hot coffee and a clay pipe full of tobacco."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "咖啡馆内景：长条木桌与长凳，人挤人坐着，壁炉生着火；每人面前一只浅陶碗或小陶杯装着深褐色咖啡；桌上摊着单页新闻纸；空气里全是烟"
  negative: "吧台点单、咖啡拉花、马克杯、纸杯、外带、菜单板、咖啡机、单人沙发"

- fact_id: london1666.food.018
  claim: 咖啡馆的招牌气味是烟草——1673 年的讽刺小册子说它「烟草臭得比地狱的硫磺还厉害」；里面的人一边抽陶土长烟斗、一边读《Gazette》、一边高声辩论
  tag: ✅
  source: Anon., The Character of a Coffee-House, with the Symptomes of a Town-Wit (London, 11 April 1673)
  source_url: http://www.csun.edu/~kaddison/Character.htm
  quote: "stinks of tobacco worse than hell of brimstone" / "a Rota, that, like Noah's ark, receives animals of every sort" / "sitting in a cloud of smoke" / "a silly fop and a worshipful justice, a griping rook and a grave citizen" / "save twopence a week in Gazettes, and has his news and his coffee for the same charge" / "let their pipes go out, and coffee grow cold, for pure zeal of attention" / "with more noise, but not half so much harmony, as a pack of beagles."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "屋里一层化不开的烟雾，人人叼着白色陶土长烟斗；有人站起来大声念报纸，别人凑过去听，凉掉的咖啡搁在桌上没人管"
  negative: "明亮通风的现代咖啡馆、禁烟标志、安静看书的顾客、玻璃落地窗"
  note: 小册子成于 1673 年，比本站晚 7 年，但描述的是 1660 年代以来已经成型的场所类型；tier 记 T0（一手印本），年代差须在 dossier 里标注

- fact_id: london1666.food.019
  claim: 咖啡、巧克力、冰果露（sherbet）、茶的零售在 1663 年《Excise Act》下需要执照（费 12 便士）并缴税；到 1685 年这几样的税收占全英净消费税收入的 4%
  tag: ✅
  source: Excise Act 1663 (15 Cha. 2 c. 11)，经 legislation.gov.uk + Colonial Williamsburg 研究报告转述
  source_url: https://www.legislation.gov.uk/aep/Cha2/15/11/contents/enacted
  quote: "The licensing of the retail sale of coffee, chocolate, sherbet, and tea was enjoined by the Excise Reform Act of 1663. No person was allowed to sell or retail coffee, chocolate, etc. without a license" / "In 1663, English coffee-houses were required to have a license, at a fee of twelve-pence."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（背景）1666 年咖啡馆是受执照管制的正规行业，四种饮料并列：咖啡、巧克力、冰果露、茶"
  negative: "把咖啡馆拍成地下黑市、无照摊贩"

- fact_id: london1666.food.020
  claim: **咖啡馆实际上把女性排除在外**——名义上人人可进，实践中「体面女性」不进；1674 年出现了著名的《Women's Petition Against Coffee》，署名「数千名丰腴好女人的卑微请愿」，骂咖啡是「新奇的、可憎的、异教徒的液体」
  tag: ✅
  source: The Women's Petition Against Coffee (London, 1674)，Wikisource 全文 + Res Obscura / Smithsonian 学术讨论
  source_url: https://en.wikisource.org/wiki/Women%27s_Petition_against_Coffee
  quote: "The Humble Petitions and Address of Several Thousands of Buxome Good-Women, Languishing in Extremity of Want" / "Newfangled, Abominable, Heathenish Liquor" / "Although coffee houses claimed to admit anyone, in practice women were largely excluded."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "咖啡馆里全是男人，一个女客也没有（端盘子的可能有女性）；女性旅行者站在门口往里看，就已经引来侧目"
  negative: "咖啡馆里男女混坐谈笑、女性顾客独自落座点单"
  note: **这条对本站的女性旅行者是硬约束**——「一口一问」若设在咖啡馆，她进不去，或者进去就是全场焦点（这恰好是个极好的戏剧点，但必须是**有意设计**的，不能是穿帮）。1674 年请愿书晚于本站 8 年，作为「当时风气」证据成立，作为「1666 年具体事件」不成立。
```

## 4.5 【绝对不能出现的食物】逐条给出处

> 这一节直接变成**负向词**。注意：不是所有新世界作物都该禁——火鸡（food.015）与巧克力（下面）在 1666 年都已落地。**一刀切才是错。**

```yaml
- fact_id: london1666.food.021
  claim: 土豆在 1660 年代英格兰只是**富人花园里的稀罕物**，皇家学会 1662 年才开始推广栽培；成为穷人主食要到 19 世纪（判定说明：1666 年伦敦平民餐桌上不该有）
  tag: ❌
  source: 综合检索（Cassidy Cash / New England Historical Society / 1662 Royal Society 记载）
  source_url: https://www.cassidycash.com/potatoes-first-arrived-in-england-in-the-16th-century/
  quote: "Potatoes first appeared in some quantity in the 1660s in England, and the British Royal Society first cultivated potatoes in 1662. However, before becoming established as a food crop, potatoes certainly weren't common as a garden plant, more a curiosity for the gardens of the very wealthy." / "widespread cultivation and prominence in the British diet did not take place until the 19th century."
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "（负向）画面里没有土豆——没有整只土豆、没有土豆泥、没有薯条、没有烤土豆"
  negative: "土豆、马铃薯、薯条、薯块、土豆泥、炸鱼薯条 fish and chips"

- fact_id: london1666.food.022
  claim: 番茄在英国被当作有毒的「毒苹果 / 爱情果」，只作观赏栽培，这个观念从 Gerard《Herball》(1597) 一直延续两百多年
  tag: ❌
  source: Country Life「Why was the tomato considered to be poisonous?」+ Gerard, Herball (1597)
  source_url: https://www.countrylife.co.uk/food-drink/curious-question-why-was-the-tomato-considered-to-be-poisonous-241004
  quote: "Tomatoes were grown by the British purely for ornamental purposes, an attitude that persisted well until the 19th century" / "Gerard's opinion of the tomato, though based on a fallacy, prevailed in Britain and in the British North American colonies for over 200 years."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "（负向）画面里没有番茄——没有整颗、没有切片、没有番茄酱、没有红色酱汁"
  negative: "番茄、西红柿、番茄酱、红色浓酱、意式酱汁"

- fact_id: london1666.food.023
  claim: 玉米（maize / Indian corn / Turkish wheat）在 17 世纪欧洲虽有种植，但普遍被认为不如小麦大麦燕麦有营养；在英格兰不是人吃的主食
  tag: ❌
  source: ScienceDirect「A European perspective on maize history」+ Encyclopedia.com「The Natural History of Maize」
  source_url: https://www.sciencedirect.com/science/article/pii/S1631069110003045
  quote: "negative reactions to maize in the Old World largely focused on the belief that maize was less nourishing than extant European grain products such as wheat, barley, or oat cereals."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "（负向）画面里没有玉米——没有玉米棒、没有玉米粒、没有玉米面"
  negative: "玉米、玉米棒、爆米花、玉米面包、玉米粒"

- fact_id: london1666.food.024
  claim: 辣椒在 1548 年就在英格兰的**花园**里种着、1629 年 Parkinson 与 1653 年 Culpeper 的书里有它（药用/植物学），但**进入英国食谱**要到 1669 年 Evelyn 的一条醋渍配方；1666 年 9 月它不在英国人的菜里
  tag: ❌
  source: Edmund Standing「Hot Peppers and Hot Sauces in the English Cookery of the 17th to 19th Centuries」（引 John Evelyn, 1669）
  source_url: https://edmundstanding.wordpress.com/2020/05/28/hot-peppers-and-hot-sauces-in-the-english-cookery-of-the-17th-to-19th-centuries/
  quote: "in a separate Vinegar, gently bruise a Pod of Guinny-Pepper"（Evelyn, 1669，文中列为最早的烹饪用法指令）／ "There is no evidence of widespread use in English food during the 1660s—only theoretical applications mentioned in medical texts."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "（负向）画面里没有辣椒——没有红辣椒、没有辣椒粉、没有辣酱；当时的辛味来自黑胡椒、芥末、姜、肉豆蔻"
  negative: "辣椒、红辣椒串、辣椒粉、辣酱、咖喱"

- fact_id: london1666.food.025
  claim: **巧克力在 1666 年的伦敦是有的，而且就在咖啡馆里喝**——Pepys 1661-04-24 用「jocolatte」解宿醉，1664-11-24 明确写「到咖啡馆去喝 jocolatte，非常好」。伦敦第一家巧克力屋 1657 年就开了（判定说明：**不是**禁忌；禁忌的是固体巧克力）
  tag: ✅
  source: The Diary of Samuel Pepys, 24 April 1661 & 24 November 1664
  source_url: https://www.pepysdiary.com/diary/1664/11/24/
  quote: "About noon out with Commissioner Pett, and he and I to a Coffee-house, to drink jocolatte, very good; and so by coach to Westminster, being the first day of the Parliament's meeting."（1664-11-24）／ "so rose and went with Mr Creede to drink our morning draught, which he did give me in jocolatte to settle my stomach."（1661-04-24）
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "巧克力是**热饮**：深褐色、稠、带浮沫，装在小陶杯或锡镴杯里，在咖啡馆或巧克力屋喝；价钱昂贵"
  negative: "固体巧克力、巧克力块、巧克力棒、糖衣巧克力、可可粉包装、牛奶巧克力的浅棕色"

- fact_id: london1666.food.026
  claim: **茶在 1666 年的伦敦也是有的，但极新、极贵、极稀**——英语里第一条喝茶的记载就是 Pepys 1660-09-25：「后来我叫了一杯茶（一种中国饮料），以前从没喝过」。1663 年起茶与咖啡巧克力同受执照与税的管制（判定说明：存在，但**绝不是**日常饮料；当日常饮料画就是错）
  tag: ⚠️
  source: The Diary of Samuel Pepys, Tuesday 25 September 1660
  source_url: https://www.pepysdiary.com/diary/1660/09/25/
  quote: "And afterwards I did send for a cup of tee (a China drink) of which I never had drank before, and went away."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "茶只可能出现在咖啡馆的价目里、或作为稀罕货被提到；平民手里、家里、街上一律没有茶"
  negative: "家里泡茶、下午茶、茶壶茶杯成套、加奶加糖的英式红茶、街上喝茶、任何把茶当日常的镜头"
  note: 1660 年这杯茶正是在咖啡馆（Sultaness Head, Sweetings Rents）喝到的。**「英国人＝喝茶」这个刻板印象在 1666 年完全不成立**，这是本站极好的一个反差点。

- fact_id: london1666.food.027
  claim: 叉子在 17 世纪英格兰仍被视为**意大利式的外国做作**；Thomas Coryat 1611 年自称是伦敦第一个用叉子吃饭的人，为此得了个「Furcifer（叉子佬）」的绰号。对多数人来说刀、勺和手指就够了——用手指或刀尖把食物送进嘴。到 17 世纪中叶叉子在上层与贵族中已近常态，三齿四齿叉从 17 世纪第三个四分之一才出现（判定说明：平民用叉子＝错；上流餐桌上有叉子＝可以）
  tag: ❌
  source: Country Life「Who invented the fork?」+ 综合（Richard Crosse 1632 双齿叉）
  source_url: https://www.countrylife.co.uk/food-drink/curious-questions-who-invented-the-fork-251540
  quote: "For 17th-century Englishmen, a fork was a foreign affectation particularly associated with Italy and Italians. In a nation where, for many, knives, spoons and fingers were adequate to the task of eating — with fingers or the point of a knife used to bring food to the mouth — forks would continue to provoke both ribaldry and disapproval into the next century." / "Early forks, such as that made by London spoon-maker Richard Crosse in 1632, had two prongs" / "Three- and four-prong forks appeared from the third quarter of the 17th century."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "平民吃饭只有**手指、一把刀、一只勺**：肉用刀尖挑进嘴，汤羹用木勺或角勺，面包用手撕"
  negative: "叉子、刀叉并排摆放、三齿或四齿叉、西餐摆台、餐巾折花、成套餐具"

- fact_id: london1666.food.028
  claim: 餐具按阶层分层：极穷用木托盘（trencher）与陶杯／深木碗；自耕农与中等人家用锡镴（pewter）——较穷的自耕农家里 6–12 件锡镴器，中等以上 40–50 件；乡绅用银器与进口瓷器
  tag: ✅
  source: OLD-ENGLISH「Yeoman's House」+ John Moore Museum「The Humble Trencher」
  source_url: https://www.johnmooremuseum.org/the-humble-trencher/
  quote: "Wooden trenchers were still in everyday use in the yeoman's house but most also had pewter. Inventories of the poorer yeomen showed 6 to 12 pewter pieces but the average and above had 40 to 50." / "The gentry ate from silver and imported china; the very poor made out with wooden trenchers and pottery mugs." / "More practical and economic versions were made of wood (oak, beech, sycamore or pine), the slightly finer pewter."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "器皿分三档：穷人是方形或圆形木托盘 trencher（橡木/山毛榉，边缘刀痕累累、油浸发黑）＋ 素陶杯；中等人家是灰白哑光的锡镴盘与锡镴大杯（不反光、有凹痕与磨白的边）；只有乡绅桌上才有银器与瓷器"
  negative: "白瓷盘、玻璃杯、不锈钢餐具、成套同款餐具、现代碗碟、闪亮反光的金属器皿"
```

## 4.6 两顿可拍的饭

### 饭一 · 街头（正午前后，市集边上）

**菜品**
- 一块 **maslin 面包**（小麦掺黑麦，灰褐色、大而扁、外皮硬）或一便士的 **cheat 面包**（米黄带细麸点）— food.006 / 007
- 一块**硬干酪**（食.003）
- **牡蛎**，从浅筐里现开现吃，壳扔脚边 — food.014
- 一杯 **small beer**，浑浊浅琥珀色 — food.010 / 011

**器皿**：没有盘子。面包本身就是托——把干酪压在面包上用手拿着；牡蛎直接从壳里吸；啤酒装在**素陶杯**或**角杯**里。— food.028

**怎么吃**：**全部用手 + 一把随身的小刀**。**没有叉子**。— food.027

**口播可用的点**：「这一便士买到的东西，比我在 21 世纪一便士买到的多得多；但这块面包的重量，是由市长今年定的小麦价决定的——价钱永远是一便士，变的是它有多大。」（依据 food.007；**不要报具体盎司数**，见 food.008 ⚠️）

### 饭二 · 咖啡馆（下午）

**⚠️ 本站的女性旅行者进不去。** 见 food.020。三种处理方式，任选其一但必须是**有意设计**的：
1. 她站在门口往里拍，口播说明「这扇门后面是 1666 年伦敦最重要的公共空间，而它不欢迎我」——这是最强的一条。
2. 她硬进去，全场安静下来看她——把「被排除」拍成戏。
3. 换成**酒馆 / ordinary**（下面的备选），那里女性可以在。

**咖啡馆里有什么**
- **一碟（dish）咖啡**，一便士；深褐、浑浊、很可能又苦又糊 — food.017
- **jocolatte（热巧克力）**，稠、深褐、带浮沫，贵 — food.025
- **茶**，有，但是稀罕货，不是人人点 — food.026
- 一斗**陶土长烟斗**的烟草，含在那一便士里 — food.017
- 桌上摊着**单页新闻纸（Gazette）**，有人念出声 — food.018

**器皿**：浅**陶碗**或小**陶杯**（不是马克杯、不是玻璃）。白色**陶土长烟斗**。

**怎么吃喝**：挤在长条木桌与长凳上，谁先到坐哪儿，**不讲座次**（1674 年《咖啡馆规约》：「Pre-eminence of place none here should mind, but take the next fit seat he can find」）；各付各的（「let each man what he calls for pay」）。屋里烟雾弥漫。

```yaml
- fact_id: london1666.food.029
  claim: 1674 年张贴在英格兰咖啡馆墙上的《Rules and Orders of the Coffee House》规定：不论身份高低，坐最近的空位即可；各人自付自点；骂脏话罚十二便士；起争执者要请对方喝一碟咖啡；禁牌禁骰，赌注不得超过五先令
  tag: ✅
  source: The Rules and Orders of the Coffee House（1674 年单页印刷品背面的诗）
  source_url: https://uncommon-courtesy.com/2014/04/11/how-to-handle-yourself-in-an-17th-century-coffee-house/
  quote: "Enter, sirs, freely, but first, if you please, / Peruse our civil orders, which are these." / "Pre-eminence of place none here should mind, but take the next fit seat he can find." / "let each man what he calls for pay."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "咖啡馆里不排座次：长凳上挤着穿绸缎的与穿粗呢的，肩挨着肩；墙上钉着一张印着规约的单页纸"
  negative: "分区雅座、贵宾席、侍者引位、按身份分桌"
  note: 单页印于 1674 年，晚于本站 8 年。作为「1660–70 年代咖啡馆风气」成立，**不得作为 1666 年墙上就贴着这张纸的依据**。
```

**备选：酒馆 / ordinary（女性可在）**
- 一块从**熟食铺**买来或酒馆自烤的**羊肩肉**（food.013，Pepys 亲身记录）
- **面包**与**干酪**
- **small beer** 或一品脱**葡萄酒**（Pepys 常与人「a pint or two of wine」— food.004 来源同页）
- **器皿**：锡镴盘、锡镴大杯、木勺；**没有叉子**；**没有餐巾**（Pepys 1666-09-04 原话就是 "without any napkin or any thing"）

---

# §13 误传清单（本站可直接引用的 ❌ 条目）

| # | 误传 | 正解 | fact_id |
|---|---|---|---|
| 1 | 男人穿及膝长外套 vest / 三件套雏形 | 查理二世 1666-10-07 才在枢密院宣布、10-15 才首次穿；比本站晚 5 周，且大火已在其间发生 | dress.001 / 002 |
| 2 | 清教徒式全黑衣 | 黑染料贵且易褪，黑衣是主日与画像的最好衣裳；日常是「sadd colours」沉色——赤褐、枯叶褐、茶褐、暗橄榄 | dress.016 / 017 |
| 3 | 高顶窄檐黑帽 + 帽子上一枚方形大金属扣 | capotain 属内战前与共和期，1666 年已过时；帽扣纯属 19 世纪想象。此时是矮冠宽檐软毡帽 | dress.018 |
| 4 | 三角帽 tricorne + 长马甲 + 紧身及膝马裤 | 那是 18 世纪。1666 年是短 doublet + 阔如短裙的 petticoat breeches | dress.004 / 005 / 018 |
| 5 | 鲜艳饱和的化学染料色、崭新挺括的布 | 只有天然染料、褪色快；应是洗旧的柔和沉色，同件衣服深浅不匀 | dress.009 / 017 |
| 6 | 劳动阶层女性戴蕾丝、系花边围裙 | 蕾丝是穷人做、富人穿；劳动阶层零蕾丝零装饰织带 | dress.010 |
| 7 | 女性披散长发上街 | 除非富到能做发型，否则一律遮发（coif / hood / 方巾） | dress.011 / 012 |
| 8 | 土豆（含薯条、土豆泥、炸鱼薯条） | 1662 年皇家学会才开始推广，此时是富人花园的稀罕物，成为主食要等 19 世纪 | food.021 |
| 9 | 番茄、番茄酱 | 英国视为「毒苹果」，纯观赏，这个观念持续两百多年 | food.022 |
| 10 | 玉米 | 被认为不如麦类有营养，不是英格兰人吃的东西 | food.023 |
| 11 | 辣椒、辣酱 | 花园里有、药书里有，但进英国食谱要到 1669 年 Evelyn 的醋渍配方 | food.024 |
| 12 | 平民用叉子吃饭、刀叉摆台 | 叉子是「意大利式外国做作」；平民靠手指、刀尖、勺 | food.027 |
| 13 | 喝清水、玻璃水杯 | 伦敦没有干净饮用水，上下老小都喝 small beer；器皿是陶、木、锡镴 | food.010 / 028 |
| 14 | 英国人=喝茶；家里泡茶、下午茶 | 英语里第一条喝茶记载是 Pepys 1660-09-25，且是在咖啡馆。1666 年茶极新极贵，不是日常 | food.026 |
| 15 | 女性自在地坐在咖啡馆里 | 名义开放、实际排除体面女性；1674 年还出了《Women's Petition Against Coffee》 | food.020 |
| 16 | 「新世界作物一律没有」的一刀切 | 火鸡 1570 年代就传入、1660 年代常见；巧克力 1657 年起有巧克力屋、Pepys 在咖啡馆喝 jocolatte | food.015 / 025 |

---

# 待人工核证清单（按优先级）

| 优先级 | 项 | 缺什么 | 建议来源 |
|---|---|---|---|
| **高** | food.008 · 1666 年伦敦 assize 具体重量表 | 一便士白/wheaten/household 面包各重几盎司 | London Metropolitan Archives, Corporation of London assize records；British History Online 17 世纪 City records |
| **高** | food.016 · 星期六是否为法定鱼日 | 伊丽莎白朝「政治性鱼日」法在 1666-09-01（周六）的实际约束力 | 5 Eliz. c. 5 的存废；1660 年代 Lenten proclamations 原件 |
| **高** | food.005 · Farriner | 只有 Wikipedia + 旅游站；需一手 | National Archives 壁炉税记录；Bakers' Company 档案；London Museum 2023 新发现（首位目击者） |
| 中 | food.002 / 003 / 012 | 出处不明的综述与价格 | Liza Picard, *Restoration London*（1997）相关章节 |
| 中 | dress.017 · sadd colours | 1638 年清单出自新英格兰语境 | Fischer, *Albion's Seed* 原书注脚；英格兰本土的同期 inventory |
| 中 | 套 B · 搬运工/面包师行业着装 | 未查到 1660 年代伦敦的行业服色惯例 | Laroon, *The Cryes of the City of London*（1688）图像；Bakers' Company 规章 |
| 中 | 套 D · 女仆是否有雇主提供的 livery | 男仆 livery 有据，女仆未查到 | 1660 年代伦敦家户账簿 |
| 低 | dress.019 / food.029 | Randle Holme(1688)、Coffee House Rules(1674) 均晚于本站 | 找 1660 年代更早的同类记载做交叉 |

# 图库需求（转交 stage 2）

本次**未生成任何参考图**（本 worker 只做史料）。stage 2 建立资产时，按 §3.1 的五套锁定串各建一张人物锚点图，并按 ai_video.md rule 4b-A 给每个 fenced prompt 加路由键前缀。

食物侧建议建的主体卡：`p{N}_面包摊`（manchet/cheat/maslin 三档同框）、`p{N}_锡镴与木器`（trencher + pewter + 角勺 + 陶杯，零叉子）、`bg{N}_咖啡馆内景`（长桌长凳 + 烟雾 + 陶碗 + 单页新闻纸）。
