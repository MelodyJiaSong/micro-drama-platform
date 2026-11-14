# dialogue 审稿报告 · ep01 s2–s8 · 出片前第 1 轮

审稿人：claude-opus-5-5/dialogue。范围：s2、s3、s4、s8、s5、s6、s7（按播放顺序）。
材料：`materials/lines.md`、各镜 `materials/shots/*/spec.md`（节拍、台词区间）、`episodes/ep01/scenes/*/shots/st*/资料包/prompt.txt`（台词行、口型行、参考清单）、`episodes/ep01/story.md` 第 21、55–151 行。
出片前没有本版成片，「识别结果与台词不一致」一项不适用。旁证：用 faster-whisper 转写了几条 11-06/11-07 的旧版成片（台词和现在的稿子不完全一样，没有喂剧本给模型）。英文用 medium.en，拉丁语用 medium、language=la。结果在 `work/dialogue/asr_old_renders_en.txt`、`work/dialogue/asr_old_renders_la.txt`。

## 必查项
- D1 ✓ 所有台词都是自然的美式 vlog 口语，没有书面腔。可选改写见「逐句」；这一项没有必须改的。s3_st4 那一句的问题是逻辑问题，归在 D4。
- D2 ✗ s6_st3 第二句「This is what's left of the budget… and still no bed.」11 个词只给了 3.5 秒（6.5–10.0），约 3.1 词/秒，中间还有省略号要停顿，超过了上限。其余各镜开口前都留了 ≥1 秒，说完后都留了 ≥1.5 秒（s2_st2 正好 1.5 秒）。另有 4 镜贴着上限或和语气打架，见表。
- D3 ✗ 拉丁语都核过了：语法、时代口吻都对，大多数出自庞贝铭文或 Petronius 原句，注音也都写进了 prompt。问题有三个：①「Garum?」在 s1 的 prompt 里注了「GAH-rum，重音在前」，s3_st4、s5_st13 的 prompt 里没注，旧 s3_st4 成片被转写成「Goram」；② s8_st6 说拉丁语的妇女在 prompt 里没有外貌描述，也没有声音参考；③ 几处元音长短注得不准（ito、dum）。
- D4 ✗ s3_st4 的指路逻辑前后打架：她嘴上说的是「Straight down this street, then… left」，s3_st8 却一出门脸就朝自己的左边（画右）拐了，正好和她刚目送的 Felix 的下巴方向（画左）相反；「dextram 听着像 left」也没给理由。其余回收都对得上：Mission one/two（story 第 21 行）对 s5_st7、s6_st3、s7_st1；钱数 7+1+1 → s3 付 2 → s8 付 quadrans → s5 付 2 → s6 付 3+1，和每句台词一致；s4_st2/st5 的「Smell anything? … Nope」；s5_st9 回收 dextram。
- D5 ✗（存疑）说话人在文字上都标对了，口型行也写了「其他人不开口」。但有三处的声音来源靠不住：s6_st3 画外 Fortunata 没挂 `c5_Fortunata_audio`；s8_st6 说话的妇女没有任何描述和声音参考；s5_st8 的店主也没有声音描述。这三镜都只挂了 Riley 的声音参考。

## 问题表

| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |
|---|---|---|---|---|---|---|
| s3_st4 → s3_st8 | st4 8.2–14.2 秒；st8 6–9 秒 | 台词逻辑·前后说法 | 记录 | ① 故事 | story.md 第 67–69 行和 spec 都是这样写的：Felix 说「Hac recta platea… ito ad dextram」（先沿这条街直走，再右拐），下巴朝画左扬（5.5–7 秒，她看着他扬下巴停了 1 秒）；她复述「Straight down this street, then… "dextram." That sounds like left.」，按这个意思应该先朝画左直走、再左拐，可 st8 6–9 秒她一出门脸就朝画右走。看得仔细的观众会觉得她连自己的话都没照着做，而不是「猜错一个词」。另外 dexter / dexterity 的意思是「右」，美国观众多半知道，「sounds like left」没有理由，听着像编剧硬让她错。 | 便宜：去掉「直走」那一步，让她把错猜成一次随手乱猜，例如 st4 改成「Okay… "dextram." No clue. Sounds like left? I'm going left.」（11 词，6 秒内 1.8 词/秒）；Felix 的下巴改成朝门外的街扬一下，不偏左右，这样她走画右就只错在「右」这个词上。如果要保留「观众比她先知道」，就在 st6 Felix 的目光朝画左看、再摇头，信息就在他身上。 |
| s6_st3 | 6.5–10.0 秒 | 说得完·语速 | 记录 | ② 分镜文字 | 「This is what's left of the budget… and still no bed.」11 词 / 3.5 秒 ≈ 3.1 词/秒，超过 2.8；同一窗口里还要摊开手、「停住让人数清」4 枚钱，语气又是「有点累、自嘲」。旧版 s6 g1 成片说的是更短的「Sun's going down, I've got this, and no bed.」，9 个词用了 3.06 秒（3.42–6.48），这个模型本来就偏快，加长以后多半会说赶，不会是从容的自嘲。 | 便宜，二选一：①改台词：「This is what's left… and still no bed.」（8 词，2.3 词/秒）；②改节拍：6.4–10.6 秒说第二句，10.6–11.5 秒攥手叹气，11.5–13 秒画外吆喝，13–15 秒出画。 |
| s6_st3 | 11–12.5 秒 | 说话人·画外声 | 存疑 | ③ prompt | 台词行有「画外 Fortunata … Hospitium hic locatur!」，可参考清单只有 `c1_Riley_audio`，没有 `c5_Fortunata_audio`；口型行是通用的「画内说话的人嘴型与台词同步」。两个风险：这句的声音和 s6_st1 1.5–3.0 秒 Fortunata 本人喊的同一句对不上（观众连着听两遍，一听就知道不是同一个人）；画内只有 Riley，模型可能让她跟着张嘴。旧 s6 g1 成片 9.60–11.54 秒，拉丁语模型把这句转写成「Hospitalium in locatit」（英文模型转成「Hospitilium hin locatit」），说明模型旧版就把 hic、locatur 念走了样，而那一版画外吆喝同样没有挂 Fortunata 的声音参考。 | 便宜：出片时这一镜不让模型生成画外吆喝（prompt 改成「11 秒起画外传来女人的吆喝，本镜不生成人声」），剪辑时把 s6_st1 的那句贴进来，两句就是同一个声音；或者至少挂上 `c5_Fortunata_audio`，口型行改成「画外声，画内无人张嘴」。 |
| s8_st6 | 5.1–8.8 秒 | 说话人·声音／外语 | 存疑 | ③ prompt | 本镜唯一一句拉丁语由「妇女」说，可 prompt 的「人物」段只有主持人，没有她的外貌（四十多岁、圆脸、米白浴袍，只写在 s8_st5 的画面行里），也没有声音描述，参考里只有 `c1_Riley_audio`。模型可能用 Riley 的音色说这句拉丁语，或者画错人张嘴。旁证：旧 s8 g2 成片用拉丁语模型转写，「I could stay here all day.」（11.70–13.66 秒）和 Riley 的下一句（14.50 秒起）之间只隔 0.84 秒，没有转出任何拉丁语，那一版妇女这句很可能根本没生成。 | 便宜：在 s8_st6（以及 st9）的「人物」段补上妇女：外貌同 st5，加一句「声音：中年女声，略低、带笑，语速从容」；口型行写明「拉丁语那句只有画右的妇女张嘴」。 |
| s3_st4、s5_st13 | st4 1.1–1.7 秒；st13 7.6–8.2 秒 | 专名·注音 | 记录 | ③ prompt | 「Garum?」在 s1_st2、s1_st4 的 prompt 里注了「GAH-rum，重音在前」（只有这两个 prompt 里有 GAH-rum）；s3_st4、s5_st13 的台词行只写了「Riley（问）：Garum?」，连「美式英语」都没写。旧 s3_st4 成片 1.18–1.98 秒被转写成「Goram?」。全集要回收这个词，读音应该前后一致。 | 便宜：两处都补「Garum（GAH-rum，重音在前，问句上扬）」。 |
| s5_st8 | 1.6–2.6 秒 | 说话人·声音 | 存疑 | ③ prompt | 喊「Dextram, dextram!」的店主是不立卡的配角，没有声音描述，参考里只有 `c1_Riley_audio`。Riley 背对镜头，口型上不会穿帮，但模型可能用女声，或用 Riley 的音色喊出来。 | 便宜：人物段补一句「店主：中年男声，粗嗓，隔着街口大喊」。 |
| 全部有台词的镜（规则源：prompt 编译模板） | — | 说得完·语速提示冲突 | 记录 | 规则源 | 每个 prompt 的口型行都是同一句「正常语速与口型」，可台词括号里写了 s4_st4「说得慢一点」、s7_st2「两个人名放慢」、s3_st4 Felix「飞快」、s8_st6「懒洋洋」。两条指令互相抵消，模型多半按「正常语速」来。 | 便宜：口型行改成「语速按台词括号里写的来；没写的按正常语速」。 |
| s8_st6 | 1.6–3.8 秒 | 说得完·语气 | 记录 | ② 分镜文字 | 「I could stay here all day.」6 词 / 2.2 秒 ≈ 2.7 词/秒，没超限，但写的是「懒洋洋地说」，懒洋洋的语速大约 2 词/秒，需要 3 秒左右。旧 s8 g2 成片这句只用了 1.5 秒（12.20–13.70），说得很快，没有懒洋洋的感觉。 | 便宜：窗口放宽到 1.6–4.4 秒，妇女耸肩挪到 4.4–5.1 秒（拉丁语仍从 5.1 秒开始）。 |
| s4_st4 | 5.7–10.8 秒 | 说得完·语气 | 记录 | ② 分镜文字 | 13 词 / 5.1 秒 ≈ 2.55 词/秒，中间还有省略号要停，可节拍要求「说得慢一点、小声、又累」。旧版成片 4.88–9.86 秒说的是 11 个词的版本，用了约 5 秒。 | 便宜：「I'm totally lost」改成「I'm lost」（12 词），或窗口放宽到 5.6–11.6 秒，耸肩挪到 11.6–14 秒。 |
| s7_st1 | 2.3–3.3 / 3.7–4.7 / 5.1–6.3 秒 | 说得完·停顿 | 记录 | ② 分镜文字 | 每一对「问句＋停半拍＋答」只给了 1.0–1.2 秒；「Budget? …Gone.」还多一个省略号，1.2 秒放不下「两个词＋半拍停顿＋耸肩」。说完后留了 2.7 秒，时间是够的。 | 便宜：改成 2.3–3.6 / 4.0–5.3 / 5.7–7.2 秒，转头挪到 7.2–9 秒。 |
| s3_st1 | 1.6–2.2 / 2.8–3.6 秒 | 外语·发音对比 | 存疑 | ④ 模型随机 | 同一个词「Salve」，在一镜里要读出两种音（Felix 读 SAHL-weh，Riley 按英文念成 Sal-VAY）。音频模型常常把同一个词读成一样的音；要是 Riley 也读对了，或 Felix 也读成 Sal-VAY，Felix 4–5.5 秒的笑就没了由头。 | 不用改文字。出片后用 whisper medium、language=la 分别转写两段，再人耳听一遍，确认两种读音确实不同；不一样就按「模型随机」重出（要积分）。 |
| s4_st2 | 1.3–5.3 秒 | 说得完·贴上限；口语·指代 | 记录 | ② 分镜文字 | 「They wash clothes in pee. And the emperor? He taxes it.」11 词 / 4.0 秒 ≈ 2.75 词/秒，贴着上限，中间还有问句停顿和挑眉。第二段「so Dad held a coin up to his nose」里的 his 指谁不清楚（皇帝自己，还是儿子）。 | 便宜：窗口改成 1.3–5.6 秒，掏钱改到 5.6–7 秒；第二段改成「His son called it gross — so Dad shoved a coin under the kid's nose: "Smell anything?"」（15 词 / 5.8 秒 ≈ 2.6 词/秒）。 |
| s3_st4、s8_st6 | — | 外语·注音细节 | 记录 | ③ prompt | 「ito」是 ītō，第一个 i 是长音，注成「IH-toh」会读成短 i，应该是「EE-toh」；「dum」是短 u，注成「doom」会读成长 u，应该是「dum」（像英文 dumb 去掉 b，口型略圆）。hospitium、dupondium 末尾的 -um 注成「oo」，这是古典读法里鼻化的 -um，可以接受。 | 便宜：改两处注音：`EE-toh ahd DEK-strahm`、`dum WER-sahs teh`。 |

## 逐句（D1 可选改写 · D2 数字）

格式：台词 · 词数 / 窗口 / 词每秒 · 开口前 / 说完后 · 可选改写（不改也行）。
- s2_st2「No sewers on most of these streets — the street IS the drain.」12 / 1.5–6.5 秒 / 2.4；「That's what the stepping stones are for.」7 / 6.5–9.5 秒 / 2.3 · 1.5 秒 / 1.5 秒（卡在下限）· 保留。
- s2_st8「And yeah… apparently a woman in pants is a lot.」9 / 4.5–8.5 秒 / 2.3 · 4.5 秒 / 2.5 秒 · 保留，很自然。
- s3_st1 Felix「Salve!」1.6–2.2 秒；Riley「Salve!」2.8–3.6 秒 · 保留。
- s3_st2「Pre-sliced bread. Before sliced bread was even a thing.」9 / 3.6–7.4 秒 / 2.4 · 1.6 秒 / 1.6 秒 · 可选：「Pre-sliced bread. Two thousand years before sliced bread.」（少一个 bread was even a thing 的绕口）。
- s3_st3「Mm. Dense… kinda smoky. So good.」6 / 1.6–4.3 秒 / 2.2（有三处停顿，偏紧但嚼着说可以）· 2.7 秒 · 保留。
- s3_st4 Riley「Garum?」1.1–1.7 秒（开口前 1.1 秒，刚过下限）；Felix 拉丁语 6 词 / 2.3–5.2 秒，写的是「飞快」，可以；Riley 14 词 / 8.2–14.2 秒 / 2.3 · 说完后 1.8 秒 · 改写见问题表第 1 行。
- s4_st3「Left. Definitely left.」3 / 1.7–3.2 秒 · 保留，接在 s3_st4 后面是好的回音。
- s4_st1「Oh — oh no. That's pee!」5 / 2.6–4.4 秒 / 2.8（贴上限，喊出来的话可以）；「Apage!」5.7–6.2 秒；「Okay, okay — I'm going!」4 / 7.7–9.2 秒 / 2.7 · 说完后 1.8 秒 · 可选：「Oh — oh no. Is that… pee?!」（先疑后确认，更像闻到味的第一反应）。
- s4_st2 见问题表。
- s4_st5「…Nope.」2.6–3.1 秒 · 保留，回收「Smell anything?」，对应 non olet。
- s4_st4 见问题表；口语本身自然。
- s8_st1「Hear that? That's the Temple of Isis — basically Pompeii's two o'clock alarm. And at two, everybody hits the baths.」19 / 4.1–11.3 秒 / 2.6（压低声音，偏紧）· 4.1 秒 / 2.7 秒 · 可选：「Hear that? Temple of Isis — basically Pompeii's two o'clock bell. And two o'clock means… bath time.」（17 词，two 不再重复两遍，alarm 改成 bell 更贴切）。
- s8_st2「Cover charge? The smallest coin they've got.」7 / 8.6–11.3 秒 / 2.6 · 保留（quadrans 入浴费，史实对）。
- s8_st4「It's SO hot in here. And I'm fully dressed. Rookie mistake.」11 / 2.6–7.3 秒 / 2.3 · 2.7 秒 · 保留。
- s8_st9「No soap. You just oil up… and scrape it all off.」10 / 3.1–7.1 秒 / 2.5 · 2.9 秒 · 保留。
- s8_st6「I could stay here all day.」见问题表；妇女「Dies nihil est. Dum versas te, nox fit.」出自 Petronius《Satyricon》41.10（Dama 在宴席上说的口头话），尼禄时代的口语，放在公元 75 年的浴场里很贴切，语法也对；3.7 秒，从容。Riley「I'm pretty sure that means "get moving."」7 / 10.1–12.8 秒 / 2.6 · 说完后 2.2 秒 · 保留。
- s5_st1「Clean-ish. And starving. Good news? Dinner here is at three-thirty.」约 11 个口语词 / 1.6–6.3 秒 / 2.3 · 保留。
- s5_st8「Dextram, dextram!」1.6–2.6 秒 · 保留。
- s5_st9「Wait… "dextram" means right? …I went the wrong way all morning.」11 / 1.6–7.3 秒 / 1.9 · 保留，回收到位。
- s5_st2「Assibus hic bibitur!」、s5_st10「Dupondium si dederis, meliora bibes.」出自庞贝 Hedone 酒馆铭文（CIL IV 1679），原文拼作 dupundium，dupondium 也是古典写法；语法、手指数（1 as / 1 dupondius = 2 as）和 Riley 的猜测「One coin… two coins」都对得上。
- s5_st11「One coin, cheap stuff… two coins, the good stuff?」9 / 1.6–6.3 秒 / 1.9 · 保留。
- s5_st12「Ha! The OK sign works here!」6 / 3.6–5.8 秒 / 2.7 · 2.2 秒 · 保留。
- s5_st3「They water the wine down. Everybody does.」7 / 8.6–11.3 秒 / 2.6 · 保留。
- s5_st13「Garum?」/「Euge!」· Euge（好极了）是 Plautus 式的口头感叹，用在这里对 · 说完后 1.8 秒 · 保留（只补 garum 注音）。
- s5_st5「Salty… funky… and then — whoa. It's basically fish sauce. My grandma would put this on everything.」17 / 2.1–9.3 秒 / 2.4 · 保留（她是中美混血，奶奶爱用鱼露说得通）。
- s5_st7「Mission two: done. Now… a bed.」6 / 5.1–7.8 秒 · 保留。
- s6_st3 见问题表；s6_st1「Hospitium hic locatur!」出自庞贝铭文，对；s6_st2「Convenit.」（「成交」）对，KON-weh-nit 重音也对。
- s7_st4「Cozy.」· 保留，反讽到位。
- s7_st1 见问题表；口语自然。
- s7_st2「People write on every wall here.」6 / 2.2–4.8 秒；「My favorite: "Vibius Restitutus slept here alone… missing his Urbana."」10 词约 21 个音节 / 5.1–9.8 秒（人名放慢，偏紧，但旧版成片同样一句只用了 2.94 秒，4.18–7.12）；「Two thousand years later, we still read it.」8 / 10.1–13.3 秒 · 说完后 1.7 秒 · 内容对应 CIL IV 2146，忠实 · 保留。
- s7_st3「Okay. Bedtime.」/「Who knows where I'll wake up tomorrow…」/「Goodnight from Pompeii.」分段 1.3 / 2.8 / 1.4 秒，都不超过 2.5 词/秒 · 保留，钩子清楚。

## 整体观察
- 台词整体质量高：口语自然、Riley 的声音统一；拉丁语句句有出处（庞贝铭文、Petronius），这一块是全集的亮点。
- 最该在出片前改的是 s3_st4 的指路逻辑（故事层），整集的迷路线都靠它；改法只是改文字，很便宜。
- 一类反复出现的风险：说话的配角没有声音参考（s6_st3 画外、s8_st6 妇女、s5_st8 店主），而三镜都挂着 Riley 的声音参考，模型容易借她的音色。补一句声音描述，或者画外声改到后期贴，都是便宜的改法。
- 旧版成片显示这个模型说话普遍比窗口快（s8 那句 6 词 1.5 秒，s7 人名那句 8 词 2.9 秒），所以「说不完」的风险小，「说得赶、没了语气」的风险大。凡是标了「慢」「懒洋洋」的句子，要让模板的「正常语速」让位。
- 旧版成片里的拉丁语普遍念走样或被漏掉（Hospitalium in locatit、妇女那句不见了），所以注音写进 prompt 只是第一步，出片后逐句核对才是关键。
- 出片后：所有拉丁语句用 whisper medium、language=la 转写核对（s3_st1 两种 Salve 的读音、s3_st4、s4_st1、s5_st2/st10/st13、s6_st1/st2、s8_st6）；英文用 medium.en 核 garum 的重音和 s6_st3 的语速。

## 其他
- s8_st6、s8_st9 的 prompt 里妇女没有外貌描述（只有 s8_st5 写了），跨镜长相可能不连续（归 character/continuity）。
