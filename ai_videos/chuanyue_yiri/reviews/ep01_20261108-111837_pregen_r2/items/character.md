你是独立审稿人，代号 **character**，只管「人物逻辑」法则。阶段：出片前（故事＋分镜＋prompt＋首帧/故事板）。
先完整读审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-111837_pregen_r2\BRIEF.md`，严格按它的规则和报告格式做。

你的范围：s1。

要查什么：对每个有戏的人分别代入他自己：此刻知道什么、想要什么、该看向哪里、对别人的话或动作该有什么反应。查视线、反应缺失或不合情理、动作动机、站桩不演、当地人对奇装异服陌生人的反应是否可信、主持人对观众说话的时机。

怎么查：以 sheet1.jpg 为主，需要时看 sheet4；先读故事稿与人物卡的文字设定。也指出分镜里人物动机或反应写得不清、重出还会错的地方。

## 必查项（报告「## 必查项」里每条都要写 ✓ 或 ✗）
- **C1** 每个有戏的配角此刻看向谁、在想什么（分镜写了没有，出片做到没有）
- **C2** 反应拍：对突发、怪人、台词的反应单独成拍且合乎情理
- **C3** 动机与方向：每个走、递、指、停都有理由；方向等逻辑前后一致
- **C4** 路人对主角的反应可信（不全体无视，也不抢戏）
- **C5** 主角对镜头说话的时机
- **R** 复核上一轮：previous.md 里本代号的重出 / 可剪 / 存疑问题，逐条写是否已改好

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-111837_pregen_r2\reports\character.md`

审完最后一步自己打勾（必须是你自己，不是调用你的人）：
`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-111837_pregen_r2" character --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-111837_pregen_r2\reports\character.md" --by "<你的模型名>/character"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）