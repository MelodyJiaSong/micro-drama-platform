# voice_en__judge report (round 1)

## 裁决
- V1 1 理由：b 站得住。l43 "Those little vertical lines were some long, some short." 语序不是母语口语（母语会说 "Some were long, some were short"），a 判 natural，但 a 自己的复述也改成了 "Remember those vertical lines, some long, some short?"，等于默认这句要改；而且它在 outro（严格项），按规则是必改。l08 "how many kilometers the ride was" 只是稍显笨，记建议。其余各句是正常口语，这一点两人一致。
- V2 1 理由：b 站得住。outro 交接处 l42 已经提出问题，l43 又换个说法再问一遍，还要靠一句别扭的语序去回扣 l17 讲过的竖线，严格项里出现「有点别扭」就是必改。另外 l39 "So when the news says…" 紧接着 l40 "So a model is…"，进 outro 的交接连用两个 "So"（见补充问题）。冷开场 l01–l04 和各章交接（l13→l14、l31→l32）都没问题，两人在这点上一致。
- V3 1 理由：两人的证据都成立。b 指出 l22 "Turn it back a little" 里的 "it" 接的是 l21 的单价旋钮，后半句却同时设了两个旋钮；更糟的是起步价其实从 $10 上调到 $10.20，"turn back" 对起步价方向是反的（s3.html 里 l22 调的是 turnBoth）。a 指出 l22 "ten twenty" 和 l25 "thirty fifty" 不带单位，光听容易误听成时间或范围。都是只听一遍会卡住的地方，所以是 1 不是 2。
- V5 1 理由：b 站得住，a 没算语速。l33 有 32 个音节只给 4.2s（≈7.6 音节/秒），l34 有 12 个音节只给 1.5s（≈8 音节/秒），而邻句 l07 是 8 音节/1.9s（≈4.2），l13 是 14 音节/4.2s（≈3.3）。要么音频被赶，要么时长是按显示文本「In 2020 … 175 billion」估的、和实际念的长度对不上，而 s5.html 的 countTo 动画就卡在这两个时长上。这个问题在时长或配音，不在文字，b 的删字改写不采纳（见驳回）。
- V4 2 理由：维持 2。两人各抓到一部分（a：l34/l33、l37/l12；b：l14 三重声明），但共同漏了 "turning the knobs to the right positions" 这个说法在 l13、l31、l41 近乎原样出现三次，l30 又说一次 "turning knobs"。l26–l28 三句连着说「学到的只在两个数里」也偏松。都是轻度重复，在讲解片里有作用，仍是小瑕疵。
- V6 2 理由：从 3 降到 2。a 漏了严格项 l43，必改句没有改写；a 的 l44 改写（14 词）比原句（9 词）长，违反「不长于原句」。b 的 l33/l34 改写删了年份，还把 l34 改成 "That many knobs."，丢掉了数字和「参数＝旋钮」的对应；b 的 l22 改写仍保留没单位的 "ten twenty"。下面补了可直接替换的改写。

## 补充问题
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l43 | V1, V2 | 必改 | Those little vertical lines were some long, some short. So how do you tell whether one setting is good or bad? | 严格项（outro）语序别扭，两人给的改写都不理想：a 没列入问题表，b 的改写丢了回扣。这里要明确把观众带回 l17 的竖线。 | Remember those little vertical lines, some long, some short? So how do you tell a good setting from a bad one? |
| l22 | V3 | 必改 | Turn it back a little, to a base fare of about ten twenty and about two fifty per kilometer. | "it" 指代不清，"back" 对起步价方向相反（$10→$10.20 是往上调），两个数字又没有单位。 | Back the per-kilometer knob off to about two fifty, and nudge the base fare to ten dollars twenty. |
| l40 | V2, V5 | 必改 | So a model is a machine with knobs, and the parameters are those knobs. | 紧跟 l39 "So when the news says…"，进 outro 连用两个 "So"，听起来是口头禅（全片以 "So" 开头的句子有 9 句：l02/l04/l21/l24/l26/l30/l39/l40/l43）。这是严格交接位。 | In short, a model is a machine with knobs, and the parameters are those knobs. |
| l33–l34 | V5 | 必改 | （时长 4.2s / 1.5s） | 语速约 8 音节/秒，是邻句的两倍。先核实际音频；如果时长是按显示文本估的，就按实际念的长度重排时间轴（s5.html 的 countTo/eq 动画卡在这里）。文字不用删。 | （文字不改；改配音或时长） |
| l31 | V4 | 建议 | And "the model has learned" means the knobs are now in the right positions. | "the right positions" 在 l13、l31、l41 近乎原样说了三遍，l41 再说时已经没有新意，也让 l42 的提问显得重复。 | And "the model has learned" just means the knobs ended up set well. |

## 驳回
- b l33（删 "In twenty twenty"）：问题出在时长或配音，不在文字。年份对应屏上的出处「Brown et al. · OpenAI · 2020」，删掉反而损失信息。
- b l34（"That many knobs."）：丢了数字和「参数＝旋钮」在这个数上的落点，而 l39 的回扣要靠它；还是一个碎片句。该修时长，不该删字。
- b l29（"Give a friend those two numbers and the same calculation…"）：l28 刚说过机器没变，观众默认朋友手里是同一台机器；改写丢了 "scrap of paper" 这个画面，"the same calculation" 也偏书面。原句保留。
- b l22 改写（"Try ten twenty for the base fare…"）：修了指代，但留着没单位的 "ten twenty"，也断了和 l21 冲过头的衔接。以补充问题里的改写为准。
- a l44（"That's next time: how we score a setting, what people call a loss function."）：比原句长（违反 V6），而且原句作为下期预告本来就自然，只预告一个术语名可以接受。原句保留，降为记录。
- a l43 判 natural：不成立。理由见 V1、V2 的裁决。
