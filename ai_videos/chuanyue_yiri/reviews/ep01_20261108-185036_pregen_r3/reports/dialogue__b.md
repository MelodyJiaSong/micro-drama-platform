---
worker_id: dialogue__b
stage: 3
role: validator
status: complete
confidence: high
blockers:
  - 正常语速模板仍覆盖逐镜快慢要求
  - 停顿长度与部分台词窗口尚未对齐
  - 问路路线及反应拍存在未修矛盾
---

# ep01 第三轮出片前独立审稿：台词（时长与逻辑）

范围：s2 → s3 → s4 → s8 → s5 → s6 → s7。只审 D1–D6，不审场一成片；仅为核目标编号读取故事稿开场。未读其他审稿人的报告及 reconcile。未调用收费服务、未提交生成、未运行 tick。

材料：任务书、BRIEF、materials/index.md、lines.md、58 份 spec.md、58 份当前 prompt 与 manifest、previous.md 本类别 14 项、changes.md、故事稿、bible、相关人物卡与 r05 台词库。当前 58 份 prompt 与本单 snapshot/prompts 逐文件 SHA256 相同。逐张查看 spec 所列 58 张首帧、58 张 overhead、58 张 overhead_ref，以及 manifest 去重后的 25 张人物/场景/道具参考图，共 199 张；仅在内存中排列查看，未保存拼图。索引七场均为“镜组：无”。

本轮没有指定新视频、音轨、ASR 或时间对齐结果。以下评分针对出片前的文字与参考图；不能证明实际发音、口型或混音已合格。未用旧片声音替当前 prompt 作证。

## 评分表

- D1 1 证据：脚本统计 37 个有台词镜头、58 个发声窗口；全部镜头首句前 ≥1.1 秒、末句后 ≥1.5 秒。但 37 份 prompt 的口型行仍统一“正常语速与口型”，与 s3_st4“飞快”、s4_st4“说得慢”、s8_st6“语速从容”相冲突；s2_st8、s8_st1、s5_st9、s7_st7 的停顿预算不足或未量化，详见问题表与计算表。
- D2 1 证据：s3_st4 动作总述仍说“她说话时 Felix 抬眼”，节拍却在 Riley 12.8 秒说完后，13–14.5 秒安排他的独立反应；s8_st6 的 5.1–8.8 秒仍未拆两句与翻手落点。s6_st3 13.6 秒听吆喝的剪辑依赖已经写明。
- D3 2 证据：s5_st13、s7_st1 当前 prompt 均有 GAH-rum；s8_st6 已用短 u 的 dum /dʊm/；s5_st13 当前为 EW-geh、两音节、硬 g，已非 changes 所述 YOO-geh。Petronius 41 原文与两句浴场对白相符，Terence 问路句是有删节的改编。小瑕疵是 r05:142 仍留 doom，:148 仍留未说明连读的 EH-oo-geh，详见问题表。
- D4 1 证据：目标一找床、目标二试 garum，与 s5_st7“Mission two: done”及 s7_st1 总结一致；钱数 9→7→6→4→0 枚闭合。但 s3_st4“Straight… then dextram”接 s3_st8 出店即左转，直行阶段仍未交代；s4_st2 的 his nose 指代歧义仍在。
- D5 3 证据：出片前说话人映射清楚：s3_st1 为 Felix 1.6–2.2 秒→Riley 2.8–3.6 秒；s8_st6 为 Riley 1.6–4.3 秒→画右 Helvia 5.1–8.8 秒→Riley 10.1–12.8 秒，首帧两人左右位置对应；s5_st8 明确画右粗嗓男店主喊话，Riley 不说话。s6_st3 已改为“只生成 Riley 自己的两句话”。本分仅证明文字和静态参考的映射，不冒充动态口型验收。
- D6 1 证据：s8_st1 已明确墙后低音量实声，s6_st6 5.4–7.4 秒已有“很轻的碗勺声”；但 s3_st1 的隆隆磨声和 s8_st4 的出水声仍无对白期降音量要求，58 份 prompt 中未找到“对白清楚在前/环境声降低/对白优先”。实际声轨可懂度待出片，详见问题表。
- R 1 证据：I45 部分修复；I46 当前 prompt 修复、r05 未齐；I60 原声样错挂条件已消失；I61 文字风险减轻；I62 仍待音轨；I63、I64 未修；I86 原文保留但不构成时序矛盾；I87、I89 生成端文字已修；I88、I90、I91、I92 未修。下表逐项给当前证据。

## 问题表

“重出”表示若按现文出片会把矛盾带入视频；当前尚在出片前，所列修改均可先以便宜的文字/编译修改处理，不代表本轮已经需要花积分重出视频。

| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |
|---|---|---|---|---|---|---|
| 全部有台词镜，例 s3_st4、s4_st4、s8_st6 | 2.3–5.2；7.1–12.9；5.1–8.8 | D1·语速模板；R I45 | 重出 | ③ prompt 或首帧 / 规则源 | 37 份当前 prompt 均有“正常语速与口型”；与此同时明确要求 Felix 飞快、Riley 慢说、Helvia 从容。第 3 轮仍把冲突同时送给模型。 | 便宜：口型行改为“语速和停顿以本镜台词括号及动作时间窗为准；未指定时用正常语速；口型同步”，重编并核对。 |
| s3_st4 → s3_st8 → s4_st3 | 8.2–12.8 → 1.5–3.5/6–9 → 1.7–3.2 | D4·路线逻辑；R I88 | 重出 | ① 故事 / ② 分镜文字 | s3_st4 复述“Straight… then dextram”；s3_st8 只从柜台走两步到街上便向左走，首帧与两份俯视图也没有先沿街直行、到街口再转弯的阶段；s4_st3 随即“Left. Definitely left.”。词义误猜成立，两步路线与画面对应仍断开。 | 便宜：采用单一方向指令 Ito ad dextram!，Riley 改“Okay… dextram. No clue. Sounds like left?”；或保留原台词并补明确的先直行、到街口才左转。故事、分镜、prompt 同步。 |
| s3_st1；s8_st4；有台词镜声音模板 | 1.6–3.6；2.6–7.3 | D6·对白层级；R I63/I64 | 重出 | ③ prompt 或首帧 / 规则源 | s3_st1 画面行仍为“只听得见隆隆的磨声”，未指定对白时更轻；s8_st4 出水汩汩与自嘲对白共存；模板仅限制声音种类和禁配乐，未规定对白优先。这里报的是可修改的输入缺口，并非断言新片已经听不清。 | 便宜：加“对白清晰置前，人物说话时环境声降低”；s3_st1 再明确磨声低于 Salve / Sal-VAY。出片后耳听并复核识别，混音可修则后期处理；只有实际错读/漏句且无法修复才要积分。 |
| s2_st8；s8_st1；s5_st9；s7_st7 | 4.5–8.5；6.1–13.8；1.6–7.3；6.8–7.9 | D1·停顿预算；R I45 | 存疑 | ② 分镜文字 / ③ prompt 或首帧 | 分别允许总停顿 ≤0.429、0.914、1.771、0.386 秒，才能保持 ≤2.8 词/秒；原文却用“半拍”“一拍”或省略号而没有秒数。若半拍=0.5 秒、一拍=1 秒，则分别 2.86、2.84、2.97、3.33 词/秒。拍长未定义，因此不是实际超速实测。 | 便宜：明确停顿秒数并扩窗；按上述假设，四窗至少 4.072、7.786、5.929、1.215 秒，另留表演余量。也可把 s8_st1 改“Hear that? Temple of Isis. Pompeii's two o'clock alarm. Time for the baths.”，s7_st7 改“Rustic.”，同步定稿后重算。 |
| s3_st3；s4_st1；s5_st12 | 1.6–4.3；2.6–4.4；3.6–5.8 | D1·自然停顿余量 | 存疑 | ② 分镜文字 | 6 词的嚼食评价总停顿预算仅 0.557 秒，规格却要求“词与词之间停一下”；5 词的 Oh—oh no… 总预算仅 0.014 秒；6 词的 Ha!… 总预算仅 0.057 秒。纯词数勉强可放，嚼食、重复感叹和笑声后的停顿未落实。 | 便宜：给 Oh 和 Ha 独立的停顿秒数并放宽窗口；s3_st3 可写“Mm… dense, smoky. So good.”并安排咽下后说。若不改台词，按总停顿量反推扩窗，不把全镜留白充作句内时间。 |
| s3_st4 | 8.2–12.8 / 13–14.5 | D2·反应拍；R I90 | 记录 | ② 分镜文字 | 动作总述“她说话时 Felix 抬眼…鼓起腮帮憋住笑”，节拍明确放在她说完以后；当前 prompt 仍同时携带两版时序。 | 便宜：总述改“她说完后 Felix 才抬眼…”，保留 13–14.5 秒独立反应。 |
| s8_st6 | 5.1–8.8 | D2·翻手对词；R I92 | 记录 | ② 分镜文字 | 只给两句拉丁语一个合并窗口，指“第二句时”翻手，没有指定落在 versas，也未留可验证的句间停顿。 | 便宜：例如 5.1–6.3 秒 Dies nihil est.，6.3–6.8 秒停，6.8–8.8 秒 Dum versas te, nox fit.，在 versas 时翻掌；重新核词速和自然度。 |
| s4_st2 → s4_st5 | 7.1–13.4 → 0–3.1 | D4·his 指代；R I91 | 记录 | ① 故事 | Dad held a coin up to his nose 中 his 既可能是儿子也可能是 Dad；下一镜 Riley 自己闻钱，仍会强化歧义。当前 story 与 prompt 都保留原句。 | 便宜：改“His son called it gross — so Dad held up a coin: ‘Smell anything?’”（13 词），不靠模糊代词定位鼻子；保留 6.3 秒窗并重算停顿。 |
| r05 台词库 #21/#27；关联 s8_st6、s5_st13 | 不适用（规则源） | D3·注音来源未同步；R I46 | 记录 | 规则源 | r05_衣着语言黑名单.md:142 仍写 doom；:148 仍写 EH-oo-geh，未明确 eu 一音节。当前 Helvia 卡与 s8_st6 已改 dum；当前 s5_st13 为 EW-geh、两音节硬 g。changes 所述 YOO-geh 已不是送出版本。 | 便宜：同步 r05 为短 u 的 dum，以及 eu 合成一音节、与 geh 共两音节的提示；可补 /ˈeu̯.ɡe/，避免以后复制旧注音。 |
| s8_st1、s8_st4、s6_st6、s5_st8，以及拉丁语镜 | 待出片 | D6·可懂度 / D3·实际读音；R I62 | 存疑 | ④ 模型随机 | 本单为 pregen，无对应当前材料的新声轨或 ASR；静态图和音色文字不能证明低声、隔墙声、远处喊声，以及 Salve 对比实际清楚。 | 便宜：出片后逐句耳听，截取拉丁语用对应语言转写辅助核对；识别与耳听不一致时再区分识别器错与演员错。本轮不伪造重听结论。 |

## 逐句计算

脚本在本次会话内执行，未另存代码或数据。统计规则为 `[A-Za-z]+(?:['’-][A-Za-z]+)*`：缩写、连字符词各算一个词，标点不算词。因此 I'm 是 1 词；Okay, okay — I'm going! 是 **4 词**，不是 previous I45 的 5 词。该窗口 4÷1.6=2.50，扩至 7.7–9.3 秒后的这项已修，不能沿用旧错误计数判失败。语速不能替代音节难度判断。

计算式：净词速=N÷(结束−开始−句内停顿)；允许总停顿=(结束−开始)−N÷2.8。后者是无需猜“拍长”的硬预算。表中停顿 P 为透明的排演假设：明确半拍暂按 0.5 秒、一拍暂按 1 秒；未定长省略号暂按 0.5 秒；s4_st4 两个句间停顿暂合计 1 秒。其他句末/呼吸未擅自追加。P=0 表示未扣停顿，不能解释为台词必须连读。s7_st7 6.3–6.8 秒那半拍已在窗外，表中 0.5 秒是 Very… 中的另一个未定长停顿假设。出片必须用实际发声/静音区间替换假设。

| 镜头 | 发声窗（秒） | 原句/连续语段 | 词数 N | 试算停顿 P（秒） | 净词/秒 | ≤2.8 时允许总停顿（秒） |
|---|---|---|---|---|---|---|
| s2_st2 | 1.5–6.5 | No sewers on most of these streets — the street IS the drain. | 12 | 0.5 | 2.67 | 0.714 |
| s2_st2 | 6.5–9.5 | That's what the stepping stones are for. | 7 | 0 | 2.33 | 0.500 |
| s2_st8 | 4.5–8.5 | And yeah… apparently a woman in pants is a lot. | 10 | 0.5 | 2.86 | 0.429 |
| s3_st1 | 1.6–2.2 | Salve! | 1 | 0 | 1.67 | 0.243 |
| s3_st1 | 2.8–3.6 | Salve! | 1 | 0 | 1.25 | 0.443 |
| s3_st2 | 3.6–7.4 | Pre-sliced bread. Before sliced bread was even a thing. | 9 | 0 | 2.37 | 0.586 |
| s3_st3 | 1.6–4.3 | Mm. Dense… kinda smoky. So good. | 6 | 0.5 | 2.73 | 0.557 |
| s3_st4 | 1.1–1.7 | Garum? | 1 | 0 | 1.67 | 0.243 |
| s3_st4 | 2.3–5.2 | Hac recta platea… ito ad dextram! | 6 | 0.5 | 2.50 | 0.757 |
| s3_st4 | 8.2–12.8 | Okay. Straight… then 'dextram.' No clue. Sounds like left? | 9 | 0.5 | 2.20 | 1.386 |
| s4_st1 | 2.6–4.4 | Oh — oh no. That's pee! | 5 | 0 | 2.78 | 0.014 |
| s4_st1 | 6.1–6.6 | Apage! | 1 | 0 | 2.00 | 0.143 |
| s4_st1 | 7.7–9.3 | Okay, okay — I'm going! | 4 | 0 | 2.50 | 0.171 |
| s4_st2 | 1.3–5.6 | They wash clothes in pee. And the emperor? He taxes it. | 11 | 0 | 2.56 | 0.371 |
| s4_st2 | 7.1–13.4 | His son called it gross — so Dad held a coin up to his nose: "Smell anything?" | 16 | 0.5 | 2.76 | 0.586 |
| s4_st3 | 1.7–3.2 | Left. Definitely left. | 3 | 0 | 2.00 | 0.429 |
| s4_st4 | 7.1–12.9 | It's noon. Everything's closed. I'm totally lost… and I still smell like pee. | 13 | 1 | 2.71 | 1.157 |
| s4_st5 | 2.6–3.1 | …Nope. | 1 | 0 | 2.00 | 0.143 |
| s5_st1 | 1.6–6.3 | Clean-ish. And starving. Good news? Dinner here is at three-thirty. | 10 | 0 | 2.13 | 1.129 |
| s5_st2 | 4.1–6.2 | Assibus hic bibitur! | 3 | 0 | 1.43 | 1.029 |
| s5_st5 | 2.1–9.3 | Salty… funky… and then — whoa. It's basically fish sauce. My grandma would put this on everything. | 16 | 1 | 2.58 | 1.486 |
| s5_st7 | 5.1–7.8 | Mission two: done. Now… a bed. | 6 | 0.5 | 2.73 | 0.557 |
| s5_st8 | 1.6–2.6 | Dextram, dextram! | 2 | 0 | 2.00 | 0.286 |
| s5_st9 | 1.6–7.3 | Wait… "dextram" is right? …I went the wrong way all morning. | 11 | 2 | 2.97 | 1.771 |
| s5_st10 | 1.6–5.3 | Dupondium si dederis, meliora bibes. | 5 | 0 | 1.35 | 1.914 |
| s5_st11 | 1.6–6.3 | One coin, cheap stuff… two coins, the good stuff? | 9 | 0.5 | 2.14 | 1.486 |
| s5_st12 | 3.6–5.8 | Ha! The OK sign works here! | 6 | 0 | 2.73 | 0.057 |
| s5_st13 | 8.6–9.2 | Garum? | 1 | 0 | 1.67 | 0.243 |
| s5_st13 | 10.4–11 | Euge! | 1 | 0 | 1.67 | 0.243 |
| s5_st14 | 9.1–11.9 | They water the wine down. Everybody does. | 7 | 0 | 2.50 | 0.300 |
| s6_st1 | 1.5–3 | Hospitium hic locatur! | 3 | 0 | 2.00 | 0.429 |
| s6_st2 | 8.7–9.5 | Convenit. | 1 | 0 | 1.25 | 0.443 |
| s6_st3 | 6.3–7.5 | Sun's going down. | 3 | 0 | 2.50 | 0.129 |
| s6_st3 | 7.9–12.5 | This is what's left of the budget… and still no bed. | 11 | 0.5 | 2.68 | 0.671 |
| s6_st6 | 5.4–7.4 | Ha — it's a truck stop. | 5 | 0 | 2.50 | 0.214 |
| s7_st1 | 1.5–2 | Okay. | 1 | 0 | 2.00 | 0.143 |
| s7_st1 | 2.3–3.6 | Bed? Found. | 2 | 0.5 | 2.50 | 0.586 |
| s7_st1 | 4–5.3 | Garum? Tasted. | 2 | 0.5 | 2.50 | 0.586 |
| s7_st1 | 5.7–7.2 | Budget? …Gone. | 2 | 0.5 | 2.00 | 0.786 |
| s7_st2 | 2.2–4.6 | People write on every wall here. | 6 | 0 | 2.50 | 0.257 |
| s7_st2 | 5–6.9 | My favorite, from history class: | 5 | 0 | 2.63 | 0.114 |
| s7_st2 | 7.3–12.8 | Vibius Restitutus slept here alone… missing his Urbana. | 8 | 0.5 | 1.60 | 2.643 |
| s7_st2 | 13.3–17.3 | Two thousand years from now, people will still read it. | 10 | 0 | 2.50 | 0.429 |
| s7_st3 | 1.5–2.8 | Okay. Bedtime. | 2 | 0 | 1.54 | 0.586 |
| s7_st3 | 3.2–6 | Who knows where I'll wake up tomorrow… | 7 | 0 | 2.50 | 0.300 |
| s7_st3 | 6.4–7.8 | Goodnight from Pompeii. | 3 | 0 | 2.14 | 0.329 |
| s7_st4 | 6.6–7.2 | Cozy. | 1 | 0 | 1.67 | 0.243 |
| s7_st6 | 3.3–4.3 | Air conditioning. | 2 | 0 | 2.00 | 0.286 |
| s7_st6 | 6.8–8.8 | And… that's the bathroom. | 4 | 0.5 | 2.67 | 0.571 |
| s7_st7 | 4.8–6.3 | Straw mattress. Ropes underneath. | 4 | 0 | 2.67 | 0.071 |
| s7_st7 | 6.8–7.9 | Very… rustic. | 2 | 0.5 | 3.33 | 0.386 |
| s8_st1 | 6.1–13.8 | Hear that? That's the Temple of Isis — basically Pompeii's two o'clock alarm. And at two, everybody hits the baths. | 19 | 1 | 2.84 | 0.914 |
| s8_st4 | 2.6–7.3 | It's SO hot in here. And I'm fully dressed. Rookie mistake. | 11 | 0 | 2.34 | 0.771 |
| s8_st6 | 1.6–4.3 | I could stay here all day. | 6 | 0 | 2.22 | 0.557 |
| s8_st6 | 5.1–8.8 | Dies nihil est. Dum versas te, nox fit. | 8 | 0.5 | 2.50 | 0.843 |
| s8_st6 | 10.1–12.8 | I'm pretty sure that means "get moving." | 7 | 0 | 2.59 | 0.200 |
| s8_st9 | 5.1–9.6 | No soap. You just oil up… and scrape it all off. | 11 | 0.5 | 2.75 | 0.571 |
| s8_st10 | 1.1–3.1 | Cover charge? One tiny coin. | 5 | 0 | 2.50 | 0.214 |

这 58 个窗口覆盖全部 37 个有台词镜头；其余 21 镜无指定对白。s8_st6 的拉丁两句合并窗口来自原规格，单独句长尚未锁定，已报 D2。s3_st3 另有词间停顿；若真的每个词都分开停，表中仅扣一处省略号会低估耗时。s4_st2 后半句 **16 词**，扣 0.5 秒仍为 2.76，放宽后的窗口已达数值要求。s6_st3 后半句 11÷(4.6−0.5)=2.68；s8_st9 11÷(4.5−0.5)=2.75，均已改善。s7_st2 四段分别为 6/2.4、5/1.9、8/(5.5−0.5)、10/4.0；含独立人名放慢的余量，不再因整段总词数误判。

### 镜头进出留白

下表是首句开口前 / 末句结束后，均从 spec 的精确对白窗计算；不是每个对话轮次之间也要空 1.5 秒。中途接话、指定独立反应按该镜节拍另审。最小首句前留白 1.1 秒，最小末句后留白 1.5 秒，全部达到本维度的镜头首尾阈值。

| 镜头 | 开口前（秒） | 说完后（秒） |
|---|---|---|
| s2_st2 | 1.5 | 1.5 |
| s2_st8 | 4.5 | 2.5 |
| s3_st1 | 1.6 | 9.4 |
| s3_st2 | 3.6 | 1.6 |
| s3_st3 | 1.6 | 2.7 |
| s3_st4 | 1.1 | 3.2 |
| s4_st1 | 2.6 | 1.7 |
| s4_st2 | 1.3 | 2.6 |
| s4_st3 | 1.7 | 6.8 |
| s4_st4 | 7.1 | 3.1 |
| s4_st5 | 2.6 | 4.9 |
| s5_st1 | 1.6 | 2.7 |
| s5_st10 | 1.6 | 2.7 |
| s5_st11 | 1.6 | 2.7 |
| s5_st12 | 3.6 | 2.2 |
| s5_st13 | 8.6 | 3.0 |
| s5_st14 | 9.1 | 3.1 |
| s5_st2 | 4.1 | 2.8 |
| s5_st5 | 2.1 | 2.7 |
| s5_st7 | 5.1 | 3.2 |
| s5_st8 | 1.6 | 10.4 |
| s5_st9 | 1.6 | 2.7 |
| s6_st1 | 1.5 | 8.0 |
| s6_st2 | 8.7 | 4.5 |
| s6_st3 | 6.3 | 4.5 |
| s6_st6 | 5.4 | 3.6 |
| s7_st1 | 1.5 | 1.8 |
| s7_st2 | 2.2 | 1.7 |
| s7_st3 | 1.5 | 4.2 |
| s7_st4 | 6.6 | 2.8 |
| s7_st6 | 3.3 | 2.2 |
| s7_st7 | 4.8 | 4.1 |
| s8_st1 | 6.1 | 3.2 |
| s8_st10 | 1.1 | 4.9 |
| s8_st4 | 2.6 | 2.7 |
| s8_st6 | 1.6 | 2.2 |
| s8_st9 | 5.1 | 3.4 |

## 外语、专名与逻辑核验

- Salve / Apage / Euge：均为可成立的招呼、驱赶、赞叹短语；不是现代语法硬译。Salve 有 [Plautus《Curculio》原文](https://www.thelatinlibrary.com/plautus/curculio.shtml)支持；Euge 可见 [《Aulularia》IV.vi](https://www.thelatinlibrary.com/plautus/aulularia.shtml)，并有 [BBAW Lewis–Short 词条](https://cld.bbaw.de/lemma/lat/euge)支持赞叹义。Felix 的 SAHL-weh 与 Riley 故意念成 Sal-VAY 的差异已明确写入 s3_st1 prompt；故意的错误不能报成 Latin 错读。Euge 当前 EW-geh 是改善后的近似注音，最终仍需耳听 eu 合音与硬 g。
- Hac recta platea… ito ad dextram：hac/recta/platea 配合成立，ito 为命令形式，ad dextram 为向右；当前是删节拼接的改编，不宜称逐字完整原句。[Terence《Adelphoe》原文](https://www.thelatinlibrary.com/ter.adel.html)在 581–583 行附近还含前后路线条件。语法本身不判错；本报告的 D4 问题是改编后两步指路与 Riley 的实际走法未统一。
- s5_st2/st10 报价： [意大利国家钱币机构的庞贝专题第16页](https://www.pompei.numismaticadellostato.it/static/repository/guidaPompei/PNS_Guida_Pompei12_en/files/basic-html/page16.html)展示 CIL IV 1679，支持一 as 与两 as 的报价阶梯。铭文有 dipundium 拼写，prompt 用规范化 Dupondium，属于可说明的规范化，不是金额差错。
- s8_st6：[Petronius《Satiricon》41](https://www.thelatinlibrary.com/petronius1.html)能逐字核到当前两句。Dies 为主语、nihil est 为判断，dum 从句与 nox fit 成立，口语化省略自然；“get moving”是 Riley 明说“pretty sure”的误猜，不是报告应替她改成正确翻译。
- Hospitium hic locatur / Convenit：分别可作此处招租和成交回应。r05 已把前者从 CIL IV 807 招牌转成吆喝标为创作转用；其原链接本次未成功打开，未冒充已独立核对铭文图。两句的当前 prompt 注音均在；实际咬字未审。
- Vespasian 已不在本范围定稿台词，故不沿用旧专名误读问题。Garum 的三处问话/总结已有前重音提示；s7_st2 的 Vibius Restitutus / Urbana 是 Riley 的英语叙述，有放慢与读音提示。CIL IV 2146 的 [Ancient Graffiti Project 数据条目](https://agp.wlu.edu/Graffiti/graffito/AGP-EDR197679)搜索结果支持人名与缺席 Urbana 的转述；详情页本次返回 502，原铭文图片未核，不能据此给字形真实性打分。
- 钱数：初始 7 as + quadrans + sestertius；s3_st1 付2 as→7枚；s8_st2 付 quadrans→6枚；s5_st3 付2 as→4枚；s6_st2 付3 as+sestertius→0枚。s7_st1 Budget gone 与之对应。s4 闻钱后放回，不是额外消费。
- “all morning”在下午回顾上午迷路，语法与时序均成立，不需要仅因场景在下午就强改 all day。s5_st8 先听见店主、再目击右转、s5_st9 才悟出 dextram 的回收成立；s8_st6 的误译和当日两项目标也都明确。
- 实际外语转写未执行：本轮没有对应的新音轨。没有把拉丁语识别器缺词当演员错读，也没有把未听过的发音判通过。

## 上一轮逐项复核

| I 编号 | 本轮结论 | 当前证据 |
|---|---|---|
| I45 | 部分已修，不能关闭 | s4_st1 退场句为4词，2.50词/秒；s4_st2后半16词，扣半秒2.76；s6_st3后半扣半秒2.68；s8_st9扣半秒2.75；s7_st2分段有窗。仍有正常语速模板冲突和未量化停顿，见问题表。s5_st12、s4_st1首句、s3_st3仍需自然停顿余量；s7_st7不能只看整句6词就放行。 |
| I46 | 当前送出注音已修；来源表待齐 | s5_st13、s7_st1 GAH-rum 已进 prompt；s8_st6 dum 已进 prompt 和 Helvia 卡；s5_st13 当前是 EW-geh，不是 changes 的 YOO-geh。r05:142/:148 仍旧注音。Felix 问路语法可成立，Salve 对比待声音实测。 |
| I60 | 旧问题条件已消失；动态结果未审 | 当前 s5_st8 与 s8_st6 manifest 均无 c1_Riley_audio，也无其他音频 ref，不能继续声称“只挂 Riley 声样”。两镜有店主粗嗓/Helvia略低带笑的文字声线；s8_st6 其实是 Riley—Helvia—Riley 三轮发言。声音归属出片再听。 |
| I61 | 文字风险明显减轻，实际声音待核 | s8_st1 画面行已指墙后实声、低音量、隔墙发闷，避免把合唱当配乐；但未明确 6.1–13.8 秒相对低声对白的压低幅度。并入 D6 统一对白优先修法。 |
| I62 | 待验证，不能当已修 | s6_st6 5.4–7.4秒有轻碗勺声；其余低声/远喊仍无新音轨或ASR可审。本轮只核可懂度设计。 |
| I63 | 未修 | s3_st1 当前 prompt 仍为“只听得见隆隆的磨声”，未给 1.6–3.6秒 Salve 对比安排对白期降声。 |
| I64 | 未修 | 58份声音模板仍只列保留种类和禁配乐；无统一对白优先指令，相关噪声镜也未补齐。 |
| I86 | 未改字，但不判问题 | 下午回忆“all morning”成立；她中午已明确说迷路、下午已去过浴场，仍可回顾上午走错。把它换成 all day 反而扩大断言。 |
| I87 | 生成端文字已修；剪辑实施待核 | s6_st3 当前动作与节拍写明13.6–14.6秒的吆喝取自 s6_st1，剪辑贴作画外声。本单没有已完成剪辑，不能把“写了”当“贴了”。 |
| I88 | 未修 | s3_st4仍保留 Straight… then；s3_st8仍为出柜台到街上直接左转；原问题保留，见D4。 |
| I89 | 已修 | s6_st3明确“本镜只生成 Riley 自己的两句话”，与Fortunata吆喝由剪辑加入的分工不冲突；不再禁掉Riley自身人声。 |
| I90 | 未修 | s3_st4总述仍“她说话时”，而反应窗仍13–14.5秒，在Riley12.8秒结束后。 |
| I91 | 未修，小指代瑕疵 | s4_st2仍写 Dad held a coin up to his nose；s4_st5仍由Riley闻自己的钱。 |
| I92 | 未修 | s8_st6仍把拉丁两句合并5.1–8.8秒，仅写第二句翻手；没有逐句落点或 versas 对位。 |

## 整体观察

Vision 要求观众像在古城过了一天；独立反应和静默镜有助于它，不能用急读抵消。
本轮首尾留白普遍充分，主要风险已集中为句内停顿、模板优先级和少量叙事衔接。
I45 的“5词”旧计数错误已纠正，不把已修内容再次判失败。
当前拉丁语注音整体改善，来源表仍需同步；静态材料无法证明实际发音与混音。
建议先处理问题表中的便宜改动，再由调用方按流程收轮；本报告未放行生成。

给调用方摘要：最低分D1/D2/D4/D6/R为1。优先处理语速模板冲突、问路两步路线、对白层级、四处停顿预算、Felix反应时机。报告已写至本文件；未运行tick，由调用方凭运行日志登记。
