# t11 Loss function — narration (English)

v1.3.1 (2026-11-10, after the listening check: l18 "the lows and the highs cancel out" in present tense; "too-lows" was transcribed as "two lows"). v1.3 (2026-11-09, per the lines_r3 judge's must-fix: l31–l33 "even the lowest point isn't zero" move to the end of "A small experiment"; chapter 3 now opens at l34 with the judge's wording; also l15 "That's the red square", l29, l33, l45, l46 per the judges). v1.2 (2026-11-09, per lines_r2 judges: l49 says "landscape" (the word the narration used), l50 no double "that's", l43 no repeated "trained", l20 l26 l33 l35 trimmed tics, l23 "one of the most common"). v1.1 (2026-11-09, per lines_r1 judges: l05 defines error as too high or too low, l11 and l38 chapter openers, l29 l33 l47 l49 l50 judges' wording, fewer "That's…", l40–l41 say "sure" to match the screen, l19 −$0.33 matches the screen). v1 (2026-11-09): spoken first by a native narrator from `drafts/v1_brief.md` (`drafts/v1_en.md`); the author only merged short lines, trimmed, aligned line ids with `script.md`, and checked facts ("a hundred billion knobs" → "tens of billions": the largest Llama 2 has 70 billion parameters). Segment, line ids and tags match `script.md`.

## s0 Cold open [冷开场]
- l01: Last time, we said a model is a machine with knobs, and learning means turning those knobs to the right spot.
- l02: But what does "right" even mean? How does the machine know this turn beat the last one?
- l03: The trick is to give its mistakes a score.
- l04: That score is called the loss, and the rule for working it out is the loss function. That's today's topic.

## s2 What a loss function is [章:problem]
- l05: Every time the model guesses, it lands a bit too high or too low. That gap is the error.
- l06: Roll all those errors up into one number, and that's the loss: a score for how wrong it is.
- l07: It's the opposite of a test score: lower is better, and zero means not wrong at all.
- l08: Kind of like golf, where fewer strokes is better.
- l09: Now the machine can check itself. If a turn lowers the score, keep it. If not, turn it back.
- l10: So training is just turning the knobs again and again to push that score down.

## s3 A small experiment [章:experiment]
- l11: Remember those twelve made-up taxi rides? Distance along the bottom, fare up the side.
- l12: The model's still that straight line, with two knobs: starting fare and price per kilometer.
- l13: First try: a {$5|five-dollar} starting fare and {$2|two dollars} a kilometer. The whole line sits too low.
- l14: Take the {5|five}-kilometer ride: it cost {$23|twenty-three dollars}, the model guessed {$15|fifteen}, so it's off by {$8|eight}. That's the error.
- l15: Now square it: eight times eight is {64|sixty-four}. That's the red square.
- l16: Do that for all twelve rides, take the average, and this setting scores {78|seventy-eight}.
- l17: Second try: {$4|four dollars} to start and {$3.50|three fifty} a kilometer. Too steep, so short rides come out low and long ones high.
- l18: If we skip the squaring and just average the errors, the lows and the highs cancel out.
- l19: The average is only {−$0.33|minus thirty-three cents}, so it looks like it's barely wrong at all.
- l20: So we square. Everything turns positive, and nothing cancels.
- l21: And big misses cost way more: off by two costs four, but off by eight costs {64|sixty-four}.
- l22: Square, then average, and this setting scores {13.4|thirteen point four}.
- l23: This is called mean squared error, and it's one of the most common loss functions.
- l24: Third try: {$10|ten dollars} to start, {$2.50|two fifty} a kilometer. The squares are tiny, and it scores {2.19|two point one nine}.
- l25: The third has the lowest score, so it's the best of the three.
- l26: But that's only three tries. Score every setting of both knobs, and you get a landscape of scores.
- l27: Starting fare along the bottom, price per kilometer up the side, and the darker the color, the higher the score.
- l28: Our three tries: the first way up high, the second halfway down, the third nearly at the bottom of the valley.
- l29: The best is {$10.20|ten dollars twenty} to start and {$2.54|two fifty-four} a kilometer. It scores {1.97|one point nine seven}.
- l30: It's the best setting, and the whole job of training is finding that lowest point.
- l31: Here's something easy to miss: even the lowest point isn't zero.
- l32: Real fares bounce around with traffic and detours, so no straight line could nail every ride.
- l33: Training isn't chasing zero. It's getting as low as it can.

## s4 The model only sees the score [章:lens]
- l34: Here's the thing: the model has no idea what a taxi is. All it sees is the score.
- l35: The way you score it shapes how it learns. Because we squared the errors, it's terrified of big mistakes.
- l36: It would rather be a little off on every ride than way off on just one.
- l37: So when you pick a loss function, you're really telling the model what "good" means.

## s5 How big models are scored [章:real]
- l38: Big language models like ChatGPT get a score in training too, just not for taxi fares.
- l39: Their job is to guess the next word, like what comes after "Twinkle, twinkle, little."
- l40: The score checks how sure the model was about the real next word. The less sure, the bigger the penalty.
- l41: If it was {90%|ninety percent} sure of the right word, the penalty's tiny. Only {10%|ten percent} sure, and it's way bigger.
- l42: This kind of scoring is called cross-entropy. The name is all you need for now.
- l43: In {2023|twenty twenty-three}, Meta tracked that score while training a model called Llama 2.
- l44: It read {2 trillion|two trillion} tokens of text. Tokens are roughly words or bits of words.
- l45: And even then, the score was still falling, nowhere near flat.
- l46: A big model has tens of billions of knobs, we have two, but the job's the same: find the lowest point.

## s6 Wrap-up [包装:outro]
- l47: So, a loss function is how you score the model's mistakes, and lower is better.
- l48: And training is just pushing that score down.
- l49: But with tons of knobs, that landscape's way too big to see all at once. So which way do you turn to go downhill?
- l50: That's where gradient descent comes in. It's up next time.
