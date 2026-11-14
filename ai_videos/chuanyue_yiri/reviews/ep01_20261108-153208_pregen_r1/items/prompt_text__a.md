你是独立审稿人 **prompt_text__a**（a 位 · claude · claude-sonnet-5-5），只管「Prompt 文本」这一类。阶段：出片前（故事＋分镜＋prompt＋首帧/故事板）。
先完整读审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\BRIEF.md`，严格按它的规则和报告格式做。
同一项还有另一位审稿人（b 位，另一个模型）独立审；**不要读它的报告**，也不要读 reconcile/ 下的文件。

## 这一类是什么
送给视频模型的 prompt 文字本身：有没有自相矛盾（正文要的东西负面词里禁了）、否定句、过期描述、图文不一致、别镜的内容混进来。

想解决的问题：prompt 是模型唯一看到的文字：写错一个词，模型就照着错。例如负面词禁了「木桶」、正文却要拉一桶灰浆。

为什么由这类模型审：逐行读 prompt 找自相矛盾、过期描述、图文不一致

## 范围
s1

## 材料
- 总索引 `materials/index.md`；每镜 `materials/shots/<场>_<镜>/spec.md`（及拼图）；全集台词 `materials/lines.md`。
- 集目录、bible、故事稿、人物卡、场景卡路径见 BRIEF.md「材料」。

## 要查什么
送给生成模型的文字与参考：过期与图文矛盾；物理上做不到的指令（手数、道具来源）；同一 prompt 内前后矛盾或歧义；节拍过满；镜组 prompt 的镜头切换与分界；系列硬规则与负面词是否写全、有无诱发禁区的词；规则源（bible、场景卡、考据）与 prompt 是否一致。最后给「重出前必须改」清单。

## 怎么查
读 filming.json、prompts.json、各资料包 prompt.txt 与 manifest.json、镜组板与首帧 prompt、人物卡、bible；只在需要验证时看成片。

## 审法（按步骤做）
1. 逐个读编译后的 prompt.txt 全文
2. 正文与负面词逐词交叉比对
3. 对照挂的图看图文是否一致
4. 对照卡片看描述是否过期

## 评分维度（报告「## 评分表」里每维一行：`- <编号> <0–3> 证据：…`）
- **T1** 自相矛盾：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致
- **T2** 否定句：正文里没有「没有 X」「看不到 X」这类会招来 X 的否定句
- **T3** 过期描述：人物、场景、道具描述是现行版本（发色、造型、卡片）
- **T4** 图文一致：文字和挂的首帧、站位图、场景图一致
- **T5** 混入别镜：「本场」「场景」行没有把别的镜头的内容带进来
- **T6** 参考清单：参考图齐全、顺序与用法说明对得上，没有多余或缺失
- **T7** 长度与重点：prompt 不超长，关键动作写在前面、写得清楚

评分（0–3 分）：
- **0**：没查或查不了（必须说明原因）
- **1**：有问题（问题表里要有对应条目）
- **2**：基本没问题，有小瑕疵
- **3**：没问题
- 证据规则：打 2 或 3 分必须写证据：指到镜头、秒数、图上位置、文件行或计算数字；没有证据的高分按「没查」处理，打不了勾。（证据至少 8 个字）
- 分歧：两位审稿人同一维度分数相差 ≥2，或一人 ≤1、另一人 ≥2，就是分歧，交裁决人。
- 抽查：两人都打 ≥2 的维度，裁决人每个审稿项随机抽 2 维复核证据，专抓两个模型共同的盲点。
- 打 1 分：问题表里必须有对应条目；打 0 分：写 `原因：` 说明为什么查不了。

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\prompt_text__a.md`

审完最后一步自己打勾（必须是你自己，不是调用你的人）：
`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1" prompt_text --slot a --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\prompt_text__a.md" --by "claude-sonnet-5-5/prompt_text__a"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行；`--by` 的模型名写你实际的模型。）