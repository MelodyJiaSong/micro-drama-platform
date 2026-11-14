你是裁决人 **screen_en__judge**（claude-opus-5-5），裁「English on-screen text (slides)」这一项两位审稿人的分歧，并抽查两人都判通过的维度。

## 材料
- a 位报告：`edu_videos/redian_xiangying/t01_faa_ground_stop/reviews/lines_r1/reports/screen_en__a.md`；b 位报告：`edu_videos/redian_xiangying/t01_faa_ground_stop/reviews/lines_r1/reports/screen_en__b.md`
- 被审材料：`edu_videos/redian_xiangying/t01_faa_ground_stop/reviews/lines_r1/materials/screen_en.md`，截图 `edu_videos/redian_xiangying/t01_faa_ground_stop/reviews/lines_r1/materials/screen/en/`
- 你可以另读讲稿 `edu_videos/redian_xiangying/t01_faa_ground_stop/script.en.md` 与场景源文件 `edu_videos/redian_xiangying/t01_faa_ground_stop/scenes/web/` 核对。
- 本项标准：`edu_videos/redian_xiangying/t01_faa_ground_stop/reviews/lines_r1/items/screen_en__a.md`（评分维度、硬上限、示例）。

## 要裁的维度
- **P2**（分歧）a 2 分（Most screens carry numbers and contrasts ("21 → 129", "Unsustainable 51 / Potentially 54", "Money ≠ safety"). Breaches: l83 body "So treat the replacing as the riskiest part" and l82 headline repeat the narration almost word for word; l26 h1 "Each time, someone was changing it" and l51 repeat verbat）；b 1 分（l24, l26, l51 and l82–l83 reproduce the narration’s sentences instead of supplying an outline. The “Disputed” qualification at l15 is not explained in its narration.）
- **P3**（分歧）a 2 分（Hierarchy is clear (h1 big number, body label, source line at the bottom, eyebrow "03 · Why touching it is risky"). Inconsistencies: chapter 3 is titled "Why touching it is risky" on the card and eyebrow but "Why touching it is the risky part" in the section heading; chapter 4 "Not always a change" ）；b 1 分（l70–l72 retain the entire faded opposing argument alongside the response; l49 labels the second category only “Potentially 54,” leaving its meaning incomplete.）
- **P4**（分歧）a 2 分（Sentence case, curly apostrophes and arrows are consistent, with no trailing periods on fragments. Faults: l67/l68/l69 "The old gear broke(Duffy)" has no space before the bracket; l47 "Interest ontech debt" is missing a space or has a stray line break; chapter title "The worst ones" is a dangling pr）；b 1 分（“Design the switch as the riskiest phase” at l71 is awkward English; “treat the replacing” at l83 is especially unnatural in the closing takeaway.）
- **P5**（分歧）a 2 分（Fresh content per beat is small. l01, l08, l10, l23, l31, l45 and l55 are glanceable. Only dense moments: l06 (new numbers 4,467 and 10,079 in 3.8s), l19 (26 words, 2.7s, but only 3 new words) and l58 (a new 3-block card in 4.6s). l02 and l03 hold a 54-word advisory for 9.6s in total, readable only ）；b 1 分（The 54-word advisory body at l02–l03 needs approximately 18 seconds at three words per second, but these lines together last 9.6 seconds, before allowing for subtitles.）
- **P6**（抽查）a 3 分（Every breach and awkward phrase below has a drop-in rewrite.）；b 3 分（Every issue below has replacement English; the l51 replacement reduces the quotation to two contrast labels, and the l82–l83 replacement removes both oversized blocks.）

## 规则
- Strict items (same in every round, never relaxed in the last round): the cold open, linking lines (what's coming, chapter transitions), the outro, and on-screen chapter titles — anything 'a bit off' there is 必改 (must fix).
- 分歧维度：回到材料本身核两人的证据，谁站得住；抽查维度：专找两个模型**共同**漏掉的问题，不因两人都给高分就放过。
- 两人的问题表里，你认为不成立或改写反而更差的条目，在「## 驳回」里列出位置和理由。
- 只读，不改被审材料。

## 输出（写到 `edu_videos/redian_xiangying/t01_faa_ground_stop/reviews/lines_r1/reports/screen_en__judge.md`）
1. `## 裁决`：每个要裁的维度一行 `- <编号> <0–3> 理由：…`（理由至少 8 字，引用句号或屏号）。
2. `## 补充问题`（两人都漏的，可空）：同审稿报告的表头 `| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |`。
3. `## 驳回`：`- <位置>：<理由>`（可空）。
然后只回复 150 字以内的摘要。
