你是裁决人 **dialogue__judge**（claude · claude-opus-5-5），裁「台词（时长与逻辑）」审稿项 dialogue 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reconcile\dialogue.md`。

## 两份报告
- a 位（claude-sonnet-5-5/dialogue__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\dialogue__a.md`
- b 位（gpt-6.1-sol/dialogue__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\dialogue__b.md`

## 要裁的维度
- **D4**（抽查）台词逻辑：a 3 分（story.md 第 21 行 Mission one=find a bed、Mission two=garum；story.md 第 27 行 Future garum 回收 Mission two；第 133 行 "Mission two: done. Now… a bed." 与第 139 行 "still no bed" 回收一致；第 31 行 earthquake twelve years ago（63→75）正确；dextram 在 s1 范围外（story 第 65–67 行 Felix 说右、Riley 猜左，后面回收），s1 不涉及）；b 3 分（story.md 场一与本轮四个有词镜头的英文相符；st2 的 Mission one＝找床、Mission two＝尝鱼露，与故事场六 Mission two: done. Now… a bed.、场八 Bed? Found. Garum? Tasted. 对得上。初始 7＋1＋1＝9 枚，场一只展示不支出；故事后续付 2 枚、1 枚小铜币、2 枚、最后 3 枚小钱＋大黄铜币，枚数归零。地震 twelve 与本剧 r01:80–81 的 63 年取值及 75−63＝12 相容；不在本类别把 62/63 年史学争议判成编号错误。）
- **D6**（抽查）听得清：a 2 分（st1/st3/st4 台词行已写「吐字清楚，海浪声/骡蹄回声/浪声压在对白下面」（prompt 第 16/17/17 行）；小瑕疵：st1 Riley 离镜头约 4.5–5m 全景低声说话，仅靠文字约束，是否听得清要出片后 faster-whisper 逐词核（previous I39 仍待核））；b 3 分（st1 prompt:16 明确“吐字清楚，海浪声压在对白下面”，st4 prompt:17 明确浪声在对白下面，st3 prompt:17 明确骡蹄回声在对白下面；声音行禁止配乐。出片前声场指令已经补齐，实际可懂度尚待新条核听，见 B02，不借用旧条转写为新条放行。）

## 全部评分维度
- **D1** 说得完：每句 ≤2.8 词/秒（停顿另算），开口前 ≥1 秒，说完后 ≥1.5 秒（用脚本算，给数字）
- **D2** 节拍对位：台词和动作节拍对得上（说到哪句做哪个动作）
- **D3** 外语与专名：拉丁语语法与出处、注音进了 prompt；专名不易读错
- **D4** 台词逻辑：编号、回收、前后说法一致（目标一二、dextram、钱数）
- **D5** 说话人：每句的说话人对，画内该张嘴的人张嘴，不说话的人不出声
- **D6** 听得清：环境声不盖过台词；悄悄话、远处的话能听清

评分（0–3 分）：
- **0**：没查或查不了（必须说明原因）
- **1**：有问题（问题表里要有对应条目）
- **2**：基本没问题，有小瑕疵
- **3**：没问题
- 证据规则：打 2 或 3 分必须写证据：指到镜头、秒数、图上位置、文件行或计算数字；没有证据的高分按「没查」处理，打不了勾。（证据至少 8 个字）
- 分歧：两位审稿人同一维度分数相差 ≥2，或一人 ≤1、另一人 ≥2，就是分歧，交裁决人。
- 抽查：两人都打 ≥2 的维度，裁决人每个审稿项随机抽 2 维复核证据，专抓两个模型共同的盲点。

## 规则
- 分歧维度：回到材料本身核两人的证据，谁的证据站得住；抽查维度：专门找两个模型可能**共同**漏掉的问题，不因两人都给高分就放过。
- 每个要裁的维度在报告「## 裁决」写一行：`- <编号> <最终分 0–3> 理由：<引用证据：镜头·秒数·图上位置·文件行>`（理由至少 8 个字）。
- 发现两人都漏的问题，可以加问题表（同审稿报告的表头，含「严重度」列）。只读，不改被审材料。

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\dialogue__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2" dialogue --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\dialogue__judge.md" --by "<你的模型名>/dialogue__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）