# screen_en__judge（claude-opus-5-5），第 3 轮

核对依据：`materials/screen_en.md` 逐屏文字，截图 card_c_lens、card_intro、card_s6、s0_l04、s2_l08–l10、s3_l21/l25/l28–l30、s4_l32/l33/l36/l37、s5_l38/l41/l45/l46，源文件 `scenes/web/s3.html`、`s4.html`、`s5.html`。

## 裁决

- P1 3 理由：取 a。b 的唯一硬伤证据不成立：card_c_lens 截图只有「The model only sees the score」，是 6 词，正好在上限内。材料里的「7 words」是 s4 页眉「03 · The model only sees the score」把编号「03 ·」算进去了，而编号和页眉都按规则豁免。其余各屏都在硬上限内：l21 的两行「Off by …」算一个列表块，共 4 块；l29/l30 图内文字去掉编号后 9 词；l25 的 Try 1/2/3 算一个块。b 点名的 l18「They cancel out」、l35「How you score shapes learning」、l37「Loss function defines “good”」、l43「Loss keeps falling」都是 3–5 词的结论式标题，不是口播整句。这几条在第 2 轮已逐条裁定（I10/I18/I21/I23），b 这次没给新理由。
- P2 2 理由：取 a。分工整体成立：l09「Turn, then check」、l36「4 × 2² = 16」、l41「Penalty 0.11 / 2.30」都是屏幕给结构和数字、口播负责解释。剩下的是小瑕疵，算不上 1 分的问题：l35 标题与口播「The way you score it shapes how it learns」近乎同义，但上一轮裁决人已保留；l45 的 h2「Loss keeps falling」和曲线标注「Still falling ↓」同屏重复，属建议级。此外 l10「Training: push it down」在画面上紧挨 KNOB 表盘，而且这一刻旋钮读数正从 2.2 升到 2.5，「it」容易被读成旋钮，与 outro 已改成的「push loss down」也不一致。a 的条目成立，建议照改。
- P3 2 理由：章节编号 01–04、章名卡与页眉一致，层级都不超过三级。l29/l30 的「3 · 2.19」和「Lowest · 1.97」确实落在同一个可见点上：s3.html 里绿圈没有自己的点，源码注释写明「第三种的黑点留在绿圈上层」，所以 b 指出的问题存在。但口播 l28 已说「the third nearly at the bottom」，表盘读数也从 $10/$2.50 变成 $10.20/$2.54，观众能理解为「最低点就在第 3 次旁边」，不会读出矛盾。按建议级处理，不到必改，也不必删「3 · 2.19」（见驳回）。
- P5 2 理由：两人都没给准。b 打 1 分的依据是标签挂在哪个点上，这是层级问题，不是阅读时间问题；l29 停 6.5 s、l30 停 5.8 s，图内 9 词加卡片，3 词/秒以内读得完。b 还写 s5_l46 没问题，但截图里旋钮阵列最右一列只剩残边（x≈1318）。源码 `tiny("#many", 96, 16, 9.5)` 每行 16 列，放进 440px 宽的 svg 必然被裁，a 看对了。a 却仍打 3 分，同时又漏看了 l33、l37 两处标题折行后末行孤词（见补充）。有可见瑕疵，记 2 分。
- R 2 理由：第 2 轮的必改项基本都已落实：I1/I2 outro 改为「Training: push loss down」，I3「Model = machine + knobs」，I5「Lower loss = better」，I15「Lowest loss ≠ 0」，I16/I17「Taxi? No idea」，I19「Big misses cost most」，I21 改成 loss function，I25 左列加宽到 720px 后不再压旋钮。b 判「改出新问题」的 I14（7 词）数错了，不成立。但 a 打 3 分偏高，有两处遗留：I13 只把标签挪到环的另一侧，同一个点挂两个分数的观感仍在；I25 修完遮挡后，旋钮阵列右侧被裁的问题仍在。

## 补充问题

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l33 | P5, P4 | 建议 | h1「Not zero, just the / lowest」 | s4_l33 截图里标题折成两行，第二行只剩「lowest」一个词，还把「the lowest」拆开了。这和第 2 轮 I19/I24 是同一类孤词问题，两位都漏了。「just the lowest」也省掉了中心词，读起来有点悬。 | 「Lowest, not zero」（3 词，一行放得下）；或保留原文，给 `.ttl .t` 加 `text-wrap: balance` |
| l37 | P5, P3 | 建议 | h1「Loss function defines / “good”」 | s4_l37 截图里第二行只剩带引号的「“good”」。这是第 3 章的收束句，是观众停下来记的那句话，孤词看起来像排版失误，而不是有意强调。 | 文字不改，改成两行均衡：「Loss function / defines “good”」（`text-wrap: balance`，或在 defines 前手动断行） |
| l30 | P5 | 记录 | h1「Find the lowest point」 | 标题右端到 x≈1855，右边距约 65px，左边距是 120px，超出了标题安全区（约 x≤1824）。其他屏的标题都留够了右边距。 | 文字不改；这一屏的 h1 字号降一档（如 60px），或右栏左移 |

## 驳回

- c_lens / l31–l37 页眉（b，P1 必改「7 words」→「Only the score」）：不成立。章名卡实际是 6 词（见 card_c_lens），多出来的 1 词是页眉里豁免的编号「03 ·」。「Only the score」去掉了主语，第 2 轮 I14 已因此驳回过。
- l18–l19（b，必改「Error cancellation」）：第 2 轮 I10 已驳回。抽象名词比「They cancel out」难懂，也对不上画面上的「Too high +」和「Too low −」。这次没有新理由。
- l37（b，必改「Defining “good”」）：第 2 轮 I21 已因去掉主语而驳回。这一屏真正的问题是折行孤词（见补充），不是句式。
- l35–l36（b，必改「Scoring → learning / Bigger misses → bigger penalties」）：上一轮已裁定保留。改写后第二行 4 词变 5 词，也丢了「most」的比较意味，改写反而更差。原条目最多算记录级。
- l29–l30（b，必改「remove 3 · 2.19」）：删掉第 3 次尝试的标签，会切断 l28「the third nearly at the bottom」的视觉连续，第 2 轮 I13 已说明。问题本身成立，但只到建议级。更好的改法是在最低点（BEST）画一个绿色实心小点压在第 3 次的点上面，第 3 次的点在 l29 起就变灰（l30 已经是灰的）。这样绿圈有了自己的点，两个标签各挂一个点。
- l43–l45（b，必改，h2 改「Training loss」）：降为建议。h2 改成「Training loss」后，l43–l44 屏上就没有趋势信息了。改曲线标注更好：「Still falling ↓」改为「No floor yet ↓」，对应口播「no sign yet of a floor」，既保留定位作用，又不再重复 h2。
- l08（b，建议「Golf: fewer strokes」）：第 2 轮 I6 已裁定「fewest strokes wins」是惯用说法。改写会拆掉它与「Lower loss = better」的并列结构，读起来也不如原文自然。
- s5_l46（b，P5 证据「keeps … clear of the illustration」当作已无问题）：遮挡确实修好了，但阵列右侧被裁，b 漏看了。以 a 的记录为准。
