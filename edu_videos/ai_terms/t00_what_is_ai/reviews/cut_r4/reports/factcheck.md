本轮有 **4 处必改：l31 英文、l44、l45、l52**。实验数字内部一致，但实际运行结果仍属**存疑、未独立复算**。本轮只读取指定三份材料及外部出处；画面文字按 `claims.json.screen` 审核。

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l08 | 双语 | 建议 | “不写规则／no rules”容易被理解为机器学习没有人为设定的算法、结构和约束；实际是不逐条编写识别规则。 | 中：所以今天的 AI，大多换个做法：给例子，让它学认法。<br>英：So most of today's AI flips it around: learn from examples instead of hand-written recognition rules. |
| l20 | 双语 | 建议 | 未见题上的成绩能检验泛化表现，不能单凭它证明模型“真会认”或排除捷径；“真会／只是记住”说得稍满。 | 中：得考没见过的题，才知道它换张图还能不能认。<br>英：Test it on unseen images to see how well its learning carries over. |
| l23 | 双语 | 建议 | C02 写的是 **20 次结果的中位数**；“瞎猜10%”是十类均匀随机猜测的期望，单次考试不保证恰好10%。 | 中：这样换着抽二十回，中位数约37%；十选一瞎猜，平均10%，可还差得远。<br>英：Across twenty random sets of ten, the median was about 37%: above the 10% expected from uniform guessing, but still low. |
| l24 | 双语 | 建议 | 88%是20次抽样结果的中位数，97%是全部1497张训练的一次结果；当前并列口播隐藏了口径差异。 | 中：一百个例子，中位数88%；将近一千五百个全用上，这次答对97%。<br>英：With a hundred examples, the median is 88%. Using all 1,500 or so, this run gets 97%. |
| l28 | 双语 | 建议 | 建议明确96%是**模型报出的预测概率**。“有96%的把握”容易被听成经验证的可靠程度；材料未提供校准证据。[概率校准文档](https://scikit-learn.org/stable/modules/calibration) | 中：咱们这个模型还会报预测概率。这张图，它给“三”96%。<br>英：Our model also reports prediction probabilities. It gives three 96% here. |
| l31 | en | 必改 | 英文把中文“能聊天的大语言模型”扩大成了“聊天机器人都运行在大语言模型上”。规则式聊天机器人也是聊天机器人。[斯坦福教材：规则式聊天机器人](https://web.stanford.edu/~jurafsky/slp3/old_dec21/ed3book_dec292021.pdf) | 英：Large language models generate chat replies this way. |
| l44 | 双语 | 必改 | “用AI记住三点”的语境，尤其英文“it always answers”，把本片封闭十分类模型的行为推广给所有AI。模型或系统可以设置拒答、拒识机制；C05、C20只支持本片模型。 | 中：第一，这个数字模型遇到陌生输入也会答。给它看字母 A，它仍只能在零到九里挑。<br>英：First, our digit model must choose even for unfamiliar inputs. Show it the letter A, and it still picks from zero to nine. |
| l45 | 双语 | 必改 | **92%不只是“排名第一”**，而是模型给“四”分配的概率值；“最像”还容易被理解为直接比较图形相似度。真正的限制是输出类别没有“非数字”。 | 中：它给“四”的预测概率是92%，但只在十个数字里选，没判断这是不是数字。<br>英：It assigns four 92%, among digits only. That doesn't tell us whether this is a digit. |
| l47 | 双语 | 建议 | 与l28统一，把81%明确归给模型输出，避免继续把预测概率和实际可靠程度混称“把握”。 | 中：第二，预测概率高也会错。刚才那张潦草的二，它给“一”81%，照样错了。<br>英：Second, high prediction probabilities can be wrong. Remember that messy two? It gave one 81%, and was wrong. |
| l52 | 双语 | 必改 | “练习好、新题差”是过拟合的典型表现，但不能据此直接定性：新题分布改变也会导致下降。前文刚展示字母A，这里尤其容易把范围外输入失败与过拟合混为一谈。教材是在训练、测试来自同一分布的框架下讨论误差差距。[《Deep Learning》§5.2](https://www.deeplearningbook.org/contents/ml.html) | 中：练习题会了，同类新题却差很多？可能过拟合了，下期聊。<br>英：Next time: why can a model ace practice but struggle on similar new questions? It may be overfitting. |
| 全片 | 双语 | 记录 | 台账覆盖尚不完整：l03–l04的传统程序例子、l12“很多人以为”没有明确登记；l18–l19、l51虽有相关声明，却缺句号索引。 | 台账补入：“l03–l04：传统程序与明确规则的应用例子”；C01补l18，C18补l19，C13补l51。l12首句可直接改为：中“AI 的认法，需要程序员一条条写进去吗？”；英“Do programmers have to code in every recognition rule?” |

**逐项核查证据与存疑范围**

- **C01、C07：数据来源与单位核对通过。** scikit-learn所用版本确为1797张、每张8×8，复制自UCI原数据的测试部分；UCI完整数据则有5620个样本，两者没有混用。作者、1998年和现行CC BY 4.0许可均有官方依据。1797−300＝1497，双语“1700多／nearly 1,800”均成立。[scikit-learn数据说明](https://scikit-learn.org/stable/datasets/toy_dataset.html#optical-recognition-of-handwritten-digits-dataset)、[UCI数据页](https://archive.ics.uci.edu/dataset/80/optical%2Brecognit)
- **C02、C03、C19：口径可核，结果存疑。** 台账明确37%、88%为中位数，97%为全量训练结果；300题错10题对应96.67%，四舍五入为97%，无算术矛盾。这些成绩属于**本片实验**，不是UCI或scikit-learn官方性能结论。核实须检查当前产物对应的运行记录、20次准确率及错题列表。
- **C04、C05、C06、C20：数值存疑，概念限制已核。** 指定材料只有96%、92%、81%及分类结果的断言说明，没有实际输出；不能独立确认。核实应对照当前模型、指定样本和完整概率向量，同时检查预处理、调参是否使用了测试数据。概率归一化本身不能证明校准良好。[概率校准文档](https://scikit-learn.org/stable/modules/calibration)
- **C11：报道归属、数字及主要翻译核对通过。** 打开路透社原报道的PDF存档，确认十年间收到的简历、大多来自男性、含women’s的简历被降分，以及项目后来关停。“等于自己学会”保留了原文 *In effect* 的解释性语气。讲稿没有声称工具实际淘汰过女性，也没有把偏见写成停项的唯一原因。[路透社原报道存档](https://jlucasmckay.bmi.emory.edu/global/bmi510/Reference/hiring-bias.pdf)
- **C12、C13、C14、C17：基本概念与引文核对通过。** AI、机器学习、深度学习的包含关系符合教材；规则式AI没有被漏掉。监督学习引文中的“then learning”确有原文；难以形式化描述直觉任务的引文也对应原书。手写数字反例属于本片例子，不能当作教材实际展示的反例。[《Deep Learning》第1章](https://www.deeplearningbook.org/contents/intro.html)、[第5章](https://www.deeplearningbook.org/contents/ml.html)
- **C15：引文位置核对通过。** GPT-3论文§1确有“simply by predicting what comes next”；台账已把逐词元生成标成概括。口播说“词”，登记画面补“严格说是词元token”，作为入门简化可接受。[GPT-3论文§1](https://arxiv.org/pdf/2005.14165)
- **C18、C21、C22：原文依据成立，口播边界见表。** 泛化与过拟合引文均能对应教材；l48同时保留数据、设计和训练因素，未把能力或错误全部归因于数据。l18–l19正确区分训练例子与留出的测试题。欠拟合、验证集、正则化、捷径学习没有在本轮讲稿或登记画面中作专门解释，无对应术语误用。[《Deep Learning》第5章](https://www.deeplearningbook.org/contents/ml.html)

**最重要的3条**

1. 收紧l44：强制十选一是本片模型的限制，不能推广成AI总会硬答。
2. 修正l52：避免把范围外输入失败直接归为过拟合。
3. 统一l28、l45、l47：区分模型报出的概率、类别排名和实际可靠程度。

**做得好的、别改掉的**

1. l25保留“在这次实验里”，没有把更多数据必然更好写成普遍定律。
2. 亚马逊案例保留路透社归属和试验性质，未虚构实际招聘后果。
3. l34保留规则式AI，l48保留设计与训练因素，使“从数据学习”的主线没有变成单一原因论。