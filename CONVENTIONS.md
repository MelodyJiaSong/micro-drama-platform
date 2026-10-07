# CONVENTIONS.md — Claude / Codex 共用约定

Hosts a **spec-driven workflow** and the platform that drives it. New spec-driven development projects use six stages; AI dramas use their dedicated pipeline. Existing-project fixes and convention maintenance stay scoped to the requested change. Artifacts are plain files so either agent can inspect and resume them.

## State surfaces (explicit determinism)

All workflow / `agent_team` state lives in one of these surfaces. No hidden caches, no other locations:

1. **`AGENTS.md` + `CONVENTIONS.md`** — shared entry and rules. `CLAUDE.md` imports the entry; it does not own separate business rules.
2. **Runtime adapters** — `.claude/settings*.json`, `.claude/hooks/`, `.mcp.json` for Claude. `.agents/skills/<name>/` owns each shared skill's body; `.agents/skill-aliases.json` maps its name to the legacy Claude command. `tools/sync_agent_skills.py` generates only `.claude/skills/` adapters for both command names, pointing to the canonical `.agents/` source. Runtime permissions and connected tools come from the active environment, not from another agent's config.
3. **`specs/{task_type}/{task_name}/`** — per-task pipeline artifacts.
4. **`.audit/adhoc_agents/{YYYY-MM-DD}/{task_id}/`** — runtime spawn logs (`spawns/{worker_id}/{prompt.md, output.md}`), `events.jsonl`, per-round answer JSONs.
5. **Shared skills + playbooks + refs** under `.agents/skills/` and `.agents/references/` — the only maintained workflow sources for both agents; see § Stage playbooks and reference docs. `.claude/` must not contain independent business instructions or reference copies.

**全局制作入口（follow-up194/198）**：管理 UI 的工作流统一导航跨剧创作规则、代理配置声明、服务默认值与制作参考，目录源为 `.agents/references/project/workflow_catalog.json`，登记路径、分类、稳定引用编号及自动发现范围，正文仍在上述唯一维护位置。分为 `1_AI Video` 与 `2_Claude Code与Codex`；AI Video 下三个模块分别是 `1.1_故事创作`、`1.2_影视改编`、`1.3_Prompt编译`。具体源用三级编号，编号随来源身份固定，标题/排序变化不改号、删除不复用；自动发现但未登记编号的源标待编号，禁止按显示顺序重编号。新增跨剧源须进入目录或已登记发现范围；run 里的跨剧来源应可从历史快照跳转至当前全局源，未登记来源明确列出。历史run的编号映射标为当前目录，保留冻结内容与指纹，不补造历史编号或代理设置；用户配置只读脱敏，不读取 memory、凭据文件或执行配置代码。集中展示不改变模块适用范围、授权及收费请求审计。

Rules:

- **工作流覆盖与跨会话维护（follow-up199）**：Claude Code / Codex 按 [.agents/references/project/ai_video_workflow.md](.agents/references/project/ai_video_workflow.md) 维护同一目录与源。新增影响制作的共用指南、模板、静态默认值、环境覆盖入口或编译实现时登记稳定编号并检查「工作流覆盖核对」；此页核对可读取源、编号、文档引用与真实 run 来源，不证明所有源实际加载。局部剧/季/集输入继续在剧导航与 run 快照中；隐藏系统上下文、外部插件内部状态及秘密环境值不宣称穷举覆盖。已结束会话的变更从共用文件、项目规格与审计接续，不写私有 memory。

- **Pipeline status is derived from persisted artifacts and checks, not from memory.** Existing expected files are candidates for completion: read them, verify required sections and QC, and ensure review fingerprints match current inputs. Missing, stale, partial or blocked artifacts mean the stage is not done. Resume logic reads the tree and applicable checks.
- **New mechanisms must land in one of the surfaces above.** No sidecars, session-scoped stores, or side-channel caches.
- **Round-trip artifacts** between parent ↔ workers / user (e.g., `round1_answers.json`, aggregated worker outputs) live under `.audit/`, NOT in `specs/` (which is reserved for canonical user-facing output).
- **Code-navigation indexes are derived caches, not state surfaces.** The optional CodeGraph index at `projects/{name}/.codegraph/` (a symbol/call graph over that project's code, exposed to agents via the `codegraph` MCP server in `.mcp.json`, scoped to `projects/ai_video_management` for the current trial) is a **per-machine, gitignored, rebuildable cache** — a faster substitute for grep/glob fan-out, nothing more. It MUST NOT be treated as authoritative: pipeline status is still re-derived from the filesystem (rule 1 above), and it never indexes the markdown surfaces (`specs/`, `ai_videos/`, `.claude/`). Delete `.codegraph/` and re-run `codegraph index <project>` anytime; never read stale graph data as ground truth.

## 外部服务请求审计（全局必经）

适用于本仓库全部剧/季/集、系列与公共资产、软件任务及独立调用；Claude、Codex、主代理与子任务使用同一契约。全流程、阶段续跑、补资产、局部修复、独立 skill 或手工命令均不能跳过。新剧和旧剧从本条生效后的每次调用都执行，不要求迁移旧剧结构，也不补造历史日志；产物规则的遗留豁免不适用于调用审计。

每次调用 Dreamina CLI、ElevenLabs、Hyper3D、Cascadeur，以及后续接入的收费服务前：

1. 先读 `.agents/references/project/paid_services.md`，核对实际接口、授权、完整请求与剧/集/资产归属。
2. 经 `tools/service_request.py` 的 `RequestLog` 先追加 request 事件并落盘，再调用；无归属或日志写入失败时停止。生成提交、查询、下载、每次重试及失败都记录；结果/错误用同一 request_id 关联。
3. 保留完整文本参数与参考文件元信息，凭据脱敏；日志按每集及人物/场景/道具/装备等资产集合归档，UI「请求日志」审查。详细字段和分组只在 `paid_services.md` 维护。
   能力限制按 `paid_services.md` 的目标model_version及共用模型表核对，区分官方规格与实际调用证据；不把旧CLI帮助统一套给新模型（2026-10-03 Seedance2.5实测修正）。
4. CLI / API / MCP / 插件及新增脚本入口都须先接入相同记录机制；入口未接入就停止，不能直连后补记。工具可用、AUTONOMOUS、旧剧或批量任务均不构成豁免；原有生成与人工剪辑授权继续执行。

委派涉及外部服务调用时，主代理须在任务说明中传递本契约、目标归属及共用文档路径；执行者自行完成调用前记录，不能由主代理事后补造。运行时无法观察 CLI 内部 HTTP 或无法拦截外部已安装工具的边界，按服务文档明确报告。

## 场景 / 背景图片的生成服务

Claude、Codex 与子任务为所有剧生成或重生成 scene/bg 图片（世界锚点、场景锚点、各方向 plate、时间/天气变体及 shot 专用背景）时，只能使用 **GPT 最新图像模型或 ElevenLabs**；**禁止 Dreamina/Seedream，包括 auto 模式失败后的回退**。新剧全程执行，旧剧今后的调用同样执行；不据此批量重生旧资产。人物、道具、装备和 Seedance 视频不在本条图片范围内。

指定“GPT 最新模型”时，调用前核对官方文档及实际入口支持的型号，记录实际 model_id；型号不公开的内置工具不能声称已验证最新具体型号。模型不可用时报告，不能静默降级或改用 Dreamina。服务与型号、完整 prompt、参考文件哈希、生成 ID、费用/未知费用继续按上节先记请求；出图后逐张看图并绑定新 SHA 审图，替换资产后同步、检查受影响资料包。执行入口：`tools/gen_bg_images.py` / `tools/image_engine.py`；审图：`tools/scene_review.py`；详见 `.agents/references/project/paid_services.md`。

## Auto-memory is disabled

Do not use agent-private auto-memory for this repository. Do not read or write `.claude/memory/` or `~/.claude/projects/<slug>/memory/`, and do not create a parallel Codex memory copy. Repository facts and lessons belong to the shared state surfaces. Higher-priority runtime instructions still apply.

If you'd save a memory entry, persist to a state surface instead:
- Cross-conversation rules → `CONVENTIONS.md`.
- Per-project intent → `specs/{type}/{name}/`.
- Per-run audit → `.audit/adhoc_agents/{date}/{task_id}/`.
- Harness config → the active runtime adapter (see § Tool scoping and team coordination).

The urge to save memory is a signal that one of the surfaces is missing the information. Put it there instead.

## Repo layout

```
micro-drama-platform/
├── AGENTS.md                             # shared entry; both agents read it
├── CONVENTIONS.md                        # this detailed contract
├── CLAUDE.md                             # imports AGENTS.md
├── .agents/                              # shared source of truth
│   ├── skill-aliases.json                # shared names → legacy Claude commands
│   ├── skills/<name>/SKILL.md            # canonical bodies; Codex reads directly
│   │   └── playbooks/                    # supporting runbooks, where needed
│   └── references/{interview,research,validation,project}/
├── pyproject.toml                         # canonical Python deps; `uv sync` reads this
├── requirements.txt                       # mirror for pip fallback
├── README.md
├── .claude/
│   ├── skills/<shared-or-legacy-name>/SKILL.md  # generated references to .agents
│   ├── hooks/                            # Claude lifecycle adapters
│   └── settings*.json                    # Claude runtime configuration
├── specs/
│   └── {task_type}/{task_name}/
│       ├── user_input/{raw_prompt.md, revised_prompt.md, follow_ups/{YYYYMM}.md}
│       ├── interview/{qa.md, promoted.md}
│       ├── findings/{angle-*.md, dossier.md, promoted.md}
│       ├── final_specs/{spec.md, promoted.md}
│       ├── validation/{strategy.md, acceptance_criteria.md, ..., promoted.md}
│       └── changelog.md                   # append-only follow-up log
├── projects/{name}/                       # task_type=development outputs
├── ai_videos/{name}/                      # task_type=ai_video outputs
└── .audit/adhoc_agents/{YYYY-MM-DD}/{task_id}/   # gitignored; events.jsonl + spawns/
```

## task_type enum

Required when starting a production / development pipeline. Choose from the known target; ask if unclear. Common convention maintenance is not a new production task and needs no fabricated task_type / project.

- `development` — software outputs land in `projects/{name}/`. Walks the **six-stage `agent_team`** workflow below.
- `ai_video` — AI 短剧产物落在 `ai_videos/{name}/`；不走 agent_team。新流程用 `ai-videos-pipeline` 的故事创作 → 影视改编 → Prompt 编译，Research与资产独立支持；媒体制作按需执行原有人工关卡。见下文「AI 短剧创作」。

## The six-stage workflow (task_type=development)

The skill `agent_team` is the single entry point for **`development`** tasks and walks all six stages. Users invoke it as Claude `/agent-team`, Codex `$agent-team`, or by asking for a spec-driven software task; legacy Claude `/agent_team` remains available. **For `task_type=ai_video`, use `ai-videos-pipeline` (source `ai_videos__全流程编排`) instead (§ AI 短剧 pipeline).**

| # | Stage | Output | Coordination |
|---|---|---|---|
| 1 | Intake | `user_input/{raw,revised}_prompt.md` | parent-direct, no workers |
| 2 | Interview | `interview/qa.md` | parent-direct, optional category workers |
| 3 | Research | `findings/{angle-*.md, dossier.md}` | parent-direct + parallel angle workers |
| 4 | Spec compilation | `final_specs/spec.md` | parent-direct, no workers |
| 5 | Validation strategy | `validation/{strategy.md, ...}` | parent-direct + parallel level-specialist workers |
| 6 | Execution + streaming validation | `projects/{name}/` | parent-direct + validators per work unit when available |

The procedural detail for each coordinated stage lives in `.agents/skills/agent-team/playbooks/{interview,research,validation}.md`. The parent-direct coordination model — and why there is no manager-subagent layer — is documented once in § Tool scoping and team coordination.

## AI 短剧创作

three-module-v1的影视改编按episode→scene→shot组织。scene表示剧情场次，环境资产称background；《魔兽世界》资产目录迁为background，其他旧剧保留scenes兼容读取。分镜及prompt契约唯一正文在共用pipeline modules/filming.md与prompts.md；稳定key采用ep1_s1_st1，编号不随重排改变。旧run冻结输入与历史日志不回写，媒体迁移保持字节及bg编号并同步实际路径引用和R2索引。

新流程为三个模块：故事创作 → 影视改编 → Prompt 编译；Research 与资产独立支持。
所有剧今后新写/本次修改剧情按[通用故事指南](.agents/references/project/story_guidelines.md)组织与核对；原作版本、改编边界及已确定状态显式输入，不套固定长片序列数。新规则选用版本留存，不重写历史profile/run或自动回溯旧剧情。
`workflow.json` 声明 `three-module-v1`，本剧输入输出在 `episodes/epNN/{story,filming,prompts}.json`。
唯一编排源是 `.agents/skills/ai-videos-pipeline/SKILL.md` 及其 `modules/`。新流程不加载旧0–7阶段、自动审查套件或角色访谈系统。
一次只改一个模块；下游提出上游修改请求，不擅自重写。上游确定版本后交接，上游改变则下游保留并标记待更新。
创作结果保存并绑定输入版本；prompt编译是固定转换。POC先做一个小场景，逐次比较、接受或回退。
长期事实在资产库的世界规则或选定资产卡维护；截至某集的位置、伤势、持有物、知识、关系、目标等变化记录在该集state_changes.md。按集序承接已确定的变化，不读取未来集，不把草稿当既成事实；POC先用人工核对。
所有运行时的故事生成/重跑按`.agents/skills/ai-videos-pipeline/modules/story-runs.md`执行独立run：冻结输入/规则及来源哈希；原始协作和候选在.audit，每集仅存索引；逐项记录真实参与者、意见、采纳/否决/延后理由、决策者及对应修改。未确定候选不自动污染长期事实/集状态；上一run不默认成为下一run输入。
每run以输入与规则/产出/过程目录显式展示实际影响本run的文件、设定、任务指令和运行条件，逻辑软链接定位冻结版本并核对源文件变化；未记录条件明确标缺项，不能用后续整理文件补造历史输入。详细契约只在上述story-runs.md维护。来源：2026-10-04用户要求完整run输入/产出及依赖可见。
三模块创作UI只读，修改通过Claude Code/Codex。共享输入/规则为persistent；每run输入快照、候选产出和过程记录独立保留，并分别标明用途与范围。transient表示不自动跨run继承，不表示删除历史。
共享输入/规则使用EP/shared/的显式版本，独立于run；同规则对照必须核对冻结输入与规则，而非默认用最新流程。任意run可soft promote成当前EP草稿，候选保留；选用绑定及历史在EP维护，不等于确定故事或世界事实。
现有其他剧保持原产物；新结构先在魔兽世界落地。服务审计、人工生成/剪辑和R2媒体契约继续有效。

## Skill + playbook naming

- Canonical skills live in `.agents/skills/<name>/SKILL.md`, with matching lowercase ASCII hyphenated names (`agent-team`, `ai-videos-*`). `.agents/references/` holds shared references. `.claude/skills/` contains generated adapters only, never another copy of the workflow.
- 原 `agent_team` / `ai_videos__{中文名}` 是兼容名称，映射在 `.agents/skill-aliases.json`；旧中文称呼可继续出现在正文引用和 stage playbook 文件名里（`ai_videos__stageN_*`），不代表另一份源文件。
  - Claude 用 `/name`，Codex 用 `$name` 或自然语言；原 Claude 命令保留并指向同一 `.agents/` 源正文，相对路径以源目录为准。源正文从实际消息读取参数；Claude 参数提示保存在源 frontmatter 的 `metadata.claude.argument-hint`，同步脚本将其转换为 Claude 入口的 `argument-hint`，并在该入口展开 `$ARGUMENTS`。不把未展开占位符放进共用工作流。
- Stage playbooks live under `.agents/skills/agent-team/playbooks/`. They are NOT subagent definitions — they are runbooks the parent reads inline.
- `.claude/agents/` is reserved for future permanent subagents (currently empty; every spec-driven stage is parent-direct).
- Workers, when available and permitted, are general-purpose subagents driven by playbook prompts, captured under `.audit/adhoc_agents/{date}/{task_id}/spawns/`.
- YAML frontmatter `description` field has a hard ceiling of **500 characters**.

## Stage playbooks and reference docs

Two folders sit alongside the workflow, with intentionally separate lifecycles:

- **Playbooks** at `.agents/skills/agent-team/playbooks/{interview,research,validation}.md` — the procedural runbook for each coordinated stage. The contract for *what the parent does*.
- **Refs** at `.agents/references/` — accumulated institutional memory. *What the parent has learned*. Two scopes:
  - **Stage-scoped:** `.agents/references/{interview,research,validation}/{general.md, <task_type>.md}` — what's been learned at each stage.
  - **Project-scoped:** `.agents/references/project/{general.md, <task_type>.md}` — cross-cutting rules about the *outputs* (e.g., light-theme app chrome for development webapps). NOT for project-specific facts (those go under `specs/`) and NOT for harness contracts (those stay in `CONVENTIONS.md`).

**Pre-reading contract.** Before each coordinated stage (2, 3, 5) and before each stage-6 work-unit `validation.started`, the parent MUST read:
1. The stage playbook.
2. `.agents/references/{stage}/general.md`.
3. `.agents/references/{stage}/<task_type>.md`, if present.
4. `.agents/references/project/general.md`.
5. `.agents/references/project/<task_type>.md`, if present (`ai_video`: the canon `ai_video.md` only — `ai_video_history.md` / `ai_video_harness.md` are history, grep on demand).

The parent records each file it actually read as `{path, sha256}` (SHA-256 of the file's bytes at read time) in a single `pre_reading_consulted` array on the run's first `events.jsonl` event for that stage (or on each `validation.started` event in stage 6). The hash turns the event into a reproducibility receipt — two runs can diff "did the playbook or a ref drift between us?" without git archaeology. A missing or empty array is a **critical failure** — institutional memory wasn't loaded.

**Precedence when rules conflict:** per-task-type ref > matching `general.md` in same folder; project-scoped ref > stage-scoped ref > playbook default. A project-specific spec under `specs/{type}/{name}/` may override project-scoped refs for that one project, with a note explaining the divergence.

**Update protocol.** Surgical only — one new principle / severity row / required move at a time, with a one-line citation of the source run / follow-up. Wholesale rewrites are anti-patterns; the goal is to grow institutional memory.

**Why three folders, not one:** different lifecycles. Playbooks change rarely; stage refs accumulate per stage; project refs accumulate per task-type. Folding them together would either balloon the playbook past readability or conflate stage-time-of-use with output-time-of-use.

The spec_driven webapp's `EXPOSED_TREE` recursive globs (`.agents/skills/agent-team/playbooks/*.md`, `.agents/references/**/*.md`) auto-pick up new subfolders.

## Project rules (under `projects/`)

- One folder per project; no cross-project imports.
- **Solution layout is mandatory** — `apps/{api,ui,…}/` for executables, `libs/{infrastructure,domain,application,common}/` for shared code, each layer sub-bucketed by role (`application/{queries,commands,dtos,mappers}`, `domain/{entities,value_objects,errors,repositories}`, `infrastructure/{readers,writers,clients,daos,middleware}`; `common/` stays flat). Within each role sub-folder, one file per aggregate: `{aggregate}__{role}.py`. For `commands/` + `queries/` the file holds EXACTLY ONE class (`{Aggregate}Command` / `{Aggregate}Query`) with one method per operation — e.g., `ActorCommand.generate(...)`, `.generate_diverse(...)`, `.delete(...)`. For `dtos/` the file holds both Qdtos and Cdtos for that aggregate (the suffix on the class name disambiguates). Routes follow the same pattern: `apps/api/routes/{aggregate}__route.py`, each with its own `APIRouter()`; `routes/__init__.py` combines them into a single `router` that `app_factory.py` mounts. Authoritative spec: `.agents/references/project/development.md` §1. The old `backend/` + `frontend/` shape is retired.
- **Routes / job entries / CLIs do NOT import infrastructure directly.** Every endpoint maps to exactly one application-layer Query or Command method. Empty `libs/application/` while `apps/*` has executables is a stage-5 `blocker` — see `.agents/references/project/development.md` §6b and `.agents/references/validation/development.md` §11b.
- **Commands go through `libs/domain/`** (entities + value objects + repository protocols). Read-side queries may skip the domain layer per development.md §3 carve-out; state changes may not.
- **Single Responsibility Principle** — one concern per file. Exception classes don't live in writer/reader files (extract to `libs/infrastructure/errors/{aggregate}__error.py`); DAO dataclasses go in `libs/infrastructure/daos/{aggregate}__dao.py`; DTOs go in `libs/application/dtos/{aggregate}__dto.py`; Pydantic request bodies stay with the route handler. See `.agents/references/project/development.md` §1.
- **File size guideline** — prefer `< 100 lines`, split by sub-concern (mirroring the layer's role taxonomy) when bigger. Hard cap is around `~1000` lines with no clear sub-concern boundary (stage-5 `warning`). See `.agents/references/project/development.md` §1.
- Python: own `requirements.txt` (direct deps only); mirrored into root `pyproject.toml`; root `requirements.txt` is the pip fallback. `apps/*` Python uses `dependency_injector` per development.md §5.
- Strong typing on every parameter, return, and attribute. Use `str | None`, not `Optional[str]`. `@dataclass(frozen=True)` for value objects and DTOs; mutable `@dataclass` only for entities with invariant-guarded mutation methods.
- Frontend (`apps/ui/`): standard React; `node_modules/` in `.gitignore`. DDD layering does NOT apply to UI code.
- README required and updated alongside any feature change.
- **Cross-cutting project-output rules** (themes, visual defaults, structural conventions, DDD+CQRS layering details) live in `.agents/references/project/` per § Stage playbooks and reference docs — NOT in this section.

## AI video rules (under `ai_videos/`)

- **外部服务调用必留痕**：遵本文件 § 外部服务请求审计（全局必经）及 `.agents/references/project/paid_services.md`；所有剧与独立调用均适用。

规则全在 **`.agents/references/project/ai_video.md`（资产与媒体工具参考，≤ 60 KB；三模块POC按需读，不加载旧制作阶段）**：每条一行 + 机检指针。
来历、事故、已废止条款在 `ai_video_history.md`（2026-09-28 拆分前全文）与 `ai_video_harness.md`，按 rule 号 grep、不通读。本节只留会话层面的硬约束：

- **新规则怎么进**：单剧教训先写 `specs/ai_video/{name}/lessons.md`；第二部剧复现或用户明说全局，才在 `ai_video.md` 加一行（≤ 2 行 + 机检指针），来历写进 `ai_video_history.md` 文末「沿革」。能量化的写成闸门。`tools/check_canon.py`（Stop hook）查体量。
- **产物规则变更不回溯旧剧**：新规则只管新产物与这次改到的镜；旧镜 / 旧集走显式遗留清单（只减不增，如 `seedance.toml` 的 `legacy_eps`）。本条不豁免 § 外部服务请求审计（全局必经）。
- **出片**：第一镜出片前整集 animatic 必须过审（rule 44，`seedance_kit open` 闸门）；「生成」永远人点；上传的是 `## Seedance prompt` 精简稿（rule 12.4-P，≤ 2000 字）；**改了 shot prompt，回复里必须告诉用户改了哪几镜、资料包是否全部一致**（rule 12.4-K）。
- **音频**：每剧 `seedance.toml` 声明 `audio_mode`（native / tts_first，rule 12.4-H2）；Seedance prompt明确保留本镜指定对白、自然环境声和动作声，禁止背景音乐/配乐，无对白镜明确没有人说话，出片后试听核对。三模块由Prompt编译固定写入；配乐在后期独立设计，不恢复legacy BGM。既有后期工具的字幕与响度规则见 `tools/post/finish_ep.py`（rule 42）。
- **媒体走 R2 不走 git**：`ai_videos/assets.json` 是索引，`tools/assets_sync.py`；先传字节再提交索引。
- 单剧偏离写 `specs/ai_video/{name}/` 的 divergence。

## Event stream

`.audit/adhoc_agents/{date}/{task_id}/events.jsonl` is append-only JSONL. Lines parse independently; atomic line-sized appends are safe. Event types:

`exec.unit.started`, `exec.unit.completed`, `validation.started`, `validation.issue.raised`, `validation.pass`, `validation.requires_manual_walkthrough`, `exec.revision.applied`, `pipeline.halted`, `regen.delete.planned`, `regen.delete.completed`, `regen.write.completed`.

The parent writes during stage 6 runtime validation and at the start of each coordinated stage to record `pre_reading_consulted`.

### Event schema

Every event MUST have the common envelope: `ts` (ISO 8601 UTC string), `type` (one of the event types above), `task_id` (`{task_name}-{YYYYMMDD-HHmmss}`).

Per-type required fields, in addition to the envelope:

- `exec.unit.started` / `exec.unit.completed` / `exec.revision.applied`: `work_unit_id`, `work_unit_kind`.
- `validation.started`: `work_unit_id`, `levels: string[]`, `pre_reading_consulted: {path, sha256}[]`.
- `validation.issue.raised`: `work_unit_id`, `issue_id`, `level`, `severity`, `description`.
- `validation.pass` / `validation.requires_manual_walkthrough`: `work_unit_id`.
- `pipeline.halted`: `reason`, optional `work_unit_id`.
- `regen.delete.planned` / `regen.delete.completed`: `path`, optional `count`.
- `regen.write.completed`: `path`, `size_bytes`.
- Stage-entry events (the synthetic event that opens each coordinated stage): `stage` (int 1–6), `pre_reading_consulted: {path, sha256}[]`.

Unknown fields are allowed (forward-compatible). Missing required fields are a critical failure — the event is treated as if it didn't run, and the stage halts on synthesis.

### Date-level task index

`.audit/adhoc_agents/{date}/index.jsonl` is append-only and gives a one-line summary per task started that day. At task start, append `{ts, task_id, task_type, task_name, status: "started", run_dir}`. At terminal status (clean exit or `pipeline.halted`), append `{ts, task_id, status: "completed" | "halted", terminal_reason?}`. Readers derive current status from the **last** entry per `task_id` — never edit prior lines. The index is the cheap "what ran today / which task halted" lookup; the per-task `events.jsonl` is the full detail.

## Prompt triage gate (every prompt)

Before doing any work, triage how the current prompt relates to the spec-driven ecosystem. This runs on **every** prompt — including casual ones — and produces exactly one of three outcomes:

1. **Common-level rule** — the prompt establishes a rule, convention, or contract that affects all spec-driven projects, the workflow itself, or the harness. Extract the abstracted rule (NOT the prompt's wording or its non-spec-driven framing) and update the right common surface:
   - Workflow contracts, state surfaces, cross-cutting conventions → `CONVENTIONS.md`.
   - Stage-procedure changes → `.agents/skills/agent-team/SKILL.md` or `.agents/skills/agent-team/playbooks/{interview,research,validation}.md`.
   - Accumulated institutional memory (stage-scoped or output-scoped) → `.agents/references/{interview,research,validation,project}/{general.md,<task_type>.md}` per § Stage playbooks and reference docs.
   - Harness config (hooks, permissions, env) → `.claude/settings.json` / `settings.local.json`.
2. **Project-scoped instruction** — the prompt adds intent to one existing spec-driven project. Run § Follow-up prompt handling below.
3. **Neither** — casual chat, general question, or task with no spec-driven impact (e.g., "hello", a one-off shell question). No persistence. Answer normally.

Rules for outcome 1 (common-level updates):

- **Extract the rule, not the prompt.** Strip examples that don't generalize, personal framing, and any non-spec-driven preamble. The committed text should read as a project convention, not a quoted instruction.
- **Surgical edits only.** Add the smallest unit that captures the rule (one section / one bullet / one ref row). Don't restructure surrounding text.
- **If the prompt is ambiguous** between common-level and project-scoped, ASK the user — do not silently pick.
- **"Nothing to update" is a valid conclusion** — but only after the triage is actually run. Skipping the triage is the failure mode.

The triage is itself a state-surface discipline: every rule the user gives must land in one of the surfaces named in § State surfaces, or be deliberately classified as non-persistent.

## Follow-up prompt handling

Once a spec-driven project exists, follow-up chat may contain additional intent for it. Triage every new prompt before doing anything else.

1. **Triage.** Casual chat / general question with no spec-driven impact → answer normally, no persistence. Real instruction → classify which project. **If ambiguous (project X, Y, or none), ASK the user** — do not silently pick.
2. **Persist** by APPENDING to the current month's log at `specs/{type}/{name}/user_input/follow_ups/{YYYYMM}.md` (e.g. `202608.md`). Never create a per-follow-up file; a new file is started ONLY when the month rolls over. Append a section headed `## NNN — {YYYY-MM-DD HH:mm:ss} — {slug}` (NNN zero-padded, sequential per project, continuing across months), preceded by a `---` rule. Contents: abstracted instruction (drop chitchat) + a one-line summary. Body headings start at `###` so they nest under the section. An OPTIONAL routing-hint block may follow the header as a blockquote — YAML frontmatter cannot repeat inside a combined file (all fields optional):
   ```
   > target_stage: 1 | 2 | 3 | 4 | 5 | 6        # which stage this instruction primarily affects
   > target_artifacts:                            # specific files the walk should examine first
   >   - validation/security.md
   >   - final_specs/spec.md
   > severity: low | medium | high                # how invasive the patch is allowed to be
   ```
   The routing-hint block is a hint, not a contract — the downstream walk still inspects every artifact. Omit the block entirely if no routing hint is needed.
3. **Regenerate `revised_prompt.md`** = `raw_prompt.md` + every `follow_ups/*.md` in filename (chronological) order, and within each monthly log every `## NNN` section in order. No confirmation needed.
4. **Walk downstream artifacts** in order: `interview/qa.md` → `findings/dossier.md` + per-angle → `final_specs/spec.md` → `validation/strategy.md` + per-level → generated outputs under `projects/` or `ai_videos/`.
5. **Auto-update affected sections in place.** Smallest change that resolves the conflict / fills the gap. Surgical only; no whole-file regen. Inline markers (`<!-- auto-updated by follow-up NNN -->`) are NOT added by default — ask the user if a particular update is invasive enough to warrant one.
6. **Append `changelog.md`** at `specs/{type}/{name}/changelog.md`:
   ```markdown
   ## Follow-up NNN — {YYYY-MM-DD HH:mm:ss}
   Source: user_input/follow_ups/{YYYYMM}.md - section NNN
   Summary: {one line}

   Auto-updated:
   - {path} — {one-line description}

   No conflicts found in: {list}
   ```
7. **Never auto-trigger a full stage regeneration.** Surgical patches only. Full regen is user-triggered (the `changelog.md` entries are the user's signal that downstream artifacts were touched).

## Regeneration prompts & autonomous mode

The `spec_driven` webapp emits **copy-paste regeneration prompts** the user pastes into Claude Code or Codex to re-run one or more stages. Every such prompt opens with one of two execution-mode headers — The active agent MUST honor them at the top of a turn's input.

**Header contract:**

- **`# EXECUTION MODE: AUTONOMOUS`** —
  - Do NOT ask the user or call any user-input tool. Not for clarification, not for "A or B," not for confirmation. The user is not at the keyboard.
  - For ambiguity, use best judgment AND record it inline in the produced artifact (e.g., `*(judgment call — chose X because Y)*`) so the user has a self-explaining trail.
  - Produce every requested artifact in the same turn before stopping; do not pause for confirmation between stages. Iteration bounds (§ below) still apply — when a bound trips, halt cleanly with a `pipeline.halted` event + summary.
  - Every other rule still applies (state surfaces, agent-spawning contract, follow-up procedure for new instructions arriving mid-run). Autonomous removes intermediate questioning; it does not supply approvals required for generation, publishing or destructive source changes.
- **`# EXECUTION MODE: INTERACTIVE`** — default. Use the active runtime's user-input capability when intent is genuinely ambiguous and not inferable from existing artifacts (see § Tool scoping and team coordination).
- **No header** = INTERACTIVE.

**What the webapp generates.** `POST /api/regen-prompt` (FR-14c) inlines the project's current `revised_prompt.md` (or `raw_prompt.md` if no revised yet) plus every `user_input/follow_ups/*.md`. A pasted regen prompt is therefore self-contained.

**Defaults.** The webapp's autonomous-mode toggle defaults to **off** (interactive); accidental autonomous runs should not be the path of least resistance. The toggle persists in browser `localStorage` under `spec_driven.autonomous_mode.v1` (no server-side persistence — autonomous is per-prompt, not global).

### Regeneration semantics: read-zero from prior outputs

A regeneration deletes the regenerated stage's prior outputs and rewrites from scratch. Surgical preservation of prior text is **forbidden** during regen — it makes the output a function of (input ∧ all previous runs) and defeats the workflow.

This read-zero contract applies to the development spec pipeline. AI-video regeneration uses its stage playbook and ai_video.md rules 10 / 16.4: rewrite selected Markdown / derived outputs, preserve media, cards, ledgers and unrelated episodes; never delete a media-bearing shots tree as a software stage-6 output.

The regenerated stage reads ONLY:
1. The current stage's *input* artifacts (canonical outputs of prior stages).
2. `AGENTS.md`, `CONVENTIONS.md` and shared `.agents/` context (skill, playbooks, refs).
3. The user-input layer (`raw_prompt.md` + every `user_input/follow_ups/*.md`).
4. The current stage's `<stage>/promoted.md` sidecar, if present (see § Pinned items).

Per-stage delete-then-regenerate contract:

| Stage | Delete first | Preserve | Inputs |
|---|---|---|---|
| 1 — Intake | (none — `revised_prompt.md` rewritten in place from raw + follow-ups) | n/a | `user_input/raw_prompt.md`, `user_input/follow_ups/*.md` |
| 2 — Interview | `interview/qa.md` | `interview/promoted.md` | `user_input/revised_prompt.md`, `interview/promoted.md`, `CONVENTIONS.md`, `.agents/skills/agent-team/{SKILL.md, playbooks/interview.md}`, `.agents/references/{interview,project}/*.md` |
| 3 — Research | `findings/*` except `promoted.md` | `findings/promoted.md` | `revised_prompt.md`, `interview/qa.md`, `findings/promoted.md`, `CONVENTIONS.md`, `.agents/skills/agent-team/{SKILL.md, playbooks/research.md}`, `.agents/references/{research,project}/*.md` |
| 4 — Spec | `final_specs/spec.md` | `final_specs/promoted.md` | `revised_prompt.md`, `interview/qa.md`, `findings/dossier.md` (+ angles if useful), `final_specs/promoted.md` |
| 5 — Validation | every file under `validation/` except `promoted.md` | `validation/promoted.md` | `final_specs/spec.md`, `validation/promoted.md`, `CONVENTIONS.md`, `.agents/skills/agent-team/{SKILL.md, playbooks/validation.md}`, `.agents/references/{validation,project}/*.md` |
| 6 — Execution | the explicitly selected development outputs under `projects/{name}/` (respect user edits) | (no v1 promoted.md in stage 6) | `final_specs/spec.md`, every file under `validation/`, `CONVENTIONS.md`, `.agents/references/project/*.md` |

Operational notes:

- Delete is real `rm -rf`-equivalent, not logical "treat as missing." Stale bytes are how surgical-edit regen creeps back in. `<stage>/promoted.md` stays in Preserve, never Delete.
- **Multi-stage regen is sequential.** Delete each stage's outputs the moment that stage runs (after inputs are confirmed), not all up-front; otherwise stage N+1 is missing its inputs.
- **Selective module regen.** If the prompt selects only some stage modules (e.g., only `validation/security.md` + `performance.md`), delete only those files. Default copy-paste prompts select all.
- **`changelog.md` and `.audit/` are NEVER regen outputs.** They are the audit log; they get appended to with a record of what was deleted/regenerated.
- **Project README and Makefile** may be stage-6 outputs; regenerate them only when selected in the requested development scope, preserving unrelated user edits.
- **AI-video episode scope**: `scope=episode N` / `episodes M..N` regenerates the selected stage's Markdown and permitted derived outputs for those episodes only, using the drama's actual legacy or numbered directory layout. Preserve media, cards, ledgers, other stages and other episodes; never delete an entire media-bearing episode / shots tree. `scope=project` expands the selected stage to the project, with the same preservation rules (ai_video.md rules 10 / 16.4).
- **The `agent_team` skill, playbooks, and agent_refs** are NOT regen outputs — they are harness context. Never deleted by a project-scoped regen.

Audit-event contract for any regen: emit `regen.delete.planned` (one line per file before delete), `regen.delete.completed` (with count), `regen.write.completed` (path + size after write) into `events.jsonl`. The webapp's `build_regen_prompt__query.py` includes this contract in every assembled prompt's `### Constraints` section.

### Pinned items survive regeneration

Each spec-pipeline stage (interview, findings, final_specs, validation) supports a `<stage>/promoted.md` sidecar. The user pins atomic items via the spec_driven webapp (`POST /api/promote`); they're written to `promoted.md` and deleted via `DELETE /api/promote`.

1. **`<stage>/promoted.md` is an INPUT, not an output.** Preserved across regen (Files-to-preserve column above).
2. **Every pin appears verbatim in the regenerated artifact** at the natural insertion point for its source-file/id metadata. Newly-generated content for a pinned slot is dropped — promoted always wins.
3. **Orphaned pins** (insertion point gone) go to a `## Pinned items (orphaned)` section at the end of the originally-pinned source file. NEVER silently dropped.
4. **Editing a pin updates `promoted.md` only.** The generated artifact is touched at the next regen. Drift between editions is acceptable; users resolve it by running stage N regen.
5. **`<stage>/promoted.md` is itself viewable / editable** through the webapp via the same path-sandbox. It is NOT a regen target.
6. **Stage 6 (project code) has no v1 promotion** — different granularity story, deferred.

## 人物参考按需上传（2026-10-03 用户全局裁定）

Claude/Codex共用：所有新剧在 `seedance.toml` 写 `character_reference_mode = "uploads"` 与 `character_reference_layout = "triptych"`，每镜上传入画角色当前造型的一张三视图合图；native模式仅画内发声者另上传对应MP3，画外/OS沿用后期配音。不依赖预建Seedance entity；合图的三个人像是同一人的三个角度，不生成三个人，不复述声样内容。shot保留裸 `=>@`；Reference uploads逐项绑定真实文件，资料包按实际顺序填图片/音频编号与哈希。缺图/声音绑定不清即阻碍，不能静默退回entity。

已有剧只在用户指定范围迁移；本次仅《魔兽世界》全部现行prompt，不动其他剧或归档。请求仍走 `.agents/references/project/paid_services.md` 的唯一日志入口；先确认当前CLI/模型容量，超限不能静默删参考或假称可自动提交。详细产物规则见 `ai_video.md` rule 4 / 12.4-H2。

**人物资产文件名（2026-10-03，全剧通用）**：所有剧、季、集及系列共享资产的所有 character（主配角、NPC、龙套、怪物）今后新建、补齐、重生成、抽帧或导入三视图/声样，统一 `characters/{角色}/views/{角色}_front.png`、`{角色}_side.png`、`{角色}_back.png`、`{角色}_audio.mp3`；`{角色}`＝角色目录名。换装图保留各造型子目录，用 `{造型键}_front/side/back.png`，声音复用角色自己的 `_audio.mp3`。front/side/back 分别是正/侧/背，生成与导入不得再写 views1/2/3、views.mp3 或中文方向后缀；不按旧数字顺序猜方向。迁移先看图、保留字节与哈希、更新真实路径及按镜资料包，不能靠改名宣布原图质量过审。Claude/Codex执行同一规则；其他旧剧已有文件兼容读取，不批量改名，这不豁免其今后的新产物。

**三视图合图交接（2026-10-03，follow-up 102）**：所有剧、所有character今后的资产流程在三张源图齐备后，用 `python tools/character_sheet.py ai_videos/{剧}` 确定性拼接；左front、中side、右back，原像素保留，尺寸不同时等宽格内居中补边，不裁切/拉伸/重画。基础输出 `views/{角色目录名}_views.png`，换装输出 `{造型键}_views.png`；三张源图及 `_audio.mp3` 保留。合图内写源图SHA，源图改变须重建合图；每人只上传合图，native画内发声者另传声样，不同时上传三张单图。声明 `character_reference_layout = "triptych"`；缺合图/源指纹过期即阻碍。此规则适用于今后的所有剧和角色，历史单图镜只在指定范围迁移。合图三格代表同一角色三个角度；原图朝向质量问题仍须单独验收。

## Tool scoping and team coordination

工具按能力选择；下面的名字是示例，以会话实际暴露的工具及 schema 为准。只对延迟工具做发现，不向 Codex 调用 Claude 的 ToolSearch。不把某次 Claude 会话的父子权限限制当跨运行时事实。

| 能力 | Claude Code 示例 | Codex 示例 / 缺失时 |
|---|---|---|
| 读写文件、执行脚本 | Read / Write / Edit / Bash | 文件、补丁、shell 工具；Windows 按实际 PowerShell 语法执行 |
| 提问 / 收集答案 | AskUserQuestion；延迟时 ToolSearch | 可用的 request_user_input 或 request_user_input_async；遵守模式 / 参数限制；都不可用时在对话提问 |
| 检索与读原文 | WebSearch / WebFetch | 可用的 web search / open / fetch；有已加载工具时直接用 |
| 委派与等待 | Agent | 可用的 spawn_agent / send_message / wait_agent；限额不足分批，普通工作可主代理直做 |
| 看本地图片 / 浏览器 | Read、已连接的浏览器 MCP | 本地图片查看工具、已连接的浏览器 / computer-use；不把写在配置里的 MCP 当成已连接 |
| 技能参数 / 后台任务 | $ARGUMENTS / run_in_background | 从用户消息解析参数；用实际 shell 会话 / 后台任务机制，记录自己启动的 PID |

**提问契约**：由主代理向用户提问，优先支持选项的工具。按本环境的题数、选项数、异步和模式限制分批。异步调用返回不代表已回答；答案到达前可做独立工作，依赖答案的步骤等待。已有答案和授权继续有效。默认选项、超时、自主模式都不等于人工审批；必须的剪辑审批或人点生成仍保留。没有提问工具时用对话问，不能伪造用户选择。AUTONOMOUS 不提问，记录判断依据；无法满足人工审批的环节保持待人工。

**协调契约**：主代理读 playbook + refs、分工、综合。并行仅用于独立工作，不并发写同一文件；以当前环境许可和限额为准。普通研究 / 验证在子代理缺失时可由主代理执行，审计记 `execution_mode: parent-direct`，不伪造 spawn。fresh-context 观众 / 审稿检查是例外：需要没有作者上下文的独立审稿人；支持隔离时使用隔离，否则交独立会话或人工，记录 `未审`，不得盖独立审稿通过章。子代理只收到所需材料及最小共用工具约定，不能给「只看屏幕」审稿人额外剧本或作者解释。

**worker 产物与审计**：真实委派写 canonical artifact 和 `.audit/adhoc_agents/{date}/{task_id}/spawns/{worker_id}/{prompt.md,output.md}`。若运行时不提供子代理文件写入，主代理可保存实际发出的 prompt 和原样收到的结果，并记录写入者；不得补造不存在的调用。

审稿证据须在worker最终完成或明确确认文件冻结后取SHA并提交；进度消息不代替冻结回执。冻结后需纠正来源措辞或结论时保留原版、另建修订证据，先核实际输入是否改变再重绑指纹；已经发生的付费任务不因文档修订盲目重提。来源：shengji_zhilu follow-up106 round05审稿来源措辞在提交后修订。

Both the canonical artifact and the audit `output.md` MUST begin with a YAML frontmatter envelope so the parent's synthesis is machine-checkable:
   ```yaml
   ---
   worker_id: researcher-03-prior-art
   stage: 3
   role: researcher | level-specialist | validator
   angle: prior-art               # researcher only
   level: security                # level-specialist / validator only
   work_unit_id: backend_api      # validator only
   status: complete | partial | deferred_tool_unavailable | halted
   blockers: []                   # list of strings; empty if none
   confidence: high | medium | low
   ---
   ```
   Required fields: `worker_id`, `stage`, `role`, `status`. The remaining fields are role-conditional per the comments above. The parent rejects worker outputs missing the envelope (or with unknown `status`) and re-spawns once before halting with `pipeline.halted`.

主代理直接综合 qa.md / dossier.md / strategy.md，并在各协调阶段首事件记录 `pre_reading_consulted`。单代理执行也记录已读文件及执行方式。

**能力缺失**：明确记录缺少什么、受影响范围及可继续部分。研究工具缺失不凭训练记忆冒充已查证，不编引用；必要 QC / 独立审稿缺失标 blocker / 未审，不能宣称通过。工具调用名不同不是能力缺失。

**hooks 与收尾**：`.claude/settings.json` 的 UserPromptSubmit / Stop 只约束 Claude 自动执行，不假定其他运行时自动加载该配置；`.mcp.json` 也不是 Codex 工具已连接的证明。两端都遵守 prompt triage。改 shot / 引用资产后对受影响镜逐个执行 `seedance_kit.py sync <路径>` + `check <路径>`，核对输出与退出码；`sync` 回读资料包后仍未对齐或构建失败时返回 1。改现行规范后执行 `check_canon.py`；Codex 显式做，Claude hook 补兜底。全仓 `sync --all --quiet` 只在确需全仓对齐时用；不因一次局部改动悄悄改其他剧的派生包。

**优先级**：本节解释现有 skill 的工具术语；现行规范优先于历史文档。`ai_video_history.md` / `ai_video_harness.md` 是沿革证据，不从中恢复已废止的工具硬绑定。

## 用户报问题：查同类与流程原因，按授权修复

用户指出某个产物有问题（一个 shot、一张图、一段代码）时，在本次范围内查同类和流程原因：
1. 上升一层：流程里哪一环本该拦住它、为什么没拦住、同类还会在哪里出现——按本次任务范围机检同类，给出规模；全剧扫描只在该剧确实受影响时执行。
2. 说明发现与流程改进（能量化的落成闸门，见 AI 短剧 pipeline 机制 ③）。明显错误直接修；已有修复 / 改流程授权不重复请示。扩大创作方向或制作范围时才确认必要选择。
3. 按依赖顺序改闸门 / 生成器 / skill / refs 与受影响产物，复验并记来源；一次 review 不自动重生旧剧。

来源：2026-10-02 用户要求共用规范 review，并明确「过程中看到明显错误的地方顺手改」。

AUTONOMOUS 模式下不能问：按 best judgment 改，proposal 与理由记进 changelog。

## Deletions need no approval (2026-09-18)

删除产物（图 / 白模 / blend / 中间文件 / 整个目录）**不必请示**，看准了就删、接着往下跑。
理由：本仓库的产物都是**可重新生成的**——图由卡生成、白模由图生成、blend 由脚本生成，
而卡 / 清单 / 脚本本身在 git 里。停下来问一句的代价（一轮往返、流水线空转）远大于删错的代价。
这条**不覆盖**对 git 跟踪源文件的破坏性操作（`git reset --hard` / 强推 / 删脚本与清单），那些照旧谨慎。

## Iteration bounds

用户明确授权某范围“自主修复/重生成直到通过、不要中途询问”时，将范围、付费授权、默认轮次/时间界限覆盖及退出条件写入该任务follow-up后执行；授权不扩大到其他剧或任务。每轮保留新证据、归因、输入修正与实际费用，重复原因改变方案而非原样盲重试。必需独立QC/产物指纹、请求前日志、结果未知不重提继续有效；不能降低标准结束循环。没有这种明确授权时遵下列默认界限。

- Default 3 revision rounds per work unit before halting.
- Cap interview iterations at 3 rounds total.
- Circuit-break + emit `pipeline.halted` if the same issue repeats across two iterations OR wall-clock exceeds 30 minutes on a single unit.
- After halt, escalate to the user. Never silently retry past the bound.

## Task ID convention

`task_id = "{task_name}-{YYYYMMDD-HHmmss}"`, built once at run start. Use for `.audit/adhoc_agents/{date}/{task_id}/`.

For `task_type=ai_video`, `task_name` is pinyin or English even when the project's natural identifier is a Chinese title (per `.agents/references/project/ai_video.md` rule 1). The Chinese title is captured in `ai_videos/{name}/README.md`, not in the path.

## General coding rules

- **能用 100 字说清的不写 200 字。** 文档、卡片、库条目、chat 回复一律写完再删一遍：
  删重复、删铺垫、删「值得注意的是」这类空转。**表格优于排比句，一行示例优于一段解释。**
  例外只有两处：有明确下限的产物（锚点 prompt ≥1500 字）、以及 prompt 里为锁死模型行为
  而必要的冗余——那里的密度靠去重得到，不靠少写。
- Default to writing no comments. Only when the *why* is non-obvious.
- Don't add features, abstractions, or backwards-compat shims the task didn't ask for.
- Don't add error handling for cases that cannot happen. Validate at system boundaries (user input, external APIs); trust internal calls.
- Prefer editing existing files over creating new ones. Never create `*.md` documentation files unless explicitly requested.
- Strong typing + OOP rules above apply to all Python under `projects/` and `tools/`.
- **一个名字只有一处定义。** 配置键、枚举值、路径片段、阈值名——凡是「写的一处」与「读的一处」
  分别落在两个文件里的，必须有一方引用另一方，不许各写各的字面量。**漂了不会报错，只会静默失效**：
  实测 schema 白名单写 `平滑`、reader 读 `g.get("平顺", 1.0)`，于是配置里调的阈值一律不生效、
  默认值悄悄接管，而校验、日志、报错全都正常——排查掉整整一轮。写校验时顺手加一条：
  **配置里出现了 schema 允许、但代码从未读取的键，应当报错而不是忽略**。
- **改一个全局常数时，手写的副本不会跟着改——要在「读进来的那一刻」判掉。** 上一条讲名字，
  这一条讲**数值**：派生量（由常数算出来的坐标、尺寸、时长）会自动跟上，而**配置里手写死的
  同类数值不会**，且两者混在同一份文件里看不出区别。实测：整城坐标统一缩放 0.5 之后，
  `["Place", …]` 这类派生坐标自动缩了，某个镜头配置里手写的 `["世界", x, y, …]` 没缩，
  于是一条 200 m 的航线被算成 2277 m、时速 114 m/s——而下游闸门只报得出「侧向加速度超标」
  这个症状，完全指不到病根。做法：**给手写值加一条「它该落在什么范围内」的入口校验**
  （坐标要落在场景包围盒内、时长要落在合法区间、比例要落在枚举里），在解析配置时就 raise，
  并在报错里直接写出怀疑对象（「多半是缩尺前的值，xy 折半即可」）。症状级的闸门不能替代入口校验。

- **长任务必须可中断可续跑，且不许用「按进程名杀」收尾。** 渲染、批量生成、大规模抓取一律
  **逐单元落盘 + 跳过已完成 + 最后合并**（例：逐帧 PNG → ffmpeg 合片），而不是让一个进程写一个大产物——
  后者被打断就是零产出，实测拿到过两次 `moov atom not found` 的废文件。
  与此配套的是**禁止 blanket kill**（`Stop-Process -Name blender` / `pkill -f python` 这类按名字全杀）：
  同一台机器上常常有别的 session 在跑自己的任务，按名字杀会连别人的一起杀掉，
  而且**杀 shell 不杀它已经 spawn 出去的子进程**，留下多个进程写同一个文件。
  要停只停自己那一个 PID；判断「该不该再起一个」也按命令行匹配自己的那一条。
- **AI 视频生成时自检（不必提醒，收尾前必过；规则见 `ai_video.md`）**：
  ① 上传的 `## Seedance prompt` **≤2000 字**（rule 12.4-P，生成器 raise）；② 台词朗读一遍是**真人口语**，零公文腔 / 文言 / 翻译腔（白话大师 B1–B7）；
  ③ 逐镜问「这镜真有这个光源吗」「这个词是痕迹还是正在发生」（K32，`tools/prompt_light.py`）；
  ④ 镜内切镜写 `镜内状态:`，探入与位移拆先后（K33，`tools/shot_logic.py`）；
  ⑤ 改了剧情 / 台词：查相邻镜与集边界的连贯，跑 `ai_videos__审查总编排`；定稿某集或改开场结尾时通读全剧的开场、结尾与签名台词；
  剧情或走位不合理要改后续情节与走位，**删掉一句台词不算修好**。
- **脚本引号按实际 shell 处理**：含反斜杠或多行的补丁优先用补丁工具或临时脚本；PowerShell 不套 Bash heredoc，不把字符串插值当安全转义。递归删除前核对绝对路径在授权范围内，只处理可再生产物。
