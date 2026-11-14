你是裁决人 **screen_zh__judge**（claude-opus-5-5），裁「中文屏幕文字（PPT 式画面）」这一项两位审稿人的分歧，并抽查两人都判通过的维度。

## 材料
- a 位报告：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/reports/screen_zh__a.md`；b 位报告：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/reports/screen_zh__b.md`
- 被审材料：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen_zh.md`，截图 `edu_videos/ai_terms/t13_backprop/reviews/lines_r1/materials/screen/zh/`
- 你可以另读讲稿 `edu_videos/ai_terms/t13_backprop/script.md` 与场景源文件 `edu_videos/ai_terms/t13_backprop/scenes/web/` 核对。
- 本项标准：`edu_videos/ai_terms/t13_backprop/reviews/lines_r1/items/screen_zh__a.md`（评分维度、硬上限、示例）。

## 要裁的维度
- **P2**（分歧）a 2 分（多数屏分工好（l22「责任 = 错误 × 送进来的数」只给公式，口播解释）；但 l40 的 caption「官方教程」口播没说过、还复述口播；agenda 第 04 项「从 1986 到今天」l06 口播没提；l17「神经网络也是一串齿轮」口播是「也像」。）；b 1 分（l28 已显示新旋钮值“×0.7、＋0.94”，却仍保留旧输出“6、4”和旧回传算式；outro“一趟算出每个旋钮”也未表达出口播所说的拧动方向与多少。）
- **P3**（分歧）a 2 分（层级清楚（页眉小标签 + h1 + 图）；但叫法不一：agenda「一个个试」、l10 / l11「挨个试」、l29–l34「挨个试拧」、l01 / l31「几十亿个 / 十亿个旋钮」；l09「梯度」屏上没写「坡度」，l39 / l40 却用「坡度」。agenda 第 01 项 9 字，超列表项 ≤8 字。）；b 1 分（目录与章节卡的四个名称一致；但 l28 新旧数值混放，l32—l34 又把“一遍1秒的话”这一估算条件排成与两种算法同级的行。）
- **P6**（抽查）a 2 分（问题表每处超限、不顺都给了替换写法；l26 的减负方案只能给倾向性建议，需看图再定。）；b 3 分（问题表已为 l22—l28 的超限图文、l30 对比卡、l34、l40 和 outro 提供可直接替换的文字及删留方案。）

## 规则
- 从严条目（每一轮都一样，不因为是最后一轮放宽）：开场、串场（本期要讲什么、章节过渡）、片尾这几类句子，以及屏幕上的章节标题，只要判「有点怪」就算必改。
- 分歧维度：回到材料本身核两人的证据，谁站得住；抽查维度：专找两个模型**共同**漏掉的问题，不因两人都给高分就放过。
- 两人的问题表里，你认为不成立或改写反而更差的条目，在「## 驳回」里列出位置和理由。
- 只读，不改被审材料。

## 输出（写到 `edu_videos/ai_terms/t13_backprop/reviews/lines_r1/reports/screen_zh__judge.md`）
1. `## 裁决`：每个要裁的维度一行 `- <编号> <0–3> 理由：…`（理由至少 8 字，引用句号或屏号）。
2. `## 补充问题`（两人都漏的，可空）：同审稿报告的表头 `| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |`。
3. `## 驳回`：`- <位置>：<理由>`（可空）。
然后只回复 150 字以内的摘要。
