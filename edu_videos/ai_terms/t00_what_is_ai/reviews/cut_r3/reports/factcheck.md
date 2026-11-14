本轮仍有 **3 项必改**：l23 把实验结果说成最低样本门槛，l32 把“种类更全”的作用说成已获验证，l45 把单月统计扩大成“每个月”。实验数字内部一致，但缺少运行输出，真实性仍存疑。

仅检查指定四份材料及外部出处；画面文字以 `claims.json` 登记内容为准，未检查实际成片。

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l01 | 双语 | 记录 | **R：已解决。**中文已改为“不需要”，英文保留 “nobody had to”，均表示不必逐条编写识别规则，没有再断言具体产品的开发历史。 | 保留。 |
| l15 | 双语 | 建议 | **R：未解决。**“不写规则”仍可能让观众误以为算法、目标和约束也不需要人设计。作者只标“保留”，没有说明消除歧义的依据。 | zh：今天的 AI，大多换个做法：不逐条写认法，给例子。<br>en：Most of today's AI uses examples instead of hand-written recognition rules. |
| l17 | 双语 | 建议 | **R：未解决。**前句展示的是带答案的监督学习；它确实属于机器学习，因此不是直接错误，但补“一种”能避免观众把人工标注当成所有机器学习的必要条件。 | zh：它从例子里找规律。这是机器学习的一种。<br>en：It learns patterns from examples. This is one kind of machine learning. |
| l19 | 双语 | 记录 | **R：未解决。**“很多人以为”仍没有公众认知调查支持；属于修辞性概括，不影响后半句机制解释，不必升级成主要错误。 | 首句改为：<br>zh：AI 的本事，不全是程序员写进去的。<br>en：An AI's abilities aren't all programmed explicitly. |
| l23 | 双语 | 必改 | **R：未解决。**10 张约 37%、100 张约 88%，不能证明“要上百个才认得准”；“才／needs…before”额外断言了最低需求。C19 的实验来源也不能支持儿童数量认知。 | 第二句改为：<br>zh：待会儿会看到，这次给模型一百个例子，它就认得明显更准。<br>en：As you'll see, our model does much better with a hundred examples in this experiment.<br>儿童部分另列来源，或明确登记为类比。 |
| l24 | 双语 | 记录 | **R：未解决。**“上千道／a thousand dishes”仍未登记。做菜本来就是虚构类比，不必要求厨师统计研究，但这个具体数量没有解释作用。 | 局部替换：<br>zh：老师傅反复练习，每次尝一口、听人评价、差了就调，才练出来。<br>en：A seasoned cook develops that feel through practice, tasting, feedback, and adjustments. |
| l25 | 双语 | 建议 | **R：未解决。**味觉和评价可以类比反馈，但不一定对应唯一的“正确答案”。作者未给出保留理由；建议保留类比、放松等号。 | 局部替换：<br>zh：尝一口、听评价，就是检查做得怎么样；差了就调，这就是学习。<br>en：Tasting and feedback check how it turned out. Adjusting when it's off is learning. |
| l27 | 双语 | 建议 | **R：未解决。**新增“训练”的解释是有效补充，但未处理原问题：“才知道真会认了”仍把测试证据说得过满。一次留出测试估计的是新样本表现，不能证明学到的规律一定可靠。 | 末两句替换：<br>zh：为什么这样分？要检验它能不能认出训练时没见过的新题。<br>en：Why split it this way? To test how well it handles examples it never trained on. |
| l32 | 双语 | 必改 | **R：未解决。**实验改变样本数量及抽到的内容，没有单独比较“数量相同、种类不同”的效果；因此不能把“越全／more kinds”的独立作用说成已验证。 | 中间一句替换：<br>zh：这次实验里，例子增加后，考试成绩提高了。<br>en：In this experiment, scores improved with more examples. |
| l33 | 双语 | 记录 | **R：未解决。**“人也要犹豫”仍未登记。它可以是对图片的主观观察，但现有材料没有图片或人工辨认记录，无法独立确认，也不能由模型认错推出。 | 删除末句。 |
| l35 | 双语 | 建议 | **R：未解决。**C04 已说明是模型预测概率，口播和登记画面仍未明确“模型估计”。“把握”可以作通俗说法，但首次出现时宜说明其含义；输出概率的可靠性需要校准证据。[概率校准文档](https://scikit-learn.org/stable/modules/calibration.html) | zh：这个模型也报预测概率。这张图，它给“三”96%；这是模型估计。<br>en：Our model also assigns probabilities. Here, it gives three 96%. That's its estimate.<br>上屏：zh「模型预测：3，96%」；en「Model prediction: 3, 96%」。 |
| l38 | 双语 | 记录 | **R：已解决。**保留“能从数据学到知识”，同时指出流畅不保证正确；没有再把生成机制解释成不能掌握事实知识。[GPT-3 论文事实问答部分](https://arxiv.org/html/2005.14165v4#S3.SS2) | 保留。 |
| l43 | 双语 | 记录 | **存疑的是逐字引文核验，不是已发现讲稿错误。**C08、C16 的诺奖页面本轮返回 403，未能逐字确认；原论文支持单个结构测定耗时数月至数年的核心事实。[AlphaFold 原论文](https://pmc.ncbi.nlm.nih.gov/articles/PMC8371605/) | 口播暂保留。核验状态注明：**“诺奖原句待复核”**；用可访问的官网正文或官方 PDF 核对 C08 两句、C16 一句原文。 |
| l45 | 双语 | 必改 | **R：未解决。**原报道是 **2023 年 1 月的月活跃用户估计**；中文“每个月就有”扩大为持续多月的结论。英文应保留 active，与台账、画面口径一致。[Reuters 原稿转载](https://www.marketscreener.com/news/latest/ChatGPT-sets-record-for-fastest-growing-user-base-analyst-note-42873811/) | zh：ChatGPT 上线约两个月，月活跃用户估计达到一亿。<br>en：About two months after launch, ChatGPT had an estimated 100 million monthly active users. |
| l47 | zh | 记录 | **R：已解决。**明确指英文 women's，没有扩大成中文“女子”字样；“女子国际象棋社社长”保留了例子的主要意思，没有改变扣分对象。[Reuters 原页面存档 PDF](https://jlucasmckay.bmi.emory.edu/global/bmi510/Reference/hiring-bias.pdf) | 保留。 |
| l51 | 双语 | 建议 | **R：未解决。**本模型不能输出“非数字”有 C20 支持；“小孩会说”仍不由模型实验支持。作为假设类比可以理解，但换成“人可以”更准确。 | zh：它只在十个数字里比较。人可以说“不是数字”，这个模型只能选数字。<br>en：It compares only ten digits. A person can reject the input; this model must choose a digit. |
| 全片 | 双语 | 记录 | **R：未解决，存疑。**C01–C06、C19、C20 仍只有断言说明，指定材料没有运行输出。可以核对数字关系，不能确认各成绩、探针概率和错题身份确由当前模型产生；这也不等于已经证明数字错误。 | 核验状态写：**“待对照当前实验运行输出核实”**。需核对模型配置、预处理、划分和抽样种子、20 次成绩及中位数、探针索引及概率；同时确认测试集未用于调参或挑选模型。 |
| 全片 | 双语 | 记录 | **R：未解决，台账覆盖仍有缺口。**l24–l25 未登记；C13 未挂 l56–l57；l19 公众认知、l33 人工辨认、l51 儿童表现缺对应依据；C19 的实验来源不能覆盖儿童认知部分。作者只写“保留”，未给出实质核查理由。 | 补记：**“l24–l25：虚构做菜类比，非实证案例”**；C13 增加 l56、l57；C19 拆分模型实验与儿童类比。其余采用对应行替换稿。 |

其余必查项的核对证据：

- **C01–C07：**官方文档支持 `load_digits` 为 1,797 张、8×8、十类数字，且是 UCI 原数据的测试集副本；UCI 全库是 5,620 条，不能混为本片样本数。CC BY 4.0 许可登记正确。1,797−300＝1,497；300 题错 10 题即约 96.67%，四舍五入为 97%，两句不矛盾。10% 是十类均匀随机猜测的期望准确率。其余实验结果仍按表中“存疑”处理。[scikit-learn 数据说明](https://scikit-learn.org/stable/datasets/toy_dataset.html#optical-recognition-of-handwritten-digits-dataset)、[UCI 数据与许可](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)
- **C08–C11、C16：**奖项归属核对通过：Hassabis 与 Jumper 共同分享一半，另一半属于 Baker；不是两人各得一半。亚马逊报道确有十年简历、大多来自男性、women's 扣分及项目放弃，讲稿没有断言已实际淘汰女性，也没有把放弃原因归结为偏见这一项。[瑞典皇家科学院官方材料](https://www.kva.se/app/uploads/2025/03/Nobelposter_2024_chemistry.pdf)、[Reuters 存档原稿](https://jlucasmckay.bmi.emory.edu/global/bmi510/Reference/hiring-bias.pdf)
- **C12–C15、C17：**AI／机器学习／深度学习的层级、规则下棋程序的例子、“模型”作为本片分类映射的解释均可接受；C12 图注、C14 引文和 C15 的短引文可与原文对应。l37 用“词”作简化，台账已登记“严格说是词元 token”，须确保该提示实际呈现。[教材第 1 章](https://www.deeplearningbook.org/contents/intro.html)、[GPT-3 原论文](https://arxiv.org/html/2005.14165v4)
- **C18–C23：**C18 泛化引文、C22 过拟合引文与教材对应；l58 作为预告描述典型现象可以保留。C21 没有再给数据与设计、训练强行排主次；C23 已明确虚构示例。欠拟合、验证集、正则化、捷径学习未在本轮讲稿中展开，没有相应错误定义；300 道“考试题”按描述承担测试集作用，是否参与调参仍待实验记录确认。[教材第 5 章](https://www.deeplearningbook.org/contents/ml.html)
- **翻译及 R 复核：**已逐条复核上一轮全部 factcheck 条目。未发现把程度词译成确定比例、把估计译成实测等新增翻译错误；本轮也未发现“改出了新问题”的条目。作者“未专门改动，保留”是处理记录，不能单独作为反驳依据；修辞、类比的小问题已按实际影响保留为“建议／记录”。

**最重要的 3 条**

1. l23 改成“本次一百个例子表现更好”，删除最低样本门槛的暗示。
2. l32 只报告样本增加后的成绩变化，不宣称独立验证了“种类更全”的作用。
3. l45 恢复单月月活估计口径，删除“每个月”。

**做得好的、别改掉的**

1. 区分“不给识别规则”和“提供答案标签”，保留 l32 前半句。
2. l38 同时承认模型能学到知识、流畅回答可能出错。
3. 现实案例保留来源、估计及使用范围限制，尤其亚马逊的“曾想用”。

其他：无。