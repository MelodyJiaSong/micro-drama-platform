# voice_en__judge 裁决（lines_r1 · English narration, native ear, blind）

## 裁决
- V1 1 理由：b 的 1 分成立。a 自己的问题表里就把 l01（开场，属严格项）、l34、l39 定为必改，和它给的 2 分（基本没问题）自相矛盾。核材料：l01 "keep anything harmful below a line"（harmful 是"东西"，below a line 要的是一个量，耳朵得自己把比喻补全）；l37–l39 从 price/points 一下换成 "coefficient"，加上被动的书面句 "How hard that's penalized is the same kind of coefficient"；l34 是念出声的公式片段。必改不止一处，只能给 1。
- V2 1 理由：严格项里有好几处"有点别扭"，按规则都是必改，所以不能给 2。具体是：结尾 l42 "Next time you want it all…" 紧跟 l43 "Next time, we'll get into…"，"Next time" 连说两遍，结尾像重新开了个头（两人都发现了）；l37 "Coefficients that put a price on a rule are all over AI." 是从 Safe RLHF 转到"AI 里到处都有"的过渡句，转得生硬（a 发现）。a 举的 l17 是镜头内的普通叙述句，不是过渡句，这条不成立；b 说 l42 的 "worth" 有歧义，也不成立（见驳回）。但前两条已经够把分压到 1。
- V3 1 理由：只听一遍跟不上的地方不止一处。l26 一口气四个小数（7.75 / 8.04 / 0.29 / 3×0.1）；l23 "uphill points" 容易听成名词复数 points；l38–l39 引入 "coefficient" 却没用大白话解释。另外两人都漏了 l18：说的是 "At one point five"，但没说这是价格，而 1.5 正好也是 l25 里的篱笆半径（s3.html 里篱笆就是 `ring(1.5, …)`），同一个数字指两样东西，靠耳朵分不清。所以 V3 判 1。
- V5 2 理由：抽查后维持 2 分。旁白始终是同一个温和、亲切的声音，长短句也有交错（l12 很短，l14 较长）。但两人都没听出一个反复出现的句式：「X: Y」冒号起头，l01、l05、l12、l13、l14、l20、l23、l29、l33、l34、l40、l42 共 12 处（如 "Lagrange's idea:"、"Our job:"、"The goal:"、"Their tool was…:"、"in one line:"）。单看每句都自然，连起来听就成了口头禅，节奏单调。这条记为建议，见补充问题。
- V6 1 理由：抽查后降到 1 分。开场是严格项，可两人给 l01 的改写都把 "line" 删了（a 改成 "stay under a limit on harm"，b 改成 "set a limit on the harm they might cause"），这样 l02 的 "never cross this line" 和屏幕上的「Harm ≤ the line」就失去了指向，算不上可以直接替换的改写。b 的 l34 改写丢了 "Lagrange multiplier" 这个点题词；b 的 l37 改写 "adjustable penalties" 不准确（正则化系数在训练中并不自动调）；b 判 l06 为 clearly off，问题表里却没有这一行；a 的 l17 改写不通顺。b 给 3 分说"全部可直接替换"，不成立。

## 补充问题
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l01 | V6 | 必改 | be as helpful as you can, but keep anything harmful below a line | 开场是严格项。改 l01 时必须保住 "line"，l02 的 "never cross this line" 和屏幕上的「Harm ≤ the line」都靠它；a、b 的改写都把它删了。 | When we train an AI, we often ask for something like this: be as helpful as you can, but don't let harm cross a line. |
| l18 | V3 | 必改 | At one point five, the dot backs up a bit, but it's still outside. | 没说 1.5 是价格（λ）。之后 l25 的篱笆半径也是 "one point five"，同一个数字指两个量，只听一遍会弄混。"Raise it again" 也没给数值，而屏幕此时显示的是 2.63。 | At a price of one point five, the dot backs up a bit, but it's still outside. Raise it again, it backs up again. |
| l43 | V2 | 必改 | Next time, we'll get into gradient descent. | 结尾是严格项。和 l42 开头的 "Next time" 撞词。只改 l43 就行，l42 是点题句，应保留。 | Up next: gradient descent. |
| l05/l12/l14/l33/l34/l40 等 | V5 | 建议 | Lagrange's idea: … / Our job: … / Lagrange's way: … / The goal: … / Their tool was…: … / in one line: … | 全片 12 处「名词短语＋冒号」起句，听起来像模板。挑其中 4–5 处改成完整句即可，l05、l40 可以保留。 | l12 "Our job is to find the highest spot."；l33 "We want harm under the line, and as much help as we can get within it."；l34 "They used a Lagrange multiplier: take the helpfulness score, and subtract lambda times the harm score." |
| l16/l21/l27(b 改写) | V3 | 建议 | right out of the circle / hides inside the circle / widen the circle | 旁白里从没说过篱笆是圆形，"circle" 是凭空冒出来的；b 的 l27 改写又用了 "circle"。 | l16 "…way outside the fence."；l21 "…the dot hides back inside the fence…" |

## 驳回
- a 的 l17（V2 建议）：l17 是镜头内的普通叙述句，不是过渡句，原句口语、意思清楚（b 判 natural）。a 的改写 "So we raise the price, more the farther out the dot is." 语序别扭，比原句差。
- a 的 l34 改写 "helpfulness, minus lambda times harm"：a 自己指出的毛病是"念出来像公式"，这个改写还是在念公式，没解决问题。改用补充问题表里 l34 的写法。
- a 的 l01 改写 "stay under a limit on harm"：删掉了 "line"，和 l02 的 "this line"、屏幕上的「Harm ≤ the line」接不上了。
- b 的 l01 改写：同样删了 "line"，还丢了 "ask for something like this" 这个请求式框架，而 l02 把这两条要求称作 "different requests"，正是接着这个框架说的。
- b 的 l11（必改）：原句 "The rings are contour lines, rising toward the summit in the middle" 已经说清楚环线和高度的关系，普通观众知道地图上的等高线。这条不到必改。b 的改写还删掉了 "experiment"，而这是本章（屏幕章节卡 "A small experiment"）的框架。
- b 的 l34 改写 "They subtract lambda times the harm score from the helpfulness score."：丢了 "Lagrange multiplier"，这一章最关键的点题（Safe RLHF 用的就是本集的工具）就没了。
- b 的 l36 改写：删掉了 "Just like our mountain"，这是把 AI 例子接回山地实验的回扣，a 也列为应保留。如果担心观众对不上，可以改成 "Just like the dot on our mountain."，不该删。
- b 的 l37 改写 "adjustable penalties"：l38 的正则化系数一般是人手设定的，不会自动调，用 "adjustable" 不准确。a 的 "Prices on rules show up all over AI." 和屏幕上的「Prices on rules」一致，更好。
- b 的 l42（必改，理由 "worth" 有歧义）：l24–l29 讲的就是 shadow price，也就是"这条规则值多少"，"what's this rule really worth?" 正是回扣这一段。结尾重复 "Next time" 的问题改 l43 就能解决，不必重写 l42。
- b 的 V6 3 分理由（"All 16 lines … receive a drop-in rewrite"）：l06 被判 clearly off，问题表里却没有它；l01、l34 的改写也不能直接替换（见上）。
