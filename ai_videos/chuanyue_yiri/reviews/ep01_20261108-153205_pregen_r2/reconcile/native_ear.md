# native_ear（母语听感）双审对比

- a 位：claude-sonnet-5-5/native_ear__a（claude-sonnet-5-5）报告 `reports/native_ear__a.md`
- b 位：gpt-6-astra/native_ear__b（gpt-6-astra）报告 `reports/native_ear__b.md`
- 状态：完成；裁决人 claude-opus-5-5/native_ear__judge，报告 `reports/native_ear__judge.md`

## 评分对比

| 维度 | a 分 | a 证据 | b 分 | b 证据 | 需裁决 | 最终 | 裁决理由 |
|---|---|---|---|---|---|---|---|
| N1 自然度 | 2 | 逐句听下来约 35 句 Riley 英文，绝大多数自然（s2_st8 "apparently a woman in pants is a lot"、s4_st4 "I'm totally lost… and I still smell like pee"、s8_st4 "Rookie mistake"、s7_st4 "Cozy."）；"有点怪"4 句：s8_st10、s4_st2 第二段、s5_st9、s8_st1；没有"很怪"。 | 2 | L8–128 的 Riley 台词逐句见下表；L36 的 his、L50 的 they、L119 的 Rope springs 有轻微听辨负担，其余主要是自然口语。 | 抽查 | 2 | 同意两人都给 2 分。逐句复听 L8–L128，Riley 的英文大多是自然的美式口语（L11 "is a lot"、L42 "I still smell like pee"、L53 "Rookie mistake"、L108 "truck stop"、L122 问答清单）。两人一致标出的 L36 his 指代不清、L50 they 指代不清，我核过都成立，属于「有点怪」。a 单独标的 L70 "means right?"：纯听觉下会被听成 "means, right?"，这一镜靠模型自己出声，语调不受控，所以 a 的风险判断成立；b 判自然也有依据（L66 的指路动作能消歧）。两人都没指出、我补一处：L125 "people will still read it"，母语者在这里更常说 "will still be reading it"，现在的说法偏平，属于记录级。全片没有一句「很怪」，所以不判 1；还有上述小瑕疵，所以不给 3。 |
| N2 别扭原因 | 2 | 别扭原因集中在指代不清（s8_st10 "they've got"、s4_st2 "up to his nose" 的 his）、同音歧义（s5_st9 "means right?" 听着像附加问句）、讲解腔（s8_st1 "basically Pompeii's two o'clock alarm"）；无直译句式，无穿越者视角错乱（s7_st2 末句已改成 from now on 的视角）。 | 2 | L25 仍用 Sounds like left 表示无依据的猜测；L36 代词有两个男性先行词；L47 信息包装稍像预写讲解，见 B01–B05。 | 一致 | 2 |  |
| N3 笑点与回收 | 2 | dextram 线回收完整（s3_st4 随口猜 left → s4_st3 "Left. Definitely left." → s5_st8 店主喊 → s5_st9 "I went the wrong way all morning"）；garum 线 s3_st4/s5_st13/s5_st5/s7_st1 呼应；s7_st6 "Air conditioning / that's the bathroom" 靠画面成立。小瑕疵：s4_st2→s4_st5 的"钱不臭"笑点只靠 "Smell anything?"→"…Nope." 暗示；"Mission two" 的开场目标本范围内无法核（s1 不在材料内）。 | 2 | L25→30→67→70 的 dextram 猜错、强化、纠正链可读；L36→39 的 Smell anything/Nope 和 L94→122 的找床/找到床均有回收。L94 的 Mission two 缺 s1 原句，只能保留未核实边界，见 B06。 | 抽查 | 2 | 同意两人都给 2 分，并关闭两人共同留下的存疑。dextram 线完整：L25 猜 left → L30 "Definitely left" → L42 迷路 → L67 店主喊 Dextram 并往右指 → L70 恍然大悟。开场目标的回收我核过：s1_st2 的 prompt.txt L19 和 filming.json L38 都写着 "Mission one: find a bed before dark. Mission two: try garum… And my budget… is this."。所以 L94 "Mission two: done. Now… a bed." 的编号和顺序都对；L122 Bed→Garum→Budget 的顺序和开场一致；"Budget? …Gone" 回收开场的 "my budget… is this"，也和 L104 付后 0 枚、L121「两手是空的」对得上。a 的存疑（s5_st7）和 b 的 B06 都可以关闭。不给 3，是因为 L36→L39 的「钱不臭」笑点只靠 "Smell anything?"→"…Nope." 这一问一答落地。L38 写她自己闻钱、一本正经说 Nope 再笑出来，不懂典故的观众也能接住动作笑点，但「皇帝收尿税」的反讽只有一半落地。这是记录级，不必为它加词。 |
| N4 人设口吻 | 2 | 口吻整体是二十多岁美国旅行博主（kinda、SO hot、funky、Rookie mistake、pretty sure），s7_st2/s7_st3 转温柔也合理；小瑕疵是口癖重复：basically 出现在 s8_st1、s5_st5、s6_st6 三次，省略号停顿几乎每句都有（s3_st3、s3_st4、s5_st5、s5_st7、s7_st7、s7_st1）。 | 2 | L11 的 is a lot、L53 的 Rookie mistake、L91 的 grandma 和 L108 的 truck stop 都符合现代年轻旅行博主；L47 略偏解说，L119 的 Rope springs 略显生造。 | 一致 | 2 |  |
| N5 改写 | 3 | 下面问题表里每个"有点怪"句和口癖都给了不更长的改写（如 s8_st10 7 词→5 词；s6_st6 删 basically；s8_st1 删 basically 和 And）。 | 3 | 全部五处「有点怪」均给出不增词改写；整段词数分别 9→8、27→25、19→15、7→5、6→6，并列出按 2.8 词/秒所需最低发声时间。 | 一致 | 3 |  |
| N6 最别扭的 5 句 | 3 | 已排出最别扭的 5 句并排序（见下节）。 | 3 | 下文按听者即时理解负担列出最别扭五句，顺序为 L36、L25、L50、L119、L47；均能对应逐句表与问题表，没有把自然短句凑作问题。 | 一致 | 3 |  |

## 问题表（两位审稿人与裁决人的并集，去掉完全相同的行）

| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 | 来自 |
|---|---|---|---|---|---|---|---|
| s8_st10 | 全镜（台词 8 秒内） | N2 指代不清（承 I164） | 可剪 | ① 故事 | "The smallest coin they've got."：they 指罗马人还是门房不明；"Cover charge?" 像在转述问话，镜头前听着断开 | 便宜：改 "Cover charge? One tiny coin."（7 词→5 词）；若要保留"最小面额"梗：“Cover charge? Smallest coin they make.” | a |
| s4_st2 | 约 5.6–11 秒（第二段） | N2 指代不清 | 可剪 | ① 故事 | "so Dad held a coin up to his nose"：his 是皇帝还是儿子；"Dad" 称呼与前文 "the emperor" 不衔接（听感"很突兀"） | 便宜：改 "His son called it gross — so he held a coin under the kid's nose: "Smell anything?""（长度不增）；保持后面 s4_st5 "…Nope." 即可 | a |
| s5_st9 | 整句 | N2 歧义（音频） | 可剪 | ① 故事 | "dextram" means right?：纯听觉下 "means right?" 近似 "means, right?" | 便宜：改 "Wait… "dextram" is *right*? I went the wrong way all morning."，台词括号注"right 重读、一拍停顿"（词数不增） | a |
| s8_st1 | 6.1–13.1 秒 | N2 讲解腔（承 I166） | 记录 | ① 故事 | "That's the Temple of Isis — basically Pompeii's two o'clock alarm. And at two, everybody hits the baths." 定义句式 + 与 s5_st5、s6_st6 的 basically 重复 | 便宜：改 "Hear that? That's the Temple of Isis — Pompeii's two o'clock alarm. At two, everybody hits the baths."（删 basically 和 And） | a |
| s6_st6 | 全镜 | N4 口癖重复 | 记录 | ① 故事 | "Ha — it's basically a truck stop." 与 s8_st1、s5_st5 共三处 basically | 便宜：改 "Ha — it's a truck stop." | a |
| s3_st4 | 整句 | N2 电报式 | 记录 | ① 故事 | "Okay. Straight… then 'dextram.' No clue. Sounds like left?" 四个碎句 | 便宜：改 "Okay, straight, then… 'dextram'? No clue. Left, maybe?"（词数相同，更连贯） | a |
| s5_st1 | 整句 | N1 语序 | 记录 | ① 故事 | "Good news? Dinner here is at three-thirty." 母语者更常说 "Dinner's at three-thirty here." | 便宜：改 "Good news? Dinner's at three-thirty here."（更短） | a |
| 全集 | — | N4 省略号停顿口癖 | 记录 | 规则源 | 省略号开头/中段几乎每句都有（s3_st3、s3_st4、s5_st5、s5_st7、s7_st1、s7_st7），听感节奏单一 | 便宜：至少留 2–3 句直说不拖音，如 s5_st7 "Mission two: done. Now a bed." | a |
| s4_st2 → s4_st5 | — | N3 笑点 | 记录 | ① 故事 | "money doesn't smell" 的结论从不说出口；不知典故的观众只能靠 "Nope" 猜 | 存疑：核实 s4_st5 "…Nope." 后画面/字幕是否给出结论；若没有，s4_st5 改 "…Nope. Money doesn't stink."（+3 词，窗口 8 秒够） | a |
| s4_st2 | 整镜 0–15 秒；句位未提供 | N1/N2·代词先行词 | 记录 | ① 故事 | B01，L36：His son… Dad held a coin up to his nose 中 his 可顺接 Dad，也可指儿子；下一镜 Riley 自己闻钱不能消除故事里的歧义。 | 便宜：后半改 His son called it gross — so Dad made him sniff a coin: “Smell anything?” 明确是让儿子闻钱，保留下一镜 Nope。 | b |
| s3_st4 | 整镜 0–16 秒；句位未提供 | N2/N3/R·猜错动机 | 记录 | ① 故事 | B02，L25：No clue 已表明不懂，Sounds like left? 仍暗示词音或词义提供了 left 的依据；问号缓和了自信，却未消掉旧 I165 的牵强处。 | 便宜：Okay. Straight… then 'dextram.' No clue. Left, maybe? 后接 L30 Left. Definitely left. 的升级仍成立。 | b |
| s8_st10 | 整镜 0–8 秒；句位未提供 | N1/N2/R·指代 | 记录 | ① 故事 | B03，L49–50：钱已在门房袋里，The smallest coin they've got 的 they 未明说指罗马人，第一耳也可能指浴场人员的钱；并非语法错误。 | 便宜：Cover charge? One tiny coin. 不依赖可见的钱或额外手势，也保留现代入场费比喻。 | b |
| s7_st7 | 整镜 0–12 秒；句位未提供 | N1/N2/N4·生造搭配 | 记录 | ① 故事 | B04，L118–119：画面说明是交叉绳网，Rope springs 听起来像一种专名或绳制弹簧；与 Air conditioning 的明确反讽相比，类比意图不够立即。 | 便宜：Straw mattress. Ropes underneath. Very… rustic. 保留简短房间点评与收尾笑点。 | b |
| s8_st1 | 整镜 0–16 秒；句位未提供 | N2/N4/R·讲解腔 | 记录 | ① 故事 | B05，L47：Temple of Isis、Pompeii's two o'clock alarm、at two 三项连续解释，two 重复；英语通顺，但像背好的转场解说，旧 I166 仍在。 | 便宜：Hear that? That's the Temple of Isis. Guess it's two o'clock! Time for the baths. 把既有知识化成现场反应，不新增专名。 | b |
| s7_st2 | 整镜 0–17 秒，末句 | N1/N2·时态 | 记录 | ① 故事 | lines.md L125 "Two thousand years from now, people will still read it."：这里讲的是持续到两千年后的状态，母语者更常说 "will still be reading it"；现在的说法不算错，但收尾句听着偏平。两位审稿人都判了自然 | 便宜：改 "Two thousand years from now, people will still be reading it."（加 1 词；17 秒窗口足够，不压语速）。如果严格要求不加词，可以保留原句 | judge |
| s5_st7 → s7_st1 | 整镜分别 0–11、0–9 秒 | N3·开场任务编号（关闭 a 的 s5_st7 存疑与 b 的 B06） | 记录 | — | s1_st2 prompt.txt L19、filming.json L38、story.md L21 都写着 Mission one = 天黑前找床，Mission two = 尝 garum，budget 摊在手心。L94 "Mission two: done. Now… a bed." 和 L122 Bed→Garum→Budget 的顺序都与开场一致 | 不用改，结论：已核实、关闭 | judge |
| s5_st7 | — | N3 回收 | 存疑 | ① 故事 | "Mission two: done. Now… a bed." 本范围内看不到 Mission one；"Now… a bed" 把床当下一目标但 s7_st1 的清单顺序是 Bed→Garum | 存疑：核实 s1_st2 台词是否列了三个目标以及顺序 | a |
| s5_st7→s7_st1 | 整镜分别 0–11、0–9 秒 | N3/R·开场任务编号 | 存疑 | ① 故事 | B06，L94 有 Mission two，L122 有 Bed/Garum/Budget；lines.md 从 s2 开始，没有开场 Mission one/two 原话。changes.md L101 声称 s1 已铺垫，不能当亲自盲审的证据。 | 便宜：由允许看开场的人核对编号与任务内容；若吻合可直接关闭。若未铺垫，把 Mission two: done. 改为 Garum: tried.，Now… a bed. 保留。 | b |
