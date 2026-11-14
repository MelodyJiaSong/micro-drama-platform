# voice_en__judge 裁决（lines_r3，最后一轮）

## 裁决
- V1 1 理由：l09「For each knob, which way to turn and how far is its slope.」把疑问式从句硬当主语，耳朵要等到「is its slope」才回头重解析，a 自己在逐句表也判它 a bit off，只给「小瑕疵」偏宽；l25「For A, the knob is two: twelve.」冒号念不出来，乘法这一步靠听众自己补。两句都在讲核心机制，维持 b 的 1 分，两句均为必改，定稿见文末。
- V2 2 理由：b 扣分依据 l05「a neural network is layers of small units」站不住，这是口语讲解里很常见的说法（"a network is just layers of…"），不算 a bit off，驳回；冷开场 l01-l04（「The real trick?」呼应 l10「The obvious way?」）、l06 单句预告、l34→l35「So where does this come from?」等过渡都顺。a 指出的 l26 衔接问题归 V3 处理。维持 a 的 2 分。
- V3 1 理由：l26「Each unit then does the same for its own two knobs.」紧跟 l24-l25 的「error × knob」，耳朵最自然把「the same」理解成再乘旋钮，而真正要说的是 l22 的「error × input」，这是核心机制上的误导；l23 让听众把「six, four, one」和「thirty-six, twenty-four and six」两串数在脑子里配对；l25 缺乘法。维持 b 的 1 分；l23、l25、l26 定稿见文末。
- R 1 理由：a 判 3 分说「No new problems introduced by the fixes」，但 l09 按 I82/I83 改完后出现了疑问式从句当主语的新问题（a 自己在 V1 也标了 l09）；I95/I96 的 l23 两串数仍需配对，只是部分解决；I100 的 l26 两位审稿人本轮独立重报，作者「复用 l22 规则」的不改理由不成立。I78 l01 作者按上轮裁决不改，理由成立。维持 b 的 1 分。
- V5 2 理由：抽查同意 2 分。声音整体温和统一，l11「For a single step.」/l32「For one step.」短句收尾有节奏；两人共同漏了 l27「so all turn down」省掉主语、念起来像电报（见补充问题），另 l23（8.1s）念完数字列表气口偏紧，随 l23 定稿一并缓解。
- V6 2 理由：抽查不同意 b 的 3 分。b 声称所有改写都不长于原句，但 l22 改写 18 词长于原句 17 词，l09 改写丢掉了「how far」（幅度），还破坏了与 l02/l42「which way… and how far」的呼应；a 的 l33 改写（14 词对 11 词）和 l40 改写也比原句长。两人都有小瑕疵，统一给 2 分。

## 补充问题
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l27 | V1/V5 | 建议 | The guess was high, so all turn down, some more than others. | 「so all turn down」省掉主语，像图注缩写，两位审稿人逐句表里都自然补成「they all」却没有报出来。 | One trip back, and all seven knobs have a number. We guessed high, so they all turn down, some more than others. |
| l20/l28 | V3 | 记录 | …and guesses: twenty-nine yuan. | 英语听众对「yuan」不熟，TTS 念法可能被听成别的词；后面 l21、l28 都没带单位，影响不大。只记录，不要求改（如果要改，得和画面同步）。 | （可选）…and guesses: twenty-nine. |

## 驳回
- l01（b，必改）：「billions of knobs, some hundreds of billions」承接前半句的省略说法是正常口语，上轮裁决已经这么判过，b 本轮没有拿出新证据；就算有人把「some」听成「大约」，意思也没错。维持不改。
- l05（b，必改）：「a neural network is layers of small units」是常见讲解口语，不算 a bit off；改成「has layers」反而弱化了「网络就是层」这层意思。不改。
- l09（b 改写）：「how a nudge changes the error—up or down」丢掉了「how far」（幅度），也破坏了与 l02/l42 的呼应。不采纳 b 的写法，用文末定稿。
- l22（b，建议）：改写比原句长，原句经上轮修改后已经能听懂。不改。
- l33（a，建议）：前面刚说「about two runs」，耳朵会自然把「three」接成「三次运行」，画面上也有「≈ 3 runs' worth」；a 的改写反复用「runs' worth」，比原句长 3 词，更啰嗦。不改。
- l40（a，建议）：第二句「Underneath, it's backpropagation」已经把这个新术语挂到本集主题上了，加「called」只多一个词，没有实际收益。不改。
- l26（a 改写「works out blame… the same way」）：仍然留着「the same way」，指代问题没解决。不采纳，用文末定稿。
- l23（b 改写）：删掉了「Bigger input, bigger blame.」，而这一句两位审稿人都认为有效。不采纳，用文末定稿。

## 维持的必改（定稿写法，可原样替换）
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l09 | V1/V3 | 必改 | For each knob, which way to turn and how far is its slope. All the slopes together are the gradient. | 疑问式从句当主语，耳朵要回头重解析。 | Each knob's slope tells you which way to turn, and how far. All the slopes together are the gradient. |
| l23 | V3/V5 | 必改 | The inputs are six, four, and for the seventh knob, one. So the blame is thirty-six, twenty-four and six. Bigger input, bigger blame. | 两串数字要在脑子里配对，「six」一句里身兼数职。 | So: six times six, thirty-six. Six times four, twenty-four. And the seventh knob's input is one, so six. Bigger input, bigger blame. |
| l25 | V1/V3 | 必改 | For A, the knob is two: twelve. For B, it's one: six. | 冒号念不出来，听众听不到乘法这一步。 | For A, the error times two: twelve. For B, times one: six. |
| l26 | V3 | 必改 | Each unit then does the same for its own two knobs. | 「the same」紧跟「error × knob」，会误导成再乘旋钮。 | For their own two knobs, it's error times input again. |
