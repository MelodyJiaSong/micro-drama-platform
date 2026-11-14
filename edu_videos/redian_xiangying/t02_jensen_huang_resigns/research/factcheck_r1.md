# 事实核查 R1：t02 黄仁勋辞任英伟达 CEO

- 核查人：独立上下文事实核查（未参与档案写作）；核查日期 2026-11-14。
- 对象：`research/dossier.md`（重点 §8）、`claims.json`（C01–C112）、`research/angles/politics.md`、`us_china.md`、`sacrifice_test.md`。
- 方法：优先用 WebFetch 打开台账给出的 source 逐字核对；WebSearch 用 19 次（上限 20）。未调用任何收费服务，未下载图片视频（WebFetch 自动缓存的起诉状 PDF 只在本地抽取文本核对）。未改 `claims.json` 与 `dossier.md`。
- 判定：**通过**＝原文、数字、日期、归属与 status 都对得上；**需改**＝内容有误、措辞不逐字、来源对不上或 status 不当；**未能核**＝原文打不开或检索不到，片中不能按现有写法用；**删除**＝建议不进讲稿；**未复核**＝不在本轮优先范围，本轮未查。
- WebFetch 的摘要模型偶尔会转述，下文凡写「逐字一致」的，都是让它逐串比对过（是 / 否）的结果；直弯引号差异不计。

---

## 一、总结论

1. **主线「中美科技战让一个 CEO 的私事变成了国家安全问题」站得住。** 一手材料直接把两件事连在一起：董事会 11-08 声明的调查起因就是报道称他是「a foreign intelligence effort」的目标；众院三位主席 11-05 请他简报；Moolenaar 11-12 呼吁在 NDAA 里加「bipartisan export control legislation」；外交部毛宁 11-12 说「为实施科技封锁寻找借口」，这几处原文都逐字核到了。限定只有一条：辞职的直接原因公司没有写（8-K 与新闻稿核实无原因），而董事会接受辞职那天（11-11）的新消息是公司治理方面的（第二段关系报道）。所以主线只能说「私事变成了国家安全问题」，**不能说「国家安全问题让他下台」**。
2. **第二层「国会两党都要收紧、只有白宫在放；两党都拿他打自己的仗」方向对，但现有措辞有两处不准，必须改。**
   - 「只有白宫在放」说过头了。众院外委会 42:2:1 通过 AI Overwatch Act，反对票确实来自两名共和党人；但 GAIN AI 条款是在白宫施压下从最终版 NDAA 里删掉的，删除需要国会共和党领导层同意（多家报道称白宫直接找过多数党领袖 Scalise）。AI Overwatch 至今没有上全院表决。截至 11-14，国会**没有通过任何有约束力的收紧措施**。白宫内部也不是只有一种声音：据 NYT 匿名信源，提醒高层的备忘录由 Rubio 主持起草；据 Axios，经 Reuters 转述，特朗普今年第三次批准打击转运，在战情室追问 Lutnick 的是财长 Bessent。
   - 「民主党借他打特朗普和商务部，共和党鹰派借他推出口管制法案」这个两分法不干净。11-12 当天，民主党的 Warren 同样呼吁通过 AI Overwatch Act（Mast 的法案）；共和党的 Tim Scott（要 Lutnick 12-10 作证）、Huizenga（批评商务部不配合）、Mast（要查 BIS）同样在追商务部。真正分得开的只有一条：**民主党点名特朗普本人，共和党不点**。另外，11-11 前唯一有记录公开要他下台的议员是共和党人 Cramer。
3. **「两党斗争的牺牲品」作为中文舆论的说法可以引，但台账里那句胡锡进「原话」不是原话。** HK01 是转述，原文没有引号；同一家媒体前一天（11-09）的转述是胡锡进说「这是民主党和美国建制派搞黄仁勋、并进而搞特朗普的一种方式」。这是**指向民主党的**说法，不是对称的「两党恶斗」。如果片中把它讲成中立的「两党恶斗」，等于替评论人改了立场。
4. 档案用来反驳「牺牲品」说法的几块关键证据，有三块本轮**没核到原文**：Himes 质疑间谍定性（Politico 拒绝抓取，检索也搜不到）、CNN「over-torqued」、Blanche「no conclusions」。三者都只经 Wikipedia 转述，而且 Blanche 的头衔（司法部长还是代理司法部长）也没核实。另有一处用错：Moolenaar 的「firing」是辞职公告当天发的事后声明，不是要他下台的施压，被档案拿来证明「公开要他下台的是共和党人」，属于误用。
5. **第二位当事人**：本系列的所有文件（`edu_videos/redian_xiangying/` 全目录）都没有写她的姓名。但台账 C29 的 source（The Nightly 转载 NYT）**点了她的名字和职务**，CNBC「second-affair」那篇大概率也点了。这些页面不能截图上片，片中也不能提她的职务或业务线。

---

## 二、逐条表

### 2.1 论点直接用到的 C01–C79

| id | 判定 | 原文或更正 | 依据 URL |
|---|---|---|---|
| C01 | 通过 | 8-K：11-11 董事会 "accepted the resignation of Jen-Hsun Huang"，立即生效；签署日 11-12 | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000082/nvda-20261111.htm |
| C02 | 通过 | Kress "age 59"，2013 年起任 EVP 兼 CFO，兼任临时 CEO | 同上 |
| C03 | 通过（小注） | 新闻稿副标题 "Harvey C. Jones Appointed First-Ever Chair of the Board" 逐字；「73 岁、1993 年起任董事」出自 8-K，不在新闻稿里，note 应注明出处为 8-K | 8-K；https://www.sec.gov/Archives/edgar/data/1045810/000104581026000082/nvidiaannouncesceotransiti.htm |
| C04 | 通过 | 逐字一致 | Exhibit 99.1 |
| C05 | 通过 | 逐字一致 | Exhibit 99.1 |
| C06 | 通过（尾部待复核） | 核到 "together with our leadership team, I am committed to building on the extraordinary foundation Jensen created"；"over the last 33 years" 这半句不在本轮的摘录里，引用前对一次全文 | Exhibit 99.1 |
| C07 | 通过 | 8-K 与新闻稿都没有写原因 | 8-K；Exhibit 99.1 |
| C08 | 通过 | "Tuesday, November 17" 一致 | Exhibit 99.1 |
| C09 | 未复核 | — | — |
| C10 | 通过（加注） | 起诉状页眉 "Case 5:26-cv-13448 Document 1 Filed 11/09/26"，原告 Mark Kistenmacher，被告 NVIDIA 与 Jen-Hsun Huang，类别期逐字一致。**加注**：起诉状点名 Alice Huang，并转述 NYT，称她 "suspected Chinese spy"；这是原告的单方指控，片中如果出起诉状截图，这些段落要遮掉 | https://www.dandodiary.com/wp-content/uploads/sites/893/2026/11/Nvidia-Complaint.pdf |
| C11 | 通过 | 起诉状第 34 段 "fell $7.97 per share, or 4.27%, to close at $178.67 on November 9, 2026"；Yahoo 日线一致 | 起诉状；Yahoo chart |
| C12 | 通过 | 11-12 O 151.01 / H 167.14 / L 148.80 / C 166.19，前收 173.73；算得 -4.34% 和盘中 -14.35% | https://query1.finance.yahoo.com/v8/finance/chart/NVDA?range=3mo&interval=1d |
| C13 | 通过（算术） | 7.54 × 241 亿 ≈ 1,817 亿美元 | 同上；SEC XBRL |
| C14 | 未复核（SOX） | NVDA 部分一致；SOX 本轮未复算 | — |
| C15 | 部分通过 | NVDA 186.64→162.85 = -12.75% 一致；SOX、AMD、AVGO、标普本轮未复算。**补充**：11-11（第二段关系报道、WSJ「准备撤换」、Baird 降级当天）NVDA 收 173.73，**涨 2.87%**；讲稿如果讲「消息一出就跌」要避开这一天 | Yahoo chart |
| C16 | 未复核 | — | — |
| C17 | 通过 | "I owe my family and all of you an apology." 与 "I was unfaithful to my wife." 都逐字一致；信中**没有**出现 China、Alice、Megaspeed、spy、intelligence 这些词 | https://nvidianews.nvidia.com/news/a-message-to-our-company |
| C18 | 通过 | 三句都逐字一致（只有一处是弯撇号） | 同上 |
| C19 | 通过 | 三段都逐字一致；声明日期 2026-11-08 | https://nvidianews.nvidia.com/news/statement-from-nvidia-board-of-directors |
| C20 | 通过 | CNBC："cited people briefed on intelligence surveillance"。CNBC 那篇**没有**写「特朗普约一年前被简报」，这一说法出自 NYT（起诉状转引："Roughly a year ago, Mr. Trump was briefed"） | https://www.cnbc.com/2026/10/29/nvidia-jensen-huang-chinese-intelligence-asset.html |
| C21 | 通过 | 逐字一致 | 同上 |
| C22 | 通过（加注） | 逐字一致。「such investigations」指 WSJ 所说「新方另外调查过她与中国的关系」，**不等于新加坡从没调查过她**（见 C23） | https://www.police.gov.sg/media-hub/news/2026/10/20261030_clarification_statement_on_wall_street_journals_article |
| C23 | **需改** | ① "was not investigated for espionage" 是 Bernama 的转述，**原文没有引号**；带引号的只有 "had provided information which she knew to be inaccurate to SPF in the course of investigations"。② 同一篇报道还称：新加坡警方**确实调查过黄乐**，事由是她作为 Megaspeed 时任 CEO、董事长和主要控制人，涉嫌参与 Megaspeed 不实申报一案；2026 年 2 月与总检察署商议后认定证据不足。之后因她提供不实信息，新方对她发出严厉警告并禁止再入境。档案 §3 和 §6 的写法「新加坡否认曾就间谍事由调查黄乐」本身没错，但 sacrifice_test 反方论证里「新加坡说没调查过她间谍的事」要保留「间谍」这个限定，不能简化成「新加坡没调查过她」。③ 「明知提供不实信息」是新加坡政府对一位未被起诉的个人的认定，片中只能说「新加坡内政部称」。MHA 原文仍未取得，status 维持「有争议」 | https://web26.bernama.com/en/news.php?id=2633581 |
| C24 | 通过 | 郭嘉昆，10-30，逐字一致 | https://www.mfa.gov.cn/web/wjdt_674879/fyrbt_674889/202610/t20261030_12050300.shtml |
| C25 | 通过 | 郭嘉昆，11-09，逐字一致 | https://www.mfa.gov.cn/web/fyrbt_673021/jzhsl_673025/202611/t20261109_12056081.shtml |
| C26 | 通过 | 毛宁，11-12，逐字一致；这句之前还有一句「对于所谓"中国间谍"论调，我们已经阐明了立场」 | https://www.mfa.gov.cn/web/wjdt_674879/fyrbt_674889/202611/t20261112_12058185.shtml |
| C27 | 通过（加注） | AP 稿三句都逐字一致；讲话时间是 11-09（周一），WBTV 页面日期是 11-10。第二句是特朗普转述黄仁勋的话，里面「the person in question was a spy」是特朗普的措辞，引用时不能去掉引号 | https://www.wbtv.com/2026/11/10/trump-says-fbi-is-looking-nvidia-ceo-jensen-huangs-affair-with-alleged-chinese-agent/ |
| C28 | **未能核** | Politico 拒绝抓取，两次检索都没找到 Himes 的相关原话；"they didn't know" 和 "useful idiot" 都只见于 Wikipedia 转述。status 应降为「未能核」，**不能作为主要反驳证据**（见 §三） | https://www.politico.com/news/2026/11/11/jim-himes-alice-huang-nvidia-spy-01161718（不可访问） |
| C29 | 通过（风险） | 五名匿名前/现员工；原文写的是 "reports to him"；"Nvidia declined to provide a statement."。**该页点了当事人的姓名和职务**，见 §四 | https://thenightly.com.au/from/the-new-york-times/claims-ai-trailblazer-jensen-huang-had-affair-with-nvidia-executive--c-23151623 |
| C30 | 通过 | 逐字一致，之后他挂断了电话 | 同上 |
| C31 | 通过（补） | Reuters 11-13：两名匿名知情人，加上 Reuters 看到的 2026 年 10 月内部通信（2025 年的部分没看到）；对象是总法律顾问和首席营销官等高管，"standard business dealings with customers" 出现在两则 10 月消息里。档案 §3 黄乐那一行的引语不是原句，原句是 "A phone call and email to contact information listed on a business card for Alice Huang went unanswered." | https://investing.com/news/stock-market-news/exclusiveexnvidia-ceo-misled-top-lawyer-on-affair-with-chinese-businesswoman-sources-say-5026828 |
| C32–C41 | 未复核 | — | — |
| C42 | 通过（status 可升） | CNBC 转录："there is only one man to take his place - TIM COOK of Apple"、"A Legend replaces a Legend!"，可改为「已证实（经 CNBC 转录）」 | https://www.cnbc.com/2026/11/12/nvidia-jensen-huang-ceo-live-updates.html |
| C43 | 通过 | "has agreed to come"、"We're in negotiations for which day."；Mast 还说谈不拢就 "subpoena him" | 同上 |
| C44–C47 | 未复核 | — | — |
| C48 | 通过 | "Additionally, we are highly dependent on the services of our longstanding executive team." 后一句讲继任规划，与台账一致 | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm |
| C49 | 未复核 | — | — |
| C50 | 通过 | 董事会对 CNBC 的声明（11-13），两句都一致 | https://www.cnbc.com/2026/11/13/nvidia-huang-ceo-replacement-search.html |
| C51–C71 | 未复核 | — | — |
| C72 | 通过（风险） | 新闻稿日期 11-05，三位主席与所属委员会、日期、截止日都一致。**风险**：这份新闻稿的标题写「ties to Chinese intelligence asset」，正文称黄乐 "a publicly reported Chinese intelligence asset"，截图上片就等于替委员会重复这项指控 | https://chinaselectcommittee.house.gov/media/press-releases/moolenaar-mast-and-crawford-seek-briefing-from-jensen-huang-on-ties-to-chinese-intelligence-asset |
| C73 | 通过（status 改） | 引语逐字一致，日期 11-12。建议改为「已证实（引语）」，「离任性质有争议」另写在 note。**注意**：这是辞职公告后的声明，「unfortunate end that could have been avoided」带惋惜语气，不是要他下台的施压 | https://chinaselectcommittee.house.gov/media/press-releases/moolenaar-statement-on-jensen-huang-s-resignation-from-nvidia |
| C74 | 未复核 | — | — |
| C75 | 通过 | 回答彭博社的提问，逐字一致 | 外交部 11-12 实录 |
| C76 | 通过（算术） | 23.79 × 241 亿 ≈ 5,733 亿美元 | — |
| C77 | 部分通过 | NVDA 181.60 一致；SOX、标普未复算 | Yahoo chart |
| C78 | 需改（小） | 10-K："approximately 42,000 employees in 38 countries"（FY2026 末）。「4.2 万多名」改为「约 4.2 万名」，出处改为 10-K | 10-K |
| C79 | 未复核 | — | — |

### 2.2 补充研究 C80–C112

| id | 判定 | 原文或更正 | 依据 URL |
|---|---|---|---|
| C80 | 通过 | 参院：民主党至少拿到 54 席（AP 预测）；众院：民主党夺回多数；第 120 届国会 2027-01-03 就职（出自众院那篇） | https://aljazeera.com/news/2026/11/4/democratic-party-flips-us-senate-in-2026-midterm-elections ；https://www.aljazeera.com/news/2026/11/4/democratic-party-gains-us-house-majority-in-2026-midterm-elections |
| C81 | 通过 | 日期一致；只能证明时间先后 | NYT URL 日期；C80 |
| C82 | 通过 | 引语逐字一致；「先要 20%、还价到 15%」是报道的转述 | https://www.ideastream.org/2025-08-11/trump-says-nvidia-will-hand-the-u-s-15-of-its-h20-chip-sales-to-china |
| C83 | 通过 | 两句都逐字一致 | 10-K |
| C84 | 通过（补） | 两句都一致。**补充**：10-K 里 H200 许可计划写在 2026 年 2 月，对象是 "specific China-based customers"，不是 "approved customers"（"approved customers" 是特朗普 2025-12-08 宣布时的措辞）。另外，民主党 Wyden 和 Neal 11-12 的信质疑这笔 25% 关税安排是否构成违宪的出口税 | 10-K；CNBC 直播 |
| C85 | 通过 | 原文**确实**写作 "computing/compute"（带斜杠），可以照引；下文还有 "our effective foreclosure from the China market helped our competitors build larger developer and customer ecosystems" | 10-K |
| C86 | 通过 | 一致 | 10-K |
| C87 | 通过 | 一致 | 10-K |
| C88 | **未能核** | 10-K 按地区收入表在三段读取里都没读到；总收入 215,938 百万美元核到了。中国 197 亿和 9% 两个数片中不用 | 10-K |
| C89 | 通过（维持「有争议」） | Open 杂志（11-09）转述 Reuters 11-05："roughly 600,000 of those chips were waiting in Hong Kong"；北京 "was holding back approval for large shipments into the mainland" | https://openthemagazine.com/world/explained-trump-backs-jensen-huang-why-are-nvidias-chips-stuck-in-hong-kong |
| C90 | 通过 | Reuters 经 BNN，2025-05-21 台北 Computex：逐字一致；95%→50% 是转述，不是原话 | https://www.bnnbloomberg.ca/business/technology/2025/05/21/nvidia-ceo-praises-trump-move-to-scrap-some-ai-export-curbs/ |
| C91 | 通过（小注） | 两句都一致。X 帖的发布日期 Fox 没有写明，「当天改口」应改为「随后在 X 上发声明」 | https://www-ak-ms.foxbusiness.com/fox-news-tech/nvidia-ceo-jensen-huang-warns-china-going-win-ai-race-against-america-report |
| C92 | 未复核 | — | — |
| C93 | 未复核 | — | — |
| C94 | 通过（加注） | 日期 2025-12-12；签名 7 人全为民主党（Warren 牵头，Schumer、Wyden、Andy Kim、Bennet、Kaine、Slotkin）；三句都逐字一致。**加注**：信中把「a donation to the Trump ballroom」列为「charm offensive」的一部分，**没有写捐款人和金额**。片中不能说「民主党的信指英伟达捐了 2,500 万」 | https://www.banking.senate.gov/newsroom/minority/warren-schumer-colleagues-press-lutnick-on-administrations-decision-to-sell-out-us-national-and-economic-security-by-greenlighting-the-sale-of-h200-chips-to-china |
| C95 | 通过 | Reuters 经 The Standard（2025-12-13 HKT），句子开头一致；要求的简报时限是「1 月中」 | https://www.thestandard.com.hk/china/article/319233/US-lawmaker-demands-details-on-Trumps-decision-to-sell-Nvidia-H200-chips-to-China |
| C96 | **需改（来源）** | 台账给的 Al Jazeera 只写了 "overwhelmingly voted to advance"，**没有** McCormick、Barr、Issa，也没有 Meeks。票数 **42-2-1**、两名共和党人反对、Issa 投 present、Meeks 支持、新增两年禁售 Blackwell，这些来自 Axios 2026-01-21（403，经检索摘要与 MarketScreener 等转述）。source 应改为 Axios，quote 注明「检索摘要转述」；票数可以用，引号不能用。法案号 H.R. 6875 经 Ripon Advance 核到 | https://www.axios.com/2026/01/21/bill-chip-sales-china-advances （未读原文）；https://riponadvance.com/featured/house-foreign-affairs-committee-passes-masts-ai-overwatch-act/ |
| C97 | **需改（拆分）** | The Register 只核到：Sacks 转发一条帖子，称该法案由 "never Trumpers" 策划、有 Anthropic CEO 资金支持，并写 "Correct"。Mast 的「My job is not to be a yes-man to David Sacks or for Jensen Huang」**不在** The Register 里，检索也没找到，属于**未能核**，片中不用引号 | https://www.theregister.com/2026/01/21/house_gop_ai_chip_exports_trump_china_nvidia/ |
| C98 | 通过（小改） | 日期 2026-03-24，Banks（R-IN）与 Warren（D-MA）联名，引语逐字一致。正文要求的是 BIS「立即暂停并全面复审」所有对中国及马来西亚、泰国、越南、新加坡的先进英伟达芯片许可（「暂停或复审」是标题的说法） | https://www.banking.senate.gov/newsroom/minority/senators-banks-and-warren-urge-commerce-secretary-lutnick-to-suspend-or-reconsider-nvidia-export-licenses-amid-supermicro-chip-diversion-indictment |
| C99 | **需改（补全）** | NYT 原文写「Rubio … had overseen the drafting of a memo」，访华前几周起草，只发给少数高层官员；据一名信源，**这份备忘录不是给特朗普的，也没在空军一号上给他看**。Rubio 得知黄仁勋要在阿拉斯加登机后，才向特朗普 "briefed the president on the issue"（另一名匿名官员证实）；文章称这至少是 7 个月里的第二次简报（第一次在 2025 年深秋）。国务院拒绝置评，白宫发了一份背景声明质疑报道但没给细节。status「指控未证实」恰当。档案里「情报来自特朗普政府内部（Rubio 备忘录）」必须带「据 NYT 匿名信源」 | https://www.staradvertiser.com/2026/11/11/breaking-news/trump-knew-of-nvidia-ceos-suspected-spy-ties-before-beijing-visit/ |
| C100 | 通过 | 三句都一致。第三句的完整原文是 "Certainly, it didn't make much of an impact on me."，都是 11-09（周一）说的；"very honorable man" 是在被问到会不会向习近平提起此事时说的（AP） | 同上；WBTV/AP |
| C101 | 通过 | Reuters（Kanishka Singh，11-10）："Senior Republican on US Senate banking panel calls on Nvidia CEO Huang to resign"；引语逐字一致，是 11-10 晚上对 Politico 说的；Cramer 是 R-ND（247wallst 核到）。note 写「经 Reuters 转述 Politico」即可 | https://wsau.com/?p=1034404 ；https://247wallst.com/investing/2026/11/11/a-republican-senator-just-told-jensen-huang-to-step-down/ |
| C102 | **未能核** | 台账给的 247wallst 那篇**根本没提 Kudlow**。检索摘要称他在 Fox Business 节目里要黄仁勋「立即下台」、称之为「commonsense action」，但两次检索都没找到原视频或可靠的原文转录。片中不用引号，最多说「据报道，前白宫经济顾问、Fox Business 主持人 Kudlow 在节目中要他下台」；Kudlow 不是议员，不能算进「共和党人要他走」 | 247wallst（不含该内容） |
| C103 | **需改（来源对不上）** | GV Wire 的 Reuters 稿只写了：Axios 称 Lutnick「stalled」、「has repeatedly stood in the way」，特朗普今年第三次批准打击转运（之前征求过马斯克的意见），Bessent 在战情室就商务部阻挠执行出口管制当面质问 Lutnick。**稿里没有** Megaspeed、实体清单、「start a trade war with China」，也没有商务部的否认。这三点要么找到 Axios 原文，要么删掉；status 维持「指控未证实」 | https://gvwire.com/2026/11/11/lutnick-stalled-trump-crackdown-on-diversion-of-nvidia-chips-to-china-axios-reports/ |
| C104 | 通过 | 白宫官员："President Trump maintains complete confidence in the secretary." | CNBC 直播 |
| C105 | **需改（逐字）** | 原句是 "It's clear that the American people cannot rely on Big Tech billionaire CEOs to put our national security above their bottom line."；Warren 同时呼吁通过 AI Overwatch Act。CNBC 称她 "is poised to lead" 银行委员会，没有用 "chair" | CNBC 直播 |
| C106 | 通过 | 逐字一致，后面还有一句 "has to be looked at" | CNBC 直播 |
| C107 | 通过（note 改） | "Congress must demand answers" 一致。Schumer 的追问原文是 "Were government officials told not to investigate because of Trump's relationship with Mr. Huang?"，还有 "What did Trump know when he personally invited Mr. Huang aboard Air Force One?"。档案和角度文件里「追问调查是否因……被叫停」应改为「追问是否有官员被告知不要调查」 | CNBC 直播 |
| C108 | 通过 | 两句都逐字一致 | 委员会 11-12 声明 |
| C109 | 通过（维持「有争议」） | Hewitt 访谈："what a horrible thing that is!"、"That's so sad to see that happen."。CNBC 转述 NYT：Trump 周二（11-10）致电黄仁勋，"urging him to fight to keep his job as Nvidia CEO"。NYT 原文没检索到，Star-Advertiser 转载的那篇 NYT 也没有这条 | CNBC 直播 |
| C110 | **需改（不是原话，方向也要补）** | HK01（11-10）原文是「胡锡进认为，黄仁勋被揪斗出来，这是美国两党恶斗搞出的一个政治牺牲品，它完全是美国的恶作剧，与中国没半毛钱关系」，**是记者转述，没有引号**，微博原帖没有找到。HK01 前一天（11-09）的转述是：「这是民主党和美国建制派搞黄仁勋、并进而搞特朗普的一种方式」。片中只能写「据香港 01 转述，胡锡进称……」，不能加书名号或引号当原话用，并且要把他 11-09 指向民主党的说法一起讲出来 | https://global.hk01.com/即时中国/60408934/黄仁勋出轨-胡锡进-黄乐受的是历史上女人最猛烈-复杂的冤枉 ；https://global.hk01.com/article/60408734 |
| C111 | 通过 | 「环球时报快评：黄仁勋出轨，还能扯上中国？」（11-09，环球时报官方账号），引句逐字一致；全文**没有提两党**，也没用「牺牲品」 | https://news.sina.cn/gj/2026-11-09/detail-iniycfmw6324682.d.html |
| C112 | **需改（重写）** | 依据要按本核查更新：去掉 C28 Himes、Blanche、CNN（未能核）；Moolenaar 不能算「要他走」；「只有白宫在放」要加国会领导层与「未立法」两个限定；「民主党打特朗普 / 共和党推法案」改成「两党都推立法、都追商务部，民主党点名特朗普」。建议的改写见 §五 | — |

### 2.3 不在台账、但出现在 §8 和角度文件里的说法

| 说法（位置） | 判定 | 更正与依据 |
|---|---|---|
| 「2025-12 英伟达承诺向白宫宴会厅出资 2,500 万美元」（politics.md §1；sacrifice_test S5；dossier §8.3） | **需改（日期）** | 2,500 万这个金额出自**华盛顿邮报 2026-10-15** 披露的泄露捐款表（统计到 2026 年 9 月底），Reuters 称未独立核实；英伟达表示支持的是非党派的信托、与商业利益无关，但没有确认金额。英伟达捐款这件事 2025-12 就已经为人所知：Warren 与 Dave Min 2025-12-04 致信英伟达等 5 家公司，警告可能违反联邦反贿赂法；英伟达 2025-12-16 回函称钱捐给了 Trust for the National Mall。Korea Times（Reuters）的原句是 "The company committed $25 million … according to media reports"。来源：https://thenextweb.com/news/nvidia-apple-25m-trump-ballroom-donors ；https://www.warren.senate.gov/newsroom/press-releases/warren-min-lawmakers-question-giant-corporations-on-trump-ballroom-donations-influence-peddling-with-trump-administration-for-favors/ （检索摘要）；https://www.koreatimes.co.kr/world/20261110/trumps-close-ties-to-nvidias-huang-scrutinized-after-foreign-intelligence-concerns |
| 海湖庄园晚宴、国家科学奖章、特朗普买卖英伟达股票、习近平国宴（politics.md §1） | 通过（报道称） | Korea Times（Reuters，11-10）都有对应句子 |
| Coons 11-07「I'm pushing to investigate Jensen Huang and Nvidia…」 | 通过 | 发在 X 上，经 Reuters 转述；同上 |
| 特朗普 11-08「honorable guy」 | 通过 | Reuters 称是「周日晚」对记者说的；Open 杂志另记了一句 "done an amazing job for our country" |
| Warren 2025-12-03 两句 | 通过（小注） | 原文都没在句号处结束：「…behind closed doors as he kills the bipartisan GAIN AI Act」、「…under oath – not pushing his agenda in secret meetings」 | https://www.banking.senate.gov/newsroom/minority/warren-criticizes-nvidia-ceos-closed-door-meeting-on-capitol-hill-presses-administration-not-to-greenlight-sale-of-h200-ai-chips-to-china |
| GAIN AI 随参院版 NDAA 77:20 通过 | 通过 | Washington Technology 2025-10-14：77-20，Banks 提案，Warren 称之为 "This bipartisan amendment" | https://www.washingtontechnology.com/companies/2025/10/ai-export-control-bill-passes-senate-ndaa-amendment/408798/ |
| 最终版 NDAA 删掉 GAIN AI | 通过（报道称） | 多家报道（Axios 2025-11-19 等）称白宫施压，并直接找过多数党领袖 Scalise；黄仁勋称这个结果 "wise"。没有核 NDAA 正文 | 检索摘要（Axios、Akin Gump、Tom's Hardware） |
| CNBC 直播各条的时间戳（politics.md §3） | 需改（小） | 本轮读到的时间与角度文件差 1–21 分钟（例如 Meeks 12:27、Wyden/Neal 12:18、Hewitt 15:56），可能是直播页更新造成的。讲稿不要用分钟级时间 | CNBC 直播 |
| Huizenga（R）「disappointing」「disturbing」 | 风险 | CNBC 是间接引述，说他认为黄仁勋**危及国家安全**的行为令人失望、令人不安。这两个词不是他的直接引语，不能作为他的原话上片 | CNBC 直播 |
| Blanche「There's no conclusions reached…」；CNN「over-torqued」（allegations.md，sacrifice R5） | **未能核** | 检索两次都没找到，只经 Wikipedia 转述；另外有检索结果在别的语境里称 Blanche 为 **Acting Attorney General**，「司法部长」这个头衔要先核实再写 | — |

---

## 三、论点证据链评估

### 3.1 主线：中美科技战让一个 CEO 的私事变成了国家安全问题

**站得住（强）。** 证据链：情报关注的是一家疑似转运英伟达芯片到中国的客户（新加坡警方声明 C22；MHA 称该公司涉嫌不实申报，C23）→ 董事会以「外国情报活动」报道为由启动调查（C19，一手）→ 三委员会主席请他简报，委员会口径直接把黄乐写成「publicly reported Chinese intelligence asset」（C72，一手）→ 辞职当天 Moolenaar 把这件事接到 NDAA 出口管制立法上（C108，一手）→ 中方称之为科技封锁的借口（C26，一手）。

需要守住的边界：
- 他书面承认的只有「不忠」，没有点名，信里也没有任何涉华字眼（C17）。「私事」指的是这一点，不能写成「他承认与间谍有染」。
- 董事会接受辞职的当天，新出来的消息是第二段关系报道（治理问题）；辞职原因没有公开（C07）。主线只讲「变成国家安全问题」，**不讲「因国家安全下台」**。

### 3.2 第二层（我们的判断）

| 半句 | 评估 | 依据 | 缺口与反例 |
|---|---|---|---|
| 「国会两党都要收紧」 | **基本成立** | 2025-12-12 民主党 7 人的信（C94）；Moolenaar 2025-12 的信（C95）；GAIN AI 参院 77:20；AI Overwatch 外委会 42:2:1、Meeks 支持（C96，来源待换）；Banks＋Warren 联名（C98）；11-12 Warren、Moolenaar 都呼吁立法 | 反对票来自两名共和党人；国会**至今没有通过任何约束性措施**；应写成「两党都有人带头要收紧」，不写成「国会要收紧」 |
| 「只有白宫在放」 | **说过头，需改** | 白宫放行 H20、H200（C82–C84）；据报白宫施压删掉 GAIN AI；Sacks 认同「never Trumpers」的说法（C97 后半） | GAIN AI 是在国会共和党领导层的配合下删掉的；AI Overwatch 卡在全院表决之前（Scalise 未表态）；行政部门内部也有收紧的声音：Rubio 备忘录（匿名报道）、Bessent 质问 Lutnick（匿名报道）、特朗普三次批准打击转运（匿名报道）、贸易代表 Greer「we remain concerned」。准确的说法是：**「批准对华放行的是特朗普白宫」** |
| 「丑闻来时他站在白宫那边」 | **成立（作为关系描述）** | 海湖庄园、宴会厅捐款、随行访华、PCAST、奖章、特朗普 11-08/09/10/12 持续力挺（C100、C109） | 这是对他政治位置的描述，片中要给出处；宴会厅捐款的日期按 §2.3 改 |
| 「两党都拿他打自己的仗」 | **作为「我们的判断」有依据** | 民主党：Meeks、Schumer、Wyden/Neal 都指向特朗普政府（C106、C107）；共和党鹰派：Moolenaar 立刻接到 NDAA（C108） | 「拿他打仗」带有工具化的动机意味，建议改成描述行为的「借这件事」 |
| 「民主党借他打特朗普和商务部，共和党鹰派借他推出口管制法案」 | **两分法不准，需改** | — | Warren（D）11-12 同样呼吁通过 AI Overwatch（C105）；Tim Scott（R）要 Lutnick 12-10 公开作证，Huizenga（R）批评商务部不配合，Mast（R）要查 BIS，都是共和党在追商务部。能干净分开的只有：**民主党点名特朗普本人，共和党不点名** |

### 3.3 档案漏掉或用错的反例

1. **民主党早就冲着黄仁勋本人来了，不只是冲特朗普**：Warren 2025-12-03 要他「testify publicly and under oath」；Warren 与 Min 2025-12-04 致信英伟达 CEO，就宴会厅捐款警告可能违反反贿赂法；Coons 11-07「investigate Jensen Huang and Nvidia」；检索摘要还显示 Warren 2026-09-22 施压特朗普确认黄仁勋不会出现在谈判桌上，他还拒绝出席 Warren 要求的 2026 年 6 月听证会（后两条未读原文）。这**支持**「他被当作特朗普阵营的人来打」，但削弱「民主党只打特朗普」。
2. **11-11 前公开要他下台的议员只找到一个**：Cramer（R）。Kudlow 不是议员，原话也没核到；Moolenaar 的「firing」是 11-12 的事后声明，带惋惜语气，不能算施压。档案 §8.3 反驳 1、sacrifice R1、§8.1 表格要改。本轮另外检索两次，**也没找到**民主党人在 11-11 前要他辞职；Jeffries 11-12 说辞职「was the right thing to do」（CNBC 直接引语，已核）。
3. **公开力挺他的共和党议员一个也没找到**（检索两次）；力挺他的是特朗普本人，以及马斯克、Ackman 等商界人物。CNBC 直播里有赵长鹏说「a mistake for Nvidia to let Jensen resign」，还有 Hyphen Capital 的 Dave Lu 批评舆论对他的对待带有种族色彩。最后这条是英文世界里接近「被冤枉」叙事的声音，与 sacrifice R8「英文世界几乎没有」的说法有出入，建议补进 §3 的舆论表。
4. **胡锡进的框架本身是党派化的**：11-09 指向「民主党和美国建制派」，11-10 才说「两党恶斗」（都是 HK01 的转述）。档案把胡锡进当成「两党斗争牺牲品」说法的代表，要同时讲他指向民主党这一点。
5. **「民主党人 Himes 反而质疑间谍定性」没核到**，不能作为 sacrifice R5、dossier §8.1 和 §8.4 的关键反驳；CNN 与 Blanche 也一样。去掉这三条以后，「间谍定性有争议」还剩下：新加坡 MHA 称未以间谍事由调查她（Bernama 转述）、无任何起诉、中方否认，仍然够用。

---

## 四、法律与平台风险句清单

| # | 句子或做法（出处） | 风险 | 建议 |
|---|---|---|---|
| R1 | 截图或朗读众院委员会 11-05 新闻稿标题「…Ties to Chinese Intelligence Asset」、正文「a publicly reported Chinese intelligence asset」（C72） | 替委员会向未被起诉的黄乐重复间谍指控 | 只说「三位共和党主席以涉及国家安全为由请他简报」；如果必须引用，加「委员会称」，并紧接着放新加坡和中方的说法 |
| R2 | 「新加坡称她曾向警方提供明知不准确的信息，被警告并禁止入境」（C23） | 对个人的事实性认定，而且 MHA 原文没有取得 | 只说「据马来西亚国家通讯社转述新加坡内政部声明」；取得 MHA 原文之前不上片 |
| R3 | 「新加坡没调查过她」（sacrifice_test §4 反方论证的简化风险） | 与 MHA 所说「警方调查过她、2026 年 2 月证据不足」矛盾 | 保留「没有以间谍事由调查」，并补一句「新加坡曾就公司申报问题调查她，认定证据不足」 |
| R4 | 「情报来自特朗普政府内部（Rubio 备忘录）」（dossier §8.1、§8.3；sacrifice R3） | 把匿名报道当成事实，并归给具名官员 | 写「据《纽约时报》援引匿名信源」，并补上白宫质疑该报道 |
| R5 | 「Lutnick 拖延调查」「Lutnick 说会引发贸易战」「Bessent 追问 Megaspeed 实体清单」（C103） | 对具名官员的指控，而且后两点在台账来源里找不到 | 删掉后两点；前一点只说「Axios 援引匿名信源报道」 |
| R6 | 胡锡进「这是美国两党恶斗搞出的一个政治牺牲品」加引号（C110；dossier §8.1；sacrifice S8） | 把转述当原话，属于错误归属 | 写「据香港 01 转述」，去掉引号，并加上他 11-09 指向民主党的说法 |
| R7 | 「民主党借他打特朗普」「共和党鹰派借他推法案」（第二层） | 动机推断（系列规则禁止）；英文受众会认为说的是党派动机 | 改成描述行为：「民主党人借这件事追问特朗普知道什么；共和党鹰派借这件事推出口管制立法」，并标「我们的判断」 |
| R8 | Huizenga「危及国家安全令人失望、令人不安」 | 间接引语里预设了黄仁勋危及国家安全 | 不用 |
| R9 | 特朗普「He said he had absolutely no idea that the person in question was a spy」（C27） | 句子里预设「她是间谍」 | 要用就完整保留引号和「特朗普说」，旁边加「她的身份没有定论」 |
| R10 | 起诉状截图（C10）里「suspected Chinese spy」、点名 Alice Huang 的段落 | 原告单方指控 | 只截页眉和案号 |
| R11 | 「黄仁勋误导总法律顾问」（C31） | 对黄仁勋的事实指控，只有两名匿名信源 | 只说「路透社援引两名匿名知情人士报道」；本人代表与公司拒绝置评 |
| R12 | 第二位当事人：The Nightly（NYT 转载，C29）**点了她的姓名和职务**，CNBC「second-affair」那篇大概率也有 | 隐私与骚扰政策；非公众人物 | 这些页面一律不截图、不滚动展示；片中不提她的职务或业务线，只说「一名向他汇报的高管」。本系列全部文件已检索，**没有出现她的姓名** |
| R13 | 「美国情报界自己都说不准她是不是间谍」「司法部长说没有结论」（sacrifice §4） | 依据是 CNN 与 Blanche 的说法，都没核到；头衔也可能不对 | 核到原文之前不用；改用「没有任何起诉；中国否认；新加坡称未以间谍事由调查她」 |
| R14 | 「英伟达捐 2,500 万美元换政策」（由 C94 与宴会厅捐款合起来容易推出） | 把民主党信里的指控和泄露的捐款表拼成「行贿」的暗示 | 两件事分开说，各自注明「民主党人的信称」「据《华盛顿邮报》披露」；英伟达称与商业利益无关 |
| R15 | 「Moolenaar 说他是被解雇的」 | 与 8-K「accepted the resignation」冲突 | 照 dossier §6.1 的写法：「公司称辞职；有议员称之为解雇」 |

---

## 五、必须改的清单（19 条）

1. **C110 胡锡进**：改为 HK01 转述，去掉引号；补 11-09「民主党和美国建制派搞黄仁勋、并进而搞特朗普」；dossier §8.1、sacrifice S8 和 §3 表格同步改。
2. **C28 Himes**：降为「未能核」；从 dossier §8.1、§8.4 和 sacrifice R5 的关键反驳里拿掉，或者标成「待核」。
3. **Blanche 与 CNN「over-torqued」**：标「未能核」，核实 Blanche 的头衔；sacrifice §4 反方论证里的相关句子要改。
4. **Moolenaar 被误用为「要他下台」**：dossier §8.3 反驳 1、§8.1 表格、sacrifice R1 都要改成「辞职后，他称之为解雇，并要求英伟达换上把国家安全放第一的领导层」。
5. **C102 Kudlow**：「未能核」，source 错（247wallst 那篇不含 Kudlow），去掉引号，不计入「共和党人要他走」。
6. **C103 Axios**：删掉 Megaspeed 实体清单、「start a trade war with China」和商务部否认这三点，或者另找 Axios 原文。
7. **C96 AI Overwatch**：source 换成 Axios，写 42-2-1，注明「检索摘要转述」。
8. **C97**：拆开写；Mast「yes-man」那句「未能核」，Sacks「Correct」保留。
9. **C23 新加坡 MHA**：把引语和转述分开；补「警方曾就 Megaspeed 申报问题调查她，2026 年 2 月认定证据不足」；status 维持「有争议」。
10. **C99 Rubio 备忘录**：补「备忘录不是给特朗普的」「阿拉斯加登机前当面简报」「至少第二次」「白宫背景声明质疑报道」；凡写「情报来自特朗普政府内部」的地方都要加「据 NYT 匿名信源」。
11. **宴会厅 2,500 万美元的日期**：「2025-12 承诺」改为「据《华盛顿邮报》2026-10-15 披露」；补英伟达 2025-12-16 回函；C94 加注「信中没写捐款人」。
12. **第二层「只有白宫在放」**：改为「批准对华放行的是特朗普白宫」，并补「国会至今未立法，GAIN AI 被删掉要有国会领导层配合」。
13. **第二层的党派两分法**：改为「两党都借这件事推收紧立法、都追商务部；民主党点名特朗普，共和党不点名；11-11 前唯一公开要他走的议员是共和党人 Cramer」。
14. **C105 Warren**：引语按原句「It's clear that the American people…」，补「同时呼吁通过 AI Overwatch Act」。
15. **C107 Schumer**：politics.md 与 dossier §8.3 改为「追问是否有官员被告知不要调查」。
16. **补反例**：Warren 2025-12-03 要求宣誓作证、Warren 与 Min 2025-12-04 的反贿赂法警告信、Coons 11-07 要调查黄仁勋本人，写进 politics.md §2 和 sacrifice §2.2；Dave Lu、赵长鹏的声音补进 sacrifice §3 的舆论表。
17. **C112**：按第 12、13 条与 §三重写依据和结论。建议改成：「我们的判断：在对华卖先进芯片的问题上，国会两党都有人带头要收紧（外委会 42:2），批准放行的是特朗普白宫；丑闻出来后，两党都借这件事推收紧、追商务部，区别在于民主党把矛头指向特朗普。我们没有找到『某一党推动他下台』的记录。」
18. **R1 委员会新闻稿措辞**与 **R12 第二位当事人**：在 media 规划里明确这些页面不截图（C29、C72 的 note 里写上）。
19. **C78**：「4.2 万多名」改为「约 4.2 万名（10-K）」。

**建议改（不阻塞）**：C03 写明出处为 8-K；C42 升为「已证实（经 CNBC 转录）」；C73 status 改为「已证实（引语）」；C84 补「2026 年 2 月、specific China-based customers」；C91「当天」改为「随后」；C98 改为「立即暂停并全面复审」；politics.md 去掉分钟级时间戳；C15 补 11-11 当天上涨 2.87%。

---

## 六、未能核与未复核

- **未能核**（原文打不开或检索不到）：C28（Himes）、C88（中国收入 197 亿）、C97 前半（Mast「yes-man」）、C102（Kudlow 原话）、C103 中的 Megaspeed 实体清单、「trade war」与商务部否认、C96 的票数细节（只有检索摘要，Axios 原文 403）、C109 后半（特朗普致电劝留，只有 CNBC 转述 NYT）、Blanche 原话与头衔、CNN「over-torqued」、MHA 声明原文、胡锡进微博原帖。
- **未复核**（不在本轮优先范围）：C09、C14 和 C15 中的 SOX、AMD、AVGO、标普部分、C16、C32–C41、C44–C47、C49、C51–C71、C74、C77 中的 SOX 和标普部分、C79、C92、C93。其中 C38、C40（Bernstein）与 C37（Rene Haas）如果进讲稿，建议下一轮补核。
- **配额**：WebSearch 用了 19 次，剩 1 次（会话共用额度另计）。
