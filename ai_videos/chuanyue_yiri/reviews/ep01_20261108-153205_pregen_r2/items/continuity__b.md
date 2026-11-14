你是独立审稿人 **continuity__b**（b 位 · codex · gpt-6.1-sol），只管「连续性」这一类。阶段：出片前（故事＋分镜＋prompt＋首帧/故事板）。
先完整读审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\BRIEF.md`，严格按它的规则和报告格式做。
同一项还有另一位审稿人（a 位，另一个模型）独立审；**不要读它的报告**，也不要读 reconcile/ 下的文件。

## 这一类是什么
跨镜头、跨场的一致：道具状态、钱的账、服装发型、光的方向、站位，前一镜结束的样子和下一镜开始的样子接得上。

想解决的问题：单镜看都对、连起来就穿帮：钱越花越多、油灯换了四种样子、头发湿了又干、两人左右对调跳轴。

为什么由这类模型审：跨镜头记账（道具、钱、服装、光向、站位）+ 看图核对

## 范围
s2、s3、s4、s8、s5、s6、s7

## 材料
- 总索引 `materials/index.md`；每镜 `materials/shots/<场>_<镜>/spec.md`（及拼图）；全集台词 `materials/lines.md`。
- 集目录、bible、故事稿、人物卡、场景卡路径见 BRIEF.md「材料」。
- 上一轮问题清单 `previous.md`、这轮改动 `changes.md`：评分表里 R 一行逐条复核。

## 要查什么
先建全集道具状态表（钱币逐次核账、食物、器物、灯等），找对不上的地方；服装与头发状态；同场光向与场间时段推进；跳轴与左右对调；场景布置跨镜一致。

## 怎么查
看每场 bounds.jpg（镜头接口两帧）与 scene1.jpg（整场每秒 1 帧），加每镜 spec.md；附上道具状态表。

## 审法（按步骤做）
1. 建一张全范围的道具 / 钱 / 服装 / 光向台账（每镜一行）
2. 相邻镜头比对结束与开始的状态
3. 跨场核对台词里引用的前事
4. 台账附在报告里

## 评分维度（报告「## 评分表」里每维一行：`- <编号> <0–3> 证据：…`）
- **K1** 道具状态表：逐镜列出每件道具进、出场状态，前后接得上
- **K2** 钱账：每次付钱前后的枚数和种类，全集账平
- **K3** 服装与发型：衣服、腰带、布包、头发干湿与发型，镜与镜一致
- **K4** 光与时间：光向、时段、天色随时间推进合理，同场一致
- **K5** 站位接续：上一镜结束的位置、朝向接下一镜开始
- **K6** 环境接续：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现
- **K7** 跨场引用：台词或画面提到前面的事（面包、方向、钱），前面确实发生过
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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\continuity__b.md`

## 最后一步（Codex 审稿位）
Codex 沙箱只能看到工作区，python 不在里面，**你不用、也不要运行 tick**。只要：
1. 把报告写到 `C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\continuity__b.md`；
2. 在你最后的输出里单独打印一行：`REPORT WRITTEN: C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\continuity__b.md`。
调用你的人会凭 `codex exec` 的运行日志代为登记（日志里必须有这一行，且晚于派单时间），不会替你写或改报告。
（只有在沙箱外、能直接运行 python 时才可以自己打勾：`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2" continuity --slot b --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\continuity__b.md" --by "gpt-6.1-sol/continuity__b"`；找不到 `python` 用 `C:/Users/light/AppData/Local/Programs/Python/Python311/python.exe`。）
- 你在 Codex 里跑（`codex exec` 跑这份任务书）。