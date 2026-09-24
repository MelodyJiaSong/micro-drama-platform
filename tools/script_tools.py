# -*- coding: utf-8 -*-
"""阶段 4 剧本的解析器 + 闸门 + `dialogue.md` 生成器。

用法（仓库根目录）：
    python tools/script_tools.py check <剧目录或 ep 目录>     # 只跑闸门
    python tools/script_tools.py gen   <剧目录或 ep 目录>     # 生成 dialogue.md（含闸门）

为什么 `dialogue.md` 是**生成**的而不是手写的（rule 4i ①）
----------------------------------------------------------
playbook 要求每集出两份文件：`script.md`（画面 + 台词）与 `dialogue.md`（纯台词通读）。
**同一句台词出现在两份文件里，手写第二份必漂**——改了 script 忘了改 dialogue，
而两边都不会报错，只会让配音那一侧拿到旧词。
所以 `script.md` 是**台词的唯一出处**，`dialogue.md` 由本工具生成，**不手改**。

闸门（不合格 exit 1，`blocker` 清零才进阶段 5）
-----------------------------------------------
- **节奏**：单镜念白所需秒数 ≤ 本镜时长。中文按 **≤ 5 字/秒**（目标 ≈ 4）、英文按 **≤ 3 词/秒**
  （目标 ≈ 2.5）折算，同一镜可以混排。念不完就是念不完。
  台词行尾注释里若带时间窗 `【a–bs】`，还要**逐窗**核：同一窗里的念白需时 ≤ 窗长。整镜平均合格、
  局部挤成 4–5 词/秒的情况只有这样才抓得到；一镜里只要有一句带窗，本镜每句都得带。
- **时长**：每镜 3–30s（`ai_video.md` 全局）；**本仓库还有一条偏好**——避免 4–6s 碎镜。
- **合计**：各镜时长之和必须等于文件头声明的本集总时长，且落在单集区间内——
  默认 90–120s；剧可在 `4_剧本/script.toml` 的 `[episode] min_s / max_s` 改写（取离 ep 最近的一份）。
- **标注**：每行台词必须带 `[对白] / [OS] / [系统] / [叠层]` 之一（playbook §3）。
- **白话铁律**：禁古语 / 公文唱礼腔（`台词大师` D1b）；英文台词禁伪古英语（thou / hath / verily…）。**这条是生成时闸门**，
  不留给下游 review——书面台词在本仓库反复出现过，靠提醒治不好。
  开了口子的只有**声音彩蛋通道**（行尾带「不走白话闸门」标注的那几行）。
"""
from __future__ import annotations

import io
import os
import re
import sys
import tomllib

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

_SHOT = re.compile(r"^### 镜 (\S+)\s*$", re.M)
_DUR = re.compile(r"^-\s*时长:\s*([0-9.]+)\s*s\s*$", re.M)
_SCENE = re.compile(r"^-\s*场景:\s*(.+?)\s*$", re.M)
_MOOD = re.compile(r"^-\s*情绪氛围:\s*(.+?)\s*$", re.M)
# 行尾注释前只许有**同一行内**的空白。写成 `\s*` 会把换行也吃掉，于是 `(.*)` 跑去
# 捕获下一行台词——那一行就此从解析结果里消失，**字数与条数都静默变少、不报任何错**。
# 实测：ep01 S01 三行台词只解析出两行，而生成的 dialogue.md 看上去完全正常。
_LINE = re.compile(r'^[ 	]*-[ 	]*\[(对白|OS|系统|叠层)\][ 	]*([^:：]+?)[ 	]*[:：][ 	]*"(.+?)"[ 	　]*(.*)$'
                   r'(?:\n[ 	]+（(.+?)）[ 	]*$)?', re.M)
# 英文台词下一行可附一行全角括号的中文意思（审稿用，不念、不计时），见 divergence #19
_EN_WORD = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*")
_CJK = re.compile(r"[\u4e00-\u9fff]")
_WIN = re.compile(r"【\s*([0-9.]+)\s*[–-]\s*([0-9.]+)\s*s\s*】")
CN_CPS_MAX = 5.0
EN_WPS_MAX = 3.0
_TOTAL = re.compile(r"\*\*(\d+)s\*\*")

# 古语 / 公文唱礼腔的黑名单。命中即 blocker——**生成时就不许写出来**。
ARCHAIC: tuple[str, ...] = (
    "吾", "汝", "尔等", "之乎", "者也", "矣", "焉", "岂", "安能", "莫非",
    "此乃", "速速", "尔族", "不得喧哗", "按序上前", "老朽", "在下不才",
    "敢问阁下", "承蒙", "失敬", "告罪", "领命", "遵命", "谨遵",
)
EP_RANGE_DEFAULT: tuple[float, float] = (90.0, 120.0)
_CFG_KEYS: dict[str, set[str]] = {"episode": {"min_s", "max_s"}}

ARCHAIC_EN: re.Pattern[str] = re.compile(
    r"\b(thou|thee|thy|thine|hath|doth|verily|forsooth|'tis|henceforth|hither|thither|whence|wherefore)\b",
    re.I)

# 声音彩蛋通道：行尾自己声明了豁免的，跳过白话闸门（concept 裁定 4）
EXEMPT = "不走白话闸门"


class Shot:
    def __init__(self, key: str, body: str) -> None:
        self.key = key
        self.body = body
        d = _DUR.search(body)
        if not d:
            raise SystemExit("镜 %s 缺 `- 时长: Ns` 行" % key)
        self.dur = float(d.group(1))
        s = _SCENE.search(body)
        self.scene = s.group(1) if s else ""
        m = _MOOD.search(body)
        self.mood = m.group(1) if m else ""
        self.lines = [(k, who.strip(), txt, tail) for k, who, txt, tail, _g in _LINE.findall(body)]
        self.glosses = [g for *_x, g in _LINE.findall(body)]

    def _spoken(self) -> list[str]:
        """只数**要念出来的**：`[叠层]` / `[系统]` 是后期贴的，不占念白时间。"""
        return [t for k, _w, t, _tail in self.lines if k in ("对白", "OS")]

    @staticmethod
    def need_of(text: str) -> float:
        return len(_CJK.findall(text)) / CN_CPS_MAX + len(_EN_WORD.findall(text)) / EN_WPS_MAX

    def window_errors(self, tag: str) -> list[str]:
        spoken = [(t, tail) for k, _w, t, tail in self.lines if k in ("对白", "OS")]
        wins = [(_WIN.search(tail), t) for t, tail in spoken]
        if not any(w for w, _t in wins):
            return []
        errs: list[str] = []
        need: dict[tuple[float, float], float] = {}
        for w, t in wins:
            if w is None:
                errs.append("%s %s: 本镜有台词带时间窗，「%s」却没带" % (tag, self.key, t[:24]))
                continue
            a, b = float(w.group(1)), float(w.group(2))
            if not 0 <= a < b <= self.dur:
                errs.append("%s %s: 时间窗【%g–%gs】不在 0–%gs 内" % (tag, self.key, a, b, self.dur))
                continue
            need[(a, b)] = need.get((a, b), 0.0) + self.need_of(t)
        for (a, b), n in sorted(need.items()):
            if n > b - a + 1e-6:
                errs.append("%s %s: 时间窗【%g–%gs】念白需 %.1fs > 窗长 %gs，念不完"
                            % (tag, self.key, a, b, n, b - a))
        return errs

    @property
    def cn_chars(self) -> int:
        return sum(len(_CJK.findall(t)) for t in self._spoken())

    @property
    def en_words(self) -> int:
        return sum(len(_EN_WORD.findall(t)) for t in self._spoken())

    @property
    def need_s(self) -> float:
        return self.cn_chars / CN_CPS_MAX + self.en_words / EN_WPS_MAX

    @property
    def amount(self) -> str:
        return " + ".join(x for x in (("%d 字" % self.cn_chars) if self.cn_chars else "",
                                      ("%d 词" % self.en_words) if self.en_words else "") if x) or "0"


def parse(path: str) -> tuple[list[Shot], int | None]:
    text = io.open(path, encoding="utf-8").read()
    keys = [(m.group(1), m.start()) for m in _SHOT.finditer(text)]
    shots = []
    for i, (k, a) in enumerate(keys):
        b = keys[i + 1][1] if i + 1 < len(keys) else len(text)
        shots.append(Shot(k, text[a:b]))
    head = text[:keys[0][1]] if keys else text
    t = _TOTAL.search(head)
    return shots, (int(t.group(1)) if t else None)


def ep_range(path: str) -> tuple[float, float]:
    """离 ep 最近的 `script.toml`；没有就用默认。schema 之外的键直接报错，不静默忽略。"""
    d = os.path.dirname(os.path.abspath(path))
    while d.startswith(REPO) and d != REPO:
        f = os.path.join(d, "script.toml")
        if os.path.isfile(f):
            with open(f, "rb") as fh:
                cfg = tomllib.load(fh)
            for sec, body in cfg.items():
                bad = set(body) - _CFG_KEYS.get(sec, set()) if isinstance(body, dict) else {sec}
                if sec not in _CFG_KEYS or bad:
                    raise SystemExit("%s: 未知配置 [%s] %s" % (f, sec, sorted(bad)))
            ep = cfg.get("episode", {})
            lo = float(ep.get("min_s", EP_RANGE_DEFAULT[0]))
            hi = float(ep.get("max_s", EP_RANGE_DEFAULT[1]))
            if not 0 < lo < hi <= 3600:
                raise SystemExit("%s: [episode] 区间 %g–%g 不合法" % (f, lo, hi))
            return lo, hi
        d = os.path.dirname(d)
    return EP_RANGE_DEFAULT


def check(path: str) -> list[str]:
    shots, declared = parse(path)
    tag = os.path.basename(os.path.dirname(path))
    errs: list[str] = []
    if not shots:
        return ["%s: 一个 `### 镜 X` 都没有" % tag]

    for s in shots:
        if not 3.0 <= s.dur <= 30.0:
            errs.append("%s %s: 时长 %gs 不在 3–30s" % (tag, s.key, s.dur))
        if 4.0 <= s.dur <= 6.0:
            errs.append("%s %s: 时长 %gs 落在 4–6s 碎镜区——先问能不能与邻镜合并"
                        % (tag, s.key, s.dur))
        if s.need_s > s.dur:
            errs.append("%s %s: 念白 %s 需 %.1fs > 本镜 %gs（中文 ≤%g 字/秒、英文 ≤%g 词/秒），念不完"
                        % (tag, s.key, s.amount, s.need_s, s.dur, CN_CPS_MAX, EN_WPS_MAX))
        errs.extend(s.window_errors(tag))
        if not s.mood:
            errs.append("%s %s: 缺 `- 情绪氛围:` 行" % (tag, s.key))
        for kind, who, txt, tail in s.lines:
            if EXEMPT in tail:
                continue
            hit = [w for w in ARCHAIC if w in txt] + [m.group(0) for m in ARCHAIC_EN.finditer(txt)]
            if hit:
                errs.append("%s %s: 「%s」里有古语/公文腔 %s —— 换口语说法"
                            % (tag, s.key, txt[:24], "、".join(hit)))

    total = sum(s.dur for s in shots)
    if declared is not None and abs(total - declared) > 0.5:
        errs.append("%s: 各镜时长合计 %gs ≠ 文件头声明的 %ds" % (tag, total, declared))
    lo, hi = ep_range(path)
    if not lo <= total <= hi:
        errs.append("%s: 单集 %gs 不在 %g–%gs" % (tag, total, lo, hi))
    return errs


def gen_dialogue(path: str) -> str:
    shots, declared = parse(path)
    ep = os.path.basename(os.path.dirname(path))
    out = [
        "# %s · 纯台词（通读 / 配音用）" % ep.upper(),
        "",
        "> **本文件是生成物**：`python tools/script_tools.py gen <ep 目录>`。",
        "> 台词的唯一出处是同目录 `script.md`（rule 4i ①）——**改台词 ＝ 改 script.md 重跑**，不手改本文件。",
        "> `[叠层]` / `[系统]` 是**后期贴的 UI**，不进配音，也不占念白时间（concept B3 三层归属制）。",
        "",
        "| 镜 | 时长 | 念白量 | 念白需时 |",
        "|---|---|---|---|",
    ]
    for s in shots:
        out.append("| %s | %gs | %s | %.1fs |" % (s.key, s.dur, s.amount, s.need_s))
    out.append("| **合计** | **%gs** | — | **%.1fs** |"
               % (sum(s.dur for s in shots), sum(s.need_s for s in shots)))
    out.append("")
    out.append("---")
    for s in shots:
        out.append("")
        out.append("## 镜 %s　*(%gs · %s)*" % (s.key, s.dur, s.scene))
        if not s.lines:
            out.append("")
            out.append("*（本镜无台词）*")
            continue
        out.append("")
        for (kind, who, txt, tail), gloss in zip(s.lines, s.glosses):
            note = re.sub(r"^\*\(|\)\*$", "", tail.strip()).strip() if tail.strip() else ""
            mark = {"对白": "", "OS": "内心独白·嘴唇不动",
                    "系统": "后期贴·仅主角可见", "叠层": "后期贴·≤1.5s"}[kind]
            ann = "　".join(x for x in (mark, note) if x)
            out.append('%s: "%s"%s' % (who, txt, ("　*(%s)*" % ann) if ann else ""))
            if gloss:
                out.append("　　（%s）" % gloss)
    return "\n".join(out) + "\n"


def episodes(root: str) -> list[str]:
    root = os.path.abspath(root)
    if os.path.isfile(os.path.join(root, "script.md")):
        return [os.path.join(root, "script.md")]
    hits = []
    for dirpath, _dirs, files in os.walk(root):
        if "script.md" in files:
            hits.append(os.path.join(dirpath, "script.md"))
    return sorted(hits)


def main() -> None:
    if len(sys.argv) < 3 or sys.argv[1] not in ("check", "gen"):
        raise SystemExit(__doc__)
    mode, target = sys.argv[1], sys.argv[2]
    paths = episodes(target)
    if not paths:
        raise SystemExit("%s 下没有 script.md" % target)

    all_errs: list[str] = []
    for p in paths:
        all_errs.extend(check(p))
    if all_errs:
        print("台词闸门 %d 条：" % len(all_errs))
        for e in all_errs:
            print("  ❌ " + e)
        sys.exit(1)

    tot_shots = tot_dur = 0
    for p in paths:
        shots, _ = parse(p)
        tot_shots += len(shots)
        tot_dur += sum(s.dur for s in shots)
        if mode == "gen":
            d = os.path.join(os.path.dirname(p), "dialogue.md")
            io.open(d, "w", encoding="utf-8").write(gen_dialogue(p))
            print("  → %s" % os.path.relpath(d, REPO))
    print("%d 集 · %d 镜 · %gs —— 台词闸门全过 ✔" % (len(paths), tot_shots, tot_dur))


if __name__ == "__main__":
    main()
