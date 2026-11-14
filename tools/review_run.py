# -*- coding: utf-8 -*-
"""审查单：每次审查先出一张清单（要哪些独立审稿人、各自必查什么），审稿人审完自己打勾；全部打勾才算审完。出片前最多循环 3 轮；每轮收轮只记结论，不等用户 review，用户只在出片时确认。

用法（仓库根目录）：
    python tools/review_run.py new <集目录> --stage pregen|story|filming|prompt|take|cut|episode|full [--scenes s1,s2] [--known "…"]
    python tools/review_run.py new <集目录> --after <上一轮审查单> --changes <这轮改了什么.md>   # 开下一轮（最多 3 轮）
    python tools/review_run.py tick <审查单> <代号> --slot a|b --report <报告.md> --by <模型>/<代号>__<a|b>   # v5（v2 单不带 --slot，--by <模型>/<代号>）
    python tools/review_run.py tick … --attest-log <codex exec 日志>    # Codex 沙箱跑不了 python：调用方凭运行日志代为登记
    python tools/review_run.py adjudicate <审查单> <代号> --report <裁决.md> --by <模型>/<代号>__judge
    python tools/review_run.py fail <审查单> <代号> [--slot a|b|judge] --note "为什么没审成"
    python tools/review_run.py dispatch <审查单> <代号> [--slot a|b|judge] --runner … --model … --prompt-file …
    python tools/review_run.py issues <审查单>                          # 由评分＋问题表推出分级问题清单 issues.json / issues.md
    python tools/review_run.py fix <审查单> <I编号> --solution "…" [--status planned|implemented|wontfix] [--reason "…"] [--file <改了的文件>…] [--before <旧图> --after <新图>…]
    python tools/review_run.py corrections <审查单>                     # 修复页：每个问题怎么修的、首帧前后、分镜文字 diff、下一轮复核结果
    python tools/review_run.py status|gate <审查单>
    python tools/review_run.py conclude <审查单> [--verdict "…"]        # 收轮：写「结果.md」与结论（可出片 / 不可出片＋理由），状态→已收轮
    python tools/review_run.py confirm <审查单> --quote "用户原话"      # 出片时用户在对话里同意后登记（shot_take 出片前会查）
    python tools/review_run.py migrate [<剧目录或审查单>]              # 旧状态「待用户确认」→「已收轮」（写进 log）
    python tools/review_run.py list <剧目录或集目录>
    python tools/review_run.py can-submit <集目录> <镜头key…>          # shot_take 出片前调用

出片前的流程（用户 2026-11-07，chuanyue_yiri follow-up 035）
--------------------------------------------------------------
1. `new --stage pregen` 出审查单：名册 `.agents/references/project/review_roster.json` 按「阶段 × 法则 × 范围」排审稿人，
   每位都有编号的必查项（must）；第 2、3 轮另加「R：复核上一轮的问题」。
2. 每位审稿人用全新上下文拿任务书审，报告在「## 必查项」里逐条写 ✓ / ✗，再自己 `tick`；作者不能代勾，缺必查项不能勾。
3. `gate`：没全勾就继续第 2 步；全勾了看结果——便宜的改动（除 Seedance 积分外都算便宜：改故事、分镜、prompt、编译器、
   Codex 出图、工具）直接改，写进 changes，再 `new --after` 开下一轮；最多 3 轮。
4. `conclude` 写结果与结论（可出片 / 不可出片＋理由），状态「已收轮」——每轮审查不设用户 review 闸门（用户 2026-11-08）。
   用户的确认只在出片时：用户在对话里同意出片后 `confirm --quote`。开了审查闸门的剧（workflow.json `"review_gate": "required"`），
   shot_take 提交前 `can-submit` 要求覆盖该场的最新一张已收轮出片前审查单已由用户确认、材料未变。
5. `corrections` 生成修复页（corrections.json / .md）：每个有方案的问题、改了哪些文件、每镜首帧前后对比（审查时那张 → 现在 / 下一轮那张）、
   分镜文字逐字段 diff、下一轮审稿人的复核结果；`new` 会把被审的分镜、prompt 与首帧哈希存进 `materials/snapshot/` 作为「修复前」。
所有审查单存在 `ai_videos/<剧>/reviews/<集>_<时间>_<阶段>_r<轮>/`，管理站 /review-run 显示。

v5 双审（用户 2026-11-08，chuanyue_yiri follow-up）
-----------------------------------------------
每个审稿项（法则 × 范围）由名册 `reviewers` 排两位：a＝合适的 Claude 模型、b＝合适的 Codex 模型，各自拿 `items/<代号>__<a|b>.md`
独立审，按该类 rubric 每维 0–3 打分（≥2 要证据、1 要有问题行、0 要原因）。两位都勾后自动对比（`reconcile/<代号>.md`）：分歧
（差 ≥2，或一人 ≤1 一人 ≥2）与抽查（两人都 ≥2 的维度按 hash 抽 2 维）交裁决人（`items/<代号>__judge.md` → `adjudicate`）。
全部完成后 `issues` 推出分级问题（critical / major / verify / minor），`fix` 记方案与实施状态；严重与主要都 implemented 或
wontfix（写理由）后才能 `new --after` 开下一轮，changes.md 与 previous.md 由问题清单生成，下一轮审稿人用 R 逐条复核。
没有 slots 的 v2 单照旧（每项一位、必查项 ✓/✗）。
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import random
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROSTER = REPO / ".agents/references/project/review_roster.json"
CHECKLIST = "checklist.json"
RESULT = "结果.md"
SEVERITIES = ("重出", "可剪", "记录", "存疑")
FONT = "fontfile='C\\:/Windows/Fonts/msyh.ttc'"
MEDIA_STAGES = {"take", "cut", "episode", "full"}
STATES = ("进行中", "已完成", "已作废", "已收轮", "用户已确认出片")
LEGACY_WAIT = "待用户确认"                       # 旧单的收轮状态，migrate / status 改成「已收轮」
CLOSED = {"已收轮", LEGACY_WAIT, "用户已确认出片"}
SNAP = "materials/snapshot"
MARK = re.compile(r"(✓|✗|✔|✘|通过|不通过|不适用|N/?A)")
VERSION = 5
SLOTS = ("a", "b")
PY_FALLBACK = "C:/Users/light/AppData/Local/Programs/Python/Python311/python.exe"
LEVELS = ("critical", "major", "verify", "minor")
LEVEL_NAME = {"critical": "严重", "major": "主要", "verify": "待核实", "minor": "记录"}
SEV_LEVEL = {"重出": "critical", "可剪": "major", "存疑": "verify", "记录": "minor"}
FIX_STATUS = ("open", "planned", "implemented", "wontfix")
DEFAULT_SCORING = {
    "scale": {"0": "没查或查不了（必须说明原因）", "1": "有问题（问题表里要有对应条目）", "2": "基本没问题，有小瑕疵", "3": "没问题"},
    "evidence_rule": "打 2 或 3 分必须写证据：指到镜头、秒数、图上位置、文件行或计算数字；没有证据的高分按「没查」处理，打不了勾。",
    "disagreement": "两位审稿人同一维度分数相差 ≥2，或一人 ≤1、另一人 ≥2，就是分歧，交裁决人。",
    "audit": "两人都打 ≥2 的维度，裁决人每个审稿项随机抽 2 维复核证据，专抓两个模型共同的盲点。"}
DEFAULT_REVIEWERS = [{"slot": "a", "runner": "claude", "model": "claude-opus-5-5"}]   # Claude 单审（用户 2026-11-14，follow-up 065）


def now() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def rel(p: Path) -> str:
    try:
        return p.resolve().relative_to(REPO).as_posix()
    except ValueError:
        return p.as_posix()


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def roster() -> dict:
    return json.loads(ROSTER.read_text(encoding="utf-8"))


def resolve(p: str) -> Path:
    q = Path(p)
    return (q if q.is_absolute() else REPO / q).resolve()


# ---------------------------------------------------------------- 集的结构
def read_json(p: Path) -> dict:
    d = json.loads(p.read_text(encoding="utf-8"))
    return d.get("content", d) if isinstance(d, dict) else d


def latest(paths: list[Path]) -> Path | None:
    def ver(p: Path) -> int:
        m = re.search(r"_v(\d+)\.json$", p.name)
        return int(m.group(1)) if m else -1
    return max(paths, key=ver) if paths else None


def layout(ep: Path) -> dict:
    filming = read_json(ep / "filming.json")
    scenes = {s["id"]: s for s in filming.get("scenes", [])}
    order, versions = list(scenes), {}
    ep_cut = latest(list((ep / "edit/final").glob("cut_v*.json")))
    if ep_cut:
        d = json.loads(ep_cut.read_text(encoding="utf-8"))
        order = [s["scene"] for s in d.get("scenes", [])] or order
        versions = {s["scene"]: s.get("cut_version") for s in d.get("scenes", [])}
    order += [s for s in scenes if s not in order]
    for sid in order:
        if sid not in versions:
            c = latest(list((ep / f"scenes/{sid}/edit/final").glob("cut_v*.json")))
            if c:
                versions[sid] = int(re.search(r"_v(\d+)", c.name).group(1))
    return {"scenes": scenes, "order": order, "cuts": versions, "episode_cut": ep_cut}


def drama_dir(ep: Path) -> Path:
    return ep.parent.parent if ep.parent.name == "episodes" else ep.parent


def reviews_dir(ep: Path) -> Path:
    return drama_dir(ep) / "reviews"


def fingerprint_files(ep: Path, stage: str, lay: dict) -> list[Path]:
    d = drama_dir(ep)
    files = [ep / "filming.json", ep / "story.json", ep / "prompts.json", d / "bible.md"]
    files += sorted((d / "2_世界观人设/characters").glob("c*/c*.md"))
    if stage in {"pregen", "prompt", "full"}:
        files += sorted(ep.glob("scenes/*/shots/*/资料包/prompt.txt")) + sorted(ep.glob("scenes/*/groups/*/资料包/prompt.txt"))
    if stage in MEDIA_STAGES:
        files += [ep / f"scenes/{s}/edit/final/cut_v{v}.json" for s, v in lay["cuts"].items()]
        if lay["episode_cut"]:
            files.append(lay["episode_cut"])
    return [f for f in files if f.is_file()]


def fingerprint(ep: Path, stage: str, lay: dict, scenes: list[str] | None = None) -> dict[str, str]:
    """被审材料的指纹。给了 scenes（v2 审查单，follow-up 036）就只看这几场：filming.json / prompts.json 只取这几场的场对象，
    资料包只取这几场的，人物卡只取这几场出场的人；故事稿、bible 与剪辑仍整份。这样一场一场走循环时，改别的场不会作废这张单。"""
    if scenes is None:
        return {rel(f): sha(f) for f in fingerprint_files(ep, stage, lay)}
    out: dict[str, str] = {}
    cast = {c.split("-")[0] for s in scenes for shot in lay["scenes"].get(s, {}).get("shots", []) for c in shot.get("cast", [])}
    for f in fingerprint_files(ep, stage, lay):
        r = rel(f)
        if f.name in ("filming.json", "prompts.json") and f.parent == ep:
            doc = read_json(f)
            by_id = {s["id"]: s for s in doc.get("scenes", [])}
            extra = {k: v for k, v in doc.items() if k != "scenes"}
            for s in scenes:
                blob = json.dumps({"scene": by_id.get(s), **extra}, ensure_ascii=False, sort_keys=True)
                out[f"{r}#{s}"] = hashlib.sha256(blob.encode("utf-8")).hexdigest()
            continue
        if f.parent.parent.name == "characters" and f.parent.name.split("_")[0] not in cast:
            continue
        if "/scenes/" in r and not any(f"/scenes/{s}/" in r for s in scenes):
            continue
        out[r] = sha(f)
    return out


# ---------------------------------------------------------------- 材料
def ff(args: list[str]) -> None:
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


def sheet(video: Path, a: float, b: float, fps: int, out: Path, w: int = 320, cols: int = 6) -> None:
    n = max(1, math.ceil((b - a) * fps))
    vf = (f"trim=start={a}:end={b},fps={fps},scale={w}:-1,"
          f"drawtext={FONT}:text='%{{pts\\:hms}}':x=6:y=6:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6,"
          f"tile={cols}x{math.ceil(n / cols)}")
    ff(["-i", str(video), "-vf", vf, "-frames:v", "1", "-q:v", "3", str(out)])


def frame(video: Path, t: float, out: Path, w: int = 480) -> None:
    ff(["-ss", f"{max(t, 0):.3f}", "-i", str(video), "-frames:v", "1", "-vf", f"scale={w}:-1", str(out)])


def spec_lines(spec: dict) -> list[str]:
    return ["## 分镜规格", *([f"**看点**（这一镜要观众看懂或感到什么；只给审查用，不进 prompt）：{spec['point']}"] if spec.get("point") else []),
            f"**动作**：{spec.get('action')}", f"**走位**：{spec.get('blocking')}", f"**节拍**：{spec.get('beats')}",
            f"**镜头**：{spec.get('camera')}", f"**光线**：{spec.get('lighting')}", f"**台词**：{spec.get('dialogue') or '（无）'}"]


def lines_md(lay: dict, scenes: list[str], out: Path) -> None:
    """母语听感审稿人的唯一材料（follow-up 036）：全集台词按播放顺序，每镜附一句画面说明，不带分镜规格。"""
    out.mkdir(parents=True, exist_ok=True)
    rows = ["# 全集台词（按播放顺序）", "",
            "每镜：镜头 · 时长 · 画面上在发生什么（一句），然后是台词。人物设定见剧 README 与人物卡（盲审只用这里的一句画面说明）。", ""]
    for sid in scenes:
        sc = lay["scenes"][sid]
        rows += [f"## {sid} · {sc.get('location', '')} · {sc.get('time', '')}", ""]
        for spec in sc["shots"]:
            said = [ln.strip() for ln in str(spec.get("dialogue", "")).splitlines() if ln.strip()]
            if said:
                rows += [f"**{sid}_{spec['id']}**（{spec.get('duration')} 秒）— {str(spec.get('action', ''))}",
                         *[f"> {ln}" for ln in said], ""]
    (out / "lines.md").write_text("\n".join(rows), encoding="utf-8")


def junctions_md(lay: dict, scenes: list[str], out: Path) -> None:
    """镜间接点表（chuanyue_yiri follow-up 056）：相邻两镜的结尾 ↔ 开头并排，附 tools/shot_junctions.py 的机检疑点。
    原来连续性（K5）、人物（C7）都有「接得上」的检查项，但材料是一镜一份，没人逐个接点看，EP1 s1 st1→st2 就漏了。"""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from shot_junctions import table
    rows, _ = table([{"id": sid, **lay["scenes"][sid]} for sid in scenes])
    out.mkdir(parents=True, exist_ok=True)
    (out / "junctions.md").write_text(chr(10).join(rows), encoding="utf-8")


def prepare_text(ep: Path, lay: dict, scenes: list[str], out: Path) -> list[str]:
    """出片前材料：每镜的分镜规格与要送去的 prompt、俯视图、首帧图、镜组板路径。"""
    (out / "shots").mkdir(parents=True, exist_ok=True)
    index = []
    for sid in scenes:
        sc = lay["scenes"][sid]
        groups = {m: g["id"] for g in sc.get("groups", []) for m in g["shots"]}
        gl = []
        for g in sc.get("groups", []):
            gd = ep / "scenes" / sid / "groups" / g["id"]
            gl.append("%s＝%s（板：`%s`；prompt：`%s`）" % (g["id"], " → ".join(g["shots"]), gd / "board.png", gd / "资料包" / "prompt.txt"))
        index += [f"## {sid} · {sc.get('location', '')} · {sc.get('time', '')}", f"本场目的：{sc.get('purpose', '')}",
                  "镜组：" + ("；".join(gl) or "无"), ""]
        for k, spec in enumerate(sc["shots"]):
            st = spec["id"]; sd = ep / f"scenes/{sid}/shots/{st}"
            pics = sorted(p for p in (sd / "planning").glob("*.png")) if (sd / "planning").is_dir() else []
            d = out / "shots" / f"{sid}_{st}"; d.mkdir(exist_ok=True)
            (d / "spec.md").write_text("\n".join([
                f"# {sid} {st}（场内第 {k + 1} 个镜头）", "",
                f"- 设计时长：{spec.get('duration')} 秒；出场：{', '.join(spec.get('cast', []))}" + (f"；属镜组 {groups[st]}" if st in groups else "；单拍"),
                f"- 送给模型的 prompt：`{sd / '资料包/prompt.txt'}`；参考清单：`{sd / '资料包/manifest.json'}`",
                *[f"- 规划图：`{p}`" for p in pics], "", *spec_lines(spec)]), encoding="utf-8")
            index.append(f"- `{sid}_{st}` {spec.get('duration')}s{'（镜组 ' + groups[st] + '）' if st in groups else ''} {str(spec.get('action', ''))[:40]}…")
        index.append("")
    return index


def prepare_media(ep: Path, lay: dict, scenes: list[str], out: Path) -> list[str]:
    """出片后材料：成片实际用到的那段的 4 fps / 1 fps 拼图与 spec.md；每场镜头接口帧与整场 1 fps。"""
    (out / "shots").mkdir(parents=True, exist_ok=True); (out / "scenes").mkdir(exist_ok=True)
    index = []
    for sid in scenes:
        ver = lay["cuts"].get(sid)
        if not ver:
            raise SystemExit(f"{sid} 还没有最终场剪辑，出片类审查要先有 scenes/{sid}/edit/final/cut_vN.json")
        sc = lay["scenes"][sid]; shots = {x["id"]: x for x in sc["shots"]}
        groups = {g["id"]: g["shots"] for g in sc.get("groups", [])}
        cut = json.loads((ep / f"scenes/{sid}/edit/final/cut_v{ver}.json").read_text(encoding="utf-8"))
        index += [f"## {sid} · {sc.get('location', '')} · {sc.get('time', '')}", f"本场目的：{sc.get('purpose', '')}", ""]
        bounds, heard = [], []
        for k, e in enumerate(cut["events"]):
            st, g = e["shot"], e.get("group")
            td = ep / (f"scenes/{sid}/groups/{g}/renders/{e['take']}" if g else f"scenes/{sid}/shots/{st}/renders/{e['take']}")
            video = next(td.glob("*.mp4"))
            d = out / "shots" / f"{sid}_{st}"; d.mkdir(exist_ok=True)
            a, b = float(e["in"]), float(e["out"])
            sheet(video, a, b, 4, d / "sheet4.jpg")
            sheet(video, a, b, 1, d / "sheet1.jpg", w=480, cols=4)
            ann = json.loads((td / "annotation.json").read_text(encoding="utf-8")) if (td / "annotation.json").is_file() else {}
            words = [w for w in ann.get("words", []) if a - 0.05 <= w["s"] <= b]
            (d / "spec.md").write_text("\n".join([
                f"# {sid} {st}（场内第 {k + 1} 个镜头）", "",
                f"- 视频：`{video}`",
                f"- 成片用的区间：{a:.2f}–{b:.2f} 秒（共 {b - a:.2f} 秒）" + (f"；镜组 {g}（{' → '.join(groups.get(g, []))}），镜组条里的时间" if g else "；单镜条"),
                f"- 送给模型的 prompt：`{td / 'prompt.txt'}`",
                f"- 每秒 4 帧拼图：`{d / 'sheet4.jpg'}`（黄字＝原条时间）", f"- 每秒 1 帧拼图：`{d / 'sheet1.jpg'}`",
                f"- 设计时长：{shots[st].get('duration')} 秒；出场：{', '.join(shots[st].get('cast', []))}", "", *spec_lines(shots[st]), "",
                "## 语音识别（英文模型；外语会被识别成近音英文，秒＝原条时间）",
                " ".join(f"{w['w']}[{w['s']:.2f}-{w['e']:.2f}]" for w in words) or "（无）", "",
                f"## 剪辑理由\n{e.get('reason', '')}"]), encoding="utf-8")
            index.append(f"- `{sid}_{st}`：{a:.2f}–{b:.2f}s{'（镜组 ' + g + '）' if g else ''} {str(shots[st].get('action', ''))[:40]}…")
            bounds.append((st, video, a, b))
            heard.append((st, " ".join(w["w"] for w in words if w["s"] >= b - 4) or "（无）", " ".join(w["w"] for w in words if w["s"] <= a + 4) or "（无）"))
        pairs = []
        for i in range(len(bounds) - 1):
            p1, p2 = out / "scenes" / f"_{sid}_{i}_a.png", out / "scenes" / f"_{sid}_{i}_b.png"
            frame(bounds[i][1], bounds[i][3] - 0.06, p1); frame(bounds[i + 1][1], bounds[i + 1][2] + 0.02, p2)
            pairs.append((bounds[i][0], bounds[i + 1][0], p1, p2))
        if len(heard) > 1:   # 接点两侧听到的话（follow-up 056）：台词是不是同一个人接着说，靠接口帧看不出来
            jrows = [f"# {sid} 镜间接点：前一镜最后 4 秒 ↔ 后一镜最初 4 秒（语音识别）", "", f"接口帧见 `{sid}_bounds.jpg`。", ""]
            for x, y in zip(heard, heard[1:]):
                jrows += [f"## {x[0]} → {y[0]}", f"- 前一镜尾：{x[1]}", f"- 后一镜头：{y[2]}", ""]
            (out / "scenes" / f"{sid}_junctions.md").write_text("\n".join(jrows), encoding="utf-8")
        if pairs:
            ins, filt = [], []
            lab = "drawtext=" + FONT + ":text='{}':x=6:y=6:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.6"
            for j, (s1, s2, p1, p2) in enumerate(pairs):
                ins += ["-i", str(p1), "-i", str(p2)]
                filt.append(f"[{2*j}:v]{lab.format(s1 + ' 尾')}[a{j}];[{2*j+1}:v]{lab.format(s2 + ' 头')}[b{j}];[a{j}][b{j}]hstack[r{j}]")
            filt.append("".join(f"[r{j}]" for j in range(len(pairs))) + f"vstack=inputs={len(pairs)}[o]" if len(pairs) > 1 else "[r0]null[o]")
            ff([*ins, "-filter_complex", ";".join(filt), "-map", "[o]", "-q:v", "3", str(out / "scenes" / f"{sid}_bounds.jpg")])
            for _, _, p1, p2 in pairs:
                p1.unlink(missing_ok=True); p2.unlink(missing_ok=True)
        sv = ep / f"scenes/{sid}/edit/final/{sid}_final_v{ver}.mp4"
        if sv.is_file():
            dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(sv)],
                                       capture_output=True, text=True).stdout or 0)
            sheet(sv, 0, dur, 1, out / "scenes" / f"{sid}_scene1.jpg", w=400, cols=6)
        index += ["", f"场剪辑成片：`{sv}`；接口帧：`{out / 'scenes' / (sid + '_bounds.jpg')}`；整场每秒 1 帧：`{out / 'scenes' / (sid + '_scene1.jpg')}`", ""]
    return index


def snapshot(ep: Path, lay: dict, scenes: list[str], run: Path) -> dict[str, dict]:
    """修复页的「修复前」（用户 2026-11-08）：被审的每场分镜（filming_<场>.json）、每镜 / 镜组编译好的 prompt（prompts/<场>_<镜>.txt）、
    每镜首帧的路径与 sha256（first_frames.json）。只存文字与哈希，图本身留在各镜 planning/ 与其归档目录里。"""
    out = run / SNAP
    (out / "prompts").mkdir(parents=True, exist_ok=True)
    frames: dict[str, dict] = {}
    for sid in scenes:
        sc = lay["scenes"].get(sid)
        if not sc:
            continue
        (out / f"filming_{sid}.json").write_text(json.dumps(sc, ensure_ascii=False, indent=1), encoding="utf-8")
        for spec in sc.get("shots", []):
            st = spec["id"]; sd = ep / f"scenes/{sid}/shots/{st}"
            pr = sd / "资料包/prompt.txt"
            if pr.is_file():
                shutil.copyfile(pr, out / "prompts" / f"{sid}_{st}.txt")
            img = sd / "planning" / f"{st}_first_frame.png"
            if img.is_file():
                frames[f"{sid}_{st}"] = {"path": rel(img), "sha256": sha(img),
                                         "mtime": dt.datetime.fromtimestamp(img.stat().st_mtime).isoformat(timespec="seconds")}
        for g in sc.get("groups", []):
            pr = ep / f"scenes/{sid}/groups/{g['id']}/资料包/prompt.txt"
            if pr.is_file():
                shutil.copyfile(pr, out / "prompts" / f"{sid}_{g['id']}.txt")
    (out / "first_frames.json").write_text(json.dumps(frames, ensure_ascii=False, indent=1), encoding="utf-8")
    return frames


# ---------------------------------------------------------------- 生成审查单
def partition(kind: str, scenes: list[str]) -> list[list[str]]:
    if kind == "pairs" and len(scenes) > 2:
        return [scenes[i:i + 2] for i in range(0, len(scenes), 2)]
    if kind == "halves" and len(scenes) > 3:
        h = math.ceil(len(scenes) / 2)
        return [scenes[:h], scenes[h:]]
    return [scenes]


R_TEXT_V2 = "复核上一轮：previous.md 里本代号的重出 / 可剪 / 存疑问题，逐条写是否已改好"
R_TEXT_V5 = "复核上一轮：previous.md 里本类别的每个问题（I 编号），逐条写是否已改好；在「## 评分表」写一行 `- R <分> 证据：…`"


def rubric_of(spec: dict) -> list[dict]:
    """v5 评分维度；名册没写 rubric 的法则退回到 must（每条必查项当一维）。"""
    if spec.get("rubric"):
        return [{"id": r["id"], "name": r.get("name", r["id"]), "question": r.get("question", ""), "critical": bool(r.get("critical"))}
                for r in spec["rubric"]]
    return [{"id": m["id"], "name": m["text"].split("：")[0][:16], "question": m["text"], "critical": False} for m in spec.get("must", [])]


def cast_map(ep: Path, lay: dict, scenes: list[str]) -> list[tuple[str, str, list[str]]]:
    """角色立场审查（chuanyue_yiri follow-up 063）：每个出场的有卡人物 → (键, 名字, 出现的场)；有路人的镜头另成一组「路人」。"""
    chars = drama_dir(ep) / "2_世界观人设" / "characters"
    names = {d.name.split("_", 1)[0]: d.name.split("_", 1)[1] for d in chars.iterdir() if d.is_dir() and "_" in d.name} if chars.is_dir() else {}
    seen: dict[str, list[str]] = {}
    extras: list[str] = []
    for sid in scenes:
        for sh in lay["scenes"][sid]["shots"]:
            for c in sh.get("cast", []):
                base = c.split("-")[0]
                if sid not in seen.setdefault(base, []):
                    seen[base].append(sid)
            if sh.get("extras") and sid not in extras:
                extras.append(sid)
    out = [(k, names.get(k, k), v) for k, v in sorted(seen.items(), key=lambda kv: int(re.sub(r"\D", "", kv[0]) or 0))]
    return out + ([("extras", "路人与群众", extras)] if extras else [])


def role_history(ep: Path, key: str) -> list[str]:
    """前几集里这个人物出现的每一镜（台词与动作开头），给角色立场审稿人对照跨集一致（chuanyue_yiri follow-up 064）。"""
    rows: list[str] = []
    for prev in sorted(d for d in ep.parent.iterdir() if d.is_dir() and d.name < ep.name and (d / "filming.json").is_file()):
        try:
            scenes = json.loads((prev / "filming.json").read_text(encoding="utf-8"))["content"]["scenes"]
        except (OSError, ValueError, KeyError):
            continue
        hits = [(sc["id"], sh) for sc in scenes for sh in sc["shots"] if key in [c.split("-")[0] for c in sh.get("cast", [])]]
        if hits:
            rows += [f"## 前几集的你 · {prev.name}（{len(hits)} 镜，只列台词与动作开头）", ""]
            rows += [f"- {sid}_{sh['id']}：{str(sh.get('action', ''))[:160]}… ｜台词：{sh.get('dialogue') or '（无）'}" for sid, sh in hits]
            rows.append("")
    return rows


def roles_md(ep: Path, lay: dict, scenes: list[str], out: Path) -> None:
    """每个角色一份第一人称材料 materials/roles/<键>.md：他出现的每一镜，同框的人、全部台词、动作与节拍原文。"""
    (out / "roles").mkdir(parents=True, exist_ok=True)
    chars = drama_dir(ep) / "2_世界观人设" / "characters"
    for key, name, _ in cast_map(ep, lay, scenes):
        card = next((d / f"{d.name}.md" for d in chars.glob(f"{key}_*") if d.is_dir()), None) if key != "extras" else None
        ledger = card.parent / "behavior.md" if card else None
        rows = [f"# 你是 {name}" + (f"（{key}）" if key != "extras" else "（画面里所有路人）"), "",
                (f"人物卡：`{card}`" if card else "没有人物卡：按场景里的普通人代入（店主、路人、孩子……各按自己的身份）。"),
                (f"行为档案（前几集已经立住的说话方式、习惯、分寸，跨集要一致）：`{ledger}`" if ledger and ledger.is_file()
                 else "行为档案：还没有（第一次出场）。审完在报告末尾写「## 行为档案增补」，列出这一集立住的行为。" if card else ""), "",
                "下面按播放顺序列出你出现的每一镜。只用「你此刻知道的事」判断：剧情需要什么、作者写的心理说明，都不算你的理由。", ""]
        rows += role_history(ep, key) if key != "extras" else []
        for sid in scenes:
            sc = lay["scenes"][sid]
            for sh in sc["shots"]:
                cast = [c.split("-")[0] for c in sh.get("cast", [])]
                if (key == "extras" and not sh.get("extras")) or (key != "extras" and key not in cast):
                    continue
                rows += [f"## {sid}_{sh['id']} · {sc.get('location', '')} · {sc.get('time', '')}",
                         f"- 同框：{', '.join(cast) or '（无有卡人物）'}" + (f"；路人 {sh['extras']} 个" if sh.get("extras") else ""),
                         f"- 动作：{sh.get('action', '')}", f"- 节拍：{sh.get('beats', '')}", f"- 台词：{sh.get('dialogue') or '（无）'}", ""]
        (out / "roles" / f"{key}.md").write_text(chr(10).join(rows), encoding="utf-8")


ROLE_QUESTIONS = ("逐镜、逐拍用第一人称回答：我在哪、面对的是谁（他是什么人、懂不懂我的话）、我此刻知道什么、想要什么；"
                  "然后看分镜给我写的——①我说的话（措辞、长短、语种、音量）面对这个人合不合适、他能不能明白我要什么；"
                  "②我的手和身体（手势、姿态、距离）合不合我的身份、对方的身份和场合；③我的表情和强度合不合处境（不过演）；"
                  "④我看谁、什么时候看；⑤别人对我说话、做动作时，我会怎么回应、多快；⑥我做的每件事我自己知道为什么，不是为了剧情。"
                  "每一条不合适的都写出「此刻的我会怎么说 / 怎么做」。")


def build_items(stage: str, scenes: list[str], ros: dict, loop: int, version: int = VERSION,
                cast: list[tuple[str, str, list[str]]] | None = None) -> list[dict]:
    items = []
    for law in ros["stages"][stage]["laws"]:
        spec = ros["laws"][law]
        roles = cast if spec.get("partition") == "cast" else None
        parts = [r[2] for r in roles] if roles else partition(spec.get("partition", "whole"), scenes)
        if roles is not None and not roles:
            continue
        for i, part in enumerate(parts):
            iid = (f"{law}_{roles[i][0]}" if roles else law if len(parts) == 1 else f"{law}_{chr(65 + i)}")
            must = [dict(m) for m in spec.get("must", [])]
            if loop > 1:
                must.append({"id": "R", "text": R_TEXT_V5 if version >= 5 else R_TEXT_V2})
            it = {"id": iid, "law": law, "law_name": spec["name"], "color": spec.get("color", "#64748b"),
                  "scope": part, "checks": spec["checks"], "how": spec.get("how", ""), "blind": bool(spec.get("blind")),
                  **({"blind_note": spec["blind_note"]} if spec.get("blind_note") else {}),
                  **({"prefer_model": spec["prefer_model"]} if spec.get("prefer_model") else {}),
                  "must": must, "status": "pending", "report": f"reports/{iid}.md", "prompt": f"items/{iid}.md"}
            if roles:
                key, name = roles[i][0], roles[i][1]
                me = ("画面里所有路人与群众（每个按自己的身份代入）" if key == "extras" else f"「{name}」（{key}）")
                it["role"] = key
                it["checks"] = f"你就是{me}。{ROLE_QUESTIONS} 材料：`materials/roles/{key}.md`（你出现的每一镜）。 " + it["checks"]
                it["law_name"] = f"{spec['name']}·{name}"
            if version >= 5:
                reviewers = spec.get("reviewers") or DEFAULT_REVIEWERS
                it.update(what=(it["checks"] if roles else spec.get("what", "")), problem=spec.get("problem", ""), method=list(spec.get("method", [])),
                          model_why=spec.get("model_why", ""), rubric=rubric_of(spec), report=f"reconcile/{iid}.md",
                          ticked_by="", ticked_by_list=[], findings={s: 0 for s in SEVERITIES}, rows=0,
                          slots={r["slot"]: {"slot": r["slot"], "runner": r["runner"], "model": r["model"], "status": "pending",
                                             "report": f"reports/{iid}__{r['slot']}.md", "prompt": f"items/{iid}__{r['slot']}.md",
                                             "agents": []} for r in reviewers})
            items.append(it)
    return items


def scoring_lines(scoring: dict) -> list[str]:
    sc = scoring or DEFAULT_SCORING
    return ["评分（0–3 分）：", *[f"- **{k}**：{v}" for k, v in sorted((sc.get("scale") or DEFAULT_SCORING["scale"]).items())],
            f"- 证据规则：{sc.get('evidence_rule', DEFAULT_SCORING['evidence_rule'])}（证据至少 8 个字）",
            f"- 分歧：{sc.get('disagreement', DEFAULT_SCORING['disagreement'])}",
            f"- 抽查：{sc.get('audit', DEFAULT_SCORING['audit'])}"]


def brief_text(ep: Path, stage_name: str, run: Path, media: bool, known: str, loop: int, max_loops: int,
               version: int = 2, scoring: dict | None = None) -> str:
    text = brief_text_v2(ep, stage_name, run, media, known, loop, max_loops)
    if version < 5:
        return text
    head, _, _ = text.partition("## 报告格式（缺一不能打勾）")
    return head + "\n".join([
        "## 双审与评分（v5）",
        "- 每个审稿项由两位审稿人**各自独立**审：a 位是 Claude 模型、b 位是 Codex 模型（名册 `reviewers`，按这一类最合适的模型选）。"
        "不要读另一位的报告；两人都说没问题不等于没问题——工具会对比两份评分，分歧和抽查交裁决人。", *scoring_lines(scoring or {}), "",
        "## 报告格式（缺一不能打勾）",
        "1. `## 评分表`：任务书里每个评分维度一行：`- <维度编号> <0–3> 证据：<镜头·秒数·图上位置·文件行·计算数字>`，"
        "例如 `- P1 1 证据：s3_st2 自拍却双手掰面包（见问题表）`、`- P4 3 证据：s1_st1–st5 首帧放大，手里都有支撑`。"
        "可写「3分」、全角冒号；打 0 分写 `原因：…`。第 2、3 轮另写一行 `- R <分> 证据：…`（复核上一轮）。",
        "2. 问题表，每个问题一行，按严重度排序（打 1 分的维度在这里必须有对应条目，「法则·子类」写维度编号）：", "",
        "| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |", "|---|---|---|---|---|---|---|", "",
        "   严重度：重出 / 可剪 / 记录 / 存疑。本该哪关：① 故事 / ② 分镜文字 / ③ prompt 或首帧 / ④ 模型随机 / 规则源。",
        "   建议改动要标「便宜」（改文字、出图、改工具即可）或「要积分」（必须重出视频）。",
        "   全部没问题时不写空表，写一行「结论：无问题」。",
        "3. 「整体观察」（≤10 行）。",
        "4. **最后一步打勾**：Claude 审稿位自己运行任务书里的 `tick` 命令（带 `--slot`），看到「已打勾」才算完成；被拒就按提示改报告再打。"
        "Codex 审稿位（沙箱里没有 python）不运行 tick，最后打印一行 `REPORT WRITTEN: <报告路径>`，由调用方凭 codex exec 运行日志 `tick … --attest-log <日志>` 代为登记。",
        "5. 给调用你的人回 300 字以内摘要：最低分的维度、最严重的 5 条、报告路径、打勾结果。"])


def brief_text_v2(ep: Path, stage_name: str, run: Path, media: bool, known: str, loop: int, max_loops: int) -> str:
    d = drama_dir(ep)
    head = (d / "README.md").read_text(encoding="utf-8").splitlines()[0].lstrip("# ") if (d / "README.md").is_file() else d.name
    mat = (["- 每镜 `materials/shots/<场>_<镜>/`：`spec.md`（分镜规格、视频路径、成片用的区间、语音识别、剪辑理由）、`sheet4.jpg`（每秒 4 帧）、`sheet1.jpg`（每秒 1 帧）。",
            "- 每场 `materials/scenes/<场>_bounds.jpg`（镜头接口）、`<场>_junctions.md`（接点两侧各 4 秒听到的话）与 `<场>_scene1.jpg`（整场每秒 1 帧）。",
            "- 镜间接点表 `materials/junctions.md`：分镜里每个接点上一镜结尾 ↔ 下一镜开头，带机检疑点（⚠ 重新开场类、ℹ 视角来源切换）。"]
           if media else ["- 每镜 `materials/shots/<场>_<镜>/spec.md`：分镜规格、送给模型的 prompt 与参考清单路径、俯视图 / 首帧图路径；镜组板与镜组 prompt 路径在索引里。",
                          "- 镜间接点表 `materials/junctions.md`：每个接点上一镜结尾 ↔ 下一镜开头，带机检疑点（⚠ 重新开场类、ℹ 视角来源切换）。",
                          "- 出片前审查看的是**文字与参考图**：做不到、会出错、前后矛盾的写法都要报，因为它们一定会变成画面错误。"])
    again = ([f"- 这是第 {loop} 轮（最多 {max_loops} 轮）。上一轮的问题在 `previous.md`，这轮改了什么在 `changes.md`；必查项 R 要逐条复核。"] if loop > 1 else [])
    return "\n".join([
        f"# 审稿说明（{head} · {ep.name} · {stage_name} · 第 {loop} 轮）", "",
        "所有审稿人共用，先读完。审查单目录：`" + str(run) + "`（下文相对路径都相对它）。", "",
        "## 材料", "- 总索引：`materials/index.md`。", *mat, *again,
        f"- 集目录：`{ep}`；系列规则：`{d / 'bible.md'}`；故事稿：`{ep / 'story.md'}`（结构化版 `story.json`）；人物卡：`{d / '2_世界观人设/characters'}`；场景卡：`{d / '2_世界观人设/background'}`。",
        "- 需要时可用 ffmpeg 另抽帧或放大裁切，**只写到你自己的目录** `work/<你的代号>/`。", "",
        "## 已知、不用报告", known or "（无）", "",
        "## 规则",
        "- **只读**：不改仓库里任何文件（本审查单目录下你自己的报告与 work 目录除外），不调用任何收费服务，不提交生成。",
        "- **只管你自己那条法则**；顺手看到别的问题列在最后「其他」里，一句话。",
        "- 拿不准写「存疑」并说明怎么核实；证据必须指到镜头、秒数、拼图第几格或文件行。",
        "- 既报产物的错，也报「分镜 / prompt / 规则源本身的问题」。", "",
        "## 报告格式（缺一不能打勾）",
        "1. `## 必查项`：任务书里每个必查项编号一行，写 ✓（查过、没问题）或 ✗（有问题，见表）加一句说明，例如 `- P1 ✗ s3_st2 自拍却双手掰面包`。",
        "2. 问题表，每个问题一行，按严重度排序：", "",
        "| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |", "|---|---|---|---|---|---|---|", "",
        "   严重度：重出 / 可剪 / 记录 / 存疑。本该哪关：① 故事 / ② 分镜文字 / ③ prompt 或首帧 / ④ 模型随机 / 规则源。",
        "   建议改动要标「便宜」（改文字、出图、改工具即可）或「要积分」（必须重出视频）。",
        "   全部没问题时不写空表，写一行「结论：无问题」。",
        "3. 「整体观察」（≤10 行）。",
        "4. **最后一步自己打勾**：运行任务书里的 `tick` 命令，看到「已打勾」才算完成；被拒就按提示改报告再打。",
        "5. 给调用你的人回 300 字以内摘要：最严重的 5 条、报告路径、打勾结果。"])


def item_prompt(it: dict, run: Path, stage_name: str) -> str:
    scope = "、".join(it["scope"]) if it["scope"] else "全部"
    blind = ("\n" + it.get("blind_note", "**你是观众视角：不要读任何 spec.md、story、index 或分镜规格**，只看成片画面、听台词。")
             if it["blind"] else "")
    prefer = ([f"建议换一个模型来审（{it['prefer_model']}，和作者不是同一个模型）：调用你的人可以用 "
               f"`{it['prefer_model']} exec` 跑这份任务书；打勾时 `--by` 写实际模型名。", ""] if it.get("prefer_model") else [])
    return "\n".join([
        f"你是独立审稿人，代号 **{it['id']}**，只管「{it['law_name']}」法则。阶段：{stage_name}。",
        f"先完整读审稿说明：`{run / 'BRIEF.md'}`，严格按它的规则和报告格式做。{blind}", "",
        f"你的范围：{scope}。", "", *prefer, f"要查什么：{it['checks']}", "", f"怎么查：{it['how']}", "",
        "## 必查项（报告「## 必查项」里每条都要写 ✓ 或 ✗）", *[f"- **{m['id']}** {m['text']}" for m in it["must"]], "",
        f"报告写到：`{run / it['report']}`", "",
        "审完最后一步自己打勾（必须是你自己，不是调用你的人）：",
        f"`python tools/review_run.py tick \"{run}\" {it['id']} --report \"{run / it['report']}\" --by \"<你的模型名>/{it['id']}\"`",
        "（在仓库根目录 C:\\workspace\\micro-drama-platform 运行。）"])


def rubric_lines(it: dict, loop: int) -> list[str]:
    out = [f"- **{r['id']}** {r['name']}：{r['question']}" + ("（**关键维度**：≤1 分即严重问题）" if r.get("critical") else "")
           for r in it["rubric"]]
    if loop > 1:
        out.append(f"- **R** 复核上一轮：{R_TEXT_V5.split('：', 1)[1]}")
    return out


def tick_cmd(run: Path, it: dict, slot: str) -> str:
    s = it["slots"][slot]
    return (f"python tools/review_run.py tick \"{run}\" {it['id']} --slot {slot} --report \"{run / s['report']}\" "
            f"--by \"{s['model']}/{it['id']}__{slot}\"")


def slot_prompt(it: dict, slot: str, run: Path, stage_name: str, scoring: dict, loop: int) -> str:
    """v5 一位审稿人（a=Claude / b=Codex）的任务书：是什么、rubric＋评分规则、审法、范围、材料、本位的打勾命令。"""
    s = it["slots"][slot]
    scope = "、".join(it["scope"]) if it["scope"] else "全部"
    other = next((x for x in SLOTS if x != slot), "")
    blind = ("\n" + it.get("blind_note", "**你是观众视角：不要读任何 spec.md、story、index 或分镜规格**，只看成片画面、听台词。")
             if it["blind"] else "")
    mats = (["- 只读 `materials/lines.md`（盲审，别的材料都不读）。"] if it["law"] == "native_ear" else
            ["- 只用给观众的成片材料（拼图、成片），不读规格。"] if it["blind"] else
            ["- 总索引 `materials/index.md`；每镜 `materials/shots/<场>_<镜>/spec.md`（及拼图）；全集台词 `materials/lines.md`。",
             "- 集目录、bible、故事稿、人物卡、场景卡路径见 BRIEF.md「材料」。"])
    if loop > 1:
        mats.append("- 上一轮问题清单 `previous.md`、这轮改动 `changes.md`：评分表里 R 一行逐条复核。")
    codex = s["runner"] == "codex"
    if codex:
        finish = ["## 最后一步（Codex 审稿位）",
                  "Codex 沙箱只能看到工作区，python 不在里面，**你不用、也不要运行 tick**。只要：",
                  f"1. 把报告写到 `{run / s['report']}`；",
                  f"2. 在你最后的输出里单独打印一行：`REPORT WRITTEN: {run / s['report']}`。",
                  "调用你的人会凭 `codex exec` 的运行日志代为登记（日志里必须有这一行，且晚于派单时间），不会替你写或改报告。",
                  f"（只有在沙箱外、能直接运行 python 时才可以自己打勾：`{tick_cmd(run, it, slot)}`；找不到 `python` 用 `{PY_FALLBACK}`。）"]
    else:
        finish = ["审完最后一步自己打勾（必须是你自己，不是调用你的人）：", f"`{tick_cmd(run, it, slot)}`",
                  "（在仓库根目录 C:\\workspace\\micro-drama-platform 运行；`--by` 的模型名写你实际的模型。）"]
    prefer = ([f"- 本类建议由 {it['prefer_model']} 审：{'你就是这一位' if s['runner'] == it['prefer_model'] else '另一位（' + other + ' 位）是'}。", ""]
              if it.get("prefer_model") else [])
    return "\n".join([
        f"你是独立审稿人 **{it['id']}__{slot}**（{slot} 位 · {s['runner']} · {s['model']}），只管「{it['law_name']}」这一类。阶段：{stage_name}。",
        f"先完整读审稿说明：`{run / 'BRIEF.md'}`，严格按它的规则和报告格式做。{blind}",
        *([f"同一项还有另一位审稿人（{other} 位，另一个模型）独立审；**不要读它的报告**，也不要读 reconcile/ 下的文件。", ""]
          if len(it["slots"]) > 1 else ["这一项只有你一位审稿人（Claude 单审），没有第二位、也没有裁决人复核：拿不准的写「存疑」并说明怎么核实。", ""]),
        "## 这一类是什么", it.get("what") or it["checks"], *([f"\n想解决的问题：{it['problem']}"] if it.get("problem") else []),
        *([f"\n为什么由这类模型审：{it['model_why']}"] if it.get("model_why") else []), "",
        f"## 范围\n{scope}", "", "## 材料", *mats, "", *prefer,
        f"## 要查什么\n{it['checks']}", "", f"## 怎么查\n{it['how']}", "",
        "## 审法（按步骤做）", *[f"{k}. {m}" for k, m in enumerate(it.get("method") or [], 1)], "",
        "## 评分维度（报告「## 评分表」里每维一行：`- <编号> <0–3> 证据：…`）", *rubric_lines(it, loop), "",
        *scoring_lines(scoring), "- 打 1 分：问题表里必须有对应条目；打 0 分：写 `原因：` 说明为什么查不了。", "",
        f"报告写到：`{run / s['report']}`", "", *finish,
        *([f"- 你在 Codex 里跑（`codex exec` 跑这份任务书）。"] if codex else [])])


def overview_prompt(it: dict, run: Path, stage_name: str, loop: int) -> str:
    """v5 审稿项总览（管理站「审稿人任务书」链接）：两位审稿人各自的任务书与打勾命令。"""
    lines = [f"# 审稿项 {it['id']}（{it['law_name']} · {stage_name}）", "",
             f"范围：{'、'.join(it['scope']) or '全部'}。双审：每位拿自己的任务书、全新上下文、互不看报告；两人都打勾后工具自动对比，分歧与抽查交裁决人。", ""]
    for slot, s in it["slots"].items():
        lines += [f"## {slot} 位 · {s['runner']} · {s['model']}", f"- 任务书：`{run / s['prompt']}`", f"- 报告：`{run / s['report']}`",
                  f"- 打勾：`{tick_cmd(run, it, slot)}`" + (" `--attest-log <codex exec 运行日志>`（Codex 沙箱跑不了 python，由调用方凭日志代登记）" if s["runner"] == "codex" else ""), ""]
    lines += ["## 评分维度", *rubric_lines(it, loop)]
    return "\n".join(lines)


def judge_prompt(it: dict, run: Path, data: dict) -> str:
    j = it["judge"]
    rows = []
    for d in j["dims"]:
        sc = it["scores"][d]
        rows.append(f"- **{d}**（{sc['verdict']}）{sc['name']}：a {sc['a']} 分（{sc['a_ev'] or '—'}）；b {sc['b']} 分（{sc['b_ev'] or '—'}）")
    return "\n".join([
        f"你是裁决人 **{it['id']}__judge**（{j['runner']} · {j['model']}），裁「{it['law_name']}」审稿项 {it['id']} 的分歧并抽查两位都判通过的维度。",
        f"审稿说明：`{run / 'BRIEF.md'}`；对比表：`{run / it['report']}`。", "",
        "## 两份报告", *[f"- {k} 位（{s['by']}）：`{run / s['report']}`" for k, s in it["slots"].items()], "",
        "## 要裁的维度", *rows, "",
        "## 全部评分维度", *rubric_lines(it, 1), "", *scoring_lines(data.get("scoring") or {}), "",
        "## 规则",
        "- 分歧维度：回到材料本身核两人的证据，谁的证据站得住；抽查维度：专门找两个模型可能**共同**漏掉的问题，不因两人都给高分就放过。",
        "- 每个要裁的维度在报告「## 裁决」写一行：`- <编号> <最终分 0–3> 理由：<引用证据：镜头·秒数·图上位置·文件行>`（理由至少 8 个字）。",
        "- 发现两人都漏的问题，可以加问题表（同审稿报告的表头，含「严重度」列）。只读，不改被审材料。", "",
        f"报告写到：`{run / j['report']}`", "",
        "最后一步自己登记裁决：",
        f"`python tools/review_run.py adjudicate \"{run}\" {it['id']} --report \"{run / j['report']}\" --by \"<你的模型名>/{it['id']}__judge\"`",
        "（在仓库根目录 C:\\workspace\\micro-drama-platform 运行。）"])


def previous_md(prev_run: Path, prev: dict) -> str:
    out = [f"# 上一轮（第 {prev.get('loop', 1)} 轮）的问题", "", f"审查单：`{prev_run}`", ""]
    for it in prev["items"]:
        rp = prev_run / it["report"]
        if not rp.is_file():
            continue
        rows = [ln for ln in rp.read_text(encoding="utf-8").splitlines()
                if ln.startswith("|") and any(s in ln for s in ("重出", "可剪", "存疑")) and "严重度" not in ln]
        if rows:
            out += [f"## {it['id']}（{it['law_name']}）", "", "| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |", "|---|---|---|---|---|---|---|", *rows, ""]
    return "\n".join(out)


CN_NUM = "零一二三四五六七八九十"


def scope_label(scenes: list[str], order: list[str]) -> str:
    """审查范围的人话写法（用户 2026-11-08：看不出哪张是最新的）：全集 / 场一 / 场二到场八 / 场一、场三。"""
    nums = sorted(int(re.sub(r"\D", "", s) or 0) for s in scenes)
    cn = lambda n: "场" + (CN_NUM[n] if 0 <= n <= 10 else str(n))
    if not scenes or sorted(scenes) == sorted(order):
        return "全集"
    if len(nums) > 2 and nums == list(range(nums[0], nums[0] + len(nums))):
        return f"{cn(nums[0])}到{cn(nums[-1])}"
    return "、".join(cn(n) for n in nums)


def run_title(ep: str, scenes: list[str], order: list[str], stage_name: str, loop: int, ts: str, attempt: int = 1) -> str:
    """名字里带范围、第几次审查（同一范围开过几条审查链）、轮次和开单时间：ep01 · 场一 · 出片前（第 2 次）第 1 轮 · 11-08 15:32。"""
    when = f"{ts[4:6]}-{ts[6:8]} {ts[9:11]}:{ts[11:13]}" if len(ts) >= 13 else ts
    stage = stage_name.split("（")[0] + (f"（第 {attempt} 次）" if attempt > 1 else "")
    return f"{ep} · {scope_label(scenes, order)} · {stage} 第 {loop} 轮 · {when}"


def chain_attempt(reviews: Path, episode: str, stage: str, scenes: list[str], chain: str) -> int:
    """同一集、同一阶段、同一范围的第几条审查链（按链的开单时间排）。"""
    starts = {}
    for f in reviews.glob("*/checklist.json"):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if d.get("episode") == episode and d.get("stage") == stage and sorted(d.get("scenes", [])) == sorted(scenes):
            c = d.get("chain") or d.get("id")
            starts[c] = min(starts.get(c, d.get("created_at", "")), d.get("created_at", ""))
    starts.setdefault(chain, "9999")
    return sorted(starts, key=lambda c: starts[c]).index(chain) + 1


def cmd_new(a: argparse.Namespace) -> int:
    ep = resolve(a.target)
    ros = roster(); max_loops = int(ros.get("max_loops", 3))
    prev, prev_run, loop, chain, prev_issues = None, None, 1, None, None
    if a.after:
        prev_run = resolve(a.after); prev = load(prev_run)
        if prev.get("state") not in {"已完成", "已收轮", LEGACY_WAIT}:
            raise SystemExit(f"上一轮还没审完（{prev.get('state')}）：先让所有审稿人打勾，再开下一轮。")
        loop, chain = int(prev.get("loop", 1)) + 1, prev.get("chain", prev["id"])
        if loop > max_loops:
            raise SystemExit(f"已经审了 {max_loops} 轮，不再循环：对最后一轮运行 conclude 记下结论（出片时再由用户在对话里确认）。")
        if int(prev.get("version", 2)) >= 5 or (prev_run / ISSUES_JSON).is_file():
            prev_issues = write_issues(prev_run, prev)
            blocking = [i for i in prev_issues if i["level"] in ("critical", "major") and not resolved(i)]
            if blocking:
                raise SystemExit(f"上一轮还有 {len(blocking)} 个严重 / 主要问题没处理完（要 implemented，或 wontfix 并写理由），不能开下一轮：\n  " +
                                 "\n  ".join(f"{i['id']} [{i['level']}·{i['status']}] {i['category']} {i['dimension']} {'、'.join(i['shots'])}：{i['problem'][:50]}"
                                             for i in blocking[:12]) +
                                 f"\n  先 `python tools/review_run.py fix {rel(prev_run)} <I编号> --solution \"…\" --status implemented` 记下方案并实施。")
        if not a.changes and not any(i.get("solution") for i in prev_issues or []):
            raise SystemExit("开下一轮必须用 --changes 写明这轮之后改了什么（文件路径或一段文字），或先用 fix 给问题清单记下方案。")
        a.stage = a.stage or prev["stage"]
        a.scenes = a.scenes or ",".join(prev["scenes"])
        a.known = a.known or prev.get("known", "")
        ep = REPO / prev["target"]
    if not a.stage:
        raise SystemExit("要给 --stage（或用 --after 接上一轮）")
    if a.stage not in ros["stages"]:
        raise SystemExit(f"不认识的阶段 {a.stage}；可选：{'、'.join(ros['stages'])}")
    lay = layout(ep)
    scenes = [s for s in lay["order"] if not a.scenes or s in a.scenes.split(",")]
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    rid = f"{ep.name}_{ts}_{a.stage}_r{loop}"
    run = reviews_dir(ep) / rid
    (run / "reports").mkdir(parents=True); (run / "items").mkdir(); (run / "work").mkdir()
    (run / ".gitignore").write_text("work/\nmaterials/**/*.jpg\nmaterials/**/*.png\n", encoding="utf-8")
    media = a.stage in MEDIA_STAGES
    stage_name = ros["stages"][a.stage]["name"]
    if not a.no_materials:
        index = prepare_media(ep, lay, scenes, run / "materials") if media else prepare_text(ep, lay, scenes, run / "materials")
        lines_md(lay, scenes, run / "materials")
        junctions_md(lay, scenes, run / "materials")
        roles_md(ep, lay, scenes, run / "materials")
        index = ["全集台词按播放顺序：`materials/lines.md`（母语听感审稿人只读这一份）",
                 "镜间接点表：`materials/junctions.md`（上一镜结尾 ↔ 下一镜开头，带机检疑点；连续性、人物、台词审稿人逐个接点判）", "", *index]
        (run / "materials/index.md").write_text("\n".join([f"# {ep.name} 审查材料索引", "", "场顺序：" + " → ".join(scenes), "", *index]), encoding="utf-8")
    snapshot(ep, lay, scenes, run)
    changes = ""
    if prev is not None:
        user = ""
        if a.changes:
            cp = Path(a.changes)
            user = cp.read_text(encoding="utf-8") if cp.is_file() else a.changes
        changes = changes_from_issues(prev_issues, user) if prev_issues is not None else user
        (run / "changes.md").write_text(f"# 第 {loop - 1} 轮之后改了什么\n\n{changes}\n", encoding="utf-8")
        (run / "previous.md").write_text(previous_from_issues(prev_run, prev, prev_issues) if prev_issues is not None
                                         else previous_md(prev_run, prev), encoding="utf-8")
    items = build_items(a.stage, scenes, ros, loop, cast=cast_map(ep, lay, scenes))
    scoring = ros.get("scoring") or DEFAULT_SCORING
    (run / "BRIEF.md").write_text(brief_text(ep, stage_name, run, media, a.known or "", loop, max_loops, VERSION, scoring), encoding="utf-8")
    for it in items:
        if "slots" in it:
            (run / it["prompt"]).write_text(overview_prompt(it, run, stage_name, loop), encoding="utf-8")
            for slot in it["slots"]:
                (run / it["slots"][slot]["prompt"]).write_text(slot_prompt(it, slot, run, stage_name, scoring, loop), encoding="utf-8")
        else:
            (run / it["prompt"]).write_text(item_prompt(it, run, stage_name), encoding="utf-8")
    data = {"version": VERSION, "scoring": scoring, "adjudicator": ros.get("adjudicator") or {"runner": "claude", "model": "claude-opus-5-5"},
            "id": rid, "chain": chain or rid, "loop": loop, "max_loops": max_loops, "parent": rel(prev_run) if prev_run else "",
            "title": a.title or run_title(ep.name, scenes, lay["order"], stage_name, loop, ts,
                                           chain_attempt(reviews_dir(ep), ep.name, a.stage, scenes, chain or rid)), "target": rel(ep), "episode": ep.name,
            "stage": a.stage, "stage_name": stage_name, "gate_stage": bool(ros["stages"][a.stage].get("gate")),
            "scenes": scenes, "created_at": now(), "author": a.author, "known": a.known or "", "changes": changes,
            "roster_sha": sha(ROSTER), "materials": fingerprint(ep, a.stage, lay, scenes), "fp_scope": "scenes", "items": items, "state": "进行中", "log": []}
    save(run, data)
    if prev is not None:
        prev["child"] = rel(run); save(prev_run, prev)
    print(f"审查单已生成：{rel(run)}（第 {loop}/{max_loops} 轮，{len(items)} 位审稿人）")
    for it in items:
        print(f"  [ ] {it['id']:<14} {it['law_name']}  范围：{'、'.join(it['scope'])}  评分 {len(it.get('rubric') or it['must'])} 维  任务书：{rel(run / it['prompt'])}")
        for slot, s in (it.get("slots") or {}).items():
            print(f"        {slot} 位 {s['runner']:<6} {s['model']:<18} {rel(run / s['prompt'])}")
    return 0


# ---------------------------------------------------------------- 打勾、状态、收轮、确认
def load(run: Path) -> dict:
    p = run / CHECKLIST
    if not p.is_file():
        raise SystemExit(f"{run} 不是审查单目录（没有 {CHECKLIST}）")
    return json.loads(p.read_text(encoding="utf-8"))


def save(run: Path, data: dict) -> None:
    """原子写：先写临时文件再替换（follow-up 036：几十个审稿人同时打勾时，直接覆盖写把 checklist.json 写坏过）。"""
    import os
    tmp = run / (CHECKLIST + f".{os.getpid()}.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    for _ in range(50):
        try:
            os.replace(tmp, run / CHECKLIST); return
        except PermissionError:          # Windows：别的进程正在读，稍等再换
            import time; time.sleep(0.1)
    os.replace(tmp, run / CHECKLIST)


class RunLock:
    """同一张审查单的命令串行执行：读 → 改 → 写之间不让别的进程插进来（follow-up 036）。"""
    def __init__(self, run: Path, timeout: float = 300.0):
        self.path, self.timeout, self.fd = run / ".lock", timeout, None

    def __enter__(self):
        import os, time
        start = time.time()
        while True:
            try:
                self.fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY); os.write(self.fd, str(os.getpid()).encode()); return self
            except FileExistsError:
                try:
                    if time.time() - self.path.stat().st_mtime > 600:   # 死锁兜底：持锁进程早已不在
                        self.path.unlink(missing_ok=True); continue
                except FileNotFoundError:
                    continue
                if time.time() - start > self.timeout:
                    raise SystemExit(f"审查单正被别的命令占用（{self.path}），等了 {int(self.timeout)} 秒仍没释放")
                time.sleep(0.2)

    def __exit__(self, *exc):
        import os
        if self.fd is not None:
            os.close(self.fd)
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass


def stale_files(data: dict) -> list[str]:
    ep = REPO / data["target"]
    cur = fingerprint(ep, data["stage"], layout(ep), data["scenes"] if data.get("fp_scope") == "scenes" else None)
    old = data.get("materials", {})
    return sorted(k for k in set(old) | set(cur) if old.get(k) != cur.get(k))


def parse_report(text: str) -> tuple[dict[str, int], int, bool]:
    counts = {s: 0 for s in SEVERITIES}
    rows, header = 0, None
    prev_table = False
    for line in text.splitlines():
        if not line.startswith("|"):
            prev_table = False
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if "严重度" in cells:
            header = cells.index("严重度"); prev_table = True; continue
        if not prev_table:          # 新的一张表（没有「严重度」列，如道具状态表）：不算问题行（follow-up 036）
            header = None
        prev_table = True
        if header is None or set(line.replace("|", "").strip()) <= set("-: "):
            continue
        if len(cells) > header:
            rows += 1
            for s in SEVERITIES:
                if s in cells[header]:
                    counts[s] += 1; break
    clean = bool(re.search(r"^\s*结论[:：]\s*无问题", text, re.M))
    return counts, rows, clean


ROW_KEYS = (("shot", "镜头"), ("sec", "秒"), ("sub", "法则"), ("sev", "严重度"), ("gate", "哪关"), ("evidence", "证据"), ("fix", "建议"))


def parse_rows(text: str) -> list[dict]:
    """含「严重度」列的问题表里的每一行（与 parse_report 计数同一套规则），按表头取镜头、子类、严重度、证据、建议改动。"""
    out, header, cols, prev_table = [], None, [], False
    for line in text.splitlines():
        if not line.startswith("|"):
            prev_table = False
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if "严重度" in cells:
            header, cols, prev_table = cells.index("严重度"), cells, True; continue
        if not prev_table:
            header = None
        prev_table = True
        if header is None or set(line.replace("|", "").strip()) <= set("-: ") or len(cells) <= header:
            continue
        row = {"raw": "| " + " | ".join(cells) + " |", "cells": cells}
        for key, word in ROW_KEYS:
            k = next((i for i, c in enumerate(cols) if word in c), None)
            row[key] = cells[k] if k is not None and k < len(cells) else ""
        row["sev"] = next((s for s in SEVERITIES if s in row["sev"]), row["sev"])
        out.append(row)
    return out


def section(text: str, title: str) -> str:
    m = re.search(rf"^#+\s*{title}\s*$(.*?)(?=^#+\s|\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def parse_scores(body: str, ids: list[str]) -> tuple[dict[str, dict], list[str]]:
    """评分表 / 裁决行：`- P1 3 证据：…`、`- P1：2分 证据: …`、`- P4 0 原因：…`。返回（{编号: {score, evidence}}, 缺的编号）。"""
    got, missing = {}, []
    lines = body.splitlines()
    for d in ids:
        pat = re.compile(rf"^\s*(?:[-*+]|\d+\.)?\s*[*_`]*{re.escape(d)}(?![A-Za-z0-9])[*_`]*\s*[:：]?\s*[*_`]*(\d+)\s*分?[*_`]*(.*)$")
        m = next((pat.match(ln) for ln in lines if pat.match(ln)), None)
        if not m:
            missing.append(d); continue
        rest = m.group(2)
        ev = re.search(r"(?:证据|原因|理由|说明)\s*[:：]\s*(.*)$", rest)
        got[d] = {"score": int(m.group(1)), "evidence": (ev.group(1) if ev else rest).strip(" \t-—:：|*")}
    return got, missing


def parse_must(text: str, must: list[dict]) -> tuple[dict[str, str], list[str]]:
    """「## 必查项」一节里每个编号的 ✓/✗；返回（结果, 缺的编号）。"""
    m = re.search(r"^#+\s*必查项\s*$(.*?)(?=^#+\s|\Z)", text, re.M | re.S)
    body = m.group(1) if m else ""
    got, missing = {}, []
    for it in must:
        key = re.escape(it["id"])
        lines = body.splitlines()   # 先找以编号开头的行（「- R ✓」），再退回到行内任意位置的整词编号；「R」不能配到「Riley」（follow-up 036）
        line = next((ln for ln in lines if re.match(rf"^\s*(?:[-*+]|\d+\.)?\s*[*_`]*{key}(?![A-Za-z0-9])", ln)), None)             or next((ln for ln in lines if re.search(rf"(?<![A-Za-z0-9]){key}(?![A-Za-z0-9])", ln)), None)
        mark = MARK.search(line or "")
        if not mark:
            missing.append(it["id"]); continue
        got[it["id"]] = "✓" if mark.group(1) in {"✓", "✔", "通过"} else "—" if mark.group(1) in {"不适用", "N/A", "NA"} else "✗"
    return got, missing


def cmd_tick(a: argparse.Namespace) -> int:
    run = resolve(a.run); data = load(run)
    it = next((x for x in data["items"] if x["id"] == a.item), None)
    if not it:
        raise SystemExit(f"审查单里没有审稿人 {a.item}；有：{'、'.join(x['id'] for x in data['items'])}")
    if data.get("state") in CLOSED:
        raise SystemExit("这张审查单已收轮，不能再打勾；要重审请开下一轮。")
    if "slots" in it:
        return tick_slot(a, run, data, it)
    if getattr(a, "slot", ""):
        raise SystemExit("这张审查单是 v2 格式（每项一位审稿人），不用 --slot。")
    by = a.by.strip()
    if not by or by.lower() in {"author", "作者"} or by == data.get("author") or by.split("/")[-1] != it["id"]:
        raise SystemExit(f"打勾被拒：--by 必须是审稿人自己的身份「<模型>/{it['id']}」，作者（{data.get('author')}）不能替审稿人打勾。")
    rp = resolve(a.report)
    if not rp.is_file() or not rp.read_text(encoding="utf-8").strip():
        raise SystemExit(f"打勾被拒：报告不存在或是空的：{rp}")
    attested = None
    if getattr(a, "attest_log", ""):
        last = (it.get("agents") or [{}])[-1]
        if "codex" not in str(last.get("runner", "")).lower():
            raise SystemExit("代为登记被拒：--attest-log 只用于最近一次派给 Codex 的审稿人（Codex 沙箱跑不了 python）；"
                             "这一项最近的派单不是 Codex（先 dispatch 登记）。")
        attested = check_attest(a.attest_log, run, rp, it["report"], it.get("agents"), it["id"])
    text = rp.read_text(encoding="utf-8")
    counts, rows, clean = parse_report(text)
    if rows == 0 and not clean:
        raise SystemExit("打勾被拒：报告里没有含「严重度」列的问题表，也没有写「结论：无问题」。按审稿说明的格式改好再打勾。")
    must_res, missing = parse_must(text, it.get("must", []))
    if missing:
        raise SystemExit("打勾被拒：「## 必查项」里缺这些编号的 ✓/✗：" + "、".join(missing) + "。每个必查项都要写结论。")
    stale = stale_files(data)
    if stale:
        raise SystemExit("打勾被拒：审查开始后被审材料变了，这张审查单已作废，请重开：\n  " + "\n  ".join(stale[:10]))
    dst = run / it["report"]
    if rp != dst.resolve():
        dst.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(rp, dst)
    it.update(status="done", ticked_at=now(), ticked_by=by, findings=counts, rows=rows, clean=clean, must_result=must_res, report_sha=sha(dst))
    if attested:
        it["attested"] = attested
    if a.note:
        it["note"] = a.note
    event = "代为登记（审稿人进程无法运行 python，凭其运行日志）" if attested else "tick"
    data["log"].append({"at": now(), "item": it["id"], "event": event, "by": by,
                        **({"log": attested["log"]} if attested else {}), **({"note": a.note} if a.note else {})})
    data["state"] = state_of(data, [])
    save(run, data)
    done = sum(x["status"] == "done" for x in data["items"])
    print(f"已打勾：{it['id']}（{rows} 条；" + "，".join(f"{k} {v}" for k, v in counts.items() if v) +
          f"；必查 ✗ {sum(v == '✗' for v in must_res.values())}/{len(must_res)}）。进度 {done}/{len(data['items'])}，审查单状态：{data['state']}")
    return 0


def check_identity(by: str, data: dict, expect: str) -> None:
    if not by or by.lower() in {"author", "作者"} or by == data.get("author") or by.split("/")[-1] != expect:
        raise SystemExit(f"打勾被拒：--by 必须是审稿人自己的身份「<模型>/{expect}」，作者（{data.get('author')}）不能替审稿人打勾。")


def validate_scores(text: str, dims: list[str], rows: int, title: str = "评分表") -> dict[str, dict]:
    body = section(text, title)
    got, missing = parse_scores(body, dims)
    errs = []
    if missing:
        errs.append(f"「## {title}」里缺这些维度：" + "、".join(missing) + "（每维一行 `- <编号> <0–3> 证据：…`）")
    for d, v in got.items():
        s, ev = v["score"], v["evidence"]
        if s not in (0, 1, 2, 3):
            errs.append(f"{d} 分数 {s} 不在 0–3")
        elif s >= 2 and len(ev) < 8:
            errs.append(f"{d} 打了 {s} 分但没有证据（至少 8 个字，指到镜头、秒数、图上位置、文件行或数字）")
        elif s == 1 and rows == 0:
            errs.append(f"{d} 打 1 分（有问题），问题表里必须有对应条目")
        elif s == 0 and len(ev) < 2:
            errs.append(f"{d} 打 0 分（没查 / 查不了）要写原因")
    if errs:
        raise SystemExit("打勾被拒：\n  " + "\n  ".join(errs))
    return got


def dispatched_at(rec_list: list[dict]) -> dt.datetime | None:
    for rec in reversed(rec_list or []):
        try:
            return dt.datetime.fromisoformat(str(rec.get("at", "")).replace("Z", ""))
        except ValueError:
            continue
    return None


def check_attest(log: str, run: Path, rp: Path, report_rel: str, agents: list[dict] | None, tag: str) -> dict:
    """凭 Codex 运行日志代为登记：日志存在、含报告路径或文件名（任务书让它最后打印 `REPORT WRITTEN: <路径>`）、修改时间晚于派单。"""
    lp = resolve(log)
    if not lp.is_file():
        raise SystemExit(f"代为登记被拒：运行日志不存在：{lp}")
    log_text = lp.read_text(encoding="utf-8", errors="replace")
    dst = run / report_rel
    needles = {str(rp), rp.as_posix(), rel(rp), rp.name, str(dst), dst.as_posix(), rel(dst), Path(report_rel).name, report_rel}
    if not any(n and (n in log_text or n.replace("/", "\\") in log_text) for n in needles):
        raise SystemExit(f"代为登记被拒：运行日志里找不到报告路径或文件名（{rp.name}），不能证明是这位审稿人写的。")
    sent = dispatched_at(agents or [])
    if sent is None:
        raise SystemExit("代为登记被拒：这一位还没有派单记录（dispatch），无法核对日志时间。")
    if dt.datetime.fromtimestamp(lp.stat().st_mtime) <= sent:
        raise SystemExit(f"代为登记被拒：运行日志的修改时间早于派单时间（{sent.isoformat(timespec='seconds')}），不是这次审稿的日志。")
    keep = run / "agents" / f"{tag}_attest.log"          # 日志常在临时目录：留一份在审查单里备查
    keep.parent.mkdir(exist_ok=True); shutil.copyfile(lp, keep)
    return {"log": rel(lp), "copy": rel(keep), "at": now(), "log_sha": sha(lp)}


def tick_slot(a: argparse.Namespace, run: Path, data: dict, it: dict) -> int:
    """v5：一位审稿人（a / b 位）打勾。两位都勾了就自动对比（reconcile）。"""
    slot = (a.slot or "").strip() or (next(iter(it["slots"])) if len(it["slots"]) == 1 else "")   # 单审不用写 --slot
    if slot not in it["slots"]:
        raise SystemExit(f"打勾被拒：v5 审查单每项有两位审稿人，要用 --slot {'|'.join(it['slots'])} 指明是哪一位。")
    s = it["slots"][slot]
    by = a.by.strip()
    check_identity(by, data, f"{it['id']}__{slot}")      # 结尾 __a / __b 不同，两位天然是不同身份
    rp = resolve(a.report)
    if not rp.is_file() or not rp.read_text(encoding="utf-8").strip():
        raise SystemExit(f"打勾被拒：报告不存在或是空的：{rp}")
    attested = None
    if a.attest_log:
        if s["runner"] != "codex":
            raise SystemExit("代为登记被拒：--attest-log 只用于 Codex 审稿位（沙箱跑不了 python 时），Claude 审稿人自己打勾。")
        attested = check_attest(a.attest_log, run, rp, s["report"], s.get("agents"), f"{it['id']}__{slot}")
    text = rp.read_text(encoding="utf-8")
    counts, rows, clean = parse_report(text)
    if rows == 0 and not clean:
        raise SystemExit("打勾被拒：报告里没有含「严重度」列的问题表，也没有写「结论：无问题」。按审稿说明的格式改好再打勾。")
    scores = validate_scores(text, [r["id"] for r in it["rubric"]], rows)
    r_check = None
    if data.get("loop", 1) > 1:
        got, _ = parse_scores(section(text, "评分表"), ["R"])
        if "R" in got:
            r_check = "✓" if got["R"]["score"] >= 2 else "✗"
            if got["R"]["score"] >= 2 and len(got["R"]["evidence"]) < 8:
                raise SystemExit("打勾被拒：R（复核上一轮）打了高分但没有证据。")
        else:
            m, _ = parse_must(text, [{"id": "R", "text": ""}])
            r_check = m.get("R")
        if not r_check:
            raise SystemExit("打勾被拒：第 2、3 轮要在「## 评分表」（或「## 必查项」）写一行 R：逐条复核 previous.md 里的问题。")
    stale = stale_files(data)
    if stale:
        raise SystemExit("打勾被拒：审查开始后被审材料变了，这张审查单已作废，请重开：\n  " + "\n  ".join(stale[:10]))
    dst = run / s["report"]
    if rp != dst.resolve():
        dst.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(rp, dst)
    if by.split("/")[0] != s["model"]:
        print(f"注意：名册给 {slot} 位排的是 {s['model']}，打勾署名是 {by.split('/')[0]}。")
    s.update(status="done", ticked_at=now(), by=by, scores=scores, findings=counts, rows=rows, clean=clean,
             finding_rows=parse_rows(text), report_sha=sha(dst), **({"r_check": r_check} if r_check else {}))
    s.pop("note", None)
    if attested:
        s["attested"] = attested
    if a.note:
        s["note"] = a.note
    event = "代为登记（审稿人进程无法运行 python，凭其运行日志）" if attested else "tick"
    data["log"].append({"at": now(), "item": it["id"], "slot": slot, "event": event, "by": by,
                        **({"log": attested["log"]} if attested else {}), **({"note": a.note} if a.note else {})})
    it["ticked_by_list"] = [x["by"] for x in it["slots"].values() if x.get("status") == "done"]
    it["ticked_by"] = " + ".join(it["ticked_by_list"])
    it["ticked_at"] = now()
    if all(x.get("status") == "done" for x in it["slots"].values()):
        reconcile(run, data, it)
    else:
        it["status"] = "failed" if any(x.get("status") == "failed" for x in it["slots"].values()) else "pending"
        it.pop("judge", None)
    data["state"] = state_of(data, [])
    save(run, data)
    low = [f"{d} {v['score']}" for d, v in scores.items() if v["score"] <= 1]
    print(f"已打勾：{it['id']}__{slot}（{rows} 条问题；低分维度：{'、'.join(low) or '无'}）。该项状态：{it['status']}"
          + (f"（分歧 {len(it.get('disputes', []))}、抽查 {len(it.get('audits', []))}，裁决任务书 {it['judge']['prompt']}）" if it["status"] == "adjudicating" else "")
          + f"。进度 {sum(x['status'] == 'done' for x in data['items'])}/{len(data['items'])}，审查单状态：{data['state']}")
    return 0


def audit_pick(rid: str, iid: str, cands: list[str], k: int = 2) -> list[str]:
    """抽查哪几维：由 hash(审查单 id + 审稿项 id) 定种子，同一张单同一项每次抽到的一样。"""
    if len(cands) <= k:
        return list(cands)
    seed = int(hashlib.sha256(f"{rid}{iid}".encode("utf-8")).hexdigest()[:16], 16)
    picked = set(random.Random(seed).sample(cands, k))
    return [c for c in cands if c in picked]


def union_rows(groups: list[tuple[str, list[dict]]]) -> list[dict]:
    out, seen = [], {}
    for src, rows in groups:
        for r in rows:
            key = tuple(re.sub(r"\s+", "", c) for c in r["cells"])
            if key in seen:
                if src not in seen[key]["from"]:
                    seen[key]["from"].append(src)
                continue
            row = {**r, "from": [src]}
            seen[key] = row; out.append(row)
    return out


def reconcile(run: Path, data: dict, it: dict) -> None:
    if "b" not in it["slots"]:                  # Claude 单审（用户 2026-11-14，chuanyue_yiri follow-up 065）：无对比、无裁决，按 a 位定分
        a = it["slots"]["a"]
        it["scores"] = {r["id"]: {"name": r["name"], "a": a["scores"][r["id"]]["score"], "a_ev": a["scores"][r["id"]]["evidence"],
                                  "b": None, "b_ev": "", "verdict": "单审", "agreed": a["scores"][r["id"]]["score"], "final": None}
                        for r in it["rubric"]}
        it["disputes"], it["audits"], it["reconciled_at"] = [], [], now()
        it["finding_rows"] = union_rows([("a", a.get("finding_rows", []))])
        recount(it)
        it.pop("judge", None)
        finalize(it, {})
        data["log"].append({"at": now(), "item": it["id"], "event": "reconcile", "note": "单审（只有 a 位）→ 完成"})
        write_reconcile(run, it)
        return
    a, b = it["slots"]["a"], it["slots"]["b"]
    table = {}
    for r in it["rubric"]:
        d = r["id"]; sa, sb = a["scores"][d]["score"], b["scores"][d]["score"]
        dispute = abs(sa - sb) >= 2 or (min(sa, sb) <= 1 and max(sa, sb) >= 2)
        table[d] = {"name": r["name"], "a": sa, "a_ev": a["scores"][d]["evidence"], "b": sb, "b_ev": b["scores"][d]["evidence"],
                    "verdict": "分歧" if dispute else "一致", "agreed": None if dispute else min(sa, sb), "final": None}
    cands = [d for d, v in table.items() if v["verdict"] == "一致" and min(v["a"], v["b"]) >= 2]
    audits = audit_pick(data["id"], it["id"], cands)
    for d in audits:
        table[d]["verdict"] = "抽查"
    it["scores"] = table
    it["disputes"] = [d for d, v in table.items() if v["verdict"] == "分歧"]
    it["audits"] = audits
    it["reconciled_at"] = now()
    it["finding_rows"] = union_rows([("a", a.get("finding_rows", [])), ("b", b.get("finding_rows", []))])
    recount(it)
    dims = it["disputes"] + it["audits"]
    if dims:
        adj = data.get("adjudicator") or {"runner": "claude", "model": "claude-opus-5-5"}
        it["judge"] = {"runner": adj["runner"], "model": adj["model"], "status": "pending", "dims": dims,
                       "prompt": f"items/{it['id']}__judge.md", "report": f"reports/{it['id']}__judge.md", "agents": []}
        it["status"] = "adjudicating"
        (run / it["judge"]["prompt"]).write_text(judge_prompt(it, run, data), encoding="utf-8")
        data["log"].append({"at": now(), "item": it["id"], "event": "reconcile",
                            "note": f"分歧 {'、'.join(it['disputes']) or '无'}；抽查 {'、'.join(audits) or '无'} → 待裁决"})
    else:
        it.pop("judge", None)
        finalize(it, {})
        data["log"].append({"at": now(), "item": it["id"], "event": "reconcile", "note": "无分歧、无可抽查维度 → 完成"})
    write_reconcile(run, it)


def recount(it: dict) -> None:
    rows = it.get("finding_rows", [])
    it["findings"] = {s: sum(r["sev"] == s for r in rows) for s in SEVERITIES}
    it["rows"] = len(rows)
    it["clean"] = not rows


def finalize(it: dict, ruling: dict[str, dict]) -> None:
    for d, v in it["scores"].items():
        if d in ruling:
            v["final"] = ruling[d]["score"]; v["judge_reason"] = ruling[d]["evidence"]
        else:
            v["final"] = v["agreed"]
    it["final_scores"] = {d: v["final"] for d, v in it["scores"].items()}
    it["must_result"] = {d: ("✓" if f >= 2 else "✗") for d, f in it["final_scores"].items()}
    rc = [x.get("r_check") for x in it["slots"].values() if x.get("r_check")]
    if rc:
        it["must_result"]["R"] = "✗" if "✗" in rc else "✓"
    it["status"] = "done"
    it["done_at"] = now()


def write_reconcile(run: Path, it: dict) -> None:
    cell = lambda s: str(s).replace("|", "/").replace("\n", " ")
    if "b" not in it["slots"]:
        a = it["slots"]["a"]
        lines = [f"# {it['id']}（{it['law_name']}）单审", "", f"- 审稿人：{a.get('by')}（{a['model']}）报告 `{a['report']}`", "- 状态：完成", "",
                 "## 评分", "", "| 维度 | 分 | 证据 |", "|---|---|---|"]
        lines += [f"| {d} {cell(v['name'])} | {v['a']} | {cell(v['a_ev'])} |" for d, v in it["scores"].items()]
        lines += ["", "## 问题表", ""]
        if it.get("finding_rows"):
            lines += ["| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |", "|---|---|---|---|---|---|---|"]
            lines += [f"| {cell(r['shot'])} | {cell(r['sec'])} | {cell(r['sub'])} | {cell(r['sev'])} | {cell(r['gate'])} | {cell(r['evidence'])} | {cell(r['fix'])} |"
                      for r in sorted(it["finding_rows"], key=lambda r: SEVERITIES.index(r["sev"]) if r["sev"] in SEVERITIES else 9)]
        else:
            lines.append("结论：无问题")
        (run / "reconcile").mkdir(exist_ok=True)
        (run / it["report"]).write_text("\n".join(lines) + "\n", encoding="utf-8")
        return
    a, b = it["slots"]["a"], it["slots"]["b"]
    lines = [f"# {it['id']}（{it['law_name']}）双审对比", "",
             f"- a 位：{a.get('by')}（{a['model']}）报告 `{a['report']}`", f"- b 位：{b.get('by')}（{b['model']}）报告 `{b['report']}`",
             f"- 状态：{'待裁决' if it['status'] == 'adjudicating' else '完成'}"
             + (f"；裁决人 {it['judge'].get('by') or it['judge']['model']}，报告 `{it['judge']['report']}`" if it.get("judge") else ""), "",
             "## 评分对比", "", "| 维度 | a 分 | a 证据 | b 分 | b 证据 | 需裁决 | 最终 | 裁决理由 |", "|---|---|---|---|---|---|---|---|"]
    for d, v in it["scores"].items():
        fin = "待裁决" if v["final"] is None else str(v["final"])
        lines.append(f"| {d} {cell(v['name'])} | {v['a']} | {cell(v['a_ev'])} | {v['b']} | {cell(v['b_ev'])} | {v['verdict']} | {fin} | {cell(v.get('judge_reason', ''))} |")
    lines += ["", "## 问题表（两位审稿人与裁决人的并集，去掉完全相同的行）", ""]
    if it.get("finding_rows"):
        lines += ["| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 | 来自 |", "|---|---|---|---|---|---|---|---|"]
        lines += [f"| {cell(r['shot'])} | {cell(r['sec'])} | {cell(r['sub'])} | {cell(r['sev'])} | {cell(r['gate'])} | {cell(r['evidence'])} | {cell(r['fix'])} | {'、'.join(r['from'])} |"
                  for r in sorted(it["finding_rows"], key=lambda r: SEVERITIES.index(r["sev"]) if r["sev"] in SEVERITIES else 9)]
    else:
        lines.append("结论：无问题")
    (run / "reconcile").mkdir(exist_ok=True)
    (run / it["report"]).write_text("\n".join(lines) + "\n", encoding="utf-8")


def cmd_adjudicate(a: argparse.Namespace) -> int:
    run = resolve(a.run); data = load(run)
    it = next((x for x in data["items"] if x["id"] == a.item), None)
    if not it or "slots" not in it:
        raise SystemExit(f"审查单里没有 v5 审稿项 {a.item}")
    if data.get("state") in CLOSED:
        raise SystemExit("这张审查单已收轮，不能再裁决；要重审请开下一轮。")
    if it.get("status") != "adjudicating" or not it.get("judge"):
        raise SystemExit(f"{it['id']} 现在不需要裁决（状态 {it.get('status')}）：两位审稿人都打勾后才有裁决任务。")
    j = it["judge"]
    by = a.by.strip()
    check_identity(by, data, f"{it['id']}__judge")
    if by in [x.get("by") for x in it["slots"].values()]:
        raise SystemExit("裁决被拒：裁决人不能是这一项的审稿人。")
    rp = resolve(a.report)
    if not rp.is_file() or not rp.read_text(encoding="utf-8").strip():
        raise SystemExit(f"裁决被拒：报告不存在或是空的：{rp}")
    text = rp.read_text(encoding="utf-8")
    got, missing = parse_scores(section(text, "裁决"), j["dims"])
    errs = ([f"「## 裁决」里缺这些维度：{'、'.join(missing)}（每维一行 `- <编号> <最终分> 理由：…`）"] if missing else [])
    errs += [f"{d} 最终分 {v['score']} 不在 0–3" for d, v in got.items() if v["score"] not in (0, 1, 2, 3)]
    errs += [f"{d} 理由太短（至少 8 个字，引用证据）" for d, v in got.items() if len(v["evidence"]) < 8]
    if errs:
        raise SystemExit("裁决被拒：\n  " + "\n  ".join(errs))
    stale = stale_files(data)
    if stale:
        raise SystemExit("裁决被拒：审查开始后被审材料变了，这张审查单已作废，请重开：\n  " + "\n  ".join(stale[:10]))
    dst = run / j["report"]
    if rp != dst.resolve():
        dst.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(rp, dst)
    j.update(status="done", by=by, at=now(), ruling={d: v for d, v in got.items()}, report_sha=sha(dst))
    it["finding_rows"] = union_rows([("a", it["slots"]["a"].get("finding_rows", [])), ("b", it["slots"]["b"].get("finding_rows", [])),
                                     ("judge", parse_rows(text))])
    recount(it)
    finalize(it, got)
    write_reconcile(run, it)
    data["log"].append({"at": now(), "item": it["id"], "slot": "judge", "event": "adjudicate", "by": by,
                        "note": "；".join(f"{d}→{v['score']}" for d, v in got.items())})
    data["state"] = state_of(data, [])
    save(run, data)
    print(f"已裁决：{it['id']}（" + "，".join(f"{d} {it['scores'][d]['a']}/{it['scores'][d]['b']}→{v['score']}" for d, v in got.items()) +
          f"）。进度 {sum(x['status'] == 'done' for x in data['items'])}/{len(data['items'])}，审查单状态：{data['state']}")
    return 0


def cmd_fail(a: argparse.Namespace) -> int:
    run = resolve(a.run); data = load(run)
    it = next((x for x in data["items"] if x["id"] == a.item), None)
    if not it:
        raise SystemExit(f"审查单里没有审稿人 {a.item}")
    slot = getattr(a, "slot", "") or ""
    if "slots" in it:
        if slot == "judge":
            if not it.get("judge"):
                raise SystemExit(f"{it['id']} 还没有裁决任务")
            it["judge"].update(status="failed", note=a.note, failed_at=now())
        elif slot in it["slots"]:
            it["slots"][slot].update(status="failed", note=a.note, failed_at=now())
            it["status"] = "failed"; it.pop("judge", None)
        else:
            raise SystemExit(f"v5 审查单要用 --slot {'|'.join(it['slots'])}|judge 指明哪一位没审成。")
    else:
        it.update(status="failed", note=a.note, failed_at=now())
    data["log"].append({"at": now(), "item": it["id"], "event": "fail", "note": a.note, **({"slot": slot} if slot else {})})
    data["state"] = state_of(data, []); save(run, data)
    print(f"已记失败：{it['id']}{'__' + slot if slot else ''}。失败的不算审完，需重派后由审稿人打勾。")
    return 0


def cmd_drop_slot(a: argparse.Namespace) -> int:
    """把一张进行中的审查单改成单审（用户 2026-11-14，chuanyue_yiri follow-up 065：Codex 太慢，改为 Claude 单审）：
    去掉每项还没打勾的那一位（默认 b 位），记日志；剩下的位都已打勾的项马上按单审收尾。"""
    run = resolve(a.run); data = load(run)
    n = 0
    for it in data["items"]:
        s = it.get("slots", {}).get(a.slot)
        if not s or len(it["slots"]) < 2 or s.get("status") == "done":
            continue
        it.setdefault("dropped_slots", []).append({**s, "slot": a.slot, "dropped_at": now(), "note": a.note})
        del it["slots"][a.slot]
        n += 1
        data["log"].append({"at": now(), "item": it["id"], "slot": a.slot, "event": "drop-slot", "note": a.note})
        if all(x.get("status") == "done" for x in it["slots"].values()):
            reconcile(run, data, it)
    data["state"] = state_of(data, [])
    save(run, data)
    print(f"已去掉 {n} 个 {a.slot} 位；进度 {sum(x['status'] == 'done' for x in data['items'])}/{len(data['items'])}，审查单状态：{data['state']}")
    return 0


def cmd_dispatch(a: argparse.Namespace) -> int:
    """登记派单（follow-up 036，用户 2026-11-08：审查单要能看到每一步由哪个独立 agent 审、用的什么指令、什么 skill）。
    每派一次记一条：执行方式（Claude 子代理 / codex exec …）、模型、完整指令原文（另存 agents/<代号>_<n>.md）、依据的规则与技能、
    之后用 --reply-file 补登它最后的回复。只是元数据，不改被审材料，收轮后也能补登。"""
    run = resolve(a.run); data = load(run)
    it = next((x for x in data["items"] if x["id"] == a.item), None)
    if not it:
        raise SystemExit(f"审查单里没有审稿人 {a.item}")
    slot = a.slot or ""
    task = it["prompt"]
    if "slots" in it:                       # v5：记到这一位（a / b / 裁决人）自己的 agents；条目级 agents 另存一份带 slot 的镜像给管理站
        if slot == "judge":
            if not it.get("judge"):
                raise SystemExit(f"{it['id']} 还没到裁决（两位审稿人都打勾后才有裁决任务）")
            holder = it["judge"]
        elif slot in it["slots"]:
            holder = it["slots"][slot]
        else:
            raise SystemExit(f"v5 审查单要用 --slot {'|'.join(it['slots'])}|judge 指明派给哪一位。")
        task = holder["prompt"]
        agents = holder.setdefault("agents", [])
    elif slot:
        raise SystemExit("这张审查单是 v2 格式（每项一位审稿人），不用 --slot。")
    else:
        agents = it.setdefault("agents", [])
    if a.reply_file and not a.prompt_file:          # 只补登回复：挂到最近一次派单上
        if not agents:
            raise SystemExit("还没有派单记录，先登记派单再补回复")
        agents[-1]["reply"] = Path(a.reply_file).read_text(encoding="utf-8").strip()
        agents[-1]["replied_at"] = now()
        mirror = next((x for x in reversed(it.get("agents", [])) if slot and x.get("slot") == slot and x.get("n") == agents[-1]["n"]), None)
        if mirror is not None and mirror is not agents[-1]:
            mirror.update(reply=agents[-1]["reply"], replied_at=agents[-1]["replied_at"])
        save(run, data)
        print(f"已补登回复：{it['id']}{'__' + slot if slot else ''} 第 {len(agents)} 次派单"); return 0
    if not (a.runner and a.model and a.prompt_file):
        raise SystemExit("登记派单要给 --runner、--model 和 --prompt-file（发给审稿人的完整指令原文）")
    n = len(agents) + 1
    rel_prompt = f"agents/{it['id']}{'__' + slot if slot else ''}_{n}.md"
    (run / "agents").mkdir(exist_ok=True)
    (run / rel_prompt).write_text(Path(a.prompt_file).read_text(encoding="utf-8"), encoding="utf-8")
    law = it.get("law", "")
    skills = [s.strip() for s in (a.skills or "").split(";") if s.strip()] or [
        f"审稿人名册 .agents/references/project/review_roster.json · 法则 {law}（{it.get('law_name', '')}）",
        "审稿说明 BRIEF.md（材料、规则、报告格式）", f"任务书 {task}（范围、要查什么、怎么查、评分维度 / 必查项、打勾命令）"]
    rec = {"n": n, "at": a.at or now(), "runner": a.runner, "model": a.model, "context": a.context or "全新上下文，看不到作者会话与别的审稿报告",
           "prompt": rel_prompt, "skills": skills, **({"slot": slot} if slot else {})}
    if a.reply_file:
        rec["reply"] = Path(a.reply_file).read_text(encoding="utf-8").strip(); rec["replied_at"] = now()
    if a.note:
        rec["note"] = a.note
    agents.append(rec)
    if slot:
        it.setdefault("agents", []).append(dict(rec))
    data["log"].append({"at": now(), "item": it["id"], "event": "dispatch", "by": a.runner, "note": f"{a.model} · 第 {n} 次派单",
                        **({"slot": slot} if slot else {})})
    save(run, data)
    print(f"已登记派单：{it['id']}{'__' + slot if slot else ''} 第 {n} 次 · {a.runner} · {a.model} · 指令 {rel_prompt}")
    return 0


def state_of(data: dict, stale: list[str]) -> str:
    if data.get("state") in CLOSED and not stale:
        return "已收轮" if data["state"] == LEGACY_WAIT else data["state"]
    if stale:
        return "已作废"
    return "已完成" if all(x["status"] == "done" for x in data["items"]) else "进行中"


def show(run: Path, data: dict, stale: list[str]) -> None:
    done = sum(x["status"] == "done" for x in data["items"])
    print(f"{data['title']}  [{data['state']}]  第 {data.get('loop', 1)}/{data.get('max_loops', 3)} 轮  {done}/{len(data['items'])}  （{rel(run)}）")
    mark = {"done": "x", "failed": "!", "pending": " ", "adjudicating": "~"}
    for x in data["items"]:
        f = x.get("findings") or {}
        if "slots" in x:
            ticks = "  ".join(f"{k}{'✓' if s.get('status') == 'done' else '!' if s.get('status') == 'failed' else '○'} {s['model']}"
                              + ("（代登记）" if s.get("attested") else "") for k, s in x["slots"].items())
            j = x.get("judge")
            jtxt = (f"  裁决{'✓' if j.get('status') == 'done' else '!' if j.get('status') == 'failed' else '○'} {j['model']}" if j else "")
            sev = ("  " + "，".join(f"{k}{v}" for k, v in f.items() if v)) if x.get("scores") else ""
            print(f"  [{mark.get(x['status'], ' ')}] {x['id']:<14} {x['law_name']:<8} 范围：{'、'.join(x['scope'])}  {ticks}{jtxt}{sev}")
            if x.get("scores"):
                print("        " + "  ".join(f"{d} {v['a']}/{v['b']}→{'?' if v['final'] is None else v['final']}"
                                            + ("（分歧）" if v["verdict"] == "分歧" else "（抽查）" if v["verdict"] == "抽查" else "")
                                            for d, v in x["scores"].items()))
            for k, s in x["slots"].items():
                if s.get("status") == "failed":
                    print(f"        {k} 位失败：{s.get('note', '')}")
            continue
        extra = ("  " + "，".join(f"{k}{v}" for k, v in f.items() if v)) if x["status"] == "done" else (f"  失败：{x.get('note', '')}" if x["status"] == "failed" else "")
        print(f"  [{mark.get(x['status'], ' ')}] {x['id']:<14} {x['law_name']:<8} 范围：{'、'.join(x['scope'])}{extra}")
    if (run / ISSUES_JSON).is_file():
        iss = load_issues(run)
        open_ = [i for i in iss if not resolved(i)]
        print(f"  问题清单 {len(iss)} 条（" + "，".join(f"{LEVEL_NAME[l]} {sum(i['level'] == l for i in iss)}" for l in LEVELS) +
              f"）；未处理 {len(open_)}，其中严重 {sum(i['level'] == 'critical' for i in open_)}")
    if stale:
        print("  材料已变（审查单作废）：" + "、".join(stale[:6]) + ("…" if len(stale) > 6 else ""))


def migrate_state(data: dict) -> bool:
    """旧单的「待用户确认」→「已收轮」（用户 2026-11-08：每轮审查结果不要用户 review，不该有等用户的状态）。返回是否改了。"""
    if data.get("state") != LEGACY_WAIT:
        return False
    data["state"] = "已收轮"
    data.setdefault("log", []).append({"at": now(), "event": "migrate",
                                       "note": f"状态「{LEGACY_WAIT}」→「已收轮」：每轮审查不再等用户 review，用户只在出片时确认"})
    return True


def cmd_status(a: argparse.Namespace, gate: bool = False) -> int:
    run = resolve(a.run); data = load(run)
    if migrate_state(data):
        attach_result_verdict(run, data)
        save(run, data)
        print(f"已迁移：{rel(run)} 状态「{LEGACY_WAIT}」→「已收轮」")
    stale = stale_files(data)
    st = state_of(data, stale)
    if st != data.get("state"):
        data["state"] = st; save(run, data)
    show(run, data, stale)
    if gate:
        v5 = int(data.get("version", 2)) >= 5
        if st in CLOSED and (v5 or (run / ISSUES_JSON).is_file()):
            crit = [i for i in write_issues(run, data) if i["level"] == "critical" and not resolved(i)]
            if crit:
                print(f"未处理的严重（critical）问题 {len(crit)} 个：")
                for i in crit:
                    print(f"  {i['id']} [{i['status']}] {i['category']} {i['dimension']} {'、'.join(i['shots'])}：{i['problem'][:60]}")
                if st != "用户已确认出片":
                    print("审查闸门：不通过（收轮后仍有未处理的严重问题：fix 记方案并实施，或 wontfix 写理由；要不要带着它出片，出片时由用户决定）"); return 1
                print("（用户已确认出片，按用户决定放行）")
        if st in {"已完成"} | CLOSED:
            print("审查闸门：通过（" + ("全部双审、对比、裁决完成" if v5 else "全部打勾") + "，材料未变）"); return 0
        waiting = "还有没打勾的审稿人"
        if any(x.get("status") == "adjudicating" for x in data["items"]):
            waiting += "或待裁决的项"
        print("审查闸门：不通过（" + ("材料已变，重开审查单" if stale else waiting) + "）"); return 1
    return 0


def chain_runs(data: dict, root: Path) -> list[tuple[Path, dict]]:
    out = []
    for p in sorted(root.glob(f"*/{CHECKLIST}")):
        d = json.loads(p.read_text(encoding="utf-8"))
        if d.get("chain", d["id"]) == data.get("chain", data["id"]):
            out.append((p.parent, d))
    return sorted(out, key=lambda x: x[1].get("loop", 1))


def verdict_from_text(text: str) -> dict:
    t = (text or "").strip()
    res = "不可出片" if re.search(r"不可出片|不建议|不能出片|暂不|先修", t) else "可出片" if ("可出片" in t or "可以出片" in t) else ""
    return {"result": res, "text": t, "reasons": []}


def attach_result_verdict(run: Path, data: dict) -> None:
    """旧单的结论只写在「结果.md」的「- 结论：」一行：迁移时抄进 checklist 的 verdict。"""
    if (data.get("verdict") or {}).get("text"):
        return
    rp = run / (data.get("result") or RESULT)
    m = re.search(r"^- 结论[:：]\s*(.+)$", rp.read_text(encoding="utf-8"), re.M) if rp.is_file() else None
    if m:
        data["verdict"] = verdict_from_text(m.group(1))


def auto_verdict(run: Path, data: dict, issues: list[dict] | None) -> dict:
    """收轮结论：还有未处理的严重问题 → 不可出片（理由列出）；否则可出片。v2 单没有问题清单时按报告里的问题表现推（不写 issues.json）。"""
    if issues is None:
        issues = derive_issues(run, data) if all(x.get("status") == "done" for x in data["items"]) else []
        for i in issues:
            i.setdefault("status", "open")
    crit = [i for i in issues if i["level"] == "critical" and not resolved(i)]
    if crit:
        reasons = [f"{(i.get('id') + ' ') if i.get('id') else ''}{i['category']}·{i['dimension']} {'、'.join(i['shots'])}：{i['problem'][:60]}"
                   for i in crit[:12]] + ([f"……另有 {len(crit) - 12} 个"] if len(crit) > 12 else [])
        return {"result": "不可出片", "text": f"还有 {len(crit)} 个严重问题没处理", "reasons": reasons}
    return {"result": "可出片", "text": "没有未处理的严重问题", "reasons": []}


def accept_fixes(run: Path, data: dict, stale: list[str]) -> None:
    """最后一轮修复落地后，材料必然变了，按修复后的材料收轮（follow-up 069）：只限最后一轮、全部打勾、严重与主要问题都已登记处理。
    记下被审版本的指纹和修复改动的文件；这些修复没有再经独立审稿，由用户出片前在对话里审（confirm 时材料又变仍会拦）。"""
    loop, top = int(data.get("loop", 1)), int(data.get("max_loops", 3))
    if loop < top:
        raise SystemExit(f"--accept-fixes 只用于最后一轮（第 {top} 轮），现在是第 {loop} 轮：修复后开下一轮复审。")
    if not all(x["status"] == "done" for x in data["items"]):
        raise SystemExit("还不能收轮：要全部打勾。")
    issues = write_issues(run, data) if int(data.get("version", 2)) >= 5 else load_issues(run)
    open_ = [i["id"] for i in issues if i["level"] in ("critical", "major") and not resolved(i)]
    if open_:
        raise SystemExit("严重 / 主要问题还没登记处理（review_run.py fix）：" + "、".join(open_))
    if data.get("state") == "用户已确认出片":
        raise SystemExit("用户已确认出片，之后材料再变要重开审查单，不能再按修复后的材料收轮。")
    if data.get("state") == "已收轮":                       # 收轮后、用户确认前又补了修复：重新收轮，被审版本仍是最初那份
        data["state"] = "已完成"
    ep = REPO / data["target"]
    data.setdefault("reviewed_materials", data.get("materials", {}))
    stale = sorted(set(stale) | set((data.get("accepted_fixes") or {}).get("changed", [])))
    data["materials"] = fingerprint(ep, data["stage"], layout(ep), data["scenes"] if data.get("fp_scope") == "scenes" else None)
    data["accepted_fixes"] = {"at": now(), "changed": stale}
    data["log"].append({"at": now(), "event": "accept_fixes", "note": f"按修复后材料收轮，修复改了 {len(stale)} 个文件，未经独立复审"})


def cmd_conclude(a: argparse.Namespace) -> int:
    run = resolve(a.run); data = load(run)
    stale = stale_files(data)
    if getattr(a, "accept_fixes", False) and stale:
        accept_fixes(run, data, stale)
        stale = []
    if state_of(data, stale) != "已完成":
        raise SystemExit("还不能收轮：要全部打勾且材料未变。")
    rounds = chain_runs(data, run.parent)
    v5 = int(data.get("version", 2)) >= 5
    issues = write_issues(run, data) if v5 else (load_issues(run) or None)
    verdict = auto_verdict(run, data, issues)
    if a.verdict.strip():
        given = verdict_from_text(a.verdict)
        verdict = {"result": given["result"] or verdict["result"], "text": given["text"], "reasons": verdict["reasons"]}
    head = f"- 结论：{verdict['result']}" + (f"：{verdict['text']}" if verdict["text"] and verdict["text"] != verdict["result"] else "")
    lines = [f"# 审查结果：{data['title']}", "",
             f"- 集：{data['target']}；阶段：{data['stage_name']}；共 {len(rounds)} 轮（上限 {data.get('max_loops', 3)}）；最后一轮：`{rel(run)}`",
             head, *[f"  - {r}" for r in verdict["reasons"]],
             "- 每轮审查不等用户 review；出片时用户在对话里确认，`shot_take.py` 出片前会检查（`review_run.py can-submit`）。",
             "", "## 各轮", "", "| 轮 | 审查单 | 审稿人 | 重出 | 可剪 | 记录 | 存疑 | 这轮之前改了什么 |", "|---|---|---|---|---|---|---|---|"]
    for p, d in rounds:
        t = {s: sum((x.get("findings") or {}).get(s, 0) for x in d["items"]) for s in SEVERITIES}
        ch = (d.get("changes") or "").strip().splitlines()
        lines.append(f"| {d.get('loop', 1)} | `{p.name}` | {len(d['items'])} | {t['重出']} | {t['可剪']} | {t['记录']} | {t['存疑']} | {(ch[0][:60] + '…') if ch else '—'} |")
    if v5:
        lines += ["", *score_summary(data), "", "## 问题清单（由评分与问题表推出，详见 issues.md）", "",
                  "| 级别 | 总数 | 未处理 |", "|---|---|---|",
                  *[f"| {LEVEL_NAME[l]}（{l}） | {sum(i['level'] == l for i in issues)} | {sum(i['level'] == l and not resolved(i) for i in issues)} |" for l in LEVELS],
                  "", "## 最后一轮仍未解决的问题", ""]
        rest = [i for i in issues if not resolved(i) and i["level"] != "minor"]
        lines += issue_table(rest) if rest else ["（无）"]
    else:
        lines += ["", "## 最后一轮仍未解决的问题（重出 / 可剪 / 存疑）", ""]
        lines += [ln for ln in previous_md(run, data).splitlines()[4:]]
    if data.get("accepted_fixes"):
        ch = data["accepted_fixes"]["changed"]
        lines += ["", "## 最后一轮修复（未经独立复审）", "",
                  f"最后一轮审完后按问题清单修复，改了 {len(ch)} 个被审文件；按修复后的材料收轮（--accept-fixes）。"
                  "这些修复没有再经独立审稿，出片前由用户在对话里审；之后材料再变，confirm / 出片闸门照样拦。", "",
                  *[f"- `{c}`" for c in ch[:40]], *([f"- …共 {len(ch)} 个"] if len(ch) > 40 else [])]
    if a.note:
        lines += ["", "## 作者说明", a.note]
    (run / RESULT).write_text("\n".join(lines) + "\n", encoding="utf-8")
    data["state"] = "已收轮"; data["concluded_at"] = now(); data["result"] = RESULT; data["verdict"] = verdict
    data["log"].append({"at": now(), "event": "conclude", "note": f"{verdict['result']}：{verdict['text']}"})
    save(run, data)
    print(f"已收轮：{rel(run / RESULT)}；结论：{verdict['result']}（{verdict['text']}）。"
          + ("出片时用户在对话里同意后运行 confirm --quote，shot_take 出片前会检查。" if verdict["result"] == "可出片" else ""))
    return 0


def cmd_confirm(a: argparse.Namespace) -> int:
    run = resolve(a.run); data = load(run)
    migrate_state(data)
    if data.get("state") != "已收轮":
        raise SystemExit(f"只有「已收轮」的审查单能登记出片确认（现在是 {data.get('state')}）。先 conclude。")
    if stale_files(data):
        raise SystemExit("收轮后被审材料又变了：要重开审查单。")
    if not a.quote.strip():
        raise SystemExit("--quote 要写用户在对话里同意出片的原话。")
    data.update(state="用户已确认出片", confirmed_at=now(), confirm_quote=a.quote.strip())
    data["log"].append({"at": now(), "event": "confirm", "quote": a.quote.strip()})
    save(run, data)
    print(f"已登记用户确认：{rel(run)}")
    return 0


def cmd_migrate(a: argparse.Namespace) -> int:
    """把旧单的「待用户确认」改成「已收轮」（结论从结果.md 抄进 verdict），每张写一条 log。给剧目录、reviews 目录或一张审查单；不给就扫全部剧。"""
    if a.target:
        p = resolve(a.target)
        files = ([p / CHECKLIST] if (p / CHECKLIST).is_file() else sorted(p.glob(f"*/{CHECKLIST}")) or sorted(p.glob(f"reviews/*/{CHECKLIST}")))
    else:
        files = sorted((REPO / "ai_videos").glob(f"*/reviews/*/{CHECKLIST}")) + sorted((REPO / "ai_videos").glob(f"*/*/reviews/*/{CHECKLIST}"))
    n = 0
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        if migrate_state(data):
            attach_result_verdict(f.parent, data)
            save(f.parent, data); n += 1
            print(f"已迁移：{rel(f.parent)}  {LEGACY_WAIT} → 已收轮（结论：{(data.get('verdict') or {}).get('result') or '—'}）")
    print(f"共迁移 {n} 张（看了 {len(files)} 张）")
    return 0


# ---------------------------------------------------------------- 评分汇总、问题清单、方案（v5，用户 2026-11-08）
ISSUES_JSON = "issues.json"
ISSUES_MD = "issues.md"


def score_summary(data: dict) -> list[str]:
    """每一类：两位审稿人的分并排，加最终分（多段范围取最低），再列分歧与抽查怎么裁的。"""
    laws: dict[str, list[dict]] = {}
    for it in data["items"]:
        if "slots" in it:
            laws.setdefault(it["law"], []).append(it)
    out = ["## 各类评分（0–3；a＝Claude、b＝Codex；多段范围取最低）", ""]
    for its in laws.values():
        first = its[0]
        out += [f"### {first['law_name']}（{'、'.join(x['id'] for x in its)}）", "",
                f"| 维度 | a（{first['slots']['a']['model']}） | b（{first['slots'].get('b', {}).get('model', '单审，无 b 位')}） | 最终 |", "|---|---|---|---|"]
        for r in first["rubric"]:
            d = r["id"]
            vals = [x["scores"][d] for x in its if x.get("scores") and d in x["scores"]]
            if not vals:
                out.append(f"| {d} {r['name']} | — | — | 未审完 |"); continue
            fins = [v["final"] for v in vals if v["final"] is not None]
            final = str(min(fins)) if len(fins) == len(vals) else "待裁决"
            out.append(f"| {d} {r['name']} | {min(v['a'] for v in vals)} | {min((v['b'] for v in vals if v['b'] is not None), default='—')} | {final} |")
        rulings = []
        for x in its:
            for d in x.get("disputes", []) + x.get("audits", []):
                v = x["scores"][d]
                rulings.append(f"- {x['id']} {d} {v['name']}（{v['verdict']}）：a {v['a']} / b {v['b']} → "
                               + ("待裁决" if v["final"] is None else f"{v['final']}") + (f"；理由：{v['judge_reason']}" if v.get("judge_reason") else ""))
        out += ["", "分歧与抽查的裁决：", *rulings, ""] if rulings else ["", "无分歧、无抽查维度。", ""]
    return out


def load_issues(run: Path) -> list[dict]:
    p = run / ISSUES_JSON
    return json.loads(p.read_text(encoding="utf-8")).get("issues", []) if p.is_file() else []


def resolved(i: dict) -> bool:
    return i.get("status") == "implemented" or (i.get("status") == "wontfix" and bool((i.get("reason") or "").strip()))


def _norm(s: str) -> str:
    return re.sub(r"[\s`*_]", "", s or "").lower()


def _uniq(xs) -> list:
    out = []
    for x in xs:
        if x and x not in out:
            out.append(x)
    return out


def cost_of(fixes: list[str]) -> str:
    text = " ".join(fixes)
    return "要积分" if "要积分" in text else "便宜" if "便宜" in text else ""


def dims_in(text: str, rubric: list[dict]) -> list[str]:
    return [r["id"] for r in rubric if re.search(rf"(?<![A-Za-z0-9]){re.escape(r['id'])}(?![A-Za-z0-9])", text or "")
            or (len(r.get("name", "")) >= 2 and r["name"] in (text or ""))]


def derive_issues(run: Path, data: dict) -> list[dict]:
    """问题清单：最终分 ≤1 的维度各成一条（带两位审稿人的证据与对应问题行）；问题表里其余的行按「镜头＋法则·子类」去重各成一条。
    级别：critical＝某维 0 分、任一重出行、或名册标 critical 的维度 ≤1；major＝其余 1 分维度与可剪行；minor＝记录；verify＝存疑。"""
    out, by_key = [], {}
    for it in data["items"]:
        if it.get("status") != "done":
            continue
        rubric = it.get("rubric") or []
        if "slots" in it:
            names = {k: s.get("by") or f"{it['id']}__{k}" for k, s in it["slots"].items()}
            if (it.get("judge") or {}).get("by"):
                names["judge"] = it["judge"]["by"]
            rows = it.get("finding_rows", [])
        else:
            names = {"v2": it.get("ticked_by") or it["id"]}
            rp = run / it["report"]
            rows = [{**r, "from": ["v2"]} for r in parse_rows(rp.read_text(encoding="utf-8"))] if rp.is_file() else []
        used: set[int] = set()
        crit = {r["id"] for r in rubric if r.get("critical")}
        q = {r["id"]: r.get("question", "") for r in rubric}
        for d, v in (it.get("scores") or {}).items():
            f = v.get("final")
            if f is None or f > 1:
                continue
            match = [k for k, r in enumerate(rows) if d in dims_in(r["sub"], rubric)] or \
                    [k for k, r in enumerate(rows) if re.search(rf"(?<![A-Za-z0-9]){re.escape(d)}(?![A-Za-z0-9])", r["raw"])]
            used |= set(match)
            mrows = [rows[k] for k in match]
            level = "critical" if f == 0 or d in crit or any(r["sev"] == "重出" for r in mrows) else "major"
            ev = [f"a（{v['a']} 分）：{v['a_ev']}"] + ([f"b（{v['b']} 分）：{v['b_ev']}"] if v.get("b") is not None else [])
            ev += [f"裁决（{f} 分）：{v['judge_reason']}"] if v.get("judge_reason") else []
            ev += [r["evidence"] for r in mrows if r["evidence"]]
            fixes = _uniq(r["fix"] for r in mrows)
            out.append({"key": f"dim:{it['id']}:{d}", "level": level, "law": it["law"], "category": it["law_name"], "item": it["id"],
                        "dimension": f"{d} {v['name']}", "shots": _uniq(r["shot"] for r in mrows),
                        "problem": f"{d} {v['name']} 最终 {f} 分：{q.get(d, '')}" + (f"；{mrows[0]['evidence']}" if mrows and mrows[0]["evidence"] else ""),
                        "evidence": ev, "sources": _uniq([names.get("a"), names.get("b"), names.get("judge") if v.get("judge_reason") else None]
                                                         + [names.get(s) for r in mrows for s in r["from"]]),
                        "fix": "；".join(fixes), "cost": cost_of(fixes), "scores": {"a": v["a"], "b": v["b"], "final": f},
                        "rows": [r["raw"] for r in mrows]})
        for k, r in enumerate(rows):
            if k in used:
                continue
            level = SEV_LEVEL.get(r["sev"], "verify")
            key = f"row:{it['law']}:{_norm(r['shot'])}:{_norm(r['sub'])}"
            src = [names.get(s, s) for s in r["from"]]
            if key in by_key:
                i = by_key[key]
                if LEVELS.index(level) < LEVELS.index(i["level"]):
                    i["level"] = level
                i["evidence"] = _uniq(i["evidence"] + [r["evidence"]])
                i["sources"] = _uniq(i["sources"] + src)
                fixes = _uniq(i["fix"].split("；") + [r["fix"]])
                i.update(fix="；".join(fixes), cost=cost_of(fixes))
                i["rows"].append(r["raw"])
                continue
            i = {"key": key, "level": level, "law": it["law"], "category": it["law_name"], "item": it["id"], "dimension": r["sub"],
                 "shots": _uniq([r["shot"]]), "problem": f"{r['sub']}：{r['evidence']}" if r["sub"] else r["evidence"],
                 "evidence": _uniq([r["evidence"]]), "sources": _uniq(src), "fix": r["fix"], "cost": cost_of([r["fix"]]),
                 "severity": r["sev"], "rows": [r["raw"]]}
            by_key[key] = i; out.append(i)
    order = {x["id"]: n for n, x in enumerate(data["items"])}
    return sorted(out, key=lambda i: (LEVELS.index(i["level"]), order.get(i["item"], 99)))


def write_issues(run: Path, data: dict) -> list[dict]:
    """推导问题清单并与已有 issues.json 合并（按 key 保留编号、方案、状态）；写 issues.json 与 issues.md。"""
    old = {i["key"]: i for i in load_issues(run)}
    n = max([int(i["id"][1:]) for i in old.values() if re.fullmatch(r"I\d+", i.get("id", ""))] or [0])
    issues = []
    for i in derive_issues(run, data):
        prev = old.get(i["key"])
        if prev:
            i.update(id=prev["id"], status=prev.get("status", "open"), solution=prev.get("solution", ""),
                     reason=prev.get("reason", ""), history=prev.get("history", []))
            i.update({k: prev[k] for k in ("files", "frames", "solution_source") if prev.get(k)})      # fix --file / --before --after 登记的
        else:
            n += 1
            i.update(id=f"I{n}", status="open", solution="", reason="", history=[])
        issues.append(i)
    (run / ISSUES_JSON).write_text(json.dumps({"run": data["id"], "generated_at": now(), "issues": issues}, ensure_ascii=False, indent=1),
                                   encoding="utf-8")
    (run / ISSUES_MD).write_text(issues_md(data, issues), encoding="utf-8")
    return issues


def _c(s) -> str:
    return str(s or "").replace("|", "/").replace("\n", " ")


def issue_table(issues: list[dict]) -> list[str]:
    lines = ["| 问题 | 级别 | 类别·维度 | 镜头 | 问题 | 来源 | 建议改动 | 成本 | 状态 | 方案 |", "|---|---|---|---|---|---|---|---|---|---|"]
    for i in issues:
        lines.append(f"| {i['id']} | {LEVEL_NAME[i['level']]} | {_c(i['category'])}·{_c(i['dimension'])} | {_c('、'.join(i['shots']))} | "
                     f"{_c(i['problem'][:120])} | {_c('、'.join(i['sources']))} | {_c(i['fix'])} | {i['cost'] or '—'} | {i['status']} | "
                     f"{_c(i.get('solution'))}{'（理由：' + _c(i['reason']) + '）' if i.get('reason') else ''} |")
    return lines


def issues_md(data: dict, issues: list[dict]) -> str:
    lines = [f"# 问题清单：{data['title']}", "",
             "由双审评分（最终分 ≤1 的维度）与问题表推出。严重＝某维 0 分、任一「重出」、或关键维度 ≤1；主要＝其余 1 分维度与「可剪」；"
             "待核实＝「存疑」；记录＝「记录」。每条用 `review_run.py fix <审查单> <I编号> --solution \"…\" --status planned|implemented|wontfix` 记方案；"
             "严重与主要都 implemented（或 wontfix 写理由）后才能开下一轮。", "",
             "| 级别 | 条数 | 未处理 |", "|---|---|---|",
             *[f"| {LEVEL_NAME[l]}（{l}） | {sum(i['level'] == l for i in issues)} | {sum(i['level'] == l and not resolved(i) for i in issues)} |" for l in LEVELS],
             "", *(issue_table(issues) if issues else ["（没有问题）"]), "", "## 证据", ""]
    for i in issues:
        lines += [f"### {i['id']} {LEVEL_NAME[i['level']]} · {i['category']} · {i['dimension']}", *[f"- {e}" for e in i["evidence"] if e]]
        if i.get("scores"):
            lines.append(f"- 分数：a {i['scores']['a']} / b {i['scores']['b']} → 最终 {i['scores']['final']}")
        lines += [*[f"  {r}" for r in i["rows"]], ""]
    return "\n".join(lines) + "\n"


def changes_from_issues(issues: list[dict], user: str) -> str:
    done = [i for i in issues if i.get("solution") or i.get("status") != "open"]
    lines = ["## 按问题清单的方案（review_run.py fix 登记）", ""]
    lines += ([f"- {i['id']} [{LEVEL_NAME[i['level']]}·{i['status']}] {i['category']}·{i['dimension']} {'、'.join(i['shots'])}：{i.get('solution') or '—'}"
               + (f"（理由：{i['reason']}）" if i.get("reason") else "") for i in done] or ["（无）"])
    if user.strip():
        lines += ["", "## 补充说明", user.strip()]
    return "\n".join(lines)


def previous_from_issues(prev_run: Path, prev: dict, issues: list[dict]) -> str:
    out = [f"# 上一轮（第 {prev.get('loop', 1)} 轮）的问题清单", "", f"审查单：`{prev_run}`（详见其 issues.md）", "",
           "本轮每位审稿人在「## 评分表」的 R 一行逐条复核**本类别**的问题：是否已按「方案」改好、有没有带出新问题；没改好的写进问题表。", ""]
    by_law: dict[str, list[dict]] = {}
    for i in issues:
        by_law.setdefault(i["category"], []).append(i)
    for cat, xs in by_law.items():
        out += [f"## {cat}", "", *issue_table(xs), ""]
    if not issues:
        out.append("（上一轮没有问题）")
    return "\n".join(out)


def cmd_issues(a: argparse.Namespace) -> int:
    run = resolve(a.run); data = load(run)
    if any(x.get("status") != "done" for x in data["items"]):
        raise SystemExit("还没审完（有审稿项未打勾或待裁决），推不出完整的问题清单。")
    issues = write_issues(run, data)
    print(f"问题清单：{rel(run / ISSUES_MD)}（" + "，".join(f"{LEVEL_NAME[l]} {sum(i['level'] == l for i in issues)}" for l in LEVELS) + "）")
    for i in issues:
        print(f"  {i['id']:<4} {i['level']:<8} {i['status']:<11} {i['category']}·{i['dimension']} {'、'.join(i['shots'])} — {i['problem'][:60]}"
              + (f"  [{i['cost']}]" if i["cost"] else ""))
    return 0


def cmd_fix(a: argparse.Namespace) -> int:
    run = resolve(a.run); data = load(run)
    issues = load_issues(run) or (write_issues(run, data) if all(x.get("status") == "done" for x in data["items"]) else [])
    i = next((x for x in issues if x["id"] == a.issue), None)
    if not i:
        raise SystemExit(f"问题清单里没有 {a.issue}（先运行 issues）；有：{'、'.join(x['id'] for x in issues) or '无'}")
    if a.status not in FIX_STATUS[1:]:
        raise SystemExit("--status 只能是 planned / implemented / wontfix")
    if not a.solution.strip():
        raise SystemExit("--solution 要写准备怎么改 / 已经怎么改了（wontfix 写不改的处理方式）")
    if a.status == "wontfix" and not a.reason.strip():
        raise SystemExit("wontfix 必须用 --reason 写为什么不改（例如：要积分、收益小、交用户决定）")
    befores, afters = a.before or [], a.after or []
    if len(befores) != len(afters):
        raise SystemExit("--before 与 --after 要成对给（每张旧图对一张新图）")
    for f in befores + afters:
        if not resolve(f).is_file():
            raise SystemExit(f"图不存在：{f}")
    files = [rel(resolve(f)) for f in (a.file or [])]
    for f in files:
        if not (REPO / f).exists():
            print(f"注意：{f} 现在不存在（已删除或路径写错）")
    frames = [{"before": rel(resolve(b)), "after": rel(resolve(c))} for b, c in zip(befores, afters)]
    i.update(solution=a.solution.strip(), status=a.status, reason=a.reason.strip())
    if files:
        i["files"] = _uniq(i.get("files", []) + files)
    if frames:
        i["frames"] = i.get("frames", []) + [f for f in frames if f not in i.get("frames", [])]
    i.setdefault("history", []).append({"at": now(), "status": a.status, "solution": a.solution.strip(),
                                        **({"reason": a.reason.strip()} if a.reason else {}), **({"by": a.by.strip()} if a.by.strip() else {}),
                                        **({"files": files} if files else {}), **({"frames": frames} if frames else {})})
    (run / ISSUES_JSON).write_text(json.dumps({"run": data["id"], "generated_at": now(), "issues": issues}, ensure_ascii=False, indent=1), encoding="utf-8")
    (run / ISSUES_MD).write_text(issues_md(data, issues), encoding="utf-8")
    data["log"].append({"at": now(), "event": "fix", "item": i["item"], "note": f"{i['id']} → {a.status}：{a.solution.strip()[:80]}",
                        **({"by": a.by.strip()} if a.by.strip() else {})})
    save(run, data)
    left = [x for x in issues if x["level"] in ("critical", "major") and not resolved(x)]
    print(f"已登记：{i['id']} {a.status}" + (f"（文件 {len(files)} 个）" if files else "") + (f"（前后图 {len(frames)} 对）" if frames else "") +
          f"。严重 / 主要问题还剩 {len(left)} 个未处理" + ("；全部处理后可 new --after 开下一轮。" if left else "，可以 new --after 开下一轮。"))
    return 0


# ---------------------------------------------------------------- 修复页（用户 2026-11-08：审查结果链到修复页，两边关联）
CORR_JSON = "corrections.json"
CORR_MD = "corrections.md"
SPEC_FIELDS = (("duration", "时长"), ("cast", "出场"), ("action", "动作"), ("blocking", "走位"), ("beats", "节拍"), ("camera", "镜头"),
               ("lighting", "光线"), ("dialogue", "台词"), ("props", "道具"), ("extras", "路人"), ("point", "看点"))
SPEC_MD_KEYS = {"动作": "action", "走位": "blocking", "节拍": "beats", "镜头": "camera", "光线": "lighting", "台词": "dialogue"}
VERIFY = ("已复核通过", "复核仍有问题", "待复核")


def _val(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    if isinstance(v, list):
        return ", ".join(_val(x) for x in v)
    if isinstance(v, dict):
        return json.dumps(v, ensure_ascii=False, sort_keys=True)
    t = str(v).strip()
    return "" if t in ("（无）", "None") else t


def parse_spec_md(text: str) -> dict[str, str]:
    """审查单 materials/shots/<场>_<镜>/spec.md（spec_lines 写的格式）→ 字段。只有这些字段：时长、出场、动作、走位、节拍、镜头、光线、台词。"""
    out: dict[str, str] = {}
    m = re.search(r"设计时长[:：]\s*([\d.]+)\s*秒", text)
    if m:
        out["duration"] = _val(float(m.group(1)))
    m = re.search(r"出场[:：]\s*([^；;\n]*)", text)
    if m:
        out["cast"] = ", ".join(x.strip() for x in m.group(1).split(",") if x.strip())
    body = text.split("## 分镜规格", 1)[1] if "## 分镜规格" in text else ""
    marks = list(re.finditer(r"^\*\*(动作|走位|节拍|镜头|光线|台词)\*\*[:：]", body, re.M))
    for k, mk in enumerate(marks):
        end = marks[k + 1].start() if k + 1 < len(marks) else len(body)
        chunk = body[mk.end():end]
        chunk = re.split(r"^##\s", chunk, maxsplit=1, flags=re.M)[0]
        out[SPEC_MD_KEYS[mk.group(1)]] = _val(chunk.strip())
    return out


def spec_fields(shot: dict) -> dict[str, str]:
    return {k: _val(shot.get(k)) for k, _ in SPEC_FIELDS if k in shot}


def spec_at(run: Path, sid: str, st: str) -> tuple[dict[str, str] | None, str]:
    """一张审查单审的那一版分镜：先看快照 filming_<场>.json，旧单退回 materials/shots/<场>_<镜>/spec.md。"""
    snap = run / SNAP / f"filming_{sid}.json"
    if snap.is_file():
        sc = json.loads(snap.read_text(encoding="utf-8"))
        shot = next((x for x in sc.get("shots", []) if x.get("id") == st), None)
        return (spec_fields(shot) if shot else None), rel(snap)
    md = run / "materials/shots" / f"{sid}_{st}" / "spec.md"
    if md.is_file():
        return parse_spec_md(md.read_text(encoding="utf-8")), rel(md)
    return None, ""


def _pieces(text: str) -> list[str]:
    return [x.strip() for x in re.split(r"(?<=[。；！？;!?])|\n", text or "") if x and x.strip()]


def text_diff(a: str, b: str, pieces: bool = True) -> list[str]:
    import difflib
    sa, sb = (_pieces(a), _pieces(b)) if pieces else ((a or "").splitlines(), (b or "").splitlines())
    return list(difflib.unified_diff(sa, sb, lineterm="", n=1))[2:]


class Frames:
    """各镜首帧的所有版本：现行 planning/<镜>_first_frame.png ＋ planning/_*/ 下的归档（_r1、_r2、_r1b_old、_v2_old…）。sha 按需算、缓存。"""

    def __init__(self) -> None:
        self._sha: dict[tuple, str] = {}

    def sha(self, f: Path) -> str:
        st = f.stat(); key = (str(f), st.st_mtime_ns, st.st_size)
        if key not in self._sha:
            self._sha[key] = sha(f)
        return self._sha[key]

    def versions(self, ep: Path, sid: str, st: str) -> list[dict]:
        pl = ep / f"scenes/{sid}/shots/{st}/planning"
        files = [pl / f"{st}_first_frame.png"] + sorted(pl.glob(f"_*/{st}_first_frame.png"))
        return [{"file": f, "path": rel(f), "label": "现行" if f.parent == pl else f.parent.name,
                 "mtime": dt.datetime.fromtimestamp(f.stat().st_mtime)} for f in files if f.is_file()]

    def pick(self, vers: list[dict], want_sha: str = "", at: str = "") -> dict | None:
        """按 sha 找那一版；没有 sha 就取「那个时刻已经在的」最新一版（文件修改时间 ≤ 时刻）。"""
        if want_sha:
            return next((v for v in vers if self.sha(v["file"]) == want_sha), None)
        if at:
            t = dt.datetime.fromisoformat(at) + dt.timedelta(seconds=1)
            older = [v for v in vers if v["mtime"] <= t]
            return max(older, key=lambda v: v["mtime"]) if older else None
        return next((v for v in vers if v["label"] == "现行"), None)

    def out(self, v: dict | None, how: str) -> dict | None:
        if not v:
            return None
        return {"path": v["path"], "label": v["label"], "sha256": self.sha(v["file"]),
                "mtime": v["mtime"].isoformat(timespec="seconds"), "mtime_ms": int(v["file"].stat().st_mtime * 1000), "how": how}


def shot_keys(text: str, scenes: list[str]) -> list[str]:
    """问题里的镜头写法（s3_st3、s1_st3→s1_st5、「s1 全场（st3、st4、st5）」、单场单里的 st4）→ 场_镜 列表。"""
    out, cur = [], scenes[0] if len(scenes) == 1 else None
    for m in re.finditer(r"(?<![A-Za-z0-9])(s\d+)(?:_((?:st|g)\d+))?(?![0-9])|(?<![A-Za-z0-9_])(st\d+)(?![0-9])", text or ""):
        if m.group(1):
            cur = m.group(1)
            if m.group(2):
                out.append(f"{cur}_{m.group(2)}")
        elif cur:
            out.append(f"{cur}_{m.group(3)}")
    return _uniq(out)


def find_child(run: Path, data: dict) -> tuple[Path, dict] | None:
    """下一轮：checklist 的 child，或同一 reviews 目录里 parent 指向本单的那张。"""
    if data.get("child") and (REPO / data["child"] / CHECKLIST).is_file():
        c = REPO / data["child"]
        return c, load(c)
    me = rel(run)
    for f in sorted(run.parent.glob(f"*/{CHECKLIST}")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if d.get("parent") == me:
            return f.parent, d
    return None


def _bigrams(t: str) -> set[str]:
    t = _norm(t)
    return {t[k:k + 2] for k in range(len(t) - 1)}


def solutions_from_changes(issues: list[dict], changes: str, scenes: list[str]) -> int:
    """旧单（没有用 issues/fix 登记方案）：从下一轮 changes.md 的「- 法则 · 镜头 · 发现 → 处理」行配方案。同一法则同一镜头有多行时取和问题文字最像的一行。"""
    lines, law = [], ""
    for ln in changes.splitlines():
        h = re.match(r"^#{2,4}\s*([A-Za-z_]+)\s*$", ln.strip())
        if h:
            law = h.group(1); continue
        if ln.lstrip().startswith("- ") and "→" in ln:
            body = ln.strip()[2:]
            head = body.split("·", 1)[0].strip()
            lines.append({"law": head if re.fullmatch(r"[A-Za-z_]+", head) else law, "keys": shot_keys(body.split("→", 1)[0], scenes),
                          "left": body.split("→", 1)[0], "right": body.split("→", 1)[1].strip(), "text": body})
    n = 0
    for i in issues:
        keys = set(i.get("keys") or [])
        cands = [x for x in lines if x["law"] == i["law"] and keys & set(x["keys"])]
        if not cands:
            continue
        ref = _bigrams(i["problem"] + " ".join(i.get("evidence") or []))
        best = max(cands, key=lambda x: len(_bigrams(x["left"]) & ref))
        i.update(solution=best["right"], status="implemented", solution_source="changes.md", solution_line=best["text"])
        n += 1
    return n


def _subpart(s: str) -> str:
    """「连续性·站位（…）」→「站位（…）」：法则名本身不算子类，比子类要去掉。"""
    return s.split("·", 1)[1] if "·" in s else s


def same_sub(i: dict, dim: str, sub: str, r: dict, x: dict) -> bool:
    """下一轮问题表的一行和这条问题是不是同一个子类：维度编号相同、子类文字互相包含、行里写了这条的编号，或子类头一个词相同。"""
    if dim and dim in dims_in(r["sub"], x.get("rubric") or []):
        return True
    if i.get("id") and i.get("solution_source") != "changes.md" and re.search(rf"(?<![A-Za-z0-9]){re.escape(i['id'])}(?!\d)", r["raw"]):
        return True
    a, b = _norm(_subpart(i["dimension"])), _norm(_subpart(r["sub"]))
    if not a or not b:
        return False
    if a in b or b in a:
        return True
    ida, idb = re.match(r"[a-z]+\d+", a), re.match(r"[a-z]+\d+", b)
    if ida and idb:
        return ida.group(0) == idb.group(0)
    ha, hb = re.split(r"[·/（(、，,]", a)[0], re.split(r"[·/（(、，,]", b)[0]
    return len(ha) >= 2 and ha == hb


def verify_issue(i: dict, child: tuple[Path, dict] | None, cache: dict) -> dict:
    """下一轮有没有复核这条、结论如何：同一类审稿项的问题表里还有没有同镜头同子类的行、维度最终分、R 一行提到这条编号时怎么说。"""
    if not child:
        return {"status": "待复核", "how": ["还没开下一轮"]}
    cdir, cdata = child
    scenes = {k.split("_")[0] for k in i.get("keys") or []}
    items = [x for x in cdata["items"] if x.get("law") == i["law"] and (not scenes or not x.get("scope") or scenes & set(x["scope"]))]
    if not items:
        return {"status": "待复核", "run": rel(cdir), "how": [f"下一轮没有「{i['category']}」这一类审稿人"]}
    if any(x.get("status") != "done" for x in items):
        return {"status": "待复核", "run": rel(cdir), "how": ["下一轮这一类还没审完"]}
    how, still, rows_out = [], False, []
    keys = set(i.get("keys") or [])
    dim = i["dimension"].split()[0] if i["key"].startswith("dim:") else ""
    sub = _norm(i["dimension"])
    for x in items:
        if x["id"] not in cache:
            if "slots" in x:
                rows = x.get("finding_rows", [])
            else:
                rp = cdir / x["report"]
                rows = parse_rows(rp.read_text(encoding="utf-8")) if rp.is_file() else []
            rtexts = []
            for who, rep in ([(k, cdir / sl["report"]) for k, sl in x["slots"].items()] if "slots" in x else [("", cdir / x["report"])]):
                if rep.is_file():
                    t = rep.read_text(encoding="utf-8")
                    m = re.search(r"^\s*(?:[-*+]|\d+\.)?\s*[*_`]*R(?![A-Za-z0-9])[*_`]*.*$", section(t, "评分表") or section(t, "必查项"), re.M)
                    if m:
                        rtexts.append((who, m.group(0).strip()))
            cache[x["id"]] = (rows, rtexts)
        rows, rtexts = cache[x["id"]]
        other = []                                    # 同镜头、别的子类、还要改的行：R ✗ 时用来判断这条是不是还没改好
        for r in rows:
            rk = set(shot_keys(r["shot"], x.get("scope") or cdata.get("scenes") or []))
            if not keys & rk:
                continue
            if not same_sub(i, dim, sub, r, x):
                if r["sev"] in ("重出", "可剪"):
                    other.append(r)
                continue
            rows_out.append(r["raw"])
            if r["sev"] in ("重出", "可剪", "存疑"):
                still = True
                how.append(f"{x['id']} 问题表仍有：{r['sev']} · {r['sub']} · {r['evidence'][:60]}")
            else:
                how.append(f"{x['id']} 只剩记录级：{r['sub']} · {r['evidence'][:60]}")
        if dim and x.get("final_scores", {}).get(dim) is not None:
            f = x["final_scores"][dim]
            how.append(f"{x['id']} {dim} 最终 {f} 分")
            still = still or f <= 1
        mark = (x.get("must_result") or {}).get("R")
        if mark:
            how.append(f"{x['id']} R {mark}" + ("（这一类有上一轮的问题没改好）" if mark == "✗" else ""))
        if mark == "✗" and other:
            still = True
            how += [f"{x['id']} 同镜头仍有：{r['sev']} · {r['sub']} · {r['evidence'][:60]}" for r in other[:3]]
        if i.get("id") and i.get("solution_source") != "changes.md":
            for who, t in rtexts:
                mm = re.search(rf"(?<![A-Za-z0-9]){re.escape(i['id'])}(?!\d)", t)
                if mm:
                    snip = t[mm.start():mm.start() + 50]
                    how.append(f"{x['id']}{'__' + who if who else ''} R：{snip}")
                    still = still or bool(re.search(r"✗|未改|没改|仍|还没|没有改", snip))
    return {"status": "复核仍有问题" if still else "已复核通过", "run": rel(cdir), "how": _uniq(how) or ["这一类审完，没有同镜头同子类的问题行"],
            "rows": _uniq(rows_out)}


def build_corrections(run: Path, data: dict) -> dict:
    ep = REPO / data["target"]
    lay = layout(ep)
    scenes = data.get("scenes") or lay["order"]
    child = find_child(run, data)
    fr = Frames()
    source = "issues.json"
    issues = [dict(x) for x in load_issues(run)]
    changes_md = ""
    if child and (child[0] / "changes.md").is_file():
        changes_md = rel(child[0] / "changes.md")
    if not issues:
        source = "推导（问题表）＋下一轮 changes.md"
        issues = derive_issues(run, data) if all(x.get("status") == "done" for x in data["items"]) else []
        for k, i in enumerate(issues, 1):
            i.update(id=f"I{k}", status="open", solution="", reason="", history=[])
    for i in issues:
        i["keys"] = shot_keys(" ".join(i.get("shots") or []), scenes)
    if source != "issues.json" and changes_md:
        solutions_from_changes(issues, (REPO / changes_md).read_text(encoding="utf-8"), scenes)
    snap_frames = json.loads((run / SNAP / "first_frames.json").read_text(encoding="utf-8")) if (run / SNAP / "first_frames.json").is_file() else {}
    child_frames = (json.loads((child[0] / SNAP / "first_frames.json").read_text(encoding="utf-8"))
                    if child and (child[0] / SNAP / "first_frames.json").is_file() else {})
    shots = []
    for sid in scenes:
        cur_scene = lay["scenes"].get(sid) or {}
        before_scene = (json.loads((run / SNAP / f"filming_{sid}.json").read_text(encoding="utf-8"))
                        if (run / SNAP / f"filming_{sid}.json").is_file() else {})
        reviewed = sorted((p.parent.name.split("_", 1)[1] for p in (run / "materials/shots").glob(f"{sid}_*/spec.md")),
                          key=lambda x: int(re.sub(r"\D", "", x) or 0))
        ids = _uniq([x["id"] for x in before_scene.get("shots", [])] + reviewed + [x["id"] for x in cur_scene.get("shots", [])])
        for st in ids:
            key = f"{sid}_{st}"
            # 首帧
            vers = fr.versions(ep, sid, st)
            b = fr.pick(vers, want_sha=(snap_frames.get(key) or {}).get("sha256", "")) if key in snap_frames else fr.pick(vers, at=data["created_at"])
            b_how = "审查时的快照（sha 对上）" if key in snap_frames else f"审查开始（{data['created_at'].replace('T', ' ')}）时已在的那一版"
            if child:
                af = fr.pick(vers, want_sha=(child_frames.get(key) or {}).get("sha256", "")) if key in child_frames else fr.pick(vers, at=child[1]["created_at"])
                a_how = f"下一轮（{child[0].name}）审的那一版"
            else:
                af = fr.pick(vers); a_how = "现行首帧"
            frame = {"before": fr.out(b, b_how), "after": fr.out(af, a_how)}
            if key in snap_frames and not b:
                frame["note"] = "审查时那张首帧没有留档（sha 对不上任何现存版本）"
            frame["changed"] = bool(frame["before"] and frame["after"] and frame["before"]["sha256"] != frame["after"]["sha256"])
            # 分镜文字
            bs, bsrc = spec_at(run, sid, st)
            if child:
                cs, csrc = spec_at(child[0], sid, st)
            else:
                cs, csrc = None, ""
            if cs is None:
                cur = next((x for x in cur_scene.get("shots", []) if x.get("id") == st), None)
                cs, csrc = (spec_fields(cur) if cur else None), rel(ep / "filming.json") + f"#{sid}"
            fields = []
            if bs is not None or cs is not None:
                bs, cs2 = bs or {}, cs or {}
                # 旧单的 spec.md 只有时长、出场和六行规格：只比这些字段，免得把 props / extras 当成新加的
                compare = [k for k, _ in SPEC_FIELDS if k in bs or k in cs2] if not bsrc.endswith("spec.md") and not csrc.endswith("spec.md") else \
                    [k for k, _ in SPEC_FIELDS if k in bs and k in cs2] if bs and cs2 else [k for k, _ in SPEC_FIELDS if k in bs or k in cs2]
                for k, name in SPEC_FIELDS:
                    if k not in compare:
                        continue
                    va, vb = bs.get(k, ""), cs2.get(k, "")
                    if va != vb:
                        fields.append({"field": k, "name": name, "before": va, "after": vb, "diff": text_diff(va, vb)})
            spec = {"before_source": bsrc, "after_source": csrc, "changed": bool(fields), "fields": fields,
                    **({"removed": True} if cs is None and bs is not None else {}), **({"added": True} if bs is None and cs is not None else {})}
            # prompt（只有新单有快照）
            prompt = None
            pb = run / SNAP / "prompts" / f"{key}.txt"
            if pb.is_file():
                pa = (child[0] / SNAP / "prompts" / f"{key}.txt") if child else None
                pa = pa if pa and pa.is_file() else ep / f"scenes/{sid}/shots/{st}/资料包/prompt.txt"
                ta, tb = pb.read_text(encoding="utf-8"), pa.read_text(encoding="utf-8") if pa.is_file() else ""
                prompt = {"before_source": rel(pb), "after_source": rel(pa) if pa.is_file() else "", "changed": ta != tb,
                          "diff": text_diff(ta, tb, pieces=False) if ta != tb else []}
            shots.append({"key": key, "scene": sid, "shot": st, "frame": frame, "spec": spec, **({"prompt": prompt} if prompt else {}),
                          "issues": [i["id"] for i in issues if key in i["keys"] and (i.get("solution") or i.get("status") != "open")]})
    by_key = {x["key"]: x for x in shots}
    cache: dict = {}
    corrections = []
    for i in issues:
        if not (i.get("solution") or "").strip():
            continue
        hist = i.get("history") or []
        frames_manual = i.get("frames") or []
        for f in frames_manual:
            for k in i["keys"]:
                if k in by_key:
                    by_key[k].setdefault("manual_frames", [])
                    if f not in by_key[k]["manual_frames"]:
                        by_key[k]["manual_frames"].append(f)
        pending = [k for k in i["keys"] if k in by_key and "首帧" in (i.get("solution") or "") and not by_key[k]["frame"]["changed"]]
        corrections.append({
            "id": i["id"], "level": i["level"], "law": i["law"], "category": i["category"], "item": i["item"], "dimension": i["dimension"],
            "shots": i.get("shots") or [], "keys": i["keys"], "scenes": _uniq([k.split("_")[0] for k in i["keys"]]) or
            next((x.get("scope", []) for x in data["items"] if x["id"] == i["item"]), []),
            "problem": re.sub(r"\s+", " ", i["problem"])[:160], "fix": i.get("fix", ""), "solution": i["solution"], "status": i["status"],
            "reason": i.get("reason", ""), "cost": i.get("cost", ""), "solution_source": i.get("solution_source", "fix"),
            **({"solution_line": i["solution_line"]} if i.get("solution_line") else {}),
            "history": [{"at": h.get("at", ""), "status": h.get("status", ""), "by": h.get("by", ""), **({"files": h["files"]} if h.get("files") else {})}
                        for h in hist],
            "files": i.get("files") or [], "frames": frames_manual,
            **({"frame_pending": pending} if pending else {}),
            "verification": verify_issue(i, child, cache)})
    def count(xs, key, names):
        return {n: sum(1 for x in xs if x[key] == n) for n in names}
    summary = {"issues": len(issues), "corrections": len(corrections), "by_level": count(corrections, "level", LEVELS),
               "by_status": count(corrections, "status", FIX_STATUS),
               "by_verification": {v: sum(1 for c in corrections if c["verification"]["status"] == v) for v in VERIFY},
               "shots": len(shots), "frames_changed": sum(x["frame"]["changed"] for x in shots), "specs_changed": sum(x["spec"]["changed"] for x in shots),
               "shots_touched": sum(1 for x in shots if x["frame"]["changed"] or x["spec"]["changed"] or x["issues"])}
    return {"run": data["id"], "dir": rel(run), "title": data.get("title", ""), "loop": data.get("loop", 1), "parent": data.get("parent", ""),
            "child": rel(child[0]) if child else "", "child_state": child[1].get("state", "") if child else "",
            "issues_source": source, "changes_md": changes_md, "has_snapshot": (run / SNAP).is_dir(),
            "summary": summary, "corrections": corrections, "shots": shots}


def corrections_md(doc: dict) -> str:
    s = doc["summary"]
    L = [f"# 修复记录：{doc['title']}", "",
         f"本轮审查单：`{doc['dir']}`" + (f"；下一轮：`{doc['child']}`（{doc['child_state']}）" if doc["child"] else "；还没开下一轮"), "",
         f"问题来源：{doc['issues_source']}" + (f"；方案来自 `{doc['changes_md']}`" if doc["issues_source"] != "issues.json" and doc["changes_md"] else ""), "",
         f"有方案的问题 {s['corrections']} / {s['issues']} 条；"
         + "，".join(f"{LEVEL_NAME[l]} {s['by_level'][l]}" for l in LEVELS) + "；"
         + "，".join(f"{v} {s['by_verification'][v]}" for v in VERIFY)
         + f"；首帧换了 {s['frames_changed']} 镜，分镜文字改了 {s['specs_changed']} 镜。", ""]
    by_id = {c["id"]: c for c in doc["corrections"]}
    for sid in _uniq([x["scene"] for x in doc["shots"]]):
        rows = [x for x in doc["shots"] if x["scene"] == sid and (x["frame"]["changed"] or x["spec"]["changed"] or x["issues"])]
        loose = [c for c in doc["corrections"] if not c["keys"] and sid in c["scenes"]]
        if not rows and not loose:
            continue
        L += [f"## {sid}", ""]
        for x in rows:
            fb, fa = x["frame"]["before"], x["frame"]["after"]
            L += [f"### {x['key']}", ""]
            if x["frame"]["changed"]:
                L.append(f"- 首帧：`{fb['path']}`（{fb['label']}）→ `{fa['path']}`（{fa['label']}）")
            elif fb:
                L.append(f"- 首帧没换（`{fb['path']}`）")
            for c in [by_id[k] for k in x["issues"] if k in by_id]:
                L.append(f"- **{c['id']}** [{LEVEL_NAME[c['level']]}·{c['status']}·{c['verification']['status']}] {c['category']}·{c['dimension']}：{c['problem'][:80]}")
                L.append(f"  - 方案：{c['solution']}")
                if c["files"]:
                    L.append("  - 改了：" + "、".join(f"`{f}`" for f in c["files"]))
            for f in x["spec"]["fields"]:
                L += [f"- 分镜「{f['name']}」改了：", "", "```diff", *f["diff"], "```", ""]
            L.append("")
        for c in loose:
            L += [f"### {sid} 整场 / 未指明镜头", "", f"- **{c['id']}** [{LEVEL_NAME[c['level']]}·{c['status']}·{c['verification']['status']}] "
                  f"{c['category']}·{c['dimension']}：{c['problem'][:80]}", f"  - 方案：{c['solution']}", ""]
    return "\n".join(L) + "\n"


def cmd_corrections(a: argparse.Namespace) -> int:
    run = resolve(a.run); data = load(run)
    doc = build_corrections(run, data)
    old = json.loads((run / CORR_JSON).read_text(encoding="utf-8")) if (run / CORR_JSON).is_file() else {}
    old_at = old.pop("generated_at", "")
    doc_at = old_at if old_at and old == doc else now()       # 内容没变就不改时间：重跑幂等
    (run / CORR_JSON).write_text(json.dumps({"generated_at": doc_at, **doc}, ensure_ascii=False, indent=1), encoding="utf-8")
    (run / CORR_MD).write_text(corrections_md(doc), encoding="utf-8")
    if old_at != doc_at:
        data["log"].append({"at": now(), "event": "corrections", "note": f"修复页：{doc['summary']['corrections']} 条方案、首帧换了 {doc['summary']['frames_changed']} 镜"})
        data["corrections"] = CORR_JSON
        save(run, data)
    s = doc["summary"]
    print(f"修复页：{rel(run / CORR_MD)}（有方案 {s['corrections']}/{s['issues']} 条；首帧换了 {s['frames_changed']} 镜、分镜改了 {s['specs_changed']} 镜；"
          + "，".join(f"{v} {s['by_verification'][v]}" for v in VERIFY) + "）" + ("" if old_at != doc_at else "（内容没变）"))
    return 0


def scene_of(key: str) -> str | None:
    m = re.search(r"_(s\d+)_", key + "_")
    return m.group(1) if m else None


def can_submit(ep: Path, keys: list[str]) -> tuple[bool, str]:
    """出片闸门：每个镜头所在场，覆盖它的最新一张已收轮出片前（gate 阶段）审查单，要由用户在出片时确认过、材料未变。
    每轮审查本身不等用户 review（用户 2026-11-08）；用户的确认只在这里、出片时。"""
    root = reviews_dir(ep)
    runs = []
    for p in sorted(root.glob(f"{ep.name}_*/{CHECKLIST}")):
        d = json.loads(p.read_text(encoding="utf-8"))
        if d.get("gate_stage") and d.get("state") in CLOSED:
            runs.append((p.parent, d))
    missing = []
    for k in keys:
        sid = scene_of(k)
        cover = sorted([(p, d) for p, d in runs if sid in d.get("scenes", [])], key=lambda x: (x[1].get("concluded_at") or x[1].get("created_at", "")))
        if not cover:
            missing.append(f"{k}：没有覆盖 {sid} 的已收轮出片前审查单"); continue
        p, d = cover[-1]
        if d.get("state") != "用户已确认出片":
            v = (d.get("verdict") or {}).get("result") or "—"
            missing.append(f"{k}：覆盖 {sid} 的最新一张审查单 {p.name} 已收轮（结论：{v}），出片要用户在对话里确认后 confirm --quote")
        elif stale_files(d):
            missing.append(f"{k}：覆盖 {sid} 的审查单确认后材料又变了，要重审")
    if missing:
        return False, "出片前审查没过闸（review_run.py）：\n  " + "\n  ".join(missing) + \
            f"\n  流程：python tools/review_run.py new {rel(ep)} --stage pregen → 双审打分 → 修复 → 下一轮（最多 3 轮）→ conclude → 出片时用户同意后 confirm"
    return True, "出片前审查已确认"


def cmd_can_submit(a: argparse.Namespace) -> int:
    ok, msg = can_submit(resolve(a.target), a.keys)
    print(msg)
    return 0 if ok else 1


def cmd_list(a: argparse.Namespace) -> int:
    p = resolve(a.target)
    root = p / "reviews" if (p / "reviews").is_dir() else reviews_dir(p)
    ep = None if (p / "reviews").is_dir() else p.name
    rows = []
    for q in sorted(root.glob(f"*/{CHECKLIST}")):
        d = json.loads(q.read_text(encoding="utf-8"))
        if ep and d.get("episode") != ep:
            continue
        done = sum(x["status"] == "done" for x in d["items"])
        rows.append(f"{d['id']:<40} {d['state']:<8} 第{d.get('loop', 1)}轮 {done}/{len(d['items'])}  {d['title']}")
    print("\n".join(rows) if rows else "（没有审查单）")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new"); n.add_argument("target"); n.add_argument("--stage", default="")
    n.add_argument("--scenes", default=""); n.add_argument("--title", default=""); n.add_argument("--known", default="")
    n.add_argument("--author", default="Claude Code"); n.add_argument("--no-materials", action="store_true")
    n.add_argument("--after", default="", help="上一轮审查单目录：开下一轮（最多 roster.max_loops 轮）")
    n.add_argument("--changes", default="", help="--after 时必填：这轮之后改了什么（文件路径或文字）")
    t = sub.add_parser("tick"); t.add_argument("run"); t.add_argument("item"); t.add_argument("--report", required=True)
    t.add_argument("--by", required=True); t.add_argument("--note", default="", help="可选备注（如补登说明），写进清单并在管理站显示")
    t.add_argument("--slot", default="", help="v5：a（Claude）| b（Codex）")
    t.add_argument("--attest-log", default="", help="Codex 审稿人跑不了 python 时，凭它的 codex exec 运行日志代为登记")
    f = sub.add_parser("fail"); f.add_argument("run"); f.add_argument("item"); f.add_argument("--note", required=True)
    f.add_argument("--slot", default="", help="v5：a | b | judge")
    ad = sub.add_parser("adjudicate"); ad.add_argument("run"); ad.add_argument("item"); ad.add_argument("--report", required=True)
    ad.add_argument("--by", required=True)
    iss = sub.add_parser("issues"); iss.add_argument("run")
    fx = sub.add_parser("fix"); fx.add_argument("run"); fx.add_argument("issue"); fx.add_argument("--solution", required=True)
    fx.add_argument("--status", default="planned", choices=["planned", "implemented", "wontfix"]); fx.add_argument("--reason", default="")
    fx.add_argument("--file", action="append", help="这次修复改了的文件（可多次）"); fx.add_argument("--by", default="", help="谁改的")
    fx.add_argument("--before", action="append", help="旧图（与 --after 成对，可多次）"); fx.add_argument("--after", action="append", help="新图")
    co = sub.add_parser("corrections"); co.add_argument("run")
    mg = sub.add_parser("migrate"); mg.add_argument("target", nargs="?", default="")
    for name in ("status", "gate"):
        s = sub.add_parser(name); s.add_argument("run")
    c = sub.add_parser("conclude"); c.add_argument("run"); c.add_argument("--verdict", default=""); c.add_argument("--note", default="")
    c.add_argument("--accept-fixes", action="store_true", help="最后一轮：修复落地后按修复后的材料收轮（严重与主要问题须都已登记处理），修复由用户出片前审")
    cf = sub.add_parser("confirm"); cf.add_argument("run"); cf.add_argument("--quote", required=True)
    dp = sub.add_parser("dispatch"); dp.add_argument("run"); dp.add_argument("item")
    for flag in ("--runner", "--model", "--prompt-file", "--reply-file", "--skills", "--context", "--note", "--at", "--slot"):
        dp.add_argument(flag, default="")
    ds = sub.add_parser("drop-slot"); ds.add_argument("run"); ds.add_argument("--slot", default="b"); ds.add_argument("--note", required=True)
    li = sub.add_parser("list"); li.add_argument("target")
    cs = sub.add_parser("can-submit"); cs.add_argument("target"); cs.add_argument("keys", nargs="+")
    a = ap.parse_args(argv)
    _call = lambda: {"new": cmd_new, "tick": cmd_tick, "fail": cmd_fail, "conclude": cmd_conclude, "confirm": cmd_confirm,
            "list": cmd_list, "can-submit": cmd_can_submit, "dispatch": cmd_dispatch, "drop-slot": cmd_drop_slot, "adjudicate": cmd_adjudicate,
            "issues": cmd_issues, "fix": cmd_fix, "corrections": cmd_corrections, "migrate": cmd_migrate}.get(a.cmd, lambda x: cmd_status(x, gate=a.cmd == "gate"))(a)
    _run = getattr(a, "run", "") or ("" if a.cmd in ("new", "list", "can-submit") else getattr(a, "target", ""))
    if _run and (resolve(_run) / CHECKLIST).is_file():
        with RunLock(resolve(_run)):
            return _call()
    return _call()


if __name__ == "__main__":
    sys.exit(main())
