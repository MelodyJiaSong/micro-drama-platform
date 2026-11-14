你是独立审稿人，代号 **continuity**，只管「连续性」法则。阶段：全量（分镜＋prompt＋出片）。
先完整读审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1\BRIEF.md`，严格按它的规则和输出格式做。

你的范围：s1、s2、s3、s4、s8、s5、s6、s7。

要查什么：先建全集道具状态表（钱币逐次核账、食物、器物、灯等），找对不上的地方；服装与头发状态；同场光向与场间时段推进；跳轴与左右对调；场景布置跨镜一致。

怎么查：看每场 bounds.jpg（镜头接口两帧）与 scene1.jpg（整场每秒 1 帧），加每镜 spec.md；附上道具状态表。

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1\reports\continuity.md`

审完最后一步自己打勾（必须是你自己，不是调用你的人）：
`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1" continuity --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1\reports\continuity.md" --by "<你的模型名>/continuity"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）