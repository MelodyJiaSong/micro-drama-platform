# screen_en__judge 裁决（第 1 轮，claude-opus-5-5，母语英语读屏标准）

核对基准：两位审稿时用的 `materials/screen_en.md` 与 `materials/screen/en/`（13:19）都早于作者后来的版面修订。我以当前源文件 `scenes/web/*.html`（`data-en`；s0/s3/s5/s8/s9 和 `script.en.md` 在 19:26 又改了一次，作者仍在编辑）、`package.json`（13:25）和 `renders/_shots/en/`（13:26）为准。两人引用的 l35、l37、l42、l49、l50 证据在当前版里都已失效。截图与源文件仍有一处不一致：l49 截图是 "First ask: what data?"，源文件已改成 "First check: what data?"，需要重出截图。片尾卡（card_s10）和片头卡没有当前截图，只按 `package.json` 文字核对。

## 裁决
- P3 2 理由：b 的证据（l37 右侧五块 37 词、l49 三张卡同时保留细节）在当前版已不成立。当前 s7.html 到 l37 时右侧只剩一行 "“Today's AI” = machine learning"（截图 s7_l37 印证），l35 也只剩 "Deep learning: layered neural networks" 一行。s9.html 在 l47/l48 用 EDU.out 清掉前一张卡的正文，l49 截图只剩三张卡标题和 "First ask: what data?"。a 引用的 l35/l37 四层文字同样已失效，只有 l15 的 "= the model" 等号碎片仍在。另有几处小瑕疵（见补充问题）："Pattern"（s3 l10）与 "patterns"（s0 l02）单复数不一；眉题编号不统一（s3 无眉题，s4 "An analogy"、s7 "Circles within circles" 不带章号）；l07 "So is an 8" 折成两行；l25 的 97% 标注紧贴右栏。层级总体清楚，判 2。
- P4 2 理由：b 列的三条证据只剩一条成立。l42 已改为 "Bias in, bias out"，l50 已改为 "Has it seen this before?"，所以 "unclear it" 和 "learned this kind of question" 两条都已失效。仍成立的是片头标题 `package.json` "What Is AI?" 用了 title case，与全片 sentence case 不一致。a 指出的 "Rules · written by people""Pattern · learned" 这类点号标签已删除。新版仍有小瑕疵："Called machine learning"（l10 h1）读起来像缺了主语的残句；l07 "mistakes others" 指代偏虚。两处都不是严格项，片尾 "Not rules people write / Patterns learned from examples" 平行自然。判 2。
- P6 2 理由：两人每条问题都给了改写，a 的多条已被作者采纳（"Your phone spots your cat""Bias in, bias out""Has it seen this before?""Learned, or just memorized?"），但 b 给 3 分偏高。b 有几条改写本身就是 P4 明令必改的生硬名词堆叠，比原文更差：l01 "Cat recognition"、l27 "Future forecasts ≠ answer predictions"、l44 "Unseen inputs, forced answers"、l12 "Assumption: hand-coded abilities"。l09–l10 "3 / 7 / 3 / 7" 和 l28/l45 "3 / Other digits" 两条是改图表设计，依据的计数前提也不成立（见驳回）。a 的 intro 一条只写 "Check separately"，没有给改写。两人都漏了下面的补充问题，因此判 2。

## 补充问题
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| s0_l02 | P3, P4 | 必改 | "Many examples →" ＋ 药丸 "patterns"（截图中折到下一行，小写开头独占一行） | 冷开场属严格项。小写 "patterns" 孤零零换行，读起来像断掉的半句；它和 s3 的 "Pattern" 是同一概念，单复数却不一致 | 一行放下："Many examples → patterns"（缩小字号或 nowrap），或改成 "Examples → patterns" |
| s3_l10 | P4 | 建议 | h1 "Called machine learning" | 76px 主标题以过去分词开头，是缺主语的残句，母语读者会停顿一下 | "This is machine learning"（4 词，呼应 s0 的 "That's today's AI"）或 "= machine learning" |
| s3_l10 | P3 | 建议 | 流程药丸 "Pattern" | 与口播 "finds the patterns" 和 s0 的 "patterns" 单复数不一致 | "Patterns" |
| s2_l06–l07 | P3 | 建议 | "So is an 8"（截图折成 "So is / an 8" 两行），下一行 "So is a 5" 却是一行 | 两条平行反例排版不一致，第一条被拆成两行，读起来断开 | 给标签加 nowrap，或缩成 "Also an 8" / "Also a 5" |
| s2_l07 | P4 | 建议 | "Misses some, / mistakes others" | "some""others" 都没说清是什么，"mistakes others" 也可能被理解成认错别的东西；它本应收住前面两条规则 | "Misses some 3s, / mislabels others"（5 词） |
| s3 / s4 / s7 眉题 | P3 | 建议 | s3 无眉题；s4 "An analogy"；s7 "Circles within circles" | 其他场景眉题都是 "0N · 章名"，这三处不带章号，s7 看上去像一个没编号的新章，和 01–05 的章节编号体系不一致 | 统一为章内小节样式，如 "01 · An analogy""03 · Circles within circles"；或眉题只放章名、小节名降为 caption |
| s5_l25 | P3 | 建议 | 图表标注 "97%" 与右栏 "Only told: which are 3s" | 截图中 97% 的右缘与右栏文字只隔约 15px，像一行连读："97% Only told…"，层级混淆 | 右栏下移到 97% 以下（top ≥ 520px），或把 97% 标注改成居中放在点上方偏左 |
| s9_l49 | P3 | 记录 | 截图 "First ask: what data?"，源文件 "First check: what data?" | 截图滞后于源文件；口播现为 "first find out what data it learned from"，用 "check" 更贴近 | 重出 renders/_shots/en/ 后再核 |
| intro（片头标题卡） | P4 | 建议 | "What Is AI?" | b 已指出，这里补定级别：片头卡不在严格项清单内，YouTube 标题习惯用 title case 也说得通，但它和全片 sentence case 不一致 | "What is AI?" |

## 驳回
- b l28、b l45–l49（"Ten category labels 0–9 … 10-word chart block >9"）：柱状图下面的 0–9 是分类轴的刻度标签，作用等同于 axis tick（截图 s6_l28、s9_l46 都是轴下单个数字），不该按图内文字计数。改成 "3 / Other digits" 会抹掉"只能在十个数字里挑"这个画面证据，这正是 l45 口播要说明的点，改写更差。
- b l09–l10（"Each card row contains 10 items, exceeding the six-item grouping"）：每张样本图下的数字是答案标注，属于编号性质，不计词；数字墙表现的是"成百上千张带答案的例子"，压成 "3 / 7 / 3 / 7" 四张就失去了这层意思，改写更差。
- b l01 改写 "Cat recognition"：名词堆叠，丢掉了冷开场的钩子；P4 明说生硬名词堆叠必改。现版 "Your phone / spots your cat"（5 词）已经合规。
- b l27 改写 "Future forecasts ≠ answer predictions"、b l44 改写 "Unseen inputs, forced answers"、b l12 改写 "Assumption: hand-coded abilities"：都是生硬名词堆叠，念出来不顺，比原文和现版（"Guesses answers, not the future""It answers anyway""Programmers typed it all in"）都差。
- b P4 证据中的 l42 "unclear it" 和 l50 "learned this kind of question"：当前源文件已改为 "Bias in, bias out" 和 "Has it seen this before?"，问题已不存在（只是失效，原判断当时成立）。
- a s5_l20 改写 "Unseen test = real learning"：语义错误，没见过的考题是检验是否学会的手段，本身不等于学会；a 同行给的备选 "Learned, or just memorized?" 才对，现版也已采用这一句。
