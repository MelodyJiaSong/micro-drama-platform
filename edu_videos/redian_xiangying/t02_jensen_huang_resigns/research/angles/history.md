# 角度：history：历史先例与「关键人物风险」

- **检索日期**：2026-11-14（片中一律说「截至 2026-11-14」）
- **检索范围**：
  - SEC EDGAR 一手文件：NVIDIA FY2026 / FY2025 10-K、2026 年委托书（DEF 14A），以及 Apple、Intel、McDonald's、HP、Boeing、Lockheed Martin、BP（6-K）、Uber 的 8-K、10-K 和招股书（424B4）；SEC 新闻稿 2023-4；SEC Staff Legal Bulletin 14E。
  - NVIDIA 官网治理文件：Corporate Governance Policies（2025-03-03）、NCGC 章程、Code of Conduct。
  - 学术文献：用 Crossref、OpenAlex、IDEAS/RePEc 按 DOI 核对书目和摘要。
  - 新闻报道（二手）：AP、CNBC、Fortune、TechCrunch、INSEAD Knowledge、Semafor、24/7 Wall St.（Yahoo 转载）等。
- **检索词（简列）**：Krzanich non-fraternization 2018 stock；Easterbrook SEC 2023 / settlement $105 million；Mark Hurd resign HP shares；Stonecipher Boeing 2005；Looney BP not fully transparent；Kalanick resign 2017；Jobs 2009 medical leave SEC；Jobs 1985 resign stock；Nike Parker Donahoe 2019；Nvidia succession plan board；sudden executive deaths stock price；CEO hospitalization；founder-CEO；managerial indiscretions firm value。
- **检索局限**：本会话的 WebSearch 共享额度中途用完，此后只用 WebFetch 抓已知 URL，并用 EDGAR 文件索引和 DOI 元数据查找。因此 **Nestlé 2025（Freixe）、Kohl's 2025 等较新的先例没有核实，正文不写**，只列在文末「尚不清楚」；紧急继任计划的问卷数据（Conference Board、Spencer Stuart 等）也没有取得。
- **隐私**：报道中第二段关系的当事人是英伟达在职高管，本文件不写其姓名。**片中不点名**。

---

## 一、先例逐案

### 总览表

| 先例 | 日期 | 是否创始人 | 官方给的原因（一手） | 临时 / 继任 | 短期股价（出处见各案） | 长期（可查数据） |
|---|---|---|---|---|---|---|
| Apple：乔布斯失去经营权，后辞职 | 1985-05 失去经营权；1985-09 辞去董事长 | 是 | 乔布斯自称公司对其新创业「hostile」（报道转述） | Sculley 继续任 CEO | TIME：辞职消息传出后「jumped $1 a share」 | 1997 年乔布斯回归（众所周知，本文未取一手）|
| Apple：病假披露争议 | 2009-01-05 公开信；2009-01-14 宣布病假 | 是 | 01-05 称「hormone imbalance」，01-14 改口「more complex」 | Tim Cook 负责日常运营 | 盘后 -7.3%（AP） | SEC 审查，未见结论 |
| Apple：乔布斯辞去 CEO | 2011-08-24 | 是 | 「that day has come」 | **按既定继任计划**由 COO Cook 接任 | 盘后约 -5%；次日收盘 -0.65% | 非关联方持股市值 3229 亿美元（2011-03）→ 3.25 万亿美元（2025-03）|
| Boeing：Stonecipher 被要求辞职 | 2005-03-06 | 否 | 与一名**不直接向他汇报**的女高管有私人关系，违反 Code of Conduct | CFO Bell 临时；董事长扩权 | 未查到 | 2005-06 外聘 McNerney |
| HP：Mark Hurd 辞职 | 2010-08-06 | 否 | 未违反性骚扰政策，但违反 Standards of Business Conduct | CFO Lesjak 临时（不参选正式 CEO）| 首个交易日市值约 -90 亿至 -100 亿美元，约 -10% | 外聘 Apotheker 不到一年即离任 |
| Lockheed Martin：候任 CEO Kubasik 辞职 | 2012-11-09 | 否 | 与一名下属员工有「close personal relationship」 | Hewson 接任（依「robust succession plan」）| 未查到 | Hewson 2013-01-01 起任 CEO |
| Uber：卡兰尼克辞去 CEO | 2017-06-20 | 是 | 投资人要求他让位（他本人对 NYT 的声明） | 2017 年 8 月起由 Dara Khosrowshahi 任 CEO（本文未取一手）| 非上市，无股价 | 2019 IPO 发行价 45 美元；2023 年经营利润 11.1 亿美元 |
| Intel：Krzanich 辞职 | 2018-06-20 | 否 | 违反「non-fraternization policy」（新闻稿语，8-K 没写原因）| CFO Swan 临时，后转正 | 收盘 -2.4%，报 52.19 美元 | 一年后 -8.7%（标普 +8.5%）；之后四年内又换两任 CEO |
| McDonald's：Easterbrook 被解雇 | 2019-11-01 生效，11-03 公布 | 否 | 「recent consensual relationship with an employee」 | 内部人 Kempczinski **当即**接任正式 CEO | 次日约 -2.7% 至 -3% | 2020 年起诉；2021 年追回逾 1.05 亿美元；2023 年 SEC 和解 |
| Nike：Parker 卸任（对照组）| 2019-10-22 宣布 | 否 | 有计划的交接，本人称与 Oregon Project 无关 | Donahoe | 盘后 +<1% | — |
| BP：Looney 辞职 | 2023-09-12 | 否 | 对过往与同事关系「not fully transparent」 | CFO Auchincloss 临时，2024-01 转正 | 次日收盘约 -2.7% 至 -3%（各家不一）| 2023-12 以「严重不当行为」解雇，没收及追回合计 3243 万英镑 |
| **NVIDIA：黄仁勋辞职** | 2026-11-11 | **是（联合创始人，任期 33 年）** | 8-K **未写原因** | **CFO Kress 临时，兼任 CFO**；首任董事长 Jones | 11-12 收 166.19 美元（-4.34%），盘中跌幅各家不一（见主简报）| 尚待观察 |

> 说明：长期一列里的「非关联方持股市值」取自各公司 10-K 封面，不等于总市值。我们不把长期变化归因于 CEO 离任，因为影响因素太多。

### 1. Apple

**1985 年：创始人被董事会剥夺经营权，随后辞职**
- 时间线：1985 年 5 月下旬董事会支持 CEO Sculley，乔布斯失去日常经营权，只保留董事长；1985-09-16 辞去董事长（各来源对 5 月的具体日期说法不一）。来源：Technologizer 2011-08-25 汇编的 1985 年报道 https://technologizer.com/2011/08/25/steve-jobs-steps-down-the-first-time-the-1985-press-coverage/index.html
- 股价：TIME（1985-09-30，经 Technologizer 转载）："Apple stock jumped $1 a share after Jobs' resignation became known"。**转述自 Technologizer 的转载，TIME 原刊未见。**
- 意义：这是「创始人离开、市场反而上涨」的例子。不过当时苹果业绩差，Microcap Club 称苹果从 IPO 到 1985 年 9 月股价跌了 47%（二手来源，未核对）https://microcapclub.com/same-stock-different-returns/

**2009 年：病假披露争议**
- 2009-01-05，乔布斯公开信（一手）："my doctors think they have found the cause—a hormone imbalance"；"The remedy for this nutritional problem is relatively simple and straightforward"。https://www.apple.com/newsroom/2009/01/05Letter-from-Apple-CEO-Steve-Jobs/
- 2009-01-14 致员工邮件，随 8-K Exhibit 99.1 一同提交（一手）："during the past week I have learned that my health-related issues are more complex than I originally thought"；"I have asked Tim Cook to be responsible for Apple's day to day operations"；"As CEO, I plan to remain involved in major strategic decisions"。https://www.sec.gov/Archives/edgar/data/320193/000118143109003017/rrd229456_27079.htm
- 股价：AP 报道 "Apple's shares slid $6.19, or 7.3 percent, to $79.14 in after-hours trading."（MPR 转载 AP）https://www.mprnews.org/story/2009/01/14/stevejobs_health
- SEC：Bloomberg 2009 年初报道 SEC 对苹果的健康披露做「review」，2009-07 报道仍在审查，焦点是 01-05 至 01-14 这九天（Fortune 2009-07-08 转述 Bloomberg）https://fortune.com/2009/07/08/steve-jobs-health-wheres-that-sec-probe/ 。**我们没有查到 SEC 对此采取执法行动的公开记录（未穷尽检索）。**
- 与本次的关联：两件事都是关键人物的私人事务（健康 / 私生活）先由外界报道，再由当事人公开表态，之后才出现正式的人事变动。苹果案的教训在于「先给轻描淡写的说法，九天后改口」。英伟达这次是 11-08 致员工信承认婚外情、11-11 辞职，中间也隔了几天，但是否存在「披露不完整」由其他角度核对，本文不下结论。

**2011 年：有继任计划的辞职**
- 8-K（一手）："On August 24, 2011: - Steve Jobs resigned as Chief Executive Officer of Apple Inc. … The Board promoted Chief Operating Officer Timothy D. Cook to Chief Executive Officer"。https://www.sec.gov/Archives/edgar/data/320193/000118143111047179/rrd320651.htm
- 乔布斯辞职信（一手）："I have always said if there ever came a day when I could no longer meet my duties and expectations as Apple's CEO, I would be the first to let you know. Unfortunately, that day has come."；"I strongly recommend that we execute our succession plan and name Tim Cook as CEO of Apple." https://www.apple.com/newsroom/2011/08/24Letter-from-Steve-Jobs/
- 股价：盘后约跌 5%（CNN Money 标题「Apple stock tumbles 5% in after hours trading」https://money.cnn.com/2011/08/24/technology/apple_after_hours_shares/index.htm ，本次抓取 503，只见标题）。Fortune 称盘后跌「nearly $20 (5.22%)」（检索摘要，未逐字核对）https://fortune.com/2011/08/24/steve-jobs-resigns-tim-cook-is-ceo-stock-drops-nearly-20/ 。次日收盘 Fortune 原文："Apple loses 0.65%"，同日 "the Dow and the S&P 500 fell 1.51% and 1.52%, respectively" https://fortune.com/2011/08/25/wall-street-shrugs-off-steve-jobs-resignation/
- 长期：10-K 封面的非关联方持股市值，FY2011 版为 "approximately $322,921,000,000"（截至 2011-03-25）https://www.sec.gov/Archives/edgar/data/320193/000119312511282113/d220209d10k.htm ，FY2025 版为 "approximately $ 3,253,431,000,000"（截至 2025-03-28）https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm ，约十倍。
- 对照要点：**有公开的、事先指定的继任人。**盘后一度大跌，正式交易日只跌 0.65%，还跑赢了大盘。

### 2. Boeing 2005：Harry Stonecipher

- 公司新闻稿，8-K Ex.99.1（一手，2005-03-07）："its Board of Directors asked for and received the resignation of President and CEO Harry Stonecipher on Sunday, March 6"；"a personal relationship between Stonecipher and a female executive of the company who did not report directly to him. The Board determined that his actions were inconsistent with Boeing's Code of Conduct."；董事长 Platt："The resignation was in no way related to the company's operational performance or financial condition"；"the CEO must set the standard for unimpeachable professional and personal behavior"；"The Board has a robust succession planning process in place"；CFO James Bell 任临时 CEO，"Bell, who is not a candidate"。https://www.sec.gov/Archives/edgar/data/12927/000119312505046669/dex991.htm
- 新闻稿还写道："The investigation determined the relationship was consensual and had no effect on the conduct of the company's business."，以及调查起因是 "information that was sent anonymously"。
- 继任：2005-06-29 与 W. James McNerney, Jr.（外部人，时任 3M CEO，3M 身份为常识，本文未取一手）签订雇佣协议，任董事长、总裁兼 CEO。https://www.sec.gov/Archives/edgar/data/12927/000119312505138157/dex991.htm
- 股价：**未查到可靠数字。**
- 对照要点：当事人不是创始人，对方也**不直接向他汇报**，董事会照样要求他辞职，理由是 CEO 要立「标准」。英伟达这次报道称第二段关系的对象是**向其汇报**的高管（NYT 报道、Axios 等转述，见主简报，未证实），按 Boeing 的标准性质更重。这一条是「我们的判断」。

### 3. HP 2010：Mark Hurd

- 新闻稿，8-K Ex.99.1（一手，2010-08-06）："Chairman, Chief Executive Officer and President Mark Hurd has decided with the Board of Directors, to resign his positions effective immediately."；"The investigation determined that there was no violation of HP's sexual harassment policy, but did find violations of HP's Standards of Business Conduct."；CFO Cathie Lesjak 任临时 CEO，"Lesjak has taken herself out of consideration as the permanent CEO"；首席独立董事 Robert Ryan："This departure was not related in any way to the company's operational performance or financial condition"。https://www.sec.gov/Archives/edgar/data/47217/000104746910007177/a2199755zex-99_1.htm
- 股价：AP（2010-12-20，NBC 转载）："HP's market value, which stood at around $108 billion before Hurd's exit"，"dropped about $9 billion in the stocks' first day of trading after the Aug. 6 resignation" https://www.nbcnews.com/id/wbna40758517 。INSEAD 的 Theo Vermaelen（2010-09-13）："HP's market value fell by $10 billion, close to a 10 per cent decline" https://knowledge.insead.edu/leadership-organisations/mark-hurd-affair 。**两个数字（90 亿 / 100 亿美元）有出入，均列出。**
- 后续：Vermaelen 写道，2010-09-07 "Hurd became co-president of Oracle"，当天 "Oracle's stock price increased by 5.9 per cent"（同上）。AP 称 SEC 在调查 Hurd 被迫辞职的情况（同上 NBC 链接）。
- 继任：2010-09-30 宣布外聘 Léo Apotheker，11-01 生效 https://www.sec.gov/Archives/edgar/data/47217/000110465910050820/a10-18763_18k.htm ；2011-09-22 "Léo Apotheker terminated as President and Chief Executive Officer" https://www.sec.gov/Archives/edgar/data/47217/000110465911052939/a11-26875_18k.htm
- 对照要点：与英伟达的结构最像，都是**CFO 临时兼任 CEO、调查后宣布、公司强调与经营无关**。HP 的教训是外聘继任者不到一年就离任，也就是说临时安排平稳，不代表正式接班会成功。

### 4. Lockheed Martin 2012：候任 CEO Christopher Kubasik

- 新闻稿，8-K Ex.99.1（一手，2012-11-09）："its board of directors asked for and received the resignation of Christopher E. Kubasik … effective immediately"；"Kubasik, previously slated to become CEO in January, resigned after an ethics investigation confirmed that he had a close personal relationship with a subordinate employee. His actions violated the company's Code of Ethics and Business Conduct"；时任董事长兼 CEO Stevens："we have a strong leadership team and a robust succession plan that allowed the board and me to react quickly"。https://www.sec.gov/Archives/edgar/data/936468/000119312512463676/d436152dex991.htm
- 继任：董事会当天选 Marillyn Hewson 为总裁兼 COO，2013-01-01 起任 CEO（8-K）https://www.sec.gov/Archives/edgar/data/936468/000119312512463676/d436152d8k.htm
- 股价：未查到。
- 对照要点：这家国防承包商在国家安全敏感行业，处理「与下属的关系」用的是**伦理调查确认、当天辞职、当天接班人到位**。同样是国安敏感行业，英伟达董事会至今在找猎头（见下文 CNBC 11-13），差别在于事先有没有接班人。

### 5. Uber 2017：Travis Kalanick（创始人，非上市）

- 时间与说法：2017-06-20 深夜，NYT 首报，TechCrunch 转述并经 Uber 发言人确认。Kalanick 对 NYT 说："I love Uber more than anything in the world"，"at this difficult moment in my personal life I have accepted the investors request to step aside"。TechCrunch 称此前五名主要投资人（含 Benchmark）联名致信要求他让位；他留任董事。https://techcrunch.com/2017/06/20/uber-ceo-travis-kalanick-resigns/
- 背景（TechCrunch，同上）：一周前他在 Eric Holder 报告发布后休假，报告涉及「toxic company culture」。
- 股价：非上市，无。TechCrunch 称最近一轮估值约 700 亿美元（同上）。
- 长期：2019 年 IPO 招股书（424B4）："initial public offering price is $45.00 per share" https://www.sec.gov/Archives/edgar/data/1543151/000119312519144716/d647752d424b4.htm 。招股书风险因素写道："Our workplace culture and forward-leaning approach created operational, compliance, and cultural challenges"；"We have previously received significant media coverage and negative publicity, particularly in 2017"（同上）。FY2023 10-K：经营利润 "Income (loss) from operations $ (1,832) $ 1,110"，即 2022 年亏 18.32 亿美元、2023 年盈 11.10 亿美元 https://www.sec.gov/Archives/edgar/data/1543151/000154315124000012/uber-20231231.htm
- 对照要点：同为创始人，但 Uber 当时不是上市公司，是**投资人逼宫**。英伟达是上市公司，黄仁勋持股 3.58%，单一股权（见第三节），董事会本身就有决定权。

### 6. Intel 2018：Brian Krzanich

- 8-K（一手）："On June 21, 2018, Intel Corporation ("Intel") announced that, on June 20, 2018, Brian M. Krzanich resigned as Chief Executive Officer and a member of Intel's Board"；"the Board appointed Robert ("Bob") H. Swan, 58, Intel's Executive Vice President and Chief Financial Officer, to serve as interim Chief Executive Officer … Mr. Swan also continues to serve as CFO"。**8-K 没写原因，与英伟达 8-K 写法相同。** https://www.sec.gov/Archives/edgar/data/50863/000119312518199045/d598882d8k.htm
- 原因（新闻稿）：Intel 新闻室原链接已失效（重定向到 404）。AP 转述 "the relationship was in violation of the company's non-fraternization policy, which applies to all managers"（CBS Sacramento 转载 AP）https://www.cbsnews.com/sacramento/news/intel-ceo-resigns-brian-krzanich/ 。**新闻稿原文未见，只有转述。**
- 股价：AP："closed down 2.4 percent at $52.19"（同上）。24/7 Wall St.："Intel stock fell 2.4% that day … the S&P 500 fell 0.6%"；一年后 "Intel was down 8.7% while the S&P 500 was up 8.5%"（2026-11-11，Yahoo 转载；**该文未写数据来源**）https://finance.yahoo.com/markets/stocks/articles/nvidia-board-reportedly-preparing-oust-233419551.html
- 长期：Swan 于 2019-01-30 转正 https://www.sec.gov/Archives/edgar/data/50863/000119312519023301/d702987d8k.htm ；2021-01-13 宣布 Gelsinger 接任 https://www.sec.gov/Archives/edgar/data/50863/000119312521009142/d82915d8k.htm ；Gelsinger 2024-12-01 辞职 https://www.sec.gov/Archives/edgar/data/50863/000005086324000173/intc-20241201.htm ；2025-03-10 任命 Lip-Bu Tan https://www.sec.gov/Archives/edgar/data/50863/000005086325000036/intc-20250310.htm 。非关联方持股市值从 1583 亿美元（2017-06-30，FY2017 10-K）降到 993 亿美元（2025-06-27，FY2025 10-K）https://www.sec.gov/Archives/edgar/data/50863/000005086318000007/a12302017q4-10kdocument.htm ；https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm 。**下滑主要与制程和竞争有关，不能归因于这次离任。**
- 对照要点：「CFO 临时兼任」「8-K 不写原因」「董事会表示内外部候选人都会考虑」三点几乎与英伟达一致。不同在于 Intel 当时业务已承压，英伟达则处在业务高点（24/7 Wall St. 的文章也这样对比）。

### 7. McDonald's 2019–2023：Steve Easterbrook

- 新闻稿，8-K Ex.99.1（一手，2019-11-03）："Kempczinski succeeds Steve Easterbrook, who has separated from the Company following the Board's determination that he violated company policy and demonstrated poor judgment involving a recent consensual relationship with an employee."；"The Company confirms that this leadership transition is unrelated to the Company's operational or financial performance." https://www.sec.gov/Archives/edgar/data/63908/000089882219000080/pressrelease1.htm 。8-K 正文用的是 "was separated from his officer and director positions … effective as of November 1, 2019" https://www.sec.gov/Archives/edgar/data/63908/000089882219000080/mcd8k20191104.htm
- 股价：24/7 Wall St. 称 "fell 2.7% the next trading day"，一年后 "up 14.7%, ahead of the S&P 500's 11.9%"（上引 Yahoo 链接，未写数据源）。AP 称盘中 "fell 3% to $187.60"，Bloomberg 称 "as much as 2.9%"（均为检索摘要，例如 https://www.clickondetroit.com/business/2019/11/04/mcdonalds-ousted-ceo-will-get-26-weeks-of-pay/ ）。**2.7% / 2.9% / 3% 量的是不同时点，全部列出。**
- 2020-08-10 8-K（一手）：董事会经员工举报后调查，"concluded that Mr. Easterbrook lied to the Company and the Board and destroyed information regarding inappropriate personal behavior and in fact had been involved in sexual relationships with three additional Company employees prior to his termination"，并在特拉华州衡平法院起诉追回补偿。https://www.sec.gov/Archives/edgar/data/63908/000089882220000056/mcd8k.htm
- 2021-12-16 和解新闻稿（一手）："Mr. Easterbrook has returned equity awards and cash, with a current value of over $105 million"；Easterbrook："I failed at times to uphold McDonald's values"。https://www.sec.gov/Archives/edgar/data/63908/000006390821000042/exhibit991-12162021.htm
- 2023-01-09 SEC 新闻稿 2023-4（一手）：认定 Easterbrook 违反证券法反欺诈条款，"five-year officer and director bar and a $400,000 civil penalty"（不承认也不否认）；McDonald's 违反 Section 14(a)，因为 "McDonald's failed to disclose that the company exercised discretion in treating Easterbrook's termination as without cause in conjunction with the execution of a separation agreement valued at more than $40 million"；公司因合作免罚。https://www.sec.gov/news/press-release/2023-4
- 长期：非关联方持股市值从 1577 亿美元（2019-06-28）升到 2085 亿美元（2025-06-30）https://www.sec.gov/Archives/edgar/data/63908/000006390820000022/mcd-12312019x10k.htm ；https://www.sec.gov/Archives/edgar/data/63908/000006390826000035/mcd-20251231.htm
- 对照要点：(1) **接班人当场就是正式 CEO**，市场只小跌。(2) 事后查出**隐瞒更多关系、对董事会说谎**，才演变成诉讼和 SEC 执法。也就是说，最严重的后果来自「对董事会不坦白」，而不是关系本身。英伟达这次，Reuters 独家称黄仁勋曾误导公司首席律师（见主简报，**报道称，未证实**）。如属实，性质会更接近 McDonald's 和 BP 两案；是否属实由其他角度核对。

### 8. Nike 2019：Mark Parker（对照组，不算「突然离任」）

- CNBC（2019-10-22）：Parker 于 2020 年 1 月卸任 CEO，转任执行董事长，由董事 John Donahoe 接任；"Parker said the decision was not prompted by the recent doping allegations tied to Nike's Oregon Project"；Nike 盘后 "last up less than 1%"，而 ServiceNow（Donahoe 原公司）"fell more than 10%"。https://www.cnbc.com/2019/10/22/nike-ceo-mark-parker-to-step-down-john-donahoe-to-replace-him-in-2020.html
- 对照要点：有计划的交接，即使背景里有丑闻，股价也几乎不动。**接班人离开的那家公司反而大跌**，这也是一种「关键人物溢价」。

### 9. BP 2023：Bernard Looney

- 6-K（一手，2023-09-12）："Bernard Looney has notified the Company that he has resigned as Chief Executive Officer with immediate effect. Murray Auchincloss, the Company's CFO, will act as CEO on an interim basis."；2022 年 5 月董事会收到匿名举报，"No breach of the Company's Code of Conduct was found. However, the Board sought and was given assurances"；"Mr Looney has today informed the Company that he now accepts that he was not fully transparent in his previous disclosures." https://www.sec.gov/Archives/edgar/data/313807/000165495423011775/a2297m.htm
- 6-K（一手，2023-12-13）："in providing inaccurate and incomplete assurances in July 2022, Mr Looney knowingly misled the board. The board has determined that this amounts to serious misconduct"，即日解雇；"The total maximum value of the potential remuneration that has been forfeited or clawed back is £32,426,000"，其中 "87% of this value is automatically forfeited as a result of Mr Looney's resignation"。真正「追回」的两项是 £420,000（2022 年现金奖金的 50%，税后）和 £529,000（股票的 6/36，税后），合计约 94.9 万英镑。https://www.sec.gov/Archives/edgar/data/313807/000165495423015466/a6931w.htm
- 继任：2024-01-17 6-K，标题「MURRAY AUCHINCLOSS APPOINTED BP CEO」https://www.sec.gov/Archives/edgar/data/313807/000165495424000652/a9756z.htm
- 股价（二手，**各家不一**）：开盘最多跌 1.8%；Alliance News 称收盘「down nearly 3%」；Geo News 称「closing down 2.7%」；Hargreaves Lansdown 称「fell 1.1%」（未注明时点）。来源为检索摘要，例如 https://www.geo.tv/amp/509771-bp-ceos-resignation-impacts-share-prices 、https://www.hl.co.uk/shares/share-research/BP-CEO-Looney-quits-over-incomplete-relationships-disclosure
- 对照要点：BP 一共发了**三份一手公告**（辞职、解雇与没收薪酬、转正），每份都写明原因和金额。英伟达 8-K 至今没写原因，薪酬处理也未披露（**尚不清楚**）。

---

## 二、「关键人物风险」：学术研究能说什么

只列书目已用 Crossref / OpenAlex / IDEAS 核对过的文献，结论只引摘要原文。拿不到摘要的，只写书目，不写结论。

1. **Johnson, Magee, Nagarajan & Newman (1985)**，"An analysis of the stock price reaction to sudden executive deaths: Implications for the managerial labor market"，*Journal of Accounting and Economics* 7: 151–174。DOI: 10.1016/0165-4101(85)90034-5（IDEAS 页：https://ideas.repec.org/a/eee/jaecon/v7y1985i1-3p151-174.html ）。**本次没有取得摘要或正文**（IDEAS 显示 "No abstract is available"，ScienceDirect 返回 403），因此不引其结论。这篇是「用高管猝死做自然实验」的开山之作。
2. **Worrell, Davidson, Chandy & Garrison (1986)**，"Management turnover through deaths of key executives: Effects on investor wealth"，*Academy of Management Journal* 29(4): 674–694。DOI: 10.2307/255939。OpenAlex 只给出摘要首句，结论未取得，不引。
3. **Salas (2010)**，"Entrenchment, governance, and the stock price reaction to sudden executive deaths"，*Journal of Banking & Finance* 34(3): 656–666。DOI: 10.1016/j.jbankfin.2009.09.002。摘要原文："If a highly effective manager dies unexpectedly, the stock price reaction should be negative. If, however, death removes an entrenched manager when the board would or could not, the stock price reaction should be positive."；"the reaction is strongly positive (6.8%) if: (1) the executive's tenure exceeds 10 years, and (2) abnormal stock returns over the last three years are negative." https://ideas.repec.org/a/eee/jbfina/v34y2010i3p656-666.html （SSRN 早期版本写的是「5 to 7%」，DOI 10.2139/ssrn.819564）
   - 与本次的关系（**我们的判断**）：黄仁勋任期远超 10 年，但过去三年股价表现极好，不满足 Salas 所说「市场为之叫好」的第二个条件。按这一框架，市场应把他的离开当作损失。英伟达 11-12 下跌与这个方向一致，但单个案例不能检验理论。
4. **Quigley, Crossland & Campbell (2017)**，"Shareholder perceptions of the changing impact of CEOs: Market reactions to unexpected CEO deaths, 1950–2009"，*Strategic Management Journal* 38(4): 939–949。DOI: 10.1002/smj.2504。摘要原文："Using an event study methodology and a sample of 240 sudden and unexpected CEO deaths, we show that absolute (unsigned) market reactions to these events in U.S. public firms have increased markedly between 1950 and 2009."；"highlighting the importance of succession planning"。
   - 可用的认知：股东越来越把 CEO 当作决定公司好坏的关键人物，市场对 CEO 突然离开的反应幅度（不论涨跌）在过去六十年里越来越大。
5. **Nguyen & Nielsen (2014)**，"What Death Can Tell: Are Executives Paid for Their Contributions to Firm Value?"，*Management Science* 60(12): 2994–3010。DOI: 10.1287/mnsc.2014.2011。摘要原文："Using stock price reactions to sudden deaths of top executives as a measure of expected contribution to shareholder value"；"an average top executive (chief executive officer) appears to retain 71% (65%) of the marginal rent from the firm-manager relationship."
6. **Bennedsen, Pérez-González & Wolfenzon (2020)**，"Do CEOs Matter? Evidence from Hospitalization Events"，*Journal of Finance* 75(4): 1877–1911。DOI: 10.1111/jofi.12897。摘要原文："CEOs have a significant effect on profitability and investment"；"CEO effects are larger for younger CEOs, in growing and family-controlled firms, and in human-capital-intensive industries"；"the hospitalization of other senior executives does not have similar effects"；"CEO contingency plans are valuable."（数据为丹麦企业，外推到美国大公司需谨慎。）
   - 同组作者 2007 年工作论文 "Do CEOs Matter?"（SSRN，DOI 10.2139/ssrn.970575）摘要原文："CEO deaths are strongly correlated with declines in firm operating profitability, asset growth and sales growth"；"the death of board members does not seem to affect firm prospects"。
7. **Fahlenbrach (2009)**，"Founder-CEOs, Investment Decisions, and Stock Market Performance"，*Journal of Financial and Quantitative Analysis* 44(2): 439–466。DOI: 10.1017/S0022109009090139。摘要原文："Eleven percent of the largest public U.S. firms are headed by the CEO who founded the firm."；"An equal-weighted investment strategy that had invested in founder-CEO firms from 1993 to 2002 would have earned a benchmark-adjusted return of 8.3% annually … the abnormal return is still 4.4% annually."
   - 这是「创始人 CEO 溢价」的代表研究，样本期为 1993–2002，不能直接套用到 2026 年的英伟达。
8. **Cline, Walkling & Yore (2018)**，"The consequences of managerial indiscretions: Sex, lies, and firm value"，*Journal of Financial Economics* 127(2): 389–415。DOI: 10.1016/j.jfineco.2017.11.008。摘要原文："Personal managerial indiscretions are separate from a firm's business activities but provide information about the manager's integrity."；"companies of accused executives experience significant wealth deterioration, reduced operating margins, and lost business partners"；"Indiscretions are also associated with an increased probability of unrelated shareholder-initiated lawsuits, Department of Justice and Securities and Exchange Commission investigations"；"Indiscretions occur more often at poorly governed firms where disciplinary turnover is less likely." https://ideas.repec.org/a/eee/jfinec/v127y2018i2p389-415.html
   - 与本次关系最直接的一篇：私生活丑闻会被市场当作「诚信信号」，后果不只是换人。具体数字（异常收益率等）在正文里，本次未取得。

**学术部分的小结**（我们的判断，依据为上列摘要）：
- 一个 CEO 值多少钱，可以用「他突然离开时市场怎么反应」来度量。这种反应有正有负：被认为是负担的人离开，股价会涨（Salas）。
- 市场对 CEO 突然离开的反应幅度几十年来在变大（Quigley 等）。
- CEO 的缺席会实际影响盈利和投资，不只是情绪（Bennedsen 等）。研究者由此得出「应急预案有价值」的结论。
- 私生活丑闻通过「诚信」渠道影响公司价值，而且更常出现在治理弱的公司（Cline 等）。这一条可以接到第三节英伟达的治理文件。

---

## 三、公司治理做法

### A. 英伟达自己的文件（一手原文）

**1）10-K 风险因素里的「关键人员」：没有点名黄仁勋**
- FY2026 10-K（2026-02-25 提交，黄仁勋本人签署）的风险因素标题："If we are unable to attract, retain and motivate our executives and key employees, our business may be harmed."；该段末句："Additionally, we are highly dependent on the services of our longstanding executive team. Failure to ensure effective succession planning, transfer of knowledge, and smooth transitions involving executives and key employees could hinder our strategic planning, execution, and long-term success." https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm
- FY2025 10-K 的同一段话字句相同 https://www.sec.gov/Archives/edgar/data/1045810/000104581025000023/nvda-20250126.htm
- **要点：10-K 说的是「依赖长期在任的高管团队」（longstanding executive team），没有单独点名 Jen-Hsun Huang。**我们在全文里检索 "Huang"，只出现在高管名单和签名页。
- 「succession」一词在 FY2026 10-K 中**出现一次**，就是上面这句。

**2）委托书与治理政策：没有写 CEO 继任计划**
- 2026 年委托书（2026-05-12）全文**没有出现 "succession"**（我们的全文检索结果；只出现 "successor" 一次，是董事选举的套话 "until his or her successor is elected"）。https://www.sec.gov/Archives/edgar/data/1045810/000104581026000036/nvda-20260512.htm
- 委托书「Board Leadership Structure」原文："Our Board ensures that each member has an equal voice in the affairs and management of NVIDIA by having an independent Lead Director, rather than a chairperson."；当时的首席独立董事为 Stephen C. Neal（77 岁）。Harvey C. Jones 73 岁，1993 年起任董事。（同上）
- 董事会风险监督清单列了 "Management development"，没有 "succession"（同上）。
- Corporate Governance Policies（2025-03-03 版）只写："Senior Management Development. The Board shall receive and review periodic updates on the Company's senior management development."；关于领导结构："The Board may select a chairperson of the Board in its discretion. If the Company does not have an independent chairperson, a Lead Independent Director … shall be designated annually"。**全文没有 "succession"**；NCGC 章程也没有（我们对 PDF 文本的检索结果）。https://s201.q4cdn.com/141608511/files/doc_governance/2025/Mar/07/NVIDIA-Corporate-Governance-Policies-March-3-2025-068bb7.pdf ；https://s201.q4cdn.com/141608511/files/doc_governance/2025/Mar/07/NVIDIA-NCGC-Charter-March-3-2025-a0052c.pdf
- 2026-11-12 新闻稿："Harvey C. Jones Appointed First-Ever Chair of the Board"（见主简报一手材料 2）。也就是说，**英伟达是在危机中才第一次把董事长和 CEO 分设**，此前既没有董事长，CEO 与首席独立董事并存。
- 现状（CNBC 2026-11-13，引述董事会）："We are in the process of selecting a search firm for the Nvidia CEO role"；"We have not formally engaged any potential candidates."；"Any speculation regarding individual candidates, whether internal or external, is premature." https://www.cnbc.com/2026/11/13/nvidia-huang-ceo-replacement-search.html

**3）股权结构：单一股权，创始人持股 3.58%**
- 10-K 封面只登记一类股票："Common Stock, $0.001 par value per share NVDA The Nasdaq Global Select Market"（FY2026 10-K）。委托书："stockholders have one vote for each share"。
- 委托书持股表（截至 2026-03-23）："Jen-Hsun Huang 870,604,104 … 3.58%"；全体董事和高管合计 3.94%；BlackRock 7.43%，Vanguard 7.31%。（2026 年委托书）
- 意义：与 Meta、Alphabet 那种双重股权不同，**英伟达董事会有实际的去留决定权**。黄仁勋在 11-11 前还是董事，但只占一个席位。

**4）员工关系政策：公开 Code of Conduct 没有明文的「恋爱禁令」**
- 英伟达公开的 Code of Conduct（©2023）在利益冲突一节列出可能构成冲突的情形，其中包括 "Investments or personal relationships"，并要求 "If involved in a situation that could present a perceived or actual conflict of interest, contact Employment Legal for guidance"。它提到内部有 "Conflict of Interest Policy" 和 "Outside Activities-Conflict of Interest Preapproval Process"，但这两份未公开。https://images.nvidia.com/aem-dam/en-zz/Solutions/about-us/NVIDIA-Code-of-Conduct-External.pdf
- **尚不清楚**：英伟达内部有没有类似 Intel「non-fraternization policy, which applies to all managers」那样的条款，以及是否要求申报与下属的关系。公开文件看不出来。

**5）Semafor 的说法与我们的核对有冲突**
- Semafor（2026-11-09，Liz Hoffman、Andrew Edgecliffe-Johnson）："The word "succession" appears nowhere in its most recent annual report to shareholders, versus 25 times for Microsoft and 16 for Alphabet."；"The average Nvidia board member has been there almost 15 years"；"Nvidia's lead director is a 77-year-old former law-firm executive." https://www.semafor.com/article/11/09/2026/with-a-weak-board-and-no-successor-nvidia-confronts-a-governance-crisis
- **冲突**：我们核对的 FY2026 10-K 里「succession」出现了 1 次（风险因素段）。如果 Semafor 指的是委托书或另行印发的年报册子，「零次」可能成立；如果指 10-K，就不准确。片中建议说「英伟达的委托书和董事会治理政策里都没有出现 succession 一词，10-K 只在风险因素里提过一次」，这一说法我们已逐字核对。

### B. 继任计划是董事会的职责：监管层的表态（一手）

- SEC 公司金融部 Staff Legal Bulletin No. 14E（2009-10-27）："One of the board's key functions is to provide for succession planning so that the company is not adversely affected due to a vacancy in leadership. Recent events have underscored the importance of this board function to the governance of the corporation. We now recognize that CEO succession planning raises a significant policy issue regarding the governance of the corporation that transcends the day-to-day business matter of managing the workforce." https://www.sec.gov/interps/legal/cfslb14e.htm
  - 含义：从 2009 年起，SEC 工作人员不再允许公司以「日常经营事务」为由，把股东要求披露 CEO 继任计划的提案排除出投票。这份公告发布于苹果病假争议同一年（文中的「Recent events」具体指什么，原文没说）。
- 先例里写明「有继任计划」的一手原文：Boeing 2005 "The Board has a robust succession planning process in place"；Lockheed 2012 "a robust succession plan that allowed the board and me to react quickly"；Apple 2011 "execute our succession plan"。英伟达 2026-11-12 的新闻稿则写 "The Board is initiating a search for a permanent Chief Executive Officer"。

### C. 「CFO 临时兼任 CEO」是常见的应急安排（一手文件归纳）

| 公司 | 临时 CEO | 是否兼任 CFO | 是否参选正式 CEO | 结果 |
|---|---|---|---|---|
| Boeing 2005 | CFO James Bell | 是（"will continue in this role"）| 否（"not a candidate"）| 外聘 McNerney |
| HP 2010 | CFO Cathie Lesjak | 是 | 否（"taken herself out of consideration"）| 外聘 Apotheker，不到一年离任 |
| Intel 2018 | CFO Bob Swan | 是 | 是 | 2019-01 转正 |
| BP 2023 | CFO Murray Auchincloss | 新闻稿未写 | 是 | 2024-01 转正 |
| NVIDIA 2026 | CFO Colette Kress | 是（"will continue in that role"）| 新闻稿只说「内外部候选人」，未说明她是否参选 | 待定 |

（我们的判断：这是董事会在没有指定接班人时最常用的安排。它只说明「应急」，不说明「有计划」。）

### D. 员工恋爱 / 汇报关系政策：先例中的写法

- Intel：「non-fraternization policy, which applies to all managers」（AP 转述）
- Boeing：对方「did not report directly to him」，仍判定违反 Code of Conduct
- Lockheed：「close personal relationship with a subordinate employee」，违反 Code of Ethics and Business Conduct
- McDonald's：「violated company policy」（2019）；后查出与另外三名员工有关系，并「lied to the Company and the Board」（2020）
- BP：关系本身在 2022 年被认定「No breach」，问题出在「not fully transparent」「knowingly misled the board」
- HP：「no violation of HP's sexual harassment policy, but did find violations of HP's Standards of Business Conduct」

（我们的判断：先例的共同点是，董事会处理的往往不是「谈恋爱」本身，而是**利益冲突、汇报关系和对董事会是否坦白**。最终代价最大的两案，McDonald's 和 BP，都是因为不坦白。）

---

## 四、对照：本次与先例的异同（只写有依据的）

**相似之处**
1. **8-K 不写原因，新闻稿或员工信另说**：Intel 2018 与英伟达 2026 的 8-K 都只写辞职和临时安排（两份 8-K 原文）。
2. **CFO 临时兼任 CEO，同时启动内外部搜寻**：Boeing、HP、Intel、BP 都是这样，英伟达也是。
3. **董事会强调业务照常**：Boeing "in no way related to the company's operational performance"；HP "not related in any way to the company's operational performance"；McDonald's "unrelated to the Company's operational or financial performance"；英伟达 Jones："we expect the company's operations, customer commitments and product roadmap to continue without interruption"。
4. **关系涉及员工或下属**：Lockheed（下属）、Intel（员工）、McDonald's（员工）。英伟达的第二段关系据 NYT 报道是向其汇报的高管（**报道称，未证实**；片中不点名）。

**不同之处**
1. **创始人身份与任期**：除 Apple 和 Uber 外，上述先例都是职业经理人。黄仁勋是联合创始人，任 CEO 33 年（新闻稿 "the extraordinary foundation Jensen created over the last 33 years"）。学术上，创始人 CEO 溢价（Fahlenbrach）和「越来越重视 CEO」（Quigley 等）都意味着冲击可能更大。
2. **叠加国家安全层面**：上述先例**都没有**「外国情报工作」的指控。英伟达董事会 11-08 声明称 "recent reporting that founder and CEO Jensen Huang has been the target of a foreign intelligence effort"，并说 "the Board has no reason to believe that either national security or NVIDIA secrets were compromised"（**报道称有情报指控；董事会说没有理由认为机密泄露；未证实**）。这在我们检索到的先例中没有对应，也是本次事件真正的新东西。
3. **没有事先指定的接班人**：Apple 2011 和 McDonald's 2019 当场换上正式 CEO，市场反应温和（-0.65%；约 -2.7% 至 -3%）。英伟达截至 11-13 还在选猎头公司（CNBC）。Lockheed、Boeing 都在新闻稿里强调「robust succession plan」，英伟达的治理文件里找不到这个词。
4. **单一股权、董事会有权**：不同于 Uber 2017 年（非上市、靠投资人联名施压），英伟达董事会依自身权力接受了辞职（8-K："the Board … accepted the resignation"）。
5. **公司处在业务高点**：Intel 2018 年业务已承压。英伟达的业务状况由其他角度提供；24/7 Wall St. 的文章也做了这一对比（二手）。
6. **市值体量**：先例里市值最大的是 2011 年的苹果（非关联方持股市值约 3229 亿美元）。英伟达是数万亿美元级的公司（具体数字见主简报和市场角度），一次 4% 的下跌，绝对金额远超任何先例。这一条是我们的判断，数字由市场角度核对。

**可以留在长期认知里的道理**（我们的判断，供论点组使用）：
> 关键人物风险不在于这个人会不会出事，而在于他出事那天，董事会手里有没有一个名字。

依据：Apple 2011、Lockheed 2012、McDonald's 2019 手里有名字，市场反应小；HP 2010 只有临时安排，外聘接班人很快失败；英伟达的 10-K 承认「highly dependent」，但治理文件里没有继任计划。

---

## 台账候选

| # | claim（中文） | source | quote（原文） | status |
|---|---|---|---|---|
| 1 | 英伟达 FY2026 10-K 的风险因素说公司高度依赖长期在任的高管团队，未单独点名黄仁勋 | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm | "Additionally, we are highly dependent on the services of our longstanding executive team. Failure to ensure effective succession planning, transfer of knowledge, and smooth transitions involving executives and key employees could hinder our strategic planning, execution, and long-term success." | 已证实 |
| 2 | 英伟达 2026 年委托书说董事会设首席独立董事而不设董事长 | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000036/nvda-20260512.htm | "by having an independent Lead Director, rather than a chairperson" | 已证实 |
| 3 | 英伟达 2026 年委托书全文没有出现 "succession" 一词 | 同上 | （检索结果，无原文可引；仅有 "until his or her successor is elected"）| 已证实（我们的全文检索） |
| 4 | 英伟达董事会治理政策只要求定期听取「高管培养」汇报，没有写继任计划 | https://s201.q4cdn.com/141608511/files/doc_governance/2025/Mar/07/NVIDIA-Corporate-Governance-Policies-March-3-2025-068bb7.pdf | "Senior Management Development. The Board shall receive and review periodic updates on the Company's senior management development." | 已证实 |
| 5 | 黄仁勋持股 3.58%（截至 2026-03-23），公司只有一类普通股，每股一票 | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000036/nvda-20260512.htm | "Jen-Hsun Huang 870,604,104 … 3.58%"；"stockholders have one vote for each share" | 已证实 |
| 6 | Semafor 称英伟达最新年报中「succession」一次都没出现；我们核对 10-K 有一次 | https://www.semafor.com/article/11/09/2026/with-a-weak-board-and-no-successor-nvidia-confronts-a-governance-crisis | "The word "succession" appears nowhere in its most recent annual report to shareholders" | 有争议 |
| 7 | 2011 年乔布斯辞职信建议执行既定继任计划，由 Cook 接任 | https://www.apple.com/newsroom/2011/08/24Letter-from-Steve-Jobs/ | "I strongly recommend that we execute our succession plan and name Tim Cook as CEO of Apple." | 已证实 |
| 8 | 乔布斯辞职次日苹果收跌 0.65%，同日道指和标普分别跌 1.51% 和 1.52% | https://fortune.com/2011/08/25/wall-street-shrugs-off-steve-jobs-resignation/ | "Apple loses 0.65%"；"the Dow and the S&P 500 fell 1.51% and 1.52%, respectively" | 已证实（二手） |
| 9 | 2009 年乔布斯先称「荷尔蒙失衡」、治疗简单，九天后改口并休病假 | https://www.apple.com/newsroom/2009/01/05Letter-from-Apple-CEO-Steve-Jobs/ ；https://www.sec.gov/Archives/edgar/data/320193/000118143109003017/rrd229456_27079.htm | "a hormone imbalance"；"relatively simple and straightforward"；"my health-related issues are more complex than I originally thought" | 已证实 |
| 10 | 2009-01-14 苹果盘后跌 7.3% | https://www.mprnews.org/story/2009/01/14/stevejobs_health | "Apple's shares slid $6.19, or 7.3 percent, to $79.14 in after-hours trading." | 已证实（二手，AP） |
| 11 | Intel 2018 年 8-K 只写辞职和 CFO 临时兼任，没写原因 | https://www.sec.gov/Archives/edgar/data/50863/000119312518199045/d598882d8k.htm | "the Board appointed Robert ("Bob") H. Swan … to serve as interim Chief Executive Officer … Mr. Swan also continues to serve as CFO" | 已证实 |
| 12 | Intel 称 Krzanich 违反适用于所有经理的反亲密关系政策 | https://www.cbsnews.com/sacramento/news/intel-ceo-resigns-brian-krzanich/ | "in violation of the company's non-fraternization policy, which applies to all managers"（AP 转述） | 已证实（二手；新闻稿原文链接失效） |
| 13 | Intel 当日收跌 2.4%，报 52.19 美元 | 同上 | "closed down 2.4 percent at $52.19" | 已证实（二手，AP） |
| 14 | McDonald's 2019 年以「与员工的两厢情愿关系」违反公司政策为由让 Easterbrook 离职，并当即任命正式 CEO | https://www.sec.gov/Archives/edgar/data/63908/000089882219000080/pressrelease1.htm | "violated company policy and demonstrated poor judgment involving a recent consensual relationship with an employee" | 已证实 |
| 15 | McDonald's 2020 年称 Easterbrook 对公司和董事会说谎、销毁信息，另与三名员工有性关系 | https://www.sec.gov/Archives/edgar/data/63908/000089882220000056/mcd8k.htm | "lied to the Company and the Board and destroyed information … sexual relationships with three additional Company employees" | 已证实（公司指控，后以和解结案） |
| 16 | Easterbrook 和解退回价值逾 1.05 亿美元的股权和现金 | https://www.sec.gov/Archives/edgar/data/63908/000006390821000042/exhibit991-12162021.htm | "returned equity awards and cash, with a current value of over $105 million" | 已证实 |
| 17 | SEC 2023 年对 Easterbrook 处五年任职禁令和 40 万美元罚款 | https://www.sec.gov/news/press-release/2023-4 | "five-year officer and director bar and a $400,000 civil penalty" | 已证实（当事人不承认也不否认） |
| 18 | HP 2010：Hurd 未违反性骚扰政策，但违反商业行为准则；CFO 临时任 CEO | https://www.sec.gov/Archives/edgar/data/47217/000104746910007177/a2199755zex-99_1.htm | "no violation of HP's sexual harassment policy, but did find violations of HP's Standards of Business Conduct" | 已证实 |
| 19 | HP 首个交易日市值约蒸发 90 亿美元（原约 1080 亿）/ 另一说为 100 亿美元、约 10% | https://www.nbcnews.com/id/wbna40758517 ；https://knowledge.insead.edu/leadership-organisations/mark-hurd-affair | "dropped about $9 billion in the stocks' first day of trading"；"HP's market value fell by $10 billion, close to a 10 per cent decline" | 有争议（两数并列） |
| 20 | Boeing 2005：对方不直接向 CEO 汇报，董事会仍要求其辞职 | https://www.sec.gov/Archives/edgar/data/12927/000119312505046669/dex991.htm | "a female executive of the company who did not report directly to him"；"the CEO must set the standard for unimpeachable professional and personal behavior" | 已证实 |
| 21 | Lockheed 2012：候任 CEO 因与下属的关系辞职，公司称有「robust succession plan」，当天任命接班人 | https://www.sec.gov/Archives/edgar/data/936468/000119312512463676/d436152dex991.htm | "close personal relationship with a subordinate employee"；"a robust succession plan that allowed the board and me to react quickly" | 已证实 |
| 22 | BP 2023：Looney 承认对过往关系披露不完整 | https://www.sec.gov/Archives/edgar/data/313807/000165495423011775/a2297m.htm | "he now accepts that he was not fully transparent in his previous disclosures" | 已证实 |
| 23 | BP 认定 Looney 故意误导董事会并解雇，没收及追回薪酬合计最高 3243 万英镑 | https://www.sec.gov/Archives/edgar/data/313807/000165495423015466/a6931w.htm | "knowingly misled the board"；"The total maximum value of the potential remuneration that has been forfeited or clawed back is £32,426,000" | 已证实 |
| 24 | Uber 2017：Kalanick 称接受投资人要求让位 | https://techcrunch.com/2017/06/20/uber-ceo-travis-kalanick-resigns/ | "I have accepted the investors request to step aside" | 已证实（二手，NYT 获得声明） |
| 25 | SEC 2009 年表态：CEO 继任计划是董事会关键职能，属于重大公司治理议题 | https://www.sec.gov/interps/legal/cfslb14e.htm | "One of the board's key functions is to provide for succession planning so that the company is not adversely affected due to a vacancy in leadership." | 已证实 |
| 26 | 研究：240 起 CEO 猝死样本显示，1950–2009 年市场反应幅度显著变大 | https://doi.org/10.1002/smj.2504 | "absolute (unsigned) market reactions to these events in U.S. public firms have increased markedly between 1950 and 2009" | 已证实（文献摘要） |
| 27 | 研究：任期超过 10 年且过去三年表现差的高管猝死，股价反而上涨 6.8% | https://doi.org/10.1016/j.jbankfin.2009.09.002 | "the reaction is strongly positive (6.8%) if: (1) the executive's tenure exceeds 10 years, and (2) abnormal stock returns over the last three years are negative" | 已证实（文献摘要） |
| 28 | 研究：CEO 住院会显著影响盈利和投资，应急预案有价值 | https://doi.org/10.1111/jofi.12897 | "CEOs have a significant effect on profitability and investment"；"CEO contingency plans are valuable." | 已证实（文献摘要，丹麦样本） |
| 29 | 研究：1993–2002 年投资创始人 CEO 公司每年超额收益 8.3%，控制变量后 4.4% | https://doi.org/10.1017/S0022109009090139 | "a benchmark-adjusted return of 8.3% annually … the abnormal return is still 4.4% annually" | 已证实（文献摘要） |
| 30 | 研究：高管私德问题会造成公司财富缩水、失去合作方、更多诉讼与调查，且多发于治理差的公司 | https://doi.org/10.1016/j.jfineco.2017.11.008 | "companies of accused executives experience significant wealth deterioration, reduced operating margins, and lost business partners"；"Indiscretions occur more often at poorly governed firms" | 已证实（文献摘要） |
| 31 | 英伟达董事会截至 11-13 还在选猎头公司，尚未正式接触候选人 | https://www.cnbc.com/2026/11/13/nvidia-huang-ceo-replacement-search.html | "We are in the process of selecting a search firm for the Nvidia CEO role"；"We have not formally engaged any potential candidates." | 已证实（董事会对 CNBC 的声明） |
| 32 | 有现成接班人的先例市场反应小，只有临时安排的先例风险更大 | 综合 #7 #8 #14 #18 #21 | — | 我们的判断 |
| 33 | 本次的国家安全层面在我们检索到的 CEO 丑闻先例中没有对应 | 综合第一节 | — | 我们的判断 |

---

## 尚不清楚 / 冲突

**冲突**
1. **Semafor 说「succession」在年报中一次都没出现，我们查 FY2026 10-K 有一次**（风险因素段）。委托书和治理政策确实没有。片中建议用我们核对过的说法。
2. **HP 2010 的市值损失**：AP 说首日约 90 亿美元，INSEAD 说约 100 亿美元、近 10%；另有报道称最高达 150 亿美元、累计跌 14%（检索摘要，未核对原文）。
3. **McDonald's 2019-11-04 的跌幅**：2.7%（24/7 Wall St.，收盘口径）、最多 2.9%（Bloomberg，盘中）、3% 至 187.60 美元（AP，午后）。
4. **BP 2023-09-13 的跌幅**：开盘最多 -1.8%，收盘 -2.7% 或「近 3%」，HL 称 -1.1%（时点不明）。
5. **苹果 2011-08-24 盘后跌幅**：约 5%（CNN Money）、5.22%（Fortune）、5.5% 至 355.76 美元、最多 7%（各家检索摘要，均未逐字核对）。
6. **BP 追回金额**：媒体出现「不到 100 万英镑」和「180 万英镑」两种说法。BP 一手公告中真正属于「追回」的两项税后合计约 94.9 万英镑；3243 万英镑是包括自动没收在内的最高总值。
7. **24/7 Wall St. 的一年期回报数字**（Intel -8.7%，McDonald's +14.7%）没有注明数据源，我们无法独立复算（Stooq 有反爬验证，本次没有绕过）。

**尚不清楚**
1. 英伟达内部有没有「与下属恋爱须申报 / 禁止」的条款。公开 Code of Conduct 只把 "personal relationships" 列为可能的利益冲突。
2. 英伟达董事会在此之前有没有**未公开的**紧急继任预案。公开文件找不到；Forbes 称黄仁勋「据报道不相信继任计划」（Forbes 2026-11-12 Edward Segal 的文章，抓取被拒 403，原话和出处未见）。
3. Kress 是否参选正式 CEO。新闻稿只说 "will consider internal and external candidates"。
4. 黄仁勋离任的薪酬与股权处理（是否按「有因」解雇）。8-K 未写。McDonald's 一案说明，这一点日后可能成为 SEC 关注的重点（McDonald's 正是因未披露「无因」处理的裁量而被认定违规）。
5. SEC 对苹果 2009 年健康披露的审查有无结论。未见公开执法记录。
6. 1985 年苹果股价「涨 1 美元」只见 TIME 的转载，原刊未核对，也没有百分比。
7. Boeing 2005、Lockheed 2012 的当日股价没有查到。
8. **未核实、未写入正文的线索**（检索额度用尽）：Nestlé 2025 年以「与直接下属的未披露恋爱关系」解雇 CEO Laurent Freixe；Kohl's 2025 年 CEO Ashley Buchanan 因利益冲突被解职；Best Buy 2012（Brian Dunn）。这些都与本次有可比性，建议事实核查或补充检索时补齐，并优先找一手公告。
9. 学术文献 Johnson, Magee, Nagarajan & Newman (1985) 和 Worrell 等 (1986) 的结论没有取得摘要，正文只列书目，不能在片中引用其结论。
10. 交易所规则：NYSE 上市公司手册 303A.09 据我们所知要求公司治理准则涉及 management succession（含紧急情况）。**本次未取得原文**，而且英伟达在 Nasdaq 上市，不适用 NYSE 规则，片中不要用。
