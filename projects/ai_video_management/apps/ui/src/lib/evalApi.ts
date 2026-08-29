/** API client + types for the eval-center module (ai_video_eval file surfaces).
 * Results are read-only; rubric + config are editable; runs are CLI-triggered only. */

export interface EvalAnchors {
  g1: string;
  g3: string;
  g5: string;
}

export interface EvalField {
  id: string;
  name_cn: string;
  evaluator: "rule" | "llm";
  weight: number;
  judge_instruction_cn?: string;
  anchors?: EvalAnchors;
  rule_id?: string;
  rule_params?: Record<string, unknown>;
  applies_when?: string;
  gate?: boolean;
  gate_min_grade?: number;
  sources?: string[];
}

export interface EvalSubcategory {
  id: string;
  name_cn: string;
  weight: number;
  fields: EvalField[];
}

export interface EvalDimension {
  dimension_id: string;
  name_cn: string;
  description_cn: string;
  weight: number;
  file: string;
  subcategories: EvalSubcategory[];
}

export interface EvalOverview {
  version: string;
  verdict: Record<string, unknown>;
  dimension_weights: Record<string, number>;
  dimensions: EvalDimension[];
  files: string[];
}

export interface EvalRunManifest {
  run_id: string;
  ts: string;
  project: string;
  status: string;
  rubric_version: string;
  tier?: string;
  composite?: number | null;
  findings_total?: number;
  findings_blocker?: number;
  halted_reason?: string | null;
  usage?: { cost_usd?: number; api_calls?: number; cache_hits?: number };
  selector?: { dry_run?: boolean };
}

export interface EvalRuns {
  runs: EvalRunManifest[];
  latest: Record<string, string>;
}

export interface EvalFinding {
  finding_id: string;
  unit_id: string;
  dim_id: string;
  field_id: string;
  field_name_cn: string;
  grade: number;
  severity: "blocker" | "major" | "minor";
  justification: string;
  evidence: string[];
  revision_hint: string;
  locator: string;
  unit_tier?: string;
}

export interface EvalSubcategoryScore {
  sub_id: string;
  name_cn: string;
  composite: number | null;
  graded: number;
  inconclusive: number;
  inapplicable: number;
  errors: number;
  rule_passed?: number;
  rule_failed?: string[];
}

export interface EvalDimensionScore {
  dim_id: string;
  name_cn: string;
  composite: number | null;
  graded: number;
  inconclusive: number;
  inapplicable: number;
  errors: number;
  gate_failures: string[];
  subcategories?: EvalSubcategoryScore[];
  rule_passed?: number;
  rule_failed?: string[];
}

export interface EvalFieldMeta {
  name_cn: string;
  dim_id: string;
  dim_name: string;
  sub_id: string;
  sub_name: string;
  weight: number;
  gate: boolean;
  evaluator: "rule" | "llm";
}

export interface EvalUnitVerdict {
  unit_id: string;
  tier: string;
  composite: number | null;
  dimension_scores: EvalDimensionScore[];
  findings: EvalFinding[];
  graded: number;
  inconclusive: number;
  errors: number;
  gate_failures: string[];
  carried_forward: boolean;
  rule_total?: number;
  rule_passed?: number;
  rule_failed_fields?: string[];
}

export interface EvalRollup {
  scope_id: string;
  tier: string;
  composite: number | null;
  unit_tally: Record<string, number>;
  dimension_composites: Record<string, number>;
  unit_count: number;
  gate_failed_units?: string[];
  rule_failed_units?: string[];
}

export interface EvalVerdicts {
  project_verdict: EvalRollup;
  episode_verdicts: Record<string, EvalRollup>;
  units: EvalUnitVerdict[];
}

export interface EvalRunDetail {
  manifest: EvalRunManifest;
  verdicts: EvalVerdicts | null;
  findings: EvalFinding[] | null;
}

export interface EvalFieldResult {
  field_id: string;
  dim_id: string;
  sub_id: string;
  status: string;
  grade: number | null;
  confidence: number;
  spread: number;
  justification: string;
  evidence: string[];
  revision_hint: string;
  source: string;
  error?: string | null;
}

export interface EvalUnitResults {
  unit_id: string;
  fields: EvalFieldResult[];
  field_meta?: Record<string, EvalFieldMeta>;
}

export interface EvalSaveResult {
  validated: boolean;
  output: string;
}

export interface EvalRawJudgment {
  field_id: string;
  grade: number;
  confidence: number;
  justification: string;
  evidence: string[];
  revision_hint: string;
}

export interface EvalRawSample {
  sample: number | null;
  error?: string | null;
  judgments: EvalRawJudgment[] | null;
  text_preview?: string | null;
}

export interface EvalRawJudgments {
  unit_id: string;
  dim_id: string;
  model?: string;
  samples_requested?: number;
  samples: EvalRawSample[];
}

async function evalJson<T>(response: Response): Promise<T> {
  const text = await response.text();
  if (!response.ok) {
    let message = `HTTP ${response.status}`;
    try {
      const parsed = text ? (JSON.parse(text) as { detail?: { message?: string } }) : null;
      if (parsed?.detail?.message) message = parsed.detail.message;
    } catch {
      // not JSON
    }
    throw new Error(message);
  }
  return JSON.parse(text) as T;
}

const GET_OPTS: RequestInit = {
  method: "GET",
  headers: { Accept: "application/json" },
  cache: "no-store",
};

export async function fetchEvalOverview(): Promise<EvalOverview> {
  return evalJson(await fetch("/api/eval/overview", GET_OPTS));
}

export async function fetchEvalRubricFile(name: string): Promise<{ name: string; content: string }> {
  return evalJson(await fetch(`/api/eval/rubric-file?name=${encodeURIComponent(name)}`, GET_OPTS));
}

export async function putEvalRubricFile(name: string, content: string): Promise<EvalSaveResult> {
  return evalJson(
    await fetch("/api/eval/rubric-file", {
      method: "PUT",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ name, content }),
    }),
  );
}

export async function fetchEvalConfig(): Promise<{ content: string }> {
  return evalJson(await fetch("/api/eval/config", GET_OPTS));
}

export async function putEvalConfig(content: string): Promise<EvalSaveResult> {
  return evalJson(
    await fetch("/api/eval/config", {
      method: "PUT",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ content }),
    }),
  );
}

export async function fetchEvalRuns(): Promise<EvalRuns> {
  return evalJson(await fetch("/api/eval/runs", GET_OPTS));
}

export async function fetchEvalRunDetail(runId: string): Promise<EvalRunDetail> {
  return evalJson(await fetch(`/api/eval/run/${encodeURIComponent(runId)}`, GET_OPTS));
}

export async function fetchEvalReport(runId: string): Promise<{ content: string }> {
  return evalJson(await fetch(`/api/eval/run/${encodeURIComponent(runId)}/report`, GET_OPTS));
}

export async function fetchEvalUnitResults(runId: string, unit: string): Promise<EvalUnitResults> {
  return evalJson(
    await fetch(
      `/api/eval/run/${encodeURIComponent(runId)}/unit?unit=${encodeURIComponent(unit)}`,
      GET_OPTS,
    ),
  );
}

export async function fetchEvalRawJudgments(
  runId: string,
  unit: string,
  dim: string,
): Promise<EvalRawJudgments> {
  return evalJson(
    await fetch(
      `/api/eval/run/${encodeURIComponent(runId)}/raw?unit=${encodeURIComponent(unit)}&dim=${encodeURIComponent(dim)}`,
      GET_OPTS,
    ),
  );
}

export function formatEvalTs(ts?: string): string {
  if (!ts) return "—";
  const date = new Date(ts);
  if (Number.isNaN(date.getTime())) return ts;
  const pad = (n: number): string => String(n).padStart(2, "0");
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
}

export const TIER_CN: Record<string, string> = {
  pass: "通过",
  conditional_pass: "有条件通过",
  fail: "不通过",
  needs_canon_fix: "需先修 canon",
};

export const SEVERITY_CN: Record<string, string> = {
  blocker: "阻断",
  major: "严重",
  minor: "轻微",
};
