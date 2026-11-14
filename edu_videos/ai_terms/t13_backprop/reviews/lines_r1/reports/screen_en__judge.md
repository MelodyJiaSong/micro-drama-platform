# screen_en__judge（claude-opus-5-5）— English on-screen text，第 1 轮裁决

依据：materials/screen_en.md 全文；截图 s0_l03、s0_l04、s2_l10、s3_l15、s4_l21、s4_l25、s4_l27、s4_l28、s4_l30、s4_l33、s5_l38、s5_l40；核对 scenes/web/s2.html、s4.html 的屏上文字源（只读）。未以当前 script 为准。

## 裁决
- P2 1 理由：b 的 l28 证据成立。截图里 "6 × 2 = 12"、"6 × 1 = 6" 仍是满色红字，紧挨更新后的 "×1.82"、"×0.88"。节点圈仍是旧值 6 和 4，但按新旋钮算 A=0.7×5+0.94=4.44、B=0.25×5+1.97=3.22，屏上数字算不出 23.88，新旧状态混在一屏。a 自己的问题表也把 outro "Pass the blame back, every knob in one trip" 列为 P2 必改（严格项，几乎逐字重复 l41–l42），给 2 分与自己的表矛盾。另见补充 l27 "All positive" 是口播没出现的说法。
- P3 2 理由：b 的证据（l29–l30 七项数字行超过六项分组上限）属于 P1 计数，不是层级或一致性问题。agenda、章节卡与 eyebrow 的四个章节名逐字一致（"01 · Too many knobs to try" 等），截图中 l30 两张卡的小号大写标签作卡片 kicker 读得清，"8"/"1" 主次分明。l40 后出现的 76px "Autograd = Backpropagation" 压在 54px 行下面，属小瑕疵。补充的 l10 "3 runs" 计数口径不一致为建议级，维持 2。
- P4 1 理由：严格项里有确实读着别扭的句子。outro "Pass the blame back, every knob in one trip" 是两个分句硬拼，念出来不顺；冷开场 l04 eyebrow "One trip backward, all of them" 里的 "all of them" 无所指（截图里它是整屏唯一的说明文字）。l15–l16 "Backward: one step each" 的 "each" 没有指代。a 把前两条列为 P4 必改却给 2 分，自相矛盾；按 b 判 1。
- P5 2 理由：b 按全屏累计算 l25 "28 words in 3.8s ≈ 7.4 words/s" 不成立。l25 实际只新增 "6 × 2 = 12"、"6 × 1 = 6" 两式，且与口播 "Times 2 gives A 12. Times 1 gives B 6" 同步；l26 只加 4 个数字，用时 5.4s。真正偏紧的是 l40：5.0s 内新增约 11 个词，同时要读字幕。l30 在 5.4s 内加一张卡加一行勾，也偏紧。属小瑕疵，取 a 的 2。
- P6 2 理由：两人对标出的问题都给了改写，但有几处改写站不住，b 给 3 偏高。b 的 l18–l21 改写删掉旋钮值，而 l25 口播 "Times 2/Times 1" 要用这些值；l29–l30 删掉两行数字，口播 "Same seven numbers, exactly" 就没有可对照的证据；l24 的 "Error × knob" 丢掉等式左边，也破坏了与 "Blame = error × input" 的平行。a 对 l25–l28 只说要等裁定、没给能用的改写；l40 改成 "Autograd runs backpropagation"，仍与口播 "automatic differentiation" 对不上。两人都漏了 l27、l10、l30 三处（见补充）。

## 补充问题

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l27 | P2 | 必改 | "All positive → all turn down" | 口播只说 "The guess was high, so all turn down"，从没讲过梯度符号为正。屏上用 "positive" 是口播没有的新概念；观众看到的又是一组红色"blame"数字，并不知道正号指什么 | "Guess too high → all turn down" |
| l10 | P3 | 建议 | "3 runs" | 3 个旋钮显示 3 runs，只算每个旋钮重跑一次。l29 用的口径是 "8 forward runs"（1 次原样跑 + 7 个旋钮），l31 是 "1,000,000,001 runs"，也包含原样那一遍。同一种笨办法出现两种计数，细心的观众会对不上 | "3 reruns"（与口播 "rerun" 一致，并与包含原样那遍的 "runs" 区分） |
| l30 | P2 | 建议 | "✓ Same seven numbers" | 与口播 "Same seven numbers, exactly" 逐字重复；两行相同的数字已经能证明这一点 | "✓ Identical" |
| l40 | P2/P6 | 建议 | "Autograd = Backpropagation" | 两位审稿人的改写要么保留 "Autograd"（与口播 "automatic differentiation" 不一致），要么删掉这个术语；"=" 也比口播的 "underneath" 说得重 | 一行 "Automatic differentiation"，下一行 "Underneath: backpropagation" |
| l35–l38 | P3 | 记录 | eyebrow "Nature" + 来源行 "Nature 323, 533–536 (1986)" + 大号 "1986" | 同一张论文卡里，期刊名和年份各出现两次 | 删掉卡片顶部的 "Nature" eyebrow |

## 驳回
- a · agenda（P1 "23 words"）：按计数规则，编号不计词，同形条目算一个块。四个条目 5+2+3+4=14 词，加 Prereqs 行 5 词，共 19 词，没有超过 22（b 的 19 词是对的）。"item 04 not previewed in l06" 和 "Prereqs" 两点可保留，但超字数不成立。
- a · l36（P1 "5 text blocks"）：来源行免计；"Forward pass →" 和 "← Backward pass" 是一行同形对照，按规则算一个块。所以 1986 / 论文标题 / 作者 / 前后向行共 4 块，没有超限。
- a · l03 "Never ends → Never finishes"：改写更长，也没比原文更顺；"Never ends" 作红色反转短语成立。
- a、b · l03 "Tried 9"（必改）：截图中 9 个被圈的表盘与计数器同时出现，"Tried 9" 是动画计数标签，不是口播外的新说法。b 的 "9 tested" 也不比原文好。
- b · l18–l21 改写（只留 "5 km · A · B" 等）：删掉了 ×2/×1/+1/×0.4/+2/+13 这些旋钮值。口播 l18 数的 "7 knobs" 和 l25 要用的 "Times 2/Times 1" 都依赖这些值，这样改理解会变差。
- b · l29–l30 改写（删掉两行数字）：两行完全相同的七个数就是 "Same seven numbers, exactly" 的证据，删掉后对照就没了。应缩短其他文字或收紧版式，不应删数字。
- b · l24–l26 "Passed back = error × knob → Error × knob"（必改）：去掉左边就不知道算的是什么，也破坏了与 l22 "Blame = error × input" 的平行结构。原文最多算建议级，可改成 "Sent back = error × knob"。
- b · l17 "Networks work the same"：4 词短标题，不是口播句子，不必改。
