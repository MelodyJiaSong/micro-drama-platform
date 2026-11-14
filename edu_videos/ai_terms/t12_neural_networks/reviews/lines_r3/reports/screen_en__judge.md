# screen_en__judge 裁决（lines_r3，第 3 轮 · 终轮，claude-opus-5-5）

核对依据：`materials/screen_en.md`、截图 s4_l30 / s3_l24 / s5_l36 / s6_l41 / s6_l46 / s0_l04；场景源 `scenes/web/s4.html:22-23`（仍为 `Which way<br>to turn?` / `Next episode`）、`scenes/web/s6.html:52`（仍为 `~2 pts worse`）；另从 `renders/package/en/agenda.mp4`、`outro.mp4` 抽末帧核对包装卡（两位审稿人都说「无法核实」）：目录 01–04 连续、提示「Helpful to know · Gradient descent · S1 · E4 · Not required — one-line recap」（无句号）、片尾「In short / Simple units, stacked in layers / Stack deep → recognize complex patterns / Next · Backpropagation」，分行清楚；`chapter_experiment.mp4` 已存在。

## 裁决

- P1 2 理由：除 l20–l24 网络图与 l47 引语卡外，全片每块 ≤9 词、每屏 ≤22 词（最高 l24 约 18 词、l36 17 词）；b 的两条依据都已有前两轮裁定（见驳回），不构成新的超限。a 指出 l35「10 in 5 layers: up to 32 pieces」（8 词）偏长属实，但在上限内，2 分。
- P2 1 理由：a 的 l30 证据成立，且 l30 是严格项（衔接句）：口播已改成「there's a much faster way to find each one's direction. That's next time」，屏上仍是「Which way / to turn?」+「Next episode」，像是在问 l25 刚演示过的「每个旋钮往哪拧」，与口播、与 l25 都对不上，必须改。b 的 l47 依据不成立（见驳回），但本维度因 l30 判 1。
- R 1 理由：l46 屏上仍是「Remove a middle layer → ~2 pts worse」（s6.html:52 原样），上一轮 I19/I20 已裁「pts → points」，作者标「已改」与实际不符，未解决；l30 口播改写（v1.2）后屏幕未同步，改出新问题。其余：I1–I5 经我抽包装卡末帧核实已解决（b 判「未核实」不再成立）；I8、I9、I12、I17、I22 已解决；I7、I10、I11、I14、I16、I18、I21 的不采纳理由成立。
- P6 2 理由：a 给了 l30「A faster way / Next time」这类可直接替换的写法，方向对；但 a 的 l35 改写加两个「units」会让右侧标题超出画面宽度。b 漏掉 l30，且「L1: 12 units」「Unit → corner」「The importance of depth」都丢信息或引入缩写，3 分偏高，取 2。
- P4 2 理由：两人共同抓到 l46「pts」与 l29「Unit bends → corner」略生硬；两人共同漏掉 l24「Named after neurons · loosely」用间隔点把副词切出去，读出来像翻译腔（补充问题）。章节名「Beyond straight lines / Build a small network / Why go deep? / AlexNet, 2012」朗读自然，无尾句号，2 分。

## 维持的问题（终稿改写）

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l30 | P2, P3 | 必改 | h1「Which way / to turn?」+ h2「Next episode」 | 严格项（下期预告衔接句）。新口播讲的是「更快地算出每个旋钮的方向」，屏上却把「往哪拧」当成未解问题，与 l25（已用上期办法逐个往下坡拧）矛盾，也和口播「next time」用词不一。 | h1「A much faster way」（两行：A much / faster way）+ h2「Next time」。若 l30 口播终稿点明「millions of knobs」，可改为 h1「Millions of knobs?」+ h2「Next time: a much faster way」。两种都不说「往哪拧」是新问题，只说「更快」，不碰 l25。中文屏「旋钮的坡度怎么算？/ 下一期」请口播定稿后一并核对。 |
| l46 | P4 | 必改 | 「Remove a middle layer → ~2 pts worse」 | 上一轮裁决人已定「pts → points」，作者标「已改」但屏上和源文件都没改；终轮不能再留。 | 「Remove a middle layer → ~2 points worse」（保留下方小字「First-guess accuracy (top-1)」，宽度在画面内） |
| l36 | P3 | 建议 | 「Earlier folds, reused」位于左侧（并排·阶梯）图下 | 这句说的是叠层网络，却挂在并排那张图下面，容易被读成阶梯图的说明。 | 文字不变，挪到右侧（5 层·锯齿）图下，字号降到 caption 级 |

## 补充问题

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l24 | P4 | 建议 | 「Named after neurons · loosely」 | 用间隔点把「loosely」单独切出去，朗读像两段残句，和全片「A · B」并列用法（如「Layer 1 · 12 units」）也不一致。 | 「Loosely named after neurons」 |

## 驳回

- b · l20–l24（P1，必改，网络图 10 词超过 9）：前两轮（r1 I22、r2 I11）已裁：「整张图算 1 块」是为了不让图内标签撑高块数，图内文字计入每屏 ≤22 词；图里是四个各 ≤4 词的独立标签，不是 10 词的一句话。改写「L1: 12 units」又引入缩写，比现状差。终轮维持。
- b · l47（P1/P2，必改）：前两轮（I38、I21）已裁：引语卡出示论文原话并标出处（§7）是标准做法，本轮已按 I22 加省略号。「The importance of depth」+「Paper finding」去掉了证据，不采纳。
- b · l29 改写「Unit → corner」：丢掉「bends」，箭头两端都是名词，意思更含糊；现状「Unit bends → corner」可保留。
- b · l46 改写「Middle layer removed → ~2-point drop」：改了口播一致的动词「Remove」，没必要；只换「points」即可（见上表）。
- a · l35 改写「10 units side by side: up to 11 pieces」/「10 units in 5 layers: up to 32 pieces」：s5_l36 截图里右侧标题已占到 x≈960–1805，54px 下两处各加「units」会超出 1920 画面；「≤」与「up to」并存只到记录级，保持现状。
- b · R「I3/I4/I5 未解决（包装卡未核实）」：已从 `renders/package/en/` 抽 agenda、outro 末帧核实，chapter_experiment 也已渲出，判为已解决。
