const JOB_STATES: Record<string, string> = {
  queued: "排队",
  preparing: "准备中",
  submitting: "提交中",
  generating: "渲染中",
  downloading: "下载中",
  done: "完成",
  paused_needs_human: "待人工处理",
  failed: "失败",
  cancelled: "已取消",
};

const REASONS: Record<string, string> = {
  moderation_reject: "审核未通过",
  real_face_rejected: "写实真人素材被拒",
  upload_rejected: "上传被拒",
  fill_mismatch: "填写校验不一致",
  step_failed: "步骤重试耗尽",
  inputs_changed: "确认后参考文件被改动，需要重新预检",
  wait_timeout: "等待超时",
  download_failed: "下载重试耗尽",
  restart_during_submit: "提交过程中服务重启，结果不明",
  submit_rejected: "点击提交后平台拒绝",
  submit_unconfirmed: "提交结果不明",
  estimate_exceeds_confirmed: "页面预计积分超出已确认值",
  cli_error: "CLI 出错",
  login_expired: "登录失效",
  captcha_or_risk_popup: "出现验证码或风控弹窗",
  insufficient_credit: "积分不足",
  page_contract_broken: "页面结构对不上",
  browser_lost: "浏览器窗口丢失",
  cli_login_required: "CLI 未登录",
  compliance_confirmation_required: "需要完成合规确认",
};

const QUEUE_PAUSE_HINTS: Record<string, string> = {
  login_expired: "请在浏览器窗口里重新登录后恢复队列",
  captcha_or_risk_popup: "请在浏览器窗口处理后恢复队列",
  insufficient_credit: "请充值或等待积分到账后恢复队列",
  page_contract_broken: "即梦页面可能已改版，请检查 canary 结果",
  browser_lost: "请打开浏览器窗口后恢复队列",
  cli_login_required: "请在终端运行 dreamina login 后恢复队列",
  compliance_confirmation_required: "请先完成合规确认后恢复队列",
};

const BLOCKED_ON: Record<string, string> = {
  slot: "等待空槽位",
  interval: "等待提交间隔",
  queue_paused: "队列已暂停",
};

const STEPS: Record<string, string> = {
  set_params: "设置参数",
  upload: "上传",
  fill: "填写",
  preview: "预演",
  verify: "校验",
};

const SEVERITY: Record<string, string> = { ok: "正常", warning: "警告", error: "错误" };

const REF_KINDS: Record<string, string> = {
  image: "图片",
  video: "视频",
  audio: "音频",
  entity: "主体",
  first_frame: "首帧",
};

const REF_STATUS: Record<string, string> = {
  found: "已找到",
  not_found: "找不到",
  ambiguous: "多重匹配",
  link_invalid: "链接无效",
  legacy: "旧写法",
};

const RECONCILE: Record<string, string> = {
  mapped: "已映射",
  missing_on_platform: "即梦缺失",
  unmapped_on_platform: "即梦上有但未映射",
};

const LOGIN: Record<string, string> = { logged_in: "已登录", logged_out: "未登录", unknown: "未知" };

const OPERATION_STATES: Record<string, string> = { pending: "等待执行", running: "执行中", succeeded: "成功", failed: "失败" };

const BATCH_STATES: Record<string, string> = {
  awaiting_confirm: "待确认",
  confirmed: "已确认",
  expired: "已过期",
  rejected: "已拒绝",
};

const BACKENDS: Record<string, string> = { web: "web", cli: "CLI" };

const DIFF_CHANGE: Record<string, string> = { added: "新增", removed: "删除", changed: "修改" };

function pick(table: Record<string, string>, value: string | null | undefined, fallback = "—"): string {
  if (value === null || value === undefined || value === "") return fallback;
  return table[value] ?? value;
}

export const label = {
  jobState: (value: string | null | undefined) => pick(JOB_STATES, value),
  reason: (value: string | null | undefined) => pick(REASONS, value),
  queuePauseHint: (value: string | null | undefined) => (value ? QUEUE_PAUSE_HINTS[value] ?? null : null),
  blockedOn: (value: string | null | undefined) => (value && value !== "none" ? BLOCKED_ON[value] ?? value : null),
  step: (value: string | null | undefined) => pick(STEPS, value),
  severity: (value: string | null | undefined) => pick(SEVERITY, value),
  refKind: (value: string | null | undefined) => pick(REF_KINDS, value),
  refStatus: (value: string | null | undefined) => pick(REF_STATUS, value),
  reconcile: (value: string | null | undefined) => pick(RECONCILE, value),
  login: (value: string | null | undefined) => pick(LOGIN, value),
  operationState: (value: string | null | undefined) => pick(OPERATION_STATES, value),
  batchState: (value: string | null | undefined) => pick(BATCH_STATES, value),
  backend: (value: string | null | undefined) => pick(BACKENDS, value),
  diffChange: (value: string | null | undefined) => pick(DIFF_CHANGE, value),
};

export const SEVERITY_ICON: Record<string, string> = { ok: "✓", warning: "⚠", error: "✕" };

export function formatCredits(value: number | null | undefined): string {
  return value === null || value === undefined ? "无法估算" : `${value} 积分`;
}

export function formatSeconds(value: number | null | undefined): string {
  if (value === null || value === undefined) return "—";
  if (value < 60) return `${Math.round(value * 10) / 10} 秒`;
  const minutes = Math.floor(value / 60);
  return `${minutes} 分 ${Math.round(value - minutes * 60)} 秒`;
}

export function text(value: string | number | boolean | null | undefined, fallback = "—"): string {
  if (value === null || value === undefined || value === "") return fallback;
  if (typeof value === "boolean") return value ? "是" : "否";
  return String(value);
}

export function baseName(path: string | null | undefined): string {
  if (!path) return "";
  const parts = path.split("/").filter(Boolean);
  return parts[parts.length - 1] ?? path;
}

const IMAGE_EXT = /\.(png|jpe?g|webp)$/i;

export function isImagePath(path: string | null | undefined): path is string {
  return typeof path === "string" && IMAGE_EXT.test(path);
}
