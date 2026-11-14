# 角度：可用素材候选

- 检索日期：2026-11-14
- 事件：2026-11-13（周五）FAA 全国地面停飞。约 15:54 ET 发布（NBC；Flightradar24 记为 20:54 UTC），20:15 ET 解除（Duffy 在白宫记者会上说，CBS、NBC、CNBC 一致）。官方说法是通信故障影响多个航路管制中心（ARTCC）。时间线细节见同目录 `timeline.md`。
- 分级按 `edu_videos/redian_xiangying/README.md` §4：**优先**（官方、公共领域、CC、公开数据重画，可作画面主体）/ **少量**（有版权的新闻截图或片段，只作评论对象，单段几秒，标来源）/ **不用**。
- 本文件只列链接，**没有下载任何图片或视频**，也没有调用收费服务。真要用的素材，下载时逐条写进 `media_ledger.json`。
- 「核实状态」一栏的写法：
  - **已打开**：本次实际读到页面或接口返回。
  - **检索到**：出现在搜索结果里，但抓取被拒（faa.gov、transportation.gov、fly.faa.gov、bts.gov、gao.gov 产品页对本工具一律返回 403）。
  - 「检索到」的条目，入台账前要人工用浏览器打开核对。
- 本轮的 WebSearch 配额已用完，还没检索的方向列在文末「待补检索」。

## 一、法律依据（判断许可时引用）

| 依据 | 链接 | 要点 | 核实状态 |
|---|---|---|---|
| USA.gov：联邦政府材料与版权 | https://www.usa.gov/government-copyright | ① 联邦政府网站上的文字、图片、logo「可能受版权或其他限制」，用前要逐件确认。② **不得以暗示政府机构背书的方式使用**。③ **未经许可不得使用联邦机构 logo 或商标**。④ 州和地方政府作品不适用 U.S. government work。⑤ **美国政府作品在美国境外可能受当地版权法保护**。页内链到《美国版权法》第 101、105 条 | 已打开 |
| 17 U.S.C. §105 | 经上面 USA.gov 页链接；Commons 的 PD-USGov 标签原文写的是 "Work of the United States Federal Government under the terms of 17 U.S.C. § 105" | 联邦雇员在职务内创作的作品不享有美国版权。例外：①承包商作品（看合同，不一定是公共领域）；②第三方作品被政府网页收录或授权使用；③政府受让持有的版权；④商标、徽章（受另外的法规限制，与版权无关） | USA.gov 页已打开；法条原文没有单独打开 |
| FAA Order 1700.6D（FAA 品牌政策、FAA logo、FAA 签名与 DOT 印章的使用） | https://www.faa.gov/documentLibrary/media/Order/Order_1700.6D.pdf ；状态页 https://www.faa.gov/regulations_policies/orders_notices/index.cfm/go/document.information/documentID/1042519 | 据检索摘要：2024-02-27 发布，**只有 FAA 内部机构可以使用 FAA logo，例外须经 FAA 传播事务助理局长批准**；外部机构须书面申请；该令取代了 1700.6C | 检索到（PDF 403）。需核实：人工打开 PDF，确认外部使用条款的原文和章节号 |
| FAA 网站链接政策 | https://www.faa.gov/web_policies/linking_policy | 据检索摘要：FAA 不能授权使用外链网站上的版权材料 | 检索到 |
| FAA 内部网页标准「版权」页 | https://employees.faa.gov/tools_resources/web/developers/standards/copyright | 据检索摘要：FAA 网站一般不用有版权的文字；**承包商为 FAA 制作的照片、图形归 FAA 所有，因此属公共领域**（这是 FAA 自己的立场） | 检索到；域名本工具解析不了，无法打开 |
| 白宫网站版权政策 | https://www.whitehouse.gov/copyright/ | 「依联邦法律，本网站上政府制作的材料不受版权保护」；政府可以持有受让的版权；**第三方内容除另有注明外按 CC BY 3.0 授权** | 已打开 |
| GAO 版权声明 | https://www.gao.gov/copyright | GAO 的产品和网站信息在美国不受版权法保护，可以不经许可完整复制分发；**但其中可能有受版权保护的图片或其他材料，单独复制可能需要权利人许可** | 已打开 |
| C-SPAN 版权与授权 | https://www.c-span.org/about/copyrightsAndLicensing/ | ① 联邦政府活动（国会委员会听证、行政机构听证、白宫活动、国会和总统委员会）的 C-SPAN 录像，**非商业**用途在网上发布、注明 C-SPAN 即可。② **C-SPAN 不允许任何未经授权的商业使用，包括联邦政府活动的录像，注明来源也不行**；纪录片、节目、播客、「主要靠 C-SPAN 内容获取收入」的用途都要授权。③ 页面提到「不在公共领域的活动」，说明部分镜头（如两院会场官方镜头）另当别论 | 已打开 |
| FlightAware 网站使用条款 | https://www.flightaware.com/about/termsofuse | 授权是「可撤销、非独占、不可转让、个人、有限」的；不得为公共或商业目的复制、公开展示网站材料；**免费的网页产品、API 和数据只限个人使用**；没有明确授权不得复制、出版、分发或商用 | 已打开 |
| FlightAware 媒体转载说明 | https://www.flightaware.com/news/media/reproduction.rvt | 「经认可的新闻机构和媒体人员」可以转载 FlightAware 的内容、图片、地图和数据。署名：电视或纸媒写 "Courtesy of FlightAware (flightaware.com)"；网络媒体写 "Courtesy of FlightAware" 并链接；广播或播客念 "Directly from FlightAware dot com"。**政治议题不得点名 FlightAware**，改称 "flight tracking records"。页面没有提到商业使用、视频或 YouTube | 已打开 |
| Flightradar24 条款 | https://www.flightradar24.com/terms-and-conditions | 2.1：使用权**只限个人、非商业**。5.3.1：任何商业使用，以及**任何公开展示（商业或非商业）**，都只能用 Business 级订阅。8.2：公开或商业发布的材料须清楚注明 Flightradar24。10.3："Flightradar24" 商标受保护，禁止抓取、去除权利声明 | 已打开 |
| Cirium（FlightStats）服务协议 | https://developer.flightstats.com/about/terms_for_paid_accounts ；总条款页 https://www.cirium.com/terms-and-conditions | 据检索摘要：非独占、可终止的 API 和数据许可；不得把实时数据与其他数据商的数据混用；媒体联系 media@cirium.com（出自 2025-11 新闻稿） | 检索到。需核实：没有找到「媒体引用数字」的条款 |

## 二、优先级：官方、公共领域与 CC 素材

### 2.1 官方发布（本事件）

| # | 素材描述 | 链接 | 权利方 | 许可判断（依据） | 建议用途 | 级别 | 核实状态 |
|---|---|---|---|---|---|---|---|
| P1 | 白宫官方 YouTube：「Secretary Mullin & Secretary Duffy provide an update on the FAA National Ground Stop.」11-13 晚的白宫记者会。Duffy 说「20:15 开放空域」、「路由器过载」，Mullin 说「没有恶意行为迹象」 | https://www.youtube.com/watch?v=aH2db_pvy38 （频道 @WhiteHouse） | 白宫（美国联邦政府） | 政府制作的材料不受版权保护（[白宫版权政策](https://www.whitehouse.gov/copyright/)；§105）。**需核实**两点：①白宫简报室的画面是白宫自拍，还是电视台联合摄制组（pool）的信号。可以对比 CBS 嵌入的 36:41 版（片头片尾有没有电视台台标）；有 pool 台标的版本不用。②YouTube 服务条款原则上不允许下载，优先找 whitehouse.gov/videos 的原片，或用屏幕录制以外的官方渠道取得 | 引语原声与画面主体：Duffy 和 Mullin 的关键原话各取几秒，配中文字幕 | 优先 | 已打开（oEmbed 确认标题与频道） |
| P2 | FAA 新闻稿「FAA Statement on Nationwide Ground Stop」 | https://www.faa.gov/newsroom/faa-statement-nationwide-ground-stop | FAA | 联邦机构文字属公共领域（§105）。页面上的 FAA logo 不入画（Order 1700.6D、USA.gov） | 引语卡：用我们自己的排版重排原文，不截网页（避开 logo） | 优先 | 检索到（403）。需核实原文，timeline.md 也记了这一条 |
| P3 | FAA 空管系统指挥中心（ATCSCC）停飞公告 "all airports are ground stopped" | 公告：https://www.fly.faa.gov/ois/oisedit/adv_oisedit_dis?number=111&day=11132026&gdp=-1&gstop=196093 （CBS 文中的链接，转记自 timeline.md）；公告库 https://www.fly.faa.gov/adv/advADB | FAA ATCSCC | 公共领域数据和文字。**公告库只保留 15 天**（据 NAS Status 用户指南和检索摘要），**11-28 前必须人工存下文字版**（只存文字，不算图片视频） | 文字重排成「电报卡」画面；时间点做进时间线 | 优先 | 检索到（403）。需核实：人工打开并存档 |
| P4 | NAS Status（全国空域系统状态）。当晚显示全部机场 Ground Stop | https://nasstatus.faa.gov/ ；用户指南 https://nasstatus-alpha.faa.gov/static/media/NASStatusUserGuide.cccc6d48.pdf | FAA | 公共领域数据。页面是实时状态（JS 应用），**事后看不到当晚的状态**，所以只当数据来源，不截图。界面上的 FAA logo 不入画 | 用 P3 的公告文字和媒体报道的时刻，自己重画一张「全美机场变红」示意地图 | 优先（数据） | 首页已打开（只返回 JS 壳）；用户指南是检索到的 |
| P5 | DOT 官方 YouTube「Modern Skies for America」、「Modern Skies Act」、「Modern Skies Summit」、「U.S. Transportation Secretary Sean P. Duffy Joins Aviation Modernization Summit」（事发前的空管现代化宣传和直播） | https://www.youtube.com/watch?v=H9QEv8CZM0U ；https://www.youtube.com/watch?v=z1Ua59KWbyw ；https://www.youtube.com/watch?v=QP8bogzv808 ；https://www.youtube.com/watch?v=JRHzX3oTUTY （频道 https://www.youtube.com/@USDOTgov ） | 美国交通部 | 联邦政府作品，原则上属公共领域。**需核实**片中有没有第三方素材（配乐、新闻画面、承包商动画），有的话那一段不用 | 背景段「早有改造计划」：取几秒部长讲话或宣传画面 | 优先 | 已打开（oEmbed 确认标题与频道） |
| P6 | FAA 官方 YouTube 频道 | https://www.youtube.com/@FAANews | FAA | 同上。本次只看到最新一页，以飞行安全培训视频为主，**没有看到停飞相关视频** | 备用空镜（塔台、雷达）：先逐条看说明 | 优先（备用） | 已打开 |
| P7 | 白宫 Flickr | https://www.flickr.com/photos/whitehouse/ | 白宫 | 官方照片多标「United States Government Work」，**逐张核对许可栏**。本次没看到当晚简报照片 | 记者会静帧（如果有） | 优先（待查） | 首页已打开 |

> **警示**：https://www.flickr.com/photos/faa/ **不是 FAA 官方账号**。它是个人账号「francisco arellano」（2007 年注册，没有公开照片），本次已打开确认。本次也**没找到 FAA 或 DOT 的官方 Flickr**（https://www.flickr.com/photos/usdotgov/ 返回 404）。用户要求里提到的「FAA 的 Flickr」需核实：从 faa.gov 页脚或社交媒体目录找官方链接，不要凭网址猜。

### 2.2 Wikimedia Commons（空管中心、塔台、人物）

许可信息全部来自 Commons API（extmetadata）的实际返回。

| # | 素材描述 | 文件页 | 权利方（作者） | 许可（依据） | 建议用途 | 级别 |
|---|---|---|---|---|---|---|
| C1 | 华盛顿 ARTCC（ZDC）航路管制员工作照，3008×1960 | https://commons.wikimedia.org/wiki/File:AirTraffic-8.jpg | FAA（来源：FAA 管制员招聘新闻资料包，原链接已失效，Commons 附了 2007 年存档） | 公共领域，PD-USGov（§105） | 「航路中心长什么样」的主画面 | 优先 |
| C2 | 同一张照片的低分辨率版，1429×1147 | https://commons.wikimedia.org/wiki/File:Air_traffic_controllers_at_the_Washington_ARTCC.jpg | FAA | 公共领域，PD-USGov | 用 C1 即可，这张备用 | 优先 |
| C3 | 纽约 ARTCC（ZNY，Ronkonkoma）建筑外景，592×308（分辨率低） | https://commons.wikimedia.org/wiki/File:New_York_Air_Route_Traffic_Control_Center.png | FAA | 公共领域（FAA 照片，来源是 faa.gov 的 ZNY 页） | 小窗或地图标注配图 | 优先 |
| C4 | 洛杉矶 ARTCC（ZLA），863×500 | https://commons.wikimedia.org/wiki/File:Los_Angeles_ARTCC.jpg | FAA（来源：faa.gov ZLA-ARTCC.pdf） | 公共领域 | 「22 个航路中心」图里的示例 | 优先 |
| C5 | ARTCC 管制员雷达屏示意图（FAA《仪表飞行手册》插图），1974×1872 | https://commons.wikimedia.org/wiki/File:Scope_of_an_ARTCC_controller.png | FAA | 公共领域 | 解释「中心靠什么看飞机」 | 优先 |
| C6 | 达拉斯-沃斯堡 TRACON 管制员（NASA FAST 工具现场测试） | https://commons.wikimedia.org/wiki/File:TRACON_DFW.gif | NASA | 公共领域（NASA 是联邦机构） | 「终端区雷达管制」概念图（注意是 TRACON，不是 ARTCC） | 优先 |
| C7 | 交通部长 Sean Duffy 官方肖像，2025-03-05 | https://commons.wikimedia.org/wiki/File:Secretary_of_Transportation_Sean_Duffy_Official_Portrait.jpg | 美国交通部（来源：transportation.gov 部长页） | 公共领域。**不得暗示背书**（USA.gov） | 人物卡 | 优先 |
| C8 | FAA 印章 SVG | https://commons.wikimedia.org/wiki/File:Seal_of_the_United_States_Federal_Aviation_Administration.svg | 美国政府 | 版权上属公共领域，但 Commons 标了 **insignia（徽章）限制**；另受 FAA Order 1700.6D 约束 | **不作装饰或片头元素**，最多在评论语境里一闪，最好不用 | 少量（实际建议不用） |
| C9 | 纽瓦克机场塔台（2002 年建成），2013 年摄 | https://commons.wikimedia.org/wiki/File:NewarkAirportControlTower_01.jpg | Djflem | CC0 | 塔台空镜（2025 年纽瓦克故障可作对照） | 优先 |
| C10 | 纽瓦克机场塔台，640×480 | https://commons.wikimedia.org/wiki/File:Newark_Airport_Control_Tower.jpg | Dsantiago1997（en.wikipedia 用户） | 作者自行释出为公共领域 | 备用 | 优先 |
| C11 | FAA 华盛顿总部大楼和招牌，2006 年摄 | https://commons.wikimedia.org/wiki/File:Federal_Aviation_Administration_headquarters_and_sign.jpg | Runner1928 | CC BY-SA 4.0：**必须署名，改编后的图也要按 BY-SA 发布** | 「FAA 总部」空镜。招牌上有 FAA 字样，属于纪实拍摄，不当 logo 使用 | 优先 |
| C12 | 航班大量取消的出发屏（通用示意），2012 年摄，320×240（分辨率很低） | https://commons.wikimedia.org/wiki/File:Cancelled_flights.jpg | Hotelstvedi | CC BY-SA 3.0 | 小窗示意。**不能说是 11-13 当天的画面** | 优先（低清） |
| C13 | 多伦多皮尔逊机场出发屏，2025 年加航罢工时几乎全部取消 | https://commons.wikimedia.org/wiki/File:2025_AC_Strike_YYZ_cancellation_board_1.jpg | OhanaUnited | CC BY-SA 4.0 | 只作通用示意，并写明「示意，非本次事件」；**不建议使用**，容易误导 | 优先（慎用） |

> Commons 上 ERAM（航路自动化系统）和 ATCSCC（指挥中心）都**没找到合适的照片**（搜 ERAM 只出伊朗的 Eram 公园）。这两类画面建议：①从 FAA 官网 ERAM 或 ATCSCC 介绍页找 FAA 自拍照（需核实）；②自己用网页场景画示意图；③用 Seedance 做模拟画面，并标注「模拟」。

### 2.3 GAO 与国会

| # | 素材描述 | 链接 | 权利方 | 许可判断 | 建议用途 | 级别 | 核实状态 |
|---|---|---|---|---|---|---|---|
| G1 | GAO 证词 GAO-25-108162（引用 2024-09 的报告：FAA 的 138 个空管系统中 51 个「不可持续」，另有约 39% 「可能不可持续」） | https://gao.gov/assets/gao-25-108162.pdf | GAO（美国政府问责局） | 美国境内不受版权保护（[GAO 版权声明](https://www.gao.gov/copyright)）。**报告里的照片要逐张看图注**：标了第三方来源的单独使用需要许可 | 数据卡：「51/138」用我们自己的图表重画。原图表如果是 GAO 自制，也可以直接引用 | 优先 | 检索到 |
| G2 | GAO-24-107001「Air Traffic Control: FAA Actions Are Urgently Needed to Modernize Aging Systems」（2024-09-23），是 G1 引用的原报告 | https://www.gao.gov/products/gao-24-107001 | GAO | 同上 | 同上。引用写原报告编号 | 优先 | 编号来自检索摘要；产品页抓取 403。需核实：人工打开确认页面和 PDF 链接 |
| G3 | GAO-24-105254（2023-11，NextGen 项目管理） | https://www.gao.gov/products/GAO-24-105254 ；PDF https://www.gao.gov/assets/d24105254.pdf ；要点版 https://www.gao.gov/assets/d24105254high.pdf | GAO | 同上 | 背景：现代化项目多年拖期 | 优先 | 检索到 |
| G4 | 国会听证视频（事后可能有空管故障听证） | 本次没有检索到具体听证（配额用完） | 视来源而定 | **C-SPAN 版本不能未经授权商用**（[C-SPAN 政策](https://www.c-span.org/about/copyrightsAndLicensing/)），本系列按商业发行管理，所以 C-SPAN 版本不进优先级。**改用委员会官网或委员会官方 YouTube 自播的视频**：一般由国会自己的录制设施制作，需核实属于政府作品，并看画面有没有 C-SPAN 台标 | 议员质询的原声片段 | 委员会自播版：优先（需核实）；C-SPAN 版：少量（评论性使用，几秒，保留台标并注明） | 未检索 |

## 三、公开数据（只取数字，自己画图）

| # | 数据 | 链接 | 权利方 | 许可判断 | 怎么用、怎么注明 | 级别 | 核实状态 |
|---|---|---|---|---|---|---|---|
| D1 | BTS 航班准点与取消数据（Airline On-Time Performance） | https://www.transtats.bts.gov/ONTIME/ ；数据门户 https://www.transtats.bts.gov/ | 美国交通部运输统计局（BTS） | 联邦政府数据。据检索摘要，data.gov 上 BTS 航班数据记录的许可标注是 usa.gov「government works」 | **页面写明数据「1995 年 1 月至 2026 年 8 月」，11 月的数据要约两个月后才发布**，所以这期只能用 BTS 的历史基线（如美国日均航班量、2023-01 NOTAM 故障当日的取消数作对比）。署名：「数据：美国交通部运输统计局（BTS）」 | 优先 | 已打开（data.gov 许可是检索到的） |
| D2 | FlightAware 取消和延误数字（如 Axios 引用的「全天取消 6,000 多班」） | https://www.flightaware.com/ | FlightAware | **网站数据只限个人使用**（[ToS](https://www.flightaware.com/about/termsofuse)）。媒体转载许可只给「经认可的新闻机构」，本频道算不算需核实；**政治议题还不得点名 FlightAware** | 只引数字，并写明转引自哪家媒体（如「据 Axios 引 FlightAware 数据」），图表自己画。**不截 FlightAware 网页或地图**。想直接用的话写信给 FlightAware 拿书面许可 | 优先（数字转引）/ 截图不用 | 已打开（条款） |
| D3 | Flightradar24 数字（如 NBC 引用的「停飞时有 4,042 架飞往美国的航班在空中」） | 博客 https://www.flightradar24.com/blog/live/nationwide-ground-stop-issued-for-united-states/ | Flightradar24 AB | 条款：只限个人非商业使用；**任何公开展示都要 Business 订阅**；8.2 要求注明 Flightradar24 | 只引数字，写「据 Flightradar24（经 NBC 报道）」。**不截图，不录回放**。想要回放画面的话，买 Business 订阅或拿书面许可，并把许可写进台账 | 优先（数字转引）/ 截图不用 | 条款已打开；博客页检索到（403） |
| D4 | Cirium 数字（CNBC 引用：16:00 ET 后计划起飞约 11,000 班、约 150 万旅客、约 600 班改航） | https://www.cnbc.com/2026/11/13/faa-ground-stop.html （转引处） | Cirium | 条款没有找到媒体引用的规定。需核实：写信到 media@cirium.com 确认能否在商业视频里引数字 | 写「据 CNBC 引 Cirium 数据」，自己画图 | 优先（数字转引） | CNBC 已打开；Cirium 条款是检索到的 |
| D5 | ATCSCC 公告与 NAS Status | 见 P3、P4 | FAA | 公共领域 | 时刻和范围的一手数据 | 优先 | 同 P3、P4 |

> 各家的数字差别很大（取消数：ABC 约 5,000、NBC 5,000 多、Axios 引 FlightAware 6,000 多；受影响航班：CNBC 1 万多、Yahoo 1.45 万多）。图表上每个数字都要注明来源和统计口径，不要混在一起加总。

## 四、少量级：新闻机构的画面（只作评论对象）

用法：单段几秒，必须配我们的评论，不作画面主体，画面上标「来源：××」，原台标保留，不裁掉。**图片的权利方是图片社（Getty、AP、Reuters），不是转载它的网站**，要按图注写。

| # | 来源与素材 | 链接 | 权利方 | 建议用途 | 核实状态 |
|---|---|---|---|---|---|
| N1 | CBS News 文章；嵌入视频「Nationwide ground stop lifted, Duffy calls for congressional funding to upgrade ATC system」（36:41）；旧金山机场旅客照片 | https://www.cbsnews.com/news/faa-issues-nationwide-ground-stop/ | CBS News（视频）；照片 Tayfun Coskun / Anadolu via Getty Images | 评论 CBS 独家信源说的「私有通信网软件更新导致重启」：配文章标题截图 2 到 3 秒 | 已打开 |
| N2 | NBC News 文章；嵌入视频「Secy. Mullin says FAA ground stop was caused by 'telecommunication outage'」（1:51）和「Some airports beginning to run out of space for planes amid nationwide ground stop」（2:48） | https://www.nbcnews.com/news/us-news/faa-orders-nationwide-ground-stop-departing-flights-reasons-safety-rcna609247 | NBC News；照片 Jacek Boczarski / Anadolu via Getty（奥黑尔机场）、John Locher / AP（拉斯维加斯） | 「机场停机位不够」的评论片段，几秒 | 已打开 |
| N3 | ABC News 直播页 | https://abcnews.com/US/live-updates/faa-ground-stop-live-updates-hundreds-flights-canceled/?id=138125140 | ABC News；照片 Brian Snyder / Reuters（波士顿 Logan 机场出发屏）、Elizabeth Frantz / Reuters 与 Alex Brandon / AP Photo（白宫简报室） | Duffy「1980 年代的铜线」原话：**原声优先用 P1 白宫版**，ABC 只作标题截图 | 已打开 |
| N4 | CNBC 文章 | https://www.cnbc.com/2026/11/13/faa-ground-stop.html | CNBC；照片 Nikos Frazier / Omaha World-Herald / Lee / Getty、Jeniece Pettitt / CNBC、Gabriela Riccardi / CNBC | Cirium 数据的出处截图 | 已打开 |
| N5 | AP（WRAL 合署） | https://www.wral.com/news/ap/faa-orders-ground-stop-nationwide-nov-2026/ | The Associated Press、WRAL | 「2001 年 9·11、2023 年 NOTAM 之后又一次全国停飞」的出处 | 已打开 |
| N6 | CNN 直播页 | https://www.cnn.com/2026/11/13/us/live-news/flights-ground-stop-faa | CNN | 标题截图 | 检索到（本工具返回 451） |
| N7 | NPR | https://www.npr.org/2026/11/13/nx-s1-6040403/faa-nationwide-groundstop-airports | NPR | 标题截图 | 检索到 |
| N8 | Axios | https://www.axios.com/2026/11/13/faa-nationwide-ground-stop | Axios | FlightAware 取消数的转引出处 | 检索到（403） |
| N9 | Reuters 照片（经 ABC 使用）：波士顿 Logan 出发屏、白宫简报室 | 见 N3 | Thomson Reuters | 要用 Reuters 照片作主体只能购买授权；不买就只在 N3 的截图里出现 | 本次没有检索到 Reuters 自己的报道页 |

## 五、不用

| 类型 | 例子（本次检索中见到的情况） | 风险 |
|---|---|---|
| 来源不明的社交媒体视频 | X、TikTok、Instagram 上「机场大厅滞留」「塔台屏幕全黑」之类的转发视频，原作者找不到 | 拍摄者保留版权，换谁转发都不改变这一点；画面可能是旧事件，比如 2023-01 的 NOTAM 停飞、2025 年纽瓦克故障（检索结果里大量出现这些旧事件），容易张冠李戴；还可能是 AI 生成。没有原作者就没法进台账 |
| 去水印或二次搬运 | YouTube 上搬运 CNN、CBS 直播的「Full」「LIVE」频道；去掉台标的片段 | 去除权利管理信息本身就违反 DMCA §1202；平台 Content ID 会直接认领或下架；不符合系列规则 |
| 冒用官方名义的账号 | `flickr.com/photos/faa` 这个个人账号（见 2.1 的警示） | 看网址像官方，实际不是，会把非官方素材误标成「FAA 公共领域」 |
| 航迹软件的回放录屏 | 别人发的 Flightradar24 或 FlightAware 回放视频（「全美上空飞机消失」那种） | 违反 FR24 条款 2.1、5.3.1 和 FlightAware 条款，录屏的人自己也没有转授权的资格 |
| 政府页面里的第三方照片 | 政府网页或报告中注明「Getty」「AP」「承包商名」的图 | 虽然在 .gov 网站上，但不属于公共领域（GAO、USA.gov、白宫政策都写明了） |
| 承包商自有材料 | L3Harris（据 CBS，FAA 通信网 FENS 由其运营）官网的系统图、宣传片 | 企业版权和商标，没有授权不能用 |
| 管制通话录音（如 LiveATC） | 「停飞当晚的塔台录音」 | 本次没有核实 LiveATC 的条款，**暂列不用**；要用先查其条款（需核实） |

## 注意事项

1. **署名格式**（画面角标和视频简介各写一次，台账同步）：
   - 联邦政府作品：「图：FAA ／ 美国联邦政府作品（公共领域）」；「视频：白宫官方 YouTube」。公共领域法律上不要求署名，但本系列一律注明来源，方便溯源。
   - CC 素材：`作者 / Wikimedia Commons / 许可名 / 文件页链接`，例如「图：Runner1928 / Wikimedia Commons / CC BY-SA 4.0」，链接放在简介里。CC0 也写作者。
   - BY-SA 素材如果做了裁切、调色、叠字，改编后的那张图要按 BY-SA 发布。需要大改的画面优先选 PD 或 CC0（C1、C3–C7、C9、C10）。
   - 数据：「数据：BTS」；转引的数字写「据 CNBC 引 Cirium」「据 NBC 引 Flightradar24」，不要写成我们直接取得的。
   - 新闻截图：「来源：CBS News」，照片另写图片社，如「照片：Getty Images / Anadolu」。
2. **Flightradar24 和 FlightAware 截图风险**：两家的免费服务都只限个人使用。FR24 明确规定**任何公开展示**都要 Business 订阅，FlightAware 只给「经认可的新闻机构」转载许可，政治议题还不让点名。所以默认**不截图、不录屏、不用它们的地图**，只转引数字、自己画图。确实要用的话，拿到书面许可或买对应订阅，把许可编号写进台账。
3. **政府作品里混入的第三方版权**：
   - 逐张看图注。政府网页、GAO 报告、白宫 Flickr 上标了 AP、Getty、承包商或「Courtesy of」的都不是公共领域。
   - 白宫网站上的第三方内容按 CC BY 3.0 授权，需要署名。
   - 白宫简报室的视频要确认是不是电视台联合摄制组的信号（P1）。
   - DOT 宣传片可能夹带授权配乐或新闻画面（P5）。
4. **Logo、徽章与背书**：FAA logo、FAA 印章、DOT 印章不作片头、角标或装饰。纪实画面里自然出现的招牌、讲台徽章可以接受。画面和标题不得暗示 FAA、DOT 或白宫认可本频道（USA.gov、Order 1700.6D）。
5. **境外发行**：USA.gov 明确提示美国政府作品在美国境外可能受当地版权保护。本系列如果在美国以外的平台发行，需核实目标地区（如中国大陆平台）对美国政府作品的处理；目前风险判断为低，但要记录在案。
6. **人物与肖像**：管制员、旅客照片（C1、C2、C6 等）属纪实或公务场景，作新闻评论用一般没问题，但不要配贬损性解说，也不要把具体个人说成「失职者」。
7. **时效**：ATCSCC 公告库只保留 15 天（P3），**11-28 前**要存下当日公告文字。NAS Status 是实时页面，当时的状态已经看不到了。BTS 的 11 月数据约 2027 年 1 月才发布，这期只能用历史基线。
8. **台账**：本表任何一条进成片前，都要先在 `media_ledger.json` 建条目（原始链接、权利方、许可或「评论性使用」、用了哪段、出现在第几段画面、下载时间、本地路径）。原始文件放 `assets/source/`，不进 git。

## 待补检索（本轮 WebSearch 配额已用完）

- faa.gov 上的 b-roll、照片下载页（FAA 新闻资料包、ERAM 和 ATCSCC 的官方照片）。
- FAA 和 DOT 有没有官方 Flickr。
- 事后的国会听证日程，以及委员会自播视频的版权状态（House Recording Studio 和委员会网播是否属政府作品）。
- CBS 嵌入的 36:41 记者会视频和白宫 YouTube 版是不是同一信号（看台标）。
- Reuters 和 AP 自己的视频报道页（用于少量级引用）。
- LiveATC 条款；Cirium 的媒体引用政策。
