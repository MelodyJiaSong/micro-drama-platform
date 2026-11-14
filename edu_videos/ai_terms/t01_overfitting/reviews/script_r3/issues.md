# 审稿汇总：script_r3

必改 7 · 存疑 0 · 建议 14 · 记录 32；「多人」= 两个以上角色指到同一句。处理结论写在最后一列（改 / 不改＋理由）。

| 句号 | 语言 | 级别 | 角色 | 多人 | 问题 | 建议改法 | 处理 |
|---|---|---|---|---|---|---|---|
| l02 | 双语 | 建议 | factcheck |  | **R：未解决。** 英文第二句仍直接确诊；旧数据好、新数据差也可能来自分布变化。“很多时候／Often”的频率没有登记依据。 | zh：可能不是程序出错，而是过拟合。<br>en：One possible culprit is overfitting. |  |
| s6 | 双语 | 记录 | teacher |  | R：未解决（作者没有回应）。存疑：口播只说「练习误差 / 考试误差」，learning.json 的 O2 写的是「练习（训练）误差」，Q1 用「训练邮件」，Q4 用「最终测试集」，口播里一次也没出现「训练误差 / 测试误差 / 测试集」。核实办法：查 s6 画面标签有没有把标准名并列写上，写了就算已解决。 | 口播不改；s6 标签第一次出现时写「练习误差（训练误差）」「考试误差（测试误差）」，en "practice (training) error" / "exam (test) error"。 |  |
| l07 | zh | 记录 | teacher |  | R（r2 l41）：l41 已改成「这类毛病」，但目录里的「它在现实里闯的祸」还是把「它」指向过拟合。三个案例里有两个是捷径学习。 | zh：现实里闯过的祸，和怎么防。 |  |
| l09 | zh | 记录 | teacher | ★ | R：未解决（作者没有回应）。「拟合」两个字仍然没有点破，中文观众未必能从「拟合」想到「贴合」，「过」拟合也就少了直觉。 | 口播不改；术语卡写「拟合 = 让曲线贴合数据；过拟合 = 贴过了头」。 |  |
| s9 | 双语 | 记录 | teacher |  | R：未解决，可以接受。验证集、正则化两个新术语都在最后一分钟出现，违反对标里「最后一分钟不引入新术语」一条，但 O4 需要这两个词，以清单形式出现也行。存疑：两个词是否上了术语卡，需要核对画面。 | 口播不改；两个词都上术语卡，s10 不再出现新词。 |  |
| l09 | 双语 | 记录 | factcheck | ★ | **R：已解决。C09。** 定义聚焦于偶然细节损害新数据表现，没有把“完全没学到规律”作为必要条件；与教材的过拟合解释相容。[教材 §5.2](https://www.deeplearningbook.org/contents/ml.html) | 保留。 |  |
| l10 | 双语 | 建议 | teacher |  | 和 l09 自相矛盾：l09 说模型「连偶然的细节也学了进去」，意思是规律学了，偶然细节也学了；l10 却说「没学会规律」。l40 又用「连规律也丢了」来形容直线（欠拟合）。同一种说法同时套在两种相反的毛病上。l57 呼应的就是这一句，两处要一起改。 | zh：打个比方：练习题连印错的答案都背了，还当成规律。来看个小实验。<br>en：Think of it as memorizing every answer, misprints included, and trusting them. Let's see it in a small experiment. |  |
| l11 | 双语 | 记录 | factcheck |  | **C15：概念基本正确。** 训练用于拟合，测试用于评估未见样本；随机偏差作为本实验噪声的解释可接受。教材引文确实说明测试样本与训练样本分开收集，但不能单独证明本实验的噪声生成方式和六点数量。[教材 §5.2](https://www.deeplearningbook.org/contents/ml.html) | 概念表述保留；实验事实见末尾存疑项。 |  |
| l13 | 双语 | 记录 | teacher |  | R：未解决（作者没有回应），但现在可以接受：紧接着的 l14「第一种模型……只会画直线」已经让「模型画出一条线」成立。本轮关闭。 | 保留。 |  |
| l14 | 双语 | 必改 | factcheck |  | **R：未解决，纵向方向已解决。C14。** 中文“汇总”未说清指标；英文 **added up** 明确说成距离相加，而台账是高度差平方的平均。作者“不采纳平方平均，因为过细”的理由不足：可以省公式，不能换计算口径；台账也不能抵消错误口播。 | zh：第一种只会画直线。这里的误差，是每个点与曲线高度差平方的平均。<br>en：Model one draws a straight line. Here, error is the average squared difference in height between points and predictions. |  |
| l15 | 双语 | 建议 | factcheck |  | **R：未解决，但已无“不穿点就是欠拟合”的错误。C09。** “误差压不下来”容易理解为完全不能降低；实际是无法降得足够低。 | zh：直线连整体弯曲的走势都抓不住，这叫欠拟合。<br>en：The line misses even the overall bend. That's underfitting. |  |
| l21 | en | 记录 | factcheck |  | **R：已解决。C01。** 倍数表达使用 “times model two’s”，没有“高出多少倍”的歧义；具体倍率尚未独立复算。 | 保留倍率句式。 |  |
| l22 | 双语 | 建议 | factcheck |  | **R：未解决。** 随机不等于绝不重复；关键是本次偏差不能可靠预测新样本。 | 替换中间一句：<br>zh：可随机偏差，不能可靠地预测新题。<br>en：But those random wobbles won't reliably predict new points. |  |
| l23 | 双语 | 建议 | factcheck |  | **R：未解决，部分已解决。** “比如这里／Here”已消除零训练误差是必要条件的暗示；但“欠拟合很容易发现”仍被写成无条件判断。 | zh：欠拟合，练习题就做不好；过拟合容易漏看，因为练习成绩可能很好，比如这里误差是零。<br>en：Underfitting shows up on practice data. Overfitting can be harder to spot because training scores may look excellent—as they do here. |  |
| l25 | 双语 | 记录 | teacher |  | R：未解决（作者没有回应）。类比里「印错的答案」只映射了「被存下来」，没有映射「害人」。考砸的原因被说成「题目一变就不会」，和噪声无关。 | zh：可一到考试，题一变样就不会，还照搬印错的。<br>en：On the exam, any change throws him, and he repeats the typos. |  |
| l27 | 双语 | 记录 | teacher |  | R：①已解决，「能力大到」已删，叫法统一成「复杂」。②我上轮提的「练习册只错几处、数据每个点都有噪声」没有采纳。现在说的局限（学生知道自己在背，模型不知道）能防拟人化，又接回「足够复杂」，可以成立。本轮关闭。 | 保留。 |  |
| l28 | 双语 | 记录 | factcheck |  | **R：已解决。C08。** “相近、但不一样”明确区分记住噪声与利用沙发线索，没有把两种机制等同。 | 保留。 |  |
| l30 | 双语 | 建议 | teacher |  | R：未解决（作者没有回应）。「小朋友是见得太少」把病因说成了数量问题。照片全是沙发上的猫，再加一千张也没用，病根是太单一。这样和 l54「更多样」对不上，也和 Q5（草地上的牛）考的点对不上，观众会以为「多给数据」就能治捷径学习。 | zh：这两个孩子，都把眼前的例子当成了规律：学生记得太多，小朋友见得太单一。后一种叫捷径学习，后面还会碰到。<br>en：…The student remembered too much. The child saw only sofas. … |  |
| l31 | 双语 | 记录 | factcheck |  | **R：已解决，限措辞冲突。C02。** “通常／typical”不再与台账和画面的“中位数”冲突。是否实际抽样三百组并取中位数，仍需运行结果证明。 | 保留。 |  |
| l33 | 双语 | 记录 | factcheck |  | **R：已解决。C02、C09。** 前面的“回到实验”限定了语境；现在比较预测成绩，没有声称只有中间复杂度才会学到规律，也没有主张越简单越好。 | 保留；曲线数值另核实。 |  |
| l37 | 双语 | 建议 | factcheck |  | **R：未解决。C03。** 只存十个高度就能还原十个点，需要横坐标已知。 | zh：横坐标已知，只需记十个高度。<br>en：With horizontal positions known, store the ten heights. |  |
| l39 | 双语 | 必改 | factcheck | ★ | **R：改出了新问题。C03、C13。** 原先“参数多就没学规律”的推断已删，但新增“十个数字存十个点，等于没有压缩”仍把参数数量当成编码长度。MDL 比较描述所需的比特数，还要考虑精度及残差；不能仅凭十对十判定没有压缩。[Grünwald §1.5](https://homepages.cwi.nl/~pdg/book/chapter1.pdf) | zh：第三种用十个数字，让曲线穿过全部十个点。它把每个点都拟合得太准，连随机偏差也记了下来。<br>en：Model three uses ten numbers to pass through all ten points. It fits every point exactly, including its random deviation from the underlying pattern. |  |
| l39 | 双语 | 记录 | teacher | ★ | R：已解决，「十个数字存十个点，等于没有压缩」已经说穿。新风险：l39 和 l44 都在数个数，观众可能记成「数字比点少就不会过拟合」或「数字比数据多一定过拟合」（7 个数字配 10 个点也会记下部分噪声）。 | 口播不改；l39 画面加小字「数字越接近点数，越容易记下噪声」/ en "The closer the count is to the points, the more noise it can store." |  |
| l40 | en | 建议 | factcheck | ★ | **R：未解决，中文已解决。C13。** 中文已改成目标式的“要留住规律、少记噪声”；英文仍说直接留下规律、排除噪声，强于中文，也容易让人误以为压缩保证分离两者。[Grünwald §1.5](https://homepages.cwi.nl/~pdg/book/chapter1.pdf) | en：Good compression aims to capture patterns without chasing noise. Squeeze too hard, like the straight line, and you lose the pattern, too. |  |
| l40 | 双语 | 记录 | teacher | ★ | R：已解决。两头都讲了（留规律、少记噪声；压过了头连规律也丢），「恰好是噪声」的过满说法已删。 | 保留。 |  |
| l41 | 双语 | 记录 | teacher |  | R：已解决（「这类毛病」）。目录残留见 l07。 | 保留。 |  |
| l42 | 双语 | 记录 | factcheck |  | **R：已解决，指指标和数据点口径。C04。** 原文确为最初版本、五千万候选搜索词、1,152 个数据点；cases 没有被译成病人。口播“一千多／about 1,100”与画面精确值相容；流感样就诊占比也已补回。[Lazer 原文，第 1203 页](https://cdanfort.w3.uvm.edu/csc-reading-group/lazer-flu-science-2014.pdf) | 保留。 |  |
| l44 | 双语 | 必改 | factcheck | ★ | **R：未解决，翻译部分已解决。C04。** 候选搜索词数量与多项式自由参数数量不是同一口径，“比十个数字配十个点还夸张”继续引导观众直接比较。应讲清季节性假关联，而非用两种不同数量推出程度比较。“既……也……”没有误译成各占一半，正确。[Lazer 原文](https://cdanfort.w3.uvm.edu/csc-reading-group/lazer-flu-science-2014.pdf) | zh：有些搜索词只是随季节变化，并不真正反映流感。研究者说，这是过拟合：它既在测流感，也在测冬天。<br>en：Some search terms tracked the season rather than flu itself. Researchers called this overfitting: it tracked both flu and winter. |  |
| l44 | 双语 | 建议 | teacher | ★ | R：未解决（作者没有回应）。量级比喻已修好（「还夸张」），这是全片把实验和现实案例做比较的唯一一处。但从「可挑的多」到「也在测冬天」还缺一步：词一多，总有些词只是碰巧冬天多搜。少了这一步，「测冬天」听起来是个梗，不是机制，也接不回 l09 的「偶然的细节」。l44 还是 O3 的支撑句。l43 已经说过「研究者说」，这里可以省。 | zh：可挑的远比数据点多，比十个数字配十个点还夸张，总有词碰巧冬天多搜。这是过拟合：既测流感，也测冬天。<br>en：Far more choices than data points, worse than ten numbers for ten points, so some terms tracked winter. Researchers called it overfitting: part flu detector, part winter detector. |  |
| l45 | 双语 | 建议 | teacher | ★ | R：未解决（作者没有回应；r2 里 editor 和我都建议删）。「108 周里 100 周偏高」没说跟过拟合是什么关系，观众会默认也是过拟合造成的，对理解概念没有增量，属于诱惑性细节（对标第二节，Rey 2012）。zh 的「偏差」又撞上 l12 给噪声下定义用的「随机的偏差」，一个是随机，一个是系统性偏高。 | 删除。 |  |
| l45 | 双语 | 记录 | factcheck | ★ | **R：已解决。C05。** 原文窗口为 2011-08-21 至 2013-09-01，108 周中 100 周估高；没有说高了 100%，也未将这些偏差全部归因于最初版本的过拟合。[Lazer 图注，第 1204 页](https://cdanfort.w3.uvm.edu/csc-reading-group/lazer-flu-science-2014.pdf) | 保留。 |  |
| l46 | 双语 | 记录 | factcheck |  | **C06：已核实。** NIH 与 MSH 联合训练的肺炎模型，联合内部测试 AUC 为 0.931，IU 外部测试为 0.815；“成绩下降”准确，没有将 AUC 误称为诊断准确率。[Zech 结果](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1002683) | 保留。 |  |
| l47 | 双语 | 记录 | factcheck |  | **R：已解决。C06。** 是另训的医院识别 CNN；NIH 为 22,050/22,062，MSH 为 8,386/8,388，分别约 99.95%、99.98%。研究还包含 IU，不能把 99.9% 推广至全部医院；本轮“两家医院的片子”限定正确。[Zech 结果](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1002683) | 保留；画面继续同时呈现模型身份和范围。 |  |
| l48 | 双语 | 必改 | factcheck | ★ | **新增口径问题。C06。** 34.2%、1.2%、1.0% 是各研究数据集中的肺炎阳性标签比例，并非各医院全部就诊病人的患病比例。“认医院有助于预测”的推断有依据，但分母和标签口径需要收窄。[Zech 方法与结果](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1002683) | 只替换首句：<br>zh：各院数据中，标成肺炎的比例差很大。<br>en：Pneumonia label rates differed widely across datasets. |  |
| l48 | 双语 | 记录 | teacher | ★ | R：已解决。补上了「各家医院的肺炎病人比例差得很远」，「靠认医院」现在讲得通了。 | 保留。 |  |
| l49 | 双语 | 建议 | factcheck | ★ | **R：已解决，指数值与研究范围；新增机制解释需降调。C07。** 107 个良性痣在既定阈值下的误判率由约 15.9% 升至 54.2%，画面 16%→54% 正确。原文却明确说机制不清，只提出可能解释；“很可能／likely”比原文更确定。中文“痣上”也宜改为“痣旁”。[Winkler 结果与讨论](https://jamanetwork.com/journals/jamadermatology/fullarticle/2740808) | zh：还有一个识别黑色素瘤的系统：医生常在可疑的痣旁画标记，它可能把标记当成了线索。研究中，画了标记的良性痣，一半多被它判成了癌。<br>en：An AI that detects melanoma, a skin cancer, may have picked up doctors’ ink marks around suspicious moles. In one study, it flagged over half the marked benign moles as cancer. |  |
| l49 | 双语 | 记录 | teacher | ★ | R：已解决。补上了「医生常在可疑的痣上画标记」这一环，并用「很可能」保留了不确定性。 | 保留。 |  |
| l50 | 双语 | 必改 | factcheck | ★ | **R：未解决。C08。** 同类新数据可能表现好，这一点正确；“换个环境**才**／**only** fail”却把环境变化写成失败的必要条件。两个案例的共同解释也不宜抹去皮肤研究保留的机制不确定性。[Geirhos 原文](https://www.allpsych.uni-giessen.de/rauisch/readings/Geirhos_et_al.2020.pdf)、[Winkler 讨论](https://jamanetwork.com/journals/jamadermatology/fullarticle/2740808) | zh：后两个例子提示了捷径学习：模型依赖医院或笔迹等线索。同类新题可能考好，换个环境却失灵。<br>en：Those cases suggest shortcut learning: relying on hospital clues or ink marks. Such shortcuts can work on similar new data yet fail elsewhere. |  |
| l50 | 双语 | 建议 | teacher | ★ | R：未解决。①「同类新数据上也能考好」没有把推论点破：l34 的两种误差信号这时不报警，l52 的验证集也抓不住，观众会以为验证集什么都能防，这是一个新误解。②「和认猫的小朋友一样」没有把映射说出来（医院指纹、标记 ↔ 沙发），类比没有显式对应回去。 | zh：医院和标记，就像那张沙发。这是捷径学习，过拟合的近亲：同类新题照样考好，两种误差都不报警，换了环境才露馅。<br>en：The hospital clues and ink marks were their sofa. That's shortcut learning, a close cousin of overfitting. They score well on similar new data, so no alarm sounds until the setting changes. |  |
| l52 | 双语 | 记录 | factcheck |  | **R：已解决，指概念。C10。** 验证集选择模型、测试集留到最后，准确；承认演示按测试成绩选择，避免将演示当成规范流程。教材支持这一区分，但不能证明本次演示实际怎样选模。[教材 §5.3](https://www.deeplearningbook.org/contents/ml.html) | 讲稿保留；本次选模过程列入实验核实材料。 |  |
| l53 | 双语 | 建议 | teacher |  | R：未解决（作者没有回应）。只说了「不能这样」，没说为什么。按考试成绩挑模型，考试就不再是没见过的题，等于对考试也贴过了头。这是全片唯一一次把概念用回到自己身上的机会，也正对着 Q4 的数据泄漏干扰项。不讲原因，观众记住的只是一条规矩（以前抓过的「教数据泄漏」只修好了一半）。 | zh：坦白一句：演示时我们按考试挑了模型；真做项目可不行，考试就不再是新题了。<br>en：Confession: we picked the demo model by exam score. In practice, don't: the exam stops being new. |  |
| l54 | 双语 | 记录 | teacher | ★ | R：未解决。只给了做法，没给「为什么」：数据一多，模型背不下每个点；巧合也不会次次出现，这一点同时收回了沙发那条线。 | zh：第二，多收集、更多样的数据：点多了背不下，巧合也难次次出现。<br>en：Two: more data, and more varied data. Too many points to memorize, and coincidences rarely repeat. |  |
| l54 | 双语 | 记录 | factcheck | ★ | **C12：已核实。** “更多、更多样”“不容易／less likely”是概率性改善，没有保证根除过拟合。所登记英文引文可在教材 §7.4 找到；台账应直接链接该章。[教材 §7.4](https://www.deeplearningbook.org/contents/regularization.html) | 讲稿保留；出处定位为 `regularization.html，§7.4`。 |  |
| l55 | 双语 | 记录 | factcheck |  | **R：已解决。C11。** 用复杂度惩罚举例，允许软约束，没有声称正则化必然让模型无法插值。登记的正则化定义与原文一致。[教材 §5.2.2](https://www.deeplearningbook.org/contents/ml.html) | 保留。 |  |
| l57 | 双语 | 必改 | teacher | ★ | R：部分解决。「就像」已经说明这是比方，作者「精确定义在 l09」的理由部分成立。但这是观众最可能带走、拿去复述的一句，问题仍在，而且现在更明显：①「没学会规律」和 l40 形容直线（欠拟合）的「连规律也丢了」是一回事，同一句话盖住了两种相反的毛病，观众带走的其实是欠拟合的描述，正是「狗的例子其实是欠拟合」那一类错；②「没学会」会引向 learning.json 列出的误解「过拟合就是训练不够」；③没有噪声，O1 的「因为记住了噪声和巧合」落不到片尾。 | zh l57：过拟合，就像连印错的都背下来，<br>zh l58：当成了规律。<br>en l57：Overfitting is like memorizing even the typos<br>en l58：and trusting them. |  |
| l57 | 双语 | 建议 | factcheck | ★ | **R：已解决，指把比方冒充定义的问题。** “就像／is like”已经明确类比，作者这次处理理由成立，不再按错误定义判必改。不过“没学会规律”仍不如“连偶然偏差也学进去”准确：过拟合可以同时包含规律和噪声。 | zh l57：过拟合，就像把练习题背得太死，<br>zh l58：连错处也照背。<br>en l57：Overfitting is like memorizing the workbook<br>en l58：including its mistakes. |  |
| 全片 | 双语 | 必改 | factcheck | ★ | **R：未解决，事实登记已明显补齐。** C14、C15 已覆盖误差指标、六点、训练／测试与噪声定义；仍需补齐或明确挂接：l02 的频率判断、l16 的拟合走势、l27 的记忆容量解释、l39 新增的压缩断言、l57—l58 的总结。C10 虽挂了 l53，教材却不能证明“本演示按考试成绩选模”。 | 删除 l02 无依据的频率；C03 挂接 l27，C14 挂接 l16，C09 挂接 l57、l58；C13 同步修订后的压缩表述；本次选模方式登记为实验事实。 |  |
| 全片 | 双语 | 记录 | teacher | ★ | R（learning.json 句号错位，r2 必改）：已解决。五个目标的 `lines` 已经和本稿对上，逐条核对都指向相关句。 | 保留。 |  |
| 全片 | 双语 | 记录 | teacher | ★ | R（O3 / Q3 口径）：已解决。O3 改成「数字多到能把每个点原样存下，连噪声也一起记住」，与 l39 一致。 | 保留。 |  |
| 全片 | 双语 | 记录 | factcheck | ★ | **R：已解决。** 已登记的句号仍能对应当前相关内容，没有整段错位；遗漏挂接与句号错位是两类问题。 | 保留现有对应关系，修改讲稿后补齐挂接。 |  |
| 全片 | 双语 | 记录 | factcheck | ★ | **R：未解决，存疑。C01、C02、C03、C14。** 三次多项式四个系数、九次多项式十个系数在数学上成立；十个不同横坐标允许九次以下多项式插值。但材料未提供实际点集、拟合或运行结果。`20 ≤ RATIO < 30` 不能证明画面四舍五入为 25，亦不能证明测试 MSE 为 1.80；函数名不能证明实际统计曲线。 | 数字暂不猜改。核实材料应提供：当前点集与噪声生成方式、三模型训练／测试 MSE、未取整倍率、三百次逐复杂度中位数，以及实际选模方式。 |  |
| 全片 | 双语 | 记录 | factcheck | ★ | **R：未解决。C10。** 引文内容正确，出处仍错写 §5.3.1；该节讲交叉验证，所引段落在 §5.3。[教材原文](https://www.deeplearningbook.org/contents/ml.html) | 将出处节号替换为 `§5.3`。 |  |
| 全片 | 双语 | 记录 | factcheck | ★ | **R：未解决。C13。** `quote` 仍是拼接改写，不能当作逐字引文；序言末尾用的是 “about the data”，并非 “about it”。[Grünwald 序言，第 xxv 页](https://homepages.cwi.nl/~pdg/book/preface.pdf) | `quote` 替换为：`the more we are able to compress the data, the more we have learned about the data`；出处补 `Preface, p. xxv`。 |  |

## 处理结论（作者，2026-11-08 → v3.3，讲稿定稿）

**采纳**：l14 误差说明改为「平方后取个平均」（与台账均方误差一致）；l30「见得太单一」（病因是单一而非数量，与 l54「更多样的数据」、Q5 对上）；l44 删去与参数数量的口径比较，改讲机制「总有一些只是碰巧在冬天搜得多」；l48「数据里标成肺炎的比例」（标签口径）；l50「可能考得不错，换个环境就可能失灵」（不写成必要条件）；**片尾一句话改为「过拟合，就像连印错的都背了下来，还当成了规律」**——带上噪声、不再和欠拟合「连规律也丢了」撞车；l02 去掉「很多时候」的频率判断；台账挂接 C03→l27、C14→l16、C09→l57/l58，补 C16（演示用测试误差挑模型）。

**不采纳**：l39「十个数字存十个点，等于没有压缩」——这是「学习可以看成压缩」视角下的直观说法，已在台账 C13 注明参数数不等于编码长度；改成「拟合得太准」会丢掉这一段的视角，属取舍。
