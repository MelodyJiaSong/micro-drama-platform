# 角度：coverage（别人已经讲过什么）

- **检索日期**：2026-11-14（所有播放量、标题均为当日快照，片中一律写「截至 2026-11-14」）
- **检索范围**：英文主流媒体（NYT、WSJ、Bloomberg、Reuters、FT、CNBC、Axios、NPR、Foreign Policy、Fortune、Forbes、ABC 澳洲；The Verge 未检到原文）；中文媒体（第一财经、贝壳财经/新京报、36氪/铅笔道、量子位、钛媒体、光明网/中新社、经济日报（台）、数位时代（台）、香港星岛/TVB/巴士的报）；视频平台（YouTube 经 yt-dlp 搜索元数据、B 站经站内搜索 API 按播放排序）；X 社区注释。
- **检索词（简列）**：Jensen Huang resigns / steps down / affair spy / Nvidia without Jensen / who replaces；黄仁勋 辞职 / 间谍 / 婚外情 / 下台；黃仁勳 辭職 / 外遇；英伟达 黄仁勋 卸任；外交部 黄仁勋；Fortune Jensen Huang tag；Singapore Alice Huang denial 等。
- **方法与限制**：
  - YouTube 用 `yt-dlp --flat-playlist ytsearch12:` 取公开元数据（标题、频道、播放），单视频详情被 YouTube 机器人验证拦截，**上传日期未取到**；B 站用站内搜索接口（order=click），有发布日期。未下载任何视频或图片。
  - NYT、WSJ、Bloomberg、FT 原文有付费墙，**未读到原文**；标题框架来自转载、聚合或他人引述，均已注明转述来源。
  - 会话共享的 WebSearch 额度在检索中途用尽：**抖音、TikTok、小红书、知乎、微博未能直接检索**，下表相应行写「未查到」。系列 README 选题依据记录了 #jensenhuang 上 TikTok 全球增长标签前 10、微博、知乎有多条（follow-up 021），本文件没有独立核实。
- **隐私**：报道点名的第二位当事人不是公众人物。按事实核查 r1，**片中与所有文件都不出现她的姓名与职务**；本文件不含她的姓名。片中只说「一名向他汇报的高管」（与 dossier 风险 R12 一致，汇报关系不等于职务）。（2026-11-14 主会话改正：原句称「保留了姓名」与实际不符，已删。）

---

## 1. 英文主流媒体：角度与标题框架

| 媒体 | 代表标题或框架（原文） | 主要角度 | 出处 / 转述链 |
|---|---|---|---|
| NYT | 10-29 首报（美国情报认为 Alice Huang 向北京传递信息、与黄仁勋关系密切）；11-11 报道第二段关系（向其汇报的高管，信源为「five people who worked at the company」） | 国家安全＋私德；后来转向公司治理（与下属的关系） | 未读原文。转述自 The Nightly 转载 https://thenightly.com.au/world/new-york-times-the-woman-in-the-middle-of-nvidias-chinese-spy-scandal-c-23145636 ；Reuters 简讯转述（WSAU 转载）https://wsau.com/2026/11/11/nvidia-ceo-huang-had-relationship-with-executive-who-reported-to-him-nyt-reports/ |
| WSJ | 10-30「Chinese Executive Close to Nvidia CEO Suspected of Giving China Information」；11-11 董事会「preparing to oust」 | 国家安全，然后转向「董事会逼宫」 | 10-30 标题见新加坡警方声明原文（一手）https://www.police.gov.sg/media-hub/news/2026/10/20261030_clarification_statement_on_wall_street_journals_article ；11-11 转述自 Reuters INSTANT VIEW（Devdiscourse 转载）https://www.devdiscourse.com/article/international/4005439-nvidia-is-preparing-to-oust-ceo-jensen-huang-wsj-reports 。另据 Fortune 转述，WSJ 报道黄仁勋曾在会上称 Kress 为「a deer in the headlights」和「reporting CFO」 |
| Reuters | 「ANALYSIS-Nvidia's clubby board faces a sticky 'honey pot' test」；Megaspeed Factbox；11-12 报道黄仁勋与另一名未具名员工有「intimate relationship」 | **董事会独立性与治理**（董事在任年限、无董事长、章程允许「with or without cause」免职），另有 Megaspeed 背景 | https://www.devdiscourse.com/article/international/4004786-analysis-nvidias-clubby-board-faces-a-sticky-honey-pot-test ；第三段关系转述自 CNBC https://www.cnbc.com/2026/11/12/nvidia-nvda-jensen-huang-second-affair.html |
| Bloomberg | 「Nvidia Lacks Clear Successor for Superstar CEO Who Built Company」（2026-01-27，事件前）；彭博电视多条「Who Could Replace…」；据 Fortune 转述，Bloomberg 报道黄仁勋离任前「had given up」，说过「whatever」「I don't care」，并称自己为「piece of sh--」 | 接班；「最后几天」的内幕细节 | 1 月文章 https://www.bloomberg.com/news/articles/2026-01-27/nvidia-lacks-clear-successor-for-superstar-ceo-who-built-company （未读原文）；内幕转述自 Fortune 晨报 https://fortune.com/2026/11/13/inside-the-dismal-final-days-of-jensen-huang-a-broken-man-heard-saying-things-like-whatever-and-i-dont-care/ |
| FT | 据转述，FT 报道黄仁勋与 Alice Huang 有恋爱关系（CNBC 引 FT）；企业文化「imperial control」「feudal system」「I can't tell you what a cult this place is」；子女在公司任职 | 企业文化与权力集中；家族成员在公司任职 | 转述自 CNBC（同上）及 Fortune 晨报（同上），未读原文 |
| CNBC | 「Nvidia stock closes down over 4% after CEO Jensen Huang announces resignation」；Eamon Javers 独家：Alice Huang 与华为有关联 | **股价**＋华为关联 | https://www.cnbc.com/2026/11/12/nvidia-nvda-jensen-huang-second-affair.html |
| Axios | 「Jensen Huang spy scandal rocks AI race」(11-09)；「Nvidia has no obvious successor to Jensen Huang — and that's a problem」(11-09)；「Should Jensen Huang be fired? Corporate ethicists call for administrative leave」(11-09)；「Nvidia investors rush to keep Jensen despite private disappointment」(11-09)；「Nvidia sinks after report implicates CEO Jensen Huang in 2nd affair」(11-11) | AI 竞赛、**接班**、**治理伦理**、投资者态度、股价，角度最全 | https://axios.com/2026/11/09/jensen-huang-spy-scandal-ai ；https://www.axios.com/2026/11/09/nvidia-jensen-huang-succession-plan ；https://www.axios.com/2026/11/09/jensen-huang-nvidia-ceo-chinese-spy ；https://axios.com/2026/11/09/nvidia-investors-rush-to-keep-jensen-huang-despite-private-disappointment ；https://www.axios.com/2026/11/11/nvidia-jensen-huang-affair-shares |
| NPR | 「Nvidia CEO Jensen Huang steps down amid alleged spy scandal」；导语「reports that he may have had an affair with an alleged Chinese spy quickly sank his career」 | 间谍丑闻导致下台（因果框架） | https://www.npr.org/2026/11/12/nx-s1-6037833/jensen-huang-nvidia-stepped-down |
| Foreign Policy | 页面标题「Jensen Huang's Resignation Over Chinese Spy Scandal Puts Nvidia Under Scrutiny」；og 标题「The Fall of Nvidia's Jensen Huang」；「big implications for the global AI race」 | 地缘政治、AI 竞赛、Trump 与中国 | https://foreignpolicy.com/2026/11/09/jensen-huang-spy-scandal-alice-nvidia-trump-china/ （URL 日期 11-09，标题已写「Resignation」，应是事后更新，见冲突节） |
| Fortune | 「Nvidia built itself around one man. A scandal is testing that bet」(11-09)；「'Stay, with less': Why Nvidia's board may rein in Jensen Huang rather than fire him」(11-11)；「Jensen Huang built Nvidia into a $4 trillion AI giant but owned less than 4% of it…」(11-12)；「Lori Huang, not Jensen, is president of the Huangs' $9 billion foundation…」(11-12)；「Inside the dismal final days of Jensen Huang…」(11-13)；「…his influence on U.S. AI policy is over」(11-10) | **一人公司、所有权与投票权、治理、接班**；也有八卦式内幕 | https://fortune.com/2026/11/09/nvidia-power-built-around-jensen-huang-scandal-testing-formula/ ；https://fortune.com/2026/11/11/nvidia-board-directors-jensen-huang-captive-board/ ；https://fortune.com/2026/11/12/jensen-huang-nvidia-ceo-resignation-ai-chip-founders-voting-power-board-control-mark-zuckerberg-meta-stock-market/ ；https://fortune.com/2026/11/10/nvidia-ceo-jensen-huang-might-hang-on-as-ceo-but-his-influence-on-u-s-ai-policy-is-over/ |
| Forbes | 「Nvidia sinks 11% at open after Jensen Huang resigns, pushing market cap below Microsoft」（据 URL 与简报，页面需 JS，未读正文） | 市值排名 | https://www.forbes.com/sites/fionariley/2026/11/12/nvidia-sinks-11-at-open-after-jensen-huang-resigns-pushing-market-cap-below-microsoft/ |
| ABC（澳洲） | 「Nvidia's Jensen Huang scandal brings China's spy networks into view」 | 借题讲中国情报网络 | https://www.abc.net.au/news/2026-11-13/nvidia-scandal-china-spy-network/107381704 |
| The Verge | 未检到原文。X 社区注释引用了一个 theverge.com/ai-artificial-… 链接（被截断） | 尚不清楚 | — |

**英文媒体小结**：首周（10-29 至 11-10）以「间谍/国家安全」为主框架，Reuters、Axios、Fortune 同时做「董事会能否独立调查」「没有接班人」；11-11 第二段关系见报后，框架转向「与下属的关系属于治理违规」（Bernstein 的 Rasgon 对 CNBC 说：「much tougher for the board to leave him in position」）；11-12 以后转向股价、接班、「最后几天」内幕。治理与关键人风险**并非没人讲**：Fortune、Axios、Reuters 都讲了，但多是一两段专家引语，没有展开成机制。

## 2. 中文媒体：框架差异

| 媒体 | 代表标题 / 框架 | 对「中国间谍」说法的处理 | 出处 |
|---|---|---|---|
| 中新社（光明网转载） | 「黄仁勋婚外情对象为中国情报部门工作？ 外交部回应」 | 标题用问号；全文只是外交部问答：郭嘉昆「我们此前已就此作出回应，所谓中国间谍的论调，纯属捕风捉影，污蔑抹黑」 | https://m.gmw.cn/2026-11/09/content_1304584247.htm |
| 第一财经 | 「黄仁勋出事，英伟达接班人准备好了吗？」(11-09) | 只写「承认自己有婚外情」「董事会启动独立调查」，不展开间谍说法；重点放在**股权结构与婚变对控制权的影响**（持股 3.58%、约 92% 经信托与妻子共同持有） | https://www.yicai.com/news/103433174.html |
| 贝壳财经（新京报） | 「英伟达没有接班人」 | 不谈间谍；明确写「关键人风险」的反向定价，并指出股价**在丑闻前已从 10-06 高点回撤约 21%** | https://m.bjnews.com.cn/detail/1794302833129362.html |
| 36氪（转铅笔道） | 「黄仁勋出轨风波最大危机：或将失去英伟达控制权」 | 正文写「黄仁勋出轨，他自己承认了」；**但页面 meta 描述却写「此类未经核实的传闻大概率属于不实谣言」**，与正文矛盾（疑为平台自动生成或旧描述） | https://eu.36kr.com/zh/p/4062486156727168 |
| 量子位 / 钛媒体 | 「黄仁勋承认出轨发全员信道歉！英伟达启动紧急调查」/「英伟达启动独立调查：黄仁勋继续担任CEO」 | 科技快讯，不定性 | https://www.qbitai.com/2026/11/508498.html ；https://www.tmtpost.com/8198079.html |
| 央视新闻、环球网（B 站号） | 「英伟达公司宣布：黄仁勋辞职」/「英伟达宣布CEO黄仁勋辞职」 | 只发公司公告事实，不提间谍 | B 站 BV1FuWZ6dEjb、BV1TRWo6KEnk |
| 经济日报（台，编译路透） | 「路透：黃仁勳暈船 台灣人表示同情、不敢置信」 | 写家乡视角：蜜饯行老板「我覺得這一定是騙人的、是假新聞」，理发师「我每天替他祈禱」 | https://money.udn.com/money/story/5599/9869800 |
| 数位时代（台） | 「黃仁勳會因婚外情坐牢嗎？半導體老將拆解3種情境，看輝達代價與台灣供應鏈衝擊」 | 分「私德 / 出口管制 / 国安」三层情境，落到**台湾供应链** | https://www.bnext.com.tw/article/93016/jensen-huang-affair-national-security-nvidia-taiwan-supply-chain |
| 台湾电视（东森、中天、TVBS、三立） | 「小三小四小五連環爆」「閃辭罵『我是爛人』」「華裔就是原罪」（中天，介文汲） | 东森、三立偏八卦；中天偏「美国政界逼宫华裔」 | 见第 3 节 YouTube 表 |
| 香港（星岛、TVB、巴士的报） | 「黃仁勳出軌3.0｜路透社揭還涉第三段婚外情」；TVB「新加坡指調查黃樂不涉間諜活動」；巴士的报「芯片行業或將進入『戰國時代』」 | TVB 的说法**比新加坡原声明走得更远**（见第 4 节） | YouTube：OSiRYxBSwDM、6W8U1G8BuUA、vrmMS4X165Q |
| 财新、每经、IT 之家、新浪/腾讯科技、虎嗅、天下、联合报 | **未查到**本事件的专门报道（检索只返回旧文或无关文，额度用尽后无法补查）。腾讯新闻有 B 站视频号（见下） | — | — |

**中文媒体小结**：
- 大陆正规财经媒体（第一财经、贝壳财经、36氪）几乎**回避间谍说法**，集中讲股权、控制权、接班，反而比不少英文报道更早把「关键人风险」写成主题；官方口径（外交部「捕风捉影」）由中新社、环球网等转发。
- 台湾媒体分两层：报纸、商业杂志讲「家乡同情」与「供应链冲击」；电视台以「小三小四小五」八卦为主。本次**没有检到**以「台湾之光」为题的辞职报道（「台灣之光」一词在检索中只出现在事件前韩媒称赞黄仁勋、苏姿丰的文章里），所以「台湾之光视角」只能说**以家乡情感的形式存在**。
- 海外中文自媒体（文昭、新唐人、万维、唐靖远、路德社）把事件讲成「中共渗透」，并附带大量未核实细节（见第 4 节）；另一端的大陆自媒体讲成「美国打压华人 / 美国自断一臂」。两端都把**未证实的情报指控**当成叙事前提。

## 3. 视频平台

### 3.1 YouTube（yt-dlp 搜索快照，2026-11-14；上传日期未取到）

| 频道 | 标题（原文） | 播放 | 角度 |
|---|---|---|---|
| CNN | Nvidia CEO Jensen Huang resigns, Nvidia stock plunges | 1,760,806 | 突发＋股价 |
| CNN | Nvidia board preparing to oust Huang after report of second affair | 1,454,832 | 董事会逼宫 |
| 二爷故事 | 黄仁勋的出轨：中美AI暗战 | 1,001,628 | 中美 AI 对抗 |
| The Deshbhakt（印度） | Not Just 'Affairs' \| Jensen Huang's Exit From Nvidia Rattles The Tech World & Trump's White House | 991,349 | 政治与白宫 |
| 志祺七七（台） | 黃仁勳外遇對象是中國間諜？一段婚外情，為何會牽連美中AI大戰？ | 897,429 | 科普解释，美中 AI |
| BBC News | Nvidia's CEO Jensen Huang has resigned. Now what? | 723,647 | 接下来怎样 |
| 东森新闻 CH51 | 黃仁勳閃辭罵「我是爛人、隨便啦、我不在乎」徹底放棄抵抗！… | 680,928 | 八卦内幕 |
| 文昭谈古论今 | 黃仁勳辭職，危機才剛開始！董事會為何徹底切割？… | 638,538 | 政治解读（海外中文） |
| Valuetainment | Jensen Huang RESIGNS - Carlos Ghosn Reacts to NVIDIA Stock Plunge | 456,002 | 被赶下台的前 CEO 现身说法 |
| Fox Business | BREAKING: Jensen Huang RESIGNS as CEO of Nvidia | 368,385 | 突发 |
| 攝徒日記 Fun TV | 黃仁勳認了婚外情！甜蜜合照曝光，起底中國美女間諜身分… | 359,972 | 八卦＋「间谍」定性 |
| 57东森财经 | Scandal After Scandal: Nvidia Exec Resigns! … | 345,232 | 八卦 |
| BBC News | Reports of second Jensen Huang affair deepens Nvidia scandal | 344,018 | 突发 |
| CBS News | Nvidia preparing to fire CEO Jensen Huang after affair with suspected Chinese spy, sources say | 325,878 | 突发 |
| 老周横眉 | 黄仁勋出轨女间谍，牵出300亿芯片迷局！揭秘中国如何绕开美国封锁 | 324,296 | 出口管制、走私 |
| Alan Chen | 马斯克回了5个词，老黄下一站会是Terafab吗？ | 309,789 | 下一步去向（推测） |
| CNBC Television | The Investment Committee reacts to Nvidia's stock after Jensen Huang's resignation | 309,020 | 投资 |
| Pivot（Kara Swisher & Scott Galloway） | Nvidia CEO Jensen Huang Resigns: So What Happens Now? | 293,553 | 评论 |
| 拽著歷史說故事 | 离开了黄仁勋，英伟达将何去何从？董事会的决定隐含哪些信息… | 245,182 | 治理＋股民怎么办 |
| 唐靖远 | 黃仁勛被逼辭職，出軌第三案曝光！黃樂現身北京，與軍方關聯流出… | 215,889 | 中共渗透（含未核实说法） |
| 新闻大白话 | Jensen Huang abruptly resigns…; US intelligence chief changes tune, is Huang not a s… | 209,871 | 「间谍」说法反转（标题被截断，未核实） |
| BBC News 中文 | 被揭疑涉第二宗婚外情 黃仁勳辭任輝達執行長 | 199,711 | 突发 |
| Parkev Tatevosian, CFA | How Far Could Nvidia Stock Fall if Jensen Huang Resigns? | 173,541 | 股价估算 |
| Vaush | BREAKING: NVIDIA CEO JENSEN HUANG RESIGNS | 160,490 | 政治评论 |
| 磊哥聊政经 | 重磅！英伟达宣布黄仁勋辞职！净身出户！… | 154,522 | 夸张标题（「净身出户」无依据） |
| Bloomberg Television | Jensen Huang Resigns as Nvidia CEO | 127,543 | 突发 |
| Nate B Jones | Why Jensen Huang's Resignation Could Change Your AI Bill | 28,373 | **对普通用户的影响**（少见） |
| TechLinked | A Giant Has Fallen | 15,729 | 科技圈 |
| Brut Explains | Would NVIDIA Fail Without Jensen Huang? | 2,931 | 一人公司（播放很低） |

注：同一视频在不同搜索里标题略有不同（如 BBC 8580Uu0lxFM 先后显示「…resigns after second affair allegations」和「…Now what?」），应是频道改过标题。

### 3.2 B 站（站内搜索按播放排序，2026-11-14 快照）

| UP 主 | 标题 | 播放 | 发布 | 角度 |
|---|---|---|---|---|
| 央视新闻 | 英伟达公司宣布：黄仁勋辞职 | 2,775,959 | 11-12 | 官方事实 |
| 蒸気火鸡 | NVIDIA：黄仁勋辞职 | 1,051,868 | 11-13 | 玩家 / 梗 |
| 亮仔的玫瑰w | 天啊，美国彻底懵了！黄仁勋从英伟达辞职美国芯片股大盘直接血崩！…市值两日蒸发超4300亿美元 | 1,023,974 | 11-12 | 「美国懵了」情绪 |
| 擦擦玩游戏 | 黄仁勋辞职百万撤离 60系显卡彻底没戏了？ | 882,183 | 11-13 | **显卡玩家视角** |
| RT今日俄罗斯 | 彭博社：黄仁勋婚外情对象黄乐已返回中国 | 804,130 | 11-12 | 转述彭博（未核实） |
| 环球交叉点 | 中国外交部回应黄仁勋婚外情事件 | 682,465 | 11-09 | 官方回应 |
| 蔡雅奇刑法 | 黄仁勋因这个事儿辞职…让我不禁想起了刘强东。我以一个刑辩律师的角度说几句 | 668,978 | 11-13 | 法律、类比 |
| RT今日俄罗斯 | 美媒称中国女间谍与黄仁勋关系密切 英伟达回应！ | 611,345 | 10-30 | 首报转述 |
| 新西兰三妹Summer | 黄仁勋承认婚外情 英伟达董事会调查涉外国情报行动指控！沈逸 三妹 | 550,111 | 11-09 | 地缘政治 |
| 腾讯新闻 | 被问及黄仁勋是否该辞职，特朗普长叹一口气：他是个非常出色的人，但建议库克执掌英伟达 | 532,910 | 11-13 | Trump 表态（原话待核） |
| 最新情报局 | 11.13泪目！英伟达超97%员工挽留黄仁勋！黄仁勋称自己算个什么东西！… | 531,184 | 11-13 | 煽情（「97%」未核实） |
| 悠然啥也不懂 | 如何看待英伟达 CEO 黄仁勋在致员工内部信中承认婚外情？ | 514,841 | 11-09 | 知乎体问答 |
| 大象新闻 | 黄仁勋辞职后，马斯克再为他发声：创始人可不是随随便便就能换掉的 | 484,642 | 11-13 | Musk 表态（原话待核） |
| 红星视频 | 被指控涉嫌欺诈 英伟达、黄仁勋遭股东集体诉讼！…「黄仁勋一旦离任 英伟达将面临巨大接班难题」 | 445,450 | 11-10 | 诉讼＋接班 |
| 棉花糖向前冲 | 老黄出轨大家为什么都一幅没所谓的态度 | 431,695 | 11-10 | 舆论心态 |
| 华商报 | 黄仁勋辞职后英伟达总部外出现鲜花镜头拍到有员工哭泣 | 384,731 | 11-13 | 现场情绪 |
| 蛊徒波瑠卡 | 黄仁勋辞职后某乎回旋镖笑话精选 | 322,468 | 11-13 | 知乎旧回答被翻出（间接说明知乎讨论热） |
| 杜雨说AI | 黄仁勋承认婚外情，英伟达市值蒸发六千亿！——比大佬出轨更严重的是利益冲突 | 214,983 | 11-09 | **利益冲突**（接近治理机制） |
| 老张在修仙 | 黄仁勋下台，最大的输家是中国AI | 63,235 | 11-13 | 对中国 AI 的影响 |
| 红衣大叔周鸿祎 | 黄仁勋突然下台！将对中国AI有何影响？ | 29,770 | 11-13 | 对中国 AI 的影响 |
| YouTube精选智慧 | 「…黄仁勋被整下台，是因为他支持中国开源AI，挡了美国闭源大厂的财路」 | 18,620 | 11-13 | 阴谋论 |

### 3.3 抖音、TikTok、小红书、知乎、微博

- **未查到**代表性视频与数据：WebSearch 额度用尽，这些平台需登录才能检索，没有可核对的公开元数据。
- 间接线索：系列 README 记录了 #jensenhuang 上 TikTok 全球增长标签前 10、微博和知乎有多条（follow-up 021，未独立核实）；B 站「某乎回旋镖笑话精选」（32 万播放）说明知乎上有大量讨论和旧回答被翻出。
- 英文梗图圈：ThePrint「From Coldplay kiss cam to Tim Cook joke—the Jensen Huang meme factory」https://theprint.in/feature/coldplay-kiss-cam-tim-cook-joke-jensen-huang-meme/3094174/ ；Malay Mail「AI bites back…sparks memes, from Coldplay kiss cam to Usher's 'Confessions'」https://www.malaymail.com/news/life/2026/11/10/ai-bites-back-nvidia-boss-jensen-huangs-affair-scandal-sparks-memes-from-coldplay-kiss-cam-to-ushers-confessions/242706 。

## 4. 谣言、伪造与以讹传讹

| 说法 | 性质 | 依据 |
|---|---|---|
| X 帐号 @wholemars 发的「第二封道歉信」（"Hey guys, me again. I owe my family and all of you another apology…"，2026-11-12 05:46 UTC，约 513 赞） | **伪造讽刺**。X 社区注释原文：「This claimed email from Jensen Huang is fabricated satire and was not sent. NVIDIA's records and reporting confirm only the Nov 8 memo with different text」 | X 官方 syndication 接口读取的帖子与注释 https://x.com/wholemars/status/2120755007423484389 （注释 ID 2120764690586386908）；英伟达官网只有 11-08 一封信 https://nvidianews.nvidia.com/news/a-message-to-our-company |
| 「黄仁勋承认与中国女间谍有婚外情」（大量中英文标题，如 CNBC 写「On Sunday, Huang admitted to having an affair. The CEO was romantically involved with Alice Huang… according to The Financial Times」） | **混淆**：信中只承认「I was unfaithful to my wife」，**未点名任何人**；对象是谁出自 NYT/FT 的匿名信源；「间谍」是美国情报方面的判断，未经司法认定，中方否认 | 致员工信一手；CNBC 原文 |
| 新加坡「调查后认定黄乐不涉间谍活动」（TVB 标题「新加坡指調查黃樂不涉間諜活動」） | **转述失真**：新加坡警方声明只说政府和官员没说过 WSJ 所称的话，并且「there were no such investigations conducted in respect of Alice Huang」；对 Megaspeed 的调查「ongoing」。即**没有调查她**，而不是调查后为她洗清 | 新加坡警方声明原文 https://www.police.gov.sg/media-hub/news/2026/10/20261030_clarification_statement_on_wall_street_journals_article |
| 「我是爛人 / 我算个什么东西」（东森、中天、B 站多条标题当作黄仁勋原话） | **报道称，层层转述**：Fortune 晨报转述 Bloomberg，说他被听到称自己为「piece of sh--」，以及「whatever」「I don't care」；Bloomberg 信源未知（未读原文），当事人未回应。中文标题去掉了「据彭博」，改写成直接引语 | Fortune 晨报（同上） |
| 「第五段婚外情 / 小五」（三立英文字幕「Fifth Affair」） | **翻译误差**：台湾俚语里「小三」指第一位婚外对象，「小五」就是第三段；英文字幕直译成 fifth。目前的报道是三段（NYT 两段＋Reuters 一段未具名员工），均未获当事人证实 | CNBC 转述 Reuters「intimate relationship」with an unnamed second employee |
| 「英伟达超 97% 员工挽留黄仁勋」「员工联署要求复职」 | **未核实**。能查到的是匿名职场社区 Blind 的调查（检索摘要称 88% 反对他离任、82% 认为董事会应留任他；原页面被人机验证拦截，未读原文），属自选样本问卷，不是联署，也不是 97% | https://www.teamblind.com/news/jensen-huang-should-remain-nvidia-ceo （未读原文） |
| 「黄乐潜逃北京 / 与军方关联 / 康伟牵线 / 献妻获释」（唐靖远、万维、新唐人等标题） | **未核实**。「黄乐已返回中国」有 RT 中文号标注转述彭博，未见彭博原文；其余未见主流媒体来源 | YouTube AvasL6mrvFY、380IJYiUAQc、HJzE-4sv3e8；B 站 BV11mWD61EpK |
| 「净身出户」「33 年打拼一场空」（磊哥聊政经） | **无依据**。8-K 只写辞去 CEO 与董事职务，未涉及他的股权；所持股份并不因辞职而失去 | 8-K 一手 https://www.sec.gov/Archives/edgar/data/1045810/000104581026000082/nvda-20261111.htm |
| 「被指控涉嫌欺诈，遭股东集体诉讼」（红星视频；贝壳财经写 Rosen Law Firm「已…提起投资者集体诉讼」） | **有争议 / 尚不清楚**：未见法院案号或起诉书；这类律所常先发「征集原告 / 调查」公告，是否已正式立案需查 PACER | 贝壳财经原文 |
| 「黄仁勋被整下台是因为支持中国开源 AI」 | **阴谋论，无依据**，属动机推断 | B 站 BV1nVWz6gEXy |
| 36氪页面 meta 描述称「黄仁勋出轨且本人承认」是「大概率属于不实谣言」 | **反向错误**：黄仁勋本人在官网信中承认；36氪正文本身也写「他自己承认了」 | https://eu.36kr.com/zh/p/4062486156727168 |

## 5. 总结：主流角度、普遍缺口、给本系列的建议

### 5.1 已被讲烂的角度
1. **间谍 / 美人计 / 国家安全**：首周主框架，中英文都有，海外中文自媒体讲得最重。
2. **股价与市值**：「蒸发 5000 亿」「跌破 4 万亿」「市值被微软超过」。
3. **接班人是谁**：Kress、Lisa Su、Tim Cook（Trump 提）、Eric Schmidt（Sonnenfeld 提）等名单式猜测。
4. **美中 AI 竞赛 / 出口管制 / 对中国 AI 的影响**：二爷故事、志祺七七、周鸿祎、Foreign Policy。
5. **八卦内幕**：小三小四小五、「我是烂人」、员工哭泣、总部鲜花。
6. **董事会与治理**：Reuters「clubby board」、Fortune「stay, with less」、Axios 伦理学者，有人讲但篇幅短。
7. **所有权结构**：Fortune、第一财经、贝壳财经都讲了「只持股 3.58%、没有 AB 股」。

### 5.2 普遍缺了什么（我们的判断）
- **「为什么第一段没让他下台，第二段让他下台了」这条规则没人讲透**。Axios 的伦理学者说第一段关系「probably isn't a fireable offense, since it wasn't with an employee」；Rasgon 说与下属的关系让董事会「much tougher」留他。这就是私德变成公司治理违规的分界线（与下属的关系＝利益冲突＋权力不对等＋披露义务），2018 年 Intel Krzanich、2019 年 McDonald's Easterbrook 都是这样被定的（检索摘要提及，未核对一手）。视频里几乎只讲「间谍」与「八卦」，没把这条线画出来。
- **跌幅里有多少是「黄仁勋折价」，没人拆**。贝壳财经指出股价在丑闻前已从 10-06 高点回撤约 21%，11-09 费城半导体指数上涨而英伟达下跌；绝大多数视频把「蒸发几千亿」全算在丑闻头上。可以用「相对半导体指数的超额跌幅」做一张自己的图（数据需另一角度核对）。
- **历史基率缺位**：创始人或长期 CEO 被迫离任后公司怎样（Apple 1985、Uber 2017、Intel 2018、McDonald's 2019……）只有 Axios 一句「think Travis Kalanick at Uber」和 Challenger 的「17 other CEOs… ousted this year」。没人系统讲过「关键人走了，公司通常会怎样」。
- **信息链条本身**：一条匿名信源的情报判断，怎样在几天内变成中文标题里的「女间谍」事实；没点名的道歉信怎样被写成「承认与间谍有染」；「piece of sh--」怎样经 Bloomberg → Fortune → 台媒变成「我是烂人」；「小五」怎样被译成「第五段」。这是可长期复用的媒体素养内容，目前没人做。
- **普通观众的利害**：几乎只有 Nate B Jones（AI 账单）和擦擦玩游戏（显卡）从用户角度讲。持有指数基金的人间接持有英伟达，这个视角没人讲（具体权重需另查）。

### 5.3 给本系列的独有角度建议
- **主线（建议）**：「一家公司把多少价值押在一个人身上，这笔押注怎样被定价、又怎样被结算。」热点开场用辞职与股价；正片讲三件事：① 关键人溢价怎样估算、怎样与大盘回撤分开；② 治理规则怎样把私事变成公事（与下属的关系这条线）；③ 历史基率：明星 CEO 离任后公司的常见走向。结尾落在观众可用的认知：评估任何「靠一个人撑着」的组织（公司、团队、基金）时该问的几个问题。
- **侧栏（可选）**：一段「一条新闻怎样跨语言变形」，用本文件第 4 节的 3 到 4 个例子，只陈述可核对的转述链，不做动机推断。
- **反方最强论证**（留给档案）：英伟达的护城河（CUDA、生态、供应链）是制度化的，不系于一人；Axios 也说「There are many examples of companies surviving and even thriving after a well-known headline-grabbing founder departs」。片子需要正面回应。
- **要避免**：间谍定性（未证实）、点名第二位当事人、复述未核实细节、「美国打压华人」或「中共渗透」任何一边的动机叙事。

---

## 台账候选

| claim | source | quote | status |
|---|---|---|---|
| X 上流传的黄仁勋「第二封道歉邮件」是伪造的讽刺帖，已被社区注释标注 | https://x.com/wholemars/status/2120755007423484389 | "This claimed email from Jensen Huang is fabricated satire and was not sent." | 已证实（社区注释＋官网只有 11-08 一封信） |
| 新加坡政府称没有对 Alice Huang 进行过 WSJ 所称的调查；对 Megaspeed 的调查仍在进行 | https://www.police.gov.sg/media-hub/news/2026/10/20261030_clarification_statement_on_wall_street_journals_article | "there were no such investigations conducted in respect of Alice Huang"；"Investigations into Megaspeed are ongoing." | 已证实（政府一手声明） |
| WSJ 10-30 报道标题 | 同上（新加坡警方声明引用） | "Chinese Executive Close to Nvidia CEO Suspected of Giving China Information" | 已证实（标题存在；内容属报道称） |
| 中国外交部发言人郭嘉昆 11-09 称「中国间谍」说法纯属捕风捉影 | https://m.gmw.cn/2026-11/09/content_1304584247.htm | 「所谓中国间谍的论调，纯属捕风捉影，污蔑抹黑」 | 已证实（当事方表态，中新社转载） |
| 11-12 英伟达收跌 4.34%，盘中最多跌 14% | https://www.cnbc.com/2026/11/12/nvidia-nvda-jensen-huang-second-affair.html | "Nvidia shares declined 4.34% Thursday"；"steeper losses earlier in the day of as much as 14%" | 已证实（CNBC 报道；盘中跌幅各家不一，见冲突） |
| Bernstein 把目标价从 400 美元减半到 200 美元 | 同上 | "Bernstein on Thursday slashed its price target on Nvidia's stock by half from $400 to $200." | 已证实（CNBC 报道） |
| Rasgon：与下属的关系让董事会更难留他 | 同上 | "much tougher for the board to leave him in position" | 已证实（引语，CNBC） |
| 伦理学者认为第一段关系本身大概不构成解雇理由，因为对象不是员工 | https://www.axios.com/2026/11/09/jensen-huang-nvidia-ceo-chinese-spy | "The affair itself probably isn't a fireable offense, since it wasn't with an employee, business ethics experts say." | 有争议（专家观点） |
| Challenger 统计：2026 年已有 17 位 CEO 因职业不当行为指控被撤 | 同上 | "he would join 17 other CEOs who have been ousted this year due to allegations of professional misconduct, according to Challenger, Gray & Christmas" | 已证实（Axios 转述 Challenger，未见原始统计） |
| 英伟达章程允许董事会多数「with or without cause」免除 CEO | https://www.devdiscourse.com/article/international/4004786-analysis-nvidias-clubby-board-faces-a-sticky-honey-pot-test | "its bylaws allow his removal 'with or without cause' by the vote of a majority of directors" | 已证实（Reuters 分析转载；建议另一角度核对章程原文） |
| 黄仁勋 1 月播客：CEO 不称职就会被换；「There will never be one like me」 | https://fortune.com/2026/11/12/jensen-huang-nvidia-ceo-resignation-ai-chip-founders-voting-power-board-control-mark-zuckerberg-meta-stock-market/ | "If the CEO doesn't do his job according to 12, 13, 15 board members… that CEO is let go."；"There will never be one like me, and the reason for that is because I was raised by the company" | 已证实（Fortune 转引 Jodi Shelton 播客，未听原音频） |
| 黄仁勋离任前被听到说「whatever」「I don't care」，自称「piece of sh--」 | https://fortune.com/2026/11/13/inside-the-dismal-final-days-of-jensen-huang-a-broken-man-heard-saying-things-like-whatever-and-i-dont-care/ | "Huang had given up, Bloomberg says, and was heard saying things like 'whatever,' 'I don't care,' and referring to himself as a 'piece of sh--.'" | 指控未证实（Fortune 转述 Bloomberg，信源未知，当事人未回应；不建议入片） |
| 丑闻前英伟达已从 10-06 高点回撤约 21% | https://m.bjnews.com.cn/detail/1794302833129362.html | 「自10月6日触及5.82万亿美元的历史峰值后便持续回撤，近二十个交易日累计下跌约21%」 | 有争议（媒体计算，需用行情数据复核） |
| 「关键人风险」的反向定价框架 | 同上 | 「本质上是市场对『关键人风险』的一次反向定价」 | 我们的判断（贝壳财经观点，可作为对照） |
| 英伟达的接班人问题在事件前已被提出 | https://www.bloomberg.com/news/articles/2026-01-27/nvidia-lacks-clear-successor-for-superstar-ceo-who-built-company | 标题 "Nvidia Lacks Clear Successor for Superstar CEO Who Built Company" | 已证实（标题；正文未读） |
| Sonnenfeld：管理层没有任何人被确定为接班人 | https://www.axios.com/2026/11/09/nvidia-jensen-huang-succession-plan | "It's ridiculous that they have nobody in management identified" | 有争议（专家观点） |
| 本事件被广泛报道的视频中，播放最高的是 CNN（约 176 万）和 B 站央视新闻（约 278 万） | YouTube gCwpCPZeIGQ；B 站 BV1FuWZ6dEjb | （播放量快照，2026-11-14） | 已证实（快照数字，会变） |
| 台湾民众（黄仁勋常去的店家）的反应：不相信、同情 | https://money.udn.com/money/story/5599/9869800 | 「我覺得這一定是騙人的、是假新聞」 | 已证实（经济日报编译路透） |

## 尚不清楚 / 冲突

- **11-12 盘中跌幅**：CNBC「as much as 14%」；Forbes 标题「sinks 11% at open」；中天「盤前暴跌逾-11%」；頭條開講「開盤暴跌13%」；简报记录各家 11%–16%。收盘 -4.34% 一致。
- **11-09 跌幅**：Fortune「fell as much as 8.8% on Monday and closed down about 4.3%」（约 1900 亿美元）；贝壳财经收跌 4.27%，报 178.67 美元；36氪称法兰克福盘先跌超 6%（约 2700 亿美元，按盘前估算）。
- **「市值蒸发」口径**：B 站标题「两日蒸发超 4300 亿美元」「单日蒸发 1.21 万亿（人民币）」「5000 亿美元灰飞烟灭」；Axios 称自首报以来「lost nearly $1 trillion」。起点、币种、单日与累计混用，片中只能用我们自己按同一口径重算的数。
- **辞职日期**：8-K 写董事会 11-11 接受辞呈、即时生效；Fortune 写「On Thursday, Huang resigned」（11-12 是公告日）。应以 8-K 为准：11-11 接受，11-12 公布。
- **Foreign Policy URL 日期 11-09，但标题写 Resignation**：疑为事后改标题，原 11-09 版的标题尚不清楚。
- **NYT 第二段关系的信源人数**：Reuters 简讯转述「citing five people who worked at the company」；当事人与英伟达未证实。
- **第三段关系**：只有 Reuters（经 CNBC 转述）一家，对象未具名；未见当事人或公司回应。
- **「黄乐已返回中国」**：只见 RT 中文号转述彭博，未见彭博原文。
- **Rosen Law Firm 集体诉讼是否已正式立案**：尚不清楚。
- **Trump「建议库克执掌英伟达」、Musk「创始人可不是随随便便就能换掉的」**：只见 B 站新闻号标题，原话与出处未核实（检索额度用尽）。
- **Blind 调查数字**：88% / 82%（检索摘要）与 B 站「97%」冲突；原页面未读到。
- **The Verge、财新、每经、IT 之家、虎嗅、天下、联合报的报道框架**，以及**抖音、TikTok、小红书、知乎、微博的代表内容与数据**：未查到，需要额度恢复后补。
- YouTube 视频的**上传日期**未取到（单视频接口被机器人验证拦截）；表中播放量仅为搜索结果快照。
