# 研究档案：美国航班全国性地面停飞（FAA nationwide ground stop，2026-11-13）

- 检索日期：**2026-11-14**（片中说法以「截至 2026 年 11 月 14 日」为准）
- 检索范围：2026-11-10 至 11-14 的报道为主；历史对照回溯到 2001 年；语言：英文为主，中文（大陆、台港、海外）为辅
- 角度文件：`research/angles/` 下 `timeline.md`（事件经过）、`cause.md`（技术原因）、`history.md`（历史与现代化）、`stakeholders.md`（各方说法）、`coverage.md`（别人讲过什么）、`media.md`（素材候选）
- 事实台账：`../claims.json`（48 条：原 44 条按事实核查 r1 修改，C45–C48 为 r1 新增；`lines` 待讲稿定稿后挂行号）
- 事实核查：`research/factcheck_r1.md`（2026-11-14，独立上下文），处理情况见第 7 节
- **检索局限**（影响全档案）：faa.gov、transportation.gov、fly.faa.gov、oversight.gov 对抓取工具返回 403，FAA 新闻稿与 ATCSCC 公告**都没能直读**，原话转引自 CBS、NBC、ABC 等的逐字引用；CNN（451）、Reuters、NYT、WSJ、Bloomberg 原文未读到，只见他报转引；检索后期会话 WebSearch 配额用尽，NATCA、PASS、A4A、众议院交通委员会对本事件的表态未能检索，抖音、微博热度拿不到。gao.gov、congress.gov、9/11 委员会报告是直接核对过的一手材料。
- 没有调用任何收费服务，没有下载图片或视频。

---

## 1. 一句话论点（认知精华）

### 候选

| # | 论点 | 依赖的事实 | 强弱 |
|---|---|---|---|
| A | **最严重的那几次，出事时都有人正在动它（迁移、升级、维护）。不是每次都这样——另一半是冗余不独立（转入 B）。技术债的利息是「越老越不敢动，越不敢动越老，过渡期越拖越长」。** | A 类（改动时出事）：2009 FTI 迁移时过渡路由器配错（C35，OIG 已证实，129 个设施）、2015 华盛顿中心 ERAM 软件升级耗尽内存（C45）、2023 NOTAM 维护时误删文件（C34；GAO 定性为老旧系统故障，C33）；本次官方「老设备过载」与匿名信源「更新触发崩溃」并存（未证实，只作待验证的一例）；新旧网络并行的过渡期（FTI → FENS，承包商两次更换）；Bedford「换铜线为光纤，架构还是 50 年前那套」 | 推荐，按 r1 收窄后。反例要在片中承认：2004 洛杉矶中心（C46）、2014 洛杉矶 ERAM（C36）；分母：每月 150–200 条新路径上线，绝大多数改动没出事（C26） |
| B | **备份只防「各自坏」，防不了「一起坏」。** 主备共用一张网、一条路由、一个承包商，冗余就只是纸面上的。 | B 类（冗余不独立）：2025-09 达拉斯（C37）、2026-09 费城（C38）都是主线断、备份也断；2009 运营商升级后 FTI 主备路径不再分离（C35 note，OIG 原文）；2004 洛杉矶备份一分钟内崩溃（C46）；22 个航路中心共用一张电信骨干；Duckworth「安全建立在冗余之上」 | 机制最清楚、最可迁移；但本次是否属共模故障尚待调查，依赖性比 A 强 |
| C | **全国停飞不是系统失败，而是安全设计在起作用：系统失去把握时，退到代价看得见但安全的状态。** 我们总把刹车当事故，是因为代价看得见、风险看不见。 | FAA「out of an abundance of caution」（C09）；Duffy 称没有失去全部通信雷达（C14）；Mullin「The public was never in danger through this process.」（C44）；Stilwell「停飞是正确的」（C39）；3,500 多架在空飞机全部安全落地（C04） | 最能对冲恐慌，适合作结尾反转；单独作主线略薄 |

**推荐：A 作主线，B 作「为什么一个点会变成全国」的机制段，C 作结尾反转。** A 讲到「不是每次都这样」时顺势转入 B。

> **A（r1 收窄后的口径）：最严重的那几次，出事时都有人正在动它。不是每次都这样——达拉斯和费城就是线被挖断、备份也跟着断，那是另一个问题：冗余不独立（B）。技术债的真正利息，是越老越不敢动、越不敢动越老，换代的过渡期越拖越长，而过渡期正是最该当成高风险来设计的阶段。**
>
> 片中可直接说：「看最严重的那几次——2009 年、2023 年，可能还有这一次——出事的时候都有人正在动它。」（「这一次」只能说「可能」，根因未公布，C41。）

- **最强的反驳**：
  「这是在给拖延找借口。事实是美国空管有 105 个不可持续或可能不可持续的系统（GAO），用着 1980 年代的铜线和软盘；这次部长明确说新装的设备一台都没坏，坏的是旧网络。真正的教训就是钱给得太少、换得太慢——快点花钱换掉就好了。把『升级有风险』当论点，只会让决策者更不敢动，正好延续了技术债。而且根因还没查清，『更新触发』只来自匿名信源，你们把一个未证实的说法当成了论点的基石。再说，几十年来全国停飞只有寥寥几次、没有人因此丧命，这套系统的可靠性其实已经很高了。还有分母：L3Harris 每个月上线 150–200 条新路径，绝大多数改动根本没出事；系统一直在改，出事时『恰好在改』有什么稀奇？2004 年洛杉矶、2025 年达拉斯、2026 年费城，哪一次是有人在动它？」
- **我们为什么仍然这样看**：
  1. 我们不反对升级，恰恰相反：论点是「必须换，而且换的过程要当成最危险的阶段来设计」。反方说的「钱太少、换太慢」和我们并不冲突——拖得越久，过渡期就越长，新旧并存、两头维护的危险窗口就越大。GAO 2026-09 指出新系统没有可靠的全生命周期成本估算、11,389 份进度表互不整合，说明「快点花钱」本身并不自动等于安全。
  2. 论点不建立在本次单一根因上，也不说「每次都是改动惹祸」。按已核实的原文分类（r1）：
     - **A 类，改动时出事**：2009-11-19 FTI 全国范围通信中断——Harris 把 FTI 的 IP 业务从旧网迁到新光纤网时，洛杉矶中心一台临时过渡路由器配错，错误被复制进新换的路由器，129 个设施受影响（本应只有 21 个），约 75% 的路由断了 5 小时，820 班延误（DOT 监察长 CC-2010-012，C35；是通信中断，不是停飞令）；2015-08-15 华盛顿中心 ERAM 软件升级带来的新功能让数据塞满内存，延误 492 班、取消 476 班（FAA 声明，C45）；2023-01-11 NOTAM 停飞，触发点是承包商维护主备库同步时误删文件（FAA 初步调查，C34），GAO 则把它定性为一套 30 多年的老旧系统的故障（C33）——两层都讲，后一层正是「越老越难动」。
     - **B 类，冗余不独立**：2025-09 达拉斯（光纤被切断、冗余失效，C37）、2026-09 费城（主电路坏、备份光纤早被施工挖断，C38）。它们不是改动引发，片中明说「不是每次都这样」，然后由此转入论点 B。
     - **反例**：2004-09 洛杉矶中心语音通信中断，没人在改它，是该做的定期重启没做，备份开机一分钟内也崩溃（C46，同时是 B 的例子）；2014-04 洛杉矶 ERAM 被一份 U-2 飞行计划耗尽内存，那是已运行两年的新系统里的潜伏缺陷，事发时没人在动它（C36）。
     - **分母**：L3Harris 每月上线 150–200 条新路径（C26），绝大多数改动没出事。我们承认这一点，所以论点只说「最严重的那几次」，不说「往往」。仍然认为过渡期是高风险窗口，是因为 DOT 监察长 2010 年就写明，迁移期的临时桥接、新旧并存本身就是风险源，FAA 与 Harris 当时也承认 "there is still a risk of critical outages as new NextGen services are added"（C35）；而且同一张网 FTI、同一家公司（Harris，今 L3Harris），上一次全国范围中断正发生在上一次迁移中。
     - 即使 11-13 最终查明是纯硬件过载，Duffy 说的「新设备没坏、旧设备坏了」恰好说明网络正处在新旧并存的过渡期；本次只当「待验证的一例」，不当证据。
  3. 三位官方与准官方说法（Duffy 的旧设备过载、Mullin 的补丁与新技术压垮旧系统、CBS 信源的更新后重启崩溃）并不互斥，可能是同一件事的不同侧面。我们会在片中明确标「我们的判断」，并说明如果调查结论不同，哪部分要改。
  4. 关于「系统其实很可靠」：我们同意，这也是论点 C 要讲的。但「很少全坏」恰恰是危险的来源——越少出事，越少人知道怎么改它而不出事。
- **我们独有的角度**（对照第 5 节）：
  - 英文主流把「老旧设备」（Duffy）和「更新出错」（CBS）写成两种**互相竞争**的解释；中文几乎全是外媒转述加「美国衰落」叙事。**没有人把两者讲成同一个陷阱的两面**，也没人讲「为什么 24 小时不停的系统几十年换不掉」。
  - 没有人讲**共模故障**：多数报道默认「有备份就安全」，把这次写成「备份没做好」，而不是「这种备份天生防不了这种故障」。
  - 没有人把停飞讲成**失效安全**；中文标题多是「瘫痪」「趴窝」「惊险内幕」。
  - B 站截至 11-14 上午最热约 1.2 万播放，以搬运为主；航空解说频道（Mentour Pilot 等）截至检索时未见相关视频。中文市场的机制解说是空白。

---

## 2. 事件时间线

（美东时间 ET；详细版与数字口径见 `angles/timeline.md`）

| 日期 / 时间 | 发生了什么 | 出处（一手优先） |
|---|---|---|
| 2025-07 | 国会拨款 125 亿美元用于空管现代化（Pub. L. 119-21） | GAO-26-107992 https://www.gao.gov/products/gao-26-107992 （一手） |
| 2025-09-19 | 达拉斯两大机场停飞约 5 小时：TDM 数据电信多次故障，FAA 称 L3Harris 未确保冗余有效 | CBS Texas https://www.cbsnews.com/texas/news/outdated-infrastructure-faa-dallas-airport-ground-stops |
| 2026-08-11 | FAA 改由 AT&T 担任下一代电信网 FENS 主承包商（替换 Verizon）；旧网 FTI 仍由 L3Harris 运营 | Aviation Week https://aviationweek.com/air-transport/safety-ops-regulation/faa-taps-att-build-its-next-telecom-backbone ；Nextgov |
| 2026-09-14 | GAO 报告：新空管系统缺可靠成本估算、11,389 份进度表互不整合 | https://www.gao.gov/products/gao-26-107992 （一手） |
| 2026-09-21 | 费城 TRACON 主电路故障，备份光纤已被施工挖断；东北部多机场停飞 | Airways https://airwaysmag.com/new-post/faa-northeast-ground-stops-severed-fiber-philadelphia-tracon |
| 2026-11-10 | AI 工具 SMART 扩展到全部 22 个航路中心 | Scientific American |
| 2026-11-13 约 15:10（时刻未证实） | 芝加哥 O'Hare、Midway 先因 "equipment outage" 停飞（Advisory 107/109） | CBS Chicago（顺序）；Glitchwire（时刻，低可信）；Clash Report 转述公告编号 |
| 11-13 15:36 前后 | 雷达与通信开始不稳定（Duffy 与一名匿名管制员的说法；不是停飞时刻） | Fox、USA Today（Duffy）；Scripps（管制员） |
| 11-13 15:54 | ATCSCC 发布全国地面停飞（Advisory 111）："due to extraordinary circumstances and for reasons of safety"；离港原地等待，国际入境逐案处理 | ATCSCC 公告（403 未直读），经 NBC、Newsweek 逐字转引 |
| 11-13 17:20 前（确切时刻未核） | Duffy 在 X 宣布：问题 "impacting all Air Route Traffic Control Centers" | NBC 直播 17:20 条收录；Scripps 全文引；Duffy X 帖 https://x.com/SecDuffy/status/2121351591106072679 （原帖未直读） |
| 11-13 17:52 前（NBC 条目时间） | FAA X 帖："temporary telecommunications outage … all flights have been halted"；"Every flight has been accounted for." | NBC 直播 17:52 条 |
| 11-13 17:00–24:00 | 欧洲飞美国航班暂停起飞（USA Today 称欧控应 FAA 要求、涉及 42 国，待核欧控原文） | USA Today；Wikipedia |
| 11-13 约 21:00 前 | 白宫外记者会（Duffy、Mullin）：旧路由器过载、无网络攻击证据、要 500 亿美元 | 白宫官方 YouTube https://www.youtube.com/watch?v=aH2db_pvy38 （见 media.md）；ABC、NBC 直播 |
| 11-13 20:15 | Duffy 宣布空域重新开放（停飞约 4 小时 21 分） | CBS |
| 11-13 当晚（确切时刻核不出） | FlightAware：美国相关取消 4,467、延误 10,079；NBC 正文终版（22:19 更新）写「逾 7,000 班取消」，未写来源（C06、C47） | Fox News 直播；NBC 正文 |
| 11-14 | 余波：JetBlue 取消周六航班以重新调配机组和飞机；Reuters 引 Flightradar24：周五取消逾 4,700、延误 10,000，周六已另取消 700 班（11-13 晚的数字，C48）。截至 11-14 未查到官方根因、初步报告、已排期听证 | CNBC；Reuters 经 IBTimes/Yahoo |

---

## 3. 利益相关方

（全表与更多原话见 `angles/stakeholders.md`；以下原话均经媒体逐字转引）

| 谁 | 立场 | 公开说过什么（原话） | 出处 |
|---|---|---|---|
| FAA | 出于谨慎停飞；技术人员调查中 | "There has been a temporary telecommunications outage — out of an abundance of caution all flights have been halted." / "FAA technicians are investigating the issue. ... We will provide immediate updates as we have them"（Scripps 把首句归给 Duffy） | NBC 直播；Newsweek |
| 交通部长 Sean Duffy | 原因是老旧系统；新设备没坏；要国会紧急拨款 500 亿；还会再发生 | "What we have is an incredibly old air traffic control system." / "We have TDM telecoms, so this is analog telecom"（「模拟」是他的原话；TDM 实为数字传输，旁白不作此认定） / "By the way, all of the new equipment that we put in, none of that went down." / "I want $50 billion." / "You will have more of these" | CBS；NBC 直播；ABC 直播；USA Today |
| 国土安全部长 Markwayne Mullin | 不是袭击（未完全排除）；补丁与新技术压垮旧系统 | "This isn't another 9/11. I cannot repeat that enough." / "that new equipment and new technology was overwhelming the older system." | ABC；Globe and Mail 直播 |
| 白宫 / 特朗普 | 特朗普持续听取汇报；经 Doocy 转述称不像网络攻击，原因是 "a bunch of old broken stuff" | （二手转述） | NBC 直播；Fox 直播 |
| FAA 局长 Bryan Bedford | 11-13 当天未检索到公开表态；2026-09 称换介质不换架构 | "We're pulling copper up and putting fiber down, but it's the same data architecture that we've had for 50 years." | Airways（2026-09） |
| 参议院商务委员会（主席 Cruz） | 优先现代化航路管制中心 | "No new ARTCC has been built since LBJ was in office." | USA Today 转引 |
| 参议员 Cantwell（D） | 审查主备频率等通信技术 | "Technology issues related to how planes communicate through primary frequencies, backup frequencies" | ABC |
| 参议员 Duckworth（D） | 追责、要求调查 | "The safety of our skies is built on redundancies" | ABC |
| 参议员 Schmitt（R） | 国家安全问题 | "This is a huge public safety and national security issue" | Fox 直播 |
| L3Harris（FTI 运营商） | 未回应置评 | — | CBS、The Register |
| Air Space Intelligence（SMART 供应商） | 撇清 | "The current ground stop is not based on or a result of the SMART system." | USA Today（经 Yahoo） |
| 航司（Delta、JetBlue、United） | 只谈恢复 | Delta："it will take time to reset our operation, including the positioning of aircraft and crews." | NBC 直播 |
| 一线管制员 | 信息不透明 | "I'm as much in the dark as everyone else." | NBC（LiveATC 录音） |
| 专家 | 停飞正确；系统脆弱 | Stilwell："The ground stop was the right thing to do." Cummings："This is yet another example of how brittle our air transportation system is in our country." | Scientific American |
| 乘客 | 滞留、焦虑 | "It's a little scary, like, is it cyberattack?" | NBC |
| NATCA / PASS / A4A | **未检索到对本事件的声明**（配额用尽，需补查） | — | — |

---

## 4. 材料

### 4.1 一手材料（原文、公告、数据、文件）

- **FAA ATCSCC Advisory 111（2026-11-13）** — https://www.fly.faa.gov/ois/oisedit/adv_oisedit_dis?number=111&day=11132026&gdp=-1&gstop=196093 — 全国停飞令原文；403 未直读，媒体逐字转引一致；公告库保留 15 天，**11-28 前人工存档**
- **FAA Statement on Nationwide Ground Stop** — https://www.faa.gov/newsroom/faa-statement-nationwide-ground-stop — 「multiple」ARTCC、技术人员调查中；403 未直读
- **Duffy X 帖** — https://x.com/SecDuffy/status/2121351591106072679 — 「all」ARTCC
- **白宫记者会视频（官方 YouTube）** — https://www.youtube.com/watch?v=aH2db_pvy38 — Duffy、Mullin 原话；需核实是否为电视台联合信号
- **GAO-24-107001（2024-09-23）** — https://www.gao.gov/products/gao-24-107001 — 138 个系统中 51 个不可持续、54 个可能不可持续
- **GAO-25-108162（2025-03 证词）** — https://files.gao.gov/reports/GAO-25-108162/index.html — 2023 NOTAM 停飞约 2 小时、1,300+ 取消；NextGen 2007–2022 财年花费 140 多亿
- **GAO-26-107992（2026-09-14）** — https://www.gao.gov/products/gao-26-107992 — 125 亿拨款；无全生命周期成本估算；11,389 份进度表；5,170 条铜线已换 2,560 条
- **9/11 委员会报告第 1 章** — https://govinfo.library.unt.edu/911/report/911Report_Ch1.htm — 9:25 全国停飞、落地令、约 4,500 架
- **NOTAM Improvement Act of 2023（P.L. 118-4）** — https://www.congress.gov/bill/118th-congress/house-bill/346 — 2023 故障后的立法整改
- **DOT 监察长信件 CC-2010-012（2010-06-17，关于 2009-11-19 FTI 全国范围中断）** — https://webarchive.library.unt.edu/web/20161103185913/https://www.oig.dot.gov/sites/default/files/WEB%20FILE2_FTI%20%20Nov%2019%20outage-6-18-10_Final%20Signature%28a%29%20%282%29.pdf （原址 https://www.oig.dot.gov/sites/default/files/WEB%20FILE2_FTI%20%20Nov%2019%20outage-6-18-10_Final%20Signature%28a%29%20%282%29.pdf ）— 迁移旧网到新光纤网时洛杉矶中心过渡路由器配错；129 个设施、820 班延误；合同上限 35 亿；运营商升级后主备路径失去分离。**r1 已取得全文逐字核对**（C35、C25）。另有 2006 AV-2006-047 未读
- **FAA Statement on Automation Problems at Washington Center（2015-08-18）** — https://www.aviationpros.com/airports/airports-municipalities/press-release/12104165/faa-statement-on-automation-problems-at-washington-center — 2015 ERAM 软件升级新功能塞满内存；转载页，faa.gov 原页未直读（C45）
- **L3Harris 新闻稿（2026-05-11，企业自述）** — https://www.l3harris.com/newsroom/editorial/2026/05/l3harris-reaches-over-50-faa-telecommunications-modernization — FTI 现代化过半、2027 完成、先建后切
- **航司改签豁免与声明** — 见 VisaVerge 汇总与 American 新闻室 https://news.aa.com/news/news-details/2026/Update-on-FAAs-nationwide-ground-stop/ （未读正文）

### 4.2 二手报道与评论

- **CBS News** — https://www.cbsnews.com/news/faa-issues-nationwide-ground-stop/ — 「更新→重启→崩溃」、L3Harris；转述自：多名匿名信源
- **NBC News 直播与正文** — https://www.nbcnews.com/news/us-news/live-blog/live-updates-flights-grounded-faa-communications-outage-rcna609268 — 最细时间线、Duffy TDM 原话；转述自：Duffy 记者会、FlightAware、Flightradar24
- **ABC News 直播与正文** — https://abcnews.com/US/live-updates/faa-ground-stop-live-updates-hundreds-flights-canceled/?id=138125140 — 「1980s copper」「I want $50 billion」、Duckworth；转述自：记者会、议员声明
- **CNBC** — https://www.cnbc.com/2026/11/13/faa-ground-stop.html — Cirium 数据、JetBlue 备忘录、事件系列；转述自：Cirium、FAA 声明
- **USA Today（经 Yahoo）** — https://www.yahoo.com/news/us/articles/faa-orders-nationwide-groundstop-us-211917033.html — 参院商务委员会、Duckworth、FlightAware 机场分布；转述自：委员会 X 帖、FlightAware
- **Reuters（经 IBTimes / Yahoo）** — https://www.yahoo.com/news/us/articles/faa-lifts-nationwide-ground-stop-020705860.html — 「9·11 以来最长」、Flightradar24 取消数（周五逾 4,700、周六另 700）、Mullin「新技术压垮旧系统」（转述，原文无 buckle 一词）；转述自：Flightradar24、Mullin
- **Newsweek** — https://www.newsweek.com/faa-nationwide-ground-stop-airports-air-traffic-control-12713904 — 停飞公告文字（「federal aviation command center」非正式名）、FAA「technicians are investigating」；转述自：ATCSCC 公告、FAA 声明
- **Scripps News** — https://www.scrippsnews.com/us-news/faa-issues-nationwide-ground-stop-on-us-air-traffic — Duffy X 帖全文、「3,500 多架全部安全落地」、Mullin「zero evidence」「never in danger」、匿名管制员；转述自：Duffy、Mullin、管制员
- **历史先例（二手）**：Route Fifty 2015-08-18 https://www.route-fifty.com/digital-government/2015/08/what-went-wrong-with-the-faas-software-over-the-weekend/285483/ （2015 ERAM，C45）；IEEE Spectrum 2004-11-01 https://spectrum.ieee.org/lost-radio-contact-leaves-pilots-on-their-own （2004 洛杉矶中心，C46）；The Register 2014-05-12 https://www.theregister.com/2014/05/12/los_angeles_air_traffic_control_crash_caused_memory_shortage_u_2_spyplane_cia/ （2014 ERAM，C36）
- **Globe and Mail 直播** — https://www.theglobeandmail.com/world/article-faa-ground-stop-us-flights-live-updates/ — Mullin「patches」、加拿大反应
- **Scientific American** — https://www.scientificamerican.com/article/faa-grounds-all-u-s-flights-days-after-expanding-its-ai-air-traffic-system/ — SMART、Stilwell、Cummings
- **The Register** — https://www.theregister.com/offbeat/2026/11/13/faa-lifts-ground-stop-after-hours-long-delays-snag-travelers/5309912 — FTI 4,400+ 设施
- **Open Jaw** — https://openjaw.com/newsroom/airline/2026/11/13/faa-lifts-nationwide-ground-stop-but-delays-will-roll-into-the-weekend/ — 「没人解释为什么数据激增、为什么同时全国」
- **WSJ**（L3Harris 网络、承载无线电频率）— 转述自 Wikipedia 与 HN，原文未读
- **Bloomberg**（FBI 认为非攻击、查软件更新）— 转述自中新网，原文未读
- **新华社 / 澎湃 / 中新网 / 牛弹琴等中文报道** — 见 `coverage.md`；多数转述外媒且**未注明原始媒体**

---

## 5. 别人已经讲过什么

（详见 `angles/coverage.md`）

| 来源（视频 / 文章） | 主要角度 | 播放或影响力 | 缺了什么 |
|---|---|---|---|
| Duffy 本人；CBS、CNBC、AP、MS NOW、Flying | 美国基建老化、要拨款（官方主推） | 全国电视网与通讯社 | 「老」和「更新」并列不连；为什么一次故障打到全国 |
| ABC、CBS、NBC；澎湃、联合报、新华社 | 是不是攻击、「不是又一次 9·11」、9·11 后第二次 | 全国电视网；新华通稿被大量转载 | 9·11（清空天空）与本次（只禁起飞）的性质差别讲得少 |
| Jalopnik、The Register；自由时报、ETtoday、中央社 | AI 工具 SMART / 微软宕机巧合 | 标题流量高 | 无证据，放大未证实关联 |
| CNBC、NBC、Make Tech Easier、地方台 | 乘客滞留、退款、恢复 | 服务稿 | 为什么「停 4 小时、乱 2 天」 |
| View from the Wing（Gary Leff） | FAA 自营自管、年度拨款撑多年工程的激励问题 | 常旅客圈头部博客 | 最接近「技术债经济学」，但没讲冗余同时失效的机制 |
| Hacker News 讨论 | 为什么周五下午改关键设施、为什么没有热备 / 灰度 | 技术圈 | 猜测多、无系统解释 |
| 牛弹琴（中文自媒体）、CSDN | 「美国衰落」、冗余不足、技术债 | 头部自媒体转载广 | 技术几乎为零；无严格中美对比 |
| B 站（最热「俄乌前线」约 1.2 万播放） | 搬运英文新闻、英语学习 | 截至 11-14 上午 | 没有一条讲清机制；仅一条 12 播放的视频以「冗余」为题 |
| YouTube 新闻频道（NBC、ABC、CNN、MS NOW、Scripps 等） | 突发、白宫记者会直播 | 播放量尚不清楚 | 航空解说频道截至检索时未见视频 |
| 抖音 / 微博 | 热榜情况见系列 README 选题依据（抖音热榜第 1、微博第 2，follow-up 021） | 本次检索拿不到热度数据 | 尚不清楚 |

**我们的空位**：把「老旧」与「更新」讲成同一个陷阱（论点 A）；讲共模故障（B）；讲失效安全与看不见的账（C）。

---

## 6. 事实、争议与未知

- **已证实**：
  - 2026-11-13 美东 15:54 FAA 发布全国离港停飞，20:15 Duffy 宣布空域重开，约 4 小时 21 分；在空航班继续飞往目的地（C01–C03）。
  - 官方定性是「临时电信故障」，没有网络攻击证据（尚未完全排除）（C09、C16）。
  - Duffy 把原因归于老旧 TDM 网络、交换机和路由器过载（他原话称之为 "analog telecom"；TDM 本身是数字传输，旁白不跟着说「模拟」），并称新设备没坏；要求 500 亿美元紧急拨款（C12、C13、C18）。这是「他说过」，不是「原因已查明」。
  - 当晚 FlightAware 计美国相关取消 4,467、延误 10,079（C06）；当周平日取消约 100 班（C07）。
  - 2009-11-19 FTI 全国范围通信中断发生在旧网迁新光纤网的过程中，根因是洛杉矶中心一台临时过渡路由器配置错误；129 个设施、约 75% 路由断 5 小时、820 班延误；不是停飞令（DOT 监察长 CC-2010-012，C35）。
  - 2015-08 华盛顿中心 ERAM 故障与最近一次软件升级的新功能有关（FAA 声明，C45）；2004-09 洛杉矶中心语音中断是该做的定期重启没做、备份也随即崩溃（C46）；2014-04 洛杉矶 ERAM 是新系统的潜伏缺陷（C36）。
  - GAO：138 个空管系统中 51 个不可持续、54 个可能不可持续（C22）；新系统缺可靠成本估算、进度表不整合（C23）；国会 2025 年拨款 125 亿（C20）。
  - 这张电信网（FTI，L3Harris）正处在被替换的过渡期，下一代网络承包商 2023、2026 年两度更换（C25–C27）。
  - 9·11 是唯一一次让在空飞机全部落地；2023 和本次都是禁止起飞（C32、C33）。
- **有争议**：
  - **根因**：CBS 信源「网络更新→重启→崩溃」；Duffy「旧路由器过载、遗留网络问题」；Mullin「补丁 / 新技术压垮旧系统」；CNN 引航司信源「芝加哥 Midway 路由器」（Wikipedia 称 FAA 否认）；MS NOW 联邦官员「软件更新」；彭博「FBI 查软件更新」。官方未定论（C11、C12、C15）。
  - **「多个」还是「全部」航路管制中心**：FAA 声明说 multiple，Duffy 说 all（C10）。
  - **第几次全国停飞**：「9·11 以来第二次」（ABC、AP、NPR、新华社）、「史上第三次」（Wikipedia、澎湃、TVBS）、「9·11 以来最长」（Reuters）；FAA 无官方计数。片中口径：按 FAA 对全部机场下达的停飞令算，9·11 以来第二次（C31）。
  - **数字**：在空飞机 3,100 / 3,500 多 / 4,042；取消 4,467（FlightAware 美国相关）到逾 7,000（NBC，无来源）；解除时刻 20:15 到 20:36（C03–C07、C47、C48）。
  - **500 亿美元**：r1 确认是 Duffy 的要价（ABC、Globe、Scripps）；Reuters 转述 Mullin 估算全面改造约 500 亿，片中不必提；Scripps 同篇另有「再要 300 亿」（C18）。
  - **总价**：315 亿（2025-07）、约 325 亿、300 亿（2026-09，含机场）、500 亿（2026-11）（C21）。
  - **2023 NOTAM 的定性**：FAA 初步调查说触发是承包商维护时误删文件（C34）；GAO 定性为 30 多年老系统的故障（C33）。两层都讲。
  - **「技术人员在调查」的说话人**：「FAA technicians are investigating the issue.」Newsweek 作 FAA 声明，Scripps 归给 Duffy（C41）。
- **尚不清楚**：
  - 确切根因、谁在何时做了什么变更、为什么同时影响全国、备份为什么没接住。
  - 芝加哥先行停飞与全国故障的因果关系及确切时刻。
  - FAA 是否会发布正式调查报告；DOT 监察长、国会听证是否立案或排期。
  - L3Harris 的说法。
  - FAA 官方的最终取消 / 延误统计；周六、周日的最终恢复情况。
  - NATCA、PASS、A4A、众议院交通委员会的表态（未检索到，配额用尽）。
  - 特朗普是否正式宣布「国家紧急状态」（仅 USA Today 转述 Mullin，无文件）。
  - ~~「L3Harris 网络 20 多年 99.999% 可用」~~：r1 核对 L3Harris 2026-05-11 新闻稿没有此说，划掉，不用。
  - 2025 纽瓦克（迁到费城 TRACON 后的长距离链路依赖）能否算「搬迁也是一种动它」：证据链未单独核，暂不用。

---

## 7. 事实核查意见

### 7.1 r1 结论摘要（`research/factcheck_r1.md`，2026-11-14，独立上下文核查员）

- **事实底座大体可靠，引语一致性不过关**：44 条中 25 条通过，19 条需改，删除 0 条。主要问题是转述冒充原话、source 指错（引语不在所给页面）、个别细节写错。
- **C35（2009 FTI）核实了，而且更有力**：DOT 监察长 CC-2010-012 原文写明中断发生在旧网迁新光纤网过程中，根因是临时过渡路由器配错；升为「已证实」，但出错路由器在洛杉矶中心、不是盐湖城，也不是全国停飞令。
- **论点 A 站得住，但要收窄并承认反例与分母**：确认的「改动时出事」只有 2009、2015、2023 三例；达拉斯、费城属论点 B；2004 洛杉矶、2014 ERAM 是反例。第 1 节已按此改写。
- **新进展**：截至 11-14 没有官方根因、初步报告、已排期的国会听证或 NTSB / 监察长立案；只有 Cantwell 说商务委员会会「审查」。新口径：NBC「逾 7,000 班取消」、Reuters 引 Flightradar24 周六已另取消 700 班。

### 7.2 处理情况（逐条）

「需改」19 条全部已改，每条在 `claims.json` 有 `fc_r1` 字段写明改了什么；核不到的子项写在 `verified` 字段。

| id | 处理 |
|---|---|
| C02 | 已改：出处改 Newsweek（原 quote 不在 CBS），quote 换原文并补国际航班句；注明「Federal Aviation Command Center」非正式名。**未能核**：Advisory 111 原文未直读 |
| C04 | 已改：「3,500 多架」，补 Scripps 引 Duffy「all safely landed」；15:36 说话人写 Duffy 与匿名管制员，不采用 NBC 直播「3:36 下令停飞」 |
| C05 | 已改：quote 换 ABC、CBS、NBC 正文原文；4,042 只在 NBC 正文 |
| C06 | 已改：quote 换 Fox 原文；「约晚 9 点」改「当晚」；补 NBC 逾 7,000；删核不到的「近 5,000（ABC、NPR）」 |
| C07 | 已改：quote 换 NBC 直播 20:20 条原文；「约 5,300」改「逾 5,300」 |
| C12 | 已改：TDM 不再写「模拟」，只作 Duffy 原话引用；quote 补 "so this is analog telecom"。**未能核**：「输出不一致数据、关闭系统」无出处，已删 |
| C15 | 已改：note 的「buckle」换成 IBTimes 原句（转述） |
| C16 | 已改：主 quote 保留。**未能核**：Mullin「mechanically driven」在 ABC 两页均无，已从 note 删 |
| C17 | 已改：ASI 声明出处改 USA Today/Yahoo；Mullin 那句换成 "We're not ruling anything out at this point."。**未能核**：原 note 的 Mullin 版本 |
| C25 | 已改：35 亿是合同上限不是中标额（OIG 原文）；补 FTI 合同 2023-04 到期需延期 |
| C31 | 已改：quote 换 ABC 原文、补 Reuters「最长」原句。**未能核**：AP、NPR、新华社、Wikipedia、澎湃、TVBS 的计数说法 |
| C33 | 已改：quote 换 GAO 原文；补 GAO 定性（老旧系统、30 多年），与 C34 两层并列 |
| C35 | 已改：升「已证实」；quote 填 OIG 原文；洛杉矶中心、129 个设施、约 75% 路由断 5 小时、820 班延误；「全国范围通信中断」不是停飞令 |
| C36 | 已改：出处改 The Register 2014（FAA 发言人 Laura Brown）；「新上线」改「仍在全国铺开、洛杉矶中心 2012 年起运行」；约 46 分钟；归为论点 A 的反例 |
| C37 | 已改：TDM → TDMI；L3Harris 一句改原文引号；「两条光纤被切断」改为 FAA 告诉美航；日期注明为推算 |
| C38 | 已改：quote 换 Airways 导语原文；补 Bedford（经 NBC）与 Flightradar24 纽瓦克时刻原句 |
| C41 | 已改：出处改 Newsweek，quote 换原句；注明说话人分歧（FAA 声明 / Duffy） |
| C43 | 已改：依据重分为 A 类 / B 类 / 反例并补分母；claim 收窄为「最严重的那几次」 |
| C44 | 已改：删「Duffy 称 cautionary measure」。**未能核**：该说法无可读出处 |

另外，r1 判「通过」但带小注或未能核子项的条目也已落实（有 `fc_r1` 或 `verified` 字段）：C01、C09、C10、C11、C13、C18、C19、C22、C24、C26、C29、C34、C39。dossier 时间线已改：Duffy X 帖「16:16」改为「17:20 前（时刻未核）」，FAA X 帖改为「17:52 前」；第 6 节「99.999%」已划掉。

**r1 新增 4 条**：C45（2015 华盛顿中心 ERAM 软件升级耗尽内存，A 类；**未能核**：faa.gov 原声明未直读，只核到 Aviation Pros 转载与 Route Fifty 转述，事件日 08-15 为推定）、C46（2004 洛杉矶中心通信中断，反例兼 B 类，IEEE Spectrum）、C47（NBC「逾 7,000 班取消」，无来源，标「有争议」）、C48（Reuters 引 Flightradar24 周五逾 4,700、周六已另取消 700）。

**仍未能核**（不删，进讲稿前视需要补）：Advisory 111 原文、faa.gov 声明页、Duffy 与 FAA 的 X 帖原帖、白宫记者会视频（C01、C02、C09、C10、C12–C14、C18 只核到媒体逐字转引）；C11 的 MS NOW 与彭博；C24 的 DOT「69%」；C29 的事实本身；C08 的 Airways「827 班备降」；欧控 42 国原文；「国家紧急状态」（仅 Mullin 转述）；NATCA、PASS、A4A、众议院交通委员会表态。

### 7.3 进讲稿前要人工做的

1. ~~11-28 前存档 Advisory 111 与 FAA 声明页~~ **已完成（2026-11-14）**：faa.gov 对本机网络返回 Access Denied，取互联网档案馆当日快照，存于 `research/archive/`（见其 README）。C01、C02、C41 已按原文更新；「FEDERAL AVIATION COMMAND CENTER」确是公告原文用词；C41 原句出自 FAA 声明（Scripps 归给 Duffy 有误）。C10 中 Duffy X 帖「all」仍只核到转引。
2. **讲稿定稿前**：再查一次最新进展——FAA / DOT 是否发布根因或初步报告、国会是否排期听证、NTSB 或 DOT 监察长是否立案、L3Harris 是否表态、周六周日最终取消数；有新结论就更新第 1 节「我们为什么仍然这样看」第 3 点、C41、C42，以及论点 A 里「可能还有这一次」的说法。
3. 讲稿用到 C35 note 里 OIG 的补充原句（主备失去分离、91.4% TDM、残余风险）或 C25 的合同延期背景时，挂到对应条目的 `lines`；用到 2015 ERAM 时最好直读 FAA 原声明。
