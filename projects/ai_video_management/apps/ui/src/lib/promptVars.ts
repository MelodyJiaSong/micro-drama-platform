import { parseConfig } from "../components/PrevizConfigEditor";

/** promptVars — Seedance prompt 模板的变量填充（follow-up 053）。
 *
 * 单一事实源策略：`previz_config.toml` 是唯一可手改的参数源；Blender 建场脚本经
 * `tools/previz_config.py` 读它，Seedance prompt 则把 config 派生的事实写成 `{{占位符}}`
 * 模板，由本模块在 UI 展示/复制时实时填充 —— 三者永不漂移。
 *
 * 占位符语法（键名 = config 叶子键，小写）：
 *   {{key}}            数值/字符串原样（数组按逗号连接）
 *   {{key:zh}}         中文数字（1→一、2→两、3→三…20→二十）
 *   {{key:round}}      四舍五入取整
 *   {{key:inv_frac_zh}} 倒数分数（0.22 → 约五分之一）
 *   {{#key}}           数组长度；{{#key:zh}} 长度中文
 *   {{#key/2}}         数组长度除 2（震两下＝4 个关键拍）；{{#key/2:zh}}
 *
 * 未知键不替换、原样保留并计入 missing —— 显示层标红，绝不静默吞掉。
 */

export type ConfigLeaves = Map<string, number | string | number[]>;

/** 从 previz_config.toml 文本提出「叶子键 → 值」表（键全局唯一，与加载器同契约）。 */
export function extractLeaves(tomlText: string): ConfigLeaves {
  const model = parseConfig(tomlText);
  const leaves: ConfigLeaves = new Map();
  const collect = (keys: { key: string; value: number | string | number[] }[]) => {
    keys.forEach((k) => leaves.set(k.key, k.value));
  };
  collect(model.globals);
  collect(model.camera);
  collect(model.act2);
  model.sections.forEach((sec) => collect(sec.keys));
  model.actions.forEach((a) => { collect(a.meta); a.groups.forEach((g) => collect(g.keys)); });
  model.poses.forEach((p) => collect(p.keys));
  // 时长链（follow-up 057）：total_sec 不再是显式键，由各段 dur_* 相加合成，供 {{total_sec}} 占位符用。
  if (!leaves.has("total_sec")) {
    let sum = 0;
    let found = false;
    leaves.forEach((v, k) => {
      if (k.startsWith("dur_") && typeof v === "number") { sum += v; found = true; }
    });
    if (found) leaves.set("total_sec", Math.round(sum * 100) / 100);
  }
  return leaves;
}

const ZH_DIGITS = ["零", "一", "两", "三", "四", "五", "六", "七", "八", "九"];
const ZH_DIGITS_FORMAL = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"];

/** 口语中文数字：1→一、2→两、10→十、20→二十、25→二十五。支持 0–99。 */
export function zhNumber(n: number): string {
  const v = Math.round(n);
  if (v < 0 || v > 99) return String(v);
  if (v < 10) return ZH_DIGITS[v];
  const tens = Math.floor(v / 10);
  const ones = v % 10;
  const tensPart = tens === 1 ? "十" : `${ZH_DIGITS_FORMAL[tens]}十`;
  return ones === 0 ? tensPart : `${tensPart}${ZH_DIGITS_FORMAL[ones]}`;
}

function invFracZh(v: number): string {
  if (v <= 0 || v >= 1) return String(v);
  return `约${zhNumber(Math.round(1 / v))}分之一`;
}

const VAR_RE = /\{\{(#?)([a-z0-9_]+)(\/2)?(?::(zh|round|int|inv_frac_zh))?\}\}/g;

export interface RenderedVar {
  raw: string;        // 原占位符
  key: string;
  text: string;       // 填充后的文字（missing 时 = raw）
  missing: boolean;
}

export interface PromptRenderResult {
  text: string;               // 填充后的整段文字（copy 用）
  vars: RenderedVar[];        // 逐个替换记录（badge/告警用）
  missing: string[];          // 找不到的键
}

export function renderPromptVars(template: string, leaves: ConfigLeaves | null): PromptRenderResult {
  const vars: RenderedVar[] = [];
  const missing: string[] = [];
  if (!leaves) return { text: template, vars, missing };
  const text = template.replace(VAR_RE, (raw, hash: string, key: string, half: string, filter: string | undefined) => {
    const val = leaves.get(key);
    if (val === undefined) {
      missing.push(key);
      vars.push({ raw, key, text: raw, missing: true });
      return raw;
    }
    let n: number;
    if (hash === "#") {
      n = Array.isArray(val) ? val.length : 1;
    } else if (typeof val === "number") {
      n = val;
    } else if (Array.isArray(val)) {
      const joined = val.join("、");
      vars.push({ raw, key, text: joined, missing: false });
      return joined;
    } else {
      vars.push({ raw, key, text: String(val), missing: false });
      return String(val);
    }
    if (half === "/2") n = n / 2;
    let out: string;
    switch (filter) {
      case "zh": out = zhNumber(n); break;
      case "round": out = String(Math.round(n)); break;
      case "int": out = String(Math.trunc(n)); break;
      case "inv_frac_zh": out = invFracZh(n); break;
      default: out = Number.isInteger(n) ? String(n) : String(Math.round(n * 100) / 100);
    }
    vars.push({ raw, key, text: out, missing: false });
    return out;
  });
  return { text, vars, missing };
}

/** 一段文本是否含模板占位符（决定要不要去拉 config）。 */
export function hasPromptVars(text: string): boolean {
  VAR_RE.lastIndex = 0;
  return VAR_RE.test(text);
}
