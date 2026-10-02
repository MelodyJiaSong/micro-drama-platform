# -*- coding: utf-8 -*-
"""目标账本（follow-up 038：「shot5 的时候，观众怎么知道他们要去做什么任务，目的是什么」）。

每集一份 `4_剧本/episodes/{ep}/goals.toml`：观众要跟的每一件事——谁交代的、屏幕上哪一句说出来、为什么、谁接下、
在哪几镜推进、在哪一镜屏幕上了结（或明说留到下一集）。生成器 build 时机检：

  G1 说出来、接下来、了结，都得真在那一镜的画面动作或台词里（引用原文片段；备注与情绪说明不算——观众看不见）
  G2 别人交代的事要有主角接下（`accepted`），或写明为什么不用接（`accept_note`）
  G3 了结要么在画面上（`resolved`），要么明说留到哪一集（`carry`）
  G4 换了地点、或隔了几镜再推进同一件事，那一镜的画面或台词里得有一个提醒词（`cues`）——观众才知道这是在干那件事
  G5 奖赏不许早于了结
  G6 每一镜至少推进一件事，或列进 `[ledger] breathers`（纯景 / 喘口气的镜）
  G7 本事（`[[skill]]`，follow-up 039）：学会（`learned`，可无＝开场就会）与实战用出（`used`）都得在屏幕上，
     用在学会之后；本集没用出来就写明留到哪一集（`carry`）
  G7b 学本事要有来路（follow-up 045：「光圈为什么就出来了，总要有点铺垫」）：学会的本事写 `idea`（师父说这本事是什么 / 从哪来）
     与 `trigger`（成的那一下是什么引出来的），都在屏幕上、不晚于学会；`core = true` 的入门课再要 `why`（为什么现在学）
     与 `fail`（第一次没成）；在画外学的写 `offscreen`（理由）；只预埋规矩不演学会的写 `rule`
     follow-up 046（「教学过程有点敷衍，站在观众角度」）：`core` 再要 `demo`（师父先做一遍给他看）、`method`（能照着做的
     一个动作或一句话）、`effect`（学会后这本事有什么用，看得见），`fail` 至少两条（一问就会＝敷衍）；
     先后：why ≤ demo ≤ 第一次 fail，fail / method / trigger 都早于 learned，effect 不早于 learned
  G7c 施法设计一处定义、处处呼应（follow-up 046：「施法设计应该呼应 shot 7 的教学设计」）：`[[casting]]` 写一个人的
     起手（`stance`）、手放哪（`hand`）、光怎么走（`flow`）——各是可选正则表，任一命中即可——在 `taught` 那一镜教出来，
     代价（`cost`：要多久、什么会打断）不晚于学会之后的第一次施法上屏；此后这个人每一次施法（本事的 learned / used /
     `casts`）所在的那一行画面动作都得同时写到起手、手、光的走向；常驻的本事（光环）写 `passive = true`，它的 used
     只是「一直开着」、不算施法，亮起 / 重新亮起的那几下列进 casts
     rule 45（follow-up 053）：`[[casting]]` 写 `card = "k201"` 时，起手 / 手 / 光的走向从技能卡 `[script]` 读（全剧一处），
     账本里不许再写 stance / hand / flow——每集各写一份就是 ep01 / ep02 审判长得不一样的来源

格式：
    [ledger]
    breathers = []
    [[goal]]
    id = "kobolds"
    who = "治安官"
    what = "清掉北边林子里的狗头人，十个就够"
    why = "狗头人占了北边的矿"
    stated = ["S04", "Kobolds took the north mine"]
    accepted = ["S05", "Kobolds first"]
    cues = ["kobold", "狗头人", "camp"]
    pursued = ["S05", "S06"]
    resolved = ["S11", "Pay for the camp"]
    reward = ["S11", "S13"]
"""
from __future__ import annotations

import re
import tomllib
from pathlib import Path

import script_tools

FILE = "goals.toml"
_PLATE = re.compile(r"bg\d+-\d+|bg\d+")   # 地点按 plate 分（bg1-2 溪边与 bg1-6 林缘是两处）
CORE_NEED = {"why": "为什么现在学", "demo": "师父先做一遍给他看", "method": "能照着做的一个动作或一句话",
             "fail": "没成（至少两次）", "effect": "学会后这本事有什么用，屏幕上看得见"}


def _pairs(v) -> list[list[str]]:
    """`["S07", "片段"]` 或它的列表。"""
    if not v:
        return []
    return [list(v)] if isinstance(v[0], str) else [list(x) for x in v]


def _line_of(s, snip: str) -> str:
    """片段所在的那一行画面动作（或那句台词）——G7c 查同一行里起手 / 手 / 光的走向写没写全。"""
    for line in script_tools.shot_screen(s):
        if snip in line:
            return line
    return ""


def _skills_of(c: dict) -> tuple[str, ...]:
    v = c.get("skill")
    return () if not v else ((v,) if isinstance(v, str) else tuple(v))


_CARDS: dict[str, object] = {}


def _card(script_md: Path, key: str):
    """`[[casting]] card` → 技能卡（tools/skills_lib.py）。"""
    import skills_lib
    drama = skills_lib.drama_of(script_md)
    if str(drama) not in _CARDS:
        _CARDS[str(drama)] = skills_lib.load(drama)
    return skills_lib.find(_CARDS[str(drama)], key)


def patterns(script_md: Path, c: dict, fld: str) -> list[str]:
    """施法三样（stance / hand / flow）的正则表：点了技能卡就从卡读，否则读账本里这一条自己写的。"""
    if c.get("card"):
        return list(_card(script_md, c["card"]).script.get(fld, ()))
    return list(c.get(fld, []))


def casting_for(cfg: dict, who: str, what: str) -> dict | None:
    """一个人的某样本事按哪一条 `[[casting]]` 施法（follow-up 047：圣光术与审判长得不一样——各自按 1.12 实机）：
    点了 `skill` 的那条优先；没点 `skill` 的那条管这个人其余的本事。"""
    mine = [c for c in cfg.get("casting", []) if c.get("who") == who]
    return next((c for c in mine if what in _skills_of(c)), None) or next((c for c in mine if not _skills_of(c)), None)


def casts(script_md: Path) -> list[tuple[str, str, str, tuple[float, float] | None]]:
    """本集每一次施法：(镜号, 谁, 本事, 时间窗)。生成器拿它对平面图的 `[[cast]]`（打斗里施法要站在盾后面）。"""
    f = script_md.parent / FILE
    if not f.is_file():
        return []
    cfg = tomllib.loads(f.read_text(encoding="utf-8"))
    shots, _ = script_tools.parse(str(script_md))
    by = {s.key: s for s in shots}
    who_cast = {c.get("who") for c in cfg.get("casting", [])}
    out = []
    for sk in cfg.get("skill", []):
        if sk.get("who") not in who_cast:
            continue
        for r in _pairs(sk.get("learned")) + ([] if sk.get("passive") else _pairs(sk.get("used"))) + _pairs(sk.get("casts")):
            if r[0] in by:
                out.append((r[0], sk["who"], sk.get("what", "?"), script_tools.snippet_window(by[r[0]], r[1])))
    return out


def check(script_md: Path) -> list[str]:
    f = script_md.parent / FILE
    if not f.is_file():
        return ["目标账本：缺 %s——观众要跟的每件事写清谁交代、屏幕上哪句说出、为什么、谁接下、在哪了结（follow-up 038）" % f.name]
    cfg = tomllib.loads(f.read_text(encoding="utf-8"))
    shots, _ = script_tools.parse(str(script_md))
    order = [s.key for s in shots]
    by = {s.key: s for s in shots}
    screen = {s.key: "\n".join(script_tools.shot_screen(s)) for s in shots}   # 与冷眼观众同一份

    def pos(ref) -> tuple[int, float]:
        """屏幕上的先后：(镜序, 时间窗起点)。"""
        if not ref or ref[0] not in by:
            return (-1, 0.0)
        w = script_tools.snippet_window(by[ref[0]], ref[1])
        return (order.index(ref[0]), w[0] if w else 0.0)
    scene = {s.key: (_PLATE.findall(s.scene or "") or [""])[-1] for s in shots}
    out: list[str] = []
    served: set[str] = set(cfg.get("ledger", {}).get("breathers", []))

    def on_screen(gid: str, field: str, ref, kind: str = "目标") -> int | None:
        if not ref:
            return None
        key, snip = ref[0], ref[1]
        if key not in screen:
            out.append("%s %s：%s 的镜号 %s 不在本集" % (kind, gid, field, key))
            return None
        if snip not in screen[key]:
            out.append("%s %s：%s「%s」在 %s 的画面动作与台词里找不到——观众看不见的交代不算（%s）"
                       % (kind, gid, field, snip, key, "G1" if kind == "目标" else "G7"))
        return order.index(key)

    for g in cfg.get("goal", []):
        gid = g.get("id", "?")
        for need in ("who", "what", "why", "stated", "cues"):
            if not g.get(need):
                out.append("目标 %s：缺 %s" % (gid, need))
        i_stated = on_screen(gid, "stated", g.get("stated"))
        if g.get("accepted"):
            on_screen(gid, "accepted", g.get("accepted"))
        elif not g.get("self") and not g.get("accept_note"):
            out.append("目标 %s：%s 交代的事，屏幕上没人接下（accepted），也没写为什么不用接（accept_note）（G2）" % (gid, g.get("who", "?")))
        i_res = on_screen(gid, "resolved", g.get("resolved")) if g.get("resolved") else None
        if i_res is None and not g.get("carry"):
            out.append("目标 %s：屏幕上没了结（resolved），也没写留到哪一集（carry）（G3）" % gid)
        cues = [c.lower() for c in g.get("cues", [])]
        pursued = [k for k in g.get("pursued", []) if k in order]
        for k in g.get("pursued", []):
            if k not in order:
                out.append("目标 %s：pursued 里的 %s 不在本集" % (gid, k))
        prev = g.get("stated", [None])[0]
        for k in pursued:
            gap = prev is None or order.index(k) - order.index(prev) > 1
            moved = prev is not None and scene.get(k) != scene.get(prev)
            if (gap or moved) and not any(c in screen[k].lower() for c in cues):
                out.append("目标 %s：%s 在%s推进这件事，画面与台词里没有提醒词（%s 任一）——观众不知道这是在干什么（G4）"
                           % (gid, k, "换了地点" if moved else "隔了几镜", " / ".join(g.get("cues", []))))
            prev = k
        for k in g.get("reward", []):
            if k in order and i_res is not None and order.index(k) < i_res:
                out.append("目标 %s：奖赏在 %s，早于了结 %s（G5）" % (gid, k, g["resolved"][0]))
        for fld in ("stated", "accepted", "resolved"):
            if g.get(fld):
                served.add(g[fld][0])
        served.update(pursued)
        served.update(k for k in g.get("reward", []) if k in order)
    for sk in cfg.get("skill", []):
        sid = "%s·%s" % (sk.get("who", "?"), sk.get("what", "?"))
        i_learn = on_screen(sid, "learned", sk.get("learned"), "本事")
        if sk.get("rule"):
            i_rule = on_screen(sid, "rule", sk.get("rule"), "本事")
            i_u = order.index(sk["used"][0]) if sk.get("used") and sk["used"][0] in order else None
            if i_rule is not None and i_u is not None and i_u < i_rule:
                out.append("本事 %s：规矩预埋在 %s，晚于用出的 %s（G7b）" % (sid, sk["rule"][0], sk["used"][0]))
        if sk.get("learned") and not sk.get("offscreen"):
            need = ["idea", "trigger"] + (list(CORE_NEED) if sk.get("core") else [])
            for fld in need:
                refs = _pairs(sk.get(fld))
                if not refs:
                    out.append("本事 %s：学会得有来路，缺 %s（%s）（G7b）" % (sid, fld, {
                        "idea": "师父说这本事是什么 / 从哪来", "trigger": "成的那一下是什么引出来的", **CORE_NEED}[fld]))
                    continue
                for r in refs:
                    on_screen(sid, fld, r, "本事")
                    if fld != "effect" and pos(r) > pos(sk["learned"]):
                        out.append("本事 %s：%s「%s」在 %s，晚于学会（G7b）" % (sid, fld, r[1], r[0]))
                    if fld == "effect" and pos(r) < pos(sk["learned"]):
                        out.append("本事 %s：effect「%s」早于学会——得是他学会以后，这本事真起了作用（G7b）" % (sid, r[1]))
            if sk.get("core"):
                fails = _pairs(sk.get("fail"))
                if len(fails) < 2:
                    out.append("本事 %s：入门课只没成一次——一问就会像敷衍，让他至少试两次不成（fail 写两条）（G7b）" % sid)
                for a, b, why in (("why", "demo", "先说为什么学，再示范"), ("demo", "fail", "师父先做一遍，他再试")):
                    ra, rb = _pairs(sk.get(a)), _pairs(sk.get(b))
                    if ra and rb and pos(ra[0]) > pos(rb[0]):
                        out.append("本事 %s：%s 晚于 %s——%s（G7b）" % (sid, a, b, why))
        i_use = on_screen(sid, "used", sk.get("used"), "本事")
        if not sk.get("used") and not sk.get("carry"):
            out.append("本事 %s：学了没用出来——本集里实战用一次（used），或写明留到哪一集（carry）（G7）" % sid)
        elif i_learn is not None and i_use is not None and i_use <= i_learn:
            out.append("本事 %s：用在 %s，不晚于学会的 %s（G7）" % (sid, sk["used"][0], sk["learned"][0]))
    for c in cfg.get("casting", []):
        cid = "施法·%s%s" % (c.get("who", "?"), ("·" + "/".join(_skills_of(c))) if _skills_of(c) else "")
        if c.get("card"):
            dup = [f for f in ("stance", "hand", "flow") if c.get(f)]
            if dup:
                out.append("%s：点了技能卡 %s，又在账本里写了 %s——施法的样子只在技能卡里定义（rule 45）" % (cid, c["card"], "/".join(dup)))
            try:
                _card(script_md, c["card"])
            except SystemExit as e:
                out.append("%s：%s" % (cid, e))
                continue
        for need in ("who", "taught", "cost") + (() if c.get("card") else ("stance", "hand", "flow")):
            if not c.get(need):
                out.append("%s：缺 %s（G7c）" % (cid, need))
        if not c.get("taught"):
            continue
        on_screen(cid, "taught", c["taught"], "施法")
        on_screen(cid, "cost", c.get("cost"), "施法")
        mine = [sk for sk in cfg.get("skill", []) if sk.get("who") == c.get("who")
                and casting_for(cfg, sk.get("who"), sk.get("what", "")) is c]
        after, first = [], None
        for sk in mine:
            for fld in ("learned", "used", "casts"):
                if fld == "used" and sk.get("passive"):
                    continue
                for r in _pairs(sk.get(fld)):
                    if fld == "casts":
                        on_screen("%s·%s" % (sk.get("who"), sk.get("what")), "casts", r, "本事")
                    if r[0] not in by or pos(r) < pos(c["taught"]):
                        continue            # 教之前的施法不回溯
                    after.append((sk, r))
                    if not (sk.get("core") and fld == "learned") and (first is None or pos(r) < pos(first)):
                        first = r
        for sk, r in after:
            line = _line_of(by[r[0]], r[1])
            miss = [nm for nm, fld in (("起手", "stance"), ("手放哪", "hand"), ("光怎么走", "flow"))
                    if not any(re.search(w, line) for w in patterns(script_md, c, fld))]
            if miss:
                out.append("本事 %s·%s：%s「%s」那一行没呼应 %s 教的施法——缺 %s（%s 任一）（G7c）" % (
                    sk.get("who"), sk.get("what"), r[0], r[1], c["taught"][0], "、".join(miss),
                    "；".join("/".join(patterns(script_md, c, f)) for f in ("stance", "hand", "flow"))))
        if c.get("cost") and first is not None and pos(c["cost"]) > pos(first):
            out.append("%s：代价（%s「%s」）晚于学会后的第一次施法 %s——观众不知道他为什么要躲到盾后面（G7c）" % (
                cid, c["cost"][0], c["cost"][1], first[0]))
    for k in order:
        if k not in served:
            out.append("目标账本：%s 不推进任何一件事，也没列进 breathers——这一镜观众在看什么？（G6）" % k)
    return out
