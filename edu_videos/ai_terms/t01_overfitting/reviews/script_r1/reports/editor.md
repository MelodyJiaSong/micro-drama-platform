# 审稿报告：讲稿编辑（精炼）· ai_terms / t01_overfitting · script 第 1 轮

材料：`reviews/script_r1/materials/lines.md`、`learning.json`。没有看画面，涉及画面的判断标了「存疑」。
时长估算：中文按约 4 字/秒，英文按约 2.5 词/秒，未计包装卡停顿。

## 必查项 1：逐句判定

- **必需**：l01、l02、l09、l10、l11、l12、l13、l14、l15、l17、l18、l19、l20、l21、l25、l26、l27、l30、l31、l32、l35、l36、l41、l42、l43、l45、l46、l47、l49、l50
- **有帮助**：l16（先猜再揭晓）、l22、l23、l28、l29、l33、l34、l37、l39、l40、l44、l48、l51、l08（对外行有安抚作用，但属于元话语）
- **可删**：
  - l03–l07：目录。后面每一章都有章节卡，删掉不缺信息，而且能让定义提前约 18 秒出现。
  - l24：「练习册＝训练数据、考试＝新数据」这组对应 l10、l17 已经讲过，s4 刚演示完，再说一遍是重复。
  - l38：空洞过渡。章节卡「现实里的代价」已经交代了，l39 可以直接开讲谷歌。

## 问题表

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l17 | zh | 必改 | 「拿出六个模型从没见过的新点」听起来像「六个模型」。纯听配音时一定会误解，以为出现了六个模型。 | 再拿六个新点，模型都没见过。这叫测试数据，相当于考试。 |
| s1（l03–l07） | 双语 | 建议 | 目录开场，和 v2 是同类问题。冷开场之后接 5 句目录（约 18 秒），把定义推到约 30 秒才出现。目录既不是反差也不是问题，而且和实际章节对不上（漏了 s6「一张图」）。 | 删 l03–l07，冷开场直接接 l08 / l09。如果包装卡必须保留，只留 l08 一句。 |
| l08 | 双语 | 记录 | 有帮助，但「片中都会一句话讲清」是元话语，删 s1 后可以再短一点。 | zh：不懂模型也没关系，片中都会讲清。 / en: No background needed. We'll explain as we go. |
| l09 | 双语 | 记录 | 「先给一句话」「下面用一个小实验看清楚」都是过渡性的废话，把定义夹在中间。 | zh：一句话：过拟合，就是把练习题背下来了，却没学会规律。来看个小实验。 / en: In one sentence: overfitting is memorizing the practice problems without learning the pattern. Here's a small experiment. |
| l13 | 双语 | 建议 | 一句塞了两个新概念（误差的定义和欠拟合），观众还要同时看第一条直线。误差定义埋在「第一种」前面，不容易被注意到。 | 拆成两句。zh：l13a「先说误差：点离曲线有多远，越小越好。」l13b「第一种模型太简单，只会画直线，连练习题都对不上。这叫欠拟合。」 / en: l13a "First, error: how far the points are from the curve. Smaller is better." l13b "Model one is too simple. It only draws a straight line and misses even the practice problems. That's underfitting." |
| l16 | zh | 记录 | 第三次用「先」开头（l09「先给」、l13「先说」）。 | 猜一猜：换成新题，哪一种考得最好？ |
| l18 | 双语 | 建议 | l16 问的是「哪一种考得最好」，l18 只说「考得不错」，没有给出明确答案，问答没有接上。 | zh：第二种曲线，离新点都不远，考得最好。 / en: Model two stays close to the new points. It does best. |
| l19 | zh | 记录 | 约 45 字，字幕要分两屏。「一下就差出去很远」偏口语，意思也模糊。 | 第三种曲线在点之间乱拐，有的新点离它很远。它的考试误差，是第二种的二十多倍。 |
| l22 | zh | 记录 | 「一字不落」和「全」意思重复。 | 有个学生，把练习册的答案一字不落背了下来。练习册上的题，他次次满分。 |
| l24 | 双语 | 建议 | 重复（必查项 2）：l10、l17 已经建立了这组对应，s4 刚演示完。l24 再完整说一遍，删掉也不影响理解。 | 删除。如果需要一句桥接，zh：这就是刚才那条硬穿过每个点的曲线。 / en: That's the curve forced through every point. |
| l27 | 双语 | 建议 | 一句里放了两个新意思：两个例子的共同点，以及类比的局限。拆开后各自更好记。 | zh：l27a「两个例子是同一个错：记住了只在手头数据里成立的东西。」l27b「但类比有不像的地方：模型不会偷懒，它只是被允许记得太多。」 / en: l27a "Both are the same mistake: learning something only true of the data at hand." l27b "But the analogy has a limit. A model isn't lazy. It's just allowed to remember too much." |
| l28 | 双语 | 建议 | 「把它重复三百次」对外行没有必要，还容易误解成三百个模型或三百档复杂度。「两种误差」此时也还没有名字。存疑：如果画面标了「300 次平均」，可以只在画面上保留，不配音。 | zh：回到实验。让模型从简单一步步变复杂，看练习误差和考试误差怎么变。 / en: Back to the experiment. Make the model more and more complex, and watch practice error and exam error. |
| l30 / l32 | 双语 | 建议 | 相邻重复（必查项 2）：l30「中间那一段，才是真正学到了规律」和 l32「要找的，是中间刚刚好的那一段」说的是同一件事。l32 是 O5 的落点，应该保留 l32。 | l30 zh：考试误差却先降后升。 / en: But exam error falls, then rises. |
| l35 | 双语 | 记录 | 存疑：「四个数字」没有交代是什么数字（决定曲线形状的参数）。如果画面不显示这四个数，观众接 l36 的「十个数字」会接不上。请核对画面。 | zh：第二种曲线只靠四个数字定形，就大致说清了它们，还能说中新点。 / en: Just four numbers set model two's shape, yet it roughly fits them and comes close on new points. |
| l38 | 双语 | 记录 | 空洞过渡，章节卡已经交代了本章主题。 | 删除。如果保留，zh：这毛病在现实里闯过祸。 |
| l39 | 双语 | 建议 | 约 75 字一句，塞了谷歌、五千万词、一千多个点、过拟合、冬天五个信息点，配音一口气读不完。英文「about 1,100」和中文「一千多」不一致（原研究是 1,152 个点）。 | zh 拆三句：「谷歌曾用人们的搜索记录估算流感。」「研究者指出，它从五千万个搜索词里挑出最贴合一千多个历史数据点的那些，这正是过拟合。」「它既在测流感，也在测冬天。」 / en: "Google once estimated flu levels from people's searches." "Researchers found it sifted 50 million search terms for the best fit to just over 1,100 data points. That's overfitting." "It was part flu detector, part winter detector." |
| l41 | 双语 | 建议 | 约 95 字，是全片最长的一句。先出现「另训一个模型」，后出现「看肺炎的模型」，两个模型很容易听混。结果（换医院掉分）放在最后，叙述顺序是倒的。 | zh 拆三句：「医学影像里也有。一个看胸片判断肺炎的模型，换到新医院，成绩就掉了。」「研究者发现，胸片里藏着医院的“指纹”：另一个模型几乎能百分之百认出片子来自哪家医院。」「它的好成绩，很可能一部分靠认医院，不是认病。」 / en: "Medical imaging has examples too. A pneumonia model that read chest X-rays did worse at a new hospital." "Researchers found the X-rays carry a hospital fingerprint: another model could tell, almost perfectly, which hospital each came from." "So part of its success likely came from recognizing hospitals, not disease." |
| l42 | zh | 记录 | 「画的标记笔迹」读起来拗口。 | 还有一个识别黑色素瘤的系统：医生在皮肤上画的记号，让它把一半多的良性痣误判成了癌。 |
| l43（对 l25–l27） | 双语 | 建议 | 概念边界不清：s5 把「沙发上的猫」当作过拟合的例子（「两个例子是同一件事」），s8 又说这类例子叫捷径学习，是过拟合的「近亲」。观众会问：沙发猫到底算哪个？Q5 恰好考这一点。l43 后半句和 l27 也有些重复。 | zh：后两个例子，和沙发上的猫一样，叫捷径学习，是过拟合的近亲：手头数据上亮眼，学到的却是巧合。 / en: Those two, like the cat on the sofa, are shortcut learning, a close cousin of overfitting: brilliant on the data at hand, yet built on coincidence. |
| l45 | 双语 | 建议 | 约 68 字，塞了五件事：演示时拿考试挑模型的坦白、模拟考、验证集、两种用途、考试留到最后。坦白插在「三个办法」和「第一」之间，打断了列表。 | 先讲办法，再讲坦白，拆两句。zh：l45a「第一，再留一份数据当模拟考，叫验证集，用它挑模型、及早发现过拟合。」l45b「刚才演示时，我们直接拿考试挑了模型；实际上，考试要留到最后才用。」 / en: l45a "One: set aside another slice of data as a mock exam, called a validation set. Use it to choose your model and catch overfitting early." l45b "In the demo, we picked the model with the real exam. In practice, save that for the very end." |
| l45 | en | 建议 | 「practice exam」和全片的「practice problems」（指训练数据）都用 practice，英语观众容易把验证集当成训练数据。 | 改用 mock exam（已写进上一行的改法）。 |

## 没有问题的必查项：证据

- **必查项 5（开头）达标**：
  - 前 20 秒有具体反差：l01 在约 0–7 秒抛出「几乎满分 → 一塌糊涂」，l02「程序没写错」再加一层悬念，冷开场约 12 秒结束。
  - 45 秒内有不含术语的定义：l09「把练习题背下来了，却没学会规律」不含任何术语，中文约 30–36 秒说完，英文约 30–35 秒。
  - 余量偏紧：只要包装卡停顿超过约 9 秒就会超出 45 秒，s1 删掉后定义会提前到约 12 秒。
- **必查项 2（有意呼应除外）**：l02 只给名字、l09 给定义、l49–l50 片尾复述，是有意呼应，不算重复。l20、l22、l36 反复出现「背下来」，是贯穿全片的母题，也不算重复。真正的重复只有 l24 和 l30/l32 两处，已经列在表里。

## 最重要的 3 条

1. **l17「六个模型」听感歧义（必改）**：纯听配音会误以为出现了六个模型。改成「再拿六个新点，模型都没见过」。
2. **s1 目录开场（l03–l07）**：和 v2 是同类问题，占约 18 秒，把定义推到约 30 秒。整段删掉，冷开场直接接定义。
3. **三个超长句 l39 / l41 / l45**：各塞了 4–5 个信息点，配音和字幕都吃力。l41 的两个模型会听混，l45 的坦白打断了列表。按表中改法拆句、调整顺序。

## 做得好的、别改掉的

- 冷开场 l01–l02：「几乎满分 / 一塌糊涂」加上「程序没写错」，反差具体，悬念直接。
- l36–l37：「它不用找规律，所以也就没找」和「用更少的东西，解释更多的事」。前一句把 O3 讲透，后一句好记。
- l27 后半句与 l45 的坦白：一个指出类比的边界，一个承认演示时拿考试挑了模型。这两处诚实，能主动堵住误解（对应 Q4 的 B 选项），改写时要保留。

## 其他

- O2 写的是「两种误差都高是欠拟合」，但 s4 没讲第一种模型的考试结果，l32 也只说「左边是欠拟合」，全片没有明说。建议在 l18 或 l32 里交代一句。
- 存疑：l19「二十多倍」、l28「三百次」、l35「四个数字」，请和实验输出、画面逐一核对。
- 全片只叫「练习误差 / 考试误差」，从没出现「训练误差 / 测试误差」，可 l10、l17 教的是「训练数据 / 测试数据」。观众以后看别的资料可能对不上，可以考虑在 l31 带一次正式叫法。
