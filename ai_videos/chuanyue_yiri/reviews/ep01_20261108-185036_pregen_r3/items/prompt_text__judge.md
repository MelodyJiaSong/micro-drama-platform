你是裁决人 **prompt_text__judge**（claude · claude-opus-5-5），裁「Prompt 文本」审稿项 prompt_text 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reconcile\prompt_text.md`。

## 两份报告
- a 位（claude-sonnet-5-5/prompt_text__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\prompt_text__a.md`
- b 位（gpt-6.1-sol/prompt_text__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\prompt_text__b.md`

## 要裁的维度
- **T1**（分歧）自相矛盾：a 2 分（58 份正文与负面词逐词比对，只有「相机、手机、自拍杆」命中（见 T2）。s3_st1 的 7 枚红铜小钱＋1＋1，到 s3_st1 付 2 枚、s4_st2 掏 1 枚，再到 s8_st2 付小铜币、s5_st3 付 2 枚、s6_st2 付清，数目逐镜对得上。s8_st5 油瓶拔塞、滴、塞回，和 p5 卡、首帧里的软木塞一致。小瑕疵：s7 六镜场景卡与「画面」行互相矛盾、s4_st1 短胡茬与负面词「络腮胡」冲突，见问题表 3、6。）；b 1 分（s7_st1 P11 的空凳、木闩与 P12 的灯及空闩座冲突；s2_st3 P2、P19 禁人声而 P12 要叫卖；见 PTB02、PTB03、PTB05。）
- **T4**（分歧）图文一致：a 2 分（抽看 9 张首帧，文字和图一致。s3_st8 托板上下三上二共 5 个，与「下面三个、上面两个」相符。s8_st5 油瓶带软木塞、布包在 Riley 左胯、Helvia 右手持刮板贴左小臂。s4_st1 Tertius 站在画左单人小槽，院里后排两个工人在远处槽里。s5_st4 细高罐塞已拔、鱼露三滴将落。s6_st1 墙龛灯在 Fortunata 画左。s7_st1 门上只有两个空木闩座，灯在凳上。其余 49 张未逐张看。）；b 1 分（s5_st8 首帧只有 Riley、车夫，驴头朝镜头，P13、P15 却要求三人及驴车向纵深前行；s5_st4 首帧已落鱼露而 P15 在1–3秒才滴；见 PTB01、PTB08。）
- **T5**（分歧）混入别镜：a 1 分（送给模型的正文里留着只对人和编译有意义的跨镜、元信息文字：s6_st3 画面行「那声吆喝是 Fortunata 在 s6_st1 喊的，剪辑时贴进来作画外声」，s2_st7 三处「和/同 st5」，s5_st12/13/14/7/9 的「同 st2」「同 st3」「和 st8 同一个朝向」，s3_st4「与 st1 同一机位」，s7_st7「位置和下一镜 st1 一样」，s6_st1/2/5 人物行「2026-11-08：出图模型画不出罗马钥匙，总画成中世纪长柄钥匙，本集不挂钥匙」。见问题表 2。）；b 3 分（s8_st2、st10 的场景实体段与参考已改为 bg8-1 窄门厅，分别在 P 的“场景”行写“四壁光秃，靠墙一张矮木凳”，没有再复制更衣厅壁龛与整排石凳。BRIEF 排除的场级地点标题不计作新问题。）
- **T6**（抽查）参考清单：a 2 分（脚本核对 58 镜 manifest 的参考键与 prompt「参考：」行顺序完全一致，人物三视图、道具图都已在参考用法里说明，源图哈希无过期。s8_st2/st10 已改挂 bg8-1 门厅。小瑕疵：s4_st3 挂了 p3，但文字写布包「在画面下缘外」，与 s4_st2/s4_st5 不挂的做法不一致；s5_st4 只入一只手却挂了 c4 三视图。）；b 3 分（58 份 manifest 的297条图片参考，标签及顺序均对应 P 第5行；297份源文件与包内副本哈希一致，上传文件存在；58份 manifest 的 prompt_sha256 均对应 prompts.json 原文。s8_st5／st9／st6 的 F 第2行均已列 c1、c7、bg9、p4、p5 五张参考。）
- **T7**（抽查）长度与重点：a 2 分（长度上限 2800 → 5000 已写进 prompts-seedance.md:71，实测 58 份在 1852–4471 字，没有超 5000；超 2800 的从 47 镜降到 39 镜，超 3500 的从 25 镜降到 19 镜。仍长：s6_st1/2/3 为 4471/4431/4414，s8_st5 4128，s5_st3 4113。节拍过满：s5_st14（15 秒内掀盖、取勺、舀酒、倒、搁勺、盖盖、点水、擦台面共 8 步以上），s8_st2（15 秒数 7 枚钱、付一枚、收回 6 枚）。关键动作在「画面」行，前面有 1500–2400 字固定参考用法与人物行。）；b 2 分（58份 P 为1852–4471字符，均低于规则源5000字上限；最长 s6_st1 为4471字符，“画面”正文从第2068个字符才开始。固定项与剧负面词仍重复，属可精简瑕疵，见 PTB09。）

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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\prompt_text__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3" prompt_text --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\prompt_text__judge.md" --by "<你的模型名>/prompt_text__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）