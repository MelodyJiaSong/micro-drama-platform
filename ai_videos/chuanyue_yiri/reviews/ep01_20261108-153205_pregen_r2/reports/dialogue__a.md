# 台词（时长与逻辑）审稿报告 · dialogue__a（claude-sonnet-5-5）· ep01 出片前 第 2 轮

范围 s2/s3/s4/s8/s5/s6/s7 共 26 镜有台词。数词与窗口取自各镜 spec「节拍」括号里的秒数（词/秒＝词数÷窗口，尾留白＝窗口末到镜末）。出片前没有音频，语音识别（whisper）无法核对，只能按文字审，已在各项注明。

## 评分表
- D1 1 证据：多数达标：s2_st2 19 词/(5.0+3.0 s)=2.4/2.3、s3_st2 9/3.8=2.4、s4_st4 13/5.8=2.2、s8_st6 6/2.7=2.2、s5_st1 10/4.7=2.1；开口前最短 s3_st4 Garum 1.1 s、s8_st10 1.1 s，均≥1；尾留白最短 s3_st2 1.6 s、s4_st1 1.8 s，均≥1.5。但 s4_st1「Okay, okay — I'm going!」5 词在 7.7–9.2 s＝3.33 词/秒，超 2.8（见问题 4）；贴线的还有 s4_st1 第一句 5/1.8=2.78、s4_st2 第二段 16/5.8=2.76、s7_st2 末句 10/3.6=2.78、s8_st9 11/4.0=2.75、s8_st1 19/7.0=2.71，这些都没有余量给省略号停顿。
- D2 2 证据：动作与词对得上：s2_st2「说到 drain 左手一摊、stepping stones 拇指指后」；s3_st4 8–13 s「No clue 耸肩、Sounds like left? 歪头挑眉」；s8_st6 5.1–8.8 s 拉丁语第二句手翻；s7_st1 每句后配拍床、点头、摊手。小瑕疵：s6_st3 11.8 s 她转头听「吆喝」，声音要剪辑从 s6_st1 贴进来，本镜自身没有这句声音；s3_st4 5.5–7 s「嘴唇无声地动」可能被模型生成成出声。
- D3 2 证据：s3_st4「Hac recta platea… ito ad dextram」、s5_st8「Dextram」、s6_st1「Hospitium hic locatur」、s6_st2「Convenit」、s8_st6「Dies nihil est. Dum versas te, nox fit.」、s5_st2/st10 的 Assibus…／Dupondium si dederis, meliora bibes（庞贝 CIL IV 1679 酒馆铭文）语法与词义都对，古典读法注音都在 prompt。扣分：s8_st6 prompt 仍写「doom WER-sahs teh」（dum 为短 u，I163 未改）；s5_st13 的「Garum?」没有 GAH-rum 注音；s3_st4 的 ito（ītō）偏书面，口语多用 i（见问题 1、2、9）。
- D4 2 证据：Mission 编号闭环：s1_st2 台词「Mission one: find a bed… Mission two: try garum」→ s5_st7「Mission two: done. Now… a bed.」→ s7_st1「Bed? Found. Garum? Tasted. Budget? …Gone.」。dextram 链：s3_st4 Felix「ito ad dextram」、Riley 猜「Sounds like left?」→ s3_st8 她朝自己的左边（东）走 → s4_st3「Left. Definitely left.」→ s5_st8 店主「Dextram」→ s5_st9「"dextram" means right?」，一致。钱数：s3_st1 付 2 枚、s8_st10 付 1 枚浅色小铜币、s5 付 2 枚→ s6_st3 剩 3 小钱＋1 大币 → s6_st2 全付 → s7「Gone」，对得上。扣分：s5_st9「I went the wrong way all morning」所在场景是下午第九时（约三点半，s5 场景行）；s4_st2「His son」指代不明（见问题 5、7）。
- D5 2 证据：每镜说话人与「口型：只有标明的人张嘴」一致；s2_st8 Vibia、s3_st4 Felix 抬头反应、s8_st10 门房、s5_st12 Asellina 都写明不说话。拉丁语说话人 Felix/Tertius/Asellina/Fortunata 的 manifest 都挂了各自声音参考。扣分：s5_st8 店主与 s8_st6 妇女只有 c1_Riley_audio、没有各自声音参考，只靠文字写「中年男声／女声」，模型很可能用 Riley 的音色喊（见问题 3）；s8_st6 第 0 秒首帧 Riley 嘴已张开（闭眼长叹），要避免被当成说话。
- D6 2 证据：悄悄话都在安静处：s7_st1/st2/st3、s5_st7 夜里或柜台边；s2_st2、s3_st1 的喷泉、石磨声写成画外低音量。小瑕疵：s8_st1 prompt 第 13 行让墙后叉铃与合唱全程（0–16 s）响着，Riley 6.1–13.1 s「压低声音」说 19 词，而 prompt 又写「不要背景音乐」，合唱可能被生成成配乐并盖过她；s6_st6 大堂里两个车夫吃饭而 Riley 压低声音说话，需要人声层次（见问题 8）。
- R 1 证据：上一轮本类 11 条：I93（s6_st3 不生成吆喝，已改）、I155（s3_st4 台词与 st8 方向一致，已改）、I156（s6_st3 5.3–6.5＋6.9–10.6 s，2.7 词/秒，已改）、I159（s8_st6 窗口 1.6–4.3 s，已改）、I160（s4_st4 窗口 7.1–12.9 s，已改）、I161（s7_st1 重排，已改）、I162（s4_st2 第一段已放宽，第二段未动，「His son」仍在）、I94/I95（只加了文字声音，没挂声音参考，风险还在）、I96（出片后核，未到时点）。未改好：I157（s5_st13 无 GAH-rum）、I158（s3_st4、s8_st6 等 prompt 的「口型」行仍是「正常语速与口型」，与「飞快」「说得慢」「懒洋洋」冲突）、I163 的 s8_st6 半（仍是「doom」）。

## 问题表

| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |
|---|---|---|---|---|---|---|
| s4_st1 | 7.7–9.2 s | D1 | 记录 | ② 分镜文字 | 「Okay, okay — I'm going!」5 词/1.5 s＝3.33 词/秒；节拍窗口 7.6–9.6 s 本有 2 s，口语标注只用了 1.5 s | 便宜：口语窗口放宽到 7.7–9.5 s（≈2.8），或删一个 okay；退场 9.6 s 不变 |
| s5_st13（及 s7_st1） | 8.6–9.2 s | D3 | 记录 | ③ prompt | s5_st13 台词行只有「Riley（问，美式英语）：Garum?」，没有 GAH-rum 注音（s3_st4 已有）；s7_st1 同样无注音 | 便宜：两处补「GAH-rum，重音在前」 |
| s5_st8、s8_st6 | 1.6–2.6 s；5.1–8.8 s | D5/D6 | 存疑 | ③ prompt | 唯一说话人是配角，manifest 只有 `c1_Riley_audio`；prompt 另写「本镜不说话的人物不出声」，模型可能用 Riley 音色或让 Riley 张嘴 | 便宜：出片时先试；若串音，把「声音参考」段明确写「`c1_Riley_audio` 本镜只给嘴型对不上时忽略，不用于喊话」，或给店主／Helvia 配一条声音参考 |
| s8_st6 | 5.1–8.8 s | D3 | 记录 | ③ prompt | 注音「doom WER-sahs teh」，Dum 是短 u（I163 未改完） | 便宜：改成「dum WER-sahs teh」 |
| s5_st9 | 1.6–7.3 s | D4 | 记录 | ① 故事 | 「I went the wrong way all morning」，该镜所在 s5 是下午第九时（约三点半），她上午走错、下午已去过浴场 | 便宜：改成「all day」或「since breakfast」，story.md 同步 |
| 全部有台词的镜（规则源） | — | D1 | 记录 | 规则源 | 「口型」行统一是「正常语速与口型」，与 s3_st4「飞快」、s4_st4「说得慢」、s7_st2「两个人名放慢」、s8_st6「懒洋洋、语速从容」冲突（I158 仍 open） | 便宜：口型行改成「语速按台词括号里写的；没写的按正常语速」 |
| s4_st2 | 7.1–12.9 s | D4/D1 | 记录 | ① 故事 | 「His son called it gross」紧跟「the emperor? He taxes it」，His 指皇帝，但整句要两个人物（儿子、老爸）；16 词/5.8 s＝2.76，带引号和问句停顿，贴线 | 便宜：改成「The emperor's son called it gross — so Dad held a coin…」，或窗口再放宽 0.4 s |
| s8_st1 | 0–16 s | D6 | 存疑 | ③ prompt | 墙后叉铃与合唱全程在响，Riley 压低声音说 19 词（6.1–13.1 s，2.71 词/秒），又有「不要背景音乐」，合唱可能被当配乐或盖住她 | 便宜：写明「合唱与叉铃音量压到她说话声以下，6.1–13.1 s 更低」，出片后剪辑时对一遍 |
| s3_st4 | 2.3–5.2 s | D3 | 记录 | ② 分镜文字 | ito（ītō，将来式命令）偏书面，街头口语多用「i」；不影响理解，也不改变 dextram 的回收 | 便宜：可不改；要口语就改成「Hac recta platea i, ad dextram」并同步注音 |
| s6_st3 | 11.8–12.8 s | D2 | 记录 | ③ prompt | 她转头听吆喝，但本镜不生成人声，要靠剪辑从 s6_st1 贴；漏贴会变成她对着空气转头 | 记录：加进剪辑清单 |

## 整体观察
- 台词本身精简、口语，各镜词数多在 2.1–2.7 词/秒，尾留白都够；比上一轮的 s6_st3、s4_st4、s7_st1 的赶词问题已明显改好。
- 编号与回收闭环（Mission、dextram、钱）完整，只有 s5_st9「all morning」与时间线冲突一处。
- 拉丁语全部有古典读法注音和出处（庞贝酒馆铭文），错误集中在两处未改完的注音。
- 本轮最大风险不在文字，而在出片：配角说话时只有 Riley 的声音参考（s5_st8、s8_st6）。
- 没做 whisper 转写，出片前没有音频；I96（两种 Salve 读音）要出片后核。
