# 变更日志 · hy3（荒野生活 · 草崖第一夜）

## 初次生成 — 2026-09-12 · 阶段 1–6 一次跑完
Source: user_input/raw_prompt.md
Task: `hy3-20260912-092619`（审计在 `.audit/adhoc_agents/2026-09-12/hy3-20260912-092619/`）
Mode: **autonomous**（用户指定细节自决，不问多选题）

Research（本轮新增，在系列提案的三轮之外）:
- 5 组搜索 / 22 条样本：`hillside dugout turf roof` · `clay fireplace chimney` · `sod roof` ·
  `wild root + clay oven` · `cut-and-cover collapse support`
- **决定性读数：Primitive Technology `Chimney and pots` 35.1M（6 分钟、无人声）** —— 烟囱这个原理
  可以完全靠画面讲清楚，且形态与本片完全对齐。Old School Bushcraft 12.2M · Wargeh 9.7M ·
  BUSHCRAFT GR 8.1M 佐证「有烟囱的壁炉」是被反复拍的具体卖点。
- 草皮挑檐量级中等（TA Outdoors 3.3M、冰岛/维京草皮屋 0.14–1.4M）→ **它是构造特征，不是钩子**。
  分工：烟囱当钩子，草皮顶当识别形象。

Created:
- ai_videos/huangye_shenghuo/hy3/README.md
- 1_立项/concept.md
- 2_世界观人设/{world.md, style_guide.md, relationships.md, casting.md}
- 2_世界观人设/characters/{c1_砌炉的老人, c2_獾}/*.md（c1 含人物灵魂 12 维 + 立绘/turntable prompt）
- 2_世界观人设/props/{p1_长柄铁锹, p2_随身装备, p3_抹泥板与黏土壁炉, p4_草皮门与挑檐}/*.md
- 2_世界观人设/scenes/caoya/bg1..bg14/*.md（14 主体 / 14 视图）
- 3_大纲/outline.md · 4_剧本/script.md
- 5_6_分镜与prompt/{shotlist.md, shots/shot01..shot14/*.md, all_shot_prompts.md, publish.md}
- tools/gen_scene_prompts_hy3.py · tools/gen_shots_hy3.py

QC（阶段末关卡，全部通过）:
- **时长闸**：14 镜 × 18–27s，合计 **327s** ∈ [300, 340] ✔（起 68 / 承 137 / 转 101 / 合 21）
- **prompt 字数闸**（CLAUDE.md 5000 硬顶 / K10）：逐镜计数，**max 3315** ✔
- **接缝闸**（CLAUDE.md TOP PRIORITY / K31 / shot_seam）：13 个接缝**全部强档**
  （≥2.0 或 ≤0.5）且两端机位标签互不相同 ✔
- **光源措辞闸**（rule 16.9 / K32 / prompt_light）：**无 blocker** ✔
  （过程中被闸门拦下一次：共用风格串点名了「暖橙」→ 已改为只说抽象色温对比，光源全部交给每镜 `光线:`）
- **锁定描述符 byte-identical**（K8/K18）：C1 / C2 / P1 / P2 / P3 / STOVE / CHIMNEY / ROOF /
  DOOR / WINDOW **十条全部逐字一致** ✔
  （过程中查出 7 条真实漂移：生成器与卡的措辞不同 → **以卡为准**把生成器的串同步成逐字一致）
- `tools/check_locked_descriptors.py` **不适用**本系列（它只认 wushen 的 rule-10 表格式卡，
  本系列用 fenced 块；hy1 / hy2 同样不适用）→ 已用等价的自查脚本替代并记录在此

Pending（阶段 7 不在本期范围）:
- 全部参考图未出（14 场景 + 2 人物 + 6 道具 = 22 张）；**先出 `bg1-1` 过验收，其余全部挂它**
- Seedance 人物 entity 未建（本片新建，不复用 hy1 / hy2）
- 渲染与剪辑（阶段 7）本期不做

## QC 复验 — 2026-09-13 · `ai_videos__格式契约`
范围：hy3 全 14 shot（K1–K32）+ 2 人物卡 + 4 道具卡 + relationships（K16b / K28 / K8b）。
**复验结果：blocker 0 / warning 0。**

本轮查出并当场修的 4 个 blocker:
1. **K16b** —— c1 的 turntable 是四视图**静态图**，不是 rule 12.5 的 **4s 建立视频块**。
   已改为 4s / 5-phase（0-1 / 1-1.5 / 1.5-2.5 / 2.5-3 / 3-4）/ 抽帧 front 0.5 · side 2.0 · back 3.5 的 mp4，
   并按本系列惯例注明「**无统一声样台词**（divergence #3：本项目无台词无配音）」，补 `妆容:` 字段（K8b）。
2. **K28 ③** —— `relationships.md` 缺「本剧当前主题 / 人物 × 主题 / 关系对」三块。已补；
   主题定为**「一门手艺，在一个什么都没有的地方还成不成立」**，并把四个角色/物与主题的关系逐条写死。
3. **K32 C1** —— 共用风格串点名了具体光源「暖橙」。已改为只说抽象色温对比，光源全部交给每镜 `光线:`。
4. **K8 / K18** —— 生成器与卡的锁定串有 **7 条措辞漂移**。已**以卡为准**同步
   （P1 / P2 / P3 / STOVE / CHIMNEY / ROOF / DOOR），并把「小方口」拆成独立的 `WINDOW` 串，
   现 10 条全部 byte-identical。

顺带修的两处 **skill 自身问题**（反馈→进化机制）:
- `ai_videos__格式契约` K10 标题写「5000 硬顶」，修法栏却仍写「trim 到 ≤2000」（K16b / K29 同）→ 已改为 5000。
- **K19 与 K26 ⑤ 互相矛盾**：K19 要求 `渲染样式:` 带【全程绝对无字幕…】directive，
  K26 ⑤ 又把它列为该删的 body meta。已在 skill 里**显式裁定以 K19 为准**
  （hy1 / hy2 / hy3 三部一致），K26 ⑤ 只管跨镜承接类 meta。

## Follow-up 001 — 2026-09-13 · 世界重构（场地是系列第一卖点）
Source: user_input/follow_ups/202609.md - section 001
Trigger: 用户「hy 系列最吸引人的地方就是场地，环境要原始、自然而且要美；hy3 的第一张图欠缺点意思」

Root cause（自评，已写进系列圣经 §2b 作为反面教训）:
1. **「一个地形」不等于「一个地方」** —— 初版 bg1 是「一道三米高、坡度四十度的覆草土坡」，
   人站前面头顶就到一半，**没有尺度压迫**；hy1 有九十米红杉、hy2 有四米根盘，它什么都没有。
2. **为了技术纪律牺牲了美** —— 为「地面几乎没有锐利投影」定了灰白无方向散射光，
   但那条纪律来自雨林与红杉（本就在树冠与海雾下）。**草原没有树冠，草原本来就该有斜光。**
3. **为了逻辑自洽牺牲了题材** —— 「没有树所以必须横掘」推理没错，但把画面里可看的东西全拿掉了。

New world:
**一片无人的高草草原，被早已干涸的古河道切出一道垂直的黄土断崖。**
崖高七米、近乎垂直、横贯出画、**崖线一路消失在雾里看不到尽头**；崖面满是竖向干缩裂纹、
被**日出后一小时的低斜侧光**打出一道道细长的影；三层土一目了然；**中段有成群的崖燕废弃旧洞**
（画面里唯一的居住痕迹，而它不是人的）；崖沿倒垂半米长的干草根帘、逆光透亮；
崖顶是**齐人高的银白针茅草海，穗子被侧后光整片照透**。**暖金 × 冷蓝双色系。**

三处结构性升级（换世界顺手换来的）:
- **对抗者更硬**：从「腐殖层掉土屑」→ **黄土沿竖向干缩裂纹整块剥落**（黄土真实的失效模式）。
  而他 shot03 抬头盯那道裂纹四秒、**把下锹位置挪到裂纹外侧两步**、立支撑时**中柱正对裂纹下端** ——
  「他是老手」的证明从「按了一下土」升级成一条完整的因果链。
- **原理的高差变成实的**：烟道穿过**五米厚黄土**直通崖顶，**屋在崖面下、烟囱在崖顶草里**；
  `bg3` 一张图就把这五米高差摆在同一画面里。
- **伪装变成天然的**：屋顶改**向外挑八十厘米的草皮挑檐**，**檐上的草与崖顶倒垂的草根帘连成一片**；
  远景里整面崖只剩一个黑点和一缕烟，中间隔着五米土。

Changed:
- tools/gen_scene_prompts_hy3.py — 14 主体全部重写（世界 / 状态链 / 负向 / 验收）；world slug `caopo` → `caoya`
- tools/gen_shots_hy3.py — 常量段（锁定串 ×5 + 结构件 ×7 + 负向 + BG_REF）与 14 镜文案全部搬到新世界；
  **另补齐 rule 16.10 的 `镜内状态:` 逐段账本 11 镜**（hy2 shot05 实测过的坑：近景挖好了、切远景又从头挖），
  LEDGER_TODO 因此清零
- 2_世界观人设/{world.md, style_guide.md, relationships.md} — world 与 style_guide 重写（光从「灰白散射」
  改为「低斜侧光 + 暖金/冷蓝」，并**删掉负向里的 `地面锐利投影` / `直射阳光斑`**——崖面的裂纹影子是要的）
- props/p3、p4 三条结构件锁定串重写；`p4_草皮门与屋顶` → `p4_草皮门与挑檐`，`p4-2` 改名挑檐层次
- 1_立项/concept.md · 3_大纲/outline.md · 4_剧本/script.md · README.md · publish.md — 全部同步
- _series/series_bible.md — **新增 §2b「场地：系列的第一卖点」**（跨片规则 + 本次的三条反面教训）；
  §6 四格表 hy3 列与痕迹表同步；§3 标题按 2026-09-12 决定改为「每部可换」
- proposal.md — hy3 在四张表里的行同步

QC（重构后全部重跑，全绿）:
- 时长 327s ∈ [300,340] ✔ · prompt max **3693** ≤ 5000 ✔
- 13 个接缝**全部强档**且两端机位不同 ✔
- `prompt_light`（K32 光源措辞）**无 blocker** ✔
- `shot_logic`（K33 / rule 16.10 逐段账本）**blocker 0** ✔
- 锁定描述符 **10 条全部 byte-identical**（C1/C2/P1/P2/P3/STOVE/CHIMNEY/ROOF/DOOR/WINDOW）✔
- 机检 K3/K9/K10/K11/K15/K21/K22/K26/K27/K31 + 参考图路径存在性：**blocker 0** ✔

Note: 本次重构**零浪费** —— 22 张参考图一张都还没出，所以改世界不产生任何与既有渲染对不上的 diff。

## Follow-up 002 — 2026-09-13 · 抽帧报错（工具侧，hy3 内容未改）
Source: user_input/follow_ups/202609.md - section 002
Summary: 人物视频抽帧 extraction failed 是 webapp 回归，非 hy3 产物问题；修在 webapp 侧。

Not changed: hy3 的任何 md / 生成器 / prompt（本次只动 webapp 代码）

Produced (由修好的功能生成，media 走 R2、git 不跟踪):
- 2_世界观人设/characters/c1_砌炉的老人/views/c1_砌炉的老人_front.png（0.5s）
- …_side.png（2.0s）· …_back.png（3.5s）· …_audio.mp3 · …_trim2s.mp4

Cross-ref: specs/development/ai_video_management/ follow-up 167 + changelog
