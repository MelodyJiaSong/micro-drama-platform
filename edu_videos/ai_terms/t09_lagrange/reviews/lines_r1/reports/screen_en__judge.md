# screen_en__judge 裁决（第 1 轮）— English on-screen text

裁决人：screen_en__judge（claude-opus-5-5）。已读 a/b 两份报告、materials/screen_en.md、本项标准，并逐张看了截图 card_intro、card_c_problem、card_s6、s0_l02、s0_l03、s2_l04、s2_l06、s2_l08、s2_l09、s2_l10、s3_l15、s3_l17、s3_l20、s3_l21、s3_l23、s4_l27、s4_l29、s4_l30、s5_l31、s5_l33、s5_l35、s5_l36、s5_l39；另核了 scenes/web/s2.html、s3.html、s5.html 的相关文案。

## 裁决

- P1 1 理由：b 站得住。l20、l21 截图实数为 chart、“Tuning λ”、“λ 3/4”、“Right on the fence/Hiding inside”、“Height 7.75/6.00” 共 5 块，超过 4 块的硬上限，a 自己也把它列为必改，却仍给 2 分，自相矛盾。outro（card_s6，严格项）主标题 “a price on a constraint, set just right” 共 8 词，超过标题 6 词上限；它和上面的 “A Lagrange multiplier is” 连起来就是 l40 口播原句，属于屏上写散文。b 说 l39 分组表格是 14 词的单块、算超限，这一条不成立，见驳回。
- P2 1 理由：b 站得住。l23 “Uphill points / straight out of the fence” 几乎照抄口播 “uphill points straight out through the fence”，两人都认定。严格项 outro 原样重复 l40 的定义句（“a Lagrange multiplier is a price on a constraint”），按严格项规则必改，a 只按 P4 记成建议。l27 “Loosen a bit, gain ~3×” 单看会读成“高度变 3 倍”，丢了“相对于半径增量”这层关系，b 的指正成立（上方有算式 +0.29 ≈ 3 × 0.1 可以缓解，但标题本身仍会误导）。l30 标题是口播结论的改写句。
- P3 1 理由：判 1，但 b 的理由只成立一半。l20–l21 右栏同时摆了 60px 标题、150px 的 λ 数值、54px 状态行、HEIGHT 标签加 54px 数值，150px 的 λ 抢在标题前面先被读到，实际超过 title / point / note 三级。严格项章节卡 c_problem 的 “What a Lagrange multiplier is” 是从句，另外三张卡（A small experiment / Lambda as a price / An example from AI）都是名词短语，属于严格项里的不一致（a 已指出）。l39 左栏三行也不平行，分别是 “Safety line”、“Regularization”、“Stay near the original”。b 举的 card_intro 裁切是排版和可读性问题，归 P5，不能作为 P3 的依据。
- P5 1 理由：b 站得住，问题还比两人报的多。card_intro 截图里 “Lagrange multiplier” 左右都出了画框，开头的 L 和结尾的 r 被裁掉（b）。l30 在 4.2s 内出 14 词，约 3.3 词/秒，还要分神看字幕（两人都报了）。l17 红字 “Farther out, higher price” 压在橙色等高线填充上，并伸出面板边缘（a）。l33 主句紧贴卡片底边（a）。两人都漏了：l35/l36 图内批注 “Over → λ up” 顶部字形被图框截掉，l04、l15 有孤词换行。有多处文字被裁切，不能算“基本没问题”。
- P6 2 理由：a 给 2 分合理，b 给 3 分不成立。两人的改写里都有比原文更差的，例如 a 的 l30 “Big λ → Binding / λ = 0 → Slack” 引入口播里没有的术语，b 的 l23 “Uphill: perpendicular to fence” 也一样，b 的 l01–l03 “Goal / Constraint” 则提前抢了 l04 的卡片。两人还共同漏掉了 l35/l36 批注裁切、l04/l15 孤词换行，这几处都没有改写，谈不上“每处都有可直接替换的改写”。

## 补充问题

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l35 / l36（图内批注） | P5 | 必改 | Over → λ up | 截图里红色批注顶部被 SVG 图框截掉，“O” 和 “λ” 的上沿是平的。s5.html 第 69 行把它放在 yH(0.7)+6，紧贴图区上沿。两人都没看出来。 | 文字不变，批注下移约 20px，或给图区加上内边距，保证整行字形完整 |
| l15 | P5 | 建议 | Find: height − charge, / max | 截图里 “max” 单独掉到第二行成了孤词，读起来更像制作备注（两人只批了措辞，没看换行）。 | Maximize height − charge（一行放下） |
| l04 | P5 | 建议 | Don’t cross the / line | CONSTRAINT 卡片里 “line” 单独掉到第二行，和左边一行就放下的 GOAL 卡片不对称。 | Don’t cross the line（缩字号或加宽卡片，保持一行），或 Stay under the line |
| l27 | P5 | 建议 | Loosen a bit, gain ~3× | 76px 标题右端到约 x=1830，超出左右各 120px 的版心。改写时与 b 的 P2 意见一起处理。 | Extra height ≈ 3 × extra radius（同时缩到版心内） |
| l21 | P3 | 记录 | 绿色空心圈（上一屏 λ=3 的落点） | 上一屏最优点的绿圈留在图上，没有任何标注，不熟悉的观众会把它当成第二个点。 | 在绿圈旁加图内小字 “λ 3”，或改成淡灰色 |

## 驳回

- b · l39（P1，“分组表格 14 词超过 9 词”）：按第 2 轮计数规则，形态相同的行（每项 ≤6 词、最多 6 项）合并算一块，用来解决块数问题；单项限的是每行 ≤6 词，并不要求合并后的整块 ≤9 词。l39 全屏共 17 词，没超过 22 词，不算硬上限违规。左栏不平行、“Too complex costs” 措辞别扭的问题仍然成立。
- b · l01–l03（cold open 改成 “Helpfulness ↑ / Harm ≤ limit”，侧标改 “Goal / Constraint”）：改了更差。冷开场的钩子就是 “Do your best” 和 “never cross” 这两句口语要求形成的反差。改成 Goal/Constraint，会在 l04 讲到之前就先用上术语，还和 l04 的两张卡片重复。冷开场真正要改的是 a 指出的 “Do your / best” 换行，以及给两句加引号。
- b · l35–l36（“λ tunes itself” 是完整说明句，必改）：不成立。这是 3 个记号组成的标题式短语，符合屏上提纲写法；改成 “Adaptive λ” 反而换上了口播里没有的术语，口播用的是 “adjusts itself”。
- b · l23 改写 “Uphill: perpendicular to fence”：问题本身成立，但这个改写引入了口播没说过的 “perpendicular”，违反 P2 “用词与口播一致”。a 给的符号版 “Uphill ⟂ fence” 对大众观众也同样难懂。建议用 “Uphill → straight through fence”。
- a · l30 改写 “λ flags binding rules / Big λ → Binding / λ = 0 → Slack”：binding/slack 是口播没有的专业术语，备选的 “Holds you / Doesn’t” 不成英文短语。改用 b 的 “High λ → Costly constraint / λ = 0 → No cost” 更好，记得把标题一并缩短。
- a · l21 “6.00 is a number the narration never says”：P2 本来就要求数字由屏幕承担，屏上给出口播没念的读数正是分工到位，不算问题。这一行只有 5 块超限这一条成立。
- b · card_intro（归在 P3）：裁切是事实，但属于 P5 的排版和可读性问题，跟层级无关。截图可能只是缩放动画的中间帧，裁决人能读的材料里没有片头卡源文件，无法核实；修改前需要先确认最终停留的那一帧也被裁切。
