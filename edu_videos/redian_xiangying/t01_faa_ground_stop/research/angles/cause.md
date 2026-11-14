# 角度 2：技术原因与调查进展

- 检索日期：2026-11-14
- 结论先行：**截至 2026-11-14，官方没有公布确切根因**。目前有三种官方或准官方说法，彼此并不完全矛盾，但侧重点不同；另有几个被排除或未排除的猜测。片中只能说「目前的说法是……」，不能说「原因是……」。

## 一、三种主要说法

### 说法 A：给通信网络打的更新导致重启、崩溃（媒体信源，未经官方确认）

- CBS News 引「多名信源」：连接全美空管系统的私有通信网络做了一次更新，导致系统重启，随后崩溃并造成通信中断；该网络由 L3Harris 运营。L3Harris 未回应置评。
  - 出处：https://www.cbsnews.com/news/faa-issues-nationwide-ground-stop/ ；视频 https://www.cbsnews.com/video/update-to-network-connecting-air-traffic-control-system-led-to-outage-before-ground-stop-sources-ay/
- 《华尔街日报》报道受影响的是 L3Harris 负责的电信网络，承载管制员与飞行员通话所用的无线电频率（转述自 Wikipedia 条目与检索摘要；WSJ 原文 https://www.wsj.com/us-news/faa-temporarily-halts-flights-across-u-s-b9b06e59 付费墙，未读到）。
- 前管制员 Ruth Stilwell 推测可能是语音交换与控制系统（VSCS）的软件更新出错，并说："It would be unusual for them to do a software update during the day, but the FAA is very short-staffed."（Scientific American，https://www.scientificamerican.com/article/faa-grounds-all-u-s-flights-days-after-expanding-its-ai-air-traffic-system/）——这是专家推测，不是事实。
- FAA 与 L3Harris 均未确认 L3Harris 的角色（截至检索时）。

### 说法 B：老旧的模拟（TDM）网络、路由器过载（交通部长 Duffy，官方口径）

Duffy 在白宫外记者会上的原话（逐字引语均经媒体转引）：

- "What we have is an incredibly old air traffic control system."（CBS、Scripps）
- "Our switches, our routers, actually got overloaded with data." 并说这套是模拟电信："We have TDM telecoms."（NBC 直播 20:51 条）
- 路由器过载后 "started to give us inconsistency in the data"，于是 "we shut the system down"（NBC 直播；CBS）
- "We didn't lose all telecom, we didn't lose all radar."（NBC 直播 20:44；Globe and Mail 20:56）
- 受影响的是 "instability for our radar and our communications in our centers, in our TRACONS throughout the country."（NBC 直播 20:44）
- "We use 1980s little copper lines. It's an old system that went down and went down everywhere. It got overloaded."（ABC 直播，https://abcnews.com/US/live-updates/faa-ground-stop-live-updates-hundreds-flights-canceled/?id=138125140）
- "I think our fix gives us a pretty good indication that it was a legacy network problem that went down"（ABC 直播）
- "By the way, all of the new equipment that we put in, none of that went down."（ABC 直播）；USA Today 转述：已改成数字 IP 的中心没有出现这个问题。
- Open Jaw 的归纳："Neither official explained what caused the data surge or why it hit facilities across the country at once."（https://openjaw.com/newsroom/airline/2026/11/13/faa-lifts-nationwide-ground-stop-but-delays-will-roll-into-the-weekend/）——**这正是说法 B 的缺口**：路由器为什么在那一刻突然全国性过载，Duffy 没解释。

### 说法 C：给旧系统打补丁 / 新设备压垮旧系统（国土安全部长 Mullin）

- Globe and Mail 直播（21:29）转述：Mullin 说问题似乎始于给较旧技术打 "patches"，并引其原话 "that new equipment and new technology was overwhelming the older system."（https://www.theglobeandmail.com/world/article-faa-ground-stop-us-flights-live-updates/）
- Reuters（经 Yahoo 转载）转述：Mullin 说把新设备加进旧系统使其 "buckle"，称这是一个重大工程问题（无直接引语）。
- Axios 转述：官员在查旧设备与正在安装的新技术之间的「不兼容」（Axios 原页 403，转述自检索摘要）。
- Mullin 原话："It appears that this was mechanically driven. However, we're still looking, so we're not going to rule that out."（ABC 直播）

### 三种说法怎么拼起来（我们的判断，待官方确认）

A（网络更新触发重启崩溃）、B（旧 TDM 路由器过载、新 IP 设备没事）、C（补丁 / 新设备压垮旧系统）**可以是同一件事的三个侧面**：在一张新旧并存、正在迁移的网络上做了一次变更，旧设备承受不了，故障沿着共享网络扩散到全国。Duffy 强调「旧的坏了」，Mullin 和 CBS 信源指向「改动触发」。两种强调对应两种政策叙事：前者支持「赶紧拨钱换新」，后者提醒「换新的过程本身就是风险」。这一拼接是我们的推断，片中必须标「我们的判断」，并说明依据只是三方公开表述。

## 二、被排除或尚未排除的猜测

| 猜测 | 状态 | 出处 |
|---|---|---|
| 网络攻击 | 无证据，未完全排除。Mullin："We have seen zero evidence that this was a cyberattack"（Scripps）；"So far what we've seen there is no cyberattack. We're still working through that process."（NBC 直播 20:37）；Fox 引 Doocy 转述特朗普：不像网络攻击或 AI，"a bunch of old broken stuff" | Scripps、NBC、Fox |
| AI 工具 SMART（11-10 刚扩展到全部 22 个中心） | 供应商 Air Space Intelligence："The current ground stop is not based on or a result of the SMART system."；Wikipedia 称 FAA 否认；Mullin 被问时说 "You just can't rule out anything at this point" | ABC、NBC 直播、The Register |
| 微软同期故障 | 微软："no indication that the FAA nationwide ground stop is related"；Mullin 也说无关 | NBC 直播 19:10；CBS |
| 芝加哥 Midway 的路由器问题蔓延全国 | CNN 曾报道 FAA 对航司这么说（转述自 Clash Report，https://clashreport.com/world/articles/faa-orders-nationwide-ground-stop-citing-extraordinary-circumstances-rj94ktbb7uf）；Wikipedia 称 FAA 否认。两者都未能读到一手原文 | 有争议 |
| 国家气象局雷达也全国中断 | 不实。NWS 称其雷达正常，网传是过时网页（NBC 直播 18:58） | NBC |

## 三、背景：出故障的是哪张网

- **FTI（FAA Telecommunications Infrastructure）**：FAA 的电信骨干，2002 年由 Harris（现 L3Harris）以 35 亿美元合同中标（Nextgov 2009，https://www.nextgov.com/digital-government/2009/11/faa-it-failure-puts-shadow-on-harris-contract/250536/）。The Register 称其连接 "more than 4,400 facilities"（https://www.theregister.com/offbeat/2026/11/13/faa-lifts-ground-stop-after-hours-long-delays-snag-travelers/5309912）。FAA 的 FENS 页面称 FTI 支持约 28,000 项电信服务（转述自检索摘要，FAA 页 https://www.faa.gov/air_traffic/technology/cinp/fens 403 未读到）。
- **FTI 正在现代化**：L3Harris 2026-05-11 新闻稿称已完成逾 50%，"on track" 于 2027 年完成；每月部署 150–200 条新网络路径；约 45,000 个日航班依赖这套系统；采取 "build-then-switch"（新设施与旧系统并行安装测试再切换）；新设施 "designed to support legacy systems during the transition"（https://www.l3harris.com/newsroom/editorial/2026/05/l3harris-reaches-over-50-faa-telecommunications-modernization）。
- **继任网络 FENS**：2023 年 FAA 选 Verizon 承建 15 年、24 亿美元的 FENS，取代 L3Harris 的 FTI（Washington Technology，https://washingtontechnology.com/companies/2023/03/faa-selects-verizon-24b-telecommunications-contract/384517/；Aviation Week）；2026-08-11 FAA 改由 AT&T 担任 FENS 主承包商，替换 Verizon（Aviation Week，2026-08-27，https://aviationweek.com/air-transport/safety-ops-regulation/faa-taps-att-build-its-next-telecom-backbone ，付费墙，仅读到导语）。为维持服务，FTI 合同已延期（HigherGov 公告，https://www.highergov.com/contract-opportunity/announcement-of-fti-single-source-extension-dtfa0102d03006-ssj-22-0001-u-9b1f3/）。
- 也就是说，事发时美国空管电信处在**三层并存**状态：旧的 TDM/铜线 FTI、L3Harris 正在做的 FTI 现代化（光纤、无线、卫星、IP）、刚换主承包商的下一代 FENS。哪一层出的问题，官方未说清。
- FAA 局长 Bryan Bedford 2026-09-21 费城 TRACON 故障后的原话很能说明这种「换表皮不换骨架」的状态："We're pulling copper up and putting fiber down, but it's the same data architecture that we've had for 50 years."（Airways Magazine 转引，https://airwaysmag.com/new-post/faa-northeast-ground-stops-severed-fiber-philadelphia-tracon）
- 参议院商务委员会（主席 Cruz）："No new ARTCC has been built since LBJ was in office."（USA Today 转引委员会帖子）——即 1969 年以来没有新建航路管制中心。

## 四、先例：「升级 / 迁移引发故障」与「备份没接上」在这张网上并不新鲜

| 日期 | 事件 | 机制 | 出处 |
|---|---|---|---|
| 2009-11-19 | FTI 发生全国范围（NAS-wide）中断，飞行计划系统受影响，全美延误 | DOT 监察长 2010-06 报告（据检索摘要）：盐湖城中心迁入光纤网时引入的配置错误潜伏未被发现；Harris 工程师为让洛杉矶一台新路由器上线而断开链路，新路由器带着同样错误；工会称备份路由器没接上。FAA 早期说法是盐湖城一台路由器软件配置问题 | OIG 报告 PDF（存档，未能读出全文）https://webarchive.library.unt.edu/web/20161103185913/https://www.oig.dot.gov/sites/default/files/WEB%20FILE2_FTI%20%20Nov%2019%20outage-6-18-10_Final%20Signature%28a%29%20%282%29.pdf ；Nextgov 2009-11-20 |
| 2006–2010 | DOT 监察长多份报告批评 FTI 过渡：进度、过渡计划、主备服务都出现中断 | 2006 报告 AV-2006-047："Until FAA develops a realistic schedule and effective transition plan, it will be difficult to hold the FTI contractor accountable…"（检索摘要转引，需打开原 PDF 核对） | https://webarchive.library.unt.edu/web/20161101203519/https://www.oig.dot.gov/sites/default/files/av2006047.pdf |
| 2023-01-11 | NOTAM 系统故障致全国停飞约 90 分钟 | 承包商人员误删文件（NBC 直播 19:51 转述 DOT） | 详见 history.md |
| 2025-09-19 | 达拉斯两大机场停飞约 5 小时 | FAA 归因于 Frontier 提供的 TDM 数据电信服务多次故障，并点名 L3Harris 未确保冗余有效；FAA 称其为 "clear example of the FAA's outdated infrastructure"；美航 COO 称两条光纤被切断，主备路径同时中断 | CBS Texas，https://www.cbsnews.com/texas/news/outdated-infrastructure-faa-dallas-airport-ground-stops |
| 2026-09-21 | 费城 TRACON 主电路故障，切备份时发现备份光纤已被施工挖断；纽瓦克约 09:40–17:20 无商业航班落地 | 主备「物理上不独立」 | Airways Magazine（同上） |

**规律（我们的判断）**：这张网反复出问题的不是「某个零件老了」，而是两类结构性问题：(1) 改动（迁移、上线新设备、打补丁）在新旧混合的系统上触发连锁故障；(2) 纸面上的冗余在关键时刻不独立或没生效。11-13 这次到底属于哪一类，要等调查。

## 五、调查进展（截至 2026-11-14）

- FAA："FAA technicians are investigating the issue. We will provide updates."（经 CNBC、Scientific American 转引）
- Duffy："We're still working on the details of what went wrong today."（检索摘要转引，原出处待核）
- Duffy：恢复需要时间，"it's going to take us some time to unwind what's happened this afternoon"，"hopefully tomorrow we are going to start to see far better movement"（ABC 直播）
- 国会：Duckworth 称要 "demanding answers from the FAA"，并说事件 "will warrant a thorough and complete investigation"；Cantwell 称商务委员会将审查 "Technology issues related to how planes communicate through primary frequencies, backup frequencies"（USA Today、ABC）。
- 未见：NTSB 介入（这不是事故，通常不由 NTSB 调查——这是常识推断，需核实）、DOT 监察长立案、L3Harris 声明、FAA 正式初步报告。均写「尚不清楚」。

## 六、对论点有用的观察（我们的判断）

1. 「全国停飞」本身是安全设计在起作用：数据不一致时宁可停飞，Duffy 称 "cautionary measure"，前管制员 Stilwell 说 "The ground stop was the right thing to do."——事故的代价是航班和钱，不是人命。
2. 官方叙事在「旧设备太老」，但证据也指向「改动触发」。升级是必须的，可升级的过渡期是一个系统最脆弱的时候：新旧两套都在跑、都要维护，接口最多。
3. 「为什么一个点的问题会变成全国」——一张共享的电信骨干网是全国 22 个中心的共同依赖；冗余如果共享同一张网、同一种设备、同一次变更，就不是真冗余。
