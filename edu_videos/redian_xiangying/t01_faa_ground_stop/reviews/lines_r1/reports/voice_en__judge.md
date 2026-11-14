# voice_en__judge 裁决（第 1 轮）

核对依据：被审材料 `materials/voice_en.md`、讲稿 `script.en.md`、`scenes/web/s2.html`、`s4.html`、`timeline.en.json`。注意 `timeline.en.json` 带 `"estimated": true`，配音还没出，材料里的时长是按词数估出来的（`tools/edu_video.py --estimate`），不是实测语速。

## 裁决
- V1 1 理由：取 b。a 自己把 l71、l01 判成 V1 必改，却给了 2 分，前后矛盾。另外 l83「treat the replacing」（结尾，严格项）、l65 用间接疑问句冒充直接疑问句（章末，严格项）、l15 的「名词短语 + 从句」带时态突变、l80「the accident」没有所指，都确实是 off 的。按评分规则，有必改就是 1 分。
- V2 1 理由：取 b。a 自己把 l62 判成 V2 必改。严格项里还有：l24「what follows」是播报腔的过渡句；l25 先用祈使句「Look back」再接「we see」，人称不统一；l65、l54 章末收得不顺。章卡「The worst ones」「Not always a change」也都含糊。严格项里只要有「a bit off」就是必改，所以 1 分。
- V3 1 理由：取 b。l71「design the switchover as the most dangerous phase」听一遍可能理解成「故意把切换设计得危险」。l47 technical debt 没铺垫；l12 en route centers 没解释；l28 在航空语境里「traffic」会先被听成航班；l53「went to」听不出转移的是什么；l60「this network」指代松散。两人都漏了 l67「The secretary」：前文点过两位部长，离得最近的是 Mullin，见补充问题。
- V4 2 理由：取 a。整体句子短，确实有冗余，但都是小问题：l22「new equipment and new technology」、l61 重复 l60、l33 的出处句。b 用来定 1 分的 l40「Might.」是故意的口语强调，给事实留余地，不是填充词，已驳回。剩下的不构成必改。
- V5 2 理由：取 a。b 的三条证据全靠材料里的时长（l01 3.5s、l32 2.3s、l75 3.1s），而这些时长是估算值，l75 的 3.1s 明显是按「11,389」算作一个词估出来的。所以「挤进 3.1 秒」不能当成成片里的节奏问题，数字太密的问题已经计入 V3。a 的证据站得住：l27–l35 一直是「日期、事实、数字」的循环，有点单调；l56–l58 连用三个「地名，日期：」开头；l51 偏长。叙述者声音前后一致，属于小瑕疵。
- V6 2 理由：抽查不给 3 分。a 在逐句复述里判 off 的 l03、l06、l15、l27、l34、l49、l53、l56、l57、l58 在问题表里没有直接可替换的改写；l74 的改写（15 词）比原句（14 词）长。b 每条都给了改写，但有几条比原句差：l80 删掉了观点标记「We think」（讲稿规定观点句对应 C42–C44，要配「Our take」标）；l10 去掉了屏上「The same trap」和 l39、l82 都要回收的「trap」；l24 删掉了「不依赖这次原因」这层关键限定；l71 和 l83 两条改写几乎一字不差，结尾变成原样重复。两人都没发现这个撞车。

## 补充问题
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l67 | V3 | 必改 | The secretary said the new gear held and the old gear broke. | 前文点过两位部长：l16 Duffy（运输部），l22 Mullin（国土安全部）。耳朵记住的最近一位是 Mullin，而 Mullin 的说法正好相反（新设备压垮旧系统）。听众会把这个立场安错到人头上，归属一旦听错就和讲稿事实矛盾。 | Duffy said the new gear held and the old gear broke. |
| l77 | V2, V3 | 必改 | We'd argue it's safety design doing its job. | 结尾（严格项）的核心比喻「刹车」只出现在静音章卡「A ground stop is a brake」上，嘴上从来没说过。l80 突然冒出「braking」，只靠耳朵听的观众接不上。b 的 l77 改写碰巧补上了这个词，但两人都没指出这是根因。 | We'd argue it's a brake, doing its job. |
| l58 | V2, V3 | 建议 | Los Angeles, two thousand four: the FAA says a required routine restart never happened. | 前两句是 2025、2026，这里直接跳回 2004，中间没有任何提示。而且这是全片第二个洛杉矶案例（l29 是 2009 年那次），听众容易把两件事混成一件。「required routine restart」也是一串形容词叠在一起。 | Back in two thousand four, LA skipped a required restart, the FAA says. |
| l68 | V1, V2 | 建议 | So the lesson is too little money, too slow. Pay up and replace it. | 「lesson」紧跟在 l62「a second lesson」之后又出现，听起来像旁白自己的第二个结论，而这里其实是批评者的观点。b 只指出了归属松，没发现两个「lesson」撞在一起。 | Their answer: too little money, too slow. Pay up and replace it. |
| l51 | V3, V5 | 记录 | "We're pulling copper up and putting fiber down, but it's the same data architecture that we've had for 50 years." | 全片旁白的「we」都指本频道（「we think」「our take」）。这句引语里的「We're」指 FAA，引号听不出来，只靠 l50「said this:」区分。讲稿要求原话照录（C28），所以不改词，配音时要用停顿或语气标出这是引语。 | （不改词；配音在 l50 后加停顿，引语换语气） |
| l83 | V4 | 记录 | So when you replace it, treat the replacing as the riskiest part. | 「the replacing」应该改（b 说得对）。但改的时候不能照 l71 的写法改成同一句：两位审稿人给 l71 和 l83 的改写几乎一样，结尾就成了原样重复。最后一句应该接着 l82 往前推一步。 | So when you replace it, guard the switchover most of all. |
| l62 / 屏 s4 | V2 | 记录 | But we think these cases teach a second lesson. | 这句按两人意见改掉「second」之后，s4 屏上的「A second lesson」卡（`scenes/web/s4.html` #lesson）也要一起改，否则画面和旁白对不上。画面另项审，这里只提醒同步。 | （改句后同步 s4 #lesson 文案） |

## 驳回
- b l40（V4/V5 必改）：「This time might be the same. Might.」里单独一个「Might.」是讲解视频常用的口语强调，用来突出「原因还没公开」，和 l21、l23 的限定互相呼应。b 自己的整体观察里也说要保留 l40 的谨慎。改写去掉这个强调，反而变平了。
- b l66（V2 必改）：「Critics would say:」是自然的转述对方观点的说法，本章章卡就是「The strongest pushback」。b 的改写让质疑听起来像旁白自己在问，l67–l69 的反方立场也就失去了引出它的那一句。
- b l76（V2 必改）：「One last angle.」只是一句口语提示，不是念目录。改写丢掉了「looks like the system falling apart」这个铺垫，而 l77 正是要反驳它。
- b l82（必改及改写）：这句是 l10「the same trap」的回收，也是全片最该记住的一句，a 也认为该保留。改写「changing it brings risks of its own」太泛，没有力量。至于和第 4 章「不总是改动」之间的逻辑张力，属于内容审稿的范围。如果那边要求收一收，最小改法是「the danger isn't just that it's old」，不要整句重写。
- b l80 改写：问题成立（「the accident」没有所指），但改写删掉了「We think」，观点句就没了标记。应改为：We think braking feels like failure because you can see what it costs.
- b l10（必改）：冷开场的钩子本来就是先抛悬念，屏上的「The same trap」和 l39、l82 都会回收它。改写「We see one problem behind both.」没了钩子，还和画面文字对不上。
- b l11（必改）：l08「So why?」是嘴上说出来的问题，l11 跟着回答，听得懂。这句是全片最有力的一句（a 列为必须保留），改写把它拆散了。
- b l24 改写：问题成立（严格项，「what follows」是播报腔），但改写「earlier failures can help explain the risk」删掉了「论点不依赖这次的原因」这层事实限定。应改为：But whatever caused this one, the history points the same way.
- b l64（建议）：「same network, same contractor」照应 l56「承包商没检查备份」和 F-T-I/L3 Harris，说的是共因失效，不只是同一条沟。原句是自然的口语反问，改写把论点说窄了。
- b l52（必改）：「overlap」在 l43–l44 已经铺好，l72 还会回收。改成「transition drags on」就断了这条线。原句可以保留。
- b l46（建议）：「nobody dares touch it」是自然的口语夸张，还为 l82「when you touch it」埋了伏笔，不该削弱。
- b l08（必改）：「sound like opposites」里的「sound like」已经留了余地，两个说法也确实被摆成了对立两方。删掉这层张力，l10 的「same trap」就失去了反转。
- a l14 改写：l11 已经说过「A telecom network」，再加「the FAA's telecom network」是重复。靠耳朵听不需要展开 F-T-I 的全称。
- a l35 改写：「nearly 500 delays, nearly 500 cancellations」念出来是同一个词组重复两遍，而且把 476 说成「nearly 500」偏松。建议改成：A new feature filled up the memory. Almost five hundred delays, and nearly as many cancellations.
- a l33（「or cut」选项）：出处句是事实留痕要求的一部分，可以并进前句，但不能删。
