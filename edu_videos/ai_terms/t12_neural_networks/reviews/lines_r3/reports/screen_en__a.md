# screen_en__a report (round 3, a seat, claude-sonnet-5-5)

Hard-limit pass: I counted all 40+ screens with the round-2 rulings (eyebrows, source lines, tick numbers exempt; in-chart text counts; look-alike rows count as one block). No title is over 6 words (longest: l31 "Side by side: 1 bend each", exactly 6). No block is over 9 words (longest: l35 second line, 8). No screen has more than 4 blocks. The word-count peaks are l24 (about 20 words) and l36 (about 17 words plus diagrams), both under 22. No hard-limit breach found.

## 评分表

- P1 2 证据：s5_l35 "10 side by side: ≤ 11 pieces" (6) and "10 in 5 layers: up to 32 pieces" (8) are the longest blocks, and l46 "Remove a middle layer → ~2 pts worse" (7); every screen is within 9 / 4 blocks / 22 words, but these read close to narration clauses rather than labels. No full narration sentence on screen.
- P2 2 证据：l30 screen "Which way to turn? · Next episode" no longer matches the revised narration "there's a much faster way to find each one's direction", and contradicts l25 where the knobs are already nudged; outro line 1 "Simple units, stacked in layers" repeats l48 almost verbatim; l44 eyebrow "Not told what to look for" copies l44 narration.
- P3 2 证据：agenda 01–04 matches chapter cards "Beyond straight lines / Build a small network / Why go deep? / AlexNet, 2012" and the page eyebrows; l03 and l13 now both say "Straight lines only". Flaws: l36 "Earlier folds, reused" sits at the same 54px weight as the two data headings, so the hierarchy is flat; agenda side card "Prereqs: Gradient descent" is not verifiable.
- P4 2 证据：l35 mixes notations "≤ 11 pieces" and "up to 32 pieces" in the same pair; l46 still abbreviates "~2 pts worse"; l29 "Unit bends → corner" is slightly clipped. Otherwise sentence case, no trailing periods, parallel colon fragments (l31, l32), and chapter titles read naturally aloud.
- P5 3 证据：screenshots s5_l36, s6_l41, s3_l24 and s4_l30 are large, uncluttered and readable at a glance; the busiest screens (l24, l46) hold 5.4 s or more, and l22 "37 / knobs" is 1.9 s but only 2 words of text.
- P6 2 证据：rewrites below are short drop-ins, but the l30 case needs a screen redesign rather than a word swap, and the agenda/outro cards could only be checked from extracted text (screenshots empty).
- R 2 证据：Resolved: I8 (l03/l13 now the same), I12 ("Sum + 1 knob → fare"), I15 ("Unit bends → corner"), I17 ("up to 32 pieces"), I22 (quote now "…the depth really is important…"), I9 (l03 single line, l44 60px). Not resolved: I19/I20, l46 still says "pts" although the judge asked for "points". Rejections hold: I11 (diagram text is counted only toward the 22-word cap, and l20–l24 are at most 20 words), I14, I18, I21 (quotation card with attribution), I7, I10, I16. New problem introduced: l30 narration was rewritten (I48/I49) but the screen text was not updated, so it now mismatches. I1/I2/I3/I5 (package cards re-rendered): cannot verify, the screenshot fields for agenda, c_* and outro are empty.

## 问题表

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l30 | P2, P3 | 必改 | "Which way / to turn?" + "Next episode" | Strict linking line. Narration now says there is "a much faster way to find each one's direction"; the screen still poses the which-way question that l25 had already answered (nudge each knob downhill), so screen and narration disagree and the teaser is also wrong in tone (next time is about speed, not direction). Screenshot s4_l30 confirms the old text. | "A faster way" / "Next time" (or "Too many knobs?" / "Next time: a faster way") |
| l35, l36, l37 | P4 | 建议 | "10 side by side: ≤ 11 pieces" / "10 in 5 layers: up to 32 pieces" | Two notations (≤ symbol vs "up to") for the same idea in one pair; "10" has no noun, so a viewer reading only the screen cannot tell what is being counted. | "10 units side by side: up to 11 pieces" / "10 units in 5 layers: up to 32 pieces" (8 and 9 words, both within limit) |
| l36 | P3 | 建议 | "Earlier folds, reused" (same 54px as the two data headings) | Third heading at the same level, placed below the left chart only, so it reads as a caption for the staircase, not the takeaway for both. | Make it a caption size under both charts, or "Reuse earlier folds" at a smaller weight |
| l46 | P4 | 建议 | "Remove a middle layer → ~2 pts worse" | "pts" is a clipped abbreviation; the previous round (I20) asked for "points" and the author marked it fixed, but the text still has "pts". | "Remove a middle layer → ~2 points worse" |
| outro | P2 | 记录 | "Simple units, stacked in layers" | Near-verbatim repeat of l48 "simple little units with knobs, stacked layer on layer". Acceptable for a one-line takeaway card; note only. | Keep, or "Units + knobs, stacked in layers" |
| l44 | P2 | 记录 | eyebrow "Not told what to look for" | Nearly the same words as narration "Nobody told it what to look for"; kept because it labels the surprise. Still a repeat, set in small eyebrow type. | Keep (judge already ruled), or "Unprompted" is not recommended (new term) |
| l29 | P4 | 记录 | "Unit bends → corner" | Slightly clipped, but understandable beside the curve and matches narration "every corner ... one little unit making its bend". | Optional: "One unit = one corner" |
| agenda | P3, P4 | 存疑 | "Prereqs: Gradient descent" | Extracted label "Prereqs" is course jargon and the hint text "Not required — one-line recap" is not in the materials; screenshot empty, so the rendered card cannot be checked. If the card really prints "Prereqs:", change it. | "Good to know: Gradient descent" |
| agenda, c_*, outro | P3, P5 | 存疑 | empty screenshot fields | Strict-item cards (agenda numbering 01–04, chapter cards, outro "Next · Backpropagation", hold times) were not in the supplied screenshots, so I only checked extracted text, which is consistent. | Supply card frames for the next round |

## 整体观察

- Round 3 state is close: no hard-limit breach, outline style is mostly held, and most round-2 fixes landed.
- Must fix before lock: l30 screen text must follow the rewritten narration (strict linking line).
- Keep: l41 stat grid (8 layers / 60M knobs / 1.2M photos / 1,000 categories) is a model outline slide, big numbers with small units.
- Keep: l22 "37 knobs" and l24 network diagram with a three-level hierarchy (title, definition, loosely-named note).
- Keep: l35 side-by-side staircase vs zigzag with colour-coded 11 vs 32; contrast carried by the screen, narration explains.
- Remaining polish: l35 notation and noun, l36 weight, l46 "pts".
