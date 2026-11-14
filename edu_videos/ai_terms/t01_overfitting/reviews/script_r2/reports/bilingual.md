# 审稿报告：双语编辑（语义一致）· t01_overfitting · script 第 2 轮

审稿材料：`reviews/script_r2/materials/lines.md`（v3.1，l01–l59）、`learning.json`、`reviews/script_r1/issues.md`。只读，没有参考其他审稿报告。

本轮没有必改项。两版整体对得很齐：限定语（很可能 / likely，研究中 / In one study，最初 / first version，可能 / may）都逐句保留了，数字（十 / 六 / 二十多倍 / 三百 / 五千万 / 108 周中 100 周 / 99.9% / 一半多）两版一致。剩下的问题集中在三处：英文 l47 实验描述走样，l50 两版都没点出「新」数据，英文 l09 的 accidents 意思不透明。

## 问题表

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l47 | en | 建议 | **事实走样。**中文「认出其中两家医院的片子，准确率超过 99.9%」说的是：识别片子来自哪家医院，其中两家的准确率超过 99.9%（和原研究按医院分列的结果一致）。英文 "tell scans from two of the hospitals apart" 说的却是在两家医院之间做二选一区分，是另一个实验，99.9% 也就挂到了别的任务上。结论（片子带医院指纹）没变，所以不算必改。 | en：…a separate model could identify scans from two of the hospitals with over 99.9 percent accuracy. |
| l50 | 双语 | 建议 | **漏点（两版相同）。**捷径学习区别于过拟合的关键，是在同分布的**新**数据上也能过关。两版都只说「同类数据 / similar data」，听起来可能指训练数据本身，区别就没讲到。这一点影响 O1 和 Q5（草地上的牛）。 | zh：它们在同类新题上也能考好，换个环境才露馅。<br>en：They can score well on similar new data, and only fail when the setting changes. |
| l09 | en | 建议 | **意思不透明。**中文「偶然的细节」很清楚；英文 "learns the accidents, too" 普通观众容易听成事故 / 意外，听不出「偶然的巧合」。这是全片的定义句，值得改。 | en：…so closely that it learns the flukes, too, and does worse on new data. |
| l43 | en | 记录 | **R1 未解决（作者未回应）。**数字和限定语有小出入：中文「一千多个**历史**数据点」，英文 "about 1,100 data points"，少了「历史」；原研究（Lazer et al. 2014）是 1,152 个，"about 1,100" 偏低。 | en：Researchers noted its first version tested 50 million search terms for the best fit to over 1,100 past data points. |
| l03 | en | 记录 | **R1 未解决（作者未回应）。**中文说「讲四件事」，英文 "In this episode:" 没说几件，和议程卡的四项对不上。 | en：Four things today: |
| l44 | 双语 | 记录 | 比方的分寸两版都不准：五千万个词配 1,152 个点是「远多于」，「十个数字配十个点」只是「刚好够」，用「就像」会把程度说小。两版一致，不算走样。 | zh：可挑的远比数据多，比十个数字配十个点还过分。<br>en：Far more choices than data, worse than ten numbers for ten points. |
| l02 | en | 记录 | 轻重不一：中文「很多时候」管住了整句（不是程序错，而是过拟合）；英文 "Often" 只管第一句，第二句 "The model has a problem called overfitting." 成了断言。 | en：Often the code is fine; the model is overfitting. |
| l45 | zh | 记录 | 「偏差」在 l12 刚被用来解释噪声（「随机的偏差」），这里指的是一直往高估的系统性误差，中文观众可能把两者连起来。英文 "problems" 没有这个问题。 | zh：后来的版本也不准：2011到2013年，108周里，有100周估得偏高。 |
| l45 | en | 记录 | 主语单复数不接："Later versions" 后面接 "it overestimated"。 | en：From 2011 to 2013, they overestimated flu in 100 of 108 weeks. |

## 必查项逐项说明

1. **逐句比意思**：l01–l59 逐句对过。除上表外都一致，例如 l12「大致…随机的偏差」/ "slightly off… random wobbles"，l29「可能是」/ "may learn"，l48「很可能」/ "likely"，l49「研究中，画了标记的良性痣」/ "In one study… marked harmless moles"，l53「可不能这样」/ "you shouldn't"。
2. **本语言自然说法 / 换例子**：英文 l49 给 melanoma 加了 "an AI that spots skin cancer" 的解释，中文靠「判成了癌」带出，属于合理的本地化。l08 中文「用一句话讲清」、英文 "as we go"，l24「印错的几处」/ "typos"，也是各自自然的说法。这些都不算问题。
3. **事实、数字、出处、限定语**：数字逐个核对，见开头。出处方面，l43「研究者指出」/ "Researchers pointed out"，l44「研究者说」/ "The researchers called it"，l47「研究者发现」/ "Researchers found"，两版一致。限定语「最初 / first version」「其中两家 / two of the hospitals」「超过 / over」也一致。不一致的只有 l47 英文的任务描述和 l43 的「历史」/ 1,100，已列入上表。
4. **两版各自能否达成 learning.json 目标**：
   - O1（定义：手里数据好、新数据差，因为记了噪声和巧合）：两版都由 l09、l22、l57–l58 达成；捷径学习（Q5）由 l28–l30、l50 达成，l50 补上「新」之后会更稳。
   - O2（两种误差判断）：两版 l23、l34、l35 都明确说了「练习低、考试高 = 过拟合信号；两种都高 = 欠拟合」，R1 的漏点已补齐。
   - O3（复杂模型为什么过拟合）：两版 l27、l37–l39（十个数字正好穿过十个点，连噪声一起存下）都能达成。
   - O4（三种对策）：两版 l52、l54、l55 都能达成。英文改成 mock exam 后，不会再和 practice problems 混淆；Q4 要的「不碰最终测试集」由 l52「真正的考试留到最后 / Save the real exam for the very end」覆盖。
   - O5（不是越简单越好；训练误差为零不等于好）：两版 l35、l23 都能达成。
   - 两版程度相同的一点：都只用「练习 / 考试误差」，「训练 / 测试误差」没有在口播里说出来，测验用的却是这套标准叫法。好在 l11、l19 已经把 training / test data 和练习、考试对上，观众可以自己换过去，不单列。
5. **R：复核上一轮 bilingual 提出的问题**：
   - l03 四件事（en）：**未解决**，作者处理结论里没有提到，见上表。
   - l28 三百次歧义（双语）→ 现 l31：**已解决**，「换三百组随机的点，每组都…，看平均」/ "We draw 300 random sets… on each, and average"，两版都没有歧义，而且一致。
   - l30 英文主语「中间那一段学会了」→ 现 l33：**已解决**，两版都改成「复杂度在中间的模型 / Models of middle complexity」。
   - l32 O2 欠拟合「两种误差都高」→ 现 l23、l35：**已解决**，两版都说了。
   - l35 中文「说中」说过头 → 现 l38：**已解决**，「新点也估得不远」和 "stays close" 轻重一致。
   - l39 数字 1,100 和「历史」→ 现 l43：**未解决**，作者未回应，见上表。
   - l41 英文缺出处 → 现 l47：**已解决**，英文加了 "Researchers found"。拆句后英文又**改出了新问题**：实验任务描述走样，见上表 l47。
   - l42 中文限定语 → 现 l49：**已解决**，「研究中，画了标记的良性痣」和英文范围一致。
   - l43 "are called shortcut learning" → 现 l50：**已解决**，改为 "are shortcut learning"。
   - l45 practice exam（en）→ 现 l52：**已解决**，改为 mock exam。
   - 作者「不采纳」的三条都不是本角色提的，不评。

## 最重要的 3 条

1. l47 en：把 "tell scans from two of the hospitals apart" 改成 "identify scans from two of the hospitals"，让 99.9% 对应的实验和中文、原研究一致。
2. l50 双语：补上「新」（同类新题 / similar new data），把捷径学习和过拟合的区别讲到位。
3. l09 en："accidents" 改成 "flukes"，让定义句英文观众一听就懂。

## 做得好的、别改掉的

1. 限定语在两版里逐句保留（l29 可能 / may，l43 最初 / first version，l48 很可能 / likely，l49 研究中 / In one study），R1 指出的黑色素瘤范围问题处理得很干净。
2. 学生类比和实验的映射（l24、l26：印错的答案 = 噪声 / typos = noise）两版完全对齐，各用本语言最自然的词。
3. 欠拟合和过拟合的诊断（l23、l34、l35）两版都说得完整、对称，O2、O5 不再依赖画面。

## 其他

- learning.json 各目标的 `lines` 仍是改版前的旧句号，例如 O4 指向 l45–l47，现在这几句是流感和胸片，应为 l52、l54、l55。其余大致对应为：O1 → l09、l22、l57、l58；O2 → l15、l23、l34、l35；O3 → l27、l39；O5 → l23、l35。建议作者按 v3.1 重排。
- 存疑：l31 两版都说「平均 / average」；R1 记录画面写的是「三百次实验的中位数」。需要核对图表的统计口径，看口播和画面是否一致。
- s8 开头 l41 说「过拟合闯过祸」，后面三个例子里有两个是捷径学习（l50 才说明）。两版一致，属于结构问题，供 editor / teacher 参考。
