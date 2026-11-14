# screen_en__judge 裁决（第 1 轮）

核对依据：`materials/screen_en.md`、截图 s0_l04 / s2_l12 / s3_l22 / s3_l24 / s3_l25 / s4_l28 / s4_l29 / s5_l37 / s5_l38 / s5_l39，场景源 `scenes/web/s3.html`、`s4.html`、`s5.html`，包装文字 `package.json`。

## 裁决
- P1 1 理由：l38 的 18 个数字超过「同类条目最多 6 项」的合并上限，不能按一块计。该块 18 词超过 9 词，整屏 23 词超过 22 词，硬上限被突破，必须判 1。a 已把它列为必改，却给了 2 分，前后矛盾。outro 属严格项：package.json quote 为两行 "Parameters are knobs" / "learning sets them right"，是一句话拆成两行，不是提纲，也应判必改。l29 按规则算 4 块 21 词，未超限，只是偏满。
- P2 1 理由：截图 s3_l22 中，表盘已是 $10.20 / $2.54，线也贴近点，但标题仍是 "Overshot: too high"，口播说 "Turn it back a little"，屏幕与口播矛盾，必改，b 站得住。a 说 l24 提前给出答案，不成立：s3_l24 截图只显示 "8 km → ?"，$30.50 到 l25 才出现。
- P3 1 理由：截图 s4_l28 显示 "The knob settingsChanged"，s5_l37 显示 "The settingsLearned from examples"。标签和取值之间没有间隔，同/变、人定/学来的对比结构被破坏，b 的证据成立。核心定义在多屏之间说法也不统一，见补充问题。a 认为四个章节标题形式不一致，理由不足，见驳回。
- P4 1 理由：l20 "Farther, further off" 读起来像笔误，native 观众会皱眉，两人都认为别扭，a 甚至列为必改。outro（严格项）第二行小写开头的 "learning sets them right" 是半句话；"set (something) right" 惯用义是「纠正」，与「拧到对的位置」有偏差，严格项按必改处理。a 把问题列成必改，分数却给 2，不能维持。
- P6 2 理由：两人每条都给了改写，但有几条改写建立在错误证据上：a 的 l24 和 l28/l37「16px」、b 的 l39 和 l04。有些改写反而更差：b 在 l10 把 "per km" 改成 "rate"，与表盘标签 "Per km" 不一致；b 在 l31 用 "Trained = tuned" 丢了「位置对」的意思；a 在 l16 写 "Guesses form a line"，变成了整句。两人还共同漏掉了核心定义跨屏不一致这一条。

## 补充问题
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l13 / l30 / l31 / outro | P3/P4 | 必改（outro 为严格项） | "Learning = setting the knobs" / "Training = turning knobs" / "Learned = set right" / "learning sets them right" | 本期的核心结论在四处用了四种说法：learning/training/learned 混用，setting/turning/set right/sets them right 混用。观众难以把它们认作同一个定义，结尾也没有回扣 l13。 | 统一成两个固定句式：l13 "Learning = setting the knobs right"；l30 "Training = turning knobs"；l31 "Learned = knobs set right"；outro "Parameters = knobs" / "Learning = setting them right" |
| l12 vs l37 | P3 | 建议 | l12 "The math by people / Settings from examples"；l37 "The math / People decide · The settings / Learned from examples" | 同一组对比在第 1 章和第 4 章措辞不同；l37 的作用是回扣 l12，措辞不同就回扣不上。 | 两处统一为 "Math: set by people" / "Settings: learned from examples"，l37 沿用 l12 的版式 |
| l28 / l37 | P3/P5 | 必改 | `.rows .row` 采用 grid `1fr auto`，en 版标签加取值超出行宽 | 根因在版式：en 文本比 zh 长，`1fr` 被挤到 0，标签和取值之间没有间隔。只改文字可能在其他行复发。 | 文字改短（"Machine: same" / "Settings: changed"），同时给 row 加 `column-gap` |

## 驳回
- a · l24「8 km → ?$30.50」：s3_l24 截图只有 "8 km → ?"，答案在 l25 才替换出现。"?$30.50" 是 DOM 抽取把隐藏元素拼在一起造成的，不是屏幕内容。「提前剧透」和「格式错误」两条都不成立。
- a · l28 / l37「16px 读不清」：截图中这些行实际约 54px（h2）。16px 是缩放动画中途的 computed 值，可读性问题不成立；只有黏连问题成立。
- a · 四个章节标题必改：严格项要求读来自然。"What a model looks like" / "Let's turn the knobs" / "Where the learning lives" / "Billions of knobs" 都是自然的口语标题，YouTube 章节混用不同形式很常见。a 的改写 "Where learning is stored" 和 "A model, up close" 反而更生硬。
- a · outro「run-on, no break」与 b · outro「missing separation」：package.json 的 quote 本来就分成两行，没有缺分隔。问题实质在于半句拆行和措辞，按 P4 / 补充问题处理。
- b · l39「100Bparameters 丢空格」：s5_l39 截图显示 "100B parameters = 100B knobs"，空格正常，不成立。
- b · l04「Inside a model 卡片遮住 A model」：s0_l04 截图中 "A model" 完整，离卡片左缘约 50px，没有遮挡，最多算偏挤。改成 "Model" 会丢掉冠词，读起来更差。
- b · l32 必改：l32 是章内第一屏，不是过渡句。"Chatting takes far more knobs" 只有 5 词，标题式可接受；改写 "More knobs for conversation" 并不更好。
- b · l10「Fare = base + rate × distance」：表盘标签全程是 "Per km"，公式改成 "rate" 会造成术语不一致，比原文差。
- b · l31「Trained = tuned」：丢掉了「拧到对的位置」这层意思，且与 l13 的定义脱节，比原文差。
- a · l16「Guesses form a line」：把等式标签改成了完整句子，违背提纲原则。
- a · l34 删除 "= 175 billion knobs"：这是把参数数换算成旋钮的关键一步，属于数字加标签，符合提纲要求，应保留。
