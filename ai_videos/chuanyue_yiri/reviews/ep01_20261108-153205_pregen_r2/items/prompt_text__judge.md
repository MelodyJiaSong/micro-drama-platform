你是裁决人 **prompt_text__judge**（claude · claude-opus-5-5），裁「Prompt 文本」审稿项 prompt_text 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reconcile\prompt_text.md`。

## 两份报告
- a 位（claude-sonnet-5-5/prompt_text__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\prompt_text__a.md`
- b 位（gpt-6.1-sol/prompt_text__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\prompt_text__b.md`

## 要裁的维度
- **T4**（分歧）图文一致：a 2 分（首帧抽看大体一致：s2_st5 太阳在画右上方屋顶后、画左墙面暖金，与光线行一致；s3_st7 托板、陶碗、一摞面包、缺一瓣面包与文字一致；s5_st3 攥拳的是离镜头近的左手；s6_st3 画右驴车车尾、街尽头无城门；s7_st3 头在画左、右侧朝下、左手捏毯子边。小瑕疵：s8_st1 光向、s5_st4 鱼露罐形状、s8_st5 油瓶大小与瓶塞（见问题 6、7、2）。）；b 1 分（s3/st2 首帧左后方有炉口和两座磨，但文字与 overhead 是从店里拍街外的 Riley；s4/st1 首帧仍为宽大池；s8/st9 刮具悬在胸前而文字要求第 0 秒已贴小臂。见 B01–B03。）
- **T6**（分歧）参考清单：a 2 分（脚本比对 58 镜 manifest.refs 的 tag 序列与 prompt「参考」行完全一致、文件全部存在、除首帧模板句外每个 key 在正文至少用到 2 次，无多余参考；顺序统一为首帧、俯视图、三视图、道具、场景、音频。小瑕疵：s4_st2、s4_st5、s5_st5 正文写「从布包后面伸进口袋」「布包挂在腰带左前侧（在画面下缘外）」，但没挂 p3_面包布包（画外，影响小）。）；b 1 分（58 份 manifest 与 prompts.json 顺序、源图哈希均对齐，最多 8 张图；但 s8/st5、st9、st6 的首帧 prompt:L2 只列 c1、bg9、p3，未接入现行 c7、p4、p5。门厅 bg8 的用法也未收窄。见 B04、B09。）
- **T7**（抽查）长度与重点：a 2 分（编译后 prompt 2000–4644 字（`wc` 字符数），25/58 镜超过 3500 字，s6_st1/2/3 为 4644/4544/4407 字，逼近「超过 5000 字拒绝编译」的上限，而 prompts-seedance.md 写 2.5 实测可用约 1000–2000 字；关键动作排在参考用法、人物、本场、场景（约 1500–2000 字）之后；s5_st13、s7_st2、s8_st2 动作节拍 10 个以上。没有一镜越线，所以不打 1。）；b 2 分（58 条资料包文本按实际字符数计为 1997–4644，中位数 3392.5，全部低于本地 prompts-rules.md 的 5000 字门槛；最长 s6/st2 为 4644 字，「画面」到第 2292 个字符才开始。节拍均有时间段；参考说明、外观、完整动作复述与节拍重复较多，宜精简，未发现超长硬阻断。）

## 全部评分维度
- **T1** 自相矛盾：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致
- **T2** 否定句：正文里没有「没有 X」「看不到 X」这类会招来 X 的否定句
- **T3** 过期描述：人物、场景、道具描述是现行版本（发色、造型、卡片）
- **T4** 图文一致：文字和挂的首帧、站位图、场景图一致
- **T5** 混入别镜：「本场」「场景」行没有把别的镜头的内容带进来
- **T6** 参考清单：参考图齐全、顺序与用法说明对得上，没有多余或缺失
- **T7** 长度与重点：prompt 不超长，关键动作写在前面、写得清楚

评分（0–3 分）：
- **0**：没查或查不了（必须说明原因）
- **1**：有问题（问题表里要有对应条目）
- **2**：基本没问题，有小瑕疵
- **3**：没问题
- 证据规则：打 2 或 3 分必须写证据：指到镜头、秒数、图上位置、文件行或计算数字；没有证据的高分按「没查」处理，打不了勾。（证据至少 8 个字）
- 分歧：两位审稿人同一维度分数相差 ≥2，或一人 ≤1、另一人 ≥2，就是分歧，交裁决人。
- 抽查：两人都打 ≥2 的维度，裁决人每个审稿项随机抽 2 维复核证据，专抓两个模型共同的盲点。

## 规则
- 分歧维度：回到材料本身核两人的证据，谁的证据站得住；抽查维度：专门找两个模型可能**共同**漏掉的问题，不因两人都给高分就放过。
- 每个要裁的维度在报告「## 裁决」写一行：`- <编号> <最终分 0–3> 理由：<引用证据：镜头·秒数·图上位置·文件行>`（理由至少 8 个字）。
- 发现两人都漏的问题，可以加问题表（同审稿报告的表头，含「严重度」列）。只读，不改被审材料。

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\prompt_text__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2" prompt_text --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\prompt_text__judge.md" --by "<你的模型名>/prompt_text__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）