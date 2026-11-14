# 审稿汇总：script_r1

必改 20 · 存疑 0 · 建议 63 · 记录 92；「多人」= 两个以上角色指到同一句。处理结论写在最后一列（改 / 不改＋理由）。

| 句号 | 语言 | 级别 | 角色 | 多人 | 问题 | 建议改法 | 处理 |
|---|---|---|---|---|---|---|---|
| s1 | 双语 | 建议 | editor |  | 目录开场，和 v2 是同类问题。冷开场之后接 5 句目录（约 18 秒），把定义推到约 30 秒才出现。目录既不是反差也不是问题，而且和实际章节对不上（漏了 s6「一张图」）。 | 删 l03–l07，冷开场直接接 l08 / l09。如果包装卡必须保留，只留 l08 一句。 |  |
| l01 | zh | 记录 | native_zh | ★ | **自然。**“几乎满分／错得一塌糊涂”对比清楚，分号处可换气。 | 保留原句。 |  |
| l01 | en | 记录 | native_en | ★ | 自然。“meets new data”“falls apart”口语化，转折清楚，两句都易读。 | 保留。 |  |
| l02 | 双语 | 建议 | factcheck | ★ | 仅凭“旧数据好、新数据差”，还不能排除程序问题或数据分布变化，直接确诊过拟合过满。 | zh：这可能不是程序出错，而是过拟合。<br>en：One possible culprit is overfitting. |  |
| s2 | 双语 | 记录 | teacher |  | 一段两个新术语：s2 是训练数据和噪声，s3 是误差和欠拟合。s2 都是先给画面，问题不大；s3 按 l13 的改法先画面后命名，就能减轻负担。 | 见 l13。 |  |
| l02 | zh | 记录 | native_zh | ★ | **自然。**“犯的毛病”口语顺畅。“过拟合”首次出现，纯听觉能否辨词存疑，需核实首次出现时是否有术语字幕。 | 保留原句；“叫过拟合”连读完整，勿在术语内部停顿。 |  |
| l02 | en | 记录 | native_en | ★ | 自然。短句先排除直觉解释，再引入术语，重音明确。 | 保留。 |  |
| l03 | zh | 记录 | native_zh | ★ | **自然。**短句，适合引出目录。 | 保留原句。 |  |
| l03 | en | 记录 | native_en | ★ | 自然。常见口头引导语；后面的项目应接着读，不宜每项都读成独立宣告。 | 保留。 |  |
| l03 | en | 记录 | bilingual | ★ | 中文说「讲四件事」，英文没有说是四件，跟议程卡上的四项对不上。 | en：Four things today. |  |
| l04 | zh | 记录 | native_zh | ★ | **自然。**承接“四件事”，省略成分可从上句补足。 | 保留原句。 |  |
| l04 | en | 记录 | native_en | ★ | 自然。作为 l03 引出的议程项目，句子片段成立。 | 保留。 |  |
| l05 | zh | 建议 | native_zh | ★ | **有点怪。**目录里突然报出“一个学生”，听着像人物名单，没说清要讲学生的什么问题。 | 为什么只背练习册不行； |  |
| l05 | en | 建议 | native_en | ★ | 稍别扭。突然报出“A student…”像念幻灯片标题，与前面的“What…”衔接不够顺，也没说明要讲学生的什么。 | Why memorizing answers fails. |  |
| l06 | zh | 记录 | native_zh | ★ | **自然。**“换个角度看学习”是顺口的口语表达。 | 保留原句。 |  |
| l06 | en | 记录 | native_en | ★ | 自然。作为议程项目成立；“a different way to think about…”是自然表达。 | 保留。 |  |
| l07 | en | 建议 | native_en | ★ | 稍别扭。两个“and”拖长收尾；“it”在听觉上可能接到上一句的“learning”，使人短暂听成“学习造成的麻烦”。 | Then, real-world failures—and how to avoid them. |  |
| l07 | zh | 记录 | native_zh | ★ | **自然。**“闯过的祸”“怎么防”有口语感，“它”能回指过拟合。 | 保留原句。 |  |
| l08 | zh | 建议 | native_zh | ★ | **有点怪。**“片中都会一句话讲清”搭配略硬，少了“用”的连接。 | 不懂模型、训练数据也没关系，都会用一句话讲清。 |  |
| l08 | 双语 | 记录 | editor | ★ | 有帮助，但「片中都会一句话讲清」是元话语，删 s1 后可以再短一点。 | zh：不懂模型也没关系，片中都会讲清。 / en: No background needed. We'll explain as we go. |  |
| l08 | en | 记录 | native_en | ★ | 自然。“No background needed”是常见口语省略，后一句完整承接，没有孤立口号感。 | 保留。 |  |
| l09 | 双语 | 必改 | factcheck | ★ | “背下来了，却没学会规律”把极端类比当成定义。过拟合可以同时学到规律和噪声，也不要求逐点记忆。[概念依据](https://www.deeplearningbook.org/contents/ml.html) | zh：先给一句话：过拟合，就是太贴合练习题，反而做不好同类新题。下面看个小实验。<br>en：Overfitting means fitting practice data too closely to do well on similar new data. Let's see a small experiment. |  |
| l09 | zh | 建议 | native_zh | ★ | **有点怪。**“先给一句话”像讲解提纲里的提示语，直接进入解释更顺。 | 过拟合，就是把练习题背下来了，却没学会规律。下面用一个小实验看清楚。 |  |
| l09 | 双语 | 记录 | editor | ★ | 「先给一句话」「下面用一个小实验看清楚」都是过渡性的废话，把定义夹在中间。 | zh：一句话：过拟合，就是把练习题背下来了，却没学会规律。来看个小实验。 / en: In one sentence: overfitting is memorizing the practice problems without learning the pattern. Here's a small experiment. |  |
| l09 | en | 记录 | native_en | ★ | 自然。定义句稍长，但可在“overfitting”后及“without”前自然分组；没有绕口结构。 | 保留。 |  |
| s10 | 双语 | 建议 | teacher |  | 结尾只重复了定义和下一期预告，没有一个让人愿意再想一想的问题。注意：对标里提到的论语梗"学而不思则欠拟合"和本片的定义相反（本片说死记 = 过拟合），**别用**。 | 在 l50 后加一句：<br>zh：下次你觉得自己全懂了，换一道没见过的题试试。<br>en: Next time you're sure you've got it, try a question you've never seen. |  |
| l10 | zh | 记录 | native_zh | ★ | **自然，画面指代存疑。**“这十个点”需要观众当时能看到对应对象；仅凭讲稿不能确认。 | 保留原句；核实“这十个点”出口时，十个点已经出现。 |  |
| l10 | en | 记录 | native_en | ★ | 自然。“training data”随即用练习题解释。存疑：“These ten points”的视觉指向需在对应画面出现时核实。 | 文字保留；核对“these”说出口时十个点已出现。 |  |
| l11 | en | 建议 | native_en | ★ | 稍别扭。“some pattern”含糊，句尾再补“at random”像临时追加说明，口播容易读散。 | They follow a pattern, but each point is slightly off. Those random differences are noise. |  |
| l11 | zh | 记录 | native_zh | ★ | **自然。**虽有“分布”“偏差”等解释用词，但句法顺，“它们”明确指前句的点。 | 保留原句。 |  |
| l12 | 双语 | 记录 | teacher | ★ | l08 承诺"模型一句话讲清"，l12 只说了模型的任务，没说在画面里模型就是那条曲线；后面"第一种模型只会画直线"要靠观众自己接上。 | zh：模型，就是从这些点里找出规律的那条曲线，好拿去预测没见过的新数据。<br>en: The model is the curve that finds the pattern in these points, so it can predict new data it has never seen. |  |
| l12 | zh | 记录 | native_zh | ★ | **自然。**“好去预测”缓和了术语带来的书面感，逗号处分两拍即可。 | 保留原句。 |  |
| l12 | en | 记录 | native_en | ★ | 自然。“find the pattern”到“predict new data”的目的关系清楚，句长可控。 | 保留。 |  |
| l13 | 双语 | 必改 | teacher | ★ | ①"误差……越小越好"直接种下 O5 和 explain_back 要驳斥的误解"训练误差越低越好"：两句之后（l15）误差为零的模型恰恰是坏模型。②名字在画面之前（"先说误差"，线还没画出来就先下定义）。③同一句里塞进两个新术语（误差、欠拟合）。 | zh：第一种模型太简单，只会画直线。点到线的距离叫误差；它连练习题上的误差都压不下来，这叫欠拟合。<br>en: Model one is too simple. It only draws a straight line. The gap from each point to the line is the error, and it can't even shrink that on the practice problems. That's underfitting. |  |
| l13 | 双语 | 必改 | factcheck | ★ | 台账使用 MSE，解说却只说“距离”，未说明是纵向误差的平方平均；“对不上练习题”也容易让观众把不穿过所有点当作欠拟合，与 l14 冲突。 | zh：这里的误差，是预测与实际高度差平方的平均值。第一种只会画直线，连整体弯曲趋势都抓不住，这叫欠拟合。<br>en：Here, error means the average squared difference between predicted and actual heights. Model one draws a straight line and misses even the overall bend. That's underfitting. |  |
| l13 | 双语 | 建议 | editor | ★ | 一句塞了两个新概念（误差的定义和欠拟合），观众还要同时看第一条直线。误差定义埋在「第一种」前面，不容易被注意到。 | 拆成两句。zh：l13a「先说误差：点离曲线有多远，越小越好。」l13b「第一种模型太简单，只会画直线，连练习题都对不上。这叫欠拟合。」 / en: l13a "First, error: how far the points are from the curve. Smaller is better." l13b "Model one is too simple. It only draws a straight line and misses even the practice problems. That's underfitting." |  |
| l13 | zh | 建议 | native_zh | ★ | **有点怪。**“点和曲线差得有多远”混用了“相差多少”和“离得多远”两种说法。整条已有句号，不必强行一口气读完。 | 先说误差：点离曲线多远，误差就多大，越小越好。第一种模型太简单，只会画直线，连练习题都对不上，这叫欠拟合。 |  |
| l13 | en | 建议 | native_en | ★ | 稍别扭。“First, error:”像念术语卡；“match the practice problems”搭配也偏生硬，听众可能不清楚是匹配题目还是答题表现。 | Error means how far the points are from the curve. Smaller is better. Model one is too simple. It draws a straight line and struggles even with the practice problems. That's underfitting. |  |
| l14 | zh | 记录 | native_zh | ★ | **自然。**“第二种，一条……”是可接受的口语省略；“它”紧接曲线，指代清楚。 | 保留原句。 |  |
| l14 | en | 记录 | native_en | ★ | 自然。“gentle curve”“overall trend”搭配正常，第二句转折顺畅。 | 保留。 |  |
| l15 | zh | 记录 | native_zh | ★ | **自然。**“拐来拐去”“硬是”顺口，句号已提供换气位置。 | 保留原句。 |  |
| l15 | en | 记录 | native_en | ★ | 自然。“twists and turns”有口语节奏，“every single point”重音清楚。 | 保留。 |  |
| l16 | zh | 记录 | editor | ★ | 第三次用「先」开头（l09「先给」、l13「先说」）。 | 猜一猜：换成新题，哪一种考得最好？ |  |
| l16 | zh | 记录 | native_zh | ★ | **自然。**问句短，重音容易落在“哪一种”。 | 保留原句。 |  |
| l16 | en | 记录 | native_en | ★ | 自然。“Quick guess”在邀请观众参与时成立，后面有完整问题，不像孤立的议程碎句。 | 保留。 |  |
| l17 | zh | 必改 | editor | ★ | 「拿出六个模型从没见过的新点」听起来像「六个模型」。纯听配音时一定会误解，以为出现了六个模型。 | 再拿六个新点，模型都没见过。这叫测试数据，相当于考试。 |  |
| l17 | zh | 建议 | native_zh | ★ | **有点怪。**“六个模型从没见过的新点”定语偏长，听到“六个模型”时容易先误分组。 | 拿出六个新点，模型从没见过。这叫测试数据，相当于考试。 |  |
| l17 | en | 记录 | native_en | ★ | 自然。新点、测试数据、考试三个表达逐步衔接；“This”有紧邻的明确指代。 | 保留。 |  |
| l18 | 双语 | 建议 | editor | ★ | l16 问的是「哪一种考得最好」，l18 只说「考得不错」，没有给出明确答案，问答没有接上。 | zh：第二种曲线，离新点都不远，考得最好。 / en: Model two stays close to the new points. It does best. |  |
| l18 | zh | 记录 | native_zh | ★ | **自然。**对象、距离、评价依次展开，口语节奏清楚。 | 保留原句。 |  |
| l18 | en | 记录 | native_en | ★ | 自然。两句短而清楚，适合留时间给观众看图。 | 保留。 |  |
| l19 | en | 建议 | factcheck | ★ | “twenty times higher than”存在倍数歧义，中文“是……二十多倍”和画面倍率表达更明确。 | 仅替换末句：Its test error is over twenty times model two's. |  |
| l19 | zh | 建议 | native_zh | ★ | **很怪。**“有的新点一下就差出去很远”搭配不稳，距离关系不清，听感还像新点自己移了位置。 | 第三种曲线，在点和点之间乱拐，离有些新点很远。它的考试误差，是第二种的二十多倍。 |  |
| l19 | zh | 记录 | editor | ★ | 约 45 字，字幕要分两屏。「一下就差出去很远」偏口语，意思也模糊。 | 第三种曲线在点之间乱拐，有的新点离它很远。它的考试误差，是第二种的二十多倍。 |  |
| l19 | en | 记录 | native_en | ★ | 小瑕疵。“twenty times higher than”口语常见，但比较倍数有解释歧义；直接说“twenty times”更干净。 | Model three swings wildly between the points, and some new points land far from its curve. Its exam error is more than twenty times model two's. |  |
| l20 | 双语 | 建议 | teacher | ★ | 讲了"背下了噪声"，没讲**为什么**背了噪声换到新数据就错：噪声是随机的，新数据里不会重演。这句正是"怎么想"的关键一步。另外"拟合"二字从头到尾没解释，中文观众不一定懂。 | zh：它连噪声也背了下来，可噪声到了新题不会重演。这就是过拟合。（画面卡：拟合 = 让曲线贴住点；贴过了头 = 过拟合）<br>en: It memorized the noise too, and noise never repeats in new data. That's overfitting. |  |
| l20 | zh | 记录 | native_zh | ★ | **自然。**“也一起背了下来”能接住前面的学生比喻，落点明确。 | 保留原句。 |  |
| l20 | en | 记录 | native_en | ★ | 自然。“along with everything else”自然补充了“连噪声一起记住”的意思。 | 保留。 |  |
| l21 | 双语 | 必改 | teacher | ★ | 对照 O2：讲稿里没有一句说欠拟合是"**两种误差都高**"（s4 只考了模型二、三，模型一的考试误差没出现）。对照 O5："练习误差为零≠好模型"只是暗示，没有点名。 | zh：欠拟合，练习和考试都差，一眼就看得出；过拟合更危险：练习误差为零，看起来好极了。<br>en: An underfit model is bad on both, so you spot it fast. An overfit model is more dangerous: zero practice error, and it looks great. |  |
| l21 | 双语 | 建议 | factcheck | ★ | “一眼就能看出”“更危险”都是无条件判断；可直接解释为何容易漏检。 | zh：欠拟合，练习题就做不好；过拟合容易漏看，因为训练成绩可能很好。<br>en：Underfitting shows up on practice data. Overfitting can be harder to spot because training scores may look excellent. |  |
| l21 | zh | 记录 | native_zh | ★ | **自然。**“一眼就能看出”“好极了”口语感强；分号处停顿即可。 | 保留原句。 |  |
| l21 | en | 记录 | native_en | ★ | 自然。术语前文已引入；“looks great”符合面向普通观众的口吻。 | 保留。 |  |
| l22 | 双语 | 建议 | teacher | ★ | 学生类比里没有和"噪声"对应的东西：背下来的都是对的答案，而模型背下的恰恰包括噪声。补一个"印错的答案"，类比就能逐点对上。 | zh：有个学生把练习册答案全背了下来，连印错的几处也照背。练习册上，他次次满分。<br>en: Picture a student who memorizes every workbook answer, misprints included. On the workbook, he scores a hundred every time. |  |
| l22 | zh | 记录 | editor | ★ | 「一字不落」和「全」意思重复。 | 有个学生，把练习册的答案一字不落背了下来。练习册上的题，他次次满分。 |  |
| l22 | zh | 记录 | native_zh | ★ | **自然。**“一字不落，全背了下来”虽有重复，但属于自然强调。“一字不落”的“落”应读 là。 | 保留原句。 |  |
| l22 | en | 记录 | native_en | ★ | 自然。“scores a hundred”在美式英语考试语境中成立，不必为了完整而补成书面表达。 | 保留。 |  |
| l23 | zh | 记录 | native_zh | ★ | **自然。**“可一到……就……”是常见口语句式，转折清楚。 | 保留原句。 |  |
| l23 | en | 记录 | native_en | ★ | 自然。“he's lost”简洁、口语化；插入的时间条件不会造成听觉歧义。 | 保留。 |  |
| l24 | 双语 | 建议 | editor | ★ | 重复（必查项 2）：l10、l17 已经建立了这组对应，s4 刚演示完。l24 再完整说一遍，删掉也不影响理解。 | 删除。如果需要一句桥接，zh：这就是刚才那条硬穿过每个点的曲线。 / en: That's the curve forced through every point. |  |
| l24 | 双语 | 建议 | teacher | ★ | 映射说得很明确（好），但没有映射噪声；配合 l22 补上。 | zh：对上实验：练习册是训练数据，印错的答案是噪声，考试是新数据；死记硬背，就是那条硬穿过每个点的曲线。<br>en: Map it back: the workbook is the training data, the misprints are noise, the exam is new data, and cramming is that curve forced through every point. |  |
| l24 | zh | 建议 | native_zh | ★ | **有点怪。**“对上刚才的实验”搭配生硬；“那条硬穿过每个点的曲线”定语较挤，“硬穿过”也不如“穿过”顺口。 | 对应刚才的实验：练习册就是训练数据，考试就是新数据，背下来的答案，就是那条穿过每个点的曲线。 |  |
| l24 | en | 建议 | native_en | ★ | 明显别扭。“Map it back”偏技术讲解口吻；末尾把“answers”直接等同于“curve”，语法虽可解析，听觉上却要回想才能理解。 | In our experiment, the training data is the workbook, and new data is the exam. Forcing a curve through every point is like memorizing the answers. |  |
| l25 | 双语 | 必改 | teacher | ★ | 认猫的例子讲的不是过拟合，是**虚假相关 / 捷径学习**：小朋友学到的"沙发 = 猫"是一条**很简单**的规则，病根是照片太单一（数据偏），不是"记得太多"。限制复杂度治不了它，换更多样的照片才行（l46）。这正是"狗的例子其实是欠拟合吧？"那类评论会抓的问题。例子本身好懂，而且正好铺垫 l43 和测验 Q5，所以建议**留下但改标签**（见 l27），不要再当成过拟合的同一件事。 | l25–l26 原文保留，改 l27 和 l43。 |  |
| l25 | zh | 记录 | native_zh | ★ | **自然。**先交代认猫，再交代照片条件，两句都容易念。 | 保留原句。 |  |
| l25 | en | 记录 | native_en | ★ | 自然。“Or say…”是自然的口头举例方式，人物与照片的关系清楚。 | 保留。 |  |
| l26 | zh | 记录 | native_zh | ★ | **自然。**两种判断形成对照，“反倒不认了”有日常说话的味道。冒号、分号处均可停顿。 | 保留原句。 |  |
| l26 | en | 记录 | native_en | ★ | 自然。两次“Show him…”构成好懂的平行句式。“cat”和“no”应以轻微引语语气读出。 | 保留。 |  |
| l27 | 双语 | 必改 | teacher | ★ | ①"两个例子是同一件事"和 l43"捷径学习是过拟合的**近亲**"前后矛盾。②"模型只是被允许记得太多"放在认猫例子后面，把病因说错了。③说出的"不像之处"是"模型不会偷懒"，但背完整本练习册并不算偷懒，这一条没打中要害。另外，两个例子只比了共同点，没比差异，算不上真正的"两个例子做比较"。 | zh：两个都把只在手头数据里成立的东西当了真：学生是记得太多，小朋友是见得太少。类比不像的地方：模型不是故意死记，只是被允许记太多。<br>en: Both took something true only of the data at hand as the rule. The student remembered too much; the child saw too little. Where the analogy breaks: a model doesn't choose to cram. It's just allowed to remember too much. |  |
| l27 | 双语 | 必改 | factcheck | ★ | 背训练样本与依赖沙发背景不能说成“同一件事”；捷径可以是一条很简单的规则，不是“被允许记得太多”。[原文区分](https://arxiv.org/html/2004.07780v4) | zh：两个例子都用了不可靠的线索，但机制不同。认猫的例子是走捷径，不一定是记得太多。<br>en：Both rely on unreliable clues, but the mechanisms differ. The cat example uses a shortcut; it needn't involve remembering too much. |  |
| l27 | 双语 | 建议 | editor | ★ | 一句里放了两个新意思：两个例子的共同点，以及类比的局限。拆开后各自更好记。 | zh：l27a「两个例子是同一个错：记住了只在手头数据里成立的东西。」l27b「但类比有不像的地方：模型不会偷懒，它只是被允许记得太多。」 / en: l27a "Both are the same mistake: learning something only true of the data at hand." l27b "But the analogy has a limit. A model isn't lazy. It's just allowed to remember too much." |  |
| l27 | zh | 建议 | native_zh | ★ | **有点怪。**“两个例子是同一件事”略省过头；“类比也有不像的地方”搭配绕口。 | 两个例子说的是一回事：记住了只在手头数据里成立的东西。不过，类比也不完全一样：模型不会偷懒，只是被允许记得太多。 |  |
| l27 | en | 记录 | native_en | ★ | 自然，略偏解释性。“Both”结合前文可理解为两个例子；“data at hand”稍正式但不构成理解障碍。 | 保留。 |  |
| l28 | 双语 | 建议 | editor | ★ | 「把它重复三百次」对外行没有必要，还容易误解成三百个模型或三百档复杂度。「两种误差」此时也还没有名字。存疑：如果画面标了「300 次平均」，可以只在画面上保留，不配音。 | zh：回到实验。让模型从简单一步步变复杂，看练习误差和考试误差怎么变。 / en: Back to the experiment. Make the model more and more complex, and watch practice error and exam error. |  |
| l28 | 双语 | 建议 | teacher | ★ | "重复三百次，让模型从简单变到复杂"有歧义，听起来像是有三百档复杂度（十个点最多只能到十个数字）。存疑：要和实验代码核对"三百"到底指什么，按实际改。 | zh：回到实验：换三百组随机的点，各做一遍，看模型由简到繁时，两种误差平均怎么变。<br>en: Back to the experiment. We rerun it on 300 fresh sets of random points and watch how both errors change, on average, as the model gets more complex. |  |
| l28 | 双语 | 建议 | factcheck | ★ | 旁白容易听成“连续三百次逐步加复杂度”；画面却说“三百次实验的中位数”，统计口径没有讲清。具体重复方式仍须复算确认。 | 若确为每种复杂度重复三百次：<br>zh：回到实验。每种复杂度重复三百次，看两种误差的中位数。<br>en：For each model complexity, we run 300 trials and compare the median training and test errors. |  |
| l28 | en | 建议 | native_en | ★ | 稍别扭。“watch both errors”可以理解，但听众已经听过两个类比，再回来时需要回忆“both”是哪两个。明确复述更利于纯听。 | Back to the experiment. Over 300 runs, we increase model complexity and track practice error and exam error. |  |
| l28 | 双语 | 建议 | bilingual | ★ | 两版都有歧义：「重复三百次，让模型从简单变到复杂」/ "repeat it 300 times, making the model more and more complex" 可以理解成三百步、每步加一点复杂度，也可以理解成每档复杂度各重复三百次再取平均。存疑：请对照实验脚本或图的数据说明，确认 300 指什么，再选用下面的改法。 | zh（若是每档取平均）：回到实验。模型从简单调到复杂，每档做三百次取平均，看两种误差。<br>en：Back to the experiment. For each level of complexity, we average 300 runs and watch both errors. |  |
| l28 | zh | 记录 | native_zh | ★ | **自然。**“它”紧接“实验”，回指明确；后三个动作可按逗号分拍。 | 保留原句。 |  |
| l29 | 双语 | 记录 | teacher | ★ | 讲稿一直用"练习误差 / 考试误差"，标准叫法"训练误差 / 测试误差"一次也没出现；learning.json O2 和测验 Q4 用的是"训练 / 测试集"。英文里数据叫 training/test data，误差却叫 practice/exam error，配对不一致。这一期是"高频词"系列，观众出去会碰到标准叫法。 | 讲稿不改；l29 画面标签第一次出现时并列"练习误差（训练误差）""考试误差（测试误差）"，英文 "practice (training) error" / "exam (test) error"。 |  |
| l29 | zh | 记录 | native_zh | ★ | **自然。**“一路往下走”适合口播，“越……越……”便于听懂。 | 保留原句。 |  |
| l29 | en | 记录 | native_en | ★ | 自然。“The more…, the better…”是顺畅的口语结构，两个分句长度平衡。 | 保留。 |  |
| l30 | 双语 | 必改 | factcheck | ★ | 测试误差上升不能证明模型完全没学到规律；“只有中间才真正学会”把程度差别说成有无之分。 | zh：这次实验里，考试误差先降后升，中间那段预测新点最好。<br>en：In this experiment, test error falls, then rises. The middle range predicts new points best. |  |
| l30 | en | 必改 | native_en | ★ | 明显别扭，主体错位。“the middle stretch has actually learned”字面变成“中间那一段学会了”，应明确是处于中间复杂度的模型。 | But exam error falls, then rises. Only models in the middle have learned the pattern. |  |
| l30 | 双语 | 建议 | editor | ★ | 相邻重复（必查项 2）：l30「中间那一段，才是真正学到了规律」和 l32「要找的，是中间刚刚好的那一段」说的是同一件事。l32 是 O5 的落点，应该保留 l32。 | l30 zh：考试误差却先降后升。 / en: But exam error falls, then rises. |  |
| l30 | zh | 建议 | native_zh | ★ | **有点怪。**“中间那一段，才是真正学到了规律”把图上的区段放在了学习者的位置，句法略悬空。 | 考试误差先降后升。中间那段，模型才真正学到了规律。 |  |
| l30 | en | 记录 | bilingual | ★ | "Only the middle stretch has actually learned the pattern" 说成一段曲线「学会了」，主语别扭；中文「中间那一段」口语里可以接受。 | en：But exam error falls, then rises. Only models in the middle actually learned the pattern. |  |
| l31 | zh | 记录 | native_zh | ★ | **自然。**“很低／很高”对照明确，两个误差名称重复有助于听辨。 | 保留原句。 |  |
| l31 | en | 记录 | native_en | ★ | 自然。“telltale sign”是常见英语表达，不属于需要另行解释的技术词；句子可以连贯读完。 | 保留。 |  |
| l32 | 双语 | 建议 | bilingual | ★ | O2 要求观众会判断「两种误差都高是欠拟合」。两版都只讲了欠拟合在练习题上不行（l13），模型一的考试误差在 s4 没提（l18–l19 只讲了模型二和模型三），l32 也只说「左边的欠拟合」，全靠画面。缺了画面，两版都达不成 O2 的后半句。 | zh：模型越简单越好？不。太简单，两种误差都高，是左边的欠拟合。要找中间刚刚好的那段。<br>en：So is simpler always better? No. Too simple, and both errors stay high: underfitting, on the left. You want the sweet spot in the middle. |  |
| l32 | zh | 记录 | native_zh | ★ | **自然，画面指代存疑。**自问自答顺畅；“左边”“中间”需要同步图形才能落地。 | 保留原句；核实画面方向与口播一致，两个区段能被辨认。 |  |
| l32 | en | 记录 | native_en | ★ | 自然。“sweet spot”口语化。存疑：“on the left”“in the middle”依赖图示位置，需结合画面核实。 | 文字保留；核对左右位置及指示时机。 |  |
| l33 | 双语 | 建议 | teacher | ★ | "学习，其实是一种压缩"把一个视角（最小描述长度的思路）说成了事实，说过头了。 | zh：换个角度想：学习，可以看成一种压缩。<br>en: Here's another way to see it. Learning can be seen as a kind of compression. |  |
| l33 | zh | 记录 | native_zh | ★ | **自然。**冒号处停顿后再说“学习”，转入新角度的节奏清楚。 | 保留原句。 |  |
| l33 | en | 记录 | native_en | ★ | 自然。“compression”对部分观众是新概念，但后续紧接数字例子，语言上有承接。 | 保留。 |  |
| l34 | 双语 | 建议 | factcheck | ★ | 十个高度只能在横坐标已知时确定这十个点；压缩类比漏掉了共享条件。 | zh：横坐标已知，只需记十个高度。<br>en：With the horizontal positions known, we need only store ten heights. |  |
| l34 | zh | 记录 | native_zh | ★ | **自然。**“这十个点”在话题上能承接实验；若镜头已切走，需核实此时是否重新呈现。 | 保留原句；核实对应点图仍可见。 |  |
| l34 | en | 记录 | native_en | ★ | 句法自然。存疑：“ten heights”需要观众看得出“高度”指图上的什么；只听这一句无法完全确定。 | 文字暂保留；核对画面是否清楚指示点的纵向位置。 |  |
| l35 | 双语 | 建议 | teacher | ★ | "四个数字"出现得很突然：前面从没说过曲线是由几个可调的数字定下来的（直线用两个也没提）。观众不知道数的是什么。 | zh：第二种曲线由四个可调的数字定下，就把它们大致说清了，还能说中没见过的点。<br>en: Model two is set by just four adjustable numbers. That describes them roughly, and still comes close on points it has never seen. |  |
| l35 | zh | 建议 | native_zh | ★ | **有点怪。**“把点说清”“说中没见过的点”搭配别扭，尤其“说中”通常搭配答案、心事或结果。 | 第二种曲线，只用四个数字，就能大致描述这些点，还能预测没见过的点。 |  |
| l35 | en | 建议 | native_en | ★ | 稍别扭。“comes close on points”不是很自然的搭配，也省略了“什么接近什么”。直接说预测得好更易听懂。 | Model two roughly describes them with just four numbers. It also predicts new points fairly well. |  |
| l35 | zh | 建议 | bilingual | ★ | 轻重不一。中文「还能说中没见过的点」意思是预测得准，说过头了；英文 "comes close" 只是说离得不远，跟 l18「离新点都不远」一致。 | zh：第二种曲线，只用四个数字，就把它们大致说清了，新点也估得不远。 |  |
| l35 | 双语 | 记录 | editor | ★ | 存疑：「四个数字」没有交代是什么数字（决定曲线形状的参数）。如果画面不显示这四个数，观众接 l36 的「十个数字」会接不上。请核对画面。 | zh：第二种曲线只靠四个数字定形，就大致说清了它们，还能说中新点。 / en: Just four numbers set model two's shape, yet it roughly fits them and comes close on new points. |  |
| l36 | 双语 | 必改 | factcheck | ★ | 十个系数足以插值，不意味着“不用找规律，所以没找”。参数数量不能证明模型完全没有学到规律。 | zh：第三种有十个数字，能穿过全部十个点，但也跟着噪声拐弯，预测新点就差了。<br>en：Model three uses ten numbers to pass through all ten points, but it follows the noise too, hurting predictions on new points. |  |
| l36 | 双语 | 建议 | teacher | ★ | "它不用找规律，所以也就没找"把模型说成会偷懒，和 l27 说的"模型不是故意的"打架。（"十个数字配十个点"这一层本身讲得很准，要保留。） | zh：第三种模型有十个数字，正好够把十个点原样存下。没有什么逼它去找规律，它也就没找。<br>en: Model three has ten numbers, exactly enough to store all ten points as they are. Nothing forced it to find the pattern, so it didn't. |  |
| l36 | 双语 | 记录 | teacher | ★ | 现在"正好够"的措辞是准确的。但画面、简介和以后几期都别引申成"参数比数据多就一定过拟合"：现代大模型的参数远多于数据，照样能泛化（双降现象，对标里有 Welch Labs 那一期）。 | 不改；画面上别写"参数越多 → 越过拟合"这类箭头。 |  |
| l36 | zh | 记录 | native_zh | ★ | **自然。**两句都短，“它”明确指模型；就中文句法和口语节奏而言没有障碍。 | 保留原句。 |  |
| l36 | en | 记录 | native_en | ★ | 自然。数字与指代清楚；“so it didn't”作为收尾有自然的口语节奏。 | 保留。 |  |
| l37 | 双语 | 建议 | teacher | ★ | ①"用更少的东西，解释更多的事"是全片最容易引申过度的一句，而且和 l32"不是越简单越好"有冲突（观众可能只记住"越少越好"）。②压缩视角里最关键的一点没说：有损压缩**丢掉的那部分，正好是噪声**。说出这一点，s7 才能和 l20 接上。 | zh：好的压缩，丢掉的恰好是噪声；留下来的，才是规律。<br>en: Good compression throws away exactly the noise. What's left is the pattern. |  |
| l37 | zh | 记录 | native_zh | ★ | **自然。**“更少／更多”对称，适合放慢语速作为段落落点。 | 保留原句。 |  |
| l37 | en | 记录 | native_en | ★ | 自然。简短有力，“more with less”搭配地道。这里仅评价表达，不审查论断范围。 | 保留。 |  |
| l38 | en | 建议 | native_en | ★ | 稍别扭。上一句刚说“Real understanding”，“This”和“It”连续使用，会让“造成麻烦的究竟是什么”短暂失焦。 | Overfitting causes trouble in the real world, too. |  |
| l38 | 双语 | 记录 | editor | ★ | 空洞过渡，章节卡已经交代了本章主题。 | 删除。如果保留，zh：这毛病在现实里闯过祸。 |  |
| l38 | zh | 记录 | native_zh | ★ | **自然。**短句承上启下，“闯过祸”延续了开头的口语表达。 | 保留原句。 |  |
| l39 | 双语 | 必改 | factcheck | ★ | 画面“5000 万……1152……＝过拟合”把数量悬殊写成充分判据；原文依据还包括选中了无关的季节性关联。另须限定为**最初版本**，指标是流感样疾病就诊比例。[Lazer 原文](https://cdanfort.w3.uvm.edu/csc-reading-group/lazer-flu-science-2014.pdf) | zh：谷歌曾用搜索词估算流感样症状的就诊比例。初版从五千万个词里挑选，去贴合一千多个历史数据点。研究者认为它过拟合了：既在测流感，也在测冬天。<br>en：Google used searches to estimate the share of visits for flu-like illness. Its initial version selected from 50 million terms to fit about 1,100 data points. Researchers criticized its overfitting: it tracked both flu and winter.<br>画面将“＝过拟合”替换为“（初版）”。 |  |
| l39 | 双语 | 建议 | editor | ★ | 约 75 字一句，塞了谷歌、五千万词、一千多个点、过拟合、冬天五个信息点，配音一口气读不完。英文「about 1,100」和中文「一千多」不一致（原研究是 1,152 个点）。 | zh 拆三句：「谷歌曾用人们的搜索记录估算流感。」「研究者指出，它从五千万个搜索词里挑出最贴合一千多个历史数据点的那些，这正是过拟合。」「它既在测流感，也在测冬天。」 / en: "Google once estimated flu levels from people's searches." "Researchers found it sifted 50 million search terms for the best fit to just over 1,100 data points. That's overfitting." "It was part flu detector, part winter detector." |  |
| l39 | 双语 | 建议 | teacher | ★ | 没有对应回实验："五千万个词去凑一千多个点"正是 l36 的"自由度比数据多"，这是全片最好的一次迁移机会，却没点明。只说"测冬天"，观众容易理解成别的事（季节混淆）。 | zh：谷歌曾用搜索记录估算流感：从五千万个词里，挑最贴合一千多个历史点的那些。可挑的远比点多，就像十个数字配十个点；结果它一半在测流感，一半在测冬天。<br>en: Google once estimated flu from searches, picking from 50 million terms the best fit to about 1,100 data points. Far more choices than points, like ten numbers for ten points. It became part flu detector, part winter detector. |  |
| l39 | zh | 建议 | native_zh | ★ | **很怪。**第二句塞入来源、筛选过程、两个数量和结论；“最能贴合一千多个历史数据点的那些”长定语让听众等很久才知道“那些”是什么。 | 谷歌曾用搜索记录估算流感。研究者指出，它从五千万个搜索词里，挑出最贴合一千多个历史数据点的词。这正是过拟合：它既在测流感，也在测冬天。 |  |
| l39 | en | 建议 | native_en | ★ | 稍别扭。“it searched 50 million terms”在搜索引擎语境里容易听成“执行了五千万次搜索”；“best fit”又增加一层未解释的技术措辞。 | Google once used people's searches to track flu. Researchers noted it tested 50 million search terms against about 1,100 data points. That's overfitting. It was part flu detector, part winter detector. |  |
| l39 | en | 记录 | bilingual | ★ | 数字的说法略有出入：中文「一千多个历史数据点」，英文 "about 1,100 data points"。存疑：Lazer et al. 2014（Science, "The Parable of Google Flu"）原文是 1,152 个，按这个数，"about 1,100" 偏低；英文也少了「历史」这个限定。 | en：…it searched 50 million terms for the best fit to over 1,100 past data points. |  |
| l40 | 双语 | 建议 | factcheck | ★ | 100/108 核实无误，但它没有直接证明新旧版本“没好多少”，也不能单独归因于过拟合。 | 仅替换开头：<br>zh：后来的版本仍有偏差：<br>en：Later versions still had problems. |  |
| l40 | zh | 建议 | native_zh | ★ | **有点怪。**“估高了”略像数据讨论中的简写；年份和两个数量连续出现，需要明确停顿。 | 后来也没好多少：2011到2013年，108周里，有100周估得偏高。 |  |
| l40 | en | 记录 | native_en | ★ | 自然。两个年份加一个比例增加口播负担，但无绕口或歧义；在年份之后稍停即可。 | 保留。 |  |
| l41 | 双语 | 必改 | factcheck | ★ | 99.95% 和 99.98% 分别对应 NIH、Mount Sinai；同一医院识别实验的 IU 为 **95.59%**。目前“几乎百分之百认出来自哪家医院”及无范围的“99.9%”扩大了适用范围。[Zech 结果](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1002683) | 将医院识别部分替换为：<br>zh：胸片带着医院“指纹”：另训模型识别 NIH 和西奈山的片子，准确率超99.9%。<br>en：X-rays carried hospital fingerprints: a separate model identified NIH and Mount Sinai scans with over 99.9% accuracy.<br>画面数字可改为“≈100%”，并与上述医院范围同屏。 |  |
| l41 | 双语 | 建议 | editor | ★ | 约 95 字，是全片最长的一句。先出现「另训一个模型」，后出现「看肺炎的模型」，两个模型很容易听混。结果（换医院掉分）放在最后，叙述顺序是倒的。 | zh 拆三句：「医学影像里也有。一个看胸片判断肺炎的模型，换到新医院，成绩就掉了。」「研究者发现，胸片里藏着医院的“指纹”：另一个模型几乎能百分之百认出片子来自哪家医院。」「它的好成绩，很可能一部分靠认医院，不是认病。」 / en: "Medical imaging has examples too. A pneumonia model that read chest X-rays did worse at a new hospital." "Researchers found the X-rays carry a hospital fingerprint: another model could tell, almost perfectly, which hospital each came from." "So part of its success likely came from recognizing hospitals, not disease." |  |
| l41 | zh | 建议 | native_zh | ★ | **很怪。**“另训”像书面缩写；“看肺炎的模型”“好成绩很可能有一部分就靠认医院”不够顺。两个模型连续出现，叠加冒号、分号，容易听混。 | 医学影像里也有。研究者发现，胸片藏着医院的“指纹”。单独训练一个模型，几乎百分之百能认出片子来自哪家医院。诊断肺炎的模型，成绩好可能有一部分就靠认医院，而不是认病。换家新医院，成绩就掉了下来。 |  |
| l41 | en | 建议 | native_en | ★ | 稍别扭，信息较密。“a separate model”再切换到“the pneumonia model”，首次听容易混淆两个模型。“pneumonia”也未解释；不是人人都熟悉。 | Medical imaging has examples too. Chest X-rays carried clues to their hospital of origin: a separate model identified the hospital almost perfectly. A model detecting pneumonia, a lung infection, likely benefited from those clues too. At a new hospital, its performance dropped. |  |
| l41 | en | 记录 | bilingual | ★ | 出处表述不一致：中文是「研究者发现，胸片里藏着医院的指纹」，英文 "Chest X-rays turned out to carry…" 没有说是谁发现的。 | en：Medical imaging has examples too. Researchers found chest X-rays carry a hospital fingerprint: … |  |
| l42 | zh | 必改 | bilingual | ★ | 限定语两版不一致。英文有 "With the marks"，说的是带标记的良性痣有一半多被误判；中文「让它把一半多的良性痣，都误判成了癌」读起来像所有良性痣里一半多都被误判，夸大了范围。存疑：「一半多」这个数字请对照 Winkler et al. 2019（JAMA Dermatology，皮肤标记对 CNN 黑色素瘤识别的影响）里带标记时的特异度或假阳性率核实。 | zh：还有一个识别黑色素瘤的系统：带医生标记笔迹的良性痣，一半多被它误判成了癌。 |  |
| l42 | zh | 建议 | teacher | ★ | 中文没有英文 "With the marks" 那层限定，读起来像是**所有**良性痣里一半多都被判成癌，会造成新的误解。 | zh：还有一个识别黑色素瘤的系统，被医生在皮肤上画的标记骗了：画了标记的良性痣，一半多被它判成了癌。 |  |
| l42 | 双语 | 建议 | factcheck | ★ | 换算正确，但建议点明是一次研究的结果，避免听成该系统在所有场景中的固定误判率。 | zh：还有个黑色素瘤识别系统：加上皮肤标记后，研究中一半多的良性痣被它误判为癌。<br>en：In one study, adding skin markings made a melanoma detector label over half the benign moles as cancer. |  |
| l42 | zh | 建议 | native_zh | ★ | **有点怪。**“医生在皮肤上画的标记笔迹”定语长，“标记笔迹”语义重叠；病名后立刻接复杂解释，口播负担偏重。 | 还有个识别黑色素瘤的系统。医生画在皮肤上的标记，让它把一半多的良性痣误判成了癌。 |  |
| l42 | en | 建议 | native_en | ★ | 稍别扭。“melanoma”可能超出一般观众词汇；“called … moles cancer”可以听懂，但“labeled … as cancer”更顺。 | A model for spotting melanoma, a skin cancer, was fooled by doctors' ink marks. With marks, it labeled over half the harmless moles as cancer. |  |
| l42 | zh | 记录 | editor | ★ | 「画的标记笔迹」读起来拗口。 | 还有一个识别黑色素瘤的系统：医生在皮肤上画的记号，让它把一半多的良性痣误判成了癌。 |  |
| l43 | 双语 | 必改 | factcheck | ★ | “学到的却是巧合，不是规律”排除了同时利用有效特征的可能；也漏掉捷径学习可以通过同分布新数据测试这一关键区别。皮肤论文对训练中如何形成这种依赖仍保留不确定性。[捷径定义](https://arxiv.org/html/2004.07780v4)、[皮肤论文讨论](https://jamanetwork.com/journals/jamadermatology/fullarticle/2740808) | zh：这还涉及捷径学习：模型可能依赖医院或笔迹等线索。它不同于过拟合，同类新题也能考好，换个环境才露馅。<br>en：These cases point to shortcut learning: relying on cues such as hospitals or ink marks. Unlike ordinary overfitting, shortcuts can pass tests on similar new data and fail when conditions change. |  |
| l43 | 双语 | 建议 | editor | ★ | 概念边界不清：s5 把「沙发上的猫」当作过拟合的例子（「两个例子是同一件事」），s8 又说这类例子叫捷径学习，是过拟合的「近亲」。观众会问：沙发猫到底算哪个？Q5 恰好考这一点。l43 后半句和 l27 也有些重复。 | zh：后两个例子，和沙发上的猫一样，叫捷径学习，是过拟合的近亲：手头数据上亮眼，学到的却是巧合。 / en: Those two, like the cat on the sofa, are shortcut learning, a close cousin of overfitting: brilliant on the data at hand, yet built on coincidence. |  |
| l43 | 双语 | 建议 | teacher | ★ | 和 s5 的认猫例子接上（配合 l27 的改法），让"近亲"这层关系前后一致。 | zh：后两个例子，和认猫的小朋友一样，叫捷径学习，是过拟合的近亲：在手里的数据上亮眼，学到的却是巧合。<br>en: Those last two, like the child and the cats, are shortcut learning, a close cousin of overfitting: brilliant on the data at hand, but what they learned was coincidence. |  |
| l43 | en | 建议 | native_en | ★ | 明显别扭。先把“Those last two”称为一种学习现象，下一句“They look brilliant”又把它们当模型，指代对象发生切换。“what they learned was coincidence”也偏抽象。 | Those last two models show shortcut learning, a close cousin of overfitting. They looked brilliant on their training data, but learned coincidences instead of reliable patterns. |  |
| l43 | zh | 记录 | native_zh | ★ | **自然。**“后两个例子”回指明确，“近亲”容易听懂。术语“捷径学习”应完整连读。 | 保留原句。 |  |
| l43 | en | 记录 | bilingual | ★ | "Those last two are called shortcut learning" 字面意思是「这两个例子名叫捷径学习」，搭配有点别扭；意思与中文一致。 | en：Those last two are shortcut learning, a close cousin of overfitting. … |  |
| l44 | zh | 记录 | native_zh | ★ | **自然。**问句后接数量明确的回答，听众容易跟上。 | 保留原句。 |  |
| l44 | en | 记录 | native_en | ★ | 自然。“Three common ways”紧接完整问题，并由下文编号兑现，是正常口语省略，不需要一律扩成长句。 | 保留。 |  |
| l45 | en | 必改 | bilingual | ★ | 英文版前面一直用 practice problems = 训练数据、practice error = 训练误差（l09、l13、l29、l31），这里又把验证集叫 "practice exam"。英文观众很容易把验证集当成训练数据的一部分，可 Q4 考的正是这个区分。中文用「练习题 / 模拟考」，两个词分得开，没有这个问题。 | en：…set aside another slice of data as a mock exam, called a validation set. … |  |
| l45 | 双语 | 建议 | editor | ★ | 约 68 字，塞了五件事：演示时拿考试挑模型的坦白、模拟考、验证集、两种用途、考试留到最后。坦白插在「三个办法」和「第一」之间，打断了列表。 | 先讲办法，再讲坦白，拆两句。zh：l45a「第一，再留一份数据当模拟考，叫验证集，用它挑模型、及早发现过拟合。」l45b「刚才演示时，我们直接拿考试挑了模型；实际上，考试要留到最后才用。」 / en: l45a "One: set aside another slice of data as a mock exam, called a validation set. Use it to choose your model and catch overfitting early." l45b "In the demo, we picked the model with the real exam. In practice, save that for the very end." |  |
| l45 | en | 建议 | editor | ★ | 「practice exam」和全片的「practice problems」（指训练数据）都用 practice，英语观众容易把验证集当成训练数据。 | 改用 mock exam（已写进上一行的改法）。 |  |
| l45 | zh | 建议 | native_zh | ★ | **有点怪。**“拿考试挑了模型”省略了“成绩”，搭配生硬；“实际该这样做。第一”被句号割断，随后又接冒号，口播层次偏碎。 | 刚才为了演示，我们按考试成绩挑模型。实际该这样做：第一，再留一份数据当模拟考，叫验证集。用它挑模型、及早发现过拟合，真正的考试留到最后。 |  |
| l45 | en | 记录 | native_en | ★ | 自然。整条较长，但由多句组成，不需要一口气读完；“validation set”有紧邻的通俗解释。可在“practice exam”后自然停顿。 | 保留。 |  |
| l46 | zh | 记录 | native_zh | ★ | **自然。**“更多、更多样”有意形成递进，没有明显绕口；两个短语之间轻停即可。 | 保留原句。 |  |
| l46 | en | 记录 | native_en | ★ | 自然。“more data, and more varied data”的重复有作用；“pass for patterns”地道，音节衔接也不绕口。 | 保留。 |  |
| l47 | 双语 | 必改 | factcheck | ★ | 正则化不等于让模型“没有能力记住每个点”，也不保证无法插值；它可以通过软约束改变模型偏好。[正则化定义](https://www.deeplearningbook.org/contents/regularization.html) | zh：第三，用正则化约束学习，比如惩罚过度复杂的拟合，减少追着噪声跑。<br>en：Three: use regularization, such as penalizing overly complex fits, to discourage fitting noise. |  |
| l47 | 双语 | 建议 | teacher | ★ | "正则化"这个名字对普通观众是不透明的（中文"正则"容易联想到正则表达式），属于"名字误导人时要点破"的情况；对标里还提到过专家嫌"正则化说得太粗"。s9 一段引入两个术语（验证集、正则化），因为是列清单，可以接受。 | zh：第三，给模型的复杂度立规矩，别让它有本事把每个点都背下来。这叫正则化，"正则"就是立规矩。<br>en: Three: put limits on the model's complexity so it can't memorize every point. That's regularization: keeping the model in line. |  |
| l47 | en | 建议 | native_en | ★ | 稍别扭。“These methods”在三项清单末尾，听觉上容易回指全部三项。让指代紧贴第三项更清楚。 | Three: limit the model's complexity so it can't memorize every point. That's called regularization. |  |
| l47 | zh | 记录 | native_zh | ★ | **自然。**“别让它有本事……”有口语感，术语解释另起一句，节奏合理。“正则化”首次听辨效果需试读核实。 | 保留原句；术语完整连读，并核实首次出现时有字幕。 |  |
| l48 | zh | 记录 | native_zh | ★ | **自然。**是引出下句的提示语，应继续接 l49。 | 保留原句。 |  |
| l48 | en | 记录 | native_en | ★ | 自然。是明确的收尾引导，不存在 v1 “Four things.”那种孤立碎片感。 | 保留。 |  |
| l49 | 双语 | 必改 | factcheck | ★ | 片尾再次把“记忆”和“学到规律”写成互斥，强化了 l09 的错误定义。 | 两句合计替换：<br>zh：过拟合，就是太贴合练习题，／反而做不好同类新题。<br>en：Overfitting means fitting practice data too closely／to do well on similar new data. |  |
| l49 | zh | 记录 | native_zh | ★ | **自然。**这是跨编号长句的前半句，结尾应轻停，不能读成已经收句。 | 保留原句，与 l50 连贯读出。 |  |
| l49 | en | 记录 | native_en | ★ | 与 l50 连读时自然；本行是未完句，不能读成句号收束。 | 保留，与 l50 连读。 |  |
| l50 | zh | 记录 | native_zh | ★ | **自然。**承接 l49，不是主语缺失；重音可落在“没学会规律”。 | 保留原句。 |  |
| l50 | en | 记录 | native_en | ★ | 与 l49 构成完整、顺口的定义。“without”正好承接核心对比。 | 保留，不另起宣告语气。 |  |
| l51 | zh | 记录 | native_zh | ★ | **自然。**预告简短，术语边界清楚。 | 保留原句。 |  |
| l51 | en | 记录 | native_en | ★ | 自然。预告中直接报下期术语成立；无需在此提前解释“reinforcement learning”。 | 保留。 |  |
| 全片 | 双语 | 必改 | factcheck | ★ | **台账句号错位。** C04–C08 仍指向 l35–l39，实际案例已在 l39–l43；C01–C03 也存在错位，不能据此追溯当前讲稿。 | `lines` 建议替换为：C01＝`["l15","l19"]`；C02＝`["l28","l29","l30"]`；C03＝`["l10","l34","l35","l36"]`；C04–C08 分别＝`["l39"]`、`["l40"]`、`["l41"]`、`["l42"]`、`["l43"]`。 |  |
| 全片 | 双语 | 必改 | factcheck | ★ | **事实登记不全。** 未独立登记的包括：过拟合定义、训练数据与噪声、误差及欠拟合、六个测试点与测试集、过拟合信号、压缩观点，以及验证集／增加数据／正则化。现有 C01–C03 不能覆盖这些概念。 | 台账至少补录对应 l09–l13、l17、l21、l27、l31、l33、l37、l45–l47、l49–l50 的事实及依据；“学习是压缩”应标为解释视角。旁白可分别缩为：zh“换个角度：把学习想成压缩。”；en“One useful lens is learning as compression.” |  |
| 全片 | 双语 | 记录 | teacher | ★ | explain_back 列出的误解"过拟合就是训练不够"讲稿没有点名驳斥。l15"误差是零"和改后的 l21"练习误差为零"已经从侧面驳了，暂时够用。 | 不另加句子；后测观察这一项误解的出现率。 |  |
| 全片 | 双语 | 记录 | factcheck | ★ | **存疑：C01–C03 的实验结果未能独立复算。** 给出的断言只能检查近零训练误差、倍率落在20至30之间、系数数量；不能单独证明画面的1.80、25倍，以及三百次中位数曲线的形状。 | 暂不改数字，也不标为已核实。核实方式：用当前实验代码输出各模型 MSE、未取整倍率、训练／测试点数及各复杂度的三百次中位数，并逐项比对画面。代码不在本次授权材料内，未读取或运行。 |  |

## 处理结论（作者，2026-11-08；改动落在 v3.1 讲稿，句号已重排）

**采纳**
- 定义（factcheck l09/l49）：l09 改为精确定义「把练习题贴得太紧，连偶然的细节都学了进去，做新题反而变差」，「背答案却没学会规律」降为比方（l10）与片尾记忆句；片尾保留比方作为可引用的一句话。
- 误差（teacher/factcheck/editor l13）：先画直线再命名误差，拆成 l14/l15，删去「越小越好」，避免种下「训练误差越低越好」。未在口播里讲「平方平均」（对外行过细），画面说明误差为点到线的距离。
- 欠拟合 = 两种误差都高（teacher/bilingual l21/l32）：l23、l35 补上；O5「练习误差为零≠好模型」在 l23 点名。
- 噪声为什么害人（teacher l20）：l22 补「噪声是随机的，到了新题不会重演」。
- 学生类比映射噪声（teacher l22/l24）：l24「连印错的几处也照背」，l26 显式映射「印错的答案是噪声」。
- 类比失效处（teacher l27）：改为「学生知道自己在背，模型不知道」。
- **认猫例子概念错误（teacher l25/l27，factcheck l27）**：改为「相近、但不一样的毛病」，l30 对比「学生记得太多，小朋友见得太少」，并接到 l50 捷径学习。
- l17 歧义「六个模型」（editor/native_zh）：改为「再拿六个新点，模型都没见过」。
- l18 回答猜题（editor）：「考得最好」。
- 三百次（teacher/factcheck/bilingual/editor l28）：改为「换三百组随机的点，每组都从简单做到复杂，看平均」。
- 「只有中间才学到规律」过满（factcheck/native_en l30）：改为「复杂度在中间的模型，预测新数据最准」。
- 压缩视角（teacher l33/l36/l37，factcheck l36）：「可以看成一种压缩」；l39 改为「连噪声也一起存了下来，新点反而估不准」；l40 改为「好的压缩，丢掉的恰好是噪声；留下来的，才是规律」（不再说「用更少解释更多」，与「不是越简单越好」不冲突）。
- 流感（factcheck/editor/teacher l39）：限定「最初」版本，拆句，并连回实验「可挑的远比数据多，就像十个数字配十个点」；画面去掉「= 过拟合」的等号判据。l40「后来的版本也有偏差」。
- 胸片（factcheck/editor/native l41）：拆成 l46–l48，限定「其中两家医院、超过 99.9%」，先讲肺炎模型再讲另训模型。
- 黑色素瘤（bilingual/teacher/factcheck l42）：限定「研究中，画了标记的良性痣」。
- 捷径学习与过拟合的区别（factcheck/teacher/editor l43）：l50 补「它们在同类数据上也能考好，换个环境才露馅」。
- 验证集坦白位置（editor l45）：先讲办法（l52）再坦白（l53）；英文 practice exam → mock exam（bilingual/editor）。
- 正则化（factcheck/teacher l47）：改为「对过于复杂的曲线加惩罚」，不再说「没有能力记住每个点」。
- 结尾启发（teacher s10）：l59 加「下回你觉得全懂了，换一道没见过的题试试」。
- 冷开场措辞（factcheck l02）：「很多时候，不是程序写错了」。
- 事实台账（factcheck 全片）：按 v3.1 句号重排，补概念条目 C09–C13（引文待第 2 轮核对原文）。
- 母语听感：中英文「有点怪 / 很怪」的句子按建议改写（l05、l08、l09、l11、l19、l24、l35、l38、l41、l42、l45、l47 等）。

**不采纳**
- 删除本期内容段（editor s1）：用户明确要求开场介绍本期内容与先修；改为缩短（6 句短句）。
- 片尾一句话改成精确定义（factcheck l49）：精确定义已在 l09；片尾保留可引用的比方。
- 误差说成「高度差平方的平均」（factcheck l13）：对目标观众过细，画面与「点到线的距离」已足够；台账 C01 记明是均方误差。
