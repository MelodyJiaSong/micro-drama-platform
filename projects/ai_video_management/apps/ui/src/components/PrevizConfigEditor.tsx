import { useCallback, useMemo, useState } from "react";

import type { FileResult } from "../types";

/** PrevizConfigEditor — 结构化查看/编辑 previz_config.toml。
 *
 * 为什么不是普通文本编辑器：previz 配置是「动作段 × 段内主体 × 参数」的三层结构
 * （rule 12.16 §8 / follow-up 051），记事本里它是 200+ 行平文本，找一个键要靠肉眼扫。
 * 本组件把 TOML 解析成 段落卡片 + 时间轴条 + 姿态网格，行内注释变成字段说明；
 * 保存时**逐键回写原文本的对应行**（surgical replace），注释与排版一字不动 ——
 * 绝不整档重新序列化，config 文件仍然是人读得懂的那份。
 *
 * 解析的是本仓库 previz_config 的 TOML 子集：[表]、[["数组表"]]、key = 数字/字符串/数组。
 * 解析失败的行原样保留、不可编辑（显示在「未识别行」里），保存不受影响。
 */

// ---------------------------------------------------------------- 解析

interface KeyEntry {
  line: number;          // 行号（0-based）
  key: string;           // 键名（去引号）
  value: number | string | number[];
  kind: "number" | "string" | "array";
  comment: string;       // 行内 # 注释（含前导空白与 #）
  section: string;       // 所属表路径（人读用）
}

interface SubjectGroup {
  subject: string;       // 主体名（酒剑仙/长剑/…）
  keys: KeyEntry[];
}

interface ActionBlock {
  index: number;         // 第几个 [["动作"]]
  name: string;          // "名称"
  start: number | null;  // "起"
  end: number | null;    // "止"
  meta: KeyEntry[];      // 名称/起/止 行
  groups: SubjectGroup[];
}

interface PoseBlock {
  key: string;           // pose_xxx / hand_xxx
  comment: string;       // 表头行内注释（姿态含义）
  keys: KeyEntry[];      // 关节/手指行
}

interface GenericSection {
  name: string;
  comment: string;
  keys: KeyEntry[];
}

interface ConfigModel {
  lines: string[];
  globals: KeyEntry[];   // ["全局"]（旧版细节配置）
  camera: KeyEntry[];    // ["机位"]
  act2: KeyEntry[];      // ["第二幕"]（细节版：只装 act2_t0 等零散键）
  sections: GenericSection[];  // 其余任意表（MVP 版：总览/机位/第一幕/第二幕 都走这里）
  actions: ActionBlock[];
  poses: PoseBlock[];
  headerComments: string[];  // 文件头注释（使用说明）
  unparsed: number[];    // 无法识别的非空行
}

function parseValue(raw: string): { value: number | string | number[]; kind: KeyEntry["kind"] } | null {
  const t = raw.trim();
  if (t.startsWith("[")) {
    const inner = t.slice(1, t.endsWith("]") ? -1 : undefined).trim();
    if (inner === "") return { value: [], kind: "array" };
    const parts = inner.split(",").map((p) => Number(p.trim()));
    if (parts.some((n) => Number.isNaN(n))) return null;
    return { value: parts, kind: "array" };
  }
  if (t.startsWith('"')) {
    const m = /^"((?:[^"\\]|\\.)*)"$/.exec(t);
    if (!m) return null;
    return { value: m[1], kind: "string" };
  }
  const n = Number(t);
  if (!Number.isNaN(n) && t !== "") return { value: n, kind: "number" };
  return null;
}

const KEY_LINE = /^(\s*)("(?:[^"]+)"|[A-Za-z0-9_-]+)\s*=\s*([^#]*?)\s*(#.*)?$/;
const TABLE_LINE = /^\s*(\[\[?)\s*(.+?)\s*\]\]?\s*(#.*)?$/;

function unquote(s: string): string {
  return s.startsWith('"') ? s.slice(1, -1) : s;
}

export function parseConfig(text: string): ConfigModel {
  const lines = text.split("\n");
  const model: ConfigModel = {
    lines, globals: [], camera: [], act2: [], sections: [], actions: [], poses: [],
    headerComments: [], unparsed: [],
  };
  let section = "";            // "全局" | "机位" | "第二幕" | "动作" | "动作.主体" | "姿态.pose_x"
  let curAction: ActionBlock | null = null;
  let curGroup: SubjectGroup | null = null;
  let curPose: PoseBlock | null = null;
  let inHeader = true;

  lines.forEach((line, i) => {
    const trimmed = line.trim();
    if (trimmed === "") return;
    if (trimmed.startsWith("#")) {
      if (inHeader) model.headerComments.push(trimmed.replace(/^#\s?/, ""));
      return;
    }
    const tm = TABLE_LINE.exec(line);
    if (tm) {
      inHeader = false;
      const isArray = tm[1] === "[[";
      const pathParts = tm[2].split(".").map((p) => unquote(p.trim()));
      const head = pathParts[0];
      if (isArray && head === "动作") {
        curAction = {
          index: model.actions.length + 1, name: "", start: null, end: null, meta: [], groups: [],
        };
        model.actions.push(curAction);
        curGroup = null; curPose = null; section = "动作";
        return;
      }
      if (head === "动作" && pathParts.length >= 2 && curAction) {
        curGroup = { subject: pathParts[1], keys: [] };
        curAction.groups.push(curGroup);
        curPose = null; section = `动作.${pathParts[1]}`;
        return;
      }
      if (head === "姿态" && pathParts.length >= 2) {
        curPose = { key: pathParts[1], comment: (tm[3] ?? "").replace(/^#\s?/, ""), keys: [] };
        model.poses.push(curPose);
        curAction = null; curGroup = null; section = `姿态.${pathParts[1]}`;
        return;
      }
      curAction = null; curGroup = null; curPose = null; section = head;
      if (!["全局", "机位", "第二幕"].includes(head)) {
        model.sections.push({ name: head, comment: (tm[3] ?? "").replace(/^#\s?/, ""), keys: [] });
      }
      return;
    }
    const km = KEY_LINE.exec(line);
    if (km) {
      inHeader = false;
      const key = unquote(km[2]);
      const parsed = parseValue(km[3]);
      if (!parsed) { model.unparsed.push(i); return; }
      const entry: KeyEntry = {
        line: i, key, value: parsed.value, kind: parsed.kind,
        comment: (km[4] ?? "").replace(/^#\s?/, ""), section,
      };
      if (curPose) { curPose.keys.push(entry); return; }
      if (curGroup) { curGroup.keys.push(entry); return; }
      if (curAction) {
        curAction.meta.push(entry);
        if (key === "名称" && typeof parsed.value === "string") curAction.name = parsed.value;
        if (key === "起" && typeof parsed.value === "number") curAction.start = parsed.value;
        if (key === "止" && typeof parsed.value === "number") curAction.end = parsed.value;
        return;
      }
      if (section === "全局") { model.globals.push(entry); return; }
      if (section === "机位") { model.camera.push(entry); return; }
      if (section === "第二幕" && model.sections.every((sec) => sec.name !== "第二幕")) { model.act2.push(entry); return; }
      const home = model.sections.find((sec) => sec.name === section);
      if (home) { home.keys.push(entry); return; }
      model.unparsed.push(i);
      return;
    }
    model.unparsed.push(i);
  });
  return model;
}

// ---------------------------------------------------------------- 回写

function formatValue(kind: KeyEntry["kind"], v: number | string | number[]): string {
  if (kind === "array") return `[${(v as number[]).map((n) => formatNum(n)).join(", ")}]`;
  if (kind === "string") return `"${String(v)}"`;
  return formatNum(v as number);
}

function fmtT(n: number): string {
  return String(Math.round(n * 100) / 100);
}

function formatNum(n: number): string {
  if (Number.isInteger(n)) return String(n);
  return String(Math.round(n * 1000) / 1000);
}

/** 把编辑写回原始行：只替换 `=` 与 `#` 之间的值段，键名、缩进、注释都不动。 */
export function applyEdits(text: string, edits: Map<number, { kind: KeyEntry["kind"]; value: number | string | number[] }>): string {
  const lines = text.split("\n");
  edits.forEach(({ kind, value }, lineIdx) => {
    const line = lines[lineIdx];
    const km = KEY_LINE.exec(line);
    if (!km) return;
    const head = `${km[1]}${km[2]} = ${formatValue(kind, value)}`;
    const comment = km[4] ? `${line.includes("  #") ? "  " : " "}${km[4]}` : "";
    lines[lineIdx] = head + comment;
  });
  return lines.join("\n");
}

// ---------------------------------------------------------------- 展示

const SUBJECT_COLORS: Record<string, string> = {
  酒剑仙: "#3fa34d", 长剑: "#3b82d6", 剑群: "#7c6bd6", 酒葫芦: "#d65f5f",
  特效: "#2aa8a8", 机位: "#b8863b",
};

function subjectColor(name: string): string {
  return SUBJECT_COLORS[name] ?? "#8a8a8a";
}

interface FieldProps {
  entry: KeyEntry;
  draft: string | undefined;
  invalid: boolean;
  onChange: (raw: string) => void;
}

/** 单个键的编辑行：键名 + 输入框 + 注释说明。数组以逗号分隔文本编辑。 */
function Field({ entry, draft, invalid, onChange }: FieldProps): JSX.Element {
  const original = entry.kind === "array"
    ? (entry.value as number[]).join(", ")
    : String(entry.value);
  const shown = draft ?? original;
  const dirty = draft !== undefined && draft !== original;
  return (
    <label className={`pvzc-field${dirty ? " pvzc-dirty" : ""}${invalid ? " pvzc-invalid" : ""}`}
      title={entry.comment || entry.key}>
      <span className="pvzc-field-key">{entry.key}</span>
      {entry.kind === "number" ? (
        <input type="number" step={Number.isInteger(entry.value as number) ? 1 : 0.05}
          value={shown} onChange={(e) => onChange(e.target.value)}
          aria-label={`${entry.key}: ${entry.comment}`} />
      ) : (
        <input type="text" value={shown} onChange={(e) => onChange(e.target.value)}
          aria-label={`${entry.key}: ${entry.comment}`}
          className={entry.kind === "array" ? "pvzc-array-input" : "pvzc-text-input"} />
      )}
      {entry.comment ? <span className="pvzc-field-note">{entry.comment}</span> : null}
    </label>
  );
}

// ---------------------------------------------------------------- 高亮 raw 视图

function highlightToml(text: string): JSX.Element[] {
  return text.split("\n").map((line, i) => {
    const trimmed = line.trim();
    let cls = "";
    let content: JSX.Element | string = line;
    if (trimmed.startsWith("#")) cls = "tml-comment";
    else if (TABLE_LINE.test(line)) cls = "tml-table";
    else {
      const km = KEY_LINE.exec(line);
      if (km) {
        content = (
          <>
            <span className="tml-key">{km[1]}{km[2]}</span>
            <span className="tml-eq"> = </span>
            <span className="tml-value">{km[3]}</span>
            {km[4] ? <span className="tml-comment">  {km[4]}</span> : null}
          </>
        );
      }
    }
    return <div key={i} className={`tml-line ${cls}`}><span className="tml-ln">{i + 1}</span>{content}</div>;
  });
}

// ---------------------------------------------------------------- 主组件

interface PrevizConfigEditorProps {
  file: FileResult;
  onSave: (newContent: string) => Promise<void>;
  conflict: { current_mtime: string } | null;
  saveError: Error | null;
  onReload: () => Promise<void>;
}

export function PrevizConfigEditor({ file, onSave, conflict, saveError, onReload }: PrevizConfigEditorProps): JSX.Element {
  const model = useMemo(() => parseConfig(file.content), [file.content]);
  // drafts: lineIdx -> 输入框原始文本；提交时统一解析
  const [drafts, setDrafts] = useState<Map<number, string>>(new Map());
  const [tab, setTab] = useState<"structured" | "raw">("structured");
  const [saving, setSaving] = useState(false);
  const [showHelp, setShowHelp] = useState(false);
  const [posesOpen, setPosesOpen] = useState<Set<string>>(new Set());
  // 左侧导航＝面板切换（follow-up 056）：一次只显示一个区间的设置，不再整页铺开。
  const [activePanel, setActivePanel] = useState<string>("__first__");

  // 时长链（follow-up 057）：每段一个 dur_* 键；段起点 = 前面各段时长之和，总长 = Σ。
  // 用草稿值实时计算——输入框里改时长，顶部时间轴立即跟着变。
  const chain = useMemo(() => {
    const spans: { start: number; end: number; dur: number }[] = [];
    let t = 0;
    model.actions.forEach((a) => {
      const durEntry = a.meta.find((k) => k.key.startsWith("dur_"));
      let dur = durEntry && typeof durEntry.value === "number" ? durEntry.value : 0;
      if (durEntry) {
        const d = drafts.get(durEntry.line);
        if (d !== undefined && !Number.isNaN(Number(d)) && d.trim() !== "") dur = Number(d);
      }
      spans.push({ start: t, end: t + dur, dur });
      t += dur;
    });
    return { spans, total: t };
  }, [model, drafts]);
  const totalSec = useMemo(() => {
    const t = model.globals.find((k) => k.key === "total_sec");
    if (typeof t?.value === "number") return t.value;
    return chain.total > 0 ? chain.total : 30;
  }, [model, chain]);

  const entryByLine = useMemo(() => {
    const m = new Map<number, KeyEntry>();
    const collect = (ks: KeyEntry[]) => ks.forEach((k) => m.set(k.line, k));
    collect(model.globals); collect(model.camera); collect(model.act2);
    model.sections.forEach((sec) => collect(sec.keys));
    model.actions.forEach((a) => { collect(a.meta); a.groups.forEach((g) => collect(g.keys)); });
    model.poses.forEach((p) => collect(p.keys));
    return m;
  }, [model]);

  const parseDraft = useCallback((entry: KeyEntry, raw: string): { ok: boolean; value?: number | string | number[] } => {
    if (entry.kind === "string") return { ok: raw.trim() !== "", value: raw };
    if (entry.kind === "number") {
      const n = Number(raw);
      return Number.isNaN(n) || raw.trim() === "" ? { ok: false } : { ok: true, value: n };
    }
    const parts = raw.split(",").map((p) => Number(p.trim()));
    if (raw.trim() === "" || parts.some((n) => Number.isNaN(n))) return { ok: false };
    return { ok: true, value: parts };
  }, []);

  const invalidLines = useMemo(() => {
    const bad = new Set<number>();
    drafts.forEach((raw, line) => {
      const entry = entryByLine.get(line);
      if (entry && !parseDraft(entry, raw).ok) bad.add(line);
    });
    return bad;
  }, [drafts, entryByLine, parseDraft]);

  const dirtyCount = useMemo(() => {
    let n = 0;
    drafts.forEach((raw, line) => {
      const entry = entryByLine.get(line);
      if (!entry) return;
      const original = entry.kind === "array" ? (entry.value as number[]).join(", ") : String(entry.value);
      if (raw !== original) n += 1;
    });
    return n;
  }, [drafts, entryByLine]);

  // 时长链警告：某段时长 ≤ 0
  const warnings = useMemo(() => {
    const w: string[] = [];
    model.actions.forEach((a, i) => {
      const span = chain.spans[i];
      if (span && span.dur <= 0) w.push(`动作${a.index}「${a.name}」：时长 ${span.dur}s ≤ 0`);
    });
    return w;
  }, [model, chain]);

  const setDraft = useCallback((line: number, raw: string) => {
    setDrafts((prev) => {
      const next = new Map(prev);
      const entry = entryByLine.get(line);
      const original = entry
        ? (entry.kind === "array" ? (entry.value as number[]).join(", ") : String(entry.value))
        : undefined;
      if (raw === original) next.delete(line); else next.set(line, raw);
      return next;
    });
  }, [entryByLine]);

  const doSave = useCallback(async () => {
    if (invalidLines.size > 0 || dirtyCount === 0) return;
    const edits = new Map<number, { kind: KeyEntry["kind"]; value: number | string | number[] }>();
    drafts.forEach((raw, line) => {
      const entry = entryByLine.get(line);
      if (!entry) return;
      const parsed = parseDraft(entry, raw);
      if (parsed.ok && parsed.value !== undefined) edits.set(line, { kind: entry.kind, value: parsed.value });
    });
    setSaving(true);
    try {
      await onSave(applyEdits(file.content, edits));
      setDrafts(new Map());
    } catch {
      /* onSave 已把冲突/错误放进上层 state */
    } finally {
      setSaving(false);
    }
  }, [drafts, entryByLine, invalidLines, dirtyCount, file.content, onSave, parseDraft]);

  const panelIds = useMemo(() => {
    const ids: string[] = [];
    if (model.globals.length > 0) ids.push("globals");
    if (model.camera.length > 0) ids.push("camera");
    model.sections.forEach((sec) => ids.push(`sec:${sec.name}`));
    if (model.act2.length > 0) ids.push("act2");
    model.actions.forEach((a) => ids.push(`action:${a.index}`));
    if (model.poses.length > 0) ids.push("poses");
    return ids;
  }, [model]);
  const current = panelIds.includes(activePanel) ? activePanel : (panelIds[0] ?? "");

  const togglePose = useCallback((key: string) => {
    setPosesOpen((prev) => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key); else next.add(key);
      return next;
    });
  }, []);

  const renderKeys = (keys: KeyEntry[]): JSX.Element => (
    <div className="pvzc-grid">
      {keys.map((k) => (
        <Field key={k.line} entry={k} draft={drafts.get(k.line)}
          invalid={invalidLines.has(k.line)} onChange={(raw) => setDraft(k.line, raw)} />
      ))}
    </div>
  );

  return (
    <div className="pvzc-root">
      {/* ---------- 工具栏 ---------- */}
      <div className="pvzc-toolbar">
        <div className="pvzc-tabs" role="tablist">
          <button type="button" role="tab" aria-selected={tab === "structured"}
            className={tab === "structured" ? "active" : ""} onClick={() => setTab("structured")}>
            🧩 结构视图
          </button>
          <button type="button" role="tab" aria-selected={tab === "raw"}
            className={tab === "raw" ? "active" : ""} onClick={() => setTab("raw")}>
            📄 原文（高亮）
          </button>
        </div>
        <button type="button" className="pvzc-help-btn" onClick={() => setShowHelp((v) => !v)}
          aria-expanded={showHelp}>❓ 键名规则</button>
        <div className="pvzc-toolbar-right">
          {dirtyCount > 0 ? <span className="pvzc-dirty-count">已改 {dirtyCount} 项</span> : null}
          {invalidLines.size > 0 ? <span className="pvzc-invalid-count">{invalidLines.size} 项格式不对</span> : null}
          <button type="button" className="pvzc-save" onClick={() => { void doSave(); }}
            disabled={saving || dirtyCount === 0 || invalidLines.size > 0}>
            {saving ? "保存中…" : "💾 保存"}
          </button>
          {dirtyCount > 0 ? (
            <button type="button" className="pvzc-discard" onClick={() => setDrafts(new Map())}>
              放弃修改
            </button>
          ) : null}
        </div>
      </div>
      {showHelp ? (
        <div className="pvzc-help">
          {model.headerComments.map((c, i) => <div key={i}>{c}</div>)}
        </div>
      ) : null}
      {conflict ? (
        <div className="pvzc-banner pvzc-banner-conflict">
          ⚠ 文件已被别处修改（磁盘版本 {conflict.current_mtime}）。
          <button type="button" onClick={() => { void onReload(); setDrafts(new Map()); }}>重新载入</button>
        </div>
      ) : null}
      {saveError && !conflict ? (
        <div className="pvzc-banner pvzc-banner-error">保存失败：{saveError.message}</div>
      ) : null}
      {warnings.map((w, i) => (
        <div key={i} className="pvzc-banner pvzc-banner-warn">⚠ {w}</div>
      ))}

      {tab === "raw" ? (
        <div className="pvzc-raw">{highlightToml(file.content)}</div>
      ) : (
        <div className="pvzc-body">
          {/* ---------- 左侧导航 ---------- */}
          <nav className="pvzc-nav" aria-label="配置区间切换">
            {model.globals.length > 0 ? (
              <button type="button" className={current === "globals" ? "pvzc-nav-active" : ""}
                onClick={() => setActivePanel("globals")}>⚙ 全局</button>
            ) : null}
            {model.camera.length > 0 ? (
              <button type="button" className={current === "camera" ? "pvzc-nav-active" : ""}
                onClick={() => setActivePanel("camera")}>🎥 机位</button>
            ) : null}
            {model.sections.map((sec) => (
              <button key={sec.name} type="button"
                className={current === `sec:${sec.name}` ? "pvzc-nav-active" : ""}
                onClick={() => setActivePanel(`sec:${sec.name}`)}>📌 {sec.name}</button>
            ))}
            {model.act2.length > 0 ? (
              <button type="button" className={current === "act2" ? "pvzc-nav-active" : ""}
                onClick={() => setActivePanel("act2")}>🎬 第二幕基准</button>
            ) : null}
            {model.actions.map((a) => (
              <button key={a.index} type="button"
                className={`pvzc-nav-action${current === `action:${a.index}` ? " pvzc-nav-active" : ""}`}
                onClick={() => setActivePanel(`action:${a.index}`)}
                title={`${chain.spans[a.index - 1] ? `${fmtT(chain.spans[a.index - 1].start)}–${fmtT(chain.spans[a.index - 1].end)}s` : ""}`}>
                {a.name || `动作${a.index}`}
              </button>
            ))}
            {model.poses.length > 0 ? (
              <button type="button" className={current === "poses" ? "pvzc-nav-active" : ""}
                onClick={() => setActivePanel("poses")}>🧍 姿态库</button>
            ) : null}
          </nav>

          {/* ---------- 主区：时间轴常驻 + 单面板切换 ---------- */}
          <div className="pvzc-main">
            {model.actions.length > 0 ? (
            <section id="pvzc-timeline" className="pvzc-section pvzc-timeline-section">
              <div className="pvzc-chain-total">总长 = 各段时长之和 = <b>{formatNum(totalSec)}s</b></div>
              <div className="pvzc-timeline" role="img"
                aria-label={`时间轴：${model.actions.length} 个区间，总长 ${formatNum(totalSec)} 秒`}>
                {model.actions.map((a) => {
                  const span = chain.spans[a.index - 1];
                  if (!span || span.dur <= 0) return null;
                  const left = (span.start / totalSec) * 100;
                  const width = Math.max((span.dur / totalSec) * 100, 0.6);
                  const active = current === `action:${a.index}`;
                  return (
                    <button key={a.index} type="button"
                      className={`pvzc-timeline-block${active ? " pvzc-timeline-active" : ""}`}
                      style={{ left: `${left}%`, width: `${width}%` }}
                      title={`${a.name}\n${fmtT(span.start)}–${fmtT(span.end)}s（${formatNum(span.dur)}s）`}
                      onClick={() => setActivePanel(`action:${a.index}`)}>
                      <span>{a.index}</span>
                    </button>
                  );
                })}
                {[0, 5, 10, 15, 20, 25].filter((t) => t < totalSec).map((t) => (
                  <span key={t} className="pvzc-timeline-tick" style={{ left: `${(t / totalSec) * 100}%` }}>{t}s</span>
                ))}
              </div>
            </section>
            ) : null}

            {current === "globals" ? (
              <section className="pvzc-section"><h3>⚙ 全局</h3>{renderKeys(model.globals)}</section>
            ) : null}
            {current === "camera" ? (
              <section className="pvzc-section"><h3>🎥 机位</h3>{renderKeys(model.camera)}</section>
            ) : null}
            {model.sections.map((sec) => current === `sec:${sec.name}` ? (
              <section key={sec.name} className="pvzc-section">
                <h3>📌 {sec.name}{sec.comment ? <span className="pvzc-action-range">{sec.comment}</span> : null}</h3>
                {renderKeys(sec.keys)}
              </section>
            ) : null)}
            {current === "act2" ? (
              <section className="pvzc-section"><h3>🎬 第二幕基准</h3>{renderKeys(model.act2)}</section>
            ) : null}
            {model.actions.map((a) => current === `action:${a.index}` ? (
              <section key={a.index} className="pvzc-section pvzc-action">
                <h3>
                  <span className="pvzc-action-index">{a.index}</span>
                  {a.name.replace(/^\d+\s*/, "") || `动作${a.index}`}
                  <span className="pvzc-action-range">
                    {chain.spans[a.index - 1] ? `${fmtT(chain.spans[a.index - 1].start)} – ${fmtT(chain.spans[a.index - 1].end)}s（自动，改时长即顺延）` : ""}
                  </span>
                </h3>
                {renderKeys(a.meta.filter((k) => k.key !== "名称"))}
                {a.groups.map((g) => (
                  <div key={g.subject} className="pvzc-subject">
                    <h4><i style={{ background: subjectColor(g.subject) }} /> {g.subject}</h4>
                    {renderKeys(g.keys)}
                  </div>
                ))}
              </section>
            ) : null)}
            {current === "poses" ? (
              <section className="pvzc-section">
                <h3>🧍 姿态库（{model.poses.length} 个定式）</h3>
                <p className="pvzc-pose-note">
                  关节 = [X, Y, Z] 欧拉角(度)：X 正≈向前抬/前屈，Y ≈向体侧张开，Z ≈扭转。
                </p>
                {model.poses.map((p) => (
                  <div key={p.key} className="pvzc-pose">
                    <button type="button" className="pvzc-pose-head" onClick={() => togglePose(p.key)}
                      aria-expanded={posesOpen.has(p.key)}>
                      <span className="pvzc-pose-caret">{posesOpen.has(p.key) ? "▾" : "▸"}</span>
                      <code>{p.key}</code>
                      <span className="pvzc-pose-desc">{p.comment}</span>
                    </button>
                    {posesOpen.has(p.key) ? renderKeys(p.keys) : null}
                  </div>
                ))}
              </section>
            ) : null}

            {model.unparsed.length > 0 ? (
              <section className="pvzc-section">
                <h3>未识别行（原样保留）</h3>
                <pre className="pvzc-unparsed">
                  {model.unparsed.map((i) => `${i + 1}: ${model.lines[i]}`).join("\n")}
                </pre>
              </section>
            ) : null}
          </div>
        </div>
      )}
    </div>
  );
}
