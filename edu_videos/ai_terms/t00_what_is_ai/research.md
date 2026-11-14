# t00 什么是 AI — 调研与出处

讲稿 v1「⑤ 现实」段（s6，l32–l36）的案例与屏幕上的数字都来自下列原文。2026-11-08 逐条打开原始出处核对（论文、官方页面、原始新闻报道）；Reuters 官网对抓取返回 401，两篇 Reuters 报道读的是 Internet Archive 保存的原页面（快照地址附在各条下）。

## 用到的三个案例

### 1. AlphaFold：从已知结构里学会预测蛋白质形状（2024 诺贝尔化学奖）
- 出处：
  - 诺奖新闻稿（2024 年 10 月 9 日）：https://www.nobelprize.org/prizes/chemistry/2024/press-release/
  - 诺奖科普介绍：https://www.nobelprize.org/prizes/chemistry/2024/popular-information/
  - 原论文：Jumper J, Evans R, Pritzel A, et al., Hassabis D. "Highly accurate protein structure prediction with AlphaFold." *Nature* 596(7873):583–589, 2021（2021-07-15 在线）。https://doi.org/10.1038/s41586-021-03819-2 （开放全文 PMC8371605）
  - 数据库：EMBL-EBI AlphaFold Protein Structure Database，https://alphafold.ebi.ac.uk/ ；2022 年扩容公告 https://ebi-biows.gitdocs.ebi.ac.uk/blog/2022-07-28-new-afdb-release ；EMBL 2026-09-24 新闻 https://www.embl.org/news/science-technology/alphafold-database-adds-viral-protein-complexes-to-support-pandemic-preparedness/
- 核对：
  - 得主与获奖理由（新闻稿原文）：一半授予 David Baker（University of Washington / HHMI）"for computational protein design"；另一半由 Demis Hassabis 与 John Jumper（均为 Google DeepMind, London）共享 "for protein structure prediction"。新闻稿还说：他们 "developed an AI model to solve a 50-year-old problem: predicting proteins' complex structures"；"In 2020, Demis Hassabis and John Jumper presented an AI model called AlphaFold2"；"they have been able to predict the structure of virtually all the 200 million proteins that researchers have identified"；"AlphaFold2 has been used by more than two million people from 190 countries"。
  - 以前测一个结构要多久（两处可靠原文，可任选）：
    - 诺奖科普介绍小标题 "Work that once took years now takes just a few minutes"，正文 "Previously, it often took years to obtain a protein structure, if at all. Now it can be done in a few minutes."（以前得到一个蛋白质结构常常要花好几年，有时根本测不出来；现在几分钟就能算出来。）
    - Jumper 等 2021 摘要："Structural coverage is bottlenecked by the months to years of painstaking effort required to determine a single protein structure."（测定单个蛋白质结构要花几个月到几年的艰苦工作。）同一摘要："the structures of around 100,000 unique proteins have been determined … a small fraction of the billions of known protein sequences"。
  - 「从已知的结构里学」：诺奖科普介绍原文 "The team trained AlphaFold2 on the vast information in the databases of all known protein structures and amino acid sequences"；同文说科学家此前主要靠 X 射线晶体学测出约 20 万种蛋白质的结构（"around 200,000 different proteins"）。
  - 数据库数量：
    - 2022-07-28 扩容后为 214,684,311 个预测结构（EMBL-EBI 公告原文 "a whopping 214,684,311 structures"），之后单链蛋白预测基本没变，EMBL-EBI 关于页至今写 "over 200 million protein structure predictions"。
    - 截至 2026-09-24，EMBL 新闻稿写 "the database has grown to more than 260 million protein and protein complex predictions"——这个 2.6 亿**包含蛋白质复合物**预测；数据库首页标题也已改成 "over 260 million"，但同页 Background 仍写 "The latest database release contains over 200 million entries"。
- 措辞注意：
  - 「超过 2 亿」准确（单个蛋白质的预测，2022 年 7 月起即约 2.14 亿）；若想用更新的 2.6 亿，必须写明「含复合物，截至 2026 年 9 月」。都是**预测**结构，不是实验测出的结构；据 EMBL-EBI，其中约 35% 高精度（"as good as experimentally determined structures"）、另约 45% "accurate enough for many applications"（转引自 Callaway E, *Nature* 新闻 2022，https://doi.org/10.1038/d41586-022-02083-2 ；EMBL-EBI 原新闻稿未单独打开），不要说「解出了所有蛋白质」。
  - 讲稿 l33「它的两位作者」不准确：Jumper 等 2021 论文有三十多位作者，诺奖只授予其中两人（Hassabis、Jumper），且只占当年化学奖的一半（另一半给 Baker 的蛋白质设计）。建议改为「带领研发它的两个人」或「它的两位主要研发者」。
  - 获奖的是 AlphaFold2（2020 年 CASP14 亮相，2021 年论文）；「预测得和实验差不多准」只能说「多数情况下」（论文原话 "competitive with experimental structures in a majority of cases"）。
  - 「过去要靠实验一点一点测」与原文一致；若上屏数字，用「几个月到几年」（论文）或「常常要好几年」（诺奖），不要说「几十年」。「几分钟」是诺奖科普的说法。
  - 「200 多万人、190 个国家」是诺奖材料给出的使用人数（截至 2024 年 10 月），没有说明统计口径；要用就写「据诺贝尔奖官方介绍」。

### 2. ChatGPT 用户增长（估计值）
- 出处：Krystal Hu. "ChatGPT sets record for fastest-growing user base - analyst note." Reuters，电头 2023-02-01（页面 datePublished 2023-02-02）。https://www.reuters.com/technology/chatgpt-sets-record-fastest-growing-user-base-analyst-note-2023-02-01/ （读的是 Internet Archive 快照 http://web.archive.org/web/20230203002327/https://www.reuters.com/technology/chatgpt-sets-record-fastest-growing-user-base-analyst-note-2023-02-01/ ）。上线日期：OpenAI "Introducing ChatGPT"，2022-11-30，https://openai.com/index/chatgpt/
- 核对（报道原文）：
  - 首段："ChatGPT … is **estimated** to have reached 100 million monthly active users in January, just two months after launch, making it the fastest-growing consumer application in history, according to a UBS study on Wednesday."
  - "The report, citing data from analytics firm Similarweb, said an average of about 13 million unique visitors had used ChatGPT per day in January, more than double the levels of December."
  - UBS 原话："In 20 years following the internet space, we cannot recall a faster ramp in a consumer internet app."
  - 对比：TikTok 约 9 个月、Instagram 2 年半到 1 亿用户（报道注明数据来自 Sensor Tower）。
- 官方最新周活（OpenAI 自己公布）：
  - 2026-02-27 "Scaling AI for everyone"（https://openai.com/index/scaling-ai-for-everyone/）："more than 900M weekly active users"，"more than 50 million consumer subscribers"。
  - 2026-08-31 "A milestone in expanding access to AI"（https://openai.com/index/expanding-access-to-ai-with-chatgpt-ads/）："helps keep ChatGPT available to more than 1 billion weekly active users"。——**目前可用的最新、措辞最明确的官方数字：超过 10 亿周活（2026 年 8 月 31 日）**。
  - 2026-09-29 "DevDay 2026 Recap"（https://openai.com/index/devday-2026-recap/）写 "our collective 1.2B weekly users"；"collective" 口径不明（可能合计多个产品），不建议上屏。
- 措辞注意：
  - 「一亿」是 UBS 根据 Similarweb 网站流量数据做的**估计**，不是 OpenAI 公布的数；讲稿 l34「估计就过了一亿」已带「估计」，保留。原文是「月活跃用户」（monthly active users），不是注册用户。
  - 「史上增长最快的消费应用」是 UBS 分析师的判断，不是公认的统计结论；若用这句要标「据瑞银分析师」。
  - 「两个月」原文是 "just two months after launch"（2022-11-30 上线，统计月份为 2023 年 1 月），说「大约两个月」合适。
  - 周活 9 亿 / 10 亿是**公司自述**，口径（周活跃用户）与 2023 年的「月活估计」不同，不能直接放在一条增长曲线上比。

### 3. Amazon 招聘 AI 学会了偏见
- 出处：Jeffrey Dastin. "Amazon scraps secret AI recruiting tool that showed bias against women." Reuters，2018-10-10，San Francisco。https://www.reuters.com/article/us-amazon-com-jobs-automation-insight-idUSKCN1MK08G （读的是 Internet Archive 2018-10-15 快照 http://web.archive.org/web/20181015230815/https://www.reuters.com/article/us-amazon-com-jobs-automation-insight/amazon-scraps-secret-ai-recruiting-tool-that-showed-bias-against-women-idUSKCN1MK08G ）
- 核对（报道原文）：
  - 时间线：团队 2014 年起开发简历筛选程序；"by 2015, the company realized its new system was not rating candidates for software developer jobs and other technical posts in a gender-neutral way"；"ultimately disbanded the team by the start of last year"（即 2017 年初）。工具给候选人打 1 到 5 星。
  - 训练数据与原因："Amazon's computer models were trained to vet applicants by observing patterns in resumes submitted to the company over a **10-year period**. Most came from men, a reflection of male dominance across the tech industry."
  - 怎么偏："In effect, Amazon's system taught itself that male candidates were preferable. It penalized resumes that included the word "women's," as in "women's chess club captain." And it downgraded graduates of two all-women's colleges"；另说它偏好男性工程师简历里更常见的动词，如 "executed"、"captured"（一人所说）。
  - 修补无效："Amazon edited the programs to make them neutral to these particular terms. But that was no guarantee that the machines would not devise other ways of sorting candidates that could prove discriminatory"。
  - 是否用过：知情人称 "Amazon's recruiters looked at the recommendations generated by the tool when searching for new hires, but never relied solely on those rankings"。Amazon 的回应：拒绝评论技术问题，但称该工具 "was never used by Amazon recruiters to evaluate candidates"，且 "did not dispute that recruiters looked at the recommendations"。
  - 其他：报道称数据问题还导致不合格者常被推荐、结果 "almost at random"，于是项目被关停；后来保留了一个 "much-watered down version" 做去重等杂务。
- 措辞注意：
  - 来源是 Reuters 援引**五位匿名知情人**，不是 Amazon 公开承认的事故；Amazon 否认用它评估过候选人。所以只说「曾想用」「后来放弃了」，不说「用它淘汰了很多女性」。
  - 讲稿 l35「给写着『女子』字样的简历扣分」：原文是英文词 "women's"（如「女子国际象棋社社长」），建议画面上保留英文 women's，口播可说「带 women's（女子的）这个词」。
  - 「过去十年的简历」原文 "over a 10-year period"，可用；「大多来自男性」原文 "Most came from men"，可用。
  - 放弃原因不只偏见：报道写高管对项目失去信心，且推荐结果近乎随机。讲稿「这个工具后来被放弃了」没说原因，可以；不要说「因为偏见被叫停」。

## 备选（这一期没用）
- **1959 年 Arthur Samuel 的跳棋程序（「machine learning」一词）**
  - 出处：Samuel AL. "Some Studies in Machine Learning Using the Game of Checkers." *IBM Journal of Research and Development* 3(3):210–229, 1959 年 7 月。https://doi.org/10.1147/rd.33.0210 （Crossref 元数据核对；全文读的是 MIT 存的重印本 https://people.csail.mit.edu/brooks/idocs/Samuel.pdf ，注明 "Originally published in IBM Journal, Vol. 3, No. 3, July, 1959"。弗吉尼亚大学那份 https://www.cs.virginia.edu/evans/greatworks/samuel.pdf 是 1967 年的续篇 "II—Recent Progress"，不是 1959 原文，别引错。）
  - 核对（原文摘要与引言）："Enough work has been done to verify the fact that a computer can be programmed so that it will learn to play a better game of checkers than can be played by the person who wrote the program."；只用了 "8 or 10 hours of machine-playing time"，而且只给了 "the rules of the game, a sense of direction, and a redundant and incomplete list of parameters … whose correct signs and relative weights are unknown and unspecified"。引言："Programming computers to learn from experience should eventually eliminate the need for much of this detailed programming effort."——正好对应「不是人写规则，而是从经验里学」。
  - 常见误引：「Field of study that gives computers the ability to learn without being explicitly programmed」**不在 1959 论文里**（全文检索 "explicit" 无结果）。这是后人的概括，常被标成「Samuel, 1959」；不能当 Samuel 原话上屏。要引就用上面摘要那句。
  - 「machine learning 一词由他创造」：论文标题与摘要确实用了 machine learning，通常被视为该词最早的印刷出处之一；但引言里他自己写 "For some years the writer has devoted his spare time to the subject of machine learning"，我们也没有检索 1959 年前的文献，所以只说「1959 年的论文标题里就用了『机器学习』这个词」，不说「他发明了这个词」。
  - 其他注意：程序当时还下不过顶尖棋手（1967 续篇脚注：1965 年世界冠军 W. F. Hellman 与程序对弈，通信赛四盘全胜，只有一盘仓促的面对面对局被下成和棋；续篇摘要也写 "While still unable to outplay checker masters"）；不要说「打败了人类冠军」。

## 不用
- **AlphaFold 数据库「2.6 亿」**：最新，但含复合物，且首页同时还写着 "over 200 million entries"，容易被质疑口径；本期用「超过 2 亿」。
- **ChatGPT「12 亿周活」**：OpenAI DevDay 2026 回顾页的 "collective 1.2B weekly users" 口径不明，不用；需要最新数字就用「超过 10 亿周活（OpenAI，2026-08-31）」。
- **Samuel「without being explicitly programmed」定义**：原论文里没有，见上。

## 数据集许可（本期实验用的手写数字）
- 数据集：Optical Recognition of Handwritten Digits，作者 E. Alpaydin、C. Kaynak（Bogazici University，伊斯坦布尔），1998 年 6 月 30 日捐赠给 UCI。https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits ，DOI https://doi.org/10.24432/C50P49
- 许可（UCI 页面原文）："This dataset is licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) license. This allows for the sharing and adaptation of the datasets for any purpose, provided that the appropriate credit is given." —— 可商用（含有广告收益的 YouTube 视频），可改编（我们画成方格、归一化都算改编），条件是署名。CC BY 4.0 的署名要求：注明作者与出处、许可名称（最好附链接），并说明是否做过修改。原始 1998 年的 `optdigits.names` 里没有许可条款，CC BY 4.0 是 UCI 现行页面给的；以 UCI 页面为准。
- 样本数：UCI 原数据共 5620 个，分训练集 `optdigits.tra` 3823 个、测试集 `optdigits.tes` 1797 个（下载原始压缩包核对）；共 43 人书写，30 人进训练集、另外 13 人进测试集。scikit-learn 文档写明 `load_digits` "is a copy of the test set of the UCI ML hand-written digits datasets"：1797 张、8×8、每格 0–16 的整数（32×32 位图按 4×4 不重叠小块数黑点得到）。本机核对：scikit-learn 1.9.1 自带的 `digits.csv.gz` 与 UCI `optdigits.tes` 逐值完全相同（1797×65）。
- scikit-learn 文档：https://scikit-learn.org/stable/datasets/toy_dataset.html （scikit-learn 代码本身是 BSD-3 许可，与数据许可分开；数据的署名对象是 Alpaydin & Kaynak / UCI）。
- 推荐屏幕署名（单行，片中出数据时用）：
  - 中：`数据：UCI 手写数字（Alpaydin & Kaynak，1998），CC BY 4.0 · 经 scikit-learn 加载，已改画`
  - 英：`Data: Optical Recognition of Handwritten Digits, Alpaydin & Kaynak (1998), UCI ML Repository, CC BY 4.0 · via scikit-learn, adapted`
  - 视频简介（完整版）：`Alpaydin, E. & Kaynak, C. (1998). Optical Recognition of Handwritten Digits [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C50P49 — licensed CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/); 8×8 test-set version loaded via scikit-learn load_digits; rendered and rescaled for this video.`
  - 现有 `scenes/t00.py` 的 `SRC_DIGITS` 只写了「数据：UCI 手写数字（Alpaydin & Kaynak，1998）· scikit-learn digits」，缺许可名与「已修改」说明；建议补上 CC BY 4.0，并在简介放完整引用与许可链接。
