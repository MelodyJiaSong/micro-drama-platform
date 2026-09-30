# -*- coding: utf-8 -*-
"""技能库 `skills/` 的唯一定位、读卡、拼施法文字与闸门（ai_video.md rule 45；shengji_zhilu follow-up 053）。

技能与装备一样是全剧一处定义的资产——**每一镜只写「谁、何时、对谁、什么档、成没成」**，施法的样子（每个阶段一句逐字锁定串）、
手势（previz 姿势键）、口令（读条技能一句固定短句 + 定稿录音）、签名音效、技能样片（参考视频）全部从卡里来：

    {剧}/2_世界观人设/skills/
        skills.toml               职业位 · 阶段名 · 法系颜色语法 · 口令政策（每部剧自己的配置，工具里一个也不写死）
        registry.toml             编号唯一出处：key / name / name_en / class / school / level / cast（有没有读条）
        k{职业位}{NN}_{名}/        一个会上屏的技能一个目录（按需建，不预建——装备建了 375 件只用了 17 件）：
            skill.toml            内容唯一出处（时长、姿势、锁定串、档位、口令、声音、样片、谁学会、禁写）
            skill.md              由 skill.toml 生成的可读卡（含样片出片 prompt）
            样片 / 峰值图 / 音效 / 口令录音    定稿后放这里，skill.toml 里写文件名

原典长什么样看 0_research（w25 / w26），本剧定稿写在卡里；偏离原典的地方写 `liberty`，不许悄悄混进「原典如此」。

    python tools/skills_lib.py check  <剧里任意路径>                 # 只跑闸门
    python tools/skills_lib.py md     <剧里任意路径>                 # 重生成全部 skill.md
    python tools/skills_lib.py sample <剧> <键或名> [--no-open]      # 技能样片备料 + 开即梦（「生成」人点）
    python tools/skills_lib.py adopt  <剧> <键或名> <mp4> [--peak 秒] # 选定的样片收进卡、截峰值图、写进 [sample]
"""
from __future__ import annotations

import json
import re
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

WORLD = "2_世界观人设"
ROOT_NAME = "skills"
CONFIG, REGISTRY, CARD, CARD_MD = "skills.toml", "registry.toml", "skill.toml", "skill.md"
KEY = re.compile(r"^k(\d)(\d{2})$")
DIR = re.compile(r"^(k\d{3})_(.+)$")
PHASES: tuple[str, ...] = ("gather", "release", "effect", "linger")
OUTCOMES: tuple[str, ...] = ("成", "断", "空", "挡")      # 成＝放出去生效；断＝蓄到一半被打断；空＝蓄了没出来（学的时候）；挡＝放出去了、被盾 / 光壳挡下
SLOTS: tuple[str, ...] = ("施法者", "目标", "力度")
SCRIPT_KEYS: tuple[str, ...] = ("stance", "hand", "flow")
NAMED_ABSENCE = re.compile(r"没有|不是|别是|不带|不戴|不穿")
FENCE = "`" * 3


class SkillError(SystemExit):
    pass


@dataclass(frozen=True)
class Call:
    text: str                     # 一字不差的口令（英文片）
    zh: str
    at: str                       # 在哪个阶段念：gather / release
    delivery: str                 # 怎么念（低声、平稳…）
    by: tuple[tuple[str, str], ...] = ()      # 个别施法者另有一句：((卡目录, 口令), …)

    def for_caster(self, who: str) -> str:
        return dict(self.by).get(who, self.text)


@dataclass(frozen=True)
class Learned:
    who: str                      # 人物卡目录（没有卡的写称呼）
    ep: str                       # "" ＝ 底子（剧开始前就会）
    shot: str
    teacher: str = ""


@dataclass(frozen=True)
class Card:
    key: str
    name: str
    name_en: str
    cls: str
    school: str
    level: int
    cast: bool                    # 有读条（蓄）＝ True；瞬发＝ False
    dir: Path
    say: tuple[str, ...]
    facts: tuple[str, ...]
    liberty: str
    interrupt: str
    timing: dict[str, tuple[float, float, float]]      # 阶段 → (最短, 默认, 最长) 秒
    pose: dict[str, str]
    look: dict[str, str]
    tier: dict[str, str]
    call: Call | None
    sound: dict[str, str]
    sample_video: str
    sample_still: str
    sample_prompt: str
    learned: tuple[Learned, ...]
    forbid: tuple[str, ...]
    script: dict[str, tuple[str, ...]] = field(default_factory=dict)   # 剧本里施法那一行要写到的：stance / hand / flow（正则，任一命中）
    variants: dict[str, dict] = field(default_factory=dict)
    hue: tuple[float, ...] = ()       # 本卡光的色相带，覆盖法系的（同一法系颜色不同：冲锋暗红、雷霆一击蓝白）
    short: dict[str, str] = field(default_factory=dict)   # 精简稿与跨切重述用的短锁定串（阶段 → 串）；变体的写在 [variant.X.short]
    mark: str = ""                    # 这道光在画面里叫什么（绑定句用，不用技能名）：「暖金色的光和光柱」

    def file(self, name: str) -> Path | None:
        return (self.dir / name) if name and (self.dir / name).is_file() else None


@dataclass(frozen=True)
class Cast:
    """一镜里的一次施放。who / target 写人物卡目录（没有卡的写称呼）；t＝起手时刻（瞬发技能＝出手时刻）。"""
    key: str
    who: str
    target: str = ""
    t: float = 0.0
    tier: str = "熟练"
    outcome: str = "成"
    at_break: float | None = None       # outcome ＝ 断 时，第几秒被打断
    variant: str = ""
    dur: tuple[tuple[str, float], ...] = ()     # 覆盖某阶段时长：(("gather", 3.0),)
    base: str = "站"                             # 施法时的下身（站 / 跪 / 单膝跪…），previz 姿势 ＝ base + 卡里的手势


@dataclass(frozen=True)
class Beat:
    t: float
    phase: str
    text: str


# ─────────────────────────── 定位与读卡 ───────────────────────────

def drama_of(path: Path) -> Path:
    for q in [path.resolve(), *path.resolve().parents]:
        if (q / WORLD).is_dir():
            return q
    raise SkillError(f"{path} 不在一部剧的目录里（找不到 {WORLD}/）")


def root(drama: Path) -> Path:
    return drama / WORLD / ROOT_NAME


def config(drama: Path) -> dict:
    p = root(drama) / CONFIG
    if not p.is_file():
        raise SkillError(f"{drama.name} 没有 {ROOT_NAME}/{CONFIG}")
    return tomllib.loads(p.read_text(encoding="utf-8"))


def registry(drama: Path) -> dict[str, dict]:
    rows = tomllib.loads((root(drama) / REGISTRY).read_text(encoding="utf-8")).get("skill", [])
    out: dict[str, dict] = {}
    for r in rows:
        if not KEY.match(r.get("key", "")):
            raise SkillError(f"registry 键不合法：{r.get('key')!r}（k{{职业位}}{{两位序号}}）")
        if r["key"] in out:
            raise SkillError(f"registry 键重复：{r['key']}")
        out[r["key"]] = r
    return out


def _timing(raw: dict, key: str) -> dict[str, tuple[float, float, float]]:
    out: dict[str, tuple[float, float, float]] = {}
    for ph, v in raw.items():
        if ph not in PHASES:
            raise SkillError(f"{key} [timing] 未知阶段 {ph!r}（只认 {'/'.join(PHASES)}）")
        lo, mid, hi = (float(x) for x in v)
        if not lo <= mid <= hi:
            raise SkillError(f"{key} [timing] {ph} 要写 [最短, 默认, 最长]，得到 {v}")
        out[ph] = (lo, mid, hi)
    return out


def _card(d: Path, reg: dict[str, dict]) -> Card:
    m = DIR.match(d.name)
    key = m.group(1)
    if key not in reg:
        raise SkillError(f"{d.name}：{key} 不在 registry.toml")
    r = reg[key]
    if m.group(2) != r["name"]:
        raise SkillError(f"{d.name}：目录名与 registry 的 name「{r['name']}」不一致（目录名由 registry 派生）")
    raw = tomllib.loads((d / CARD).read_text(encoding="utf-8"))
    extra = set(raw) - {"say", "facts", "liberty", "interrupt", "timing", "pose", "look", "tier", "call", "sound", "sample",
                        "learned", "forbid", "variant", "script", "hue", "short", "mark"}
    if extra:
        raise SkillError(f"{key} skill.toml 有不认识的键 {sorted(extra)}（写了却没人读＝静默失效）")
    c = raw.get("call")
    call = None if not c else Call(c["text"], c.get("zh", ""), c.get("at", "gather"), c.get("delivery", ""),
                                   tuple((str(k), str(v)) for k, v in c.get("by", {}).items()))
    s = raw.get("sample", {})
    return Card(key=key, name=r["name"], name_en=r.get("name_en", ""), cls=r["class"], school=r["school"],
                level=int(r["level"]), cast=bool(r.get("cast", False)), dir=d,
                say=tuple(raw.get("say", [])), facts=tuple(raw.get("facts", [])), liberty=raw.get("liberty", ""),
                interrupt=raw.get("interrupt", ""), timing=_timing(raw.get("timing", {}), key),
                pose=dict(raw.get("pose", {})), look=dict(raw.get("look", {})), tier=dict(raw.get("tier", {})),
                call=call, sound=dict(raw.get("sound", {})), sample_video=s.get("video", ""),
                sample_still=s.get("still", ""), sample_prompt=s.get("prompt", ""),
                learned=tuple(Learned(x["who"], x.get("ep", ""), x.get("shot", ""), x.get("teacher", ""))
                              for x in raw.get("learned", [])),
                forbid=tuple(raw.get("forbid", [])),
                script={k: tuple(v) for k, v in raw.get("script", {}).items()},
                variants=dict(raw.get("variant", {})), hue=tuple(float(x) for x in raw.get("hue", ())),
                short=dict(raw.get("short", {})), mark=raw.get("mark", ""))


def load(drama: Path) -> dict[str, Card]:
    reg = registry(drama)
    cards: dict[str, Card] = {}
    for d in sorted(root(drama).iterdir()):
        if d.is_dir() and DIR.match(d.name) and (d / CARD).is_file():
            c = _card(d, reg)
            cards[c.key] = c
    return cards


def find(cards: dict[str, Card], key_or_name: str) -> Card:
    if key_or_name in cards:
        return cards[key_or_name]
    hit = [c for c in cards.values() if c.name == key_or_name]
    if len(hit) != 1:
        raise SkillError(f"技能「{key_or_name}」没有卡（或重名）——先在 skills/ 建卡（rule 45）")
    return hit[0]


# ─────────────────────────── 拼施法文字 ───────────────────────────

def _fill(text: str, who: str, target: str, force: str) -> str:
    return re.sub(r"\s{2,}", " ", text.replace("{施法者}", who).replace("{目标}", target).replace("{力度}", force))


def durations(card: Card, cast: Cast) -> dict[str, float]:
    over = dict(cast.dur)
    out = {}
    for ph, (lo, mid, hi) in card.timing.items():
        v = float(over.get(ph, mid))
        if not lo <= v <= hi:
            raise SkillError(f"{card.name}：{ph} 写了 {v:g}s，卡里允许 {lo:g}–{hi:g}s（rule 45 时长闸门）")
        out[ph] = v
    return out


def looks(card: Card, cast: Cast, short: bool = False) -> dict[str, str]:
    """这次施放每个阶段的锁定串（变体覆盖卡）；short＝精简稿用的短串：变体改过的阶段只认变体的短串，其余用卡的，没写短串的用全串。"""
    look = dict(card.look)
    var = {}
    if cast.variant:
        if cast.variant not in card.variants:
            raise SkillError(f"{card.name}：没有变体「{cast.variant}」")
        var = card.variants[cast.variant]
        look.update(var.get("look", {}))
    if short:
        for ph in look:
            if ph in var.get("short", {}):
                look[ph] = var["short"][ph]
            elif ph not in var.get("look", {}) and ph in card.short:
                look[ph] = card.short[ph]
    return look


def compose(card: Card, cast: Cast, names: dict[str, str], short: bool = False) -> list[Beat]:
    """一次施放 → 按时刻排好的逐字锁定串。names：卡目录 → 画面里的称呼（亚伦）。short＝用短锁定串（精简稿）。"""
    if cast.outcome not in OUTCOMES:
        raise SkillError(f"{card.name}：outcome 只能是 {'/'.join(OUTCOMES)}，得到 {cast.outcome!r}")
    if cast.tier and cast.tier not in card.tier:
        raise SkillError(f"{card.name}：档位「{cast.tier}」不在卡的 [tier]（{'/'.join(card.tier)}）")
    look = looks(card, cast, short)
    who, target = names.get(cast.who, cast.who), names.get(cast.target, cast.target)
    force = card.tier.get(cast.tier, "")
    d = durations(card, cast)
    beats: list[Beat] = []
    t = cast.t

    def add(ph: str, key: str | None = None) -> None:
        text = look.get(key or ph)
        if text:
            beats.append(Beat(round(t, 2), key or ph, _fill(text, who, target, force)))

    if cast.outcome == "空":                 # 没出来：蓄光那几秒手上本来就没有光，只在该出来的那一刻写「还是空的」；瞬发卡就在出手那一刻
        if not look.get("fizzle"):
            raise SkillError(f"{card.name}：卡里没有 [look] fizzle（没放出来的样子），不能写 outcome＝空")
        if card.cast:
            t += d["gather"]
        add("fizzle", "fizzle")
        return beats
    if card.cast:
        add("gather")
        if cast.outcome == "断":
            if cast.at_break is None or not cast.t < cast.at_break <= cast.t + d["gather"]:
                raise SkillError(f"{card.name}：outcome＝断 要写 at_break，且落在蓄光段 {cast.t:g}–{cast.t + d['gather']:g}s 内")
            t = cast.at_break
            add("interrupt", "interrupt")
            return beats
        t += d["gather"]
    if cast.outcome == "挡":
        if not look.get("blocked"):
            raise SkillError(f"{card.name}：卡里没有 [look] blocked（被挡下的样子），不能写 outcome＝挡")
        add("release")
        t += d.get("release", 0.0)
        add("blocked", "blocked")
        return beats
    for ph in ("release", "effect", "linger"):
        add(ph)
        t += d.get(ph, 0.0)
    return beats


def _gap_words(dt: float) -> str:
    return "随即" if dt < 0.6 else f"约 {dt:g} 秒后"


def chunks(beats: list[Beat], bounds: list[tuple[float, float]]) -> list[str]:
    """一次施放的几拍 → `动作:` 里的时刻分句：同一机位段里的几拍并成一句，段内用相对时间（「约 2.5 秒后」不算时刻，
    免得撞 052 G14 的密度闸门）；跨了切点就在新的机位段另起一句、写绝对时刻（Seedance 2.5 只认整秒，交给压缩器取整）。"""
    def seg(t: float) -> int:
        for i, (a, b) in enumerate(bounds):
            if a - 1e-6 <= t < b - 1e-6:
                return i
        return len(bounds) - 1
    out: list[str] = []
    cur, last_seg, last_t = "", None, 0.0
    for b in beats:
        k = seg(b.t)
        if k != last_seg:
            if cur:
                out.append(cur)
            cur = f"{b.t:g}s {b.text}"
        else:
            cur += f"，{_gap_words(b.t - last_t)}{b.text}"
        last_seg, last_t = k, b.t
    if cur:
        out.append(cur)
    return out


def end_time(card: Card, cast: Cast) -> float:
    d = durations(card, cast)
    if cast.outcome == "断" and cast.at_break is not None:
        return cast.at_break
    tail = {"成": ("release", "effect", "linger"), "挡": ("release", "effect")}.get(cast.outcome, ())
    return cast.t + sum(d.get(ph, 0.0) for ph in (("gather",) if card.cast else ()) + tail)


SELF_PHASES = frozenset({"gather", "release", "interrupt", "fizzle"})    # 光亮在施法者身上（出片回读、排程闸门同一口径）
TARGET_PHASES = frozenset({"effect", "linger"})                           # 光亮在目标身上；blocked 落在挡的人身前
TAIL_S = {"interrupt": 0.5, "fizzle": 1.0}      # 卡 [timing] 不写的收尾阶段在画面里留多久；blocked 按 effect 时长


def phases(card: Card, cast: Cast) -> list[tuple[str, float, float]]:
    """一次施放的阶段时间窗 [(阶段, 起, 止)]，与 compose 同一套时刻；没有外观串的阶段不出（画面里没东西可量）。"""
    beats = compose(card, cast, {})
    d = durations(card, cast)
    out: list[tuple[str, float, float]] = []
    for i, b in enumerate(beats):
        end = b.t + (d.get(b.phase) or TAIL_S.get(b.phase) or (d.get("effect", 0.0) if b.phase == "blocked" else 0.0))
        if i + 1 < len(beats) and beats[i + 1].t > b.t:
            end = min(end, beats[i + 1].t)        # 断：蓄光止于被打断那一刻
        out.append((b.phase, b.t, round(end, 3)))
    return out


RESTATE = "接上段："         # 跨硬切还在的阶段在新机位段开头重述时的前缀（闸门按它回读）
RESTATE_MIN = 0.3            # 阶段在切点两边各留这么久以上才算「跨切」


def restates(card: Card, cast: Cast, names: dict[str, str], cuts: list[float]) -> list[tuple[float, str]]:
    """跨硬切还在的阶段（蓄着的光、光壳、余晖）在新机位段开头重述一次（w28 §3 ① ⑦）：[(切点, 「接上段：短串」)]。"""
    look = looks(card, cast, short=True)
    who, target = names.get(cast.who, cast.who), names.get(cast.target, cast.target)
    force = card.tier.get(cast.tier, "")
    return [(cut, RESTATE + _fill(look[ph], who, target, force))
            for ph, a, b in phases(card, cast) for cut in cuts if a + RESTATE_MIN < cut < b - RESTATE_MIN and look.get(ph)]


MARK_MAX = 16
_LIGHT = re.compile(r"光|火|电|焰|辉|星")


def lit_target(card: Card, cast: Cast) -> bool:
    """目标身上会不会亮：生效 / 余晖的锁定串里写到了目标、又写到了光（冲锋只让目标僵住，不在他身上发光）。"""
    lk = looks(card, cast)
    return any("{目标}" in lk.get(ph, "") and _LIGHT.search(lk.get(ph, "")) for ph in TARGET_PHASES)


def binding_clause(card: Card, cast: Cast, names: dict[str, str]) -> str:
    """一次施法的绑定句（w28 §3 ②）：「{mark}只属于{谁}，落在{目标}身上，只在 a–b 秒」——秒取整（Seedance 只认整秒）。
    没放出来（空）不写：画面里没有光可绑。精简稿【技能】与局部重拍修复单共用。"""
    ph = phases(card, cast)
    if cast.outcome == "空" or not ph:
        return ""
    who, tgt = names.get(cast.who, cast.who), names.get(cast.target, cast.target)
    on_t = bool(tgt) and tgt != who and lit_target(card, cast) and any(p in TARGET_PHASES for p, _, _ in ph)   # 断 / 挡：光没落到目标身上
    a, b = int(ph[0][1]), -int(-max(e for _, _, e in ph) // 1)
    return "%s只属于%s%s，只在%d–%d秒" % (card.mark, who, "，落在%s身上" % tgt if on_t else "", a, b)


BINDING_TAIL = "除了这里写的施法的人和受光的人，画里其他人手上、身上都不发光"


_CASTS_MD = re.compile(r"<!-- casts: (\[.*?\]) -->")


def casts_record(casts: tuple[Cast, ...] | list[Cast]) -> str:
    """shot md 里机读的施放记录（生成器写；后期音效、出片回读用 casts_in 读回）。"""
    return "<!-- casts: " + json.dumps([{"key": c.key, "who": c.who, "target": c.target, "t": c.t, "tier": c.tier, "outcome": c.outcome,
                                         "at_break": c.at_break, "variant": c.variant, "dur": dict(c.dur), "base": c.base}
                                        for c in casts], ensure_ascii=False) + " -->"


def casts_in(md: str) -> list[Cast]:
    m = _CASTS_MD.search(md)
    return [Cast(c["key"], c["who"], c.get("target", ""), float(c["t"]), c.get("tier", "熟练"), c.get("outcome", "成"),
                 c.get("at_break"), c.get("variant", ""), tuple((k, float(v)) for k, v in (c.get("dur") or {}).items()),
                 c.get("base", "站")) for c in (json.loads(m.group(1)) if m else [])]


def _hue(v: object, where: str) -> tuple[float, float, float, float]:
    if not isinstance(v, (list, tuple)) or len(v) != 4:
        raise SkillError(f"{where} hue 要写 [色相 lo°, hi°, 饱和度下限, 亮度下限]，得到 {v!r}")
    lo, hi, s, val = (float(x) for x in v)
    if not (0 <= lo < 360 and 0 <= hi < 360 and 0 <= s <= 1 and 0 <= val <= 1):
        raise SkillError(f"{where} hue 越界：{v!r}（色相 0–360，lo > hi 表示跨 0°；饱和度 / 亮度 0–1）")
    return lo, hi, s, val


def school_hue(drama: Path, school: str) -> tuple[float, float, float, float]:
    """法系光的色相带（skills.toml [school.X] hue）：出片回读按它量光，排程闸门按它判「异色」。"""
    sc = config(drama).get("school", {}).get(school)
    if sc is None or "hue" not in sc:
        raise SkillError(f"法系「{school}」在 skills.toml 没写 hue")
    return _hue(sc["hue"], f"[school.{school}]")


def card_hue(drama: Path, card: Card) -> tuple[float, float, float, float]:
    """这张卡的光的色相带：卡里写了 hue 用卡的，否则用法系的。"""
    return _hue(card.hue, f"{card.key}") if card.hue else school_hue(drama, card.school)


HOLD = 0.2          # 手势段尾提前多少秒钉住（previz 关键帧之间线性插值，不钉就一路慢慢挪）
LEAD = 0.3          # 起手前多少秒钉回原姿势


def poses(card: Card, cast: Cast, label: str = "", lead: bool = True) -> list[tuple[str, float, str]]:
    """previz 关键帧：(施法者称呼, 时刻, 「下身+手势」)。每段手势起止都钉住：蓄光一直端着、放光那一下才举，
    光落下的那段手还举着，余晖里再放下；lead＝起手前 LEAD 秒钉回原姿势（镜表另写了这个人的姿势时由调用方关掉）。"""
    who = label or cast.who
    d = durations(card, cast)
    end = end_time(card, cast)
    segs: list[tuple[float, float, str]] = []
    t = cast.t
    if card.cast and card.pose.get("gather"):
        g_end = cast.at_break if cast.outcome == "断" and cast.at_break is not None else t + d["gather"]
        segs.append((t, g_end, card.pose["gather"]))
    if card.cast:
        t += d["gather"]
    if cast.outcome in ("成", "挡") and card.pose.get("release"):
        segs.append((t, min(end, t + d.get("release", 0.0) + d.get("effect", 0.0)), card.pose["release"]))
    if not segs:
        return []
    out: list[tuple[str, float, str]] = []

    def key(at: float, pose: str) -> None:
        at = round(at, 2)
        if not out or at > out[-1][1] + 1e-6:
            out.append((who, at, pose))
    for i, (a, b, p) in enumerate(segs):
        if i == 0 and lead and a >= LEAD:
            key(a - LEAD, cast.base)
        key(a, f"{cast.base}+{p}")
        nxt = segs[i + 1][0] if i + 1 < len(segs) else end
        key(min(b, nxt) - HOLD, f"{cast.base}+{p}")
    key(end, cast.base)
    return out


def call_line(card: Card, who: str) -> str | None:
    return card.call.for_caster(who) if card.call else None


def sound_cues(card: Card, beats: list[Beat]) -> list[tuple[float, Path]]:
    out = []
    for b in beats:
        f = card.file(card.sound.get(b.phase, ""))
        if f:
            out.append((b.t, f))
    return out


def call_file(card: Card, who: str) -> Path | None:
    """口令定稿录音：卡目录下 {键}_口令_{施法者}.wav（一个施法者录一次，全剧原样用）。"""
    return card.file(f"{card.key}_口令_{who}.wav") if card.call else None


def refs(card: Card, callers: tuple[str, ...] = ()) -> list[tuple[str, Path]]:
    """定稿了的样片 / 峰值图 / 口令录音 → (参考行项名, 文件)。"""
    out = []
    v, s = card.file(card.sample_video), card.file(card.sample_still)
    if v:
        out.append((f"{card.key}_{card.name}样片(技能样片·只取施法动作与光效)", v))
    if s:
        out.append((f"{card.key}_{card.name}峰值(技能峰值图·只取光的形状与颜色)", s))
    for who in dict.fromkeys(callers):
        f = call_file(card, who)
        if f:
            out.append((f"{card.key}_口令_{who}(口令录音·只取念法与节奏)", f))
    return out


def knows(card: Card, who: str, ep: str, shot: str, order: list[str]) -> bool:
    """who 在 ep / shot 时会不会这个技能：底子（ep 空）、学会的那一镜及以后。order＝集的先后。"""
    for ln in card.learned:
        if ln.who != who:
            continue
        if not ln.ep:
            return True
        if order.index(ep) > order.index(ln.ep):
            return True
        if ep == ln.ep and _shot_no(shot) >= _shot_no(ln.shot):
            return True
    return False


def _shot_no(s: str) -> int:
    m = re.search(r"\d+", s or "")
    return int(m.group(0)) if m else 0


# ─────────────────────────── 闸门 ───────────────────────────

def check(drama: Path) -> list[str]:
    bad: list[str] = []
    cfg = config(drama)
    schools = cfg.get("school", {})
    try:
        cards = load(drama)
    except SkillError as e:
        return [str(e)]
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import facts_registry
    facts = facts_registry.load(str(drama))[0]
    for c in cards.values():
        tag = f"{c.key} {c.name}"
        if c.school not in schools:
            bad.append(f"{tag}：法系「{c.school}」不在 skills.toml [school]")
        try:
            card_hue(drama, c)
        except SkillError as e:
            bad.append(f"{tag}：{e}")
        for fid in c.facts:
            f = facts.get(fid)
            if f is None:
                bad.append(f"{tag}：出处 {fid} 没在 0_research 注册")
            elif f.get("verified_by") not in ("human", "ai_read"):
                bad.append(f"{tag}：出处 {fid} 是 {f.get('verified_by')}，没人核过原件")
        need = (("gather", "release") if c.cast else ("release",))
        for ph in need:
            if not c.look.get(ph):
                bad.append(f"{tag}：[look] 缺 {ph}")
            if ph not in c.timing:
                bad.append(f"{tag}：[timing] 缺 {ph}")
        if c.cast and not c.look.get("interrupt"):
            bad.append(f"{tag}：有读条的技能要写 [look] interrupt（被打断的样子）")
        if not c.mark or len(c.mark) > MARK_MAX or NAMED_ABSENCE.search(c.mark):
            bad.append(f"{tag}：mark（这道光叫什么，绑定句用）要写、≤ {MARK_MAX} 字、正面说：{c.mark!r}")
        for k, v in c.short.items():
            if k not in c.look:
                bad.append(f"{tag}：[short] {k} 在 [look] 里没有对应阶段")
        for vn, vv in c.variants.items():
            for k in vv.get("short", {}):
                if k not in vv.get("look", {}) and k not in c.look:
                    bad.append(f"{tag}：[variant.{vn}.short] {k} 在变体与卡的 [look] 里都没有")
            for k in vv.get("look", {}):
                if k in c.short and k not in vv.get("short", {}):
                    bad.append(f"{tag}：变体「{vn}」改了 {k} 的样子却没写短串——精简稿会退回全串（[variant.{vn}.short] 补 {k}）")
        for k, v in (list(c.look.items()) + [(f"{vn}.{k}", v) for vn, vv in c.variants.items() for k, v in vv.get("look", {}).items()]
                     + [(f"short.{k}", v) for k, v in c.short.items()]
                     + [(f"{vn}.short.{k}", v) for vn, vv in c.variants.items() for k, v in vv.get("short", {}).items()]):
            if NAMED_ABSENCE.search(v):
                bad.append(f"{tag}：[look] {k} 写了否定句「{v[:24]}…」——锁定串只写实际有什么（rule 12.4-P）")
            unknown = set(re.findall(r"\{([^}]+)\}", v)) - set(SLOTS)
            if unknown:
                bad.append(f"{tag}：[look] {k} 有未知占位 {sorted(unknown)}（只认 {'/'.join(SLOTS)}）")
        policy = cfg.get("call", {}).get("policy", "")
        if policy == "cast_only":
            if c.cast and c.call is None:
                bad.append(f"{tag}：有读条的技能要有 [call] 口令（口令政策 cast_only）")
            if not c.cast and c.call is not None:
                bad.append(f"{tag}：瞬发技能不念口令（口令政策 cast_only）")
        for ph, fname in c.sound.items():
            if fname and not (c.dir / fname).is_file():
                bad.append(f"{tag}：[sound] {ph} 写了 {fname} 但文件不在")
        for fname in (c.sample_video, c.sample_still):
            if fname and not (c.dir / fname).is_file():
                bad.append(f"{tag}：[sample] 写了 {fname} 但文件不在")
        if not c.learned:
            bad.append(f"{tag}：[[learned]] 为空——谁会这个技能、何时学会只在这里写")
        miss = [k for k in SCRIPT_KEYS if not c.script.get(k)]
        if miss:
            bad.append(f"{tag}：[script] 缺 {'/'.join(miss)}（剧本里施法那一行要写到的起手 / 手 / 光的走向，目标账本 G7c 读这里）")
        for k, pats in c.script.items():
            for pat in pats:
                try:
                    re.compile(pat)
                except re.error as e:
                    bad.append(f"{tag}：[script] {k} 的正则「{pat}」写错了：{e}")
        for p in c.pose.values():
            if p not in _pose_names():
                bad.append(f"{tag}：[pose] 「{p}」不在 build_previz 的 POSES 里")
    return bad


_POSES: set[str] = set()


def _pose_names() -> set[str]:
    if not _POSES:
        src = (Path(__file__).resolve().parent / "previz" / "build_previz.py").read_text(encoding="utf-8")
        body = src[src.index("POSES = {"):]
        body = body[:body.index("\n}\n")]
        _POSES.update(re.findall(r'^\s{4}"([^"]+)":', body, re.M))
    return _POSES


# ─────────────────────────── 可读卡 ───────────────────────────

def render_md(c: Card) -> str:
    phases = {"gather": "蓄", "release": "放", "effect": "生效", "linger": "余", "interrupt": "被打断", "fizzle": "没出来", "blocked": "被挡下"}
    look = "\n".join(f"| {phases.get(k, k)} | {v} |" for k, v in c.look.items())
    timing = "、".join(f"{phases[k]} {lo:g}–{hi:g}s（默认 {mid:g}）" for k, (lo, mid, hi) in c.timing.items())
    learned = "\n".join(f"| {x.who} | {x.ep or '底子'} | {x.shot or '—'} | {x.teacher or '—'} |" for x in c.learned)
    call = ("无（瞬发技能不念口令）" if c.call is None else
            f"「{c.call.text}」（{c.call.zh}）——{ {'gather': '蓄光时', 'release': '放出时'}.get(c.call.at, c.call.at) }念，{c.call.delivery}"
            + "".join(f"；{w} 念「{t}」" for w, t in c.call.by))
    return f"""# {c.key} · {c.name}（{c.name_en}）

> 由 `skill.toml` 生成，别手改（`python tools/skills_lib.py md <剧>`）。技能库规则见 `.claude/agent_refs/project/ai_video.md` rule 45。

| 项 | 内容 |
|---|---|
| 职业 / 法系 / 学会等级 | {c.cls} / {c.school} / {c.level} 级 |
| 读条 | {"有" if c.cast else "瞬发"}；{timing} |
| 台词里的叫法 | {"、".join(c.say) or "—"}（技能名本身不出口） |
| 打断 | {c.interrupt or "—"} |
| 姿势（previz） | {"、".join(f"{phases.get(k, k)}＝{v}" for k, v in c.pose.items()) or "—"} |
| 口令 | {call} |
| 声音 | {"、".join(f"{phases.get(k, k)}＝{v}" for k, v in c.sound.items() if v) or "未定稿（后期不贴）"} |
| 样片 / 峰值图 | {c.sample_video or "未定稿"} / {c.sample_still or "未定稿"} |
| 原典出处 | {"、".join(c.facts) or "—"} |
| 本剧偏离 | {c.liberty or "无"} |
| 禁写 | {"、".join(c.forbid) or "—"} |

## 锁定串（逐字进 prompt；{{施法者}} {{目标}} {{力度}} 由生成器填）

| 阶段 | 锁定串 |
|---|---|
{look}

档位（只换强弱词）：{"、".join(f"{k}＝「{v or '（不加）'}」" for k, v in c.tier.items())}

## 谁会

| 谁 | 学会的集 | 镜 | 老师 |
|---|---|---|---|
{learned}

## 技能样片出片 prompt（即梦 · 全能参考 · 定稿一条后写进 skill.toml [sample] video）

{FENCE}text
{c.sample_prompt or "（未写）"}
{FENCE}
"""


SAMPLE_DIR = "样片"


def sample_kit(drama: Path, card: Card, open_web: bool = True) -> Path:
    """技能样片备料：prompt 写进卡目录 样片/prompt.txt、进剪贴板、在本剧 seedance.toml 的 Chrome 账号开即梦；「生成」永远人点。"""
    import subprocess
    if not card.sample_prompt:
        raise SkillError(f"{card.key} {card.name}：[sample] prompt 还没写")
    kd = card.dir / SAMPLE_DIR
    kd.mkdir(exist_ok=True)
    (kd / "prompt.txt").write_text(card.sample_prompt + "\n", encoding="utf-8")
    (kd / "使用说明.txt").write_text(
        f"{card.key} {card.name} 技能样片（tools/skills_lib.py sample 生成，别手改）\n\n"
        "1. 即梦 → 视频生成 → 全能参考，不挂任何参考素材，粘贴 prompt（已在剪贴板）。\n"
        "2. 抽 3–4 条，挑施法动作与光效最干净、最像卡里锁定串的一条；有字、有人脸、光的颜色或形状不对的都不要。\n"
        f"3. 下载后跑：python tools/skills_lib.py adopt <剧> {card.key} <下载的 mp4> [--peak 秒]\n"
        "   —— 它把视频收进卡目录、截峰值定帧图、写进 skill.toml [sample]；此后每个用到这个技能的镜自动挂上。\n",
        encoding="utf-8")
    if open_web:
        import seedance_kit
        cfg = seedance_kit.config(drama)
        subprocess.run(["powershell", "-NoProfile", "-Command",
                        f"Get-Content -Raw -Encoding UTF8 -LiteralPath '{kd / 'prompt.txt'}' | Set-Clipboard"], check=True)
        subprocess.Popen([str(seedance_kit.CHROME), f"--profile-directory={seedance_kit.chrome_profile_dir(cfg['chrome_profile'])}", cfg["url"]])
    return kd


def adopt(drama: Path, card: Card, video: Path, peak: float | None) -> tuple[Path, Path]:
    """选定的样片收进卡目录（{key}_样片.mp4）+ 峰值定帧（{key}_峰值.png），并写进 skill.toml [sample]。"""
    import shutil
    import subprocess
    if not video.is_file():
        raise SkillError(f"没有这个文件：{video}")
    dst = card.dir / f"{card.key}_样片{video.suffix.lower()}"
    shutil.copy2(video, dst)
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(dst)],
                           capture_output=True, text=True)
    secs = float(probe.stdout.strip() or 0)
    if not 2.0 <= secs <= 15.0:
        raise SkillError(f"样片 {secs:.1f}s：Seedance 参考视频每段要 2–15 s（rule 24）")
    at = peak if peak is not None else secs * 0.6
    still = card.dir / f"{card.key}_峰值.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{at:.2f}", "-i", str(dst), "-frames:v", "1", str(still)], check=True)
    toml = card.dir / CARD
    text = toml.read_text(encoding="utf-8")
    text = re.sub(r'^video = ".*"$', f'video = "{dst.name}"', text, count=1, flags=re.M)
    text = re.sub(r'^still = ".*"$', f'still = "{still.name}"', text, count=1, flags=re.M)
    toml.write_text(text, encoding="utf-8")
    return dst, still


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    cmds = ("check", "md", "sample", "adopt")
    if len(sys.argv) < 3 or sys.argv[1] not in cmds:
        print(__doc__)
        return 2
    drama = drama_of(Path(sys.argv[2]))
    if sys.argv[1] == "md":
        for c in load(drama).values():
            (c.dir / CARD_MD).write_text(render_md(c), encoding="utf-8")
        print(f"已重生成 {len(load(drama))} 张 skill.md")
        return 0
    if sys.argv[1] == "sample":
        card = find(load(drama), sys.argv[3])
        kd = sample_kit(drama, card, "--no-open" not in sys.argv)
        print((kd / "使用说明.txt").read_text(encoding="utf-8"))
        return 0
    if sys.argv[1] == "adopt":
        card = find(load(drama), sys.argv[3])
        peak = float(sys.argv[sys.argv.index("--peak") + 1]) if "--peak" in sys.argv else None
        dst, still = adopt(drama, card, Path(sys.argv[4]), peak)
        (card.dir / CARD_MD).write_text(render_md(find(load(drama), card.key)), encoding="utf-8")
        print(f"已收进 {dst.name} 与 {still.name}；此后用到 {card.name} 的镜自动挂上样片与峰值图")
        return 0
    bad = check(drama)
    for b in bad:
        print("  ✗ " + b)
    print(f"技能库：{len(load(drama)) if not bad or 'registry' not in bad[0] else '?'} 张卡，{len(bad)} 个问题")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
