# voice_en__judge 裁决（第 1 轮，claude-opus-5-5，母语英语听感）

核对范围：materials/voice_en.md 全部 52 句；对照 script.en.md 与 scenes/web/s5.html、s6.html 确认 l17、l23、l26、l28 的画面锚点（s5 在 l17 计数到「1,797」，l23 有「每点：抽 20 次取中位数」，l26 聚焦 #two 那张潦草的 2；s6 在 l28 显示被测图与 96%）。

## 裁决
- V1 1 理由：b 站得住。l15「The number, plus "that's a three," is an example with its answer」像口述等式，第一遍听不懂；l50「has it ever learned this kind of question」是英语里不成立的搭配，且落在全片实用结论上；加上严格项 l52「Next time: overfitting, or why…」是标题腔（两人都判必改）。有必改且不止一处，不能给 2；a 的 2 分与它自己问题表里的 l52 必改自相矛盾。
- V2 1 理由：严格项片尾 l52 是「术语, or why…」的副标题朗读，两人都列必改；l51「In a sentence:」后接两句，属机械式总结开头，也在严格的片尾里；l33「These terms nest like circles」在没有章节卡的情况下突然转入分类，「These terms」没有刚说过的指代对象。严格项有必改，按规则只能 1。a 所说 l43–l48「One/Two/Three」是模板，这条理由不成立（见驳回），但不影响 1 分。
- V3 1 理由：l17「seventeen ninety-seven」第一耳听成年份 1797（画面会计数到 1,797，能缓解但不能替代耳朵）；l23「Do that twenty times」实际指的是「随机抽 10 张→训练→测试」重复 20 次再取中位数，耳朵听不出来；l45「closest of the ten」中「the ten」指什么没交代；l15「The number」分不清是写出来的字还是读出来的名字。问题实在，1 分成立。a 举的 l26/l28「this」有画面锚点，不算听不懂。
- V5 2 理由：两人 2 分维持，但两人都漏了节奏上的口癖：52 句里有 7 句以「So」开头（l02、l08、l21、l37、l40、l43、l49），其中 l43 和 l49 在同一节；l35（9.2s）、l23（8.6s）一口气说不完。旁白整体温和统一，l46「The model won't.」这种短句收尾很好，所以是小瑕疵而不是问题。
- V6 2 理由：b 的 3 分偏高。b 的 l17 改写「one thousand seven hundred and ninety-seven」在耳朵上比原句的数字更长、更拗口；l44 改写去掉了「One:」，但 l47、l48 仍是「Two:/Three:」，不能直接替换；l35 改写「Its neural networks」中「Its」指代不清，还丢了图上那层层嵌套的圆。a 的 l15 改写把「例子」误写成标签本身。两人基本都给了改写，也都排了前五，但有可用性瑕疵，所以给 2。

## 补充问题
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l50 / l52 | V2, V3 | 必改 | Next time an AI sounds totally sure, ask yourself… / Next time: overfitting, or why… | 两句间隔约 13 秒，都用「Next time」开头，但意思不同：一个是「以后你用 AI 时」，一个是「下一集」。片尾是严格项，耳朵会在这里串台。两人都没发现。改 l50，让 l52 独占「Next time」。 | Whenever an AI sounds totally sure, ask yourself: has it seen questions like this before? |
| l47 | V1, V3 | 建议 | Two: it gives predictions, not truth. That messy two? It was eighty-one percent sure it was a one, and it was wrong. | 这是讲识别数字的视频，同一句里列表序号「Two」紧挨着数字「two」和「one」，耳朵会撞车；l44「One:」后面紧接着就是「zero to nine」，也有同样的风险。改用 First/Second/Third，三句要一起改（l48 改成「Third,」）。 | Second, it gives predictions, not truth. Remember that messy two? It was eighty-one percent sure it was a one, and wrong. |
| l44 | V1, V3 | 建议 | One: it'll answer even things it never learned. Show this digit model the letter A, and it can only pick from zero to nine. | 与上条配套：「answer even things」搭配不自然（b 已指出）。这里给一个能和 l47、l48 序号保持一致的直接替换。 | First, it always answers, even on things it's never seen. Show our digit model the letter A, and it still picks a digit. |
| l43, l40 | V5 | 建议 | So when you use AI, remember three things. / So in effect, it taught itself that male candidates were better. | 全片 7 句以「So」开头，在 l40–l49 这段特别密（l40、l43、l49）。保留 l49 的「So」（它是真正的因果承接），这两句删掉。 | When you use AI, remember three things. / In effect, it taught itself that male candidates were better. |
| l31 | V1 | 建议 | That's how the large language models you chat with reply. | 长名词短语加关系从句，最后才落到动词「reply」上，「you chat with reply」听着像病句，收尾也弱。两人都判 natural。 | That's how chatbots, built on large language models, reply. |

## 驳回
- a · l43（必改）：「So when you use AI, remember three things.」是地道口语，不属于 TOC 朗读，a 给的改写也没更好。驳回必改，只按上面的「So」口癖降为建议。
- a · l44 / l47 / l48 的「模板」理由：一句话预告三点，再用 One/Two/Three 分述，是英语讲解视频的常见口语结构，不同于「In this episode: X. Y. Z.」那种目录朗读。驳回 a 的这条理由。改成 First/Second/Third 仍然可以采纳，但理由换成补充问题里的「序号和数字撞音」。
- a · l15 改写「And each "that's a three" is one example.」：把「例子」说成了标签本身（例子应是图加答案），意思错了，也没处理前一句。不采纳，改用 b 的改写。
- a · l26「like this messy two」、l28「this one's a three」：s5.html 在 l26 聚焦 #two 那张图，s6.html 在 l28 显示被测图和 96%，「this」有明确的画面锚点。视频里这样指代是正常的，不算缺陷。
- a · l16（cut）：「a model needs way more examples」是孩子类比和模型之间的关键差异，l21–l24 的实验正是在兑现这一句。删掉会断掉这层承接，驳回。
- b · l17 改写「one thousand seven hundred and ninety-seven」：比原句的数字还多 5 个音节，精确到个位对听众也没用。改用 a 的思路「nearly eighteen hundred handwritten digits」（画面计数 1,797，说法吻合）。
- b · l44 改写「It can answer without knowing.」：去掉了「One:」，但 l47、l48 保留了 Two/Three，不能直接替换；「without knowing」不知道什么也没说清。不采纳，改用补充问题里的 l44 改写。
- b · l35 改写「Machine learning is part of AI. Deep learning is part of machine learning. Its neural networks…」：「Its」指代不清，也丢掉了与画面嵌套圆对应的「Inside…」结构，并不比原句好。l35 问题本身成立，建议只在 l35 拆句：「Inside AI is machine learning, and inside that, deep learning. It runs on neural networks: many layers of simple math.」
- b · l12 改写「programmers wrote every AI answer」：把「AI 能做的一切」改成「每个答案」，意思变了，还与屏上「Programmers typed in eve…」对不上。不采纳；问题本身（与 l08–l10 重复）只作记录。
