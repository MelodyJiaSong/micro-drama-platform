# voice_en__a report (round 3, blind, ear only)

## 评分表
- V1 2 证据：Most lines pass the friend test (l07 "the model makes a guess, we compare it with the right answer, and the gap is the error"; l10 "The obvious way? Nudge one knob, rerun everything"). Small off spots: l09 "which way to turn and how far is its slope" (clause as subject), l15 "each gear's ratio", l20 "adds a seventh knob", l40 "automatic differentiation".
- V2 2 证据：Cold open l01-l04 flows (l04 "The real trick?" answers l03 and echoes l10 "The obvious way?"). Agenda l05-l06 is one sentence of purpose, no list. Hand-offs l11 to l12 and l34 to l35 ("So where does this come from?") work. Slight bump: l26 "does the same" after the two-step l24-l25.
- V3 2 证据：Terms are set up before use mostly (loss l08, gradient l09). Weak spots: l09 gives "slope" and "gradient" back to back; l23 carries six, four, one, thirty-six, twenty-four, six in one breath; l33 "roughly three in all" (three what?) can be misheard as three trips; l40 "automatic differentiation" has no gloss.
- V4 2 证据：l41 "Backpropagation is passing the blame backward, from the output, layer by layer." and l42 "One trip back, and every knob knows which way to turn, and how far." both recap, and l42 repeats l02/l04 wording; one could go. l16 "Nothing gets redone." restates the first half. Otherwise tight.
- V5 2 证据：One warm narrator throughout; good short punches (l11 "For a single step.", l32 "For one step."). l17 (10.4s, three sentences) and l23 (8.1s, number list) are heavy for one breath; l19 "In the first layer, two units, A and B, use two knobs each to turn the five into six and four." is dense.
- V6 2 证据：Every flagged line has a drop-in rewrite below, none longer than the original. Top 5 most awkward: l09, l19, l26, l33, l40.
- R 3 证据：Previous voice_en items re-checked. I78 l01 (author kept "some hundreds of billions"): reasoning holds, it reads as normal speech. I79 l04 now "The real trick? One trip backward tells you how to turn every knob." solved. I80 l06 now one plain "build a tiny network and watch the error run backward" solved, no list. I94 l22 and I95/I96 l23 solved ("Bigger input, bigger blame" helps). I98/I99 l25 "For A, the knob is two: twelve." now clear, minor only. I100 l26 kept: still slightly ambiguous but acceptable (suggestion only, author reasoning holds). I101 l28 solved. I103 l35 solved. I105/I106 l39 solved. I107 l40 solved, no more collision with l41. I108 l41 kept as natural wrap-up; I agree, though it overlaps l42 (recorded below). No new problems introduced by the fixes.

## 逐句复述
| 句号 | 原句 | 跟朋友会怎么说 | 判 |
|---|---|---|---|
| l01 | Today's big AI models have billions of knobs, some hundreds of billions. | Big AI models have billions of knobs, some even hundreds of billions. | natural |
| l02 | Every step of training, you need to know which way each knob should turn, and how far. | At every training step you've got to know which way to turn each knob, and by how much. | natural |
| l03 | You'd never finish testing them one at a time. | You'd never finish if you tested them one by one. | natural |
| l04 | The real trick? One trip backward tells you how to turn every knob. It's called backpropagation. | The trick is, one trip backward tells you how to turn every knob. It's called backpropagation. | natural |
| l05 | Last time we saw that a neural network is layers of small units, each with its own knobs. | Last time we saw a neural network is layers of little units, each with its own knobs. | natural |
| l06 | This time, we'll build a tiny network and watch the error run backward through it, knob by knob. | Today we'll build a tiny network and watch the error run backward through it. | natural |
| l07 | In training, the model makes a guess, we compare it with the right answer, and the gap is the error. | While training, the model guesses, we check it against the right answer, and the gap is the error. | natural |
| l08 | The loss is a score for how wrong it is. Training is turning the knobs to push that score down. | The loss is just a score for how wrong it is. Training means turning knobs to bring it down. | natural |
| l09 | For each knob, which way to turn and how far is its slope. All the slopes together are the gradient. | For each knob, the slope says which way to turn it and how far. Put all the slopes together and you get the gradient. | a bit off |
| l10 | The obvious way? Nudge one knob, rerun everything, and see if the error went up or down. | The obvious way is nudge one knob, rerun everything, see if the error went up or down. | natural |
| l11 | One full rerun per knob. Billions of knobs, billions of reruns. For a single step. | One full rerun per knob. So billions of reruns, just for one step. | natural |
| l12 | Backpropagation starts at the answer instead. Picture a chain of gears, with a pointer on the last one. | Backprop starts from the answer instead. Picture a chain of gears with a pointer on the last one. | natural |
| l13 | Turn the first gear one notch, and the second turns two. Turn the second one notch, and the third turns three. | Turn gear one a notch and gear two moves two. Turn gear two a notch and gear three moves three. | natural |
| l14 | So how far does the pointer move? Multiply along the way: two times three. Six notches. | So how far does the pointer move? Just multiply: two times three, six notches. | natural |
| l15 | So start at the pointer and work backward, multiplying by each gear's ratio as you go. | So you start at the pointer and go backward, multiplying at each gear. | a bit off |
| l16 | At each gear you multiply once and reuse what you already have. Nothing gets redone. | At each gear you multiply once and reuse what you've already got. | natural |
| l17 | A neural network is a chain like this. Each knob affects the answer through the layers after it. So the error can flow back the same way. | A network is a chain like this. Each knob affects the answer through the layers after it, so the error can flow back the same way. | natural |
| l18 | Here's a real, tiny network: two layers, seven knobs. It guesses taxi fares. We give it a five-kilometer ride. | Here's a tiny network, two layers, seven knobs. It guesses taxi fares. We give it a five-kilometer ride. | natural |
| l19 | In the first layer, two units, A and B, use two knobs each to turn the five into six and four. | The first layer has two units, A and B, with two knobs each. They turn the five into a six and a four. | a bit off |
| l20 | The second layer multiplies each by a knob, adds a seventh knob, and guesses: twenty-nine yuan. | The second layer multiplies each one by a knob, adds the last knob, and guesses twenty-nine yuan. | a bit off |
| l21 | The real fare was twenty-three. Six too high. That six is the error we pass back. | The real fare was twenty-three, so it's six too high. That six is the error we pass back. | natural |
| l22 | Last layer first. A knob's blame is the error times the number fed into it. That's its slope. | Last layer first. A knob's blame is the error times whatever went into it. That's its slope. | natural |
| l23 | The inputs are six, four, and for the seventh knob, one. So the blame is thirty-six, twenty-four and six. Bigger input, bigger blame. | The inputs are six and four, and one for the last knob. So the blame is thirty-six, twenty-four, six. Bigger input, bigger blame. | natural |
| l24 | One layer back, the error flows along the wires and gets multiplied by each knob it passes. | Going one layer back, the error flows along the wires and gets multiplied by each knob it passes. | natural |
| l25 | For A, the knob is two: twelve. For B, it's one: six. | For A the knob is two, so twelve. For B it's one, so six. | a bit off |
| l26 | Each unit then does the same for its own two knobs. | Then each unit does the same thing for its own two knobs. | a bit off |
| l27 | One trip back, and all seven knobs have a number. The guess was high, so all turn down, some more than others. | One trip back and all seven knobs have a number. The guess was too high, so they all turn down, some more than others. | natural |
| l28 | We turn each knob down a little and guess again. Twenty-nine becomes about twenty-four. Much closer. | We turn each knob down a bit and guess again. Twenty-nine drops to about twenty-four. Much closer. | natural |
| l29 | We checked the slow way too: one run with nothing changed, then one per nudged knob. Eight runs. | We also checked the slow way: one run unchanged, then one per nudged knob. Eight runs. | natural |
| l30 | Same seven numbers, exactly. Backpropagation needed just one run forward and one trip back. | Same seven numbers, exactly. Backprop needed just one run forward and one trip back. | natural |
| l31 | Scale up to a billion knobs, and the slow way is a billion and one runs. | Scale up to a billion knobs and the slow way takes a billion and one runs. | natural |
| l32 | Even at one second a run, that's over thirty years. For one step. | Even at a second a run, that's over thirty years. For one step. | natural |
| l33 | Backpropagation is still one trip each way. The trip back costs about two runs, so roughly three in all. | Backprop is still one trip each way. The trip back costs about two runs' worth, so about three runs' worth in total. | a bit off |
| l34 | Without it, nobody could train these models. | Without it, nobody could train these models. | natural |
| l35 | So where does this come from? In nineteen eighty-six, Rumelhart, Hinton and Williams laid it out in the journal Nature. | So where's this from? In 1986, Rumelhart, Hinton and Williams published it in Nature. | natural |
| l36 | They found each knob's slope in two passes: forward, then back from the output. | They got each knob's slope in two passes: forward, then back from the output. | natural |
| l37 | They also found that the units in the middle learn to pick up useful patterns on their own. | They also showed the units in the middle learn useful patterns by themselves. | natural |
| l38 | Others had similar ideas earlier. This paper showed the method working on networks with several layers. | Others had similar ideas earlier. This paper showed it working on networks with several layers. | natural |
| l39 | Today, in PyTorch, a popular tool for building models, one line does it: loss dot backward. Every knob gets its slope. | Today in PyTorch, a popular tool for building models, one line does it: loss dot backward. Every knob gets its slope. | natural |
| l40 | That's automatic differentiation. Underneath, it's backpropagation. | That's called automatic differentiation, but underneath it's just backprop. | a bit off |
| l41 | Backpropagation is passing the blame backward, from the output, layer by layer. | So backprop is basically passing the blame backward, layer by layer. | a bit off |
| l42 | One trip back, and every knob knows which way to turn, and how far. | One trip back and every knob knows which way to turn and how far. | natural |
| l43 | But with so many knobs, a model can memorize the practice questions and get new ones wrong. | But with so many knobs, a model can memorize the practice questions and then fail new ones. | natural |
| l44 | That's overfitting, and it's up next. | That's overfitting, and that's next. | natural |

## 问题表
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l09 | V1/V3 | 建议 | For each knob, which way to turn and how far is its slope. All the slopes together are the gradient. | A clause ("which way to turn and how far") is the subject; the ear holds it until "is its slope". Two new terms back to back. | For each knob, the slope says which way to turn and how far. All the slopes together are the gradient. |
| l19 | V3/V5 | 建议 | In the first layer, two units, A and B, use two knobs each to turn the five into six and four. | Stacked appositives and "turn" doing double duty. Dense for one breath. | The first layer has two units, A and B, two knobs each. They turn the five into six and four. |
| l33 | V3 | 建议 | The trip back costs about two runs, so roughly three in all. | "three in all" can be heard as three trips, right after "one trip each way". | The trip back costs about two runs' worth, so roughly three runs' worth in all. |
| l26 | V3 | 建议 | Each unit then does the same for its own two knobs. | "The same" has two nearby referents (the l24 multiply, or the l22 blame rule). | Each unit then works out blame for its own two knobs the same way. |
| l40 | V3 | 建议 | That's automatic differentiation. | New term for a first-time listener, no gloss, 2.3s. | That's called automatic differentiation. Underneath, it's backpropagation. |
| l15 | V1 | 记录 | multiplying by each gear's ratio as you go | "ratio" is slightly written-style; l13 never used the word. | multiplying at each gear as you go |
| l20 | V1 | 记录 | adds a seventh knob | "adds a knob" is a little odd. | adds the seventh knob |
| l41/l42 | V4 | 记录 | Backpropagation is passing the blame backward... / One trip back, and every knob knows... | Two recap lines in a row, both fine alone. Not a must fix. | Keep, or merge: "So it's passing the blame backward, and every knob learns which way to turn, and how far." |
| l25 | V1 | 记录 | For A, the knob is two: twelve. | Slightly telegraphic; clear on one hearing. | For A the knob is two, so twelve. For B it's one, so six. |

Strict items (cold open l01-l04, agenda l05-l06, outro l41-l44): no must-fix. l41 is definition-shaped but acceptable (prior ruling agreed).

## 整体观察
- Big improvement over earlier rounds: no table-of-contents agenda, no "noun phrase and how to..." patterns left.
- Sentence-final punches ("For a single step.", "For one step.", "Bigger input, bigger blame.") sound like a real explainer; keep them.
- The cold open's "The real trick?" paired with l10 "The obvious way?" is a good echo; keep.
- The gear analogy (l12-l16) is clear on one hearing with simple numbers; keep.
- Remaining risk is the number-heavy stretch l22-l25 (many sixes); it parses, but only just by ear.
- Terms "slope" (l09) and "automatic differentiation" (l40) are the only places a new word lands without a hook.
