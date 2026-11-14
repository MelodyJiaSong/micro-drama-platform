/** 开发稿「表格就是图」：把五页里的表解析成 Mermaid 图源和可视化数据（框架 v0.4，xihuan follow-up 003）。
 * 表格解析规则与 ai_videos/xihuan/framework/check.py 的 table() 一致；作者只填表，这里负责画。 */
import { parseSections } from "./devPreview";

export const STAGES = ["开端", "大转折一", "中点", "大转折二", "高潮", "结局"] as const;
const LIB_ID = /(?<![A-Za-z0-9])(?:PL|PS|SC|EL|HL|DK|PR|AU|GD|TR|PH|EV|FL|TL|CL|RC|RS|GF|GR|IR|CF|IT|MT|OR|BS)\d{2}(?![A-Za-z0-9])/g;
const PERSON = /(?<![A-Za-z0-9])P\d+(?![A-Za-z0-9])/g;

/** 小节里第一张表的数据行（去表头、去分隔行），每行拆成单元格。 */
export function parseTable(section = ""): string[][] {
  const rows = section.split("\n").filter(l => l.trimStart().startsWith("|"));
  const cells = rows.map(r => r.trim().replace(/^\|+|\|+$/g, "").split("|").map(c => c.trim().replace(/^\*+|\*+$/g, "").trim()));
  return cells.filter((c, i) => i > 0 && !c.every(x => /^:?-+:?$/.test(x || "-")));
}

/** 小节里的正文（不含表格、标题、注释）。 */
export function prose(section = ""): string {
  return section.split("\n").filter(l => l.trim() && !/^\s*(\||#|<!--|```)/.test(l)).join(" ").trim();
}

export const libIds = (text: string): string[] => [...new Set(text.match(LIB_ID) ?? [])];

/** 人物能力：外在（身体、武艺、法术、技能）与内在（智慧、心志），各一句、各 1–5 分（xihuan follow-up 004）。 */
export interface Ability { outer: string; outerScore: number | null; inner: string; innerScore: number | null }
export interface Person { id: string; name: string; role: string; want: string; flaw: string; ability?: Ability }

const score = (s: string): number | null => (/^[1-5]$/.test(s) ? Number(s) : null);
export interface DevModel {
  theme: Record<string, string>;
  world: { stage: string; groups: { name: string; lib: string; line: string }[]; relations: string[][]; change: string };
  power: { sources: { name: string; lib: string; who: string; cost: string }[]; ladder: { tier: string; who: string }[]; counters: string[][] };
  people: { list: Person[]; relations: string[][] };
  conflict: { main: string; rows: { a: string; what: string; b: string; main: boolean }[]; inner: string };
  secrets: { secret: string; who: string; when: string; change: string }[];
  audience: { core: string; hooks: { kind: string; look: string }[] };
}

const cell = (r: string[], i: number): string => r[i] ?? "";

export function buildModel(pages: Partial<Record<string, string>>): DevModel {
  const s = (p: string): Record<string, string> => parseSections(pages[p] ?? "");
  const w = s("02_世界"), pw = s("03_力量"), pp = s("04_人物"), c = s("05_矛盾"), se = s("06_秘密与伏笔"), au = s("07_观众与爽点");
  return {
    theme: s("01_主题"),
    world: { stage: prose(w["舞台"]), change: prose(w["正在发生的变化"]),
      groups: parseTable(w["种族与势力"]).map(r => ({ name: cell(r, 0), lib: cell(r, 1), line: cell(r, 2) })),
      relations: parseTable(w["关系"]) },
    power: { sources: parseTable(pw["力量源"]).map(r => ({ name: cell(r, 0), lib: cell(r, 1), who: cell(r, 2), cost: cell(r, 3) })),
      ladder: parseTable(pw["强弱阶梯"]).map(r => ({ tier: cell(r, 0), who: cell(r, 1) })), counters: parseTable(pw["克制"]) },
    people: { list: withAbilities(parseTable(pp["人物"]).map(r => ({ id: cell(r, 0), name: cell(r, 1), role: cell(r, 2), want: cell(r, 3), flaw: cell(r, 4) })),
        parseTable(pp["能力"])),
      relations: parseTable(pp["关系"]) },
    conflict: { main: prose(c["主要矛盾"]), inner: prose(c["内在矛盾"]),
      rows: parseTable(c["矛盾图"]).map(r => ({ a: cell(r, 0), what: cell(r, 1), b: cell(r, 2), main: cell(r, 3).startsWith("主") })) },
    secrets: parseTable(se["秘密"]).map(r => ({ secret: cell(r, 0), who: cell(r, 1), when: cell(r, 2), change: cell(r, 3) })),
    audience: { core: prose(au["核心体验"]), hooks: parseTable(au["爽点"]).map(r => ({ kind: cell(r, 0), look: cell(r, 1) })) },
  };
}

function withAbilities(people: Person[], rows: string[][]): Person[] {
  const byId = new Map(rows.map(r => [cell(r, 0), r]));
  return people.map(p => {
    const r = byId.get(p.id);
    return r ? { ...p, ability: { outer: cell(r, 1), outerScore: score(cell(r, 2)), inner: cell(r, 3), innerScore: score(cell(r, 4)) } } : p;
  });
}

/** 内外能力象限图：横轴外在、纵轴内在；同分的人横向错开，主角加粗。 */
export function abilityChart(m: DevModel): string | null {
  const scored = m.people.list.filter(p => p.ability?.outerScore && p.ability.innerScore);
  if (!scored.length) return null;
  const seen = new Map<string, number>();
  const pos = (s: number): number => (s - 0.5) / 5;
  const points = scored.map(p => {
    const a = p.ability!;
    const key = `${a.outerScore}-${a.innerScore}`;
    const k = seen.get(key) ?? 0;
    seen.set(key, k + 1);
    const x = Math.min(0.97, Math.max(0.03, pos(a.outerScore!) + (k % 2 ? -1 : 1) * Math.ceil(k / 2) * 0.05));
    const name = p.name.replace(/["':[\]]/g, "") || p.id;
    const style = p.id === m.people.list[0]?.id ? " radius: 9, color: #b7791f" : " radius: 6";
    return `  "${name}": [${x.toFixed(2)}, ${pos(a.innerScore!).toFixed(2)}]${style}`;
  });
  return ["quadrantChart", '  x-axis "外在弱" --> "外在强"', '  y-axis "内在弱" --> "内在强"',
    '  quadrant-1 "内外皆强"', '  quadrant-2 "内强外弱"', '  quadrant-3 "都还弱"', '  quadrant-4 "外强内弱"', ...points].join("\n");
}

/** 把文字里的人物编号换成名字（图上给人看名字，不看编号）。 */
export function humanize(text: string, people: Person[]): string {
  const names = new Map(people.map(p => [p.id, p.name]));
  return text.replace(PERSON, id => names.get(id) || id);
}

/** 秘密按故事阶段排进时间线；没写阶段的放「未定」。 */
export function secretsByStage(secrets: DevModel["secrets"]): { stage: string; items: DevModel["secrets"] }[] {
  const lanes = [...STAGES, "未定"].map(stage => ({ stage, items: [] as DevModel["secrets"] }));
  for (const x of secrets) (lanes.find(l => x.when.includes(l.stage)) ?? lanes[lanes.length - 1]).items.push(x);
  return lanes.filter(l => l.items.length || l.stage !== "未定");
}

const quote = (s: string): string => `"${s.replace(/"/g, "#quot;").replace(/\s+/g, " ").trim()}"`;
type Shape = "rect" | "round" | "hex" | "stadium";
const wrap: Record<Shape, (l: string) => string> = { rect: l => `[${l}]`, round: l => `(${l})`, hex: l => `{{${l}}}`, stadium: l => `([${l}])` };

class Graph {
  private ids = new Map<string, string>();
  private lines: string[];
  private links = 0;
  private styles: string[] = [];
  constructor(dir: "LR" | "TB", private label: (k: string) => string, private shape: (k: string) => Shape = () => "rect") {
    this.lines = [`flowchart ${dir}`];
  }
  node(key: string): string {
    let id = this.ids.get(key);
    if (!id) {
      id = `n${this.ids.size}`;
      this.ids.set(key, id);
      this.lines.push(`  ${id}${wrap[this.shape(key)](quote(this.label(key) || key))}`);
    }
    return id;
  }
  edge(a: string, b: string, text: string, kind: "arrow" | "thick" | "dotted" = "arrow", style?: string): void {
    const op = { arrow: "-->", thick: "===", dotted: "-.-" }[kind];
    this.lines.push(`  ${this.node(a)} ${op}${text ? `|${quote(text)}|` : ""} ${this.node(b)}`);
    if (style) this.styles.push(`  linkStyle ${this.links} ${style}`);
    this.links += 1;
  }
  hero(key: string | undefined): void {
    const id = key ? this.ids.get(key) : undefined;
    if (id) this.lines.push("  classDef hero fill:#fdf1d6,stroke:#b7791f,stroke-width:2px", `  class ${id} hero`);
  }
  get size(): number { return this.links; }
  toString(): string { return [...this.lines, ...this.styles].join("\n"); }
}

const endpoints = (rows: string[][]): string[][] => rows.filter(r => cell(r, 0) && cell(r, 2));

/** 世界「关系」：种族与势力之间的关系图。 */
export function worldChart(m: DevModel): string | null {
  const g = new Graph("LR", k => k);
  for (const r of endpoints(m.world.relations)) g.edge(r[0], r[2], cell(r, 1));
  return g.size ? g.toString() : null;
}

/** 力量「克制」：克制者 → 被克制。 */
export function counterChart(m: DevModel): string | null {
  const g = new Graph("LR", k => humanize(k, m.people.list));
  for (const r of m.power.counters.filter(r => cell(r, 0) && cell(r, 1))) g.edge(r[0], r[1], "克制");
  return g.size ? g.toString() : null;
}

/** 人物「关系」：主角高亮。 */
export function peopleChart(m: DevModel): string | null {
  const g = new Graph("LR", k => humanize(k, m.people.list), () => "round");
  for (const r of endpoints(m.people.relations)) g.edge(r[0], r[2], cell(r, 1));
  g.hero(m.people.list[0]?.id);
  return g.size ? g.toString() : null;
}

/** 矛盾图：主要矛盾粗红线，次要矛盾虚线；人物圆角，种族 / 势力六边形，力量源（如魔戒）胶囊形。 */
export function conflictChart(m: DevModel): string | null {
  const pids = new Set(m.people.list.map(p => p.id));
  const powers = new Set(m.power.sources.map(s => s.name));
  const g = new Graph("LR", k => humanize(k, m.people.list), k => (pids.has(k) ? "round" : powers.has(k) ? "stadium" : "hex"));
  for (const r of m.conflict.rows.filter(r => r.a && r.b)) {
    g.edge(r.a, r.b, r.what, r.main ? "thick" : "dotted", r.main ? "stroke:#b03a2e,stroke-width:4px" : "stroke:#7d8f88,stroke-width:1.5px");
  }
  g.hero(m.people.list[0]?.id);
  return g.size ? g.toString() : null;
}

/** Markdown 里的 ```mermaid 代码块拆出来单独画。 */
export function splitMermaid(text: string): { kind: "md" | "mermaid"; text: string }[] {
  const out: { kind: "md" | "mermaid"; text: string }[] = [];
  const re = /```mermaid\s*\n([\s\S]*?)```/g;
  let last = 0;
  for (let m = re.exec(text); m; m = re.exec(text)) {
    if (m.index > last) out.push({ kind: "md", text: text.slice(last, m.index) });
    out.push({ kind: "mermaid", text: m[1].trim() });
    last = m.index + m[0].length;
  }
  if (last < text.length) out.push({ kind: "md", text: text.slice(last) });
  return out.filter(p => p.text.trim());
}
