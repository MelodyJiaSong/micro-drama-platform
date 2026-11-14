# Narration (in playback order)

Each line: id (spoken duration / pause after): exactly what the narrator says. [On screen: …] lists the most prominent on-screen text when the line ends, only so you can tell whether words like 'this' or 'on the left' point at something; the visuals are reviewed separately. Title and chapter cards are silent; they only mark scene changes.

## Cold open (before the title card)
- l01（8.1s / pause 0.3s）：Last time, we said a model is a machine with knobs, and learning means turning those knobs to the right spot.  [On screen: 「Model = machine + knobs」]
- l02（6.5s / pause 0.3s）：But what does "right" even mean? How does the machine know this turn beat the last one?  [On screen: 「?」, 「Is this turn better?」]
- l03（3.5s / pause 0.4s）：The trick is to give its mistakes a score.  [On screen: a chart]
- l04（7.7s）：That score is called the loss, and the rule for working it out is the loss function. That's today's topic.  [On screen: 「Loss function」, a chart]

> [On screen: title card (series + episode title)]

> [On screen: chapter card “What is a loss function?”]

## What a loss function is
- l05（7.3s / pause 0.3s）：Every time the model guesses, it lands a bit too high or too low. That gap is the error.  [On screen: 「How far off = error」, a chart]
- l06（7.3s / pause 0.3s）：Roll all those errors up into one number, and that's the loss: a score for how wrong it is.  [On screen: 「17.9」, 「Errors → one score」, a chart]
- l07（6.5s / pause 0.3s）：It's the opposite of a test score: lower is better, and zero means not wrong at all.  [On screen: 「17.9」, 「Lower loss = better」, a chart]
- l08（3.5s / pause 0.3s）：Kind of like golf, where fewer strokes is better.  [On screen: 「17.9」, 「Lower loss = better」, a chart]
- l09（7.3s / pause 0.4s）：Now the machine can check itself. If a turn lowers the score, keep it. If not, turn it back.  [On screen: 「8.6」, 「Turn, then check」]
- l10（5.8s）：So training is just turning the knobs again and again to push that score down.  [On screen: 「2.2」, 「Training: push it down」]

> [On screen: chapter card “A small experiment”]

## A small experiment
- l11（5.8s / pause 0.4s）：Remember those twelve made-up taxi rides? Distance along the bottom, fare up the side.  [On screen: a chart]
- l12（5.8s / pause 0.3s）：The model's still that straight line, with two knobs: starting fare and price per kilometer.  [On screen: 「$0」, 「$0」, a chart]
- l13（6.9s / pause 0.3s）：First try: a five-dollar starting fare and two dollars a kilometer. The whole line sits too low.  [On screen: 「Try 1: too low」, 「$5」, a chart]
- l14（8.1s / pause 0.4s）：Take the five-kilometer ride: it cost twenty-three dollars, the model guessed fifteen, so it's off by eight. That's the error.  [On screen: 「Try 1: too low」, 「$5」, a chart]
- l15（4.6s / pause 0.3s）：Now square it: eight times eight is sixty-four. That's this red square.  [On screen: 「Try 1: too low」, 「$5」, a chart]
- l16（5.4s / pause 0.4s）：Do that for all twelve rides, take the average, and this setting scores seventy-eight.  [On screen: 「78」, 「Try 1: too low」, a chart]
- l17（8.5s / pause 0.3s）：Second try: four dollars to start and three fifty a kilometer. Too steep, so short rides come out low and long ones high.  [On screen: 「Try 2: too steep」, 「$4」, a chart]
- l18（7.3s / pause 0.4s）：If we skipped the squaring and just averaged the errors, the too-lows and too-highs would cancel out.  [On screen: 「They cancel out」, 「$4」, a chart]
- l19（6.2s / pause 0.4s）：The average is only minus thirty-three cents, so it looks like it's barely wrong at all.  [On screen: 「−$0.33」, 「They cancel out」, a chart]
- l20（4.6s / pause 0.4s）：So we square. Everything turns positive, and nothing cancels.  [On screen: 「Squared: all positive」, 「$4」, a chart]
- l21（6.5s / pause 0.3s）：And big misses cost way more: off by two costs four, but off by eight costs sixty-four.  [On screen: 「Squared: all positive」, 「$4」, a chart]
- l22（3.8s / pause 0.3s）：Square, then average, and this setting scores thirteen point four.  [On screen: 「13.4」, 「Squared: all positive」, a chart]
- l23（5.0s / pause 0.4s）：This is called mean squared error, and it's one of the most common loss functions.  [On screen: 「Mean squared error」, 「$4」, a chart]
- l24（7.7s / pause 0.3s）：Third try: ten dollars to start, two fifty a kilometer. The squares are tiny, and it scores two point one nine.  [On screen: 「2.19」, 「Try 3: close」, a chart]
- l25（5.0s / pause 0.4s）：The third has the lowest score, so it's the best of the three.  [On screen: 「Compare all three」, 「78」, a chart]
- l26（6.9s / pause 0.3s）：But that's only three tries. Score every setting of both knobs, and you get a landscape of scores.  [On screen: 「A map of scores」, a chart]
- l27（7.7s / pause 0.4s）：Starting fare along the bottom, price per kilometer up the side, and the darker the color, the higher the score.  [On screen: 「A map of scores」, 「Darker = higher score」, a chart]
- l28（8.1s / pause 0.3s）：Our three tries: the first way up high, the second halfway down, the third nearly at the bottom of the valley.  [On screen: 「A map of scores」, 「$10」, a chart]
- l29（6.5s / pause 0.3s）：Ten dollars twenty to start, then two fifty-four a kilometer, gives the lowest score: one point nine seven.  [On screen: 「1.97」, 「A map of scores」, a chart]
- l30（5.8s）：It's the best setting, and the whole job of training is finding that lowest point.  [On screen: 「1.97」, 「Find the lowest point」, a chart]

> [On screen: chapter card “The model only sees the score”]

## The score is all it sees
- l31（4.2s / pause 0.3s）：Here's something easy to miss: even the lowest point isn't zero.  [On screen: 「1.97」, 「Lowest loss ≠ 0」, a chart]
- l32（6.2s / pause 0.3s）：Real fares bounce around with traffic and detours, so no straight line could nail every ride.  [On screen: 「1.97」, 「Lowest loss ≠ 0」, a chart]
- l33（5.0s / pause 0.4s）：So training isn't chasing zero. It's getting as low as it can.  [On screen: 「Not zero, just the lowes」, a chart]
- l34（7.7s / pause 0.4s）：And here's the other thing: the model has no idea what a taxi is. All it sees is the score.  [On screen: 「Taxi? No idea」, a chart]
- l35（6.9s / pause 0.4s）：The way you score it shapes how it learns. Because we squared the errors, it's terrified of big mistakes.  [On screen: 「How you score shapes lea」, 「Big misses cost most」, a chart]
- l36（6.2s / pause 0.4s）：It would rather be a little off on every ride than way off on just one.  [On screen: 「How you score shapes lea」, 「Big misses cost most」, a chart]
- l37（5.8s）：So when you pick a loss function, you're really telling the model what "good" means.  [On screen: 「Loss function defines “g」, a chart]

> [On screen: chapter card “How big models are scored”]

## How big models are scored
- l38（6.2s / pause 0.4s）：Big language models like ChatGPT get a score in training too, just not for taxi fares.  [On screen: 「Language models」, 「Scored too, but not on f」]
- l39（5.8s / pause 0.4s）：Their job is to guess the next word, like what comes after "Twinkle, twinkle, little."  [On screen: 「Twinkle, twinkle, little」]
- l40（7.7s / pause 0.4s）：The score checks how sure the model was about the real next word. The less sure, the bigger the penalty.  [On screen: 「Twinkle, twinkle, little」, 「Less sure → bigger penal」]
- l41（8.1s / pause 0.4s）：If it was ninety percent sure of the right word, the penalty's tiny. Only ten percent sure, and it's way bigger.  [On screen: 「Twinkle, twinkle, little」, 「90% sure」]
- l42（6.2s / pause 0.4s）：This kind of scoring is called cross-entropy. The name is all you need for now.  [On screen: 「Cross-entropy」]
- l43（7.7s / pause 0.4s）：In twenty twenty-three, Meta tracked that score while training a model called Llama 2.  [On screen: 「Llama 2」, 「Loss keeps falling」, a chart]
- l44（5.8s / pause 0.3s）：It read two trillion tokens of text. Tokens are roughly words or bits of words.  [On screen: 「Llama 2」, 「Loss keeps falling」, a chart]
- l45（5.8s / pause 0.3s）：And even then, the score was still falling, with no sign yet of a floor.  [On screen: 「Llama 2」, 「Loss keeps falling」, a chart]
- l46（8.1s）：A big model has tens of billions of knobs, we have two, and the job's the same: find the lowest point.  [On screen: 「Score ↓」, 「Score ↓」]

## Outro (on screen: end card)
- l47（5.8s / pause 0.4s）：So, a loss function is how you score the model's mistakes, and lower is better.
- l48（3.1s / pause 0.4s）：And training is just pushing that score down.
- l49（9.2s / pause 0.4s）：But with tons of knobs, that landscape's way too big to see all at once. So which way do you turn to go downhill?
- l50（3.8s）：That's where gradient descent comes in. It's up next time.

