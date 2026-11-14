# dialogue（台词（时长与逻辑））单审

- 审稿人：claude-sonnet-5-5/dialogue__a（claude-sonnet-5-5）报告 `reports/dialogue__a.md`
- 状态：完成

## 评分

| 维度 | 分 | 证据 |
|---|---|---|
| D1 说得完 | 1 | 整句语速偏快，要给镜头加长。s4_st3 第一句 13 词，识别 4.32–7.44 秒（medium 2.58–5.82 秒），3.1–3.2 秒念完＝约 4.0 词/秒，按 2.5 词/秒需 5.2 秒；s3_st4 末句 18 词用 4.3 秒（13.40→17.7）＝4.2 词/秒，需 7.2 秒，而分镜给了 7.2 秒（12.7–19.9）却被压缩；s6_st3 首句 13 词 3.3 秒＝3.9 词/秒，「Hope that's enough for a bed」6 词 1.3 秒＝4.8；s2_st8 十词 2.1 秒＝4.8；s6_st6 6 词 1.2 秒＝5.0；s5_st5「It really is just fish sauce」6 词 1.3 秒＝4.7；s1_st4 与 s1_st3 的长句约 3.5。尾部留白不足：s1_st4 0.98 秒、s4_st3 0.94 秒、s6_st3 约 1.0 秒、s8_st5 1.0 秒、s3_st3 0.76 秒、s5_st10 0.28 秒（多为镜内切点，续在下一镜，只记录）。开口前不足 1 秒：s3_st1 首个 Salve 在 0.78 秒。语速正常的有 s1_st2（2.1–2.7）、s2_st2（2.8）、s5_st1（2.2）、s8_st1（2.3）、s8_st4（2.4）。见问题表 1–3。 |
| D2 节拍对位 | 2 | s3_st4 逐格对得上：第 6–8 秒 Felix 右臂伸直指画左，同时 Hac recta platea（6.62–7.78）；ito ad dextram（8.0–8.94）手臂推；第 9–11 秒 Riley 抬手同向指，That way?（9.56）。s5_st12 的 OK 手势对 the OK sign works（5.8 秒）。扣分：s3_st7 的四句台词（Hm? / Mm-hm / Tene! / Oh — thank you!）两个识别器都没听到，无法核对手势对不对词；s5_st13 问句缩短。 |
| D3 外语与专名 | 2 | 拉丁语语法与出处总体可信：Assibus hic bibitur / Dupondium si dederis, meliora bibes 是庞贝真实涂鸦（CIL IV 1679）；Vibius Restitutus 涂鸦是真实的；Hac recta platea… ito ad dextram、Apage、Vis?、Convenit、Illic. Sursum.、Hospitium hic locatur 语法正确；s8_st6 的 Helvia 念「Dies nimin est, dum versaste, not fix」，近音对得上 Dies nihil est. Dum versas te, nox fit。扣分：garum 在 s1_st4 第 19.2 秒识别成 groom（medium 同），s7_st1 识别成 girl / Gurram，s4_st3 识别成 Garam；s3_st4 里 Felix 和 Riley 的 dextram 都识别成 dextrum。其余镜（s1_st2、s3_st4、s5_st1）识别成 garum，所以更可能是读法不稳，也可能是识别器问题。问题表 6、7。 |
| D4 台词逻辑 | 2 | 回收链顺：开场「睡觉＋garum」两件事（s1_st2 12–15 秒）→ s5_st13 买到鱼露、s6_st2/st5 租到床位；dextram（s3_st4 她说不懂）→ s5_st8 店主喊 Ad dextram → s5_st9「Dextram means right?… wrong way all day」；s4_st3 说 still going left 与 s3_st4 的 go left 一致；钱账 s1 的 9 枚 → s8_st10「one tiny coin」→ s6_st3「3 小＋1 大 all the money I have left」→ s7_st1「don't have any money left」，数字一致；十二年前地震（公元 62/63 → 75）成立。扣分：s1_st3 识别缺 They're all patched up，且 fixing 变成 patching up，意思不变，只记录；s3_st1 没听到 Unum，「买一个」的交代缺失；缺镜造成的断点见 D7。 |
| D5 说话人 | 2 | s3_st4 第 5–9 秒 Felix 张嘴（拼图第 5、6 格大嘴型）、Riley 闭嘴听；s5_st13 第 12–13 秒 Asellina 笑着脱口 Euge（识别 10.86–11.92）；s6_st3 画外 Fortunata 的 Hospitium 是画外声（19.3–21.3 秒），Riley 随后转头，说话人清楚。扣分：s2_st5 画外 Riley 的话被听成「Riley, Riley!」；s3_st7 与 s6_st5 画内人该开口的地方没有人声（问题表 4、5）。 |
| D6 听得清 | 1 | 几处该听清的台词听不清或没有。s2_st5（2–7 秒）画外「Oh, cool — a fountain.」在原条 1.5–3.1 秒，入点 2.0 秒切掉了前面大半，medium 只识别出 0–1.6 秒的「Riley, Riley!」；s3_st7 全条 13 秒两个识别器都无人声；s6_st5 全条 12 秒两个识别器无人声，RMS 120–520（有人说话的镜头为 1500–5000）；s5_st13 Riley 的问句只剩「Grim?」1.4 秒。见问题表 4、5、8。 |
| D7 跨镜接续 | 2 | 逐个有台词接点连着读：s1_st1→st2（Wait, wait — I gotta do this right. → Good morning from Pompeii!）自然，已避开 follow-up 056 的毛病；s2_st1→st2（Okay, made it.）、s3_st1→st2（Salve → Oh, it's pre-cut!）、s3_st2→st3（So smart → Mm — mm.）、s3_st3→st7（so good → Hm?）、s4_st3→st1（…garum? → Oh — oh no. That's pee.）、s4_st2→st5（Does this smell? → Nope.）、s5_st9→st2、s5_st11→st12、s5_st12→st3、s7_st4→st6→st7→st1 都像同一个人接着说。扣分：缺镜造成的接不上，见问题表 9–11；s4_st1→st2 旧条少 kicked out 一句，「So get this」接得上但丢了被轰这一拍。 |
| D8 跨语言说清 | 2 | Riley 对 Felix 的 s3_st4 是完整说法加手势：右手比倒酱、两手一摊问 garum（拼图第 1–3 格），Felix 整条手臂指路并慢速念 Hac recta platea… ito ad dextram，Riley 抬手同向确认（第 9–11 格），已避开 follow-up 062 的毛病；Asellina 竖一根、两根手指加拉丁语报价，Riley 猜价并配 OK 手势（s5_st2/st10/st11/st12）。Fortunata 报价用四根手指（s6_st2）。扣分：s5_st13 Riley 的问句实际只有一个词 garum（Grim? 1.4 秒，脚本 11 词），靠举面包瓣＋指面包补，对方听得懂、观众也猜得到，但台词被压缩，见问题表 8；s6 缺 st1 导致 Quattuor 没说出口。 |

## 问题表

| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |
|---|---|---|---|---|---|---|
| s4_st3 | 4.3–7.4 | D1 语速 | 重出 | ③ prompt | 第一句 13 词识别 4.32–7.44（medium 2.58–5.82）＝约 4.0 词/秒，按 2.5 词/秒需 5.2 秒；设计 15 秒节拍里这句没留够 | 要积分：不改句子，加长这句的节拍到约 5.5 秒（镜头到 17 秒左右），走路张望放在句前或句后 |
| s3_st4 | 13.4–17.7 | D1 语速 | 重出 | ③ prompt | 末句 18 词 4.3 秒＝4.2 词/秒，按 2.5 词/秒需 7.2 秒；分镜 12.7–19.9 本来给了 7.2 秒，模型压缩了；整条成片只用到 17.7，之后还有 4.2 秒尾部 | 要积分：节拍保持 7.2 秒并在 prompt 写明「按正常语速、说完再抬手点头」。若本镜已超重出上限，则记录，交用户定 |
| s2_st5 | 入点 2.0 秒（原条 1.5–3.1） | D6 / D5 / D2 | 重出 | ② 分镜文字 | 画外「Oh, cool — a fountain.」设计在原条 1.5–3.1 秒，成片入点 2.0 秒切掉前面大半；medium 只识别出 0–1.6 秒的「Riley, Riley!」，观众听不到这句，Vibia 回头的缘由不成立 | 便宜：入点前移到约 1.2 秒（接 st2 的画面不变）；若原条该处无完整句，则要积分重出这句画外话 |
| s3_st7 | 全条 13 秒 | D6 / D2 / D5 | 重出 | ③ prompt | 分镜四句 Hm? / Mm-hm! / Tene! / Oh — thank you!（Tene 8.9–9.2 秒，thank you 9.3–10.5 秒），small.en 与 medium 都无人声；拼图第 7–8 格 Felix 递布包、Riley 接，嘴型待核；属分诊③保留旧条 | 核实：人工听 13 秒音轨；若确无人声，则要积分重出，或后期补配（声音模块待设计，交用户定） |
| s6_st5 | 全条 12 秒 | D6 / D5 | 重出 | ③ prompt | Fortunata 的「Illic. Sursum.」（约 5–7 秒指楼梯，拼图第 6–8 格抬手）和 Riley 的 Thank you 两个识别器都没有；RMS 仅 120–520；small.en 反而出了「Oh, my God」（0–11 秒，更像幻听）；旧条分诊③ | 核实：人工听音轨；若确无人声，则 Riley 进院子去楼梯前没有指路的口头交代，要积分重出这一镜 |
| s5_st13 | 7.9–12.0 秒（成片区间 0.5–14） | D8 / D6 / D2 | 可剪 | ③ prompt | 分镜 Riley「Um — do you have any garum? For my bread?」11 词需 4.4 秒，识别只有「Garum?」（medium「Grim?」8.4–9.8 秒，1.4 秒）；靠举面包瓣和手指面包弥补（拼图第 8–10 格） | 记录：保留；用户若要整句，要积分重出。台词不为语速删改，说不下就延长镜头或重排节拍 |
| s6_st3、s2_st8、s6_st6、s5_st5、s1_st4、s1_st3 | s6_st3 8.6–18.1；s2_st8 5.1–7.2；s6_st6 6.8–8.0；s5_st5 13.8–19.4；s1_st4 18.4–22.0；s1_st3 10.6–15.2 | D1 语速 | 记录 | ③ prompt | 句内语速 3.4–5.0 词/秒：s6_st3 末句 6 词 1.3 秒（4.8）、s2_st8 10 词 2.1 秒（4.8）、s6_st6 6 词 1.2 秒（5.0）、s5_st5 6 词 1.3 秒（4.7）。短句识别时间戳误差大，可能偏高 | 便宜：先用 faster-whisper 重听，确认是否真的偏快；若确实偏快，这批镜头统一加留白重出，不删词 |
| s6_st3 → s6_st2（缺 st1） | st3 24.1 秒出画 → st2 第 0 秒 | D7 / D8 / D4 | 记录 | ② 分镜文字 | st1 缺：Fortunata 的 Salve、Riley 的「Um — sleep? One night?」和 Quattuor 都没有，st2 一开场就是伸手加四指，只靠 Convenit（8.7–10.6 秒）；Riley 在 st3 刚攥钱快步出画，观众没看到谈价过程；这批「Quattuor 四枚」只靠手指表达 | 记录：缺镜本身不报；st1 补出之前，st2 前 8 秒的空白要靠画面（四指＋摊手）撑住 |
| s7_st1 → s7_st3（缺 st2） | st1 16.2 秒 | D7 / D4 | 记录 | ② 分镜文字 | st1 结尾她转头看灯上的划痕、嘴角上扬，是 st2 涂鸦台词（Vibius Restitutus… kind of sweet）的铺垫；st2 缺，st3 直接「Okay. I'm gonna try to sleep.」，铺垫落空 | 记录：缺镜本身不报；st2 补出前，可把 st1 末尾转头一段剪掉，避免悬空 |
| s3_st4 → s4_st3（缺 st8）、s4_st5 → s8_st1（缺 s4_st4） | s3_st4 结尾；s4_st5 结尾 | D7 / D4 | 记录 | ② 分镜文字 | s3_st8 缺：Okay, bye! / Vale! / Okay… left. 都没有，st4 结尾她右手抬到胸前、Felix 笑，下一镜直接是窄街自拍 Okay, so I'm still going left；s4_st4 缺：「everything's closed / I have no idea where I am」迷路这一拍没有，s4_st5 笑完直接跳到 s8_st1「perfect time for the baths」，她怎么从迷路到想去浴场没有交代 | 记录：缺镜本身不报；补镜前注意这两处接缝 |
| s3_st1 | 3.7 秒后 | D4 / D5 | 记录 | ③ prompt | 分镜 Felix「Unum.」没听到，只有 Salve ×2（1.28–2.50、2.98–3.72）；之后 9 秒没有人声；属分诊③保留旧条（台词与现行分镜不一致） | 记录：保留；Riley 竖一根手指、Felix 点头已能表达买一个，观众看得懂 |
| s8_st6 | 6.3–9.6 秒 | D3 | 记录 | 规则源 | 「Dies nihil est. Dum versas te, nox fit.」语法成立，但我查不到古典出处，像是自编的格言；Riley 误解成 get moving 是笑点，不影响观众 | 记录：请用户确认是否自编；若要「出处」，换成真实涂鸦或谚语 |
| lines.md / junctions.md | — | D4（材料） | 记录 | 规则源 | 材料表里列了 s1_st6（Come here — see those little guys?），但 materials 里没有 s1_st6，这句其实在 s1_st4 的 12.9–22.0 秒；st4 的第一句台词写「无」，实际 12.88 秒起 Riley 开口；st4 末句 of. 之后只留 0.98 秒 | 记录：核对 workflow_catalog / 镜头表里 st4 与 st6 的关系，更新接点表 |
| s1_st4（lines 标作 s1_st6）、s7_st1、s4_st3 | s1_st4 19.2 秒；s7_st1 7.6–7.8 秒；s4_st3 6.3 秒 | D3 专名 | 存疑 | ④ 模型随机 | garum 在 s1_st4 识别成 groom（两个识别器一致）、s7_st1 识别成 girl / Gurram、s4_st3 识别成 Garam，而 s5_st1、s3_st4 能识别成 garum；s1_st4 是观众第一次听到这个词 | 核实：用另一个拉丁语或英语模型转写；若确实不是 GAH-rum，则 s1_st4 要积分重出，其余可记录 |
| s5_st2、s8_st5 | s5_st2 4.8–6.6 秒；s8_st5 约 6 秒 | D3 / D6 | 存疑 | ④ 模型随机 | Assibus hic bibitur 识别成「Asi, millisi, bibite」（medium「Assibili si bibite」）；s8_st5 Helvia 的 Vis? 两个识别器都没听到，首个识别到的字在 11.94 秒，前 11 秒无人声 | 核实：人工听这两处；Latin 单词被英文识别器吞掉很常见，如听得清就划掉 |
