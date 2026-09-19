# 《时空旅行》系列 · 变更日志（系列级）

## Follow-up 001 — 2026-09-13 14:41:00
Source: user_input/follow_ups/202609.md - section 001
Summary: 立项前调研以 11 份已完成报告为准，跳过卡住的 F7 / D1 两个角度；提案落盘。

Auto-updated:
- ai_videos/shikong_lvxing/proposal.md — **新建**：§0 十二个待拍板决定 + A 系列公式（十二条不变量 / 记者人设 / 10:30 单集骨架 / 五固定栏目 / 元素预算 / 20 条趣味元素 / 教育机制）+ B 第一季 12 站片单 + C 前三站概念卡 + D 每站史料调研 SOP（15 节 dossier / 三级史实标签 / K-F1–F6 机检）+ E 合规 + F 调研证据（12 条读数 + 12 条断言核实）+ G 流水线对接
- ai_videos/shikong_lvxing/series.json — **新建**（slug 暂定 shikong_jizhe、prefix 暂定 zg，待决定 1）
- specs/ai_video/shikong_lvxing/user_input/{raw_prompt,revised_prompt}.md — 新建

Pending user decision（未擅自改动任何 skill / agent_refs）:
- 决定 1–12 见 proposal.md §0；其中决定 7（阶段 0 史料调研 + K-F 机检）是仓库级规则变更，需批准后才改 `ai_videos__全流程编排` / `ai_videos__格式契约` / `ai_video.md`

No conflicts found in: huangye_shenghuo/*, hy1–hy3/*（本次未改动任何既有剧）

## Follow-up 002 — 2026-09-13 19:25:00
Source: user_input/follow_ups/202609.md - section 002
Summary: 系列名《时空旅行》/ 前缀 sk / 旅行者名册 / 双语同画面中文先汴京英文先罗马 / 16:9 约 10 分钟。

Auto-updated:
- ai_videos/shikong_jizhe → ai_videos/shikong_lvxing — 目录改名（同步 specs/ai_video/ 目录）
- ai_videos/shikong_lvxing/series.json — name_zh 时空旅行、slug shikong_lvxing、episode_prefix sk
- ai_videos/shikong_lvxing/proposal.md — §0 决定 1–4 标「已定」；A §3 改写为「旅行者名册」（共用人设骨架 + T1–T4 名册草案 + 五样恒定符号承担识别度）；C 三张卡各加「旅行者」行；G 目录 / voice_id / 开工顺序同步；全文 zg → sk
- specs/ai_video/shikong_lvxing/user_input/revised_prompt.md — 重生成

Pending user decision: proposal.md §0 决定 5–12；英文系列名（建议 Posted to the Past）

No conflicts found in: huangye_shenghuo/*, hy1–hy3/*

## Follow-up 003 — 2026-09-13 19:32:00
Source: user_input/follow_ups/202609.md - section 003
Summary: 镜长约 20 s / 首尾易拼接零剪辑 / 逛城市一镜到底 / 体验衣食住行。

Auto-updated:
- ai_videos/shikong_lvxing/proposal.md — §0 追加「已定 13–16」表；A §2 新增不变量 I-13（镜长 + 切口 + 一镜到底）；A §4 站一改「住 + 穿」、站三加一镜到底穿街长镜、站六改「住 · 客栈晚饭」、镜数从 80–110 改为 28–34、新增「镜数与镜长」段；A §7 元素 21/22；B §3 核对清单加三项；C 三张卡加「一镜到底」行；G §2 第 4 行、§3 第 1 条、§4 生成器字段（dur / onetake / jb 机检）同步
- specs/ai_video/shikong_lvxing/user_input/revised_prompt.md — 重生成

No conflicts found in: huangye_shenghuo/*, hy1–hy3/*（本条与仓库既有「硬切 + 景别跳档」「一个地点 + 一个状态 ＝ 一镜」规则一致，无需改 CLAUDE.md）

## Follow-up 004 — 2026-09-13 19:40:00
Source: user_input/follow_ups/202609.md - section 004
Summary: 资产建立前先做大量参考图 research；scenes / props 下下载历史图片做 reference；一镜到底走 Blender 建城 + previz 视频参考。

Auto-updated:
- ai_videos/shikong_lvxing/proposal.md — §0 追加「已定 17–19」；A §2 I-13 加 Blender 一镜到底条款；D §6 第 4 步改为「建参考图库（≥ 8 张 / 资产 + refs.md）」；B §3 核对清单加一项；G §5 加第 5、6 条；新增 G §7「参考图库」（目录结构 / refs.md 字段 / `tools/ref_fetch.py` 规格）与 G §8「一镜到底的 Blender 工作流」（含与 rule 4d ① 的关系说明）
- specs/ai_video/shikong_lvxing/user_input/revised_prompt.md — 重生成

Pending: `tools/ref_fetch.py` 尚未实现（待决定 7 / G §5 批准后与阶段 2 一起建）；一镜到底工作流的 divergence 在开 sk1 时登记 `specs/ai_video/sk1/divergence.md`

No conflicts found in: huangye_shenghuo/*, hy1–hy3/*

## Follow-up 005 — 2026-09-13 20:05:00
Source: user_input/follow_ups/202609.md - section 005
Summary: 第二轮拍板——结尾不固定、每站独立、只定 sk1、城市建立加俯视排版图、批准阶段 0 与 ref_fetch。

Auto-updated:
- ai_videos/shikong_lvxing/proposal.md — §0 决定 5–12 标已定 + 第二轮拍板表；A §2 I-6/I-8/I-12 改写；A §3 名册措辞；A §4 第 9 段降可选、第 10 段去下站预告；A §5 收②可选、收③改考证卡；A §6 删「跨站轻线索」；A §7 元素 20 改写；A §8 第 6 条改写；B 改候选池（只 sk1 定）+ §2 重写；C 标题与 sk2/sk3 卡改候选；G §5 标已批准、§6 收尾句、§8 加「城市建立五步」与 rule 4g ② divergence 说明
- specs/ai_video/shikong_lvxing/user_input/revised_prompt.md — 重生成

Next（已批准、待落地）: ① `ai_videos__全流程编排` 增阶段 0 playbook；② `ai_videos__格式契约` 增 K-F1–F6；③ `ai_video.md` 增史实标签规则；④ `tools/ref_fetch.py`；⑤ 开 sk1 阶段 0

No conflicts found in: huangye_shenghuo/*, hy1–hy3/*

## Follow-up 005（落地记录）— 2026-09-13 20:30:00
Source: user_input/follow_ups/202609.md - section 005（决定 3 / 9 批准项）
Summary: 阶段 0 与史实标签机检落进仓库；ref_fetch 工具建好并实测。

Auto-updated（仓库级，只对声明「史料驱动」的新项目生效，不回溯旧剧）:
- CLAUDE.md — AI 短剧 pipeline 表加「0 史料调研（条件触发）」行
- .claude/skills/ai_videos__全流程编排/SKILL.md — 六阶段表加阶段 0 行；项目目录树加 `0_research/dossier.md`
- .claude/skills/ai_videos__全流程编排/playbooks/ai_videos__stage0_史料调研.md — 新建（提问清单 / SOP 7 步 / 15 节模板 + YAML fact / QC 关卡）
- .claude/skills/ai_videos__格式契约/SKILL.md — 新增 K34（史实标签 K-F1–F6 + refs.md / 许可入画）
- .claude/agent_refs/project/ai_video.md — 新增 rule 17（阶段 0 / 三级标签 / 参考图库 / 双语 voice_id / 锁定串「不是 X」）
- tools/ref_fetch.py — 新建：`search`（Met + Commons，免 key）/ `pull`（下载到 `ref/` + 写 `refs.md`，登记许可）/ `register`（手动下载的图）；实测 Commons 与 Met 均可搜可下
- ai_videos/shikong_lvxing/proposal.md — G §5 / §7 标「已落地」

No conflicts found in: huangye_shenghuo/*, hy1–hy3/*（阶段 0 为条件触发，旧剧不受影响）

## sk1 阶段 0 回写 — 2026-09-13 21:50
Source: sk1/0_research/dossier.md §0 ②（冲突裁定）
Summary: 概念卡 C §sk1 按史料校正八行；系列公共库 `_series/{sources.md, blacklist.md, glossary.md}` 由 sk1 阶段 0 建立。

Auto-updated:
- ai_videos/shikong_lvxing/proposal.md — C §sk1 卡：当天大事 / 任务障碍 / 一日时间线 / 三位受访者 / 我试试 / myth bust / 本站存疑 / 一镜到底 + 末行校正记录
- ai_videos/shikong_lvxing/_series/{sources.md, blacklist.md, glossary.md} — 新建（W5 / W6）

No conflicts found in: A / B / D–G 各章（路线纠正只影响 sk1 卡；A §4 站一已是「在当地住处醒来」，无冲突）

## Follow-up 006 — 2026-09-14 00:05:00
Source: user_input/follow_ups/202609.md - section 006
Summary: 自主模式——sk1 不停顿跑到出 prompt；疑问自决并记「判断：」。
Auto-updated: specs/ai_video/shikong_lvxing/user_input/revised_prompt.md — 重生成

## Follow-up 007–010 — 2026-09-14 08:54:27（进行中）
Source: user_input/follow_ups/202609.md - sections 007, 008, 009, 010
Summary: 007 自主跑完剩余工作；008 当地人不开口、只有旅行者对镜自述；009 节目形态＝外来游客全开放带逛（城市面貌 / 吃 / 住过夜 / 娱乐 / 穿 / 人的活动 / 当天大事 / 医馆·官府·皇宫·文人），10–15 分钟；010 每站开场航拍式长镜扫全城，整城 Blender 建模 + 白模动画作 Seedance 参考，写城市建模说明。

Auto-updated:
- ai_videos/shikong_lvxing/series.json — description 改为游览形态
- specs/ai_video/shikong_lvxing/changelog.md — 标题由暂定名《驻古记者》改为《时空旅行》
- ai_videos/shikong_lvxing/proposal.md — §F.10 更新、新增 §F.12（F7 受众变现 + D1 Horrible Histories 补跑）；A / B / C / D §4 / E / G 按 008–010 重写进行中，G §8 写整城建模说明
- ai_videos/shikong_lvxing/sk1/* — 见 `specs/ai_video/sk1/changelog.md` 同日条目

No conflicts found in: huangye_shenghuo/*

## Follow-up 008–010 落地记录（系列级）— 2026-09-14 09:35:32
Source: user_input/follow_ups/202609.md - sections 008, 009, 010

Auto-updated:
- ai_videos/shikong_lvxing/proposal.md — **A / B / C / D §4 行 12 / E / G 重写为游览形态**（P_series）：不变量 13 → 15 条（新增 I-14 航拍开场、I-15 默认有权限守规矩）；A §4 游览骨架（10 / 15 分钟两档）；A §5 固定栏目 ① 今日逛单 ② 穿搭检查 ③ 一口一问 ④ 跟着一个人 ⑤ 我以为 · 踩坑 + 口令件「听着像编的，但这是真的」；A §7 元素 27 条；C §sk1 改为指向 `sk1/1_立项/concept.md` 的指针卡；G §8 **整城建模说明**（Claude + Blender + Hyper3D + Cascadeur 分工与步骤、用户待办清单）；采纳 §F.12 建议 1–6、8。随后父级补改 D §3 / §4 / §6 与 §F.12 残留的「记者踩坑 / 当地人纠正 / 记者会问什么」措辞
- ai_videos/shikong_lvxing/_series/blacklist.md — 汴京站 K01–K16 → **K01–K45**：K17–K24 开封府 / 宫城（W8）、K25–K33 医馆（W7）、K34–K45 客店过夜 / 作息（W10）
- ai_videos/shikong_lvxing/_series/characters/c1_林问/c1_林问.md — 按游览形态回改（S2_series_c1）：12 维灵魂、说话风格只对镜、三件不变物措辞与 p3 逐字一致、耳后铜片不再是翻译器
- .claude/agent_refs/project/ai_video.md rule 17.2 — 口播义务主语改「记者 / 旅行者」

No conflicts found in: huangye_shenghuo/*

## Follow-up 011 — 2026-09-14 12:49:22
Source: user_input/follow_ups/202609.md - section 011
Summary: 高风险问题也由 Claude 自行决定（用户离开约 8 小时）。

Auto-updated:
- specs/ai_video/shikong_lvxing/user_input/revised_prompt.md — 重生成

Decisions recorded（判断）:
- 本地 git commit 照做，范围只含本系列与其规则 / 工具改动（不含 hy4、即梦桥接、index-tts 与临时文件）；资产 pre-commit hook 同步参考图与白模动画到 R2
- 不执行 `git push` 到远端：用户从未要求，推送出去无法撤回
- 即梦锚点图不代为出图：桥接服务规定扣积分必须用户本人在本地网页确认，自动化点击有封号风险

No conflicts found in: huangye_shenghuo/*

## Follow-up 012 — 2026-09-15 21:21:22
Source: user_input/follow_ups/202609.md - section 012
Summary: 旅行者改为阳光开朗、一看就有锻炼的独立女性 vlogger，出 6 位候选（3 中 3 外）；视频里旅行者直接出声、人物 prompt 带声音；系列人物只住 `_series/`，单站不放同键人物卡。

Auto-updated:
- tools/gen_traveller_cards.py — 新增：六张系列人物卡的唯一出处（数据表 + 模板；读 p3 / p11 锁定串；闸门：识别标签 ≤30 汉字、prompt ≤5000、首行路由键、12 维灵魂）
- ai_videos/shikong_lvxing/_series/characters/c1_林问/c1_林问.md — 重做：29 岁前户外领队 / 攀岩型 vlogger（脸、身形、现代装、声音锁定串、12 维人物灵魂、立绘 c1-1、带声样建立视频 c1-2、sk1 宋装变体 c1-11 / c1-12）
- ai_videos/shikong_lvxing/_series/characters/{c2_周野, c3_许棠, c4_艾拉, c5_妮娅, c6_露西娅} — 新增候选卡（同结构；c1–c3 视频里说普通话，c4–c6 说英语）
- ai_videos/shikong_lvxing/sk1/2_世界观人设/characters/c1_林问/ — 删除（宋装变体迁入系列卡；旧立绘与旧卡存档 `ai_videos/_deleted/shikong_lvxing/sk1_c1_林问_旧长相_20260915/`）
- ai_videos/shikong_lvxing/sk1/2_世界观人设/props/p11_旅行者宋装/ — 新增：宋装形制锁定串 + 历史参考图库（自原 c1 卡迁入，ref_id 改为 p11_旅行者宋装.refNN）+ 锚点 prompt p11-1（1520 字）
- ai_videos/shikong_lvxing/sk1/2_世界观人设/characters/c2–c4 → c21_李十六 / c22_周四娘 / c23_沈十九 — 本地沉默面孔改键，避开系列名册键段（worker RENUM_sk1）
- tools/gen_shots_sk1.py — `--traveller cN` 选旅行者；两态锁定串、声音锁定串、voice_id、视频语种一律读系列卡；有台词的镜加 `声音:` 行 + `{名}声音(cN-2 声样)` 参考 + NEG_VOICE；`## 台词配音 prompt` 降为补录 / 译配；本地角色键 c21–c23；36 镜重生（默认 c1；c4 试跑全部闸门通过后复原）
- projects/ai_video_management/ — DownloadsImporter 同时向 `_series/` 路由，两边同键拒收并报 `series_key_conflict`（新 libs/common/series_shared.py、11 条新测试、README；worker IMP_series）
- CLAUDE.md § AI video rules · Series nesting — 新增「系列共用人物只住 `_series/`」规则
- ai_videos/shikong_lvxing/proposal.md — §3 名册换成 6 位候选；共用骨架「人脸 / 声音」行改为视频直接出声；目录树里的宋装参考图库指向 p11
- ai_videos/shikong_lvxing/_series/glossary.md — 英文专名表不再写死旧 voice_id
- specs/ai_video/sk1/divergence.md — 新增 #20 视频直接出声 / #21 声样按语种分两句 / #22 系列人物只住 `_series`、本地键 c21 起 / #23 旅行者可换；#5、#16 措辞同步
- sk1 casting.md / publish.md / relationships.md / 0_research/dossier.md / qc_stage2.md — 同步候选名册、视频原声 + 译配轨、指针

No conflicts found in: sk1 1_立项/concept.md、3_大纲/outline.md、world.md、style_guide.md（旅行者只以占位名「林问」出现，换人时由生成器替换）；scenes/ 与 p11 以外的道具卡

## Follow-up 013 — 2026-09-18 13:02:01
Source: user_input/follow_ups/202609.md - section 013
Summary: 系列扩边出「虚拟城支线」，第 2 站 sk2 ＝ 魔兽世界暴风城（经典旧世 Vanilla）。

Auto-updated:
- `ai_videos/shikong_lvxing/series.json` — description 去掉「历史上的」限定，写明城分历史城 / 虚拟城两类及各自的纪年口径
- `ai_videos/shikong_lvxing/proposal.md` — 新增 § H「虚拟城支线」：两类站对照表、十五条不变量改两条（I-2 / I-10）、明确不改 I-4、虚拟城选站三判据
- `ai_videos/shikong_lvxing/_series/sources.md` — 新增 §8「虚构世界」：T0–T4 tier 映射表 + 暴风城来源表 + 检索教训（只追加不改已有行）
- `specs/ai_video/sk2/` — 新建（raw/revised prompt、divergence #101–110、changelog）
- `ai_videos/shikong_lvxing/sk2/` — 新建阶段编号目录，与 sk1 同构

No conflicts found in: `_series/{blacklist.md, glossary.md, characters/}`（sk2 的暴风城黑名单与译名表由阶段 0 产出后另行追加，不改 sk1 已有行）；sk1 的任何产物（站站独立）。

## Follow-up 014 — 2026-09-18 15:10:00
Source: user_input/follow_ups/202609.md - section 014
Summary: 虚拟城站的 I-7 由「当地人零台词」改为「有逐字原文才能开口」；历史站不动。

Auto-updated:
- `ai_videos/shikong_lvxing/proposal.md` § H —「十五条不变量的改写」由两条增至三条，新增 I-7 条目（含原始理由的还原、虚拟城口径、配套三条）
- `specs/ai_video/sk2/divergence.md` — 新增 #111 及配套三条

No conflicts found in: sk1 与其余历史站（I-7 对历史站原样成立，未改一字）；I-5 旅行者三铁律、I-11 / I-12 旅行者形态（**均未变**：她仍不与当地人对话，仍是全片唯一解说声源）。

## Follow-up 015 — 2026-09-18 16:10:00
Source: user_input/follow_ups/202609.md - section 015
Summary: 虚拟城站允许「偶尔的 NPC 互动」（三档制）；形态确认为「旅游 + 解说」。

Auto-updated:
- `ai_videos/shikong_lvxing/series.json` — description 里「她不和当地人对话」按历史城 / 虚拟城两类分述
- `ai_videos/shikong_lvxing/proposal.md` § H · I-7 条目 — 补「互动三档」表 + 不变的分界线（知识只由旅行者讲）
- `specs/ai_video/sk2/divergence.md` — 新增 #113，含本站实际用到的档 2 台词表
- `ai_videos/shikong_lvxing/sk2/1_立项/concept.md` — 形态铁律段改写

撤销: follow-up 008 的「她不和当地人对话」**在虚拟城站的适用**（历史站原样不动）。

No conflicts found in: sk1 与其余历史站；I-5 旅行者三铁律（问路买东西不属「干预」，三铁律原样成立）；I-11 / I-12（她仍是全片唯一解说声源）。
