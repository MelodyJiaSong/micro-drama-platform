# voice_en__a report (round 1, blind, claude-sonnet-5-5)

## 评分表
- V1 2 证据：most lines sound spoken ("Now try writing down how.", "take a guess", "A kid would say, 'That's not a number.'"); off spots are l52 "Next time: overfitting, or why…", l32 "sounding smooth doesn't guarantee being right", l35 "made of many layers of simple calculations".
- V2 2 证据：cold open l01→l02 ("So how does it do it?") and the digit story l05→l07 flow like one person thinking; but l43–l48 "One: / Two: / Three:" reads as a numbered template, and l52 is a headline-plus-"or why" outro.
- V3 2 证据：one idea per line mostly holds, "Fat, skinny, tilted" lands instantly; but l17 "seventeen ninety-seven" sounds like a year, l26 "like this messy two" and l28 "this one's a three" point at visuals an ear cannot see, l23 "Do that twenty times" has a fuzzy referent.
- V4 2 证据：l16 "a model needs way more examples, as you'll see" and l19+l20 (training/never sees test, then "only unseen questions can show…") repeat each other; l12 "Mostly, it learned from examples" repeats l08–l10.
- V5 2 证据：one warm narrator throughout, good short/long mix (l46 "The model won't." vs l30); l35 (9.2s, two ideas + a term) and l33 are not one-breath lines.
- V6 2 证据：every off line below has a drop-in rewrite no longer than the original; top five ranked in 整体观察.

## 逐句复述
| 句号 | 原句 | 跟朋友会怎么说 | 判 |
|---|---|---|---|
| l01 | Your phone can find your cat in your photos, yet nobody ever gave it rules for what a cat looks like. | Your phone can find your cat in your photos, and nobody ever told it what a cat looks like. | natural |
| l02 | So how does it do it? It saw tons of examples and worked out the patterns itself. That's today's AI. | Same. | natural |
| l03 | A traditional program works differently: people write the rules one by one, and the computer follows them. | An old-school program works differently. Somebody writes every rule, and the computer just follows them. | natural |
| l04 | For payroll or booking flights, the rules are clear, so that's enough. | For payroll or booking flights, the rules are clear, so that works fine. | natural |
| l05 | But some things resist rules, like reading a handwritten three. Fat, skinny, tilted, you know it instantly. | But some things are hard to put into rules, like a handwritten three. Fat, skinny, tilted, you still know it instantly. | a bit off ("resist rules") |
| l06 | Now try writing down how. "Two curves stacked"? So is an eight. "Bottom half opens left"? So does a five. | Same. | natural |
| l07 | Rules like that miss some threes and mistake other digits for threes. | Rules like that miss some threes, and call other digits threes. | natural |
| l08 | So most of today's AI flips it around: no rules, just examples. | Same. | natural |
| l09 | Show the computer hundreds or thousands of handwritten digits, each with its answer: this is a three, this is a seven. | Show it hundreds or thousands of handwritten digits, each labeled: this is a three, this is a seven. | natural |
| l10 | It finds the patterns itself, and that's called machine learning. | It finds the patterns itself. That's machine learning. | natural |
| l11 | What it learns is called a model. Show the model a new image, and it gives you an answer. | What it ends up with is called a model. Give it a new image and it tells you what it thinks. | natural |
| l12 | A lot of people think programmers typed in everything AI can do. Mostly, it learned from examples, which we call data. | People think programmers typed in everything AI can do. Mostly it learned it from examples. We call those data. | natural |
| l13 | It's like teaching a kid numbers. You don't hand them a manual saying "a three is two half-circles stacked." | It's like teaching a kid numbers. You wouldn't give them a manual that says a three is two half-circles. | natural |
| l14 | You just keep pointing and saying, "That's a three." Eventually they get it, even in handwriting they've never seen. | Same. | natural |
| l15 | What the kid learns is the model. The number, plus "that's a three," is an example with its answer. | The kid's understanding is the model. And the number plus "that's a three" is one example. | a bit off (hard to follow by ear) |
| l16 | One difference: a model needs way more examples, as you'll see. | One difference: a model needs way more examples. You'll see. | natural |
| l17 | Let's actually try it. Here's a public set of seventeen ninety-seven handwritten digits, each a tiny eight-by-eight grid. | Let's try it. There's a public set of about eighteen hundred handwritten digits, each a tiny eight-by-eight grid. | a bit off (sounds like the year 1797) |
| l18 | First we lock away three hundred as the test, and the rest are examples to learn from. | First we lock away three hundred for a test. The rest are what it learns from. | natural |
| l19 | Learning from them is called training, and during training it never sees a test question. | Learning from those is called training, and it never gets a peek at the test. | natural |
| l20 | Only questions it hasn't seen can show whether it truly learned, or just memorized. | Only questions it hasn't seen tell you if it really learned or just memorized. | natural |
| l21 | So, take a guess: with just ten examples, how much of the test does it get right? | Same. | natural |
| l22 | Pick ten at random, and often some digits don't show up at all. | Same. | natural |
| l23 | Do that twenty times, and it usually scores about thirty-seven percent. That beats the ten percent you'd get guessing, but it's a long way off. | Run it twenty times and it usually scores about thirty-seven percent. That beats guessing, which is ten, but it's not good. | a bit off ("Do that" unclear) |
| l24 | With a hundred examples, it gets eighty-eight percent. With all of the nearly fifteen hundred, it gets ninety-seven percent. | Same. | natural |
| l25 | Nobody told it what a three looks like, only which images were threes. In this experiment, more examples meant better scores. | Same. | natural |
| l26 | Still, it missed ten of the three hundred, like this messy two it called a one. A few would make anyone hesitate. | Still, it got ten of the three hundred wrong, like a messy two it called a one. Honestly, a person might hesitate on a few of those. | a bit off ("like this") |
| l27 | Here's another way to see it: today's AI is a prediction machine. Not predicting the future, just seeing something and guessing the answer. | Here's another way to think about it: today's AI is basically a prediction machine. Not of the future, it just looks at something and guesses. | natural |
| l28 | Our model also says how sure it is. It's ninety-six percent sure this one's a three. | Our model also says how sure it is. Here it's ninety-six percent sure it's a three. | a bit off ("this one") |
| l29 | Other AI works the same way. Image models guess whether a photo has a cat in it. | Same. | natural |
| l30 | Give a language model half a sentence, and it guesses the next word, then the next, until there's a whole answer. | Same. | natural |
| l31 | That's how the large language models you chat with reply. | That's how chatbots write back to you. | natural |
| l32 | They guess well and learn a lot from data, but sounding smooth doesn't guarantee being right. | They guess pretty well, but just because it sounds smooth doesn't mean it's right. | a bit off (gerund, written) |
| l33 | These terms nest like circles. The outermost is AI, artificial intelligence: computers doing things that seem to take smarts. | These terms nest inside each other, like circles. The biggest is AI, computers doing things that seem to take smarts. | a bit off (lecture tone) |
| l34 | A chess program built on hand-written rules counts as AI. A plain payroll program doesn't. | Same. | natural |
| l35 | Inside AI is machine learning, and inside that is deep learning. It uses models called neural networks, made of many layers of simple calculations. | Inside AI is machine learning, and inside that, deep learning, which uses neural networks: lots of layers of simple math. | a bit off ("It uses", too packed) |
| l36 | "Deep" just means many layers, not deep understanding. Large language models are built with deep learning. | Same. | natural |
| l37 | So when this episode says "today's AI," it means the machine learning circle. | So when I say "today's AI," I mean the machine learning circle. | a bit off ("this episode") |
| l38 | Learning from data can go wrong, too. According to Reuters, Amazon once tried using AI to screen résumés. | Learning from data can go wrong. Reuters reported that Amazon once tried using AI to screen résumés. | natural |
| l39 | It learned from ten years of résumés sent to the company, mostly by men. | It learned from ten years of résumés, and most came from men. | natural |
| l40 | So in effect, it taught itself that male candidates were better. | So it basically taught itself that men were better candidates. | natural |
| l41 | Résumés with the word "women's," as in "women's chess club captain," got marked down. | Same. | natural |
| l42 | The tool was later scrapped. Whatever bias is in the data, a model can learn that too. | They scrapped it. Whatever bias is in the data, a model can pick it up too. | natural |
| l43 | So when you use AI, remember three things. | Okay, so here are three things to keep in mind when you use AI. | a bit off (strict: linking line) |
| l44 | One: it'll answer even things it never learned. Show this digit model the letter A, and it can only pick from zero to nine. | First, it'll answer things it never learned. Show this digit model an A and it still has to pick a number from zero to nine. | a bit off (strict: "One:" template) |
| l45 | It says it's ninety-two percent sure it's a four, but that only means four looked closest of the ten. | It says it's ninety-two percent sure it's a four, but that just means four looked closest. | natural |
| l46 | A kid would say, "That's not a number." The model won't. | Same. | natural |
| l47 | Two: it gives predictions, not truth. That messy two? It was eighty-one percent sure it was a one, and it was wrong. | Second, it gives predictions, not facts. That messy two? It was eighty-one percent sure it was a one, and it was wrong. | a bit off (strict: "Two:" template) |
| l48 | Three: its strengths and flaws come from its data, and also from how it's designed and trained. | Third, it's only as good as what it learned from, and how it was built. | a bit off (written; "strengths and flaws come from") |
| l49 | So to judge whether an AI is reliable, first ask what data it learned from. | So to know if an AI is reliable, first ask what it learned from. | natural |
| l50 | Next time an AI sounds totally sure, ask yourself: has it ever learned this kind of question? | Next time an AI sounds totally sure, ask yourself: has it ever seen this kind of question? | a bit off ("learned this kind of question") |
| l51 | In a sentence: today's AI mostly doesn't run on rules people write. It learns patterns from examples on its own. | In short: today's AI mostly doesn't run on rules people write. It learns patterns from examples. | natural |
| l52 | Next time: overfitting, or why a model can ace the practice questions and still stumble on new ones. | Next time, we'll look at why a model can ace the practice questions and still flop on new ones. That's called overfitting. | clearly off (strict: outro, "X, or why Y" headline) |

## 问题表
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l52 | V1/V2 | 必改 | Next time: overfitting, or why a model can ace the practice questions and still stumble on new ones. | Strict outro. Headline-style "Next time: [term], or why…" is a topic list, not speech; the unexplained term lands first and gets lost. | Next time: why a model can ace the practice questions and still flop on new ones. It's called overfitting. |
| l44 | V2 | 必改 | One: it'll answer even things it never learned. | Strict linking line. Bare "One: / Two: / Three:" is the "Point one…" template; with l43 it is an enumerated recap. | First, it'll answer even things it never learned. |
| l47 | V2 | 必改 | Two: it gives predictions, not truth. | Same template. | Second, it only gives predictions, not facts. |
| l48 | V1/V2 | 必改 | Three: its strengths and flaws come from its data, and also from how it's designed and trained. | Same template plus written-style abstract nouns ("strengths and flaws"); drifts from the data message that l49 then picks up. | Third, it's only as good as its data and how it was built. |
| l43 | V2 | 必改 | So when you use AI, remember three things. | Strict linking line. Flat, instruction-like; "remember three things" is a lecture opener. | Here are three things to keep in mind when you use AI. |
| l17 | V3 | 必改 | a public set of seventeen ninety-seven handwritten digits | Heard as the year 1797; listener may miss that it is a count. Hard number-hearing problem. | a public set of about eighteen hundred handwritten digits |
| l35 | V1/V3 | 建议 | Inside AI is machine learning, and inside that is deep learning. It uses models called neural networks, made of many layers of simple calculations. | 9.2s, three terms in one go; "It" is ambiguous. | Inside that is deep learning, which uses neural networks: many layers of simple math. |
| l32 | V1 | 建议 | sounding smooth doesn't guarantee being right. | Gerund phrasing, written. | but a smooth answer isn't always a right one. |
| l33 | V1/V5 | 建议 | These terms nest like circles. The outermost is AI, artificial intelligence: computers doing things that seem to take smarts. | Lecture tone ("The outermost is…"). | These terms nest like circles. The biggest is AI: computers doing things that seem to take smarts. |
| l15 | V3 | 建议 | The number, plus "that's a three," is an example with its answer. | Hard to parse by ear; "the kid learns is the model" is abstract. | And each "that's a three" is one example. |
| l26 | V3 | 建议 | like this messy two it called a one | "this" depends on the picture. | like a messy two it called a one |
| l28 | V3 | 建议 | It's ninety-six percent sure this one's a three. | "this one" depends on the picture. | It's ninety-six percent sure that one's a three. |
| l23 | V3 | 建议 | Do that twenty times, and it usually scores | "Do that" is unclear. | Try that twenty times and it usually scores |
| l50 | V1 | 建议 | has it ever learned this kind of question? | One does not "learn a question". | has it ever seen this kind of question? |
| l37 | V1 | 建议 | when this episode says "today's AI," | Written; unlike a presenter. | when I say "today's AI," |
| l05 | V1 | 记录 | some things resist rules | Slightly written. | some things are hard to put into rules |
| l16 | V4 | 记录 | One difference: a model needs way more examples, as you'll see. | Can be cut with no loss; l17 shows it. | (cut) |
| l12 | V4 | 记录 | Mostly, it learned from examples, which we call data. | Repeats l08–l10; "which we call data" is the only new bit. | Mostly it learned from examples, or data. |
| l19 | V4 | 记录 | Learning from them is called training, and during training it never sees a test question. | Overlaps with l18/l20. | Learning from them is training, and it never sees the test. |

## 整体观察
- Top 5 most awkward: l52 (outro), l17 ("seventeen ninety-seven"), l44/l47/l48 ("One:/Two:/Three:" template), l35 (packed terms), l32 (written phrasing).
- The cold open (l01–l02) is strong: concrete, a hook question ("So how does it do it?"), no TOC.
- Works, keep: the two-curves/eight/five digit-rule bit (l06); "take a guess" with a 1.9s pause (l21); "A kid would say, 'That's not a number.' The model won't." (l46).
- The old agenda is gone: there is no TOC-style line anywhere; l52 is the one remaining place with that headline rhythm.
- Numbers are many (l17–l24, l28, l45, l47); only l17 is a real hearing problem.
- Several "this/like this" lines (l26, l28, l44) only work with the picture; fragile on audio only.
