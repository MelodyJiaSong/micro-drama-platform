已逐条检查 C01–C23。结论：**3 处必改**，主要涉及绝对化表述、语言模型机制和引文翻译。实验数字内部一致，但指定材料没有运行输出，相关结果仍标为「存疑」。画面文字按 claims.json 的 `screen` 字段审查，未观看成片。

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l01 | 双语 | 必改 | 「从来没有人／nobody ever」把某类识别器的学习方式扩大成了历史断言；C13 的教材出处只能支持“不必逐条编写识别规则”，不能支持“从未有人写过”。[教材第 1 章](https://www.deeplearningbook.org/contents/intro.html) | zh：相册认得出你家的猫，却不需要人把「猫长什么样」逐条写成规则。<br>en：Your photo app can spot your cat without anyone spelling out every rule for recognizing one. |
| l15 | 双语 | 建议 | 「不写规则」容易被听成机器学习不需要人设计算法、目标或约束。这里实际省掉的是逐条手写的识别规则。 | zh：今天的 AI，大多换了一个做法：不逐条写认法，给例子。<br>en：Most of today's AI takes a different approach: give examples instead of spelling out recognition rules. |
| l17 | 双语 | 建议 | 前一句演示的是**监督学习**。直接作为机器学习的完整定义，容易让观众以为所有机器学习都需要人提供答案。 | zh：它从例子里找规律。这是机器学习的一种。<br>en：It learns patterns from examples. This is one kind of machine learning. |
| l23 | 双语 | 建议 | 「要看上百个……才」把本次抽样结果说成了最低样本需求；C02 没有证明这个门槛。C19 的实验出处也不能证明儿童如何理解数量。 | 将第二句替换为：<br>zh：待会儿会看到，这次给模型一百个例子，它就认得明显更准。<br>en：As you'll see, our model does much better with a hundred examples in this experiment. |
| l24 | 双语 | 记录 | 「做过上千道／a thousand dishes」是未登记的具体数量，容易让虚构类比带上实证意味。 | 局部替换：<br>zh：老师傅反复练习，每次尝一口、听人评价、差了就调一调，才练出来。<br>en：A seasoned cook develops that feel through practice, tasting, feedback, and adjustments. |
| l25 | 双语 | 建议 | 尝味道、听评价属于反馈，不一定存在唯一的「正确答案」。把它直接等同于监督学习标签，类比不够准确。 | 局部替换：<br>zh：尝一口、听评价，就是检查做得怎么样；差了就调，这就是学习。<br>en：Tasting and feedback check how it turned out. Adjusting when it's off is learning. |
| l27 | 双语 | 建议 | 「才知道它是真会认了」说得稍满。留出测试题能估计新样本表现，不能一次考试就证明它掌握了可靠规律；还取决于数据分布与是否泄漏。[教材 §5.2–5.3](https://www.deeplearningbook.org/contents/ml.html) | 将末两句替换为：<br>zh：为什么这样分？要检验它能不能认出训练时没见过的新题。<br>en：Why split it this way? To test how well it handles examples it never trained on. |
| l33 | 双语 | 记录 | 「连人看了都要犹豫」未登记，也没有人工辨认记录；不能从模型错题直接推出人的表现。 | 将末句替换为：<br>zh：这也是模型认错的一张。<br>en：That's one of its mistakes. |
| l35 | 双语 | 建议 | 「96% 的把握」可以作为通俗说法，但首次出现时最好明确这是**模型估计**。C04 已有此限定，口播和上屏没有带出来；未校准的预测概率不能直接当作可靠正确率。[概率校准文档](https://scikit-learn.org/stable/modules/calibration.html) | zh：这个模型也会报预测概率。这张图，它给「三」96%；这不是实测正确率。<br>en：Our model also assigns probabilities. Here, it gives three 96%. That's its estimate, not measured accuracy.<br>上屏：zh「模型预测：3，96%」；en「Model prediction: 3, 96%」。 |
| l38 | 双语 | 必改 | 「猜的是接下来像什么话，不是什么是真的」把**生成机制不能保证真实性**说成了机制排斥事实知识。所引 GPT-3 论文同时评估了事实问答，不能据此推出语言模型只学接话、不学事实。[GPT-3 论文 §3.3](https://arxiv.org/html/2005.14165v4#S3.SS3) | zh：能聊天的大语言模型，通常这样生成回答。它能从数据里学到知识，但接话流畅，不保证事实正确。<br>en：Conversational language models usually generate replies this way. They can learn factual knowledge, but fluent text doesn't guarantee accurate facts. |
| l45 | 双语 | 建议 | 原报道是**2023 年 1 月这一统计月份的月活估计**；「每个月就有」容易听成持续多个月的已确认人数。英文也宜保留 active。[Reuters 原稿转载](https://www.investing.com/news/world-news/chatgpt-sets-record-for-fastestgrowing-user-base--analyst-note-2993773) | zh：ChatGPT 上线约两个月，月活跃用户估计达到一亿。<br>en：About two months after launch, ChatGPT had an estimated 100 million monthly active users. |
| l47 | zh | 必改 | 原文惩罚的是英文词 **women’s**，不是中文词「女子」。当前口播与 C11 上屏保留的英文词不一致；「club」译成「队」也不如「社」贴切。[Reuters 原页面存档 PDF](https://jlucasmckay.bmi.emory.edu/global/bmi510/Reference/hiring-bias.pdf) | 结果，它等于学会了「男性候选人更好」：简历里出现英文 women’s，比如「女子国际象棋社社长」，就会被扣分。这个工具后来被放弃了。 |
| l51 | 双语 | 建议 | 十分类模型不能输出「非数字」成立；「小孩会说」却是另一个未经验证的儿童表现断言，也不是 C20 的实验能证明的。 | zh：这个把握，只是在十个数字里比谁更像。人可以说「不是数字」，这个模型只能选数字。<br>en：That confidence compares only the ten digits. A person can reject the input; this model must choose a digit. |
| 全片 | 双语 | 记录 | **存疑：**C01–C06、C19、C20 的实验部分只有断言描述，没有本轮运行输出；不能把台账自述当成独立复核结果。尤其 96%、92%、81% 和具体错题身份尚未验证。 | 台账核验状态先写：**「待对照本轮运行输出核实」**。核实应提供模型配置、划分与抽样种子、20 次准确率及中位数、探针样本和概率输出；无需先改口播数字。 |
| 全片 | 双语 | 记录 | 台账覆盖仍有缺口：l24–l25 的做菜类比未登记；l19「很多人以为」没有调查依据；l56–l57 重述 C13，但未列入其句号。儿童与人工辨认断言见上表。 | l19 首句可缩为：zh「AI 的本事，不全是程序员写进去的。」／en「An AI's abilities aren't all programmed explicitly.」<br>台账补记：**「l24–l25：虚构做菜类比，非实证案例」**；C13 增补 l56、l57。 |

**其余核查证据与边界**

- **C01–C07、C19、C20：**官方文档确认 `load_digits` 是 UCI 原数据的测试子集，含 **1,797 张、8×8、10 类**；不能把 UCI 完整数据也说成只有 1,797 张。1,797−300＝1,497；300 题错 10 题对应 96.67%，四舍五入为 97%，无算术矛盾。37%／88% 是 20 次抽样的中位数，97% 是全量训练一次，台账已区分；10% 是十类**均匀随机猜测的期望准确率**。[scikit-learn 数据说明](https://scikit-learn.org/stable/datasets/toy_dataset.html#optical-recognition-of-handwritten-digits-dataset) UCI 页面也确认作者与 CC BY 4.0，C07 登记成立。[UCI 原页](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)
- **C08、C09、C16：**“常要好几年”得到诺奖官方索引支持，原论文也明确说明实验测定常耗时数月至数年；“预测”没有被说成实验测定。Hassabis 与 Jumper **共同分享一半**，另一半属于 Baker，人数与份额正确。诺奖正文此次返回 403，采用官方检索条目与原论文交叉核对。[诺奖科普](https://www.nobelprize.org/prizes/chemistry/2024/popular-information/)、[诺奖新闻稿](https://www.nobelprize.org/prizes/chemistry/2024/press-release/)、[AlphaFold 原论文](https://pmc.ncbi.nlm.nih.gov/articles/PMC8371605/)
- **C10、C11：**Reuters 官网及所附 Internet Archive 快照此次无法读取，改查 Reuters 原稿转载及原页面存档。已确认一亿来自 **UBS 引 Similarweb 的估计**；十年简历、大多来自男性、惩罚 women’s 均与报道一致。讲稿没有把“后来放弃”强说成“仅因偏见叫停”，也没有声称实际淘汰了女性。
- **C12–C15、C17、C18、C21：**AI／机器学习／深度学习的包含关系、模型作为本例输入到类别的映射、泛化概念均成立。C13、C14、C18 的摘录与教材相应段落一致；C15 的短引确实出现在 GPT-3 引言。l37 用「词」是简化，但登记的上屏已补「严格说是词元 token」，可保留。[教材第 1 章](https://www.deeplearningbook.org/contents/intro.html)、[第 5 章](https://www.deeplearningbook.org/contents/ml.html)、[GPT-3 原论文](https://arxiv.org/html/2005.14165v4)
- **C22、C23及专业概念：**C22 的过拟合引文与教材原文一致，l58 作为预告没有概念错误；C23 已明确是虚构反例。欠拟合、正则化、捷径学习未在本次讲稿或登记画面中直接定义。测试集没有被叫成验证集；但是否曾用这 300 张题调参，指定材料无法确认，仍属存疑，应查实验过程记录。[教材 §5.2–5.3](https://www.deeplearningbook.org/contents/ml.html)

**最重要的 3 条**

1. l01 删除「从来没有人」，避免把学习方法讲成未经支持的历史断言。
2. l38 改为「生成流畅不保证事实正确」，保留事实知识与生成机制的区别。
3. l47 中文保留英文 **women’s**，让解说、原文与上屏一致。

**做得好的、别改掉的**

1. 诺奖明确说“两位研发负责人共同分享一半”，归属与份额准确。
2. 实验注明“这一次”，并登记中位数与单次全量结果，没有宣称普遍达到 97%。
3. 用高置信错题和范围外字母解释局限，同时承认设计、训练也影响表现，避免把问题全部归咎于数据。

**其他：**未提出本角色范围外的问题。