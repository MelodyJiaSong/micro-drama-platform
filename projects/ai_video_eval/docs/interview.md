# ai_video_eval — requirements interview

Free-form interview (2026-07-28), ≥50 questions across 13 angles. Answers recorded verbatim by round. Companion docs: `raw_prompt.md`, `revised_prompt.md`.

## Round 1 — Scope & evaluation targets

- **Artifact layers evaluated in v1 (multi-select):** Shot prompts only (shotNN.md: 视频 prompt + 台词配音 + Shot context). Episode scripts / canon artifacts / whole-drama sequence NOT selected as v1 eval targets.
- **Verdict granularity:** shot + episode + project rollup (per-shot verdicts aggregate upward).
- **Layouts:** legacy (wushen_juexing) + new staged dirs, via auto-detection.
- **单片/MV mode (sub_type=short):** YES, in v1 (flat layout, MV-specific applicability).

## Round 2 — Independence boundary

- **Location:** `projects/ai_video_eval/` in this repo. Independence = zero runtime coupling to `.claude` settings/skills, not physical separation.
- **Rubric origin:** derive-then-freeze — mine existing review skills/agent_refs into the rubric at authoring time; rubric fully self-contained afterwards, no runtime reads of `.claude` anything.
- **Judge engine:** Anthropic API direct (python SDK, no harness).
- **Isolation:** own config/.env inside the eval project; reads `ai_videos/{name}/` artifacts directly; never reads `.claude/`, `CLAUDE.md`, or repo settings at runtime.

## Round 3 — Rubric structure & format

- **Format:** YAML files (schema-validated; one file per dimension + top file for weights/gates).
- **Hierarchy:** fixed 3 levels — dimension → sub-category → field (fields are judged leaves).
- **Per-field judge output:** rich record — ordinal grade (1–5) + confidence + justification + verbatim evidence quotes + concrete revision hint.
- **Versioning:** semver on rubric + every verdict stamped with rubric version + content hash; cross-version comparisons flagged.

## Round 4 — Dimension content

- **Dimension set:** full ~9 — groundedness · consistency · faithfulness · renderability (模型视角) · dialogue quality · cinematography · pacing/duration · format compliance · dramatic effectiveness.
- **Mechanical checks:** hybrid rubric — same tree holds `evaluator: rule` (deterministic code) and `evaluator: llm` fields; one aggregation.
- **Weights:** configurable per-dimension AND per-field in rubric YAML.
- **Applicability:** explicit `applies_when` conditions on unit metadata (shot type, sub_type, has_dialogue…); inapplicable fields excluded deterministically before judging.

## Round 5 — Judge layer

- **Model policy:** per-dimension configurable (config maps dimension → model + params), one strong default.
- **Call granularity:** one call per dimension per shot (that dimension's fields + its grounding bundle; ~9 calls/shot).
- **Sampling:** default 3 independent samples per judging call, per-dimension configurable.
- **Anchoring:** every field ships grade anchors in the rubric (what 1 / 3 / 5 concretely look like, domain examples).

## Round 6 — Grounding context

- **Sources (multi-select, all four):** 小说原文 excerpt · canon slice (referenced character/scene/prop cards + world.md sections) · episode script.md + dialogue.md · adjacent shots (prev/next).
- **Assembly:** deterministic slicing from shot metadata — same input bytes → same context bytes (hashable).
- **Canon contradictions:** ⚠ NOT the recommended option — **mark affected fields inconclusive** (no grade; verdict notes the gap). No auto-precedence resolution.
- **Cross-episode:** window + summaries — previous ep's ending beats verbatim + cached summary index of earlier eps (signature lines, power level, open hooks).

## Round 7 — Deterministic aggregation layer (non-LLM)

- **Sample reconciliation:** median grade; confidence = min sample confidence, downgraded further if spread > 1 step; evidence union; spread kept as stability signal.
- **Roll-up:** weighted average at every level + hard gates — `gate: true` fields below threshold cap the parent verdict regardless of average.
- **Inconclusive/inapplicable:** excluded from averages (weights renormalize), counted separately; if inconclusive share exceeds configured threshold → unit verdict `needs_canon_fix`.
- **Verdict taxonomy:** pass / conditional_pass / fail / needs_canon_fix + 0–100 composite + per-dimension subscores, at every rollup level.

## Round 8 — Determinism, caching & reproducibility

- **Caching:** content-addressed — key = hash(shot bytes + grounding bytes + rubric version + model + params); unchanged inputs reuse stored judgments byte-for-byte.
- **Re-run default:** incremental by input hash; `--full` forces everything.
- **Output enforcement:** API structured-output/tool-schema forced JSON + pydantic validation (ranges/enums) + bounded retries; persistent violation → field marked `judge_error`, never silently guessed.
- **Run record:** full — `runs/{run_id}/` with manifest (input hashes, model IDs, rubric version+hash, config snapshot), every raw judge response, parsed results, aggregation output, final verdicts. Any verdict re-derivable.

## Round 9 — Outputs & consumption

- **Formats:** JSON canonical + rendered Chinese Markdown report per episode/run.
- **Location:** everything under `projects/ai_video_eval/runs/{run_id}/` + stable `runs/latest/{project}.json` pointer. **`ai_videos/` is never written to.**
- **Insights:** structured findings list — {unit, dimension, sub-category, field, grade, severity, evidence quotes, revision_hint, file+section locator}, sorted by severity.
- **Handoff:** documented, versioned JSON schema + short consumption guide inside the eval project; future revision agents read `runs/latest/{project}.json` on demand.

## Round 10 — Architecture & stack

- **Language:** Python (typed, pydantic, anthropic SDK, own requirements.txt).
- **Structure:** repo DDD solution layout (apps/cli + libs 4-layer per § Project rules) — runtime independence ≠ structural exemption.
- **Interface:** CLI only v1 (`eval run / report / rubric validate / resume / dispute`).
- **Rubric authoring:** draft-all-then-review — mine ai_video.md + 9 review skills + changelog lessons into a complete draft (anchors included); user reviews dimension-by-dimension before freezing v1.0.0.

## Round 11 — Execution model & ops

- **Run scoping:** flexible selectors (--project/--ep/--eps/--shot/--dimension); default = changed-since-last-run.
- **Parallelism:** asyncio concurrent judge calls, configurable in-flight cap, backoff on 429/5xx.
- **Cost:** pre-run token/cost estimate + configurable budget cap (abort before start if estimate exceeds; graceful stop + checkpoint mid-run).
- **Failures:** checkpoint + resume; failed fields marked `judge_error` with cause; `eval resume {run_id}` re-attempts failures only.

## Round 12 — Relationship to existing QC + calibration

- **vs review skills:** independent second opinion; in-pipeline skill reviews keep running; neither depends on the other.
- **Overlap:** deliberate overlap is fine — independence is runtime coupling, not ideas.
- **Calibration (user-specified phased plan):** ⚠ custom answer — **start with in-production calibration** (no golden set exists yet): disputes during real use tune the rubric; **disputed/labeled cases accumulate into a golden set**; once large enough, **switch to golden-set calibration** as the formal gate.
- **Meta-eval:** agreement with golden labels + re-run stability (sample-spread distribution), reported per rubric version.

## Round 13 — Feedback loop, trends & v1 boundary

- **Auto-revise loop:** out of scope v1 — eval ends at verdicts + contract-conforming insights.
- **Trends:** basic analytics in v1 — per-dimension score trajectories across runs/episodes + recurring-failure ranking.
- **Disputes:** structured — `eval dispute <finding-id> --because …` records corrections; batch into rubric version bumps AND accumulate as the golden set (feeds the Round-12 phased plan).
- **v1 acceptance:** one full wushen_juexing episode (legacy layout) AND xianjian_yi_mv (short/flat layout) evaluated end-to-end, with verdicts + insights the user judges accurate and useful.

## Key deviations from recommendations (decisions to honor)

1. **v1 eval targets = shot prompts only** — episode/project verdicts exist only as rollups of shot verdicts; scripts/canon/sequence are grounding context, not eval targets.
2. **短片/MV mode is in v1**, not phase 2.
3. **Canon contradictions → fields inconclusive** (excluded from averages, counted, `needs_canon_fix` verdict above threshold) — no auto-precedence resolution.
4. **Calibration is phased**: production-dispute calibration now → golden-set calibration once disputes accumulate.

## Status

Interview complete (52 questions, 13 rounds, 2026-07-28). Built same day: `docs/spec.md` compiled, rubric mined (9 parallel distillation agents → 133 fields, frozen as `rubric/` v1.0.0-draft), full system implemented + tested (28 tests), dry-runs validated on wushen_juexing ep08 (novel layout) and xianjian_yi_mv (short layout). Remaining for v1 acceptance: API key in `.env` → live judged run on both projects → user reviews verdicts; per-dimension rubric review to freeze 1.0.0.
