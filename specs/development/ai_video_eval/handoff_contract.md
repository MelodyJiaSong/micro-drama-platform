# Handoff contract — consuming eval verdicts (v1)

Stable interface for any downstream revision agent. Read `runs/latest/{project}.json` first; never write into `ai_videos/` from the eval side.

## Entry point

`projects/ai_video_eval/runs/latest/{project}.json`:

```json
{
  "run_id": "20260728-210535-wushen_juexing",
  "ts": "…",
  "project": "wushen_juexing",
  "tier": "conditional_pass",
  "composite": 78.4,
  "verdicts_path": "<run_id>/verdicts.json",
  "findings_path": "<run_id>/findings.json",
  "report_path": "<run_id>/report.md"
}
```

Paths are relative to `projects/ai_video_eval/runs/`.

## findings.json — the actionable list

Array sorted by severity (`blocker` → `major` → `minor`), then grade. Each finding:

| field | meaning |
|---|---|
| `finding_id` | stable sha1(unit_id\|field_id)[:10] — cite it in disputes |
| `unit_id` | `{project}/{ep or flat}/{shotNN}` |
| `dim_id` / `sub_id` / `field_id` / `field_name_cn` | rubric coordinates (see `rubric/dimensions/{dim_id}.yaml` for the judge instruction + anchors) |
| `grade` | 1–5 (median of judge samples, or 1/5 for rule checks) |
| `severity` | `blocker` (grade ≤1) / `major` (≤2) / `minor` (≤3) |
| `justification` | judge's written reasoning (or rule message) |
| `evidence` | verbatim quotes from the shot/grounding |
| `revision_hint` | one concrete edit suggestion (which field, what change) |
| `locator` | absolute path of the evaluated `shotNN.md` |
| `unit_tier` | the owning shot's verdict tier |

## verdicts.json — the full picture

`project_verdict` + `episode_verdicts{scope}` (tier, composite 0–100, unit_tally, dimension_composites) + `units[]` (per-shot tier, composite, per-dimension scores incl. inconclusive/error counts, gate_failures, findings, carried_forward).

Tier semantics: `pass` / `conditional_pass` / `fail` / `needs_canon_fix` (the last means: canon contradictions blocked judging — fix canon before revising shots).

## Revision loop protocol

1. Fix artifacts starting from `blocker` findings (use `revision_hint` + `evidence`).
2. Re-run `eval run --project X` — unchanged shots carry forward; changed shots re-judge (cache makes repeats cheap).
3. Verdict disagreements go back via `eval dispute --project X --finding <finding_id> --because "…"` — they accumulate the golden set that recalibrates the rubric.

Schema stability: additive changes only within rubric 1.x; field removals/renames bump the rubric major version (stamped in every manifest and verdicts.json).
