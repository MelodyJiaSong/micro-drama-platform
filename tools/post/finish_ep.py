# -*- coding: utf-8 -*-
"""一集收尾：可选调色 → 切段 → 对白配平 → 拼接 → 混音（按音频模式）→ 响度归一 → 母带 + 烧字幕版 + SRT → QC → 存档。每步单独落盘、可续跑。

    python tools/post/finish_ep.py <剧> <ep> [--audio-mode native|tts_first] [--shots 1-7] [--proxy]
        [--grade [--ref shotNN] [--strength 0.7]] [--bgm X.mp3 [--bgm-volume 0.4]]
        [--lang src|zh|both] [--burn-lang src|zh|both] [--font 字体名] [--python PY]

剪什么：有 cut/edl.toml → edl.plan() 的事件（bodies.event 按帧切）；没有 → pc.cut_shots 整镜顺接（bodies.legacy，画面时间线同改版前；
承接镜剪掉的头记作源片入点，所以承接镜的 TTS / 技能音效 / 字幕比改版前早 bodies.TRIM，对上了剪过的画面）。
成片只按用户批准过的 edl 出：status 还是 draft、或 edl.verify（V1–V10，审片结论是硬闸门）有一处不过，都在切段之前报错停下。
音频模式读 seedance.toml 的 `audio_mode`（--audio-mode 覆盖；都没有即报错）：native 保留 Seedance 原生人声、逐事件对白配平
（bodies.dx_gains），不动嘴的句子（pc.onscreen）叠每镜 TTS post 轨（pc.tts_file，按段的源片入 / 出点裁），要配却缺即报错；tts_first
人声用 lip / post 轨（旧剧 _voice.mp3 / _dialogue.wav），源音轨经 demucs 只留环境声。TTS 轨与 take 差过 1 帧即报错（md 改了时长、
take 没重出，或反过来）。--bgm 以人声为 sidechain 压低。
响度走 loudness.py（loudnorm linear + alimiter，走了 dynamic 即报错）。字幕按 CPS 上限排读完时间，还有读不完的在出母带前报错。
交付 `{ep}_final.mp4`（pc.master_size lanczos、pc.DELIVER、写回 AIGC）、`{ep}_final_burned.mp4`（同样 pc.DELIVER、带 AIGC）、
`.srt` / `.zh.srt`（这次没出的语言删掉旧的）、`.segments.json`（v2）；两条成片回读 AIGC，最后 qc.run，任一 FAIL 即报错。
有 edl 时再存档 post/masters/v{版本}/（见 archive）。
--proxy：按当前 edl（草稿也行）出 post/proxy/{ep}_v{版本}_proxy.mp4（短边 PROXY_SHORT、烧时间码与双语字幕、响度照常归一，
不写 AIGC、不进 masters、不碰 {ep}_final*，segments 与 SRT 写在旁边）；edl verify（--proxy-ok）与 QC（自测）都只报告。
中间件在 `{ep}/post/`，每件先写 .part 再换名、带 `.stamp.json`，输入与参数没变就跳过。调色与 demucs 交给 --python 的解释器；
缺的对齐缓存由 edl.aligns_for 用 pc.ALIGN_PYTHON 补。
"""
from __future__ import annotations

import argparse
import datetime
import json
import shutil
import subprocess
import wave
from dataclasses import asdict, dataclass
from pathlib import Path

import post_common as pc
import aigc
import bodies
import edl
import loudness
import qc
import segments
import stems
import subs
import mux_av        # tools/ 下的，post_common 已把 tools/ 加进 sys.path

AUDIO_MODES = ("native", "tts_first")
OLD_VOICE = ("{s}_voice.mp3", "{s}_dialogue.wav")     # 旧剧 tts_first 的单轨名（indextts_dub 之前）
MASTERS_SUB = "masters"
MANIFEST = "manifest.json"
PROXY_SHORT = 540
TIMECODE = "%{pts\\:hms}"            # drawtext：成片时间 时:分:秒.毫秒


@dataclass(frozen=True)
class Timeline:
    files: list[Path]                          # 每段的中间片
    parts: list[segments.Part]
    plan: list[edl.Cut] | list[dict]           # 给 qc 的事件表
    takes: dict[str, Path]                     # 镜 → 当前 take（shotNN.mp4）
    clips: list[Path]                          # 实际切段的源（调过色就是调色片）
    aligns: dict[tuple[str, str], edl.Align]
    doc: edl.Edl | None


def audio_mode(drama: Path, override: str | None) -> str:
    mode = override or pc.seedance_kit.config_or_empty(drama).get("audio_mode")
    if mode not in AUDIO_MODES:
        got = f"是 {mode!r}" if mode else "没有 audio_mode"
        raise SystemExit(f"{drama.name}/seedance.toml {got}：写成 {' 或 '.join(AUDIO_MODES)}，或用 --audio-mode 指定")
    return mode


def graded_clips(drama: Path, epd: Path, dirs: list[Path], a: argparse.Namespace) -> list[Path]:
    if not a.grade:
        return [pc.shot_mp4(d) for d in dirs]
    cmd = [str(a.python), str(Path(__file__).with_name("grade_match.py")), str(drama), epd.name,
           "--shots", ",".join(str(pc.shot_no(d)) for d in dirs), "--strength", str(a.strength)]
    cmd += [x for r in a.ref for x in ("--ref", r)]
    if subprocess.run(cmd).returncode != 0:
        raise SystemExit("调色没过，停在这里（上面是 grade_match 的报错）")
    report = json.loads((epd / pc.POST_DIR / "grade" / "grade.json").read_text(encoding="utf-8"))
    return [Path(report["shots"][d.name]["file"]) for d in dirs]


# ─────────────────────────── 时间线 ───────────────────────────

def whole_shots(drama: Path, epd: Path, post: Path, a: argparse.Namespace) -> Timeline:
    """没有 edl：cut_shots 的镜整镜顺接；段长量出来（bodies.legacy），源入点＝承接缝剪掉的头。"""
    dirs = pc.cut_shots(epd, a.shots)
    takes = {d.name: pc.shot_mp4(d) for d in dirs}
    for t in takes.values():
        pc.check_fps(t)
    cur = edl.current_takes(epd, takes)
    evs = tuple(edl.Event(segments.WHOLE_ID % i, s, pc.take_id(cur[s]), "start", "end", "shot", "", "", "", "")
                for i, s in enumerate(takes, 1))
    aligns = edl.aligns_for(drama, epd, evs, cur)
    clips = graded_clips(drama, epd, dirs, a)
    rows = bodies.legacy(post, dirs, clips)
    parts = [segments.Part(e.id, e.shot, e.take, head, head + seg.dur, seg.start, seg.dur, 0.0)
             for e, (_f, seg, head) in zip(evs, rows)]
    plan = [{"id": p.event, "shot": p.shot, "take": p.take, "src_in": p.src_in, "src_out": p.src_out, "dur": p.dur,
             "kind": "shot"} for p in parts]
    return Timeline([f for f, _s, _h in rows], parts, plan, takes, clips, aligns, None)


def from_edl(drama: Path, epd: Path, post: Path, a: argparse.Namespace) -> Timeline:
    """按 edl 出。成片（不带 --proxy）：草稿、或 verify 有一处不过即报错——审片结论（V1）等闸门在这里是硬的。"""
    if a.shots:
        raise SystemExit(f"{pc.rel(edl.edl_path(epd))} 在：剪哪些镜由 edl 定，--shots 只管没有 edl 时的整镜顺接")
    doc = edl.load(epd)
    if doc.status == "draft" and not a.proxy:
        raise SystemExit(f"{pc.rel(doc.path)} v{doc.version} 还是草稿：成片只按用户批准过的 edl 出（status = approved / locked，"
                         "approved_by 写批准人）——草稿先 --proxy 出代理片给用户看")
    shots = list(dict.fromkeys(e.shot for e in doc.events))
    takes = {s: pc.shot_mp4(epd / "shots" / s) for s in shots}
    for t in takes.values():
        if t.is_file():
            pc.check_fps(t)
    found = edl.verify(drama, epd, proxy_ok=a.proxy)
    for f in found:
        print(f"{'✗' if f.level == edl.FAIL else '⚠'} {f.code} {f.msg}")
    n = sum(f.level == edl.FAIL for f in found)
    how = "（--proxy-ok）" if a.proxy else ""
    print(f"edl verify{how}：{n} 处不过、{len(found) - n} 条警告" if found else f"edl verify{how}：V1–V10 全过")
    if n and not a.proxy:
        raise SystemExit(f"edl v{doc.version} verify 有 {n} 处不过（上面逐条），不出成片：改 edl、或回对应的闸门补好再出"
                         "（审片不通过的 take 先重出片再审）；只想看剪辑用 --proxy")
    if n:
        print("代理片照出，交剪辑师与用户看")
    cuts = edl.plan(drama, epd)
    aligns = {(c.shot, c.take): edl.read_align(edl.align_path(epd, c.shot, c.take), c.shot, c.take) for c in cuts}
    clips = graded_clips(drama, epd, [epd / "shots" / s for s in shots], a)
    rows = bodies.events(post, cuts, dict(zip(shots, clips)))
    return Timeline([f for f, _p in rows], [p for _f, p in rows], cuts, takes, clips, aligns, doc)


# ─────────────────────────── 混音 ───────────────────────────

def voice_files(d: Path, mode: str) -> list[Path]:
    """这一镜在该模式下可用的人声轨（在的才用）：indextts_dub 的 post 轨；tts_first 另有 lip 轨与旧剧的单轨。"""
    if mode == "native":
        return [pc.tts_file(d, pc.TTS_POST)]
    return [pc.tts_file(d, pc.TTS_LIP), pc.tts_file(d, pc.TTS_POST), *(d / n.format(s=d.name) for n in OLD_VOICE)]


def _needs(md: Path, mode: str, part: segments.Part) -> bool:
    """这一段在该模式下要不要 TTS：tts_first 有台词就要；native 只有不动嘴的句子要（画内人声是 Seedance 原生的）。
    只看计划窗起点落在本段保留区间里的句子（TTS 轨按同一区间裁）。"""
    lines = [ln for ln in pc.dialogue(md) if subs.kept(part, ln.t0)]
    return bool(lines) if mode == "tts_first" else any(not pc.onscreen(ln.kind) for ln in lines)


def check_sync(track: Path, take: Path) -> None:
    """indextts_dub 按 md 的 duration_s 把轨摆成镜长；与 take 差过 1 帧＝md 改了时长而 take 没重出（或反过来），
    按 take 的入 / 出点裁出来的句子会落在别的画面上。"""
    with wave.open(str(track), "rb") as w:
        n = w.getnframes() / w.getframerate()
    t = pc.probe(take).v_dur
    if abs(n - t) > 1 / pc.FPS:
        raise SystemExit(f"{track.name} {n:.3f}s ≠ {take.name} {t:.3f}s（差过 1 帧）：md 与 take 不同步——take 旧了就重出片，"
                         "TTS 旧了就重跑 tools/indextts_dub.py --force")


def skill_cues(epd: Path, parts: list[segments.Part]) -> list[tuple[Path, float]]:
    """rule 45：每镜 shot md 里机读的施放记录（`<!-- casts: … -->`，生成器写）→ 技能卡定稿音效按阶段时刻摆到整集时间线上。
    音效只认卡里定稿的那一个文件，每次原样贴——同一技能每次一样的声音靠这个，不靠模型现编。
    按剪辑出入点摆：只摆落在这一段源片 [src_in, src_out) 里的，成片时刻＝start + (t − src_in)（剪掉那段的施放不出声）。"""
    import skills_lib
    cards = skills_lib.load(skills_lib.drama_of(epd))
    by_shot: dict[str, list[tuple[float, Path]]] = {}
    out: list[tuple[Path, float]] = []
    for p in parts:
        if p.shot not in by_shot:
            by_shot[p.shot] = []
            for cast in skills_lib.casts_in(pc.shot_md(epd / "shots" / p.shot).read_text(encoding="utf-8")):
                card = skills_lib.find(cards, cast.key)
                by_shot[p.shot] += skills_lib.sound_cues(card, skills_lib.compose(card, cast, {}))
        out += [(f, p.start + t - p.src_in) for t, f in by_shot[p.shot] if p.src_in <= t < p.src_out]
    return out


def voice_track(post: Path, epd: Path, parts: list[segments.Part], mode: str,
                takes: dict[str, Path]) -> tuple[Path | None, list[Path]]:
    """每镜 TTS 轨按段的源片入 / 出点裁好、摆到段起点，技能定稿音效按施放时刻摆上 → {ep}_voice.wav；
    native 整集既没有画外 / 独白、也没有技能音效时返回 None。→（轨, 用到的文件）"""
    out = post / f"{epd.name}_voice.wav"
    total = parts[-1].end
    items, trims, missing, synced = [], {}, [], set()
    for p in parts:
        d = epd / "shots" / p.shot
        found = [f for f in voice_files(d, mode) if f.is_file()]
        for f in found:
            if f in (pc.tts_file(d, pc.TTS_LIP), pc.tts_file(d, pc.TTS_POST)) and f not in synced:
                check_sync(f, takes[p.shot])
                synced.add(f)
            trims[len(items)] = (p.src_in, p.src_out)
            items.append((f, p.start))
        if not found and _needs(pc.shot_md(d), mode, p):
            missing.append(p.shot)
    items += skill_cues(epd, parts)
    if missing:
        names = " / ".join(f.name.replace(missing[0], "shotNN") for f in voice_files(epd / "shots" / missing[0], mode))
        raise SystemExit(f"{mode}：{list(dict.fromkeys(missing))} 要配音却没有 TTS（{names}；跑 tools/indextts_dub.py"
                         f"{' --only ' + pc.TTS_POST if mode == 'native' else ''}）——不补这几句就哑了")
    if not items:
        if mode == "native":
            return None, []
        raise SystemExit("tts_first：整集没有一条 TTS")
    used = list(dict.fromkeys(f for f, _ in items))
    sig = pc.signature([f for f, _ in items], starts=[round(t, 3) for _, t in items], total=round(total, 3),
                       trims=[[round(x, 6) for x in trims[k]] if k in trims else [] for k in range(len(items))], ar=pc.AR)
    if pc.fresh(out, sig):
        return out, used
    cmd: list[str | Path] = [pc.FFMPEG, "-y"]
    fc = []
    for k, (f, t) in enumerate(items):
        cmd += ["-i", f]
        cut = f"atrim=start={trims[k][0]:.6f}:end={trims[k][1]:.6f},asetpts=PTS-STARTPTS," if k in trims else ""
        fc.append(f"[{k}:a]{cut}aresample={pc.AR},aformat=channel_layouts=stereo,adelay={round(t * 1000)}:all=1[v{k}]")
    labels = "".join(f"[v{k}]" for k in range(len(items)))
    mix_ = f"amix=inputs={len(items)}:normalize=0:duration=longest," if len(items) > 1 else ""
    n = round(total * pc.AR)            # 按样本数补齐（apad=whole_dur 在 amix 后偶尔不补，见 indextts_dub.place）
    fc.append(f"{labels}{mix_}apad=whole_len={n},atrim=end_sample={n}[out]")
    part = out.with_name(out.stem + ".part.wav")
    pc.run(cmd + ["-filter_complex", ";".join(fc), "-map", "[out]", part])
    part.replace(out)
    pc.stamp(out, sig)
    return out, used


def mix(post: Path, epd: Path, mode: str, cut: Path, parts: list[segments.Part], takes: dict[str, Path],
        a: argparse.Namespace) -> tuple[Path, list[Path]]:
    """→（混好的片, 混进去的音频文件）。"""
    voice, used = voice_track(post, epd, parts, mode, takes)
    if mode == "native" and not a.bgm and voice is None:
        print("混音：native、没有 BGM、也没有画外 / 独白——源音轨原样进成片")
        return cut, []
    out = post / f"{epd.name}_mix.mp4"
    part = out.with_name(out.stem + ".part.mp4")
    argv = ["--video", str(cut), "--out", str(part)]
    ins = [cut]
    if mode == "native":
        argv += ["--keep-source-audio", "--duck-source"] + (["--dialogue", str(voice)] if voice else [])
        ins += [voice] if voice else []
    else:
        no_voc = stems.separate(cut, post / "stems" / cut.stem, a.python)
        argv += ["--dialogue", str(voice), "--source-stem", str(no_voc)]
        ins += [voice, no_voc]
    if a.bgm:
        argv += ["--bgm", str(a.bgm)] + (["--bgm-volume", str(a.bgm_volume)] if a.bgm_volume is not None else [])
        ins.append(a.bgm)
        used.append(a.bgm)
    sig = pc.signature(ins, mode=mode, bgm_volume=a.bgm_volume)
    if pc.fresh(out, sig):
        print(f"混音：已是最新，跳过（{out.name}）")
        return out, used
    if mux_av.main(argv) != 0:
        raise SystemExit("混音失败（上面是 mux_av 的报错）")
    part.replace(out)
    pc.stamp(out, sig)
    return out, used


# ─────────────────────────── 出片 ───────────────────────────

def encode(src: Path, out: Path, vf: list[str], venc: list[str]) -> None:
    """一次编码：视频按 vf / venc，音频走 loudness 的线性归一（pc.ACODEC mux_av.LOUD_BITRATE、pc.AR）；loudnorm 报 dynamic 即报错。"""
    lp = loudness.plan(src)
    part = out.with_name(out.stem + ".part.mp4")
    r = subprocess.run([pc.FFMPEG, "-hide_banner", "-nostats", "-y", "-i", str(src), "-map", "0:v:0", "-map", "0:a:0", *vf,
                        "-af", lp.af, *venc, "-c:a", pc.ACODEC, "-b:a", mux_av.LOUD_BITRATE, "-ar", str(pc.AR), "-ac", "2",
                        str(part)], capture_output=True)
    err = r.stderr.decode("utf-8", "replace")
    if r.returncode != 0:
        raise SystemExit(f"编码 {out.name} 失败：{err[-1500:]}")
    s = loudness.check(err, out.name)
    part.replace(out)
    print(f"响度：原片 {lp.raw['input_i']} LUFS / {lp.raw['input_tp']} dBTP → 预增益 {lp.pre_db:+.2f} dB + alimiter "
          f"{loudness.TP_TARGET:g} dBTP → loudnorm linear {s['output_i']} LUFS / {s['output_tp']} dBTP（{out.name}）")


def master(post: Path, mixed: Path, takes: list[Path], final: Path) -> dict[str, str]:
    """母带：短边不足 pc.MASTER_SHORT 就 lanczos 放大，pc.DELIVER 交付编码并写回 AIGC；回读 AIGC，缺即报错。→ 写回的标签"""
    tags = aigc.collect(takes)
    m = pc.probe(mixed)
    size = pc.master_size(m.w, m.h)
    sig = pc.signature([mixed], size=list(size), deliver=list(pc.DELIVER), loud=loudness.PARAMS,
                       bitrate=mux_av.LOUD_BITRATE, acodec=pc.ACODEC, aigc=tags)
    if pc.fresh(final, sig, post):
        print(f"母带：已是最新，跳过（{final.name}）")
    else:
        vf = ["-vf", f"scale={size[0]}:{size[1]}:flags=lanczos,setsar=1"] if size != (m.w, m.h) else []
        encode(mixed, final, vf, [*pc.DELIVER, *aigc.ffmpeg_args(tags)])
        pc.stamp(final, sig, post)
    if tags and (miss := aigc.readback(final, tags)):
        raise SystemExit(f"{final.name} 回读 AIGC 隐式标识缺 {miss}")
    return tags


def timing_inputs(epd: Path, parts: list[segments.Part]) -> list[Path]:
    """字幕时间取决于的文件：各镜 md，在的对齐缓存与 TTS sidecar。"""
    out: list[Path] = []
    for shot, take in dict.fromkeys((p.shot, p.take) for p in parts):
        d = epd / "shots" / shot
        out += [pc.shot_md(d)] + [f for f in (edl.align_path(epd, shot, take), pc.tts_file(d, pc.TTS_POST, ".json"))
                                  if f.is_file()]
    return out


def burned(post: Path, epd: Path, final: Path, parts: list[segments.Part], tags: dict[str, str],
           a: argparse.Namespace) -> Path:
    out = epd / f"{epd.name}_final_burned.mp4"
    sig = pc.signature([final, *timing_inputs(epd, parts)], lang=a.burn_lang, font=a.font,
                       parts=[asdict(p) for p in parts], venc=list(pc.DELIVER), aigc=tags)
    if pc.fresh(out, sig, post):
        print(f"烧录：已是最新，跳过（{out.name}）")
    else:
        subs.burn(final, out, epd, parts, a.burn_lang, a.font, post / f"{out.stem}.ass", extra=aigc.ffmpeg_args(tags),
                  venc=pc.DELIVER)
        pc.stamp(out, sig, post)
    if tags and (miss := aigc.readback(out, tags)):
        raise SystemExit(f"{out.name} 回读 AIGC 隐式标识缺 {miss}")
    return out


def _write_json(p: Path, obj: dict) -> None:
    part = p.with_name(p.name + ".part")
    part.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    part.replace(p)


def archive(post: Path, epd: Path, doc: edl.Edl, outputs: list[Path], inputs: list[Path], rep: dict) -> Path:
    """post/masters/v{版本}/：成片、字幕、segments 与 QC 报告复制进去（不硬链接：集目录里的同名文件下次出片会被重写），
    manifest.json 记全部输入的 sha256、edl 版本与批准信息、QC 结果。版本目录已在：里面的成片与 manifest 记的一致、又与这次
    逐字节相同 → 只把 manifest 的 edl / QC 更新成这次的（如 approved → locked）；否则报错——同一个版本号只对应一条成片。"""
    d = post / MASTERS_SUB / f"v{doc.version:03d}"
    report = qc.report_path(epd, outputs[0])
    now = datetime.datetime.now().isoformat(timespec="seconds")
    shas = {p.name: pc.sha256(p) for p in outputs}
    manifest = {"version": 1, "made_at": now,
                "edl": {"path": pc.rel(doc.path), "version": doc.version, "base_version": doc.base_version,
                        "status": doc.status, "approved_by": doc.approved_by, "sha256": pc.sha256(doc.path)},
                "inputs": {pc.rel(p): pc.sha256(p) for p in dict.fromkeys(inputs)},
                "outputs": shas,
                "qc": {"result": rep["result"], "report": pc.rel(d / report.name),
                       "checks": {k: c["status"] for k, c in rep["checks"].items()}}}
    if d.exists():
        man = d / MANIFEST
        old = json.loads(man.read_text(encoding="utf-8")) if man.is_file() else {}
        kept = {n: pc.sha256(d / n) for n in shas if (d / n).is_file()}
        if old.get("outputs") != shas or kept != shas:
            raise SystemExit(f"{pc.rel(d)} 已存着别的成片，不覆盖：edl 升版本（version = {doc.version + 1}，"
                             f"base_version 写上一个已批准的版本）再出")
        if (old.get("edl"), old.get("qc")) == (manifest["edl"], manifest["qc"]):
            print(f"存档：{pc.rel(d)} 已是这一条成片，跳过")
            return d
        shutil.copy2(report, d / report.name)
        _write_json(man, {**manifest, "made_at": old.get("made_at", now), "updated_at": now})
        print(f"存档：{pc.rel(d)} 成片没变，manifest 的 edl / QC 更新成这次的（status {old.get('edl', {}).get('status')} → {doc.status}）")
        return d
    tmp = d.with_name(d.name + ".part")
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    for p in [*outputs, report]:
        shutil.copy2(p, tmp / p.name)
    _write_json(tmp / MANIFEST, manifest)
    tmp.rename(d)
    print(f"存档 → {pc.rel(d)}（{len(outputs)} 件 + QC 报告 + {MANIFEST}）")
    return d


def proxy(post: Path, epd: Path, tl: Timeline, parts: list[segments.Part], mixed: Path, a: argparse.Namespace) -> Path:
    """代理片：缩到短边 PROXY_SHORT、烧时间码、响度归一（一次编码）→ 烧双语字幕；segments 与 SRT 写在旁边；QC 只报告。"""
    pdir = post / pc.PROXY_SUB
    pdir.mkdir(exist_ok=True)
    stem = f"{epd.name}_v{tl.doc.version:03d}_proxy"
    out, base = pdir / f"{stem}.mp4", pdir / f"{stem}.base.mp4"
    m = pc.probe(mixed)
    w, h = pc.scale_short(m.w, m.h, PROXY_SHORT)
    edge = round(min(w, h) * 0.02)
    vf = (f"scale={w}:{h}:flags=lanczos,setsar=1,drawtext=font='{a.font}':text='{TIMECODE}':x={edge}:y={edge}:"
          f"fontsize={round(min(w, h) * 0.045)}:fontcolor=white:borderw=2")
    sig = pc.signature([mixed], vf=vf, enc=list(pc.MEZZ), loud=loudness.PARAMS, bitrate=mux_av.LOUD_BITRATE, acodec=pc.ACODEC)
    if not pc.fresh(base, sig):
        encode(mixed, base, ["-vf", vf], list(pc.MEZZ))
        pc.stamp(base, sig)
    segments.write(pdir / f"{stem}.segments.json", parts)
    subs.write_srts(epd, parts, pdir / stem, "both", w, h)
    sig = pc.signature([base, *timing_inputs(epd, parts)], font=a.font, parts=[asdict(p) for p in parts])
    if pc.fresh(out, sig):
        print(f"代理片：已是最新，跳过（{out.name}）")
    else:
        subs.burn(base, out, epd, parts, "both", a.font, pdir / f"{stem}.ass")
        pc.stamp(out, sig)
    try:
        qc.run(out, tl.plan, epd, selftest=True)
    except SystemExit as e:
        print(f"代理片 QC 只报告、不拦（代理片本来就不带 AIGC、不是母带尺寸与码率）：{e}")
    return out


def main() -> int:
    pc.utf8_console()
    ap = argparse.ArgumentParser(description="一集收尾：调色 → 切段 → 拼接 → 混音 → 响度 → 成片 / 烧字幕 / SRT → QC → 存档")
    ap.add_argument("drama")
    ap.add_argument("ep")
    ap.add_argument("--audio-mode", choices=AUDIO_MODES, default=None)
    ap.add_argument("--shots", default=None, help="没有 edl 时：如 1-7,9；默认从第一镜起连续有出片的镜")
    ap.add_argument("--proxy", action="store_true", help="按当前 edl 出代理片（post/proxy/），不出成片")
    ap.add_argument("--grade", action="store_true", help="先做全集分组调色")
    ap.add_argument("--ref", action="append", default=[])
    ap.add_argument("--strength", type=float, default=0.7)
    ap.add_argument("--bgm", type=Path, default=None)
    ap.add_argument("--bgm-volume", type=float, default=None)
    ap.add_argument("--lang", choices=("src", "zh", "both"), default="both", help="SRT 出哪几种")
    ap.add_argument("--burn-lang", choices=("src", "zh", "both"), default="src")
    ap.add_argument("--font", default=subs.FONT)
    ap.add_argument("--python", type=Path, default=pc.POST_PYTHON, help="跑调色 / demucs 的解释器")
    a = ap.parse_args()
    drama = pc.drama_root(a.drama)
    epd = pc.ep_dir(drama, a.ep)
    mode = audio_mode(drama, a.audio_mode)
    post = epd / pc.POST_DIR
    post.mkdir(exist_ok=True)
    has_edl = edl.edl_path(epd).is_file()
    if a.proxy and not has_edl:
        raise SystemExit(f"--proxy 按 edl 出片，{pc.rel(edl.edl_path(epd))} 还没有：先跑 edl.py init")
    tl = from_edl(drama, epd, post, a) if has_edl else whole_shots(drama, epd, post, a)
    head = (f"edl v{tl.doc.version}（{tl.doc.status}）{len(tl.parts)} 个事件" if tl.doc
            else f"{len(tl.parts)} 镜整镜顺接（{tl.parts[0].shot}–{tl.parts[-1].shot}）")
    print(f"{drama.name} {epd.name}：{head}，{tl.parts[-1].end:.2f}s，音频模式 {mode}")
    final = epd / f"{epd.name}_final.mp4"
    body = pc.probe(tl.files[0])
    size = pc.master_size(body.w, body.h)
    if not a.proxy and (dense := subs.too_dense(epd, tl.parts, a.lang, *size)):
        raise SystemExit(f"字幕读不完 {len(dense)} 条（qc Q7 同一口径），不出母带：\n  " + "\n  ".join(dense)
                         + "\n——剧本层把这几句改短或给更长的时间窗（重出片），或剪辑层把所在事件的出点往后放")
    parts = bodies.dx_gains(tl.parts, tl.takes, tl.aligns) if mode == "native" else tl.parts
    cut = bodies.concat(post, epd, tl.files, parts)
    mixed, audio_in = mix(post, epd, mode, cut, parts, tl.takes, a)
    if a.proxy:
        print(f"代理片 → {proxy(post, epd, tl, parts, mixed, a)}")
        return 0

    tags = master(post, mixed, list(tl.takes.values()), final)
    seg_file = final.with_name(final.stem + ".segments.json")
    segments.write(seg_file, parts)
    srts = subs.write_srts(epd, parts, final.with_suffix(""), a.lang, *size)
    for old in (final.with_name(final.stem + s) for s in subs.SRT_SUFFIXES.values()):
        if old not in srts:
            old.unlink(missing_ok=True)          # 这次没出的语言：别让旧时间线的字幕留在成片旁边、被 QC 与观众读到
    burn = burned(post, epd, final, parts, tags, a)
    rep = qc.run(final, tl.plan, epd)
    outputs = [final, burn, *srts, seg_file]
    if tl.doc:
        grades = [c for c in tl.clips if c not in tl.takes.values()]
        plan_json = edl.out_dir(epd) / edl.PLAN_NAME
        archive(post, epd, tl.doc, outputs, [*tl.takes.values(), *grades, tl.doc.path, plan_json,
                                             *timing_inputs(epd, parts), *audio_in], rep)
    print("产物：" + "、".join(p.name for p in outputs) + f"（{epd}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
