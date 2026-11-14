# screen_en__judge 裁决（第 3 轮 · claude-opus-5-5）

## 裁决
- P2 1 理由：b 的理由不成立。两条灰色引语和正式目标并排，是「原话 → 正式写法」的对照结构，r2 裁决（I3/I4）已定稿保留，作者照办。但两人都漏了一个严格项问题：l02 引号里写的是 “Never cross it”，口播 l02 和讲稿原话是 “never cross this line”。引号意味着逐字引用，屏幕却和观众同时听到的话对不上，而且 “it” 在左列没有指代对象（`scenes/web/s0.html:14`）。冷开场是严格项，有一点不对就要改，所以记 1 分，见补充问题和必改定稿。a 指的 l27「公式＋文字关系」并列，r2 已作为分工不同处理，不再计。
- P4 2 理由：采 a 的 2 分。l13 “Rule: stay in the fence” 不算严格项（既不是冷开场、衔接句、片尾，也不是章节标题），意思也听得懂。r2 裁决 I13 已把级别降为建议，b 再报必改不成立。l04 “Make it the best” 中 “it” 指代不清，l07 “at / most” 折行，都是建议级。章节标题 “What is a Lagrange multiplier?” / “A small experiment” / “Lambda as a price” / “How AI uses it” 和片尾 “In short / Price the rule just right” 读出来都自然，没有必改。
- R 1 理由：采 b 的 1 分，但不采纳 b 判 I3 未解决的理由（灰色引语保留是 r2 裁决的定稿）。I7/I8（l04）、I11（l07）、I13（l13）三条标了「不改」，理由栏抄的却是 r2 裁决人赞成改写的原话：I11 原话是“定稿改用 Max 1 hour a day”，I13 原话是“改写可以采纳”，I7 原话是“如果要改，用 As good as possible”。这些都不是反驳理由。截图 s2_l07 的 “most” 仍单独成行，s3_l13 仍是 “stay in the fence”。a 也承认 I11 未解决，却给了 2 分，偏宽。上一轮的必改项 I1、I3/I4、I5/I6 确实都已解决。
- P6 2 理由：两人每条问题都给了改写，但有两条改写不能用。a 给 l27 的 “Extra height ≈ 3 × radius gain” 把口播 l26 的 “extra radius” 改成 “radius gain”，前后半句不再平行。按截图量，“3 × extra radius” 在 56px 下约宽 460px，整句约 870px，从 x=960 起排会超过右边距，说“一行放得下”不成立。b 给冷开场的“删掉两条灰色引语”与 r2 定稿冲突。两人还都漏了 l02 引语与口播不一致这一条，自然也没有给改写。
- P3 2 理由：章节卡和页眉现在一一对应（c_problem 与 l04–l10，c_experiment 与 l11–l23 等），这一点两人都说得对。但两人共同漏了两处。一是 l33：目标行写成 “Harm ≤ the line · Most helpful”，顺序和冷开场 l01 的 “Most helpful / Harm ≤ the line” 相反；而且红色的 “Harm” 正落在绿色「How helpful」卡片下方，绿色的 “Most helpful” 落在红色「How harmful」卡片下方，颜色对应交叉。二是 l30：用的是 “Costly constraint”，而 l24 的标题、口播 l24/l29/l30 都说 “rule”，同一章里术语换了。

## 补充问题
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l02–l03（冷开场，`scenes/web/s0.html:14`） | P2, P4 | 必改 | “Never cross it” | 严格项。灰色引语带引号，按逐字引用来读，但口播 l02（字幕同时出现在画面下方）说的是 “never cross this line”。另一条 “Do your best” 是逐字的，这条不是，两条之间也不一致。“it” 在左列没有先行词，只能借右列的 “the line” 去理解。这句在 l03 淡化后还留在画面上。 | **“Never cross this line”**（与口播逐字一致）。左列英文宽度从 470px 放宽到约 600px，避免 nowrap 文字压到右列；右列整体右移约 130px，“Harm ≤ the line” 结束在 x≈1640，仍在边距内 |
| l33（`scenes/web/s5.html:32`） | P3 | 建议 | Harm ≤ the line · Most helpful | 顺序和冷开场 l01–l02 相反，削弱首尾呼应。上方卡片是绿色「How helpful」在左、红色「How harmful」在右，下面目标行却是红在左、绿在右，颜色对应交叉。截图里的 “·” 在 76px 下显示成一个粗黑方块。 | **Most helpful · Harm ≤ the line**（长度不变，颜色与卡片同侧，和冷开场同序） |
| l30（`scenes/web/s4.html:50`） | P2, P3 | 建议 | High λ → Costly constraint | 本章 l24 标题是 “How costly is the rule?”，口播 l24/l29/l30 也都说 “rule”。这里突然换成 “constraint”，又和下一行 “No cost” 长短不齐。 | **High λ → Costly rule** |

## 驳回
- b · l02–l03 必改（删除两条灰色引语）：r2 裁决 I3/I4 已定稿，引语和正式目标并列是对照结构，不算重复，作者按定稿保留。本轮真正的问题是引语措辞和口播对不上，不是引语该不该存在，已在补充问题里改判。
- b · l13 级别「必改」：l13 不是严格项，意思也听得懂，r2 裁决已降为建议，本轮维持建议。改写 **Rule: inside the fence** 本身可以采纳：比原文短，60px 下一行放得下。
- b · l04 改写「Best possible result」：引入了口播里没有的 “result”。r2 裁决给过更贴近口播 l04 “as good as possible” 的写法 **As good as possible**，以那条为准。
- a · l27 改写「Extra height ≈ 3 × radius gain」：把 “extra radius” 改成 “radius gain”，打破了 extra … / extra … 的平行，和口播 l26 也对不上；整句在 56px 下一行放不下（估约 870px，从 x=960 起排）。原写法用 `<br>` 主动断行，可以保留。
- a · R 2 分：a 自己列出 I11 未解决、I13 未采纳，但没有核对作者的「不改」理由其实是裁决人赞成改写的原话，打分偏宽。

## 必改定稿
| 位置 | 原文 | 定稿 | 说明 |
|---|---|---|---|
| l02–l03 冷开场灰色引语（`scenes/web/s0.html:14` 的 `#kb`） | “Never cross it” | **“Never cross this line”** | 与口播 l02 逐字一致。同时把 `html[lang=en] .hook .k { width: 470px; }` 改为 `width: 600px;`，避免压到右列。“Do your best”、“Most helpful”、“Harm ≤ the line” 三处不动 |
