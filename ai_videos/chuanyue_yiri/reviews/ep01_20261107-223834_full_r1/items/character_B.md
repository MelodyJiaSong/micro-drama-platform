你是独立审稿人，代号 **character_B**，只管「人物逻辑」法则。阶段：全量（分镜＋prompt＋出片）。
先完整读审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1\BRIEF.md`，严格按它的规则和输出格式做。

你的范围：s8、s5、s6、s7。

要查什么：对每个有戏的人分别代入他自己：此刻知道什么、想要什么、该看向哪里、对别人的话或动作该有什么反应。查视线、反应缺失或不合情理、动作动机、站桩不演、当地人对奇装异服陌生人的反应是否可信、主持人对观众说话的时机。

怎么查：以 sheet1.jpg 为主，需要时看 sheet4；先读故事稿与人物卡的文字设定。也指出分镜里人物动机或反应写得不清、重出还会错的地方。

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1\reports\character_B.md`

审完最后一步自己打勾（必须是你自己，不是调用你的人）：
`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1" character_B --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1\reports\character_B.md" --by "<你的模型名>/character_B"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）