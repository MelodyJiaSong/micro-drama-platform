# dialogue__a 报告（台词：时长与逻辑 · s1 · 第 2 轮）

方法：按各镜 spec/prompt 的节拍窗口，用脚本数词（连字号词算 1、75 AD 按 seventy-five A D 算 3 个发声单位）算词/秒、开口前与说完后余量。未重听音频（出片前无音轨）。

| 镜 | 句 | 词数 | 窗口(s) | 词/秒 | 开口前 | 说完后 |
|---|---|---|---|---|---|---|
| st1 | Okay… I just time-traveled. Almost two thousand years back. | 9 | 5.5–10 | 2.0 | 5.5s | 2.0s（12s 镜） |
| st2 | Good morning from Pompeii! It's May, 75 AD.（9 词，75 AD 读 3 单位） | 9 | 1.5–5.5 | 2.25 | 1.5s | 接 Mission one |
| st2 | Mission one: find a bed before dark. | 7 | 5.5–8.5 | 2.33 | - | - |
| st2 | Mission two: try garum — the sauce this whole town's famous for. | 11 | 8.5–13 | 2.44 | - | - |
| st2 | And my budget… is this. | 5 | 13–16 | 1.67 | - | 3.0s（19s 镜） |
| st3 | They had a huge earthquake twelve years ago. They're still fixing it. | 12 | 7.5–12.5 | 2.4 | 7.5s | 1.5s（14s 镜） |
| st4 | See those tiny fish? Future garum. | 6 | 12.5–15.5 | 2.0 | 12.5s | 2.5s（18s 镜） |

## 评分表
- D1 2 证据：全部 ≤2.8 词/秒（st1 2.0、st2 最高 2.44、st3 2.4、st4 2.0）；开口前均 ≥1.5s；说完后 st1 2.0s、st2 3.0s、st4 2.5s 均达标，但 st3 说完后恰好 1.5s（12.5–14s），无余量；st2 前三句之间没有写停顿，靠句内标点
- D2 3分 证据：st1 5.5s 开口、说完 10–12s 回头看城；st2 说到 this whole town 时（8.5–13s 窗）拇指指城、And my budget 举拳 is this 摊手，与 spec 节拍一一对应；st3 6.5–7.5s 转身扬眉后 7.5s 开口、同时挑夫走远；st4 11.7–12.5s 凑近镜头后 12.5s 说话、「See those tiny fish?」后停半拍
- D3 2 证据：st2 prompt 第 18 行已注 Pompeii 读 pom-PAY、75 AD 读 seventy-five A-D、garum 读 GAH-rum；st4 第 17 行注 garum；st1 的 time-traveled、st3 的 twelve years ago 无需注音；小瑕疵：st3 无专名但 quake 年份 62/63 AD→75 AD 为 12–13 年，twelve 可接受；st2 的 garum 发音「GAH-rum」是英语借词读法，非拉丁原音，需出片后转写核
- D4 3分 证据：story.md 第 21 行 Mission one=find a bed、Mission two=garum；story.md 第 27 行 Future garum 回收 Mission two；第 133 行 "Mission two: done. Now… a bed." 与第 139 行 "still no bed" 回收一致；第 31 行 earthquake twelve years ago（63→75）正确；dextram 在 s1 范围外（story 第 65–67 行 Felix 说右、Riley 猜左，后面回收），s1 不涉及
- D5 2 证据：st1/st2 画面只有 Riley；st3 有工人和挑夫、st4 有两渔夫，prompt 第 17–18 行「口型」行写了「每句只由标明的人说，其他人不开口」，spec 已删「嘴微微张开」（grep 张嘴=0）；但 st3/st4 声音行仍只写「仅保留本镜指定对白…」，未像 st5 加「本镜没有人说话」，路人出声的防护弱于 st5
- D6 2 证据：st1/st3/st4 台词行已写「吐字清楚，海浪声/骡蹄回声/浪声压在对白下面」（prompt 第 16/17/17 行）；小瑕疵：st1 Riley 离镜头约 4.5–5m 全景低声说话，仅靠文字约束，是否听得清要出片后 faster-whisper 逐词核（previous I39 仍待核）
- R 2 证据：I12/I36 已改（st3 缩为 12 词、2.4 词/秒、spec 14s），余量 1.5s 刚好达标；I19/I20 已改（三镜台词行均加清晰度/层级）；I34/I37/I38 已改（st2 prompt 第 18 行注读法）；I39 属出片后核对，待办；I35 未改好（见问题 1）

| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |
|---|---|---|---|---|---|---|
| s1_st3 / s1_st4 | 全程 | D5 说话人（I35 未改） | 记录 | ③ prompt | st3、st4 prompt 末行「声音：仅保留本镜指定对白、自然环境声和动作声；不要背景音乐或配乐。」无「除 Riley 外无人说话」；st5 同位置有「本镜没有人说话」；st3 有工人（愣住/点头）、st4 有渔夫 | 便宜：st3/st4 声音行加「除 Riley 外本镜没有人说话，路人不出声」（编译器模板按镜出人数时统一加） |
| s1_st3 | 12.5–14 | D1 | 记录 | ② 分镜文字 | 12 词/5s=2.4 词/秒，两句间未写停顿；说完恰留 1.5s，无余量；悄悄话略慢则压缩到 <1.5s | 便宜：把开口提前到 7.2s（转身拍 6.5–7.5 提前半拍），或第二句并入「They're still fixing it.」前写明句间停 0.3s；不够再考虑 15s（要积分） |
| s1_st2 | 1.5–8.5 | D1 | 记录 | ② 分镜文字 | 前两句（9+7 词）合计 16 词放 7s（1.5–8.5）平均 2.29，但各句之间没写停顿；实际句间若各停 0.3s，第一句 4s 内 9 词（含 3 个年份发声单位）≈2.25→2.5 词/秒，仍在线内但接近上限 | 记录即可；出片后 ASR 看实际起止 |
| s1_st1 | 5.5–10 | D6 | 存疑 | ④ 模型随机 | previous I39：st1 全景 4.5–5m 低声说话，旧条无台词版转写为空，没有 ASR 验证 | 出片后 faster-whisper 对 st1 不喂剧本转写；逐词 p<0.8 或漏词再后期提对白 |

## 整体观察
- 台词量整体偏松（st1 2.0、st4 2.0 词/秒），仅 st3 余量卡在 1.5s 边界。
- 编号与回收（Mission one/two、Future garum、twelve years ago）在 s1 内与 story 全集一致，无逻辑冲突。
- 读音注释到位（Pompeii、75 AD、garum），拉丁语仅 garum 一词，无语法问题。
- 其他：无。
