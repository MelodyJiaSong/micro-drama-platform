# dialogue（台词（时长与逻辑））单审

- 审稿人：claude-sonnet-5-5/dialogue__a（claude-sonnet-5-5）报告 `reports/dialogue__a.md`
- 状态：完成

## 评分

| 维度 | 分 | 证据 |
|---|---|---|
| D1 说得完 | 2 | 多数镜按识别时间戳算正常语速：s5_st1 32 词/14.3 秒=2.24 词/秒、开口前 1.18 秒、说完后 3.64 秒；s5_st5 32 词/17.8 秒=1.80、前 1.46、后 2.24；s4_st2 47 词/21.0 秒=2.24、后 2.85。偏短的留白见问题表：s3_st4 开口前 0.43 秒（成片 0.83 起、首句 1.26）、s3_st3 说完后 0.76、s4_st3 后 0.94、s8_st5 后 1.00、s6_st3 后 1.10、s8_st2 首字在 0.00 秒；s5_st11/st12/st7 语速 2.88/2.87/2.95 词/秒略快但不到挤压。没有一镜要靠删句子救，都是剪辑点或加留白。 |
| D2 节拍对位 | 1 | s5_st8 识别「Ad dextram」在 0.00–3.18 秒，拼图第 5–8 格（4–7 秒）店主才抬臂指横街，喊和指不同步，与分镜「喊和指是同一个动作」不符；s5_st11 说完问句 9.78 秒，OK 手势在第 12–13 格（11–13 秒），分镜写「说到 right 时比 OK」；s4_st2 第 0 格拇指戳身后的门（对应「kicked out」那句）但识别从 0.94 秒「So get this」开始，该句没听到。见问题表。 |
| D3 外语与专名 | 2 | 拉丁语逐句核对：Salve / Unum / Tene / Non hic / Hac recta platea… ito ad dextram / Apage / Hospitium hic locatur（庞贝真涂鸦）/ Quattuor / Convenit / Illic. Sursum / Assibus hic bibitur · Dupondium si dederis, meliora bibes（Asellina 真涂鸦）/ Euge / Vis? / Vale，语法和时代口吻都对；medium 自动语言把 s3_st4 的 Felix 听成「Not here. Go straight and then turn right.」，释义正确，s5_st10 识别「Du pondión si deres melióra bibes」。小瑕疵：Helvia 的「Dies nihil est. Dum versas te, nox fit.」语法可行但出处不明（疑为自拟）；「garum」被识别成 Garam/Grump/Gurram/girl，读音是否 GAH-rum 需人耳听（见问题表）。 |
| D4 台词逻辑 | 2 | 回收链完整：s3_st4「so I'm just gonna go left」→ s4_st3「I'm still going left, garum's gotta be down here」→ s5_st9「"Dextram" means right? …wrong way all day」；garum 在 s3_st4 / s4_st3 / s5_st1「saving my bread for garum」/ s5_st13 / s7_st1 回收；钱账：s5_st12 手里 6 枚→付 2 枚→s6_st3「3 枚小钱＋1 枚大币」=Quattuor 4 枚→s7_st1「no money left」（s5_st3 付金币已知不算）。扣分：实际念出的话与 lines.md 多处不同（s8_st1「two is when the baths open」、s4_st5「smells like money」、s8_st10「That's it」，见问题表），以及缺镜 s7_st2（涂鸦台词）。 |
| D5 说话人 | 2 | s3_st4 拼图第 5–10 格 Felix 张嘴并伸臂、第 2–4 与 12–19 格 Riley 张嘴，说话人与识别时间一致；s8_st6 拼图第 4–9 格 Helvia 转向 Riley 说拉丁语，Riley 第 15 格才开口；s4_st2 全程只有 Riley。存疑一处：s8_st7（0.00–2.32「Hey, come on!」）与 s8_st8（「Come on」×3，2.24–10.60）按分镜是不说话的路人镜，管线识别出英文，我的 medium 重听未复现，疑为识别器把环境声听成话（见问题表）。 |
| D6 听得清 | 1 | s3_st7 带通 RMS：0.5–1.0 秒 -24dB、1.5–2.0 秒 -25dB、3.0–3.5 秒 -25dB，而「Tene!」（约 7 秒）和「Oh — thank you!」（约 8 秒）处只有 -34～-44dB，对比 s3_st1 的 Felix 「Salve」-16dB；管线与 medium 重听整镜 13 秒零识别。s6_st5 全程 -31～-48dB，识别只有幻觉的「Oh, my God」，Fortunata 的「Illic. Sursum.」和 Riley 的「Thank you.」听不到。见问题表。 |
| D7 跨镜接续 | 2 | 按 junctions.md 逐个有台词的接点连起来读：s3_st1→st2「Unum.」→「Oh, it's pre-cut!」、s3_st2→st3「That's so smart」→「Mm — mm. Okay, that's really dense」、s4_st3→st1「…garum?」→「Oh — oh no. That's pee.」、s4_st1→st2「I'm going!」→「So… get this」、s8_st9→st6「Kind of love it, though.」→「I could stay here all day.」、s5_st8→st9「Ad dextram」→「Wait. "Dextram" means right?」、s7_st6→st7「Cool cool cool」→「So it's literally a bag of straw」，都像同一个人接着说，没有重新打招呼。扣分：s6_st3→s6_st2 因 s6_st1 暂缺，价格与招呼没听到；s4_st3 开头重述「going left / garum」。见问题表。 |
| D8 跨语言说清 | 2 | s3_st4 做到位：Riley 先倒酱比划（拼图第 2–3 格）再问「Garum? Where can I get garum?」，Felix 摇头、整臂指向画左并放慢念完整句（第 6–10 格），Riley 顺着指同方向再确认「That way?」，Felix 点两下头；Asellina 的一指/二指报价（s5_st2/st10）、OK 手势互认（s5_st11/12）、Fortunata 四指+Convenit 都配了看得懂的动作。扣分：s3_st1 的「Unum」+竖一指没听到也没看到（见问题表）；s6_st5 的「Illic. Sursum.」只看到手势不明显指向楼梯（拼图第 6–7 格抬手靠近头侧）；s8_st6 的 Helvia 朝门口摆手出现在第 20 秒，在 Riley 解读「get moving」之后。 |

## 问题表

| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |
|---|---|---|---|---|---|---|
| s3_st7 | 约 7–8 秒（Tene! / Oh — thank you!） | D6 | 重出 | ④ 模型随机，③ 机检应抓「应有台词无识别」 | 管线识别（无）+ medium 重听零识别；带通 RMS 7–8 秒仅 -34～-44dB，对比 s3_st1 的 Felix -16dB；开头 0.5–3.5 秒有三处 -24/-25dB 的短声（疑为「Hm?」「Mm-hm」）。分镜写 Felix「洪亮」的 Tene! 听不到，布包递出（拼图第 7 格）没有话 | 人耳听 7–9 秒确认；确实没有就重出（要积分）。不要为此改台词 |
| s6_st5 | 0–12 秒 | D6 | 重出 | ④ / ③ | 全程 -31～-48dB；管线识别成「Oh, my God」跨 0–11 秒（幻觉）；Fortunata「Illic. Sursum.」（压低声音）与 Riley「Thank you.」听不到；拼图第 6–7 格 Fortunata 抬右手靠近头侧，没有明显指向院子左后方楼梯 | 人耳听；若确认太轻或没说，重出并在 prompt 里要求清晰可闻 + 手臂指向楼梯（要积分）；只是偏轻则后期提升该段音量（便宜） |
| s3_st4 | 成片 0.83 秒起 | D1 | 可剪 | ② 剪辑 | 首句「Garum?」识别 1.26 秒，成片入点 0.83 秒，开口前仅 0.43 秒（规则 ≥1 秒）；分镜节拍 0–1.2 秒两人安静 | 入点前移到约 0.26 秒（便宜，剪辑）；原条 0–1.2 秒是安静帧 |
| s3_st3 / s4_st3 / s6_st3 / s8_st5 / s6_st5 | 出点 | D1 | 可剪 | ② 剪辑 | 说完后留白：s3_st3 末词 9.24 秒、出点 10.00 秒=0.76 秒；s4_st3 13.98→14.92=0.94 秒；s6_st3 23.90→25.00=1.10 秒；s8_st5 15.00→16.00=1.00 秒；s6_st5 11.08→12.00=0.92 秒（识别不可靠）。规则 ≥1.5 秒 | 原条有余量就把出点后移到至少 +1.5 秒（便宜）；没有余量则下一镜入点前留静帧或让下一镜开场晚 0.5–1 秒（便宜）。不改台词 |
| s5_st11 | 9.78 秒 vs 11–13 秒 | D2 | 记录 | ③ | 识别念成「Is that what you're saying?」（9.56–9.78），分镜是「Is that — right?」配 OK 手势；OK 手势出现在拼图第 12–13 格（11–13 秒），晚于问句约 2 秒。s5_st12 Asellina 回 OK 仍成立 | 记录；下次出片 prompt 写明手势落在问句最后一个词；本条可留 |
| s4_st2 | 0.21–1.0 秒 | D2 / D4 | 记录 | ③ prompt | 分镜第一句「So I just got kicked out of a Roman laundromat」，拼图第 0 格拇指戳身后的门，但识别和 medium 重听都从「So, get this」（1.0 秒）开始，「kicked out」那句没了；「His son was like, "Dad, that's disgusting,"」也变成间接转述「Apparently his son thought that was disgusting」（13.3–18.9 秒），无学儿子口气；成片起点 0.21 秒，开口前 0.73 秒 | 记录；st1 已演了被轰出，观众不缺信息。要保留「学儿子口气」的笑点则重出（要积分）；否则 lines.md 对齐到实际台词（便宜） |
| s6_st3→s6_st2 | 接点（s6_st1 暂缺） | D7 | 记录 | ② 缺镜 | s6_st3 末 Riley 听到吆喝走出画（「Hospitium… hospitality?」23.46–23.90 秒），下一镜 s6_st2 直接是 Fortunata 摊手四指、Riley 摊钱；「Salve」「Um — sleep? One night?」「Quattuor」都没有，价格只靠四指和 4 枚钱传达 | 补 s6_st1（要积分）；补之前该接点可接受，但「Quattuor」听不到 |
| s3_st4→s4_st3 | 接点（s3_st8 暂缺） | D7 | 记录 | ② 缺镜 | s3_st4 末「so I'm just gonna go left」，s3_st8 的「Okay, bye! / Vale! / Okay… left.」缺；下一场 s4_st3 开口就是「Okay, so I'm still going left, and garum's gotta be down here somewhere.」，在没离开面包房的情况下重述了「left」和「garum」 | 补 s3_st8 后此处自然；补之前 s4_st3 首句可保持（转场另审） |
| s7_st1→s7_st3 | 接点（s7_st2 暂缺） | D4 | 记录 | ② 缺镜 | s7_st1 末她回头看墙上划痕笑，下一镜 s7_st3 直接晚安；涂鸦台词（Vibius Restitutus…Urbana）的回收没出现，墙上划痕观众无从知道意义 | 补 s7_st2（要积分）；暂缺期间 s7_st1 末尾回头看划痕可保留，但没有后续 |
| s8_st2 | 0.00 秒 | D1 | 记录 | ③ | 识别「Salve.」0.00–1.62 秒，开口前 0 秒；承接 s8_st1「Yeah. Baths.」时转场过急 | 若原条前面还有帧则入点前移；否则可接受（有意的紧接） |
| s8_st1、s8_st10、s4_st5、s3_st2、s7_st3 | 各镜 | D4 | 记录 | ② / ③ | 实际念出与 lines.md 不同：s8_st1 识别「Apparently they do their afternoon thing right around two, and two is when the baths open, so bath time.」（script：perfect time for the baths. / Yeah. Baths.）；s4_st5「Nope, just smells like money. Honestly, he's got a point.」（script：Nothing. Just, like, metal.）；s8_st10「it was literally one tiny coin to get in. That's it.」（script：That's, like, nothing.）；s3_st2 末「had sliced bread first. Love that.」（script：That's so smart.）；s7_st3「I'm gonna sleep」缺「try to」 | 记录；不是逻辑错。lines.md 以脚本为准，审稿看「听到的」，建议 lines.md 附实际识别稿（便宜） |
| s5_st8 | 0.00–3.18 秒 vs 拼图第 5–8 格（4–7 秒） | D2 | 存疑 | ③ prompt | 识别「Daxiram!」0.00–2.40、2.62–3.18；拼图店主在第 1–4 格站着，第 5–8 格才抬臂指横街，喊声比指向早约 2 秒，且早于车夫抬手一指（第 4 格前后）；分镜写「喊和指是同一个动作」 | 人耳听 0–3 秒是否确为店主的喊声；确认错位则重出（要积分），或把此条放到 s5_st9 之前并后移音轨（便宜，但会失同步） |
| s3_st1 | 约 3.7–13 秒 | D8 / D2 | 存疑 | ③ | 识别只有两个「Salve.」（1.28–2.50、2.98–3.72），没有 Felix 的「Unum.」；拼图第 4–8 格没看到 Felix 竖一指回应；分镜要求 Riley 竖指指面包、Felix 竖指回一个词 | 人耳听；确认缺失则 s3_st1 数量交流不完整，观众看不出买一个，重出（要积分） |
| s8_st7、s8_st8 | 0.00–2.32、2.24–10.60 秒 | D5 | 存疑 | ④ / 识别器 | 管线识别出「Hey, come on!」「Come on, come on, come on」，两镜分镜没有台词（路人不说话）；medium 重听无输出 | 人耳听；若真有人声说英文就是外来人声，重出（要积分）；否则是环境声误识，记录即可 |
| s8_st6 | 5.5–12.6 秒 | D3 | 存疑 | ① 故事 | Helvia「Dies nihil est. Dum versas te, nox fit.」识别器听不到拉丁语；出处不明，疑为自拟格言；语法可行（dum + 直陈式现在时） | 核出处或接受为仿格言；用拉丁语转写模型重听 5.5–12.6 秒核发音（便宜） |
| s7_st1、s5_st13、s4_st3 | 多处 | D3 | 存疑 | ④ | 「garum」被识别成 Gurram（s7_st1 6.1–8.2 秒）/ girl / Grump（s5_st13 8.44–9.84 秒，只识别到这一词）/ Garam，目标读音 GAH-rum；s5_st13 Riley 的问句「Um — do you have any garum? For my bread?」只剩一个词，开口前 7.94 秒 | 人耳听 garum 读音是否 GAH-rum；读成 GUR-um 就重出（要积分），读音可接受则记录 |
