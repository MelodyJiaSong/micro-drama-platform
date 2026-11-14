# Narration (in playback order)

Each line: id (spoken duration / pause after): exactly what the narrator says. [On screen: …] lists the most prominent on-screen text when the line ends, only so you can tell whether words like 'this' or 'on the left' point at something; the visuals are reviewed separately. Title and chapter cards are silent; they only mark scene changes.

## Cold open (before the title card)
- l01（6.2s / pause 0.4s）：You've probably seen it in the news: some big AI model has over a hundred billion parameters.  [On screen: 「100B+」, 「parameters」]
- l02（5.8s / pause 0.4s）：So what actually is a parameter? And what does it mean to have that many?  [On screen: 「100B+」, 「parameters」]
- l03（9.6s / pause 0.3s）：Last time, we saw that today's AI mostly figures out patterns on its own, from examples. What it ends up with is called a model.  [On screen: 「→」, 「A model」]
- l04（5.0s）：So this time, let's crack a model open and see what's really inside.  [On screen: 「?」, 「→」]

> [On screen: title card (series + episode title)]

> [On screen: chapter card “What a model looks like”]

## What a model looks like
- l05（7.7s / pause 0.3s）：A model is basically a machine: you feed an input in one end, and an answer comes out the other.  [On screen: 「Input」, 「Answer」]
- l06（8.5s / pause 0.4s）：And on this machine, there's a row of knobs. Turn them to different positions, and the same input gives a different answer.  [On screen: 「3」, 「9」]
- l07（1.9s / pause 0.4s）：Those knobs are the parameters.  [On screen: 「Parameters = knobs」, 「3」]
- l08（8.5s / pause 0.4s）：Here's an example: guessing a taxi fare. We put in the distance in kilometers, and out comes a guess at the price.  [On screen: 「Distance」, 「Fare」]
- l09（8.1s / pause 0.4s）：At its simplest, this machine needs just two knobs: one for the base fare, and one for the price per kilometer.  [On screen: 「Distance」, 「Fare」]
- l10（6.9s / pause 0.4s）：To make a guess, it takes the base fare and adds the per-kilometer price times the distance.  [On screen: 「Distance」, 「Fare」]
- l11（10.0s / pause 0.4s）：Say the base fare is set to ten dollars and the per-kilometer knob to two dollars. For a five-kilometer ride, it guesses twenty dollars.  [On screen: 「5 km」, 「$20」]
- l12（9.2s / pause 0.3s）：People decide how the machine does its math. But where each knob is set? Nobody types that in. The machine learns it from examples.  [On screen: 「5 km」, 「$20」]
- l13（4.2s）：That's all "learning" is: turning the knobs to the right positions.  [On screen: 「Learning = setting knobs」, 「5 km」]

> [On screen: chapter card “Let's turn the knobs”]

## Let's turn the knobs
- l14（5.8s / pause 0.4s）：Here are twelve made-up taxi rides, just for this example. They're not real receipts.  [On screen: 「Twelve taxi rides」, a chart]
- l15（7.7s / pause 0.3s）：Each dot is one ride: the further right, the longer the trip, and the higher up, the more it cost.  [On screen: 「Twelve taxi rides」, a chart]
- l16（6.5s / pause 0.3s）：Draw the model's guesses, and you get a straight line that gives a fare for every distance.  [On screen: 「$0.00」, 「$1.00」, a chart]
- l17（7.7s / pause 0.4s）：The little vertical line from each dot to that line shows how far off the guess was for that ride.  [On screen: 「$0.00」, 「$1.00」, a chart]
- l18（10.4s / pause 0.4s）：Let's start with the knobs set pretty much at random: zero base fare, a dollar per kilometer. The line's way too low, and every ride gets underestimated.  [On screen: 「$0.00」, 「$1.00」, a chart]
- l19（5.4s / pause 0.4s）：Turn the base fare up to ten dollars, and the whole line lifts up.  [On screen: 「$10.00」, 「$1.00」, a chart]
- l20（6.5s / pause 0.3s）：Now the short rides are pretty close, but the longer the ride, the further off it gets.  [On screen: 「$10.00」, 「$1.00」, a chart]
- l21（9.6s / pause 0.4s）：So turn the per-kilometer knob, and the line gets steeper. At three fifty a kilometer, we've gone too far: now the long rides are overestimated.  [On screen: 「$10.00」, 「$3.50」, a chart]
- l22（6.9s / pause 0.3s）：Back the per-kilometer knob off to about two fifty, and nudge the base fare to ten dollars twenty.  [On screen: 「$10.20」, 「$2.54」, a chart]
- l23（6.2s / pause 0.4s）：Now the line runs right along the dots, and all those little vertical lines are short.  [On screen: 「$10.20」, 「$2.54」, a chart]
- l24（6.9s / pause 0.3s）：Once it's tuned, you can actually use it. So ask it: what would an eight-kilometer ride cost?  [On screen: 「$10.20」, 「$2.54」, a chart]
- l25（7.3s）：None of our twelve rides was eight kilometers, but it can still make a guess: about thirty dollars fifty.  [On screen: 「$10.20」, 「$2.54」, a chart]

> [On screen: chapter card “What it learned”]

## What it learned
- l26（2.7s / pause 0.4s）：So what did this machine actually learn?  [On screen: 「$10.20」, 「$2.54」]
- l27（6.2s / pause 0.4s）：Everything it learned from those twelve rides comes down to where those two knobs are set.  [On screen: 「$10.20」, 「$2.54」]
- l28（6.9s / pause 0.4s）：The machine itself hasn't changed one bit. The only thing that's different is where the knobs are set.  [On screen: 「$10.20」, 「$2.54」]
- l29（8.1s / pause 0.4s）：Copy those two numbers onto a scrap of paper, hand it to a friend, and they've got the exact same model.  [On screen: 「$10.20」, 「$2.54」]
- l30（5.8s）：So when people talk about "training a model," what they're really doing is turning knobs.  [On screen: 「Training = turning knobs」]

> [On screen: chapter card “Billions of knobs”]

## Billions of knobs
- l32（10.4s / pause 0.4s）：Two knobs are plenty for guessing a taxi fare. But if you want a model to write essays or chat with people, you need way, way more.  [On screen: 「Chatting takes far more 」]
- l33（4.2s / pause 0.3s）：In twenty twenty, OpenAI released G P T three, which has a hundred and seventy-five billion parameters.  [On screen: 「175,000,000,000」, 「Brown et al. · OpenAI · 」]
- l34（1.5s / pause 0.3s）：That's a hundred and seventy-five billion knobs.  [On screen: 「175,000,000,000」, 「= 175 billion knobs」]
- l35（10.0s / pause 0.4s）：How many is that? Read out one knob setting every second, no eating, no sleeping, and it'd take you over five and a half thousand years.  [On screen: 「≈ 5,545 years」, 「One reading per second」]
- l36（6.9s / pause 0.4s）：Obviously, nobody turned all those knobs by hand. Their settings came from training on huge amounts of text.  [On screen: 「Set by training, not by 」]
- l37（10.0s / pause 0.4s）：But the idea is the same as with the taxi fare: people decide how the machine does its math, and the settings are learned from examples.  [On screen: 「Set by training, not by 」, 「The mathby people」]
- l38（6.9s / pause 0.3s）：And a trained model, saved to a file, is mostly just this long, long list of knob settings.  [On screen: 「Model file = knob settin」, 「1.1958 −0.7341 0.5973 −0」]
- l39（6.9s）：So when the news says "over a hundred billion parameters," it means the machine has over a hundred billion knobs.  [On screen: 「100B parameters = 100B k」]

## Outro (on screen: end card)
- l40（3.5s / pause 0.3s）：In short, a model is a machine with knobs.
- l41（4.2s / pause 0.4s）：And learning just means turning the knobs to the right positions.
- l42（3.1s / pause 0.3s）：But what does "the right positions" actually mean?
- l43（8.1s / pause 0.4s）：Remember those little vertical lines, some long, some short? So how do you tell a good setting from a bad one?
- l44（3.5s）：That's next time, when we talk about loss functions.

