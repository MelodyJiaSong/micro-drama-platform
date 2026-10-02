# -*- coding: utf-8 -*-
"""看上下文的逐拍逻辑检测（follow-up 034：S03 杜克走着走着就摔了、路上看不到他在跑）。不 import bpy，生成器在 build 时调。

四条都只看「写出来的动作」与「平面图上的运动」，不靠审美：
  L1 速度词 ↔ 平面图：写了跑 / 冲上 / 拔腿，这个人在这一拍里平面图上得真跑起来（≥ RUN_MIN）；写走的不能快过 WALK_MAX。
  L2 结果要有原因：摔倒 / 喘 / 逃 / 愣住……同一拍里在它前面、或上一拍（第一拍看上一镜最后一拍）得有原因词；
     喘也认平面图上的「前 3 秒里跑过」。摔倒只认外力（撞 / 推 / 砸空 / 被拽 / 湿滑地面）或本镜生效、severity＝行动受限的伤——
     跑着、一绊、一脚踩空都不算（follow-up 035：敦实的杜克在三级台阶上自己扑倒，补一口没破皮的狼咬当原因也不算）。
  L3 状态账本：`4_剧本/episodes/{ep}/states.toml` 登记的伤 / 状态，在 (from, to] 的每一镜里都得写到（show 里任一个词）。
  L3b 伤必须登记：动作里有人被咬 / 被砍 / 擦伤…，就得在账本里有 who＝此人、from＝本镜的一条（带不带到下一镜都要声明）。
  L3c 伤势配得上后果（check_states）：severity ∈ SEVERITY；写着挡住 / 没伤到的只能是无碍，无碍的当场就过去（to＝from、show 空）；
      show 里有瘸 / 腿软这类词，severity 须是行动受限。
  L3d 瘸要有伤：动作里写谁瘸 / 拖着腿，这个人本镜得有生效的行动受限条目。
"""
from __future__ import annotations

import math
import re
import tomllib
from pathlib import Path

RUN_MIN, WALK_MAX = 2.2, 3.5          # m/s
SPAN = re.compile(r"(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)\s*s")
CLAUSE = re.compile(r"[，；。！？]|——")
RUN = re.compile(r"冲上|冲下|冲进|冲出|冲过|冲到|冲回|冲向|冲过来|往前冲|冲刺|顶上去|拔腿|狂奔|飞奔|奔跑|快跑|抢着跑|迎上去|扑向|扑过去|扑上去"
                 r"|(?<![逃开])跑(?!得|题|调|开)")
WALK = re.compile(r"走近|走过|走向|走到|走进|走出|踱|慢慢走|照旧走|缓步")
OUTCOMES = {
    "摔倒": (re.compile(r"摔倒|摔了一跤|绊倒|绊了一跤|栽倒|跌倒|跌坐|脸朝下(?:拍|趴)|往前栽|整个人往前扑"),
             re.compile(r"撞|推|砸空|抡空|太重|太满|够不着|一拽|一脚(?:踢|蹬|踹)|被.{0,8}(?:打|踢|撞|扑|咬住|拽|拖|砸|劈|绊|推|顶|掀|甩)"
                        r"|(?:泥|苔|冰|油|湿|碎石|滚木).{0,6}(?:滑|踩空)|踩(?:在|上|中).{0,6}(?:泥|苔|冰|油|湿|碎石|滚木)"), False),
    "喘": (re.compile(r"喘"), re.compile(r"跑|冲|打|扑|砸|抡|挡|爬|搬|挖|赶|逃|追|咬|劈|顶"), True),
    "逃": (re.compile(r"逃|夹着尾巴|掉头跑|跑开|溜走"),
           re.compile(r"挨|被.{0,6}(?:打|砸|劈|踢|撞|顶)|嗷|砸在|劈在|一顶|踢|吓|光|火|劈"), False),
    "愣住": (re.compile(r"愣住|一愣|吓一跳|吓得|猛地抬头|眼睛一瞪"),
             re.compile(r"声|喊|吼|响|看见|出现|窜|扑|咬|叫|碰|摸|拍"), False),
}
INJURY = re.compile(r"咬了|咬住|咬在|砍中|砍在|划破|扭了|撞伤|受伤|擦伤|啄在|啄伤|踢伤|挨了一(?:镐|刀|斧|锤|剑|拳|脚|叉)")   # 衣物破损（撕开的裤膝）归状态账本管
SEVERITY = ("无碍", "皮外", "行动受限", "非伤")  # states.toml `severity` 的全部取值：无碍＝挨了一下但当场没事；非伤＝衣物 / 物件的状态；
                                                 # 只有行动受限能让人瘸、腿软、自己摔
NOHARM = re.compile(r"没破皮|没伤到|没受伤|没咬透|挡住|打滑")
IMPAIR = re.compile(r"瘸|跛|一软|腿软|脚软|拖着.{0,2}[腿脚]|站不稳")
LIMP = re.compile(r"瘸|跛|拖着.{0,2}[腿脚]")
FALL_BODY = re.compile(r"一软|伤脚|伤腿|瘸|跛|脱力|体力不支")


def beats(action: str) -> list[tuple[float, float, str]]:
    ms = list(SPAN.finditer(action))
    return [(float(m.group(1)), float(m.group(2)), action[m.end(): (ms[i + 1].start() if i + 1 < len(ms) else len(action))])
            for i, m in enumerate(ms)]


def _pos(path: list, t: float) -> tuple[float, float]:
    pts = [(float(p[0]), float(p[1]), float(p[2])) for p in path]
    if t <= pts[0][0]:
        return pts[0][1], pts[0][2]
    for (t0, x0, y0), (t1, x1, y1) in zip(pts, pts[1:]):
        if t0 <= t <= t1:
            k = (t - t0) / (t1 - t0) if t1 > t0 else 1.0
            return x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    return pts[-1][1], pts[-1][2]


def max_speed(ov: dict, actor: dict, a: float, b: float) -> float:
    cuts = [float(c["t"]) for c in ov.get("camera", []) if c.get("cut")]
    best, t, dt = 0.0, a, 0.1
    while t + dt <= b + 1e-6:
        if not any(t - 0.15 < c <= t + dt + 0.15 for c in cuts):   # 切点处允许跳到下一段站位
            best = max(best, math.dist(_pos(actor["path"], t), _pos(actor["path"], t + dt)) / dt)
        t += dt
    return best


def _base(label: str) -> str:
    return re.sub(r"（.*?）|\(.*?\)", "", label).strip()


def _who(clause: str, humans: list[dict]) -> list[dict]:
    if "两人" in clause or "两个人" in clause:
        return humans
    return [h for h in humans if _base(h.get("label", h["key"])) in clause]


def _subject(clause: str, verb_at: int, actors: list[dict]) -> list[dict]:
    """动词的主语：这一小句里、动词之前最先出现的那个名字（中文主语在前；「暴徒扑向亚伦」里跑的是暴徒）。"""
    head = clause[:verb_at]
    if "两人" in head or "两个人" in head:
        return [a for a in actors if a["key"].startswith("c")]
    hits = [(head.find(_base(a.get("label", a["key"]))), a) for a in actors if _base(a.get("label", a["key"])) in head]
    if not hits:
        return []
    first = min(p for p, _a in hits)
    return [a for p, a in hits if p == first]


def load_states(script_dir: Path) -> list[dict]:
    f = script_dir / "states.toml"
    return tomllib.loads(f.read_text(encoding="utf-8")).get("state", []) if f.is_file() else []


def active_states(states: list[dict], key: str, order: list[str]) -> list[dict]:
    """在 key 这一镜生效的条目：from ≤ 本镜 ≤ to。"""
    if key not in order:
        return []
    i = order.index(key)
    return [s for s in states if s["from"] in order and s.get("to", s["from"]) in order
            and order.index(s["from"]) <= i <= order.index(s.get("to", s["from"]))]


def check_states(states: list[dict], order: list[str]) -> list[str]:
    """L3c：账本自洽——伤势分档配得上它在后面几镜被写出来的样子。"""
    out: list[str] = []
    for s in states:
        tag = "states.toml %s「%s」" % (s.get("who"), s.get("what", "")[:24])
        sev, to = s.get("severity"), s.get("to", s["from"])
        if sev not in SEVERITY:
            out.append("%s：severity＝%r，须是 %s 之一" % (tag, sev, " / ".join(SEVERITY)))
            continue
        for k, v in (("from", s["from"]), ("to", to)):
            if v not in order:
                out.append("%s：%s＝%s 不是本集镜号" % (tag, k, v))
        if NOHARM.search(s["what"]) and sev != "无碍":
            out.append("%s：写着挡住了 / 没伤到，severity 却是 %s" % (tag, sev))
        if sev == "无碍" and (to != s["from"] or s["show"]):
            out.append("%s：无碍的事当场就过去——to 须等于 from、show 须为空；要带到下一镜就得是真伤（皮外 / 行动受限）" % tag)
        heavy = [w for w in s["show"] if IMPAIR.search(w)]
        if heavy and sev != "行动受限":
            out.append("%s：show 里有「%s」（腿脚不听使唤），severity 须是行动受限；伤不到这个分量就别写瘸"
                       % (tag, " / ".join(heavy)))
    return out


def check_shot(key: str, action: str, text_all: str, ov: dict | None, prev_last_beat: str,
               states: list[dict], order: list[str]) -> list[str]:
    out: list[str] = []
    humans = [a for a in (ov or {}).get("actor", []) if a["key"].startswith("c")]
    actors = list((ov or {}).get("actor", []))
    hurt = {s["who"] for s in active_states(states, key, order) if s.get("severity") == "行动受限"}
    bs = beats(action)
    for i, (a, b, txt) in enumerate(bs):
        before = bs[i - 1][2] if i else prev_last_beat
        for cl in CLAUSE.split(txt):
            rm = RUN.search(cl)
            who = _subject(cl, rm.start(), actors) if rm else []
            if ov and who and rm:
                for h in who:
                    v = max_speed(ov, h, a, b)
                    if v < RUN_MIN:
                        out.append("%s %g–%gs「%s」写的是跑，平面图上%s这一拍最快 %.1f m/s（跑要 ≥ %g）"
                                   % (key, a, b, cl.strip()[:24], _base(h.get("label", h["key"])), v, RUN_MIN))
            wm = WALK.search(cl)
            who = _subject(cl, wm.start(), actors) if wm and not rm else []
            if ov and who:
                for h in who:
                    v = max_speed(ov, h, a, b)
                    if v > WALK_MAX:
                        out.append("%s %g–%gs「%s」写的是走，平面图上%s这一拍 %.1f m/s（走 ≤ %g）"
                                   % (key, a, b, cl.strip()[:24], _base(h.get("label", h["key"])), v, WALK_MAX))
        for name, (pat, cause, kin) in OUTCOMES.items():
            for m in pat.finditer(txt):
                if cause.search(txt[: m.start()]) or cause.search(before):
                    continue
                who = _who(CLAUSE.split(txt[: m.end()])[-1], humans) if ov else []
                if kin and ov and any(max_speed(ov, h, max(0.0, a - 3.0), a + 0.5) >= RUN_MIN for h in who):
                    continue
                snip = txt[max(0, m.start() - 10): m.end() + 4].strip()
                if name == "摔倒" and (FALL_BODY.search(txt[: m.start()]) or FALL_BODY.search(before)):
                    if any(n in txt[: m.end()] or n in before for n in hurt):
                        continue
                    out.append("%s %g–%gs「%s」：拿身上的状态（脚一软 / 伤脚）当摔倒的原因，但摔的人本镜没有 severity＝行动受限 的账本条目"
                               "——先问这一摔该不该有，不该有就删（ai_videos__逻辑因果 §2b），别往前补一个小伤" % (key, a, b, snip))
                    break                                                     # 同一拍同一类结果只报一次
                out.append("%s %g–%gs「%s」：%s 没有看得见的原因（同一拍前面与上一拍都没交代）%s"
                           % (key, a, b, snip, name,
                              "；摔倒只认外力 / 湿滑地面 / 行动受限的伤，跑着、一绊、踩空不算——先问这一摔该不该有" if name == "摔倒" else ""))
                break
    for m in INJURY.finditer(action):
        cl = CLAUSE.split(action[: m.start()])[-1] + CLAUSE.split(action[m.start():])[0]   # 伤字所在的那一小句
        for h in _who(cl, humans):
            nm = _base(h.get("label", h["key"]))
            if not any(s["who"] == nm and s["from"] == key for s in states):
                out.append("%s「…%s…」：%s 受伤 / 被咬，没在 states.toml 里登记（带不带到下一镜都要声明）"
                           % (key, action[max(0, m.start() - 8): m.end() + 6], nm))
    for m in LIMP.finditer(action):
        seg = re.split(r"[；。]", action[: m.start()])[-1]                     # 瘸的是这一句的主语：句里第一个名字
        named = sorted((seg.find(_base(h.get("label", h["key"]))), _base(h.get("label", h["key"]))) for h in humans)
        nm = next((n for p, n in named if p >= 0), "")
        if nm and nm not in hurt:
            out.append("%s「…%s…」：写%s瘸，但本镜没有他 severity＝行动受限 的账本条目（L3d）"
                       % (key, action[max(0, m.start() - 8): m.end() + 4], nm))
    idx = order.index(key) if key in order else -1
    for s in states:
        if (s["from"] in order and s.get("to", s["from"]) in order
                and order.index(s["from"]) < idx <= order.index(s.get("to", s["from"]))):
            if not any(w in text_all for w in s["show"]):
                out.append("%s：%s「%s」（%s 起）这一镜得写到（%s 任一个），没写" % (
                    key, s["who"], s["what"], s["from"], " / ".join(s["show"])))
    return out
