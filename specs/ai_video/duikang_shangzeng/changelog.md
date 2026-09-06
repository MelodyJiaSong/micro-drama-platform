# changelog · duikang_shangzeng

## 立项 — 2026-08-29
Source: user_input/raw_prompt.md（项目起点，无 follow-up）
Summary: 《对抗熵增》Ferrari F80 品牌广告片立项，走 ai_videos__全流程编排 阶段 1–3 + 阶段 5–6 样板镜。

用户裁定（AskUserQuestion 四题）：
- 车型 = **Ferrari F80**（非分镜原案的 LaFerrari）
- 叙事自由度 = **保留意象 · 重构骨架**
- 人物 = **一位锁定驾驶者 · 局部为主**（手 / 眼 / 侧脸 / 背影）
- 画幅 = **对齐竞品** → 实测得 2.35:1 / 3840×2160 / 25fps

新建产物：
- 1_立项/benchmark_teardown.md — 竞品 0710_v1.m4v 实测拆解（8 条可测量缺陷 + 硬指标）
- 1_立项/concept.md — 立项策划单 + 全片策略
- 2_世界观人设/world.md — 熵增法则视觉规则书
- 2_世界观人设/style_guide.md — 双色系统 / 五幕调色 / 节奏声音规格 / 负面词串
- 2_世界观人设/props/f80_ferrari/f80_ferrari.md — 车型锁定（三层强锁）
- 2_世界观人设/props/cavallino_horse/cavallino_horse.md — 全片唯一暗线
- 2_世界观人设/characters/driver/driver.md — 驾驶者（局部出镜规则）
- 2_世界观人设/scenes/{entropy_city,medieval_road,ice_plain}.md
- 3_大纲/arc_outline.md — 故事大纲 + 61 镜分镜总表（105.0s）
- 5_6_分镜与prompt/previz_plan.md — Blender previz 方案（18 镜）
- 5_6_分镜与prompt/shots/{shot14,shot20,shot60}/ — 三个样板镜

Divergence（相对 agent_refs/project/ai_video.md，均已在产物内注明）：
- rule 7 画幅：9:16 → **2.35:1**（用户指定对齐竞品交付规格）
- rule 6 单集时长：180–195s → **105s**（sub_type=short 广告片）
- rule 6 单镜 <3s 需注明：本片成片镜长 0.4–6s 双峰，靠「生成长 5–12s · 剪得短」实现
- rule 5 ① 小说原文：广告片无小说，以同等功能的「画面速写」替代
- previz 分工：F80 白模**保留真实车体几何**（产品即长相；马/人/建筑仍用 proxy）

待用户裁定：tagline 四选一 / 第Ⅳ幕是否加 OS / F80 三维模型取得方式。

## Follow-up 001 — 2026-08-29 14:52:00
Source: user_input/follow_ups/202608.md - section 001
Summary: previz 从「18 镜选做」改为「61 镜全做」，并确立「blend → MP4 → reference_video」四步工序：previz 管主干动作与人物物品位置，Seedance 管全部细节渲染与特效。

Auto-updated:
- 5_6_分镜与prompt/previz_plan.md — 全文重写：四步标准工序、prompt 与 previz 的字段分工、A/B/C/D 四档、关键帧 t ＝ 动作时间轴硬约束
- 5_6_分镜与prompt/shots/shot01..61/previz_config.toml — 新增 61 份骨架（A37 / B16 / C7 / D1）
- tools/gen_previz_scaffolds.py — 新增：从 arc_outline.md 生成 previz 骨架
- ai_videos/duikang_shangzeng/README.md — 使用说明第二步改为全量 previz

引擎改动（向后兼容，xianjian_yi_mv 不受影响）：
- tools/previz/build_previz.py — ① 新增 [全局].项目，场景主档路径不再硬编码 xianjian_yi_mv（缺省仍为它）；② 新增 [[道具]].形 = "模型" + .档，可从 .blend 追加真实网格当 proxy（自动 join、归一化到尺寸包围盒、原点落底面中心）
- tools/whitemodel_to_mp4.py — 新增 --project；shots 路径不再硬编码
- 备份：tools/previz/build_previz.py.bak

新增 divergence：
- F80 白模保留真实车体几何（走 形="模型"），突破「3D 不碰长相」的既定分工。理由：本片的长相即产品，且 F80 是 Seedance 唯一必然画错的对象。马/人/建筑仍用色块 proxy。

待办（previz_plan.md §七）：
1. 建三份场景主档 .blend（entropy_city 四板一体 / medieval_road / ice_plain）
2. 取得 F80 白模 → 跑 --force 把 61 份配置从 形="box" 升级为 形="模型"
3. 逐镜手调 TODO：方位角 / 占画高 / 关键帧 t 与位置
4. 回修 shot14/20/60 的 走位:/镜头:/动作:，去掉 previz 已管的坐标性描述

No conflicts found in: 1_立项/*, 2_世界观人设/*, 3_大纲/arc_outline.md（分镜表未变，previz 骨架由它派生）

### Follow-up 001 · 实测补记 — 2026-08-29
Blender 5.1 实跑验证，61 份配置过 tomllib 自检，抽样 shot04(C)/shot25(A)/shot58(A) 均自检通过。

实测修掉三个生成器缺陷：
- TOML 中文裸键非法（`[全局]` → `["全局"]`，嵌套 `[["道具"."关键帧"]]`）；生成器现内建 tomllib 自检
- 平移运镜默认量未按景别区分：85mm 微距用 8m 推进直接穿过主体（占画高 85%→41%）。改为按景别给初值
- 跟随镜让车向前跑 40m 导致占画高缩到 4%：跟随镜车＝画框锚点保持原点，相对运动写在马/角色上

实测暴露、留待手调两项（已记入 previz_plan §七之二）：
- 对冲镜车向默认反了（shot17 起近落远，应起远落近）
- shot32 马被解算到画面右侧，违反「马恒在画面左」铁律 —— previz 抓出了文字 prompt 阶段看不出的越轴错误

## Follow-up 002 — 2026-08-29 15:40:00
Source: user_input/follow_ups/202608.md - section 002
Summary: 核心 object 建多角度参考盘（对齐人物 turntable 流程），成套上传视频模型建立对象。

Auto-updated:
- .claude/agent_refs/project/ai_video.md — 新增 rule 4c「Image-first object pipeline」（common-level 规则，适用于任何以物件为核心主体的 ai_video 项目）
- 2_世界观人设/props/f80_ferrari/f80_ferrari.md — §3 重写为「多角度参考盘」：双轨制 + 七视角标准盘 + 基底 prompt/角度子句表 + 生成上传流程
- tools/render_object_turntable.py — 新增：从白模 .blend 渲 7 视角静帧 + 10s 转盘 MP4

设计要点：
- 5 个静止落点（0/45/90/135/180°），抽帧 t=0.75/2.85/4.85/6.85/9.10s，与人物 turntable 同构
- 跨角度 framing 恒定（85mm / 恒定距离 / 恒定光位），只有方位角变 —— 这是参考盘能用的前提
- A 轨（白模，几何精确）当 B 轨（Seedream 写实）的结构参考，比纯生成多角度一致性高一个量级

实测修正：
- 相机距离公式初版算错（7.41m），车顶被裁切；改为 dist = 主体最长边 × 焦距 ÷ (sensor × 0.78) = 14.96m，七视角完整入画且 framing 一致

No conflicts found in: 1_立项/*, 3_大纲/arc_outline.md, 5_6_分镜与prompt/previz_plan.md

### Follow-up 001 · 实渲补记 — 2026-08-29
从 `--no-render` 自检进到**真渲 MP4**，暴露三个自检抓不到的问题（自检只验几何解算，不看成片可读性）：

1. **跟随镜里马没锚定** —— 车已锚定在原点（画框锚点），但马仍带 +40m 前进轨迹，
   几帧内冲出画面。修：跟随镜的马也锚定，只写**相对车**的位移
   （起幅 [-3.2, -4.5] 落后一个身位 → 落幅 [-3.2, -0.5] 追平不超越）。
2. **马 proxy 与素模场景同色** —— 马用「深灰」，而 `build_previz.py` 的素模化把场景整体
   刷成中性灰，灰模视频里马与建筑无法分辨。previz 的全部意义是「一眼看清谁在哪」，
   主体必须高对比。修：马 proxy 改「绿」。
3. **scaffold 默认构图不可用** —— shot25 骨架值（占画高 0.35 / 横向偏移 0 / 方位角 25）
   渲出来车被切边、马贴画框边缘。手调到（0.24 / 0.20 / 40）后车马同框可读。
   **结论：61 份配置是「能跑的骨架」，不是「能用的成品」**，每镜的
   `方位角 / 占画高 / 主体坐标` 都必须按镜手调——这一步无法自动化。

新增产物：
- 2_世界观人设/props/f80_ferrari/whitemodel_usage.md — 白模三用途的具体流程
  （① Seedream 结构参考图 ② 转盘建立对象 ③ 逐镜 previz reference_video），
  含「.blend 是母版、PNG/MP4 是交付格式」的关系厘清与换模升级路径
- shots/shot25/{shot25_previz.blend, shot25_previz.mp4} — 首个实渲 previz（2560×1090/25fps/8.04s）

工具修正：
- tools/render_object_turntable.py — ① 相机距离公式（车顶被裁）② Blender 5.x slotted actions
  移除了 action.fcurves ③ 旋转段直线插值切弦致相机忽近忽远，每 15° 补帧

## Follow-up 003 — 2026-08-29 16:30:00
Source: user_input/follow_ups/202608.md - section 003
Summary: 对象建立顺序反转为「图先行」（纯文字基准图 → 挂基准图派生 6 角度 → 由图生白模）；车内座舱升格为独立的第二个 object。

Auto-updated:
- ai_videos/duikang_shangzeng/2_世界观人设/props/object_build_flow.md — 【新增】Step 1→3 完整流程与全部 prompt 正文：
  基准图 prompt（纯文字、8 条验收清单）、六张派生角度的共用前缀 + 角度句对照表、
  image-to-3D 的 MCP 调用与四步归一化（车头 +Y / 2.06×4.84×1.14 / 原点落底面中心 / 清材质）
- ai_videos/duikang_shangzeng/2_世界观人设/props/f80_cockpit/f80_cockpit.md — 【新增】第二个 object 的完整卡片：
  锁定描述符、驾驶位主视角基准 prompt + 8 条验收、三张派生（wheel/paddle/console）、
  可选座舱白模、跨镜一致性校验点（12↔45 同一仪表、43↔44 同一拨片、11 的手套不进基准图）
- ai_videos/duikang_shangzeng/2_世界观人设/props/f80_ferrari/f80_ferrari.md — §3.0「双轨制」整节替换为
  「图先行，白模后置」；§3.2 基底 prompt 与 §3.5 座舱 prompt 加「已被取代 / 已迁出」横幅；
  §四 模型来源标注现行选择改为方案 2（由图生模）
- ai_videos/duikang_shangzeng/2_世界观人设/props/f80_ferrari/whitemodel_usage.md — 顶部横幅：
  用途①（白模图当结构参考位）废止，用途③（逐镜 previz reference_video）成为白模唯一职责
- ai_videos/duikang_shangzeng/production_pipeline.md — Step 1–5 按新顺序重写
  （1 基准图 / 2 六派生 / 3 由图生模 / 3b 座舱对象 / 4 其余参考图 / 5 建立对象含 f80_cockpit），
  关键路径图改为「Step 1 是全片唯一单点瓶颈」

废止的决定（记录理由，防回退）:
- 原 A/B 双轨制（白模在前、写实图在后）废止 —— 手工 blockout 的白模精度不足以当结构参考，
  反而把写实图的质量上限拉低到 blockout 水平。基准图自由生成、质量上限最高，才配当锚点。
- `props/f80_ferrari/f80_ferrari.md` §四 模型来源方案 3（手工 blockout）不再是现行选择；
  现有 whitemodel/ 是其遗留产物，Step 3 跑完后整体替换。

No conflicts found in: 1_立项/, 3_大纲/, 4_剧本/, 5_6_分镜与prompt/（61 份 previz_config.toml 全部
按路径指向 f80_ferrari.blend，换模后自动生效，无需改动任何配置或 prompt）

## Follow-up 004 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 004
Summary: 更正 003 —— 一个 object 恰好 5 个 prompt（1 无参考全景 + 3 挂图1 的正/侧/背 + 1 给 Claude 的白模 prompt）；内饰顺延为 object 二。

Auto-updated:
- 2_世界观人设/props/object_build_flow.md — 整篇重写为 5-prompt 结构：
  派生角度由 6 个收敛回 3 个（正/侧/背）；Prompt 2/3/4 各写成可直接粘贴的完整正文
  （取消「共用前缀 + 角度句对照表」的抽象）；新增 Prompt 5 —— 明确标注**给 Claude 不给出片模型**，
  正文即 MCP 调用 + 四步归一化 + 下游重跑的可粘贴指令块；文末 object 二（内饰）标注顺延
- 2_世界观人设/props/f80_ferrari/f80_ferrari.md — §3.0 改为 5-prompt 流程图；
  §3.5 由「已迁出 f80_cockpit」改为「暂缓，等 object 一 完成后按同一 5-prompt 结构落卡」
- production_pipeline.md — Step 1/2/3 改为 Prompt 1 / Prompt 2·3·4 / Prompt 5；
  Step 3b 改为「object 二 内饰，等 Step 1–3 全部完成再开」；Step 5 身份包改为 4 张图 + 转盘；
  关键路径注明「图1 是全片唯一单点瓶颈」

已撤销（003 的过度发挥）:
- 删除 2_世界观人设/props/f80_cockpit/ 整个目录 —— 内饰对象提前建卡，违反「先做完 object 一」的顺序；
  待 object 一 完成后按同一 5-prompt 结构重建
- 撤销「派生角度补齐到 6 个」（front/side/rear3q/rear/top/low3q）—— 收敛回正/侧/背三个

No conflicts found in: 1_立项/, 3_大纲/, 4_剧本/, 5_6_分镜与prompt/


## Follow-up 005 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 005
Summary: 把 xianjian_yi_mv 的 prompt 结构实践抽象为仓库通用契约（rule 4d），并按契约重写本项目 5 个 object prompt。

Auto-updated:
- .claude/agent_refs/project/ai_video.md — 【新增 rule 4d】「对象建立的 5-prompt 结构 + 参考图 prompt 字段契约」：
  A 部分＝object 定义（靠剪影/比例识别 vs 靠部件相对位置识别＝两个对象）+ 5-prompt 表 +
  三条硬约束（图先行白模后置 / 星形非链式 / 图1 过验收才动下游）+ prompt 5 是给 Claude 的任务书；
  B 部分＝10 条字段契约（首行路由键 / `参考:` 带 `=>@` 占位 / **`参考用法:` 必写** / 字段化 /
  锁定描述符 byte-identical / `恒定项:` / `本视角要点:` / 负向单独块 / 合规去品牌 fallback / ≤2000 字）
  + 物件参考图标准字段序 + 「必须带可证伪验收清单表」。**全仓库所有剧共用。**
- .claude/agent_refs/project/ai_video.md — rule 4c 的「A 轨先行」加取代横幅：
  转盘时刻表 / framing 恒定 / 身份包整包上传三项仍有效，白模改为在 B 轨之后由图生成
- CLAUDE.md § AI video rules — 新增指针 bullet，指向 rule 4d（object 定义、五步、字段契约要点）
- 2_世界观人设/props/object_build_flow.md — 5 个 prompt 全部按 rule 4d 重写：
  加 `参考:` 行与 `@` 上传占位、加 `参考用法:` 权限归属行、字段化（主体/形体规格/识别特征/
  材质细节/姿态/机位/本视角要点/场景/光线/镜头/恒定项/构图/渲染样式/比例）、
  锁定描述符四张 byte-identical、负向词单列一块并注明不并进正向、加去品牌合规 fallback；
  文件头改为引用 rule 4d 而非自述规范

No conflicts found in: 1_立项/, 3_大纲/, 4_剧本/, 5_6_分镜与prompt/


## Follow-up 006 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 006
Summary: object 每视角一个 `v{N}_{视角}` 子目录、中文视角词作路由键；导入功能实现该路由；脚本产物目录排除出重命名扫描。

Auto-updated:
- .claude/agent_refs/project/ai_video.md — rule 4d 新增 §A2「落盘结构与路由键」：
  目录树、路由键必须中文且全剧唯一的理由（~9 字符截断实证）、歧义时报 unmatched 不猜、
  一文件夹一权威图重导即覆盖、脚本产物目录必须登记进 GENERATED_DIR_NAMES
- ai_videos/duikang_shangzeng/2_世界观人设/props/f80_ferrari/{v1_车外全景,v2_车外正面,v3_车外侧面,v4_车外背面}/ — 新建（含 .gitkeep）
- 2_世界观人设/props/object_build_flow.md — 四条 prompt 首行路由键由 `f80_ferrari_{视角}`
  改为 `车外{视角}`（截断安全）；`参考:` 行句柄同步；产物路径改为 v{N}_ 子目录；
  object 二 补车内一套视角词与目录

Cross-project (see specs/development/ai_video_management/changelog.md):
- downloads__writer.py — 新增 prop view 路由（_prop_view_token / _match_prop_view /
  _match_view_any_prop）、prop_view 覆盖语义、GENERATED_DIR_NAMES 排除重命名
- drama_layout.py — 新增 props_dir() 助手

No conflicts found in: 1_立项/, 3_大纲/, 4_剧本/, 5_6_分镜与prompt/（61 份 previz_config.toml
按路径引用 f80_ferrari.blend，未受目录新增影响）


## Follow-up 007 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 007
Summary: 场景走四层结构（平面图→广角全景→方位板→previz）；Seedance 2.5 实证推翻「建立对象」框架；entropy_city 补城市肌理并建 12 张方位板目录。

Auto-updated:
- .claude/agent_refs/project/ai_video.md — 【新增 rule 4e】场景建立的四层结构：
  为什么场景不能建成 object（无界 vs 有界刚体）、S1–S4 各层职责、S1 必须先于建模与出图、
  有 blend 就渲不要生成、S1 是一次免费体检（必跑必看）、方位板数量由分镜表推导不拍脑袋、
  方位段全剧唯一、变化态跨度大时单独出板
- .claude/agent_refs/project/ai_video.md — 【新增 rule 4d §A3】Seedance 2.5 实证修订：
  参考是 per-generation 没有持久化对象库、30图+10视频槽位不再稀缺、
  白模 clay render 是官方参考模态、多主体互动场景是官方自陈弱区
- .claude/agent_refs/project/ai_video.md — rule 4c「整包上传建立对象」加作废标注
- 2_世界观人设/props/object_build_flow.md — 「收尾·建立对象」改写为「组装参考包（每镜随附）」
- 2_世界观人设/scenes/entropy_city/entropy_city.blend — 补 266 个体块城市肌理
  （keep-out 让开全部走廊，既有 previz 构图零影响；确定性种子可重跑）
- 2_世界观人设/scenes/entropy_city/entropy_city_平面图.png — 新增（正交俯视，590.6m × 586.1m）
- 2_世界观人设/scenes/entropy_city/scene_build_flow.md — 新增：S1–S4 流程、布局锚表、
  S2 四张广角全景骨架 + 地点表、S3 方位板骨架 + 12 张机位与服务镜次表、每镜参考包组成
- 2_世界观人设/scenes/entropy_city/bg{0..4}_*/ — 新建 12 个方位板目录（路由键唯一性已校验）
- tools/render_scene_plan.py — 新增：场景 .blend → 正交俯视平面图（按场景长宽比出图）
- tools/add_city_fabric.py — 新增：按 keep-out 补城市肌理体块

待定（等用户拍板）:
- 复原态（第Ⅳ–Ⅴ幕 9 镜）是同板改色（A）还是六个方向各补一张变化态板（B）。倾向 B。

No conflicts found in: 1_立项/, 3_大纲/, 4_剧本/（61 份 previz_config.toml 未改动）


## Follow-up 008 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 008
Summary: 纠正 007——场景主体改为场景无关的固定视图集（核心4+选配2），不按分镜表推导；确认产品侧主体＝图集+description，可 @ 引用。

Auto-updated:
- .claude/agent_refs/project/ai_video.md — rule 4e 整节重写为「场景主体：一套场景无关的固定视图集」：
  显式作废「方位板由分镜表推导」并写明理由（主体是流程资产，换一部戏那些方向全用不上）；
  核心四张 + 选配两张的规格与「为什么任何场景都需要」；选配按**场景性质**加不按分镜加；
  主体边界判定（同一套材质与光能否读成一个地方 → entropy_city 是世界不是场景）；
  方向三来源分工表（主体只给长相，方向归 previz）；变化态跨度大时另建变化态主体
- .claude/agent_refs/project/ai_video.md — rule 4d §A3 修正：产品侧有持久化主体
  （图集 + description，`@` 引用），API 博客的 per-request 是下层实现；
  **产品 UI 与 API 文档冲突时以 UI 为准**；一次引用 1–8 个主体最稳（9–12 稳定性下降）；
  **description 字段 ＝ 锁定描述符的家**，prompt 里不再逐镜重贴
- 2_世界观人设/scenes/entropy_city/ — 删除 007 建的 12 个分镜推导方位板目录，
  改建 20 个固定视图集目录（全城2 / 广场6 / 主街5 / 高架4 / 隧道3），路由键唯一性已校验
- 2_世界观人设/scenes/entropy_city/scene_build_flow.md — 整篇重写为固定视图集流程：
  主体边界表、视图集规格表、星形出图顺序、正向骨架 + 4 地点表、派生骨架 + 15 视图表、
  description 内容、方向三来源

待定（等用户拍板）:
- 复原态：按 rule 4e 新规应另建变化态主体（广场/主街/全城三个），而非同板改色

No conflicts found in: 1_立项/, 3_大纲/, 4_剧本/, 5_6_分镜与prompt/


## Follow-up 009 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 009
Summary: 确立场景层级模型 L0/L1/L2/L3（主体＝Place×State）与三条判定；entropy_city 落为 1 World / 5 Place / 8 主体 / 30 视图。

Auto-updated:
- .claude/agent_refs/project/ai_video.md — 【新增 rule 4f】场景层级模型：
  三种切法对照表 + 证明其非上下级的不对称（光影变→主体变而 Blender 不动；炸毁→两者都变）；
  四层模型与 description 继承链；判定一「调色师测试」定新主体；判定二「挡镜头测试」定几何变体；
  判定三「用到才建但不允许建一半」+ 视图集规格不可读剧本 / 状态清单可读剧本的分工；
  State 封闭枚举 + 自由扩展位 + 稀疏差量 + 变体继承基线平面图；
  两条反模式（为细节拆主体 / 把 sub-scene 当层级）；变更传播表
- 2_世界观人设/scenes/entropy_city.md — 新增「层级归属」节：四层实体对照、基线态声明、
  状态清单表（含变体理由）、「Blender 几何变体：无」的判定结论
- 2_世界观人设/scenes/entropy_city/scene_build_flow.md — 边界节改为
  1 World / 5 Place / 8 主体；主体表补 3 个复原变体；状态块更新
- 2_世界观人设/scenes/entropy_city/bg*_复原*/ — 新建 10 个变体视图目录
  （广场复原5 / 主街复原4 / 全城复原1）

校验：30 个路由键零重复、零互为子串、最长 6 字（截断限 ~9 字）

No conflicts found in: 1_立项/, 3_大纲/, 4_剧本/, 5_6_分镜与prompt/


## Follow-up 010 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 010
Summary: entropy_city 30 个视图槽位全部就位（4 平面渲染 + 26 模板生成的 prompt）；修正复原态变体的字段自相矛盾并升为 rule 4f 一条。

Auto-updated:
- 2_世界观人设/scenes/entropy_city/bg*/{view}.md — 【新增 26 份】每个视图目录一份可直接粘贴的 prompt，
  由模板生成：共用骨架跨 26 份 byte-identical；负面词 2 版（基线/复原）；
  参考用法 3 版（平面/派生/状态）；最长 847 字（上限 2000）
- 2_世界观人设/scenes/entropy_city/bg{0,1,2,3}_*平面*/*.png — 【新增 4 张】
  全城/广场/主街/高架 平面图，从 entropy_city.blend 正交俯视渲染（平面视图永不生成）
- tools/render_scene_plan.py — 加 --region 支持，可只框一个 Place 出平面图
- tools/gen_scene_prompts.py — 【新增】从单一数据表生成全部视图 prompt，可重跑
- .claude/agent_refs/project/ai_video.md — rule 4f 新增「变体主体怎么写：结构继承，外观整套换」：
  结构字段（机位/构图/恒定项/参考图）继承 vs 外观字段（本地点/光线/色彩/**负面词**）整套换；
  记录实测踩坑与「负面词最容易被漏」的原因
- 2_世界观人设/scenes/entropy_city/scene_build_flow.md — 状态块更新为已完成态 + 校验结果

修正的缺陷（生成时自查发现，非下游报错）:
1. 复原态变体沿用基线负面词（禁「彩色灯光/鲜艳广告牌」）与复原态语义直接冲突
2. 复原态变体 `本地点:` 仍为熵增态描述（「积着薄薄一层灰」），与同份 prompt 的 `色彩:` 行打架

No conflicts found in: 1_立项/, 3_大纲/, 4_剧本/, 5_6_分镜与prompt/


## Follow-up 011 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 011
Summary: 26 份视图 md 改为「用途 + 验收」两块，操作步骤移出文件；修复无正向视图地点（全城）的锚点解析。

Auto-updated:
- 2_世界观人设/scenes/entropy_city/bg*/{view}.md — 全部重生成：新增「这张图是干什么用的」
  （进哪个主体 / 职责 / 谁在等它 / 出片时谁用 / 不做会怎样）+ 分类验收清单
  （锚点 6 条 / 派生 5 条 / 材质 4 条 / 变体 6 条）；不含操作步骤
- tools/gen_scene_prompts.py — 移除 steps() 段；修 StopIteration：
  地点若无 fwd 视图（全城），其唯一 look 视图即锚点、直接挂平面图


## Follow-up 012 — 2026-08-30 12:05:00
Source: user_input/follow_ups/202608.md - section 012
Summary: 白模只扛几何（到型面语言层），颜色/材质细节/特效归 Seedance；渲染侧先修，让型面真的渲得出来。

Auto-updated:
- .claude/agent_refs/project/ai_video.md — 【新增】§「previz 白模必须把型面渲得可读」
  （挂在 §方向从哪来 之后）：分工推论（几何必须被渲进画面否则到不了模型手里）、
  抹掉型面的三个成因（平光 / 无 AO / 背景与模型同明度）、Freestyle 四类边
  （silhouette+border+crease+ridge_valley，ridge_valley 管无硬边的鼓凹）、
  「堆网格细节前先确认渲染读得出来」、以及细节边界（白模扛到 T3，T4 归 Seedance）
- tools/previz/build_previz.py — 【新增】§形状可读性：EEVEE AO
  (use_raytracing + use_fast_gi + AMBIENT_OCCLUSION_ONLY, distance 0.6m)
  + Freestyle 描边 + taa_render_samples≥32 + 背景压深；
  三点布光取代两盏平光（主:补 由 2.5:1 拉到 5.6:1，新增 PREVIZ_RIM 轮廓光）
- tools/previz/build_previz.py — 白模 prop 改用专用 M_WHITEMODEL（无自发光）
  取代 MATS 的 ID 色材质：MATS 全部带 emission 0.25，自发光是平的，
  恰好把全场唯一需要读出型面的物体抹平
- tools/render_object_turntable.py — 同一套 AO / Freestyle / 三点光配置
  （两处白模观感必须一致）；背景与地面压深至 0.13 / 0.16

Bug 修复（本轮实测暴露，非用户报告）:
- tools/render_object_turntable.py — 引擎回退链错误：Blender 5.x 的枚举已无
  "BLENDER_EEVEE_NEXT"，赋值抛 TypeError 后**回退目标写的是 BLENDER_WORKBENCH**，
  于是 5.1 上一路掉进 Workbench——AO 被 startswith 判空跳过、Freestyle 在
  Workbench 下根本不渲。改为 EEVEE_NEXT → EEVEE 两级回退，找不到即硬报错
- tools/render_object_turntable.py — 材质用 `use_nodes=False` + `diffuse_color`，
  那只是**视口显示色**：Workbench 认、EEVEE 不认，EEVEE 退回默认近白表面，
  车/地面/背景渲成同一片白。改为渲染器无条件剥掉源档材质换成节点化灰模
  （`clay_material()` + `strip_and_clay()`）——这也正是白模「只承载几何不承载材质」
  的应有实现，且将来换 image-to-3D 生成的网格（自带烤死贴图）同样适用

实测结论（现有脚本 blockout，修完渲染后重渲七视角）:
- T1 姿态比例 ✅ 达标
- T2 剪影地标 ❌ 轮子是外凸的圆柱、完全无轮拱；座舱是多面楔子、无泪滴收窄
- T3 型面语言 ❌ 前轮后竖开口、车头横贯黑条、后轮拱外鼓 全部不成立
→ 「改脚本 blockout」确认到不了 T3，降为兜底；换模型的决策依据已具备

No conflicts found in: 1_立项/, 3_大纲/, 4_剧本/, 5_6_分镜与prompt/shots/


## Follow-up 012 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 012
Summary: 明确「链条起点只能是纯文字或渲染」；纠正 rule 4e 中全新场景的第一张图顺序（先生成平面图 → 作废）。

Auto-updated:
- .claude/agent_refs/project/ai_video.md — rule 4e「S1 平面图」节重写：
  分「已有 .blend」与「全新场景」两种起点；作废「先生成平面图再建模」，
  改为「纯文字广角正向 → 建模 → 渲平面 → 出其余」；写明理由与 object 流程反转同源；
  草图平面定性为一次性脚手架（不进主体、不当参考）；补「鸡生蛋被 Blender 断开」的说明
- 2_世界观人设/scenes/entropy_city/scene_build_flow.md — 新增「第一张图从哪来」小节：
  本场景起点是渲染；平面图只给布局不给长相，故锚点实质纯文字驱动、必须反复重跑


## Follow-up 013 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 013
Summary: 按「精简三律」重写 26 份场景 prompt（平均 850 → 314 字），并把三律写进 rule 4d。

Auto-updated:
- tools/gen_scene_prompts.py — 重写：`场景` 按地点写（不再共用会夹带别处细节的世界串）；
  `光线`+`色彩` 合为 `光色`、`机位`+`镜头` 合为 `机位`；派生 prompt 删 `场景`/`光色`；
  变体改用 `只改:`/`不改:` 两行；`参考用法` 压到一句；负面词去重
- 2_世界观人设/scenes/entropy_city/bg*/{view}.md — 26 份全部重生成
- .claude/agent_refs/project/ai_video.md — rule 4d 新增「参考图 prompt 的精简三律」

修正的缺陷（自查发现）:
1. 「无方向主光/灰烬色/微粒下落」跨 3 个字段重复（word-stacking，仓库明禁）
2. 共用世界串把主街的「广告屏」带进广场 prompt——有害，可能真画出来
3. 派生 prompt 重述全套长相，与其参考图构成自相矛盾风险

校验：平均 314 字（最短 269 / 最长 404），字段 8/7/8；广场 prompt 已无「广告屏」，主街仍有


## Follow-up 013 — 2026-08-30 12:40:00
Source: user_input/follow_ups/202608.md - section 013
Summary: 建 vendor 无关的白模归一化+验收闸门（通用，全仓库所有剧所有 object 复用）。

Auto-updated:
- tools/whitemodel_normalize.py — 【新建】白模闸门。任何来源的网格（glb/gltf/obj/
  fbx/stl/ply/blend）进来，出去是可用的 {name}.blend。四步归一化写成代码
  （朝向按 spec 旋转 / 等比缩放到声明包围盒 / 原点落底面中心 / 无条件剥材质）
  + 可证伪验收报告（包围盒、原点、材质残留、松散块数 + 逐条识别特征探针）。
  QC 不通过退出码 1——是闸门不是报告。`--qc-only` 可体检已有白模
- ai_videos/duikang_shangzeng/2_世界观人设/props/f80_ferrari/object.toml —
  【新建】首个 object spec：尺寸/容差/源朝向/目标朝向 + 6 条验收
  （尾翼·扩散器·车头黑条·前分流器 走「占位」，后轮拱外鼓·泪滴座舱收窄 走「截面对比」）。
  内容即用户在任务书里手写的那张验收单，写一次、此后每次重生成自动验
- .claude/agent_refs/project/ai_video.md — 【新增】rule 4d §A1b「白模闸门：
  归一化与验收是代码，不是散文」：闸门 vendor 无关（genericity 来自闸门不来自来源）、
  两类探针表（占位 / 截面对比）、两条实测硬约束、阈值校准方向、薄结构兜底、
  等比缩放而非逐轴拉伸的理由

实测（现有脚本 blockout 过闸门，--qc-only）: 4 项硬失败——
原点未落接地面（说明已提交的 .blend 从未做过归一化四步）、材质残留 1、
扩散器仅 6 顶点（需 ≥12）、前分流器仅 4 顶点（需 ≥8）

本轮开发中修掉的探针 bug（均为自测发现）:
- 截面对比方向判断：用 `">" in rel` 判方向，而 "A > B" 与 "B > A" 都含 ">"，
  导致 "B > A" 的比较取反、正确的网格被误判失败。改为按哪一侧在前决定
- 截面对比缺第三轴限定：突出于主体的附件淹没主体信号——量「后轮拱外鼓于车身中段」
  时两个带量到的都是外凸的轮子。新增 `限定` 字段
- 空带假通过：带内无几何时 extent＝0，"A > B" 平凡成立。改为空带硬失败并报明原因

No conflicts found in: 1_立项/, 3_大纲/, 4_剧本/, 5_6_分镜与prompt/shots/


## Follow-up 014 — 2026-08-30 14:20:00
Source: user_input/follow_ups/202608.md - section 014
Summary: 自建本地 image-to-3D 环境（受阻于网络）；闸门探针改为密度无关判据；补齐第Ⅰ幕 8 个 shot prompt。

Auto-updated:
- tools/whitemodel_generate.py — 【新建】由参考图生成白模原始网格（本地推理，
  零成本可无限重试）。读 object.toml 的 ["参考图"] 段做视角映射，只生成 shape 不生成 texture
  （材质在闸门里会被剥掉，且显存需求由 16GB 降到 6GB）
- tools/whitemodel_normalize.py — 占位探针判据由**顶点数**改为**面积占比**（密度无关）：
  320 顶点的脚本 blockout 与十万顶点的生成网格描述同一结构时差三个数量级，
  绝无可能共用绝对阈值，而闸门的意义正是同一份清单验任何来源的网格
- tools/whitemodel_normalize.py — 截面对比新增 `最大差` 上界关系：
  有些特征要判的是「A 不该比 B 大太多」（如轮拱须包住轮子），只有上界能表达
- tools/whitemodel_normalize.py — 新增 `--src-forward` / `--src-up` 命令行覆盖：
  生成网格的朝向每版都可能不同，改 toml 太重
- props/f80_ferrari/object.toml — 新增 ["参考图"] 视角映射（front/left；
  3/4 锚点不参与重建，mv 模型只认正交视角，塞进 back 槽会把车尾拧歪）；
  阈值改为面积占比；新增「轮拱包覆轮子」上界验收；
  **新增「本清单测得到什么、测不到什么」段**
- props/f80_ferrari/f80_ferrari.blend — **首次真正过完四步归一化**（此前从未做过）：
  包围盒 2.060×4.840×1.140 精确、原点落接地面、材质清零。原档已备份
- .claude/agent_refs/project/ai_video.md — rule 4d §A1b 追加三条：探针能力边界
  （体量测量判定不了表面质量与拓扑，「全部通过」≠「好白模」，不写明会误导下一个人）、
  占位用面积占比不用顶点数、截面对比需要上界关系
- production_pipeline.md — Step 6 状态 4/61 → 12/61；Step 3 改为「闸门已建，等 mesh 来源」
- 5_6_分镜与prompt/shots/shot02..shot09 — 【新建】**第Ⅰ幕补齐**，共 8 个 shot prompt
  （失速铁律示范 / 机械犬瓦解 / 高脚杯保持杯形 / 路人边界消失 / 雨滴悬停 /
  车的反证镜 / 青铜马埋点 / 她睁眼）。全部过生成时自检：
  视频 prompt 985–1518 字符（≤2000 硬顶）、零字幕污染、车锁定描述符 byte-identical

环境受阻（非设计问题，已尽力绕行）:
- 本机网络对持续大文件下载不可用：pytorch.org 376kB/s 后中断；aliyun pypi 中断；
  aliyun / nju pytorch-wheels 停在 9MB；github codeload 及两个代理固定停在 104KB；
  HF 权重 25 分钟只到 56MB。多源轮换 + 断点续传均无法在可用时间内完成
- 绕行方案已定并部分落地：**放弃自建 venv，改用 ComfyUI 现成环境**——
  该机 ComfyUI 已有 torch 2.7.1+cu128（CUDA 可用），且 ComfyUI **原生内置 Hunyuan3D**
  （comfy/ldm/hunyuan3d + comfy_extras/nodes_hunyuan3d.py，含 Hunyuan3Dv2ConditioningMultiView
  多视角节点），因此只差一个权重文件，不需要腾讯仓库、不需要装 torch
- 权重 tencent/Hunyuan3D-2mv 的下载重试循环仍在后台运行（200 次续传）
- 许可证已核实：Tencent Hunyuan 社区许可**允许商用**，限制为地域排除 EU/UK/韩国、
  MAU >100 万需单独授权。本用途（内部 previz 代理，网格永不进成片）在范围内

No conflicts found in: 1_立项/, 3_大纲/, 4_剧本/


## Follow-up 014（续）— 2026-08-30 15:10:00
Source: user_input/follow_ups/202608.md - section 014（自行推进后续 step）
Summary: 第Ⅱ幕补齐 9 镜；补上马卡缺失的青铜像态锁定描述符。

Auto-updated:
- 5_6_分镜与prompt/shots/shot10..13, shot15..19 — 【新建】**第Ⅱ幕补齐**共 9 个 shot prompt
  （车灯亮起 / 手转旋钮 / 仪表扫针 / 排气回火 / 起步打滑 / 冲出广场入主街 /
  对冲掠过 / 颜色灌回路面 / 铜色褪去露出黑马）。加上已有的 shot14、shot20，
  第Ⅱ幕 11 镜齐；Step 6 累计 21/61
- props/cavallino_horse/cavallino_horse.md — 【新增】**青铜像态锁定描述符**（byte-identical）。
  此前卡片只有活马态锁定串，而 shot08（埋点）/ shot19（褪铜）/ shot20（首帧承接）
  三镜都依赖铜态，各镜各写必然漂移——正是 rule 4d 设立锁定描述符要防的那一类。
  同时写明两态的硬对应：额头竖纹（铜态凸棱 ↔ 活态白纹）位置相同、
  左前蹄白斑褪铜后须在同一位置显形——这两处是观众确认"同一匹马"的唯一凭据
- 5_6_分镜与prompt/shots/shot08/shot08.md — 铜态描述符改为引用卡片新增的 byte-identical 串
  （原为本会话自拟，与卡片不一致）
- production_pipeline.md — Step 6 状态 12/61 → 21/61

设计决策（供复核）:
- shot18「颜色灌回」三个要点写成硬验收：**滞后 0.5s**（立刻变色会读成车身带光效）、
  **从车痕向两侧渗**（整屏提亮会读成调色而非事件）、**渗到两米就停**（无边界会读成
  "世界修好了"，第Ⅳ幕整城复原就失去可升级空间）。三条缺一即重跑
- shot17 与 shot16 之间是**故意越轴**（车尾→车头）：车在世界坐标里方向未变，
  只是机位到了它前方。两镜之间不得加过渡，加了会被读成"车掉头"
- shot19 声明**尾帧锁定**（shot20 的交接源）：重生时须把末帧钉回
  shot19_lastframe.png，否则 shot20 及下游整条链要跟着重渲
- shot12 标注**依赖缺口**：内饰对象（object 二）尚未建立，仪表盘无参考图可挂，
  当前仅靠文字约束；内饰建立后 shot12/43/44/45 应重跑

自检（全 20 镜，按卡片规范串校验）:
- 视频 prompt 985–1785 字符，全部 ≤2000 硬顶
- 零字幕污染；锁定描述符 byte-identical：车 9 处 / 铜马 2 处 / 活马 2 处 / driver 2 处，全对
- 注：过程中一次「shot14 车锁不一致」是校验器拿 shot01 当基准造成的误报，
  以卡片 160 字规范串复核后 shot14 正确

No conflicts found in: 1_立项/, 3_大纲/, 4_剧本/


## Follow-up 014 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 014
Summary: 补世界锚点层——广场正向为全片唯一自由生成图，其余四个地点锚点挂它继承世界基调。

Auto-updated:
- .claude/agent_refs/project/ai_video.md — rule 4e 新增「一个世界只有一张自由生成图」：
  三层星形图、世界锚点选取标准、地点锚点的 `参考用法` 写法、地点锚点不重述光色、
  「自由生成的特权只给链条起点那一张」
- tools/gen_scene_prompts.py — 新增 WORLD_ANCHOR 概念与 USE_PLACE / LIGHT_SAME 两段文案；
  地点锚点改挂 `广场正向 + 本地点平面图`；新增 place 类 PURPOSE
- 2_世界观人设/scenes/entropy_city/bg*/{view}.md — 26 份重生成
- 2_世界观人设/scenes/entropy_city/scene_build_flow.md — 出图顺序图改为三层星形

修正的缺陷（排依赖图时发现）:
1. 原 5 个锚点各自只挂自己的平面图，彼此无图片纽带 → 五个地点可能出成五个世界的调子
2. `全城斜瞰` 也是锚点（全城无正向视图），先前的 step-by-step 误将其归入第 2 步

校验：广场正向 ← 广场平面｜主街/高架/隧道正向 + 全城斜瞰 ← 广场正向 + 本地点平面；
26 份平均 315 字


## Follow-up 015 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 015
Summary: 结构参考改为本机位灰模透视图；场景描述写详细；目录 bg{N} 按依赖层级编号。借灰模渲染抓出广场开口被堵与隧道无几何两个缺陷。

Auto-updated:
- tools/render_scene_view.py — 【新增】按机位/朝向/焦段从 .blend 渲 21:9 灰模透视图
- tools/add_tunnel.py — 【新增】补隧道几何（14×6m 断面、150m、12 组顶灯）
- tools/fix_plaza_opening.py — 【新增】拆 BG1_TOWER_4 为两栋夹住开口的板楼
- 2_世界观人设/scenes/entropy_city/_clay/*.png — 【新增 12 张】各视图机位的灰模透视图
- 2_世界观人设/scenes/entropy_city/entropy_city.blend — 补隧道几何 + 打通广场北开口
- 2_世界观人设/scenes/entropy_city/bg*/ — 30 个目录按依赖层级重编号
  （bg0 平面 / bg1 世界锚点 / bg2 地点锚点 / bg3 派生 / bg4 变体），按名排序即出图顺序
- tools/gen_scene_prompts.py — 参考改灰模；SCENE 五段全部写详细；新增 USE_TEX（材质视图无灰模）
- .claude/agent_refs/project/ai_video.md — rule 4e 新增两节：
  「结构参考用本机位的灰模透视图，不要用平面图」（含参考位分工表 + 灰模即几何体检）
  与「落盘顺序 ＝ 依赖顺序」
- projects/ai_video_management/.../downloads__writer.py — `_clay` 加入 GENERATED_DIR_NAMES

灰模渲染抓到的几何缺陷（平面图看不出）:
1. BG1_TOWER_4 横堵广场北开口 → shot16 车开不出广场。已拆为两栋夹住开口
2. 隧道零几何 → shots 21/22/40 previz 无隧道。已补


## Follow-up 016 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 016
Summary: 二次纠正——锚点图零参考自由生成，3D 模型降为图的下游，blend 产物全部移出参考位。

Auto-updated:
- .claude/agent_refs/project/ai_video.md — rule 4e 中「结构参考用灰模透视图」整节**作废并替换**为
  「图先行，3D 在后——绝不拿 blockout 当出图参考」：四步链条、为什么 blockout 会锁死质量上限
  （与 follow-up 003 废止白模结构参考同一个坑）、平面图/灰模的两个正当用途、
  布局靠锚点 prompt 文字约束而非参考图、已有 blend 的老项目降级为 previz 专用
- tools/gen_scene_prompts.py — 锚点 `参考: 无`；地点锚点 ref 仅世界锚点图；
  派生 ref 仅本地点锚点图；`样式` 加强细节密度要求
- 2_世界观人设/scenes/entropy_city/_blender/ — 【新增】收纳 4 张平面图 + 12 张灰模透视，
  移出出图树、不参与生成
- 2_世界观人设/scenes/entropy_city/scene_build_flow.md — 出图顺序改为图先行四步链；
  新增「布局怎么约束（不靠参考图）」空间事实表

重复犯错记录（防三次）:
follow-up 003 已在 object 流程上废止「白模渲图当结构参考」；本轮在 scene 上重犯，
把灰模透视挂进参考位。已在 rule 4e 标注「这条被踩过两次，写死在这里」。


## Follow-up 017 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 017
Summary: 视图集由 26 张砍到 8 张必做 + 18 张按需；世界锚点 prompt 扩到 1556 字。

Auto-updated:
- .claude/agent_refs/project/ai_video.md — rule 4e 新增「视图集要多小：先做锚点，派生按需补」：
  必做＝每个 Place×State 一张锚点；派生视图是材质保真度不是方向机制、默认不做；
  锚点 prompt 篇幅下限 1500 字及其分层写法与理由
- tools/gen_scene_prompts.py — SCENE 五段全部扩写为分层长文（广场 8 层）
- 2_世界观人设/scenes/entropy_city/bg*/ — 26 份重生成；18 份按需视图的 md 顶部加
  「按需·先不做」标注

自查纠正: 我此前违反了自己写的 rule 4f「用到才建」——按固定视图集把 26 张全列为待做


## Follow-up 018 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 018
Summary: 清理 follow-up 015 目录改名遗留的 22 份过期 md；生成器加自动收敛守卫。

Auto-updated:
- 2_世界观人设/scenes/entropy_city/bg*/ — 删除 22 份名字与目录不符的过期 md
- tools/gen_scene_prompts.py — 新增 sweep_stale()，每次运行先删掉视图目录里任何
  非 `{目录名}.md` 的 md，保证一目录恰好一份 prompt

缺陷来源: follow-up 015 重编号目录时 `mv` 只改目录名、未改内部文件名，
生成器随后按新名又写一份 → 每个改名目录两份 md、一份过期


## Follow-up 019 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 019
Summary: 目录结构收敛为「一个目录 ＝ 一个主体」（26 视图目录 → 8 主体目录）；导入端支持目录内多视图共存。

Auto-updated:
- 2_世界观人设/scenes/entropy_city/bg{1..8}_* — 8 个主体目录，各一份 md 装该主体全部视图
  （description + 出图顺序表 + 每视图用途与验收 + prompt + 一份共用反向词）
- tools/gen_scene_prompts.py — 改为按 SUBJECTS 分组输出，一目录一份 md
- .claude/agent_refs/project/ai_video.md — rule 4e 新增「落盘结构：一个目录 ＝ 一个主体」


## Follow-up 020 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 020
Summary: `_blender/` 改为「给 Claude 的建模指令 md + 建模后的校验产物」，删除旧路线的渲染残留。

Auto-updated:
- 2_世界观人设/scenes/entropy_city/_blender/ — 删除 4 张平面图目录 + 12 张灰模透视
  （均从手工 blockout 渲出，follow-up 016 后既非参考亦非产物）
- 2_世界观人设/scenes/entropy_city/_blender/blender_build.md — 【新增】给 Claude 的建模指令：
  前置（五张锚点图）/ 现状（校正而非重建）/ 可粘贴 prompt 块 / 验收 / 完成后下游重跑；
  含「只建镜头相关体量、装饰不建」及其理由
- .claude/agent_refs/project/ai_video.md — rule 4e 目录树补 `_blender/` 三项内容；
  新增「`.blend` 怎么建：一份给 Claude 的建模 prompt」


## Follow-up 021 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 021
Summary: `参考:` handle 改为完整路径；每个 prompt 块补「上传 / 出图后存」两行；加引用可达性机检。

Auto-updated:
- tools/gen_scene_prompts.py — 新增 VIEW_PATH 映射；全部 ref handle 改为
  `{主体目录}/{视图}.png`；md 每个 prompt 块上方输出「上传」「出图后存」两行
- 2_世界观人设/scenes/entropy_city/bg*/ — 8 份主体 md 重生成
- .claude/agent_refs/project/ai_video.md — rule 4d 新增「`参考:` 行写完整路径，不写裸名」，
  含可机检规则（ref handle ⊆ 产物路径）

校验：26 条 prompt 的全部 ref handle 均指向本流程会产出的路径，差集为空


## Follow-up 022 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 022
Summary: `.blend` 迁入 `scenes/{name}/_blender/`，previz 解析路径同步；清掉场景根的 .blend1 与被重命名误伤的平面图。

Auto-updated:
- 2_世界观人设/scenes/{entropy_city,ice_plain,medieval_road}/_blender/{name}.blend — 由场景根迁入
- tools/previz/build_previz.py — 场景 .blend 解析改为 `_blender/{场景名}.blend`，
  旧布局作兜底；shot25 --no-render 实测通过
- .../entropy_city/_blender/blender_build.md — 新增「落点」节；存盘路径与 `参考:` 行
  （改为完整路径）同步
- .claude/agent_refs/project/ai_video.md — rule 4e 目录树补 `{world}.blend` 落点；
  新增「场景根只留主体目录、_blender/ 与流程 md」及其理由

清理:
- 三个场景的 `.blend1`（Blender 自动备份）
- entropy_city.png（3MB）——早先放在场景根的平面图被重命名扫描改成了 `{场景名}.png`，
  看着像场景立绘、实为素模俯视图


## Follow-up 015 — 2026-08-30 16:30:00
Source: 会话内决策（Hunyuan3D 因许可终止 → 改用 Rodin Creator 付费档）
Summary: F80 白模由 Rodin 多图重建生成并过闸门，Step 3 完成。

Auto-updated:
- props/f80_ferrari/f80_ferrari.blend — **由脚本 blockout 换为 Rodin 重建网格**
  （100 万面 / 734,486 顶点，来源 f80_raw.glb 35.5MB，四张参考图多视角融合）。
  过闸门全部通过：包围盒 2.060×4.840×1.140 偏差 0.0% / 原点落接地面 / 材质清零 /
  尾翼 10.82% / 扩散器 4.74% / 车头黑条 3.05% / 前分流器 3.02% /
  后轮拱外鼓 / 泪滴座舱收窄 / 轮拱包覆 / 朝向判别。旧 blockout 已备份
- props/f80_ferrari/whitemodel/ — 七视角定角图 + 10s 转盘 MP4 全部由新网格重渲
- **61 份 previz 配置与全部 shot prompt 零改动** —— 闸门做成 vendor 无关的回报

闸门的两个真实盲点（本轮实测暴露并修复）:
- **包围盒抓不住 180° 掉头。** Rodin 输出车头指向 -Y（我按 +Y 归一化），
  导致所有按车长分带的探针整体量错另一端——「尾翼 0.21%」量的其实是车头低鼻区，
  「车头黑条 4.07% 通过」是**假通过**。新增「朝向·车尾高于车头」截面对比探针，
  以后任何 object 掉头当场被抓
- **占位阈值须按首个通过的网格校准，不能沿用 blockout 时代的值。**
  松散块上限 40 对生成网格无意义（每条缝每片格栅都是独立壳，实测 46575），
  按 rule 4d §A1b 的校准方向重定为 60000

工具修复:
- tools/render_object_turntable.py + tools/previz/build_previz.py —
  Freestyle 按面数自动开关（>20 万面即关）。Blender 5.1 的 Freestyle 在生成网格的
  非流形拓扑上崩溃（FEdgeSmooth.normal_left），且高面数靠 AO 已足够读型面
- props/f80_ferrari/object.toml — 源朝向改为实测值（前 -Y / 上 +Z）；
  新增朝向判别验收；松散块阈值校准

vendor 决策记录:
- Hunyuan3D-2 **弃用**：Tencent Hunyuan Community License 带地域排除（EU/UK/KR）
  与 MAU>100 万门槛，不满足「完全开源可商用」。已下的两个 4.93GB 权重留在
  C:\models\checkpoints\ 待处置（其中 turbo 版是本机原有，非本次下载）
- **Rodin (Hyper3D) Creator 档**：全套餐授予完整商用权、支持多图融合、
  Creator 无 API（生成在网页端由用户完成，GLB 手动交付给闸门）——
  这与既有分工一致（用户出图挑图，Claude 接手），每 object 仅多一次点击

No conflicts found in: 1_立项/, 3_大纲/, 4_剧本/, 5_6_分镜与prompt/


## Follow-up 023 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 023
Summary: 修复导入失败（主体目录被当单图 plate 清空）；路由键改 `bg{N}.{M}`；今日流程写进 stage2 playbook 与 CLAUDE.md。

Auto-updated:
- tools/gen_scene_prompts.py — 路由键 `bg{N}.{M}_{视图名}`；md 每个 prompt 补「路由键」行
- 2_世界观人设/scenes/entropy_city/bg*/ — 8 份主体 md 重生成
- .claude/skills/ai_videos__全流程编排/playbooks/ai_videos__stage2_世界观人设.md —
  新增 §3b「资产建立标准流程」：六条铁律 + 命名与路由表 + 六步顺序（新剧默认读到）
- CLAUDE.md § AI video rules — 原 object-only 条目扩为覆盖 object 与 scene 的六条铁律
  + 命名路由规则

根因（已复现）: `bg1_广场` 被当成单图 plate，每次导入 `_clear_folder_media` 清空整个目录，
三张图导进去只活下来一张；截断的 `广场正` 还能靠子串匹配覆盖正确那张


## Follow-up 024 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 024
Summary: 修复导入落名错误（键不在文件名开头）；首图验收发现并修掉画幅、红色自相矛盾、过期验收条目。

Auto-updated:
- tools/gen_scene_prompts.py — 落盘路径改 `bg{N}.{M}.png`；`构图` 字段把画幅提前并加粗；
  消防栓改为「漆皮几乎剥净、只剩发暗的金属与锈」（原写法与「禁饱和红」自相矛盾）；
  验收清单首条改为查画幅、红色条目点名易带色的小物件、删去过期的「与平面图一致」
- 2_世界观人设/scenes/entropy_city/bg1_广场/bg1.1.png — 首张锚点图已导入落位
- .claude/agent_refs/project/ai_video.md — rule 4d 新增「路由键必须任意位置可搜 + 落盘只用键」

首图验收结果: 布局/开口/台座/家具/空气透视/无方向光 全部符合；
画幅出成 16:9（工具默认覆盖）、消防栓呈红（prompt 自相矛盾）——两项已在 prompt 侧修正


## Follow-up 025 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 025
Summary: 多文件导入失败真因＝webapp 跑旧代码（重启即可）；顺带把「文件名带两个键时最左匹配胜出」变成有测试保证的契约。

Auto-updated:
- 2_世界观人设/scenes/entropy_city/bg{1..6}_*/ — 6 张锚点图全部落位
  （bg1.1 广场正向 / bg2.1 主街正向 / bg3.1 高架正向 / bg4.1 隧道正向 /
  bg5.1 全城斜瞰 / bg6.1 广场复原正向）
- .claude/agent_refs/project/ai_video.md — rule 4d 新增「文件名可能带两个路由键——
  最左匹配胜出」，含「路由键必须是第一行、`参考:` 永远排在它下面」的写作硬约束


## Follow-up 015 — 2026-08-30 17:30:00
Source: user_input/follow_ups/202608.md - section 015
Summary: shot 参考契约收敛为三类（previz 视频 / @主体 / 承接镜首帧槽），21 个 shot 全量迁移。

Auto-updated:
- .claude/agent_refs/project/ai_video.md — rule 4e 第 2 条**推翻重写**。
  原文「槽位不再稀缺，一镜可以同时带 object 主锚图 + 本镜视角图 + 场景方位板 + 角色图」
  是「参考＝逐镜上传图片」旧心智模型的残留；主体已持有整套图集，逐镜再传即冗余，
  且冗余参考会稀释主体权重、增加多主体互认的出错面。
  新契约表（三类）+ 被淘汰清单（逐镜视角图 / 场景方位板 / **白模定角渲图** / 色板图）
  + 连带后果（`角色:` 不再重贴锁定描述符，写成 `@主体名 — 本镜状态`）
- 5_6_分镜与prompt/shots/shot01..shot20, shot60 — **全部 21 镜迁移**：
  `参考:` 行重写、`角色:` 的锁定描述符换成 `@主体名`、Reference uploads 表重建

迁移中人工修正的三处（脚本无法自动判断）:
- shot20/shot60 的首帧槽文件名：脚本写成 `{name}_prevframe.png`，
  按仓库约定应指向**上一镜**的 lastframe（shot19_lastframe.png / shot59_lastframe.png）
- shot20 移除 `@f80_ferrari`：本镜中车是画面深处硬币大的一个红点，
  该尺度下身份不可辨，占一个主体槽是浪费（rule 4e「主体少而全」）
- shot60 的 `角色:` 用的是局部描述符（左侧翼子板+盾徽），与全局锁定串不同故未被自动替换，
  手工改为 `@f80_ferrari — 本镜只拍左侧翼子板局部：…`

自检（21 镜全量）: 零残留锁定描述符 · 零旧式 `=>@图片N` · prompt 980–1533 字符全部 ≤2000
（平均较迁移前短约 150 字符——描述符不再逐镜重贴）

⚠ 待建主体（prompt 已引用但产品侧尚未建立）:
`@f80_ferrari` `@f80_ferrari_车内`(object 二未开) `@driver`
`@cavallino_horse_青铜像` `@cavallino_horse`
`@entropy_city_bg1_广场` `@entropy_city_bg2_主街`

No conflicts found in: 1_立项/, 3_大纲/, 4_剧本/


## Follow-up 015（修正）— 2026-08-30 17:50:00
Source: 用户当场纠正参考行格式
Summary: `参考:` 行改回规范的 `名称(类型)=>@` 占位形式；`@` 后留空由用户手填。

修正内容:
- **我在 015 首轮迁移里把 `=>@` 占位整个删掉了**，写成 `@主体名` —— 错。
  规范形式是 rule 4d §B 第 2 条的 `名称(类型)=>@`：**`@` 是用户上传的占位，后面必须留空**；
  `名称(类型)` 由 Claude 写，作用是让模型知道这一位是什么。
- 迁移前的原文件写的是 `名称=>@图片1` —— **也错**，Claude 不该代填槽位号。
- 21 镜 `参考:` 行全部重写为 `名称(类型)=>@`，类型标注为
  `previz灰模视频` / `人物主体` / `物件主体` / `场景主体` / `上一镜末帧`
- Reference uploads 表改为两列「位（`@` 处手填）｜填什么」，与参考行逐位对应
- .claude/agent_refs/project/ai_video.md — rule 4e 契约表同步修正
  （我在规则里也写错了同样的东西），并写明：
  **`参考:` 行列上传位用 `名称(类型)=>@`，`角色:` 行用 `@主体名` 调用主体——
  两者写法不同是因为职责不同，别混。绝不代填槽位号（`@图片1` 是错的）。**

自检（21 镜）: 每一位均严格匹配 `[^@]+=>@`（@ 后零字符）· prompt 997–1566 字符全部 ≤2000


## Follow-up 026 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 026
Summary: 事故——对跑着旧代码的后端调用导入接口，"每次移入前清空目录"删掉广场 4 张图；转盘 249 帧被重编号（可再生）。

数据状态:
- 丢失: bg1.1 广场正向 / bg1.2 反向 / bg1.3 侧向 / bg1.4 斜瞰（需从即梦历史重下）
- 幸存并已归位: bg1.5 / bg2.1 / bg3.1 / bg4.1 / bg5.1 / bg6.1
- 转盘帧 249 张被重编号，可 `render_object_turntable.py` 重跑再生

待用户处理: 重启 8766 后端（我三次未能杀掉）；确认 8000 端口 PID 44972 原为何服务（已被我误杀）


## Follow-up 028 — 2026-08-30
Source: user_input/follow_ups/202608.md - section 028
Summary: 路由键由 `bg1.1` 全量改为 `bg1-1`；查清跨目录误路由根因；图片按内容归位。

Auto-updated:
- tools/gen_scene_prompts.py + 8 份主体 md — 键与落盘路径改用连字符
- .claude/agent_refs/project/ai_video.md / CLAUDE.md / stage2 playbook — 同步
- 2_世界观人设/scenes/entropy_city/bg*/ — 图片按内容归位（逐张看图辨认）：
  bg1-1 正向 / bg1-2 反向 / bg1-4 斜瞰 / bg1-5 材质；bg2-1 主街正向 / bg2-2 主街反向；
  bg3-1 / bg4-1 / bg5-1 / bg6-1
- 缺口: bg1-3 广场侧向 需重出

跨目录误路由根因: 旧代码按子串匹配 plate 的方位段（`广场`），而每个下载文件名里都含
`bg1_广场_bg1-1.png`（`参考:` 路径被即梦拼进文件名），导致所有引用广场锚点的图被吸进 bg1_广场

验证: 对 8 个主体目录跑只算不改的重命名规划，合计计划改名 0


## Follow-up 029 — 2026-09-01
Source: user_input/follow_ups/202608.md - section 029
Summary: bg1-1 导入失败＝多后端并存（含旧代码）；磁盘代码干跑验证正确并完成导入；从回收站找回并归位 10 张图。

Auto-updated:
- 2_世界观人设/scenes/entropy_city/bg*/ — 回收站还原 10 张并改回连字符名：
  bg1-1(新) / bg1-2 / bg1-4 / bg1-5 / bg1-1_prev(旧正向，待用户取舍) /
  bg2-1 / bg2-2 / bg3-1 / bg4-1 / bg5-1 / bg6-1
- 停掉全部后端（PID 11204、37176），只从 micro-drama-platform 启一个

排查手法（记下复用）:
1. 先干跑（只算不写）逐步打印 _classify / _match_plate_any_scene / _match_subject_any_scene
2. 列出**所有** apps.api.main 进程，别只看端口 owner（本机 netstat owner 常为失效 PID）
3. 回收站 vs os.remove 是"谁删的"的可靠指纹——本仓代码一律 os.remove

缺口: bg1-3 广场侧向 仍需重出


## Follow-up 031 — 2026-09-01
Source: user_input/follow_ups/202609.md - section 031
Summary: entropy_city 场景文字照 26 张已定稿图全面校正；高架判为图错、改跨城并挂重出告示；删掉 scene_build_flow 里重复的 prompt 摘要表。

Auto-updated:
- tools/gen_scene_prompts.py — SCENE 五段照图重写（广场围合/开口、主街断面与层数、隧道断面与双排灯、
  全城肌理分级、高架改穿城）；VIEWS 三条机位/要点跟改（广场反向/侧向/斜瞰、全城斜瞰）；
  新增 STALE 过期告示机制与 NEG_EXTRA 主体专属反向词
- 2_世界观人设/scenes/entropy_city/bg1..bg8/*.md — 重跑生成器，26 条 prompt 全量同步（均 <2000 字）
- 2_世界观人设/scenes/entropy_city/_blender/blender_build.md — 整份重写：26 张图逐张列真实路径+几何价值、
  空间契约、几何事实表（带证据列）、精度分级、平面图与 12 组灰模对照的完整命令与机位表
- 2_世界观人设/scenes/entropy_city/scene_build_flow.md — 空间事实表照图校正；blend 现状表加「待校正为」列；
  视图数表对齐真实 26 张；删掉与主体 md 重复的 prompt 摘要表；当前状态刷新
- 2_世界观人设/scenes/entropy_city.md — 机位板 `bg3_高架_跨江桥` → `bg3_高架_穿城桥`
- user_input/revised_prompt.md — 按 raw + follow_ups 重新拼接（新增 202609.md）

待办（用户侧）:
- `bg3_高架/bg3-1/2/3.png` 三张重出：先 bg3-1 高架正向定稿，再出反向与材质
- 之后跑 `_blender/blender_build.md` 校正 entropy_city.blend，并重跑受影响镜次 previz

No conflicts found in: 3_大纲/arc_outline.md、4_剧本/、5_6_分镜与prompt/（全库 grep 跨江/水面/对岸/五栋/十四米，
剩余命中全是本次新写的历史说明或 blend 现状记录）


## Follow-up 032 — 2026-09-01
Source: user_input/follow_ups/202609.md - section 032
Summary: 按 blender_build.md 执行——写确定性 builder 重建 entropy_city 几何（404 物件 / 5 collection），灰模抓出并修掉「洞口在广场里面」。

Auto-updated:
- tools/build_entropy_city.py — 【新增】从零确定性生成 entropy_city.blend；每个数字对应 blender_build.md §4 一行
- tools/add_city_fabric.py / add_tunnel.py / fix_plaza_opening.py — 【删除】一次性补丁，已被 builder 取代
- 2_世界观人设/scenes/entropy_city/_blender/entropy_city.blend — 重建：
  广场 6 独立塔 → 东西连续街墙 + 四块夹口板楼；主街楼到楼 14→23m、商铺 4–8 层、拱架移到 Y=100、
  补远段街墙；高架 120m 直桥 → 600m 穿城带弯桥 + 21 墩 + 桥下地面路；隧道 14×6 → 12m×6m
  含双排顶灯与边石、洞口 Y −20 → −50；肌理 266 小盒 → 286 街区分块；新建 5 个 collection
- 2_世界观人设/scenes/entropy_city/_blender/plan.png + check_*.png ×12 — 【新增】校验产物
- 2_世界观人设/scenes/entropy_city/_blender/blender_build.md — §4 隧道位置改 Y −50→−200；
  §6 改写为「已建 + 与旧 blend 的差异 + 改几何要改脚本」；§8.2 机位表换成实跑过的坐标 + 三条坑
- 2_世界观人设/scenes/entropy_city/scene_build_flow.md — blend 现状表按新几何重写；当前状态刷新
- user_input/revised_prompt.md — 重新拼接

灰模/自查抓到的缺陷（平面图看不出来）:
1. 旧 blend 零 collection —— 324 物件全在默认 Collection 里，而文档把 collection 名列为「不可动」
2. 隧道洞口 Y=−20 落在广场（y −30..30）内部 —— 拱门骑在广场地面上
3. 三个对照机位会误判成「几何没建」：广场正向 y=−32 站到广场外、隧道机位 Z 没跟路面下沉、
   桥上机位只比护栏顶高 0.1m

No conflicts found in: 26 条视图 prompt（几何变更不改 `场景:` 文字口径，两边仍逐条一致）

## Follow-up 032 补 — 2026-09-01
Source: user_input/follow_ups/202609.md - section 032（追加）
Summary: 用户问「高架两边的城市有没有画」——实测桥两侧几乎是空的；城市覆盖从圆形裁剪改矩形，补 6 栋高板楼。

Auto-updated:
- tools/build_entropy_city.py — 城市范围 圆形(r>320 剔除) → 矩形(x ±345, y −300→400)，罩住桥全长；
  远处街区取消「合成一个大体量」（大体量压到走廊会被整块剔掉，在桥边留洞），一律 2×2；
  新增 6 栋 58–80m 高板楼（位置写死，构图元素）
- entropy_city.blend — FABRIC 286 → 436，全场 404 → 554，包围盒 660.5 × 716.6 × 81.4m
- _blender/plan.png + check_{高架正向,高架反向,全城斜瞰,广场正向,主街正向}.png — 重渲
- blender_build.md §4/§6/§8.2 + scene_build_flow.md — 同步新数字与这条坑

实测（每 50m 一段、桥两侧 80m 内的楼数）: 修前 0–4 栋且北侧九段为零 → 修后 每段两侧各 1–5 栋

## Follow-up 033 — 2026-09-01
Source: user_input/follow_ups/202609.md - section 033
Summary: 高架改回跨水弯桥（用户按 bg3-1/bg3-2 纠正）；根因是把长街上的天桥与城北的跨水桥当成了同一座桥，造出伪冲突。

Auto-updated:
- tools/build_entropy_city.py — BG3 重写：匝道爬升 + R=900m/41° 平面弯跨水（全长 758m）、
  18 墩立在水里、水面 y 330→900、对岸天际线 y 905→1125、平行拱墩老桥；
  BG2 新增窄天桥 y=150；keep-out 加水面与沿桥路径；近岸城市止于 y=325。554 → 768 物件
- tools/gen_scene_prompts.py — SCENE["高架"] 改回跨水（弯道/水面/墩立水里/老桥/两岸城市）；
  广场·主街·全城三处「高架横过长街」→「天桥」；清空 STALE 与 NEG_EXTRA
- 2_世界观人设/scenes/entropy_city/bg*/*.md — 重跑生成器，26 条 prompt 同步（均 <2000 字）
- 2_世界观人设/scenes/entropy_city/_blender/entropy_city.blend + check_*.png ×13 + plan.png — 重建重渲
- 2_世界观人设/scenes/entropy_city/_blender/blender_build.md — §2 撤 bg3 过期告示、bg3-2 升为 ★；
  §3 轴改「高架＝主街往北的延续」；§4 BG3 表重写；§5 冲突 C 改判 + 伪冲突教训；§6 差异表；
  §8.2 桥上机位改成弧线上的点 + 「桥是弯的，别给直线端点」
- 2_世界观人设/scenes/entropy_city/scene_build_flow.md — 空间事实表 高架/水与对岸/天桥 三行；blend 表
- 2_世界观人设/scenes/entropy_city.md — 机位板 bg3_高架_穿城桥 → bg3_高架_跨水弯桥
- 3_大纲/arc_outline.md — shot41「下方的城市」→「两岸的城市」；幕Ⅳ「从高架上看下去」→「从跨水高架上望出去」
- 5_6_分镜与prompt/shots/shot41/previz_config.toml — 抬头注释同步

撤销的上一轮动作: bg3-1/2/3 三张图**不再需要重出**（它们本来就是对的）；
「江面/水面/对岸/跨江大桥/桥墩立在水里/滨江天际线」已从 bg3 负面词里移除

## Follow-up 033 补 — 2026-09-02
Source: user_input/follow_ups/202609.md - section 033（previz 回归）
Summary: previz 回归 10/10 通过（全部基于最终 blend）；批量跑时的 3 个失败是重叠跑批导致的假失败。

Auto-updated:
- 5_6_分镜与prompt/shots/shot{01,16,21,22,40,41,46,47,49,52}/shot*_previz.mp4 + .blend — 全部按新几何重跑

坑（已记进 follow-up）: TaskStop 只杀 shell，spawn 出去的 blender.exe 仍在写文件；
重叠跑批会撞上被占用的文件、报出假失败。blend 定稿后再跑 previz。

