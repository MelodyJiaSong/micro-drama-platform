# Research playbook (stage 3)

Procedural runbook the parent reads to drive stage 3. Pre-reading contract, parent-direct model, audit-spawn paths, and pinned-items handling are in `CONVENTIONS.md` (§ Stage playbooks and reference docs, § Tool scoping, § Pinned items survive regeneration).

Always focus on **business value and use case**, not technology trivia.

## Inputs

`task_type`, `task_name`, `task_id`, plus:
- `revised_prompt_path` = `specs/{task_type}/{task_name}/user_input/revised_prompt.md`
- `qa_path` = `specs/{task_type}/{task_name}/interview/qa.md`

## Procedure

### 1. Identify research angles

Read revised prompt + Q&A. Pick **3–6 angles** where missing knowledge would degrade the spec. Examples (pick only what applies):

- **Prior art** — existing solutions and how they solve it (named products, OSS).
- **Domain knowledge** — vocabulary, standards, mental models the user is implicitly invoking.
- **User workflow patterns** — how target users actually do this work today.
- **Integration constraints** — APIs, data formats, rate limits of named external systems.
- **Risk areas** — concurrency, data loss, auth, anywhere wrong choices are expensive.
- **Regulatory / compliance** — only if the spec touches regulated data.
- **UX conventions** — only if the spec involves UI.

Each angle needs a **one-line goal** that names a specific business / use-case question the spec author would otherwise have to guess at. *"Survey of comparable tools"* is not an angle; *"what UX pattern do mature read-only artifact viewers converge on for the sidebar"* is.

Don't pad. If the use case is well understood, fewer angles is fine.

### 2. Spawn researcher workers in parallel

One general-purpose worker per angle, all in parallel via `子代理委派能力` (single message, multiple tool calls). Each worker:

- Receives available search / page-fetch, file and shell capabilities; tool names and permissions come from the actual runtime.
- Receives revised prompt, Q&A, its assigned angle + 1-line goal.
- Writes to `specs/{task_type}/{task_name}/findings/angle-{slug}.md`.
- Returns a 3-bullet executive summary in its final message.

Capture spawn audit under `.audit/adhoc_agents/{YYYY-MM-DD}/{task_id}/spawns/researcher-NN-{slug}/`.

#### Worker prompt template

```
You are a researcher for the "{angle}" angle of a spec-driven task.

Step 0 — verify available search and page-fetch capabilities. Use loaded tools directly;
discover only tools actually deferred in this runtime. See CONVENTIONS.md's tool mapping.
If either capability is unavailable, return {"angle": "{slug}", "status": "deferred_tool_unavailable", "missing": [...], "partial_findings_from_repo_only": "<from local files>"} and STOP. Do not paraphrase training data as if researched. Do not pad.

Revised user prompt:
{paste}

Interview Q&A:
{paste}

Your angle: {angle}
What this angle should answer: {1-line goal}

Constraints:
- Focus on BUSINESS and USE CASE — not language/library/framework choices unless the spec explicitly hinges on them.
- Cite sources (URLs) for non-obvious facts (real searched / fetched pages only, never invented).
- Distinguish established practice from your opinion.
- 600–1200 words; bullets and tables are fine.
- If you can't find substantive content, say so explicitly — don't pad.

Write findings to specs/{task_type}/{task_name}/findings/angle-{slug}.md. The file MUST begin with the worker-output envelope (per CONVENTIONS.md § Tool scoping and team coordination, coordination point 3):

---
worker_id: researcher-NN-{slug}
stage: 3
role: researcher
angle: {slug}
status: complete   # or partial / deferred_tool_unavailable / halted
blockers: []
confidence: high | medium | low
---

Then the sections:
1. What this angle covers
2. Key findings (bulleted, with citations)
3. Implications for the spec (concrete, actionable)
4. Open questions surfaced

Mirror the same file (envelope + sections) into your audit output.md. Return a 3-bullet executive summary in your final message.
```

#### Halting on deferred-tool failure

If any worker returns `status: "deferred_tool_unavailable"`, do NOT consolidate the dossier as if the angle were covered. Recovery paths:

1. **Run the missing web calls from the parent** if those tools are available there. Record the actual executor.
2. **Halt and escalate** with `{"status": "halted", "reason": "deferred_tool_unavailable", "missing": [...]}` if the parent can't recover the angle either.

Plaintext-fallback / fabricated-citation behavior is forbidden. Empty beats invented.

### 3. Consolidate into a dossier

Read every `angle-*.md` and write `specs/{task_type}/{task_name}/findings/dossier.md`:

```markdown
# Findings dossier — {task_name}

Run: {task_id}

## Angles researched
1. {angle slug} — {1-line goal}
2. ...

## Cross-cutting insights
- {insight that emerged from combining angles} *(angle-a + angle-b)*

## Per-angle highlights
### {angle 1 slug}
- {highlight 1}
- ...

## Recommendations for the spec
- {concrete recommendation}

## Open questions surviving research
- {question}, asked from angle {slug}
```

Cross-cutting insights MUST cite the angle files that combined to surface them (e.g., `*(prior-art + filesystem-risks)*`).

## Tools

- `Read`, `Write`, `Bash` — standard.
- `子代理委派能力` — researcher workers in parallel.
- Search / page-fetch — use available runtime tools, including when the parent runs an angle directly.

## Failure modes to refuse

- **No paraphrasing from training data** as if researched. Every factual claim traces to a fetched URL.
- **No fabricated worker outputs.** If the parent runs an angle directly (recovery), audit folder records that.
- **No padding.** Honest "open questions / not researched" beats thin angle files.
