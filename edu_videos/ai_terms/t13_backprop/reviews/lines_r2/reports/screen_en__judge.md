# screen_en 裁决（第 2 轮，judge · claude-opus-5-5）

依据：`materials/screen_en.md` 逐屏文字与计数，以及截图 s0_l03、s2_l10、s4_l21、s4_l25、s4_l26、s4_l28、s4_l30、s4_l33；并对照 `previous.md` 中本项 I1–I38 的处理。只按 materials 与截图裁，不看作者开审后的改动。

## 裁决

- P3 1 理由：b 的依据放错了维度。l29–l30 每行 7 个数超过 6 项归组上限，这是 P1 的计数问题，不是层级问题；s4_l30 截图的层级其实清楚（页签、大数+单位、数字行、✓ Identical）。但 P3 仍然有实打实的问题。一是 agenda 提示行「Prereqs: Last time: neural networks」两个标签连着两个冒号叠在一起，体例也和 01–04 的「NN · 名称」不一致，而它属于严格项（衔接卡），沾一点毛病就是必改。二是 a 自己列出的命名漂移：同一个笨办法先后叫「One at a time?」（l03）、「The slow way」（l10–l11）、「Nudge one by one」（l29–l34）。有必改项，所以不能给 2。
- P5 1 理由：两人引的证据一样：l25 屏上 28 词、4.6 s，l26 屏上 25 词、4.2 s。a 在问题表里把 l25、l26 标为 P1/P5 必改，同时给 P5 打 2，自相矛盾。看 s4_l25 截图：两个新算式「6 × 2 = 12」「6 × 1 = 6」和旧的责任牌 36/6/24 都是同一种红色，挤在同一列，观众要在 4.6 s 里从 7 个红色数字中找出新出现的两个，还要同时读字幕。b 站得住。
- R 1 理由：严格项里有两条没过。一是 I2 agenda：作者回复的处理是「改成 Last time: neural networks」，但 materials 实际是「Prereqs: Last time: neural networks」。「Prereqs」没去掉，还多出一个双冒号，属于改出新问题。二是 I1 片尾：「Overfitting」作为下一集的标识没有截图可证，a 凭作者一句「模板会加 next」就接受，对严格项不够。此外 I17–I21（网络图字数）两人都判未解决；I25 的 7 项数字行按本轮计数口径仍然超限（上一轮裁决只禁止删数字，并没有豁免 7 项）。a 判它已解决不成立。
- P6 1 理由：（抽查，两人共同漏判）好几条改写比原文还差，或者不能直接替换。a 把 l10 的「3 / runs」改掉，会打乱上轮裁决定下的口径（I12：reruns 不含原样那一遍，runs 含）。b 把 l29–l30 拆成「60 · 12 · 30 · 6」和「36 · 24 · 6」分两拍出现，毁掉了 l30「Same seven numbers, exactly」需要的同屏逐一对照。b 在 l27 的改写自己又放进一行 7 项（「60 · 12 · 30 · 6 · 36 · 24 · 6」），还删掉了上轮裁决定下的因果「Guess too high →」。于是 l29–l30 这条必改超限，两人都没给出能用的改写（a 没给，b 给的更差）。b 给 3 分不成立。
- P2 2 理由：（抽查）两人给 2 分，我维持。l09「Gradient = slope」、l10「Nudge → rerun → compare」、l40 两行确实做到了屏上给结构、口播负责解释。两人共同漏掉两处，都是建议级：l28 口播说「29 becomes about 24. Much closer」，屏上只有「23.88」，29 和实际 23 都不在屏上，「closer」在画面上没有参照；l39「every slope at once」的「at once」是口播没有的说法。见补充问题。

## 补充问题

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l29–l30 | P1/P6 | 必改 | 两张卡各一行「60 12 30 6 36 24 6」 | 每行 7 项，超过 6 项归组上限（两人都确认了超限）。但 a 没给改写，b 拆成两拍又毁掉了「一模一样」的同屏对照，必改项至今没有可用改写。 | 七个数仍然同屏、同序，每行在第 4 与第 5 个数之间加细竖线，按两层分组：「60 12 30 6 │ 36 24 6」。每组 ≤6 项，各算一个同形块；不增删一个字，两卡上下对齐，「✓ Identical」不动 |
| l28 | P2 | 建议 | 「One small step: closer」+ 圈内「23.88」 | 口播「29 becomes about 24. Much closer」，但屏上已经没有 29，也没有实际车费 23，「closer」缺少可比的数字。屏上本该给的对比数字缺了。 | 标题改「One step: 29 → 23.88」（4 词）；猜测圈下加一个小灰标签「Actual: 23」。同时按 b 的写法收走「A」「B」，图内字数不增加 |
| l26 | P2/P4 | 建议 | 「Blame = received × input」 | 「received」这个词口播没有（b 已指出）。b 的改写「incoming error」又带进一个口播没有的新词。口播 l26 说的是「does the same」，屏上照搬 l22 的同一条公式，最能表达「同一个算法再用一遍」 | 「Blame = error × input」（与 l22 逐字相同；红色的 error 此时指向 A 收到的 12、B 收到的 6） |
| l39 | P2 | 建议 | 「PyTorch: every slope at once」 | 口播是「one line … gives every knob its slope」。「at once」是口播没讲的同时性说法，屏上应该给的「一行代码」反而没写出来。 | 「One line: every slope」（4 词） |
| l20–l21 | P2 | 记录 | 「Guess 29」「Actual 23」 | 输入有单位「km」，车费没有单位，而口播说「29 yuan」。不影响理解。 | 可选：在「Guess」一行的 29 后加小号「yuan」，否则保持不变 |

## 驳回

- a · l10–l11「3 / runs」「of runs, per step」：上轮裁决（I12）特意把 l10 改成 reruns，用来和含原样那一遍的 runs（l29「8」= 1+7、l31「1,000,000,001」）区分。3 个旋钮应是 3 reruns、4 runs，统一成「runs」反而让数对不上。a 列在 P3 的「reruns/runs 不一致」也不成立，这是有意的区分。
- b · l29–l30 改写（分两拍「60 · 12 · 30 · 6」/「36 · 24 · 6」）：l30 口播「Same seven numbers, exactly」要的是七个数同屏逐一对齐，分拍出现就没法对照了。改用补充问题里的分组竖线方案。
- b · l27 改写「All seven knobs: down」+「60 · 12 · 30 · 6 · 36 · 24 · 6」：一行 7 项违反了 b 自己在 l29–l30 援引的 6 项上限；又删掉了上轮裁决定下的「Guess too high →」因果（I22）。原文「Guess too high → all turn down」保留，图内按 a 的写法收暗旋钮读数。
- b · P3 的依据（7 项数字行超出归组上限）：这是 P1 的计数问题，s4_l30 截图的层级是清楚的。P3 判 1 的理由改为 agenda 双标签和笨办法命名漂移，不用这一条。
- b · l03「One at a time? Too slow」（必改）：「Never finishes」是标题常见的省略主语写法，读出来顺，也对应口播「You'd never finish」。「Too slow」反而丢了「永远做不完」的力度。原文维持。
- a · l38「Earlier, similar methods」/ b · l38「Earlier methods」：a 的写法读出来别扭；b 的写法丢了「similar」，像是说早就有人发明了同一个方法，违背 C13 限定语的本意。若要改成提纲体，用「Similar ideas: earlier」（3 词，和口播「similar ideas earlier」同词）；否则维持原文（作者「不改」理由成立）。
- a · l18–l24「请口径负责人把旋钮读数比照坐标刻度豁免」：本轮口径（2026-11-09）已明确规定图内文字只有坐标刻度数字豁免，审稿与裁决都不能扩大豁免范围。这一条只能作为给用户的口径建议，不能当作对超限的处理。
