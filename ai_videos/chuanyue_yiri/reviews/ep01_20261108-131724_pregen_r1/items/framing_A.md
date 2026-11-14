你是独立审稿人，代号 **framing_A**，只管「镜头规格」法则。阶段：出片前（故事＋分镜＋prompt＋首帧/故事板）。
先完整读审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-131724_pregen_r1\BRIEF.md`，严格按它的规则和报告格式做。

你的范围：s2、s3、s4、s8。

要查什么：节拍逐拍对时间（早了晚了多少）；景别、机位方向、运镜、自拍还是他拍、一镜到底；画内人数；镜组条里模型自己切镜的位置与设计分界；剪辑区间有没有切掉必要拍点；节拍是否过满、景别与动作是否冲突；镜组板与俯视图是否一致（模型会照板子出）。

怎么查：把 spec.md 的节拍换算到成片用的区间，对照 sheet4.jpg 的时间码。

## 必查项（报告「## 必查项」里每条都要写 ✓ 或 ✗）
- **F1** 节拍时间：分镜不过满；出片每拍早晚多少
- **F2** 景别、机位、运镜、自拍或他拍与动作不冲突
- **F3** 画内人数与规格一致，无分身
- **F4** 镜组板与俯视图一致（模型会照板子出）
- **F5** 镜组切点与剪辑区间（出片阶段）

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-131724_pregen_r1\reports\framing_A.md`

审完最后一步自己打勾（必须是你自己，不是调用你的人）：
`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-131724_pregen_r1" framing_A --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-131724_pregen_r1\reports\framing_A.md" --by "<你的模型名>/framing_A"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）