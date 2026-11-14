# 讲稿（中英对照）

### s0 冷开场（冷开场）
| 句号 | 中文 | English |
|---|---|---|
| l01 | 手机相册能从照片里认出你家的猫，可没人把认猫的规则，一条条写给它。 | Your phone can find your cat in your photos, yet nobody ever gave it rules for what a cat looks like. |
| l02 | 那它怎么会的？给它看大量例子，它自己学出了规律。这，就是今天的 AI。 | So how does it do it? It saw tons of examples and worked out the patterns itself. That's today's AI. |

### s2 规则写不完（章节 problem）
| 句号 | 中文 | English |
|---|---|---|
| l03 | 传统的电脑程序，是人把规则一条条写好，电脑照着执行。 | A traditional program works differently: people write the rules one by one, and the computer follows them. |
| l04 | 算工资、订机票，规则清清楚楚，这样就够了。 | For payroll or booking flights, the rules are clear, so that's enough. |
| l05 | 可有些事，规则很难写全，比如认一个手写的三。人写的三有胖有瘦有歪，你一眼就认得出。 | But some things are hard to write rules for, like reading a handwritten three. Fat, skinny, tilted, you know it instantly. |
| l06 | 真要写成规则，就难了。说上下两个弯吧，八也是。说下半截开口朝左吧，五也是。 | Now try writing down how. "Two curves stacked"? So is an eight. "Bottom half opens left"? So does a five. |
| l07 | 这样写，会漏掉一些三，也会把别的数字认成三。 | Rules like that miss some threes and mistake other digits for threes. |

### s3 换个做法
| 句号 | 中文 | English |
|---|---|---|
| l08 | 所以今天的 AI，大多换了个做法：不写规则，给例子。 | So most of today's AI flips it around: no rules, just examples. |
| l09 | 给电脑看成百上千张手写数字，每张都告诉它答案：这是三，这是七。 | Show the computer hundreds or thousands of handwritten digits, each with its answer: this is a three, this is a seven. |
| l10 | 它自己从例子里找出规律，这种做法叫机器学习。 | It finds the patterns itself, and that's called machine learning. |
| l11 | 它学出来的那套认法叫模型，来一张新图，模型就给出答案。 | What it learns is called a model. Show the model a new image, and it gives you an answer. |
| l12 | 很多人以为，AI 的本事是程序员一条条写进去的。其实大多是从例子里学来的，这些例子就叫数据。 | A lot of people think programmers coded in everything AI can do. Mostly, it learned from examples, which we call data. |

### s5 做个小实验（章节 experiment）
| 句号 | 中文 | English |
|---|---|---|
| l17 | 咱们真做一次。这是一套公开的手写数字图片，一共1700 多张，每张只有八行八列的小格子。 | Let's actually try it, with nearly 1,800 handwritten digits, each a tiny 8×8 grid. |
| l18 | 先拿出三百张锁起来当考试题，剩下的给它学。 | First we lock away 300 as the test, and the rest are examples to learn from. |
| l19 | 看例子学习的过程叫训练，训练时考试题一张都不许看。 | Learning from them is called training, and during training it never sees a test question. |
| l20 | 只有考没见过的题，才知道它是真会认了，还是只是记住了。 | Only questions it hasn't seen can show whether it truly learned, or just memorized. |
| l21 | 你先猜猜：只给它看十个例子，考试能答对多少？ | So, take a guess: with just 10 examples, how much of the test does it get right? |
| l22 | 随便抽十个，常常有几种数字一张都没抽到。 | Pick ten at random, and often some digits don't show up at all. |
| l23 | 这样换着抽二十回，一般只答对37%左右，比瞎猜的10%强些，可还差得远。 | We tried twenty different random sets of ten. The typical score was about 37%: better than the 10% you'd get guessing, but still low. |
| l24 | 给一百个例子，答对88%。把将近一千五百个例子全看完，答对97%。 | With a hundred examples, it gets 88%. With all 1,500 or so, it gets 97%. |
| l25 | 从头到尾没人给它写认三的规则，只告诉它哪张是三。在这次实验里，例子越多，考得越好。 | We never gave it rules for a three, just told it which ones were threes. In this experiment, more examples meant better scores. |
| l26 | 但三百道题，它还是错了十道，比如这张潦草的二，认成了一。 | Still, it missed 10 of the 300, like this messy two it called a one. |

### s6 换个角度看（章节 lens）
| 句号 | 中文 | English |
|---|---|---|
| l27 | 刚才那个模型，其实就是在预测：看一张图，猜它是几。今天的 AI 就像一台预测机器，猜的不是未来，是答案。 | Here's another way to see it: today's AI is a prediction machine. Not predicting the future, just seeing something and guessing the answer. |
| l28 | 咱们这个模型不光猜，还会说有几成把握。这张图，它有96%的把握说是三。 | Our model also says how sure it is. It's 96% sure this one's a three. |
| l30 | 别的 AI 也一样。给语言模型半句话，它猜下一个词，一个接一个猜下去，就成了一段回答。 | Other AI works the same way. Give a language model half a sentence, and it guesses the next word, then the next, until there's a whole answer. |
| l31 | 能跟你聊天的大语言模型，就是这么回答的。 | Chatbots run on large language models, and that's how they reply. |
| l32 | 它猜得很好，也从数据里学到很多知识，可话接得顺，不保证说得对。 | They guess well, but a smooth answer can still be wrong. |

### s7 一圈套一圈
| 句号 | 中文 | English |
|---|---|---|
| l33 | AI 包括机器学习，像大圈套小圈。最外圈是 AI，也叫人工智能，就是让电脑做看着要动脑子的事。 | So how do all these terms fit together? Picture AI, artificial intelligence, as the biggest circle: computers doing things that seem to take smarts. |
| l34 | 人写规则的下棋程序也算 AI，算工资的普通程序就不算。 | A chess program built on hand-written rules counts as AI. A plain payroll program doesn't. |
| l35 | 机器学习在 AI 里面，再往里是深度学习。它用的模型叫神经网络，就是很多层简单的计算，一层叠一层。 | Inside AI is machine learning, and inside that, deep learning, which runs on neural networks: many layers of simple math. |
| l36 | 深度只是说层数多，不是理解得深。大语言模型，就是用深度学习做出来的。 | "Deep" just means many layers, not deep understanding. Large language models are built with deep learning. |
| l37 | 这期说的 AI，就是机器学习这一圈。 | When I say "today's AI," I mean machine learning: AI that learns from examples. |

### s8 一个真实的例子（章节 real）
| 句号 | 中文 | English |
|---|---|---|
| l38 | 从数据里学，也可能学歪。路透社报道过，亚马逊想过用 AI 筛简历。 | Learning from data can go wrong, too. According to Reuters, Amazon once tried using AI to screen résumés. |
| l39 | 它学的是公司过去十年收到的简历，大多来自男性。 | It learned from 10 years of résumés sent to the company, mostly by men. |
| l40 | 结果它等于自己学会了「男性候选人更好」。 | In effect, it taught itself that male candidates were better. |
| l41 | 简历里只要有英文 women's，也就是「女子的」，就会被扣分，比如「女子国际象棋社社长」。 | Résumés with the word "women's," as in "women's chess club captain," got marked down. |
| l42 | 这个工具后来没做下去。数据里的偏见，也可能被它一起学走。 | The tool was later scrapped. If the data is biased, the model can pick that up too. |

### s9 用的时候记住三点（章节 fix）
| 句号 | 中文 | English |
|---|---|---|
| l43 | 所以用 AI 的时候，记住三点。 | When you use AI, remember three things. |
| l44 | 第一，没学过的东西它也会硬答。给这个只认数字的模型看一个字母 A，它只能在零到九里挑。 | First, it always answers, even about things it's never seen. Show our digit model the letter A, and it still has to pick from zero to nine. |
| l45 | 它说有92%的把握是四，其实只是说：在零到九里，这张图最像四。 | It says it's 92% sure that's a four. But that just means four was its best match out of ten digits. |
| l46 | 小孩会说「这不是数字」，它不会。 | A kid would say, "That's not a number." The model won't. |
| l47 | 第二，再有把握也会错。刚才那张潦草的二，它有81%的把握说是一，照样错了。 | Second, it gives you predictions, not the truth. Remember that messy two? The model was 81% sure it was a one, and it was wrong. |
| l48 | 第三，它哪儿行、哪儿不行，跟它学的数据有关，也跟它怎么设计、怎么训练有关。 | Third, what it gets right or wrong depends on its data, and also on how it's designed and trained. |
| l49 | 判断一个 AI 靠不靠谱，先看它是拿什么数据学的。 | So to judge whether an AI is reliable, first find out what data it learned from. |
| l50 | 下次 AI 很有把握地回答你，就想一想：这种问题，它学过吗？ | Whenever an AI sounds totally sure, ask yourself: has it seen questions like this before? |

### s10 片尾（包装卡 outro）
| 句号 | 中文 | English |
|---|---|---|
| l51 | 今天的 AI，主要不靠人写规则，靠自己从例子里学出规律。 | Most of today's AI isn't built on rules people write. It learns patterns from examples. |
| l52 | 可要是练习题全会，一换新题就不行呢？这叫过拟合，咱们下期聊。 | Next time, we'll look at why a model can ace the practice questions and still stumble on new ones. It's called overfitting. |
