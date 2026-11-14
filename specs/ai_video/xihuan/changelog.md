
## Follow-up 001 — 2026-11-08 19:51:20
Source: user_input/follow_ups/202611.md - section 001
Summary: 西幻系列新剧开发框架：七页逐步放大 + 检查工具 + 两部作品试套。

Auto-updated:
- ai_videos/xihuan/framework/ — README（v0.2.1）、templates/ 八页模板、check.py（形式与跨页结构检查，--json 写 _check.json）、test_check.py（11 项回归）
- ai_videos/xihuan/framework/examples/ — 指环王电影三部曲、权力的游戏 HBO 两份试套（v0.2.1 通过）、各自 _反馈.md（两轮）与 _评估.md、总评估 _评估.md
- ai_videos/xihuan/README.md 开新剧入口；workflow_catalog.json 登记框架说明与检查工具

验证: 两轮独立试套：v0.1 反馈 26 条建议合并为 v0.2；v0.2 复测两部各 13 条，8 已解决，其余部分解决，无未解决；v0.2.1 补结构检查后两份示例无错误无提示；test_check.py 11 项通过
费用: 无收费调用

No conflicts found in: 系列级试点，未改共用指南；与 story-characters「类别不中途更换」的出入已在框架 README 注明


## Follow-up 002 — 2026-11-08 20:50:04
Source: user_input/follow_ups/202611.md - section 002
Summary: 框架 v0.3：删季结构与分集附录；时间一律用故事阶段（开端、大转折一、中点、大转折二、高潮、结局）；检查工具禁止季集记法；示例与 UI 同步。

Auto-updated:
- ai_videos/xihuan/framework/{README.md,templates/,check.py,test_check.py,examples/}

验证: check.py 拦季/集用语（test_season_and_episode_concepts_are_rejected）；两部试套 v0.4 重填后 check 通过、无季集

No conflicts found in: （未单独核查）


## Follow-up 003 — 2026-11-08 20:53:36
Source: user_input/follow_ups/202611.md - section 003
Summary: 框架 v0.4：五页核心 + 其他；每页以一张图为核心（Mermaid 关系图、阶梯与克制图），UI 渲染图并自动配资料库概念图；精简字段与检查。

Auto-updated:
- ai_videos/xihuan/framework/ 五页核心+其他、表格就是图；projects/ai_video_management/apps/ui: devDiagrams.ts、DevDiagrams.tsx、DevPreviewPage 全景/逐页图、mermaid 11.4.1；examples/_评估.md 与两部 _反馈.md v0.4 复测

验证: pytest test_check.py 12 passed；vitest 227 passed；tsc、npm run build 通过；浏览器 5174 看过框架流程图、指环王全景/力量卡、权游矛盾图

No conflicts found in: （未单独核查）


## Follow-up 004 — 2026-11-08 21:32:46
Source: user_input/follow_ups/202611.md - section 004
Summary: 人物页加必填「能力」表：外在（身体、武艺、法术、技能）与内在（智慧、心志）各一句并各打 1–5 分；check.py 校验编号与分数、每个人物都要有能力行；UI 人物卡显示内外能力，并画内外能力象限图；两部试套补能力表。

Auto-updated:
- ai_videos/xihuan/framework/templates/04_人物.md（必填「能力」表）、check.py、test_check.py、examples/{lotr,got}/04_人物.md；projects/ai_video_management/apps/ui: devDiagrams.ts（abilityChart 象限图）、DevDiagrams.tsx（人物卡内外能力与分数点）、DevPreviewPage.css、test/dev-preview.test.tsx

验证: pytest test_check.py 13 passed；vitest 226/227（map-regions 并发下超时，单独跑 17/17 通过，与本改动无关）；tsc 与 npm run build 通过；两部试套 check 通过；浏览器 DOM 核对象限图 8 点位置、四象限配色与主角高亮（该窗口截图超时，未目视）

No conflicts found in: （未单独核查）


## Follow-up 005 — 2026-11-08 22:33:32
Source: user_input/follow_ups/202611.md - section 005
Summary: 用框架 v0.4 开第一部西幻新剧：先做市场与 IP research（0_research），再写 0_开发 七页（五页核心 + 秘密与伏笔 + 观众与爽点），剧 README 的 Vision 为草稿待用户定；check.py 通过；另起独立审稿评估框架与剧本雏形，结果写进 _评估.md / _反馈.md 供用户在 UI 里看。

Auto-updated:
- ai_videos/xihuan/jian_jinshu/（README、0_research/research.md、0_开发 七页 + _check.json/_反馈.md/_评估.md）；ai_videos/xihuan/README.md；framework README（页序≠创作顺序）与模板检查项（人物去处、天降检查、爽点对应场面、IP 核对）

验证: check.py 通过（三份稿）；test_check 13 passed；独立审稿（sonnet）三轮：初审 5 条必须改 → 二次复审清零，结论可交故事创作，余罗文弧线留给故事创作；后端树已列出「开发稿 · 贱金属」

No conflicts found in: （未单独核查）


## Follow-up 006 — 2026-11-08 22:42:37
Source: user_input/follow_ups/202611.md - section 006
Summary: 《贱金属》依赖金属成色，整剧移入 ai_videos/_deleted；按用户选的「被逐的圣骑士」（女圣骑士被诬陷当众失恩，与恶魔亲王立约复仇，真相是大主教偷走了她的圣光）重新用框架 v0.4 开发，只用主流元素（圣光、深渊契约、圣骑士、教会），参考魔兽世界、指环王、浮士德等；独立审稿至必须改清零。

Auto-updated:
- ai_videos/xihuan/shiguangzhe/（README、0_research、0_开发 七页 + _check/_反馈/_评估）；《贱金属》移入 ai_videos/_deleted/jian_jinshu/；ai_videos/xihuan/README.md

验证: check.py 通过；独立审稿（sonnet，新代理）初审 4 条必须改 → 复审清零、可交故事创作；复审后小修恋爱铺垫（未再审，已在 _反馈 注明）

No conflicts found in: （未单独核查）

