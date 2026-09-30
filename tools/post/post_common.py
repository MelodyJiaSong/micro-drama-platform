# -*- coding: utf-8 -*-
"""tools/post 共用：剧根与集目录定位、剪进成片的镜、镜在成片里的时间线、shot md 的台词与场景键、ffprobe、可续跑的步骤戳。"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))
import seedance_kit  # noqa: E402

FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"
POST_PYTHON = REPO / "index-tts/.venv/Scripts/python.exe"   # 装了 cv2 / numpy（demucs 另装）的后期解释器
ALIGN_PYTHON = REPO / ".venv-post/Scripts/python.exe"       # torch(cu128) + stable-ts：台词强制对齐（post/align.py）
POST_DIR = "post"                                            # 每集的后期工作目录（可再生）
CUT_DIR = "cut"                                              # 每集的剪辑决定（edl.toml，git 跟踪，不是缓存）
FPS = 24                     # 成片帧率：Seedance 原生 24p（即梦网页下载是 60 tbr 容器，实为 24 帧/秒 VFR）
AR = 48000                   # 成片音频采样率
MEZZ = ("-c:v", "libx264", "-preset", "medium", "-crf", "12", "-pix_fmt", "yuv420p")    # 中间片近无损：只在交付时有损编码一次
DELIVER = ("-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart")
MASTER_SHORT = 1080          # 母带短边不足 1080 就 lanczos 放大（非生成式）
ACODEC = "aac"               # 交付音频编码：finish_ep 出片、bodies 拼接写，qc Q2 回读查
DX_TARGET = -23.0            # 对白门控响度目标（LUFS）：画内逐事件配平与画外 TTS 归一共用
STALE_TOL_S = 0.5            # 出片片长与 md 的 duration_s 差过这么多＝旧片（出片固有多 0.02–0.08 s）
TAKE_ID_LEN = 12             # take 身份（文件 sha256）在 edl、对齐缓存名、审片目录名里取的位数
PROXY_SUB = "proxy"          # 每集代理片目录 {ep}/post/proxy/（finish_ep --proxy 写，viewing_packet 按它分观片包目录）
TTS_LIP, TTS_POST = "lip", "post"            # tools/indextts_dub.py 的两条镜长轨：lip＝画内开口，post＝不动嘴
LIP_KINDS = ("正常台词",)                      # 台词配音块「类型」：画内开口（原生音轨里有；tts_first 走 lip 轨）
OFF_KINDS = ("内心独白", "画外", "系统提示音")  # 不动嘴：原生音轨里没有，后期按 post 轨配
SHOT_RE = re.compile(r"shot(\d+)")
WINDOW_RE = re.compile(r"(\d+(?:\.\d+)?)\s*[–\-~—至]\s*(\d+(?:\.\d+)?)")
NUM_RE = re.compile(r"\d+(?:\.\d+)?")
SCENE_RE = re.compile(r"`(bg(\d+)(?:-\d+)?_[^`(（=]+)")
FIELD_RE = re.compile(r"\s*([^:：]+?)\s*[:：]\s*(.*)$")
KIND_NOTE_RE = re.compile(r"[（(]")           # 「内心独白（画外，嘴唇不动）」「正常台词(对口型)」：括号起是注
SILENCE_RE = re.compile(r"silence_(start|end): (-?\d+(?:\.\d+)?(?:e[-+]?\d+)?)")
FRAME_RE = re.compile(r"^frame=(\d+)$", re.M)
_odd_kinds: set[str] = set()


def warn(msg: str) -> None:
    print(f"⚠ {msg}", file=sys.stderr)


def rel(p: Path) -> str:
    """仓库相对路径（报错、报告、manifest 用）；不在仓库里给绝对路径。"""
    try:
        return p.resolve().relative_to(REPO).as_posix()
    except ValueError:
        return p.resolve().as_posix()


def take_id(sha: str) -> str:
    return sha[:TAKE_ID_LEN]


def utf8_console() -> None:
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="replace")


# ─────────────────────────── 定位 ───────────────────────────

def drama_root(name: str) -> Path:
    """剧目录路径，或剧名 / seedance.toml 里登记的别名（与 seedance_kit.resolve 同一规则）。"""
    p = Path(name)
    if p.is_dir():
        return p.resolve()
    dramas = [d for d in seedance_kit.AI.iterdir() if d.is_dir() and not d.name.startswith((".", "_"))]
    hit = [d for d in dramas if d.name == name or name in seedance_kit.config_or_empty(d).get("alias", [])]
    if len(hit) != 1:
        raise SystemExit(f"剧「{name}」对不上（{seedance_kit.CONFIG} 的 alias 里登记别名）：{[d.name for d in hit] or '无'}")
    return hit[0]


def ep_name(ep: str) -> str:
    return "ep%02d" % int(re.sub(r"\D", "", ep))


def ep_dir(drama: Path, ep: str) -> Path:
    name = ep_name(ep)
    std = drama / "5_6_分镜与prompt" / "episodes" / name
    if (std / "shots").is_dir():
        return std
    hits = [p for p in drama.rglob(name) if (p / "shots").is_dir()]
    if len(hits) != 1:
        raise SystemExit(f"{drama.name} {name}：找到 {len(hits)} 个带 shots/ 的集目录")
    return hits[0]


def shot_no(d: Path) -> int:
    return int(SHOT_RE.fullmatch(d.name).group(1))


def shot_dirs(epd: Path) -> list[Path]:
    return sorted((d for d in (epd / "shots").iterdir() if d.is_dir() and SHOT_RE.fullmatch(d.name)), key=shot_no)


def shot_md(d: Path) -> Path:
    return d / f"{d.name}.md"


def shot_mp4(d: Path) -> Path:
    return d / f"{d.name}.mp4"


def tts_file(d: Path, track: str, ext: str = ".wav") -> Path:
    """tools/indextts_dub.py 写的镜长轨（.wav）与每句实际摆位 sidecar（.json）：shotNN/shotNN_tts_{lip|post}{ext}。"""
    return d / f"{d.name}_tts_{track}{ext}"


def parse_shots(spec: str) -> set[int]:
    """「1-7,9」「shot02,shot05」→ 镜号集合。"""
    out: set[int] = set()
    for part in re.sub(r"shot", "", spec).split(","):
        a, _, b = part.strip().partition("-")
        out.update(range(int(a), int(b or a) + 1))
    return out


def cut_shots(epd: Path, spec: str | None) -> list[Path]:
    """剪进成片的镜。不给 --shots：从第一镜起连续有出片（shotNN.mp4）的前缀——中间缺一镜就停，不跳着拼。旧片（stale_take）一律报错。"""
    dirs = shot_dirs(epd)
    if spec:
        want = parse_shots(spec)
        unknown = sorted(want - {shot_no(d) for d in dirs})
        picked = [d for d in dirs if shot_no(d) in want]
        missing = [d.name for d in picked if not shot_mp4(d).is_file()]
        if unknown or missing:
            raise SystemExit(f"--shots {spec}：没有这些镜 {unknown}；没出片 {missing}")
        return _fresh_takes(picked)
    out: list[Path] = []
    for i, d in enumerate(dirs):
        if not shot_mp4(d).is_file():
            later = [x.name for x in dirs[i + 1:] if shot_mp4(x).is_file()]
            warn(f"{d.name} 还没有出片，只拼到 {out[-1].name if out else '（无）'}"
                 + (f"；后面已出片的 {'、'.join(later)} 要一起拼就用 --shots" if later else ""))
            break
        out.append(d)
    if not out:
        raise SystemExit(f"{epd.name}：第一镜就没有出片")
    return _fresh_takes(out)


def _fresh_takes(dirs: list[Path]) -> list[Path]:
    old = [why for d in dirs if (why := stale_take(shot_md(d), shot_mp4(d)))]
    if old:
        raise SystemExit("出片是旧片，不进成片：\n  " + "\n  ".join(old))
    return dirs


# ─────────────────────────── 媒体 ───────────────────────────

@dataclass(frozen=True)
class Media:
    v_dur: float
    a_dur: float
    w: int
    h: int
    has_audio: bool


def probe(p: Path) -> Media:
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "stream=codec_type,width,height,duration",
                        "-show_entries", "format=duration", "-of", "json", str(p)], capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"ffprobe 读不了 {p}：{r.stderr.decode('utf-8', 'replace')[-300:]}")
    j = json.loads(r.stdout)
    fmt = float(j.get("format", {}).get("duration", 0) or 0)
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    return Media(float(v.get("duration", fmt)) if v else 0.0, float(a.get("duration", fmt)) if a else 0.0,
                 int(v["width"]) if v else 0, int(v["height"]) if v else 0, a is not None)


def scale_short(w: int, h: int, short: int) -> tuple[int, int]:
    """等比缩放到短边 short（宽高取偶数）。"""
    k = short / min(w, h)
    return 2 * round(w * k / 2), 2 * round(h * k / 2)


def master_size(w: int, h: int) -> tuple[int, int]:
    """母带尺寸：短边不足 MASTER_SHORT 就等比放大到它，够了不动。1280×720 → 1920×1080，720×1280 → 1080×1920。"""
    return (w, h) if min(w, h) >= MASTER_SHORT else scale_short(w, h, MASTER_SHORT)


def cfr_frames(p: Path) -> int:
    """按 FPS 转成恒定帧率后的帧数——bodies.event 用 fps 滤镜按帧号切的就是这条时间线。即梦下载的 VFR 片末帧只占 1/60 s，
    容器时长 × FPS 会少算一帧，nb_frames 也对不上（shot06 实测 649 帧、fps=24 只出 648），所以解码一遍数。"""
    r = subprocess.run([FFMPEG, "-hide_banner", "-nostats", "-progress", "pipe:1", "-i", str(p), "-map", "0:v:0",
                        "-vf", f"fps={FPS}", "-f", "null", "-"], capture_output=True)
    got = FRAME_RE.findall(r.stdout.decode("utf-8", "replace"))
    if r.returncode != 0 or not got:
        raise SystemExit(f"数不出 {p} 的帧数：{r.stderr.decode('utf-8', 'replace')[-300:]}")
    return int(got[-1])


def silences(err: str, dur: float) -> list[tuple[float, float]]:
    """ffmpeg silencedetect 打印的 silence_start / silence_end → 静音区间（秒，夹进 0–dur；没有 silence_end 的算到 dur）。"""
    out: list[tuple[float, float]] = []
    start: float | None = None
    for kind, v in SILENCE_RE.findall(err):
        if kind == "start":
            start = max(0.0, float(v))
        elif start is not None:
            out.append((start, min(float(v), dur)))
            start = None
    return out + ([(start, dur)] if start is not None else [])


def md_duration(md: Path) -> float | None:
    """shot md front matter 的 duration_s（镜长，秒）；没写就 None。"""
    m = re.search(r"^duration_s:\s*([\d.]+)", md.read_text(encoding="utf-8"), re.M)
    return float(m.group(1)) if m else None


def stale_take(md: Path, take: Path) -> str | None:
    """出片是不是旧片：片长与 md 的 duration_s 差 > STALE_TOL_S（md 改了时长、片没重出）→ 返回原因；md 没写 duration_s 不判。"""
    want = md_duration(md)
    if want is None:
        return None
    got = probe(take).v_dur
    if abs(got - want) <= STALE_TOL_S:
        return None
    return (f"{take.parent.name}/{take.name} 长 {got:.2f}s，md 定的是 {want:g}s（差 > {STALE_TOL_S:g}s：md 改过、片没重出）"
            "——先重出，或把旧片挪进 renders/")


def check_fps(take: Path) -> None:
    """源片帧率：avg_frame_rate 取整 ≠ FPS 即报错（即梦下载是 60 tbr 容器、实为 24 帧 VFR，只有 avg 可信）。"""
    r = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=avg_frame_rate",
                        "-of", "csv=p=0", str(take)], capture_output=True, text=True)
    raw = r.stdout.strip()
    fps = float(Fraction(raw)) if raw and not raw.endswith("/0") else 0.0
    if round(fps) != FPS:
        raise SystemExit(f"{take}：avg_frame_rate 实测 {raw or '读不出'}（≈{fps:.3f}），不是 {FPS} 帧/秒")


def run(cmd: list[str | Path], cwd: Path | None = None) -> None:
    r = subprocess.run([str(c) for c in cmd], capture_output=True, cwd=cwd)
    if r.returncode != 0:
        raise SystemExit(f"命令失败（{r.returncode}）：{' '.join(str(c) for c in cmd[:8])} …\n"
                         f"{r.stderr.decode('utf-8', 'replace')[-1500:]}")


# ─────────────────────────── 时间线 ───────────────────────────

@dataclass(frozen=True)
class Seg:
    shot: str
    start: float
    dur: float


def read_segments(path: Path) -> list[Seg]:
    j = json.loads(path.read_text(encoding="utf-8"))
    return [Seg(s["shot"], float(s["start_s"]), float(s["dur_s"])) for s in j["segments"]]


def write_segments(path: Path, segs: list[Seg], approx: bool) -> None:
    total = segs[-1].start + segs[-1].dur if segs else 0.0
    rows = [{"shot": s.shot, "start_s": round(s.start, 3), "end_s": round(s.start + s.dur, 3), "dur_s": round(s.dur, 3)}
            for s in segs]
    path.write_text(json.dumps({"version": 1, "approx": approx, "total_s": round(total, 3), "segments": rows},
                               ensure_ascii=False, indent=2), encoding="utf-8")


def segments_from_mp4s(dirs: list[Path]) -> list[Seg]:
    out: list[Seg] = []
    t = 0.0
    for d in dirs:
        dur = probe(shot_mp4(d)).v_dur
        out.append(Seg(d.name, t, dur))
        t += dur
    return out


# ─────────────────────────── shot md ───────────────────────────

@dataclass(frozen=True)
class Line:
    speaker: str
    kind: str
    text: str
    zh: str
    t0: float
    t1: float
    target: float | None


def _fields(block: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for raw in block.split("\n"):
        for part in raw.split("｜"):
            m = FIELD_RE.match(part)
            if m and m.group(1) not in out:
                out[m.group(1)] = m.group(2).strip()
    return out


def dialogue(md: Path) -> list[Line]:
    """「## 台词配音 prompt」下每个 ```text 块 → 一句台词（没有时间窗或台词的块跳过并警告）。"""
    sec = re.search(r"^## 台词配音 prompt[^\n]*\n(.*?)(?=^## |\Z)", md.read_text(encoding="utf-8"), re.S | re.M)
    out: list[Line] = []
    for i, block in enumerate(re.findall(r"^```text\n(.*?)^```", sec.group(1), re.S | re.M) if sec else [], 1):
        f = _fields(block)
        win = WINDOW_RE.search(f.get("时间窗", ""))
        if not win or not f.get("台词"):
            warn(f"{md.name} 台词配音 {i}：缺 时间窗 或 台词，不出字幕")
            continue
        tgt = NUM_RE.search(f.get("时长目标", ""))
        out.append(Line(f.get("角色", ""), f.get("类型", ""), f["台词"], f.get("中文意思", ""),
                        float(win.group(1)), float(win.group(2)), float(tgt.group(0)) if tgt else None))
    return out


def base_kind(kind: str) -> str:
    """「类型」去掉括注：「内心独白（画外，嘴唇不动）」→ 内心独白；没写类型按正常台词（indextts_dub 的旧约定）。"""
    return KIND_NOTE_RE.split(kind, maxsplit=1)[0].strip() or LIP_KINDS[0]


def onscreen(kind: str) -> bool:
    """这句台词画内开口（原生音轨里有）还是不动嘴（后期配）——全仓只在这里判。不认识的类型按不动嘴：
    原生音轨里不找它、native 缺 TTS 时 finish_ep 报错，不会悄悄哑掉；每种只警告一次。"""
    base = base_kind(kind)
    if base not in LIP_KINDS + OFF_KINDS and base not in _odd_kinds:
        _odd_kinds.add(base)
        warn(f"台词类型「{kind}」不认识（只认 {' / '.join(LIP_KINDS + OFF_KINDS)}，括注随意）——按不动嘴处理；"
             f"画内开口的改写成 {LIP_KINDS[0]}")
    return base in LIP_KINDS


def scene_key(md: Path) -> tuple[str, str] | None:
    """「参考:」行里第一个 bg 主体 →（主体键 bg{N}, 原文名）；路由键 bg{N}-{M}_… 归到主体 bg{N}。"""
    m = re.search(r"^参考:(.*)$", md.read_text(encoding="utf-8"), re.M)
    k = SCENE_RE.search(m.group(1)) if m else None
    return (f"bg{k.group(2)}", k.group(1)) if k else None


def is_chengjie(md: Path) -> bool:
    """本镜开头是不是承接上一镜（front matter `seam:`，缺了看 `衔接` 行）。"""
    text = md.read_text(encoding="utf-8")
    m = re.search(r"^seam:\s*(\S+)", text, re.M) or re.search(r"^- \*\*衔接\*\*[:：]\s*(\S+)", text, re.M)
    return bool(m) and m.group(1).startswith("承接")


# ─────────────────────────── 步骤戳（逐单元落盘、跳过已完成）───────────────────────────

def signature(inputs: list[Path], **params: object) -> dict:
    return {"inputs": [[p.as_posix(), p.stat().st_size, p.stat().st_mtime_ns] for p in inputs], "params": params}


def _stamp_path(out: Path, where: Path | None) -> Path:
    return (where or out.parent) / (out.name + ".stamp.json")


def fresh(out: Path, sig: dict, where: Path | None = None) -> dict | None:
    """产物在、且上次写它时的输入与参数和这次一样 → 返回上次的戳；否则 None（要重做）。
    戳默认挨着产物放；交付件（集目录里的成片）把戳放进 `where`（post/），集目录只留交付件。"""
    sp = _stamp_path(out, where)
    if not (out.is_file() and sp.is_file()):
        return None
    st = json.loads(sp.read_text(encoding="utf-8"))
    return st if st.get("sig") == json.loads(json.dumps(sig)) else None


def stamp(out: Path, sig: dict, where: Path | None = None, **extra: object) -> None:
    _stamp_path(out, where).write_text(json.dumps({"sig": sig, **extra}, ensure_ascii=False, indent=1), encoding="utf-8")


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()
