# -*- coding: utf-8 -*-
"""多视角独立审稿：另起全新的 CLI 进程（`codex exec` / `claude -p`）判审稿类检查——Claude 与 Codex 通用。

用法（仓库根目录）：
    python tools/qc_review.py <出片目录> [--when 一镜到底]      # 出片后：看拼图（+ 峰值图）
    python tools/qc_review.py <技能目录> --pre                  # 出片前：看规格 + 开场图 + 峰值图
    通用参数：[--reviewer auto|codex|claude] [--sheet 拼图] [--timeout 300] [--dry-run]

设计（dota_yingxiong follow-up 263 / 266）
------------------------------------------
· **另起进程**而不是用代理自带的子代理：Claude 有子代理、Codex 没有，改成脚本后两边能力对等。
  进程跑在临时空目录、只读，只拿到图与规格副本，读不到作者写的 `review.md`。
· **多视角，每个视角一个独立进程**（登记表里每条检查的 `perspective`）：
    character —— 出场几个角色就开几个审稿人，每个代入一个角色、只判与自己有关的立场与视线
                （用户：「每个人物都应该站在自己的立场上独立思考」）；任一角色判不过即不过；
    director  —— 规格、结构、比例、起势收势；
    audience  —— 第一次看的观众，**不给规格**，只看画面说出发生了什么；
    fidelity  —— 原版还原，额外附峰值图对照。
· **轮换模型**：各视角轮流分给 Claude 与 Codex（默认先给「另一个」模型），并行跑；某个失败自动换另一个；
  都失败记「未审」写原因——绝不由作者代判。
· 还没有机检工具的机检项（auto = false）先由导演视角兜底，证据标「审稿兜底，待机检工具」。
· **三种结论、两层**（follow-up 354）：pass / fail / 审不了（材料缺 / 看不清），取消「拿不准就判 fail」；
  每项标【通用】（只看画面本身，不拿规格数字当判据）或【对照规格】（只有大偏差 fail，容差见 qc.SPEC_TOLERANCE）。
提示词与原始回复存 `.audit/adhoc_agents/{日期}/qc_review/`（纯文字审稿不是收费生成服务，不写 request_log.md）。
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qc  # noqa: E402
import qc_pre  # noqa: E402
import scale_table  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
SHEET_GLOBS = ("sheet*.jpg", "*_4fps*.jpg", "mc_*.jpg")
IMAGE_EXT = (".png", ".jpg", ".jpeg", ".webp")
FRAMING = {
    "director": "你是这部片的导演兼审片人，按规格逐项核对。",
    "audience": "你是第一次看这段画面的普通观众，没看过任何剧本。只凭眼睛看到的判断。",
    "fidelity": "你负责「原版还原」：DotA 1 原版技能长什么样，这段就该是什么样。附图里的峰值图是锁定的技能长相，对照它判。",
}


@dataclass
class Target:
    path: Path
    pre: bool
    images: dict[str, list[tuple[Path, str]]]     # 视角 → [(图, 这张图是什么)]；各视角看的图不同
    spec: str
    cast: list[scale_table.Height]
    stages: set[str]
    write: Callable[[list[tuple[str, str, str, str]]], None] = field(repr=False)


@dataclass(frozen=True)
class Task:
    name: str                  # 视角标签：director / audience / fidelity / 角色名
    perspective: str
    checks: tuple[qc.Check, ...]
    who: str = ""              # 角色视角：代入的角色键


def pick(order: str) -> list[str]:
    """auto：调用方是 Claude（有 CLAUDECODE）就先让 Codex 审，否则先让 Claude 审；另一个作后备。"""
    if order in ("codex", "claude"):
        return [order, "claude" if order == "codex" else "codex"]
    return ["codex", "claude"] if os.environ.get("CLAUDECODE") else ["claude", "codex"]


def find_sheet(rd: Path, art: Path, explicit: str, make: bool = True) -> Path:
    if explicit:
        return Path(explicit).resolve()
    if art.suffix.lower() in IMAGE_EXT:
        return art
    for g in SHEET_GLOBS:
        hit = sorted(rd.glob(g))
        if hit:
            return hit[-1]
    out = rd / "sheet_4fps.jpg"                               # 没有拼图就现出一张（每秒 4 帧、带时间码）
    if not make:
        return out                                            # dry-run 不写任何文件
    subprocess.run([sys.executable, str(REPO / "tools" / "motion_check.py"), str(art), "--sheet", str(out)],
                   cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if not out.exists():
        raise SystemExit(f"没有拼图，motion_check 也没出成：{out}")
    return out


def safe(fn: Callable[[], object], default: object) -> object:
    try:
        return fn()
    except SystemExit:
        return default                                        # 没有资料包清单的老技能：认不出角色与峰值图


def shot_point(shot_dir: Path) -> str:
    """六模块剧镜头目录 scenes/<场>/shots/<镜> → filming.json 里这一镜的 point；没有就空。"""
    try:
        ep = shot_dir.parents[3]
        scenes = json.loads((ep / "filming.json").read_text(encoding="utf-8"))["content"]["scenes"]
        sc = next(x for x in scenes if x["id"] == shot_dir.parents[1].name)
        return str(next(x for x in sc["shots"] if x["id"] == shot_dir.name).get("point") or "")
    except (OSError, ValueError, KeyError, StopIteration, IndexError):
        return ""


def build_target(p: Path, pre: bool, a: argparse.Namespace) -> Target:
    sd = p if pre else p.parent.parent
    keys = safe(lambda: qc_pre.cast(sd), [])
    cast = scale_table.heights(qc_pre.drama_name(sd), keys) if keys else []
    fr = safe(lambda: qc_pre.frames(sd), {})
    if not pre and (p / "prompt.txt").is_file():
        # 出片后对照的是这一条**提交时**的 prompt，不是卡上现在的规格：卡后来改了，旧条不按新规格判（follow-up 354；
        # 六模块剧镜头条本来就这样，chuanyue_yiri follow-up 054）
        spec = (p / "prompt.txt").read_text(encoding="utf-8")[:6000].strip()
    else:
        spec = qc_pre.spec_text(qc_pre.card_of(sd))
    point = "" if pre else shot_point(sd)
    if point:                                                  # 看点不进 prompt，只给审查（chuanyue_yiri follow-up 058/059）
        spec += ("\n\n## 看点（分镜 point：这一镜要观众看懂或感到什么）\n" + point +
                     "\n先写你关掉声音看到的这一镜在讲什么，再对照看点。")
    label = {"start": "我们的开场图（视频第一帧）", "peak": "我们的峰值图（锁定的技能长相）"}
    ours = [(fr[k], label[k]) for k in ("start", "peak") if k in fr]
    idents = [(i, "出场角色的身份立绘") for i in safe(lambda: qc_pre.identity_images(sd), [])]
    origin = [(o, "DotA 1 原版参考截图") for o in qc_pre.original_refs(sd)]
    peak = [x for x in ours if x[0] == fr.get("peak")]
    if pre:
        images = {"character": ours, "director": ours + idents, "fidelity": origin + peak}
        return Target(p, True, images, spec, cast, set(qc_pre.PRE_STAGES), lambda items: qc_pre.record(sd, items))
    art = qc.artifact_of(p)
    sheet = [(find_sheet(p, art, a.sheet, make=not a.dry_run), "成片的每秒 4 帧拼图")]
    images = {"character": sheet, "director": sheet, "audience": sheet, "fidelity": sheet + peak + origin[:1]}
    reg = qc.registry(qc.drama_dir_of(p))
    return Target(p, False, images, spec, cast, {a.stage},
                  lambda items: qc.record_into(p / "qc.json", qc.sha(art), reg, items, {"artifact": art.name}))


def tasks_for(checks: list[qc.Check], cast: list[scale_table.Height]) -> list[Task]:
    out = []
    char = tuple(c for c in checks if c.perspective == "character")
    for h in cast if char else []:
        out.append(Task(h.name, "character", char, h.key))
    for persp in ("director", "audience", "fidelity"):
        group = tuple(c for c in checks if c.perspective != "character" and
                      (c.perspective == persp or (persp == "director" and c.perspective not in FRAMING)))
        if group:
            out.append(Task(persp, persp, group))
    return out


VERDICT_RULES = """## 怎么下结论（三种，follow-up 354）
- pass：看清楚了，没有问题。
- fail：看清楚了，有问题；evidence 写出看到的错。
- 审不了：判这一项要用的东西不在附图或文字里（reason＝材料缺，写明缺什么），或者东西在、但拼图太小太粗看不清（reason＝看不清，写明哪里看不清）。
  审不了不是不通过：不要因为看不清就判 fail，也不要因为看不清就判 pass。"""
RULES = VERDICT_RULES + f"""
## 每项前面标了层
- 【通用】只看画面本身有没有观众看得出的错（物体凭空出现、人数变化、动作没有因果、该看的不看、像摆件……），不拿规格里的秒数、措辞、身高数字当判据；规格只用来知道这一段要讲什么。
- 【对照规格】拿画面和规格比，只有大的偏差才判 fail。没有单独写容差的按这条：{qc.SPEC_TOLERANCE}"""


def prompt_for(task: Task, t: Target) -> str:
    imgs = t.images.get(task.perspective, [])
    names = "；".join(f"第 {i + 1} 张＝{desc}" for i, (_, desc) in enumerate(imgs)) or "（没有图）"
    heights = "；".join(f"{h.name} {h.meters:g} m（{h.kind}）" if h.meters else f"{h.name} 身高未写" for h in t.cast)
    if task.perspective == "character":
        me = next(h for h in t.cast if h.key == task.who)
        head = (f"你就是「{me.name}」。站在你自己的立场独立思考：每一拍你看到什么、想要什么、该做什么。"
                "只判与你自己有关的行为与视线，别替别的角色操心。"
                "逐拍问自己（chuanyue_yiri follow-up 063）：我面对的是谁、懂不懂我的话；我说的话、手势、姿态、表情强度、"
                "看谁、对别人的回应，是不是此刻的我会有的；只因为剧情需要才做的举动、比事情本身还大的表情都判 fail，"
                "并写出此刻的我会怎么说、怎么做。")
    else:
        head = FRAMING[task.perspective]
    spec = "" if task.perspective == "audience" else f"\n## 规格（这条片子本该是什么样）\n{t.spec or '（没有找到规格）'}\n"
    note = ("\n注意：我们的开场图、峰值图是真人电影质感的设计稿，本来就不是游戏画面；判「参考是不是原版 / 6.83d」只看原版参考截图。"
            if task.perspective == "fidelity" else "")
    if not t.pre:   # 拼图每格左上角的黄色时间码是审片工具加的，不在成片里（dota_yingxiong follow-up 282：被当成画面文字误判）
        note += "\n注意：拼图每格左上角的黄色时间码是审片工具加上去的，成片里没有；判画面文字时不算它。"
    items = "\n".join(f"- 【{qc.LAYER_NAME[c.layer]}】{c.id}：{c.desc}" + (f"（判法：{c.how}）" if c.how else "")
                      + (f"（容差：{c.tolerance}）" if c.layer == "spec" and c.tolerance else "") for c in task.checks)
    schema = ", ".join(f'{{"id":"{c.id}","verdict":"pass|fail|审不了","reason":"","evidence":"…"}}' for c in task.checks)
    cast_line = f"\n出场角色与人物卡身高：{heights}\n" if t.cast and task.perspective != "audience" else ""
    return (f"{head}\n只根据附图（{names}）和下面给你的文字判定，不要读取或运行任何其他东西。"
            f"evidence 必须指到具体图、格、秒数或规格里的哪一拍。{note}\n{cast_line}{spec}\n"
            f"{VERDICT_RULES if task.perspective == 'audience' else RULES}\n"
            f"## 逐项检查\n{items}\n\n## 输出\n只输出一个 JSON 数组，不要任何其他文字（reason 只在审不了时填 材料缺 或 看不清）：[{schema}]")


def run_reviewer(who: str, prompt: str, images: list[Path], work: Path, timeout: int) -> str:
    local = []
    for i, img in enumerate(images):
        dst = work / f"{i + 1}_{img.name}"
        shutil.copy(img, dst)                                 # 只把图的副本放进空目录
        local.append(dst.name)
    if who == "codex":
        last = work / "_last.txt"
        cmd = ["codex", "exec", "--skip-git-repo-check", "-s", "read-only", "-o", str(last)]
        for name in local:
            cmd += ["-i", name]
        subprocess.run(cmd, input=prompt, cwd=work, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=timeout, shell=os.name == "nt")
        return last.read_text(encoding="utf-8") if last.exists() else ""
    reads = "、".join(str(work / n) for n in local)
    cmd = ["claude", "-p", "--output-format", "text", "--allowedTools", "Read", "--add-dir", str(work)]
    r = subprocess.run(cmd, input=f"先用 Read 工具逐张读取图片：{reads}。\n{prompt}", cwd=work, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=timeout, shell=os.name == "nt")
    return r.stdout


UNKNOWN = {"审不了", "unknown", "cannot_judge", "无法判定"}


def parse(raw: str, wanted: set[str]) -> dict[str, tuple[str, str, str]]:
    """取回复里第一个合法的 JSON 数组；数组后面多写的文字不管（follow-up 296：贪婪正则吞进尾巴文字导致整次审稿崩）。
    返回 检查id → (结论, 证据, 审不了的原因)；审不了没写合法原因的按「看不清」。"""
    rows, dec = None, json.JSONDecoder()
    for m in re.finditer(r"\[\s*\{", raw):
        try:
            obj, _ = dec.raw_decode(raw[m.start():])
        except ValueError:
            continue
        if isinstance(obj, list):
            rows = obj
            break
    if rows is None:
        return {}
    out = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        cid, verdict = str(row.get("id", "")), str(row.get("verdict", "")).strip().lower()
        if cid not in wanted:
            continue
        ev = str(row.get("evidence", "")).strip()
        if verdict in ("pass", "fail"):
            out[cid] = (verdict, ev, "")
        elif verdict in UNKNOWN:
            reason = str(row.get("reason", "")).strip()
            out[cid] = ("审不了", ev, reason if reason in qc.REASONS else "看不清")
    return out


Result = tuple[Task, str, dict[str, tuple[str, str, str]], list[str]]


def run_task(task: Task, t: Target, order: list[str], timeout: int, audit: Path) -> Result:
    prompt, notes = prompt_for(task, t), []
    for who in order:
        with tempfile.TemporaryDirectory(prefix="qc_review_") as tmp:
            try:
                raw = run_reviewer(who, prompt, [img for img, _ in t.images.get(task.perspective, [])], Path(tmp), timeout)
            except (OSError, subprocess.TimeoutExpired) as exc:
                raw, notes = "", notes + [f"{who} 调用失败：{exc}"]
        d = audit / f"{t.path.name}_{task.perspective}_{task.who or task.name}_{who}"
        d.mkdir(parents=True, exist_ok=True)
        (d / "prompt.md").write_text(prompt, encoding="utf-8")
        (d / "output.md").write_text(raw or "（无输出）", encoding="utf-8")
        got = parse(raw, {c.id for c in task.checks})
        if got:
            return task, who, got, notes
        notes.append(f"{who} 没给出可解析的结论")
    return task, "", {}, notes


def aggregate(results: list[Result], checks: list[qc.Check]) -> list[tuple[str, ...]]:
    """每条检查汇总各视角的结论：任一视角不过即不过；否则有视角审不了即审不了（任一缺材料就记材料缺）；
    全都过才过；其余（有视角没给结论）记未审。"""
    items = []
    for c in checks:
        votes = [(task, who, got.get(c.id), notes) for task, who, got, notes in results if c in task.checks]
        if not votes:
            items.append((c.id, "未审", "review", "认不出出场角色（无资料包清单），角色视角无从代入"))
            continue
        tag = "·审稿兜底，待机检工具" if c.kind == "machine" else ""
        ev = "；".join(f"[{task.name}·{who or '无审稿人'}{tag}] {v[1] if v else '；'.join(n) or '没给结论'}"
                      for task, who, v, n in votes)
        verdicts = [v[0] for _, _, v, _ in votes if v]
        reasons = {v[2] for _, _, v, _ in votes if v and v[0] == "审不了"}
        if "fail" in verdicts:
            items.append((c.id, "fail", "review", ev))
        elif reasons:
            items.append((c.id, "审不了", "review", ev, "材料缺" if "材料缺" in reasons else "看不清"))
        else:
            items.append((c.id, "pass" if len(verdicts) == len(votes) else "未审", "review", ev))
    return items


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("target")
    ap.add_argument("--pre", action="store_true", help="出片前：审技能目录的规格、开场图与峰值图")
    ap.add_argument("--stage", default="video")
    ap.add_argument("--when", action="append", default=[])
    ap.add_argument("--reviewer", default="auto", choices=("auto", "codex", "claude"))
    ap.add_argument("--sheet", default="")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--dry-run", action="store_true", help="只打印各视角的提示词，不调审稿人、不写任何文件")
    a = ap.parse_args(argv)
    t = build_target(Path(a.target).resolve(), a.pre, a)
    reg = qc.registry(qc.drama_dir_of(t.path))
    checks = [c for c in reg.values() if c.stage in t.stages and (c.kind == "review" or not c.auto)
              and (not c.when or c.when in a.when)]
    if not checks:
        print("这一环节没有要审稿的检查", file=sys.stderr)
        return 0
    tasks = tasks_for(checks, t.cast)
    if a.dry_run:
        for task in tasks:
            print(f"===== 视角：{task.name} =====\n{prompt_for(task, t)}\n")
        return 0
    order = pick(a.reviewer)
    audit = REPO / ".audit" / "adhoc_agents" / dt.date.today().isoformat() / "qc_review"
    jobs = [(task, order[i % 2:] + order[:i % 2]) for i, task in enumerate(tasks)]       # 视角轮流先给两个模型
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda j: run_task(j[0], t, j[1], a.timeout, audit), jobs))
    items = aggregate(results, checks)
    t.write(items)
    used = "、".join(f"{task.name}→{who or '失败'}" for task, who, _, _ in results)
    print(f"多视角审稿（{used}）：" + "、".join(f"{i[0]}={i[1]}" + (f"（{i[4]}）" if len(i) > 4 else "") for i in items))
    return 0


if __name__ == "__main__":
    sys.exit(main())
