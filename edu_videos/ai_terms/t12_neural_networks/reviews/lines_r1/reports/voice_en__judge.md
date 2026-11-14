# voice_en__judge 裁决（lines_r1 · English narration, native ear, blind）

核对范围：两份报告、`materials/voice_en.md`、`script.en.md`、`claims.json`（C 条 l46 / l33–l35 / l43 原文）、上一集 `t11_loss_function/script.en.md`（loss 的定义）。只读，未改被审材料。

## 裁决
- V1 1 理由：b 成立。l21 "That one weighs each bent line with its own knob" 对外行耳朵属于 clearly off（weighs 听成称重，也没说把各条线加起来）；严格项里有好几处 a bit off：冷开场 l03 前置宾语 "That, it can't learn"、l01 "learned distance and fare"（缺了「两者关系」）、章节过渡 l30 名词性从句作主语 "How we work out … is next episode's story"、l31 "So far, our units sat"（两位的复述都把时态改成了 sit / we've had）、l33 "In a worked example"；另有正文 l43 报告腔 "had a … error rate, against …"。严格项有必改，这一维只能给 1。
- V2 1 理由：严格的衔接句与收尾都有必改：l30 中途预告下一集，和 l50–l51 重复，而且是倒装的长主语；l31 时态不对；l33 用 "In a worked example" 硬插例子；收尾 l50 "which way each one turns" 听起来像旋钮自己会转，应为 which way to turn each one。a 自己把 l30、l50 标为必改却给了 2 分，自相矛盾。b 的 l05、l06 证据不成立（见驳回）。冷开场 l01–l04 加 agenda l05–l06 确实不是照念目录，这一点两人一致，也成立。
- V3 1 理由：b 成立。l21 没说明合成方式（每条线乘自己的旋钮、求和、再加一个）；l46 "cost about two percentage points" 没说是哪个指标，听众会接到 l42–l43 的五猜错误率（15.3%）上，而 claims 原文是 "a loss of about 2% for the top-1 performance"，指的是另一个指标；l12 第一次出现 "loss"，没和 l05 的 "score" 接上（t11 已定义 loss 就是 score，但本集听众只听到 score）；l34 的 "pieces" 和句末 "it" 都没有可听出的所指。a 说 l21 "That one" 有歧义，不成立：l20 句末刚说完 "one unit in the second"。
- V5 2 理由：维持 2。叙述者温和、口吻统一，长短句交替（l21 7.3s 之后接 l22 1.9s）。偏长的句子有 l27 8.1s（两个小数）、l43 8.1s、l44 8.5s，l41 一句塞了四个数字，这些都要拆开换气。两人共同漏掉的是句首 "So" 偏多：l04、l16、l35、l37、l48 五句以 So 开头，l50 句中还有一个 "so how"，节奏略单调，属小瑕疵，不降分。
- V6 2 理由：b 的 3 分不成立。b 自称所有改写都不长于原句，实际 l36 改写 8 词对原句 7 词、l45 8 对 7、l41 19 对 18，都超长；l28 改写 "right now" 有歧义，l46 改写 "raised the error rate" 会被听成 top-5 错误率，l36 改写丢了「复用」这个论点，改得比原句差。a 也只到 2：l34 改写 19 词对原句 16 词，超长；l41 判了 off 却没给改写；把 loss 换成 error 破坏了系列术语（t11 l04 已定名 "the loss"）。

## 补充问题
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l31 | V1, V2 | 必改 | So far, our units sat side by side, each adding one bend. | 章节过渡句，属严格项。"So far" 搭配一般过去时 "sat"，母语耳朵听着别扭。两位的复述都悄悄改了时态（sit / we've had），却都判 natural，是共同盲点。 | So far, we've put units side by side, each adding one bend. |
| l46 | V3 | 必改 | They also found that removing any middle layer cost about two percentage points. | 两人都没发现：原文（claims，Krizhevsky et al. §7）说的是 "about 2% for the top-1 performance"，即第一猜的准确率，不是 l42–l43 刚讲的五猜错误率。不点明指标，听众会默认是 15.3% 那个数；b 的改写 "raised the error rate" 正好会把听众带偏。 | Remove any middle layer, and its first-guess accuracy dropped about two points. |
| l32 | V3 | 建议 | Now stack them instead, so each layer folds the line it gets from the layer before. | 第一次出现 "fold"（把折线再对折），只靠耳朵缺少画面；l33 才补出 "in half"。两人都判 natural。 | Now stack them: each layer folds the line from the one before, like paper. |
| l04/l16/l35/l37/l48 | V5 | 记录 | So how… / So its line… / So ten units… / So the deeper… / So a neural network… | 五句以 So 开头，l50 句中还有一个 "so how"，因果连接词用得单调。 | 挑一两句去掉 So（如 l16 "Its line stays flat, then bends upward."；l37 "The deeper the stack, the more complex the shapes the same units can build."）。 |

## 驳回
- l06（b）："learns the bend" 呼应的是 l03–l04 的 "a pattern that bends"，属于自然的口语回扣，不是生造；b 的改写 "fits a curve" 反而引入了术语 fit，更书面。这一条不成立。
- l05（b）："toward wherever the score drops fastest" 是正常口语，"by walking downhill blindfolded" 是延续上一集的比喻，不算 off。b 的改写删掉了 "score"，而 l12、l25 要接上 loss，靠的正是这个词；"blindfolded walkers" 也更书面。这一条和改写都驳回。
- l02（b，部分）：说 "late night a little more too" clipped 不成立，这种省略是正常口语。但改成 "time of day" 可以保留，单说 "the time" 可能被听成乘车时长，冷开场应采用。
- l28（b 改写）："It gets rush-hour and late-night fares right now." 里的 "right now" 可以理解成「此刻」，有歧义，比原句差。
- l36（b 改写）："Each layer folds the previous layer's shape again." 丢了「后面的层复用前面折好的」这个论点（Montúfar 2014 "re-use pieces of computation"，是深度带来指数增益的原因），而且比原句长。
- l46（b 改写）："raised the error rate" 会被接到 l43 的 top-5 错误率上，与原文的 top-1 不符；问题本身成立，改写按补充问题表那一版。
- l33（b 改写，部分）："For example" 可以采用，但 "back on itself" 丢了 "in half"，而 l34 的翻倍逻辑要靠「对折」才说得通。建议改为 "For example, two units per layer can fold a slanted line exactly in half."
- l12 / l25 / l27（a）：把 loss 一律换成 error 不成立。loss 是系列已经定义过的术语（t11 l04 "That score is called the loss"），本集 l25 还明确说用的是 "last episode's trick"。正确的修法是在 l12 第一次出现时补一句和 score 的关联（如 b 的 "Its loss—its error score—…"，或 "its loss, that wrongness score, can't get below eleven point five"），不是换词。
- l21（a，部分）：说 "That one" 有歧义不成立，l20 句末就是 "one unit in the second"。真正的问题是 weighs 这个词以及没说求和。a 的改写同样漏了求和；可以用 "That unit scales each bent line with a knob, adds them up, plus one knob: out comes the fare."（19 词，不长于原句）。
- l34（a 改写）：19 词对原句 16 词，违反「不长于原句」。可以用 b 的版本，或 "One layer makes two straight pieces, two make four; each new layer can double that."
