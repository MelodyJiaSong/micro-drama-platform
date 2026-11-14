## 评分表

- V1 1 证据：l11 “Distance along the bottom, fare up the side” still sounds like chart labels read aloud; l15 “That's this red square” is an awkward handoff; l50 “and that's next time” sounds clipped.
- V2 1 证据：The chapter transition at l38 now connects naturally through “just not for taxi fares.” However, strict items l02, l11, l49 and l50 still need changes. The outro’s question is useful, but its wording and landing remain awkward.
- V3 1 证据：l05 introduces high and low guesses but never explains negative errors. Consequently, l18–l19 jump from an eight-dollar gap to errors cancelling and an average of “minus thirty-three cents.”
- V4 3 证据：l14–l16 move directly through error, squaring and averaging. l47–l48 give a short, useful recap. The golf comparison at l08 supplies an intuitive comparison rather than empty repetition.
- V5 2 证据：l31 “Here's something easy to miss” and l36 “It would rather be a little off…” sustain a conversational voice. l28’s three-part positional list is less fluid; l29 carries several numbers but now labels the starting fare clearly.
- V6 3 证据：Every line marked “a bit off” below has a drop-in rewrite in the issue table, no longer than its original. The five most awkward lines are ranked after that table.
- R 1 证据：**I59—resolved by justified non-adoption:** “How big models are scored” is an ordinary chapter title; passive wording alone is not a defect. **I60—unresolved:** l02 is unchanged; “beat” is conversational, but “this turn” still makes the listener reconstruct the knob adjustment. The visual justification does not settle an ear-only concern. **I61—partly resolved:** l20 and l30 vary the sentence endings successfully; l50 still has a weak double-“that's” landing. **I62—unresolved:** l05 adds high/low directions but retains “Every time” and does not establish signed errors. **I63—resolved:** “put simply” is gone from l10. **I64—unresolved:** l11’s opening question improves the entry, but the following axis-label fragments remain. Keeping axis information does not require keeping that structure. **I65—resolved:** “made-up taxi rides” removes the awkward standalone qualification. **I66—unresolved:** retaining a square reference is reasonable, but does not justify “That's this.” **I67—resolved:** l17’s “so short rides come out low…” creates a clearer causal link; the remaining conversational ellipsis is acceptable. **I68—unresolved:** l05’s high/low wording still does not explain why an error can be negative; l18 retains the improvised nouns “too-lows and too-highs.” **I69—no new fix required:** the three scores remain dense, but l25 supplies the essential comparison; screen visibility is not evidence for this blind review. **I70—resolved:** l26 now says “landscape of scores.” **I71—justified non-adoption:** the axis directions themselves are conventional spoken chart description; I would not require a rewrite of l27. **I72—partly justified non-adoption, still a small issue:** “clearly off” was too strong, but l28 remains a compressed roll call rather than flowing speech. **I73—resolved:** “ten dollars twenty” makes the amount identifiable by ear. **I74—resolved:** l29 now distinguishes the settings from the resulting score. **I75—partly resolved:** “chasing as low…” is gone, but l33’s “It's just getting as low…” still leaves the score implicit. **I76—resolved:** l38 provides its own audible bridge. **I77—resolved:** the ambiguous “It's just scoring…” has gone. **I78—resolved:** “just not for taxi fares” gives the contrast concrete meaning. **I79—resolved:** l40’s “how sure…about the real next word” is speakable and clear. **I80—resolved:** l41 now tells us what the percentages describe. **I81—resolved:** “tracked that score” works without seeing a curve. **I82—resolved:** l47 now defines the loss function as how mistakes are scored, preserving l04’s distinction. **I83—partly resolved:** “go downhill” works; “to ever see whole” introduces a clipped phrase. **I84—partly resolved:** “That's where gradient descent comes in” establishes its role, but “and that's next time” still needs a natural landing.

## 问题表

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l18 | V1, V3 | 必改 | If we skipped the squaring and just averaged the errors, the too-lows and too-highs would cancel out. | High and low guesses have been introduced, but negative and positive errors have not. “Too-lows and too-highs” also requires decoding improvised nouns while following arithmetic. | Without squaring, low guesses count as negative errors. High guesses count as positive, so they can cancel. |
| l11 | V1, V2, V3 | 必改 | Remember those twelve made-up taxi rides? Distance along the bottom, fare up the side. | The opening question is natural. What follows sounds like reading axis labels, and gives a blind listener positions before clearly restating the information being compared. Strict chapter opening. | Remember those twelve made-up taxi rides? We've got each ride's distance and fare. |
| l02 | V1, V2 | 必改 | But what does "right" even mean? How does the machine know this turn beat the last one? | “Beat” is idiomatic, but “this turn” briefly sounds like a turn in a game. Naming the knob adjustment makes the cold-open question immediately clear. | But what does "right" even mean? How does the machine know whether turning a knob improved its guess? |
| l49 | V1, V2 | 必改 | But with tons of knobs, that map gets way too big to ever see whole. So which way do you turn to go downhill? | “See whole” sounds clipped here. I expect “see the whole map” or “see it all at once.” The question itself is a useful hook. Strict outro. | But with tons of knobs, we can't see the whole map. So which way do we turn to go downhill? |
| l50 | V1, V2, V5 | 必改 | That's where gradient descent comes in, and that's next time. | The first clause works. “And that's next time” sounds like an abbreviated production note and weakens the final beat. Strict outro. | Next time, we'll see how gradient descent helps us decide. |
| l15 | V1, V3 | 建议 | Now square it: eight times eight is sixty-four. That's this red square. | “That's this” is awkward. The listener also needs to understand what the square represents. That connection can be stated while preserving the visual reference. | Eight times eight is sixty-four. The red square shows that squared error. |
| l28 | V1, V5 | 建议 | Our three tries: the first way up high, the second halfway down, the third nearly at the bottom of the valley. | Understandable, but the introductory label and three verbless positions sound like a roll call. Small linking verbs would make this sound more conversational. | Our first try is high on the slope. The second is lower, and the third is near the valley floor. |
| l33 | V1, V3 | 建议 | So training isn't chasing zero. It's just getting as low as it can. | “It” grammatically continues to mean training, while “getting low” concerns the score. The listener can infer the meaning, but naming the score is cleaner. | Training isn't chasing zero. It's getting the score as low as possible. |
| l05 | V3 | 建议 | Every time the model guesses, it lands a bit too high or too low. That gap is the error. | “Every time” unnecessarily says that guesses always miss. Introducing high/low as possibilities also leaves room for an exact guess. | The model can guess too high or too low. That difference is the error. |

**Five most awkward lines:** 1. l18; 2. l11; 3. l50; 4. l49; 5. l02.

## 逐句复述

The conversational versions below are the retell test. Where a line is marked off, the issue table provides the length-limited replacement.

| 句号 | 原句 | 跟朋友会怎么说 | 判 |
|---|---|---|---|
| l01 | Last time, we said a model is a machine with knobs, and learning means turning those knobs to the right spot. | Remember the machine with knobs? Learning means adjusting them until they're in the right place. | natural |
| l02 | But what does "right" even mean? How does the machine know this turn beat the last one? | But how does it know whether adjusting a knob made its guess better? | a bit off |
| l03 | The trick is to give its mistakes a score. | We give its mistakes a score. | natural |
| l04 | That score is called the loss, and the rule for working it out is the loss function. That's today's topic. | The score is the loss. The loss function is the rule we use to calculate it. That's what we're looking at today. | natural |
| chapter 1 | What is a loss function? | So, what's a loss function? | natural |
| l05 | Every time the model guesses, it lands a bit too high or too low. That gap is the error. | A guess can be too high or too low. The difference from the actual answer is the error. | a bit off |
| l06 | Roll all those errors up into one number, and that's the loss: a score for how wrong it is. | Combine those errors into one number, and you've got a score for how wrong the model is. | natural |
| l07 | It's the opposite of a test score: lower is better, and zero means not wrong at all. | Unlike a test score, you want this number to be low. Zero means no mistakes. | natural |
| l08 | Kind of like golf, where fewer strokes is better. | It's like golf: fewer strokes is better. | natural |
| l09 | Now the machine can check itself. If a turn lowers the score, keep it. If not, turn it back. | Now it can check whether an adjustment helped. Keep it if the score drops; otherwise, undo it. | natural |
| l10 | So training is just turning the knobs again and again to push that score down. | Training means adjusting those knobs over and over to lower the score. | natural |
| chapter 2 | A small experiment | Let's try a small experiment. | natural |
| l11 | Remember those twelve made-up taxi rides? Distance along the bottom, fare up the side. | Remember our twelve made-up taxi rides? We've got each ride's distance and fare. | a bit off |
| l12 | The model's still that straight line, with two knobs: starting fare and price per kilometer. | We're still using a straight line, with one knob for the starting fare and another for the price per kilometer. | natural |
| l13 | First try: a five-dollar starting fare and two dollars a kilometer. The whole line sits too low. | Let's try five dollars to start and two dollars a kilometer. That puts the whole line too low. | natural |
| l14 | Take the five-kilometer ride: it cost twenty-three dollars, the model guessed fifteen, so it's off by eight. That's the error. | The five-kilometer ride cost twenty-three dollars. We guessed fifteen, so the error is eight dollars. | natural |
| l15 | Now square it: eight times eight is sixty-four. That's this red square. | Eight times eight is sixty-four. That's the squared error the red square represents. | a bit off |
| l16 | Do that for all twelve rides, take the average, and this setting scores seventy-eight. | Do the same for every ride and average the results. These settings get a score of seventy-eight. | natural |
| l17 | Second try: four dollars to start and three fifty a kilometer. Too steep, so short rides come out low and long ones high. | Now try four dollars to start and three fifty a kilometer. The line's too steep: short rides come out low, long rides high. | natural |
| l18 | If we skipped the squaring and just averaged the errors, the too-lows and too-highs would cancel out. | Without squaring, low guesses give negative errors and high guesses give positive ones. Those can cancel when we average them. | clearly off |
| l19 | The average is only minus thirty-three cents, so it looks like it's barely wrong at all. | We get an average error of just minus thirty-three cents, which makes the guesses seem much better than they are. | natural; depends on fixing l18 |
| l20 | So we square: once everything's squared, it's all positive, and nothing cancels. | Squaring makes the errors positive, so they don't cancel each other out. | natural |
| l21 | And big misses cost way more: off by two costs four, but off by eight costs sixty-four. | Bigger mistakes get much bigger penalties. Being off by two costs four; being off by eight costs sixty-four. | natural |
| l22 | Square, then average, and this setting scores thirteen point four. | Square the errors and average them. This time the score is thirteen point four. | natural |
| l23 | This is called mean squared error, and it's the most common loss function. | That's mean squared error. It's the most common loss function. | natural |
| l24 | Third try: ten dollars to start, two fifty a kilometer. The squares are tiny, and it scores two point one nine. | Try ten dollars to start and two fifty a kilometer. The squared errors are tiny now; the score is two point one nine. | natural |
| l25 | The third has the lowest score, so it's the best of the three. | The third try has the lowest score, so it's our best one. | natural |
| l26 | But that's just three tries. Score every setting of both knobs, and you get a landscape of scores. | But we've only tried three settings. Imagine scoring every combination: you'd get a whole landscape of scores. | natural |
| l27 | Starting fare along the bottom, price per kilometer up the side, and the darker the color, the higher the score. | We've got starting fare along the bottom and price per kilometer up the side. Darker means a higher score. | natural |
| l28 | Our three tries: the first way up high, the second halfway down, the third nearly at the bottom of the valley. | Our first try is high up. The second is lower, and the third is almost at the bottom of the valley. | a bit off |
| l29 | Ten dollars twenty to start, then two fifty-four a kilometer, gives the lowest score: one point nine seven. | The best settings are ten dollars twenty to start and two fifty-four a kilometer. That gets the score down to one point nine seven. | natural |
| l30 | It's the best setting, and the whole job of training is finding that lowest point. | That's the best setting. Training is about finding that lowest point. | natural |
| chapter 3 | It only sees the score | All the model sees is the score. | natural |
| l31 | Here's something easy to miss: even the lowest point isn't zero. | Notice that even the lowest score isn't zero. | natural |
| l32 | Real fares bounce around with traffic and detours, so no straight line could nail every ride. | Traffic and detours change fares, so one straight line can't get every ride exactly right. | natural |
| l33 | So training isn't chasing zero. It's just getting as low as it can. | Training isn't trying to reach zero. It's trying to get the score as low as possible. | a bit off |
| l34 | And here's the other thing: the model has no idea what a taxi is. All it sees is the score. | And remember, the model doesn't know what a taxi is. It only sees the score. | natural |
| l35 | However you score it, that's how it learns. Because we squared the errors, it's terrified of big mistakes. | The way we score it shapes what it learns. Squaring the errors makes big mistakes especially costly. | natural |
| l36 | It would rather be a little off on every ride than way off on just one. | It would rather miss every fare by a little than miss one fare by a lot. | natural |
| l37 | So when you pick a loss function, you're really telling the model what "good" means. | Choosing the loss function tells the model what counts as doing well. | natural |
| chapter 4 | How big models are scored | How do we score big models? | natural |
| l38 | Big language models like ChatGPT get a score in training too, just not for taxi fares. | Language models get training scores too. They're just being scored on something other than fares. | natural |
| l39 | Their job is to guess the next word, like what comes after "Twinkle, twinkle, little." | They guess what word comes next. What comes after “Twinkle, twinkle, little”? | natural |
| l40 | The score checks how sure the model was about the real next word. The less sure, the bigger the penalty. | We check how sure it was about the word that actually came next. Less sure means a bigger penalty. | natural |
| l41 | If it was ninety percent sure of the right word, the penalty's tiny. Only ten percent sure, and it's way bigger. | If it was ninety percent sure about the right word, there's hardly any penalty. At ten percent, the penalty is much bigger. | natural |
| l42 | This kind of scoring is called cross-entropy. The name is all you need for now. | That's called cross-entropy. You only need to recognize the name for now. | natural |
| l43 | In twenty twenty-three, Meta trained a model called Llama 2 and tracked that score as it trained. It kept going down. | Meta tracked that score while training Llama 2 in twenty twenty-three, and it kept dropping. | natural |
| l44 | It read two trillion tokens of text. Tokens are roughly words or bits of words. | It read two trillion tokens. A token is roughly a word or part of a word. | natural |
| l45 | And even then, the score was still falling, with no sign yet of a floor. | Even after all that text, the score was still dropping. It hadn't bottomed out. | natural |
| l46 | A big model has tens of billions of knobs, we have two, and the job's the same: find the lowest point. | They've got tens of billions of knobs; we've got two. But we're both trying to find the lowest point. | natural |
| l47 | So, a loss function is how you score the model's mistakes, and lower is better. | The loss function tells us how to score the mistakes. A lower score is better. | natural |
| l48 | And training is just pushing that score down. | Training is about lowering that score. | natural |
| l49 | But with tons of knobs, that map gets way too big to ever see whole. So which way do you turn to go downhill? | With that many knobs, we can't see the whole map. How do we know which way to turn to go downhill? | a bit off |
| l50 | That's where gradient descent comes in, and that's next time. | Next time, we'll see how gradient descent helps us decide. | a bit off |

## 整体观察

- **Round 2 still needs changes:** five strict-item issues remain, alongside the missing signed-error explanation.
- Keep l03–l04’s clear distinction between the score and the rule for calculating it.
- Keep l25’s plain “best of the three” comparison; it helps listeners recover the point without remembering every decimal.
- Keep l37–l38’s progression from defining “good” to scoring language models. That transition now follows an audible thought.
- Conversational fragments can work: l13, l17 and l27 are understandable spoken descriptions. The issue is where compression becomes label-reading or obscures a necessary step.
- This review assesses the supplied words as heard internally; recorded delivery and the unspecified main title cannot be assessed from this material.