# hy4 changelog

## 立项 — 2026-09-13
Source: user_input/raw_prompt.md
Summary: hy4《荒野生活 · 深雪第一夜》开工，阶段 1–6 一次走完。

上游: `proposal.md` §C hy4 概念卡（深雪 · 第一夜）+ `_series/series_bible.md`。
本轮四个决定见 raw_prompt.md；与概念卡的三处偏离（片长 / 美食线镜数 / 允许携带食材）同上。

## 阶段 1–6 一次走完 — 2026-09-13
Source: user_input/raw_prompt.md

产物（约 40 个文件）:
- **阶段 1** `1_立项/concept.md` —— 13 节。§0 写明与提案概念卡的三处偏离及理由。
- **阶段 2** `2_世界观人设/` —— `world.md` · `style_guide.md` · `casting.md` ·
  `relationships.md` · 2 张人物卡（c1 含 rule 12.11 的十二维人物灵魂）· 5 张道具卡 ·
  **12 个场景主体**（由 `tools/gen_scene_prompts_hy4.py` 生成）。
- **阶段 3** `3_大纲/outline.md` —— 18 镜骨架 + 三条线并行 + 节奏曲线 + 与前三部的差异核对。
- **阶段 4** `4_剧本/script.md` —— 无台词，每镜写**画面 / 声音 / 要害**三块 + 声音总谱。
- **阶段 5+6** `tools/gen_shots_hy4.py` → 18 镜 shotNN.md + `shotlist.md`（含切口审计表）
  + `all_shot_prompts.md`；另 `publish.md`（四站）与 `README.md`。

规格: **16:9 · 448s（7:28）· 18 镜**，单镜 20–28s。起 94 + 承 172 + 转 100 + 合 82。

三道闸门（**本片无任何 legacy 豁免，是第一部从第一行起全受约束的片子**）:
- `shot_seam.audit` —— **17/17 接缝强档**（≥2.0 或 ≤0.5），两端机位标签互不相同。
- `shot_logic.gate` —— **18/18 带 `镜内状态:` 逐段账本**，段数与 `分镜:` 一一对应。
- `prompt_light.gate` —— `渲染样式:` 零光源点名；无火的镜反向声明 + 挂 `NEG_NOFIRE`。
- K10 正向最长 **2879 字**（硬顶 5000）；K22 人声抑制全镜在位。

**顺带修好一个 checker defect（hy4 逼出来的）**:
`tools/shot_logic.py` 原先按 `；` 数段，而段落正文里本来就会出现 `；`
（hy4 实测：`镜内状态:` 写「**与上一段相同**；她停在原地…」被数成两段），
导致 9 镜误报「账本段数与分镜对不上」。
改为**按时间前缀 `N–Ms` 数段**——段落真正的标识是时间，不是分隔符。
改后 hy1–hy4 四个生成器全部通过。

美食线（本轮的重点）: 占 **shot12–15 共 100s、全片 22%**，与建造线并列。
- shot12 化雪水（**雪 → 水**，因果链起点 + 兑现「储物＝天然冰箱」）
- shot13 和面（**本片最强反差：冻红开裂的手 × 揉得光滑发亮的面团**，两样必须同框）
- shot14 醒面 + 剖鱼（**零下醒面必须靠火**，这是本片独有的物理前提；两件事并行且有因果）
- shot15 石板烤饼（**决定性瞬间：饼鼓起来**，封面候选 2，从变色到鼓成包不许切）

待用户: **出 20 张参考图**（12 场景 + 3 人物 + 5 道具），
先出 `bg1-1` 过完验收，其余挂它或它的下游；`c1-1`/`c1-2` 出完后建 Seedance 人物 entity。


## Follow-up 001 — 2026-09-13 18:10:00
Source: user_input/follow_ups/202609.md - section 001
Summary: c1 的 turntable 是静帧四视图、缺 K16b 要求的 4s 建立视频 prompt；补齐并顺带统一落盘裸键命名。

Auto-updated:
- ai_videos/huangye_shenghuo/hy4/2_世界观人设/characters/c1_凿冰的女人/c1_凿冰的女人.md —
  turntable 段整段重写为 4s 建立视频块（16:9 · 5-phase 时间轴 · 抽帧 0.5/2.0/3.5 ·
  验收五条 · 发型反向声明 · 不背包 · 手取 shot01 干净态）；立绘落盘声明改裸键
- ai_videos/huangye_shenghuo/hy4/2_世界观人设/characters/c2_雪兔/c2_雪兔.md — 落盘声明改裸键
- ai_videos/huangye_shenghuo/hy4/2_世界观人设/props/p{1..5}_*/*.md — 落盘声明改裸键
- ai_videos/huangye_shenghuo/hy4/2_世界观人设/casting.md —
  参考图清单改裸键；c1-2 一行由 `.png`/turntable 改为 `.mp4`/**4s 建立视频**
- tools/gen_shots_hy4.py — Reference-uploads 的资产路径改裸键、c1 那行改「立绘 + 4s 建立视频」
- ai_videos/huangye_shenghuo/hy4/5_6_分镜与prompt/ — 重跑生成器（18 镜 + shotlist）

Verified:
- 生成器重跑干净：18 shots / 448s / 正向 prompt 最长 2879 字（硬顶 5000）
- 两道 build-time 闸门无 legacy 豁免通过：`shot_logic.gate` · `prompt_light.gate`
- 切口审计 17/17 接缝 ✅（K31 铁律⓪）
- turntable 块自查：4s · 5-phase 段数对齐 · 抽帧点齐全 · 负向含无人声/无字幕组 ·
  ```text body 1180 字（远低于 5000）

Pending:
- **`c1-2.mp4` 与全部 8 张参考图尚未出** —— 本条只补了 prompt，图与视频待用户生成
- hy4 无 `divergence.md`（hy3 有）；16:9 与"无台词无配音"两处偏离目前只记在 concept.md §0

No conflicts found in: 1_立项/concept.md, 3_大纲/outline.md, 4_剧本/script.md, 2_世界观人设/{world,style_guide,relationships}.md

## Follow-up 002 — 2026-09-13 19:10:17
Source: user_input/follow_ups/202609.md - section 002
Summary: 实拍反馈 shot01–04：雪铲取出前没描述过所以凭空冒出、shot01 手部收尾没有结果所以接 shot02 突兀、shot02 侧身穿枝被演成撞树、bg3 雪井太小又贴地平视。

Auto-updated:
- tools/gen_shots_hy4.py —
  新增 `CARRY`（雪铲竖扣包背面、D 形握把高出包顶一拃）并写进 `BAG_NOTE`；shot01–03 加 `p1`；
  新增 `坑沿` 装备状态（shot04，原先误写「本镜内卸包」）；shot04 改「从包背面解下扣着的雪铲」、滑下将近两米；
  shot01 重排为「远景 → 手插雪顶到冰（雪太薄）→ 切回远景转身走向林墙」，落幅 0.10 远景背影；
  shot02 改为用手拨枝、身体不碰树，新增 `NEG_BUMP`；shot03 雪井尺寸与 N1 机位（坑沿外三米·一人高·俯角二十五度）；
  bg3 场景串改为六米×一米八；shot18 的「shot01 末段」改为「手部特写段」
- tools/gen_scene_prompts_hy4.py — bg3 放大（直径约六米＝五倍树干、深约一米八、远侧坑壁高过一人、树干下半截露在坑里），
  N1 抬高，验收第一条改尺寸，新增主体级 `neg`（浅坑词组）；bg8 同步 N1 与尺寸
- ai_videos/huangye_shenghuo/hy4/5_6_分镜与prompt/ — 重跑生成器（shot01–04、shot18、shotlist、all_shot_prompts 变动）
- ai_videos/huangye_shenghuo/hy4/2_世界观人设/scenes/shenxue/{bg3,bg8}_*/ — 重跑场景生成器
- ai_videos/huangye_shenghuo/hy4/4_剧本/script.md — shot01 手试雪太薄→转身、shot02 拨枝、shot03 N1 与尺寸、shot04 解下雪铲
- ai_videos/huangye_shenghuo/hy4/2_世界观人设/world.md — 雪井尺寸行
- ai_videos/huangye_shenghuo/hy4/3_大纲/outline.md、1_立项/concept.md — shot01 一句话描述
- ai_videos/huangye_shenghuo/hy4/2_世界观人设/props/p1_雪铲与雪锯/p1_雪铲与雪锯.md、casting.md — p1 镜次扩到 shot01
- .claude/agent_refs/project/ai_video.md — 新增 16.13 / 16.14 / 16.15

Verified:
- 生成器重跑干净：18 shots / 448s（时长未变）/ 正向 prompt 最长 2879 字（硬顶 5000）
- 切口审计 17/17 ✅；shot01→shot02 由 4.89 变为 **0.22**，机位 `冰湖平视远景 → 林中平视` 不同
- `shot_logic` blocker 0；`prompt_light` blocker 0（shot13/18「通红」两条 warning 为既有、与本次无关）
- 巡检：shot01–04 无「包侧抽出 / 擦过 / 蹭到 / 直径约三米」残留；撞树负向只挂 shot02
- 相邻连贯：shot01 末（转身走向林墙）→ shot02 首（走进云杉林）✓；shot02 末（朝画外走）→ shot03（转过一棵树入画）✓；
  shot03 末（包连雪铲卸在坑沿）→ shot04 首（包口微距、握把露在边缘）✓；shot18 手部特写仍对 shot01 手部段 ✓

Pending:
- **需重出图**：`bg3-1`（主）→ 挂它的 `bg4-1`、`bg8-1` → `bg11-1`（N1 对比帧必须同机位同尺寸）；`bg5-1`/`bg12-1` 只继承基调，可不重出
- **需重渲**（若已出过）：shot01–04（prompt 改了）；图重出后 shot05（bg4）、shot09（bg8）、shot17（bg11）
- 未跑完整 `ai_videos__审查总编排`，本次只做了机械闸门 + 相邻连贯人工复核

No conflicts found in: shot05–shot17 prompts, 2_世界观人设/{style_guide,relationships}.md, characters/*, props/{p2,p3,p4,p5}
