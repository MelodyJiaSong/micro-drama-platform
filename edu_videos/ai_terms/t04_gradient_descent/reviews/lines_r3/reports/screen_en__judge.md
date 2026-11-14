# screen_en__judge (claude-opus-5-5), round 3 (final)

Checked: screen_en.md; screenshots s0_l04, s2_l12, s2_l14, s3_l20, s3_l22, s3_l27, s4_l31, s4_l38, s5_l43, s5_l46, card_intro, card_c_real, card_s6; timeline.en.json (card durations); tools/edu_video.py (subtitle style and wrapping) and edu_videos/_shared/design/tokens.json (`subtitle_band` 150).

## 裁决

- P1 2 理由：a stands. b's 必改 on l20–l21 ("Nudge +$0.10 → score" + "Base fare $5.00 −1.7" + "Per km $2.00 −11.2" = 11 words over the 9-word block limit) misreads the round-2 ruling. A card row of look-alike items counts as one block and is capped per item (each ≤6 words, ≤6 items), not at 9 words. A 9-word cap on the whole row would contradict the ruling, which allows up to 36. Here each knob card is 4 words. The header counts toward the words, which a included. l20 is chart 6 + knob row 11 + Score/Steps 4 = 21 words in 3 blocks, so it is legal. b also applies its own reading unevenly: the l38 outcome row "5.5 Far off / Score 2.0 Made it / 224 Off the map" is 11 words too, and b passed it. l38/l39 reaching exactly 22 and l22 at 21 are tight but within the limits, so 2 rather than 3.
- R 2 理由：a stands. b's 1 rests on three points, and none holds. (1) The "new 11-word block" under I13 is the misreading rejected above. (2) I3 "chapter-card durations absent": timeline.en.json gives c_analogy / c_experiment / c_lens / c_real 2.6s each for 2–4-word titles (≤1.6 words/s), so the gap is closed. (3) I4 subtitle clearance: still not seen in a cut frame, but the author's reason has support in the code. edu_video.py writes one-line cues only (chunks_en/wrap_en split long text into separate cues; FontSize 20, MarginV 22, "字高约 50px"). tokens.json sets subtitle_band 150, and the edu_web check flags any element whose bottom is below y=930. The lowest text, "Base fare ($)", ends at y≈925. That makes I4 a 记录 with a final-cut frame check, not an open defect. All other r2 items (I1/I2 outro, I9–I21) are confirmed fixed in the screenshots (card_s6, s2_l15, s3_l20, s4_l38, s5_l43).
- P6 2 理由：b's 3 rests mainly on its l20–l21 rewrite. That rewrite is worse than the original (see 驳回): it hides the live $5.00 / $2.00 readouts mid-experiment and drops the "+$0.10" nudge size that gives −1.7 / −11.2 their meaning. a's drop-ins (l38 "Learning rate", l27 "True minimum: 1.97", l43 "Wobbly, but close", moving the "Illustration" label at l20) are usable and same-length or shorter. Both reviewers missed l31 and l22 (补充问题), so 2.
- P4 2 理由：both reviewers passed s4_l31's title "Same start, same steps". "Same steps" literally means identical steps, which is exactly what differs across the three panels; narration l31 says "same number of steps". l22 "Step one: mostly per km" opens like a how-to list. Neither is a strict item, and the cold open, chapter cards ("Downhill, blindfolded" … "Training giant models", seen on card_c_real) and outro read naturally. So 2 rather than b's 3.

## 补充问题

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l31–l33 | P4 / P2 | 建议 | h1 "Same start, same steps" (s4_l31) | "Same steps" can be read as "identical steps", but the point is that the three paths take different steps over the same number of steps (narration: "same number of steps"). Both reviewers passed it. | "Same start, same step count" (5 words; l33 total 18→19, and the title is gone by l34) |
| l22 | P4 | 建议 | h2 "Step one: mostly per km" | "Step one:" opens like an instruction list, while the line reports what the first step did (STEPS = 1 above). | "First step: mostly per km" (same 5 words) |

## 驳回

- b · l20–l21 必改 "11-word results block exceeds the 9-word limit": under the round-2 ruling a look-alike card row is one block capped per item (each ≤6 words). Each knob card is 4 words, and the screen totals 21 words in 3 blocks, so there is no breach. b's rewrite ("Score change" header, hide $5.00 / $2.00) is worse. The live knob readouts vanish mid-experiment, and the nudge size disappears for 13.1s (l20 + l21), so "−1.7" no longer says per what. Keep "Nudge +$0.10 → score".
- b · R I13 "screen-total fixed, but a new 11-word block problem": this is the same misreading. I13 is resolved.
- b · c_analogy / c_experiment / c_lens / c_real 存疑 "hold durations missing": timeline.en.json gives 2.6s each, enough for 2–4 words. Closed.
- b · l01–l29, l38–l39, l42–l46 存疑 and a · same 存疑 "subtitle overlap cannot be judged": downgrade to 记录. Subtitles are one-line cues inside the 150px band, and the edu_web band check enforces bottom ≤ y=930, which the lowest text ("Base fare ($)" ≈925) meets. A frame check of the final cut is still owed, but no wording or layout change is needed now.
