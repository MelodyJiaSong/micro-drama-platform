# voice_en__a report (round 2, blind, ear only)

## 评分表

- V1 2 证据：Most lines pass the "would I say this to a friend" test (l05 "like someone blindfolded on a mountain, with no idea where the valley is"; l29 "It never saw the whole map. It only felt the ground underfoot."). Small written-style residue: l12 "the slope underfoot is how much the score changes when you nudge each knob a little"; l45 "The second upgrade is smarter steps: a method called Adam gives each knob its own step size, based on its past slopes."
- V2 2 证据：Cold open flows as one thought (l04 "way too many to map" -> l05 blindfolded -> l06 "How does it find the bottom?" -> l07 "It uses something called gradient descent"). Chapter hand-offs are good (l30 "What if we'd picked wrong?"; l50 -> l51 -> l52). No table-of-contents reading anywhere. Small ding: l40 "with two upgrades" plus l45 "The second upgrade is smarter steps:" is a mild outline frame.
- V3 2 证据：l21 "So both go up" follows l20 where the score "drops", so "both" can be heard as the score. l35 "ninety-six, a hundred eighteen, a hundred forty-five" in 3.5s is hard to catch. l23 chains four numbers in one sentence. Terms are otherwise explained before use (gradient l13, learning rate l15, stochastic gradient descent l42, Adam l45).
- V4 2 证据：l26 "The gentler the slope, the shorter each step" is a bare claim with no reason. l46 "Meta's Llama uses a tweaked version" is a side fact the story does not need. l14 partly repeats l10-l11. The rest is tight, with no empty truisms.
- V5 2 证据：Warm, plain narrator throughout, with good short lines (l03 "With two knobs, that's easy."; l36 "Five steps in, it's off the map."). l45 is 21 words in 8.5s, and l12 is 19 words, so neither is easy in one breath.
- V6 2 证据：Drop-in rewrites are given below for l12, l21, l23, l35, l38, l45, none longer than the original. The 5 most awkward lines are ranked at the end of the issue table.
- R 2 证据：Round 1 voice_en issues I74-I80, I82-I89, I92-I99, I101, I103-I113 are resolved. Examples: l03 is now "With two knobs, that's easy."; l17 is "The taxi fares are made up."; l50 is "a model with just two knobs"; l07 now says "something called gradient descent". Partly resolved: I97/I98 l35 (digits are better, but three numbers in 3.5s remain); I105/I106 l45 (the "Second, smarter steps:" heading was reframed, but it is still long and colon-led). Author "不采纳" judgments: I81 l12 (keep slope correspondence) holds as a reason, but the line is still heavy, so I keep a 建议. I90 l23 (numbers match the screen counter) holds, but it is still a number list. I91 l24 "gentle" is not upheld as a problem, and I agree. I102 l42 is natural, and I agree. No new problems were introduced by round-1 edits, except that the l21 fix still leaves "both go up" ambiguous.

## 逐句复述

| 句号 | 原句 | 跟朋友会怎么说 | 判 |
|---|---|---|---|
| l01 | Last time, we scored the model's mistakes: the lower the score, the better. | Last time we gave the model a score for its mistakes. Lower is better. | natural |
| l02 | We gave every setting of two knobs a score and drew it as a landscape. The lowest point is the best setting. | We scored every setting of two knobs and drew it like a landscape. The lowest spot is the best one. | natural |
| l03 | With two knobs, that's easy. | With two knobs, that's easy. | natural |
| l04 | But a big model can have hundreds of billions of knobs, way too many to map. | But a big model has hundreds of billions of knobs. You can't map that. | natural |
| l05 | So the model's like someone blindfolded on a mountain, with no idea where the valley is. | So the model's like someone blindfolded on a mountain who has no idea where the valley is. | natural |
| l06 | How does it find the bottom? | How does it find the bottom? | natural |
| l07 | It uses something called gradient descent. Let's see how it works. | It uses something called gradient descent. Let's see how it works. | natural |
| l08 | So picture yourself up there, trying to reach the valley. | Picture yourself up there, trying to get down to the valley. | natural |
| l09 | You can't see, but your feet feel which way the ground tilts, and how steeply. | You can't see, but your feet can feel which way the ground tilts and how steep it is. | natural |
| l10 | So you feel for the steepest way down, and take one small step. | So you find the steepest way down and take one small step. | natural |
| l11 | Feel again, step again, and you get there. | Feel again, step again, and you get there. | natural |
| l12 | For the model, the slope underfoot is how much the score changes when you nudge each knob a little. | For the model, the slope just means: nudge a knob a bit and see how much the score changes. | a bit off |
| l13 | The gradient is the direction all the knobs should turn at once to drop the score fastest. | The gradient is which way to turn all the knobs, together, to make the score drop fastest. | natural |
| l14 | Gradient descent turns all the knobs one small step that way, then checks the slope again. | Gradient descent turns every knob a little that way, then checks the slope again. | natural |
| l15 | How big each step is, that's the learning rate, set by a person before training. | How big each step is, that's the learning rate. A person picks it before training. | natural |
| l16 | Here's last episode's map: base fare across, price per kilometer up. | Here's the map from last time: base fare going across, price per kilometer going up. | natural |
| l17 | Darker means a higher score. The taxi fares are made up. | Darker means a higher score. The taxi fares are made up. | natural |
| l18 | We start at a five dollar base fare and two dollars a kilometer: a score of seventy-eight, way up high. | We start at five dollars base and two dollars a kilometer. That scores seventy-eight, way up high. | natural |
| l19 | First, feel the slope: nudge each knob up ten cents. | First, feel the slope: nudge each knob up ten cents. | natural |
| l20 | Nudge the base fare up and the score drops one point seven. Nudge per kilometer up, and it drops eleven point two. | Raise the base fare ten cents and the score drops one point seven. Raise the per-kilometer price and it drops eleven point two. | natural |
| l21 | So both go up, but the per-kilometer slope is much steeper. | So we raise both, but the per-kilometer one matters way more. | a bit off |
| l22 | So the first step mostly turns that one. | So the first step mostly turns that one. | natural |
| l23 | In three steps, the score falls from seventy-eight to twenty-five, twelve, nine, and we're in the valley. | Three steps and we're down from seventy-eight to nine, in the valley. | a bit off |
| l24 | The floor is a long, gentle trench. | The bottom is a long, gentle trench. | natural |
| l25 | The base fare creeps up, the per-kilometer rate eases back, and we inch along. | The base fare creeps up, the kilometer rate eases back, and we inch along. | natural |
| l26 | The gentler the slope, the shorter each step. | The flatter it is, the smaller each step gets. | natural |
| l27 | After a thousand-odd steps, the score's about two. The true minimum is one point nine seven. | After about a thousand steps the score is around two. The real minimum is one point nine seven. | natural |
| l28 | The knobs end up near a ten-dollar base fare and two fifty a kilometer. | We end up near ten dollars base and two fifty a kilometer. | natural |
| l29 | It never saw the whole map. It only felt the ground underfoot. | It never saw the whole map. It only felt the ground under its feet. | natural |
| l30 | That run used a learning rate of zero point zero zero five. What if we'd picked wrong? | That run used a learning rate of point zero zero five. What if we'd picked wrong? | natural |
| l31 | Here are three paths from the same start, same number of steps. | Here are three paths from the same start, same number of steps. | natural |
| l32 | Make it ten times smaller, zero point zero zero zero five, and it heads the right way but crawls. | Make it ten times smaller and it goes the right way but crawls. | natural (zeros are a mouthful) |
| l33 | It ends at a score of five point five, still far from the bottom. | It ends at five point five, still far from the bottom. | natural |
| l34 | Make it about four times bigger, zero point zero two one, and it overshoots across the valley, higher than where it started. | Make it about four times bigger and it overshoots the valley and lands higher than where it started. | natural |
| l35 | Then it climbs higher and higher: 96, 118, 145. | Then it keeps climbing, past a hundred. | a bit off |
| l36 | Five steps in, it's off the map. | Five steps in, it's off the map. | natural |
| l37 | Our original rate walks steadily to the bottom. | Our original rate walks steadily to the bottom. | natural |
| l38 | That's why the learning rate is often the single most important setting in training. | That's why the learning rate is often the most important setting. | a bit off |
| l39 | Too big, and it bounces right off the map. Too small, and you waste time. | Too big and it bounces off the map. Too small and you waste time. | natural |
| l40 | Big models use gradient descent too, with two upgrades. | Big models use gradient descent too, but with two upgrades. | natural |
| l41 | First, there's too much data to read it all every step. | First, there's too much data to read all of it every step. | natural |
| l42 | So each step grabs a small random batch, roughly estimates the slope, and goes. That's stochastic gradient descent. | So each step just grabs a small random batch, guesses the slope, and goes. That's called stochastic gradient descent. | natural |
| l43 | The path wobbles, but it saves loads of computing and still ends up near the bottom. | The path wobbles, but it saves loads of computing and still gets near the bottom. | natural |
| l44 | GPT-3, for example, saw only about one part in a hundred thousand of its training data per step. | GPT-3, for example, only looked at about one part in a hundred thousand of its data on each step. | natural |
| l45 | The second upgrade is smarter steps: a method called Adam gives each knob its own step size, based on its past slopes. | The second upgrade is smarter steps. A method called Adam gives each knob its own step size, using what its slope's been doing. | a bit off |
| l46 | GPT-3 was trained with Adam, and Meta's Llama uses a tweaked version. | GPT-3 was trained with Adam, and Meta's Llama uses a tweaked version. | natural |
| l47 | That's how GPT-3's hundred and seventy-five billion knobs got turned, one small step at a time. | That's how GPT-3's 175 billion knobs got turned, one small step at a time. | natural |
| l48 | Gradient descent is walking downhill blindfolded: feel for the steepest way down, and take a small step. | Gradient descent is basically walking downhill blindfolded: feel for the steepest way down and take a small step. | natural |
| l49 | And how big those steps are is the learning rate. | And how big those steps are is the learning rate. | natural |
| l50 | But a model with just two knobs can only learn so much. | But a model with just two knobs can only learn so much. | natural |
| l51 | Next time, we'll stack lots of little units in layers, each with its own knobs, and see what happens. | Next time, we'll stack a bunch of little units in layers, each with its own knobs, and see what happens. | natural |
| l52 | That's called a neural network. | That's called a neural network. | natural |

## 问题表

| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l45 | V1, V5 | 建议 | The second upgrade is smarter steps: a method called Adam gives each knob its own step size, based on its past slopes. | 21 words in 8.5s with a colon that reads as a heading. "Based on its past slopes" is written-style, and the sentence carries three ideas (upgrade, method name, per-knob step). | The second upgrade is smarter steps. Adam gives each knob its own step size, based on its past slopes. |
| l12 | V1, V5 | 建议 | For the model, the slope underfoot is how much the score changes when you nudge each knob a little. | Definition-style sentence, 19 words, hard to say in one breath. This is the pivot from metaphor to model. | For the model, the slope is how much the score changes when you nudge a knob a little. |
| l35 | V3, V5 | 建议 | Then it climbs higher and higher: 96, 118, 145. | Three numbers in 3.5s. Spoken as words ("ninety-six, a hundred eighteen...") they blur, and the idea is just "it keeps climbing". | Then it climbs higher and higher, past a hundred. |
| l21 | V3 | 建议 | So both go up, but the per-kilometer slope is much steeper. | Follows "the score drops" in l20, so "both go up" can be heard as the score. "Slope" is the video's own word, but "per-kilometer slope" is a heavy compound. | So we raise both, but per kilometer matters far more. |
| l23 | V3 | 建议 | In three steps, the score falls from seventy-eight to twenty-five, twelve, nine, and we're in the valley. | Four numbers in one sentence; the middle two (25, 12) are unnecessary for the ear. The screen counter carries them. | In three steps the score falls from seventy-eight to nine, and we're in the valley. |
| l38 | V1 | 建议 | That's why the learning rate is often the single most important setting in training. | "The single most important setting in training" is written-style emphasis. | That's why the learning rate is often the most important setting. |
| l46 | V4 | 记录 | GPT-3 was trained with Adam, and Meta's Llama uses a tweaked version. | The Llama half is a side fact. Kept earlier because the screen shows Llama, so I only note it. | (keep as is, or cut the Llama clause if the screen is changed) |
| l32 / l34 | V3 | 记录 | zero point zero zero zero five / zero point zero two one | Strings of zeros are slow on the ear, but the screen shows the same numbers. Acceptable. | (none) |

Five most awkward lines, in order: l45, l12, l35, l21, l23.

Strict items check (cold open l01-l07, linking lines l30/l40/l50-l52, outro l48-l52, chapter titles): no 必改 found. The cold open sounds like a person leading into a question. The outro is a plain recap and a teaser. The chapter titles "Downhill, blindfolded", "A small experiment", "How big a step?", "Training giant models" are natural. No agenda or table-of-contents is read aloud.

## 整体观察

- Big improvement over round 1: no list-reading or noun phrase + "and how to" patterns remain; the cold open and outro sound like one person talking.
- The hardest lines to follow on one hearing are those with numbers (l23, l35) and the long definition lines (l12, l45).
- Keep: the question and answer in l06-l07 ("How does it find the bottom?" / "It uses something called gradient descent.").
- Keep: l29 "It never saw the whole map. It only felt the ground underfoot." as the experiment's takeaway.
- Keep: l37 and l39 ("Our original rate walks steadily to the bottom." / "Too big, and it bounces right off the map. Too small, and you waste time."), which are short, concrete and memorable.
- No 必改 items. The weakest dimensions are V1 to V6 at 2 each, all with small blemishes.
