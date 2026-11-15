# -*- coding: utf-8 -*-
"""整集音频预览（ai_video_management follow-up 360，edu_videos follow-up 040）：出视频前，用本地 TTS 按人物声音
把整集对白排成一条音轨，用户先听、代理也拿它自检；时间轴就是之后出视频的每镜时长与台词起点。

    python tools/audio_preview.py build <清单.json> [--lang zh|en] [--force-qa]
    python tools/audio_preview.py from-filming <集目录> [--lang en]      # 短剧：由 filming.json 生成清单，再 build

清单（输入，代理或适配脚本写）：
    title, path（预览页的路径：知识点目录或集目录）, lang（缺省 zh）
    voices   {说话人: {reference（相对仓库根的 wav）, reference_text}}；没有声样的说话人用 voices["*"]（旁白 / 频道音色）
    say      {写法: 念法}：只在送去配音与回听时替换（多音字「栅极」→「珊极」），页面上的台词不变
    defaults {lead 0.6, gap 0.35, tail 0.8, min 4, max 15}（秒；每镜可覆盖 lead / tail / min）
    scenes[] {id, title, subtitle?, shots[] {id, title, image?, note?, lead?, tail?, min?, lines[] {speaker, text}}}
    links[]  {label, path}；notes[] {title, items[]}

产物（{path}/audio/preview[/<lang>]/）：lines/<说话人>/ 逐句配音（VoxCPM2，Apache-2.0）与 takes.json（回听选条），
preview.wav / preview.m4a，timeline.json（每镜 start、duration、台词相对起止——出视频的时长契约）；
{path}/audio_preview[.<lang>].json 给管理站 `/episode-preview?path=<path>&audio=1` 读（成片模式的 audio 变体）。
每镜时长 = 起势 + 各句 + 句间停顿 + 收尾，向上取整秒，不少于 min；超过 max（Seedance 单条上限）报出来，要拆镜。
本地运行不收费、不走请求日志；只是听感预览，不进成片（成片配音照 edu / 短剧各自的声音流程）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
from edu_video import SR, WHISPER, cer, trimmed, wer  # noqa: E402

VOXCPM_PY = REPO / ".cache/venvs/voxcpm/Scripts/python.exe"
DEFAULTS = {"lead": 0.6, "gap": 0.35, "tail": 0.8, "min": 4, "max": 15}
SEEDS = [1, 2, 3]
LIMIT = {"zh": 0.15, "en": 0.20}      # 回听错率超过就换种子
NOTE_RE = re.compile(r"[（(][^）)]*[）)]")
SAY_RE = re.compile(r"\{([^|{}]*)\|([^{}]*)\}")      # 讲稿的 `{显示|念法}`（与 edu_video.py 同）


def rel(p: Path) -> str:
    return p.resolve().relative_to(REPO).as_posix()


def clean(text: str) -> str:
    """去掉台词里写给作者的括号备注（「（倒扣朝向待核）」），只留要念的字。"""
    return re.sub(r"\s+", " ", NOTE_RE.sub("", text)).strip()


def display(text: str) -> str:
    """页面与字幕上的写法：`{显示|念法}` 取显示。"""
    return SAY_RE.sub(r"\1", clean(text))


def spoken(spec: dict, text: str) -> str:
    """送去配音的写法：`{显示|念法}` 取念法，再按清单 say 把多音字换成同音字（模型把「栅极」念成 zhà jí）。"""
    text = SAY_RE.sub(r"\2", clean(text))
    for a, b in spec.get("say", {}).items():
        text = text.replace(a, b)
    return text


def whisper_model():
    from faster_whisper import WhisperModel
    # 只用 CPU：本机 faster-whisper 的 CUDA 缺 cublas64_12.dll（2026-11-14 试过，转写时才报错），与 edu_video.py 一致
    return WhisperModel(WHISPER, device="cpu", compute_type="int8")


def slug(speaker: str) -> str:
    return "v_" + hashlib.sha1(speaker.encode("utf-8")).hexdigest()[:8]


def line_id(speaker: str, text: str) -> str:
    return "l_" + hashlib.sha1(f"{speaker}\n{text}".encode("utf-8")).hexdigest()[:10]


def voice_for(spec: dict, speaker: str) -> dict:
    v = spec["voices"].get(speaker) or spec["voices"].get("*")
    if not v:
        raise SystemExit(f"说话人「{speaker}」没有声样（voices 里也没有 \"*\"）")
    if not (REPO / v["reference"]).is_file():
        raise SystemExit(f"声样不存在：{v['reference']}")
    return v


def synthesize(spec: dict, out: Path, lang: str, force_qa: bool) -> dict[str, dict]:
    """逐句出配音，回听挑最好的一条；返回 line_id → {wav, seconds, cer, seed, speaker, text}。"""
    wanted: dict[str, dict[str, str]] = {}
    for sc in spec["scenes"]:
        for sh in sc["shots"]:
            for ln in sh.get("lines", []):
                text = spoken(spec, ln["text"])
                if text:
                    wanted.setdefault(ln["speaker"], {})[line_id(ln["speaker"], text)] = text
    takes_path = out / "lines" / "takes.json"
    takes_path.parent.mkdir(parents=True, exist_ok=True)      # 全程无台词的集也要能出静音时间轴（follow-up 363）
    takes = json.loads(takes_path.read_text(encoding="utf-8")) if takes_path.exists() else {}
    model = None
    for speaker, items in wanted.items():
        vdir = out / "lines" / slug(speaker)
        vdir.mkdir(parents=True, exist_ok=True)
        voice = voice_for(spec, speaker)
        for seeds in ([SEEDS[0]], SEEDS):      # 先一条种子；回听不过再补其余种子
            if len(seeds) == 1:
                todo = {i: t for i, t in items.items() if force_qa or i not in takes or takes[i].get("text") != t
                        or takes[i].get("reference") != voice["reference"]}
            else:
                todo = {i: t for i, t in items.items() if takes[i].get("cer", 0) > LIMIT[lang]
                        and len(takes[i].get("tried", [])) < len(SEEDS)}
            if not todo:
                break
            gen = {"voice": {"reference": voice["reference"], "reference_text": voice["reference_text"]},
                   "items": [{"id": i, "text": t, "seeds": seeds} for i, t in todo.items()]}
            gpath = vdir / "gen.json"
            gpath.write_text(json.dumps(gen, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"配音 {speaker}：{len(todo)} 句 × 种子 {seeds}", flush=True)
            subprocess.run([str(VOXCPM_PY), str(REPO / "tools/edu_voxcpm.py"), str(gpath), *todo], cwd=REPO, check=True)
            if model is None:
                model = whisper_model()
            for i, text in todo.items():
                best = None
                for seed in seeds:
                    wav = vdir / f"{i}_s{seed}.wav"
                    if not wav.exists():
                        continue
                    segs, _ = model.transcribe(str(wav), language=lang, beam_size=5)
                    heard = "".join(s.text for s in segs).strip()
                    err = cer(text, heard) if lang == "zh" else wer(text, heard)
                    if best is None or err < best["cer"]:
                        best = {"wav": rel(wav), "seed": seed, "cer": round(err, 3), "heard": heard}
                if best is None:
                    raise SystemExit(f"{speaker} {i} 没有出声")
                takes[i] = best | {"speaker": speaker, "text": text, "reference": voice["reference"], "tried": seeds}
                flag = "" if best["cer"] <= LIMIT[lang] else "  ← 超标"
                print(f"  {i} 种子{best['seed']} 错率 {best['cer']:.0%}：{text[:24]} → {best['heard'][:24]}{flag}", flush=True)
            takes_path.write_text(json.dumps(takes, ensure_ascii=False, indent=1), encoding="utf-8")
    for i, t in takes.items():
        t["seconds"] = round(len(trimmed(REPO / t["wav"])) / SR, 3)
    takes_path.write_text(json.dumps(takes, ensure_ascii=False, indent=1), encoding="utf-8")
    return takes


def layout(spec: dict, takes: dict[str, dict]) -> tuple[list[dict], float]:
    """排时间轴。每镜：起势 + 各句（句后 gap，另加该句 pause）+ 收尾，向上取整秒、不少于 min。
    defaults.split = true 时（没有定好镜头的系列，如教学视频按讲稿段落排），一段超过 max 就按句拆成几镜（`<镜>-1`、`-2`…，
    每镜不超过 max，句子不拆开）；不开时只标 over_max，由人决定拆镜（短剧的镜头是分镜定的）。"""
    d = DEFAULTS | spec.get("defaults", {})
    shots, t0 = [], 0.0

    def emit(sc: dict, sh: dict, sid: str, items: list[tuple[dict, dict]], lead: float, tail: float) -> None:
        nonlocal t0
        t, lines = lead, []
        for ln, tk in items:
            text = display(ln["text"])
            lines.append({"speaker": ln["speaker"], "text": text, "start": round(t, 2), "end": round(t + tk["seconds"], 2),
                          "wav": tk["wav"], "cer": tk["cer"]})
            t += tk["seconds"] + d["gap"] + float(ln.get("pause", 0))
        need = (t - d["gap"] if lines else t) + tail
        dur = max(sh.get("min", d["min"]), math.ceil(need - 1e-6))
        shots.append({"scene": sc["id"], "id": sid, "src": sh["id"], "title": sh.get("title", sh["id"]), "start": round(t0, 2),
                      "duration": dur, "speech_need": round(need, 2), "over_max": dur > d["max"], "lines": lines})
        t0 += dur

    for sc in spec["scenes"]:
        for sh in sc["shots"]:
            lead, tail = sh.get("lead", d["lead"]), sh.get("tail", d["tail"])
            items = [(ln, takes[line_id(ln["speaker"], spoken(spec, ln["text"]))]) for ln in sh.get("lines", []) if clean(ln["text"])]
            cost = [tk["seconds"] + d["gap"] + float(ln.get("pause", 0)) for ln, tk in items]
            if not d.get("split") or lead + sum(cost) - d["gap"] + tail <= d["max"]:
                emit(sc, sh, sh["id"], items, lead, tail)
                continue
            chunks, cur, acc = [], [], 0.0
            for it, c in zip(items, cost):
                first = not chunks and not cur
                budget = d["max"] - (lead if first else d["lead"]) - d["tail"]
                if cur and acc + c - d["gap"] > budget:
                    chunks.append(cur); cur, acc = [], 0.0
                cur.append(it); acc += c
            chunks.append(cur)
            for k, ch in enumerate(chunks, 1):
                emit(sc, sh, f"{sh['id']}-{k}", ch, lead if k == 1 else d["lead"], tail if k == len(chunks) else d["tail"])
    return shots, t0


def mix(shots: list[dict], total: float, out: Path) -> Path:
    y = np.zeros(int(math.ceil(total * SR)) + SR // 10, dtype=np.float32)
    for sh in shots:
        for ln in sh["lines"]:
            x = trimmed(REPO / ln["wav"])
            a = int((sh["start"] + ln["start"]) * SR)
            y[a:a + len(x)] += x[: len(y) - a]
    wav = out / "preview.wav"
    sf.write(str(wav), y, SR, subtype="PCM_16")
    m4a = out / "preview.m4a"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                    "-ar", str(SR), "-c:a", "aac", "-b:a", "160k", str(m4a)], check=True)
    return m4a


def clock(t: float) -> str:
    return f"{int(t // 60)}:{t % 60:04.1f}"


def build(manifest: Path, lang: str | None, force_qa: bool) -> None:
    spec = json.loads(manifest.read_text(encoding="utf-8"))
    lang = lang or spec.get("lang", "zh")
    base = REPO / spec["path"]
    out = base / "audio" / "preview" / ("" if lang == "zh" else lang)
    out.mkdir(parents=True, exist_ok=True)
    takes = synthesize(spec, out, lang, force_qa)
    shots, total = layout(spec, takes)
    audio = mix(shots, total, out)
    timeline = {"version": 1, "lang": lang, "manifest": rel(manifest), "total": total,
                "note": "每镜 duration 是出视频的目标时长（整秒）；lines 的 start/end 是台词相对本镜开头的秒数，写进视频 prompt 的时间轴。",
                "shots": [{k: v for k, v in s.items() if k != "wav"} | {"lines": [{k: v for k, v in ln.items() if k != "wav"} for ln in s["lines"]]}
                          for s in shots]}
    (out / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=1), encoding="utf-8")
    scenes = {sc["id"]: sc for sc in spec["scenes"]}
    shot_src = {(sc["id"], sh["id"]): sh for sc in spec["scenes"] for sh in sc["shots"]}
    chapters, items, cues, seen = [], [], [], set()
    for s in shots:
        if s["scene"] not in seen:
            seen.add(s["scene"])
            sc = scenes[s["scene"]]
            chapters.append({"id": s["scene"], "title": sc.get("title", s["scene"]), "t": s["start"]})
        src = shot_src[(s["scene"], s["src"])]
        said = " / ".join(f"{ln['speaker']}：{ln['text']}" for ln in s["lines"]) or "无对白"
        detail = f"本镜 {s['duration']} 秒（口播加起收需要 {s['speech_need']:.1f} 秒）"
        if s["lines"]:
            detail += "；台词起点 " + "、".join(f"{ln['start']:.1f}s" for ln in s["lines"])
        bad = [ln for ln in s["lines"] if ln["cer"] > LIMIT[lang]]
        note = "；".join(filter(None, [src.get("note", ""),
                                       f"超过单条上限 {DEFAULTS['max']} 秒，出视频要拆镜" if s["over_max"] else "",
                                       f"有 {len(bad)} 句配音回听错率超标，听感仅供参考" if bad else ""]))
        item = {"t": s["start"], "end": s["start"] + s["duration"], "title": f"{s['id']} · {s['title']}", "subtitle": said,
                "chapter": s["scene"], "detail": detail, "badge": f"{s['duration']}s"}
        if src.get("image"):
            item["image"] = src["image"]
        if note:
            item["note"] = note
        items.append(item)
        for ln in s["lines"]:
            cues.append({"t": round(s["start"] + ln["start"], 2), "end": round(s["start"] + ln["end"], 2), "who": ln["speaker"], "text": ln["text"]})
    over = [s["id"] for s in shots if s["over_max"]]
    preview = {
        "title": spec.get("title", base.name) + " · 音频预览",
        "tagline": "出视频前的整集听感：本地 VoxCPM2 按人物声样模拟对白，无画面、无配乐、无音效；每镜时长与台词起点就是之后出视频的目标。",
        "audio": rel(audio), "duration": round(total, 2), "chapters": chapters, "items": items, "cues": cues, "lang": lang,
        "notes": [{"title": "怎么用", "items": [
            "点进度条或下面的卡片跳到那一镜；播放时大图换成当前镜头的故事板，下方显示正在说的台词。",
            f"全片 {clock(total)}，{len(shots)} 镜；每镜时长 = 起势 + 台词 + 句间停顿 + 收尾，取整秒、不少于 {DEFAULTS['min']} 秒。"
            + (f"超过 {DEFAULTS['max']} 秒要拆镜：{'、'.join(over)}。" if over else ""),
            "配音只是听感预览（AI 合成），不进成片；改台词或时长后重跑 `python tools/audio_preview.py build` 即更新。",
        ]}] + spec.get("notes", []),
        "links": spec.get("links", []) + [{"label": "时间轴 timeline.json", "path": rel(out / "timeline.json")},
                                         {"label": "清单", "path": rel(manifest)},
                                         {"label": "逐句配音与回听", "path": rel(out / "lines" / "takes.json")}],
        "languages": spec.get("languages", []),
    }
    pfile = base / ("audio_preview.json" if lang == "zh" else f"audio_preview.{lang}.json")
    pfile.write_text(json.dumps(preview, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"音频预览 {clock(total)}，{len(shots)} 镜 → {rel(audio)}")
    print(f"页面：/episode-preview?path={spec['path']}&audio=1" + ("" if lang == "zh" else f"&lang={lang}"))
    if over:
        print("超过单条上限、要拆的镜头：", "、".join(over))


DIALOGUE_RE = re.compile(r"^([^（(：:]{1,40}?)\s*(?:[（(](.*?)[）)])?\s*[：:]\s*(.+)$", re.S)


def from_filming(episode: Path, lang: str) -> Path:
    """短剧：filming.json → 清单。声样按人物名找 `characters/<名>/voice*.json|wav`，找不到的说话人列出来，由代理补进清单的 voices。"""
    data = json.loads((episode / "filming.json").read_text(encoding="utf-8"))
    drama = episode.parents[1]
    voices: dict[str, dict] = {}
    scenes = []
    for sc in data["content"]["scenes"]:
        shots = []
        for sh in sc["shots"]:
            lines = []
            for part in re.split(r"\s+/\s+|\n+", sh.get("dialogue") or ""):
                m = DIALOGUE_RE.match(part.strip())
                if m:
                    lines.append({"speaker": m.group(1).strip(), "text": m.group(3).strip()})
            frame = episode / "scenes" / sc["id"] / "shots" / sh["id"] / "planning" / f"{sh['id']}_first_frame.png"
            shot = {"id": f"{sc['id']}_{sh['id']}", "title": (sh.get("action") or "")[:30], "lines": lines,
                    "min": int(sh.get("duration") or DEFAULTS["min"])}
            if frame.exists():
                shot["image"] = rel(frame)
            shots.append(shot)
        scenes.append({"id": sc["id"], "title": f"{sc['id']} · {sc.get('location', '')}", "subtitle": sc.get("time", ""), "shots": shots})
    manifest = episode / "audio" / "preview_manifest.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    old = json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else {}
    model = None
    for name in sorted({ln["speaker"] for sc in scenes for sh in sc["shots"] for ln in sh["lines"]}):
        if name in old.get("voices", {}):
            continue
        # 人物资产的声样：characters/<cN_名字>/views/<cN_名字>_audio.mp3（char-assets 命名规则）
        hits = sorted(p for p in drama.glob("2_*/characters/*/views/*_audio.mp3")
                      if re.fullmatch(rf"c\d+_{re.escape(name)}", p.parents[1].name, re.I))
        if not hits:
            continue
        wav = episode / "audio" / "preview" / "voices" / f"{slug(name)}.wav"
        wav.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(hits[0]), "-ac", "1", "-ar", str(SR), str(wav)], check=True)
        if model is None:
            model = whisper_model()
        segs, _ = model.transcribe(str(wav), language=lang, beam_size=5)   # 声样原文：转写一次，存进清单，可手改
        voices[name] = {"reference": rel(wav), "reference_text": "".join(x.text for x in segs).strip(), "source": rel(hits[0])}
        print(f"声样 {name}：{rel(hits[0])} → {voices[name]['reference_text'][:40]}", flush=True)
    spec = {"title": f"{drama.name} {episode.name}", "path": rel(episode), "lang": lang,
            "voices": old.get("voices", {}) | voices, "scenes": scenes}
    manifest.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    missing = sorted({ln["speaker"] for sc in scenes for sh in sc["shots"] for ln in sh["lines"]} - set(spec["voices"]))
    if missing and "*" not in spec["voices"]:
        raise SystemExit(f"清单已写 {rel(manifest)}，但这些说话人没有声样，补进 voices 后再 build：{'、'.join(missing)}")
    return manifest


def main() -> None:
    ap = argparse.ArgumentParser(description="整集音频预览（本地 TTS，出视频前审听感与时长）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("manifest"); b.add_argument("--lang"); b.add_argument("--force-qa", action="store_true")
    f = sub.add_parser("from-filming"); f.add_argument("episode"); f.add_argument("--lang", default="en")
    a = ap.parse_args()
    if a.cmd == "build":
        build(Path(a.manifest).resolve(), a.lang, a.force_qa)
    else:
        m = from_filming(Path(a.episode).resolve(), a.lang)
        build(m, a.lang, False)


if __name__ == "__main__":
    main()
