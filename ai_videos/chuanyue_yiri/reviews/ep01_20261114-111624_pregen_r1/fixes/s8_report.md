# s8 修复报告（EP01 出片前审查 r1 → fix065，follow-up 066）

产出：
- `s8_shots.json`：改了 9 镜（st2 st10 st3 st8 st4 st5 st9 st6 st7），每个都是完整对象；没有删镜，播放顺序不变（st1 不动）。
- `s8_frames.json`：3 张首帧要重画（st3、st4、st7）。
- overhead 已改并重出俯视图：st2 st10 st3 st8 st4 st5 st9 st6（原文件备份在 `fix065/s8_overhead_backup/`）。
- 镜长有变：st10 11→12、st8 10→13、st5 14→16、st9 21→23、st6 19→21（本场共多 11 秒）。

机检（把 s8_shots.json 合进 filming.json 的临时副本 `fix065/lint_s8/` 上跑）：`filming_lint --scene s8` 通过（原版有 1 处 [跨镜]「交给 st10」，已去掉）；`shot_junctions --scene s8` 11 个接点，0 个 ⚠，2 个视角切换提示（和原来一样）。
overhead：filming.json 里还是旧镜长，直接跑 `tools/shot_overhead.py` 时，5 个变长镜头会报「时刻超出镜长」。所以我用 `fix065/run_overhead_s8.py` 在内存里把镜长换成新值再跑，8 镜都出图、没有警告。主会话合并 filming.json 之后，要对 st10 st8 st5 st9 st6 正式再跑一遍 `shot_overhead.py`，再对 s8 跑 `shot_pack.py sync`。跑工具时顺带重画了 `scenes/s8/planning/s8_blocking.png`。

## 逐条

**I5 [critical] P8 首帧＝第 0 秒（s8_st2）**：已改。st2 首帧里 Riley 已经站定、两手垂着；文字照首帧改：第 0 秒她已站在门房面前约一米。改了 action / blocking / beats 第 0 拍，删掉「正迈步」。overhead 的路径改成第 0 秒已站定，5–5.5 秒往前跨半步伸手。

**I6 [critical] P9（s8_st7）**：已改。st7 的 point 改成「出了一身汗、神清气爽，也饿了」，和动作里的「衬衫被汗贴在背上」一致。

**I12 [critical] C11 反应合比例（st10、st3、st8）**：已改。
- st10：去掉「摇头笑出了声」和「嘴角一撇」。6.5–8 秒改成「嘴角微微一动、轻轻摇一下头、右手朝厅里一挥，嘴闭着」；10.5–12 秒改成「目光跟着她、还带一点笑意，转回去看门外，系紧钱袋口」。改了 action / beats / blocking。
- st3：第 0 秒没人笑，人人在做自己的事：梳头、叠布、系腰带、挽头发，深处三个在聊天。只有同伴在 4–5.5 秒被碰了一下才抿嘴憋笑。删掉「厅里只剩滴水声」（读起来像全厅都停了）。首帧也要改，进了 frames。
- st8：只留一次掩嘴（2.5–4 秒，同伴）。9–10 秒那次笑改成「年长妇女转回去和同伴接着小声说话」。

**I17 [critical] D1 说得完（s8_st9）**：已改，句子没动。“Kind of love it, though.” 的窗口放宽到 16.4–18.9 秒，Gross 后停半拍。还刮板和收尾整体后移，镜长 21→23。beats 和 overhead 已同步。

**I19 [critical] N8 修辞痕迹（s8_st4）**：已改 dialogue / beats / action。原句 “Why did I keep my clothes on? Rookie mistake.” 是自问自答再加一句收尾包袱，改成 “Everybody out there was in a sheet. I'm such an idiot.”（说 out there 时左手拇指朝身后来的方向一指；说 idiot 时摇头）。整句现在是：Oh my god, it is so hot in here. And I'm wearing, like, all of my clothes. Everybody out there was in a sheet. I'm such an idiot. 每秒约 2.5 词，说完后留 2.4 秒。交审时请用户听一下这句。

**I22 [critical] F1 景别与人物大小**：
- st10：已改 overhead。照首帧反推，机位挪到 (3.05,11.6)，离 Riley 约 1.3 米。Riley 在画面横向约 0.58，门房约 0.29，和首帧对上。仍和 st2 在两人连线同一侧，不跨轴。blocking 改成「离 Riley 约一米三」。
- st3：camera / beats 里的「背影在画面下部」照几何改成「头顶在画面上部约三分之一处，背影从头到大腿入画」。
- st9：Helvia 从「画右边缘只入画半身」改成「画右，整个上半身入画」（几何 u≈0.79，首帧 0.83）。改了 action / blocking / camera。
- st6：camera / blocking 从「腰以上」改成「两人坐着，从头到脚都在画里」，几何和首帧都是这样。
- st7：改首帧，老汉画到约 0.9 画高，进了 frames。

**I23 [critical] F3 画面位置**：
- st10：同 I22，overhead 已对齐首帧。
- st4：已改 overhead 和 blocking。原站位下热水池其实在画右边框外，note 却写「在镜头身后」，首帧画在画右。现在照首帧，机位改朝正北，Riley 在 (2.7,3.7)。圆盆落在画左约 0.14–0.31，热水池和台阶在画右约 0.6 起，和首帧一致。blocking 补了「身后偏右是热水池和台阶」。
- st9 / st6 / st3：同 I22。

**I24 [critical] F4 节拍秒数（s8_st10）**：已改。「回头、点头、走出画」原来挤在 1.5 秒里，现在给 2.5 秒（8–10.5 秒）；门房收尾一拍放在 10.5–12 秒，镜长 11→12。overhead 的出画路线离镜头 1.2 米以上。

**I25 [critical] F8 看点画得出来（s8_st7）**：已改，同 I6。

**I28 / I29 [critical] V1 语言、V2 肢体（s8_st2、s8_st5/st9）**：已改。
- st2：Riley 先开口说「Salve!」（1.3–1.9 秒，读得比早上的 Sal-VAY 准一点，有点得意），门房是听到招呼才抬头，并点头回礼。原来那句「两手垂在身侧，不比划」删掉。改了 dialogue / action / beats / blocking。
- st5：接刮板时她说 “Oh — thank you.”（13.0–14.2 秒），Helvia 点一下头。
- st9：还刮板后她笑着冲 Helvia 点头。
- st6：收尾她转向 Helvia，点头、右手按胸口。
- st10：她走前回头朝门房点头、左手按胸口。

**I30 [critical] V6 动机（s8_st2→st10、s8_st3/st8）**：已改。
- 钱：Riley 不知道票价，就把一手 7 枚摊给门房、挑眉等她自己拿；门房看一眼那枚金黄大币，只捏走最小的浅色小铜币。所以她在 st2 的 10–11.5 秒「眉毛一扬、不敢信地笑」，到 st10 说 “literally one tiny coin” 也就顺了。钱账：付前 7 枚（5 as＋1 quadrans＋1 sestertius）→ 门房捏走 quadrans → 塞回 6 枚（5 as＋1 sestertius），和首帧一致（首帧这时还没掏钱）。
- 穿衣进热水室：st8 加了 4–7.5 秒这段。年长妇女朝她头顶的壁龛抬下巴，看看她的衬衫，摇一下头。Riley 看一眼壁龛，手摸到最上面那颗扣子，停一下又松开，脸一红，点个头，然后快步进去。「没脱」是她自己当场决定的，和 st4 的 “I'm such an idiot” 接上。st8 镜长 10→13，走路 8–12.6 秒，约每秒 1.5 米。

**I42 [critical] Helvia V5 回应（st6、st5、st9）**：已改，但审稿建议的「嗤地笑、摇头笑」没照搬，见下面第 3 点。
- st5：原来的「抬抬下巴」改成：把刮板搁在膝上，拿起油瓶朝她晃一晃，再朝她胳膊努努嘴，Riley 才会意伸手。滴完油后 Helvia 还用手掌在自己小臂上比划着抹两下。
- st9：Riley 对镜头说话时，Helvia 一直在抹自己的油、拢鬓角的头发。看到 Riley 刮出一道干净皮肤，她停下手点一下头。接回刮板时点头，最后和 Riley 互相笑着点头，嘴闭着。
- st6：Helvia 全程手上有活。Riley 朝她偏头时，她抬眼看一下、眉毛轻轻一抬；Riley 道谢时她点头，朝门口方向摆一下手。
- 没照搬的原因：任务书规定「对空气说话、旁人憋笑」全集只留 2–3 处，本场只留 st10 门房那一处。Helvia 听不懂英语，所以只对动作和手势起反应，对 Gross 之类的英语不起反应。

**I46 [major] P7 服装与动作（s8_st5）**：已改，不用重画首帧。首帧里 Helvia 的左臂整条光着，袖子撩上去了。文字照首帧写：第 0 秒她左边的半袖撩到肩头，正刮左小臂靠肘那段；14.2–16 秒她把左袖拉回肘部，接上 st9 / st6 首帧里半袖到肘。

**I47 [major] C9 像真人（st9 / st10 / st6、st8）**：已改。本场「对空气说话、旁人反应」只留 st10 门房一处，而且改得克制。st9 和 st6 的 Helvia 不再对英语憋笑。st8 的两次掩嘴笑只留一次。

**I56 [major] V5 回应（s8_st5/st9、s8_st6→st7）**：已改，同 I28。st6 最后加了一拍（19–21 秒）：Riley 转向 Helvia 点头、按胸口道谢，Helvia 点头、摆手让她去。镜长 19→21。她不站起来，因为这个机位一站起来头就出画了。

**I65 / I66 [major] 路人 V5 / V6（s8_st8）**：已改，同 I30。年长妇女用抬下巴、指壁龛、摇头来「沟通」，同伴只掩一次嘴。

**I68 [verify] C1·C2（s8_st2）**：已改，同 I30。门房自己挑钱，Riley 的「试探」看得出来。

**I70 [verify] D3 拉丁语**：不改。句子来自 Petronius《Sat.》41（人物卡写了 r05 #21 ✅）。审稿说它是编写句，和人物卡说法不一样。dialogue 括注里删掉了「笑着耸肩」（见 I137），读法没动。转写和发音要不要再核，交给主会话 / 用户。

**I72 [verify] E6 史实（s8_st10 门票价）**：不改，交给主会话。r03 写的是罗马城的价，庞贝的实价和女区的价都没查到；交付前要复核来源。

**I74 [verify] F6·F5 座次（st3→st8）**：已改 st3。st3 画左三位从近到远：梳头的 (0.7,9.4)、年长的 (0.75,8.2)、三十来岁的同伴 (0.9,7.6)，后两位和 st8 同坐标。st3「靠里第三位」到 st8 不见了的问题这样解决：画左靠前梳头的那位在 st8 的画框左边外面（几何上偏出 35°，超过半视角 27°）。st3 首帧要跟着改，进了 frames。

**I86 [minor] P6 距离（st5→st6）**：只改文字。st5 的 blocking 从「相隔不到一米」改成「相隔约一米」，overhead 是 0.9 米。st6 首帧看上去略宽，相接时差几十厘米，不显眼，不重画。

**I94 / I135 [minor] Helvia 对听不懂的英语起反应（s8_st9）**：已改。删掉「听到 rub oil all over yourself 时抬眼瞟她」，她的反应只对刮出的那道干净皮肤。

**I107 [minor] E3 服饰（st3、st8）**：
- st3：改首帧，进了 frames。action 里的衣服写成「一整块粗亚麻布从双肩裹到小腿，前襟斜搭交叠，圆领口贴着锁骨，腰间一根同色布带」，和 Helvia 人物卡一致；没照审稿写的「从腋下裹」，因为人物卡和本片着装安排都是遮到双肩。
- st8：不改首帧。我看 st8 首帧画左两位是大块粗织布裹在身上，没有翻领，也不是毛巾布；文字已经和 st3 统一。主会话要是看法不同，可以照 st3 的 edit 补一张。

**I121 [minor] F5 overhead 只放 3 人（s8_st3）**：已改。overhead 补齐 7 人：画左 3、画右靠前 1、厅深处 3。厅深处那 3 位和 st8 画右深处的远景是同一批，坐标都是 (5.3,3.0)。

**I123 [minor] V3（s8_st4）**：改首帧，进了 frames。文字第 0 拍改成「热得眯眼皱眉、鼓腮呼地吐气」，表情和 action 一致。

**I134 [minor] Helvia st5 全程无声**：不改声音。没加「嗯——」这类声音：一方面 bible 第 14 行规定出词要由考据给，另一方面 st5 的台词行只给 Riley。改成加手势：晃油瓶、努嘴、在自己小臂上比划抹开，她「热心教人」从动作上看得出来。

**I136 [minor] V3 st5 首帧 Helvia 已在笑**：只改文字。人物卡外观本来就写「嘴角带着一点看热闹的笑」，首帧没错。第 0 拍写成「脸上带着平常那点和善的笑、眼睛看着自己的胳膊」；2.5 秒的反应从「嘴角一抽、笑一下」改成「眉毛一挑」，不叠加笑。

**I137 [minor] V3 st6 重复耸肩**：已改。dialogue 括注删掉「笑着耸肩」，只留「带笑」；手上只有说到 versas 时那一翻。

**I138 [minor] V3 门房（s8_st10）**：已改，同 I12。

**I140 [minor] V7 门房要不要立卡**：交给主会话。门房出现两镜、收钱、和 Riley 有互动，按 bible 第 40 行应该立卡，或者在 bible 里写明「无名配角」例外。我没改人物卡和 bible。

**I143 [minor] V4 门房视线（s8_st2）**：已改。6.5–8.5 秒门房低头看她手心里的钱，目光在金黄大币上停一下，才捏起小铜币。

## 交给主会话

1. 把 `s8_shots.json` 合进 `episodes/ep01/filming.json`。合完对 st10 st8 st5 st9 st6 正式跑一遍 `python tools/shot_overhead.py <镜目录>`（我已用内存覆盖镜长的方式验证过，没有警告），再对 s8 跑 `shot_pack.py sync`。
2. 重画 3 张首帧：st3、st4、st7（见 `s8_frames.json`）。st3 的 edit 改动比较多（7 人换衣服、画右三人挪到深处、座次），要是局部改图做不出来，就只能整张重出。
3. I140：给门房立最小人物卡，或者在 bible 写明无名配角例外。
4. I72：庞贝浴场（女区）门票价的出处，交付前复核。
5. I70：Helvia 这句拉丁语的出处说法不一致（人物卡说出自 Petronius *Sat.* 41，审稿说是编写句），请考据核一下。

## 需要用户定

- st4 新台词 “Everybody out there was in a sheet. I'm such an idiot.”（替换 “Why did I keep my clothes on? Rookie mistake.”）：按规则改是为了自然，请用户听感确认。
- st5 加的 “Oh — thank you.”：原来是无声镜头，现在 Riley 开口了。
- 故事点清单里本场节点 19（换转场）、20B（门房要两枚）、24A（Helvia 指天比日落）、25（缩短 / 删出浴场镜）这些备选，审稿问题清单没要求改，我没动，仍等用户选。
