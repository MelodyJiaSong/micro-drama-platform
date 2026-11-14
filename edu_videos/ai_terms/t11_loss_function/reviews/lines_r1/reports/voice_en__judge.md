# voice_en__judge 裁决（第 1 轮）

核对材料：`materials/voice_en.md`、`script.en.md`、`script.md`（中文对照，查出 l47、l49 的翻译来源）、`scenes/web/s3.html`（l15 的红色方块确在画面上）。

## 裁决
- V1 1 理由：严格项有句子确实不自然。l11 是章节开场，但只有两段坐标轴碎片，结尾 "The data's made up." 很生硬；l38 也是章节开场，"It's just scoring something different" 里的 it 指代不清，主语还从"被打分"变成了"打分"。按严格规则，这两条都是必改（a 判 "a bit off" 却只给建议，自相矛盾）。另外 l33 "chasing as low as it can get" 缺宾语，l49 "can't see the edges" 是中文「看不到边」的直译。b 的 1 分站得住，但它举的 l27、l28 证据不成立，见驳回。
- V2 1 理由：片尾 l47 "a loss function is a score for how wrong the model is" 把 l04 立下的 loss（分数）和 loss function（算分规则）混成一个概念，中文原句是「给错误打个分」，英文译偏了；严格项必改。l49→l50 的落点也不顺：l49 用了直译比喻，l50 "That's gradient descent" 只报了个名字，没接住上一句"往哪拧"的问题，"that's" 还连用两次。l37→l38 的章节转场靠 l38 承接，但 l38 本身不清楚。a 说"严格项无缺陷"不成立。
- V3 1 理由：l47 让观众带着错误的术语区分离开；l29 的 "ten twenty" 光听可能被理解成 1020 或者一个时刻，一句里还挤了三个数；l05 把 error 定义成"偏多远"，没有方向，l18–l19 却突然要靠正负相抵（"minus thirty cents"）；l41 "Give the right word ninety percent" 没说这个百分比是什么的百分比。b 的证据基本成立。
- V5 2 理由：整体是同一个温和的讲述者，l08、l34、l35–l36 的口吻很好。但两人都漏了一个口头禅："That's…" 收句出现了十次左右（l04、l05、l06、l14、l15、l20、l30、l35，l50 一句里就两次），节奏单调。l13–l29 的数字一段接一段，l29 又最密。
- V6 2 理由：两人的改写都不合格。a 的 l17 改写 24 词，原句 23 词；l29 改写 22 词，原句 21 词，都超过"不长于原句"的硬上限，l29 改写里的 "Score: …" 还是电报式碎片。b 的长度都合规，但 l15、l18、l27、l02 的改写比原句更差（见驳回）。两人都排出了最别扭的前 5 句。

## 补充问题
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l49 | V1, V2, V3 | 必改 | But with tons of knobs, that map gets so huge you can't see the edges. So which way do you turn to get down? | 片尾严格项。"can't see the edges" 是「地形图大得看不到边」的直译，英语母语者听来比喻不对：问题不在看不到边缘，而在于没法把整张图看全、直接找到最低点。"turn to get down" 也有点别扭。两位审稿人都判了 natural。 | But with tons of knobs, that map gets way too big to ever see whole. So which way do you turn to go downhill? |
| l04, l05, l06, l14, l15, l20, l30, l35, l50 | V5 | 建议 | That's today's topic / that's the error / that's the loss / That's this red square / That's why we square / That's the best setting / that's how it learns / That's gradient descent, and that's… | "That's…" 收句约十次，成了口头禅，听感单调。严格项 l04 保留；l50 按 b 的条目改；非严格句挑两三处换掉即可。 | l20: So we square: once everything's squared, it's all positive, and nothing cancels. / l30: It's the best setting, and the whole job of training is finding that lowest point. |

## 驳回
- b l02：不成立。"this turn beat the last one" 是很地道的口语，画面上的 "Is this turn better?" 也对得上；b 的改写 "whether turning a knob helped" 丢了"跟上一次比"的意思，反而变差。冷开场保持原句。
- b l15：改写更差。它删掉了 "That's this red square"，而 l24 "the squares are tiny" 正是靠这句建立起"红色方块＝平方误差"的画面（s3.html 里 8²=64 用 --d-bad 色标出）。保持原句。
- b l18：问题部分成立（正负号在前面没铺垫），但级别从必改降为建议。改写更差：书面腔，还删掉了 "If we skipped the squaring" 这个前提，而 l20 "That's why we square" 正是回答它的。应该在定义处改，l05 改为 "Every time the model guesses, it lands a bit too high or too low. That gap is the error."（19 词，不超过原句 19 词）。
- b l27：不成立。"X along the bottom, Y up the side" 是讲解视频的常见口语说法；b 的改写 "The axes show…" 更像讲课腔。
- b l28：判 "clearly off" 不成立。对着画面用省略式并列描述三个位置，口语里很自然，最多算记录。
- b l33：问题成立，但改写 "aims for the lowest possible score" 更书面。改为 "So training isn't chasing zero. It's just getting as low as it can."（13 词）。
- b l11：问题成立（严格项，必改），但改写删掉了坐标轴的说明，而 l12–l13 要靠它来看图。改为 "Remember those twelve made-up taxi rides? Distance along the bottom, fare up the side."（14 词，不超过原句 21 词）。
- b l50：问题成立（必改），但改写 "guides those turns" 偏书面，也没正面回答 l49 的问题。改为 "That's where gradient descent comes in, and that's next time."（10 词）。
- b l47：问题成立（必改）。可用的改写更贴近中文原意并呼应 l03："So, a loss function is how you score the model's mistakes, and lower is better."（15 词，不超过原句 17 词）。
- a 章节卡 "How big models are scored"：不成立。这是自然的章节标题，不需要改。
- a l11、a l38：级别判错。这两句是章节开场的严格项，既然判了 "a bit off"，就应该是必改，不是建议。
- a l17 改写：24 词，超过原句 23 词，违反长度上限。可改为 "Second try: four dollars to start and three fifty a kilometer. Too steep, so short rides come out low and long ones high."（23 词）。
- a l29 改写：超长 1 词，"Score: one point nine seven." 是电报式碎片。改用 b 的版本 "Ten dollars twenty to start, then two fifty-four a kilometer, gives the lowest score: one point nine seven."
