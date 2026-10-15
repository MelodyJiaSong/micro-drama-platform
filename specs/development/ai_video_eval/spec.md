# ai_video_eval — spec (v1)

Derived from `docs/interview.md` (52-question interview, 2026-07-28). This is the build contract; deviations require a note here.

## Goal

A **100% runtime-independent** eval system that grades the shot-prompt artifacts of `ai_videos/` dramas against a frozen, versioned rubric, using LLM judges (Anthropic API direct) for subjective fields and deterministic rule code for mechanical fields, then aggregates all field grades through a **non-LLM, fully deterministic** layer into verdicts + machine-consumable findings that a future revision agent can act on.

## Independence boundary

- Lives at `projects/ai_video_eval/`; reads `ai_videos/{project}/` artifacts directly.
- Never reads `.claude/`, `CLAUDE.md`, or repo settings at runtime. Config = `config/eval_config.yaml` + `.env` only.
- The rubric was **derived once** from the review skills/agent_refs (mined 2026-07-28 via 9 parallel distillation agents), then frozen: `rubric/rubric.yaml` + `rubric/dimensions/*.yaml`, semver + content hash stamped into every verdict.

## Scope (v1)

- Eval targets: **shot prompts** (`shotNN.md`) only; episode/project verdicts are rollups of shot verdicts.
- Layouts: staged-novel (`5_6_*/episodes/epNN/shots/`), staged-short/MV (`5_6_*/shots/`), legacy root `episodes/` fallback.
- Out of scope v1: auto-revise loop, rendered-video QC, canon artifacts as eval targets.

## Rubric

- **v3.0.0 (2026-07-29, user-directed simplification):** 6 dimensions → 15 core fields (11 `rule` / 4 near-mechanical `llm`). Removed per user: the faithfulness 忠实剧本, dramatic_effectiveness 戏剧效果, and groundedness 立足原文 dimensions (not every drama has a source novel), every check judged < ~95% run-to-run deterministic, and complex checks — keeping 2–3 core checks per dimension. The full v1 rubric (9 dims / 133 fields) is snapshotted at `rubric/archive_v1/` for incremental re-adoption (copy a field back into its dimension file, `rubric validate`, bump version).
- 3 fixed levels: dimension → sub-category → field.
- v3 dimensions: consistency 一致性 · renderability 可渲染性 · dialogue_quality 台词质量 · cinematography 运镜与站位 · pacing 时长节奏 · format_compliance 格式契约.
- Every field: Chinese judge instruction + 1/3/5 anchors, weight, optional `applies_when` (deterministic pre-filter over unit metadata), optional `gate` (+`gate_min_grade`), source citations.
- Mechanical rules live once each (byte-match/duration/char-count in format_compliance, speech-rate in pacing).
- `version: 1.0.0-draft` until the user's per-dimension review freezes 1.0.0.

## Judge layer

- Two pluggable engines (`judge.engine`):
  - `api` — Anthropic API direct (the interview-chosen design): `output_config.format` JSON-schema-forced output, `output_config.effort` per dimension. Needs a key in `.env`.
  - `claude_code` — headless `claude -p` subprocesses on the user's Claude subscription (added 2026-07-28 per user request, since no API key was available). Independence preserved: subprocess cwd = system temp dir (no CLAUDE.md/skills/MCP), all tools disallowed, schema enforced by prompt + robust extraction + pydantic. Cache keys include the engine. Live-validated same day.
- `claude-opus-5` default judge; per-dimension override — format_compliance/pacing on `claude-sonnet-5`; pydantic validation on every sample.
- One call per dimension per shot; default 3 samples (variance from model stochasticity — Opus 5 takes no temperature).
- Grounding per call (deterministically sliced, hashed): shot file + 小说原文 + matched character/scene/prop cards (locked tags + voice_ids surfaced) + world.md keyword sections + ep script/dialogue + adjacent shots + prior-ep ending (+ structure.md for shorts).
- Prompt caching: shared shot+grounding prefix carries `cache_control`; first dimension call warms it, the rest read.
- Refusal / schema-invalid / API failure → field `judge_error`, never silently guessed.

## Deterministic aggregation

- Sample reconcile: median grade; confidence = min sample confidence ×0.6 if spread ≥2; evidence union.
- Canon conflict: judge flags `CANON_CONFLICT:`; majority of samples flagged → field `inconclusive`.
- Rollup: weighted averages (field weight × sub weight; dimension weights from rubric.yaml) with renormalization over graded fields; composite = (grade−1)/4×100.
- Gates (2026-07-29 hardened per user): gate fields are binary hard contracts (rule gates render as 通过/不通过, no 1–5 gradation in the UI). Any gate field failing → unit FAIL **and propagates to the top**: the episode and project rollups are FAIL outright (`gate_failed_units` listed on the rollup), regardless of composites.
- Inconclusive share > 0.25 → `needs_canon_fix`.
- Tiers: pass ≥75 / conditional_pass ≥60 / fail; episode/project: any-FAIL caps at conditional, FAIL share ≥0.2 → FAIL.
- Findings: every graded field ≤3 → {blocker ≤1 / major ≤2 / minor ≤3}, sorted, stable `finding_id`.

## Determinism & reproducibility

- **Fresh-start runs (2026-07-29, user-directed; supersedes the interview's incremental/cache design):** every `run` re-evaluates its full selection from scratch — no carry-forward of prior verdicts, no local judge-response cache. A run's outcome is a function of (artifacts, rubric, config) at run time only. Clarity over cost, per user.
- Full run record under `runs/{run_id}/`: manifest (hashes, models, rubric id, usage, status), raw judge outputs, per-unit field results, verdicts.json, findings.json, report.md. `runs/latest/{project}.json` pointer.

## Ops

- CLI: `run` / `estimate` / `report` / `trends` / `dispute` / `rubric validate`; selectors --ep/--shot/--dimension; `--dry-run` = rule fields only.
- Async concurrency (default 8), SDK retries; budget: pre-run estimate gate + mid-run hard stop with partial results preserved.
- Estimate models prompt-cache savings; ballpark full-ep (15 shots, defaults): ~$47 cached / ~$16 at `--samples 1`.

## Portal UI (added 2026-07-28, per user request)

The ai_video_management portal hosts an "评测中心" module (`/eval`): read-only browsing of runs/verdicts/findings/reports, plus editing of the rubric YAMLs (server-side `rubric validate` via subprocess, auto-rollback on failure) and `eval_config.yaml`. Eval runs stay CLI-triggered only. The portal consumes this project's **files** — no code import crosses the project boundary, and this project remains unaware of the portal (independence intact). Implementation lives in ai_video_management (`eval_center` aggregate).

## Calibration (phased, per interview)

Production disputes first: `eval dispute --finding <id> --because ...` records a structured correction and appends `golden/golden.jsonl`. Once the golden set is meaningful, add formal agreement/stability meta-eval per rubric version (phase 2).

## Acceptance (v1)

One full wushen_juexing episode AND xianjian_yi_mv evaluated end-to-end with verdicts + insights the user judges accurate. (Blocked only on an API key in `.env`.)
