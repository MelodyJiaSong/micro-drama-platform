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
  **慢嗓**（剧的 `2_世界观人设/casting.md` 语速栏以「慢 / 很慢 / 极慢」开头的角色）逐窗按 ≤ 2.3 词/秒；
  casting 写了「那一句反而快」这类例外的，在台词行尾注释里写「语速快」放行（shengji_zhilu ep02 时长节奏审 M9：慢嗓被排到 3 词/秒的天花板）。
- **时长**：每镜 3–30s（`ai_video.md` 全局）；**本仓库还有一条偏好**——避免 4–6s 碎镜。问过用户、合不了的，
  列进同一份 `script.toml` 的 `[fragment_ok]`（`ep02 = ["S40"]`，键＝ep 目录名），闸门放行。
- **合计**：各镜时长之和必须等于文件头声明的本集总时长，且落在单集区间内——
  默认 90–120s；剧可在 `4_剧本/script.toml` 的 `[episode] min_s / max_s` 改写（取离 ep 最近的一份）；
  单集放宽写在同一份的 `[episode_overrides]`（`ep02 = [690, 750]`，键＝ep 目录名）。
- **场景展示**（剧级 opt-in：`script.toml` 有 `[scenery]` 才启用）：每个场景主体（`场景:` 行第一个 `bgN`）
  在全剧**第一次出现**的那一镜必须有 `- 场景展示: 【a–bs】{方式}：{特点}`，窗长 ≥ 阈值——
  该 bg 所在的区也是第一次出现用 `new_zone_min_s`，否则用 `new_bg_min_s`。「第一次」按集序跨集算；
  `场景:` 行带「闪前」的镜不算抵达。理由：新地方先给景再演戏（shengji_zhilu follow-up 011）。
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
SLOW_WPS_MAX = 2.3          # 慢嗓角色（casting.md 语速栏以 慢 / 很慢 / 极慢 开头）
_SLOW = re.compile(r"(极慢|很慢|慢)")
SLOW_EXEMPT = "语速快"      # 行尾注释写了它，这一句不按慢嗓算
_TOTAL = re.compile(r"\*\*(\d+)s\*\*")
_SCENERY = re.compile(r"^-\s*场景展示:\s*【\s*([0-9.]+)\s*[–-]\s*([0-9.]+)\s*s\s*】\s*(.*)$", re.M)
_BG_KEY = re.compile(r"`(bg\d+)`")

# 古语 / 公文唱礼腔的黑名单。命中即 blocker——**生成时就不许写出来**。
ARCHAIC: tuple[str, ...] = (
    "吾", "汝", "尔等", "之乎", "者也", "矣", "焉", "岂", "安能", "莫非",
    "此乃", "速速", "尔族", "不得喧哗", "按序上前", "老朽", "在下不才",
    "敢问阁下", "承蒙", "失敬", "告罪", "领命", "遵命", "谨遵",
)
EP_RANGE_DEFAULT: tuple[float, float] = (90.0, 120.0)
_CFG_KEYS: dict[str, set[str]] = {"episode": {"min_s", "max_s"},
                                  "scenery": {"new_zone_min_s", "new_bg_min_s", "idle_max_s", "post_trim_zone_s", "post_trim_bg_s"}}
# 单集覆盖：键是 ep 目录名、值是 [min_s, max_s]（shengji_zhilu follow-up 048：ep02 用户批准放宽）
_OVERRIDES = "episode_overrides"
# 用户批准的 4–6s 碎镜：键是 ep 目录名、值是镜号列表（shengji_zhilu ep02 S40，用户 2026-09-30：合并会让精简稿超 2000 字）
_FRAG_OK = "fragment_ok"
# 已出片、台词共用一个时间窗的镜（061：一窗多句，字幕只显示得出第一句、对口型也乱；新镜一律一窗一句）：键 epNN、值镜号列表，只减不增
_SHARED_OK = "shared_window_ok"
# 同一镜里同一个人说同一句（> 12 字符）两遍：默认报错（用户 2026-10-01，S04 治安官「Hey, citizen!」念了两遍）；确属有意的登记在这里，只减不增：键 epNN、值镜号列表
_REPEAT_OK = "repeat_ok"
_EP_DIR = re.compile(r"ep\d{2,}$")

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
    def need_of(text: str, en_wps: float = EN_WPS_MAX) -> float:
        return len(_CJK.findall(text)) / CN_CPS_MAX + len(_EN_WORD.findall(text)) / en_wps

    def window_errors(self, tag: str, slow: frozenset[str] = frozenset()) -> list[str]:
        spoken = [(who, t, tail) for k, who, t, tail in self.lines if k in ("对白", "OS")]
        wins = [(_WIN.search(tail), t, who in slow and SLOW_EXEMPT not in tail) for who, t, tail in spoken]
        if not any(w for w, _t, _s in wins):
            return []
        errs: list[str] = []
        need: dict[tuple[float, float], float] = {}
        for w, t, is_slow in wins:
            if w is None:
                errs.append("%s %s: 本镜有台词带时间窗，「%s」却没带" % (tag, self.key, t[:24]))
                continue
            a, b = float(w.group(1)), float(w.group(2))
            if not 0 <= a < b <= self.dur:
                errs.append("%s %s: 时间窗【%g–%gs】不在 0–%gs 内" % (tag, self.key, a, b, self.dur))
                continue
            need[(a, b)] = need.get((a, b), 0.0) + self.need_of(t, SLOW_WPS_MAX if is_slow else EN_WPS_MAX)
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


def _config(path: str) -> tuple[dict, str | None]:
    """离 ep 最近的 `script.toml`（及其路径）；没有就返回空配置。schema 之外的键直接报错，不静默忽略。"""
    d = os.path.dirname(os.path.abspath(path))
    while d.startswith(REPO) and d != REPO:
        f = os.path.join(d, "script.toml")
        if os.path.isfile(f):
            with open(f, "rb") as fh:
                cfg = tomllib.load(fh)
            for sec, body in cfg.items():
                if sec == _OVERRIDES and isinstance(body, dict):
                    bad = {k for k, v in body.items() if not _EP_DIR.match(k) or not isinstance(v, list)
                           or len(v) != 2 or not all(isinstance(x, (int, float)) for x in v)}
                    if bad:
                        raise SystemExit("%s: [%s] 键须为 epNN、值须为 [min_s, max_s]：%s" % (f, sec, sorted(bad)))
                    continue
                if sec in (_FRAG_OK, _SHARED_OK, _REPEAT_OK) and isinstance(body, dict):
                    bad = {k for k, v in body.items() if not _EP_DIR.match(k) or not isinstance(v, list)
                           or not all(isinstance(x, str) and re.fullmatch(r"S\d{2,}", x) for x in v)}
                    if bad:
                        raise SystemExit("%s: [%s] 键须为 epNN、值须为镜号列表 [\"S40\"]：%s" % (f, sec, sorted(bad)))
                    continue
                bad = set(body) - _CFG_KEYS.get(sec, set()) if isinstance(body, dict) else {sec}
                if sec not in _CFG_KEYS or bad:
                    raise SystemExit("%s: 未知配置 [%s] %s" % (f, sec, sorted(bad)))
            return cfg, f
        d = os.path.dirname(d)
    return {}, None


def ep_range(path: str) -> tuple[float, float]:
    cfg, f = _config(path)
    ep = cfg.get("episode", {})
    lo = float(ep.get("min_s", EP_RANGE_DEFAULT[0]))
    hi = float(ep.get("max_s", EP_RANGE_DEFAULT[1]))
    ov = cfg.get(_OVERRIDES, {}).get(os.path.basename(os.path.dirname(os.path.abspath(path))))
    if ov:
        lo, hi = float(ov[0]), float(ov[1])
    if not 0 < lo < hi <= 3600:
        raise SystemExit("%s: [episode] 区间 %g–%g 不合法" % (f, lo, hi))
    return lo, hi


def _zones(scenes_root: str) -> dict[str, str]:
    """bgN → 它所在的区（scenes 下的上级目录路径；扁平布局为空串）。主体目录判据＝目录里有同名 md。"""
    out: dict[str, str] = {}
    for dirpath, dirs, _files in os.walk(scenes_root):
        for d in dirs:
            m = re.match(r"(bg\d+)_", d)
            if m and os.path.isfile(os.path.join(dirpath, d, d + ".md")):
                out[m.group(1)] = os.path.relpath(dirpath, scenes_root).replace(os.sep, "/")
    return out


def scenery_cfg(drama: str) -> dict:
    """剧级 `4_剧本/script.toml` 的 [scenery]（景与空走的阈值一处定义：script_tools、szzl 引擎 G15、后期 edl 校验都读这里）。"""
    return _config(os.path.join(str(drama), "4_剧本", "episodes", "_"))[0].get("scenery", {})


_BEAT_T = re.compile(r"(?<![\d.–-])(\d+(?:\.\d+)?)s(?![\d–])")


def _has_beat(s: "Shot", a: float, b: float) -> bool:
    """窗里有没有「事」：一句台词的时间窗压在里面，或画面动作里有一个落在窗内的带时刻节拍（059 / 060：景和事一起给）。"""
    if any((w := _WIN.search(tail)) and float(w.group(1)) < b and float(w.group(2)) > a for k, _w, _t, tail in s.lines if k in ("对白", "OS")):
        return True
    act = s.body.split("- 台词:")[0]
    return any(a < float(m.group(1)) < b for m in _BEAT_T.finditer(act))


def scenery_errors(path: str) -> list[str]:
    cfg, f = _config(path)
    sc = cfg.get("scenery")
    if not sc or not f:
        return []
    zone_min, bg_min = float(sc["new_zone_min_s"]), float(sc["new_bg_min_s"])
    idle_max = float(sc.get("idle_max_s", 0) or 0)
    drama = os.path.dirname(os.path.dirname(f))
    zones = _zones(os.path.join(drama, "2_世界观人设", "scenes"))
    seen_bg: set[str] = set()
    seen_zone: set[str] = set()
    errs: list[str] = []
    for ep_path in episodes(os.path.join(os.path.dirname(f), "episodes")):
        mine = os.path.samefile(ep_path, path)
        tag = os.path.basename(os.path.dirname(ep_path))
        for s in parse(ep_path)[0]:
            m = _BG_KEY.search(s.scene)
            if not m or "闪前" in s.scene:
                continue
            bg = m.group(1)
            if bg not in zones:
                if mine:
                    errs.append("%s %s: 场景主体 %s 在 scenes/ 下找不到" % (tag, s.key, bg))
                continue
            first_bg, first_zone = bg not in seen_bg, zones[bg] not in seen_zone
            seen_bg.add(bg)
            seen_zone.add(zones[bg])
            if not mine or not first_bg:
                continue
            need = zone_min if first_zone else bg_min
            what = "新地区 %s" % zones[bg] if first_zone else "新地点 %s" % bg
            wins = [(float(a), float(b)) for a, b, _t in _SCENERY.findall(s.body)]
            if not wins:
                errs.append("%s %s: %s第一次出现，缺 `- 场景展示: 【a–bs】…` 行（≥%gs）" % (tag, s.key, what, need))
                continue
            longest = max(b - a for a, b in wins)
            if longest < need:
                errs.append("%s %s: %s第一次出现，场景展示只有 %gs，要 ≥%gs" % (tag, s.key, what, longest, need))
            for a, b in wins:
                if not 0 <= a < b <= s.dur:
                    errs.append("%s %s: 场景展示窗【%g–%gs】不在 0–%gs 内" % (tag, s.key, a, b, s.dur))
                elif idle_max and b - a > idle_max + 1e-6 and not _has_beat(s, a, b):
                    errs.append("%s %s: 场景展示窗【%g–%gs】%gs 里没台词、没带时刻的节拍——景和事一起给（> %gs 就要有事，059 / 060 G10）"
                                % (tag, s.key, a, b, b - a, idle_max))
        if mine:
            break
    return errs


_TITLES = frozenset({"Brother", "Marshal", "Auntie", "Sister", "Father"})


def slow_voices(path: str) -> frozenset[str]:
    """casting.md 里语速栏以 慢 / 很慢 / 极慢 开头的角色名：粗体名按 ` / ` 拆，每段认整段与名字（头衔后那个词或第一个词）。
    `seedance.toml` 的 legacy_eps 里的集不查（规则变更不回溯旧剧）。"""
    d = os.path.dirname(os.path.abspath(path))
    ep = os.path.basename(d)
    while d.startswith(REPO) and d != REPO and not os.path.isdir(os.path.join(d, "2_世界观人设")):
        d = os.path.dirname(d)
    f = os.path.join(d, "2_世界观人设", "casting.md")
    if not os.path.isfile(f):
        return frozenset()
    sys.path.insert(0, os.path.join(REPO, "tools"))
    import seedance_kit
    from pathlib import Path
    if ep in seedance_kit.config_or_empty(Path(d)).get("legacy_eps", []):
        return frozenset()
    out: set[str] = set()
    for ln in io.open(f, encoding="utf-8"):
        m = re.match(r"\|\s*\*\*(.+?)\*\*[^|]*\|[^|]*\|[^|]*\|([^|]*)\|", ln)
        if m and _SLOW.match(m.group(2).replace("*", "").strip()):
            for part in m.group(1).replace('"', "").split(" / "):
                words = part.split()
                out.add(part.strip())
                if words:
                    out.add(words[1] if words[0] in _TITLES and len(words) > 1 else words[0])
    return frozenset(out)


def check(path: str) -> list[str]:
    shots, declared = parse(path)
    tag = os.path.basename(os.path.dirname(path))
    frag_ok = set(_config(path)[0].get(_FRAG_OK, {}).get(tag, []))
    slow = slow_voices(path)
    stale = frag_ok - {s.key for s in shots if 4.0 <= s.dur <= 6.0}
    errs_ok = ["%s: [fragment_ok] 里的 %s 已不是 4–6s 碎镜（或镜号不存在），从名单删掉" % (tag, k) for k in sorted(stale)]
    errs: list[str] = []
    if not shots:
        return ["%s: 一个 `### 镜 X` 都没有" % tag]
    errs += errs_ok
    shared_ok = set(_config(path)[0].get(_SHARED_OK, {}).get(tag, []))
    repeat_ok = set(_config(path)[0].get(_REPEAT_OK, {}).get(tag, []))

    for s in shots:
        wins = [(float(w.group(1)), float(w.group(2)), txt) for k, _who, txt, tail in s.lines
                if k in ("对白", "OS") and (w := _WIN.search(tail))]
        if s.key not in shared_ok:
            for i, (a1, b1, t1) in enumerate(wins):
                for a2, b2, t2 in wins[i + 1:]:
                    if a1 < b2 - 1e-6 and a2 < b1 - 1e-6:
                        errs.append("%s %s: 「%s」【%g–%gs】与「%s」【%g–%gs】时间窗重叠——一窗一句，按说话先后排开（061）"
                                    % (tag, s.key, t1[:16], a1, b1, t2[:16], a2, b2))
        if s.key not in repeat_ok:
            seen: dict[tuple[str, str], int] = {}
            for k, who, txt, tail in s.lines:
                if k in ("对白", "OS") and len(txt) > 12 and not txt.startswith("Pheta"):
                    seen[(who, txt)] = seen.get((who, txt), 0) + 1
            for (who, txt), n in seen.items():
                if n > 1:
                    errs.append("%s %s: %s 的「%s」在同一镜念了 %d 遍——换成不同的话；确属有意的登记 script.toml [repeat_ok]"
                                % (tag, s.key, who, txt[:24], n))
        if not 3.0 <= s.dur <= 30.0:
            errs.append("%s %s: 时长 %gs 不在 3–30s" % (tag, s.key, s.dur))
        if 4.0 <= s.dur <= 6.0 and s.key not in frag_ok:
            errs.append("%s %s: 时长 %gs 落在 4–6s 碎镜区——先问能不能与邻镜合并"
                        % (tag, s.key, s.dur))
        if s.need_s > s.dur:
            errs.append("%s %s: 念白 %s 需 %.1fs > 本镜 %gs（中文 ≤%g 字/秒、英文 ≤%g 词/秒），念不完"
                        % (tag, s.key, s.amount, s.need_s, s.dur, CN_CPS_MAX, EN_WPS_MAX))
        errs.extend(s.window_errors(tag, slow))
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
    errs.extend(scenery_errors(path))
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


def shot_screen(s: "Shot") -> list[str]:
    """一镜里观众看得到、听得到的：场景展示、画面动作（去 ⚠ 注记）、说出口的台词（不带行尾说明与中文意思）。
    冷眼观众的输入与目标账本的机检都只认这一份（follow-up 038）。"""
    out = ["【%s–%ss】（景）%s" % (a, b, txt.strip()) for a, b, txt in _SCENERY.findall(s.body)]
    m = re.search(r"^- 画面动作: (.*?)(?=^- [^\n]*?:|\Z)", s.body, re.S | re.M)
    out += [line.strip() for line in (m.group(1).splitlines() if m else [])
            if line.strip() and not line.strip().startswith("⚠")]
    for k, who, txt, tail in s.lines:
        if k in ("对白", "OS"):
            out.append('- %s%s: "%s"' % (who, "（画外音）" if ("画外" in tail or k == "OS") else "", txt))
    return out


def snippet_window(s: "Shot", snip: str) -> tuple[float, float] | None:
    """片段在这一镜的哪个时间窗：画面动作的【a–bs】行，或台词行尾的【a–bs】（follow-up 043 演示拍特写闸门用）。"""
    m = re.search(r"^- 画面动作: (.*?)(?=^- [^\n]*?:|\Z)", s.body, re.S | re.M)
    for line in (m.group(1).splitlines() if m else []):
        w = _WIN.match(line.strip())
        if w and snip in line:
            return float(w.group(1)), float(w.group(2))
    for _k, _who, txt, tail in s.lines:
        w = _WIN.search(tail)
        if w and snip in txt:
            return float(w.group(1)), float(w.group(2))
    return None


def screen_text(path: str) -> str:
    """观众看得到、听得到的全部（follow-up 038 冷眼观众）：每镜的场景展示、画面动作与台词；
    不给备注、情绪氛围、⚠ 制作注记、台词行尾的表演说明与中文意思——作者知道、观众不知道的东西一律拿掉。"""
    shots, _ = parse(path)
    out = ["# 观众看得到、听得到的全部（只有画面与台词；不含备注、情绪说明、制作注记）", ""]
    for s in shots:
        out.append("## %s（%gs）" % (s.key, s.dur))
        out += shot_screen(s) + [""]
    return "\n".join(out)


def main() -> None:
    if len(sys.argv) < 3 or sys.argv[1] not in ("check", "gen", "screen"):
        raise SystemExit(__doc__)
    mode, target = sys.argv[1], sys.argv[2]
    if mode == "screen":                     # python tools/script_tools.py screen <script.md> [输出路径]
        txt = screen_text(target if target.endswith(".md") else os.path.join(target, "script.md"))
        if len(sys.argv) > 3:
            io.open(sys.argv[3], "w", encoding="utf-8").write(txt)
            print("→ %s" % sys.argv[3])
        else:
            sys.stdout.reconfigure(encoding="utf-8")
            print(txt)
        return
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
