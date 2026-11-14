你是独立审稿人，代号 **framing_B**，只管「镜头规格」法则。阶段：全量（分镜＋prompt＋出片）。
先完整读审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1\BRIEF.md`，严格按它的规则和输出格式做。

你的范围：s8、s5、s6、s7。

要查什么：节拍逐拍对时间（早了晚了多少）；景别、机位方向、运镜、自拍还是他拍、一镜到底；画内人数；镜组条里模型自己切镜的位置与设计分界；剪辑区间有没有切掉必要拍点；节拍是否过满、景别与动作是否冲突；镜组板与俯视图是否一致（模型会照板子出）。

怎么查：把 spec.md 的节拍换算到成片用的区间，对照 sheet4.jpg 的时间码。

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1\reports\framing_B.md`

审完最后一步自己打勾（必须是你自己，不是调用你的人）：
`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1" framing_B --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1\reports\framing_B.md" --by "<你的模型名>/framing_B"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）