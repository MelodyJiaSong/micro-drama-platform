---
worker_id: researcher-04-benchmark-format
stage: 3
role: researcher
angle: benchmark-format
status: partial
blockers:
  - "YouTube 单条元数据与评论拿不到：yt-dlp meta 被 YouTube 拦截，要求登录验证（不用 cookies 绕过）。YouTube 只有播放量和时长，点赞与评论都没有"
  - "Reddit 拿不到：reddit.com 与镜像站 WebFetch 返回 403，WebSearch 不接受 reddit.com 域名。英文提问来源改用 Quora、Physics Forums 和搜索结果里的 ELI5 标题"
confidence: medium
---

# 芯片系列 · 对标与形式调研（t01 角度文件）

> 查看日期：2026-11-14。频道通用结论已在 `edu_videos/_shared/research/explainer_benchmark.md` 中，本文不重复，只补芯片题材和「缩小 + 双人问答」形式的证据。
> 数据来源：YouTube 播放量与时长来自仓库工具 `tools/yt_research.py search/channel`（yt-dlp 扁平检索，只有播放量和时长；`meta` 被要求登录，点赞与评论都没拿到）。B 站数据来自公开接口 `x/web-interface/view` 与 `x/v2/reply`（热评第 1 页）。原始 JSONL 在会话草稿目录，未入库。
> 表中「赞/播」「藏/播」由接口原始数字算出。没核实过的描述都标了「未核实」。

## 1. 高影响力芯片 / 晶体管 / 制造视频

### 1a. YouTube（播放量查于 2026-11-14）

| # | 视频 | 链接 | 播放 | 时长 | 讲法与画面 | 讲得好 | 缺了什么 |
|---|---|---|---|---|---|---|---|
| 1 | Branch Education · How are Microchips Made? | https://www.youtube.com/watch?v=dX9CGRZwD-w | 1194 万 | 27:48 | 单人旁白，Blender 3D 全程建模，从晶圆厂走到单个工艺步骤；HN 上 2024-05 有人转贴 | 结构准确、镜头连续，作者称是「做过最复杂的一期」 | 长 28 分钟，一期塞几百道工序；没有人物，也没有观众的问题线 |
| 2 | Branch Education · How do Transistors Build into a CPU? | https://www.youtube.com/watch?v=_Pqfjer8-O4 | ≈250 万（频道列表取整） | 26:45 | 3D：单个晶体管 → 反相器 / 与门 → 宏单元 → 运算；用乐高积木作比喻（BlenderNation 2025-06-24 与 Evertiq 2025-11-21 的介绍） | 从开关到逻辑的「搭积木」层级讲得清楚 | 同样很长；缩放时没有持续可见的比例尺（据介绍文，未逐帧核实） |
| 3 | Branch Education · How do CPUs Work? | https://www.youtube.com/watch?v=16zrEPOsIcI | 332 万 | 36:23 | 3D 拆解 CPU 架构 | 系统全景 | 36 分钟，只适合已经有兴趣的观众 |
| 4 | Branch Education · The $200M Machine that Prints Microchips (EUV) | https://www.youtube.com/watch?v=B2482h_TNwg | 239 万 | 38:31 | 3D 拆 EUV 光刻机 | 机器内部光路可视化 | 未查到评论 |
| 5 | Veritasium · The Closest Thing We Have to Alien Technology | https://www.youtube.com/watch?v=MiUHjLxm3V0 | **6614 万** | 55:00 | 讲最先进芯片的制造机器（简介：「The insane machines that make the most advanced computer chips」） | 证明「造芯片的机器」本身就是大众爆款题材，55 分钟也能拿到 6600 万 | 太长，与我们 3–5 分钟一期一个概念的定位相反 |
| 6 | Veritasium · How Does a Transistor Work? | https://www.youtube.com/watch?v=IcrBqCFLHIY | 459 万 | 6:00 | 讲者出镜 + 示意图（未逐帧核实） | 6 分钟单概念，与我们时长相当 | 早期作品，画面以 2D 示意为主（未核实） |
| 7 | The Engineering Mindset · Transistors Explained | https://www.youtube.com/watch?v=J4oO7PT_nzQ | 2029 万 | 18:20 | 2D/3D 动画讲晶体管类型与电路 | 搜索词「how transistors work」排名第一，长尾播放大 | 偏电子工程课，不讲「芯片里」的场景 |
| 8 | Real Engineering · Transistors – The Invention That Changed The World | https://www.youtube.com/watch?v=OwS9aTE2Go4 | 598 万 | 8:12 | 旁白 + 动画 + 历史（电子管到晶体管） | 用历史动机讲「为什么需要」 | 机制讲得浅（未逐帧核实） |
| 9 | Ben Eater · Making logic gates from transistors | https://www.youtube.com/watch?v=sTu3LwpF6XI | 313 万 | 13:02 | 面包板实物搭电路 | 真实器件、可复现，可信度高 | 只讲分立元件，不讲芯片尺度 |
| 10 | Asianometry · The Gate-All-Around Transistor is Coming | https://www.youtube.com/watch?v=5RPFfPtgw7g | 54 万 | 15:44 | 旁白 + 资料图，偏产业与历史 | 产业深度，适合行业观众 | 画面弱、不面向新手（据频道一贯风格，未逐条核实） |
| 11 | **MKBHD × Epic Spaceman · I shrunk down into an M5 chip** | https://www.youtube.com/watch?v=Jh9pFp1oM7E | **421 万** | 11:52 | **讲者每次缩小 100 倍**，用按键、头发、纸张、米粒、楼房作参照，直到 3 nm 晶体管（据 sozai.app 转录） | 以讲者身体作比例尺，参照物连续，最接近我们的「缩小」形式 | 转录里**几乎没讲晶体管怎么开关**；全片一人旁白，没有问答；说明了「苹果不公开架构」，所以画面是示意 |
| 12 | Epic Spaceman · I Flew Inside The Chip In My Phone | https://www.youtube.com/watch?v=QtW1lQITckE | 66 万 | 19:07 | 把芯片放大到曼哈顿大小（B 站搬运版简介是这么说的）；作者声明「NO generative AI… months using Blender」 | 「放大到城市」这个尺度类比很直观 | 作者特意声明没用生成式 AI。说明这个赛道在乎「手工可信」，我们用 AI 视频必须明确标注 |
| 13 | NISENet · Zoom Into a Microchip | https://www.youtube.com/watch?v=Fxv3JoS1uY8 | 329 万 | 3:40 | 连续放大镜头 | 4 分钟以内的纯缩放也能有 300 万+ 播放 | 没有讲解线 |

两人形式的旁证：Cleo Abram × MKBHD · Quantum Computers, explained with MKBHD（https://www.youtube.com/watch?v=e3fz3dqhN44 ，1157 万，17:01）。搜索结果显示是双人合作，但具体讲法未核实。

### 1b. B 站（公开接口，2026-11-14）

| # | UP 主 · 视频 | 链接 | 播放 | 时长 | 赞/播 | 藏/播 | 讲法与画面 | 好 / 缺 |
|---|---|---|---|---|---|---|---|---|
| 1 | **影视飓风 × 极客湾 · 芯片放大几万倍，你会看到什么？**（2024-04-11） | https://www.bilibili.com/video/BV17F4m1T7M2 | **542 万** | 16:39 | **8.27%** | 1.81% | 实验室实拍：显微镜、SEM 下挖出晶体管 | 好：**真货画面**，可信度高。极客湾置顶评论（2 万赞）主动补充「nm 是基于密度的营销数字」。缺：热评几乎都是商单和赞叹，**没有人提原理问题**，说明这片主要是「看奇观」 |
| 2 | 极客队长 · 光刻机咋就这么难？（2020-06） | https://www.bilibili.com/video/BV1uT4y1J72t | 315 万 | 11:22 | 4.37% | 1.72% | 旁白 + 资料图，附互动小游戏 | 好：ASML 官方号来评论（9588 赞）。缺：热评被「卡脖子」、产业政策话题占满 |
| 3 | 硅谷101 · 人类会被困在 1nm 吗？（2025-08） | https://www.bilibili.com/video/BV19stCzAEdc | 218 万 | 44:35 | 1.33% | 0.99% | 访谈 + 资料，讲光源、数值孔径、工艺因子 | 好：深度。缺：45 分钟，新手门槛高 |
| 4 | **谈三圈 · 我们用 18 吨的光刻机，刻 28 纳米的汉字**（2025-02-22） | https://www.bilibili.com/video/BV1SiPTeKE3T | 205 万 | 15:17 | 3.56% | 0.95% | 晶圆厂从业者**用真实工艺做一件趣事**（OPC / SMO） | 好：真实工艺 + 好玩的目标，投币率 2.07%。缺：热评是梗，没有原理问题 |
| 5 | 谈三圈 · 放大 20 万倍，3 纳米芯片最深层的秘密 | https://www.bilibili.com/video/BV1JfNqzKEyF | 98 万 | 19:37 | 5.43% | 1.99% | 实测剖面分析 | 好：「解剖报告」这种真实证据。缺：偏硬核 |
| 6 | NONO 频道 · 放大一亿倍，看芯片内部的工作原理（2022-11） | https://www.bilibili.com/video/BV1Ce4y1W71k | 206 万 | 4:04 | 2.35% | **2.82%** | **简介写明「动画作者：BranchEducation」**，配中文旁白重剪 | 好：说明 Branch 的画面压到 4 分钟配中文，照样有 200 万播放。缺：版权标为「原创」，热评只有赞叹 |
| 7 | 爱上半导体 · Mos 管的工作原理（2021-06） | https://www.bilibili.com/video/BV1344y167qm | 158 万 | 4:58 | 2.92% | **3.18%** | 2D/3D 示意，单概念 | 好：5 分钟讲一个机制，收藏率高 |
| 8 | 爱上半导体 · 芯片的几纳米说的是什么？FinFET 与 GAAFET（2024-12） | https://www.bilibili.com/video/BV1Bp6KYXEG5 | 16.8 万 | 4:40 | 4.90% | **3.77%** | 示意动画 | 好：最高赞评论（227 赞）说「看了好多版本的都没明白具体为什么导通，看了你的视频一下就懂了」，**「为什么导通」是真实的卡点** |
| 9 | 科普创世纪 · 3D 动画揭秘 CPU 内部晶体管是如何工作的（2023-07） | https://www.bilibili.com/video/BV1Wm4y1L7Kd | 13.4 万 | 3:46 | 2.83% | 2.51% | 3D 动画 | 好：热评「比课本好」「课本每一句都看懂但整体没啥概念」 |
| 10 | 微观眼 · 芯片，放大 1 万倍，知道为什么难造了吧！ | https://www.bilibili.com/video/BV1zK411Y7Me | 249 万 | 1:15 | 1.01% | **0.27%** | 显微镜奇观短片 | 缺：只有奇观，收藏率很低 |
| 11 | （形式对照，非芯片）Redknot-乔红 · 用最好的动画为你讲解——内存的原理（2025-01） | https://www.bilibili.com/video/BV1Htr8YhELV | 344 万 | 13:29 | 4.68% | **4.23%** | 3D 动画讲 DDR | 好：中文区「3D 讲原理」也能爆。热评（3436 赞）：「这还是简化太多了」。**简化要说出来** |
| 12 | YouTube 精选字幕组 · 把芯片放大 200 万倍（Epic Spaceman 搬运，2026-03） | https://www.bilibili.com/video/BV1zuQUBwEoX | 29 万 | 16:43 | 2.19% | 2.58% | 搬运 | 简介称「以往科普大多用显微镜放大……Epic Spaceman 提出全新角度」，**「放大到城市」在中文区已经有观众知道** |

异常值：花椒炒虾米「深度拆解：芯片制造全流程」（BV1sK5m6yEV4）播放 57.5 万，但点赞只有 959（0.17%），弹幕为 0。数据可疑，不作对标。

### 1c. 对标小结（只写新增的）

- **长篇深度片占头部**：Branch 27–38 分钟、Veritasium 55 分钟、硅谷 101 45 分钟。**3–5 分钟只讲一个机制、画面精良的芯片视频很少**。中文区的短片（爱上半导体、科普创世纪）收藏率 2.5–3.8%，但画面朴素、播放在 10–150 万。这个时长和质量的组合是空位。
- **两种对立的形式**：一种是「奇观」（显微镜、SEM、放大到城市），播放高、收藏低（微观眼 0.27%）；另一种是「原理」（MOS 管怎么导通），收藏高。**我们要把两者合在一个镜头里**：先看到真东西，再讲它怎么工作。
- **中文区芯片话题被「卡脖子」和产业叙事主导**（极客队长、硅谷 101 的热评）。纯讲「它怎么工作」的好画面内容少，也能避开政治争吵。
- 热评几乎从来不是问题，而是赞叹、梗（「学会了，明天开厂生产 cpu」170 赞）和产业争论。**真实问题在知乎和问答站里**，见第 3 节。

## 2. 「缩小进某物内部」与「两人问答」的先例

### 2a. 缩小 / 尺度先例

| 作品 | 手法 | 有效之处 | 被批评之处或风险 |
|---|---|---|---|
| Powers of Ten（Eames，1977） https://www.youtube.com/watch?v=0fKBhvDjuy0 （950 万）；Wikipedia https://en.wikipedia.org/wiki/Powers_of_Ten_(film) | 每 10 秒放大或缩小一个数量级，返程每 2 秒一级，一直到夸克；1998 年入选美国国家电影登记 | **固定节奏的数量级步进**，观众不会迷失尺度 | Wikipedia 没有记录批评；它只讲尺度，不讲机制 |
| The Magic School Bus · Gets Programmed（S4，1997-11-22，飞进电脑） https://tvtropes.org/pmwiki/pmwiki.php/Recap/TheMagicSchoolBusS4E11GetsProgrammed （仅搜索结果） | 全班缩小进电脑，把巴士变成软盘 | 有剧情动机（要救同学） | IMDb 的 goofs 页挑出程序逻辑错误；**没查到这部剧对纠正误解的同行评审效果研究**（Virginia Tech 2024–26 NSF 项目研究的是它的历史，不是学习效果：https://news.vt.edu/articles/2024/12/clahs-matthew-wisnioski-school-bus.html ） |
| 工作细胞（2015–21） https://en.wikipedia.org/wiki/Cells_at_Work! | 把细胞拟人化，新手红细胞常迷路，白细胞是懂行的一方 | **「迷路的新手 + 懂行的老手」正是我们的人设结构**；生物准确性受赞，西南大学附中老师 2018 年拿它布置作业 | Anime News Network（2016）认为知识呈现方式有瑕疵，也有评价说重复 |
| 人体大冒险（Once Upon a Time… Life，1987） https://en.wikipedia.org/wiki/Once_Upon_a_Time..._Life | 器官拟人 + 剧情 + 比喻 | 每集一个器官，**一集一个系统** | Wikipedia 专门有一节列「生物学不准确」，**比喻容易被当成事实** |
| MKBHD × Epic Spaceman（见 1a #11） | 讲者身体当比例尺，每步 ×100 | 参照物连续：按键、细菌、头发、DNA、楼房 | 转录里机制几乎为零：**只有尺度，没有原理** |
| Kurzgesagt https://en.wikipedia.org/wiki/Kurzgesagt | 扁平动画讲宏大尺度 | 节奏与美术 | 2019 年发片「Can You Trust Kurzgesagt Videos?」，下架两支旧片；2024 年 Workout Paradox 因「too simplified」重做。**过度简化会被公开追责，需要来源和更正机制** |

**手法结论**：
1. 用固定的数量级步进作比例尺（Powers of Ten），并给每一级配一个熟悉的参照物（Epic Spaceman）。这两点已经被验证有效。
2. 拟人和比喻有效，但会被当成事实（人体大冒险、ANN 对工作细胞的评价）。所以**每一个比喻、每一个示意画面都要标出来**。
3. 只做尺度会变成「奇观片」；只做机制会变成「课本」。

### 2b. 两人问答讲科技

- **形式先例**：工作细胞的「新手 + 老手」；Cleo Abram × MKBHD 讲量子计算机（1157 万，具体讲法未核实）。在 YouTube 和 B 站芯片题材的头部结果里，**没有找到「双人问答」的芯片视频**：Branch、Veritasium、Real Engineering、Ben Eater、Asianometry、影视飓风、谈三圈都由单人主讲；MKBHD 与 Epic Spaceman 虽然两人合作，转录里也是单人旁白。
- **常见坑**（叙事学与已有对标）：
  - **「明知故问」**（Wikipedia 叫「idiot lecture」，例句「As you well know, Professor, a prime number is…」），角色把双方都知道的事讲给观众听。https://en.wikipedia.org/wiki/Exposition_(narrative) 。对策：新手只问自己真不知道、观众也真会问的问题（来源见第 3 节）。
  - **信息倾倒**（info-dump）：Wikipedia 认为写进对白里比写进叙述更糟。对策：向导每次回答不超过 2–3 句，然后马上给画面。
  - **人设抢戏**：已有对标里，IBM 最高赞评论（1300 赞）在讨论讲者反着写字，噱头盖过了内容。对策：人物的笑点只放在转场，不放在讲机制的时候。
  - **新手被写成傻子**：这是编剧行业常识，没找到文献。对策：新手的错误猜测必须是**合理的**，最好就是常见误解（见 2c）。

### 2c. 学习科学证据：对话式讲解与提问者的作用

| 发现 | 出处 | 对我们的含义 |
|---|---|---|
| 学习者「旁听」虚拟导师与学生的对话时，如果学生连续提**深层问题**，学习者写出的相关内容明显多于只听独白的组 | Driscoll, Craig, Gholson, Ventura, Hu, Graesser (2003). *J. Educational Computing Research* 29(4), 431–450. doi:10.2190/Q8CM-FH7L-6HJU-DT9W | 新手的问题要问「为什么 / 怎么会 / 如果…会怎样」，不问「这叫什么」 |
| 深层问题效应（deep-level-reasoning-question effect）：起作用的主要是**深层问题本身**。把同样的问题嵌进独白，效果依然存在 | Craig, Sullins, Witherspoon, Gholson (2006). *Cognition and Instruction* 24(4), 565–591. doi:10.1207/s1532690xci2404_4 | **两个人物本身不是有效成分，问题才是**。人设只是承载问题的方式，不要花篇幅建人设 |
| 深层问题效应在 8–11 年级、计算机素养与牛顿物理两个领域里重现 | Gholson et al. (2009). *Instructional Science* 37(5), 487–493. doi:10.1007/s11251-008-9069-2 | 适用于非大学生观众 |
| 两人一起观看「导师辅导学生」的录像，学得和被辅导的学生一样好；独自观看的效果较差 | Chi, Roy, Hausmann (2008). *Cognitive Science* 32(2), 301–341. doi:10.1080/03640210701863396 。后续研究：Muldner, Lam, Chi，*J. Educational Psychology*（2013/14，仅见于检索结果） | 被观看的应该是「**有卡点的真实对话**」，新手的困惑要可见 |
| 物理中的「替代学习」：学生与导师就**误解**展开对话的录像，比平铺直叙的讲解更能带来概念转变 | Muller, Sharma, Eklund, Reimann (2007). *Instructional Science* 35(6), 519–533. doi:10.1007/s11251-007-9017-6 （摘要未取到，结论据作者 2008 年的相关论文与检索摘要） | 新手说出误解、向导用画面驳倒，这就是我们的核心节拍 |
| 讲解中纳入误解（「Saying the wrong thing」） | Muller, Bewes, Sharma, Reimann (2008). *J. Computer Assisted Learning* 24(2), 144–155. doi:10.1111/j.1365-2729.2007.00248.x | 已在频道总对标中（d≈0.8），这里不重复 |
| **反面证据**：有研究在真实课程中用对话视频做替代学习，没能复现效果（Ding 等，2018） | 只见于检索摘要，**未核实** | 不能保证双人形式本身有效，必须做真人前测和后测 |

## 3. 普通人对芯片最好奇或最困惑的 10 个问题（新手提问来源）

1. **指甲盖那么小，怎么放得下几百亿个晶体管？怎么做到那么小？**
   知乎「为什么在那么小的芯片上面可以蚀刻出几十亿个晶体管？」https://www.zhihu.com/question/520235377 ；ELI5（2023-09）https://www.reddit.com/r/explainlikeimfive/comments/16frd0u/ （正文未取到，只有标题）；Quora https://www.quora.com/How-do-companies-like-Intel-manufacture-chips-that-have-such-tiny-parts-How-can-they-accurately-build-something-with-billions-of-transistors
2. **一堆开关通了电，怎么就会算数了？**
   知乎「CPU 只是一堆晶体管为什么通电之后就可以运算了？」https://www.zhihu.com/question/22012073 ；知乎「CPU 是怎样工作的？」https://www.zhihu.com/question/21998860 ；Physics Forums「How does a computer tell a 0 from a 1?」https://www.physicsforums.com/threads/how-does-a-computer-tell-a-0-from-a-1.149537/
3. **「3 纳米」到底是哪里 3 纳米？**
   B 站「如何评价网传 ASML『掀老底』称 3nm 芯片实际为 23nm」（13 万播放）https://www.bilibili.com/video/BV1dx4y1b7VP ；爱范儿「22nm、14nm、10nm 究竟是什么意思？」https://www.ifanr.com/805064 ；影视飓风片下极客湾置顶评论（2 万赞）也主动解释了这一点
4. **晶体管没有能动的零件，凭什么能「开」和「关」？为什么会导通？**
   知乎「CPU 内部的晶体管有什么作用？」https://www.zhihu.com/question/600089341 ；B 站爱上半导体片下最高赞评论（227 赞）：「看了好多版本的都没明白具体为什么导通」https://www.bilibili.com/video/BV1Bp6KYXEG5
5. **芯片和光刻机为什么这么难造？**
   知乎「光刻机的制作难度有多大？」https://www.zhihu.com/question/463522477 ；极客队长（315 万播放）https://www.bilibili.com/video/BV1uT4y1J72t ，热评（1320 赞）补充「EDA、封测、光刻胶更难」
6. **几百亿个晶体管，坏一个还能用吗？**
   知乎「CPU 中有上亿个晶体管，坏了一个还能工作吗？」https://www.zhihu.com/question/549140878
7. **做不小，那为什么不把芯片做大一点？**
   知乎 https://www.zhihu.com/question/8992463775 ；https://www.zhihu.com/question/12797220523 ；「芯片为何不能做得无限大？」https://www.zhihu.com/question/448036005
8. **为什么芯片越小越好？晶体管当初是怎么越做越小的？**
   知乎「为什么芯片越小越好?」https://www.zhihu.com/question/378211697 ；Quora「How did transistors get so small?」https://www.quora.com/How-did-transistors-get-so-small
9. **还能缩小多少？1 纳米是尽头吗？**
   Quora「What is the theoretical limit of chip technology?」https://www.quora.com/What-is-the-theoretical-limit-of-chip-technology ；硅谷 101「人类会被困在 1nm 吗？」（218 万播放）https://www.bilibili.com/video/BV19stCzAEdc
10. **几百亿个零件是怎么设计出来的，不会画错吗？**
    Quora「…7.2 billion transistors. How is something with that many parts designed or manufactured?」https://www.quora.com/The-Intel-Broadwell-EP-Xeon-is-a-processor-with-over-7-2-billion-transistors-How-is-something-with-that-many-parts-designed-or-manufactured

**未查到可靠提问出处**：「为什么用硅」（搜索结果几乎不讨论）；英文 YouTube 高赞评论里的提问（评论被拦截）。附带一个可当彩蛋的问题：「Minecraft 红石能造电脑吗？」（Redknot 片下的回复）。

## 4. 我们独有的角度：已做过的和空位

| 要素 | 已经有人做过 | 空位 |
|---|---|---|
| 缩小进芯片 | **做得很多**：MKBHD × Epic Spaceman（421 万）、Epic Spaceman（66 万）、NISENet（329 万）、影视飓风 SEM 实拍（542 万）、微观眼、NONO 转制 Branch 动画（206 万） | 「缩小」本身不新。新的是**缩小之后讲清机制**：Epic Spaceman 那支几乎没讲开关原理 |
| 比例尺贯穿 | Powers of Ten 的数量级步进；Epic Spaceman 用身体加参照物 | 没见到**全系列共用的一条比例尺**（每期从同一个起点缩下去、角标常驻、回程倒放）。另外，比例尺在讲机制的镜头里也一直保留，这在对标里没见过 |
| 双人问答 | 工作细胞（生物）、Cleo × MKBHD（量子）；芯片头部视频**全是单人主讲** | **芯片题材的双人问答是空位**。学习科学给的边界：起作用的是深层问题和误解对话，不是两个人本身（Craig 2006；Muller 2007） |
| 诚实标注示意 | 零散做过：MKBHD 说「苹果不公开架构」；极客湾置顶「nm 是营销数字」；Epic Spaceman 声明「NO generative AI」；Kurzgesagt 有公开更正 | **没见到系统化的画面标注**（角标「实拍 / 实测」「3D 示意·比例准确」「AI 氛围·非结构」）。这对我们是必需的：我们用 AI 视频，而这个赛道的创作者会专门声明「没用 AI」，中文观众也反感没标注的 AI 内容（见频道总对标） |
| 3–5 分钟单概念 + 精良 3D | 中文短片（爱上半导体、科普创世纪）收藏率高但画面朴素；Branch 画面精良但 30 分钟左右 | **「Branch 级的画面、5 分钟、一个机制」中英都空**。NONO 把 Branch 动画压到 4 分钟拿到 206 万，说明有需求 |
| 真实证据锚点 | 影视飓风 SEM、谈三圈剖面图 | 我们可以每期放一帧**真实显微照片**（需授权或公开许可），和 3D 模型同框对照：「这是真的，这是我们的模型」 |

**一句话定位**：别人做「缩小看奇观」或「长篇讲原理」，我们做「缩小到那里，由新手问出那个真问题，5 分钟讲透一个机制，画面告诉你哪里是真的」。

## 5. 系列知识点地图（建议 9 期，后 3 期与晶圆厂参观衔接）

| 期 | 标题（中 / 英） | 核心问题 | 核心画面 |
|---|---|---|---|
| t01 | 芯片里面到底有什么？/ What's actually inside a chip? | 那块黑色的东西里面是什么，「几百亿个开关」在哪？ | 从手机缩小，穿过封装，经过十几层铜导线的「立交桥城市」，落到最底层的晶体管阵列 |
| t02 | 没有零件会动的开关 / A switch with no moving parts | 晶体管凭什么开和关、为什么会导通？（问题 4） | 栅极加电压，沟道里的电子聚成一座「桥」，比例尺停在约 10 nm 量级 |
| t03 | 开关怎么学会算数 / How switches learn to add | 一堆开关怎么就会算 1+1？（问题 2） | 两个晶体管组成反相器，再组成与非门，最后组成半加器，灯亮了 |
| t04 | 「3 纳米」不是 3 纳米 / "3 nm" isn't 3 nm | 3 纳米到底量的是哪里？（问题 3） | 在 3D 模型上量真实间距，和标签数字对照；FinFET 过渡到 GAA |
| t05 | 为什么越小越好 / Why smaller is better | 做小有什么好处，为什么不把芯片做大？（问题 7、8） | 同一块晶圆上切大芯片和切小芯片，缺陷点随机撒落，对比良率 |
| t06 | 坏一个会怎样 / What if one transistor breaks? | 坏了还能用吗？（问题 6） | 测试探针在晶圆上逐颗打点；同一种芯片按好坏分成不同档位 |
| t07 | 用光印电路 / Printing circuits with light | 怎么在硅上「画」出几百亿个图形？（问题 1） | 光穿过掩模，在光刻胶上成像；波长与线宽并排比较。**这期开始进晶圆厂** |
| t08 | 一层一层盖楼 / Building a chip floor by floor | 十几层导线是怎么叠上去的？ | 沉积、刻蚀、抛光循环，楼层逐层升高 |
| t09 | 为什么比手术室干净一万倍 / Cleaner than an operating room | 一粒灰为什么能毁掉芯片？ | 一粒灰尘和晶体管放在同一个比例尺上；洁净室气流 |

可选第 10 期：缩小的尽头（问题 9，量子隧穿与 1 nm），作为季终。

## 6. t01 建议结构（约 4:30，7 拍）

人物代号：**小新**（好奇的新手）与**向导**。比例尺角标全程常驻，显示当前视野宽度和一个参照物图标。所有数字由事实核查角色另行核实，这里只给结构。

| 拍 | 时间 | 这一拍回答的问题 | 人物在哪 / 画面 | 标注 |
|---|---|---|---|---|
| 1 冷开场 | 0:00–0:20 | 「这么小一片，怎么放得下几百亿个东西？」（问题 1） | 桌面上的真实尺度，小新捏着拆开的手机芯片；向导说「那我们进去看」 | AI 氛围镜头，角标「AI 画面 · 非结构」 |
| 2 定义卡 | 0:20–0:45 | 芯片是什么？一句话：「一块硅上做出来、用导线连起来的很多很多开关」 | 两人开始缩小，比例尺从 1 cm 跳到 1 mm | 定义卡（中英） |
| 3 误解 1：黑壳不是芯片 | 0:45–1:25 | 「黑色那块就是芯片吗？」不是，那是封装，真正的硅片藏在里面 | 两人站在封装基板上，看到锡球和硅片；插一帧**真实硅片照片** | 「实拍」与「3D 示意 · 比例准确」并排 |
| 4 导线城市 | 1:25–2:25 | 「这些像立交桥的是什么？就是晶体管吗？」（误解 2）不是，这是十几层铜导线，越往下越细 | 两人像坐电梯一样逐层下降，比例尺 10 µm → 100 nm，参照物从头发到细菌到病毒 | 「示意：层数与颜色经过简化」 |
| 5 到底了 | 2:25–3:10 | 「开关在哪？怎么一个能动的零件都没有？」向导只指出位置，说明它们没有零件会动，原理留到下一期 | 两人站在晶体管阵列之间，晶体管和人差不多高 | 「3D 示意」 |
| 6 先猜一下 + 拉回尺度 | 3:10–3:50 | 「你猜，从指甲盖到这里缩小了多少倍？」随后倒放回程，比例尺快速回到 1 cm | 小新先猜，向导揭晓，回程镜头连续 | 数字有出处 |
| 7 一句话记住 + 下一期 | 3:50–4:30 | 「芯片 = 底层几百亿个开关 + 上面十几层导线」；下一期：没有零件会动的开关，凭什么开关？ | 回到桌面；片尾卡列出本期哪些画面是实拍、哪些是示意、哪些是 AI | 截图卡（中文版）；来源写在简介 |

人物使用规则（依据第 2 节）：
- 小新每个问题都必须来自第 3 节的真实问题，或者是常见误解。
- 向导每次回答不超过 3 句，然后交给画面。
- 讲机制时人物退到画面边上，不做动作。
- 笑点只放在两次缩小之间的转场。
