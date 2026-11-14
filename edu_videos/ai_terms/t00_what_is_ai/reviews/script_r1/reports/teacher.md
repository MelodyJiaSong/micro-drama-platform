# 审稿报告：好老师（例子、类比、认知与启发）· ai_terms / t00_what_is_ai · script 第 1 轮

> 只读材料：`materials/lines.md`、`learning.json`、`_shared/research/explainer_benchmark.md`。未读其他审稿报告。
> 用户补充：本系列时长不设上限、质量优先。所以有几条改法比原句长，表里标了「（较长，质量优先）」；没有为了压时长建议删内容。下面建议删的只有会教歪或加重术语负担的部分。

## 逐句问题表

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l02 | 双语 | 记录 | 标题问「什么是 AI」，全片没有一次说出全称「人工智能 / artificial intelligence」。零基础观众未必知道 AI 是哪几个词的缩写。 | zh：它是怎么学会的？这就是今天要讲的：什么是 AI，也就是人工智能。 / en: So how did it learn? That's today's question: what is AI, artificial intelligence? |
| l09 | en | 记录 | 英文这里叫 ordinary computer program，l25 叫 traditional program，同一个东西换了叫法（中文两处都是「传统程序」，没问题）。 | en: Start with a traditional computer program. People write the rules, one by one, and the computer follows them. |
| l13 | en | 记录 | 「Two bumps, one on top of the other? So does an eight.」前半句是名词短语，后面接 So does 语法上接不上，听起来别扭。（中文没问题，反例 8、5 选得好。） | en: But try writing down how. Two bumps, stacked? An eight has that too. Opens to the left at the bottom? A five does too. |
| l17–l18 | 双语 | 建议 | s3 一段里新出两个术语（l17 机器学习、l18 模型），违反「一段最多一个新术语」。另外 l18 说模型是「学出来的东西」，l22 又说「小孩就是模型」（学习者本人），前后说法不一致，见 l22。 | 两种改法任选：① 把「模型」挪到 s4，用小孩类比引出（见 l22 改法），l18 改为 zh：学会以后，来一张新图，它就能给出答案。 / en: Once it has learned, hand it a new image, and it gives you its answer. ② 保留 l18，但 l22 必须按下面改，让「模型」的意思前后一致。 |
| l19 | 双语 | 建议 | 这句其实在驳一个常见误解（AI 背后是写好的答案库），但没有点名「很多人以为」，驳斥力度弱（Muller 2008 的「先说出误解再驳」）。另外这里第一次出现「数据」，前面一直说「例子」，突然换词却没交代数据就是这些例子；后文 l41、l46、l50 都用「数据」。 | zh：很多人以为，AI 背后是程序员写好的一条条答案。其实，它的本事大多是从例子里学来的，这些例子，就叫数据。 / en: Many people think there's a programmer behind AI, typing in answers one by one. In fact, most of what it can do, it learned from examples. Those examples are its data.（较长，质量优先） |
| l22 | 双语 | 建议 | 对应关系有偏差：l18 定义「学出来的东西叫模型」，这里却把学习者本人「小孩」对应成模型。观众会以为模型是「会学习的那个人」。按 l18 的定义，应该对应到小孩学会的那套认法。 | zh：小孩学会的那套认法，就是模型；你指给他看的数字，加上你说的「这是三」，就是带答案的例子。 / en: What the child picks up, their way of telling a three, is the model. What you point at, plus your "this is a three," is an example with its answer. |
| l23 | 双语 | 记录 | 已经说出两点不像，很好。但最关键的一点没说：小孩懂「三」是什么意思，模型只是把图对到标签上。这一点 l48 正好可以回扣（见 l48），不必在这里加。 | 不改；在 l48 回扣小孩（见 l48）。 |
| l24–l25 | 双语 | 必改 | 做菜类比会教歪：① 「尝过一千道菜，自己琢磨出了菜谱」「机器学习，自己总结出菜谱」都在暗示机器学习的产出是一份人能读的菜谱（也就是规则），和上一句 l23「它学会的规律，常常连做它的人也说不清」直接矛盾，还混淆了全片的核心对比「人写的规则 vs 学出来的规律」。② 尝菜只是看到成品，没有「答案」，对不上 l16「每一张都告诉它答案」。③ 没说这个类比在哪里不像。改成「靠反馈练出手感、却写不出菜谱」，三点都能对上。改不了就删掉，小孩类比加预测机器已经够用。 | zh l24：再比如做菜。一种厨师照着菜谱，一步一步做；另一种厨师没有菜谱，做了一千道，每道都有人尝了告诉他：对了，还是咸了。 / zh l25：传统程序，是照菜谱做菜；机器学习，是靠一千次「尝了告诉你」练出手感：做得出那个味道，却未必写得出菜谱。 / en l24: Or think about cooking. One cook follows a recipe, step by step. Another has no recipe. They cook a thousand dishes, and each time someone tastes it and tells them: right, or too salty. / en l25: A traditional program cooks from the recipe. Machine learning is the cook who learned by feedback. It can make the dish, but it may never be able to write the recipe down.（较长，质量优先） |
| l27 | 双语 | 建议 | 留出考试题的做法有了，但没讲「为什么」。O3 写明「要用没见过的数据来检验」，Q3 专考这一点，讲稿里却没有一句原则性的话。补上这一句，l54「背答案」也有了伏笔。 | zh：先拿出三百张锁起来，训练的时候一张都不许看，留着当考试题：只有考它没见过的题，才知道它是真会认了，还是只是记住了。剩下的，是给它学的例子。 / en: First, we lock away three hundred of them. The model never sees them during training. They're the exam: only questions it has never seen can tell us whether it really learned, or just remembered. The rest are the examples it learns from.（较长，质量优先） |
| l27–l33 | 双语 | 记录（存疑） | 没法确认演示有没有「用考试题挑模型」：如果模型种类、参数，或「随便抽十个」用的随机种子，是看了这 300 张考题的成绩挑出来的，就等于在教数据泄漏（以前出过同类问题）。l29「37% 左右」如果只是抽了一次，「往往……左右」的说法就不准。 | 核实办法：查本期实验脚本：① 模型和参数是不是事先定好的，没看测试成绩调过；② 10 个例子那一档是不是多次随机抽取后的平均。是的话保留原句；如果只抽了一次，改成 zh：这一次随便抽的十个里，有三个数字它一张都没见过，考试只答对了37%。（按实际数字填） |
| l32 | 双语 | 建议 | 「没有人告诉它三长什么样」紧接着 l16「每一张都告诉它答案：这是三」，较真的观众会问「你明明告诉它了」，还可能误以为机器学习不用人参与。要分清「告诉它规则」和「告诉它答案」。另外 O3 写的是「越多、越全」，这里只说了「越多」。 | zh：自始至终，没有人告诉它三长什么样，只告诉它哪张是三。它见得越多、越全，认得越准。相册认猫，也是同一个道理。 / en: At no point did anyone tell it what a three looks like, only which images were threes. The more it sees, and the more kinds, the better it gets. Your photo app finds your cat the same way. |
| l33 | 双语 | 必改 | l49 说「刚才那张写得很潦草的二」，但讲稿里从没介绍过这张二。如果 l33 的画面没有把这张二标出来，观众无从「刚才」。即使画面有，解说也应该点一句，否则这次回扣会落空。 | zh：不过，三百道考题，它还是错了十道。比如这张潦草的二，它认成了一。有几张，连人看了都要犹豫。 / en: Still, out of three hundred exam questions, it missed ten. Like this scrawled two, which it read as a one. A few of them would make a person hesitate too. |
| l34 | 双语 | 建议 | 「预测」这个名字容易误导：日常说预测是指看未来（天气、股市），这里是「看到一样东西，猜它的答案」。这正属于「名字误导人时要点破」。 | zh：换个角度想：今天的 AI，其实就像一台预测机器。这里的预测不是看未来，而是看到一样东西，猜它的答案。 / en: Here's another way to see it. Today's AI is something like a prediction machine. Not predicting the future: predicting the answer for whatever you show it. |
| l37–l39 | 双语 | 建议 | s6 一段里新出三个术语：大语言模型（l37），深度学习和神经网络（l39 同一句出两个），再加上「把握」，超过一段一个的上限。神经网络在全片只出现这一次，后面再没用到，学习目标也没有它。 | 把 s6 拆成两段：s6a 预测机器（到 l37 为止，只新出大语言模型）；s6b 词的关系（l38–l40）。l39 改成先讲画面、名字只顺带提：zh：再往里是深度学习：用很多层简单计算叠起来的模型来学，你听说过的神经网络，就是这种模型。大语言模型，是深度学习的一种。 / en: Inside that is deep learning: learning with models built from many layers of simple calculations. That's what people mean by neural networks. Large language models are one kind of deep learning.（如果画面上没有「多层」的图，就删掉神经网络这半句） |
| l38 | 双语 | 必改 | 「人写规则的办法也算 AI」没交代哪些算：s2 刚把算工资、订机票说成「人写规则」的传统程序，观众顺着推就是「算工资也是 AI」，正中 Q1 的误解「凡是电脑做的事都叫 AI」。全片题目是「什么是 AI」，却从没给 AI 本身下过定义，这里就是该补的地方。 | zh：这几个词，是一个套一个的。AI 是最大的圈：让电脑做需要「聪明」的事，都算；人写规则的下棋程序也算，算工资的普通程序就不算。机器学习在它里面。 / en: These terms nest inside each other. AI is the biggest circle: any computer doing something that seems to take smarts. A chess program built from hand-written rules counts. A payroll program doesn't. Machine learning sits inside it.（较长，质量优先） |
| l40 | 双语 | 建议 | 「大家说的 AI，大多指的就是机器学习」说的是用词习惯，这在 2026 年存疑，今天多数人嘴里的 AI 指的是聊天机器人。真正想说的是 AI 背后用的技术。改成说技术，既准确，又不和误解「AI 就是聊天机器人」搅在一起。 | zh：今天你听到的 AI，几乎都是用机器学习做出来的。 / en: Almost all the AI you hear about today is built with machine learning. |
| l42 | 双语 | 记录 | 「一个往往要好几年」说重了，有的几个月就能测出来。「学会了直接预测」也可能让人以为实验不需要了，其实预测还要靠实验核对，这正好呼应 l49「预测，不是真理」。 | zh：蛋白质的形状，过去靠实验测，有的要好几年。（其余不变） / en: Working out the shape of a protein used to take lab work, sometimes for years.（其余不变） |
| l44 | 双语 | 建议 | 缺「为什么」：只说简历大多来自男性，观众推不出为什么就会扣「女子」的分。路透社原报道有一句现成的话（「in effect, Amazon's system taught itself that male candidates were preferable」），补上它，因果链就完整了，也回扣了「从例子里自己学出规律」。 | zh：但它学到的不只有规律。据路透社报道，亚马逊曾想用 AI 筛简历；可它学的，是公司过去十年收到的简历，大多来自男性。它等于自己学会了：男性候选人更好。 / en: But patterns aren't the only thing it learns. According to Reuters, Amazon once tried using AI to screen résumés. It learned from ten years of résumés sent to the company, mostly from men. In effect, it taught itself that male candidates were preferable.（较长，质量优先） |
| l48 | 双语 | 必改 | ① 「它只会它学过的」和 l21「连没见过的写法也认得出」、l32 的说法直接冲突，还会强化 Q2 的误解 C「存起来查表」。要说的是它只懂学过的那一类东西。② 92% 为什么这么高，没讲出来：把握只是在零到九这十个答案里比谁更像，所以碰到 A 也会很有把握。这是 Q4 误解 D「90% 就说明大概率对」的解药。③ 这里正好回扣小孩类比，也说出了那个类比最重要的不像之处。 | zh：第一，它只懂它学过的那一类东西。我们给它看一个字母 A：它从没见过字母，又只能在零到九里挑一个，于是一本正经地说：92%是四。小孩会说「这不是数字」，它不会：它的把握，只是在十个数字里比谁更像。 / en: One: it only knows the kind of thing it learned. We showed it the letter A. It has never seen a letter, and it can only pick from zero to nine, so it says, with a straight face: 92% sure, it's a four. A child would say, that's not a number. The model can't. Its confidence only says which of the ten digits fits best.（较长，质量优先） |
| l49 | 双语 | 记录 | 只要 l33 按上面改了，这里就能接上，不用改。 | 不改（依赖 l33）。 |
| l50 后（新增） | 双语 | 建议 | 结尾只有总结和下期预告，缺一个让人带走、下次用 AI 时会想起来的问题。这一句把 O4（把握）和 O6（数据）收到同一个日常场景里，不引入新术语。 | zh（新增，放在 l50 之后）：下次 AI 很有把握地回答你，不妨想一想：这种问题，它学过吗？ / en (new, after l50): Next time an AI answers you with total confidence, ask yourself: has it ever learned this kind of question? |
| 全片 | zh | 记录 | 全片的核心对比是「规则（人写的）vs 规律（学出来的）」，两个词中文只差一个字，听的时候容易混（英文 rules / pattern 分得开）。 | 画面上两词固定配不同颜色与标签：「规则·人写的」「规律·学出来的」；解说不改。 |

## 必查项逐条说明

1. **例子与类比逐点映射**（结论：猫 留；手写三和反例 8、5 留；小孩 改；做菜 改，改不了就删；考试题 留；预测机器 留；亚马逊 改；字母 A 改）
   - 相册认猫（l01/l32）：对应「没人写规则，是从例子学的」。会误导的地方：「没人告诉它」会被理解成不需要人标答案，按 l32 改法修。留。
   - 手写三（l11–l14）：对应「规则说不清、写不完」。8、5 两个反例正好演示两种错：漏掉真的三、把别的数字当成三（l14）。映射准确，留。
   - 小孩认数字（l20–l23）：例子对应带答案的样本，「连没见过的写法也认得出」对应泛化。会误导的地方：「小孩=模型」和 l18 的定义不一致。改。
   - 做菜（l24–l25）：会教歪，见表。改，改不了就删。
   - 锁起来的考试题（l27）：对应测试集，映射清楚，但缺「为什么」。留并补一句。
   - 预测机器（l34–l37）：对应输入 → 带把握的答案，并把图片、声音、文字三种任务统一起来。会误导的地方：「预测」一词，见 l34。留。
   - 亚马逊（l44–l46）：对应「数据里的偏见也会被学到」，事实与路透社 2018 年报道一致（women's、女子国际象棋社、工具被放弃）。因果链缺一环，改。
   - 字母 A（l48）：对应「没学过的东西也会硬给答案」，例子很好，只是措辞「只会它学过的」会教歪。改。
2. **类比是否显式对应、是否说出失效**：小孩类比做到了：l22 对应，l23 说出两点不像。做菜类比有对应（l25），没说失效，而且对应本身和 l23 矛盾。预测机器没说边界，按 l34 补一句点破就够了。
3. **两个不同例子并比较**：有。算工资、订机票（规则说得清）对比手写三（说不清），判断标准在 l10/l11 明说了，直接支撑 O2 和 Q1。照片、声音、半句话（l36–l37）用同一个句式并列，比较的是共同结构。手写数字和认猫在 l32 点了「同一个道理」，比较偏弱但够用。改 l48 后还会多一组「小孩 vs 模型」的显式比较。
4. **认知提升**：不只是一个定义，而是给了三个能带走的思考方法：① 规则写得清就写，写不清才学（O2）；② 预测机器加把握；③ 先问数据（l50）。「为什么」讲到了：为什么规则写不完（l13–l14），为什么 10 个例子不够（l29：有些数字一张都没见过，讲得很好）。没讲到的：为什么要留考题（l27），为什么把握高也会错（l48），为什么会学到偏见（l44）。都已在表里给了补法。
5. **误解**：已点名或驳斥的有：答案库（l19，力度偏弱）、AI 是客观的（l46）、把握高就对（l49）、AI 只是聊天机器人（l38–l40）。逐句找到四处可能制造新误解的地方：l25（机器学习能写出可读的菜谱）、l38（算工资也是 AI）、l48（查表式「只会学过的」）、l32（不用人标答案）。
6. **启发**：中段有 l28「先猜一下」，有 l23「连做它的人也说不清」这个耐人寻味的点；结尾有 l50 的实用视角和 l54 的悬念问题。缺一个让人看完还会想的问题，补法见「l50 后（新增）」。讲稿里没有「学习即压缩」这类引申视角，所以不存在过度引申的问题。
7. **术语**：先画面后名字基本做到了（先看一堆三，l17 才说出「机器学习」；先实验，后说「预测机器」）。一段一个术语的规则有两处超了：s3（机器学习、模型）和 s6（大语言模型、深度学习、神经网络）。叫法前后不一致的有两处：例子换成数据（l19）、英文 ordinary 和 traditional 混用（l09/l25）。名字误导、但没点破的是「预测」（l34），「把握」的点破放在 l48。最后一分钟没有引入新术语：l54 的「过拟合」只是下期预告，可以接受。
8. **对照 learning.json**：
   - O1：l09、l15–l17、l52–l53 支撑清楚。l25 现在是反向支撑，要改。
   - O2：l10、l11、l13、l14 清楚。
   - O3：「越多」清楚（l29–l31），「越全」只有 l29 间接体现，「要用没见过的数据检验」缺一句原则，按 l27、l32 补。
   - O4：l35、l48、l49 有，但「把握为什么不代表对」缺机制，按 l48 补。
   - O5：l38–l40 有，但「人写规则也算 AI」缺边界，会和 Q1 冲突，按 l38 改。
   - O6：l44–l46、l50 清楚，l44 补上因果更稳。

## 最重要的 3 条

1. **l24–l25 做菜类比会教歪**：「机器学习自己总结出菜谱」暗示它学出的是人能读的规则，和 l23 直接矛盾，也混淆了全片的核心对比，而且没有说出类比在哪里失效。改成「靠反馈练出手感，却写不出菜谱」，改不了就删。
2. **l38「人写规则的办法也算 AI」没有边界，全片也从没定义 AI**：观众会推出「算工资也是 AI」，正中 Q1 的误解。在这里补一句定义：做需要「聪明」的事；下棋程序算，算工资不算。
3. **l48「它只会它学过的」和 l21/l32 的泛化说法冲突**，会强化「查表」误解；而且没讲把握只是在十个答案里比谁更像。改成「只懂它学过的那一类东西」，再回扣小孩类比，补上把握的机制。另外，l33 要先把那张潦草的二点出来，否则 l49 的「刚才那张」接不上（同为必改）。

## 做得好的、别改掉的

1. s2 用反例拆掉规则（「八也是」「五也是」），l14 同时点出漏判和误判两种错：画面感强，「为什么规则写不完」讲得真透。
2. 小孩类比有显式对应（l22），还主动说出两点不像（l23），完全符合「对应加失效」的要求。按 l22 改过对应关系后保持这个结构。
3. 实验段先让观众猜（l28），10、100、1500 三档逐步递进，并解释了 10 个为什么不够（l29），还坦白承认错题（l33），再用字母 A 演示模型硬答。最后落到 l50「先问它是从什么数据里学的」，是一个能带走的思考方法。

## 其他

- Q4 选项 D「90% 说明它有九成可能是对的」：在学过的题上，一个校准良好的模型给 90% 确实大致如此。这个干扰项只有在「兔子」这个题境下才错，建议题干或选项写明「在这张兔子图上」，避免较真的人质疑。
