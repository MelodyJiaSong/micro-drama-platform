# dialogue 审稿报告 · ep01 s1 · 出片前第 3 轮

审稿人：claude-opus-5-5/dialogue。范围：s1 五镜（播放顺序 st1 → st2 → st4 → st3 → st5）。
材料：各镜 spec.md、`episodes/ep01/scenes/s1/shots/stN/资料包/prompt.txt`、`episodes/ep01/story.md` 第 8–36 行及后文回收句、`0_research/parts/r01_城市与一天.md` 第 78–81 行。
旁证：用 faster-whisper medium.en 转写了四条旧版成片（11-06/11-07 版，台词与现行稿接近，不喂剧本），结果在 `work/dialogue/asr_old_renders.txt`。

## 必查项
- R ✓ 上轮本代号只有一条存疑（st5 无台词却挂了人声参考 `c1_Riley_audio`）：prompt 第 5 行仍挂着，资料包里仍有 `05_音频1`，没有改；但这一条已经列入 BRIEF「已知」第 2 条交用户定，所以不进问题表。文字这边补了「这一镜不说话，也不笑出声」（spec 动作行、节拍 11–13 秒；prompt 第 2、16、20 行）。旁证：旧 st5 成片（20261107-141656，同样挂着音频1、台词为无）转写只出来「Thanks for watching!」，no_speech_prob 0.73–0.79，是 Whisper 在静音上的典型幻听，不是真的说话，说明风险不大。出片后仍用 medium.en 转写 st5 核实。附带核了上轮 changes 里本代号的其他几条：st3 说话窗口已收紧到 7.5–12.5 秒 ✓；story.md 摊钱顺序已改成说到 is this 才摊开（第 23 行）✓。
- D1 ✓ 五句都是自然的美式口语、符合 vlog 口吻，没有书面腔，不必改；可选改写见下文「逐句」。
- D2 ✓ 语速都在 2.8 词/秒以内，开口前都留了 ≥1 秒，说完后都留了 ≥1.5 秒（st3 刚好 1.5 秒，卡在下限）；逐镜数字见下文。
- D3 ✓ s1 没有外语；专名 garum 在 st2、st4 的 prompt 台词行都注了「GAH-rum，重音在前」；75 AD 在旧 st2 成片里读成「seventy-five AD」（1.94–2.58 秒），没有读错。出片后用 medium.en 核 garum 的重音。
- D4 ✓ 两个目标编号（Mission one 找床 / Mission two 尝 garum）在后文回收齐了：s6「Mission two: done. Now… a bed.」，s7「…and still no bed.」，s8「Bed? Found. Garum? Tasted. Budget? …Gone.」。st4 的「That's garum. …Eventually.」回收 st2 的目标二，播放顺序 st2 → st4 也对。「twelve years ago」按 Seneca 的 63 年说，到 75 年 5 月是 12 年，和 r01 第 80–81 行、bible 场景卡「地震后 12 年」一致。story.md 里的台词和 spec 逐字相同。
- D5 ✓ 说话的只有她一个人，st1、st2、st4、st3 说话时都已经转过来面对镜头；渔夫、工人、挑夫都写了不说话，prompt 第 18 行口型规则也写了「其他人不开口」；st5 写明了不出声。

## 问题表

| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |
|---|---|---|---|---|---|---|
| s1_st3 | 7.5–12.5 秒 | 说得完·悄悄话能不能听清 | 记录 | ② 分镜文字 | 这一句是「压低声音、像说悄悄话」，可动作行写着同时「骡蹄声在拱顶下回响」，0–2.5 秒还写了蹄声「越来越响」。拱顶下的混响会盖过气声。另外，旧 st3 成片（20261107-011606）把 13 个词压在 3.9 秒里说完（约 3.3 词/秒），模型说悄悄话时偏快，再碰上回声，就更难听清 | 便宜：节拍 7.5–12.5 秒加一句「骡子已走远，蹄声渐弱、压得很低，她的悄悄话清清楚楚」。出片后用 medium.en 转写，核对 earthquake / twelve 能不能逐词转出来 |

## 逐句（D1 可选改写 · D2 数字）

格式：台词 · 词数 / 窗口 / 词每秒 · 开口前 / 说完后 · 可选改写（不改也行）。
- st1「Okay… I just time-traveled. Almost two thousand years back.」· 9 词 / 5.5–10 秒（4.5 秒）/ 2.0 · 5.5 秒 / 2 秒 · 可选：Okay… I just time-traveled. Like… almost two thousand years.
- st2「Good morning from Pompeii! It's May, 75 AD.」· 约 10 个口语词（75 AD 读作 seventy-five A-D）/ 1.5–5.5 秒 / 2.5 · 开口前 1.5 秒 · 保留
- st2「Mission one: find a bed before dark.」· 7 / 5.5–8.5 秒 / 2.3 · 保留
- st2「Mission two: try garum — the sauce this whole town's famous for.」· 11 / 8.5–13 秒 / 2.4 · 保留
- st2「And my budget… is this.」· 5 / 13–16 秒 / 1.7（中间停半拍）· 说完后 3 秒 · 保留；整镜 33 词 / 14.5 秒 = 2.3
- st4「See those tiny fish? That's garum. …Eventually.」· 7 / 12–16.5 秒 / 1.6 · 1 秒（11–12 秒转身）/ 1.5 秒 · 保留
- st3「They had a huge earthquake twelve years ago. They're still fixing the damage.」· 13 / 7.5–12.5 秒 / 2.6 · 1 秒（6.5–7.5 秒转身）/ 1.5 秒 · 可选：This place got hit by a huge earthquake twelve years ago. They're still fixing it.（「They」指代更清楚；词数不变）
- st5：无台词

## 整体观察
- 第 3 轮，台词逐字没改，窗口和前后留白都达标；本代号上轮唯一一条存疑已交用户定，旧成片旁证也显示风险不大。
- 旧成片显示，这个模型说话普遍比窗口快（旧 st2 约 2.9 词/秒，旧 st3 约 3.3 词/秒），所以窗口宽一点不要紧，多出来的时间会落在说完后对着镜头的停顿里，不会说不完。
- 唯一要注意的是 st3：悄悄话撞上拱顶下的回声，可能听不清。改法便宜，就是在节拍里加一句文字。
- 出片后建议：五镜都用 medium.en 转写；st2、st4 核 garum 的重音在前；st5 应该什么也转不出来，「Thanks for watching」一类是幻听，看 no_speech_prob 判断。

## 其他
- story.md 场一 st3、st5 的画面描述还是旧版（第 29 行写工人「蹲在墙根」，现行是弯腰把筐扛起来；第 33 行写「秃头老汉」，现行是白发老人；第 25 行写「一筐筐」鱼，现行是一筐），属于 changes「交主会话」第 6 条，还没同步。台词本身不受影响。
