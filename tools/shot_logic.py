# -*- coding: utf-8 -*-
"""镜内逻辑自洽检查 —— 全仓唯一一份实现（格式契约 K33 的可执行版）。

契约出处：`.claude/agent_refs/project/ai_video.md` rule 16.10 / 16.11。

## 这两个 bug 是同一个病

hy2 shot05 实测报回来两处：
1. 近景里烟道已经挖好了，切到远景又在从头挖（**建造进度倒退**）。
2. 从根盘背面的洞里塞石片，人已经起身往外走，**手还留在洞里** —— 而且按他站的位置，
   那只手长得不像人的手。

看着是两个毛病，其实是一个：**prompt 写满了「他在做什么」，却几乎没写「此刻它是什么样」。**
视频模型是逐时刻渲染的——你不写死每一刻的**状态**，状态就会自己漂。
镜内切镜把这件事放大了：一次切镜就是一次重新构图，模型没有义务记住上一段挖到哪儿了。

所以两条检查都是在问同一句话：**这一镜的每一个时刻，画面里的东西分别是什么样子？**

## L1（blocker）：有镜内切镜的建造镜，必须有 `镜内状态:` 逐段账本

判据：`分镜:` 有 ≥2 段，且 `情节:`/`动作:` 里出现建造动词（挖/铺/盖/绑/垒/架/封/剥/砌/编；名词里的字不算，见 `NOT_BUILD`：军巡铺、纸马铺、封面、脚手架…），
但没有 `镜内状态:` 行 → blocker。
账本要求：**段数与 `分镜:` 一致，且后一段包含前一段已完成的全部**（单调不倒退）。
段数能机检，单调性靠人写——但**写下来这个动作本身就逼作者过一遍时间线**，
shot05 的矛盾（剖视段展示成品，下一段又在挖）就是在补账本时暴露的。

## L2（warning）：同一段里既有「肢体探入」又有「身体位移」，必须写死先后

判据：某段的动作文字里同时出现探入类动词（伸进/塞进/掏/探进/伸手进/够进）与
位移类动词（起身/退开/走开/转身/离开/站起来），却没有次序词
（先…然后/然后才/收回…再/退出…再）→ warning。
模型会把两者叠在同一时刻，于是手留在洞里、身体走开 → 橡皮手。
顺带：**探入类动作必须写明身体与开口的距离**，否则模型按构图需要拉长手臂。
这一条判不准（次序词的写法太多），所以只报 warning + 附原句。

用法：
    import shot_logic
    shot_logic.gate(emitted, legacy={"shot01"})     # 生成器构建闸门
    python tools/shot_logic.py [范围]                # 巡检
"""
import io
import os
import re
import sys
from dataclasses import dataclass

BUILD_VERBS: tuple[str, ...] = ("挖", "铺", "盖", "绑", "垒", "架", "封", "剥", "砌", "编", "捆")
# 含建造字的名词不是建造动作（sk1 实测误报：军巡铺兵、纸马铺、本子封面、考古脚手架、地名开封）。只收无歧义的名词，「铺满」「石砌」这类可能真在建造的不收。
NOT_BUILD: tuple[str, ...] = ("军巡铺", "铺兵", "铺屋", "纸马铺", "店铺", "铺子", "封面", "信封", "脚手架", "书架", "衣架", "开封", "封丘")
REACH_VERBS: tuple[str, ...] = ("伸进", "塞进", "掏开", "掏出", "探进", "伸手进", "够进", "插进")
MOVE_VERBS: tuple[str, ...] = ("起身", "退开", "走开", "转身", "离开", "站起来", "退到", "走向")
ORDER_MARKS: tuple[str, ...] = ("然后才", "先把", "再去", "收回", "退出洞", "之后才", "先…", "然后")

SKIP_DIRS: tuple[str, ...] = ("_deleted", "previz", "renders")
_CLAUSE = re.compile(r"[；;]")
# 段落计数**不能靠分隔符**：`；` 在段落正文里本来就会出现
# （hy4 实测：`镜内状态:` 的一段写「**与上一段相同**；她停在原地…」就被数成了两段）。
# 段落真正的标识是**时间前缀** `N–Ms`，拿它来数才稳。
_SEG_HEAD = re.compile(r"\d+\s*[–\-~]\s*\d+\s*s")


@dataclass(frozen=True)
class Issue:
    shot: str
    level: str
    code: str
    detail: str


def _field(pos: str, name: str) -> str:
    for ln in pos.split("\n"):
        if ln.startswith(name + ":"):
            return ln
    return ""


def positive(md: str) -> str | None:
    b = re.findall(r"```text\n(.*?)\n```", md, re.S)
    return b[0] if b else None


def _count_segments(line: str) -> int:
    """按时间前缀 `N–Ms` 数段 —— 不按分隔符，正文里的 `；` 不会干扰。"""
    body = line.split(":", 1)[1] if ":" in line else ""
    return len(_SEG_HEAD.findall(body))


def check(shot: str, md: str) -> list[Issue]:
    pos = positive(md)
    if not pos:
        return []
    out: list[Issue] = []
    n_cuts = _count_segments(_field(pos, "分镜"))
    body = _field(pos, "情节") + _field(pos, "动作")
    for noun in NOT_BUILD:
        body = body.replace(noun, "")

    # ── L1：建造镜 + 镜内切镜 → 必须有逐段状态账本 ──
    if n_cuts >= 2 and any(v in body for v in BUILD_VERBS):
        ledger = _field(pos, "镜内状态")
        if not ledger:
            out.append(Issue(shot, "blocker", "L1",
                             "本镜有 %d 段镜内切镜、且在建造（%s），却没有 `镜内状态:` 逐段账本"
                             "——切镜时建造进度会倒退（rule 16.10）"
                             % (n_cuts, "/".join(v for v in BUILD_VERBS if v in body)[:20])))
        else:
            n_led = _count_segments(ledger)
            if n_led != n_cuts:
                out.append(Issue(shot, "blocker", "L1",
                                 "`镜内状态:` 有 %d 段，`分镜:` 有 %d 段——必须一一对应"
                                 % (n_led, n_cuts)))

    # ── L2：同段内「肢体探入」＋「身体位移」而无次序词 ──
    for cl in _CLAUSE.split(_field(pos, "动作")):
        r = [v for v in REACH_VERBS if v in cl]
        m = [v for v in MOVE_VERBS if v in cl]
        if r and m and not any(k in cl for k in ORDER_MARKS):
            out.append(Issue(shot, "warning", "L2",
                             "同一段里既有「%s」又有「%s」却没写先后——模型会把两者叠在同一时刻"
                             "（手留在洞里、身体走开 → 橡皮手，rule 16.11）。原句：…%s…"
                             % (r[0], m[0], cl.strip()[:56])))
    return out


def gate(md_by_shot: dict[str, str], legacy: set[str] | None = None) -> list[Issue]:
    legacy = legacy or set()
    issues = [i for s in sorted(md_by_shot) for i in check(s, md_by_shot[s])]
    hard = [i for i in issues if i.level == "blocker" and i.shot not in legacy]
    if hard:
        raise SystemExit(
            "镜内逻辑不合格 %d 处（rule 16.10/16.11 · 格式契约 K33）：\n" % len(hard)
            + "\n".join("  %s [%s] %s" % (i.shot, i.code, i.detail) for i in hard))
    return issues


def _scan(root: str) -> int:
    n_files = blockers = 0
    cur = None
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in sorted(files):
            if not (fn.startswith("shot") and fn.endswith(".md")) or fn == "shotlist.md":
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, "ai_videos").replace(os.sep, "/")
            drama = rel.split("/5_6_")[0] if "/5_6_" in rel else os.path.dirname(rel)
            n_files += 1
            got = check(fn[:-3], io.open(p, encoding="utf-8").read())
            if not got:
                continue
            if drama != cur:
                print("\n%s" % drama)
                cur = drama
            for i in got:
                blockers += i.level == "blocker"
                print("  %s %s [%s] %s"
                      % ("❌" if i.level == "blocker" else "⚠", i.shot, i.code, i.detail[:150]))
    print("\n扫描 %d 个 shot md —— blocker %d" % (n_files, blockers))
    return blockers


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(1 if _scan(sys.argv[1] if len(sys.argv) > 1 else "ai_videos") else 0)
