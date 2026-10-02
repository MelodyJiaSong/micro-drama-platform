# AI 短剧现行规范（ai_video.md）

> task_type=ai_video 开工唯一必读（已并入原 `ai_video_harness.md`）。只写现行规则 + 机检指针；来历、事故、反例、旧版全文在 `ai_video_history.md`，按 rule 号 / 日期 grep，不通读。
> 专题 ref 仍有效、按需读：`ai_video_jingbie.md`（景别档与切口）、`ai_video_shouweizhen.md`（跨镜首尾帧承接）、`ai_video_yunjing.md`（运镜）。
> 机检列：路径相对 `tools/`；K＝`ai_videos__格式契约` 的 K 号；szzl＝`szzl_shot_engine.py`（生成器闸门，rule 29–41 目前只有它全接）；ov＝`shot_overhead.py`；webapp＝`projects/ai_video_management/`。
> 「（本轮裁定）」＝2026-09-28 主会话裁定，清单见文末、可推翻；「（仅 xx）」＝单剧规则，别的剧复现或用户明说全局才升格。

## 0. 一集怎么走

每步 QC blocker 清零才进下一步；任何改动跑受影响范围 `ai_videos__审查总编排` + 记 `specs/ai_video/{name}/changelog.md`；每阶段先用多选题问用户（interactive 默认）。

| 步 | 产物 | 闸门 / 工具 |
|---|---|---|
| 0 史料（仅史料驱动项目） | `0_research/dossier.md` + 各资产 `refs.md` | K34；`ref_fetch.py`、`ref_aspect.py` |
| 1 立项 | `1_立项/concept.md`：题材、单集时长、比例、子类型 | 人工确认 |
| 2 人设与资产 | `2_世界观人设/`：角色卡（人物灵魂）+ `relationships.md`、立绘 + 4 s 建立视频、`voices/{voice_id}/ref.wav`；场景 `bg{N}_` 锚点；物件 `props/p{N}_`；装备 `equipment/`；技能库 `skills/`（rule 45） | `check_stage2.py`；K8 / K25 / K28 / K30；`image_engine.py`；`scene_review.py` |
| 3 大纲 | `3_大纲/arc_outline.md`：大方向 + 前几集细纲，后续集推进到时再细化 | `ai_videos__剧情连贯` + `ai_videos__全剧序列` |
| 4 剧本 | `4_剧本/episodes/epNN/{script.md, dialogue.md, goals.toml, states.toml}` | `script_tools.py check`；`beat_logic.py`；`goal_ledger.py`；台词大师 / 白话大师；逻辑因果 §2b；对白通读 + 冷眼观众（`dialogue_review.py` 指纹章） |
| 5 分镜 | `5_6_分镜与prompt/episodes/epNN/shots/shotNN/`：`planning/overhead.toml` + `shotNN_overhead_ref.png`；复杂镜才 previz（先静帧） | ov `gate` / `previz_triggers`；`previz/planschema.py`；`previz/review.py`；K31 `shot_seam.py` |
| 6 prompt | `shotNN.md`：设计稿（第一个 text 块）+ `## Seedance prompt` 精简稿 + `## 台词配音 prompt` | 生成器 build 闸门（szzl `gate` / `product_gates`）；`prompt_compact.py`；K 全表；`ai_videos__审查总编排` |
| 6.5 animatic 过审（rule 44） | `{ep}_animatic.mp4` + `viewing_animatic/review.md` | `animatic.py`；`viewing_packet.py`；`ai_videos__整集观感`；`seedance_kit open` 闸门 |
| 7 出片 | `shotNN.mp4`（即梦网页，「生成」永远人点）；tts_first 剧先出 `shotNN_tts_lip.wav` | `seedance_kit.py open`；`indextts_dub.py` |
| 7a 出片审片 | 每镜审片清单 | `render_review.py` + `ai_videos__出片审片` |
| 8 后期 | `{ep}_final.mp4` + `{ep}_final_burned.mp4` + SRT | `post/finish_ep.py`（响度回读） |
| 9 整集观感 | `viewing/review.md`（绑成片 sha256） | `viewing_packet.py` + `ai_videos__整集观感` |
| 10 发布 | 每集 `publish.md`（四站） | 人工 |
| 11 观众回路 | `audience_report.md` → 候选 follow-up（用户决定落不落） | `audience.py log / ingest` |

## 1. 目录、命名与通则

| rule | 现行 | 机检 |
|---|---|---|
| 1 | 剧目录、结构文件英文 / 拼音，内容中文；资产目录（角色 / 场景 / 道具 / plate）及同名文件可中文；中文标题写在 README。 | K12 |
| 1b | 产物零 hex（`#RRGGBB`），写自然色名；色温、尺寸照写。 | K9；`check_stage2.py` |
| 2 | 阶段编号目录 `1_立项/ … 5_6_分镜与prompt/episodes/epNN/shots/shotNN/shotNN.md`，每镜一个同名目录、禁平铺；已有旧结构剧可保留。 | K1、K24 |
| 2b | 有 `series.json` 才是系列，成员从文件系统派生、`_` 目录非成员；跨片不变量只写 `_series/series_bible.md`；共用资产只住 `_series/`（集内不留同键副本，集内角色键从 c21 起）；剧根只由 `drama_depth()` 判，禁止按路径深度推。 | webapp `libs/common/drama_ref.py`；`series_shared.py`（series_key_conflict） |
| 3 / H-6 | 子类型 novel（`episodes/epNN/`）/ short（平铺、无 world.md）：阶段 2 定、阶段 4 重申。 | 无 |
| 9 | 每剧中文 README（概要、用法、角色、风格词），随改随更。 | 无 |
| 10 | regen `scope=episode N` / `episodes M..N` 只删该集目录，默认 `scope=project`；short 只有 project。 | 无 |
| 12.8 | 角色 `characters/c{N}_{名}/c{N}_{名}.md`，N 不补零，分配后不重排、不复用、只追加。 | 无 |
| 12.9 / H-36 | 资产与 shot 各一同名目录；媒体不进 git、走 R2：`ai_videos/assets.json` 是索引，先传字节再提交索引。 | `assets_sync.py`（`install-hooks`） |
| 4e / 4f 目录即主体 | 场景主体目录 `bg{N}_{主体}/` + 同名 md（全部视图 prompt + description + 共用负面词），可嵌套 `scenes/{大陆}/{区}/`，消费者按 `bg{N}_` + 同名 md 递归识别；bg 号只来自 `scenes/registry.toml`；手写 terrain 与生成物分文件。 | `check_world_scenes_szzl.py` W1–W8；webapp `downloads__writer.py`（`_view_key`） |
| 4f 路由键 / 4b-A | 每个出图块首行首位是路由键（场景 `bg{N}-{M}`、卡内 `{key}-{N}_{视图名}`），导入取最左、落盘名只用键；锁定串用裸围栏；复用卡无出图块。 | `check_stage2.py`；`downloads__writer.py`（`_keyed_route`） |
| 4b-B | 跨片复用不复制不软链，放 `{文件名}.link.json`（target 限 `ai_videos/` 内真实文件）；系列内共用改住 `_series/`。 | 无（实现 webapp `libs/common/asset_link.py`） |
| 4d-A2 | 脚本产物目录登记 `GENERATED_DIR_NAMES`，免被导入改名。 | `downloads__writer.py` |
| 4i | 一份东西一个出处；冲突先问是不是同一个东西、再按剧情判谁错；下游不回喂上游、只许对账；指令文档开头先对账；大投入前先出片小样测。 | `plate_match.py`（对账） |
| H-31 | 规则变更不回溯旧剧：新规只管新产物与这次改到的镜；机检只在指定范围报 blocker，旧镜走显式遗留清单（只减不增）；`seedance.toml` 的 `legacy_eps` 同理。 | `prompt_light.py gate(legacy=)`；`shot_logic.py gate(opt_in=)` |
| H-37 | 单剧偏离写进 `specs/ai_video/{name}/` 的 divergence。 | 无 |
| 16.4 | 重生成覆写 md，不整树删含媒体的 `shots/`；重编号前先 push 媒体。 | `gen_shots_hy1.py`（`prune_stale_shot_dirs`） |

## 2. 资产：人物 · 场景 · 物件 · 装备

**人物**

| rule | 现行 | 机检 |
|---|---|---|
| 4 | 每个具名角色一张立绘（`c{N}-1.png` 定脸）+ 锁定描述符；入画角色挂 Seedance 资产包 entity（entity 已锁长相）。 | K8、K25 |
| 12.1 | 出现 ≥ 2 镜或开口的角色必须建卡：定位 / 锁定描述符（不写五官、含妆容；识别标签 ≤ 30 字只写可辨造型）/ 性格 / `## 人物灵魂` / 弧光 / 配音参考（voice_id 源）；多音字加 `读音锁定:`；字段以 stage2 playbook 为准。 | `check_stage2.py`（`check_card`）；K8 / K8b |
| 12.4 发声建卡 | 有台词或内心独白的角色（含一次性路人）先建卡（识别标签 + voice_id + 立绘）并登记 `casting.md`；不开口的群像可 inline。 | K30；szzl `voice_id` |
| 12.11 | 每个具名角色 `## 人物灵魂` 12 维 + `relationships.md` 人物网；ongoing、逐集深化；一切剧情创作先读透、选择对不上就改情节或补人物。 | K28 |
| 22.1 | 非东亚角色立绘首句写死人种；出图逐张验脸。 | `gen_char_images.py`（ETHNIC） |
| 22.2 | 具名人形角色建卡时一次写齐立绘 + `{目录名}_turntable` 4 s 建立视频（正→侧→背），禁占位；非人形、场景、物件不做；有台词者念统一声样句。 | `check_stage2.py`；K16 / K16b；`gen_turntable_videos.py` |
| 15 | 写两轮不出的性状 → 出细节参考图；深度写一亮一黑；永久痕迹写「此后一直在」。 | 无 |

**场景**

| rule | 现行 | 机检 |
|---|---|---|
| 4e 图先行 | 锚点纯文字零参考；自制 3D / 平面图 / 白模渲图绝不当出图参考；一世界一张自由生成图；公版史图可图生图（仅史料驱动）。 | 无 |
| 4e 视图集 | 主体与镜头无关（一套材质与光＝一个主体）；每 Place×State 必做一张锚点；plate 与派生视图按镜需要才出、不预建（本轮裁定）；航拍镜共用一张零参考俯瞰锚点。 | `plate_match.py` |
| 4f 层级 | Blender 管几何、主体管外观、Scene 卡管叙事地点；主体＝Place×State，调色调不回来即新主体；几何变体只为挡镜头建，变体外观整套换；禁为细节拆主体；一目录一主体，状态变体另立。 | 无 |
| 4f 锚点 | 锚点 prompt 1500–1600 字（即梦上限，本轮裁定），分层写；锚点级档只有锚点 prompt。 | W4；`check_stage2.py`（锚点级跳 K23） |
| 4f 精简 | 一个事实只说一次；共用串只写本地点有的；派生不重述长相；变体写 `只改:` `不改:`。 | 无 |
| 4f `参考:` | handle 与盘上路径逐字一致；写明「上传」「出图后存」。 | 无 |
| 4h-K(b) | 场景出图按依赖分层（世界锚点 → bg → plate），可挂视锥内 ≤ 3 件 prop 图；prompt 不写相机词、不点名禁物。 | `gen_bg_images.py`（CAMERA_WORDS）；W13 |
| 33 | 场景图出图后逐张过审（承重连续 / 通得到 / 不悬空 / 尺度 / 无文字 / 对得上卡），结论绑图的 sha256 写进图的 md；没审过不许挂。 | `scene_review.py gate` |
| 07-03 背景板 | 背景板只画固定结构，剧情道具归 shot；摆放合现实；主光有真实光源；同一处改 3 次仍错就换参考兜底。 | `scene_review.py`；K32 |
| 12.4 美术 / 25 | 写真实材质与纵深，默认实拍写实；不挂游戏 / CG 锚、不堆粒子光；古装写全陈设、不跨朝代，不用西式建筑；「半写实」只指世界设计，渲染拉满写实。 | `gen_scene_prompts_sk2.py`（仅 sk2） |
| 18 | 防「像动画 / 游戏 CG」：画类参考不进上传窗口（人物绝不进）；实拍写成摄影参数；做旧写污损；写光比与近黑区。 | 无 |
| 4l | 第一张锚点走 ElevenLabs；派生图、简单物件、三视图走即梦；蓝档以上武器走 ElevenLabs；auto 失败才换引擎，显式 `--engine` 不换。 | `image_engine.py`（`first_choice`）；`equipment_lib.py`（`engine_for`） |

**物件**

| rule | 现行 | 机检 |
|---|---|---|
| 4b | 跨 ≥ 2 镜且外观须一致的道具立卡 + 图，住 `props/p{N}_{名}/`（编号只出自 `props/registry.toml`）；ref 只进道具可见的镜；可见状态改变须有画内动作。 | K20 |
| 4d-A / 21 | object＝有界刚体（内部空间另立）：锚点零参考 → 正 / 侧 / 背挂锚点 → 由图生白模；锚点过验收才派生；场景先拆物件。 | `gen_object_cards.py` |
| 4d | 任何来源白模过同一闸门 + `object.toml` 探针；全过≠好白模，须看渲染；`--fit` 以代码默认为准、文档不写数值（本轮裁定）。 | `whitemodel_normalize.py` |
| 4d-B | 参考图 prompt：首行路由键 → `参考:`（锚点写「无」）→ `参考用法:`（冲突听谁）→ `视图:`（正对面 / 看不见面 / 外轮廓）；派生加 `恒定项:` `本视角要点:`；比例漂移 > 2.0 或近平面物件退同尺寸替身盒。 | `view_check.py`；`build_objects.py`（DRIFT_MAX） |
| 4d-A3 | 主体＝图集 + description；每镜 `@主体` 1–8 个，超了拆镜；状态变体另立主体。 | K27 |
| 28 | 雕像按人物类：先自出三视图再 image-to-3D，官方图不喂。 | 无 |

**装备**

| rule | 现行 | 机检 |
|---|---|---|
| 4m | 可换的穿戴与手持是装备：键即层级码（`e5103`＝`5_近战武器/51_主手/` 第 03 件），编号只出自 `equipment/registry.toml`，`item.toml` 唯一出处，谁穿什么只写 `loadouts/*.toml`；prompt 不写原名；灰白绿不发光，蓝档以上发品质色光；换装只出三面图。 | `equipment_lib.py`（`check_spec` / `wearing`）；`gen_outfit_views.py` |
| 4m-⑦⑧ | 做工串不写结构件、不点名缺席物；侧背写相对转角；比喻改写成形状；每件最多出 3 次，仍偏记 `known_issue`。 | `gen_equipment.py`（ABSOLUTE_POS / NAMED_ABSENCE） |
| 36 / 37 装备锁 | 装备锁带尺寸与「不是 X」（形近物）；扛 / 背的东西写清手或带子（`item.toml [carry]`）；拿法见 rule 41 G3。 | szzl `carry_gate` / `asset_lock` |

## 3. 3D 与平面图

| rule | 现行 | 机检 |
|---|---|---|
| 4g | 环境走脚本体块 + 构件拼装，不走 image-to-3D；生成式 3D（Hyper3D）只做有界有机小件、不做整身人物，出模先渲一眼；按镜头远近分 A 立面 / B 体块 / C 剪影 / D 不建；一镜点名主体 ≤ 8，超了拆镜。 | `build_scene.py`（KINDS） |
| 4g-G | previz 里人物与可动道具用 ID 色 + 剪影，建筑器物纯灰；prompt 写明色块只是身份标记、不入画。 | 无 |
| 4k | 每个 bg 解析到恰好一份 floor plan（天气时辰不算 state）；block 必填 `id`（引用只用 id、不用圆牌号）/ `h_m` / `src`；零 block 合法；解析不到下游拒跑；平面图 / 航线图不进 `参考:`（免 previz 镜的 overhead_ref 例外）。 | `previz/planschema.py`（`check` / `audit`）；`build_floorplan.py --check` |
| 4j overhead | 每镜先出 `planning/overhead.toml`（位置唯一出处）→ 审图 + `shotNN_overhead_ref.png`，点头后才建 blend；复杂镜（`previz_triggers`）才做 shot blend / previz 并在 md 末尾写 `## previz prompt`；简单镜 `参考:` 挂 overhead_ref。 | ov `gate` / `previz_triggers` / `previz_decision`；szzl `previz_prompt` |
| 4j 航线 | 机位在世界里飞的镜先出航线图给用户过目再建 previz；航线由生成器解析定义、不手改关键帧；闸门从相机回读，不过不写盘。 | `shot_plan.py`；`gen_route_sk1.py`、`build_bianjing.py`（`verify_camera`）（仅 sk1） |
| 4h-A | 场景 blend 只出 `.blend` + 校验 PNG，不渲 mp4、不进参考；shot previz 改拷贝副本，不写回场景源。 | ov `previz_decision` |
| 4h-K | 每个 bg 一份 `_blender/{bg}.blend`（树内无 `.glb`），由 `build_scene.py` 从 `blocks.toml` 确定性生成、不手改，没场景图即 raise；物件只住 `props/p{N}_*`，一个 GLB 一个物体。 | `build_scene.py`；`gen_bg_assets.py check`；W11 / W12 / Z4 |
| 4h-B/C | `previz_config.toml` 是 3D 唯一真相，prompt 不复述、派生数字写实值；关键帧 `t` 与 `动作:` 逐拍对齐；A/B 档走共享引擎 `previz/build_previz.py`（不拷引擎），S 档钩子叫 `shot{NN}_previz.py`。 | `build_previz.py`（SCHEMA）；webapp `previz__writer.py` |
| 4h 人体 | 人体动作用 Cascadeur（`cascadeur/choreo.py` + 共享姿势库 `cascadeur/poses.toml`）；烘焙躯干前倾与编排差 > 20° 即 blocker；人不许站进场景实体。 | `build_previz.py`（LEAN_TOL） |
| 4h 纪律 | 判几何先渲定点特写（新建相机）；白模取景按焦距÷距离对齐 `景别档`，只自动修人出画的关键帧；previz 批量不重叠跑、批渲中不改运行库；改完只停自己的 PID、重开新文件。 | `previz_frame_fix.py` |
| 30 | previz 先 `previz/review.py <config>` 出静帧（十几秒）、看过再渲整条；先查看不看得见；几何在平面图层就拦。 | `previz/review.py`；ov `visibility`；`planschema.py`（`derived`） |
| 4e 型面 | 灰模渲染强主光 + 轮廓光、AO、暗背景、Freestyle；方向由 previz / overhead 给。 | 无 |
| 24 | previz 参考视频每段 2–15 s、≥ 409600 px、24–60 fps；超 15 s 自动切段上传。 | `previz/seedance_ref.py`（LIMITS） |
| 19 | 没有俯视全城镜时只建拍得到的走廊带。 | `build_bianjing.py`（仅 sk1 实现） |
| 20 | Hyper3D 由 pipeline 直调 Rodin HTTP，key 放 `.env`。 | `hyper3d_fetch.py` |
| 27 | 射线不认 `hide_render`；异步出片记账本；检查先让它失败一次；不从单张投影判三维。 | 无 |
| 4h builder | 城市 builder 沿低空航线挖 keep-out；缩城只缩坐标，手写坐标入口校验（仅 sk1）。 | `build_bianjing.py`（`camera_keepouts`） |
| 4h-B5 | 两条 clip 拼一镜到底：缝在总里程中点、两边同速、缝后 ≥ 1.5 s 不机动、缝放画面最简单处（仅 sk1）。 | 无 |

## 4. 剧本与台词

| rule | 现行 | 机检 |
|---|---|---|
| 14 / 集长 | 单集时长由 concept 定（默认竖屏 90–180 s；横屏长集按其 concept）（本轮裁定）；溢出镜顺延下一集，不删台词不注水；名场面排 AI 强项，情感戏靠独白与节奏，正向立意；前 3 s 钩、集尾卡点。 | `script_tools.py check`（`EP_RANGE_DEFAULT`，集 `min_s / max_s` 覆盖） |
| 17 | 史料驱动：dossier 先于立项，三级史实标签，每镜 `史实:`，锚点前建 `ref/`；上传图宽高比 1:3–3:1（此句全局）（仅史料驱动）。 | K34；`ref_fetch.py`、`ref_aspect.py` |
| H-32 | 阶段 3 翻桥段库 `ai_videos/_research/xianxia/plots/`，注 `桥段: plot_NNNN`，不回写（仅仙侠近亲题材）。 | 无 |
| 12.4 白话 / H-39 | 台词一律真人口语白话，零公文腔 / 文言 / 翻译腔；写完朗读一遍。 | `script_tools.py check`（ARCHAIC）；`ai_videos__白话大师` |
| 12.4 语速 | 台词字数 ÷ 时长 ≤ 5 字/秒；超了加时长（≤ 30 s）/ 精简 / 拆镜。 | `script_tools.py`（CN_CPS_MAX、`need_of`）；szzl `gate` |
| 12.6-B | `dialogue.md` 由 `script.md` 生成，不手改。 | `script_tools.py gen_dialogue` |
| 29 听者 / 生物 | 正常台词要有听的人（画里有别人或注明「对画外 X」），自言自语改内心独白；叙事点名的生物必须挂卡（判别位分得开近亲物种），出现地点合理。 | szzl `_TO_OFFSCREEN` / `CREATURES` |
| 31 | 结果要有看得见的原因（摔倒只认外力或行动受限的伤）；写了跑平面图上就得跑；伤与破损按 severity 登记 `states.toml` 并一直写到结束；剧本阶段与出片前子代理带全集上下文逐拍通读；结果没原因先问该不该有，不往前补因。 | `beat_logic.py`；ov `physics_errors` / `jump_cuts`；`ai_videos__逻辑因果` |
| 34 | 台词、动作、情节任何一处改了，由没写过这集的子代理带全剧上下文把整集对话通读（十问：接得上 / 母语口语 / 声口 / 称呼 / 信息边界 / 不替画面解释…），改完 `--dialogue-stamp`；指纹对不上即 raise。 | `dialogue_review.py gate`；`ai_videos__对白通读` |
| 35 | 每集 `goals.toml` 目标账本：每件事屏幕上说出、接下、换地点提一句、了结看得见；冷眼观众只看 `script_tools.py screen` 的画面与台词逐镜通读，与对白通读共用指纹章（`--viewer-stamp`）。 | `goal_ledger.py check`（G1–G6）；`ai_videos__冷眼观众` |
| 39 | 学会的本事在屏幕上交代 idea（师父的道理）与 trigger（成的那一下的起因，对得上人物灵魂）；入门课再要 why 与第一次没成；不花镜头教常识，本事意义按原典。 | `goal_ledger.py` G7b |
| 40 入门课 / 施法 | 入门课要 demo / method / effect、fail ≥ 2，先后有序；施法的起手 `stance`、手 `hand`、光的走向 `flow` 只在技能卡 `[script]` 定义一处（goals.toml `[[casting]]` 写 `card` 引用，rule 45），此后每次施法剧本与 prompt 都写到三样；规矩用看得见的样子讲，不让人物数数。 | `goal_ledger.py` G7b / G7c；szzl `cast_errors` |
| 26 | IP 衍生片：只引真实文件原句；账号 / 域名不含作品名；免责三件事放片头与简介首屏；不变现（仅 IP 衍生片）。 | 无 |

## 5. 分镜与镜头

| rule | 现行 | 机检 |
|---|---|---|
| 6 / H-7 | 镜长 3–30 s 按剧情 beat，无时间码约束；4–6 s 碎镜先问能否与邻镜合并（一地一态＝一镜，20–27 s）；镜内切镜写 `分镜:`（段起止秒 + 段名 + 切入方式）；hero 拍放镜尾；`动作:` 铺满镜长。 | K11；szzl `gate`；xj `SHOT_MIN / SHOT_MAX` |
| 7 / H-8 | 默认 9:16，剧可在 concept 另定并写 divergence。 | K11 |
| 16.5–16.7 【最高优先】 | 相邻镜默认硬切 + 景别跳档：上镜落幅 ÷ 下镜起幅的人占画高 ≥ 2.0 或 ≤ 0.5，且两端机位标签不同（1.5–2.0 须同时换 plate 或机位转 ≥ 45°）；每镜写 `景别档:`；做不出切口就合并，或拆一个紧取景开场；先于时长。这是生成端的设计：成片仍可按 rule 42 剪辑的 edl 剪——零**人工**剪辑，不是零剪辑。 | `shot_seam.py`（`verdict` / `audit`）；K31；`ai_video_jingbie.md` §2.0 |
| 06-21 承接 | 跨镜首帧承接是例外，只在必须同一连续动作时用：写 `衔接:`；承接镜首帧＝上一镜成片末帧、首拍续已到状态不重演；交接源写 `尾帧锁定:`、末拍落静定 beat；首尾帧位置 / 姿态 / 景别须明显不同。 | K26；运镜 M8；`seam_tune.py`；`ai_video_shouweizhen.md` |
| 12.4 自包含 | 每镜只放本镜那段台词，跨镜对白不重叠；正文不写「承 shotNN / 下一镜」。 | K26 ③ |
| 12.4 `镜头:` | `{景别} + {运动}`，景别落五级阶梯；关键瞬间缓推近到面部；中近景及更近注明背景虚化。 | K31 |
| 12.4 `走位:` / 32 | 写每个在画人物的位置、视线对象与相对位置（单人镜也写），用画面左右 + 脸朝不朝镜头，罗盘方位只留在平面图；说话人与机位夹角背对（> 110°）即 raise（台词窗内逐点量，不只量中点——台词在窗内任一刻都可能念出，049），有意背影在剧本行尾写「背影：理由」；口型对应的说话人那一刻必须在画里、没被挡。 | ov `screen_view`；szzl `screen_clause` |
| 12.4 `动作:` | 时间轴铺满 `时长:`；每拍写每个在画人物的动作 + 微表情 + 视线对象，不干站，反应不镜像复述；配角对眼前事件有反应。 | szzl `gate` / `idle_errors` / `gaze_errors` |
| 12.4 人数 | 每条 prompt 带 `人数:`，点名画里每个具名人物与总数、别无他人。 | szzl `headcount` |
| 12.4 场景 | 每镜（含回忆 / 过场）至少挂一个场景主体并在 `场景:` 引用；回忆镜可只建单视图。 | szzl `gate` |
| 12.4-E 光线 | `光线:` 2–4 句写主光方向 / 色温、材质反光、时辰大气；眼神只写神态，不写眼睛发光。 | K13、K32 |
| 16.1–16.3 | 掉落写真实重力；背包只属于移动镜、镜内卸下；结构件成型后锁串跨镜原样贴。 | 无 |
| 16.8–16.9 / H-40 | 历史痕迹写冷材质 + 当前状态；共用渲染串不点名只属于某些镜的光源；逐镜问「这镜真有这个光源吗」「这是痕迹还是正在发生」。 | `prompt_light.py gate`；K32 |
| 16.10–16.12 / H-41 | 镜内切镜写 `镜内状态:`，进度不倒退；探入与位移拆先后写死。 | `shot_logic.py gate`；K33 |
| 16.13–16.15 | 后面要用的工具携带时就可见；锚点尺寸按最终状态倒推、宁夸张；碰环境用手。 | 无 |
| 06-21 写实 | 写实剧渲染串不用致假词（游戏 / CG / 工笔…）；古装群像束发、面孔各异；台词点名的物件画面里要有；功能角色有反应。 | 无 |
| 29 攻防 | 护人格挡写 overhead `[[guard]]`、反应写 `[[react]]`；每拍算得通距离 ÷ 速度（人 ≤ 8 m/s、四足 ≤ 14 m/s；扑咬 2 m 内 ≤ 0.8 s 不干等；反应时长来得及）；同卡多只各一条 `[[actor]]`。 | ov `guard_errors` / `physics_errors` |
| 36 身体层 | 该打中的每一下写 overhead `[[hit]]`，平面图查够得着、previz 查贴身；镜内跳切的新位置切前在画里而人不在 → 分身，raise。 | ov `hit_errors` / `ghost_errors` |
| 37 | `[[skill]].learned` 那一刻镜内要有近景 / 特写段、变化写到秒；`本镜状态` 提到兵器必须写怎么拿。 | szzl `demo_errors` / `hold_errors` |
| 38 | 切点两边同一个人不跳左右、两人先后不对调（有意跨轴写 `axis_ok`）；最后一句台词离镜尾 ≥ 0.8 s。 | szzl `axis_errors` / `gate`（TAIL_QUIET） |
| 40 持盾 / 施法 | overhead `[[actor]]` 写 `shield`（左 / 右，`shield_t` 限时段），盾那一侧正面挨打写 `open`；打斗里施法写 `[[cast]]`，威胁进 3 m 须有盾或 `[[guard]]`（故意暴露写 `exposed`）。 | ov `shield_errors` / `cast_errors`；szzl `cast_errors` |
| 41 G1 空窗 | 有人在画的时间窗至少一句有人在做事；景边走边给；纯景标「空镜」让人出画；特写 / 插入不算。 | szzl `idle_errors`；K35 |
| 41 G2 状态对时 | `镜内状态` 写「已 X」的时刻不早于 `动作` 做完 X 的时刻。 | `shot_logic.py` L3（`opt_in`，只拦新剧 / 改到的镜） |
| 41 G3 拿法 | `本镜状态` 拿 / 背装备那句逐字含装备卡 `[carry]` 的一种拿法；盾不写「挎」；同槽两件时手上拿品质高的那件（念旧写 `备注: 旧件在用：理由` 且屏幕上看得见）；需求等级超前只许 `level_waiver` 豁免。 | szzl `equip_errors`；`equipment_lib.py` |
| 41 G4 视线 | `动作` 里有人看 / 盯 / 数而他正脸朝镜头（< 60°）→ 平面图登记 `[[gaze]]`；面朝须对上目标（≤ 45°）；`key = true` 的看点整镜至少一刻入画；生成器把看点方位写进 `走位:`。 | ov `gaze_errors` / `gaze_notes`；szzl `gaze_errors` |
| 41 G5 previz 保真 | 平面图 `count = N` → previz N 个；命中用的兵器件 previz 里必须有；持物姿态 `臂盾L / 背盾 / 单手握R`、出手切 `前砸 / 前劈R`；盘上 config 与平面图重算不一致即 blocker；每个路点时刻都钉姿态；人在 ≥ 0.3 m 的 `[[object]]` 占地里，底姿态只许 `坐墩 / 站高`（坐 / 站在它顶上），否则绕开。 | szzl `previz_fidelity`（`_seat_errors`）；`build_previz.py`（命中贴身、`ON_TOP`） |
| 41 G6 外观出处 | 写游戏机制外观的共用串 / 施法串一律经 `look(text, facts)`：挂的事实须在 0_research 注册且 verified_by ∈ human / ai_read；草稿不许进串；核错的事实用 `banned` 列出写法，正文再出现即 raise。 | szzl `look()` / `refuted_errors` |
| 41 G7 打击几何 | `[[hit]].part` 与来向对得上（胸 / 脸要出手者在目标面朝 ±90° 内，背 / 后脑反之）；写了倒 / 撞 / 飞，目标此后 0.6 s 顺出招方向移动、不超 `KNOCK_MAX_M`；part 是身上道具时 previz 量那件。 | ov `strike_errors`；`build_previz` 命中 |
| 41 G8 施法因果 | 光的命中不早于同一人 `[[cast]]` 起光、弹道离己方 ≥ 0.5 m；敌人起光前 1 s 内朝施法者逼近 ≥ 1 m 即 raise；hostile 持械者在 `REACH_M` 内停 > 2 s 却无 `[[hit]]` 即 raise（`stuck` 兵器卡住算在拔；`over` 光从某人肩上方飞过）。 | ov `cast_order_errors` |
| 41 G9 道具连续 | 被拖 / 抢 / 捡 / 扔 / 卡住的道具写成会动的 `[[prop]]`（key / label / path）；同场景接连两镜同 key 的位置首尾对上（≤ 0.3 m，画外挪过写 `moved`）；人钻出 / 钻回洞写 actor `enter` / `gone`；`动作` 拿法不与 `[carry]` 打架。 | ov `prop_errors`；szzl `prop_seam_errors` / `equip_errors` |
| 41 G10 previz 回读 | `build_previz` 写 `{shot}_previz.stamp.json`（配置 / 钩子 / 编排 sha256），不符即 raise；逐关键时刻量：人物根偏平面图 > 0.3 m、该着地的那处（站＝脚、跌坐＝臀、跪＝膝，`POSE_CONTACT`）离地超限即 blocker。 | `build_previz` 自检；szzl `previz_fidelity` |
| 12.4 系统 UI | 系统交互画成在画悬浮框，框内 ≤ 3 字或符号，语义靠系统配音（仅系统流剧）。 | 无 |
| 9b | 可选：Shot context 写 `表演库参考: perf_NNNN — 用于 <角色> <beat>`，改写进 `动作:`、不照抄。 | 无 |

## 6. Seedance prompt 与出片

| rule | 现行 | 机检 |
|---|---|---|
| H-8 | 出片只走 Seedance（即梦网页 2.5，全能参考，单条 ≤ 30 s）。 | 无 |
| 5 | 每镜一个 `shotNN.md`：YAML → [小说原文，可选（本轮裁定）] → H1 → `## Shot context` → `## 视频 prompt`（设计稿，一个 text 块）→ `## Seedance prompt`（精简稿）→ `## 台词配音 prompt`（说话镜）→ [`## previz prompt`]。 | K1 / K2；两引擎 `verify` |
| 12 设计稿 | 字段序 `参考` `参考用法` `角色` [`人数`] `情节` `场景` `镜头` [`分镜` `镜内状态`] `走位` `动作` [`命中`] `台词` `光线` `节奏` `渲染样式` `比例` `时长` `负面词`；`节奏` 自由写；不写标题行、面部辨识特征；锁定串逐字相同，词表出自 `style_guide.md`；设计稿不设字数上限。 | K3、K8、K18；xj `_REQUIRED_FIELDS` |
| 12.4-P | 上传的是 `## Seedance prompt`，由设计稿生成：参考行 →【参考素材】（人物＝entity、白模颜色＝人物）→【声音】→【概述】（情节首句）→ 按整秒「镜头N｜a–b秒」分段（景别运镜 + 画面左右 + 动作 + 命中 + 画内台词 `{…}`）→【人物】本镜状态与装备形制 →【人数】→【场景与光】→【画面】渲染 / 比例 / 时长 →【声音】→【不要】。 | `prompt_compact.py`（`compact`） |
| 12.4-P 不进 | 不进 Seedance：角色锁定串、镜内状态、节奏、音乐、走位里的罗盘句、「情绪目的」注、点名具体物件的否定句；负面词只留通用短清单（画面文字 / 字幕 / 水印 / 畸形肢体 / 多余手指 / 人脸变形等），想压住的物件改成正面写实际有什么；静默镜在【声音】行写「本镜没有人说话」（本轮裁定）。 | `prompt_compact.py`（`_drop_negations`） |
| 12.4-P 上限 | 精简稿 ≤ 2000 字（官方示例 650–1400；过 1500 先考虑拆镜或把动作写概括），超限 raise，`legacy_eps` 的集只警告；压缩后回读：设计稿每个动作分句都得在精简稿里，否则 raise。 | `prompt_compact.py`（COMPACT_MAX、回读 raise）；`seedance_kit.py parse` 优先取 `## Seedance prompt` |
| 12.4-C / 23 | `参考:` 行＝全能参考上传清单：每项 `` `{项名}(类型)=>@` ``，`@` 后留空、槽位语义只靠项名；次序 previz → 首帧 → 场景 → entity → 物件；主体目录 / 路由键在首位；build 时验。 | K27；szzl `_handles`；`gen_shots_sk2.py`（`gate_refs`） |
| 4d-A3 `参考:` 位 | `参考:` 只列 previz / 主体 / 承接首帧 / overhead_ref；`角色:` 写 `@主体 — 本镜状态`。 | K27 |
| 40 entity | 只给入画的人挂 entity（含背影）；画外 / 不入画说话人不挂、不写「只用声音」，其台词后期配——从窗的第一秒起配，念的那段不许与画内台词的窗重叠，也不许他的脸那时在画里（人占画高 < 0.2 的远景不算）（049）。 | szzl `gate`（「只用声音」、画外撞车 / 嘴不动却有声 raise） |
| 12.4 槽位 | 全能参考上限按官方 2.5：图 ≤ 30、视频 ≤ 10 段合计 ≤ 30 s、音频 ≤ 10 段合计 ≤ 30 s；主体图 1–8 个、主体音视频每段 5–10 s 效果最好（本轮裁定）。 | `previz/seedance_ref.py`（LIMITS）；K27 ④ |
| 12.4 `角色:` | `角色:` ＝ 卡里一句话锁定（逐字）+ 本镜状态；背影写背面可见特征、相似背影逐一区分；生成块写具体角色名，不用关系称谓（台词除外）。 | K8；szzl `char_lock` |
| 12.4 `台词:` | 每单元 `{时间窗} {说话人}（{正常台词｜内心独白｜画外}·{口型注}）：{正文}`，正文不可删；内心独白 / 画外嘴不动、画里无人替他开口；无台词写「无」；零字幕信息。 | K4–K6、K21；szzl `_lines_field` |
| 12.4 渲染 / 11c | `渲染样式:` ≤ 10 个每镜都成立的质感词，不放分辨率词；prompt 里零字幕信息（牌匾 / 系统 UI 属画面）；字幕只在成片阶段加（rule 42）。 | K4、K19 |
| 12.4 合规 | 生成块（含 turntable）不出现影视 / 画作 / 景点 / 游戏名与真人名、真实军事地标、武器特写与暴力词；不写引号待渲染文字；弱化帝王政治词；不用真人照片作参考；暴力题材去未成年标记；被拒先分文字 / 脸图 / 字数 / 限流。 | szzl `gate`（IP_RED）；K17 |
| 44 | 剧本与分镜定稿后、第一镜出片前：`python tools/animatic.py <剧> <ep>` 拼整集 animatic（已出片的镜用成片；其余按分镜段取图：`keyframe/k{段}.png` → previz 每 1.5 s 一帧（段里的动作看得见）→ 首张场景图 → 平面图，印镜号、段、动作摘要；台词烧双语字幕）。首帧图可选。 | `animatic.py` |
| 44 审 | 再 `viewing_packet.py <剧> <ep> --video {ep}_animatic.mp4` + `ai_videos__整集观感` 审，结论 `viewing_animatic/review.md` 绑 animatic 的 sha256。 | `viewing_packet.py --check --animatic` |
| 44 闸门 | `seedance_kit open` 调 `animatic.problems()`：没 animatic、结构指纹（镜长 + 分镜段 + 台词）变了、没审或审的是旧版 → 不给开；`legacy_eps` 豁免；prompt 措辞改了不作废 animatic。 | `seedance_kit.py`（`animatic_gate`）；`animatic.py --check` |
| 12.4-K | `python tools/seedance_kit.py open <剧> <ep> <shot>`：参考文件按上传顺序编号硬链接进 `资料包/`、prompt 进剪贴板、在本剧 `seedance.toml` 的 Chrome 账号开即梦，「生成」永远人点；资料包是派生缓存（gitignored、不进 R2），生成器写完当场对齐、Stop hook 每回合 `sync --all --quiet`；主体 entity 不进包。改了 shot prompt，回复里必须告诉用户改了哪几镜、资料包是否全部一致。 | `seedance_kit.py`（`after_write` / `sync`）；`.claude/settings.json` Stop hook |
| 45 技能库 | 技能与装备一样全剧一处定义：`2_世界观人设/skills/`（`skills.toml` 职业位 / 法系颜色 / 口令政策，`registry.toml` 编号，会上屏的技能才建 `k{职业位}{NN}_{名}/skill.toml`）；原典看 w25 / w26，本剧偏离写 `liberty`。 | `skills_lib.py check` |
| 45 施放 | 镜表只写 `casts=(Cast(键, 谁, 对谁, 时刻, 档, 结局),)`：各阶段逐字锁定串、previz 手势、样片参考全由卡生成，不手写；谁何时学会只写卡 `[[learned]]`，等级读装备表等级段；卡的禁写（审判「脱锤飞出」、冲锋「撞翻」…）进产物即 raise。`动作:` 里写 `〔施法〕` 定施法分句落点，长镜里夹着别的事就用手写时刻把一次施放切开按先后插回；负向词否定了施法要出的光 / 火（圣光术镜挂「治疗光柱」）即 raise；overhead 不许 `[[hit]] with=光`；Cascadeur 体的施法手势写 choreo（053 / 056）。 | szzl `skill_errors` / `cast_chunks` / `_with_casts` / `skill_forbid_errors` |
| 45 口令 | 有读条的技能每次念卡里那一句固定短句（不念技能名，守 G1），落在蓄光那几秒；瞬发不念；战士的吼归音效（用户 2026-09-30）。口令用游戏里有官方译文的种族语言（shengji：圣光术德莱尼语 Pheta vi acahachi、火球术萨拉斯语 Felo'melorn!，事实进 w26），全剧第一次出现由剧中人说出意思；放出去的那次（成 / 挡）必念全句，被打断 / 没出来的可念半句；对白通读不按母语口语审口令（056）。 | szzl `skill_errors`；`ai_videos__对白通读` / `冷眼观众` 例外条 |
| 45 资产 | 技能样片（4–7 s、无脸无字）、峰值图、定稿音效、口令录音各做一次全剧复用；施法镜按固定文件名挂施法片段（样片按卡 `window` 剪）或峰值图（参考视频合计 ≤ 30 s，放不下只挂峰值图并写明），样片没收进来那几镜资料包建不起来；音效后期按施放时刻原样贴。 | szzl `skill_refs`；`post/finish_ep.py`（`skill_cues`） |
| 45 样片做法 | 样片＝绿幕棚里拍：卡 `[[sample.keyframe]]` 写 2–3 张只管动作的手势参考图（绿幕、低饱和、不带光效，`skill_keyframes.py` 用即梦出，后面的以第一张图生图）+ 完整视频 prompt（第一行＝`{键}_{名}_样片`，和角色 / 场景 prompt 一样以键开头，下载名才带键；场景＝绿幕，光效全靠文字写成真实分层的光）；不用 Blender / Cascadeur 白模；收片 `skills_lib.py adopt <剧> <键>`（不给路径就收 ~/Downloads 最新那条），按实测改 `peak` / `window`（用户 2026-10-01：以后都这样做）。 | `skills_lib.py check`（keyframe / window / peak） |
| 45 账本 | 每集 goals.toml `[[casting]]` 写 `card = "k201"`，起手 / 手 / 光的走向从卡 `[script]` 读，账本里再写即报错。 | `goal_ledger.py` G7c（`patterns`） |
| 12.4 webapp | 高亮 text 块行首字段名，复制仍是纯文本。 | webapp `apps/ui/src/markdown/renderer.tsx`（FIELD_LABEL_RE） |

## 7. 音频与后期

| rule | 现行 | 机检 |
|---|---|---|
| 12.4 配音块 | 说话镜带 `## 台词配音 prompt`（voice_id / 情绪 / 语速 / 类型 / 台词 / 时长目标）；一个角色全剧一个 voice_id；声样只认人物卡 `views/views.mp3`（建立视频的统一声样句＝即梦 entity 绑的同一段），无卡的画外角色才用 `voices/{voice_id}/ref.wav`。 | K7；`check_stage2.py`（`check_casting`）；`indextts_dub.py`（`find_ref`） |
| 12.4-H2 | 每部剧在 `seedance.toml` 声明 `audio_mode`：`native`＝画内正常台词用 Seedance 原生人声（entity 绑该角色声样），画外 / 内心独白后期 IndexTTS 配（`indextts_dub.py --only post` → `shotNN_tts_post.wav`），声样与 entity 绑的是同一段；`tts_first`＝先用 IndexTTS 出 `shotNN_tts_lip.wav`，作 @音频 上传让 Seedance 对口型，成片用同一文件，源音轨经 demucs 去人声留环境声。 | `post/finish_ep.py`（audio_mode 缺键 raise、该配却缺 TTS raise）；`indextts_dub.py` |
| 12.4-H2 禁止 | 禁止文字驱动口型、事后再用另一段 TTS 覆盖（两条时间轴必错位）；内心独白 / 画外嘴不动、后期配。 | `indextts_dub.py`（lip / post 两条镜长轨，同窗多句顺排） |
| 12.4-H2 音乐 | Seedance 一律不出音乐：prompt 开头与结尾各写一次「不要任何音乐」；BGM 只在后期加（`finish_ep --bgm`，共享库 `ai_videos/_bgm/`）。 | `prompt_compact.py`（NO_MUSIC） |
| 42 | `python tools/post/finish_ep.py <剧> <ep> [--grade] [--bgm X] [--proxy]`：按 `cut/edl.toml` 切段（没有就整镜顺接；旧片报错）→ 可选分组调色 → 逐事件对白配平到 −23 LUFS → 按 audio_mode 混音 → 两遍线性 loudnorm −14 LUFS / −1 dBTP（退到动态即 raise）→ 1080p lanczos 母带 + 烧字幕版 + SRT，存 `post/masters/v{NNN}/`；每步落盘可续跑，收尾 `qc.py` 从成片回读。 | `post/finish_ep.py`；`post/qc.py`（Q1–Q9） |
| 42 剪辑 | 每集 `cut/edl.toml` 是唯一剪辑出处（git 跟踪）：`/ai_videos__cut` 里 Claude 只从 `edl.py candidates` 的切点提补丁（剪头尾 / 删整段 / 闪前 ≤ 4 s），`edl.py verify` 过、代理片经用户逐条批才升版本；成片只出批准过的 edl。审稿意见按成本分流：已出片的镜剪，未出片的先改剧本再出，要新画面的开票回生成端。 | `post/edl.py`（`verify` V1–V10）；`ai_videos__cut` |
| 42 标识 | 成片与烧录版写回源片的 AIGC 隐式标识（全部 ProduceID），回读缺即 raise；发布时勾平台 AI 标识。 | `post/aigc.py`；qc Q8 |
| 42 字幕 | prompt 里零字幕；字幕只在成片阶段加：中文竖屏版默认烧录，YouTube 传 SRT。时间取实测：画内句按 `post/align.py` 强制对齐，画外句按 TTS 实际摆位；每条至少读得完（EN ≤ 20、ZH ≤ 9 字/秒，镜尾句读不完可跨切点，跨就在新镜停满 0.5 s），读不完出片前 raise；漏说 / 改词进人听清单。 | `post/subs.py`；`post/align.py`；qc Q7 |
| 42 环境 | demucs / cv2 用 index-tts 的 venv（`--python`）；demucs 没装时报出安装命令。 | `post/stems.py`（`check_demucs`） |
| 36 出片审片 | 出片落盘跑 `render_review.py` 抽逐秒拼图、命中与跳切前后特写，子代理看图判分身 / 道具变样 / 悬空 / 没打到 / 背对；不通过回对应闸门补，不直接改 prompt 碰运气；镜尾响度实测。结论 `verdict.md` 绑 take 的 sha256，成片只收「通过」的 take；片长与 md 差 > 0.5 s 的旧片不审、不进成片。 | `render_review.py`（`tail_verdict` / `verdict_ok`）；`post_common.stale_take`；`ai_videos__出片审片` |

## 8. 审查与发布

| rule | 现行 | 机检 |
|---|---|---|
| 12.4-D | 审查准则的权威定义在各审查 skill，`ai_videos__审查总编排` 按单镜 → 整集 → 全剧串跑；改动后与出片前必跑，blocker 清零。 | `ai_videos__审查总编排` |
| 06-16 复核 / H-42 | 改 script / dialogue / shot 后按落点跑审查总编排（动了集首尾加全剧层）；查相邻镜与集边界连贯，定稿或改开场结尾时通读全剧开场、结尾与签名台词；跨集重复保留前一处；剧情或走位不合理改后续情节与走位，只删台词不算修好。 | `ai_videos__审查总编排`、`ai_videos__全剧序列` |
| 43 观感 | `ai_videos__整集观感`：animatic 与整集成片各审一次（`viewing_animatic/` 与 `viewing/`），没写过这集的子代理只看观片包判想不想看下去：逐镜注意力 0–10、预计划走点、前 3 秒钩子、每 20–30 s 情绪点、标了好笑 / 好哭的镜成不成立、集尾钩、最该改的 3 处（镜号 + 秒数）；与冷眼观众（看不看得懂）分工。 | `viewing_packet.py`（`--check`） |
| 43 观众 | 发布后 `tools/audience.py log / ingest`：记发布链接；留存曲线按镜映射、评论摘录 → `audience_report.md`；候选 follow-up 由用户决定是否落。 | `audience.py` |
| 16 publish | 每集一份 `publish.md`，四站：YouTube / TikTok 英文、抖音 / 小红书中文，每块单独 text 块。 | 无 |

## 已废止

正文不再保留，查沿革：`ai_video_history.md` 按号 grep。

2（`my_novel/` 章节先行）· 4c · 4e（bg 编号按层级 / 出场顺序）· 4f（blender_build.md）· 8 · 11（seam-frame）· 12.2 · 12.3（v2 / v3 场景档、plate 当场建）· 12.4（place_holder、`=>` 写法、画外 OS 声音占位、场景单 token、字段反引号、多声轨静音 + mux、朝向 plate、Kling 双 variant、首行 `{NN}集{NN}镜视`、节奏四档枚举、K22 静默镜人声负面词、槽位 ≤ 9 图 / ≤ 3 视频）· 12.4-A（角色字段展开规则，内容并入 12.4 `角色:`）· 12.4-B · 12.4-F · 12.4-H（→ 12.4-H2）· 12.5（7 s turntable v4–v11、`c{NN}_{pinyin}`）· 12.6 · 12.6-C · 12.6-D · 12.6-E · 12.7 · 12.10 · 13（每集 cue，→ 12.4-H2）· 38（镜内配乐收尾，→ 12.4-H2）· 负面词四条（05-25 / 06-17 / 06-19 / 06-21，→ 12.4-P）· 念法三条式 · 起始帧 / 结束帧块 · Kling 全部条款 · 镜长 3–15 s · 视频 prompt 2000 / 5000 字上限（→ 12.4-P）· 走位写东南西北（→ 32）· 默认不烧字幕（→ 42）· 12.4-H 视频不带 TTS 一律 mux 覆盖（→ 12.4-H2）· 06-21 写实④禁静态硬切（→ 16.5）· 06-21 写实⑦语速 ≤ 4（→ 5 字/秒）· 23（09-25 画外说话人挂 entity，→ 40）

## 本轮裁定清单

2026-09-28 主会话裁定；不同意的直接说，按更新协议改回。

- rule 2 `my_novel/` 章节先行：已废止（只剩 feng_shou_lu 旧剧用）。
- rule 4c 物件 10 s 转盘 + 5 落点：已废止，被 4d / 4h-K 取代。
- rule 4d 白模 `--fit` 默认值：以 `whitemodel_normalize.py` 代码默认为准，文档不写数值。
- rule 4e 派生视图 vs 4h-K 各方位 plate：锚点必做；plate 与派生视图按镜需要才出（shengji 804 个 bg 只用到 8 个）。
- rule 4f 锚点 prompt 上限：1600 字（即梦实测上限）；下限 1500 不变。
- rule 5 H1 前「小说原文」段：可选。
- rule 12.4 全能参考槽位上限：按火山官方 Seedance 2.5 指南（图 ≤ 30、视频 ≤ 10 段合计 ≤ 30 s、音频 ≤ 10 段合计 ≤ 30 s）。
- rule 12.4 静默镜人声负面词（K22）：被 12.4-P 取代；静默镜在【声音】行写「本镜没有人说话」。
- rule 12.4 节奏四档枚举：已废止；节奏不进 Seedance prompt，设计稿里自由写。
- rule 12.6-D prompt 首行标识符：已废止（为 Kling 截断定的）。
- rule 12.10 场景 14 s walk-through 视频：已废止；长相靠锚点 + plate，几何靠平面图 + previz。
- rule 13 BGM cue vs rule 38 镜内配乐收尾：被 12.4-H2 取代；rule 38 只留左右不互换与台词离镜尾 ≥ 0.8 s。
- 单集时长：由 concept 定（默认竖屏 90–180 s；shengji 横屏长集按其 concept）；BLUEPRINT 的 90–120 s 是默认值不是硬约束。
- rule 4k-G、rule 12.5-A：未裁，见下节。

## 待用户裁定

- rule 4k-G「已登记未执行」：原文自注需拍板。
- rule 12.5-A 角色造型覆盖块：stage2 playbook 仍要「应用造型」，`gen_turntables_szzl.py` 从立绘抽装束、无卡带此块。
- rule 11d 出场字卡：只 wushen_juexing 用、出图写 Kling——废止还是改走即梦。
- rule 17.4 史料图「允许进参考槽」vs rule 18 画类参考不进上传窗口。
- 06-21 承接的 `首末帧反差:` 行是否必填。
- 12.4 `角色:` ≥ 4 个角色时是否只写前 3 人。
- 12.4-E 台词行是否带语气注。
- K29 `{角色}声音=>@` token：native 下 entity 已绑声样，是否废止。
- H-20 sk1 的 `bg{N}_set.blend` 与 4h-K `_blender/{bg}.blend` 并存。
- 出图卡末负面词清单、平面图 `absent` 喂负面词：是否也受 12.4-P「不点名物件」约束（12.4-P 只管 Seedance prompt）。
- 16 publish：旧文「一部一张」vs CLAUDE.md「每集一份」（本文暂取每集一份）。
- 05-31 骨架版 prompt、05-27 / 05-30 webapp 编辑器条款：废止，还是移到 webapp README。

**规范已定、工具 / skill 未跟上（待同步，不是裁定）**

- `## Seedance prompt` 只接进了 szzl 引擎；其它剧的生成器（xj / hy / sk）第一次改到时再接。
- tts_first 模式：生成器还不会把 `shotNN_tts_lip.wav` 挂进 `参考:` 与 Reference uploads（目前没有剧用 tts_first；第一部用它的剧接）。
- 两引擎 `PROMPT_MAX = 5000` 仍卡设计稿（K10 已改为只卡精简稿）。
- K19；szzl `NEG_RING` / `confusable_negatives` 点名具体物件（只进设计稿，精简稿已剥掉）。K10 / K15 / K22 已按 12.4-P 改。
- K27 ④ 仍按「≤ 3 视频 / 总 ≤ 15 s」判超槽；K16 仍写 7 s turntable；W4 仍按 1500–2000 字。
- `script_tools.py` `EP_RANGE_DEFAULT = (90, 120)`（裁定默认 90–180）。
- szzl 设计稿仍写 `音乐:` 镜内收尾句（12.4-H2 后应删）。
- stage6 playbook 残留：首行 `{NN}集{NN}镜视`、字段反引号、「负面词固定块（必填）」、`## 台词配音 prompt`「后期 mux」。

## 更新协议

1. 本文件只写**现行**规则：每条 ≤ 3 行 + 机检指针；来历、事故、举例、反例一律写进 `ai_video_history.md`（旧版全文，按 rule 号 grep，不通读）。
2. **能量化的写成闸门**（代码里 raise），本文件只留一行「做什么 + 机检指针」。
3. **单剧教训先留在该剧**：新教训默认写进 `specs/ai_video/{name}/lessons.md`；第二部剧复现、或用户明说全局，才升进本文件。
4. 规则被取代：直接改本文件那一条（或删掉），在 `ai_video_history.md` 末尾「沿革」追加一行「rule X 被 Y 取代（日期、来源）」；本文件不留「已废止」正文，只在末尾「已废止」清单列 rule 号。
5. 体量：本文件 ≤ 60 KB，`tools/check_canon.py` 在 Stop hook 里查，超了报警。
