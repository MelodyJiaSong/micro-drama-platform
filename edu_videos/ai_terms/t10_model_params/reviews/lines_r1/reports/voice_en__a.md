# voice_en__a report (round 1)

## 评分表
- V1 3 证据：Nearly every line is plain speech, e.g. l12 "Nobody types that in. The machine learns it from examples." and l35 "no eating, no sleeping". Only the spoken prices (l22, l25) wobble, which is scored under V3.
- V2 3 证据：The cold open l01-l04 is a real hook ("You've probably seen it in the news..." then "So what actually is a parameter?"), and l04 "let's crack a model open" leads in with no TOC. Chapter hand-offs flow, e.g. l13 "turning the knobs" into l14 "Here are twelve taxi rides". The outro l42 "what does 'the right positions' actually mean?" leads straight into l43.
- V3 2 证据：l22 "about ten twenty and about two fifty per kilometer" and l25 "about thirty fifty" can be misheard as times or a range; the ear can't tell "$10.20" from "ten twenty". Everything else is one idea per line.
- V4 2 证据：l34 "That's a hundred and seventy-five billion knobs" repeats l33. l37 "people decide how the machine does its math, and the settings are learned from examples" repeats l12. l40-l41 recap l07 and l13. Each repeat is mild and does a job in an explainer.
- V5 3 证据：One warm narrator throughout. Rhythm varies: l07 "Those knobs are the parameters." (1.9s) next to the long l08. Every line fits one breath; the longest, l32 and l35 (10s), still read comfortably.
- V6 3 证据：Rewrites below for every flagged line (l22, l25, l34, l37, l44). No line is clearly off; the 5 most awkward are ranked under the issues table.

## 逐句复述
| 句号 | 原句 | 跟朋友会怎么说 | 判 |
|---|---|---|---|
| l01 | You've probably seen it in the news: some big AI model has over a hundred billion parameters. | You've probably seen headlines saying some AI model has over a hundred billion parameters. | natural |
| l02 | So what actually is a parameter? And what does it mean to have that many? | So what's a parameter, actually? And what does it mean to have that many? | natural |
| l03 | Last time, we saw that today's AI mostly figures out patterns on its own, from examples. What it ends up with is called a model. | Last time we saw that AI mostly learns patterns from examples by itself. What it ends up with is called a model. | natural |
| l04 | So this time, let's crack a model open and see what's really inside. | So today, let's open one up and see what's inside. | natural |
| l05 | A model is basically a machine: you feed an input in one end, and an answer comes out the other. | A model's basically a machine. You put something in one end, an answer comes out the other. | natural |
| l06 | And on this machine, there's a row of knobs. Turn them to different positions, and the same input gives a different answer. | The machine has a row of knobs, and if you turn them, the same input gives a different answer. | natural |
| l07 | Those knobs are the parameters. | Those knobs are the parameters. | natural |
| l08 | Here's an example: guessing a taxi fare. What goes in is how many kilometers the ride was, and what comes out is a guess at the price. | Say you're guessing a taxi fare. You put in the distance, and out comes a price guess. | natural |
| l09 | At its simplest, this machine needs just two knobs: one for the base fare, and one for the price per kilometer. | The simplest version needs two knobs: a base fare and a price per kilometer. | natural |
| l10 | To make a guess, it takes the base fare and adds the per-kilometer price times the distance. | It takes the base fare, then adds the per-kilometer price times the distance. | natural |
| l11 | Say the base fare is set to ten dollars and the per-kilometer knob to two dollars. For a five-kilometer ride, it guesses twenty dollars. | Say the base is ten bucks and it's two bucks a kilometer. Five kilometers, so twenty dollars. | natural |
| l12 | People decide how the machine does its math. But where each knob is set? Nobody types that in. The machine learns it from examples. | People design the math, but nobody types in the knob settings. The machine learns them from examples. | natural |
| l13 | That's all "learning" is: turning the knobs to the right positions. | That's all learning is: getting the knobs to the right spots. | natural |
| l14 | Here are twelve taxi rides. It's made-up data, just for illustration, not real receipts. | Here are twelve taxi rides. I made them up, they're not real receipts. | natural |
| l15 | Each dot is one ride: the further right, the longer the trip, and the higher up, the more it cost. | Each dot is a ride. Further right is a longer trip, higher up is a pricier one. | natural |
| l16 | Draw the model's guesses, and you get a straight line that gives a fare for every distance. | The model's guesses make a straight line, one fare for every distance. | natural |
| l17 | The little vertical line from each dot to that line shows how far off the guess was for that ride. | Each little vertical line shows how far off the guess was for that ride. | natural |
| l18 | Let's start with the knobs set pretty much at random: zero base fare, a dollar per kilometer. The line's way too low, and every ride gets underestimated. | Start with random-ish settings: no base fare, a dollar a kilometer. The line's way too low, every ride is underestimated. | natural |
| l19 | Turn the base fare up to ten dollars, and the whole line lifts up. | Crank the base fare to ten dollars and the whole line lifts. | natural |
| l20 | Now the short rides are pretty close, but the longer the ride, the further off it gets. | Short rides are close now, but the longer the ride, the worse it gets. | natural |
| l21 | So turn the per-kilometer knob, and the line gets steeper. At three fifty a kilometer, we've gone too far: now the long rides are overestimated. | So turn the per-kilometer knob and the line gets steeper. At three-fifty a kilometer we've overshot, and long rides are overestimated. | natural |
| l22 | Turn it back a little, to a base fare of about ten twenty and about two fifty per kilometer. | Back it off a bit: about ten dollars twenty base, about two-fifty a kilometer. | a bit off (ambiguous spoken numbers) |
| l23 | Now the line runs right along the dots, and all those little vertical lines are short. | Now the line hugs the dots and all the little vertical lines are short. | natural |
| l24 | Once it's tuned, you can actually use it. So ask it: what would an eight-kilometer ride cost? | Now it's tuned, we can use it. How much for an eight-kilometer ride? | natural |
| l25 | None of our twelve rides was eight kilometers, but it can still make a guess: about thirty fifty. | None of our twelve rides was eight kilometers, but it still guesses: about thirty dollars fifty. | a bit off (thirty fifty) |
| l26 | So what did this machine actually learn? Just the two readings on its knobs. | So what did it actually learn? Just the two knob readings. | natural |
| l27 | Everything it picked up from those twelve rides lives in these two numbers. | Everything it got from those twelve rides is in these two numbers. | natural |
| l28 | The machine itself hasn't changed one bit. The only thing that's different is where the knobs are set. | The machine itself didn't change. Only the knob settings did. | natural |
| l29 | Copy those two numbers onto a scrap of paper, hand it to a friend, and they've got the exact same model. | Write those two numbers on a scrap of paper, hand it to a friend, and they've got the same model. | natural |
| l30 | So when people talk about "training a model," what they're really doing is turning knobs. | So when people say "training a model," they just mean turning knobs. | natural |
| l31 | And "the model has learned" means the knobs are now in the right positions. | And "it's learned" means the knobs are in the right spots. | natural |
| l32 | Two knobs are plenty for guessing a taxi fare. But if you want a model to write essays or chat with people, you need way, way more. | Two knobs is fine for a taxi fare. To write essays or chat, you need way, way more. | natural |
| l33 | In twenty twenty, OpenAI released GPT-3, which has a hundred and seventy-five billion parameters. | In 2020 OpenAI released GPT-3, with 175 billion parameters. | natural |
| l34 | That's a hundred and seventy-five billion knobs. | That's 175 billion knobs. | natural (repeat) |
| l35 | How many is that? Read out one knob setting every second, no eating, no sleeping, and it'd take you over five and a half thousand years. | How many is that? Read one setting per second, no eating or sleeping, and you'd need over 5,500 years. | natural |
| l36 | Obviously, nobody turned all those knobs by hand. Their settings came from training on huge amounts of text. | Obviously nobody turned them by hand. The settings came from training on tons of text. | natural |
| l37 | But the idea is the same as with the taxi fare: people decide how the machine does its math, and the settings are learned from examples. | But it's the same idea as the taxi fare: people design the math, the settings are learned from examples. | natural |
| l38 | And a trained model, saved to a file, is mostly just this long, long list of knob settings. | And a trained model saved to a file is mostly just a huge list of knob settings. | natural |
| l39 | So when the news says "over a hundred billion parameters," it means the machine has over a hundred billion knobs. | So when the news says "a hundred billion parameters," that's a hundred billion knobs. | natural |
| l40 | So a model is a machine with knobs, and the parameters are those knobs. | So: a model is a machine with knobs, and the parameters are the knobs. | natural |
| l41 | And learning just means turning the knobs to the right positions. | And learning is just turning them to the right spots. | natural |
| l42 | But what does "the right positions" actually mean? | But what counts as "the right positions"? | natural |
| l43 | Those little vertical lines were some long, some short. So how do you tell whether one setting is good or bad? | Remember those vertical lines, some long, some short? How do you tell if a setting's good or bad? | natural |
| l44 | That's next time, when we talk about loss functions. | That's next time: loss functions. | natural |

## 问题表
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l25 | V3 | 建议 | about thirty fifty | Spoken "thirty fifty" is easy to mishear (30-50? a range?). Answer is $30.52. | about thirty dollars fifty. |
| l22 | V3 | 建议 | a base fare of about ten twenty and about two fifty per kilometer | "ten twenty" sounds like a time or a range; no currency unit. | Back it off a bit: about ten dollars twenty base, two-fifty a kilometer. |
| l34 | V4 | 建议 | That's a hundred and seventy-five billion knobs. | Repeats l33 with one word swapped, though it ties parameter to knob at the number's moment. Could merge. | (merge into l33) In 2020, GPT-3 came out with 175 billion parameters. That's 175 billion knobs. |
| l37 | V4 | 记录 | But the idea is the same as with the taxi fare: people decide how the machine does its math, and the settings are learned from examples. | Near-verbatim repeat of l12. Works as a callback, but could be shorter. | But it's the same idea as the taxi fare: people design the math, the machine learns the settings. |
| l44 | V3 | 存疑 | when we talk about loss functions | "Loss functions" is a new term in the teaser; fine as a tease, a casual viewer may not retain it. | That's next time: how we score a setting, what people call a loss function. |

Top 5 most awkward (all mild): l25, l22, l34, l37, l44.

## 整体观察
- Strict items (cold open l01-l04, outro l40-l44, chapter transitions): no TOC-reading, no "noun phrase + and how to..." pattern, nothing 必改.
- Keep: the cold open question "So what actually is a parameter?" right after the news line is a real hook.
- Keep: the knob metaphor is used consistently and the taxi example is concrete.
- Keep: l35 (5,500 years of reading) and l29 (scrap of paper) are vivid and sound spoken.
- l43 calls back to the vertical lines from l17, far earlier; "Remember those vertical lines" (see retell) helps an ear-only listener.
- l39 closes the loop with l01 nicely; the repeats l34/l37/l40-l41 are mild and defensible.
- Spoken currency numbers (l22, l25) are the only real hearing risk.
