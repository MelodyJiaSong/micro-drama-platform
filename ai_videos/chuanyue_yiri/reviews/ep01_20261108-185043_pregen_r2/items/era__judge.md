你是裁决人 **era__judge**（claude · claude-opus-5-5），裁「时代与世界观」审稿项 era 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reconcile\era.md`。

## 两份报告
- a 位（claude-opus-5-5/era__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\era__a.md`
- b 位（gpt-6.1-sol/era__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\era__b.md`

## 要裁的维度
- **E2**（分歧）建筑与材质：a 2 分（抹灰红/赭墙配深色墙裙、红陶筒瓦、凝灰岩城墙墙头平整无城垛、多边形玄武岩路面、st5 铺面门槛和斜靠的门板都对，全片没有百叶窗和玻璃窗。存疑三处：st1/st4 城门上方带红瓦两坡顶的门楼（st1 x250–580,y160–230）；st1/st4 左上屋脊上有带帽的烟囱状构件（st1 x322,y137，work/era__a/st1_chimney.png）；st5 从城里看只有一个拱，st1/st3 从城外看却是一大一小两个拱。见问题表）；b 1 分（st1/st2/st4 首帧均为大拱在左、小拱在右；st3 首帧和 spec.md:10 进一步写死小洞在大洞右边，与海门朝东实景的小洞在左相反（问题 1）。bg1-2 卡:9、19 把拱顶写成凝灰岩大石砌，与官方导览 p.81 的混凝土筒拱结构不符（问题 2）。红瓦、彩色抹灰、石板、木板店门本身可用；门楼及屋脊竖件仍存疑（问题 4、5）。）
- **E4**（抽查）系列禁区：a 2 分（五镜首帧的天空都放大看过，没有烟、白气或雾带（st1 太阳附近 x0–420,y40–240 也没有）；五份资料包 prompt 的正文里没有火山、熔岩、维苏威，场景行只写「长满葡萄藤的绿色缓坡山」；台词里也没提这座山。小瑕疵：参考底图 bg1 的山顶有一块灰色裸岩（work/era__a/bg1_summit.png，原图约 x1490–1560,y140–160），bg1 种子 prompt 写的是「山顶平缓发灰」，容易被看成火山顶。另外 bg1 种子 prompt 里还有火山口暗示词，记在 E7）；b 3 分（st1/st2/st4 画右远山至天空、神庙脚手架上方均无烟柱、白烟或蒸汽，st3/st5 门洞和街道也无此物。五份 snapshot/prompts 全文核读及关键词检查，未见火山、熔岩、维苏威、山顶的坑等诱发词；禁烟词只在排除项。场一全部对白无山名或灾难预兆；按 BRIEF 已知项，将画右绿山视为 Monti Lattari。）
- **E5**（抽查）文字：a 2 分（五镜首帧都放大找过字，墙、船（st1 work/era__a/st1_boats.png）、门板、钱币（p2 图三枚币都无字）上都没有可读的字母或数字；船名、招牌都没有。小瑕疵：st1、st4 城墙的石块上有一片弯钩状的纹路（work/era__a/st1_wall.png，原图 x560–1000,y250–420），不是字母，但像刻出来的记号，生成视频时可能变成符号）；b 2 分（放大核对 st1 抹灰墙、st4 船舷、st5 两侧陶罐/门板/墙裙、p2 三枚币，未见可读单词、数字或明确铭文；但 st1 神庙三角山墙中央约 x=54%–56%、y=11%–15% 有近似 S/V 的深色曲折痕，不能确定是浮雕还是类字母，见问题 6。俯视图中的编号和文字是规划标注，五份 prompt 均明确不让它们入画。）

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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\era__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2" era --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\era__judge.md" --by "<你的模型名>/era__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）