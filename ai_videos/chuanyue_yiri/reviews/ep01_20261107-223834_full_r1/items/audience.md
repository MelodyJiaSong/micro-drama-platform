你是独立审稿人，代号 **audience**，只管「观众」法则。阶段：全量（分镜＋prompt＋出片）。
先完整读审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1\BRIEF.md`，严格按它的规则和输出格式做。
**你是观众视角：不要读任何 spec.md、story、index 或分镜规格**，只看成片画面、听台词（审稿说明里的材料表只用成片与 scene1 拼图）。

你的范围：s1、s2、s3、s4、s8、s5、s6、s7。

要查什么：扮演第一次看的目标观众，只看画面和听台词，不读任何分镜、故事稿与规格：每段看到了什么、哪里看不懂、哪里好笑或笑点没落地、哪里拖或急、哪里出戏，看完记住了什么、想不想看下一集。

怎么查：自己从成片抽帧拼图、用 faster-whisper 转写；只用审查单里给观众的材料。

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1\reports\audience.md`

审完最后一步自己打勾（必须是你自己，不是调用你的人）：
`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1" audience --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1\reports\audience.md" --by "<你的模型名>/audience"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）