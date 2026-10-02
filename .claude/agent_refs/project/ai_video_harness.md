# AI 短剧 harness 条款全文（原 CLAUDE.md，2026-09-26 瘦身时逐字迁出）

> **2026-09-28 起本文件只作沿革、不再是开工必读**：条文已逐条并入现行规范 `ai_video.md`（每条一行 + 机检指针）；冲突以 `ai_video.md` 为准。


> **ai_video 任务开工前必读**，与 `ai_video.md` 同级（CLAUDE.md § AI video rules 只留一行一条的索引）。
> 本文件是**原文照搬**：条文的增删改照旧按 CLAUDE.md「Update protocol」surgical 进行，改在这里，
> CLAUDE.md 的索引行只在硬约束本身变了时才同步。迁出理由：CLAUDE.md 每轮整份进上下文，
> 7 万字里有 3.5 万是只在 ai_video 任务里用得到的条文（shengji_zhilu follow-up 032 时间复盘）。

## § AI video rules（原 CLAUDE.md 同名节）

Detailed output rules live in `.claude/agent_refs/project/ai_video.md` per § Stage playbooks and reference docs. This section captures only the harness contract that other parts of `CLAUDE.md` reference.

- **Series nesting (2026-09-09).** A drama is `ai_videos/{name}/` by default, but several dramas that form a series live under one series folder: **`ai_videos/{series}/{episode}/`**. A directory directly under `ai_videos/` is a **series iff it contains `series.json`** (`{name_zh, slug, episode_prefix, …}`) — that marker is the single explicit rule; episode membership stays derived from the filesystem, never listed in the manifest. Shared cross-episode material goes in `ai_videos/{series}/_series/` (a `_`-prefixed dir is never an episode). Episode folders are `{prefix}{N}` (`hy1`, `hy2`) — the topic changes, the number does not; the Chinese title lives in each episode's `README.md`. Specs land at `specs/ai_video/{episode}/`; generators are `tools/gen_shots_{episode}.py` / `tools/gen_scene_prompts_{episode}.py`. Cross-episode invariants (the recurring person, sound doctrine, signature closer, production specs) live once in `_series/series_bible.md`; each episode's `concept.md` writes only what is specific to it. **Webapp side:** the drama root is 2 or 3 segments and is resolved in exactly one place — `projects/ai_video_management/libs/common/drama_ref.py`; the tree marks drama nodes with `is_drama` and series folders with `type: "series"`, and **no consumer may re-derive the drama root from path depth**. **Series-shared characters live only in `_series/` (2026-09-15).** A character (or prop / scene) reused across episodes has exactly one folder, under `ai_videos/{series}/_series/{characters,props,scenes}/`; an episode folder never holds a same-key or same-name copy. `DownloadsImporter` routes an episode's import into `_series/` too, and leaves in Downloads (error `series_key_conflict`) any file whose destination key is owned by both sides. So episode-local asset keys start above the series range (characters from `c21`), and a view that belongs to one episode only (a period costume) hangs on the series card under a series-unique key `c{N}-{episode number}{view}` (sk1 → `c1-11`, `c1-12`). An asset shared by two episodes that has no `_series/` home yet may keep the rule 4b-B `.link.json` pointer; once it moves into `_series/`, delete the episode's pointer folder, or the importer sees two owners of one key.
- One folder per project at `ai_videos/{task_name}/` (or `ai_videos/{series}/{episode}/`). `task_name` is **pinyin or English**, never Chinese (e.g. `chongsheng_zhi_zongcai_furen`). The Chinese title lives in `ai_videos/{name}/README.md`.
- **Drama folder (`task_name`) + structural files stay English/pinyin** (task_id stability + cross-project template reuse): `shotlist.md` / `world.md` / `style_guide.md` / `arc_outline.md` / `script.md` / `dialogue.md` / `shotNN.md` / `episodes/epNN/` / `shots/shotNN/` etc. **All file content is Chinese.**
- **`scenes/` may nest the world's own hierarchy (2026-09-22, shengji_zhilu follow-up 006):** `scenes/{大陆}/{区}/bg{N}_{主体}/`. The subject-dir test is unchanged (`bg{N}_` + same-name md); hierarchy dirs are index-only (same-name md + `ref/` map links) and every consumer finds subjects **by that test, recursively, never by depth**. bg numbers come from `scenes/registry.toml` only. Details: `ai_video.md` rule 4e 2026-09-22 amendment.
- **Asset sub-folders MAY be Chinese (per follow-up 2026-06-19).** Character folders (`characters/c{N}_裴知秋`), scene folders (`scenes/集市长街`), and scene-plate folders (`bg{N}_街角_摊位`) — plus their main sidecar `.md` + generated `.png/.mp4` named after the folder — use Chinese names so the left-nav reads natively in Chinese AND the download-import routing key (prompt first line) is Chinese end-to-end. `DownloadsImporter` routes on Chinese tokens fine (scene-name token + 方位/机位 token); verified. Drama folder still pinyin. (This relaxes the earlier "all paths English/pinyin" rule.)
- Two sub-types, distinguished at stage-2 interview: `novel` (multi-episode, layout under `episodes/epNN/`) and `short` (single-piece, flat layout). Sub-type is captured in `qa.md` metadata and reasserted in stage-4 spec.
- Every shot is **3–30 s, duration set per plot beat (≤ 30 s ceiling — raised from 15 s on 2026-09-06 when the generator's clip limit became 30 s)**. Author picks the duration the dramatic beat actually needs — fast reaction cuts at 3–6 s, expository / hook / monologue beats stretching toward 15 s, and only hero one-take sequences (e.g. a full sword-form 单镜) using the 15–30 s band — instead of padding short scenes to fill the Seedance budget. No "fill the full budget" pressure; no divergence note needed for any specific duration in the range. Anything longer than 30 s is two shots with a continuity token. **Shot lengths are free to change while shots are being worked on (2026-09-06): there is no episode timeline / timecode slot acting as a constraint on a single shot, a `timecode` / `成片用段` field is informational only, and a mismatch with an older slot is never a pending item. Assembly into the finished cut is decided only after the user is satisfied with every shot.** **Avoid 4–6 s fragment shots (2026-09-07): when a shot lands in 4–6 s, first ask whether it can merge with its neighbour into one continuous take** — the generator produces each shot's ambient audio / music as one unified bed, so a 12 s continuous shot carries one bed while two 6 s shots force the editor to splice two unrelated ones. Merge as a real continuous camera move (tilt down into a close-up, push in to macro, pull back to a two-shot, cut to handheld follow), never as an internal hard cut inside one prompt. If the neighbours genuinely cannot merge (different location, different build state, different time), add a real beat to reach ≥ 7 s instead of leaving it at 4 s. This targets *fragmentation*, not *pace* — genuine 3–5 s reaction cuts and montage beats are unaffected. A project may write the floor into its generator (`MIN_D`). **Amended 2026-09-08 (hy1/002): a cut *inside* one generated clip is fine** — the model holds picture and music consistent across a 20 s+ shot — so the merge unit is **one location + one state = one shot** (landing 20–27 s), not "whatever a continuous camera move can cover". Cap the upside: a bad beat anywhere in a 27 s shot costs the whole re-render, so stay under the 30 s render ceiling and put hero beats (emotional peak, signature/cover frame) at the *end* of their shot. Write the internal structure into a `分镜:` line (per-segment start/end seconds + `连续运镜`/`切`), and state that cuts carry no transition effects and do not break the shot's single continuous timeline, ambience, or light.
- Every shot ships with a **Seedance** prompt. Default aspect ratio 9:16. （2026-09-17：Kling 整条退出本仓库——工具、双 prompt 契约、10 s 切分口径一并删除；出片只走 Seedance。）
- **Dialogue (`台词`) is a first-class shot field**, carried in the prompt body as a `台词:` block per `.claude/agent_refs/project/ai_video.md` rule 12.4 「台词契约（v2）」. The shot prompt MUST NOT contain any subtitle (`字幕`) detail — no font/size/position/color/「内嵌硬字幕」/「后期软字幕」/styling; subtitles are added by the user in post. The `台词:` field carries only: speaker + line, a `正常台词` / `内心独白` type label, and the on-screen lip directive — `内心独白` (inner-monologue / OS) means the mouth does NOT move. (The earlier 字幕 三选一 contract — 内嵌硬字幕 / 后期软字幕 / 默剧 — is abolished.)
- **Canonical shot template + 台词配音 (TTS) layer (rule 12.4-H, 2026-06-14):** the earlier "visuals-only / no TTS" carve-out is **retired**. Every speaking shot additionally carries a `## 台词配音 prompt` block (`角色 / 音色(锁定 voice_id) / 情绪 / 语速 / 类型 / 台词 / 时长目标`); the same character reuses ONE `voice_id` across the whole drama. Audio is decoupled: the video carries no auto-TTS; `tools/mux_av.py` muxes video MP4 + 台词 MP3 + BGM into the finished cut. **内心独白(OS) is a speaking shot, NOT 默剧**: it MUST carry a `## 台词配音 prompt` (locked voice_id) and the finished cut MUST mux the OS line in (mux copies the video stream + writes a new audio track, so the locked voice overwrites any Seedance-baked audio) — an OS deliverable is never shipped silent. The mouth-still lip contract for OS is unchanged (no lip movement; the voice is画外 narration). 2026-06-22. The canonical `shotNN.md` = YAML envelope → 小说原文/Chapter excerpt → H1 → `## Shot context` → `## 视频 prompt` (single block: 参考/角色+面部辨识特征/情节/场景/镜头/走位/动作/台词/光线/节奏/渲染样式/比例/时长) → `## 台词配音 prompt`. The `## 起始帧` / `## 结束帧` static-frame blocks are **abolished** (no longer emitted or required).
- **【TOP PRIORITY】相邻镜之间默认走「一眼可辨的硬切 + 景别跳档」，承接首帧是例外（2026-09-09 用户定调）。** 目标是**把成片拼接的剪辑工作降到零**：切口明显时两条 clip 首尾相接即成立，切口含糊时只能靠出片端接缝抹平/补帧/色彩对齐去善后。**排镜阶段的第一约束**——定完景别后先逐对算 `人占画高` 比值（**上镜落幅 ÷ 下镜起幅**）：✅ ≥2.0 或 ≤0.5／⚠️ 1.5–2.0 且同时换 plate 或机位方位 ≥45°／❌ <1.5 且两者皆无。每镜 `## Shot context` 必写 `景别档: {起幅景别}{人占画高} → {落幅景别}{人占画高}`，与 previz `subj_frac` 同量对账。**运动方向差不能代替景别差**；一对镜要么明显切、要么无缝接，**不存在「半接不接」**。判定归 `ai_videos__运镜` M3，机检归 `ai_videos__格式契约` K31，数值量尺见 `.claude/agent_refs/project/ai_video_jingbie.md` §2.0。本条在冲突时**优先于**下一条的承接机制。**2026-09-12 三条补充（`ai_video.md` 16.5–16.7）**：① `人占画高` 只量人、不量画框，**两端同机位同取景时比值会虚高成合格**（一端人走出画即可），所以 `景别档:` 还要记两端的**机位标签**，**上镜落幅与下镜起幅的机位标签相同即 ❌，不看比值**——共用固定机位的对比帧设计只能落在镜内或隔着别的镜，不能落在接缝两端；② **切口是排镜的第一约束、时长第二**，做不出切口时应当**合并**相邻两镜（镜内切镜）或**拆出一个紧取景当开场**，时长 **4–30s 之间都合法**、「不要太短」是偏好不是闸门；③ 审计要**左移进生成器**（每镜带 `jb=` / `jbcam=`，build 时逐对算，不合格直接 raise、分镜根本生成不出来），不要留给出片前的 reviewer。
- **Cross-shot first-frame handoff (跨镜首帧承接, ai_video.md 2026-06-21):** every shot's `## Shot context` carries a `衔接:` line — `承接 shot{NN} 末帧（首帧＝上一镜末帧）` for visually-continuous adjacent shots, else `硬切（独立首帧）` (the default; each episode's first shot is always 硬切). For a 承接 shot, the next shot's **first frame = the previous shot's rendered last frame** (user extracts it and uploads it to the model's first-frame slot — never a freshly-generated still), and the `参考:` line gets a leading `本镜首帧(上一镜末帧)=>` handle + a Reference-uploads entry. Only continuous pairs (same scene/bg, continuous-or-graded camera, unbroken action) chain frames; cuts (越轴/正反打/景别跳切/换场/时间跳/回忆进出) stay 硬切. **尾帧锁定 (handoff-source side):** a shot whose last frame feeds a downstream 承接 shot (its 交接源) carries a `尾帧锁定:` line — on **regeneration** it must pin its last frame to its saved `shot{NN}_lastframe.png` via the model's 尾帧/end-frame slot, so regenerating one shot does NOT force re-rendering the whole downstream chain (first generation is free). Decision is made by `ai_videos__运镜` (M8); landing is mechanically checked by `ai_videos__格式契约` (K26).
- Image-first character consistency: each named character gets a Seedream ref-image prompt + a locked Chinese descriptor; the descriptor is re-pasted byte-identically in every shot prompt that names the character.
- **Asset prompt heads + cross-episode reuse (`ai_video.md` rule 4b-A / 4b-B, 2026-09-12).** 1. Every fenced block in a `characters/` or `props/` card that is meant to be pasted into an image model **must start with its routing key** (`p1-1_砍刀锚点`, `c2-1_…`, `p3-1_…`) — the download-import button matches on the prompt's leading characters, so a key anywhere but the front means the generated file never lands in its folder. Locked descriptors and negative lists are NOT prompts: put them in a bare fence / the prompt's own `负面词:` line, never in a block that looks copy-pasteable. 2. An asset reused from an earlier episode is **never copied and never symlinked** — copies drift (rule 4i 1) and symlinks are skipped by every reader as a traversal guard. Record it as a tracked `{filename}.link.json` (`{target, note}`) sitting where the asset would have lived; the tree renders it as a leaf whose `path` is the **target**, so preview and `/api/media` work unchanged, and `is_link` tells the UI to mark it. Reuse cards carry no image prompt at all. Helper: `libs/common/asset_link.py`.
- **物理与状态连续性三条（`ai_video.md` rule 16，2026-09-07）。** 生成模型每镜从零重演，不写死就一定漂：
  ① **掉落物必须写「真实重力」**——断枝/叶/木片/泥块/水珠一律「加速下坠、越落越快、落地即停并溅起」，
  负向配 `慢动作 / 落体滞空 / 羽毛般缓降 / 掉落物匀速下落`；只写「落下」＝把速度交给模型，它一定选慢放。
  ② **随身负重装备（背包等）只属于移动镜**——进入作业状态前必须在某一镜里**镜内卸下**（这同时是
  「他开始干活了」的叙事信号），此后每一劳作镜写「不在身上」+ 负向 `干活时背着背包`。
  ③ **人造结构件（绳结/捆绑/榫卯/补丁）一旦成型就锁成 byte-identical 串**（圈数/绕向/结头位置/余头长度/
  留下的痕迹），凡该节点入画的镜原样复现；成型之前的镜要**反向声明「此时尚未捆绑」**。
  实测失败模式：扎完绳子，下一镜绳结莫名消失。三条都应做成生成器字段，不靠作者每镜手写。
  **16.8／16.9 两条补充（2026-09-12）**：④ **描述「历史痕迹」不能用「正在发生」的说法**——
  「烧得发红的石头」本意是多年前的烧痕，模型一律按**当前状态**画成冒火星的红热石头（汉语没有过去时，
  而状态才有画面）。痕迹要写成名词化的冷材质（「暗红褐色烧斑与细裂纹」）＋ 正面写死当前状态
  （「早已冷透，不发光不发烫不冒烟」）＋ 让动作作证（「他**徒手**拨开」）＋ 负向挂反面词。
  同理：积水的坑 ≠ 正在下雨、烧黑的锅底 ≠ 锅在火上。⑤ **风格串里描述「某个具体光源」的措辞必须按镜条件化**——
  `渲染样式:` 是全镜共用串，`冷白灰环境与暖橙火光强色温对比` 这种只属于夜里有火那几镜的设定
  一旦写死进去，白天挖土的镜也在被要求画暖橙火光（hy2 污染 6 镜、hy1 8 镜）。
  拆成 `STYLE_BASE` ＋ 条件分句，没有该光源的镜还要**反向声明**并挂灭火负向组。
  一般化：**任何全片共用串写进去前先问「这句对每一镜都成立吗」**，不成立的就不属于共用串。
- **资产建立（object 与 scene）走「图先行」标准流程**（`ai_video.md` rule 4d / 4e / 4f，
  可执行顺序见 `ai_videos__stage2_世界观人设` playbook §3b）。六条铁律：
  ① **图先行、3D 在后**——锚点图纯文字自由生成、零参考图；**绝不拿 blockout / 白模 / 灰模
  渲图当出图参考**（会把质量上限锁死在方盒子水平；此坑在 object 与 scene 上各踩过一次）。
  ② **一个世界只有一张自由生成图**，其余地点锚点挂它继承世界基调。
  ③ **一个目录 ＝ 一个主体**：`bg{N}_{主体名}/` 内一份 md 装该主体全部视图的 prompt +
  该主体全部图；**状态变体（日→夜 / 完好→废墟）是另一个主体、另一个目录**。
  ④ **必做只有锚点**；反向 / 侧向 / 材质等派生视图默认不做——**方向由 previz 给，
  不由参考图给**，等实拍真漂了再补。
  ⑤ **锚点 prompt ≥1500 字**（硬顶 2000），分层写满且零重复。
  ⑥ **`.blend` 是图的下游**，住 `scenes/{name}/_blender/`，只为 previz 服务；
  该目录只放 `blender_build.md`（给 Claude 的建模指令）+ Claude 建出的 `.blend` 及校验产物。
- **环境（城/镇/村）走「几何在 3D、长相在主体」**（`ai_video.md` rule 4g）。
  面向多镜头共用同一地点、含长镜头穿行的项目，六条要点：
  ① **object 与 environment 是两类**——有界刚体走 4d 的 image-to-3D；
  **环境永远不用 image-to-3D**（生成式给不出直角、统一地平面与重复开间节奏）。
  ② **生成构件，不生成建筑**：有机繁复的小件（窗/斗拱/瓦当/桥栏）走生成，
  平直重复的（墙/屋顶/街面/桥拱）走脚本；先定模数，构件按模数出。
  ③ **一致性来自「只有一份几何」，不来自模型的记忆**——全项目一份 `{world}.blend`，
  所有镜头 previz 从它渲。场景主体给的是**风格一致**，不是**几何一致**。
  ④ **几何精度按镜头接近度分级**（贴身而过=真立面 / 中景=体块+屋顶形制 /
  远景=纯体块 / 看不到=不建）；**镜头先于几何**，先画长镜头路径再定精度。
  ⑤ **ID 色索引必须正反向成对声明**（"标记色非服装、不得入画"），否则会被渲成戏服；
  人物上 ID 色、建筑保持灰模（分界＝形状由谁提供）。
  ⑥ **一镜内主体数 ≤ 8**——这是**分镜阶段**的硬约束，超了就拆镜。
- **分层出片：每一镜先出镜头平面图（overhead），用户点头后才做 shot blend（`ai_video.md` rule 4j 2026-09-25 修订，全仓所有剧）。**
  四层各管各的、越往下改一次越贵：① **场景层**（scene blend + 场地平面图 floor plan，静态的地方）→
  ② **镜头平面图 overhead**（每镜一张俯视图：机位路线与视角、每个人的走位与时刻、建筑与本镜物件在哪；
  **不管动作细节与形状**，改一次秒级）→ ③ **shot blend**（真实动作、走位细节、物件形状、镜头远近变化，渲 previz MP4）→
  ④ **Seedance**（色彩、表情、特效、质感）。**位置只写一次**：每镜 `planning/overhead.toml` 是唯一出处，挂在该场景
  floor plan 的坐标系上、引用其块 id；shot blend 的 `previz_config.toml` 从它读位置，不重填坐标。
  `python tools/shot_overhead.py --all <ep 目录>` 出全集的 `shotNN_overhead.png` + `overheads.md` 索引，
  闸门在画图前拦：入画人物与 prompt `角色:` 双向一致、时刻落在镜长内、机位扎进实心体块、按景别与焦距反算的机位距离对不上。
  **previz MP4 只给复杂镜（2026-09-25 同日再修）**：overhead 每镜必有，shot blend / previz 不是——
  `shot_overhead.previz_triggers` 量化判据（机位连续移动 > 12 m / 镜内硬切 ≥ 4 段 / 同时 ≥ 3 人在走 / ≥ 2 对肢体接触 / 人与怪攻防接触 / 有护人格挡 `[[guard]]`）
  任一成立才做，`[meta] previz` 可推翻但须写 `previz_why`。简单镜把**专为模型画的** `shotNN_overhead_ref.png`
  （16:9、裁到本镜、无标题侧栏坐标图例、人物颜色按卡号固定）直接挂进 `参考:`，图例写进 `参考用法:`，不带 `## previz prompt` 块。
  **名字统一叫 overhead（镜头平面图）**——影视工业里画机位、运镜与演员走位的俯视图就叫 overhead；
  floor plan 留给场地本身，flight plan 是航空用语（下一条的航线 / 走位两分法由本条取代；旧剧已出的图不回溯改名）。
  **每个 `shotNN.md` 带齐三层的做法**：overhead 图挂在 `## Shot context`、Seedance 在 `## 视频 prompt`、
  文件末尾再加一段 **`## previz prompt`**（由生成器从 `overhead.toml` + `动作:` 拼出的 shot blend 生成指令：`[全局]` 键值、
  换算好的 Blender 坐标、按硬切分段的机位、角色色块与路点、道具、姿态词表、验收）。它必须在末尾，
  因为闸门把第一个 ```text 块当 Seedance prompt。
- **机位在世界里走动的镜，先出航线图给用户过目，再建 previz（`ai_video.md` rule 4j，2026-09-20）。**
  *（适用范围与命名已由上一条取代；空中航线的生成器与闸门细则仍有效。）*
  `python tools/shot_plan.py <shot 目录>` 从 `previz_config.toml` 的 `[[机位]]` + 世界地理坐标表
  出 `shots/shotNN/planning/{shotNN_flightplan.png, shotNN_route.md}`（河/墙 + 建筑组方块 + 红线航线 +
  方向箭头 + 航点 + 高度剖面），约一秒；建筑组方块写在 `planning/blocks.toml`（含 **bg 归属键**）。
  **命名按镜头类型分（2026-09-21）**：机位在世界里飞的叫**航线图 flight plan**（`_flightplan.png`），
  地面镜的机位与人物走位叫**走位平面图 ground plan**（`--kind ground` → `_groundplan.png`），
  统称「镜头平面图」；`floor plan` 一词退役——它在影视工业里指室内 / 场地平面图，
  用来称呼一条一公里多的空中航线是错的（旧剧已出的 `*_floorplan.png` 不回溯改名）。
  **顺序是硬的：图 → 用户点头 → 才渲 previz**——`镜头:` 是散文、previz 是几百个关键帧，
  两者都无法让人一眼看出「从哪飞到哪、途经什么、离那条河多远」，而错一条航线要重渲整条成片。
  图上三个必对项：① **航线与它声称跟随的地物**（`route.md` 的 `离{河}中线` 一列；实测事故 sk1 shot01
  ——prompt 写「贴着汴河飞」，实际只有穿门洞那一瞬离河 2 m，其余 96–318 m、夹角最大 61°，
  于是几何权威的 previz 与 prompt 文字互相矛盾）② **途经建筑组有没有主体卡**（标「无专属 bg」的
  反复入画就该回阶段 2 补卡）③ **方向箭头**（一条线两头都说得通）。
  **航线本身要有生成器，不许手改逐帧关键帧（2026-09-21）**：sk1 走 `tools/gen_route_sk1.py`——
  航点表写「沿河第几米、偏哪一岸几米、这一点多快、多高」，逐帧机位由它算（弦长参数化样条
  + 速度剖面积分 + 等距低通），**闸门不过就不写盘**（侧向 ≤1 g、切向、速度区间、门洞净空、
  贴河段的离河距离与航向差、视线偏航向、交接帧逐值相等、实测走廊）。
  理由：那 751 行关键帧原本是一次性脚本算完就删的，于是「改航线」等于手改 751 行——没人会改，
  矛盾就一直留着。**时刻由速度积分得出、不由作者写死**：按 (时刻, 弧长) 配时间，
  两个航点之间差半秒就能挤出 9 m/s 或 100 m/s，而逐帧二阶差分会把这种「时间上的抖」
  读成侧向加速度，闸门于是拦下一条几何上明明很平缓的航线。
  ④ **入画覆盖表**：`--coverage` 逐帧算视锥，列出每个世界坐标条目的入画秒数与最近距离，
  并标出**哪些反复入画却没有主体卡**——`bg_anchors.toml` 的 `[[todo]]` 由它生成，不靠目测。
  ⑤ **航线要按 blend 里的真几何验，不能只按坐标表**：Place 局部几何与全城坐标表并不重合
  （实测 sk1 门内北岸贴着水边就是沿城客店排），「沿中线飞」在图上完全合理、在几何里直接穿墙；
  实测出来的可飞走廊写回生成器的 `corridor` 闸门，别只留在某一次的报错里。
  世界一级的覆盖用 `--city`：读 `scenes/{world}/bg_anchors.toml`（**只声明挂在坐标表的哪一条，
  不写坐标**）出全城 bg 分布图；没有点位的主体写进 `[[unplaced]]` 并把原因印在图上，
  **把「漏标」与「本来就没有点位」分开**。
- **每个场景 bg 主体配一份 3D（2026-09-21 用户定调）**：`scenes/{world}/bg{N}_*/` 下要么有
  `bg{N}_set.blend`（**含多于一个 object** 的体块集：地面 / 墙 / 屋 / 树 / 水 /
  船 / 塔各自成件；2026-09-25 起不再导出 `_set.glb`，见下文「GLB 只装单个物体」），要么有 `bg{N}_set.link.json` 指向已有的几何（全城俯瞰这类主体的三维
  就是全城 blend 本身，复制一份只会漂）。sk1 的生成器是 `tools/build_bg_sets_sk1.py`
  （`--check` 不开 Blender 就能核对齐不齐）。**它是给 previz 摆机位、判遮挡与纵深用的三维速记，
  不是出图参考**——rule 4d ① 仍然成立：绝不拿白模渲图当出图参考。改体块 ＝ 改生成器的表重跑。
- **3D 层的工程契约**（`ai_video.md` rule 4h）。六条：
  ① ~~每镜必配 previz，覆盖率 100%~~ → **overhead 覆盖率 100%，previz 只给复杂镜**（2026-09-25，见上文「分层出片」）；
  动作时刻表简单镜由 overhead 路点秒数 + `动作:` 时间轴承担。两层 blend 分工见 rule 4g §J
  （场景层只出 `.blend` + 校验 PNG 不渲 mp4；只有 shot previz 出 mp4）。
  ② **`previz_config.toml` 是 3D 层唯一真相**——坐标/尺寸/机位数值只写 TOML，
  prompt 不复述；**关键帧 `t` 与 shot md `动作:` 时间轴逐拍对齐**，改一处必同步另一处。
  ③ **A/B 档一律走通用引擎 `tools/previz/build_previz.py`，禁止拷进 shot 目录改**；
  S 档 hero 长镜可写 per-shot Python，但必须 import 共享 rig 库、且
  **命名 `shot{NN}_previz.py`，绝不与引擎重名**（同名会让合法产物看起来像 fork）。
  ④ **场景 `.blend` 由 `tools/build_{world}.py` 确定性生成，不手改**——blend 走 R2、
  被 gitignore，手改过的 blend 没有可审阅的来源；改几何 ＝ 改脚本重跑；
  一次性补丁脚本随 builder 落地即删。
  ⑤ **几何覆盖范围按「镜头要拍到什么」定，不按「到原点多远」定**；
  走廊 keep-out 是整块剔除，**小体量塞得进走廊之间，大体量只会被整块剔掉**。
  ⑥ **previz 批量任务不许重叠跑**——`TaskStop` 杀 shell 不杀已 spawn 的 `blender.exe`，
  重叠会报假失败；blend 定稿后再跑 previz。
- **Hyper3D / Rodin 已接入**（`ai_video.md` rule 4h §G）。开关 `blendermcp_use_hyper3d`
  是 **per-scene** 的（换 .blend 要重开，这是误判「没装好」的头号来源），
  key 在 addon preferences；自检走 `mcp__blender__get_hyper3d_status`。
  用它的判据仍是 rule 4g §B 四问——**有界的有机小件（器物/构件/法宝/随身道具）用；
  环境永不用；整身着装人物也不用**（2026-09-05 实测：立绘喂进去塌成一团光滑坨，
  见 rule 4h §G1。人物 proxy 走参数化人体骨架 + 现成布料衣物网格）。
  **出了模型必须先渲一眼再往下做**，别拿没看过的网格去绑定/做 previz。
  无论哪家 vendor，白模一律过 `tools/whitemodel_normalize.py` 同一道闸门。
- **每个场景主体都要有一份 3D 产物**（`ai_video.md` rule 4h-K，2026-09-21 用户定调）。
  `scenes/` 下每个 `bg{N}_{主体名}/` 出 `.blend`（放 `_blender/`）。
  （2026-09-25 修订：原「单个网格说得完的出 `.glb`」作废——场景从来不是单个物体，见下条。）
  理由：主体卡 + 锚点图只锁**长相**，锁不住**几何**；rule 4g ③「一致性来自只有一份几何」
  由此从「一个世界一份 blend」收紧到「一个场景主体一份 3D 产物」。
  建法不新增流程：`planning/blocks.toml` 是几何唯一出处，
  **通用引擎 `tools/build_scene.py <scene 目录>` 确定性生成、不拷脚本、不手改**；
  未登记的 `kind` 与布局违规（扎进山脊 / 块压块 / 坐在河道上）**在生成时 raise**。
  场景层只出 `.blend` + 校验 PNG，**不渲 mp4**。
- **GLB 只装单个物体；场景 blend ＝ 场景图 + prompt + 单物体 GLB 的汇总**（`ai_video.md` rule 4h-K
  2026-09-25 修订，用户定调）。四条：
  ① **一个 GLB ＝ 一个物体**（一栋建筑 / 一件器物 / 一张桌子）。块里有几样东西就是几件物件，
  由 `blocks.toml` 的 `parts` 让 `build_scene` 摆在一起——组合是 Blender 的活，**绝不导出场景级 GLB**。
  物件名读起来是几样东西（「长木桌与长凳」「木箱木桶堆」「…群」）`gen_bg_assets check` 直接拦下，
  确是一件的写 `single = "理由"`。
  ② **物件只住本剧 `props/p{N}_{名}/`**（卡 + asset.toml + ref/ + 三视图 + `mesh/p{N}.glb`），剧情物件与场景物件
  共用一套编号，唯一出处 `props/registry.toml`，新物件用 `tools/props_lib.py new` 领号、不许手填；
  **场景只引用、不自带资产库**（区里只留 `_plan/` 布局规划）；同一件东西全剧只一份（形制与状态都相同才合并）。
  ③ **每个场景都要出图**：bg 锚点图与各方位 plate 图，`tools/gen_bg_images.py` 按依赖分层出
  （世界锚点 → bg 锚点挂它 → plate 挂所属 bg），画幅跟成片走；**另挂这张图自己机位视锥里、没被房子挡住的
  最多 3 件物件的正面图**（没有机位的图不挂——「全 bg 最大的前 3 件」实测把书架贴到院外、把窝棚贴进矿道），
  让场景图里的物件与它的 GLB 长得一样；挂了参考图就固定加一句「不照搬参考图构图」；引擎按下一条分工。
  **出图 prompt 里不写「相机 / 摄影机 / 镜头架」**，写「视点在…」——模型会画出一台三脚架相机（W13 机检）。
  **也不点名禁物**：即梦没有负向通道，「没有钟楼」「不是提灯」「门上没有门扇」会把钟楼 / 提灯 / 门扇画出来——正面写实际有什么。
  ④ **没有场景图不建 blend**（图先行、3D 在后）：`build_scene` 把 plate 图挂成同名机位相机的背景图对账，
  场景卡 / plate 卡 / 物件卡的 prompt 进 blend 文本块，物件三视图立在场地外作参考。
  机检：W11（bg 目录里有 GLB、或 props 里 GLB 不在 `p{N}_*/mesh/p{N}.glb`）与 Z4（区里还有 `_assets/`）即 blocker，W12 缺场景图 warning。
- **出图引擎分工（`ai_video.md` rule 4l，2026-09-25 用户定调）**：**第一张锚点**（世界锚点、bg 锚点、角色立绘、复杂物件的第一张）先走 **ElevenLabs**——贵但复杂图出得好；**挂了锚点的派生图**（plate、角色 / 物件的侧背视图与状态变体）和**简单单物件**先走 **即梦 CLI**——便宜，有参考图或主体简单时够用。首选失败再退另一家；超即梦 1600 字的只能走 ElevenLabs。唯一出处 `tools/image_engine.py`，出图工具默认 `--engine auto` 读它。
- **每个 bg 必备一份场地平面图（floor plan），它是 previz 与出片的上游**
  （`ai_video.md` rule 4k，2026-09-22 用户定调）。链条：
  **floor plan（场地层）→ overhead 镜头平面图（shot 层，rule 4j）→ shot blend / previz MP4 → Seedance**。
  图上**圆牌 1、2、3、4 只用来看图**；可引用的键是每块的 **`id`**（`b01`…）——
  圆牌按面积降序生成，**改一块尺寸就会重排**，引它会静默指到别的建筑上。
  **一份图挂在一个坐标系上，不是挂在一个目录上**：每个 `bg{N}_*` 必须能**解析**到恰好一份图，
  但不必自己拥有；不拥有的写三行 `planning/plan.toml` 指过去。
  **状态变体共用一份图**（`[meta] states` + 每块 `state_in`），**天气与时辰从不构成 state**。
  新增必填只有三个：`id` / `h_m`（航线图唯一算不出来的数）/ `scale_src`（推定的在图上挂 ⚠）。
  **零个 block 合法**——全仓一大半 bg 是没有建筑的自然场景。
  **「必备」靠消费者跑不起来咬人**（`build_scene` / previz / `shot_plan` 解析不到就拒绝运行），
  不靠全仓盘点，于是新活被挡住、旧剧一个都不扫。
  schema 只有一份：`tools/previz/planschema.py`（不 import bpy，图与 blend 共用）。
  **平面图/航线图/校验渲图一张都不许进 `参考:` 行**——它抵达 Seedance 的路径是 previz MP4 + prose 字段
  （唯一例外：免 previz 镜的 `shotNN_overhead_ref.png`，它是专为模型画的，见上文「分层出片」）。
- **产物一致性纪律**（`ai_video.md` rule 4i）。三条：
  ① **一份东西只有一个出处，副本必漂**——多份同构 prompt 走生成器
  （`tools/gen_scene_prompts.py`），改 prompt ＝ 改生成器重跑；索引/流程文件只写指针不抄内容。
  ② **冲突判定三问，顺序不能颠倒**：先问「这两个东西是不是同一个东西」（伪冲突），
  再问「谁错」（判据＝剧情需求 + 交叉印证，不是「谁更新」也不是「默认听图」），
  最后给改动挂证据。**在伪冲突上做取舍，两边都不对。**
  ③ **「文档记载的现状」不是现状**——每份「照此开工」的指令文档须以自查对账一节开场。
- **装备是第四类资产（`ai_video.md` rule 4m，2026-09-25 用户定调）**：`2_世界观人设/equipment/[{C}_{分类}/]{C}{S}_{槽位}/e{C}{S}{NN}_{品质}_{名}/`，
  **键是层级码**（每层目录带号、子层号以父层号开头：`e5103` ＝ `5_近战武器/51_主手/` 第 03 件；2026-09-26），路由键 `{键}-{M}`，编号唯一出处 `equipment/registry.toml`。**人物卡只管人**（身体 + 便服底层），兵器、盾、甲胄、披风、护腕
  一律是装备卡；谁在哪一段穿什么只写在 `equipment/loadouts/{人物卡目录}.toml`，空槽的反向声明由它自动生成。
  槽位、品质档与可选的分类层每剧自配（`equipment.toml`；魔兽剧按护甲四类 + 武器两类分）；**灰白绿不发光，蓝档及以上必须有特效光且光色＝品质色**（机检，2026-09-26）、做工逐档递进；物品原名不进 prompt。
  出图与 props 一样是正 / 侧 / 背三张；**引擎逐件定：蓝档及以上的武器走 ElevenLabs（贵，省着用），其余走即梦 CLI**（`equipment.toml [meta]`，`Config.engine_for`）。
  工具 `tools/equipment_lib.py` / `tools/gen_equipment.py`（卡是生成物）。
- **参考图资产的命名与路由（全仓统一）**：主体目录 `bg{N}_{主体名}`（`{N}` 全剧唯一），
  主体 md `{目录名}.md`（**它同时是「这是主体目录」的判据**），
  **路由键 `bg{N}-{M}`**，prompt 首行 ＝ 落盘文件名 stem ＝ `bg{N}-{M}_{视图名}`。
  键必须**纯 ASCII+数字、在首位、极短**——出图工具按 prompt 前几个字命名下载并截断，
  `bg1-2_广场反向` 截成 `bg1-2_广场` 仍带着 `bg1-2`，**匹配不依赖中文部分**。
  `参考:` 行写**与盘上逐字一致的完整路径**；可机检：全部 handle ⊆ 全部产物路径。
- **`参考:` 行只用裸 `=>@` 占位，绝不代填槽位号（全仓统一，2026-09-06）。** 每个上传项写成
  `` `{项名}(类型)=>@` ``，**`@` 后留空**——那是用户上传时手填的占位；Claude 只写项名。
  `=>@1` / `=>@图1` / `=>@第一张图` 一律不合格。**槽位语义完全由项名自身承载**，不需要编号：
  `本镜首帧(上一镜末帧)=>@` ＝ 首帧、`本镜末帧=>@` ＝ 尾帧、`{角色}=>@` ＝ 锁该角色、
  `{bg}=>@` ＝ 场景、`{角色}声音=>@` ＝ 该角色音色源。项名已经说清楚了，再挂一个序号
  只是多一处会和实际上传顺序对不上的地方。**旧的独立 `参考分配:` 行同步废除**（它的职责
  就是把 @图N 映射回角色/场景/首尾帧，没有编号就没有存在意义），其语义叮嘱移进 `参考用法:`。
  这条同时消解了仓库内一处长期冲突——场景/物件主体 prompt（`ai_video.md` rule 4d §B / 4e）
  一直用裸 `=>@` 并明写「绝不代填槽位号」，而 2026-06-28 起的 shot prompt 却要求 inline
  `=>@N`，同一个 `参考:` 行在两条管线里写法相反。**现统一为裸 `=>@`。**
  细则见 `ai_video.md` rule 12.4-C；机检归 `ai_videos__格式契约` K27。
  **角色挂 Seedance 资产包 entity（2026-09-25）**：一个 entity 同时锁长相与声音，入画的角色只挂
  `{卡目录名}(Seedance 角色 entity·长相与声音)=>@`、不再另挂人物图与声样；说话但不入画的挂同一个 entity 并注明
  `只用声音，不入画`（rule 23 修订）。
- **规则变更默认只对「新增与改动的产物」生效，不回溯已完成的旧剧（2026-09-06 用户定调）。**
  本文件与 `agent_refs/` 的输出规则会持续演进（仓库里已有大量 amendment）。每次改规则时：
  **新建的剧、以及旧剧里这次真的动到的那个 shot / 主体，按新规则走；其余旧产物保持原样，
  不做全仓回溯。** 理由——旧剧的 prompt 多半已经出过图、成过片，机械 sweep 会制造一堆
  与既有渲染对不上的 diff，收益却接近零。
  **对审查类 skill 的直接约束**：`ai_videos__格式契约` 等机检 skill **只在被显式指定的范围内**
  报违规（某个 shot / 某集 / 某个新剧），**不得因为一条新规则就把旧剧全量判为 blocker**。
  确实需要统一旧剧时，由用户显式发起，作为一次独立的迁移任务。
- **仙侠通用桥段库 `ai_videos/_research/xianxia/plots/`（2026-09-22 用户定调）。** 跨剧复用的**情节元件**：
  诗文比试、比武、拍卖会捡漏这一类小情节，**不含具体人物 / 场景 / 世界观**，只有功能位、节拍表、
  爽点落点、可替换变量，写新剧时当点缀填进去。**只做仙侠**（含古装 / 武侠 / 玄幻近亲题材），
  与同目录 `parts/x*.md` 的仙侠 canon 调研互补——canon 管**这个世界是什么样**，本库管**演什么**。
  一条 entry ＝ 一个 `.md`，**四样缺一不算建好**：功能位（谁在场，只写作用不写人）· 节拍表（每拍带
  秒数 + 观众预期 + 这拍改变了什么）· 爽点落点（爽的是哪一下、靠前面哪一拍憋出来）· 可替换变量。
  **动作点**：阶段 3 写 `arc_outline.md` 时翻本库，选中的注明 `桥段: plot_NNNN`；落到具体剧的产物
  （功能位换成真人、变量填死）属于该剧，**不回写本库**。
  **「哪条受欢迎」只能从 entry 末尾 `## 用例与反馈` 表派生**，不许写热度分数；别人的市场观察记
  `## 出处`，与自有数据分开——发布数据尚未回流之前，本库只回答「有哪些元件可用」。
- Per-episode (or per-short) `publish.md` with platform metadata is part of the stage-6 contract. **它是每部片唯一的「四站发布页」**（2026-09-12）：固定七节——母版与通用设置 / 封面帧 / **YouTube** / **TikTok** / **抖音** / **小红书** / 平台对照表 + 发布前检查清单；**YouTube 与 TikTok 一律英文，抖音与小红书一律中文**，四份文案各自独立创作而非互译；每块可复制内容单独进 ```text 围栏（标题/描述/标签各一块），每节附该站字段上限与完整 metadata（类别·语言·儿童内容·合集·许可·封面帧·画幅时长）。细则见 `.claude/agent_refs/project/ai_video.md` rule 16。
- **Render-side 台词烧录 — 全流程默认关闭（follow-up 2026-06-20「所有 shot prompt 都不要烧字幕」）:** 默认**不烧任何字幕**，pipeline **不生成** per-shot `subtitles.md`；字幕统一由用户后期自行添加。webapp 烧字幕功能（`subtitles.md` → `_subtitled.mp4`）代码保留，仅作用户手动 opt-in，**不属默认产物、不参与格式契约校验、缺失不报错**。详见 `.claude/agent_refs/project/ai_video.md` rule 11c。
- README required and in Chinese, updated alongside any feature change.
- **Media bytes live in Cloudflare R2, not git; `ai_videos/assets.json` is the tracked index.** Video / image / audio / PDF under `ai_videos/` stays gitignored. `tools/assets_sync.py` (`status` / `push` / `pull` / `prune`) keeps a mirror copy in an S3-compatible bucket and rewrites the manifest — `path -> {sha256, size}`, sorted, so it diffs and reverts like any other tracked file. **The object key IS the path under `ai_videos/`**, so the bucket mirrors the drama tree — top level is the drama name / shared library, below it the semantic structure (`characters/c1_裴知秋/`, `episodes/ep01/shots/shot01/`) — and browses in the R2 dashboard the way it browses on disk (Chinese keys verified working). sha256 is recorded only to detect change: a file that merely moved is a server-side `CopyObject`, costing no upload bandwidth. Never Git LFS: LFS retains every superseded render forever, which is the opposite of what a re-render-heavy workflow needs. Git remains the sole source of truth for what git tracks — `assets_sync` skips tracked files rather than duplicating them, and never syncs `_deleted/` or `previz/frames/`. Credentials come only from a gitignored root `.env` (see `tools/assets/README.md`); they never enter the manifest. On a fresh clone: `git pull`, then `python tools/assets_sync.py install-hooks`, then `python tools/assets_sync.py pull`. **Ordering is directional — bytes first, index second: `assets_sync.py push` → commit `assets.json` → `git push`.** Pushing the manifest ahead of its objects hands every puller an index pointing at objects that do not exist. This is automated, not remembered — `python tools/assets_sync.py install-hooks` installs five hooks per clone (`.git/hooks/` is not versioned; the tracked templates live in `tools/assets/hooks/`): **`pre-commit`** uploads new/changed media and `git add`s the refreshed `assets.json` into that same commit — the only hook point where bytes and index can enter one commit, which is why the upload happens at commit time, not push time (it warns instead of failing when R2 is unreachable, so being offline never blocks a commit); **`pre-push`** is the backstop — if media still missed the manifest it uploads it and then refuses the push, because the index it just rewrote is in no commit yet (`--no-verify` to override); **`post-merge` / `post-rewrite` / `post-checkout`** download whatever media the incoming index names, covering merge, `--rebase`, and branch-switch pulls alike. Opt out per-invocation with `ASSETS_SYNC_AUTO_PUSH=0` / `ASSETS_SYNC_AUTO_PULL=0`. `push` is resumable: it lists the bucket first and skips objects already there at the same size, and checkpoints the manifest every 25 files, so an interrupted 7 GB upload resumes instead of restarting. **The manifest describes the project, not the machine** — an entry whose local file is absent may have been deleted or may simply never have been pulled, and the two are indistinguishable, so `push` KEEPS such entries by default rather than erasing another machine's media from the index; `push --prune-missing` is the explicit way to drop them. `prune` deletes objects the CURRENT manifest does not reference, which can strand an older commit's manifest — only prune when old versions' media is expendable.
- Cross-cutting output rules and the full layout spec live in `.claude/agent_refs/project/ai_video.md`. Per-project deviations live in `specs/ai_video/{name}/` with a divergence note.

## § 生成时自检（原 CLAUDE.md § General coding rules 里的五条 AI 视频 self-check）

- **AI-video prompt length self-check (default, no reminder needed).** Whenever you generate OR modify any AI-video `## 视频 prompt` (or any other `ai_videos/` ```text prompt body), before finishing you MUST count the whole ```text block and confirm it is **≤ 5000 中文字符 (HARD, no exception, 情节 included; raised from 2000 on 2026-09-06 — the generator's prompt limit is now 5000)** per `.claude/agent_refs/project/ai_video.md` (全局 5000 硬顶) / 格式契约 K10. There is no soft/hard split and no `情节:` exemption. If over, trim on the spot (collapse 负面词 redundancy to the ~22-item standard set; drop locked descriptors re-pasted in `角色识别 / 参考图:` that already live byte-identical in `角色:`; cut 走位/动作/光线 padding — density via de-duplication, not word-stacking) until ≤5000, then finish. Do NOT rely on the downstream K10 validator to catch it — this is a generation-time gate. The same applies when a worker generates prompts: instruct it to self-verify ≤5000 and report the count.
- **AI-video 台词白话 self-check (default, no reminder needed).** Whenever you generate OR modify ANY AI-video 台词 (a `script.md` / `dialogue.md` 对白·旁白·OS line, or a shot `台词:` block), before finishing you MUST **朗读 every line in your head and confirm it is 大白话 / 真人口语** — NO 公文腔·唱礼腔·文言·书面词·对仗格言·翻译腔·念稿感. 反面典型（禁止出现）：「众家新苗按序上前、按手灵石定档，不得喧哗」「除尔族籍」「尔等速速退下」「此乃天赐良机」. This is the `ai_videos__白话大师` B1–B7 / `ai_videos__台词大师` D1 标准 applied **at GENERATION time** — a 书面 line must NEVER be emitted in the first place, not left for a downstream 台词/白话 review to catch. Fix on the spot (换口语词、拆短句、去对仗、按声口说人话) before finishing. 宗师 / 皇室 / 司仪 等角色可带**少量** register 词作声口（如「老夫」「根骨」），但**不得堆砌文言或公文唱礼腔**——一句话先过「这是真人会这么说的吗」。This gate exists because 书面台词 recurred across many episodes despite repeated reminders; generation-time self-check is the fix.
- **AI-video 光源与热态措辞 self-check（default, no reminder needed）.** 每当你生成或修改任何 AI-video 的 `## 视频 prompt`，**在收尾前必须逐镜问两句**（`ai_video.md` 16.8 / 16.9，格式契约 K32）：① **「这一镜画面里真的有这个光源吗？」**——`渲染样式:` 这类**全镜共用串**最容易被塞进只属于部分镜的光线设定（实测：`冷白灰环境与暖橙火光强色温对比` 被写死进全 12 镜，于是白天挖土的镜也在被要求画暖橙火光）。共用串只放**对每一镜都成立**的内容（影像质感/颗粒/滤镜/字幕禁令）；光源、天气、时段、建造状态一律拆成条件分句，**没有该光源的镜还要反向声明**（「本镜画面里没有任何火、也没有任何暖色光源」）并挂对应负向组。② **「这个词写的是痕迹，还是正在发生？」**——汉语没有过去时，`烧红的石头`／`烧焦的木头`／`积水的坑` 会被一律画成**当前状态**（真的在发红冒火星）。痕迹要写成**名词化的冷材质**（暗红褐色烧斑与细裂纹）＋**正面写死当前状态**（早已冷透多年，不发光不发烫不冒烟）＋**让人物动作作证**（他**徒手**拨开——徒手能碰就是凉的）＋**负向挂反面词**。这两条都是**生成时**的闸门，不要留给下游 K32 去抓。**已有可执行实现**：`python tools/prompt_light.py <范围>` 巡检，生成器里 `prompt_light.gate(emitted, legacy={...})` 做构建闸门——`legacy` 是已出过渲染、暂不改的镜的**显式清单，只减不增**，新镜一犯就终止生成。
- **AI-video 镜内自洽 self-check（default, no reminder needed）.** 任何带**镜内切镜**的 shot，收尾前必须再问两句（`ai_video.md` 16.10–16.12，格式契约 K33，可执行：`python tools/shot_logic.py`）：① **「这一镜的每一段，被造的东西分别是什么样？」**——prompt 通常写满了「他在做什么」，却没写「此刻它是什么样」；视频模型逐时刻渲染，不写死状态，状态就会漂，一次镜内切镜就是一次重新构图（实测：近景里通道已挖好，切到远景又在从头挖）。写法是 `分镜:` 之外再出一行 **`镜内状态:`，段数与 `分镜:` 一一对应**、声明后一段必须包含前一段已完成的全部。**补账本会逼你过一遍时间线，脚本自身的矛盾往往就在这时暴露**。② **「这一段里有没有「手在做一件事、身体在做另一件事」？」**——同段内的探入（伸进/塞进/掏）与位移（起身/退开/走开）会被叠在同一时刻，于是人已走开、手还留在洞里。必须拆成先后（先收手 → 然后才起身），重复动作写「每次都退出来」，并写明**身体与开口的几何关系**（相距约一臂、肩到手是完整连线），否则模型按构图需要拉长手臂。
- **Narrative-edit coherence check (default, no reminder needed).** Whenever you edit a narrative/content artifact — AI-video `script.md` / `dialogue.md` / shot `台词:` or shot 剧情 (小说原文/情节/动作/走位), or any analogous story/spec prose — you MUST, before finishing, re-check continuity with the **adjacent context**: the neighboring units (previous & next shot/section) AND any **boundary** the edit touches (for a first/last shot: the previous episode's ending ↔ this episode's opening). Confirm action/posture/emotion/dialogue carry over without abruptness, repeated beats, or contradiction; a key turn that already happened in the prior unit is NOT replayed, only continued. Fix any break surgically in the smallest adjacent spot. For AI video the full procedure is `.claude/agent_refs/project/ai_video.md` § "2026-06-16 amendment — 改动剧本/台词后默认自动做连贯性 check". **For AI video, this coherence check is now one layer of the full default review: any ep/shot edit must by default run the `ai_video__review_suite` orchestrator (台词/站位朝向/运镜/动作/时长节奏/光线/整集连贯/全剧序列/机械契约 — 9 single-responsibility skills) over the affected scope before finishing — see ai_video.md § "2026-06-17 amendment — 任何 ep/shot 改动 + 出片前，默认跑 review_suite".** The adjacent/whole-sequence checks below are the suite's continuity + arc layers.
  - **Whole-work sequence review (not just pairwise-adjacent).** The adjacent/boundary check above catches local breaks but MISSES a beat that *repeats what an earlier unit already resolved* (e.g., a second break-up declaration opening EP2 after EP1 already ended on one). So whenever you finalize/regenerate an episode, touch an episode opening or ending, or are asked to review the story, ALSO read **every episode's opening + ending beats and all signature lines as one ordered sequence** (for a single-piece short: every scene's beats) and check across the whole work for: repeated beats/declarations across episode boundaries, redundant or restarting openings, contradictions, signature-line reuse, and爽点/escalation consistency. This holistic pass is a superset of the adjacent check — run it before declaring a multi-episode narrative coherent. For AI video the procedure is the same ai_video.md amendment, § 全剧序列 review.
  - **Review plot + blocking, not just lines; muting a line is not a fix.** The review covers the actual *plot and spatial blocking* (who is where, facing where, moving or not — across consecutive units), not only the dialogue text. If a line is redundant, silencing it does NOT resolve the problem when the underlying plot/blocking is still illogical (e.g., a character who already "left" in the prior unit is kept on-stage for several more units, or "walks out" twice). When you find an unreasonable beat, **fix the subsequent plot**: re-sequence that beat and every affected later unit so positions/movement stay monotonic and each action happens once — don't just edit the words.
