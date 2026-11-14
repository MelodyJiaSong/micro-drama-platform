你是独立审稿人 **dialogue__a**（a 位 · claude · claude-sonnet-5-5），只管「台词（时长与逻辑）」这一类。阶段：出片前（故事＋分镜＋prompt＋首帧/故事板）。
先完整读审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\BRIEF.md`，严格按它的规则和报告格式做。
同一项还有另一位审稿人（b 位，另一个模型）独立审；**不要读它的报告**，也不要读 reconcile/ 下的文件。

## 这一类是什么
台词在给定时间里说得完、说完留出呼吸；拉丁语和专名读得对；台词前后逻辑（编号、回收、谁说的）一致。

想解决的问题：台词太满被挤压、节奏发急；Vespasian 被读成 Vespalian；「Mission one」编号对不上开场目标。

为什么由这类模型审：算语速与留白（脚本）、核外语与专名、台词逻辑

## 范围
s1

## 材料
- 总索引 `materials/index.md`；每镜 `materials/shots/<场>_<镜>/spec.md`（及拼图）；全集台词 `materials/lines.md`。
- 集目录、bible、故事稿、人物卡、场景卡路径见 BRIEF.md「材料」。
- 上一轮问题清单 `previous.md`、这轮改动 `changes.md`：评分表里 R 一行逐条复核。

## 要查什么
口语自然度（给改写）；节拍时间里说得完（约 2.5–2.8 词/秒）、说完后留 ≥1.5 秒；识别结果与台词不一致处判断是读错还是识别器问题；外语（如拉丁语）语法、时代口吻、发音（另用对应语言模型转写核对）；说话人是否正确；故事稿台词前后逻辑（编号、回收）。

## 怎么查
读各镜 spec.md 的台词、节拍、语音识别与区间，加故事稿；可用本机 faster-whisper 重听片段。

## 审法（按步骤做）
1. 用脚本数每句词数，按节拍时段算词/秒与留白，给出数字
2. 核外语原文出处、语法与注音
3. 核台词前后逻辑与回收

## 评分维度（报告「## 评分表」里每维一行：`- <编号> <0–3> 证据：…`）
- **D1** 说得完：每句 ≤2.8 词/秒（停顿另算），开口前 ≥1 秒，说完后 ≥1.5 秒（用脚本算，给数字）
- **D2** 节拍对位：台词和动作节拍对得上（说到哪句做哪个动作）
- **D3** 外语与专名：拉丁语语法与出处、注音进了 prompt；专名不易读错
- **D4** 台词逻辑：编号、回收、前后说法一致（目标一二、dextram、钱数）
- **D5** 说话人：每句的说话人对，画内该张嘴的人张嘴，不说话的人不出声
- **D6** 听得清：环境声不盖过台词；悄悄话、远处的话能听清
- **R** 复核上一轮：previous.md 里本类别的每个问题（I 编号），逐条写是否已改好；在「## 评分表」写一行 `- R <分> 证据：…`

评分（0–3 分）：
- **0**：没查或查不了（必须说明原因）
- **1**：有问题（问题表里要有对应条目）
- **2**：基本没问题，有小瑕疵
- **3**：没问题
- 证据规则：打 2 或 3 分必须写证据：指到镜头、秒数、图上位置、文件行或计算数字；没有证据的高分按「没查」处理，打不了勾。（证据至少 8 个字）
- 分歧：两位审稿人同一维度分数相差 ≥2，或一人 ≤1、另一人 ≥2，就是分歧，交裁决人。
- 抽查：两人都打 ≥2 的维度，裁决人每个审稿项随机抽 2 维复核证据，专抓两个模型共同的盲点。
- 打 1 分：问题表里必须有对应条目；打 0 分：写 `原因：` 说明为什么查不了。

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\dialogue__a.md`

审完最后一步自己打勾（必须是你自己，不是调用你的人）：
`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2" dialogue --slot a --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\dialogue__a.md" --by "claude-sonnet-5-5/dialogue__a"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行；`--by` 的模型名写你实际的模型。）