# native_ear（母语听感）双审对比

- a 位：claude-sonnet-5-5/native_ear__a（claude-sonnet-5-5）报告 `reports/native_ear__a.md`
- b 位：gpt-6-astra/native_ear__b（gpt-6-astra）报告 `reports/native_ear__b.md`
- 状态：完成；裁决人 claude-opus-5-5/native_ear__judge，报告 `reports/native_ear__judge.md`

## 评分对比

| 维度 | a 分 | a 证据 | b 分 | b 证据 | 需裁决 | 最终 | 裁决理由 |
|---|---|---|---|---|---|---|---|
| N1 自然度 | 2 | lines.md 共 4 句台词（s1_st1 / st2 / st4 / st3）。st1、st2 基本自然，st4 "That's garum. …Eventually." 很怪，st3 有点怪（讲解腔）。 | 2 | lines.md 第 8、11、14、17 行共 12 个句子／独立话语单位，10 个自然，2 个「Mission」句有轻微念提纲感；无「很怪」。逐句表列全。 | 抽查 | 2 | 逐句复核 lines.md 第 8、11、14、17 行共 12 个话语单位，没有「很怪」的句子；a 把 s1_st4 判「很怪」过严（理由同 N2①）。小瑕疵：第 11 行双 Mission 略像念任务卡，第 17 行略偏导游腔。s1_st1「Almost two thousand years back.」是惊讶时的口语补充，自然。两位共同的盲点未发现：「twelve years ago」按 Tacitus 记的 AD 63 正好 12 年（按 Seneca 的 AD 62 是 13 年），两种算法都说得过去，不用改。 |
| N2 别扭原因 | 1 | s1_st4 指代不清（指着鱼说 "That's garum"）；s1_st3 讲解腔（"They had a huge earthquake…"）；s1_st2 "Mission one/two" 电报式罗列加 "75 AD" 写法（见问题表）。 | 2 | 第 11 行连续「Mission one / Mission two」略显预先编排；第 8 行碎句有惊讶语境，第 17 行 had / ago 与 AD 75 当下视角相容，未发现明确直译或时态错误。 | 分歧 | 2 | a 位三条证据都站不住「有问题」。①s1_st4 lines.md 第 14 行「That's garum. …Eventually.」是英语常见的「先断言、再自我修正」干笑点，that 指第 13 行写明的满筐小鳀鱼，指代清楚，不是指代不清；②「75 AD」在美式口语里很常见（故事稿第 1 行标题同样写 75 AD），「AD 75」只是书面规范，不算别扭；③「Mission one / Mission two」是故事稿第 5 行 v2.1 ⑦ 按上一轮双盲审有意改成的挑战型 vlog 编号，属风格选择。剩下的小瑕疵是 s1_st3 第 17 行两句偏解说，但第 16 行写明她刚看了新补的裂缝、说完眨眼，解说有画面动机，按 2 分「小瑕疵」计；时态 had / ago 以 AD 75 为当下，正确。 |
| N3 笑点与回收 | 1 | s1_st4 "…Eventually." 笑点被压缩，母语观众接不住；开场目标 "find a bed before dark / try garum"（st2）在 s1 内只有 garum 在 st4 被碰，床没有回收，dextram 在 s1 台词里没出现，无法核对。 | 0 | 第 11→14 行的 garum 铺垫与 Eventually 笑点已查，但唯一材料第 17 行即结束；没有目标结尾或 dextram，无法核实该维度要求的完整回收。证据：lines.md 第 1–17 行范围，见问题表 NE-03。 | 一致 | 0 |  |
| N4 人设口吻 | 2 | st1、st2 是年轻 vlogger 口吻（"Okay… I just time-traveled"、"Good morning from Pompeii!"）；st3 的 "They had a huge earthquake twelve years ago. They're still fixing the damage." 变成导游腔，口吻略掉。 | 2 | 第 8 行 Okay、第 11 行预算揭示、第 14 行悄悄话式 Eventually 连起来像亲切旅行博主；第 11 行双 Mission 稍显主持提纲，其余口吻一致。 | 抽查 | 2 | 第 8 行 Okay…、第 11 行 Good morning from Pompeii! 与 my budget… is this 的摊钱揭示、第 14 行悄悄话式 Eventually，都是二十多岁亲切旅行博主的口吻，前后一致；第 17 行内容偏解说，但第 16 行规定悄悄话＋说完笑着眨眼，口吻没掉。小瑕疵同 N1，2 分。 |
| N5 改写 | 2 | 问题表里每句 "有点怪 / 很怪" 都给了不更长的改写，词数不超过原句（st4 原 11 词，改后 10 词；st3 原 14 词，改后 13 词）。 | 3 | 两句「有点怪」均给改写，逐句词数分别由 7→6、11→10；s1_st2 全段按读出的词计由 33→31，最少发声时间为 31÷2.8≈11.08 秒。 | 一致 | 2 |  |
| N6 最别扭的 5 句 | 3 | 下方「最别扭的 5 句」已按顺序列出 5 项，且每项带改写。 | 3 | 「最别扭的 5 句」按相对风险排序列出 s1_st2 两个 Mission 句、日期句、s1_st3 地震句、s1_st1 年代碎句；后三句明确标自然，不为凑五条虚构错误。 | 一致 | 3 |  |

## 问题表（两位审稿人与裁决人的并集，去掉完全相同的行）

| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 | 来自 |
|---|---|---|---|---|---|---|---|
| s1_st4 | 18s | N2 / N3 指代不清、笑点没落地 | 可剪 | ① 故事 | lines.md 第 14 行 "That's garum. …Eventually." | 便宜：改成 "See those tiny fish? Future garum." 或 "Those become garum. Eventually." | a |
| s1_st3 | 14s | N2 / N4 讲解腔 | 记录 | ① 故事 | lines.md 第 17 行，两句平铺直叙像旁白，没有旅行博主的反应 | 便宜：改成 "Huge earthquake here, twelve years ago. They're still patching it up." | a |
| s1_st2 | 19s | N2 电报式罗列 / 日期写法 | 记录 | ① 故事 | lines.md 第 11 行 "It's May, 75 AD" | 便宜：改成 "May, AD 75"，目标句去掉 "find / try" 动词也可 | a |
| s1_st1 | 12s | N1 小瑕疵 | 记录 | ① 故事 | lines.md 第 8 行 "years back" | 便宜：改成 "Almost two thousand years." | a |
| s1_st2 | 原条 19 秒；未给台词起止点 | N1／N2／N4 · NE-01 提纲腔 | 记录 | ① 故事 | lines.md 第 11 行「Mission one: find a bed before dark.」随后又「Mission two」；连续编号使刚到现场的兴奋稍像预录开场，但也是成立的 vlog 风格。 | 便宜：可改为「Today: find a bed before dark.」7→6 词；保留找床和天黑前的目标。 | b |
| s1_st2 | 原条 19 秒；未给台词起止点 | N1／N2／N4 · NE-02 重复编号 | 记录 | ① 故事 | lines.md 第 11 行「Mission two: try garum — the sauce this whole town's famous for.」；接前句形成第二次任务播报，问题在节奏而非语法或生僻词。 | 便宜：与 NE-01 成对改为「Then try garum — the sauce this whole town's famous for.」11→10 词；保留 garum 和解释，供下一镜回收。 | b |
| s1（全集回收） | 不适用 | N3 · 材料范围 | 记录 | 规则源（lines.md 只收 s1） | 故事稿第 113–115 行「Dextram!」回收、第 133 行「Mission two: done. Now… a bed.」、第 157 行「Bed? Found. Garum? Tasted. Budget? …Gone.」说明回收写在后面场次，a 位「床没有回收」是材料不全造成的误判 | 便宜：lines.md 改成真正的全集台词，或在任务书里把 N3 限定为 s1 内的铺垫 | judge |
| s1_st3 | 14s | N3 史实存疑 | 存疑 | ① 故事 | 地震常见年份 AD 62 / 63，到 AD 75 是 12–13 年；盲审无法确认作者取的年份 | 便宜：核对 spec / 人物卡；若取 62，改为 "thirteen years ago" | a |
| s1；结尾位置未提供 | 不适用 | N3 · NE-03 回收材料缺失 | 存疑 | 规则源（本审稿项的材料范围） | lines.md 第 11 行提出找床、尝 garum；第 14 行仅有鱼／garum 的即时呼应；第 17 行结束，全表无 dextram 或结尾。不能据此断言成片漏回收。 | 便宜：若仍要求 N3 全项评分，由派单方补充允许盲读的相关台词及一句画面说明；否则把该项限定为 s1 内铺垫。当前不补写剧情、不判完整回收通过。 | b |
