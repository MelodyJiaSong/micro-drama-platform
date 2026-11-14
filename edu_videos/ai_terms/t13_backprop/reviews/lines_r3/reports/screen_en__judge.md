# screen_en__judge（claude-opus-5-5），第 3 轮（末轮）

核对依据：`materials/screen_en.md` 与截图 s0_l03、s4_l30、s4_l33、s5_l40；包装卡文字按实际渲染链核对：`tools/edu_package.py` card_data（agenda 卡取 `_shared/package.json` 的 agenda_title「In this episode」、prereq_title「HELPFUL TO KNOW」，以及本期 `t13_backprop/package.json` 的 prereq「Neural networks (last episode)」和 prereq_hint「Not required — covered in a sentence」）与 `edu_videos/_shared/package/template.html`（第 143–145 行 agenda 版式，第 179 行片尾「Next · Overfitting」）。材料中 agenda 末行的「Prereqs: 」是 `tools/edu_review.py` 的 card_texts 生成材料时自己加的前缀，卡面上没有这几个字。

## 裁决

- P4 1 理由：两位审稿人的证据只有一半成立。agenda 的「Prereqs」不成立，卡上印的是眉题「HELPFUL TO KNOW」加「Neural networks (last episode)」，没有 Prereqs，a 和 b 都被材料的标注前缀误导了。l03「One at a time? Never finishes」成立：这是从严的冷开场，「Never finishes」是一个第三人称单数动词，但前面只有问句「One at a time?」，找不到主语（"one at a time" 本身不是会 finish 的东西）。它也不是英语里现成的省略说法，读着像半句话。两位审稿人本轮各自独立指出主语缺失，a 只是顾及上轮裁决才降为存疑。按「冷开场有一点别扭就必改、末轮不放宽」，维持必改。定稿写法：l03 h1 改为「One at a time? Takes forever」（6 词，标题不超 6 词；红色部分为「Takes forever」），右侧「9 tested」不动。「Takes forever」是口语里现成的省略句，保留了口播「You'd never finish」的力度，也接得上 l32「over 30 years」。
- P6 2 理由：l18–l28 的图表超限，两人都给了可执行的保留 / 隐藏清单，字数都在 9 词以内，所以不判 1。但有三处缺陷，所以不给 3。一是两人对 agenda 的改写「Last time: neural networks」针对的「Prereqs:」卡上并不存在，改写落空；真正超限的 agenda 提示行（见补充问题）两人都没给改写。二是 b 对 l03 的改写「One by one? Impossible」用「Impossible」把口播「never finish」说重了，属于屏幕新增断言。三是 a 的 l20 改写自相矛盾：先说隐藏「Guess 29」标签，清单里又保留「Guess」。b 自评 3 分偏高。
- P3 2 理由：章名在 agenda、c_problem / c_analogy / c_experiment / c_real 章节卡和页眉之间是一致的（「Too many knobs to try」「Working backward」「A small experiment」「From 1986 to today」）。但 a 指出的同一方法多名问题成立：l30 卡片页签是「ONE BY ONE」，紧接着 l31–l34 的对比行改成「Nudge one by one」，两屏都是和「Backpropagation」并列的同一组对照，叫法却变了；b 给 3 分漏了这一点。另外 s4_l33 截图里，脚注「1 s per run: ≈ 31.7 years per step」紧贴在 Backpropagation 行下面，容易被读成反向传播要 31.7 年（a 已提出，成立）。两处都是建议级。定稿写法：l31–l34 对比行标签「Nudge one by one」→「One by one」；脚注只在 l32 显示，l33 起隐藏（l34 已经不显示，只需提前一句）。

## 补充问题

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| agenda | P1 | 必改 | 卡面实际文字：「In this episode」（h2 72px）／01–04 四行章名／眉题「HELPFUL TO KNOW」／「Neural networks (last episode)」／提示行「Not required — covered in a sentence」 | 这是从严的串场卡。材料只列了四行章名和带前缀的 prereq，漏了卡标题和提示行，所以两人只数到 19 词。按实际卡面计数（编号、眉题豁免）：3 + 14 + 4 + 6 = 27 词，超过每屏 22 词的硬上限。提示行的信息与眉题「HELPFUL TO KNOW」重复，l05 口播又马上用一句话回顾了神经网络，删掉它不损失信息。 | 删去提示行：把本期 `package.json` 里 en 的 prereq_hint 置为 ""。定稿卡面：「In this episode」／「01 · Too many knobs to try」「02 · Working backward」「03 · A small experiment」「04 · From 1986 to today」／「HELPFUL TO KNOW」「Neural networks (last episode)」，共 21 词，4 块以内。 |

## 驳回

- agenda（a：P4/P3/R 必改「Prereqs: Neural networks (last episode)」→「Last time: neural networks」；b：P2/P4 必改，改写相同）：卡面上没有「Prereqs」。这是 edu_review.py 生成材料时加的标签，实际眉题是 `_shared/package.json` 的 prereq_title「HELPFUL TO KNOW」，下面接「Neural networks (last episode)」，读来自然，也和 l05「Last time…」一致。上轮 I1/I2 实际已经解决，a 的 R 行判「未解决」不成立。若在「HELPFUL TO KNOW」下再写「Last time:」，会叠出两层引导语。
- outro（a、b：存疑「若无 Next 标签则改 Next: Overfitting」）：template.html 第 179 行固定输出「Next · Overfitting」（next_label + name，bilingual_cards 为 false，不带中文小字），标签确实存在。按改写再加「Next:」会变成重复标签。包装卡没有截图、版式和时长没法核，这部分仍属 P5 的存疑，不在本裁决范围内。
- l03（b 改写「One by one? Impossible」）：「Impossible」比口播「You'd never finish」说得更重，等于屏幕新增断言；「One by one」也和本句口播「one at a time」不一致。必改维持，按裁决给的「One at a time? Takes forever」执行。
- l03（a 可选改写「One at a time? Never done」）：「Never done」容易被读成「从来没人这么做过」，有歧义，不采用。
