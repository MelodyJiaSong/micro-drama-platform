# Claude / Codex 共用入口

本仓库用于 AI 短剧制作，也包含制作管理应用和 spec-driven 软件流程。Claude 与 Codex 遵守同一套业务规范；当前用户指令及运行环境的工具、权限约束优先。

## 开工与路由

- 先检查工作区改动；保留用户和其他会话的改动。内容中文，结构路径沿用仓库约定。
- 详细共用约定在 [CONVENTIONS.md](CONVENTIONS.md)。开工必读其中 State surfaces、外部服务请求审计（全局必经）、Prompt triage gate、Tool scoping and team coordination、General coding rules；其余按任务读取。
- **AI Video 工作流维护与接续**：先读 [.agents/references/project/ai_video_workflow.md](.agents/references/project/ai_video_workflow.md)。管理 UI「工作流」按 AI Video（创作知识）/ 系统与代码（代码、工具、运行与代理设置）分类，三大模块独立导航，跨剧源编号连续（`tools/workflow_catalog.py`）。修改影响制作的共用指南、设置、模板或工具默认值时同步 `workflow_catalog.json` 并核对覆盖页；正文只改唯一源，不另建代理私有规则。
- **短剧制作**：先读目标剧 README、`workflow.json` 和 `.agents/skills/ai-videos-pipeline/SKILL.md`。剧 README 开头的「Vision（观众体验）」（一句话 Vision 加「核心：」）是全剧宗旨，每个模块创作与审查都对照它；第一原则「观众是主角」，细则见 SKILL.md。声明 `workflow.json: three-module-v1` 的剧只走六模块：故事创作 → 影视改编 → Prompt 编译与出片 → 剪辑 → 声音与音乐 → 成片交付（后三个待设计），按模块读上游；Research 和资产独立。旧流程已删除，旧剧目录只作数据保留（根目录有 `OBSOLETE.md`），不再续跑旧流程；短剧不走 `agent_team`。
- **软件开发**：读 `.agents/references/project/{general,development}.md`、项目 README 和 `specs/development/{name}/`。新建完整 spec-driven 项目用 `agent_team`；已有项目修复按 follow-up 流程做局部修改。
- **规范 / skills 维护**：直接改共用约定和对应源文件；不另建短剧，不启动制作或软件六阶段流程。
- 续跑以文件内容、实际检查及审计为准。产物存在只是候选完成，QC blocker 清零且结论对应当前产物才算完成。

## 外部服务请求审计（全局必经）

所有剧、季、集、共享资产及独立任务，Claude、Codex 与其子任务调用 Dreamina、ElevenLabs、Hyper3D 或后续接入的收费服务时，必须遵守 `CONVENTIONS.md` 同名章节，先读 `.agents/references/project/paid_services.md`，确定归属，先写 `request_log.md` 再调用。查询、下载、失败与重试也留痕；无归属、日志不可写或入口未接入就停止，不能通过直连 CLI / API / MCP / 插件绕过。

本条适用于今后的每次调用，包括续跑、补资产、局部修复、独立 skill、手工命令与子任务；不补造历史请求。授权与「生成永远人点」等原有规则继续有效。

## 一份规则，两个入口

| 内容 | 唯一维护位置 |
|---|---|
| 共用入口 / 详细约定 | `AGENTS.md` / `CONVENTIONS.md` |
| Claude 入口 | `CLAUDE.md`，导入本文件，不另写业务规则 |
| skills 与同目录 playbooks 正文 | `.agents/skills/<共用名称>/`，唯一源文件，Codex 直接发现 |
| 共用参考规则 | `.agents/references/`，两端读取同一份 |
| Claude skill 入口 | `.claude/skills/*/SKILL.md`，自动生成，统一指向 `.agents/skills/` |
| 共用名称 → 旧 Claude 名称 | `.agents/skill-aliases.json` |
| Claude 专用配置 | `.claude/settings*.json`、`.claude/hooks/`、`.mcp.json` |

`.agents/` 是共用 skills / refs 的 source of truth，不在 `.claude/` 维护业务正文或另一份参考规则。修改流程只改 `.agents/` 的源文件；改 name / description / `metadata.claude.argument-hint` 后重跑 `python tools/sync_agent_skills.py`，新增 skill 同时更新名称表，收尾运行 `python tools/sync_agent_skills.py --check`。脚本只生成 Claude 薄入口，不改 Codex 直接读取的源正文；不手改生成入口、不复制正文、不依赖 Windows 软链接。Claude 用 `/ai-videos-…`，Codex 用 `$ai-videos-…`；Claude 原有 `/ai_videos__…` 命令保留并指向同一源文件。若入口尚未被会话发现，直接按路径读正文。

## 工具与收尾

- skills 中工具按**能力**解释，实际映射见 `CONVENTIONS.md` 的 Tool scoping and team coordination。不假定 Claude 工具名、参数、父子权限或 hooks 在 Codex 可用。
- interactive 用本环境可用的提问工具；工具缺失时在对话提问。AUTONOMOUS 不提问，记录判断依据；已有答案或授权继续有效。默认选项、等待超时都不代表用户同意。
- 普通任务可由主代理完成。playbook 要求的可并行工作在工具可用且当前环境允许时委派；限额不足时分批。要求 fresh context 的观众 / 审稿 QC 必须用独立上下文，缺少该能力就记录未审，不由作者自审冒充通过。
- 改分镜、overhead 或参考资产后，对本次范围运行 `python tools/shot_pack.py sync <集目录> [镜头key]`（只报告用 `check`）；工作流目录或共用源增删迁移后运行 `python tools/workflow_catalog.py --fix` 再 `--check`；改 skill 名称或描述后运行 `python tools/sync_agent_skills.py` 再 `--check`。Claude Stop hook 是额外保障；其他环境显式执行。核对 sync / check 的输出，报告失败、未检查范围和未对齐或已失效的资料包，不能只凭退出码宣称全部一致。
- 软件改动执行项目规定且与改动相关的检查；规范改动执行入口、引用、frontmatter 检查。无法执行的验证明确报告。
- 保留「生成永远人点」、锁片前质检与独立审稿、人工剪辑批准、媒体 R2 索引流程。实际工具未连接时说明缺失能力并完成其余可做部分。
- 不把本项目知识写进 Claude 或 Codex 私有 memory。项目意图落 `specs/`，通用规则落上述共用文件，运行审计落 `.audit/`。
