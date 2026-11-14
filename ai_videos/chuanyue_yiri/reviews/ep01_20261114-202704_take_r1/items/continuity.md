# 审稿项 continuity（连续性 · 出片）

范围：s3、s4、s8、s5、s6、s7。双审：每位拿自己的任务书、全新上下文、互不看报告；两人都打勾后工具自动对比，分歧与抽查交裁决人。

## a 位 · claude · claude-opus-5-5
- 任务书：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-202704_take_r1\items\continuity__a.md`
- 报告：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-202704_take_r1\reports\continuity__a.md`
- 打勾：`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-202704_take_r1" continuity --slot a --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-202704_take_r1\reports\continuity__a.md" --by "claude-opus-5-5/continuity__a"`

## 评分维度
- **K1** 道具状态表：逐镜列出每件道具进、出场状态，前后接得上
- **K2** 钱账：每次付钱前后的枚数和种类，全集账平
- **K3** 服装与发型：衣服、腰带、布包、头发干湿与发型，镜与镜一致
- **K4** 光与时间：光向、时段、天色随时间推进合理，同场一致
- **K5** 站位接续：上一镜结束的位置、朝向接下一镜开始
- **K6** 环境接续：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现
- **K7** 跨场引用：台词或画面提到前面的事（面包、方向、钱），前面确实发生过
- **K8** 镜间接点：逐个接点（materials/junctions.md 每一条，含没有机检标记的）判：上一镜最后一拍的位置、朝向、视线、手里的东西、情绪和音量，和下一镜第 0 秒接得上；接不上时要有切的理由（跳过时间、换地点、反应插入、主观镜头）写在下一镜开头。报告里列接点表：每个接点一行，✓ 或 ✗ 加一句理由
- **K9** 视角来源：每镜是谁在拍（自拍 / 跟拍 / 架着的相机 / 主观）；同一刻里来源切换（尤其她正对着一台相机说话，下一镜换成另一台）有没有交代（拿起、放下、架好、递给），或符合本剧视角约定（bible）；和「重新开场」一起出现的一律 ✗