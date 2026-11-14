你是裁决人 **screen_zh__judge**（claude-opus-5-5），裁「中文屏幕文字（PPT 式画面）」这一项两位审稿人的分歧，并抽查两人都判通过的维度。

## 材料
- a 位报告：`edu_videos/ai_terms/t00_what_is_ai/reviews/lines_r1/reports/screen_zh__a.md`；b 位报告：`edu_videos/ai_terms/t00_what_is_ai/reviews/lines_r1/reports/screen_zh__b.md`
- 被审材料：`edu_videos/ai_terms/t00_what_is_ai/reviews/lines_r1/materials/screen_zh.md`，截图 `edu_videos/ai_terms/t00_what_is_ai/reviews/lines_r1/materials/screen/zh/`
- 你可以另读讲稿 `edu_videos/ai_terms/t00_what_is_ai/script.md` 与场景源文件 `edu_videos/ai_terms/t00_what_is_ai/scenes/web/` 核对。
- 本项标准：`edu_videos/ai_terms/t00_what_is_ai/reviews/lines_r1/items/screen_zh__a.md`（评分维度、硬上限、示例）。

## 要裁的维度
- **P3**（分歧）a 2 分（章节卡 03 + 五点进度条清楚；「01 · 规则写不完」「05 · 用的时候记住三点」与章名一致；l49 三张卡「第一/第二/第三」靠明暗分层，一眼先看第三张，层级好。瑕疵：s3、s4、s7 的 eyebrow（「打个比方」「一圈套一圈」）不带章号，其余带；l34–l37 的「最外圈：AI（人工智能）」与大 h2 并存，三级之外还有图内文字，第一眼不明确。）；b 1 分（l35–l37 保留上一层定义再叠新说明；l48–l49 三张卡的旧解释持续可读，主次被累计文字冲淡。）
- **P4**（抽查）a 2 分（章节标题「规则写不完」「做个小实验」「换个角度看」「一个真实的例子」「用的时候记住三点」读着都顺，没有「现实里的祸」那类生造词。瑕疵：l12「大多是从例子里学来的。这些例子，就叫 数据」句中带句号；l41「“women's” → 扣分」、l44「“92% 是 4”」用弯引号，全片其余用「」；l28 eyebrow「我们这个模型报出的把握」是口语句子，不是标签；l11、l35、l36 中英并列注释（model、deep learning · neural network）。）；b 2 分（「规则写不完」「做个小实验」「用的时候记住三点」自然顺口；局部仍有「92% 是4」这样的省略生硬写法及说明句句号。）
- **P6**（抽查）a 3 分（本报告问题表对每处超限都给了可直接替换的短写法。）；b 3 分（下表对l01长正文、l20整句、l35圈图及l49累计超限等，均给出短句替换或可执行的整屏替换方案。）

## 规则
- 从严条目（每一轮都一样，不因为是最后一轮放宽）：开场、串场（本期要讲什么、章节过渡）、片尾这几类句子，以及屏幕上的章节标题，只要判「有点怪」就算必改。
- 分歧维度：回到材料本身核两人的证据，谁站得住；抽查维度：专找两个模型**共同**漏掉的问题，不因两人都给高分就放过。
- 两人的问题表里，你认为不成立或改写反而更差的条目，在「## 驳回」里列出位置和理由。
- 只读，不改被审材料。

## 输出（写到 `edu_videos/ai_terms/t00_what_is_ai/reviews/lines_r1/reports/screen_zh__judge.md`）
1. `## 裁决`：每个要裁的维度一行 `- <编号> <0–3> 理由：…`（理由至少 8 字，引用句号或屏号）。
2. `## 补充问题`（两人都漏的，可空）：同审稿报告的表头 `| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |`。
3. `## 驳回`：`- <位置>：<理由>`（可空）。
然后只回复 150 字以内的摘要。
