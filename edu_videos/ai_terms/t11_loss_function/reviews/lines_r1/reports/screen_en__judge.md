# screen_en__judge（claude-opus-5-5），round 1

## 裁决
- P1 1 理由：b 站得住。l01 冷开场 h1「A model is a machine with knobs」7 词，超过标题 ≤6 的上限，而且是口播原句（冷开场属严格项）；a 写「titles all ≤6 words」时漏了这一屏。l19 按 round-2 口径数：旋钮对（1）+ 图表（1）+ h1「Try 2: too steep」+ −0.33 分数卡 + h2「✗ They cancel out」= 5 块，超过 ≤4 块；a 说它「sits at the block ceiling」，数错了。l15 图表内文字 Fare ($)/km/Actual $23/Off by $8/Guess $15/8² = 64 共 11 词，超过单块 ≤9 词。三处都是硬上限违规，只能给 1。
- P3 2 理由：取 a。b 拿来扣 P3 的唯一证据是 l19 的 5 块，这是 P1 的块数硬上限，上面已经扣过；它本身也没说明层级哪里错了。从截图核：章节编号 01–04 的眉标和四张章节卡一致；各屏最多三级（标题、要点、注）。小瑕疵如 a 所列：l41 引句「Twinkle, twinkle, little star」96px 压过底部 76px 的结论 h1「Less sure, bigger penalty」；l25 h1「Try 3」和表格行「Try 3 2.19」重复。这些够不上 1 分。
- P5 2 理由：b 的 2 分站得住，a 的 3 分偏高。原因一：l14–l15 橙色线直接穿过「Off by $8」的 by 和 $8 之间（s3_l15.png 可见）。原因二：两人都漏了几处遮挡和渲染问题（见补充问题）：l06–l08 的「→」被 SVG 裁掉，只剩灰色短横，读起来像减号；l29–l30 第 3 次的黑点被绿色「Lowest point」圆点盖住；l15 灰色数据点压在「64」的 4 上。阅读时长方面，l41 16 词 7.7 s、l36 21 词 6.2 s 都在 ~3 词/秒以内，没问题。
- P6 2 理由：两人确实每条都给了改写，但有几条改写比原文差：b 的 l33「Lowest possible loss」、l34「Score only」、l35「Squared penalties」、l19「Try 2: cancellation」，a 的 c_lens「All the model sees」和 l34 的备选「Knows no taxis」，都丢了原句要传达的对比或结论（理由见「驳回」）。另外，补充问题里的遮挡与裁切两人都没给修法，所以不到 3。

## 补充问题

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l06–l08 | P5 | 建议 | 误差柱与「LOSS 17.9」卡之间的「→」（s2.html：`text("→")` x=470，SVG 宽 500，76px） | 箭头字形被 SVG 右边界裁掉，截图里只剩一段灰短横，看上去是「−」。紧挨着有正有负的误差柱，容易被读成「误差减 17.9」，抵消了 l06 h1「Errors → one score」的意思。 | 把 #pile 的宽度加到 ≥560，或者把箭头左移到 x≈440；也可以改用带箭头头部的 SVG path。 |
| l29–l30 | P5 | 建议 | 绿色「Lowest point」圆点与「3 · 2.19」 | 最低点（10.20, 2.54）和第 3 次（10, 2.50）几乎重合，绿点完全盖住了第 3 次的黑点；同时三个尝试标签淡成低对比的灰色、压在陶土底色上。观众本该看出「第 3 次已经接近谷底」，现在只剩一个绿点。 | 第 3 次黑点保留白描边并放在绿点上层，或者在绿点外画一圈环；尝试标签保持 l28 的深色描边样式，不要淡化。 |
| l15 | P5 | 记录 | 「8² = 64」 | 4 km 处的灰色数据点压在「64」末位上，红色方块的左上角也贴着文字。 | 把「8² = 64」移到方块上方（y≈540，与「Actual $23」错开），或者往左挪 30px，让开数据点。 |
| l08、l45 | P5 | 记录 | 「Golf: fewer strokes / win」；「Training loss keeps / falling」 | 两处 h2 折行后，末行只剩一个词（孤词），读起来卡一下。 | l08 改为「Golf: fewer strokes wins」并把卡片加宽到一行放下，或者改成「Golf: fewest strokes win」；l45 采用 b 的「Training loss ↓」，一行即可。 |
| l18–l19 | P1 | 建议 | h1「Try 2: too steep」+ h2「✗ They cancel out」 | 5 块超限，需要一个不丢意思的修法（b 的方案会丢掉 too steep）。 | 从 l18 起把 h1 换成「No squaring: they cancel」，删掉 h2「✗ They cancel out」，保留 −0.33 卡。这样共 4 块：图表、旋钮、h1、分数卡。 |
| l15 | P1 | 建议 | 「Off by $8」 | b 建议出公式时删掉它，但这样「8」的来历就断了。 | 改成「$8」贴在红色竖线旁（1 词），图表总数降为 9 词，「8² = 64」的来源仍然看得到。 |

## 驳回
- c_lens（a）：改写「All the model sees」去掉了关键词「score」，章节卡上只剩「模型看到的全部」，宾语没了，比原文更费解。原题「The score is all it sees」6 词，未超限。若要改，用「It only sees the score」（5 词）。
- l34（a，备选「Knows no taxis」）：不是自然英语，母语者读来别扭，比原文差。主改写「No idea what a taxi is」可以留。
- l19（a，级别）：口播「about −$0.30」与屏幕「−0.33」是近似取整，「about」已经交代了，不算「与口播矛盾」。级别降为建议；补上「$」或改成「−$0.33」即可。
- l19（b，改写）：「Try 2: cancellation」丢了「too steep」（这正是线一端偏低、一端偏高的原因），而且把结论变成了一个抽象名词。改用上表「No squaring: they cancel」的方案。
- l33（b）：「Lowest possible loss」丢掉了这句要的「不是 0」对比（承接 l31「Lowest ≠ 0」、口播「isn't chasing zero」）。原文只是略显生硬，不到必改；若要顺，改成「Not zero, just the lowest」（5 词）。
- l34（b）：「Score only」太省，丢了「它不知道出租车是什么」这层对比，而这正是本章要点。改用「Sees only the score」，第二行用 a 的「No idea what a taxi is」或直接删掉。
- l35–l36（b）：「Squared penalties」只是标签，丢掉了「大错罚得狠」这个结论，而 l36 的图正是在证明这个结论。若嫌「hates」拟人化，改成「Squaring punishes big misses」（4 词）。
