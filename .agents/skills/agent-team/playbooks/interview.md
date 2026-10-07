# Interview playbook (stage 2)

Procedural runbook the parent reads to drive stage 2. Pre-reading contract, parent-direct model, audit-spawn paths, and pinned-items handling are in `CONVENTIONS.md` (§ Stage playbooks and reference docs, § Tool scoping, § Pinned items survive regeneration).

## Inputs

`task_type`, `task_name`, `task_id`, plus `revised_prompt_path` = `specs/{task_type}/{task_name}/user_input/revised_prompt.md`.

## Procedure

### 1. Identify probe categories

Read the revised prompt. Pick **3–6** categories that probe real ambiguity for THIS task. Common categories — pick only what's load-bearing, ignore the rest:

- User roles & goals
- Functional scope (in/out, MVP boundaries)
- Data model (entities, relationships, sources of truth)
- Integrations (external systems, APIs, file formats)
- UX & interaction (UI conventions, accessibility, primary flows)
- Non-functional (performance, scale, security, deployment)
- Edge cases & failure modes
- Success criteria

>6 dilutes focus; <3 usually misses something.

### 2. Generate the question pool

For each category, produce **3–5 multi-choice questions** that probe a real ambiguity. Pick one shape:

- **Shape A — direct (default).** Parent generates the pool itself in one pass. Cheaper, lower latency. Use when categories are tight.
- **Shape B — fan-out.** Parent spawns one worker per category in parallel via `子代理委派能力`. Each worker reads the prompt + its assigned category and returns 3–5 questions as JSON. Use when categories require divergent reasoning that would crowd the parent's context, or total questions would exceed ~15.

Each question MUST:
- Be specific to this use case (not generic).
- Have distinct, mutually-exclusive options within the active tool's limit; let its UI supply free-text / Other when supported.
- Mark the recommended option with `(Recommended)` suffix when there's a clear default.
- Probe a real ambiguity, not a settled fact.

Use free text when the missing fact cannot sensibly be expressed as choices.

### 3. Ask the user via `用户提问能力`

The parent asks using the active runtime's user-input tool. Discover it only if deferred; use conversation if no such tool is available. See `CONVENTIONS.md` § Tool scoping and team coordination.

- Batch within the actual tool's question / option limits; asynchronous calls require actual answers before dependent work proceeds.
- Group questions by category so the user doesn't context-switch.
- Preserve options and whether multiple answers are needed; if the tool only supports single selection, split the question or accept a free-text answer.

### 4. Iterate to clarity

After collecting answers, re-evaluate each category:

- **Shape A.** Parent re-reads the prompt + answers and decides per-category whether it's clear.
- **Shape B.** Parent re-invokes each worker in parallel: "is this category clear, or are there follow-ups?" Each returns `{"clear": true}` or `{"clear": false, "follow_ups": [...]}`.

Cap at 3 rounds total. If still unclear after 3, escalate with a plain-text summary of what remains.

### 5. AUTONOMOUS mode

Under `# EXECUTION MODE: AUTONOMOUS`, do NOT call `用户提问能力`. For each generated question, pre-answer with best-judgment default annotated as `*(judgment call — chose X because Y)*`. Each annotation cites the FR slice it binds into so a future interactive run can revise without re-deriving the rationale.

### 6. Write `qa.md`

Save to `specs/{task_type}/{task_name}/interview/qa.md`:

```markdown
# Interview — {task_name}

Run: {task_id}

## Categories probed
- {category 1} — {1-line why}
- ...

## Round 1

### {category 1}
**Q:** {question text}
- A: {selected option label} — {selected option description}
- (or "Other: {user's free-text}")
- (or "A *(judgment call — chose X because Y)*: {label}" under autonomous mode)

### {category 2}
...

## Round 2 (if any)
...

## Team consensus
All categories marked clear after {N} round(s).
```

## Tools

- `Read` — revised prompt, pre-reading, prior `qa.md` (if resuming).
- `Write` — `qa.md`.
- `Bash` — `mkdir -p` audit folders, ISO timestamps.
- `子代理委派能力` — shape B only.
- `用户提问能力` — interactive mode only.

## Failure modes to refuse

- **Do not fabricate answers.** When the input tool is unavailable, ask in conversation; autonomous mode uses annotated judgment calls rather than claimed user approvals.
- **Don't fabricate shape-B worker outputs** when shape A actually ran. Audit and artifact must agree.
- **Don't pad.** 3 categories with 3 sharp questions beat 6 categories with filler.
