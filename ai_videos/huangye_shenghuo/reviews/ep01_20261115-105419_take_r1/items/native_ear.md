# 审稿项 native_ear（母语听感 · 出片）

范围：s1、s2、s3、s4、s5、s6、s7、s8。双审：每位拿自己的任务书、全新上下文、互不看报告；两人都打勾后工具自动对比，分歧与抽查交裁决人。

## a 位 · kimi · kimi
- 任务书：`C:\workspace\micro-drama-platform\ai_videos\huangye_shenghuo\reviews\ep01_20261115-105419_take_r1\items\native_ear__a.md`
- 报告：`C:\workspace\micro-drama-platform\ai_videos\huangye_shenghuo\reviews\ep01_20261115-105419_take_r1\reports\native_ear__a.md`
- 打勾：`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\huangye_shenghuo\reviews\ep01_20261115-105419_take_r1" native_ear --slot a --report "C:\workspace\micro-drama-platform\ai_videos\huangye_shenghuo\reviews\ep01_20261115-105419_take_r1\reports\native_ear__a.md" --by "kimi/native_ear__a"`

## 评分维度
- **N1** 自然度：逐句：母语观众听着自然 / 有点怪 / 很怪
- **N2** 别扭原因：直译句式、电报式、时态或视角、讲解腔、指代不清、生僻词
- **N3** 笑点与回收：笑点母语观众接得住；开场目标与结尾、dextram 回收得上
- **N4** 人设口吻：像一个二十多岁、亲切的旅行博主在说话，前后口吻一致
- **N5** 改写：每句「有点怪 / 很怪」都给最自然的改写（长度不限）
- **N6** 最不像真人说话的 5 句：必须列满至少 5 句并排序、各给改写；不允许「全部自然、无可列」
- **N7** 说出口测试：逐句先遮住原句、按画面说明写自己的说法，再对比原句；原句离真人随口说法越远分越低（写出差距最大的几句的两种说法）
- **N8** 修辞痕迹：自问自答、三连排比、停顿抖包袱、工整对仗、字幕 / 广告文案腔的句子数；每处都列出，像「写出来的台词」就扣分
- **N9** 处境匹配：语气、音量、精力和当时处境对得上（深夜独处、刚被赶、边嚼边说、累了一天），不像主持人对镜头念稿
- **N10** 连着读：lines.md 里同一个人相邻两镜的台词连起来读：中间被切开的地方，听着像不像同一个人在同一刻接着说话；像重新开场、重新打招呼、情绪突然换挡的，列出来并给改写（可以加一句过渡，长度不限）