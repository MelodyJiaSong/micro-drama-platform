# 审稿报告：双语编辑（语义一致）· ai_terms / t00_what_is_ai · script 第 2 轮

材料：`reviews/script_r2/materials/lines.md`（l01–l58）、`learning.json`（O1–O6、Q1–Q6）、`reviews/script_r1/issues.md`（上一轮汇总与处理结论）。只读，未改其他文件。

结论：两版整体对齐，本轮没有必改。剩下的都是轻重或衔接上的小差：英文丢了一处保留语气（l14），一处因果（l44），一处结构提示（l03）。最后这条上一轮标了「改」，但文字没动。

## 逐句问题表

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l03 | en | 记录 | 中文报了数「讲四件事」，英文 "Here's what we'll cover." 没报数，英文观众少了一个结构提示。上一轮已指出，处理栏写「改（v2.1 l03，采纳或等效改写）」，现稿未改。 | en：Four things today. |
| l06 | en | 记录 | 中文「换个角度：AI 像一台预测机器」是一个打比方的视角；英文 "How AI works as a prediction machine." 读起来像在讲 AI 的实际工作原理，语气比中文实，也和 l34 的 "is like" 不一致。 | en：Seeing AI as a prediction machine. |
| l13 | en | 记录 | 中文难点在「把怎么认写成规则」；英文 "try explaining how" 换成了「解释」，和下句 l14 "Rules like these" 的衔接稍弱。意思大体还在，因为 O2 英文目标用的就是 spell out。 | en：But try writing down how. |
| l14 | en | 建议 | 轻重不一。中文用「很容易漏掉……也容易认成……」留了余地；英文 "Rules like these miss some threes, and mistake other digits for threes." 是一般现在时陈述，读起来成了「必然会错」。上一轮事实核查就是为这类说满的话把 l14 标成必改，英文这次又说满了。 | en：Rules like these can easily miss some threes, or mistake other digits for threes. |
| l29 | zh | 记录 | 中文「这样多抽几回」，英文 "Try it many times"。实际是 20 次抽样（见上一轮 l29 核查）。「几回」听着偏少，两版的分量不同。 | zh：这样反复抽很多回，考试成绩一般只有37%左右。 |
| l44 | en | 记录 | 中文「因此分享了……」点明是因为 AlphaFold 获奖；英文 "went on to share" 只表示时间先后，因果没说出来。上一轮这条只解决了一部分（原来的 and 改成了 went on to）。事实两版一致：2024 年化学奖的一半由两位负责人分享。 | en：Its two lead developers shared half of the 2024 Nobel Prize in Chemistry for it. |

## 必查项逐项说明

1. **逐句比意思**：l01–l58 逐句对过，问题都列在上表。以下限定语两版一致，已核对：l15「大多 / Most」、l23「通常…常常 / usually…often」、l32「这一次 / Here」、l45「大约…估计 / About…estimated」、l46、l48「可能 / can」、l53「主要…也和…有关 / mostly…and also」、l56「主要 / mainly」。轻重不一的只有 l14（en 少了「很容易」）、l06（en 语气偏实）、l44（en 少了因果）。
2. **各用本语言的说法**：下面这些是允许的本地化，不算问题：l05「小实验」→ a real experiment；l24「上千道」→ a thousand；l47 中文「女子国际象棋队队长」对应 Reuters 原文 "women's chess club captain"，captain 的职务没走样；l50 中文「一本正经地说」，英文用引号直接给出答案来传达同样的语气。
3. **事实、数字、出处、限定语**：两版逐项一致，已核对：1797 / 1,797；八行八列 / eight-by-eight；300 张考题；10 例 37%（20 次抽样的典型值）；随机猜 10%；100 例 88%；近 1500（1797−300=1497）例 97%；错 10 题（10/300 ≈ 3.3% 的错误率，和 97% 对得上）；96%、92%、81%；AlphaFold 2024 诺贝尔化学奖「一半」、两人；ChatGPT「约两个月、估计、每月一亿」；路透社、亚马逊、十年、大多来自男性、"women's"、工具被放弃。除 l29「几回 / many times」的分量差（见上表）外，没有不一致。
4. **能否各自达成 learning.json 目标**：
   - O1：两版都有 l02、l09、l15–l17、l19、l25、l56–l57；「带答案」两版都在 l16、l22 讲到。英文 l09 和 l25 已统一成 traditional program，和 O1 英文原文一致。
   - O2：两版都有 l10（算工资、订机票）、l11、l13–l14、l39（下棋程序算、算工资程序不算）。英文 l13/l14 有上表的小瑕疵，不影响达成目标。
   - O3：两版都有 l27「只有考没见过的题才知道是真会」、l29–l32「越多、越全」。
   - O4：两版都有 l34–l35、l38「猜得好≠说得对」、l50–l52、l54。
   - O5：两版都有 l39–l41，圈层顺序一致：AI ⊃ ML ⊃ DL ⊃ LLM。
   - O6：两版都有 l46–l48、l53「先问从什么数据里学」。
   - 结论：两版各自都能支撑六个目标，没有一版缺某个目标的要点。
5. **R：复核上一轮本角色问题**：
   - l03（en 缺「四件事」）：**未解决**。处理栏写了「改」，现稿英文仍是 "Here's what we'll cover."，见上表。
   - l09（en ordinary → traditional）：**已解决**。英文 l09 "a traditional computer program" 和 l25 "A traditional program" 一致。
   - l13（en "So does an eight" 语法接不上）：**已解决**。现稿 "An eight has those too. … Open on the left at the bottom? So is a five." 语法成立，意思和中文「上下两个弯 / 下半截开口朝左」一致。另有一个「explaining」的小瑕疵，见上表。
   - l14（en "slip through" 有歧义）：**已解决，但改出了新问题**。歧义没了，但改写时丢了中文的「很容易」，成了轻重不一，见上表。
   - l38 → v2.1 l39（「人写规则也算 AI」没交代范围）：**已解决**。两版都改成「人写规则的下棋程序也算；算工资的普通程序不算」，O5 和 Q1 的误解都照顾到了。
   - l42 → v2.1 l44（en 缺「因此」的因果）：**部分解决**。and 改成了 went on to，因果仍然没说出来，见上表。
   - l53 → v2.1 l57（en 缺「自己」）：**已解决**。现稿 "It teaches itself patterns from examples."
   - 本角色上一轮没有作者「不采纳」的条目。

## 最重要的 3 条

1. **l14 en**：要补回保留语气（"can easily"），不然英文又成了上一轮事实核查标必改的那种说满的话。
2. **l03 en**：处理栏标了「改」，文字没动。要补上 "Four things today."，并核对其他标了「改」的条目是否真的落了稿。
3. **l44 en**：补上 "for it"，让英文也说出获奖是因为 AlphaFold，和中文「因此」对齐。

## 做得好的、别改掉的

1. 保留语气两版对得很齐（l15、l23、l32、l45、l48、l53、l56），本轮几乎没有一版说满、另一版留余地的情况，只有 l14 例外。
2. l39 用「下棋程序算、算工资程序不算」给 AI 划边界，两版用同一对例子，O5 和 Q1 都清楚。
3. l50–l52 的字母 A、92%、潦草的二、81% 这组例子，两版数字和逻辑完全一致，英文用引号直接给出答案的做法很自然。

## 其他

- 上一轮 teacher 在 l02 提出要说出全称「人工智能 / artificial intelligence」，处理栏写了「改」，但现稿两版都没有出现全称（不属本角色，建议作者核对）。
- 英文 l18、l22 "The way of telling … apart that it ends up with" 和 l24 "has made a thousand dishes: taste, hear…, adjust" 读起来偏绕（属 native_en 范围）。
