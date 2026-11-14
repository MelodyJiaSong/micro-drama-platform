# 事实核查意见 R1：t01_faa_ground_stop

- 核查日期：2026-11-14（片中口径仍为「截至 2026 年 11 月 14 日」）
- 核查人：独立上下文事实核查员（Claude）。没有参与写档案；只核对，不润色。
- 核查对象：`research/dossier.md`、`claims.json`（44 条）、`research/angles/*.md`（重点读了 history.md、cause.md）
- 方法：逐条用 WebFetch 打开 claims.json 给的 source 读原文；source 不含所引内容时另找出处。WebSearch 用了 8 次（上限 15 次）。
- 没有调用任何收费服务，没有下载图片或视频。DOT 监察长 2010 年的 PDF 信件（文本文件）经 WebFetch 取回，在 scratchpad 里本地解析成文字后逐字核对。
- 没能直读：faa.gov 声明页、ATCSCC Advisory 111、Duffy 与 FAA 的 X 帖原帖、白宫记者会视频、CNN 直播（HTTP 451）。这几项只能核到「媒体逐字转引」这一层。
- 本文件不改 `claims.json`、`dossier.md`，修改由作者按第 4 节执行。

---

## 1. 总结论

1. **事实底座大体可靠，但引语一致性不过关。** 44 条里 25 条通过（含带小注或未能核子项的），**19 条需改**，3 条只能部分核实（有子项未能核）。没有需要整条删除的条目。需改的主要问题是：quote 不是原文（转述冒充原话）、source 指错（引语根本不在所给页面上）、个别事实细节写错。
2. **论点 A 最关键的历史先例（C35，2009 年 FTI 全国中断）这次核实了，而且比档案写的更有力。** DOT 监察长信件 CC-2010-012（2010-06-17）原文写明：故障发生在 Harris 把 FTI 的 IP 业务**从旧网迁到新光纤网**的过程中，根因是新旧网之间一台**临时过渡路由器**的配置错误，被复制进新上线的路由器后触发。C35 可以从「有争议」升为「已证实」，但细节要改：出错的路由器在**洛杉矶中心**，不在盐湖城。
3. **论点 A 站得住，但要收窄措辞，并在片中承认反例。** 能确认属于「改动、迁移、维护时出事」的先例有：2009 FTI 迁移、2015 华盛顿中心 ERAM 软件升级（档案漏了，建议补）、2023 NOTAM 维护时误删文件。2014 年 ERAM 属于「新系统的潜伏缺陷」，不是「动它的时候」。2025 达拉斯、2026-09 费城、2025 纽瓦克、2004 洛杉矶中心都**不是**改动引发，是反例或属于论点 B。C43 把达拉斯、费城算进「改动时出事」的依据，这是错的。
4. **新进展：截至 11-14，没有查到官方根因、初步报告，也没有查到已排期的国会听证。** 只有 Cantwell 说商务委员会会「审查」（ABC）。补充一个新口径：NBC 正文终版（11-13 22:19 更新）写「逾 7,000 班取消」，比档案列的所有数字都高。

---

## 2. 逐条表

结论：**通过** / **需改** / **未能核** / **删除**。原文一律照录英文。

| id | 结论 | 原文或更正 | 依据 URL |
|---|---|---|---|
| C01 | 通过 | NBC："The sudden and stunning alert was issued at 3:54 p.m. ET" / "due to extraordinary circumstances and for reasons of safety"。Advisory 111 原文仍未直读 | https://www.nbcnews.com/news/us-news/faa-orders-nationwide-ground-stop-departing-flights-reasons-safety-rcna609247 |
| C02 | **需改** | quote **不在 CBS 页面上**（CBS 没有引公告原文，也没提国际航班）。这段文字出自 Newsweek："by order of the federal aviation command center, all airports are ground stopped" / "All departing traffic should remain ground stopped until further notice." / "Inbound international flights will be managed on a case by case basis"。注意：「Federal Aviation Command Center」不是正式机构名（正式名是 ATCSCC），疑为管制广播或转述，须对照 Advisory 111 原文。「国际航班逐案处理」另有 FAA X 帖可佐证（NBC 17:52 条）："Every flight has been accounted for, and international flights will be handled on a case by case basis" | https://www.newsweek.com/faa-nationwide-ground-stop-airports-air-traffic-control-12713904 ；NBC 直播 |
| C03 | 通过 | CBS："At 8:15 tonight, Eastern time, we've opened up the airspace," Duffy said。NBC、CNBC 都写 FAA 在 8:15 p.m. ET 解除；The Register 写约 8:30 PM；Scripps 写「shortly after 8 p.m.」。「4 小时 21 分」是我们自己算的，标注保留 | https://www.cbsnews.com/news/faa-issues-nationwide-ground-stop/ |
| C04 | 需改（小） | Duffy quote 逐字无误（NBC 20:44 条）。但：① 飞机数各家写法是「over / more than 3,500」（NBC 正文、USA Today、Scripps），NBC 直播写「around 3,500」，建议说「3,500 多架」；② 15:36 的出处不一：NBC 直播写成「the ground stop was called at 3:36 p.m.」（把起始时刻当成停飞时刻，是错的），Scripps 把 3:36 归给**匿名管制员**，Fox、USA Today 归给 Duffy。建议写「据 Duffy 和一名管制员的说法，15:36 前后开始不稳定」；③ Scripps 引 Duffy："More than 3,500 flights were airborne at the time of the stop, and all safely landed"，可用 | https://www.nbcnews.com/news/us-news/live-blog/live-updates-flights-grounded-faa-communications-outage-rcna609268 ；https://www.scrippsnews.com/us-news/faa-issues-nationwide-ground-stop-on-us-air-traffic |
| C05 | **需改** | 换成原文。ABC："According to Flightradar24, there were 3,100 airborne aircraft bound for U.S. airports earlier amid nationwide ground stop." CBS："about 3,100 airborne aircraft bound for U.S. airports when the ground stop began"。NBC 正文（4,042 已确认，出自 Flightradar24）："When the FAA issued the alert, 4,042 flights headed for U.S. destinations were airborne"。注意 NBC 直播页**没有** 4,042，只在 NBC 正文里有 | ABC 138121848；CBS；NBC rcna609247 |
| C06 | 需改 | 数字无误，quote 换成原文。Fox："As of the latest available figures, FlightAware reported 4,467 U.S.-related cancellations and 10,079 delays." / "Globally, the website recorded 5,141 cancellations and 26,196 delays." ① Fox 只有相对时间戳（「2 hours ago」），「约晚 9 点」核不出，建议写「当晚」；② 口径表补一条：NBC 正文终版（22:19 更新）写「after more than 7,000 flights were canceled」，没写数据来源；③ ABC 正文 18:20 时是「more than 2,000」，「近 5,000（ABC）」在我读到的两个 ABC 页面上都没找到 | https://www.foxnews.com/live-news/faa-issues-nationwide-ground-stop-cites-communications-issue ；NBC rcna609247 |
| C07 | **需改** | quote 是拼接的，不是原文。NBC 直播 20:20 条原文："upwards of 5,300 flights have been canceled" / "Most days this week saw about 100 flight cancelations into and out of the U.S."。claim 里的「11-13 截至 20:20」对 | NBC 直播 |
| C08 | 通过 | CNBC："There were 11,000 flights scheduled to depart U.S. airports after 4 p.m. ET on Friday, according to flight-data firm Cirium, with 1.5 million passengers." / "There were about 600 diverted flights on Friday"。Airways 的 827 这次没核 | https://www.cnbc.com/2026/11/13/faa-ground-stop.html |
| C09 | 通过 | NBC 直播 17:52 条逐字一致。**dossier 时间线要改**：FAA X 帖是 17:52 条，不是「约 17:00–17:45」 | NBC 直播 |
| C10 | 通过 | CNBC 引 FAA："impacting multiple Air Route Traffic Control Centers"。Scripps 全文引 Duffy X 帖："...following a communication issue impacting all Air Route Traffic Control Centers"。**dossier 时间线要改**：NBC 直播收录 Duffy X 帖的是 17:20 条，「16:16」没能核实 | CNBC；Scripps；NBC 直播 |
| C11 | 通过（注明） | 与 CBS 的叙述一致："...leading to a crash and a communications outage," according to multiple sources；"The system is operated by L3Harris, which did not immediately respond to CBS News' request for comment."。这句 quote 是 **CBS 的叙述句，不是信源原话**，片中不要放进引号当某人说的。MS NOW、彭博未能核 | CBS |
| C12 | **需改** | quote 逐字无误（NBC 20:51 条），但 Duffy 原话还有一句："We have TDM telecoms, so this is analog telecom"。**claim 写「老旧的模拟（TDM）电信」是技术错误**：TDM（时分复用）是数字传输技术，不是模拟。片中只能说「Duffy 称之为模拟电信」，或直接说「老式 TDM 专线」，不要用旁白认定 TDM 是模拟。claim 的后半句「输出不一致的数据，于是关闭系统」在 NBC 页面上没找到，**未能核**，要么补出处，要么删掉 | NBC 直播 |
| C13 | 通过（小注） | ABC 直播逐字："We use 1980s little copper lines." / "It's an old system that went down and went down everywhere." / "By the way, all of the new equipment that we put in, none of that went down."。中间的「It got overloaded.」在 ABC 页面上没找到（angles 文件说出自 Yahoo），省略号拼接时要注明出处 | https://abcnews.com/US/live-updates/faa-ground-stop-live-updates-hundreds-flights-canceled/?id=138125140 |
| C14 | 通过 | NBC 直播 20:44 条逐字一致 | NBC 直播 |
| C15 | 需改（note） | Globe and Mail 21:29 条：「patches」是转述，"new equipment and new technology was overwhelming the older system" 是原话，逐字一致。**note 要改**：IBTimes/Yahoo（转 Reuters）里没有「buckle」这个词，原文是 "the introduction of newer technology into the older system had overwhelmed it"（转述） | https://www.theglobeandmail.com/world/article-faa-ground-stop-us-flights-live-updates/ ；https://www.yahoo.com/news/us/articles/faa-lifts-nationwide-ground-stop-020705860.html |
| C16 | 需改（note） | 主 quote 通过（ABC 138121848："This isn't another 9/11. I cannot repeat that enough,"）。Scripps "We have seen zero evidence that this was a cyberattack" 通过。**note 里「It appears that this was mechanically driven...」在两个 ABC 页面上都没有找到**，未能核，进讲稿前要找到原出处，找不到就删 | ABC；Scripps |
| C17 | **需改** | 前半句通过。SciAm："As of November 10, it was deployed across all 22 air traffic regions in the country."。**ASI 声明不在 SciAm 页面上**，出处改成 USA Today（经 Yahoo）："The current ground stop is not based on or a result of the SMART system"。note 里的 Mullin「You just can't rule out anything at this point」没能核到；USA Today 的原话是 "We're not ruling anything out at this point." | https://www.scientificamerican.com/article/faa-grounds-all-u-s-flights-days-after-expanding-its-ai-air-traffic-system/ ；https://www.yahoo.com/news/us/articles/faa-orders-nationwide-groundstop-us-211917033.html |
| C18 | 通过（补 note） | **500 亿是 Duffy 的要价**：ABC 直播逐字 "I want Congress to give us emergency funding." "This is bipartisan." "I want $50 billion."（Duffy）；Globe and Mail 20:56 条也归给 Duffy；Scripps 同。IBTimes/Yahoo 另写 "Mullin estimated that a complete overhaul could cost approximately $50 billion."（转述）。片中说法：「Duffy 当晚要求国会紧急拨款 500 亿美元」，不必提 Mullin。另注：Scripps 同一篇里还写 Duffy 说要 "another $30 billion to complete the work"，与 500 亿并存，提到总价时要说明口径不一 | ABC 直播；Globe；Scripps |
| C19 | 通过 | USA Today/Yahoo："You will have more of these. You will have more of them, unless the American people and in Congress tell us to build," Duffy said.。注意原文是「and in Congress」，history.md 里的「and the Congress ... and I can't wait for that」与此不一致，以本句为准；CNBC "It's going to continue to fail" 通过 | Yahoo 211917033；CNBC |
| C20 | 通过 | GAO："In July 2025, Congress appropriated $12.5 billion to support BNATCS..."。quote 截短无妨 | https://www.gao.gov/products/gao-26-107992 |
| C21 | 通过 | Roll Call 逐字一致；2025-07-16，众议院运输与基础设施委员会听证 | https://rollcall.com/2025/07/16/duffy-air-traffic-control-overhaul-to-cost-31-5-billion/ |
| C22 | 通过（补口径） | GAO-24-107001 逐字："The assessment determined that of its 138 systems, 51 (37 percent) were unsustainable" / "54 (39 percent) were potentially unsustainable"；2024-09-23。补充：① 这是 **FAA 自己的可持续性评估**，GAO 报告并引用（「The assessment determined」），片中说「GAO 引 FAA 自评」更准；② 17 个特别令人担忧的系统：本报告说至少 6 年、有的 10–13 年；GAO-25-108162 说「at least 6 to 10 years away」，两处口径不同 | https://www.gao.gov/products/gao-24-107001 ；https://files.gao.gov/reports/GAO-25-108162/index.html |
| C23 | 通过 | GAO-26-107992 逐字一致；2026-09-14 | GAO-26-107992 |
| C24 | 通过 | "as of May 2026, FAA reported replacing 2,560 of 5,170 old and frail copper wires"。数字是 **FAA 报告给 GAO 的**。DOT 的「69%」仍未核 | GAO-26-107992 |
| C25 | 需改（note） | Register "more than 4,400 facilities" 通过。**note 错了**：35 亿美元是 FTI 合同的**上限**（ceiling），不是中标金额。OIG 原文："The contract has a current maximum value of $1.4 billion and a ceiling amount of $3.5 billion"；合同 2002 年 7 月授予，本质是一份 2017 年到期的 15 年租约。另：Washington Technology 2023-03 报道 FTI 合同 2023 年 4 月底到期、需要延期，也就是说本次出事的是一张**靠延期合同运行的过渡期网络**（对论点 A 有用） | https://www.theregister.com/offbeat/2026/11/13/faa-lifts-ground-stop-after-hours-long-delays-snag-travelers/5309912 ；OIG CC-2010-012；https://washingtontechnology.com/companies/2023/03/faa-selects-verizon-24b-telecommunications-contract/384517/ |
| C26 | 通过 | L3Harris 2026-05-11："'build-then-switch' approach – installing new infrastructure while the old system runs"；"on track for completion in 2027"；"150-200 new network paths each month"。页面**没有**「99.999%」，dossier 第 6 节这条传言可以划掉 | https://www.l3harris.com/newsroom/editorial/2026/05/l3harris-reaches-over-50-faa-telecommunications-modernization |
| C27 | 通过 | Aviation Week（2026-08-27）逐字一致。Washington Technology（2023-03-28）："awarded Verizon the $2.4 billion recompete"。Nextgov（2026-08-14）："initial $74.3 million task order"、"a minimum of 22 months"、"impossible to meet"、"December 2028 operational deadline" | Aviation Week；Washington Technology；https://www.nextgov.com/modernization/2026/08/faa-brings-t-network-modernization-program/415417/ |
| C28 | 通过 | Airways 引 CNN，逐字一致（2026-09-21 事件报道） | https://airwaysmag.com/new-post/faa-northeast-ground-stops-severed-fiber-philadelphia-tracon |
| C29 | 通过（限定） | USA Today/Yahoo 逐字一致。限定为「委员会这样说」；事实本身没有用 FAA 设施资料核（例如夏威夷、阿拉斯加的设施是否例外），片中不要当成我们自己核过的事实 | Yahoo 211917033 |
| C30 | 通过 | USA Today："The safety of our skies is built on redundancies."；ABC 正文同 | ABC；Yahoo |
| C31 | 需改 | 结论（9·11 以来第二次）可用，quote 换原文。ABC："The nationwide ground stop was only the second since 9/11."。Scripps 也写上一次是 2023 年 1 月、再上一次是 9·11 之后。AP、NPR、新华社、Wikipedia、澎湃、TVBS 这次**未能核**。注意 CBS 页面没有「second」一词，只有 Sumwalt 的 "There was one back in 2023 for just a few hours"。Reuters「9·11 以来最长」经 IBTimes 核到："longest nationwide grounding since the Sept.11, 2001, terrorist attacks" | ABC 138121848；Scripps；Yahoo 020705860 |
| C32 | 通过 | 9/11 委员会报告第 1 章逐字一致：9:25 全国停飞，Sliney 的落地令，"about 4,500 commercial and general aviation aircraft soon landed without incident" | https://govinfo.library.unt.edu/911/report/911Report_Ch1.htm |
| C33 | 需改（小） | 数字对，quote 换原文："To ensure safety, FAA grounded all departing aircraft for about 2 hours to fix the system." / "The outage caused over 1,300 flight cancellations and almost 10,000 flight delays throughout the day."。**对论点 A 要注意**：同一份 GAO 证词把这次停飞归为 "the outage of an aging air traffic control (ATC) system"，并说 NOTAM 系统 "over 30 years old"，没有提承包商删文件 | https://files.gao.gov/reports/GAO-25-108162/index.html |
| C34 | 通过 | 逐字一致；出自 FAA 的「preliminary review」，2023-01-19。片中要说「FAA 初步调查」 | https://www.nbcsandiego.com/news/business/money-report/faa-says-contractor-unintentionally-deleted-files-before-outage-disrupted-thousands-of-flights/3147182/ |
| C35 | **需改（升级为已证实）** | OIG 信件 **CC-2010-012，2010-06-17**，Inspector General Scovel 写给众议院运输委员会 Oberstar、Costello。原文："On November 19, 2009, FAA's FTI system experienced a NAS-wide outage while Harris was transitioning FTI Internet Protocol (IP) services from a legacy network to the new FTI Operations Internet Protocol (OPIP) fiber optic network." / "the root cause of the outage occurred when a Harris engineer incorrectly configured one of several temporary routers (known as Logical Transition Bridges) between the old and new networks." / "The new router also contained the configuration error, since the route map ... was copied from the replaced router."。**更正**：① 出错的是**洛杉矶中心**的路由器（错误 2009-10-21 首次引入后一直潜伏，11-19 换新路由器时被触发），不是 Nextgov 说的盐湖城（盐湖城是流量被挤爆的地方）；② 影响 129 个设施（本应只有 21 个），约 75% 的路由被阻断 5 小时，"resulting in 820 flight delays"；③ 这**不是全国停飞令**，原文是 "grounded hundreds of flights nationwide"。片中可说「全国范围的通信中断」，不能说「全国停飞」 | https://webarchive.library.unt.edu/web/20161103185913/https://www.oig.dot.gov/sites/default/files/WEB%20FILE2_FTI%20%20Nov%2019%20outage-6-18-10_Final%20Signature%28a%29%20%282%29.pdf （本次经 https://www.oig.dot.gov/sites/default/files/WEB%20FILE2_FTI%20%20Nov%2019%20outage-6-18-10_Final%20Signature%28a%29%20%282%29.pdf 取得全文） |
| C36 | **需改** | ① **quote 不在所给的 Reuters/Yahoo 页面上**。那篇只有 "while processing a flight plan filed for a U-2 aircraft that operates at very high altitudes under visual flight rules"、"to now require specific altitude information for each flight plan"，以及加内存的转述。quote 出自 FAA 发言人 Laura Brown，见 The Register 2014-05-12，出处要改；② **「新上线」不准**：洛杉矶中心 2012 年 2 月就进入 ERAM 初始运行（IOC），到 2014-04 已在用约两年，只是全国部署 2015 年才完成。应改为「当时仍在全国铺开的新一代系统 ERAM」；③ 宕机约 46 分钟（NATCA 的 Nate Pair："46 minutes later we were back up and running"），Reuters 写 LAX「more than 200 flights」延误或取消 | https://www.yahoo.com/news/faa-says-air-traffic-computer-overwhelmed-u-2-012553030--finance.html ；https://www.theregister.com/2014/05/12/los_angeles_air_traffic_control_crash_caused_memory_shortage_u_2_spyplane_cia/ ；https://www.aviationtoday.com/2012/02/06/eram-achieves-initial-operating-capability-at-6-sites/ |
| C37 | 需改（小） | quote 通过。① 原文是「TDMI」，不是「TDM」："multiple failures of the TDMI data telecommunications service provided by Frontier"；② L3Harris 一句几乎逐字："an oversight by L3 Harris, an FAA contractor, failed to make sure that redundancies in the system functioned properly"，可以改成引号；③ 「两条光纤被切断」是 FAA 告诉美航的（"originally stemmed from two cut fiber optic cables"），不是美航 COO 自己的判断；④ 页面没写日期，只有 2025-09-20 的时间戳，19 日是推算 | https://www.cbsnews.com/texas/news/outdated-infrastructure-faa-dallas-airport-ground-stops |
| C38 | **需改** | quote 换原文。Airways 导语："lost its primary communications circuit and officials found that its backup line had been cut"；另一句归给 Bedford（经 NBC）："When the system switched to backup, officials discovered that the fiber-optic line..."。纽瓦克时刻核实无误："No commercial flights landed at Newark from about 09:40 ET until just after 17:20 ET"（Flightradar24，经 NBC New York）。Amtrak 与 NJ Transit 之争核实无误 | Airways |
| C39 | 通过 | SciAm 逐字一致。另有一句 Stilwell 的话与论点 A 直接相关："It would be unusual for them to do a software update during the day, but the FAA is very short-staffed"（这是推测，不是事实） | SciAm |
| C40 | 通过 | NBC 正文逐字一致 | NBC rcna609247 |
| C41 | **需改** | **quote 不在 CNBC 上**，CNBC 只有转述（technicians "are investigating, the agency said"）。Newsweek 有 "FAA technicians are investigating the issue." 和 "We will provide immediate updates as we have them"；Scripps 把 "FAA technicians are investigating the issue." 归给 Duffy。要改出处，quote 改成 "...investigating the issue. We will provide immediate updates as we have them"，并注明说话人有分歧（FAA 声明还是 Duffy）。结论「截至 11-14 无官方根因」本次检索也支持 | Newsweek；Scripps |
| C42 | 通过（作判断） | 已标「我们的判断」、用「可能」，可以。补充：Stilwell 的「白天做软件更新不寻常」（C39 注）也可以作为背景，但同样只是推测 | — |
| C43 | **需改** | 依据清单有误：2025 达拉斯（光纤被切断、冗余失效）、2026-09 费城（主电路故障、备份光纤被施工挖断）**不是改动引发**，属于论点 B（冗余不独立）。2014 ERAM 是「新系统的潜伏缺陷」，也不是「动它时」。建议改为：「改动时出事：2009 FTI 迁移（OIG 已证实）、2015 ERAM 软件升级（建议新增）、2023 NOTAM 维护时误删；冗余不独立：2004 洛杉矶中心备份一分钟内崩溃、2009 FTI 运营商升级后备份路径失去分离、2025 达拉斯、2026 费城」。详见第 3 节 | 见第 3 节 |
| C44 | 需改（note） | 判断本身可以。note 里「Duffy 称 cautionary measure」在 Scripps、USA Today 原文里都**没找到**（只有 "out of an abundance of caution"，是 FAA 与 Mullin 的话），换成可核实的句子。Mullin "The public was never in danger through this process." 已在 Scripps 核到 | Scripps；Yahoo 211917033 |

**统计**：通过 25 条（含带小注的）；需改 19 条：C02、C04、C05、C06、C07、C12、C15、C16、C17、C25、C31、C33、C35、C36、C37、C38、C41、C43、C44；删除 0 条。另有 3 条通过但带「未能核」子项：C11（MS NOW、彭博）、C29（事实本身）、C31（AP、NPR、新华社、Wikipedia、中文媒体）。

---

## 3. 论点 A 证据链评估

论点 A：「关键系统最危险的时刻，往往不是它老了，而是你动它的时候。」

### 3.1 先例逐个分类（只按已核实的原文分）

| 事件 | 是否「改动、升级、迁移、维护时出事」 | 依据 | 对 A 的作用 |
|---|---|---|---|
| **2009-11-19 FTI 全国通信中断** | **是，而且是教科书式的**：旧网迁新网的过渡期，临时过渡路由器配错，换新路由器时把错误配置复制过去 | OIG CC-2010-012 原文（C35） | 最强支撑。OIG 还写道："both FAA and Harris officials acknowledged that there is still a risk of critical outages as new NextGen services are added"。当年的 FTI、迁移、Harris（今 L3Harris），与本次是同一张网、同一家公司 |
| **2015-08-15 华盛顿中心（Leesburg）ERAM 故障**（档案没有） | **是**：最新软件版本里的新功能让数据留在内存里删不掉，存储满后系统停摆；FAA 关闭该功能止损。延误 492 班、取消 476 班 | Route Fifty（2015-08-18）："remained in the system's memory until storage capacity was full"；"The current fix suspended the function entirely to eliminate the possibility of problems" | 强支撑，**建议补进 claims**。这次检索只核到 Route Fifty 的转述，FAA 原声明没有直读 |
| **2023-01-11 NOTAM 停飞** | **是（维护操作触发）**，但官方另有一层定性 | FAA 初步调查：承包商修主备库同步时误删文件（C34）；GAO 定性为 "the outage of an aging air traffic control (ATC) system"，系统 "over 30 years old"（C33） | 支撑，但要讲全：触发点是维护，底层是 30 多年的老系统。这正好可以讲成 A 的第二层「越老越不敢动、越难动」，不能只讲成「改动惹祸」 |
| **2026-11-13 本次** | **未证实** | 只有 CBS 匿名信源的「更新→重启→崩溃」（C11），Mullin 的「patches」是 Globe 转述（C15）；Duffy 说是旧设备过载（C12、C13） | 不能当证据，只能当「待验证的一例」。档案已这样处理，正确 |
| 2014-04-30 洛杉矶中心 ERAM（U-2） | **否**：ERAM 在洛杉矶已运行约两年，是新系统的潜伏缺陷遇到罕见输入，事发时没有人在改它 | C36 更正 | 弱支撑，只能支撑「换新系统的过渡期有风险」，不能证明「动它的时候」 |
| 2004-09-14 洛杉矶中心语音通信中断（档案没有） | **否**：VCSU 子系统 2003 年才投用，计时器 49.7 天溢出，要靠每 30 天人工重启规避；这次是重启**没做**。备份 "crashed within a minute after it was turned on"。约 400 架飞机失联，约 800 班受影响 | IEEE Spectrum | **反例**：没人动它，它自己坏了（准确说，是该做的维护没做）。同时也是论点 B 的好例子：主备同时失效 |
| 2025-09-19 达拉斯 | **否**：两条光纤被切断，冗余失效 | CBS Texas（C37） | 属于 B；对 A 是中性到反例 |
| 2026-09-21 费城 TRACON | **否**：主电路故障，备份光纤已被施工挖断 | Airways（C38） | 属于 B；对 A 是反例 |
| 2025-04/05 纽瓦克（费城 TRACON） | 直接原因不是：铜线或电信故障（FAA 正式根因未检索到）。**但**根子上是 2024 年把纽瓦克进离场管制从纽约迁到费城造成的长距离链路依赖，这一点属于「组织层面的改动」 | angles/history.md 3.1–3.3（本次未逐条重核） | 可以作为 A 的延伸（「搬迁也是一种动它」），但证据链要单独核，暂不建议用 |
| 2014-09 芝加哥中心纵火 | 否（人为破坏） | — | 无关 |

### 3.2 结论

- **站得住，但要收窄。** 已证实的案例里，「动它时出事」实打实有三例（2009、2015、2023）。规模最大的那次（2009，129 个设施）正好发生在同一张网 FTI 的上一次迁移中。这条线对本期是很好的历史钩子。
- **「往往」要有限定。** 局部的大事故（2004 洛杉矶、2025 达拉斯、2026 费城、2025 纽瓦克）多数不是改动引发，而是老化、外部挖断、维护缺失，加上备份不独立。建议在片中说成：**「看最严重的那几次——2009 年、2023 年，可能还有这一次——出事的时候都有人正在动它」**，同时明说「不是每次都这样：达拉斯和费城就是线被挖断、备份也跟着断」，顺势转入论点 B。这样不改变论点，只是把边界讲诚实。
- **反方还缺一条要承认：分母问题。** L3Harris 每月部署 150–200 条新路径（C26），绝大多数改动没有出事。「出事时恰好在改」也可能只是因为系统一直在改。片中应承认这一点，再说明我们为什么仍然认为过渡期是高风险窗口：OIG 2010 年就写明，迁移期的临时桥接和新旧并存本身就是风险源，FAA 与 Harris 当时也承认风险还在。
- **OIG 2010 给了一个比「动它危险」更硬的点，建议用。** 原文："According to Harris officials, FTI sites that supposedly had diversity no longer had it after AT&T or Sprint made upgrades to their network."（运营商升级自己的网络后，本应分离的主备路径不再分离。）这一句同时支撑 A（升级引入风险）和 B（冗余不独立），而且是监察长的一手文件。另一个背景数字：2009 年 12 月，FTI 上 91.4% 的业务还跑在 TDM 旧网上（19,174 / 20,982）。17 年后部长还在说「我们是 TDM」，可以作为「越不敢动越老」的佐证（这是我们的判断，要这样标）。
- **dossier 第 1 节「我们为什么仍然这样看」第 2 点**要按上面改：2014 ERAM 换成 2015 ERAM（或两个都保留，但 2014 改称「新系统潜伏缺陷」），2009 去掉「待逐字核对」，细节（129 个设施、本应只影响 21 个、820 班延误、5 小时）以 OIG 原文为准。

---

## 4. 截至 2026-11-14 的新进展

- **根因**：没有查到 FAA、DOT 公布根因或初步报告。L3Harris 仍只有「未回应」（CBS、The Register）。Scripps 引一名匿名管制员："controllers have not yet been told what caused the specific issue or what fixes are underway"。
- **国会**：没有查到已排期的听证。只有 Cantwell："...will be something the Commerce Committee will be reviewing"（ABC）。检索结果里唯一一条 Cruz 听证是 2025-11 的提名听证，与本事件无关。
- **NTSB、DOT 监察长**：没有查到立案。
- **余波**：Reuters（经 IBTimes）引 Flightradar24：周五取消逾 4,700、延误 10,000；周六已取消约 700。NBC 正文终版写「逾 7,000 班取消」，没写来源。
- **国家紧急状态**：USA Today 写 Mullin 称特朗普已宣布空管故障为「a national emergency」。没有文件佐证，维持「仅 Mullin 转述」。
- **欧控 42 国**：USA Today 原文核到（"42 countries"，美东周五 17:00 至午夜，应 FAA 要求），欧控原文仍未读。

检索局限：受配额限制只做了 3 次面向新进展的搜索，CNN 返回 451。11-14 当天稍晚以后的进展可能漏检，进讲稿前再查一次。

---

## 5. 必须改的清单（按严重程度）

1. **C35 升级并改细节**：改为「已证实」，quote 填 OIG 原文，来源写 CC-2010-012（2010-06-17）。出错路由器在洛杉矶中心，影响 129 个设施、820 班延误、5 小时，不是全国停飞令。dossier 去掉「待核」字样。
2. **C43 及 dossier 第 1 节论据**：把达拉斯、费城从「改动时出事」移到「冗余不独立」；2014 ERAM 改称「新系统潜伏缺陷」；新增 2015 ERAM 软件升级一条（需要新的 claim 编号，进讲稿前最好直读 FAA 原声明）；在片中承认反例（2004 洛杉矶、达拉斯、费城）和分母问题。
3. **C12「模拟（TDM）」**：TDM 不是模拟，旁白不能这样说，只能引述 Duffy 原话 "so this is analog telecom"。「输出不一致的数据、于是关闭系统」没有出处，补出处或删掉。
4. **C36**：出处改成 The Register 2014（FAA 发言人 Laura Brown）；「新上线」改为「仍在全国铺开的新一代系统，洛杉矶中心 2012 年起运行」；时长约 46 分钟。
5. **C02**：quote 不在 CBS，出处改成 Newsweek；标注「Federal Aviation Command Center」不是正式名称；Advisory 111 原文要在 **11-28 前**人工存档核对。
6. **C17**：ASI 声明的出处从 SciAm 改为 USA Today/Yahoo；Mullin 那句改成 "We're not ruling anything out at this point."
7. **C41**：quote 不在 CNBC，改用 Newsweek 原句，并注明说话人有分歧（FAA 还是 Duffy）。
8. **C05、C06、C07、C31、C33、C38**：quote 全部换成第 2 节给出的原文；C06 口径表补上 NBC「逾 7,000」，删掉核不到的「约晚 9 点」和「近 5,000（ABC）」，或者补出处。
9. **C16、C44**：note 里核不到的 "mechanically driven"、"cautionary measure" 删掉，或者补可读的出处。
10. **C04**：「约 3,500」改为「3,500 多架」；15:36 的说话人写清楚（Duffy 与匿名管制员），不要沿用 NBC 直播「3:36 下令停飞」的错误写法。
11. **C25**：35 亿美元是合同上限，不是中标额。
12. **C15、C37**：「buckle」改为 IBTimes 原句；TDM 改为 TDMI；「两条光纤被切断」改为「FAA 告诉美航」。
13. **dossier 时间线**：FAA X 帖改为 17:52 前（NBC 条目时间），Duffy X 帖「16:16」改为「17:20 前已发」或标「时刻未核」；第 6 节「L3Harris 99.999%」在 L3Harris 新闻稿里没有，划掉。

## 6. 未能核的条目或子项

- ATCSCC Advisory 111 原文（C01、C02 所依）、faa.gov 声明页、Duffy 与 FAA 的 X 帖原帖、白宫记者会视频：都没有直读，只核到媒体逐字转引。
- C11：MS NOW「联邦官员证实软件更新」、彭博「FBI 查软件更新」。
- C12：「输出不一致数据、关闭系统」。
- C16：Mullin "mechanically driven"。
- C17：note 里 Mullin 那句的原版。
- C24：DOT「69% 铜线已替换」。
- C29：「LBJ 以来没有新建 ARTCC」的事实本身。
- C31：AP、NPR、新华社、Wikipedia、澎湃、TVBS 的计数说法（只核了 ABC、Scripps、Reuters/IBTimes）。
- C44：Duffy "cautionary measure"。
- 2015 ERAM：只核到 Route Fifty 转述，FAA 原声明未直读。
- 新进展：CNN 451；11-14 晚些时候的进展可能漏检。

## 7. 本次使用的检索

WebSearch 8 次，WebFetch 约 35 次。主要一手材料：GAO-24-107001、GAO-25-108162、GAO-26-107992、9/11 委员会报告第 1 章、DOT OIG CC-2010-012、L3Harris 2026-05-11 新闻稿。
