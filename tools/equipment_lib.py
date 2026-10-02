# -*- coding: utf-8 -*-
"""装备库 `equipment/` 的唯一定位、编号与装备表（`ai_video.md` rule 4m；2026-09-25 shengji_zhilu follow-up 021）。

装备是与 characters / scenes / props 并列的资产类型——**人物卡只管人**（身体 + 便服底层），手里的兵器、身上的甲、
手上的护腕一律是装备卡，谁在哪一段穿什么由装备表决定：

    {剧}/2_世界观人设/equipment/
        equipment.toml               槽位（顺序 / 空槽怎么反向声明 / 出图怎么陈列）· 品质档（每档的做工语法）· 渲染串出处
        registry.toml                编号唯一出处：key / name_zh / slot / tier（目录名由它派生，不许手改目录）
        [{C}_{分类}/]{C}{S}_{槽位}/e{C}{S}{NN}_{品质}_{名}/
                                     一件装备一个目录：item.toml（内容唯一出处）+ 生成的卡 md + e{…}-{M}_{视图}.png
                                     **层级码**（follow-up 028）：每层目录带号，子层的号以父层的号开头——
                                     e5103 ＝ 5_近战武器 / 51_主手 / 第 03 件，从号码就能一层层找到目录；
                                     分类层可选（equipment.toml 配了 [[category]] 才有，号在 `no`）；槽位号＝它在
                                     该分类 slots 里的序号；各段位数在 [meta] key_digits；同一槽内按品质灰→橙排序号。
                                     条目目录一律按名字判（e{N}_…）递归找，不按深度找
        loadouts/{人物卡目录}.toml    装备表：便服覆盖哪些槽 + 按阶段（等级段 / 集）列身上的装备键
        loadouts/{人物卡目录}.md      由装备表生成的可读表（含每段自动生成的空槽反向声明）

一个字段只写一处：名字 / 槽位 / 品质只在 registry；形制与 prompt 素材只在 item.toml；谁在何时穿只在装备表——
卡上「谁穿」一行由装备表反推，不在 item.toml 里再写一遍。品质词与槽位词是**每部剧自己的配置**（本剧是魔兽的
灰白绿蓝紫橙，仙侠剧可以是凡灵仙神），工具里一个也不写死。

不 import bpy，命令行工具与分镜引擎共用：
    python tools/equipment_lib.py new   <剧里任意路径> <名> <槽位> <品质> [<分类>]   # 领号并登记
    python tools/equipment_lib.py check <剧里任意路径>                       # 只跑闸门
    python tools/equipment_lib.py renumber <剧里任意路径> [--apply]          # 旧键改层级码：搬目录、改图名、registry 记 was
"""
from __future__ import annotations

import copy
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

WORLD = "2_世界观人设"
ROOT_NAME = "equipment"
CONFIG, REGISTRY, ITEM, LOADOUTS = "equipment.toml", "registry.toml", "item.toml", "loadouts"
KEY = re.compile(r"^e(\d+)$")
DIR = re.compile(r"^(e\d+)_([^_]+)_(.+)$")          # e{N}_{品质}_{名}
HEX = re.compile(r"#[0-9a-fA-F]{6}\b")
ITEM_REQUIRED: tuple[str, ...] = ("noun", "family", "size", "subject", "colors", "material", "ornament", "wear", "tell", "lock", "negative")
LOCK_MAX = 30
# 光的写法（follow-up 027）：卡的其余 prompt 字段与负向里凡是写到「光」的短语都要和本档光色对账——
# 实测 e5152（橙）的侧 / 背仍写「冷蓝白光晕」「蓝白电弧」，正面是橙光、侧背是蓝光，三张图就不是同一件
LIGHT_PROMPT_FIELDS: tuple[str, ...] = ("subject", "colors", "material", "ornament", "tell", "side", "back")
LIGHT_PHRASE = re.compile(r"([^，。；、\s]{0,6})(光晕|光芒|(?<![高反])光点|光尘|电弧|火焰(?![纹形状图])|火光|光球|荧光|色光(?![泽洁面滑素亮])|的光(?![泽洁面滑素亮])|发光)")
# 负向里泛禁「光」本身的词（「发光」「光晕」「魔法光芒」）会把蓝紫橙必有的光一起禁掉；火焰 / 电弧只在本件光效用到时才算
GLOW_GENERIC = re.compile(r"发光|光晕|光芒|光效|特效|光点|光尘|荧光|魔法光")
NEGATED = ("不", "没", "无")


@dataclass(frozen=True)
class Slot:
    name: str
    body: str          # 空槽反向声明的主语：「肩上」
    empty: str         # 空着时没有的东西：「护肩」
    display: str       # 正面图怎么陈列
    declare: bool      # 空槽要不要反向声明（衬衣 / 远程这类不声明）


@dataclass(frozen=True)
class Tier:
    name: str
    rank: int
    label: str
    rule: str
    positive: str
    negative: str
    family: dict[str, str]
    glow: str = ""                         # 这一档允许的光色词（空 ＝ 这一档一律不发光）
    glow_forbid: tuple[str, ...] = ()      # 这一档的光里不许出现的别档颜色词
    glow_required: bool = False            # 这一档必须有特效光（蓝紫橙，follow-up 027）
    glow_grammar: str = ""                 # 这一档光芒的强度与形态，并进正面 prompt


@dataclass(frozen=True)
class Category:
    name: str
    slots: tuple[str, ...]                 # 这一类允许的槽位（盾不进布甲、胸甲不进武器类）；槽位号＝这里的序号（1 起）
    classes: str                           # 谁用（只进卡与索引，给人看）
    note: str
    no: int = 0                            # 分类号：目录 `{no}_{name}`、键首位（follow-up 028）


@dataclass(frozen=True)
class Config:
    root: Path
    meta: dict
    slots: tuple[Slot, ...]
    tiers: tuple[Tier, ...]
    categories: tuple[Category, ...] = ()

    def engine_for(self, r: "Row") -> str:
        """这件的三视图走哪家（equipment.toml [meta] elevenlabs_categories / elevenlabs_min_tier）；其余一律即梦。"""
        cats = self.meta.get("elevenlabs_categories", [])
        floor = self.meta.get("elevenlabs_min_tier")
        if floor and r.category in cats and self.tier(r.tier).rank >= self.tier(floor).rank:
            return "elevenlabs"
        return "dreamina"

    @property
    def digits(self) -> tuple[int, ...]:
        """键的各段位数：有分类层是 (分类, 槽位, 序号)，没有是 (槽位, 序号)——[meta] key_digits。"""
        return tuple(self.meta["key_digits"])

    def slot_no(self, category: str, slot: str) -> int:
        order = self.category(category).slots if self.categories else tuple(s.name for s in self.slots)
        return order.index(slot) + 1

    def prefix(self, category: str, slot: str) -> str:
        """层级码里「分类 + 槽位」那一段：5_近战武器 / 51_主手 → "51"。"""
        d = self.digits
        s = f"{self.slot_no(category, slot):0{d[-2]}d}"
        return f"{self.category(category).no:0{d[0]}d}{s}" if self.categories else s

    def cat_dir(self, category: str) -> str:
        return f"{self.category(category).no:0{self.digits[0]}d}_{category}"

    def slot_dir(self, category: str, slot: str) -> str:
        return f"{self.prefix(category, slot)}_{slot}"

    def key(self, category: str, slot: str, nn: int) -> str:
        if not 1 <= nn < 10 ** self.digits[-1]:
            raise SystemExit(f"{self.slot_dir(category, slot)} 的序号 {nn} 超出 {self.digits[-1]} 位——改 [meta] key_digits 再 renumber")
        return f"e{self.prefix(category, slot)}{nn:0{self.digits[-1]}d}"

    def category(self, name: str) -> Category:
        for c in self.categories:
            if c.name == name:
                return c
        raise SystemExit(f"{self.root / CONFIG} 没有分类「{name}」（合法：{'、'.join(c.name for c in self.categories)}）")

    def slot(self, name: str) -> Slot:
        for s in self.slots:
            if s.name == name:
                return s
        raise SystemExit(f"{self.root / CONFIG} 没有槽位「{name}」（合法：{'、'.join(s.name for s in self.slots)}）")

    def tier(self, name: str) -> Tier:
        for t in self.tiers:
            if t.name == name:
                return t
        raise SystemExit(f"{self.root / CONFIG} 没有品质档「{name}」（合法：{'、'.join(t.name for t in self.tiers)}）")

    @property
    def families(self) -> tuple[str, ...]:
        return tuple(self.tiers[0].family) if self.tiers else ()


@dataclass(frozen=True)
class Row:
    key: str
    name_zh: str
    slot: str
    tier: str
    moved_from: tuple[str, ...] = ()
    category: str = ""
    was: str = ""                          # 改层级码前的旧键（follow-up 028）：旧文档 / 旧镜里的 e34 靠它查到今天的号

    @property
    def n(self) -> int:
        return int(KEY.match(self.key).group(1))

    @property
    def dir_name(self) -> str:
        return f"{self.key}_{self.tier}_{self.name_zh}"


@dataclass(frozen=True)
class Stage:
    id: str
    levels: tuple[int, int] | None
    episodes: tuple[str, ...]
    where: str
    wear: tuple[str, ...]
    note: str
    shots: tuple[str, str] | None = None   # 一集内按镜分段（含两端），如 ("S06", "S12")；None ＝ 整集一套
    # 需求等级豁免（follow-up 047）：{键: 理由}——剧里不讲等级（concept G1），剧情需要提前上手时写明理由放行；闸门照样打印，不静默
    level_waiver: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class Loadout:
    character: str
    base: tuple[str, ...]
    base_note: str
    stages: tuple[Stage, ...]
    path: Path


# ─────────────────────────── 定位 ───────────────────────────

def equipment_root(anywhere: Path | str) -> Path:
    """从剧里任意路径（equipment 本身 / 条目目录 / 人物卡 / 2_世界观人设 / 剧根）找到本剧的 equipment/。"""
    p = Path(anywhere).resolve()
    for q in [p, *p.parents]:
        if q.name == ROOT_NAME and (q / CONFIG).is_file():
            return q
        if q.name == WORLD:
            return q / ROOT_NAME
        if (q / WORLD / ROOT_NAME / CONFIG).is_file():
            return q / WORLD / ROOT_NAME
    raise SystemExit(f"{anywhere} 不在任何带 {CONFIG} 的 {ROOT_NAME}/ 之下")


_LOAD_CACHE: dict[tuple[str, int, int], dict] = {}


def _load(p: Path) -> dict:
    """按（路径, 修改时间, 大小）缓存解析结果、返回副本（同一次运行里反复读同一张装备卡）。"""
    if not p.is_file():
        return {}
    st = p.stat()
    k = (str(p), st.st_mtime_ns, st.st_size)
    if k not in _LOAD_CACHE:
        _LOAD_CACHE[k] = tomllib.loads(p.read_text(encoding="utf-8"))
    return copy.deepcopy(_LOAD_CACHE[k])


def config(root: Path) -> Config:
    raw = _load(root / CONFIG)
    if not raw:
        raise SystemExit(f"缺 {root / CONFIG}")
    slots = tuple(Slot(s["name"], s.get("body", ""), s.get("empty", ""), s["display"], bool(s.get("declare", True)))
                  for s in raw.get("slot", []))
    tiers = tuple(Tier(t["name"], int(t["rank"]), t.get("label", ""), t["rule"], t["positive"], t["negative"],
                       dict(t.get("family", {})), t.get("glow", ""), tuple(t.get("glow_forbid", [])),
                       bool(t.get("glow_required", False)), t.get("glow_grammar", ""))
                  for t in raw.get("tier", []))
    cats = tuple(Category(c["name"], tuple(c["slots"]), c.get("classes", ""), c.get("note", ""), int(c.get("no", 0)))
                 for c in raw.get("category", []))
    for c in cats:
        bad = [s for s in c.slots if s not in {x.name for x in slots}]
        if bad:
            raise SystemExit(f"{root / CONFIG}：分类「{c.name}」里的槽位 {bad} 不在 [[slot]] 里")
    # 层级码的入口校验（follow-up 028）：号要唯一、放得进位数，否则目录号与键会对不上
    dig = raw.get("meta", {}).get("key_digits")
    if not dig or len(dig) != (3 if cats else 2):
        raise SystemExit(f"{root / CONFIG}：[meta] key_digits 要写成 {'[分类, 槽位, 序号]' if cats else '[槽位, 序号]'} 的位数")
    nos = [c.no for c in cats]
    if cats and (len(set(nos)) != len(nos) or not all(1 <= n < 10 ** dig[0] for n in nos)):
        raise SystemExit(f"{root / CONFIG}：[[category]] 的 no 要唯一且在 1–{10 ** dig[0] - 1}：{nos}")
    widest = max([len(c.slots) for c in cats] or [len(slots)])
    if widest >= 10 ** dig[-2]:
        raise SystemExit(f"{root / CONFIG}：一类最多 {widest} 个槽位，放不进 {dig[-2]} 位槽位号")
    fams = {tuple(sorted(t.family)) for t in tiers}
    if len(fams) > 1:
        raise SystemExit(f"{root / CONFIG}：各品质档的 family 键不一致——每档都要写全同一组材质族")
    for s in slots:
        if s.declare and not (s.body and s.empty):
            raise SystemExit(f"{root / CONFIG}：槽位「{s.name}」要反向声明却缺 body / empty")
    return Config(root, raw.get("meta", {}), slots, tiers, cats)


# ─────────────────────────── 编号 ───────────────────────────

def registry(root: Path) -> list[Row]:
    return [Row(r["key"], r["name_zh"], r["slot"], r["tier"], tuple(r.get("from", [])), r.get("category", ""), r.get("was", ""))
            for r in _load(root / REGISTRY).get("item", [])]


def _fmt(v) -> str:
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(_fmt(x) for x in v) + "]"
    if isinstance(v, int):
        return str(v)
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'


def write_registry(root: Path, rows: list[Row]) -> None:
    head = ("# 本剧装备编号唯一出处（tools/equipment_lib.py；ai_video.md rule 4m）。新装备用 equipment_lib.allocate() 领号，不许手填。\n"
            "# 键是层级码 e{分类}{槽位}{序号}（follow-up 028）：e5103 ＝ 5_近战武器/51_主手/ 第 03 件；was ＝ 改码前的旧键。\n"
            "# 目录名由本表派生：改名 / 改档只改这里，再跑 tools/gen_equipment.py 搬目录；换槽位 / 换分类要换号（renumber）。\n")
    body = []
    for r in sorted(rows, key=lambda r: r.n):
        body.append("[[item]]\n" + f"key = {_fmt(r.key)}\nname_zh = {_fmt(r.name_zh)}\n"
                    + (f"category = {_fmt(r.category)}\n" if r.category else "")
                    + f"slot = {_fmt(r.slot)}\ntier = {_fmt(r.tier)}\n"
                    + (f"from = {_fmt(list(r.moved_from))}\n" if r.moved_from else "")
                    + (f"was = {_fmt(r.was)}\n" if r.was else ""))
    text = head + "\n" + "\n".join(body)
    tomllib.loads(text)
    (root / REGISTRY).write_text(text, encoding="utf-8", newline="\n")


def allocate(root: Path, name_zh: str, slot: str, tier: str, moved_from: tuple[str, ...] = (), category: str = "") -> str:
    """领本分类本槽位的下一个序号并登记；返回层级码 `e{C}{S}{NN}`。槽位、品质、分类先对 equipment.toml 核。"""
    cfg = config(root)
    cfg.slot(slot)
    cfg.tier(tier)
    if cfg.categories:
        c = cfg.category(category)
        if slot not in c.slots:
            raise SystemExit(f"分类「{category}」不收槽位「{slot}」（收：{'、'.join(c.slots)}）")
    if "_" in name_zh or "_" in tier:
        raise SystemExit(f"名字与品质里不能有下划线（目录名靠它分段）：{name_zh} / {tier}")
    rows = registry(root)
    if any(r.name_zh == name_zh and r.slot == slot for r in rows):
        raise SystemExit(f"「{name_zh}」已在 {slot} 登记——同一件东西全剧只一份")
    pre = cfg.prefix(category, slot)
    used = [int(r.key[1 + len(pre):]) for r in rows if r.key[1:].startswith(pre) and len(r.key) == len(cfg.key(category, slot, 1))]
    key = cfg.key(category, slot, max(used + [0]) + 1)
    rows.append(Row(key, name_zh, slot, tier, moved_from, category))
    write_registry(root, rows)
    return key


def item_dir(root: Path, row: Row, cfg: Config | None = None) -> Path:
    cfg = cfg or config(root)
    base = root / cfg.cat_dir(row.category) if cfg.categories else root
    return base / cfg.slot_dir(row.category, row.slot) / row.dir_name


_INDEX: dict[Path, dict[str, list[Path]]] = {}


def _scan(root: Path) -> dict[str, list[Path]]:
    idx: dict[str, list[Path]] = {}
    for d in root.rglob("e*_*"):
        m = DIR.match(d.name)
        if m and d.is_dir() and LOADOUTS not in d.relative_to(root).parts:
            idx.setdefault(m.group(1), []).append(d)
    _INDEX[root] = idx
    return idx


def find(root: Path, key: str) -> Path | None:
    """e{N} → 它的目录（按目录名判，不按深度）；同号两个目录直接报错。
    一次扫描建索引、缓存；缓存里没有或目录已不在（被搬走 / 删掉）就重扫——370 件时逐件 rglob 要几分钟。"""
    hits = _INDEX.get(root, {}).get(key)
    if not hits or not all(h.is_dir() for h in hits):
        hits = _scan(root).get(key, [])
    if len(hits) > 1:
        raise SystemExit(f"{key} 在 {root} 下有 {len(hits)} 个目录：{[str(h.relative_to(root)) for h in hits]}")
    return hits[0] if hits else None


def row(root: Path, key: str) -> Row:
    for r in registry(root):
        if r.key == key:
            return r
    raise SystemExit(f"{key} 没在 {root / REGISTRY} 登记")


def item(root: Path, key: str) -> dict:
    d = find(root, key)
    if d is None:
        raise SystemExit(f"{key} 没有目录（先跑 tools/gen_equipment.py 建）")
    spec = _load(d / ITEM)
    if not spec:
        raise SystemExit(f"{d / ITEM} 缺失或为空")
    return spec


def carry(root: Path, key: str, mode: str) -> str:
    """item.toml `[carry]` 里的一种拿法（follow-up 042）：扛 / 挎 / 背一律写清手或带子，一处定义、各镜逐字引用。"""
    got = item(root, key).get("carry", {})
    if mode not in got:
        raise SystemExit(f"{key} 的 item.toml [carry] 里没有「{mode}」（有：{'、'.join(got) or '无'}）")
    return got[mode]


def confusable(root: Path, key: str) -> list[str]:
    """item.toml `confusable`：模型容易把它画成的东西（锤 → 斧子）。进 `角色:` 的装备锁与负面词（follow-up 042）。"""
    return [w.strip() for w in re.split(r"[，,、]", item(root, key).get("confusable", "")) if w.strip()]


def lock(root: Path, key: str) -> str:
    """一句话锁定——分镜引擎进 `角色:` 行的装备段，byte-identical。"""
    return item(root, key)["lock"]


# ─────────────────────────── 装备表 ───────────────────────────

def loadout_paths(root: Path) -> list[Path]:
    return sorted((root / LOADOUTS).glob("*.toml"))


def loadout(root: Path, character: str) -> Loadout:
    p = root / LOADOUTS / f"{character}.toml"
    raw = _load(p)
    if not raw:
        raise SystemExit(f"{character} 没有装备表 {p}")
    stages = tuple(Stage(s["id"], tuple(s["levels"]) if s.get("levels") else None, tuple(s.get("episodes", [])),
                         s.get("where", ""), tuple(s.get("wear", [])), s.get("note", ""),
                         tuple(s["shots"]) if s.get("shots") else None,
                         tuple((k, str(v)) for k, v in s.get("level_waiver", {}).items())) for s in raw.get("stage", []))
    return Loadout(raw["character"], tuple(raw.get("base", [])), raw.get("base_note", ""), stages, p)


def shot_n(key: str) -> int:
    """镜号 `S06` / `shot06` / `6` → 6。"""
    return int(re.sub(r"^\D+", "", str(key)))


def stage_for(lo: Loadout, episode: str, shot: str | None = None) -> Stage:
    """一集一套时按集找；一集内按镜分段（阶段带 `shots = ["S06", "S12"]`）时按镜号落到恰好一段。"""
    hits = [s for s in lo.stages if episode in s.episodes]
    if any(s.shots for s in hits):
        if shot is None:
            raise SystemExit(f"{lo.character} 的装备表把 {episode} 按镜分段了，调用方必须给镜号")
        n = shot_n(shot)
        hits = [s for s in hits if s.shots and shot_n(s.shots[0]) <= n <= shot_n(s.shots[1])]
    if len(hits) != 1:
        where = f"{episode} {shot}" if shot else episode
        raise SystemExit(f"{lo.character} 的装备表里 {where} 落在 {len(hits)} 个阶段（应恰好 1 个）：{[s.id for s in hits]}")
    return hits[0]


def covered(root: Path, lo: Loadout, st: Stage) -> dict[str, str]:
    """槽位 → 占它的东西（装备键 / "便服"）。被双手武器挡住的副手不算占着——画面上它确实空着，照样反向声明。"""
    out: dict[str, str] = {s: "便服" for s in lo.base}
    for k in st.wear:
        out[row(root, k).slot] = k
    return out


def empty_clause(root: Path, lo: Loadout, st: Stage) -> str:
    """该阶段看得见却空着的槽 → 正面写死的反向声明（concept C7：不写，模型一定自动补一身甲）。"""
    cfg = config(root)
    cov = covered(root, lo, st)
    parts = [f"{s.body}没有{s.empty}" for s in cfg.slots if s.declare and s.name not in cov]
    for k in st.wear:                    # 单侧装备（原典只有一只的护肩）：另一侧照样反向声明
        one = item(root, k).get("one_side")
        if one:
            s = cfg.slot(row(root, k).slot)
            parts.append(f"{'左' if one == '右' else '右'}{s.body}没有{s.empty}")
    return "、".join(parts)


def wearing(root: Path, character: str, episode: str, shot: str | None = None) -> tuple[Stage, list[str], str]:
    """(阶段, 身上装备键, 空槽反向声明)——分镜引擎的唯一入口。一集内按镜换装的装备表必须给镜号。"""
    lo = loadout(root, character)
    st = stage_for(lo, episode, shot)
    return st, list(st.wear), empty_clause(root, lo, st)


# ─────────────────────────── 闸门 ───────────────────────────

def check_item(root: Path, r: Row, cfg: Config | None = None) -> list[str]:
    """一件装备自己的 item.toml 契约（不看装备表）；并行写卡时各写各的，用它只查自己那几件。"""
    cfg = cfg or config(root)
    d = find(root, r.key)
    spec = _load(d / ITEM) if d else {}
    if not spec:
        return [f"{r.key} {r.name_zh} 缺 {ITEM}"]
    return check_spec(cfg, r, spec)


def check_spec(cfg: Config, r: Row, spec: dict) -> list[str]:
    """item.toml 内容本身的契约——不需要目录与编号，暂存区里还没领号的卡也能查（gen_equipment.py lint）。"""
    errs: list[str] = []
    miss = [k for k in ITEM_REQUIRED if not str(spec.get(k, "")).strip()]
    if miss:
        errs.append(f"{r.key} {ITEM} 缺字段：{'、'.join(miss)}")
    if spec.get("family") not in cfg.families:
        errs.append(f"{r.key} family「{spec.get('family')}」不在品质语法的材质族里：{'、'.join(cfg.families)}")
    if len(spec.get("lock", "")) > LOCK_MAX:
        errs.append(f"{r.key} 一句话锁定 {len(spec['lock'])} 字 > {LOCK_MAX}：{spec['lock']}")
    for k, v in spec.items():
        if isinstance(v, str) and HEX.search(v):
            errs.append(f"{r.key} {ITEM} 的 {k} 里有 hex 色值（用自然色名）")
        if isinstance(v, str) and "**" in v:
            errs.append(f"{r.key} {ITEM} 的 {k} 里有 markdown 粗体（会进 prompt）")
    for b in spec.get("blocks", []):
        if b not in {s.name for s in cfg.slots}:
            errs.append(f"{r.key} blocks 里的「{b}」不是槽位")
    if spec.get("one_side") not in (None, "左", "右"):
        errs.append(f"{r.key} one_side 只能是「左」或「右」")
    # 光与品质色一致（follow-up 024）：灰白绿不发光；蓝紫橙若发光，光色只能是本档颜色
    fx = str(spec.get("effect", "")).strip()
    if cfg.tier(r.tier).glow_required and not fx:
        errs.append(f"{r.key}（{r.tier}）没有写光效 effect——这一档必须有「{cfg.tier(r.tier).glow}」特效光（follow-up 027）")
    if fx:
        t = cfg.tier(r.tier)
        if not t.glow:
            errs.append(f"{r.key}（{r.tier}）写了光效「{fx[:30]}」——这一档不发光，删掉 effect")
        else:
            if t.glow not in fx:
                errs.append(f"{r.key}（{r.tier}）的光效没写本档光色「{t.glow}」：{fx[:40]}")
            wrong = [w for w in t.glow_forbid if w in fx]
            if wrong:
                errs.append(f"{r.key}（{r.tier}）的光效里有别档颜色 {wrong}——发光就必须是「{t.glow}」：{fx[:40]}")
    t = cfg.tier(r.tier)
    for k in LIGHT_PROMPT_FIELDS:
        for pre, word in LIGHT_PHRASE.findall(str(spec.get(k, ""))):
            if any(n in pre for n in NEGATED):
                continue
            if not t.glow:
                errs.append(f"{r.key}（{r.tier}）{k} 里写了光「{pre}{word}」——这一档不发光")
            elif [w for w in t.glow_forbid if w in pre]:
                errs.append(f"{r.key}（{r.tier}）{k} 里的光「{pre}{word}」不是本档光色「{t.glow}」")
    if t.glow:
        for term in str(spec.get("negative", "")).replace(",", "，").split("，"):
            own = GLOW_GENERIC.search(term) or [w for w in ("火焰", "电弧", "火光") if w in term and w in fx]
            if own and not [w for w in t.glow_forbid if w in term]:
                errs.append(f"{r.key}（{r.tier}）负向「{term}」把本档必有的光一起禁掉了——负向只禁别档颜色的光")
    if cfg.categories:
        if not r.category:
            errs.append(f"{r.key} 没有分类（registry 缺 category）")
        elif r.slot not in cfg.category(r.category).slots:
            errs.append(f"{r.key} 分类「{r.category}」不收槽位「{r.slot}」")
    return errs


def check(root: Path) -> list[str]:
    """全部 blocker；空列表 ＝ 过。build 时调用，不过就不写盘。"""
    cfg = config(root)
    errs: list[str] = []
    rows = registry(root)
    seen: dict[str, Row] = {}
    for r in rows:
        if not KEY.match(r.key):
            errs.append(f"{r.key} 不是 e{{数字}}")
        if r.key in seen:
            errs.append(f"{r.key} 重复登记")
        seen[r.key] = r
        if r.slot not in {s.name for s in cfg.slots}:
            errs.append(f"{r.key} 槽位「{r.slot}」不在 {CONFIG}")
        if r.tier not in {t.name for t in cfg.tiers}:
            errs.append(f"{r.key} 品质「{r.tier}」不在 {CONFIG}")
        if "_" in r.name_zh:
            errs.append(f"{r.key} 名字里有下划线：{r.name_zh}")
        if cfg.categories and r.category and r.category not in {c.name for c in cfg.categories}:
            errs.append(f"{r.key} 分类「{r.category}」不在 {CONFIG}")
        elif (r.category or not cfg.categories) and r.slot in {s.name for s in cfg.slots} and \
                (not cfg.categories or r.slot in cfg.category(r.category).slots):
            pre = cfg.prefix(r.category, r.slot)
            if not (r.key[1:].startswith(pre) and len(r.key) == len(cfg.key(r.category, r.slot, 1))):
                errs.append(f"{r.key} {r.name_zh} 不在 {cfg.slot_dir(r.category, r.slot)} 的号段（应是 e{pre}"
                            f"{'N' * cfg.digits[-1]}）——跑 tools/equipment_lib.py renumber")
    for r in rows:
        errs += check_item(root, r, cfg)
    for p in loadout_paths(root):
        lo = loadout(root, p.stem)
        if lo.character != p.stem:
            errs.append(f"{p.name}：character = {lo.character} 与文件名不一致")
        for b in lo.base:
            if b not in {s.name for s in cfg.slots}:
                errs.append(f"{p.name}：便服覆盖的「{b}」不是槽位")
        ids, eps = set(), {}
        spans: dict[str, list[tuple[int, int, str]]] = {}
        for st in lo.stages:
            if st.id in ids:
                errs.append(f"{p.name}：阶段 {st.id} 重复")
            ids.add(st.id)
            for e in st.episodes:
                if st.shots:          # 一集内按镜分段：同集各段的镜号区间不许重叠
                    a, b = shot_n(st.shots[0]), shot_n(st.shots[1])
                    if a > b:
                        errs.append(f"{p.name} {st.id}：shots {st.shots} 起止倒置")
                    for a2, b2, other in spans.get(e, []):
                        if a <= b2 and a2 <= b:
                            errs.append(f"{p.name}：{e} 的 {st.id} {st.shots} 与 {other} 镜号重叠")
                    spans.setdefault(e, []).append((a, b, st.id))
                    if e in eps and eps[e] != "*shots":
                        errs.append(f"{p.name}：{e} 同时有整集阶段 {eps[e]} 与按镜阶段 {st.id}")
                    eps[e] = "*shots"
                    continue
                if e in eps:
                    errs.append(f"{p.name}：{e} 同时落在 {eps[e]} 与 {st.id}")
                eps[e] = st.id
            slots: dict[str, str] = {}
            for k in st.wear:
                if k not in seen:
                    errs.append(f"{p.name} {st.id}：{k} 没登记")
                    continue
                r = seen[k]
                if r.slot in slots:
                    errs.append(f"{p.name} {st.id}：{r.slot} 同时穿着 {slots[r.slot]} 与 {k}")
                slots[r.slot] = k
                d = find(root, k)
                spec = _load(d / ITEM) if d else {}
                req = spec.get("req_level")
                if st.levels and isinstance(req, int) and req > st.levels[1]:
                    why = dict(st.level_waiver).get(k, "").strip()
                    if why:
                        print(f"  ⚠ {p.name} {st.id}：{k} {r.name_zh} 需求 {req} 级、本段 {st.levels[1]} 级——豁免：{why}")
                    else:
                        errs.append(f"{p.name} {st.id}（{st.levels[0]}–{st.levels[1]} 级）：{k} {r.name_zh} 需求 {req} 级，超前"
                                    "（剧情非提前不可就在该段写 level_waiver = {键 = \"理由\"}）")
            for k in st.wear:         # 第二遍：槽位都落定后再查「双手武器挡住的副手」，与列表顺序无关
                d = find(root, k) if k in seen else None
                for b in (_load(d / ITEM) if d else {}).get("blocks", []):
                    if b in slots:
                        errs.append(f"{p.name} {st.id}：{k} 占着{b}，却同时穿着 {slots[b]}")
    return errs


KEY_IN_TEXT = re.compile(r"(?<![A-Za-z0-9_#./\\-])(e\d+)(?![0-9A-Za-z])")


def renumber_plan(root: Path) -> dict[str, str]:
    """旧键 → 层级码。同一分类同一槽位里按品质档（低→高）、再按旧号排序号；已经是层级码的件保持原号。"""
    cfg = config(root)
    rows = registry(root)
    groups: dict[tuple[str, str], list[Row]] = {}
    for r in rows:
        groups.setdefault((r.category, r.slot), []).append(r)
    plan: dict[str, str] = {}
    for (cat, slot), rs in groups.items():
        pre, width = cfg.prefix(cat, slot), len(cfg.key(cat, slot, 1))
        fits = [r for r in rs if r.key[1:].startswith(pre) and len(r.key) == width]
        taken = {int(r.key[1 + len(pre):]) for r in fits}
        nn = 0
        for r in sorted([r for r in rs if r not in fits], key=lambda r: (cfg.tier(r.tier).rank, r.n)):
            nn += 1
            while nn in taken:
                nn += 1
            plan[r.key] = cfg.key(cat, slot, nn)
    return plan


def remap_text(text: str, plan: dict[str, str]) -> str:
    """文本里的旧键（含视图后缀 e34-1、目录名 e34_蓝_…）换成新键；不认识的 e 数字原样留着。"""
    return KEY_IN_TEXT.sub(lambda m: plan.get(m.group(1), m.group(1)), text)


def renumber(root: Path, apply: bool) -> dict[str, str]:
    """把不在自己号段里的件改成层级码：搬目录、改图名与 item.toml 首行、registry 记 was、装备表同步。
    卡 md 与装备表 md 是生成物，搬完删掉旧的、由 gen_equipment.py build 重生。"""
    cfg = config(root)
    plan = renumber_plan(root)
    if not apply:
        return plan
    rows = registry(root)
    for r in rows:
        new = plan.get(r.key)
        if not new:
            continue
        have = find(root, r.key)
        nr = Row(new, r.name_zh, r.slot, r.tier, r.moved_from, r.category, r.was or r.key)
        want = item_dir(root, nr, cfg)
        if have is not None:
            want.parent.mkdir(parents=True, exist_ok=True)
            have.rename(want)
            for f in list(want.iterdir()):
                if f.is_file() and f.name.startswith((f"{r.key}-", f"{r.key}_", f"{r.key}.")):
                    if f.suffix == ".md":
                        f.unlink()
                    else:
                        f.rename(want / (new + f.name[len(r.key):]))
            it = want / ITEM
            if it.is_file():
                t = it.read_text(encoding="utf-8")
                it.write_text(re.sub(rf"^# {r.key} ", f"# {new} ", t, count=1), encoding="utf-8", newline="\n")
    write_registry(root, [Row(plan.get(r.key, r.key), r.name_zh, r.slot, r.tier, r.moved_from, r.category,
                              (r.was or r.key) if r.key in plan else r.was) for r in rows])
    for p in loadout_paths(root):
        p.write_text(remap_text(p.read_text(encoding="utf-8"), plan), encoding="utf-8", newline="\n")
        md = p.with_suffix(".md")
        if md.is_file():
            md.unlink()
    for d in sorted((x for x in root.rglob("*") if x.is_dir()), key=lambda x: -len(x.parts)):
        if LOADOUTS not in d.relative_to(root).parts and not any(d.iterdir()):
            d.rmdir()
    _INDEX.pop(root, None)
    return plan


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if len(a) >= 5 and a[0] == "new":
        print(allocate(equipment_root(a[1]), a[2], a[3], a[4], category=a[5] if len(a) > 5 else ""))
        return 0
    if len(a) >= 2 and a[0] == "renumber":
        root = equipment_root(a[1])
        plan = renumber(root, "--apply" in a)
        for old, new in plan.items():
            print(f"  {old} → {new}")
        print(f"{'已改' if '--apply' in a else '将改'} {len(plan)} 件" + ("" if "--apply" in a else "（加 --apply 执行）"))
        return 0
    if len(a) == 2 and a[0] == "check":
        errs = check(equipment_root(a[1]))
        for e in errs:
            print("  ❌", e)
        print("装备库闸门：", "过" if not errs else f"{len(errs)} 个 blocker")
        return 1 if errs else 0
    raise SystemExit(__doc__.split("不 import bpy", 1)[1])


if __name__ == "__main__":
    raise SystemExit(main())
