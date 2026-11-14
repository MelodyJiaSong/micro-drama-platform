# 审稿报告：好老师（例子、类比、认知与启发）

ai_terms / t01_overfitting · script 第 1 轮 · 独立审稿（只读了 lines.md、learning.json、explainer_benchmark.md）

## 逐句问题表

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l12 | 双语 | 记录 | l08 承诺"模型一句话讲清"，l12 只说了模型的任务，没说在画面里模型就是那条曲线；后面"第一种模型只会画直线"要靠观众自己接上。 | zh：模型，就是从这些点里找出规律的那条曲线，好拿去预测没见过的新数据。<br>en: The model is the curve that finds the pattern in these points, so it can predict new data it has never seen. |
| l13 | 双语 | 必改 | ①"误差……越小越好"直接种下 O5 和 explain_back 要驳斥的误解"训练误差越低越好"：两句之后（l15）误差为零的模型恰恰是坏模型。②名字在画面之前（"先说误差"，线还没画出来就先下定义）。③同一句里塞进两个新术语（误差、欠拟合）。 | zh：第一种模型太简单，只会画直线。点到线的距离叫误差；它连练习题上的误差都压不下来，这叫欠拟合。<br>en: Model one is too simple. It only draws a straight line. The gap from each point to the line is the error, and it can't even shrink that on the practice problems. That's underfitting. |
| l20 | 双语 | 建议 | 讲了"背下了噪声"，没讲**为什么**背了噪声换到新数据就错：噪声是随机的，新数据里不会重演。这句正是"怎么想"的关键一步。另外"拟合"二字从头到尾没解释，中文观众不一定懂。 | zh：它连噪声也背了下来，可噪声到了新题不会重演。这就是过拟合。（画面卡：拟合 = 让曲线贴住点；贴过了头 = 过拟合）<br>en: It memorized the noise too, and noise never repeats in new data. That's overfitting. |
| l21 | 双语 | 必改 | 对照 O2：讲稿里没有一句说欠拟合是"**两种误差都高**"（s4 只考了模型二、三，模型一的考试误差没出现）。对照 O5："练习误差为零≠好模型"只是暗示，没有点名。 | zh：欠拟合，练习和考试都差，一眼就看得出；过拟合更危险：练习误差为零，看起来好极了。<br>en: An underfit model is bad on both, so you spot it fast. An overfit model is more dangerous: zero practice error, and it looks great. |
| l22 | 双语 | 建议 | 学生类比里没有和"噪声"对应的东西：背下来的都是对的答案，而模型背下的恰恰包括噪声。补一个"印错的答案"，类比就能逐点对上。 | zh：有个学生把练习册答案全背了下来，连印错的几处也照背。练习册上，他次次满分。<br>en: Picture a student who memorizes every workbook answer, misprints included. On the workbook, he scores a hundred every time. |
| l24 | 双语 | 建议 | 映射说得很明确（好），但没有映射噪声；配合 l22 补上。 | zh：对上实验：练习册是训练数据，印错的答案是噪声，考试是新数据；死记硬背，就是那条硬穿过每个点的曲线。<br>en: Map it back: the workbook is the training data, the misprints are noise, the exam is new data, and cramming is that curve forced through every point. |
| l25–l26 | 双语 | 必改 | 认猫的例子讲的不是过拟合，是**虚假相关 / 捷径学习**：小朋友学到的"沙发 = 猫"是一条**很简单**的规则，病根是照片太单一（数据偏），不是"记得太多"。限制复杂度治不了它，换更多样的照片才行（l46）。这正是"狗的例子其实是欠拟合吧？"那类评论会抓的问题。例子本身好懂，而且正好铺垫 l43 和测验 Q5，所以建议**留下但改标签**（见 l27），不要再当成过拟合的同一件事。 | l25–l26 原文保留，改 l27 和 l43。 |
| l27 | 双语 | 必改 | ①"两个例子是同一件事"和 l43"捷径学习是过拟合的**近亲**"前后矛盾。②"模型只是被允许记得太多"放在认猫例子后面，把病因说错了。③说出的"不像之处"是"模型不会偷懒"，但背完整本练习册并不算偷懒，这一条没打中要害。另外，两个例子只比了共同点，没比差异，算不上真正的"两个例子做比较"。 | zh：两个都把只在手头数据里成立的东西当了真：学生是记得太多，小朋友是见得太少。类比不像的地方：模型不是故意死记，只是被允许记太多。<br>en: Both took something true only of the data at hand as the rule. The student remembered too much; the child saw too little. Where the analogy breaks: a model doesn't choose to cram. It's just allowed to remember too much. |
| l28 | 双语 | 建议 | "重复三百次，让模型从简单变到复杂"有歧义，听起来像是有三百档复杂度（十个点最多只能到十个数字）。存疑：要和实验代码核对"三百"到底指什么，按实际改。 | zh：回到实验：换三百组随机的点，各做一遍，看模型由简到繁时，两种误差平均怎么变。<br>en: Back to the experiment. We rerun it on 300 fresh sets of random points and watch how both errors change, on average, as the model gets more complex. |
| l29–l31 | 双语 | 记录 | 讲稿一直用"练习误差 / 考试误差"，标准叫法"训练误差 / 测试误差"一次也没出现；learning.json O2 和测验 Q4 用的是"训练 / 测试集"。英文里数据叫 training/test data，误差却叫 practice/exam error，配对不一致。这一期是"高频词"系列，观众出去会碰到标准叫法。 | 讲稿不改；l29 画面标签第一次出现时并列"练习误差（训练误差）""考试误差（测试误差）"，英文 "practice (training) error" / "exam (test) error"。 |
| l33 | 双语 | 建议 | "学习，其实是一种压缩"把一个视角（最小描述长度的思路）说成了事实，说过头了。 | zh：换个角度想：学习，可以看成一种压缩。<br>en: Here's another way to see it. Learning can be seen as a kind of compression. |
| l35 | 双语 | 建议 | "四个数字"出现得很突然：前面从没说过曲线是由几个可调的数字定下来的（直线用两个也没提）。观众不知道数的是什么。 | zh：第二种曲线由四个可调的数字定下，就把它们大致说清了，还能说中没见过的点。<br>en: Model two is set by just four adjustable numbers. That describes them roughly, and still comes close on points it has never seen. |
| l36 | 双语 | 建议 | "它不用找规律，所以也就没找"把模型说成会偷懒，和 l27 说的"模型不是故意的"打架。（"十个数字配十个点"这一层本身讲得很准，要保留。） | zh：第三种模型有十个数字，正好够把十个点原样存下。没有什么逼它去找规律，它也就没找。<br>en: Model three has ten numbers, exactly enough to store all ten points as they are. Nothing forced it to find the pattern, so it didn't. |
| l36 / l47 | 双语 | 记录 | 现在"正好够"的措辞是准确的。但画面、简介和以后几期都别引申成"参数比数据多就一定过拟合"：现代大模型的参数远多于数据，照样能泛化（双降现象，对标里有 Welch Labs 那一期）。 | 不改；画面上别写"参数越多 → 越过拟合"这类箭头。 |
| l37 | 双语 | 建议 | ①"用更少的东西，解释更多的事"是全片最容易引申过度的一句，而且和 l32"不是越简单越好"有冲突（观众可能只记住"越少越好"）。②压缩视角里最关键的一点没说：有损压缩**丢掉的那部分，正好是噪声**。说出这一点，s7 才能和 l20 接上。 | zh：好的压缩，丢掉的恰好是噪声；留下来的，才是规律。<br>en: Good compression throws away exactly the noise. What's left is the pattern. |
| l39 | 双语 | 建议 | 没有对应回实验："五千万个词去凑一千多个点"正是 l36 的"自由度比数据多"，这是全片最好的一次迁移机会，却没点明。只说"测冬天"，观众容易理解成别的事（季节混淆）。 | zh：谷歌曾用搜索记录估算流感：从五千万个词里，挑最贴合一千多个历史点的那些。可挑的远比点多，就像十个数字配十个点；结果它一半在测流感，一半在测冬天。<br>en: Google once estimated flu from searches, picking from 50 million terms the best fit to about 1,100 data points. Far more choices than points, like ten numbers for ten points. It became part flu detector, part winter detector. |
| l42 | zh | 建议 | 中文没有英文 "With the marks" 那层限定，读起来像是**所有**良性痣里一半多都被判成癌，会造成新的误解。 | zh：还有一个识别黑色素瘤的系统，被医生在皮肤上画的标记骗了：画了标记的良性痣，一半多被它判成了癌。 |
| l43 | 双语 | 建议 | 和 s5 的认猫例子接上（配合 l27 的改法），让"近亲"这层关系前后一致。 | zh：后两个例子，和认猫的小朋友一样，叫捷径学习，是过拟合的近亲：在手里的数据上亮眼，学到的却是巧合。<br>en: Those last two, like the child and the cats, are shortcut learning, a close cousin of overfitting: brilliant on the data at hand, but what they learned was coincidence. |
| l47 | 双语 | 建议 | "正则化"这个名字对普通观众是不透明的（中文"正则"容易联想到正则表达式），属于"名字误导人时要点破"的情况；对标里还提到过专家嫌"正则化说得太粗"。s9 一段引入两个术语（验证集、正则化），因为是列清单，可以接受。 | zh：第三，给模型的复杂度立规矩，别让它有本事把每个点都背下来。这叫正则化，"正则"就是立规矩。<br>en: Three: put limits on the model's complexity so it can't memorize every point. That's regularization: keeping the model in line. |
| s10（l50 后） | 双语 | 建议 | 结尾只重复了定义和下一期预告，没有一个让人愿意再想一想的问题。注意：对标里提到的论语梗"学而不思则欠拟合"和本片的定义相反（本片说死记 = 过拟合），**别用**。 | 在 l50 后加一句：<br>zh：下次你觉得自己全懂了，换一道没见过的题试试。<br>en: Next time you're sure you've got it, try a question you've never seen. |
| s2 / s3 | 双语 | 记录 | 一段两个新术语：s2 是训练数据和噪声，s3 是误差和欠拟合。s2 都是先给画面，问题不大；s3 按 l13 的改法先画面后命名，就能减轻负担。 | 见 l13。 |
| 全片 | 双语 | 记录 | explain_back 列出的误解"过拟合就是训练不够"讲稿没有点名驳斥。l15"误差是零"和改后的 l21"练习误差为零"已经从侧面驳了，暂时够用。 | 不另加句子；后测观察这一项误解的出现率。 |

## 必查项核对（逐项证据）

1. **例子与类比逐点映射**
   - 十个点 + 三种模型：数据、噪声、复杂度、零误差、考试一一对应。判"留"。
   - 学生背练习册：练习册对训练数据、考试对新数据、背答案对穿过每个点的曲线（l24），只缺噪声。判"改"，见 l22 / l24。
   - 认猫：概念对错了（是虚假相关，不是过拟合）。判"改标签留下"，见 l25–l27。
   - 学习即压缩：大方向对，结论说过头了。判"改"，见 l33 / l37。
   - 谷歌流感：判"改"，要对应回实验（l39）。
   - 胸片、黑色素瘤：判"留"，l43 已经正确归到捷径学习；l42 中文要补限定。
2. **类比是否显式对应、是否说出失效处**：学生类比有显式对应（l24），也说了一处不像（l27），但那一处没打中要害。认猫例子没有对应回实验，失效处也没说。已给出改法。
3. **两个不同例子并比较**：有两个（学生、认猫），但 l27 只说了"同一件事"，没有比出差异。改后变成"记得太多 vs 见得太少"的对照，还正好对应两种不同的对策（l47 限制复杂度 / l46 更多样的数据）。
4. **认知提升 / 为什么**：有心智模型。一是"两种误差一起看"的诊断法（l31），二是"自由度够就不必找规律"（l36），三是压缩视角。缺"噪声为什么在新数据上害人"这一步（l20），以及"压缩丢掉的就是噪声"（l37）。已给出改法。
5. **误解**：明确点名并驳斥了"越简单越好"（l32），还有"程序写错了"（l02）。逐句排查，发现会制造新误解的有：l13"误差越小越好"（必改）、l27 把捷径学习说成同一件事、l37 可能被听成"越少越好"、l42 中文指代范围不清、l36 拟人成偷懒。
6. **启发**：中段有一个先猜问题（l16，好）。压缩视角有启发性，但 l33"其实是"和 l37 说过头了。结尾缺一个开放的问题，已给出一句。
7. **术语**：训练数据、噪声、测试数据、验证集、捷径学习、正则化都是先给画面或描述，再给名字。例外是 l13 的误差（先名字，而且一句两个术语）。叫法前后一致：练习 / 考试一套用到底，没有中途换名（好），但没有和标准叫法"训练误差 / 测试误差"挂钩。正则化、拟合这两个名字不透明，也没有点破。
8. **对照 learning.json**
   - O1：有支撑（l09、l20、l49–l50，加上 l01 的"换到新数据就不行"）。
   - O2：只有"过拟合信号"那一半有支撑（l31）；"两种都高 = 欠拟合"**没有支撑句**，改 l21。
   - O3：有支撑（l15、l36）。
   - O4：有支撑（l45–l47，三种对策各自解决什么都说了）。
   - O5："不是越简单越好"有支撑（l32）；"零训练误差≠好模型"只是暗示，而且被 l13 的"越小越好"抵消，改 l13、l21。

## 最重要的 3 条

1. **l25–l27 认猫例子对错了概念**：它是捷径学习（数据太单一），不是"记得太多"。"同一件事"和 l43 的"近亲"也互相矛盾。改成"学生记得太多，小朋友见得太少"的对照。
2. **l13"误差越小越好"**：在讲稿里亲手种下了"训练误差越低越好"这个误解，而且名字先于画面。删掉这几个字，改成先画距离再命名。
3. **l21 补上学习目标的支撑句**：O2 缺"欠拟合是两种误差都高"，O5 的"练习误差为零≠好模型"没点名。用一句话同时补上。

## 做得好的、别改掉的

- l45 主动承认"刚才为了演示，直接拿考试挑了模型"，再引出验证集：把数据泄漏这个老坑提前堵住了。
- l32 用自问自答点名驳斥"越简单越好"；l21 的"过拟合更危险，因为看起来好极了"，给了观众一个真正有用的判断视角。
- l36"十个数字，正好够把十个点原样存下"：一句话讲清"为什么复杂会过拟合"，和测验 Q3 完全对应；l16 先猜后揭晓的节奏也别动。

## 其他

- l19"二十多倍"和 l35"四个数字"属于存疑：要和实验代码的实际输出（模型二的次数、两种模型的考试误差之比）核对，并确认是单次实验的结果还是三百次的平均。
- l40"后来的版本也没好多少"：原研究把 2011–2013 年的高估一部分归因于搜索算法改动和媒体报道，不只是过拟合，建议请事实核查角色再看一下措辞。
