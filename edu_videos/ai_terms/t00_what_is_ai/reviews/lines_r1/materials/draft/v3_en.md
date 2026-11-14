## s0 Cold open [cold open]
- l01: Your phone can find your cat in your photos, yet nobody wrote it rules for what cats look like.
- l02: So how? It saw tons of examples and worked out the patterns itself. That's today's AI.

## s2 Too many rules [chapter:problem]
- l03: Traditional programs work differently: people write rules one by one, and the computer follows them.
- l04: For payroll or booking flights, the rules are clear, so that's enough.
- l05: But some things resist rules, like a handwritten three: fat, skinny, tilted, you know it instantly.
- l06: Now write down how. "Two curves stacked"? So is an eight. "Bottom half opens left"? So does a five.
- l07: Rules like that miss some threes and mistake other digits for threes.

## s3 A different approach
- l08: So most of today's AI flips it around: no rules, just examples.
- l09: Show the computer hundreds or thousands of handwritten digits, each with its answer: this is a three, this is a seven.
- l10: It finds the patterns itself, and that's called machine learning.
- l11: What it learns is called a model; show the model a new image, and it answers.
- l12: Many people think programmers typed AI's skills in; mostly, it learned them from examples, which we call data.

## s4 An analogy
- l13: It's like teaching a kid numbers: you don't hand them a manual saying "a three is two stacked half-circles."
- l14: You just keep pointing: "that's a three." Eventually they get it, even in handwriting they've never seen.
- l15: What the kid learns is the model; the number plus "that's a three" is an example with its answer.
- l16: One difference: a model needs way more examples, as you'll see.

## s5 A small experiment [chapter:experiment]
- l17: Let's try it: a public set of {1,797|seventeen ninety-seven} handwritten digits, each a tiny {8×8|eight-by-eight} grid.
- l18: First we lock away {300|three hundred} as the test; the rest are examples to learn from.
- l19: Learning from them is called training, and during training it never sees a test question.
- l20: Only unseen questions show whether it truly learned, or just memorized.
- l21: So, guess: with just {10|ten} examples, how much of the test does it get right?
[pause 1.5]
- l22: Pick ten at random, and often some digits don't show up at all.
- l23: Over twenty tries, it usually scores about {37%|thirty-seven percent}: better than guessing's {10%|ten percent}, but a long way off.
- l24: A hundred examples: {88%|eighty-eight percent}. All of the nearly {1,500|fifteen hundred}: {97%|ninety-seven percent}.
- l25: Nobody told it what a three looks like, only which images were threes. In this experiment, more examples meant better scores.
- l26: Still, it missed {10|ten} of the {300|three hundred}, like this messy two it called a one; a few would make anyone hesitate.

## s6 A different lens [chapter:lens]
- l27: Another lens: today's AI is a prediction machine. Not about the future; it sees something and guesses the answer.
- l28: Our model also says how sure it is: {96%|ninety-six percent} sure this one's a three.
- l29: Other AI works the same way: image models guess whether a photo has a cat.
- l30: Give a language model half a sentence, and it guesses the next word, then the next, until there's a whole answer.
- l31: That's how the large language models you chat with reply.
- l32: They guess well and learn a lot from data, but sounding smooth doesn't guarantee being right.

## s7 Circles within circles
- l33: These terms nest like circles. Outermost is AI, artificial intelligence: computers doing things that seem to take smarts.
- l34: A chess program built on hand-written rules counts; a plain payroll program doesn't.
- l35: Inside AI is machine learning; inside that, deep learning, which uses models called neural networks: simple calculations stacked in many layers.
- l36: "Deep" just means many layers, not deep understanding. Large language models are built with deep learning.
- l37: And "today's AI" in this episode means the machine learning circle.

## s8 One real example [chapter:real]
- l38: Learning from data can go wrong, too. According to Reuters, Amazon once tried using AI to screen résumés.
- l39: It learned from {10|ten} years of résumés sent to the company, mostly by men.
- l40: So in effect, it taught itself male candidates were better.
- l41: Résumés with "women's," like "women's chess club captain," got marked down. The tool was later dropped.
- l42: So it can pick up the data's biases, too.

## s9 Three things to remember [chapter:fix]
- l43: So when you use AI, remember three things.
- l44: One: it'll answer even what it never learned. Show this digit model the letter A; it can only pick zero through nine.
- l45: It's {92%|ninety-two percent} sure it's a four, which only means four was closest of the ten. A kid would say, "That's not a number." It won't.
- l46: Two: it gives predictions, not truth. That messy two? {81%|Eighty-one percent} sure it was a one, and wrong.
- l47: Three: its strengths and flaws come mostly from its data, though design and training matter too.
- l48: So to judge whether an AI is reliable, first ask what data it learned from.
- l49: Next time an AI sounds totally sure, ask: has it learned this kind of question?

## s10 Outro [package:outro]
- l50: In a sentence: today's AI mostly doesn't follow rules people write; it learns patterns from examples on its own.
- l51: Next time: overfitting, or why something aces the practice questions but stumbles on new ones.
