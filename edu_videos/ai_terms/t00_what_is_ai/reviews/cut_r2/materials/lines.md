# 讲稿（中英对照）

### s0 冷开场（冷开场）
| 句号 | 中文 | English |
|---|---|---|
| l01 | 相册认得出你家的猫。可并没有人把「猫长什么样」一条条写成规则，教给电脑。 | Your photo app can spot your cat. Yet nobody had to write down, rule by rule, what a cat looks like. |
| l02 | 那它是怎么会的？简单说：给它看大量例子，让它自己学出规律。这，就是今天的 AI。 | So how does it know? In short: you show it lots of examples, and it works out the pattern itself. That's today's AI. |

### s1 本期内容（包装卡 agenda）
| 句号 | 中文 | English |
|---|---|---|
| l03 | 这一期，讲四件事： | Four things today. |
| l04 | AI 要解决什么问题； | The problem AI is built to solve. |
| l05 | 一个学认数字的小孩，再加一个实际跑出来的小实验； | A child learning their numbers, and a real experiment. |
| l06 | 换个角度：AI 像一台预测机器； | Seeing AI as a prediction machine. |
| l07 | 它带来的改变和麻烦，还有用好它的三个提醒。 | What it changes, what can go wrong, and three things to remember. |
| l08 | 这一期不需要任何基础。 | You don't need any background. |

### s2 规则写不完（章节 problem）
| 句号 | 中文 | English |
|---|---|---|
| l09 | 先看传统的电脑程序：人把规则一条一条写好，电脑照着执行。 | Start with a traditional computer program. People write the rules, one by one, and the computer follows them. |
| l10 | 算工资、订机票，规则说得清清楚楚，这样做就够了。 | For payroll, or booking a flight, the rules are crystal clear, and that works fine. |
| l11 | 可有些事，规则很难写全。比如，认出一个手写的数字三。 | But some tasks are hard to capture in rules. Like recognizing a handwritten three. |
| l12 | 这些三，都是人手写的：有的胖，有的瘦，有的歪。你一眼就能认出来。 | Every one of these is a three, written by hand. Some are fat, some are thin, some slant. You recognize them at a glance. |
| l13 | 可要把「怎么认」写成规则，就难了。上下两个弯？八也是。下半截开口朝左？五也是。 | But try explaining how. Two bumps, one above the other? An eight has those too. Open on the left at the bottom? So is a five. |
| l14 | 这样写规则，很容易漏掉一些三，也容易把别的数字认成三。 | Rules like these can easily miss some threes, or mistake other digits for threes. |

### s3 换个做法
| 句号 | 中文 | English |
|---|---|---|
| l15 | 今天的 AI，大多换了一个做法：不写规则，给例子。 | Most of today's AI takes a different approach. Don't write rules. Give examples. |
| l16 | 给电脑看成百上千张手写的数字，每一张都告诉它答案：这是三，这是七。 | Show the computer hundreds, even thousands, of handwritten digits, each one with the answer: this is a three, this is a seven. |
| l17 | 它自己从例子里找出规律。这种做法，叫机器学习。 | It finds the pattern in the examples on its own. That approach is called machine learning. |
| l18 | 学出来的那套认法，叫模型。以后来一张新图，模型就给出它的答案。 | The way of telling digits apart that it ends up with is called a model. Hand the model a new image, and it gives you its answer. |
| l19 | 很多人以为，AI 的本事是程序员一条条写进去的。其实大多是从例子里学来的；这些例子，就叫数据。 | Many people think a programmer typed in everything an AI can do. In fact, most of it was learned from examples. Those examples are called data. |

### s4 打个比方（章节 analogy）
| 句号 | 中文 | English |
|---|---|---|
| l20 | 这就像教小孩认数字。你不会给他一本说明书，写着：3，是两个半圆叠在一起。 | It's like teaching a child their numbers. You don't hand them a manual that says: a 3 is two half circles, stacked. |
| l21 | 你只是指着数字，一遍一遍地告诉他：这是三。看得多了，他就会认了，连没见过的写法也认得出。 | You just point and keep saying, "This is a three." Eventually they get it, even when the three is written in a way they've never seen. |
| l22 | 小孩学会的那套认法，就是模型；你指给他看的数字，加上你说的「这是三」，就是带答案的例子。 | The way of telling numbers apart that the child picks up is the model. Each digit you point at, plus your "this is a three," is an example with its answer. |
| l23 | 不过有两点不像。待会儿你会看到，我们这个模型要看上百个例子才认得准。而且小孩慢慢会知道，「三」代表三个东西；模型学会的，只是看图挑一个答案。 | Two things don't match, though. As you'll see, our model needs a hundred or so examples before it gets good. And a child comes to understand that three means three things. The model has only learned to look at an image and pick an answer. |
| l24 | 再比如做菜。有的菜，照菜谱一步一步做就行，就像传统程序；有的菜靠手感：老师傅做过上千道，每次尝一口、听人评价、差了就调一调，才练出来。 | Or think about cooking. Sometimes you just follow a recipe, step by step. That's a traditional program. Other times, a seasoned cook goes by feel, built over a thousand dishes of tasting, getting feedback, and adjusting whatever's off. |
| l25 | 每做一道菜，就像模型猜一个答案；尝一口、听评价，就是对照正确答案；差了就调，这就是学习。练出的手感，老师傅自己也没法全写进菜谱。 | Each dish is like the model making a guess. Tasting it and hearing what people think is checking against the right answer. Adjusting when it's off: that's learning. And the feel they end up with is something even the cook can't fully write down. |

### s5 亲手做个实验（章节 experiment）
| 句号 | 中文 | English |
|---|---|---|
| l26 | 我们真的来做一次。这是一套公开的手写数字图片，共1797张，每张只有八行八列的小格子。 | Let's actually try it. Here's a public collection of handwritten digits: 1,797 images, each just an eight-by-eight grid. |
| l27 | 先拿出三百张锁起来，留着当考试题，训练的时候一张都不许看；剩下的，是给它学的例子。为什么这样分？只有考它没见过的题，才知道它是真会认了，还是只是记住了。 | First, we lock away three hundred of them as the exam. The model never sees them during training; the rest are the examples it learns from. Why split it this way? Only questions it has never seen can tell us whether it really learned, or just remembered. |
| l28 | 先猜一下：只给它看十个例子，考试能答对多少？ | Take a guess: with just ten examples, how much of the exam would it get right? |
| l29 | 随便抽十个，往往有几个数字一次都没出现。这样抽了二十回，考试成绩一般只有37%左右。比瞎猜的10%强，但还差得远。 | Pick ten at random, and usually a few digits don't show up at all. Try it twenty times, and the typical score is about 37%. That beats random guessing at 10%, but it's still a long way off. |
| l30 | 给它看一百个例子，答对了88%。 | With a hundred examples: 88%. |
| l31 | 把将近一千五百个例子全看完，答对了97%。 | With all of the nearly fifteen hundred training examples: 97%. |
| l32 | 自始至终，没有人告诉它三长什么样，只告诉它哪张是三。这一次，它见得越多、越全，认得越准。相册认猫，也是同一个道理。 | At no point did anyone tell it what a three looks like, only which images were threes. Here, the more it saw, and the more kinds, the better it got. Your photo app finds your cat the same way. |
| l33 | 不过，三百道考题，它还是错了十道。比如这张潦草的二，它认成了一。有几张，连人看了都要犹豫。 | Still, out of three hundred exam questions, it missed ten. Like this messy two, which it read as a one. A few of them would make a person hesitate too. |

### s6 一台预测机器（章节 lens）
| 句号 | 中文 | English |
|---|---|---|
| l34 | 换个角度想：今天的 AI，就像一台预测机器。这里的预测，不是看未来，而是看到一样东西，猜它的答案。 | Here's another way to see it. Today's AI is like a prediction machine. Not predicting the future: predicting the answer for whatever you show it. |
| l35 | 我们这个模型，不光猜答案，还会报出把握。比如这张图，它有96%的把握说是三。 | Our model doesn't just guess. It also reports how sure it is. For this image: "96% sure it's a three." |
| l36 | 别的 AI 也一样：识图的模型，猜照片里有没有猫；语音模型，猜一段声音说的是哪几个字。 | Other AI works the same way. An image model guesses whether a photo has a cat in it. A speech model guesses which words were said. |
| l37 | 给它半句话，它猜下一个词；一个词接一个词地猜下去，就成了一段回答。 | Give a language model half a sentence, and it guesses the next word. Keep going, word after word, and you get a whole reply. |
| l38 | 能跟你聊天的大语言模型，就是这样生成回答的。它猜得非常好，也能从数据里学到很多知识；可话接得顺，不保证说得对。 | Large language models, the technology behind chatbots, write their replies this way. They're extremely good at guessing, and they pick up a lot of knowledge from data. But a smooth reply isn't a guarantee of a true one. |

### s7 一圈套一圈
| 句号 | 中文 | English |
|---|---|---|
| l39 | 刚才这些词，是一圈套一圈的。最外圈是 AI，也就是人工智能：让电脑做那些看起来需要「聪明」的事。人写规则的下棋程序也算 AI；算工资的普通程序，就不算了。 | These terms nest, circle within circle. The outermost circle is AI, artificial intelligence: getting computers to do things that seem to take intelligence. A chess program built from rules people wrote counts as AI. An ordinary payroll program doesn't. |
| l40 | 机器学习在 AI 里面。再往里是深度学习。深度学习用的模型叫神经网络，由很多层简单的计算叠起来。别被名字骗了：神经网络和大脑里的神经，只是有一点点像；「深度」也只是说层数多，不是理解得深。 | Machine learning sits inside AI. Inside that is deep learning. It uses models called neural networks, built from many layers of simple calculations. Don't let the names fool you: these networks are only loosely like neurons in a brain, and "deep" just means many layers, not deep understanding. |
| l41 | 大语言模型，就是一种深度学习。这一期讲的 AI，说的就是机器学习这一圈。 | Large language models are one kind of deep learning. In this episode, when we say AI, we mean the machine learning circle. |

### s8 现实里的影响（章节 real）
| 句号 | 中文 | English |
|---|---|---|
| l42 | 这种从数据里学的本事，已经在改变现实。 | This ability to learn from data is already changing the real world. |
| l43 | 蛋白质的形状，过去靠实验测，测一个常常要好几年。AlphaFold，从已知的结构里，学会了直接预测。 | Finding a protein's shape often took years of lab work. AlphaFold learned from known structures to predict shapes directly. |
| l44 | 带领研发它的两个人，因此分享了2024年诺贝尔化学奖的一半。 | Its two lead developers went on to share half of the 2024 Nobel Prize in Chemistry for it. |
| l45 | ChatGPT 上线大约两个月，估计每个月就有一亿人在用。 | About two months after launch, ChatGPT had an estimated hundred million monthly users. |
| l46 | 但它也可能学歪。据路透社报道，亚马逊曾想用 AI 筛简历；这个 AI 学的，是公司过去十年收到的简历，大多来自男性。 | But it can also learn the wrong lessons. According to Reuters, Amazon once tried using AI to screen résumés. That AI learned from ten years of résumés sent to the company, mostly from men. |
| l47 | 结果，它等于自己学会了「男性候选人更好」：简历里只要出现英文 women's，也就是「女子的」，比如「女子国际象棋社社长」，就会被扣分。这个工具后来被放弃了。 | In effect, it taught itself that male candidates were preferable. It marked down résumés with the word "women's," as in "women's chess club captain." The tool was later scrapped. |
| l48 | 数据里的偏见，也可能被它一起学走。 | Bias in the data can be learned right along with everything else. |

### s9 用好它的三个提醒（章节 fix）
| 句号 | 中文 | English |
|---|---|---|
| l49 | 所以，用 AI 的时候，有三个提醒。 | So when you use AI, here are three things to keep in mind. |
| l50 | 第一，没学过的东西，也可能让它乱认。我们给这个只认数字的模型看一个字母 A：它只能在零到九里挑一个，于是一本正经地说，有92%的把握是四。 | One: unfamiliar inputs can fool it. We showed this digit-only model an A. It had to pick from zero to nine. Its answer? "92% sure it's a four." |
| l51 | 这个把握，只是在十个数字里比谁更像。小孩会说「这不是数字」，它不会。 | That confidence only compares the ten digits against each other. A child would say, "That's not a number." The model can't. |
| l52 | 第二，它给的是预测，不是真理。刚才那张潦草的二，它有81%的把握说是一，还是错了。 | Two: it gives predictions, not truth. Remember that messy two? It was 81% sure it was a one, and it was wrong. |
| l53 | 第三，它的本事和毛病，既来自它学的数据，也和它怎么设计、怎么训练有关。判断一个 AI 靠不靠谱，先问它是从什么数据里学的。 | Three: its strengths and flaws come from the data it learned from, and also from how it was designed and trained. To judge whether an AI is trustworthy, first ask what data it learned from. |
| l54 | 下次 AI 很有把握地回答你，不妨想一想：这种问题，它学过吗？ | Next time an AI answers you with total confidence, ask yourself: has it ever learned this kind of question? |

### s10 片尾（包装卡 outro）
| 句号 | 中文 | English |
|---|---|---|
| l55 | 记住这一句： | Remember this: |
| l56 | 今天的 AI，主要不靠人写规则， | Today's AI isn't mainly built from rules people write. |
| l57 | 而是从例子里，自己学会规律。 | It teaches itself patterns from examples. |
| l58 | 下一期讲过拟合：练习题做得很好，新题却不行，是怎么回事？ | Next time: overfitting. Why can a model ace its practice questions, and still fail new ones? |
