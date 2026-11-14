你是裁决人 **screen_zh__judge**（claude-opus-5-5），裁「中文屏幕文字（PPT 式画面）」这一项两位审稿人的分歧，并抽查两人都判通过的维度。

## 材料
- a 位报告：`edu_videos/redian_xiangying/t01_faa_ground_stop/reviews/lines_r1/reports/screen_zh__a.md`；b 位报告：`edu_videos/redian_xiangying/t01_faa_ground_stop/reviews/lines_r1/reports/screen_zh__b.md`
- 被审材料：`edu_videos/redian_xiangying/t01_faa_ground_stop/reviews/lines_r1/materials/screen_zh.md`，截图 `edu_videos/redian_xiangying/t01_faa_ground_stop/reviews/lines_r1/materials/screen/zh/`
- 你可以另读讲稿 `edu_videos/redian_xiangying/t01_faa_ground_stop/script.md` 与场景源文件 `edu_videos/redian_xiangying/t01_faa_ground_stop/scenes/web/` 核对。
- 本项标准：`edu_videos/redian_xiangying/t01_faa_ground_stop/reviews/lines_r1/items/screen_zh__a.md`（评分维度、硬上限、示例）。

## 要裁的维度
- **P2**（分歧）a 2 分（多数屏数字与对比分工得当（l31 「21 → 129」、l49 「不可持续 51 / 可能不可持续 54」）。小瑕疵：l07 「有争议」「计数口径不一」和 l15 「有争议：「多个」还是「全部」中心」是口播没说过的新说法；l83 body 「要换，就把「换」当成最该小心的事」与口播几乎逐字重复；l82 两行大字也是口播整句。）；b 1 分（l15、l51、l82–l83把口播整句再次印上屏；l15还新增口播未交代的「多个还是全部中心」争议。）
- **P3**（分歧）a 2 分（多数屏「大字结论 + 小注出处」两级清楚，eyebrow 编号「01 · 到底坏了什么」与章节卡一致。瑕疵：s5 材料章名「反方最有力的说法」与章节卡、页眉「反方怎么说」不是同一说法；l02/l03 屏上英文大段与中文 38px 大字抢第一眼。）；b 1 分（l31–l33、l70–l72旧文字淡化后仍可读，却未计入材料清单；尤其反方整栏留屏，挤占回应的阅读空间。）
- **P4**（分歧）a 2 分（标题短语基本顺（「到底坏了什么」「停飞其实是刹车」「不是每次都这样」），无句末句号、引号用「」规范。瑕疵：l68-l69 「说有风险 → 更不敢动」读着别扭；l65 h2 「这次为什么一个故障打到全国？」13 字近整句；eyebrow 「FlightAware，当晚」半中半英。）；b 1 分（l24「接下来的内容，不靠这次的结论」串场含糊；l27「同一家 Harris」搭配生硬；l65「一个故障打到全国」不像自然的中文标题。）
- **P6**（分歧）a 3 分（下方问题表对每处超限屏都给了可直接替换的短写法（如 l15 改「多个中心通信故障」、l83 改删 body）。）；b 1 分（l15、l51、l65、l74及片尾均需实质改写，不能仅靠换行解决；下表逐处提供替换文字。）

## 规则
- 从严条目（每一轮都一样，不因为是最后一轮放宽）：开场、串场（本期要讲什么、章节过渡）、片尾这几类句子，以及屏幕上的章节标题，只要判「有点怪」就算必改。
- 分歧维度：回到材料本身核两人的证据，谁站得住；抽查维度：专找两个模型**共同**漏掉的问题，不因两人都给高分就放过。
- 两人的问题表里，你认为不成立或改写反而更差的条目，在「## 驳回」里列出位置和理由。
- 只读，不改被审材料。

## 输出（写到 `edu_videos/redian_xiangying/t01_faa_ground_stop/reviews/lines_r1/reports/screen_zh__judge.md`）
1. `## 裁决`：每个要裁的维度一行 `- <编号> <0–3> 理由：…`（理由至少 8 字，引用句号或屏号）。
2. `## 补充问题`（两人都漏的，可空）：同审稿报告的表头 `| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |`。
3. `## 驳回`：`- <位置>：<理由>`（可空）。
然后只回复 150 字以内的摘要。
