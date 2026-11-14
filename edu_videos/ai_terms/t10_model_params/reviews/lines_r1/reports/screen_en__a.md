# screen_en__a report (round 1) - English on-screen text

## 评分表
- P1 2 证据：Most screens are keyword-only (l30 "Training = turning knobs", l13 "Learning = setting the knobs"). Breaches: l38 has an 18-number block (18 words > 9; screen 23 words > 22); l29 is 21 words/10 blocks with every number shown twice (dials, card, readouts).
- P2 2 证据：Division of labour is mostly good (l16-l23 chart headings carry the point, narration explains). Breaches: l24 "8 km → ?$30.50" shows the answer before narration asks the question (l25 gives it); l22 heading "Overshot: too high" contradicts narration "Turn it back a little"; l34 "= 175 billion knobs" repeats narration verbatim.
- P3 2 证据：Eyebrow numbering 01-04 matches chapter cards, and "Base fare / Per km" labels stay consistent l09-l29. But chapter titles mix forms ("What a model looks like", "Let's turn the knobs", "Where the learning lives", "Billions of knobs"), and l17 says "Bars" while narration says "little vertical lines".
- P4 2 证据：Sentence case and no trailing periods throughout. Problems: l20 "Farther, further off" (wincing near-pun), outro "Parameters are knobs learning sets them right" (run-on, 7 words, no break), l24 "?$30.50" malformed, l28/l37 labels fused as "The machineSame" / "The mathPeople decide" in the extraction.
- P5 1 证据：l28 and l37 labels are 16px on a 1920x1080 frame (unreadable next to burned-in subtitles); l38 is an 18-number wall for 6.9s; l29 (21 words, 8.1s) and l11 (18 words, 10s) are heavy; l34 text stays only 1.5s.
- P6 3 证据：Every breach or awkward phrase below has a drop-in rewrite.

## 问题表

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| outro | P4/P1 | 必改 | "Parameters are knobs learning sets them right" | Strict item. Run-on of two ideas with no punctuation; reads as a garbled sentence, not an outline. | Two lines: "Parameters = knobs" / "Learning = setting them right" |
| l22 | P2 | 必改 | "Overshot: too high" | Stale from l21; narration says it is turned back and the fit is close. Contradicts narration. | "Turned back a little" (or "Almost there") |
| l24 | P2/P4 | 必改 | "8 km → ?$30.50" | Gives away the answer before narration asks; "?$30.50" is malformed (question mark plus number). | l24: "8 km → ?"; l25: "8 km → $30.50" |
| c_experiment, c_lens, c_real, c_problem | P3/P4 | 必改 (strict, chapter titles) | "What a model looks like" / "Let's turn the knobs" / "Where the learning lives" / "Billions of knobs" | Inconsistent forms (noun clause, imperative, noun clause, noun phrase); "Where the learning lives" is abstract and the least natural aloud. | "A model, up close" / "Turning the knobs" / "Where learning is stored" / "Billions of knobs" (keep eyebrows identical) |
| l38 | P1/P5 | 必改 | 18 numbers "1.3298 0.9606 0.4326 ..." | Single block with 18 words (>9); screen total 23 (>22). Fine as texture, but counts under the rules. | Show 6 numbers plus "…": "1.33 0.96 0.43 −0.18 1.19 … " (6 words) |
| l20 | P4 | 必改 | "Farther, further off" | Near-pun reads as a typo to native viewers. | "Longer ride, bigger miss" |
| l28 / l37 | P5 | 必改 | "The machine / Same", "The knob settings / Changed"; "The math / People decide", "The settings / Learned from examples" | 16px text on a 1080p frame; unreadable in time. Also fused in extraction. | Raise to at least 28px; or "Machine: same" / "Knobs: changed"; "Math: people" / "Settings: learned" |
| l29 | P1/P2 | 建议 | Dials + "FOR A FRIEND" card + "$10.20 / $2.54" readouts + "= the exact same model" | 21 words, 10 blocks; each number appears twice, and "Base fare/Per km" labels repeat. Title "What it learned: two readings" also stays from l26. | Drop the dial readouts or the card; keep one: title, card (2 rows), "= same model" |
| l17 | P2/P3 | 建议 | "Bars = how far off" | Narration calls them "little vertical lines"; the term differs. | "Gaps = how far off" or "Misses" |
| l34 | P2 | 建议 | "= 175 billion knobs" | Repeats narration verbatim; on screen only 1.5s. | Remove; keep the big number and "knobs" in the eyebrow ("GPT-3 · Parameters = knobs") |
| l12 | P4 | 建议 | "The math by people" / "Settings from examples" | Not parallel ("by" vs "from" without a verb or colon). | "Math: set by people" / "Settings: learned from examples" |
| l30/l31 | P4 | 建议 | "Training = turning knobs" / "Learned = set right" | Not parallel (noun vs past participle). | "Trained = knobs set right" |
| l16 | P4 | 建议 | "Guesses = a line" | Equation form is slightly odd. | "Guesses form a line" |
| l19 | P4 | 记录 | "Whole line goes up" | Fine; could be tighter. | "Line shifts up" |
| l05 | P3 | 记录 | "3" and "—" in the Input/Answer slots | Placeholders appear before the taxi example; harmless. | Keep |
| l11 | P1 | 记录 | 18 words, 8 blocks | Under 22 but heavy; formula and worked sum both show. | Keep sum "10 + 2 × 5 = 20" only, drop the formula line on this screen |
| l26 | P4 | 记录 | "What it learned: two readings" | "readings" is slightly odd for knob values. | "What it learned: two numbers" |

## 整体观察
- Chart-heading style (l16-l23) is mostly the right outline form: 3-4 words, equation or label, narration carries the explanation.
- The cold open (l01-l04) is clean: "100B+" / "parameters" / "Parameter = ?" is a strong outline and passes the strict items; only the l03/l04 eyebrow stack ("Last time", "What it ends up with") is borderline busy.
- The outro is the weakest strict item; the next-time card "Loss function" is good but add "Next time:" label.
- Real shortcomings are mostly density and tiny text (l28, l37, l38, l29), not prose; no narration sentences are printed on screen (the earlier problem is fixed).
- Keep: "Knobs = parameters" (l07), "Training = turning knobs" (l30), and the one-number-per-screen reveals at l33/l35.
