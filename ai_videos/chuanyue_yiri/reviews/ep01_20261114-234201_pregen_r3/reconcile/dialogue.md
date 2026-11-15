# dialogue（台词（时长与逻辑））单审

- 审稿人：claude-sonnet-5-5/dialogue__a（claude-sonnet-5-5）报告 `reports/dialogue__a.md`
- 状态：完成

## 评分

| 维度 | 分 | 证据 |
|---|---|---|
| D1 说得完 | 2 | 按 2.5 词/秒核。s7_st2（26 秒，重点镜）：People write… 7 词/3.0s=2.3；And there's… 5/1.9s=2.6；I swear… 8/3.2s=2.5；from an inn… 6/2.2s=2.7；It says, 2/0.5s；引文 9 词（17 音节）/6.0s，含两个放慢的人名和 alone 后半拍停顿，完全够；That's kind of sweet. 4/1.7s=2.4。开口前 2.3s（≥1），说完后 23.4→26 留 2.6s（≥1.5）。s6_st1（13 秒）：Hospitium 1.5–3.0 开口前 1.5s；Um — sleep? 0.9s；Quattuor 10.7–11.4，说完后 1.6s（刚过 1.5）。s6_st3 的 12 词/5.6s=2.1、9 词/3.6s=2.5、6 词/2.3s=2.6，收尾留 1.9s。s7 各镜均在 2.2–2.5 词/秒。小瑕疵：①s6_st1 回礼 Salve. 只有 0.4s（5.6–6.0）；②已出片的 s7_st1「yeah, I'd do it again.」5 词/1.4s=3.6 词/秒（约 4.3 音节/秒，口语还能接受），其后空 4.3s，可以放宽但不需重出。不需要延长镜头。 |
| D2 节拍对位 | 3 | s7_st2 every wall 在 2.3–5.3 句内对侧脸瞟墙和拇指一指，history textbook 在 8.1–11.3 对眉毛一扬，just like this 在 11.6–13.8 对左手一摊，alone 后停半拍，最后 23.9–26 垂眼看灯苗；s6_st1 Hospitium 1.5–3.0 对行人摆手，Salve 5.1–6.0 对点头，sleep? 6.7–7.6 对手贴脸，One night? 7.9–8.6 对竖一指，Quattuor 10.7–11.4 对四指；s6_st3 的 this 12.7s 摊手；s7_st6、s7_st7 的动作都落在句子区间内。 |
| D3 外语与专名 | 2 | 拉丁语都对。Hospitium hic locatur 是庞贝客栈招牌套话（CIL IV 807 一类），locatur 是被动态「出租」，对；Salve/Quattuor/Convenit（成交）/Illic. Sursum.（那儿，楼上）语法和口吻都对；Vibius Restitutus 涂鸦出自庞贝客栈（CIL IV 4957），英文转述正确；注音 SAHL-weh、KWAHT-too-or、KON-weh-nit、IL-lik. SOOR-soom、VIB-ee-us res-tih-TOO-tus、ur-BAH-nah、GAH-rum 都在 prompt 里。扣分：s6_st1 prompt 台词行与规格里 hos-PIH-tee-oo heek loh-KAH-toor 仍缺词尾 -um（应为 -oom），即上一轮 I34 未改（见问题表 1）。 |
| D4 台词逻辑 | 3 | 开场「两件事：找床、试 garum」（story.md:32）→ s6_st3 钱「all the money I have left」→ s6_st1/st2 报价 Quattuor＝4 枚，付出 3 小钱＋1 大币共 4 枚，与 spec 手数一致 → s7_st1「I don't have any money left」，钱已花光，一致；「Hospitium… hospitality?」回收 s6_st3 的吆喝；dextram 回收在 s5 之前已完成（story.md:160），本范围无回头矛盾；s7_st1 的 garum 与开场目标对得上（Mission 编号已于 v2.2 去掉）；Fortunata 的 Convenit 对应 st1 的 Quattuor。 |
| D5 说话人 | 3 | s6_st1 画内只有 Fortunata 与 Riley 开口，两名行人「不说话」并在 prompt 口型行「每句只由标明的人说」；首帧图 st1_first_frame.png 里 Fortunata 嘴闭、行人在画左侧脸走过，符合 0–1.5s 的「嘴闭着」；s6_st3 的 Hospitium 标明「画外女声、不入画、画面里只有 Riley 开口」；s6_st5/st6 与 s7 各镜都是单人说话，spec 都写了「没人说话」的段落。s7_st2 首帧嘴闭带笑，对应 0–2.2s 不说话。 |
| D6 听得清 | 2 | s6_st1 的 Fortunata 回礼 Salve. 是「低声」且只有 0.4s，紧接 Riley 的 Salve!（5.1–5.6），两句之间 0 间隔，容易被吞（I35 未改，见问题表 2）；其余没问题：s6_st3 画外吆喝写明「清楚压过骡子响鼻」，s6_st6 大堂只有「很轻的碗勺声」，s7_st2 整段轻声但夜里屋内无环境噪声，所有 prompt 都带「对白优先，环境声压到对白下面」。 |
| D7 跨镜接续 | 2 | 逐个有台词的接点连起来读：s6_st3→st1「Hospitium… hospitality?」→「Hospitium hic locatur!」说话人换了，同一句拉丁语隔着一刀再喊一遍，但 Riley 刚在 st3 猜过词义，观众看到喊话的人，可以接受（记录）；s6_st1→st2「Quattuor.」→（静默 8.8s）→「Convenit.」接得上；st2→st5「Convenit.」→「Illic. Sursum.」不同事件，Fortunata 点一下头递灯，顺；st5→st6「Thank you.」→「Oh, this is basically a truck stop.」换地点，没问题；s6_st6→s7_st4 场间，「truck stop」→「Okay. Cozy.」换场；s7_st4→st6「Okay. Cozy.」→「Oh, and we've got air conditioning.」同一人接着吐槽，Oh, and 顺着前一句往下数，好；st6→st7「Cool. Cool cool cool.」→「So it's literally a bag of straw…」So 接得上；st7→st1「Rustic, I guess.」→「It's fine, though. It's a bed.」though 顺着前面的吐槽转为满意，好；st1→st2「I'd do it again.」→「People write on, like, every wall here.」换话题没有承接词，st1 末尾转头看划痕是承接，但 st2 首帧又是正对镜头（I36 未改，见问题表 3）；st2→st3「…kind of sweet.」→「Okay. I'm gonna try to sleep.」Okay. 作为收场转折，躺好，合理；st3→st5 无台词。 |
| D8 跨语言说清 | 3 | s6_st1 Riley 对听不懂英语的 Fortunata 说话：指自己（6–6.6）＋手贴脸闭眼（6.6–7.8）＋Um — sleep?，再竖一指＋One night?（7.8–9），Fortunata 竖一指点头回应（观众看得懂她懂了），随后 Quattuor 配四根手指（10.5–11.6）＋伸手要钱（11.6–13），Riley 抿嘴并摊开右拳；s6_st2 付钱一枚一枚放，Fortunata 目光落在大币上、四指轻晃，观众看得懂「还差一点」，Convenit 点头收钱；s6_st5 Illic. Sursum. 配手指往上一挑，Riley 顺着看过去再点头。没有「只一个词、没手势」的问句。 |

## 问题表

| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |
|---|---|---|---|---|---|---|
| s6_st1 | 台词行 / 1.5–3.0s | D3（I34 未改） | 记录 | ③ prompt | prompt.txt「台词」行与 spec 台词仍写 hos-PIH-tee-oo heek loh-KAH-toor，缺词尾 -um；同一句另有一处（junctions.md）更写成 loh-KAH-too，几处不统一，模型可能读成 hospitio / locato | 便宜：prompt 台词行与动作行统一改为 hos-PIH-tee-oom heek loh-KAH-toor；s6_st3 已出片不重出 |
| s6_st1 | 5.6–6.0s | D6 / D1（I35 未改） | 记录 | ② 分镜文字 | 回礼 Salve. 0.4s，低声，且与 Riley 的 Salve!（5.1–5.6）零间隔，易被 Riley 的声音吞掉 | 便宜：Salve. 放到 5.7–6.2（5–6 秒段不变，6.7 开口前仍有 0.5s），台词里写「低声但咬字清楚」 |
| s7_st2 | 0–2.2s | D7（I36 未改） | 记录 | ② 分镜文字 | st1 末尾她转头看划痕、嘴角上扬；st2 首帧（已看图）却正对镜头微笑，「People write on…」没有承接词；0–2.2s 只写「吸一口气」 | 便宜：不改词；0–2.2s 加「目光从灯苗抬向镜头、嘴角再扬一点」，让「看到划痕 → 想起一句」看得见 |
| s6_st3→st1 | st3 21.9–23.1 / st1 1.5–3.0 | D7 | 记录 | ② 分镜文字 | 观众隔一刀又听到同一句 Hospitium hic locatur!（间隔不到 4 秒） | 不用改；若觉得重复，可在 st1 0–1.5s 的吆喝前加一声前奏（先招手后开口）。接受现状也可 |
| s7_st1 | 12.3–13.7s | D1 | 记录 | ② 分镜文字 | 「yeah, I'd do it again.」5 词 1.4s＝3.6 词/秒，快于 2.5；其后到 14s 以后全是空镜，有余地 | 已出片保留，不重出；若以后重出，把这句放宽到 12.3–14.3，不改词 |
