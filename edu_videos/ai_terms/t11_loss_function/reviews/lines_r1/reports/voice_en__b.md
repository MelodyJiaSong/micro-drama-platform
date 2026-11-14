## 评分表

- V1 1 证据：Several lines sound written or compressed rather than spoken. l28 reads out three positions; l33’s “chasing as low as it can get” lacks a clear object; l27 stacks axis labels without verbs.
- V2 1 证据：The overall progression makes sense, but strict linking lines need work: l02’s “this turn beat the last one,” l38’s unclear “It’s just scoring,” and l50’s “That’s gradient descent.” The outro also changes the definition established in l04.
- V3 1 证据：l05 introduces error as how far a guess misses, but l18–l19 suddenly require negative errors. l41 leaves “percent chance” implicit. l29 delivers two prices and a decimal score in one sentence.
- V4 2 证据：Most examples earn their place, especially l14–l22. l48 could disappear without losing information: l46 already says the job is to “push that score down,” and l47 supplies the recap.
- V5 2 证据：l07–l08 and l35–l37 have a warm, conversational voice. l28 becomes a positional roll call, and l29’s consecutive numbers interrupt that otherwise approachable rhythm. Actual delivery cannot be assessed without audio.
- V6 3 证据：All 14 lines marked off below have drop-in rewrites, each no longer than its original by word count; for example, l38 goes from 16 to 15 words and l50 remains 10 words. The five most awkward lines are ranked under 整体观察.

## 逐句复述

“Natural” does not require my conversational paraphrase to be identical. “Off” identifies wording, structure, or information packaging that I would actually change for speech.

| 句号 | 原句 | 跟朋友会怎么说 | 判 |
|---|---|---|---|
| l01 | Last time, we said a model is a machine with knobs, and learning means turning those knobs to the right spot. | Last time, we pictured a model as a machine with knobs, and learning meant getting those knobs into the right positions. | natural |
| l02 | But what does "right" even mean? How does the machine know this turn beat the last one? | But what does “right” mean? How does it know whether turning a knob helped? | a bit off |
| l03 | The trick is to give its mistakes a score. | The trick is to give its mistakes a score. | natural |
| l04 | That score is called the loss, and the rule for working it out is the loss function. That's today's topic. | We call that score the loss, and the rule that calculates it the loss function. That’s what we’re talking about today. | natural |
| chapter: What is a loss function? | What is a loss function? | So, what is a loss function? | natural as a silent chapter title |
| l05 | Every time the model guesses, it's a bit off from the real answer. How far off, that's the error. | A guess can be above or below the real answer. The difference is the error. | a bit off |
| l06 | Roll all those errors up into one number, and that's the loss: a score for how wrong it is. | Put all those errors into one number, and that’s the loss: how wrong the model is overall. | natural |
| l07 | It's the opposite of a test score: lower is better, and zero means not wrong at all. | It’s the opposite of a test score: lower is better, and zero means no mistakes. | natural |
| l08 | Kind of like golf, where fewer strokes is better. | Kind of like golf: fewer strokes is better. | natural |
| l09 | Now the machine can check itself. If a turn lowers the score, keep it. If not, turn it back. | Now it can check itself. If turning a knob lowers the score, keep the change. Otherwise, turn it back. | natural |
| l10 | So training, put simply, is turning the knobs over and over to push that score down. | So training is basically turning those knobs again and again to bring the score down. | natural |
| chapter: A small experiment | A small experiment | Let’s try a small experiment. | natural as a silent chapter title |
| l11 | Back to those twelve taxi rides from last time: distance along the bottom, fare up the side. The data's made up. | Let’s use those twelve made-up taxi rides again. We have each ride’s distance and fare. | a bit off |
| l12 | The model is still that straight line, with two knobs: the starting fare, and the price per kilometer. | We’re still using a straight line with two knobs: the starting fare and the price per kilometer. | natural |
| l13 | First try: a five-dollar starting fare and two dollars a kilometer. The whole line sits too low. | First, let’s try five dollars to start and two dollars a kilometer. That puts the whole line too low. | natural |
| l14 | Take the five-kilometer ride: it cost twenty-three dollars, the model guessed fifteen, so it's off by eight. That's the error. | Take the five-kilometer ride. It cost twenty-three dollars, but the model guessed fifteen, so the error is eight. | natural |
| l15 | Now square it: eight times eight is sixty-four. That's this red square. | Now square that error: eight times eight gives a penalty of sixty-four. | a bit off |
| l16 | Do that for all twelve rides, take the average, and this setting scores seventy-eight. | Do that for all twelve rides and average the results. This setting scores seventy-eight. | natural |
| l17 | Second try: four dollars to start and three fifty a kilometer. Too steep: too low on short rides, too high on long ones. | Next, try four dollars to start and three fifty a kilometer. That’s too steep: short rides come out too cheap and long rides too expensive. | natural |
| l18 | If we skipped the squaring and just averaged the errors, the too-lows and too-highs would cancel out. | Count low guesses as negative errors and high guesses as positive ones. When you average them, they can cancel. | clearly off |
| l19 | The average is about minus thirty cents, so it looks like it's barely wrong at all. | The average comes out around minus thirty cents, which makes it look as though the model barely missed. | natural; depends on fixing l18 |
| l20 | That's why we square: once everything's squared, it's all positive, so nothing cancels. | That’s why we square the errors: the negative ones turn positive, so they don’t cancel the positive ones. | natural |
| l21 | And bigger misses cost a lot more: off by two costs four, but off by eight costs sixty-four. | And bigger mistakes get much bigger penalties: miss by two and it costs four; miss by eight and it costs sixty-four. | natural |
| l22 | Square, then average, and this setting scores thirteen point four. | Square the errors, then average them, and this setting scores thirteen point four. | natural |
| l23 | This is called mean squared error, and it's the most common loss function. | This is called mean squared error, and it’s the most common loss function. | natural |
| l24 | Third try: ten dollars to start and two fifty a kilometer. The line hugs the points, the squares are tiny, and it scores two point one nine. | Third try: ten dollars to start and two fifty a kilometer. The line stays close to the points, the squares are tiny, and the score is two point one nine. | natural |
| l25 | The third has the lowest score, so it's the best of the three. | The third try has the lowest score, so it’s the best of those three. | natural |
| l26 | But that's only three tries. Score every possible setting of the two knobs, and you get a landscape map of scores. | But we’ve tried only three settings. Score every possible pair of knob settings, and you get a landscape of scores. | a bit off |
| l27 | Starting fare along the bottom, price per kilometer up the side, and the darker the color, the higher the score. | The axes show starting fare and price per kilometer. Darker areas mean higher scores. | a bit off |
| l28 | Our three tries: the first way up high, the second halfway down, the third nearly at the bottom of the valley. | Our first try is high on the slope. The second is lower, and the third is near the valley floor. | clearly off |
| l29 | The lowest point is a starting fare of about ten twenty and two fifty-four a kilometer, scoring one point nine seven. | Ten dollars twenty to start, then two fifty-four a kilometer, gives the lowest score: one point nine seven. | a bit off |
| l30 | That's the best setting, and the whole job of training is to find that lowest point. | That’s the best setting. Training’s job is to find that lowest point. | natural |
| chapter: The score is all it sees | The score is all it sees | The score is all it sees. | natural as a silent chapter title |
| l31 | Here's something easy to miss: even the lowest point isn't zero. | Here’s something you might miss: even the lowest point isn’t zero. | natural |
| l32 | Real fares bounce around with traffic and detours, so no straight line could nail every ride. | Real fares vary with traffic and detours, so a straight line couldn’t get every ride exactly right. | natural |
| l33 | So training isn't chasing zero. It's chasing as low as it can get. | Training aims for the lowest possible score, even if that isn’t zero. | a bit off |
| l34 | And here's the other thing: the model has no idea what a taxi is. All it sees is the score. | And here’s the other thing: the model doesn’t know what a taxi is. All it sees is the score. | natural |
| l35 | However you score it, that's how it learns. Because we squared the errors, it's terrified of big mistakes. | The way you score it shapes how it learns. Since we squared the errors, it really wants to avoid big mistakes. | natural |
| l36 | It would rather be a little off on every ride than way off on just one. | It would rather be a little wrong on every ride than wildly wrong on one. | natural |
| l37 | So when you pick a loss function, you're really telling the model what "good" means. | So choosing a loss function means telling the model what counts as good. | natural |
| chapter: How big models are scored | How big models are scored | How do big models get their scores? | natural as a silent chapter title |
| l38 | Big language models like ChatGPT get a score in training too. It's just scoring something different. | Language models like ChatGPT get training scores too, but for predicting words instead of fares. | a bit off |
| l39 | Their job is to guess the next word, like what comes after "Twinkle, twinkle, little." | Their job is to guess the next word—like what follows “Twinkle, twinkle, little.” | natural |
| l40 | The score looks at how confident the model was in the word that actually comes next. The less confident, the bigger the penalty. | The score depends on how confident it was about the word that really comes next. Less confidence means a bigger penalty. | natural |
| l41 | Give the right word ninety percent, and the penalty is tiny. Give it only ten percent, and it's way bigger. | If it gives the right word a ninety percent chance, the penalty is tiny. At ten percent, it’s much bigger. | a bit off |
| l42 | This kind of scoring is called cross-entropy. The name is all you need for now. | This scoring method is called cross-entropy. For now, you just need the name. | natural |
| l43 | In twenty twenty-three, Meta trained a language model called Llama 2, and plotted this score as a curve. It kept going down. | In twenty twenty-three, Meta trained a language model called Llama 2 and plotted its score. The curve kept going down. | natural |
| l44 | The model read two trillion tokens of data. Tokens are roughly words or pieces of words. | The model read two trillion tokens. A token is roughly a word or a piece of one. | natural |
| l45 | And even then, the score was still falling, with no sign yet of a floor. | Even after that, the score was still falling. There wasn’t any sign of it bottoming out yet. | natural |
| l46 | Tens of billions of knobs or just two, the job is the same: push that score down. | Whether there are tens of billions of knobs or just two, the job is the same: get the score down. | natural |
| l47 | So, a loss function is a score for how wrong the model is, and lower is better. | So, a loss function works out how wrong the model is. A lower score is better. | clearly off |
| l48 | And training is just pushing that score down. | And training means bringing that score down. | natural, but expendable repetition |
| l49 | But with tons of knobs, that map gets so huge you can't see the edges. So which way do you turn to get down? | But with loads of knobs, the map becomes enormous. How do you know which way to turn to get downhill? | natural |
| l50 | That's gradient descent, and that's where we're headed next time. | Next time, we’ll see how gradient descent guides those turns. | a bit off |

## 问题表

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l47 | V2, V3 | 必改 | So, a loss function is a score for how wrong the model is, and lower is better. | The outro contradicts the distinction I heard in l04: the **loss** is the score; the **loss function** is the rule for calculating it. The recap leaves me remembering the wrong distinction. Strict outro item. | So, a loss function works out how wrong the model is. A lower score is better. |
| l18 | V3 | 必改 | If we skipped the squaring and just averaged the errors, the too-lows and too-highs would cancel out. | I have heard error described as “how far off,” with an example of eight. Nothing has told me errors can be negative. “Cancel out” and the following “minus thirty cents” therefore introduce a missing step. “Too-lows and too-highs” also makes me decode improvised nouns while following the arithmetic. | Average errors as negatives for low guesses and positives for high guesses, and they can cancel out. |
| l38 | V1, V2, V3 | 必改 | Big language models like ChatGPT get a score in training too. It's just scoring something different. | What does “it” mean—the model, training, or the score? The sentence switches from receiving a score to doing the scoring. This chapter transition should name the difference directly. Strict transition item. | Language models like ChatGPT get training scores too, but for predicting words instead of fares. |
| l02 | V1, V2 | 必改 | But what does "right" even mean? How does the machine know this turn beat the last one? | “This turn beat the last one” sounds like comparing turns in a game. I briefly have to translate it back into adjusting a knob. The question should make the improvement clear immediately. Strict cold-open item. | But what does "right" even mean? How does the machine know whether turning a knob helped? |
| l11 | V1, V2, V3 | 必改 | Back to those twelve taxi rides from last time: distance along the bottom, fare up the side. The data's made up. | The chapter opens with a fragment followed by two axis-label fragments. Listening alone, I get positions on an unseen chart before a clear reminder of what information we have. Strict chapter-transition item. | Let's use those twelve made-up taxi rides again. We have each ride's distance and fare. |
| l50 | V2, V3 | 必改 | That's gradient descent, and that's where we're headed next time. | After “which way do you turn?”, “That’s gradient descent” names something without quite answering or explaining its role. The double “that’s” also weakens the landing. Strict outro item. | Next time, we'll see how gradient descent guides those turns. |
| l28 | V1, V3, V5 | 建议 | Our three tries: the first way up high, the second halfway down, the third nearly at the bottom of the valley. | This is a caption-like positional roll call. Missing verbs make the listener supply the relationships while holding three locations in mind. Complete clauses would sound more like someone describing what happened. | Our first try is high on the slope. The second is lower, and the third is near the valley floor. |
| l29 | V3, V5 | 建议 | The lowest point is a starting fare of about ten twenty and two fifty-four a kilometer, scoring one point nine seven. | Three numerical values arrive in one sentence. “The lowest point is a starting fare … and …” also blurs the distinction between the setting and its score. Label the opening amount as money and make the score the sentence’s destination. | Ten dollars twenty to start, then two fifty-four a kilometer, gives the lowest score: one point nine seven. |
| l33 | V1, V3 | 建议 | So training isn't chasing zero. It's chasing as low as it can get. | “Chasing as low as it can get” sounds unfinished: chasing what? I can reconstruct “the lowest score,” but the spoken sentence should supply it. | Training aims for the lowest possible score, even if that isn't zero. |
| l41 | V1, V3 | 建议 | Give the right word ninety percent, and the penalty is tiny. Give it only ten percent, and it's way bigger. | “Give the right word ninety percent” leaves out what the percentage measures. A listener without this background should hear “chance,” rather than having to infer it from “confident.” | If the model gives the right word a ninety percent chance, the penalty's tiny. At ten percent, it's much bigger. |
| l27 | V1, V3 | 建议 | Starting fare along the bottom, price per kilometer up the side, and the darker the color, the higher the score. | Two label fragments turn into a third relationship halfway through the sentence. This sounds like reading chart annotations. State what the axes represent, then explain the color. | The axes show starting fare and price per kilometer. Darker areas mean higher scores. |
| l05 | V1, V3 | 建议 | Every time the model guesses, it's a bit off from the real answer. How far off, that's the error. | “Every time” tells me guesses necessarily miss. More importantly for the next example, “how far off” establishes only a distance, leaving the later negative error unexplained. A guess can be above or below the answer. | A guess can be above or below the real answer. The difference is the error. |
| l26 | V1 | 建议 | But that's only three tries. Score every possible setting of the two knobs, and you get a landscape map of scores. | “Landscape map of scores” piles three nouns together and sounds composed on the page. “Landscape of scores” gives the listener the same metaphor more cleanly. | But we've tried only three settings. Score every possible pair of knob settings, and you get a landscape of scores. |
| l15 | V1, V3 | 建议 | Now square it: eight times eight is sixty-four. That's this red square. | “That’s this” is an awkward demonstrative handoff. The color reference gives an ear-only listener nothing further; connect sixty-four to its role in the score instead. | Now square that error: eight times eight gives a penalty of sixty-four. |

## 整体观察

- **Most awkward, ranked:** 1. l28—positional roll call; 2. l33—unfinished “chasing” construction; 3. l38—unclear subject; 4. l27—axis-label fragments; 5. l29—three numerical values tangled together.
- **Keep:** l03–l04’s simple distinction between the score and the rule that calculates it.
- **Keep:** l14–l22’s concrete eight → sixty-four → average progression, with the missing sign explanation added.
- **Keep:** l35–l37’s warm explanation of why choosing the score matters; l49 also gives the next episode a useful question.
- The spoken chapter openings mostly follow a thought rather than announce an agenda. The four supplied silent chapter titles read naturally as titles.
- l48 can be cut: it repeats l46 almost immediately.
- This is a text-based listening simulation. No recording was supplied; actual pronunciation, breath placement, and delivery remain unassessed. The main title card’s wording was not supplied.