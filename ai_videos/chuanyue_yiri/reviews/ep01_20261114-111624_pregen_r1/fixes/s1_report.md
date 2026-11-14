# s1 修复报告（EP01 pregen r1 → follow-up 066）

产出：`s1_shots.json`（改了 st1、st2、st3、st4、st5 共 5 镜，没有删镜，播放顺序不变）、`s1_frames.json`（1 张首帧要重画：st5）、本场 5 个 `overhead.toml` 已改，并重出了俯视图。
时长变化：st1 22 → 23 秒，st3 18 → 20 秒，其余不变。

机检：把新镜头并进临时副本跑了 `tools/filming_lint.py --scene s1`，结果通过；`tools/shot_junctions.py --scene s1` 的结果是 5 个接点、0 个 ⚠，另有 1 个视角切换提示，就是 st1→st2 拿起相机这一处，属于 bible 写明的例外。
overhead：`filming.json` 还没合并，所以这次是用 `overhead_s1.py` 包一层去跑 `tools/shot_overhead.py`：它只在本次运行里把时长换成 s1_shots.json 的新值，不写 filming.json。5 镜都出了图，没有 ✗。顺带重画了场级走位图 `scenes/s1/planning/s1_blocking.png`。**主会话合并 filming.json 后，请对 st1、st3（这两镜时长变了）按正常命令再跑一次 `python tools/shot_overhead.py …`，再跑 `shot_pack sync`。**

## 逐条

### I1 [critical] 道具来源与去向
- **已改 st2（action / blocking / beats）**：钱的排法改成和 p6 道具图一样：靠指根两排各 3 枚 as，靠手腕一排是 1 as、quadrans、sestertius。原来写的一排 4 枚，比手掌还宽，这次一起去掉了。
- **已改 st2**：不再写「攥拳 → 摊开就排好」。左手从第 0 秒起就在画框下方，手心朝上微微拢着，托着刚从左裤袋掏出来、已经在手心摊开的 9 枚钱。20.8 秒把手平稳抬到镜头前，说 this 时四指伸直、手心摊平。收尾四指一合，攥回拳头放低出画。托着钱的手没法再竖拇指，所以 everyone here 那一下改成朝身后的城偏一下头、眼睛往后一瞟。首帧左手本来就在画框外，不用重画。
- **已改 st1（action / blocking / beats / camera）**：相机写明架在「齐胸高的轻便三脚架上」，机高 1.5 米和 overhead 一致。结尾改成「握住相机，把它从三脚架上拿起来」。三脚架一直在画外，st2 自拍也拍不到它，所以留在沙滩上不交代。没有采用「连杆一起拔起来」：那样 st2 的自拍里会出现杆子，和 bible「画面里不出现自拍杆」冲突。
- **已改 st4 overhead.toml**：旧注释里的「两根绳、各攥一根」、meta.note 里的「各攥一根 / 各抓一只提耳」、0–2.5 秒节拍里的「各攥一根」，都改成「一根绳、四只手都在这一根绳上」「各用双手抓住提耳」，重出了俯视图。

### I2 [critical]（跨场）
- s1 部分（st2 一排 4 枚 as 放不下）**已改**，见 I1。s2 的浑水和 bg2 卡不在本场范围。

### I17 [critical] 说得完（s1_st1）
- **已改 st1（duration / beats / blocking / camera / dialogue）**：镜长改为 23 秒。Wait, wait — I gotta do this right. 的窗口放宽到 16.8–19.6 秒（2.8 秒，约 2.5 词/秒），16.5–19.5 秒按正常步速（约 1.4 米/秒）边走边说。19.5–21.5 秒站在镜头前笑，21.5–23 秒拿起相机，说完后留了 3.4 秒。句子没删词。

### I21 [critical] 规则源（维苏威 / 葡萄藤山）
- **需要用户定 / 交给主会话**：bible §9、dossier 第 16 和 78 行、bg1 场景行，对那座山该怎么写说法不一。s1 的 st1、st2、st4 三张首帧画右都是一座满坡葡萄藤的锥形大山。要等先定好「山入不入画、写成什么样」，再决定这三张首帧要不要局部重画，所以暂时没列进 frames 清单。s1 分镜正文本身没有写山。

### I26 [critical] 正文要相机、负面词禁相机
- **已改 st1**：加了 `"allow_negatives": ["相机"]`，「手机」「自拍杆」继续保留。编译器已经支持这个字段（episode_workflow__entity.py）。

### I48 / I79 st5 首帧受光侧反了
- **改首帧（st5）**：首帧是画右一排也被照亮。按机位朝西、五月清晨太阳在东偏北推算，分镜写的「画左上半截亮，画右和街面在阴影里」是对的，所以文字不改，改图，已列进 `s1_frames.json`。
- 顺手统一了 st5 的路面水：动作行原来写「路面中线一线流水」，光线行写「排水沟里一线流水」，现在都改成和 bg2-2 卡一致的「两侧略高、中线略低，中线上一线积水反光」。

### I50 [major] st2 开场稿感
- **已改 st2 dialogue / beats**：「Okay, so, two goals today: find… and try garum…」改成「Okay, two things today: I need somewhere to sleep before it gets dark, and I need to try garum — …」，口气更像随口说。
- **不改**的部分：开场句 Good morning from Pompeii! 保留。它是 st1「I gotta do this right」之后有意重新开录，正是 filming.md「镜与镜接得上」给的范例。亮钱的停顿也保留：九枚钱是故事点 2「全部预算一眼看懂」的核心，而且 p6 已经出过两次「手心只有 6 枚」，需要那 2 秒让镜头看清。
- 节拍按新词数重排：9–14.8 秒 13 词，14.8–20.8 秒 15 词，都不超过 2.5 词/秒。

### I52 [major]（s1_st4 部分）
- **已改 st4 overhead.toml**：0–8 秒 Riley 的朝向点从 (37.8,54.0) 改到 (36.8,56.5)，俯视图上显示侧身，和首帧的左侧脸一致。绳子相关的注释和节拍也一并清理了，见 I1。s2_st3 不在本场范围。

### I53 [major] 否定句
- **已改 st4**：「没有耳钉、没有耳环，耳朵上没有任何金属亮点」改成「耳垂光着，被头发盖住」；「不变短、不消失」改成「整根绳子一直平摊在沙上、看得见」；「不凑成脸部大特写」改成「仍是大腿以上的中景」。
- **已改 st2**：「互不重叠」改成「一枚挨一枚分三排」；「没有银灰色的钱」改成「钱都是红铜色和金黄色」；「不叠成一摞、不滑落、不增不减」和「手指不碰钱」改成「9 枚一直平贴在她手心里、一枚不少」。

### I54 [major] 正文混入别镜
- **已改 st1 action**：删掉「（下一镜她举着它自拍）」。s1 其他镜头没有这类写法。

### I55 [major] prompt 过长，st4 节拍过满
- **已改（部分）**：st2 把动作描述里的重复删掉了一些，钱的排法只写一遍。st4 补了渔夫手上的活，正文没有变短。
- **不改**：st4 不拆成两镜，拆镜要多花积分，需要用户同意。
- **交给主会话**：「画面 / 走位 / 动作 / 镜头」四行反复写同一串动作，是编译器的问题。

### I56 [major] Riley 不回应（s1_st5 部分）
- **已改 st5 action / beats**：赶驴人点头时，「Riley 笑着点一下头回礼」。st5 的 overhead.toml 里原来还残留「赶驴人瞥她的裤子」「她低头看自己的裤子」，和分镜不一致，已按分镜改正。裤子梗全集只用一次，留给 s2。

### I57 [major] Felix
- 不在本场范围，没有动。

### I65 [major] 路人回应（s1_st4 部分）
- **已改 st4 action / beats**：按任务书，「对空气说话、旁人憋笑」这个梗不放在这里。她说话的 8 秒里，两个渔夫手上的活不停：年长的拢鱼、拣出海草甩到沙上，年轻的把一只小螃蟹扔回浪里。约第 13 秒她朝鱼筐偏头，年轻渔夫只对这个看得见的动作抬眼看她半秒，又低头干活，不对任何英语词起反应，也不交换眼色。

### I78 / I118 [minor]「快步」和实际速度对不上
- **已改 st1**：「快步」改成「用平常的步子」。4.1 米用 3 秒，约 1.4 米/秒，overhead 路点已同步。

### I98 [minor] st2 到 st4 音量跳变
- **已改 st4 beats / action / overhead**：11.7–12.5 秒加了一拍：她先回头看一眼两个渔夫，像怕吵着他们，再转向镜头、探身、压低声音，给小声说话一个来由。

### I99 [minor] 接点表把拉丁语记在 Riley 名下
- **交给主会话**：要改 `tools/shot_junctions.py` 的台词拆分。s1 没有拉丁语，不受影响。

### I100 [minor] st1 台词
- **已改 st1 dialogue / beats / overhead**：「Like, real, two-thousand-years-ago Pompeii.」改成「Like, the real one.」。st2 紧接着会说 75 AD，年代信息不会丢。说完到 Wait 之间多出约 3 秒，填上「扭头越过右肩再望一眼城」这个反应（14–15.5 秒），她不会空站着。

### I102 [minor] st3 台词
- **已改 st3 dialogue / beats / action / overhead**：改成「Oh — look at all these cracks. They're all patched up. There was this huge earthquake here, like, twelve years ago — and they're still fixing it.」，避开和 st4 连着两次用 See…，口气也从讲冷知识变成随口聊。
- 保留「twelve years ago」：Seneca 记的地震是 63 年，到 75 年正好 12 年，见 r01 第 80 行。
- 新台词 25 词，按正常语速要约 10 秒，所以镜长 18 → 20 秒，台词放在 7.6–17.9 秒，说完后留 2 秒。挑夫和骡子的路点延到第 20 秒，一直在画里。

### I117 [minor] st3 工人回礼发生在画外
- **已改 st3 beats / action / blocking / overhead**：工人那几拍整体提前约 0.8 秒：2.2–3 秒看她，3–3.7 秒她打招呼，3.7–4.4 秒点头回礼并转身，约第 5 秒出画右。按 overhead 算，他约 4.75 秒才超出半视角，这几拍都在画内演完。工人位置不动，首帧不用重画。

## 交给主会话
1. **合并**：把 `s1_shots.json` 的 5 镜并进 filming.json。合并后对 st1、st3 正常重跑 `shot_overhead.py`（时长变了），再对 s1 跑 `shot_pack sync`。
2. **I21**：bible §9、dossier 第 16 和 78 行、bg1 场景行对山的写法要统一（是否入画、去掉「葡萄藤」）。定下来以后，再判断 s1 st1、st2、st4 三张首帧画右的葡萄藤锥形山要不要局部重画。
3. **I55**：编译器让「画面」行只写静态构图，动作只留在「动作」一行。st4 是否拆镜要用户批积分。
4. **I99**：修 `tools/shot_junctions.py`，台词按说话人拆分。

## 需要用户定
- I21：山的处理，见上。
- st4 要不要拆成两镜（要积分）。
- I50 中保留的部分：「Good morning from Pompeii!」开场和 2 秒亮钱。我的判断是保留，理由见上；如果想改成故事点清单里的 2B（不报目标、只说预算），需要用户挑选。
