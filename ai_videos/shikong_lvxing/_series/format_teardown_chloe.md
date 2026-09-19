# 系列级格式拆解 · Chloe VS History

> **这是系列共用文档，不属于任何一站**（`_series/` ＝ 跨站材料）。sk3 开站时（2026-09-18）产出，后续各站沿用与追加。
> 全部数字为 **2026-09-18 yt-dlp 实测快照**，可复现：
> `yt-dlp --flat-playlist -J "https://www.youtube.com/channel/UCZB1r1In9RfE7tpVrYgcjLQ/videos"`
> 字幕与元数据：`yt-dlp --skip-download --write-auto-subs --sub-langs "en.*" --write-info-json <watch_url>`
> 与 `proposal.md` §F（2026-09-13 第一轮调研）的关系：F 章证明了「格式可行」，本文回答 **「同一个人、同一套工具、同一个格式，为什么有的条目是别的条目的三倍」**。

---

## 1. 实测：频道全 7 条长片

| 上线 | 标题 | 播放 | 赞 | 赞率 | 评论 | 时长 | 日均播放 |
|---|---|---|---|---|---|---|---|
| 2026-04-14 | **I time travelled to the Titanic 1912!** | **2,778,109** | 107,306 | 3.86% | 9,700 | 853 s | **17,695** |
| 2026-05-15 | **I time travelled to Tudor London in 1536!** | **2,541,367** | 100,776 | 3.96% | 5,700 | 746 s | **20,169** |
| 2026-03-23 | I time travelled to Ancient Rome! | 1,483,945 | 63,224 | 4.26% | 5,500 | 563 s | 8,290 |
| 2026-08-07 | I time travelled to Edo Japan in 1657! | 361,212 | 14,367 | 3.98% | 1,400 | 832 s | 8,600 |
| 2026-06-15 | I time travelled to Ancient Egypt in 2400BC! | 594,355 | 29,305 | 4.93% | 3,000 | 822 s | 6,257 |
| 2026-07-09 | I time travelled to D-Day in 1944 (WW2) | 393,089 | 16,807 | 4.28% | 2,200 | 899 s | 5,536 |
| 2026-06-02 | Can I Survive 24 Hours in the Ice Age? (30,000BC) | 490,349 | 24,271 | 4.95% | 1,800 | 740 s | 4,540 |

**读法**：YouTube 播放前置分布，日均值会**高估新片、低估老片**——所以这个排序只会**低估** Titanic / Tudor 的领先幅度。最新的 Edo（42 天）日均 8,600，仍不到 Titanic 的一半。

**赞率反向是关键读数**：Ice Age 4.95% 最高但播放最低，Titanic 3.86% 最低但播放最高。**赞率高＝只在核心受众里转；Titanic 是破圈了**，被大量非历史受众看到。所以 `proposal.md` 读数 9 的「赞率 ≥ 3% 是健康线」要补一句：**赞率是「有没有被当 slop」的温度计，不是「跑得好不好」的指标**——冲破圈时它必然下降。

---

## 2. 领先的两条 vs 落后的五条：差别是结构，不是题材

Titanic 与 Tudor London 共有、其余五条都没有的四件东西：

| # | 装置 | Titanic 的实例（时码） |
|---|---|---|
| **S1** | **已知结局的倒计时** | 观众进场就知道船会沉，于是每次报时都是悬念。`08:15`「Tomorrow is April 14th, **the day of the sinking**.」→ `11:25`「It is 11:38 p.m. **2 minutes**.」 |
| **S2** | **一个注定失败的个人任务** | `00:39` 立下：「I also want to try to talk to the captain about the iceberg. I feel like **someone should at least try to say something**.」→ `10:47` 执行 → `11:01` 失败：「Of course he didn't listen. I don't blame him… **but I tried**.」 |
| **S3** | **一道阶级边界 + 一次越界** | 三等舱票 → Liam 给情报（E 甲板的门、乘务员每晚离开 20–30 分钟）→ 换装 → 潜入 → 大楼梯。它供给了全片**最强的视觉对比**：rice soup ↔ 11 道菜、刷漆木板 ↔ 真木、太短的铺位 ↔ 大楼梯 |
| **S4** | **具名 NPC + 真对话** | 6 段：爱尔兰情侣、Liam、船长 Smith、头等舱乘客（冷淡拒答）、乘务员。`02:43`「到了纽约你打算做什么？」→「我叔叔在码头给我找好了活。我们要结婚，找个自己的地方。」 |

**Tudor London 的同构**：已知结局＝安妮·博林命不久矣；任务＝设法见到安妮；边界＝客栈 → 汉普顿宫；NPC＝亨利八世与宫中人。

**Ancient Rome（1.48 M，同一个人、同一套工具）四件全无**——它是纯逛城。**这就是 1.48 M 与 2.78 M 之间的全部差别。**

### 2b. 第五件：情绪曲线前后分家
Titanic 前 2/3 是高密度信息 + 笑点（rice soup 就是米加热水、床太短、poop deck、领带上的肉汁「a gravy situation I'm not willing to explain」）；**后 1/3 笑点清零**（`09:29`「I did not want this day to come.」、救生艇坐 65 人只上了 28、`12:58`「Nobody is pretending now.」）。
→ 与本系列 I-9 密度合同的「最后 60–90 秒慢下来、零笑点」同向，但 Titanic 把这一段**从 90 秒拉到了 4 分钟**。

---

## 3. 为什么没被骂 AI slop（比结构更要紧的一层）

### 3a. 第 16 秒的「工艺声明卡」
`00:16–00:28`，紧跟开场钩子：
> "In this episode, I used **real historical illustrations and photographs of the Titanic in the public domain** to turn them into photorealistic worlds. Everything you see is **as close as we can get to the real thing**. Enjoy, guys. **This was a lot of work.**"

一句话同时交代**方法**、**出处**、**劳动**。

### 3b. 创作者自述：信任来自史料，不是来自提示词
Jonathan Laramie（Chloe VS History / Majestic Studios），一手访谈 *The Maker of 'Chloe vs History'*（YouTube `dNejbCnqfq4`，2026-03-25）：
> "It's all a matter of trust. **You're not asking AI to imagine something from a text prompt and just trusting what it spits out. The trust comes from the historical sources.**"
> "It was only until **the end of 2025** where we got this new tool, and you could upload the image and say 'make this a photorealistic version', and it would actually **keep the integrity of the image intact**." （在那之前上传参考图只被当作风格参考，出来的是另一张图）
> "It doesn't really take much longer to add a reference, and actually **I really enjoy doing the research**."
> "You've got to edit it **like you are a documentary maker**. And that's what takes all the time."

### 3c. 效果：最高赞评论全在夸「查过」与「费了功夫」
| 赞 | 评论 |
|---|---|
| 12,000 | "This is one of the only videos that used AI **purely for education**, not for brainrot, not for trickery." |
| 8,800 | "Closest to time traveling we got so far." |
| 6,300 | "Difference between **AI slop and AI gem: tons of work and passion**." |
| 2,900 | "Do you guys understand how much prompting, waiting, reprompting… someone spent a lotta time on it" |
| 802 | **"As a historian, I see, of course, many inaccuracies, but this is not important. The video turned out to be very lively and interesting."** |

→ **门槛是「看得出你查过」，不是「零错误」。** 历史学家在评论区明确豁免了准确性瑕疵，因为片子证明了自己在乎。这条直接支持本系列 I-10 三重标注与片尾考证卡的做法，也说明**不必为了消灭每一处 ⚠️ 而砍掉戏**。

### 3d. 实物史料当道具、数字当锚
`03:26`「All right, so **I have the actual menu for today**.」（三等舱真菜单：rice soup / roast beef / plum pudding）
数字锚：三等舱票 ≈ 今天 500 美元、11 道菜、救生艇额定 65 人只坐了 28、2,224 人上船、1,517 人遇难。

### 3e. 置顶评论做情绪与劳动的披露（7,400 赞）
创作者自己发的长评：「这是我做过最难的一条，不只是技术上，是情感上。泰坦尼克是 1,517 个各自独立的故事在同一夜结束在同一个地方。」

---

## 4. 观众参与层：彩蛋是可量化的资产

大楼梯上走过 **Rose 和 Jack**（2 秒背景）。带时间码讨论它的高赞评论至少 5 条：804 / 401 / 328 / 86 / 73 赞。
→ 一个两秒的背景彩蛋买来了大量**回看、二刷、带时码评论**。**本系列每站应当埋 1–2 个同类彩蛋**（本站候选：皮普斯在后院埋帕玛森奶酪与酒）。

连**瑕疵也在被消费**：「8:02 那个倒着走路的女人笑死我了」（172 赞）、「2:45 那姑娘的脖子穿过栏杆了」（77 赞）。不完美提供了社交货币——**不要为了零瑕疵牺牲产量**。

---

## 5. 制作流程（可直接抄的部分）

1. **素材源**：公版历史插画 / 照片 → **image-to-image 转照片级，保持原图完整性**（不是风格参考）。
2. **人物一致性**：多视图 character sheet；**每换一套衣服就重做一张「人已经穿着该服装」的 sheet**——不要用「人物 sheet ＋ 服装图」两张参考图喂进去。
3. **场景一致性**：每个地点一张 location sheet，全片复用。
4. **视频**：Seedance 2.0，带图参考 + 原生音频，16:9 1080p。
5. **声音**：统一 voice clone 盖掉模型的随机音色（每条 clip 的原生音色都不一样）。
6. **剪辑**：按纪录片的方式剪——创作者原话说这才是耗时大头。
7. **成本量级**：单片数周、10–15 次返工（`proposal.md` F §1 读数 12 转述）。

> **与本仓库现行工艺的关系**：第 1 条与 `ai_video.md` rule 4d ①「锚点图纯文字自由生成、零参考图」相抵。2026-09-18 用户拍板**两条并用、各管一层**——公版史图 image-to-image 出**长相**，Blender 整城白模只出**几何与运动**（航拍长镜 / 一镜到底的机位路径与 previz）。rule 4d ① 真正要防的是**拿白模 / 灰模渲图当出图参考**（会把质量上限锁死在方盒子水平），**那一条照旧严禁**——历史原图与白模渲图是两回事。详见 `specs/ai_video/sk3/divergence.md` D3。

---

## 6. 对本系列不变量的结论（已落 `proposal.md` A §2 的 2026-09-18 修订）

2026-09-14 那次形态改写，恰好把 S1–S4 四件**全删了**（I-3 取消任务与结局、I-5 ① 禁示警、I-7 当地人零台词、I-15 不写越界）。而 `proposal.md` F §1 **读数 8 早已记录过其中一条**——「Titanic 版加了 6 段短对话就成为频道第一」——结论在库里，形态却按相反方向改了。

自 sk3 起按**站型**分叉：**游览型**（sk1 维持原样）/ **Titanic 型**（sk3 起）。分型表见 `proposal.md` A §2。

**I-7 的理由没有被推翻**：「古代方言与说法无法确定，一开口就等于编造」在古代站上依然成立。分级开放只是承认**它在 1666 年的伦敦不成立**——说英语，且皮普斯日记把当天的话逐字记了下来。判据从「一刀切禁止」变成**「这一站的语言有没有逐字史料、现代观众听不听得懂」**。

---

## 7. 下一站选站时要问的四个问题（本文的可操作产出）

选站不再只问「史料厚不厚、观众熟不熟」，先过这四问；**四问全中才配走 Titanic 型**：

1. **观众进场前就知道结局吗？**（没有 → 只能做游览型）
2. **有没有一个旅行者可以尝试、且**注定失败**的具体动作？失败**本身**有没有史料记载？**（有记载的失败 > 编造的失败）
3. **城里有没有一道她能越过的硬边界？**（阶级 / 城门 / 宫墙 / 舱位——它同时供给悬念与视觉对比）
4. **这一站的语言有没有逐字史料、现代观众能不能听懂？**（决定 NPC 能不能开口 ＝ 决定能不能有 S4）

> 伦敦 1666 四问全中，第 2 问是**最强的一种**——失败本身有 T0 记载：《伦敦公报》官方通告认定「本该拆房断火而未办」，皮普斯亲耳记下市长崩溃的原话。
> **但这里有一个教训，写给以后选站的人**：最初支撑第 2 问的是那句流传最广的「a woman might piss it out」，阶段 0 一查——**查无一手出处**，最早只到 1807 年的汇编。结论没变，依据换了。
> **所以第 2 问要问的是「失败有没有记载」，不是「有没有一句名言」。名言的传播度和它的史料强度经常反着来**——越是人人会背的句子，越可能是后人追加的。选站时先去查那句话的脚注。庞贝、维苏威、君士坦丁堡 1453 中前三问、第 4 问不中（拉丁语 / 希腊语无法确定当时说法）→ 可做 Titanic 型但 NPC 维持零台词。
