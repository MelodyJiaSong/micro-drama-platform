# t13 Backpropagation · English narrator first draft

## s0 Cold open
- l01: Today's big AI models have billions of knobs, some hundreds of billions.
- l02: Every step of training, you need to know which way each knob should turn, and how far.
- l03: Testing them one at a time would never finish. The real trick takes one trip backward. It's called backpropagation.

## s1 In this episode
- l04: Last time: a neural network is layers of small units, each with knobs.
- l05: Today: why testing knobs one by one breaks down, and how the error flows backward through a tiny network.

## s2 Too many knobs to try
- l06: Here's training. The model guesses, we compare with the right answer, and the gap is the error.
- l07: The loss is a score for how wrong it is. Further off, higher score.
- l08: Training is turning the knobs to push that score down.
- l09: So each step, you want the gradient: which way each knob should turn to drop the error fastest. The slope.
- l10: The obvious way? Nudge one knob, rerun everything, see if the error went up or down.
- l11: One full rerun per knob. Billions of knobs, billions of reruns. For a single step.

## s3 Working backward
- l12: Backpropagation works from the other end. Picture a chain of gears, with a pointer on the last one.
- l13: Turn the first gear one notch, the second turns {2|two}. One notch on the second, the third turns {3|three}.
- l14: So how far does the pointer move? Multiply along the way: {2 × 3|two times three}. {6|Six} notches.
- l15: It's easiest to start at the pointer and walk back, multiplying in one ratio per gear.
- l16: Each gear handles only its own link and reuses what's already done. Nothing is recalculated.
- l17: A neural network is a chain like this. Every knob drives the final answer through a few layers. So the error can flow back.

## s4 A small experiment
- l18: Here's a real, tiny network. Two layers, {7|seven} knobs.
- l19: The input is a taxi ride: {5|five} kilometers. Units A and B, two knobs each, turn that into {6|six} and {4|four}.
- l20: The second layer weights each by a knob, adds one more, and guesses: {29|twenty-nine} yuan.
- l21: The real fare was {23|twenty-three}. {6|Six} too high. That six is the error we pass back.
- l22: Last layer first. Each knob's blame is the error times what's fed into it: {36|thirty-six}, {24|twenty-four}, {6|six}.
- l23: Bigger number in, bigger blame.
- l24: One layer back, the error is multiplied by the knob it crosses. Times {2|two} gives A {12|twelve}. Times {1|one} gives B {6|six}.
- l25: Each unit splits its share between its two knobs: {60|sixty}, {12|twelve}, {30|thirty}, {6|six}.
- l26: One trip back, and all seven knobs have a number. The guess was high, so all turn down, some more than others.
- l27: Turn each a small step and guess again. {29|Twenty-nine} becomes {23.88|about twenty-four}. Much closer.
- l28: The slow way took {8|eight} forward runs: one untouched, plus one per knob. Same seven numbers, exactly.
- l29: Backpropagation needed one run forward and one trip back.
- l30: Scale up to a billion knobs, and the slow way is {1,000,000,001|a billion and one} runs.
- l31: Even at one second a run, that's over {31.7|thirty} years. For one step.
- l32: Backpropagation stays one forward, one back. Roughly {3|three} runs' worth. Without it, billion-knob models couldn't be trained.

## s5 From 1986 to today
- l33: In {1986|nineteen eighty-six}, a Nature paper by Rumelhart, Hinton and Williams laid this out clearly.
- l34: Each connection's slope comes in two passes: forward, then backward from the top layer.
- l35: They also found the hidden units come to represent important features of the task.
- l36: Similar methods came earlier. This paper showed them training multi-layer networks.
- l37: Today in PyTorch, one line, {loss.backward()|loss dot backward}, gives every knob its slope.
- l38: That's automatic differentiation. Underneath, it's backpropagation: walking back from the output, collecting slopes.
- l39: Every training step is this: guess forward, pass the blame back, turn every knob a little.

## s6 Ending
- l40: Backpropagation is passing the blame backward, from the output, layer by layer.
- l41: One trip back, and every knob knows which way to turn, and how far.
- l42: But lots of knobs bring trouble. A model can memorize the practice questions and flunk a new one.
- l43: That's overfitting, and it's up next.
