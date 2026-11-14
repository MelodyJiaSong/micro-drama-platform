## 评分表

- V1 1 证据：l20 “weights each by a knob” sounds like technical shorthand; l15 “multiplying in one ratio” is an awkward spoken construction.
- V2 1 证据：l04 “gets them all” leaves the opening promise unclear. l29 changes from “Now check” to “That took” without an audible calculation. However, l06 is a connected spoken preview, not a table of contents.
- V3 1 证据：l22 introduces “blame” while delivering three unexplained results; l26 “splits its share” suggests division; l33 announces approximately three runs immediately after describing two passes.
- V4 2 证据：Most lines advance the explanation. l36 repeats the forward/backward description already given in l30 and l33, with little additional payoff.
- V5 2 证据：l10 “The obvious way? Nudge one knob” and l32 “For one step” have effective conversational rhythm. l25 “Times two gives A twelve” compresses arithmetic into a harder-to-parse phrase.
- V6 3 证据：All 24 lines marked off below have replacement wording in the issue table, no longer than their originals by spoken-word count. The five most awkward lines are ranked below.

## 问题表

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l20 | V1, V3 | 必改 | The second layer weights each by a knob, adds one more, and guesses: twenty-nine yuan. | “Weights” arrives as an unexplained technical verb. “Adds one more” could mean another knob, number, or operation. | Two knobs multiply those outputs; another adds a value. The predicted fare is twenty-nine yuan. |
| l26 | V3 | 必改 | Each unit then splits its share between its own two knobs, the same way. | “Splits its share” sounds like dividing a quantity between two recipients. It does not let a listener reconstruct the operation. | For each unit's two knobs, multiply its error by each knob's input again. |
| l09 | V1, V3 | 必改 | So each step, you want the gradient: which way each knob should turn to drop the error fastest. The slope. | “The slope” is an unattached afterthought. A beginner has not been told what either technical word means or how they relate. | Each knob has a slope: how much turning it changes the error. Together, those slopes make up the gradient. |
| l22 | V1, V3 | 必改 | Last layer first. Each knob's blame is the error times what's fed into it: thirty-six, twenty-four, six. | “Blame” suddenly replaces the earlier vocabulary. The listener must decode that metaphor and retain three results simultaneously. | Last layer first. Each knob's slope is six times its input: thirty-six, twenty-four, six. |
| l33 | V1, V3 | 必改 | Backpropagation stays one forward, one back. Roughly three runs' worth. | “Stays one forward” is compressed wording. More seriously, one plus one has just become three without an explanation of the backward pass's cost. | One forward run, plus two runs' work backward. Roughly three. |
| l04 | V2, V3 | 必改 | The real trick gets them all in one trip backward. It's called backpropagation. | Strict cold open: “gets them all” could mean obtaining the knobs, testing them, or turning them. State what the trick finds. | One backward pass tells us how each knob affects the error. That's backpropagation. |
| l29 | V2, V3 | 必改 | Now check it the slow way. That took eight forward runs: one untouched, plus one per knob. | Strict transition: the instruction immediately becomes a completed past event. “One untouched” also leaves the noun implicit. | Checking the slow way takes eight runs: one unchanged, then one with each knob nudged. |
| l16 | V1, V3 | 必改 | Each gear handles only its own link and reuses what's already done. Nothing is recalculated. | Literal gears have suddenly become calculators. “What's already done” never identifies the result being reused. | At each link, multiply its ratio by the result you've already worked out. |
| l37 | V3 | 必改 | They also found that the units in the middle learn useful features on their own. | “Features” has a specialized meaning here that an uninitiated listener has not been given. | They also found that middle units learn to pick out useful patterns on their own. |
| l39 | V3, V5 | 必改 | Today in PyTorch, one line, loss dot backward, gives every knob its slope. | Strict transition to the present: PyTorch is unidentified, and the listener must infer that “loss dot backward” is a programming command. | With PyTorch, a programming tool, one command calculates every slope: “loss dot backward.” |
| l01 | V1 | 必改 | Today's big AI models have billions of knobs, some hundreds of billions. | Strict cold open: “some hundreds of billions” is an awkward ellipsis and can initially sound like an approximate quantity. | Today's big AI models have billions of knobs—sometimes hundreds of billions. |
| l03 | V1 | 必改 | Testing them one at a time would never finish. | Strict cold open: the testing is awkwardly made the thing that “finishes.” A person finishing the task is more natural. | You'd never finish testing them one at a time. |
| l05 | V1, V2 | 必改 | Last time we saw that a neural network is layers of small units, each with its own knobs. | Strict linking line: “a neural network is layers” sounds compressed rather than conversational. | Last time, we saw that a neural network has layers of small units, each with its own knobs. |
| l07 | V1, V2 | 必改 | Here's training: the model guesses, we compare it with the right answer, and the gap is the error. | Strict chapter opening: “Here's training” sounds like a label being introduced. The following explanation is otherwise easy to follow. | In training, the model guesses. We compare its guess with the right answer; the gap is the error. |
| l43 | V1, V2 | 必改 | But lots of knobs bring trouble. A model can memorize the practice questions and flunk a new one. | Strict outro: “lots of knobs bring trouble” sounds like a written slogan. “Flunk a new question” is also less idiomatic than getting it wrong. | But with so many knobs, a model can memorize practice questions and get a new one wrong. |
| l17 | V3 | 建议 | A neural network is a chain like this. Every knob drives the final answer through a few layers. So the error can flow back. | “So” presents an inference that the listener has not quite been given. Explain what working backward discovers. | A network works similarly: each knob affects the answer through several layers. Working backward tells us how much each knob changes the error. |
| l24 | V3 | 建议 | One layer back, the error is multiplied by the knob it crosses. | An error “crossing” a knob requires interpreting the diagram metaphor. The multiplier is the knob's value. | Back one layer, multiply the error by the connecting knob's value. |
| l25 | V3, V5 | 建议 | Times two gives A twelve. Times one gives B six. | The missing starting number and adjacent letter/number names make this unnecessarily difficult by ear. | A gets six times two: twelve. B gets six. |
| l15 | V1 | 建议 | It's easiest to start at the pointer and walk back, multiplying in one ratio per gear. | “Multiplying in one ratio” sounds awkward aloud. “Multiplying by” is the familiar construction. | Start at the pointer and work backward, multiplying by each gear's ratio as you go. |
| l13 | V1 | 建议 | Turn the first gear one notch, the second turns two. One notch on the second, the third turns three. | The second relationship is compressed into a telegraphic phrase. Explicit conditional wording is easier to hear. | Turn the first gear one notch, and the second turns two. Turn the second one notch, and the third turns three. |
| l23 | V1 | 建议 | Bigger number in, bigger blame. | The shorthand is catchy, but “bigger blame” is an awkward collocation. Keeping “slope” also connects to the proposed l22. | Bigger input, steeper slope. |
| l28 | V1 | 建议 | Turn each a small step and guess again. Twenty-nine becomes about twenty-four. Much closer. | “Turn each a small step” is less natural than turning a knob down a little. | Turn each knob down a bit. Twenty-nine becomes about twenty-four. Much closer. |
| l36 | V1, V3, V4 | 建议 | In the paper, each connection's slope is worked out in two passes: forward, then backward from the top layer. | Passive textbook phrasing repeats the two-pass explanation. “Connection” replaces “knob,” and “top layer” assumes an orientation the listener cannot see. | They calculated each knob's slope with a forward pass, then a backward pass, starting at the output. |
| l38 | V1, V3 | 建议 | Similar methods had been proposed earlier. This paper showed it could train networks with several layers. | The first sentence sounds like academic prose. In the second, “it” has no clean singular antecedent: the paper or the method? | Others had suggested similar methods, but this paper showed that they worked with several layers. |

**Five most awkward lines, ranked:**  
1. **l20:** “weights each by a knob, adds one more.”  
2. **l26:** “splits its share between its own two knobs.”  
3. **l09:** the gradient definition followed by “The slope.”  
4. **l22:** “Each knob's blame” followed by three results.  
5. **l04:** “The real trick gets them all.”

## 逐句复述

The conversational retell preserves the intended meaning; judgments compare the original with that retell. Fragments are not automatically faults: several work well as spoken emphasis.

| 句号 | 原句 | 跟朋友会怎么说 | 判 |
|---|---|---|---|
| l01 | Today's big AI models have billions of knobs, some hundreds of billions. | These big AI models have billions of knobs—sometimes hundreds of billions. | a bit off |
| l02 | Every step of training, you need to know which way each knob should turn, and how far. | Every time you train it, you need to know which way to turn every knob, and by how much. | natural |
| l03 | Testing them one at a time would never finish. | You'd never finish testing them one at a time. | a bit off |
| l04 | The real trick gets them all in one trip backward. It's called backpropagation. | There's a way to find how every knob affects the error in one backward pass. That's backpropagation. | clearly off |
| l05 | Last time we saw that a neural network is layers of small units, each with its own knobs. | Remember those layers of little units? Each unit has its own knobs. | a bit off |
| l06 | This time, we'll see why testing knobs one by one breaks down, then watch the error flow backward through a tiny network. | We'll see why testing every knob takes too long, then follow the error backward through a little network. | natural |
| l07 | Here's training: the model guesses, we compare it with the right answer, and the gap is the error. | When we train it, it guesses. We compare that guess with the answer, and the difference is the error. | a bit off |
| l08 | The loss is a score for how wrong it is. Training is turning the knobs to push that score down. | The loss tells you how wrong the model is. Training means adjusting the knobs to lower that score. | natural |
| l09 | So each step, you want the gradient: which way each knob should turn to drop the error fastest. The slope. | We need to know how much each knob changes the error. Those individual slopes make up the gradient. | clearly off |
| l10 | The obvious way? Nudge one knob, rerun everything, and see if the error went up or down. | You could just move one knob a little, run it again, and see whether the error gets better or worse. | natural |
| l11 | One full rerun per knob. Billions of knobs, billions of reruns. For a single step. | That's a whole rerun for every knob. Billions of knobs means billions of reruns—just for one step. | natural |
| l12 | Backpropagation works from the other end. Picture a chain of gears, with a pointer on the last one. | Backpropagation starts at the other end. Imagine some connected gears, with a pointer on the last one. | natural |
| l13 | Turn the first gear one notch, the second turns two. One notch on the second, the third turns three. | If you turn the first gear one notch, the second turns two. If the second turns one, the third turns three. | a bit off |
| l14 | So how far does the pointer move? Multiply along the way: two times three. Six notches. | So how far does the pointer move? Two times three: six notches. | natural |
| l15 | It's easiest to start at the pointer and walk back, multiplying in one ratio per gear. | Start at the pointer and work backward. Multiply by each gear's ratio as you go. | a bit off |
| l16 | Each gear handles only its own link and reuses what's already done. Nothing is recalculated. | At each link, use its ratio and the result you've already calculated farther along. | clearly off |
| l17 | A neural network is a chain like this. Every knob drives the final answer through a few layers. So the error can flow back. | Each knob affects the answer through several layers. We can work backward to find how much it changes the error. | a bit off |
| l18 | Here's a real, tiny network. Two layers, seven knobs. The input is a taxi ride: five kilometers. | Let's try a tiny network with two layers and seven knobs. We give it a five-kilometer taxi ride. | natural |
| l19 | In the first layer, units A and B use two knobs each to turn that into six and four. | A and B each have two knobs. They turn that five into six and four. | natural |
| l20 | The second layer weights each by a knob, adds one more, and guesses: twenty-nine yuan. | The next layer multiplies those outputs by two knob values, adds another value, and predicts a fare of twenty-nine yuan. | clearly off |
| l21 | The real fare was twenty-three. Six too high. That six is the error we pass back. | The fare was actually twenty-three, so we're six too high. That's the error we send backward. | natural |
| l22 | Last layer first. Each knob's blame is the error times what's fed into it: thirty-six, twenty-four, six. | Start with the last layer. Multiply each knob's input by the error, six. That gives slopes of thirty-six, twenty-four, and six. | clearly off |
| l23 | Bigger number in, bigger blame. | The bigger the input, the bigger the slope. | a bit off |
| l24 | One layer back, the error is multiplied by the knob it crosses. | To go back another layer, multiply the error by the connecting knob's value. | a bit off |
| l25 | Times two gives A twelve. Times one gives B six. | A gets six times two, which is twelve. B gets six times one, which is six. | a bit off |
| l26 | Each unit then splits its share between its own two knobs, the same way. | Now do the same multiplication for each unit's two knobs, using that unit's error. | clearly off |
| l27 | One trip back, and all seven knobs have a number. The guess was high, so all turn down, some more than others. | After one backward pass, we've got a number for every knob. Here they all turn down, but by different amounts. | natural |
| l28 | Turn each a small step and guess again. Twenty-nine becomes about twenty-four. Much closer. | Turn each knob down a little and try again. Now it's about twenty-four instead of twenty-nine. Much closer. | a bit off |
| l29 | Now check it the slow way. That took eight forward runs: one untouched, plus one per knob. | If we check the slow way, we need eight runs: the original, then another with each knob nudged. | a bit off |
| l30 | Same seven numbers, exactly. Backpropagation needed just one run forward and one trip back. | We get exactly the same seven numbers. Backpropagation only needed one forward pass and one backward pass. | natural |
| l31 | Scale up to a billion knobs, and the slow way is a billion and one runs. | With a billion knobs, the slow method needs a billion and one runs. | natural |
| l32 | Even at one second a run, that's over thirty years. For one step. | Even if each run takes just a second, that's more than thirty years—for one step. | natural |
| l33 | Backpropagation stays one forward, one back. Roughly three runs' worth. | Backpropagation needs one forward run. The backward pass takes about two runs' worth of work, so roughly three altogether. | clearly off |
| l34 | Without it, billion-knob models couldn't be trained. | Without that shortcut, we couldn't train models this big. | natural |
| l35 | In nineteen eighty-six, a Nature paper by Rumelhart, Hinton and Williams laid this out clearly. | Rumelhart, Hinton, and Williams explained this clearly in a nineteen eighty-six paper in Nature. | natural |
| l36 | In the paper, each connection's slope is worked out in two passes: forward, then backward from the top layer. | They calculated each knob's slope by going forward, then working backward from the output. | a bit off |
| l37 | They also found that the units in the middle learn useful features on their own. | They also found that the middle units learn to recognize useful patterns by themselves. | a bit off |
| l38 | Similar methods had been proposed earlier. This paper showed it could train networks with several layers. | Other people had suggested similar methods, but this paper showed they worked for networks with several layers. | a bit off |
| l39 | Today in PyTorch, one line, loss dot backward, gives every knob its slope. | There's a programming tool called PyTorch. One command, “loss dot backward,” calculates all those slopes. | a bit off |
| l40 | That's automatic differentiation. Underneath, it's backpropagation: walking back from the output, collecting slopes. | That's called automatic differentiation. Under the hood, it works backward from the output to calculate the slopes. | natural |
| l41 | Backpropagation is passing the blame backward, from the output, layer by layer. | Backpropagation means working backward from the output, passing the blame through each layer. | natural |
| l42 | One trip back, and every knob knows which way to turn, and how far. | One backward pass tells every knob which way to turn and by how much. | natural |
| l43 | But lots of knobs bring trouble. A model can memorize the practice questions and flunk a new one. | With so many knobs, a model can memorize the practice questions and still get a new question wrong. | a bit off |
| l44 | That's overfitting, and it's up next. | That's called overfitting. We'll look at that next. | natural |
| Chapter: Too many knobs to try | Too many knobs to try | There are too many knobs to test individually. | natural as a silent title |
| Chapter: Working backward | Working backward | Let's work backward. | natural as a silent title |
| Chapter: A small experiment | A small experiment | Let's try a little experiment. | natural as a silent title |
| Chapter: From 1986 to today | From 1986 to today | Here's how this connects to what people use today. | natural as a silent title |

## 整体观察

- Keep l06: its two connected actions sound like a person setting up an explanation, rather than reading section headings.
- Keep the direct question in l10 and the emphatic fragments in l11 and l32; they create useful spoken rhythm.
- Keep the twenty-nine → twenty-three → about twenty-four progression; those numbers give the example a clear purpose.
- The main listening barrier is the shift among “slope,” “gradient,” “blame,” “share,” and unnamed numbers before their relationships are secure.
- The four supplied chapter titles pass the strict wording check. Exact main-title, agenda-card, and end-card wording was not supplied.
- This is a blind spoken-text assessment; recorded pronunciation, delivery, and actual breath timing were not available.