# 审稿报告：双语编辑（语义一致）（ai_terms / t00_what_is_ai · script 第 1 轮）

审稿材料：`reviews/script_r1/materials/lines.md`（l01–l54）、`learning.json`（O1–O6、Q1–Q6）。未读其他审稿报告，未改动任何其他文件。

总体结论：两版意思高度一致，事实、数字和保留语气基本逐句对齐，没有发现中英意思相反或数字不一致的地方。问题集中在三处：l38 两版的表述都有歧义；英文版 l09 的术语和后文不统一；l49 回指了一张旁白没介绍过的图（存疑）。

## 逐条问题表

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l38 | 双语 | 建议 | 两版都写「人写规则的办法也算 AI / rules that people write count as AI」，没说清是「用人写规则做成的 AI」。观众会顺着 l09–l10 推出「算工资程序也是 AI」，正好落进 Q1 记录的误解「凡是电脑做的事都叫 AI」，也让 O5「人写规则的办法也算 AI」显得含糊。英文字面上更是在说「规则本身算 AI」。两版轻重一致，但两版都没把 O5 讲清。 | zh：AI 是最大的圈，人写规则的下棋程序也算；机器学习在它里面。 / en：AI is the biggest circle; chess programs built on written rules count too. Machine learning sits inside it. |
| l09 | en | 建议 | 中文 l09 和 l25 都用「传统程序」，英文 l09 用 ordinary computer program，l25 换成 traditional program。O1 要比的正是「传统程序 vs 机器学习」，英文观众未必能把两处连起来，讲回来时也少了一个能用的词（O1 英文目标原文即 traditional program）。 | en：Start with a traditional computer program. People write the rules, one by one, and the computer follows them. |
| l49 | 双语 | 建议（存疑） | 两版都回指「刚才那张写得很潦草的二 / Remember that scrawled two?」，但旁白此前从没介绍过这张图。l33 只说「有几张，连人看了都要犹豫」。如果 l33 的画面没有单独亮出这张 2、标出模型答「1」，两版都会让人看不懂，应升为必改。核实办法：查 l33 的分镜或画面，确认这张 2 已单独展示。 | zh：第二，它给的是预测，不是真理。这张写得很潦草的二，它有81%的把握说是一，还是错了。 / en：Two: it gives predictions, not truth. This scrawled two? It was 81% sure it was a one, and it was wrong. |
| l03 | en | 记录 | 中文报了数「讲四件事」，英文没有。下面正好四条议程，英文观众少了一个结构提示。 | en：Four things today. |
| l13 | en | 记录 | “Two bumps, one on top of the other? So does an eight.” 前半句没有动词，接 So does 不合语法，口播会让人别扭。下半句 Opens… So does a five 没问题。 | en：Two bumps, stacked? An eight has those too. |
| l14 | en | 记录 | slip through 在「过滤」语境里容易听成「混过去、被接受」，中文意思是「漏认」。意思没反，但不如中文直白。 | en：However many rules you write, some threes get missed, and some other digits get mistaken for threes. |
| l42 | en | 记录 | 中文有「因此」，把获奖和 AlphaFold 因果相连；英文用 and 并列，因果变弱，听着像两件并列的事。事实一致：2024 年化学奖一半由 Hassabis 与 Jumper 分享，表彰蛋白质结构预测。 | en：…to predict shapes directly, and for it, the two people who led its development shared half of the 2024 Nobel Prize in Chemistry. |
| l53 | en | 记录 | 中文「自己学会规律」里的「自己」是 O1 的关键（finds the pattern itself），英文收尾没有这层；l17 有 on its own，所以只是收尾稍弱。（建议改法比原句多一个词） | en：It finds the patterns in examples itself. |

## 必查项逐项说明

**1. 逐句比意思（一致 / 走样 / 漏点 / 轻重不一）**
54 句逐句比过。没有发现意思走样或相反。漏点只有 l03（数字「四」）、l42（因果「因此」）和 l53（「自己」），都已列入表格。保留语气全部对齐：l15「大多 / Most of」、l19「大多 / Most of」、l23「通常…常常 / usually…often」、l29「往往…左右 / usually…about」、l34「其实就像 / something like」、l40「大多 / mostly」、l42「往往 / often」、l43「估计 / was estimated」、l44「据路透社报道 / According to Reuters」、l52「主要不靠 / isn't mainly」。l45 中文「只要出现…就会被扣分」比英文 started marking down 略重，但与路透社原文 penalized 的力度相当，不算轻重不一。

**2. 允许各用本语言自然说法 / 换例子**
英文多处做了合理的本地化，没有改变意思，不算问题：l20 teaching a child their numbers、l37 用 chatbots 指代、l45 英文直接用 women's（中文另加了解释「英文是 women's」）、l48 with a straight face 对「一本正经」。两版例子完全相同（手写 3、猫、做菜、AlphaFold、ChatGPT、亚马逊），没有出现某一版换了例子却换错的情况。

**3. 事实、数字、出处、限定语一致**
逐个核对过：1797 张、8×8、留出 300 张、10 / 100 / 将近 1500（1797−300=1497）、37% / 10% / 88% / 97%、300 题错 10 题（290/300≈96.7%，与 97% 自洽）、96% 是三、92% 是四、81% 是一、2024 年诺贝尔化学奖「一半、两人」、ChatGPT「约两个月、月活约一亿、估计」、亚马逊「十年、大多来自男性、women's chess club captain、后来放弃」、出处「路透社 / Reuters」。两版完全一致，也和公开资料相符（sklearn digits 数据集；2024 年化学奖一半授予 Hassabis 与 Jumper；UBS 估算 2023 年 1 月月活约 1 亿；路透社 2018 年报道）。l29 随机抽 10 个例子时，平均约有 3.5 个数字一张都没抽到，「往往有几个 / usually a few」两版都说得对。

**4. 两版是否都能达成 O1–O6**
- O1：两版都有 l09、l15–l17、l25、l52–l53。英文 l09 的术语不统一（见表），是唯一让英文稍弱的地方。
- O2：两版都有 l10（算工资、订机票，规则清楚）、l11、l13–l14（规则说不清、写不完）。能达成，但 l38 的歧义可能让观众把「写规则的程序」都当成 AI，和 Q1 的考点相互干扰（见表）。
- O3：两版都有 l27（锁起来当考试题、训练时不看）、l29–l31（例子越多越准，且 l29 点出「有些数字没见过」，对应「越全」）、l32。两版一致，能达成。
- O4：两版都有 l35（带把握）、l48（没学过也照样回答，92% 是四）、l49（81% 把握还是错了）。能达成。l49 的回指是否成立待画面核实（见表）。
- O5：两版都有 l38–l40 的嵌套关系（AI ⊃ 机器学习 ⊃ 深度学习 ⊃ 大语言模型）。嵌套能达成；「人写规则也算 AI」这半条两版都含糊（见表）。
- O6：两版都有 l44–l46、l50，偏见案例和「先问它从什么数据里学」一致。能达成。

## 最重要的 3 条

1. **l38（双语）**：「人写规则的办法也算 AI」没说清，两版都可能让观众得出「所有写规则的程序都是 AI」，和 l09–l10 的对比以及 Q1 的误解直接冲突。改成具体例子（「人写规则的下棋程序也算」），把边界讲清。
2. **l49（双语，存疑）**：「刚才那张潦草的二」在旁白里没有出处。先核实 l33 的画面；如果没有单独亮出这张图，就改成不依赖前文的「这张…」。
3. **l09（en）**：ordinary 改成 traditional，和 l25 以及 O1 的关键词保持一致。

## 做得好的、别改掉的

- 保留语气和出处两版严格对齐（大多 / Most、估计 / was estimated、据路透社 / According to Reuters），没有哪一版说得更绝对。
- 实验数字形成一条能自洽核对的链（1797−300≈1500、290/300≈97%），两版逐字一致。
- 英文没有逐字硬译，而是用本语言最自然的口语（l13 So does a five、l46 Bias included、l48 with a straight face），节奏短、适合口播；中文 l45 主动补了「英文是 women's」，照顾到了中文观众。

## 其他

- 中文 TTS 可能把 l26 的「1797」读成「一七九七」，建议写成「一千七百九十七」或在发音表里锁定读法。
- learning.json 的 O5 原文「人写规则的办法也算 AI / rule-based programs also count as AI」本身也有 l38 的歧义，可以一起改成「人写规则做成的 AI 也算」。
- l45 中文一句里塞了引号、英文注释和例子，口播偏长，可以考虑在「women's」之后断句。
