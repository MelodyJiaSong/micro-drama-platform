# -*- coding: utf-8 -*-
"""每次生成一个「条」目录（follow-up 230）：视频、生成记录、当时的 prompt 与审核放在一起。

    python tools/shot_take.py submit <集目录> <镜头key> [<镜头key> …] [--stage draft|final] [--from <条>]
                                                                                    # 依次提交 → 查询 → 下载建条目录（会扣积分，只在用户决定生成后跑）
    python tools/shot_take.py approved <集目录>                                     # 列出草稿已通过、还没出正式条的镜头
    python tools/shot_take.py poll   <集目录> <镜头key> <submit_id> [--credits N]   # 查询直到出结果，下载并建条目录
    python tools/shot_take.py record <集目录> <镜头key> <submit_id> --video <已下载的视频> [--credits N]

条目录 ＝ `{镜头目录}/renders/{YYYYMMDD-HHMMSS}_{submit_id 前 8 位}/`（草稿放 `{镜头目录}/drafts/`，follow-up 266）：
    {镜头key}_{原文件名}.mp4   生成的视频（文件名带镜头 key，导入与选条都认它）
    generation.json            submit_id、模型、时长、比例、分辨率、积分、时间、参考清单（每个文件的 key 与 sha256）
    prompt.txt                 提交时的 prompt 原文（资料包里填好上传编号的那一份）
    review.md                  审核：Vision / 对的 / 不对的 / 结论 / 怎么看的。先写待审核模板，看片后填写（Vision 一项 2026-10-12 起必填，follow-up 249）
提交与查询都经 `tools/service_call.py` 先记请求日志；`submit` 只在用户决定生成后运行（生成视频永远人点）。

两步出片（follow-up 265）：`--stage draft`（默认）按资料包原样出低价草稿，分辨率读剧 `workflow.json` 的
`prompt.draft_resolution`（缺省 480p，Seedance 2.5 最低一档）；用户在管理界面把草稿标成「通过」（写进该条 review.md 的
「状态：通过…」）后，`--stage final` 出正式条：分辨率读 `prompt.resolution`（720p），资料包全部参考与 prompt 照旧，
再把通过的草稿统一成 1280×720、24fps、无声、≤15 s 一段，作为最后的参考视频追加上去，「参考：」「参考用法：」两行补上它
（镜头、走位、表演、节奏照草稿，长相服装仍以三视图为准）。不给 `--from` 就用这一镜最新一条通过的草稿。
`--stage final --no-draft <理由>`：用户明确要求这次不经草稿时，按资料包原样直接出正式条，理由记进生成记录
（`no_draft`），没有草稿参考视频（follow-up 272）。
提交用资料包 `upload/` 里的副本、绝对路径（follow-up 229 实测：相对路径传不上，大文件在 VPN 下超时）；
上传阶段失败不扣费，最多重试 UPLOAD_RETRIES 次；回执带 submit_id 就不再重提（重提会重复扣费）。
"""
from __future__ import annotations

import argparse
import json
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

REVIEW_TEMPLATE = """# 审核：{key} · {take}

状态：待审核

Vision：

## 对的

-

## 不对的

-

## 结论

（保留 / 重出 / 改分镜后重出，写清原因）

## 怎么看的

（逐秒抽帧、全分辨率局部、与参考图并排、音量；判断「没有」之前先看全分辨率）
"""


def shot_info(ep_dir: Path, key: str) -> tuple[dict, Path]:
    shots, _ = shot_pack.episode_problems(ep_dir)
    shot = next((s for s in shots if s["id"] == key), None)
    if shot is None:
        raise SystemExit("prompts.json 里没有 %s" % key)
    return shot, shot_pack.shot_dir(ep_dir, shot["scene"], key)


STAGES = ("draft", "final")
STAGE_DIR = {"draft": "drafts", "final": "renders"}     # 草稿单独一个目录（follow-up 266）
DEFAULT_RESOLUTION = {"draft": "480p", "final": "720p"}
APPROVED = "通过"
STATUS_PREFIX = "状态："


def stage_resolution(settings: dict, stage: str) -> str:
    """草稿读 `draft_resolution`，正式条读 `resolution`（剧 workflow.json 的 prompt 段）。"""
    return settings.get("draft_resolution" if stage == "draft" else "resolution", DEFAULT_RESOLUTION[stage])


def take_record(folder: Path) -> dict:
    f = folder / "generation.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.is_file() else {}


def take_status(folder: Path) -> str:
    f = folder / "review.md"
    text = f.read_text(encoding="utf-8") if f.is_file() else ""
    return next((ln[len(STATUS_PREFIX):].strip() for ln in text.splitlines() if ln.startswith(STATUS_PREFIX)), "")


def take_stage(folder: Path, settings: dict) -> str:
    """两步出片之前的条没有 stage：分辨率等于草稿档的算草稿，其余算正式条。"""
    record = take_record(folder)
    if record.get("stage") in STAGES:
        return record["stage"]
    return "draft" if record.get("resolution") == stage_resolution(settings, "draft") else "final"


def approved_draft(sd: Path, from_take: str | None = None, settings: dict | None = None) -> Path:
    """用户标了通过的草稿条：给了 `from_take` 就核对那一条，否则取这一镜最新一条。"""
    settings = settings or {}
    renders = sd / STAGE_DIR["draft"]

    def ok(f: Path) -> bool:
        return f.is_dir() and take_stage(f, settings) == "draft" and take_status(f).startswith(APPROVED)
    if from_take:
        folder = renders / from_take
        if not ok(folder):
            raise SystemExit("%s 不是用户标了通过的草稿：先在管理界面审草稿并点「通过」" % from_take)
        return folder
    found = sorted((f for f in renders.iterdir() if ok(f)), key=lambda f: f.name) if renders.is_dir() else []
    if not found:
        raise SystemExit("%s 没有用户标了通过的草稿：先出草稿（--stage draft），审过点「通过」再出正式条" % sd.name)
    return found[-1]


def draft_video(folder: Path) -> Path:
    videos = sorted(p for p in folder.glob("*.mp4") if p.is_file())
    if not videos:
        raise SystemExit("%s 里没有视频" % folder)
    return videos[0]


def draft_reference(folder: Path) -> list[Path]:
    """草稿 → 可上传的参考视频：1280×720（480p 宽 848 时不够 Seedance 参考下限 409600 像素）、24fps、去音轨，
    超过 15 s 按 seedance_ref 切段。放在草稿条目录的 upload/ 下，提交了什么一看就知道。"""
    from tools.previz.seedance_ref import split
    src = draft_video(folder)
    out = folder / "upload" / "draft_ref.mp4"
    out.parent.mkdir(exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-an", "-r", "24",
                    "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1",
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(out)], check=True)
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)],
                       capture_output=True, text=True, check=True)
    return split(out, float(p.stdout.strip()), [])


def draft_names(key: str, n: int) -> list[str]:
    return ["%s_draft" % key] if n == 1 else ["%s_draft_p%d" % (key, i) for i in range(1, n + 1)]


def final_prompt(text: str, key: str, tags: list[str]) -> str:
    """资料包 prompt 原样，「参考：」行末追加草稿的 key=>@视频N，「参考用法：」行末补一句用法。"""
    names = draft_names(key, len(tags))
    listed = "、".join("`%s`" % n for n in names)
    usage = ("%s是本镜用户已审过的草稿%s：机位、运镜、构图、人物站位与走位、动作、表演和台词节奏都照它重拍，时长一致；"
             "人物长相、服装与道具仍以三视图和道具图为准，不照搬草稿的低清画质与瑕疵；草稿与其他运动参考不一致时以草稿为准。"
             % (listed, "（按顺序接起来是完整一镜）" if len(tags) > 1 else ""))
    out: list[str] = []
    has_usage = False
    for line in text.splitlines(keepends=True):
        body = line.rstrip("\n")
        end = line[len(body):]
        if body.startswith("参考："):
            line = body + "".join("、`%s=>%s`" % (n, t) for n, t in zip(names, tags)) + end
        elif body.startswith("参考用法："):
            has_usage = True
            line = body + usage + end
        out.append(line)
    if not has_usage:
        i = next(i for i, ln in enumerate(out) if ln.startswith("参考："))
        out.insert(i + 1, "参考用法：" + usage + "\n")
    return "".join(out)


def make_take(ep_dir: Path, key: str, sid: str, video: Path, credits: int | None, model: str | None,
              sent: tuple[str, dict] | None = None, meta: dict | None = None) -> Path:
    """`sent` ＝ 提交那一刻的（prompt 原文, manifest）。等出片期间资料包可能已重编译（follow-up 231 实测 st12），
    条目录必须记提交时的版本；poll / record 补收时拿不到，才退回资料包当前版本。
    `meta` ＝ 两步出片的 stage、实际提交的分辨率、正式条出自哪条草稿（follow-up 265）。"""
    meta = meta or {}
    shot, sd = shot_info(ep_dir, key)
    pack = sd / shot_pack.PACK
    manifest = json.loads((pack / shot_pack.MANIFEST).read_text(encoding="utf-8")) if (pack / shot_pack.MANIFEST).is_file() else {}
    if sent is not None:
        manifest = sent[1]
    settings = shot_pack.es.settings(shot_pack.es.drama_root(ep_dir)).get("prompt", {})
    take = "%s_%s" % (datetime.now().strftime("%Y%m%d-%H%M%S"), sid[:8])
    folder = sd / STAGE_DIR[meta.get("stage", "draft")] / take
    folder.mkdir(parents=True)
    dst = folder / (video.name if key in video.name else "%s_%s" % (key, video.name))
    shutil.copyfile(video, dst)
    duration = next((int(ln[3:-1]) for ln in shot["text"].splitlines() if ln.startswith("时长：")), None)
    record = {"key": key, "take": take, "submit_id": sid, "model": model or settings.get("model", "seedance2.5"),
              "stage": meta.get("stage", "draft"), "duration_s": duration, "ratio": settings.get("ratio", "16:9"),
              "resolution": meta.get("resolution") or stage_resolution(settings, meta.get("stage", "draft")), "credits": credits,
              "downloaded_at": datetime.now().isoformat(timespec="seconds"), "video": dst.name,
              "request_log": (ep_dir / "request_log.md").relative_to(REPO).as_posix(),
              "prompt_sha256": manifest.get("prompt_sha256"),
              "refs": [{k: r.get(k) for k in ("tag", "key", "kind", "role", "src", "sha256")} for r in manifest.get("refs", [])]}
    if meta.get("from_take"):
        record["from_take"] = meta["from_take"]
    if meta.get("no_draft"):
        record["no_draft"] = meta["no_draft"]
    (folder / "generation.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    prompt = pack / "prompt.txt"
    text = sent[0] if sent is not None else prompt.read_text(encoding="utf-8") if prompt.is_file() else shot["text"] + "\n"
    (folder / "prompt.txt").write_text(text, encoding="utf-8", newline="\n")
    (folder / "review.md").write_text(REVIEW_TEMPLATE.format(key=key, take=take), encoding="utf-8", newline="\n")
    return folder


def query(ep_dir: Path, sid: str, download_dir: Path | None) -> dict:
    cmd = [sys.executable, str(REPO / "tools" / "service_call.py"), "--target", ep_dir.relative_to(REPO).as_posix(), "--",
           "dreamina", "query_result", "--submit_id=%s" % sid]
    if download_dir is not None:
        download_dir.mkdir(parents=True, exist_ok=True)
        cmd.append("--download_dir=%s" % download_dir)
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        return json.loads(r.stdout)
    except ValueError:
        return {"gen_status": "unparsed", "raw": (r.stdout + r.stderr)[-500:]}


UPLOAD_RETRIES = 3
DOWNLOAD_RETRIES = 3


def media_problem(video: Path, want_s: float | None = None) -> str:
    """'' when the file decodes end to end (and, if given, lasts about want_s); otherwise what is wrong.
    A download cut off mid-file still opens and reports a duration, so only a full decode catches it
    (2026-10-11: s2 st8 / st12 / st16 were truncated and recorded as takes)."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "null", "-"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    err = r.stderr.strip()
    if r.returncode != 0 or err:
        return "解码出错：" + (err.splitlines()[0][:160] if err else "ffmpeg rc=%d" % r.returncode)
    if want_s is not None:
        p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                           capture_output=True, text=True)
        try:
            dur = float(p.stdout.strip())
        except ValueError:
            return "读不出时长"
        if abs(dur - float(want_s)) > 0.5:
            return "时长 %.2f 秒，应为 %s 秒" % (dur, want_s)
    return ""


PENDING = ".pending"      # {drafts|renders}/.pending/{submit_id}.json：提交时的 prompt、manifest 与 meta，poll 补收时用


def pending_file(ep_dir: Path, key: str, sid: str, stage: str | None = None) -> Path:
    """给了 stage 就是那一步的目录；没给（poll 补收）就找已有的那一份，都没有按正式条目录。"""
    sd = shot_info(ep_dir, key)[1]
    paths = [sd / STAGE_DIR[s] / PENDING / ("%s.json" % sid) for s in ([stage] if stage else STAGES)]
    return next((p for p in paths if p.is_file()), paths[-1])


def submit(ep_dir: Path, key: str, stage: str = "draft", from_take: str | None = None, no_draft: str | None = None
           ) -> tuple[str, int | None, tuple[str, dict], dict] | None:
    """提交一镜：返回 (submit_id, 积分, 提交时的 (prompt, manifest), meta)；上传阶段失败重试；其他失败返回 None。"""
    shot, sd = shot_info(ep_dir, key)
    pack = sd / shot_pack.PACK
    if shot_pack.state(pack, shot) != "ok" or (pack / shot_pack.INVALID).is_file():
        print("  ✗ %s 资料包不是最新：先跑 python tools/shot_pack.py sync" % key)
        return None
    man = json.loads((pack / shot_pack.MANIFEST).read_text(encoding="utf-8"))
    sent_text = (pack / "prompt.txt").read_text(encoding="utf-8")
    settings = shot_pack.es.settings(shot_pack.es.drama_root(ep_dir)).get("prompt", {})
    duration = next(int(ln[3:-1]) for ln in shot["text"].splitlines() if ln.startswith("时长："))
    resolution = stage_resolution(settings, stage)
    meta: dict = {"stage": stage, "resolution": resolution}
    args = [x for r in man["refs"] for x in (shot_pack.FLAG[r["kind"]], str((pack / r["upload"]).resolve()))]
    if stage == "final" and no_draft:
        meta["no_draft"] = no_draft
    elif stage == "final":
        draft = approved_draft(sd, from_take, settings)
        parts = draft_reference(draft)
        model = settings.get("model", "seedance2.5")
        limit = shot_pack.MODEL_LIMITS.get(shot_pack.MODEL_ALIASES.get(model, model), {}).get("max_videos", 0)
        videos = sum(1 for r in man["refs"] if r["kind"] == "video")
        if videos + len(parts) > limit:
            print("  ✗ %s 参考视频 %d 条 + 草稿 %d 段，超过 %s 一次 %d 条" % (key, videos, len(parts), model, limit))
            return None
        tags = ["@视频%d" % (videos + i) for i in range(1, len(parts) + 1)]
        sent_text = final_prompt(sent_text, key, tags)
        src = draft_video(draft).relative_to(REPO).as_posix()
        man = {**man, "refs": [*man["refs"], *({"tag": t, "key": n, "kind": "video", "role": "用户已审过的草稿", "src": src,
                                                 "sha256": shot_pack.sha256(part) if part.is_file() else None}
                                                for t, n, part in zip(tags, draft_names(key, len(parts)), parts))]}
        args += [x for part in parts for x in ("--video", str(part))]
        meta["from_take"] = draft.name
    cmd = [sys.executable, str(REPO / "tools" / "service_call.py"), "--target", ep_dir.relative_to(REPO).as_posix(), "--",
           "dreamina", "multimodal2video", *args, "--prompt=%s" % sent_text.rstrip("\n"),
           "--duration=%d" % duration, "--ratio=%s" % settings.get("ratio", "16:9"), "--video_resolution=%s" % resolution,
           "--model_version=%s" % settings.get("model", "seedance2.5"), "--poll=0"]
    for attempt in range(1, UPLOAD_RETRIES + 1):
        r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace")
        try:
            d = json.loads(r.stdout)
        except ValueError:
            print("  ✗ %s 回执读不出：%s" % (key, (r.stdout + r.stderr)[-300:]))
            return None
        reason = d.get("fail_reason", "")
        if d.get("gen_status") != "fail":
            print("  ✓ %s 已提交 %s（积分 %s，第 %d 次）" % (key, d.get("submit_id"), d.get("credit_count"), attempt), flush=True)
            pend = pending_file(ep_dir, key, d["submit_id"], stage)
            pend.parent.mkdir(parents=True, exist_ok=True)
            pend.write_text(json.dumps({"prompt": sent_text, "manifest": man, "meta": meta}, ensure_ascii=False) + "\n",
                            encoding="utf-8")
            return d["submit_id"], d.get("credit_count"), (sent_text, man), meta
        if "upload phase" not in reason and "upload resource" not in reason:  # apply / commit 阶段的上传失败也未扣费
            print("  ✗ %s 提交失败（非上传阶段，不重试）：%s" % (key, reason[:300]))
            return None
        print("  · %s 上传阶段失败（不扣费），重试 %d/%d：%s" % (key, attempt, UPLOAD_RETRIES, reason[-120:]), flush=True)
    return None


def wait_and_record(ep_dir: Path, key: str, sid: str, credits: int | None, model: str | None, interval: int, tries: int,
                    sent: tuple[str, dict] | None = None, meta: dict | None = None) -> int:
    pend = pending_file(ep_dir, key, sid)
    if sent is None and pend.is_file():
        saved = json.loads(pend.read_text(encoding="utf-8"))
        sent = (saved["prompt"], saved["manifest"])
        meta = meta or saved.get("meta")
    tmp = Path(tempfile.mkdtemp(prefix="dreamina_%s_" % sid[:8]))
    for _ in range(tries):
        d = query(ep_dir, sid, None)
        st = d.get("gen_status")
        print(time.strftime("%H:%M:%S"), key, st, (d.get("queue_info") or {}).get("queue_status", ""), d.get("fail_reason", ""), flush=True)
        if st == "success":
            videos: list[Path] = []
            want = next((float(ln[3:-1]) for ln in (sent[0] if sent else "").splitlines() if ln.startswith("时长：")), None)
            for attempt in range(1, DOWNLOAD_RETRIES + 1):  # 下载偶发超时（VPN 下 vlabvod），已扣费，只重下不重提
                query(ep_dir, sid, tmp)
                videos = sorted(p for p in tmp.rglob("*.mp4"))
                problems = [(v, media_problem(v, want)) for v in videos]
                if videos and not any(why for _, why in problems):
                    break
                for v, why in problems:          # 截断的文件删掉重下，不进条目录
                    if why:
                        print("  · %s 下载的文件不完整（%s），删掉重下" % (key, why), flush=True)
                        v.unlink(missing_ok=True)
                videos = []
                print("  · %s 下载失败，重试 %d/%d" % (key, attempt, DOWNLOAD_RETRIES), flush=True)
                time.sleep(10)
            if not videos:
                print("  ✗ 显示成功但没下载到视频：%s；稍后跑 poll %s（不会重复提交）" % (tmp, sid))
                return 1
            for v in videos:
                print("→ %s" % make_take(ep_dir, key, sid, v, credits, model, sent, meta=meta).relative_to(REPO).as_posix(), flush=True)
            shutil.rmtree(tmp, ignore_errors=True)
            pend.unlink(missing_ok=True)
            return 0
        if st in ("fail", "failed"):
            print(json.dumps(d, ensure_ascii=False)[:800])
            return 1
        time.sleep(interval)
    print("  ✗ %s 查询 %d 次仍未完成；稍后跑 poll %s（不会重复提交）" % (key, tries, sid))
    return 1


def approved_shots(ep_dir: Path) -> list[str]:
    """草稿已被用户标通过、且还没有从这条草稿出过正式条的镜头。"""
    settings = shot_pack.es.settings(shot_pack.es.drama_root(ep_dir)).get("prompt", {})
    shots, _ = shot_pack.episode_problems(ep_dir)
    out = []
    for shot in shots:
        sd = shot_pack.shot_dir(ep_dir, shot["scene"], shot["id"])
        try:
            draft = approved_draft(sd, None, settings)
        except SystemExit:
            continue
        renders = sd / STAGE_DIR["final"]
        done = {take_record(f).get("from_take") for f in renders.iterdir() if f.is_dir()} if renders.is_dir() else set()
        if draft.name not in done:
            out.append(shot["id"])
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="生成记录：每次生成一个条目录")
    ap.add_argument("action", choices=["submit", "poll", "record", "approved"])
    ap.add_argument("episode", type=Path)
    ap.add_argument("key", nargs="?")
    ap.add_argument("rest", nargs="*", help="poll / record：submit_id；submit：更多镜头 key")
    ap.add_argument("--video", type=Path)
    ap.add_argument("--stage", choices=STAGES, default="draft", help="draft＝低价草稿（默认）；final＝用通过的草稿出正式条")
    ap.add_argument("--from", dest="from_take", help="final：用哪一条草稿（缺省＝这一镜最新一条通过的草稿）")
    ap.add_argument("--no-draft", dest="no_draft", metavar="理由",
                    help="final：用户明确要求这次不经草稿，按资料包直接出正式条；理由写进生成记录")
    ap.add_argument("--credits", type=int)
    ap.add_argument("--model")
    ap.add_argument("--interval", type=int, default=60)
    ap.add_argument("--max", type=int, default=40, help="最多查询几次")
    a = ap.parse_args()
    ep_dir = a.episode.resolve()
    if a.action == "approved":
        for key in approved_shots(ep_dir):
            print(key)
        return 0
    if a.key is None:
        ap.error("要给镜头 key")
    if a.no_draft and a.stage != "final":
        ap.error("--no-draft 只用于 --stage final")
    if a.action == "submit":
        rc = 0
        for key in [a.key, *a.rest]:
            try:
                got = submit(ep_dir, key, a.stage, a.from_take, a.no_draft)
            except SystemExit as e:        # 没有通过的草稿：这一镜不提交，接着下一镜
                got = None
                print("  ✗ %s" % e, flush=True)
            if got is None:
                rc = 1
                print("  ✗ %s 未提交，跳到下一镜" % key, flush=True)
                continue
            rc |= wait_and_record(ep_dir, key, got[0], got[1], a.model, a.interval, a.max, got[2], got[3])
        return rc
    sid = a.rest[0]
    if a.action == "record":
        settings = shot_pack.es.settings(shot_pack.es.drama_root(ep_dir)).get("prompt", {})
        meta = {"stage": a.stage, "resolution": stage_resolution(settings, a.stage)}
        print("→ %s" % make_take(ep_dir, a.key, sid, a.video.resolve(), a.credits, a.model, meta=meta).relative_to(REPO).as_posix())
        return 0
    return wait_and_record(ep_dir, a.key, sid, a.credits, a.model, a.interval, a.max)


if __name__ == "__main__":
    sys.exit(main())
