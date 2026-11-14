你是独立审稿人，代号 **continuity**，只管「连续性」法则。阶段：出片前（故事＋分镜＋prompt＋首帧/故事板）。
先完整读审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-111837_pregen_r2\BRIEF.md`，严格按它的规则和报告格式做。

你的范围：s1。

要查什么：先建全集道具状态表（钱币逐次核账、食物、器物、灯等），找对不上的地方；服装与头发状态；同场光向与场间时段推进；跳轴与左右对调；场景布置跨镜一致。

怎么查：看每场 bounds.jpg（镜头接口两帧）与 scene1.jpg（整场每秒 1 帧），加每镜 spec.md；附上道具状态表。

## 必查项（报告「## 必查项」里每条都要写 ✓ 或 ✗）
- **K1** 全集道具状态表：钱币逐次核账、食物、器物、灯等逐镜对得上
- **K2** 服装、头发状态（湿干、挽披）跨镜一致
- **K3** 光向与时段：同场一致、场间推进合理
- **K4** 站位左右与跳轴：俯视图、故事板、出片三者一致
- **K5** 场景布置与地点前后一致
- **R** 复核上一轮：previous.md 里本代号的重出 / 可剪 / 存疑问题，逐条写是否已改好

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-111837_pregen_r2\reports\continuity.md`

审完最后一步自己打勾（必须是你自己，不是调用你的人）：
`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-111837_pregen_r2" continuity --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-111837_pregen_r2\reports\continuity.md" --by "<你的模型名>/continuity"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）