你是裁决人 **dialogue__judge**（claude · claude-opus-5-5），裁「台词（时长与逻辑）」审稿项 dialogue 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reconcile\dialogue.md`。

## 两份报告
- a 位（claude-sonnet-5-5/dialogue__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\dialogue__a.md`
- b 位（gpt-6.1-sol/dialogue__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\dialogue__b.md`

## 要裁的维度
- **D3**（分歧）外语与专名：a 2 分（s3_st4「Hac recta platea… ito ad dextram」、s5_st8「Dextram」、s6_st1「Hospitium hic locatur」、s6_st2「Convenit」、s8_st6「Dies nihil est. Dum versas te, nox fit.」、s5_st2/st10 的 Assibus…／Dupondium si dederis, meliora bibes（庞贝 CIL IV 1679 酒馆铭文）语法与词义都对，古典读法注音都在 prompt。扣分：s8_st6 prompt 仍写「doom WER-sahs teh」（dum 为短 u，I163 未改）；s5_st13 的「Garum?」没有 GAH-rum 注音；s3_st4 的 ito（ītō）偏书面，口语多用 i（见问题 1、2、9）。）；b 1 分（s3_st4 prompt 第 20 行已有 Garum＝GAH-rum 与 ītō＝EE-toh；s5_st13 prompt 第 20 行仍无 Garum 注音；s8_st6 prompt 第 22 行、Helvia 人物卡与 r05 台词库 #21 仍写 doom，未完成 I163。Salve 的两种读音是有意设计；未提供本轮声音，实际发音尚不能验证。）
- **D4**（分歧）台词逻辑：a 2 分（Mission 编号闭环：s1_st2 台词「Mission one: find a bed… Mission two: try garum」→ s5_st7「Mission two: done. Now… a bed.」→ s7_st1「Bed? Found. Garum? Tasted. Budget? …Gone.」。dextram 链：s3_st4 Felix「ito ad dextram」、Riley 猜「Sounds like left?」→ s3_st8 她朝自己的左边（东）走 → s4_st3「Left. Definitely left.」→ s5_st8 店主「Dextram」→ s5_st9「"dextram" means right?」，一致。钱数：s3_st1 付 2 枚、s8_st10 付 1 枚浅色小铜币、s5 付 2 枚→ s6_st3 剩 3 小钱＋1 大币 → s6_st2 全付 → s7「Gone」，对得上。扣分：s5_st9「I went the wrong way all morning」所在场景是下午第九时（约三点半，s5 场景行）；s4_st2「His son」指代不明（见问题 5、7）。）；b 1 分（story.md 第 21/133/157 行的目标一找床、目标二尝鱼露及结尾回收一致，钱包 7 as＋1 quadrans＋1 sestertius → 5 as＋quadrans＋sestertius → 5 as＋sestertius → 3 as＋sestertius → 0 可对齐；但第 67 行仍说 Straight… then 'dextram.'，第 69 行与 s3_st8 6–9 秒却直接左拐，I155 的“直走后再拐”与立即拐弯矛盾未完全消除。）
- **D6**（分歧）听得清：a 2 分（悄悄话都在安静处：s7_st1/st2/st3、s5_st7 夜里或柜台边；s2_st2、s3_st1 的喷泉、石磨声写成画外低音量。小瑕疵：s8_st1 prompt 第 13 行让墙后叉铃与合唱全程（0–16 s）响着，Riley 6.1–13.1 s「压低声音」说 19 词，而 prompt 又写「不要背景音乐」，合唱可能被生成成配乐并盖过她；s6_st6 大堂里两个车夫吃饭而 Riley 压低声音说话，需要人声层次（见问题 8）。）；b 0 分（本单提供的是新文字、首帧、俯视图和音色参考，没有对应当前修订的成片对白、混音或识别区间；无法试听确认水声、合唱、远处喊声是否盖住对白。s8_st1 仅写墙后低声合唱、Riley 压低声音，不能据此判“听得清”已通过。）
- **D2**（抽查）节拍对位：a 2 分（动作与词对得上：s2_st2「说到 drain 左手一摊、stepping stones 拇指指后」；s3_st4 8–13 s「No clue 耸肩、Sounds like left? 歪头挑眉」；s8_st6 5.1–8.8 s 拉丁语第二句手翻；s7_st1 每句后配拍床、点头、摊手。小瑕疵：s6_st3 11.8 s 她转头听「吆喝」，声音要剪辑从 s6_st1 贴进来，本镜自身没有这句声音；s3_st4 5.5–7 s「嘴唇无声地动」可能被模型生成成出声。）；b 2 分（s2_st2 drain 配摊手、stepping stones 配拇指后指；s5_st2/st10 一根/两根手指各配对应报价；s8_st9 0–2 秒先刮、3.1–7.1 秒再解释、7.3 秒起还刮板，节拍基本清楚。小瑕疵是 s3_st4 spec 第 10 行写 Felix 在 Riley 说话时反应，而第 12 行把同一反应放在她说完后的 13–14.5 秒。）
- **D5**（抽查）说话人：a 2 分（每镜说话人与「口型：只有标明的人张嘴」一致；s2_st8 Vibia、s3_st4 Felix 抬头反应、s8_st10 门房、s5_st12 Asellina 都写明不说话。拉丁语说话人 Felix/Tertius/Asellina/Fortunata 的 manifest 都挂了各自声音参考。扣分：s5_st8 店主与 s8_st6 妇女只有 c1_Riley_audio、没有各自声音参考，只靠文字写「中年男声／女声」，模型很可能用 Riley 的音色喊（见问题 3）；s8_st6 第 0 秒首帧 Riley 嘴已张开（闭眼长叹），要避免被当成说话。）；b 2 分（s3_st1 1.6–2.2 秒 Felix、2.8–3.6 秒 Riley；s4_st1 6.1–6.6 秒仅 Tertius 喊 Apage；s8_st6 第 17–18 行明确画右 Helvia 说拉丁语；s5_st8 已写粗嗓中年男声。s6_st3 的吆喝已从台词栏移除，但动作行“本镜不生成人声”范围过宽，宜限定为不生成 Fortunata 的画外吆喝；以上为文字分配检查，非实际口型验收。）

## 全部评分维度
- **D1** 说得完：每句 ≤2.8 词/秒（停顿另算），开口前 ≥1 秒，说完后 ≥1.5 秒（用脚本算，给数字）
- **D2** 节拍对位：台词和动作节拍对得上（说到哪句做哪个动作）
- **D3** 外语与专名：拉丁语语法与出处、注音进了 prompt；专名不易读错
- **D4** 台词逻辑：编号、回收、前后说法一致（目标一二、dextram、钱数）
- **D5** 说话人：每句的说话人对，画内该张嘴的人张嘴，不说话的人不出声
- **D6** 听得清：环境声不盖过台词；悄悄话、远处的话能听清

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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\dialogue__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2" dialogue --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\dialogue__judge.md" --by "<你的模型名>/dialogue__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）