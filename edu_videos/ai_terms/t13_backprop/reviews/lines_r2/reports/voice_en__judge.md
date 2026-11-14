# voice_en__judge（第 2 轮 · claude-opus-5-5）

核对依据：`materials/voice_en.md`、`script.en.md`、`scenes/web/s4.html`（网络：输入 5；A = 6、B = 4；第二层旋钮 2、1，偏置 13，2×6 + 1×4 + 13 = 29；偏置的「输入」恒为 1）、`previous.md` 中 I71–I119。

## 裁决
- V1 1 理由：l06 是 strict 的「what's coming」句，两位都判 a bit off（a 自己在问题表里标了 V1/V2 必改，却给了 2 分，前后矛盾）；l22「Each knob's share of the blame, which is its slope, is the error times…」主语被插入语拦腰截断，念出来费劲；l25「A's side is times two: twelve」是图表速记口吻。按 strict 规则，有必改就不能给 2。采 b。
- V2 1 理由：l06「we'll see why… watch… and see where…」三项并列预告，就是本项要抓的目录腔换了个句子外壳；上轮裁决认可的是两项版，作者加上第三项后更像行程单。两位都认定必改，a 给 2 分与自己的必改条目矛盾。b 把 l39 算作 strict 过渡不成立（见驳回），但仅凭 l06 已够 1 分。采 b。
- V3 1 理由：实验段只靠耳朵跟不上。l19「A gets six」没说 6 是 A 算出来的；l20「adds one more」与 l23「six, four and one」里的 one 互相误导（实际加的是第七个旋钮 13，它的输入才是 1），l23 的 1 全片没交代；l25 的 ×2、×1 是第二层旋钮的值，从没念过。b 的三条证据都核实成立，a 列的 l19/l23 也是实打实的听感问题，够 1 分。
- R 1 理由：I77（l06）改出新问题，两项变三项更像目录；I94/I95（l22）把 blame 和 slope 挂上了，却改出插入语；上轮裁决在 I94 已指出偏置输入「one」没介绍，本轮 l23 仍未交代（未解决）；I98（l25）改写后仍缺起始数与旋钮值。a 自己写了 I77「改出新问题，unresolved」却给 2 分，不成立。b 判 I72（l01）未解决不成立（见驳回），但不影响 1 分。
- V4 1 理由：（抽查）两人都漏了 l40→l41 紧挨着的重复。l40「Underneath, it's backpropagation: walking back from the output, collecting slopes.」话音刚落，strict 收尾 l41 又说「Backpropagation is passing the blame backward, from the output, layer by layer.」，听着就是同一句话说两遍。收尾里 a bit off 即必改，所以降到 1。另有 l09 几乎照搬 l02（建议）。两人指出的 l16「Nothing gets redone」、l36 复述两遍走法属实，但只是小毛病。
- V5 2 理由：（抽查）整体是同一个温和的讲述者，短句收拍有效（l11「For a single step.」、l28「Much closer.」、l32「For one step.」）。l06（10.8s）、l17（10.4s）偏长，l39 叠了三个插入语，两人都已指出。两人共同漏掉的是 l35「a nineteen eighty-six Nature paper」名词前叠修饰（见补充问题），只到建议级，维持 2。

## 补充问题
| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |
|---|---|---|---|---|---|
| l40–l41 | V4, V2 | 必改 | l40: Underneath, it's backpropagation: walking back from the output, collecting slopes. / l41: Backpropagation is passing the blame backward, from the output, layer by layer. | 两句连着播，都把反向传播说成「从输出往回走」，l41 又是 strict 收尾第一句，耳朵听来是同一句话复读。a 只说 l41 复述了 l04/l27/l30，b 判 l41 natural，都没发现它和紧邻的 l40 撞车。在 l40 删掉，l41 的 blame 收束可以留着 | l40: That's automatic differentiation. Underneath, it's backpropagation. |
| l20 + l23 | V3 | 必改 | l20: …multiplies each by a knob, adds one more, and guesses… / l23: The inputs are six, four and one… | 两处连起来会误导：耳朵容易把 l20 的「one more」听成「加 1」，l23 的「one」又像在印证这个理解。实际加的是第七个旋钮（值 13），1 是这个旋钮的固定输入。b 分别指出两处含糊，没发现它们互相坐实一个错误理解；两人的改写都没把「1 属于第七个旋钮」说出来 | l20: The second layer multiplies each by a knob, adds a seventh knob, and guesses: twenty-nine yuan. / l23: The inputs are six, four, and for the seventh knob, one. So the blame is thirty-six, twenty-four and six. |
| l25 | V3 | 必改 | A's side is times two: twelve. B's side is times one: six. | 单独念出的「A's」听着像「ace」，句首又没有铺垫。×2、×1 是第二层两个旋钮的值，全片没念过，耳朵不知道 2 和 1 从哪来。两人都没提「A's」的听感问题；b 的改写「A gets six times two」又和 l19「A gets six」（A 的输出）撞车 | For A, its knob is two: twelve. For B, it's one: six. |
| l09 | V4, V3 | 建议 | Each step, you want to know which way each knob should turn to drop the error fastest. That's the gradient, or the slope. | 前半句几乎照搬 l02「Every step of training, you need to know which way each knob should turn」，两句只隔约 30 秒；「the gradient, or the slope」还把所有旋钮的整体量和单个旋钮的量说成了同一个东西 | Which way each knob should turn, and how far: that's its slope. All of them together: the gradient. |
| l35 | V3, V5 | 建议 | A nineteen eighty-six Nature paper by Rumelhart, Hinton and Williams laid it out clearly. | 年份、刊名叠在 paper 前面，是书面写法。只靠耳朵时「Nature」是个普通词，可能听成「讲自然的论文」，后面同一口气还有三个人名。前面已有「So where does this come from?」过渡，在科普口语里尚可接受，所以记建议 | So where does this come from? In nineteen eighty-six, Rumelhart, Hinton and Williams laid it out in the journal Nature. |
| l18 | V3 | 记录 | We feed it the length of a taxi ride: five kilometers. | 一直没说网络要猜什么，要等到 l20「guesses: twenty-nine yuan」、l21「The real fare」才能倒推出是在猜车费；靠后文能补上，所以只记录 | It guesses taxi fares. We give it a five-kilometer ride. |

## 驳回
- l01（b，必改，I72 判「未解决」）：上轮裁决已判定「billions of knobs, some hundreds of billions」是正常口语，作者按裁决不改。b 没有拿出新证据，不成立。
- l04（b 改写）：「finds every knob's direction」偏名词化，在 strict 冷开场里问题成立。但 b 的改写「One trip backward tells us…」删掉了「The real trick」，l03「你永远试不完」接 l04「真正的窍门」的转折就没了，改写比原句差。可改为「The real trick? One trip backward tells you how to turn every knob. It's called backpropagation.」，和 l10「The obvious way?」相呼应。
- l06（a 改写）：「…Last, where it all came from.」末尾是不成句的目录条目，仍是三项预告，正是本项要抓的腔调，不可用。b 的改写首句「Trying knobs one by one would take forever.」复读了 l03。建议只留一个预告动作：「This time, we'll build a tiny network and watch the error run backward through it, knob by knob.」
- l09（b，必改）：l09 不是 strict 句，前半句已经把「which way… fastest」讲清楚，标签是接在解释后面的，不属于「labels replace an explanation」，降为建议（另见补充问题）。b 的改写把「which way」这层方向意思丢了。
- l17（b 改写）：比原句长，而且删掉了「the error can flow back」这个意象，l24「the error flows along the wires」正是靠它铺垫，改写反而更差。
- l20（b 改写）：「Another adds a number」还是含糊（加什么数？），这种拆句写法上轮裁决已驳过一次。问题本身成立，改写见补充问题。
- l23（b 改写）：「The knobs get thirty-six, twenty-four and six」删掉了输入 6、4，36、24 就成了凭空冒出来的数；「get」也有歧义。改写见补充问题。
- l25（b 改写）：「A gets six times two」里的「A gets six」和 l19「A gets six」（A 的输出）完全同形，听众会以为又在说 A 的值。改写见补充问题。
- l26（b 改写）：「multiplies its new error by its two knobs' inputs」引入了新术语「new error」，两个 its 指代不清。上轮裁决已驳回同类说明书式写法，原句复用 l22 规则可以保留。
- l39（b，归为 strict 过渡）：1986 章的过渡句是 l35，l39 是章内转到「今天」，不在 strict 范围内。插入语叠加的问题成立，按建议级处理，不计入 V2 的 strict 必改。
- l41（a，定义腔 / 建议）：「Backpropagation is passing the blame backward…」是正常的收尾总结口吻，不成立。真正的问题是和 l40 撞车，在 l40 改即可（见补充问题），l41 保留，给 l22–l23 埋下的 blame 做收束。
