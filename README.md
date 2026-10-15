# AI 短剧制作平台

个人 AI 短剧制作仓库：多部短剧、共用资产库、制作 skills，以及 FastAPI + React 管理应用。Claude 与 Codex 共用规范和流程正文。

短剧创作走六个模块：故事创作 → 影视改编 → Prompt 编译与出片 → 剪辑 → 声音与音乐 → 成片交付（后三个待设计）。Research 与人物、场景等资产独立支持；先在魔兽世界 EP1 开始小型 POC。旧流程已于 2026-10-11 删除，旧剧目录只作数据保留（根目录有 `OBSOLETE.md`）。下面的软件六阶段流程仅用于 spec-driven 开发任务。

```
┌─── Six-stage spec-driven pipeline ─────────────────────────────────────┐
│  1 Intake              raw prompt → revised_prompt.md                  │
│  2 Interview           multi-choice Q&A → interview/qa.md              │
│  3 Research            parallel researcher fan-out → findings/         │
│  4 Spec compilation    revised + qa + dossier → final_specs/spec.md    │
│  5 Validation strategy parallel level-specialists → validation/        │
│  6 Execute ⇄ validate  per-unit code + parallel validators (events)    │
│                        outputs → projects/{name}/                     │
└────────────────────────────────────────────────────────────────────────┘
```

## Repo layout

| Path                                       | What lives there |
|--------------------------------------------|------------------|
| `AGENTS.md` / `CONVENTIONS.md`              | Claude / Codex 共用入口与详细约定。 |
| `CLAUDE.md`                                | Claude 入口，导入 `AGENTS.md`。 |
| `.agents/skills/` / `.agents/references/` | 两端共用的唯一 skill 正文、playbooks 与参考规则；Codex 直接读取。 |
| `.agents/skill-aliases.json` / `.claude/skills/` | 共用名称到旧 Claude 名称的映射，以及自动生成的 Claude 引用入口。 |
| `pyproject.toml`                           | Canonical Python deps. `uv sync` reads this. |
| `requirements.txt`                         | Mirror of the above, kept for the pip fallback path. |
| `.agents/skills/agent-team/SKILL.md`       | The pipeline-orchestrator skill. |
| `.agents/skills/agent-team/playbooks/*.md` | Stage playbooks (interview, research, validation) the parent reads inline. |
| `.agents/references/{interview,research,validation}/*.md` | Accumulated institutional memory per stage. |
| `specs/`                                   | Persistence layer for the spec-driven workflow (`user_input/`, `interview/`, `findings/`, `final_specs/`, `validation/`). |
| `projects/`                                | All projects, including the platform itself. User code outputs land here. |
| `projects/spec_driven/`                    | The FastAPI + React platform that drives the pipeline. Run backend + frontend in two terminals. |
| `ai_videos/`                               | User AI-video task outputs. |
| `.audit/adhoc_agents/`                     | Local-only audit trail for worker subagents and stage events (gitignored). |
| `.venv/`                                   | Local Python virtualenv (gitignored). |

## Two ways to drive the pipeline

1. **From Claude Code or Codex** — 软件任务使用 Claude `/agent-team` 或 Codex `$agent-team`；短剧使用 Claude `/ai-videos-pipeline` 或 Codex `$ai-videos-pipeline`。自然语言指定流程也可以。主代理读相同 playbooks / refs，按当前环境的能力协调工作。
2. **From the browser** — run `spec_driven` (FastAPI backend + React frontend) and drive the same phases through a UI with a live event log. Same playbooks, same artifacts, same `specs/` persistence — different surface.

## 共用 skill 命令

4 个 skills 共用同一组名称，调用符号按客户端使用 `/` 或 `$`。例如把下表命令后接 `shengji_zhilu` 和本次任务要求：

| 功能 | Claude Code | Codex |
|---|---|---|
| 新建 / 继续短剧 | `/ai-videos-pipeline` | `$ai-videos-pipeline` |
| 补人物资产 | `/ai-videos-char-assets` | `$ai-videos-char-assets` |
| ChatGPT 订阅出图，无需 API key | `/codex-imagegen` | `$codex-imagegen` |

另一个是软件流程的 `agent-team`（见上节）。也可以两端都写「用 ai-videos-pipeline 继续 shengji_zhilu 第 1 集的影视改编」。原 Claude `/ai_videos__…` 命令保留。完整名称见 [.agents/skill-aliases.json](.agents/skill-aliases.json)。Claude 的 [skills 文档](https://code.claude.com/docs/en/skills) 与 Codex 的 [本地 skills 文档](https://learn.chatgpt.com/docs/build-skills) 分别说明调用方式。

## Quick start

### Windows: micro-drama management

From the repository root, use the project virtual environment (no activation or
`make` required):

```powershell
.\start.ps1
```

Each run first stops the previous backend / frontend (processes it started
plus whatever listens on 8766 / 5174), then starts both in the background with
logs in `projects/ai_video_management/logs/`. Open `http://127.0.0.1:5174/`
(Vite dev server) or `http://127.0.0.1:8766/` (built bundle). Options:
`-NoReload` (no uvicorn auto-reload), `-BackendOnly`, `-Stop` (stop only).
The launcher checks the project `.venv` first,
then the root `.venv`, and skips environments whose Python executable no longer
works. If neither works, create a project environment with an installed Python
and install `projects/ai_video_management/requirements.txt` into it.
If port 8766 is held by another program, run `./start.ps1 -Port 8767`; the
frontend proxy follows the same port.
Build the UI first if `apps/api/static/index.html` is missing:

```powershell
cd projects/ai_video_management/apps/ui
npm install
npm run build
```

### Spec-driven workflow platform

Two terminals.

```bash
# one-time install (from repo root)
uv sync                                                       # install Python deps
( cd projects/spec_driven/apps/ui && npm install )

# terminal 1 — backend (FastAPI on http://127.0.0.1:8765)
cd projects/spec_driven && python -m apps.api.main

# terminal 2 — frontend (Vite dev on http://127.0.0.1:5173)
cd projects/spec_driven/apps/ui && npm run dev
```

Open the UI at `http://127.0.0.1:5173`. Vite proxies `/api` → `http://127.0.0.1:8765`.

If you don't have `uv` yet: install it from https://docs.astral.sh/uv/ — fastest. Or fall back to `python -m venv .venv && .venv/bin/pip install -r requirements.txt`.

### Configurable env vars

Override before running either entry. CLI flags on `npm run ui` (e.g. `-- --port 3000`) also work.

| Var               | Default                                | Used by              |
|-------------------|----------------------------------------|----------------------|
| `BACKEND_HOST`    | `127.0.0.1`                            | backend              |
| `BACKEND_PORT`    | `8000`                                 | backend, vite proxy  |
| `BACKEND_RELOAD`  | empty (false)                          | backend (dev reload) |
| `BACKEND_URL`     | `http://$BACKEND_HOST:$BACKEND_PORT`   | vite proxy override  |
| `FRONTEND_HOST`   | `127.0.0.1`                            | vite                 |
| `FRONTEND_PORT`   | `5173`                                 | vite                 |

### Production build (optional sanity check)

```bash
python -m compileall projects/spec_driven/apps projects/spec_driven/libs
( cd projects/spec_driven/apps/ui && npm run build )
```

## What's a "task" and how does it produce output

A new spec-driven **development** task is one trip through the six-stage pipeline. Give it a `task_name` and raw prompt; the parent coordinates applicable work. AI dramas use their dedicated pipeline above; existing-project fixes remain scoped follow-up edits.

| # | Stage                          | Parent reads                                                                                              | Workers it spawns                                                       | Output |
|---|--------------------------------|-----------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|--------|
| 1 | Intake                         | (raw prompt)                                                                                              | none                                                                    | `user_input/{raw_prompt.md, revised_prompt.md}` |
| 2 | Interview                      | `playbooks/interview.md` + `.agents/references/interview/*.md`                                                    | optional category workers (parallel) when categories diverge            | `interview/qa.md` |
| 3 | Research                       | `playbooks/research.md` + `.agents/references/research/*.md`                                                      | one researcher per angle (3–6, all parallel)                            | `findings/{angle-*.md, dossier.md}` |
| 4 | Spec compilation               | revised_prompt + qa.md + dossier.md                                                                       | none                                                                    | `final_specs/spec.md` |
| 5 | Validation strategy            | `playbooks/validation.md` (strategy mode) + `.agents/references/validation/*.md`                                  | one level-specialist per validation level (all parallel)                | `validation/{strategy.md, acceptance_criteria.md, bdd_scenarios.md, system_tests.md, unit_tests.md, ...}` |
| 6 | Execution + streaming validation | `playbooks/validation.md` (runtime mode) + `.agents/references/validation/*.md`                                  | per work unit: applicable validators when available           | `projects/{name}/...` + `events.jsonl` |

Worker subagents are traced to `.audit/adhoc_agents/{date}/{task_id}/spawns/{worker_id}/{prompt.md, output.md}` — every dynamic spawn is replayable and inspectable. Stage-start events with `pre_reading_consulted` arrays land in `.audit/adhoc_agents/{date}/{task_id}/events.jsonl` alongside execution + validation events.

## Iteration bounds and circuit-breaker

- Default `max_iterations: 3` per work-unit.
- Halt + emit `pipeline.halted` when (a) the same issue id repeats across two iterations, (b) more than five issues stay open after iteration 2, or (c) wall-clock exceeds 30 minutes on a single unit.
- After halt, the SKILL escalates to the user. There are no silent retries past the cap.

## Conventions

从 [AGENTS.md](AGENTS.md) 开始，按任务读取 [CONVENTIONS.md](CONVENTIONS.md) 和对应 refs / skills。`.agents/skills/` 与 `.agents/references/` 是共用正文的唯一维护位置；`.claude/skills/` 只有指向它们的生成入口，settings / hooks / MCP 声明属于运行时适配。

维护源 skill 的 name / description 后运行：

```powershell
python tools/sync_agent_skills.py
python tools/sync_agent_skills.py --check
```

两端 ASCII 名称查 `.agents/skill-aliases.json`；3 份正文直接维护在 `.agents/skills/`。同步脚本只生成 Claude 的同名及旧名入口，均引用同一源文件，从不复制正文或回写源文件。修改流程正文即时共享；改名称、描述、`metadata.claude.argument-hint` 或新增 skill 后同步入口。Claude 入口传递 `$ARGUMENTS`，共用正文从实际消息读取参数。改分镜、overhead 或参考资产后，显式运行 `python tools/shot_pack.py sync <集目录>`（只报告用 `check`）；工作流目录或共用源增删迁移后运行 `python tools/workflow_catalog.py --fix` 再 `--check`；不能依赖 Claude Stop hook 在 Codex 中自动运行。新入口未被当前会话发现时可直接按路径读源 skill，或重新开启会话。

发现约定依据：[OpenAI AGENTS.md 文档](https://learn.chatgpt.com/docs/agent-configuration/agents-md)、[本地 skills 文档](https://learn.chatgpt.com/docs/build-skills)。本次共用适配保留现有应用运行后端；Prompt Lab 的自动执行器仍使用其配置的 Claude CLI。
