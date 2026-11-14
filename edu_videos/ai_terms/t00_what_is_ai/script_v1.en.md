# t00 What Is AI — Script

> In one sentence: Today's AI isn't built from rules people write. It learns the patterns from examples.

English version of `script.md` (v1, 2026-11-08). Segment ids, line ids and tags match the Chinese script one to one; the wording is rewritten for spoken English, not translated literally.
Each `- lNN: text` is one narration line, subtitle and animation cue; `[pause N]` adds N seconds after the line and is not read.
Spell numbers so the voice reads them correctly when it matters (years, percentages).

## s0 In this episode [package:agenda]
- l01: Your photo app can spot your cat, yet no one ever told the computer what a cat looks like. So how does it know? This is episode zero: what is AI. Four things.
- l02: The problem today's AI is built to solve.
- l03: A child learning their numbers, and a real experiment.
- l04: A different lens: today's AI as a prediction machine.
- l05: And the changes and trouble it brings, plus three things to keep in mind.
- l06: You don't need any background for this one. We start from zero.

## s1 Too many rules [chapter:problem]
- l07: Your photo app finds the cats in your pictures. Your phone turns speech into text. There are chatbots you can talk to. We call all of this AI. But what is it, really?
- l08: Start with an ordinary computer program. People write the rules, one by one, and the computer follows them.
- l09: For payroll, or booking a flight, the rules are crystal clear, and that works fine.
- l10: But some things have rules nobody can spell out. Like recognizing a handwritten three.
- l11: Every one of these is a three, written by a real person. Some are fat, some are thin, some slant, some are broken. You recognize them at a glance. But try writing down how, as rules. No number of rules is ever enough.

## s2 A different approach
- l12: Today's AI takes a different approach. Don't write rules. Give examples.
- l13: Show the computer hundreds, even thousands, of handwritten digits, each one with the answer: this is a three, this is a seven.
- l14: It finds the pattern in the examples on its own. That approach is called machine learning.
- l15: What it learns is called a model. Hand the model a new image, and it gives you its answer.

## s3 An analogy [chapter:analogy]
- l16: It's like teaching a child their numbers. You don't hand them a manual that says: a three is two half circles, stacked.
- l17: You just point and say, again and again: this is a three. After enough of them, they get it. They can read it even in handwriting they've never seen.
- l18: Or think about cooking. One cook follows a recipe, step by step. Another has tasted a thousand dishes, and works out the recipe on their own.
- l19: A traditional program cooks from the recipe. Machine learning writes the recipe, from a thousand dishes. It's just that the recipe works for the machine, and people can't always read it.

## s4 Let's run an experiment [chapter:experiment]
- l20: Let's actually try it. This is a public dataset of handwritten digits. {1,797|seventeen hundred ninety-seven} images, each just eight by eight squares.
- l21: First, we lock away three hundred of them. The model never sees them during training. They're the exam.
- l22: Show it just ten random examples, so some digits it has never seen even once, and it scores about {37%|thirty-seven percent}. That beats random guessing at {10%|ten percent}, but it's still a long way off.
- l23: Show it a hundred examples: {88%|eighty-eight percent}.
- l24: Show it all of them, almost fifteen hundred: {97%|ninety-seven percent}.
- l25: At no point did anyone tell it what a three looks like. The more it sees, the better it gets.
- l26: Still, out of three hundred exam questions, it missed ten. A few of them would make a person hesitate too.

## s5 A prediction machine [chapter:lens]
- l27: Here's another way to see it. Today's AI is something like a prediction machine.
- l28: Give it something, and it guesses an answer, with a level of confidence. For this image, it says: {96%|ninety-six percent} sure, it's a three.
- l29: Give it a photo, and it guesses whether there's a cat. Give it audio, and it guesses which words were said.
- l30: Give it half a sentence, and it guesses the next word. Guess word after word, and you get a whole reply. The large language models you chat with are built on exactly this. They're just extremely good at it.
- l31: These terms nest inside each other. AI is the biggest circle, and hand-written rules count as AI too. Machine learning sits inside it. Inside that is deep learning, which learns with many-layered neural networks, and large language models are one kind of deep learning. When people say AI today, they mostly mean machine learning.

## s6 Real-world impact [chapter:real]
- l32: This ability to learn from data is already changing the real world.
- l33: Working out the shape of a protein used to take experiments, often for years. AlphaFold learned from known structures to predict shapes directly, and the two people who led its development shared in the {2024|twenty twenty-four} Nobel Prize in Chemistry.
- l34: ChatGPT was estimated to pass a hundred million monthly active users, about two months after launch.
- l35: But patterns aren't the only thing it learns. According to Reuters, Amazon once tried using AI to screen résumés. It learned from ten years of résumés, mostly from men, and it started marking down résumés that included the word "women's," as in "women's chess club captain." The tool was later scrapped.
- l36: Whatever is in the data, it learns. Bias included.

## s7 Three things to keep in mind [chapter:fix]
- l37: So when you use AI, keep three things in mind.
- l38: One: it only knows what it has learned. We showed it the letter A. It has never seen a letter, and it can only pick from zero to nine, so it says, with a straight face: {92%|ninety-two percent} sure, it's a four.
- l39: Two: it gives predictions, not truth. Remember that scrawled two? It was {81%|eighty-one percent} sure it was a one, and it was wrong.
- l40: Three: its strengths and its flaws both come from data. To judge whether an AI is trustworthy, first ask what data it learned from.

## s8 Outro [package:outro]
- l41: Remember this:
- l42: Today's AI isn't mainly built from rules people write.
- l43: It learns the patterns from examples.
- l44: Next time: overfitting. What happens when a model memorizes the answers?
