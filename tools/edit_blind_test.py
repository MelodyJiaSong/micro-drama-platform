"""剪辑盲测：同一素材池、同一说明，两种剪法盲审对比（ai_video_management follow-up 354）。

首个用例：现有流程 vs CapCut AI 粗剪（chuanyue_yiri follow-up 039）。商用是硬门：
被测一方的成片只能由素材池里的画面和声音组成，任何外来画面、文字、音乐、音效都判不合规，
不合规的版本不进盲审。

    python tools/edit_blind_test.py pool    <测试目录> --cut <场 cut_vN.json>   # 建素材池与现有流程一方
    python tools/edit_blind_test.py set-vid <测试目录> clip_01 <VID>             # 记上传后的 VID
    python tools/edit_blind_test.py check   <测试目录> <成片.mp4> [--draft <stdraft.json>] [--name capcut]
    python tools/edit_blind_test.py blind   <测试目录>                             # 两方都合规后盲化
    python tools/edit_blind_test.py review  <测试目录> [--reviewer claude codex]  # 独立模型盲审（A/B 正反各一次）
    python tools/edit_blind_test.py reveal  <测试目录>                             # 人审表填完后揭盲

画面检查：成片每秒 4 帧，与素材池每一帧比（128×72 灰度），整体差与 16×12 分块的最大块差都要小；
声音检查：每 0.5 秒窗口与素材池音轨做归一化互相关，取最大值。阈值先用现有流程一方校准（它只用素材池）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import secrets
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
for _stream in (sys.stdout, sys.stderr):    # Windows 非 UTF-8 控制台打印中文会崩（chuanyue_yiri follow-up 043）
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
W, H = 128, 72            # 画面找最近帧用的尺寸
HW, HH = 320, 180         # 分块比对用的尺寸（小字幕在低分辨率下会被抹平）
BX, BY = 32, 18           # 分块数（每块 10×10 像素）
SR = 8000                 # 声音比对采样率
FRAME_GLOBAL_MAX = 0.03   # 整体平均差上限（0–1）；现有流程一方实测最大 0.0015
FRAME_BLOCK_MAX = 0.035   # 最大块差上限；现有流程一方 0.0068、CRF28 重编码 0.0177；20px 半透明角标 ≥0.05、36px 字幕 0.19
FRAME_RUN = 3             # 连续或同一位置这么多个采样帧（4 fps）超限才判不合规
AUDIO_MIN_CORR = 0.95     # 声音窗口最低相关；实测 5% 分位 0.994，跨切点的单个窗口会掉
AUDIO_RUN = 3             # 连续这么多个低窗口（≥1 秒）才判不合规
AUDIO_RMS_EXCESS = 1.25   # 按草稿重建时，成片窗口能量超过应有能量的倍数即判叠加了别的声音
SILENCE_RMS = 0.003
FORBIDDEN_KEYS = ("transition", "effect", "filter", "font", "animation", "template", "sticker", "background.image")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    r = subprocess.run(cmd, capture_output=True, **kw)
    if r.returncode:
        err = r.stderr.decode("utf-8", "replace") if isinstance(r.stderr, bytes) else r.stderr
        raise SystemExit(f"命令失败：{' '.join(cmd[:6])}…\n{err[-800:]}")
    return r


def duration(p: Path) -> float:
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], text=True)
    return float(r.stdout.strip())


def frames(p: Path, fps: float | None, w: int = W, h: int = H) -> np.ndarray:
    vf = (f"fps={fps}," if fps else "") + f"scale={w}:{h}:flags=area,format=gray"
    raw = run(["ffmpeg", "-v", "error", "-i", str(p), "-vf", vf, "-f", "rawvideo", "-"]).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w)


def audio(p: Path) -> np.ndarray:
    raw = run(["ffmpeg", "-v", "error", "-i", str(p), "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]).stdout
    return np.frombuffer(raw, np.float32).copy()


def load(test: Path) -> dict:
    return json.loads((test / "pool.json").read_text(encoding="utf-8"))


def save(test: Path, data: dict) -> None:
    (test / "pool.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------- pool ----------
def cmd_pool(a: argparse.Namespace) -> None:
    test, cut_path = a.test.resolve(), a.cut.resolve()
    cut = json.loads(cut_path.read_text(encoding="utf-8"))
    scene = cut_path.parents[2]
    (test / "pool").mkdir(parents=True, exist_ok=True)
    (test / "arms").mkdir(exist_ok=True)
    clips, seen = [], {}
    for ev in cut["events"]:
        if ev["sha256"] in seen:
            continue
        base = scene / ("groups/" + ev["group"] if ev.get("group") else "shots/" + ev["shot"]) / "renders" / ev["take"]
        src = next(base.glob("*.mp4"))
        if sha256(src) != ev["sha256"]:
            raise SystemExit(f"素材指纹不符：{src}")
        name = f"clip_{len(clips) + 1:02d}"
        shutil.copy2(src, test / "pool" / f"{name}.mp4")
        seen[ev["sha256"]] = name
        clips.append({"name": name, "file": f"pool/{name}.mp4", "sha256": ev["sha256"], "source": str(src.relative_to(REPO)),
                      "duration_s": round(duration(src), 3), "vid": None})
    clean = cut_path.parent / cut["output"]["files"]["clean"]["path"]
    if sha256(clean) != cut["output"]["files"]["clean"]["sha256"]:
        raise SystemExit(f"现有流程成片与剪辑决定的指纹不符：{clean}")
    shutil.copy2(clean, test / "arms" / "pipeline.mp4")
    save(test, {"created": datetime.now().isoformat(timespec="seconds"), "cut": str(cut_path.relative_to(REPO)),
                "clips": clips, "arms": {"pipeline": {"file": "arms/pipeline.mp4", "sha256": sha256(clean),
                                                      "source": str(clean.relative_to(REPO))}}})
    print(f"素材池 {len(clips)} 条 → {test / 'pool'}；现有流程一方 → arms/pipeline.mp4")


def cmd_set_vid(a: argparse.Namespace) -> None:
    data = load(a.test)
    clip = next((c for c in data["clips"] if c["name"] == a.clip), None)
    if not clip:
        raise SystemExit(f"素材池没有 {a.clip}")
    clip["vid"] = a.vid
    save(a.test, data)
    print(f"{a.clip} → vid://{a.vid}")


# ---------- check ----------
def check_draft(draft: dict, vids: set[str], clips: list[dict] | None = None) -> tuple[list[str], list[str], dict[str, str]]:
    """返回（问题、提示、vid→素材名）。CapCut AI 粗剪会把上传的素材另存一份、换一个 vid（2026-11-09 实测）：
    不在上传记录里的 vid，若它被用到的最远位置与某条素材的时长相差 ≤0.1 秒，先按副本归过去记提示，
    再由画面与按草稿重建的声音核对内容；对不上任何素材才算问题。"""
    problems: list[str] = []
    warnings: list[str] = []
    alias: dict[str, str] = {c["vid"]: c["name"] for c in (clips or []) if c.get("vid")}
    reach: dict[str, float] = {}
    for seg in draft.get("segments", []):
        src = (seg.get("attributes") or {}).get("source", "")
        if isinstance(src, str) and src.startswith("vid://"):
            reach[src[6:]] = max(reach.get(src[6:], 0.0), float(seg["attributes"].get("end.ms", 0)) / 1000)
    for v, end in reach.items():
        if v in alias or not clips:
            continue
        near = [c for c in clips if abs(c["duration_s"] - end) <= 0.1]
        if len(near) == 1:
            alias[v] = near[0]["name"]
            warnings.append(f"草稿：vid {v} 不在上传记录里，用到 {end:.3f} 秒，与 {near[0]['name']}（{near[0]['duration_s']} 秒）"
                            f"时长相符，按 CapCut 内部副本处理；内容由画面与声音核对")

    def walk(node, path: str) -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                lk = k.lower()
                if any(f in lk for f in FORBIDDEN_KEYS) and v not in (None, "", 0, False, [], {}):
                    problems.append(f"{path}.{k} = {str(v)[:80]}（CapCut 素材字段）")
                walk(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]")
        elif isinstance(node, str) and "://" in node[:12]:
            scheme, _, rest = node.partition("://")
            if scheme != "vid":
                problems.append(f"{path} = {node[:80]}（非自备来源 {scheme}://）")
            elif rest not in vids and rest not in alias:
                problems.append(f"{path} = {node[:80]}（vid 既不在上传记录里，也对不上任何素材的时长）")

    for seg in draft.get("segments", []):
        t = seg.get("type")
        if t not in {"DRAFT", "VIDEO", "AUDIO"}:
            problems.append(f"片段 {seg.get('id')} 类型 {t}（只许 DRAFT / VIDEO / AUDIO）")
    walk(draft, "$")
    return problems, warnings, alias


def best_frame(out: np.ndarray, pool: np.ndarray, out_hi: np.ndarray, pool_hi: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    of = out.reshape(len(out), -1).astype(np.float32) / 255.0
    pf = pool.reshape(len(pool), -1).astype(np.float32) / 255.0
    best_g, best_i = np.empty(len(out), np.float32), np.empty(len(out), np.int64)
    for s in range(0, len(of), 32):
        d = np.abs(of[s:s + 32, None, :] - pf[None, :, :]).mean(-1)
        best_i[s:s + 32], best_g[s:s + 32] = d.argmin(1), d.min(1)
    # 被测方帧率与素材不同（CapCut 出 30 fps，素材 24 fps）时，采样帧落在两帧之间，运动部位会有偏差：
    # 取最佳帧与前后各一帧里块差最小的（2026-11-09）。外加的文字、角标在相邻帧里同样存在，不受影响。
    # 转帧率也可能把相邻两帧混合成一帧，所以相邻两帧的平均也算候选。
    blocks = np.full(len(out), np.inf, np.float32)
    where = np.zeros(len(out), np.int64)        # 最大块差所在的块编号
    off_seen = False
    last = len(pool) - 1
    for a_off, b_off in ((-1, -1), (0, 0), (1, 1), (-1, 0), (0, 1)):
        ja, jb = np.clip(best_i + a_off, 0, last), np.clip(best_i + b_off, 0, last)
        ref = (pool_hi[ja].astype(np.float32) + pool_hi[jb].astype(np.float32)) / 2
        diff = np.abs(out_hi.astype(np.float32) - ref) / 255.0
        per = diff.reshape(len(out), BY, HH // BY, BX, HW // BX).mean((2, 4)).reshape(len(out), -1)
        better = per.max(1) < blocks
        where = np.where(better, per.argmax(1), where) if off_seen else per.argmax(1)
        blocks = np.minimum(blocks, per.max(1))
        off_seen = True
    return best_g, blocks, best_i, where


def audio_corr(out: np.ndarray, pools: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    win, hop = SR // 2, SR // 4
    starts = np.arange(0, max(len(out) - win, 0) + 1, hop)
    score = np.full(len(starts), np.nan, np.float32)
    rms = np.array([np.sqrt(np.mean(out[s:s + win] ** 2)) for s in starts])
    prepared = []
    for src in pools:
        n = 1 << int(np.ceil(np.log2(len(src) + win)))
        c2 = np.concatenate([[0.0], np.cumsum(src.astype(np.float64) ** 2)])
        prepared.append((np.fft.rfft(src, n), n, np.sqrt(np.maximum(c2[win:] - c2[:-win], 1e-12)), len(src)))
    for k, s in enumerate(starts):
        if rms[k] < SILENCE_RMS:
            continue
        w = out[s:s + win] - 0.0
        wn = np.linalg.norm(w)
        best = 0.0
        for spec, n, local, L in prepared:
            if L < win:
                continue
            c = np.fft.irfft(spec * np.conj(np.fft.rfft(w, n)), n)[: L - win + 1]
            best = max(best, float((c / (local * wn)).max()))
        score[k] = best
    return starts / SR, score


def clip_audio(p: Path, ss: float, t: float, vol: float = 1.0) -> np.ndarray:
    raw = run(["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{t:.3f}", "-i", str(p), "-vn",
               "-af", f"volume={vol}", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def draft_audio(video: Path, draft: dict, alias: dict[str, str], test: Path, data: dict) -> dict | None:
    """按草稿逐段把素材原声（乘片段音量）按时间戳对齐，与成片同位置比对。比在素材池里任找最像的一段更严：
    每个窗口必须正好来自草稿写的那一段。草稿有独立音频片段或变速时返回 None，退回素材池搜索。"""
    segs = [x for x in draft.get("segments", []) if x.get("type") in ("VIDEO", "AUDIO")]
    if any(x["type"] == "AUDIO" for x in segs) or any("speed" in (x.get("attributes") or {}) for x in segs):
        return None
    files = {c["name"]: test / c["file"] for c in data["clips"]}
    win, hop = SR // 2, SR // 4
    total = duration(video)
    covered = np.zeros(int(total * SR) + 1, bool)
    windows: list[tuple[float, float, float]] = []      # (成片时间, 相关, 能量比)
    for x in segs:
        at, tl = x["attributes"], x["timeline"]
        src = at.get("source", "")
        name = alias.get(src[6:]) if src.startswith("vid://") else None
        if name is None:
            return None
        t0, d = tl["start.ms"] / 1000, tl["duration.ms"] / 1000
        c = clip_audio(video, t0, d)
        s = clip_audio(files[name], at.get("start.ms", 0) / 1000, d, float(at.get("volume", 1)))
        n = min(len(c), len(s))
        covered[int(t0 * SR): int(t0 * SR) + n] = True
        for i in range(0, n - win + 1, hop):
            u, v = c[i:i + win], s[i:i + win]
            ru = np.sqrt(np.mean(u ** 2))
            if ru < SILENCE_RMS:
                continue
            rv = np.sqrt(np.mean(v ** 2))
            windows.append((round(t0 + i / SR, 2), float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v) + 1e-12)),
                            float(ru / (rv + 1e-12))))
    full = audio(video)
    gaps = [round(k / SR, 2) for k in range(0, len(full) - win + 1, hop)
            if not covered[k:k + win].any() and np.sqrt(np.mean(full[k:k + win] ** 2)) >= SILENCE_RMS]
    return {"windows": windows, "uncovered_loud_s": gaps}


def cmd_check(a: argparse.Namespace) -> None:
    test = a.test.resolve()
    data = load(test)
    video = a.video.resolve()
    name = a.name or video.stem
    report: dict = {"video": str(video), "sha256": sha256(video), "duration_s": round(duration(video), 3),
                    "checked": datetime.now().isoformat(timespec="seconds"), "problems": [], "warnings": []}
    draft, alias = None, {}
    if a.draft:
        vids = {c["vid"] for c in data["clips"] if c.get("vid")}
        draft = json.loads(a.draft.read_text(encoding="utf-8"))
        report["draft"] = {"file": str(a.draft.resolve()), "sha256": sha256(a.draft)}
        probs, warns, alias = check_draft(draft, vids, data["clips"])
        report["problems"] += [f"草稿：{p}" for p in probs]
        report["warnings"] += warns

    pool_files = [test / c["file"] for c in data["clips"]]
    pool_frames = np.concatenate([frames(p, None) for p in pool_files])
    pool_hi = np.concatenate([frames(p, None, HW, HH) for p in pool_files])
    out = frames(video, 4)
    out_hi = frames(video, 4, HW, HH)
    g, b, best_i, where = best_frame(out, pool_frames, out_hi, pool_hi)
    bad = [i for i in range(len(out)) if g[i] > FRAME_GLOBAL_MAX or b[i] > FRAME_BLOCK_MAX]
    report["frames"] = {"sampled": len(out), "global_p95": round(float(np.percentile(g, 95)), 4),
                        "global_max": round(float(g.max()), 4), "block_p95": round(float(np.percentile(b, 95)), 4),
                        "block_max": round(float(b.max()), 4), "flagged_s": [round(i / 4, 2) for i in bad]}
    # 外加的文字、角标、贴纸会持续：连续 FRAME_RUN 个采样帧超限，或同一块在 FRAME_RUN 帧以上超限，才判不合规；
    # 零散的单帧（转帧率插出的中间帧、运动部位）只提示，并存对比图给人看（2026-11-09）。
    runs, cur = [], []
    for i in range(len(out)):
        if i in bad:
            cur.append(i)
        else:
            if cur: runs.append(cur)
            cur = []
    if cur: runs.append(cur)
    same_block = {}
    for i in bad:
        same_block.setdefault(int(where[i]), []).append(i)
    persistent = [r for r in runs if len(r) >= FRAME_RUN] + [v for v in same_block.values() if len(v) >= FRAME_RUN]
    if bad and g.max() > FRAME_GLOBAL_MAX:
        report["problems"].append(f"画面：整帧对不上素材池，时间点 {[round(i / 4, 2) for i in bad if g[i] > FRAME_GLOBAL_MAX][:20]}")
    if persistent:
        report["problems"].append(f"画面：{len(persistent)} 处持续的局部差异（可能是文字、角标、贴纸、特效），"
                                  f"时间点 {[[round(r[0] / 4, 2), round(r[-1] / 4 + 0.25, 2)] for r in persistent][:20]}")
    elif bad:
        from PIL import Image
        (test / "check").mkdir(exist_ok=True)
        img = test / "check" / f"{name}_flagged_frames.png"
        rows = [np.hstack([out_hi[i], pool_hi[best_i[i]], np.clip(np.abs(out_hi[i].astype(int) - pool_hi[best_i[i]].astype(int)) * 6, 0, 255).astype(np.uint8)])
                for i in bad[:8]]
        Image.fromarray(np.vstack(rows)).save(img)
        report["warnings"].append(f"画面：{len(bad)} 个零散采样帧局部超限（不连续、不在同一位置），时间点 {report['frames']['flagged_s'][:20]}；"
                                  f"对比图 check/{img.name}（左成片、中最近素材帧、右差异×6）")

    da = draft_audio(video, draft, alias, test, data) if draft else None
    rms_ratio: list[float] = []
    if da is not None:
        w = da["windows"]
        t = np.array([x[0] for x in w]); s = np.array([x[1] for x in w], np.float32)
        rms_ratio = [x[2] for x in w]
        loud = [x[0] for x in w if x[2] > AUDIO_RMS_EXCESS]
        report["audio_method"] = "按草稿逐段重建（时间戳对齐，含片段音量）"
        if loud:
            report["problems"].append(f"声音：{len(loud)} 个窗口比草稿应有的声音响 {AUDIO_RMS_EXCESS} 倍以上（疑似叠加了别的声音），时间点 {loud[:20]}")
        if da["uncovered_loud_s"]:
            report["problems"].append(f"声音：草稿片段之外仍有声音，时间点 {da['uncovered_loud_s'][:20]}")
    else:
        t, s = audio_corr(audio(video), [audio(p) for p in pool_files])
        report["audio_method"] = "在素材池里搜最相似的片段"
    low = [round(float(t[i]), 2) for i in range(len(s)) if not np.isnan(s[i]) and s[i] < AUDIO_MIN_CORR]
    valid = s[~np.isnan(s)]
    report["audio"] = {"windows": int(len(valid)), "corr_p05": round(float(np.percentile(valid, 5)), 4) if len(valid) else None,
                       "corr_min": round(float(valid.min()), 4) if len(valid) else None, "flagged_s": low}
    if rms_ratio:
        report["audio"]["rms_ratio_range"] = [round(min(rms_ratio), 3), round(max(rms_ratio), 3)]
    runs, cur = [], []
    for i in range(len(s)):
        if not np.isnan(s[i]) and s[i] < AUDIO_MIN_CORR:
            cur.append(round(float(t[i]), 2))
        else:
            if cur: runs.append(cur)
            cur = []
    if cur: runs.append(cur)
    long_runs = [r for r in runs if len(r) >= AUDIO_RUN]   # 跨切点的窗口最多连着 2 个
    report["audio"]["runs"] = [[r[0], r[-1] + 0.5] for r in runs]
    if long_runs:
        report["problems"].append(f"声音：{len(long_runs)} 段连续 1 秒以上与素材池音轨对不上（可能混入音乐、音效或改了声音），"
                                  f"区间 {[[r[0], r[-1] + 0.5] for r in long_runs][:20]}")
    elif low:
        report["warnings"].append(f"声音：{len(runs)} 处短暂偏低 {low[:20]}（多在切点上），人耳确认")
    report["pass"] = not report["problems"]
    (test / "check").mkdir(exist_ok=True)
    (test / "check" / f"{name}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    data.setdefault("arms", {}).setdefault(name, {}).update(file=str(video.relative_to(test)) if video.is_relative_to(test) else str(video),
                                                             sha256=report["sha256"], check=f"check/{name}.json", check_pass=report["pass"])
    save(test, data)
    print(json.dumps({k: report.get(k) for k in ("pass", "problems", "warnings", "frames", "audio_method", "audio")}, ensure_ascii=False, indent=2))


# ---------- blind ----------
def normalize(src: Path, dst: Path) -> None:
    run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-map_metadata", "-1", "-map_chapters", "-1",
         "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p",
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000",
         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
         "-fflags", "+bitexact", "-flags:v", "+bitexact", "-flags:a", "+bitexact", str(dst)])


def cmd_blind(a: argparse.Namespace) -> None:
    test = a.test.resolve()
    data = load(test)
    arms = data.get("arms", {})
    if set(arms) != {"pipeline", "capcut"}:
        raise SystemExit(f"需要 pipeline 与 capcut 两方，现有：{sorted(arms)}")
    for k, v in arms.items():
        if not v.get("check_pass"):
            raise SystemExit(f"{k} 没有通过合规机检（check/{k}.json），不能进盲审")
        if sha256(test / v["file"]) != v["sha256"]:
            raise SystemExit(f"{k} 成片在机检后改过，重跑 check")
    order = ["pipeline", "capcut"]
    random.SystemRandom().shuffle(order)
    (test / "blind").mkdir(exist_ok=True)
    key = {"salt": secrets.token_hex(16), "A": order[0], "B": order[1], "made": datetime.now().isoformat(timespec="seconds")}
    for label, arm in zip("AB", order):
        dst = test / "blind" / f"{label}.mp4"
        normalize(test / arms[arm]["file"], dst)
        key[f"{label}_sha256"] = sha256(dst)
    blob = json.dumps(key, sort_keys=True)
    commit = hashlib.sha256(blob.encode()).hexdigest()
    (test / "_key_do_not_open.json").write_text(blob + "\n", encoding="utf-8")
    data["blind"] = {"commitment": commit, "A_sha256": key["A_sha256"], "B_sha256": key["B_sha256"],
                     "normalize": "1280x720 24fps H.264 CRF18；loudnorm -16 LUFS；去元数据"}
    save(test, data)
    print(f"盲化完成：blind/A.mp4、blind/B.mp4；钥匙承诺 sha256 {commit}（钥匙文件人审结束前不要打开）")


# ---------- review ----------
def sheet(video: Path, out: Path, every: float = 1.0) -> list[Path]:
    from PIL import Image, ImageDraw
    tmp = Path(tempfile.mkdtemp())
    run(["ffmpeg", "-v", "error", "-i", str(video), "-vf", f"fps=1/{every},scale=320:180", str(tmp / "f_%04d.png")])
    shots = sorted(tmp.glob("f_*.png"))
    pages, per = [], 30
    for p in range(0, len(shots), per):
        chunk = shots[p:p + per]
        page = Image.new("RGB", (6 * 320, ((len(chunk) + 5) // 6) * 200), "black")
        for i, f in enumerate(chunk):
            im = Image.open(f)
            x, y = (i % 6) * 320, (i // 6) * 200
            page.paste(im, (x, y))
            ImageDraw.Draw(page).text((x + 4, y + 182), f"{(p + i) * every:.0f}s", fill="white")
        dst = out.with_name(f"{out.stem}_p{p // per + 1}.png")
        page.save(dst)
        pages.append(dst)
    shutil.rmtree(tmp, ignore_errors=True)
    return pages


def cuts(video: Path) -> list[float]:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(video), "-vf", "select='gt(scene,0.3)',showinfo", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return [round(float(line.split("pts_time:")[1].split()[0]), 2) for line in r.stderr.splitlines() if "pts_time:" in line]


def transcript(video: Path) -> list[dict]:
    from faster_whisper import WhisperModel
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(str(video), language="en", word_timestamps=True, vad_filter=False,
                               condition_on_previous_text=False)     # 与 scene_cut.py annotate 同设置
    lines = []
    for s in segs:                   # 段级时间不准，用首末词的时间
        words = s.words or []
        if words:
            lines.append({"start": round(words[0].start, 2), "end": round(words[-1].end, 2), "text": s.text.strip()})
    return lines


RUBRIC = """你是资深剧集剪辑师，做盲审。两个版本 A、B 用的是同一组素材、同一份说明，只有剪法不同；你不知道哪个是谁剪的，也不要猜。
材料：说明（brief.md）、每个版本的分页联系表（每秒一帧，左下角是秒数）、检测到的切点时间、带时间的台词转写。转写只识别英文，拉丁语台词（Salve、指路的那句）会缺，不要据此判台词被剪掉。你看不到动态和声音，
凡是要靠看动态或听声音才能判断的，写「材料不足」，不要编。

按以下各项给 A、B 各打 1–5 分，并各写一句依据（引用秒数或台词）：
1. vision：是否满足说明里的 Vision（像自己去过那里、亲眼看见那一天的生活）
2. story：这场戏的事件顺序是否清楚，观众看得懂发生了什么
3. dialogue：台词是否完整，没有被切掉开头或结尾
4. rhythm：节奏，哪里拖、哪里赶
5. cuts：每一刀是否有动机（新信息、反应、视线、动作）
6. ending：场尾是否落在说明要求的点上
最后给 overall 偏好：A / B / 持平，以及最关键的一条理由。

只输出一个 JSON 对象，不要别的文字：
{"scores": {"A": {"vision": n, "story": n, "dialogue": n, "rhythm": n, "cuts": n, "ending": n}, "B": {...}},
 "notes": {"A": {"vision": "…", …}, "B": {…}}, "overall": "A|B|持平", "reason": "…"}"""


def cmd_review(a: argparse.Namespace) -> None:
    test = a.test.resolve()
    data = load(test)
    if "blind" not in data:
        raise SystemExit("先 blind")
    mat = test / "review" / "materials"
    mat.mkdir(parents=True, exist_ok=True)
    pack: dict[str, dict] = {}
    for label in "AB":
        v = test / "blind" / f"{label}.mp4"
        pages = sheet(v, mat / f"{label}_sheet.png")
        pack[label] = {"pages": pages, "cuts": cuts(v), "transcript": transcript(v), "duration_s": round(duration(v), 2)}
    brief = (test / "brief_en.md").read_text(encoding="utf-8")
    results = []
    for who in a.reviewer:
        for swap in (False, True):          # 正反各一次，抵消先后位置偏差
            show = ["B", "A"] if swap else ["A", "B"]
            work = Path(tempfile.mkdtemp(prefix="blind_review_"))
            images: list[str] = []
            text = [RUBRIC, "", "## brief.md", brief]
            for shown, real in zip("AB", show):
                info = pack[real]
                text += [f"## 版本 {shown}", f"时长 {info['duration_s']} 秒；切点（秒）{info['cuts']}",
                         "台词转写：" + json.dumps(info["transcript"], ensure_ascii=False)]
                for i, pg in enumerate(info["pages"]):
                    dst = work / f"{shown}_p{i + 1}.png"
                    shutil.copy(pg, dst)
                    images.append(dst.name)
                text.append(f"联系表图片：{', '.join(n for n in images if n.startswith(shown))}")
            prompt = "\n".join(text)
            if a.dry_run:
                (test / "review" / f"prompt_{who}{'_swap' if swap else ''}.md").write_text(prompt, encoding="utf-8")
                shutil.rmtree(work, ignore_errors=True)
                continue
            if who == "codex":
                last = work / "_last.txt"
                cmd = ["codex", "exec", "--skip-git-repo-check", "-s", "read-only", "-o", str(last)]
                for n in images:
                    cmd += ["-i", n]
                subprocess.run(cmd, input=prompt, cwd=work, capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=a.timeout, shell=os.name == "nt")
                raw = last.read_text(encoding="utf-8") if last.exists() else ""
            else:
                reads = "、".join(str(work / n) for n in images)
                r = subprocess.run(["claude", "-p", "--output-format", "text", "--allowedTools", "Read", "--add-dir", str(work)],
                                   input=f"先用 Read 工具逐张读取图片：{reads}。\n{prompt}", cwd=work, capture_output=True,
                                   text=True, encoding="utf-8", errors="replace", timeout=a.timeout, shell=os.name == "nt")
                raw = r.stdout
            parsed = None
            try:
                parsed = json.loads(raw[raw.index("{"): raw.rindex("}") + 1])
                if swap:                     # 换回真实标签
                    for field in ("scores", "notes"):
                        if field in parsed:
                            parsed[field] = {"A": parsed[field].get("B"), "B": parsed[field].get("A")}
                    parsed["overall"] = {"A": "B", "B": "A"}.get(parsed.get("overall"), parsed.get("overall"))
            except ValueError:
                pass
            results.append({"reviewer": who, "swapped": swap, "parsed": parsed, "raw": raw})
            shutil.rmtree(work, ignore_errors=True)
    if a.dry_run:
        print(f"只写了材料与提示词：{test / 'review'}")
        return
    out = test / "review" / "model_reviews.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for r in results:
        p = r["parsed"] or {}
        print(f"{r['reviewer']}{'（换位）' if r['swapped'] else ''}：偏好 {p.get('overall', '解析失败')} — {p.get('reason', '')[:120]}")


def cmd_reveal(a: argparse.Namespace) -> None:
    test = a.test.resolve()
    data = load(test)
    sheet_md = test / "scoresheet.md"
    if "待填" in sheet_md.read_text(encoding="utf-8") and not a.force:
        raise SystemExit("人审表还有「待填」；填完再揭盲（或 --force）")
    blob = (test / "_key_do_not_open.json").read_text(encoding="utf-8").strip()
    if hashlib.sha256(blob.encode()).hexdigest() != data["blind"]["commitment"]:
        raise SystemExit("钥匙文件与盲化时的承诺不符，结果作废")
    key = json.loads(blob)
    data["reveal"] = {"A": key["A"], "B": key["B"], "time": datetime.now().isoformat(timespec="seconds")}
    save(test, data)
    print(f"A = {key['A']}，B = {key['B']}")
    rev = test / "review" / "model_reviews.json"
    if rev.is_file():
        for r in json.loads(rev.read_text(encoding="utf-8")):
            o = (r["parsed"] or {}).get("overall")
            print(f"  {r['reviewer']}{'（换位）' if r['swapped'] else ''}：偏好 {o} → {key.get(o, o)}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("pool"); s.add_argument("test", type=Path); s.add_argument("--cut", type=Path, required=True)
    s = sub.add_parser("set-vid"); s.add_argument("test", type=Path); s.add_argument("clip"); s.add_argument("vid")
    s = sub.add_parser("check"); s.add_argument("test", type=Path); s.add_argument("video", type=Path)
    s.add_argument("--draft", type=Path); s.add_argument("--name")
    s = sub.add_parser("blind"); s.add_argument("test", type=Path)
    s = sub.add_parser("review"); s.add_argument("test", type=Path)
    s.add_argument("--reviewer", nargs="+", default=["claude", "codex"], choices=["claude", "codex"])
    s.add_argument("--timeout", type=int, default=900)
    s.add_argument("--dry-run", action="store_true", help="只生成材料与提示词，不调审稿人")
    s = sub.add_parser("reveal"); s.add_argument("test", type=Path); s.add_argument("--force", action="store_true")
    a = p.parse_args(argv)
    {"pool": cmd_pool, "set-vid": cmd_set_vid, "check": cmd_check, "blind": cmd_blind,
     "review": cmd_review, "reveal": cmd_reveal}[a.cmd](a)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
