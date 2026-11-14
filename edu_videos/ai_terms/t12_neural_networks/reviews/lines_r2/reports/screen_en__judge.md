# screen_en__judge（claude-opus-5-5）· lines_r2

核对依据：两位审稿报告；`materials/screen_en.md` 逐屏重算；截图 s0_l03、s3_l21、s3_l24、s5_l35、s6_l41、s6_l44、s6_l46、s6_l47、card_intro；`previous.md` 本项条目（I15、I22、I38 的上一轮裁决）；`package.json`；另从 `renders/package/en/` 的 agenda、outro、chapter_lens、chapter_real 抽末帧核对包装卡（只读，未改任何被审文件）。

## 裁决
- P1 2 理由：a 站得住。b 判 l20–l24 网络图「10 词超过 9」不成立：本轮口径「整张图合算 1 块」与同构列表一样只用于块数上限，图内文字计入每屏 ≤22 词，不套每块 ≤9 词（上一轮 I22 已这样裁，列表块本来就能超过 9 词，同理）。逐屏重算：l24 = 2+4+4+图 10 = 20 词 / 4 块，l21 = 4+5+10 = 19 词 / 3 块，l36 = 6+6+3 = 15 词，标题最长 l31「Side by side: 1 bend each」6 词，都不超限。l47 是引语卡，上一轮 I38 已裁为可接受的例外。扣 1 分是因为 l24 在词数和块数两个上限上都顶格。
- P2 2 理由：b 给 1 分的唯一依据是 l47 引语和口播重复，上一轮 I38 已驳回（引语卡出示论文原话并标出处），不成立。a 列的 l44「Not told what to look for」、l29「Each corner = one unit」和口播几乎一字不差，属于短标签的小瑕疵，只到「建议」。另有 l35「10 in 5 layers: 32 pieces」把口播「can give 32」说成了必然结果（见补充问题）。整体是基本没问题、有小瑕疵，给 2。
- R 1 理由：b 的分数成立，但理由要换。b 依据的 I22、I38「未解决」都不成立（见驳回）。真正的问题是几处修改改出了严格项上的新毛病。I5 的修改让目录卡提示句「Not required — recapped in one line.」带句号，渲染画面已确认。I20 让 l13「Straight lines only」和冷开场 l03「Only straight lines」成了同一句话的两种语序。I6 的作者理由是「包装卡已人工看过」，但现有 `renders/package/en/agenda.mp4`（21:19）早于 package.json 的显式编号修复（21:23），画面上的编号仍是 01/03/04/05，chapter_experiment 卡也没有渲染（见补充问题）。a 记下了前两条，但只给 2，偏宽。
- P5 2 理由：两人都判 2，抽查同意。l22「37 knobs」1.9 s、l38 5 词 2.3 s、l16 5 词 2.7 s、l36 新增 3 词 3.1 s 都读得完。两人共同漏掉的是排版断行：s0_l03「Only straight / lines」和 s6_l44「Layer 1: stripes, / colors」各把一个词单独甩到下一行，看字幕的同时读这种断行更费劲。只是建议级。outro 的停留时长已从渲染核实：两行分开，下面是「Next · Backpropagation」，b 说的「无法核实」可以撤销。
- P6 2 理由：b 给 3 分偏高。b 对 l20–l24（「12 units / 1 unit」）和 l47（「The value of depth」）的改写，上一轮已经判为更差。l46 改成「Top-1 accuracy: ~2 percentage points lower」又删掉了起因「Remove a middle layer」，也删掉了「First-guess」这个解释。a 的改写大多可以直接替换（l03/l13 统一、l24 删 h2、l21、l46），只有 l44「Self-learned」引入了口播没说过的新说法。两人都没给 l35 和目录编号写改写，所以给 2。

## 补充问题
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| agenda（渲染） | P3 | 必改 | `renders/package/en/agenda.mp4` 末帧编号「01 / 03 / 04 / 05」 | 目录是严格项。现有渲染早于 package.json 的显式 tag 修复（21:19 早于 21:23），画面编号仍跳过 02，和章节卡、页眉的 01–04 对不上。源文件已改，但成片可用的渲染没有更新，作者 I6「已人工看过」的说法不覆盖当前版本。中文 agenda 渲染（21:23）也要一并核对。 | 重渲 en/zh agenda，确认显示「01 Beyond straight lines / 02 Build a small network / 03 Why go deep? / 04 AlexNet, 2012」后再锁定 |
| c_experiment | P3, P5 | 存疑 | `renders/package/en/` 与 `zh/` 都只有 chapter_problem、chapter_lens、chapter_real，没有 chapter_experiment | 第 02 章章节卡（严格项）没有渲染画面，章名、编号和停留时长都无法核实。 | 渲染 chapter_experiment，核对「02 · Build a small network」 |
| agenda prereq_hint | P4 | 必改 | 「Not required — recapped in one line.」 | 渲染已确认（a 上轮列为存疑）：严格项上的片段带句末句号，「recapped」也偏生硬。 | 「Not required — one-line recap」（不带句号） |
| l35 | P2 | 建议 | 「10 side by side: ≤ 11 pieces」/「10 in 5 layers: 32 pieces」 | 口播说「at most 11」「can give 32」，两个都是上限；屏上一个写 ≤、一个写死，读起来像叠层就一定得到 32 段。l33–l34 的「hand-built example」注释到这一屏也收掉了。 | 「10 in 5 layers: up to 32 pieces」（7 词，块内合规） |
| l03, l44 | P5, P3 | 建议 | s0_l03「Only straight / lines」；s6_l44「Layer 1: stripes, / colors」 | 截图里都把一个词单独断到下一行，短语被切开，边看字幕边读更费劲。 | 加宽文本框排成一行，或断成「Only / straight lines」「Layer 1: / stripes, colors」 |
| l47 | P4 | 记录 | 「“The depth really is important”」 | 论文 §7 原句是「So the depth really is important for achieving our results」。屏上截取后把 the 改成了大写 The，结尾也没有省略号，严格说不算原样引用。 | 「“…the depth really is important…”」或保持现状 |

## 驳回
- b · l20–l24（P1，必改，网络图 10 词超 9）：「整张图合算 1 块」只用于块数上限，图内文字计入每屏 ≤22 词，上一轮 I22 已裁定。改成「12 units / 1 unit」会丢掉口播强调的层号，更差。b 在 R 里写「I22 未解决」，同样不成立。
- b · l47（P1/P2，必改）：引语卡出示原话并标出处是标准做法，上一轮 I38 已裁定。「The value of depth」/「Paper takeaway」既丢了证据，又引入了行话。b 在 R 里写「I38 未解决」也不成立。
- b · l21「visibly cramped comma–plus join」：s3_l21 截图里是正常的「Add up, +1 knob → fare」，有空格，并不挤。b 的改写「Sum + knob → fare」还丢了「再加一个」的意思。措辞生硬这一点保留，采用 a 的「Sum + 1 knob → fare」。
- b · l46 改写「Top-1 accuracy: ~2 percentage points lower」并删掉说明：删掉了起因「Remove a middle layer」和「First-guess」的解释，更差。只把「pts」改成「points」即可：「Remove a middle layer → ~2 points worse」（与口播「Remove」一致，不用 a 的「Drop」）。
- a · l44 改写「Self-learned, placed as a caption」：「Self-learned」是口播没说过的新说法，违反 P2，挪成 caption 还多出一块。问题本身（标签和口播几乎一字不差）只够记录，保持现状。
- b · outro「line separation remains unverified」、b/a · I6/I11「包装卡无法核实」：outro 渲染已核实，两行分开，下面是「Next · Backpropagation」，这一点可以撤销。agenda 和章节卡的实际问题改记在补充问题。
