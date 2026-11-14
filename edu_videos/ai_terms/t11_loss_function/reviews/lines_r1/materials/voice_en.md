# Narration (in playback order)

Each line: id (spoken duration / pause after): exactly what the narrator says. [On screen: …] lists the most prominent on-screen text when the line ends, only so you can tell whether words like 'this' or 'on the left' point at something; the visuals are reviewed separately. Title and chapter cards are silent; they only mark scene changes.

## Cold open (before the title card)
- l01（8.1s / pause 0.3s）：Last time, we said a model is a machine with knobs, and learning means turning those knobs to the right spot.  [On screen: 「A model is a machine wit」]
- l02（6.5s / pause 0.3s）：But what does "right" even mean? How does the machine know this turn beat the last one?  [On screen: 「?」, 「Is this turn better?」]
- l03（3.5s / pause 0.4s）：The trick is to give its mistakes a score.  [On screen: a chart]
- l04（7.7s）：That score is called the loss, and the rule for working it out is the loss function. That's today's topic.  [On screen: 「Loss function」, 「损失函数」, a chart]

> [On screen: title card (series + episode title)]

> [On screen: chapter card “What is a loss function?”]

## What a loss function is
- l05（7.3s / pause 0.3s）：Every time the model guesses, it's a bit off from the real answer. How far off, that's the error.  [On screen: 「How far off = error」, a chart]
- l06（7.3s / pause 0.3s）：Roll all those errors up into one number, and that's the loss: a score for how wrong it is.  [On screen: 「17.9」, 「Errors → one score」, a chart]
- l07（6.5s / pause 0.3s）：It's the opposite of a test score: lower is better, and zero means not wrong at all.  [On screen: 「17.9」, 「Lower is better」, a chart]
- l08（3.5s / pause 0.3s）：Kind of like golf, where fewer strokes is better.  [On screen: 「17.9」, 「Lower is better」, a chart]
- l09（7.3s / pause 0.4s）：Now the machine can check itself. If a turn lowers the score, keep it. If not, turn it back.  [On screen: 「8.6」, 「Turn, then check」]
- l10（6.2s）：So training, put simply, is turning the knobs over and over to push that score down.  [On screen: 「2.2」, 「Training: push it down」]

> [On screen: chapter card “A small experiment”]

## A small experiment
- l11（8.1s / pause 0.3s）：Back to those twelve taxi rides from last time: distance along the bottom, fare up the side. The data's made up.  [On screen: a chart]
- l12（6.9s / pause 0.4s）：The model is still that straight line, with two knobs: the starting fare, and the price per kilometer.  [On screen: 「$0」, 「$0」, a chart]
- l13（6.9s / pause 0.4s）：First try: a five-dollar starting fare and two dollars a kilometer. The whole line sits too low.  [On screen: 「Try 1」, 「$5」, a chart]
- l14（8.1s / pause 0.4s）：Take the five-kilometer ride: it cost twenty-three dollars, the model guessed fifteen, so it's off by eight. That's the error.  [On screen: 「Try 1」, 「$5」, a chart]
- l15（4.6s / pause 0.4s）：Now square it: eight times eight is sixty-four. That's this red square.  [On screen: 「Try 1」, 「$5」, a chart]
- l16（5.4s / pause 0.4s）：Do that for all twelve rides, take the average, and this setting scores seventy-eight.  [On screen: 「78」, 「Try 1」, a chart]
- l17（8.5s / pause 0.4s）：Second try: four dollars to start and three fifty a kilometer. Too steep: too low on short rides, too high on long ones.  [On screen: 「Try 2: too steep」, 「$4」, a chart]
- l18（7.3s / pause 0.3s）：If we skipped the squaring and just averaged the errors, the too-lows and too-highs would cancel out.  [On screen: 「Try 2: too steep」, 「$4」, a chart]
- l19（6.2s / pause 0.4s）：The average is about minus thirty cents, so it looks like it's barely wrong at all.  [On screen: 「−0.33」, 「Try 2: too steep」, a chart]
- l20（5.0s / pause 0.3s）：That's why we square: once everything's squared, it's all positive, so nothing cancels.  [On screen: 「Squared: all positive」, 「$4」, a chart]
- l21（6.9s / pause 0.4s）：And bigger misses cost a lot more: off by two costs four, but off by eight costs sixty-four.  [On screen: 「Squared: all positive」, 「$4」, a chart]
- l22（3.8s / pause 0.4s）：Square, then average, and this setting scores thirteen point four.  [On screen: 「13.4」, 「Squared: all positive」, a chart]
- l23（5.0s / pause 0.3s）：This is called mean squared error, and it's the most common loss function.  [On screen: 「Mean squared error」, 「$4」, a chart]
- l24（10.0s / pause 0.3s）：Third try: ten dollars to start and two fifty a kilometer. The line hugs the points, the squares are tiny, and it scores two point one nine.  [On screen: 「2.19」, 「Try 3」, a chart]
- l25（5.0s / pause 0.4s）：The third has the lowest score, so it's the best of the three.  [On screen: 「Try 3」, 「$10」, a chart]
- l26（8.1s / pause 0.3s）：But that's only three tries. Score every possible setting of the two knobs, and you get a landscape map of scores.  [On screen: 「A map of scores」, 「$10」, a chart]
- l27（7.7s / pause 0.3s）：Starting fare along the bottom, price per kilometer up the side, and the darker the color, the higher the score.  [On screen: 「A map of scores」, 「$10」, a chart]
- l28（8.1s / pause 0.3s）：Our three tries: the first way up high, the second halfway down, the third nearly at the bottom of the valley.  [On screen: 「A map of scores」, 「$10」, a chart]
- l29（6.5s / pause 0.3s）：The lowest point is a starting fare of about ten twenty and two fifty-four a kilometer, scoring one point nine seven.  [On screen: 「1.97」, 「A map of scores」, a chart]
- l30（6.2s）：That's the best setting, and the whole job of training is to find that lowest point.  [On screen: 「1.97」, 「Find the lowest point」, a chart]

> [On screen: chapter card “The score is all it sees”]

## The score is all it sees
- l31（4.2s / pause 0.3s）：Here's something easy to miss: even the lowest point isn't zero.  [On screen: 「1.97」, 「Lowest ≠ 0」, a chart]
- l32（6.2s / pause 0.3s）：Real fares bounce around with traffic and detours, so no straight line could nail every ride.  [On screen: 「Lowest ≠ 0」, 「Traffic, detours: random」, a chart]
- l33（5.0s / pause 0.4s）：So training isn't chasing zero. It's chasing as low as it can get.  [On screen: 「Not zero, just lowest」, a chart]
- l34（7.7s / pause 0.4s）：And here's the other thing: the model has no idea what a taxi is. All it sees is the score.  [On screen: 「It only sees the score」, 「Doesn't know what a taxi」, a chart]
- l35（6.9s / pause 0.4s）：However you score it, that's how it learns. Because we squared the errors, it's terrified of big mistakes.  [On screen: 「Score it, shape it」, 「Squared: hates big misse」, a chart]
- l36（6.2s / pause 0.4s）：It would rather be a little off on every ride than way off on just one.  [On screen: 「Score it, shape it」, 「Squared: hates big misse」, a chart]
- l37（5.8s）：So when you pick a loss function, you're really telling the model what "good" means.  [On screen: 「The loss function / = wh」, a chart]

> [On screen: chapter card “How big models are scored”]

## How big models are scored
- l38（6.2s / pause 0.4s）：Big language models like ChatGPT get a score in training too. It's just scoring something different.  [On screen: 「Language models」, 「Scored in training, too」]
- l39（5.8s / pause 0.4s）：Their job is to guess the next word, like what comes after "Twinkle, twinkle, little."  [On screen: 「Twinkle, twinkle, little」]
- l40（8.8s / pause 0.4s）：The score looks at how confident the model was in the word that actually comes next. The less confident, the bigger the penalty.  [On screen: 「Twinkle, twinkle, little」, 「Less sure, bigger penalt」]
- l41（7.7s / pause 0.4s）：Give the right word ninety percent, and the penalty is tiny. Give it only ten percent, and it's way bigger.  [On screen: 「Twinkle, twinkle, little」, 「Less sure, bigger penalt」]
- l42（6.2s / pause 0.4s）：This kind of scoring is called cross-entropy. The name is all you need for now.  [On screen: 「Cross-entropy」, 「交叉熵」]
- l43（8.1s / pause 0.4s）：In twenty twenty-three, Meta trained a language model called Llama 2, and plotted this score as a curve. It kept going down.  [On screen: 「Llama 2」, 「Training loss keeps fall」, a chart]
- l44（6.2s / pause 0.4s）：The model read two trillion tokens of data. Tokens are roughly words or pieces of words.  [On screen: 「Llama 2」, 「Training loss keeps fall」, a chart]
- l45（5.8s / pause 0.4s）：And even then, the score was still falling, with no sign yet of a floor.  [On screen: 「Llama 2」, 「Training loss keeps fall」, a chart]
- l46（6.5s）：Tens of billions of knobs or just two, the job is the same: push that score down.  [On screen: 「Score ↓」, 「Score ↓」]

## Outro (on screen: end card)
- l47（6.5s / pause 0.4s）：So, a loss function is a score for how wrong the model is, and lower is better.
- l48（3.1s / pause 0.3s）：And training is just pushing that score down.
- l49（9.2s / pause 0.3s）：But with tons of knobs, that map gets so huge you can't see the edges. So which way do you turn to get down?
- l50（3.8s）：That's gradient descent, and that's where we're headed next time.

