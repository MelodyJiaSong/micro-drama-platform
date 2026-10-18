# -*- coding: utf-8 -*-
"""技能视频资料包与出片：每个技能卡一个 `资料包/`，格式与镜头资料包相同（`tools/shot_pack.py`），出片走同一 Dreamina 入口。

技能卡在 `ai_videos/{剧}/2_世界观人设/characters/{英雄}/skills/{目录}/{目录}.md`（dota_yingxiong follow-up 010），
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
    python tools/skill_pack.py submit <剧> <技能键 …> [--stage draft|final]   # 提交并等结果（会扣积分，只在用户决定生成后执行）
    python tools/skill_pack.py poll   <剧> <技能键> <submit_id>                # 补收

条目录 ＝ `{技能目录}/{drafts|renders}/{YYYYMMDD-HHMMSS}_{submit_id 前 8 位}/`：`{目录}_clip.mp4`、`generation.json`、`prompt.txt`。
生成永远人点：submit 只在用户明确要出片后运行。
"""
from __future__ import annotations

import argparse
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

KIND = {".png": "image", ".jpg": "image", ".jpeg": "image", ".mp3": "audio", ".wav": "audio", ".mp4": "video"}
ROLE = {"image": "参考图", "audio": "声音参考", "video": "参考视频"}
STAGE_DIR = {"draft": "drafts", "final": "renders"}


def settings_dir(drama: str) -> Path:
    return REPO / "ai_videos" / drama / "2_世界观人设"


def skill_dirs(drama: str, keys: list[str]) -> list[Path]:
    out = []
    for md in sorted(settings_dir(drama).glob("characters/*/skills/k*/k*.md")):
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
    base = settings_dir(sd.parents[3].parent.name)
    refs = []
    for item in [x.strip() for x in m.group(1).split(";") if x.strip()]:
        key, rel = [x.strip().strip("`") for x in item.split("=", 1)]
        path = base / rel
        if not path.is_file():
            raise SystemExit("%s：参考文件不在 %s" % (sd.name, path))
        kind = KIND[path.suffix.lower()]
        refs.append({"key": key, "kind": kind, "role": ROLE[kind], "path": path.relative_to(REPO).as_posix()})
    return {"id": sd.name + "_clip", "text": b.group(1), "refs": refs}


def sync(drama: str, keys: list[str]) -> int:
    bad = 0
    for sd in skill_dirs(drama, keys):
        s = shot(sd)
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


def command(drama: str, sd: Path, stage: str) -> list[str]:
    s = shot(sd)
    pack = sd / shot_pack.PACK
    if s is None or shot_pack.state(pack, s) != "ok":
        raise SystemExit("%s 资料包不是最新：先跑 python tools/skill_pack.py sync %s %s" % (sd.name, drama, sd.name.split("_")[0]))
    man = json.loads((pack / shot_pack.MANIFEST).read_text(encoding="utf-8"))
    prompt = json.loads((REPO / "ai_videos" / drama / "workflow.json").read_text(encoding="utf-8")).get("prompt", {})
    res = prompt.get("draft_resolution", "480p") if stage == "draft" else prompt.get("final_resolution", "720p")
    args = [x for r in man["refs"] for x in (shot_pack.FLAG[r["kind"]], str((pack / r["upload"]).resolve()))]
    return [sys.executable, str(REPO / "tools" / "service_call.py"), "--target", sd.relative_to(REPO).as_posix(), "--",
            "dreamina", "multimodal2video", *args, "--prompt=%s" % (pack / "prompt.txt").read_text(encoding="utf-8").rstrip("\n"),
            "--duration=%d" % duration(s), "--ratio=%s" % prompt.get("ratio", "16:9"), "--video_resolution=%s" % res,
            "--model_version=%s" % prompt.get("model", "seedance2.5"), "--poll=0"]


def submit(drama: str, sd: Path, stage: str) -> tuple[str, int | None] | None:
    cmd = command(drama, sd, stage)
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
            pend.write_text(json.dumps({"stage": stage, "credits": d.get("credit_count"),
                                        "prompt": (sd / shot_pack.PACK / "prompt.txt").read_text(encoding="utf-8"),
                                        "manifest": json.loads((sd / shot_pack.PACK / shot_pack.MANIFEST).read_text(encoding="utf-8"))},
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
    return 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="技能视频资料包与出片")
    ap.add_argument("action", choices=("sync", "cmd", "submit", "poll"))
    ap.add_argument("drama")
    ap.add_argument("rest", nargs="*")
    ap.add_argument("--stage", choices=tuple(STAGE_DIR), default="draft")
    a = ap.parse_args()
    if a.action == "sync":
        return sync(a.drama, a.rest)
    if a.action == "poll":
        return poll(a.drama, skill_dirs(a.drama, a.rest[:1])[0], a.rest[1])
    dirs = skill_dirs(a.drama, a.rest)
    if a.action == "cmd":
        for sd in dirs:
            print(" ".join('"%s"' % x if " " in x else x for x in command(a.drama, sd, a.stage)[:-1]), "…")
        return 0
    sent = [(sd, submit(a.drama, sd, a.stage)) for sd in dirs]   # 先全部提交，再逐个等，排队时间重叠
    return max([poll(a.drama, sd, r[0]) if r else 1 for sd, r in sent] or [0])


if __name__ == "__main__":
    raise SystemExit(main())
