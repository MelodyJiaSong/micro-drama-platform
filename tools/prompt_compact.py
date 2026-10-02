# -*- coding: utf-8 -*-
"""把生成器拼出的「设计稿」prompt（十几个 `字段: 值` 行）压成上传 Seedance 的精简 prompt（ai_video.md rule 12.4-P）。

依据火山官方《Seedance 2.5 提示词指南》（volcengine.com/docs/82379/2607689）：
素材指代 → 一句话概述 → 按整秒时间戳逐段写画面 / 运镜 / 动作 / 台词 → 结尾写贯穿全片的细节；
参考素材够准时只写指代、不复述；动作写概括；负向只对字幕与声音有效；时间戳只认整秒。

设计稿仍留在 shot md 的第一个 text 块给人和闸门读；这里只做「选、并、改写时间」，不创作内容：
  · 保留：参考行、人数、情节首句、场景、分镜段、画面左右（screen_clause）、护人格挡、动作、命中、画内台词、光线、渲染、比例、时长
  · 去掉：参考用法长文、角色锁定串（entity 已锁长相）、镜内状态与节奏（与动作重复）、走位里的罗盘句、
          「情绪目的」注、音乐行、点名具体物件的否定句与负面词
压完再回读：保留字段里每个带时间的分句都必须原样（改写时间后）出现在结果里，否则 raise——压缩不许丢内容。
"""
from __future__ import annotations

import re
from dataclasses import dataclass

COMPACT_MAX = 2000
AUDIO_MODES = ("native", "tts_first")
NO_MUSIC = "只有画里人物的对白人声、环境声和动作声；不要音乐、背景音乐、BGM、配乐、器乐、旋律、氛围铺底音"
NEG_KEEP = ("人物本身不自发光", "不自发光", "不发光")
# 【不要】的通用项：每部剧都成立、不点名任何物件；画风类（卡通 / 游戏截图感…）由剧的 seedance.toml `negatives` 追加
NEG_GENERIC = "字幕，画面文字，水印，logo，分身（同一个人在画面里同时出现两次），双胞胎，人脸变形，五官漂移，畸形肢体，多余手指"

_FIELD = re.compile(r"^([^\s:：【]{1,6}):\s?(.*)$")
_SPAN = re.compile(r"^(\d+(?:\.\d+)?)[–-](\d+(?:\.\d+)?)s\s*")
_POINT = re.compile(r"^(\d+(?:\.\d+)?)s\s*")
_DEC = re.compile(r"(\d+\.\d+)(?=\s*s|–)")
_NEGATION = re.compile(r"没有|不是|别是|不要|不带|不戴|不穿")
_PURPOSE = re.compile(r"（情绪目的[^）]*）")
_REF = re.compile(r"`([^`(（]+)[(（]([^`]*)[)）]=>@`")
ROLES = (("技能样片", "技能样片"), ("技能峰值图", "技能峰值图"), ("白模", "白模"), ("平面图", "平面图"), ("首帧", "首帧"), ("场景", "场景"), ("entity", "角色"),
         ("装备", "装备"), ("物件", "物件"), ("音频", "音频"))
_LINE = re.compile(r"^(?P<who>[^（(]+)（(?P<kind>正常台词|内心独白|画外)[·・](?P<lip>[^）]*)）：(?P<text>.+)$")


@dataclass(frozen=True)
class Cast:
    key: str              # 卡目录名，与参考行的 entity 句柄同名
    label: str            # 设计稿里的称呼（亚伦）
    color: str = ""       # 白模里的人偶颜色；免 previz 的镜为空
    speaker: str = ""     # 剧本台词里的说话人名（Aaron）；同一张卡的几个别名用「|」隔开


@dataclass(frozen=True)
class Seg:
    a: int
    b: int
    head: str


def _round(x: float) -> int:
    return int(x + 0.5)


_DURATION_MARK = ("≤", "<", "约", "不超过", "持续", "只有", "大约", "时长")   # 时长：镜长 28.5 s 不许写成 29 秒（8f ep02 S46）


def whole_seconds(text: str) -> str:
    """0.1 秒级时刻 → 整秒（Seedance 2.5 只响应整秒时间戳）。时长不取整：「≤0.3s」取整成「≤0秒」就把一闪写没了
    （shot13 实测），所以前面带时长记号、或本身不到 1 秒的数原样保留。"""
    def one(m: re.Match) -> str:
        v = float(m.group(1))
        before = m.string[max(0, m.start() - 4):m.start()].rstrip()
        if v < 1.0 or any(before.endswith(k) for k in _DURATION_MARK):
            return m.group(1)
        return str(_round(v))
    text = _DEC.sub(one, text)
    return re.sub(r"(\d+(?:\.\d+)?)–(\d+(?:\.\d+)?)s", r"\1–\2秒", re.sub(r"(\d+(?:\.\d+)?)s(?=[\s，。；、）]|$)", r"\1秒", text))


def fields(full: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for ln in full.split("\n"):
        m = _FIELD.match(ln)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def _chunks(text: str, sep: str = "；") -> list[str]:
    return [c.strip() for c in text.split(sep) if c.strip()]


def _start(chunk: str) -> float | None:
    m = _SPAN.match(chunk) or _POINT.match(chunk)
    return float(m.group(1)) if m else None


def _drop_negations(text: str) -> str:
    """描述性字段里点名物件的否定分句（「头上没有头盔」「不是斧子」）整句去掉：模型会把被点名的东西画出来。"""
    keep = []
    for c in re.split(r"([；，])", text):
        if c in "；，":
            keep.append(c)
        elif not _NEGATION.search(c) or any(k in c for k in NEG_KEEP):
            keep.append(c)
    return re.sub(r"[；，]{2,}", lambda m: m.group(0)[0], "".join(keep)).strip("；，")


def segments(f: dict[str, str], secs: float) -> list[Seg]:
    cut = f.get("分镜", "").split("。", 1)[0]
    if not cut:
        return [Seg(0, _round(secs), _PURPOSE.sub("", f.get("镜头", "")).split("；", 1)[0])]
    segs: list[Seg] = []
    for part in cut.split("｜"):
        m = _SPAN.match(part.strip())
        if not m:
            raise ValueError("分镜段没有时间窗：%s" % part)
        a, b = _round(float(m.group(1))), _round(float(m.group(2)))
        head = part.strip()[m.end():].strip()
        if segs and (a == segs[-1].a or "【切】" not in part):     # 8f 运镜3：没【切】是同一条运镜的接续，不另起一个「镜头N」
            segs[-1] = Seg(segs[-1].a, max(b, segs[-1].b), segs[-1].head + "，接着" + head if a != segs[-1].a else segs[-1].head + "，" + head)
        elif b > a:
            segs.append(Seg(a, b, head))
    return segs


def timeline(full: str, secs: float) -> list[tuple[Seg, list[str]]]:
    """设计稿 → 每个分镜段 + 落在这段里的动作分句（animatic 印在画面上的摘要用）。"""
    f = fields(full)
    segs = segments(f, secs)
    acts: list[list[str]] = [[] for _ in segs]
    last = 0
    for c in _chunks(f.get("动作", "")):
        last = _bucket(segs, _start(c), last)
        acts[last].append(whole_seconds(_SPAN.sub("", c, count=1)))
    return list(zip(segs, acts))


def _bucket(segs: list[Seg], t: float | None, last: int) -> int:
    if t is None:
        return last
    r = _round(t)
    for i, s in enumerate(segs):
        if s.a <= r < s.b:
            return i
    return len(segs) - 1


def short_refs(line: str) -> str:
    """参考行的句柄只留名字 + 两字用途（长说明挪进【参考素材】）；资料包按名字对文件，不看括号。"""
    def one(m: re.Match) -> str:
        role = next((r for k, r in ROLES if k in m.group(2)), "参考")
        return "`%s(%s)=>@`" % (m.group(1), role)
    return _REF.sub(one, line)


def _people(text: str, cast: list[Cast]) -> str:
    """角色字段：entity 已锁长相，锁定串去掉，只留称呼 + 本镜状态；装备 / 物件的形制串保留（尺寸与拿法靠它）。"""
    label: dict[str, str] = {}
    for c in cast:          # 同一张卡的几个人（一群矿工、两只狼）：称呼并列，不让最后一个的称呼顶掉前面的（052 S11「抢锤的小矿工：同框不超过 6 只」）
        label[c.key] = label[c.key] + "、" + c.label if c.key in label and c.label not in label[c.key].split("、") else label.get(c.key, c.label)
    out: list[str] = []
    for c in _chunks(_drop_negations(text)):
        m = re.match(r"^([cm]\d+_[^＝]+)＝", c)
        if m:
            if out and out[-1].endswith("：") and not out[-1].startswith(("装备", "物件")):
                out.pop()           # 上一个人没有本镜状态：不留空标签「里瑞亚：」（8f #8）
            out.append(label.get(m.group(1), m.group(1)) + "：")
        elif c.startswith("本镜状态：") and out and out[-1].endswith("："):
            out[-1] += c[len("本镜状态："):]
        else:
            if out and out[-1].endswith("：") and not out[-1].startswith(("装备", "物件")):
                out.pop()
            out.append(c)
    if out and out[-1].endswith("："):
        out.pop()
    return "；".join(out)


def _mapping(ents: list[Cast]) -> tuple[str, str]:
    """「称呼＝entity」与「白模颜色＝称呼」各一句；同一张卡的几个人、同色的几个人偶并成一项。"""
    by_key: dict[str, list[str]] = {}
    by_color: dict[str, list[str]] = {}
    for c in ents:
        by_key.setdefault(c.key, []).append(c.label)
        if c.color:
            by_color.setdefault(c.color, []).append(c.label)
    who = "；".join("%s＝%s" % ("、".join(v), k) for k, v in by_key.items())
    dolls = "、".join("%s人偶是%s" % (k, "、".join(v)) for k, v in by_color.items())
    return who, dolls


def _line_text(chunk: str, mode: str, audio_n: dict[str, int], names: dict[str, str]) -> str | None:
    body = _SPAN.sub("", chunk, count=1)
    m = _LINE.match(body)
    if not m or m.group("kind") != "正常台词":
        return None             # 画外 / 内心独白后期配音，不交给 Seedance
    who, text = m.group("who").strip(), m.group("text").strip()
    who = names.get(who, who)
    if "不对口型" in m.group("lip"):
        return "%s背对镜头说：{%s}" % (who, text)
    if mode == "tts_first":
        return "%s说（口型对齐音频%d）：{%s}" % (who, audio_n.setdefault(who, len(audio_n) + 1), text)
    return "%s说：{%s}" % (who, text)


def compact(full: str, cast: list[Cast], secs: float, mode: str, extra_negatives: str = "", doll_note: str = "",
            swaps: dict[str, str] | None = None, skills: str = "", kf_use: str = "") -> str:
    """doll_note：白模用法的补充说明（szzl 052：不照搬白模人偶的姿势），接在「不取长相」后面；缺省不加，别的剧不受影响。
    swaps：`动作:` 里原样换掉的分句（技能卡全串 → 短串，8f #17）；回读核对按换过的动作比。
    skills：【技能】绑定句（每道光只属于谁、只在几秒，057 E2）；空＝本镜没有施法。"""
    if mode not in AUDIO_MODES:
        raise ValueError("audio_mode 只能是 %s，得到 %r" % ("/".join(AUDIO_MODES), mode))
    f = fields(full)
    for a, b in (swaps or {}).items():
        if a not in f.get("动作", ""):
            raise ValueError("要换的施法分句不在设计稿 `动作:` 里：" + a[:40])
        f["动作"] = f["动作"].replace(a, b)
    segs = segments(f, secs)
    body: list[list[str]] = [[] for _ in segs]

    def put(chunks: list[str]) -> None:
        last = 0
        for c in chunks:
            last = _bucket(segs, _start(c), last)
            body[last].append(_SPAN.sub("", c, count=1) if _SPAN.match(c) else c)

    walk = f.get("走位", "")
    screen = walk.split("画面里（按机位换算）：", 1)[1] if "画面里（按机位换算）：" in walk else ""
    guard = re.search(r"护人格挡：(.*?)(?:；画面里|$)", walk)
    put(["%s 画面：%s" % (m.group(0).strip(), c[m.end():]) if (m := _SPAN.match(c)) else c
         for c in _chunks(screen.split("；")[0], "｜")])
    if guard:
        put(_chunks(guard.group(1)))
    put(_chunks(f.get("动作", "")))
    hits = _chunks(f.get("命中", "").split("。打中的那一下")[0])
    act = f.get("动作", "")
    marks = list(re.finditer(r"(\d+(?:\.\d+)?)s", act))
    said: dict[int, str] = {}
    for k, m in enumerate(marks):              # 每个时刻后面那段话（到下一个时刻为止）
        end = marks[k + 1].start() if k + 1 < len(marks) else len(act)
        said[_round(float(m.group(1)))] = said.get(_round(float(m.group(1))), "") + act[m.end():end]

    def _dup(h: str) -> bool:
        """动作里同一秒已经写了这一下（同一件家伙）才省掉命中行；同一秒写的是别的事就留（88 U3：S21 画外那一声当被吞了）。"""
        t = _start(h)
        w = re.search(r"的(.)[^的，；]{0,3}(?:打|撞|咬|顶)在", h)
        return t is not None and w is not None and w.group(1) in said.get(_round(t), "")
    put([h for h in hits if not _dup(h)])
    audio_n: dict[str, int] = {}
    names: dict[str, str] = {}
    for c in cast:          # speaker 可以是「|」隔开的几个别名（Kobold / Kobold Worker 同一张卡，8f #9）；同卡几个人取第一个
        for sp in c.speaker.split("|"):
            if sp:
                names.setdefault(sp, c.label)
    lines = [(c, t) for c in _chunks(f.get("台词", "").split("。台词只供")[0])
             if (t := _line_text(c, mode, audio_n, names))]
    last = 0
    for c, t in lines:
        last = _bucket(segs, _start(c), last)
        body[last].append(t)

    who, dolls = _mapping([c for c in cast if c.key in f.get("参考", "")])
    if kf_use:          # 状态图镜（szzl 084）：绿幕前小人偶示意图，不是白模视频
        ref_use = ("状态图是绿幕前没有五官的简化小人偶示意图，只给本镜动作的先后、姿势与位置的大概意思（颜色只是标记、不是服装颜色）"
                   + ("：" + dolls if dolls else "") + "；" + kf_use + "。")
    else:
        ref_use = None
    ref_use = ref_use or ("视频是本镜白模动画（多段按段号首尾相接），严格参考其中的运镜、走位与动作时刻，不取长相"
               + ("，" + doll_note if doll_note else "") + "；白模里" + dolls + "。"
               if dolls else "平面图是俯视示意，只用来摆机位与站位，图上的线条、颜色、文字都不出现在画面里。")
    people = _people(f.get("角色", ""), cast)
    light = "；".join(dict.fromkeys(_chunks(_drop_negations(f.get("光线", "")))))
    audio = NO_MUSIC if mode == "native" else "人声以上传的音频为准，口型与节奏严格对齐；另外只要环境声和动作声，不要任何音乐"
    out = [
        "参考: " + short_refs(f.get("参考", "")),
        "【参考素材】人物：%s。%s场景图只参考材质与形制，光线和时辰只按【场景与光】；物件与装备图只参考形制。" % (who or "无", ref_use)
        + ("技能样片只参考其中的施法动作与光效，不采用其中的人物和场景。" if "技能样片" in f.get("参考", "") else "")
        + ("技能峰值图只参考光的形状与颜色。" if "技能峰值图" in f.get("参考", "") else "")
        + ("打中的每一下武器与身体真的接触、看得见受力，不是挥空。" if hits else ""),
        "【声音】" + ("本镜没有人说话；" if not lines else "") + audio + "。",     # 12.4-P 静默镜（8f #6）：画外句后期配，也算
        "【概述】" + f.get("情节", "").split("；", 1)[0].rstrip("。") + "。",
    ]
    for i, (s, b) in enumerate(zip(segs, body), 1):
        out.append("镜头%d｜%d–%d秒｜%s。%s" % (i, s.a, s.b, s.head, "；".join(b)))
    out += [
        "【人物】" + people,
    ] + (["【技能】" + skills + "。"] if skills else []) + [
        "【人数】" + f.get("人数", ""),
        "【场景与光】" + "、".join(dict.fromkeys(_chunks(f.get("场景", ""), "、"))) + "；" + light,
        "【画面】" + f.get("渲染样式", "") + "；比例 " + f.get("比例", "") + "；时长 " + f.get("时长", ""),
        "【声音】同开头：不要任何音乐。" + ("镜内切换是硬切，不加转场效果。" if len(segs) > 1 else ""),
        "【不要】" + NEG_GENERIC + ("，" + extra_negatives if extra_negatives else ""),
    ]
    text = "\n".join(whole_seconds(x) if not x.startswith("参考:") else x for x in out)
    lost = [c for c in _kept(f) if whole_seconds(_SPAN.sub("", c, count=1))[:24] not in text]
    if lost:
        raise ValueError("压缩丢了设计稿里的内容：" + "｜".join(x[:40] for x in lost[:3]))
    return text


def _kept(f: dict[str, str]) -> list[str]:
    """回读核对用：设计稿里必须原样进精简稿的分句（动作）；命中与动作同一秒的只留动作那句。"""
    return _chunks(f.get("动作", ""))
