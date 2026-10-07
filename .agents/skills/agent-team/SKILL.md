---
name: agent-team
description: Spec-driven 软件新项目或完整阶段重跑：需求整理、访谈、研究、规格、验证、执行；持久化产物并支持续跑。短剧走 ai_videos__全流程编排；已有项目局部修复按共用 follow-up 流程。
---

> Claude / Codex 共用正文。执行前按根目录 `AGENTS.md` 路由，工具、提问、委派、参数与收尾遵 `CONVENTIONS.md` § Tool scoping and team coordination。路径相对仓库根；同目录资源相对本源文件。


# agent_team — spec-driven workflow

You drive a task through six stages, persisting every artifact so the user can resume at any stage. Coordinated stages (2, 3, 5, 6) use the parent-direct model — see `CONVENTIONS.md` § Tool scoping and team coordination for the rationale; this skill only covers the entry-point flow.

## Inputs (collect from the user if not given)

- `task_type` — this skill handles `development` only. Route `ai_video` to `ai_videos__全流程编排`; do not run the software stages for dramas.
- `task_name` — slug, no spaces (e.g., `spec_driven`).
- `raw_prompt` — what the user wants to build.

Build `task_id = "{task_name}-{YYYYMMDD-HHmmss}"` once at run start (see `CONVENTIONS.md` § Task ID convention).

## Resuming

If `specs/development/{task_name}/` already exists, honor the user's stage / scope. Otherwise resume at the first incomplete stage after reading artifacts and checks; ask only if the intended scope is ambiguous. File presence alone is not QC completion:

| Stage | Missing if … |
|---|---|
| 1 Intake | `user_input/revised_prompt.md` doesn't exist |
| 2 Interview | `interview/qa.md` doesn't exist |
| 3 Research | `findings/dossier.md` doesn't exist |
| 4 Spec | `final_specs/spec.md` doesn't exist |
| 5 Validation strategy | `validation/strategy.md` doesn't exist |
| 6 Execution | output project folder is empty or validation hasn't run end-to-end |

When resuming, read `changelog.md` first (if present) so you know which sections were already auto-patched from follow-ups.

## Follow-up prompts (between full runs)

Follow-up chat that arrives between runs is handled by `CONVENTIONS.md` § Follow-up prompt handling — those edits do NOT invoke this skill.

## Stage flow

For each coordinated stage, read its playbook AND its agent_refs files (per `CONVENTIONS.md` § Stage playbooks and reference docs — pre-reading contract). Record `pre_reading_consulted` on the stage's first `events.jsonl` event.

### Stage 1 — Intake

1. Save raw prompt to `specs/{task_type}/{task_name}/user_input/raw_prompt.md`.
2. Revise it: clean grammar, expand abbreviations, surface implicit constraints, structure into goal / context / desired outcome. **Don't invent requirements.** Save to `user_input/revised_prompt.md`.
3. Show to the user; iterate if they object.

### Stage 2 — Interview

Run `.agents/skills/agent-team/playbooks/interview.md`. Output: `interview/qa.md`. Interactive: resolve outstanding choices with the user; autonomous: annotate judgment calls and continue within the requested scope.

### Stage 3 — Research

Run `.agents/skills/agent-team/playbooks/research.md`. Output: `findings/dossier.md` + per-angle files.

### Stage 4 — Spec compilation

Read `revised_prompt.md` + `qa.md` + `dossier.md`. Produce `final_specs/spec.md` with these sections:

- **Goal** (one paragraph)
- **Out of scope** (explicit list)
- **User roles & primary flows**
- **Functional requirements** (numbered, each testable)
- **Non-functional requirements** (performance, security, deployment as relevant)
- **Acceptance criteria summary** (full criteria belong in stage 5)
- **Open questions** (if any survived)

Interactive: show to the user and resolve material disagreements. Autonomous: record assumptions and continue; it does not replace required external approvals.

### Stage 5 — Validation strategy

Run `.agents/skills/agent-team/playbooks/validation.md` (strategy mode). Output: `validation/strategy.md` + per-level files.

### Stage 6 — Execution + streaming validation

1. Decompose the spec into 3–8 work units (e.g., `backend_api`, `frontend_component`, `db_schema`).
2. Initialize `.audit/adhoc_agents/{YYYY-MM-DD}/{task_id}/events.jsonl`.
3. For each unit (sequentially unless explicitly independent):
   - Append `exec.unit.started`.
   - Implement into `projects/{task_name}/`.
   - Append `exec.unit.completed`.
   - Run `playbooks/validation.md` (runtime mode) against the unit.
   - On issues: revise, append `exec.revision.applied`, re-validate. Cap per `CONVENTIONS.md` § Iteration bounds.
4. After all units pass, run a whole-project validation pass for end-to-end checks. For development tasks, emit `validation.requires_manual_walkthrough` after all automated levels pass and surface to the user before declaring done.

## Audit and post-mortem

After the run (successful or halted), summarize for the user: stages run, workers spawned per stage, durations, surprises, recommendations.
