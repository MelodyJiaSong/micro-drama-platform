# voice_en__judge — English narration (native ear, blind) 裁决（第 2 轮）

核对依据：材料 `materials/voice_en.md`、讲稿 `script.en.md`、`timeline.en.json`、`audio/en/`（空目录）、`tools/edu_video.py` 的估算逻辑、`scenes/data.py` 断言、`previous.md` I60–I77。

关键事实：材料里的时长来自估算时间轴（`timeline.en.json` 标了 `"estimated": true`，`audio/en/` 里没有配音）。估算公式是「词数 ÷ 2.6 词/秒」，但 `words_en()` 会把念出来的数字词并成一个数字记号：l34「That's a hundred and seventy-five billion knobs」算成 `that's / 175 / billion / knobs` 4 个词，得出 1.5s；l33 算成 11 个词，得出 4.2s。按实际要念的词数（l33 约 17 词，l34 8 词）估，应约 6.5s / 3.1s。两位审稿人在 V3、V5 上因「4.2s / 1.5s 太快」扣的分，扣的是估算工具的产物，不是文字或配音缺陷。

## 裁决
- V3 2 理由：b 打 1 分的两条依据都站不住。l33 的 4.2s、l34 的 1.5s 是估算时间轴把数字词并成「175」来计数造成的，实念约 6.5s / 3.1s。l29 的「朋友手里有同一台机器」已由 l28「The machine itself hasn't changed one bit」交代，上一轮裁决也判了不采纳。剩下的小瑕疵在 l33：一句里同时有年份、公司、型号、数字，信息偏密，不过 l34 紧接着把数字再说一遍，起到了补救作用，所以给 2。
- V5 2 理由：a 的判断成立，b 的扣分依据是估算时长。全片是同一个温和、不端着的叙述者（l12「Nobody types that in」、l35「no eating, no sleeping」），句长有长有短（l07 只有 5 个词，l18 两句）。真实节奏要等配音出来、经 qa 实测才能确认，所以不给 3。
- R 2 理由：I60、I62–I66、I68、I74–I76 已解决。I61 只解决了一半：l14 只把「illustration」换掉了，「made-up / just for this example / not real receipts」三层同义说明还在，b 说得对，仍是建议级。I67、I72、I73、I77 不采纳的理由成立。I69–I71 不改文字是合理的，时长等配音后复核。只剩一条建议级问题，不到 1 分。
- V2 2 理由：（抽查）l01→l04 的冷开场、l39 回扣 l01、l24→l26 的衔接都自然。但两人都漏了一处：outro 里 l42「But what does "the right positions" actually mean?」和 l43 后半句「So how do you tell a good setting from a bad one?」问的是同一个问题，三个问句连着说。这是严格项，有一点别扭也按必改处理（见补充问题）。
- V1 2 理由：（抽查）同意两人的判断。l05、l19、l28、l29 都像在跟人说话；l16「Draw the model's guesses」略书面。另外 l22「nudge the base fare to ten dollars twenty」少了 up，念起来缺方向感，只算记录级。

## 补充问题
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l43 | V2, V4 | 必改 | Remember those little vertical lines, some long, some short? So how do you tell a good setting from a bad one? | 严格项（outro）。l42 刚问过「the right positions 是什么意思」，l43 后半句把同一个问题换个说法又问一遍，l42–l43 连着三个问号，到 l44 时听起来在原地打转。竖线这个回扣应该当作线索抛出来，不该再接一个问题。（这句是上一轮 I76 的改写，当时只修了语序，没顾及 l31 删掉之后 l42 紧挨着 l43。） | Remember those little vertical lines, some long, some short? They're the clue. |
| l33–l34 | V3, V5 | 记录 | （估算时长 4.2s / 1.5s） | 这不是文字问题。估算时长偏短，是因为 `tools/edu_video.py` 的 `words_en()` 把「a hundred and seventy-five billion」「G P T three」并成数字记号再计数。上一轮作者对 I70 的说明「估算时间轴按显示文本算」也不准确，实际是按念法文本算、但数字被合并了。s5.html 的计数动画卡在这条估算轴上。配音后重跑 timeline，用 qa 实测语速复核；如果要改估算器，属于工具修复，不在本项范围。 | （文字不改；配音后重跑 timeline 复核） |
| l27–l28 | V4 | 建议 | …comes down to where those two knobs are set. / …The only thing that's different is where the knobs are set. | 相邻两句都用「where the knobs are set」收尾，第二遍听不出新信息。 | l28: The machine itself hasn't changed one bit. Only the knob settings have. |
| l22 | V1 | 记录 | and nudge the base fare to ten dollars twenty | 「nudge … to」没说方向，口语里一般说「nudge … up to」。 | Back the per-kilometer knob off to about two fifty, and nudge the base up to ten dollars twenty. |

## 驳回
- l33、l34（b，必改，「Retain wording; extend the allotted time」）：时长来自估算时间轴把数字词合并计数，并没有证明配音或文字有缺陷。降为记录，配音后用 qa 实测复核（见补充问题）。
- l33–l34（a，合并改写「That's that many knobs.」）：丢掉了数字落在「旋钮」上的那一下，还是个碎片句，比原句差。上一轮 I71、I72 已因同样理由判过不采纳。
- l35（a，「fifty-five hundred years」）：「five and a half thousand」是地道英语（英国、澳洲常用，美国人也听得懂），和屏上「≈ 5,545 years」也对得上，不算缺陷。
- l17（a，改写）：改写比原句长，违反 V6。原句的「that line」紧接 l16 的「a straight line」，听一遍能对上。
- l29（b，建议）：上一轮裁决已判不采纳。l28 加上 l12、l37「people decide how the machine does its math」已经交代机器是人设计的、没有变；改写还丢了「scrap of paper」这个画面。
