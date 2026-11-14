# dialogue 审稿报告 · ep01 s1 · 出片前第 1 轮

审稿人：claude-opus-5-5/dialogue。范围：s1（st1、st2、st4、st3、st5，按播放顺序）。
依据：各镜 `materials/shots/*/spec.md`、`episodes/ep01/scenes/s1/shots/*/资料包/prompt.txt`、`story.md` v2.1、`filming.json` / `prompts.json` / `story.json`（四处台词逐字一致）、`0_research/parts/r01_城市与一天.md` §2。
实测参考：本机 faster-whisper medium.en 重听 s1 **旧版**成片（台词与现版大体相同，用来估语速），逐词时间戳存在 `work/dialogue/whisper_old_renders.txt`。

## 必查项
- D1 ✓ 五句台词口语都自然，没有讲解腔；可选改写见下文「改写建议」，没有必须改的。
- D2 ✗ 按词数公式算全部 ≤2.8 词/秒，但用旧版实测语速核对：s1_st4 这句给 3.5 秒，旧版同一句实际说了约 4.9 秒，说完后留不到 1.5 秒；s1_st1 预计刚好卡在 1.5 秒边上。
- D3 ✗ 「garum」是拉丁借词，prompt 里没有注音（其他场的拉丁语台词都附了「发音 …」），全集 4 处 garum 的读法没有锁定；「75 AD」「Pompeii」读法旧版实测没问题。出片前阶段，还没有成片可以核发音。
- D4 ✗ 台词本身的逻辑没问题：Mission one 床 / Mission two garum，s6「Mission two: done. Now… a bed.」、s8「Bed? Found. Garum? Tasted. Budget? …Gone.」都回收上了；75 AD 离现在「almost two thousand years」（约 1951 年）对；「twelve years ago」按 Seneca 记的 63 年算是对的。只有 story.md 里摊钱动作的位置和分镜不一致，属记录。
- D5 ✓ 五镜只有 Riley 开口，说话时都面对镜头；渔夫、挑夫、脚手架工人、赶驴人都写了「不说话」；st5 写了「台词：无」「本镜没有人说话」；有台词的四镜都带口型行。

## 问题表

| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |
|---|---|---|---|---|---|---|
| s1_st4 | 设计 7–10.5（说）/ 10.5–12（收尾） | D2 说得完·时段不够 | 记录 | ② 分镜文字 | 7 词 / 3.5 秒 = 2.0 词/秒，按公式能过。但这句有问号和「…」两处停顿，又是小声说悄悄话的口气。旧版同一句（只少一个「…」）实测 See 4.46 → Eventually 9.34，共 **4.9 秒**（`work/dialogue/whisper_old_renders.txt` 第 2 行）。按这个语速从 7 秒开口，要到约 11.5–11.9 秒才说完，收尾「回头看鱼、笑」只剩 0.1–0.5 秒，达不到 ≥1.5 秒 | 便宜：二选一。① 节拍改成 6–6.5 侧脸凑近、6.5–11 说（4.5 秒）、11–12.5 回头看鱼，镜长加到 12.5–13 秒；② 镜长不变，把「See those tiny fish?」改成「Those tiny fish?」，并在 prompt 节拍里写「Eventually 最晚在第 10.5 秒说完」 |
| s1_st1 | 设计 4–8（说）/ 8–10（回望） | D2 说得完·贴着下限 | 记录 | ② 分镜文字 | 9 词 / 4 秒 = 2.25 词/秒。旧版「Okay… I just time-traveled. Almost two thousand years.」实测 3.60–7.80，共 **4.2 秒**，Okay 后面停了约 0.9 秒。现版多了一个 back，预计约 4.5 秒，从 4 秒开口要到约 8.5 秒才说完，回望只剩约 1.5 秒，刚好卡在下限 | 便宜：节拍改成 2.5–3.5 转身、3.5–8 说（4.5 秒）；或者镜长加到 10.5 秒，回望放在 8.5–10.5 |
| s1_st2、s1_st4（连带 s3、s6 的「Garum?」） | st2 8.5–13；st4 7–10.5 | D3 外语·注音没进 prompt | 记录 | ③ prompt | 两个 prompt 的台词行都只有「garum」，没有读音。而 s7 的「Convenit」「Hospitium…」在 prompts.json 里都带「发音 …」。garum 在英语里常见两种读法：GAR-um（拉丁原音）和 GAIR-um，全集出现 4 次，每次各自生成，读法可能前后不一样。旧版两次都被识别成「garum」（g1 19.84、st4 8.02），说明听得懂，但没有保证一致 | 便宜：编译器给英文台词里的拉丁借词也附注音，例如台词后加「（garum 读作 GAH-rum，重音在前，a 读 father 的 a）」，s1、s3、s6 全部统一。出片后用 medium.en 转写、人工听一遍 4 处读法是否一致 |
| s1_st2 | 13–16 | D4 故事稿与分镜的动作顺序不一致 | 记录 | ① 故事 | story.md 第 21 行把「摊开左手给镜头看」写在 Mission 那句台词（第 23 行）**前面**；分镜和 prompt 写的是说到「is this」时才摊开。按故事稿读，会以为她先亮钱、再报目标，「And my budget… is this.」就成了马后炮 | 便宜：story.md 把第 21 行挪到第 23 行之后，或者改成「说到 is this 时，她把攥着的左手摊开…」 |

## 改写建议（D1，都是可选的）
- st1「Okay… I just time-traveled. Almost two thousand years back.」可以保留。想更口语一点可以改成「Okay… I just time-traveled. Like… two thousand years back.」，词数相同。
- st2 可以保留。「It's May, 75 AD.」如果模型把 AD 读成单词 ad，可以写成「seventy-five A.D.」，不过旧版实测读对了。
- st4「See those tiny fish? That's garum. …Eventually.」笑点成立。为时长考虑可以改成「Those tiny fish? That's garum. …Eventually.」。
- st3「They had a huge earthquake twelve years ago. They're still fixing the damage.」自然。更口语的说法是「…They're still rebuilding.」，少 2 个词。

## 整体观察
- 上一轮台词偏满的问题（s1_st2 15.6 秒的话塞进 15 秒、s1_st3 塞进 3.5 秒）已经通过加长镜头和删句解决。st2 按旧版语速估约 12–13 秒，在 1.5–16 秒的窗口里放得下；st3 估约 3.8 秒，给了 5.5 秒，都有余量。
- 「≤2.8 词/秒」对带「…」、问号和小声口气的短句会算得偏宽：st4 按公式是 2.0 词/秒，实测相当于 1.4 词/秒。建议规则源对每个「…」、问号或冒号停顿另加 0.4–0.6 秒，或者按台词口气（小声 / 半喘）降到 2.0 词/秒左右。
- 出片后要做：用 medium.en 转写，核对每句开口和说完的时间、garum 的读法，以及 st1 Okay 后面的停顿有没有吃掉回望。

## 其他（不在本法则范围，各一句）
- s1_st3 的 prompt 正文要求「一只装着灰浆的木桶」，负面词里却有「木桶」（所有 s1 prompt 的负面词模板都有），两处互相矛盾。
- `materials/lines.md` 给母语听感审稿人的画面说明在约 100 字处截断，句子是半截的（如 st1「说完又忍不住」、st2「说 A」），可能误导盲审；这是审查材料生成工具的问题。
- `episodes/ep01/_filming_content.json` 里还是旧台词（「Mission one: done」「Fun fact:」「About ten thousand people…」），如果还有工具在读它，会把旧台词带回来。
- 镜头编号和播放顺序不一致（st4 第 3 个播、st3 第 4 个播），容易看错。
