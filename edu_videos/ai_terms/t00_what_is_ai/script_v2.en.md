# t00 What Is AI — Script

> In one sentence: Today's AI isn't mainly built from rules people write. It teaches itself patterns from examples.

English version of `script.md` (v2.3, 2026-11-08, final after script review rounds 1–3). Segment ids, line ids and tags match the Chinese script one to one; the wording is rewritten for spoken English, not translated literally. v1 is kept as `script_v1.en.md`.
Each `- lNN: text` is one narration line, subtitle and animation cue; `[pause N]` adds N seconds after the line and is not read.
Spell numbers so the voice reads them correctly when it matters (years, percentages).

## s0 Cold open [cold open]
- l01: Your photo app can spot your cat. Yet nobody had to write down, rule by rule, what a cat looks like.
- l02: So how does it know? In short: you show it lots of examples, and it works out the pattern itself. That's today's AI.

## s1 In this episode [package:agenda]
- l03: Four things today.
- l04: The problem AI is built to solve.
- l05: A child learning their numbers, and a real experiment.
- l06: Seeing AI as a prediction machine.
- l07: What it changes, what can go wrong, and three things to remember.
- l08: You don't need any background.

## s2 Too many rules [chapter:problem]
- l09: Start with a traditional computer program. People write the rules, one by one, and the computer follows them.
- l10: For payroll, or booking a flight, the rules are crystal clear, and that works fine.
- l11: But some tasks are hard to capture in rules. Like recognizing a handwritten three.
- l12: Every one of these is a three, written by hand. Some are fat, some are thin, some slant. You recognize them at a glance.
- l13: But try explaining how. Two bumps, one above the other? An eight has those too. Open on the left at the bottom? So is a five.
- l14: Rules like these can easily miss some threes, or mistake other digits for threes.

## s3 A different approach
- l15: Most of today's AI takes a different approach. Don't write rules. Give examples.
- l16: Show the computer hundreds, even thousands, of handwritten digits, each one with the answer: this is a three, this is a seven.
- l17: It finds the pattern in the examples on its own. That approach is called machine learning.
- l18: The way of telling digits apart that it ends up with is called a model. Hand the model a new image, and it gives you its answer.
- l19: Many people think a programmer typed in everything an AI can do. In fact, most of it was learned from examples. Those examples are called data.

## s4 An analogy [chapter:analogy]
- l20: It's like teaching a child their numbers. You don't hand them a manual that says: a 3 is two half circles, stacked.
- l21: You just point and keep saying, "This is a three." Eventually they get it, even when the three is written in a way they've never seen.
- l22: The way of telling numbers apart that the child picks up is the model. Each digit you point at, plus your "this is a three," is an example with its answer.
- l23: Two things don't match, though. First, a model leans on lots of examples: as you'll see, ours does far better with a hundred than with ten. And a child comes to understand that three means three things. The model has only learned to look at an image and pick an answer.
- l24: Or think about cooking. Sometimes you just follow a recipe, step by step. That's a traditional program. Other times, a seasoned cook goes by feel, built over a thousand dishes of tasting, getting feedback, and adjusting whatever's off.
- l25: Each dish is like the model making a guess. Tasting it and hearing what people think is checking against the right answer. Adjusting when it's off: that's learning. And the feel they end up with is something even the cook can't fully write down.

## s5 Let's run an experiment [chapter:experiment]
- l26: Let's actually try it. Here's a public collection of handwritten digits: {1,797|seventeen hundred ninety-seven} images, each just an eight-by-eight grid.
- l27: First, we lock away three hundred of them as the exam; the rest are the examples it learns from. Learning from examples is called training, and during training the model never sees the exam. Why split it this way? Only questions it has never seen can tell us whether it really learned, or just remembered.
- l28: Take a guess: with just ten examples, how much of the exam would it get right? [pause 1.5]
- l29: Pick ten at random, and usually a few digits don't show up at all. Try it twenty times, and the typical score is about {37%|thirty-seven percent}. That beats random guessing at {10%|ten percent}, but it's still a long way off.
- l30: With a hundred examples: {88%|eighty-eight percent}.
- l31: With all of the nearly fifteen hundred training examples: {97%|ninety-seven percent}.
- l32: At no point did anyone tell it what a three looks like, only which images were threes. In this experiment, more examples meant higher scores. Your photo app finds your cat the same way.
- l33: Still, out of three hundred exam questions, it missed ten. Like this messy two, which it read as a one. A few of them would make a person hesitate too.

## s6 A prediction machine [chapter:lens]
- l34: Here's another way to see it. Today's AI is like a prediction machine. Not predicting the future: predicting the answer for whatever you show it.
- l35: Our model doesn't just guess. It also reports how sure it is. For this image: "96% sure it's a three."
- l36: Other AI works the same way. An image model guesses whether a photo has a cat in it. A speech model guesses which words were said.
- l37: Give a language model half a sentence, and it guesses the next word. Keep going, word after word, and you get a whole reply.
- l38: Large language models, the technology behind chatbots, write their replies this way. They're extremely good at guessing, and they pick up a lot of knowledge from data. But a smooth reply isn't a guarantee of a true one.

## s7 Circles within circles
- l39: These terms nest, circle within circle. The outermost circle is AI, artificial intelligence: getting computers to do things that seem to take intelligence. A chess program built from rules people wrote counts as AI. An ordinary payroll program doesn't.
- l40: Machine learning sits inside AI. Inside that is deep learning. It uses models called neural networks, built from many layers of simple calculations. Don't let the names fool you: these networks are only loosely like neurons in a brain, and "deep" just means many layers, not deep understanding.
- l41: Large language models are built with deep learning. In this episode, "today's AI" means the machine learning circle.

## s8 Real-world impact [chapter:real]
- l42: This ability to learn from data is already changing the real world.
- l43: Finding a protein's shape often took years of lab work. AlphaFold learned from known structures to predict shapes directly.
- l44: Its two lead developers went on to share half of the {2024|twenty twenty-four} Nobel Prize in Chemistry for it.
- l45: About two months after launch, ChatGPT had an estimated hundred million monthly active users.
- l46: But AI can also learn the wrong lessons. According to Reuters, Amazon once tried using AI to screen résumés. That AI learned from ten years of résumés sent to the company, mostly from men.
- l47: In effect, it taught itself that male candidates were preferable. It marked down résumés with the word "women's," as in "women's chess club captain." The tool was later scrapped.
- l48: Bias in the data can be learned right along with everything else.

## s9 Three things to keep in mind [chapter:fix]
- l49: So when you use AI, here are three things to keep in mind.
- l50: One: unfamiliar inputs can fool it. We showed this digit-only model an A. It had to pick from zero to nine. Its answer? "{92%|ninety-two percent} sure it's a four."
- l51: That confidence only compares the ten digits against each other. A child would say, "That's not a number." The model can't.
- l52: Two: it gives predictions, not truth. Remember that messy two? It was {81%|eighty-one percent} sure it was a one, and it was wrong.
- l53: Three: its strengths and flaws come from the data it learned from, and also from how it was designed and trained. To judge whether an AI is trustworthy, first ask what data it learned from.
- l54: Next time an AI answers you with total confidence, ask yourself: has it ever learned this kind of question?

## s10 Outro [package:outro]
- l55: Remember this:
- l56: Today's AI isn't mainly built from rules people write.
- l57: It teaches itself patterns from examples.
- l58: Next time: overfitting. Why can a model ace its practice questions, and still fail new ones?
