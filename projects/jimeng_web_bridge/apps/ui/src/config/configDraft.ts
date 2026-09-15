export type ConfigData = Record<string, unknown>;

const BARE_KEY = /^[A-Za-z0-9_-]+$/;

/** Same dotted form the server uses for `field_path` / `config_key` (libs/domain/value_objects/config_table__valueobject.py::key_path). */
export function keyPath(segments: readonly string[]): string {
  return segments.map((segment) => (BARE_KEY.test(segment) ? segment : `"${segment}"`)).join(".");
}

export function isTable(value: unknown): value is ConfigData {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

export function cloneData<T>(value: T): T {
  return JSON.parse(JSON.stringify(value)) as T;
}

export function getIn(data: ConfigData, path: readonly string[]): unknown {
  let current: unknown = data;
  for (const segment of path) {
    if (!isTable(current)) return undefined;
    current = current[segment];
  }
  return current;
}

export function setIn(data: ConfigData, path: readonly string[], value: unknown): ConfigData {
  const [head, ...rest] = path;
  const copy: ConfigData = { ...data };
  if (rest.length === 0) {
    if (value === undefined) delete copy[head];
    else copy[head] = value;
    return copy;
  }
  const child = isTable(copy[head]) ? (copy[head] as ConfigData) : {};
  copy[head] = setIn(child, rest, value);
  return copy;
}

const identities = new WeakMap<object, number>();
let nextIdentity = 0;

/** Stable per-object number, used to remount an editor whenever a fresh server copy arrives. */
export function identityKey(value: object): number {
  let id = identities.get(value);
  if (id === undefined) {
    nextIdentity += 1;
    id = nextIdentity;
    identities.set(value, id);
  }
  return id;
}

export function formatValue(value: unknown): string {
  if (value === undefined || value === null) return "（无）";
  if (typeof value === "string") return value;
  return JSON.stringify(value);
}

export function focusConfigKey(path: string): boolean {
  const target = Array.from(document.querySelectorAll<HTMLElement>("[data-config-key]")).find(
    (element) => element.getAttribute("data-config-key") === path,
  );
  if (!target) return false;
  target.focus();
  return true;
}

export interface NumberRule {
  integer?: boolean;
  min?: number;
  max?: number;
}

export function numberProblem(value: unknown, rule: NumberRule): string | null {
  if (value === undefined) return null;
  if (typeof value !== "number" || !Number.isFinite(value)) return "必须是数字";
  if (rule.integer && !Number.isInteger(value)) return "必须是整数";
  if (rule.min !== undefined && value < rule.min) return `不能小于 ${rule.min}`;
  if (rule.max !== undefined && value > rule.max) return `不能大于 ${rule.max}`;
  return null;
}
