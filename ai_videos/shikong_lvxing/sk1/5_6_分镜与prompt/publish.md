# 四站发布页 ·《时空旅行》汴京清明一日（sk1）

> **这一页 ＝ 本站的四站发布页**（`ai_video.md` rule 16）。固定七节；三至六节各自自包含，只看一节就能把一个站传完。
> 所有 ```text 围栏里**只有要粘贴的正文**；说明一律写在围栏外。
> **YouTube 与 TikTok 英文，抖音与小红书中文，四份文案各自创作、不是互译。**
> 上游：`../1_立项/concept.md`（游览形态）· `../3_大纲/outline.md`（36 镜、段落时长）· `shotlist.md`（逐镜时长，章节按它算）· `../../proposal.md` §E（合规）/ §F.3（标题与封面公式）/ §F.12（音轨、评论、测验）。
> 文案里每一个数字都来自事实注册表 `../0_research/parts/`（✅ 条目，W7–W11 已合并），并在 2026-09-14 与定稿镜头的中英台词逐条对过（SYNC_sk1）；片中口播说是推测的，文案里不写成定论。

---

## 1. 母版与通用设置

| 项 | 值 |
|---|---|
| 节目定性 | **AI 历史情景科普节目 · 游览 vlog**，不是微短剧；片名一律「第 N 站」，**不用「剧 / 集 / 连载」，不用「新闻 / 报道 / 记者」**（proposal §E.1 R1 / R4） |
| 系列 | 中《时空旅行》/ 英 *Posted to the Past*；本站是第 1 站，站与站独立（不预告下一站、不回指上一站） |
| 本站片名 | 中「汴京清明一日」/ 英 *One Day in Kaifeng, 1120* |
| 画幅 | **16:9 横屏，一条母版**；不出竖版母版（`specs/ai_video/sk1/divergence.md` #1）。TikTok 竖版切条是「建议」，出片后再定做不做 |
| 片长 | **≈ 14:58（898 s，36 镜，含可选 S36）**；S36 不入片则 **≈ 14:34（874 s）** |
| 声音 | **全片只有旅行者林问一个人说话**（对镜 + 画外）；当地人零台词，人群只有听不清字句的环境声 |
| 两条解说轨 | 中文 `zh-f-reporter-linwen-01` / 英文 `en-f-reporter-linwen-01`（`../2_世界观人设/casting.md`），**同一画面、同一环境音与 BGM** |
| 成片文件 | 英文版 `sk1_en.mp4` · 中文版 `sk1_zh.mp4` · 中文解说混音轨 `sk1_zh_audio.wav`（给 YouTube 附加音轨用，与母版逐帧等长） |
| 字幕 | **母版零字幕**，画面不烧任何文字；各站字幕由用户后期自行添加 |
| 发布频道 | YouTube 用已入 YPP 的《荒野生活》老频道（proposal §0 决定 9） |

**判断**：成片文件名是本页定的，出片时按实际文件名替换。（理由：生成器还没定 mux 输出名，发布页先给一个能对账的名字。）

### 三重标注（proposal §E.3，四站发布前逐项勾）

| # | 标注 | 落在哪 |
|---|---|---|
| ① | **AI 生成标识** | 四站后台的 AI 声明开关全开（每节「其余设置」表里写了开关位置）；mux 不得剥离元数据（R2 / R12） |
| ② | **情景再现 · 演绎声明** | 片头字卡（下）+ 四站简介里的声明段 |
| ③ | **史料出处** | 片尾考证卡（下）+ YouTube 简介 3 条公开史料链接 |

**片头字卡（后期叠在航拍 S01 上，0:40 之前出现，约 4 s）**——中文版 / 英文版各一：

```text
AI 复原的历史情景 · 旅行者和她的解说是演绎的 · 当地人不说话 · 片里的数字都有出处
```

```text
AI-reconstructed historical scenes · The traveller and her narration are performed · The locals never speak · Every number has a source
```

**判断**：proposal §E.3 ② 的固定句是「人物对白为基于史料的虚构演绎」，本站改成「旅行者和她的解说是演绎的 · 当地人不说话」。（理由：本站没有对白，只有一个人的解说；照抄「对白」会让观众以为有古人开口。）

**片尾考证卡（后期叠在 S35 航拍收束上，14:14–14:34 之内，5–8 s）**——`{N}` `{M}` 发布当天用 `python tools/facts_registry.py ai_videos/shikong_lvxing/sk1` 填：

```text
本站考证：《东京梦华录》· 张择端《清明上河图》· 《宋史》卷一百七十五 · 程民生《宋代物价研究》
本站 {N} 条事实 · {M} 条存疑
```

```text
Sources: Dongjing Meng Hua Lu (Meng Yuanlao) · Along the River During the Qingming Festival (Zhang Zeduan) · History of Song, ch. 175 · Cheng Minsheng, Prices in the Song Dynasty
This stop: {N} facts · {M} still uncertain
```

**判断**：`{N}` ＝ 工具输出的 `facts:` 总数，`{M}` ＝ `by tag` 里 ⚠️ 的条数。2026-09-14 快照是 **538 / 111**（w1–w11 合并后；发布前还可能变，所以不写死）。（理由：❌ 误传条目每条都带正解，也算查过的事实；「存疑」严格对应 ⚠️ 这一级。）

---

## 2. 封面帧

**首选（四站通用）：S04 · 虹桥「桥中回望」**——一镜到底走到桥中、林问扶着木栏回头的那一下。

| 项 | 值 |
|---|---|
| 取自 | `S04` 第 16–20 秒（桥中扶栏回望那一段；在这 4 秒里挑侧脸最清楚的一帧），成片 `01:44–01:48`，**最佳约 `01:46`** |
| 画面 | 虹桥桥面中段：林问（现代装：深灰工装夹克、黑齐肩低马尾）扶着朱红木栏回头看河面，机位在她侧前方约四十五度，**四分之三侧脸入画**；身后是河面和刚从桥洞里出来的船，桥面的席棚、大伞从画面边上带到 |
| 备选（A/B 测） | ① `S02` 第 29 秒（成片 `00:59`）：停在宣德楼正前方仰视的那一帧（纯城市、没有人）② `S26` 桅杆砸平、桥洞阴影扫过桅根（约第 24 秒，成片 `10:52` 前后；有事件、没有脸） |
| 不选 | `S29` 全场一起笑（有脸有情绪，但勾栏认不出「汴京 / 清明」） |

**判断**：选 S04。（理由：① 四个 hero beat 里只有它**同时**有旅行者和《清明上河图》里最认得出的地标——虹桥，中文观众一眼对上「清明上河图」；② 符合 §F.3 穿越 vlog 封面公式：人在左中、身后是古代人群、右侧 2–3 个超大字；③ 这时她还穿着现代夹克，**现代衣服站在宋代人群里，不用一个字就说清了「穿越」**；④ S26 的人太远、桅杆特写缩成缩略图就看不清，留作 A/B 备选；⑤ S02 宣德楼仰视是纯城市公式、弱于有人的 vlog 公式，但它是全片最干净的城市帧，2026-09-14 按定稿镜头从「不选」改为 A/B 备选。）

**判断**：若 S04 出片后回头那一下拿不到清楚的脸，封面改用 S02 或 S26（A/B 测），不从这三帧以外另找。（理由：守定稿的三个封面候选。）

### 封面字（后期加，画面本身零文字）

| 版本 | 大字 | 小字 |
|---|---|---|
| 英文（YouTube / TikTok） | `1120` | `KAIFENG` |
| 中文（抖音 / 小红书） | `1120 · 汴京` | `清明这一天` |

- **大字只写年份和地点**（§F.3：不写「AI」字样；年份必须写对——1120，不加 BC / AD）。
- 中文小字「清明这一天」；英文不加小字（英文观众不认得 Qingming，多一个词只会挤小大字）。

### 安全布局

- **16:9（1920×1080）**：人脸落在**左侧三分线**附近、画高上半；大字放**右上到右中**，占右侧约 40% 宽；四边各留 5% 安全边；**右下角不放字**（YouTube 时长角标盖在那里）。
- **9:16 竖裁（抖音 / TikTok 竖封面）**：从 1080 高里裁 608 宽，**只剩原画 32% 的宽度**。裁框中心压在她的脸上（裁框左边约在原画宽度 12% 处，按实际帧里脸的位置微调），身后的河面与船只留窄窄一条；大字挪到**顶部 20%**，底部 25% 与右侧 15% 不放字（两站的文案栏与按钮盖在那里）。
- **3:4 竖裁（小红书 / 抖音竖封面）**：裁 810 宽，保留原画 42% 的宽度；脸在上三分之一，身后留一段河面和船；大字放顶部。

---

## 3. YouTube · English

**字段上限**：标题 ≤100 字符 ｜ 说明 ≤5000 字符 ｜ 标签总长 ≤500 字符 ｜ 章节 ≥3 条、首条 `00:00`、每条 ≥10 s

**判断**：英文站片名定为 *One Day in Kaifeng, 1120*，系列名 *Posted to the Past* 放标题末尾当标签。（理由：用「城市 + 年份」公式 §F.3 ③，而不抄 Chloe 的「I time travelled to…」——逐字抄她标题的号没有一个破 2 万，§F.1 读数 2 / K03；Kaifeng 是英文观众查得到、地图上找得到的名字，Bianjing 没人搜；标题不写「AI」，§F.3。）

### 标题（首选）

```text
One Day in Kaifeng, 1120: Street Food, a Night at an Inn & the Qingming Crowds | Posted to the Past
```

### 备选标题

```text
One Day in Kaifeng, 1120 — The City Where Silver Couldn't Buy Breakfast | Posted to the Past
```

```text
One Day in Kaifeng, 1120: What Ordinary People Actually Did All Day | Posted to the Past
```

### 说明

```text
This isn't a history lesson. The traveller is made up. The facts aren't. The pictures are AI reconstructions.

Kaifeng, the capital of Song China, on the Qingming holiday of 1120, over 900 years ago. I walked in over the Rainbow Bridge with one string of copper coins and tried to spend a whole day, and a night, the way people here did.

What I did:
- Crossed the Rainbow Bridge. There isn't a single pillar under it; the whole arch is timber, painted red.
- Checked into an inn in the morning and changed into Song clothes. Yes, they already sat on chairs.
- Tried to pay for breakfast with silver. Wrong city. Here you pay in copper, and "100 coins" on the street means you count out 75.
- Watched porters haul grain sacks at the docks, and rented a donkey for the long walk (the book says a mount costs under 100 coins).
- Walked the imperial avenue: over 200 paces wide, with a lane down the middle that no person or horse may enter.
- Walked through Xuande Gate into the palace courtyard, touching nothing. Looked into a doctor's shop you can find in the Qingming scroll, the Kaifeng Prefecture office and the book stalls at Xiangguo Temple, and watched scholars whisk tea by a garden pond.
- Went out of the city with everyone else for Qingming, then walked back along the river just as a boat came at the Rainbow Bridge with its mast still up.
- Laughed along in a packed theatre tent in the entertainment quarter.
- Ate night-market buns at 15 coins each at most, and booked a jug of wine at a grand wine house at 72.
- Slept at the inn and woke at the fifth watch to someone beating an iron plate down the street.

00:00 Flying in over Kaifeng
01:00 One string of copper coins
01:28 The Rainbow Bridge, in one take
02:20 East Water Gate
02:46 Checking into an inn
03:12 Outfit change
03:40 Morning market and the silver mistake
04:46 Porters at the granary wharf
05:10 Trades by their clothes, and a rented donkey
05:32 A doctor's shop from the scroll
06:24 Zhou Bridge
06:46 The imperial avenue
07:12 Xuande Tower, and through the gate
08:06 Kaifeng Prefecture and the coin-toss stalls
08:56 Books at Xiangguo Temple
09:20 Tea by a garden pond
09:44 Qingming: the whole city heads out
10:28 The mast that didn't come down
11:14 The entertainment quarter
12:04 Zhou Bridge night market
12:28 A grand wine house
12:54 The day's bill
13:22 Back at the inn
13:50 The fifth watch
14:14 Dawn over the city
14:34 Kaifeng today (optional)

How this was made
Human-researched, sources listed. The streets, people and events are AI reconstructions based on historical sources. The traveller is fictional and her narration is performed with an AI voice. The locals never speak: nobody knows what Kaifeng street talk sounded like in 1120, so we don't make it up. Facts carry their source on screen, and anything historians still argue about is said out loud as a guess.

This stop: {N} facts · {M} still uncertain.

Read the sources yourself:
The Dreams of the Eastern Capital (Dongjing Meng Hua Lu), Meng Yuanlao's record of Kaifeng, full text: https://ctext.org/wiki.pl?if=en&res=712358
Along the River During the Qingming Festival, Palace Museum digital paintings: https://minghuaji.dpm.org.cn/
History of Song, chapter 175, on the grain barges (Chinese): https://zh.wikisource.org/wiki/%E5%AE%8B%E5%8F%B2/%E5%8D%B7175

Also available with Chinese narration: Settings, then Audio track.
```

- **章节时间按 `shotlist.md` 逐镜时长算（2026-09-14 定稿，26 条），成片剪完后必须按实际时间重排**（rule 16.7）。S36 不入片：只删最后一行 `14:34 Kaifeng today (optional)`，其余不动。
- `{N}` `{M}` 发布当天用 `python tools/facts_registry.py ai_videos/shikong_lvxing/sk1` 填（定义见第 1 节）。

**判断**：说明第一句用 proposal §A.1 的定位句改写成英文三短句。（理由：定位句是四站固定第一句；§F.3 实测「This is not a history lesson」这类开头能降低观众对准确性的抵触。）

**判断**：说明里的英文文案不写旅行者的名字。（理由：proposal A 章正在重写，英文名还可能变；「the traveller」不会过时。）

### 标签

```text
kaifeng, song dynasty, northern song, one day in kaifeng, qingming festival, qingming scroll, along the river during the qingming festival, ancient china, chinese history, time travel vlog, history vlog, ancient city tour, daily life in ancient china, street food history, rainbow bridge, bianjing, 1120, posted to the past
```

### 其余设置

| 字段 | 值 |
|---|---|
| 类别 | **Education（教育）** |
| 视频语言 | English |
| 字幕认证 | 不适用 |
| 是否为儿童打造 | **否** — No, it's not made for kids |
| 修改后的内容（Altered or synthetic content） | **是（Yes）** |
| 付费推广 | 否 |
| 播放列表 | `Posted to the Past` |
| 许可 | 标准 YouTube 许可（Standard YouTube License） |
| 允许嵌入 | 是 |
| 评论 | 开，「保留可能不当的评论待审核」 |
| 封面 | `S04` 桥中回望 + 英文封面字 `1120` / `KAIFENG`（第 2 节）；若频道有 Test & compare，同时上传 `S02` 与 `S26` 两张做 A/B |
| 画幅 / 时长 | 16:9 · ≈ 14:58（S36 不入片 ≈ 14:34） |

**判断**：类别选 Education，不沿用《荒野生活》的 Film & Animation。（理由：本系列定性是科普节目；同格式的 Chloe VS History 就归 Education，§F.12 读数 F7-1。）

**修改后的内容选「是」的理由**：片中 1120 年汴京的街景、人群和事件是生成出来的，看上去像真实拍摄，但从未发生在镜头前；旅行者的声音是合成的。YouTube 要求这类「逼真但不是实拍的场景」必须披露。

### 字幕（用户后期加）

- 母版零字幕。英文字幕由英文解说稿导出 SRT，挂在 English 下；中文 SRT 挂在「中文」语言行下（下一小节）。
- 专名拼写统一：以 `_series/glossary.md` §2.3 英文解说专名表为准（如 `Kaifeng` `Rainbow Bridge` `East Water Gate` `Zhou Bridge` `the imperial avenue` `Xuande Tower / Xuande Gate` `Kaifeng Prefecture` `The Dreams of the Eastern Capital` `wen`）。**不要直接用自动字幕**——它会把这些名字听错。

### 附加中文音轨 + 中文标题与说明

YouTube 自动配音**只能把中文配成英文，没法把英文配成中文**（§F.12 读数 F7-4），所以中文解说要自己作为附加音轨上传。

1. 出中文混音轨 `sk1_zh_audio.wav`：中文解说（`zh-f-reporter-linwen-01`）+ 与英文母版**同一套环境音和 BGM**；从 `00:00` 起与母版逐帧等长，片头片尾都不能多一帧或少一帧。
2. YouTube Studio → 内容 → 本片 → 左栏「语言（Languages）」→「添加语言」→ 选中文（Studio 列表里对应普通话 / 简体中文的那一项）。
3. 在「中文」这一行的「音频（Audio）」列点「添加」→ 上传 `sk1_zh_audio.wav` → 发布。
4. 同一行的「标题和说明（Title & description）」→ 粘贴下面两块。
5. 同一行的「字幕（Subtitles）」→ 上传中文 SRT（用户后期出）。

- 若「音频」列不出现，说明频道还没开放多语言音轨：**不要把中文版当另一条视频传到同一频道**（会把播放量拆成两份），先只挂中文标题、说明和字幕。

**中文标题**

```text
时空旅行｜汴京清明一日：揣一贯铜钱，在 1120 年的汴京过一天、住一晚
```

**中文说明**

```text
这不是历史课。旅行者是虚构的，事是查过的，画面是 AI 复原的。

宣和二年（1120）清明，北宋都城汴京（今河南开封）。我揣着一贯铜钱，从城外虹桥走进城，早上在客店放下东西，逛了一整天，夜里回客店睡。

00:00 航拍：清晨飞进汴京
01:00 一贯铜钱，今天的逛单
01:28 虹桥一镜到底
02:20 进东水门
02:46 住客店，照守则查房
03:12 换宋装
03:40 早市：拿银子付账翻车
04:46 仓前码头的袋家
05:10 看行头 · 租头驴
05:32 赵太丞家医馆
06:24 州桥
06:46 御街
07:12 宣德楼，进宣德门
08:06 开封府 · 门外关扑
08:56 相国寺书铺书画摊
09:20 园池边读书人点茶
09:44 清明：全城出郊
10:28 虹桥险情：桅杆没放下
11:14 瓦子勾栏，满棚一起笑
12:04 州桥夜市
12:28 正店
12:54 今日总账
13:22 回客店过夜
13:50 五更报晓
14:14 天亮，航拍收束
14:34 今天的州桥遗址（可选）

【怎么做的】
画面是依据史料做的 AI 情景复原；旅行者是虚构人物，解说是 AI 配音演绎；当地人全程不说话——没人知道 1120 年汴京街上的人怎么说话，我们就不替他们编。片里的数字都带出处，学界还在争的，片中当场说明是推测。

本站 {N} 条事实 · {M} 条存疑

【出处】
《东京梦华录》全文：https://ctext.org/wiki.pl?if=gb&res=712358
《清明上河图》故宫名画记：https://minghuaji.dpm.org.cn/
《宋史》卷一百七十五 食货上三（漕运）：https://zh.wikisource.org/wiki/%E5%AE%8B%E5%8F%B2/%E5%8D%B7175
```

**判断**：YouTube 这一节出现中文，只限「中文」语言行的标题、说明和音轨。（理由：rule 16.2 管的是英文主标题 / 说明 / 标签不许夹中文；Studio 的「语言」行是另一个输入框，只给中文界面的观众看，而且翻译后的标题和说明会进搜索——§F.12 读数 F7-3、建议 7。）

### 自动配音

| 设置 | 值 |
|---|---|
| Studio → 设置 → 上传默认设置 → 高级设置 →「允许自动配音」 | **开** |
| 「发布前手动审核配音」（Studio 提供时） | **开** |
| 审核时抽听 | `Kaifeng` `Bianjing` `Xuande` `Xiangguo` 这几个专名；读错的语言，那一种配音不发布 |

**判断**：开自动配音。（理由：英文源可以自动配成十几种语言，只是没有中文；全片只有一个解说声源，最适合整轨配音——§F.12 读数 F7-3 / F7-4。中文轨由第 4 步手动上传补上。）

### 置顶评论

```text
One question, just about this day: If you had one string of copper coins and one day in Kaifeng in 1120, what would you spend your first coin on?

Spotted a mistake? Reply here with a source and we'll add the correction to this comment.
```

- **全片只留这一个评论问题**：S34（成片约 13:58–14:07）口播的问题，英文置顶与 S34 的英文配音句一字不差，中文两站置顶与 S34 中文台词一字不差。
- **不问「下一站去哪」**（§F.12 读数 F7-6；站与站独立，proposal §0 决定 11）。
- 本站的更正只补进这条置顶评论，不开「上一站纠错」。

### 社区帖 · 猜价格测验（上线前 1–3 天发）

YouTube 社区帖选「测验（Quiz）」：≤4 个答案、唯一正确答案、可附解释。片中 S30 的「猜价格」暂停卡问的是同一题，正片就是揭晓。

**题目**

```text
Kaifeng, 1120. At the night market by Zhou Bridge, what did one stuffed bun cost?
```

**选项 1**

```text
1 copper coin
```

**选项 2（正确答案）**

```text
No more than 15 copper coins
```

**选项 3**

```text
About 100 copper coins
```

**选项 4**

```text
A small piece of silver
```

**解释**

```text
The Dreams of the Eastern Capital (Dongjing Meng Hua Lu), the old record of Kaifeng's streets, lists the night-market buns by Zhou Bridge (goose, duck, chicken, rabbit, tripe, eel) at no more than 15 coins each. An ordinary worker made about 100 coins a day, by one modern historian's estimate. And silver? Nobody bought dinner with silver.
```

- 上线后在这条帖子下回复一次正片链接。

**判断**：测验题选夜市包子价（`price.001`），不选斗米价。（理由：包子价是《东京梦华录》原文直接记下的 ✅；斗米 250 文是按前后几年推算出来的，dossier §14 #5 标 ⚠️，不能当测验的「正确答案」。）

### 片尾画面与卡片

- **片尾画面**：放在最后 12 秒——S36 入片时约 `14:46` 起（遗址镜末段），S36 不入片时约 `14:22` 起（S35 航拍收束末段）。只放「订阅」+「最适合观看者的视频」两个元素，**放在左上和右上两角**；画面**下方中间三分之一留空**（考证卡叠在 S35 上，S36 不入片时两者同屏）。
- **不放下一站 / 系列播放列表元素**，片中不加信息卡。

**判断**：片尾画面不推系列播放列表。（理由：站与站独立、不做下站预告，proposal §0 决定 11；片尾画面也算预告。）

---

## 4. TikTok · English

**字段上限**：caption ≤2200 字符（含 hashtag）｜ 建议 3–5 个 hashtag
**画幅**：**完整片横屏直投**（16:9，上下黑边，接受）。下面 4 条竖版切条和 1 条精华是**建议**：`divergence.md` #1 定了「竖屏切条出片后再定」，所以这里只给剪法，不承诺一定做。

### 完整片 · Caption

```text
One string of copper coins. One day in Kaifeng, 1120, capital of Song China, on Qingming, when the whole city walks out to the family graves.

A breakfast I tried to pay for with silver. The Rainbow Bridge. A palace gate. A packed theatre. Night-market buns, 15 coins tops. A bed at an inn.

The traveller is made up. The locals never speak. The facts come with sources. Sounds made up. It isn't.

#history #songdynasty #ancientchina #kaifeng #timetravel
```

### 完整片 · 其余设置

| 字段 | 值 |
|---|---|
| 上传方式 | 长视频上传（≈ 15 分钟；手机端传不了时走电脑端或创作者中心） |
| 封面 | `S04` 桥中回望 + 英文封面字（第 2 节） |
| **AI 生成内容标签** | **开**（More options → AI-generated content） |
| 声音 | 英文版原声 `sk1_en.mp4`，不叠平台音乐 |
| 字幕 | 用户后期上传英文字幕；不直接用自动字幕（专名会听错） |
| 允许 | 评论 / Duet / Stitch 全开 |
| 地区 | 英语区为主 |

### 竖版切条（建议 · 每条 < 60 s）

**裁法通用规则**：16:9 → 9:16 只保留原画 32% 的宽度。近景和特写段直接竖裁、裁框跟住林问的脸或手；**全景和远景段不裁**，改成「16:9 居中 + 上下两块模糊铺底」，否则人群和桥会被切光。开头 2 秒的钩子字由用户后期加。

**① 拿银子付早饭钱 ·** `S09`（26 s）+ `S10`（20 s）＝ **46 s**
- 裁法：S09 开头的早市全景用居中 + 模糊铺底；摊主摇头指钱串之后竖裁跟脸；数钱特写和 S10 食物特写直接竖裁。
- 钩子字：`Paying in silver, 1120`

```text
Tried to pay for breakfast in 1120 Kaifeng with silver. The stall keeper just pointed at my coins.

This city runs on copper. And when the street says 100 coins, you count out 75.

#history #songdynasty #ancientchina #timetravel
```

**② 住进客店，换宋装 ·** `S07`（26 s）+ `S08`（28 s）＝ **54 s**
- 裁法：S07 开头 6 秒房门口全景居中 + 模糊铺底，镜头推近她查房之后竖裁；S08 开头 5 秒窗边全景居中，之后逐段中景到特写直接竖裁跟人。
- 钩子字：`Outfit check: 1120`

```text
Checked into an inn in Kaifeng, 1120. First I followed a Song magistrate's advice for travelers: check the walls, check under the bed. Then the surprise: they already sat on chairs.

Then the outfit check, one piece at a time: a short wrap top, a high-waisted skirt, a wide-sleeved jacket left open under the arms, hair wrapped in black cloth.

#history #songdynasty #hanfu #ancientchina
```

**③ 夜市猜价格 ·** `S30`（24 s）+ `S31`（26 s）＝ **50 s**
- 裁法：S30 开头只点油灯的长街居中 + 模糊铺底，包子摊前中景与食物微距竖裁；S31 开头 7 秒彩楼欢门远景居中，阁子里掂银注碗那段竖裁。
- 钩子字：`Guess the price`（停在 S30 的「猜价格」暂停卡上 3 秒）

```text
Guess the price: one stuffed bun at the Zhou Bridge night market, Kaifeng, 1120. Answer's in the clip.

Then a grand wine house where the whole table was silver. The silver was the tableware, not the money. A jug of wine, by the book: 72 coins.

#history #streetfood #songdynasty #ancientchina
```

**④ 桅杆没放下 ·** `S26`（26 s）+ `S27`（20 s）＝ **46 s**
- 裁法：S26 远景冲桥段居中 + 模糊铺底，**镜尾桅杆倒平的特写竖裁**；S27 前 12 秒她望着纤夫的近景竖裁，后 8 秒高位远景段居中加上下模糊铺底。
- 钩子字：`The mast is still up`

```text
Rainbow Bridge, Kaifeng, 1120. A grain boat comes at the bridge with its mast still up. The whole crew throws itself at the mast.

The Qingming scroll shows a boat lowering its mast too. And some of the men who worked these boats never went home again.

#history #qingmingscroll #songdynasty #ancientchina
```

### 精华版（建议 · 90–120 s）

`S02`（30 s，航拍俯冲到宣德楼 + 签名开场画外）→ `S04`（28 s，虹桥一镜到底）→ `S09`（26 s，拿银子付账）→ `S26`（26 s，虹桥险情）＝ **110 s**

- 裁法：四镜里三镜是远景 / 全景，**整条用「16:9 居中 + 上下文字区」**，不竖裁。
- 这四镜在正片里不相邻，生成器只机检了相邻镜的切口；拼完从头看一遍，接得不顺的地方用户自行处理。
- 结尾停在 S26 桅杆倒平的那一帧。

```text
Over 900 years ago, one city, one day: a flight over Kaifeng to the palace gate, the Rainbow Bridge in one take, a breakfast I tried to pay for with silver, and a boat that nearly hit the bridge.

The whole day is in the long video.

#history #songdynasty #kaifeng #ancientchina #timetravel
```

| 字段（每条切条与精华都一样） | 值 |
|---|---|
| **AI 生成内容标签** | **开** |
| 封面 | 各条自己的镜里挑一帧：① S09 摊主指钱串 ② S08 转半圈 ③ S30 包子特写 ④ S26 桅杆倒平 ⑤ S26 桅杆倒平 |
| 声音 | 英文原声，不叠平台音乐 |

**判断**：切条挑的是「笑点 + 身体体验 + 猜价格 + 当天大事」四类，不再用提案 §A.4 旧版切条清单（街头民调 / 采访）。（理由：当地人静默之后没有采访可切；§F.12 读数 F7-5 的高播放开头几乎都在 5 秒内给一个数字或实物，四条的钩子字都照这个写。）

---

## 5. 抖音 · 中文

**字段上限**：标题建议 ≤55 字 ｜ 话题 3–5 个
**画幅**：**横屏直投**（16:9 完整片）；发布页要横 / 竖两张封面时，横封面用 S04 原帧，竖封面按第 2 节 3:4 裁。

### 标题

```text
时空旅行·第1站｜汴京清明一日：揣一贯铜钱逛北宋汴京一整天，还住了一晚客店
```

### 简介

```text
宣和二年清明，北宋汴京。
我揣着一贯铜钱，从城外虹桥走进这座城，逛了一整天——

早饭掏碎银，摊主直摇头：这座城只认铜钱，街上说一百文，只数七十五枚。
御街两百多步宽，中间朱漆杈子围出来的御道，人和马都不许进。
清明全城出郊，轿子顶上插满杨柳；回到虹桥，正赶上一艘船桅杆没放下，冲着桥洞过来。
瓦子勾栏里跟着全场一起笑，州桥夜市的包子一个不过十五文。
早上在客店放下东西，夜里回来睡，五更天有人打着铁牌报晓，把我敲醒。

听着像编的，但片里每个数字都有出处；拿不准的，我当场说是推测。

【声明】本片由 AI 生成：汴京的街景、人物和事件，是依据《东京梦华录》《清明上河图》等史料做的 AI 情景复原；旅行者林问是虚构人物，她的解说是 AI 配音演绎；片中当地人全程不说话。
```

### 话题

```text
#清明上河图 #东京梦华录 #北宋 #汴京 #时空旅行
```

### 置顶评论

```text
只问这一站：给你一贯铜钱，在 1120 年的汴京待一天，你第一文钱花在哪？
发现片里哪儿不对，带上出处回复在这条下面，我们把更正补进这条置顶。
```

### 其余设置

| 字段 | 值 |
|---|---|
| 文件 | 中文版 `sk1_zh.mp4` |
| 封面 | `S04` 桥中回望 + 中文封面字 `1120 · 汴京` / `清明这一天` |
| **作者声明** | 发布页「添加声明」→ **「内容由 AI 生成」**；声明栏若允许多选，另勾「虚构演绎」一类的选项 |
| 合集 | 《时空旅行》 |
| 章节 | 创作者中心提供「章节」时，照 YouTube 中文说明里那组时间点填（成片后重排） |
| 位置 | **不填** |
| 字幕 | 用户后期加中文字幕 |
| 允许 | 评论 / 合拍 / 下载 全开 |

**判断**：声明只能单选时选「内容由 AI 生成」，「演绎」那一层交给简介末尾的【声明】段和片头字卡。（理由：AI 标识办法 2025-09-01 施行，是限流下架的硬线，proposal §E.3 ①；演绎声明在简介和片头都有，不会漏。）

**判断**：抖音不加定位。（理由：今天的开封不等于 1120 年的汴京，加了定位会被当成实地探店；汴京已经作为话题出现。）

**判断**：标题用「时空旅行·第1站」作前缀。（理由：README 规定系列名只作前缀；proposal §E.1 要求节目式编号「第 N 站」，避开「第 N 集」式的短剧包装。）

---

## 6. 小红书 · 中文

**字段上限**：标题 **≤20 字**（超出直接截断）｜ 正文 ≤1000 字 ｜ 话题 ≤10 个 ｜ 封面建议 3:4 竖版
**画幅**：视频是 **16:9 横屏直投**；**封面单独出一张 3:4 竖裁**（第 2 节）。

### 标题

```text
汴京清明一日｜我在北宋住了一晚客店
```

**判断**：小红书标题不放「时空旅行」，系列名落到合集、正文第一行和话题里。（理由：20 字上限放不下「系列名 + 站名 + 钩子」三件；站名「汴京清明一日」是必须保留的那一半。）

### 正文

```text
《时空旅行》第 1 站 · 汴京清明一日
宣和二年（1120）清明，北宋汴京。从城外虹桥走进城，逛到天黑，住一晚客店🌙

🪙 带的钱｜一贯铜钱。拿碎银付早饭钱，摊主直摇头——这里买东西用铜钱
🧮 数钱｜街上说一百文，只数七十五枚，这叫省陌
🥣 早饭｜早市粥饭点心，一份不过二十文
🥟 夜宵｜州桥夜市的包子，一个不过十五文，三更才散
🍶 喝的｜正店银瓶酒一角七十二文；满桌银器是酒具，不是钱
👘 穿的｜在客店换宋装：短襦、长裙、宽袖褙子、包髻露额
🌿 当天大事｜清明全城出郊，轿子顶上插满杨柳杂花；城南迎祥池一年只开这一天
🎭 玩的｜瓦子里大小勾栏五十多座，最大的棚能坐几千人
🛏 住的｜早上放下东西，夜里回来睡；五更天有人打铁牌报晓，把我敲醒

最想让你看的两个画面：
① 虹桥一镜到底，从桥头一路走到桥尾的「十千脚店」
② 午后一艘船桅杆没放下，冲着虹桥过来，水手扑上去放桅

片里每个数字都有出处字卡，拿不准的会当场说「这是推测」。
本站存疑一条：《清明上河图》的「清明」是不是指清明节，学界到现在没定论。

【声明】画面由 AI 生成，是依据《东京梦华录》《清明上河图》等史料做的情景复原；旅行者是虚构人物，解说是 AI 配音演绎；当地人全程不说话。

#时空旅行 #清明上河图 #东京梦华录 #北宋 #宋朝生活 #汴京 #开封 #历史冷知识 #AI复原 #古人的一天
```

### 置顶评论

```text
只问这一站：给你一贯铜钱，在 1120 年的汴京待一天，你第一文钱花在哪？
片里哪儿不对，带出处回在这条下面，更正会补进置顶～
```

### 其余设置

| 字段 | 值 |
|---|---|
| 笔记类型 | 视频笔记（中文版 `sk1_zh.mp4`） |
| 封面 | `S04` 桥中回望 · **3:4 竖裁**（脸在上三分之一）+ 中文封面字 `1120 · 汴京` / `清明这一天` |
| **内容声明** | 发布页声明选项里选 **「含 AI 生成内容」**（名称以发布页实际选项为准） |
| 合集 | 《时空旅行》 |
| 话题 | 见正文末尾（10 个） |
| 位置 | 不填 |

### 图文笔记（另发一条 · 9 张图）

**主题：一贯铜钱，在 1120 年的汴京能买什么**——9 张图全部取自正片帧，价格字和出处小字由用户后期加；这条图文同样要打 AI 声明。

| # | 取帧 | 图上大字 | 出处小字 |
|---|---|---|---|
| 1 封面 | `S09` 摊主摇头、指她腰里的钱串（3:4 竖裁） | `一贯铜钱，在汴京能买什么？` | —— |
| 2 | `S09` 数钱的手特写 | `说一百文，只数七十五枚` | 《东京梦华录》卷三 |
| 3 | `S10` 粥饭特写 | `早市粥饭点心 ≤ 20 文` | 《东京梦华录》卷三 |
| 4 | `S05` 脚店桌上的银注碗 | `小酒店下酒菜一份 ≤ 15 文` | 《东京梦华录》卷二 |
| 5 | `S13` 她骑在驴上 | `路远租头牲口骑 ≤ 100 钱` | 《东京梦华录》卷四 |
| 6 | `S30` 包子特写 | `州桥夜市包子一个 ≤ 15 文` | 《东京梦华录》卷二 |
| 7 | `S31` 银瓶酒 | `银瓶酒一角 72 文` | 《东京梦华录》卷二 |
| 8 | `S31` 掂银注碗 | `满桌银器是酒具，不是钱` | 《东京梦华录》卷四 |
| 9 | `S12` 码头扛袋的人 | `普通劳动者一天约 100 文` | 程民生估算（《宋人生活水平考察》《宋代物价研究》） |

**图文标题**

```text
一贯铜钱在北宋汴京能买啥
```

**图文正文**

```text
《时空旅行》汴京清明一日的账本，全部按书上记的价：

早市粥饭点心，一份不过二十文
小酒店下酒菜，一份不过十五文
州桥夜市包子，一个不过十五文
正店银瓶酒，一角七十二文
路远租牲口骑，不过一百钱

对照一下：一个普通劳动者一天挣一百文上下（程民生估算）。
还有两个坑：街上说一百文只数七十五枚；满桌银器是酒具，宋朝人不拿银子买东西。

【声明】图片取自 AI 生成的情景复原视频；价格出自《东京梦华录》等史料。

#时空旅行 #东京梦华录 #北宋 #宋朝物价 #清明上河图 #历史冷知识
```

**判断**：图文卡只放 ✅ 条目（`money.002` `price.003` `price.002` `job.018` `price.001` `price.005` `money.007` `price.024`），不放客店一晚的价钱和斗米价。（理由：客店价是 `ai_draft`，斗米价是推算的 ⚠️，截图后没法再挂口播说明。）

**判断**：第 2 张大字仍写「说一百文，只数七十五枚」（`money.002` ✅），不改成片里的「二十文数十五枚」——那是按比例推算的（`money.009` ⚠️），截图后没法挂推测口播（R5 F02 对图文卡的这一半不采纳）。

**判断**：第 5 张写「租头牲口」而不写「租驴」。（理由：原文是「租鞍马」，片里拍成驴；写「牲口」对得上画面，也不违背原文。）

---

## 7. 平台对照 + 发布前检查清单

| 项 | YouTube | TikTok | 抖音 | 小红书 |
|---|---|---|---|---|
| 语言 | **英文**（另挂中文音轨 + 中文标题说明） | **英文** | 中文 | 中文 |
| 片名 | *One Day in Kaifeng, 1120* · *Posted to the Past* | 同左 | 时空旅行·第1站｜汴京清明一日 | 汴京清明一日（系列名进合集） |
| 文件 | `sk1_en.mp4` + `sk1_zh_audio.wav` | `sk1_en.mp4` | `sk1_zh.mp4` | `sk1_zh.mp4` |
| 画幅 | 16:9 原生 | 16:9 直投（切条为建议） | 16:9 直投 | 16:9 直投 + 3:4 封面 |
| 时长 | ≈ 14:58 | 完整片 + 4 条切条 + 1 条精华（建议） | 完整片 | 完整片 + 9 图图文 |
| 封面 | S04 · `1120 / KAIFENG` | S04 · 同左 | S04 · `1120 · 汴京` | S04 · 3:4 竖裁 |
| AI 标识 | Altered content = Yes | AI-generated content = On | 内容由 AI 生成 | 含 AI 生成内容 |
| 演绎声明 | 说明「How this was made」 | caption 第三段 | 简介【声明】 | 正文【声明】 |
| 史料链接 | 3 条 | —— | —— | —— |
| 章节 | 26 条 | —— | 有「章节」功能时填 | —— |
| 置顶评论 | 同一个问题（英） | —— | 同一个问题（中） | 同一个问题（中） |
| 互动 | 社区测验帖（猜包子价） | 切条 ③ 猜价格 | —— | 图文账本 |
| 标题上限 | 100 字符 | —— | ~55 字 | **20 字** |
| 合集 / 播放列表 | `Posted to the Past` | —— | 《时空旅行》 | 《时空旅行》 |

### 发布前检查

- [ ] 传的是最终成片，不是 previz、不是旧版；中英两版画面逐帧一致，只有解说轨不同
- [ ] **画面里没有字幕、没有水印、没有 logo**；片头字卡与片尾考证卡是后期叠的，字对了
- [ ] **四站 AI 标识全部打开**：YouTube Altered content = Yes ／ TikTok AI-generated content = On ／ 抖音「内容由 AI 生成」／ 小红书「含 AI 生成内容」；TikTok 切条、精华与小红书图文也逐条打开
- [ ] mux 没有剥离生成元数据（R2 / R12）
- [ ] **考证卡的「本站 {N} 条事实 · {M} 条存疑」已在发布当天用 `python tools/facts_registry.py ai_videos/shikong_lvxing/sk1` 填好**；YouTube 英文说明、中文说明两处的 `{N}` `{M}` 同步替换，页面上不再剩任何花括号
- [ ] **字幕由用户后期添加**：YouTube 英文 SRT + 中文 SRT、TikTok 英文、抖音 / 小红书中文；专名拼写对照第 3 节
- [ ] **YouTube 中文音轨已上传**（语言 → 中文 → 音频），与母版等长；中文标题和说明已粘贴
- [ ] YouTube 自动配音已开，并抽听过专名
- [ ] **章节时间已按成片实际时间重排**（rule 16.7）；首条 `00:00`、每条 ≥10 s；S36 不入片时已删最后一行；中文说明里那组时间点同步重排
- [ ] 片尾 S34 口播的评论问题与三站置顶评论是同一个问题；片中与各站文案都**没有**「下一站去哪」
- [ ] YouTube 社区测验帖在上线前 1–3 天发出；上线后回复了正片链接
- [ ] 当地人零台词：成片里没有任何听得清字句的古人说话声
- [ ] 中文标题和简介里没有「剧 / 集 / 连载」，没有「新闻 / 报道 / 记者」
- [ ] 小红书标题 ≤20 字，正文 ≤1000 字，话题 ≤10 个；抖音话题 3–5 个
- [ ] 封面：S04 帧有清楚的侧脸（没有就换 S02 / S26）；小红书那张是 3:4 竖裁；右下角没压字
- [x] W7–W11 已合并；文案里医馆 / 官府 / 皇宫 / 园林 / 瓦子 / 客店的说法已与定稿镜头的中英台词对过（2026-09-14 SYNC_sk1）
- [ ] **改过任何 shot 的话**，章节、切条剪法、精华剪法、封面帧时间全部重算（rule 16.7）
