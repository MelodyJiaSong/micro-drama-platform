# voice_en__judge（第 3 轮裁决，claude-opus-5-5）

核对依据：`materials/voice_en.md`、`script.en.md`（v1.2）、`timeline.en.json`（`"estimated": true`，l33 = 11.335–15.565，l34 = 15.915–17.454）、`audio/en/` 为空（英文尚未配音）、`previous.md` 中 I43–I57 的作者处理与上一轮裁决。

## 裁决
- V3 2 理由：b 判 1 的两条依据都站不住。一是 l33 4.2s、l34 1.5s，这是估算时间轴把「a hundred and seventy-five billion」「G P T three」合并成数字记号计数造成的（timeline.en.json `estimated: true`，audio/en 为空）。上一轮 I52–I54 已裁定为工具估算问题，降为记录，配音后用 qa 实测复核；措辞本身一遍能听清，b 自己也承认措辞自然。二是 l29「hand it to a friend」，上一轮 I50 已判不采纳：l10 讲过算法，l12 说过「People decide how the machine does its math」，l28 又说「The machine itself hasn't changed」，机器是固定的，听得出来。剩下的小瑕疵是 l44「loss functions」没有解释就收尾，只是预告，扣到 2 分。
- V5 2 理由：b 判 1 的依据只有 l33/l34 的估算时长，同上，不算文字缺陷。全片同一个口吻，长短句交替（l07「Those knobs are the parameters.」1.9s 紧挨 l08、l09 的长句）。a 说 l21 一口气说不完不成立：l21 是两句，在「steeper.」处自然换气。保留 2 分是因为真实配音还没出来，l33/l34 的实际节奏没法确认；配音后如果语速超过约 4.5 音节/秒，要按 qa 结果重开。
- R 2 理由：I43、I44、I46、I48、I49、I51、I57 都已解决（l10 先乘后加，l14 已缩短，l22「nudge … up」，l28「Only the knob settings have」，l43「They're the clue」）。I47、I50、I56 的不采纳理由成立，见上一轮裁决。I52–I55 按裁定延到配音后实测，不算未解决。a 给 3 分偏宽：I45/I46 改成了 l16「they form a straight line, a fare for every distance」，尾巴挂着一个名词短语，本轮两位都判 a bit off，属于改出的小问题，所以给 2 不给 3。b 给 1 分偏严，它算作未解决的 I50、I52–I55 都已有裁定。
- V1 2 理由：同意两位。除 l16 的名词短语尾巴外，大部分是口语（l12「But where each knob is set? Nobody types that in.」，l35「no eating, no sleeping」）。两人都漏的一个小点：l22「ten dollars twenty」和 l25「thirty dollars fifty」是英澳说法，美国观众更常说「ten twenty」「thirty fifty」。不影响听懂，记一笔（见补充问题），不扣分。
- V2 3 理由：严格项逐条复核。冷开场 l01–l04 是「新闻 → 提问 → 上回 → 打开看看」一条思路，没有目录腔。章节卡「What a model looks like / Let's turn the knobs / What it learned / Billions of knobs」用词地道；每章开头那句 l05、l14、l26、l32 都接得上卡片。片尾 l40–l44 回顾、提问、回扣竖线、预告，衔接顺。l02 和 l04 都以「So」开头，属正常口语，严格标准下也不算 a bit off。没有共同漏掉的必改项。

## 补充问题
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l33 / l34 | V3, V5 | 记录 | In twenty twenty, OpenAI released G P T three, which has a hundred and seventy-five billion parameters. / That's a hundred and seventy-five billion knobs. | 文字不改。英文配音出来后重跑 timeline，用 qa 实测这两句的语速（估算约 7.4 和 8 音节/秒，是计数误差）。实测仍偏快，就延长分配给 l33/l34 的时长，s5 的计数动画跟着走，不动台词。 | （文字不改；配音后实测复核） |
| l22 / l25 | V1 | 记录 | …nudge the base fare up to ten dollars twenty. / …about thirty dollars fifty. | 「ten dollars twenty」是英澳口语，美国观众一般说「ten twenty」。能听懂，不是缺陷；如果以美式配音为准，可以顺手改。 | …nudge the base fare up to ten twenty. / …about thirty fifty. |

## 驳回
- l33 / l34（b，必改，「Allow roughly three seconds / seven to eight seconds」）：时长来自估算时间轴，不是台词或配音的缺陷，上一轮 I52–I55 已裁定降为记录，等配音后实测。本轮没有新证据，维持原裁定，不升必改。
- l29（b，建议，「Give a friend the same machine and those two numbers…」）：上一轮 I50 已判不采纳。l10、l12、l28 已经交代机器固定不变，改写还丢了「scrap of paper」这个画面。
- l17（b，建议，「The gap between each dot and the model's line…」）：改写把「little vertical line」换成「gap」，会打断 l23「all those little vertical lines are short」和片尾 l43「Remember those little vertical lines」的回扣，比原文差。原文「that line」紧接 l16 的 straight line，听一遍能对上（同上一轮 I47）。
- l44（a，建议，「That's next time: how we score a guess. It's called a loss function.」）：改写 12 个词，原文 9 个，违反 V6「不长于原句」；而且把下一集的内容提前讲了。预告里点一个术语名是常见做法，保留原句。
- l34（a，存疑改写「That's that many knobs.」）：「that's that many」念起来别扭，也丢了把「parameters」换成「knobs」时重复关键数字这一步。原句保留。
- l21（a，V5「a bit long for one breath」）：l21 是两句，在「steeper.」处换气，不构成问题。
