# CLAUDE.md — spec_coding monorepo

Hosts a **spec-driven workflow** and the platform that drives it. Every non-trivial task moves through six stages with artifacts persisted as plain files so any stage can be inspected, edited, or resumed.

## State surfaces (explicit determinism)

All workflow / `agent_team` state lives in one of these surfaces. No hidden caches, no other locations:

1. **`CLAUDE.md`** — rules and conventions (this file).
2. **`.claude/settings.json`** + **`settings.local.json`** — harness config, hooks, permissions, env.
3. **`specs/{task_type}/{task_name}/`** — per-task pipeline artifacts.
4. **`.audit/adhoc_agents/{YYYY-MM-DD}/{task_id}/`** — runtime spawn logs (`spawns/{worker_id}/{prompt.md, output.md}`), `events.jsonl`, per-round answer JSONs.
5. **Stage playbooks + refs** under `.claude/skills/agent_team/` and `.claude/agent_refs/` — see § Stage playbooks and reference docs.

Rules:

- **Pipeline status is derived from the filesystem, not from memory.** "Stage N done" iff Stage N's expected artifacts under `specs/{type}/{name}/` exist. Resume logic reads the tree.
- **New mechanisms must land in one of the surfaces above.** No sidecars, session-scoped stores, or side-channel caches.
- **Round-trip artifacts** between parent ↔ workers / user (e.g., `round1_answers.json`, aggregated worker outputs) live under `.audit/`, NOT in `specs/` (which is reserved for canonical user-facing output).
- **Code-navigation indexes are derived caches, not state surfaces.** The optional CodeGraph index at `projects/{name}/.codegraph/` (a symbol/call graph over that project's code, exposed to agents via the `codegraph` MCP server in `.mcp.json`, scoped to `projects/ai_video_management` for the current trial) is a **per-machine, gitignored, rebuildable cache** — a faster substitute for grep/glob fan-out, nothing more. It MUST NOT be treated as authoritative: pipeline status is still re-derived from the filesystem (rule 1 above), and it never indexes the markdown surfaces (`specs/`, `ai_videos/`, `.claude/`). Delete `.codegraph/` and re-run `codegraph index <project>` anytime; never read stale graph data as ground truth.

## Auto-memory is disabled

Do NOT use the auto-memory system. Do NOT read or write `.claude/memory/` or `~/.claude/projects/<slug>/memory/`. If session-start instructions mention `MEMORY.md`, treat its absence as canonical: there are no memories.

If you'd save a memory entry, persist to a state surface instead:
- Cross-conversation rules → `CLAUDE.md`.
- Per-project intent → `specs/{type}/{name}/`.
- Per-run audit → `.audit/adhoc_agents/{date}/{task_id}/`.
- Harness config → `.claude/settings*.json`.

The urge to save memory is a signal that one of the surfaces is missing the information. Put it there instead.

## Repo layout

```
spec_coding/
├── CLAUDE.md
├── pyproject.toml                         # canonical Python deps; `uv sync` reads this
├── requirements.txt                       # mirror for pip fallback
├── README.md
├── .claude/
│   ├── agent_refs/                        # institutional memory (see § Stage playbooks and reference docs)
│   │   ├── interview/{general.md, <task_type>.md}
│   │   ├── research/{general.md, <task_type>.md}
│   │   ├── validation/{general.md, <task_type>.md}
│   │   └── project/{general.md, <task_type>.md}
│   ├── skills/agent_team/
│   │   ├── SKILL.md                       # pipeline orchestrator (parent-direct)
│   │   └── playbooks/{interview,research,validation}.md
│   └── settings.local.json
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

Required at task start. Pick one; ask the user if unclear; never invent.

- `development` — software outputs land in `projects/{name}/`. Walks the **six-stage `agent_team`** workflow below.
- `ai_video` — AI 短剧 planning + prompt outputs land in `ai_videos/{name}/`. **Does NOT use agent_team.** Walks the dedicated **`ai_videos__全流程编排`** pipeline (脑洞→立项→世界观人设→分集大纲→文学剧本→分镜运镜→标准化分镜Prompt→整集 animatic→出片与后期). See § AI 短剧 pipeline below.

## The six-stage workflow (task_type=development)

The skill `agent_team` is the single entry point for **`development`** tasks and walks all six stages. Users invoke it as `/agent_team` or by asking for a spec-driven software task. **For `task_type=ai_video`, use `ai_videos__全流程编排` instead (§ AI 短剧 pipeline).**

| # | Stage | Output | Coordination |
|---|---|---|---|
| 1 | Intake | `user_input/{raw,revised}_prompt.md` | parent-direct, no workers |
| 2 | Interview | `interview/qa.md` | parent-direct, optional category workers |
| 3 | Research | `findings/{angle-*.md, dossier.md}` | parent-direct + parallel angle workers |
| 4 | Spec compilation | `final_specs/spec.md` | parent-direct, no workers |
| 5 | Validation strategy | `validation/{strategy.md, ...}` | parent-direct + parallel level-specialist workers |
| 6 | Execution + streaming validation | `projects/{name}/` or `ai_videos/{name}/` | parent-direct + parallel validators per work unit |

The procedural detail for each coordinated stage lives in `.claude/skills/agent_team/playbooks/{interview,research,validation}.md`. The parent-direct coordination model — and why there is no manager-subagent layer — is documented once in § Tool scoping and team coordination.

## AI 短剧 pipeline (task_type=ai_video)

`task_type=ai_video` 走专用的 **`ai_videos__全流程编排`** skill（不走 agent_team）。阶段 0–7（2026-09-28 起出片与后期纳入流程）：

| # | 阶段 | playbook | 产物落点 | QC 关卡 |
|---|---|---|---|---|
| 0 | 史料调研（**条件触发**：史料驱动项目——历史 / 纪实 / 复原类，concept 或系列圣经声明「史料驱动」；2026-09-13） | `ai_videos__stage0_史料调研` | `ai_videos/{name}/0_research/dossier.md` + 每个资产的 `refs.md`（`tools/ref_fetch.py`） | `ai_videos__格式契约` K34（dossier 15 节 + ≥ 20 条人工核过的 fact + 参考图库）；不齐不进阶段 1 |
| 1 | 核心创意立项 | `ai_videos__stage1_立项` | `ai_videos/{name}/1_立项/concept.md` | 人工确认 |
| 2 | 世界观+锁定人设 | `ai_videos__stage2_世界观人设` | `2_世界观人设/{world,characters,relationships,scenes,props,casting,style_guide}`（`characters/*` 每卡含 `## 人物灵魂`、`relationships.md`＝人物网，ai_video.md rule 12.11；`props/`＝重要复用物件卡，rule 4b） | `ai_videos__格式契约` |
| 3 | 分集大纲 | `ai_videos__stage3_大纲` | `3_大纲/arc_outline.md` | `ai_videos__剧情连贯`+`ai_videos__全剧序列` |
| 4 | 文学剧本(台词) | `ai_videos__stage4_剧本` | `4_剧本/episodes/epNN/{script,dialogue}.md` | `ai_videos__台词大师` |
| 5 | 分镜运镜 | `ai_videos__stage5_分镜` | `5_6_分镜与prompt/episodes/epNN/shots/shotNN/shotNN.md`(运镜设计) + 走动镜的 `shots/shotNN/planning/`(航线俯视图) | 站位朝向/运镜/动作表演/光线色调/时长节奏 |
| 6 | 标准化分镜 Prompt | `ai_videos__stage6_prompt` | 同 shotNN.md（设计稿 + `## Seedance prompt` 精简稿）+`all_shot_prompts.md` | `ai_videos__格式契约` + 出片前全 `ai_videos__审查总编排` |
| 6.5 | 整集 animatic 过审（rule 44） | stage6 §7 | `{ep}_animatic.mp4` + `viewing_animatic/review.md` | `ai_videos__整集观感`；`seedance_kit open` 闸门 |
| 7 | 出片与后期（rule 12.4-K / 42 / 43） | stage6 §9 | `shotNN.mp4` → `cut/edl.toml` → `{ep}_final.mp4` + 烧字幕版 + SRT → `viewing/review.md` → `audience_report.md` | `ai_videos__出片审片` → `ai_videos__cut`（代理片经用户批）→ `tools/post/finish_ep.py` → `ai_videos__整集观感` → `tools/audience.py` |

阶段 5、6 产物合一在 `shotNN.md`。项目用**阶段编号目录**（`1_立项/ … 5_6_分镜与prompt/`），新项目默认采用；已有项目（wushen_juexing）保留原结构、可选迁移。

**四大贯穿机制**（编排强制执行）：① **每步 QC**——每阶段强制过审（blocker 清零，严格度=严）才进下一步；② **每次 update 复核**——任何产物改动/重生默认跑受影响范围 `ai_videos__审查总编排` + 记 `specs/ai_video/{name}/changelog.md`；③ **反馈→进化**——用户每条实战反馈 surgical 更新对应 playbook/审查 skill/`agent_refs` + 记教训（带来源；单剧教训先进该剧 `lessons.md`，见 § AI video rules）；**能量化的反馈必须落成可机检闸门（左移进生成器、在 build 时 raise），而不是写成一条「记得注意」；闸门一律从最终产物回读，不校验生成它的中间变量**（2026-09-19）；④ **人物灵魂 + 人物网为创作前提**（2026-06-28，ai_video.md rule 12.11）——把每个具名角色当活生生的人写透（`## 人物灵魂` 12 维：年龄/前史/动机根因/目标/needs/desire/矛盾/恐惧/创伤+致伤事件/此刻决策逻辑/性格/成长轨迹）+ 建 `relationships.md` 人物网（社会/精神/情感关系 + 与当前主题关系）；这是 **ongoing** 的（人会成长，逐集深化校正）；凡剧情脑暴/写改大纲/写改台词/任何创新，都须在读透相关角色灵魂 + 人物网的前提下创作，并回看选择是否对得上、不对就改情节或补深人物。**交互默认 interactive**：每阶段先用多选题问用户、用答案细化再生成。**敏捷原则**（2026-06-18）：大方向先定、每集剧情边拍边改，不一次性出全剧剧情；阶段 1–3 只定大方向骨架 + 前几集细纲，后续各集留松、推进到该集再细化、随 feedback 临时调整、不绑死。**大胆增删整段 shot / 重排集结构**（2026-06-28）：目标是「做出一部好剧」，不拘泥于现有镜次/结构——加细节致单集超长就把溢出情节顺延下一集（守 concept 定的单集时长）、该补的铺垫/衬托/争抢/高潮就**新增整段 shot**、平淡或冗余的就**整段删**、需要就**拆集 / 并集 / 重排镜序**；过程中出现很多大改是正常的、不是失败。增删后照常跑「每次 update 复核」（受影响范围 `审查总编排` + changelog）。详见 `.claude/skills/ai_videos__全流程编排/{SKILL.md, BLUEPRINT.md}`。

## Skill + playbook naming

- Repo-owned skills use `<prefix>__<name>` (double underscore). The orchestrator skill `agent_team` is the exception (top-level workflow, no prefix).
- **AI 短剧 skills use the `ai_videos__` prefix + a Chinese name** (e.g. `ai_videos__台词大师`, `ai_videos__全流程编排`): ASCII prefix keeps them greppable, Chinese suffix keeps them readable (Chinese skill names register fine). This covers the pipeline orchestrator, its stage playbooks (`ai_videos__stageN_*`), and the review skills.
  - **Exception — skills the user triggers by typing `/`** get an all-ASCII name (`ai_videos__char_assets`) plus an `argument-hint` carrying a usage example: Chinese-named skills don't show in the `/` autocomplete (user-observed 2026-09-30).
- Stage playbooks live under `.claude/skills/agent_team/playbooks/`. They are NOT subagent definitions — they are runbooks the parent reads inline.
- `.claude/agents/` is reserved for future permanent subagents (currently empty; every spec-driven stage is parent-direct).
- Workers spawned at runtime are general-purpose subagents driven by playbook prompts, captured under `.audit/adhoc_agents/{date}/{task_id}/spawns/`.
- YAML frontmatter `description` field has a hard ceiling of **500 characters**.

## Stage playbooks and reference docs

Two folders sit alongside the workflow, with intentionally separate lifecycles:

- **Playbooks** at `.claude/skills/agent_team/playbooks/{interview,research,validation}.md` — the procedural runbook for each coordinated stage. The contract for *what the parent does*.
- **Refs** at `.claude/agent_refs/` — accumulated institutional memory. *What the parent has learned*. Two scopes:
  - **Stage-scoped:** `agent_refs/{interview,research,validation}/{general.md, <task_type>.md}` — what's been learned at each stage.
  - **Project-scoped:** `agent_refs/project/{general.md, <task_type>.md}` — cross-cutting rules about the *outputs* (e.g., light-theme app chrome for development webapps). NOT for project-specific facts (those go under `specs/`) and NOT for harness contracts (those stay in `CLAUDE.md`).

**Pre-reading contract.** Before each coordinated stage (2, 3, 5) and before each stage-6 work-unit `validation.started`, the parent MUST read:
1. The stage playbook.
2. `agent_refs/{stage}/general.md`.
3. `agent_refs/{stage}/<task_type>.md`, if present.
4. `agent_refs/project/general.md`.
5. `agent_refs/project/<task_type>.md`, if present (`ai_video`: the canon `ai_video.md` only — `ai_video_history.md` / `ai_video_harness.md` are history, grep on demand).

The parent records each file it actually read as `{path, sha256}` (SHA-256 of the file's bytes at read time) in a single `pre_reading_consulted` array on the run's first `events.jsonl` event for that stage (or on each `validation.started` event in stage 6). The hash turns the event into a reproducibility receipt — two runs can diff "did the playbook or a ref drift between us?" without git archaeology. A missing or empty array is a **critical failure** — institutional memory wasn't loaded.

**Precedence when rules conflict:** per-task-type ref > matching `general.md` in same folder; project-scoped ref > stage-scoped ref > playbook default. A project-specific spec under `specs/{type}/{name}/` may override project-scoped refs for that one project, with a note explaining the divergence.

**Update protocol.** Surgical only — one new principle / severity row / required move at a time, with a one-line citation of the source run / follow-up. Wholesale rewrites are anti-patterns; the goal is to grow institutional memory.

**Why three folders, not one:** different lifecycles. Playbooks change rarely; stage refs accumulate per stage; project refs accumulate per task-type. Folding them together would either balloon the playbook past readability or conflate stage-time-of-use with output-time-of-use.

The spec_driven webapp's `EXPOSED_TREE` recursive globs (`.claude/skills/agent_team/playbooks/*.md`, `.claude/agent_refs/**/*.md`) auto-pick up new subfolders.

## Project rules (under `projects/`)

- One folder per project; no cross-project imports.
- **Solution layout is mandatory** — `apps/{api,ui,…}/` for executables, `libs/{infrastructure,domain,application,common}/` for shared code, each layer sub-bucketed by role (`application/{queries,commands,dtos,mappers}`, `domain/{entities,value_objects,errors,repositories}`, `infrastructure/{readers,writers,clients,daos,middleware}`; `common/` stays flat). Within each role sub-folder, one file per aggregate: `{aggregate}__{role}.py`. For `commands/` + `queries/` the file holds EXACTLY ONE class (`{Aggregate}Command` / `{Aggregate}Query`) with one method per operation — e.g., `ActorCommand.generate(...)`, `.generate_diverse(...)`, `.delete(...)`. For `dtos/` the file holds both Qdtos and Cdtos for that aggregate (the suffix on the class name disambiguates). Routes follow the same pattern: `apps/api/routes/{aggregate}__route.py`, each with its own `APIRouter()`; `routes/__init__.py` combines them into a single `router` that `app_factory.py` mounts. Authoritative spec: `.claude/agent_refs/project/development.md` §1. The old `backend/` + `frontend/` shape is retired.
- **Routes / job entries / CLIs do NOT import infrastructure directly.** Every endpoint maps to exactly one application-layer Query or Command method. Empty `libs/application/` while `apps/*` has executables is a stage-5 `blocker` — see `agent_refs/project/development.md` §6b and `agent_refs/validation/development.md` §11b.
- **Commands go through `libs/domain/`** (entities + value objects + repository protocols). Read-side queries may skip the domain layer per development.md §3 carve-out; state changes may not.
- **Single Responsibility Principle** — one concern per file. Exception classes don't live in writer/reader files (extract to `libs/infrastructure/errors/{aggregate}__error.py`); DAO dataclasses go in `libs/infrastructure/daos/{aggregate}__dao.py`; DTOs go in `libs/application/dtos/{aggregate}__dto.py`; Pydantic request bodies stay with the route handler. See `agent_refs/project/development.md` §1.
- **File size guideline** — prefer `< 100 lines`, split by sub-concern (mirroring the layer's role taxonomy) when bigger. Hard cap is around `~1000` lines with no clear sub-concern boundary (stage-5 `warning`). See `agent_refs/project/development.md` §1.
- Python: own `requirements.txt` (direct deps only); mirrored into root `pyproject.toml`; root `requirements.txt` is the pip fallback. `apps/*` Python uses `dependency_injector` per development.md §5.
- Strong typing on every parameter, return, and attribute. Use `str | None`, not `Optional[str]`. `@dataclass(frozen=True)` for value objects and DTOs; mutable `@dataclass` only for entities with invariant-guarded mutation methods.
- Frontend (`apps/ui/`): standard React; `node_modules/` in `.gitignore`. DDD layering does NOT apply to UI code.
- README required and updated alongside any feature change.
- **Cross-cutting project-output rules** (themes, visual defaults, structural conventions, DDD+CQRS layering details) live in `.claude/agent_refs/project/` per § Stage playbooks and reference docs — NOT in this section.

## AI video rules (under `ai_videos/`)

规则全在 **`.claude/agent_refs/project/ai_video.md`（现行规范，≤ 60 KB，ai_video 任务开工唯一必读）**：每条一行 + 机检指针。
来历、事故、已废止条款在 `ai_video_history.md`（2026-09-28 拆分前全文）与 `ai_video_harness.md`，按 rule 号 grep、不通读。本节只留会话层面的硬约束：

- **新规则怎么进**：单剧教训先写 `specs/ai_video/{name}/lessons.md`；第二部剧复现或用户明说全局，才在 `ai_video.md` 加一行（≤ 2 行 + 机检指针），来历写进 `ai_video_history.md` 文末「沿革」。能量化的写成闸门。`tools/check_canon.py`（Stop hook）查体量。
- **规则变更不回溯旧剧**：新规则只管新产物与这次改到的镜；旧镜 / 旧集走显式遗留清单（只减不增，如 `seedance.toml` 的 `legacy_eps`）。
- **出片**：第一镜出片前整集 animatic 必须过审（rule 44，`seedance_kit open` 闸门）；「生成」永远人点；上传的是 `## Seedance prompt` 精简稿（rule 12.4-P，≤ 2000 字）；**改了 shot prompt，回复里必须告诉用户改了哪几镜、资料包是否全部一致**（rule 12.4-K）。
- **音频**：每剧 `seedance.toml` 声明 `audio_mode`（native / tts_first，rule 12.4-H2）；Seedance 不出音乐，BGM、字幕、响度在后期 `tools/post/finish_ep.py`（rule 42）。
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
   - Workflow contracts, state surfaces, cross-cutting conventions → `CLAUDE.md`.
   - Stage-procedure changes → `.claude/skills/agent_team/SKILL.md` or `.claude/skills/agent_team/playbooks/{interview,research,validation}.md`.
   - Accumulated institutional memory (stage-scoped or output-scoped) → `.claude/agent_refs/{interview,research,validation,project}/{general.md,<task_type>.md}` per § Stage playbooks and reference docs.
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

The `spec_driven` webapp emits **copy-paste regeneration prompts** the user pastes into Claude Code CLI to re-run one or more stages. Every such prompt opens with one of two execution-mode headers — Claude MUST honor them at the top of a turn's input.

**Header contract:**

- **`# EXECUTION MODE: AUTONOMOUS`** —
  - Do NOT call `AskUserQuestion`. Not for clarification, not for "A or B," not for confirmation. The user is not at the keyboard.
  - For ambiguity, use best judgment AND record it inline in the produced artifact (e.g., `*(judgment call — chose X because Y)*`) so the user has a self-explaining trail.
  - Produce every requested artifact in the same turn before stopping; do not pause for confirmation between stages. Iteration bounds (§ below) still apply — when a bound trips, halt cleanly with a `pipeline.halted` event + summary.
  - Every other rule still applies (state surfaces, agent-spawning contract, follow-up procedure for new instructions arriving mid-run). Autonomous lifts only the question-asking restriction.
- **`# EXECUTION MODE: INTERACTIVE`** — default. `AskUserQuestion` available when intent is genuinely ambiguous and not inferrable from existing artifacts.
- **No header** = INTERACTIVE.

**What the webapp generates.** `POST /api/regen-prompt` (FR-14c) inlines the project's current `revised_prompt.md` (or `raw_prompt.md` if no revised yet) plus every `user_input/follow_ups/*.md`. A pasted regen prompt is therefore self-contained.

**Defaults.** The webapp's autonomous-mode toggle defaults to **off** (interactive); accidental autonomous runs should not be the path of least resistance. The toggle persists in browser `localStorage` under `spec_driven.autonomous_mode.v1` (no server-side persistence — autonomous is per-prompt, not global).

### Regeneration semantics: read-zero from prior outputs

A regeneration deletes the regenerated stage's prior outputs and rewrites from scratch. Surgical preservation of prior text is **forbidden** during regen — it makes the output a function of (input ∧ all previous runs) and defeats the workflow.

The regenerated stage reads ONLY:
1. The current stage's *input* artifacts (canonical outputs of prior stages).
2. `CLAUDE.md` and shared `.claude/` context (skill, playbooks, refs).
3. The user-input layer (`raw_prompt.md` + every `user_input/follow_ups/*.md`).
4. The current stage's `<stage>/promoted.md` sidecar, if present (see § Pinned items).

Per-stage delete-then-regenerate contract:

| Stage | Delete first | Preserve | Inputs |
|---|---|---|---|
| 1 — Intake | (none — `revised_prompt.md` rewritten in place from raw + follow-ups) | n/a | `user_input/raw_prompt.md`, `user_input/follow_ups/*.md` |
| 2 — Interview | `interview/qa.md` | `interview/promoted.md` | `user_input/revised_prompt.md`, `interview/promoted.md`, `CLAUDE.md`, `.claude/skills/agent_team/{SKILL.md, playbooks/interview.md}`, `.claude/agent_refs/{interview,project}/*.md` |
| 3 — Research | `findings/*` except `promoted.md` | `findings/promoted.md` | `revised_prompt.md`, `interview/qa.md`, `findings/promoted.md`, `CLAUDE.md`, `.claude/skills/agent_team/{SKILL.md, playbooks/research.md}`, `.claude/agent_refs/{research,project}/*.md` |
| 4 — Spec | `final_specs/spec.md` | `final_specs/promoted.md` | `revised_prompt.md`, `interview/qa.md`, `findings/dossier.md` (+ angles if useful), `final_specs/promoted.md` |
| 5 — Validation | every file under `validation/` except `promoted.md` | `validation/promoted.md` | `final_specs/spec.md`, `validation/promoted.md`, `CLAUDE.md`, `.claude/skills/agent_team/{SKILL.md, playbooks/validation.md}`, `.claude/agent_refs/{validation,project}/*.md` |
| 6 — Execution | the entire `projects/{name}/` or `ai_videos/{name}/` folder | (no v1 promoted.md in stage 6) | `final_specs/spec.md`, every file under `validation/`, `CLAUDE.md`, `.claude/agent_refs/project/*.md` |

Operational notes:

- Delete is real `rm -rf`-equivalent, not logical "treat as missing." Stale bytes are how surgical-edit regen creeps back in. `<stage>/promoted.md` stays in Preserve, never Delete.
- **Multi-stage regen is sequential.** Delete each stage's outputs the moment that stage runs (after inputs are confirmed), not all up-front; otherwise stage N+1 is missing its inputs.
- **Selective module regen.** If the prompt selects only some stage modules (e.g., only `validation/security.md` + `performance.md`), delete only those files. Default copy-paste prompts select all.
- **`changelog.md` and `.audit/` are NEVER regen outputs.** They are the audit log; they get appended to with a record of what was deleted/regenerated.
- **Project README and Makefile** under `projects/{name}/` are stage-6 outputs and ARE deleted with the rest of the folder.
- **AI-video novels accept a per-episode regen scope.** When `task_type=ai_video, sub_type=novel`, a regen prompt may declare `scope=episode N` (or `scope=episodes M..N`); the parent then deletes only `ai_videos/{name}/episodes/ep{NN}/` for the named range, preserving `characters/`, `world.md`, `style_guide.md`, `arc_outline.md`, and other episodes' folders. Default remains `scope=project` (whole-folder delete per the table). Shorts have only the project-level scope.
- **The `agent_team` skill, playbooks, and agent_refs** are NOT regen outputs — they are harness context. Never deleted by a project-scoped regen.

Audit-event contract for any regen: emit `regen.delete.planned` (one line per file before delete), `regen.delete.completed` (with count), `regen.write.completed` (path + size after write) into `events.jsonl`. The webapp's `regen_prompt.py` includes this contract verbatim in every assembled prompt's `### Constraints` section.

### Pinned items survive regeneration

Each spec-pipeline stage (interview, findings, final_specs, validation) supports a `<stage>/promoted.md` sidecar. The user pins atomic items via the spec_driven webapp (`POST /api/promote`); they're written to `promoted.md` and deleted via `DELETE /api/promote`.

1. **`<stage>/promoted.md` is an INPUT, not an output.** Preserved across regen (Files-to-preserve column above).
2. **Every pin appears verbatim in the regenerated artifact** at the natural insertion point for its source-file/id metadata. Newly-generated content for a pinned slot is dropped — promoted always wins.
3. **Orphaned pins** (insertion point gone) go to a `## Pinned items (orphaned)` section at the end of the originally-pinned source file. NEVER silently dropped.
4. **Editing a pin updates `promoted.md` only.** The generated artifact is touched at the next regen. Drift between editions is acceptable; users resolve it by running stage N regen.
5. **`<stage>/promoted.md` is itself viewable / editable** through the webapp via the same path-sandbox. It is NOT a regen target.
6. **Stage 6 (project code) has no v1 promotion** — different granularity story, deferred.

## Tool scoping and team coordination

Some tools are **deferred** — schemas not loaded at session start; calling them directly fails with `InputValidationError`. They appear by name in the session-start system reminder. Load with `ToolSearch(query="select:<name>", max_results=1)` first.

**Empirically established scoping** (load-bearing for the parent-direct workflow):

- **`AskUserQuestion`** is **parent-only**. Subagents return "no matching deferred tools found" on ToolSearch. This is precisely why stage 2 is parent-direct — only the parent can prompt the user.
- **`WebSearch` / `WebFetch`** load at first-level subagent scope (verified 2026-05-02 in research workers) AND at parent scope. The parent can run an angle directly when a worker's deferred-tool load fails (recovery path).
- **The `Agent` (subagent-spawn) tool is parent-only.** Subagents cannot spawn nested subagents. This drives the parent-direct model: only the parent fans out workers in parallel.

**Coordination model (parent-direct):**

1. **The parent IS the manager** at every coordinated stage (2, 3, 5, 6). It reads playbook + refs, decides team composition, spawns workers, synthesizes outputs. There is no manager-subagent layer in between.
2. **Workers spawn in parallel** — single message, multiple `Agent` tool calls. Canonical way to maximize parallelism on this harness.
3. **Workers write their own outputs and audit files.** Each worker writes its artifact to the canonical `specs/{type}/{name}/` location AND its spawn audit (`prompt.md` + `output.md`) under `.audit/adhoc_agents/{date}/{task_id}/spawns/{worker_id}/`. No fabricated spawn folders.

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
4. **The parent does synthesis directly** after workers finish — `qa.md`, `dossier.md`, `strategy.md` are parent-written.

**Universal rules:**

- **No silent fallbacks.** If a tool fails to load, halt with a structured failure (`{status, missing, partial_results_if_any}`). Never paraphrase from training data, never invent citations, never dump multi-choice questions inline as plaintext, never fabricate worker outputs.
- **Plaintext-fallback for `AskUserQuestion` is forbidden** — the multi-choice UX is a hard contract.
- **The parent records `pre_reading_consulted`** on the run's first event for each coordinated stage. Missing array = critical failure.
- **New scoping findings update this section** before proceeding.

## 用户报问题：先提流程改进，同意后再修（2026-09-27）

用户指出某个产物有问题（一个 shot、一张图、一段代码）时，**第一步不是修它**：
1. 上升一层：流程里哪一环本该拦住它、为什么没拦住、同类还会在哪里出现——先用机检把全剧同类扫一遍，给出规模。
2. 把流程改进的 proposal 告诉用户（能量化的落成闸门，见 AI 短剧 pipeline 机制 ③），**等用户同意**。
3. 同意后先改流程（闸门 / 生成器 / skill / refs），再用新流程修这一处和扫出来的同类。

AUTONOMOUS 模式下不能问：按 best judgment 改，proposal 与理由记进 changelog。

## Deletions need no approval (2026-09-18)

删除产物（图 / 白模 / blend / 中间文件 / 整个目录）**不必请示**，看准了就删、接着往下跑。
理由：本仓库的产物都是**可重新生成的**——图由卡生成、白模由图生成、blend 由脚本生成，
而卡 / 清单 / 脚本本身在 git 里。停下来问一句的代价（一轮往返、流水线空转）远大于删错的代价。
这条**不覆盖**对 git 跟踪源文件的破坏性操作（`git reset --hard` / 强推 / 删脚本与清单），那些照旧谨慎。

## Iteration bounds

- Default 3 revision rounds per work unit before halting.
- Cap interview iterations at 3 rounds total.
- Circuit-break + emit `pipeline.halted` if the same issue repeats across two iterations OR wall-clock exceeds 30 minutes on a single unit.
- After halt, escalate to the user. Never silently retry past the bound.

## Task ID convention

`task_id = "{task_name}-{YYYYMMDD-HHmmss}"`, built once at run start. Use for `.audit/adhoc_agents/{date}/{task_id}/`.

For `task_type=ai_video`, `task_name` is pinyin or English even when the project's natural identifier is a Chinese title (per `agent_refs/project/ai_video.md` rule 1). The Chinese title is captured in `ai_videos/{name}/README.md`, not in the path.

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
- **Bash 工具的 heredoc 会吞反斜杠**（`\n` 变成真换行、`\b` 变成退格）：含反斜杠的 Python 补丁先写成文件再跑。
