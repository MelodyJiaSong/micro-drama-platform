# 屏幕文字（逐屏）

每句口播说完前一刻，屏幕上看得见的文字块：`[层级 字号px]` 文字（字数）。层级：eyebrow 小标签、display 大数字、h1 标题、h2 小标题、body 正文、caption 注释、chart 图表文字。截图是 1920×1080 的那一刻（字幕在成片里另外压在底部，截图里没有）。

## s0 开场（片头之前）
### l01（3.5s）
- 口播：现在的大模型，有几十亿、上千亿个旋钮。
- [h1 76px] 几十亿个旋钮（6 字）
- 合计（不含小标签、图表）：1 块，6 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s0_l01.png`
### l02（4.6s）
- 口播：训练时每走一步，都得知道每个旋钮往哪拧、拧多少。
- [h1 76px] 每一步：往哪拧、拧多少（9 字）
- 合计（不含小标签、图表）：1 块，9 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s0_l02.png`
### l03（2.4s）
- 口播：一个一个去试？根本试不完。
- [h1 76px] 一个个试？试不完（7 字）
- [div 54px] 试了 9 个（4 字）
- 合计（不含小标签、图表）：2 块，11 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s0_l03.png`
### l04（4.3s）
- 口播：实际上，倒着走一趟就全算出来了，这叫反向传播。
- [display 132px] 反向传播（4 字）
- 合计（不含小标签、图表）：1 块，4 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s0_l04.png`

## s1 本期内容（画面：目录卡）
### agenda（包装卡，整段 15.3s）
- 口播 l05：上期说过，神经网络就是一层层小单元，每个都带着旋钮。
- 口播 l06：这期咱们先看看挨个试为什么不行，再拿个小网络，看错误怎么倒着传回去，最后说说它的来历。
- 屏幕：01 · 挨个试，行不通（7 字）
- 屏幕：02 · 倒着算（4 字）
- 屏幕：03 · 做个小实验（6 字）
- 屏幕：04 · 从 1986 到今天（6 字）
- 屏幕：先修：上期：神经网络与深度学习（13 字）
- 截图：``

## c_problem（章节卡）
- 挨个试，行不通
- 截图：``

## s2 一个个试，试不过来
### l07（5.2s）
- 口播：先说训练：模型猜个答案，跟正确答案一比，差多少就是错误。
- [eyebrow 22px] 01 · 一个个试，试不过来（9 字）
- [h1 76px] 差多少 = 错误（5 字）
- [eyebrow 22px] 模型（2 字）
- [chart 40px] 猜的（2 字）
- [chart 40px] 正确答案（4 字）
- [chart 40px] 错误（2 字）
- 合计（不含小标签、图表）：1 块，5 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s2_l07.png`
### l08（6.1s）
- 口播：给错误打个分，差得越多分越高，叫损失。训练就是拧旋钮，让错误变小。
- [eyebrow 22px] 01 · 一个个试，试不过来（9 字）
- [h1 76px] 训练：拧旋钮，压低损失（9 字）
- [eyebrow 22px] 模型（2 字）
- [chart 40px] 猜的（2 字）
- [chart 40px] 正确答案（4 字）
- [chart 40px] 错误（2 字）
- 合计（不含小标签、图表）：1 块，9 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s2_l08.png`
### l09（5.4s）
- 口播：每个旋钮往哪拧，错误降得最快？这个方向叫梯度，也就是坡度。
- [eyebrow 22px] 01 · 一个个试，试不过来（9 字）
- [h1 76px] 梯度：降得最快的方向（9 字）
- [eyebrow 22px] 模型（2 字）
- [chart 40px] 猜的（2 字）
- [chart 40px] 正确答案（4 字）
- [div 64px] ↻（0 字）
- [div 64px] ↺（0 字）
- [div 64px] ↻（0 字）
- [chart 40px] 错误（2 字）
- 合计（不含小标签、图表）：4 块，9 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s2_l09.png`
### l10（7.4s）
- 口播：最直接的办法是挨个试：把一个旋钮拧一点点，从头重算一遍，看错误变大还是变小。
- [eyebrow 22px] 01 · 一个个试，试不过来（9 字）
- [h1 76px] 笨办法：挨个试（6 字）
- [eyebrow 22px] 模型（2 字）
- [span 150px] 3（1 字）
- [h2 54px] 遍（1 字）
- [div 54px] 重算一遍，看错误变没变（10 字）
- 合计（不含小标签、图表）：4 块，18 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s2_l10.png`
### l11（7.0s）
- 口播：可有多少个旋钮，就得重算多少遍。几十亿个旋钮就是几十亿遍，这还只是一步。
- [eyebrow 22px] 01 · 一个个试，试不过来（9 字）
- [h1 76px] 笨办法：挨个试（6 字）
- [eyebrow 22px] 模型（2 字）
- [div 150px] 几十亿遍（4 字）
- [div 54px] 才走一步（4 字）
- 合计（不含小标签、图表）：3 块，14 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s2_l11.png`

## c_analogy（章节卡）
- 倒着算
- 截图：``

## s3 倒着往回算
### l12（6.3s）
- 口播：反向传播换了个思路。打个比方，一串齿轮咬在一起，最后一个带着指针。
- [eyebrow 22px] 02 · 倒着往回算（6 字）
- [h1 76px] 一串齿轮（4 字）
- [chart 30px] 指针（2 字）
- 合计（不含小标签、图表）：1 块，4 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s3_l12.png`
### l13（5.7s）
- 口播：第一个转一格，第二个就转两格。第二个转一格，第三个就转三格。
- [eyebrow 22px] 02 · 倒着往回算（6 字）
- [h1 76px] 一串齿轮（4 字）
- [chart 30px] 指针（2 字）
- [chart 52px] ×2（1 字）
- [chart 52px] ×3（1 字）
- 合计（不含小标签、图表）：1 块，4 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s3_l13.png`
### l14（5.4s）
- 口播：那第一个转一格，指针转几格？沿路的倍数乘起来，二乘三，六格。
- [eyebrow 22px] 02 · 倒着往回算（6 字）
- [h1 76px] 指针转几格？（5 字）
- [chart 30px] 指针（2 字）
- [div 130px] 2 × 3 = 6（3 字）
- [chart 52px] ×2（1 字）
- [chart 52px] ×3（1 字）
- 合计（不含小标签、图表）：2 块，8 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s3_l14.png`
### l15（7.4s）
- 口播：倒着算最省事：从指针开始往回走，每过一个齿轮，就在上一步的结果上再乘个倍数。
- [eyebrow 22px] 02 · 倒着往回算（6 字）
- [h1 76px] 倒着算，每处乘一次（8 字）
- [chart 64px] 6（1 字）
- [chart 64px] 3（1 字）
- [chart 64px] 1（1 字）
- [chart 30px] 指针（2 字）
- [chart 52px] ×2（1 字）
- [chart 52px] ×3（1 字）
- 合计（不含小标签、图表）：1 块，8 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s3_l15.png`
### l16（3.5s）
- 口播：每处只乘一次，算过的接着用，不用重算。
- [eyebrow 22px] 02 · 倒着往回算（6 字）
- [h1 76px] 倒着算，每处乘一次（8 字）
- [chart 64px] 6（1 字）
- [chart 64px] 3（1 字）
- [chart 64px] 1（1 字）
- [chart 30px] 指针（2 字）
- [h2 54px] 算过的，接着用（6 字）
- [chart 52px] ×2（1 字）
- [chart 52px] ×3（1 字）
- 合计（不含小标签、图表）：2 块，14 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s3_l16.png`
### l17（8.5s）
- 口播：神经网络也像一串齿轮：每个旋钮隔着几层，影响最后的答案。所以错误也能一层层倒着传回去。
- [eyebrow 22px] 02 · 倒着往回算（6 字）
- [h1 76px] 神经网络也像一串齿轮（10 字）
- [chart 64px] 6（1 字）
- [chart 64px] 3（1 字）
- [chart 64px] 1（1 字）
- [chart 30px] 指针（2 字）
- [h2 54px] 旋钮 → 一层层 → 答案（7 字）
- [h2 54px] 错误 ← 倒着传回去（7 字）
- [chart 52px] ×2（1 字）
- [chart 52px] ×3（1 字）
- 合计（不含小标签、图表）：3 块，24 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s3_l17.png`

## c_experiment（章节卡）
- 做个小实验
- 截图：``

## s4 做个小实验
### l18（6.1s）
- 口播：来看个真的小网络：两层，七个旋钮。输入的是打一趟车的路程：五公里。
- [eyebrow 22px] 03 · 做个小实验（6 字）
- [div 28px] A（1 字）
- [div 32px] ×2（1 字）
- [div 32px] ×1（1 字）
- [div 32px] +1（1 字）
- [n 84px] 5（1 字）
- [u 28px] 公里（2 字）
- [div 32px] +13（1 字）
- [div 28px] B（1 字）
- [div 32px] ×0.4（1 字）
- [div 32px] +2（1 字）
- [div 32px] ×1（1 字）
- 合计（不含小标签、图表）：11 块，12 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s4_l18.png`
### l19（5.7s）
- 口播：第一层两个小单元，A 和 B，各用两个旋钮算一下：A 得六，B 得四。
- [eyebrow 22px] 03 · 做个小实验（6 字）
- [div 28px] A（1 字）
- [div 44px] 6（1 字）
- [div 32px] ×2（1 字）
- [div 32px] ×1（1 字）
- [div 32px] +1（1 字）
- [n 84px] 5（1 字）
- [u 28px] 公里（2 字）
- [div 32px] +13（1 字）
- [div 28px] B（1 字）
- [div 44px] 4（1 字）
- [div 32px] ×0.4（1 字）
- [div 32px] +2（1 字）
- [div 32px] ×1（1 字）
- 合计（不含小标签、图表）：13 块，14 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s4_l19.png`
### l20（5.9s）
- 口播：第二层把这两个数各乘一个旋钮，再加上一个，猜出车费：二十九块。
- [eyebrow 22px] 03 · 做个小实验（6 字）
- [div 28px] A（1 字）
- [span 76px] 29（1 字）
- [span 54px] 猜（1 字）
- [div 44px] 6（1 字）
- [div 32px] ×2（1 字）
- [div 32px] ×1（1 字）
- [div 32px] +1（1 字）
- [div 56px] 29（1 字）
- [n 84px] 5（1 字）
- [u 28px] 公里（2 字）
- [div 32px] +13（1 字）
- [div 28px] B（1 字）
- [div 44px] 4（1 字）
- [div 32px] ×0.4（1 字）
- [div 32px] +2（1 字）
- [div 32px] ×1（1 字）
- 合计（不含小标签、图表）：16 块，17 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s4_l20.png`
### l21（5.4s）
- 口播：可实际是二十三块，多猜了六块。这六块，就是要往回传的错误。
- [eyebrow 22px] 03 · 做个小实验（6 字）
- [div 28px] A（1 字）
- [span 76px] 29（1 字）
- [span 54px] 猜（1 字）
- [div 44px] 6（1 字）
- [div 32px] ×2（1 字）
- [div 32px] ×1（1 字）
- [div 32px] +1（1 字）
- [span 76px] 23（1 字）
- [span 54px] 实际（2 字）
- [div 56px] 29（1 字）
- [n 84px] 5（1 字）
- [span 76px] +6（1 字）
- [span 54px] 多猜（2 字）
- [u 28px] 公里（2 字）
- [div 32px] +13（1 字）
- [div 28px] B（1 字）
- [div 34px] 6（1 字）
- [div 44px] 4（1 字）
- [div 32px] ×0.4（1 字）
- [div 32px] +2（1 字）
- [div 32px] ×1（1 字）
- 合计（不含小标签、图表）：21 块，24 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s4_l21.png`
### l22（8.3s）
- 口播：先看最后一层的三个旋钮。每个旋钮分到的责任，也就是它的坡度，等于错误乘上送进它的数。
- [h2 54px] 责任 = 错误 × 送进来的数（9 字）
- [eyebrow 22px] 03 · 做个小实验（6 字）
- [div 28px] A（1 字）
- [div 44px] 6（1 字）
- [div 32px] ×2（1 字）
- [div 32px] ×1（1 字）
- [div 32px] +1（1 字）
- [div 56px] 29（1 字）
- [n 84px] 5（1 字）
- [u 28px] 公里（2 字）
- [div 32px] +13（1 字）
- [div 28px] B（1 字）
- [div 34px] 6（1 字）
- [div 44px] 4（1 字）
- [div 32px] ×0.4（1 字）
- [div 32px] +2（1 字）
- [div 32px] ×1（1 字）
- 合计（不含小标签、图表）：16 块，25 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s4_l22.png`
### l23（6.5s）
- 口播：送进来的是六、四、一，所以分到三十六、二十四、六。送进来的越大，分到的越多。
- [h2 54px] 责任 = 错误 × 送进来的数（9 字）
- [eyebrow 22px] 03 · 做个小实验（6 字）
- [div 28px] A（1 字）
- [div 44px] 6（1 字）
- [div 32px] ×2（1 字）
- [div 32px] ×1（1 字）
- [div 32px] +1（1 字）
- [div 34px] 36（1 字）
- [div 56px] 29（1 字）
- [n 84px] 5（1 字）
- [u 28px] 公里（2 字）
- [div 32px] +13（1 字）
- [div 28px] B（1 字）
- [div 34px] 6（1 字）
- [div 34px] 6（1 字）
- [div 44px] 4（1 字）
- [div 32px] ×0.4（1 字）
- [div 32px] +2（1 字）
- [div 32px] ×1（1 字）
- [div 34px] 24（1 字）
- 合计（不含小标签、图表）：19 块，28 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s4_l23.png`
### l24（5.4s）
- 口播：再往前一层，错误顺着连线往回走，路过哪个旋钮，就乘上哪个。
- [h2 54px] 传回去 = 错误 × 路过的旋钮（10 字）
- [eyebrow 22px] 03 · 做个小实验（6 字）
- [div 28px] A（1 字）
- [div 44px] 6（1 字）
- [div 32px] ×2（1 字）
- [div 32px] ×1（1 字）
- [div 32px] +1（1 字）
- [div 34px] 36（1 字）
- [div 56px] 29（1 字）
- [n 84px] 5（1 字）
- [u 28px] 公里（2 字）
- [div 32px] +13（1 字）
- [div 28px] B（1 字）
- [div 34px] 6（1 字）
- [div 34px] 6（1 字）
- [div 44px] 4（1 字）
- [div 32px] ×0.4（1 字）
- [div 32px] +2（1 字）
- [div 32px] ×1（1 字）
- [div 34px] 24（1 字）
- 合计（不含小标签、图表）：19 块，29 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s4_l24.png`
### l25（3.7s）
- 口播：A 那边乘二，收到十二。B 那边乘一，收到六。
- [h2 54px] 传回去 = 错误 × 路过的旋钮（10 字）
- [eyebrow 22px] 03 · 做个小实验（6 字）
- [div 28px] A（1 字）
- [div 40px] 6 × 2 = 12（3 字）
- [div 44px] 6（1 字）
- [div 32px] ×2（1 字）
- [div 32px] ×1（1 字）
- [div 32px] +1（1 字）
- [div 34px] 36（1 字）
- [div 56px] 29（1 字）
- [n 84px] 5（1 字）
- [u 28px] 公里（2 字）
- [div 32px] +13（1 字）
- [div 28px] B（1 字）
- [div 34px] 6（1 字）
- [div 34px] 6（1 字）
- [div 44px] 4（1 字）
- [div 32px] ×0.4（1 字）
- [div 32px] +2（1 字）
- [div 40px] 6 × 1 = 6（3 字）
- [div 32px] ×1（1 字）
- [div 34px] 24（1 字）
- 合计（不含小标签、图表）：21 块，35 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s4_l25.png`
### l26（5.0s）
- 口播：两个小单元再用同样的办法，算出自己两个旋钮的责任。
- [h2 54px] 责任 = 收到的 × 送进来的数（10 字）
- [eyebrow 22px] 03 · 做个小实验（6 字）
- [div 28px] A（1 字）
- [div 44px] 6（1 字）
- [div 32px] ×2（1 字）
- [div 32px] ×1（1 字）
- [div 32px] +1（1 字）
- [div 34px] 36（1 字）
- [div 34px] 60（1 字）
- [div 34px] 12（1 字）
- [div 56px] 29（1 字）
- [n 84px] 5（1 字）
- [u 28px] 公里（2 字）
- [div 32px] +13（1 字）
- [div 28px] B（1 字）
- [div 34px] 6（1 字）
- [div 34px] 6（1 字）
- [div 44px] 4（1 字）
- [div 32px] ×0.4（1 字）
- [div 32px] +2（1 字）
- [div 34px] 30（1 字）
- [div 34px] 6（1 字）
- [div 32px] ×1（1 字）
- [div 34px] 24（1 字）
- 合计（不含小标签、图表）：23 块，33 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s4_l26.png`
### l27（9.1s）
- 口播：就这么倒着走一趟，七个旋钮全拿到了自己的数。这次猜多了，七个都该往小拧，只是有的多拧、有的少拧。
- [h2 54px] 猜多了 → 都往小拧（7 字）
- [eyebrow 22px] 03 · 做个小实验（6 字）
- [div 28px] A（1 字）
- [div 44px] 6（1 字）
- [div 32px] ×2（1 字）
- [div 32px] ×1（1 字）
- [div 32px] +1（1 字）
- [div 34px] 36（1 字）
- [div 34px] 60（1 字）
- [div 34px] 12（1 字）
- [div 56px] 29（1 字）
- [n 84px] 5（1 字）
- [u 28px] 公里（2 字）
- [div 32px] +13（1 字）
- [div 28px] B（1 字）
- [div 34px] 6（1 字）
- [div 34px] 6（1 字）
- [div 44px] 4（1 字）
- [div 32px] ×0.4（1 字）
- [div 32px] +2（1 字）
- [div 34px] 30（1 字）
- [div 34px] 6（1 字）
- [div 32px] ×1（1 字）
- [div 34px] 24（1 字）
- 合计（不含小标签、图表）：23 块，30 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s4_l27.png`
### l28（6.7s）
- 口播：按这七个数各拧一小步再猜：从二十九变成差不多二十四，离二十三近多了。
- [h2 54px] 拧一小步：更准了（7 字）
- [eyebrow 22px] 03 · 做个小实验（6 字）
- [div 28px] A（1 字）
- [div 32px] ×1.82（1 字）
- [div 32px] ×0.7（1 字）
- [div 32px] +0.94（1 字）
- [div 40px] 23.88（1 字）
- [n 84px] 5（1 字）
- [u 28px] 公里（2 字）
- [div 32px] +12.97（1 字）
- [div 28px] B（1 字）
- [div 32px] ×0.25（1 字）
- [div 32px] +1.97（1 字）
- [div 32px] ×0.88（1 字）
- 合计（不含小标签、图表）：13 块，20 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s4_l28.png`
### l29（6.3s）
- 口播：再用笨办法核对：先不拧算一遍，再每个旋钮拧一下各算一遍，一共八遍。
- [eyebrow 22px] 03 · 做个小实验（6 字）
- [eyebrow 22px] 挨个试（3 字）
- [span 110px] 8（1 字）
- [h2 54px] 正着算（3 字）
- [h2 54px] 遍（1 字）
- [span 44px] 60（1 字）
- [span 44px] 12（1 字）
- [span 44px] 30（1 字）
- [span 44px] 6（1 字）
- [span 44px] 36（1 字）
- [span 44px] 24（1 字）
- [span 44px] 6（1 字）
- 合计（不含小标签、图表）：10 块，12 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s4_l29.png`
### l30（7.6s）
- 口播：算出来的七个数，跟反向传播一模一样。可反向传播只正着算了一遍，再倒着走了一趟。
- [eyebrow 22px] 03 · 做个小实验（6 字）
- [eyebrow 22px] 挨个试（3 字）
- [eyebrow 22px] 反向传播（4 字）
- [span 110px] 8（1 字）
- [div 110px] 1 遍 + 1 趟（4 字）
- [h2 54px] 正着算（3 字）
- [h2 54px] 遍（1 字）
- [span 44px] 60（1 字）
- [span 44px] 12（1 字）
- [span 44px] 30（1 字）
- [span 44px] 6（1 字）
- [span 44px] 36（1 字）
- [span 44px] 24（1 字）
- [span 44px] 6（1 字）
- [span 44px] 60（1 字）
- [span 44px] 12（1 字）
- [span 44px] 30（1 字）
- [span 44px] 6（1 字）
- [span 44px] 36（1 字）
- [span 44px] 24（1 字）
- [span 44px] 6（1 字）
- [h2 54px] ✓ 一模一样（4 字）
- 合计（不含小标签、图表）：19 块，27 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s4_l30.png`
### l31（5.4s）
- 口播：旋钮一多，差距就拉开了：十亿个旋钮，挨个试要算十亿零一遍。
- [eyebrow 22px] 03 · 做个小实验（6 字）
- [h1 76px] 十亿个旋钮（5 字）
- [span 92px] 1,000,000,001遍（2 字）
- [h2 54px] 挨个试（3 字）
- [span 28px] 遍（1 字）
- 合计（不含小标签、图表）：4 块，11 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s4_l31.png`
### l32（4.3s）
- 口播：哪怕一遍只要一秒，也得三十多年，这才走了一步。
- [eyebrow 22px] 03 · 做个小实验（6 字）
- [h1 76px] 十亿个旋钮（5 字）
- [span 92px] 1,000,000,001遍（2 字）
- [h2 54px] 挨个试（3 字）
- [span 28px] 遍（1 字）
- [div 38px] 一遍 1 秒的话，挨个试 ≈ 31.7 年，才走一步（15 字）
- 合计（不含小标签、图表）：5 块，26 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s4_l32.png`
### l33（6.5s）
- 口播：反向传播呢，还是一来一回。倒着那趟大约顶两遍，加起来也就三遍的工夫。
- [eyebrow 22px] 03 · 做个小实验（6 字）
- [h1 76px] 十亿个旋钮（5 字）
- [span 92px] 1,000,000,001遍（2 字）
- [h2 54px] 挨个试（3 字）
- [span 28px] 遍（1 字）
- [span 92px] ≈ 3遍（2 字）
- [h2 54px] 反向传播（4 字）
- [span 28px] 遍（1 字）
- [div 38px] 一遍 1 秒的话，挨个试 ≈ 31.7 年，才走一步（15 字）
- 合计（不含小标签、图表）：8 块，33 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s4_l33.png`
### l34（4.1s）
- 口播：没有它，几十亿个旋钮的大模型根本训练不动。
- [eyebrow 22px] 03 · 做个小实验（6 字）
- [h1 76px] 没它，大模型练不动（8 字）
- [span 92px] 1,000,000,001遍（2 字）
- [h2 54px] 挨个试（3 字）
- [span 28px] 遍（1 字）
- [span 92px] ≈ 3遍（2 字）
- [h2 54px] 反向传播（4 字）
- [span 28px] 遍（1 字）
- [div 38px] 一遍 1 秒的话，挨个试 ≈ 31.7 年，才走一步（15 字）
- 合计（不含小标签、图表）：8 块，36 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s4_l34.png`

## c_real（章节卡）
- 从 1986 到今天
- 截图：``

## s5 从 1986 到今天
### l35（10.7s）
- 口播：1986年，Rumelhart、Hinton、Williams 在《自然》杂志发了篇论文，把这个办法讲清楚了。
- [eyebrow 22px] 04 · 从 1986 到今天（6 字）
- [display 190px] 1986（1 字）
- [eyebrow 22px] 《自然》杂志 · 1986（5 字）
- [h2 54px] Learning representations by back-propagating errors（6 字）
- [div 22px] Rumelhart · Hinton · Williams · Vol. 323, pp. 533–536（8 字）
- 合计（不含小标签、图表）：3 块，15 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s5_l35.png`
### l36（5.7s）
- 口播：论文里说，坡度分两趟算：先正着一趟，再从输出那头倒着传回来。
- [eyebrow 22px] 04 · 从 1986 到今天（6 字）
- [display 190px] 1986（1 字）
- [eyebrow 22px] 《自然》杂志 · 1986（5 字）
- [h2 54px] Learning representations by back-propagating errors（6 字）
- [div 22px] Rumelhart · Hinton · Williams · Vol. 323, pp. 533–536（8 字）
- [h2 54px] 正着一趟 →（4 字）
- [h2 54px] ← 倒着一趟（4 字）
- 合计（不含小标签、图表）：5 块，23 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s5_l36.png`
### l37（7.0s）
- 口播：他们还发现，这么训练下来，中间那些单元会自己学会抓住任务里有用的规律。
- [eyebrow 22px] 04 · 从 1986 到今天（6 字）
- [display 190px] 1986（1 字）
- [eyebrow 22px] 《自然》杂志 · 1986（5 字）
- [h2 54px] Learning representations by back-propagating errors（6 字）
- [div 22px] Rumelhart · Hinton · Williams · Vol. 323, pp. 533–536（8 字）
- [h2 54px] 中间的单元：自己学会抓规律（12 字）
- 合计（不含小标签、图表）：4 块，27 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s5_l37.png`
### l38（5.9s）
- 口播：类似的算法更早也有人提过，这篇论文演示了用它训练多层网络。
- [eyebrow 22px] 04 · 从 1986 到今天（6 字）
- [display 190px] 1986（1 字）
- [eyebrow 22px] 《自然》杂志 · 1986（5 字）
- [h2 54px] Learning representations by back-propagating errors（6 字）
- [div 22px] Rumelhart · Hinton · Williams · Vol. 323, pp. 533–536（8 字）
- [caption 28px] 类似的算法，更早已有人提出（12 字）
- 合计（不含小标签、图表）：4 块，27 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s5_l38.png`
### l39（9.1s）
- 口播：现在用 PyTorch 这类框架，写一行 loss.backward()，所有旋钮的坡度就都算好了。
- [eyebrow 22px] 04 · 从 1986 到今天（6 字）
- [div 96px] loss.backward()（2 字）
- [span 96px] loss（1 字）
- [h2 54px] PyTorch：一次算好所有坡度（9 字）
- 合计（不含小标签、图表）：3 块，12 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s5_l39.png`
### l40（6.7s）
- 口播：这叫自动求导，底下就是反向传播：从输出倒着走，一路收集每个旋钮的坡度。
- [eyebrow 22px] 04 · 从 1986 到今天（6 字）
- [div 96px] loss.backward()（2 字）
- [span 96px] loss（1 字）
- [h1 76px] 自动求导（4 字）
- [h2 54px] 底下就是反向传播（8 字）
- [div 22px] 出处：PyTorch 官方教程（7 字）
- 合计（不含小标签、图表）：5 块，22 字
- 截图：`edu_videos/ai_terms/t13_backprop/reviews/lines_r2/materials/screen/zh/s5_l40.png`

## s6 片尾（画面：片尾卡）
### outro（包装卡，整段 20.4s）
- 口播 l41：反向传播，就是把错误从输出往回传，一层层分责任。
- 口播 l42：倒着走一趟，每个旋钮该往哪拧、拧多少，就全算出来了。
- 口播 l43：不过旋钮多了也有麻烦：模型可能把练习题背下来，换道新题就不会了。
- 口播 l44：下一期，咱们聊聊过拟合。
- 屏幕：错误往回传， 一层层分责任（11 字）
- 屏幕：过拟合（3 字）
- 截图：``

