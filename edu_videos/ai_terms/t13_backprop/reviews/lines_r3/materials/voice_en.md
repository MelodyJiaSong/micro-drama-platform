# Narration (in playback order)

Each line: id (spoken duration / pause after): exactly what the narrator says. [On screen: …] lists the most prominent on-screen text when the line ends, only so you can tell whether words like 'this' or 'on the left' point at something; the visuals are reviewed separately. Title and chapter cards are silent; they only mark scene changes.

## Cold open (before the title card)
- l01（4.6s / pause 0.4s）：Today's big AI models have billions of knobs, some hundreds of billions.  [On screen: 「Billions of knobs」]
- l02（6.5s / pause 0.4s）：Every step of training, you need to know which way each knob should turn, and how far.  [On screen: 「Which way? How far?」]
- l03（3.5s / pause 0.4s）：You'd never finish testing them one at a time.  [On screen: 「One at a time? Never fin」, 「9 tested」]
- l04（6.2s）：The real trick? One trip backward tells you how to turn every knob. It's called backpropagation.  [On screen: 「Backpropagation」]

> [On screen: title card (series + episode title)]

## What's coming (on screen: agenda card)
- l05（6.9s / pause 0.4s）：Last time we saw that a neural network is layers of small units, each with its own knobs.
- l06（6.9s）：This time, we'll build a tiny network and watch the error run backward through it, knob by knob.

> [On screen: chapter card “Too many knobs to try”]

## Too many knobs to try
- l07（7.7s / pause 0.3s）：In training, the model makes a guess, we compare it with the right answer, and the gap is the error.  [On screen: 「The gap = error」, a chart]
- l08（7.7s / pause 0.3s）：The loss is a score for how wrong it is. Training is turning the knobs to push that score down.  [On screen: 「Training: lower the loss」, a chart]
- l09（7.7s / pause 0.4s）：For each knob, which way to turn and how far is its slope. All the slopes together are the gradient.  [On screen: 「↻」, 「↺」, a chart]
- l10（6.5s / pause 0.3s）：The obvious way? Nudge one knob, rerun everything, and see if the error went up or down.  [On screen: 「3」, 「The slow way」]
- l11（5.8s）：One full rerun per knob. Billions of knobs, billions of reruns. For a single step.  [On screen: 「Billions」, 「The slow way」]

> [On screen: chapter card “Working backward”]

## Working backward
- l12（6.9s / pause 0.4s）：Backpropagation starts at the answer instead. Picture a chain of gears, with a pointer on the last one.  [On screen: 「A chain of gears」, a chart]
- l13（8.1s / pause 0.4s）：Turn the first gear one notch, and the second turns two. Turn the second one notch, and the third turns three.  [On screen: 「A chain of gears」, a chart]
- l14（6.2s / pause 0.3s）：So how far does the pointer move? Multiply along the way: two times three. Six notches.  [On screen: 「2 × 3 = 6」, 「How far does it go?」, a chart]
- l15（6.2s / pause 0.4s）：So start at the pointer and work backward, multiplying by each gear's ratio as you go.  [On screen: 「Backward, gear by gear」, a chart]
- l16（5.8s / pause 0.4s）：At each gear you multiply once and reuse what you already have. Nothing gets redone.  [On screen: 「Backward, gear by gear」, 「Reuse results」, a chart]
- l17（10.4s）：A neural network is a chain like this. Each knob affects the answer through the layers after it. So the error can flow back the same way.  [On screen: 「Networks work like gears」, 「Knob → layers → answer」, a chart]

> [On screen: chapter card “A small experiment”]

## A small experiment
- l18（7.7s / pause 0.3s）：Here's a real, tiny network: two layers, seven knobs. It guesses taxi fares. We give it a five-kilometer ride.  [On screen: 「5」, 「×2」]
- l19（7.3s / pause 0.4s）：In the first layer, two units, A and B, use two knobs each to turn the five into six and four.  [On screen: 「5」, 「6」]
- l20（6.2s / pause 0.3s）：The second layer multiplies each by a knob, adds a seventh knob, and guesses: twenty-nine yuan.  [On screen: 「5」, 「29」]
- l21（6.2s / pause 0.4s）：The real fare was twenty-three. Six too high. That six is the error we pass back.  [On screen: 「5」, 「29」]
- l22（6.9s / pause 0.4s）：Last layer first. A knob's blame is the error times the number fed into it. That's its slope.  [On screen: 「5」, 「29」]
- l23（8.1s / pause 0.4s）：The inputs are six, four, and for the seventh knob, one. So the blame is thirty-six, twenty-four and six. Bigger input, bigger blame.  [On screen: 「5」, 「29」]
- l24（6.5s / pause 0.4s）：One layer back, the error flows along the wires and gets multiplied by each knob it passes.  [On screen: 「5」, 「Going back: error × knob」]
- l25（4.6s / pause 0.3s）：For A, the knob is two: twelve. For B, it's one: six.  [On screen: 「5」, 「Going back: error × knob」]
- l26（4.2s / pause 0.4s）：Each unit then does the same for its own two knobs.  [On screen: 「5」, 「Blame = error × input」]
- l27（8.5s / pause 0.4s）：One trip back, and all seven knobs have a number. The guess was high, so all turn down, some more than others.  [On screen: 「5」, 「Guess too high → all tur」]
- l28（6.2s / pause 0.3s）：We turn each knob down a little and guess again. Twenty-nine becomes about twenty-four. Much closer.  [On screen: 「5」, 「One step: 29 → 23.88」]
- l29（6.9s / pause 0.4s）：We checked the slow way too: one run with nothing changed, then one per nudged knob. Eight runs.  [On screen: 「8」, 「forward runs」]
- l30（5.4s / pause 0.3s）：Same seven numbers, exactly. Backpropagation needed just one run forward and one trip back.  [On screen: 「8」, 「1 forward + 1 back」]
- l31（6.2s / pause 0.4s）：Scale up to a billion knobs, and the slow way is a billion and one runs.  [On screen: 「1,000,000,001runs」, 「A billion knobs」]
- l32（5.0s / pause 0.3s）：Even at one second a run, that's over thirty years. For one step.  [On screen: 「1,000,000,001runs」, 「A billion knobs」]
- l33（7.3s / pause 0.3s）：Backpropagation is still one trip each way. The trip back costs about two runs, so roughly three in all.  [On screen: 「1,000,000,001runs」, 「≈ 3runs’ worth」]
- l34（2.7s）：Without it, nobody could train these models.  [On screen: 「1,000,000,001runs」, 「≈ 3runs’ worth」]

> [On screen: chapter card “From 1986 to today”]

## From 1986 to today
- l35（7.3s / pause 0.3s）：So where does this come from? In nineteen eighty-six, Rumelhart, Hinton and Williams laid it out in the journal Nature.  [On screen: 「1986」, 「Learning representations」]
- l36（5.4s / pause 0.4s）：They found each knob's slope in two passes: forward, then back from the output.  [On screen: 「1986」, 「Learning representations」]
- l37（6.9s / pause 0.4s）：They also found that the units in the middle learn to pick up useful patterns on their own.  [On screen: 「1986」, 「Learning representations」]
- l38（6.2s / pause 0.3s）：Others had similar ideas earlier. This paper showed the method working on networks with several layers.  [On screen: 「1986」, 「Learning representations」]
- l39（8.1s / pause 0.4s）：Today, in PyTorch, a popular tool for building models, one line does it: loss dot backward. Every knob gets its slope.  [On screen: 「loss.backward()」, 「loss」]
- l40（2.3s）：That's automatic differentiation. Underneath, it's backpropagation.  [On screen: 「loss.backward()」, 「loss」]

## Outro (on screen: end card)
- l41（4.6s / pause 0.4s）：Backpropagation is passing the blame backward, from the output, layer by layer.
- l42（5.4s / pause 0.4s）：One trip back, and every knob knows which way to turn, and how far.
- l43（6.5s / pause 0.3s）：But with so many knobs, a model can memorize the practice questions and get new ones wrong.
- l44（2.3s）：That's overfitting, and it's up next.

