import type {
  AdjudicationBody,
  BatchConfirmationQdto,
  BatchConfirmCdto,
  BatchPrecheckCdto,
  BatchQdto,
  BrowserOpenCdto,
  ConfigSaveBody,
  DailyTotalsQdto,
  DramaConfigQdto,
  DramaTreeQdto,
  GlobalConfigQdto,
  GlobalConfigSaveCdto,
  HistoryPageQdto,
  JobDetailQdto,
  JobPageQdto,
  JobStateCdto,
  OperationCdto,
  OperationQdto,
  PromoteCdto,
  ProposeCdto,
  QueueStateCdto,
  ReconcileQdto,
  SaveConfigCdto,
  SessionStatusQdto,
  StepOp,
} from "./types";

export interface ApiErrorBody {
  error_code: string;
  message: string;
  hint: string | null;
  config_key?: string | null;
}

export class ApiError extends Error {
  readonly status: number;
  readonly body: ApiErrorBody;

  constructor(status: number, body: ApiErrorBody) {
    super(body.message);
    this.status = status;
    this.body = body;
  }
}

export function parseErrorBody(status: number, raw: unknown): ApiErrorBody {
  if (raw !== null && typeof raw === "object" && "error_code" in raw && "message" in raw) {
    const body = raw as Record<string, unknown>;
    return {
      error_code: String(body.error_code),
      message: String(body.message),
      hint: typeof body.hint === "string" ? body.hint : null,
      config_key: typeof body.config_key === "string" ? body.config_key : null,
    };
  }
  return { error_code: `http_${status}`, message: `请求失败（HTTP ${status}）`, hint: null, config_key: null };
}

export function toApiError(error: unknown): ApiError {
  if (error instanceof ApiError) return error;
  const message = error instanceof Error && error.message ? error.message : "网络错误";
  return new ApiError(0, { error_code: "network_error", message: `无法连接服务：${message}`, hint: "确认服务仍在运行后重试", config_key: null });
}

export async function apiRequest<T>(method: string, path: string, body?: unknown, noStore = false): Promise<T> {
  const response = await fetch(path, {
    method,
    credentials: "same-origin",
    cache: noStore ? "no-store" : undefined,
    headers: body === undefined ? { Accept: "application/json" } : { Accept: "application/json", "Content-Type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await response.text();
  const parsed: unknown = text ? safeJson(text) : null;
  if (!response.ok) throw new ApiError(response.status, parseErrorBody(response.status, parsed));
  return parsed as T;
}

function safeJson(text: string): unknown {
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}

const enc = encodeURIComponent;

function query(params: Array<[string, string | number | null | undefined]>): string {
  const search = new URLSearchParams();
  for (const [key, value] of params) {
    if (value !== null && value !== undefined && value !== "") search.append(key, String(value));
  }
  const text = search.toString();
  return text ? `?${text}` : "";
}

export interface JobListFilter {
  states?: string[];
  batchId?: string | null;
  drama?: string | null;
  since?: string | null;
  page?: number;
  pageSize?: number;
}

export interface HistoryFilter {
  drama?: string;
  shot?: string;
  subject?: string;
  dateFrom?: string;
  dateTo?: string;
  page?: number;
  pageSize?: number;
}

export const api = {
  session: () => apiRequest<SessionStatusQdto>("GET", "/api/session"),
  openBrowser: () => apiRequest<BrowserOpenCdto>("POST", "/api/session/browser/open"),
  startCanary: (backend: string) => apiRequest<OperationCdto>("POST", "/api/operations/canary", { backend }),
  operation: (operationId: string) => apiRequest<OperationQdto>("GET", `/api/operations/${enc(operationId)}`),

  batch: (batchId: string, page: number, pageSize: number) =>
    apiRequest<BatchQdto>("GET", `/api/batches/${enc(batchId)}${query([["page", page], ["page_size", pageSize]])}`),
  confirmation: (batchId: string) => apiRequest<BatchConfirmationQdto>("GET", `/ui-api/batches/${enc(batchId)}/confirmation`, undefined, true),
  confirmBatch: (batchId: string, token: string) =>
    apiRequest<BatchConfirmCdto>("POST", `/ui-api/batches/${enc(batchId)}/confirm`, { token }, true),
  reprecheck: (batchId: string) => apiRequest<BatchPrecheckCdto>("POST", `/api/batches/${enc(batchId)}/reprecheck`, { drop_error_items: true }),

  jobs: (filter: JobListFilter) => {
    const params: Array<[string, string | number | null | undefined]> = (filter.states ?? []).map((state) => ["state", state]);
    params.push(["batch_id", filter.batchId], ["drama", filter.drama], ["since", filter.since], ["page", filter.page], ["page_size", filter.pageSize]);
    return apiRequest<JobPageQdto>("GET", `/api/jobs${query(params)}`);
  },
  job: (jobId: string) => apiRequest<JobDetailQdto>("GET", `/api/jobs/${enc(jobId)}`),
  cancelJob: (jobId: string) => apiRequest<JobStateCdto>("POST", `/api/jobs/${enc(jobId)}/cancel`),
  resumeJob: (jobId: string) => apiRequest<JobStateCdto>("POST", `/api/jobs/${enc(jobId)}/resume`),
  adjudicate: (jobId: string, body: AdjudicationBody) => apiRequest<JobStateCdto>("POST", `/ui-api/jobs/${enc(jobId)}/adjudicate`, body),
  pauseQueue: (backend: string) => apiRequest<QueueStateCdto>("POST", `/api/queues/${enc(backend)}/pause`),
  resumeQueue: (backend: string) => apiRequest<OperationCdto>("POST", `/api/queues/${enc(backend)}/resume`),
  step: (jobId: string, op: StepOp) => apiRequest<OperationCdto>("POST", `/api/jobs/${enc(jobId)}/steps/${op}`),
  stepSubmit: (jobId: string) => apiRequest<OperationCdto>("POST", `/ui-api/jobs/${enc(jobId)}/steps/submit`),
  artifactUrl: (jobId: string, name: string) => `/api/artifacts/${enc(jobId)}/${enc(name)}`,
  thumbUrl: (path: string, maxEdge?: number) => `/api/thumbs${query([["path", path], ["max_edge", maxEdge]])}`,

  dramas: () => apiRequest<DramaTreeQdto>("GET", "/api/dramas"),
  dramaConfig: (drama: string) => apiRequest<DramaConfigQdto>("GET", `/api/dramas/${enc(drama)}/config`),
  proposeConfig: (drama: string) => apiRequest<ProposeCdto>("POST", `/api/dramas/${enc(drama)}/config/propose`),
  saveDramaConfig: (drama: string, body: ConfigSaveBody) => apiRequest<SaveConfigCdto>("PUT", `/api/dramas/${enc(drama)}/config`, body),
  globalConfig: () => apiRequest<GlobalConfigQdto>("GET", "/api/config/global"),
  saveGlobalConfig: (body: ConfigSaveBody) => apiRequest<GlobalConfigSaveCdto>("PUT", "/ui-api/config/global", body),

  entitySync: () => apiRequest<OperationCdto>("POST", "/api/operations/entity-sync"),
  reconcile: (drama?: string) => apiRequest<ReconcileQdto>("GET", `/api/entities/reconcile${query([["drama", drama]])}`),
  createEntityRequest: (dramaRel: string, characterDir: string, description: string | null) =>
    apiRequest<BatchPrecheckCdto>("POST", "/api/entities/create-requests", {
      drama_rel: dramaRel,
      character_dir: characterDir,
      ...(description ? { description } : {}),
    }),

  history: (filter: HistoryFilter) =>
    apiRequest<HistoryPageQdto>(
      "GET",
      `/api/history${query([
        ["drama", filter.drama],
        ["shot", filter.shot],
        ["subject", filter.subject],
        ["date_from", filter.dateFrom],
        ["date_to", filter.dateTo],
        ["page", filter.page],
        ["page_size", filter.pageSize],
      ])}`,
    ),
  dailyTotals: (days: number) => apiRequest<DailyTotalsQdto>("GET", `/api/history/daily${query([["days", days]])}`),
  promote: (candidateRel: string) => apiRequest<PromoteCdto>("POST", "/api/candidates/promote", { candidate_rel: candidateRel }),
};
