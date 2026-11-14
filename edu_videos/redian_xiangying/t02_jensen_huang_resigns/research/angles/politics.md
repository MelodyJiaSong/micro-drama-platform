# 角度：politics（两党各自的表态与动作）

- **检索日期**：2026-11-14（片中一律写「截至 2026-11-14」）
- **任务**：用户定的本期角度「这件事背后是美国两党之间的斗争，黄仁勋是被牺牲的对象；大背景是中美科技竞争」。本文件只整理**两党与白宫各自公开说了什么、做了什么**，按时间排列；是否支持该假设的判断写在 `sacrifice_test.md`。
- **检索范围**：参院银行委员会少数党新闻室（一手）、众院对华特设委员会新闻稿（一手）、CNBC 11-12 直播（逐条转录议员发言）、Axios、AFP（经 EWN）、NYT（经 Honolulu Star-Advertiser 转载）、Reuters（经 Korea Times）、The Register、Foreign Policy、RedState、The Bulwark、Responsible Statecraft、FDD（Washington Post 原刊）、环球网、HK01、虎嗅。
- **检索词（简列）**：2026 midterm results；Axios Lutnick stalled Megaspeed Bessent；Wyden Neal letter Lutnick；Moolenaar H200 December 2025；GAIN AI Act Banks NDAA；AI Overwatch Act Mast vote；Trump urged Huang fight；Bannon Loomer Huang；Cramer Huang resign；Sacks Huang；Rubio memo；Kudlow resign now。
- **限制**：Politico、Axios、Gizmodo、FourWeekMBA 原文 403 或拒绝抓取，相关条目经转载或检索摘要转述，已注明。NYT 原文付费墙，经转载读到。Truth Social 原帖未直接读取。WebSearch 摘要模型多次误称「找不到辞职报道」，那是检索工具的问题，不影响本档案已核的一手材料（8-K 等）。
- **党派标注**：R = 共和党，D = 民主党。

---

## 0. 先看这张表：谁在推，谁在挡

| 方面 | 2025–2026 对华芯片出口的立场 | 丑闻后对黄仁勋的态度 | 依据 |
|---|---|---|---|
| 特朗普本人（R，总统） | **放**：H20 换 15% 分成（2025-08）、H200 换 25%（2025-12） | **力挺**：「very honorable man」；据 NYT 曾致电劝他争取留任（转述）；辞职后称「what a horrible thing」并推荐 Tim Cook | 见 §1、§3 |
| 白宫顾问 Sacks、商务部长 Lutnick | **放**：Sacks 劝参院共和党删 GAIN AI 法案；据 Axios，Lutnick 多次拖延对转运公司的打击 | 白宫只公开力挺 Lutnick（「complete confidence」），没有就黄仁勋去留表态 | §1、§3 |
| 国会共和党对华鹰派（Moolenaar、Mast、Crawford、Banks、Tim Scott、Cramer） | **收**：反对 H200 出口、推 AI Overwatch Act、GAIN AI Act | **最早、最响的施压者**：三位众院主席请他简报；Tim Scott 要求公开作证、可发传票；**Cramer 公开要他下台**；Moolenaar 把离任称为「firing」 | §2、§3 |
| 国会民主党（Warren、Schumer、Wyden、Coons、Meeks、Jeffries、Himes） | **收**：反对 H200 出口，同样支持 GAIN AI、AI Overwatch | 主攻**特朗普和 Lutnick**（「特朗普知道却不管」）；Jeffries 称辞职「the right thing to do」；**Himes 反而质疑「间谍」定性** | §2、§3 |

一句话：**在对华芯片问题上，分界线不是两党之间，而是「国会两党」对「白宫＋英伟达」。**丑闻出来以后，两党都在施压，但施压的对象和目的不同——民主党的主要靶子是特朗普政府，共和党鹰派的主要靶子是出口政策和英伟达。

---

## 1. 背景：黄仁勋与特朗普政府（2025-04 至 2026-10）

| 日期 | 事件 | 原话 / 要点 | 出处 | 性质 |
|---|---|---|---|---|
| 2025-04 | 黄仁勋出席海湖庄园晚宴；之后政府放弃了限制部分英伟达对华芯片的计划 | 「Huang attended a dinner at Trump's Mar-a-Lago club in April 2025」（摘要转述） | Reuters 经 Korea Times 2026-11-10 https://www.koreatimes.co.kr/world/20261110/trumps-close-ties-to-nvidias-huang-scrutinized-after-foreign-intelligence-concerns | 报道称 |
| 2025-07-15 | 黄仁勋在北京宣布 H20 获美方出口许可 | 「美国政府已经批准了我们的出口许可，可以开始发货了」 | 环球时报 经环球网 https://world.huanqiu.com/article/4NVgbHwiLSI | 已证实（引语） |
| 2025-08-11 | 特朗普在白宫记者会讲 H20 交易：他先要 20%，黄仁勋还价到 15% | 「And I said if I'm going to do that, I want you to pay us as a country something, because I'm giving you a release」 | NPR 经 Ideastream https://www.ideastream.org/2025-08-11/trump-says-nvidia-will-hand-the-u-s-15-of-its-h20-chip-sales-to-china | 已证实（引语）；「20% 还价到 15%」为转述 |
| 2025-10 | 特朗普授予黄仁勋国家科学奖章，同日披露夏季买入至多 160 万美元、卖出至多 100 万美元英伟达股票 | 白宫发言人 Davis Ingle：第三方机构独立管理总统资产（转述） | Korea Times（Reuters） | 报道称 |
| 2025-11-19 | Axios：白宫出手阻止限制芯片出口的 GAIN AI 法案 | 标题「White House moves to block bill restricting AI chip exports」 | https://www.axios.com/2025/11/19/white-house-block-bill-restricting-ai-chip-exports （未读原文） | 报道称 |
| 2025-12-06 | 最终版 NDAA 删除 GAIN AI 条款（参院版 10-10 以 77:20 通过时含该条） | 黄仁勋称结果「wise」（转述） | Nextgov 2025-12 https://www.nextgov.com/policy/2025/12/bill-prioritizing-american-customers-for-ai-chips-not-expected-make-it-final-ndaa-sources-say/409920/ ；检索摘要 | 已证实（立法结果）；黄仁勋原话待核 |
| 2025-12-08 | 特朗普宣布允许英伟达向中国「approved customers」出售 H200，美方收 25% | 环球网：「特朗普表示，美方将从相关芯片出口中收取 25% 的分成」 | 环球网 https://world.huanqiu.com/article/4PT6kkiRAKT | 已证实（宣布）；**10-K 把 25% 写成「进口进美国时的关税」**，不是分成，见 `us_china.md` |
| 2025-12 | 英伟达承诺向白宫宴会厅项目出资 2,500 万美元 | 「Nvidia committed $25 million toward Trump's planned White House ballroom, according to media reports」 | Korea Times（Reuters） | 报道称 |
| 2026-03-26 | Sacks 卸任 AI 与加密沙皇，转任总统科技顾问委员会（PCAST）联席主席；黄仁勋是 PCAST 成员 | — | Daily Signal https://www.dailysignal.com/2026/03/26/david-sacks-out-as-ai-and-crypto-czar-takes-on-new-role/ | 报道称 |
| 2026-05（春） | 国务卿 Rubio 主持起草一份机密备忘录，提醒少数高层官员黄仁勋与黄乐的关系；黄仁勋起初不在访华名单上，特朗普临时邀他在阿拉斯加加油时登机；Rubio 在空军一号上向特朗普当面讲过 | 美方官员：Rubio「briefed the president on the issue」；特朗普：「No, I didn't hear about it then.」「didn't make much of an impact on me」 | NYT 2026-11-10，经 Honolulu Star-Advertiser 转载 https://www.staradvertiser.com/2026/11/11/breaking-news/trump-knew-of-nvidia-ceos-suspected-spy-ties-before-beijing-visit/ | 备忘录：报道称（匿名）；特朗普原话：已证实（NYT 转载） |
| 2026-05-13 | 黄仁勋随特朗普抵达北京（白宫官方照片） | — | media.md D1 | 已证实 |
| 2026-09 | 黄仁勋出席白宫为习近平举行的国宴（Reuters 转述）；All-In 峰会上特朗普来电，黄仁勋开免提 | — | Korea Times；TechRepublic https://www.techrepublic.com/article/news-trump-jensen-huang-ai-safety-data-centers/ | 报道称 |

**我们的判断（只描述关系，不推断动机）**：截至丑闻爆发，黄仁勋在公开记录里是**和特朗普政府走得最近的科技 CEO 之一**，也是放宽对华芯片出口的主要游说者。这让他在华盛顿的政治版图里站在「白宫一边」，而不是「某一党一边」。

---

## 2. 国会两党此前的动作：对华芯片是两党共识

| 日期 | 谁（党派） | 动作 / 原话 | 出处 | 性质 |
|---|---|---|---|---|
| 2025-10-10 | 参院（Banks R 牵头、Warren D 联合牵头） | GAIN AI 法案作为 NDAA 修正案随参院版 77:20 通过 | Washington Technology https://www.washingtontechnology.com/companies/2025/10/ai-export-control-bill-passes-senate-ndaa-amendment/408798/ | 已证实（检索摘要，原文未逐字读） |
| 2025-12-03 | Warren（D，参院银行委员会首席少数党议员） | 「He's now sneaking in to meet with Senate Republicans behind closed doors.」「Mr. Huang should be brought in to testify publicly and under oath.」 | 参院银行委员会少数党新闻室（一手） https://www.banking.senate.gov/newsroom/minority/warren-criticizes-nvidia-ceos-closed-door-meeting-on-capitol-hill-presses-administration-not-to-greenlight-sale-of-h200-ai-chips-to-china | 已证实 |
| 2025-12-12 | Warren、Schumer、Wyden、Andy Kim、Bennet、Kaine、Slotkin（全为 D）致信 Lutnick | 「The President's dangerous decision to give away critical national security controls」；把决定归于「personal lobbying by NVIDIA's CEO Jensen Huang」「a donation to the Trump ballroom」 | 同上新闻室（一手） https://www.banking.senate.gov/newsroom/minority/warren-schumer-colleagues-press-lutnick-on-administrations-decision-to-sell-out-us-national-and-economic-security-by-greenlighting-the-sale-of-h200-chips-to-china | 已证实（引语）；「捐款换政策」是信中的指控 |
| 2025-12（约 12-11/12） | Moolenaar（R，众院对华特设委员会主席）致信 Lutnick，要求 1-15 前简报 H200 决定依据 | 「Approving the sale of cutting-edge chips to Chinese companies risks undercutting the extraordinary strategic advantage that President Trump achieved in his first term.」 | Reuters 经 The Standard https://www.thestandard.com.hk/china/article/319233/US-lawmaker-demands-details-on-Trumps-decision-to-sell-Nvidia-H200-chips-to-China | 已证实（引语经 Reuters） |
| 2025-12 | Mast（R，众院外委会主席）提出 AI Overwatch Act（H.R. 6875）：国会 30 天内可否决对敌对国的芯片出口许可 | — | Al Jazeera https://www.aljazeera.com/economy/2026/1/21/us-house-panel-advances-bill-to-give-congress-authority-on-ai-chip-exports | 已证实 |
| 2026-01-21 | 众院外委会「overwhelmingly」通过 AI Overwatch Act；民主党首席议员 Meeks 支持；**只有两名共和党人（McCormick、Barr）反对，Issa 弃权**；新版含两年禁售 Blackwell | Mast：「My job is not to be a yes-man to David Sacks or for [Nvidia CEO] Jensen Huang.」；Sacks 转发「never Trumpers」策划该法案的帖子并写「Correct」 | Axios https://www.axios.com/2026/01/21/bill-chip-sales-china-advances （检索摘要）；The Register https://www.theregister.com/2026/01/21/house_gop_ai_chip_exports_trump_china_nvidia/ ；Daily Caller 经检索摘要 | 已证实（投票结果）；Mast 原话经 Daily Caller 转述 |
| 2026-01 | Laura Loomer（MAGA 活动人士）称 AI Overwatch Act 是「pro-China sabotage disguised as oversight」（转述） | — | Daily Caller / BizPac Review https://www.bizpacreview.com/2026/01/20/right-wing-influencers-caught-flooding-social-media-with-near-identical-posts-on-obscure-bill-hated-by-tech-giant-1616961/ | 报道称 |
| 2025-09/10 | Bannon（前白宫首席策略师）称黄仁勋是「中国影响力代理人」（中文转述，英文原话未找到） | — | unwire.hk 2025-10-01 https://unwire.hk/2025/10/01/huang-china-agent-controversy/ai | 报道称（转述） |
| 2026-03-24 | **Banks（R）与 Warren（D）联名**要求 Lutnick 暂停或复审英伟达对华及东南亚出口许可（起因：Super Micro 相关人员被控转运） | 「can no longer base licensing decisions on assurances from executives who have a financial stake in the outcome」 | 参院银行委员会少数党新闻室（一手） https://www.banking.senate.gov/newsroom/minority/senators-banks-and-warren-urge-commerce-secretary-lutnick-to-suspend-or-reconsider-nvidia-export-licenses-amid-supermicro-chip-diversion-indictment | 已证实 |
| 2026-05-05 | Coons（D）致信 Lutnick：Lutnick 在听证会说没有 H200 出口到中国，与黄仁勋 3-17 对记者说已获中美两国批准相矛盾 | — | Coons 办公室 https://www.coons.senate.gov/?p=23613 （检索摘要） | 报道称 |

**小结**：2025-12 之后，国会里反对对华卖 H200 的有共和党主席（Moolenaar、Mast、Banks），也有民主党领袖（Schumer、Warren）。真正替英伟达说话的是白宫（Sacks）和 MAGA 网红（Loomer），而 MAGA 内部也有 Bannon 这样的反对者。**分歧主要在共和党内部（国会鹰派 vs 白宫产业派），不在两党之间。**

---

## 3. 丑闻期间（2026-10-29 至 11-13）：按时间排

| 日期 | 谁（党派 / 职务） | 原话 / 动作 | 出处 | 性质 |
|---|---|---|---|---|
| 10-29 | NYT（Swan、Haberman 等，us/politics 栏目） | 首报；称特朗普约一年前被简报过、未采取行动 | NYT（付费墙）；转述见 timeline.md | 报道称（匿名） |
| **11-03** | **中期选举**：民主党同时拿下参众两院（新国会 2027-01-03 就职） | — | Al Jazeera https://aljazeera.com/news/2026/11/4/democratic-party-flips-us-senate-in-2026-midterm-elections ；https://www.aljazeera.com/news/2026/11/4/democratic-party-gains-us-house-majority-in-2026-midterm-elections | 已证实（多家媒体报道；最终席位数各家不一） |
| 11-04/05 | Mast、Moolenaar、Crawford（三人均 R） | 请黄仁勋 11-18 参加「a joint, closed-door briefing」 | 委员会新闻稿（一手，见 media.md C1） | 已证实 |
| 11-07 | Coons（D） | 「I'm pushing to investigate Jensen Huang and Nvidia to determine whether our national security was compromised.」 | Reuters 经 Korea Times | 已证实（引语经 Reuters） |
| 11-08 | 特朗普 | 称黄仁勋「honorable guy」；「He's done such an incredible job.」；「I hope everything's fine.」 | Korea Times（Reuters） | 已证实（引语） |
| 11-09 | 特朗普（白宫） | 「I just think he's a very honorable man.」；转述黄仁勋称不知道她是间谍；说不会向习近平提此事 | NYT 经 Star-Advertiser；AP（timeline.md） | 已证实 |
| 11-10 | Cramer（R-ND，参院银行委员会资深成员） | 「The potential for extortion is so tremendous that something as sensitive as Nvidia chips, I just think he's got to go」（对 Politico） | Reuters 经 WSAU 等转载 https://wsau.com/?p=1034404 ；247wallst https://247wallst.com/investing/2026/11/11/a-republican-senator-just-told-jensen-huang-to-step-down/ （均为检索摘要） | 已证实（引语经 Reuters 转述 Politico；Politico 原文 403） |
| 11-10 | NYT | Rubio 备忘录与空军一号简报 | Star-Advertiser 转载 | 报道称（匿名） |
| 11-10 | Axios | Lutnick 曾收到关于黄仁勋关系的机密备忘录 | https://axios.com/2026/11/10/lutnick-nvidia-jensen-huang-china-memo （403，检索摘要） | 报道称（匿名） |
| 11-10 | Singleton（FDD，WaPo 评论） | 副标题「They should work together to prevent China from winning the AI race.」 | https://www.fdd.org/analysis/the-huang-honey-trap-scandal-sends-a-message-about-chip-export-controls/ | 观点 |
| 11-11 | Kudlow（特朗普首任国家经济委员会主任，Fox Business 主持人） | 各家措辞不一：「Mr. Huang, resign now」/「Step down, Mr. Huang, right now」 | 检索摘要（Business Insider 等）；原视频未看 | 报道称（措辞待核） |
| 11-11 | Axios（匿名高层信源） | Lutnick 拖延特朗普批准的打击转运行动；Bessent 在战情室追问为何不把 Megaspeed 列入实体清单，Lutnick 称会「start a trade war with China」；商务部发言人否认 Bessent 当面质问 | Axios 经 GV Wire https://gvwire.com/2026/11/11/lutnick-stalled-trump-crackdown-on-diversion-of-nvidia-chips-to-china-axios-reports/ （检索摘要） | 报道称（匿名，部分被否认） |
| 11-11 | AFP 采访的分析人士 | CSIS 的 Mehta：鹰派「really wanted to see a more aggressive approach around export controls to China」「They will now see some fruits of their efforts.」；Brookings 的 Kyle Chan：共和党人过去怕得罪特朗普，现在特朗普不再被视为不可战胜 | AFP 经 EWN https://www.ewn.co.za/2026/11/11/nvidia-ceo-affair-revives-push-for-tougher-us-line-on-china | 观点（引语已证实） |
| 11-11 | Himes（D，众院情报委员会首席少数党议员） | 简报后怀疑「间谍」定性；问 FBI 反情报调查是否启动，「they didn't know」 | Politico（403，转述，见 allegations.md） | 报道称 |
| 11-12 09:26 | Greer（美国贸易代表） | 「the crown jewels to remain in U.S. hands or in the hands of our allies」 | CNBC 直播 https://www.cnbc.com/2026/11/12/nvidia-jensen-huang-ceo-live-updates.html | 已证实（经 CNBC） |
| 11-12 09:58 | Warren（D；CNBC 称其为下届银行委员会主席） | 「The American people cannot rely on Big Tech billionaire CEOs to put our national security above their bottom line.」；呼吁通过 AI Overwatch Act（Mast 的法案） | CNBC 直播 | 已证实（经 CNBC） |
| 11-12 10:18 | 白宫（官方声明） | 「President Trump maintains complete confidence in the secretary.」（指 Lutnick） | CNBC 直播 | 已证实（经 CNBC） |
| 11-12 10:35 | 特朗普（Truth Social） | 推荐 Tim Cook：「A Legend replaces a Legend!」 | CNBC 直播 | 已证实（经 CNBC） |
| 11-12 11:06–11:19 | Mast（R） | 仍信任 Lutnick，要查 BIS：「The people that we deal with in BIS, those are the ones that are at the granular level of dealing with Nvidia and chips.」；「He has agreed to come.」 | CNBC 直播 | 已证实（经 CNBC） |
| 11-12 11:08 | Thune（R，参院多数党领袖；选后将任少数党领袖） | 「I would expect there would be some follow-up, yeah.」 | CNBC 直播 | 已证实（经 CNBC） |
| 11-12 11:36 | Jeffries（D，众院少数党领袖，预计 2027 任议长） | 「We need a classified briefing made available to members of Congress.」；称辞职是「the right thing to do」 | CNBC 直播 | 已证实（经 CNBC；后半句为 CNBC 转述） |
| 11-12 12:04 | Wyden（D）、Neal（D）致信 Lutnick | 特朗普政府「did not appear to acknowledge this evident national security threat」；对向涉华公司批出口展开调查 | CNBC 直播；business.md | 已证实（经 CNBC） |
| 11-12 12:18 | Schumer（D，参院少数党领袖） | 「Congress must demand answers from Mr. Huang and others at Nvidia.」；追问官员是否因特朗普与黄仁勋的关系被叫停调查 | CNBC 直播 | 已证实（前句）；后半为 CNBC 转述 |
| 11-12 12:19 | Meeks（D，众院外委会首席少数党议员） | 「All the reports say that Trump knew what took place and just basically made it like it was no big deal.」 | CNBC 直播 | 已证实（经 CNBC） |
| 11-12 13:41 | Huizenga（R，众院金融服务委员会副主席） | 商务部「They have not been as cooperative as they should be.」 | CNBC 直播 | 已证实（经 CNBC） |
| 11-12 15:35 | 特朗普（Hugh Hewitt 访谈） | 「But what a horrible thing that is! That's so sad to see that happen.」 | CNBC 直播 | 已证实（经 CNBC） |
| 11-12 20:22 | NYT（经 CNBC 转述） | 特朗普周二（11-10）致电黄仁勋，劝他为保住职位而争取 | CNBC 直播（非直接引语） | 报道称（未见 NYT 原文） |
| 11-12 | Moolenaar（R） | 「Jensen Huang's firing from the company he founded is an unfortunate end that could have been avoided.」；「Nvidia must now change its corporate practices and appoint leadership that makes national security its top priority.」；「In Congress we must act quickly to pass bipartisan export control legislation in the year-end national defense bill.」 | 委员会新闻稿（一手） https://chinaselectcommittee.house.gov/media/press-releases/moolenaar-statement-on-jensen-huang-s-resignation-from-nvidia | 已证实 |
| 11-12 | Tim Scott（R，参院银行委员会主席） | 「The American people deserve answers.」；要求黄仁勋 12-03、Lutnick 12-10 公开作证，必要时发传票 | CNBC 直播 | 已证实（经 CNBC） |

### 3.1 党派媒体怎么框

| 媒体（倾向） | 框架 | 出处 |
|---|---|---|
| The Bulwark（反特朗普保守派） | 「Trump was briefed about the relationship, his administration failed to intervene.」标题「Trump's Favorite Tech CEO Caught in Chinese Spy Sex Scandal」 | https://www.thebulwark.com/p/trumps-favorite-tech-ceo-caught-in |
| Daily Beast（偏左） | 标题「Trump's billionaire pal Jensen Huang targeted in mystery woman spy plot」 | https://www.thedailybeast.com/trumps-billionaire-pal-jensen-huang-targeted-in-mystery-woman-spy-plot |
| RedState（亲特朗普） | 称 NYT 空军一号报道「an attempt at constructing a narrative shifting blame to Trump」「really a nothingburger」；但认为 Megaspeed 转运是需要彻查的真问题 | https://redstate.com/jenvanlaar/2026/11/10/trump-air-force-one-briefing-on-jensen-huang-and-chinese-honeypot-n2209253 |
| Responsible Statecraft（克制派） | 批评硅谷风投为黄仁勋护短；称「tech-China hawk」联盟分裂，鹰派趁势要求暂停对华出货 | https://responsiblestatecraft.org/jensen-huang-china-spy/ |

**我们的判断**：偏左与反特朗普媒体把黄仁勋当作「特朗普的朋友」来写，**火力对准的是特朗普**；亲特朗普媒体反击的也是「甩锅给特朗普」，**而不是替黄仁勋喊冤**。没有一方把黄仁勋本人当作要保护的「自己人」，除了特朗普本人和硅谷投资人。

---

## 4. 小结：两党在对华芯片问题上是分歧还是共识

1. **政策层面是共识**：H200 对华销售被两党国会领袖同时反对（Moolenaar R、Mast R、Banks R vs Schumer D、Warren D）；AI Overwatch Act 在众院外委会两党压倒性通过（R 主席提、D 首席议员支持）；Banks（R）＋Warren（D）联名要求暂停许可。Moolenaar 在黄仁勋辞职当天呼吁「bipartisan export control legislation」。
2. **真正的裂缝在共和党内部**：国会鹰派 vs 白宫（特朗普、Sacks、Lutnick）＋ MAGA 网红（Loomer）。Sacks 把 AI Overwatch Act 说成「never Trumpers」的动作，说明这场争论在共和党内被当作「忠诚问题」。
3. **两党的分歧在「追责对象」**：民主党把丑闻当作**特朗普与 Lutnick 失职**的证据（Wyden/Neal、Schumer、Meeks），并将从 2027 年起掌握两院委员会；共和党鹰派也追查商务部和 BIS（Mast、Huizenga、Tim Scott），但不点名特朗普，并且**公开要黄仁勋走的是共和党人**（Cramer）和特朗普前幕僚（Kudlow）。
4. **特朗普是站在黄仁勋一边的**：截至 11-13 的公开记录里，他从头到尾为黄仁勋说话（11-08、11-09、据报 11-10 来电、11-12「horrible thing」）。
