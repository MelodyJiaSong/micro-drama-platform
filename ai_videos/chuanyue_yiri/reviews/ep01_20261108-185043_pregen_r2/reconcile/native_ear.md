# native_ear（母语听感）双审对比

- a 位：claude-sonnet-5-5/native_ear__a（claude-sonnet-5-5）报告 `reports/native_ear__a.md`
- b 位：gpt-6.1-sol/native_ear__b（gpt-6.1-sol）报告 `reports/native_ear__b.md`
- 状态：完成；裁决人 claude-opus-5-5/native_ear__judge，报告 `reports/native_ear__judge.md`

## 评分对比

| 维度 | a 分 | a 证据 | b 分 | b 证据 | 需裁决 | 最终 | 裁决理由 |
|---|---|---|---|---|---|---|---|
| N1 自然度 | 2 | lines.md 第 8、11、14、17 行共 4 句口播，st1 "Okay… I just time-traveled." 与 st4 "See those tiny fish? Future garum." 自然；st3 两句和 st2 "It's May, 75 AD" 略平。 | 2 | lines.md:8、11、14、17 共 11 个句子或口语片段逐一审读；只有第 11 行两句连续 Mission 编号略显提纲腔，其余自然，详见逐句表。 | 一致 | 2 |  |
| N2 别扭原因 | 2 | 第 17 行 st3 "They had a huge earthquake twelve years ago. They're still fixing it." 是两句平铺直叙的讲解腔；第 11 行 "Mission one / Mission two" 有提纲腔；第 8 行 "years back" 略书面。无直译病句，也无指代不清。 | 2 | lines.md:11 的 this 有第 10 行摊钱动作，:14 的 those 有第 13 行鱼筐；:17 的 ago 以公元 75 年为叙述当下成立。第 11 行重复编号只有轻微播报感，未发现硬性直译或时态错误。 | 一致 | 2 |  |
| N3 笑点与回收 | 2 | 开场目标 "find a bed before dark" 与 "try garum" 在 st4 由 "Future garum" 回收，渔夫鱼筐的画面说明接得上；本材料只有 s1，床的回收无法判断；"Future garum" 对不懂 garum 的观众稍隐晦，靠 st2 的 "the sauce" 解释撑住。 | 0 | 只能核实 lines.md:11→14 的 garum 铺垫与鱼筐笑点；材料止于 :17，没有结尾或 dextram，不能核实维度要求的完整回收。不能据此断言成片遗漏，也不能判完整回收通过。 | 分歧 | 2 | 本项范围是 s1（items/native_ear.md:3），s1 内的铺垫和笑点都成立：lines.md:11 立下找床、尝 garum、预算三个目标，lines.md:14 "See those tiny fish? Future garum." 由第 13 行的鱼筐画面接住，笑点清楚。三个目标在后文都有回收，裁决人已核实：story.md:115 "Wait… 'dextram' is right?"、story.md:133 "Mission two: done. Now… a bed."、story.md:139 "…and still no bed."、story.md:157 "Bed? Found. Garum? Tasted. Budget? …Gone."。a 位给 2 分的依据站得住；b 位给 0 分的理由（盲审材料里没有结尾）属实，但这是材料范围造成的，不是台词本身有缺陷，所以不采用 0 分。剩下的小瑕疵：lines.md:1 标题写「全集台词」，实际只收了 s1，盲审时听不到回收；previous I5 的方案「补全台词或把 N3 限定为 s1」还没落实，保留 b 位的规则源存疑行。 |
| N4 人设口吻 | 2 | st1 到 st4 的口吻是亲切的 vlog 腔（"Good morning from Pompeii!"、"my budget… is this."）；st3 转为信息陈述，反应感弱，与前三句的俏皮不完全统一。 | 2 | lines.md:8 的 Okay、:11 的 Good morning 与预算揭示、:14 的 Future garum 均符合年轻旅行博主；第 11 行连续 Mission one / Mission two 稍像准备好的节目提纲，仍是成立的 vlog 口吻。 | 一致 | 2 |  |
| N5 改写 | 2 | 下表每条 "有点怪" 都给了不更长的改写（st3 11 词改 11 词，st1 8 词改 7 词，st2 去掉重复编号）。 | 3 | 逐句表第 5、6 项涵盖全部“有点怪”句，改写分别为 7→6 词、11→10 词；其余逐句标注保留。改写保留找床、天黑前、尝 garum 及解释，不破坏第 14 行呼应。 | 抽查 | 2 | 每条判为「有点怪」的句子都有改写，而且都不更长。裁决人重新数了词：Mission one 句 7→6、Mission two 句 11→10（b 位的计数准确）；st3 原句 12 词，a 位写成「11 改 11」，实际 12→9；st1 原句 9 词，a 位写成「8 改 7」，实际 9→8。a 位计数有误，但结论「不更长」仍成立。两人都漏了一点：两份报告都建议把 "Mission one / Mission two" 改成 "Today… Then…"，可后文 story.md:133 "Mission two: done." 正是靠这个编号回收的。改写一旦采纳，这个回收就断了（见下方问题表第一行），所以只给 2 分。 |
| N6 最别扭的 5 句 | 2 | 最别扭的 5 句排序见下方「最别扭的 5 句」，均为小瑕疵，没有很怪的句子。 | 3 | 下方按相对生硬程度列出五句，均定位到 lines.md:8、11、17；前两句有轻微问题，后三句仍判自然，未为凑数虚造五个缺陷。 | 抽查 | 2 | 两份报告都列出了 5 句并排了序，每句都定位到 lines.md:8、11、14、17，也都没有为凑数虚造很怪的句子。小瑕疵有两处。一是两人都把 lines.md:11 的 Mission 编号排进前二，但从 story.md:133 看，这是有意的节目化铺垫，不该算别扭。二是 a 位把 "It's May, 75 AD." 判为有点怪，理由是 AD 应放在年份前；在美式口语里 "seventy-five A-D" 很常见，lines.md:11 也注了这个读法，b 位判自然更准确。 |

## 问题表（两位审稿人与裁决人的并集，去掉完全相同的行）

| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 | 来自 |
|---|---|---|---|---|---|---|---|
| s1_st3 | 约 7.5–12.5 秒 | N2 讲解腔（对应 I40） | 记录 | ① 故事 | 第 17 行 "They had a huge earthquake twelve years ago. They're still fixing it." 像导游词，没有博主反应；"They had" 的 They 稍空 | 便宜：改为 "Huge earthquake here, twelve years ago. Still fixing it." 或 "Big earthquake twelve years ago — they're still patching it up."（词数不增） | a |
| s1_st2 | 1.5–5.5 秒 | N1/N2 日期写法与任务编号（对应 I41、I43、I44） | 记录 | ① 故事 | 第 11 行 "It's May, 75 AD." 英语里 AD 一般写在年份前，"AD 75"；"Mission one… Mission two" 连发两次提纲 | 便宜：改为 "It's May, AD 75. Today: find a bed before dark. Then try garum — the sauce this whole town's famous for." | a |
| s1_st1 | 0–12 秒 | N1 "years back"（对应 I42） | 记录 | ① 故事 | 第 8 行 "Almost two thousand years back." 口语里可用，但前面已有 time-traveled，后面补 back 有点冗余 | 便宜：改为 "Almost two thousand years." | a |
| s1_st4 | 12.5–15.5 秒 | N3 "Future garum" 略隐晦 | 记录 | ① 故事 | 第 14 行 观众只在 st2 听过一次 garum，鱼变成 garum 的联系靠画面；不懂的观众可能没接上 | 便宜：可保留；稳妥改为 "Tiny fish. Future garum."（不更长），或保留现状 | a |
| s1_st2 | 全句 | N2 "this whole town's famous for" | 记录 | ① 故事 | 第 11 行 "the sauce this whole town's famous for" 语法对，嘴上稍长，属书面 | 便宜：改为 "the sauce this town's famous for" | a |
| s1_st2 | 19 秒镜内；句级窗口未提供 | N1 / N2 / N4 / R · I43、I44 | 记录 | ① 故事 | lines.md:11 连续 “Mission one: find a bed before dark.” / “Mission two: try garum…”；两次报编号略显提纲感，但不至于让母语者听不懂或出戏。 | **便宜**：成对改为 “Today: find a bed before dark.” 与 “Then try garum — the sauce this whole town's famous for.”；7→6、11→10 词。可保留现句作为节目化口吻，不构成重出要求。 | b |
| s1_st2 | 1.5–5.5 秒窗口之后的目标句；句级起止未提供 | N5 / N3 · I43、I44 的改写会断掉回收 | 记录 | 规则源 | 两位审稿人都建议把 lines.md:11 的 "Mission one: … Mission two: …" 改成 "Today: … Then …"；但 story.md:133 的 "Mission two: done. Now… a bed." 直接回收这个编号。盲审材料只有 s1，两人看不到这句。 | **便宜**：I43、I44 按「保留原句」关闭，不采纳改写；如果以后一定要改编号，必须同步改 story.md:133 的回收句。 | judge |
| s1；全集结尾未提供 | 无法定位；材料仅四段、共 63 秒镜长 | N3 / R · I5 部分未闭合 | 存疑 | 规则源 | lines.md:11 立找床与尝 garum 目标，:14 已改成 Future garum，:17 即结束；没有 dextram 或结尾。previous.md:32 已要求补盲审材料或缩小维度，changes.md:9 仅说明鱼句修改。 | **便宜**：将结尾与 dextram 所在对白及一句画面说明补入允许盲读的 lines.md；或明确将本次 N3 限为 s1 铺垫。补齐前保持完整回收未审，不要求补写剧情。 | b |
| s1（全集回收） | 无法定位；lines.md 只有 4 段有声镜头 | N3 · 盲审材料与维度范围不一致 | 存疑 | 规则源 | lines.md:1 标题「全集台词」，但只到第 17 行（s1_st3）；N3 维度要求核对结尾和 dextram 的回收，previous.md:32 的方案没有落实。 | **便宜**：派单工具在单场审查时，要么把全集台词附进 lines.md，要么在任务书里把 N3 写成「s1 内铺垫」。 | judge |
