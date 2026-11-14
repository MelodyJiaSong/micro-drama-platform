// 审查机制（chuanyue_yiri follow-up 032/034）：六道关、按法则分工的独立审稿人、结论分类与漏网回路。审稿人排班的唯一源是 .agents/references/project/review_roster.json，这里的 LAWS 只是机制图用的展示数据。
// 结论门槛与登记的检查仍以 qc_checks.toml 为准；每次审查的审稿人清单由 tools/review_run.py 按名册生成。

export const REVIEW_STRATEGY_PATH = "/workflow/qc/strategy";
export const STRATEGY_STATUS = "机制图 · 审稿人排班以 review_roster.json 为准，每次审查生成审查单（follow-up 032 / 034）";

export type StageId = "story" | "filming" | "prompt" | "take" | "cut" | "episode";
export type LawId = "physics" | "character" | "continuity" | "dialogue" | "native_ear" | "era" | "framing" | "audience" | "sound";

export interface Check { text: string; isNew?: boolean }
export interface Stage {
  id: StageId; no: string; name: string; question: string; artifact: string; file: string;
  machine: Check[]; gate: string; human?: string; cost: string;
}
export interface Law { id: LawId; name: string; color: string; rule: string; materials: string; stages: StageId[]; example: string; isNew?: boolean }

export const STAGES: Stage[] = [
  { id: "story", no: "①", name: "故事稿", question: "写之前想清楚", artifact: "故事稿", file: "story.json",
    machine: [{ text: "Vision 与观众原则写了没有（audience_check）" }, { text: "每句台词在镜头时长内说得完", isNew: true }],
    gate: "交用户确定前", human: "用户确定故事稿", cost: "改一句话" },
  { id: "filming", no: "②", name: "分镜", question: "每个动作做得到吗", artifact: "分镜", file: "filming.json",
    machine: [{ text: "俯视站位、视野、人不在墙里（shot_overhead / FOV）" }, { text: "手数预算：自拍镜出现「双手 / 捧 / 掰」就报警", isNew: true },
      { text: "道具状态表逐镜对得上", isNew: true }],
    gate: "编译 Prompt 前", human: "用户确定分镜", cost: "改一句话" },
  { id: "prompt", no: "③", name: "Prompt 与首帧", question: "交给模型的东西对吗", artifact: "资料包", file: "prompt + 参考 + 首帧",
    machine: [{ text: "资料包与参考一致（shot_pack check）" }, { text: "敏感词、禁用词" }, { text: "节拍总长 = 镜头时长" }],
    gate: "提交即梦前；结论绑定 prompt 与参考的哈希", human: "生成永远人点", cost: "重画一张首帧（订阅额度）" },
  { id: "take", no: "④", name: "单条出片", question: "片子本身有没有错", artifact: "出片", file: "renders/<take>.mp4",
    machine: [{ text: "每秒 4 帧拼图 + 手和道具放大图", isNew: true }, { text: "语音识别对词、拉丁语" }, { text: "切镜检测、黑帧、画面文字" }],
    gate: "进剪辑前；任一法则判「重出」就不进", cost: "重出一条 200–300 积分" },
  { id: "cut", no: "⑤", name: "场剪辑", question: "这一场顺不顺", artifact: "场剪辑", file: "edit/final/cut_vN.json",
    machine: [{ text: "不切在词中间" }, { text: "场尾停留 ≥ 1.5 秒" }, { text: "响度；无台词段不提音量" }],
    gate: "拼整集前", cost: "重剪（免费）或回上游重出" },
  { id: "episode", no: "⑥", name: "整集", question: "看完想不想看下一集", artifact: "整集", file: "ep01_final_vN.mp4",
    machine: [{ text: "场间接口：最后一句到转场的间隔" }, { text: "转场时长、头尾淡入淡出" }],
    gate: "锁片前", human: "用户批准锁片", cost: "最贵：可能牵动多场" },
];

export const LAWS: Law[] = [
  { id: "physics", name: "世界物理", color: "#c0502e", isNew: true,
    rule: "重力与支撑、手的数量、道具守恒（不凭空出现或消失）、穿模、身体变形、火光烟水",
    materials: "分镜文字；首帧图；4 fps 拼图 + 手和道具放大图", stages: ["filming", "prompt", "take"],
    example: "面包黏在指尖、剩下的悬空；硬币凭空出现在鼻子上；油灯凭空出现；一条街溶解成另一条街" },
  { id: "character", name: "人物逻辑", color: "#7a4fb0",
    rule: "每个角色一位审稿人，代入自己：我知道什么、想要什么、此刻该看哪、该怎么反应",
    materials: "人物卡、本场目标；拼图", stages: ["story", "filming", "take"],
    example: "Felix 指了左她却往右走，他该有反应；接水女人盯裤子的视线方向" },
  { id: "continuity", name: "连续性", color: "#2f74b5",
    rule: "跨镜的道具状态、服装、光线、站位；账目（钱数）",
    materials: "道具状态表；上一镜尾帧与下一镜首帧", stages: ["filming", "take", "cut", "episode"],
    example: "开场 4 枚小铜钱，后面花了 5 枚；两镜里的油灯形状不同" },
  { id: "dialogue", name: "台词（时长与逻辑）", color: "#1f8a5b",
    rule: "时长内说得完、口型、识别对词、拉丁语与专名、台词前后逻辑（编号、回收）",
    materials: "剧本；语音识别文本；音频", stages: ["story", "prompt", "take"],
    example: "pho 被听成 peanut；台词说到镜头最后一帧，场尾停不住" },
  { id: "native_ear", name: "母语听感", color: "#0f766e", isNew: true,
    rule: "英语母语观众盲听：每句真人会不会这么说，有没有直译句式、电报式、视角时态说不通、讲解腔；尽量换另一个模型审",
    materials: "只给全集台词表 lines.md 和一句画面说明", stages: ["story", "prompt", "take", "episode"],
    example: "结尾「We'll still be reading it two thousand years from now」视角说不通（用户指出，台词审稿人没抓到）" },
  { id: "era", name: "时代与世界观", color: "#8a6d1f",
    rule: "现代物件、史实、系列禁区（不提不拍维苏威）",
    materials: "bible；拼图", stages: ["story", "filming", "prompt", "take"],
    example: "开场坡顶那缕白烟会不会被看成火山" },
  { id: "framing", name: "镜头规格", color: "#476070",
    rule: "节拍对得上秒数、机位取景、一镜到底、人数",
    materials: "规格全文；拼图", stages: ["prompt", "take"],
    example: "镜组里模型自己切的镜，切点和设计不一样" },
  { id: "audience", name: "观众", color: "#c23f7a",
    rule: "不看规格，只说看到了什么、看懂没有、笑点在不在、节奏急不急",
    materials: "只给画面和声音", stages: ["story", "take", "cut", "episode"],
    example: "场间转场太急（用户第一轮就指出）" },
  { id: "sound", name: "声音", color: "#5a7d2a",
    rule: "响度、环境声是否空洞、峰值；声音模块设计好后接上",
    materials: "响度曲线；成片", stages: ["cut", "episode"],
    example: "Convenit 偏响；刮板那镜几乎没有环境声" },
];

export const lawsAt = (stage: StageId): Law[] => LAWS.filter(l => l.stages.includes(stage));

// ---------- 依赖图：谁依赖谁；改了上游，下游哪些结论作废 ----------
export type DepKind = "input" | "artifact" | "plan" | "verdict";
export interface DepNode { id: string; label: string; sub?: string; col: number; row: number; kind: DepKind; isNew?: boolean }
export interface DepEdge { from: string; to: string; kind: "feeds" | "binds" | "gates" }

export const DEP_NODES: DepNode[] = [
  { id: "bible", label: "系列规则", sub: "bible.md", col: 0, row: 0, kind: "input" },
  { id: "chars", label: "人物卡 + 三视图", sub: "characters/", col: 0, row: 1, kind: "input" },
  { id: "bgs", label: "场景卡 + 场景图", sub: "background/", col: 0, row: 2, kind: "input" },
  { id: "props", label: "道具状态表", sub: "每场一张", col: 0, row: 3, kind: "input", isNew: true },
  { id: "story", label: "故事稿", sub: "story.json", col: 1, row: 1, kind: "artifact" },
  { id: "filming", label: "分镜", sub: "filming.json", col: 2, row: 1, kind: "artifact" },
  { id: "overhead", label: "俯视站位图", sub: "planning/", col: 3, row: 0, kind: "plan" },
  { id: "board", label: "镜组板 / 场故事板", sub: "groups/ · board/", col: 3, row: 1, kind: "plan" },
  { id: "ff", label: "首帧图", sub: "stN_first_frame.png", col: 3, row: 2, kind: "plan" },
  { id: "pack", label: "资料包", sub: "prompt + 参考", col: 4, row: 1, kind: "artifact" },
  { id: "take", label: "出片", sub: "renders/<take>", col: 5, row: 1, kind: "artifact" },
  { id: "cut", label: "场剪辑", sub: "cut_vN.json", col: 6, row: 1, kind: "artifact" },
  { id: "ep", label: "整集", sub: "episode join", col: 7, row: 1, kind: "artifact" },
  { id: "v_pre", label: "出片前结论", sub: "qc_pre.json", col: 4, row: 3, kind: "verdict" },
  { id: "v_take", label: "出片结论", sub: "qc.json", col: 5, row: 3, kind: "verdict" },
  { id: "v_cut", label: "剪辑检查", sub: "scene_cut check", col: 6, row: 3, kind: "verdict" },
  { id: "v_ep", label: "整集审片", sub: "锁片前", col: 7, row: 3, kind: "verdict" },
];

export const DEP_EDGES: DepEdge[] = [
  { from: "bible", to: "story", kind: "feeds" }, { from: "chars", to: "story", kind: "feeds" },
  { from: "bible", to: "filming", kind: "feeds" }, { from: "bgs", to: "filming", kind: "feeds" }, { from: "props", to: "filming", kind: "feeds" },
  { from: "story", to: "filming", kind: "feeds" },
  { from: "filming", to: "overhead", kind: "feeds" }, { from: "filming", to: "board", kind: "feeds" }, { from: "board", to: "ff", kind: "feeds" },
  { from: "chars", to: "board", kind: "feeds" }, { from: "bgs", to: "board", kind: "feeds" },
  { from: "filming", to: "pack", kind: "feeds" }, { from: "overhead", to: "pack", kind: "feeds" }, { from: "ff", to: "pack", kind: "feeds" },
  { from: "chars", to: "pack", kind: "feeds" }, { from: "bgs", to: "pack", kind: "feeds" },
  { from: "pack", to: "take", kind: "feeds" }, { from: "take", to: "cut", kind: "feeds" }, { from: "cut", to: "ep", kind: "feeds" },
  { from: "pack", to: "v_pre", kind: "binds" }, { from: "take", to: "v_take", kind: "binds" }, { from: "props", to: "v_take", kind: "feeds" },
  { from: "cut", to: "v_cut", kind: "binds" }, { from: "ep", to: "v_ep", kind: "binds" },
  { from: "v_pre", to: "take", kind: "gates" }, { from: "v_take", to: "cut", kind: "gates" }, { from: "v_cut", to: "ep", kind: "gates" },
];

/** 某节点的全部上游（它依赖谁）与全部下游（改了它，谁要重做或重审）。 */
export function closure(id: string, edges: DepEdge[] = DEP_EDGES): { up: Set<string>; down: Set<string> } {
  const walk = (start: string, next: (e: DepEdge) => [string, string]): Set<string> => {
    const seen = new Set<string>(); const stack = [start];
    while (stack.length) {
      const cur = stack.pop() as string;
      for (const e of edges) {
        const [a, b] = next(e);
        if (a === cur && !seen.has(b)) { seen.add(b); stack.push(b); }
      }
    }
    return seen;
  };
  return { up: walk(id, e => [e.to, e.from]), down: walk(id, e => [e.from, e.to]) };
}

// ---------- 漏网案例：错误从哪关进来、闯过了哪几关、新检查会在哪关拦下 ----------
export interface CaseTrace {
  id: string; title: string; shot: string; origin: StageId; originWhy: string;
  passed: Partial<Record<StageId, string>>; caughtBy: string; caughtAt: StageId | "user";
  newCatch: Partial<Record<StageId, string>>;
}

export const CASES: CaseTrace[] = [
  { id: "bread", title: "面包黏在手上", shot: "s3 st2（第 2 版）", origin: "filming",
    originWhy: "自拍占一只手，分镜却写「双手握着面包掰」：要三只手",
    passed: { prompt: "只查站位和取景的几何", take: "1 fps 小图里指尖捏着像「拿着」；只查凭空出现，没查谁托着", cut: "剪辑只看节奏", episode: "同一模型的子代理，没分工" },
    caughtBy: "用户", caughtAt: "user",
    newCatch: { filming: "手数预算机检 + 物理审稿", prompt: "首帧图数手", take: "放大拼图 + 物理审稿" } },
  { id: "coin", title: "硬币凭空出现在鼻子上", shot: "s4 st2（第 1 版）", origin: "filming",
    originWhy: "分镜没写硬币从哪来，模型自己变出来",
    passed: { take: "我看到了，判成「保留并备注」", cut: "剪辑照用", episode: "没有独立审片" },
    caughtBy: "用户", caughtAt: "user",
    newCatch: { filming: "道具状态表：每件道具写明从哪来", take: "物理审稿；画面错误一律重出" } },
  { id: "lamp", title: "油灯凭空出现、形状不一", shot: "s6 st2（第 2 版）", origin: "filming",
    originWhy: "写了「递给她一盏灯」，没交代灯原来在哪",
    passed: { prompt: "首帧图没画灯", take: "作者自审没注意", cut: "剪辑照用" },
    caughtBy: "整集独立审片", caughtAt: "episode",
    newCatch: { filming: "道具状态表", take: "连续性审稿看上下镜首尾帧" } },
];

// ---------- 结论分类 ----------
export const SEVERITY = [
  { id: "redo", label: "重出", hint: "画面错误，剪不掉" },
  { id: "cut", label: "可剪", hint: "剪掉不丢拍点" },
  { id: "note", label: "记录", hint: "下一版或后期处理" },
  { id: "pass", label: "通过", hint: "" },
] as const;

export const ROLLOUT = [
  { step: "给 Portal Travel 建剧级登记表，接上 qc.py gate", scope: "剧级", needs: "" },
  { step: "qc_review.py 支持镜头 / 镜组出片目录，审稿人按法则分工，结论写四个维度", scope: "工具", needs: "" },
  { step: "新机检：手数预算、道具状态表、4 fps + 手部放大拼图、语音识别对词", scope: "工具", needs: "" },
  { step: "回测：拿 EP01 的 29 条重审，看能否自己抓出面包、硬币、油灯，记下误报", scope: "回测", needs: "" },
  { step: "物理、人物逻辑、台词、连续性升仓库级", scope: "仓库级", needs: "需要用户同意" },
  { step: "单集预览里每条片子显示分类结论与证据", scope: "应用", needs: "" },
];
