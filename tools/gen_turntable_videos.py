# -*- coding: utf-8 -*-
"""人物卡的建立视频（turntable）出片：卡里 turntable prompt + 立绘（+ 叫声参考录音）→ 即梦「全能参考」。任一部剧通用。

prompt 在卡里（`## turntable 说明` 的 ```text 块，首行 `{卡目录}_turntable`；szzl 由 `tools/gen_turntables_szzl.py` 生成），
本文件只负责出片；画幅与时长读该块的「比例：画幅 X:Y，时长 N 秒」（或「画幅: X:Y ｜ 时长: Ns」）行，落盘名 ＝ 首行。
走 `dreamina multimodal2video` 而不是 image2video：非人生物要挂**声音参考**（卡里 `## 叫声设计` + `ref/audio/*.mp3`），只有全能参考收音频。

`参考:` 行按上传顺序把 `=>@` 填成 `@图片1 / @音频1…`（同 `seedance_kit.py`；正本卡里仍是裸 `=>@`，rule 12.4-C）。
立绘缺失时依次退：views 锚点正面帧（`gen_char_images.anchor_frame`）→ 从文件夹里最新的原始建立视频 0.5 s 处截一帧。
新片落盘后，同一文件夹里旧的原始建立视频挪进 `ai_videos/_deleted/`（与 webapp 软删同一处），webapp 始终只看到一条。

用法（仓库根目录；一般经 `tools/char_assets.py` 调用）：
    python tools/gen_turntable_videos.py --drama shengji_zhilu --only m2 --dry-run
    python tools/gen_turntable_videos.py --drama shengji_zhilu --only m2
    python tools/gen_turntable_videos.py --drama shengji_zhilu --cry --force
    python tools/gen_turntable_videos.py --drama shengji_zhilu --harvest     # 把超时没收回的任务收回来
纪律：串行（即梦并发上限）；一部剧同时只许一个进程出片（`.char_assets.lock`，2026-09-30 两会话同出 c25–c34、互相覆盖）；
提交即记账（`.turntable_jobs.json`），账里同卡还有在途 / 已成未收的任务就收那一条、不重提；下载先写 `.part` 再改名。
"""
from __future__ import annotations

import argparse
import ctypes
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from tools import gen_char_images as gci  # noqa: E402  views 锚点帧在哪

DELETED = REPO / "ai_videos" / "_deleted"
CLI = Path.home() / "bin" / "dreamina.exe"
# seedance2.5：CLI 帮助没列、服务端收（2026-09-30 实测，4–30 s）；会员账号 priority 7、零排队，80 分 / 条
MODELS = ("seedance2.5", "seedance2.0", "seedance2.0fast", "seedance2.0_vip", "seedance2.0fast_vip")
RESOLUTION = "720p"
FRONT_S = 0.5
POLL_EVERY = 10
POLL_MAX = 1200
LEDGER = ".turntable_jobs.json"
LOCK = ".char_assets.lock"            # 一部剧同时只许一个进程出人物资产（char_assets.py 整轮持有）
REF_ITEM = re.compile(r"`([^`]+?)=>@`")
SPEC = re.compile(r"^(?:比例|画幅)[:：].*?(\d+:\d+).*?时长[:：]?\s*(\d+)\s*(?:秒|s)", re.M)
REEL = "video.mp4"                     # webapp 截出来的 2 s 片段，不是原始建立视频
QUIET_DB = -50.0                       # 有 `## 叫声设计` 的卡，整条平均响度低于它＝叫声没出来（实测 m6 写「几乎听不见」出片约 −75 dB）
CRY = "## 叫声设计"


def chars_dir(drama: str) -> Path:
    d = REPO / "ai_videos" / drama / "2_世界观人设" / "characters"
    if not d.is_dir():
        raise SystemExit(f"没有 {d.relative_to(REPO)}（--drama 相对 ai_videos/，如 shengji_zhilu、shikong_lvxing/sk2）")
    return d


def creature_sound(d: Path) -> dict | None:
    """非人生物的叫声（szzl follow-up 041）：卡里 `## 叫声设计` 一节是唯一出处；参考录音 ＝ `ref/audio/*.mp3`。
    录音只收许可干净的真实世界录音，文件名带「不挂建立视频」的不挂。"""
    text = (d / (d.name + ".md")).read_text(encoding="utf-8")
    i = text.find(CRY)
    if i < 0:
        return None
    j = text.find("\n## ", i + 1)
    sec = text[i:j if j >= 0 else len(text)]
    field = {k: (re.search(r"^- \*\*%s\*\*[：:](.+)$" % k, sec, re.M) or [None, ""])[1].strip() for k in ("说话", "声音", "负向")}
    if not field["声音"]:
        raise SystemExit("%s：`%s` 一节没有 `- **声音**：` 行" % (d.name, CRY))
    refs = sorted(p for p in (d / "ref" / "audio").glob("*.mp3") if "不挂建立视频" not in p.name)
    return {"speaks": field["说话"].startswith("是"), "sound": field["声音"].removeprefix("声音：").strip(),
            "neg": [n.strip() for n in re.split(r"[，,、]", field["负向"]) if n.strip()], "refs": refs}


def cli(*args: str, timeout: int = 300) -> dict | list | None:
    p = subprocess.run([str(CLI), *args], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    raw = (p.stdout or "") + (p.stderr or "")
    for o, c in (("{", "}"), ("[", "]")):
        i = raw.find(o)
        if i >= 0:
            try:
                return json.loads(raw[i:raw.rfind(c) + 1])
            except json.JSONDecodeError:
                continue
    return None


def originals(d: Path) -> list[Path]:
    """文件夹里的原始建立视频，新的在前。"""
    return sorted((p for p in d.iterdir() if p.is_file() and p.suffix.lower() == ".mp4" and p.name != REEL
                   and not p.name.endswith(".part.mp4")), key=lambda p: -p.stat().st_mtime)


def has_block(d: Path) -> bool:
    text = (d / f"{d.name}.md").read_text(encoding="utf-8")
    return re.search(r"```text\n%s_turntable\n" % re.escape(d.name), text) is not None


def portrait(d: Path) -> Path:
    for p in (d / f"{d.name}.png", gci.anchor_frame(d, "front")):
        if p.is_file():
            return p
    if vids := originals(d):
        out = Path(tempfile.gettempdir()) / "turntable_front" / f"{d.name}_front.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(FRONT_S), "-i", str(vids[0]), "-frames:v", "1", str(out)],
                       check=True)
        return out
    raise SystemExit(f"{d.name}：没有立绘、views 正面帧，也没有旧建立视频可截")


def job(d: Path) -> tuple[str, Path, list[Path], str, str, int]:
    """(落盘 stem, 立绘, 声音参考, 送审 prompt, 画幅, 时长)。"""
    text = (d / f"{d.name}.md").read_text(encoding="utf-8")
    m = re.search(r"```text\n(%s_turntable\n.*?)```" % re.escape(d.name), text, re.S)
    if not m:
        raise SystemExit(f"{d.name}：卡里没有 `{d.name}_turntable` 的 text 块（按 stage2 模板写进卡里）")
    stem, body = m.group(1).rstrip("\n").split("\n", 1)
    spec = SPEC.search(body)
    if not spec:
        raise SystemExit(f"{d.name}：prompt 里没有「比例：画幅 X:Y，时长 N 秒」")
    cry = creature_sound(d)
    audio = cry["refs"][:3] if cry else []
    tags = iter(["@图片1"] + ["@音频%d" % (i + 1) for i in range(len(audio))])
    ref = next((l for l in body.split("\n") if re.match(r"参考[:：]", l)), None)
    if ref is None or len(REF_ITEM.findall(ref)) != 1 + len(audio):
        raise SystemExit(f"{d.name}：参考行要有 {1 + len(audio)} 项 `名字=>@`（立绘 + 叫声录音），实际 {ref!r}")
    body = body.replace(ref, REF_ITEM.sub(lambda x: f"`{x.group(1)}=>{next(tags)}`", ref))
    return stem, portrait(d), audio, body, spec.group(1), int(spec.group(2))


def ledger(chars: Path, sid: str | None = None, key: str | None = None) -> dict[str, str]:
    path = chars / LEDGER
    d = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    if sid and key:
        d[sid] = key
        path.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    return d


def alive(pid: int) -> bool:
    if sys.platform == "win32":        # os.kill(pid, 0) 在 Windows 上是 TerminateProcess，不能拿来探活
        k32 = ctypes.windll.kernel32
        h = k32.OpenProcess(0x1000, False, pid)
        if not h:
            return False
        code = ctypes.c_ulong()
        k32.GetExitCodeProcess(h, ctypes.byref(code))
        k32.CloseHandle(h)
        return code.value == 259       # STILL_ACTIVE
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


class DramaLock:
    """一部剧同时只许一个进程出建立视频；锁主已死就接管。"""

    def __init__(self, chars: Path) -> None:
        self.path = chars / LOCK

    def __enter__(self) -> "DramaLock":
        for _ in range(2):
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(os.getpid()).encode())
                os.close(fd)
                return self
            except FileExistsError:
                pid = int(self.path.read_text(encoding="utf-8").strip() or 0)
                if alive(pid):
                    raise SystemExit(f"另一个进程（PID {pid}）正在给这部剧出人物资产，等它跑完再来（锁 {self.path.name}）")
                self.path.unlink(missing_ok=True)
        raise SystemExit(f"拿不到锁 {self.path}")

    def __exit__(self, *exc: object) -> None:
        self.path.unlink(missing_ok=True)


def land(url: str, d: Path, stem: str) -> int:
    dst = d / f"{stem}.mp4"
    part = d / f"{stem}.part.mp4"
    for i in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=300) as r, part.open("wb") as f:
                while chunk := r.read(1 << 20):
                    f.write(chunk)
            break
        except OSError:
            if i == 3:
                raise
            time.sleep(10 * (i + 1))
    for old in originals(d):
        if old.name == part.name:
            continue
        bin_ = DELETED / old.relative_to(REPO / "ai_videos")
        if bin_.exists():
            bin_ = bin_.with_name(f"{old.stem}_{time.strftime('%Y%m%d-%H%M%S')}{old.suffix}")
        bin_.parent.mkdir(parents=True, exist_ok=True)
        old.replace(bin_)
    part.replace(dst)
    return dst.stat().st_size


def mean_db(mp4: Path) -> float:
    p = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(mp4), "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = re.search(r"mean_volume: (-?[\d.]+) dB", p.stderr)
    return float(m.group(1)) if m else -120.0


def verdict(d: Path, stem: str, note: str) -> str:
    """从落盘的成片回读：有叫声设计的卡，整条近乎静音就判不通过（文件留着，是当前最好的一条）。"""
    db = mean_db(d / f"{stem}.mp4")
    if creature_sound(d) and db < QUIET_DB:
        return f"近乎静音 {stem}.mp4 平均 {db:.0f} dB < {QUIET_DB:.0f}：叫声没出来——卡里 `声音` 的音量措辞改成「比谁低一截、但听得见」再重出"
    return f"OK {stem}.mp4 {note} · 平均 {db:.0f} dB"


def video_url(r: dict) -> str | None:
    vids = (r.get("result_json") or {}).get("videos") or []
    return vids[0].get("video_url") if vids else None


def wait(sid: str, d: Path, stem: str) -> str:
    t0 = time.time()
    while time.time() - t0 < POLL_MAX:
        r = cli("query_result", f"--submit_id={sid}", timeout=120) or {}
        st = r.get("gen_status") if isinstance(r, dict) else None
        if st == "success" and video_url(r):
            kb = land(video_url(r), d, stem) // 1024
            return verdict(d, stem, f"{kb} KB {time.time() - t0:.0f}s")
        if st == "fail":
            return f"失败：{str(r.get('fail_reason'))[:300]}"
        time.sleep(POLL_EVERY)
    return f"超时（已记账 {sid[:8]}，稍后 --harvest）"


def pending(chars: Path, name: str) -> str | None:
    """账里这张卡还在生成的任务（别的进程提交的、或本进程超时放手的）：等它，不重提（一条 80 分）。
    已成功的不算——落盘后被删掉的旧片不该收回来；超时后成功的走 --harvest。"""
    for sid in reversed([s for s, n in ledger(chars).items() if n == name]):
        r = cli("query_result", f"--submit_id={sid}", timeout=120) or {}
        if isinstance(r, dict) and r.get("gen_status") == "querying":
            return sid
    return None


def one(d: Path, dry: bool, model: str) -> str:
    stem, img, audio, prompt, ratio, dur = job(d)
    head = f"{stem}.mp4 ← {img.name} + {[a.name for a in audio]} · {ratio} · {dur}s · {model} · {len(prompt)} 字"
    if dry:
        print(f"  [dry] {head}\n{prompt}\n")
        return "dry"
    if sid := pending(d.parent, d.name):
        print(f"  {d.name}: 账里有在途任务 {sid[:8]}，等它（不重提）", flush=True)
        return wait(sid, d, stem)
    args = ["multimodal2video", "--image", str(img)]
    for a in audio:
        args += ["--audio", str(a)]
    args += [f"--prompt={prompt}", f"--duration={dur}", f"--ratio={ratio}", f"--video_resolution={RESOLUTION}",
             f"--model_version={model}", "--poll=0"]
    sub = cli(*args, timeout=600) or {}
    sid = sub.get("submit_id") if isinstance(sub, dict) else None
    if not sid or sub.get("gen_status") == "fail":
        return f"提交失败：{str(sub)[:300]}"
    ledger(d.parent, sid, d.name)
    q = (cli("query_result", f"--submit_id={sid}", timeout=120) or {}).get("queue_info") or {}
    print(f"  {d.name}: 已提交 {sid[:8]}（{head}）· priority {q.get('priority')} · 排第 {q.get('queue_idx')} / {q.get('queue_length')}",
          flush=True)
    return wait(sid, d, stem)


def harvest(chars: Path) -> None:
    for sid, name in ledger(chars).items():
        d = chars / name
        stem = f"{name}_turntable"
        if (d / f"{stem}.mp4").is_file():
            continue
        r = cli("query_result", f"--submit_id={sid}", timeout=120) or {}
        if isinstance(r, dict) and r.get("gen_status") == "success" and video_url(r):
            print(f"  {name}: 补收 · " + verdict(d, stem, f"{land(video_url(r), d, stem) // 1024} KB"))


def todo(chars: Path, only: list[str], cry: bool = False, force: bool = False) -> list[Path]:
    """要出片的卡：有卡、有 turntable 块、有立绘（或可退的正面帧），且还没有原始建立视频（--force 除外）。"""
    return [d for d in sorted(chars.iterdir()) if d.is_dir() and (d / f"{d.name}.md").is_file()
            and (not only or d.name.split("_")[0] in only) and (not cry or creature_sound(d))
            and has_block(d) and (force or not originals(d))]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--drama", required=True, help="相对 ai_videos/，如 shengji_zhilu")
    ap.add_argument("--only", default="", help="逗号分隔的卡号，如 m2,c12")
    ap.add_argument("--cry", action="store_true", help="所有带 `## 叫声设计` 的卡")
    ap.add_argument("--force", action="store_true", help="已有建立视频也重出（旧的挪进 ai_videos/_deleted/）")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--harvest", action="store_true")
    ap.add_argument("--model", default="seedance2.5", choices=MODELS,
                    help="默认 seedance2.5（会员 priority 7、零排队）；普通 seedance2.0 实测排队 3 万位、几乎不动")
    args = ap.parse_args()
    chars = chars_dir(args.drama)
    if args.harvest:
        harvest(chars)
        return 0
    only = [s for s in args.only.split(",") if s]
    if not only and not args.cry:
        raise SystemExit("给 --only 或 --cry（不许一把全出；全剧补齐走 tools/char_assets.py）")
    dirs = todo(chars, only, args.cry, args.force or args.dry_run)
    if not dirs:
        print("范围里没有要出的卡（都已有建立视频，或缺 turntable 块）")
        return 0
    bad = 0
    with DramaLock(chars):
        for d in dirs:
            res = one(d, args.dry_run, args.model)
            if res != "dry":
                print(f"  {d.name}: {res}", flush=True)
            bad += not (res.startswith("OK") or res == "dry")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
