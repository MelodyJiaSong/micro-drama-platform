# dialogue__a 报告（台词：时长与逻辑 · 第 3 轮 · claude-sonnet-5-5）

方法：按各镜 spec.md「节拍」里的说话窗口（括号内秒数）用脚本数词，算词/秒；核开口前、说完后留白；核拉丁语与 story.md 第 21/65/67/113/115 行、prompt.txt 的台词、声音、口型行。未重听音频（出片前无声轨）。未逐张看首帧图（本类别只看文字与台词）。

## 评分表
- D1 2 证据：脚本数 43 个说话窗口，全部 ≤2.8 词/秒。最紧：s4_st1「Oh — oh no. That's pee!」5 词/1.8 s=2.78；s5_st12 6 词/2.2 s=2.73。扣停顿后略超：s2_st8 10 词/(4.0−0.5 s)=2.86，s8_st1 19 词/(7.7−1.0 s)=2.84。开口前最短 s8_st10 1.1 s，其余 ≥1.3 s。说完后最短 s2_st2 9.5→11 s=1.5 s，s3_st2 7.4→9 s=1.6 s，s4_st1 9.3→11 s=1.7 s，s7_st2 17.3→19 s=1.7 s，s7_st1 7.2→9 s=1.8 s，均 ≥1.5 s。
- D2 2 证据：s3_st4 动作总述仍写「她说话时 Felix 抬眼瞄她」，节拍却是 13–14.5 s（她说完 12.8 s 之后）才抬眼，I90 未改。s8_st6 节拍仍是单窗「5.1–8.8 秒」说两句、手一翻，无分句时间，I92 未改。其余各镜台词与动作对位：s2_st2 的 drain 与 stepping stones 手势各在自己的句窗内（1.5–6.5、6.5–9.5 s）；s7_st1 每个问句有各自秒数。
- D3 2 证据：Garum 在 s3_st4、s5_st13、s7_st1 都有 GAH-rum 注音（I46 已改）。s8_st6 注 dum /dʊm/。Hospitium、Convenit、Apage、Assibus、Dupondium 都带古典注音。「Assibus hic bibitur…」是 CIL IV 1679 的真涂鸦。小瑕疵：s5_st13 prompt 第 19 行写 EW-geh，changes.md 写 YOO-geh，两处不一致。s3_st4 的 ito 是将来式命令，口语更常见 i。s8_st6「Dies nihil est. Dum versas te, nox fit.」语法通顺，但是新编句，没有出处，要在片尾说明或标「自拟」。
- D4 2 证据：Mission one 找床（story.md 第 21 行）、Mission two 吃 garum（s5_st7）、s7_st1「Bed? Found. Garum? Tasted. Budget? Gone」都对得上。钱数账本对：7 枚红铜币付面包 2、付酒 2，剩 3 枚加大黄铜币（s6_st3 掌心 3+1），全部付给 Fortunata 后钱尽。迷路线 Hac recta platea…ito ad dextram → 猜 left → s4_st3「Left. Definitely left.」→ s5_st8/st9 回收 dextram，通顺。小瑕疵：s5_st9「all morning」，该镜在下午（I86 未改）；s4_st2「held a coin up to his nose」his 指代不明（I91 未改）。
- D5 3 证据：s2_st8 Vibia 只表情不出声，节拍 4.5–8.5 s 仅 Riley 说；s8_st6 节拍 5.1–9 s「只有她张嘴」；s6_st3 括注「本镜只生成 Riley 自己的两句话」，吆喝贴 s6_st1（I89 已改）；s5_st8 店主喊 1.6–2.6 s 时 Riley 反应拍「停住头转」不张嘴；s8_st10 门房不说话。manifest 里没有 Riley 音频参考，I60 的串音隐患在 prompt 层面不存在。
- D6 2 证据：s8_st1 prompt 第 12 行写明合唱与叉铃「音量低、隔着墙闷闷的」；s6_st6 写明说话时只剩很轻的碗勺声（I62 已改）。但所有 prompt 第 2 行与末行的声音模板仍只写「仅保留本镜指定对白、自然环境声和动作声」，没有「对白在前、说话时环境声降低」（I64 未改）。s3_st1 的「隆隆的磨声」没写音量（I63 未改）。Salve 与 Sal-VAY 的对比靠 1.6–3.6 s 听清，有风险。
- R 2 证据：已改好：I45（s4_st1 窗口 7.7–9.3 s，s4_st2 16 s，s8_st9 窗口 5.1–9.6 s，s8_st1 窗口 6.1–13.8 s）、I46（注音补齐）、I62（s6_st6）、I87、I89。仍未改：I61/I64（对白优先指令，prompt 模板第 2 行与末行不变）、I63（磨声音量）、I86（all morning）、I88（只在 s3_st4 的 prompt 第 20 行保留，逻辑已通，不再算问题）、I90、I91、I92。

## 问题表

| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |
|---|---|---|---|---|---|---|
| 全部有台词镜（规则源） | 全程 | D6·无对白优先指令 | 记录 | 规则源 | prompt.txt 第 2 行与末行声音模板无「对白压过环境声」；s8_st1 合唱、s3_st1 磨声与对白重叠（I64/I63/I61 未改） | 便宜：模板加「对白清楚在前，人物说话时环境声降低」；s3_st1 磨声写「低低地从画外传来，对白时更轻」；重编译 |
| s8_st1 | 6.1–13.8 s | D1·边缘 | 记录 | ② 分镜文字 | 19 词，扣句间 1.0 s 停顿后 2.84 词/秒，又是压低声音，叉铃合唱同时在响 | 便宜：删 And at two，改成 Hear that? Temple of Isis… Pompeii's two o'clock alarm. Everybody hits the baths. 之类，或窗口放宽到 14.3 s |
| s2_st8 | 4.5–8.5 s | D1·边缘 | 记录 | ② 分镜文字 | 10 词，扣半拍停顿后 2.86 词/秒 | 便宜：窗口放宽到 4.3–8.7 s，或删 apparently |
| s4_st1 | 2.6–4.4 s | D1·边缘 | 记录 | ② 分镜文字 | 5 词/1.8 s=2.78，含破折号停顿，又要求「大声、清清楚楚」 | 便宜：窗口放宽到 2.6–4.6 s（节拍后移 0.2 s） |
| s3_st4 | 动作总述 vs 13–14.5 s | D2 | 记录 | ② 分镜文字 | 总述「她说话时 Felix 抬眼」与节拍「她说完后 13–14.5 s 才抬眼」相抵（I90） | 便宜：总述改为「她说完后 Felix 才抬眼」 |
| s8_st6 | 5.1–8.8 s | D2 | 记录 | ② 分镜文字 | 两句拉丁语共用一个窗口，翻手时机交给模型（I92） | 便宜：拆成 5.1–6.4 Dies nihil est. / 6.6–8.8 Dum versas te, nox fit.，versas 时手翻 |
| s5_st9 | 1.6–7.3 s | D4 | 记录 | ① 故事 | 「I went the wrong way all morning」所在镜在下午第九时（I86 未改） | 便宜：改 all day，story.md 第 115 行同步 |
| s4_st2 | 7.1–13.4 s | D4·指代 | 记录 | ① 故事 | held a coin up to his nose，his 可指儿子或爸爸（I91） | 便宜：改 held a coin up to his son's nose（多 1 词，6.3 s 内仍 ≤2.6 词/秒） |
| s5_st13 | 10.4–11.0 s | D3 | 记录 | ③ prompt | prompt 写 EW-geh，changes.md 写 YOO-geh，注音不统一 | 便宜：统一为一种，并同步剧级词库与人物卡 |
| s8_st6 | 5.1–8.8 s | D3·出处 | 存疑 | ① 故事 | 「Dies nihil est. Dum versas te, nox fit.」不是已知的庞贝涂鸦，疑似自拟；Riley 译成「get moving」是玩笑译法 | 便宜：确认是自拟后在剧级词库标注，不当作真实涂鸦宣传 |

## 整体观察
1. 台词窗口整体宽裕，全部 ≤2.8 词/秒；有 3 处扣停顿后接近或略超，都是便宜的文字改动。
2. 开口前与说完后的留白全部达标，最紧的 s2_st2 刚好 1.5 s，没有余量。
3. 迷路线（Felix 说右、Riley 猜左、s5 回收 dextram）、两个 Mission、钱数账本前后一致，没有硬伤。
4. 拉丁语注音覆盖完整，真实涂鸦（Assibus hic bibitur、Hospitium hic locatur、Vibius Restitutus）与自拟句（Dies nihil est）建议在词库里标清。
5. 上一轮 I63/I64/I90/I92 的「便宜」改动这轮仍没做，且 I64 是全局模板问题，值得出片前一次改掉。

其他：s8_st1「Temple of Isis … two o'clock alarm」的史实依据我没核，属于时代类审稿。
