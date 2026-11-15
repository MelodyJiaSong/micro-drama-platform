# AI 短剧制作平台

个人 AI 短剧制作仓库：多部短剧、共用资产库、制作 skills，以及 FastAPI + React 管理应用。Kimi 与 Codex 共用规范、制作流程、管理界面和审计；Claude 已停用，历史记录保留。

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
| `AGENTS.md` / `CONVENTIONS.md` | Kimi / Codex 共用入口与详细约定。 |
| `.agents/mcp.json` | 项目 MCP 唯一源；生成 `.kimi-code/mcp.json` 与 `.codex/config.toml`。 |
| `.agents/skills/` / `.agents/references/` | 唯一 skill 正文、playbooks 与参考规则，Kimi / Codex 直接读取。 |
| `.agents/agents/` / `.kimi-code/plugin/` | 自定义 Kimi agents 与可安装的 hooks 插件。 |
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

1. **From Kimi Code / Codex** — Kimi 软件任务使用 `/skill:agent-team`，短剧使用 `/skill:ai-videos-pipeline`；Codex 对应 `$agent-team` 与 `$ai-videos-pipeline`。自然语言指定流程也可以。主代理读相同 playbooks / refs，按当前环境的能力协调工作。
2. **From the browser** — run `spec_driven` (FastAPI backend + React frontend) and drive the same phases through a UI with a live event log. Same playbooks, same artifacts, same `specs/` persistence — different surface.

## 共用 skill 命令

在 Kimi 中把下列命令后接剧名和本次任务要求；未被系统命令占用时也可省略 `skill:` 前缀。

| 功能 | Kimi Code | Codex |
|---|---|---|
| 新建 / 继续短剧 | `/skill:ai-videos-pipeline` | `$ai-videos-pipeline` |
| 补人物资产 | `/skill:ai-videos-char-assets` | `$ai-videos-char-assets` |
| ChatGPT 订阅出图，无需 API key | `/skill:codex-imagegen` | `$codex-imagegen` |

软件流程使用 `/skill:agent-team`。也可以直接写「用 ai-videos-pipeline 继续 shengji_zhilu 第 1 集的影视改编」。源文件都在 `.agents/skills/`，无需生成入口或别名映射。调用格式见 [Kimi Agent Skills 文档](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html)。Codex 同样可执行完整流程；图片生成仍由 `tools/codex_image.py` 记录请求后调用。独立审稿保持现有 Kimi 单审规则。

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

从 [AGENTS.md](AGENTS.md) 开始，按任务读取 [CONVENTIONS.md](CONVENTIONS.md) 和对应 refs / skills。`.agents/skills/`、`.agents/agents/` 与 `.agents/references/` 是唯一维护位置；MCP 唯一源在 `.agents/mcp.json`，两端配置由 `python tools/sync_agent_config.py --fix` 生成，hooks 插件源在 `.kimi-code/plugin/`。

维护源 skill 的 name / description 后运行：

```powershell
python tools/check_agent_skills.py
python tools/check_agent_skills.py
```

正文直接维护在 `.agents/skills/`，Kimi / Codex 自动发现；自定义 agent 放在 `.agents/agents/`。修改 name、description、type 或新增 skill 后运行 `python tools/check_agent_skills.py`。改分镜、overhead 或参考资产后，显式运行 `python tools/shot_pack.py sync <集目录>`（只报告用 `check`）；工作流目录或共用源增删迁移后运行 `python tools/workflow_catalog.py --fix` 再 `--check`。两边都运行 `python tools/sync_agent_config.py --check` 核对配置。Kimi hooks 插件首次使用执行 `/plugins install .kimi-code/plugin` 并 `/reload`；未安装时也必须显式完成上述检查。

配置依据：[Kimi Agent Skills](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html)、[Agents](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/agents.html)、[MCP](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/mcp.html) 与 [Hooks](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/hooks.html) 官方文档。Prompt Lab 通过服务端环境变量 `PROMPT_LAB_RUNTIME=kimi|codex` 选择执行器，默认 Kimi；运行记录保存实际执行器，Codex 使用 `workspace-write`。

Codex 配置依据：[项目配置](https://learn.chatgpt.com/docs/config-file/config-basic)、[MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)、[共用 skills 发现](https://learn.chatgpt.com/docs/build-skills)。项目配置仅在受信任的项目中加载；重启会话后核对实际工具。仓库不改写用户级权限、凭据或信任设置。
