# -*- coding: utf-8 -*-
"""排行榜批量渲染队列（follow-up 046 / 047）：脱离会话独立运行，逐条落盘、可续跑。

    python ai_videos/paihangbang/_tools/render_queue.py <jobs.json> [--workers 3] [--send]

每条：（中文版）等翻译完成 → merge → gate（不过就跳过并报告）→ 渲静音片到 render/_silent/ →
把该期 render/_audio/<ep>_music.m4a 原样装回（时长差 > 0.2 s 不装、报告）→ 写到正式文件名 →（--send）压 720p 发给用户。
已有正式文件且比 data 新的跳过（续跑）。状态逐行写 render/_queue.log。
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import threading
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
EPS = REPO / "ai_videos" / "paihangbang" / "episodes"
RS = REPO / "projects" / "rank_scroll"
TOOLS = REPO / "ai_videos" / "paihangbang" / "_tools"
LOG = EPS.parent / "_tools" / "render_queue.log"
MUSIC_LOCK = threading.Lock()


def log(msg: str) -> None:
    line = f"{time.strftime('%m-%d %H:%M:%S')} {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def run(argv: list[str], cwd: Path = REPO) -> subprocess.CompletedProcess:
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def duration(p: Path) -> float:
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)])
    return float(r.stdout.strip() or 0)


def rebuild_music(ep: Path, name: str, dur: float, audio: Path) -> str:
    """用该期母版 manifest 记的 Suno 曲目（含入出点）重建配乐床，--music-fit end（末曲从头部裁，自然收尾），写回 _audio。
    中文版没有自己的 manifest 就用英文版的（两版同一首配乐）。返回说明文字。"""
    mans = [ep / "render" / f"{name}.manifest.json", ep / "render" / f"{ep.name}_master.manifest.json"]
    man = next((m for m in mans if m.is_file()), None)
    if man is None:
        return "没有 manifest，未重建"
    specs = []
    for t in json.loads(man.read_text(encoding="utf-8")).get("inputs", {}).get("music") or []:
        raw = Path(t["path"])
        cands = [raw] if raw.is_absolute() else [REPO / raw, RS / raw, ep / raw, ep.parent / raw, ep / "render" / raw]
        p = next((c.resolve() for c in cands if c.is_file()), None)
        if p is None:
            return f"曲目找不到：{t['path']}"
        a, b = t.get("in_s"), t.get("out_s")
        specs.append(f"{p}@{a or 0}:{b}" if b else (f"{p}@{a}" if a else str(p)))
    if not specs:
        return "manifest 里没有配乐曲目"
    sys.path.insert(0, str(RS))
    from rank_scroll.render import build_music_bed
    wav = audio.with_suffix(".rebuild.wav")
    build_music_bed(specs, dur, 0.0, dur, "end", wav, log=lambda *_: None)
    audio.parent.mkdir(parents=True, exist_ok=True)
    if audio.exists():
        audio.replace(audio.with_name(audio.stem + f".before_{int(time.time())}.m4a"))
    r = run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-c:a", "aac", "-b:a", "192k", str(audio)])
    wav.unlink(missing_ok=True)
    return "ok" if r.returncode == 0 else r.stderr[-200:]


def job(j: dict, send: bool, tmp: Path) -> None:
    ep, lang, risk = EPS / j["ep"], j["lang"], j["risk"]
    name = f"{j['ep']}_master" + ("_with-risk-images" if risk else "") + ("" if lang == "en" else f"_{lang}")
    final = ep / "render" / f"{name}.mp4"
    data = ep / ("data.json" if lang == "en" else "data.zh.json")
    tag = f"{j['ep']} [{lang}{' 带风险图' if risk else ''}]"
    if lang == "zh":
        tr = ep / "_build" / "zh" / "translation.json"
        for _ in range(180):                               # 最多等 90 分钟翻译
            if tr.exists():
                break
            time.sleep(30)
        if not tr.exists():
            log(f"✗ {tag} 翻译未完成，跳过"); return
        run([sys.executable, str(TOOLS / "zh_edition.py"), "merge", str(ep)])
        g = run([sys.executable, str(TOOLS / "zh_edition.py"), "gate", str(ep)])
        if g.returncode:
            log(f"✗ {tag} 合规闸门未过，不渲染：{g.stdout.strip()[-400:]}"); return
    if final.exists() and final.stat().st_mtime > data.stat().st_mtime and not j.get("force"):
        log(f"= {tag} 已是最新，跳过渲染")
    else:
        silent = ep / "render" / "_silent" / f"{name}.mp4"
        silent.parent.mkdir(parents=True, exist_ok=True)
        argv = [sys.executable, "-m", "rank_scroll", "render", str(ep), "--lang", lang, "--out", str(silent)] + (["--allow-risk-images"] if risk else [])
        log(f"▶ {tag} 开始渲染")
        r = run(argv, cwd=RS)
        if r.returncode or not silent.exists():
            log(f"✗ {tag} 渲染失败：{(r.stderr or r.stdout)[-400:]}"); return
        audio = ep / "render" / "_audio" / f"{j['ep']}_music.m4a"
        dv = duration(silent)
        with MUSIC_LOCK:                                         # 中英文两路共用一条 _audio，串行重建
            if not (audio.exists() and abs(duration(audio) - dv) <= 0.2):
                rebuilt = rebuild_music(ep, name, dv, audio)    # 时长变了（如 follow-up 068 改滚动速度）：按 manifest 曲目重裁
                log(f"  ↺ {tag} 配乐按 manifest 曲目重裁到 {dv:.1f}s：{rebuilt}")
        if audio.exists() and abs(duration(audio) - dv) <= 0.2:
            m = run(["ffmpeg", "-v", "error", "-y", "-i", str(silent), "-i", str(audio), "-map", "0:v", "-map", "1:a", "-c", "copy",
                     "-movflags", "+faststart", str(final)])
            if m.returncode:
                log(f"✗ {tag} 装配乐失败：{m.stderr[-300:]}"); return
            log(f"✓ {tag} 完成（{dv:.1f}s，配乐已装）→ {final.name}")
        else:
            final.write_bytes(silent.read_bytes())
            log(f"! {tag} 完成但未装配乐（时长 {dv:.1f}s 与音轨 {duration(audio) if audio.exists() else '缺失'} 不符）→ {final.name}")
    if send:
        mp4 = tmp / f"{name}_720p.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-i", str(final), "-vf", "scale=1280:720,fps=30", "-c:v", "libx264", "-preset", "medium",
             "-b:v", "500k", "-maxrate", "800k", "-bufsize", "1600k", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(mp4)])
        z = tmp / f"{name}_720p.zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_STORED) as f:
            f.write(mp4, mp4.name)
        title = json.loads(data.read_text(encoding="utf-8")).get("title", "")
        d = duration(final)
        msg = f"{'中文版' if lang == 'zh' else '英文修正版'} · {j['ep']} · {title}（{int(d // 60)}:{int(d % 60):02d}{'，带风险图版' if risk else ''}）"
        r = run(["cc-connect", "send", "--message", msg, "--file", str(z)])
        log(f"  ↳ 已发送 {z.name}：{(r.stdout + r.stderr).strip()[-40:]}")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("jobs")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--send", action="store_true")
    a = ap.parse_args()
    jobs = json.loads(Path(a.jobs).read_text(encoding="utf-8"))
    tmp = Path(a.jobs).parent / "_send"
    tmp.mkdir(exist_ok=True)
    log(f"队列开始：{len(jobs)} 条，{a.workers} 路并行")
    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(lambda j: _safe(j, a.send, tmp), jobs))
    log("队列结束")


def _safe(j, send, tmp):
    try:
        job(j, send, tmp)
    except Exception as e:  # noqa: BLE001 —— 一条失败不影响其余
        log(f"✗ {j} 异常：{e}")


if __name__ == "__main__":
    main()
