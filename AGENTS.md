# Kimi / Codex 共用工作入口

本仓库用于 AI 短剧制作，也包含制作管理应用和 spec-driven 软件流程。Kimi / Codex 主代理与子代理遵守同一套业务规范；当前用户指令及运行环境的工具、权限约束优先。

## 开工与路由

- 先检查工作区改动；保留用户和其他会话的改动。内容中文，结构路径沿用仓库约定。
- 详细共用约定在 [CONVENTIONS.md](CONVENTIONS.md)。开工必读其中 State surfaces、外部服务请求审计（全局必经）、Prompt triage gate、Tool scoping and team coordination、General coding rules；其余按任务读取。
- **AI Video 工作流维护与接续**：先读 [.agents/references/project/ai_video_workflow.md](.agents/references/project/ai_video_workflow.md)。管理 UI「工作流」按 AI Video（创作知识）/ 系统与代码（代码、工具、运行与代理设置）分类，三大模块独立导航，跨剧源编号连续（`tools/workflow_catalog.py`）。修改影响制作的共用指南、设置、模板或工具默认值时同步 `workflow_catalog.json` 并核对覆盖页；正文只改唯一源，不另建代理私有规则。
- **短剧制作**：先读目标剧 README、`workflow.json` 和 `.agents/skills/ai-videos-pipeline/SKILL.md`。剧 README 开头的「Vision（观众体验）」（一句话 Vision 加「核心：」）是全剧宗旨，每个模块创作与审查都对照它；第一原则「观众是主角」，细则见 SKILL.md。声明 `workflow.json: three-module-v1` 的剧只走六模块：故事创作 → 影视改编 → Prompt 编译与出片 → 剪辑 → 声音与音乐 → 成片交付（后三个待设计），按模块读上游；Research 和资产独立。旧流程已删除，旧剧目录只作数据保留（根目录有 `OBSOLETE.md`），不再续跑旧流程；短剧不走 `agent_team`。
- **教学视频**：先读 [edu_videos/README.md](edu_videos/README.md) 与目标系列 README；产物在 `edu_videos/{系列}/tNN_{知识点}/`，不走短剧流程。
- **软件开发**：读 `.agents/references/project/{general,development}.md`、项目 README 和 `specs/development/{name}/`。新建完整 spec-driven 项目用 `agent-team`；已有项目修复按 follow-up 流程做局部修改。
- **规范 / skills 维护**：直接改共用约定和对应源文件；不另建短剧，不启动制作或软件六阶段流程。
- 续跑以文件内容、实际检查及审计为准。产物存在只是候选完成，QC blocker 清零且结论对应当前产物才算完成。

## 外部服务请求审计（全局必经）

所有剧、季、集、共享资产及独立任务，Kimi / Codex 主代理与子任务调用 Dreamina、ElevenLabs、Hyper3D 或后续接入的收费服务时，必须遵守 `CONVENTIONS.md` 同名章节，先读 `.agents/references/project/paid_services.md`，确定归属，先写 `request_log.md` 再调用。查询、下载、失败与重试也留痕；无归属、日志不可写或入口未接入就停止，不能通过直连 CLI / API / MCP / 插件绕过。

本条适用于今后的每次调用，包括续跑、补资产、局部修复、独立 skill、手工命令与子任务；不补造历史请求。授权与「生成永远人点」等原有规则继续有效。Kimi 与 Codex 均可作为主代理运行同一流程；Codex 出图仍经 `tools/codex_image.py` 记录请求后调用。Claude 已停用，不恢复其入口、配置或新任务执行器；历史产物与审计保留原始来源。

## 一份规则，一个入口

| 内容 | 唯一维护位置 |
|---|---|
| 共用入口 / 详细约定 | `AGENTS.md` / `CONVENTIONS.md` |
| skills 与同目录 playbooks 正文 | `.agents/skills/<共用名称>/`，Kimi / Codex 直接发现 |
| 自定义 agent | `.agents/agents/*.md`，Kimi 直接发现 |
| 共用参考规则 | `.agents/references/` |
| 项目 MCP 唯一源 | `.agents/mcp.json`；`tools/sync_agent_config.py --fix` 生成 `.kimi-code/mcp.json` 与 `.codex/config.toml` |
| hooks 插件源 | `.kimi-code/plugin/kimi.plugin.json` 与同目录 `hooks/` |

`.agents/` 是 skills、agents、refs 的 source of truth，不生成第二份入口或复制正文。修改流程只改源文件；新增或修改 skill 的 name、description、type 后运行 `python tools/check_agent_skills.py`。Kimi 用 `/skill:<name>`，未被系统命令占用时也可用 `/<name>`；Codex 用 `$<name>`；两边都可自然语言指定同一 skill。若入口尚未被当前会话发现，直接按路径读正文。

Codex 直接使用共用入口与 skills；权限、模型和用户配置由本机运行时管理，不复制 Kimi 专用 agent 定义为 Codex 配置。两边收尾都显式运行 `python tools/sync_agent_config.py --check`、`python tools/check_agent_skills.py`、`python tools/workflow_catalog.py --check` 与 `python tools/followup.py check --all`。

Kimi 不支持项目级 hooks 配置。仓库提供可安装插件，首次使用在 Kimi 中执行 `/plugins install .kimi-code/plugin`，然后 `/reload`。插件按用户安装并对所有项目生效，脚本只会识别本仓库；不修改用户级 `config.toml` 来伪造项目 hooks。

## 工具与收尾

- skills 中工具按**能力**解释，实际映射见 `CONVENTIONS.md` 的 Tool scoping and team coordination。工具名、参数、父子权限与 hooks 以当前 Kimi / Codex 会话为准。
- interactive 用本环境可用的提问工具；工具缺失时在对话提问。AUTONOMOUS 不提问，记录判断依据；已有答案或授权继续有效。默认选项、等待超时都不代表用户同意。
- 普通任务可由主代理完成。playbook 要求的可并行工作在工具可用且当前环境允许时委派；限额不足时分批。要求 fresh context 的观众 / 审稿 QC 必须用独立上下文，缺少该能力就记录未审，不由作者自审冒充通过。
- follow-up 与 changelog 只经 `python tools/followup.py new / done` 写入，不手改月度文件与 changelog；收尾运行 `python tools/followup.py check --all`（安装插件后 Stop hook 自动拦），漏记、撞号、格式不对或「待补」超过 6 小时都必须当场补齐。
- 流程与规则分仓库级、剧级两层，拿不准一律先放剧级，升仓库级须用户明确同意（CONVENTIONS「用户报问题」节）。剧目录有 `qc_checks.toml` 的剧按 skill `ai-videos-self-check` 自检：出片后机检并 `python tools/qc.py record`，审稿类检查一律 `python tools/qc_review.py`（另起 Kimi 进程独立审稿；审查单、教学视频台词审与专家审等全部审查同样只用一位 Kimi），交付或进成片前 `python tools/qc.py gate`；用户抓到问题 `python tools/qc.py defect`，用户放行闸门结论 `python tools/qc.py override`。
- 改分镜、overhead 或参考资产后，对本次范围运行 `python tools/shot_pack.py sync <集目录> [镜头key]`（只报告用 `check`）；工作流目录或共用源增删迁移后运行 `python tools/workflow_catalog.py --fix` 再 `--check`；改 skill 元数据后运行 `python tools/check_agent_skills.py`。Kimi Stop hook 是额外保障，不能替代显式检查。核对 sync / check 的输出，报告失败、未检查范围和未对齐或已失效的资料包，不能只凭退出码宣称全部一致。
- 软件改动执行项目规定且与改动相关的检查；规范改动执行入口、引用、frontmatter 检查。无法执行的验证明确报告。
- 保留「扣积分的生成永远人点」（不扣积分的本地视频代理可直接出）、出视频前用户先审整集音频预览（`tools/audio_preview.py`，详见 CONVENTIONS 出图与出片的授权）、锁片前质检与独立审稿、人工剪辑批准。实际工具未连接时说明缺失能力并完成其余可做部分。
- 不把本项目知识写进代理私有 memory。项目意图落 `specs/`，通用规则落上述共用文件，运行审计落 `.audit/`。
