# 审稿项 framing（镜头规格 · 出片）

范围：s6、s7。双审：每位拿自己的任务书、全新上下文、互不看报告；两人都打勾后工具自动对比，分歧与抽查交裁决人。

## a 位 · kimi · kimi
- 任务书：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261115-165821_take_r1\items\framing__a.md`
- 报告：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261115-165821_take_r1\reports\framing__a.md`
- 打勾：`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261115-165821_take_r1" framing --slot a --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261115-165821_take_r1\reports\framing__a.md" --by "kimi/framing__a"`

## 评分维度
- **F1** 景别与人物大小：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%
- **F2** 机位与朝向：站位图的机位方向、首帧的视角、文字的「镜头」三者一致
- **F3** 画面位置：人和关键道具在画面里的左右上下位置，三处一致
- **F4** 节拍秒数：动作节拍的秒数排得下（走多远、几秒到），没有挤压
- **F5** 画内人数：写了几个人就几个人（含 extras），首帧一致
- **F6** 轴线：同一场前后镜头的左右关系不跳轴
- **F7** 一镜到底：单镜内不需要切镜；镜头运动写清且做得到
- **F8** 看点画得出来：每镜的 point（这一镜要观众看懂什么）靠哪些画面元素传达；这些元素在 prompt 里写成看得见的具体样子、首帧里就看得到（例：满街流动的水、只有石头顶面是干的）；没写 point 的镜头判 ✗