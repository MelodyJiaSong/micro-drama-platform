# s7 修复报告 · 第三轮（fix070 / pregen r3，最后一轮）

产出：
- `fix070/s7_shots.json`：改了 6 镜（st4、st6、st1、st2、st3、st5），st7 没改。没有删镜头，也没有新镜头，播放顺序不变。**st4 镜长 10→11 秒，st3 镜长 15→16 秒**，其余不变。st5 的 `extras` 字段整个删掉了。
- `fix070/s7_frames.json`：3 张首帧要重画（st5、st6、st7）。st2 不用重画，见 I4/I5。
- overhead：st1、st2、st3、st4、st5、st6 都改了。st1、st2、st5、st6 已用 `shot_overhead.py` 重新出图，没有警告。**st3、st4 被闸门拦下**（「路点时刻须落在 0–15s / 0–10s」），原因是 overhead 已经按新镜长写好，filming.json 还是旧镜长。我在内存里把镜长换成 16 / 11 秒跑了一次闸门，两镜都通过，图也按新镜长出了；合并后请再正式跑一次。
- 自检：`check_patch070.py s7` 打印 **PASS**。我另外在临时集目录单独跑了 filming_lint（通过）和 shot_junctions（7 个接点，0 个 ⚠）。

用户定的四件事：s7 正文里没有写山，st5 首帧里也没有山（远处是海面暗线）；钱账方面 st1 写的是「钱已经花光，两手空着」，台词改成 `I don't have any money left`，还是一枚不剩，和 s6 对得上。浴场和 s1 拆镜不涉及本场。

## 逐条

### I3 / I8 [critical] P6、F5（s7_st5 端灯路人、沟底街面看不见）
- **已改** st5：照审稿人的方案①处理。`extras` 字段删掉；action、blocking、camera、lighting 里的路人和「那盏移动的小陶灯」都删掉；窄街改成「两排屋檐之间夹着一道窄窄的黑缝，那是藏在屋檐下面的窄街」，不再写「看得见沟底石板街面」和「近处那排房子的整面墙」。现在动作、走位、镜头、光线四行写法一致，都是「画面里只有屋顶、屋顶间的暗缝和零星的灯光」。
- **已改** overhead：删掉路人的 `[[prop]]`，0–4 秒那一拍改成小方窗熄灯，重新出图。
- **改首帧** st5：把画面中部偏右那条和瓦檐齐平、泛白的石板带改成屋顶间的一道暗缝，其余不变。
- 负面词「其他人」和首帧 prompt 里写路人的那段话由主会话处理（见任务书）。

### I4 [critical] P8 首帧 = 第 0 秒（s7_st5、s7_st1 / st2）
- st5：同 I3。原来首帧里没有路人、文字却要求有，现在路人删了，两边一致。熄灭的那扇小方窗在现首帧里就有（画面右边，横向约 86%、从上往下约 58%），重画时保留。
- st1 / st2 的视线：**已改**，统一成「越过右肩看身后灯上方那一小片较深的划痕」。我放大看了现在采用的 st2 首帧（15:02），她的脸是侧着朝画左、往左上看，和审稿人说的一样。审稿人建议统一成「望右上窗洞」，但那样要重画 st2 首帧。改成看划痕首帧不用动，而且她先回头看了墙上的划痕，接着说 `People write on, like, every wall here`、拇指往身后一指，动机来自她自己看到的东西，更顺。改动范围：
  - st1：action 和 beats 结尾（16.6–18 秒）从「抬头望窗洞」改成「转头越过右肩，看身后灯上方那一小片较深的乱划痕」，走位行和 overhead 原本就是这么写的（look (0.4,0.4)），保留。
  - st2：action 开头和 beats 0–1 秒从「望窗洞」改成「头转向画左、越过右肩看那片划痕」，走位行和 overhead 原本就是这么写的，保留。
  - prompt.txt 里不会再同时出现两种说法。
- s6_st6 左手那一项不在本场。

### I5 [critical] K8 镜间接点
- s7_st1 → st2：**已改**，见 I4。st1 最后一拍和 st2 第 0 秒都是「越过右肩看灯上方的划痕」，和 st2 首帧一致。
- s7_st3 → st5（灯灭两次）：**已改**。st5 熄灯的那扇窗写明是「画面右边、中远处一座房子高处的墙上的一扇小方窗」，并加上「其余几处天井和窗口的灯还亮着」，所以它是城里另一户人家熄灯，不是她的窗。她的窗是客房北墙上一尺见方的墙洞，这里写的是别人家的窗，位置也说清楚了。路人同 I3。
- s5_st5 → st7 不在本场。

### I9 / I27 [critical] V4、V6（s7_st4 一个人住店，对空闩座毫无反应）
- **已改**（只加动作，不加台词，也不加新的故事事实）：推上门以后，3.6–5 秒她朝门迈半步，左手摸到门板内侧那两个空着的木闩座，手指在空槽里一摸，停半拍，轻轻耸一下肩，再转回身。这样后面的 `Okay. Cozy.` 也就成了她接受了「这门锁不上」。闩座本来就写在每一镜的场景描写里，st4 首帧的门板内侧也画了两个闩座，不用重画。
- 后面的节拍顺延：转回身 5–5.7 秒，灯扫墙 5.7–7.7 秒（时长不变），台词 8.0–9.3 秒，收尾 9.4–11 秒（台词后留 1.7 秒）。**镜长 10→11 秒**。
- overhead：她迈半步后停在 (0.55,1.65)，离门 0.5 米，手够得着；灯的路点跟着手走；第二个机位关键帧挪到 5.7 秒。
- 上一轮这一条写的是「要用户定」。这次按审稿人给的便宜改法直接做了，故事点清单里关于门闩的说法请主会话同步（见下）。如果用户不要这一拍，删掉 3.6–5 秒那一拍、镜长改回 10 秒就行。
- s4_st1、s6_st2 首帧、s5 等其他镜头不在本场。

### I14 [major] K6 环境接续（s7 墙上的划痕）
- **改首帧** st6、st7：给墙面补上淡淡的、方向各异的短直线划痕，其余不变。st4 首帧门边的墙已经有细密的划痕，st1、st2 灯上方有一片深划痕，所以这几张不动。文字没改，各镜本来就写「墙面上划满深浅不一、方向各异的乱划痕」。
- s5、s1 的部分不在本场。

### I19 [major] N8（s7_st1 重念 s1_st2 的清单，every last coin 是包袱）
- **已改** 台词：`It's fine, though. It's a bed. And I'm honestly still thinking about that garum. I don't have any money left, but — yeah, I'd do it again.` 去掉了「every last coin」这个包袱，三件事不再按「床、鱼露、钱」一项一项排成清单，钱的那句是随口带出来的。
- 动作：说到 money left 时两手在膝上翻开、掌心朝上一摊（她两手空着，正好看得出钱花光了）；说到 `yeah, I'd do it again` 时笑着点点头，手放回膝上。去掉了原来「耸肩、摇头」配包袱的那组动作。
- 说话时间 2.4–13.7 秒，14–16.6 秒笑着舒一口气，镜长 18 秒不变。overhead 的节拍跟着改了。

### I39 [verify] E5 文字（st1 / st2 墙上的划痕）
- **不改**：照审稿人的建议，出片后抽帧检查。如果长出了字形，就局部修首帧，只留交叉的直线。

### I56 [minor] P4 火的方向（s7_st6 灯伸到床沿下面）
- **已改**：action、beats 改成「把灯放低到床沿外侧、贴近地面，往床底照」，lighting 改成「从侧面照亮床沿、绳网底面和床底的夜壶」。overhead 里灯的路点本来就在床沿外侧 (2.45,1.1)，只改了节拍文字。首帧不受影响（第 0 秒她在举灯照窗洞）。

### I72 [minor] N8（s7_st3 预告片式收尾）
- **已改** 台词，用了审稿人的版本：`Okay. I'm gonna try to sleep. I honestly don't know where I'll wake up tomorrow… but, uh — goodnight from Pompeii.`。按自然语速，说话时间 1.6–11.2 秒；吹灯 11.4–12.9 秒，12.9 秒灯灭，13.9–16 秒躺回去。**镜长 15→16 秒**。action、beats、lighting 里的秒数和 overhead 都改了。首帧不用重画。

### I75 [minor] N2（s7_st2 一句里套了两层插入语）
- **已改** 台词：`People write on, like, every wall here. And there's this famous one — I swear it was in my history textbook — from an inn just like this. It says, "Vibius Restitutus slept here alone, and missed his Urbana." That's kind of sweet.`。只剩一层插入语，`from an inn just like this` 单独成句。审稿人的版本里 `That's… kind of sweet` 带一个停顿，我去掉了，免得像在抖包袱。
- 节拍重排：just like this 那个摊手的动作挪到 11.3–13.2 秒，引文 14.8–21.0 秒，镜长 26 秒不变。action 里的叙述顺序也跟着改了。

## 交给主会话
1. **合并 filming.json**：`s7_shots.json` 里 6 个镜头整对象替换。st4 `duration` 10→11，st3 15→16；st5 的 `extras` 已经删掉。合并后运行 `python tools/shot_overhead.py ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st3` 和 `.../st4`（overhead 已经按新镜长写好；内存里模拟新镜长跑过闸门，能通过）。然后对 s7 全场运行 `python tools/shot_pack.py sync ai_videos/chuanyue_yiri/episodes/ep01`，重新编译 prompt.txt。
2. **重画首帧**：st5、st6、st7，按 `s7_frames.json` 做。st5 的 `st5_first_frame_prompt.txt` 还写着路人那段，要换成暗缝和熄灯小方窗的写法。st6、st7 的「不要」里保留「可读的字母」，防止划痕长出字形。
3. **story.md / story_beats.md 同步**（只改文字）：st1、st2、st3 的新台词；st4 关门后摸空闩座、耸肩那一拍；节点 38 的「钱一分不剩」的说法跟着 st1 新台词改。
4. 负面词（st5「其他人」、火山）按任务书由主会话处理。

## 需要用户定
- 无必须决定的事项。st4 摸空闩座这一拍是按审稿人的便宜改法直接加的，用户不想要的话按 I9 里写的办法回退。
