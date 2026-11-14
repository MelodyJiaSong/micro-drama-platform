# screen_en__a (a seat, claude-sonnet-5-5), round 2

## 评分表
- P1 2 证据：No hard-limit breach under the round-2 rules. Heaviest screens: l29 (title 5 + dials 6 + card 6 + "= the exact same model" 4 = 21 words, 4 blocks, at the ceiling) and l25 (chart 3 + dials 6 + "8 km → $30.50" 3 + caption 5 = 17 words, 4 blocks). Longest title "Set by training, not by hand" (l36) = 6 words, ok. l38 six-number list counts as one block. Only soft flaws: "Not one of the twelve" (l25) and "= 175 billion knobs" (l34) are near-sentences.
- P2 2 证据：l34 "= 175 billion knobs" repeats narration "a hundred and seventy-five billion knobs" nearly verbatim; l25 "Not one of the twelve" echoes "None of our twelve rides was eight kilometers"; l35 "One reading per second" uses "reading" while narration says "knob setting" (term drift). l29 shows the same two numbers twice (dials at 30% plus the card).
- P3 2 证据：Chapter eyebrows 01–04 match chapter cards ("What a model looks like", "Let's turn the knobs", "What it learned", "Billions of knobs") and l13 "Learning = setting knobs right" matches the outro. Small flaws: l12 "The math / by people" vs "Settings / from examples" has an article mismatch; l29 carries two number sets, so the eye has two places to land.
- P4 2 证据：Sentence case throughout, no Chinglish, no trailing periods, arrows and "=" used consistently, all four chapter titles read naturally aloud. Minor: outro/l13 "Learning = setting knobs right" is slightly stilted ("setting knobs right" drops the article); l22 "Backing off a bit" is a gerund while its siblings (l18 "All too low", l20 "Longer ride, bigger miss") are not; l12 "The math by people" has no verb or colon.
- P5 2 证据：Short screens are fine (l07 "Parameters = knobs" 2 words in 1.9s; l34 adds 3 words in 1.5s but they restate the big number already on screen). Densest are l29 (21 words in 8.1s, with the number set duplicated) and l25 (17 words in 7.3s plus a chart). Both still readable at ~3 words/s, but with subtitles at the bottom they are tight.
- P6 2 证据：Every flaw below has a drop-in rewrite; nothing is a hard-limit breach, so rewrites are polish.
- R 3 证据：See the re-check list below. Every must-fix from r1 (I1/I2 outro, I14 "Farther, further off", I16/I17 stale "Overshot" at l22, I22/I23/I29 colliding columns at l28/l37, I30/I31 18-number block at l38) is resolved in the screenshots, and the "不改" judgements hold; no new defect was created by the fixes.

### R: previous issues, one by one (screen_en only)
- I1/I2 outro run-on: 已解决. Now two equation lines "Parameters = knobs" / "Learning = setting knobs right" (6 words) plus "Loss function". Wording note in issue table (建议).
- I3 l04 card covering "A model": 已解决. s0_l04 shows "A model" fully clear of the "INSIDE A MODEL" card with a gap of roughly 90px; "不改/移位" judgement stands.
- I4 l05 placeholders: 不改 accepted (记录).
- I5 "per km" in the formula: 不改 accepted; the dial label is "Per km" on every screen, so the formula stays consistent.
- I7/I8/I9/I29 l12 and l37 parallel labels: 已解决 in layout (s5_l37 and s2_l12 show two clean rows, same wording in both), residual article asymmetry logged below as 建议.
- I10 "Guesses = a line": 不改 accepted; equation labels are outline-style.
- I11 "Bars = how far off" vs narration "little vertical lines": 不改, reason weak but low-impact; kept as 存疑 below.
- I12/I13 l19 "Whole line goes up": 不改 accepted.
- I14/I15 l20: 已解决 ("Longer ride, bigger miss").
- I16/I17 l22: 已解决 ("Backing off a bit"; no stale "Overshot").
- I18 l23 "Right along the dots": 不改, judgement stands (it pins the conclusion to the chart).
- I19 l24 "?$30.50": 已解决 / 不成立 confirmed; the text inventory shows only "8 km → ?" at l24.
- I20 l26 title: 已解决 ("All it learned: two settings" appears from l27).
- I21/I22/I23 l28: 已解决. s4_l28 shows "Machine … Same" and "Knob settings … Changed" at table size with a clear gap; no collision.
- I24/I50 l29 density: 已解决 as to the limits (21 words, 4 blocks) but still the densest screen; 改出新问题: none, residual 建议 below.
- I25/I26 l30/l31: 已解决 (l31 removed).
- I27 l32: 不改 accepted (record only).
- I28 l34: 不改, judgement stands as number-plus-label; verbatim echo kept as 记录.
- I30/I31 l38: 已解决 (six numbers, one block).
- I32 l39 spacing: 不成立 confirmed.

## 问题表

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| outro / l13 | P4 | 建议 | Learning = setting knobs right | Strict item (outro). Understandable and consistent with l13, but "setting knobs right" is clipped; a native would say "getting the knobs right" or "tuning the knobs". Not a hard breach; the "right positions" idea is the one narration l41 actually states. | Learning = getting the knobs right (and the same at l13) |
| l29 | P1/P2/P5 | 建议 | Dials ($10.20 / $2.54, faded) + card (For a friend / Base fare $10.20 / Per km $2.54) + "= the exact same model" | 21 words, 4 blocks, at the ceiling; the same numbers and labels appear twice (faded dials and card) for 8.1s of reading. | Remove the dials entirely at this beat (keep title, card, "= same model") |
| l12 | P4/P3 | 建议 | The math · by people / Settings · from examples | Rows are not strictly parallel: "The math" has an article, "Settings" does not; no verb or colon, so each row reads as a clipped fragment. Same pair repeats at l37, so it is consistent, but still uneven. | Math · set by people / Settings · learned from examples (same at l37) |
| l35 | P2 | 建议 | One reading per second | Narration says "read out one knob setting every second"; elsewhere the screen says "settings" (l27, l28, l38), so "reading" is the odd term. | One setting per second |
| l22 / l25 | P2 | 记录 | Per km dial $2.54 and "$30.50" | Narration says "about $2.50"; the dial shows $2.54. Not wrong ("about"), but a viewer may notice the gap between $2.50 spoken and $2.54 shown. | Keep; optionally say "about two fifty-four"-style in narration or round the dial to $2.50 |
| l34 | P2 | 记录 | = 175 billion knobs | Verbatim echo of narration, only 1.5s on screen; carries the parameter-to-knob step so keep. | Keep (or "175 billion knobs" without "=") |
| l25 | P2 | 建议 | Not one of the twelve | Near-verbatim echo of narration, 5 words in the fourth block. | Not in the data (4 words) or drop |
| l17 | P2 | 存疑 | Bars = how far off | Narration says "little vertical lines"; the screen calls them "bars" while the picture shows thin lines. | Gaps = how far off |
| l22 | P4 | 记录 | Backing off a bit | Gerund fragment, unlike its siblings; reads fine. | Back off a bit |
| l32 | P1 | 记录 | Chatting takes far more knobs | Subject-verb-object, close to a sentence but only 5 words and a chapter-opening title. | More knobs for chat |
| l39 | P2 | 记录 | 100B parameters = 100B knobs | l01 says "100B+"; narration "over a hundred billion". The plus is dropped, a small mismatch with the cold open and narration. | 100B+ parameters = 100B+ knobs |

## 整体观察
- No hard-limit breach under the round-2 counting rules; the screen set is an outline, not prose, and the big r1 problems (outro run-on, stale l22 label, colliding columns, 18-number block) are fixed.
- Remaining issues are polish: l29 duplicated numbers, the outro equation wording, and a few small term drifts (reading/setting, bars/lines, $2.54 vs "about $2.50").
- Keep: the cold-open chain "Last time → A model → Inside a model ?" (clear, readable, answered by the chapters); the equation-label style ("Parameters = knobs", "Learning = ...", "Training = turning knobs"); the knob dials that carry the story with almost no words.
- Chapter titles all read naturally aloud and match their eyebrows; no must-fix in the strict items.
