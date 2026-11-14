# 教学视频（edu_videos）

代码渲染的教学视频：数学可视化、概念动画（PPT 级）、软件/网站操作教程。画面由程序算出——准确、可复现、改一处重渲一处；不用生成式视频模型出主体画面。

## 结构

```
edu_videos/
├── README.md                 本文件：大系列约定（试行）
└── <series>/                 小系列，如 linear_algebra、machine_learning
    ├── README.md             Vision、受众、风格、知识点地图
    ├── _shared/              系列共用：配乐、包装文字 package.json、系列自己的音色（可选，覆盖频道音色）
    └── tNN_<slug>/           一个知识点 = 一支视频（中英两版同出）
        ├── script.md         中文讲稿（分段，即配音原文）；英文 script.en.md，段号句号一一对应
        ├── package.json      本期包装文字（标题、本期内容、先修、章节名、一句话、下一期，中英）
        ├── timeline.json     配音时间轴 → 动画触发点（英文 timeline.en.json）
        ├── scenes/           Manim / HyperFrames / Playwright / Blender 源码
        ├── audio/ renders/ final/   媒体，不进 git
        └── request_log.md    外部服务请求日志（RequestLog 自动定位到此）
```

系列 README 可在系列级覆盖本文件的约定：`redian_xiangying`（热点相迎）以热点开场讲认知，画面另用真实素材与 Seedance 模拟视频，规则见其 README。

目录名用英文 slug。`tNN` 是稳定编号，调整顺序不改号，播放顺序以系列 README 的知识点地图为准。

## 工具（本机，2026-11-08 冒烟测试通过）

| 用途 | 工具 | 许可 | 调用 |
|---|---|---|---|
| 数学 2D/3D | Manim CE 0.22.1 | MIT | `.cache/venvs/manim/Scripts/manim`；公式依赖 MiKTeX（用户 PATH） |
| PPT 级动画、概念图、字幕 | HyperFrames 0.9.21 + KaTeX 0.16.11 | Apache-2.0 / MIT | `.cache/node/hyperframes/node_modules/.bin/hyperframes` |
| 软件/网站教程 | Playwright 录真实界面 + ffmpeg 叠光标、点击、放大 | Apache-2.0 / — | 系统 Python |
| 3D 实体、开场 | Blender 5.x | GPL（产出不受限） | `tools/blender_exe.py` |
| **画面（默认）**：网页场景（排版、D3 图表、GSAP 动效） | HyperFrames + GSAP 3.13 + D3 7 + MiSans | Apache-2.0 / GSAP 标准许可 / ISC / MiSans 许可（免费商用，须注明） | `tools/edu_web.py`；每期 `scenes/web/sN.html` + `scenes/data.py`；共用 `_shared/design/web/`（tokens.css、base.css、runtime.js） |
| 统一包装（片头、本期内容、章节转场、片尾） | HyperFrames + GSAP 3.13 + MiSans | Apache-2.0 / GSAP 标准许可（免费、可商用） / OFL | `tools/edu_package.py`；模板 `_shared/package/template.html`，样张 `styleboard.html` |
| 配音 | VoxCPM2 本地（频道男声，中英文同一音色；2026-11-08 选定） | Apache-2.0（成片须注明 AI 配音、不得冒充真人） | `tools/edu_video.py tts` → `.cache/venvs/voxcpm` 跑 `tools/edu_voxcpm.py`；选型样音在 `_shared/voice_lab/` |
| 字级时间戳 | faster-whisper | MIT | 系统 Python |
| 配乐 | ACE-Step 本地 / Suno | MIT / 见 paid_services | Suno 走 `suno-music` skill，下载额度有月上限 |
| 插图 | Codex 内置出图 | 见 paid_services | `tools/codex_image.py --out edu_videos/<系列>/<知识点>/...` |

## 设计规范

**频道设计规范 v1**：`_shared/design/design_system.md`（数值唯一来源 `tokens.json`），2026-11-08 用户选定 S3 浅色舞台 · P3 暖琥珀 · F3 MiSans · I1 哑光陶土 3D；对比样张与定稿样张在 `/character-review?path=edu_videos/_shared/design`。画面默认用网页场景（`tools/edu_web.py`），Manim 只留给数学变形；需要用户挑选的设计问题一律做成多选项并排对比（用户 2026-11-08）。对标调研与学习科学证据：`_shared/research/explainer_benchmark.md`。给外部设计师的需求说明：`_shared/design/designer_brief.md`。

## 审查（三层，2026-11-08 起）

1. **程序检验**（每次出片，不花钱）：`python tools/edu_review.py validate <知识点>` 查配音、字幕、语速、画面自检（`tools/edu_web.py check`）、事实台账 `claims.json`、成片响度与时长；必改清零才往下。
2. **专家审稿**（独立上下文，按句号出意见）：`python tools/edu_review.py brief <知识点> --stage script|cut` 开一轮，角色与必查项在 `_shared/review/roles.json`——讲稿编辑（精炼）、好老师（例子 / 类比 / 认知与启发 / 误解）、事实核查、中文与英文母语听感（盲审，换 Codex 审）、双语编辑（只比语义不比字面）、美术指导、AI 学生（只用来筛题）。审完 `merge` 汇成 `issues.md`，逐条写处理结论，最多 3 轮。
3. **理解测验**（真人为准）：每期写讲稿前先定 `learning.json`（学习目标、迁移题为主的测验、讲回来要点、常见误解）；成片后 3–5 位真人盲看：前测 → 看片 → 后测 → 讲回来。AI 学生会泄露已有知识，只能用来筛题和找漏洞，不作过关依据。

讲稿阶段先审（改字最便宜），成片阶段再审画面与听感。

**台词审 v2（口播＋屏幕文字，用户 2026-11-08，借鉴 Portal Travel 审查单）**：配音与渲染之前必过。`python tools/edu_review.py new <知识点>` 开 `reviews/lines_rN/`，四项、标准各不相同：中文口播、英文口播（母语盲审，只读按播放顺序的口播，查「像真人在讲 / 衔接 / 一遍听懂 / 精炼 / 口吻 / 改写」）、中文屏幕文字、英文屏幕文字（逐句截图＋可见文字与字数，查「只列纲要 / 与口播分工 / 层级体例 / 措辞排版 / 看得完」，带硬上限）。每项 a 位 Claude、b 位 Codex 独立审，每维 0–3 分、高分要证据；`check` 校验格式并对比：分歧（差 ≥2 或一人 ≤1 一人 ≥2）与两人都过的维度抽 2 维交 Claude Opus 裁决；`issues` 汇总最终分与问题，逐条写处理；第 2、3 轮加 R 复核上一轮。每项每维最终 ≥2 且无未处理的必改才算通过。**审查结果都记在审查单下**（用户 2026-11-08）：`issues.json` / `issues.md` 每条问题编号 I1…，处理用 `fix`（按编号或「项＋位置」批量）登记方案、状态（已改 / 不改＋理由）和改了的文件；`conclude` 收轮写 `结果.md`；每一步同时写管理站读的 `checklist.json`，在 `/review-run?path=edu_videos/<系列>/<知识点>/reviews/lines_rN` 看评分、裁决、问题清单与处理。下一轮 `new` 自动带上一轮的处理，审稿人用 R 逐条复核。**v3（用户 2026-11-09，「现实里的祸，和怎么防」过了三轮没拦住）**：口播审稿报告必须有「## 逐句复述」——每句先写「跟朋友会怎么说」再对比，少于八成句子判报告不合格；开场、串场、章节过渡、片尾与章节标题有一点怪就算必改，最后一轮也不放宽；程序口语黑名单（`lint`）先标可疑句，写进任务书交审稿人逐条判；讲稿大改后用 `new --chain <名>` 另起一条审查链。标准只改 `_shared/review/line_review.json`。

## 制作流程（试行；试点跑通后定稿，再升为共用 skill）

工具链：`tools/edu_video.py`（tts / qa / timeline / package / sheet / preview / mux，都可加 `--lang en`）、`tools/edu_package.py`（包装卡）与 `tools/edu_manim.py`（`CuedScene`：按句触发动画、侧边面板排版与层级；`tr("中文", "English")` 取当前语言）。频道统一的音色在 `edu_videos/_shared/voice.json`（`engine` + 参考音 `_shared/voice/host_m_voxcpm.wav` 及原文；系列 `_shared/voice.json` 可覆盖），视觉常量在 `edu_videos/_shared/style.py`。

1. **讲稿** `script.md`：`## sN` 画面段、`- lNN: 文本` 一句（数字写汉字；`[停N]` 句后停顿）。一支只讲一个知识点，**3–5 分钟、一个概念讲透、例子宁少勿多**（用户 2026-11-09：t01 七分钟太长，例子一个就够）；先直觉后公式。
   **先说后写**（用户 2026-11-09）：讲稿不从书面稿往口语改。先写「每一拍要讲清楚的意思和事实」（不写措辞），再让中文、英文各一位讲解员（另起上下文的模型，不给旧稿）像跟朋友聊天一样把每段说出来，作者只剪短、核对事实与限定语；跑 `python tools/edu_review.py lint <知识点>`（口语黑名单）清零或逐条说明后才进台词审。
   段标题可带 `[章:<id>]`（段前插章节转场卡）、`[包装:agenda]` / `[包装:outro]`（该段画面用本期内容 / 片尾卡，卡上各项随该段每句出场）；系列有 `_shared/package.json` 时自动加片头卡。
   英文稿 `script.en.md` 段号、句号、标签与中文一一对应（工具会核对），停顿写 `[pause N]`；按英文口语重写，不逐字直译。
2. **配音**：`tts`（本地克隆频道音色，逐句）→ `qa`（faster-whisper 回听：中文拼音音节错率、英文单词错率与语速，超标的在 `<audio>/lines/takes.json` 换种子重出）→ `timeline`。配音是时间主轴；英文版各命令加 `--lang en`，产物在 `audio/en/`、`timeline.en.json`。
3. **画面**：`scenes/` 里每段一个 `CuedScene`，`self.at("lNN")` 等到该句开口再动画；数值用 numpy 算；画面文字一律 `tr()`。先按估算时间轴出低清草稿看图，配音定稿后再出 1080p；英文版 `EDU_LANG=en` 渲到 `renders/en/`。包装卡 `package` 按时间轴渲到 `renders/package/<lang>/`。
4. **审片**：`sheet` 每句抽一帧拼总览图，自己看一遍，再另起上下文独立审稿（目标观众 + 专业老师两种视角），按下方清单；两种语言都要看。
5. **合成**：Manim 输出拷成 `renders/[en/]sN.mp4` → `mux`（拼接、配音响度归一、配乐自动压低、烧录字幕）→ `final/<知识点>[.en].mp4` → `preview`（管理应用单集预览页，页头可切换中英文）。
6. **标注**：成片片尾卡自带「AI 配音」标注（VoxCPM2 模型卡要求），发布说明里也写明。

**审片清单**（t03 独立审稿抓到的问题，逐条查）：
- 记号前后一致：变换后统一带撇（î′、v⃗′）；「落点」只说原向量的（不写「î′ 的落点」）。
- 每个结论都有一句「为什么」，并回扣开头的问题；不能只靠一个数例「对上」。
- 演示的变换要看得出变化：对称变换（旋转 90°、网格自身重合）要放不对称参照物。
- 定义要严谨到不被反例推翻，口语化不能牺牲正确性。
- 开头 15 秒内要有动画，不能全是静态公式。
- 文字卡片压在点阵、网格之上（z_index）；标签不压箭头、不被轴线穿过（加底）。
- 公式面板及面板上的高亮框、圈注都要高于网格层级：Manim 的整组 `Rotate`、`Circumscribe` 会把对象提到最上层或画在面板下面。
- 现实案例逐个数字核对**是谁做到的**：t01 初稿把「另训一个模型认出医院 99.9%」说成肺炎模型自己认医院，是独立审稿抓到的；引原话照原意译（part…part 不是「一半…一半」），术语照原文（cases 是数据点不是病例）。
- 演示里拿测试集挑了模型，讲对策时要说明「实际该用验证集」，否则就是在教数据泄漏。
- 片头本期内容卡要覆盖全部章节；先修里说「片中一句话带过」的，每一条都要真带过（如「误差」）。
- 英文版画面字逐张核对出框（英文比中文长）；字幕与念法不同的数字写 `{显示|念法}`。
- 定义类的话全片前后一致：一处说「AI 不写规则」、另一处说「AI 包括人写规则」就自相矛盾；常驻角标别和后面的结论打架（ai_terms t00 审稿）。
- 小实验交代清楚怎么算的：随机抽样要说明抽法与覆盖（「随便抽十个，有的数字一张没见过」），取中位数、对数刻度在画面上用小字注明；画面用词和口播一致。
- 否定一条规则或说法时给反例（「8 也有两个弯」），不能只打叉；叉不要画在本来就是否定句的字上。
- 回听核对已认数字的两种念法（逐位 2024 → 二零二四、位值 1797 → 一千七百九十七、37% → 百分之三十七）与英文 %、连字符、重音字母；仍报错的再人工判断。
- 配音回听按拼音比对（识别把「矩阵」写成「举证」不算错），重点听有没有吞字：本地音色念「i 和 j」容易吞掉 j，改写法绕开（「i 落到哪、j 落到哪」）。
- **本期内容不逐行念目录**（用户 2026-11-08）：口播用一两句自然的话串起来（「这期，我们先用一个小实验……再聊聊……」），目录卡各行在口播里均匀出现；目录项就是章节卡标题（`package.json` 写 `"agenda": "chapters"`），编号、叫法与章节卡、页眉全片一致。
- **屏幕只列纲要**（用户 2026-11-08，t01 台词审三轮）：关键词、数字、短语；新一屏出来旧说明先收走；不把口播整句印上屏，也不印口播没说过的术语（偏离²、中位数、多项式次数、「指纹」都被抓过）；标题可以换成当句结论代替右侧说明栏；结论词（过拟合、捷径学习）做主标题，不能是全屏最小的字。计数口径见 `_shared/design/design_system.md` 7.5 节。
- 还没揭晓的数字显示「—」，不能先显示 0.00（`EDU.count` 会保留原文直到开始滚动）；容器整体透明时子元素淡入也看不见（t01 l40 空白 7 秒）。
- 中文回听把小数写成「99.9%」时按「九十九点九」比对（`number_variants` 已处理小数），不算念错。

## 规则

- **商用**：只用可商用工具；中文字体用 Noto Sans SC，英文与纯数字用 Inter（均 OFL；Manim 里 Inter 从 `.cache/fonts/inter/` 按进程注册，`style.zh()` 自动选字体），不用微软雅黑；edge-tts（微软在线服务）不进成片。GSAP 3.13 起由 Webflow 全部免费（含商用，标准许可禁止拿它做与 Webflow 竞争的可视化建站工具，与我们无关）。
- **外部服务**照 `CONVENTIONS.md`「外部服务请求审计」先记日志；目标路径写在 `edu_videos/<系列>/<知识点>/` 下。
- **媒体不进 git**（`.gitignore` 已排除）。
- **HyperFrames**：遥测已关；不用 `publish`（会上传 HeyGen）；外链样式表不生效，KaTeX 等放本地；字体用 `@font-face` 声明。

## 系列

| 系列 | 目录 | 状态 |
|---|---|---|
| 线性代数 | [linear_algebra/](linear_algebra/README.md) | t03 试点成片（2026-11-08，4 分 22 秒） |
| AI 高频词 | [ai_terms/](ai_terms/README.md) | t01 过拟合 v2（模板 v2、中英双语，2026-11-08） |
| 系统化中频交易 | [quant_mft/](quant_mft/README.md) | 建系列、知识点地图 25 期（2026-11-08）；t01 试点规划中 |
| 探索（真人写实、两人问答，第一季芯片） | [tansuo/](tansuo/README.md) | t01 故事板 v4（定稿主角林 G9、凯 K1）待用户预览（2026-11-14）；画面为系列级例外，见其 README |
| 机器学习 | `machine_learning/`（未建） | 设想 |
| 软件/网站教程 | 待定 | 待定教哪个工具 |
