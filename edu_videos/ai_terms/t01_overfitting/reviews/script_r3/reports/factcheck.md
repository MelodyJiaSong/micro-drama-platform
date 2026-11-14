**事实核查结论：尚有必改项，暂不建议放行。** 三个真实案例的核心数字基本准确；主要问题在误差口径、压缩类比，以及部分结论超出了证据范围。

本次只读了指定四份材料，并核对相关论文与教材原文。画面文字仅核对 `claims.json` 的 `screen` 字段；未查看成片、实验代码或运行结果，因此实验数值仍有待核实项。下表的 **R** 表示上一轮问题复核；替换文字均不长于对应原句。

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l02 | 双语 | 建议 | **R：未解决。** 英文第二句仍直接确诊；旧数据好、新数据差也可能来自分布变化。“很多时候／Often”的频率没有登记依据。 | zh：可能不是程序出错，而是过拟合。<br>en：One possible culprit is overfitting. |
| l09 | 双语 | 记录 | **R：已解决。C09。** 定义聚焦于偶然细节损害新数据表现，没有把“完全没学到规律”作为必要条件；与教材的过拟合解释相容。[教材 §5.2](https://www.deeplearningbook.org/contents/ml.html) | 保留。 |
| l11、l12、l13、l19 | 双语 | 记录 | **C15：概念基本正确。** 训练用于拟合，测试用于评估未见样本；随机偏差作为本实验噪声的解释可接受。教材引文确实说明测试样本与训练样本分开收集，但不能单独证明本实验的噪声生成方式和六点数量。[教材 §5.2](https://www.deeplearningbook.org/contents/ml.html) | 概念表述保留；实验事实见末尾存疑项。 |
| l14 | 双语 | 必改 | **R：未解决，纵向方向已解决。C14。** 中文“汇总”未说清指标；英文 **added up** 明确说成距离相加，而台账是高度差平方的平均。作者“不采纳平方平均，因为过细”的理由不足：可以省公式，不能换计算口径；台账也不能抵消错误口播。 | zh：第一种只会画直线。这里的误差，是每个点与曲线高度差平方的平均。<br>en：Model one draws a straight line. Here, error is the average squared difference in height between points and predictions. |
| l15 | 双语 | 建议 | **R：未解决，但已无“不穿点就是欠拟合”的错误。C09。** “误差压不下来”容易理解为完全不能降低；实际是无法降得足够低。 | zh：直线连整体弯曲的走势都抓不住，这叫欠拟合。<br>en：The line misses even the overall bend. That's underfitting. |
| l21 | en | 记录 | **R：已解决。C01。** 倍数表达使用 “times model two’s”，没有“高出多少倍”的歧义；具体倍率尚未独立复算。 | 保留倍率句式。 |
| l22 | 双语 | 建议 | **R：未解决。** 随机不等于绝不重复；关键是本次偏差不能可靠预测新样本。 | 替换中间一句：<br>zh：可随机偏差，不能可靠地预测新题。<br>en：But those random wobbles won't reliably predict new points. |
| l23 | 双语 | 建议 | **R：未解决，部分已解决。** “比如这里／Here”已消除零训练误差是必要条件的暗示；但“欠拟合很容易发现”仍被写成无条件判断。 | zh：欠拟合，练习题就做不好；过拟合容易漏看，因为练习成绩可能很好，比如这里误差是零。<br>en：Underfitting shows up on practice data. Overfitting can be harder to spot because training scores may look excellent—as they do here. |
| l28 | 双语 | 记录 | **R：已解决。C08。** “相近、但不一样”明确区分记住噪声与利用沙发线索，没有把两种机制等同。 | 保留。 |
| l31 | 双语 | 记录 | **R：已解决，限措辞冲突。C02。** “通常／typical”不再与台账和画面的“中位数”冲突。是否实际抽样三百组并取中位数，仍需运行结果证明。 | 保留。 |
| l33、l35 | 双语 | 记录 | **R：已解决。C02、C09。** 前面的“回到实验”限定了语境；现在比较预测成绩，没有声称只有中间复杂度才会学到规律，也没有主张越简单越好。 | 保留；曲线数值另核实。 |
| l37 | 双语 | 建议 | **R：未解决。C03。** 只存十个高度就能还原十个点，需要横坐标已知。 | zh：横坐标已知，只需记十个高度。<br>en：With horizontal positions known, store the ten heights. |
| l39 | 双语 | 必改 | **R：改出了新问题。C03、C13。** 原先“参数多就没学规律”的推断已删，但新增“十个数字存十个点，等于没有压缩”仍把参数数量当成编码长度。MDL 比较描述所需的比特数，还要考虑精度及残差；不能仅凭十对十判定没有压缩。[Grünwald §1.5](https://homepages.cwi.nl/~pdg/book/chapter1.pdf) | zh：第三种用十个数字，让曲线穿过全部十个点。它把每个点都拟合得太准，连随机偏差也记了下来。<br>en：Model three uses ten numbers to pass through all ten points. It fits every point exactly, including its random deviation from the underlying pattern. |
| l40 | en | 建议 | **R：未解决，中文已解决。C13。** 中文已改成目标式的“要留住规律、少记噪声”；英文仍说直接留下规律、排除噪声，强于中文，也容易让人误以为压缩保证分离两者。[Grünwald §1.5](https://homepages.cwi.nl/~pdg/book/chapter1.pdf) | en：Good compression aims to capture patterns without chasing noise. Squeeze too hard, like the straight line, and you lose the pattern, too. |
| l42、l43 | 双语 | 记录 | **R：已解决，指指标和数据点口径。C04。** 原文确为最初版本、五千万候选搜索词、1,152 个数据点；cases 没有被译成病人。口播“一千多／about 1,100”与画面精确值相容；流感样就诊占比也已补回。[Lazer 原文，第 1203 页](https://cdanfort.w3.uvm.edu/csc-reading-group/lazer-flu-science-2014.pdf) | 保留。 |
| l44 | 双语 | 必改 | **R：未解决，翻译部分已解决。C04。** 候选搜索词数量与多项式自由参数数量不是同一口径，“比十个数字配十个点还夸张”继续引导观众直接比较。应讲清季节性假关联，而非用两种不同数量推出程度比较。“既……也……”没有误译成各占一半，正确。[Lazer 原文](https://cdanfort.w3.uvm.edu/csc-reading-group/lazer-flu-science-2014.pdf) | zh：有些搜索词只是随季节变化，并不真正反映流感。研究者说，这是过拟合：它既在测流感，也在测冬天。<br>en：Some search terms tracked the season rather than flu itself. Researchers called this overfitting: it tracked both flu and winter. |
| l45 | 双语 | 记录 | **R：已解决。C05。** 原文窗口为 2011-08-21 至 2013-09-01，108 周中 100 周估高；没有说高了 100%，也未将这些偏差全部归因于最初版本的过拟合。[Lazer 图注，第 1204 页](https://cdanfort.w3.uvm.edu/csc-reading-group/lazer-flu-science-2014.pdf) | 保留。 |
| l46 | 双语 | 记录 | **C06：已核实。** NIH 与 MSH 联合训练的肺炎模型，联合内部测试 AUC 为 0.931，IU 外部测试为 0.815；“成绩下降”准确，没有将 AUC 误称为诊断准确率。[Zech 结果](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1002683) | 保留。 |
| l47 | 双语 | 记录 | **R：已解决。C06。** 是另训的医院识别 CNN；NIH 为 22,050/22,062，MSH 为 8,386/8,388，分别约 99.95%、99.98%。研究还包含 IU，不能把 99.9% 推广至全部医院；本轮“两家医院的片子”限定正确。[Zech 结果](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1002683) | 保留；画面继续同时呈现模型身份和范围。 |
| l48 | 双语 | 必改 | **新增口径问题。C06。** 34.2%、1.2%、1.0% 是各研究数据集中的肺炎阳性标签比例，并非各医院全部就诊病人的患病比例。“认医院有助于预测”的推断有依据，但分母和标签口径需要收窄。[Zech 方法与结果](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1002683) | 只替换首句：<br>zh：各院数据中，标成肺炎的比例差很大。<br>en：Pneumonia label rates differed widely across datasets. |
| l49 | 双语 | 建议 | **R：已解决，指数值与研究范围；新增机制解释需降调。C07。** 107 个良性痣在既定阈值下的误判率由约 15.9% 升至 54.2%，画面 16%→54% 正确。原文却明确说机制不清，只提出可能解释；“很可能／likely”比原文更确定。中文“痣上”也宜改为“痣旁”。[Winkler 结果与讨论](https://jamanetwork.com/journals/jamadermatology/fullarticle/2740808) | zh：还有一个识别黑色素瘤的系统：医生常在可疑的痣旁画标记，它可能把标记当成了线索。研究中，画了标记的良性痣，一半多被它判成了癌。<br>en：An AI that detects melanoma, a skin cancer, may have picked up doctors’ ink marks around suspicious moles. In one study, it flagged over half the marked benign moles as cancer. |
| l50 | 双语 | 必改 | **R：未解决。C08。** 同类新数据可能表现好，这一点正确；“换个环境**才**／**only** fail”却把环境变化写成失败的必要条件。两个案例的共同解释也不宜抹去皮肤研究保留的机制不确定性。[Geirhos 原文](https://www.allpsych.uni-giessen.de/rauisch/readings/Geirhos_et_al.2020.pdf)、[Winkler 讨论](https://jamanetwork.com/journals/jamadermatology/fullarticle/2740808) | zh：后两个例子提示了捷径学习：模型依赖医院或笔迹等线索。同类新题可能考好，换个环境却失灵。<br>en：Those cases suggest shortcut learning: relying on hospital clues or ink marks. Such shortcuts can work on similar new data yet fail elsewhere. |
| l52、l53 | 双语 | 记录 | **R：已解决，指概念。C10。** 验证集选择模型、测试集留到最后，准确；承认演示按测试成绩选择，避免将演示当成规范流程。教材支持这一区分，但不能证明本次演示实际怎样选模。[教材 §5.3](https://www.deeplearningbook.org/contents/ml.html) | 讲稿保留；本次选模过程列入实验核实材料。 |
| l54 | 双语 | 记录 | **C12：已核实。** “更多、更多样”“不容易／less likely”是概率性改善，没有保证根除过拟合。所登记英文引文可在教材 §7.4 找到；台账应直接链接该章。[教材 §7.4](https://www.deeplearningbook.org/contents/regularization.html) | 讲稿保留；出处定位为 `regularization.html，§7.4`。 |
| l55 | 双语 | 记录 | **R：已解决。C11。** 用复杂度惩罚举例，允许软约束，没有声称正则化必然让模型无法插值。登记的正则化定义与原文一致。[教材 §5.2.2](https://www.deeplearningbook.org/contents/ml.html) | 保留。 |
| l57、l58 | 双语 | 建议 | **R：已解决，指把比方冒充定义的问题。** “就像／is like”已经明确类比，作者这次处理理由成立，不再按错误定义判必改。不过“没学会规律”仍不如“连偶然偏差也学进去”准确：过拟合可以同时包含规律和噪声。 | zh l57：过拟合，就像把练习题背得太死，<br>zh l58：连错处也照背。<br>en l57：Overfitting is like memorizing the workbook<br>en l58：including its mistakes. |
| 全片 | 双语 | 必改 | **R：未解决，事实登记已明显补齐。** C14、C15 已覆盖误差指标、六点、训练／测试与噪声定义；仍需补齐或明确挂接：l02 的频率判断、l16 的拟合走势、l27 的记忆容量解释、l39 新增的压缩断言、l57—l58 的总结。C10 虽挂了 l53，教材却不能证明“本演示按考试成绩选模”。 | 删除 l02 无依据的频率；C03 挂接 l27，C14 挂接 l16，C09 挂接 l57、l58；C13 同步修订后的压缩表述；本次选模方式登记为实验事实。 |
| 全片 | 双语 | 记录 | **R：已解决。** 已登记的句号仍能对应当前相关内容，没有整段错位；遗漏挂接与句号错位是两类问题。 | 保留现有对应关系，修改讲稿后补齐挂接。 |
| 全片 | 双语 | 记录 | **R：未解决，存疑。C01、C02、C03、C14。** 三次多项式四个系数、九次多项式十个系数在数学上成立；十个不同横坐标允许九次以下多项式插值。但材料未提供实际点集、拟合或运行结果。`20 ≤ RATIO < 30` 不能证明画面四舍五入为 25，亦不能证明测试 MSE 为 1.80；函数名不能证明实际统计曲线。 | 数字暂不猜改。核实材料应提供：当前点集与噪声生成方式、三模型训练／测试 MSE、未取整倍率、三百次逐复杂度中位数，以及实际选模方式。 |
| 全片 | 双语 | 记录 | **R：未解决。C10。** 引文内容正确，出处仍错写 §5.3.1；该节讲交叉验证，所引段落在 §5.3。[教材原文](https://www.deeplearningbook.org/contents/ml.html) | 将出处节号替换为 `§5.3`。 |
| 全片 | 双语 | 记录 | **R：未解决。C13。** `quote` 仍是拼接改写，不能当作逐字引文；序言末尾用的是 “about the data”，并非 “about it”。[Grünwald 序言，第 xxv 页](https://homepages.cwi.nl/~pdg/book/preface.pdf) | `quote` 替换为：`the more we are able to compress the data, the more we have learned about the data`；出处补 `Preface, p. xxv`。 |

**必查项核对说明**

- **逐条台账：** C01—C03、C14 的实验结果保留存疑；C04—C07 已核对原始研究的主体、数字、分母及范围；C08 已核对捷径定义；C09—C12、C15 已核对教材相关原文；C13 已核对序言与 MDL 描述长度解释。没有把台账自称“verified”当成独立核实。
- **夸大与因果：** l45 没有把后期全部偏差归因于过拟合；l48 的混杂解释有研究依据，但须限定数据集；l49 的学习机制仍是推测；l50 的必要条件式表述必须收回。
- **引文翻译：** `part…part` 没有译成“一半……一半”，`cases` 没有译成病例数；两项均通过。C13 的问题是英文引文不逐字，而非中文翻译。
- **专业概念与漏登：** 验证集、测试集、正则化的核心区分通过；过拟合与捷径学习已经区分。误差口径、压缩断言及剩余事实挂接见表中修改项。
- **作者不采纳：** 不口播公式可以接受，但把 MSE 说成距离相加不能接受；保留内容介绍段不属于事实核查职责，不另作判断。

**最重要的 3 条**

1. **l14：统一误差口径。** 具体数值和倍率使用 MSE，英文不能解释成距离相加。
2. **l39、l44：撤回不同数量之间的直接推论。** 参数个数不等于压缩长度，候选搜索词个数也不等于拟合自由参数个数。
3. **l48—l50：守住证据范围。** 区分数据集标签比例与医院患病比例，保留机制不确定性，删除“只有环境变化才失败”。

**做得好的、别改掉的**

1. “另训一个模型”及“两家医院”保住了 99.9% 数字的正确主体和范围。
2. GFT 已明确最初版本、数据点和流感样就诊占比，没有把后期估高全部归咎于同一个机制。
3. 验证集与测试集分工清楚，并主动说明演示选模方式不能照搬。