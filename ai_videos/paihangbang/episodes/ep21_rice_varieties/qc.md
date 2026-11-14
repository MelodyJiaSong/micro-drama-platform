# ep21 · 30 Kinds of Rice Around the World · 审片记录

## 第 1 轮独立审片 — 2026-11-06

> 审片人：另起上下文的独立审片代理，没有参与本期的数据、出图和渲染。只新建了本文件；没有改其他文件，没有重渲，也没有调用收费服务。抽帧放在仓库外的临时目录，审完即删。

**结论：小修后可发布。** 不需要重做配图，但下面的 blocker 和 major 都要先改完，再重渲、重新生成 `publish.md`。改的都是文字、数据和计分板配置。

### 核对依据

- **成片**：`render/ep21_rice_varieties_master.mp4`，1920×1080，60 fps，244.833 s。音轨是 `anullsrc` 静音轨（静音母版，配乐项第 6 项本轮跳过）。
- **manifest 一致**：output_sha256 `9b75cbd2…` 与文件一致。inputs 中 `data.json`（`e519d286…`）、`assets.json`（`019a36f0…`）与当前文件一致，所以本轮结论对应当前产物。
- **时间线**：intro 0–5，scroll 5–211.83，champion（列表模式下是末卡停留）–215.83，tally –222.83，sources –226.83，end –244.83 s。
- **抽帧**：每 4 s 抽 1 帧，缩到 960 px，共 61 帧。另外补抽了 2.5、4.5、210、213、215.5、216.5、223、225 s。
- **对照材料**：`data.json`、`sources.md`、`topic.md`、`publish.md`、`_build/research.md` §5、`bible.md` §2.4 与 §7、README 的 Vision。
- **外部核对**：只做了网页检索，用于 #23 和 #16 两条（见 B1、m3）。

### §7 清单逐项

| # | 项 | 结论 |
|---|---|---|
| 1 | 顺序与 data.json 一致 | ✅ 30 张卡顺序与 data.json 一致：Koshihikari → … → Wild Rice。5 张洞察卡分别在 #3、#8、#16、#25、#26 之后，没有重复或缺卡。列表模式不显示名次药丸，正确。 |
| 2 | 每条上屏内容能在 sources.md 追到出处 | ❌ 见 M3、M4、B1 |
| 3 | 国旗与国家对得上 | ⚠️ 28 张正确：JP/CN/ID/VN/LA/TH/MM/IN/NP/UZ/IR/TR/IT/FR/ES/PT/EG/NG/ML/BR/MX/US 旗形都核过。Basmati、Wild Rice 两张卡的国家写的是双国，却只挂一面旗，见 M2、m6 |
| 4 | 配图闸门 | ✅ 已由 tile_gate 通过（本轮不重审）。30 张都是 AI 图，每张卡有 AI IMAGE 药丸，底部有「AI-generated image, not a photo」 |
| 5 | 文字不出框、手机可读 | ✅ 30 张卡居中时都没有出框或截断。大字粒型、品种名、国家都清楚。标签行在 1080p 下约 26 px，勉强可读。右上「RICE BY COUNTRY」和卡底 AI 小字太小，只是辅助信息 |
| 6 | 音乐 | 跳过（尚未配乐） |
| 7 | 描述框来源与署名 | ⚠️ 见 M4、m9、m10 |

### Blocker

**B1 · #23 Carolino 徽章「PORTUGAL'S FAVOURITE」与事实不符（约 2:28–2:40）**
- 问题：`sources.md` 给的出处（Observador / ANIA 2023）只说葡萄牙人均每年吃约 16 kg 白米，不能证明 Carolino 是最受欢迎的品种。检索到的市场份额数据正好相反：ANIA 2021 年数据中 agulha 占 46.8%、carolino 占 21.9%；INIAV《Campanha Agrícola 2023》（引 COTArroz）中 agulha 占 50.4%、carolino 占 18.1%，而且 carolino 在逐年下降。同一张卡的标签「16 kg/person a year」也会让人以为这 16 kg 都是 Carolino。
- 修：徽章改成有出处的说法，例如「PORTUGAL'S NATIVE RICE」或「EU PGI SINCE 2008」，后者的出处 EUR-Lex 670/2008 已在 sources.md。标签改成「Portugal: 16 kg rice/person/yr」，或者换成「Soaks up broth」（原第二个标签，目前没显示）。sources.md 的 #23 行同步更新。

### Major

**M1 · 观众看不出这些米的区别：大字「粒型」不在同一个维度上，而且白米卡彼此太像（全片，尤其 0:05–1:25、2:10–3:30）**
- 问题：README Vision 要求「一眼看懂」，本期 topic 也明确「重点是给观众展示世界各种不同的大米」。实际成片有三处做不到：
  1. **大字不在同一维度**。主数值位本该让观众横向比较，现在混着五种东西：
     - 长短：Short / Medium / Long / Extra-long / Long & thin
     - 体积：Large / Bold / Plump / Round / Tiny / Ribbed
     - 黏性：Glutinous
     - 颜色：Black rice / Red rice
     - 加工或物种：Broken / Unpolished / Whole grain / Own species / Aquatic grass

     结果是同类米用了不同的词：Koshihikari、Wuchang、Egyptian 写「Short grain」，Calasparra、Pandan Wangi 写「Round grain」，Paw San 写「Plump grain」，Gobindobhog 写「Tiny grain」，观众无法判断这些词之间有什么差别。Hashemi 的「Long grain」与 Agulhinha 的「Long & thin」差在哪里，屏上也没有交代。
  2. **约 19 张白米卡的主图几乎一样**：都是近距离的一堆白米，有的是生米，有的是熟饭（Koshihikari、Pandan Wangi、Paw San 是饭，Yamada Nishiki、Zengcheng、Basmati 是生米），也没有统一的尺寸参照。观众看不出 Gobindobhog「Tiny」比 Koshihikari 小，也看不出 Carnaroli 和 Morelos 两张「Large grain」有什么不同。真正一眼能分开的只有有颜色的那几张：紫、黑、红、野米。
  3. **能区分米的信息被渲染器丢掉了**。标签放不下时从后往前丢，30 张卡里约 19 张只显示了第一个标签。被丢掉的包括 Zengcheng、Paw San 的「Aromatic」，Basmati 的「Nutty aroma」，African Rice 的「Oryza glaberrima」（这正是「Own species」的依据）。与此同时，好几张卡在重复同一信息：
     - Pandan Wangi 的「fragrant」出现 3 次
     - Jumli Marshi 是「Red rice」加「Red grain」
     - Egyptian 是「soft & slightly sticky」加「Soft & sticky」
     - Wuchang、Hashemi 也都把「香」写了两遍
- 修（只改 data.json 和配置，不需要重出图）：
  - 大字统一写**粒长等级**，四档：Short / Medium / Long / Extra-long，按 research.md 已有的粒型归类，口径在 sources.md 写明（例如 USDA 或 Codex 粒长分级）。
  - 副字（secondary）统一写**口感**：Sticky / Soft & clingy / Fluffy & separate / Creamy / Firm & chewy。
  - 第一个标签统一写**颜色和香气**：White · Aromatic、Red bran、Black → purple 等。
  - 「Glutinous / Broken / Unpolished / Own species / Not true rice」这类特殊身份放到徽章位。
  - 每张卡上屏的标签控制在只显示 1 个也不丢关键信息，删掉重复项。
  - 另外建议把一张洞察卡换成直接讲「区别」的：例如「Sticky or fluffy? It's the starch: glutinous rice has almost no amylose; basmati has lots.」，出处可用已列的 Olsen & Purugganan 2002 加一条直链淀粉含量来源。

**M2 · Basmati 只挂印度旗，计分板也只算给印度（约 1:43–1:52；计分板 3:36）**
- 问题：卡上国家写「INDIA / PAKISTAN」、产区写「Punjab, India & Pakistan」，旗却只有印度一面，国名和国旗对不上（§7 第 3 项）。计分板把这张卡算进印度，所以印度以 4 张「赢得」计分板。印巴的 basmati 地理标志正在争议中，research.md §3.4 也写了「Do not claim one country 'owns' basmati」，这样会引来巴基斯坦观众的抵触。
- 修：首选双旗（渲染器如果支持）；不支持就不挂旗，改用中性图标，并且这张卡不计入任何国家。至少要在计分板上把它从印度的计数里拿掉，或者同时计入印度和巴基斯坦。

**M3 · `research.md` §5 的待核项还没关闭，其中有几条直接上了屏或进了发布稿**
- 问题（时间为该卡在画面中央时）：
  - #11 Paw San 徽章「WORLD'S BEST RICE 2011」（约 1:16）：FFTC 一手页面返回 403，没有打开过。
  - #15 Jumli Marshi 徽章「HIGHEST RICE ON EARTH」（约 1:38）：海拔有 3,050 m 和 2,850–2,900 m 两种说法，而且这是个最高级说法。
  - #18 Hashemi 徽章「FOR CHELOW & TAHDIG」（约 2:03）：Iranica 页面返回 403，只看过搜索索引里的内容。
  - #27 卡名「Brazilian Agulhinha」和标签「'Little needle'」（约 3:16）：这个市场名没有任何来源。
  - #25 Ofada（约 2:47）：Comment 2 写的是「Gyimah-Brempong … UPenn Press, pp. 30-31」，链接却是 Wikipedia。这等于把维基百科冒充成专著引用，和本系列「每个数字有出处」的卖点（D1）正相反。
- 修：每一条都由人打开一手页面核对，或者换成可打开的来源，然后在 research.md §5 记下「已核 / 已改」。Jumli 的徽章建议改成「GROWN NEAR 3,000 m」，或者写成有归属的「'Highest rice on Earth' – UNDP」。Ofada 换成书的原页、NCRI / AfricaRice 资料或那篇 AJOL 论文，不要用 Wikipedia 链接冒充书目。Agulhinha 找不到来源的话，卡名改成「Brazilian Long-Grain」，标签换成「For arroz e feijão」。

**M4 · `sources.md` 自称覆盖粒型、徽章和标签，实际每条只给了一个 fact 的出处；本期最核心的上屏内容「粒型、口感」没有出处**
- 问题：sources.md 表头写的是「每条卡面文字（粒型、badge、tags）与 fact 的出处」，但表里只有 fact 一列。有些 fact 根本不上屏，例如 #8 Lao 的 IRRI 种质库那条；而上屏的「Short grain」「Extra-long」「Tiny grain」「Buttery scent」「Rolled into balls」「Stuffed into mahshi」「Pinkish tint」等都没有出处。research.md 自己也写着 #17 的颜色只出自旅游和贸易页面。§7 第 2 项不通过。
- 修：sources.md 每行加两列：「粒型 / 口感出处」和「徽章出处」，GI 规格书、品种登记、FSSAI、GB/T 等基本都有粒型描述。找不到出处的描述性词，要么删掉，要么改成主观程度更低的说法。改完后按 M1 的新文字重新对一遍。

**M5 · 国家计分板在列表期没有意义，还容易误导；片尾也缺高潮（3:28–3:43）**
- 问题：
  - 这一期是编辑挑选的 30 种米，「Rice by country」只反映选题时的取舍，印度 4、日本 3。观众很容易读成「印度的米种最多」，这个结论没有依据。
  - 美国的 2 张里有一张是「NOT TRUE RICE」的野米（而且是美加共有），印度的 4 张里有一张是印巴共有的 Basmati。
  - 右上角计数从第 17 张起基本不再变化，后半程没有悬念。
  - 末卡 Wild Rice 停在画面中线偏左约 6 s（约 3:28–3:36），右边三分之一是空的，「NOT TRUE RICE」这个结尾惊喜没有得到强调，画面直接跳到一个高亮印度的条形图。
- 修：
  - 计分板改为 `tally.by = continent`（Asia 19 / Europe 4 / Africa 3 / Americas 4），或者最好改成按粒长或类型统计（Short x / Medium x / Long x / Extra-long x / Sticky x / Coloured x），这样结尾正好对 M1 做一次回顾。
  - 渲染器在列表模式下应让末卡居中，并给「NOT TRUE RICE」徽章一个强调。如果改不了渲染器，至少把末卡停留缩短。

### Minor

- **m1 · 片头副标题（0:00–0:05）**：「Grain type · A tour from Japan to the Americas」把 metric_label 当成了副标题，读起来像字段名，也没有告诉观众会看到什么。改：period_label 或副标题写成「Short, long, sticky, red, black – and one that isn't rice at all」；metric_label 不进副标题。
- **m2 · 角标重复（0:05–2:20）**：19 张卡连续写「ASIA」，几乎没有信息。改：corner 用次区域（EAST ASIA / SOUTHEAST ASIA / SOUTH ASIA / CENTRAL & WEST ASIA），顺便把「from Japan to the Americas」这条旅程线表现出来。
- **m3 · #16 Basmati 标签「Doubles in length」（约 1:45）**：FSSAI 2023 标准要求非蒸谷 basmati 煮后伸长比 ≥ 1.7（蒸谷米 ≥ 1.5），不是 2 倍。改：「Grows 1.7x+ longer」，或者删掉。如果 M1 改版后这张卡的大字仍写 Extra-long，保留徽章「12 mm WHEN COOKED」就够了。
- **m4 · #9、#11 两张「WORLD'S BEST RICE」徽章**：这是行业刊物 The Rice Trader 的评选，不是官方称号；Hom Mali 也不止 2021 年得过。改：「WORLD'S BEST RICE AWARD 2020–21」「… AWARD 2011」，或者写成「'World's Best Rice' 2011」。
- **m5 · #5 Zengcheng 标签「3.5x longer than wide」**：标准原文是「> 3.5」，而且出处是广东丝苗米标准，不是增城的地理标志标准。改：「Over 3.5x longer than wide」，sources.md 注明口径。
- **m6 · #30 Wild Rice（3:20–3:36）**：国家写「UNITED STATES / CANADA」，只挂美国旗，还计入美国。处理同 M2：双旗，或者不计入任何国家。
- **m7 · 洞察卡分布不均**：#25 和 #26 之后各有一张，两张之间只隔一张卡，约 7 s；#16 到 #25 之间没有洞察卡，美洲段也没有。改：ceebu jën 那张移到 #22 或 #23 之后，或者把 World Food Prize 那张移到 #28 之后。最好再加一张讲「区别」的洞察卡（见 M1）。
- **m8 · 来源卡（3:43–3:47）**：只有 4 s，还夹着与来源无关的「A tour from Japan to the Americas」。「Image credits: shown on each card」也没有说明全部配图都是 AI 生成。改：删掉旅程行，加一行「All rice images are AI-generated illustrations, not photos」。
- **m9 · publish.md 描述框文字**：
  - 首段「30 entries one by one, in order (not a ranking), each with its grain type (A tour from Japan to the Americas).」是模板句，读起来生硬。
  - 「Every number on screen is sourced (per-item links in the pinned comment)」：这一期主要是事实陈述而不是数字；而且逐条链接在 Comment 2（回复）里，置顶的 Comment 1 只有图片署名。
  - scope_note 说「Sources for every fact are listed below」，描述框里其实没有逐条来源。
  - 30 行「AI illustration (AI-generated (Codex image_gen))」括号套括号，描述框和 Comment 1 各重复一遍；「resized and cropped, no other changes」对 AI 图来说也不适用。
  - hashtag「#DataComparison」不贴题。

  改：首段人工重写，例如「From sticky Japanese mochigome to Indian basmati and the 'rice' that isn't rice: 30 kinds of rice, what makes each one different, and where it grows.」；来源说明改成「per-item sources in the replies under the pinned comment」；30 行署名合并成一句「All 30 rice images are AI-generated illustrations (Codex image_gen), not photos」；hashtag 改成 #Rice #FoodGeography #RiceVarieties。
- **m10 · publish.md 缺 Tags 栏和封面**：ep11、ep12 等期都有「## Tags（YouTube 标签栏）」，本期没有；检查清单里的 `render/thumbnail.png` 也不存在。改：补标签（rice varieties, types of rice, basmati, jasmine rice, koshihikari, sticky rice, black rice, red rice, wild rice, risotto rice, paella rice…）并出封面。配乐后还要补 Suno 署名和「不登记 Content ID」一条，再重新生成 publish.md。
- **m11 · 计分板小字**：右上「RICE BY COUNTRY」约 16 px，在手机上看不清。如果按 M5 保留角落计分板，标签字号放大到与卡上标签同级。

### 已确认无问题

- 30 张卡居中时，文字、徽章、标签都没有出框。
- 国旗旗形正确，都在飘动，各卡相位错开。
- 列表模式没有名次药丸。
- 洞察卡文字都在卡内。
- 片尾 18 s 留出了 YouTube 片尾元素区。
- 「Altered or synthetic content」已在清单里写为 Yes，每张卡都有 AI 标识，符合 bible §4。
- 章节时间点与画面对得上：0:45 Broken Rice、1:28 Gobindobhog、2:10 Tosya、2:48 Ofada、3:36 计分板，都已在画面上逐一确认。

### 外部核对来源

- [INIAV, Campanha Agrícola 2023 (COTArroz market shares)](https://iniav.pt/images/Noticias/Campanha_Agrícola_2023.pdf)
- [24noticias / Lusa, Portugueses comem 16 kg de arroz branco por ano (ANIA 2021 shares)](https://24noticias.sapo.pt/atualidade/artigos/portugueses-comem-16-kg-de-arroz-branco-por-ano)
- [Down To Earth, FSSAI sets standards for basmati rice](https://www.downtoearth.org.in/news/food/fssai-sets-standards-for-basmati-rice-to-be-enforced-from-august-87105)
- [FoodNavigator-Asia, India launches Basmati rice standards (elongation ratio 1.7 / 1.5)](https://www.foodnavigator-asia.com/Article/2023/03/22/india-launches-basmati-rice-standards-amid-longstanding-geographical-dispute-with-pakistan)

## 第 2 轮独立复核 — 2026-11-06

> 复核人：另起上下文的独立审片代理，没有参与本期的制作和修订。本轮只在本文件末尾追加了这一节，没有改其他文件，没有重渲，也没有调用收费服务。抽帧放在仓库外的临时目录（`%TEMP%/ep21qc2`），缩小后查看，审完已删。

**结论**

- **英文版：小修后可发布。** 画面上已经没有 blocker。剩下的 major 都在来源和描述框里（见 R2-M1）。
- **中文版：需返工。** 6 张「你知道吗？」洞察卡的中文不换行，正文被卡片边缘截掉，一句也读不全（R2-B1）。修复只涉及渲染器的中文换行，改好后重渲中文版即可，数据和配图都不用重做。

### 核对依据

- **英文成片** `render/ep21_rice_varieties_master.mp4`：output_sha256 `58f1f9cd…`，与文件一致。manifest inputs 中的 `data.json`（`2173b30e…`）、`assets.json`（`019a36f0…`）、30 张图、2 段 Suno 音乐的 sha256 都与当前文件逐一相同。结论对应当前产物。
- **中文成片** `render/ep21_rice_varieties_master_zh.mp4`：output_sha256 `9f2cac62…`，与文件一致。
  - manifest **没有记录 `data.zh.json` 的哈希**，只记了 `data.json`（见 R2-m14），所以无法用哈希证明成片对应当前的 `data.zh.json`。
  - 用三种办法补证，结论是成片对应当前 `data.zh.json`：
    1. `data.zh.json` 的修改时间 23:28，早于渲染时间 23:35。
    2. `_build/zh_fix.py` 对当前 `data.zh.json` 是幂等的。我在内存里模拟运行，结果无变化。
    3. 逐卡抽帧，卡面文字与 `data.zh.json` 一一对得上。
  - 另外，`projects/rank_scroll/rank_scroll/{draw,cards}.py` 在 11-07 00:01 被改过，晚于两版渲染。当前成片不反映这次改动。
- **时间线**：intro 0–5，scroll 5–216.5，末卡 –220.5，tally –227.5，sources –231.5，end –249.5 s（4:09.5）。
- **抽帧**：
  - 用 `rank_scroll.timeline` 算出 36 个元素（30 张卡 + 6 张洞察卡）各自居中的时刻，在这些时刻对中英两版各抽 1 帧，裁出中间的卡并排对照。
  - 另外抽了 1、2.5、4.6、7、160、200、218、222、229.5、233、245 s，还有中文版每张洞察卡前后各 2 s。
- **自动检查**：`zh_edition.py gate` 通过。

### 第 1 轮问题逐项复核

| 项 | 结论 | 证据 |
|---|---|---|
| B1 Carolino 徽章 | **已修** | 徽章改为「EU PGI SINCE 2008」（2:40.8）。只显示的标签是「White japonica · Soaks up broth」，不再暗示 16 kg。sources.md 第 29、40 行已同步 |
| M1 大字不在同一维度 | **部分（主体已修）** | 大字已统一成 Short / Medium / Long / Extra-long，副字统一写口感，第一个标签统一写颜色和香气，也新增了一张讲直链淀粉的洞察卡（1:33.7）。仍有三处没改完：① #7 大字仍是「Broken grain」，不在四档之内（可以接受）；② 重复信息还在，见 R2-m3；③ 白米卡的主图仍然彼此相似（图没换），不过有了统一的粒长档位，观众已经能分辨 |
| M2 Basmati 单旗 | **已修** | 1:51.8 显示印度、巴基斯坦双旗。计分板改为按洲统计，不再计入某个国家 |
| M3 research §5 待核项 | **部分** | 已修 4 条：Jumli 改「GROWN NEAR 3,000 m」；Agulhinha 改「Brazilian Long-Grain」；Hashemi、Paw San 的徽章都换成了不依赖 403 页面的说法。**未修**：#25 Ofada 仍用 Wikipedia 链接冒充 UPenn Press 专著（sources.md 第 31、47 行，publish.md 第 73 行）；Paw San 的 Comment 2 仍链到没打开过的 FFTC 页面（publish.md 第 59 行）。research.md §5 也没有记下「已核 / 已改」。见 R2-M1 |
| M4 sources.md 缺粒型和徽章出处 | **部分** | 加了「On card」「Grain / texture basis」两列，第 3 行写明了 USDA 粒长阈值。但 basis 列只是转述 research.md，没有逐条外部出处，徽章出处也和 fact 合在一列。降为 minor，见 R2-m4 |
| M5 计分板 / 末卡 | **已修，可接受** | 计分板改为「Rice by continent」（3:40.5）：Asia 19 / Europe 4 / Africa 3 / North America 3 / South America 1。末卡 Wild Rice 在 3:36.5–3:40.5 **已经居中**：218 s 帧中卡片中心在画面横向中点，右侧空白只是因为后面没有卡了。停留 4 s。「NOT TRUE RICE」没有额外强调，但在列表模式下可以接受，不阻塞发布 |
| m1 片头副标题 | **部分** | period_label 已改为「From sticky to fluffy, white to black」，但片头和左上角仍显示「Grain length · …」（0:01、0:07），metric_label 依然被当作前缀。中文版同样是「米粒长度 · …」 |
| m2 角标重复 | **已修** | 改用次区域：EAST ASIA / SE ASIA / SOUTH ASIA / CENTRAL ASIA / WEST ASIA / EUROPE / NORTH AFRICA / WEST AFRICA / S. AMERICA / N. AMERICA |
| m3 Basmati「Doubles」 | **已修** | data.json 改为「Grows 1.7x+ longer」（英文卡上放不下，没显示）；中文卡显示「煮后伸长至1.7倍以上」 |
| m4 WORLD'S BEST RICE | **已修，可接受** | #9 改为「'BEST RICE' 2020+2021」，#11 徽章删除了这项奖。小建议：写成「'WORLD'S BEST RICE' 2020–21」信息更完整，前提是放得下 |
| m5 3.5x | **已修** | 「3.5x+ longer than wide」，中文「长宽比超过3.5」，出处口径已在 sources.md 第 11 行注明 |
| m6 Wild Rice 单旗 | **已修** | 3:36.5 显示美国、加拿大双旗 |
| m7 洞察卡分布 | **已修** | 6 张洞察卡分别在 #3、#8、#13、#19、#23、#28 之后，间隔均匀，美洲段也有了 |
| m8 来源卡 | **部分** | 已加「Images: AI-generated」。但 3:47.5–3:51.5 的来源卡第二行仍是与来源无关的「From sticky to fluffy, white to black」 |
| m9 描述框 | **已修** | 首段已重写；来源说明改为「replies under the pinned comment」；AI 署名合并成一句；hashtag 已换 |
| m10 Tags / 封面 / 配乐署名 | **已修** | 已补 Tags 栏；封面 `thumbnail.png` 1280×720；已补 Suno 署名和「不登记 Content ID」一条 |
| m11 计分板小字 | **未修，可接受** | 右上标签仍约 16 px。按洲统计只有 5 项，而且 3:40.5 有 7 s 全屏计分板，角落计分板只是辅助。附带一个小现象：角落计分板最多放 4 个胶囊，进入北美段后 South America 1 被挤掉（160、200、218 s 帧对比），可以接受 |

### 新发现

#### Blocker

**R2-B1 · 中文版 6 张洞察卡的文字不换行、被截断（0:21.0、0:57.3、1:33.7、2:16.3、2:46.3、3:22.7）**
- 问题：
  - `projects/rank_scroll/rank_scroll/draw.py` 第 117 行的 `wrap()` 只按空格断行（`s.split(" ")`）。中文句子里没有空格，整句就成了一行，超出卡片宽度的部分被裁掉。
  - 实际画面：「国际水稻研究所在菲律宾…」「糯米不含麸质：英文里的…」「米饭黏糯还是松散，取…」「全球近一半人口以大米为…」「塞内加尔鱼饭用鱼和碎…」「2004年世界粮食奖：袁…」，每张都只露出前十来个字。英文版换行正常。
  - 这违反 §7 第 5 项「文字不出框」。洞察卡也是 README「每期不一样」的卖点，现在中文观众一句也读不完。
- 修：
  - `wrap()` 对 CJK 文本按字符断行（遵守标点避头尾），或者在中文版的分词阶段先插入可断点。改完重渲 `--lang zh`。
  - 建议同时给渲染器加一道机检：任何文本行宽 > 可用宽度时直接报错。
  - **其他期的中文版只要有洞察卡，大概率也有同样问题**，建议对所有已渲染的 `_zh.mp4` 复查。

#### Major

**R2-M1 · 来源仍有冒充和未核项，而且直接出现在 YouTube 评论里（英文发布稿，以及两版共用的 sources.md）**
- 问题：
  - Comment 2 第 73 行写的是「Gyimah-Brempong … UPenn Press, pp. 30-31」，链接却是 `en.wikipedia.org/wiki/Ofada_rice`。sources.md 第 47 行作者自己也写着「发布前须换」，到现在还没换。这和本系列「每条有出处」的承诺正相反，观众点开链接就能发现。
  - Comment 2 第 59 行 Paw San 链到的 FFTC 页面从来没有打开核对过（research.md §5 第 11 条）。
  - research.md §5 也没有补「已核 / 已改」记录。
- 修：
  - Ofada 换成能打开的一手来源（NCRI / AfricaRice 资料，或者 sources.md 已列的 AJOL 论文作主出处），或者如实写成「via Wikipedia」。
  - Paw San 由人打开 FFTC 页面核对，打不开就把主出处换成 Rice Trader 获奖名单或 Irrawaddy 报道。
  - 然后重跑 publish 生成发布稿。注意：如果改的是 data.json 里的 `source` 字段，manifest 的 data.json 哈希会随之失配，要么重渲，要么在 qc 里记明「只改了 source 字段，画面不变」。
  - 只改 sources.md 和 publish.md、不动 data.json 的话，不需要重渲。

#### Minor

- **R2-m1 · 描述框首段把 basmati 写成单国所有（publish.md 第 13 行、publish.zh.md 第 23、47、76、88 行）**：「Indian basmati」「印度巴斯马蒂香米」与卡面双旗、research.md「Do not claim one country 'owns' basmati」的口径冲突，容易引来巴基斯坦观众的争论。改：英文写「basmati from India and Pakistan」，中文写「南亚的巴斯马蒂香米」。
- **R2-m2 · 片头和左上角仍带字段名「Grain length · / 米粒长度 ·」（0:00–0:05 及全程左上）**：见 m1。改：metric_label 不再拼进副标题，或者改成「4 grain lengths · …」这类给观众看的说法。
- **R2-m3 · 卡内重复信息**：
  - Hashemi 大字「Long grain」加标签「Long & slender」（2:04.5，中英都显示）
  - Calasparra 副字「absorbent」加标签「Soaks up broth」（2:34.5）
  - Carolino 副字「creamy in broth」加标签「Soaks up broth」（2:40.8）
  - Jumli 徽章「GROWN NEAR 3,000 m」加标签「High-altitude rice」（1:45.5）
  - 中文碎米「易吸收酱汁」加「善于吸收酱汁」（0:45.5）

  改：把第二个标签换成新信息，例如 Hashemi 换「Gilan's top landrace」，Carolino 换「For arroz de pato / malandrinho」，前提是有出处；找不到出处就删掉。
- **R2-m4 · 粒长分档缺逐条出处，个别分档与口径定义冲突**：
  - sources.md 第 3 行把 extra-long 定义为「basmati 类细长粒」，但 #28 Morelos 是粗大的「white belly」粒，不细长，却标了 Extra-long（3:17.2）。
  - #30 野米不是稻，套 USDA 稻米分级本身就勉强。
  - #20 Carnaroli 在 research.md 里写的是「medium-long」，卡上却是「Long grain」。

  改：Morelos 按 DO 规格书的原文定档，大概率是「Long grain」。basis 列给出每条的外部依据（GI 规格书或品种登记页），没有就注明「描述性，出自 research §2」。
- **R2-m5 · 来源卡第二行与来源无关（3:47.5–3:51.5，中英两版）**：period_label 被重复放上来源卡。改：来源卡不显示 period_label。
- **R2-m6 · 中文「地标」被当作「地理标志」的简称**：#9「2013泰国首获欧盟地标」（1:02.8）、#23「2008年起欧盟地标保护」（2:40.8）。中文读者通常把「地标」理解为 landmark。改：「2013年成为泰国首个欧盟地理标志」「2008年起受欧盟地理标志保护」。
- **R2-m7 · 中文年份缺「年」，写法不统一**：#9「2013泰国…」、#19「2017土耳其原产地保护」（2:10.8）、#28「2012起墨西哥原产地保护」（3:17.2）。其余各卡都写「…年」。改：统一补上「年」。
- **R2-m8 · 中文译法不准或别扭**：
  - #19 徽章「堪称苏丹御膳」（2:10.8）与原意「曾专供苏丹餐桌」不符。改「曾专供苏丹御膳」。
  - #1「日本头牌大米」（0:05）太口语，「头牌」另有歧义。改「日本种植最多的米」或「日本第一米」。
  - #29「从约6.35公斤种子起步」（3:28.2）：「约」配两位小数，写法矛盾。改「从约6公斤种子起步」。
  - #16「煮熟长12毫米」（1:51.8）：标准是平均不少于 12 mm。改「煮熟后长逾12毫米」，英文可同步改「12 mm+ WHEN COOKED」。
  - #28「垩白米腹」改用行业术语「腹白明显」。
  - #26「非洲稻」可补标准名「光稃稻」。
  - #17 标签「2026年抓饭获地理标志」意思不完整。改「安集延抓饭2026年获地理标志」，放不下就写「2026年获抓饭地理标志」。
- **R2-m9 · 中文洞察卡第 2 条翻译别扭（0:57.3，也出现在抖音、小红书的描述里）**：「英文里的“糯”是指像胶一样黏」，但「糯」是中文字，这句话说不通。改：「糯米不含麸质：英文 glutinous 意为“像胶一样黏”，与麸质（gluten）无关」，或者直接写「糯米的黏来自支链淀粉，不含麸质」。修 R2-B1 时一并改。
- **R2-m10 · publish.zh.md 小问题**：
  - 第 61 行写卡面标「AI图像」，实际卡面是「AI 生成图」（封面是「AI图像」），要对齐。
  - 第 61 行「30张米的图片」改「30张大米图片」。
  - 第 69 行置顶评论「图片署名（作者，授权）：」是模板残留，改「图片说明：」。
  - 第 80 行视频号话题「#排行榜」与「不是排名」矛盾，改「#美食地理」。
  - 第 48 行「每张卡的说法都有出处」：中文平台不放外链，观众看不到出处。改「资料来源见片尾」，或在简介里列出不带链接的来源名。
- **R2-m11 · 中文封面副题与片中不一致**：`thumbnail_zh.png` 写「从黏糯到松散」，片头写「从软糯到松散」，统一成一种。
- **R2-m12 · 中文来源卡的署名行是英文（3:47.5）**：「Flags: flagcdn.com (public domain) · Icons: Tabler Icons (MIT) · Font: Noto Sans SC (OFL)」，可本地化为「国旗：flagcdn（公有领域）· 图标：Tabler Icons（MIT）· 字体：思源黑体（OFL）」。
- **R2-m13 · publish.md 第 37 行 Comment 1 的字数「2192 字符」已过时**：实际正文约 250 字符，是 finish_publish.py 改写后没有重算。重新生成时一并更新。
- **R2-m14 · 中文版 manifest 记录的是 `data.json` 的哈希，不是 `data.zh.json`（`render.py` 第 544 行）**：中文版改数据后，单凭 manifest 无法判断成片是否过期。改：`inputs` 按 lang 记录 `data.{lang}.json`。这一条是渲染器工具问题，可以单独开 follow-up。

### 音频（中英两版音轨逐样本一致，md5 相同）

- **配乐全程都在**：0.4 s 起有声，`silencedetect -45 dB / 0.5 s` 只在 248.65–249.5 s（片尾淡出到底）检出静音，中间没有断档。
- **响度**：整合响度 −16.0 LUFS，LRA 3.5 LU，峰值 −3.7 dBFS（max_volume −3.7 dB），没有削波或爆音。
- **两段 Suno 曲的衔接**：交叉淡化点在约 160.8–163 s，短时 RMS 下降约 3–4 dB，持续约 2 s，听感上是正常的过渡，不是断档。
- **淡出**：片尾从约 246.3 s 开始淡出，到 249.5 s 降到 −104 dB，约 3 s，干净。end 段 231.5–249.5 共 18 s，音乐一直延续，符合 §7 第 6 项「片尾 15–20 秒干净」。列表模式没有前 10 名高潮，这一要求不适用。

### §4b 中文版合规

- `zh_edition.py gate` 通过。全片没有 TW / HK / MO 条目，也没有涉台、涉港、涉澳文字。
- 双旗卡写「印度 / 巴基斯坦」「美国 / 加拿大」，没有领土表述问题。
- 单位为毫米、公斤、米，没有英制显示。
- 字体是 Noto Sans SC（来源卡已标注），没有用微软雅黑。
- 除 R2-B1 外，中文卡面在居中帧中都没有出框，品种名、粒长、口感都清楚。

### 已确认无问题

- 30 张卡的顺序、国旗、次区域角标与 data.json / data.zh.json 一致。列表模式不显示名次药丸。每张卡都有「AI IMAGE / AI 生成图」药丸和底部 AI 小字。
- 章节时间点与画面对得上：0:45.5 碎米、1:28.2 Gobindobhog、2:10.8 Tosya、2:58.2 Ofada、3:40.5 计分板。publish.md 和 publish.zh.md 两份章节都正确。
- 两张封面都是 1280×720，四张样图都有 AI 标识。
