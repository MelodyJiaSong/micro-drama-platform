# voice_en__judge（claude-opus-5-5，lines_r1）

## 裁决
- V1 1 理由：多句明显不像口语：l36 用被动句 "each connection's slope is worked out in two passes"，l20 把 "weights each by a knob" 当动词用，l09 句尾悬着 "The slope."，l22 突然冒出 "blame" 又连报三个数。a 自己把 l36 列为 V1 必改，却给了 2 分，前后矛盾。b 的 1 分站得住。另外 l34 用被动句 "couldn't be trained" 收章（见补充）。
- V2 1 理由：Strict 衔接处有好几处"有点别扭"，按规则都是必改，不能给 2 分。具体：l04 "gets them all" 没说清拿到的是什么（b 指出）；l17 句尾 "So the error can flow back" 和前一句接不上，正好在出章处（a 指出）；1986 章卡不出声，l34 之后 l35 直接报年份，耳朵听不出换了话题（a 指出）；l12 "the other end" 指不到任何东西，两人都漏了。l06 是连贯的口头预告，不是念目录，这一点 b 判得对，a 说它重复 l03 不算毛病。
- V5 2 理由：大部分是同一个温和、平实的讲述声音，l10 "The obvious way?"、l14 "Six notches."、l32 "For one step." 这些短句节奏好。但有两处两人都漏了：l35-l38 连着四句都是讲义式起句（"In nineteen eighty-six," "In the paper," "They also found" "Similar methods had been"），整段没有一句短句；演示段 you / we / 祈使混用，l28 "Turn each…"、l29 "Now check it" 让观众去做旁白自己在做的事。所以维持 2 分，不升。
- V6 2 理由：b 说 24 条全有改写，核对属实；a 在逐句复述里判了 off 的 l37、l35 在问题表里没有直接改写。但两边都有改写比原句更差：a 的 l06 退回成标题式 "Today: why…"，a 的 l13 出现 "two by two" 听觉陷阱，b 的 l20 用分号、是书面腔，b 的 l22/l23 删掉 "blame"，让 l41 的收尾失去铺垫（见驳回）。达不到 3 分。

## 补充问题
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l12 | V2 | 必改 | Backpropagation works from the other end. Picture a chain of gears, with a pointer on the last one. | Strict 章节开头。上一章从没提过哪一"端"，慢办法是从各个旋钮往前推。只靠耳朵听，"the other end" 指不到任何东西，听众不知道是哪一端。 | Backpropagation starts at the answer instead. Picture a chain of gears, with a pointer on the last one. |
| l34 | V1, V2 | 必改 | Without it, billion-knob models couldn't be trained. | Strict 出章句，后面紧接不出声的 1986 章卡。"couldn't be trained" 是被动书面腔，这一句也没给耳朵任何过渡到历史的提示。 | Without it, nobody could train these models. |
| l35 | V2 | 必改 | In nineteen eighty-six, a Nature paper by Rumelhart, Hinton and Williams laid this out clearly. | Strict 章节开头，在不出声的章卡之后。一开口就是年份，接着一口气三个姓加一本期刊，耳朵听不出已经转到历史。a 只记为建议、要另加桥接句；按 strict 规则应升为必改，并给出不加长的直接替换句。 | This took off in nineteen eighty-six, with a Nature paper by Rumelhart, Hinton and Williams. |
| l28-l29 | V5 | 建议 | Turn each a small step and guess again. … Now check it the slow way. That took eight forward runs… | 人称和语气漂移：l02/l09 用 "you"，l07/l21 用 "we"，演示段又换成祈使句，像在吩咐观众动手，而动手的其实是旁白。l29 从祈使句突然跳到过去式（b 只从衔接角度提过）。演示段建议统一用 "we"。 | l28: We nudge each and guess again. Twenty-nine becomes about twenty-four. Much closer. / l29: We checked the slow way too: eight forward runs, one untouched, plus one per knob. |
| l35-l38 | V5 | 建议 | In nineteen eighty-six, … / In the paper, … / They also found … / Similar methods had been proposed earlier. | 连续两句用 "In …" 起头，四句都是同一种讲义式陈述节奏，是全片唯一一段没有短句收拍的地方。a 只笼统说了"讲课腔"，没指出起句重复。 | l36: They found each knob's slope in two passes: forward, then back from the output. / l38: Others had similar ideas earlier. This paper made them work on several layers. |
| l26 | V1, V3 | 建议 | Each unit then splits its share between its own two knobs, the same way. | 两人都指出 "splits" 不对：场景里每个旋钮得到的是 share × 各自的输入（12×5、12×1），不是把 share 一分为二。但两人的改写都不能直接用（见驳回）。不加长、直接可替换的说法是复用 l22 已经讲过的规则。 | Each unit then does the same for its own two knobs. |

## 驳回
- a · l06 改写 "Today: why trying knobs one by one is hopeless, then we watch…"："Today: why X" 是把标题念出来，正是本项要抓的目录腔，比原句差。l06 原句是连贯的口头预告，保留不改，b 的判断成立。
- a · l13 改写 "One notch on gear one turns gear two by two."："gear two by two" 听起来像"两两一组"，是听觉陷阱，gear one / gear two 编号也加重负担。应采用 b 的写法：补上 "and"，后半句说成 "Turn the second one notch"。
- a · l22 改写 "six times six, six times four, six times one"：一口气四个 "six"，耳朵分不清。还丢掉了 l23 和画面都要用的结果 36 / 24 / 6，而且偏置那一项的输入 "one" 从没介绍过。
- a · l33 改写 "Still one forward, one back: about the cost of three runs."：a 自己指出的"二对三"矛盾原样留着，没有修好。
- b · l01（必改，改写 "sometimes hundreds of billions"）：原句是正常口语。"sometimes" 反而让旋钮数听起来像会忽多忽少。降为记录；真要改，说 "and some have hundreds of billions"。
- b · l05（必改，"a neural network is layers of…"）："is layers of" 是母语里常见的口语省略，听着不别扭，不算 strict 缺陷。
- b · l20 改写 "Two knobs multiply those outputs; another adds a value. The predicted fare is twenty-nine yuan."：分号结构和 "The predicted fare is" 都是书面腔，比原句差。应采用 a 的 "The second layer multiplies each by a knob, adds one more, and guesses: twenty-nine yuan."
- b · l22 / l23 改写（把 "blame" 换成 "slope"，以及 "Bigger input, steeper slope"）：l41 的收尾 "passing the blame backward" 会失去唯一的铺垫。应该在 l22 把 blame 和 slope 挂钩一次，而不是删掉 blame。另外，"steeper" 这个坡度比喻放在旋钮上不贴切。
- b · l26 改写 "For each unit's two knobs, multiply its error by each knob's input again."：两个 "its" 指谁不清（单元还是旋钮），而且是说明书口吻，旁白不会这么说。问题本身成立，改写见补充问题 l26。
