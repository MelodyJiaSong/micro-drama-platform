# 变更

## 建剧 — 2026-11-06

Source: user_input/raw_prompt.md
Summary: 新建系列 chuanyue_yiri（One Day in ___）：README（Vision）、workflow.json、制作圣经与模板库 v0（bible.md）、选题表（topics.md）。第一集庞贝公元 75 年。

未调用收费服务。

## Follow-up 001 — 2026-11-06 18:49:57
Source: user_input/follow_ups/202611.md - section 001
Summary: 新建系列 chuanyue_yiri（One Day in ___）：README 与 Vision、workflow.json（16:9、90–180 秒）、bible.md 模板库 v0（栏目库、镜头模板、考据模板、自动化路线，全部草案）、topics.md（第一集庞贝 75 AD）

Auto-updated:
- ai_videos/chuanyue_yiri/README.md — 新建：Vision、核心、已定事项、文件、状态
- ai_videos/chuanyue_yiri/workflow.json — three-module-v1、series、90–180 秒、seedance2.5、16:9
- ai_videos/chuanyue_yiri/bible.md — 模板库 v0：系列公式、主持人、单集骨架、栏目库 S01–S11、镜头模板 T1–T9、质量底线、考据模板、自动化路线、合规
- ai_videos/chuanyue_yiri/topics.md — 选题标准、第一集庞贝 75 AD 选题卡、候选池
- specs/ai_video/chuanyue_yiri/ — raw_prompt、changelog 建剧

验证: 文档新建，未调用收费服务；workflow.json 已解析；镜头模板均为草案、未实拍验证；主持人长相与名字待用户定

No conflicts found in: （未单独核查）


## Follow-up 002 — 2026-11-06 18:58:44
Source: user_input/follow_ups/202611.md - section 002
Summary: 当地人说当地语言、主持人猜并用肢体回应（新增镜头模板 T10、考据加当地语言台词）；时长起步 90–180 秒不限死（检查上限暂定 300）；主持人人设定为欧美、健硕、活泼、有探险精神、美式英语、有亲和感

Auto-updated:
- ai_videos/chuanyue_yiri/bible.md — §1 当地人说当地语言；§2 主持人人设；§3 时长不限死；§4 S02/S11 加 T10；§5 T7 改写、新增 T10；§6 审核项；§7 当地语言台词
- ai_videos/chuanyue_yiri/README.md — 已定表：时长、当地人、主持人
- ai_videos/chuanyue_yiri/workflow.json — episode_seconds 上限 180 → 300

验证: 文档改动，未调用收费服务；workflow.json 可解析

No conflicts found in: （未单独核查）


## Follow-up 003 — 2026-11-06 19:17:23
Source: user_input/follow_ups/202611.md - section 003
Summary: 主持人名字由代理选定为 Riley；识别特征待用户答复（雀斑不是必需）

Auto-updated:
- ai_videos/chuanyue_yiri/bible.md — §2 名字 Riley

验证: 文档改动，未调用收费服务

No conflicts found in: （未单独核查）


## Follow-up 004 — 2026-11-06 19:46:53
Source: user_input/follow_ups/202611.md - section 004
Summary: Codex 出 4 张 Riley 长相候选（A 蜂蜜金高马尾 / B 铜红长卷发半扎 / C 深棕粗麻花辫 / D 栗棕及肩短卷发）与并排对比图，待用户选

Auto-updated:
- ai_videos/chuanyue_yiri/2_世界观人设/characters/c1_Riley/candidates/ — riley_A–D.png 与 riley_candidates_sheet.png（对比图为本地 PIL 拼接）

验证: 四张逐张看图：都是写实、欧美、健硕、笑容亲和、无文字；请求日志 characters/request_log.md 已记录
费用: Codex 订阅额度 4 次，费用未知

No conflicts found in: （未单独核查）


## Follow-up 005 — 2026-11-06 19:59:26
Source: user_input/follow_ups/202611.md - section 005
Summary: Codex 再出 10 张 Riley 长相候选 E–N（北欧、拉丁裔、非裔、爱尔兰、东欧、白人东亚混血、中西部、希腊、白人非裔混血、西海岸），拼两张对比图，待用户选

Auto-updated:
- ai_videos/chuanyue_yiri/2_世界观人设/characters/c1_Riley/candidates/ — riley_E–N.png、riley_candidates_sheet_2.png（E–I）、riley_candidates_sheet_3.png（J–N）

验证: 10 张逐张看图：都按各自描述出了对应长相，写实、笑容亲和、无文字；请求日志 characters/request_log.md 已记录
费用: Codex 订阅额度 10 次，费用未知

No conflicts found in: （未单独核查）


## Follow-up 006 — 2026-11-06 20:38:33
Source: user_input/follow_ups/202611.md - section 006
Summary: Riley 定为候选 N：建人物卡 c1_Riley（外观、锁定描述符、配音参考、叫声设计、16:9 10 秒建立视频 prompt），立绘直接用 N 原图；建立视频 dry-run 通过，待用户确认提交

Auto-updated:
- ai_videos/chuanyue_yiri/2_世界观人设/characters/c1_Riley/c1_Riley.md — 新建人物卡
- ai_videos/chuanyue_yiri/2_世界观人设/characters/c1_Riley/c1_Riley.png — 复制自 candidates/riley_N.png（sha 31e351334362）
- ai_videos/chuanyue_yiri/README.md — 状态

验证: char_assets status：立绘块/立绘/视频块齐，缺建立视频与三视图；gen_turntable_videos --dry-run 解析正常（16:9 · 10s · seedance2.5 · 1105 字）；未提交视频

No conflicts found in: （未单独核查）


## Follow-up 009 — 2026-11-06 21:18:35
Source: user_input/follow_ups/202611.md - section 009
Summary: 每集按栏目需要由代理设计当地人物（摊贩、祭司、店主等），立卡规则写进 bible

Auto-updated:
- ai_videos/chuanyue_yiri/bible.md — §2.1 每集的当地人物（立卡条件、编号、设计依据、个性、说话与声样、资产链、数量）；§2 跨集识别物改为脏金色波浪长发

验证: 文档改动；ep01 的当地人物在考据汇总与本集计划后设计

No conflicts found in: （未单独核查）


## Follow-up 007 — 2026-11-06 20:48:42
Source: user_input/follow_ups/202611.md - section 007
Summary: Riley 建立视频出片（seedance2.5，16:9 10s），按实际片重抽三视图与声样；启动 ep01 庞贝 75 AD 考据：6 路并行调研（城市与一天、吃与住、信仰权力娱乐、谋生医疗贫富、衣着语言黑名单、视觉素材）

Auto-updated:
- ai_videos/chuanyue_yiri/2_世界观人设/characters/c1_Riley/ — 建立视频 c1_Riley_turntable.mp4（submit ba50f664）、按实际片重抽 views 三视图与声样、人物卡生成记录
- ai_videos/chuanyue_yiri/episodes/ep01/0_research/parts/r01–r05 — 五路考据
- ai_videos/chuanyue_yiri/episodes/ep01/0_research/refs/ — 70 张开放许可参考图与 refs.md
- ai_videos/chuanyue_yiri/episodes/ep01/0_research/dossier.md — 考据总表

验证: 建立视频逐帧初审（未核听台词）；考据五份主代理通读，frontmatter 齐、未查项照实列出；refs 子代理抽看约 30 张；未做独立审稿
费用: Seedance 建立视频 1 条（工具估约 80 分，以回执为准）

No conflicts found in: （未单独核查）


## Follow-up 010 — 2026-11-06 21:22:46
Source: user_input/follow_ups/202611.md - section 010
Summary: Riley 默认穿现代旅行装到达（与当地人形成对比），可在集中换上当地服装；全剧负面词去掉「现代服饰」改为限定路人

Auto-updated:
- ai_videos/chuanyue_yiri/bible.md — §2「穿什么」：默认现代旅行装到达，可中途换装
- ai_videos/chuanyue_yiri/workflow.json — 负面词「现代服饰」改为「路人穿现代服饰」
- ai_videos/chuanyue_yiri/2_世界观人设/characters/c1_Riley/c1_Riley.md — 本人造型即现代旅行装，新增「现代旅行装」段
- ai_videos/chuanyue_yiri/episodes/ep01/0_research/dossier.md — Riley 服装一行

验证: 文档改动；workflow.json 可解析；c1-1_Pompeii 换装三视图保留，供集中换装后使用

No conflicts found in: （未单独核查）


## Follow-up 008 — 2026-11-06 21:08:33
Source: user_input/follow_ups/202611.md - section 008
Summary: 用户举的栏目只是例子：由代理思考 One Day in ___ 通常拍什么（扩展栏目库），并自主完成考据与资产准备（图片代理直接出；视频仍人点）

Auto-updated:
- ai_videos/chuanyue_yiri/0_research/parts/f01_同类节目拍什么.md — 同类节目调研（25 条视频章节与约 1,800 条热评）
- ai_videos/chuanyue_yiri/bible.md — §3 单集骨架改为开场三件套（含当天小目标）、短片与长片结构、每集反差配额；§4 栏目库 v1：三档 25 栏目（S01–S25）+ 本集特色，附依据；QC 时代错置提醒
- ai_videos/chuanyue_yiri/episodes/ep01/0_research/dossier.md — 栏目号按 v1 重映射
- ai_videos/chuanyue_yiri/2_世界观人设/characters/c1_Riley/c1-1_Pompeii/ — 庞贝换装卡与正侧背三视图、合图

验证: f01 主代理通读 §3–§5；c1-1 三视图逐张看图（同一人、披巾骨簪铜镯三面一致）；未做独立审稿
费用: Codex 订阅额度 3 次（换装三视图），费用未知

No conflicts found in: （未单独核查）


## Follow-up 011 — 2026-11-06 21:35:10
Source: user_input/follow_ups/202611.md - section 011
Summary: EP01 庞贝 75 AD 故事稿 v1 → 独立冷读 → v1.1；新建 series.md（Riley 主目标）；决策记录含体验地图、观众轨、目标影响、台词逐句、站位与视线

Auto-updated:
- ai_videos/chuanyue_yiri/episodes/ep01/story.md — 故事稿 v1.1（六场约 150 秒）
- ai_videos/chuanyue_yiri/episodes/ep01/decisions/story.md — 集级故事决策记录
- ai_videos/chuanyue_yiri/2_世界观人设/series.md — 全剧方向与 Riley 主目标
- ai_videos/chuanyue_yiri/README.md — 状态

验证: audience_check --module story：齐全；独立冷读（fresh context，1 blocker / 6 major / 7 minor）已处理，v1.1 未再冷读；待用户确认与评分卡

No conflicts found in: （未单独核查）


## Follow-up 013 — 2026-11-06 22:14:16
Source: user_input/follow_ups/202611.md - section 013
Summary: EP01 当地人物 4 张立绘（c2 Felix 面包师、c3 Tertius 洗衣工、c4 Asellina 熟食铺老板娘、c5 Fortunata 大车店女店主）与 7 张场景图（bg1 海门外陡坡为世界锚点、bg2 石板街、bg3 面包房、bg4 洗衣坊、bg5 熟食铺、bg6 大车店门口、bg7 大车店客房）；ElevenLabs 额度用尽，全部自动改走 Codex

Auto-updated:
- ai_videos/chuanyue_yiri/2_世界观人设/characters/c2_Felix|c3_Tertius|c4_Asellina|c5_Fortunata/ — 人物卡与立绘（c3 下摆过短、c4 围裙污渍像血，改卡重出一次）
- ai_videos/chuanyue_yiri/2_世界观人设/background/registry.toml 与 pompeii_75/bg1–bg7 — 背景卡与锚点图

验证: 逐张看图：人物写实无字；背景均为有屋顶、抹灰上色的 75 年样貌，无人无字；bg7 高窗略像格子玻璃窗，待分镜确认入画再修；未做独立审稿
费用: Codex 订阅额度 13 次（人物 6、背景 7），费用未知；ElevenLabs 4+7 次 quota_exceeded 失败未扣费

No conflicts found in: （未单独核查）


## Follow-up 015 — 2026-11-06 22:39:45
Source: user_input/follow_ups/202611.md - section 015
Summary: 用户批准 4 条当地人物建立视频（8 秒，约 640 积分）；正片出片方式定为编译完整集后一次批准

Auto-updated:
- ai_videos/chuanyue_yiri/2_世界观人设/characters/c2_Felix|c3_Tertius|c4_Asellina|c5_Fortunata/ — 建立视频（8 s，submit 641be8ae / 84ee673e / d45b7fc4（c4 首次 0b003735 上传阶段失败后重提）/ 1b176c6e），按实际片抽 views 三视图与声样、合图

验证: 逐帧看片：全身入画、同一张脸、侧背转到位；silencedetect 定说话段截声样；台词与口音未核听；未独立审稿
费用: Seedance 4 条成功各 160 积分（回执）；c4 首次上传阶段失败

No conflicts found in: （未单独核查）


## Follow-up 016 — 2026-11-06 22:59:31
Source: user_input/follow_ups/202611.md - section 016
Summary: EP01 影视改编：7 场 21 镜 186 秒（场六拆为 s6 门口 / s7 客房），7 处场地平面图、21 份 overhead 与取景静帧；集级与场级决策记录；Prompt 编译与 21 个资料包；Riley 外观段补现代旅行装

Auto-updated:
- ai_videos/chuanyue_yiri/episodes/ep01/filming.json、story.json、prompts.json — 经 EpisodeWorkflowCommand 保存 / 批准 / 编译
- ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1–s7/ — overhead、取景静帧、场级决策、prompt.txt、资料包
- ai_videos/chuanyue_yiri/episodes/ep01/decisions/filming.md — 集级影视改编决策
- ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1–bg7/planning/blocks.toml — 场地平面图（推定）
- ai_videos/chuanyue_yiri/2_世界观人设/characters/c1_Riley/c1_Riley.md — 外观段加现代旅行装

验证: shot_overhead --all：21 镜 blocker 0 warning 0；取景静帧 21 镜自检通过（s2 st1 主观镜改低机位侧拍后通过）；audience_check filming：齐全；shot_pack check：ok 21

No conflicts found in: （未单独核查）


## Follow-up 012 — 2026-11-06 21:56:52
Source: user_input/follow_ups/202611.md - section 012
Summary: EP01 维苏威火山全片不提（用户回答三选一）

Auto-updated:
- ai_videos/chuanyue_yiri/episodes/ep01/story.md、filming.json、dossier 负面词；s1 st3 第 1 轮远山成火山锥，改分镜重出

验证: 21 镜逐镜看拼图：全片台词与画面都没提维苏威；s1 st3 第 2 轮远山为低缓绿坡（decisions/render_review.md）

No conflicts found in: bible.md §1、story.md


## Follow-up 014 — 2026-11-06 22:28:04
Source: user_input/follow_ups/202611.md - section 014
Summary: 用户不打评分卡、授权代理直接继续（故事稿 v1.1 视为确认）；出片不出 480p 草稿，直接正式条（workflow.json prompt.skip_draft）

Auto-updated:
- ai_videos/chuanyue_yiri/workflow.json prompt.skip_draft；故事稿 v1.1 直接进影视改编

验证: 21 镜全部以 720p 正式条出片，无 480p 草稿（generation.json no_draft）

No conflicts found in: AGENTS.md 生成永远人点：出片仍由用户逐批批准（017）


## Follow-up 017 — 2026-11-06 23:00:20
Source: user_input/follow_ups/202611.md - section 017
Summary: 用户批准 EP01 全部 21 镜正片出片（720p、不出草稿、约 3,700 积分；同一镜最多重出 3 轮）

Auto-updated:
- ai_videos/chuanyue_yiri/episodes/ep01/scenes/*/shots/*/renders/（22 条）、各 review.md、decisions/render_review.md、filming.json s1 st3

验证: 21 镜第 1 轮全部成功；逐镜 1fps 拼图 + faster-whisper 转写 + 独立子代理审片；s1 st3 重出 1 轮后保留；其余 20 镜保留（7 镜有备注）
费用: Dreamina seedance2.5 720p 共 3,880 积分（22 条）

No conflicts found in: 同一镜最多重出 3 轮：只用了 1 轮


## Follow-up 018 — 2026-11-06 23:06:17
Source: user_input/follow_ups/202611.md - section 018
Summary: EP01 出片审完后做一个友好的预览页（按场展示每镜视频、台词、审片结论），给用户链接

Auto-updated:
- Artifact https://claude.ai/artifact/Bx16u9E6WWcZYCRHWQHshn（21 镜压缩片、定妆照、台词与拉丁语释义、审片结论、连播）

验证: 发布成功，47 个附件 33 MB；页面数据由 filming.json 生成，镜数与时长 21 镜 / 186 秒对得上

No conflicts found in: 无


## Follow-up 019 — 2026-11-07 09:02:14
Source: user_input/follow_ups/202611.md - section 019
Summary: EP01 7 场正片剪辑 v1 与整集 v1

Auto-updated:
- scenes/s1–s7/edit/final/cut_v1.json 与 s*_final_v1(.mp4/_标注.mp4)；edit/final/cut_v1.json → ep01_final_v1.mp4（181.0s）；各条 annotation.json；episodes/ep01/preview.json；README 状态

验证: scene_cut check 7 场问题无，render 时长与帧数全对、无黑段；episode_cut join 时长 181.0 对，切点 16 中检出 15（s1 st1→st2 画面相近 scdet 未检出），黑段只有 s4→s5 黑场；抽帧核对转场与片尾淡出
费用: 0（本地 ffmpeg / faster-whisper，无收费调用）

No conflicts found in: 只新增剪辑产物，不改分镜与条


## Follow-up 020 — 2026-11-07 09:59:12
Source: user_input/follow_ups/202611.md - section 020
Summary: 规则进仓库级（审核结论门槛、分镜进出与余量、剪辑转场与节奏、两条自检）；EP01 v2 改稿

Auto-updated:
- 仓库级：filming.md 给剪辑留出进出与余量、prompts-generate.md 审核结论门槛（画面错误一律重出）与场故事板单镜首帧、edit-transitions.md / edit-fine.md 场尾停留与转场、edit.md 镜组事件、qc_checks.toml 两条（video.object_continuity、edit.scene_joins）；剧级：bible 开场直接说穿越、Portal Travel 改名与时空门开场计划、时长上限 480；Riley v2 身材（高清全身三视图，v1 存档 _v1_stocky）；新背景 bg8–bg11；EP01 故事 v2、分镜 42 镜 15 镜组、镜组板与首帧图、全集重出 29 条、逐条 review.md、八场正片剪辑、整集 v3 ep01_final_v3.mp4（6:33）、decisions/render_review_v2.md、preview.json

验证: 逐条 1 fps 拼图 + 可疑处 4–12 fps 细看 + faster-whisper 转写（拉丁语段 medium 强制拉丁语）；两次 fresh context 独立审稿（场一、整集），意见逐条处理并记录；scene_cut / episode_cut check 无问题，渲染时长与帧数对；v3 接口转写实测间隔 ≥1.1 秒（s8→s5 改切后首词完整）；单集预览页无头 Chrome 打开正常
费用: Dreamina 29 条 8,960 积分；Codex 出图（背景 4、Riley 3、镜组板 15、首帧 12 张）走订阅额度

No conflicts found in: 旧 v1 条与剪辑保留；新增规则与现有规则不冲突


## Follow-up 021 — 2026-11-07 15:03:54
Source: user_input/follow_ups/202611.md - section 021
Summary: Riley 保持 v2 身材与现代旅行装，经 Codex 内置出图出 10 张不同脸的候选（左全身、右脸部特写），放 c1_Riley/candidates/faces_v3/，供用户挑；选定前不改立绘与三视图

Auto-updated:
- c1_Riley/candidates/faces_v3/：riley_face_f01–f10（欧美脸）、f11–f20（中美混血，用户追加；以后可说中英文）、_prompts/、拼图 _sheet_*.jpg；立绘、三视图、EP01 未动

验证: 20 张逐张看拼图：身材、服装、站姿与 v2 三视图一致；第一批脸差异偏小（F01/F04/F05 近似），第二批混血特征明确
费用: Codex 内置出图 20 次（ChatGPT 订阅额度，characters/request_log.md 已记）

No conflicts found in: EP01 v2 由会话 9142d566 推进，本条只写 candidates/faces_v3，不改它在用的参考图


## Follow-up 022 — 2026-11-07 15:20:24
Source: user_input/follow_ups/202611.md - section 022
Summary: Riley 第三批脸候选 F21–F30：中美混血、黑发、大眼睛、高鼻梁、知性美；身材服装仍照 v2 三视图

Auto-updated:
- c1_Riley/candidates/faces_v3/riley_face_f21–f30.png、_prompts/f21–f30、_sheet_f21-f30.jpg；立绘与三视图未动

验证: 拼图逐张看：10 张均黑发、大眼、高鼻梁、混血特征明确，身材服装与 v2 三视图一致；已发用户
费用: Codex 内置出图 10 次（characters/request_log.md 已记）

No conflicts found in: 只写 candidates/faces_v3


## Follow-up 023 — 2026-11-07 15:41:14
Source: user_input/follow_ups/202611.md - section 023
Summary: 以候选 F22 为基准出 10 张微调变体 F22a–F22j（同一人，单项微调五官、发型、表情），身材服装不变

Auto-updated:
- c1_Riley/candidates/faces_v3/riley_face_f22a–j.png、_prompts/f22a–j、_sheet_f22_variants.jpg；立绘与三视图未动

验证: 与 F22 原图并排看：10 张同一人、身材服装一致；多数微调幅度很小，F22h 雀斑没去干净；已发用户
费用: Codex 内置出图 10 次（characters/request_log.md 已记）

No conflicts found in: 只写 candidates/faces_v3


## Follow-up 024 — 2026-11-07 15:55:24
Source: user_input/follow_ups/202611.md - section 024
Summary: F22 第二轮 10 张（F22k–F22t）：上一轮微调太细，这轮同一张脸做更明显的变化（发型、刘海、眼镜、眼型、瞳色、肤色、角度）

Auto-updated:
- c1_Riley/candidates/faces_v3/riley_face_f22k–t.png、_prompts/f22k–t、_sheet_f22_variants2.jpg；立绘与三视图未动

验证: 拼图逐张看：10 张同一人、变化都看得出（短发、马尾、丸子头、眼镜、刘海、东方眼型、琥珀瞳、白皙肤色、侧脸、麻花辫），身材服装一致；已发用户
费用: Codex 内置出图 10 次（characters/request_log.md 已记）

No conflicts found in: 只写 candidates/faces_v3


## Follow-up 025 — 2026-11-07 16:11:29
Source: user_input/follow_ups/202611.md - section 025
Summary: Riley 第五批脸候选 F31–F40：与 F21–F30 同一方向（中美混血、黑发、大眼、高鼻梁、知性美），但每张是不同的人，区分度拉大

Auto-updated:
- c1_Riley/candidates/faces_v3/riley_face_f31–f40.png、_prompts/f31–f40、_sheet_f31-f40.jpg；立绘与三视图未动

验证: 拼图逐张看：10 张为不同的人，身材服装与 v2 三视图一致；F34/F38 与 F22 型相近，其余区分明显；已发用户
费用: Codex 内置出图 10 次（characters/request_log.md 已记）

No conflicts found in: 只写 candidates/faces_v3


## Follow-up 026 — 2026-11-07 18:01:47
Source: user_input/follow_ups/202611.md - section 026
Summary: Riley 第六批脸候选 F41–F50：中美混血、东方感更多、五官秀气精致，黑发，身材服装不变

Auto-updated:
- c1_Riley/candidates/faces_v3/riley_face_f41–f50.png、_prompts/f41–f50、_sheet_f41-f50.jpg；立绘与三视图未动

验证: 拼图逐张看：东方感与秀气明显多于前几批，10 张为不同的人，身材服装一致；已发用户
费用: Codex 内置出图 10 次（characters/request_log.md 已记）

No conflicts found in: 只写 candidates/faces_v3


## Follow-up 027 — 2026-11-07 18:10:40
Source: user_input/follow_ups/202611.md - section 027
Summary: Riley 第七批脸候选 F51–F60：在秀气东方美的中美混血基础上，统一小嘴、尖下巴（瓜子脸 / V 脸），抿嘴或浅笑以免嘴显大

Auto-updated:
- c1_Riley/candidates/faces_v3/riley_face_f51–f60.png、_prompts/f51–f60、_sheet_f51-f60.jpg；立绘与三视图未动

验证: 拼图逐张看：10 张都是小嘴、抿嘴浅笑；尖下巴以 F51/F52/F55/F56 最明显，F58/F60 下巴偏圆；身材服装一致；已发用户
费用: Codex 内置出图 10 次（characters/request_log.md 已记）

No conflicts found in: 只写 candidates/faces_v3


## Follow-up 028 — 2026-11-07 18:28:31
Source: user_input/follow_ups/202611.md - section 028
Summary: 三个入围脸 F59 / F51 / F22 各出：全身三视图（正、侧、背）＋开心、难过、愤怒、悲伤四张表情特写，做对比板给用户三选一

Auto-updated:
- c1_Riley/candidates/compare_v3/{f22,f51,f59}/views.png + expr_happy/sad/angry/grief.png、_prompts/、_compare_board.jpg；立绘与三视图未动

验证: 对比板逐张看：三人各自 5 张为同一人，三视图头到脚完整、背面发型清楚（F59 辫子一致），四种表情区分明确；已发用户
费用: Codex 内置出图 15 次（characters/request_log.md 已记）

No conflicts found in: 只写 candidates/compare_v3


## Follow-up 029 — 2026-11-07 18:42:40
Source: user_input/follow_ups/202611.md - section 029
Summary: F22 改秀气版 F22s、F59 改大眼版 F59e，各重出定妆照＋三视图＋四表情；F51 重出开心、难过、愤怒（悲伤保留）；表情改为克制好看的演法

Auto-updated:
- compare_v3/f22s/（base、views、四表情）、compare_v3/f59e/（同）、compare_v3/f51/expr_{happy,sad,angry}_v2.png、_compare_board_v2.jpg、_base_before_after.jpg

验证: 并排看：F22S 比原 F22 更收敛秀气（变化中等），F59E 眼睛变大幅度小；F51 开心、愤怒明显更好看，难过仍偏皱；各人 5 张为同一人；已发用户
费用: Codex 内置出图 15 次（characters/request_log.md 已记）

No conflicts found in: 只写 candidates/compare_v3


## Follow-up 030 — 2026-11-07 20:35:57
Source: user_input/follow_ups/202611.md - section 030
Summary: 用户选定 Riley 新脸 F22S（秀气版）。先用 Codex 出正式全身正、侧、背三视图到 c1_Riley/_v3_f22s/ 待替换；替换现役立绘/三视图、建立视频与 EP01 是否重出待用户答复

Auto-updated:
- c1_Riley/_v3_f22s/：c1_Riley_front/side/back.png（941×1672，与现役同规格）、c1_Riley_views.png、_prompts/；现役立绘与 views/ 未替换

验证: 三视图头到脚完整、同一人同服装；正面脸部放大与 F22S 并排核对一致；已发用户
费用: Codex 内置出图 3 次（characters/request_log.md 已记）

No conflicts found in: EP01 在用现役 views/，替换待用户定 EP01 方案（A 保留旧脸 / B 重出）


## Follow-up 032 — 2026-11-07 20:50:36
Source: user_input/follow_ups/202611.md - section 032
Summary: 镜组收窄规则写入 filming.md / edit.md（仓库级，用户已同意）；面包黏手（s3 st2，自拍占一只手却写双手掰）记缺陷；审查策略页面已出，待用户确认后实施。

Auto-updated:
- .agents/skills/ai-videos-pipeline/modules/filming.md（镜组收窄规则）; .agents/skills/ai-videos-pipeline/modules/edit.md（组内切点不合适回上游拆组）; ep01/scenes/s3/shots/st2/planning/st2_first_frame{.png,_prompt.txt}（固定机位双手掰的首帧，未出片）; qc 缺陷 new:physics_support

验证: 面包黏手在 4 fps 拼图上确认（10.9–14.5 s 指尖捏顶、剩余面包悬空）；其他自拍镜逐条查过只用一只手；qc.py escapes 确认本剧闸门从未调用；审查策略页 https://claude.ai/artifact/85AYUqbGZqbbKxX1cKkFH7 待用户确认后实施；按用户要求未重出视频
费用: 0 积分（首帧图走 Codex 订阅）

No conflicts found in: 只追加规则段落，不改已有镜组字段与工具


## Follow-up 031 — 2026-11-07 20:44:20
Source: user_input/follow_ups/202611.md - section 031
Summary: Riley 换为 F22S：替换立绘与三视图（v2 存档 _v2_tall/）、改人物卡（外观、中英双语声线）；出中英双语建立视频与声样；Codex 出一套表情图；人物审阅页（ai_video_management follow-up 329）

Auto-updated:
- c1_Riley：立绘与 views 换 F22S（v2 存 _v2_tall/）、c1_Riley.md（外观、中英声线、15 秒 turntable 块、生成记录）、c1_Riley_turntable.mp4、views/c1_Riley_audio.mp3（中英 9.6 秒）、expressions/E01–E12、review.json；README 状态

验证: 转写：英文 0–4.3 s、普通话 4.3–9.3 s 与台词一致；1 fps 拼图正侧背到位、全身完整；12 张表情同一人；审阅页可打开
费用: seedance2.5 建立视频 1 条（c74607af）；Codex 内置出图 12 张；均记 characters/request_log.md

No conflicts found in: EP01 v2 的 28 条是旧脸，用户未定是否重出；EP01 引用的 views 路径已指向新脸，若重出旧镜会是新脸


## Follow-up 033 — 2026-11-07 22:21:13
Source: user_input/follow_ups/202611.md - section 033
Summary: 13 位按法则分工的独立审稿人（物理×4、人物逻辑×2、镜头规格×2、连续性、台词、时代、观众、prompt 文本）全量审 EP01 v2：248 条（重出 75），八成源于出片前；汇总与分步建议写入 decisions/audit_v2_全量审查.md，原始报告归档 audit_v2/

Auto-updated:
- ep01/decisions/audit_v2_全量审查.md（新：汇总、分步建议、248 条附录）; ep01/decisions/audit_v2/（13 份审稿报告与审稿说明）

验证: 13 份报告全部回收（首轮 11 位因网络 403 中断，重派后完成）；脚本合并 248 行表格并统计严重度与来源；关键结论交叉印证：迷路主线（人物 A / 观众 / 台词三方独立）、维苏威山与白烟（5 方独立）、面包黏手（物理 B 独立复现用户发现）；bible 第 181 行核实只写避开爆发当天；未出片、未花积分
费用: 0 积分（审稿为本机子代理与 faster-whisper）

No conflicts found in: 只新增审查文件，不改分镜、prompt、资产；人物卡由另一会话维护，未动


## Follow-up 034 — 2026-11-07 22:50:28
Source: user_input/follow_ups/202611.md - section 034
Summary: 新增审查单机制：名册 review_roster.json 按阶段×法则×范围生成清单；审稿人交合格报告后自己 tick，作者不能代勾；材料变则作废；gate 全勾才过；规则写入 pipeline SKILL.md 与 prompts-generate.md；EP01 全量审查补登为第一张单（13/13）

Auto-updated:
- tools/review_run.py（新）; tools/tests/test_review_run.py（新 4 条）; .agents/references/project/review_roster.json（新，登记为工作流源 1.0.5）; .agents/skills/ai-videos-pipeline/SKILL.md「审查以审查单为准」; modules/prompts-generate.md 独立审查行; workflow_catalog.json; ep01/reviews/20261107-223834_full（补登 13/13）

验证: pytest tools/tests 225 passed（含 review_run 4 条：按名册生成、作者不能代勾、无表报告拒勾、无问题结论可勾、失败项挡闸、材料变更作废）；EP01 实跑 new --stage full 生成的 13 项与当日实际审稿人一一对应，补登后 gate 通过；workflow_catalog --check 编号连续 235 源；补登项均带备注「勾由作者会话代为登记」
费用: 0

No conflicts found in: 新增工具与名册；SKILL 只追加一段；不改 qc.py / qc_review.py 既有行为


## Follow-up 035 — 2026-11-07 23:17:31
Source: user_input/follow_ups/202611.md - section 035
Summary: 出片前审查循环：名册加必查项与 pregen 阶段、max_loops=3；review_run 支持 --after 开下一轮（必填 changes，自动复核上一轮）、tick 校验必查项、conclude 写结果.md、confirm 登记用户原话、can-submit；审查单移到 ai_videos/<剧>/reviews/；shot_take 在 review_gate=required 时拦未确认的出片；本剧已开闸；规则写入 SKILL.md 与 prompts-generate.md

Auto-updated:
- tools/review_run.py（循环、必查项、conclude/confirm/can-submit、存到剧 reviews/）; tools/tests/test_review_run.py（6 条）; tools/shot_take.py（review_gate 闸门、--skip-review）; review_roster.json（must、pregen、max_loops）; chuanyue_yiri/workflow.json（review_gate=required）; reviews/ep01_20261107-223834_full_r1（由集目录迁来）; ai-videos-pipeline SKILL.md、modules/prompts-generate.md

验证: pytest tools/tests 227 passed（含：必查项缺一不能勾、--after 无 changes 拒绝、第 4 轮拒绝、未 confirm 不放行出片、确认后材料变更失效、未覆盖的场不放行）；实跑 shot_take submit ep1_s1_st1 被闸门拦下（未发起任何生成）；迁移后旧审查单 status 正常
费用: 0

No conflicts found in: 闸门只对 workflow.json 写了 review_gate=required 的剧生效，目前仅 chuanyue_yiri；其他剧出片不受影响


## Follow-up 037 — 2026-11-08 13:42:43
Source: user_input/follow_ups/202611.md - section 037
Summary: review_run.py 升到名册 v5：每项 Claude＋Codex 双审（按名册选合适模型）、按类 rubric 0–3 打分且高分须证据；两份都勾后自动对比，分歧与抽查交裁决人 adjudicate；issues 推出 critical/major/verify/minor 问题清单，fix 记方案，critical/major 处理完才能开下一轮，changes/previous 由清单生成；Codex 位凭 codex exec 日志 --attest-log 代登记（v2 单同样）。

Auto-updated:
- tools/review_run.py：v5 审查单（slots a/b、per-slot 任务书含是什么/rubric/评分规则/审法/范围/材料/打勾命令；评分表校验；--attest-log 代登记（Codex 位与最近派单为 Codex 的 v2 项，日志须含报告路径且晚于派单，日志另存 agents/）；reconcile 自动对比与确定性抽查；adjudicate 裁决；dispatch/fail --slot；issues 分级清单 issues.json/md；fix 方案与状态；new --after 要求 critical/major 处理完并由清单生成 changes.md/previous.md；status/gate/conclude 显示两位分数并排与最终分，收轮后有未处理 critical 时 gate 不过）。tools/tests/test_review_run.py 更新原 11 条并新增 11 条（共 22）。SKILL.md「审查以审查单为准」段与 modules/prompts-generate.md 一行改为新循环。进行中的 v2 单 ep01_20261108-131724_pregen_r1 的 native_ear 已凭 codex 日志代登记，单子 13/13 已完成。

验证: python -m pytest tools/tests/test_review_run.py -q：22 passed；python -m pytest tools/tests -q：248 passed；sync_agent_skills.py --check、workflow_catalog.py --check 通过；管理站 tests/test_review_run_api.py 因本机缺 fastapi 未能运行；管理站 UI 未改（ticked_by 保持字符串，另加 ticked_by_list）。

No conflicts found in: （未单独核查）


## Follow-up 036 — 2026-11-08 09:17:02
Source: user_input/follow_ups/202611.md - section 036
Summary: EP01 出片前审查循环：先按全量审查把便宜的改动做掉（故事 v2.1、规则源、分镜、prompt、首帧），再开 pregen 审查单 r1–r3，结果交用户确认；不出片

Auto-updated:
- 故事 v2.1（迷路线、钱账、面包、目标编号、头发、台词母语改写、客栈大堂与客房参观）；bible §2/§9；workflow.json 风格与负面词；场景卡 bg1–bg13 及 bg1-2/bg2-2 修订与重出；道具卡 p1–p5、人物卡 c6/c7（Codex 出图）；filming 63 镜全部单拍并按 s1 三轮、s2–s8 第 1 轮审查逐条修复；首帧 63 张重画；review_roster v3–v5（母语听感、mechanisms、rubric、双审）；tools/review_run.py（指纹按场、dispatch、v5 双审/裁决/issues/fix、代登记）；出图改为只用 Codex

验证: s1 出片前审查 3 轮完成（重出 11→4→2）；s2–s8 第 1 轮 13 位审稿人完成，207 条问题中 critical/major 71 条全部 implemented；tools 测试 247 passed；shot_pack check ok 63；shot_overhead 63 镜 blocker 0

No conflicts found in: （未单独核查）


## Follow-up 038 — 2026-11-08 15:38:06
Source: user_input/follow_ups/202611.md - section 038
Summary: tools/review_run.py 加每张审查单的命令锁（.lock，读-改-写串行）和原子写入（临时文件 + os.replace）；写坏的 ep01_20261108-153205_pregen_r2 取第一个完整对象恢复，原文件留档；受影响的打勾由审稿人自己重打

Auto-updated:
- tools/review_run.py（RunLock、save 原子写）

验证: tools/tests/test_review_run.py 30 passed；r2 审查单恢复后 dialogue/native_ear a 位均为已打勾

No conflicts found in: （未单独核查）


## Follow-up 039 — 2026-11-08 20:12:53
Source: user_input/follow_ups/202611.md - section 039
Summary: EP01 s3 面包房：同一素材池、同一说明，现有流程版 vs CapCut AI 粗剪版（只用自备素材，禁用 CapCut 一切公司内容），机检合规后盲化，人与独立模型盲审。

Auto-updated:
- ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/edit/blind_capcut/README.md — 盲测设计、逐项商用来源、机检规则与校准、步骤与状态
- ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/edit/blind_capcut/brief_en.md — 两方共用的英文剪辑说明（台词按素材实际所说）
- ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/edit/blind_capcut/codex_desktop_prompt.md — Codex 桌面版 CapCut 一方执行提示（禁用公司内容、先记请求日志、用户导出）
- ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/edit/blind_capcut/scoresheet.md — 人审盲评表
- ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/edit/blind_capcut/pool.json、pool/clip_01–03.mp4、arms/pipeline.mp4 — 素材池（st5 c08587ff、g1 39d404cc、g2 6855880d）与现有流程一方 s3_final_v3（aa85902b）
- ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/edit/blind_capcut/check/ — 现有流程一方机检合规与五个灵敏度校准
- .agents/references/project/paid_services.md — CapCut 行加盲测唯一例外

验证: 现有流程一方机检合规；人为加字幕、角标、背景噪声都判不合规，CRF28 重编码合规；在 scratchpad 副本上空跑 blind / review --dry-run / reveal 通过。CapCut 一方待用户在 Codex 桌面版执行；未发生任何 CapCut 调用与费用

No conflicts found in: （未单独核查）


## Follow-up 040 — 2026-11-08 20:26:11
Source: user_input/follow_ups/202611.md - section 040
Summary: 母语听感（review_roster.json native_ear）加说出口测试 N7、修辞痕迹 N8、处境匹配 N9，N6 改为强制列满最不像真人说话的 5 句；明确结构巧妙不加分。用新标准重审 ep01 全集台词并改写。

Auto-updated:
- .agents/references/project/review_roster.json（native_ear 加 N7 说出口测试、N8 修辞痕迹、N9 处境匹配，N6 强制列句，结构巧妙不加分）

验证: pytest tools/tests/test_review_run.py 30 passed；两位盲审（Claude Sonnet、Opus）用新标准都把 Bed? Found… 排第 1

No conflicts found in: 只改母语听感一类的审稿说明，不动工具逻辑


## Follow-up 041 — 2026-11-08 20:56:50
Source: user_input/follow_ups/202611.md - section 041
Summary: 流程改为台词先自然、镜头再跟：review_roster 母语听感去掉「不更长 / ≤2.8 词每秒」，台词审稿 D1 改为算所需时长、修法是延长镜头 / 加镜头 / 加场 / 重写镜头或场；character-sim、story-structure、filming 同步写明不为长度语速删改台词。按新规则重审 ep01 台词并改进。

Auto-updated:
- review_roster.json（native_ear 去掉不更长 / ≤2.8 词每秒；dialogue D1 改为算所需时长，修法延长镜头 / 加镜头 / 加场 / 重写）、character-sim SKILL.md、story-structure.md、filming.md；ep01 台词按 v7 定稿 33 句、镜长 708→871 秒

验证: pytest 30 passed；overhead 63 镜 0 blocker 0 warning；shot_pack 63/63 ok；prompts.json 无旧台词残留

No conflicts found in: 镜头数不变，首帧未改


## Follow-up 042 — 2026-11-08 21:01:24
Source: user_input/follow_ups/202611.md - section 042
Summary: 补充 041：语速保持正常（约 2.5 词/秒，不靠说快塞进镜头），台词变长就延长视频或多加镜头；filming / story-structure / character-sim 与台词审稿 D1 同步写明。

Auto-updated:
- filming.md、story-structure.md、character-sim SKILL.md、review_roster.json dialogue D1：语速保持正常约 2.5 词/秒，不靠说快塞进镜头

验证: 两组作者按正常语速重排节拍，overhead 闸门 0 blocker 0 warning

No conflicts found in: 与 041 一致


## Follow-up 043 — 2026-11-08 21:25:40
Source: user_input/follow_ups/202611.md - section 043
Summary: 补插件安装步骤（官方安装提示 + 连接检查也先记日志）；两个盲测工具的输出改为 UTF-8，避免在非 UTF-8 控制台崩溃。

Auto-updated:
- ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/edit/blind_capcut/codex_desktop_prompt.md — 加「先装插件」：官方安装提示，连接检查也先记请求日志，装好后在新任务里执行
- tools/mcp_request_log.py、tools/edit_blind_test.py — stdout / stderr 强制 UTF-8，非 UTF-8 控制台不再因打印中文崩溃

验证: PYTHONIOENCODING=cp1252 下两个工具都正常打印并退出 0；py_compile 通过。CapCut 仍未调用、未上传；Codex 写的 arms/capcut_notes.md 保留


## Follow-up 044 — 2026-11-08 21:36:33
Source: user_input/follow_ups/202611.md - section 044
Summary: 编译器 v14：有台词的镜头声音行加「对白优先」；只有路人（extras）的镜头也带自然表演句；道具用法改成同类照样画、数量按画面。chuanyue_yiri ep01 重编 63 镜。

Auto-updated:
- libs/common/episode_workflow.py（COMPILER_VERSION 14、DIALOGUE_PRIORITY_RULE、PROP_USAGE）、libs/domain/entities/episode_workflow__entity.py；ep01 prompts.json 重编

验证: 后端 pytest 499 passed，1 failed 为 test_global_workflow 引用闭包（xihuan/xianxia/paid_services 等他处新增文件未登记，非本次改动）；ep01 对白优先 82 处、就是这一件 0 处、s2_st3/s5_st6/s7_st5 带自然表演句；shot_pack 63/63 ok

No conflicts found in: 其他剧 prompts 会显示过期，按用户「不用管过期的」不重编


## Follow-up 045 — 2026-11-09 00:42:48
Source: user_input/follow_ups/202611.md - section 045
Summary: Codex CLI 接续完成 CapCut 一方（第三条重传、AI 粗剪、下载渲染成片）；机检首轮不合规经复核为三类误报，机检改进并回归后两方合规；盲化出 A/B，跑独立模型盲审。

Auto-updated:
- ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/edit/blind_capcut/arms/capcut.mp4 — CapCut AI 粗剪渲染成片（Codex CLI 下载，sha256 60a84b6d…，30 fps，52.07 秒）及 capcut_stdraft.json
- ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/edit/blind_capcut/check/ — 首轮不合规原报告存 capcut_v1_failed.json；改进后 capcut.json 合规；calibration_v2_* 回归
- tools/edit_blind_test.py — check：CapCut 副本 vid 按时长归属、按草稿逐段重建声音（能量超量与草稿外声音）、画面取相邻帧与两帧平均的最小块差并要求持续才判不合规、零散超限存对比图；review 加 --dry-run
- ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/edit/blind_capcut/blind/A.mp4、B.mp4 — 盲化（承诺 514e6378…）；review/model_reviews.json — Claude、Codex 各两次
- ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/edit/blind_capcut/README.md、arms/capcut_notes.md — 状态与复核理由
- .audit/adhoc_agents/2026-11-08/capcut-mcp/README.md — 实测一节
- 删除 C:\Users\light\AppData\Local\Temp\capcut-install-d528bdb874434ec1ae8af017d1f1f018 — 插件安装临时目录（安装包下载副本，可重新下载，未备份）

验证: 复核：按草稿逐段重建声音相关最低 0.9635、能量比 0.965–1.008；零散超限帧看图确认为嘴部与炉火运动。回归：CapCut 成片叠加粉噪、0.4 秒提示音、字幕、角标均判不合规，两方与重编码合规。A/B 元数据一致。用户尚未盲看；揭盲未做
费用: CapCut 积分未知（无费用字段）

No conflicts found in: （未单独核查）


## Follow-up 046 — 2026-11-09 08:47:45
Source: user_input/follow_ups/202611.md - section 046
Summary: 揭盲并写结论：场三 CapCut 与现有流程用户分不出高下；CapCut 维持不用，不扩到整集

Auto-updated:
- ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/edit/blind_capcut/README.md（步骤 6、8 状态与结论节）；.audit/adhoc_agents/2026-11-08/capcut-mcp/README.md（盲测结果节）

验证: reveal --force 输出 A=pipeline、B=capcut，与 _key_do_not_open.json 一致；按 cut_v3.json 与 capcut_stdraft.json 逐段核对差别
费用: 无（本步不调用收费服务）

No conflicts found in: （未单独核查）


## Follow-up 047 — 2026-11-09 09:25:05
Source: user_input/follow_ups/202611.md - section 047
Summary: EP01 全集只读校验：三模块状态、资料包、63 镜出片（脸版本、prompt 版本、审核结论）、场剪辑与整集剪辑；报告 .audit/adhoc_agents/2026-11-09/chuanyue-ep01-validate/report.md

Auto-updated:
- 只读校验，未改剧内文件；报告与脚本在 .audit/adhoc_agents/2026-11-09/chuanyue-ep01-validate/（临时副本 ai_videos/chuanyue_yiri/_build/validate_1109/）

验证: episode-workflow API 三模块状态；shot_pack.py check 63 ok；逐条读 generation.json/review.md 对 prompt sha 与参考 sha；scene_cut.py check ×8、episode_cut.py check
费用: 无外部服务

No conflicts found in: EP01 由另一会话推进，本条不写其文件


## Follow-up 048 — 2026-11-09 12:19:13
Source: user_input/follow_ups/202611.md - section 048
Summary: EP01：同步资料包；63 镜按当前 prompt 与 Riley 新版（11-09）全部重出 720p 正式条（约 871 秒、约 1.74 万积分）；逐条审核；8 场重剪、整集重剪（修 s2/s8/s6 断链、s5 漏镜、s7 场尾停留），成片发用户

Auto-updated:
- 资料包同步（63 ok）；63 镜按当前 prompt 与 11-09 Riley 重出 720p：62 条已落盘（各镜 renders/20261109-*），s8 st4 首次提交网络超时未扣费、已重提；每条 _review/ 审片材料（拼图、逐词转写、motion）；审片说明 _build/rerender_1109/REVIEWER_BRIEF.md。进行中：8 场独立审片、重出不合格镜、8 场与整集重剪、发成片（完成后另记）

验证: shot_pack check 63 ok；shot_take 日志 62 条 →、0 扣费失败；审片材料逐条齐全。首批 4 位审片代理因网络 403 中断未写结论，已重启 8 位
费用: seedance2.5 720p 62 条（按 20 积分/秒估约 1.7 万积分，submit 回执逐条记 episodes/ep01/request_log.md）；余额提交前 129,612

No conflicts found in: 跳过出片前审查闸门（review_gate）用用户原话；上一轮审查单 r3 已作废，遗留 16 条次要问题未处理；EP01 先前由另一会话推进，期间无其他会话写入


## Follow-up 049 — 2026-11-09 21:08:31
Source: user_input/follow_ups/202611.md - section 049
Summary: 剧级出片规则：每个镜头最多重出一次；重出后审核仍不满意就停，不再出，剪辑用两条里较好的一条并列给用户处理

Auto-updated:
- 全仓流程：.agents/skills/ai-videos-pipeline/modules/prompts-generate.md「重试与搁置」改为每镜最多重出一次、仍不满意搁置交用户；filming-action.md、ai-videos-self-check/SKILL.md 闸门一句、CONVENTIONS Iteration bounds 加例外；本剧 README 已定表一行。用户追加「请写进流程」即同意升仓库级

验证: workflow_catalog --fix/--check：11 组 258 源编号连续；sync_agent_skills --check 通过；grep 三处源文件均含新规则
费用: 无

No conflicts found in: 取代 2026-10-11「默认 3 轮」；EP01 本轮已重出过的 7 镜按新规则不再出


## Follow-up 051 — 2026-11-10 07:04:53
Source: user_input/follow_ups/202611.md - section 051
Summary: EP01 v4：重出与复审收尾（每镜最多重出两次），8 场新剪辑与整集 v4（13:44）发用户；搁置与待处理清单

Auto-updated:
- 场剪辑 s1 v5、s2 v3、s3 v5、s4 v6、s8 v3、s5 v4、s6 v4、s7 v4；整集 edit/final/cut_v4.json → ep01_final_v4.mp4（824.5 s）；分镜改 s1 st4/s2 st3/s3 st1,5,6,7/s5 st3/s6 st6/s7 st1/s8 st2,10（经 episode-workflow API 保存、确定、编译）；首帧重出 s1 st4、s2 st3、s3 st6、s5 st3；搁置 s2 st3

验证: scene_cut check 8 场问题无（4 处幻听切点经审片核对后 word_cut_ok）；episode_cut check 无问题、join 时长对；每条采用条都有 review.md 结论；shot_pack check 63 ok；720p 四段已发用户
费用: seedance2.5 720p：首轮 63 条 + 重出 17 条（含 s5 st3 第二次重出在途）；Codex 出图首帧 4 张（多次网络失败重试，均未出图不计）

No conflicts found in: s5 st3 用占位条，第二次重出通过后换条重剪；s8 门房 st2 与 st10 不是同一张脸待用户定；s3 st8 5.2–6.2 秒、s7 st5 原声需声音模块处理


## Follow-up 050 — 2026-11-09 21:18:46
Source: user_input/follow_ups/202611.md - section 050
Summary: 全仓出片规则由每镜最多重出一次改为最多两次（第三条起不出，搁置交用户）；EP01 已搁置的 s1 st4、s2 st3 恢复，按审核建议改上游后出第二次

Auto-updated:
- 全仓流程改为每镜最多重出两次：prompts-generate.md「重试与搁置」、filming-action.md、ai-videos-self-check/SKILL.md、CONVENTIONS Iteration bounds 例外、本剧 README 已定表；EP01 按新规则：s1 st4、s2 st3 恢复第二次重出（s1 st4 通过，s2 st3 搁置）

验证: workflow_catalog --check 11 组 258 源编号连续；sync_agent_skills --check 通过；五处源文件 grep 含「最多重出两次」
费用: 无（规则改动）

No conflicts found in: 取代同日 049 的「一次」


## Follow-up 052 — 2026-11-10 07:11:12
Source: user_input/follow_ups/202611.md - section 052
Summary: s5 st3 第二次重出审核（银色钱已解决，付错成金币→搁置）；s5 场剪辑 v5、整集 v5；更新的 s5 发用户

Auto-updated:
- s5 st3 review.md（搁置）、scenes/s5/edit/final/cut_v5.json→s5_final_v5.mp4、edit/final/cut_v5.json→ep01_final_v5.mp4（824.5 s）

验证: 3.0/5.5/7.0 秒全分辨率看钱：无银色钱，付的是金黄大币；s5 渲染时长对；整集 join 时长对；s5 已压 720p 发用户
费用: seedance2.5 720p 1 条（s5 st3 第二次重出）；Codex 首帧 1 张

No conflicts found in: 搁置镜：s2 st3（光向反）、s5 st3（付错钱）交用户


## Follow-up 053 — 2026-11-10 08:40:57
Source: user_input/follow_ups/202611.md - section 053
Summary: 诊断 s1→s2 接口、s2 女人与裤子梗、s3 Felix 听话时定格的根因与漏审环节；提出流程与审查改进方案（写作规则、出片前/出片/剪辑审查新维度、自动检测、缺陷回流）及 EP01 修复计划，待用户选

Auto-updated:
- 只出方案，未改文件；诊断依据：filming.json s2 st5/st7/st8、s3 st4 节拍，s1/s2 场剪辑接口，review_roster.json 各阶段法则

验证: 逐镜读节拍：s3 st4 Felix 在 Riley 8–17 秒独白期间无任何动作；s2 st5/st7 写了「一动不动」「就那样盯着看」共约 4 秒；裤子梗在 s1 st5、s2 st5–st8 重复出现；s2 开场接的是搁置镜 st3 的 2.5 秒；本轮出片审核按 REVIEWER_BRIEF 只查硬错，场剪辑/整集未开 cut、episode 审查单
费用: 无

No conflicts found in: 方案待用户选；升仓库级规则须用户同意


## Follow-up 054 — 2026-11-10 09:11:09
Source: user_input/follow_ups/202611.md - section 054
Summary: 落实表演自然度方案：全仓流程加「人不定格 / 听者有活 / 一个梗一次」写作规则、审查名册人物逻辑加 C8 听者 C9 像真人、出片审核加表演一节与人物静止检测、剪辑与整集审完才发；本剧加 qc_checks 与用户缺陷；EP01 改 s3 st4、s2 裤子梗（四镜并两镜）、s1 st5、s1→s2 接口并重出重剪

Auto-updated:
- 全仓：filming.md「画面里的人不定格」；prompts-generate.md 审核「表演」一节；edit.md「场剪辑、整集审完才发」；review_roster.json 人物逻辑 C8/C9、观众 A7、cut/episode 阶段加人物逻辑；新工具 tools/filming_lint.py、tools/person_motion.py（opencv-python-headless 4.x）；tools/qc_review.py 镜头条以 prompt.txt 作规格。本剧：qc_checks.toml（filming.no_freeze、video.person_still、video.acting_natural）、3 条用户缺陷（qc.py defect）。EP01：分镜改 s3 st4、s2 st5/st8（删 st6/st7）、s1 st5，首帧重出 s2 st8；重出 s1 st5、s2 st5、s2 st8×2、s3 st4×2；场剪辑 s1 v7、s2 v5、s3 v6；整集 cut_v7 → ep01_final_v7.mp4（803.6 s），四段发用户

验证: filming_lint 在旧分镜报出 Felix 段；person_motion 在旧条报 Felix 静止 10.3 s、新条只 2.3 s；qc_review 独立审稿（s1 st5、s2 st5 acting_natural 未过，列给用户放行）；整集观众审 v6：7 接口 6 过，按意见改 s1 结尾/s1→s2 硬切/s2 收短后 v7 自查接口；scene_cut、episode_cut check 无问题；workflow_catalog、sync_agent_skills --check 通过
费用: seedance2.5 720p 6 条（s1 st5、s2 st5、s2 st8×2、s3 st4×2）；Codex 首帧 1 张；独立审稿 codex/claude 调用若干

No conflicts found in: s2 st8 已用满两次重出，包袱处女人不再抬头看（观众审指出）列给用户；s2 st5、s1 st5 独立审稿未过待用户放行


## Follow-up 055 — 2026-11-10 19:21:03
Source: user_input/follow_ups/202611.md - section 055
Summary: st1 低声惊叹（他拍固定全景）直接跳到 st2 欢快自拍开场，画面和台词都断。st1 结尾改为她边说 'Wait, wait — I gotta do this right.' 边走向架在沙滩上的相机、伸手拿起（手掌挡满画面），接 st2 自拍重新开场；st1 18→22 秒，st2 不改。桥接句经独立母语听感审查（Sonnet）选定

Auto-updated:
- story.json/story.md v2.4、filming.json s1 st1（22 s）、st1 overhead.toml、prompts 重编译（draft）、资料包 sync

验证: 独立 Sonnet 母语听感审查选定桥接句；shot_overhead 重出 st1；shot_pack check ok 61；scene_board s1 刷新；st1 视频待用户点头重出

No conflicts found in: （未单独核查）


## Follow-up 056 — 2026-11-10 19:28:42
Source: user_input/follow_ups/202611.md - section 056
Summary: 镜间接点（上一镜结尾↔下一镜开头）进流程与验证：写作规则（filming.md「镜与镜接得上」、story-structure.md「台词跨镜头接着说」）、机检 tools/shot_junctions.py、审查单材料 junctions.md 与出片后 <场>_junctions.md、名册 K8/K9/D7/N10 与 cut 阶段加台词、edit.md 场剪辑逐接点连听、剧级 qc 三项与用户缺陷

Auto-updated:
- .agents/skills/ai-videos-pipeline/modules/{filming,story-structure,edit}.md、.agents/references/project/review_roster.json（K8/K9/D7/N10、cut 阶段加 dialogue）、tools/shot_junctions.py（新）、tools/review_run.py（materials/junctions.md、<场>_junctions.md）、tools/tests/test_shot_junctions.py、ai_videos/chuanyue_yiri/qc_checks.toml（3 项）、qc defect

验证: shot_junctions 在改前 filming 上只报 s1_st1→st2（3 条 ⚠），改后 0 ⚠；新增测试 3/3；tools 测试 test_review_run/qc/qc_review 57 passed；app 测试 test_process_qc/test_review_run_api 10 passed；sync_agent_skills --check、workflow_catalog --check 通过；独立审稿人用新标准审 EP01 全部接点进行中

No conflicts found in: （未单独核查）


## Follow-up 057 — 2026-11-10 19:36:57
Source: user_input/follow_ups/202611.md - section 057
Summary: 独立审稿人按 K8/K9/D7/N10 审 EP01 全部 60 个接点：58 ✓ 2 ✗（s5_st2→st10 手指数跳、s7_st7→st1 同一口气演两遍），17 个视角切换提示全部可接受；指出 bible 没定义「他拍」是什么，补 bible §2「视角约定」一行，作为 ℹ 的判据

Auto-updated:
- ai_videos/chuanyue_yiri/bible.md §2 视角约定

验证: 独立审稿人（Opus，全新上下文）接点审查报告；两处 ✗ 未改，待用户决定

No conflicts found in: （未单独核查）


## Follow-up 058 — 2026-11-10 20:06:30
Source: user_input/follow_ups/202611.md - section 058
Summary: 根因：分镜没写看点、撑看点的水只写了「一道浅浅的水」、首帧就没水、动作时长给宽、审核写「Vision 给出了」放行。流程：分镜加可选字段 point（只给审查、不进 prompt）；filming.md 加「每镜写看点，画得出来，按真实速度演」；名册 P9 效果有来源、P10 真实速度、F8 看点画得出来、A8 看点落地；出片审核加「看点」一节（先盲写再对照）；filming_lint 报缺看点；剧级 qc 三项与用户缺陷。EP01：s2 st1 重写（7→5 秒、满街浑水、真实速度、菜叶漂过）与 st2 路面同步，两张首帧重画；60 镜看点由独立代理起草写入

Auto-updated:
- projects/ai_video_management entity（point 可选字段）+测试；tools/review_run.py（spec 看点行、SPEC_FIELDS）；tools/filming_lint.py（缺看点）；filming.md、prompts-generate.md；review_roster.json P9/P10/F8/A8；qc_checks.toml 三项；EP01 filming（s2 st1/st2、60 镜 point）、s2 st1 overhead、s2 st1/st2 首帧（_r6_before 归档）

验证: app test_episode_workflow 68 passed；tools 测试 269 passed；point 写入后 61 条 prompt md5 不变；shot_pack check ok 61；filming_lint 只剩 054 规则的 7 处旧问题；st2 新首帧脸部放大对比无雀斑

No conflicts found in: （未单独核查）


## Follow-up 059 — 2026-11-10 20:45:43
Source: user_input/follow_ups/202611.md - section 059
Summary: EP01 按新检查修 15 镜分镜：看点画得出来（s1_st3 补痕、s2_st3 满街浅水、s5_st4 鱼露落在浅色断面、s7_st1/st2 灯上方涂鸦、s8_st9 刮出哑光一道、s2_st5 看点改由下一镜点明、s5_st6 反应改合理）、真实速度（s4_st4、s6_st4、s8_st1）、人不定格（s1_st3、s3_st8、s5_st7、s5_st8、s8_st9 Helvia）、接点（s5_st10 接一根手指、s7_st1 不重演舒气）；6 张首帧重画；流程：shot_take submit 先跑剧级登记的分镜机检（--skip-checks 用户原话）、scene_cut render 正片剪辑逐条查 qc gate（--skip-gate 用户原话）、prompts-generate.md 审完 qc.py record、edit.md 同步；待重出 17 镜 242 秒

Auto-updated:
- EP01 filming 15 镜、s4_st4/s6_st4/s8_st1 overhead、6 张首帧（_r7_before 归档）；tools/shot_take.py、tools/scene_cut.py、tools/tests/test_submit_filming_checks.py；prompts-generate.md、edit.md

验证: filming_lint 通过；shot_junctions 0 ⚠；shot_pack check ok 61；scene_board 7 场刷新；tools 测试全过（+2 新）；filming_checks 模拟缺看点被拦、scene_cut s1 cut_v7 因无 qc.json 被拦；首帧逐张目检（s7 第一版像通风口重出）

No conflicts found in: （未单独核查）


## Follow-up 060 — 2026-11-10 21:41:05
Source: user_input/follow_ups/202611.md - section 060
Summary: 17 镜 720p 重出（9 路并行）；独立审稿 qc_review 全部判闸门不过——修两处审稿工具：motion_check 拼图按片长全覆盖（原 8×8 只到 16 秒，长镜结尾一律拿不准判 fail）、qc_review 给导演视角附分镜 point；42 条旧条按原审核补记 qc（新检查项记未审）；场剪辑 s1 v8 s2 v6 s3 v7 s4 v7 s5 v6 s6 v5 s7 v5 s8 v4 与整集 v8（815.7 秒）按用户原话 --skip-gate 渲染，闸门问题随片交用户

Auto-updated:
- 17 条 renders（review.md、qc.json、annotation.json）、42 条旧条 qc.json、8 个场剪辑决定与成片、整集 cut_v8 与 ep01_final_v8.mp4；tools/motion_check.py、tools/qc_review.py

验证: 17 条全部下载；场剪辑 8 场时长对、无黑段；整集 815.7 秒切点对账一致（末段叠化/夜景 4 处未检出属正常）；s1 st1→st2 接点抽帧确认手掌挡镜后切自拍；tools 测试通过

No conflicts found in: （未单独核查）


## Follow-up 061 — 2026-11-14 10:05:36
Source: user_input/follow_ups/202611.md - section 061
Summary: 流程：story-structure.md 加「故事点清单（先审点，再写稿）」——集目录 story_beats.md，每点一行按时间顺序、标抓人强/中/弱、每节点 2–3 个备选、用户挑完再写稿；名册 audience A9 故事点抓人。EP01：写出 41 个故事点审查稿与备选（最弱：清晨街景与正午到浴场；最大漏项：维苏威火山的倒计时），待用户挑

Auto-updated:
- story-structure.md、review_roster.json（A9）、EP01 story_beats.md

验证: 41 点按 story.md 时间顺序逐一对照；新备选标明未进考据的先补考据

No conflicts found in: （未单独核查）


## Follow-up 062 — 2026-11-14 10:43:50
Source: user_input/follow_ups/202611.md - section 062
Summary: 根因：①为情节需要硬写人物举动（头也不抬、不指方向），审查只核对是否照规格、接受分镜替人物写的心理理由；②跨语言交流无人审（母语听感只看英文自然度）；③054/059 的「人不定格」被执行成给配角加表情和整镜反应，检查只罚静止不罚过演。流程：filming.md「动机来自人物，反应要克制，跨语言要说清」、story-structure.md「情节靠人物，不靠硬写」、名册 C10/C11/D8、filming_lint [动机][过演][跨语言]（只查配角、喊话与带手势的问句不报）、shot_take 提交前跑、剧级 qc 三项与三条用户缺陷、测试；EP01 story_beats 节点 15/15b 给备选待用户挑

Auto-updated:
- filming.md、story-structure.md、review_roster.json、tools/filming_lint.py、tools/shot_take.py、tools/tests/test_filming_lint_motive.py、ai_videos/chuanyue_yiri/qc_checks.toml、EP01 story_beats.md

验证: EP01 机检报 13 处（s3 st1/st4/st6 与 s5 st13 已按手势豁免排除）；新测试 4 passed；qc defect 三条

No conflicts found in: （未单独核查）


## Follow-up 063 — 2026-11-14 10:59:50
Source: user_input/follow_ups/202611.md - section 063
Summary: 新审查类「角色立场」(review_roster role，V1 语言 V2 肢体 V3 表情 V4 视线 V5 回应 V6 动机)：partition=cast，每个出场有卡人物一位审稿人（路人合一位），Claude/Codex 双审，进 pregen/filming/take/episode/full；review_run 生成 materials/roles/<人物>.md 第一人称材料（他出现的每一镜原文）；qc_review 出片后角色视角加同样的逐拍自问；filming.md「每个角色自己走一遍」、story-structure.md 同名一行（写作者先自己换位走一遍，拿不准用人物即兴）

Auto-updated:
- .agents/references/project/review_roster.json、tools/review_run.py、tools/qc_review.py、tools/tests/test_review_run.py、filming.md、story-structure.md

验证: EP01 实测：cast_map 得 Riley/Felix/Tertius/Asellina/Fortunata/Vibia/Helvia/路人 8 个角色；pregen 审查单生成 role_c1…role_c7、role_extras；roles 材料逐镜原文；tools 测试 273 passed；app 测试通过

No conflicts found in: （未单独核查）


## Follow-up 064 — 2026-11-14 11:15:57
Source: user_input/follow_ups/202611.md - section 064
Summary: 角色立场审稿人加跨集一致：人物目录 behavior.md 行为档案；review_run roles 材料附行为档案路径与「前几集的你」（前几集该人物出现的每一镜台词与动作开头）；名册 role 加 V7 跨集一致，报告末尾写「行为档案增补」，收轮后并进 behavior.md；filming.md 同步

Auto-updated:
- tools/review_run.py、review_roster.json（V7）、filming.md

验证: 语法检查通过；EP01 是第一集无前集，V7 从 EP02 起生效；EP01 行为档案由本轮角色立场审查的增补建立

No conflicts found in: （未单独核查）


## Follow-up 065 — 2026-11-14 11:59:08
Source: user_input/follow_ups/202611.md - section 065
Summary: 审稿由 Claude＋Codex 双审改为 Claude 单审：名册每类只留 a 位（母语听感用 Sonnet，与写台词的 Opus 拉开）；review_run 单审直接按 a 位定分、无对比无裁决，tick 单审不必写 --slot，新增 drop-slot 把进行中的审查单改单审；本轮 pregen 停掉 21 个 Codex 位；管理 UI 无 b 位时不画 b 列；SKILL.md、prompts-generate.md、名册说明同步；测试用双审名册副本保留对比/裁决用例，新增单审用例

Auto-updated:
- review_roster.json、tools/review_run.py、tools/tests/test_review_run.py、tools/tests/conftest.py、ReviewV5.tsx、SKILL.md、prompts-generate.md

验证: tools 测试 275 passed；app review_run_api 6 passed；UI tsc 通过、vitest 227 passed；本轮审查单 drop-slot 后 20/21 完成

No conflicts found in: （未单独核查）


## Follow-up 066 — 2026-11-14 12:37:57
Source: user_input/follow_ups/202611.md - section 066
Summary: 剧级登记表按两层标注，跟随仓库级自检闸门改版

Auto-updated:
- ai_videos/chuanyue_yiri/qc_checks.toml — 13 条标 layer（point_written、point_visible、point_landed、no_cross_ref 为 spec，其余 quality）；video.point_landed 写容差：只问关掉声音能否说出 point 的意思，动作层次与秒数不在此项判

验证: 见 dota_yingxiong 354：tools 测试 282 passed；对本剧 s3 st4 实条 qc_review --dry-run 与 qc.py gate 核对通过

No conflicts found in: 注意：本剧 qc_checks.toml 的 filming.no_cross_ref 在本条分配前已写 sources「chuanyue_yiri#066」（另一会话先写号后分配），与本条撞号，需那个会话改成它实际分到的号


## Follow-up 067 — 2026-11-14 14:13:46
Source: user_input/follow_ups/202611.md - section 067
Summary: EP01 出片前全量审查 r1（Claude 单审 21 项，含 8 位角色立场审稿人）共 143 问题（严重 42、主要 24）；8 个修复代理按场改分镜文字与 overhead，主会话合并（60 镜 890 秒，删 s3_st6），面包房按 15B/15b A；28 张首帧局部重画（2 张重做后合格）；故事稿 v2.5 同步；bg2 场景卡满街浑水；Felix/Fortunata 人物卡、p3 道具卡、负面词更新；工具：figure_colors 改按卡号固定（俯视图与 prompt 人物色不再对反）、filming_lint 加 [跨镜]、shot_take 提交前跑；filming.md「镜与镜接得上」改写；66 个严重/主要问题登记 fix（I61 开价、I21 山的写法待用户定）；开 r2 复审

Auto-updated:
- filming.json/story.json/story.md、各镜 overhead 与首帧（_r8_before 归档）、bg2 场景卡、c2/c5 人物卡、p3 道具卡、workflow.json 负面词、tools/episode_shots.py、tools/filming_lint.py、tools/shot_take.py、filming.md、qc_checks.toml、review r1 fixes/

验证: 编译通过（两镜 prompt 精简到 5000 字内）；filming_lint 通过；shot_junctions 0 ⚠；shot_overhead --all 无错；shot_pack check ok 60；首帧逐张前后对比核对；tools/app 相关测试通过；r2 复审进行中

No conflicts found in: （未单独核查）


## Follow-up 068 — 2026-11-14 15:13:49
Source: user_input/follow_ups/202611.md - section 068
Summary: r2 复审（Claude 单审）严重 10、主要 23；8 场按 r2 修复（修复代理用 check_patch 自检 PASS 后交稿，首帧按场流水线出图）；用户定：山不入画（bible §9、bg1 卡、负面词、s1 首帧去山、故事点 1B/4A/41A 不采用）、女店主竖四指 Quattuor.、浴场换上亚麻浴巾（新换装阶段 c1-1_浴场裹布 卡与三视图，删全部穿衣梗）、s1 st4 拆成 st4+st6（主会话定）；编译器：换装阶段卡「Shot prompt 外观」优先、prompt 长度计入资料包「图片N」；约 33 张首帧重画（s7 st2 改文字配图、s7 st5 删远处行人、s4 st4 改图丢了十字路口退回原图）；故事稿 v2.6；开 r3

Auto-updated:
- filming.json/story.json/story.md、各镜 overhead 与首帧（_r9_before 归档）、c1-1_浴场裹布、bible §9、bg1 卡、workflow.json 负面词、story_beats、libs 编译器与资料读取、review r2 fixes/

验证: app 测试 test_episode_workflow 68 passed、materials 相关 70 passed；编译通过；filming_lint、shot_junctions 0 ⚠；shot_overhead --all 无错；shot_pack check ok 61；首帧逐张核对；r3 复审进行中

No conflicts found in: （未单独核查）


## Follow-up 069 — 2026-11-14 16:21:11
Source: user_input/follow_ups/202611.md - section 069
Summary: 第 3 轮（最后一轮）出片前审稿（Claude 单审，critical 10 / major 21）后按场修复：分镜文字、overhead、首帧局部重画 23 张提升 22 张（s3 st8 退回旧图）；负面词去掉「火山」只留「远山、任何山」，bg1 底图去山；review_run.py conclude 新增 --accept-fixes，最后一轮按修复后的材料收轮并标明修复未经独立复审、交用户出片前审。

Auto-updated:
- tools/review_run.py（conclude --accept-fixes）、tools/tests/test_review_run.py、ep01 filming.json / story.json / prompts.json、61 镜 overhead 与资料包、22 张首帧（_r10_before 存档）、workflow.json 负面词、bg1 底图、reviews/ep01_20261114-151333_pregen_r3（fixes/、结果.md）

验证: test_review_run.py 33 passed（含新测试 accept_fixes）；filming_lint、shot_junctions 0 ⚠；shot_overhead --all blocker 0；shot_pack check ok 61；scene_board --check 最新；r3 已收轮且材料未变

No conflicts found in: 只改本剧 ep01 与 review_run conclude 新开关，不动其他剧


## Follow-up 070 — 2026-11-14 20:34:46
Source: user_input/follow_ups/202611.md - section 070
Summary: 接续 11-14 分诊重出的 21 镜：逐条作者审核与闸门补记、选条、s3–s8 新场剪辑（s3 v8 s4 v8 s5 v7 s6 v6 s7 v6 s8 v5）、整集 v9；s1/s2 旧条按现行规则独立重审；开出片后（s3–s8）与整集审查单派独立审稿；重出与搁置清单交用户定

Auto-updated:
- 21 条 review.md / qc.json / annotation.json；s1/s2 六条旧条 qc 重审；s3 cut_v8、s4 cut_v8、s5 cut_v7、s6 cut_v6、s7 cut_v6、s8 cut_v5 及成片；整集 edit/final/cut_v9.json、ep01_final_v9.mp4；审查单 reviews/ep01_20261114-202704_take_r1、ep01_20261114-202947_episode_r1（已收轮）

验证: scene_cut check/render 六场时长对、无黑段、未用 --skip-gate；episode_cut check 无问题、join 768.9s（s5 段内检出切点比预期早约 4 帧）；两张审查单 gate 通过并收轮：出片 严重32/主要27、整集 严重23/主要13，均不可交付

No conflicts found in: 只改本剧 ep01 剪辑与审查产物，未改分镜、prompt、规则源，未提交生成


## Follow-up 071 — 2026-11-14 22:03:32
Source: user_input/follow_ups/202611.md - section 071
Summary: 重出 v9 缺的 4 镜（s3 st8、s4 st4、s6 st1、s7 st2，共 1440 积分）：s3 st8、s4 st4 保留并补进 s3 v9、s4 v9 与整集 v10；s6 st1 一镜内场景硬切、s7 st2 人脸仍不是 Riley，判重出，建议先改上游再过出片前审查

Auto-updated:
- 4 条新条 review.md / qc.json（qc_review 独立审）；s3 cut_v9、s4 cut_v9 及成片；edit/final/cut_v10.json、ep01_final_v10.mp4

验证: shot_take submit 4 条 success；qc_review：s3 st8、s4 st4、s7 st2 闸门过，s6 st1 不过；s7 st2 人脸与立绘、s7 st1 并排比对不上；scene_cut check/render 无问题、时长对、无黑段、未跳闸门；episode_cut check 无问题、join 800.2s
费用: Seedance 1440 积分

No conflicts found in: 只改本剧 ep01 出片与剪辑产物


## Follow-up 072 — 2026-11-14 23:56:51
Source: user_input/follow_ups/202611.md - section 072
Summary: s6 st1 改中景双人一个景别到底、四指与 st2 统一且手心朝镜头、打量挪到走近时、行人换样子错开 Riley；s7 st2 首帧改正脸（侧脸首帧是人脸跑偏主因）、衬衫素色、划痕变浅、窗洞去蓝光、台词节拍重排；c5 人物卡外观句、bible §9 旧山句作废；出片前审查 s6/s7 三轮（r1 严重7主要9、r2 严重5主要13、r3 严重3主要8，均已处理），r3 --accept-fixes 收轮可出片，待用户确认

Auto-updated:
- filming.json（s6 st1、s7 st2）、prompts.json、两镜 overhead 与首帧（_r11–_r14 存档）、c5_Fortunata.md、bible.md §9、s6/s7 资料包与场故事板；reviews/ep01_20261114-230732_pregen_r1、232708_pregen_r2、234201_pregen_r3

验证: 编译通过（s6 st1 压到 5000 字内）；shot_pack sync 13 镜更新；filming_lint 通过；shot_junctions 60 接点 0 ⚠；shot_overhead --all blocker 0；首帧每版看图验收；s6/s7 其余已出片镜中 s6 st2 因人物卡句子改动 prompt 变了（保留原条不重出）
费用: Codex 出图 6 张（订阅额度）；未调 Seedance

No conflicts found in: 只改本剧 ep01 两镜及其人物卡、bible 一句

