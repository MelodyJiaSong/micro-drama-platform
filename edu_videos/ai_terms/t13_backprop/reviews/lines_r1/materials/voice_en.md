# Narration (in playback order)

Each line: id (spoken duration / pause after): exactly what the narrator says. [On screen: …] lists the most prominent on-screen text when the line ends, only so you can tell whether words like 'this' or 'on the left' point at something; the visuals are reviewed separately. Title and chapter cards are silent; they only mark scene changes.

## Cold open (before the title card)
- l01（4.6s / pause 0.4s）：Today's big AI models have billions of knobs, some hundreds of billions.  [On screen: 「Billions of knobs」]
- l02（6.5s / pause 0.4s）：Every step of training, you need to know which way each knob should turn, and how far.  [On screen: 「Every step: which way, h」]
- l03（3.5s / pause 0.4s）：Testing them one at a time would never finish.  [On screen: 「One by one? Never ends」, 「Tried 9」]
- l04（5.0s）：The real trick gets them all in one trip backward. It's called backpropagation.  [On screen: 「Backpropagation」]

> [On screen: title card (series + episode title)]

## What's coming (on screen: agenda card)
- l05（6.9s / pause 0.4s）：Last time we saw that a neural network is layers of small units, each with its own knobs.
- l06（8.5s）：This time, we'll see why testing knobs one by one breaks down, then watch the error flow backward through a tiny network.

> [On screen: chapter card “Too many knobs to try”]

## Too many knobs to try
- l07（6.9s / pause 0.4s）：Here's training: the model guesses, we compare it with the right answer, and the gap is the error.  [On screen: 「The gap = error」, a chart]
- l08（7.7s / pause 0.3s）：The loss is a score for how wrong it is. Training is turning the knobs to push that score down.  [On screen: 「Training: lower the loss」, a chart]
- l09（7.7s / pause 0.3s）：So each step, you want the gradient: which way each knob should turn to drop the error fastest. The slope.  [On screen: 「↻」, 「↺」, a chart]
- l10（6.5s / pause 0.4s）：The obvious way? Nudge one knob, rerun everything, and see if the error went up or down.  [On screen: 「3」, 「The slow way」]
- l11（5.8s）：One full rerun per knob. Billions of knobs, billions of reruns. For a single step.  [On screen: 「Billions」, 「The slow way」]

> [On screen: chapter card “Working backward”]

## Working backward
- l12（6.9s / pause 0.4s）：Backpropagation works from the other end. Picture a chain of gears, with a pointer on the last one.  [On screen: 「A chain of gears」, a chart]
- l13（7.3s / pause 0.4s）：Turn the first gear one notch, the second turns two. One notch on the second, the third turns three.  [On screen: 「A chain of gears」, a chart]
- l14（6.2s / pause 0.4s）：So how far does the pointer move? Multiply along the way: two times three. Six notches.  [On screen: 「2 × 3 = 6」, 「How far does it go?」, a chart]
- l15（6.2s / pause 0.4s）：It's easiest to start at the pointer and walk back, multiplying in one ratio per gear.  [On screen: 「Backward: one step each」, a chart]
- l16（5.8s / pause 0.4s）：Each gear handles only its own link and reuses what's already done. Nothing is recalculated.  [On screen: 「Backward: one step each」, 「Reuse what’s done」, a chart]
- l17（9.2s）：A neural network is a chain like this. Every knob drives the final answer through a few layers. So the error can flow back.  [On screen: 「Networks work the same」, 「Knob → layers → answer」, a chart]

> [On screen: chapter card “A small experiment”]

## A small experiment
- l18（6.5s / pause 0.4s）：Here's a real, tiny network. Two layers, seven knobs. The input is a taxi ride: five kilometers.  [On screen: 「5」, 「×2」]
- l19（6.5s / pause 0.4s）：In the first layer, units A and B use two knobs each to turn that into six and four.  [On screen: 「5」, 「6」]
- l20（5.8s / pause 0.3s）：The second layer weights each by a knob, adds one more, and guesses: twenty-nine yuan.  [On screen: 「5」, 「29」]
- l21（6.2s / pause 0.4s）：The real fare was twenty-three. Six too high. That six is the error we pass back.  [On screen: 「5」, 「29」]
- l22（6.5s / pause 0.4s）：Last layer first. Each knob's blame is the error times what's fed into it: thirty-six, twenty-four, six.  [On screen: 「5」, 「29」]
- l23（1.9s / pause 0.4s）：Bigger number in, bigger blame.  [On screen: 「5」, 「29」]
- l24（4.6s / pause 0.4s）：One layer back, the error is multiplied by the knob it crosses.  [On screen: 「5」, 「29」]
- l25（3.8s / pause 0.4s）：Times two gives A twelve. Times one gives B six.  [On screen: 「5」, 「29」]
- l26（5.4s / pause 0.4s）：Each unit then splits its share between its own two knobs, the same way.  [On screen: 「5」, 「29」]
- l27（8.5s / pause 0.4s）：One trip back, and all seven knobs have a number. The guess was high, so all turn down, some more than others.  [On screen: 「5」, 「29」]
- l28（5.4s / pause 0.3s）：Turn each a small step and guess again. Twenty-nine becomes about twenty-four. Much closer.  [On screen: 「5」, 「One small step: closer」]
- l29（6.5s / pause 0.4s）：Now check it the slow way. That took eight forward runs: one untouched, plus one per knob.  [On screen: 「8」, 「Check: two ways」]
- l30（5.4s / pause 0.4s）：Same seven numbers, exactly. Backpropagation needed just one run forward and one trip back.  [On screen: 「8」, 「1 forward + 1 back」]
- l31（6.2s / pause 0.3s）：Scale up to a billion knobs, and the slow way is a billion and one runs.  [On screen: 「1,000,000,001runs」, 「A billion knobs」]
- l32（5.0s / pause 0.4s）：Even at one second a run, that's over thirty years. For one step.  [On screen: 「1,000,000,001runs」, 「≈ 31.7years, for one ste」]
- l33（3.8s / pause 0.3s）：Backpropagation stays one forward, one back. Roughly three runs' worth.  [On screen: 「1,000,000,001runs」, 「≈ 31.7years, for one ste」]
- l34（3.1s）：Without it, billion-knob models couldn't be trained.  [On screen: 「1,000,000,001runs」, 「≈ 31.7years, for one ste」]

> [On screen: chapter card “From 1986 to today”]

## From 1986 to today
- l35（5.4s / pause 0.3s）：In nineteen eighty-six, a Nature paper by Rumelhart, Hinton and Williams laid this out clearly.  [On screen: 「1986」, 「Learning representations」]
- l36（7.3s / pause 0.4s）：In the paper, each connection's slope is worked out in two passes: forward, then backward from the top layer.  [On screen: 「1986」, 「Learning representations」]
- l37（5.8s / pause 0.3s）：They also found that the units in the middle learn useful features on their own.  [On screen: 「1986」, 「Learning representations」]
- l38（6.2s / pause 0.3s）：Similar methods had been proposed earlier. This paper showed it could train networks with several layers.  [On screen: 「1986」, 「Learning representations」]
- l39（5.0s / pause 0.4s）：Today in PyTorch, one line, loss dot backward, gives every knob its slope.  [On screen: 「loss.backward()」, 「loss」]
- l40（5.0s）：That's automatic differentiation. Underneath, it's backpropagation: walking back from the output, collecting slopes.  [On screen: 「loss.backward()」, 「loss」]

## Outro (on screen: end card)
- l41（4.6s / pause 0.4s）：Backpropagation is passing the blame backward, from the output, layer by layer.
- l42（5.4s / pause 0.4s）：One trip back, and every knob knows which way to turn, and how far.
- l43（6.9s / pause 0.4s）：But lots of knobs bring trouble. A model can memorize the practice questions and flunk a new one.
- l44（2.3s）：That's overfitting, and it's up next.

