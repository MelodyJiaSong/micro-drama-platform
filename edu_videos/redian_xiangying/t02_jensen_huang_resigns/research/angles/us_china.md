# 角度：us_china（中美科技竞争背景）

- **检索日期**：2026-11-14（片中一律写「截至 2026-11-14」）
- **任务**：为用户角度的后半句「大背景是中美科技竞争」补材料：美国出口管制怎样演变、英伟达在华业务有多大、中国怎样反制、DeepSeek 等中国 AI 进展的影响、黄仁勋在两国之间公开说过什么。
- **检索范围**：英伟达 FY2026 10-K（SEC，一手，分段读取）；环球网（环球时报报道）；NPR；Reuters（经 Korea Times、Open、Business Standard、TechRepublic 转述）；The Register；Fox Business（转述 FT）；DatacenterDynamics、TechCrunch（转述 FT）；Jurist、Digital Policy Alert（转述 SAMR 公告）；Fortune、Bloomberg（DeepSeek V4）。
- **检索词（简列）**：Nvidia China revenue FY2026 10-K；H200 China shipments 2026 Beijing approval；SAMR Nvidia Mellanox；CAC H20 backdoor；RTX Pro 6000D；DeepSeek 2026 Huawei Ascend；Huang export controls failure Computex；China is going to win the AI race；Super Micro indictment。
- **限制**：10-K 的「按地区收入」表在 WebFetch 的分段里没读到，中国收入金额只有二手数字（标「有争议」）。SAMR 反垄断调查 2025-09 之后的进展没查到。中国商务部、海关、网信办关于 H200 的官方文件没有直接检索到，相关条目都是 FT / Reuters 的匿名信源报道。

---

## 1. 美国出口管制演变（与本事件有关的部分）

| 时间 | 发生了什么 | 出处 | 性质 |
|---|---|---|---|
| 2022–2024（拜登政府） | 多轮先进芯片对华出口限制；英伟达为中国做降规版（A800/H800，后为 H20） | 10-K：「Over the past three years, we have been subject to a series of shifting and expanding export control restrictions.」 | 已证实（10-K 原话） |
| 2024 前后 | 美国商务部开始调查新加坡 Megaspeed（英伟达客户）是否转运 | NYT（转述，见 timeline.md）；RedState、Axios 亦称调查始于 2024 年拜登任内 | 报道称 |
| 2025-04 | H20 被要求出口许可，等于禁售；英伟达在 FY2026 第一季度计提 45 亿美元 | 10-K：「we incurred a $4.5 billion charge in the first quarter of fiscal year 2026 associated with H20」 | 已证实 |
| 2025-07-15 / 2025-08 | 美方恢复 H20 许可；美国政府官员表示期望拿到「15% or more」的收入，但没有成文规定 | 10-K：「In August 2025, the USG granted licenses that would allow us to ship certain H20 products to certain China-based customers.」「USG officials expressed an expectation that the USG will receive 15% or more of the revenue」「the USG did not publish a regulation codifying such requirement」 | 已证实 |
| FY2026 全年 | 按这些许可实际只卖出约 6,000 万美元 H20 | 10-K：「We generated approximately $60 million in H20 revenue under those licenses.」 | 已证实 |
| 2025-12-08 | 特朗普宣布允许向「approved customers」卖 H200 | 环球网 https://world.huanqiu.com/article/4PT6kkiRAKT | 已证实 |
| 10-K 的写法 | 25% 是 H200 **进口进美国时的关税**，不是分成；截至 10-K，H200 计划下没有任何收入 | 10-K：「any H200 shipped under the new licensing program will be subject to a 25% tariff upon importation into the United States」「To date, we have not generated any revenue under the H200 licensing program」 | 已证实。**与媒体常说的「美国抽成 25%」不同**，片中按 10-K 讲 |
| 10-K 对处境的总结 | 截至 FY2026 末，英伟达在中国数据中心市场「实际上被排除」 | 「As of the end of fiscal year 2026, we were effectively foreclosed from competing in China's data center computing/compute market」 | 已证实 |
| 2026-03-19 | 纽约联邦检察官起诉 Super Micro 联合创始人等三人，指控约 25 亿美元 AI 服务器转运中国（其中约 5.1 亿美元含 B200、H200 的服务器在 2025-04 至 05 间运出）；Super Micro 本身不是被告 | eWeek https://www.eweek.com/news/nvidia-ai-server-smuggling-china-2-5b-scheme/ 等（二手） | 指控未证实（起诉阶段） |
| 2026-05 | Reuters：美方已向约 10 家中国公司（阿里、腾讯、字节、京东等）发 H200 许可，但一颗都还没交付 | TechRepublic 转述 https://www.techrepublic.com/article/news-nvidia-h200-ai-chip-sales-china-stalled/ | 报道称 |
| 2026-11-11 | Axios：特朗普今年第三次批准打击转运公司，商务部长 Lutnick 拖延（匿名信源，商务部部分否认） | 见 politics.md §3 | 报道称 |
| 2026-11 | 国会推动在年底 NDAA 中加入出口管制条款；Jeffries「strongly supports」（转述） | AFP 经 EWN；检索摘要 | 报道称 |

## 2. 英伟达在华业务与收入占比

| 口径 | 数字 | 出处 | 性质 |
|---|---|---|---|
| FY2025（截至 2025-01），旧口径（账单地址） | 中国（含香港）171.08 亿美元 / 总收入 1,304.97 亿，约 13% | FY2025 10-K（检索摘要引用） | 已证实（旧口径；原表本次未重读） |
| FY2026（截至 2026-01），新口径（直接客户总部所在地） | 中国（含香港）约 197 亿美元 / 总收入 2,159.38 亿，约 9% | FourWeekMBA（二手分析，原文 403）；总收入来自 10-K | **有争议**：中国金额未在 10-K 原表核到 |
| 新口径说明 | 「Revenue by geographic region is designated based on the location of the headquarters of direct customers.」「The end customer and shipping location may be different from our customers' headquarters location.」 | 10-K（一手） | 已证实 |
| FY2026 美国以外客户占比 | 31%（FY2025 为 41%） | 10-K：「we generated 31% of our revenue in fiscal year 2026 from sales outside the United States」 | 已证实 |
| 「曾经占 13%」的说法 | Reuters 称中国「once accounted for 13% of its total revenue」 | Outlook Business 转述 Reuters https://www.outlookbusiness.com/corporate/china-tears-down-its-wall-on-nvidias-h200-ai-chips-after-months-of-resistance | 报道称 |
| 市场份额 | 黄仁勋 2025-05：英伟达在中国份额从四年前约 95% 降到约 50% | Axios 2025-05-21 https://www.axios.com/2025/05/21/nvidia-s-china-struggle-closer | 已证实（他的说法） |
| 2026-08 | FT：字节、腾讯近几周各收到约 1 万颗 H200；仍需国家发改委另行批准 | Business Standard 转述 https://business-standard.com/world-news/china-allows-limited-nvidia-h200-shipments-why-is-beijing-easing-curbs-126081900438_1.html | 报道称 |
| 2026-11-05 | Reuters：约 60 万颗 H200 滞留香港，北京未批准大规模进入内地；10 月字节、阿里、腾讯订购逾 300 万张较低端显卡，英伟达告诉客户 2027 年初交付 | Open 杂志转述 https://openthemagazine.com/world/explained-trump-backs-jensen-huang-why-are-nvidias-chips-stuck-in-hong-kong | 报道称 |

**我们的判断**：按英伟达自己的 10-K，到 2026 年初，它在中国数据中心市场「实际上被排除」，H200 许可开出后近一年也只有零星交付。也就是说，**丑闻爆发时，中国业务对英伟达已经不是收入大头，而是「未来的期权」和政治筹码**。这一点削弱「为了中国市场才把他拿下」之类的利益推断，因为中国收入的大部分已经先没了。

## 3. 中国的反制（与英伟达直接相关的）

| 时间 | 动作 | 原话 / 要点 | 出处 | 性质 |
|---|---|---|---|---|
| 2025-07-31 | 国家网信办约谈英伟达，要求说明 H20 是否有「后门」 | 关注「mature tracking and location and remote shutdown technologies」（英文转述） | The Register https://www.theregister.com/2025/07/31/beijing_nvidia_backdoors/ | 已证实（约谈事实）；英文为转译 |
| 2025-08 下旬 | 网信办等劝阻企业购买 H20（转述） | — | TechCrunch https://techcrunch.com/2025/09/17/china-tells-its-tech-companies-they-cant-buy-ai-chips-from-nivida | 报道称 |
| 2025-09-15 | 市场监管总局初步认定英伟达违反收购迈络思（Mellanox）的附加限制性条件，将进一步调查 | 英伟达：「We comply with the law in all respects」 | Jurist https://www.jurist.org/news/2025/09/china-finds-nvidia-violated-antimonopoly-law-in-preliminary-probe/ | 已证实（初步认定）；**此后结果未查到** |
| 2025-09-17 | FT：网信办要求字节、阿里等停止测试并取消 RTX Pro 6000D 订单 | — | DatacenterDynamics 转述 FT https://www.datacenterdynamics.com/en/news/chinas-internet-regulator-tells-chinese-tech-companies-to-stop-buying-nvidia-ai-chips-report/ | 报道称（匿名，无官方文件） |
| 10-K 的概括 | 中国政府「has encouraged customers to purchase from our China-based competitors」，并「discouraged customers from purchasing, importing, or using our data center products」 | 10-K（一手） | 已证实（英伟达自述） |
| 2026 年 | 北京先挡后放 H200：2026-05 未交付，2026-08 少量放行，2026-11 约 60 万颗滞留香港 | 见 §2 | 报道称 |
| 2025-07-15 | 外交部林剑：「中方反对将科技和经贸问题政治化、工具化、武器化」 | 环球网 https://world.huanqiu.com/article/4NVgbHwiLSI | 已证实（经环球网） |
| 2026-11-12 | 外交部毛宁：「美方应当停止编造所谓的"间谍叙事"，为实施科技封锁寻找借口。」 | 外交部实录（见 timeline.md） | 已证实 |

## 4. DeepSeek 等中国 AI 进展对这场竞争的影响

- **2025-01 DeepSeek 冲击**：英伟达单日市值大跌（档案其他角度未展开；本次未重查具体数字，片中如用需另核）。
- **众院对华特设委员会**以 DeepSeek 为例质疑英伟达对华销售：委员会致商务部的信「letter-to-doc-nvidia-deepseek-pla-use」（PDF） https://chinaselectcommittee.house.gov/sites/evo-subsites/selectcommitteeontheccp.house.gov/files/evo-media-document/letter-to-doc-nvidia-deepseek-pla-use_final.pdf （本次只见标题，未读正文）；Moolenaar 2025-12 关于 H200 的信也引了英伟达与 DeepSeek 的经历来说明军民融合下难分商业与军事客户（Reuters 转述）。
- **2026-04-24 DeepSeek V4 预览版**：针对华为昇腾芯片适配；华为称 V4-Flash 部分训练用了其芯片、V4 可在昇腾 950 超节点集群上运行；DeepSeek 没有披露训练用了哪些处理器；字节、腾讯、阿里随后向华为询单（Fortune https://fortune.com/2026/04/24/deepseek-v4-ai-model-price-performance-china-open-source/ ；BNN Bloomberg https://www.bnnbloomberg.ca/business/artificial-intelligence/2026/04/24/deepseek-previews-new-ai-model-adapted-to-run-on-huawei-chips/ ）。「V4-Pro 全部在昇腾上训练」只见于低质量博客，**不用**。
- **两种解读都有人说**：主张收紧的一方认为，中国开发者转向国产硬件说明管制在逼出替代、更不能放；反对的一方（包括黄仁勋）认为管制「backfired」，反而加速了华为生态。两边都是观点。

**我们的判断**：DeepSeek 让「卖还是不卖」变成了一个真问题——卖，怕帮对手；不卖，怕把市场和开发者生态让给华为。这正是黄仁勋与国会鹰派公开对立的那条线，也是为什么他的私人关系一旦被情报界盯上，就立刻成了国家安全议题。

## 5. 黄仁勋在两国之间的公开立场（原话）

| 日期 | 场合 | 原话 | 出处 | 性质 |
|---|---|---|---|---|
| 2025-05-21 | 台北 Computex | 「All in all, the export control was a failure」；份额「95%」降到「50%」；「If they don't have enough Nvidia, they will use their own.」 | Reuters 经 BNN Bloomberg https://www.bnnbloomberg.ca/business/technology/2025/05/21/nvidia-ceo-praises-trump-move-to-scrap-some-ai-export-curbs/ ；Fortune https://fortune.com/2025/05/22/nvidia-ceo-jensen-huang-failure-us-restrictions-chips-semiconductors-china-ai-artificial-intelligence/ | 已证实 |
| 2025-07-15 | 北京链博会期间 | 「美国政府已经批准了我们的出口许可，可以开始发货了，所以我们将开始向中国市场销售 H20。」 | 环球网 | 已证实 |
| 2025-09/10 | 访谈（据报道） | 称「中国鹰派」这个标签是「耻辱的徽章」（中文转述；英文原话未找到） | unwire.hk https://unwire.hk/2025/10/01/huang-china-agent-controversy/ai ；Washington Examiner 评论（未读） | **报道称**（英文原文待核，片中不用直接引号） |
| 2025-10 | 采访 | 「伤害中国的事情，往往也可能伤害美国，甚至会更严重。」（中文转述） | 环球网 2025-12 报道 | 报道称（经转译） |
| 2025-11-05 | FT Future of AI 峰会场边 | 「China is going to win the AI race」；同日在 X 上改口：「China is nanoseconds behind America in AI.」「It's vital that America wins by racing ahead and winning developers worldwide.」 | Fox Business 转述 FT https://www-ak-ms.foxbusiness.com/fox-news-tech/nvidia-ceo-jensen-huang-warns-china-going-win-ai-race-against-america-report | 已证实（两句都有转载；FT 原文未读） |
| 2026-03-17 | 对记者 | 称已获中美两国政府必要批准（Coons 信转述） | Coons 办公室 | 报道称 |
| 2026-11-08 | 致员工信 | 「I love our country and our company」「I am proud and grateful to be an American.」 | Foreign Policy 转述（原信见 timeline.md P3） | 已证实 |
| 2026-11-09 公布 | Bloomberg 采访片段 | 称与 Megaspeed 的关系「normal and not unusual」；称出口管制是难以扭转的错误（「hard to unwind」，转述） | Foreign Policy；检索摘要 | 报道称 |
| 2025–2026 | 接受 AP 采访 | 贸易谈判是两国政府的事，他的角色是解释规则对行业意味着什么（转述） | Open 杂志转述 AP | 报道称 |

**小结**：黄仁勋公开的立场一贯是「**美国应该赢，但赢法是卖给全世界、包括中国**」。他既批评美国管制「失败」，也强调自己是美国人、美国必须领先。这让他在中国舆论里被看作「被美国政治牵连的华裔企业家」，在华盛顿鹰派眼里却是「替中国市场游说的人」。同一个人的同一套话，在两国舆论里被读成两种角色。
