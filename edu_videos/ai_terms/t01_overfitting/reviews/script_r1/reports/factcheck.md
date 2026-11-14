结论：**需修改后复核。** 主要问题是把过拟合等同于“完全没学会规律”、混淆捷径学习的机制，以及医院识别数字缺少适用范围。

本次仅读取指定三份仓库材料，并核对相关原始文献；未读取其他审稿报告、未修改文件。画面文字仅核查 `claims.json` 的 `screen` 字段，未审实际成片。表中替换稿按对应句子或片段替换。

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l02 | 双语 | 建议 | 仅凭“旧数据好、新数据差”，还不能排除程序问题或数据分布变化，直接确诊过拟合过满。 | zh：这可能不是程序出错，而是过拟合。<br>en：One possible culprit is overfitting. |
| l09 | 双语 | 必改 | “背下来了，却没学会规律”把极端类比当成定义。过拟合可以同时学到规律和噪声，也不要求逐点记忆。[概念依据](https://www.deeplearningbook.org/contents/ml.html) | zh：先给一句话：过拟合，就是太贴合练习题，反而做不好同类新题。下面看个小实验。<br>en：Overfitting means fitting practice data too closely to do well on similar new data. Let's see a small experiment. |
| l13 | 双语 | 必改 | 台账使用 MSE，解说却只说“距离”，未说明是纵向误差的平方平均；“对不上练习题”也容易让观众把不穿过所有点当作欠拟合，与 l14 冲突。 | zh：这里的误差，是预测与实际高度差平方的平均值。第一种只会画直线，连整体弯曲趋势都抓不住，这叫欠拟合。<br>en：Here, error means the average squared difference between predicted and actual heights. Model one draws a straight line and misses even the overall bend. That's underfitting. |
| l19 | en | 建议 | “twenty times higher than”存在倍数歧义，中文“是……二十多倍”和画面倍率表达更明确。 | 仅替换末句：Its test error is over twenty times model two's. |
| l21 | 双语 | 建议 | “一眼就能看出”“更危险”都是无条件判断；可直接解释为何容易漏检。 | zh：欠拟合，练习题就做不好；过拟合容易漏看，因为训练成绩可能很好。<br>en：Underfitting shows up on practice data. Overfitting can be harder to spot because training scores may look excellent. |
| l27 | 双语 | 必改 | 背训练样本与依赖沙发背景不能说成“同一件事”；捷径可以是一条很简单的规则，不是“被允许记得太多”。[原文区分](https://arxiv.org/html/2004.07780v4) | zh：两个例子都用了不可靠的线索，但机制不同。认猫的例子是走捷径，不一定是记得太多。<br>en：Both rely on unreliable clues, but the mechanisms differ. The cat example uses a shortcut; it needn't involve remembering too much. |
| l28 | 双语 | 建议 | 旁白容易听成“连续三百次逐步加复杂度”；画面却说“三百次实验的中位数”，统计口径没有讲清。具体重复方式仍须复算确认。 | 若确为每种复杂度重复三百次：<br>zh：回到实验。每种复杂度重复三百次，看两种误差的中位数。<br>en：For each model complexity, we run 300 trials and compare the median training and test errors. |
| l30 | 双语 | 必改 | 测试误差上升不能证明模型完全没学到规律；“只有中间才真正学会”把程度差别说成有无之分。 | zh：这次实验里，考试误差先降后升，中间那段预测新点最好。<br>en：In this experiment, test error falls, then rises. The middle range predicts new points best. |
| l34 | 双语 | 建议 | 十个高度只能在横坐标已知时确定这十个点；压缩类比漏掉了共享条件。 | zh：横坐标已知，只需记十个高度。<br>en：With the horizontal positions known, we need only store ten heights. |
| l36 | 双语 | 必改 | 十个系数足以插值，不意味着“不用找规律，所以没找”。参数数量不能证明模型完全没有学到规律。 | zh：第三种有十个数字，能穿过全部十个点，但也跟着噪声拐弯，预测新点就差了。<br>en：Model three uses ten numbers to pass through all ten points, but it follows the noise too, hurting predictions on new points. |
| l39 | 双语 | 必改 | 画面“5000 万……1152……＝过拟合”把数量悬殊写成充分判据；原文依据还包括选中了无关的季节性关联。另须限定为**最初版本**，指标是流感样疾病就诊比例。[Lazer 原文](https://cdanfort.w3.uvm.edu/csc-reading-group/lazer-flu-science-2014.pdf) | zh：谷歌曾用搜索词估算流感样症状的就诊比例。初版从五千万个词里挑选，去贴合一千多个历史数据点。研究者认为它过拟合了：既在测流感，也在测冬天。<br>en：Google used searches to estimate the share of visits for flu-like illness. Its initial version selected from 50 million terms to fit about 1,100 data points. Researchers criticized its overfitting: it tracked both flu and winter.<br>画面将“＝过拟合”替换为“（初版）”。 |
| l40 | 双语 | 建议 | 100/108 核实无误，但它没有直接证明新旧版本“没好多少”，也不能单独归因于过拟合。 | 仅替换开头：<br>zh：后来的版本仍有偏差：<br>en：Later versions still had problems. |
| l41 | 双语 | 必改 | 99.95% 和 99.98% 分别对应 NIH、Mount Sinai；同一医院识别实验的 IU 为 **95.59%**。目前“几乎百分之百认出来自哪家医院”及无范围的“99.9%”扩大了适用范围。[Zech 结果](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1002683) | 将医院识别部分替换为：<br>zh：胸片带着医院“指纹”：另训模型识别 NIH 和西奈山的片子，准确率超99.9%。<br>en：X-rays carried hospital fingerprints: a separate model identified NIH and Mount Sinai scans with over 99.9% accuracy.<br>画面数字可改为“≈100%”，并与上述医院范围同屏。 |
| l42 | 双语 | 建议 | 换算正确，但建议点明是一次研究的结果，避免听成该系统在所有场景中的固定误判率。 | zh：还有个黑色素瘤识别系统：加上皮肤标记后，研究中一半多的良性痣被它误判为癌。<br>en：In one study, adding skin markings made a melanoma detector label over half the benign moles as cancer. |
| l43 | 双语 | 必改 | “学到的却是巧合，不是规律”排除了同时利用有效特征的可能；也漏掉捷径学习可以通过同分布新数据测试这一关键区别。皮肤论文对训练中如何形成这种依赖仍保留不确定性。[捷径定义](https://arxiv.org/html/2004.07780v4)、[皮肤论文讨论](https://jamanetwork.com/journals/jamadermatology/fullarticle/2740808) | zh：这还涉及捷径学习：模型可能依赖医院或笔迹等线索。它不同于过拟合，同类新题也能考好，换个环境才露馅。<br>en：These cases point to shortcut learning: relying on cues such as hospitals or ink marks. Unlike ordinary overfitting, shortcuts can pass tests on similar new data and fail when conditions change. |
| l47 | 双语 | 必改 | 正则化不等于让模型“没有能力记住每个点”，也不保证无法插值；它可以通过软约束改变模型偏好。[正则化定义](https://www.deeplearningbook.org/contents/regularization.html) | zh：第三，用正则化约束学习，比如惩罚过度复杂的拟合，减少追着噪声跑。<br>en：Three: use regularization, such as penalizing overly complex fits, to discourage fitting noise. |
| l49、l50 | 双语 | 必改 | 片尾再次把“记忆”和“学到规律”写成互斥，强化了 l09 的错误定义。 | 两句合计替换：<br>zh：过拟合，就是太贴合练习题，／反而做不好同类新题。<br>en：Overfitting means fitting practice data too closely／to do well on similar new data. |
| 全片 | 双语 | 必改 | **台账句号错位。** C04–C08 仍指向 l35–l39，实际案例已在 l39–l43；C01–C03 也存在错位，不能据此追溯当前讲稿。 | `lines` 建议替换为：C01＝`["l15","l19"]`；C02＝`["l28","l29","l30"]`；C03＝`["l10","l34","l35","l36"]`；C04–C08 分别＝`["l39"]`、`["l40"]`、`["l41"]`、`["l42"]`、`["l43"]`。 |
| 全片 | 双语 | 必改 | **事实登记不全。** 未独立登记的包括：过拟合定义、训练数据与噪声、误差及欠拟合、六个测试点与测试集、过拟合信号、压缩观点，以及验证集／增加数据／正则化。现有 C01–C03 不能覆盖这些概念。 | 台账至少补录对应 l09–l13、l17、l21、l27、l31、l33、l37、l45–l47、l49–l50 的事实及依据；“学习是压缩”应标为解释视角。旁白可分别缩为：zh“换个角度：把学习想成压缩。”；en“One useful lens is learning as compression.” |
| 全片 | 双语 | 记录 | **存疑：C01–C03 的实验结果未能独立复算。** 给出的断言只能检查近零训练误差、倍率落在20至30之间、系数数量；不能单独证明画面的1.80、25倍，以及三百次中位数曲线的形状。 | 暂不改数字，也不标为已核实。核实方式：用当前实验代码输出各模型 MSE、未取整倍率、训练／测试点数及各复杂度的三百次中位数，并逐项比对画面。代码不在本次授权材料内，未读取或运行。 |

**已核查、没有发现错误的部分**

- **C01–C03：** 三次多项式四个系数、九次多项式十个系数的计数正确；十个横坐标互异的点可由至多九次多项式插值。实际点位、误差及重复实验结果仍属上述“存疑”，不能把数学上成立当作运行结果已验证。
- **C04：** 五千万个候选搜索词、1152个数据点与原文一致；“一千多个／about 1,100”是合理约数。原文的 *cases* 在此指数据点；“part flu detector, part winter detector”译为“既测流感，也测冬天”没有擅自赋予各半比例。[原文](https://cdanfort.w3.uvm.edu/csc-reading-group/lazer-flu-science-2014.pdf)
- **C05：** 原文图注明确支持2011年8月21日至2013年9月1日、108周中100周高估；单位是**周**，比较基准是 CDC 估计，并非“100个错误病例”。[原文图注](https://cdanfort.w3.uvm.edu/csc-reading-group/lazer-flu-science-2014.pdf)
- **C06：** “另训一个模型”归属正确；肺炎联合模型的内部测试 AUC 0.931、外部 IU 测试 AUC 0.815也正确。它们是 AUC，不是准确率；当前没有把二者混称。[原文](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1002683)
- **C07：** 特异度84.1%→45.8%，对应良性痣假阳性率15.9%→54.2%，取整16%→54%正确；分母是107个良性痣，判别阈值为0.5，不是全部130个皮损。研究比较了同一批良性痣加标记前后，l42描述标记影响有实验依据。[原文方法与结果](https://jamanetwork.com/journals/jamadermatology/fullarticle/2740808)
- **C08：** 台账引用的捷径定义与原文一致；原文确实将胸片案例作为例子，并区分了训练集过拟合与同分布测试仍能通过的捷径。问题在讲稿的进一步概括，见 l27、l43。[原文](https://arxiv.org/html/2004.07780v4)
- **l45：** 验证集用于选模型、测试集留到最后的职责分工正确；主动说明演示曾用考试挑模型，也避免了把演示操作当成正式评估流程。[概念依据](https://www.deeplearningbook.org/contents/ml.html)

**最重要的 3 条**

1. 改掉“背下来＝完全没学会规律”及“正则化＝不能记忆”的绝对表述，尤其是开头和片尾。
2. 保留过拟合与捷径学习的区别：后者可能连同类新题也考得很好。
3. 限定医院识别数字的范围，修正台账句号；实验数值在复算前保持“存疑”。

**做得好的、别改掉的**

1. “另训一个模型”已纠正模型归属，“很可能有一部分”保留了推断边界。
2. *part…part* 没译成“一半……一半”；良性痣误判率的换算也正确。
3. l45明确区分验证集与最终测试集，是本稿值得保留的重要澄清。