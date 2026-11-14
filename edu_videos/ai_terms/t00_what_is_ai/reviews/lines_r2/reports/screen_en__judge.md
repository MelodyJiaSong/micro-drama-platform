# screen_en__judge — English on-screen text（第 2 轮裁决，claude-opus-5-5）

核对范围：a/b 两份报告、`materials/screen_en.md`、52 张截图中的关键屏（intro、s0_l01–l02、s2_l05/l07、s3_l10/l12、s5_l21/l23/l25/l26、s6_l27/l28/l31、s7_l34/l36、s8_l38/l41、s9_l46–l48、card_s10）、`scenes/web/*.html` 的 data-en 源文本，以及 `previous.md` 本项条目（含第 1 轮裁决 I20 对数字标签的驳回）。

计数口径（沿用第 1 轮裁决 I20，并与 2026-11-09 计数规则「numbering doesn't count」一致）：样本图下的 0–9 答案标注、l22/l23 的 0–9 数字芯片都按编号或刻度处理，不计词也不计块。方法注 "Median of 20 draws · each gridline ×10" 不属于豁免的 source line，要计入字数。

## 裁决

- P1 1 理由：有两处硬上限确实超了，两人都核实到了。l21 data-en 为 "With just 10 examples,<br>how many right?"，7 词，超过标题上限 6 词；l25 侧栏 5+7、图内 8、方法注 7，共 27 词，超过 22 词上限。a 已在问题表把这两处列为「必改」，评分却给 2，前后不一致。b 给的 l10「27 词」和 l23「26 词」是把数字标注算了进去，违背第 1 轮裁决 I20，不采纳；按本口径，l23 实际只有 16 词。l01 的两个 5 词短句是标题式提纲，不算 prose。
- P2 1 理由：严格项 outro 把口播 l51 的 "Most of today's AI isn't built on rules…" 压成了 "Not rules people write"，丢掉 "most"，屏幕说法比口播更绝对，等于在严格项上多出一个口播没有的断言（只有 b 抓到）。l02 "That's today's AI"、l42 "The tool was scrapped" 几乎逐字重复口播，l10 "That's machine learning" 也接近重复。a 给 2 时漏了 outro 这条。
- P3 1 理由：l33–l37 的眉题是 "03 · Circles within circles"，而章卡和 l27–l32 的眉题都是 "03 · A different lens"，章内改名却没有章卡；s3（l08–l12）全段没有眉题（I5 仍未解决）；l27 章节开场大标题折行成 "Today's AI: a / prediction machine"，"a" 单独挂在行尾；l06 "Also / an 8" 仍折成两行。以上证据都来自 a。b 给 1 的理由是「十项一行超过分组上限」，按 I20 不成立，但材料本身确实有问题，维持 1 分。
- P4 1 理由：直撇号和弯撇号混用，源文件 s0 用 `That&#39;s today&#39;s AI`，s6 用 `Today&#39;s AI`，s3 用 `That&#39;s machine learning`，而 s8 用 "men’s"/"women’s"，s7 l37 同一行里是弯引号配直撇号，其中 l02 属于严格项；outro 眉题 "IN ONE SENTENCE" 下面是两个片段；l31 "How chatbot LLMs reply" 是生硬的名词堆叠，读出来别扭，按 P4 属必改；l25 "Only told: which are 3s" 是半句。a 自己列了 3 条 P4「必改」，评分仍给 2，不成立。b 的 intro "What Is AI?" 一条不作扣分依据（见驳回）。
- P5 2 理由：按每拍新增阅读量算，a 的分析站得住。l25 时 37%、88%、97% 和图注从 l23/l24 起就在屏上，l25 新增只有侧栏 12 词，7.8 秒约 1.5 词/秒；l26 约 13 词 4.6 秒，l22 3 词加芯片 3.9 秒，都能读完。b 用「27 词 / 7.8 秒」计算，把早已读过的图表文字又算了一遍，夸大了负担。小瑕疵：l17、l23–l25、l38–l41 底部 22px 注释离字幕带近，手机上偏小，截图没有字幕，没法核实是否重叠。
- P6 2 理由：两人都给了逐条改写，但都有改得更差的条目。b 的 "Your cat, found"（l01）丢了主语和钩子，"Also 8 / Also 5"（l06）不合英语语法，"Missing digits: 0, 4, 7, 8"（l22–l23）把可视化换成了文字；a 的 "It predicts, not proves" 不地道，"It mirrors its data"（l48）删掉了口播明说的 design/training，l25 "More examples, better scores" 丢了 "In this experiment" 的范围限定。b 给 3 不成立。
- R 1 理由：I35/I36 的 l21 仍是 7 词，作者以 within limits 为由不采纳，这个理由不成立，必改项未解决；I5 s3 仍无眉题；I16 l06 仍折行；I39/I40 改出新问题（屏上没有画格线，却写 "each gridline ×10"）；I1/I84 outro 改出新问题（"IN ONE SENTENCE" 和丢失的 "most"）；I45/I46 l27 改出新问题（孤立的 "a"）。b 复核时说 I20/I21「未解决」、I3/I6 应改，这两点不成立（见驳回）。

## 补充问题

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l22–l23（s5） | P4, P2 | 建议 | "Grey = never drawn" | 这一集讲的就是手写数字，"drawn" 很容易被读成「没人手写过」，而不是「没被随机抽到」。口播用的是 "don't show up"，两人都没提这个歧义。 | "Grey = not picked" 或 "Grey = missing" |
| l10（s3） | P4 | 必改 | "That's machine learning"（源文件写作 `That&#39;s`） | a 的撇号清单列了 l02、l27、l28、l37，漏掉 l10。这是第 01 章收尾的点题大标题，和 s8 的弯撇号不一致。 | "That’s machine learning" |
| l33–l34（s7） | P3, P4 | 建议 | "Outermost: AI (artificial intelligence)"，圆内另有标签 "AI" | "Outermost:" 是图表术语式的半句，AI 在同一屏上标了两遍。两人都只评了下一行的 "smart-seeming"。 | "AI = artificial intelligence"（4 词） |
| l34（s7） | P2, P3 | 记录 | 圆内标签 "Chess program (rules)"，右侧又有 "✓ Chess program: AI" | 同一屏 "Chess program" 出现两次，阅读落点重复。 | 圆内只留一个点或图标，或删掉右侧那条，只保留 "✗ Payroll program: not AI" 做对照 |
| l25 改写约束 | P2 | 记录 | "In this experiment: more examples, better scores" | 这里的 "In this experiment" 是对应口播的范围限定，任何压缩都要保留，否则就变成一条泛化断言。a 的改写把它删了。 | "Here: more examples, better scores"（5 词） |
| outro（card_s10） | P2, P4 | 必改 | "IN ONE SENTENCE" / "Not rules people write" / "Patterns learned from examples" | 综合 a、b：眉题和内容不符，丢了 "most"。a 的改写只换眉题，没有补回 "most"。 | 眉题 "MOST OF TODAY’S AI"；主体 "Not rules people write / Patterns learned from examples"；保留 "Next · Overfitting" |

## 驳回

- b l09–l10、l22–l23（P1/P3/P5 必改，「20 个标注块」「l10 27 词」「l23 26 词、13 块」）：第 1 轮裁决 I20 已认定数字墙下的 0–9 是答案标注，属于编号，本轮规则也写明 numbering 不计词，芯片行和坐标刻度同理，所以不构成违规。改写 "four rows of five" 只是在钻分组规则的空子；"Missing digits: 0, 4, 7, 8" 把一眼就能看懂的灰色芯片换成要读的文字，更差。
- b l01（必改，「cold open 仍是完整叙述句」）："Your phone / spots your cat" 和 "No one wrote cat-spotting rules" 各 5 词，是标题式短句，没超限，第 1 轮作者已按要求改过。改写 "Your cat, found" 丢了主语 phone 和反差钩子，更差。
- b l06–l07 改写 "Also 8 / Also 5"：母语读者会觉得缺冠词，不合语法。这里真正的问题是折行，加 nowrap 或调宽列即可，保留 "Also an 8 / Also a 5"。
- b intro（P4 必改 "What Is AI?"）及 R 中的 I3/I6：片头卡不在严格项清单里，第 1 轮裁决只定为「建议」，作者以系列包装统一用 title case 为由不改，理由成立，记录即可。
- b P5 l25「27 词 / 7.8 秒、需约 9 秒」：图表文字和方法注在 l23/l24 已经出现，l25 新增阅读只有 12 词，负担判断不成立。字数超限仍然在 P1 计。
- b l25 改写 "Labeled 3s"：丢了口播 "only told it which images were threes" 中「只给标签、不给规则」的对照，意思变模糊。
- a l44–l49 改写 "It predicts, not proves" / "It mirrors its data"：前一句不是地道英语；后一句删掉了口播 l48 明说的 "how it's designed and trained"，造成新的不准确。
- a l25 改写 "More examples, better scores"：删掉 "In this experiment" 的范围限定，把实验结论变成了泛化断言。
- a l39 改写 "10 years of mostly male résumés"："male résumés" 搭配别扭，简历本身没有性别。现版 "10 years of résumés, mostly men’s" 更自然，也不超限。
