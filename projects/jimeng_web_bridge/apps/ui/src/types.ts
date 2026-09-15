// Wire types: one interface per response DTO in libs/application/dtos/*.py.
// Field names are the JSON keys; enum-valued fields stay `string` so contract fixtures remain assignable.

export interface HealthQdto {
  ok: boolean;
}

export interface CanaryCheckQdto {
  name: string;
  ok: boolean;
  detail: string | null;
}

export interface WebSessionQdto {
  login_state: string;
  browser_open: boolean;
  web_version: string | null;
  checked_at: string | null;
  canary_operation_id: string | null;
  canary_state: string | null;
  canary_ok: boolean | null;
  canary_checks: CanaryCheckQdto[];
}

export interface CliSessionQdto {
  configured: boolean;
  logged_in: boolean | null;
  version: string | null;
  min_version: string;
  version_ok: boolean | null;
  credit_balance: number | null;
  checked_at: string | null;
  error: string | null;
}

export interface QueueStateCdto {
  backend: string;
  state: string;
  reason: string | null;
  updated_at: string;
}

export interface SessionStatusQdto {
  web: WebSessionQdto;
  cli: CliSessionQdto;
  queues: QueueStateCdto[];
  today_confirmed_credits: number;
  test_mode: boolean;
}

export interface BrowserOpenCdto {
  accepted: boolean;
  message: string | null;
}

export interface OperationCdto {
  operation_id: string;
  kind: string;
  state: string;
}

export interface OperationQdto {
  operation_id: string;
  kind: string;
  state: string;
  subject_id: string | null;
  job_id: string | null;
  step: string | null;
  created_at: string;
  started_at: string | null;
  finished_at: string | null;
  result: Record<string, unknown> | null;
  error_code: string | null;
  error_message: string | null;
}

export interface BatchPrecheckCdto {
  batch_id: string;
  state: string;
  ok_count: number;
  warning_count: number;
  error_count: number;
  estimated_credits: number;
  has_unestimated: boolean;
  existing_job_ids: string[];
  confirm_path: string;
}

export interface BatchConfirmCdto {
  batch_id: string;
  job_ids: string[];
  confirmed_at: string;
}

export interface BatchCheckQdto {
  check: string;
  severity: string;
  code: string;
  message: string;
  config_key: string | null;
  reference_name: string | null;
}

export interface BatchReferenceQdto {
  name: string;
  label: string;
  kind: string;
  path: string | null;
  entity: string | null;
  sha256: string | null;
}

export interface BatchParamsQdto {
  model: string;
  ratio: string;
  resolution: string;
  count: number;
  duration_s: number | null;
  reference_mode: string | null;
}

export interface BatchItemQdto {
  index: number;
  kind: string;
  backend: string;
  source_type: string;
  source_path: string;
  block_key: string | null;
  drama_rel: string | null;
  output_slot: string;
  entity_name: string | null;
  prompt_codepoints: number;
  has_negative_prompt: boolean;
  params: BatchParamsQdto | null;
  references: BatchReferenceQdto[];
  severity: string;
  checks: BatchCheckQdto[];
  estimated_credits: number | null;
  existing_job_id: string | null;
  reroll: boolean;
}

export interface BatchQdto {
  batch_id: string;
  state: string;
  created_at: string;
  expires_at: string | null;
  confirmed_at: string | null;
  confirmer: string | null;
  ok_count: number;
  warning_count: number;
  error_count: number;
  estimated_credits: number;
  has_unestimated: boolean;
  existing_job_ids: string[];
  job_ids: string[];
  balance_start: number | null;
  balance_end: number | null;
  confirm_path: string;
  page: number;
  page_size: number;
  total_items: number;
  items: BatchItemQdto[];
}

export interface BatchConfirmationQdto {
  batch_id: string;
  token: string;
  expires_at: string;
  seconds_left: number;
  estimated_credits: number;
  today_confirmed_credits: number;
}

export interface TransitionQdto {
  from_state: string | null;
  to_state: string;
  reason: string | null;
  at: string;
}

export interface JobSummaryQdto {
  job_id: string;
  batch_id: string;
  kind: string;
  backend: string;
  source_type: string;
  source_path: string | null;
  drama_rel: string | null;
  output_slot: string;
  state: string;
  reason: string | null;
  blocked_on: string | null;
  preparing_step: string | null;
  attempt: number;
  confirmed: boolean;
  cancel_requested: boolean;
  credits_spent: boolean;
  platform_task_id: string | null;
  credits_estimated_static: number | null;
  credits_estimated_page: number | null;
  credits_charged: number | null;
  created_at: string;
  updated_at: string;
}

export interface JobPageQdto {
  items: JobSummaryQdto[];
  total: number;
  page: number;
  page_size: number;
  cursor: string | null;
}

export interface JobRuntimeQdto {
  screenshots: string[];
  outputs: string[];
  progress_pct: number | null;
  last_error: string | null;
  sidecar_missing: boolean;
}

export interface AllowedActionQdto {
  action: string;
  ui_only: boolean;
}

export interface JobDetailQdto {
  job: JobSummaryQdto;
  transitions: TransitionQdto[];
  pause_reason: string | null;
  pause_tier: string | null;
  resume_allowance: string | null;
  allowed_actions: AllowedActionQdto[];
  runtime: JobRuntimeQdto;
  credits_not_refundable: boolean;
}

export interface JobStateCdto {
  job_id: string;
  state: string;
  reason: string | null;
  attempt: number;
  cancel_requested: boolean;
  credits_spent: boolean;
  platform_task_id: string | null;
  message: string | null;
}

export interface WaitJobQdto {
  job_id: string;
  state: string;
  reason: string | null;
  blocked_on: string | null;
  preparing_step: string | null;
  platform_task_id: string | null;
  progress_pct: number | null;
  updated_at: string;
}

export interface StateCountQdto {
  state: string;
  count: number;
}

export interface WaitSnapshotQdto {
  jobs: WaitJobQdto[];
  counts: StateCountQdto[];
  total_jobs: number;
  missing_job_ids: string[];
  operation: OperationQdto | null;
}

export interface WaitQdto {
  snapshot: WaitSnapshotQdto;
  finished: boolean;
  suggested_next: string;
  waited_s: number;
  timeout_s: number;
}

export interface DramaNodeQdto {
  name: string;
  path: string;
  type: string;
  children: DramaNodeQdto[];
}

export interface DramaTreeQdto {
  dramas: DramaNodeQdto[];
}

export interface ConfigErrorQdto {
  error_code: string;
  field_path: string;
  message: string;
}

export interface NeedsConfirmationQdto {
  code: string;
  key: string;
  config_key: string | null;
  reason: string;
  suggestion: string | null;
  shots: string[];
}

export interface CardEntityQdto {
  character_dir: string;
  card_rel: string;
  entity_name: string | null;
  naming_abbrev: string;
  source_drama_rel: string | null;
  in_snapshot: boolean | null;
  error_code: string | null;
  config_key: string | null;
}

export interface ReferencePreviewItemQdto {
  name: string;
  label: string;
  kind: string | null;
  resolver: string | null;
  status: string;
  resolved_path: string | null;
  link_path: string | null;
  entity_name: string | null;
  candidates: string[];
  reason: string | null;
  message: string | null;
  suggested_override_key: string | null;
}

export interface ShotReferencePreviewQdto {
  shot_rel: string;
  shot: string;
  parse_error: string | null;
  integrity_ok: boolean;
  unrecognized: string[];
  items: ReferencePreviewItemQdto[];
}

export interface DramaConfigQdto {
  drama_rel: string;
  location: string;
  exists: boolean;
  data: Record<string, unknown>;
  raw_text: string | null;
  sha256: string | null;
  parse_error: string | null;
  validation_error: ConfigErrorQdto | null;
  needs_confirmation: NeedsConfirmationQdto[];
  entities: CardEntityQdto[];
  reference_preview: ShotReferencePreviewQdto[];
}

export interface ConfigDiffItemCdto {
  key: string;
  change: string;
  current: unknown;
  proposed: unknown;
}

export interface ProposeCdto {
  drama_rel: string;
  location: string;
  exists: boolean;
  current_sha256: string | null;
  current_parse_error: string | null;
  proposed_data: Record<string, unknown>;
  proposed_toml: string;
  diff: ConfigDiffItemCdto[];
  validation_error: ConfigErrorQdto | null;
  needs_confirmation: NeedsConfirmationQdto[];
  entities: CardEntityQdto[];
  reference_preview: ShotReferencePreviewQdto[];
}

export interface SaveConfigCdto {
  drama_rel: string;
  location: string;
  sha256: string;
}

export interface GlobalConfigQdto {
  location: string;
  values: Record<string, unknown>;
  raw_text: string | null;
  sha256: string | null;
  parse_error: string | null;
  validation_error: ConfigErrorQdto | null;
  overridden_by_env: string[];
}

export interface GlobalConfigSaveCdto {
  location: string;
  sha256: string;
  changed_keys: string[];
}

export interface EntityUsageQdto {
  drama_rel: string;
  character_dir: string | null;
  card_rel: string | null;
  source_drama_rel: string | null;
  via: string;
}

export interface ReconcileRowQdto {
  name: string;
  state: string;
  usages: EntityUsageQdto[];
  thumbnail_url: string | null;
  modified_at: string | null;
}

export interface UnnamedCardQdto {
  drama_rel: string;
  character_dir: string;
  card_rel: string;
  error_code: string;
  config_key: string | null;
}

export interface DramaConfigIssueQdto {
  drama_rel: string;
  error: ConfigErrorQdto;
}

export interface ReconcileQdto {
  drama_rel: string | null;
  snapshot_synced_at: string | null;
  snapshot_age_h: number | null;
  stale: boolean;
  never_synced: boolean;
  mapped_count: number;
  missing_count: number;
  unmapped_count: number;
  rows: ReconcileRowQdto[];
  unnamed_cards: UnnamedCardQdto[];
  config_issues: DramaConfigIssueQdto[];
}

export interface DurationsQdto {
  queue_wait_s: number | null;
  prepare_s: number | null;
  render_s: number | null;
  download_s: number | null;
}

export interface HistoryItemQdto {
  job_id: string;
  batch_id: string;
  kind: string;
  backend: string;
  state: string;
  reason: string | null;
  drama_rel: string | null;
  shot: string | null;
  subject: string | null;
  block_key: string | null;
  source_path: string | null;
  output_slot: string;
  attempt: number;
  credits_estimated_static: number | null;
  credits_estimated_page: number | null;
  credits_charged: number | null;
  created_at: string;
  finished_at: string | null;
  durations: DurationsQdto;
  outputs: string[];
  candidates: string[];
}

export interface BatchBalanceQdto {
  batch_id: string;
  balance_start: number | null;
  balance_end: number | null;
}

export interface HistoryPageQdto {
  items: HistoryItemQdto[];
  total: number;
  page: number;
  page_size: number;
  batches: BatchBalanceQdto[];
}

export interface DailyTotalQdto {
  date: string;
  jobs: number;
  jobs_done: number;
  jobs_failed: number;
  credits_estimated_static: number;
  credits_estimated_page: number;
  credits_charged: number;
}

export interface DailyTotalsQdto {
  timezone: string;
  days: DailyTotalQdto[];
}

export interface ArchivedFileCdto {
  from_rel: string;
  to_rel: string;
}

export interface PromoteCdto {
  candidate_rel: string;
  target_rel: string;
  sidecar_rel: string;
  sha256: string;
  size: number;
  archived: ArchivedFileCdto[];
}

export type AdjudicationBody =
  | { choice: "link_existing"; platform_task_id: string }
  | { choice: "confirm_not_submitted" }
  | { choice: "cancel" }
  | { choice: "approve_estimate"; approved_credits: number };

export type StepOp = "set_params" | "upload" | "fill" | "preview";

export type ConfigSaveBody = { data: Record<string, unknown>; expected_sha256: string | null } | { text: string; expected_sha256: string | null };
