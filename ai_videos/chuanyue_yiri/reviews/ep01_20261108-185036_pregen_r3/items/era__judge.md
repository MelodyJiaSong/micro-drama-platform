你是裁决人 **era__judge**（claude · claude-opus-5-5），裁「时代与世界观」审稿项 era 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reconcile\era.md`。

## 两份报告
- a 位（claude-opus-5-5/era__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\era__a.md`
- b 位（claude-sonnet-5-5/era__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\era__b.md`

## 要裁的维度
- **E7**（分歧）规则源：a 1 分（story.md:75 还写着「柳条笼子上罩着白布，底下冒出细细的黄白色烟」，:53 还写着「一缕烟从门楣上飘出来」；story.json 已经按 I50 改了（「黄白色烟」出现 0 次、「门楣下贴着」出现 1 次），两份故事稿不一致。另外 bg3_面包房.md:31「空气里飘着一点面粉和炉烟」、s5_st10 首帧 prompt 第 4 行「冒着热气」、c7 卡「米白厚亚麻浴袍」、p4 卡「一根直的木柄」都和禁区或史实有冲突或存疑。bg2 卡（「四块深灰色大石块」）和各场景卡的「木桶」已按 I50 改好）；b 2 分（bg2 已改「深灰色大石块」；bg4 已删笼下冒烟，story.md:53 改成门楣下一缕炉烟；bg10 已把百叶窗改成实木板窗（s8_st1 右墙窗扇是平木板，z_w81）；bg7 已改无玻璃窗洞；扣分：bg8 卡写「窗洞里最多嵌一整块厚而模糊的单片玻璃」，而 s8_st2/st3 负面词是「玻璃、带玻璃的窗」，两处口径不一；bible §9 没写室内浴场蒸汽、罐口热气的尺度，story.md:117 还写「有的冒着热气」，而画面禁区写的是「成股的蒸汽升上天空」不行，口径要定；bible §9 末句「要不要让山入画，待用户定」仍悬着（本范围画面里没有山，s7_st5 已不画）。）
- **E3**（抽查）服饰与发型：a 2 分（Riley 在 59 镜里一直是米白短袖衬衫、橄榄色腰带、卡其工装裤、深棕短靴，看得见的镜头里没有耳环、项链、手表；当地人穿 tunica/palla，Vibia 插骨簪（s2_st5）、老人穿长 tunica 披斗篷（s2_st4 放大 z_s2st4_people.png，不是托加）；s6_st1 两个过路男人都刮了脸。瑕疵：s5_st8 赶驴人留着整齐短须，和首帧 prompt 第 4 行「车夫…脸刮得干净」不符（z_s5st8_man.png）；s8_st3/st8 妇女的「浴袍」是带翻领、长袖、厚棉质感的现代浴袍样子（z_s8st3_robes.png））；b 2 分（Riley 在 58 张首帧里都没有耳环、项链、手表（s2_st2、s5_st4、s8_st4 近景脸与脖子）；本地人都是 tunica、palla、浴袍，妇女挽髻插骨簪（s2_st5、s8_st5、s8_st9），s4_st1 洗衣工、s8_st7 老人是素色短褂加皮凉鞋；扣分：s5_st6 右边男人和 s6_st6 两个男人都有明显胡茬（z_men56、z_men66），而 prompt 写「脸刮得干净」，上一轮 I107 只改好了 s6_st1。）
- **E4**（抽查）系列禁区：a 2 分（kw.py 扫 59 份送模型 prompt 加首帧 prompt，「火山／维苏威／熔岩／Vesuv」0 处；台词全集没提维苏威；所有首帧的天空里没有山、没有烟柱（s7_st5 往西南看是海平线，s6_st1 画左已改成连着的房子）；浴场蒸汽都在室内。瑕疵：s5_st10 首帧 prompt 第 4 行还是「旁边一只敞口陶罐冒着热气」，首帧画右下有一股热气从罐口升到画面约一半高（y≈470/941），即 I106，没有改）；b 2 分（全部首帧没有烟柱、白烟、冒烟的山；s7_st5 夜景地平线是平的海线，无山；s2/s4 街景天空干净；s3_st1/st5/st7 的炉口只有火光，没有烟；扣分：s5_st10 首帧罐口升起一股灰白热气，高到约画面 30%，不是 prompt 写的「贴在罐口」（z_steam510.jpg，上一轮 I106 没改好）；s8_st3/st4/st8 的浴场蒸汽在室内，不算升天，但 bible §9 对「成股的蒸汽」没写室内例外（见 E7）。）

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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\era__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3" era --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\era__judge.md" --by "<你的模型名>/era__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）