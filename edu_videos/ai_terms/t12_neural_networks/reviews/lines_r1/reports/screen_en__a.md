# screen_en__a — round 1 (English on-screen text)

Reviewer: a · claude-sonnet-5-5. Checked screen_en.md in full; opened screenshots s3_l24, s5_l36, s6_l41, s6_l47. The agenda, outro and chapter cards have no screenshots, so those were judged from the text only. Counts follow the round-2 ruling: a chart counts as one block, its text counts as words, tick numbers are exempt.

## 评分表
- P1 2 证据：No screen has prose or a full sentence. The longest blocks are s6_l46 "Remove a middle layer → about −2 points" (7 words) and s5_l31 "Side by side: one bend each" (6). No hard limit is broken. A few screens sit at the ceiling: l29 ≈20 words, l30 ≈21 words (chart text plus a leftover caption), l24 ≈20 words. Agenda is 4 short items, so the earlier "four narration sentences" problem is fixed. The outro pair is only a loose fragment.
- P2 2 证据：Numbers and contrasts are carried well (l27 "Best line: 11.5" vs 0.26, l35 "≤ 11" vs "32"). Problems: l36 "Later layers reuse earlier folds" is almost the narration word for word. l47's quote matches the narration quote, which is acceptable. Outro "Deep enough to see more" is not what l49 says ("recognize really complicated things"). Agenda item 04 "AlexNet, 2012" is not mentioned in l05/l06.
- P3 2 证据：There are never more than 3 levels. The chapter eyebrows (01–04) match the agenda and the c_* cards exactly. Problems: s6_l47 shows two source lines at once ("Krizhevsky et al. 2012 · §7" above "Krizhevsky et al. · NIPS 2012"). l30 keeps the stale caption "Each corner = one unit" under the new title "Which way to turn?". l13's h1 "Lines can’t bend" just repeats the eyebrow "01 · Lines can't bend". l04 says "Neural networks" (plural), l23/l24 say "Neural network".
- P4 2 证据：Sentence case is used throughout and there are no trailing periods. Problems: s5_l31 "Side by side: one bend each" and s5_l32 "Stacked: fold again" are colon-fragment headings and not parallel. s3_l21 "A knob for each" and "Plus one more → fare" are cryptic. s6_l42 "5 guesses; all wrong = a miss" mixes a semicolon and an equals sign. Agenda "Prereqs:" is jargon shorthand. The apostrophe in l13 is curly (’) and everywhere else it is straight ('). Chapter titles are mixed in form (statement / imperative / question / noun phrase) but all read naturally aloud.
- P5 3 证据：Short lines hold only little text: l22 (1.9s) is "37 / knobs / 12 × 2 + 12 + 1" plus a persistent diagram. l16 (3.1s) adds only one 5-word line on a static background. l36 (3.1s) adds 5 words. l38 (2.3s) is 5 words. Most chart screens add 1–3 words per line. The screenshots (s3_l24, s5_l36, s6_l41, s6_l47) have big type and generous spacing, so reading time is fine. The only watch point is l30 (21 words in 5.4s) and l24 (20 words in 7.7s); the stale caption on l30 is a nuisance, not a failure.
- P6 3 证据：Every row in the issue table has a drop-in rewrite.

## 问题表

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| outro | P2 | 必改 | "Simple units, stacked in layers / Deep enough to see more" | Outro is a strict item. "see more" is vague and is not the claim of l49 (recognize really complicated things). The two lines also run together without punctuation. | "Simple units, stacked in layers" / "Stack deep → recognize complex things" |
| s0 l04 | P3/P4 | 必改 | h1 "Neural networks" | Cold open (strict). Plural here but singular "Neural network" at l23/l24, the definition moment. | "Neural network" |
| agenda | P4 | 必改 | "Prereqs: Gradient descent" | Agenda is a strict item. "Prereqs" is a jargon abbreviation and reads like a syllabus. | "Builds on: gradient descent" |
| agenda | P2 | 建议 | "04 · AlexNet, 2012" | Narration l05/l06 never mentions AlexNet, so the agenda introduces a section the narration doesn't name. Fine if the narration adds it. | keep text; add "…and a famous deep network" to l06 or accept the gap |
| l30 | P3/P5 | 建议 | caption "Each corner = one unit" stays under "Which way to turn?" and "Next episode" | Stale caption from l29, about 21 words with chart text, and it distracts from the linking message (next-episode link is strict). | Remove the caption at l30. Keep "Which way to turn?" and "Next episode" |
| s6_l47 | P3 | 建议 | "Krizhevsky et al. 2012 · §7" and "Krizhevsky et al. · NIPS 2012" | Two near-identical source lines stacked. | Keep only "Krizhevsky et al. 2012 · §7" (or add § to the bottom line) |
| s3_l21 | P4/P2 | 建议 | "A knob for each" / "Plus one more → fare" | "each" has no referent on a screen where the diagram only shows units; "Plus one more → fare" is cryptic. | "One knob per unit" / "+1 knob → fare" |
| s5_l31–l32 | P4 | 建议 | "Side by side: one bend each" / "Stacked: fold again" | Colon fragments, not parallel; l31 is at the 6-word title limit. | "Side by side" with caption "1 bend each"; "Stacked" with caption "Fold again" (or "Side by side: 1 bend each" / "Stacked: refold") |
| s5_l36 | P2 | 建议 | "Later layers reuse earlier folds" | Close to a word-for-word copy of the narration. | "Reuse earlier folds" |
| s6_l42–43 | P4 | 建议 | "5 guesses; all wrong = a miss" | Semicolon and equals sign mixed into one fragment; "top-5" in the chart title is not said in the narration. | "5 guesses · all wrong = miss" or "Miss = all 5 wrong"; chart title "Top-5 error rate" |
| s0 l01 | P4 | 建议 | h2 "Learns it fine" | Chatty and slightly vague. | "Fits well" or "Learned ✓" |
| axis text, all chart screens | P1/P5 | 建议 | "Time of day (h)" (4 words) | The axis title costs 4 words per chart screen against the ≤22 cap (l29/l30 reach ~20–21). | "Hour" (1 word) |
| s2 l13 | P4/P3 | 记录 | h1 "Lines can’t bend" | Curly apostrophe here, straight apostrophe in eyebrow/agenda/chapter card; and it repeats the chapter title. | Use one apostrophe style; or change the h1 to "Straight lines only" |
| s3_l22 | P5 | 记录 | "12 × 2 + 12 + 1" | The formula is shown for 1.9s only; viewers can't parse it in time. It's a bonus, not a must-read. | Keep, or "12 × 2 + 12 + 1 = 37" |
| agenda / chapter cards | P4 | 记录 | "Lines can't bend", "Build a small network", "Why go deep?", "AlexNet, 2012" | Chapter titles are not parallel (statement, imperative, question, noun phrase). They read fine aloud, so this is a note only. | Optional parallel set: "Why lines fail" / "Build a small network" / "Why go deep?" / "AlexNet, 2012" |
| s0 l01–l03 | P1 | 记录 | all chart text | Cold open chart screens are the most word-heavy (l01 has 5 blocks per the tool's count). Under the chart rule it is one chart block + 1 h2, so it passes. | none |

## 整体观察
- No prose on any slide. Every text line is a label, a number or a ≤7-word fragment, and no hard limit is broken. The user's earlier complaint (narration sentences on the agenda) is fixed.
- Strict items are mostly good: the cold open is clean and the chapter cards match the agenda and eyebrows. The outro line "Deep enough to see more", the "Neural networks" plural at l04 and "Prereqs" are the only items that are "a bit off".
- Biggest recurring cost is the chart axis title "Time of day (h)" on every chart screen. Trimming it to "Hour" buys room on the busiest screens (l29, l30).
- Things that work and should be kept: (1) big-number slides with small unit labels (s6_l41, l22 "37 knobs", l43 "15.3%" vs "26.2%"); (2) the head-to-head contrast on s5_l35 "10 side by side: ≤ 11" vs "10 in 5 layers: 32" with colour on the numbers; (3) the quiet quote slide s6_l47, once the double source line is cut.
