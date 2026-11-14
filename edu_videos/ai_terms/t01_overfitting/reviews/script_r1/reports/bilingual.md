# 双语编辑审稿报告（语义一致）· ai_terms / t01_overfitting · script 第 1 轮

审稿人角色：双语编辑（语义一致）
材料：`reviews/script_r1/materials/lines.md`（l01–l51 中英对照）、`learning.json`（O1–O5、Q1–Q5）
方法：l01–l51 中英两版逐句比意思（不比字面），逐一核对数字、出处、限定语；再按 O1–O5 分别检查两版能否各自达成目标。

## 逐条问题

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l45 | en | 必改 | 英文版前面一直用 practice problems = 训练数据、practice error = 训练误差（l09、l13、l29、l31），这里又把验证集叫 "practice exam"。英文观众很容易把验证集当成训练数据的一部分，可 Q4 考的正是这个区分。中文用「练习题 / 模拟考」，两个词分得开，没有这个问题。 | en：…set aside another slice of data as a mock exam, called a validation set. … |
| l42 | zh | 必改 | 限定语两版不一致。英文有 "With the marks"，说的是带标记的良性痣有一半多被误判；中文「让它把一半多的良性痣，都误判成了癌」读起来像所有良性痣里一半多都被误判，夸大了范围。存疑：「一半多」这个数字请对照 Winkler et al. 2019（JAMA Dermatology，皮肤标记对 CNN 黑色素瘤识别的影响）里带标记时的特异度或假阳性率核实。 | zh：还有一个识别黑色素瘤的系统：带医生标记笔迹的良性痣，一半多被它误判成了癌。 |
| l32（O2） | 双语 | 建议 | O2 要求观众会判断「两种误差都高是欠拟合」。两版都只讲了欠拟合在练习题上不行（l13），模型一的考试误差在 s4 没提（l18–l19 只讲了模型二和模型三），l32 也只说「左边的欠拟合」，全靠画面。缺了画面，两版都达不成 O2 的后半句。 | zh：模型越简单越好？不。太简单，两种误差都高，是左边的欠拟合。要找中间刚刚好的那段。<br>en：So is simpler always better? No. Too simple, and both errors stay high: underfitting, on the left. You want the sweet spot in the middle. |
| l35 | zh | 建议 | 轻重不一。中文「还能说中没见过的点」意思是预测得准，说过头了；英文 "comes close" 只是说离得不远，跟 l18「离新点都不远」一致。 | zh：第二种曲线，只用四个数字，就把它们大致说清了，新点也估得不远。 |
| l28 | 双语 | 建议 | 两版都有歧义：「重复三百次，让模型从简单变到复杂」/ "repeat it 300 times, making the model more and more complex" 可以理解成三百步、每步加一点复杂度，也可以理解成每档复杂度各重复三百次再取平均。存疑：请对照实验脚本或图的数据说明，确认 300 指什么，再选用下面的改法。 | zh（若是每档取平均）：回到实验。模型从简单调到复杂，每档做三百次取平均，看两种误差。<br>en：Back to the experiment. For each level of complexity, we average 300 runs and watch both errors. |
| l41 | en | 记录 | 出处表述不一致：中文是「研究者发现，胸片里藏着医院的指纹」，英文 "Chest X-rays turned out to carry…" 没有说是谁发现的。 | en：Medical imaging has examples too. Researchers found chest X-rays carry a hospital fingerprint: … |
| l39 | en | 记录 | 数字的说法略有出入：中文「一千多个历史数据点」，英文 "about 1,100 data points"。存疑：Lazer et al. 2014（Science, "The Parable of Google Flu"）原文是 1,152 个，按这个数，"about 1,100" 偏低；英文也少了「历史」这个限定。 | en：…it searched 50 million terms for the best fit to over 1,100 past data points. |
| l03 | en | 记录 | 中文说「讲四件事」，英文没有说是四件，跟议程卡上的四项对不上。 | en：Four things today. |
| l43 | en | 记录 | "Those last two are called shortcut learning" 字面意思是「这两个例子名叫捷径学习」，搭配有点别扭；意思与中文一致。 | en：Those last two are shortcut learning, a close cousin of overfitting. … |
| l30 | en | 记录 | "Only the middle stretch has actually learned the pattern" 说成一段曲线「学会了」，主语别扭；中文「中间那一段」口语里可以接受。 | en：But exam error falls, then rises. Only models in the middle actually learned the pattern. |

## 必查项逐项说明

1. **逐句比意思**：51 句里除上表各条外，意思都一致。保留语气核对过：l26「可能」/ "may"、l41「很可能」/ "likely"、l27「被允许记得太多」/ "allowed to remember too much" 两版轻重相同。轻重不一只有 l35 一处；漏点只有 l03 没说「四件」。
2. **本语言自然说法**：两版各用本语言习惯说法的地方都没有改变意思，不算问题，例如 l32 "sweet spot" 对「刚刚好的那一段」、l39 "part flu detector, part winter detector" 对「既在测流感，也在测冬天」、l22 "scores a hundred" 对「次次满分」、l38 "This isn't just theory" 对「真的闯过祸」。
3. **事实、数字、出处、限定语**：数字逐个对过，两版一致：十个点、六个新点、二十多倍 / more than twenty times、300 次、四个数字 / 十个数字、五千万个搜索词、2011–2013 年 108 周里有 100 周估高、「几乎百分之百」/ "almost perfectly"、「一半多」/ "more than half"。不一致的有三处：l42 限定语、l41 出处、l39 的「一千多」与 "about 1,100"（见表）。
4. **learning.json 目标**：
   - O1：两版都能达成（l01、l09、l20、l21、l43、l49–l50，「噪声」「巧合」两版都有）。
   - O2：两版都只达成一半，「两种都高是欠拟合」缺口语说明（见 l32 条）。
   - O3：两版都能达成（l15、l34–l36，十个数字正好存下十个点）。
   - O4：中文能达成；英文 l45 的 "practice exam" 会削弱「验证集 ≠ 训练数据」的理解（见 l45 条）。
   - O5：两版都能达成（l15 + l19 + l21 讲了「训练误差为零不等于好」；l32 讲了「不是越简单越好」）。
   - Q5（牛与草地）的迁移，两版都有 l25–l26 猫与沙发的例子支撑。

## 最重要的 3 条

1. l45 en：把验证集叫 "practice exam"，跟 practice problems / practice error（训练数据 / 训练误差）撞词，改成 "mock exam"。
2. l42 zh：漏了「带标记的」这个限定，「一半多的良性痣」范围夸大，跟英文 "With the marks" 不一致。
3. l32 双语：两版口语里都没有说「两种误差都高 = 欠拟合」，O2 后半句只靠画面。

## 做得好的、别改掉的

1. 保留语气两版一一对应（l26 可能 / may，l41 很可能 / likely），所有数字两版完全一致。
2. 全片的核心一句（l09 与 l49–l50）中英都前后呼应，英文首尾用词也完全相同，便于记忆。
3. 两版都用本语言的地道说法，没有逐字硬译，例如 "part flu detector, part winter detector"、"sweet spot"、「模型不会偷懒，它只是被允许记得太多」。

## 其他

- l13 把「误差」的定义和「第一种模型」塞在同一句里，信息有点密（不属本角色，一句带过）。
