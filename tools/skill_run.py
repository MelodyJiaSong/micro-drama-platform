# -*- coding: utf-8 -*-
"""技能视频总控：一次后台启动，把一条（或几条）技能从关键帧一路跑到出片后闸门，只在真正要人判断时停下。

    python tools/skill_run.py <剧> k421 k423 [--auto-approve] [--until pre|submit|post]
    python tools/skill_run.py <剧> --status k421 k423        # 只看每条停在哪一步、为什么

为什么要有它（dota_yingxiong follow-up 282）
------------------------------------------
用户：「为什么每一步都要我来询问情况，你才继续做」。原因是代理把十来步工具一段段手动接：
出图 → 看图 → 资料包 → 机检 → 审稿 → 闸门 → 提交 → 收片 → 机检 → 审稿 → 闸门，每段跑完都要代理被唤醒才接下一段，
四条技能排队串行，会话一断就全停。本工具把这些步骤串成一条可续跑的流水线，几条技能并行，每步先看产物与结论是否已对得上
（对得上就跳过），所以中断后原样再跑一次即可续上。

每条技能的步骤（全部复用现有工具，不另立规则）
------------------------------------------
1. 关键帧：「视频参考」里 `*_start` / `*_peak` 的图不存在、且 `planning/<图名>.txt`（prompt）与 `planning/<图名>.refs`
   （每行一张参考图，仓库相对路径）都在，就经 `tools/codex_image.py` 出图（它先记请求日志）。只对**明确的网络失败或超时且
   确认没出图**的情况重试，最多 3 次；其他失败停下。出图全局串行（订阅额度与网络都扛不住并发）。
   **出完的图代理仍要看**：本工具不替代看图，`--until pre` 可以停在出片前审稿之后先看图。
2. 资料包：`skill_pack.sync`。
3. 出片前闸门：`qc_pre.json` 缺失或与资料包 sha 对不上 → `qc_pre.py machine` + `qc_review.py --pre`；然后 `qc_pre.gate`。
   不过就停下，把不过的检查分成「改规格 / 改图能解决」与「画面无法验证类（体型换算、远景细节）」两组列出——后一组改图
   也难解决，要**当场**交用户决定放行还是重画（follow-up 282：别拖到第 3 轮才问）。审稿人现在对看不清的项记「审不了·看不清」
   （放行、列为待人看，follow-up 354），这一组应当少见。
   用户已明确放行、且整类都在放行范围内的检查（如画面无法换算真实尺寸的 `keyframe.scale`），可用
   `--allow 检查id=用户原话 --followup NNN` 传进来：重审后照样按用户原话记 `qc.py override`，不再停下问第二次。
4. 时间轴：指纹没审过时，有 `--auto-approve`（剧 README 记有用户授权免等，如 dota 2026-10-24）就 `approve` 留痕，否则停下等用户。
5. 出片：已有同 prompt 的出片就跳过；有挂起的提交就补收；否则日志闸门通过后提交 720p 正式条（`--stage final --no-draft`）并等结果。
6. 出片后：`motion_check`（动作段取规格里起势结束到收势开始）自动记 `video.slowmo`；`qc_review`（`--when` 按规格里出现的
   眩晕 / 减速 / 一镜到底自动加）；`qc.py gate`。拼图仍要代理看过再写 `review.md`。

每条技能的进度写在 `{技能目录}/run_state.json`，全程日志在 `.audit/adhoc_agents/{日期}/skill_run/`。
有 cc-connect 时，每条出片后立刻把压缩预览（zip）与拼图发给用户，每条技能停下或完成也推一条消息（尽力而为，失败不影响流程）。
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import re
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "tools"))
from tools import skill_pack  # noqa: E402
import qc  # noqa: E402
import qc_pre  # noqa: E402

PY = sys.executable
IMG_LOCK = threading.Lock()
LOG_LOCK = threading.Lock()
NET_SIGNS = ("network error", "10054", "timed_out\": true", "stream disconnected")
UNVERIFIABLE = {"keyframe.scale"}                      # 画面无法换算真实尺寸：改图也难解决，要用户定
STATE = "run_state.json"
WHEN_WORDS = ("眩晕", "减速", "一镜到底")


class Stop(Exception):
    """这条技能要停下：need = user（用户判断）/ agent（代理改规格、改图后再跑）/ error。"""

    def __init__(self, need: str, msg: str):
        super().__init__(msg)
        self.need = need


def audit_dir() -> Path:
    d = REPO / ".audit" / "adhoc_agents" / datetime.now().strftime("%Y-%m-%d") / "skill_run"
    d.mkdir(parents=True, exist_ok=True)
    return d


def log(sd: Path, msg: str) -> None:
    line = "%s %s %s" % (datetime.now().strftime("%H:%M:%S"), sd.name, msg)
    with LOG_LOCK:
        print(line, flush=True)
        with (audit_dir() / "run.log").open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def save_state(sd: Path, step: str, status: str, detail: str = "") -> None:
    (sd / STATE).write_text(json.dumps({"step": step, "status": status, "detail": detail,
                                        "updated": datetime.now().isoformat(timespec="seconds")},
                                       ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(sd: Path, args: list[str], name: str, timeout: int = 7200) -> subprocess.CompletedProcess:
    r = subprocess.run([PY, *args], cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=timeout)
    with (audit_dir() / ("%s_%s.log" % (sd.name, name))).open("a", encoding="utf-8") as fh:
        fh.write("$ %s\n%s\n%s\n[exit %s]\n" % (" ".join(args), r.stdout, r.stderr, r.returncode))
    return r


def send_preview(sd: Path, rd: Path, note: str) -> None:
    """出片后立刻把预览发给用户（follow-up 295：「技能一新的视频出来了么？为什么不发我」）。
    960 宽 crf30 压缩、打 zip（飞书不收直接发的 mp4），连同拼图一起经 cc-connect 发；失败只记日志。"""
    exe = shutil.which("cc-connect")
    clip = next(rd.glob("*_clip.mp4"), None)
    if not exe or not clip:
        return
    import zipfile
    out = audit_dir() / "send"
    out.mkdir(exist_ok=True)
    mp4 = out / ("%s_%s.mp4" % (sd.name.split("_")[0], rd.name[-8:]))
    try:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(clip), "-vf", "scale=960:-2", "-c:v", "libx264", "-crf", "30",
                        "-preset", "veryfast", "-c:a", "aac", "-b:a", "96k", str(mp4)], check=True, timeout=600)
        zp = mp4.with_suffix(".zip")
        with zipfile.ZipFile(zp, "w") as z:
            z.write(mp4, mp4.name)
        r = subprocess.run([exe, "send", "--file", str(zp), "--message", "%s 新出片 %s：%s（解压后是 mp4）" % (sd.name, rd.name[-8:], note)],
                           capture_output=True, text=True, timeout=180)
        sheet = rd / "sheet_4fps.jpg"
        if sheet.exists():
            subprocess.run([exe, "send", "--image", str(sheet)], capture_output=True, timeout=180)
        log(sd, "预览已发用户" if r.returncode == 0 else "预览发送失败：%s" % (r.stdout + r.stderr)[-200:])
    except Exception as e:
        log(sd, "预览发送异常：%r" % e)


def notify(text: str) -> None:
    exe = shutil.which("cc-connect")
    if not exe:
        return
    try:
        subprocess.run([exe, "send", "--message", text], capture_output=True, timeout=30)
    except Exception:
        pass


# ── 1 关键帧 ──────────────────────────────────────────────

def keyframes(drama: str, sd: Path) -> None:
    text = (sd / (sd.name + ".md")).read_text(encoding="utf-8")
    part = text[text.index("## 技能视频 prompt"):] if "## 技能视频 prompt" in text else ""
    m = re.search(r"^视频参考[:：]\s*(.+)$", part, re.M)
    if not m:                                              # skill_pack.shot 遇到缺图会直接退出，这里自己读参考行
        raise Stop("agent", "技能卡还没有「技能视频 prompt」或「视频参考:」行")
    base = skill_pack.settings_dir(drama)
    for item in [x.strip() for x in m.group(1).split(";") if x.strip()]:
        key, rel = [x.strip().strip("`") for x in item.split("=", 1)]
        if not re.search(r"_(start|peak)$", key):
            continue
        img = base / rel
        if img.exists():
            continue
        prompt, refs = img.with_suffix(".txt"), img.with_suffix(".refs")
        if not (prompt.exists() and refs.exists()):
            raise Stop("agent", "缺关键帧 %s，且没有 %s / %s 可以自动出图" % (img.name, prompt.name, refs.name))
        ref_args = [x for line in refs.read_text(encoding="utf-8").splitlines() if line.strip()
                    for x in ("--ref", line.strip())]
        for attempt in range(1, 4):
            with IMG_LOCK:
                log(sd, "出关键帧 %s（第 %d 次）" % (img.name, attempt))
                r = run(sd, ["tools/codex_image.py", "--out", str(img), "--prompt-file", str(prompt), *ref_args],
                        "keyframe", timeout=1800)
            if r.returncode == 0 and img.exists():
                log(sd, "关键帧已出 %s——代理仍要看图" % img.name)
                break
            out = r.stdout + r.stderr
            thread = re.search(r'"thread_id": "([0-9a-f-]+)"', out)
            made = thread and (Path.home() / ".codex" / "generated_images" / thread.group(1)).exists()
            if made or "没有拿到新图" not in out or not any(k in out for k in NET_SIGNS):
                raise Stop("error", "关键帧 %s 出图失败且不能确认没出图，不自动重提：见 %s" % (img.name, audit_dir()))
            log(sd, "网络失败、确认没出图，2 分钟后重试")
            time.sleep(120)
        else:
            raise Stop("error", "关键帧 %s 网络失败 3 次" % img.name)


# ── 3 出片前闸门 ──────────────────────────────────────────

def pre(drama: str, sd: Path, allow: dict[str, str], followup: str) -> None:
    p = sd / qc_pre.RESULT
    data0 = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    reg = qc.registry(qc.drama_dir_of(sd))
    wanted = [c.id for c in reg.values() if c.stage in qc_pre.PRE_STAGES and c.kind == "review"]
    reviewed = all(cid in data0.get("checks", {}) for cid in wanted)
    fresh = data0.get("sha256") == qc_pre.digest(sd) and reviewed   # 审稿上次崩了也要重跑（follow-up 296）
    if not fresh:
        log(sd, "出片前机检 + 多视角审稿")
        run(sd, ["tools/qc_pre.py", "machine", str(sd)], "pre_machine")
        run(sd, ["tools/qc_review.py", str(sd), "--pre"], "pre_review")
    block, soft = qc_pre.gate(sd)
    if block and allow:
        data = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"checks": {}}
        fails = [k for k, v in data.get("checks", {}).items() if v.get("verdict") in ("fail", "审不了")]
        for cid in [k for k in fails if k in allow]:      # 用户放行＝接受这次的结果（follow-up 354：放行分 accept / false_positive）
            run(sd, ["tools/qc.py", "override", str(sd), "--check", cid, "--kind", "accept", "--note", allow[cid]] +
                (["--followup", followup] if followup else []), "override")
            log(sd, "按用户放行记 %s" % cid)
        block, soft = qc_pre.gate(sd)
    if not block:
        log(sd, "出片前闸门通过" + ("（放行 / 软提示 %d 项）" % len(soft) if soft else ""))
        return
    data = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"checks": {}}
    fails = {k: v for k, v in data.get("checks", {}).items() if v.get("verdict") == "fail"}
    if not fails:
        raise Stop("agent", "；".join(block))
    unver = [k for k in fails if k in UNVERIFIABLE]
    fixable = [k for k in fails if k not in UNVERIFIABLE]
    lines = ["出片前闸门不通过"]
    if fixable:
        lines.append("改规格 / 改图能解决：" + "；".join("%s — %s" % (k, fails[k].get("evidence", "")[:160]) for k in fixable))
    if unver:
        lines.append("画面无法验证类（请用户当场决定放行或重画）：" + "、".join(unver))
    raise Stop("agent" if fixable else "user", "\n".join(lines))


# ── 4 时间轴 / 5 出片 ─────────────────────────────────────

def approve(sd: Path, auto: bool) -> None:
    fp = skill_pack.timeline(skill_pack.shot(sd))[1]
    if skill_pack.approved(sd) == fp:
        return
    if not auto:
        raise Stop("user", "时间轴（指纹 %s）待用户审阅：python tools/skill_pack.py timeline <剧> %s"
                   % (fp, sd.name.split("_")[0]))
    skill_pack.approve(sd)
    log(sd, "时间轴按剧级授权记审阅 %s" % fp)


def current_render(sd: Path) -> Path | None:
    pack = sd / qc_pre.PACK / "prompt.txt"
    want = pack.read_text(encoding="utf-8").strip() if pack.exists() else None
    for rd in sorted((sd / "renders").glob("*/"), reverse=True):
        got = rd / "prompt.txt"
        if want and got.exists() and got.read_text(encoding="utf-8").strip() == want and list(rd.glob("*_clip.mp4")):
            return rd
    return None


def render(drama: str, sd: Path) -> Path:
    rd = current_render(sd)
    if rd:
        return rd
    pend = sorted((sd / "renders" / ".pending").glob("*.json"))
    if pend:
        sid = pend[-1].stem
        log(sd, "补收挂起的提交 %s" % sid[:8])
    else:
        why = skill_pack.feedback_gate(sd)
        if why:
            raise Stop("user", why)
        if not skill_pack.log_gate(drama):
            raise Stop("agent", "本会话 follow-up 日志有未收尾条目，先 followup.py done")
        r = skill_pack.submit(drama, sd, "final", no_draft=True)
        if not r:
            raise Stop("error", "提交失败（见上方输出与 request_log）")
        sid = r[0]
        log(sd, "已提交 %s（积分 %s）" % (sid[:8], r[1]))
    code = skill_pack.poll(drama, sd, sid, interval=30, tries=240)
    rd = current_render(sd)
    if code != 0 or not rd:
        raise Stop("error", "出片未落地（poll 返回 %s）：之后再跑本工具会补收" % code)
    return rd


# ── 6 出片后 ──────────────────────────────────────────────

def action_window(sd: Path) -> str:
    beats = skill_pack.timeline(skill_pack.shot(sd))[0]
    start = end = None
    for t, text in beats:
        m = re.match(r"([\d.]+)[–-]([\d.]+)", t)
        if not m:
            continue
        if "起势" in text[:6]:
            start = m.group(2)
        if "收势" in text[:6]:
            end = m.group(1)
    return "%s-%s" % (start or "1.0", end or str(max(skill_pack.duration(skill_pack.shot(sd)) - 2, 2)))


def whens(sd: Path) -> list[str]:
    text = (sd / (sd.name + ".md")).read_text(encoding="utf-8")
    body = text[text.index("## 技能视频 prompt"):] if "## 技能视频 prompt" in text else text
    body = "\n".join(ln for ln in body.splitlines() if not ln.startswith("负面词"))
    found = [w for w in WHEN_WORDS if w in body]
    if "一镜到底" in qc.forced_when(sd) and "一镜到底" not in found:
        found.append("一镜到底")
    return found


def post(sd: Path, rd: Path) -> None:
    data = qc.load_qc(rd)
    clip = next(rd.glob("*_clip.mp4"))
    if "video.slowmo" not in data.get("checks", {}):
        win = action_window(sd)
        r = run(sd, ["tools/motion_check.py", str(clip), "--action", win, "--sheet", str(rd / "sheet_4fps.jpg")], "motion")
        bad = any(k in r.stdout for k in ("慢动作嫌疑", "定格")) and "未见慢动作嫌疑" not in r.stdout
        ev = "motion_check 动作段 %s s：%s（拼图 sheet_4fps.jpg 待代理看过写 review.md）" % (
            win, (r.stdout.strip().splitlines() or ["无输出"])[-1][:200])
        run(sd, ["tools/qc.py", "record", str(rd), "--check", "video.slowmo=%s" % ("fail" if bad else "pass"),
                 "--by", "machine", "--evidence", ev], "record")
        log(sd, "流畅机检 %s（%s）" % ("可疑" if bad else "通过", win))
        if "一镜到底" in whens(sd):                           # 剪切检测同一次 motion_check 输出（follow-up 295）
            cut = next((ln.strip() for ln in r.stdout.splitlines() if "剪切" in ln), "")
            fail = "疑似剪切" in cut
            run(sd, ["tools/qc.py", "record", str(rd), "--check", "video.onetake_cuts=%s" % ("fail" if fail else "pass"),
                     "--by", "machine", "--evidence", "motion_check 剪切检测：%s" % (cut or "无输出")], "record")
            log(sd, "一镜到底机检 %s" % ("有剪切" if fail else "通过"))
    wh = whens(sd)
    reviewed = any(v.get("by") == "review" for v in qc.load_qc(rd).get("checks", {}).values())
    if not reviewed:
        log(sd, "出片后多视角审稿" + ("（%s）" % "、".join(wh) if wh else ""))
        run(sd, ["tools/qc_review.py", str(rd), *[x for w in wh for x in ("--when", w)]], "post_review")
    r = run(sd, ["tools/qc.py", "gate", str(rd), *[x for w in wh for x in ("--when", w)]], "post_gate")
    if r.returncode != 0:
        raise Stop("agent", "出片后闸门不通过：%s\n%s" % (rd.relative_to(REPO).as_posix(), (r.stderr or r.stdout)[-800:]))
    log(sd, "出片后闸门通过：%s" % rd.relative_to(REPO).as_posix())


# ── 编排 ─────────────────────────────────────────────────

def one(drama: str, sd: Path, a: argparse.Namespace) -> tuple[str, str, str]:
    step = "keyframe"
    try:
        save_state(sd, step, "running")
        keyframes(drama, sd)
        step = "sync"
        save_state(sd, step, "running")
        skill_pack.sync(drama, [sd.name.split("_")[0]])
        step = "pre"
        save_state(sd, step, "running")
        pre(drama, sd, a.allow_map, a.followup)
        if a.until == "pre":
            save_state(sd, step, "done", "停在出片前（--until pre）")
            return sd.name, "done", "出片前闸门通过，按 --until pre 停下"
        step = "approve"
        approve(sd, a.auto_approve)
        step = "render"
        save_state(sd, step, "running")
        rd = render(drama, sd)
        if a.until == "submit":
            save_state(sd, step, "done", rd.relative_to(REPO).as_posix())
            return sd.name, "done", "已出片 %s" % rd.relative_to(REPO).as_posix()
        step = "post"
        save_state(sd, step, "running", rd.relative_to(REPO).as_posix())
        try:
            post(sd, rd)
        except Stop as e:
            send_preview(sd, rd, "出片后自检不通过——" + str(e).splitlines()[0][:80] + "；等你反馈再决定是否重出")
            raise
        send_preview(sd, rd, "出片后自检通过，等你看")
        save_state(sd, "post", "passed", rd.relative_to(REPO).as_posix())
        return sd.name, "passed", "出片后闸门通过：%s（拼图待代理看过写 review.md）" % rd.relative_to(REPO).as_posix()
    except Stop as e:
        save_state(sd, step, "needs_" + e.need, str(e))
        log(sd, "停在 %s（需要 %s）：%s" % (step, e.need, str(e).splitlines()[0]))
        return sd.name, "needs_" + e.need, str(e)
    except Exception as e:                                   # 工具异常：记下来，别的技能继续
        save_state(sd, step, "error", repr(e))
        log(sd, "异常 %s：%r" % (step, e))
        return sd.name, "error", repr(e)


def main(argv: list[str] | None = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("drama")
    ap.add_argument("keys", nargs="+")
    ap.add_argument("--auto-approve", action="store_true", help="剧 README 记有用户授权免等时才用：时间轴照记审阅、不等回复")
    ap.add_argument("--until", choices=("pre", "submit", "post"), default="post")
    ap.add_argument("--status", action="store_true", help="只打印每条停在哪一步")
    ap.add_argument("--allow", action="append", default=[], metavar="检查id=用户原话",
                    help="用户已明确放行的出片前检查（只放整类都在放行范围内的，如 keyframe.scale）；规格改动后重审仍按此放行")
    ap.add_argument("--followup", default="", help="放行记到哪条 follow-up")
    a = ap.parse_args(argv)
    a.allow_map = dict(x.split("=", 1) for x in a.allow)
    dirs = skill_pack.skill_dirs(a.drama, a.keys)
    if not dirs:
        raise SystemExit("找不到技能：%s" % " ".join(a.keys))
    if a.status:
        for sd in dirs:
            st = json.loads((sd / STATE).read_text(encoding="utf-8")) if (sd / STATE).exists() else {}
            print("%-26s %-8s %-14s %s  %s" % (sd.name, st.get("step", "-"), st.get("status", "未跑"),
                                               st.get("updated", ""), st.get("detail", "")[:200]))
        return 0
    with cf.ThreadPoolExecutor(max_workers=len(dirs)) as ex:
        results = list(ex.map(lambda sd: one(a.drama, sd, a), dirs))
    print("\n== 汇总 ==")
    for name, status, detail in results:
        print("%-26s %-12s %s" % (name, status, detail))
    notify("技能总控 %s：" % a.drama + "；".join("%s %s" % (n, s) for n, s, _ in results))
    return 0 if all(s in ("passed", "done") for _, s, _ in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
