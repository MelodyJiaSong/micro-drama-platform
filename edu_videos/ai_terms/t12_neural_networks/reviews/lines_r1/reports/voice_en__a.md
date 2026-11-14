# voice_en__a report (round 1, blind, ear only)

## 评分表
- V1 2 证据：Most lines sound spoken ("Remember our two-knob taxi-fare machine?", l01; "The fix isn't one big machine. It's lots of simple little ones.", l14). Off spots: l33 "In a worked example," l43 "A version of it had a fifteen point three percent error rate, against…", l21 "That one weighs each bent line".
- V2 2 证据：Cold open l01-l04 flows as one thought and the agenda (l05-l06) is a real sentence pair, not a TOC. Weak spots: l30 teases "next episode's story" mid-video, then l50-l51 repeat the tease; l31 "So far, our units sat side by side" is a good chapter bridge but l33 "In a worked example" drops in with no setup.
- V3 2 证据：l12 "its loss can't get below eleven point five" uses "loss" with no ear-level definition, and "11.5 / 26.6" are hard to hold; l34-l35 "pieces" (one layer gives two pieces, ten units give at most eleven) is never defined by ear; l21 "That one" is ambiguous after l20 names two layers.
- V4 2 证据：l36 "Later layers reuse what earlier ones already folded" and l37 "the deeper the stack, the more complex the shapes" say nearly the same thing; l28 "Rush hours and late nights, it catches them all" is mostly filler after l27; l49 "recognize really complicated things" is vague.
- V5 2 证据：Warm, consistent narrator. Rhythm is mostly good with short punchy lines (l22 "That's thirty-seven knobs in total."), but l43 (8.1s) and l44 (8.5s) are long and cannot be said in one breath comfortably; l50 (7.7s) is a three-clause sentence.
- V6 2 证据：Drop-in rewrites provided below for all flagged lines; top five most awkward: l50, l43, l21, l33, l12.

## 逐句复述
| 句号 | 原句 | 跟朋友会怎么说 | 判 |
|---|---|---|---|
| l01 | Remember our two-knob taxi-fare machine? It learned distance and fare just fine. | Remember that taxi-fare machine with two knobs? It figured out distance versus fare fine. | natural |
| l02 | But fares also depend on the time: rush hour costs more, and late night a little more too. | But fares change with the time of day too. Rush hour's pricier, and late at night costs a bit more. | natural |
| l03 | That, it can't learn, because all it can draw is a straight line. | It can't learn that, though. All it can draw is a straight line. | a bit off (fronted "That, it can't learn") |
| l04 | So how does a machine learn a pattern that bends? With a neural network. | So how do you get a machine to learn a bendy pattern? A neural network. | natural |
| l05 | Last time, we turned the knobs by walking downhill blindfolded, toward wherever the score drops fastest. | Last time we turned the knobs like walking downhill blindfolded, always heading where the score drops fastest. | natural |
| l06 | Today we'll build a tiny network that learns the bend, and see why going deeper helps. | Today we'll build a tiny network that learns the bend, then see why going deeper helps. | natural |
| l07 | Here's some made-up data: the same five-kilometer ride, forty-eight times, at different hours of the day. | Here's some made-up data: the same five-kilometer ride, taken forty-eight times at different hours. | natural |
| l08 | Daytime runs about twenty-three dollars, just what our two-knob machine charges. | In the daytime it's about twenty-three bucks, which is what our machine would charge. | natural |
| l09 | Around eight a.m. and six p.m. it spikes, and late at night it's a bit pricier. | Around eight in the morning and six at night it spikes, and late at night it's a bit higher. | natural |
| l10 | Same two knobs, one for height and one for slope, but now we feed it the time, not the distance. | Same two knobs, one for height, one for slope. But now we give it the time instead of the distance. | natural |
| l11 | However you turn them, the best you get is a nearly flat line through the middle. | Whatever you do with them, the best you get is a nearly flat line through the middle. | natural |
| l12 | It's too cheap at rush hour and too pricey by day, and its loss can't get below eleven point five. | It's too cheap at rush hour and too expensive in the day. Its error never gets below eleven point five. | a bit off ("loss" not yet explained by ear) |
| l13 | The knobs aren't the problem: this machine only draws straight lines, and the pattern bends. | The knobs aren't the issue. The machine only draws straight lines and the pattern bends. | natural |
| l14 | The fix isn't one big machine. It's lots of simple little ones. | Natural as is. | natural |
| l15 | Each unit still has two knobs and draws a line, plus one rule: anything below zero becomes zero. | Each little unit still has two knobs and draws a line, with one rule: anything below zero becomes zero. | natural |
| l16 | So its line stays flat, then bends upward. | So the line stays flat, then bends up. | natural |
| l17 | The two knobs set where it bends and how steeply. | The knobs decide where it bends and how steep it gets. | natural |
| l18 | One bend isn't enough, so add more units that bend in different spots. | One bend isn't enough, so we add more units that bend in different places. | natural |
| l19 | Add them up, and you can build bumps, steps, almost any curve. | Add them together and you can make bumps, steps, pretty much any curve. | natural |
| l20 | Our network has twelve units side by side in the first layer, and one unit in the second. | Our network has twelve units side by side in the first layer, and just one in the second. | natural |
| l21 | That one weighs each bent line with its own knob, adds one more knob, and out comes the fare. | That last unit takes each bent line, gives it its own knob, adds one more knob, and out comes the fare. | a bit off ("That one weighs") |
| l22 | That's thirty-seven knobs in total. | Natural as is. | natural |
| l23 | Layers of little units like this are what we call a neural network. | Layers of little units like this are what we call a neural network. | natural |
| l24 | The name comes from neurons in the brain, but don't take that too seriously: it's just little units with knobs. | The name comes from brain neurons, but don't read much into that. It's just little units with knobs. | natural |
| l25 | To turn all thirty-seven, we use last episode's trick, nudging every knob whichever way drops the loss fastest. | To set all thirty-seven, we use last episode's trick: nudge every knob whichever way drops the error fastest. | a bit off ("loss", long) |
| l26 | It starts as a random squiggle, and step by step it bends toward the peaks. | It starts as a random squiggle, then bit by bit it bends toward the peaks. | natural |
| l27 | After ten thousand steps, the loss is down to zero point two six, while the best straight line managed eleven point five. | After ten thousand steps the error is down to zero point two six. The best straight line only got eleven point five. | a bit off (long, number-heavy) |
| l28 | Rush hours and late nights, it catches them all. | It catches the rush hours and the late nights. | natural |
| l29 | And every corner on this curve is one little unit making its bend. | And every corner in this curve is one little unit making its bend. | natural |
| l30 | How we work out which way each knob should turn is next episode's story. | How we work out which way to turn each knob? That's for next episode. | a bit off (nominalized, "story") |
| l31 | So far, our units sat side by side, each adding one bend. | So far our units sit side by side, each adding one bend. | natural |
| l32 | Now stack them instead, so each layer folds the line it gets from the layer before. | Now stack them instead, so each layer folds the line it gets from the one before. | natural |
| l33 | In a worked example, two units per layer can fold a slanted line exactly in half. | Take two units per layer. They can fold a slanted line exactly in half. | a bit off ("In a worked example") |
| l34 | One layer gives two pieces, two layers give four, and each new layer can double it. | One layer gives you two pieces, two layers give four, and every new layer doubles it. | a bit off ("pieces" undefined) |
| l35 | So ten units side by side give at most eleven pieces. Stacked five deep, they can give thirty-two. | So ten units side by side give at most eleven pieces, but stacked five deep they can give thirty-two. | natural |
| l36 | Later layers reuse what earlier ones already folded. | Later layers reuse what earlier ones already folded. | natural |
| l37 | So the deeper the stack, the more complex the shapes the same units can build. | So the deeper the stack, the more complex the shapes you can build. | natural |
| l38 | That's the "deep" in deep learning. | Natural as is. | natural |
| l39 | In twenty twelve, three researchers at the University of Toronto trained a very deep neural network. | In 2012, three researchers at the University of Toronto trained a really deep neural network. | natural |
| l40 | They were Krizhevsky, Sutskever and Hinton, and the network later became known as AlexNet. | They were Krizhevsky, Sutskever and Hinton, and the network became known as AlexNet. | natural |
| l41 | It had eight layers and sixty million knobs, and learned a thousand categories from one point two million photos. | It had eight layers and sixty million knobs, and it learned a thousand categories from one point two million photos. | a bit off (dense) |
| l42 | At that year's ImageNet contest, it got five guesses per picture, and only missed if all five were wrong. | At that year's ImageNet contest it got five guesses per picture, and only counted as wrong if all five missed. | natural |
| l43 | A version of it had a fifteen point three percent error rate, against twenty-six point two percent for the runner-up. | A version of it was wrong fifteen point three percent of the time. The runner-up was wrong twenty-six point two. | a bit off (written-style, long) |
| l44 | Nobody told it what to look for, yet its first layer learned to spot stripes at all angles, and patches of color. | Nobody told it what to look for, yet its first layer learned stripes at every angle and patches of color. | a bit off (long) |
| l45 | Later layers built on those, layer by layer. | Later layers built on those, step by step. | natural |
| l46 | They also found that removing any middle layer cost about two percentage points. | They also found that cutting any middle layer cost about two percentage points. | natural |
| l47 | As the paper put it, "the depth really is important." | As the paper said, "the depth really is important." | natural |
| l48 | So a neural network is just simple little units with knobs, stacked layer on layer. | So a neural network is just simple little units with knobs, stacked in layers. | natural |
| l49 | Stack them deep enough, and they can recognize really complicated things. | Stack them deep enough and they can recognize really complicated stuff. | a bit off (vague) |
| l50 | Thirty-seven knobs is easy, but AlexNet had sixty million, so how do you work out which way each one turns? | Thirty-seven knobs is easy. But AlexNet had sixty million. How do you figure out which way each one turns? | a bit off (one run-on) |
| l51 | That's backpropagation, coming up next time. | That's backpropagation, and it's coming next time. | natural |

## 问题表
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l50 | V5 | 必改 | Thirty-seven knobs is easy, but AlexNet had sixty million, so how do you work out which way each one turns? | Outro line (strict item): a three-clause run-on; "but ... so how" is hard to say in one breath. Also repeats l30's tease. | Thirty-seven knobs is easy. AlexNet had sixty million. How do you know which way to turn each one? |
| l30 | V2 | 必改 | How we work out which way each knob should turn is next episode's story. | Noun-clause subject plus "story" is written style; it is a linking line (strict). | Which way should each knob turn? That's for next episode. |
| l21 | V3 | 必改 | That one weighs each bent line with its own knob, adds one more knob, and out comes the fare. | "That one" is ambiguous after two layers; "weighs" is unclear by ear. | The last unit gives each bent line its own knob, adds one more, and out comes the fare. |
| l12 | V3 | 建议 | its loss can't get below eleven point five | "Loss" is heard for the first time with no meaning; viewers who missed the previous episode will not follow. | its error never gets below eleven point five. |
| l33 | V1 | 建议 | In a worked example, two units per layer can fold a slanted line exactly in half. | Textbook phrasing ("In a worked example"). | Take two units per layer: they can fold a slanted line exactly in half. |
| l43 | V1 | 建议 | A version of it had a fifteen point three percent error rate, against twenty-six point two percent for the runner-up. | Written-style, number-heavy; "had an error rate against" is not spoken. | A version of it was wrong fifteen point three percent of the time. The runner-up: twenty-six point two. |
| l34 | V3 | 建议 | One layer gives two pieces | "Pieces" is never defined by ear (pieces of what?). | One layer cuts the line into two straight pieces, two layers into four, and each new layer can double that. |
| l03 | V1 | 建议 | That, it can't learn, because all it can draw is a straight line. | Fronted object sounds stagey. | It can't learn that, because all it can draw is a straight line. |
| l25 / l27 | V3 | 建议 | the loss is down to zero point two six | Same "loss" term; mixes with 11.5 and 0.26. | the error is down to zero point two six, while the best straight line only managed eleven point five. |
| l36 / l37 | V4 | 建议 | Later layers reuse... / So the deeper the stack... | Two lines make one point. | Drop l36, or merge: Later layers reuse earlier folds, so a deeper stack builds more complex shapes. |
| l28 | V4 | 记录 | Rush hours and late nights, it catches them all. | Filler after l27; could go without loss. | (cut or keep as a beat) |
| l44 | V5 | 记录 | Nobody told it what to look for, yet its first layer learned to spot stripes at all angles, and patches of color. | 8.5s, hard in one breath. | Nobody told it what to look for, yet its first layer learned stripes at every angle, and patches of color. |
| l49 | V4 | 记录 | they can recognize really complicated things | Vague; "really complicated things" is a truism. | Stack them deep enough, and they can recognize faces, words, whole scenes. |

## 整体观察
- Overall the narration sounds like a person, and the cold open and agenda (l01-l06) are natural: no TOC-reading.
- Biggest risk is the ending: l50 is a run-on and l30 plus l50-l51 tease the same cliffhanger twice.
- "Loss" (l12, l25, l27) is used without an ear-level definition; swap for "error" or define it once.
- "Pieces" in the depth chapter (l34-l35) needs one setup phrase.
- Keep: (1) the cold open's taxi-fare callback l01-l04; (2) the blindfolded-downhill recap in l05; (3) the closing summary l48 plus the "depth really is important" quote l47.
