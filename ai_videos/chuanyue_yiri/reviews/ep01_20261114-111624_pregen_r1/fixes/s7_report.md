# s7 修复报告（fix065 / follow-up 066）

产出：`s7_shots.json`（改 7 镜：st4、st6、st7、st1、st2、st3、st5，无删镜、播放顺序不变）、`s7_frames.json`（3 张首帧要重画：st1、st2、st5）、本场 overhead（st1、st2、st3、st4、st5、st6 已改；st7 不用改）。
机检：把 s7_shots.json 套进一份临时 filming.json 后跑了 `filming_lint`，s7 的问题清零（原来 st1 有一条「上一镜」）；`shot_junctions --scene s7` 共 7 个接点，0 个疑点。
俯视图：st1、st3、st4、st5、st6 已用 `shot_overhead.py` 重出，没有警告。**st2 重出被闸门拦了**：overhead 已经按 26 秒写好，但 filming.json 里还是 23 秒；主会话合并 s7_shots.json 后要再跑一次（见下面「交给主会话」）。

## 逐条

### I8 [critical] P9 效果有来源（s7_st3、s7_st7）
- **已改** st3 `lighting`：改成「0–12.3 秒……12.3 秒火苗灭后」，并补一句 10.8–12.3 秒吹气时火苗被吹得一斜一晃；和 beats、道具行、overhead（物件标签「12.3 秒吹灭」）对齐。
- **已改** st7 `lighting`：改成「0–13.8 秒灯在她右手里……13.8–15.8 秒平放到凳上……15.8 秒起灯在小凳上」，和 beats、道具行、overhead [[beat]] 一致。

### I19 [critical] N8 修辞痕迹（只改 s7_st1）
- **已改** st1 `dialogue`：`So I got a bed, and I got to try garum. I'm totally broke now. But it was so worth it.`——两件事用 and 连起来，花光钱单独一句平说，最后一句平平地收；去掉了三项并列、省略号停顿抖包袱、自问自答「Honestly? Worth it.」，开头也去掉了一个 Okay（本场 Okay 太多）。`beats`、`action` 的手势跟着重排（bed 拍床、garum 点头、broke 摊手耸肩），说话 1.6–10.4 秒，前后各留余量，镜长 13 秒不变；overhead 同步。
- 其余镜头（s4_st5、s3_st2 等）不在本场。

### I20 [critical] E5 文字（s7_st1、s7_st2）
- **已改** st1 `action`/`beats`/`camera`、st2 `action`/`beats`/`camera`：灯上方那片刻痕一律写成「一小片刻得较深、交错杂乱的划痕，看不出行、看不出字形」，删掉「几行排得整整齐齐」「整齐的刻痕」「看得清」；st2 不再给那片墙「看得清」的要求。
- **改首帧** st1、st2：首帧里已经画成了伪拉丁字母，进了 frames 清单（只改那一小片墙，其余不动）。
- 视频负面词要补「像字母的刻痕、成行的伪文字」，本字段改不了，见「交给主会话」。

### I21 [critical] E7 规则源（本场只有 s7_st2）
- **已改** st2：同 I20，去掉了诱发伪文字的「几行排得整整齐齐、刻得比别处深的细线」。
- **改首帧** st2（同 I20）。
- bible §9 / dossier 维苏威说法、bg1 场景行、p4 刮板卡不在本场，见「交给主会话」。

### I22 [critical] F1 景别与人物大小（本场 s7_st6、s7_st3）
- **已改** st6（overhead 按首帧反推）：用首帧里四个参照（小凳 u≈0.05、窗洞 u≈0.47、床尾东南角 u≈0.57、Riley u≈0.69，离镜头约 1.6 m）解出机位其实在东南角 (2.95,3.05)、朝西北偏北，Riley 在床尾东边 (2.95,1.5)，距镜头 1.55 m。overhead 机位、Riley 和灯的路径照此改；分镜 `blocking`、`camera` 里的「西南角朝东北」改成「东南角朝西北偏北，离 Riley 一米半左右」，门写成「在画面左边之外」。首帧不用重画。
- **已改** st3：按首帧（脸约一米外、头离灯约三十厘米）把机位前移到 (1.3,1.9)，景别改「中近景」，Riley 的头挪到 (0.9,0.8)（离灯约 0.45 m，凑过去吹时嘴离灯苗二十多厘米）；`blocking`、`camera` 的「中景、离床沿一米多」改成「中近景，离床沿大半米、离她的脸一米左右」。24mm 下灯（画左）和窗洞（画右上）都能入画。首帧不用重画。

### I23 [critical] F3 画面位置（本场 s7_st6、s7_st3）
- **已改**：同 I22。st6 新机位下 Riley 横向位置算出来 u≈0.69，和首帧一致；st3 灯在画左、窗洞在右上，和首帧一致。

### I24 [critical] F4 节拍秒数（本场 s7_st7、s7_st3、s7_st6）
- **已改** st7、st3 光线秒数（同 I8）。
- **已改** st6：首帧里夜壶第 0 秒就在画内，删掉 4.5–6.5 秒（overhead 写 6–8 秒）的下摇，改成固定机位（`camera` 文字、overhead 只留一个机位）；挪半步从原来压在 5.8–6.0 秒改成 6–6.6 秒，下蹲 6.6–7.4 秒（`blocking`、`beats`、overhead 路径和 [[beat]] 一致）。

### I25 [critical] F8 看点画得出来（本场 s7_st4、s7_st5）
- **已改** st4 `point` 改成「……满墙划痕、一张铺着草垫的木床」，`action`/`beats` 的「落到绳底木床上」改成「落到铺着草垫和深褐毛毯的木床上」（绳网留到 st7 掀草垫时才露出来）；顺手把 `lighting` 里「没有月光照进屋」「没有光束从窗洞照进屋」等否定句改成正向写法。overhead beat 同步。
- **已改** st5 `action`/`blocking`/`beats`：窄街写成「像屋顶之间一道深沟：两边墙面从屋檐落到石板街面，街面比屋檐低一层楼」，路人走在沟底；overhead note 和 beat 同步。
- **改首帧** st5：首帧里路人像走在屋顶平台上，进了 frames 清单（只把他脚下那段改成看得出的街槽）。

### I30 [critical] V6 动机（本场 s7_st4–s7_st3、s7_st2）
- s7_st2「她读不懂拉丁文却认出墙上那句」：**已改**，做法见 I67。
- s7_st4–st3「一个人住店，从不看门闩」：**需要用户定**。审稿建议在 st4 关门后摸一下门边发现没有闩、愣一下，st6 补一句 `…and no lock. Cool cool cool.` 或拿凳子顶门。这会加一个故事点、加台词，并改动 st6 已经定的笑点节奏，属于故事层，按规定要用户在 story_beats.md 选。本轮没改。

### I48 [major] K4 光与时间（本场 s7_st3、s7_st7）
- **已改**：同 I8。s1_st5 不在本场。

### I67 [verify] C1 她怎么读得懂刻痕（s7_st2）
- **已改** st2 `dialogue`：`People write on, like, every wall here. And there's this famous one, from an inn just like this — I swear it was in my history textbook — that says, "Vibius Restitutus slept here alone, and missed his Urbana." Which is kind of sweet.`——她是在想起课本上一家客栈墙上的名句，不是在读这面墙。手势同步改：说 every wall 时拇指越过右肩朝身后满是划痕的墙一指，说 just like this 时左手朝屋里一摊；去掉了「朝那一小片刻痕一指」（会让人以为她在读这片）。台词按正常语速多了约 3 秒，**镜长 23→26 秒**，`beats` 重排（说话 2.3–23.7 秒，前后各留余量），overhead 同步。
- `point` 改成「住客在墙上留话是庞贝的日常：她想起课本上一家客栈墙上的名句……」。

### I69 [verify] K1 st6 拿灯的手
- **不改**：放大首帧核过（裁切图 `s7_st6_arm_crop.png`）。她背对镜头、脸朝画左，靠镜头这一侧垂着的是左臂，从身体前面举起来托灯的是右手，和分镜一致。

### I71 [verify] E6 史实（s7_st2）
- **已改**：同 I67。台词写成「from an inn just like this」，不再说就在这面墙上；这和 CIL IV 2146 原址在另一家客栈（VII.12.35）对得上。

### I104 [minor] N4 口头禅
- **已改** st1（去掉 Honestly）、st3 `dialogue` 改成 `Okay. I'm gonna sleep. No idea where I'm gonna wake up tomorrow… but — goodnight from Pompeii.`（去掉 Honestly，beats 秒数微调到 4.0–7.6 / 8.2–8.5 / 9.0–10.4，吹灯 10.8–12.3 秒不变）。全集的 Honestly 现在只剩 s4_st5 一处（那一处由 s4 决定留不留）。

## 交给主会话
1. **合并 filming.json**：s7_shots.json 的 7 镜整对象替换；st2 `duration` 23→26。合并后跑 `python tools/shot_overhead.py ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2` 重出 st2 俯视图（overhead.toml 已经按 26 秒写好，现在因为镜长对不上被闸门拦下）。之后 `shot_pack.py sync` s7 全场，重新编译 s7 的 prompt.txt。
2. **story.md 同步台词**（只改文字，不加新故事事实）：第 165 行 st1 那句、第 167 行 st2 那句、第 169 行 st3 那句，改成 s7_shots.json 里的新台词；story_beats 节点 38 的「说实话？值」可以跟着改成「值」。
3. **视频负面词**：s7 用 bg7 的镜头（尤其 st1、st2），视频 prompt 的负面词现在只有「画面文字」。建议在 bg7 场景卡或编译器里给这些镜头补上「可读的拉丁字母，涂鸦字母，像字母的刻痕，成行的伪文字」（bg7 卡的底图负面词里已经有前两项，只是没带进视频 prompt）。
4. **首帧提示词**：st1、st2 的 `planning/*_first_frame_prompt.txt` 如果写了「整齐的刻痕」之类，重画时按 s7_frames.json 的改图说明来，并在「不要」里加「像字母的刻痕、成行的伪文字」。
5. I21 的其余部分（bible §9 和 dossier 的维苏威说法、bg1 场景行的「葡萄藤」、p4 刮板卡）不在本场，交给对应的会话或主会话处理。

## 需要用户定
- I30 门闩：Riley 一个人住大车店，要不要加「摸门边发现没有闩」这一拍和「…and no lock」这句台词（会改 st4、st6 和故事点清单）。本轮没改。
