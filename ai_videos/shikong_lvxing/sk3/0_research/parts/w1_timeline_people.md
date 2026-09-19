---
worker_id: researcher-w1-timeline
stage: 0
role: researcher
angle: timeline-and-people
status: complete
blockers: []
confidence: high
---

# sk3 伦敦 1666-09-01 · 阶段 0 史料调研 · w1（§1 时空坐标 / §11 当日时间线 / §12 人物）

调研时间：2026-09-18。方法：所有 fact 均为实际抓取原文页后逐字摘录；
`pepysdiary.com` 对 WebFetch 返回 403，改用 curl + UA 抓取全文后本地解析；
`theconversation.com` curl SSL 失败，改用 WebFetch 定向取原句。
Gutenberg 的 Evelyn 日记全本已下载并本地 grep（`42081-h.htm`），
1667 年 Rege Sincera 小册子（内含《伦敦公报》官方通告全文）从
`fireoflondon.org.uk` 的转录 PDF 取得并 `pdftotext` 抽取。

**本站最重要的一条结论写在最前面**：任务要求核实的市长名言
「Pish! A woman might piss it out」**不在 Pepys 日记里**——见
`london1666.people.005`，这是本轮最需要用户回看的一条。

---

## §1 时空坐标

```yaml
- fact_id: london1666.coord.001
  claim: 1666 年 9 月 1 日（儒略历）是星期六；次日 9 月 2 日是星期日，Pepys 在日记开头亲笔写作「Lord's day」（主日）。
  tag: ✅
  source: The Diary of Samuel Pepys, 1 & 2 September 1666（pepysdiary.com 逐日页标题 + 日记正文）
  source_url: https://www.pepysdiary.com/diary/1666/09/02/
  quote: "Sunday 2 September 1666 — (Lord's day). Some of our mayds sitting up late last night to get things ready against our feast to-day, Jane called us up about three in the morning"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "1666年9月1日星期六傍晚的伦敦城，第二天是主日，家家在为周日备餐"
  negative: "现代日期显示,数字时钟,工作日通勤,周一早高峰"

- fact_id: london1666.coord.002
  claim: 1666 年英格兰仍用儒略历（旧历），与欧陆格里高利历（新历）相差 10 天；故旧历 1666-09-01 ≈ 新历 1666-09-11。英国迟至 1752 年才改历。
  tag: ⚠️
  source: University of Nottingham, Manuscripts & Special Collections, "Julian/Gregorian Calendars" 研究指南
  source_url: https://www.nottingham.ac.uk/manuscriptsandspecialcollections/researchguidance/datingdocuments/juliangregorian.aspx
  quote: "In correspondence between Britain and France between 1582 and 1752, for instance, there would be a discrepancy of 10 or 11 days between the two calendars."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "格里高利历日期,1752年后历法,双日期标注"
```

> ⚠️ **分歧说明（coord.002）**：我实际读到的学术页只说「10 或 11 天」，
> 没有为 1666 年单独落一个数。10 天这个值是由规则推出来的（1582 改历减 10 天，
> 1700 年才因儒略闰年多出第 11 天），不是某一页原文直接写的 1666。
> Wikipedia 的换算表页面我也抓了，但它给的最近一行是 1500 年，同样没有 1666 专行。
> **结论仍取 10 天（这是史学界通识），但按要求标 ⚠️ 而非 ✅。**

```yaml
- fact_id: london1666.coord.003
  claim: 火灾前的那个夏天异常炎热干旱，东风持续猛吹——这是同时代 1667 年印行的小册子明写的成因清单之一。
  tag: ✅
  source: Rege Sincera, "Observations both Historical and Moral upon the Burning of London, September 1666"（London, 1667）
  source_url: https://www.fireoflondon.org.uk/assets/uploads/2016/08/Transcript_42.39_55.pdf
  quote: "the preceding Summer which was extraordinarily hot and dry, the East wind that blew violently all that while, and the want of Engines and water to quench the fire"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "久旱后的伦敦木构街区，木料干透发白，屋瓦烫手，空气里浮着细尘"
  negative: "湿润路面,雨天,泥泞街道,青苔,潮湿墙面,阴雨天空"

- fact_id: london1666.coord.004
  claim: Pepys 本人在 9 月 2 日日记里把「长期干旱」写成火势失控的直接原因，并说连教堂的石头都变得可燃。
  tag: ✅
  source: The Diary of Samuel Pepys, 2 September 1666
  source_url: https://www.pepysdiary.com/diary/1666/09/02/
  quote: "and every thing, after so long a drought, proving combustible, even the very stones of churches"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "干裂的木板墙与晒透的沥青木瓦，触手发烫"
  negative: "湿木头,水渍,雨后反光,新刷油漆的鲜亮墙面"

- fact_id: london1666.coord.005
  claim: 起火后刮的是猛烈东风——Evelyn 亲笔记「a fierce eastern wind in a very dry season」，《伦敦公报》官方通告也记「violent Easterly winde」。两条互相独立印证。
  tag: ✅
  source: The Diary of John Evelyn, 3 September 1666（Project Gutenberg #42081, Vol. II）；另见 London Gazette, Whitehall, September 8, 1666
  source_url: https://www.gutenberg.org/files/42081/42081-h/42081-h.htm
  quote: "The fire having continued all this night ... when conspiring with a fierce eastern wind in a very dry season, I went on foot to the same place"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "自东方吹来的持续强风，掀动招牌、吹斜炊烟、卷起街面细尘，人得侧身迎风走"
  negative: "无风,静止空气,烟柱笔直上升,西风,旗帜低垂"

- fact_id: london1666.coord.006
  claim: 《伦敦公报》官方通告把东风列为火势蔓延的关键推手，措辞为「a violent Easterly winde fomented it」。
  tag: ✅
  source: The London Gazette, No. 85, dated "Whitehall, September 8" 1666（1667 年 Rege Sincera 小册子全文转载）
  source_url: https://www.fireoflondon.org.uk/assets/uploads/2016/08/Transcript_42.39_55.pdf
  quote: "It fell out most unhappily too, that a violent Easterly winde fomented it, and kept it burning all that day"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "无风,顺风减弱,风向标静止"
```

> 注：`.thegazette.co.uk` 官方站的 issue 85 PDF（`/London/issue/85/data.pdf`，HTTP 200，193 KB）
> **是纯扫描图、无文字层**（pdftotext 抽出 2 字节）。上面这条走的是
> 伦敦博物馆「Fire of London」教育站的官方转录 PDF，转录内含 1667 年小册子完整排版，
> 可信度高，但**它是转录件不是扫描件**——列入人工抽查清单。

**§1 给分镜的可用结论**：
- 拍摄时刻＝**1666-09-01 星期六**，黄昏到深夜；次日是主日，全城在为周日做准备。
- 天候＝**久旱之末 + 猛烈东风**。街道干燥、木构干透、风声是这一站的底噪。
- 全城尚不知道：**7 小时后（9/2 约 01:00）**布丁巷就要起火。

---

## §11 当日大事时间线（1666-09-01 清晨 → 09-02 约 03:00）

### 时间轴（凡时间点均标注出处强度）

| 时刻（旧历） | 事件 | 强度 |
|---|---|---|
| 9/1 上午 | Pepys 整个上午在海军署办公，随后回家吃饭 | ✅ T0 |
| 9/1 午后 | 把新书房彻底打扫干净「against to-morrow」——为次日主日的宴客做准备 | ✅ T0 |
| 9/1 下午 | 与 Sir W. Pen、妻子、Mercer 去看「Polichinelly」（木偶戏，即 Punch 的前身）；Young Killigrew 带一群纨绔进场，四人吓得躲起来 | ✅ T0 |
| 9/1 傍晚 | 戏散后去伊斯灵顿吃喝，「mighty merry」，一路唱着歌回家 | ✅ T0 |
| 9/1 夜 | Pepys 回办公室写了一两封信，然后就寝 | ✅ T0 |
| 9/1 约 20:00–21:00 | Farriner 按平常时间打烊；为周日正餐备了几罐炖肉，把炉膛的煤耙拢，上楼睡觉 | ⚠️ T2（Tinniswood 复原） |
| 9/1 约 24:00 | 女儿 Hanna 查看烤房、再巡一遍屋子确认无事，然后也去睡 | ⚠️ T2（Tinniswood 复原） |
| 9/2 约 01:00 | **官方口径的起火时刻**：《伦敦公报》「at one of the Clock in the morning」，布丁巷近新鱼街 | ✅ T0 |
| 9/2 01:00–02:00 | Farriner 的帮工（journeyman）被烟呛醒——Harley 议员家书原话「between one and two His man was waked with ye choak of ye Smoke」 | ✅ T0（引于 T1） |
| 9/2 约 01:00 后 | 全家翻出楼上窗户、沿檐槽爬进邻居家窗户逃生；女仆不敢跟，死在屋里 | ⚠️ T2 + ✅ T0 家书 |
| 9/2 约 03:00 | **女仆 Jane 叫醒 Pepys**，说城里起大火；Pepys 披上睡袍到窗边看，判断「far enough off」，回去接着睡 | ✅ T0 |
| 9/2 约 07:00 | Pepys 再起身，此时火看起来「不如先前大、而且更远」 | ✅ T0 |
| 9/2 上午 | Jane 报：已烧掉三百多间房，正沿鱼街往伦敦桥烧；Pepys 上塔楼、下船，见到全景 | ✅ T0 |
| 9/2 上午 | 塔楼副官告诉 Pepys：**火起于布丁巷「国王的面包师」家中** | ✅ T0 |
| 9/2 正午前 | Pepys 面奏国王与约克公爵；国王下令「spare no houses, but to pull down before the fire every way」 | ✅ T0 |
| 9/2 正午前后 | Pepys 在坎宁街遇到市长 Bloodworth——脖子上围着手帕、形容枯槁 | ✅ T0 |
| 9/2 约 22:00 | Evelyn 的日记把起火记成「about ten」——**与官方 1 点说法冲突** | ⚠️ T0 冲突 |

---

### 逐条 fact

```yaml
- fact_id: london1666.timeline.001
  claim: 9 月 1 日星期六，Pepys 上午在办公室、回家吃饭、把新书房打扫干净「为明天」（即次日主日的宴客）。
  tag: ✅
  source: The Diary of Samuel Pepys, 1 September 1666（全文仅一段，此为开头）
  source_url: https://www.pepysdiary.com/diary/1666/09/01/
  quote: "Up and at the office all the morning, and then dined at home. Got my new closet made mighty clean against to-morrow."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "17世纪伦敦市民家中，男主人指挥仆人擦洗一间新书房，为明天的宴客做准备"
  negative: "现代清洁用品,吸尘器,塑料桶,电灯"

- fact_id: london1666.timeline.002
  claim: 9 月 1 日下午，Pepys 一行去看「Polichinelly」木偶戏（Punch 先生的意大利原型），因怕被约克公爵的寝宫侍从 Young Killigrew 撞见「上班时间寻乐」而躲藏；散场后去伊斯灵顿吃喝、一路唱歌回家。
  tag: ✅
  source: The Diary of Samuel Pepys, 1 September 1666（正文 + L&M 注，见页面 annotations）
  source_url: https://www.pepysdiary.com/diary/1666/09/01/
  quote: "Sir W. Pen and my wife and Mercer and I to “Polichinelly,” but were there horribly frighted to see Young Killigrew come in with a great many more young sparks; but we hid ourselves, so as we think they did not see us. ... and so, the play being done, we to Islington, and there eat and drank and mighty merry; and so home singing"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "露天木偶戏棚前的人群，木偶Punch在小台上挥棒，观众哄笑；几个衣着体面的人缩在人堆后面躲avoid视线"
  negative: "现代提线木偶剧场,电动玩偶,舞台灯光,麦克风"

- fact_id: london1666.timeline.003
  claim: Farriner 9 月 1 日星期六约晚八九点按常规打烊，为次日主日备了几罐炖肉，把炉膛的煤耙拢后上楼睡；女儿 Hanna 约午夜查看过烤房与整屋，确认无事才去睡。
  tag: ⚠️
  source: Adrian Tinniswood 著作节选（Penguin "How the Great Fire of London started"）
  source_url: https://www.penguin.co.uk/discover/articles/how-the-great-fire-of-london-started
  quote: "Thomas Farriner closed for business at the usual time on Saturday evening, around eight or nine at night. He prepared several pots of baked meat for Sunday dinner, raked up the coals in the hearth and went to bed. ... Hanna checked on the bakehouse around midnight, when she also took a last look round the house to make sure all was well. Then she too went to bed."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "深夜的木构面包铺烤房，砖砌蜂窝炉膛里余煤被耙拢成一堆，暗红余烬无明火；一名年轻女子提着烛台最后巡视一圈"
  negative: "明火熊熊,炉门大开火舌外窜,现代烤箱,金属排烟管,电灯泡"

- fact_id: london1666.timeline.004
  claim: 官方口径的起火时刻是 9 月 2 日凌晨一点，地点布丁巷近新鱼街；官方通告同时承认「本该拆房断火却没及时办」。
  tag: ✅
  source: The London Gazette No. 85, "Whitehall, September 8" 1666（Rege Sincera 1667 转录本）
  source_url: https://www.fireoflondon.org.uk/assets/uploads/2016/08/Transcript_42.39_55.pdf
  quote: "On the Second instant, at one of the Clock in the morning, there happened to break out a sad and deplorable Fire in Pudding-lane near New-Fishstreet; which falling out at that hour of the night, and in a quarter of the Town (so close built with Wooden pitched Houses.) spread it self so far before day, and with such disraction to the Inhabitants and Neighbours, that care was not taken for the timely preventing the further diffusion of it, by pulling down Houses, as it ought to have have been"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "凌晨一点的布丁巷，两侧木构房屋外墙涂着防水柏油，巷道极窄，二层向外挑出几乎相触"
  negative: "宽阔街道,砖石立面,路灯,现代消防通道"

- fact_id: london1666.timeline.005
  claim: 最早发现火情的是 Farriner 的帮工，约凌晨一点到两点之间被烟呛醒；同一封家书还明说「火起处远离烟囱与烤炉」。
  tag: ✅
  source: 议员 Sir Edward Harley 1666 年家书，引于 Kate Loveman（University of Leicester）2023 年研究
  source_url: https://theconversation.com/great-fire-of-london-how-we-uncovered-the-man-who-first-found-the-flames-214443
  quote: "that between one and two His man was waked with ye choak of ye Smoke, the fire begun remote from ye chimney and Oven"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "一名年轻男工在阁楼被浓烟呛醒，猛地坐起咳嗽，烟从地板缝往上渗"
  negative: "火舌扑面,明亮火光照满房间,现代烟雾报警器,消防喷淋"

- fact_id: london1666.timeline.006
  claim: 这名帮工 2023 年被首次具名考订为 Thomas Dagger（威尔特郡 Norton 人），1655 年入学徒、1664 年满师后留在布丁巷做非正式帮工。
  tag: ✅
  source: Kate Loveman（University of Leicester）为伦敦博物馆所做的研究，2023
  source_url: https://www.londonmuseum.org.uk/about/press/press-releases/first-witness-to-the-great-fire-of-london-uncovered/
  quote: "Thomas Dagger's role has gone unrecognised ... can now be identified for the first time as Thomas Dagger"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "无名氏,匿名仆人,女性帮工"

- fact_id: london1666.timeline.007
  claim: Farriner 家的女仆不敢跟着逃、被烧死在屋里，成为大火第一个遇难者；她的名字至今无考。
  tag: ✅
  source: Sir Edward Harley 家书（同上），引于 Loveman 2023
  source_url: https://theconversation.com/great-fire-of-london-how-we-uncovered-the-man-who-first-found-the-flames-214443
  quote: "His mayd was burnt in ye Hous not adventuring to Escape"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "全家平安撤离,无人伤亡,有名有姓的女仆"

- fact_id: london1666.timeline.008
  claim: Pepys 家女仆 Jane 约凌晨三点叫醒他；他披上睡袍到窗边看，判断火在马克巷背后「够远的」，就回去继续睡。
  tag: ✅
  source: The Diary of Samuel Pepys, 2 September 1666
  source_url: https://www.pepysdiary.com/diary/1666/09/02/
  quote: "Jane called us up about three in the morning, to tell us of a great fire they saw in the City. So I rose and slipped on my nightgowne, and went to her window, and thought it to be on the backside of Marke-lane at the farthest; but, being unused to such fires as followed, I thought it far enough off; and so went to bed again and to sleep."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "凌晨三点，男人披着长睡袍站在阁楼窗前，远处城里一片橙红火光；他看了一会儿转身走开"
  negative: "惊慌奔跑,大喊大叫,现代睡衣,电灯开关"

- fact_id: london1666.timeline.009
  claim: Pepys 约七点再起身，此时看火「不如先前大、而且更远」；直到 Jane 报「已烧掉三百多间房、正沿鱼街烧向伦敦桥」他才认真起来。
  tag: ✅
  source: The Diary of Samuel Pepys, 2 September 1666
  source_url: https://www.pepysdiary.com/diary/1666/09/02/
  quote: "About seven rose again to dress myself, and there looked out at the window, and saw the fire not so much as it was and further off. ... By and by Jane comes and tells me that she hears that above 300 houses have been burned down to-night by the fire we saw, and that it is now burning down all Fish-street, by London Bridge."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "立即报警,连夜救火,现代新闻播报"

- fact_id: london1666.timeline.010
  claim: 塔楼副官当面告诉 Pepys，火起于布丁巷「国王的面包师」家——这是「Farriner 是国王供应商」这一身份的同时代一手印证。
  tag: ✅
  source: The Diary of Samuel Pepys, 2 September 1666
  source_url: https://www.pepysdiary.com/diary/1666/09/02/
  quote: "the Lieutenant of the Tower, who tells me that it begun this morning in the King’s baker’s house in Pudding-lane, and that it hath burned St. Magnus’s Church and most part of Fish-street already"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "普通面包铺,无王室关联,现代连锁烘焙店"

- fact_id: london1666.timeline.011
  claim: Evelyn 日记 9 月 2 日条把起火时刻记成「about ten」（晚十点），与官方「凌晨一点」严重不符——这是两份一手史料之间的真实分歧。
  tag: ⚠️
  source: The Diary of John Evelyn, 2 September 1666（Project Gutenberg #42081 Vol. II，全条仅一句）
  source_url: https://www.gutenberg.org/files/42081/42081-h/42081-h.htm
  quote: "2d September, 1666. This fatal night, about ten, began the deplorable fire, near Fish street, in London."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "唯一确定的起火时间,史料一致,无争议"

- fact_id: london1666.timeline.012
  claim: Evelyn 9 月 3 日日记：先在家做礼拜，午饭后带妻儿乘马车到南岸 Bankside，眼看伦敦桥到三起重机一线全部烧尽。
  tag: ✅
  source: The Diary of John Evelyn, 3 September 1666
  source_url: https://www.gutenberg.org/files/42081/42081-h/42081-h.htm
  quote: "3d September, 1666. I had public prayers at home. The fire continuing, after dinner, I took coach with my wife and son, and went to the Bankside in Southwark, where we beheld that dismal spectacle, the whole city in dreadful flames near the waterside; all the houses from the Bridge, all Thames street, and upward toward Cheapside, down to the Three Cranes, were now consumed; and so returned, exceedingly astonished what would become of the rest."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "泰晤士河南岸，一家三口站在河边眺望对岸整座城市在火里"
  negative: "近距离火场,消防员,现代河岸护栏"
```

### 9 月 1 日本身有没有可考的事件？

**有，而且对本站极有用。** 三条：

1. **Pepys 的一整天都有记载**（timeline.001 / 002）——上午办公、下午看木偶戏躲人、
   晚上伊斯灵顿吃喝唱歌回家。这是**「大火前最后一个普通周六」**的完整一手样本，
   vlog 可以直接跟着这条线走。
2. **次日是主日**，全城在备周日正餐（Pepys 打扫书房「against to-morrow」并要宴客；
   Farriner 备了周日炖肉）。**「明天要请客」是这一站最好的反讽装置。**
3. **五天前（8 月 27 日）Evelyn 和 Christopher Wren 刚在老圣保罗大教堂现场勘察完毕，
   决定给它加一个英格兰前所未见的穹顶**——见 `london1666.timeline.013`。
   老教堂九天后就烧成废墟，Wren 后来真的造了穹顶，但是在新教堂上。
   **这是本站最强的一个「你们不知道的事」钩子。**

```yaml
- fact_id: london1666.timeline.013
  claim: 1666 年 8 月 27 日（大火前 6 天），Evelyn 与 Christopher Wren 等人现场勘查老圣保罗大教堂，两人力排众议主张塔楼须另起新基，并提议建一座「英格兰尚不知有此形制」的宏伟穹顶。
  tag: ✅
  source: The Diary of John Evelyn, 27 August 1666
  source_url: https://www.gutenberg.org/files/42081/42081-h/42081-h.htm
  quote: "but we totally rejected it, and persisted that it required a new foundation, not only in regard of the necessity, but for that the shape of what stood was very mean, and we had a mind to build it with a noble cupola, a form of church-building not as yet known in England, but of wonderful grace."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "老圣保罗大教堂中殿，一群17世纪男子举着图纸仰头讨论，塔楼内部脚手架林立"
  negative: "现代圣保罗大教堂的穹顶,雷恩爵士晚年形象,完工的白色石砌穹顶"

- fact_id: london1666.timeline.014
  claim: 老圣保罗被烧时，教堂拱顶塌落砸穿地下的圣福音堂（St Faith's），书商行会（Stationers）搬进去避难的全部存书被点着，连烧一周。
  tag: ✅
  source: The Diary of John Evelyn, 1666 年 9 月 7 日勘察废墟条
  source_url: https://www.gutenberg.org/files/42081/42081-h/42081-h.htm
  quote: "The ruins of the vaulted roof falling, broke into St. Faith's, which being filled with the magazines of books belonging to the Stationers, and carried thither for safety, they were all consumed, burning for a week following."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "书籍被抢救出来,地窖安全,现代图书馆"
```

> ✅ **任务点回答**：「书商把存书搬进圣福音堂地窖结果全烧」这条**属实**，
> 而且有 Evelyn 亲眼所见的一手原文（上条）。可放心用作虚构人物「书商学徒」的盼头。

---

## §12 可观察 / 可对话的人物

### A. 真实历史人物（只念有记载的原话）

```yaml
- fact_id: london1666.people.001
  claim: Thomas Farriner（亦拼 Farynor / Faryner），布丁巷面包师，1637 年入面包师行会，1649 年起在圣玛格丽特新鱼街教区开铺（今纪念碑所在地）；1666 年时任「Conduct of the King's Bakehouse」并为海军供应饼干（ship's biscuit），本人还是教区执事。1670 年卒，葬于圣马格努斯教堂中殿。
  tag: ✅
  source: pepysdiary.com Encyclopedia, "Thomas Farriner"（站点编者据 L&M 注与行会记录编纂）
  source_url: https://www.pepysdiary.com/encyclopedia/10873/
  quote: "After an apprenticeship, he became a member of the Baker's Company in 1637 and by 1649 had set up shop with his wife at Pudding Lane in the parish of St Margaret New Fish Street (now the site of the Monument). By 1666 he held the post of 'Conduct of the King's Bakehouse', and was supplying the Navy with biscuits. He was also a churchwarden."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "五十多岁的伦敦面包师，围裙沾面粉，手背有旧烫疤，站在自家窄门面的烤房前"
  negative: "年轻面包师,白色现代厨师服,连锁店招牌,金属烤盘"

- fact_id: london1666.people.002
  claim: 9 月 1 日当晚 Farriner 家里的人可考的有四位：本人、成年女儿 Hannah、儿子 Thomas、帮工 Thomas Dagger，外加一名死于火中的女仆。
  tag: ✅
  source: London Museum 新闻稿（Kate Loveman 研究，2023）
  source_url: https://www.londonmuseum.org.uk/about/press/press-releases/first-witness-to-the-great-fire-of-london-uncovered/
  quote: "The Farriner household survivors included Thomas Farriner, his adult children Hannah and Thomas, and his journeyman Thomas Dagger. One maid perished in the fire."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "大家庭,众多仆役,独居老人"

- fact_id: london1666.people.003
  claim: Samuel Pepys，海军署官员，1666 年 9 月 1 日全天行踪有逐条日记可考；他是本站唯一能提供「前一夜完整一天」的真实人物。
  tag: ✅
  source: The Diary of Samuel Pepys, 1 September 1666
  source_url: https://www.pepysdiary.com/diary/1666/09/01/
  quote: "Up and at the office all the morning, and then dined at home. ... and so home singing, and, after a letter or two at the office, to bed."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "三十三岁的海军署官员，深色外套与白色领巾，晚上提灯从办公室走回家"
  negative: "假发夸张的晚年Pepys肖像,现代公务员西装"

- fact_id: london1666.people.004
  claim: 市长 Sir Thomas Bloodworth 有据可查的原话，是 9 月 2 日正午前后在坎宁街对 Pepys 说的一段崩溃之词：「主啊，我能怎么办？我已经用尽了，人们不听我的。」
  tag: ✅
  source: The Diary of Samuel Pepys, 2 September 1666
  source_url: https://www.pepysdiary.com/diary/1666/09/02/
  quote: "At last met my Lord Mayor in Canningstreet, like a man spent, with a handkercher about his neck. To the King’s message he cried, like a fainting woman, “Lord! what can I do? I am spent: people will not obey me. I have been pulling down houses; but the fire overtakes us faster than we can do it.”"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "中年市长，脖子上胡乱围着一条手帕，满脸烟灰与倦容，在街上对人摊手"
  negative: "威严市长袍,金链,镇定自若,发号施令"

- fact_id: london1666.people.005
  claim: 名言「Pish! A woman might piss it out」**不在 Pepys 日记中**。对 pepysdiary.com 全日记做 "piss" 全文检索共 18 条命中，无一条出自 1666 年 9 月 2 日（1666 年 9 月唯一命中是 9 月 18 日，内容是 Pepys 自述排尿）。Wikipedia 虽写「According to Samuel Pepys' record」，其脚注却指向 James Malcolm《Londinium Redivivum》vol. 4（1807），即事发 141 年后的汇编。
  tag: ⚠️
  source: pepysdiary.com 全文检索结果（18 hits）＋ Wikipedia "Thomas Bloodworth" 及其脚注 [3]
  source_url: https://www.pepysdiary.com/search/?q=piss
  quote: "Searching for piss, in diary entries, ordered by relevancy. 18 found. — Tuesday 6 June 1665 / Saturday 9 April 1664 / Monday 12 October 1663 / Sunday 26 August 1666 / Friday 15 November 1667 / ... / Tuesday 18 September 1666 / ... / Wednesday 11 July 1666"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "Pepys日记原话,同时代记载,一手引语,史实确证的名言"

- fact_id: london1666.people.006
  claim: 剑桥大学图书馆特藏组的公开文章在引这句话时用的是「was said to have remarked」（据说曾说），并未指明出处——即学界公开写作中对这句话本身也持保留。
  tag: ⚠️
  source: Cambridge University Library Special Collections Blog, "The Great Fire of London"
  source_url: https://specialcollections-blog.lib.cam.ac.uk/?p=13020
  quote: "was said to have remarked on the night of 2nd September that 'a woman might piss it out'"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "确凿引语,有出处的原话,一手史料"

- fact_id: london1666.people.007
  claim: 「该拆房断火却没拆」这条对市长的实质指控，有《伦敦公报》官方通告作一手依据，措辞是「本该如此办而未办」。
  tag: ✅
  source: The London Gazette No. 85, "Whitehall, September 8" 1666
  source_url: https://www.fireoflondon.org.uk/assets/uploads/2016/08/Transcript_42.39_55.pdf
  quote: "care was not taken for the timely preventing the further diffusion of it, by pulling down Houses, as it ought to have have been so that this lamentable Fire in a short time became too bigg to be mastered by any Engines, or working near it"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "手持长柄火钩的市民站在巷口，看着火势蔓延却无人下令拆房"
  negative: "高压水枪,现代消防车,有组织的救火队,爆破拆除"

- fact_id: london1666.people.008
  claim: 国王 Charles II 的可考指令，由 Pepys 面奏后当场转达：不惜任何房屋，沿火头前方一律拆除。约克公爵 James 当场表示可以再拨士兵。
  tag: ✅
  source: The Diary of Samuel Pepys, 2 September 1666
  source_url: https://www.pepysdiary.com/diary/1666/09/02/
  quote: "the King commanded me to go to my Lord Mayor from him, and command him to spare no houses, but to pull down before the fire every way. The Duke of York bid me tell him that if he would have any more soldiers he shall"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "国王亲自救火,国王缺席,王室不闻不问"

- fact_id: london1666.people.009
  claim: 官方通告记载国王与约克公爵亲身连日奔走救火，约克公爵曾在圣殿区通宵督阵、用火药炸房断火；这是官方口径（有宣传成分，但行动本身有多方印证）。
  tag: ⚠️
  source: The London Gazette No. 85, "Whitehall, September 8" 1666
  source_url: https://www.fireoflondon.org.uk/assets/uploads/2016/08/Transcript_42.39_55.pdf
  quote: "His Royal Highness, who watched there that whole night in person, by the great labours and diligence used, and especially by their applying powder to blow up the Houses about it, before day most happily mastered it."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "王室逃离伦敦,袖手旁观,官方无作为"
```

> ⚠️ **对「真实人物只念有记载原话」这条铁律的直接后果**：
> **Bloodworth 在本片中不能说「A woman might piss it out」。**
> 他能说的只有 `people.004` 那段崩溃之词（有 Pepys 一手记录），
> 而且那是 **9 月 2 日正午**、不是 9 月 1 日夜里。
> 如果 sk3 一定要在「前一夜」见到市长，要么让他只做沉默的背景人物，
> 要么由旅行者以「明天你会说一句话，被人记一辈子」的方式**间接提及**这句传言，
> 并在片中或字幕里点明「这句话查无一手出处」——这反而是本站可以独有的一个诚实亮点。

### B. 典型虚构人物（阶层/职业有据，人是虚构的）

四位，每位都挂了真实史料的锚。

```yaml
- fact_id: london1666.people.010
  claim: 【虚构人物 1 · 泰晤士街货栈搬工】泰晤士街一线堆的是沥青、柏油、油、葡萄酒、白兰地——Pepys 亲眼所见并逐项点名。搬工的职业与货物均有一手依据。
  tag: ✅
  source: The Diary of Samuel Pepys, 2 September 1666
  source_url: https://www.pepysdiary.com/diary/1666/09/02/
  quote: "The houses, too, so very thick thereabouts, and full of matter for burning, as pitch and tarr, in Thames-street; and warehouses of oyle, and wines, and brandy, and other things."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "泰晤士街窄巷货栈门口，粗壮搬工肩扛沥青桶，地面被油渍浸黑，桶身渗出黑色柏油"
  negative: "叉车,托盘,集装箱,现代仓库,安全帽,反光背心"

- fact_id: london1666.people.011
  claim: 【虚构人物 2 · 比林斯盖特码头脚夫】比林斯盖特是鲜鱼咸鱼、贝类、柑橘、洋葱、水果、块根、小麦黑麦等谷物的集散港——Stow 的伊丽莎白时代伦敦志有明文，British History Online 转载。
  tag: ✅
  source: Stow, Survey of London，转引自 Old and New London, vol. 2（British History Online）
  source_url: https://www.british-history.ac.uk/old-new-london/vol2/pp41-60
  quote: "Stow (Elizabeth) describes Billingsgate as a port or harborough for ships and boats bringing fish, fresh and salt, shell-fish, oranges, onions, fruit, roots, wheat, rye, and other grain."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "清晨的比林斯盖特码头，木船靠岸，柳条筐里堆着鲜鱼与洋葱，脚夫赤脚踩在湿滑石阶上"
  negative: "现代渔港,冷藏车,塑料箱,起重机,机动船"

- fact_id: london1666.people.012
  claim: 【虚构人物 3 · 泰晤士河船夫】火起后河面全是驳船与小船抢运家什，居民从一处水边台阶攀爬到另一处——这套「河上求生」的动线由 Pepys 一手记下，船夫这个职业是那一夜真正的救命通道。
  tag: ✅
  source: The Diary of Samuel Pepys, 2 September 1666
  source_url: https://www.pepysdiary.com/diary/1666/09/02/
  quote: "Everybody endeavouring to remove their goods, and flinging into the river or bringing them into lighters that layoff; poor people staying in their houses as long as till the very fire touched them, and then running into boats, or clambering from one pair of stairs by the water-side to another."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "泰晤士河水边石阶，船夫撑着一条平底小船等客，船里已堆了别人家的箱笼"
  negative: "机动艇,救生衣,现代码头浮桥,游船"

- fact_id: london1666.people.013
  claim: 【虚构人物 4 · 圣保罗教堂旁的书商学徒】书商行会的存书被搬进大教堂地下的圣福音堂避难，结果随拱顶塌落全部烧毁、连烧一周。这位学徒的「盼头」＝那批他亲手码进地窖、以为万无一失的书。
  tag: ✅
  source: The Diary of John Evelyn（废墟勘察条，Project Gutenberg #42081 Vol. II）
  source_url: https://www.gutenberg.org/files/42081/42081-h/42081-h.htm
  quote: "The ruins of the vaulted roof falling, broke into St. Faith's, which being filled with the magazines of books belonging to the Stationers, and carried thither for safety, they were all consumed, burning for a week following."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "大教堂地下石砌拱顶地窖，成捆未装订的书页与印张一直码到拱顶，一名少年学徒举着烛台在书堆间穿行"
  negative: "现代图书馆书架,精装书,电灯,防火门,灭火器"
```

#### 四位虚构人物的「盼头」（Titanic 型对话的等价物）

本站要的那句「问乘客到了美国要做什么」，四个等价问法：

| # | 人物 | 阶层锚点 | 今晚在做什么 | **他的盼头**（问出来的那句） |
|---|---|---|---|---|
| 1 | 泰晤士街货栈搬工 | `people.010` 沥青/柏油/油/酒货栈 | 赶在主日前把最后几桶柏油归位 | 「攒够钱盘下半间货栈，不再替人扛桶。」——他不知道明天这条街上的油与白兰地会把火推成不可扑灭的规模 |
| 2 | 比林斯盖特码头脚夫 | `people.011` Stow 所记货种 | 卸完最后一船咸鱼，等着明早的主日集 | 「明天卖完这船，给闺女扯块新布做主日衣裳。」——明天她的主日在逃命里过 |
| 3 | 泰晤士河船夫 | `people.012` 河上撤离动线 | 收工，把船拴在水边台阶上 | 「等这阵子过去，换一条更大的船。」——他确实会在明天赚到一生最多的一笔钱，而那是从邻居的绝望里赚的 |
| 4 | 圣保罗旁的书商学徒 | `people.013` Stationers 存书入圣福音堂 | 帮师傅把新到的印张码进店里 | 「满师以后自己开一间铺子，先印我自己想印的那一本。」——他师傅的全部存货九天后会在圣福音堂地窖烧一个星期 |

> 写作提示：**前三位的盼头都要「明天/下周」这种短期尺度**，才能和 7 小时后的起火形成落差；
> 第四位的盼头用「满师以后」这种长期尺度，用来托底整集的余味。
> 四位都**不要**让旅行者剧透——Titanic 那条之所以动人，正在于问的人知道、被问的人不知道，
> 而镜头只拍被问者的脸。

---

## §0 待人工抽查清单（最该由用户回看原文页的 5 条）

| # | fact_id | 为什么必须人工看 |
|---|---|---|
| 1 | `london1666.people.005` | **本轮最关键的一条。** 我用 pepysdiary.com 的全日记检索证明「A woman might piss it out」不在 Pepys 日记里（18 条 "piss" 命中无一在 1666-09-02）。但该站底本是 Wheatley 1893 年版，**该版对秽语确有删节**，站方仅以 `[… — L&M]` 方括号补入部分 Latham & Matthews 复原文字。理论上存在「这句被 Wheatley 删了、站方也没补」的可能。**要彻底定论，须查 Latham & Matthews 版《Pepys 日记》第 7 卷（1666）9 月 2 日条原文。** 另需核 Malcolm《Londinium Redivivum》vol. 4（1807）pp. 73–74 究竟写了什么——我抓到的三份 archive.org 扫描件 OCR 全部损坏（vol. 4 全文连 "woman" 都检索不到），无法自证。 |
| 2 | `london1666.coord.002` | 儒略/格里高利 10 天差是**我按规则推的**，不是哪一页原文直接为 1666 年写死的。我实际读到的诺丁汉大学页只说「10 或 11 天」，Wikipedia 换算表最近一行是 1500 年。结论本身是史学通识，但按「不替史料做裁决」的要求必须请用户确认一次。 |
| 3 | `london1666.timeline.004` / `.006` / `people.007` / `.009` | 这四条都引自**同一份转录 PDF**（fireoflondon.org.uk 的 Rege Sincera 1667 转录本）。`thegazette.co.uk` 官方站的 issue 85 PDF 是**纯扫描图无文字层**，我无法交叉核对逐字。转录件里已能看到明显手误（"as it ought to have have been"、"disraction"），说明是人工转录。**建议用户比对一次官方扫描件图像。** |
| 4 | `london1666.timeline.003` | Farriner 9 月 1 日晚八九点打烊、Hanna 午夜巡查——**这是本站「前一夜」的核心场景**，却是全份 dossier 里 tier 最低的一条（T2，Tinniswood 的叙事性复原，Penguin 节选未标注他据何史料）。既然整集就架在这个时刻上，值得回溯到 Tinniswood《By Permission of Heaven》正文看注释。 |
| 5 | `london1666.timeline.011` | Evelyn 记「about ten」vs 官方记「凌晨一点」——**11 小时的一手史料冲突**。我按要求如实并列、未做裁决。用户需决定成片怎么处理：采官方 1 点、或把这处分歧本身做成一个内容点（本站是史料驱动 vlog，展示「两个目击者记的时间差了 11 小时」恰好是好素材）。 |

---

## 附：本轮抓取失败 / 受限的来源（供后续 worker 避坑）

- `pepysdiary.com` → WebFetch 一律 **403**；用 `curl -A "<Chrome UA>"` 正常 200。
- `theconversation.com` → curl **SSL error 35**；WebFetch 正常。
- `thegazette.co.uk/London/issue/85/data.pdf` → 200 但**纯扫描图，无文字层**。
- Project Gutenberg / 转录 PDF → WebFetch 以版权为由**拒绝逐字复现**；
  须 `curl` 下载后本地 `pdftotext` / 正则抽取（公有领域文本，合规）。
- archive.org 的 Malcolm《Londinium Redivivum》三份扫描件（`londiniumrediviv00malc`、
  `b33519560_0004`、`10225284bsb`）**OCR 全部不可用**（长 s 与版面噪声）。
