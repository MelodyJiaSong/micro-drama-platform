你是独立审稿人 **character_A__b**（b 位 · codex · gpt-6.1-sol），只管「人物逻辑」这一类。阶段：出片前（故事＋分镜＋prompt＋首帧/故事板）。
先完整读审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\BRIEF.md`，严格按它的规则和报告格式做。
同一项还有另一位审稿人（a 位，另一个模型）独立审；**不要读它的报告**，也不要读 reconcile/ 下的文件。

## 这一类是什么
每个人物此刻知道什么、想要什么、该看向谁、该怎么反应，要合乎他的身份和处境；配角的反应拍不能被吞掉。

想解决的问题：人物「不像真人」：当地人对穿裤子的外国女人毫无反应、面包师眼看她走错路却不看她、观众看不懂人物为什么这么做。

为什么由这类模型审：读长文本、讲人物动机与反应逻辑

## 范围
s2、s3、s4、s8

## 材料
- 总索引 `materials/index.md`；每镜 `materials/shots/<场>_<镜>/spec.md`（及拼图）；全集台词 `materials/lines.md`。
- 集目录、bible、故事稿、人物卡、场景卡路径见 BRIEF.md「材料」。
- 上一轮问题清单 `previous.md`、这轮改动 `changes.md`：评分表里 R 一行逐条复核。

## 要查什么
对每个有戏的人分别代入他自己：此刻知道什么、想要什么、该看向哪里、对别人的话或动作该有什么反应。查视线、反应缺失或不合情理、动作动机、站桩不演、当地人对奇装异服陌生人的反应是否可信、主持人对观众说话的时机。

## 怎么查
以 sheet1.jpg 为主，需要时看 sheet4；先读故事稿与人物卡的文字设定。也指出分镜里人物动机或反应写得不清、重出还会错的地方。

## 审法（按步骤做）
1. 为每个有戏的人物写一行「此刻知道 / 想要 / 看向」
2. 找出被吞掉或雷同的反应拍
3. 核对主持人的反应是否符合人设

## 评分维度（报告「## 评分表」里每维一行：`- <编号> <0–3> 证据：…`）
- **C1** 知道什么：每个人此刻知道什么、不知道什么，行为不越过他的认知
- **C2** 想要什么：每个人此刻的目的清楚，动作服务于目的
- **C3** 视线：每个时刻每个人看向谁，合理（不无缘无故看镜头、不无视身边的怪事）
- **C4** 反应拍：配角的反应单独占拍，不被吞掉；反应和身份、性格相符
- **C5** 主持人性格：Riley 的反应符合人设（好奇、敢试、自嘲），对当地人有回应
- **C6** 路人：路人有合理的反应且不雷同，不抢主笑点
- **C7** 动机连贯：跨镜头的情绪与动机连得上，没有突然的转变
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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\character_A__b.md`

## 最后一步（Codex 审稿位）
Codex 沙箱只能看到工作区，python 不在里面，**你不用、也不要运行 tick**。只要：
1. 把报告写到 `C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\character_A__b.md`；
2. 在你最后的输出里单独打印一行：`REPORT WRITTEN: C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\character_A__b.md`。
调用你的人会凭 `codex exec` 的运行日志代为登记（日志里必须有这一行，且晚于派单时间），不会替你写或改报告。
（只有在沙箱外、能直接运行 python 时才可以自己打勾：`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2" character_A --slot b --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\character_A__b.md" --by "gpt-6.1-sol/character_A__b"`；找不到 `python` 用 `C:/Users/light/AppData/Local/Programs/Python/Python311/python.exe`。）
- 你在 Codex 里跑（`codex exec` 跑这份任务书）。