# 变更

## Follow-up 011 — 2026-10-05 10:53:08

Source: user_input/follow_ups/202610.md - section 011
Summary: 新流程明确Seedance视频保留本镜指定对白、自然环境声、动作声，禁止背景音乐/配乐，无对白镜明确没有人说话。compiler v3固定加入，配乐后期独立设计，出片试听。

现有EP1仍为未确定故事与空分镜，当前EP文件和历史run不变；未生成视频。共用流程与编译/字幕91项回归、canon/入口检查通过，证据见 `.audit/adhoc_agents/2026-10-05/seedance-no-background-music/`。

## Follow-up 010 — 2026-10-05 09:17:23

资产 scenes 改名 background，索引改为 background_index.md，更新当前资产/研究引用。集→场→镜头由 content.scenes[].shots[] 组织；完整镜头 key 为 ep1_s1_st1，编译首行与下载导入一致。bg编号（含bg2-2视角）保持原样。EP1未确定故事、空分镜和历史run保留。

9,784个资产逐件校验：1,910个媒体/二进制文件内容相同，886个资产文本仅更新路径，72份故事/历史/共享输入文件原样保留。现有R2索引没有本剧条目，本次没有上传或修改远端对象。历史请求日志及生成回执保留原路径记录，迁移映射为 2_世界观人设/scenes → 2_世界观人设/background。核验与浏览器证据保存在 `.audit/adhoc_agents/2026-10-05/scene-background-migration-20261005-091723/`。

## 2026-10-03 · 三模块重新开始

用户要求清理旧剧情与流程，随后明确保留Research及资产。新增最小三模块数据与UI；EP1保持空白起点，等待故事方向。
删除范围及服务日志保全记录在 .audit/adhoc_agents/2026-10-03/three-module-poc/。

左侧已按用户最终裁定固定五项导航，EP1位于主工作区，不单设入口。

用户进一步明确2/3/4为可展开stage目录；POC暂按stage→EP1显示，右侧只显示选中内容。

## Follow-up 001 — 2026-10-03 21:27:59
Source: user_input/follow_ups/202610.md - section 001
Summary: 新增最小世界规则及EP1状态变化记录；故事stage的EP1展开为故事正文、状态变化。复用文档编辑能力，当前承接由人工核对；既有资产卡只作候选资料，不自动继承旧剧情。

更新：世界规则、state_changes.md、树导航与支持文档编辑入口；共用story/assets指南明确事实生命周期。故事、分镜和prompt内容保持原版本。


## Follow-up 002 — 2026-10-03 22:30:19
Source: user_input/follow_ups/202610.md - section 002
Summary: 实现独立run创建CLI、只读索引/详情API和友好创作记录页；EP新增共享创作输入及记录入口。UI移除三模块和支持文档编辑入口；共享流程固定输入、独立作者/审稿与逐项主编决策。run story-run-20261003-214907-dd638b81生成《一枚铜币》候选：四项作者提案采纳，审稿的魔兽辨识度建议暂缓，无真实否决；正文载入草稿，世界规则与已接受状态未写入候选。技术团队单独标scope。

规则唯一源：.agents/skills/ai-videos-pipeline/modules/story-runs.md；实现与验证记录：.audit/adhoc_agents/2026-10-03/story-run-20261003-214907-dd638b81/。先前支持文档手工编辑约定由本次只读要求替代。


## Follow-up 003 — 2026-10-03 23:18:33
Source: user_input/follow_ups/202610.md - section 003
Summary: 建立EP/shared明确profile及分离input/rules，保留两次完全相同冻结输入。Run1《一枚铜币》，Run2《少掉的两枚铜币》，作者/审稿均新独立上下文；两稿差异和高度相近结构如实保留。新增共享输入/规则友好页面、A/B比较、soft promote CLI和current selection历史/指纹。左侧EP1分共享配置、当前EP1、runs；每run再分产出与过程。UI只读，复制选用命令。

Run2: .audit/adhoc_agents/2026-10-03/story-run-20261003-144640-85f316d4/。共用要求在story-runs.md；旧story_input.json原样移shared/previous_configuration.json，未丢失配置。当前EP1仍选Run1草稿，Run2未自动覆盖；两次同规则不是单条规则的因果验证。验证详情见本run validation.json。

## Follow-up 004 — 2026-10-04 21:55:39
Source: user_input/follow_ups/202610.md - section 004
Summary: 续接《魔兽世界》，核对EP1选用、输入及模块状态，询问具体续接方向。

更新：追加续接要求，重建revised_prompt.md。核对当前正文与Run1候选及选用指纹一致，两run输入哈希和规则一致；故事未确定，分镜和prompt为空。两run的魔兽辨识度意见均为暂缓，下一步建议补充显式背景输入后另跑；用户尚未选择本次方向。故事、共享profile、资产和已有run保持当前版本。

## Follow-up 006 — 2026-10-04 22:47:11
Source: user_input/follow_ups/202610.md - section 006
Summary: 原作主线、滚动连载与自主研究要求；19份直接来源的相关原文/摘要整理为14条共用故事规则。

更新：共用story_guidelines.md、故事模块引用、CONVENTIONS.md未来剧情入口；findings/story-guideline-research-20261004.md保存适用性、研究角度、来源与缺口；revised_prompt.md按原始输入及月度follow-up重建。项目README新增之后制作的游戏主线与指南指针。
核对范围：仅规则/文档；旧profile/run、当前候选、已确定状态、资产、分镜、prompt和媒体未修改。未做新故事生成、独立故事QC或规则效果A/B；规范检查与反例核对见.audit本次任务validation.json。

## Follow-up 005 / 007 — 2026-10-04

Source: user_input/follow_ups/202610.md - sections 005、007
Summary: 先打磨流程，显式列出两run的真实输入、文件版本、任务边界和产出；用户休息期间自主完成本次可见性与相关验证。

更新：新增 `findings/run-input-inventory-20261004.md`，列出两run相同的五份文件、冻结setting、用户追加要求、对照设计、作者/审稿实际输入和不可还原条件；README加入清单入口。UI每run分输入与规则/产出/过程，软链接定位当时快照或与历史SHA256一致的审计文件。未采用的workflow-v2等后续整理文件不追认为生成输入，未知模型/采样条件不补造。

验证与实现归属ai_video_management follow-up190/192，完整记录在 `.audit/adhoc_agents/2026-10-04/run-explicit-io/`。两run.json、input.json、EP故事与选用记录逐文件SHA256均与开工前一致；当前仍为Run1《一枚铜币》草稿。未生成新故事，未确定版本，未改共享profile、长期事实、已确定状态、资产、分镜、Prompt或媒体，未调用付费服务。保留其他会话的后续游戏主线/写作指南要求。


## Follow-up 008 — 2026-10-05 08:47:32
Source: user_input/follow_ups/202610.md - section 008
Summary: 核对剧、集、镜头实际模型，建议补场次与shot/生成片段边界；幕和段落按需要表达。

更新：追加评估请求与结论，按raw_prompt及月度follow-up重建revised_prompt。只做结构评估，未实施schema或流程迁移。核对README、workflow、现行EP1故事/分镜/prompt、模块指南、故事规则及分镜数据模型；现行分镜为空，不能据此判定实际切镜质量或已发生镜头命名错误。示意分场不是已确定改编；未执行独立观众QC、软件修改或付费请求。


## Follow-up 009 — 2026-10-05 09:05:29
Source: user_input/follow_ups/202610.md - section 009
Summary: 核对资产目录、bg登记簿与北郡修道院卡，认可background环境资产与剧情scene分离的方向。

更新：记录方案与关系，重建revised_prompt；未重命名资产目录、未修改模块契约或程序。核对发现资产覆盖空间/布局等完整环境，background应以此定义。方案中的场次为后续改编单位，不自动从旧资产或旧剧情生成；历史run快照保留。

## Follow-up 012 — 2026-10-05 10:59:57

Source: user_input/follow_ups/202610.md - section 012
Summary: 在 EP1 下建立 cue 占位目录，具体音乐流程待后续补充。

Auto-updated:
- `ai_videos/shengji_zhilu/episodes/ep01/cue/.gitkeep` — 保留集级 cue 目录。
- `ai_videos/shengji_zhilu/README.md` — 记录占位用途及后续补充范围。
- `user_input/revised_prompt.md` — 按原始输入及月度 follow-up 重建。

核对：当前仅有 EP1；既有 EP 文件 SHA256 不变，cue 仅含占位文件。无 shot、参考资产、共用规范或应用代码改动，无付费调用；验证记录在 `.audit/adhoc_agents/2026-10-05/episode-cue-placeholder/validation.json`。
