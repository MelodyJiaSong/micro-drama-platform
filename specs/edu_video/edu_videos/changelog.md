
## Follow-up 001 — 2026-11-08 10:25:43
Source: user_input/follow_ups/202611.md - section 001
Summary: 新建 edu_videos 结构、线性代数知识点地图，请求日志支持 edu_videos 归属

Auto-updated:
- edu_videos/README.md — 新建：大系列结构、工具与许可、试行流程、规则
- edu_videos/linear_algebra/README.md — 新建：Vision、受众、15 个知识点地图，试点 t03
- specs/edu_video/edu_videos/user_input/raw_prompt.md — 新建：原始意图
- tools/service_request.py — RequestLog 接受 edu_videos/<系列>/<知识点>/ 归属，根目录报错
- tools/tests/test_service_request.py — 新增 edu_videos 归属与根目录用例
- tools/codex_image.py — --out 帮助文字含 edu_videos
- AGENTS.md — 加教学视频路由
- CONVENTIONS.md — Repo layout 加 edu_videos；task_type 加 edu_video
- .agents/references/project/paid_services.md — Codex 出图目标可在 edu_videos 下
- .agents/skills/codex-imagegen/SKILL.md、.agents/skills/suno-music/SKILL.md — 目标路径含 edu_videos
- .gitignore — edu_videos 媒体不进 git
- 本机（不入库）— .cache/venvs/manim（Manim 0.22.1）、.cache/node/hyperframes（HyperFrames 0.9.21、KaTeX 0.16.11，遥测已关）、MiKTeX 25.12 用户级安装

验证: pytest test_service_request/test_codex_image/test_suno_request_audit 28 passed；git check-ignore 确认 mp4 忽略、README 入库；sync_agent_skills --check、workflow_catalog --check 通过；Manim（公式、中文、3D）与 HyperFrames（中文、KaTeX）冒烟渲染看图通过

No conflicts found in: （未单独核查）


## Follow-up 002 — 2026-11-08 12:04:51
Source: user_input/follow_ups/202611.md - section 002
Summary: t03 试点成片与配音/时间轴/字幕/合成工具链

Auto-updated:
- edu_videos/linear_algebra/t03_matrix_as_transform/{research.md,script.md,scenes/t03.py,timeline.json} — 调研、讲稿 33 句、六段 Manim 动画、配音时间轴
- edu_videos/linear_algebra/_shared/{voice.json,style.py,music/gen_v1.json} — 系列音色（MOSS 设计音色 teacher_m 种子1）、视觉常量、ACE-Step 配乐 bgm_v1_s11（本地，MIT）
- tools/edu_video.py — tts/qa（拼音比对）/timeline/sheet/mux（逐段补齐末帧、响度归一、配乐自动压低、烧录字幕）
- tools/edu_manim.py — CuedScene：按配音句子时间触发动画
- edu_videos/README.md — 工具链、试行流程、审片清单、系列状态
- 成片（不入库）final/t03_matrix_as_transform.mp4，263.1 秒，1080p30，5d529bae92d37959；配音 takes：l19 种子2、l22 种子2

验证: 配音 faster-whisper 拼音比对全部通过；两轮独立审稿（目标观众+数学老师）：首轮 9 条与终审 A–G 均已修复并看图复核（s3/s4/s5 总览图、旋转段抽帧）；成片响度约 -17 LUFS，音画时长一致；终审之后的修复未再送独立审稿
费用: 全部本地运行，无付费服务调用

No conflicts found in: （未单独核查）


## Follow-up 003 — 2026-11-08 13:12:06
Source: user_input/follow_ups/202611.md - section 003
Summary: 新建 ai_terms 系列，t01 过拟合成片；频道级共用风格与音色

Auto-updated:
- edu_videos/ai_terms/{README.md,t01_overfitting/script.md,t01_overfitting/scenes/t01.py,t01_overfitting/timeline.json} — 新系列 Vision 与词表；t01 讲稿 24 句、七段动画，数据全部由 numpy 实验算出（种子 99、300 次中位数、岭回归 λ=0.01）
- edu_videos/ai_terms/t01_overfitting/assets/{student_v1,exam_v1}.png — Codex 出图两张（日志 t01_overfitting/request_log.md），第二张以第一张为参考保持角色一致
- edu_videos/ai_terms/_shared/music/bgm_v1_s11.wav — ACE-Step 本地电子配乐（MIT）
- edu_videos/_shared/{style.py,voice.json} — 风格与音色由线性代数系列提为频道级；t03 import 路径同步
- tools/edu_manim.py — CuedScene 收入 dur/mid/fit/fade_all/stack（面板层级 TOP）；t03 去重
- tools/edu_video.py — voice.json 频道级回退；字幕冒号必断、每屏 20 字
- 成片（不入库）final/t01_overfitting.mp4，195.4 秒，1080p30，-17.2 LUFS，2375fe07b6455293；takes：l19 种子2、l22 种子2

验证: 配音拼音比对全部通过（l19 两次跑飞/读错后改写法重出）；独立审稿 1 轮（观众/从业者/画面三视角）13 条全部修复，修复后自己看总览图与成片抽帧复核，未再送独立审稿
费用: Codex 内置出图 2 次（ChatGPT 订阅额度，费用未知）；其余本地

No conflicts found in: （未单独核查）


## Follow-up 004 — 2026-11-08 13:37:32
Source: user_input/follow_ups/202611.md - section 004
Summary: 系列片包装、内容框架、中英双版本与配音升级

Auto-updated:
- edu_videos/_shared/package/styleboard.html（+ renders/f1–f5.png，不入库） — 系列包装风格样张：片头、本期内容与先修、章节转场、片尾、英文片头
- edu_videos/ai_terms/README.md — 节目模板 v2 草案：包装 + 问题 / 类比 / 实验 / 视角 / 现实 / 对策 六段

验证: 样张用本机 Chrome 渲染后看图确认（修了渐变字下伸部被裁）；配音方案（ElevenLabs 付费）、模板与样张风格待用户确认后再做包装动画、双语管线与 t01 重制

No conflicts found in: （未单独核查）


## Follow-up 005 — 2026-11-08 14:08:44
Source: user_input/follow_ups/202611.md - section 005
Summary: 本地 TTS 选型实验：Qwen3-TTS、VoxCPM2 与现用 MOSS 对比

Auto-updated:
- edu_videos/_shared/voice_lab/{texts.json,lab_qwen.py,lab_voxcpm.py,build_review.py,review.json} — 选型实验脚本、试听审阅数据（样音 wav 不入库）
- .agents/references/project/paid_services.md — 商用表登记 Qwen3-TTS、VoxCPM2（允许，选型试用）与 VibeVoice（不用：仅研究、输出带可听 AI 声明）
- 本机（不入库）— .cache/venvs/{qwen3-tts,voxcpm}（torch 2.11 cu128），.cache/models/{qwen3-tts-voicedesign,qwen3-tts-base,qwen3-tts-tokenizer,voxcpm2}

验证: 14 条样音全部生成；faster-whisper 回听：Qwen3-TTS 与 VoxCPM2 中英文音节 / 单词错率 0–2%，MOSS 英文 10%；同段中文 Qwen 16.8 s、VoxCPM 15.7–17.8 s、MOSS 22.0 s；生成速度约 4–6 秒算力 / 1 秒音频；管理应用审阅页看图确认可播放。音色好不好听待用户试听选择

No conflicts found in: （未单独核查）


## Follow-up 007 — 2026-11-08 17:59:47
Source: user_input/follow_ups/202611.md - section 007
Summary: 新建 quant_mft 系列：Vision、受众、模板与知识点地图

Auto-updated:
- edu_videos/quant_mft/README.md — 新系列：Vision、受众、六段模板（问题/直觉/机制/实验/难点/影响，数据期对应类型特点/难点/影响力）、四单元 25 期知识点地图、系列规则（不构成投资建议、事实逐条核对、数据可商用）
- edu_videos/quant_mft/_shared/package.json — 系列包装文字与章节轨，片尾标注 AI 配音与不构成投资建议
- edu_videos/README.md — 系列表登记 quant_mft
- .agents/references/project/workflow_catalog.json — 登记系列 README（1.7.15）

验证: package.json JSON 解析通过；workflow_catalog --fix / --check 编号连续；未做独立审稿（只建系列地图，无讲稿与成片）

No conflicts found in: （未单独核查）


## Follow-up 006 — 2026-11-08 16:41:10
Source: user_input/follow_ups/202611.md - section 006
Summary: 频道配音定为 VoxCPM2 男声，接入 edu_video.py tts

Auto-updated:
- edu_videos/_shared/{voice.json,voice/host_m_voxcpm.wav,style.py,package/template.html}; edu_videos/ai_terms/_shared/package.json; edu_videos/ai_terms/t01_overfitting/{script.md,script.en.md,package.json,research.md,scenes/t01.py,assets/*_v2.png,assets/cat*,assets/dog*}; tools/{edu_voxcpm.py,edu_package.py,edu_video.py,edu_manim.py}; edu_videos/README.md; edu_videos/ai_terms/README.md; .gitignore; paid_services.md; workflow_catalog.json

验证: VoxCPM2 中文 47 句、英文 47 句 faster-whisper 回听全部通过（英文 l28 换种子 2）；中文版 335.3 秒、英文版 355.0 秒，响度均 -15.9 LUFS；渲染无迟到 / 溢出告警；独立审稿 15 条：3 个 BLOCKER（l37 99.9% 实为另训模型、l35 原话误译与 cases 误读、英文画面字出框）与 SHOULD-FIX 已改并对原文复核；管理应用预览页中英切换实测可用；tools/tests 265 通过；workflow_catalog --check 通过

No conflicts found in: （未单独核查）


## Follow-up 009 — 2026-11-08 19:14:55
Source: user_input/follow_ups/202611.md - section 009
Summary: 教学视频审查机制（程序检验已落地）、设计选型对比样张、同类对标调研

Auto-updated:
- tools/edu_review.py（validate：配音、字幕、节奏、画面自检、事实台账、成片响度与时长）；tools/edu_manim.py（CuedScene 每次动画后查出框、压字幕带、文字重叠）；edu_videos/ai_terms/t01_overfitting/claims.json；edu_videos/_shared/research/explainer_benchmark.md；edu_videos/_shared/design/{boards/build_boards.py,review.json,samples/illus_*.png,designer_brief.md}；.cache/fonts/{harmonyos_sc,misans}（官方下载，授权已读）；.cache/node/hyperframes（d3 7、@fontsource/inter）；workflow_catalog.json

验证: validate 在 t01 上跑通：先抓出 8 处未登记事实与旧评分误报，修正后必改 0；三路调研（YouTube 14 支、B 站 22 支带数据与评论、学习科学文献）完成并整理；设计选型 4 组 12 张样张在 /character-review?path=edu_videos/_shared/design 可看。待用户选型后：写设计规范、审稿标准与学生测验、按新规范重做 t01

No conflicts found in: （未单独核查）


## Follow-up 008 — 2026-11-08 18:00:07
Source: user_input/follow_ups/202611.md - section 008
Summary: ai_terms 新增 t00 什么是 AI（系列开篇），按模板 v2 制作

Auto-updated:
- edu_videos/ai_terms/t00_what_is_ai/ — 新建 t00「什么是 AI」：讲稿 v1（Manim 黑底，独立审稿 2 轮）→ v2.3（频道设计规范 v1 浅色网页场景，讲稿审 3 轮，reviews/script_r1–r3/issues.md 逐条写处理结论）；script.md / script.en.md，v1 存 script_v1*.md
- edu_videos/ai_terms/t00_what_is_ai/{learning.json,claims.json,research.md,package.json} — 学习目标 6 条 + 迁移题 6 道；事实台账 C01–C23（凭记忆的原话已标待核）；案例出处核对（AlphaFold、ChatGPT、亚马逊、UCI 数据集 CC BY 4.0）
- edu_videos/ai_terms/t00_what_is_ai/scenes/{data.py,web/_lib.js,web/s0,s2–s9.html} — 手写数字实验（scikit-learn digits，带断言：37/88/97%、错 10 题、A→4 92%、2→1 81%）与浅色网页场景；旧 Manim 场景移到 scenes/_v1_manim/
- edu_videos/ai_terms/t00_what_is_ai/assets/clay_{phone_cat,child,cook_recipe,cook_taste}_v1.png — Codex 出图 4 张（陶土 3D，request_log.md 有记录）；v1 卡通图移到 assets/_v1/
- edu_videos/ai_terms/t00_what_is_ai/final/t00_what_is_ai[.en].mp4 — 成片 zh 467.7 秒 / en 482.4 秒（VoxCPM2 本地配音、bgm_v1_s11）
- tools/edu_video.py — 回听核对：中文数字两种念法（逐位 / 位值）、百分号、×；英文 %、连字符、重音、千分位逗号、NxN
- tools/edu_package.py — 每期 package.json 可覆盖 prereq_hint
- edu_videos/README.md — 审片清单加 4 条（定义前后一致、实验抽法交代、否定给反例、数字念法回听）；edu_videos/ai_terms/README.md — 词表加 t00
- edu_videos/ai_terms/t00_what_is_ai/ — v2 完成：讲稿审 3 轮（reviews/script_r1–r3）定稿 v2.3 后再按成片审 3 轮（reviews/cut_r1–r3）改字：l01/l23/l27/l32/l37/l38/l41/l45/l46/l47 收紧说法、补「训练」解释，中英相关句重配并回听通过
- edu_videos/ai_terms/t00_what_is_ai/scenes/web/*.html, _lib.js — 成片审修正：英文逐词示例词距、圈层只用墨 + 琥珀、考试成绩琥珀空心、三提醒卡等分加大、规则 / 例子标签对齐、英文出界与重叠、text-wrap: balance
- edu_videos/ai_terms/t00_what_is_ai/assets/clay_*_v1_cut.png — 陶土插图抠掉棚拍底色（羽化），场景改用透明版，不再露出方框
- edu_videos/ai_terms/t00_what_is_ai/final/t00_what_is_ai[.en].mp4 — 成片 zh 475.3 秒 / en 485.3 秒；preview.json / preview.en.json 已更新
- edu_videos/_shared/package/template.html — 片尾署名上移出字幕带、左右对齐 120（频道共用，影响以后重渲的各期片尾）
- edu_videos/_shared/review/roles.json — AI 学生的「讲回来」改为按 quiz.md 的讲回来题（原写死过拟合）
- tools/edu_video.py — 英文字幕：逗号后的右引号跟前半句；英文回听：千分位逗号、NxN
- edu_videos/ai_terms/README.md — t00 状态改为 v2 完成、待真人测验

验证: edu_review validate：必改 0（中英）；edu_web check 中英版式无问题；配音回听全部通过；讲稿审 3 轮 + 成片审 3 轮（Claude 编辑/老师/双语/美术/AI 学生 + Codex 事实/中文/英文听感），成片审第 3 轮必改 4 条已改并重渲；AI 学生两身份 6 题全对、可指出出处；真人理解测验未做（需真人）
费用: Codex 出图：v1 卡通 3 张 + 陶土 4 张（订阅额度，费用未知）；Codex 文字审稿 15 次（gpt-6.1-sol）

No conflicts found in: （未单独核查）

## Follow-up 010 — 2026-11-08 20:13:03
Source: user_input/follow_ups/202611.md - section 010
Summary: ai_terms 取消 3–5 分钟时长限制，质量优先

Auto-updated:
- edu_videos/ai_terms/README.md — Vision 与节目模板去掉时长限制：时长不设上限，质量优先，不为控制时长删减内容

验证: README 文字已改；t00 未删任何内容（成片约 7.8–8 分钟）

No conflicts found in: （未单独核查）


## Follow-up 012 — 2026-11-08 22:37:35
Source: user_input/follow_ups/202611.md - section 012
Summary: 新增台词审 v2（edu_review new/check/issues + line_review.json）：口播与屏幕文字 × 中英四项，每项 Claude/Codex 双审 0–3 评分带证据，分歧与抽查交裁决，最多 3 轮；edu_web screen_dump 逐句导出可见文字与截图；t01 全片按此复审、修正、重做。

Auto-updated:
- tools/edu_review.py（new/check/issues/fix/conclude、write_checklist）；edu_videos/_shared/review/line_review.json；tools/edu_web.py（screen_dump）；tools/edu_package.py 与 _shared/package/template.html（目录=章节卡、单语卡、片尾页眉）；_shared/design/web/runtime.js（count 不先写 0）；tools/edu_video.py（中文小数回听）；t01 script v4.2 中英、package.json、scenes/web/s0–s9；edu_videos/README.md、design_system.md 7.5；workflow_catalog.json

验证: 台词审三轮 reviews/lines_r1–r3（每轮 4 项 × Claude/Codex 双审 + Opus 裁决，处理全部登记：r1 已改 218 / 不改 9，r2 已改 104 / 不改 38，r3 已改 37 / 不改 66）；第 3 轮口播两项通过，屏幕文字两项的必改（片尾卡、l22）已按裁决修好；配音回听中英全部通过；edu_web check 中英无问题；edu_review validate 必改 0（中文 420.1 s、英文 427.7 s，响度 −15.9 LUFS）

No conflicts found in: （未单独核查）


## Follow-up 011 — 2026-11-08 20:40:16
Source: user_input/follow_ups/202611.md - section 011
Summary: 频道设计规范 v1 落地（网页场景渲染、包装换肤、陶土插图）与《过拟合》v3 讲稿三轮审查、中英重做

Auto-updated:
- t01 v3.3 讲稿与场景、配音、成片（已被台词审 v4.2 取代）

验证: 被 012 的三轮台词审与 v4.2 成片取代；最终成片 final/t01_overfitting[.en].mp4 程序检验必改 0

No conflicts found in: （未单独核查）


## Follow-up 013 — 2026-11-09 08:19:47
Source: user_input/follow_ups/202611.md - section 013
Summary: 流程：先说后写（讲解员模型按意思口述成稿）；台词审 v3 加逐句「跟朋友复述」（报告缺了不合格）、串场句与章节标题从严、口语黑名单 lint、审查链 --chain；t01 改成 v5 约 4 分钟：5 章（定义＋学生比方、小实验、学习≈压缩、谷歌流感趋势、怎么防），去掉本期内容卡、认猫、300 次实验、胸片、皮肤癌。

Auto-updated:
- edu_videos/_shared/review/line_review.json（v3：retell、strict、例句）；tools/edu_review.py（lint 口语黑名单、逐句复述校验、从严条目进任务书与裁决、--chain 审查链、analogy 台账、片尾截图避开淡出）；tools/edu_web.py（只计可见文字）；tools/edu_package.py 与 template.html（按本期章节编号、片尾署名与结论行对比度、片头下伸部）；t01 讲稿 v5.4 中英（43 句、5 章、约 4.5 分钟）、package.json、claims.json、learning.json（Q5 换题）、scenes/web（s5/s6 归档）；edu_videos/README.md

验证: 先说后写：中英讲解员各自口述成稿；台词审 v3 审查链 lines5_r1–r3（每轮 4 项 × Claude/Codex 双审 + Opus 裁决，处理全部登记：r1 已改 65 / 不改 66，r2 已改 58 / 不改 50，r3 已改 29 / 不改 73）；口语黑名单零命中；配音回听中英全部通过；edu_web check 中英无问题；edu_review validate 必改 0（中文 287.7 s、英文 267.3 s，响度 −15.9 / −16.0 LUFS）

No conflicts found in: （未单独核查）


## Follow-up 015 — 2026-11-09 12:28:23
Source: user_input/follow_ups/202611.md - section 015
Summary: AI 高频词新增 t09 拉格朗日乘子：按 v5 流程（先说后写、台词审 v3、3–5 分钟一个例子）制作中英两版；实验为围栏内找最高点（程序算出），AI 例子为 Safe RLHF 自动调 λ，另带正则化、KL 系数一句

Auto-updated:
- edu_videos/ai_terms/t09_lagrange/（讲稿、场景、包装、审查单 lines_r1–r3、成片）；edu_videos/_shared/package/template.html（片头片名自动缩字号）；tools/edu_video.py（英文回听：小数逐位、拼读缩写）；edu_videos/ai_terms/README.md

验证: edu_review validate 必改 0（−16 LUFS 中英）；edu_web check 中英版式无问题；lint 0 命中；edu_video qa 中英全部通过；tools/tests -k edu 6 passed；台词审 3 轮收轮
费用: Codex 出图 1 张（clay_kid.png，已记 request_log）

No conflicts found in: （未单独核查）


## Follow-up 014 — 2026-11-09 12:19:59
Source: user_input/follow_ups/202611.md - section 014
Summary: t00 成片追加母语听感审稿轮（cut_r4），按结论修讲稿/画面并重渲染，提供预览 URL

Auto-updated:
- edu_videos/ai_terms/t00_what_is_ai/script.md, script.en.md — 按新频道规则重写为 v3（52 行，去 AlphaFold/诺奖/ChatGPT，实例只留亚马逊），v2 归档为 *_v2
- edu_videos/ai_terms/t00_what_is_ai/package.json, claims.json, learning.json — 章节/引语/事实条目按 v3 重映射
- edu_videos/ai_terms/t00_what_is_ai/scenes/web/s0–s9.html — 屏幕改为提纲、按字数上限精简；旧场景归档 scenes/web/_v2/
- edu_videos/ai_terms/t00_what_is_ai/audio — v3 中英逐句重录并过 qa（旧音频归档 audio/_v2/）
- tools/edu_video.py — package：片尾行数不足时引语 cue 均分；qa：英文 8x8/复数数字/合成词误报修正
- edu_videos/ai_terms/t00_what_is_ai/reviews/lines_r1/ — 台词审第 1 轮：Claude a 侧 4 份报告完成；Codex b 侧首轮 13:24 断网挂死已杀掉重跑（进行中）
- edu_videos/ai_terms/t00_what_is_ai/reviews/lines_r1–r3 — 台词审 v3 三轮：中英口播（母语盲审）+ 中英屏幕，Claude/Codex 双审、Opus 裁决，225+141+107 条全部登记处理；末轮按清单改完交程序检验
- edu_videos/ai_terms/t00_what_is_ai/script.md, script.en.md — 按审稿改开场、串场、片尾与多处母语听感；删教小孩类比段（s4）与 l29，时长 6:00 → 5:24；按事实核查加限定（l31/l44/l45/l52）
- edu_videos/ai_terms/t00_what_is_ai/scenes/web/*.html, package.json — 屏幕只放纲要、字数合规、弯撇号统一、章节眉题一致、片尾补回「主要/most」；s4 移到 scenes/web/_cut/
- edu_videos/ai_terms/t00_what_is_ai/reviews/cut_r4/issues.md — 成片审（事实核查、中英母语、美术、AI 学生）188 条逐条处理；残留旧 s1/s4 总览图与渲染已删除
- edu_videos/ai_terms/t00_what_is_ai/final/t00_what_is_ai(.en).mp4/.srt — 重出中英成片（各 324 秒），v2 成片移到 final/_v2/；preview(.en).json 已更新
- tools/edu_review.py — 英文计词把带重音字母（résumés）算作一个词
- edu_videos/ai_terms/README.md — 时长规则改为 3–5 分钟（follow-up 012/013），t00 行更新为 v3

验证: edu_video qa 中英全部通过；edu_web check 中英版式自检无问题；edu_review validate 必改 0 条（程序检验通过）；成片抽帧目检；预览 http://127.0.0.1:5174/episode-preview?path=edu_videos/ai_terms/t00_what_is_ai 返回 200。台词审第 3 轮结论为「3 项未过、已到轮数上限，余下问题按清单修改后交程序检验」

No conflicts found in: edu_videos/ai_terms 其他 tNN 未改；edu_review.py 改动只影响英文计词，使含重音字母的词不再被多计

## Follow-up 016 — 2026-11-09 19:38:44
Source: user_input/follow_ups/202611.md - section 016
Summary: 调研 8 门同类课程/词表，出 AI 高频词词表提案 v2：6 季 39 期、播放顺序、前置、快线，待用户定

Auto-updated:
- edu_videos/ai_terms/词表提案_v2.md（新建）

验证: 提案文件已写；调研来源 8 个附链接；未改 README 与已做三期，等用户定
费用: 无收费服务

No conflicts found in: （未单独核查）


## Follow-up 017 — 2026-11-09 19:51:24
Source: user_input/follow_ups/202611.md - section 017
Summary: 词表提案 v2.1：不受已做三期位置限制重排，过拟合移到怎么学之后（1-7），新增模型与参数、损失函数、反向传播，40 期

Auto-updated:
- edu_videos/ai_terms/词表提案_v2.md（改为 v2.1）

验证: 第 1 季重排为 11 期、第 2 季先 LLM 后词元；各期前置与新编号核对过；README 与已做三期未动，等用户定
费用: 无收费服务

No conflicts found in: （未单独核查）


## Follow-up 018 — 2026-11-09 20:12:30
Source: user_input/follow_ups/202611.md - section 018
Summary: ai_terms 课程表.md 定稿（6 季 40 期，损失函数单独一期），README 指向它

Auto-updated:
- edu_videos/ai_terms/课程表.md（新，替代 词表提案_v2.md）；ai_terms/README.md（词表加播放列、指向课程表、t10–t13 立项）；_shared/package.json 片头改「第 N 季 · 第 N 期」；tools/edu_package.py eyebrow 支持 season；ai_terms/_shared/s1_bible.md、s1_data.py（第 1 季前半共用设定与数据）

验证: tools/tests -k edu 6 passed；左侧导航解析课程表 6 季 40 期
费用: 无收费服务

No conflicts found in: （未单独核查）


## Follow-up 019 — 2026-11-09 20:16:39
Source: user_input/follow_ups/202611.md - section 019
Summary: t10 模型与参数、t11 损失函数、t04 梯度下降、t12 神经网络、t13 反向传播 五期并行制作（各一子代理，按 t09 流程与 s1_bible）

Auto-updated:
- edu_videos/ai_terms/t10_model_params、t11_loss_function、t04_gradient_descent、t12_neural_networks、t13_backprop（讲稿、场景、包装、审查单 lines_r1–r3、成片）；ai_terms/README.md 五行状态；tools/edu_video.py（回听：by≈times、钱数念法）；tools/edu_package.py（本期内容卡章节连续编号）

验证: 五期中英成片均在（4:09–4:59.5），preview 中英齐；各期 validate --lang all 必改 0、响度 −15.9 至 −16.1 LUFS；台词审各 3 轮收轮，最终分仍有 1 分的已按裁决定稿改、未复审；tools/tests -k edu 6 passed
费用: Codex 出图：t04 1 张（clay_hiker.png）、t11 1 次请求连接失败未出图，均记各期 request_log.md；无其他收费服务

No conflicts found in: （未单独核查）


## Follow-up 020 — 2026-11-14 10:39:43
Source: user_input/follow_ups/202611.md - section 020
Summary: 新建 edu_videos/redian_xiangying 系列（系列级规则）：采纳定位（热点开场、长期认知为正片）、立场（事实/观点/推测分开、反方最强论证、claims.json 带 as_of）、素材版权分级与 media_ledger.json、研究档案模板；不采纳 Seedance 额外限制、固定片子结构、快慢两条线；平台、语言、主持人声音待定

Auto-updated:
- edu_videos/redian_xiangying/README.md（新建）、edu_videos/redian_xiangying/_shared/dossier_template.md（新建）、edu_videos/README.md（加系列级覆盖说明一行）

验证: workflow_catalog --check 通过；followup check --all

No conflicts found in: 只新增系列级文件，大系列 README 仅加一行指引；未改共用 skill 与仓库级规则


## Follow-up 021 — 2026-11-14 10:42:40
Source: user_input/follow_ups/202611.md - section 021
Summary: 2026-11-14 跨平台热榜检索（抖音/微博/B站/知乎聚合、TikTok 标签、YouTube 全球趋势）：第一 美国 FAA 全国地面停飞（11-13），第二 黄仁勋辞任英伟达 CEO（11-12）；建 t01、t02 期目录并启动研究档案

Auto-updated:
- edu_videos/redian_xiangying/README.md（期目录、搜索配额规则）；t01_faa_ground_stop 与 t02_jensen_huang_resigns 的 research/angles/*.md、research/dossier.md、claims.json（初稿）

验证: 两份 claims.json JSON 校验通过（子代理报告）；独立事实核查未做；followup check --all

No conflicts found in: 只改本系列文件


## Follow-up 022 — 2026-11-14 11:30:19
Source: user_input/follow_ups/202611.md - section 022
Summary: t01 论点定 A；t02 角度改为两党政治斗争与中美竞争背景下的黄仁勋（作为待证假设补充研究，按系列立场规则检验）；本系列素材不再按网站条款分级（用户决定，素材台账只记来源）；中英双语，B站＋YouTube

Auto-updated:
- edu_videos/redian_xiangying/README.md（素材条款规则改为用户决定直接使用、平台语言、期目录状态）；已启动 t01 独立事实核查与 t02 用户角度补充研究

验证: README 已改；核查与补充研究结果待回；followup check --all

No conflicts found in: 只改本系列；paid_services 的 AI 工具条款不受影响


## Follow-up 023 — 2026-11-14 11:48:22
Source: user_input/follow_ups/202611.md - section 023
Summary: t02 主线定为「中美科技战让一个 CEO 的私事变成国家安全问题」，第二层「对华芯片上国会两党都要收紧、只有白宫在放，两党都拿他打自己的仗」（标我们的判断），「牺牲品」作中文舆论说法引用并检验；t01 FAA 公告与声明页用 Chrome 存档到 research/archive/

Auto-updated:
- edu_videos/redian_xiangying/README.md（t01/t02 状态）；t01：research/archive/（ATCSCC Advisory 111 与 FAA 声明当日 Wayback 快照＋README）、claims.json（r1 落实 19 条＋10 条小注、新增 C45–C48、C01/C02/C10/C41 按存档原文更新）、research/dossier.md（论点 A 收窄、论据分类、第 7 节）；t02：已启动独立事实核查

验证: claims.json JSON 校验通过（48 条）；FAA 原文对照存档逐字核对；t02 核查结果待回；followup check --all

No conflicts found in: 只改本系列文件


## Follow-up 024 — 2026-11-14 12:10:26
Source: user_input/follow_ups/202611.md - section 024
Summary: t01 FAA 停飞开写讲稿：按 edu「先说后写」——先写每拍意思与事实（beats），再由中英讲解员各自口述成稿，作者剪短核事实，lint 后进台词审

Auto-updated:
- t01：drafts/v1_brief.md、drafts/v1_zh.md、drafts/v1_en.md、script.md、script.en.md（v1，83 句中英对齐）、claims.json（挂 lines；C42–C44 source=judgment）、package.json、timeline.json / timeline.en.json（估算）；系列 _shared/package.json（通用章节号 c1–c8，英文系列名暂定 Meet the Headlines）；tools/edu_review.py check_claims 允许 source=judgment

验证: edu_review lint 无可疑句；validate 只剩缺配音与时间轴（预期）；估算时长中文 424.8 秒、英文 418.2 秒；台词审需画面截图，待出画面后开

No conflicts found in: edu_review 只放宽 judgment 来源的 quote 要求，其他系列不受影响


## Follow-up 025 — 2026-11-14 12:31:22
Source: user_input/follow_ups/202611.md - section 025
Summary: t02 claims.json 落实核查 r1（改 34 条、新增 C113–C126，共 126 条）；dossier 第二层论点改为「两党都借这件事追问」、新增风险句与截图禁区；coverage.md 隐私说明改正

Auto-updated:
- t02_jensen_huang_resigns/claims.json（126 条，48 条带 fc_r1）、research/dossier.md（§1 定稿块、§6.2 风险句、§7、§8 重写）、research/angles/coverage.md（隐私说明改正）、系列 README t02 状态

验证: claims.json 合法 JSON 编号不重复（编辑报告）；全目录检索未见第二位当事人姓名；followup check --all

No conflicts found in: 只改本系列文件


## Follow-up 027 — 2026-11-14 14:29:09
Source: user_input/follow_ups/202611.md - section 027
Summary: 建 chips 系列、t01 研究档案与故事板

Auto-updated:
- edu_videos/chips/README.md — 新建系列：Vision、人物（阿凯 / 林工）、系列级画面例外（Blender 结构＋Seedance 人物＋网页叠加）、诚实标注、流程、知识点地图 v2（9 期）
- edu_videos/chips/t01_inside_a_chip/research/angles/{scale_structure,seeing_materials,fab_process,benchmark_format}.md — 4 个研究子代理并行（搜索约 64 次）
- edu_videos/chips/t01_inside_a_chip/research/dossier.md、factcheck_r1.md — 综合档案 F01–F18；独立核查 r1：13 属实 5 需改，已落实（手机芯片改「上百亿」等）
- edu_videos/chips/t01_inside_a_chip/beats.md — 9 拍节拍 v1（约 4:30）
- edu_videos/chips/_shared/characters/{lin_sheet_v1,kai_sheet_v2}.png、_shared/style_options/{A_clay,B_cinematic,C_stylized}.png — Codex 出图；kai v1 因写「十七岁」被审核拦截，改成年人重出
- edu_videos/chips/t01_inside_a_chip/storyboard/ — panels.json、P01–P14.png（Codex，人物设定图＋S3 画风做参考；P01/P02/P04/P05/P14 自查后重出，旧图在 rejected/）、review.json、gen_panels.py、build_review.py
- .audit/adhoc_agents/2026-11-14/chips-t01-research/README.md — 研究与核查子代理记录

验证: 逐张看图自查（芯片封装针脚、剖面层次、天空误导已修）；事实独立核查 r1；/api/media 与 review.json 经 5174 端口可读；故事板待用户 review；台词为草稿未过台词审
费用: Codex 内置出图 25 次（订阅额度，费用未知，日志在 edu_videos/chips/_shared 与 t01 的 request_log.md）

No conflicts found in: （未单独核查）


## Follow-up 028 — 2026-11-14 15:07:35
Source: user_input/follow_ups/202611.md - section 028
Summary: chips 系列画风定 S2 电影写实、人物改真人，重做设定图与故事板

Auto-updated:
- edu_videos/chips/README.md — 新增「画风：电影写实」节；人物改写实真人（虚构、不像任何真实个人）
- edu_videos/chips/_shared/characters/{lin_real_v1,kai_real_v1}.png — Codex 出真人设定图（三视图）
- edu_videos/chips/t01_inside_a_chip/storyboard/ — panels.json v2（真人参考＋S2 画风参考）、gen_panels.py 改写实提示、P01–P14.png v2；P03 自查重出两次（外壳开窗、背景铜导线），废图在 rejected/；v1 卡通版移到 v1_stylized/；review.json 重建

验证: 逐张看图：人物与设定图一致，P03 两处误导已修；/api/media 读图 200；故事板待用户 review
费用: Codex 内置出图 18 次（设定图 2、故事板 14、P03 重出 2；订阅额度，费用未知）

No conflicts found in: （未单独核查）


## Follow-up 029 — 2026-11-14 15:47:40
Source: user_input/follow_ups/202611.md - section 029
Summary: 探索系列：主角跨主题复用；选角方案待用户选

Auto-updated:
- （未改文件）— 只登记意图；选角方案已向用户给出建议（一套画面＋华人向导＋混血新手、中英配音），等用户选定后再改 README、目录与人物资产

验证: 无产物改动

No conflicts found in: （未单独核查）


## Follow-up 030 — 2026-11-14 15:54:32
Source: user_input/follow_ups/202611.md - section 030
Summary: 探索系列选角 v1：向导与新手各几组候选（四视图＋表情）

Auto-updated:
- edu_videos/chips → edu_videos/tansuo（目录改名；storyboard 的 panels.json、gen_panels.py、build_review.py、review.json 路径同步；.audit 研究记录路径同步）
- edu_videos/tansuo/README.md — 改为探索系列：一套画面中英配音、主角跨主题复用、选角方向（华人向导＋中欧混血新手）；edu_videos/README.md 系列表加探索
- edu_videos/tansuo/_shared/cast/casting_v1/ — candidates.json（G1–G3 向导、K1–K4 新手）、gen_casting.py、build_review.py、review.json、14 张图（每人四视图＋六格表情）

验证: 逐张看图：每位候选四视图与表情为同一人；K1–K3 混血感偏弱已在审阅页注明；/api/media 200；待用户选角
费用: Codex 内置出图 14 次（订阅额度，费用未知；日志 edu_videos/tansuo/_shared/request_log.md）

No conflicts found in: （未单独核查）


## Follow-up 031 — 2026-11-14 16:08:41
Source: user_input/follow_ups/202611.md - section 031
Summary: 主角定 G1（林）与 K1（凯），重出 t01 故事板 v3

Auto-updated:
- edu_videos/tansuo/_shared/cast/{lin,kai}/ — 正式参考：turnaround.png、expressions.png（取自选角 G1/K1）、portrait.png（Codex 新出 9:16 立绘）、turntable.txt（Seedance 建立视频 prompt，15 秒中英各一句＋转身）；cast/turntable.py（提交/轮询/下载，经 RequestLog，账本防重提）；cast/review.json
- edu_videos/tansuo/README.md — 主角已选定节

验证: 立绘逐张看图与选角一致；turntable.py --dry-run 通过；建立视频未提交（收费，待用户点）
费用: Codex 内置出图 2 次（立绘；订阅额度，费用未知）

No conflicts found in: （未单独核查）


## Follow-up 032 — 2026-11-14 16:09:59
Source: user_input/follow_ups/202611.md - section 032
Summary: 探索系列加想象力特效（服务内容、标示意），重设计 t01 故事板 v3 的特效

Auto-updated:
- edu_videos/tansuo/README.md — 新增「特效」节（华丽但画真实现象、标示意，结构不改，标志特效琥珀刻度涟漪，固定配色）；诚实标注段同步
- edu_videos/tansuo/t01_inside_a_chip/storyboard/ — panels.json v3（定角林/凯＋每格特效设计 vfx 字段）、gen_panels.py 特效提示、apply_vfx_v3.py、build_review.py 显示特效；P01–P14 v3；P13 改掉玻尔轨道原子、P04 改不透明硅与干净背景（第二次超时确认未出图后重提），废图在 rejected/；v2 在 v2_cinematic/

验证: 逐张看图：人物与定角一致；玻尔模型、透明硅、背景导线三处误导已修；/api 200；待用户 review
费用: Codex 内置出图 17 次（v3 14 张＋P13 1＋P04 2，其中 1 次超时未出图；订阅额度，费用未知）

No conflicts found in: （未单独核查）


## Follow-up 033 — 2026-11-14 16:42:00
Source: user_input/follow_ups/202611.md - section 033
Summary: 提交林、凯建立视频

Auto-updated:
- edu_videos/tansuo/_shared/cast/lin/turntable.mp4（submit 170d1079，15.07s，8634 KB）、kai/turntable.mp4（submit f80e6a95）；cast/review.json 加视频

验证: 抽帧看图：全身、正侧背转到位、服装一致、无字幕；平均响度 −23.3 / −22.8 dB；faster-whisper 转写：两人中英台词逐句吻合
费用: Seedance 2.5 两条 × 15 秒（priority 7 排第 0；工具记 80 分/条，实扣以账户为准，日志 edu_videos/tansuo/_shared/request_log.md）

No conflicts found in: （未单独核查）


## Follow-up 034 — 2026-11-14 16:50:17
Source: user_input/follow_ups/202611.md - section 034
Summary: 向导重新选角：casting_v2 五组知性美候选

Auto-updated:
- edu_videos/tansuo/_shared/cast/casting_v2/ — candidates.json（G4–G8 知性美＋G1 对照）、gen_casting.py、build_review.py、review.json、10 张新图

验证: 逐张看图：每位四视图与表情为同一人；G5/G8 偏像已告知用户；待用户选
费用: Codex 内置出图 10 次（订阅额度，费用未知）

No conflicts found in: （未单独核查）


## Follow-up 035 — 2026-11-14 17:00:41
Source: user_input/follow_ups/202611.md - section 035
Summary: 向导选角 v3：基于 G5/G6 更漂亮的五组

Auto-updated:
- edu_videos/tansuo/_shared/cast/casting_v3/ — candidates.json（G9–G13，以 G5/G6 四视图为参考、更漂亮；G5/G6 对照）、gen_casting.py、build_review.py、review.json、10 张新图

验证: 逐张看图：每位四视图与表情为同一人；G9/G10 与 G5、G11 与 G6 相似度高、变漂亮幅度有限，已告知用户
费用: Codex 内置出图 10 次（订阅额度，费用未知）

No conflicts found in: （未单独核查）


## Follow-up 036 — 2026-11-14 17:10:47
Source: user_input/follow_ups/202611.md - section 036
Summary: 林改定 G9，出立绘与建立视频

Auto-updated:
- edu_videos/tansuo/_shared/cast/lin/ — turnaround/expressions 换成 casting_v3 G9；portrait.png（Codex 新出）；turntable.txt 改无眼镜、低发髻；turntable.mp4（submit 6c62a444，15s，12475 KB）；G1 旧资产与旧建立视频（submit 170d1079）归档 lin/_old_G1/
- edu_videos/tansuo/README.md — 林改为 G9、身份标记去掉眼镜；t01 storyboard/gen_panels.py 林的描述改为 G9；cast/review.json 更新

验证: 立绘看图与 G9 一致；视频抽帧：同一张脸、转到背面低发髻正确、无字幕；平均响度 −24.4 dB；faster-whisper 分语言转写台词逐句吻合；偏差：取景只到大腿、非全身，已报用户待定
费用: Codex 内置出图 1 次（订阅额度）；Seedance 2.5 一条 15 秒（priority 7；工具记 80 分/条，实扣以账户为准）

No conflicts found in: （未单独核查）


## Follow-up 037 — 2026-11-14 17:19:47
Source: user_input/follow_ups/202611.md - section 037
Summary: 林建立视频重出（全身）；建立视频验收加全身一条

Auto-updated:
- edu_videos/tansuo/_shared/cast/lin/turntable.txt — 取景要求提到最前（远景、人物占画面高六成半、脚下留地面），负面词加半身/七分身；turntable.mp4 重出（submit aa4f185d，15s，10270 KB）；半身旧片 6c62a444 与其 prompt、账本移到 lin/_rejected/
- edu_videos/tansuo/README.md — 建立视频验收：必须全身，否则重出；cast/review.json 更新

验证: 抽帧：头顶到鞋底全身、脚下有地面、正侧背转到位、低发髻、无字幕；面部截图为 G9；平均响度 −25.1 dB；faster-whisper 分语言转写中英台词逐句吻合
费用: Seedance 2.5 一条 15 秒（priority 7；工具记 80 分/条，实扣以账户为准）；半身那条已扣费作废

No conflicts found in: （未单独核查）


## Follow-up 026 — 2026-11-14 12:44:32
Source: user_input/follow_ups/202611.md - section 026
Summary: t01 做到成片再给 /episode-preview 链接：网页场景、下载 Commons 公共领域图片与白宫记者会视频（登记 media_ledger）、Seedance 镜头 prompt 交用户点生成、配音、Suno 配乐、合成

Auto-updated:
- t01：scenes/web s0–s6、_lib.js、data.py；script v1.3（zh/en）；claims.json（C49）；media_ledger.json；seedance/ 5 镜（600 积分）及 review.md；assets/music（Suno 2 首＋bgm_t01）；reviews/lines_r1–r3；final/*.mp4、preview*.json；tools/edu_web.py（视频片段按句时间占位 {{t:}}/{{d:}}）；tools/edu_review.py（judgment 来源）；系列 README 期目录

验证: edu_review validate：必改仅剩 EN l01/l07 两条，均为识别把数字写成阿拉伯数字（3.54、9-11）的格式差异，人工判定非念错；响度 -16.0/-15.9 LUFS；edu_web check 中英无问题；预览页 200

No conflicts found in: 台词审 3 轮到上限，第 3 轮改动未再复核；白宫记者会视频因 YouTube 反机器人拦截未下载


## Follow-up 038 — 2026-11-14 17:37:43
Source: user_input/follow_ups/202611.md - section 038
Summary: t01 故事板 v4（G9）整集重出＋自检迭代，出片前用户预览

Auto-updated:
- edu_videos/tansuo/t01_inside_a_chip/storyboard/：P01–P14 v4（G9）整集重出；按审稿 r1 改 P03–P12，r2 后再改 P08、P10–P12（gen_panels.py 对 P11/P12 不再拼铜导线材质段）；淘汰图在 rejected/；panels.json P12 台词加倍数备注；build_review.py/review.json 改为 v4 并列待定事项；reviews/self_r1.md、r1.md、r2.md、r3.md；tansuo/README.md 与 edu_videos/README.md 状态

验证: 作者逐格看图自检；独立上下文审稿 r1（14 格）、r2（P03–P13）、r3（P10–P12）。r3 仍有 1 条必改：P11 林的表在右腕，两次重出已用完，按约定交用户；P12 叠层约人高六成，倍数讲稿时重算。P10–P12 首次重出遇 Codex 网络错误（workspace routing discovery failed），查 generated_images 确认未出图后重提。预览页 /character-review 返回 200。未生成任何视频。

No conflicts found in: edu_videos/README.md 大系列约定、tansuo/README.md 画风与特效节、人物参考 _shared/cast/


## Follow-up 040 — 2026-11-14 20:35:09
Source: user_input/follow_ups/202611.md - section 040
Summary: t01 故事板预览改为短剧拍摄页样式；新增整集音频预览（本地 TTS、scene/shot 进度条、时间对齐成片），今后出视频前必给

Auto-updated:
- edu_videos/tansuo/t01_inside_a_chip/storyboard/build_preview.py（新：panels.json＋beats.md → storyboard/storyboard.json 与 audio/preview_manifest.json；转场镜头起收时长；say 读音替换 栅极→珊极）；storyboard.json；audio/preview_manifest.json；audio/preview/（逐句配音、takes.json、timeline.json、preview.m4a，媒体不进 git）；audio_preview.json；_shared/cast/lin|kai/voice_zh.wav、voice_en.wav、voice.json（从建立视频按 whisper 逐字时间切出的声样）；tansuo/README.md、edu_videos/README.md 流程与状态

验证: 音频预览 1:56、14 镜、23 句，回听全部错率 ≤15%（栅极误读 zhà 由 say 修正，P13 欢呼改「哇哦」后通过）；每镜 5–13 秒，无超 15 秒；浏览器实测 /episode-preview?…&audio=1 大图随镜切换、叠台词、场/镜进度条，/storyboard-preview 与拍摄页同样式；首次整集约 16 分钟，增量改两句 99 秒。英文版未做。

No conflicts found in: tansuo README 画风/特效/诚实标注节；edu 大系列三层审查


## Follow-up 043 — 2026-11-14 21:31:41
Source: user_input/follow_ups/202611.md - section 043
Summary: edu 审查改为 Claude 单审

Auto-updated:
- edu_videos/_shared/review/roles.json（事实核查、中英母语听感 runner codex→claude，note 记录）；tools/edu_review.py 说明改为单审；edu_videos/README.md 专家审稿一段

验证: roles.json 解析通过，8 个角色 runner 全为 claude；line_review.json 已是单审（models 只有 a）；edu_review.py py_compile 与 --help 正常；edu_review 无自动测试，未实跑 brief。

No conflicts found in: 台词审 v2/v3 维度与硬上限不变


## Follow-up 045 — 2026-11-14 22:24:38
Source: user_input/follow_ups/202611.md - section 045
Summary: 探索第二季「血脂」：医学研究档案 → 季地图 → 试点期故事

Auto-updated:
- edu_videos/tansuo/t11_inside_an_artery/research/angles/*.md — 7 个研究角度（生物学与尺度、因果与好坏、他汀与其他药、生活方式、指南与情景、对标与谣言、根因）
- edu_videos/tansuo/t11_inside_an_artery/research/dossier.md — 季研究档案 F01–F58，按核查 r1 修订（§8）
- edu_videos/tansuo/t11_inside_an_artery/research/factcheck_r1.md — 独立事实核查 r1
- edu_videos/tansuo/t11_inside_an_artery/beats.md — 试点期 13 拍节拍 v1.1（凯与父亲的处境线）
- edu_videos/tansuo/README.md — 第二季血脂 Vision、凯的一家主线、合规、编码色、t11–t20 知识点地图、期目录
- edu_videos/README.md — 系列表探索行加第二季
- .audit/adhoc_agents/2026-11-14/tansuo-s2-lipids-research/ — 子代理任务说明、产物要点与 403 中断记录

验证: 独立上下文事实核查 r1（35 属实 / 10 需改 / 0 不实 / 13 未能核），需改项已落实；节拍未经观众或台词审（尚未进讲稿）；workflow_catalog.py --check 通过

No conflicts found in: （未单独核查）


## Follow-up 046 — 2026-11-14 23:00:48
Source: user_input/follow_ups/202611.md - section 046
Summary: 血脂季研究加角度：LDL 升高的根因、他汀治本还是治标

Auto-updated:
- edu_videos/tansuo/t11_inside_an_artery/research/angles/root_cause.md — LDL 升高根因与他汀治本还是治标
- edu_videos/tansuo/t11_inside_an_artery/research/angles/statins_drugs.md — §8 他汀治本还是治标
- edu_videos/tansuo/t11_inside_an_artery/research/dossier.md — F19–F24、F33、F36–F38；§4 问题 ⑩
- edu_videos/tansuo/README.md — 季地图 t15 以此为核心问题

验证: 事实核查 r1 覆盖相关条目；核查意见：基因编辑也只作用于降 LDL 一环，不能称治本，已写入档案

No conflicts found in: （未单独核查）


## Follow-up 039 — 2026-11-14 20:31:55
Source: user_input/follow_ups/202611.md - section 039
Summary: t01 已成片待审；t02 从讲稿做到成片：讲稿要点→中英讲解员口述→台词审→配音→网页场景＋Seedance 4 镜（用户已同意，约 480 积分）＋公开图片→Suno 配乐→合成→/episode-preview 链接

Auto-updated:
- edu_videos/redian_xiangying/t02_jensen_huang_resigns/（script.md/script.en.md v1.4、claims.json C127–C134、scenes/web s0–s6、seedance 4 镜、media_ledger、final/、preview*.json）；redian_xiangying/README.md 期目录

验证: 台词审 lines_r1–r3（Claude 单审）；edu_web check 中英无问题；配音 qa 全部通过；edu_review validate 必改 0；预览页 HTTP 200
费用: Seedance 480 积分（4×120）；Codex 出图 5 张（订阅额度）

No conflicts found in: （未单独核查）


## Follow-up 041 — 2026-11-14 20:47:54
Source: user_input/follow_ups/202611.md - section 041
Summary: t02：补公开图片（国会议员官方照、总部、港口等）＋Codex 生成示意图（不出真人、标 AI 生成）；讲稿中英按通顺流畅重写一轮再进台词审；ElevenLabs 中文母语音色 5 句样音给用户盲听，定了再决定 t01/t02 是否换配音引擎

Auto-updated:
- media_ledger.json M08–M22（Commons 10 张、Codex 5 张）；script.md/script.en.md 通顺重写 v1.1–v1.4；_shared/voice_lab_eleven/（ElevenLabs 查询记录）

验证: Codex 图逐张看过；ElevenLabs 样音未出：账户额度 600,358 已用尽，2026-11-17 15:01 重置（请求均已记日志，被拒不扣费）；用户选先用本地配音出 preview
费用: ElevenLabs 0（被拒）

No conflicts found in: （未单独核查）


## Follow-up 042 — 2026-11-14 21:21:17
Source: user_input/follow_ups/202611.md - section 042
Summary: 教学视频台词审（tools/edu_review.py）改 Claude 单审：line_review.json models 去掉 b 位，slots_of() 按 models 定审稿位，单审时 a 位评分即最终分、不对比不裁决；checklist/issues 兼容单审；edu README 同步；t02 lines_r1 进行中的审查单转单审（停掉 4 个 Codex 位）。上次（chuanyue_yiri 065）只改了短剧 review_run.py，没覆盖 edu_review.py

Auto-updated:
- tools/edu_review.py（slots_of 单审、TABLE_ROW 级别列允许注释）；edu_videos/_shared/review/line_review.json（models 去 b）；edu_videos/README.md 台词审说明

验证: t02 lines_r1 就地转单审后 check/issues 通过；lines_r2、r3 用 new 开单审审查单（只生成 a 位）跑通 check/issues/fix/conclude；lines_r1 重跑 issues 条数不变（110）

No conflicts found in: （未单独核查）


## Follow-up 047 — 2026-11-15 00:26:55
Source: user_input/follow_ups/202611.md - section 047
Summary: t01 不限时长、质量优先；开关原理本期讲透（t02 选题顺延）

Auto-updated:
- t01 按质量优先不限时长，开关原理并入本期；t02 改为开关怎么学会算数，中英 23 场 87 句及系列 README 已同步。

验证: 三轮讲稿审查与六类定点终审均 0 必改；edu_review lint 中英通过；36 个相关测试通过。

No conflicts found in: （未单独核查）

## Follow-up 048 — 2026-11-15 00:31:57
Source: user_input/follow_ups/202611.md - section 048
Summary: 血脂季家人不露面，纯两人讲解

Auto-updated:
- edu_videos/tansuo/README.md — 第二季主线：家人不露面、不新增选角
- edu_videos/tansuo/t11_inside_an_artery/beats.md — 父亲只以台词与出院单道具出现；同处把 047 写成了 048

验证: 文本改动，两处替换已核对；无媒体产物受影响。注：本会话误对另一会话的 047 执行了 done，已把 047 的 changelog 恢复为待补骨架

No conflicts found in: （未单独核查）


## Follow-up 049 — 2026-11-15 10:38:14
Source: user_input/follow_ups/202611.md - section 049
Summary: 血脂季不请医生署名，不做药物推荐

Auto-updated:
- edu_videos/tansuo/README.md — 不安排医生审稿署名、不做药物推荐；同步季地图与 t11 故事板状态
- edu_videos/README.md — 更新探索系列 t11 状态
- edu_videos/tansuo/t11_inside_an_artery/beats.md — 医疗边界、LDL 受体内吞与斑块破裂限定
- edu_videos/tansuo/t11_inside_an_artery/research/dossier.md — 记录用户对核查员资质建议的决定与全季推荐边界
- edu_videos/tansuo/t11_inside_an_artery/storyboard/ — v1 共 13 张 1672×941 PNG、panels/storyboard/review JSON、生成与预览脚本；图片 SHA256 与 thread_id 见 request_log.md
- edu_videos/tansuo/t11_inside_an_artery/storyboard/reviews/self_r1.md — 13 格逐图自检；P06 出片前必改
- edu_videos/tansuo/t11_inside_an_artery/audio/preview_manifest.json — 仅生成后续音频预览清单，未生成音频

验证: 未做独立故事板审稿，待用户预览；未生成收费视频

No conflicts found in: （未单独核查）


## Follow-up 050 — 2026-11-15 16:23:23
Source: user_input/follow_ups/202611.md - section 050
Summary: t11 增加他汀机制与治本治标解释

Auto-updated:
- edu_videos/tansuo/t11_inside_an_artery/beats.md — v1.2 新增他汀机制与治本/治标
- edu_videos/tansuo/t11_inside_an_artery/storyboard/panels.json — v2 新增 P12A
- edu_videos/tansuo/t11_inside_an_artery/storyboard/P12A.png — 1672×941；SHA 与生成记录见 request_log.md
- edu_videos/tansuo/t11_inside_an_artery/storyboard/reviews/self_r2.md — 新增格自检与正式模型修正边界

验证: P12A 首次网络失败无图，第二次成功并逐图验收；不作药物推荐；未生成音频或视频

No conflicts found in: （未单独核查）


## Follow-up 051 — 2026-11-15 16:28:31
Source: user_input/follow_ups/202611.md - section 051
Summary: t11 补充他汀与血脂关系及降 LDL 是否解决问题

Auto-updated:
- edu_videos/tansuo/t11_inside_an_artery/beats.md — 新增他汀与血脂关系、降 LDL 结局证据、绝对获益和残余风险
- edu_videos/tansuo/t11_inside_an_artery/storyboard/panels.json — 新增 P12B，共 15 格
- edu_videos/tansuo/t11_inside_an_artery/storyboard/P12B.png — 1672×941；SHA 与生成记录见 request_log.md
- edu_videos/tansuo/README.md 与 edu_videos/README.md — 同步 t11 v2 状态

验证: P12B 首次成功并逐图验收；15 panels/scenes/review items、全部图片与链接校验通过；未生成音频或视频

No conflicts found in: （未单独核查）


## Follow-up 052 — 2026-11-15 17:03:12
Source: user_input/follow_ups/202611.md - section 052
Summary: 芯片与血脂故事板统一入口并写入系列流程

Auto-updated:
- edu_videos/tansuo/README.md — 一期流程的故事板步骤明确每期 storyboard.json、统一 ShotCard、左导航入口与用户审顺序，适用于芯片和血脂

验证: Chrome/Playwright 实开 t01 v5-script 23 镜与 t11 v2 15 镜，左导航故事板均展开并高亮；截图 .audit/adhoc_agents/2026-11-15/storyboard-nav/t01.png 已看图

No conflicts found in: （未单独核查）


## Follow-up 044 — 2026-11-14 22:20:09
Source: user_input/follow_ups/202611.md - section 044
Summary: t01 重写：调研同类讲解 → 有铺垫的故事、观众关心的问题、详细解释、情景与特效

Auto-updated:
- t01 完成中英文叙事调研、23 场 87 句讲稿与三轮审查；V5 故事板工作稿使用已过审 V18C，其余保留临时图说明；中文音频 9:54/53 镜、英文 10:27/58 镜已生成。

验证: 六类定点终审均 0 必改；中英时间轴无超 15 秒镜头、无回听超标且句数齐全；Chrome 实际打开故事板并播放两版音频通过；36 个相关测试、lint、py_compile、workflow_catalog 与 skills 检查通过。

No conflicts found in: （未单独核查）


## Follow-up 053 — 2026-11-15 17:29:56
Source: user_input/follow_ups/202611.md - section 053
Summary: 核查 t11 v2 概念板、场镜映射与独立审稿状态

Auto-updated:
- edu_videos/tansuo/t11_inside_an_artery/storyboard/reviews/structure_r1.json — 记录场镜映射原因、独立Kimi图审、六项意见及分阶段结论
- .audit/adhoc_agents/2026-11-15/t11-v2-review/ — 输入指纹、15格拼图、真实审稿任务与原始输出、定向原文核查
- .audit/adhoc_agents/2026-11-15/t11-v2-review/corrected/ — 编码修复后的有效独立Kimi复审；首轮保留并明确作废
- edu_videos/tansuo/t11_inside_an_artery/storyboard/reviews/structure_r1.json — 补入有效独立审稿完整意见，并读回校验中文

验证: 有效Kimi独立复审结论：concept=pass、production=fail。全部15格图片已看；15场15镜映射、15镜0时长与占位字段已核，输入SHA256未变。P11定向核对原论文摘要。首次任务说明编码损坏，首轮结论作废，已改用英文完整说明重跑；中文报告读回正确。缺讲稿、claims与音频轴，成片和全量医学未审；未改创作内容或生成媒体。

No conflicts found in: （未单独核查）


## Follow-up 054 — 2026-11-15 17:34:23
Source: user_input/follow_ups/202611.md - section 054
Summary: t01 按实际场景重组并拆分视觉镜头

Auto-updated:
- storyboard/build_preview.py — 按9个实际场景登记中文53镜、英文58镜及独立视觉键；storyboard.json、audio/preview_manifest*.json、audio/preview*/timeline.json、audio_preview*.json — 同步多镜结构且保持87句与594/627秒；storyboard/reviews/v5_visual_structure*.md — 首轮6项必改与R2清零；edu_videos/README.md、tansuo/README.md — 更新期状态。

验证: 独立R2复审0必改；同语言视觉键与图片路径均不重复；两版无超15秒镜头、无回听超标；Chrome展开全部9场并加载V18C、播放双语音频通过；36个测试、py_compile、sync_agent_config、skills、workflow检查通过。shot_pack check因edu目录无prompts.json而不适用，未生成或核验短剧资料包。

No conflicts found in: （未单独核查）


## Follow-up 056 — 2026-11-15 18:01:32
Source: user_input/follow_ups/202611.md - section 056
Summary: 复查并修补芯片 t01 故事板

Auto-updated:
- edu_videos/tansuo/t01_inside_a_chip/script.md、script.en.md、beats.md、claims.json — 修正l34绝缘与换向因果，中英v2.5，记录当前版未独立复审；Intel官方PDF核对
- edu_videos/tansuo/t01_inside_a_chip/storyboard/build_preview.py、storyboard.json、storyboard/prompts/current/ — V5.1修补英文通断时序、局部放大与人体尺度、工艺拼用和电路约束；当前逐镜提示替代旧提示入口；错腕P11退出当前首帧
- edu_videos/tansuo/t01_inside_a_chip/audio/preview_manifest*.json、audio/preview/、audio_preview*.json — 本地重出中英l34并重建预览，中文592秒53镜／英文629秒58镜
- edu_videos/tansuo/t01_inside_a_chip/reviews/storyboard_v51_review.json、edu_videos/tansuo/README.md、edu_videos/README.md — 10项发现、修补与未结项及当前状态
- .audit/adhoc_agents/2026-11-15/chip-review-056/ — 原始审查输入指纹、15图联系表、Kimi额度拒绝记录、官方PDF、机检与当前产物SHA

验证: 本地作者核对15张图；分镜与预览句序、每语87句、53/58镜、无超15秒、无超标回听、14张参考图路径唯一、首帧提示存在、HTTP文件API内容一致；lint与git diff --check通过。sync_agent_config/check_agent_skills/workflow_catalog通过。shot_pack sync失败：教学目录无短剧prompts.json，不适用，替以本期检查。Kimi独立审稿因5小时额度耗尽未审；本轮UI截图未验。中文39／英文44首帧仍待制作；P11历史两次重出已用完，撤图不是已修图。

No conflicts found in: （未单独核查）


## Follow-up 055 — 2026-11-15 18:00:37
Source: user_input/follow_ups/202611.md - section 055
Summary: t11 v3分镜修订及复审

Auto-updated:
- t11已知审查项修为v3，9场38镜估算301秒；逐镜摄影调度分拍、P02健康模型、机制图、四组假设比较、限定证据与claims、节拍和预览清单同步。

验证: 结构及链路检查通过；本机API返回v3且源hash一致，新图HTTP200。独立Kimi调用因5小时用量上限失败，未审，审稿仍未闭环；shot_pack sync因教学视频暂无prompts.json失败，未生成制作包，38份分镜说明单独验证。详见storyboard/reviews/v3_resolution.json及.audit/adhoc_agents/2026-11-15/t11-v3-fix/verification.json。
费用: Codex图像1次，费用未知；request_log已记。独立Kimi因配额未运行成功。

No conflicts found in: 仅t11与系列README的t11状态行；保留t01及其他会话改动。

