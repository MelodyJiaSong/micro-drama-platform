# t00 What Is AI — Script

> In one sentence: Most of today's AI isn't built on rules people write. It learns patterns from examples.

English version of `script.md` (v3, 2026-11-09): about 5 minutes, five chapters, no agenda card; drafted "speak first" by a native narrator from the beat sheet only (no old wording, `reviews/lines_r1/materials/draft/v3_en.md`), then aligned line by line with the Chinese script. v2.3 is kept as `script_v2.en.md`.
Each `- lNN: text` is one narration line, subtitle and animation cue; `{display|spoken}` shows the first part in subtitles and has the voice say the second; `[pause N]` adds N seconds after the line.

## s0 Cold open [cold open]
- l01: Your phone can find your cat in your photos, yet nobody ever gave it rules for what a cat looks like.
- l02: So how does it do it? It saw tons of examples and worked out the patterns itself. That's today's AI.

## s2 When rules fall short [chapter:problem]
- l03: A traditional program works differently: people write the rules one by one, and the computer follows them.
- l04: For payroll or booking flights, the rules are clear, so that's enough.
- l05: But some things are hard to write rules for, like reading a handwritten three. Fat, skinny, tilted, you know it instantly.
- l06: Now try writing down how. "Two curves stacked"? So is an eight. "Bottom half opens left"? So does a five.
- l07: Rules like that miss some threes and mistake other digits for threes.

## s3 A different approach
- l08: So most of today's AI flips it around: no rules, just examples.
- l09: Show the computer hundreds or thousands of handwritten digits, each with its answer: this is a three, this is a seven.
- l10: It finds the patterns itself, and that's called machine learning.
- l11: What it learns is called a model. Show the model a new image, and it gives you an answer.
- l12: A lot of people think programmers coded in everything AI can do. Mostly, it learned from examples, which we call data.

## s5 A small experiment [chapter:experiment]
- l17: Let's actually try it, with nearly {1,800|eighteen hundred} handwritten digits, each a tiny {8×8|eight-by-eight} grid.
- l18: First we lock away {300|three hundred} as the test, and the rest are examples to learn from.
- l19: Learning from them is called training, and during training it never sees a test question.
- l20: Only questions it hasn't seen can show whether it truly learned, or just memorized.
- l21: So, take a guess: with just {10|ten} examples, how much of the test does it get right? [pause 1.5]
- l22: Pick ten at random, and often some digits don't show up at all.
- l23: We tried twenty different random sets of ten. The typical score was about {37%|thirty-seven percent}: better than the {10%|ten percent} you'd get guessing, but still low.
- l24: With a hundred examples, it gets {88%|eighty-eight percent}. With all {1,500|fifteen hundred} or so, it gets {97%|ninety-seven percent}.
- l25: We never gave it rules for a three, just told it which ones were threes. In this experiment, more examples meant better scores.
- l26: Still, it missed {10|ten} of the {300|three hundred}, like this messy two it called a one.

## s6 A different lens [chapter:lens]
- l27: Here's another way to see it: today's AI is a prediction machine. Not predicting the future, just seeing something and guessing the answer.
- l28: Our model also says how sure it is. It's {96%|ninety-six percent} sure this one's a three.
- l30: Other AI works the same way. Give a language model half a sentence, and it guesses the next word, then the next, until there's a whole answer.
- l31: Chatbots built on large language models reply this way.
- l32: They guess well, but a convincing answer can still be wrong.

## s7 Circles within circles
- l33: So how do all these terms fit together? Picture AI, artificial intelligence, as the biggest circle: computers doing things that seem to take smarts.
- l34: A chess program built on hand-written rules counts as AI. A plain payroll program doesn't.
- l35: Inside AI is machine learning, and inside that, deep learning, which runs on neural networks: many layers of simple math.
- l36: "Deep" just means many layers, not deep understanding. Large language models are built with deep learning.
- l37: When I say "today's AI," I mean machine learning: AI that learns from examples.

## s8 One real example [chapter:real]
- l38: Learning from data can go wrong, too. According to Reuters, Amazon once tried using AI to screen résumés.
- l39: It learned from {10|ten} years of résumés sent to the company, mostly by men.
- l40: In effect, it taught itself that male candidates were better.
- l41: Résumés with the word "women's," as in "women's chess club captain," got marked down.
- l42: The tool was later scrapped. If the data is biased, the model can pick that up too.

## s9 Three things to remember [chapter:fix]
- l43: When you use AI, remember three things.
- l44: First, it may answer anyway, even about things it's never seen. Show our digit model the letter A, and it still has to pick from zero to nine.
- l45: It says it's {92%|ninety-two percent} sure that's a four. But it can only pick from the ten digits.
- l46: A kid would say, "That's not a number." The model won't.
- l47: Second, it gives you predictions, not the truth. Remember that messy two? The model was {81%|eighty-one percent} sure it was a one, and it was wrong.
- l48: Third, what it gets right or wrong depends on its data, and also on how it's designed and trained.
- l49: So to judge whether an AI is reliable, first find out what data it learned from.
- l50: Whenever an AI sounds totally sure, ask yourself: has it seen questions like this before?

## s10 Outro [package:outro]
- l51: Most of today's AI isn't built on rules people write. It learns patterns from examples.
- l52: Next time, we'll look at why a model can ace the practice questions and still stumble on new ones. That's often a sign of overfitting.
