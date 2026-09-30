# -*- coding: utf-8 -*-
"""成片的段：逐段出统一规格的中间片（post/bodies/，逐段落盘可续跑）→ 逐事件对白配平 → 一次拼接。

- 整镜顺接（没有 edl）：seam_concat._render_body，与改版前逐字节同一套（承接缝两侧剪 TRIM、末帧定格补音轨尾巴）。
- edl 事件：源片 CFR 时间线上的第 fin–fout 帧 → {镜}.{take}.{fin}-{fout}.mov（pc.MEZZ 视频 + PCM 音频）；
  同一段源片被几个事件引用（闪前）只切一次。
- 对白配平（native）：本段里画内对白（align 的 speech 区间）的 BS.1770 门控响度拉向 pc.DX_TARGET，夹在 ±GAIN_MAX_DB。
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import post_common as pc
import edl
import qc
import segments
import seam_concat   # tools/ 下的，post_common 已把 tools/ 加进 sys.path

BODIES_SUB = "bodies"
TRIM = 0.10                  # 承接缝每侧剪掉的秒数（seam_concat --trim 的默认值）
GAIN_MAX_DB = 8.0
CONCAT_TOL_S = 0.05


def canvas(clips: list[Path]) -> tuple[int, int]:
    ms = [pc.probe(c) for c in clips]
    return max(m.w for m in ms), max(m.h for m in ms)


def legacy(post: Path, dirs: list[Path], clips: list[Path]) -> list[tuple[Path, pc.Seg, float]]:
    """逐镜用 seam_concat._render_body 出统一规格的片段（post/bodies/，可续跑），并量出每段在成片里的真实长度
    （帧率取整、末帧定格补音轨尾巴都会让它和源片差几帧，推算会逐镜累积漂移，所以只信量出来的）。→ [(片段, 段, 头上剪掉的秒数)]"""
    ffm = seam_concat._ffmpeg_exe()
    probes = [seam_concat._probe(ffm, c) for c in clips]
    fps = max(1, round(probes[0][1]))
    w = max(p[2] for p in probes) or 720
    h = max(p[3] for p in probes) or 1280
    seams = [pc.is_chengjie(pc.shot_md(d)) for d in dirs[1:]]
    (post / BODIES_SUB).mkdir(exist_ok=True)
    out, t = [], 0.0
    for i, (d, src, pr) in enumerate(zip(dirs, clips, probes)):
        head = TRIM if i > 0 and seams[i - 1] else 0.0
        tail = TRIM if i < len(seams) and seams[i] else 0.0
        body = post / BODIES_SUB / f"{d.name}.mp4"
        sig = pc.signature([src], head=head, tail=tail, fps=fps, w=w, h=h)
        if not pc.fresh(body, sig):
            part = body.with_name(body.stem + ".part.mp4")
            seam_concat._render_body(ffm, src, head, tail, pr[0], fps, w, h, part)
            part.replace(body)
            pc.stamp(body, sig)
        m = pc.probe(body)
        out.append((body, pc.Seg(d.name, t, max(m.v_dur, m.a_dur)), head))     # concat 滤镜按每段最长的流对齐
        t += out[-1][1].dur
    return out


def event(post: Path, src: Path, c: edl.Cut, w: int, h: int) -> Path:
    """源片第 fin–fout 帧（fps 滤镜转成 CFR 后的帧号，与 edl 的 1/FPS 取整同一时间线）→ 中间片。
    音频用 PCM：每帧正好 AR / FPS 个样本，段长逐样本精确，拼接不累积漂移。"""
    out = post / BODIES_SUB / f"{c.shot}.{c.take}.{c.fin:05d}-{c.fout:05d}.mov"
    sig = pc.signature([src], take=c.take, fin=c.fin, fout=c.fout, fps=pc.FPS, w=w, h=h, ar=pc.AR, enc=list(pc.MEZZ))
    if pc.fresh(out, sig):
        return out
    out.parent.mkdir(exist_ok=True)
    dur = c.dur
    ins: list[str | Path] = ["-i", src]
    fc = [f"[0:v]fps={pc.FPS},trim=start_frame={c.fin}:end_frame={c.fout},setpts=PTS-STARTPTS,"
          + seam_concat._norm(w, h, pc.FPS) + "[v]"]
    if pc.probe(src).has_audio:
        fc.append(f"[0:a]atrim=start={c.src_in:.6f}:end={c.src_out:.6f},asetpts=PTS-STARTPTS,aresample={pc.AR},"
                  f"apad=whole_len={round(dur * pc.AR)}[a]")      # 按样本数补（apad=whole_dur 偶尔不补，见 indextts_dub.place）
    else:
        ins += ["-f", "lavfi", "-i", f"anullsrc=r={pc.AR}:cl=stereo"]
        fc.append("[1:a]anull[a]")
    part = out.with_name(out.stem + ".part.mov")
    pc.run([pc.FFMPEG, "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", *pc.MEZZ,
            "-c:a", "pcm_s16le", "-ar", str(pc.AR), "-ac", "2", "-t", f"{dur:.6f}", part])
    got = pc.probe(part).v_dur
    if abs(got - dur) > edl.HALF_FRAME:
        raise SystemExit(f"{c.id} {c.shot}：切出来 {got:.3f}s，事件要第 {c.fin}–{c.fout} 帧 {dur:.3f}s——源片帧数不够："
                         f"take 比对齐缓存记的短？重跑 align.py --force --shots {pc.shot_no(Path(c.shot))} 再出")
    part.replace(out)
    pc.stamp(out, sig)
    return out


def events(post: Path, cuts: list[edl.Cut], clips: dict[str, Path]) -> list[tuple[Path, segments.Part]]:
    """edl 事件 → [(中间片, 段)]；段长就是 plan 的帧数，起点逐段累加。"""
    w, h = canvas(list(dict.fromkeys(clips.values())))
    out, t = [], 0.0
    for c in cuts:
        out.append((event(post, clips[c.shot], c, w, h),
                    segments.Part(c.id, c.shot, c.take, c.src_in, c.src_out, t, c.dur, 0.0)))
        t += c.dur
    return out


def dx_gains(parts: list[segments.Part], takes: dict[str, Path],
             aligns: dict[tuple[str, str], edl.Align]) -> list[segments.Part]:
    """native：每段画内对白（align 的 speech 区间，裁到本段源片范围）的门控响度 → 增益 DX_TARGET − 实测，夹在 ±GAIN_MAX_DB；
    本段没有画内对白、或短到凑不满一个 400 ms 门控块 → 0。测量与门控用 qc 的同一套（qc.Q6 查接缝对白跳变也用它）。"""
    blocks: dict[Path, list[tuple[float, float]]] = {}
    out = []
    for p in parts:
        spans = [(max(a, p.src_in), min(b, p.src_out)) for a, b in aligns[(p.shot, p.take)].speech
                 if a < p.src_out and b > p.src_in]
        take = takes[p.shot]
        if spans and take not in blocks:
            blocks[take] = qc.momentary(take)
        lufs = qc.gated_lufs(blocks[take], spans) if spans else None
        gain = 0.0 if lufs is None else round(max(-GAIN_MAX_DB, min(GAIN_MAX_DB, pc.DX_TARGET - lufs)), 2)
        print(f"  对白配平 {p.event} {p.shot}：" + ("本段没有可测的画内对白，0 dB" if lufs is None else
                                                f"实测 {lufs:.1f} LUFS → {gain:+.1f} dB（目标 {pc.DX_TARGET:g}）"))
        out.append(replace(p, gain_db=gain))
    return out


def concat(post: Path, epd: Path, files: list[Path], parts: list[segments.Part]) -> Path:
    """各段按 seam_concat 的合成法相接：每段音频乘本段对白配平增益、两端 10 ms 微淡入淡出（不重叠、不改时长），
    concat 滤镜一次编码（pc.MEZZ）→ post/{ep}_concat.mp4。"""
    out = post / f"{epd.name}_concat.mp4"
    sig = pc.signature(files, gains=[p.gain_db for p in parts], enc=list(pc.MEZZ), ar=pc.AR, acodec=pc.ACODEC)
    if pc.fresh(out, sig):
        print(f"拼接：已是最新，跳过（{out.name}）")
        return out
    fade = seam_concat._SEAM_FADE_S
    cmd: list[str | Path] = [pc.FFMPEG, "-y"]
    af = []
    for k, (f, p) in enumerate(zip(files, parts)):
        cmd += ["-i", f]
        gain = f"volume={p.gain_db:g}dB," if p.gain_db else ""
        af.append(f"[{k}:a]aresample={pc.AR},{gain}afade=t=in:st=0:d={fade},"
                  f"afade=t=out:st={max(0.0, p.dur - fade):.3f}:d={fade}[a{k}]")
    labels = "".join(f"[{k}:v][a{k}]" for k in range(len(files)))
    part = out.with_name(out.stem + ".part.mp4")
    pc.run(cmd + ["-filter_complex", ";".join(af + [f"{labels}concat=n={len(files)}:v=1:a=1[v][a]"]),
                  "-map", "[v]", "-map", "[a]", *pc.MEZZ, "-c:a", pc.ACODEC, "-ar", str(pc.AR), "-ac", "2",
                  "-movflags", "+faststart", part])
    part.replace(out)
    total, got = parts[-1].end, pc.probe(out).v_dur
    if abs(total - got) > CONCAT_TOL_S:
        raise SystemExit(f"拼接片 {got:.3f}s，各段合计 {total:.3f}s——concat 没按段长对齐，字幕与 TTS 会错位")
    pc.stamp(out, sig)
    print(f"拼接：{len(files)} 段，{got:.2f}s → {out.name}")
    return out
