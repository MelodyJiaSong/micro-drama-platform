# dialogue（台词（时长与逻辑））单审

- 审稿人：claude-sonnet-5-5/dialogue__a（claude-sonnet-5-5）报告 `reports/dialogue__a.md`
- 状态：完成

## 评分

| 维度 | 分 | 证据 |
|---|---|---|
| D1 说得完 | 1 | 多处窗口短于需要时长。s5_st1 末句 "And I've been saving my bread for garum." 8 词需 3.2s，窗口 13.3–15.8 只有 2.5s（折合 3.2 词/秒，比正常语速快 28%，是缺口最大的一处）。s1_st2（30s 已到上限）第 4 段 "And my budget for all of that is… this." 9 词需 3.6s，加「停半拍」约 4.1s，窗口 20.8–24.5 只有 3.7s；9.0 和 14.8 两个衔接点前后窗口首尾相连，没有换气。s4_st2 第 2 句 "And the emperor actually puts a tax on it." 9 词需 3.6s，窗口 7.1–10.3 只有 3.2s。s5_st12 "Oh my god, the OK sign works!" 7 词需 2.8s，窗口 3.6–6.0 只有 2.4s。其余多数窗口恰好够（零余量），见问题表 1–4 条和记录条。开口前 ≥1s、说完后 ≥1.5s 的留白各镜基本满足（s8_st10 说完 6.4→8.0 为 1.6s，勉强）。 |
| D2 节拍对位 | 2 | 台词词与动作大多对得上：s1_st1 up there（9.8–13.8）瞟城门；s3_st4 第一个 garum 出口 Felix 停手；s4_st3 说到 left 左手一摆；s6_st3 this（约 12.7s）摊钱；s8_st1 bath time 时咧嘴一笑；s8_st4 melting（7.0–8.6）扇脸。小瑕疵：s1_st2 的「说 this 时四指摊平」落在被压缩的 20.8–24.5 窗口里，语速一放慢就和摊钱错位；s5_st1 的「说完前拍布包」被压在 2.5s 里。 |
| D3 外语与专名 | 2 | 拉丁语语法和语义核对无误：Salve / Unum / Tene / Vale / Apage（希腊借词）/ Euge（希腊借词）/ Quattuor / Convenit / Illic. Sursum. / Hospitium hic locatur（庞贝铭文式）/ Assibus hic bibitur. Dupondium si dederis, meliora bibes.（改自庞贝 Edone 酒馆铭文）/ Hac recta platea… ito ad dextram（路径夺格和将来命令式正确）。注音都进了台词备注（SAHL-weh、GAH-rum、KWAHT-too-or、DEK-strahm 等）；"the emperor" 不出现 Vespasian，规避了读错风险；Pompeii 写了 pom-PAY，75 AD 写了 seventy-five A-D，Vibius Restitutus、Urbana 也有注音。扣分点：I38 仍 open（Dies nihil est. Dum versas te, nox fit. 是编写句，ito、platea 偏书面），要等用户定；出片前无法转写核实发音。 |
| D4 台词逻辑 | 2 | 「两件事」闭环：s1_st2 说睡觉和 garum → s5_st7「Now I just need to find a bed」→ s6_st3 / s7_st1 回收；s1_st6 把 garum 和鳀鱼接上。钱账：9 枚 →（s3 付 2）7 →（s8 小铜币）6 →（s5 付 2）4 →（s6 付光）0，各镜口径一致；s7_st1「every last coin」对得上。年份：地震 12 年前（63→75）对得上。扣分点：dextram 回收的因果有点绕，见问题表第 5 条（存疑）。 |
| D5 说话人 | 3 | 逐句核对说话人：s2_st5 画外 Riley，Vibia「嘴一直闭着」；s5_st13 全镜 Asellina 只说 Euge!；s3_st1、s3_st7、s4_st1、s5_st8、s6_st3（画外 Fortunata）都标了谁张嘴；s8_st2、s8_st10 门房「嘴闭着」；s8_st5、s8_st9 Helvia 不说话，s8_st6 只有 Helvia 张嘴；s5_st8 Riley「嘴唇无声地动」写明无声。没有发现张嘴的人和台词不对应。 |
| D6 听得清 | 2 | s1_st1、s1_st6、s1_st3、s8_st4、s6_st3 都写了环境声压在对白下面（s6_st3 写了「清楚压过骡子响鼻」）；r2 的 s8_st4 条已补。仍缺：s2_st2（喷泉流水）、s2_st8（压低声音，喷泉就在身后）、s8_st1（叉铃和合唱，同期声贯穿 6.1–18.8 的整段台词）、s4_st2（身后哗哗踩水声）的台词备注里没有这类说明（grep 这几镜 spec 无「压在对白下面」类字样）。 |
| D7 跨镜接续 | 2 | 逐个核对 40 个有台词的接点。s1_st1→st2 由 "Wait, wait — I gotta do this right." 交代重开，st2 第一拍深吸气，3 分；s4_st2→st5（Does this smell? → …Nope.）、s4_st4→s8_st1（Still smell like pee. → bath time）、s5_st8→st9、s7_st4→st6（Okay. Cozy. → Oh, and we've got…）、s7_st7→st1（0–2.2s 环顾）、s8_st5→st9、s7_st3（Okay. 重置 + goodnight from Pompeii 对应开场）都接得上。小瑕疵两处，见问题表 6、7 条（记录）。 |
| D8 跨语言说清 | 2 | s3_st4 已有倒酱手势、两手一摊、Felix 停手看着她并整臂指路，Riley 复述「That way?」指同一方向、Felix 点两下头，观众看得懂；s5_st11 竖一根、两根手指加点酒罐，s5_st12 OK 手势得到同样回应；s5_st13 举面包瓣加 garum，Asellina 一听即亮眼并拿鱼露罐；s6_st1 Um — sleep? 加手贴脸，Fortunata 竖四指；s6_st5 Illic. Sursum. 指加上挑；s8_st2 摊钱让门房自取。s3 面包房一段（节点 15/15b）按任务书已知，改法待用户在 story_beats.md 挑，这里只记一笔，不展开。 |

## 问题表

| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |
|---|---|---|---|---|---|---|
| s5_st1 | 13.3–15.8 | D1 | 可剪 | ② 分镜文字 | "And I've been saving my bread for garum." 8 词，2.5 词/秒需 3.2s，窗口 2.5s，要说到 3.2 词/秒才塞得下。前面 1.6–12.8 的各句窗口都刚好够，这一句是被后面「16–17.5 朝前望、嗅」挤出来的。 | 便宜：窗口改 13.3–16.5（拍布包和台词同步放宽），后两拍各顺延 0.7s，镜头 19s→20s。不改句子。 |
| s1_st2 | 20.8–24.5，9.0 / 14.8 | D1（兼 D2） | 可剪 | ② 分镜文字 | 全镜 30s 已到上限。第 4 段 9 词需 3.6s，加「停半拍」约 4.1s，窗口只有 3.7s；第 2、3、4 段窗口首尾相连（9.0、14.8 无换气），第 3 段 15 词刚好 6.0s 零余量；从 1.5 开口到 20.8 共 44 词、19.3s，只比 2.5 词/秒略慢。 | 便宜：不能再加时长，只能重排。开场 0–1.5 改 0–1.0（仍 ≥1s），后面各段整体前移 0.5s；第 2、3 段之间各留 0.3s 换气，第 4 段拿到 4.2s；24.5–26.5 摊钱停留收成 24.9–26.5（1.6s 仍够数 9 枚）；尾部 28.5–30 的 1.5s 留白不动。 |
| s4_st2 | 7.1–10.3 | D1 | 可剪 | ② 分镜文字 | "And the emperor actually puts a tax on it." 9 词需 3.6s，窗口 3.2s（2.8 词/秒）。前一句结束 5.2、这一句开始 7.1，中间白着 1.9s，后一句开始 11.6、也有 1.3s 空档。 | 便宜：窗口改 6.6–10.3（共 3.7s），把前面的空档吃掉一点。镜头 24s 不变。 |
| s5_st12 | 3.6–6.0 | D1 | 可剪 | ② 分镜文字 | "Oh my god, the OK sign works!" 7 词需 2.8s，窗口 2.4s；下一句 6.4–8.4（5 词刚好 2.0s），两句之间只有 0.4s。 | 便宜：第一句改 3.6–6.4，第二句改 6.8–8.8；Asellina 擦台面（4.8–6.2）和递杯（约 7.4）跟着后移 0.4s；掏钱段 8.6–11 顺延到 9.0–11.8，镜头 11s→12s。 |
| s2_st2→s2_st5 | 接点 | D7 | 记录 | ② 分镜文字 | st2 里喷泉流水声一直在镜头左边画外，她站在喷泉边讲了 18 秒；st5 她在画外说 "Oh, cool — a fountain."，像刚发现。st2 最后一拍只是「看着镜头笑着点头」，没有转头看向水声的动作，所以 st5 的惊喜缺一个触发点。 | 便宜：st2 的 16.3–18 秒收尾，改成点头后循着水声朝画面左边偏头看一眼（不加台词）。 |
| s5_st5→s5_st7 | 接点 | D7 | 记录 | ② 分镜文字 | st5 刚说完 "It really is just fish sauce! … She would love this."，st7 开口又是 "Okay, I finally tried garum, and it was so good."，等于把刚演过的事再总结一遍；好在中间隔着举杯、碰杯，并且紧跟 "Now I just need to find a bed." 接回第二件事，基本可接受。 | 可不改。想更顺：st7 开口句换成带转折的，比如 "Okay, garum — done, and wow." 一类（只作备选，用户已有「不要清单腔」的反馈，别用）；或保持现状。 |
| s2_st2、s2_st8、s8_st1、s4_st2 | 台词备注 | D6 | 记录 | ② 分镜文字 / 规则源 | 这四镜台词备注里没有「某某声压在对白下面」：s2_st2 喷泉流水（画外，spec 写听得见）、s2_st8 压低声音但喷泉紧挨着身后、s8_st1 叉铃和合唱贯穿 6.1–18.8 整段台词（0–6 秒环境声要听得见，说话时要退下来）、s4_st2 身后哗哗踩水声。s1、s3、s8_st4 已有，同类写法不统一；r2 的 I80 只补了 s8_st4。 | 便宜：台词备注各补一句「流水声 / 叉铃与合唱 / 踩水声压在对白下面，仍隐约可闻」；s8_st1 注明「说话期间叉铃与合唱退到背景」。 |
| s1_st3、s5_st7、s7_st1、s4_st3 等 | 见说明 | D1 | 记录 | ② 分镜文字 | 小幅缺口或零余量：s1_st3 7.6–17.9 对 25 词需 10.0s，余 0.3s；s5_st7 两句缺 0.3s 和 0.2s（5.1–8.8 对 10 词需 4.0s，9.2–12.2 对 8 词需 3.2s）；s7_st1 "It's a bed." 4.0–4.9 对 3 词加拍床需约 1.2s；s4_st3 "Oh — sorry." 8.6–9.1 对 2 词需 0.8s；s5_st9 "Oh my god." 5.0–5.9 对 3 词需 1.2s；s8_st1 "Which means… bath time." 17.1–18.8 对 4 词加半拍约 2.1s。零余量的句子很多（s2_st2、s3_st2、s6_st3、s7_st2、s8_st9 等恰好 2.5 词/秒），一旦演员气口多一点就会被压缩。 | 便宜：能放宽的窗口各放宽 0.2–0.5s（前后都有空档的镜），不改句子。 |
| s5_st9 / s3_st4 | 见说明 | D4 | 存疑 | ① 故事 | 回收的因果有点绕：Felix 指的是他自己的右手边，也就是 Riley 的左边（story.md 第 89 行写明），她猜成「left」本身没错；s3_st8 里她走反是因为转了身再按「自己的左手」走。s5_st9 却是 "Dextram means right? …I've been going the wrong way all day."，听起来像是「词义是右、我走了左」，而实际原因是转身后方向颠倒。观众多半能笑出来，但按词义反推，她改走「右」反而就是她走过的那边。核实办法：看 story_beats 里作者想让观众笑在哪（语言误解还是转身犯迷糊）。 | 便宜，只加不删：在 s5_st9 的 "I've been going the wrong way…" 前或后补半句，把原因说出口，例如「…he pointed one way and I turned around and walked the other.」；或在 s3_st8 里让镜头更明确地强调「她背对石台后的左手方向是反的」，台词不动。 |
