# 审稿报告：双语编辑（语义一致）· ai_terms / t00_what_is_ai · script 第 3 轮

材料：`reviews/script_r3/materials/lines.md`（l01–l58）、`learning.json`（O1–O6）、`reviews/script_r2/issues.md`（上一轮 bilingual 行：l03、l06、l13、l14、l29、l44）。

结论：本轮没有必改。两版的事实、数字、出处和限定语全部对齐。剩下的是几处轻重不一：英文 l40 说满了；l06 有一条上一轮的问题没处理，另一条（l29）现在也还没处理。v2.2 改过的句子（l23–l25、l35、l39、l46、l50）里，只有 l24、l40 两句的轻重和中文有差别。

## 逐条问题

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l06 | en | 建议 | **R：未解决**（上一轮本角色与 teacher 都记了，处理栏只写了「v2.2 未专门改动」，没给不采纳的理由，所以问题还在）。中文「换个角度：AI 像一台预测机器」是打比方的视角；英文 "How AI works as a prediction machine." 读成在讲 AI 的实际工作原理，比中文说得实，也和 l34 的 "is like" 对不上。 | en：Seeing AI as a prediction machine. |
| l13 | en | 记录 | **R：未解决**（上一轮记录，未改）。中文的难点是「把怎么认**写成规则**」，英文 "try explaining how" 换成了「解释」。好在 l14 有 "Rules like these" 补救，O2 的意思没丢；但这句是英文版里唯一把「规则」换成别的说法的地方。可以接受，改了更贴。 | en：But try writing the rule. |
| l14 | en | — | **R：已解决。** "can easily miss … or mistake …" 和中文「很容易漏掉……也容易……」留的余地一样，没改出新问题。 | 保留。 |
| l24 | en | 记录 | **新（v2.2 改写带出）。** 中文「照菜谱一步一步做就行，**就像**传统程序」是类比；英文 "That's a traditional program." 成了等同，语气比中文实。不影响理解。 | en：Like a traditional program. |
| l29 | 双语 | 记录 | **R：未解决**（上一轮记录，未改）。中文「这样多抽几回」听着是三五回，英文 "Try it many times" 是很多回；实际是 20 次抽样（据上一轮 issues 全片行与 l29 核查行，画面也注了 20 次）。两版说的次数一多一少。 | zh：这样抽上二十回，考试成绩一般只有37%左右。<br>en：Try it twenty times, and the typical score is about 37%.<br>（若 20 次未最终确认，zh 改「这样反复抽很多回」，en 保留） |
| l32 | en | 记录 | 中文「相册认猫，也是同一个道理」说的是道理相同；英文 "finds your cat the same way" 说成了做法相同（相册的模型和数据规模都不一样），比中文说得满（teacher 上一轮也记过）。 | en：Your photo app works on the same idea. |
| l40 | en | 建议 | **新（v2.2 改写带出），轻重不一。** 中文「它和大脑里的神经**差得很远**」有分寸；英文 "they're **nothing like** the neurons in a brain" 是全称否定。神经网络最初确实受神经元启发，英文说过头了。另外这句 "they" 离得最近的复数是 "the names"，听起来像在说「名字和神经元毫不相像」。 | en：Don't let the names fool you: these networks are only loosely like brain neurons, and "deep" just means many layers, not deep understanding. |
| l44 | en | — | **R：已解决。** 句末加了 "for it"，因果和中文「因此」对上了；"went on to" 留着也无妨。事实两版一致：两人分享 2024 年诺贝尔化学奖的一半。 | 保留。 |
| l46 | zh | 记录 | 中文「亚马逊**曾想用** AI 筛简历」比英文 "once **tried using**" 弱，像是只有过打算、没真做出来。路透社报道的是这个工具做出来了，也试过。下半句「这个 AI 学的……」能补回来，但开头的分量两版不一样。 | zh：据路透社报道，亚马逊曾试用 AI 筛简历；（其余不变） |
| l03 | en | — | **R：已解决。** "Four things today." 报了数，和中文「讲四件事」对齐。 | 保留。 |

## 必查项逐项说明

1. **逐句比意思**：58 句逐一对照，问题都在上表。其余各句两版一致，例如：l15 的「大多换了一个做法」对 "Most of today's AI"，l19 的「其实大多是……学来的」对 "most of it was learned"，l23 的「两点不像」两点都在，l27 的锁题目的（真会还是只记住），l34 的「不是看未来」对 "Not predicting the future"，l50–l52 三处把握数字和推理顺序，l56–l57 的「主要不靠」对 "isn't mainly built from"。没有发现漏点。
2. **允许本语言自然说法**：英文按本语言习惯做了本地化，意思没变，这些不算问题：l38 补 "the technology behind chatbots" 对应「能跟你聊天的」；l47 英文直接用原词 "women's chess club captain"，中文译作「女子国际象棋队队长」；l20 写成 "a 3 is two half circles, stacked"。
3. **事实、数字、出处、限定语**：数字逐个核对，两版一致：1797、300、将近一千五百 / nearly fifteen hundred（1797−300=1497）、10 个例子 37%、瞎猜 10%、100 个 88%、全部 97%、300 道错 10 道（≈96.7%，四舍五入为 97%，不矛盾）、96%、92%、81%、2024 年诺贝尔化学奖一半由两人分享、上线约两个月估计月活一亿、路透社、十年简历大多来自男性。限定语两版都在：通常/usually（l23），往往/usually、一般/typical、左右/about（l29），这一次/Here（l32），常常/often（l43），大约、估计/About、estimated（l45），也可能/can（l46、l48），主要/mostly（l53），主要/mainly（l56）。只有 l40、l46 两处轻重不一，l29 次数一多一少，都已列进上表。
4. **各自能否达成 learning.json 目标**：
   - O1：zh / en 的 l02、l09、l15–l17、l19、l22、l25、l56–l57 都在。「带答案」两版都在 l16、l22 讲清了。
   - O2：两版都有工资对手写三的对照（l10–l14），l39 两版也都提到算工资程序。英文 l13 措辞弱一点，但 l14 补上了，能达成。
   - O3：l27 讲了「用没见过的题考」，l29–l32 讲了「越多越全越准」，两版完整。
   - O4：l35、l38、l50–l52、l54 两版都讲了「把握高不等于对」和「没学过也照样答」。
   - O5：l39–l41 的圈层顺序和「规则式下棋程序也算 AI」两版一致。英文 l40 说满了，但不影响分清圈层。
   - O6：l46–l48、l53 两版一致。
   - 两版的缺口完全相同（例如 l57 两版都没说「带答案」），没有哪一版单独落下哪个目标。
5. **复核上一轮本角色问题**：l03 已解决；l14 已解决；l44 已解决；l06 未解决；l13 未解决（记录级，可接受）；l29 未解决。三条未解决的，作者都没写「不采纳」理由，只写了「v2.2 未专门改动」，所以谈不上理由成不成立。其中 l06 有两个角色指到，本轮升为建议。

## 最重要的 3 条

1. **l40 en**："nothing like the neurons in a brain" 比中文「差得很远」说满了，"they" 的指代也含糊。改成 "these networks are only loosely like brain neurons"。
2. **l06 en**：上一轮遗留，把「AI 像预测机器」说成了 "How AI works as"。改成 "Seeing AI as a prediction machine."
3. **l29 双语**：「多抽几回」和 "many times" 次数一多一少。确认是 20 次后，两版都写明二十回 / twenty times。

## 做得好的、别改掉的

1. 两版的保留语气逐句对得很齐（大多 / most、通常 / usually、估计 / estimated、可能 / can、这一次 / Here），所有数字都一致。
2. 上一轮 l03、l14、l44 都改到位了，改法没有带出新问题。v2.2 新改的 l23、l25、l35、l50 两版严格对应。
3. 英文本地化得当：l38 补了 "the technology behind chatbots"，l47 保留原词 "women's"，中文译「队长」。用的是各自语言的自然说法，事实一点没走样。

## 其他

- l36（两版同样）：l35 刚把主语收窄成「我们这个模型 / Our model」，l36「给它一张照片…一段声音」听着像这个只认数字的模型也能认猫、听声音，和 l50 的「只认数字」矛盾。建议句首加「换成别的 AI / Other AI works the same way」之类的主语切换（属 teacher / editor 范围）。
- l25（两版同样）：「尝一口就像模型先猜一个答案」，可尝一口在做菜里更像检查结果，做出这道菜本身才像猜。类比的对应关系请 teacher 判断。
