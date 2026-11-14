**结论：仍有必改项，暂不建议通过事实核查。** 最明确的问题是统计口径冲突、误差定义不一致，以及片尾仍把过拟合等同于“只记忆、没学到规律”。

仅审阅指定四份材料及其原始出处；未修改文件，未读取其他审稿报告。画面核查限于 `claims.json` 登记的文字，未查看实际画面或运行实验代码。表中 **R** 标明上一轮事实核查问题的复核结果，旧句号均注明对应关系。

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l02 | 双语 | 建议 | **R：未解决（旧 l02）。** 中文“很多时候”有所缓和，但英文第二句仍直接确诊。仅凭旧数据好、新数据差，不能排除分布变化等原因；“经常如此”的频率也无登记依据。 | zh：可能不是程序出错，而是过拟合。<br>en：One possible culprit is overfitting. |
| l09 | 双语 | 记录 | **R：已解决（旧 l09）。** 已改成过度贴合偶然细节，允许模型同时学到规律与噪声；l10 明确标为比方。 | 保留。 |
| l14 | 双语 | 必改 | **R：未解决（旧 l13 的误差口径）。** “点到线的距离”通常指最短距离；这里需要的是纵向残差，汇总指标又是 MSE。距离与距离平方的平均不能混用，尤其后面要报具体倍率。作者“不采纳”的理由不成立：可以省公式，不能换指标。[教材 §5.1.4](https://www.deeplearningbook.org/contents/ml.html) | zh：第一种只会画直线。这里的误差，是高度差平方的平均。<br>en：Model one draws a straight line. We measure error by averaging squared differences in height. |
| l15 | 双语 | 建议 | **R：未解决（旧 l13 的欠拟合解释，已有改善）。** 已不再把“不穿过每点”当欠拟合，但“误差压不下来”仍可能被理解为完全无法降低。关键是直线无法充分拟合这里的弯曲趋势。 | zh：直线连整体弯曲的走势都抓不住，这叫欠拟合。<br>en：The line misses even the overall bend. That's underfitting. |
| l21 | en | 记录 | **R：已解决（旧 l19）。** 已用 “times model two’s”，消除了 “times higher than” 的倍数歧义。数值本身另见实验存疑项。 | 保留。 |
| l22 | 双语 | 建议 | 新增的“随机，所以不会重演”过于绝对。随机偏差可能偶然重复；问题是记住本次偏差不能可靠预测新样本。 | 替换中间一句：<br>zh：可随机偏差，不能可靠地预测新题。<br>en：But those random wobbles won't reliably predict new points. |
| l23 | 双语 | 必改 | **R：改出了新问题（旧 l21）。** “很容易发现／更难察觉”仍缺条件；新增“练习误差为零”置于一般性总结中，容易成为过拟合的必要条件。过拟合不要求零训练误差。 | zh：欠拟合，练习题就做不好；过拟合容易漏看，因为练习成绩可能很好。<br>en：Underfitting shows up on practice data. Overfitting can be harder to spot because training scores may look excellent. |
| l28、l30 | 双语 | 记录 | **R：已解决（旧 l27）。** 已明确两个例子的机制不同，并将沙发线索归为捷径学习，不再说成同一种记忆过量。 | 保留“相近、但不一样”和捷径学习名称。 |
| l31 | 双语 | 必改 | **R：改出了新问题（旧 l28）。** 重复方式讲清了，但旁白改成“平均／average”，C02 的 claim 和 screen 仍明确是“中位数”。这是现有材料中的直接冲突；不能将两种统计量互换。 | 若以当前台账口径为准：<br>zh：回到实验。换三百组随机点，每组都拟合不同复杂度，再比较两种误差的中位数。<br>en：We fit each model complexity to 300 random datasets, then compare median training and test errors.<br>最终须以代码实际计算口径核定。 |
| l33 | 双语 | 记录 | **R：已解决（旧 l30）。** 已删除“只有中间才真正学到规律”，改为预测成绩比较；前句“回到实验”限定了语境，没有将 U 形曲线明说成普遍定律。 | 保留。 |
| l37 | 双语 | 建议 | **R：未解决（旧 l34）。** 只存十个高度能还原十个点，仍以横坐标已知为前提；现句未交代。 | zh：横坐标已知，只需记十个高度。<br>en：With horizontal positions known, store the ten heights. |
| l39 | 双语 | 记录 | **R：已解决（旧 l36）。** 已删除“参数够多，所以没有找规律”的推断，改为拟合噪声并损害本次新点预测。 | 保留；具体实验结果仍须复算。 |
| l40 | 双语 | 必改 | **新增问题。** “恰好／exactly”保证了噪声被完整剔除、留下的全是规律，C13 原文不支持。MDL 还要计入模型之外的残差编码，并不是把噪声直接扔掉；四个参数的近似描述也不是十个点的无损压缩。[Grünwald 第 1 章 §1.5](https://homepages.cwi.nl/~pdg/book/chapter1.pdf) | zh：目标是简洁地抓住规律，而不是追着噪声跑。<br>en：The goal is to capture patterns compactly, without chasing noise. |
| l42、l44 | 双语 | 必改 | **R：未解决（旧 l39，部分已解决）。** “最初版本”、数据点口径及去掉画面等号均已解决；但指标仍笼统写“流感”，遗漏了**类流感就诊占比**。“候选词远多于数据，就像十个参数配十点”也继续混淆候选特征搜索与插值自由度。应补回季节性假关联这一实质依据。[Lazer 原文](https://cdanfort.w3.uvm.edu/csc-reading-group/lazer-flu-science-2014.pdf) | 两句合计缩短替换，l43 保留：<br>zh l42：谷歌曾用搜索词，估算类流感就诊占比。<br>zh l44：它挑中了和流感无关的季节性线索。研究者说，这是过拟合：它既在测流感，也在测冬天。<br>en l42：Google used searches to estimate the share of visits for flu-like illness.<br>en l44：It picked up unrelated seasonal clues. Researchers called this overfitting: it tracked both flu and winter. |
| l45 | 双语 | 记录 | **R：已解决（旧 l40）。** “后来的版本也有偏差”不再声称新旧版本改善幅度，也没有把 100／108 周全部归因于过拟合。 | 保留。 |
| l47 | 双语 | 记录 | **R：已解决（旧 l41）。** “单独训练一个模型”“其中两家医院”同时限定了模型身份和数字范围；C06 也列明 NIH、Mount Sinai。 | 保留；数字与范围应同屏呈现。 |
| l49 | 双语 | 记录 | **R：已解决（旧 l42）。** 已限定“研究中／In one study”和“有标记的良性痣”，没有推广为所有场景的固定误判率。 | 保留。 |
| l50 | 双语 | 建议 | **R：未解决（旧 l43，主要问题已修复）。** 同类新数据也能考好的区别已补上，但“后两个……叫捷径学习”仍把解释直接写成定论；皮肤论文明确保留依赖形成机制的不确定性。“only fail／才露馅”也过满。捷径解释合理，宜标为推断。[Winkler 讨论](https://jamanetwork.com/journals/jamadermatology/fullarticle/2740808) | zh：后两个例子提示了捷径学习：模型依赖医院或笔迹等线索。同类新题可能考好，换个环境却失灵。<br>en：Those cases suggest shortcut learning: relying on hospital clues or ink marks. Such shortcuts can work on similar new data yet fail elsewhere. |
| l52、l53 | 双语 | 记录 | 验证集用于选择模型、测试集留到最后，概念正确；明确承认演示用了测试成绩挑模型，也避免观众照搬错误流程。C10 的出处节号需更正，见下方台账项。 | 讲稿保留。 |
| l55 | 双语 | 记录 | **R：已解决（旧 l47）。** 改为复杂度惩罚，允许软约束，不再声称正则化让模型失去插值能力。 | 保留。 |
| l57、l58 | 双语 | 必改 | **R：未解决（旧 l49）。** 仍将记忆和学习规律写成互斥，并用“就是／is”当定义。作者“不采纳”的理由不成立：片尾要求观众记住、引用，恰好更需要独立成立；前面的精确定义不能抵消结尾的错误概括。 | zh l57：过拟合，就是太贴合练习题，<br>zh l58：反而做不好同类新题。<br>en l57：Overfitting means fitting practice data too closely<br>en l58：to generalize well. |
| 全片 | 双语 | 记录 | **R：已解决（旧“台账句号错位”）。** C01—C13 已登记的句号均能对应本轮相关内容；没有发现上一轮那种整段错位。 | 保留现有对应关系，修改后同步更新。 |
| 全片 | 双语 | 必改 | **R：未解决（旧“事实登记不全”）。** C09—C13 补齐了许多概念，但仍遗漏：l11 的训练数据定义、l12 的噪声、l14 的误差口径、l19 的六个测试点与测试集定义，以及 l57—l58 的最终定义。l16／l20 的拟合及预测比较也未明确登记。 | 台账新增或扩展条目：`训练数据用于拟合；测试数据用于评估未见样本表现；本实验有六个测试点；误差指标为均方误差；模型②在本次测试中误差最低。` 噪声条目应登记本实验的生成方式；修订后的 l57—l58 加入 C09。 |
| 全片 | 双语 | 记录 | **R：未解决，存疑（旧“C01—C03 未独立复算”）。** 现有断言不能证明画面的 1.80、25 倍、300 次统计曲线，也不能证明实际使用了六个测试点。未获本次授权读取实验代码，因此不将这些数字判为已核实。 | 数字暂不改。核实须输出当前代码的各模型 MSE、未取整倍率、点数、逐复杂度统计值及聚合方式，并与画面逐项比对。 |
| 全片 | 双语 | 记录 | **新增台账问题。** C10 引文内容正确，但所在节是 §5.3，而不是 §5.3.1；后者讲交叉验证。C13 的 quote 是改写拼接，不是逐字引文。[教材 §5.3](https://www.deeplearningbook.org/contents/ml.html)、[Grünwald 序言](https://homepages.cwi.nl/~pdg/book/preface.pdf) | C10：`§5.3`。<br>C13 quote：`the more we are able to compress the data, the more we have learned about the data`，出处补 `Preface, p. xxv`。 |

**最重要的 3 条**

1. **统一实际计算、旁白与画面的统计口径。** l31 的平均／中位数冲突必须消除；l14 应明确 MSE，否则“25 倍”容易被理解为距离的倍率。
2. **修正片尾定义。** 过拟合可以同时学到规律与噪声，不要求逐点记忆，也不要求零训练误差。
3. **收回压缩段的保证。** “恰好丢掉噪声、留下规律”超出来源，不能作为 MDL 的解释结论。

**做得好的、别改掉的**

1. 胸片案例明确区分肺炎模型与另训的医院识别模型，并限定两家医院。
2. GFT 已区分初版过拟合与后续版本估高；`part…part` 没有误译成“一半……一半”。
3. 验证集、测试集的分工，以及演示选模方式的坦白，准确且有教学价值。

**claims.json 逐条核查证据**

- **C01：存疑。** 断言只限制训练 MSE 接近零、倍率在 20—30 之间，不验证测试 MSE 为 1.80 或取整后为 25；MSE 的量纲是纵轴量纲的平方，倍率本身无量纲。
- **C02：存在明确冲突。** 台账和登记画面均写中位数，双语旁白写平均；实际聚合函数与曲线形状未独立验证。
- **C03：数学关系成立，实验实现存疑。** 三次多项式有四个系数，九次有十个；十个横坐标互异的点可由至多九次多项式插值。但本次点数、横坐标条件及拟合结果未复算。
- **C04：数字、对象和引文含义核实。** Lazer 等评论的是 GFT **初版**：候选搜索词 5000 万、拟合数据点 1152。“一千多个／about 1,100”是可接受的近似；`cases` 在此指数据点，不是患者数。`part…part` 不指定各占一半。指标与类比问题见表。[Science 原文第 1203 页](https://cdanfort.w3.uvm.edu/csc-reading-group/lazer-flu-science-2014.pdf)
- **C05：核实。** 原文图注明确给出 2011-08-21 至 2013-09-01，108 周中 100 周估高；单位是“周”，不是患者比例或误差幅度。登记引文与图注一致。[Science 原文第 1204 页](https://cdanfort.w3.uvm.edu/csc-reading-group/lazer-flu-science-2014.pdf)
- **C06：核实。** 联合 NIH／MSH 训练的肺炎模型，内部测试 AUC 为 0.931、IU 外部测试为 0.815，均不是准确率。另训的医院识别 CNN 对 NIH 为 22,050／22,062，对 MSH 为 8,386／8,388，分别约 99.95%、99.98%；IU 为 95.59%，因此限定“两家”必要。l48 保留“很可能有一部分”，与论文混杂分析相容。[Zech 原文](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1002683)
- **C07：核实。** Winkler 等研究包含 107 个良性痣、23 个黑色素瘤；固定操作点下，特异度由 84.1% 降至 45.8%。以良性痣为分母，误报率为 15.9%→54.2%，取整成 16%→54% 正确。箭头表示无标记到有标记，不是随时间变化，也不是全部皮损的错误率。[JAMA 原文与图 5](https://jamanetwork.com/journals/jamadermatology/fullarticle/2740808)
- **C08：定义引文核实。** Geirhos 等确实强调：捷径能在标准测试中表现良好，却不能迁移到更具挑战的条件；不能把它简单等同于训练样本记忆。将皮肤案例解释为捷径合理，但原研究未确定其训练形成机制，见 l50。[Geirhos 原文](https://arxiv.org/html/2004.07780v4)
- **C09：引文核实。** 除排版连字外，与教材 §5.2 原文一致；来源没有要求过拟合时训练误差必须为零，也没有要求完全没学到规律。讲稿中的偏离见 l23、l57—l58。[教材 §5.2](https://www.deeplearningbook.org/contents/ml.html)
- **C10：引文核实，节号有误。** 所录验证集段落与正文一致；l52—l53 正确体现选模与最终评估的分工。出处应为 §5.3。[教材 §5.3](https://www.deeplearningbook.org/contents/ml.html)
- **C11：引文核实。** §5.2.2 确有该正则化定义；当前曲线惩罚是合适的入门例子，没有再宣称模型必然无法记忆。[教材 §5.2.2](https://www.deeplearningbook.org/contents/ml.html)
- **C12：引文核实。** 所录句子位于 §7.4 开头。l54 的“更不容易／less likely”保留概率性，没有保证数据增多必然解决问题；作为一般建议可接受。[教材 §7.4](https://www.deeplearningbook.org/contents/regularization.html)
- **C13：观点有据，引文需修正，l40 超出依据。** 序言支持把学习与发现可压缩的规律联系起来；第 1 章同时计算模型及剩余数据的描述长度，不支持“恰好丢弃全部噪声”。[序言](https://homepages.cwi.nl/~pdg/book/preface.pdf)、[第 1 章](https://homepages.cwi.nl/~pdg/book/chapter1.pdf)

**其他：** 无。