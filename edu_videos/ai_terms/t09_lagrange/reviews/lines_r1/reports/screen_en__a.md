# screen_en__a report (round 1) — English on-screen text

Reviewer: screen_en__a (a seat, claude-sonnet-5-5). Material read: materials/screen_en.md plus screenshots s0_l02, s2_l06, s3_l17, s3_l20, s4_l28, s5_l33, s5_l39, card_c_problem, card_s6. The other screens are judged from the word and block listing only.

## 评分表

- P1 2 证据：The old prose-on-screen problem is fixed. Almost every screen is keywords or numbers (l09 "Too low / Goes over", l25 "Fence radius 1.5 → 1.6"). No title is over 6 words and no block is over 9. The one hard-limit breach is the text-block count: l20 and l21 each carry 5 blocks (title "Tuning λ", "λ 3", "Right on the fence", "Height 7.75", chart).
- P2 2 证据：The split is clean in most places: l08 "1 extra minute −$1 / 1 minute less +$1" gives the numbers and the narration gives the story. Exceptions: l23 "Uphill points / straight out of the fence" is the narration clause almost verbatim. l03 eyebrow "1788 · Lagrange" is a date the narration never says. l30 "holds you back" vs narration "pinning you down".
- P3 2 证据：Three levels throughout (eyebrow, title, point), and the 01–04 numbering matches the chapter cards and the 4 progress dots. Slips: chapter 1 "What a Lagrange multiplier is" is a clause while the other three are noun phrases. Rule/constraint/line/fence/wall/charge/price drift across screens. l10 puts the key phrase "The just-right price" in 22px eyebrow type.
- P4 1 证据：l37/l38 "Too complex costs" reads as the noun stack "complex costs", so a native viewer stumbles. l14 "No fence. A charge." puts periods on fragments. "max" is used as a verb (l07, l15, l33). The cold-open label wraps as "Do your / best". The chapter 1 title ends on a dangling "is". The l37-l39 list is not parallel.
- P5 2 证据：Most screens are well under 3 words/s (l09 5 words in 6.9s; l37 7 words in 4.6s). The tight one is l30: 14 words in 4.2s (about 3.3 w/s) while the subtitle burns in at the bottom. l17's red caption "Farther out, higher price" sits on orange contour fill and runs past the panel edge. l33's headline almost touches the cards above it (screenshot).
- P6 2 证据：Every row in the issue table has a drop-in rewrite. The score is not 3 because there are 3 hard-limit or strict-item breaches (l20, l21, cold open), so the draft still needs the rewrites.

## 问题表

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l37 / l38 (list row 2) | P4 | 必改 | "② Regularization / Too complex costs" | "Too complex costs" parses as the noun phrase "complex costs"; a native viewer has to re-read it. It is also not parallel with row 1 ("λ tunes itself"). | "Complexity costs" |
| l39 (list row 3) | P4 | 必改 | "③ Stay near the original / Drifting costs" | The left column is a verb phrase while rows 1–2 are nouns. "the original" is bare (original what?). | "③ Closeness to the original model / Drifting costs" (or shorter: "③ Original model / Drifting costs") |
| l20 | P1 | 必改 | "Tuning λ" + "λ 3" + "Right on the fence" + "Height 7.75" + chart | 5 text blocks (limit 4). "Right on the fence" is stale from l19; this line is about the height. | Drop the green h2. Keep "Tuning λ" / "λ 3" / "Height 7.75" / chart. |
| l21 | P1 | 必改 | "Tuning λ" + "λ 4" + "Hiding inside" + "Height 6.00" + chart | 5 text blocks (limit 4). 6.00 is a number the narration never says. | Merge into one readout row "λ 4 · Height 6.00" and keep "Hiding inside" |
| l02 (cold open, strict) | P4 | 必改 | "Do your / best" (wrapped) and "Never cross" | The left label wraps to two lines (screenshot). "Never cross" has no object, and the narration quotes both phrases but the screen has no quote marks. | Widen the label column. "“Do your best”" / "“Never cross it”" |
| l03 (cold open, strict) | P2 | 必改 | eyebrow "1788 · Lagrange" | The narration says "over two hundred years ago", not 1788, so the date is a claim the narration does not make. It is mild and accurate, but the strict rule says anything off is must-fix. | Either have the narration say "In 1788" or change to "Lagrange" |
| card c_problem (strict, chapter title) | P4 | 必改 | "What a Lagrange multiplier is" | The embedded clause ends on a bare "is", which sounds stilted read aloud. It is also the only non-noun chapter title and repeats the l03 title card. | "What is a Lagrange multiplier?" |
| l14 | P4 | 建议 | "No fence. A charge." | Periods on fragments; also "charge" then "price" in l16. | "No fence, just a charge" |
| l15 | P4 | 建议 | "Find: height − charge, max" | "max" is clipped and used as a verb. | "Maximize: height − charge" |
| l07 | P4 | 建议 | "1 hour a day, max" | Clipped "max". | "Max 1 hour a day" |
| l33 | P4/P5 | 建议 | "Harm ≤ the line, max help" | "max help" is not idiomatic. The headline touches the card bottoms (screenshot). Also "Harm" here but "Harmful" in the l34 formula. | "Harm ≤ line, help maximized" and add spacing below the cards |
| l30 | P5 | 建议 | title + "Big λ → Holding you back" + "λ = 0 → Not in the way" | 14 words in 4.2s; "holds you back" vs narration "pinning down"; rows not parallel (gerund vs negation). | Title "λ flags binding rules". Rows "Big λ → Binding" / "λ = 0 → Slack" (or keep plain: "Big λ → Holds you" / "λ = 0 → Doesn't") |
| l23 | P2 | 建议 | "Uphill points / straight out of the fence" | Near-verbatim copy of the narration, split over two h2 blocks. The narration says "through the fence". | One block: "Uphill ⟂ fence" or "Uphill points straight out" |
| l22 | P2 | 建议 | "Contour meets fence" | The narration says "just touches". | "Contour touches fence" |
| l13 | P4 | 建议 | "Rule: stay inside" | The object is missing. | "Rule: stay in the fence" |
| l06 | P3 | 建议 | "A little over, a little lost" + "The price λ: the Lagrange multiplier" | The big λ appears twice (tag and left), the body line is tautological, and "lost" has no object. | "Over a bit, lose a bit" + "λ = the Lagrange multiplier" |
| l04 | P4 | 建议 | "Make it the best" | Vague "it", slightly off idiom. | "As good as possible" |
| l10 | P3 | 建议 | "The just-right price" (22px eyebrow) | The key phrase is at eyebrow size beside a 240px λ. | Promote to h2 size |
| l17 | P5 | 建议 | "Farther out, higher price" | Red text on orange fill, past the panel edge. | Move into the panel's white area, or "Farther out → higher price" in dark text |
| l24 | P2 | 记录 | "How costly is the rule?" | The narration says "expensive". | "How expensive is the rule?" |
| l18 | P2 | 存疑 | readout "2.63" | The narration says "At 1.5… raise it again", but the end frame shows 2.63. If 1.5 never reads on screen, the narration number has no visual anchor. | Hold 1.5 on screen for the first half of the line |
| l31 | P2 | 记录 | source line "ICLR 2024" | The narration says "In 2023" (the exempt source line gives the venue year). | Make the narration "first posted in 2023" or the source line "Dai et al. · arXiv 2023 · ICLR 2024" |
| card s6 (outro, strict) | P4 | 建议 | "a price on a constraint, / set just right" | "set just right" is a dangling participle and the comma splits it from the lead-in. It is passable but not clean. | "a price on a constraint — set just right" |

## 整体观察

- Big improvement on the prose problem: almost every screen is keywords and numbers, and there are no narration sentences on screen.
- Terms drift across the video: constraint/rule/line/fence/wall and charge/price. Fixing the l14/l15 screen wording to "price" would make the narration-to-screen link tighter.
- The screens most in need of work are the two 5-block screens (l20, l21), the l37–l39 list (grammar and parallelism) and the cold-open label wrap.
- Strict items: the cold open (l02/l03), chapter card 1 and the outro each need small fixes. Chapter cards 2–4 and the progress dots are fine.
- Keep: (1) the l25–l28 table and formula build ("Fence radius 1.5 → 1.6", "+0.29 ≈ 3 × 0.1", "Shadow price"). (2) The l09 "Too low / Goes over / Too high / Quits" pairs. (3) The colour logic (green helpful, red harmful, orange λ) plus the "Illustration" tag on the l35–l36 chart.
