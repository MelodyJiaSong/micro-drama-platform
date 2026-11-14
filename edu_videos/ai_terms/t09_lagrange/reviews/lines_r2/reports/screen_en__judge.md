# screen_en__judge（claude-opus-5-5）· 第 2 轮裁决：English on-screen text

## 裁决
- P1 2 理由：a 站得住。按第 2 轮分组规则逐屏核过，没有硬上限超标：l27 是表格两行（1 块）+ 公式 + 说明行，共 3 块 16 词；l39 是标题 + 三行列表（1 块），14 词；l06 中淡出的「No wall / A price instead」是一行同类项，算 1 块，加上「Cross it → lose points」和正文，共 3 块 14 词。b 认为「λ tunes itself」是“解释性从句”，但它只有 3 个记号，是标题，不是口播句（口播是 “And λ adjusts itself during training…”），所以 1 分不成立。剩下的小瑕疵是 l27 把同一关系印了两遍（+0.29 ≈ 3 × 0.1 和 Extra height ≈ 3 × extra radius）。
- P2 1 理由：判 1 分，但理由不是 b 给的那条。l02 的引语「“Do your best” → Be helpful」是“口语要求 → 正式目标”的对应结构，不算重复，b 的这条证据驳回。真正与口播对不上的有两处，都在严格项：①冷开场 l01–l02 的「Be helpful」丢了口播 “as helpful as you can” / “Do your best” 的“尽量”含义，同一概念到 l33 又写成「Most helpful」（中文源两处都是“尽量有用”）；②片尾 card_s6 的眉标「IN ONE SENTENCE」，而口播 l40 说的是 “in one line”，眉标下面的「Price the rule just right」也不是一个句子。见补充问题。
- P5 2 理由：抽查后维持 2 分。两人各漏一半，合起来证据完整：l07「1 hour a day at / most」把 at most 拆到两行（b 抓到）；l23「straight through / fence」孤字成行（b 抓到）；l17 标注「Farther out, higher price」右端约 x≈1000，超出地图面板边缘 x≈965（a 抓到，b 误判已解决）；l33 标题贴着卡片底边（两人都抓到）。l28（2.3 s）只新增 2 个词，l30（4.2 s）9 词，都读得完。没有发现两人共同漏掉的时长问题。
- P6 2 理由：b 给 3 分偏高，有几条改写比原文差。「Harm ≤ limit」（l01、l33）把口播和全片统一用的术语 line 换成了 limit，l35 图中也标着 “The line”；把 l35 改成「Tuning λ」会和 s3 手动调价的标题撞名，抹掉“λ 自己调”这个要点；a 给 l04 的「Do it as well as possible」比原文还长，“it” 仍然没有指代。其余改写可用（如「Rule: inside the fence」「Uphill → straight out」「λ = Lagrange multiplier」）。
- R 1 理由：上一轮的 I1 是严格章节标题项，在本轮被审渲染里只改了一半：c_problem 卡已改成 “What is a Lagrange multiplier?”，但 l04–l10 共 7 屏的眉标仍是「01 · What a Lagrange multiplier is」，与卡片不一致。a 自己把它列为必改却给了 R 2 分，前后矛盾。另外，I11 的改法造成 l07「most」孤行，I26 的改法造成 l23「fence」孤行，都是改出的新问题。已核对场景源文件：`scenes/web/s2.html:25` 现已写成 `01 · What is a Lagrange multiplier?`，但修改时间（13:09）晚于截图（13:03），必须重新渲染、确认截图后才能销项。**定稿：l04–l10 眉标 = `01 · What is a Lagrange multiplier?`**（与 c_problem 卡逐字一致）。

## 补充问题

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| card_s6（片尾） | P2 | 必改 | IN ONE SENTENCE（眉标） | 严格项。口播 l40 说的是 “So, in one line: …”，屏幕却写 sentence；下面的「Price the rule / just right」是祈使短语，不是句子。眉标和口播、和正文都对不上。两位都判片尾“已解决”，漏了这条。 | **IN ONE LINE**（定稿；标题「Price the rule / just right」和「Next · Gradient descent」保持不动） |
| l01–l02（冷开场，`scenes/web/s0.html:13`） | P2, P3 | 必改 | Be helpful | 严格项。口播是 “be as helpful as you can”，l02 的引语是 “Do your best”，都是“尽量、做到最好”的意思；「Be helpful」把这层最大化丢了，引语和正式目标对不上。同一概念在 l33 写作「Most helpful」，中文源两处都是“尽量有用”，英文前后不一致。b 只指出“祈使句与不等式不平行”，给的改写还换了术语，见驳回。 | **Most helpful**（定稿；红行「Harm ≤ the line」和两条灰色引语保留不动，l01/l02 都改） |
| l37–l39 | P3, P4 | 建议 | ① Safety line ／ λ tunes itself | 右列第 1 行是主谓从句，第 2、3 行是「Complexity costs」「Drifting costs」名词式，列表不平行；而且第 1 行只是重复 l35 的标题。 | **Harm costs**（①行右列） |
| l08 | P2, P4 | 建议 | 1 extra minute ／ 1 minute less | 两行不平行；口播说的是 “every minute under earns one”。 | **1 minute over −$1 ／ 1 minute under +$1** |

## 驳回
- b · l01–l02 必改（引语重复 + 改写「More help / Harm ≤ limit」）：引语与正式目标并列是对照结构，不算重复，应保留。改写把全片统一术语 “the line” 换成 “limit”，与口播、l33、l35 图中标注都冲突；“More help” 也表达不出“尽量”。这一条由补充问题中的「Most helpful」替代。
- b · l35–l39 必改「λ tunes itself → Tuning λ」：3 个记号的标题不是口播句。「Tuning λ」是 l16–l19 手动调价的标题，搬到 l35 会把“训练中自动调整”混同为“我们手动调”，改写比原文差。不成立。
- b · l13 级别「必改」：非严格项，意思清楚，降为建议。改写「Rule: inside the fence」可以采纳（比「stay inside the fence」短，60px 下仍放得进一行）。
- b · l33 改写「Harm ≤ limit · Maximum help」：同样换掉了 line 术语，并且打破与冷开场的呼应。措辞保持「Harm ≤ the line · Most helpful」，只把卡片下方间距加约 40px。
- b · l07 改写「Daily limit: 1 hour」：76px 下大约到 x≈1880，超出右边距，仍会折行。定稿改用 **Max 1 hour a day**（约到 x≈1760，一行放得下）。
- a · P1 证据「l06 同屏 5 个文字元素，超 4 块上限」：按第 2 轮分组规则，淡出的「No wall / A price instead」是同类一行，算 1 块，l06 实际 3 块，不算超标。淡出建议本身可以保留为建议。
- a · l04 改写「Do it as well as possible」：比原文长，“it” 仍然没有指代。如果要改，用 **As good as possible**，与口播 “as good as possible” 一致。
- a · l17 改写「Farther out → higher price」：长度和原文一样，解决不了超出面板的问题。只采纳“把标注框左移、收进面板内”这一做法。
