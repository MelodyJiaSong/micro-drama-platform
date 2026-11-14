# t13 Backpropagation — narration (English)

v1.3 (2026-11-09, per lines_r3 judge final wording: l09, l23, l25, l26; l27 subject restored; after voice QA: l19 "a six and a four", l39 "a single line" so the speech check no longer misreads them). v1.2 (2026-11-09, per lines_r2 judges: l04, l06 one preview, l09 slope per knob / gradient together, l20 'a seventh knob', l22 no interruption, l23 the seventh knob's input is one, l25, l35, l40 trimmed; l17 split, l18 says it guesses fares, l19, l28, l39). v1.1 (2026-11-09, per lines_r1 judges: l04, l12 'starts at the answer', l13, l15–l17, A/B named in l19, l22–l23 blame = slope with inputs 6/4/1, l26, we-voice in l28–l29, l33 'about two runs', l34, l35 bridge, l36–l39, l43). v1 (2026-11-09): spoken first by a native narrator from `drafts/v1_brief.md` (`drafts/v1_en.md`); the author only trimmed, regrouped lines to match `script.md`, and checked facts and caveats. Segment, line ids and tags match `script.md`.

## s0 Cold open [冷开场]
- l01: Today's big AI models have billions of knobs, some hundreds of billions.
- l02: Every step of training, you need to know which way each knob should turn, and how far.
- l03: You'd never finish testing them one at a time.
- l04: The real trick? One trip backward tells you how to turn every knob. It's called backpropagation.

## s1 In this episode [包装:agenda]
- l05: Last time we saw that a neural network is layers of small units, each with its own knobs.
- l06: This time, we'll build a tiny network and watch the error run backward through it, knob by knob.

## s2 Too many knobs to try [章:problem]
- l07: In training, the model makes a guess, we compare it with the right answer, and the gap is the error.
- l08: The loss is a score for how wrong it is. Training is turning the knobs to push that score down.
- l09: Each knob's slope tells you which way to turn, and how far. All the slopes together are the gradient.
- l10: The obvious way? Nudge one knob, rerun everything, and see if the error went up or down.
- l11: One full rerun per knob. Billions of knobs, billions of reruns. For a single step.

## s3 Working backward [章:analogy]
- l12: Backpropagation starts at the answer instead. Picture a chain of gears, with a pointer on the last one.
- l13: Turn the first gear one notch, and the second turns {2|two}. Turn the second one notch, and the third turns {3|three}.
- l14: So how far does the pointer move? Multiply along the way: {2 × 3|two times three}. {6|Six} notches.
- l15: So start at the pointer and work backward, multiplying by each gear's ratio as you go.
- l16: At each gear you multiply once and reuse what you already have. Nothing gets redone.
- l17: A neural network is a chain like this. Each knob affects the answer through the layers after it. So the error can flow back the same way.

## s4 A small experiment [章:experiment]
- l18: Here's a real, tiny network: two layers, {7|seven} knobs. It guesses taxi fares. We give it a {5|five}-kilometer ride.
- l19: In the first layer, two units, A and B, use two knobs each to turn the five into a {6|six} and a {4|four}.
- l20: The second layer multiplies each by a knob, adds a seventh knob, and guesses: {29|twenty-nine} yuan.
- l21: The real fare was {23|twenty-three}. {6|Six} too high. That six is the error we pass back.
- l22: Last layer first. A knob's blame is the error times the number fed into it. That's its slope.
- l23: So: {6 × 6|six times six}, {36|thirty-six}. {6 × 4|Six times four}, {24|twenty-four}. And the seventh knob's input is {1|one}, so {6|six}. Bigger input, bigger blame.
- l24: One layer back, the error flows along the wires and gets multiplied by each knob it passes.
- l25: For A, the error times {2|two}: {12|twelve}. For B, times {1|one}: {6|six}.
- l26: For their own two knobs, it's error times input again.
- l27: One trip back, and all seven knobs have a number. We guessed high, so they all turn down, some more than others.
- l28: We turn each knob down a little and guess again. {29|Twenty-nine} becomes about {24|twenty-four}. Much closer.
- l29: We checked the slow way too: one run with nothing changed, then one per nudged knob. {8|Eight} runs.
- l30: Same seven numbers, exactly. Backpropagation needed just one run forward and one trip back.
- l31: Scale up to a billion knobs, and the slow way is {1,000,000,001|a billion and one} runs.
- l32: Even at one second a run, that's over {30|thirty} years. For one step.
- l33: Backpropagation is still one trip each way. The trip back costs about two runs, so roughly {3|three} in all.
- l34: Without it, nobody could train these models.

## s5 From 1986 to today [章:real]
- l35: So where does this come from? In {1986|nineteen eighty-six}, Rumelhart, Hinton and Williams laid it out in the journal Nature.
- l36: They found each knob's slope in two passes: forward, then back from the output.
- l37: They also found that the units in the middle learn to pick up useful patterns on their own.
- l38: Others had similar ideas earlier. This paper showed the method working on networks with several layers.
- l39: Today, in PyTorch, a popular tool for building models, a single line does it: {loss.backward()|loss dot backward}. Every knob gets its slope.
- l40: That's automatic differentiation. Underneath, it's backpropagation.

## s6 Ending [包装:outro]
- l41: Backpropagation is passing the blame backward, from the output, layer by layer.
- l42: One trip back, and every knob knows which way to turn, and how far.
- l43: But with so many knobs, a model can memorize the practice questions and get new ones wrong.
- l44: That's overfitting, and it's up next.
