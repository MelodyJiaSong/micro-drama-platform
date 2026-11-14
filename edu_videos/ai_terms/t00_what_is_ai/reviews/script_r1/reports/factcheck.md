本轮有必改项，主要是几处把学习能力、数据作用和概念边界说得过满。三个现实案例的核心归属基本准确；实验数字内部一致，但在本次指定材料范围内，不能独立确认已经复算通过。

仅阅读了指定三份仓库材料，未读取其他审稿报告。画面文字按 `claims.json` 的 `screen` 字段核查，未见实际画面。下表的替换文字只替换所指出的片段，其余原句保留。

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l01 | 双语 | 必改 | “从来没有人告诉过电脑”混淆了**不手写识别规则**与**不给训练信息**。人工标注的猫图片也在告诉模型什么是猫。 | zh：相册认得出猫，可人并没把认猫的规则一条条写给它。<br>en：Your photo app can spot cats without people spelling out every recognition rule. |
| l11 | 双语 | 建议 | “规则谁也说不清”比“难以完整描述”更绝对。[教材引言](https://www.deeplearningbook.org/contents/intro.html)讲的是难以形式化描述，并非无人能描述任何规则。 | zh：可有些事，规则很难写全。比如，认出一个手写的数字三。<br>en：But some tasks are hard to capture in rules. Like recognizing a handwritten three. |
| l14 | 双语 | 必改 | “规则写得再多，也总会……”把工程困难说成必然结论；材料没有证明手写规则无论如何都必定失败。 | zh：手写这些规则，很容易漏掉写法，也容易认错别的数字。<br>en：Hand-written rules can miss some threes and mistake other digits for threes. |
| l15 | 双语 | 建议 | 下文展示的是带标签例子的监督学习。“不写规则”容易被理解为无需人工设计算法、目标或约束。 | zh：一种常见做法：不写识别规则，给带答案的例子。<br>en：One common approach: give labeled examples instead of hand-written recognition rules. |
| l23 | 双语 | 建议 | “模型通常比小孩需要多得多的例子”没有登记，也没有限定任务和是否包含预训练经历；不能把本次训练样本数直接与儿童全部学习经历比较。 | zh：不过并不完全一样：模型需要多少例子，取决于任务；有些模型学到的规律，连开发者也难解释。<br>en：The analogy has limits. How many examples a model needs depends on the task. Some models learn patterns even their makers struggle to explain. |
| l29 | 双语 | 建议 | C02 的37%是**20次抽样结果的中位数**，口播却像一次抽十张所得的成绩。台账中的屏幕注释已说明，但口播可更一致。 | 将“考试只答对了37%左右”替换为：多次抽样，典型成绩约37%。<br>将“It scores about 37%.”替换为：Across repeated samples, the median score is about 37%. |
| l32 | 双语 | 必改 | “没有人告诉它三长什么样”仍混淆标签与识别规则；“见得越多，认得越准”又把本次实验趋势说成普遍保证。增加不合适或有噪声的数据不保证提高成绩。 | zh：没人手写认三的规则，只给了带答案的例子。这次，多看认得更准。相册认猫，道理相通。<br>en：Nobody wrote rules for recognizing threes; they supplied labeled examples. Here, more examples helped. Photo recognition uses a similar principle. |
| l35 | 双语 | 建议 | 百分数可以表示模型置信度，但材料没有提供校准证据，不能据此解释为真实正确率；也不是所有AI都会输出这样的数值。[概率校准文档](https://scikit-learn.org/stable/modules/calibration.html)明确区分两者。 | zh：这个模型会报出预测和置信度。比如这张图：三，96%。<br>en：This model reports a prediction and confidence score. Here: three, 96%. |
| l37 | 双语 | 必改 | 常见自回归聊天模型预测的是 **token**，不一定是完整的“词”。“猜得非常非常好”也没有交代好在续写预测，并不保证内容正确。[GPT-3原论文](https://arxiv.org/html/2005.14165v4)采用token序列描述。 | zh：给它半句话，它预测下一小段文字；接着预测，就能组成回答。常见聊天大模型，就是这样一步步生成文字的。<br>en：Give it some text, and it predicts the next small piece, a token. Repeat, and you get a reply. That's how common chat language models generate text. |
| l38 | 双语 | 必改 | “人写规则的办法也算AI”范围过宽，会让观众把前面的工资计算程序也算作AI。教材支持的是**AI包含基于规则的系统**，而非所有规则程序都是AI。 | zh：AI 是最大的圈，也包括一些基于规则的系统；机器学习在它里面。<br>en：AI is the biggest circle. It includes some rule-based systems; machine learning sits inside it. |
| l39 | 双语 | 建议 | 层级基本正确，但“很多层简单计算叠起来的模型叫神经网络”不像准确的定义：神经网络也可以很浅，单有计算层叠也不足以定义它。 | zh：再往里是深度学习，常用多层神经网络，逐层处理信息。大语言模型，就是其中一种。<br>en：Inside that is deep learning, often using neural networks with many processing layers. Large language models are one example. |
| l40 | 双语 | 建议 | C12虽挂了此句，但教材层级图不能证明“今天大家说AI大多指机器学习”这一当下用语比例判断。限定本片范围更稳。 | zh：我们这一期，主要讲的就是机器学习。<br>en：This episode focuses on machine learning. |
| l43 | 双语 | 记录 | 报道说估计**达到**一亿，讲稿用“过了一亿／passed”，略微加码。其他口径正确。[路透原稿转载](https://www.euronews.com/2023/02/02/openai-chatgpt)保留了估计、月活及UBS来源。 | zh：ChatGPT 上线大约两个月，月活跃用户估计就达到一亿。<br>en：ChatGPT was estimated to have reached a hundred million monthly active users about two months after launch. |
| l44 | 双语 | 建议 | “学到的不只有规律”把偏见放到了规律之外；模型完全可能学到有偏的统计规律。 | zh：但规律也会带偏见。<br>en：But learned patterns can carry bias. |
| l45 | zh | 记录 | 引例中的 *captain* 是队长，译作“社长”改变了具体职务。[路透原稿转载](https://iol.co.za/business-report/companies/2018-10-11-amazon-scraps-secret-ai-recruiting-tool-that-showed-bias-against-women/)保留了该例。 | 将“女子国际象棋社社长”替换为：女子国际象棋队队长。 |
| l46 | 双语 | 必改 | “数据里有什么，它就学什么”把可能性说成必然，也像是在说模型完整照收全部数据。亚马逊案例只能支持**可能学到数据中的偏见**。 | zh：数据里的偏见，也可能被它学走。<br>en：It can learn biases from data, too. |
| l48 | 双语 | 必改 | “它只会它学过的”否定了泛化，与前面识别未见写法相冲突。字母A的例子说明这个数字分类器面对训练范围外输入仍会强制分类，不能推出所有AI只会处理见过的内容。 | zh：第一，没学过的，它也可能乱认。给它一个字母 A：它只学过数字，只能从零到九里选，竟答：92%是四。<br>en：One: unfamiliar inputs can fool it. Show this digit-only model an A, and it must pick zero to nine. It picks four, with 92% confidence. |
| l50 | 双语 | 必改 | “本事和毛病都来自数据”是单一原因归因。模型设计、训练目标和优化方法也会影响能力与错误。 | zh：第三，本事和毛病，既受数据影响，也受设计和训练影响。判断 AI 靠不靠谱，先问它学过什么。<br>en：Three: data, design, and training shape its strengths and flaws. To judge an AI, start by asking what it learned from. |
| l54 | 双语 | 建议 | “背答案”可作比喻，但不足以界定过拟合，也不是必要条件。应把预告落在训练表现与泛化表现的差距上。[教材第5章](https://www.deeplearningbook.org/contents/ml.html)区分了训练误差与泛化误差。 | zh：下一期，我们讲过拟合：练习题做得好，新题却不行？<br>en：Next time: overfitting. Why can training go well while new questions go badly? |
| 全片 | 双语 | 记录 | **存疑：C01–C06的实验实现未独立复核。** 指向断言不等于提供断言通过的证据；三份材料也未注明实际模型与配置。不能据此断定数字错误。 | 非口播项：补充实际模型、配置、版本及运行输出；核实抽样、中位数、错误数和三个探针分数。C01的数据规模可由公开文档确认，具体划分仍需核实。 |
| l27 | 双语 | 记录 | **存疑：300张是否始终独立于模型选择。** “训练时没见过”是正确方向，但若曾用其成绩挑模型、调参数，就不能再当作独立测试成绩。现有材料不足以判断。 | 非口播项：核实模型选择、预处理拟合和调参均未使用这300张；若使用过，另留测试集再报成绩。 |
| 全片 | 双语 | 必改 | 台账未覆盖全部事实性表述：至少漏了l01的认猫机制、l11–l19的规则与学习概括、l23的儿童比较、l32的数据量推论、l34–l37的预测机制、l46、l48首句、l50及l54。C12也不能单独支撑l40。 | 非口播项：按上述句号补登记修订后的主张、适用范围和原始出处；不增加口播。比喻中的“一千道菜”无需作为真实实验数字登记。 |

**逐项核查证据与边界**

- **C01：部分确认。** [scikit-learn文档](https://scikit-learn.org/stable/datasets/toy_dataset.html)确认1797个样本、8×8输入；1797−300＝1497无误。种子0及具体划分未独立验证。
- **C02：口径基本齐全，数值存疑。** 台账明确10、100样本点取20次抽样的中位数，1497样本点只跑一次，屏幕注释保留了例外。十类中等概率随机猜测的期望准确率为10%；不是保证每次恰好答对30题。
- **C03：算术一致，运行结果存疑。** 300题错10题，准确率为290÷300≈96.67%，四舍五入为97%，与C02末点不冲突。
- **C04：存疑。** “第一张3”的身份及96%须核对当前模型原始输出；不能把它理解为已验证的真实正确概率。
- **C05：存疑。** A→4、92%须核对实际输入矩阵和输出；0–9分类范围与数据集类别一致。
- **C06：存疑。** 2→1、81%须核对样本、标签和输出；它与C04、C05均是本片模型结果，没有冒称外部论文成绩。
- **C07：确认。** [UCI原始页面](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)确认作者、1998年、8×8预处理及CC BY 4.0；scikit-learn文档确认其加载的是UCI原测试集。1797不是UCI完整数据集的总量，当前台账已作区分。
- **C08：核心表述有依据。** 诺奖官方检索返回正文支持“以前常要几年”以及利用已知结构和氨基酸序列训练AlphaFold2；源站全文本次返回403，未完成完整页面重读。“从已知结构里学”是删略，未说只用结构，也未把预测说成实验测定。[诺奖科普介绍](https://www.nobelprize.org/prizes/chemistry/2024/popular-information/)
- **C09：确认。** 诺奖官方摘要明确：Hassabis、Jumper共同获得一半，Baker获得另一半。“带领研发的两个人”避免了“两位论文作者”的错误归属。[诺奖官方摘要](https://www.nobelprize.org/prizes/chemistry/2024/summary/)
- **C10：确认主体、时间和单位。** 核对了署名Reuters、Krystal Hu的原稿转载：UBS研究、引用Similarweb数据、2023年1月、估计达到一亿月活、上线约两个月；不是注册人数或OpenAI官方实测。仅“过了一亿”需收紧。
- **C11：核心确认。** 核对了标明Reuters的原稿转载：十年间提交的简历、多数来自男性、含英文 *women’s* 的简历受罚、项目后来被放弃。没有发现讲稿声称实际淘汰了多少女性，或把偏见说成唯一关停原因。Reuters官网及指定存档本次均未能打开。
- **C12：层级确认，措辞需限定。** 已打开[《Deep Learning》第1章图1.4、图1.5](https://www.deeplearningbook.org/contents/intro.html)：支持AI、机器学习、深度学习的包含关系及规则系统这一分支；现代聊天大模型属于深度学习也与原论文一致。该图不支持“所有手写规则都算AI”。

专业概念方面，**测试集的教学比喻本身正确**，独立性待核实；本稿没有解释欠拟合、验证集、正则化或捷径学习，未发现这些概念的错误定义，也没有把偏见案例直接冒称捷径学习。引文中没有出现把 *part…part* 译成“一半……一半”的问题；诺奖这里的“一半”确有官方份额依据。

**最重要的 3 条**

1. 改l48：把“只会学过的”改成对陌生输入可能误判，保住泛化概念。
2. 改l32、l46、l50：消除“更多必更好”“数据全部照收”“一切都源于数据”的绝对结论。
3. 补实验复核证据与漏登记主张：尤其是模型配置、测试集独立性和三个置信度探针。

**做得好的、别改掉的**

1. 37%／88%／97%配固定考试题，并披露抽样中位数，比只挑一次好成绩更可信。
2. 诺奖保留“一半”，ChatGPT保留“估计＋月活”，亚马逊保留“据路透社＋曾想用”，归属与限定处理得好。
3. 同时展示“陌生输入高分误判”和“数字识别高分误判”，能有效支撑“预测不是真理”的提醒。

其他：无。