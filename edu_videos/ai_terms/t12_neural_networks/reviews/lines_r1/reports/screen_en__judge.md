# screen_en__judge — 第 1 轮裁决（English on-screen text）

裁决人：screen_en__judge（claude-opus-5-5）。我核对了 `materials/screen_en.md` 全文，看了截图 s0_l04、s2_l12、s4_l27、s4_l30、s5_l36、s6_l44、s6_l46、s6_l47，也查了 `scenes/web/s3.html`（l22 → l23 出入点）、`scenes/web/s6.html`、`package.json`、`_shared/package.json`、`claims.json`、`research.md`、`timeline.en.json` 和 `tools/edu_review.py`（材料抽取方式）。

## 裁决
- P1 2 理由：按本项计数规则，「图表整体算 1 块」只用于块数上限，图内文字计入每屏 ≤22 词。这和列表、卡片行的规则一致：列表合成一块后，每项 ≤6 词、最多 6 项，本来就会超过 9 词。所以 b 把每屏图表块套 ≤9 词上限，判 l02–l03、l09–l13、l20–l24、l28–l30 和目录违规，都不成立。按图内文字逐屏复算：l29 = 15 + 5 = 20 词，l30 = 15 + 6 = 21 词，l12 ≈ 18 词，l24 ≈ 20 词，都在 22 以内，块数也不超过 4。没有违反任何硬上限，a 的证据站得住。剩下的小瑕疵是几处主谓完整的短句：l36「Later layers reuse earlier folds」、l44「Nobody taught it」、l13「Lines can’t bend」。所以给 2，不给 3。
- P2 1 理由：这一维有必改项。a 自己把 outro「Deep enough to see more」列为必改，却打 2，前后不一致。outro 属于严格项，它的意思和 l49「recognize really complicated things」对不上。b 指出 l44「Nobody taught it」把口播「Nobody told it what to look for」扩大成「没人训练过它」，这和事实相反，必改成立。l46「about −2 points」紧跟在 l43 的 top-5 错误率图之后，不标指标，红色的「−2」容易被读成错误率下降。而且 claims.json 写明论文原话是「top-1 performance」掉约 2%（见补充问题）。l36 和口播 l36 几乎逐字相同。b 关于 l47 引语的理由不成立（见驳回），但不影响定分。b 的 1 分站得住。
- P4 1 理由：严格项里有好几处「有点别扭」：冷开场 l01 h2「Learns it fine」偏口语，时态也和口播「learned」不一致；l04 eyebrow「Learning a bend」搭配生硬；章节标题「Lines can't bend」和本章 l16 屏上的「A line with one bend」字面上直接矛盾。按严格项规则，这些都要必改。另外 l31「Side by side: one bend each」和 l32「Stacked: fold again」不平行，l42「5 guesses; all wrong = a miss」标点混用，l13 弯撇号「’」和其他地方的直撇号「'」不统一。a 列了 l31/l32 和 l42，却没把冷开场、章节标题按严格项处理，所以 2 分偏高。b 的 1 分站得住。
- P5 2 理由：s3.html 里 l22 的「#big」在 l22+5% 入场、l23 起点出场，所以「37 / knobs / 12 × 2 + 12 + 1」实际只在屏上停约 2.2 秒，同时还有 5 个词的字幕「That's 37 knobs in total.」，超过约 3 词/秒的阅读量。所以 a 打 3（自己只记了「记录」）偏高。但算式只是辅助信息，大号「37 knobs」读得过来，而且 l25–l29 一直留着「37 knobs」eyebrow，等于补看。其他短句都没问题：l36 加 l37 合计约 8.9 秒，l38 只多 5 个词，l45 的数字格很好扫读。b 把 l22 判成整维度失败（1 分、必改），过重。裁为 2，l22 降为「建议」。
- P3 2 理由：两人都给 2 分，我维持。但有三处两人都漏了：l12 把 11.5 标成「Lowest loss」，l27/l28 又标成「Best line: 11.5」，同一个数换了说法；s6_l44 叠着两个 eyebrow（「ILLUSTRATION」在 x≈1010，「NOBODY TAUGHT IT」在 x≈1120），左右没对齐，「Illustration」标签离它要标的滤波器网格很远；s6 页眉「04 · AlexNet, 2012」因 text-transform:none 保持大小写混排，01–03 都是全大写（品牌名例外，只记录）。层级始终不超过 3 级，章节编号和目录一致，所以仍给 2。
- P6 2 理由：每条都有改写，但有几条改写不能直接替换，或者比原文更差。b 给严格项 outro 的改写「Complex pattern recognition」是名词堆叠，正好是 P4 的必改类型。b 把 l47 改成「The value of depth」/「Paper takeaway」，丢掉了论文原话这一证据。b 把 l20 改成「12 units」/「1 unit」，删掉了口播强调的「Layer 1 / Layer 2」。a 在目录「04 · AlexNet, 2012」那条给的是「改口播或接受」，不是屏幕改写。两人的 3 分降为 2。

## 补充问题

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l46 | P2 | 必改 | "Remove a middle layer → about −2 points" | claims.json 和 research.md 里论文原话是「a loss of about 2% for the top-1 performance」，可前一屏 l43 标的是「Error rate (top-5)」。屏上不写指标，观众会套用 top-5 错误率，「−2」还可能被读成错误率下降，和原意相反。b 只抓到「符号歧义」，没抓到 top-1 / top-5 指标错位；它的改写「Error: ≈+2 percentage points」在 top-5 语境下仍会被误读成 top-5。 | "Remove a middle layer → ~2 pts worse (top-1)" |
| agenda | P1/P4 | 必改 | 实渲卡片上的 prereq_hint "Not required — we'll cover each in a sentence."（材料没抽到） | 材料 `screen_en.md` 由 `tools/edu_review.py` 抽成「Prereqs: Gradient descent」，漏掉了系列级文字：标题「In this episode」、「HELPFUL TO KNOW」、「S1 · E4」和这句提示。这句提示是完整句子，放在严格项「目录」上；本期只有 1 个先修项，却写「cover each」；而且 l05 口播只是用一句话回顾了梯度下降。两位审稿人都没看到这张卡的实渲画面。 | 在本期 package.json 覆盖 prereq_hint："Not required — recapped in one line"；复审前补一张 agenda 实渲截图 |
| l12 / l27–l29 | P3 | 建议 | "Lowest loss 11.5" → "Best line: 11.5" | 同一个数（直线的最低 loss）前后两种标法，l27 的「Best line」可能被看成灰色那条线的名字，而不是 loss 值。 | l27–l29: "Straight line: 11.5" |
| s6_l44 | P3 | 建议 | eyebrow "ILLUSTRATION" 叠在 "NOBODY TAUGHT IT" 上方 | 两个 eyebrow 左右没对齐，「Illustration」挂在右侧文字栏，离左边的滤波器网格很远，看起来像第三级标题。 | 把「Illustration」移到网格左上角（和 s2/s4 图表右上角的做法一致），右栏只留一个 eyebrow |
| s6 eyebrow | P3/P4 | 记录 | "04 · AlexNet, 2012" | 01–03 页眉全大写，04 为保留品牌大小写而混排，四章看起来不统一。品牌例外可以接受，这里只记录。 | 保持现状，或整行不转大写 |
| materials（全项） | P3/P5 | 记录 | agenda / c_* / outro 截图字段为空 | 包装卡没有截图，材料也没抽出系列级文字（如 outro eyebrow「In short」、「Next」、AI 注释），两人对这几张卡的层级和停留时长都只能凭文字推断。 | 下一轮材料补上包装卡实渲截图和完整文字 |

## 驳回
- b · agenda（P1）：「目录合计 12 词、超过 9 词」不成立。按计数规则，列表或卡片行算一块，每项 ≤6 词、最多 6 项，编号不计；四项分别 3–4 词，合规。改写「Small networks / Going deeper」还和章节卡、页眉的叫法冲突，会破坏用户 2026-11-08 定的「目录、章节卡、页眉一个叫法」。
- b · l02–l13、l20–l24、l28–l30（P1，图表块 >9 词）：「图表算 1 块」只用于块数上限，图内文字计入每屏 ≤22 词，不适用每块 ≤9 词，所以不算违规。其中「Time of day (h) → Hour」可以保留为「建议」（a 已列）。l20 改成「12 units / 1 unit」会删掉口播强调的层号，更差。
- b · l35–l37（P1，对比行 10 词）：两个 h2 各 5 词，没有超限。改写「10 units → ≤11 pieces / 5 layers → 32 pieces」丢掉了「同样 10 个单元」这个比较前提，更差。至于补上单位「pieces」这一点，可以并入现有标题，比如「10 side by side: ≤ 11 pieces」。
- b · outro（P1，一块 10 词）：package.json 里 quote.en 是两行（"Simple units, stacked in layers" / "Deep enough to see more"），材料把两行拼成了一行，并不是一个 10 词块。outro 的 P2/P4 问题仍然成立，但 b 的改写「Complex pattern recognition」是名词堆叠，不采用。可以用「Stack deep → spot complex patterns」。
- b · l47（P1/P2）：引语卡在屏上显示论文原话、口播同时念出，是标准做法，这一屏的作用就是出示证据并标明来源（§7）。改成「The value of depth」/「Paper takeaway」既丢了证据，又引入了行话，更差。只保留 a 指出的问题：删掉重复的那条来源行。
- b · l19（P4）：「Add bends → bumps, steps…」里的省略号对应口播「almost any curve」的开放含义，是合理的。改成「Bends → bumps and steps」反而收窄了意思。
- b · l22（P5，必改）：问题成立，但级别降为「建议」。理由见 P5 裁决。
- a · s0 l04（P3/P4，必改）：「Neural networks」用复数作主题标题很自然，和本期片名「Neural networks and deep learning」一致；l23 用单数是因为在下定义（a neural network）。两处不冲突，不需要改。
- a · agenda「Prereqs: Gradient descent」（P4，必改）：「Prereqs:」是审稿材料抽取脚本（`tools/edu_review.py:449`）加的标签，实渲卡片上的标题是系列级的「HELPFUL TO KNOW」。这条针对的文字并不在屏幕上。真正的问题见补充问题中的 agenda 行。
