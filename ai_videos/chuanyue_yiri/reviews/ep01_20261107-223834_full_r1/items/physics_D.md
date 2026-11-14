你是独立审稿人，代号 **physics_D**，只管「世界物理」法则。阶段：全量（分镜＋prompt＋出片）。
先完整读审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1\BRIEF.md`，严格按它的规则和输出格式做。

你的范围：s6、s7。

要查什么：重力与支撑（东西被谁、用哪只手托着？有没有悬空、黏在手上）；手的数量（自拍占一只手，其余动作只剩一只手）；道具守恒（凭空出现、消失、变形、数量变化）；道具交接后去向；穿模；身体变形（多手指、肢体扭曲、脸或身体溶解/半透明）；运动物理（滑步、瞬移）；火、烟、水、蒸汽、光影；画面突然溶解成另一画面。

怎么查：逐镜看 sheet4.jpg 每一格，盯手、手里的东西、脚和地面、画面边缘进出的物体；疑点用 ffmpeg 加密抽帧或放大裁切确认。对照 spec.md，也指出分镜文字本身做不到、或没交代道具来源与去向的地方。

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1\reports\physics_D.md`

审完最后一步自己打勾（必须是你自己，不是调用你的人）：
`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1" physics_D --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261107-223834_full_r1\reports\physics_D.md" --by "<你的模型名>/physics_D"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）