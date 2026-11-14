# 审稿项 role_c1（角色立场·Riley · 出片前（故事＋分镜＋prompt＋首帧/故事板））

范围：s1、s2、s3、s4、s8、s5、s6、s7。双审：每位拿自己的任务书、全新上下文、互不看报告；两人都打勾后工具自动对比，分歧与抽查交裁决人。

## a 位 · claude · claude-opus-5-5
- 任务书：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-141331_pregen_r2\items\role_c1__a.md`
- 报告：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-141331_pregen_r2\reports\role_c1__a.md`
- 打勾：`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-141331_pregen_r2" role_c1 --slot a --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-141331_pregen_r2\reports\role_c1__a.md" --by "claude-opus-5-5/role_c1__a"`

## 评分维度
- **V1** 语言：我说的话（措辞、长短、语种、音量）面对此刻这个人合不合适；对方听不懂我的语言时，他能不能明白我要什么
- **V2** 肢体：我的手势、姿态、和对方的距离，合不合我的身份、对方的身份和这个场合
- **V3** 表情：我的表情和强度合不合此刻的处境；不过演、不面无表情
- **V4** 视线：我看谁、什么时候看；被人问话、递东西时我会看着对方
- **V5** 回应：别人对我说话、做动作时，我会怎么回应、多快；分镜写的回应是不是此刻的我会给的
- **V6** 动机：我做的每件事我自己知道为什么；只因为剧情需要的举动判 ✗，作者写的心理说明不算数
- **V7** 跨集一致：跨集一致：和行为档案（人物目录 behavior.md）、前几集的我对照——说话方式、口头禅、对陌生人的态度、肢体习惯、表情分寸、不会做的事，这一集有没有变；变了要有这一集里看得见的原因，没有原因判 ✗。审完在报告末尾写「## 行为档案增补」：这一集新立住的行为，每条带镜头编号
- **R** 复核上一轮：previous.md 里本类别的每个问题（I 编号），逐条写是否已改好；在「## 评分表」写一行 `- R <分> 证据：…`