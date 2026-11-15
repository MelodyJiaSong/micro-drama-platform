# dialogue（台词（时长与逻辑））单审

- 审稿人：claude-sonnet-5-5/dialogue__a（claude-sonnet-5-5）报告 `reports/dialogue__a.md`
- 状态：完成

## 评分

| 维度 | 分 | 证据 |
|---|---|---|
| D1 说得完 | 1 | s6_st1 全部够：Hospitium hic locatur! 3 词/1.5s（1.5–3.0，2.0 词/秒）、Um — sleep? 2 词/0.9s、One night? 2 词/0.7s、Quattuor 0.7s，开口前 1.5s、说完后 13−11.4=1.6s。但 s7_st2 仍偏快（同 r1 I38，未改）：I swear it was in my history textbook — 8 词/2.8s（8.1–10.9）=2.86 词/秒；from an inn just like this. 6 词/1.9s（11.3–13.2）=3.16 词/秒；第一句 8 词/3.0s=2.67；And there's this famous one — 5 词/1.9s=2.6；That's kind of sweet. 4 词/1.7s=2.35；引文 10 词/6.2s=1.6 慢且有停顿，整镜总共 43 词，说话区间 2.3–23.4 = 21.1s，开口前 2.3s、说完后 2.6s 够。问题只在中段节拍太挤、引文段给得太松，镜头不必加长，重排即可（见问题表）。 |
| D2 节拍对位 | 3 | s6_st1 每句对到动作：Hospitium 在 1.5–3.0 对招手加目光跟行人；Um — sleep? 在 6.7–7.6 对掌心贴脸歪头；One night? 在 7.9–8.6 对竖一指；Quattuor 在 10.7–11.4 对四指；s7_st2 every wall 在 2.3–5.3 里对瞟墙加拇指，just like this 约 13.0 对左手一摊；首帧里 Fortunata 右手在肩前手心朝自己，与 0–1.5s 的往回招一致。 |
| D3 外语与专名 | 2 | s6_st1 台词块 hos-PIH-tee-oo heek loh-KAH-toor 丢了词尾 -um 的 m（古典读法 -oom），与 r1 I40 同，仍未改（只在 s6_st3、s6_st5 已出片镜重出时才一起改的约定，st1 本轮重画，其实可以顺手改，见问题表）；Hospitium hic locatur（「此处出租住宿」，locare 被动）、Salve、Quattuor（KWAHT-too-or）语法与时代口吻对；s7_st2 Vibius Restitutus＝VIB-ee-us res-tih-TOO-tus、Urbana＝ur-BAH-nah 注音已进 prompt「台词」块。没有本机重听（出片前无音频）。 |
| D4 台词逻辑 | 3 | story.md 第 32 行开场目标「sleep ＋ garum」，s7_st1 回收 garum（lines.md 第 34 行）「still thinking about that garum…I'd do it again」，s6_st1 的 Salve 在 story.md 第 80 行面包师处已教过，Quattuor 配四指加摊开 3 红铜＋1 黄铜币，s7_st2 引文与 s7_st1 的「no money left」不冲突；没有「Mission one」编号残留。 |
| D5 说话人 | 3 | s6_st1 每句人标清楚：Fortunata 吆喝、Riley/Fortunata 互 Salve（5.1–5.6 / 5.6–6.0）、Riley 英文、Fortunata Quattuor；两行人 prompt「动作」改成「不说话」，口型行「其他人不开口」不再矛盾（r1 I39 起因已消）；s7_st2 只有 Riley 一人，画面里只有她。 |
| D6 听得清 | 2 | s6_st1 行人已不说话，吆喝（1.5–3.0）前后无抢声；小瑕疵：Fortunata「低声回 Salve.」只有 0.4s（5.6–6.0），而且紧跟在 Riley 刚走到位的脚步声后，模型容易吞掉；s7_st2 全程轻声、屋内只有灯与夜风，窗洞外无环境音设定，清楚。 |
| D7 跨镜接续 | 2 | 逐接点出声读：s6_st3 末「Hospitium… hospitality?」→ s6_st1 首「Hospitium hic locatur!」是 Riley 循声来到 Fortunata 吆喝的同一句，Riley 3.5s 入画，成立；s6_st1 末 Quattuor（11.4）→ s6_st2 首 Convenit，成立；s7_st1 末「…yeah, I'd do it again.」（剪辑出点 16.75s，面朝镜头）→ s7_st2 首 2.2s 无声吸气后「People write on, like, every wall here.」，换话题但中间有一口气与停顿、语气从放松变轻柔，勉强成立，小瑕疵：没有一句过渡词（如 Oh — and…），情绪从满足突然转到温柔，靠 2.2s 静默承担；s7_st2 末「That's kind of sweet.」→ s7_st3 首「Okay.」成立（笑着垂眼后转入睡意）。 |
| D8 跨语言说清 | 3 | s6_st1 6–9s Riley 指自己→掌心贴脸歪头闭眼→竖一指，加上 Um — sleep? One night?，是完整说法加手势；Fortunata「看着手势、眉毛一抬、竖起一指点头」，10.5–11.6s 左手四指手心朝镜头加 Quattuor，11.6s 伸手要钱，Riley 低头看拳、摊开钱币，观众看得懂；不是单词无手势问句，没有 s3 面包师那种张嘴吸气表情。 |

## 问题表

| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |
|---|---|---|---|---|---|---|
| s7_st2 | 8.1–13.2 | D1 | 记录 | ② 分镜文字 | I swear it was in my history textbook — 8 词排 2.8s（2.86 词/秒）；from an inn just like this. 6 词排 1.9s（3.16 词/秒），都高于 2.5；引文 10 词却给了 6.2s（1.6 词/秒），后面留白 2.6s 有富余。 | 便宜（只改 prompt 节拍文字，视频未出）：词不动，重排：People write… 2.3–5.3；And there's this famous one — 5.7–7.9；I swear it was in my history textbook — 8.3–11.4（3.1s）；from an inn just like this. 11.7–14.1（2.4s，just like this 的一摊约 13.4）；It says, 14.5–15.0；引文 15.5–22.0；That's kind of sweet. 22.4–24.0；末尾留白约 2s，仍 ≥1.5s；26 秒不必加长。同步改动作段里 5.5–8 / 8–11.2 / 11.2–13.6 的分段标注。 |
| s6_st1 | 1.5–3.0 | D3 | 记录 | ② 分镜文字 | 台词块与 prompt「台词」块注音 hos-PIH-tee-oo 缺词尾 -um（古典 -oom），模型或读者可能读成 hospitio；这镜本轮重出，prompt 反正要重新生成。 | 便宜：st1 注音改 hos-PIH-tee-oom heek loh-KAH-toor；s6_st3、s6_st5 已出片，只在重出时再改，不为此单独重出。 |
| s6_st1 | 5.6–6.0 | D6 | 记录 | ③ prompt | Fortunata「低声回 Salve.」只有 0.4s，紧挨 Riley 停步的 5.0–5.6，容易被吞。 | 便宜：Salve. 区间放宽到 5.7–6.2（节拍里 5–6 秒段不变），并在台词里写「低声但咬字清楚」。 |
| s7_st1→st2 | 末 / 0–2.2 | D7 | 记录 | ② 分镜文字 | 末句「I'd do it again.」后直接换话题「People write on, like, every wall here.」，没有承接词；st1 末尾她转头看划痕、st2 首帧却已正对镜头（I8 已定 wontfix，出点 16.75s 在回头前）。 | 便宜：不改词（台词 r3 定稿）；在 st2 0–2.2s 的吸气前加一个小动作：嘴角一扬、目光从灯苗抬向镜头，让「安静下来，想起另一件事」看得见。 |
