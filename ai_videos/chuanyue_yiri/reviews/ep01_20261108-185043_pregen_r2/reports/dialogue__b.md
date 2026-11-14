# dialogue__b · 场一台词（时长与逻辑）· 出片前 R2

审查范围：s1，播放顺序 st1 → st2 → st4 → st3 → st5。本报告分数评价本轮文字与参考图的可执行性，不表示新视频的发音、口型或混音已经实测通过。未读取另一位审稿人的报告或 reconcile 文件；未运行 tick，未调用生成服务。

## 评分表

- D1 2 证据：脚本逐句计数见下表；st1/st2/st4/st3 首次开口前分别为 5.5/1.5/12.5/7.5 秒，镜尾留白分别为 2/3/2.5/1.5 秒。st3 改为 12 词，句间停 0.5 秒后为 12÷4.5＝2.667 词/秒；st2 1.5–5.5 秒读出的 10 单位仅容许合计 0.429 秒停顿，仍有小瑕疵，见 B01。
- D2 3 证据：st2 prompt:14 将 this whole town 与左拇指指城、And my budget 与举拳、is this 与摊钱分别绑定；st4 prompt:13 在 5–8 秒放下鱼筐，12.5–15.5 秒才说 See those tiny fish；st3 prompt:13 先于 5.6–6.5 秒看修补裂缝，7.5 秒才解释地震。五张首帧与两版俯视图均已目检，未见必须边背对镜头边说这些台词的冲突。
- D3 3 证据：st2 prompt:18 已明确 Pompeii＝pom-PAY、75 AD＝seventy-five A-D、garum＝GAH-rum 且重音在前；st4 prompt:17 沿用同一 garum 注读。Merriam-Webster 的 Pompeii 词条列有两音节 päm-ˈpā，不能因 Cambridge 另列三音节读法就判当前注音错误。garum 为有古典出处的鱼露名词；本场没有当地人的拉丁语整句、Vespasian 或 dextram 发声，相关语法和外语音轨转写不适用。来源和核查边界见下文。
- D4 3 证据：story.md 场一与本轮四个有词镜头的英文相符；st2 的 Mission one＝找床、Mission two＝尝鱼露，与故事场六 Mission two: done. Now… a bed.、场八 Bed? Found. Garum? Tasted. 对得上。初始 7＋1＋1＝9 枚，场一只展示不支出；故事后续付 2 枚、1 枚小铜币、2 枚、最后 3 枚小钱＋大黄铜币，枚数归零。地震 twelve 与本剧 r01:80–81 的 63 年取值及 75−63＝12 相容；不在本类别把 62/63 年史学争议判成编号错误。
- D5 3 证据：四个有词镜头均只标 Riley；st1/st2/st4/st3 prompt:17/19/18/18 均有“每句只由标明的人说，其他人不开口”。st3 工人已由旧“嘴微微张开”改为愣住及点头，st4 渔夫只笑、拢鱼；st5 prompt:2、20 明确本镜没有人说话。首帧 st2 中央 Riley 闭嘴微笑，st3 她背向镜头、工人弯腰，均处在台词前；不把这些静态图当成口型同步实测。
- D6 3 证据：st1 prompt:16 明确“吐字清楚，海浪声压在对白下面”，st4 prompt:17 明确浪声在对白下面，st3 prompt:17 明确骡蹄回声在对白下面；声音行禁止配乐。出片前声场指令已经补齐，实际可懂度尚待新条核听，见 B02，不借用旧条转写为新条放行。
- R 2 证据：I12 已改为 st3 的 8＋4＝12 词；I19、I20 已补三镜对白优先级；I34 已补 A-D 字母读法；I35 虽登记仍 open，当前四份口型行已约束唯一说话人，st3 也已删“嘴微微张开”，文本风险已解决；I36 缩句后允许 0.714 秒总停顿，0.5 秒停顿可行；I37 数字注读已解决，但首段停顿预算仍未写明，部分解决，见 B01；I38 Pompeii 和年代注读已补且地名读法有词典依据；I39 缺新条实测，本轮文字补救已做，实际核听仍待出片，见 B02。

## 问题表

| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |
|---|---|---|---|---|---|---|
| s1_st1、s1_st4、s1_st3 | 设计对白窗 5.5–10、12.5–15.5、7.5–12.5 秒；无本轮新条 | D6·低声对白实测；R·I39 | 存疑 | ④ 模型随机 | 本轮只提供出片前文字、参考图，没有与当前输入对应的新音轨或 ASR；st1 约 4.5 米全景低声、st3 拱顶蹄声与低声并行。新增优先级指令可核实，实际字尾是否被遮盖无法核实；previous.md 所述旧条结果不能替代本轮。 | **便宜**：出片后先无提示转写，再逐句人耳核听三窗，记录实际起止和漏词；有漏词时先判断识别器问题与真被遮盖，并尝试提对白、压环境声。仅确认源对白本身缺失或不可修复时才考虑**要积分**重出；本轮不据此要求重出。 |
| s1_st2 | 设计 1.5–5.5 秒 | D1·数字展开与停顿；R·I37 | 记录 | ② 分镜文字 | Good morning from Pompeii! 为 4 单位，It's May, seventy five A D. 为 6，共 10；4−10÷2.8＝0.429 秒是两个句子、逗号和其他呼吸的总停顿预算。若停顿合计 0.5 秒则为 2.857 单位/秒；当前未规定停顿长度，不能据此声称已实际超速。 | **便宜**：明确这一拍合计停顿约 0.25–0.35 秒；或改为“Morning from Pompeii! It's May, 75 AD.”，保留现有注读，减至 9 单位，留 0.5 秒后为 2.571 单位/秒。若采用改写，同步故事、分镜、台词汇总与 prompt；不必增加视频时长。 |

## 计数与时间证据

已用 JavaScript 脚本逐句计数。书面词口径保留缩写、连字符；保守发声单位把 75 AD 展开为 seventy five A D，把 time-traveled 拆成 time traveled。后者比普通书面词数更保守，不把它混称为音节数。没有逐句独立时间码的两句使用共窗，不能伪造各句实际起止。

计数核心：`lexical = text.match(/[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*/g).length`；发声单位先执行 `replace('75 AD','seventy five A D').replaceAll('-',' ')`，再按保留撇号的词正则计数。净语速＝单位数÷（窗口−停顿），停顿上限＝窗口−单位数÷2.8。下列停顿是可行性试算，未给定的停顿不冒充 prompt 指令或实测。

| 镜头／句子 | 书面词数 | 保守发声单位 | 分镜窗口（秒） | 该句在 2.8 单位/秒时的最短净发声（秒） |
|---|---:|---:|---|---:|
| st1：Okay… I just time-traveled. | 4 | 5 | 与下一句共用 5.5–10 | 1.786 |
| st1：Almost two thousand years back. | 5 | 5 | 同上 | 1.786 |
| st2：Good morning from Pompeii! | 4 | 4 | 与下一句共用 1.5–5.5 | 1.429 |
| st2：It's May, 75 AD. | 4 | 6 | 同上 | 2.143 |
| st2：Mission one: find a bed before dark. | 7 | 7 | 5.5–8.5 | 2.500 |
| st2：Mission two: try garum — the sauce this whole town's famous for. | 11 | 11 | 8.5–13 | 3.929 |
| st2：And my budget… is this. | 5 | 5 | 13–16 | 1.786 |
| st4：See those tiny fish? | 4 | 4 | 与下一句共用 12.5–15.5 | 1.429 |
| st4：Future garum. | 2 | 2 | 同上 | 0.714 |
| st3：They had a huge earthquake twelve years ago. | 8 | 8 | 与下一句共用 7.5–12.5 | 2.857 |
| st3：They're still fixing it. | 4 | 4 | 同上 | 1.429 |
| st5：无台词 | 0 | 0 | 0–13 全段环境声 | — |

| 镜头／节拍 | 单位数／窗口 | 含停顿平均值 | 停顿试算 | 扣停顿后语速 | 在 2.8 上限内最多可停 |
|---|---|---:|---:|---:|---:|
| st1 全部台词 | 10／4.5 秒 | 2.222 | 合计 0.5 秒 | 2.500 | 0.929 秒 |
| st2 报地点、年月 | 10／4 秒 | 2.500 | 合计 0.5 秒 | 2.857 | 0.429 秒 |
| st2 目标一 | 7／3 秒 | 2.333 | 合计 0.25 秒 | 2.545 | 0.500 秒 |
| st2 目标二 | 11／4.5 秒 | 2.444 | 合计 0.5 秒 | 2.750 | 0.571 秒 |
| st2 预算 | 5／3 秒 | 1.667 | 合计 0.5 秒 | 2.000 | 1.214 秒 |
| st4 两句 | 6／3 秒 | 2.000 | 合计 0.5 秒 | 2.400 | 0.857 秒 |
| st3 两句 | 12／5 秒 | 2.400 | 合计 0.5 秒 | 2.667 | 0.714 秒 |

“说完后 ≥1.5 秒”按本轮镜尾留白核对，不解释为同一连续对白每句之间必须停 1.5 秒。st1 最后迈步结束到开口为 1 秒；st3 转身准备拍为 1 秒；st4 转身凑近镜头的准备拍为 0.8 秒，但镜头起口前已有 12.5 秒，未发现需要额外挤掉对白时间的文字要求。st3 镜尾 1.5 秒刚好达标，缩句后仍需按 12.5 秒前说完执行。

## 外语、口语与逻辑核查

本场只有 Riley 的现代美式英语。garum 是英文句中的食物名称；不是让当地人说的一整句拉丁语，不需要虚构拉丁语语法审查或对应语言 ASR 结果。Perseus 的 [Lewis and Short 原词条](https://atlas.perseus.tufts.edu/dictionaries/entry/urn%3Acite2%3Ascaife-viewer%3Adictionary-entries.atlas_v1%3Alat.ls.perseus-eng2-n19320/)收 gărum，并引 Pliny 31.93，词义支持本场用法；剧内 r02_吃与住.md:141–149 另有鱼露与庞贝、小鱼的来源。GAH-rum 已在两个 prompt 里统一指定首音节重读。英语借词的元音存在词典差异，[Cambridge 的 garum 词条](https://dictionary.cambridge.org/us/dictionary/english/garum)列美音 /ˈɡer.əm/；本报告不把该词典与指定借词读法的差异直接等同为生成读错，也不宣称已听过本轮发音。

Pompeii 的 pom-PAY 与 [Merriam-Webster 所列两音节读法](https://www.merriam-webster.com/dictionary/Pompeii)相容，故 I38 不因漏写末尾 ee 重新报错；[Cambridge](https://dictionary.cambridge.org/us/pronunciation/english/pompeii)列三音节形式，属于本次查到的另一读法。A-D 已明确逐字母读，不能把 AD 当英语单词 ad。

“See those tiny fish? Future garum.” 先点出鱼，再把它解释为将来的鱼露，避免旧句把活鱼直接认作成品；问句加简短回答符合她向观众分享秘密的口吻。“They're still fixing it.” 的 it 回指地震造成的损坏，在看到新补裂缝之后说，口语可懂。两个目标各有后续回收，场一未误报已经完成目标。故事场三猜 dextram＝left、场六目击向右手势后纠正，逻辑可闭合；本报告仅核故事文字，不将 s2 以后的视频节拍、外语发音或口型判为已审。

## 材料与看图记录

审查单根目录：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2`。完整读取任务书、BRIEF、index、lines、五份 spec、previous 的本类别全部九条与 changes；核对故事稿、bible、Riley 卡及相关场景卡、考据段落。五份现行 prompt 与本轮 `materials/snapshot/prompts/s1_st*.txt` 的 SHA-256 均一致，五张首帧与 `materials/snapshot/first_frames.json` 记录均一致。

逐张查看了以下 20 张不同图片，无镜组板或另列的拼图可漏看：

| 图片集合 | 已看内容与本类别观察 |
|---|---|
| `episodes/ep01/scenes/s1/shots/st{1,2,4,3,5}/planning/` | 每镜的 `stN_first_frame.png`、`stN_overhead.png`、`stN_overhead_ref.png`，共 15 张；st1 首帧中央背影、st2 中央闭嘴自拍、st4 画右 Riley 侧看渔夫、st3 画左背影与右侧工人、st5 门口远处 Riley，均能按节拍转入讲话或保持安静。两版 overhead 的对白窗与 spec 一致。 |
| `2_世界观人设/characters/c1_Riley/views/c1_Riley_views.png` | 一张三视图，正面、侧面、背面同一主持人；作为身份参照，不从图中推断她实际声音。 |
| `2_世界观人设/props/p2_钱币/p2_钱币.png` | 三种钱币形制参照，配合 st2 明确枚数为 7＋1＋1；图中三枚不被误作预算只有三枚。 |
| `2_世界观人设/background/pompeii_75/` | `bg1_海门外陡坡/bg1_海门外陡坡.png`、其下 `bg1-2_海门门洞/bg1-2_海门门洞.png`、`bg2_石板街/bg2-2_海门内回望/bg2-2_海门内回望.png`，共三张；海边、修补裂缝、门内街景支持对应台词或无词环境段。 |

以上图片路径均相对 `C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\`。本轮没有给出与当前新输入对应的视频、ASR 区间或音轨，未对旧条另抽帧、未运行 faster-whisper，不报告“实听逐字正确”。

## 整体观察

当前台词围绕穿越、进城观察、看鱼和看修补痕迹展开，支持“像亲自去过那里”的 Vision，没有把场一变成脱离眼前所见的讲课。
上轮 st3 的时长问题已实质缓解；st2 首段可以在上限内完成，但停顿预算仍紧，属于便宜可改的记录项。
I35 的登记状态落后于文本事实，不需要因为声音行未逐字重复同一禁令就再次认定说话人失控。
本轮没有已证实必须重出视频的问题；低声对白、具体口型和字尾可懂度留待新条检查。
未运行 tick；只写本报告，由调用方按审稿流程登记。
