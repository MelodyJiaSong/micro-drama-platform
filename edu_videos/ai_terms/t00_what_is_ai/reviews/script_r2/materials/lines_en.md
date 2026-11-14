# Script (English)

### s0 Cold open（冷开场）
| 句号 | English |
|---|---|
| l01 | Your photo app can spot your cat. Yet nobody ever wrote down, as rules, what a cat looks like. |
| l02 | So how does it know? In short: you show it lots of examples, and it works out the pattern itself. That's today's AI. |

### s1 In this episode（包装卡 agenda）
| 句号 | English |
|---|---|
| l03 | Here's what we'll cover. |
| l04 | The problem AI is built to solve. |
| l05 | A child learning their numbers, and a real experiment. |
| l06 | How AI works as a prediction machine. |
| l07 | What it changes, what can go wrong, and three things to remember. |
| l08 | You don't need any background. |

### s2 Too many rules（章节 problem）
| 句号 | English |
|---|---|
| l09 | Start with a traditional computer program. People write the rules, one by one, and the computer follows them. |
| l10 | For payroll, or booking a flight, the rules are crystal clear, and that works fine. |
| l11 | But some tasks are hard to capture in rules. Like recognizing a handwritten three. |
| l12 | Every one of these is a three, written by hand. Some are fat, some are thin, some slant. You recognize them at a glance. |
| l13 | But try explaining how. Two bumps, one above the other? An eight has those too. Open on the left at the bottom? So is a five. |
| l14 | Rules like these miss some threes, and mistake other digits for threes. |

### s3 A different approach
| 句号 | English |
|---|---|
| l15 | Most of today's AI takes a different approach. Don't write rules. Give examples. |
| l16 | Show the computer hundreds, even thousands, of handwritten digits, each one with the answer: this is a three, this is a seven. |
| l17 | It finds the pattern in the examples on its own. That approach is called machine learning. |
| l18 | The way of telling digits apart that it ends up with is called a model. Hand the model a new image, and it gives you its answer. |
| l19 | Many people think a programmer typed in everything an AI can do. In fact, most of it was learned from examples. Those examples are called data. |

### s4 An analogy（章节 analogy）
| 句号 | English |
|---|---|
| l20 | It's like teaching a child their numbers. You don't hand them a manual that says: a 3 is two half circles, stacked. |
| l21 | You just point and keep saying, "This is a three." Eventually they get it, even when the three is written in a way they've never seen. |
| l22 | The way of telling numbers apart that the child picks up is the model. Each digit you point at, plus your "this is a three," is an example with its answer. |
| l23 | Two things don't match, though. A model usually needs far more examples than a child. And the pattern it learns is often something even its makers can't spell out. |
| l24 | Or think about cooking. A beginner follows a recipe, step by step. A seasoned cook has made a thousand dishes: taste, hear what people think, adjust. Over time, they develop a feel for it. |
| l25 | Ask them to write that feel down as a recipe, and they can't fully do it. A traditional program cooks from the recipe. Machine learning is the seasoned cook: the skill is trained, not written down. |

### s5 Let's run an experiment（章节 experiment）
| 句号 | English |
|---|---|
| l26 | Let's actually try it. Here's a public collection of handwritten digits: 1,797 images, each just an eight-by-eight grid. |
| l27 | First, we lock away three hundred of them. The model never sees them during training. They're the exam: only questions it has never seen can tell us whether it really learned, or just remembered. The rest are the examples it learns from. |
| l28 | Take a guess: with just ten examples, how much of the exam would it get right? |
| l29 | Pick ten at random, and usually a few digits don't show up at all. Try it many times, and the typical score is about 37%. That beats random guessing at 10%, but it's still a long way off. |
| l30 | With a hundred examples: 88%. |
| l31 | With all of the nearly fifteen hundred training examples: 97%. |
| l32 | At no point did anyone tell it what a three looks like, only which images were threes. Here, the more it saw, and the more kinds, the better it got. Your photo app finds your cat the same way. |
| l33 | Still, out of three hundred exam questions, it missed ten. Like this messy two, which it read as a one. A few of them would make a person hesitate too. |

### s6 A prediction machine（章节 lens）
| 句号 | English |
|---|---|
| l34 | Here's another way to see it. Today's AI is like a prediction machine. Not predicting the future: predicting the answer for whatever you show it. |
| l35 | It guesses an answer, and tells you how sure it is. For this image: "96% sure it's a three." |
| l36 | Give it a photo, and it guesses whether there's a cat. Give it audio, and it guesses which words were said. |
| l37 | Give it half a sentence, and it guesses the next word. Keep going, word after word, and you get a whole reply. |
| l38 | Large language models, the technology behind chatbots, write their replies this way. They're extremely good at guessing. But a good guess isn't the same as a true answer. |

### s7 Circles within circles
| 句号 | English |
|---|---|
| l39 | These terms nest, circle within circle. The outermost circle is AI: getting computers to do things that seem to take intelligence. A chess program built from rules people wrote counts as AI. An ordinary payroll program doesn't. |
| l40 | Machine learning sits inside AI. Inside that is deep learning. It uses models called neural networks, built from many layers of simple calculations. |
| l41 | Large language models are one kind of deep learning. In this episode, when we say AI, we mean the machine learning circle. |

### s8 Real-world impact（章节 real）
| 句号 | English |
|---|---|
| l42 | This ability to learn from data is already changing the real world. |
| l43 | Finding a protein's shape often took years of lab work. AlphaFold learned from known structures to predict shapes directly. |
| l44 | Its two lead developers went on to share half of the 2024 Nobel Prize in Chemistry. |
| l45 | About two months after launch, ChatGPT had an estimated hundred million monthly users. |
| l46 | But learned patterns can carry bias. According to Reuters, Amazon once tried using AI to screen résumés. That AI learned from ten years of résumés sent to the company, mostly from men. |
| l47 | In effect, it taught itself that male candidates were preferable. It marked down résumés with the word "women's," as in "women's chess club captain." The tool was later scrapped. |
| l48 | Bias in the data can be learned right along with everything else. |

### s9 Three things to keep in mind（章节 fix）
| 句号 | English |
|---|---|
| l49 | So when you use AI, here are three things to keep in mind. |
| l50 | One: it only understands the kind of thing it has learned. We showed it an A. It had only ever seen digits, so it had to pick from zero to nine. Its answer? "92% sure it's a four." |
| l51 | That confidence only compares the ten digits against each other. A child would say, "That's not a number." The model can't. |
| l52 | Two: it gives predictions, not truth. Remember that messy two? It was 81% sure it was a one, and it was wrong. |
| l53 | Three: its strengths and flaws come mostly from the data it learned from, and also from how it was designed and trained. To judge whether an AI is trustworthy, first ask what data it learned from. |
| l54 | Next time an AI answers you with total confidence, ask yourself: has it ever learned this kind of question? |

### s10 Outro（包装卡 outro）
| 句号 | English |
|---|---|
| l55 | Remember this: |
| l56 | Today's AI isn't mainly built from rules people write. |
| l57 | It teaches itself patterns from examples. |
| l58 | Next time: overfitting. Why can a model ace its practice questions, and still fail new ones? |
