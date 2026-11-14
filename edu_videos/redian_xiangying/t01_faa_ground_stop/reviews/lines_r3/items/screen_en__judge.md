你是裁决人 **screen_en__judge**（claude-opus-5-5），裁「English on-screen text (slides)」这一项两位审稿人的分歧，并抽查两人都判通过的维度。

## 材料
- a 位报告：`edu_videos/redian_xiangying/t01_faa_ground_stop/reviews/lines_r3/reports/screen_en__a.md`；b 位报告：`edu_videos/redian_xiangying/t01_faa_ground_stop/reviews/lines_r3/reports/screen_en__b.md`
- 被审材料：`edu_videos/redian_xiangying/t01_faa_ground_stop/reviews/lines_r3/materials/screen_en.md`，截图 `edu_videos/redian_xiangying/t01_faa_ground_stop/reviews/lines_r3/materials/screen/en/`
- 你可以另读讲稿 `edu_videos/redian_xiangying/t01_faa_ground_stop/script.en.md` 与场景源文件 `edu_videos/redian_xiangying/t01_faa_ground_stop/scenes/web/` 核对。
- 本项标准：`edu_videos/redian_xiangying/t01_faa_ground_stop/reviews/lines_r3/items/screen_en__a.md`（评分维度、硬上限、示例）。

## 要裁的维度
- **P1**（分歧）a 2 分（Outline-only holds across s1-s6: l19 "Old routers overloaded / New gear: none failed / Asks Congress: $50B" (12 words, 2 blocks), l32 "129 facilities / 5 hours down · 820 flights delayed" (19 words), l83 three fragments (18 words). No screen breaks ≤22 words / ≤4 blocks under the round-2 counting ru）；b 1 分（l09 “An update broke it,” c_c6 “A ground stop is a brake,” and l82–l83 retain complete sentences. The outro title now meets six words, but that does not resolve outline-only compliance. No confirmed numerical hard-limit breaches remain after checking screenshots and applying the exemptions.）
- **P2**（分歧）a 2 分（Screen carries numbers and contrasts (l06 "Canceled 4,467 / Delayed 10,079", l49 "Unsustainable 51 · Potentially unsustainable 54") while narration explains. Near-verbatim echoes remain: l15 "Communication issues at multiple centers" vs "multiple en route centers had communication issues"; l74 "No r）；b 1 分（l39 repeats each explanation in two forms; l77–l78 repeat the spoken brake metaphor as “It’s a brake”; l82–l83 turn the closing narration into written prose rather than a complementary outline.）
- **R**（分歧）a 2 分（Resolved: I3/I4/I5 advisory body now blurred, only the highlight readable (s0_l02.png, s0_l03.png); I7 l05 card no longer overflows ("PLANES IN THE AIR / 3,500+ / All landed safely", s0_l05.png); I9 badges "Counts differ" / "Wording differs" self-explanatory (s0_l07.png, s1_l15.png); I11 "Secretary ）；b 1 分（I1–I2 unresolved: package renders and hold times remain absent; separate rendering explains their absence but does not verify them. I3–I5 resolved: l02–l03 now blur the advisory body and EVENT TIME; only the selected excerpt is readable. I6 unchanged: l04 agrees with its narration and attributes reo）
- **P6**（抽查）a 2 分（No hard-limit breach requires a rewrite; drop-in rewrites for every remaining nit are in the issue table (l04, l09, l13, l22, l30/l78, l52, l83, l77).）；b 3 分（The issue table supplies shorter replacements for the cold-open sentence, brake headings, duplicated l39 labels and closing prose, plus a concrete staging change for l52.）
- **P4**（抽查）a 2 分（Sentence-case headlines, no Chinglish, curly quotes consistent, arrows used consistently ("Update → reboot → crash", "Delay → longer risky overlap"). Remaining nits: l04 "4 h 21 min" (SI style; US viewers expect "4 hr 21 min"); l83 h1 "Old is risky. Change is riskier." is the only headline with sent）；b 3 分（“Past outages” at l24, “Each time: a change in progress” at l26, and “Three exceptions” at l55 read naturally. Screenshots confirm an en dash in “150–200” and correct spacing in “Old gear broke (Duffy).”）

## 规则
- Strict items (same in every round, never relaxed in the last round): the cold open, linking lines (what's coming, chapter transitions), the outro, and on-screen chapter titles — anything 'a bit off' there is 必改 (must fix).
- 分歧维度：回到材料本身核两人的证据，谁站得住；抽查维度：专找两个模型**共同**漏掉的问题，不因两人都给高分就放过。
- 两人的问题表里，你认为不成立或改写反而更差的条目，在「## 驳回」里列出位置和理由。
- 只读，不改被审材料。

## 输出（写到 `edu_videos/redian_xiangying/t01_faa_ground_stop/reviews/lines_r3/reports/screen_en__judge.md`）
1. `## 裁决`：每个要裁的维度一行 `- <编号> <0–3> 理由：…`（理由至少 8 字，引用句号或屏号）。
2. `## 补充问题`（两人都漏的，可空）：同审稿报告的表头 `| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |`。
3. `## 驳回`：`- <位置>：<理由>`（可空）。
然后只回复 150 字以内的摘要。
