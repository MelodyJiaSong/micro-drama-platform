# 角度：media（可用素材候选）

- **检索日期**：2026-11-14（片中说法一律「截至 2026-11-14」）
- **检索范围**：英伟达新闻室（Exec Bios、Media Assets、Online Press Kits、Logo 与品牌规范、网站 Terms of Service）；SEC EDGAR（8-K、Exhibit 99.1、10-K、XBRL 数据接口）；sec.gov 网站声明；众议院对华特设委员会与外交委员会新闻稿及版权页；whitehouse.gov 版权页、USAGov「政府作品版权」页、白宫 Flickr；Wikimedia Commons API（只读元数据，**未下载任何图片**）；中国外交部 2026-11-09 至 11-13 例行记者会实录；《著作权法》（中国政府网）；《互联网信息服务深度合成管理规定》《人工智能生成合成内容标识办法》；Dreamina 美国版 Terms of Service 与 Community Guidelines；YouTube、NYT、CNBC、Nasdaq、Yahoo 条款；17 U.S.C. §105、§107；本仓库 `paid_services.md` 与 `.audit/adhoc_agents/2026-10-09/commercial-use-terms/README.md`。
- **检索词（简列）**：nvidianews bios / multimedia / online-press-kit；NVIDIA terms of service、logo brand usage；sec.gov privacy "Website Dissemination"；Commons search "Jensen Huang"、"Colette Kress"；Jensen Huang House committee November 18 briefing；外交部 黄仁勋 记者会 郭嘉昆 毛宁；Dreamina terms likeness / publicity / impersonate。
- **方法说明**：网页文本用 curl 下到 scratchpad 的 `dl_media\`，去标签后读原文；Commons 只调 API 读许可、作者、限制字段；YouTube 只用 oEmbed 读标题。没有调用任何收费服务。本会话 WebSearch 额度中途用完，后面几项（Bloomberg 条款、GODL-India 许可原文、《民法典》肖像权条文、Trump 表态原始出处）没再查，已在相应位置注明。
- **本文件不是法律意见**。商业发行前，权利不清的条目要拿到书面确认，或请律师审阅（同 `paid_services.md` § 商业用途）。

## 先说结论

1. **英伟达官方新闻素材在条款上没有明确授权商业使用**。新闻室页脚链接的 NVIDIA Terms of Service 写的是「personal, non-commercial internal use only」，Exec Bios 和 Media Assets 页面上也没有另附媒体使用许可。README 把「官方发布的新闻素材」列为优先级，但本系列按商业发行管理，所以英伟达的官方头像、发布会照片、B-roll 在拿到 press@nvidia.com 书面确认之前，**只按「少量 / 评论性使用」对待**。人物主画面改用下面第 3 条的公共领域或 CC 照片。
2. **NVIDIA logo 不进我们自己的设计元素**。品牌规范写明「may not be used in any manner that isn't expressly authorized in writing」，而且「Usage of our logo also infers a partnership or endorsement」。网页场景里只用文字「NVIDIA / 英伟达」，用我们自己的字体排；真实照片里背景偶然出现的 logo 不算违规使用。
3. **人物画面主体建议用这几类**：白宫官方照片（联邦政府作品，属公共领域，但不得暗示背书）；Commons 上 CC0 和 CC BY 的照片（CES 2025、SC18、2026-04 斯坦福系列）；NVIDIA 官方 Flickr 2014 年以 CC BY-SA 2.0 放出的头像（较旧）。Kress 目前没有好的 CC 照片。
4. **文件类素材都可以作画面主体**：SEC 文件页面、国会委员会信函和新闻稿（委员会版权页援引 17 U.S.C. §105），截图时去掉 SEC 徽标。Exhibit 99.1 新闻稿本身标「© 2026 NVIDIA Corporation. All rights reserved.」，所以只作短引用和截图引证，不整篇搬运。
5. **11-18 是闭门简报请求，不是公开听证**。不会有公开的听证视频可用，只能用委员会的信函和新闻稿。
6. **数据图表全部用我们自己的图重画**：营收和股本取 SEC XBRL（已取到数值，见下文 F 节）；股价不从 Nasdaq 或 Yahoo 抓整段序列（两家条款都限个人、非商业使用），只用单日收盘价这类事实，并注明出处。
7. **Seedance 不生成任何可识别的真实人物**，包括黄仁勋、Kress、Alice Huang、被报道的女高管、Trump。只做象征性、无身份的镜头，并显式标注「AI 生成 / 模拟画面」。

---

## 一、优先级：可作画面主体

### A. 英伟达官方新闻素材：条款核查（结论是降级为「少量」，待书面确认）

**条款原文**（新闻室页脚的「Terms of Service」链接指向这个页面）：<https://www.nvidia.com/en-us/about-nvidia/terms-of-service/>

- §3.1 License Grant：「You may have the option to download one copy of the software and materials found on the Site ("Materials") on a single computer for your personal, non-commercial internal use only unless specifically licensed to do otherwise by NVIDIA in writing or as allowed by any license terms which accompany or are provided with individual Materials.」
- §3.2：「you may not (a) modify the Site or use it for any commercial purpose, or any public display, performance, sale or rental; … (c) remove any copyright or other proprietary notices from the Site」
- §4：「Except as expressly provided in these Terms, NVIDIA and its suppliers do not grant any license or right to you under any patent, copyright, trademark …」
- §17 Trademark Information：「You may not use NVIDIA's trademarks without NVIDIA's prior written permission, and nothing in these Terms will be construed as granting such permission.」
- 查过 Exec Bios、Media Assets（Corporate / Executives / Logos / Keynote Decks）和 GTC 新闻包页面的 HTML，没有找到「editorial」「usage rights」「permission」一类单独附带的媒体使用许可。所以 §3.1 例外里的「license terms which accompany … individual Materials」**在页面上看不到**。

**品牌规范原文**：<https://www.nvidia.com/en-us/about-nvidia/legal-info/logo-brand-usage/>

- 「NVIDIA's logo and other branded elements … may not be used in any manner that isn't expressly authorized in writing by NVIDIA.」
- 「Usage of our logo also infers a partnership or endorsement」
- Unapproved Endorsements：「Do not use NVIDIA branding (logo, names, visual style) in any way that implies affiliation, endorsements, or sponsorship that isn't approved or where the relationship doesn't exist.」
- 「Do not customize or re-create the NVIDIA logo.」「Do not mimic or imitate NVIDIA branding and visual style in your communication」
- 「Do not use artwork from third -party websites that contains NVIDIA branding and imagery. This includes editorial imagery.」（这条针对的是传播物料使用第三方图库里带品牌的图。我们是新闻评论，不受这条直接约束，但说明英伟达对品牌出现在别处很敏感。）

**我们的判断**：用于新闻评论、短时长展示官方照片，美国法下大概率可以主张 fair use（17 U.S.C. §107 列举了「criticism, comment, news reporting」）。但这是抗辩，不是许可，而且我们是商业用途（§107 第 1 因素明列「whether such use is of a commercial nature」）。所以：

| # | 素材 | 链接 | 权利方 | 建议用法 | 风险 |
|---|---|---|---|---|---|
| A1 | 黄仁勋官方头像（1920×1920，文件路径显示 2026-04 上传） | <https://nvidianews.nvidia.com/bios/jensen-huang> | NVIDIA | 先发邮件问 press@nvidia.com 能否用于商业新闻评论；拿到书面许可前不用。替代方案见 D、E 节 | 条款写个人、非商业；他刚因丑闻离职，英伟达未必愿意授权 |
| A2 | Kress 官方头像 | <https://nvidianews.nvidia.com/bios/colette-kress> | NVIDIA | 同 A1。Kress 没有好的 CC 替代图（见 E 节）。没有授权就用文字卡「Colette Kress，临时 CEO 兼 CFO」，不配头像 | 同上 |
| A3 | GTC Berlin 2026（10-21）新闻包照片：「NVIDIA CEO Jensen Huang Delivers GTC Berlin Keynote」等 4 张 | <https://nvidianews.nvidia.com/online-press-kit/gtc-berlin-2026-news> | NVIDIA | 「少量」：配评论，讲「三周前还在台上」，几秒，标「图：NVIDIA」 | 同 A1 |
| A4 | GTC 2026（03-16）新闻包照片：「NVIDIA CEO Jensen Huang at GTC 2026 Keynote」等 | <https://nvidianews.nvidia.com/online-press-kit/gtc-2026-news> | NVIDIA | 同 A3 | 同 A1 |
| A5 | NVIDIA Corporate B-Roll 2026（mp4，总部与园区等） | <https://nvidianews.nvidia.com/multimedia/corporate> | NVIDIA | 只有拿到书面许可才作开场或转场画面；否则不用。总部外景可以改用 Commons 上的 CC 图（本次未检索，待补） | 同 A1 |
| A6 | NVIDIA logo 文件 | <https://nvidianews.nvidia.com/multimedia/corporate/nvidia-logos> | NVIDIA（商标） | **不用**。网页场景只写文字 | 商标规则与暗示背书 |
| A7 | 新闻室页面截图：「A Message to Our Company」（11-08）、董事会声明（11-08）、独立董事声明（11-10）、「NVIDIA Announces CEO Transition」（11-12） | 见简报一手材料第 2–5 条 | NVIDIA | 「少量」：截图标题和关键一句，配我们的评论，每张几秒；引文用我们自己排的引语卡（短引用） | 低。短引用和截图引证都属于评论 |
| A8 | 新闻室页面现状截图（观察结果，可作「公司如何改写一个人」的画面）：Exec Bios 已把黄仁勋列在「Founders」下，写「founded NVIDIA in 1993 and previously served as president, chief executive officer, and a member of the board of directors」；Kress 一栏写「Interim CEO; EVP, Chief Financial Officer」；Media Assets › Executives 图库里已经没有黄仁勋 | <https://nvidianews.nvidia.com/bios>；<https://nvidianews.nvidia.com/multimedia/corporate/corporate-executives> | NVIDIA | 「少量」：截图配评论。截图时间写进台账 | 页面随时可能再改，截图日要记准 |

**GTC 主题演讲视频（NVIDIA YouTube 频道）**：例如「Jensen Huang's Keynote Highlights at NVIDIA GTC Berlin 2026」<https://www.youtube.com/watch?v=rF1EsryCAwc>（oEmbed 显示作者为 NVIDIA；GTC Berlin 主题演讲博客 <https://blogs.nvidia.com/blog/gtc-berlin-2026-keynote/> 另嵌了 12 段 NVIDIA Developer 频道的分段视频）。watch 页面没有找到 Creative Commons 标注，按标准 YouTube 许可处理。YouTube 条款 <https://www.youtube.com/static?template=terms&hl=en&gl=US> 禁止「access, reproduce, download, distribute … any part of the Service or any Content except: (a) as expressly authorized by the Service; or (b) with prior written permission from YouTube and, if applicable, the respective rights holders」。**建议**：归入「少量」，只截 2–3 秒，配我们的评论。素材向英伟达要（press@nvidia.com），或者不用，以静态 CC 照片替代。不要用 yt-dlp 下载。

### B. SEC 文件（可作画面主体，但分清哪部分是谁的）

- **sec.gov 网站声明**（<https://www.sec.gov/privacy>，「Website Dissemination」一节）：「Information presented on sec.gov is considered public information and may be copied or further distributed by users of the web site without the SEC's permission. Please consider appropriate citation to the SEC as the source.」又写：「Please do not use the SEC seal or any of the other logos or artwork from this site.」「'SEC,' the EDGAR logo, and the names EDGAR … are the SEC's registered trademarks」，不得造成「the impression that your business is affiliated with or approved by the SEC」。
- **版权归属**：SEC 自己的页面（EDGAR 界面、索引页）是联邦政府作品。8-K 和 Exhibit 99.1 是**英伟达撰写的文件**，SEC 声明允许复制分发 sec.gov 上的信息，但这不等于英伟达放弃了版权。Exhibit 99.1 文末明写「© 2026 NVIDIA Corporation. All rights reserved. NVIDIA and the NVIDIA logo are trademarks …」。我们的判断：截图和短引用作为一手证据引证，风险低；不整篇朗读、不整页长时间停留。

| # | 素材 | 链接 | 权利方 | 建议用法 | 风险 |
|---|---|---|---|---|---|
| B1 | 8-K（2026-11-12 提交，Item 5.02、9.01；事件日 11-11） | <https://www.sec.gov/Archives/edgar/data/1045810/000104581026000082/nvda-20261111.htm> | 文本：NVIDIA；托管：SEC | 画面主体：截取「accepted the resignation of Jen-Hsun Huang … effective immediately」一句并高亮。可加一张画面讲「8-K 没写原因」 | 截图裁掉 SEC 徽标 |
| B2 | 文件索引页（显示提交时间 2026-11-12 08:52:41） | <https://www.sec.gov/Archives/edgar/data/1045810/000104581026000082/> | SEC | 画面主体：讲提交时间线 | 低 |
| B3 | Exhibit 99.1「NVIDIA Announces CEO Transition」 | <https://www.sec.gov/Archives/edgar/data/1045810/000104581026000082/nvidiaannouncesceotransiti.htm> | NVIDIA（© 声明） | 截标题和三条要点，配评论 | 低到中：短引用即可 |
| B4 | 10-K（FY2026，2026-02-25 提交）风险因素：「we are highly dependent on the services of our longstanding executive team. Failure to ensure effective succession planning, transfer of knowledge, and smooth transitions involving executives and key employees could hinder our strategic planning, execution, and long-term success.」（PDF 页码约第 23 页） | <https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm> | NVIDIA | 画面主体：「公司九个月前自己写过的风险」，正好对接长期道理（关键人物风险） | 低 |
| B5 | 10-K「Information About Our Executive Officers」：黄仁勋 63 岁，Kress 58 岁（截至 2026-02-20） | 同上 | NVIDIA | 文字卡 | 注意 8-K 写 Kress 59 岁（时间点不同，不是冲突） |

### C. 国会委员会文件（联邦政府作品）

- **版权依据**：对华特设委员会版权页 <https://chinaselectcommittee.house.gov/copyright>：「Except as otherwise noted in this website, all of the content of the website constitutes a work of the Federal government under sections 105 and 403 of title 17 of the U.S. Code.」17 U.S.C. §105(a)（<https://www.law.cornell.edu/uscode/text/17/105>）：「Copyright protection under this title is not available for any work of the United States Government」。
- **限制**：USAGov <https://www.usa.gov/government-copyright>：「You cannot use government materials in a way that implies endorsement by a government agency, official, or employee.」议员照片和委员会徽章不当作我们自己的包装元素使用。

| # | 素材 | 链接 | 建议用法 | 风险 |
|---|---|---|---|---|
| C1 | 11-05 新闻稿：Moolenaar、Mast、Crawford 请黄仁勋参加「a joint, closed-door briefing」，「requested that he brief the committees on November 18, 2026. Mr. Huang must accept the invitation or provide alternative availability by November 11, 2026.」 | <https://chinaselectcommittee.house.gov/media/press-releases/moolenaar-mast-and-crawford-seek-briefing-from-jensen-huang-on-ties-to-chinese-intelligence-asset> | 画面主体：截图并高亮「closed-door」 | 低。注意信中把 Alice Huang 称为「a publicly reported Chinese intelligence asset」，这是委员会的说法，片中要标「委员会称 / 报道称」 |
| C2 | 11-12 第二次请求：致「former NVIDIA CEO Jensen Huang」、总法律顾问 Tim Teter、商务部副部长 Jeffrey Kessler 的三封信（PDF） | 新闻稿 <https://chinaselectcommittee.house.gov/media/press-releases/chairmen-moolenaar-mast-and-crawford-send-second-request-to-jensen-huang-and-nvidia-to-brief-congress>；PDF <https://foreignaffairs.house.gov/sites/evo-subsites/republicans-foreignaffairs.house.gov/files/evo-media-document/11.12.26-chairmen-letter-to-mr-jensen-huang.pdf>、<https://foreignaffairs.house.gov/sites/evo-subsites/republicans-foreignaffairs.house.gov/files/evo-media-document/11.12.26-chairmen-letter-to-nvidia-gc.pdf>、<https://foreignaffairs.house.gov/sites/evo-subsites/republicans-foreignaffairs.house.gov/files/evo-media-document/11.12.26-invitation-to-u-s-kessler.pdf>；外交委员会同文 <https://foreignaffairs.house.gov/news/press-releases/chairmen-mast-moolenaar-and-crawford-send-second-request-to-jensen-huang-and-nvidia-to-brief-congress-on-the-chinese-intelligence-asset> | 画面主体：信函首页截图（**PDF 本次只记链接，没有打开核对内容**） | 低 |
| C3 | 11-12 Moolenaar 声明：「Jensen Huang's firing from the company he founded is an unfortunate end that could have been avoided.」 | <https://chinaselectcommittee.house.gov/media/press-releases/moolenaar-statement-on-jensen-huang-s-resignation-from-nvidia> | 引语卡：放在「辞职还是被撤换」这一段，作为一方的说法 | 「firing」与公司口径「resignation」冲突，片中两边都列 |
| C4 | 11-18 闭门简报的视频 | — | **不存在公开视频**：这是闭门简报请求，不是公开听证。不要找，也不要用「听证会」字样的二手剪辑 | — |

### D. 白宫与其他政府的官方照片

- 白宫版权页 <https://www.whitehouse.gov/copyright/>：「Pursuant to federal law, government-produced materials appearing on this site are not copyright protected.」白宫 Flickr 照片的许可字段指向 <https://www.usa.gov/government-copyright>（United States Government Work）。
- USAGov 同页的限制：「On federal websites, other people may have rights to the work itself or how people use it. This includes publicity or privacy rights under state law.」「You cannot use government materials in a way that implies endorsement by a government agency, official, or employee.」
- 白宫 Flickr 主页和单张照片页面上，**这次没有抓到**过去常见的「only for publication by news organizations … may not be manipulated」限制性说明（页面是动态加载的）。下载时要再看一次页面并截图存证。

| # | 素材 | 链接 | 权利方 / 许可 | 建议用法 | 风险 |
|---|---|---|---|---|---|
| D1 | 2026-05-13 北京首都机场到达仪式：Trump 向中方官员介绍 Musk、黄仁勋等科技界人士（Official White House Photo by Daniel Torok，3000×2000） | Commons <https://commons.wikimedia.org/wiki/File:P20260513DT-0328_President_Donald_J._Trump_participates_in_an_arrival_ceremony_at_Beijing_International_Airport.jpg>；Flickr <https://www.flickr.com/photos/202101414@N05/55272554325/> | 美国联邦政府作品，公共领域 | **画面主体首选**：直接对应「中美、芯片、黄仁勋在政治中心」的语境。署名「White House / Daniel Torok」（公共领域不强制署名，但建议标） | 画面里还有 Trump、Musk、中方官员：不裁成暗示任何人背书的样子，不配引导性字幕 |
| D2 | 2025-11-18 白宫欢迎沙特王储晚宴，黄仁勋抵达（Daniel Torok，645×839，分辨率偏低） | <https://commons.wikimedia.org/wiki/File:Jen-Hsun_Huang_2025.jpg>；Flickr <https://www.flickr.com/photos/202101414@N05/54934445728/> | 公共领域 | 半身像，可作人物介绍卡 | 分辨率低，只能小图用 |
| D3 | 2023-11-09 台湾「总统府」李国鼎奖颁奖（Flickr presidentialoffice） | <https://commons.wikimedia.org/wiki/File:Jensen_Huang_20231109.jpg>（另有裁切版 `(cropped2)`） | CC BY 2.0，作者「總統府」 | 可用，署名「總統府 / CC BY 2.0」 | 两岸政治语境敏感，中文平台发布时要考虑 |
| D4 | 2025-04-21 会见日本首相石破茂（首相官邸） | <https://commons.wikimedia.org/wiki/File:Jen-Hsun_Huang_meets_Shigeru_Ishiba.jpg> | Commons 标 CC BY 4.0，作者「首相官邸」 | 讲「国家元首级接待的 CEO」时可用 | 官邸条款是否等同 CC BY 4.0，本次未核原文 |
| D5 | 2023-09-04 会见印度总理莫迪（PIB） | <https://commons.wikimedia.org/wiki/File:Jensen_Huang_meeting_with_Indian_PM_Narendra_Modi_01.jpg> | Commons 标 GODL-India | 备选 | GODL-India 许可原文本次未核，进成片前要核 |
| D6 | 2024-05-13 与欧盟高级代表博雷利会面（Photographer: Peter Dasilva，LicenseReview 已通过） | <https://commons.wikimedia.org/wiki/File:Josep_Borrell_with_NVIDIA_CEO_and_founder_Jensen_Huang_(2024).jpg>；单人裁切 <https://commons.wikimedia.org/wiki/File:Jensen_Huang_(cropped)_(2024).jpg> | CC BY 4.0 | 单人裁切版可作头像 | 低 |

### E. Wikimedia Commons 上的 CC 照片（逐张列许可与作者）

数据来自 Commons API 的 extmetadata（LicenseShortName / Artist / Restrictions），**以文件页为准，下载当天要再核一次**。其中几张标了「Personality rights」警示，原文是「Although this work is freely licensed or in the public domain, the person(s) shown may have rights that legally restrict certain re-uses unless those depicted consent to such uses.」（<https://commons.wikimedia.org/wiki/Template:Personality_rights>）。

署名格式建议：「照片：作者 / Wikimedia Commons / 许可名（链接）/ 是否裁切」，写进片尾和视频简介。本系列偏好顺序（我们的判断）：公共领域、CC0、CC BY 优先，CC BY-SA 其次。BY-SA 的「相同方式共享」用在视频里会不会让整片受约束，存在解释空间，所以尽量不用。

| # | 文件（Commons 页） | 许可 | 作者 | 拍摄日期 | 限制标记 | 建议 |
|---|---|---|---|---|---|---|
| E1 | [Jensen_Huang_-_Nvidia_Keynote_-_CES_2025_Las_Vegas_(1).jpg](https://commons.wikimedia.org/wiki/File:Jensen_Huang_-_Nvidia_Keynote_-_CES_2025_Las_Vegas_(1).jpg)（4032×3024） | CC0 | Pronoia | 2025-01-06 | — | **首选舞台照**：没有署名义务，仍建议标作者 |
| E2 | [JensenHuangSC18.jpg](https://commons.wikimedia.org/wiki/File:JensenHuangSC18.jpg)（4928×3264） | CC0 | Raysonho @ Open Grid Scheduler / Scalable Grid Engine | 2018-11-12 | — | 备选，年份较早 |
| E3 | [Jensen_huang_stanford_2026-04-30_008_(cropped).jpg](https://commons.wikimedia.org/wiki/File:Jensen_huang_stanford_2026-04-30_008_(cropped).jpg)（及同系列 2026-04-30 001–038 约 30 张） | CC BY 4.0 | Anders Eidesvik | 2026-04-30（斯坦福 CS 153 课堂） | Personality rights | **首选近照**：离事件最近的高清图 |
| E4 | [Jensen_huang_and_ro_khanna_stanford_2026-04-09_001.jpg](https://commons.wikimedia.org/wiki/File:Jensen_huang_and_ro_khanna_stanford_2026-04-09_001.jpg)；同场与 H.R. McMaster 合影（如 `H_r_mcmaster_jensen_huang_and_ro_khanna_stanford_2026-04-09_026.jpg`） | CC BY 4.0 | Anders Eidesvik | 2026-04-09 | 部分标 Personality | 讲「芯片出口与国家安全」时可用（同台的是国会议员和前国家安全顾问）；不要配暗示他们对本案表态的字幕 |
| E5 | [Jen-Hsun_Huang_Headshot_(15313247387).jpg](https://commons.wikimedia.org/wiki/File:Jen-Hsun_Huang_Headshot_(15313247387).jpg)（4305×2870） | CC BY-SA 2.0（FlickreviewR 已核） | nvidia.corporation（**英伟达官方 Flickr**） | 2014-10-10 | Personality rights | 唯一一张由英伟达自己以 CC 放出的头像；但年份旧，而且是 BY-SA |
| E6 | [Jensen_Huang_at_Computex_Taipei_20160531a.jpg](https://commons.wikimedia.org/wiki/File:Jensen_Huang_at_Computex_Taipei_20160531a.jpg)（b、c 两张同系列） | CC BY 2.0（FlickreviewR 已核） | NVIDIA Taiwan（官方 Flickr） | 2016-05-31 | — | 讲「早年」时可用 |
| E7 | [Jensen_Huang_Nvidia_Keynote_CES_2025.jpg](https://commons.wikimedia.org/wiki/File:Jensen_Huang_Nvidia_Keynote_CES_2025.jpg) | CC BY-SA 4.0 | Joseph Zadeh | 2025-01-06 | — | E1 的备选 |
| E8 | [Nvidia_CEO_Jensen_Huang_gestikuliert.jpg](https://commons.wikimedia.org/wiki/File:Nvidia_CEO_Jensen_Huang_gestikuliert.jpg) | CC BY 2.0 | Maurizio Pesce | 2017-01-05 | Personality rights | 备选 |
| E9 | [Jensen_Huang_at_Computex_Taipei_20100531.jpg](https://commons.wikimedia.org/wiki/File:Jensen_Huang_at_Computex_Taipei_20100531.jpg) | CC BY 2.0 | Masaru Kamikura | 2010-05-31 | — | 讲「33 年」时间跨度时可用 |
| E10 | [Colette_Kress_(1).png](https://commons.wikimedia.org/wiki/File:Colette_Kress_(1).png)（609×845）/ [Colette_Kress.png](https://commons.wikimedia.org/wiki/File:Colette_Kress.png) | CC BY 4.0 / CC BY 3.0（两版许可写法不一） | SiliconANGLE theCUBE（2017 年 YouTube 视频截帧） | 2017-05-01 | — | 质量差、年份旧；Kress 宁可只用文字卡 |

**注意**：`Jensen_Huang_Stanford_2026-04-30_010_(cropped).jpg` 标为 CC BY-SA 4.0、作者「Anderseidesvik」，而同系列原图是 CC BY 4.0。许可不一致，要用就用原图并按原图许可署名。

### F. 公开数据重画（用我们自己的图表）

**营收与股本：SEC XBRL 接口（联邦政府网站上的公开数据）**

数据源：<https://data.sec.gov/api/xbrl/companyconcept/CIK0001045810/us-gaap/Revenues.json>，<https://data.sec.gov/api/xbrl/companyconcept/CIK0001045810/dei/EntityCommonStockSharesOutstanding.json>（取于 2026-11-14）。下表数值进成片前，请财务角度对照 10-K / 10-Q 原文核一次。

| 期间 | 营收（美元） | 来源文件 |
|---|---|---|
| FY2025（至 2025-01-26） | 130,497,000,000 | 10-K，2026-02-25 提交，accn 0001045810-26-000021（比较期数据） |
| FY2026（至 2026-01-25） | 215,938,000,000 | 同上 |
| Q1 FY2026（至 2025-04-27） | 44,062,000,000 | 10-Q，2026-05-20 提交（比较期） |
| Q2 FY2026（至 2025-07-27） | 46,743,000,000 | 10-Q，2026-08-26 提交（比较期） |
| Q3 FY2026（至 2025-10-26） | 57,006,000,000 | 10-Q，2025-11-19 提交 |
| Q1 FY2027（至 2026-04-26） | 81,615,000,000 | 10-Q，2026-05-20 提交，accn 0001045810-26-000052 |
| Q2 FY2027（至 2026-07-26） | 96,221,000,000 | 10-Q，2026-08-26 提交，accn 0001045810-26-000075 |

- 流通股（10-Q 封面，截至 2026-08-21）：24,100,000,000 股。
- **我们的计算，不是报道值**：按 11-12 收盘 $166.19（价格出自简报二手线索，待核）× 241 亿股，约 4.0 万亿美元。只能作「约」字出现，并说明是我们估算的。
- Q3 FY2027 财报 11-17 才发布，片子若在那之后定稿，要补这一季。

**股价：数据来源条款**

- Nasdaq 条款（<https://www.nasdaq.com/legal>，页面内的 Terms of Use）：「Nasdaq grants you a personal, limited, revocable, non-exclusive … license to use the Services solely for your personal, non-commercial use. Except as expressly authorized by Nasdaq, you agree not to sell, copy, distribute, or create derivative works based on the Services」，还禁止用「any process, whether automated or manual, to capture data or content from the Service」。
- Yahoo 条款（<https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html>）：「Unless you have explicit written permission, you must not reproduce, modify, … distribute, … create derivative works based on, or exploit for any commercial purposes, any portion or use of, or access to, the Services (including content …)」。
- **建议（我们的判断）**：不抓取 Nasdaq 或 Yahoo 的整段历史序列做商业图表。只画少数关键日（10-29、11-09、11-12 及 11-17 财报后）的收盘价和涨跌幅，每个点单独注明出处（交易所公告或主流报道，多个来源互核）；单个价格属于事实。需要连续走势时，用有商业许可的数据源，或请用户决定。不截第三方行情软件的 K 线图。

---

## 二、少量：只作评论对象（配我们的评论，单段几秒，不作画面主体，标注来源）

依据：17 U.S.C. §107（<https://www.law.cornell.edu/uscode/text/17/107>）：「the fair use of a copyrighted work … for purposes such as criticism, comment, news reporting, teaching … is not an infringement of copyright」，四个因素第一项就是「whether such use is of a commercial nature」。中国《著作权法》第二十四条（<https://www.gov.cn/guoqing/2021-10/29/content_5647633.htm>）：「（二）为介绍、评论某一作品或者说明某一问题，在作品中适当引用他人已经发表的作品」，但「应当指明作者姓名或者名称、作品名称，并且不得影响该作品的正常使用，也不得不合理地损害著作权人的合法权益」。

| # | 素材 | 链接 | 权利方与条款 | 建议用法 | 风险 |
|---|---|---|---|---|---|
| S1 | NYT 10-29 首报和 11-11 第二段婚外情报道的标题页截图 | NYT 原文 URL 待核（简报只有转述链接） | NYT 条款 <https://help.nytimes.com/policies/115014893428-Terms-of-Service>：「intended for your personal, non-commercial use」，「You may not modify, publish, transmit … reproduce … create new works from, distribute, perform, display … any of the Content」 | 只截标题和日期，2–3 秒，讲「谁先报的」；**截图前确认标题里不出现第二位当事人的姓名，出现就打码** | 中。NYT 维权积极，正文段落不截 |
| S2 | CNBC 11-12 报道页截图 | <https://www.cnbc.com/2026/11/12/nvidia-nvda-jensen-huang-second-affair.html> | CNBC 条款页（<https://www.cnbc.com/terms/>，抓到的是 CNBC+ 条款）禁止「recording, copying, storage, rebroadcasting, retransmission or redistribution」 | 同 S1 | 中 |
| S3 | CNBC / Bloomberg 等电视或视频片段（例如盘中跌幅报道） | 待定 | 有版权；**Bloomberg 条款本次没有取到原文** | 单段 ≤3 秒，配我们的解说压过原声，标「来源：CNBC」。不下载整段，向用户确认素材取得方式 | **高**：YouTube 和 B 站可能触发 Content ID 版权认领。能不用就不用，用 F 节数据图替代 |
| S4 | Forbes、Foreign Policy、NPR、ABC（澳）报道标题截图 | 见简报二手线索 | 各家版权 | 讲「舆论分歧」时做标题拼贴，每张 1–2 秒 | 中 |
| S5 | GTC 主题演讲片段（NVIDIA YouTube） | 见 A 节 | NVIDIA 版权 + YouTube 条款 | 2–3 秒，讲「他的舞台形象」 | 中。优先用 E1 静态照片替代 |
| S6 | 中国外交部例行记者会**文字实录**（11-09、11-10 郭嘉昆；11-12、11-13 毛宁） | 列表页 <https://www.mfa.gov.cn/web/fyrbt_673021/jzhsl_673025/>；11-09 <https://www.mfa.gov.cn/web/fyrbt_673021/jzhsl_673025/202611/t20261109_12056081.shtml>；11-10 `…/t20261110_12056801.shtml`；11-11 `…/t20261111_12057499.shtml`；11-12 `…/t20261112_12058185.shtml`；11-13 `…/t20261113_12058837.shtml` | 页脚「中华人民共和国外交部　版权所有」；网站上没有找到单独的转载条款。答问实录不属于《著作权法》第五条（一）所列的「具有立法、行政、司法性质的文件」，所以要按第二十四条「适当引用」处理（我们的判断） | **用我们自己排的引语卡**，短引用原话，注明「外交部 2026-11-09 例行记者会实录」；可以截实录网页 2 秒作引证 | 低 |
| S7 | 外交部记者会**视频** | 外交部网站没有找到视频；视频通常来自央视等媒体 | 视频权利属于转播或拍摄方（央视等），不是外交部 | 不用，或只用 2–3 秒并标明来源 | 中到高。用 S6 文字卡替代 |
| S8 | Trump 的公开表态 | **出处待核**（简报只说「有公开表态」；本次检索额度用完，没核） | 白宫官方活动的视频和文字是联邦政府作品，属公共领域；Truth Social 帖子归作者，截图属评论性使用 | 核到原始出处后：白宫视频可作主体（不暗示背书）；帖子截图 2–3 秒 | 未核前不用 |

---

## 三、不用

| # | 素材 | 理由 |
|---|---|---|
| X1 | Alice Huang（黄乐）的任何照片，包括 Megaspeed 官网、领英、新闻配图 | 据二手报道转述，她和 Megaspeed 都没有被控任何罪名（本次只在检索摘要里看到，没有看到委员会原文或起诉记录，待核），「情报人员」是指控未证实。把她的脸放进「间谍丑闻」片子，有诽谤和隐私风险；画面一配图，观众就会默认指控成立。片中可以说「报道点名的一位新加坡数据中心公司高管」，是否念名字由讲稿审议定（建议只写一次，标「报道称」） |
| X2 | 报道中第二段（以及「第三段」）关系涉及的英伟达在职女高管：**照片、姓名、职位细节都不用** | 她是非公众人物，因私人关系被卷入。片中**不点名**（简报隐私提醒）；媒体截图里出现她的姓名就打码或不用 |
| X3 | 黄仁勋家人（妻子、子女）的照片 | 与公共利益无关，属于私人生活 |
| X4 | 来源不明的偷拍、街拍、「两人同框」传播图、社交平台二传视频 | 来源不明，属于 README「不用」一级；真假也无法核实 |
| X5 | 整段搬运的新闻视频、去水印素材、二创合集 | README「不用」一级 |
| X6 | 任何 AI 换脸、修图、合成的真人图像（包括网上流传的） | 有误导与诽谤风险，也违反下面四节的规定 |
| X7 | NVIDIA logo 作为片头、封面、转场的设计元素 | 品牌规范要求书面授权，而且会暗示背书（A 节） |
| X8 | SEC 徽章、EDGAR logo、国会委员会徽章作包装元素 | sec.gov 原文「Please do not use the SEC seal or any of the other logos」；USAGov 不得暗示背书 |

---

## 四、Seedance 模拟镜头：不生成可识别的真实人物

**条款与规定原文**

- Dreamina 美国版 Terms of Service（Last updated: January 22, 2026）<https://dreamina.capcut.com/clause/dreamina-terms-of-service>：
  - 不得「use the Services in a manner that violates or infringes on any third party's rights of publicity, privacy, copyright, trademark, or other intellectual property rights or other rights」
  - 不得「impersonate any person or entity」
  - 不得「generate or disseminate verifiably false information and/or content with the purpose of harming others」；不得「defame, disparage or otherwise harass others」
  - 上传内容须「have, or have obtained, all rights, licenses, consents, permissions」（所以不能上传黄仁勋照片作参考图）
- Dreamina Community Guidelines <https://dreamina.capcut.com/clause/dreamina-community-guidelines>：「we do not allow misinformation that causes harm to individuals, our community, or the larger public regardless of intent」；对公众人物「critical comments of public figures may be allowed; however, serious abusive behavior against public figures is not allowed」。
- 两份文件都**没有**写「禁止生成真人」的明文。限制来自公开权、隐私、冒充、虚假信息几条，合起来已经足以排除「生成黄仁勋模拟镜头」。即梦（国内版）协议原文仓库没有取得（`paid_services.md`）。
- 本仓库 `paid_services.md` § 商业用途：Dreamina 视频条款对商业用途「不明确」，用户 2026-10-09 知情后决定继续使用；OpenAI 图像（Codex 出图）「未经明确同意不得生成真人肖像」。所以 Seedance 首帧参考图如果用 Codex 出，同样不能是真人。
- 中国《互联网信息服务深度合成管理规定》<https://www.gov.cn/zhengce/zhengceku/2022-12/12/content_5731431.htm>：第六条「深度合成服务提供者和使用者不得利用深度合成服务制作、复制、发布、传播虚假新闻信息」；第十四条要求编辑人脸、人声须「取得其单独同意」。
- 《人工智能生成合成内容标识办法》（2025-09-01 起施行）<https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm>：第十条「用户使用网络信息内容传播服务发布生成合成内容的，应当主动声明并使用服务提供者提供的标识功能进行标识」。
- 《民法典》肖像权条款（第一千零一十九、一千零二十条，新闻报道的合理使用）：本次没有取到原文，进成片前请补。

**建议镜头规范（我们的判断）**

- 可以做：空无一人的董事会会议室、长桌和空椅子；晶圆、GPU 芯片、机柜的特写；SEC 文件在屏幕上滚动；数据中心走廊；象征性的剪影（无脸、无标志性穿着、不对应具体人物）；股票行情屏幕（数字用我们核过的数据）。
- 不做：黄仁勋或任何真人的脸、背影、声音；**黑色皮夹克加舞台这类一看就能认出是谁的组合**；被报道当事人的「重现」（酒店、会面、私人场景）；任何「间谍接头」式的情节化重现。这类画面等于把指控拍成事实。
- 每个 Seedance 镜头在画面上加显式标注「AI 生成 / 模拟画面」，并写进 media_ledger 和视频简介。
- 照全局规则：先写本期 `request_log.md`，生成由用户来点。

---

## media_ledger 候选

字段沿用 README（原始链接、权利方、许可或「评论性使用」、用哪段、第几段画面、下载时间与本地路径）。下面「用哪段 / 第几段画面 / 下载」留到讲稿定了再填；**本次一律没有下载**。

| id | 素材 | 原始链接 | 权利方 | 许可 / 使用依据 | 级别 | 署名 / 备注 |
|---|---|---|---|---|---|---|
| m01 | 白宫照片：北京机场到达仪式（2026-05-13） | https://www.flickr.com/photos/202101414@N05/55272554325/ | 美国联邦政府（白宫，摄影 Daniel Torok） | 公共领域（联邦政府作品）；不得暗示背书 | 优先 | 「White House / Daniel Torok」 |
| m02 | 白宫照片：沙特王储晚宴（2025-11-18） | https://commons.wikimedia.org/wiki/File:Jen-Hsun_Huang_2025.jpg | 同上 | 公共领域 | 优先 | 分辨率低 |
| m03 | CES 2025 舞台照 | https://commons.wikimedia.org/wiki/File:Jensen_Huang_-_Nvidia_Keynote_-_CES_2025_Las_Vegas_(1).jpg | Pronoia | CC0 | 优先 | 建议仍标作者 |
| m04 | 斯坦福 2026-04-30 近照 | https://commons.wikimedia.org/wiki/File:Jensen_huang_stanford_2026-04-30_008_(cropped).jpg | Anders Eidesvik | CC BY 4.0 | 优先 | 「Anders Eidesvik / Wikimedia Commons / CC BY 4.0，裁切」；有 Personality rights 警示 |
| m05 | 斯坦福 2026-04-09 与 Ro Khanna 同台 | https://commons.wikimedia.org/wiki/File:Jensen_huang_and_ro_khanna_stanford_2026-04-09_001.jpg | Anders Eidesvik | CC BY 4.0 | 优先 | 字幕不暗示同台者对本案表态 |
| m06 | 英伟达官方 Flickr 2014 头像 | https://commons.wikimedia.org/wiki/File:Jen-Hsun_Huang_Headshot_(15313247387).jpg | NVIDIA（nvidia.corporation） | CC BY-SA 2.0 | 优先（备选） | BY-SA；Personality rights 警示 |
| m07 | 8-K 页面截图 | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000082/nvda-20261111.htm | 文本 NVIDIA；托管 SEC | sec.gov「may be copied or further distributed」+ 短引用 | 优先 | 裁掉 SEC 徽标 |
| m08 | Exhibit 99.1 截图 | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000082/nvidiaannouncesceotransiti.htm | NVIDIA（©） | 评论性引用 | 优先（短） | — |
| m09 | 10-K 风险因素段落截图 | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm | NVIDIA | 评论性引用 | 优先（短） | — |
| m10 | 委员会 11-05 新闻稿截图 | https://chinaselectcommittee.house.gov/media/press-releases/moolenaar-mast-and-crawford-seek-briefing-from-jensen-huang-on-ties-to-chinese-intelligence-asset | 美国众议院对华特设委员会 | 联邦政府作品（17 U.S.C. §105、403） | 优先 | — |
| m11 | 委员会 11-12 致「former NVIDIA CEO」信函 PDF 首页 | https://foreignaffairs.house.gov/sites/evo-subsites/republicans-foreignaffairs.house.gov/files/evo-media-document/11.12.26-chairmen-letter-to-mr-jensen-huang.pdf | 众议院外交委员会等 | 联邦政府作品 | 优先 | PDF 未打开核对 |
| m12 | Moolenaar 11-12 声明截图 | https://chinaselectcommittee.house.gov/media/press-releases/moolenaar-statement-on-jensen-huang-s-resignation-from-nvidia | 同 m10 | 联邦政府作品 | 优先 | 与「resignation」口径冲突 |
| m13 | 英伟达新闻室声明页截图（4 页） | 简报一手材料 2–5 | NVIDIA | 评论性使用 | 少量 | 每张 ≤3 秒 |
| m14 | 新闻室 Exec Bios 现状截图 | https://nvidianews.nvidia.com/bios | NVIDIA | 评论性使用 | 少量 | 记截图时间 |
| m15 | GTC Berlin 新闻包照片 | https://nvidianews.nvidia.com/online-press-kit/gtc-berlin-2026-news | NVIDIA | 待书面确认；否则评论性使用 | 少量 | — |
| m16 | 外交部 11-09 实录截图与引语卡 | https://www.mfa.gov.cn/web/fyrbt_673021/jzhsl_673025/202611/t20261109_12056081.shtml | 中华人民共和国外交部 | 《著作权法》第二十四条适当引用 | 少量 | — |
| m17 | NYT 标题截图 | 待核 | NYT | 评论性使用 | 少量 | 出现第二当事人姓名即打码 |
| m18 | 营收与股本数据图（自绘） | https://data.sec.gov/api/xbrl/companyconcept/CIK0001045810/us-gaap/Revenues.json | 数据来自 SEC 申报 | 自绘图表，注明「数据：SEC 申报（10-K/10-Q）」 | 优先 | 进成片前对照原文核数 |

## 台账候选（claims.json）

| claim | source | quote | status |
|---|---|---|---|
| 三位委员会主席请黄仁勋参加的是「闭门」联合简报，日期 11-18，限 11-11 前答复 | https://chinaselectcommittee.house.gov/media/press-releases/moolenaar-mast-and-crawford-seek-briefing-from-jensen-huang-on-ties-to-chinese-intelligence-asset | "requesting his participation in a joint, closed-door briefing" / "requested that he brief the committees on November 18, 2026. Mr. Huang must accept the invitation or provide alternative availability by November 11, 2026." | 已证实（政府文件） |
| 11-12 委员会发出第二次请求，收信人包括「former NVIDIA CEO」黄仁勋、总法律顾问 Tim Teter、商务部副部长 Jeffrey Kessler | https://chinaselectcommittee.house.gov/media/press-releases/chairmen-moolenaar-mast-and-crawford-send-second-request-to-jensen-huang-and-nvidia-to-brief-congress | "sent letters to former NVIDIA CEO Jensen Huang, NVIDIA General Counsel Tim Teter, and Under Secretary of Commerce Jeffrey Kessler requesting their appearance before Congress." | 已证实（政府文件） |
| Moolenaar 把这次离任称为「firing」 | https://chinaselectcommittee.house.gov/media/press-releases/moolenaar-statement-on-jensen-huang-s-resignation-from-nvidia | "Jensen Huang's firing from the company he founded is an unfortunate end that could have been avoided." | 已证实（是他的原话）；离任性质有争议 |
| 英伟达 FY2026 10-K 自述高度依赖长期管理团队，接班安排不当会伤害长期发展 | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm | "we are highly dependent on the services of our longstanding executive team. Failure to ensure effective succession planning, transfer of knowledge, and smooth transitions involving executives and key employees could hinder our strategic planning, execution, and long-term success." | 已证实（公司文件） |
| 英伟达 FY2026（至 2026-01-25）营收 2159.38 亿美元；Q2 FY2027 单季 962.21 亿美元 | https://data.sec.gov/api/xbrl/companyconcept/CIK0001045810/us-gaap/Revenues.json | Revenues 215938000000（10-K，2026-02-25）；96221000000（10-Q，2026-08-26） | 已证实（SEC XBRL；待对照原文） |
| 截至 2026-11-14，英伟达新闻室 Exec Bios 把黄仁勋列为「Founder」，写「previously served as president, chief executive officer…」；Kress 一栏写「Interim CEO; EVP, Chief Financial Officer」 | https://nvidianews.nvidia.com/bios/jensen-huang ；https://nvidianews.nvidia.com/bios/colette-kress | "Jensen Huang founded NVIDIA in 1993 and previously served as president, chief executive officer, and a member of the board of directors." / "Colette Kress is interim CEO, as well as executive vice president and chief financial officer of NVIDIA." | 已证实（公司网页，2026-11-14 所见） |
| 外交部 11-09 回应：「中国间谍」说法是捕风捉影 | https://www.mfa.gov.cn/web/fyrbt_673021/jzhsl_673025/202611/t20261109_12056081.shtml | 郭嘉昆：「我们此前已就此作出回应。所谓"中国间谍"的论调纯属捕风捉影，污蔑抹黑。」 | 已证实（是官方原话）；所涉指控未证实 |
| 外交部 11-12：要求美方停止「间谍叙事」 | https://www.mfa.gov.cn/web/fyrbt_673021/jzhsl_673025/202611/t20261112_12058185.shtml | 毛宁：「美方应当停止编造所谓的"间谍叙事"，为实施科技封锁寻找借口。」 | 已证实（是官方原话） |
| 外交部对「黄乐身在北京」的提问答「不了解」（11-12、11-13 彭博社提问） | 同上；https://www.mfa.gov.cn/web/fyrbt_673021/jzhsl_673025/202611/t20261113_12058837.shtml | 毛宁：「我不了解你提到的情况。」（11-12）/「关于第一个问题，我不了解有关情况。」（11-13） | 已证实（原话）；行踪尚不清楚 |
| 外交部实录中，记者提问时提到「黄仁勋已承认与其有婚外情」 | https://www.mfa.gov.cn/web/fyrbt_673021/jzhsl_673025/202611/t20261109_12056081.shtml | 法新社记者：「黄仁勋已承认与其有婚外情，英伟达董事会对黄仁勋展开调查。」 | 是记者提问里的说法，不是外交部的表态。黄仁勋信中承认「unfaithful」，但没有点名对象 |

## 尚不清楚 / 冲突

1. **英伟达新闻素材能否商用**：新闻室页面没有单独的媒体使用许可，网站条款写个人、非商业。这和 README 把「官方新闻素材」列为优先之间有冲突。需要 press@nvidia.com 书面确认，或由用户决定降级使用（本文件按降级处理）。
2. **「resignation」还是「firing」**：8-K 和新闻稿写的是董事会「accepted the resignation」；Moolenaar 声明写「firing」。片中两边都列，不下结论。
3. **11-18 是「作证」还是「简报」**：简报线索写「要求 11-18 作证」；委员会原文是「closed-door briefing」请求，第二封信写「requesting their appearance before Congress」。黄仁勋是否答应、会不会发传票，尚不清楚（ABC 转述 Mast 称可能发传票，未见原文）。
4. **外交部「此前已就此作出回应」是哪一天**：11-09 实录这样说，但更早那次答问本次没有找到，可能在 10-29 至 11-06 之间，尚不清楚。
5. **白宫 Flickr 照片的附加使用说明**：这次没有抓到动态页面里的说明文字，下载前要再核并截图存证。
6. **Commons 许可不一致**：斯坦福 2026-04-30 010 裁切版标 CC BY-SA 4.0，原图系列标 CC BY 4.0；Kress 的两张截帧一张标 CC BY 4.0、一张标 CC BY 3.0。
7. **没有核原文的条款**：Bloomberg 条款、GODL-India、日本首相官邸使用条款、《民法典》肖像权条文、即梦国内版协议、YouTube 和 B 站对 AI 生成内容的披露政策。11-12 委员会信函 PDF 只记了链接，没有打开。
8. **Kress 年龄**：10-K 写 58 岁（截至 2026-02-20），8-K 写 59 岁。这是时间点不同，不是冲突，片中以 8-K 为准。
9. **股价连续序列**：没有找到可以商业再分发的免费来源，片中只用关键日的数值。
