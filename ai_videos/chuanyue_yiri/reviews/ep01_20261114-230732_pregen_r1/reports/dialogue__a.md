# dialogue__a 报告（台词：时长与逻辑 · s6、s7 · 出片前 r1）

审稿人：claude-sonnet-5-5（a 位，单审）。重点镜：s6_st1、s7_st2；其余镜只看台词时长、逻辑与接点。已看首帧图 s6_st1_first_frame.png、s7_st2_first_frame.png。未用 faster-whisper（出片前没有视频可听，发音只能按 prompt 的注音文字核）。

## 评分表

- D1 2 证据：s7_st2 全段 41 词，节拍窗口 2.3–23.4 秒共 21.1 秒，平均 1.94 词/秒，开口前 2.3 秒、说完后 2.6 秒，都够。但分句不均：「I swear it was in my history textbook —」8 词排在 8.1–10.9 秒（2.8 秒，2.9 词/秒），「from an inn just like this.」6 词排在 11.3–13.2 秒（1.9 秒，3.2 词/秒），超过 2.5 词/秒，会逼模型说快。整镜时间很宽裕，只是节拍没摊匀（见问题 1）。s6_st1 的 Hospitium hic locatur! 3 词给 1.5 秒（1.5–3.0），开口前 1.5 秒；Quattuor 在 10.7–11.4 秒，说完后留白 1.6 秒，够。Um — sleep? 2 词给 0.9 秒，One night? 2 词给 0.7 秒，都不急。其余镜：s6_st3 29 词/25 秒，s7_st1 26 词/18 秒，s7_st4 3 词/11 秒，s7_st6 15 词/15 秒，s7_st7 19 词/18 秒，s7_st3 约 21 词/16 秒，都没挤。
- D2 3 证据：s7_st2 every wall 落在 2.3–5.3 秒句内（约 4.2 秒）并配转头瞟墙、拇指一指；history textbook 对 8.1–10.9 秒的扬眉；just like this 对 11.3–13.2 秒的左手一摊；quote 在 14.8–21.0 秒，alone 后半拍。s6_st1 的招手（0–1.5）→吆喝（1.5–3.0）→Salve（5.1/5.6）→指自己（6–6.6）→手贴脸 Um — sleep?（6.7–7.6）→竖一指 One night?（7.9–8.6）→四指加 Quattuor（10.7–11.4）都是说到哪句做哪个动作。
- D3 2 证据：Hospitium hic locatur（「此处出租住宿」，locatur 是 locare 的被动，用法合理）、Salve（SAHL-weh）、Quattuor（KWAHT-too-or）、Convenit（KON-weh-nit）、Illic. Sursum.（IL-lik. SOOR-soom.）语法和古典读音都对，注音都写进了各镜 prompt。Vibius Restitutus「独自睡在这里，想念他的 Urbana」对应庞贝客栈涂鸦 CIL IV 2146（hic solus dormivit et Urbanam suam desiderabat），出处对，「客栈」说法对；两个名字有注音，garum＝GAH-rum 也有注音。小瑕疵：注音 hos-PIH-tee-oo 把词尾 -um 的 m 丢了，古典读法是 -oom（见问题 3）。
- D4 3 证据：s6_st3 与 s6_st1 的吆喝是同一句 Hospitium hic locatur!（story.md 186、188 行）；st3 的 Hospitium… hospitality? 靠这句回收。钱账：st3 手里 3 小钱＋1 大币，st1 的 12.2 秒摊开、st2 付 4 枚，与 s7_st1「I don't have any money left」一致。Quattuor＝四指＝付 4 枚。s7_st1 的 that garum 回收前面熟食铺的鱼露（story.md 170 行附近，开场也是「try garum」）；v2.2 已去掉 Mission 编号，s6、s7 没有残留编号。
- D5 3 证据：s6_st1 画内开口的只有 Fortunata（吆喝、回 Salve、Quattuor）与 Riley（Salve、Um — sleep? One night?），两个行人「只顾聊天」不成句；s6_st3 的 Fortunata 是画外，标明「画面里只有 Riley 开口」；st2 的 Convenit、st5 的 Illic. Sursum. 都是 Fortunata，Riley 回 Thank you.。s7 各镜只有 Riley。
- D6 2 证据：每镜 prompt 都有「对白优先，环境声压低到对白下面」。s6_st1 的 0–3 秒两个行人「边走边低声聊着」和 Fortunata 的吆喝同时出现，prompt 没写他们的话含糊不可辨（见问题 2）。s7_st2 整段轻声，屋里只有灯，没有盖声的环境音，问题不大。
- D7 3 证据：逐个读了 junctions.md 的 12 个接点。st3→st1：Riley 「Hospitium… hospitality?」后转场，Fortunata 继续在对路人吆喝，没有重新打招呼；st1→st2：Quattuor 之后 Convenit，是付钱后的承接；st2→st5 Convenit→Illic. Sursum.；st5→st6 Thank you.→Oh, this is basically a truck stop.（换到大堂，场景变化已写）；st4→s7_st4 无台词→Okay. Cozy.；s7_st4→st6 Okay. Cozy.→Oh, and we've got air conditioning.（接着拿灯看屋）；st6→st7 Cool cool cool→So it's literally a bag of straw（弯腰摸床，顺着看屋）；st7→st1 Rustic, I guess.→It's fine, though.（「though」接得上）；st1→st2「…I'd do it again」→「People write on, like, every wall here.」（st1 结尾回头看墙上划痕，st2 开口讲墙，情绪由「满足」转「轻声温柔」靠 st2 开头 2.2 秒吸气）；st2→st3 That's kind of sweet.→Okay. I'm gonna try to sleep.（情绪下沉自然）；st3→st5 晚安→无台词。没有重复地点和名字，没有「像刚醒来重新打招呼」。
- D8 3 证据：s6_st1 里 Riley 的意图有完整的手势加话：6–6.6 秒指指自己、6.7–7.6 秒手掌贴脸歪头「Um — sleep?」、7.9–8.6 秒竖一指「One night?」；Fortunata 的回应观众看得懂：眉毛一抬、同样竖一指、10.5–11.6 秒四指加 Quattuor，随后伸手要钱（11.6–13 秒），st2 逐枚收钱，晃四指提示补钱。st5 的 Illic. Sursum. 配手指向院子左后方再往上一挑，观众看得出是「去楼上」。没有「只有一个词没有手势」的问句，也没有头也不抬的写法。

## 问题表

| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |
|---|---|---|---|---|---|---|
| s7_st2 | 8.1–10.9、11.3–13.2 | D1 | 记录 | ② 分镜文字 | 「I swear it was in my history textbook —」8 词排 2.8 秒（2.9 词/秒）；「from an inn just like this.」6 词排 1.9 秒（3.2 词/秒），都高于 2.5 词/秒。而全镜 26 秒、台词只占 21.1 秒，前后留白 2.3 / 2.6 秒有富余，其他分句 1.5–2 词/秒偏慢。 | 便宜（改 prompt 节拍文字，视频还没出）：节拍重排，不改词不删词。例：People write… 2.3–5.3；And there's this famous one — 5.7–7.9；I swear it was in my history textbook — 8.3–11.4（3.1 秒）；from an inn just like this. 11.7–14.1（2.4 秒，just like this 的一摊落在 13.4 左右）；It says, 14.5–15.0；quote 15.5–22.0；That's kind of sweet. 22.4–24.0；末尾留白约 2 秒，仍不低于 1.5 秒，全镜不必加长。 |
| s6_st1 | 0–3.0 | D6 | 记录 | ③ prompt | 两个行人「边走边低声聊着」与 1.5–3.0 秒的吆喝重叠；prompt 只写「低声聊」，没写听不清、不成句，模型可能生成清晰的人声，抢 Fortunata 的第一句拉丁语。 | 便宜：「画面」里加「行人的交谈只是含糊的低语，听不清词句，不压过 Fortunata 的吆喝」。 |
| s6_st1、s6_st3、s6_st5 | 台词注音 | D3 | 记录 | ③ prompt | 注音写成 hos-PIH-tee-oo，丢了词尾 -um 的 m（古典读法 -oom），读者或模型可能读成 hospitio。 | 便宜：改为 hos-PIH-tee-oom；这会改动已出片的 s6_st3、s6_st5，只在重出时改，不为此单独重出。 |

## 整体观察

- 台词整体没被挤压：s6、s7 的各镜台词平均都在 2 词/秒以下，留白也够，这轮「镜头跟着台词调」落实得不错；唯一的不均是 s7_st2 中段，改节拍文字即可，不用延长镜头。
- 本轮要重出的两镜台词没改，只是 s7_st2 改成「开场正对镜头、停一下才开口」，开头 2.2 秒和 st1 结尾「回头看墙、嘴角上扬」接得上。
- 其他（一句话）：junctions.md 里 Fortunata 的注音显示成 loh-KAH-too，实际 prompt 是 loh-KAH-toor，应是接点表截断，不是 prompt 错；s6_st3 结尾 Riley 从画左走出（去镜头身后的大车店），s6_st1 里她从画右走来，走向与方位对不上，归连续性审稿人判断。
