# 角度：别人已经讲过什么（coverage）

检索日期：2026-11-14（北京时间上午；事件发生于美东 2026-11-13 周五，距检索不足 24 小时，多数报道仍在滚动更新）

> 本文件只归纳「媒体和平台怎么讲」，不替代 `timeline.md` / `cause.md` / `stakeholders.md` 的事实核查。表中的数字、原因说法都是**该来源当时的说法**，不代表已证实。凡写「转述自」的，原始出处是另一家媒体或匿名消息人士。

---

## 0. 检索覆盖度（先说清楚查到了什么、没查到什么）

| 范围 | 覆盖情况 |
|---|---|
| 英文电视网 / 通讯社 | CBS、NBC、ABC、CNBC、MS NOW、NPR（仅搜索摘要，正文抓取超时）、AP（经 PBS 转载全文）、Reuters（只见他报转引；直连被搜索工具屏蔽）、CNN（直播页 HTTP 451，仅见他报转引）、Al Jazeera、DW、CBC（YouTube 标题） |
| 报纸 | **NYT、WSJ、WaPo、Bloomberg 未能直接读到**：NYT / WSJ 被搜索工具屏蔽，WaPo / Bloomberg 未检索到原文（检索后期搜索额度用尽）。文中关于它们的内容全部是他报转引 |
| 科技媒体 | The Register、Gizmodo（403，仅标题/转引）、Jalopnik、Make Tech Easier、CNET（仅经维基转引）。**Ars Technica、The Verge、Wired 被搜索工具屏蔽，是否有报道尚不清楚** |
| 航空专业媒体 | View from the Wing、AvWeb、Flying、Simple Flying、AeroTime、Airways、Aviation Week（付费墙，只读到导语）、Flightradar24 博客（403）。**AIN 未检索到本事件报道**；The Points Guy 只检索到 2023 年 NOTAM 事件旧文，本次报道尚不清楚；The Air Current 只见凤凰网转引 |
| 评论 / 社区 | Hacker News（帖子 50491855 及父帖 50489641）、Substack 若干、aerocorner 博客、Kalshi 预测市场、CSDN 博客。**Reddit 未检索到具体帖子** |
| 中文大陆 | 新华社 / 人民网、中新网、澎湃（含澎湃号转载观察者网等）、界面、IT 之家（403，仅标题与摘要）、腾讯 / 网易 / 新浪转载、凤凰网、中财网、自媒体「牛弹琴」。**环球时报 / 环球网、央视原发页、财新、第一财经、虎嗅、知乎未检索到原文**（央视仅见「CCTV 国际时讯」署名的转载） |
| 台港及海外中文 | 中央社、联合报 / 世界日报、中时、自由时报、ETtoday、TVBS、风传媒、明报、星岛、HK01、马来西亚中国报。BBC 中文、DW 中文、RFI、联合早报被搜索工具屏蔽 |
| 视频平台 | YouTube：用 oEmbed 拿到 19 条视频的标题与频道，**播放量页面被反爬拦截，尚不清楚**。B 站：公开搜索接口可用，拿到 11-13 以后上传的相关视频及播放量（截至北京时间 11-14 约 11:00）。**抖音、微博热搜：接口拒绝访问（微博 `Forbidden`），热搜排名与阅读量尚不清楚** |

结论：英文主流的**主叙事**和中文的**转述链**覆盖较好；美国大报原文、科技深度媒体、抖音 / 微博热度是明显盲区，后续如要补，应人工在浏览器里查。

---

## 1. 英文主流媒体

| 来源 | 链接 | 主要角度 | 影响力 | 缺了什么 |
|---|---|---|---|---|
| CBS News | https://www.cbsnews.com/news/faa-issues-nationwide-ground-stop/ | **首发「更新→重启→崩溃」说法**（「多位消息人士」：连接空管系统的私有通信网络更新导致系统重启，重启后崩溃）；点名 L3Harris 运营该网络；Duffy「老系统」「不拨款还会有更多」；前 NTSB 主席 Sumwalt 称「absolutely unprecedented」 | 全国电视网，是此后几乎所有媒体（含中文）「软件更新」说法的源头之一 | 没解释为什么一次更新能同时打到全国、备份为什么没接住；把「更新」和 Duffy 的「老旧路由器过载」并列，不分析两者关系 |
| NBC News | https://www.nbcnews.com/news/us-news/faa-orders-nationwide-ground-stop-departing-flights-reasons-safety-rcna609247 | 时间线最细（15:36 发现雷达与通信数据不稳 → 15:54 发停飞 → 20:15 解除，数字来自 Duffy）；乘客滞留、机场满位；专家估算 30–40 万人滞留；ASI 声明 SMART 不是原因 | 全国电视网；YouTube 上 NBC News 有特别报道与突发两条视频 | 正文说「持续五个多小时」与自己列的时间（约 4 小时 20 分）矛盾；无技术机制 |
| ABC News | https://abcnews.com/US/nationwide-ground-stop-ordered-airports-faa/story?id=138121848 | 「是不是攻击」：Mullin「这不是又一次 9·11」「目前还不知道」；SMART AI 系统嫌疑；参议员 Duckworth「天空安全建立在冗余之上」、Cantwell 要审查主备频率 | 全国电视网；YouTube ABC News 两条 | 提到「冗余」但只是议员一句话，没有展开冗余为何失效 |
| MS NOW | https://www.ms.now/news/faa-ground-stop-all-flights-nationwide | 政治与拨款：Duffy 借机要 300 亿美元、警告「还会有更多」；民主党 Booker「不管是被攻破还是自己坏了都不可接受」；司法部消息源称是「频率问题」；搜索摘要显示一名联邦官员向 MS NOW 证实「软件更新导致」（抓取到的正文版本未见此句，可能已改版） | 有线电视网；YouTube 两条直播 / 突发 | 「老旧硬件坏了」与「软件更新」两说并存，未调和 |
| CNBC | https://www.cnbc.com/2026/11/13/faa-ground-stop.html | 航空公司运营与恢复：Cirium 数据（16 点后原定 1.1 万班、150 万旅客）、约 600 班备降 / 返航、JetBlue 内部备忘录取消周六航班以重新调配机组；把事件放进「老化 + 人手短缺」的系列（9 月 Verizon 光纤被挖断、2025 纽瓦克故障） | 财经电视网；另有视频 https://www.cnbc.com/video/2026/11/13/faa-issues-nationwide-groundstop.html | 讲了「恢复要多久」，没讲为什么恢复比停下难（机组执勤时限、飞机错位的连锁） |
| AP（经 PBS 转载） | https://www.pbs.org/newshour/nation/faa-grounds-all-flights-at-u-s-airports-due-to-air-traffic-control-communications-problems | 标准通讯稿：22 个区域中心受影响（Duffy）；至少 600 班备降（496 返回始发地）；「9·11 后第二次」；与 9 月东北部中断相似「但是全国规模」 | 通讯社，被大量地方台、中文媒体（经 NOWNEWS 等）转用 | 无机制分析 |
| Reuters（转引） | 转引见 IBTimes：https://www.yahoo.com/news/us/articles/faa-lifts-nationwide-ground-stop-020705860.html | 「9·11 以来时间最长的全国停飞」；Flightradar24 数据：周五取消 4,700+、延误 1 万、周六再取消约 700 | 通讯社 | 原文未读到，尚不清楚 |
| WSJ（转引） | 转引见 HN：https://news.ycombinator.com/item?id=50491855 ；Wikipedia | **首发「L3Harris 监管的电信网络」**：该网络承载管制员与飞行员通话的关键无线电频率；雷达是否受影响当时不明 | 大报，「L3Harris」说法源头 | 原文未读到 |
| NYT（转引） | 转引见 Wikipedia：https://en.wikipedia.org/wiki/2026_United_States_ground_stop | 机位爆满、备降小机场；阿拉斯加 / 夏威夷豁免；据澎湃 / 搜索摘要，NYT 前一天刚发过质疑航空安全的文章（牛弹琴引用） | 大报 | 原文未读到，尚不清楚 |
| Bloomberg（转引） | 转引见中新网：https://www.chinanews.com.cn/gj/2026/11-14/10731883.shtml ；TVBS | 「知情人士」：FBI 认为不是网络攻击或犯罪，调查方向之一是软件更新 | 财经通讯社；这是中文「调查指向软件更新」的主要源头 | 原文未读到 |
| NPR | https://www.npr.org/2026/11/13/nx-s1-6040403/faa-nationwide-groundstop-airports | 约 4 小时；9·11 以来第二次；Eurocontrol 应 FAA 要求暂停欧洲赴美航班 | 公共广播 | 正文抓取超时，仅见摘要 |
| Al Jazeera | https://www.aljazeera.com/news/liveblog/2026/11/13/groundling-live | 「FAA 归咎于过时设备」；15:54–20:15 | 国际台 | 直播页，细节少 |
| IBTimes（雅虎转载） | https://www.yahoo.com/news/us/articles/faa-lifts-nationwide-ground-stop-020705860.html | Duffy 老系统 + Mullin「新技术接入旧系统把它压垮」；Mullin 估全面改造约 500 亿美元 | 中等 | 汇编稿 |
| The Register | https://www.theregister.com/offbeat/2026/11/13/faa-lifts-ground-stop-after-hours-long-delays-snag-travelers/5309912 | 科技媒体口吻：FTI（FAA 电信基础设施）由 L3Harris 管理、连接 4,400+ 设施；澄清与同期微软宕机、SMART 无关 | 科技圈中等 | 讲了 FTI 是什么，没讲它为什么是单点 |
| Jalopnik | https://www.jalopnik.com/2316628/faa-orders-nationwide-ground-stop-communication-issues/ | 「肯定不是新 AI 空管工具……大概吧」：SMART 前一天刚全国铺开；顺带提 FAA 刚开始淘汰软盘 | 汽车 / 交通圈 | 以调侃代替解释 |
| Make Tech Easier | https://maketecheasier.com/faa-ground-stop-telecom-outage-flight-status-refunds/ | 服务稿：怎么查航班、DOT 退款规则（取消一律可退；国内晚到 3 小时 / 国际 6 小时算「重大延误」） | 小 | 纯服务，无机制 |
| WWD Sourcing Journal | https://wwd.com/sourcing-journal/logistics/faa-nationwide-us-ground-stop-stoppage-air-cargo-freight-ups-fedex-1239416489/ | 航空货运积压（UPS / FedEx） | 行业 | 仅标题检索到，正文未读 |

## 2. 航空专业媒体与评论 / 社区

| 来源 | 链接 | 主要角度 | 影响力 | 缺了什么 |
|---|---|---|---|---|
| View from the Wing（Gary Leff） | https://viewfromthewing.com/faa-ground-stop-every-u-s-airport-departure-halted-as-air-traffic-control-communications-fail/ | **制度与激励**：FAA 既运营又监管；多年期工程靠年度拨款；「买设备修不好坏激励和项目管理」；反对让纳税人而非航司 / 乘客买单；转述管制员论坛说「备用站点同时失效」（未证实）；读者评论「几十年技术债回家的一周」 | 常旅客圈头部博客 | 最接近「技术债经济学」，但停在治理批评，没讲冗余同时失效的技术机制 |
| AvWeb | https://avweb.com/aviation-news/nationwide-ground-stop-atc-comm-problems/ | 规范快讯：ATCSCC 原文、22 个中心、125 亿已批 + 301 亿新请求 | 飞行员圈 | 无分析 |
| Flying | https://www.flyingmag.com/air-space-is-reopened-faa-lifts-nationwide-ground-stop/ | 「过载的老旧模拟交换机」；副标题称 Mullin 说技术更新「压垮」系统；Duffy 要 500 亿 | 通航圈 | 把「老」和「更新」写在同一篇但没连起来 |
| Simple Flying | https://simpleflying.com/breaking-faa-issues-nationwide-ground-stop/ | 滚动更新，转述 CBS 记者 Olivia Rinaldi 的「更新→重启→崩溃」 | 流量大的航空站 | 时间线有明显错误（写成 17:30 发令）；无机制 |
| AeroTime | https://www.aerotime.aero/articles/faa-nationwide-ground-stop-atc-communications-november-2026 | 白宫追加 301 亿（其中 101 亿空管）的请求恰在停飞前几小时提交；回顾 2023 NOTAM「同步主备数据库时误删文件」 | 欧洲航空媒体 | 只在 2023 案例里碰到「主备同步」，没联系本次 |
| Airways | https://www.airwaysmag.com/new-post/faa-ground-stop-microsoft-outage-november-13 | 与同期微软全球宕机并列（两者无关）；Cirium 备降数 827 | 航空 | 无机制 |
| Aviation Week | https://aviationweek.com/air-transport/safety-ops-regulation/faa-issues-nationwide-ground-stop-citing-atc-communication | 付费墙，仅见导语 | 行业权威 | 尚不清楚 |
| aerocorner 博客 | https://aerocorner.com/blog/faa-nationwide-ground-stop/ | **少见的结构性一句话**：「一个中心黑掉只是一个区域变慢；同时碰到所有中心，FAA 就无处绕行」「一次更新就能全国宕机的网络是设计问题」；提到 AT&T 2026-08 拿到 7,430 万美元首期订单、2028 年底前替换 FTI | 小 | 点到为止，没讲共模故障、没讲为什么替换要十几年 |
| Hacker News | https://news.ycombinator.com/item?id=50491855 （父帖 item 50489641） | **工程师视角**：周五 15 点改关键基础设施合理吗；为什么没有热备 / 蓝绿部署 / 滚动发布；「回滚只能在已经崩了的服务器上跑」；FTI 2002–2007 建成；私有网络集中风险 | 技术圈；点赞 / 评论数页面未显示，尚不清楚 | 大量是猜测和跑题（L3Harris 前 CEO），没有人系统讲清 |
| Kalshi 预测市场 | https://news.kalshi.com/p/odds-faa-the-ground-stop-cause | 把原因做成赌盘：系统故障 94%、L3Harris 81%、承包商失误 76%、维护 / 升级 45% | 小众但被转引 | 赔率不是证据 |
| Substack（Thy Back Door 等） | https://thybackdoor.substack.com/p/faa-ground-stop-raises-questions ；https://divaboomer.substack.com/p/22-regional-atcs ；https://nimbuskey.substack.com/p/blog-144a-alert-the-day-critical | 多为 AI / 微软 / 国土安全部阴谋或疑问向 | 小 | 无可靠信源 |
| The Ohio Register | https://www.theohioregister.com/faa-lifts-rare-nationwide-ground-stop-after-telecom-crash-sparks-ai-and-diplomatic-speculation/ | 「AI 与外交猜测」 | 小，信源弱 | 不宜引用 |

## 3. 中文媒体

| 来源 | 链接 | 主要角度 | 影响力 | 缺了什么 |
|---|---|---|---|---|
| 新华社 / 人民网 | https://www.news.cn/world/20261114/5985e89f140a473a974e55a04967ce55/c.html ；http://world.people.com.cn/n1/2026/1114/c1002-40833685.html | 通稿：「近 7000 架次延误或取消」、9·11 后第二次；转引 Eurocontrol 通告 | 权威通稿，被大量转载 | 纯事实，无解释 |
| 中新网 | https://www.chinanews.com.cn/gj/2026/11-14/10731883.shtml | 「知情人士称调查指向软件更新」（转述自彭博社） | 大 | 未注明原始媒体 |
| 澎湃（记者南博一） | https://www.thepaper.cn/newsDetail_forward_34474213 | 「国土安全部长：不是又一次 9·11」；称本次为「近年第三次全国性停飞令」 | 大 | 无机制 |
| 澎湃号转载观察者网 | https://www.thepaper.cn/newsDetail_forward_34474921 （凤凰网转载 https://news.ifeng.com/c/8y2OJv6Z0ZL ） | 「上上次还是 9·11」：历史罕见 + 设备老化 + 资金缺口；专家说本次与 9·11 不同，空中飞机没被要求立即落地 | 大 | 碰到了「这是有分寸的停飞」，但没提升为「安全设计」 |
| 澎湃号「知情人士：调查指向软件更新」 | https://www.thepaper.cn/newsDetail_forward_34475386 | 软件更新 + 欧洲赴美航班暂停 | 大 | 同上 |
| 界面快讯 | https://www.jiemian.com/article/15332816.html ；https://www.jiemian.com/article/15332834.html | 「美媒称调查指向软件更新」「特朗普说与网络攻击无关」；新浪转载署「CCTV 国际时讯」 | 中 | 快讯 |
| IT 之家 | https://www.ithome.com/1/026/999.htm | 标题「8000 架次延误 + 3100 架在空中，FBI 初步排除网络攻击」；摘要称约半小时内由芝加哥局部停飞升级为全国 | 科技圈大流量 | 正文 403 未读，是否有技术解释尚不清楚 |
| 牛弹琴（自媒体，新浪财经 / 网易转载） | https://finance.sina.com.cn/wm/2026-11-14/doc-iniysepm3110515.shtml | 「一觉醒来，美国发生了一件不该发生的事」：基建锈蚀、制度低效、「花数万亿防外敌，却被内部技术问题击垮」；软盘、Windows 95、35 年雷达 | 头部时政自媒体，转载广 | 自称「不是专家」，技术几乎为零；是「美国衰落」叙事，**不是严格的中美对比** |
| 中财网 | https://www.cfi.net.cn/p20261114000005.html | 「航空系统老化风险凸显」 | 小 | — |
| CSDN 博客 | https://blog.csdn.net/feixin369/article/details/170759339 | 「美国空管系统脆弱性的一次压力测试」：提出「冗余不足」「技术债」，结论是「要多少次才能换来冗余投入」 | 小 | 有方向无机制，没讲冗余为何同时失效 |
| 中央社 | https://www.cna.com.tw/news/aopl/202611140013.aspx | 9·11 后第二度；转述 Gizmodo 讲 SMART 前一天上线 | 台湾通讯社 | 无机制 |
| 联合报 / 世界日报 | https://udn.com/news/story/6813/9878089 ；https://www.worldjournal.com/wj/story/121469/9878096 | 「官员曝原因：不是另一起 911」 | 大 | — |
| 中时 | https://www.chinatimes.com/realtimenews/20261114001287-260408 | 解除后统计：FlightAware 全天延误 9,814、取消 5,117（注明是全天）；Duffy「坏的是老设备」 | 大 | — |
| 自由时报 / ETtoday | https://news.ltn.com.tw/news/aichannel/breakingnews/5640271 ；https://www.ettoday.net/news/20261114/3271937.htm | **AI 嫌疑**：「FAA 新 AI 航管系统上线三天后全美停飞」「国土安全部锁定 AI 辅助航管系统调查」 | 大 | 标题放大了未证实的关联 |
| TVBS | https://news.tvbs.com.tw/world/4050384 | 「逾 3500 架在空中！惊险内幕」：空中飞机从 3,500 降到不足 400 架；称「美国史上第 3 次」 | 大 | 「惊险」框架与实际（空中飞机正常落地）有张力 |
| 风传媒 / 明报 / 星岛 / HK01 | https://www.storm.mg/article/11181478 ；https://news.mingpao.com/ins/%E5%9C%8B%E9%9A%9B/article/20261114/s00005/1794618180339/ ；https://www.stheadline.com/realtime-world/3636973/ ；https://global.hk01.com/%E5%8D%B3%E6%97%B6%E5%9B%BD%E9%99%85/60410669/ | 快讯为主 | 中 | — |
| 腾讯 / 网易 / 新浪转载 | https://news.qq.com/rain/a/20261114A0519R00 ；https://www.163.com/dy/article/LBM8BDS60514R9P4.html | 「特朗普已听取简报」「9·11 后第二次」 | 大（聚合分发） | — |

**未找到**：环球时报 / 环球网、观察者网原站、财新、第一财经、虎嗅、知乎、央视原发页（尚不清楚是否有报道或评论）。

## 4. 视频平台

### YouTube（标题与频道经 oEmbed 核实；播放量全部尚不清楚）

| 频道 | 标题 | 链接 | 角度 |
|---|---|---|---|
| NBC News | Special Report: FAA orders nationwide ground stop after 'telecommunications outage' | https://www.youtube.com/watch?v=lU0PHCZ_FsU | 特别报道 |
| NBC News | BREAKING: FAA issues nationwide ground stop due to 'reasons of safety' | https://www.youtube.com/watch?v=1hf95H__vqo | 突发 |
| ABC News | Nationwide ground stop ordered at airports: FAA | https://www.youtube.com/watch?v=ZRwv8ypbOfw / https://www.youtube.com/watch?v=JBluHJic6_I | 突发 |
| CNN | FAA orders nationwide ground stop due to 'extraordinary circumstances' | https://www.youtube.com/watch?v=TllFNw4zGXQ | 突发 |
| MS NOW | BREAKING: Nationwide ground stop issued in U.S. for ALL AIRCRAFT in 'EXTRAORDINARILY UNUSUAL' move | https://www.youtube.com/watch?v=2-K0zDqZL-w | 罕见性 |
| MS NOW | LIVE: White House officials brief after FAA declares nationwide ground stop | https://www.youtube.com/watch?v=csgeHC8s2Xo | 白宫发布会（Duffy / Mullin 一手原话） |
| FOX NASHVILLE | LIVE NOW: White House Addresses Nationwide Ground Stop | https://www.youtube.com/live/CC4iCGetGhI | 同上 |
| Scripps News | Why did the FAA ground all flights nationwide? What we know | https://www.youtube.com/watch?v=ZlR87sJXIZw | 「为什么」，但标题是 what we know 型 |
| USA TODAY | LIVE: Flight tracker map shows air travel conditions after … ground stop lifted | https://www.youtube.com/watch?v=vu0GNcuW2ck | 航迹图直播 |
| DW News / CBC News | US Federal Aviation Administration grounds all flights nationwide；FAA issues ground stop for aircraft across the U.S. | https://www.youtube.com/watch?v=PHrKctUUQ9o ；https://www.youtube.com/watch?v=M9EGD8TWnG8 | 国际台 |
| 地方台（FOX 5 NY、WSMV、WDIV、KOMO、FOX 2 Detroit、KTLA） | 直播 / what we know / 乘客滞留 | https://www.youtube.com/watch?v=v9zJYIa44iY 等 | 本地机场乘客 |
| Famous Places, Real Stories | The System Is Down: Why the FAA Grounded Every U.S. Flight | https://www.youtube.com/watch?v=u-nTXSo0190 | 唯一检索到的「解说型」，小频道 |

另有 TMZ 西南航空机长广播片段（https://www.tmz.com/2026/11/13/faa-issues-rare-nationwide-ground-stop-orders-all-departing-flights-halted/ ）、Fox Business 丹佛机场与空管广播录音。**航空解说频道（Mentour Pilot、blancolirio、VASAviation、74 Gear 等）截至检索时未检索到相关视频**——这是一个空档，但也可能 24 小时内就会补上。

### B 站（公开搜索接口，播放量截至北京时间 2026-11-14 约 11:00）

| UP 主 | 标题 | 链接 | 播放 | 角度 |
|---|---|---|---|---|
| 俄乌前线 | 突发！FAA 紧急向全美下达最高级别全国地面停飞令…… | https://www.bilibili.com/video/BV1wdWr6JEbM | 11,813 | 突发、强调「无一例外」 |
| 云上一孤舟 | 全美飞机停飞。911 以来全美所有离港航班第二次被叫停。 | https://www.bilibili.com/video/BV1cFWk62ETp | 4,162 | 搬运 FAA / Duffy 原话 |
| 纯正英语原声30秒 | 【CBS 附文稿】FAA 因系统软件崩溃发布罕见全国范围停飞令 | https://www.bilibili.com/video/BV1YRW66cELB | 1,934 | 英语学习搬运；简介写「逾 2.1 万架次延误」（来源未注明） |
| 一只提莫啊 | 美国 FAA 下令全国地面停飞，约 7000 航班受影响 | https://www.bilibili.com/video/BV1FfWr67EHY | 1,065 | 新闻综述 |
| 阿尔法小分队字幕组 | 全美航班趴窝！系统更新导致航空管制通信中断 FAA 紧急停飞 | https://www.bilibili.com/video/BV12KWr6XECA | 848 | 字幕搬运 |
| dailyfake | CNN News 美国 FAA 停飞所有航班：航空专家目前所知的情况 | https://www.bilibili.com/video/BV13iWr6AEyq | 793 | CNN 搬运 |
| 财经抱抱君 | 突发！911 后首次！！美国遭遇全国停飞禁令 | https://www.bilibili.com/video/BV1nEWr6yEP7 | 784 | 英语学习；「911 后首次」说法有误 |
| 柴郡ing | 突发：全美空管设备瘫痪，所有航班地面停止 | https://www.bilibili.com/video/BV1NDWr6XEYv | 380 | 简介写「多个 ARTCC」 |
| 赵巍专栏 | 一铲锁死全美空域，FAA 的冗余骗局 | https://www.bilibili.com/video/BV15hWr6iE9D | 12 | **唯一以「冗余」为题**；「一铲」暗指挖断光纤（与本次「更新」说法不符，可能混入了 2025 达拉斯 / 2026-09 东北的光纤事故），简介为空 |

B 站整体：上线不足半天，热度最高约 1.2 万播放；**以搬运英文新闻和英语学习素材为主，尚无一条讲清机制的解说**。

### 抖音 / 微博

尚不清楚。微博接口返回 `Forbidden`，抖音未能检索；搜索摘要中能看到大量微博转发「9·11 后第二次」「近 7000 架次」「22 个区域管制中心」，但**热搜排名、话题阅读量都没有查到**，不编。

---

## 5. 主要角度类型归纳

| # | 角度 | 代表来源 | 说明 |
|---|---|---|---|
| A | **美国基建老化 / 要钱**（最主流，官方主推） | Duffy 本人；CBS、CNBC、AP、MS NOW、Flying、Al Jazeera；中文：观察者网（澎湃转）、牛弹琴、中时、TVBS、中财网 | 叙事链：老设备 → 坏了 → 国会快拨款（300 / 301 / 500 亿）。软盘、Windows 95 成为固定梗 |
| B | **是不是攻击 / 不是又一次 9·11** | ABC、CBS、NBC、PBS/AP；澎湃「不是又一次 9·11」、联合报「不是另一起 911」、新华社「9·11 后第二次」 | 罕见性 + 安抚；Mullin「零证据」但「不排除任何可能」 |
| C | **AI 系统（SMART）/ 微软宕机巧合** | Jalopnik、ABC、The Register、Airways；自由时报、ETtoday、中央社；Substack | 承包商 ASI 否认；无证据，但标题流量高 |
| D | **乘客与航司：滞留、退款、恢复** | CNBC、NBC、Make Tech Easier、KTLA、地方台；JetBlue / 美航 / 联航声明 | 服务稿；TPG 本次报道尚不清楚 |
| E | **问责与政治 / 治理** | MS NOW（Booker、Cantwell）、ABC（Duckworth）、View from the Wing（FAA 激励问题）、Trump（Fox，经界面 / 澎湃转） | 民主党追问「冗余」「问责」；Leff 批 FAA 自营自管 |
| F | **承包商与「更新」**：L3Harris、FTI、为什么周五下午改 | WSJ、CBS、The Register、Simple Flying、HN、Kalshi、VisaVerge | 最接近机制的一类，但主流只给「谁运营」，只有 HN 在问「怎么会」 |
| G | **「美国衰落」/ 中美对照**（中文特有） | 牛弹琴、CSDN、B 站评论区倾向 | 本次检索**没找到严格的中美空管对比**；主要是「美国怎么了」叙事 |

---

## 6. 它们普遍缺了什么

逐条对照任务里提出的四个问题：

1. **「为什么升级本身会引发故障」——几乎没人讲。** CBS / WSJ 给出了「更新→重启→崩溃」的事实链，但没有一家主流媒体解释：为什么对「保证不停机」的系统，**变更（更新、重启）是最危险的时刻**；为什么「重启」本身就是一次大变更（所有设备同时重新建立连接、收敛、同步状态）。只有 HN 评论区在问「为什么重启会导致崩溃」「回滚只能在已经崩溃的机器上跑」，没有人给出系统性答案。

2. **「复杂系统的单点故障与冗余为何失效」——只被点名，没被解释。** Duckworth 说「安全建立在冗余之上」，CSDN 说「冗余不足」，VFTW 转述「备用站点同时失效」，aerocorner 说「无处绕行」，赵巍专栏标题说「冗余骗局」——但**没有人讲共模故障（common-mode failure）**：如果主备两套跑同一个软件、同一套配置、同时收到同一个更新，冗余只能防「各自独立地坏」，防不了「同一个原因让它们一起坏」。多数报道默认「有备份 = 安全」，所以把这次写成「备份没做好」，而不是「这种备份天生防不了这种故障」。

3. **「技术债的经济学：为何几十年换不掉」——只有 View from the Wing 碰到一半。** 主流只说「老」和「缺钱」。没人讲：24 小时运转的系统**没有停机窗口**（飞机在天上换引擎）；年度拨款撑不起多年工程（Leff 提到）；安全认证让每次改动成本极高；FTI 2002 年签约、2026 年才开始由 AT&T 替换、计划 2028 年底完成——**换掉一张网要十几年，而这十几年里旧网还得一直改**。更关键的是：**「老旧设备」（Duffy）和「更新出错」（CBS）被报道成两种互相竞争的解释，几乎没人指出它们是同一个陷阱的两面**——越老越不敢动，越不敢动越老，最后每一次动都是全国级风险。

4. **「全国停飞是安全设计而不是失败」——只有零星专家一句话。** PBS/AP 引 Arroyo「你得把飞机停在地上」、观察者网专家「空中飞机没被要求立即降落」、ABC 的 John Nance「飞行员有预案」、Mullin「出于高度谨慎」——但大多数标题是「瘫痪」「趴窝」「惊险内幕」「不该发生的事」。**没有人把它讲成 fail-safe（失效安全）原则**：系统失去把握时，选择一个代价可见但安全的状态（不再放飞机上天，天上的照常落地）；对比「失效危险」的系统（不知道出错了还继续运行）。也没人讲**代价看得见、风险看不见的不对称**：4 小时、上万航班是摆在眼前的账；如果硬撑着放行而出事，那笔账大到无法比较——所以公众天然把正确的刹车读成失败。

其他缺口：
- **恢复比停下更难**：只有 CNBC（JetBlue 取消周六航班）、VFTW（机组执勤时限）一笔带过，没人讲「停 4 小时、乱 2 天」的连锁机制。
- **「五个 9」的数学**：2025 年达拉斯事故后有报道称 L3Harris 自称该网络 20 多年可用性 99.999%（**此数字仅见于搜索摘要，CBS 正文抓取未见，需核实**）。若属实，99.999% 一年只允许约 5 分钟停机，而这一次 4 小时多——这种「可用性 ≠ 不会同时全坏」的讨论完全没人做。
- **这次是一串事故里的一个**：2025 纽瓦克、2025-09 达拉斯（光纤被挖断 + FAA 指 L3Harris 没确保冗余生效）、2026-08 明尼阿波利斯中心、2026-09 东北部（Verizon 光纤被挖断）——CNBC / AP 提过「模式」，但没人从「同一张网、同一家承包商、冗余反复没接住」这条线讲下去。
- **中文侧**：基本是外媒转述 + 「美国衰落」评论，**没有一条讲机制的解说**；B 站最热的也只有约 1.2 万播放、以搬运为主——中文市场上机制解说是空白。

---

## 7. 我们可能独占的角度候选

1. **「备份为什么会一起坏」——共模故障。** 冗余只防独立故障；当所有副本跑同一套软件、收同一次更新，它们会在同一秒一起倒下。讲清这一点，观众可以带走：自己的备份、公司的主备、甚至「两个人都看过同一份错误资料」的决策，都是同一个道理。（目前只有 HN 评论和一条 12 播放的 B 站视频沾边，没有成型解说。）
2. **「老旧」和「更新」是同一个陷阱，不是两种解释。** 把 Duffy 的「老设备」和 CBS 的「更新出错」并在一起讲：技术债的利息就是「每次修都可能更坏」——越不敢动越老，越老每次动越危险；再讲为什么 24 小时不停的系统换不掉（没有停机窗口、拨款逐年、认证成本、换一张网要十几年）。这正好是「热度过去仍然成立」的长期道理。（VFTW 只讲了治理一半，没人把两说连起来。）
3. **「停下来是设计好的」——失效安全与看不见的账。** 全国停飞不是系统失败，而是系统失去把握时退到安全状态；4 小时的代价是看得见的账，没停可能出的事是看不见的账，所以人们总把刹车当事故。可以作为片子的反转或结尾。（只有零星专家原话，没有人把它当主线。）

> 建议：以 1 或 2 为主线、3 为结尾反转。三者都依赖「更新→重启→崩溃」说法，而该说法目前只有匿名信源（CBS、MS NOW、彭博转述的 FBI 知情人士）、官方未确认——讲稿里必须标为「有争议 / 据报道」，并准备好「如果最终查明是硬件过载」时论点 2、3 仍然成立的说法（论点 1 依赖更强，需看调查结论）。

---

## 8. 报道之间的事实冲突（截至检索时）

| 项目 | 各方说法 | 备注 |
|---|---|---|
| **开始时间** | 15:54 ET（ATCSCC 通告，VFTW、AvWeb、Al Jazeera、维基）；15:53（澎湃）；15:45（Jalopnik）；「约 16:00」（CNBC）；「约 15:00」（牛弹琴）；Simple Flying 时间线写 17:30 发令（明显错误）。问题最早出现：15:36（Duffy，经 NBC / MS NOW） | 先有芝加哥 O'Hare / Midway 局部停飞；扩大到全国的间隔：「11 分钟」（澎湃）vs「约半小时」（IT 之家） |
| **解除时间** | 20:15 ET（Duffy 发布会，CBS、NBC、Al Jazeera；FR24 写 01:15 UTC）；20:19 ATCSCC 取消通告（Flying）；「约 20:30」（Simple Flying、The Register；The Register 更新里又写 02:11 UTC）；微博转载「11 月 14 日凌晨解除」（混用北京时间） | 原定截止：22:00（News9）、23:00（Jalopnik）；Eurocontrol 暂停到 05:00 UTC |
| **持续时长** | 「约 4 小时」（NPR、Make Tech Easier）；「4 个多小时」（CNBC、MS NOW、中时）；「五个多小时」（NBC 正文，与其自列时间矛盾）；「约 5 小时」（The Register）；「9·11 以来最长的全国停飞」（Reuters，经 IBTimes） | 按 15:54–20:15 计约 4 小时 21 分 |
| **「第几次」** | 「9·11 后第二次」（Reuters、AP、CNBC、ABC、NPR、新华社、中央社、多数媒体）；「美国史上第三次 / 近年第三次」（维基、澎湃南博一、TVBS、观察者网）；「2023 年以来首次」（AP、AeroTime）；「911 后首次」（B 站财经抱抱君，错误）；「absolutely unprecedented」（Sumwalt，CBS） | 前三种其实是同一计数的不同说法；但「2023 年那次算不算全国 ground stop」以及 9·11 那次（全部落地，性质不同）是否同类，没有 FAA 官方计数（aerocorner 指出） |
| **受影响中心：「全部」vs「多个」** | 「all Air Route Traffic Control Centers」（Duffy 在 X 上的帖子 https://x.com/SecDuffy/status/2121351591106072679 ）、「全部 22 个」（AP、AvWeb、Make Tech Easier、澎湃等）vs「multiple ARTCCs」（FAA 声明，CNBC、MS NOW 引；B 站柴郡ing 简介）；Duffy 在发布会又说「没有失去全部通信或雷达能力」（NBC、CBS） | 「22 个都受影响」≠「22 个全断」；Al Jazeera 写成「控制塔」，属措辞错误 |
| **故障起点** | 芝加哥 Midway 的网络路由器（CNN 援引航司消息源）；芝加哥中心先出问题，随后波士顿、华盛顿、纽约、明尼阿波利斯（The Air Current，经凤凰网转）；芝加哥 O'Hare（澎湃） | 均为非官方 |
| **原因** | 私有网络更新→重启→崩溃（CBS「多位消息人士」，Simple Flying / The Register / 中文转述）；联邦官员称软件更新（MS NOW）；「可能是软件升级」（NY Post 匿名，经 VFTW）；FBI 认为非攻击、调查方向之一软件更新（彭博知情人士 → 中新、澎湃、TVBS）；老旧路由器 / 交换机数据过载、发出不一致数据（Duffy）；「新技术接入旧系统把它压垮」（Mullin，经 IBTimes、Flying）；「频率问题」（司法部消息源，MS NOW）；老旧破损基础设施（特朗普，Fox，经界面 / 澎湃） | **官方尚无根因结论**。Duffy 还称特朗普任内新装的设备没坏、坏的是旧硬件（MS NOW、中时） |
| **空中飞机数** | 约 3,100（Flightradar24，CBS、ABC、AeroTime；中央社 3,115）；3,500+（Duffy，NBC、TVBS）；4,042 架赴美航班（Flightradar24，经 NBC） | 统计口径与时点不同 |
| **取消 / 延误** | 取消：1,100+（FlightAware 17:40，新华 / 澎湃）、1,300+（雅虎财经早段）、2,000+（ABC 18:20）、约 3,700（澎湃 19:00）、4,000+（CBS）、4,700+（Reuters 引 FR24）、5,000+（NBC）、5,117（中时，FlightAware 全天）、5,300+（MS NOW 21:25）；延误：近 1 万、9,500+、9,814、1 万+；「近 7000 架次延误或取消」（FlightAware 早段，新华社等中文通稿普遍用这个）；「8000 架次延误」（IT 之家）；「逾 2.1 万架次延误」（B 站搬运简介，来源不明） | 多为全天累计且含非停飞原因（Airways 指出 16:40 时取消仅 481 / 26,284） |
| **滞留旅客** | 30–40 万（匿名专家，NBC）；「150 万旅客」是 16 点后原定航班的载客量（Cirium，CNBC / AP），常被误读为受影响人数 | — |
| **要多少钱** | 301 亿美元追加请求（白宫 11-13 致国会信，Simple Flying、AeroTime、AvWeb）；「300 亿」（Duffy 口头，AP 等）；「500 亿」——Flying、Airways 说是 Duffy 要的紧急拨款，IBTimes 说是 Mullin 估的全面改造总价 | 「500 亿」由谁说法冲突 |
| **是否网络攻击** | 「零证据」「这不是又一次 9·11」vs「不排除任何可能」「目前还不知道」（同为 Mullin 不同时点） | 不是矛盾，但被不同媒体各取一半 |

---

## 9. 一手来源与转述链（便于后续核查）

- **一手**：FAA ATCSCC 通告（原文经 AvWeb、VFTW 引用：「Due to extraordinary circumstances and for reasons of safety」「All departing traffic should remain ground stopped until further notice」）；FAA 新闻室声明 https://www.faa.gov/newsroom/faa-statement-nationwide-ground-stop （本次抓取 403，未读到）；Duffy X 帖 https://x.com/SecDuffy/status/2121351591106072679 ；白宫发布会（YouTube MS NOW / FOX NASHVILLE 直播）；Air Space Intelligence 在 X 上的声明（经 NBC、ABC 引）；美航新闻室 https://news.aa.com/news/news-details/2026/Update-on-FAAs-nationwide-ground-stop/ （未读正文）；白宫 11-13 致国会拨款信（经 Simple Flying）；Eurocontrol 通告（经新华社）。
- **匿名信源及其首发媒体**：「更新→重启→崩溃」← CBS（多位消息人士）；「L3Harris 网络」← WSJ；「软件更新导致」← MS NOW（联邦官员）、NY Post（匿名）；「FBI 认为非攻击、查软件更新」← 彭博（知情人士）；「芝加哥 Midway 路由器」← CNN（航司消息源）；「频率问题」← MS NOW（司法部消息源）。中文媒体的「知情人士」「美媒称」基本都来自上面这几条，**很多中文稿没注明原始媒体**。
- **数据源**：FlightAware、Flightradar24、Cirium——各家数字不同主要因为引用的时点和口径不同。
