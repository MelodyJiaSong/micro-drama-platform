本轮仍有表述需收紧；**实验数字尚不能标为独立核验通过**。仅阅读指定四份材料，并核对外部原始出处；画面文字只核对了 claims.json 的 `screen` 字段，未查看实际成片。表中 **R** 表示复核上一轮事实核查意见。

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l01 | zh | 必改 | **R：未解决。**「从来没有人」改成「并没有人」，仍在断言具体相册的开发事实；教材只支持“不必逐条写识别规则”，不能证明实际无人写过。[教材第1章](https://www.deeplearningbook.org/contents/intro.html) | 相册认得出你家的猫，却不需要人把「猫长什么样」逐条写成规则。 |
| l01 | en | 记录 | **R：已解决。**“nobody had to”表达“不必”，已消除原来“从未有人做过”的历史断言。 | 保留。 |
| l15 | 双语 | 建议 | **R：未解决。**「不写规则」仍容易被理解成不需要人设计算法、目标和约束；省掉的是逐条手写识别规则。 | zh：今天的 AI，大多换了一个做法：不逐条写认法，给例子。<br>en：Most of today's AI takes another approach: examples instead of hand-written recognition rules. |
| l17 | 双语 | 建议 | **R：未解决。**作者处理栏写的是流程框字号调整，未处理概念范围。前句演示监督学习，宜明确它是机器学习的一种，避免观众以为机器学习都需要人工给答案。[教材§5.1.3](https://www.deeplearningbook.org/contents/ml.html) | zh：它从例子里找规律。这是机器学习的一种。<br>en：It learns patterns from examples. This is one kind of machine learning. |
| l19 | 双语 | 记录 | **R：未解决，属于上一轮“台账覆盖”问题。**「很多人以为」没有调查依据；C13支持学习机制，不支持公众认知比例。 | 首句替换：<br>zh：AI 的本事，不全是程序员写进去的。<br>en：An AI's abilities aren't all programmed explicitly. |
| l23 | 双语 | 建议 | **R：未解决。**「要上百个……才」把两个抽样规模的结果说成最低样本需求；10张约37%、100张约88%，不能证明不足100张就认不准。C19的实验也不能证明儿童如何理解数量。 | 第二句替换：<br>zh：待会儿会看到，这次给模型一百个例子，它就认得明显更准。<br>en：As you'll see, our model does much better with a hundred examples in this experiment. |
| l24 | 双语 | 记录 | **R：未解决。**「上千道／a thousand dishes」仍是未登记的具体数量；作者处理的是插图，未处理事实措辞。 | 局部替换：<br>zh：老师傅反复练习，每次尝一口、听人评价、差了就调一调，才练出来。<br>en：A seasoned cook develops that feel through practice, tasting, feedback, and adjustments. |
| l25 | 双语 | 建议 | **R：未解决。**尝味道、听评价是反馈，不一定是在对照唯一的正确标签；直接等同「正确答案」会混淆反馈与监督学习标签。 | 局部替换：<br>zh：尝一口、听评价，就是检查做得怎么样；差了就调，这就是学习。<br>en：Tasting and feedback check how it turned out. Adjusting when it's off is learning. |
| l27 | 双语 | 建议 | **R：未解决。**作者调整了图形，但「才知道它是真会认了」仍说得偏满。测试集估计新样本表现，不能单凭一次考试证明模型掌握了可靠规律。[教材§5.2](https://www.deeplearningbook.org/contents/ml.html) | 末两句替换：<br>zh：为什么这样分？要检验它能不能认出训练时没见过的新题。<br>en：Why split it this way? To test how well it handles examples it never trained on. |
| l32 | 双语 | 建议 | 新发现：本实验同时改变样本数量和抽到的内容，没有单独检验“种类更全”的作用；「越多、越全」不宜写成两个因素分别得到验证。 | 中间一句替换：<br>zh：这次实验里，例子增加后，考试成绩提高了。<br>en：In this experiment, scores improved with more examples. |
| l33 | 双语 | 记录 | **R：未解决。**「连人看了都要犹豫」仍未登记，也没有人工辨认记录；模型认错不能直接证明人的表现。 | 删除末句。 |
| l35 | 双语 | 建议 | **R：未解决。**C04已区分预测概率与正确率，口播及登记画面仍只写「把握／96%是3」。宜首次出现就明确是模型估计；概率是否可靠需要校准证据。[scikit-learn概率校准文档](https://scikit-learn.org/stable/modules/calibration.html) | zh：这个模型也报预测概率。这张图，它给「三」96%；这不是实测正确率。<br>en：Our model also assigns probabilities. Here, it gives three 96%. That's its estimate, not measured accuracy.<br>上屏：zh「模型预测：3，96%」；en「Model prediction: 3, 96%」。 |
| l38 | 双语 | 记录 | **R：已解决。**现稿承认模型能从数据学到知识，只说流畅不保证正确，已消除“生成机制排斥事实知识”的误导；与论文的事实问答评估相容。[GPT-3论文§3.2](https://arxiv.org/html/2005.14165v4#S3.SS2) | 保留。 |
| l45 | 双语 | 建议 | **R：未解决。**原报道指2023年1月这个统计月份的月活估计；「每个月就有」容易扩大成持续多月的结论。英文宜保留 active。[Reuters原稿转载](https://www.marketscreener.com/news/latest/ChatGPT-sets-record-for-fastest-growing-user-base-analyst-note-42873811/) | zh：ChatGPT 上线约两个月，月活跃用户估计达到一亿。<br>en：About two months after launch, ChatGPT had an estimated 100 million monthly active users. |
| l47 | zh | 记录 | **R：已解决。**现稿明确是英文 women's，并采用「女子国际象棋社社长」，与登记画面一致。没有扩大成“中文简历出现女子就扣分”。[Reuters原页面存档PDF，第2页](https://jlucasmckay.bmi.emory.edu/global/bmi510/Reference/hiring-bias.pdf) | 保留。 |
| l51 | 双语 | 建议 | **R：未解决。**封闭十分类模型不能输出“非数字”成立；「小孩会说」仍是没有来源的儿童表现断言，C20只能支持模型这一侧。 | zh：它只在十个数字里比较。人可以说「不是数字」，这个模型只能选数字。<br>en：It compares only ten digits. A person can reject the input; this model must choose a digit. |
| 全片 | 双语 | 记录 | **R：未解决，存疑。**C01–C06、C19、C20仍只有断言说明，没有本轮运行输出。能够检查数字之间的一致性，不能确认37%、88%、97%、96%、92%、81%以及错题身份确实由本轮模型产生。 | 核验状态替换为：**「待对照本轮运行输出核实」**。核实时提供模型配置、划分与抽样种子、20次成绩和中位数、探针样本及完整概率输出；暂不要求替换口播数字。 |
| 全片 | 双语 | 记录 | **R：未解决，台账覆盖仍有缺口。**l24–l25未登记；l56–l57未挂到C13；l19公众认知、l33人工辨认、l51儿童表现仍无证据。C19把儿童认知和模型实验放在同一个实验来源下，来源不能覆盖整条。 | 台账补记：**「l24–l25：虚构做菜类比，非实证案例」**；C13增加l56、l57；C19儿童部分另列来源或注明类比。其余采用对应行替换稿。 |

**逐项核查证据与边界**

- **C01、C07：**官方文档确认 `load_digits` 为1797张、每张8×8，是UCI原数据的测试集；UCI完整数据有5620条，不能混称完整UCI数据只有1797张。现稿说「一套公开图片」，没有犯这个错误。作者、1998年及CC BY 4.0也与UCI页面一致；300／1497的本片重新划分仍待运行证据。[scikit-learn数据说明](https://scikit-learn.org/stable/datasets/toy_dataset.html#optical-recognition-of-handwritten-digits-dataset)、[UCI原始页面](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)
- **C02、C03：**台账明确37%与88%为20次抽样成绩的中位数，97%为全部1497张训练的一次结果；画面脚注也登记了这一差别。300题错10题对应96.67%，四舍五入97%，算术一致。十类**均匀随机猜测的期望准确率**是10%，不是每次瞎猜恰好答对10%。
- **C04–C06、C20：**96%、92%、81%归属于本期逻辑回归模型，没有错归到所有AI。十类概率归一化与“没有非数字输出项”的解释成立，但归一化本身不能证明概率经过校准；具体样本输出仍存疑。
- **C08、C09、C16：**“过去常要几年”、从已知结构和序列资料学习，以及Hassabis、Jumper共同分享2024年化学奖的一半，均与诺奖科普材料一致；另一半属于Baker。讲稿没有把预测结构说成实验测定结构，也没有把团队说成只有两名作者。官网正文抓取受限，另核对了大学托管的官方原版PDF。[诺奖科普原版PDF](https://www.bu.edu/aldolase/biochemistry/html_docs/popular-chemistryprize2024-4.pdf)
- **C10：**一亿是UBS引用Similarweb数据作出的**2023年1月月活估计**，不是注册人数、当前人数或OpenAI官方统计；现稿保留“估计”是对的，时间措辞问题见l45。[Reuters原稿转载](https://www.marketscreener.com/news/latest/ChatGPT-sets-record-for-fastest-growing-user-base-analyst-note-42873811/)
- **C11：**十年间收到的简历、大多来自男性、惩罚women's及后来放弃项目，均能在Reuters原报道找到。现稿保留「据路透社」「曾想用」，没有说该工具已实际淘汰大量女性，也没有把偏见说成唯一关停原因。[Reuters存档PDF](https://jlucasmckay.bmi.emory.edu/global/bmi510/Reference/hiring-bias.pdf)
- **C12–C15、C17：**AI包含机器学习、深度学习属于机器学习、规则下棋程序也可属于AI，以及“模型是学出来的认法”，用于本片范围均可成立。C14引文的省略未改变原意；C13的监督学习引文与教材相符。C15所摘“simply by predicting what comes next”确实在论文引言，且已注明词元机制是概括。l37口播说“词”是简化，台账登记的“严格说是词元token”应实际保留上屏。[教材第1章](https://www.deeplearningbook.org/contents/intro.html)、[教材第5章](https://www.deeplearningbook.org/contents/ml.html)、[GPT-3论文](https://arxiv.org/html/2005.14165v4)
- **C18、C19、C21–C23：**C18泛化引文、C22过拟合引文均能在教材§5.2对上；C21没有再把能力与缺陷只归因于数据；C23已明确是假设示例。C19的样本门槛和儿童来源问题见表。l58作为过拟合的提问式预告可保留，但“新题表现差”也可能来自分布变化，不能在下期当作唯一判据。[教材§5.2](https://www.deeplearningbook.org/contents/ml.html)
- **专业概念专项：**本轮没有出现欠拟合、验证集、正则化或捷径学习的定义，未发现这些概念被混用；l27的“考试题”对应测试集。是否曾用考试成绩选模型或调参数，四份材料无法确认，需在实验复核时检查。
- **R处理结论：**上一轮事实核查条目中没有明确的「不采纳」论证。字号、插图和标签调整不能作为事实意见已解决的证据；未专门修改的项目已逐条保留为未解决。

**最重要的3条**

1. 补齐本轮实验输出；目前只能确认部分算术与登记口径一致。
2. 消除“无人写过规则”“上百个才行”“考试就知道真会了”等超出证据的表述。
3. 首次出现概率时明确“模型估计”，并把ChatGPT用户数收紧为特定月份的月活估计。

**做得好的、别改掉的**

1. l38同时保留“能学到知识”和“流畅不保证正确”，准确且易懂。
2. 诺奖归属与份额、Amazon报道归属及women's原词均处理得谨慎。
3. 用具体错题和字母A解释模型局限，并明确本期只讨论机器学习这一圈。

其他：无。