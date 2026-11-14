仍有必改项：l35、l50 把本期模型的性质推广到了所有 AI；事实台账仍有漏项，部分“原话”需要纠正。实验数字目前只能确认口径与算术一致，尚不能独立确认运行结果。

本轮只读取指定的四份材料及外部出处，未修改文件。下表的 **R** 对应上一轮 factcheck 的全部 19 项；句号采用本轮编号，括号注明旧编号。已解决项列为“记录”，不要求再改。

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l01 | 双语 | 建议 | **R：已解决原问题。** 现在已区分“不手写识别规则”和“不给训练信息”。但“从来没有人／nobody ever”仍是无出处的历史性绝对判断；C13 只能支持无需逐条写全规则。 | zh：相册认得出猫，不需要人把认猫的规则一条条写全。<br>en：Your photo app can spot cats without people spelling out every recognition rule. |
| l11 | 双语 | 记录 | **R：已解决。** “谁也说不清”已改成“很难写全”，与教材所说的难以形式化描述一致。 | 保留。 |
| l14 | 双语 | 记录 | **R：已解决。** 不再宣称无论写多少规则都必然失败，而是指出所举规则会漏判、误判。 | 保留。 |
| l15 | 双语 | 建议 | **R：未解决。** 仍说“不写规则／Don't write rules”，没有采用 C13 自己已有的“识别规则”限定；容易把人工设计算法、目标和约束也排除掉。 | zh：一种常见做法：不写识别规则，给带答案的例子。<br>en：One common approach: give labeled examples instead of hand-written recognition rules. |
| l23 | 双语 | 建议 | **R：未解决，存疑。作者“不采纳”的理由不成立。** 本片模型看十例得 37%，没有提供同任务儿童对照，更没有统一儿童既往经验与模型预训练的口径，不能证明模型“通常”需要更多例子。“通常”也不能代替证据。 | zh：不过并不完全一样。模型要多少例子，要看任务；有些模型学到的规律，连开发者也难解释。<br>en：The analogy has limits. How many examples a model needs depends on the task. Some models learn patterns even their makers struggle to explain. |
| l27 | 双语 | 记录 | **R：未解决，存疑（旧 l27）。** 作者说明模型和默认参数事先确定、未用考试题选模型，方向正确；但指定材料没有附预处理拟合范围、完整配置或运行记录，不能独立确认测试集始终隔离。教材要求测试集也不得参与超参数选择。[教材 §5.3](https://www.deeplearningbook.org/contents/ml.html) | 非口播：补充配置、预处理拟合范围及运行记录，并明确“300 张未参与训练、预处理拟合或模型选择”。不增加解说。 |
| l29 | 双语 | 记录 | **R：已解决。** “多抽几回／typical score”与 C02 的中位数口径一致；画面还注明 20 次抽样，以及最后一点只跑一次。实际数值的复核另见全片实验项。 | 保留口播与抽样注释。 |
| l35 | 双语 | 必改 | **新增。** 承接“今天的 AI”，直接说它都会报告把握，超出了本片实验和 C15 出处。并非所有模型都支持概率输出；预测概率也不自动等于实际正确率。[scikit-learn 概率校准文档](https://scikit-learn.org/stable/modules/calibration.html) | zh：这个模型还会报把握：这张图，它给「三」96%的预测概率。<br>en：This model also reports confidence: a 96% predicted probability for three. |
| l39 | 双语 | 记录 | **R：已解决（旧 l38，口播）。** 已明确举规则式下棋程序，并排除普通工资程序。**画面存疑：** C12 仍登记“人写规则（传统办法）”；若它直接标注 AI 圈的一块区域，仍可能把所有手写程序纳入 AI。指定材料没有实际布局可核实。 | 口播保留。该画面标签可改为：<br>zh：规则式 AI（如下棋）<br>en：Rule-based AI (e.g. chess) |
| l40 | 双语 | 记录 | **R：已解决（旧 l39）。** 现在先说深度学习使用神经网络，再描述多层计算；没有把“很多层计算”反过来当作所有神经网络的定义。 | 保留。 |
| l41 | 双语 | 记录 | **R：已解决（旧 l40）。** 已从缺出处的社会用语比例判断，改为明确限定本片讨论范围。 | 保留。 |
| l45 | 双语 | 记录 | **R：已解决（旧 l43）。** 本轮已没有“超过／passed”；保留估计、上线约两个月及月度用户口径。虽然作者栏写“无需改”，当前文字实际已消除了原问题。 | 保留；画面继续保留“月活跃用户（估计）”及 UBS／Similarweb 来源。 |
| l46 | 双语 | 记录 | **R：已解决（旧 l44）。** “学到的规律也可能带偏见”准确，没有再把偏见放到“规律”之外。 | 保留。 |
| l47 | zh | 记录 | **R：已解决（旧 l45）。** *captain* 已译为“队长”。画面登记了原词 *women’s*，能说明这不是中文词语触发的真实实验。 | 保留“女子国际象棋队队长”及画面英文原词。 |
| l48 | 双语 | 记录 | **R：已解决（旧 l46）。** 已从“数据里有什么就学什么”的必然判断，收紧为可能学到偏见。 | 保留。 |
| l50 | 双语 | 必改 | **R：未解决（旧 l48）。** 加“那一类”缓和了逐例记忆的误解，但“它只懂它学过的那一类东西”仍是所有 AI 的能力边界断言。这个 A 实验只能证明：本期封闭十分类模型面对范围外输入仍会强制分类。GPT-3 原论文恰恰研究了模型对新任务的迁移与上下文适应，不能据此推广。[原论文](https://arxiv.org/abs/2005.14165) | zh：第一，超出训练范围，它也可能乱认。我们给这个数字模型看字母 A：它只能从零到九里选，竟给「四」92%的概率。<br>en：One: unfamiliar inputs can fool it. We showed this digit-only model an A. It had to pick zero to nine, and gave four 92% probability. |
| l53 | 双语 | 建议 | **R：未解决（部分修正，旧 l50）。** 已补设计与训练，解决了“全部来自数据”的单因归因；但“主要来自数据／mostly”仍给出了未经证明的贡献排序。教材列出的模型、目标、优化和数据共同影响结果，不能据此排主次。 | zh：第三，本事和毛病，既受数据影响，也受设计和训练影响。判断 AI 靠不靠谱，先问它学过什么。<br>en：Three: data, design, and training shape its strengths and flaws. To judge an AI, start by asking what it learned from. |
| l54 | 双语 | 建议 | **新增。** 接在 l50 后，会进一步暗示“有没有学过这类题”足以判断答案可靠性；普通使用者通常也无法核实训练内容。对新问题的泛化与对答案的查证应区分。 | zh：下次 AI 很有把握地回答你，不妨想一想：这个答案，核实过吗？<br>en：Next time an AI answers with total confidence, ask yourself: has this answer been checked? |
| l58 | 双语 | 记录 | **R：已解决（旧 l54）。** 已把“背答案”的机制断言，改成训练题与新题表现的反差。作为下期预告成立；不应再把它展开成过拟合的唯一成因。[教材 §5.2](https://www.deeplearningbook.org/contents/ml.html) | 保留。 |
| 全片 | 双语 | 必改 | **R：未解决——事实登记仍不完整。** C12–C15 补齐了大量内容，但仍缺明确登记：l18 模型定义、l21 未见写法的泛化、l23 儿童比较及可解释性、l27 留出测试的作用、l50 开头的能力范围、l53 原因排序、l58 过拟合。C13 的标签学习概括不能替这些不同主张作证。 | 非口播：按上述句号分别登记主张与出处；l23、l50、l53 先按本表收紧。模型、泛化、测试及过拟合可分别引用教材 §5.1–5.3，不增加口播。 |
| 全片 | 双语 | 记录 | **R：未解决，存疑——C01–C06 实验仍未独立复核。** 断言地址和作者“本机运行通过”的说明是线索，不是本轮能检查的运行证据。材料未给完整配置、版本、逐次得分与探针对应图；所称“已写进讲稿头部”的实验说明也未出现在本轮 `lines.md`。不能因此判数字错，也不能判已核实。 | 非口播：在审稿材料附模型及预处理配置、版本、种子、20 次得分、中位数和三张探针图及输出；同时附测试集隔离说明。不增加解说。 |
| 全片 | 双语 | 必改 | **新增——原话与概括混放。** C15 所列“trained to predict the next token”在 GPT-3 全文及所标 §2 未找到，不能作为已核实原话；C13 将原文 *then learning* 改成了 *and learning*；C07 将原文 *This is* 换成 *load_digits is*，未标编辑替换。[GPT-3 原文](https://arxiv.org/pdf/2005.14165)、[教材原文](https://www.deeplearningbook.org/contents/ml.html)、[数据集文档](https://scikit-learn.org/stable/datasets/toy_dataset.html) | 非口播：C15 可改摘 §1 的“simply by predicting what comes next”，词元机制另标“概括”；C13 恢复 *then learning*；C07 恢复 *This is*，在引文外说明所指是 `load_digits`。 |

**逐条台账与必查项核对证据**

- **C01、C07：** 官方文档确认 `load_digits` 是 1,797 张、8×8 图像，是 UCI 原数据测试集的副本；UCI 全数据集是 5,620 个样本，因此不能把 1,797 说成 UCI 全库总数。当前台账已作区分，署名、1998 年及 CC BY 4.0 与官网一致。300＋1,497＝1,797；具体划分仍待实验记录核实。[scikit-learn](https://scikit-learn.org/stable/datasets/toy_dataset.html)、[UCI](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)
- **C02、C03：** 37%／88% 是多次抽样中位数，97% 是全部训练样本的一次结果，当前画面注释已区分。300 题错 10 题对应 96.67%，四舍五入为 97%，没有矛盾。“瞎猜 10%”应理解为十类等概率猜测的期望正确率。具体得分及“覆盖五至九类”仍存疑，核实方法见表。
- **C04、C05、C06：** 96%／92%／81% 登记的是本片模型的预测概率或置信度，不能当作经校准的实际正确率，也不是官方基准成绩。指定材料没有探针图与运行输出，本轮未独立确认三个数值。
- **C08、C16：** “常常要好几年”忠实于诺奖科普材料的频率限定，没有加成“每个都要几年”；从已知结构学习的概括成立，原文还提到氨基酸序列。官网正文及 PDF 本轮返回 403，核对依据是其官方搜索索引返回的对应原文，未宣称完整读取成功。[诺奖科普材料](https://www.nobelprize.org/prizes/chemistry/2024/popular-information/)
- **C09：** 官方摘要确认 Hassabis 与 Jumper 共同分享化学奖的一半，另一半属于 Baker；讲稿没有误说两人包揽整届奖项。“带领研发”也避免了把多人论文说成只有两位作者。[诺奖官方摘要](https://www.nobelprize.org/prizes/chemistry/2024/summary/)
- **C10：** 已通过署名 Reuters 的全文转载核对：2023 年 1 月、上线约两个月、估计一亿月活跃用户；来源链是 UBS 引用 Similarweb，不是 OpenAI 官方公布，也不是注册用户数。当前口播与已登记画面没有夸大。[Reuters 原稿转载](https://www.marketscreener.com/news/latest/ChatGPT-sets-record-for-fastest-growing-user-base-analyst-note-42873811/)
- **C11：** 已核对 Reuters 署名全文转载：十年间提交的简历、多数来自男性、惩罚 *women’s* 及所举队长例子均有原文。“曾想用”“后来被放弃”没有升级成已据此淘汰女性，也没有把项目关停归因于唯一原因。[Reuters 原稿转载](https://www.investing.com/news/stock-market-news/amazon-scraps-secret-ai-recruiting-tool-that-showed-bias-against-women-1637988)
- **C12、C13、C14：** 教材支持 AI／机器学习／深度学习的包含关系、监督学习利用输入与标签，以及直觉识别任务难以完整形式化；C14 摘录与原文相符。具体 3、5、8 的画面样图不在指定材料内，本轮不能确认其笔画展示。[教材第 1 章](https://www.deeplearningbook.org/contents/intro.html)、[第 5 章](https://www.deeplearningbook.org/contents/ml.html)
- **C15：** 自回归生成的基本解释成立；口播将 token 简化为“词”，画面已登记“严格说是词元 token”，作为入门解释可保留。需要纠正的是引文及“所有 AI 都输出把握”的范围。[GPT-3 原论文](https://arxiv.org/html/2005.14165v4)
- **专业概念：** 过拟合预告现已落在训练与泛化表现的差距上；测试集用途的方向正确，独立性仍待证据。稿中没有讲欠拟合、验证集、正则化或捷径学习，没有发现这些概念被混用；固定配置的演示不因没有另设验证集就自动错误。

**最重要的 3 条**

1. l35、l50 限定为本期数字模型，避免把局部实验推广成所有 AI 的性质。
2. 补齐事实登记，纠正 C15 等处“概括冒充逐字引文”的问题。
3. 实验数字补可复核证据；l23 的儿童比较不能用本片模型成绩佐证。

**做得好的、别改掉的**

1. 保留 37%／88% 的中位数说明，以及最后一点只跑一次的例外注释。
2. 保留诺奖“一半”、ChatGPT“估计月活”和 Amazon“据路透社／曾想用”的口径。
3. 保留“可能学到偏见”、具体错认的二，以及预测不保证正确的提醒。