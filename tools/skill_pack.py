# -*- coding: utf-8 -*-
"""技能视频资料包与出片：每个技能卡一个 `资料包/`，格式与镜头资料包相同（`tools/shot_pack.py`），出片走同一 Dreamina 入口。

技能卡在 `ai_videos/{剧}/2_世界观人设/characters/[{阵营分组}/]{英雄}/skills/{目录}/{目录}.md`（dota_yingxiong follow-up 010 / 025），
或按职业共用的 `2_世界观人设/classes/{职业}/skills/{目录}/{目录}.md`（shengji_zhilu follow-up 108），
卡里 `## 技能视频 prompt` 一节写：
    视频参考: key=相对 2_世界观人设 的路径; key=…        （上传顺序；.png/.jpg 图片，.mp3/.wav 音频，.mp4 视频）
    ```text
    {目录}_clip
    时长：10秒
    参考：`key=>@`、…        （与「视频参考」同序；资料包里填成 @图片N / @音频N）
    …
    ```

    python tools/skill_pack.py sync   <剧> [技能键 …]     # 建 / 更新资料包
    python tools/skill_pack.py cmd    <剧> <技能键>        # 只打印提交命令
    python tools/skill_pack.py timeline <剧> <技能键 …>   # 打印时间轴审阅表与指纹，先交用户 review
    python tools/skill_pack.py approve  <剧> <技能键 …>   # 用户在对话里认可时间轴表后，才在卡里记「时间轴审阅」行
    python tools/skill_pack.py submit <剧> <技能键 …> [--stage draft|final] [--no-draft]   # 提交并等结果（会扣积分，只在用户决定生成后执行）
    python tools/skill_pack.py poll   <剧> <技能键> <submit_id>                # 补收
    python tools/skill_pack.py feedback <剧> <技能键> "用户原话"            # 记用户对上一条出片的反馈（剧级策略要求时，没有就不许再提交）

条目录 ＝ `{技能目录}/{drafts|renders}/{YYYYMMDD-HHMMSS}_{submit_id 前 8 位}/`：`{目录}_clip.mp4`、`generation.json`、`prompt.txt`。
生成永远人点：submit 只在用户明确要出片后运行。
时间轴先审（必要流程，用户 2026-10-24）：每条技能视频出片前，先把时间轴表（timeline）交给用户 review，用户认可后 approve；
submit 只接受与当前时间轴指纹一致的审阅记录，时间轴或时长一改就要重审。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from tools import shot_pack  # noqa: E402
from tools import shot_take  # noqa: E402
from tools import props_lib  # noqa: E402
from projects.ai_video_management.libs.common.asset_group import character_dirs  # noqa: E402

KIND = {".png": "image", ".jpg": "image", ".jpeg": "image", ".mp3": "audio", ".wav": "audio", ".mp4": "video"}
ROLE = {"image": "参考图", "audio": "声音参考", "video": "参考视频"}
STAGE_DIR = {"draft": "drafts", "final": "renders"}


def settings_dir(drama: str) -> Path:
    return REPO / "ai_videos" / drama / "2_世界观人设"


def skill_dirs(drama: str, keys: list[str]) -> list[Path]:
    out = []
    mds = [md for card in character_dirs(settings_dir(drama) / "characters") for md in card.glob("skills/k*/k*.md")]
    mds += (settings_dir(drama) / "classes").glob("*/skills/k*/k*.md")   # 按职业共用的技能（shengji_zhilu follow-up 108）
    for md in sorted(mds, key=lambda md: (md.parents[2].name, md.parent.name)):
        if md.stem == md.parent.name and (not keys or md.parent.name.split("_")[0] in keys):
            out.append(md.parent)
    return out


def shot(sd: Path) -> dict | None:
    """读技能卡的视频 prompt；没写就返回 None。"""
    text = (sd / (sd.name + ".md")).read_text(encoding="utf-8")
    if "## 技能视频 prompt" not in text:
        return None
    part = text[text.index("## 技能视频 prompt"):]
    m = re.search(r"^视频参考[:：]\s*(.+)$", part, re.M)
    b = re.search(r"```text\n(" + re.escape(sd.name) + r"_clip\n.*?)\n```", part, re.S)
    if not m or not b:
        raise SystemExit("%s：「技能视频 prompt」缺「视频参考:」行或 text 块" % sd.name)
    base = next(p for p in sd.parents if p.name == "2_世界观人设")
    refs = []
    for item in [x.strip() for x in m.group(1).split(";") if x.strip()]:
        key, rel = [x.strip().strip("`") for x in item.split("=", 1)]
        path = base / rel
        if not path.is_file():
            raise SystemExit("%s：参考文件不在 %s" % (sd.name, path))
        kind = KIND[path.suffix.lower()]
        refs.append({"key": key, "kind": kind, "role": ROLE[kind], "path": path.relative_to(REPO).as_posix()})
    body = b.group(1)
    owners = [sd.parents[1]]
    for ref in refs:
        path = REPO / ref["path"]
        owners.extend(p for p in path.parents if re.fullmatch(r"[cm]\d+_.+", p.name)
                      and (p / (p.name + ".md")).is_file())
    owners = list(dict.fromkeys(owners))
    added = []
    for owner in owners:
        for image in props_lib.character_props(owner):
            if any(r["path"] == image.relative_to(REPO).as_posix() for r in refs):
                continue
            refs.append({"key": image.stem, "kind": "image", "role": "固定武器", "path": image.relative_to(REPO).as_posix()})
            added.append(image.stem)
    if added:
        body, count = re.subn(r"^(参考[:：].*)$", lambda m: m.group(1) + "、" + "、".join(f"`{key}=>@`" for key in added), body, count=1, flags=re.M)
        if count != 1:
            raise ValueError(f"{sd.name} 缺参考行，不能挂固定武器")
    if any(props_lib.character_prop_keys(owner) for owner in owners):
        body += "\n固定武器：独立武器图锁形制、构件结构、材质与配色；持有数量按人物卡和本镜，同款单件母版可按规定持有多件。人物图、峰值图或运动参考中的武器不能覆盖独立图；动作中不得变形或增减。"
    return {"id": sd.name + "_clip", "text": body, "refs": refs}


TIME_LINE = re.compile(r"^(\d+(?:\.\d+)?(?:[–-]\d+(?:\.\d+)?)?秒)\s*(.+)$")
APPROVAL = re.compile(r"^时间轴审阅[:：].*指纹\s*`?([0-9a-f]{12})`?", re.M)


def timeline(s: dict) -> tuple[list[tuple[str, str]], str]:
    """(时间轴行, 指纹)。指纹只覆盖时长、位置行与分秒行：负面词、参考用法等改动不要求重审。"""
    rows, keep = [], []
    for ln in s["text"].splitlines():
        m = TIME_LINE.match(ln)
        if m:
            rows.append((m.group(1), m.group(2)))
        if m or ln.startswith(("时长：", "位置：")):
            keep.append(ln)
    return rows, hashlib.sha256("\n".join(keep).encode("utf-8")).hexdigest()[:12]


def timeline_table(sd: Path) -> str:
    s = shot(sd)
    if s is None:
        raise SystemExit("%s 还没有「技能视频 prompt」" % sd.name)
    rows, fp = timeline(s)
    if not rows:
        raise SystemExit("%s 的视频 prompt 没有「N–M秒 …」分秒行，写好时间轴再审" % sd.name)
    out = ["%s · %d 秒 · 时间轴指纹 `%s`" % (sd.name, duration(s), fp), "", "| 时间 | 画面 |", "|---|---|"]
    out += ["| %s | %s |" % (t, d.replace("|", "／")) for t, d in rows]
    return "\n".join(out)


def approved(sd: Path) -> str | None:
    text = (sd / (sd.name + ".md")).read_text(encoding="utf-8")
    m = APPROVAL.search(text[text.index("## 技能视频 prompt"):]) if "## 技能视频 prompt" in text else None
    return m.group(1) if m else None


def approve(sd: Path) -> str:
    """在卡的「技能视频 prompt」节记审阅行（替换旧记录）。只在用户于对话中认可时间轴表后运行。"""
    s = shot(sd)
    fp = timeline(s)[1]
    md = sd / (sd.name + ".md")
    text = md.read_text(encoding="utf-8")
    head, part = text[:text.index("## 技能视频 prompt")], text[text.index("## 技能视频 prompt"):]
    line = "时间轴审阅: 用户认可 %s · 指纹 `%s`" % (datetime.now().strftime("%Y-%m-%d %H:%M"), fp)
    part, n = APPROVAL.subn(line, part, count=1)
    if not n:
        part = re.sub(r"^(视频参考[:：])", lambda m: line + "\n\n" + m.group(1), part, count=1, flags=re.M)
    md.write_text(head + part, encoding="utf-8")
    return fp


def check_approved(sd: Path) -> None:
    fp = timeline(shot(sd))[1]
    if approved(sd) != fp:
        raise SystemExit("%s 的时间轴（指纹 %s）还没经用户审阅：先跑 python tools/skill_pack.py timeline，把表交给用户 review，"
                         "用户认可后再 approve，然后才能 submit（必要流程，用户 2026-10-24）" % (sd.name, fp))


def sync(drama: str, keys: list[str]) -> int:
    bad = 0
    for sd in skill_dirs(drama, keys):
        try:
            s = shot(sd)
        except FileNotFoundError as exc:
            shot_pack.invalidate(sd / shot_pack.PACK, [str(exc)])
            print(f"  ! {sd.name}（固定武器缺失，资料包已失效）：{exc}")
            bad += 1
            continue
        if s is None:
            continue
        pack = sd / shot_pack.PACK
        st = shot_pack.state(pack, s)
        if st != "ok":
            shot_pack.build(pack, s)
        print("  %s %s" % ("·" if st == "ok" else "✓", sd.name + ("" if st == "ok" else "（%s → 已更新）" % st)))
    return bad


def duration(s: dict) -> int:
    return next(int(ln[3:-1]) for ln in s["text"].splitlines() if ln.startswith("时长："))


def latest_draft(sd: Path) -> Path:
    """最新一条下载完的草稿条目录；正式条拿它作运动参考（用户看过草稿后才出正式条）。"""
    takes = sorted(p for p in (sd / STAGE_DIR["draft"]).glob("*_*") if (p / (sd.name + "_clip.mp4")).is_file())
    if not takes:
        raise SystemExit("%s 还没有草稿：先出草稿，用户看过再出正式条" % sd.name)
    return takes[-1]


def draft_reference(take: Path, name: str) -> Path:
    """草稿 → 参考视频：1280×720（480p 不够 Seedance 参考像素下限）、24fps、去音轨，同 shot_take.draft_reference。"""
    out = take / "upload" / "draft_ref.mp4"
    out.parent.mkdir(exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(take / (name + "_clip.mp4")), "-an", "-r", "24",
                    "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1",
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(out)], check=True)
    return out


def command(drama: str, sd: Path, stage: str, no_draft: bool = False) -> tuple[list[str], str, dict]:
    """(提交命令, 实际发送的 prompt, 实际上传清单)。正式条在资料包之外追加最新草稿作 @视频N。"""
    s = shot(sd)
    pack = sd / shot_pack.PACK
    if s is None or shot_pack.state(pack, s) != "ok":
        raise SystemExit("%s 资料包不是最新：先跑 python tools/skill_pack.py sync %s %s" % (sd.name, drama, sd.name.split("_")[0]))
    man = json.loads((pack / shot_pack.MANIFEST).read_text(encoding="utf-8"))
    text = (pack / "prompt.txt").read_text(encoding="utf-8")
    prompt = json.loads((REPO / "ai_videos" / drama / "workflow.json").read_text(encoding="utf-8")).get("prompt", {})
    res = prompt.get("draft_resolution", "480p") if stage == "draft" else prompt.get("final_resolution", "720p")
    args = [x for r in man["refs"] for x in (shot_pack.FLAG[r["kind"]], str((pack / r["upload"]).resolve()))]
    if stage == "final" and no_draft:
        man = {**man, "no_draft": True}   # 用户要求直接出正式条、旧草稿已不符（dota follow-up 027）
    elif stage == "final":
        take = latest_draft(sd)
        ref = draft_reference(take, sd.name)
        tag = "@视频%d" % (sum(1 for r in man["refs"] if r["kind"] == "video") + 1)
        key = sd.name + "_clip"
        text = shot_take.final_prompt(text, key, [tag])
        man = {**man, "refs": [*man["refs"], {"tag": tag, "key": shot_take.draft_names(key, 1)[0], "kind": "video",
                                               "role": "用户已审过的草稿", "src": (take / (sd.name + "_clip.mp4")).relative_to(REPO).as_posix(),
                                               "sha256": shot_pack.sha256(take / (sd.name + "_clip.mp4"))}],
               "from_take": take.name}
        args += ["--video", str(ref.resolve())]
    cmd = [sys.executable, str(REPO / "tools" / "service_call.py"), "--target", sd.relative_to(REPO).as_posix(), "--",
           "dreamina", "multimodal2video", *args, "--prompt=%s" % text.rstrip("\n"),
           "--duration=%d" % duration(s), "--ratio=%s" % prompt.get("ratio", "16:9"), "--video_resolution=%s" % res,
           "--model_version=%s" % prompt.get("model", "seedance2.5"), "--poll=0"]
    return cmd, text, man


def submit(drama: str, sd: Path, stage: str, no_draft: bool = False) -> tuple[str, int | None] | None:
    check_approved(sd)
    cmd, text, man = command(drama, sd, stage, no_draft)
    for attempt in range(1, shot_take.UPLOAD_RETRIES + 1):
        r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace")
        try:
            d = json.loads(r.stdout)
        except ValueError:
            print("  ✗ %s 回执读不出（不重提）：%s" % (sd.name, (r.stdout + r.stderr)[-300:]))
            return None
        reason = d.get("fail_reason", "")
        if d.get("gen_status") != "fail" and d.get("submit_id"):
            print("  ✓ %s 已提交 %s（积分 %s）" % (sd.name, d["submit_id"], d.get("credit_count")), flush=True)
            pend = sd / STAGE_DIR[stage] / ".pending" / ("%s.json" % d["submit_id"])
            pend.parent.mkdir(parents=True, exist_ok=True)
            pend.write_text(json.dumps({"stage": stage, "credits": d.get("credit_count"), "prompt": text, "manifest": man},
                                       ensure_ascii=False) + "\n", encoding="utf-8")
            return d["submit_id"], d.get("credit_count")
        if "upload phase" not in reason and "upload resource" not in reason:
            print("  ✗ %s 提交失败（非上传阶段，不重试）：%s" % (sd.name, reason[:300] or r.stdout[-300:]))
            return None
        print("  · %s 上传阶段失败（不扣费），重试 %d/%d" % (sd.name, attempt, shot_take.UPLOAD_RETRIES), flush=True)
    return None


def poll(drama: str, sd: Path, sid: str, interval: int = 20, tries: int = 90) -> int:
    pend = next((p for p in (sd / d / ".pending" / ("%s.json" % sid) for d in STAGE_DIR.values()) if p.is_file()), None)
    saved = json.loads(pend.read_text(encoding="utf-8")) if pend else {}
    stage = saved.get("stage", "draft")
    for _ in range(tries):
        d = shot_take.query(sd, sid, None)
        st = d.get("gen_status")
        print(time.strftime("%H:%M:%S"), sd.name, st, d.get("fail_reason", ""), flush=True)
        if st == "success":
            break
        if st in ("fail", "failed"):
            return 1
        time.sleep(interval)
    else:
        print("  · %s 还没出结果，之后用 poll 补收：%s" % (sd.name, sid))
        return 2
    want = None
    try:
        want = duration(shot(sd))
    except Exception:
        pass
    for attempt in range(1, shot_take.DOWNLOAD_RETRIES + 1):
        tmp = Path(tempfile.mkdtemp(prefix="dreamina_%s_" % sid[:8]))
        shot_take.query(sd, sid, tmp)
        vids = sorted(tmp.rglob("*.mp4"))
        if vids and not shot_take.media_problem(vids[0], want):
            break
        print("  · %s 下载不完整，重下 %d/%d" % (sd.name, attempt, shot_take.DOWNLOAD_RETRIES), flush=True)
    else:
        print("  ✗ %s 下载失败（已扣费，只重下不重提）：poll %s" % (sd.name, sid))
        return 1
    folder = sd / STAGE_DIR[stage] / ("%s_%s" % (datetime.now().strftime("%Y%m%d-%H%M%S"), sid[:8]))
    folder.mkdir(parents=True)
    shutil.copyfile(vids[0], folder / (sd.name + "_clip.mp4"))
    (folder / "prompt.txt").write_text(saved.get("prompt", ""), encoding="utf-8", newline="\n")
    (folder / "generation.json").write_text(json.dumps(
        {"key": sd.name + "_clip", "submit_id": sid, "stage": stage, "credits": saved.get("credits"),
         "downloaded_at": datetime.now().isoformat(timespec="seconds"), "video": sd.name + "_clip.mp4",
         "refs": [{k: r.get(k) for k in ("tag", "key", "src", "sha256")} for r in saved.get("manifest", {}).get("refs", [])]},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if pend:
        pend.unlink()
    print("  ✓ %s → %s" % (sd.name, (folder / (sd.name + "_clip.mp4")).relative_to(REPO).as_posix()))
    next_steps(folder)
    return 0


FEEDBACK = "user_feedback.md"


def policy(sd: Path) -> dict:
    """剧级登记表里的 [policy]（没有登记表或没写就空）。"""
    import tomllib
    import qc
    drama = qc.drama_dir_of(sd)
    reg = drama / qc.DRAMA_REG if drama else None
    if not reg or not reg.is_file():
        return {}
    return tomllib.loads(reg.read_text(encoding="utf-8")).get("policy", {})


def latest_take(sd: Path) -> Path | None:
    takes = [d for sub in STAGE_DIR.values() for d in (sd / sub).glob("*/") if list(d.glob("*_clip.mp4"))]
    return max(takes, key=lambda d: d.name) if takes else None


def feedback_gate(sd: Path) -> str | None:
    """剧级策略要求时：上一条出片还没有用户反馈记录就不许再提交（dota_yingxiong follow-up 295）。返回拒绝理由或 None。"""
    if not policy(sd).get("wait_user_feedback_after_render"):
        return None
    take = latest_take(sd)
    if take and not (take / FEEDBACK).is_file():
        return ("%s 的上一条出片 %s 还没有用户反馈：先把片子发给用户，等用户回复后用 "
                "python tools/skill_pack.py feedback <剧> %s \"用户原话\" 记下，才能再提交（剧级策略 wait_user_feedback_after_render）"
                % (sd.name, take.relative_to(REPO).as_posix(), sd.name.split("_")[0]))
    return None


def feedback(sd: Path, text: str) -> Path:
    take = latest_take(sd)
    if not take:
        raise SystemExit("%s 还没有出片，不用记反馈" % sd.name)
    p = take / FEEDBACK
    old = p.read_text(encoding="utf-8") if p.is_file() else "# 用户反馈" + chr(10)
    line = "- %s：%s" % (datetime.now().strftime("%Y-%m-%d %H:%M"), text)
    p.write_text(old + chr(10) + line + chr(10), encoding="utf-8")
    return p


def log_gate(drama: str) -> bool:
    """提交前查本剧 follow-up 日志：**本会话自己**的条目撞号 / 格式不对 / 待补超时就不提交。

    拦截同时放在出片工具里，不只依赖 Kimi Stop hook。项目不在 specs 日志体系里的不拦。
    只拦自己、不拦别的会话丢下的条目，没有单点拦截（follow-up 280）。
    """
    import followup
    try:
        probs = [p for p in followup.check_one(followup.resolve(drama), followup.current_owner()) if p.blocking]
    except SystemExit:
        return True
    for pr in probs:
        print("  ✗ 日志：%s %s" % (pr.kind, pr.detail))
    if probs:
        print("  ✗ 先用 python tools/followup.py done 收尾本会话的条目再提交")
    return not probs


def pre_gate(dirs: list[Path]) -> bool:
    """出片前闸门：规格、参考、体型、每个角色的立场与视线先过关再出片（dota_yingxiong follow-up 266）。

    只对有剧级登记表的剧生效；一条不过整批不提交。结论绑定资料包，规格或参考改了要重审。
    """
    import qc_pre
    ok = True
    for sd in dirs:
        block, soft = qc_pre.gate(sd)
        for s in soft:
            print("  · %s 出片前：%s" % (sd.name, s))
        if block:
            ok = False
            rel = sd.relative_to(REPO).as_posix()
            print("  ✗ %s 出片前闸门不通过：%s" % (sd.name, "；".join(block)))
            print("     先跑：python tools/qc_pre.py machine %s" % rel)
            print("           python tools/qc_review.py %s --pre     # 多视角审：每个角色的立场与视线、导演、原版还原" % rel)
    return ok


def next_steps(folder: Path) -> None:
    """片子落地后打印自检三步——只对有剧级登记表（已启用自检）的剧。"""
    import qc
    drama = qc.drama_dir_of(folder)
    if not drama or not (drama / qc.DRAMA_REG).exists():
        return
    rel = folder.relative_to(REPO).as_posix()
    print("  → 自检（Kimi）：")
    print("     python tools/motion_check.py %s/*_clip.mp4 --action <起势结束>-<收势开始> --sheet %s/sheet_4fps.jpg" % (rel, rel))
    print("     python tools/qc.py record %s --check video.slowmo=pass|fail --by machine --evidence \"…\"" % rel)
    print("     python tools/qc_review.py %s        # 另起 Kimi 进程独立审稿" % rel)
    print("     python tools/qc.py gate %s          # 不过不交、不进成片" % rel)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="技能视频资料包与出片")
    ap.add_argument("action", choices=("sync", "timeline", "approve", "cmd", "submit", "poll", "feedback"))
    ap.add_argument("drama")
    ap.add_argument("rest", nargs="*")
    ap.add_argument("--stage", choices=tuple(STAGE_DIR), default="draft")
    ap.add_argument("--no-draft", action="store_true", help="正式条不带草稿作参考（只在用户明确要求直接出正式条时用）")
    a = ap.parse_args()
    if a.action == "sync":
        return sync(a.drama, a.rest)
    if a.action == "poll":
        return poll(a.drama, skill_dirs(a.drama, a.rest[:1])[0], a.rest[1])
    if a.action == "feedback":
        if len(a.rest) < 2:
            raise SystemExit("用法：skill_pack.py feedback <剧> <技能键> \"用户原话\"")
        print("  ✓ 已记用户反馈 → %s" % feedback(skill_dirs(a.drama, a.rest[:1])[0], " ".join(a.rest[1:])).relative_to(REPO).as_posix())
        return 0
    dirs = skill_dirs(a.drama, a.rest)
    if a.action == "timeline":
        print("\n\n".join(timeline_table(sd) for sd in dirs))
        return 0
    if a.action == "approve":
        if not a.rest:
            raise SystemExit("approve 必须点名技能键（只记用户在对话里认可过的那几条）")
        for sd in dirs:
            print("  ✓ %s 时间轴审阅已记录，指纹 %s" % (sd.name, approve(sd)))
        return 0
    for sd in dirs if a.action == "submit" else []:
        check_approved(sd)   # 先全部检查，任何一条没审就一条都不提交
        why = feedback_gate(sd)
        if why:
            raise SystemExit(why)
    if a.action == "cmd":
        for sd in dirs:
            cmd = [x for x in command(a.drama, sd, a.stage, a.no_draft)[0] if not x.startswith("--prompt=")]
            print(" ".join('"%s"' % x if " " in x else x for x in cmd), "--prompt=…")
        return 0
    if dirs and not (log_gate(a.drama) and pre_gate(dirs)):
        return 1
    sent = [(sd, submit(a.drama, sd, a.stage, a.no_draft)) for sd in dirs]   # 先全部提交，再逐个等，排队时间重叠
    return max([poll(a.drama, sd, r[0]) if r else 1 for sd, r in sent] or [0])


if __name__ == "__main__":
    raise SystemExit(main())
