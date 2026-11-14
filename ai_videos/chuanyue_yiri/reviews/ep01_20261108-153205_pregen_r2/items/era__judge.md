你是裁决人 **era__judge**（claude · claude-opus-5-5），裁「时代与世界观」审稿项 era 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reconcile\era.md`。

## 两份报告
- a 位（claude-opus-5-5/era__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\era__a.md`
- b 位（gpt-6-astra/era__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\era__b.md`

## 要裁的维度
- **E4**（分歧）系列禁区：a 2 分（s2–s8 共 116 份 prompt grep「火山、维苏威、Vesuv、volcan、熔岩」，0 处命中；58 张首帧的天空里都没有烟柱或白烟，也没有冒烟的山。小瑕疵：s5_st10 首帧右下罐口有一股热气升到画面约 40% 高（z_steam510.jpg），首帧 prompt 第 4 行还是「冒着热气」；s6_st1 画左远处露出一道丘陵（z_sky61.jpg），负面词里写着「远山、丘陵」，不过那道丘陵没有冒烟，也不是画面主体。）；b 1 分（当前 58 份视频 prompt 与 58 份首帧 prompt 检索禁用火山词均为 0 命中，当前 s4_st1 无烟；但 story.md:75 仍要求黄白烟，bg2 卡:30 的种子 prompt 仍写“大火山石”，r05:206 可复制负面词仍含火山词。见 B02、B03。）
- **E1**（抽查）器物：a 2 分（s5_st13 首帧画面中部那只杯子是透明的刻花玻璃杯（z_cup513.jpg），首帧 prompt 第 7 行写的是「粗陶杯」，负面词里还有「玻璃杯」；s6_st1/st2/st5 Fortunata 腰上挂的是长柄、椭圆环头、齿状钥匙头的「监狱钥匙」样式（z_keys61.jpg，画面横向约 28% 处），看着像中世纪的东西；s6_st6 桌上那盏双嘴灯顶上有一个小提环（z_lamp66b.jpg）。其余器物都对：s3 蜂巢炉、熔岩石磨、八瓣面包（z_bread36.jpg 托板上 5 个，每个 4 道刀口、8 瓣）；s5 嵌罐柜台、青铜锅、腊肠火腿；s6_st2、s7_st1–st7 的 p1 陶灯都是封顶、有注油孔、带环形把手（z_lamp72.jpg、z_lamp64c.jpg）；s8 有刮板、油瓶和青铜火盆；s4_st3 是洋葱和蚕豆（z_beans.jpg）。）；b 3 分（s6_st4 首帧人物手中陶灯为扁圆一体灯身、注油孔、短嘴与环柄，没有盖钮；s4_st5 右下铜币放大只有头像浮雕；s8_st5–st6 的陶油瓶、曲面铜刮板及 s3 的石磨、圆顶炉均未见现代或中世纪器物。详见逐场清单。）
- **E3**（抽查）服饰与发型：a 2 分（58 张首帧里 Riley 一直穿米白亚麻衬衫、卡其工装裤、橄榄腰带、深棕短靴，头发乌黑。s2_st2、s2_st8、s5_st5、s8_st10 放大看耳朵（z_ear22/28/55/810.jpg），没有耳环或首饰。当地女人穿及踝 tunica、披 palla、挽低髻；男人穿短 tunica。小瑕疵：s6_st1 画左两个过路男人都留着修短的胡子（z_sky61.jpg）；s6_st6 两个车夫、s5_st6 两个男人只是胡茬，可以接受。）；b 3 分（s2_st5、st7 的 Vibia 为赭色 tunica、红 palla、低髻；s3_st4 的 Felix 短衣、围裙且下颌清爽；s4 的 Tertius 是短胡茬而非大胡子。s2_st6、s5_st5、s8_st8 的 Riley 穿浅色衬衫、工装裤、腰带，露出的耳、颈、腕未见首饰；当前 c1–c7 人物图逐一核过。）

## 全部评分维度
- **E1** 器物：器物是公元 75 年庞贝有的（陶灯、双耳罐、铜币），没有现代或中世纪器物
- **E2** 建筑与材质：抹灰、红瓦、玄武岩石板、凝灰岩；没有城垛、百叶窗、玻璃格窗、托斯卡纳农舍
- **E3** 服饰与发型：当地人 tunica/palla、男人刮脸；主持人现代旅行装且无首饰
- **E4** 系列禁区：画面不出现烟柱、白烟、冒白气的山；prompt 不写火山词；维苏威不提
- **E5** 文字：画面里没有可读的文字、字母、数字（墙、船、招牌、钱币）
- **E6** 史实一致：台词和画面里的史实与考据一致（地震年份、浴场时间、物价、尿税）
- **E7** 规则源：场景卡、道具卡、考据负面词里没有和以上冲突的写法

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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\era__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2" era --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\era__judge.md" --by "<你的模型名>/era__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）