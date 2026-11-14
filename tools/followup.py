# -*- coding: utf-8 -*-
"""follow-up 与 changelog 的唯一写入口 —— 让「每个改动都有记录」机械地发生，而不是靠记得。

用法（仓库根目录；<项目> 可写 `dota_yingxiong` 或 `specs/ai_video/dota_yingxiong`）：
    python tools/followup.py new <项目> --slug <英文短名> --instruction "<用户指令>" --summary "<一行摘要>" \
        [--stage 6] [--severity medium] [--artifact <路径> ...] [--owner <会话>]
    python tools/followup.py done <项目> <NNN> --updated "<路径> — <改了什么>" ... --verified "<怎么验的 / 未审及原因>" \
        [--cost "<任务号 · 积分>"] [--no-conflict "<查过没冲突的范围>"]
    python tools/followup.py merge [<项目> ...] [--all]          # 周期性汇聚（Stop 钩子每次先跑）
    python tools/followup.py check [<项目> ...] [--all] [--hook] [--owner <会话>]

为什么必须是工具（2026-10-26，dota_yingxiong 过去 7 天日志复盘）
---------------------------------------------------------------
CONVENTIONS「Follow-up prompt handling」原本只是一段文字，各会话手工往月度文件和 changelog 末尾追加。
一周 225 条 follow-up 里实测：
  · **25 条没有 changelog**，全在最忙的两天（10-24 缺 13、10-25 缺 11）——越忙越漏；
  · **7 个编号撞号**（045/050/051/053/057/096…），两个会话各读到同一个「下一个号」；
  · **内容串写**：046 正文里混进树精小兵的第二轮，089 底下挂着泉水布局的执行结果，
    251 的 changelog 无标题地夹在 254 条目里——「追加到文件末尾」在并发下就等于写进别人的条目；
  · changelog 标题出现五种以上写法，连脚本统计都会算错 6 倍。
所以：`new` 加锁分配编号、一次写好 follow-up 与 changelog 骨架（不可能只写一边）；
`done` 把执行结果写回**该编号自己的条目**；`check` 在收尾时机检。

各自记、周期性汇聚（2026-10-27，dota_yingxiong follow-up 280）
-------------------------------------------------------------
用户：「不要有 single point of blocker，你可以先各自记载 follow up 之后在周期性汇聚」。
原先任何一个会话丢下一条「待补」超过 6 小时，全剧所有会话的 Stop 钩子和 `skill_pack submit` 都被拦
（10-26/27 两次：另一会话的 267、269 挡住骷髅王出片）。现在：
  · `new` 只在锁里领编号（锁只罩「读最大号 + 写一个新文件」，毫秒级，残留锁自动清），条目写进
    `follow_ups/_inbox/NNN-slug.md`——一条一个文件，记归属会话；**不碰共用的月度文件与 changelog**；
  · `done` 只改这条自己的文件，写完顺手汇聚；`merge` 把已收尾的条目按编号并进月度文件与 changelog，
    Stop 钩子每次先跑一遍（这就是「周期性汇聚」）；还在做的条目留在 _inbox，`revised_prompt` 照样带上；
  · **只拦自己**：钩子与出片前日志闸门只拦「本会话」超过 6 小时没收尾的条目；别的会话的、旧的、
    格式不对的都只提示（·），由各自的会话或汇聚处理，不再挡别人。
会话归属：`--owner`，否则环境变量 FOLLOWUP_OWNER / CLAUDE_CODE_SESSION_ID / CODEX_SESSION_ID / CODEX_THREAD_ID，
钩子模式还读 stdin 里的 session_id。认不出会话的条目不拦任何人（Codex 收尾显式跑 check 时可传 --owner）。

只对 ENFORCE_FROM 之后的条目生效（仓库惯例：规则不回溯旧产物）。
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SPECS = REPO / "specs"
ENFORCE_FROM = "2026-10-26"
STALE_HOURS = 6.0               # 「待补」允许挂着的时长：进行中的活不拦，丢下不管的才拦（只拦自己的）
PENDING = "待补"
PENDING_MARK = f"（{PENDING}"     # 只认骨架占位符；正文里写「其余图待补」是正常描述，不能算没收尾
LOCK_NAME = ".followup.lock"
LOCK_WAIT_S, LOCK_STALE_S = 30.0, 120.0
INBOX = "_inbox"
OWNER_ENV = ("FOLLOWUP_OWNER", "CLAUDE_CODE_SESSION_ID", "CODEX_SESSION_ID", "CODEX_THREAD_ID")

FU_HEAD = re.compile(r"^## (\d+) — (\d{4}-\d\d-\d\d)([^\n]*)$", re.M)
FU_CANON = re.compile(r"^## \d{3,} — \d{4}-\d\d-\d\d \d\d:\d\d:\d\d — \S")
CL_CANON = re.compile(r"^## Follow-up (\d{3,}) — (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)$", re.M)
ENTRY_META = re.compile(r"^<!-- followup-entry owner=(\S*) month=(\d{6}) -->$", re.M)
CL_SPLIT = "\n<!-- changelog -->\n"


@dataclass(frozen=True)
class Problem:
    project: str
    kind: str
    detail: str
    blocking: bool


@dataclass
class Entry:
    """_inbox 里的一条：follow-up 段 + changelog 段，同一个文件，只有归属会话会去改它。"""
    n: int
    path: Path
    owner: str
    month: str
    fu: str
    cl: str

    def save(self) -> None:
        self.path.write_text(f"<!-- followup-entry owner={self.owner} month={self.month} -->\n\n"
                             f"{self.fu}\n{CL_SPLIT}\n{self.cl}\n", encoding="utf-8")


def resolve(project: str) -> Path:
    p = Path(project)
    if not p.is_absolute():
        p = REPO / p
    if (p / "user_input").is_dir():
        return p
    hits = [d for d in SPECS.glob(f"*/{project}") if (d / "user_input").is_dir()]
    if len(hits) != 1:
        raise SystemExit(f"找不到唯一的项目 {project}（候选 {[str(h) for h in hits]}）")
    return hits[0]


def now() -> dt.datetime:
    return dt.datetime.now().replace(microsecond=0)


def current_owner() -> str:
    for k in OWNER_ENV:
        v = os.environ.get(k, "").strip()
        if v:
            return v
    return ""


class Lock:
    """跨会话互斥：O_EXCL 建锁文件。只罩「读最大号 + 写新文件」与汇聚这两小段，不罩任何人的工作过程。"""

    def __init__(self, spec: Path, wait_s: float = LOCK_WAIT_S) -> None:
        self.path = spec / LOCK_NAME
        self.wait_s = wait_s

    def __enter__(self) -> "Lock":
        t0 = time.monotonic()
        while True:
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(os.getpid()).encode())
                os.close(fd)
                return self
            except FileExistsError:
                try:
                    if time.time() - self.path.stat().st_mtime > LOCK_STALE_S:
                        self.path.unlink(missing_ok=True)       # 崩溃留下的锁
                        continue
                except FileNotFoundError:
                    continue
                if time.monotonic() - t0 > self.wait_s:
                    raise SystemExit(f"等锁超时：{self.path}（另一会话正在写；超过 {LOCK_STALE_S:.0f}s 视为残留）")
                time.sleep(0.2)

    def __exit__(self, *exc: object) -> None:
        self.path.unlink(missing_ok=True)


def fu_files(spec: Path) -> list[Path]:
    """已汇聚的月度文件（不含 _inbox）。"""
    return sorted((spec / "user_input" / "follow_ups").glob("*.md"))


def inbox_dir(spec: Path) -> Path:
    return spec / "user_input" / "follow_ups" / INBOX


def inbox_entries(spec: Path) -> tuple[list[Entry], list[Path]]:
    """(能读懂的条目, 读不懂的文件)。"""
    good, bad = [], []
    d = inbox_dir(spec)
    for f in sorted(d.glob("*.md")) if d.is_dir() else []:
        t = f.read_text(encoding="utf-8")
        m = ENTRY_META.search(t)
        if not m or CL_SPLIT not in t:
            bad.append(f)
            continue
        fu, cl = t[m.end():].split(CL_SPLIT, 1)
        h = FU_HEAD.search(fu)
        if not h:
            bad.append(f)
            continue
        good.append(Entry(int(h.group(1)), f, m.group(1), m.group(2), fu.strip("\n"), cl.strip("\n")))
    return sorted(good, key=lambda e: e.n), bad


def headings(spec: Path) -> list[tuple[int, str, str, Path]]:
    """月度文件 + _inbox 里所有 follow-up 标题——分配编号、查撞号都要看两处。"""
    out = []
    d = inbox_dir(spec)
    for f in fu_files(spec) + (sorted(d.glob("*.md")) if d.is_dir() else []):
        for m in FU_HEAD.finditer(f.read_text(encoding="utf-8")):
            out.append((int(m.group(1)), m.group(2), m.group(0), f))
    return out


def regen_revised(spec: Path) -> None:
    ui = spec / "user_input"
    raw = (ui / "raw_prompt.md").read_text(encoding="utf-8").rstrip() if (ui / "raw_prompt.md").exists() else ""
    parts = [raw] + [f.read_text(encoding="utf-8").strip() for f in fu_files(spec)]
    parts += [e.fu for e in inbox_entries(spec)[0]]              # 还没汇聚的意图也要让下游看到
    (ui / "revised_prompt.md").write_text("\n\n".join(p for p in parts if p) + "\n", encoding="utf-8")


def cmd_new(a: argparse.Namespace) -> int:
    spec = resolve(a.project)
    with Lock(spec):
        n = max((n for n, *_ in headings(spec)), default=0) + 1
        ts = now()
        stamp = ts.strftime("%Y-%m-%d %H:%M:%S")
        month = f"{ts:%Y%m}"
        hint = []
        if a.stage:
            hint.append(f"> target_stage: {a.stage}")
        if a.artifact:
            hint += ["> target_artifacts:"] + [f">   - {p}" for p in a.artifact]
        if a.severity:
            hint.append(f"> severity: {a.severity}")
        fu = [f"## {n:03d} — {stamp} — {a.slug}", ""]
        fu += (hint + [""]) if hint else []
        fu += ["### 指令", "", a.instruction.strip(), "", "### 摘要", "", a.summary.strip()]
        cl = [f"## Follow-up {n:03d} — {stamp}",
              f"Source: user_input/follow_ups/{month}.md - section {n:03d}",
              f"Summary: {a.summary.strip().splitlines()[0]}", "",
              "Auto-updated:", f"- （{PENDING}：执行后用 `python tools/followup.py done` 写入）", "",
              f"验证: （{PENDING}）", "",
              f"No conflicts found in: （{PENDING}）"]
        inbox_dir(spec).mkdir(parents=True, exist_ok=True)
        slug = re.sub(r"[^\w.-]+", "-", a.slug)[:60]
        Entry(n, inbox_dir(spec) / f"{n:03d}-{slug}.md", a.owner or current_owner(), month,
              "\n".join(fu), "\n".join(cl)).save()
        regen_revised(spec)
    print(f"{n:03d}")
    print(f"FOLLOWUP 已记 {spec.name} §{n:03d}（本会话的 _inbox，收尾后自动汇聚进月度文件与 changelog）；"
          f"执行完用 `done {spec.name} {n:03d}` 补全", file=sys.stderr)
    return 0


def entry_span(text: str, n: int) -> tuple[int, int]:
    m = re.search(rf"^## Follow-up {n:03d} — [^\n]*$", text, re.M)
    if not m:
        raise SystemExit(f"changelog 里没有 Follow-up {n:03d} 的规范条目（先用 `new` 建）")
    nxt = re.search(r"^## ", text[m.end():], re.M)
    return m.start(), (m.end() + nxt.start()) if nxt else len(text)


def finished(body: str, a: argparse.Namespace) -> str:
    """把一条 changelog 骨架填成收尾版（保留之前 done 写过的产物行）。"""
    head, src, summ = body.splitlines()[0:3]
    old_upd = re.findall(r"^- (?!（" + PENDING + r").*$", body.split("Auto-updated:")[-1].split("\n\n")[0], re.M)
    upd = old_upd + [f"- {u}" for u in a.updated]
    if not upd:
        raise SystemExit("至少要一条 --updated（没有产物改动就写 --updated \"无产物改动 — 原因\"）")
    new = [head, src, summ, "", "Auto-updated:", *upd, "", f"验证: {a.verified}"]
    if a.cost:
        new.append(f"费用: {a.cost}")
    new += ["", f"No conflicts found in: {a.no_conflict or '（未单独核查）'}"]
    return "\n".join(new)


def _merge_locked(spec: Path) -> int:
    """把 _inbox 里已收尾的条目按编号并进月度文件与 changelog（调用方持锁）。"""
    done = [e for e in inbox_entries(spec)[0] if PENDING_MARK not in e.cl]
    for e in done:
        month = spec / "user_input" / "follow_ups" / f"{e.month}.md"
        with month.open("a", encoding="utf-8") as fh:
            fh.write(f"\n---\n\n{e.fu}\n")
        with (spec / "changelog.md").open("a", encoding="utf-8") as fh:
            fh.write(f"\n{e.cl}\n\n")
        e.path.unlink()
    if done:
        regen_revised(spec)
    return len(done)


def cmd_done(a: argparse.Namespace) -> int:
    spec = resolve(a.project)
    n = int(a.number)
    with Lock(spec):
        mine = [e for e in inbox_entries(spec)[0] if e.n == n]
        if mine:
            e = mine[0]
            e.cl = finished(e.cl, a)
            e.save()
            _merge_locked(spec)
        else:                                   # 已汇聚 / 本改动之前建的条目：原位改 changelog
            cl = spec / "changelog.md"
            text = cl.read_text(encoding="utf-8")
            s, e_ = entry_span(text, n)
            cl.write_text(text[:s] + finished(text[s:e_], a) + "\n\n" + text[e_:].lstrip("\n"), encoding="utf-8")
    print(f"FOLLOWUP {spec.name} {n:03d} 已收尾", file=sys.stderr)
    return 0


def all_specs() -> list[Path]:
    return sorted(d for d in SPECS.glob("*/*") if (d / "user_input" / "follow_ups").is_dir())


def cmd_merge(a: argparse.Namespace) -> int:
    specs = [resolve(p) for p in a.project] if a.project else all_specs()
    total = 0
    for spec in specs:
        with Lock(spec):
            total += _merge_locked(spec)
    print(f"汇聚 {total} 条已收尾的 follow-up", file=sys.stderr)
    return 0


def _age_h(stamp: str) -> float:
    return (now() - dt.datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S")).total_seconds() / 3600


def check_one(spec: Path, me: str = "") -> list[Problem]:
    """只有「本会话（me）自己的」问题会拦（blocking）；别的会话的、旧的、读不出归属的只提示。"""
    name, out = spec.name, []
    heads = headings(spec)
    entries, bad = inbox_entries(spec)
    by_n = {e.n: e for e in entries}
    mine = {e.n for e in entries if me and e.owner == me}
    cl_text = (spec / "changelog.md").read_text(encoding="utf-8") if (spec / "changelog.md").exists() else ""
    canon = {int(n): stamp for n, stamp in CL_CANON.findall(cl_text)}
    seen: dict[int, int] = {}
    for n, *_ in heads:
        seen[n] = seen.get(n, 0) + 1
    for n, d, h, f in heads:
        if d < ENFORCE_FROM:
            continue
        if seen[n] > 1:
            out.append(Problem(name, "撞号", f"{n:03d} 在 follow_ups 里出现 {seen[n]} 次", n in mine))
        if not FU_CANON.match(h):
            out.append(Problem(name, "格式", f"{f.name}：「{h[:60]}」不是 `## NNN — YYYY-MM-DD HH:mm:ss — slug`",
                               n in mine))
        if f.parent.name != INBOX and n not in canon:
            out.append(Problem(name, "漏记", f"follow-up {n:03d}（{d}）没有规范 changelog 条目 `## Follow-up {n:03d} — …`",
                               False))
    for n, stamp in canon.items():                 # 已汇聚的条目只会是收尾过的；剩下的是改动前留下的
        if stamp[:10] < ENFORCE_FROM:
            continue
        s, e = entry_span(cl_text, n)
        if PENDING_MARK in cl_text[s:e]:
            out.append(Problem(name, "未收尾", f"Follow-up {n:03d} 还有「{PENDING}」（已 {_age_h(stamp):.1f} 小时，"
                                               f"汇聚前的旧条目，归属不明，只提示）", False))
    for e in entries:
        m = CL_CANON.search(e.cl)
        if not m or m.group(2)[:10] < ENFORCE_FROM:
            continue
        who = "本会话" if e.n in mine else f"会话 {e.owner[:8] or '未知'}"
        if PENDING_MARK in e.cl:
            age = _age_h(m.group(2))
            out.append(Problem(name, "未收尾", f"Follow-up {e.n:03d} 还有「{PENDING}」（{who}，已 {age:.1f} 小时）",
                               e.n in mine and age > STALE_HOURS))
        else:
            out.append(Problem(name, "待汇聚", f"Follow-up {e.n:03d} 已收尾、还在 _inbox（下次 merge 并入）", False))
    for f in bad:
        out.append(Problem(name, "格式", f"_inbox/{f.name} 读不出条目结构（不要手改 _inbox 文件）", False))
    return out


def cmd_check(a: argparse.Namespace) -> int:
    me = a.owner or ""
    if a.hook:
        try:
            payload = json.loads(sys.stdin.read() or "{}")
        except json.JSONDecodeError:
            payload = {}
        if payload.get("stop_hook_active"):
            return 0                                   # 同一次收尾只拦一回，避免死循环
        me = me or str(payload.get("session_id") or "")
    me = me or current_owner()
    specs = [resolve(p) for p in a.project] if a.project else all_specs()
    if a.hook:                                         # 周期性汇聚：每次收尾顺手把已收尾的条目并进去
        for spec in specs:
            try:
                with Lock(spec, wait_s=2.0):
                    _merge_locked(spec)
            except SystemExit:
                pass                                   # 别的会话正在写：这次不汇聚，下次再来，不拦人
    probs = [p for s in specs for p in check_one(s, me)]
    block = [p for p in probs if p.blocking]
    show = [p for p in probs if p.kind != "待汇聚"]
    if show and not (a.hook and not block):
        for p in show:
            print(f"{'✗' if p.blocking else '·'} [{p.project}] {p.kind}：{p.detail}", file=sys.stderr)
    if block:
        print(f"\n本会话有 {len(block)} 处 follow-up 要收尾：用 `python tools/followup.py done` 写"
              f"（别的会话的条目只提示、不拦；CONVENTIONS §Follow-up prompt handling）。", file=sys.stderr)
        return 2 if a.hook else 1
    if not a.hook:
        print(f"follow-up 日志检查通过：本会话没有要收尾的（{len(specs)} 个项目，{ENFORCE_FROM} 起；· 为其他会话或旧条目，只提示）",
              file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new")
    n.add_argument("project")
    n.add_argument("--slug", required=True)
    n.add_argument("--instruction", required=True)
    n.add_argument("--summary", required=True)
    n.add_argument("--stage", type=int)
    n.add_argument("--severity", choices=("low", "medium", "high"))
    n.add_argument("--artifact", action="append", default=[])
    n.add_argument("--owner", help="归属会话；缺省读 FOLLOWUP_OWNER / CLAUDE_CODE_SESSION_ID / CODEX_* 环境变量")
    d = sub.add_parser("done")
    d.add_argument("project")
    d.add_argument("number")
    d.add_argument("--updated", action="append", default=[])
    d.add_argument("--verified", required=True)
    d.add_argument("--cost")
    d.add_argument("--no-conflict")
    m = sub.add_parser("merge", help="把各会话 _inbox 里已收尾的条目汇聚进月度文件与 changelog")
    m.add_argument("project", nargs="*")
    m.add_argument("--all", action="store_true")
    c = sub.add_parser("check")
    c.add_argument("project", nargs="*")
    c.add_argument("--all", action="store_true")
    c.add_argument("--hook", action="store_true", help="Stop 钩子模式：先汇聚，再只在本会话有必须修的问题时输出并以 2 退出")
    c.add_argument("--owner", help="以哪个会话的身份检查；缺省读钩子 stdin 的 session_id 或环境变量")
    a = ap.parse_args(argv)
    return {"new": cmd_new, "done": cmd_done, "merge": cmd_merge, "check": cmd_check}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
