# 讲稿（中英对照）

### s0 冷开场（冷开场）
| 句号 | 中文 | English |
|---|---|---|
| l01 | 相册认得出你家的猫，可从来没有人告诉过电脑，猫长什么样。 | Your photo app can spot your cat. Yet no one ever told the computer what a cat looks like. |
| l02 | 它是怎么学会的？这就是今天要讲的：什么是 AI。 | So how did it learn? That's today's question: what is AI? |

### s1 本期内容（包装卡 agenda）
| 句号 | 中文 | English |
|---|---|---|
| l03 | 这一期，讲四件事： | Here's what we'll cover. |
| l04 | 今天的 AI，要解决什么问题； | The problem today's AI is built to solve. |
| l05 | 一个学认数字的小孩，和一个真算出来的小实验； | A child learning their numbers, and a real experiment. |
| l06 | 换个角度：今天的 AI，就像一台预测机器； | A different lens: today's AI as a prediction machine. |
| l07 | 它在现实里带来的改变和麻烦，以及用好它的三个提醒。 | The changes and trouble it brings, plus three things to keep in mind. |
| l08 | 这一期不需要任何基础，我们从零开始。 | You don't need any background for this one. We start from zero. |

### s2 规则写不完（章节 problem）
| 句号 | 中文 | English |
|---|---|---|
| l09 | 先看传统的电脑程序：人把规则一条一条写好，电脑照着执行。 | Start with an ordinary computer program. People write the rules, one by one, and the computer follows them. |
| l10 | 算工资、订机票，规则说得清清楚楚，这样做就够了。 | For payroll, or booking a flight, the rules are crystal clear, and that works fine. |
| l11 | 可有些事，规则谁也说不清。比如，认出一个手写的数字三。 | But some things have rules nobody can spell out. Like recognizing a handwritten three. |
| l12 | 这些全是真人写的三：有的胖，有的瘦，有的歪。你一眼就能认出来。 | Every one of these is a three, written by a real person. Some are fat, some are thin, some slant. You recognize them at a glance. |
| l13 | 可要把「怎么认」写成规则，就难了。上下两个弯？八也是。下半截开口朝左？五也是。 | But try writing down how. Two bumps, one on top of the other? So does an eight. Opens to the left at the bottom? So does a five. |
| l14 | 规则写得再多，也总有漏掉的写法，也总会把别的数字认成三。 | However many rules you write, some threes slip through, and some other digits get mistaken for threes. |

### s3 换个做法
| 句号 | 中文 | English |
|---|---|---|
| l15 | 今天的 AI，大多换了一个做法：不写规则，给例子。 | Most of today's AI takes a different approach. Don't write rules. Give examples. |
| l16 | 给电脑看成百上千张手写的数字，每一张都告诉它答案：这是三，这是七。 | Show the computer hundreds, even thousands, of handwritten digits, each one with the answer: this is a three, this is a seven. |
| l17 | 它自己从例子里找出规律。这种做法，叫机器学习。 | It finds the pattern in the examples on its own. That approach is called machine learning. |
| l18 | 学出来的东西，叫模型。以后来一张新图，模型就给出它的答案。 | What it learns is called a model. Hand the model a new image, and it gives you its answer. |
| l19 | 所以，AI 背后并不是程序员写好的一条条答案；它的本事，大多是从数据里学来的。 | So behind AI there isn't a programmer typing in answers one by one. Most of what it can do, it learned from data. |

### s4 打个比方（章节 analogy）
| 句号 | 中文 | English |
|---|---|---|
| l20 | 这就像教小孩认数字。你不会给他一本说明书，写着：三，是两个半圆叠在一起。 | It's like teaching a child their numbers. You don't hand them a manual that says: a three is two half circles, stacked. |
| l21 | 你只是指着数字，一遍一遍地告诉他：这是三。看得多了，他就会认了，连没见过的写法也认得出。 | You just point and say, again and again: this is a three. After enough of them, they get it. They can read it even in handwriting they've never seen. |
| l22 | 小孩，就是模型；你指给他看的，就是带答案的例子。 | The child is the model. What you point at are the examples, with their answers. |
| l23 | 不过有两点不像：模型要的例子，通常比小孩多得多；它学会的规律，常常连做它的人也说不清。 | Two things don't match, though. A model usually needs far more examples than a child. And the pattern it learns is often something even its makers can't spell out. |
| l24 | 再比如做菜。一种厨师照着菜谱，一步一步做；另一种厨师尝过一千道菜，自己琢磨出了菜谱。 | Or think about cooking. One cook follows a recipe, step by step. Another has tasted a thousand dishes, and works out the recipe on their own. |
| l25 | 传统程序，是照菜谱做菜；机器学习，是从一千道菜里，自己总结出菜谱。 | A traditional program cooks from the recipe. Machine learning writes the recipe, from a thousand dishes. |

### s5 亲手做个实验（章节 experiment）
| 句号 | 中文 | English |
|---|---|---|
| l26 | 我们真的来做一次。这是一个公开的手写数字数据集，一共1797张，每张只有八乘八个格子。 | Let's actually try it. This is a public dataset of handwritten digits. 1,797 images, each just eight by eight squares. |
| l27 | 先拿出三百张锁起来，训练的时候一张都不许看，留着当考试题。剩下的，是给它学的例子。 | First, we lock away three hundred of them. The model never sees them during training. They're the exam. The rest are the examples it learns from. |
| l28 | 先猜一下：只给它看十个例子，考试能答对多少？ | Take a guess: with just ten examples, how much of the exam would it get right? |
| l29 | 随便抽十个，往往有几个数字它一张都没见过，考试只答对了37%左右。比瞎猜的10%强，但还差得远。 | Pick ten at random, and there are usually a few digits it hasn't seen even once. It scores about 37%. That beats random guessing at 10%, but it's still a long way off. |
| l30 | 给它看一百个例子，答对了88%。 | Show it a hundred examples: 88%. |
| l31 | 看完全部将近一千五百个例子，答对了97%。 | Show it all of them, almost fifteen hundred: 97%. |
| l32 | 自始至终，没有人告诉它三长什么样。它见得越多，认得越准。相册认猫，也是同一个道理。 | At no point did anyone tell it what a three looks like. The more it sees, the better it gets. Your photo app finds your cat the same way. |
| l33 | 不过，三百道考题，它还是错了十道。有几张，连人看了都要犹豫。 | Still, out of three hundred exam questions, it missed ten. A few of them would make a person hesitate too. |

### s6 一台预测机器（章节 lens）
| 句号 | 中文 | English |
|---|---|---|
| l34 | 换个角度想：今天的 AI，其实就像一台预测机器。 | Here's another way to see it. Today's AI is something like a prediction machine. |
| l35 | 给它一样东西，它猜一个答案，还带着把握。比如这张图，它说：96%是三。 | Give it something, and it guesses an answer, with a level of confidence. For this image, it says: 96% sure, it's a three. |
| l36 | 给它一张照片，它猜里面有没有猫；给它一段声音，它猜说的是哪几个字。 | Give it a photo, and it guesses whether there's a cat. Give it audio, and it guesses which words were said. |
| l37 | 给它半句话，它猜下一个词；一个词接一个词地猜下去，就成了一段回答。能跟你聊天的大语言模型，核心本事就是这样猜，只是猜得非常非常好。 | Give it half a sentence, and it guesses the next word. Guess word after word, and you get a whole reply. The chatbots you talk to, large language models, are built on this kind of guessing. They're just extremely good at it. |
| l38 | 这几个词，是一个套一个的。AI 是最大的圈，人写规则的办法也算 AI；机器学习在它里面。 | These terms nest inside each other. AI is the biggest circle, and rules that people write count as AI too. Machine learning sits inside it. |
| l39 | 再往里是深度学习：用很多层简单计算叠起来的模型来学，这种模型叫神经网络。大语言模型，是深度学习的一种。 | Inside that is deep learning: learning with models built from many layers of simple calculations, called neural networks. Large language models are one kind of deep learning. |
| l40 | 今天大家说的 AI，大多指的就是机器学习。 | When people say AI today, they mostly mean machine learning. |

### s7 现实里的影响（章节 real）
| 句号 | 中文 | English |
|---|---|---|
| l41 | 这种从数据里学的本事，已经在改变现实。 | This ability to learn from data is already changing the real world. |
| l42 | 蛋白质的形状，过去靠实验测，一个往往要好几年。AlphaFold 从已知的结构里学会了直接预测；带领研发它的两个人，因此分享了2024年诺贝尔化学奖的一半。 | Working out the shape of a protein used to take lab work, often for years. AlphaFold learned from known structures to predict shapes directly, and the two people who led its development shared half of the 2024 Nobel Prize in Chemistry. |
| l43 | ChatGPT 上线大约两个月，月活跃用户估计就过了一亿。 | ChatGPT was estimated to have passed a hundred million monthly active users about two months after launch. |
| l44 | 但它学到的不只有规律。据路透社报道，亚马逊曾想用 AI 筛简历；可这个 AI 学的，是公司过去十年收到的简历，大多来自男性。 | But patterns aren't the only thing it learns. According to Reuters, Amazon once tried using AI to screen résumés. But that AI learned from ten years of résumés sent to the company, mostly from men. |
| l45 | 结果，简历里只要出现「女子」这个词，英文是 women's，比如「女子国际象棋社社长」，就会被扣分。这个工具后来被放弃了。 | So it started marking down résumés with the word "women's," as in "women's chess club captain." The tool was later scrapped. |
| l46 | 数据里有什么，它就学什么，包括偏见。 | Whatever is in the data, it learns. Bias included. |

### s8 用好它的三个提醒（章节 fix）
| 句号 | 中文 | English |
|---|---|---|
| l47 | 所以，用 AI 的时候，记住三点。 | So when you use AI, keep three things in mind. |
| l48 | 第一，它只会它学过的。我们给它看一个字母 A：它从没见过字母，又只能在零到九里挑一个，于是一本正经地说：92%是四。 | One: it only knows what it has learned. We showed it the letter A. It has never seen a letter, and it can only pick from zero to nine, so it says, with a straight face: 92% sure, it's a four. |
| l49 | 第二，它给的是预测，不是真理。刚才那张写得很潦草的二，它有81%的把握说是一，还是错了。 | Two: it gives predictions, not truth. Remember that scrawled two? It was 81% sure it was a one, and it was wrong. |
| l50 | 第三，它的本事和毛病，都来自数据。判断一个 AI 靠不靠谱，先问它是从什么数据里学的。 | Three: its strengths and its flaws both come from data. To judge whether an AI is trustworthy, first ask what data it learned from. |

### s9 片尾（包装卡 outro）
| 句号 | 中文 | English |
|---|---|---|
| l51 | 记住这一句： | Remember this: |
| l52 | 今天的 AI，主要不靠人写规则， | Today's AI isn't mainly built from rules people write. |
| l53 | 而是从例子里，自己学会规律。 | It learns the patterns from examples. |
| l54 | 下一期，我们讲过拟合：模型把答案背下来了，会怎样？ | Next time: overfitting. What happens when a model memorizes the answers? |
